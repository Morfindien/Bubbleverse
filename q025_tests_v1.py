#!/usr/bin/env python3
"""Mandatory Q025 V1 final-result tests."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

Q = "Q025"
RUN = "Q025-FULLMF-BASIN-COMPONENT-ATTRIBUTION-V1"
RESULT = "R-Q025-EDE-FULLMF-BASIN-COMPONENT-ATTRIBUTION-001"


def finite(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    r = json.loads(Path(a.result).read_text(encoding="utf-8"))
    diag = r.get("diagnostics", {})
    expected_keys = {
        f"m{m}_e{a}{b}"
        for m in (3,6,7)
        for a,b in ((0,1),(0,2),(1,2))
    }

    gates = {
        "Q_IDENTITY_GATE": r.get("q") == Q,
        "RUN_RESULT_IDENTITY_GATE":
            r.get("run_id") == RUN and r.get("result_id") == RESULT,
        "MODEL_IDENTITY_GATE":
            r.get("scientific_surface",{}).get("model",{}).get("backend_commit")
            == "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "MASK_SCOPE_GATE":
            r.get("scientific_surface",{}).get("masks") == [3,6,7],
        "EDGE_COMPLETENESS_GATE": set(diag) == expected_keys,
        "FIXED_VECTOR_COUNT_GATE":
            int(r.get("actual_new_likelihood_evaluations",-1)) == 72,
        "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations",-1)) == 0,
        "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated",-1)) == 0,
        "COVARIANCE_OUTPUT_GATE": all(
            isinstance(v.get("endpoint_delta",{}).get("by_spectrum"), dict)
            and isinstance(v.get("endpoint_delta",{}).get("covariance_block_pair_terms"), dict)
            for v in diag.values()
        ),
        "FUNCTIONAL_INTERACTION_GATE": all(
            set(v.get("functional_attribution",{}).get("highl_shapley",{}))
            == {"cosmology","shared_nuisance","foreground"}
            and len(v.get("functional_attribution",{}).get("highl_pair_interactions",{})) == 3
            for v in diag.values()
        ),
        "FINITE_ATTRIBUTION_GATE": all(
            all(finite(x) for x in
                v.get("functional_attribution",{}).get("highl_shapley",{}).values())
            for v in diag.values()
        ),
        "PARENT_PRESERVATION_GATE": all([
            r.get("journal_effect_if_final_pass",{}).get("q022_stable_multibasin_preserved") is True,
            r.get("journal_effect_if_final_pass",{}).get("q023_fixed_lineage_result_preserved") is True,
            r.get("journal_effect_if_final_pass",{}).get("q024_permutation_negative_result_preserved") is True,
        ]),
        "NO_CAUSAL_OVERCLAIM_GATE":
            r.get("claim_boundaries",{}).get("physical_causality_claimed") is False,
    }
    passed = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q025_MANDATORY_TESTS",
        "gates": gates,
        "tests_status": "COMPLETE",
        "FINAL_RESULT_GATE": "PASS" if passed else "FAIL",
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
