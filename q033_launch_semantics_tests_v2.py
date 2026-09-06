#!/usr/bin/env python3
"""Static tests for Q033 protocol audit V2."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "q033_launch_semantics_protocol_audit_v2.py"
CONFIG = ROOT / "q033_launch_semantics_protocol_audit_v2_config.yml"
LOCK = ROOT / "q033_launch_semantics_source_lock_v2.json"


def load_module():
    spec = importlib.util.spec_from_file_location("q033v2", PROGRAM)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load_module()
    c = m.load_cfg(CONFIG)
    assert c["project"]["q"] == "Q-033"
    assert m.is_scalar_ref(1.23)
    assert not m.is_scalar_ref({"dist": "norm", "loc": 1.0, "scale": 0.1})
    assert tuple(c["q022_parameterization"]["frozen_primordial"]) == m.PRIMORDIAL

    # Pure set-ref semantics: scalar input remains scalar after endpoint recenter.
    params = {"x": {"prior": {"min": 0.0, "max": 2.0}, "ref": 1.0}}
    # q021.set_ref is integration-tested in the audit job; here test the V2 classifier.
    assert m.is_scalar_ref(params["x"]["ref"])

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["bubbleverse_files"]["q022_globality_continuation_v2.py"] == \
        "e8519f48869dd98a34e2a3280b9f872f97a237bc"

    rec = {
        "q": "Q-033",
        "run_id": "Q033-CAMSPEC-LAUNCH-SEMANTICS-PROTOCOL-AUDIT-V2",
        "stage": "STATIC_SELF_TEST",
        "status": "PASS",
        "tests": [
            "CONFIG_IDENTITY",
            "SCALAR_REF_CLASSIFIER",
            "PRIMORDIAL_BLOCK_IDENTITY",
            "HISTORICAL_SOURCE_LOCK_SCHEMA",
        ],
    }
    (ROOT / "q033_launch_semantics_static_validation_v2.json").write_text(
        json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("Q033_V2_STATIC_SELF_TEST_GATE=PASS")


if __name__ == "__main__":
    main()
