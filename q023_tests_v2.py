#!/usr/bin/env python3
"""Mandatory validator for Bubbleverse Q023 V1."""
import argparse,json,math,os
from pathlib import Path
Q="Q023"; RUN="Q023-FULLMF-BASIN-DIRECTIONS-V2"; RESULT="R-Q023-EDE-FULLMF-BASIN-DIRECTIONS-002"
def write(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8"); os.replace(t,p)
def main():
    a=argparse.ArgumentParser(); a.add_argument("--result",required=True); a.add_argument("--output",required=True); x=a.parse_args()
    r=json.loads(Path(x.result).read_text(encoding="utf-8"))
    tests={
      "Q_IDENTITY_GATE":r.get("q")==Q,
      "RUN_RESULT_IDENTITY_GATE":r.get("run_id")==RUN and r.get("result_id")==RESULT,
      "ZERO_NEW_LIKELIHOOD_GATE":r.get("actual_new_likelihood_evaluations")==0,
      "MASK_SCOPE_GATE":r.get("selected_masks")==[3,6,7],
      "PARENT_Q022_PASS_GATE":r.get("gates",{}).get("Q022_FINAL_PARENT_GATE") is True,
      "ENDPOINT_COMPLETENESS_GATE":r.get("gates",{}).get("ENDPOINT_COMPLETENESS_GATE") is True,
      "FINITE_DIRECTION_GATE":r.get("gates",{}).get("FINITE_DIRECTION_GATE") is True,
      "THREE_PAIR_DIRECTION_GATE":sorted(r.get("cross_mask_direction_tests",{}))==["0-1","0-2","1-2"],
      "NO_PHYSICAL_OVERCLAIM_GATE":r.get("interpretation",{}).get("direction_similarity_is_physical_causation") is False,
      "Q021_NOT_REOPENED_GATE":r.get("interpretation",{}).get("q021_distributed_classification_reopened") is False,
      "Q022_NOT_REOPENED_GATE":r.get("interpretation",{}).get("q022_stability_reopened") is False,
      "INTERNAL_GATE_SET_PASS":all(bool(v) for v in r.get("gates",{}).values()),
    }
    ok=all(tests.values())
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"stage":"Q023_MANDATORY_TESTS","gates":tests,"FINAL_RESULT_GATE":"PASS" if ok else "FAIL"}
    write(x.output,out); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if ok else 2
if __name__=="__main__": raise SystemExit(main())
