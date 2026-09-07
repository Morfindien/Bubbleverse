#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

EXPECTED_Q = "Q-036"
EXPECTED_PROGRAM = "Q036-GEOMETRY-V1"
EXPECTED_RESULT = "R-Q036-EDE-ENDPOINT-GEOMETRY-PORTABILITY-001"
MANDATORY = [
    "Q_IDENTITY_GATE", "PARENT_PROVENANCE_GATE", "Q035_BASELINE_PRESERVATION_GATE",
    "NINE_BY_NINE_LABEL_IDENTITY_GATE", "COMMON_COORDINATE_GATE", "Q031_LOCKED_SCALE_GATE",
    "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE", "FINITE_RESULT_GATE", "PERMUTATION_INVARIANCE_GATE",
    "REFERENCE_REPLAY_GATE", "DECISION_REPLAY_GATE",
]

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("result"); ap.add_argument("--output",default="q036_tests_v1.json"); a=ap.parse_args()
    d=json.loads(Path(a.result).read_text())
    tests={}
    tests["IDENTITY"] = d.get("q")==EXPECTED_Q and d.get("program_id")==EXPECTED_PROGRAM and d.get("result_id")==EXPECTED_RESULT
    gates=d.get("gates",{})
    tests["MANDATORY_GATES"] = all(gates.get(k) is True for k in MANDATORY)
    x=d.get("descriptors",{})
    numbers=[x.get("location_median"),x.get("shape_median_drift"),x.get("normalized_centroid_shift")]
    tests["FINITE_SUMMARY"] = all(isinstance(v,(int,float)) and math.isfinite(v) for v in numbers)
    tests["NO_OBJECTIVE_CROSS_COMPARE"] = d.get("common_geometry",{}).get("objective_values_used") is False
    tests["Q035_PRESERVED"] = d.get("claim_boundaries",{}).get("q035_classifier_harmonization_remains_authoritative") is True
    tests["STOP_CASE_CLOSED"] = d.get("q036_stop_case") in ("A","B") if d.get("FINAL_RESULT_GATE")=="PASS" else d.get("q036_stop_case")=="C"
    tests["DECISION_CONSISTENCY"] = (
        (d.get("q036_stop_case")=="A" and d.get("final_classification")=="MATERIAL_REPRODUCIBLE_COMMON_GEOMETRY_DIFFERENCE")
        or (d.get("q036_stop_case")=="B" and d.get("final_classification")=="NO_MATERIAL_GLOBAL_COMMON_GEOMETRY_DIFFERENCE_ESTABLISHED")
        or (d.get("q036_stop_case")=="C" and d.get("final_classification")=="INCONCLUSIVE")
    )
    status="PASS" if all(tests.values()) else "FAIL"
    out={"q":EXPECTED_Q,"program_id":EXPECTED_PROGRAM,"test_id":"Q036-RESULT-TESTS-V1","status":status,"tests":tests}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if status=="PASS" else 2

if __name__=="__main__": raise SystemExit(main())
