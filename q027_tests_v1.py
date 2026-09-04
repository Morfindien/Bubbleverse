#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

Q = "Q027"
RUN = "Q027-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-V1"
RESULT = "R-Q027-EDE-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-001"
EXPECTED = {f"m{m}_e{a}{b}" for m in (3, 6, 7) for a, b in ((0, 1), (0, 2), (1, 2))}


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
    d = r.get("diagnostics", {})
    cs = r.get("cross_mask_summary", {})

    edge_fields_ok = all(
        finite(v.get("q026_parent_pair_interaction"))
        and finite(v.get("q027_recomputed_objective_pair_interaction"))
        and isinstance(v.get("decomposition", {}).get("pointwise_pair_contrasts"), list)
        and isinstance(v.get("decomposition", {}).get("covariance_block_pair_interaction_contrasts"), dict)
        for v in d.values()
    )
    precision_fixed = all(
        v.get("decomposition", {}).get("precision_fixed_across_four_parameter_states") is True
        for v in d.values()
    )
    target_rows_exist = all(
        len(v.get("decomposition", {}).get("pointwise_pair_contrasts", [])) > 0
        for v in d.values()
    )
    finite_target = all(
        finite(v["decomposition"]["target_tt_ell600_999"]["absolute_share_of_all_pointwise_pair_contrast"])
        and finite(v["decomposition"]["target_tt_ell600_999"]["residual_pair_contrast_l2_share"])
        and finite(v["decomposition"]["target_tt_ell600_999"]["precision_weighted_residual_pair_contrast_l2_share"])
        for v in d.values()
    )
    parent_repro = r.get("parent_reproduction", {}).get("q026_omega_cdm_x_A_planck_pair_gate") is True

    gates = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE": r.get("run_id") == RUN and r.get("result_id") == RESULT,
        "MODEL_BACKEND_GATE":
            r.get("scientific_surface", {}).get("model", {}).get("backend_commit")
            == "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "LIKELIHOOD_GATE":
            r.get("scientific_surface", {}).get("likelihood")
            == "planck_NPIPE_highl_CamSpec.TTTEEE",
        "EDGE_COMPLETENESS_GATE": set(d) == EXPECTED,
        "FIXED_VECTOR_COUNT_GATE": int(r.get("actual_new_likelihood_evaluations", -1)) == 36,
        "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations", -1)) == 0,
        "NO_SAMPLING_GATE": int(r.get("sampling_evaluations", -1)) == 0,
        "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated", -1)) == 0,
        "EDGE_DECOMPOSITION_COMPLETENESS_GATE": edge_fields_ok,
        "Q026_PAIR_REPRODUCTION_GATE": parent_repro,
        "PRECISION_INVARIANCE_WITHIN_SWITCH_GATE": precision_fixed,
        "TARGET_POINTWISE_ROWS_GATE": target_rows_exist,
        "FINITE_TARGET_METRICS_GATE": finite_target,
        "CROSS_MASK_SUMMARY_GATE":
            cs.get("within_mask_mechanism") == "RESIDUAL_CHANGE_UNDER_FIXED_INVERSE_COVARIANCE"
            and cs.get("spatial_localization") in {
                "MASK6_TT600_999_TRIAD_CONCENTRATED",
                "DISTRIBUTED_BEYOND_TT600_999_TRIAD",
                "MIXED_OR_WEAKLY_LOCALIZED",
            },
        "PARENT_PRESERVATION_GATE": all(r.get("journal_preservation", {}).values()),
        "NO_CAUSAL_OVERCLAIM_GATE":
            r.get("claim_boundaries", {}).get("physical_causality_claimed") is False
            and r.get("claim_boundaries", {}).get("calibration_failure_proven") is False
            and r.get("claim_boundaries", {}).get("instrumental_systematic_proven") is False,
    }

    ok = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q027_MANDATORY_TESTS",
        "gates": gates,
        "tests_status": "COMPLETE",
        "FINAL_RESULT_GATE": "PASS" if ok else "FAIL",
    }
    Path(a.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
