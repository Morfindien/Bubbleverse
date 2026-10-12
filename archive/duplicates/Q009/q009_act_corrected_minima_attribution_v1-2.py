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
DEFAULT_CONFIG = "q009_act_corrected_minima_attribution_v1_config.yml"
CODE_VERSION = "1.0-q007-topology-retest"


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


def q008_candidates(q008: Any, target_h0: float) -> list[dict[str, Any]]:
    rows = []
    for d in walk_dicts(q008):
        if d.get("q") != "Q-008":
            continue
        if d.get("status") != "PASS":
            continue
        if d.get("model") not in (None, "ede_n3"):
            continue
        if not isinstance(d.get("target_h0"), (int, float)):
            continue
        if not math.isclose(float(d["target_h0"]), float(target_h0), abs_tol=1e-9):
            continue
        if not isinstance(d.get("bestfit"), dict):
            continue
        if not isinstance(d.get("chi2_scientific_total"), (int, float)):
            continue
        rows.append(d)
    return rows


def select_q008_best_observed(q008: Any, target_h0: float) -> dict[str, Any]:
    rows = q008_candidates(q008, target_h0)
    if not rows:
        raise RuntimeError(
            f"Q008_BEST_OBSERVED_GATE=FAIL no_complete_candidate H0={target_h0}"
        )
    best = min(rows, key=lambda x: float(x["chi2_scientific_total"]))
    return best


def q007_old_point(q007: Any, target_h0: float) -> dict[str, Any]:
    matches = []
    for d in walk_dicts(q007):
        if d.get("q") != "Q-007" or d.get("status") != "PASS":
            continue
        if d.get("model") != "ede_n3":
            continue
        if not isinstance(d.get("target_h0"), (int, float)):
            continue
        if not math.isclose(float(d["target_h0"]), float(target_h0), abs_tol=1e-9):
            continue
        if isinstance(d.get("act"), dict):
            matches.append(d)
    if not matches:
        raise RuntimeError(f"Q007_COMPARISON_GATE=FAIL missing H0={target_h0}")
    return matches[0]


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


def dominant_cell(d: dict[str, dict[str, float]]) -> dict[str, Any] | None:
    cells = []
    for pol, bands in d.items():
        for band, value in bands.items():
            cells.append((float(value), pol, band))
    if not cells:
        return None
    value, pol, band = max(cells)
    return {"spectrum": pol, "band": band, "value": value}


def compare_topology(c: dict[str, Any], old_act: dict[str, Any], new_act: dict[str, Any]):
    old_pol = old_act["by_spectrum_signed_fullcov"]
    new_pol = new_act["by_spectrum_signed_fullcov"]
    old_band = old_act["by_band_signed_fullcov"]
    new_band = new_act["by_band_signed_fullcov"]
    old_pb = old_act["by_spectrum_band_signed_fullcov"]
    new_pb = new_act["by_spectrum_band_signed_fullcov"]

    old_cell = dominant_cell(old_pb)
    new_cell = dominant_cell(new_pb)

    expected_pol = c["topology_test"]["q007_expected_dominant_spectrum"]
    expected_band = c["topology_test"]["q007_expected_dominant_band"]

    q007_signature_present = (
        new_cell is not None
        and new_cell["spectrum"] == expected_pol
        and new_cell["band"] == expected_band
    )

    return {
        "old_dominant_spectrum": dominant_positive(old_pol),
        "new_dominant_spectrum": dominant_positive(new_pol),
        "old_dominant_band": dominant_positive(old_band),
        "new_dominant_band": dominant_positive(new_band),
        "old_dominant_spectrum_band_cell": old_cell,
        "new_dominant_spectrum_band_cell": new_cell,
        "q007_te_intermediate_signature_present": q007_signature_present,
        "delta_by_spectrum": map_delta(new_pol, old_pol),
        "delta_by_band": map_delta(new_band, old_band),
        "delta_by_spectrum_band": nested_map_delta(new_pb, old_pb),
    }


def preflight(c: dict[str, Any], args) -> dict[str, Any]:
    q8 = load_json(args.q008) if Path(args.q008).is_file() else {}
    q7 = load_json(args.q007) if Path(args.q007).is_file() else {}

    checks = {
        "Q_IDENTITY_GATE": c["project"]["q"] == "Q-009",
        "PARENT_Q008_GATE": q8.get("q") == "Q-008",
        "COMPARISON_Q007_GATE": q7.get("q") == "Q-007",
        "BASE_ENGINE_EXISTS": (ROOT / c["parent"]["base_engine"]).is_file(),
        "BASE_CONFIG_EXISTS": (ROOT / c["parent"]["base_config"]).is_file(),
        "NO_REOPTIMIZATION_GATE": c["execution"]["reoptimize"] is False,
        "TARGET_GATE": [float(x) for x in c["targets"]] == [71.5, 72.5, 73.5],
        "Q008_BASELINE_EXCLUSION_GATE": 70.853292 not in [float(x) for x in c["targets"]],
    }
    return {
        "q": "Q-009",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }


