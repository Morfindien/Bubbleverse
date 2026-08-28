#!/usr/bin/env python3
"""Bubbleverse Q-005 HPC V14 — common-backend differential gate.

This program deliberately separates:
  1) executable common-backend tests that can be run now, from
  2) exact K-036/K-038 paper-native reproductions whose source provenance
     is still blocked.

No numerical result is invented. A result exists only after Cobaya succeeds.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q005_hpc_v14_config.yml"


def log(msg: str, level: str = "INFO") -> None:
    print(f"[{level}] {msg}", flush=True)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_cfg(name: str = DEFAULT_CONFIG) -> dict[str, Any]:
    return load_yaml(ROOT / name)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(cmd: list[str], cwd: Path | None = None, check: bool = True,
            env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    log("$ " + " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if p.stdout:
        print(p.stdout, end="")
    if p.stderr:
        print(p.stderr, end="", file=sys.stderr)
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}")
    return p


def git_head(path: Path) -> str:
    return run_cmd(["git", "rev-parse", "HEAD"], cwd=path).stdout.strip()


def source_lock(cfg: dict[str, Any], quiet: bool = False) -> dict[str, Any]:
    p = ROOT / cfg["source_lock_file"]
    out: dict[str, Any] = {
        "q": cfg["project"]["q"],
        "project": cfg["project"]["id"],
        "path": str(p),
        "status": "FAIL",
        "checks": {},
    }
    if not p.exists():
        out["checks"]["exists"] = False
        if not quiet:
            print(json.dumps(out, indent=2))
        return out

    lock = json.loads(p.read_text(encoding="utf-8"))
    out["checks"]["exists"] = True
    out["checks"]["q_match"] = lock.get("q") == cfg["project"]["q"]
    out["checks"]["project_match"] = lock.get("project") == cfg["project"]["id"]

    c = lock.get("common_backend", {})
    expected = cfg["frozen_software"]["class_ede"]
    out["checks"]["common_repo_match"] = c.get("repository") == expected["repository"]
    out["checks"]["common_commit_match"] = c.get("commit") == expected["commit"]
    out["checks"]["common_backend_frozen"] = c.get("status") == "FROZEN_FOR_COMMON_BACKEND_TEST"

    native = lock.get("native_source_gates", {})
    out["native_source_gates"] = native
    out["claim_boundary"] = lock.get("claim_boundary", {})
    out["status"] = "PASS" if all(out["checks"].values()) else "FAIL"

    if not quiet:
        print(json.dumps(out, indent=2))
    return out


def repo_check(name: str, spec: dict[str, Any]) -> dict[str, Any]:
    p = ROOT / spec["path"]
    d = {
        "name": name,
        "path": str(p),
        "exists": p.exists(),
        "expected_commit": spec["commit"],
        "actual_commit": None,
        "pass": False,
    }
    if p.exists() and (p / ".git").exists():
        try:
            d["actual_commit"] = git_head(p)
            d["pass"] = d["actual_commit"] == d["expected_commit"]
        except Exception as e:
            d["error"] = repr(e)
    return d


def package_version(dist: str) -> str:
    try:
        return importlib.metadata.version(dist)
    except Exception as e:
        return f"NOT_INSTALLED ({e})"


def preflight(cfg: dict[str, Any]) -> dict[str, Any]:
    lock = source_lock(cfg, quiet=True)
    report: dict[str, Any] = {
        "q": cfg["project"]["q"],
        "project": cfg["project"]["id"],
        "status": "FAIL",
        "source_lock": lock,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {},
        "repositories": {},
        "imports": {},
        "paths": {},
    }
    report["q_identity_gate"] = cfg["q_memory"]["q_id"] == "Q-005"
    report["source_lock_gate"] = lock["status"] == "PASS"
    report["python_gate"] = platform.python_version().startswith(cfg["frozen_software"]["python"] + ".")

    # FIX6: the frozen class_ede fEDE/log10z_c shooting map is singular/ill-conditioned
    # at fEDE -> 0 (its source contains dxdy ~ 1/fEDE). Keep the EDE effective
    # parameter model on a positive finite domain; LCDM is represented separately.
    ede_min = float(cfg["common_ede_priors"]["fEDE"]["prior"]["min"])
    nest_eps = float(cfg["gates"]["nesting"]["epsilon_fEDE"])
    report["ede_numerical_domain_gate"] = (
        math.isfinite(ede_min) and math.isfinite(nest_eps)
        and ede_min > 0.0 and nest_eps >= ede_min
    )

    packages = [
        ("cobaya", "cobaya"),
        ("PyYAML", "pyyaml"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("Py-BOBYQA", "py_bobyqa"),
        ("Cython", "cython"),
    ]
    for dist, key in packages:
        expected = cfg["frozen_software"][key]
        actual = package_version(dist)
        report["packages"][dist] = {
            "expected": expected,
            "actual": actual,
            "pass": actual == expected,
        }

    report["repositories"]["class_ede"] = repo_check(
        "class_ede", cfg["frozen_software"]["class_ede"])
    report["repositories"]["act_dr6_lite"] = repo_check(
        "act_dr6_lite", cfg["frozen_software"]["act_dr6_lite"])

    class_root = (ROOT / cfg["frozen_software"]["class_ede"]["path"]).resolve()
    build_root = class_root / "python" / "build"
    build_libs = sorted(build_root.glob("lib.*")) if build_root.exists() else []
    products: list[Path] = []
    for lib in build_libs:
        products.extend(lib.glob("classy*.so"))
    report["paths"]["class_build"] = {
        "build_root": str(build_root),
        "lib_dirs": [str(x) for x in build_libs],
        "classy_products": [str(x) for x in products],
        "pass": bool(products),
    }

    # V14 FIX4:
    # GitHub Actions starts each workflow step in a fresh shell. The setup step
    # exports PYTHONPATH, but that shell-local export does not survive into the
    # later `python q005_hpc_v14.py ...` step. Register the frozen CLASS_EDE
    # build paths inside this process before the preflight import gate.
    class_python_paths = [
        *(str(x.resolve()) for x in build_libs),
        str(class_root),
        str(class_root / "python"),
    ]
    for p in reversed(class_python_paths):
        if p not in sys.path:
            sys.path.insert(0, p)
    importlib.invalidate_caches()
    report["paths"]["class_python_path"] = {
        "entries": class_python_paths,
        "pass": bool(build_libs),
    }

    packages_path = (ROOT / cfg["packages_path"]).resolve()
    act = cfg["frozen_software"]["act_dr6_data"]
    act_file = packages_path / "data" / act["data_folder"] / act["version"] / act["filename"]
    report["paths"]["act_data"] = {
        "path": str(act_file),
        "exists": act_file.exists(),
        "size": act_file.stat().st_size if act_file.exists() else None,
        "pass": act_file.exists() and act_file.stat().st_size > 0,
    }

    for mod in ["cobaya", "yaml", "numpy", "scipy", "pybobyqa", "Cython",
                "act_dr6_cmbonly"]:
        try:
            m = importlib.import_module(mod)
            report["imports"][mod] = {"pass": True, "file": getattr(m, "__file__", None)}
        except Exception as e:
            report["imports"][mod] = {"pass": False, "error": repr(e)}

    try:
        classy = importlib.import_module("classy")
        path = Path(classy.__file__).resolve()
        report["imports"]["classy"] = {
            "pass": str(path).startswith(str(class_root)),
            "file": str(path),
            "required_prefix": str(class_root),
        }
    except Exception as e:
        report["imports"]["classy"] = {"pass": False, "error": repr(e)}

    mandatory = [
        report["q_identity_gate"],
        report["source_lock_gate"],
        report["python_gate"],
        report["ede_numerical_domain_gate"],
        *(x["pass"] for x in report["packages"].values()),
        *(x["pass"] for x in report["repositories"].values()),
        report["paths"]["class_build"]["pass"],
        report["paths"]["class_python_path"]["pass"],
        report["paths"]["act_data"]["pass"],
        *(x["pass"] for x in report["imports"].values()),
    ]
    report["status"] = "PASS" if all(mandatory) else "FAIL"

    d = ROOT / cfg["results_dir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "q005_v14_preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def gaussian_likelihood(mean: float, sigma: float, parameter: str) -> dict[str, str]:
    return {"external": f"lambda {parameter}: stats.norm.logpdf({parameter}, loc={mean!r}, scale={sigma!r})"}


def resolve_model(cfg: dict[str, Any], name: str) -> dict[str, Any]:
    if name not in cfg["models"]:
        raise KeyError(f"Unknown model {name}")
    m = copy.deepcopy(cfg["models"][name])
    if "inherit_model" in m:
        base = resolve_model(cfg, m["inherit_model"])
        base.update({k: v for k, v in m.items() if k != "inherit_model"})
        m = base
    return m


def common_reference(params: dict[str, Any]) -> dict[str, float]:
    refs: dict[str, float] = {}
    for k, v in params.items():
        if not isinstance(v, dict):
            continue
        ref = v.get("ref")
        if isinstance(ref, dict) and "loc" in ref:
            refs[k] = float(ref["loc"])
    return refs


def freeze_likelihood_nuisance_refs(likelihood: dict[str, Any]) -> dict[str, float]:
    """Freeze likelihood-local nuisance parameters to identical documented refs.

    Cobaya's evaluate sampler otherwise draws each nuisance from its `ref`
    distribution independently for each model evaluation. That invalidates a
    fixed-point nesting/continuity comparison because the models are not being
    evaluated at the same nuisance point.
    """
    frozen: dict[str, float] = {}
    for _, spec in likelihood.items():
        if not isinstance(spec, dict):
            continue
        pmap = spec.get("params")
        if not isinstance(pmap, dict):
            continue
        for pname, pspec in list(pmap.items()):
            if not isinstance(pspec, dict):
                continue
            ref = pspec.get("ref")
            if isinstance(ref, dict) and "loc" in ref:
                value = float(ref["loc"])
            elif isinstance(ref, (int, float)):
                value = float(ref)
            else:
                continue
            keep = {}
            if "latex" in pspec:
                keep["latex"] = pspec["latex"]
            keep["value"] = value
            pmap[pname] = keep
            frozen[pname] = value
    return frozen


def build_model(cfg: dict[str, Any], model_name: str, *, smoke: bool = False,
                restart: int = 0, fixed_common: bool = False,
                nesting_epsilon: float | None = None) -> dict[str, Any]:
    m = resolve_model(cfg, model_name)
    theory_path = str((ROOT / cfg["frozen_software"]["class_ede"]["path"]).resolve())
    packages_path = str((ROOT / cfg["packages_path"]).resolve())

    params = copy.deepcopy(cfg["parameters"]["common"])
    extra_args = copy.deepcopy(cfg["theory"]["common_extra_args"])

    # FIX5: Cobaya's CLASS component only auto-claims a non-exhaustive subset of
    # varied parameters. Because the explicit BBN likelihood also consumes
    # omega_b, omega_b can otherwise be routed away from CLASS. Declare the
    # physical CLASS inputs explicitly. logA is intentionally NOT here: it is a
    # dropped sampling parameter whose transformed value A_s is the CLASS input.
    theory_input_params = [
        "omega_b", "omega_cdm", "H0", "tau_reio", "n_s", "A_s"
    ]

    kind = m["kind"]

    if kind == "ede":
        params.update(copy.deepcopy(cfg["common_ede_priors"]))
        theory_input_params.extend(["fEDE", "log10z_c", "thetai_scf"])
        extra_args.update({
            "Omega_Lambda": 0,
            "Omega_fld": 0,
            "Omega_scf": -1,
            "scf_parameters": "1,1,1,1,1,0.0",
            "attractor_ic_scf": "no",
            "CC_scf": 1,
            "scf_tuning_index": 3,
            "n_scf": int(m["n_scf"]),
        })
        if nesting_epsilon is not None:
            params["fEDE"] = {"value": float(nesting_epsilon)}
            params["log10z_c"] = {"value": 3.55}
            params["thetai_scf"] = {"value": 2.80}

    elif kind == "varying_me":
        params["varying_me"] = copy.deepcopy(m["varying_me"])
        theory_input_params.append("varying_me")
        extra_args.update({
            "varying_fundamental_constants": "instantaneous",
            "varying_alpha": 1.0,
            "varying_transition_redshift": float(m["varying_transition_redshift"]),
        })

    likelihood = copy.deepcopy(cfg["likelihoods"]["common"])
    bbn = cfg["scientific_gaussian_constraints"]["bbn_omega_b"]
    likelihood["bbn_omega_b"] = gaussian_likelihood(bbn["mean"], bbn["sigma"], "omega_b")

    if m.get("local_h0_likelihood", False):
        h = cfg["scientific_gaussian_constraints"]["h0dn"]
        likelihood["h0dn"] = gaussian_likelihood(h["mean"], h["sigma"], "H0")

    if fixed_common:
        refs = common_reference(cfg["parameters"]["common"])
        for k, val in refs.items():
            if k in params and k not in ("A_s",):
                params[k] = {"value": val}

        # FIX7: a nesting/continuity gate must evaluate every model at the same
        # nuisance point. ACT's A_act/P_act live inside the likelihood block, so
        # they were previously being independently drawn by sampler.evaluate.
        # Freeze all likelihood-local nuisances with reference locations.
        frozen_nuisance = freeze_likelihood_nuisance_refs(likelihood)
    else:
        frozen_nuisance = {}

    if smoke or fixed_common:
        sampler: dict[str, Any] = {"evaluate": {}}
    else:
        sampler = copy.deepcopy(cfg["sampler"])
        sampler["minimize"]["best_of"] = 1
        sampler["minimize"]["seed"] = int(cfg["sampler"]["minimize"].get("seed", 1701)) + restart

    suffix = "_smoke" if smoke else f"_r{restart}"
    if fixed_common:
        suffix = "_fixed"
        if nesting_epsilon is not None:
            suffix += "_nest"
    output = str((ROOT / cfg["results_dir"] / f"{model_name}{suffix}").resolve())

    return {
        "packages_path": packages_path,
        "output": output,
        "force": True,
        "debug": False,
        "theory": {
            "classy": {
                "path": theory_path,
                "ignore_obsolete": bool(cfg["frozen_software"]["class_ede"]["cobaya_ignore_obsolete"]),
                "input_params": theory_input_params,
                "extra_args": extra_args,
            }
        },
        "likelihood": likelihood,
        "params": params,
        "sampler": sampler,
    }


def render(cfg: dict[str, Any], model: str, *, smoke: bool = False,
           restart: int = 0, fixed_common: bool = False,
           nesting_epsilon: float | None = None) -> Path:
    d = ROOT / cfg["rendered_dir"]
    d.mkdir(parents=True, exist_ok=True)
    tag = "smoke" if smoke else f"r{restart}"
    if fixed_common:
        tag = "fixed" if nesting_epsilon is None else "nest"
    path = d / f"q005_v14_{model}_{tag}.yaml"
    obj = build_model(cfg, model, smoke=smoke, restart=restart,
                      fixed_common=fixed_common, nesting_epsilon=nesting_epsilon)
    path.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
    return path


def cobaya_run(path: Path, cfg: dict[str, Any]) -> int:
    env = os.environ.copy()
    class_root = (ROOT / cfg["frozen_software"]["class_ede"]["path"]).resolve()
    build_root = class_root / "python" / "build"
    libs = sorted(build_root.glob("lib.*"))
    python_path_parts = [str(x.resolve()) for x in libs] + [str(class_root), str(class_root / "python")]
    env["PYTHONPATH"] = os.pathsep.join(python_path_parts + [env.get("PYTHONPATH", "")])
    env["COBAYA_PACKAGES_PATH"] = str((ROOT / cfg["packages_path"]).resolve())

    logs = ROOT / cfg["logs_dir"]
    logs.mkdir(parents=True, exist_ok=True)
    logfile = logs / f"{path.stem}.log"

    t0 = time.time()
    with logfile.open("w", encoding="utf-8") as f:
        p = subprocess.Popen(["cobaya-run", str(path)], cwd=ROOT, env=env,
                             text=True, stdout=f, stderr=subprocess.STDOUT)
        next_heartbeat = time.time() + 300
        while p.poll() is None:
            time.sleep(5)
            if time.time() >= next_heartbeat:
                log(f"HEARTBEAT {path.name}: {(time.time()-t0)/60:.1f} min")
                next_heartbeat = time.time() + 300
        rc = int(p.returncode or 0)

    log(f"{path.name}: exit={rc}; runtime={(time.time()-t0)/60:.1f} min; log={logfile}")
    if rc:
        try:
            print(logfile.read_text(errors="replace")[-12000:], file=sys.stderr)
        except Exception:
            pass
    return rc


def parse_onepoint(path: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    lines = [x.strip() for x in path.read_text(errors="replace").splitlines() if x.strip()]
    if len(lines) < 2:
        return {"parse_status": "INSUFFICIENT_LINES", "raw_file": str(path)}
    header = lines[0].lstrip("#").split()
    values = lines[-1].split()
    if len(header) != len(values):
        return {"parse_status": "COLUMN_MISMATCH", "raw_file": str(path)}
    out: dict[str, Any] = {"parse_status": "PASS", "raw_file": str(path)}
    for k, v in zip(header, values):
        try:
            out[k] = float(v)
        except ValueError:
            out[k] = v

    components: dict[str, float] = {}
    for label, keys in cfg["likelihood_accounting"]["aliases"].items():
        for key in keys:
            if isinstance(out.get(key), (int, float)):
                components[label] = float(out[key])
                break
    out["chi2_nonoverlap"] = components
    return out


def finite_scientific_point(parsed: dict[str, Any], required: list[str] | set[str]) -> tuple[bool, str]:
    """Require a parsed one-point result with finite, non-overlapping chi2 terms."""
    if parsed.get("parse_status") != "PASS":
        return False, "PARSE_FAILURE"
    comps = parsed.get("chi2_nonoverlap", {})
    missing = sorted(set(required) - set(comps))
    if missing:
        return False, "MISSING_COMPONENTS:" + ",".join(missing)
    bad = []
    for k in required:
        try:
            v = float(comps[k])
        except Exception:
            bad.append(k)
            continue
        if not math.isfinite(v):
            bad.append(k)
    if bad:
        return False, "NONFINITE_COMPONENTS:" + ",".join(sorted(bad))
    return True, "PASS"


def find_onepoint(prefix: Path) -> Path | None:
    candidates = [
        Path(str(prefix) + ".bestfit.txt"),
        Path(str(prefix) + ".minimum.txt"),
        Path(str(prefix) + ".1.txt"),
    ]
    for p in candidates:
        if p.exists():
            return p
    found = sorted(prefix.parent.glob(prefix.name + "*.txt"))
    return found[0] if found else None


def collect(cfg: dict[str, Any], model: str, restart: int) -> dict[str, Any]:
    prefix = ROOT / cfg["results_dir"] / f"{model}_r{restart}"
    p = find_onepoint(prefix)
    result: dict[str, Any] = {
        "q": "Q-005",
        "project": cfg["project"]["id"],
        "model": model,
        "restart": restart,
        "seed": int(cfg["sampler"]["minimize"].get("seed", 1701)) + restart,
        "claim": cfg["project"]["claim"],
        "status": "FAIL",
    }
    if p is None:
        result["reason"] = "NO_ONEPOINT_RESULT_FOUND"
    else:
        best = parse_onepoint(p, cfg)
        result["bestfit"] = best
        required = set(cfg["likelihood_accounting"]["required_nonlocal"])
        m = resolve_model(cfg, model)
        if m.get("local_h0_likelihood", False):
            required.add("h0dn")
        got = set(best.get("chi2_nonoverlap", {}))
        missing = sorted(required - got)
        result["missing_likelihood_components"] = missing
        finite_ok, finite_reason = finite_scientific_point(best, required)
        result["finite_scientific_gate"] = finite_ok
        if finite_ok:
            total = sum(float(best["chi2_nonoverlap"][k]) for k in required)
            result["chi2_scientific_total"] = total
            result["status"] = "PASS"
        else:
            result["reason"] = finite_reason

    out = ROOT / cfg["results_dir"] / f"q005_job_result_{model}_r{restart}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


def plan(cfg: dict[str, Any], kind: str, restarts: int) -> dict[str, Any]:
    rs = cfg["runtime_safety"]
    restarts = max(1, min(int(restarts), int(rs["max_restarts"])))
    if kind == "smoke":
        return {"model": list(rs["enabled_models"])}
    if kind == "production":
        return {"include": [
            {"model": model, "restart": r}
            for model in rs["enabled_models"]
            for r in range(restarts)
        ]}
    if kind == "h0dn":
        return {"include": [
            {"model": model, "restart": r}
            for model in rs["enabled_h0dn_models"]
            for r in range(restarts)
        ]}
    raise ValueError(kind)


def nesting(cfg: dict[str, Any]) -> dict[str, Any]:
    """Validate the frozen EDE backend on its finite, numerically safe domain.

    IMPORTANT:
    The exact mathematical nesting point fEDE=0 cannot be evaluated through the
    frozen class_ede fEDE/log10z_c shooting parameterization. At the production
    floor fEDE=0.001 the EDE models are still genuine, model-dependent EDE
    cosmologies, so their chi2 is NOT required to match LCDM.

    This gate therefore authorizes production iff LCDM, EDE n=3 and EDE n=2
    all evaluate successfully and return finite scientific likelihood terms at
    the same fixed cosmological and likelihood-nuisance reference point.
    Delta-chi2 values are retained as diagnostics only.
    """
    eps = float(cfg["gates"]["nesting"]["epsilon_fEDE"])
    models = [("lcdm", None), ("ede_n3", eps), ("ede_n2", eps)]
    records: dict[str, Any] = {}

    for name, epsilon in models:
        p = render(cfg, name, fixed_common=True, nesting_epsilon=epsilon)
        rc = cobaya_run(p, cfg)
        record: dict[str, Any] = {"exit": rc, "yaml": str(p)}
        if rc == 0:
            prefix = ROOT / cfg["results_dir"] / f"{name}_fixed"
            if epsilon is not None:
                prefix = ROOT / cfg["results_dir"] / f"{name}_fixed_nest"
            one = find_onepoint(prefix)
            if one:
                parsed = parse_onepoint(one, cfg)
                required = cfg["likelihood_accounting"]["required_nonlocal"]
                finite_ok, finite_reason = finite_scientific_point(parsed, required)
                record["finite_scientific_gate"] = finite_ok
                record["bestfit"] = parsed
                if finite_ok:
                    record["chi2"] = sum(float(parsed["chi2_nonoverlap"][k]) for k in required)
                else:
                    record["reason"] = finite_reason
            else:
                record["finite_scientific_gate"] = False
                record["reason"] = "NO_ONEPOINT_RESULT"
        else:
            record["finite_scientific_gate"] = False
            record["reason"] = f"COBAYA_EXIT_{rc}"
        records[name] = record

    all_finite = all(
        records[m].get("exit") == 0
        and records[m].get("finite_scientific_gate") is True
        and isinstance(records[m].get("chi2"), (int, float))
        and math.isfinite(float(records[m]["chi2"]))
        for m, _ in models
    )

    deltas: dict[str, Any] = {}
    if all_finite:
        base = float(records["lcdm"]["chi2"])
        for m in ("ede_n3", "ede_n2"):
            deltas[m] = float(records[m]["chi2"]) - base

    # Document the identical nuisance point used by all three evaluate runs.
    nuisance_reference = {}
    common_like = copy.deepcopy(cfg["likelihoods"]["common"])
    nuisance_reference.update(freeze_likelihood_nuisance_refs(common_like))

    status = "PASS" if all_finite else "FAIL"
    exact_nesting_status = cfg["gates"]["nesting"].get(
        "exact_nesting_status", "BLOCKED_FROZEN_SHOOTING_LIMIT"
    )

    out = {
        "q": "Q-005",
        "project": cfg["project"]["id"],
        "test": "EDE_COMMON_BACKEND_FINITE_DOMAIN_GATE",
        "fixed_likelihood_nuisance_reference": nuisance_reference,
        "mode": cfg["gates"]["nesting"].get("mode", "BACKEND_FINITE_DOMAIN_VALIDATION"),
        "ede_production_floor": float(cfg["common_ede_priors"]["fEDE"]["prior"]["min"]),
        "epsilon_fEDE": eps,
        "epsilon_interpretation": "finite EDE-domain validation point; not mathematical fEDE=0",
        "exact_nesting_status": exact_nesting_status,
        "exact_nesting_reason": (
            "Frozen class_ede fEDE/log10z_c shooting is numerically ill-conditioned "
            "as fEDE approaches zero, so exact LCDM nesting is not asserted by this gate."
        ),
        "pass_criteria": [
            "all three Cobaya evaluate runs exit 0",
            "all required scientific likelihood components are finite",
            "all models use the same fixed cosmological reference point",
            "all likelihood-local nuisance parameters are frozen to identical ref.loc values",
        ],
        "delta_chi2_role": "DIAGNOSTIC_ONLY_NOT_A_PASS_FAIL_CRITERION",
        "records": records,
        "delta_chi2_vs_lcdm": deltas,
        "production_authorized": all_finite,
        "status": status,
    }
    path = ROOT / cfg["results_dir"] / "q005_nesting_v14.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("source-lock")
    sub.add_parser("preflight")

    pplan = sub.add_parser("plan")
    pplan.add_argument("--kind", choices=["smoke", "production", "h0dn"], required=True)
    pplan.add_argument("--restarts", type=int, default=None)
    pplan.add_argument("--json", action="store_true")

    pr = sub.add_parser("render")
    pr.add_argument("--model", required=True)
    pr.add_argument("--restart", type=int, default=0)
    pr.add_argument("--smoke", action="store_true")

    runp = sub.add_parser("run")
    runp.add_argument("--model", required=True)
    runp.add_argument("--restart", type=int, default=0)
    runp.add_argument("--smoke", action="store_true")

    cp = sub.add_parser("collect")
    cp.add_argument("--model", required=True)
    cp.add_argument("--restart", type=int, required=True)

    sub.add_parser("nesting")

    args = ap.parse_args()
    cfg = load_cfg(args.config)

    if cfg["project"]["q"] != "Q-005" or cfg["q_memory"]["q_id"] != "Q-005":
        log("Q_IDENTITY_GATE = FAIL", "ERROR")
        return 90

    if args.cmd == "source-lock":
        return 0 if source_lock(cfg)["status"] == "PASS" else 2

    if args.cmd == "preflight":
        r = preflight(cfg)
        print(json.dumps(r, indent=2))
        return 0 if r["status"] == "PASS" else 3

    if args.cmd == "plan":
        lock = source_lock(cfg, quiet=True)
        if lock["status"] != "PASS":
            if args.json:
                print(json.dumps({"error": "SOURCE_LOCK_FAIL"}, separators=(",", ":")))
            return 4
        restarts = args.restarts or cfg["runtime_safety"]["default_restarts"]
        obj = plan(cfg, args.kind, restarts)
        print(json.dumps(obj, separators=(",", ":") if args.json else None))
        return 0

    if args.cmd == "render":
        print(render(cfg, args.model, smoke=args.smoke, restart=args.restart))
        return 0

    if args.cmd == "run":
        pf = preflight(cfg)
        if pf["status"] != "PASS":
            log("PREFLIGHT = FAIL", "ERROR")
            return 5
        y = render(cfg, args.model, smoke=args.smoke, restart=args.restart)
        rc = cobaya_run(y, cfg)
        if rc != 0:
            return rc
        if args.smoke:
            prefix = ROOT / cfg["results_dir"] / f"{args.model}_smoke"
            one = find_onepoint(prefix)
            if one is None:
                log("SMOKE_FINITE_GATE = FAIL: no one-point result", "ERROR")
                return 8
            parsed = parse_onepoint(one, cfg)
            required = set(cfg["likelihood_accounting"]["required_nonlocal"])
            m = resolve_model(cfg, args.model)
            if m.get("local_h0_likelihood", False):
                required.add("h0dn")
            finite_ok, finite_reason = finite_scientific_point(parsed, required)
            if not finite_ok:
                log(f"SMOKE_FINITE_GATE = FAIL: {finite_reason}", "ERROR")
                logfile = ROOT / cfg["logs_dir"] / f"{y.stem}.log"
                if logfile.exists():
                    try:
                        print(logfile.read_text(errors="replace")[-16000:], file=sys.stderr)
                    except Exception:
                        pass
                return 8
            log("SMOKE_FINITE_GATE = PASS")
        return 0

    if args.cmd == "collect":
        r = collect(cfg, args.model, args.restart)
        return 0 if r["status"] == "PASS" else 6

    if args.cmd == "nesting":
        pf = preflight(cfg)
        if pf["status"] != "PASS":
            return 5
        r = nesting(cfg)
        return 0 if r["status"] == "PASS" else 7

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
