#!/usr/bin/env python3
"""Static and deterministic numerical gates for Bubbleverse Q-032 bridge V1."""
from __future__ import annotations

import argparse
import ast
import json
import py_compile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q-032"
RUN = "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V1"
RESULT = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-001"


def write(path, obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def static(output: str) -> int:
    files = [
        "q032_planck_tt3pair_bridge_v1.py",
        "q032_tests_v1.py",
    ]
    for name in files:
        py_compile.compile(str(ROOT/name), doraise=True)

    main_text=(ROOT/files[0]).read_text(encoding="utf-8")
    ast.parse(main_text)
    cfg=yaml.safe_load((ROOT/"q032_planck_tt3pair_bridge_v1_config.yml").read_text(encoding="utf-8"))
    src=json.loads((ROOT/"q032_source_lock_v1.json").read_text(encoding="utf-8"))
    proto=json.loads((ROOT/"q032_protocol_lock_v1.json").read_text(encoding="utf-8"))

    assert cfg["project"]["q"] == Q
    assert cfg["project"]["run_id"] == RUN
    assert cfg["project"]["result_id"] == RESULT
    assert cfg["model"]["backend_commit"] == "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
    assert cfg["implementations"]["hillipop"]["commit"] == "a09ddde3e7ce11df99f74685feb1f1764cafb251"
    assert cfg["implementations"]["hillipop"]["parent_case031_component"] == "planck_2020_hillipop.TTTEEE"
    assert cfg["implementations"]["hillipop"]["component"] == "planck_2020_hillipop.TT"
    assert cfg["implementations"]["hillipop"]["exact_data_products"]["covariance_matrix_file"] == "invfll_PR4_v4.2_TT.fits"
    assert cfg["phase_a"]["modes"] == ["TT"]
    assert cfg["phase_a"]["pairs"] == ["143x143","143x217","217x217"]
    assert cfg["optimizer"]["stage1"] == {"max_evals":200000,"rhoend":1.0e-4}
    assert cfg["optimizer"]["refinement"] == {"max_evals":300000,"rhoend":1.0e-5}
    assert float(cfg["basin"]["collapse_objective_tolerance"]) == 0.50
    assert float(cfg["basin"]["collapse_common_endpoint_rms"]) == 0.10
    assert int(cfg["basin"]["stable_basin_minimum_supporting_starts"]) == 2
    assert float(cfg["basin"]["scale_floor_fraction"]) == 1e-8
    assert cfg["covariance"]["principal_precision_submatrix_as_marginal_forbidden"] is True
    assert cfg["covariance"]["semantics"] == "C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS"
    assert cfg["rules"]["case031_closed"] is True
    assert cfg["rules"]["no_new_case031_seeds"] is True
    assert cfg["rules"]["no_basin_threshold_change"] is True
    assert cfg["rules"]["no_cross_likelihood_absolute_objective_subtraction"] is True
    assert cfg["rules"]["no_cross_likelihood_chi2_sum"] is True

    assert src["q"] == Q and src["run_id"] == RUN and src["result_id"] == RESULT
    assert src["source_registry"]["K-047"]["bibliographic_status"] == "BIBLIOGRAPHIC_DETAILS_NOT_INVENTED"
    assert src["source_registry"]["K-045/K-052"]["alias_rule"] == "ONE_EXTERNAL_SOURCE_COUNT_ONCE"
    assert src["source_registry"]["K-039/K-051"]["alias_rule"] == "ONE_EXTERNAL_SOURCE_COUNT_ONCE"
    assert src["source_registry"]["CAMSPEC_2021_ID_UNRESOLVED"]["historical_bubbleverse_id"] == "NOT_GUESSED"

    import q032_planck_tt3pair_bridge_v1 as q32
    q32.load_cfg(ROOT/"q032_planck_tt3pair_bridge_v1_config.yml")
    q32.load_source_lock()
    checked=q32.load_protocol_lock()
    assert checked["protocol_sha256"] == proto["protocol_sha256"]
    assert checked["case031_status"] == "CLOSED_AUTHORITATIVE_NOT_REOPENED"
    assert checked["hillipop"]["parent_case031_component"] == "planck_2020_hillipop.TTTEEE"
    assert checked["hillipop"]["component"] == "planck_2020_hillipop.TT"

    # Deterministic synthetic covariance test exercises the actual production routine.
    synth_path=ROOT/"q032_static_synthetic_covariance_v1.json"
    q32.self_test(cfg, synth_path)
    synth=json.loads(synth_path.read_text(encoding="utf-8"))
    assert synth["status"] == "PASS"
    assert synth["principal_precision_submatrix_used_as_marginal"] is False

    # Ensure the source contains the explicit semantic path and no accidental cross-likelihood final subtraction helper.
    assert "C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS" in main_text
    assert "cross_likelihood_absolute_objective_subtraction_performed\": False" in main_text

    rec={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"Q032_STATIC_VALIDATION","status":"PASS",
      "PY_COMPILE_GATE":"PASS","CONFIG_IDENTITY_GATE":"PASS",
      "SOURCE_ALIAS_GATE":"PASS","K047_NONINVENTION_GATE":"PASS",
      "PROTOCOL_HASH_GATE":"PASS","SYNTHETIC_COVARIANCE_SEMANTICS_GATE":"PASS"
    }
    write(output,rec)
    print("Q032_STATIC_GATE=PASS")
    return 0


def main():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static"); s.add_argument("--output",required=True)
    a=p.parse_args()
    if a.cmd=="static": return static(a.output)
    return 2

if __name__=="__main__":
    raise SystemExit(main())