def run_point(c: dict[str, Any], args) -> dict[str, Any]:
    q8 = load_json(args.q008)
    q7 = load_json(args.q007)
    target = float(args.target_h0)

    if target not in [float(x) for x in c["targets"]]:
        raise RuntimeError(f"TARGET_GATE=FAIL H0={target}")

    corrected = select_q008_best_observed(q8, target)
    old = q007_old_point(q7, target)

    core = import_core()
    base = core.load_cfg(c["parent"]["base_config"])
    tmp = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(tmp)

    vals = extract_param_vector(corrected["bestfit"], needed - {"H0"})
    vals["H0"] = target

    info, _ = build_frozen_model(c, vals)
    model, logpost = get_model(info)
    like = act_like(model)
    cl = theory_cl(like)

    if "A_act" not in vals or "P_act" not in vals:
        raise RuntimeError("ACT_NUISANCE_GATE=FAIL missing A_act/P_act")

    new_act = attribute(
        like,
        cl,
        float(vals["A_act"]),
        float(vals["P_act"]),
        c["bands"],
    )

    closure_ok = (
        float(new_act["closure_abs_error"])
        <= float(c["gates"]["closure_tolerance"])
    )

    comparison = compare_topology(c, old["act"], new_act)

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
        "q008_selected_record_sha256": canonical_hash(corrected),
        "q008_selected_stage": corrected.get("stage"),
        "q008_selected_start_family": corrected.get("start_family"),
        "q008_chi2_scientific_total": float(corrected["chi2_scientific_total"]),
        "q008_chi2_components": corrected.get("chi2_components", {}),
        "fixed_sampled_parameters": vals,
        "fixed_parameter_sha256": canonical_hash(vals),
        "act": new_act,
        "q007_before": {
            "target_h0": old["target_h0"],
            "act": old["act"],
            "point_sha256": old.get("q006_point_sha256"),
        },
        "comparison": comparison,
        "gates": {
            "Q_IDENTITY_GATE": "PASS",
            "Q008_EXACT_POINT_GATE": "PASS",
            "NO_REOPTIMIZATION_GATE": "PASS",
            "ACT_LIKELIHOOD_GATE": "PASS",
            "QUADRATIC_CLOSURE_GATE": "PASS" if closure_ok else "FAIL",
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
        },
        "status": "PASS" if closure_ok else "FAIL",
    }
    return result


def aggregate(c: dict[str, Any], args) -> dict[str, Any]:
    points = []
    for path in Path(args.input).rglob("q009_point_*.json"):
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

    signature = {
        str(p["target_h0"]): bool(
            p["comparison"]["q007_te_intermediate_signature_present"]
        )
        for p in points
    }

    if missing:
        topology_status = "UNRESOLVED"
    elif all(signature.values()):
        topology_status = "ROBUST_ACROSS_TESTED_CORRECTED_BASINS"
    elif any(signature.values()):
        topology_status = "PARTIALLY_CHANGED_ACROSS_TESTED_CORRECTED_BASINS"
    else:
        topology_status = "MATERIALLY_CHANGED_ACROSS_TESTED_CORRECTED_BASINS"

    final_gate = "PASS" if not missing else "UNRESOLVED"

    return {
        "q": "Q-009",
        "run_id": c["project"]["run_id"],
        "status": "PASS" if final_gate == "PASS" else "UNRESOLVED",
        "scientific_question": c["project"]["scientific_question"],
        "claim_boundary": {
            "points_are_best_observed_not_global": True,
            "ede_solves_h0_claim": False,
            "new_physics_claim": False,
        },
        "historical_q007_preserved": True,
        "q008_h0_70p853292_not_used_as_baseline": True,
        "q005_best_known_h0_70p853292_chi2": c["historical_baseline"][
            "q005_best_known_chi2"
        ],
        "points": points,
        "missing_targets": missing,
        "topology_result": topology_status,
        "per_target_q007_te_intermediate_signature": signature,
        "gates": {
            "JOB_COMPLETENESS_GATE": "PASS" if not missing else "FAIL",
            "GLOBALITY_GATE": "UNRESOLVED",
            "SCIENTIFIC_INTERPRETATION_GATE": (
                "PASS" if not missing else "UNRESOLVED"
            ),
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
    p.add_argument("--q008", required=True)
    p.add_argument("--q007", required=True)

    p = sub.add_parser("run")
    p.add_argument("--q008", required=True)
    p.add_argument("--q007", required=True)
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
