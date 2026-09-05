#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


Q = "Q028"
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V8"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-008"
VALID_RESOLUTIONS = {
    "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
    "VALID_COMMON_SUPPORT_SEPARATION",
}


def finite(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    r = json.loads(Path(a.result).read_text(encoding="utf-8"))

    bplus = r.get("criterion_b_plus", {})
    common = r.get("common_support", {})
    arch = r.get("execution_architecture", {})
    claim = r.get("claim_boundaries", {})
    journal = r.get("journal_preservation", {})

    diag = bplus.get("diagnostics_by_recipient_precision_mask", {})
    complete_bplus_domain = (
        set(diag) == {"3", "6", "7"}
        and all(int(diag[m].get("donor_case_count", -1)) == 9 for m in diag)
    )

    gates = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE": (
            r.get("run_id") == RUN and r.get("result_id") == RESULT
        ),
        "FIXED_VECTOR_COUNT_GATE": (
            int(r.get("actual_new_likelihood_evaluations", -1)) == 36
        ),
        "FAMILY_CHECKPOINT_COUNT_GATE": int(r.get("family_checkpoint_jobs", -1)) == 9,
        "PRECISION_JOB_COUNT_GATE": int(r.get("precision_functional_jobs", -1)) == 9,
        "PRECISION_NO_EXTRA_LIKELIHOOD_GATE": (
            int(r.get("precision_model_constructions_without_likelihood_evaluation", -1)) == 9
        ),
        "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations", -1)) == 0,
        "NO_SAMPLING_GATE": int(r.get("sampling_evaluations", -1)) == 0,
        "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated", -1)) == 0,
        "STATE_LEVEL_INVARIANCE_NOT_REQUIRED_GATE": (
            r.get("state_level_invariance_required") is False
        ),
        "CRITERION_B_PLUS_COMPLETENESS_GATE": complete_bplus_domain,
        "FROZEN_TOLERANCE_GATE": float(bplus.get("tolerance", -1)) == 2.0e-4,
        "COMMON_SUPPORT_MATHEMATICAL_VALIDITY_GATE": (
            common.get("principal_precision_submatrix_used_as_marginal") is False
            and common.get("materialized_common_precision") is False
            and int(common.get("dimension", 0)) > 0
            and finite(common.get("minimum_common_support_fraction"))
        ),
        "SPLIT_ARCHITECTURE_GATE": (
            arch.get("version") == "V8_SPLIT_CHECKPOINTED"
            and arch.get("dense_precision_artifacts_serialized") is False
            and arch.get("dense_common_precision_materialized") is False
            and arch.get("family_jobs_restartable_independently") is True
            and arch.get("precision_jobs_restartable_independently") is True
        ),
        "VALID_RESOLUTION_GATE": r.get("resolution_class") in VALID_RESOLUTIONS,
        "PARENT_PRESERVATION_GATE": all(
            journal.get(k) is True
            for k in (
                "q019_preserved",
                "q022_authoritative_endpoints_preserved",
                "q024_preserved_no_rerun",
                "q025_v2_preserved",
                "q026_preserved",
                "q027_preserved",
                "q028_v3_has_no_scientific_result",
                "q028_v4_has_no_scientific_result",
                "q028_v5_has_no_scientific_result",
                "q028_v6_has_no_scientific_result",
                "q028_v7_has_no_final_scientific_result",
            )
        ),
        "NO_CAUSAL_OVERCLAIM_GATE": all(v is False for v in claim.values()),
    }

    if r.get("resolution_class") == "VALID_COMMON_SUPPORT_SEPARATION":
        rows = r.get("shapley_rows", [])
        gates["SHAPLEY_CLOSURE_OR_VALID_NEGATIVE_STOP_GATE"] = (
            r.get("shapley_closure_gate") is True
            and len(rows) == 9
            and all(abs(float(x["closure_error"])) <= 1.0e-8 for x in rows)
        )
        gates["CRITERION_B_PLUS_CONSISTENCY_GATE"] = bplus.get("gate") is True
    else:
        gates["SHAPLEY_CLOSURE_OR_VALID_NEGATIVE_STOP_GATE"] = (
            r.get("shapley_closure_gate") == "NOT_REACHED_VALID_NEGATIVE_STOP"
            and r.get("shapley_rows") == []
        )
        # Either B+ fails, or common-support fraction fails after B+ passed.
        gates["CRITERION_B_PLUS_CONSISTENCY_GATE"] = (
            bplus.get("gate") is False
            or common.get("interpretability_gate") is False
        )

    final = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "test_suite": "Q028_V8_SPLIT_CHECKPOINTED_CRITERION_B_PLUS_MANDATORY_TESTS",
        "gates": gates,
        "FINAL_RESULT_GATE": "PASS" if final else "FAIL",
    }
    Path(a.output).write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if final else 1


if __name__ == "__main__":
    raise SystemExit(main())
