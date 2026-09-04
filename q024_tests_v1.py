#!/usr/bin/env python3
"""Mandatory validator for Bubbleverse Q024 V1."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

Q = "Q024"
RUN = "Q024-FULLMF-PERMUTATION-SIGN-INVARIANT-MATCHING-V1"
RESULT = "R-Q024-EDE-FULLMF-BASIN-MATCHING-001"


def write(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(t, p)


def finite(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--result", required=True)
    a.add_argument("--output", required=True)
    x = a.parse_args()
    r = json.loads(Path(x.result).read_text(encoding="utf-8"))

    best = r.get("best_candidate", {})
    edge_tests = best.get("edge_tests", {})
    baseline = r.get("combinatorial_baseline", {})
    interp = r.get("interpretation", {})

    tests = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE":
            r.get("run_id") == RUN and r.get("result_id") == RESULT,
        "MODEL_FREEZE_GATE":
            r.get("model", {}).get("name") == "MOD-EDE-N3"
            and r.get("model", {}).get("n_scf") == 3
            and r.get("model", {}).get("backend_commit")
            == "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "ZERO_NEW_LIKELIHOOD_GATE":
            r.get("actual_new_likelihood_evaluations") == 0,
        "MASK_SCOPE_GATE": r.get("selected_masks") == [3, 6, 7],
        "SEED_FAMILY_SCOPE_GATE": r.get("seed_families") == [0, 1, 2],
        "THIRTY_SIX_PERMUTATION_GATE":
            r.get("matching_definition", {}).get("joint_candidates_tested") == 36,
        "SIGN_INVARIANCE_GATE":
            r.get("matching_definition", {}).get("direction_sign_invariant") is True,
        "THREE_EDGE_GATE": sorted(edge_tests) == ["0-1", "0-2", "1-2"],
        "FINITE_BEST_SCORE_GATE":
            finite(best.get("global_median_abs_cosine"))
            and finite(best.get("min_edge_median_abs_cosine")),
        "COMBINATORIAL_BASELINE_GATE":
            baseline.get("candidate_count") == 36
            and finite(baseline.get("median_global_median_abs_cosine"))
            and finite(baseline.get("best_minus_permutation_median")),
        "OBJECTIVE_NOT_IDENTITY_GATE":
            r.get("matching_definition", {}).get(
                "objective_difference_used_for_identity"
            ) is False,
        "Q023_FIXED_DEFINITION_PRESERVED_GATE":
            interp.get("q023_fixed_seed_definition_preserved") is True
            and interp.get("q023_was_wrong") is False,
        "Q021_NOT_REOPENED_GATE":
            interp.get("q021_distributed_result_reopened") is False,
        "Q022_NOT_REOPENED_GATE":
            interp.get("q022_multibasin_result_reopened") is False,
        "NO_PHYSICAL_OVERCLAIM_GATE":
            interp.get("direction_similarity_is_physical_causation") is False
            and interp.get("foreground_movement_is_systematic_evidence") is False
            and interp.get("calibration_movement_is_failure_evidence") is False
            and interp.get("stable_optimizer_basin_is_distinct_universe") is False,
        "INTERNAL_GATE_SET_PASS":
            all(bool(v) for v in r.get("gates", {}).values()),
    }

    ok = all(tests.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q024_MANDATORY_TESTS",
        "gates": tests,
        "FINAL_RESULT_GATE": "PASS" if ok else "FAIL",
    }
    write(x.output, out)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
