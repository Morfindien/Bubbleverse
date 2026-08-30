#!/usr/bin/env python3
"""
Bubbleverse Q-009 — corrected-minimum ACT DR6 observable attribution.

Scientific purpose
------------------
At the CURRENT BEST-OBSERVED n=3 EDE fixed-H0 minima from Q-008, evaluate
the same ACT DR6 covariance-aware TT/TE/EE and multipole attribution used
in Q-007, without re-optimization and without changing the frozen Q-005 V14
common backend.

Q-008 points are BEST OBSERVED, not documented global minima.
Q-007 remains the historical before-state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q009_act_corrected_minima_attribution_v3_config.yml"
CODE_VERSION = "3.0-fresh-versioned-schema-fixed"


def jdump(x: Any) -> str:
    return json.dumps(x, indent=2, sort_keys=True)


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return load_yaml(p)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def walk_dicts(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk_dicts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_dicts(v)


def sampled_names(model: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for name, spec in model.get("params", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            names.add(name)
    for lspec in model.get("likelihood", {}).values():
        if isinstance(lspec, dict) and isinstance(lspec.get("params"), dict):
            for name, spec in lspec["params"].items():
                if isinstance(spec, dict) and "prior" in spec:
                    names.add(name)
    return names


def extract_param_vector(bestfit: dict[str, Any], needed: set[str]) -> dict[str, float]:
    candidates: list[dict[str, Any]] = []
    if isinstance(bestfit, dict):
        candidates.append(bestfit)
        for key in ("params", "sampled", "sampled_params", "point", "values"):
            if isinstance(bestfit.get(key), dict):
                candidates.append(bestfit[key])

    found: dict[str, float] = {}
    for block in candidates:
        for k, v in block.items():
            if k in needed and isinstance(v, (int, float)) and math.isfinite(float(v)):
                found[k] = float(v)

    missing = sorted(needed - set(found))
    if missing:
        raise RuntimeError(
            f"Q008_EXACT_POINT_GATE=FAIL missing_sampled_parameters={missing}"
        )
    return found


def import_core():
    sys.path.insert(0, str(ROOT))
    import q005_hpc_v14 as core
    return core


def freeze_all_sampled(model: dict[str, Any], vals: dict[str, float]) -> None:
    for name, spec in list(model.get("params", {}).items()):
        if name in vals and isinstance(spec, dict) and "prior" in spec:
            model["params"][name] = float(vals[name])

    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict) or not isinstance(lspec.get("params"), dict):
            continue
        for name, spec in list(lspec["params"].items()):
            if name in vals and isinstance(spec, dict) and "prior" in spec:
                lspec["params"][name] = float(vals[name])

    model.pop("sampler", None)
    model.pop("output", None)


def build_frozen_model(c: dict[str, Any], vals: dict[str, float]):
    core = import_core()
    base = core.load_cfg(c["parent"]["base_config"])
    if base["project"]["q"] != "Q-005":
        raise RuntimeError("BACKEND_Q_GATE=FAIL")

    model = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(model)
    missing = sorted(needed - set(vals))
    if missing:
        raise RuntimeError(f"POINT_COVERAGE_GATE=FAIL missing={missing}")

    freeze_all_sampled(model, vals)
    return model, base


def get_model(info: dict[str, Any]):
    from cobaya.model import get_model as cobaya_get_model
    model = cobaya_get_model(info)
    logpost = model.logposterior({})
    return model, logpost


def act_like(model):
    for name, like in model.likelihood.items():
        if "ACTDR6CMBonly" in str(name) or like.__class__.__name__ == "ACTDR6CMBonly":
            return like
    raise RuntimeError("ACT_LIKELIHOOD_GATE=FAIL")


def theory_cl(like):
    return like.provider.get_Cl(ell_factor=True)


def prediction_and_meta(like, cl, A_act: float, P_act: float):
    pred_all = np.zeros_like(like.data_vec, dtype=float)
    rows = []

    for meta in like.spec_meta:
        idx = np.asarray(meta["idx"], dtype=int)
        win = meta["window"].weight.T
        ls = np.asarray(meta["window"].values, dtype=int)
        pol = meta["pol"]

        dat = np.asarray(cl[pol])[ls] / (A_act * A_act)
        if pol[0] == "e":
            dat = dat / P_act
        if pol[1] == "e":
            dat = dat / P_act

        pred = win @ dat
        pred_all[idx] = pred
        ell = np.asarray(meta["ell"], dtype=float)

        for j, ii in enumerate(idx):
            rows.append(
                (
                    int(ii),
                    pol.upper(),
                    float(ell[j]),
                    float(like.data_vec[ii]),
                    float(pred[j]),
                )
            )
    return pred_all, rows


def band_name(ell: float, bands: list[dict[str, Any]]) -> str:
    for band in bands:
        if float(band["ell_min"]) <= ell <= float(band["ell_max"]):
            return str(band["name"])
    return "UNASSIGNED"


def attribute(like, cl, A_act: float, P_act: float, bands: list[dict[str, Any]]):
    pred, rows = prediction_and_meta(like, cl, A_act, P_act)
    delta = np.asarray(like.data_vec) - pred
    z = like.inv_cov @ delta
    contrib = delta * z
    full = float(delta @ z)

    by_pol: dict[str, float] = {}
    by_band: dict[str, float] = {}
    by_pol_band: dict[str, dict[str, float]] = {}
    residuals = []

    for ii, pol, ell, data, prediction in rows:
        c = float(contrib[ii])
        band = band_name(ell, bands)
        by_pol[pol] = by_pol.get(pol, 0.0) + c
        by_band[band] = by_band.get(band, 0.0) + c
        by_pol_band.setdefault(pol, {})
        by_pol_band[pol][band] = by_pol_band[pol].get(band, 0.0) + c

        var = float(like.covmat[ii, ii])
        sigma = math.sqrt(var) if var > 0 else None
        residuals.append(
            {
                "index": ii,
                "pol": pol,
                "ell_eff": ell,
                "data": data,
                "prediction": prediction,
                "residual": data - prediction,
                "sigma_diag": sigma,
                "pull_diag": ((data - prediction) / sigma) if sigma else None,
                "signed_fullcov_chi2_attribution": c,
            }
        )

    closure = float(sum(contrib))
    return {
        "chi2_act_reconstructed": full,
        "chi2_attribution_sum": closure,
        "closure_abs_error": abs(full - closure),
        "by_spectrum_signed_fullcov": by_pol,
        "by_band_signed_fullcov": by_band,
        "by_spectrum_band_signed_fullcov": by_pol_band,
        "statistical_independence": False,
        "interpretation": (
            "Exact additive attribution of d_i(C^-1 d)_i. Groups are "
            "covariance-coupled and are not independent chi-square likelihoods."
        ),
        "residuals": residuals,
    }



def q005_baseline(c: dict[str, Any], q005: Any) -> dict[str, Any]:
    if q005.get("q") != "Q-005":
        raise RuntimeError("Q005_BASELINE_GATE=FAIL wrong_q")

    models = q005.get("models", {})
    rec = models.get("ede_n3") if isinstance(models, dict) else None
    if not isinstance(rec, dict):
        raise RuntimeError("Q005_BASELINE_GATE=FAIL missing_models.ede_n3")

    bestfit = rec.get("bestfit")
    chi2 = rec.get("chi2_scientific_total")
    if not isinstance(bestfit, dict) or not isinstance(chi2, (int, float)):
        raise RuntimeError("Q005_BASELINE_GATE=FAIL incomplete_ede_n3_record")

    expected_h0 = float(c["historical_baseline"]["h0"])
    expected_chi2 = float(c["historical_baseline"]["q005_best_known_chi2"])
    h0_tol = float(c["gates"].get("baseline_h0_tolerance", 1e-6))
    chi2_tol = float(c["gates"].get("baseline_chi2_tolerance", 1e-3))

    h0 = bestfit.get("H0", bestfit.get("h0"))
    if not isinstance(h0, (int, float)):
        raise RuntimeError("Q005_BASELINE_GATE=FAIL missing_H0")
    if not math.isclose(float(h0), expected_h0, rel_tol=0.0, abs_tol=h0_tol):
        raise RuntimeError(
            f"Q005_BASELINE_GATE=FAIL H0={h0} expected={expected_h0}"
        )
    if not math.isclose(float(chi2), expected_chi2, rel_tol=0.0, abs_tol=chi2_tol):
        raise RuntimeError(
            f"Q005_BASELINE_GATE=FAIL chi2={chi2} expected={expected_chi2}"
        )

    return rec


def _numeric_profile_key(d: dict[str, Any], target_h0: float) -> str | None:
    for k in d:
        try:
            if math.isclose(float(k), float(target_h0), rel_tol=0.0, abs_tol=1e-9):
                return k
        except Exception:
            pass
    return None


def q008_target(q008: Any, target_h0: float) -> dict[str, Any]:
    if q008.get("q") != "Q-008":
        raise RuntimeError("Q008_BEST_OBSERVED_GATE=FAIL wrong_q")

    profiles = q008.get("profile_targets")
    if not isinstance(profiles, dict):
        raise RuntimeError("Q008_BEST_OBSERVED_GATE=FAIL missing_profile_targets")

    key = _numeric_profile_key(profiles, target_h0)
    if key is None:
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL missing_target H0={target_h0}"
        )

    rec = profiles[key]
    if not isinstance(rec, dict):
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL malformed_target H0={target_h0}"
        )

    bestfit = rec.get("bestfit")
    if not isinstance(bestfit, dict):
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL missing_bestfit H0={target_h0}"
        )

    parse_status = bestfit.get("parse_status")
    if parse_status not in (None, "PASS"):
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL bestfit_parse_status={parse_status} H0={target_h0}"
        )

    chi2 = rec.get("best_observed_chi2")
    if not isinstance(chi2, (int, float)) or not math.isfinite(float(chi2)):
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL missing_best_observed_chi2 H0={target_h0}"
        )

    return rec


def q007_historical(q007: Any, target_h0: float) -> dict[str, Any]:
    if q007.get("q") != "Q-007":
        raise RuntimeError("Q007_COMPARISON_GATE=FAIL wrong_q")

    models = q007.get("models", {})
    ede = models.get("ede_n3") if isinstance(models, dict) else None
    profiles = ede.get("profiles") if isinstance(ede, dict) else None
    if not isinstance(profiles, dict):
        raise RuntimeError("Q007_COMPARISON_GATE=FAIL missing_models.ede_n3.profiles")

    key = _numeric_profile_key(profiles, target_h0)
    if key is None:
        raise RuntimeError(f"Q007_COMPARISON_GATE=FAIL missing H0={target_h0}")

    rec = profiles[key]
    if not isinstance(rec, dict):
        raise RuntimeError(f"Q007_COMPARISON_GATE=FAIL malformed H0={target_h0}")

    for required in ("delta_by_spectrum", "delta_by_band", "delta_chi2_act"):
        if required not in rec:
            raise RuntimeError(
                f"Q007_COMPARISON_GATE=FAIL missing_{required} H0={target_h0}"
            )
    return rec


def map_delta(new: dict[str, float], old: dict[str, float]) -> dict[str, float]:
    keys = sorted(set(new) | set(old))
    return {k: float(new.get(k, 0.0)) - float(old.get(k, 0.0)) for k in keys}


def nested_map_delta(new: dict[str, dict[str, float]], old: dict[str, dict[str, float]]):
    out = {}
    for pol in sorted(set(new) | set(old)):
        out[pol] = map_delta(new.get(pol, {}), old.get(pol, {}))
    return out


def dominant_positive(d: dict[str, float]) -> str | None:
    if not d:
        return None
    return max(d, key=lambda k: float(d[k]))


def historical_dominant(rec: dict[str, Any], kind: str) -> str | None:
    candidates = (
        f"dominant_{kind}",
        f"dominant_positive_{kind}",
        f"q007_dominant_{kind}",
    )
    for k in candidates:
        if isinstance(rec.get(k), str):
            return rec[k]
    field = "delta_by_spectrum" if kind == "spectrum" else "delta_by_band"
    d = rec.get(field, {})
    return dominant_positive(d) if isinstance(d, dict) else None


def act_delta(corrected: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "delta_chi2_act": (
            float(corrected["chi2_act_reconstructed"])
            - float(baseline["chi2_act_reconstructed"])
        ),
        "delta_by_spectrum": map_delta(
            corrected["by_spectrum_signed_fullcov"],
            baseline["by_spectrum_signed_fullcov"],
        ),
        "delta_by_band": map_delta(
            corrected["by_band_signed_fullcov"],
            baseline["by_band_signed_fullcov"],
        ),
        "delta_by_spectrum_band": nested_map_delta(
            corrected["by_spectrum_band_signed_fullcov"],
            baseline["by_spectrum_band_signed_fullcov"],
        ),
    }


def preflight(c: dict[str, Any], args) -> dict[str, Any]:
    q5 = load_json(args.q005) if Path(args.q005).is_file() else {}
    q7 = load_json(args.q007) if Path(args.q007).is_file() else {}
    q8 = load_json(args.q008) if Path(args.q008).is_file() else {}

    checks = {
        "Q_IDENTITY_GATE": c["project"]["q"] == "Q-009",
        "PARENT_Q005_GATE": q5.get("q") == "Q-005",
        "COMPARISON_Q007_GATE": q7.get("q") == "Q-007",
        "PARENT_Q008_GATE": q8.get("q") == "Q-008",
        "BASE_ENGINE_EXISTS": (ROOT / c["parent"]["base_engine"]).is_file(),
        "BASE_CONFIG_EXISTS": (ROOT / c["parent"]["base_config"]).is_file(),
        "NO_REOPTIMIZATION_GATE": c["execution"]["reoptimize"] is False,
        "TARGET_GATE": [float(x) for x in c["targets"]] == [71.5, 72.5, 73.5],
        "Q008_BASELINE_EXCLUSION_GATE": 70.853292 not in [float(x) for x in c["targets"]],
    }

    # Structural gates use the real parent schemas.
    try:
        q005_baseline(c, q5)
        checks["Q005_BASELINE_GATE"] = True
    except Exception:
        checks["Q005_BASELINE_GATE"] = False

    try:
        for h in c["targets"]:
            q008_target(q8, float(h))
        checks["Q008_PROFILE_TARGETS_GATE"] = True
    except Exception:
        checks["Q008_PROFILE_TARGETS_GATE"] = False

    try:
        for h in c["targets"]:
            q007_historical(q7, float(h))
        checks["Q007_PROFILE_GATE"] = True
    except Exception:
        checks["Q007_PROFILE_GATE"] = False

    return {
        "q": "Q-009",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }


def run_point(c: dict[str, Any], args) -> dict[str, Any]:
    q5 = load_json(args.q005)
    q7 = load_json(args.q007)
    q8 = load_json(args.q008)
    target = float(args.target_h0)

    if target not in [float(x) for x in c["targets"]]:
        raise RuntimeError(f"TARGET_GATE=FAIL H0={target}")

    baseline_rec = q005_baseline(c, q5)
    corrected_rec = q008_target(q8, target)
    historical = q007_historical(q7, target)

    core = import_core()
    base = core.load_cfg(c["parent"]["base_config"])
    tmp = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(tmp)

    baseline_vals = extract_param_vector(baseline_rec["bestfit"], needed - {"H0"})
    baseline_vals["H0"] = float(c["historical_baseline"]["h0"])

    corrected_vals = extract_param_vector(corrected_rec["bestfit"], needed - {"H0"})
    corrected_vals["H0"] = target

    if "A_act" not in baseline_vals or "P_act" not in baseline_vals:
        raise RuntimeError("Q005_ACT_NUISANCE_GATE=FAIL missing A_act/P_act")
    if "A_act" not in corrected_vals or "P_act" not in corrected_vals:
        raise RuntimeError("Q008_ACT_NUISANCE_GATE=FAIL missing A_act/P_act")

    # Reconstruct the Q005 baseline ACT attribution under the same frozen backend.
    baseline_info, _ = build_frozen_model(c, baseline_vals)
    baseline_model, _ = get_model(baseline_info)
    baseline_like = act_like(baseline_model)
    baseline_cl = theory_cl(baseline_like)
    baseline_act = attribute(
        baseline_like,
        baseline_cl,
        float(baseline_vals["A_act"]),
        float(baseline_vals["P_act"]),
        c["bands"],
    )

    # Evaluate the corrected Q008 point, no optimization.
    corrected_info, _ = build_frozen_model(c, corrected_vals)
    corrected_model, _ = get_model(corrected_info)
    corrected_like = act_like(corrected_model)
    corrected_cl = theory_cl(corrected_like)
    corrected_act = attribute(
        corrected_like,
        corrected_cl,
        float(corrected_vals["A_act"]),
        float(corrected_vals["P_act"]),
        c["bands"],
    )

    baseline_closure_ok = (
        float(baseline_act["closure_abs_error"])
        <= float(c["gates"]["closure_tolerance"])
    )
    corrected_closure_ok = (
        float(corrected_act["closure_abs_error"])
        <= float(c["gates"]["closure_tolerance"])
    )

    new_delta = act_delta(corrected_act, baseline_act)
    new_dom_spectrum = dominant_positive(new_delta["delta_by_spectrum"])
    new_dom_band = dominant_positive(new_delta["delta_by_band"])
    old_dom_spectrum = historical_dominant(historical, "spectrum")
    old_dom_band = historical_dominant(historical, "band")

    expected_spectrum = c["topology_test"]["q007_expected_dominant_spectrum"]
    expected_band = c["topology_test"]["q007_expected_dominant_band"]

    topology_persists = (
        old_dom_spectrum == expected_spectrum
        and old_dom_band == expected_band
        and new_dom_spectrum == expected_spectrum
        and new_dom_band == expected_band
    )

    result = {
        "q": "Q-009",
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "scientific_question": c["project"]["scientific_question"],
        "model": "ede_n3",
        "target_h0": target,
        "point_status": "CURRENT_BEST_OBSERVED_UNDER_Q008_FINITE_SEARCH",
        "global_minimum_claim": False,
        "reoptimized": False,
        "q005_baseline": {
            "H0": float(c["historical_baseline"]["h0"]),
            "chi2_scientific_total": float(baseline_rec["chi2_scientific_total"]),
            "bestfit_sha256": canonical_hash(baseline_rec["bestfit"]),
            "fixed_sampled_parameters": baseline_vals,
            "act": baseline_act,
        },
        "q008_corrected": {
            "H0": target,
            "status": corrected_rec.get("status"),
            "best_observed_chi2": float(corrected_rec["best_observed_chi2"]),
            "best_start_family": corrected_rec.get("best_start_family"),
            "boundary_flags": corrected_rec.get("boundary_flags", corrected_rec.get("boundary_warnings", [])),
            "chi2_components": corrected_rec.get("chi2_components", {}),
            "bestfit_sha256": canonical_hash(corrected_rec["bestfit"]),
            "fixed_sampled_parameters": corrected_vals,
            "act": corrected_act,
        },
        "corrected_minus_q005_baseline": new_delta,
        "q007_historical": {
            "delta_chi2_act": historical.get("delta_chi2_act"),
            "delta_by_spectrum": historical.get("delta_by_spectrum", {}),
            "delta_by_band": historical.get("delta_by_band", {}),
            "dominant_spectrum": old_dom_spectrum,
            "dominant_band": old_dom_band,
        },
        "topology_comparison": {
            "q007_dominant_spectrum": old_dom_spectrum,
            "corrected_dominant_spectrum": new_dom_spectrum,
            "q007_dominant_band": old_dom_band,
            "corrected_dominant_band": new_dom_band,
            "q007_expected_dominant_spectrum": expected_spectrum,
            "q007_expected_dominant_band": expected_band,
            "topology_persists": topology_persists,
            "interpretation": (
                "Persistence means only that the dominant covariance-aware ACT "
                "spectrum and multipole-band topology is stable across the tested "
                "historical and corrected basins. It is not evidence that EDE solves H0."
            ),
        },
        "gates": {
            "Q_IDENTITY_GATE": "PASS",
            "Q005_BASELINE_GATE": "PASS",
            "Q008_EXACT_POINT_GATE": "PASS",
            "Q007_COMPARISON_GATE": "PASS",
            "NO_REOPTIMIZATION_GATE": "PASS",
            "ACT_LIKELIHOOD_GATE": "PASS",
            "Q005_QUADRATIC_CLOSURE_GATE": "PASS" if baseline_closure_ok else "FAIL",
            "Q008_QUADRATIC_CLOSURE_GATE": "PASS" if corrected_closure_ok else "FAIL",
            "COVARIANCE_INTERPRETATION_GATE": "PASS",
        },
        "sources": c["sources"],
        "provenance": {
            "bubbleverse_repo": c["parent"]["repository"],
            "repo_inspection_commit": c["parent"]["repo_inspection_commit"],
            "base_engine": c["parent"]["base_engine"],
            "base_config": c["parent"]["base_config"],
            "q007_engine_reused": c["parent"]["q007_engine"],
            "act_dr6_lite_commit": c["parent"]["act_dr6_lite_commit"],
            "q008_same_h0_548p321909_promoted": False,
        },
        "status": "PASS" if (baseline_closure_ok and corrected_closure_ok) else "FAIL",
    }
    return result


def aggregate(c: dict[str, Any], args) -> dict[str, Any]:
    points = []
    for path in Path(args.input).rglob("q009_v2_point_*.json"):
        try:
            d = load_json(path)
            if d.get("q") == "Q-009" and d.get("status") == "PASS":
                points.append(d)
        except Exception:
            pass

    expected = {round(float(x), 6) for x in c["targets"]}
    got = {round(float(x["target_h0"]), 6) for x in points}
    missing = sorted(expected - got)
    points.sort(key=lambda x: float(x["target_h0"]))

    persistence = {
        str(p["target_h0"]): bool(p["topology_comparison"]["topology_persists"])
        for p in points
    }

    if missing:
        scientific_classification = "UNRESOLVED_INCOMPLETE_EXECUTION"
        topology_result = "UNRESOLVED"
    elif all(persistence.values()):
        scientific_classification = (
            "Q007_TE_INTERMEDIATE_TOPOLOGY_ROBUST_ACROSS_TESTED_CORRECTED_BASINS"
        )
        topology_result = "ROBUST_ACROSS_TESTED_CORRECTED_BASINS"
    elif any(persistence.values()):
        scientific_classification = "Q007_TOPOLOGY_PARTIALLY_PERSISTS"
        topology_result = "PARTIALLY_CHANGED_ACROSS_TESTED_CORRECTED_BASINS"
    else:
        scientific_classification = (
            "Q007_TE_INTERMEDIATE_TOPOLOGY_DOES_NOT_PERSIST_AT_CORRECTED_BASINS"
        )
        topology_result = "MATERIALLY_CHANGED_ACROSS_TESTED_CORRECTED_BASINS"

    final_gate = "PASS" if not missing else "UNRESOLVED"

    return {
        "q": "Q-009",
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "status": "PASS" if final_gate == "PASS" else "UNRESOLVED",
        "scientific_question": c["project"]["scientific_question"],
        "scientific_classification": scientific_classification,
        "claim_boundary": {
            "points_are_best_observed_not_global": True,
            "ede_solves_h0_claim": False,
            "new_physics_claim": False,
            "q008_globality_gate": "UNRESOLVED",
        },
        "historical_q007_preserved": True,
        "q008_h0_70p853292_not_used_as_baseline": True,
        "q005_best_known_h0_70p853292_chi2": float(
            c["historical_baseline"]["q005_best_known_chi2"]
        ),
        "points": points,
        "missing_targets": missing,
        "topology_result": topology_result,
        "per_target_topology_persistence": persistence,
        "gates": {
            "JOB_COMPLETENESS_GATE": "PASS" if not missing else "FAIL",
            "GLOBALITY_GATE": "UNRESOLVED",
            "SCIENTIFIC_INTERPRETATION_GATE": "PASS" if not missing else "UNRESOLVED",
            "FINAL_RESULT_GATE": final_gate,
        },
        "sources": c["sources"],
        "unresolved_issues": [
            "Q-008 GLOBALITY_GATE remains UNRESOLVED; Q-009 does not test mathematical globality."
        ],
        "return_route": "RESULT INGESTION & ROUTING ENGINE",
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--q005", required=True)
    p.add_argument("--q007", required=True)
    p.add_argument("--q008", required=True)

    p = sub.add_parser("run")
    p.add_argument("--q005", required=True)
    p.add_argument("--q007", required=True)
    p.add_argument("--q008", required=True)
    p.add_argument("--target-h0", required=True, type=float)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)

    args = ap.parse_args()
    c = cfg(args.config)

    if args.cmd == "preflight":
        result = preflight(c, args)
        print(jdump(result))
        return 0 if result["status"] == "PASS" else 2

    if args.cmd == "run":
        result = run_point(c, args)
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(jdump(result) + "\n", encoding="utf-8")
        print(jdump({"q": "Q-009", "status": result["status"], "output": str(path)}))
        return 0 if result["status"] == "PASS" else 3

    if args.cmd == "aggregate":
        result = aggregate(c, args)
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(jdump(result) + "\n", encoding="utf-8")
        print(jdump({"q": "Q-009", "status": result["status"], "output": str(path)}))
        return 0 if result["status"] == "PASS" else 4

    return 9


if __name__ == "__main__":
    raise SystemExit(main())
