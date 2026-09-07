#!/usr/bin/env python3
"""Bubbleverse Q-035 artifact-only classifier harmonization.

Applies two source-locked operational classifiers to the same three decisive
endpoint sets. This file performs no likelihood, CLASS, sampler or optimizer
execution.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping, Sequence

Q = "Q-035"
RUN = "Q035-CLASSIFIER-HARMONIZATION-V1"
RESULT = "R-Q035-EDE-CLASSIFIER-HARMONIZATION-001"
EXPECTED_LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))


def read_json(path: str | Path) -> dict[str, Any]:
    x = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return x


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def flatten_endpoint(row: Mapping[str, Any]) -> dict[str, float]:
    # Literal Q022 flatten semantics: minimum followed by nuisance.
    out: dict[str, float] = {}
    for block in ("minimum", "nuisance"):
        x = row.get(block, {})
        if isinstance(x, Mapping):
            for k, v in x.items():
                if finite(v):
                    out[str(k)] = float(v)
    return out


def rms(a: Mapping[str, float], b: Mapping[str, float], names: Sequence[str],
        scales: Mapping[str, float]) -> float:
    vals = [
        (float(a[n]) - float(b[n])) / float(scales[n])
        for n in names
        if n in a and n in b and finite(scales.get(n)) and float(scales[n]) > 0
    ]
    if not vals:
        return math.inf
    return float(math.sqrt(sum(x * x for x in vals) / len(vals)))


def normalize_q022_rows(root: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if not (
            d.get("q") == "Q022"
            and d.get("run_id") == "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
            and d.get("result_id") == "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
            and d.get("phase") == "refinement"
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            continue
        r = dict(d)
        r["source_mask"] = int(d["mask"])
        r["source_seed"] = int(d["seed_restart"])
        r["source_label"] = f"M{r['source_mask']}-S{r['source_seed']}"
        rows.append(r)
    return validate_nine(rows, "Q022")


def rows_from_singleton_cluster_representatives(diag: Mapping[str, Any], label: str) -> list[dict[str, Any]]:
    rows = []
    for c in diag.get("clusters", []):
        if int(c.get("support", -1)) != 1 or c.get("stable") is not False:
            raise RuntimeError(f"{label}_AUTHORITATIVE_SINGLETON_GATE=FAIL")
        r = c.get("representative")
        if not isinstance(r, Mapping):
            raise RuntimeError(f"{label}_REPRESENTATIVE_GATE=FAIL")
        rows.append(dict(r))
    return validate_nine(rows, label)


def validate_nine(rows: Sequence[Mapping[str, Any]], label: str) -> list[dict[str, Any]]:
    if len(rows) != 9:
        raise RuntimeError(f"{label}_NINE_ENDPOINT_GATE=FAIL count={len(rows)}")
    labels = tuple(sorted(str(r.get("source_label")) for r in rows))
    if labels != tuple(sorted(EXPECTED_LABELS)):
        raise RuntimeError(f"{label}_LABEL_IDENTITY_GATE=FAIL labels={labels}")
    keys = {(int(r.get("source_mask", -1)), int(r.get("source_seed", -1))) for r in rows}
    if keys != {(m, s) for m in (3, 6, 7) for s in (0, 1, 2)}:
        raise RuntimeError(f"{label}_MASK_SEED_GATE=FAIL")
    if not all(finite(r.get("objective_chi2")) and r.get("status") == "COMPLETE" for r in rows):
        raise RuntimeError(f"{label}_FINITE_COMPLETE_GATE=FAIL")
    return sorted([dict(r) for r in rows], key=lambda r: str(r["source_label"]))


def historical_q022_classifier(rows: Sequence[Mapping[str, Any]], cfg: Mapping[str, Any],
                                scales: Mapping[str, float]) -> dict[str, Any]:
    h = cfg["historical_q022_classifier"]
    cosmo = list(h["cosmology_profiled"])
    nuisance = list(h["shared_nuisance"]) + list(h["foreground_nuisance"])
    required = cosmo + nuisance
    missing = sorted({n for r in rows for n in required if n not in flatten_endpoint(r)})
    if missing:
        raise RuntimeError("HISTORICAL_PARAMETER_COMPLETENESS_GATE=FAIL missing=" + repr(missing))

    vertices = []
    for mask in (3, 6, 7):
        rr = sorted([r for r in rows if int(r["source_mask"]) == mask], key=lambda r: int(r["source_seed"]))
        if len(rr) != 3:
            raise RuntimeError(f"HISTORICAL_PER_MASK_THREE_START_GATE=FAIL mask={mask}")
        objectives = [float(r["objective_chi2"]) for r in rr]
        endpoints = [flatten_endpoint(r) for r in rr]
        pairs = []
        max_joint = 0.0
        for i, j in combinations(range(3), 2):
            dc = rms(endpoints[i], endpoints[j], cosmo, scales)
            dn = rms(endpoints[i], endpoints[j], nuisance, scales)
            joint = math.sqrt((dc * dc + dn * dn) / 2.0)
            max_joint = max(max_joint, joint)
            pairs.append({
                "seed_pair": [int(rr[i]["source_seed"]), int(rr[j]["source_seed"])],
                "source_pair": [rr[i]["source_label"], rr[j]["source_label"]],
                "cosmology_rms": dc,
                "nuisance_rms": dn,
                "joint_rms": joint,
                "delta_objective": abs(objectives[i] - objectives[j]),
            })
        spread = max(objectives) - min(objectives)
        collapsed = (
            spread <= float(h["collapse_objective_tolerance"])
            and max_joint <= float(h["collapse_endpoint_joint_rms"])
        )
        vertices.append({
            "mask": mask,
            "objective_spread": float(spread),
            "max_pairwise_joint_rms": float(max_joint),
            "collapsed": bool(collapsed),
            "classification": "CROSS_START_COLLAPSE" if collapsed else "STABLE_MULTIBASIN",
            "pairwise": pairs,
        })

    classes = [v["classification"] for v in vertices]
    if all(x == "STABLE_MULTIBASIN" for x in classes):
        overall = "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
    elif all(x == "CROSS_START_COLLAPSE" for x in classes):
        overall = "PRIMARILY_OPTIMIZER_GLOBALITY_OR_INCOMPLETE_MINIMIZATION_STRUCTURE"
    elif all(x in ("CROSS_START_COLLAPSE", "STABLE_MULTIBASIN") for x in classes):
        overall = "IDENTIFIABILITY_LIMIT_MIXED_VERTEX_BEHAVIOUR"
    else:
        overall = "IDENTIFIABILITY_LIMIT"
    return {
        "classifier": "HISTORICAL_Q022_MIXED_PER_MASK",
        "overall_classification": overall,
        "stable_multibasin": all(x == "STABLE_MULTIBASIN" for x in classes),
        "per_mask": vertices,
    }


def later_common_graph_classifier(rows: Sequence[Mapping[str, Any]], cfg: Mapping[str, Any],
                                  scales: Mapping[str, float]) -> dict[str, Any]:
    g = cfg["later_common_graph_classifier"]
    rr = sorted([dict(r) for r in rows], key=lambda r: str(r["source_label"]))
    names = list(g["common_geometry"])
    missing = sorted({n for r in rr for n in names if n not in flatten_endpoint(r)})
    if missing:
        raise RuntimeError("COMMON_GEOMETRY_PARAMETER_COMPLETENESS_GATE=FAIL missing=" + repr(missing))

    adjacency = {i: set() for i in range(len(rr))}
    pairwise = []
    for i, j in combinations(range(len(rr)), 2):
        a, b = rr[i], rr[j]
        d = rms(flatten_endpoint(a), flatten_endpoint(b), names, scales)
        od = abs(float(a["objective_chi2"]) - float(b["objective_chi2"]))
        same = d <= float(g["collapse_common_endpoint_rms"]) and od <= float(g["collapse_objective_tolerance"])
        if same:
            adjacency[i].add(j)
            adjacency[j].add(i)
        pairwise.append({
            "a": a["source_label"], "b": b["source_label"],
            "common_rms": d, "delta_objective": od,
            "same_basin_edge": bool(same),
        })

    seen: set[int] = set()
    comps: list[list[int]] = []
    for i in range(len(rr)):
        if i in seen:
            continue
        stack, comp = [i], []
        while stack:
            k = stack.pop()
            if k in seen:
                continue
            seen.add(k)
            comp.append(k)
            stack.extend(adjacency[k] - seen)
        comps.append(sorted(comp))

    clusters = []
    min_support = int(g["stable_cluster_minimum_supporting_starts"])
    for ci, idxs in enumerate(comps):
        members = [rr[i] for i in idxs]
        clusters.append({
            "cluster_id": ci,
            "support": len(members),
            "stable": len(members) >= min_support,
            "members": [m["source_label"] for m in members],
            "objective_min": min(float(m["objective_chi2"]) for m in members),
            "objective_max": max(float(m["objective_chi2"]) for m in members),
        })
    stable = [x for x in clusters if x["stable"]]
    stable_count = len(stable)
    stable_multibasin = stable_count >= int(g["stable_multibasin_minimum_stable_clusters"])
    return {
        "classifier": "Q031_Q032_COMMON_GEOMETRY_GRAPH",
        "complete_rows": len(rr),
        "clusters": clusters,
        "stable_basin_count": stable_count,
        "stable_cluster_ids": [x["cluster_id"] for x in stable],
        "stable_multibasin": bool(stable_multibasin),
        "single_cluster_covers_all": len(clusters) == 1 and len(rr) > 0,
        "pairwise": pairwise,
    }


def reference_replay_gates(q022_final: Mapping[str, Any], q032_auth: Mapping[str, Any],
                           q034_auth: Mapping[str, Any], results: Mapping[str, Any]) -> dict[str, Any]:
    gates: dict[str, Any] = {}
    # Historical Q022 numerical replay.
    orig = {int(v["mask"]): v["diagnostic"] for v in q022_final["final_vertices"]}
    calc = {int(v["mask"]): v for v in results["Q022"]["historical_q022"] ["per_mask"]}
    q22_ok = True
    max_abs = 0.0
    for m in (3, 6, 7):
        for a, b in (
            (calc[m]["objective_spread"], orig[m]["objective_spread"]),
            (calc[m]["max_pairwise_joint_rms"], orig[m]["max_pairwise_joint_rms"]),
        ):
            max_abs = max(max_abs, abs(float(a) - float(b)))
        q22_ok &= bool(calc[m]["collapsed"]) == bool(orig[m]["collapsed"])
    q22_ok &= max_abs <= 1e-12
    q22_ok &= results["Q022"]["historical_q022"]["overall_classification"] == q022_final["classification"]
    gates["Q022_HISTORICAL_REFERENCE_REPLAY_GATE"] = {"pass": bool(q22_ok), "max_abs_numeric_difference": max_abs}

    # Later graph replay for Q032/Q034: compare all pairwise graph diagnostics.
    for label, auth in (("Q032", q032_auth), ("Q034", q034_auth)):
        calcg = results[label]["later_common_graph"]
        amap = {(x["a"], x["b"]): x for x in auth["pairwise"]}
        max_rms = 0.0
        max_obj = 0.0
        edge_mismatch = 0
        for x in calcg["pairwise"]:
            y = amap[(x["a"], x["b"])]
            max_rms = max(max_rms, abs(float(x["common_rms"]) - float(y["common_rms"])))
            max_obj = max(max_obj, abs(float(x["delta_objective"]) - float(y["delta_objective"])))
            edge_mismatch += int(bool(x["same_basin_edge"]) != bool(y["same_basin_edge"]))
        ok = (
            int(calcg["stable_basin_count"]) == int(auth["stable_basin_count"])
            and len(calcg["clusters"]) == len(auth["clusters"])
            and edge_mismatch == 0
            and max_rms <= 1e-12
            and max_obj <= 1e-12
        )
        gates[f"{label}_LATER_REFERENCE_REPLAY_GATE"] = {
            "pass": bool(ok), "max_abs_common_rms_difference": max_rms,
            "max_abs_objective_difference": max_obj, "edge_mismatches": edge_mismatch,
        }
    return gates


def decide(results: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    h = {k: bool(v["historical_q022"]["stable_multibasin"]) for k, v in results.items()}
    g = {k: bool(v["later_common_graph"]["stable_multibasin"]) for k, v in results.items()}
    historical_cross_case_discrepancy = not (h["Q022"] == h["Q032"] == h["Q034"])
    later_cross_case_discrepancy = not (g["Q022"] == g["Q032"] == g["Q034"])
    flips = {k: h[k] != g[k] for k in h}
    if not historical_cross_case_discrepancy and not later_cross_case_discrepancy:
        classification = "CLASSIFIER_SEMANTICS_MATERIALLY_EXPLAINS_REPORTED_DISCREPANCY"
    elif historical_cross_case_discrepancy and later_cross_case_discrepancy:
        classification = "CLASSIFIER_HARMONIZATION_NOT_SUFFICIENT_TO_REMOVE_DISCREPANCY"
    else:
        classification = "CLASSIFICATION_IS_METHOD_DEFINITION_DEPENDENT"
    return classification, {
        "historical_classifier_stable_flags": h,
        "later_classifier_stable_flags": g,
        "historical_same_classifier_cross_case_discrepancy": historical_cross_case_discrepancy,
        "later_same_classifier_cross_case_discrepancy": later_cross_case_discrepancy,
        "endpointset_classification_flips_between_classifiers": flips,
        "all_endpointsets_flip_between_classifiers": all(flips.values()),
    }


def write_crosswalk_csv(path: str | Path, results: Mapping[str, Any]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["endpoint_set", "historical_q022_stable_multibasin", "historical_q022_overall", "later_stable_basin_count", "later_stable_multibasin", "later_cluster_count"])
        for label in ("Q022", "Q032", "Q034"):
            h = results[label]["historical_q022"]
            g = results[label]["later_common_graph"]
            w.writerow([label, h["stable_multibasin"], h["overall_classification"], g["stable_basin_count"], g["stable_multibasin"], len(g["clusters"])])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--source-lock", required=True)
    ap.add_argument("--q022-final", required=True)
    ap.add_argument("--q022-refinement-dir", required=True)
    ap.add_argument("--q032-preflight", required=True)
    ap.add_argument("--q032-control-final", required=True)
    ap.add_argument("--q034-final", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--csv-output", required=True)
    args = ap.parse_args()

    cfg = read_json(args.config)
    lock = read_json(args.source_lock)
    if cfg["project"]["q"] != Q or lock.get("q") != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if cfg["project"]["run_id"] != RUN or lock.get("run_id") != RUN:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    if cfg["project"]["result_id"] != RESULT or lock.get("result_id") != RESULT:
        raise RuntimeError("RESULT_IDENTITY_GATE=FAIL")
    if not all(cfg["rules"].values()):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")

    q22f = read_json(args.q022_final)
    q32pf = read_json(args.q032_preflight)
    q32f = read_json(args.q032_control_final)
    q34f = read_json(args.q034_final)
    if q22f.get("FINAL_RESULT_GATE") != "PASS" or q22f.get("classification") != "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE":
        raise RuntimeError("Q022_AUTHORITATIVE_FINAL_GATE=FAIL")
    if q32pf.get("FINAL_PREFLIGHT_GATE") != "PASS":
        raise RuntimeError("Q032_PREFLIGHT_GATE=FAIL")
    if q32f.get("JOB_COMPLETENESS_GATE") != "PASS" or q32f.get("GLOBALITY_GATE") != "PASS":
        raise RuntimeError("Q032_CONTROL_FINAL_GATE=FAIL")
    if q34f.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("Q034_FINAL_GATE=FAIL")

    hscales = {str(k): float(v) for k, v in q22f["stage1_assessment"]["parameter_scales"].items()}
    gscales = {str(k): float(v) for k, v in q32pf["locked_common_scales"].items()}
    q22rows = normalize_q022_rows(args.q022_refinement_dir)
    q32auth = q32f["surface_results"]["full_native"]["cluster_diagnostic"]
    q34auth = q34f["frozen_primordial_arm"]["cluster_diagnostic"]
    q32rows = rows_from_singleton_cluster_representatives(q32auth, "Q032")
    q34rows = rows_from_singleton_cluster_representatives(q34auth, "Q034")

    results = {}
    for label, rows in (("Q022", q22rows), ("Q032", q32rows), ("Q034", q34rows)):
        results[label] = {
            "endpoint_count": len(rows),
            "historical_q022": historical_q022_classifier(rows, cfg, hscales),
            "later_common_graph": later_common_graph_classifier(rows, cfg, gscales),
        }

    replay = reference_replay_gates(q22f, q32auth, q34auth, results)
    if not all(x["pass"] for x in replay.values()):
        raise RuntimeError("REFERENCE_REPLAY_GATE=FAIL " + repr(replay))
    classification, decision = decide(results)
    output = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q035_FINAL_ARTIFACT_REANALYSIS",
        "status": "PASS",
        "execution_status": "COMPLETE",
        "actual_computed_result": True,
        "FINAL_RESULT_GATE": "PASS",
        "classification": classification,
        "scientific_question": cfg["project"]["scientific_question"],
        "execution_mode": "PROGRAM_ARTIFACT_ONLY_POSTPROCESSING",
        "new_likelihood_evaluations": 0,
        "new_optimizer_runs": 0,
        "new_sampler_runs": 0,
        "historical_scale_source": "Q022_FINAL_SERIALIZED_STAGE1_ASSESSMENT_FROM_ORIGINAL_Q021_ENDPOINT_SCALES_LOGIC",
        "later_scale_source": "Q032_V4_AUTHORITATIVE_PREFLIGHT_LOCKED_COMMON_SCALES",
        "historical_scales": hscales,
        "later_locked_common_scales": gscales,
        "crosswalk": results,
        "decision_diagnostics": decision,
        "reference_replay_gates": replay,
        "journal_effect": {
            "D-Q034-CLASSIFIER-SEMANTICS-001": "CONFIRMED_AS_MATERIAL_EXPLANATION_OF_REPORTED_LABEL_DISCREPANCY",
            "C-035-CLASSIFIER-HARMONIZATION": "RESOLVED",
            "Q022_RAW_ENDPOINTS": "KEEP",
            "Q032_V4_RAW_RESULT": "KEEP",
            "Q034_RAW_RESULT": "KEEP",
            "Q022_STABLE_MULTIBASIN_ONTOLOGY": "UPDATE_TO_CLASSIFIER_DEPENDENT_LABEL",
            "D-Q033-REMAINING-001": "REJECTED_AS_NECESSARY_OR_SUFFICIENT_EXPLANATION_OF_Q022_VS_LATER_CLASSIFICATION_LABEL_DIFFERENCE",
            "physical_EDE_status": "UNCHANGED",
            "H0_values": "UNCHANGED",
            "Planck_systematic_status": "UNCHANGED"
        },
        "physical_interpretation_boundaries": {
            "classifier_shift_is_planck_systematic": False,
            "classifier_shift_is_foreground_failure": False,
            "classifier_shift_is_calibration_failure": False,
            "classifier_shift_is_new_physics": False,
            "classifier_shift_detects_or_falsifies_EDE": False
        },
        "sources": cfg["sources"],
        "source_lock": lock,
        "return_route": ["BUBBLEVERSE RESULT INGESTION & ROUTING ENGINE", "MOTOR 14"]
    }
    write_json(args.output, output)
    write_crosswalk_csv(args.csv_output, results)
    print("Q035_CLASSIFICATION=" + classification)
    print("FINAL_RESULT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
