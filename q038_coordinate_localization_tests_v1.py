#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

Q = "Q-038"
PROGRAM_ID = "Q038-COORDLOC-V1"
RESULT_ID = "R-Q038-EDE-COORDINATE-LOCALIZATION-001"
COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
SCALES = {
    "omega_b": 3.644915744246274e-05,
    "omega_cdm": 2.9761589951235456e-04,
    "fEDE": 1.0851930861718734e-03,
    "log10z_c": 3.666125981785351e-02,
    "thetai_scf": 1.2826810796868315e-02,
    "H0": 2.253286448991929e-01,
    "A_planck": 3.7111561222435974e-04,
}
FULL_CAPTURE_THRESHOLD = 0.80
LOO_CAPTURE_THRESHOLD = 0.70
LOO_REQUIRED = 8
CONCENTRATED_MAX_SUBSET_SIZE = 2
TOL = 1e-12

MANDATORY_GATES = (
    "Q_IDENTITY_GATE",
    "JOURNAL_CONTINUITY_GATE",
    "PARENT_Q037_PROVENANCE_GATE",
    "PARENT_Q032_PROVENANCE_GATE",
    "Q037_RAW_INPUT_GATE",
    "NINE_BY_NINE_LABEL_IDENTITY_GATE",
    "COMMON_COORDINATE_GATE",
    "Q031_LOCKED_SCALE_GATE",
    "MATERIALITY_THRESHOLD_GATE",
    "CONCENTRATION_PREREGISTRATION_GATE",
    "SYMMETRIC_SUBSET_GATE",
    "EXACT_COMMON_SUPPORT_IDENTITY_GATE",
    "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE",
    "Q037_NUMERICAL_REPLAY_GATE",
    "PAIRWISE_EXACT_DECOMPOSITION_GATE",
    "FINITE_RESULT_GATE",
    "CLASSIFICATION_GATE",
    "Q035_CLOSED_PRESERVATION_GATE",
    "Q036_CLOSED_PRESERVATION_GATE",
    "Q037_CLOSED_PRESERVATION_GATE",
    "NO_CAUSAL_ATTRIBUTION_GATE",
)


