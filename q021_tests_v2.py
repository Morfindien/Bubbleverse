#!/usr/bin/env python3
"""Mandatory Q021 V2 repair result tests."""
import argparse,json,os
from pathlib import Path

Q="Q021"
RUN="Q021-PRIMORDIAL-INTERNAL-STRUCTURE-REPAIR-V2"
RESULT="R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-002"

MANDATORY=(
 "Q_IDENTITY_GATE",
 "PARENT_RUN_IDENTITY_GATE",
 "Q020_PARENT_REPRODUCTION_GATE",
 "JOB_COMPLETENESS_GATE",
 "FINITE_RESULT_GATE",
 "LIKELIHOOD_STRUCTURAL_IDENTITY_GATE",
 "COHERENT_RESTART_DECOMPOSITION_GATE",
 "DECOMPOSITION_CLOSURE_GATE",
 "STRUCTURE_CLASS_STABILITY_GATE",
 "LOCALIZED_DOMINANT_IDENTITY_GATE",
 "NO_FRANKENSTEIN_VERTEX_MIXING_GATE",
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
 g=d.get("gates",{})
 t={
  "IDENTITY":d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
  "MANDATORY_GATES_PRESENT":all(k in g for k in MANDATORY),
  "MANDATORY_GATES_PASS":all(g.get(k) is True for k in MANDATORY),
  "FINAL_RESULT_GATE":d.get("FINAL_RESULT_GATE")=="PASS",
  "CLASSIFICATION_ALLOWED":d.get("classification") in (
    "PRIMORDIAL SINGLE-DIRECTION LOCALIZED",
    "PRIMORDIAL PAIR-COUPLING LOCALIZED",
    "PRIMORDIAL THREE-WAY / DISTRIBUTED COUPLING",
    "LIKELIHOOD-CONSTRUCTION-DEPENDENT PRIMORDIAL GEOMETRY",
    "INDETERMINATE — NUMERICAL OR IDENTIFIABILITY LIMIT",
  ),
  "NO_FRANKENSTEIN_AUTHORITY":
    d.get("repair",{}).get("v1_best_per_vertex_decomposition_authoritative") is False,
  "NO_HASH_FALSE_IDENTITY":
    d.get("repair",{}).get("v1_likelihood_spec_hash_gate_authoritative") is False,
  "BASIN_SPREAD_PRESERVED":
    "optimizer_basin_diagnostics" in d,
  "NO_CAUSAL_OVERCLAIM":
    d.get("rules",{}).get("causal_systematic_claim") is False
    and d.get("rules",{}).get("new_physics_claim") is False,
  "NO_INDEPENDENCE_OVERCLAIM":
    d.get("rules",{}).get("matched_and_full_mf_are_independent_observations") is False,
 }
 final=all(t.values())
 o={
   "q":Q,"run_id":RUN,"result_id":RESULT,
   "stage":"Q021_V2_MANDATORY_TESTS",
   "status":"PASS" if final else "FAIL",
   "tests":t,
   "mandatory_parent_gates":{k:g.get(k) for k in MANDATORY},
 }
 write(a.output,o)
 print(json.dumps(o,indent=2,sort_keys=True))
 return 0 if final else 2

if __name__=="__main__":
 raise SystemExit(main())
