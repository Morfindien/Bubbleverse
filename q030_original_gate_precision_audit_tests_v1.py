#!/usr/bin/env python3
"""Mandatory technical tests for the ONE Q030 original-gate precision audit."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import yaml

Q = "Q030"
RUN = "Q030-ORIGINAL-GATE-PRECISION-AUDIT-V1"
RESULT = "R-Q030-ORIGINAL-GATE-PRECISION-AUDIT-001"
COMMON_SHA = "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test(name: str, passed: bool, detail: Any = None) -> dict[str, Any]:
    return {"test": name, "status": "PASS" if passed else "FAIL", "detail": detail}


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    c = yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    r = load(a.result)
    ts = []

    ts.append(test(
        "T001_Q_RUN_RESULT_IDENTITY",
        r.get("q") == Q
        and r.get("run_id") == RUN
        and r.get("result_id") == RESULT
        and r.get("status") == "COMPLETE",
    ))

    ts.append(test(
        "T002_ORIGINAL_TOLERANCES_UNCHANGED",
        float(c["validation"]["original_q029_identity_abs_tol"]) == 1e-8
        and float(c["validation"]["original_aggregation_abs_tol"]) == 1e-8
        and float(c["validation"]["delta_m_identity_abs_tol"]) == 1e-11
        and float(c["validation"]["q028_parent_interaction_abs_tol"]) == 2e-4
        and c["validation"]["tolerance_relaxation_forbidden"] is True,
        r.get("frozen_original_gates"),
    ))

    ts.append(test(
        "T003_EXACT_COMMON_SUPPORT",
        r.get("q028_parent", {}).get("common_dimension") == 9915
        and r.get("q028_parent", {}).get("common_support_sha256") == COMMON_SHA,
        r.get("q028_parent"),
    ))

    ec = r.get("execution_counts", {})
    ts.append(test(
        "T004_ZERO_NEW_SCIENTIFIC_EXECUTION",
        int(ec.get("new_likelihood_evaluations", -1)) == 0
        and int(ec.get("optimizer_evaluations", -1)) == 0
        and int(ec.get("sampling_evaluations", -1)) == 0
        and int(ec.get("q024_permutations", -1)) == 0,
        ec,
    ))

    ds = r.get("diagnostics", [])
    ids = {(int(d["mask"]), d["edge"]) for d in ds}
    exp = {(m, e) for m in (3, 6, 7) for e in ("e01", "e02", "e12")}
    ts.append(test(
        "T005_NINE_DIAGNOSTIC_COMPLETENESS",
        len(ds) == 9 and ids == exp,
        sorted(ids),
    ))

    ts.append(test(
        "T006_STABLE_METHOD_NOT_ALGEBRAIC_RESCUE",
        all(
            "STABLE_FACTORIAL_BILINEAR_EXPANSION" in d.get("method", "")
            and "T_MM" in d.get("terms", {})
            and "F_direct_from_residual_factorial_stable" in d
            for d in ds
        ),
        (
            "T_MM and F_residual are independently reconstructed from the "
            "factorial quadratic expansion; no F-T_DM definition is accepted."
        ),
    ))

    max_dm = max(
        abs(float(d["delta2m_equals_minus_delta2r_max_abs_error"])) for d in ds
    )
    ts.append(test(
        "T007_DELTA2M_EQUALS_MINUS_DELTA2R",
        finite(max_dm)
        and max_dm <= float(c["validation"]["delta_m_identity_abs_tol"]),
        {"max_abs_error": max_dm, "tol": c["validation"]["delta_m_identity_abs_tol"]},
    ))

    max_parent = max(abs(float(d["Q028_parent_closure_error"])) for d in ds)
    ts.append(test(
        "T008_Q028_PARENT_FUNCTIONAL_CLOSURE",
        finite(max_parent)
        and max_parent <= float(c["validation"]["q028_parent_interaction_abs_tol"]),
        {
            "max_abs_error": max_parent,
            "tol": c["validation"]["q028_parent_interaction_abs_tol"],
        },
    ))

    # The audit must REPORT the frozen scientific gate. It is not a technical
    # failure if that gate is scientifically negative.
    ar = r.get("audit_results", {})
    reported_original = r.get("ORIGINAL_Q030_GATE") in ("PASS", "FAIL")
    ts.append(test(
        "T009_ORIGINAL_GATE_EXPLICITLY_REPORTED",
        reported_original
        and finite(ar.get("max_abs_Q029_identity_closure_error"))
        and finite(ar.get("max_abs_group_pair_aggregation_closure_error")),
        {
            "ORIGINAL_Q030_GATE": r.get("ORIGINAL_Q030_GATE"),
            "max_identity": ar.get("max_abs_Q029_identity_closure_error"),
            "max_aggregation": ar.get("max_abs_group_pair_aggregation_closure_error"),
        },
    ))

    ts.append(test(
        "T010_NEGATIVE_RESULT_IS_NOT_HIDDEN",
        (
            r.get("ORIGINAL_Q030_GATE") == "PASS"
            and r.get("AUDIT_OUTCOME") == "ORIGINAL_Q030_GATE_PASS_WITH_STABLE_ARITHMETIC"
        )
        or (
            r.get("ORIGINAL_Q030_GATE") == "FAIL"
            and r.get("AUDIT_OUTCOME")
            == "ORIGINAL_Q030_GATE_FAIL_AFTER_ONE_STABLE_PRECISION_AUDIT"
        ),
        r.get("AUDIT_OUTCOME"),
    ))

    boundary = r.get("interpretation_boundaries", {})
    ts.append(test(
        "T011_NO_SCIENTIFIC_INPUT_OR_CAUSAL_MUTATION",
        boundary.get("scientific_inputs_changed") is False
        and boundary.get("likelihood_evaluated") is False
        and boundary.get("optimization_performed") is False
        and boundary.get("sampling_performed") is False
        and boundary.get("q024_rerun") is False
        and boundary.get("T_DM_is_data_only_contribution") is False
        and boundary.get("T_MM_is_physical_model_cause") is False
        and boundary.get("causal_allocation_performed") is False
        and boundary.get("new_physics_claimed") is False,
        boundary,
    ))

    finite_result = all(
        all(finite(v) for v in d["terms"].values())
        and finite(d["F_direct_from_residual_factorial_stable"])
        and finite(d["Q029_identity_closure_error"])
        for d in ds
    )
    ts.append(test("T012_FINITE_RESULT_GATE", finite_result))

    ts.append(test(
        "T013_STOP_DIRECTIVE_PRESENT",
        "STOP_AFTER_THIS_AUDIT" in r.get("stop_directive", ""),
        r.get("stop_directive"),
    ))

    ok = all(t["status"] == "PASS" for t in ts)
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "test_count": len(ts),
        "tests": ts,
        "ORIGINAL_Q030_GATE": r.get("ORIGINAL_Q030_GATE"),
        "AUDIT_EXECUTION_GATE": "PASS" if ok else "FAIL",
    }
    Path(a.output).write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"AUDIT_EXECUTION_GATE={out['AUDIT_EXECUTION_GATE']} "
        f"ORIGINAL_Q030_GATE={out['ORIGINAL_Q030_GATE']}"
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
