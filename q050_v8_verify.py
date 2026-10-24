#!/usr/bin/env python3
import json,math,sys
from pathlib import Path
p=Path(sys.argv[1])
if not p.exists() or p.stat().st_size==0: raise SystemExit("VERIFY_FAIL: result missing")
x=json.loads(p.read_text())
req=["execution_status","result_validation_status","scientific_outcome",
     "actual_computed_result","domain_z","q_branches","next_engine"]
miss=[k for k in req if k not in x]
if miss: raise SystemExit("VERIFY_FAIL: missing "+",".join(miss))
if x["q"]!="Q050" or x["revision"]!="V8": raise SystemExit("VERIFY_FAIL: identity")
if x["domain_z"]!=[650.2566501559347,810.0]: raise SystemExit("VERIFY_FAIL: domain")
if x["q_branches"]!=[1e-06,0.0]: raise SystemExit("VERIFY_FAIL: q branches")
# A claimed validated normal certificate must contain actual coverage and branch extrema.
if x["result_validation_status"]=="VALIDATED":
    c=x.get("certificate")
    if not isinstance(c,dict): raise SystemExit("VERIFY_FAIL: validated without certificate")
    for q in ("q_1e-6","q_0"):
        row=c.get(q)
        if not isinstance(row,dict): raise SystemExit("VERIFY_FAIL: missing "+q)
        for k in ("N_HMLA_min","N_HMLA_max","N_SWIFT_min","N_SWIFT_max",
                  "reachable_cells","unresolved_cells"):
            if k not in row: raise SystemExit("VERIFY_FAIL: "+q+" missing "+k)
            if isinstance(row[k],float) and not math.isfinite(row[k]):
                raise SystemExit("VERIFY_FAIL: nonfinite")
        if row["unresolved_cells"]!=0:
            raise SystemExit("VERIFY_FAIL: VALIDATED with unresolved cells")
print("VERIFY_PASS")
print("status =",x["result_validation_status"])
print("outcome =",x["scientific_outcome"])
print("result =",x["actual_computed_result"])
print("blocker =",x.get("blocker"))
