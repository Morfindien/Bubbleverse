#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping

Q = "Q-037"
PROGRAM = "Q037-TTGEOM-V1"
RESULT = "R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001"
COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
SCALES = {
    "omega_b": 3.644915744246274e-05,
    "omega_cdm": 2.9761589951235456e-04,
    "fEDE": 1.0851930861718734e-03,
    "log10z_c": 3.666125981785351e-02,
    "thetai_scf": 1.2826810796868315e-02,
    "H0": 2.253286448991929e-01,
    "A_planck": 3.7111561222435974e-04,
}
THRESHOLD = 0.10
LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
MANDATORY_GATES = (
    "Q_IDENTITY_GATE",
    "PARENT_Q032_PROVENANCE_GATE",
    "SOURCE_ARTIFACT_DIGEST_GATE",
    "Q035_BASELINE_PRESERVATION_GATE",
    "Q036_CLOSED_PRESERVATION_GATE",
    "NINE_BY_NINE_LABEL_IDENTITY_GATE",
    "COMMON_COORDINATE_GATE",
    "Q031_LOCKED_SCALE_GATE",
    "MATERIALITY_THRESHOLD_GATE",
    "EXACT_COMMON_SUPPORT_IDENTITY_GATE",
    "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE",
    "FINITE_RESULT_GATE",
    "PERMUTATION_INVARIANCE_GATE",
)


def metric(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    vals = [(float(a[c]) - float(b[c])) / SCALES[c] for c in COORDS]
    return math.sqrt(sum(v * v for v in vals) / len(vals))


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(float(a) - float(b)) <= tol


def replay(d: Mapping[str, Any]) -> tuple[bool, float]:
    rows = d["raw_endpoint_vectors"]
    desc = d["descriptors"]
    diffs = []

    matched = {l: metric(rows["camspec"][l], rows["hillipop"][l]) for l in LABELS}
    for l in LABELS:
        diffs.append(abs(matched[l] - float(desc["matched_endpoint_rms"][l])))
    diffs.append(abs(statistics.median(matched.values()) - float(desc["matched_median_displacement"])))

    cc = {c: statistics.mean(rows["camspec"][l][c] for l in LABELS) for c in COORDS}
    hc = {c: statistics.mean(rows["hillipop"][l][c] for l in LABELS) for c in COORDS}
    diffs.append(abs(metric(cc, hc) - float(desc["normalized_centroid_displacement"])))

    drifts = {}
    for a, b in combinations(LABELS, 2):
        key = f"{a}|{b}"
        dc = metric(rows["camspec"][a], rows["camspec"][b])
        dh = metric(rows["hillipop"][a], rows["hillipop"][b])
        drift = abs(dh - dc)
        diffs.extend([
            abs(dc - float(desc["camspec_internal_pairwise_distances"][key])),
            abs(dh - float(desc["hillipop_internal_pairwise_distances"][key])),
            abs(drift - float(desc["absolute_pairwise_distance_drifts"][key])),
        ])
        drifts[key] = drift
    diffs.append(abs(statistics.median(drifts.values()) - float(desc["pairwise_median_drift"])))
    diffs.append(abs(max(drifts.values()) - float(desc["pairwise_max_drift"])))
    maxdiff = max(diffs) if diffs else math.inf
    return maxdiff <= 1e-12, maxdiff


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("--output", default="q037_tests_v1.json")
    args = ap.parse_args()
    d = json.loads(Path(args.result).read_text(encoding="utf-8"))

    tests: dict[str, bool] = {}
    tests["IDENTITY"] = d.get("q") == Q and d.get("program_id") == PROGRAM and d.get("result_id") == RESULT
    tests["FINAL_RESULT_COMPLETE"] = d.get("execution_status") == "COMPLETE" and d.get("actual_computed_result") is True
    gates = d.get("gates", {})
    tests["MANDATORY_GATES"] = all(gates.get(g) is True for g in MANDATORY_GATES)
    tests["NINE_MATCHED"] = len(d.get("descriptors", {}).get("matched_endpoint_rms", {})) == 9
    tests["PAIRWISE_36_36_36"] = all(
        len(d.get("descriptors", {}).get(k, {})) == 36
        for k in (
            "camspec_internal_pairwise_distances",
            "hillipop_internal_pairwise_distances",
            "absolute_pairwise_distance_drifts",
        )
    )
    tests["NO_OBJECTIVE_CROSS_COMPARE"] = d.get("common_geometry", {}).get("objective_values_used") is False
    tests["Q035_PRESERVED"] = d.get("claim_boundaries", {}).get("q035_classifier_harmonization_remains_authoritative") is True
    tests["Q036_CLOSED"] = d.get("claim_boundaries", {}).get("q036_remains_closed") is True
    tests["NOT_INDEPENDENT_OBSERVATIONS"] = d.get("claim_boundaries", {}).get("camspec_hillipop_are_independent_observations") is False
    tests["NO_CAUSAL_OVERCLAIM"] = d.get("claim_boundaries", {}).get("causal_component_attribution_performed") is False

    replay_ok, maxdiff = replay(d)
    tests["REFERENCE_REPLAY"] = replay_ok

    desc = d["descriptors"]
    location = float(desc["matched_median_displacement"]) > THRESHOLD or float(desc["normalized_centroid_displacement"]) > THRESHOLD
    shape = float(desc["pairwise_median_drift"]) > THRESHOLD
    expected_case = "A" if (location or shape) else "B"
    expected_class = (
        "COMMON_SUPPORT_DOES_NOT_REMOVE_IMPLEMENTATION_GEOMETRY_DIFFERENCE"
        if expected_case == "A"
        else "INFORMATION_SUPPORT_RESTRICTION_MATERIALLY_EXPLAINS_OR_LOCALIZES_Q036_DIFFERENCE"
    )
    tests["DECISION_REPLAY"] = d.get("q037_stop_case") == expected_case and d.get("final_classification") == expected_class
    tests["FINAL_GATE"] = d.get("FINAL_RESULT_GATE") == "PASS"

    status = "PASS" if all(tests.values()) else "FAIL"
    out = {
        "q": Q,
        "program_id": PROGRAM,
        "test_id": "Q037-RESULT-TESTS-V1",
        "status": status,
        "max_absolute_replay_difference": maxdiff,
        "tests": tests,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
