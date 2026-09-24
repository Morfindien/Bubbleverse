#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
Q="Q-042"; PID="Q042-EXECMECH-V1"
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def close(a,b,tol=2e-5): return abs(float(a)-float(b))<=tol*max(1.0,abs(float(b)))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--result",required=True); ap.add_argument("--reference",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    d=load(a.result); r=load(a.reference)["diagnostic_reference"]
    gates={}
    gates["Q_IDENTITY"]=d.get("q")==Q and d.get("program_id")==PID
    gates["NO_SCIENCE_CLASSIFICATION"]=d.get("actual_computed_scientific_result") is False and d.get("scientific_classification")=="NOT_AVAILABLE"
    gates["V19_ARTIFACT_COUNT"]=d.get("counts",{}).get("total_chains")==32
    gates["NONCONVERGENCE_REPRODUCED"]=d.get("counts",{}).get("rminus1_last_le_1p05")==0
    gates["HIGH_ACCEPTANCE_TRANSPORT"]=d.get("counts",{}).get("acceptance_last_ge_0p95")==r["acceptance_last_ge_0p95"]
    gates["REFERENCE_ARM_SUMMARY"]=all(close(d["arms"][arm][k],r["arms"][arm][k]) for arm in ("camspec","hillipop") for k in r["arms"][arm])
    gates["REFERENCE_FULL_MEANS"]=all(close(d["full_chain_means"][key][c],r["full_chain_means"][key][c]) for key in r["full_chain_means"] for c in r["full_chain_means"][key])
    gates["MODE_RIDGE_DIAGNOSIS"]=d.get("diagnostic_flags",{}).get("mode_or_ridge_structure") is True
    gates["BOUNDARY_DIAGNOSIS"]=d.get("diagnostic_flags",{}).get("theta_boundary_structure") is True
    gates["EXECUTION_MECHANISM_DECISION"]=d.get("execution_decision")=="REJECT_MORE_OF_SAME_MCMC__SELECT_POLYCHORD_PLUS_MULTISTART_BOBYQA"
    gates["Q040_FIREWALL"]=d.get("claim_boundaries",{}).get("q040_scientific_products_used") is False
    gates["V19_UNCHANGED"]=d.get("claim_boundaries",{}).get("v19_modified") is False
    gates["SN_LOCK"]=d.get("supernova_source_lock",{}).get("component")=="sn.pantheonplus"
    status="PASS" if all(gates.values()) else "FAIL"
    out={"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("Q042_V1_FINAL_TEST_GATE="+status)
    return 0 if status=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
