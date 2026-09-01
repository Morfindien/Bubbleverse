#!/usr/bin/env python3
"""
Bubbleverse Q012 V1 — ACT + non-ACT likelihood attribution at the Q011
best-observed H0=71.5 n=3 EDE point.

Scientific scope
----------------
Q012 does NOT optimize, sample, change priors, change bounds, change datasets,
or reopen Q011. It evaluates two fixed serialized vectors on the frozen Q005
V14 likelihood surface:

  1) the Q007-preserved Q005 attribution baseline;
  2) the Q011 V4 best-observed H0=71.5 point.

The same model evaluation is used to obtain:
- the Q005 non-overlapping likelihood components (Planck low-l, ACT DR6,
  DESI DR2, BBN), using Q010 V3's accounting semantics;
- the covariance-aware ACT TT/TE/EE and ell-band attribution, using Q009 V8's
  established implementation.

Optimizer-native parent chi2 values and serialized-vector re-evaluations are
kept separate. Serialization round-trip mismatch is diagnostic only and is
never redistributed across likelihood components.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
CURRENT_Q = "Q012"
CODE_VERSION = "1.0-q011-fixed-vector-act-nonact-attribution"
DEFAULT_CONFIG = "q012_likelihood_attribution_v1_config.yml"


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"CONFIG_GATE=FAIL non-mapping config: {path}")
    return data


def cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return load_yaml(p)


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def numeric_key(d: dict[str, Any], target: float, tol: float = 1e-9) -> str | None:
    for k in d:
        try:
            if math.isclose(float(k), float(target), rel_tol=0.0, abs_tol=tol):
                return k
        except Exception:
            pass
    return None


def sign_class(x: float, tol: float) -> str:
    if abs(float(x)) <= tol:
        return "NEAR_ZERO"
    return "POSITIVE_COST" if x > 0 else "NEGATIVE_IMPROVEMENT"


def sign_relation(old: float, new: float, tol: float) -> str:
    a, b = sign_class(old, tol), sign_class(new, tol)
    if "NEAR_ZERO" in (a, b):
        return "NEAR_ZERO_OR_INDETERMINATE"
    return "SIGN_PRESERVED" if a == b else "SIGN_FLIPPED"


def map_delta(new: dict[str, float], old: dict[str, float]) -> dict[str, float]:
    keys = sorted(set(new) | set(old))
    return {k: float(new.get(k, 0.0)) - float(old.get(k, 0.0)) for k in keys}


def nested_map_delta(
    new: dict[str, dict[str, float]], old: dict[str, dict[str, float]]
) -> dict[str, dict[str, float]]:
    return {
        k: map_delta(new.get(k, {}), old.get(k, {}))
        for k in sorted(set(new) | set(old))
    }


def dominant_positive(d: dict[str, float]) -> str | None:
    return max(d, key=lambda k: float(d[k])) if d else None


def dominant_negative(d: dict[str, float]) -> str | None:
    return min(d, key=lambda k: float(d[k])) if d else None


def flatten_cells(d: dict[str, dict[str, float]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for a, inner in d.items():
        for b, v in inner.items():
            out[f"{a} x {b}"] = float(v)
    return out


def runtime_modules():
    # Imported only for preflight/run. Aggregate remains lightweight.
    import q005_hpc_v14 as core
    import q009_act_corrected_minima_attribution_v8 as q009
    import q010_nonact_likelihood_attribution_v3 as q010
    return core, q009, q010


def validate_project(c: dict[str, Any]) -> None:
    if c.get("project", {}).get("q") != CURRENT_Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c.get("execution", {}).get("reoptimize") is not False:
        raise RuntimeError("NO_REOPTIMIZATION_GATE=FAIL")
    if c.get("execution", {}).get("fixed_vector_only") is not True:
        raise RuntimeError("FIXED_VECTOR_ONLY_GATE=FAIL")


def base_model_and_needed(c: dict[str, Any]):
    core, _, q010 = runtime_modules()
    base = core.load_cfg(c["parent"]["base_config"])
    if base.get("project", {}).get("q") != "Q-005":
        raise RuntimeError("BACKEND_Q_GATE=FAIL")
    probe = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = q010.sampled_names(probe)
    return core, q010, base, needed


def q007_baseline_vector(
    c: dict[str, Any], q7: dict[str, Any], needed: set[str]
) -> tuple[dict[str, float], dict[str, Any]]:
    _, _, q010 = runtime_modules()
    if q7.get("q") != "Q-007":
        raise RuntimeError("Q007_BASELINE_PARENT_GATE=FAIL")
    if q7.get("model") != "ede_n3" or q7.get("status") != "PASS":
        raise RuntimeError("Q007_BASELINE_MODEL_STATUS_GATE=FAIL")
    h0 = q7.get("target_h0")
    expected_h0 = float(c["baseline"]["h0"])
    if not isinstance(h0, (int, float)) or not math.isclose(
        float(h0), expected_h0, rel_tol=0.0,
        abs_tol=float(c["gates"]["h0_tolerance"])
    ):
        raise RuntimeError("Q007_BASELINE_H0_GATE=FAIL")
    raw = q7.get("fixed_sampled_parameters")
    if not isinstance(raw, dict):
        raise RuntimeError("Q007_BASELINE_VECTOR_GATE=FAIL missing vector")

    vals = q010.extract_param_vector(raw, set(needed) - {"H0"})
    if "H0" in needed:
        vals["H0"] = expected_h0
    missing = sorted(set(needed) - set(vals))
    if missing:
        raise RuntimeError(f"Q007_BASELINE_VECTOR_GATE=FAIL missing={missing}")
    return vals, q7


def q011_target_vector(
    c: dict[str, Any], q11: dict[str, Any], needed: set[str]
) -> tuple[dict[str, float], dict[str, Any], dict[str, Any]]:
    _, _, q010 = runtime_modules()
    p = c["q011_parent"]
    if q11.get("q") != "Q011":
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL wrong_q")
    if q11.get("run_id") != p["run_id"]:
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL wrong_run_id")
    if q11.get("result_identifier") != p["result_id"]:
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL wrong_result_id")
    if q11.get("combined_globality_classification") != "BEST-OBSERVED MINIMUM ONLY":
        raise RuntimeError("Q011_GLOBALITY_STATUS_GATE=FAIL")
    if q11.get("mathematical_globality_proven") is not False:
        raise RuntimeError("Q011_GLOBALITY_STATUS_GATE=FAIL mathematical_globality")

    profiles = q11.get("profile_targets")
    if not isinstance(profiles, dict):
        raise RuntimeError("Q011_TARGET_GATE=FAIL missing profile_targets")
    target = float(p["target_h0"])
    key = numeric_key(profiles, target)
    if key is None:
        raise RuntimeError("Q011_TARGET_GATE=FAIL missing H0=71.5")
    rec = profiles[key]
    if not isinstance(rec, dict):
        raise RuntimeError("Q011_TARGET_GATE=FAIL malformed target")
    if rec.get("classification") != "BEST-OBSERVED MINIMUM ONLY":
        raise RuntimeError("Q011_TARGET_CLASSIFICATION_GATE=FAIL")
    chi2 = rec.get("best_chi2")
    if not isinstance(chi2, (int, float)) or not math.isclose(
        float(chi2), float(p["chi2"]),
        rel_tol=0.0, abs_tol=float(c["gates"]["parent_chi2_identity_tolerance"])
    ):
        raise RuntimeError(
            f"Q011_PARENT_CHI2_GATE=FAIL actual={chi2} expected={p['chi2']}"
        )
    best = rec.get("best_record")
    if not isinstance(best, dict) or best.get("status") != "PASS":
        raise RuntimeError("Q011_BEST_RECORD_GATE=FAIL")
    bestfit = best.get("bestfit")
    if not isinstance(bestfit, dict):
        raise RuntimeError("Q011_BEST_RECORD_GATE=FAIL missing bestfit")

    vals = q010.extract_param_vector(bestfit, set(needed) - {"H0"})
    if "H0" in needed:
        vals["H0"] = target
    missing = sorted(set(needed) - set(vals))
    if missing:
        raise RuntimeError(f"Q011_EXACT_VECTOR_GATE=FAIL missing={missing}")
    return vals, rec, best


def point_vector(
    c: dict[str, Any],
    point: str,
    q7: dict[str, Any],
    q11: dict[str, Any],
    needed: set[str],
) -> tuple[dict[str, float], dict[str, Any]]:
    if point == "baseline":
        vals, parent = q007_baseline_vector(c, q7, needed)
        meta = {
            "point_label": "baseline",
            "job_id": "POINT-BASELINE",
            "point_role": "ATTRIBUTION_BASELINE_SERIALIZED_Q007_VECTOR",
            "source_id": "INTERNAL-Q005 + INTERNAL-Q007",
            "target_h0": float(c["baseline"]["h0"]),
            "documented_parent_chi2_total": float(c["baseline"]["chi2"]),
            "parent_status": "Q005_OPTIMIZER_NATIVE_BASELINE",
            "parent_record_hash": canonical_hash(parent),
        }
        return vals, meta

    if point == "q011_71.5":
        vals, rec, best = q011_target_vector(c, q11, needed)
        meta = {
            "point_label": "q011_71.5",
            "job_id": "POINT-Q011-71P5",
            "point_role": "Q011_BEST_OBSERVED_SERIALIZED_VECTOR",
            "source_id": c["q011_parent"]["result_id"],
            "target_h0": float(c["q011_parent"]["target_h0"]),
            "documented_parent_chi2_total": float(c["q011_parent"]["chi2"]),
            "parent_status": rec["classification"],
            "q011_best_start_family": best.get("start_family"),
            "q011_best_stage": best.get("stage"),
            "q011_best_convergence_status": best.get("convergence_status"),
            "parent_record_hash": canonical_hash(best),
        }
        return vals, meta

    raise RuntimeError(f"POINT_GATE=FAIL unsupported point={point}")


def evaluate_point(
    c: dict[str, Any],
    point: str,
    q7: dict[str, Any],
    q11: dict[str, Any],
) -> dict[str, Any]:
    validate_project(c)
    core, q009, q010 = runtime_modules()
    base = core.load_cfg(c["parent"]["base_config"])
    if base.get("project", {}).get("q") != "Q-005":
        raise RuntimeError("BACKEND_Q_GATE=FAIL")

    probe = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = q010.sampled_names(probe)
    vals, meta = point_vector(c, point, q7, q11, needed)

    if "A_act" not in vals or "P_act" not in vals:
        raise RuntimeError("ACT_NUISANCE_GATE=FAIL missing A_act/P_act")

    # Q010 V3 reuse: build exact frozen Q005 model, freeze every sampled parameter.
    model_info, base = q010.build_frozen_model(c, vals)

    from cobaya.model import get_model
    model = get_model(model_info)
    lp = model.logposterior({})

    like_names = list(model.likelihood)
    loglikes = [float(x) for x in lp.loglikes]
    if len(like_names) != len(loglikes):
        raise RuntimeError("LIKELIHOOD_COMPONENT_GATE=FAIL name/loglike mismatch")

    aliases = base["likelihood_accounting"]["aliases"]
    required = list(base["likelihood_accounting"]["required_nonlocal"])
    components: dict[str, float] = {}
    raw: dict[str, float] = {}
    unmapped: dict[str, float] = {}
    for name, loglike in zip(like_names, loglikes):
        chi2 = -2.0 * loglike
        raw[str(name)] = chi2
        comp = q010.normalize_likelihood_name(str(name), aliases)
        if comp is None:
            unmapped[str(name)] = chi2
        else:
            components[comp] = components.get(comp, 0.0) + chi2

    missing_components = sorted(set(required) - set(components))
    if missing_components:
        raise RuntimeError(
            f"LIKELIHOOD_COMPONENT_GATE=FAIL missing={missing_components}"
        )
    scientific_total = float(sum(components[k] for k in required))

    # Q009 V8 reuse: ACT full-covariance observable attribution on the SAME model.
    like = q009.act_like(model)
    cl = q009.theory_cl(like)
    act = q009.attribute(
        like,
        cl,
        float(vals["A_act"]),
        float(vals["P_act"]),
        c["bands"],
    )

    finite = all(
        isinstance(components.get(k), (int, float))
        and math.isfinite(float(components[k]))
        for k in c["component_order"]
    ) and math.isfinite(scientific_total)

    act_component = float(components["act_dr6"])
    act_reconstructed = float(act["chi2_act_reconstructed"])
    act_component_error = abs(act_component - act_reconstructed)
    act_component_pass = (
        act_component_error <= float(c["gates"]["act_component_crosscheck_tolerance"])
    )
    act_quadratic_pass = (
        float(act["closure_abs_error"])
        <= float(c["gates"]["act_quadratic_closure_tolerance"])
    )

    parent_total = float(meta["documented_parent_chi2_total"])
    roundtrip_delta = scientific_total - parent_total

    gates = {
        "Q_IDENTITY_GATE": "PASS",
        "CONTEXT_CONTINUITY_GATE": "PASS",
        "BACKEND_Q_GATE": "PASS",
        "EXACT_VECTOR_GATE": "PASS",
        "NO_REOPTIMIZATION_GATE": "PASS",
        "LIKELIHOOD_COMPONENT_GATE": "PASS",
        "FINITE_SERIALIZED_POINT_GATE": "PASS" if finite else "FAIL",
        "ACT_LIKELIHOOD_GATE": "PASS",
        "ACT_QUADRATIC_CLOSURE_GATE": "PASS" if act_quadratic_pass else "FAIL",
        "ACT_COMPONENT_CROSSCHECK_GATE": "PASS" if act_component_pass else "FAIL",
        "PARENT_TOTAL_ROUNDTRIP_GATE": "DIAGNOSTIC_ONLY",
    }
    status = "PASS" if (
        finite and act_component_pass and act_quadratic_pass
    ) else "FAIL"

    return {
        "q": CURRENT_Q,
        "run_id": c["project"]["run_id"],
        "result_id": c["project"]["result_id"],
        "code_version": CODE_VERSION,
        **meta,
        "model": "ede_n3",
        "scientific_surface": "FROZEN_Q005_V14",
        "reoptimized": False,
        "fixed_vector_sha256": canonical_hash(vals),
        "fixed_sampled_parameters": vals,
        "chi2_components": {k: float(components[k]) for k in required},
        "chi2_serialized_vector_total": scientific_total,
        "documented_parent_chi2_total": parent_total,
        "serialized_roundtrip_delta_chi2": roundtrip_delta,
        "serialized_roundtrip_abs_error": abs(roundtrip_delta),
        "serialized_roundtrip_role": (
            "DIAGNOSTIC_ONLY_NOT_A_PASS_FAIL_CRITERION; do not redistribute "
            "this offset across likelihood components."
        ),
        "act": act,
        "act_component_crosscheck": {
            "q010_component_chi2": act_component,
            "q009_reconstructed_chi2": act_reconstructed,
            "abs_error": act_component_error,
            "tolerance": float(c["gates"]["act_component_crosscheck_tolerance"]),
            "status": "PASS" if act_component_pass else "FAIL",
        },
        "raw_likelihood_chi2": raw,
        "unmapped_likelihood_chi2": unmapped,
        "gates": gates,
        "sources": c["sources"],
        "status": status,
    }


def act_delta(target_act: dict[str, Any], baseline_act: dict[str, Any]) -> dict[str, Any]:
    return {
        "delta_chi2_act": (
            float(target_act["chi2_act_reconstructed"])
            - float(baseline_act["chi2_act_reconstructed"])
        ),
        "delta_by_spectrum": map_delta(
            target_act["by_spectrum_signed_fullcov"],
            baseline_act["by_spectrum_signed_fullcov"],
        ),
        "delta_by_band": map_delta(
            target_act["by_band_signed_fullcov"],
            baseline_act["by_band_signed_fullcov"],
        ),
        "delta_by_spectrum_band": nested_map_delta(
            target_act["by_spectrum_band_signed_fullcov"],
            baseline_act["by_spectrum_band_signed_fullcov"],
        ),
    }


def q009_old_71p5(q9: dict[str, Any]) -> dict[str, Any]:
    if q9.get("q") != "Q-009":
        raise RuntimeError("HISTORICAL_Q009_PARENT_GATE=FAIL")
    pts = q9.get("points")
    if not isinstance(pts, list):
        raise RuntimeError("HISTORICAL_Q009_PARENT_GATE=FAIL missing points")
    for p in pts:
        if isinstance(p, dict) and math.isclose(
            float(p.get("target_h0", -1)), 71.5, rel_tol=0.0, abs_tol=1e-9
        ):
            return p
    raise RuntimeError("HISTORICAL_Q009_PARENT_GATE=FAIL missing H0=71.5")


def q010_old_71p5(q10: dict[str, Any]) -> dict[str, Any]:
    if q10.get("q") != "Q-010":
        raise RuntimeError("HISTORICAL_Q010_PARENT_GATE=FAIL")
    targets = q10.get("targets")
    if not isinstance(targets, dict):
        raise RuntimeError("HISTORICAL_Q010_PARENT_GATE=FAIL missing targets")
    k = numeric_key(targets, 71.5)
    if k is None:
        raise RuntimeError("HISTORICAL_Q010_PARENT_GATE=FAIL missing H0=71.5")
    return targets[k]


def historical_snapshot_checks(
    c: dict[str, Any], old9: dict[str, Any], old10: dict[str, Any]
) -> tuple[dict[str, Any], bool]:
    tol = float(c["gates"]["historical_snapshot_tolerance"])
    snap = c["historical_71p5"]

    old9_delta = float(old9["corrected_minus_q005_baseline"]["delta_chi2_act"])
    checks: dict[str, Any] = {
        "q009_delta_chi2_act": {
            "artifact": old9_delta,
            "handoff": float(snap["q009_delta_chi2_act"]),
            "abs_error": abs(old9_delta - float(snap["q009_delta_chi2_act"])),
        }
    }

    old_nonact = old10["delta_chi2_nonact_components_vs_attribution_baseline"]
    known = {
        "planck_lowl": snap.get("planck_lowl"),
        "desi_dr2": snap.get("desi_dr2"),
    }
    for k, expected in known.items():
        if expected is None:
            continue
        actual = float(old_nonact[k])
        checks[k] = {
            "artifact": actual,
            "handoff": float(expected),
            "abs_error": abs(actual - float(expected)),
        }

    net = float(old10["delta_chi2_nonact_net_vs_attribution_baseline"])
    checks["nonact_net"] = {
        "artifact": net,
        "handoff": float(snap["nonact_net"]),
        "abs_error": abs(net - float(snap["nonact_net"])),
    }

    ok = all(float(v["abs_error"]) <= tol for v in checks.values())
    for v in checks.values():
        v["status"] = "PASS" if float(v["abs_error"]) <= tol else "FAIL"
        v["tolerance"] = tol
    return checks, ok


def comparison_record(old: float, new: float, tol: float) -> dict[str, Any]:
    return {
        "old": float(old),
        "new": float(new),
        "new_minus_old": float(new) - float(old),
        "old_sign": sign_class(float(old), tol),
        "new_sign": sign_class(float(new), tol),
        "sign_relation": sign_relation(float(old), float(new), tol),
    }


def aggregate(
    c: dict[str, Any],
    inputs: list[str],
    q009_old_path: str,
    q010_old_path: str,
    output: str,
    manifest_output: str,
    handoff_output: str,
) -> dict[str, Any]:
    validate_project(c)
    rows = [load_json(p) for p in inputs]
    rows = [
        r for r in rows
        if r.get("q") == CURRENT_Q
        and r.get("run_id") == c["project"]["run_id"]
    ]
    by_label = {str(r.get("point_label")): r for r in rows}
    expected = {"baseline", "q011_71.5"}
    complete = (
        set(by_label) == expected
        and all(by_label[k].get("status") == "PASS" for k in expected)
    )

    manifest = {
        "q": CURRENT_Q,
        "run_id": c["project"]["run_id"],
        "expected_jobs": ["POINT-BASELINE", "POINT-Q011-71P5"],
        "completed_jobs": [
            by_label[k]["job_id"] for k in sorted(expected & set(by_label))
            if by_label[k].get("status") == "PASS"
        ],
        "failed_jobs": [
            by_label[k]["job_id"] for k in sorted(expected & set(by_label))
            if by_label[k].get("status") != "PASS"
        ],
        "pending_jobs": sorted(expected - set(by_label)),
        "merge_id": "MERGE-001",
        "test_id": "TEST-001-FINAL-ATTRIBUTION-GATES",
        "job_completeness_gate": "PASS" if complete else "FAIL",
    }
    dump_json(manifest_output, manifest)

    result: dict[str, Any] = {
        "q": CURRENT_Q,
        "run_id": c["project"]["run_id"],
        "result_id": c["project"]["result_id"],
        "code_version": CODE_VERSION,
        "status": "UNRESOLVED",
        "scientific_question": c["project"]["scientific_question"],
        "execution_mode": "MOTOR_PLUS_HPC_FIXED_VECTOR_ATTRIBUTION",
        "model": "ede_n3",
        "scientific_surface": "FROZEN_Q005_V14",
        "q011_globality_status_preserved": "BEST-OBSERVED MINIMUM ONLY",
        "mathematical_globality_proven": False,
        "ede_physical_viability_tested": False,
        "jobs": manifest,
        "gates": {
            "Q_IDENTITY_GATE": "PASS",
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "JOB_COMPLETENESS_GATE": "PASS" if complete else "FAIL",
        },
        "sources": c["sources"],
        "claim_boundary": c["claim_boundary"],
    }
    if not complete:
        result["missing_or_failed"] = (
            sorted(expected - set(by_label))
            + [k for k, r in by_label.items() if r.get("status") != "PASS"]
        )
        result["gates"]["FINAL_RESULT_GATE"] = "UNRESOLVED"
        dump_json(output, result)
        dump_json(handoff_output, {
            "q": CURRENT_Q,
            "status": "UNRESOLVED",
            "reason": "INCOMPLETE_EXECUTION",
            "return_route": "RESULT INGESTION & ROUTING ENGINE",
        })
        return result

    base = by_label["baseline"]
    target = by_label["q011_71.5"]
    components = list(c["component_order"])
    deltas = {
        k: float(target["chi2_components"][k]) - float(base["chi2_components"][k])
        for k in components
    }
    nonact = {k: deltas[k] for k in c["non_act_components"]}
    nonact_net = float(sum(nonact.values()))
    serialized_total_delta = (
        float(target["chi2_serialized_vector_total"])
        - float(base["chi2_serialized_vector_total"])
    )
    component_sum = float(sum(deltas.values()))
    component_closure_error = abs(serialized_total_delta - component_sum)
    component_closure_pass = (
        component_closure_error <= float(c["gates"]["component_closure_tolerance"])
    )

    new_act = act_delta(target["act"], base["act"])
    act_delta_component_error = abs(
        float(new_act["delta_chi2_act"]) - float(deltas["act_dr6"])
    )
    act_delta_component_pass = (
        act_delta_component_error
        <= float(c["gates"]["act_component_crosscheck_tolerance"])
    )

    old9_parent = load_json(q009_old_path)
    old10_parent = load_json(q010_old_path)
    old9 = q009_old_71p5(old9_parent)
    old10 = q010_old_71p5(old10_parent)
    hist_checks, hist_ok = historical_snapshot_checks(c, old9, old10)

    old_act_delta = old9["corrected_minus_q005_baseline"]
    old_nonact = old10["delta_chi2_nonact_components_vs_attribution_baseline"]
    old_nonact_net = float(old10["delta_chi2_nonact_net_vs_attribution_baseline"])
    sign_tol = float(c["gates"]["sign_zero_tolerance"])

    component_compare: dict[str, Any] = {}
    for k in c["non_act_components"]:
        if k in old_nonact:
            component_compare[k] = comparison_record(
                float(old_nonact[k]), float(nonact[k]), sign_tol
            )

    act_compare = comparison_record(
        float(old_act_delta["delta_chi2_act"]),
        float(new_act["delta_chi2_act"]),
        sign_tol,
    )
    nonact_compare = comparison_record(old_nonact_net, nonact_net, sign_tol)

    new_dom_spectrum = dominant_positive(new_act["delta_by_spectrum"])
    new_dom_band = dominant_positive(new_act["delta_by_band"])
    new_cells = flatten_cells(new_act["delta_by_spectrum_band"])
    new_dom_cell_cost = dominant_positive(new_cells)
    new_dom_cell_improvement = dominant_negative(new_cells)

    old_top = old9.get("topology_comparison", {})
    old_dom_spectrum = old_top.get("corrected_dominant_spectrum")
    old_dom_band = old_top.get("corrected_dominant_band")
    act_topology_relation = (
        "PERSISTS"
        if old_dom_spectrum == new_dom_spectrum and old_dom_band == new_dom_band
        else "CHANGED"
    )

    known_relations = [
        act_compare["sign_relation"],
        nonact_compare["sign_relation"],
        *[x["sign_relation"] for x in component_compare.values()],
    ]
    if all(x == "SIGN_PRESERVED" for x in known_relations):
        qualitative = "QUALITATIVE_SIGN_PATTERN_PERSISTS"
    elif any(x == "SIGN_FLIPPED" for x in known_relations):
        qualitative = "QUALITATIVE_SIGN_PATTERN_CHANGED"
    else:
        qualitative = "PARTIALLY_PERSISTS_WITH_NEAR_ZERO_COMPONENTS"

    parent_native_delta = (
        float(c["q011_parent"]["chi2"]) - float(c["baseline"]["chi2"])
    )
    old_parent_native_delta = (
        float(c["historical_71p5"]["q008_parent_chi2"])
        - float(c["baseline"]["chi2"])
    )

    per_point_gates_pass = all(
        r["gates"].get("ACT_QUADRATIC_CLOSURE_GATE") == "PASS"
        and r["gates"].get("ACT_COMPONENT_CROSSCHECK_GATE") == "PASS"
        and r["gates"].get("FINITE_SERIALIZED_POINT_GATE") == "PASS"
        for r in (base, target)
    )
    mandatory_pass = (
        complete
        and per_point_gates_pass
        and component_closure_pass
        and act_delta_component_pass
        and hist_ok
    )

    result.update({
        "status": "PASS" if mandatory_pass else "UNRESOLVED",
        "baseline": {
            "target_h0": base["target_h0"],
            "fixed_vector_sha256": base["fixed_vector_sha256"],
            "chi2_serialized_vector_total": base["chi2_serialized_vector_total"],
            "documented_optimizer_native_chi2": base["documented_parent_chi2_total"],
            "serialized_roundtrip_delta_chi2": base["serialized_roundtrip_delta_chi2"],
        },
        "q011_target": {
            "target_h0": target["target_h0"],
            "fixed_vector_sha256": target["fixed_vector_sha256"],
            "documented_optimizer_native_chi2": target["documented_parent_chi2_total"],
            "q011_classification": target["parent_status"],
            "chi2_serialized_vector_total": target["chi2_serialized_vector_total"],
            "serialized_roundtrip_delta_chi2": target["serialized_roundtrip_delta_chi2"],
            "best_stage": target.get("q011_best_stage"),
            "best_start_family": target.get("q011_best_start_family"),
            "best_convergence_status": target.get("q011_best_convergence_status"),
        },
        "optimizer_native_parent_scalar_track": {
            "q005_reference_h0": float(c["baseline"]["h0"]),
            "q005_reference_chi2": float(c["baseline"]["chi2"]),
            "old_q008_71p5_chi2": float(c["historical_71p5"]["q008_parent_chi2"]),
            "old_q008_delta_chi2_vs_q005": old_parent_native_delta,
            "new_q011_71p5_chi2": float(c["q011_parent"]["chi2"]),
            "new_q011_delta_chi2_vs_q005": parent_native_delta,
            "q011_minus_q008": (
                float(c["q011_parent"]["chi2"])
                - float(c["historical_71p5"]["q008_parent_chi2"])
            ),
            "role": (
                "AUTHORITATIVE OPTIMIZER-NATIVE SCALARS; NOT FORCED TO CLOSE "
                "AGAINST FINITE-PRECISION SERIALIZED-VECTOR COMPONENT DELTAS."
            ),
        },
        "serialized_vector_attribution_track": {
            "delta_chi2_total": serialized_total_delta,
            "delta_chi2_components": deltas,
            "delta_chi2_act": float(new_act["delta_chi2_act"]),
            "delta_chi2_nonact_components": nonact,
            "delta_chi2_nonact_net": nonact_net,
            "component_closure_abs_error": component_closure_error,
            "component_closure_gate": "PASS" if component_closure_pass else "FAIL",
            "act_component_delta_crosscheck_abs_error": act_delta_component_error,
            "act_component_delta_crosscheck_gate": (
                "PASS" if act_delta_component_pass else "FAIL"
            ),
        },
        "act_observable_attribution_new": {
            "delta_by_spectrum_signed_fullcov": new_act["delta_by_spectrum"],
            "delta_by_band_signed_fullcov": new_act["delta_by_band"],
            "delta_by_spectrum_band_signed_fullcov": new_act["delta_by_spectrum_band"],
            "dominant_positive_cost_spectrum": new_dom_spectrum,
            "dominant_positive_cost_band": new_dom_band,
            "dominant_positive_cost_cell": new_dom_cell_cost,
            "dominant_negative_improvement_cell": new_dom_cell_improvement,
            "covariance_note": (
                "Signed d_i(C^-1 d)_i attribution is additive but covariance-coupled; "
                "grouped TT/TE/EE and ell bands are not statistically independent likelihoods."
            ),
        },
        "q009_q010_historical_comparison": {
            "historical_snapshot_crosschecks": hist_checks,
            "act_delta_chi2": act_compare,
            "nonact_net_delta_chi2": nonact_compare,
            "nonact_components": component_compare,
            "old_q009_corrected_dominant_spectrum": old_dom_spectrum,
            "new_q012_dominant_spectrum": new_dom_spectrum,
            "old_q009_corrected_dominant_band": old_dom_band,
            "new_q012_dominant_band": new_dom_band,
            "act_topology_relation": act_topology_relation,
            "qualitative_sign_pattern_relation": qualitative,
            "interpretation_rule": (
                "No arbitrary material-change threshold is imposed. Report exact old/new "
                "deltas, sign preservation/flips, and ACT topology preservation/change."
            ),
        },
        "roundtrip_diagnostics": {
            "baseline": {
                "documented_parent_total": base["documented_parent_chi2_total"],
                "serialized_total": base["chi2_serialized_vector_total"],
                "delta": base["serialized_roundtrip_delta_chi2"],
            },
            "q011_71p5": {
                "documented_parent_total": target["documented_parent_chi2_total"],
                "serialized_total": target["chi2_serialized_vector_total"],
                "delta": target["serialized_roundtrip_delta_chi2"],
            },
            "gate": "DIAGNOSTIC_ONLY",
            "rule": "DO_NOT_REDISTRIBUTE_ROUNDTRIP_OFFSET_ACROSS_COMPONENTS",
        },
        "journal_effect": {
            "Q005_V14": "KEEP_UNCHANGED",
            "Q011": "KEEP_BEST_OBSERVED_MINIMUM_ONLY_AND_DO_NOT_REOPEN",
            "Q009_71p5": (
                "SUPERSEDE_STALE_Q008_POINT_ATTRIBUTION_WITH_Q012"
                if mandatory_pass else "KEEP_STALE_PENDING_VALID_Q012"
            ),
            "Q010_71p5": (
                "SUPERSEDE_STALE_Q008_POINT_ATTRIBUTION_WITH_Q012"
                if mandatory_pass else "KEEP_STALE_PENDING_VALID_Q012"
            ),
            "PAT-001": (
                "UPDATE_USING_OBSERVED_ATTRIBUTION_CHANGE_ONLY"
                if mandatory_pass else "NO_CHANGE_PENDING_VALID_RESULT"
            ),
            "MOD-EDE-N3": "KEEP_ACTIVE_BUT_CONDITIONAL; NO_PHYSICAL_PROMOTION",
        },
        "unresolved_issues": [
            "Q011 mathematical globality is not proven.",
            "Q011 strong numerical near-global certification was not achieved.",
            "Q012 does not test external EDE viability or physical consistency.",
            "Finite-precision serialized-vector roundtrip mismatch remains diagnostic only.",
        ],
    })

    result["gates"].update({
        "Q011_PARENT_IDENTITY_GATE": "PASS",
        "Q011_TARGET_CLASSIFICATION_GATE": "PASS",
        "Q011_EXACT_VECTOR_GATE": "PASS",
        "FROZEN_BACKEND_GATE": "PASS",
        "NO_REOPTIMIZATION_GATE": "PASS",
        "FINITE_SERIALIZED_POINT_GATE": "PASS" if per_point_gates_pass else "FAIL",
        "ACT_QUADRATIC_CLOSURE_GATE": "PASS" if per_point_gates_pass else "FAIL",
        "ACT_COMPONENT_CROSSCHECK_GATE": "PASS" if act_delta_component_pass else "FAIL",
        "COMPONENT_CLOSURE_GATE": "PASS" if component_closure_pass else "FAIL",
        "HISTORICAL_Q009_Q010_SNAPSHOT_GATE": "PASS" if hist_ok else "FAIL",
        "PARENT_TOTAL_ROUNDTRIP_GATE": "DIAGNOSTIC_ONLY",
        "GLOBALITY_GATE": "UNRESOLVED_BEST_OBSERVED_ONLY",
        "PHYSICAL_VIABILITY_GATE": "NOT_TESTED",
        "SCIENTIFIC_INTERPRETATION_GATE": "PASS" if mandatory_pass else "UNRESOLVED",
        "FINAL_RESULT_GATE": "PASS" if mandatory_pass else "UNRESOLVED",
    })

    result["provenance"] = {
        "bubbleverse_repository": c["parent"]["repository"],
        "q012_execution_commit": os.environ.get("GITHUB_SHA"),
        "q012_github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "runner_os": os.environ.get("RUNNER_OS"),
        "runner_arch": os.environ.get("RUNNER_ARCH"),
        "python": platform.python_version(),
        "program_file": Path(__file__).name,
        "program_sha256": sha256_file(__file__),
        "config_file": c["_config_file"] if "_config_file" in c else DEFAULT_CONFIG,
        "config_sha256": sha256_file(
            ROOT / (c["_config_file"] if "_config_file" in c else DEFAULT_CONFIG)
        ),
        "frozen_parent_commit": c["parent"]["frozen_reference_commit"],
        "q011_parent_run_id": c["q011_parent"]["github_run_id"],
        "q011_parent_result_id": c["q011_parent"]["result_id"],
        "q009_engine_reused": c["reuse"]["q009_engine"],
        "q010_engine_reused": c["reuse"]["q010_engine"],
        "q005_engine_reused": c["parent"]["base_engine"],
    }

    dump_json(output, result)

    handoff = {
        "q": CURRENT_Q,
        "status": result["status"],
        "scientific_question": c["project"]["scientific_question"],
        "new_result": {
            "optimizer_native_parent_scalar_track": result["optimizer_native_parent_scalar_track"],
            "serialized_vector_attribution_track": result["serialized_vector_attribution_track"],
            "act_observable_attribution_new": result["act_observable_attribution_new"],
            "historical_comparison": result["q009_q010_historical_comparison"],
        } if mandatory_pass else "NOT_AVAILABLE_FINAL_GATE_UNRESOLVED",
        "journal_effect": result["journal_effect"],
        "sources": c["sources"],
        "provenance": result["provenance"],
        "test_status": result["gates"],
        "unresolved_issues": result["unresolved_issues"],
        "next_required_action": (
            "Send Q012 through Result Ingestion & Routing Engine, then Motor 14. "
            "Do not create Q013 before Q012 is documented."
            if mandatory_pass else
            "Repair only failed Q012 technical/test gate; do not reopen Q011."
        ),
        "return_route": "RESULT INGESTION & ROUTING ENGINE",
    }
    dump_json(handoff_output, handoff)
    return result


def preflight(c: dict[str, Any], q7_path: str, q11_path: str) -> int:
    validate_project(c)
    core, q010, base, needed = base_model_and_needed(c)
    env = core.preflight(base)
    if env.get("status") != "PASS":
        print(json.dumps({
            "q": CURRENT_Q, "status": "FAIL",
            "gate": "ENVIRONMENT_GATE", "parent_preflight": env
        }, indent=2))
        return 5

    q7, q11 = load_json(q7_path), load_json(q11_path)
    q007_baseline_vector(c, q7, needed)
    q011_target_vector(c, q11, needed)
    out = {
        "q": CURRENT_Q,
        "status": "PASS",
        "gate": "CONTEXT_VECTOR_AND_FROZEN_BACKEND_PREFLIGHT",
        "needed_parameters": sorted(needed),
        "q011_target_h0": c["q011_parent"]["target_h0"],
        "q011_parent_chi2": c["q011_parent"]["chi2"],
        "reoptimization": False,
    }
    print(json.dumps(out, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--q007-baseline", required=True)
    p.add_argument("--q011", required=True)

    p = sub.add_parser("run")
    p.add_argument("--q007-baseline", required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--point", required=True, choices=["baseline", "q011_71.5"])
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate")
    p.add_argument("--inputs", nargs="*", default=[])
    p.add_argument("--q009-old", required=True)
    p.add_argument("--q010-old", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--manifest-output", required=True)
    p.add_argument("--handoff-output", required=True)

    a = ap.parse_args()
    c = cfg(a.config)
    c["_config_file"] = Path(a.config).name

    if a.cmd == "preflight":
        return preflight(c, a.q007_baseline, a.q011)

    if a.cmd == "run":
        q7, q11 = load_json(a.q007_baseline), load_json(a.q011)
        r = evaluate_point(c, a.point, q7, q11)
        dump_json(a.output, r)
        print(json.dumps({
            "q": CURRENT_Q, "status": r["status"],
            "point": a.point, "output": a.output
        }, indent=2))
        return 0 if r["status"] == "PASS" else 6

    if a.cmd == "aggregate":
        r = aggregate(
            c, a.inputs, a.q009_old, a.q010_old,
            a.output, a.manifest_output, a.handoff_output
        )
        print(json.dumps({
            "q": CURRENT_Q,
            "status": r["status"],
            "final_result_gate": r.get("gates", {}).get("FINAL_RESULT_GATE"),
            "output": a.output,
        }, indent=2))
        return 0 if r.get("gates", {}).get("FINAL_RESULT_GATE") == "PASS" else 7

    return 9


if __name__ == "__main__":
    raise SystemExit(main())
