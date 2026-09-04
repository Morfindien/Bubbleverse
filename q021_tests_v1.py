#!/usr/bin/env python3
"""Mandatory finite Q021 result tests."""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path

Q="Q021"
RUN="Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
RESULT="R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"

MANDATORY = (
    "Q_IDENTITY_GATE",
    "MODEL_IDENTITY_GATE",
    "Q020_PARENT_REPRODUCTION_GATE",
    "JOB_COMPLETENESS_GATE",
    "FINITE_RESULT_GATE",
    "VERTEX_GRID_COMPLETENESS_GATE",
    "ENDPOINT_IDENTITY_GATE",
    "LIKELIHOOD_OBJECT_IDENTITY_GATE",
    "DECOMPOSITION_CLOSURE_GATE",
    "MULTISTART_OBJECTIVE_STABILITY_GATE",
    "MULTISTART_RANKING_STABILITY_GATE",
    "EQUIVALENT_INTERVENTION_SEMANTICS_GATE",
    "NO_CROSS_CHAIN_CHI2_SUM_GATE",
    "INTERPRETATION_SAFETY_GATE",
)

def write(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    os.replace(t,p)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--merged",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    d=json.loads(Path(a.merged).read_text())
    gates=d.get("gates",{})
    tests={
      "IDENTITY": d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
      "MANDATORY_GATES_PRESENT": all(k in gates for k in MANDATORY),
      "MANDATORY_GATES_PASS": all(gates.get(k) is True for k in MANDATORY),
      "FINAL_RESULT_GATE": d.get("FINAL_RESULT_GATE")=="PASS",
      "CLASSIFICATION_ALLOWED": d.get("classification") in (
        "PRIMORDIAL SINGLE-DIRECTION LOCALIZED",
        "PRIMORDIAL PAIR-COUPLING LOCALIZED",
        "PRIMORDIAL THREE-WAY / DISTRIBUTED COUPLING",
        "LIKELIHOOD-CONSTRUCTION-DEPENDENT PRIMORDIAL GEOMETRY",
        "INDETERMINATE — NUMERICAL OR IDENTIFIABILITY LIMIT",
      ),
      "NO_CAUSAL_OVERCLAIM":
        d.get("rules",{}).get("causal_systematic_claim") is False
        and d.get("rules",{}).get("new_physics_claim") is False,
      "NO_INDEPENDENCE_OVERCLAIM":
        d.get("rules",{}).get("matched_and_full_mf_are_independent_observations") is False,
      "NO_CROSS_CHAIN_SUM":
        d.get("rules",{}).get("cross_chain_chi2_sum_performed") is False,
    }
    final=all(tests.values())
    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"Q021_MANDATORY_TESTS",
      "status":"PASS" if final else "FAIL",
      "tests":tests,
      "mandatory_parent_gates":{k:gates.get(k) for k in MANDATORY},
    }
    write(a.output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

if __name__=="__main__":
    raise SystemExit(main())
