#!/usr/bin/env python3
"""
Bubbleverse Q-005 HPC V13

Creates and runs a frozen LambdaCDM/EDE numerical gate using:
- mAxiCLASS pinned commit
- ACT DR6-lite pinned commit
- Planck low-l EE sroll2
- DESI DR2 BAO
- explicit BBN omega_b Gaussian likelihood
- optional explicit H0DN Gaussian likelihood for the diagnostic hybrid run

Execution mode: SERIAL_NO_MPI. MPI is intentionally not required in V3.

This program does NOT invent scientific results. Until Cobaya finishes successfully,
actual numerical results remain NOT YET COMPUTED.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent


def load_cfg(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def log(msg: str, level: str = "INFO") -> None:
    print(f"[{level}] {msg}", flush=True)


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


def check_version(package: str, expected: str) -> tuple[bool, str]:
    try:
        actual = importlib.metadata.version(package)
        return actual == expected, actual
    except Exception as e:
        return False, f"NOT_INSTALLED ({e})"


def repo_check(name: str, spec: dict[str, Any]) -> dict[str, Any]:
    p = ROOT / spec["path"]
    result = {
        "name": name,
        "path": str(p),
        "expected_commit": spec["commit"],
        "exists": p.exists(),
        "actual_commit": None,
        "pass": False,
    }
    if p.exists() and (p / ".git").exists():
        try:
            result["actual_commit"] = git_head(p)
            result["pass"] = result["actual_commit"] == result["expected_commit"]
        except Exception as e:
            result["error"] = str(e)
    return result


def preflight(cfg: dict[str, Any]) -> dict[str, Any]:
    report: dict[str, Any] = {
        "project": cfg["project"]["id"],
        "python": platform.python_version(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "packages": {},
        "repositories": {},
        "imports": {},
        "paths": {},
        "status": "FAIL",
    }

    expected_py = cfg["frozen_software"]["python"]
    report["python_pass"] = platform.python_version().startswith(expected_py + ".")

    package_specs = (
        ("cobaya", "cobaya"),
        ("PyYAML", "pyyaml"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("Py-BOBYQA", "py_bobyqa"),
        ("Cython", "cython"),
    )
    for distribution, cfg_key in package_specs:
        expected = cfg["frozen_software"][cfg_key]
        ok, actual = check_version(distribution, expected)
        report["packages"][distribution] = {
            "expected": expected,
            "actual": actual,
            "pass": ok,
        }

    for name in ("mAxiCLASS", "act_dr6_lite"):
        report["repositories"][name] = repo_check(name, cfg["frozen_software"][name])

    maxiclass_root = ROOT / cfg["frozen_software"]["mAxiCLASS"]["path"]
    build_root = maxiclass_root / "python" / "build"
    build_libs = sorted(build_root.glob("lib.*")) if build_root.exists() else []
    classy_products = []
    for libdir in build_libs:
        classy_products.extend(libdir.glob("classy*.so"))
    report["paths"]["maxiclass_cobaya_build"] = {
        "build_root": str(build_root),
        "lib_dirs": [str(x) for x in build_libs],
        "classy_products": [str(x) for x in classy_products],
        "pass": bool(build_libs and classy_products),
    }

    packages_path = ROOT / cfg["packages_path"]
    report["paths"]["packages_path"] = {"path": str(packages_path), "exists": packages_path.exists()}

    act_data = cfg["frozen_software"]["act_dr6_data"]
    act_file = packages_path / "data" / act_data["data_folder"] / act_data["version"] / act_data["filename"]
    report["paths"]["act_dr6_scientific_data"] = {
        "path": str(act_file),
        "exists": act_file.exists(),
        "size_bytes": act_file.stat().st_size if act_file.exists() else None,
        "pass": act_file.exists() and act_file.stat().st_size > 0,
    }

    for mod in ("cobaya", "yaml", "numpy", "scipy", "pybobyqa", "Cython", "act_dr6_cmbonly"):
        try:
            m = importlib.import_module(mod)
            report["imports"][mod] = {
                "pass": True,
                "file": getattr(m, "__file__", None),
            }
        except Exception as e:
            report["imports"][mod] = {"pass": False, "error": repr(e)}

    # The imported classy must come from the frozen mAxiCLASS tree, not site-packages.
    maxiclass = (ROOT / cfg["frozen_software"]["mAxiCLASS"]["path"]).resolve()
    try:
        classy = importlib.import_module("classy")
        classy_file = Path(classy.__file__).resolve()
        report["imports"]["classy"] = {
            "pass": str(classy_file).startswith(str(maxiclass)),
            "file": str(classy_file),
            "required_prefix": str(maxiclass),
        }
    except Exception as e:
        report["imports"]["classy"] = {"pass": False, "error": repr(e)}

    must_pass = [report["python_pass"]]
    must_pass += [x["pass"] for x in report["packages"].values()]
    must_pass += [x["pass"] for x in report["repositories"].values()]
    must_pass += [x["pass"] for x in report["imports"].values()]
    must_pass.append(report["paths"]["maxiclass_cobaya_build"]["pass"])
    must_pass.append(report["paths"]["act_dr6_scientific_data"]["pass"])
    report["status"] = "PASS" if all(must_pass) else "FAIL"

    outdir = ROOT / cfg["results_dir"]
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "q005_preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def gaussian_external_likelihood(mean: float, sigma: float, name: str) -> dict[str, str]:
    # Scientific Gaussian measurements are likelihoods in V10, not Cobaya priors.
    # Hence sampler.minimize.ignore_prior=true ignores only parameter-prior density,
    # while these terms remain in the optimized scientific objective.
    return {"external": f"lambda {name}: stats.norm.logpdf({name}, loc={mean!r}, scale={sigma!r})"}


def build_model(cfg: dict[str, Any], model_name: str, smoke: bool = False, restart: int = 0) -> dict[str, Any]:
    model = cfg["models"][model_name]
    if "inherit_model" in model:
        base = dict(cfg["models"][model["inherit_model"]])
        base.update(model)
        model = base

    theory_path = str((ROOT / cfg["frozen_software"]["mAxiCLASS"]["path"]).resolve())
    packages_path = str((ROOT / cfg["packages_path"]).resolve())

    params = json.loads(json.dumps(cfg["parameters"]["common"]))
    extra_args = dict(cfg["theory"]["common_extra_args"])

    if model.get("ede"):
        extra_args.update(model.get("extra_args", {}))
        params.update(model.get("params", {}))

    likelihood = json.loads(json.dumps(cfg["likelihoods"]["common"]))
    constraints = cfg.get("scientific_gaussian_constraints", cfg["priors"])
    likelihood["bbn_omega_b"] = gaussian_external_likelihood(
        constraints["bbn_omega_b"]["mean"],
        constraints["bbn_omega_b"]["sigma"],
        "omega_b",
    )
    if model.get("local_h0_prior"):
        likelihood["h0dn"] = gaussian_external_likelihood(
            constraints["h0dn"]["mean"],
            constraints["h0dn"]["sigma"],
            "H0",
        )

    sampler = json.loads(json.dumps(cfg["sampler"]))
    base_seed = int(cfg["sampler"]["minimize"].get("seed", 1701))
    sampler["minimize"]["best_of"] = 1
    sampler["minimize"]["seed"] = base_seed + int(restart)
    if smoke:
        # Smoke means: can the complete frozen theory + likelihood stack initialize
        # and evaluate one physically valid reference point?
        # It must NOT perform a numerical minimization.
        sampler = {"evaluate": {}}

    suffix = "_smoke" if smoke else f"_r{int(restart)}"
    output = str((ROOT / cfg["results_dir"] / f"{model_name}{suffix}").resolve())

    return {
        "packages_path": packages_path,
        "output": output,
        "force": True,
        "debug": False,
        "theory": {
            "classy": {
                "path": theory_path,
                "ignore_obsolete": True,
                "extra_args": extra_args,
            }
        },
        "likelihood": likelihood,
        "params": params,
        "sampler": sampler,
    }


def render(cfg: dict[str, Any], smoke: bool = False, model_name: str | None = None,
           restart: int = 0) -> list[Path]:
    d = ROOT / cfg["rendered_dir"]
    d.mkdir(parents=True, exist_ok=True)
    names = (model_name,) if model_name else ("lcdm", "ede", "ede_local")
    paths = []
    for name in names:
        suffix = "_smoke" if smoke else f"_r{int(restart)}"
        pth = d / f"q005_{name}{suffix}.yaml"
        pth.write_text(
            yaml.safe_dump(build_model(cfg, name, smoke=smoke, restart=restart), sort_keys=False),
            encoding="utf-8",
        )
        paths.append(pth)
        log(f"Rendered {pth}")
    return paths

def cobaya_run(yaml_path: Path, cfg: dict[str, Any]) -> int:
    env = os.environ.copy()
    maxipath = str((ROOT / cfg["frozen_software"]["mAxiCLASS"]["path"]).resolve())
    env["PYTHONPATH"] = maxipath + os.pathsep + env.get("PYTHONPATH", "")
    env["COBAYA_PACKAGES_PATH"] = str((ROOT / cfg["packages_path"]).resolve())
    logs = ROOT / cfg["logs_dir"]
    logs.mkdir(parents=True, exist_ok=True)
    log_path = logs / (yaml_path.stem + ".log")

    t0 = time.time()
    with log_path.open("w", encoding="utf-8") as f:
        proc = subprocess.Popen(
            ["cobaya-run", str(yaml_path)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=f,
            stderr=subprocess.STDOUT,
        )
        next_heartbeat = time.time() + 300
        while proc.poll() is None:
            time.sleep(5)
            now = time.time()
            if now >= next_heartbeat:
                log(f"HEARTBEAT {yaml_path.name}: elapsed={(now-t0)/60:.1f} min, pid={proc.pid}")
                next_heartbeat = now + 300
        rc = int(proc.returncode or 0)

    runtime = time.time() - t0
    log(f"{yaml_path.name}: exit={rc}, runtime={runtime:.1f}s, log={log_path}")
    if rc != 0:
        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")
            print("\n========== COBAYA FAILURE LOG: " + yaml_path.name + " ==========", file=sys.stderr)
            print(text, file=sys.stderr)
            print("========== END COBAYA FAILURE LOG ==========", file=sys.stderr)
        except Exception as e:
            print(f"[WARNING] Could not read failure log {log_path}: {e!r}", file=sys.stderr)
    return rc

def find_bestfit(prefix: Path) -> Path | None:
    candidates = [
        Path(str(prefix) + ".bestfit.txt"),
        Path(str(prefix) + ".minimum.txt"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def parse_onepoint(path: Path) -> dict[str, float | str]:
    lines = [x.strip() for x in path.read_text(errors="replace").splitlines() if x.strip()]
    if len(lines) < 2:
        return {"raw_file": str(path), "parse_status": "INSUFFICIENT_LINES"}
    header = lines[0].lstrip("#").split()
    values = lines[-1].split()
    if len(header) != len(values):
        return {"raw_file": str(path), "parse_status": "COLUMN_MISMATCH"}
    out: dict[str, float | str] = {"raw_file": str(path), "parse_status": "PASS"}
    for k, v in zip(header, values):
        try:
            out[k] = float(v)
        except ValueError:
            out[k] = v
    # V10: never sum every chi2__ column: Cobaya one-point files may contain
    # aggregate and component columns simultaneously. Keep raw columns and select
    # exactly one column per scientific likelihood.
    aliases = {
        "planck_lowl": ["chi2__planck_2018_lowl.EE_sroll2"],
        "act_dr6": ["chi2__act_dr6_cmbonly.ACTDR6CMBonly"],
        "desi_dr2": ["chi2__bao.desi_dr2"],
        "bbn": ["chi2__bbn_omega_b"],
        "h0dn": ["chi2__h0dn"],
    }
    selected = {}
    for label, keys in aliases.items():
        for key in keys:
            if isinstance(out.get(key), (float, int)):
                selected[label] = float(out[key])
                break
    out["chi2_nonoverlap"] = selected
    required = {"planck_lowl", "act_dr6", "desi_dr2", "bbn"}
    if required.issubset(selected):
        out["chi2_scientific_total"] = sum(selected.values())
    return out


def collect(cfg: dict[str, Any], model_name: str | None = None, restart: int | None = None) -> dict[str, Any]:
    rdir = ROOT / cfg["results_dir"]
    summary = {
        "project": cfg["project"]["id"],
        "bubbleverse_q": cfg.get("q_memory", {}).get("q_id", "Q-005"),
        "question": cfg.get("q_memory", {}).get("original_question"),
        "models": {},
        "provenance": {
            "config_sha256": sha256_file(ROOT / "q005_hpc_v13_config.yml"),
            "script_sha256": sha256_file(ROOT / "q005_hpc_v13.py"),
        },
    }
    names = (model_name,) if model_name else ("lcdm", "ede", "ede_local")
    for name in names:
        restarts = [restart] if restart is not None else cfg.get("runtime_safety", {}).get("restart_ids", [0, 1])
        entries = []
        for rid in restarts:
            prefix = rdir / f"{name}_r{int(rid)}"
            one = find_bestfit(prefix)
            if one is None:
                entries.append({"restart": int(rid), "status": "NOT_COMPUTED"})
            else:
                entries.append({
                    "restart": int(rid),
                    "seed": int(cfg["sampler"]["minimize"].get("seed", 1701)) + int(rid),
                    "status": "COMPUTED",
                    "bestfit": parse_onepoint(one),
                })
        summary["models"][name] = {"restarts": entries}
    out = rdir / (
        f"q005_restart_summary_{model_name}_r{restart}.json"
        if model_name is not None and restart is not None
        else "q005_results_summary.json"
    )
    out.write_text(json.dumps(summary, indent=2) + "\n")
    log(f"Wrote {out}")
    return summary

def nesting_gate(cfg: dict[str, Any]) -> dict[str, Any]:
    # This gate is deliberately a generated config pair, not a fabricated result.
    # It creates a near-LCDM EDE point at f_EDE = epsilon for direct evaluation/minimization.
    eps = cfg["gates"]["nesting"]["epsilon_fraction_axion_ac"]
    base = build_model(cfg, "ede", smoke=True, restart=0)
    base["params"]["fraction_axion_ac"] = {"value": eps}
    base["params"]["log10_axion_ac"] = {"value": -3.55}
    base["output"] = str((ROOT / cfg["results_dir"] / "ede_nesting_epsilon").resolve())
    base["sampler"] = {"evaluate": {}}
    p = ROOT / cfg["rendered_dir"] / "q005_ede_nesting_epsilon.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(base, sort_keys=False))
    return {"status": "CONFIG_GENERATED", "epsilon": eps, "config": str(p)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q005_hpc_v13_config.yml")
    ap.add_argument("action", choices=["preflight", "render", "smoke", "run", "collect", "nesting"])
    ap.add_argument("--model", choices=["lcdm", "ede", "ede_local"], default="lcdm")
    ap.add_argument("--restart", type=int, default=0)
    args = ap.parse_args()

    cfg = load_cfg(ROOT / args.config)
    valid_restarts = set(cfg.get("runtime_safety", {}).get("restart_ids", [0, 1]))
    if args.restart not in valid_restarts:
        raise SystemExit(f"Invalid restart {args.restart}; expected one of {sorted(valid_restarts)}")

    if args.action == "preflight":
        rep = preflight(cfg)
        print(json.dumps(rep, indent=2))
        return 0 if rep["status"] == "PASS" else 2
    if args.action == "render":
        render(cfg, smoke=False, model_name=args.model, restart=args.restart)
        return 0
    if args.action == "nesting":
        print(json.dumps(nesting_gate(cfg), indent=2))
        return 0
    if args.action in ("smoke", "run"):
        smoke = args.action == "smoke"
        paths = render(cfg, smoke=smoke, model_name=args.model, restart=args.restart)
        rc = cobaya_run(paths[0], cfg)
        if not smoke:
            collect(cfg, model_name=args.model, restart=args.restart)
        return rc
    if args.action == "collect":
        print(json.dumps(collect(cfg, model_name=args.model, restart=args.restart), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
