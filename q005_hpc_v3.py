#!/usr/bin/env python3
"""
Bubbleverse Q-005 HPC V3

Creates and runs a frozen LambdaCDM/EDE numerical gate using:
- mAxiCLASS pinned commit
- ACT DR6-lite pinned commit
- Planck low-l EE sroll2
- DESI DR2 BAO
- explicit BBN omega_b prior
- optional explicit H0DN prior for the diagnostic hybrid run

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

    packages_path = ROOT / cfg["packages_path"]
    report["paths"]["packages_path"] = {"path": str(packages_path), "exists": packages_path.exists()}

    for mod in ("cobaya", "yaml", "numpy", "scipy", "pybobyqa", "act_dr6_cmbonly"):
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
    report["status"] = "PASS" if all(must_pass) else "FAIL"

    outdir = ROOT / cfg["results_dir"]
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "q005_preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def prior_lambda(mean: float, sigma: float, name: str) -> str:
    return f"lambda {name}: stats.norm.logpdf({name}, loc={mean!r}, scale={sigma!r})"


def build_model(cfg: dict[str, Any], model_name: str, smoke: bool = False) -> dict[str, Any]:
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

    likelihood = cfg["likelihoods"]["common"]

    priors = {
        "bbn_omega_b": prior_lambda(
            cfg["priors"]["bbn_omega_b"]["mean"],
            cfg["priors"]["bbn_omega_b"]["sigma"],
            "omega_b",
        )
    }
    if model.get("local_h0_prior"):
        priors["h0dn"] = prior_lambda(
            cfg["priors"]["h0dn"]["mean"],
            cfg["priors"]["h0dn"]["sigma"],
            "H0",
        )

    sampler = cfg["sampler"]
    if smoke:
        sampler = {
            "minimize": {
                "method": "bobyqa",
                "ignore_prior": True,
                "max_evals": 80,
                "best_of": 1,
                "seed": 1701,
                "override_bobyqa": {"rhoend": 0.2},
            }
        }

    output = str((ROOT / cfg["results_dir"] / f"{model_name}{'_smoke' if smoke else ''}").resolve())

    return {
        "packages_path": packages_path,
        "output": output,
        "force": True,
        "debug": False,
        "theory": {
            "classy": {
                "path": theory_path,
                "extra_args": extra_args,
            }
        },
        "likelihood": likelihood,
        "params": params,
        "prior": priors,
        "sampler": sampler,
    }


def render(cfg: dict[str, Any], smoke: bool = False) -> list[Path]:
    d = ROOT / cfg["rendered_dir"]
    d.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in ("lcdm", "ede", "ede_local"):
        p = d / f"q005_{name}{'_smoke' if smoke else ''}.yaml"
        p.write_text(yaml.safe_dump(build_model(cfg, name, smoke=smoke), sort_keys=False), encoding="utf-8")
        paths.append(p)
        log(f"Rendered {p}")
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
        p = subprocess.run(
            ["cobaya-run", str(yaml_path)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=f,
            stderr=subprocess.STDOUT,
        )
    runtime = time.time() - t0
    log(f"{yaml_path.name}: exit={p.returncode}, runtime={runtime:.1f}s, log={log_path}")
    return p.returncode


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
    chi2_terms = [float(v) for k, v in out.items() if isinstance(v, (float, int)) and k.startswith("chi2__")]
    if chi2_terms:
        out["chi2_like_total"] = sum(chi2_terms)
    return out


def collect(cfg: dict[str, Any]) -> dict[str, Any]:
    rdir = ROOT / cfg["results_dir"]
    summary: dict[str, Any] = {
        "project": cfg["project"]["id"],
        "actual_results_status": "NOT_YET_COMPUTED",
        "models": {},
        "gates": {},
        "provenance": {
            "config_sha256": sha256_file(ROOT / "q005_hpc_v3_config.yml"),
            "script_sha256": sha256_file(ROOT / "q005_hpc_v3.py"),
        }
    }

    complete = True
    for name in ("lcdm", "ede", "ede_local"):
        prefix = rdir / name
        one = find_bestfit(prefix)
        if one is None:
            summary["models"][name] = {"status": "NOT_COMPUTED"}
            complete = False
        else:
            summary["models"][name] = {"status": "COMPUTED", "bestfit": parse_onepoint(one)}

    if complete:
        summary["actual_results_status"] = "COMPUTED"
        lcdm = summary["models"]["lcdm"]["bestfit"]
        ede = summary["models"]["ede"]["bestfit"]
        if "chi2_like_total" in lcdm and "chi2_like_total" in ede:
            delta = float(ede["chi2_like_total"]) - float(lcdm["chi2_like_total"])
            summary["gates"]["delta_chi2_ede_minus_lcdm"] = delta
            floor = cfg["gates"]["theory_precision"]["delta_chi2_floor"]
            summary["gates"]["theory_precision_interpretation"] = (
                "ABOVE_NUMERICAL_FLOOR" if abs(delta) >= floor else "BELOW_NUMERICAL_FLOOR"
            )
        h0 = ede.get("H0")
        if isinstance(h0, (float, int)):
            threshold = cfg["gates"]["high_h0_without_local_prior"]["threshold"]
            summary["gates"]["ede_high_h0_without_local_prior"] = {
                "threshold": threshold,
                "value": h0,
                "pass": h0 >= threshold,
            }

    out = rdir / "q005_results_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    log(f"Wrote {out}")
    return summary


def nesting_gate(cfg: dict[str, Any]) -> dict[str, Any]:
    # This gate is deliberately a generated config pair, not a fabricated result.
    # It creates a near-LCDM EDE point at f_EDE = epsilon for direct evaluation/minimization.
    eps = cfg["gates"]["nesting"]["epsilon_fraction_axion_ac"]
    base = build_model(cfg, "ede", smoke=True)
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
    ap.add_argument("--config", default="q005_hpc_v3_config.yml")
    ap.add_argument("action", choices=["preflight", "render", "smoke", "run", "collect", "all", "nesting"])
    ap.add_argument("--model", choices=["lcdm", "ede", "ede_local", "all"], default="all")
    args = ap.parse_args()

    cfg = load_cfg(ROOT / args.config)

    if args.action == "preflight":
        rep = preflight(cfg)
        print(json.dumps(rep, indent=2))
        return 0 if rep["status"] == "PASS" else 2

    if args.action == "render":
        render(cfg, smoke=False)
        return 0

    if args.action == "nesting":
        print(json.dumps(nesting_gate(cfg), indent=2))
        return 0

    if args.action in ("smoke", "run"):
        smoke = args.action == "smoke"
        paths = render(cfg, smoke=smoke)
        wanted = paths if args.model == "all" else [p for p in paths if f"_{args.model}" in p.stem]
        rc = 0
        for p in wanted:
            rc = max(rc, cobaya_run(p, cfg))
        collect(cfg)
        return rc

    if args.action == "collect":
        print(json.dumps(collect(cfg), indent=2))
        return 0

    if args.action == "all":
        rep = preflight(cfg)
        if rep["status"] != "PASS":
            log("Preflight failed. Main scientific run blocked.", "ERROR")
            return 2
        render(cfg, smoke=True)
        for p in sorted((ROOT / cfg["rendered_dir"]).glob("q005_*_smoke.yaml")):
            if cobaya_run(p, cfg) != 0:
                log("Smoke test failed. Main scientific run blocked.", "ERROR")
                collect(cfg)
                return 3
        nesting_gate(cfg)
        render(cfg, smoke=False)
        for p in sorted((ROOT / cfg["rendered_dir"]).glob("q005_*.yaml")):
            if "_smoke" in p.name or "nesting_epsilon" in p.name:
                continue
            if cobaya_run(p, cfg) != 0:
                log(f"Scientific run failed: {p.name}", "ERROR")
                collect(cfg)
                return 4
        collect(cfg)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