def load(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError("JSON_OBJECT_GATE=FAIL")
    return obj


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(float(a) - float(b)) <= tol


def metric(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    z = [(float(a[c]) - float(b[c])) / SCALES[c] for c in COORDS]
    return math.sqrt(sum(v * v for v in z) / len(COORDS))


def capture(share: Mapping[str, float], subset: Sequence[str]) -> float:
    return sum(float(share[c]) for c in subset)


def replay_q037(raw: Mapping[str, Any]) -> dict[str, Any]:
    rows = raw["raw_endpoint_vectors"]
    matched = {l: metric(rows["camspec"][l], rows["hillipop"][l]) for l in LABELS}
    cc = {c: sum(rows["camspec"][l][c] for l in LABELS) / len(LABELS) for c in COORDS}
    hc = {c: sum(rows["hillipop"][l][c] for l in LABELS) / len(LABELS) for c in COORDS}
    drifts = {}
    for a, b in itertools.combinations(LABELS, 2):
        dc = metric(rows["camspec"][a], rows["camspec"][b])
        dh = metric(rows["hillipop"][a], rows["hillipop"][b])
        drifts[f"{a}|{b}"] = abs(dh - dc)
    import statistics
    return {
        "matched_median_displacement": statistics.median(matched.values()),
        "matched_max_displacement": max(matched.values()),
        "matched_exceedance_count_gt_0_10": sum(v > 0.10 for v in matched.values()),
        "normalized_centroid_displacement": metric(cc, hc),
        "pairwise_median_drift": statistics.median(drifts.values()),
        "pairwise_max_drift": max(drifts.values()),
        "pairwise_exceedance_count_gt_0_10": sum(v > 0.10 for v in drifts.values()),
    }


def recompute_minimal_subset(raw: Mapping[str, Any]) -> tuple[int, list[list[str]]]:
    sa = raw["subset_analysis"]
    qualifying = [r for r in sa["all_subsets"] if r["qualifies"]]
    min_size = min(r["size"] for r in qualifying)
    mins = [r["subset"] for r in qualifying if r["size"] == min_size]
    return min_size, mins


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("--raw", required=True)
    ap.add_argument("--output", default="q038_tests_v1.json")
    args = ap.parse_args()

    result = load(args.result)
    raw = load(args.raw)
    tests: dict[str, bool] = {}

    tests["IDENTITY"] = (
        result.get("q") == Q
        and result.get("program_id") == PROGRAM_ID
        and result.get("result_id") == RESULT_ID
        and raw.get("q") == Q
        and raw.get("program_id") == PROGRAM_ID
        and raw.get("result_id") == RESULT_ID
    )
    tests["FINAL_RESULT_COMPLETE"] = (
        result.get("execution_status") == "COMPLETE"
        and result.get("actual_computed_result") is True
        and result.get("FINAL_RESULT_GATE") == "PASS"
    )
    gates = result.get("gates", {})
    tests["MANDATORY_GATES"] = all(gates.get(g) is True for g in MANDATORY_GATES)

    rows = raw.get("raw_endpoint_vectors", {})
    tests["NINE_BY_NINE"] = (
        set(rows) == {"camspec", "hillipop"}
        and all(set(rows[x]) == set(LABELS) for x in ("camspec", "hillipop"))
    )
    tests["SEVEN_COORDS"] = all(
        set(rows[impl][label]) == set(COORDS)
        for impl in ("camspec", "hillipop")
        for label in LABELS
    )

    replay = replay_q037(raw)
    reported_replay = result["q037_replay"]["actual"]
    replay_diffs = [abs(float(replay[k]) - float(reported_replay[k])) for k in replay]
    tests["Q037_REFERENCE_REPLAY"] = max(replay_diffs) <= TOL
    tests["Q037_AUTHORITATIVE_BENCHMARK"] = float(result["q037_replay"]["max_absolute_difference"]) <= TOL

    shares = result["coordinate_shares"]
    tests["SHARE_NORMALIZATION"] = all(
        close(sum(float(v) for v in shares[channel].values()), 1.0)
        and set(shares[channel]) == set(COORDS)
        for channel in ("matched_location", "centroid", "pairwise_shape")
    )

    pairwise = raw["pairwise_shape_decomposition"]
    residuals = [float(v["exact_additivity_residual"]) for v in pairwise["edges"].values()]
    tests["PAIRWISE_36"] = len(pairwise["edges"]) == 36
    tests["PAIRWISE_EXACT_ADDITIVITY"] = max(residuals) <= TOL and float(pairwise["max_exact_additivity_residual"]) <= TOL

    sa = raw["subset_analysis"]
    tests["ALL_127_SUBSETS"] = len(sa["all_subsets"]) == 127
    subset_keys = {tuple(r["subset"]) for r in sa["all_subsets"]}
    expected_keys = {
        subset
        for size in range(1, len(COORDS) + 1)
        for subset in itertools.combinations(COORDS, size)
    }
    tests["SUBSET_UNIVERSE_EXACT"] = subset_keys == expected_keys

    all_row = next(r for r in sa["all_subsets"] if tuple(r["subset"]) == COORDS)
    tests["ALL_COORDINATE_SUBSET_QUALIFIES"] = (
        all_row["qualifies"] is True
        and all(close(v, 1.0) for v in all_row["full_capture"].values())
        and all(v == 9 for v in all_row["leave_one_label_out_pass_counts"].values())
    )

    min_size, mins = recompute_minimal_subset(raw)
    tests["MINIMAL_SUBSET_REPLAY"] = (
        min_size == int(result["minimal_qualifying_subset_size"])
        and sorted(mins) == sorted(result["minimal_qualifying_subsets"])
    )
    expected_class = "CONCENTRATED" if min_size <= CONCENTRATED_MAX_SUBSET_SIZE else "DISTRIBUTED"
    tests["DECISION_REPLAY"] = (
        result.get("q038_stop_case") == expected_class
        and result.get("final_classification") == expected_class
        and sa.get("classification") == expected_class
    )

    # Independently re-check the preregistered qualification rule for every subset.
    qualification_replay = True
    for row in sa["all_subsets"]:
        expected = (
            all(float(v) >= FULL_CAPTURE_THRESHOLD for v in row["full_capture"].values())
            and all(int(v) >= LOO_REQUIRED for v in row["leave_one_label_out_pass_counts"].values())
        )
        qualification_replay &= bool(row["qualifies"]) == expected
        for omitted, vals in row["leave_one_label_out_capture"].items():
            if omitted not in LABELS:
                qualification_replay = False
            if any(not math.isfinite(float(v)) for v in vals.values()):
                qualification_replay = False
    tests["QUALIFICATION_RULE_REPLAY"] = qualification_replay

    cb = result.get("claim_boundaries", {})
    tests["Q035_Q036_Q037_CLOSED"] = (
        cb.get("q035_remains_authoritative_closed") is True
        and cb.get("q036_remains_closed") is True
        and cb.get("q037_remains_closed") is True
    )
    tests["NO_OBJECTIVE_CROSS_COMPARE"] = cb.get("cross_likelihood_objectives_used") is False
    tests["NOT_INDEPENDENT_OBSERVATIONS"] = cb.get("camspec_hillipop_are_independent_observations") is False
    tests["NO_CAUSAL_OVERCLAIM"] = cb.get("coordinate_localization_is_causal_attribution") is False
    tests["NO_H0_CHANGE"] = cb.get("h0_changed") is False

    status = "PASS" if all(tests.values()) else "FAIL"
    out = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "test_id": "Q038-RESULT-TESTS-V1",
        "status": status,
        "tests": tests,
        "replay_max_absolute_difference": max(replay_diffs),
        "minimal_qualifying_subset_size": min_size,
        "classification": expected_class,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
