#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

Q = "Q028"
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V4"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-004"


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
    b = r.get("criterion_b_plus", {})
    diag = b.get("diagnostics_by_recipient_precision_mask", {})
    common = r.get("common_support", {})
    resolution = r.get("resolution_class")

    expected_case_keys = {
        f"residual_mask_{rmask}:e{a}{b}"
        for rmask in (3, 6, 7)
        for a, b in ((0, 1), (0, 2), (1, 2))
    }

    criterion_complete = (
        set(diag) == {"3", "6", "7"}
        and all(
            int(v.get("donor_case_count", -1)) == 9
            and set(v.get("donor_cases", {})) == expected_case_keys
            and all(
                finite(case.get("edge_choice_spread"))
                and finite(case.get("tolerance"))
                and isinstance(case.get("criterion_b_plus_case_pass"), bool)
                and set(case.get("interaction_by_precision_candidate_edge", {}))
                == {"e01", "e02", "e12"}
                and all(
                    finite(x)
                    for x in case.get(
                        "interaction_by_precision_candidate_edge", {}
                    ).values()
                )
                for case in v.get("donor_cases", {}).values()
            )
            for v in diag.values()
        )
    )

    identified_map = b.get("identified_by_mask", {})
    bplus_consistent = (
        set(identified_map) == {"3", "6", "7"}
        and isinstance(b.get("gate"), bool)
        and b.get("gate") == all(bool(identified_map[str(m)]) for m in (3, 6, 7))
    )

    common_valid = (
        common.get("construction")
        == "LABEL_INTERSECTION_PLUS_SCHUR_COMPLEMENT_MARGINAL_PRECISION"
        and int(common.get("dimension", 0)) > 0
        and common.get("principal_precision_submatrix_used_as_marginal") is False
        and set(common.get("candidate_precision_metadata_by_mask_and_edge", {}))
        == {"3", "6", "7"}
        and all(
            set(per_mask) == {"e01", "e02", "e12"}
            and all(
                meta.get("method")
                in {
                    "IDENTICAL_SUPPORT_FULL_PRECISION",
                    "SCHUR_COMPLEMENT_MARGINAL_FROM_FULL_PRECISION",
                }
                and finite(meta.get("common_fraction"))
                and float(meta.get("common_fraction")) > 0
                and meta.get("raw_antisymmetry_scientific_gate") is False
                and meta.get("symmetrization") == "P_sym = 0.5 * (P_raw + P_raw.T)"
                and finite(meta.get("raw_max_abs_antisymmetry"))
                and finite(meta.get("raw_relative_antisymmetry"))
                and isinstance(meta.get("raw_precision_sha256"), str)
                and isinstance(meta.get("symmetrized_full_precision_sha256"), str)
                for meta in per_mask.values()
            )
            for per_mask in common.get(
                "candidate_precision_metadata_by_mask_and_edge", {}
            ).values()
        )
    )

    valid_negative = (
        resolution == "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY"
        and (
            b.get("gate") is False
            or common.get("interpretability_gate") is False
        )
        and r.get("stop_condition_reached") is True
    )

    shapley = r.get("shapley_rows", [])
    valid_positive = (
        resolution == "VALID_COMMON_SUPPORT_SEPARATION"
        and b.get("gate") is True
        and common.get("interpretability_gate") is True
        and set(r.get("counterfactual", {})) == {"e01", "e02", "e12"}
        and len(shapley) == 9
        and all(
            finite(x.get("observed_diagonal_contrast"))
            and finite(x.get("residual_side_shapley"))
            and finite(x.get("precision_side_shapley"))
            and finite(x.get("closure_error"))
            for x in shapley
        )
        and r.get("shapley_closure_gate") is True
        and r.get("stop_condition_reached") is True
    )

    claim = r.get("claim_boundaries", {})
    gates = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE": (
            r.get("run_id") == RUN and r.get("result_id") == RESULT
        ),
        "FIXED_VECTOR_COUNT_GATE": (
            int(r.get("actual_new_likelihood_evaluations", -1)) == 36
        ),
        "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations", -1)) == 0,
        "NO_SAMPLING_GATE": int(r.get("sampling_evaluations", -1)) == 0,
        "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated", -1)) == 0,
        "STATE_LEVEL_INVARIANCE_NOT_REQUIRED_GATE": (
            r.get("state_level_invariance_required") is False
        ),
        "CRITERION_B_PLUS_COMPLETENESS_GATE": criterion_complete,
        "CRITERION_B_PLUS_CONSISTENCY_GATE": bplus_consistent,
        "COMMON_SUPPORT_MATHEMATICAL_VALIDITY_GATE": common_valid,
        "PRECISION_SYMMETRIZATION_PROVENANCE_GATE": all(
            meta.get("raw_antisymmetry_scientific_gate") is False
            and meta.get("symmetrization") == "P_sym = 0.5 * (P_raw + P_raw.T)"
            and finite(meta.get("raw_relative_antisymmetry"))
            for per_mask in common.get(
                "candidate_precision_metadata_by_mask_and_edge", {}
            ).values()
            for meta in per_mask.values()
        ),
        "VALID_RESOLUTION_GATE": valid_negative or valid_positive,
        "SHAPLEY_CLOSURE_OR_VALID_NEGATIVE_STOP_GATE": (
            valid_negative or r.get("shapley_closure_gate") is True
        ),
        "PARENT_PRESERVATION_GATE": all(
            r.get("journal_preservation", {}).values()
        ),
        "NO_CAUSAL_OVERCLAIM_GATE": (
            claim.get("physical_causality_claimed") is False
            and claim.get("calibration_failure_proven") is False
            and claim.get("instrumental_systematic_proven") is False
            and claim.get("foreground_systematic_proven") is False
            and claim.get("npipe_maps_incorrect_proven") is False
            and claim.get("covariance_construction_incorrect_proven") is False
            and claim.get("omega_cdm_A_planck_physical_causality_proven") is False
            and claim.get("new_physics_proven") is False
        ),
    }

    ok = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q028_V4_CRITERION_B_PLUS_MANDATORY_TESTS",
        "gates": gates,
        "tests_status": "COMPLETE",
        "FINAL_RESULT_GATE": "PASS" if ok else "FAIL",
    }
    Path(a.output).write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
