#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
Q="Q020"
RUN="Q020-PLANCK-CROSS-PROFILE-DIRECTION-REPAIR-V2"
RESULT="R-Q020-EDE-PLANCK-CROSS-PROFILE-DIRECTION-002"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--merged",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    d=json.loads(Path(a.merged).read_text())
    req=[
      "JOB_COMPLETENESS_GATE","VERTEX_GRID_COMPLETENESS_GATE","FINITE_RESULT_GATE",
      "NUISANCE_RESTART_STABILITY_GATE",
      "Q019_FULL_MF_CROSS_OBJECTIVE_REPRODUCTION_GATE",
      "Q019_LITE_CROSS_OBJECTIVE_REPRODUCTION_GATE",
      "FULL_MF_NATIVE_ENDPOINT_NONREGRESSION_GATE",
      "LITE_NATIVE_ENDPOINT_NONREGRESSION_GATE",
      "NO_CROSS_CHAIN_CHI2_SUM_GATE","Q018_GAP_NONPHYSICAL_GATE",
      "Q017_CAUSAL_STATUS_PRESERVED_GATE","INTERPRETATION_SAFETY_GATE"
    ]
    gates={"Q_IDENTITY_GATE":d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT}
    for k in req:gates[k]=d.get("gates",{}).get(k) is True
    gates["Q019_HISTORY_PRESERVATION_GATE"]=(
      d.get("repair",{}).get("historical_values_rewritten") is False
      and d.get("rules",{}).get("q019_historical_cross_cost_replaced") is False
    )
    gates["NO_GATE_RELAXATION_GATE"]=d.get("repair",{}).get("gate_relaxation_performed") is False
    final=all(gates.values())
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"test_type":"MANDATORY_V2_RESULT_TESTS",
         "gates":gates,"FINAL_RESULT_GATE":"PASS" if final else "FAIL",
         "classification":d.get("classification") if final else "UNRESOLVED"}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2
if __name__=="__main__":
    raise SystemExit(main())
