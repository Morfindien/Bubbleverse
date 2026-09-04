#!/usr/bin/env python3
"""
Bubbleverse Q019 — Planck cosmological reprofile V1

CURRENT Q: Q019

Purpose
-------
Reprofile the same MOD-EDE-N3 cosmology independently on:
  1) Q016 matched/CamSpec-lite Planck likelihood
  2) Q017 full-multifrequency CamSpec Planck likelihood

Both branches use the same sampled cosmological parameterization, hard bounds,
Cobaya minimizer semantics, and explicit normalization-free Gaussian constraint
shapes. The full-MF branch alone carries its architecture-native foreground
nuisance degrees of freedom.

This program does NOT:
- sum chi2 values across likelihood constructions;
- treat Q015-Q018 as independent Planck observations;
- interpret the Q018 architecture gap as a physical chi2 component;
- infer a causal Planck systematic;
- reopen Q016 globality or Q017's INDETERMINATE classification.

Execution:
  plan
  profile
  aggregate-primary
  cross-profile
  aggregate-final
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import signal
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q019"
RUN = "Q019-PLANCK-COSMOLOGY-REPROFILE-V1"
RESULT = "R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-001"

ARCHITECTURES = ("lite", "full_mf")
MODES = ("reference_free_h0", "fixed_h0_71p5")
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
LITE_LIKE = "q019_camspec_npipe_lite"
TARGET_H0 = 71.5

COSMO_SAMPLED = (
    "omega_b", "omega_cdm", "tau_reio", "n_s", "logA",
    "fEDE", "log10z_c", "thetai_scf", "H0",
)
COSMO_REPORT = COSMO_SAMPLED + (
    "A_s", "Omega_m", "sigma8", "S8", "rs_drag",
)
SHARED_NUISANCE = ("A_planck", "calTE", "calEE")
FULL_FOREGROUND = (
    "amp_143", "amp_217", "amp_143x217",
    "n_143", "n_217", "n_143x217",
)
ALL_FULL_NUISANCE = SHARED_NUISANCE + FULL_FOREGROUND

# Deterministic multi-start patterns. They perturb reference points only;
# parameter priors/bounds are never changed.
JITTER = {
    "omega_b": 4.0e-5,
    "omega_cdm": 6.0e-4,
    "tau_reio": 0.003,
    "n_s": 0.0015,
    "logA": 0.004,
    "fEDE": 0.004,
    "log10z_c": 0.020,
    "thetai_scf": 0.030,
    "H0": 0.20,
    "A_planck": 0.0008,
    "calEE": 0.002,
    "calTE": 0.002,
    "amp_143": 0.20,
    "amp_143x217": 0.20,
    "amp_217": 0.20,
    "n_143": 0.04,
    "n_143x217": 0.04,
    "n_217": 0.04,
}
PATTERNS = ("base", "plus", "minus", "cross_a", "cross_b", "ede_cross")
CROSS_A = {
    "omega_b": 1, "omega_cdm": -1, "tau_reio": 1, "n_s": -1,
    "logA": 1, "fEDE": -1, "log10z_c": 1, "thetai_scf": -1, "H0": 1,
    "A_planck": -1, "calEE": 1, "calTE": -1,
    "amp_143": 1, "amp_143x217": -1, "amp_217": 1,
    "n_143": -1, "n_143x217": 1, "n_217": -1,
}
CROSS_B = {k: -v for k, v in CROSS_A.items()}
EDE_CROSS = {
    "fEDE": 1, "log10z_c": -1, "thetai_scf": 1, "H0": 1,
    "omega_b": -1, "omega_cdm": 1, "n_s": 1, "tau_reio": -1, "logA": 1,
}


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                 encoding="utf-8")
    os.replace(t, p)


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if float(c["profile"]["target_h0"]) != TARGET_H0:
        raise RuntimeError("H0_TARGET_GATE=FAIL")
    if c["objective"]["basis"] != (
        "LIKELIHOOD_CHI2_PLUS_EXPLICIT_NORMALIZATION_FREE_SHARED_GAUSSIAN_SHAPES"
    ):
        raise RuntimeError("OBJECTIVE_IDENTITY_GATE=FAIL")
    return c


def load_source_lock(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / c["provenance"]["source_lock"]
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("q") != Q or d.get("run_id") != RUN:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d["model"]["backend_commit"] != c["model"]["backend_commit"]:
        raise RuntimeError("SOURCE_LOCK_MODEL_GATE=FAIL")
    return d


def load_q016_endpoint_lock(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / c["parents"]["q016"]["endpoint_lock"]
    d = json.loads(p.read_text(encoding="utf-8"))
    planck = d.get("endpoints", {}).get("planck", {})
    free = planck.get("reference_free_h0", {})
    fixed = planck.get("fixed_h0_71p5", {})
    if abs(float(free["minimum"]["H0"]) - 67.988328967159) > 1e-10:
        raise RuntimeError("Q016_FREE_ENDPOINT_GATE=FAIL")
    if abs(float(free["objective_chi2"]) - 4197.77132517269) > 1e-9:
        raise RuntimeError("Q016_FREE_OBJECTIVE_REFERENCE_GATE=FAIL")
    if abs(float(fixed["objective_chi2"]) - 4203.595181947479) > 1e-9:
        raise RuntimeError("Q016_FIXED_OBJECTIVE_REFERENCE_GATE=FAIL")
    return d


def endpoint_seed(lock: Mapping[str, Any], mode: str) -> dict[str, float]:
    row = lock["endpoints"]["planck"][mode]["minimum"]
    out: dict[str, float] = {}
    for k, v in row.items():
        if finite(v):
            out[str(k)] = float(v)
    if mode == "fixed_h0_71p5":
        out["H0"] = TARGET_H0
    return out


def shape_logp(x: float, mu: float, sigma: float) -> float:
    z = (float(x) - float(mu)) / float(sigma)
    return -0.5 * z * z


def make_shape_like(name: str, mu: float, sigma: float) -> dict[str, Any]:
    def f(**kwargs):
        return shape_logp(kwargs[name], mu, sigma)
    f.__name__ = f"q019_shape_{name}"
    return {"external": f, "input_params": [name]}


def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and "prior" in spec


def set_ref(params: dict[str, Any], name: str, value: float) -> None:
    spec = params.get(name)
    if not sampled(spec):
        return
    x = float(value)
    pr = spec.get("prior", {})
    if isinstance(pr, Mapping) and finite(pr.get("min")) and finite(pr.get("max")):
        lo, hi = float(pr["min"]), float(pr["max"])
        eps = max((hi - lo) * 1e-7, 1e-12)
        x = min(max(x, lo + eps), hi - eps)
    spec["ref"] = x


def ref_value(spec: Any) -> float | None:
    if not isinstance(spec, Mapping):
        return None
    r = spec.get("ref")
    if finite(r):
        return float(r)
    if isinstance(r, Mapping) and finite(r.get("loc")):
        return float(r["loc"])
    pr = spec.get("prior")
    if isinstance(pr, Mapping):
        if finite(pr.get("loc")):
            return float(pr["loc"])
        if finite(pr.get("min")) and finite(pr.get("max")):
            return 0.5 * (float(pr["min"]) + float(pr["max"]))
    return None


def bounded_perturb(base: Mapping[str, float], params: Mapping[str, Any],
                    pattern: str) -> dict[str, float]:
    out = dict(base)
    if pattern == "base":
        return out
    if pattern == "plus":
        signs = {k: 1 for k in JITTER}
    elif pattern == "minus":
        signs = {k: -1 for k in JITTER}
    elif pattern == "cross_a":
        signs = CROSS_A
    elif pattern == "cross_b":
        signs = CROSS_B
    elif pattern == "ede_cross":
        signs = EDE_CROSS
    else:
        raise RuntimeError("RESTART_PATTERN_GATE=FAIL")

    changed = 0
    for name, dv in JITTER.items():
        if name not in out or name not in params:
            continue
        s = float(signs.get(name, 0))
        if s == 0:
            continue
        x0 = float(out[name])
        x = x0 + s * float(dv)
        spec = params.get(name)
        if isinstance(spec, Mapping):
            pr = spec.get("prior")
            if isinstance(pr, Mapping) and finite(pr.get("min")) and finite(pr.get("max")):
                lo, hi = float(pr["min"]), float(pr["max"])
                eps = max((hi - lo) * 1e-6, 1e-10)
                if x <= lo + eps or x >= hi - eps:
                    x = x0 - s * float(dv)
                x = min(max(x, lo + eps), hi - eps)
        if x != x0:
            changed += 1
        out[name] = x
    if pattern != "base" and changed == 0:
        raise RuntimeError("NONZERO_PERTURBATION_GATE=FAIL")
    return out


def q014_base(restart: int, output_prefix: Path, c: Mapping[str, Any]):
    import q014_external_viability_v12 as q14
    q14cfg = q14.load_cfg("q014_external_viability_v12_config.yml")
    info, _ = q14.impl.build_info(
        "planck_npipe_k039_approx",
        "reference_free_h0",
        "external",
        int(restart),
        q14cfg,
        {},
        output_prefix,
        max_evals=int(c["execution"]["max_evals"]),
    )
    return copy.deepcopy(info)


def configure_common_objective(info: dict[str, Any], c: Mapping[str, Any]) -> None:
    # No normalized prior densities in the optimizer scalar. Priors remain as hard
    # support/reference geometry. Shared Gaussian shapes are explicit likelihoods.
    m = info.setdefault("sampler", {}).setdefault("minimize", {})
    m["method"] = "bobyqa"
    m["ignore_prior"] = True
    m["best_of"] = 1
    m["max_evals"] = int(c["execution"]["max_evals"])
    m.setdefault("override_bobyqa", {})["rhoend"] = float(c["execution"]["rhoend"])
    info["prior"] = {}
    for name, spec in c["objective"]["shared_gaussian_shapes"].items():
        info["likelihood"][f"q019_shape_{name}"] = make_shape_like(
            name, float(spec["mean"]), float(spec["sigma"])
        )


def build_lite(c: Mapping[str, Any], mode: str, restart: int, prefix: Path,
               seed: Mapping[str, float]) -> dict[str, Any]:
    # Reuse Q016's audited lite construction.
    import q016_objective_reprofile_v16 as q16
    qc = {
        "model": {"target_h0": TARGET_H0},
        "execution": {
            "optimizer": {
                "best_of": 1,
                "max_evals": int(c["execution"]["max_evals"]),
                "rhoend": float(c["execution"]["rhoend"]),
            }
        },
    }
    info = q16.base_info(qc, "planck", mode, restart, prefix)
    q16.configure_planck(info, qc)
    # Rename only the local dictionary key for Q019 identity; component class is unchanged.
    old = q16.PRIMARY_LIKE["planck"]
    info["likelihood"][LITE_LIKE] = info["likelihood"].pop(old)
    configure_common_objective(info, c)
    params = info["params"]
    for name, value in seed.items():
        set_ref(params, name, value)
    return info


def build_full(c: Mapping[str, Any], mode: str, restart: int, prefix: Path,
               seed: Mapping[str, float]) -> dict[str, Any]:
    info = q014_base(restart, prefix, c)
    if FULL_LIKE not in info.get("likelihood", {}):
        raise RuntimeError("FULL_MF_LIKELIHOOD_GATE=FAIL")
    info["likelihood"] = {FULL_LIKE: info["likelihood"][FULL_LIKE]}
    if mode == "fixed_h0_71p5":
        info["params"]["H0"] = TARGET_H0
    configure_common_objective(info, c)
    for name, value in seed.items():
        set_ref(info["params"], name, value)
    return info


def prior_support_signature(info: Mapping[str, Any], include_h0: bool = True) -> str:
    payload = {}
    for name in COSMO_SAMPLED:
        if name == "H0" and not include_h0:
            continue
        spec = info.get("params", {}).get(name)
        if not sampled(spec):
            continue
        pr = copy.deepcopy(spec.get("prior"))
        payload[name] = pr
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


def architecture_nuisance(info: Mapping[str, Any]) -> list[str]:
    out = []
    for name, spec in info.get("params", {}).items():
        if sampled(spec) and name not in COSMO_SAMPLED:
            out.append(str(name))
    return sorted(out)


def build_info(c: Mapping[str, Any], lock: Mapping[str, Any],
               architecture: str, mode: str, restart: int, prefix: Path,
               frozen_cosmology: Mapping[str, float] | None = None):
    seed = endpoint_seed(lock, mode if mode in MODES else "reference_free_h0")
    if architecture == "lite":
        info = build_lite(c, mode if mode in MODES else "reference_free_h0",
                          restart, prefix, seed)
    elif architecture == "full_mf":
        info = build_full(c, mode if mode in MODES else "reference_free_h0",
                          restart, prefix, seed)
    else:
        raise RuntimeError("ARCHITECTURE_GATE=FAIL")

    params = info["params"]
    start = {}
    for name, spec in params.items():
        if sampled(spec):
            rv = ref_value(spec)
            if rv is not None:
                start[name] = rv

    if frozen_cosmology is not None:
        # Cross-surface test: freeze all actual sampled cosmological parameters
        # to the opposite architecture's best free optimum.
        missing = []
        for name in COSMO_SAMPLED:
            if sampled(params.get(name)):
                if name not in frozen_cosmology or not finite(frozen_cosmology[name]):
                    missing.append(name)
                else:
                    params[name] = float(frozen_cosmology[name])
        if missing:
            raise RuntimeError("CROSS_COSMOLOGY_COMPLETENESS_GATE=FAIL " + repr(missing))
    else:
        pattern = PATTERNS[int(restart)]
        pert = bounded_perturb(start, params, pattern)
        for name, value in pert.items():
            set_ref(params, name, value)

    info["output"] = str(prefix.resolve())
    info["force"] = True
    return info


class SoftStop(Exception):
    pass


def _alarm(_sig, _frame):
    raise SoftStop()


def minimum_row(sampler: Any, prefix: Path) -> tuple[dict[str, Any], str | None]:
    import q017_planck_direction_localization_v1 as q17
    return q17.minimum_row(sampler, prefix)


def serial_cosmology(row: Mapping[str, Any], mode: str) -> dict[str, float]:
    out = {}
    for name in COSMO_REPORT:
        if name in row and finite(row[name]):
            out[name] = float(row[name])
    if mode == "fixed_h0_71p5":
        out["H0"] = TARGET_H0
    return out


def serial_nuisance(row: Mapping[str, Any], names: list[str]) -> dict[str, float]:
    return {n: float(row[n]) for n in names if n in row and finite(row[n])}


def run_profile(c: Mapping[str, Any], lock: Mapping[str, Any],
                architecture: str, mode: str, restart: int, output: str | Path) -> int:
    if architecture not in ARCHITECTURES or mode not in MODES:
        raise RuntimeError("PROFILE_IDENTITY_GATE=FAIL")
    if restart < 0 or restart >= len(PATTERNS):
        raise RuntimeError("RESTART_GATE=FAIL")
    prefix = Path(output).with_suffix("")
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "PRIMARY_PROFILE",
        "architecture": architecture, "mode": mode, "restart": restart,
        "restart_pattern": PATTERNS[restart],
        "status": "FAILED", "actual_computed_result": False,
        "cross_chain_chi2_sum_allowed": False,
    }
    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info = build_info(c, lock, architecture, mode, restart, prefix)
        rec["cosmology_prior_support_signature"] = prior_support_signature(
            info, include_h0=(mode == "reference_free_h0")
        )
        nuis = architecture_nuisance(info)
        rec["sampled_nuisance"] = nuis
        from cobaya.run import run as cobaya_run
        _updated, sampler = cobaya_run(info, force=True)
        row, source = minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        # Exact optimizer scalar: all retained Gaussian shape terms are likelihood
        # components and ignore_prior=True.
        obj = float(row["chi2"])
        rec.update({
            "status": "COMPLETE",
            "actual_computed_result": True,
            "objective_chi2": obj,
            "objective_basis": c["objective"]["basis"],
            "cosmology": serial_cosmology(row, mode),
            "nuisance": serial_nuisance(row, nuis),
            "minimum": row,
            "harvested_minimum_path": source,
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                    "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def collect_records(path: str | Path, stage: str) -> list[dict[str, Any]]:
    rows = []
    for p in Path(path).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage:
            rows.append(d)
    return rows


def best_primary(rows: list[dict[str, Any]], c: Mapping[str, Any]):
    best, stability = {}, {}
    for arch in ARCHITECTURES:
        for mode in MODES:
            cand = [
                r for r in rows
                if r.get("architecture") == arch and r.get("mode") == mode
                and r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))
            ]
            cand.sort(key=lambda r: float(r["objective_chi2"]))
            key = f"{arch}:{mode}"
            if cand:
                best[key] = cand[0]
                vals = [float(r["objective_chi2"]) for r in cand]
                stability[key] = {
                    "complete": len(cand),
                    "best_two_spread": (vals[1] - vals[0]) if len(vals) > 1 else None,
                    "pass": (
                        len(cand) >= int(c["validation"]["minimum_complete_restarts"])
                        and len(vals) > 1
                        and vals[1] - vals[0] <= float(c["validation"]["multistart_delta_objective_max"])
                    ),
                }
    return best, stability


def aggregate_primary(c: Mapping[str, Any], input_dir: str | Path, output: str | Path) -> int:
    rows = collect_records(input_dir, "PRIMARY_PROFILE")
    best, stability = best_primary(rows, c)
    expected = len(ARCHITECTURES) * len(MODES) * len(PATTERNS)
    penalties = {}
    for arch in ARCHITECTURES:
        free = best.get(f"{arch}:reference_free_h0")
        fixed = best.get(f"{arch}:fixed_h0_71p5")
        if free and fixed:
            penalties[arch] = float(fixed["objective_chi2"]) - float(free["objective_chi2"])

    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "PRIMARY_AGGREGATE",
        "status": "COMPLETE" if len(rows) == expected else "PARTIAL",
        "job_manifest": {"expected": expected, "returned": len(rows)},
        "best": best,
        "stability": stability,
        "reprofiled_high_h0_penalties": penalties,
        "q016_reference_penalty": float(c["references"]["q016_lite_penalty"]),
        "q017_frozen_endpoint_penalty": float(c["references"]["q017_full_mf_frozen_penalty"]),
        "q018_architecture_gap_not_physical_component": float(c["references"]["q018_architecture_gap"]),
        "cross_chain_chi2_sum_performed": False,
    }
    write_json(output, out)
    return 0 if out["status"] == "COMPLETE" else 2


def load_primary(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("stage") != "PRIMARY_AGGREGATE":
        raise RuntimeError("PRIMARY_AGGREGATE_IDENTITY_GATE=FAIL")
    return d


def run_cross_profile(c: Mapping[str, Any], lock: Mapping[str, Any],
                      target_arch: str, primary_path: str | Path,
                      output: str | Path) -> int:
    if target_arch not in ARCHITECTURES:
        raise RuntimeError("CROSS_ARCHITECTURE_GATE=FAIL")
    primary = load_primary(primary_path)
    source_arch = "full_mf" if target_arch == "lite" else "lite"
    source = primary["best"].get(f"{source_arch}:reference_free_h0")
    target = primary["best"].get(f"{target_arch}:reference_free_h0")
    if not source or not target:
        raise RuntimeError("CROSS_SOURCE_RESULT_GATE=FAIL")
    foreign_cosmo = source["cosmology"]
    prefix = Path(output).with_suffix("")
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "CROSS_PROFILE",
        "target_architecture": target_arch,
        "source_architecture": source_arch,
        "status": "FAILED", "actual_computed_result": False,
        "foreign_cosmology": foreign_cosmo,
    }
    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info = build_info(
            c, lock, target_arch, "reference_free_h0", 0, prefix,
            frozen_cosmology=foreign_cosmo,
        )
        nuis = architecture_nuisance(info)
        from cobaya.run import run as cobaya_run
        _updated, sampler = cobaya_run(info, force=True)
        row, source_path = minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        obj = float(row["chi2"])
        own = float(target["objective_chi2"])
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": obj,
            "target_own_free_objective": own,
            "cross_objective_cost": obj - own,
            "nuisance": serial_nuisance(row, nuis),
            "minimum": row,
            "harvested_minimum_path": source_path,
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                    "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def parameter_delta(a: Mapping[str, Any], b: Mapping[str, Any]) -> dict[str, Any]:
    out = {}
    for name in COSMO_REPORT:
        if finite(a.get(name)) and finite(b.get(name)):
            x, y = float(a[name]), float(b[name])
            out[name] = {
                "lite": x,
                "full_mf": y,
                "delta_full_minus_lite": y - x,
                "absolute_delta": abs(y - x),
            }
    return out


def aggregate_final(c: Mapping[str, Any], input_dir: str | Path,
                    primary_path: str | Path, output: str | Path) -> int:
    primary = load_primary(primary_path)
    cross = collect_records(input_dir, "CROSS_PROFILE")
    by_target = {
        r["target_architecture"]: r for r in cross
        if r.get("status") == "COMPLETE" and r.get("target_architecture") in ARCHITECTURES
    }
    lite = primary["best"].get("lite:reference_free_h0", {}).get("cosmology", {})
    full = primary["best"].get("full_mf:reference_free_h0", {}).get("cosmology", {})
    deltas = parameter_delta(lite, full)
    costs = {k: float(v["cross_objective_cost"]) for k, v in by_target.items()
             if finite(v.get("cross_objective_cost"))}

    stability_pass = all(
        primary["stability"].get(f"{a}:{m}", {}).get("pass") is True
        for a in ARCHITECTURES for m in MODES
    )
    cross_complete = set(costs) == set(ARCHITECTURES)
    tol = float(c["validation"]["negative_cross_cost_tolerance"])
    cross_nonnegative = cross_complete and all(v >= -tol for v in costs.values())
    material_thr = float(c["validation"]["cross_objective_materiality_threshold"])

    if not stability_pass or not cross_complete or not cross_nonnegative:
        classification = "INDETERMINATE"
    elif any(v > material_thr for v in costs.values()):
        classification = "LIKELIHOOD CHOICE SHIFTS PREFERRED MOD-EDE-N3 REGION"
    else:
        classification = "LIKELIHOOD DEPENDENCE PRIMARILY HIGH-H0 / LOCAL-GEOMETRY"

    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "FINAL_AGGREGATE",
        "execution_status": "COMPLETE" if cross_complete else "PARTIAL",
        "primary": primary,
        "cross_profiles": by_target,
        "free_optimum_parameter_comparison": deltas,
        "cross_objective_costs": costs,
        "classification": classification,
        "interpretation_rules": {
            "cross_objective_threshold": material_thr,
            "threshold_is_statistical_significance": False,
            "no_cross_chain_chi2_sum": True,
            "q018_gap_used_as_physical_component": False,
            "causal_systematic_claim_allowed": False,
            "new_physics_claim_allowed": False,
        },
    }
    write_json(output, out)
    return 0 if out["execution_status"] == "COMPLETE" else 2


def plan(c: Mapping[str, Any], output: str | Path) -> int:
    matrix = []
    for arch in ARCHITECTURES:
        for mode in MODES:
            for restart in range(len(PATTERNS)):
                matrix.append({
                    "architecture": arch,
                    "mode": mode,
                    "restart": restart,
                })
    d = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "PLAN",
        "expected_primary_jobs": len(matrix),
        "matrix": {"include": matrix},
        "cross_targets": list(ARCHITECTURES),
    }
    write_json(output, d)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q019_planck_cosmology_reprofile_v1_config.yml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--output", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--architecture", choices=ARCHITECTURES, required=True)
    p.add_argument("--mode", choices=MODES, required=True)
    p.add_argument("--restart", type=int, required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate-primary")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("cross-profile")
    p.add_argument("--target-architecture", choices=ARCHITECTURES, required=True)
    p.add_argument("--primary", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate-final")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--primary", required=True)
    p.add_argument("--output", required=True)

    args = ap.parse_args()
    c = load_cfg(args.config)
    load_source_lock(c)
    lock = load_q016_endpoint_lock(c)

    if args.cmd == "plan":
        return plan(c, args.output)
    if args.cmd == "profile":
        return run_profile(c, lock, args.architecture, args.mode, args.restart, args.output)
    if args.cmd == "aggregate-primary":
        return aggregate_primary(c, args.input_dir, args.output)
    if args.cmd == "cross-profile":
        return run_cross_profile(c, lock, args.target_architecture, args.primary, args.output)
    if args.cmd == "aggregate-final":
        return aggregate_final(c, args.input_dir, args.primary, args.output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
