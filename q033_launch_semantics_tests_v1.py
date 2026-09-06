#!/usr/bin/env python3
"""Static tests for Bubbleverse Q-033 launch-semantics matched A/B V1."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "q033_launch_semantics_ab_v1.py"
CONFIG = ROOT / "q033_launch_semantics_ab_v1_config.yml"
LOCK = ROOT / "q033_launch_semantics_protocol_lock_v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("q033", PROGRAM)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_historical_ref_semantics(mod):
    r = {"dist": "norm", "loc": 1.0, "scale": 0.25}
    x = mod.historical_ref_from_template(r, 3.5)
    assert isinstance(x, dict)
    assert x["dist"] == "norm"
    assert x["loc"] == 3.5
    assert x["scale"] == 0.25
    assert r["loc"] == 1.0, "function must not mutate historical template"


def test_scalar_ref_semantics(mod):
    params = {
        "x": {
            "prior": {"min": 0.0, "max": 10.0},
            "ref": {"dist": "norm", "loc": 2.0, "scale": 1.0},
        }
    }
    mod.set_scalar_ref(params, "x", 4.0)
    assert params["x"]["ref"] == 4.0
    audit = mod.scalar_ref_audit(params)
    assert audit["all_refs_scalar"] is True


def test_only_ref_stripping(mod):
    a = {
        "params": {
            "x": {"prior": {"min": 0, "max": 1}, "ref": 0.2},
            "fixed": 1.0,
        },
        "likelihood": {"L": {"dataset_params": {"x": 1}}},
        "sampler": {"minimize": {"seed": 1}},
        "output": "a",
    }
    b = copy.deepcopy(a)
    b["params"]["x"]["ref"] = {"dist": "norm", "loc": 0.2, "scale": 0.1}
    b["sampler"]["minimize"]["seed"] = 999
    b["output"] = "b"
    assert mod.canonical_hash(mod.strip_refs(a)) == mod.canonical_hash(mod.strip_refs(b))


def test_config_and_lock(mod):
    c = mod.load_cfg(CONFIG)
    assert c["project"]["q"] == "Q-033"
    assert c["model"]["backend_commit"] == mod.BACKEND_COMMIT
    assert c["basin"]["collapse_objective_tolerance"] == 0.50
    assert c["basin"]["collapse_common_endpoint_rms"] == 0.10
    assert c["basin"]["stable_basin_minimum_supporting_starts"] == 2
    assert c["basin"]["scale_floor_fraction"] == 1e-8
    d = mod.load_protocol_lock()
    assert d["q"] == "Q-033"


def main():
    mod = load_module()
    test_historical_ref_semantics(mod)
    test_scalar_ref_semantics(mod)
    test_only_ref_stripping(mod)
    test_config_and_lock(mod)
    out = {
        "q": "Q-033",
        "run_id": "Q033-CAMSPEC-LAUNCH-SEMANTICS-MATCHED-AB-V1",
        "stage": "STATIC_SELF_TEST",
        "status": "PASS",
        "tests": [
            "HISTORICAL_REF_SCALE_PRESERVATION",
            "SCALAR_REF_LITERALIZATION",
            "NON_REF_STRUCTURE_HASH",
            "CONFIG_AND_PROTOCOL_LOCK",
        ],
    }
    (ROOT / "q033_launch_semantics_static_validation_v1.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("Q033_STATIC_SELF_TEST_GATE=PASS")


if __name__ == "__main__":
    main()
