#!/usr/bin/env python3
"""Mandatory validation suite for Bubbleverse Q030 V2."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping

import yaml

Q = "Q030"
RUN = "Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V2"
RESULT = "R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-002"
COMMON_DIM = 9915
COMMON_SHA = "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"
Q028_HEAD = "7f5d35c0725530039162adfa4d71be288e8b4462"
Q028_BAD = "7f5d35efeb54b4a62d6dfb8f7074014b4fabc190"
Q027_COMMIT = "df03e30712690e61ff799558598405a22c0bacbb"


def read_json(path: str | Path) -> dict[str, Any]:
    x = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError("JSON_GATE=FAIL")
    return x


def write_json(path: str | Path, x: Any) -> None:
    Path(path).write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def check(name: str, ok: bool, detail: Any = None) -> dict[str, Any]:
    return {"test": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--config", default="q030_interaction_preserving_decomposition_v2_config.yml")
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    r = read_json(a.result)
    c = yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    v = c["validation"]
    tests: list[dict[str, Any]] = []

    tests.append(check(
        "T001_Q_RUN_RESULT_IDENTITY",
        r.get("q") == Q and r.get("run_id") == RUN and r.get("result_id") == RESULT
        and r.get("phase") == "MERGE" and r.get("status") == "COMPLETE",
    ))

    cs = r.get("common_support", {})
    tests.append(check(
        "T002_EXACT_Q028_COMMON_SUPPORT",
        int(cs.get("dimension", -1)) == COMMON_DIM and cs.get("keys_sha256") == COMMON_SHA,
        cs,
    ))

    tests.append(check(
        "T003_ZERO_NEW_SCIENTIFIC_EXECUTION",
        int(r.get("actual_new_likelihood_evaluations", -1)) == 0
        and int(r.get("actual_optimizer_evaluations", -1)) == 0
        and int(r.get("actual_sampling_evaluations", -1)) == 0
        and int(r.get("actual_q024_permutations", -1)) == 0,
    ))

    diags = r.get("diagnostics", [])
    identities = {(int(d.get("mask", -1)), str(d.get("edge"))) for d in diags}
    expected = {(m, e) for m in (3, 6, 7) for e in ("e01", "e02", "e12")}
    tests.append(check(
        "T004_NINE_DIAGNOSTIC_COMPLETENESS",
        len(diags) == 9 and identities == expected,
        sorted(identities),
    ))

    id_tol = float(v["q029_identity_closure_abs_tol"])
    max_id = max((abs(float(d["Q029_identity_closure_error"])) for d in diags), default=float("inf"))
    tests.append(check(
        "T005_Q029_EXACT_IDENTITY_CLOSURE",
        finite(max_id) and max_id <= id_tol,
        {"max_abs_error": max_id, "tol": id_tol},
    ))

    dm_tol = float(v["delta_m_identity_abs_tol"])
    max_dm = max((abs(float(d["delta2m_equals_minus_delta2r_max_abs_error"])) for d in diags), default=float("inf"))
    tests.append(check(
        "T006_DELTA2M_EQUALS_MINUS_DELTA2R",
        finite(max_dm) and max_dm <= dm_tol,
        {"max_abs_error": max_dm, "tol": dm_tol},
    ))

    q28_tol = float(v["q028_parent_interaction_abs_tol"])
    max_parent = max((abs(float(d["Q028_parent_closure_error"])) for d in diags), default=float("inf"))
    tests.append(check(
        "T007_Q028_PARENT_FUNCTIONAL_CLOSURE",
        finite(max_parent) and max_parent <= q28_tol,
        {"max_abs_error": max_parent, "tol": q28_tol},
    ))

    agg_tol = float(v["aggregation_closure_abs_tol"])
    agg_errors = []
    for d in diags:
        for mode, dist in d["distributions"].items():
            for term, err in dist["closure_error_vs_total"].items():
                agg_errors.append((d["mask"], d["edge"], mode, term, abs(float(err))))
    max_agg = max((x[-1] for x in agg_errors), default=float("inf"))
    tests.append(check(
        "T008_SPECTRUM_AND_MULTIPOLE_PAIR_CLOSURE",
        finite(max_agg) and max_agg <= agg_tol,
        {"max_abs_error": max_agg, "tol": agg_tol},
    ))

    boundary_ok = True
    for d in diags:
        b = d["interpretation_boundary"]
        boundary_ok &= (
            b.get("T_DM_name") == "DATA_MODEL_FACTORIAL_COUPLING"
            and b.get("T_DM_is_data_only_contribution") is False
            and b.get("T_MM_name") == "MODEL_QUADRATIC_FUNCTIONAL_TERM"
            and b.get("T_MM_is_physical_model_cause") is False
            and b.get("physical_causality_claimed") is False
            and b.get("cosmology_calibration_allocation_performed") is False
            and b.get("shapley_identification_used") is False
        )
    interp = r.get("interpretation", {})
    boundary_ok &= (
        interp.get("unique_data_model_attribution_claimed") is False
        and interp.get("cosmology_calibration_attribution_claimed") is False
        and interp.get("new_physics_claimed") is False
        and interp.get("shapley_as_identification_used") is False
    )
    tests.append(check("T009_NO_CAUSAL_OR_IDENTIFICATION_OVERCLAIM", bool(boundary_ok)))

    prov = r.get("provenance", {})
    provenance_ok = (
        prov.get("q027_correct_commit") == Q027_COMMIT
        and prov.get("q028_correct_execution_head_sha") == Q028_HEAD
        and prov.get("q028_misrecorded_sha_rejected") == Q028_BAD
        and prov.get("q028_correct_execution_head_sha") != Q028_BAD
        and int(prov.get("q028_final_artifact_id", -1)) == 9967068363
        and prov.get("q028_final_artifact_sha256")
        == "7dfbd1f27251ff311dd1de6118539dd691ab03d9afdb08539b3b13586c50d5af"
        and prov.get("q028_authoritative_common_support_sha256") == "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"
        and prov.get("q028_misrecorded_common_support_sha256_rejected") == "054220c018e58e902eab98b879eec4a823fb3238a1774ddbacc649bddca8b666"
        and int(prov.get("q030_v1_failed_run_id", -1)) == 33961119891
        and prov.get("q030_v2_repair") == "COMMON_SUPPORT_HASH_PROVENANCE_CORRECTION_ONLY"
    )
    tests.append(check("T010_PROVENANCE_CORRECTION_GATE", provenance_ok, prov))

    finite_ok = True
    for d in diags:
        for x in d["terms"].values():
            finite_ok &= finite(x)
        finite_ok &= finite(d["F_direct_from_residual_quadratic"])
        for dist in d["distributions"].values():
            for pair in dist["pairs"].values():
                finite_ok &= all(finite(x) for x in pair.values())
    tests.append(check("T011_FINITE_RESULT_GATE", bool(finite_ok)))

    all_pass = all(t["status"] == "PASS" for t in tests)
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "test_count": len(tests),
        "tests": tests,
        "FINAL_RESULT_GATE": "PASS" if all_pass else "FAIL",
    }
    write_json(a.output, out)
    print(f"FINAL_RESULT_GATE={out['FINAL_RESULT_GATE']}")
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
