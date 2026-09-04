#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

Q="Q020"
RUN="Q020-PLANCK-CROSS-PROFILE-DIRECTION-V1"
RESULT="R-Q020-EDE-PLANCK-CROSS-PROFILE-DIRECTION-001"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--merged",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    d=json.loads(Path(a.merged).read_text())

    gates={
      "Q_IDENTITY_GATE": d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT,
      "PARENT_FINAL_GATE": d.get("FINAL_RESULT_GATE")=="PASS",
      "JOB_COMPLETENESS_GATE": d.get("gates",{}).get("JOB_COMPLETENESS_GATE") is True,
      "VERTEX_GRID_COMPLETENESS_GATE": d.get("gates",{}).get("VERTEX_GRID_COMPLETENESS_GATE") is True,
      "NUISANCE_RESTART_STABILITY_GATE": d.get("gates",{}).get("NUISANCE_RESTART_STABILITY_GATE") is True,
      "Q019_CROSS_FULL_MF_REPRODUCTION_GATE": d.get("gates",{}).get("Q019_CROSS_FULL_MF_REPRODUCTION_GATE") is True,
      "Q019_CROSS_LITE_REPRODUCTION_GATE": d.get("gates",{}).get("Q019_CROSS_LITE_REPRODUCTION_GATE") is True,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE": d.get("rules",{}).get("cross_chain_chi2_sum_performed") is False,
      "Q018_GAP_NONPHYSICAL_GATE": d.get("rules",{}).get("q018_architecture_gap_used_as_physical_component") is False,
      "NONINDEPENDENT_ATTRIBUTION_GATE": d.get("rules",{}).get("shapley_values_are_independent_chi2_components") is False,
      "NO_CAUSAL_SYSTEMATIC_GATE": d.get("rules",{}).get("causal_systematic_claim") is False,
      "NO_NEW_PHYSICS_GATE": d.get("rules",{}).get("new_physics_claim") is False,
    }
    final=all(gates.values())
    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "test_type":"MANDATORY_RESULT_TESTS",
      "gates":gates,
      "FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "classification":d.get("classification") if final else "UNRESOLVED"
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

if __name__=="__main__":
    raise SystemExit(main())
