#!/usr/bin/env python3
import argparse,json,math
from pathlib import Path
Q="Q019"; RUN="Q019-PLANCK-COSMOLOGY-GLOBALITY-V2"; RESULT="R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-002"
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--merged",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    d=json.loads(Path(a.merged).read_text())
    g=dict(d.get("gates",{}))
    g["Q_IDENTITY_GATE"]=d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT
    g["CLASSIFICATION_GATE"]=d.get("classification") in {"LIKELIHOOD DEPENDENCE PRIMARILY HIGH-H0 / LOCAL-GEOMETRY","INDETERMINATE"}
    g["INTERPRETATION_SAFETY_GATE"]=(d.get("interpretation",{}).get("causal_systematic_claim_allowed") is False
      and d.get("interpretation",{}).get("new_physics_claim_allowed") is False
      and d.get("interpretation",{}).get("q018_architecture_gap_used_as_physical_component") is False
      and d.get("interpretation",{}).get("cross_chain_chi2_sum_performed") is False)
    mandatory=[
      "Q_IDENTITY_GATE","JOB_COMPLETENESS_GATE","FULL_MF_FREE_GLOBALITY_STABILITY_GATE",
      "PARENT_BEST_NONREGRESSION_GATE","Q016_ENDPOINT_OBJECTIVE_REPRODUCTION_GATE",
      "Q016_ENDPOINT_PENALTY_REPRODUCTION_GATE","NO_GATE_RELAXATION_GATE",
      "NO_CROSS_CHAIN_CHI2_SUM_GATE","Q018_GAP_NONPHYSICAL_GATE","V1_OTHER_GATES_PRESERVED_GATE",
      "CLASSIFICATION_GATE","INTERPRETATION_SAFETY_GATE"
    ]
    final=all(g.get(k) is True for k in mandatory)
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"test_type":"MANDATORY_RESULT_TESTS_V2",
         "gates":g,"mandatory":mandatory,"FINAL_RESULT_GATE":"PASS" if final else "FAIL",
         "classification":d.get("classification")}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2
if __name__=="__main__": raise SystemExit(main())
