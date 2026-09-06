#!/usr/bin/env python3
"""Static and final integrity tests for Bubbleverse Q-034 V1."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import q034_primordial_freeze_isolation_v1 as q34


def write(path: str | Path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def static(output: str | Path) -> int:
    c = q34.load_cfg()
    assert q34.Q == "Q-034"
    assert q34.PRIMORDIAL == ("n_s", "logA", "tau_reio")
    assert q34.START_LABELS == (
        "M3-S0", "M3-S1", "M3-S2", "M6-S0", "M6-S1", "M6-S2", "M7-S0", "M7-S1", "M7-S2"
    )
    assert c["parents"]["q032_v4"]["github_run_id"] == 34015845246
    assert c["execution"]["sampled_control_new_jobs"] == 0
    assert c["execution"]["frozen_stage1_jobs"] == 9
    assert c["execution"]["frozen_refinement_jobs_if_required"] == 9
    assert c["rules"]["freeze_only_primordial_block"] is True
    assert c["rules"]["no_q032_sector_rerun"] is True
    lock = q34.read_json(q34.ROOT / q34.SOURCE_LOCK_FILE)
    assert lock["bubbleverse_files"]["q032_planck_tt3pair_bridge_v2.py"] == "2199011cc44d6cadab3f62265ea6c77ecb187027"
    assert lock["bubbleverse_files"]["q031_planck_portability_v1.py"] == "5d903e76105b7dcaf41ce0c68cbbeeaee4cda835"
    assert lock["bubbleverse_files"]["q031_planck_portability_v1_config.yml"] == "aa8a0e466904a684fd9957d2df212f3a910e3d9a"

    sampled = {
        "likelihood": {"L": {"x": 1}},
        "sampler": {"minimize": {"best_of": 1}},
        "prior": {},
        "params": {
            "n_s": {"prior": {"min": 0.8, "max": 1.2}, "ref": 0.97},
            "logA": {"prior": {"min": 2.0, "max": 4.0}, "ref": 3.0},
            "tau_reio": {"prior": {"min": 0.01, "max": 0.2}, "ref": 0.05},
            "H0": {"prior": {"min": 50.0, "max": 90.0}, "ref": 70.0},
            "fixed": 1.0,
        },
    }
    frozen = copy.deepcopy(sampled)
    fixed = {"n_s": 0.971, "logA": 3.04, "tau_reio": 0.052}
    q34.freeze_primordial(frozen, fixed)
    audit = q34.assert_only_primordial_delta(sampled, frozen, fixed)
    assert audit["removed_from_sampled_set"] == ["logA", "n_s", "tau_reio"]
    assert audit["nonprimordial_specs_identical"] is True

    bad = copy.deepcopy(frozen)
    bad["params"]["H0"]["ref"] = 71.0
    failed = False
    try:
        q34.assert_only_primordial_delta(sampled, bad, fixed)
    except RuntimeError:
        failed = True
    assert failed, "Non-primordial mutation must fail identity gate"

    out = {
        "q": q34.Q,
        "run_id": q34.RUN,
        "result_id": q34.RESULT,
        "stage": "Q034_STATIC_TESTS",
        "status": "PASS",
        "tests": {
            "Q_IDENTITY": "PASS",
            "PRIMORDIAL_BLOCK": "PASS",
            "NINE_STARTS": "PASS",
            "CONTROL_REUSE_POLICY": "PASS",
            "ONLY_PRIMORDIAL_DELTA_POSITIVE_TEST": "PASS",
            "NONPRIMORDIAL_MUTATION_NEGATIVE_TEST": "PASS",
            "BASIN_CLASSIFIER_SOURCE_LOCK": "PASS"
        }
    }
    write(output, out)
    print("Q034_STATIC_TESTS=PASS")
    return 0


def final(preflight: str | Path, merged: str | Path, validated: str | Path, output: str | Path) -> int:
    pf = q34.load_preflight(preflight)
    m = q34.read_json(merged)
    v = q34.read_json(validated)
    assert pf["sampled_control_reuse"]["approved"] is True
    assert m["FINAL_RESULT_GATE"] == "PROVISIONAL_PENDING_VALIDATION"
    assert v["FINAL_RESULT_GATE"] == "PASS"
    assert v["status"] == "PASS"
    assert v["tests_status"] == "COMPLETE"
    assert len(v["result_tests"]) == 11
    assert all(x == "PASS" for x in v["result_tests"].values())
    assert v["classification"] in {
        "PRIMORDIAL_FREEZE_SUFFICIENT_WITHIN_MATCHED_Q034",
        "PRIMORDIAL_FREEZE_ALONE_NOT_SUFFICIENT",
    }
    assert v["sampled_control"]["stable_multibasin"] is False
    assert int(v["sampled_control"]["stable_basin_count"]) == 0
    assert int(v["frozen_primordial_arm"]["complete_profiles"]) == 9
    out = {
        "q": q34.Q,
        "run_id": q34.RUN,
        "result_id": q34.RESULT,
        "stage": "Q034_POST_FINAL_TESTS",
        "status": "PASS",
        "FINAL_RESULT_GATE": "PASS",
        "classification": v["classification"],
    }
    write(output, out)
    print("Q034_POST_FINAL_TESTS=PASS")
    return 0


def parser():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("static")
    a.add_argument("--output", required=True)
    a = sub.add_parser("final")
    a.add_argument("--preflight", required=True)
    a.add_argument("--merged", required=True)
    a.add_argument("--validated", required=True)
    a.add_argument("--output", required=True)
    return p


def main():
    args = parser().parse_args()
    if args.cmd == "static":
        return static(args.output)
    if args.cmd == "final":
        return final(args.preflight, args.merged, args.validated, args.output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
