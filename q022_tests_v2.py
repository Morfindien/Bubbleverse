#!/usr/bin/env python3
"""Mandatory validator for Bubbleverse Q022 V2."""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path

Q="Q022"
RUN="Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
RESULT="R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"

def write(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(t,p)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--result",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    r=json.loads(Path(a.result).read_text(encoding="utf-8"))
    rg=r.get("gates",{})
    final_vertices=r.get("final_vertices",[])
    allowed={
      "PRIMARILY_OPTIMIZER_GLOBALITY_OR_INCOMPLETE_MINIMIZATION_STRUCTURE",
      "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE",
      "IDENTIFIABILITY_LIMIT_MIXED_VERTEX_BEHAVIOUR",
      "IDENTIFIABILITY_LIMIT",
    }
    gates={
      "Q_IDENTITY_GATE": r.get("q")==Q,
      "RUN_IDENTITY_GATE": r.get("run_id")==RUN and r.get("result_id")==RESULT,
      "INTERNAL_GATE_SET_PASS": bool(rg) and all(bool(v) for v in rg.values()),
      "SELECTED_SCOPE_GATE": sorted(r.get("selected_masks",[]))==[3,6,7],
      "THREE_VERTEX_DECISION_GATE": len(final_vertices)==3,
      "FINITE_OBJECTIVE_DIAGNOSTIC_GATE": all(
          v.get("classification")!="INCOMPLETE"
          and math.isfinite(float(v.get("diagnostic",{}).get("objective_spread")))
          and math.isfinite(float(v.get("diagnostic",{}).get("max_pairwise_joint_rms")))
          for v in final_vertices
      ),
      "FINAL_CLASSIFICATION_GATE": r.get("classification") in allowed,
      "Q022_V1_PRESERVATION_GATE":
          r.get("q022_v1_preserved_classification")=="MIXED_COSMOLOGY_AND_NUISANCE_ASSOCIATION",
      "NO_PHYSICAL_OVERCLAIM_GATE":
          r.get("interpretation",{}).get("stable_multibasin_means_physical_distinct_solutions") is False,
      "NO_HIGHER_OBJECTIVE_ARTIFACT_SHORTCUT_GATE":
          r.get("interpretation",{}).get("higher_objective_alone_used_as_artifact_test") is False,
      "NO_CROSS_LIKELIHOOD_SUM_GATE":
          r.get("interpretation",{}).get("cross_likelihood_chi2_sum_performed") is False,
      "Q021_NOT_REOPENED_GATE":
          r.get("interpretation",{}).get("q021_distributed_classification_reopened") is False,
      "MOTOR14_STOP_ROUTE_GATE":
          r.get("journal_effect_if_pass",{}).get("q022_can_close") is True
          and "MOTOR 14" in r.get("journal_effect_if_pass",{}).get("next_engine",""),
    }
    final=all(gates.values())
    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"Q022_V2_MANDATORY_TESTS",
      "tests_status":"COMPLETE",
      "gates":gates,
      "FINAL_RESULT_GATE":"PASS" if final else "FAIL",
    }
    write(a.output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

if __name__=="__main__":
    raise SystemExit(main())
