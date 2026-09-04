#!/usr/bin/env python3
"""
Bubbleverse Q017 V1 — Planck full-multifrequency direction localization.

Scientific contract
-------------------
CURRENT Q: Q017

This program does NOT reopen Q016 cosmological globality and does NOT substitute
the historical Q011 vector. It freezes the certified Q016 Planck cosmological
endpoints and profiles ONLY the chain-native Planck NPIPE/CamSpec multifrequency
nuisance parameters.

Execution layers:
1. nuisance-only multistart profiles at the certified Q016 free/fixed endpoints;
2. leave-one-nuisance-group-locked profiles at the fixed H0=71.5 endpoint,
   locking the tested group to its free-endpoint nuisance optimum;
3. covariance-aware frequency/multipole decomposition at the selected nuisance
   optima, reusing Q015's proven full-CamSpec residual evaluator as a closure
   reference;
4. finite aggregation/classification into:
   SPECIFIC PLANCK DIRECTION LOCALIZED
   BROADLY DISTRIBUTED PLANCK PENALTY
   INDETERMINATE

Signed frequency/covariance allocations are diagnostics, not independent chi2
tests and not causal proof of an instrumental systematic.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
from pathlib import Path
import signal
import time
import traceback
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q017"
RUN = "Q017-PLANCK-DIRECTION-LOCALIZATION-V1"
RESULT = "R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-001"
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
PLANCK_BRANCH = "planck_npipe_k039_approx"


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return str(x)


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def close(a: Any, b: Any, tol: float) -> bool:
    return finite(a) and finite(b) and math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=float(tol))


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(c, dict):
        raise RuntimeError("CONFIG_GATE=FAIL non-mapping config")
    pr = c["project"]
    if pr["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if pr["run_id"] != RUN or pr["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    fs = c["frozen_surface"]
    if fs["model"] != "ede_n3" or int(fs["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if fs["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if fs["full_planck_likelihood"] != FULL_LIKE:
        raise RuntimeError("FULL_MF_LIKELIHOOD_GATE=FAIL")
    return c


def load_lock(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / c["parent_q016"]["endpoint_lock"]
    d = json.loads(p.read_text(encoding="utf-8"))
    parent = d.get("parent", {})
    expected = c["parent_q016"]
    gates = {
        "lock_q": d.get("q") == "Q016",
        "parent_run": parent.get("run_id") == expected["run_id"],
        "parent_result": parent.get("result_id") == expected["result_id"],
        "github_run": int(parent.get("github_run_id", -1)) == int(expected["github_run_id"]),
        "head_sha": parent.get("head_sha") == expected["head_sha"],
        "primary_gate": parent.get("primary_endpoint_gate") == "PASS",
        "usable": parent.get("scientifically_usable_primary_endpoint_result") is True,
        "surface_model": d.get("surface", {}).get("model") == "ede_n3",
        "surface_backend": d.get("surface", {}).get("backend_commit") == c["frozen_surface"]["backend_commit"],
    }
    if not all(gates.values()):
        raise RuntimeError("Q016_ENDPOINT_LOCK_GATE=FAIL " + json.dumps(gates, sort_keys=True))
    return d


def endpoint_record(lock: Mapping[str, Any], endpoint_name: str) -> Mapping[str, Any]:
    key = {
        "free": "reference_free_h0",
        "fixed": "fixed_h0_71p5",
    }[endpoint_name]
    return lock["endpoints"]["planck"][key]


def endpoint_values(lock: Mapping[str, Any], endpoint_name: str, c: Mapping[str, Any]) -> dict[str, float]:
    rec = endpoint_record(lock, endpoint_name)
    row = rec["minimum"]
    required = [
        "omega_b", "omega_cdm", "tau_reio", "n_s", "logA",
        "fEDE", "log10z_c", "thetai_scf"
    ]
    out: dict[str, float] = {}
    for name in required:
        if name not in row or not finite(row[name]):
            raise RuntimeError(f"Q016_ENDPOINT_PARAMETER_GATE=FAIL {endpoint_name} missing {name}")
        out[name] = float(row[name])
    if endpoint_name == "free":
        out["H0"] = float(row["H0"])
    else:
        out["H0"] = float(c["frozen_surface"]["target_h0"])
    tol = float(c["validation"]["endpoint_h0_abs_tol"])
    expected_h0 = float(c["parent_q016"]["expected_h0"][endpoint_name])
    if not close(out["H0"], expected_h0, tol):
        raise RuntimeError(f"Q016_ENDPOINT_H0_GATE=FAIL {endpoint_name}: {out['H0']} != {expected_h0}")
    return out


def _is_sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and "prior" in spec


def _ref_value(spec: Any) -> float | None:
    if not isinstance(spec, Mapping):
        return None
    ref = spec.get("ref")
    if isinstance(ref, Mapping) and finite(ref.get("loc")):
        return float(ref["loc"])
    if finite(ref):
        return float(ref)
    prior = spec.get("prior")
    if isinstance(prior, Mapping):
        if finite(prior.get("loc")):
            return float(prior["loc"])
        if finite(prior.get("min")) and finite(prior.get("max")):
            return 0.5 * (float(prior["min"]) + float(prior["max"]))
    return None


def _clip_to_prior(value: float, spec: Any) -> float:
    x = float(value)
    if not isinstance(spec, Mapping):
        return x
    prior = spec.get("prior")
    if not isinstance(prior, Mapping):
        return x
    if finite(prior.get("min")) and finite(prior.get("max")):
        lo, hi = float(prior["min"]), float(prior["max"])
        eps = max((hi - lo) * 1e-7, 1e-10)
        return min(max(x, lo + eps), hi - eps)
    return x


def _set_reference(spec: dict[str, Any], value: float) -> None:
    if not _is_sampled(spec):
        return
    proposal = spec.get("proposal")
    if not finite(proposal):
        prior = spec.get("prior", {})
        if isinstance(prior, Mapping) and finite(prior.get("scale")):
            proposal = float(prior["scale"])
        elif isinstance(prior, Mapping) and finite(prior.get("min")) and finite(prior.get("max")):
            proposal = max((float(prior["max"]) - float(prior["min"])) / 20.0, 1e-6)
        else:
            proposal = max(abs(float(value)) * 0.01, 1e-6)
    spec["ref"] = {"dist": "norm", "loc": float(value), "scale": float(proposal)}


def base_nuisance_start(info: Mapping[str, Any], lock: Mapping[str, Any],
                        endpoint_name: str, c: Mapping[str, Any]) -> dict[str, float]:
    params = info["params"]
    out: dict[str, float] = {}
    for name in c["nuisance"]["all"]:
        if name not in params:
            raise RuntimeError(f"FULL_MF_NUISANCE_GATE=FAIL missing {name}")
        v = _ref_value(params[name])
        if v is None:
            raise RuntimeError(f"NUISANCE_REFERENCE_GATE=FAIL {name}")
        out[name] = float(v)

    # Q016 certifies these calibration-like nuisance values on its matched surface.
    q16row = endpoint_record(lock, endpoint_name)["minimum"]
    for name in ("A_planck", "calTE", "calEE"):
        if name in q16row and finite(q16row[name]):
            out[name] = float(q16row[name])
    return out


def jitter_start(values: Mapping[str, float], params: Mapping[str, Any],
                 restart: int, c: Mapping[str, Any], locked: set[str]) -> dict[str, float]:
    out = {str(k): float(v) for k, v in values.items()}
    signs = c["execution"]["restart_signs"]
    if restart < 0 or restart >= len(signs):
        raise RuntimeError(f"RESTART_GATE=FAIL unsupported restart={restart}")
    s = float(signs[restart])
    if s == 0:
        return out
    for name, dv in c["execution"]["nuisance_jitter"].items():
        if name in locked or name not in out or name not in params:
            continue
        out[name] = _clip_to_prior(out[name] + s * float(dv), params[name])
    return out


def import_q14():
    import q014_external_viability_v12 as q14
    return q14


def build_full_mf_info(c: Mapping[str, Any], lock: Mapping[str, Any],
                       endpoint_name: str, restart: int, output_prefix: Path,
                       locked_values: Mapping[str, float] | None = None,
                       fixed_all_nuisance: Mapping[str, float] | None = None) -> tuple[dict[str, Any], dict[str, float], dict[str, float], list[str]]:
    """
    Reuse Q014's proven public NPIPE CamSpec construction, but freeze every
    cosmological sampled parameter to the certified Q016 endpoint.

    Q011 is not loaded or used. The Q014 builder receives an empty q011 vector
    with start_family='external', where that vector is not consulted.
    """
    q14 = import_q14()
    q14cfg = q14.load_cfg("q014_external_viability_v12_config.yml")
    info, _ = q14.impl.build_info(
        PLANCK_BRANCH,
        "reference_free_h0",
        "external",
        int(restart),
        q14cfg,
        {},  # intentionally no Q011 endpoint/vector
        output_prefix,
        max_evals=int(c["execution"]["max_evals"]),
    )
    info = copy.deepcopy(info)
    if FULL_LIKE not in info.get("likelihood", {}):
        raise RuntimeError("FULL_MF_LIKELIHOOD_GATE=FAIL component absent after Q014 reuse")
    info["likelihood"] = {FULL_LIKE: copy.deepcopy(info["likelihood"][FULL_LIKE])}

    params = info.get("params")
    if not isinstance(params, dict):
        raise RuntimeError("MODEL_PARAMETER_GATE=FAIL")
    nuisance_names = set(map(str, c["nuisance"]["all"]))
    cosmology = endpoint_values(lock, endpoint_name, c)

    # Freeze all sampled non-nuisance parameters. This is the Q017 no-globality-reopen gate.
    unknown_sampled: list[str] = []
    for name, spec in list(params.items()):
        if not _is_sampled(spec):
            continue
        if name in nuisance_names:
            continue
        if name not in cosmology:
            unknown_sampled.append(str(name))
        else:
            params[name] = float(cosmology[name])
    if unknown_sampled:
        raise RuntimeError("COSMOLOGY_FREEZE_COMPLETENESS_GATE=FAIL " + repr(sorted(unknown_sampled)))

    starts = base_nuisance_start(info, lock, endpoint_name, c)
    locked_values = {str(k): float(v) for k, v in (locked_values or {}).items()}
    fixed_all_nuisance = {str(k): float(v) for k, v in (fixed_all_nuisance or {}).items()}

    for name in nuisance_names:
        if name not in params:
            raise RuntimeError(f"FULL_MF_NUISANCE_GATE=FAIL missing declared {name}")

    if fixed_all_nuisance:
        missing = nuisance_names.difference(fixed_all_nuisance)
        if missing:
            raise RuntimeError("FIXED_NUISANCE_COMPLETENESS_GATE=FAIL " + repr(sorted(missing)))
        for name in nuisance_names:
            params[name] = float(fixed_all_nuisance[name])
        sampled_expected: list[str] = []
        starts.update(fixed_all_nuisance)
    else:
        locked_set = set(locked_values)
        starts = jitter_start(starts, params, int(restart), c, locked_set)
        for name, value in locked_values.items():
            if name not in nuisance_names:
                raise RuntimeError(f"LOCK_GROUP_PARAMETER_GATE=FAIL {name}")
            params[name] = float(value)
            starts[name] = float(value)
        sampled_expected = sorted(nuisance_names.difference(locked_set))
        for name in sampled_expected:
            spec = params[name]
            if not _is_sampled(spec):
                raise RuntimeError(f"NUISANCE_SAMPLED_GATE=FAIL {name}")
            _set_reference(spec, starts[name])

    # Preserve Q014/Cobaya objective semantics: likelihood + native priors.
    if fixed_all_nuisance:
        info.pop("sampler", None)
        info.pop("output", None)
        info.pop("resume", None)
        info.pop("force", None)
        # With every sampled parameter scalar, external prior blocks are unnecessary
        # for direct residual evaluation. Q017 reports normalization-free shapes itself.
        info.pop("prior", None)
    else:
        m = info.setdefault("sampler", {}).setdefault("minimize", {})
        m["method"] = "bobyqa"
        m["ignore_prior"] = False
        m["max_evals"] = int(c["execution"]["max_evals"])
        m["best_of"] = 1
        m["seed"] = int(c["execution"]["seed_base"]) + int(restart)
        m.setdefault("override_bobyqa", {})["rhoend"] = float(c["execution"]["rhoend"])
        info["output"] = str(output_prefix.resolve())
        info["force"] = True

    return info, cosmology, starts, sampled_expected


def minimum_row(sampler: Any, prefix: Path) -> tuple[dict[str, Any], str | None]:
    q14 = import_q14()
    row: dict[str, Any] = {}
    try:
        minimum = sampler.products()["minimum"]
        row = q14.impl.minimum_to_row(minimum)
    except Exception:
        row = {}
    source = None
    if not row:
        row, source = q14.impl.harvest_output_prefix(prefix)
    return row, source


def comparable_objective(row: Mapping[str, Any]) -> tuple[float, dict[str, float], str, dict[str, float]]:
    q14 = import_q14()
    obj, comps, basis, shapes = q14.comparable_objective(row)
    if obj is None or not finite(obj):
        raise RuntimeError("COMPARABLE_OBJECTIVE_GATE=FAIL")
    return float(obj), {str(k): float(v) for k, v in comps.items()}, str(basis), {str(k): float(v) for k, v in shapes.items()}


def _alarm_handler(signum, frame):
    raise KeyboardInterrupt("Q017_SOFT_RUNTIME_LIMIT")


def profile_command(c: Mapping[str, Any], lock: Mapping[str, Any], endpoint_name: str,
                    restart: int, output: str | Path, baseline_path: str | None,
                    lock_group: str | None) -> int:
    started = time.time()
    outp = Path(output)
    prefix = outp.parent / (outp.stem + "_cobaya")
    lock_values: dict[str, float] = {}

    if lock_group:
        if not baseline_path:
            raise RuntimeError("LOCK_PROFILE_BASELINE_GATE=FAIL baseline required")
        b = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
        if b.get("q") != Q or b.get("stage") != "BASELINE_SELECTION" or b.get("status") != "PASS":
            raise RuntimeError("LOCK_PROFILE_BASELINE_GATE=FAIL identity/status")
        groups = c["nuisance"]["groups"]
        if lock_group not in groups:
            raise RuntimeError(f"LOCK_GROUP_GATE=FAIL {lock_group}")
        free_nuis = b["selected"]["free"]["nuisance_bestfit"]
        lock_values = {name: float(free_nuis[name]) for name in groups[lock_group]}

    rec: dict[str, Any] = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "NUISANCE_PROFILE",
        "endpoint": endpoint_name,
        "restart": int(restart),
        "lock_group": lock_group,
        "status": "FAILED",
        "scientific_model_failure": False,
        "q016_globality_reopened": False,
        "q011_endpoint_used": False,
        "cross_chain_chi2_sum_performed": False,
        "full_mf_likelihood": FULL_LIKE,
        "runtime_seconds": None,
    }

    old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info, cosmology, starts, sampled_expected = build_full_mf_info(
            c, lock, endpoint_name, restart, prefix, locked_values=lock_values
        )
        rec["frozen_cosmology"] = cosmology
        rec["nuisance_start"] = starts
        rec["nuisance_locked"] = lock_values
        rec["sampled_nuisance_expected"] = sampled_expected

        from cobaya.run import run as cobaya_run
        sampler = None
        row: dict[str, Any] = {}
        harvested = None
        try:
            _updated, sampler = cobaya_run(info, force=True)
            row, harvested = minimum_row(sampler, prefix)
            optimizer_exit = "COBAYA_COMPLETED"
            status = "COMPLETE"
        except KeyboardInterrupt:
            q14 = import_q14()
            row, harvested = q14.impl.harvest_output_prefix(prefix)
            optimizer_exit = "SOFT_RUNTIME_INTERRUPT"
            status = "PARTIAL_SOFT_STOP" if row else "FAILED_SOFT_STOP_NO_MINIMUM"

        if not row:
            raise RuntimeError("MINIMUM_GATE=FAIL no finite minimum record")
        obj, comps, basis, shapes = comparable_objective(row)
        nuisance_best: dict[str, float] = {}
        for name in c["nuisance"]["all"]:
            if name in row and finite(row[name]):
                nuisance_best[name] = float(row[name])
            elif name in lock_values:
                nuisance_best[name] = float(lock_values[name])
            else:
                # A sampled nuisance must be serialized in a usable minimum.
                raise RuntimeError(f"NUISANCE_MINIMUM_SERIALIZATION_GATE=FAIL {name}")

        rec.update({
            "status": status,
            "optimizer_exit": optimizer_exit,
            "harvested_minimum_path": harvested,
            "objective_chi2": obj,
            "objective_basis": basis,
            "chi2_components": comps,
            "normalization_free_gaussian_shape_penalties": shapes,
            "minimum": row,
            "nuisance_bestfit": nuisance_best,
            "full_mf_primary_chi2": float(comps.get("chi2__" + FULL_LIKE, row.get("chi2", float("nan")))),
            "actual_computed_result": True,
        })
    except Exception as exc:
        rec.update({
            "status": "TECHNICALLY_UNAVAILABLE" if any(
                token in repr(exc).lower()
                for token in ("likelihood", "camspec", "component", "data", "import", "module", "package")
            ) else "FAILED",
            "failure_class": "FULL_MF_TECHNICAL_EXECUTION",
            "error": repr(exc),
            "traceback": traceback.format_exc()[-12000:],
            "scientific_interpretation": "NONE",
        })
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        rec["runtime_seconds"] = time.time() - started
        write_json(outp, rec)

    return 0 if rec["status"] == "COMPLETE" else 2


def plan_command(c: Mapping[str, Any], output: str | Path) -> dict[str, Any]:
    baseline = [
        {"endpoint": endpoint, "restart": int(r)}
        for endpoint in ("free", "fixed")
        for r in c["execution"]["baseline_restarts"]
    ]
    locks = [
        {"lock_group": group, "restart": int(r)}
        for group in c["nuisance"]["groups"]
        for r in c["execution"]["lock_restarts"]
    ]
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "JOB_PLAN",
        "status": "PASS",
        "baseline_matrix": {"include": baseline},
        "lock_matrix": {"include": locks},
        "expected_baseline_jobs": len(baseline),
        "expected_lock_jobs": len(locks),
        "execution_strategy": "PARALLEL_ATOMIC_NUISANCE_PROFILES_THEN_DETERMINISTIC_MERGE",
        "checkpointing": False,
        "checkpoint_reason": "Frozen Cobaya/Py-BOBYQA optimizer state is not reliably serializable; each nuisance-only start is an independent atomic task.",
    }
    write_json(output, out)
    return out


def iter_profile_records(input_dir: str | Path) -> list[dict[str, Any]]:
    rows = []
    for p in sorted(Path(input_dir).rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == "NUISANCE_PROFILE":
            d["_source_file"] = str(p)
            rows.append(d)
    return rows


def _select_best(records: list[dict[str, Any]], expected_restarts: list[int],
                 spread_max: float) -> dict[str, Any]:
    by_restart: dict[int, dict[str, Any]] = {}
    duplicates = []
    for r in records:
        rr = int(r.get("restart", -1))
        if rr in by_restart:
            duplicates.append(rr)
        else:
            by_restart[rr] = r
    missing = sorted(set(map(int, expected_restarts)).difference(by_restart))
    expected_rows = [by_restart[r] for r in expected_restarts if r in by_restart]
    complete = [r for r in expected_rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
    unavailable = [r for r in expected_rows if r.get("status") == "TECHNICALLY_UNAVAILABLE"]

    if duplicates or missing:
        status = "NUMERICALLY_UNRESOLVED"
    elif len(unavailable) == len(expected_restarts):
        status = "TECHNICALLY_UNAVAILABLE"
    elif len(complete) < 2:
        status = "NUMERICALLY_UNRESOLVED"
    else:
        ordered = sorted(complete, key=lambda x: float(x["objective_chi2"]))
        spread = float(ordered[1]["objective_chi2"]) - float(ordered[0]["objective_chi2"])
        stable = spread <= float(spread_max)
        return {
            "status": "PASS" if stable else "NUMERICALLY_UNRESOLVED",
            "best": ordered[0],
            "complete_count": len(complete),
            "best_two_spread": spread,
            "stable": stable,
            "missing_restarts": missing,
            "duplicate_restarts": duplicates,
            "statuses": {str(r): by_restart[r].get("status") for r in expected_restarts if r in by_restart},
        }

    return {
        "status": status,
        "best": min(complete, key=lambda x: float(x["objective_chi2"])) if complete else None,
        "complete_count": len(complete),
        "best_two_spread": None,
        "stable": False,
        "missing_restarts": missing,
        "duplicate_restarts": duplicates,
        "statuses": {str(r): by_restart[r].get("status") for r in expected_restarts if r in by_restart},
    }


def select_command(c: Mapping[str, Any], input_dir: str | Path, stage: str,
                   output: str | Path) -> dict[str, Any]:
    rows = iter_profile_records(input_dir)
    spread_max = float(c["validation"]["profile_multistart_spread_max"])
    if stage == "baseline":
        selected = {}
        statuses = []
        for endpoint in ("free", "fixed"):
            r = [x for x in rows if x.get("endpoint") == endpoint and x.get("lock_group") is None]
            s = _select_best(r, list(map(int, c["execution"]["baseline_restarts"])), spread_max)
            selected[endpoint] = s
            statuses.append(s["status"])
        if all(x == "PASS" for x in statuses):
            overall = "PASS"
        elif all(x == "TECHNICALLY_UNAVAILABLE" for x in statuses):
            overall = "TECHNICALLY_UNAVAILABLE"
        else:
            overall = "NUMERICALLY_UNRESOLVED"
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "BASELINE_SELECTION", "status": overall,
            "job_completeness_gate": overall in {"PASS", "TECHNICALLY_UNAVAILABLE"},
            "selected": {
                k: (v["best"] if v["best"] is not None else None)
                for k, v in selected.items()
            },
            "selection_detail": selected,
        }
    elif stage == "locks":
        selected = {}
        statuses = []
        for group in c["nuisance"]["groups"]:
            r = [x for x in rows if x.get("endpoint") == "fixed" and x.get("lock_group") == group]
            s = _select_best(r, list(map(int, c["execution"]["lock_restarts"])), spread_max)
            selected[group] = s
            statuses.append(s["status"])
        if all(x == "PASS" for x in statuses):
            overall = "PASS"
        elif all(x == "TECHNICALLY_UNAVAILABLE" for x in statuses):
            overall = "TECHNICALLY_UNAVAILABLE"
        else:
            overall = "NUMERICALLY_UNRESOLVED"
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "LOCK_SELECTION", "status": overall,
            "job_completeness_gate": overall in {"PASS", "TECHNICALLY_UNAVAILABLE"},
            "selected": {
                k: (v["best"] if v["best"] is not None else None)
                for k, v in selected.items()
            },
            "selection_detail": selected,
        }
    else:
        raise RuntimeError("SELECTION_STAGE_GATE=FAIL")
    write_json(output, out)
    return out


def band_name(ell: float, c: Mapping[str, Any]) -> str:
    for b in c["decomposition"]["ell_bands"]:
        if float(b["min"]) <= float(ell) <= float(b["max"]):
            return str(b["name"])
    return "outside_registered_bands"


def detailed_planck_state(model: Any, values: Mapping[str, float], c: Mapping[str, Any]) -> dict[str, Any]:
    like = model.likelihood[FULL_LIKE]
    cls = like.provider.get_Cl(ell_factor=True)
    CT = np.asarray(cls["tt"], dtype=float)
    CTE = np.asarray(cls["te"], dtype=float)
    CEE = np.asarray(cls["ee"], dtype=float)
    pars = dict(values)
    cals = np.asarray(like.get_cals(pars), dtype=float)
    foregrounds = like.get_foregrounds(pars) if np.any(like.cl_used[:4]) else None
    residual = np.asarray(like.data_vector, dtype=float).copy()

    labels: list[dict[str, Any]] = []
    ix = 0
    for i, (cal, n) in enumerate(zip(cals, like.used_sizes)):
        n = int(n)
        if n <= 0:
            continue
        ells = np.asarray(list(like.ell_ranges[i]), dtype=int)[:n]
        if i <= 3:
            model_vec = (CT[ells] + np.asarray(foregrounds[i], dtype=float)[ells]) / float(cal)
            obs = "TT"
        elif i == 4:
            model_vec = CTE[ells] / float(cal)
            obs = "TE"
        elif i == 5:
            model_vec = CEE[ells] / float(cal)
            obs = "EE"
        else:
            raise RuntimeError("PLANCK_SPECTRUM_LAYOUT_GATE=FAIL")
        residual[ix:ix+n] -= model_vec
        spec = str(like.cl_names[i])
        labels.extend({
            "observable": obs,
            "spectrum": spec,
            "ell": int(L),
            "band": band_name(float(L), c),
        } for L in ells)
        ix += n

    if ix != len(residual) or len(labels) != len(residual):
        raise RuntimeError("PLANCK_VECTOR_LENGTH_GATE=FAIL")

    precision = np.asarray(like.covinv, dtype=float)
    if precision.shape != (len(residual), len(residual)):
        raise RuntimeError("PLANCK_PRECISION_SHAPE_GATE=FAIL")
    z = precision @ residual
    contrib = residual * z
    chi2 = float(residual @ z)

    by_observable: dict[str, float] = {}
    by_spectrum: dict[str, float] = {}
    by_band: dict[str, float] = {}
    by_spec_band: dict[str, float] = {}
    by_obs_spec_band: dict[str, float] = {}
    group_indices: dict[str, list[int]] = {}
    rows = []

    for i, (meta, r, cc) in enumerate(zip(labels, residual, contrib)):
        obs, spec, band = meta["observable"], meta["spectrum"], meta["band"]
        ksb = f"{spec}|{band}"
        kosb = f"{obs}|{spec}|{band}"
        by_observable[obs] = by_observable.get(obs, 0.0) + float(cc)
        by_spectrum[spec] = by_spectrum.get(spec, 0.0) + float(cc)
        by_band[band] = by_band.get(band, 0.0) + float(cc)
        by_spec_band[ksb] = by_spec_band.get(ksb, 0.0) + float(cc)
        by_obs_spec_band[kosb] = by_obs_spec_band.get(kosb, 0.0) + float(cc)
        group_indices.setdefault(kosb, []).append(i)
        rows.append({
            "index": i, **meta,
            "residual": float(r),
            "precision_weighted_residual": float(z[i]),
            "signed_fullcov_contribution": float(cc),
        })

    # Exact symmetric block-pair decomposition:
    # diagonal g,g = r_g^T P_gg r_g
    # off-diagonal g,h = 2 r_g^T P_gh r_h
    groups = sorted(group_indices)
    pair_terms: dict[str, float] = {}
    for gi, g in enumerate(groups):
        I = np.asarray(group_indices[g], dtype=int)
        rg = residual[I]
        qgg = float(rg @ (precision[np.ix_(I, I)] @ rg))
        pair_terms[f"{g} <-> {g}"] = qgg
        for h in groups[gi+1:]:
            J = np.asarray(group_indices[h], dtype=int)
            rh = residual[J]
            qgh = 2.0 * float(rg @ (precision[np.ix_(I, J)] @ rh))
            pair_terms[f"{g} <-> {h}"] = qgh

    pair_sum = float(sum(pair_terms.values()))
    return {
        "chi2": chi2,
        "signed_contribution_sum": float(np.sum(contrib)),
        "covariance_block_pair_sum": pair_sum,
        "n_data": len(residual),
        "groups": {
            "by_observable": dict(sorted(by_observable.items())),
            "by_spectrum": dict(sorted(by_spectrum.items())),
            "by_band": dict(sorted(by_band.items())),
            "by_spectrum_band": dict(sorted(by_spec_band.items())),
            "by_observable_spectrum_band": dict(sorted(by_obs_spec_band.items())),
        },
        "covariance_block_pair_terms": dict(sorted(pair_terms.items())),
        "rows": rows,
    }


def expanded_values(model: Any, cosmology: Mapping[str, float],
                    nuisance: Mapping[str, float]) -> dict[str, float]:
    out: dict[str, float] = {}
    for k, v in model.parameterization.constant_params().items():
        if finite(v):
            out[str(k)] = float(v)
    out.update({str(k): float(v) for k, v in cosmology.items()})
    out.update({str(k): float(v) for k, v in nuisance.items()})
    return out


def eval_selected_endpoint(c: Mapping[str, Any], lock: Mapping[str, Any],
                           endpoint_name: str, nuisance: Mapping[str, float],
                           work: Path) -> dict[str, Any]:
    info, cosmology, _, sampled_expected = build_full_mf_info(
        c, lock, endpoint_name, 0, work, fixed_all_nuisance=nuisance
    )
    if sampled_expected:
        raise RuntimeError("DIRECT_EVAL_SAMPLED_NUISANCE_GATE=FAIL")
    from cobaya.model import get_model
    model = get_model(info)
    try:
        lp = model.logposterior({})
        if not finite(getattr(lp, "logpost", lp)):
            raise RuntimeError("DIRECT_ENDPOINT_FINITE_GATE=FAIL")
        values = expanded_values(model, cosmology, nuisance)

        # Q015 is the frozen reference evaluator for the same full CamSpec internals.
        import q015_cmb_attribution_v2 as q15
        q15cfg = yaml.safe_load((ROOT / "q015_cmb_attribution_v2_config.yml").read_text(encoding="utf-8"))
        q15cfg["ell_bands"] = copy.deepcopy(c["decomposition"]["ell_bands"])
        q15_state = q15.planck_highl_state(model, values, q15cfg)

        detailed = detailed_planck_state(model, values, c)
        tol = float(c["validation"]["covariance_closure_abs_tol"])
        gates = {
            "q015_reference_chi2_closure": close(q15_state["chi2"], detailed["chi2"], tol),
            "signed_allocation_closure": close(detailed["chi2"], detailed["signed_contribution_sum"], tol),
            "block_pair_closure": close(detailed["chi2"], detailed["covariance_block_pair_sum"], tol),
        }
        return {
            "endpoint": endpoint_name,
            "h0": cosmology["H0"],
            "nuisance_bestfit": {str(k): float(v) for k, v in nuisance.items()},
            "state": detailed,
            "q015_reference_chi2": float(q15_state["chi2"]),
            "gates": gates,
            "status": "PASS" if all(gates.values()) else "FAIL",
        }
    finally:
        try:
            model.close()
        except Exception:
            pass


def diff_mapping(fixed: Mapping[str, float], free: Mapping[str, float]) -> dict[str, float]:
    return {
        str(k): float(fixed.get(k, 0.0)) - float(free.get(k, 0.0))
        for k in sorted(set(free) | set(fixed))
    }


def decompose_command(c: Mapping[str, Any], lock: Mapping[str, Any],
                      baseline_path: str | Path, output: str | Path) -> dict[str, Any]:
    b = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    if b.get("q") != Q or b.get("stage") != "BASELINE_SELECTION":
        raise RuntimeError("DECOMPOSITION_BASELINE_IDENTITY_GATE=FAIL")
    if b.get("status") != "PASS":
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "DECOMPOSITION", "status": "NOT_RUN_BASELINE_UNRESOLVED",
            "scientific_interpretation": "NONE",
        }
        write_json(output, out)
        return out

    endpoints = {}
    for endpoint_name in ("free", "fixed"):
        nuisance = b["selected"][endpoint_name]["nuisance_bestfit"]
        endpoints[endpoint_name] = eval_selected_endpoint(
            c, lock, endpoint_name, nuisance,
            Path(output).parent / f"decomp_{endpoint_name}"
        )

    f = endpoints["free"]["state"]
    x = endpoints["fixed"]["state"]
    if len(f["rows"]) != len(x["rows"]):
        raise RuntimeError("DECOMPOSITION_VECTOR_ALIGNMENT_GATE=FAIL length")
    for a, bb in zip(f["rows"], x["rows"]):
        ka = (a["observable"], a["spectrum"], a["ell"], a["band"])
        kb = (bb["observable"], bb["spectrum"], bb["ell"], bb["band"])
        if ka != kb:
            raise RuntimeError("DECOMPOSITION_VECTOR_ALIGNMENT_GATE=FAIL labels")

    delta = {
        "raw_full_mf_highl_chi2": float(x["chi2"]) - float(f["chi2"]),
        "by_observable": diff_mapping(x["groups"]["by_observable"], f["groups"]["by_observable"]),
        "by_spectrum": diff_mapping(x["groups"]["by_spectrum"], f["groups"]["by_spectrum"]),
        "by_band": diff_mapping(x["groups"]["by_band"], f["groups"]["by_band"]),
        "by_spectrum_band": diff_mapping(x["groups"]["by_spectrum_band"], f["groups"]["by_spectrum_band"]),
        "by_observable_spectrum_band": diff_mapping(
            x["groups"]["by_observable_spectrum_band"],
            f["groups"]["by_observable_spectrum_band"]
        ),
        "covariance_block_pair_terms": diff_mapping(
            x["covariance_block_pair_terms"],
            f["covariance_block_pair_terms"]
        ),
    }
    gates = {
        "free_endpoint": endpoints["free"]["status"] == "PASS",
        "fixed_endpoint": endpoints["fixed"]["status"] == "PASS",
        "target_band_present": c["decomposition"]["target_band"]["name"] in delta["by_band"],
        "finite_delta": finite(delta["raw_full_mf_highl_chi2"]),
        "no_cross_chain_sum": True,
    }
    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "DECOMPOSITION",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "endpoints": endpoints,
        "fixed_minus_free": delta,
        "gates": gates,
        "attribution_definition": "signed full-covariance allocation c_i=r_i(C^-1 r)_i plus exact symmetric covariance block-pair partition",
        "independent_chi2_interpretation_allowed": False,
        "causal_systematic_identification": False,
        "cross_chain_chi2_sum_performed": False,
    }
    write_json(output, out)
    return out


def _abs_shares(values: Mapping[str, float]) -> tuple[list[dict[str, Any]], float]:
    rows = [(str(k), float(v)) for k, v in values.items() if finite(v)]
    denom = sum(abs(v) for _, v in rows)
    ranked = sorted(rows, key=lambda kv: abs(kv[1]), reverse=True)
    out = [{
        "direction": k,
        "value": v,
        "absolute_share": (abs(v) / denom if denom > 0 else 0.0),
    } for k, v in ranked]
    return out, denom


def _effective_number(ranked: list[dict[str, Any]]) -> float | None:
    ps = [float(x["absolute_share"]) for x in ranked if x["absolute_share"] > 0]
    if not ps:
        return None
    return 1.0 / sum(p * p for p in ps)


def _frequency_to_group(direction: str) -> str | None:
    s = direction.replace(" ", "").lower()
    if "143x217" in s or "217x143" in s:
        return "foreground_143x217"
    if "143x143" in s:
        return "foreground_143"
    if "217x217" in s:
        return "foreground_217"
    return None


def _load_optional(path: str | Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def aggregate_command(c: Mapping[str, Any], baseline_path: str | Path,
                      locks_path: str | Path | None, decomposition_path: str | Path | None,
                      output: str | Path) -> dict[str, Any]:
    b = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    locks = _load_optional(locks_path)
    decomp = _load_optional(decomposition_path)

    # Explicitly valid Q017 terminal state if full-MF execution is systematically unavailable.
    if b.get("status") == "TECHNICALLY_UNAVAILABLE":
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "FINAL",
            "execution_status": "TECHNICALLY_UNAVAILABLE",
            "tests_status": "COMPLETE_FOR_TECHNICAL_UNAVAILABILITY",
            "final_result_gate": "PASS",
            "classification": "INDETERMINATE",
            "classification_reason": "FULL_PLANCK_MULTIFREQUENCY_LIKELIHOOD_NOT_TECHNICALLY_CERTIFIED_IN_THIS_RUN",
            "scientifically_usable_result": True,
            "q016_result_invalidated": False,
            "fc_cmb_002_effect": "UNRESOLVED",
            "cross_chain_chi2_sum_performed": False,
            "causal_systematic_identification_claimed": False,
            "next_required_action": "RESULT INGESTION & ROUTING ENGINE",
        }
        write_json(output, out)
        return out

    if b.get("status") != "PASS":
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "FINAL",
            "execution_status": "NUMERICALLY_UNRESOLVED",
            "tests_status": "INCOMPLETE",
            "final_result_gate": "UNRESOLVED",
            "classification": "INDETERMINATE",
            "classification_reason": "BASELINE_NUISANCE_PROFILE_NOT_NUMERICALLY_CERTIFIED",
            "scientifically_usable_result": False,
            "q016_result_invalidated": False,
            "next_required_action": "NUMERICAL RECOVERY OF FAILED Q017 PROFILE JOBS ONLY",
        }
        write_json(output, out)
        return out

    if locks is None or decomp is None:
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "FINAL",
            "execution_status": "PARTIAL", "tests_status": "INCOMPLETE",
            "final_result_gate": "UNRESOLVED", "classification": "INDETERMINATE",
            "classification_reason": "REQUIRED_LOCK_OR_DECOMPOSITION_OUTPUT_MISSING",
            "scientifically_usable_result": False, "q016_result_invalidated": False,
            "next_required_action": "RERUN ONLY MISSING Q017 JOBS",
        }
        write_json(output, out)
        return out

    if locks.get("status") == "TECHNICALLY_UNAVAILABLE" or decomp.get("status") in {"TECHNICALLY_UNAVAILABLE", "NOT_RUN_BASELINE_UNRESOLVED"}:
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "FINAL",
            "execution_status": "TECHNICALLY_UNAVAILABLE", "tests_status": "COMPLETE_FOR_TECHNICAL_UNAVAILABILITY",
            "final_result_gate": "PASS", "classification": "INDETERMINATE",
            "classification_reason": "REQUIRED_FULL_MF_DIRECTION_STAGE_NOT_TECHNICALLY_CERTIFIED",
            "scientifically_usable_result": True, "q016_result_invalidated": False,
            "fc_cmb_002_effect": "UNRESOLVED",
            "cross_chain_chi2_sum_performed": False,
            "causal_systematic_identification_claimed": False,
            "next_required_action": "RESULT INGESTION & ROUTING ENGINE",
        }
        write_json(output, out)
        return out

    mandatory = {
        "baseline_pass": b.get("status") == "PASS",
        "locks_pass": locks.get("status") == "PASS",
        "decomposition_pass": decomp.get("status") == "PASS",
        "free_profile_stable": b["selection_detail"]["free"].get("stable") is True,
        "fixed_profile_stable": b["selection_detail"]["fixed"].get("stable") is True,
        "all_lock_profiles_stable": all(
            locks["selection_detail"][g].get("stable") is True
            for g in c["nuisance"]["groups"]
        ),
        "decomposition_endpoint_closure": all(
            all(decomp["endpoints"][ep]["gates"].values()) for ep in ("free", "fixed")
        ),
        "no_cross_chain_sum": decomp.get("cross_chain_chi2_sum_performed") is False,
    }

    free_best = b["selected"]["free"]
    fixed_best = b["selected"]["fixed"]
    profile_penalty = float(fixed_best["objective_chi2"]) - float(free_best["objective_chi2"])
    lock_costs = {
        g: float(locks["selected"][g]["objective_chi2"]) - float(fixed_best["objective_chi2"])
        for g in c["nuisance"]["groups"]
    }
    neg_tol = float(c["validation"]["negative_lock_cost_tolerance"])
    mandatory["nested_lock_nonnegative_gate"] = all(v >= -neg_tol for v in lock_costs.values())

    target = c["decomposition"]["target_band"]["name"]
    freq_target = {
        k: v for k, v in decomp["fixed_minus_free"]["by_observable_spectrum_band"].items()
        if k.startswith("TT|") and k.endswith("|" + target)
    }
    freq_ranked, freq_abs_total = _abs_shares(freq_target)
    freq_eff_n = _effective_number(freq_ranked)

    pair_target = {
        k: v for k, v in decomp["fixed_minus_free"]["covariance_block_pair_terms"].items()
        if ("|" + target + " <->" in k) or ("<-> TT|" in k and k.endswith("|" + target))
        or ("|" + target + " <-> " in k) or k.endswith("|" + target)
    }
    # More robust target-pair filter: either side of "<->" ends in the target band.
    pair_target = {}
    for k, v in decomp["fixed_minus_free"]["covariance_block_pair_terms"].items():
        sides = [x.strip() for x in k.split("<->")]
        if any(side.endswith("|" + target) for side in sides):
            pair_target[k] = v
    pair_ranked, pair_abs_total = _abs_shares(pair_target)

    # Classification must use mutually non-overlapping atomic nuisance groups.
    # foreground_all is retained as a robustness/summary lock test, but it overlaps
    # the three foreground frequency groups and therefore must not be normalized
    # as if it were a fifth independent direction.
    atomic_lock_names = list(c["classification_thresholds"]["atomic_nuisance_groups"])
    positive_lock = {
        k: max(0.0, float(lock_costs[k]))
        for k in atomic_lock_names
    }
    lock_ranked, lock_abs_total = _abs_shares(positive_lock)

    top_freq = freq_ranked[0] if freq_ranked else {"direction": None, "absolute_share": 0.0, "value": 0.0}
    top_pair = pair_ranked[0] if pair_ranked else {"direction": None, "absolute_share": 0.0, "value": 0.0}
    top_lock = lock_ranked[0] if lock_ranked else {"direction": None, "absolute_share": 0.0, "value": 0.0}
    mapped_group = _frequency_to_group(str(top_freq["direction"]))

    th = c["classification_thresholds"]
    freq_local = float(top_freq["absolute_share"]) >= float(th["specific_frequency_abs_share_min"])
    cov_local = float(top_pair["absolute_share"]) >= float(th["specific_covariance_pair_abs_share_min"])
    matched_nuisance_support = (
        mapped_group is not None
        and top_lock["direction"] == mapped_group
        and float(top_lock["absolute_share"]) >= float(th["specific_nuisance_lock_share_min"])
        and float(top_lock["value"]) >= float(th["specific_nuisance_lock_cost_min"])
    )
    calibration_support = (
        top_lock["direction"] == "calibration"
        and float(top_lock["absolute_share"]) >= float(th["specific_nuisance_lock_share_min"])
        and float(top_lock["value"]) >= float(th["specific_nuisance_lock_cost_min"])
        and cov_local
    )

    localized = mandatory["nested_lock_nonnegative_gate"] and (
        (freq_local and (cov_local or matched_nuisance_support))
        or calibration_support
    )
    broad = (
        float(top_freq["absolute_share"]) <= float(th["broad_frequency_abs_share_max"])
        and float(top_pair["absolute_share"]) <= float(th["broad_covariance_pair_abs_share_max"])
        and float(top_lock["absolute_share"]) <= float(th["broad_nuisance_lock_share_max"])
        and freq_eff_n is not None
        and float(freq_eff_n) >= float(th["broad_frequency_effective_number_min"])
    )

    if localized:
        classification = "SPECIFIC PLANCK DIRECTION LOCALIZED"
        fc_effect = "STRONGLY STRENGTHEN"
    elif broad:
        classification = "BROADLY DISTRIBUTED PLANCK PENALTY"
        fc_effect = "WEAKEN"
    else:
        classification = "INDETERMINATE"
        fc_effect = "UNRESOLVED"

    all_mandatory = all(bool(v) for v in mandatory.values())
    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "FINAL",
        "execution_status": "COMPLETE" if all_mandatory else "NUMERICALLY_UNRESOLVED",
        "tests_status": "COMPLETE",
        "final_result_gate": "PASS" if all_mandatory else "UNRESOLVED",
        "scientifically_usable_result": bool(all_mandatory),
        "classification": classification if all_mandatory else "INDETERMINATE",
        "classification_rule_status": "APPLIED" if all_mandatory else "NOT_APPLIED_DUE_MANDATORY_GATE",
        "full_mf_profile_objective_fixed_minus_free": profile_penalty,
        "full_mf_raw_highl_chi2_fixed_minus_free": decomp["fixed_minus_free"]["raw_full_mf_highl_chi2"],
        "q016_matched_primary_penalty_is_not_replaced": True,
        "q016_result_invalidated": False,
        "lock_group_costs": lock_costs,
        "target_band": target,
        "frequency_target_band_ranking": freq_ranked,
        "frequency_target_band_effective_number": freq_eff_n,
        "covariance_target_band_pair_ranking": pair_ranked,
        "nuisance_lock_ranking_atomic_nonoverlapping": lock_ranked,
        "foreground_all_lock_cost_robustness_only": lock_costs.get("foreground_all"),
        "dominant_frequency_to_nuisance_group_mapping": mapped_group,
        "mandatory_gates": mandatory,
        "fc_cmb_002_effect": fc_effect if all_mandatory else "UNRESOLVED",
        "guards": {
            "frequency_allocations_are_independent_chi2": False,
            "covariance_pair_terms_are_independent_chi2": False,
            "lock_costs_are_additive_chi2_components": False,
            "causal_systematic_identification_claimed": False,
            "cross_chain_chi2_sum_performed": False,
            "combined_interexperiment_significance_performed": False,
            "q011_vector_used_as_endpoint": False,
            "q016_cosmological_globality_reopened": False,
        },
        "journal_effect": {
            "C-EDE-002": "PRECISION_UPDATE_FROM_Q017_ONLY_IF_FINAL_RESULT_GATE_PASS",
            "FC-CMB-002": fc_effect if all_mandatory else "UNRESOLVED",
            "Q016-A": "PRESERVE",
            "COMMON-CMB-RESIDUAL-Q016": "PRESERVE_REJECTED",
            "PLANCK-OPTIMIZER-ARTIFACT": "PRESERVE_REJECTED_AS_MAIN_EXPLANATION",
        },
        "next_required_action": "RESULT INGESTION & ROUTING ENGINE" if all_mandatory else "NUMERICAL RECOVERY OF FAILED Q017 JOBS ONLY",
    }
    write_json(output, out)
    return out


def unavailable_placeholder(endpoint: str, restart: int, lock_group: str | None,
                            error: str, output: str | Path) -> None:
    write_json(output, {
        "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "NUISANCE_PROFILE",
        "endpoint": endpoint, "restart": int(restart), "lock_group": lock_group,
        "status": "TECHNICALLY_UNAVAILABLE",
        "failure_class": "FULL_MF_SETUP_OR_CAPABILITY",
        "error": str(error),
        "scientific_model_failure": False,
        "scientific_interpretation": "NONE",
        "q016_result_invalidated": False,
        "q016_globality_reopened": False,
        "q011_endpoint_used": False,
        "cross_chain_chi2_sum_performed": False,
    })


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--output", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--endpoint", choices=["free", "fixed"], required=True)
    p.add_argument("--restart", type=int, required=True)
    p.add_argument("--lock-group")
    p.add_argument("--baseline")
    p.add_argument("--output", required=True)

    p = sub.add_parser("select")
    p.add_argument("--stage", choices=["baseline", "locks"], required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("decompose")
    p.add_argument("--baseline", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate")
    p.add_argument("--baseline", required=True)
    p.add_argument("--locks")
    p.add_argument("--decomposition")
    p.add_argument("--output", required=True)

    p = sub.add_parser("unavailable")
    p.add_argument("--endpoint", choices=["free", "fixed"], required=True)
    p.add_argument("--restart", type=int, required=True)
    p.add_argument("--lock-group")
    p.add_argument("--error", required=True)
    p.add_argument("--output", required=True)

    args = ap.parse_args()
    c = load_cfg(args.config)

    if args.cmd == "plan":
        plan_command(c, args.output)
        return 0
    if args.cmd == "select":
        select_command(c, args.input_dir, args.stage, args.output)
        return 0
    if args.cmd == "aggregate":
        aggregate_command(c, args.baseline, args.locks, args.decomposition, args.output)
        return 0
    if args.cmd == "unavailable":
        unavailable_placeholder(args.endpoint, args.restart, args.lock_group, args.error, args.output)
        return 0

    lock = load_lock(c)
    if args.cmd == "profile":
        return profile_command(c, lock, args.endpoint, args.restart, args.output, args.baseline, args.lock_group)
    if args.cmd == "decompose":
        decompose_command(c, lock, args.baseline, args.output)
        return 0
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
