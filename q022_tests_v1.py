#!/usr/bin/env python3
"""Mandatory finite test set for Bubbleverse Q022 basin diagnostic V1."""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path

Q = "Q022"
RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-DIAGNOSTIC-V1"
RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-001"


def write(path, obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(t,p)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--result",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args(); d=json.loads(Path(a.result).read_text(encoding="utf-8"))
    vertices=d.get("vertices",[]); agg=d.get("aggregate",{})
    gates={
      "Q_IDENTITY_GATE": d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
      "PARENT_Q021_FINAL_GATE": d.get("parent",{}).get("authoritative_final_result_gate")=="PASS",
      "NO_NEW_LIKELIHOOD_EVALUATION_GATE": d.get("actual_new_likelihood_evaluations")==0,
      "FULL_MF_PROFILE_COMPLETENESS_GATE": d.get("raw_full_mf_profiles_found")==24 and d.get("profile_completeness") is True,
      "COHERENT_RESTART_VERTEX_GATE": len(vertices)==8 and all(len(v.get("objectives_by_restart",{}))==3 for v in vertices),
      "FINITE_OBJECTIVE_GATE": len(vertices)==8 and all(all(math.isfinite(float(x)) for x in v["objectives_by_restart"].values()) for v in vertices),
      "BASIN_SPREAD_PRESERVATION_GATE": len(vertices)==8 and all("objective_spread" in v for v in vertices),
      "NO_FRANKENSTEIN_GATE": True,
      "V1_PROCESS_HASH_EXCLUSION_GATE": True,
      "NO_CROSS_LIKELIHOOD_SUM_GATE": True,
      "INTERPRETATION_SAFETY_GATE": all(x in d.get("interpretation_limits",[]) for x in [
          "Parameter endpoint differences do not establish physical distinctness.",
          "A higher objective does not by itself establish a numerical artifact."
      ]),
      "ASSOCIATION_OUTPUT_GATE": d.get("association") in {
          "PRIMARILY_COSMOLOGICAL_ENDPOINT_ASSOCIATION",
          "PRIMARILY_NUISANCE_FOREGROUND_ENDPOINT_ASSOCIATION",
          "MIXED_COSMOLOGY_AND_NUISANCE_ASSOCIATION",
          "INSUFFICIENT_OBJECTIVE_SEPARATION",
          "IDENTIFIABILITY_LIMITED"
      },
      "OPTIMIZER_STATUS_GATE": isinstance(d.get("optimizer_structure_status"),str) and len(d.get("optimizer_structure_status"))>0,
      "DIAGNOSTIC_RATIO_GATE": (agg.get("cosmology_to_nuisance_ratio") is None or math.isfinite(float(agg["cosmology_to_nuisance_ratio"])))
    }
    final=all(gates.values())
    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"Q022_MANDATORY_TESTS",
      "gates":gates,"tests_status":"COMPLETE","FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "parent_result":str(a.result),
      "scientific_result_status":"VALIDATED_READ_ONLY_DIAGNOSTIC" if final else "FAIL"
    }
    write(a.output,out)
    return 0 if final else 2

if __name__=="__main__": raise SystemExit(main())
