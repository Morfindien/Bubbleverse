#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

Q = "Q028"
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V1"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-001"

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

    negative_identifiability = (
        r.get("scientific_classification")
        == "NON_IDENTIFIABLE_AS_MASK_SPECIFIC_PRECISION_OPERATOR_WITH_CURRENT_VALID_DECOMPOSITION"
    )
    common = r.get("common_support", {})
    shapley = r.get("shapley_rows", [])

    if negative_identifiability:
        scientific_core = (
            r.get("common_support_gate") == "NOT_REACHED"
            and any(v is False for v in r.get("precision_invariance_across_edges_by_mask", {}).values())
        )
        counterfactual_complete = True  # legitimately not run after decisive feasibility failure
        closure = True
    else:
        scientific_core = (
            common.get("construction") == "LABEL_INTERSECTION_PLUS_SCHUR_COMPLEMENT_MARGINAL_PRECISION"
            and int(common.get("dimension", 0)) > 0
            and common.get("principal_precision_submatrix_used_as_marginal") is False
            and all(
                x.get("method") in {
                    "IDENTICAL_SUPPORT_FULL_PRECISION",
                    "SCHUR_COMPLEMENT_MARGINAL_FROM_FULL_PRECISION",
                }
                and finite(x.get("common_fraction"))
                and float(x.get("common_fraction")) > 0
                for x in common.get("mask_metadata", {}).values()
            )
        )
        counterfactual_complete = (
            set(r.get("counterfactual", {})) == {"e01", "e02", "e12"}
            and len(shapley) == 9
            and all(
                finite(x.get("observed_diagonal_contrast"))
                and finite(x.get("residual_side_shapley"))
                and finite(x.get("precision_side_shapley"))
                for x in shapley
            )
        )
        closure = r.get("shapley_closure_gate") is True

    gates = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE": r.get("run_id") == RUN and r.get("result_id") == RESULT,
        "FIXED_VECTOR_COUNT_GATE": int(r.get("actual_new_likelihood_evaluations", -1)) == 36,
        "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations", -1)) == 0,
        "NO_SAMPLING_GATE": int(r.get("sampling_evaluations", -1)) == 0,
        "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated", -1)) == 0,
        "COMMON_SUPPORT_MATHEMATICAL_VALIDITY_GATE": scientific_core,
        "COUNTERFACTUAL_COMPLETENESS_OR_VALID_NEGATIVE_STOP_GATE": counterfactual_complete,
        "SHAPLEY_CLOSURE_OR_VALID_NEGATIVE_STOP_GATE": closure,
        "PARENT_PRESERVATION_GATE": all(r.get("journal_preservation", {}).values()),
        "NO_CAUSAL_OVERCLAIM_GATE": (
            r.get("claim_boundaries", {}).get("physical_causality_claimed") is False
            and r.get("claim_boundaries", {}).get("calibration_failure_proven") is False
            and r.get("claim_boundaries", {}).get("instrumental_systematic_proven") is False
            and r.get("claim_boundaries", {}).get("new_physics_proven") is False
        ),
        "INTERPRETATION_BOUNDARY_GATE": (
            negative_identifiability
            or r.get("interpretation", {}).get("residual_side_definition", "").startswith("DATA_MINUS_MODEL_RESIDUAL_FAMILY")
        ),
    }

    ok = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q028_MANDATORY_TESTS",
        "gates": gates,
        "tests_status": "COMPLETE",
        "FINAL_RESULT_GATE": "PASS" if ok else "FAIL",
    }
    Path(a.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
