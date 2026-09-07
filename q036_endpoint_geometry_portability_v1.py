#!/usr/bin/env python3
"""Bubbleverse Q-036 — artifact-only common-geometry portability analysis V1.

No CLASS, likelihood, optimizer, sampler, or cross-likelihood objective comparison.
The decision uses only the Q031 preregistered common-geometry coordinates,
Q031 locked scales, and authoritative Q022/Q031 endpoints.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping, Sequence

Q = "Q-036"
PROGRAM_ID = "Q036-GEOMETRY-V1"
RUN = "Q036-ENDPOINT-GEOMETRY-PORTABILITY-V1"
RESULT = "R-Q036-EDE-ENDPOINT-GEOMETRY-PORTABILITY-001"
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


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def metric_rms(a: Mapping[str, Any], b: Mapping[str, Any],
               names: Sequence[str], scales: Mapping[str, float]) -> float:
    vals = []
    for n in names:
        if not (finite(a.get(n)) and finite(b.get(n)) and finite(scales.get(n)) and float(scales[n]) > 0):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coordinate={n}")
        vals.append((float(a[n]) - float(b[n])) / float(scales[n]))
    return float(math.sqrt(sum(x * x for x in vals) / len(vals)))


def validate_preregister(pr: Mapping[str, Any]) -> None:
    p = pr.get("project", {})
    if p.get("q") != Q or p.get("program_id") != PROGRAM_ID or p.get("run_id") != RUN or p.get("result_id") != RESULT:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL preregister")
    g = pr.get("common_geometry", {})
    if float(g.get("collapse_scale", -1)) != 0.1:
        raise RuntimeError("PREREGISTER_THRESHOLD_GATE=FAIL")
    if g.get("objective_values_used_in_q036_decision") is not False:
        raise RuntimeError("NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE=FAIL")
    rules = pr.get("rules", {})
    mandatory_true = (
        "q035_closed", "no_stable_label_only_decision",
        "no_cross_likelihood_absolute_chi2_subtraction",
        "no_cross_likelihood_objective_sum", "no_forced_camspec_nuisance_into_hillipop",
        "q022_masks_are_provenance_labels_only", "overlapping_planck_sky_not_independent_observations",
        "reuse_authoritative_endpoints", "no_q022_q031_science_rerun", "no_threshold_tuning",
        "no_physical_systematic_inference",
    )
    if not all(rules.get(k) is True for k in mandatory_true):
        raise RuntimeError("PREREGISTER_RULE_GATE=FAIL")


def validate_source_lock(lock: Mapping[str, Any]) -> None:
    if lock.get("q") != Q or lock.get("program_id") != PROGRAM_ID:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if lock.get("q022", {}).get("result_id") != "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002":
        raise RuntimeError("Q022_SOURCE_LOCK_GATE=FAIL")
    if lock.get("q031", {}).get("result_id") != "R-CASE031-EDE-PLANCK-PORTABILITY-001":
        raise RuntimeError("Q031_SOURCE_LOCK_GATE=FAIL")
    if lock.get("q035", {}).get("result_id") != "R-Q035-EDE-CLASSIFIER-HARMONIZATION-001":
        raise RuntimeError("Q035_SOURCE_LOCK_GATE=FAIL")


def load_q022(q022_dir: str | Path, source_lock: Mapping[str, Any], names: Sequence[str]) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    expected_commit = source_lock["q022"]["execution_commit"]
    for p in Path(q022_dir).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if not (
            d.get("q") == "Q022"
            and d.get("run_id") == "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
            and d.get("result_id") == source_lock["q022"]["result_id"]
            and d.get("phase") == "refinement"
            and d.get("status") == "COMPLETE"
        ):
            continue
        if d.get("bubbleverse_commit") != expected_commit:
            raise RuntimeError(f"PARENT_PROVENANCE_GATE=FAIL q022_commit path={p}")
        label = f"M{int(d['mask'])}-S{int(d['seed_restart'])}"
        if label in rows:
            raise RuntimeError(f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL duplicate={label}")
        minimum = d.get("minimum", {})
        if not isinstance(minimum, Mapping):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL q022={label}")
        rows[label] = {n: float(minimum[n]) for n in names if n in minimum and finite(minimum[n])}
    if tuple(sorted(rows)) != tuple(sorted(EXPECTED_LABELS)):
        raise RuntimeError(f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL q022_labels={sorted(rows)}")
    if any(set(r) != set(names) for r in rows.values()):
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL q022_missing")
    return rows


def load_q031(final_path: str | Path, preflight_path: str | Path,
              source_lock: Mapping[str, Any], names: Sequence[str]) -> tuple[dict[str, dict[str, float]], dict[str, float], dict[str, Any]]:
    final = read_json(final_path)
    pre = read_json(preflight_path)
    if not (
        final.get("q") == "CASE-031"
        and final.get("run_id") == "CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1"
        and final.get("result_id") == source_lock["q031"]["result_id"]
        and final.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("PARENT_PROVENANCE_GATE=FAIL q031_final")
    if not (
        pre.get("q") == "CASE-031"
        and pre.get("run_id") == "CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1"
        and pre.get("result_id") == source_lock["q031"]["result_id"]
        and pre.get("hillipop_commit") == source_lock["q031"]["hillipop_commit"]
    ):
        raise RuntimeError("PARENT_PROVENANCE_GATE=FAIL q031_preflight")

    scales_all = pre.get("locked_common_scales", {})
    scales = {n: float(scales_all[n]) for n in names if n in scales_all and finite(scales_all[n])}
    if set(scales) != set(names) or any(v <= 0 for v in scales.values()):
        raise RuntimeError("Q031_LOCKED_SCALE_GATE=FAIL missing_or_invalid")
    expected_hash = source_lock["q031"]["locked_scales_hash"]
    pre_hash = pre.get("locked_scales_hash")
    primary_hash = final.get("primary", {}).get("locked_common_scales_hash")
    if pre_hash != expected_hash or primary_hash != expected_hash:
        raise RuntimeError(
            f"Q031_LOCKED_SCALE_GATE=FAIL expected={expected_hash} pre={pre_hash} primary={primary_hash}"
        )

    clusters = final.get("primary", {}).get("cluster_diagnostic", {}).get("clusters", [])
    rows: dict[str, dict[str, float]] = {}
    for c in clusters:
        rep = c.get("representative", {}) if isinstance(c, Mapping) else {}
        if not isinstance(rep, Mapping):
            continue
        label = str(rep.get("source_label", ""))
        if label not in EXPECTED_LABELS:
            continue
        if rep.get("status") != "COMPLETE" or rep.get("hillipop_commit") != source_lock["q031"]["hillipop_commit"]:
            raise RuntimeError(f"PARENT_PROVENANCE_GATE=FAIL q031_endpoint={label}")
        minimum = rep.get("minimum", {})
        if not isinstance(minimum, Mapping):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL q031={label}")
        rows[label] = {n: float(minimum[n]) for n in names if n in minimum and finite(minimum[n])}
    if tuple(sorted(rows)) != tuple(sorted(EXPECTED_LABELS)):
        raise RuntimeError(f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL q031_labels={sorted(rows)}")
    if any(set(r) != set(names) for r in rows.values()):
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL q031_missing")
    return rows, scales, final


def descriptors(q022: Mapping[str, Mapping[str, float]],
                q031: Mapping[str, Mapping[str, float]],
                names: Sequence[str], scales: Mapping[str, float],
                labels: Sequence[str]) -> dict[str, Any]:
    matched = {l: metric_rms(q022[l], q031[l], names, scales) for l in labels}
    c22 = {n: statistics.mean(float(q022[l][n]) for l in labels) for n in names}
    c31 = {n: statistics.mean(float(q031[l][n]) for l in labels) for n in names}
    centroid = metric_rms(c22, c31, names, scales)

    q22_pair: dict[tuple[str, str], float] = {}
    q31_pair: dict[tuple[str, str], float] = {}
    drift: dict[tuple[str, str], float] = {}
    for a, b in combinations(labels, 2):
        key = tuple(sorted((a, b)))
        dc = metric_rms(q022[a], q022[b], names, scales)
        dh = metric_rms(q031[a], q031[b], names, scales)
        q22_pair[key] = dc
        q31_pair[key] = dh
        drift[key] = abs(dh - dc)

    threshold = 0.1
    e22 = {k for k, v in q22_pair.items() if v <= threshold}
    e31 = {k for k, v in q31_pair.items() if v <= threshold}
    coord = {}
    for n in names:
        vals = [abs(float(q031[l][n]) - float(q022[l][n])) / float(scales[n]) for l in labels]
        coord[n] = {
            "median_abs_normalized_matched_shift": float(statistics.median(vals)),
            "min_abs_normalized_matched_shift": float(min(vals)),
            "max_abs_normalized_matched_shift": float(max(vals)),
            "count_gt_0_10": int(sum(v > threshold for v in vals)),
        }

    return {
        "matched_endpoint_rms": {k: float(v) for k, v in matched.items()},
        "location_median": float(statistics.median(matched.values())),
        "location_max": float(max(matched.values())),
        "location_exceedance_count_gt_0_10": int(sum(v > threshold for v in matched.values())),
        "normalized_centroid_shift": float(centroid),
        "q022_pairwise_common_rms": {f"{a}|{b}": float(v) for (a, b), v in q22_pair.items()},
        "q031_pairwise_common_rms": {f"{a}|{b}": float(v) for (a, b), v in q31_pair.items()},
        "pairwise_distance_drift": {f"{a}|{b}": float(v) for (a, b), v in drift.items()},
        "shape_median_drift": float(statistics.median(drift.values())),
        "shape_max_drift": float(max(drift.values())),
        "shape_exceedance_count_gt_0_10": int(sum(v > threshold for v in drift.values())),
        "geometry_only_edges_q022": [f"{a}|{b}" for a, b in sorted(e22)],
        "geometry_only_edges_q031": [f"{a}|{b}" for a, b in sorted(e31)],
        "geometry_only_edge_xor_count": int(len(e22 ^ e31)),
        "coordinate_descriptives_secondary_not_decision": coord,
    }


def decision(d: Mapping[str, Any], threshold: float = 0.1) -> dict[str, Any]:
    location = float(d["location_median"]) > threshold
    shape = float(d["shape_median_drift"]) > threshold
    localized = (
        not location and not shape and (
            int(d["location_exceedance_count_gt_0_10"]) > 0
            or int(d["shape_exceedance_count_gt_0_10"]) > 0
        )
    )
    if location or shape:
        classification = "MATERIAL_REPRODUCIBLE_COMMON_GEOMETRY_DIFFERENCE"
        q031_effect = "NARROWED_IMPLEMENTATION_SPECIFIC_NON_PORTABILITY_REHABILITATED"
        stop_case = "A"
    else:
        classification = "NO_MATERIAL_GLOBAL_COMMON_GEOMETRY_DIFFERENCE_ESTABLISHED"
        q031_effect = "PORTABILITY_FAILS_REQUIRES_FURTHER_DOWNGRADE_OR_REPLACEMENT"
        stop_case = "B"
    return {
        "threshold": threshold,
        "location_material": bool(location),
        "shape_material": bool(shape),
        "localized_only": bool(localized),
        "classification": classification,
        "q031_interpretation_effect": q031_effect,
        "q036_stop_case": stop_case,
    }


def replay_q031_pairwise(final: Mapping[str, Any], calculated: Mapping[str, Any]) -> dict[str, Any]:
    stored = final.get("primary", {}).get("cluster_diagnostic", {}).get("pairwise", [])
    smap = {tuple(sorted((str(x["a"]), str(x["b"])))): float(x["common_rms"]) for x in stored}
    cmap = {}
    for k, v in calculated["q031_pairwise_common_rms"].items():
        a, b = k.split("|", 1)
        cmap[tuple(sorted((a, b)))] = float(v)
    if set(smap) != set(cmap):
        return {"pass": False, "reason": "PAIR_KEY_MISMATCH", "stored": len(smap), "calculated": len(cmap)}
    max_abs = max(abs(smap[k] - cmap[k]) for k in smap) if smap else math.inf
    return {"pass": bool(max_abs <= 1e-12), "max_abs_common_rms_difference": float(max_abs), "pairs": len(smap)}


def close_enough(a: Any, b: Any, tol: float = 1e-12) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) <= tol
    return a == b


def run(args: argparse.Namespace) -> dict[str, Any]:
    prereg = read_json(args.preregister)
    lock = read_json(args.source_lock)
    validate_preregister(prereg)
    validate_source_lock(lock)
    names = list(prereg["common_geometry"]["coordinates"])
    labels = list(prereg["endpoint_identity"]["labels"])
    if tuple(labels) != EXPECTED_LABELS:
        raise RuntimeError("NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL preregister_labels")

    q022 = load_q022(args.q022_dir, lock, names)
    q031, scales, final31 = load_q031(args.q031_final, args.q031_preflight, lock, names)
    d = descriptors(q022, q031, names, scales, labels)
    dec = decision(d, float(prereg["common_geometry"]["collapse_scale"]))

    # Mandatory deterministic validation.
    rev = descriptors(q022, q031, names, scales, list(reversed(labels)))
    permutation_pass = all(close_enough(d[k], rev[k]) for k in (
        "location_median", "location_max", "location_exceedance_count_gt_0_10",
        "normalized_centroid_shift", "shape_median_drift", "shape_max_drift",
        "shape_exceedance_count_gt_0_10", "geometry_only_edge_xor_count",
    ))
    ref = replay_q031_pairwise(final31, d)
    replay_dec = decision(d, float(prereg["common_geometry"]["collapse_scale"]))
    finite_pass = all(math.isfinite(float(x)) for x in (
        d["location_median"], d["location_max"], d["normalized_centroid_shift"],
        d["shape_median_drift"], d["shape_max_drift"],
        *d["matched_endpoint_rms"].values(), *d["pairwise_distance_drift"].values(),
    ))

    gates = {
        "Q_IDENTITY_GATE": True,
        "PARENT_PROVENANCE_GATE": True,
        "Q035_BASELINE_PRESERVATION_GATE": bool(
            prereg["rules"]["q035_closed"]
            and lock["q035"]["status"] == "AUTHORITATIVE_CLOSED_CLASSIFIER_HARMONIZATION"
            and prereg["rules"]["no_stable_label_only_decision"]
        ),
        "NINE_BY_NINE_LABEL_IDENTITY_GATE": set(q022) == set(q031) == set(labels),
        "COMMON_COORDINATE_GATE": all(set(x) == set(names) for x in (*q022.values(), *q031.values())),
        "Q031_LOCKED_SCALE_GATE": True,
        "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE": prereg["common_geometry"]["objective_values_used_in_q036_decision"] is False,
        "FINITE_RESULT_GATE": bool(finite_pass),
        "PERMUTATION_INVARIANCE_GATE": bool(permutation_pass),
        "REFERENCE_REPLAY_GATE": bool(ref["pass"]),
        "DECISION_REPLAY_GATE": dec == replay_dec,
    }
    mandatory = list(prereg["mandatory_gates"])
    missing = [g for g in mandatory if not gates.get(g, False)]
    final_gate = "PASS" if not missing else "FAIL"
    if final_gate != "PASS":
        classification = "INCONCLUSIVE"
        stop_case = "C"
    else:
        classification = dec["classification"]
        stop_case = dec["q036_stop_case"]

    out = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN,
        "result_id": RESULT,
        "source_type": "BUBBLEVERSE_INTERNAL_ARTIFACT_COMPUTATION",
        "execution_status": "COMPLETE",
        "tests_status": "COMPLETE",
        "FINAL_RESULT_GATE": final_gate,
        "final_result_status": "PASS" if final_gate == "PASS" else "UNRESOLVED",
        "q036_stop_case": stop_case,
        "final_classification": classification,
        "decision": dec,
        "common_geometry": {
            "coordinates": names,
            "locked_scales": scales,
            "locked_scales_hash": lock["q031"]["locked_scales_hash"],
            "materiality_threshold": float(prereg["common_geometry"]["collapse_scale"]),
            "objective_values_used": False,
        },
        "descriptors": d,
        "gates": gates,
        "reference_replay": ref,
        "mandatory_gate_failures": missing,
        "claim_boundaries": {
            "q035_classifier_harmonization_remains_authoritative": True,
            "stable_nonstable_label_is_not_decision_basis": True,
            "cross_likelihood_absolute_chi2_compared": False,
            "cross_likelihood_objectives_summed": False,
            "camspec_hillipop_are_independent_observations": False,
            "physical_planck_systematic_established": False,
            "ede_favored_or_falsified_by_q036": False,
        },
        "journal_effect": {
            "KEEP": [
                "Q035 classifier-harmonization result and removal of the old stable-vs-non-stable discrepancy.",
                "Q022 and Q031 raw endpoint results and provenance.",
                "MOD-EDE-N3 status remains active/constrained/not established new physics."
            ],
            "UPDATE": [
                "CASE-031 negative portability cannot be justified by stable-basin labels alone.",
                "CASE-031 is rehabilitated only in a narrowed sense if Q036 continuous common-geometry materiality gates pass."
            ],
            "ADD": [
                "Q036 continuous matched-location and pairwise-shape comparison under exact Q031 locked common geometry."
            ],
            "UNRESOLVED": [
                "Which implementation-level likelihood ingredients cause the common-geometry displacement.",
                "Whether the displacement maps to a physical Planck systematic or changes external cosmological viability."
            ]
        },
        "next_required_action": "RETURN_TO_RESULT_INGESTION_AND_ROUTING_ENGINE",
        "return_route": "RESULT INGESTION & ROUTING ENGINE",
        "provenance": {
            "preregister_sha256": sha256_file(args.preregister),
            "source_lock_sha256": sha256_file(args.source_lock),
            "q022_run_id": lock["q022"]["run_id"],
            "q031_run_id": lock["q031"]["run_id"],
            "q022_commit": lock["q022"]["execution_commit"],
            "q031_commit": lock["q031"]["execution_commit"],
            "hillipop_commit": lock["q031"]["hillipop_commit"],
            "backend_commit": lock["model"]["backend_commit"],
        },
    }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--q031-final", required=True)
    ap.add_argument("--q031-preflight", required=True)
    ap.add_argument("--preregister", default="q036_endpoint_geometry_preregister_v1.json")
    ap.add_argument("--source-lock", default="q036_endpoint_geometry_source_lock_v1.json")
    ap.add_argument("--output", default="q036_final_v1.json")
    args = ap.parse_args()
    try:
        out = run(args)
    except Exception as e:
        fail = {
            "q": Q, "program_id": PROGRAM_ID, "run_id": RUN, "result_id": RESULT,
            "execution_status": "FAIL", "FINAL_RESULT_GATE": "FAIL",
            "final_classification": "INCONCLUSIVE", "error": repr(e),
        }
        write_json(args.output, fail)
        print(json.dumps(fail, indent=2, sort_keys=True))
        return 2
    write_json(args.output, out)
    print(json.dumps({
        "q": out["q"], "program_id": out["program_id"],
        "FINAL_RESULT_GATE": out["FINAL_RESULT_GATE"],
        "q036_stop_case": out["q036_stop_case"],
        "final_classification": out["final_classification"],
        "location_median": out["descriptors"]["location_median"],
        "shape_median_drift": out["descriptors"]["shape_median_drift"],
    }, indent=2, sort_keys=True))
    return 0 if out["FINAL_RESULT_GATE"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
