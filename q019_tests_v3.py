#!/usr/bin/env python3
import argparse,json
from pathlib import Path

Q="Q019"
RUN="Q019-PLANCK-COSMOLOGY-GLOBALITY-V3"
RESULT="R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-003"
SHIFT="LIKELIHOOD CHOICE SHIFTS PREFERRED MOD-EDE-N3 REGION"
LOCAL="LIKELIHOOD DEPENDENCE PRIMARILY HIGH-H0 / LOCAL-GEOMETRY"
INDET="INDETERMINATE"
CROSS_THRESHOLD=1.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--merged",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    d=json.loads(Path(a.merged).read_text())
    g=dict(d.get("gates",{}))
    g["Q_IDENTITY_GATE"]=(d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT)

    base_gate_names=[
      "Q_IDENTITY_GATE","JOB_COMPLETENESS_GATE","FULL_MF_FREE_GLOBALITY_STABILITY_GATE",
      "PARENT_BEST_NONREGRESSION_GATE","Q016_ENDPOINT_OBJECTIVE_REPRODUCTION_GATE",
      "Q016_ENDPOINT_PENALTY_REPRODUCTION_GATE","NO_GATE_RELAXATION_GATE",
      "NO_CROSS_CHAIN_CHI2_SUM_GATE","Q018_GAP_NONPHYSICAL_GATE","V1_OTHER_GATES_PRESERVED_GATE"
    ]
    base_pass=all(g.get(k) is True for k in base_gate_names)

    pv=d.get("parent_v1",{})
    try:
        cross_costs=[float(pv["cross_cost_target_lite"]),float(pv["cross_cost_target_full_mf"])]
        cross_ok=all(x==x and abs(x)!=float("inf") for x in cross_costs)
    except Exception:
        cross_costs=[]
        cross_ok=False

    if not base_pass:
        expected=INDET
    elif cross_ok and any(x>CROSS_THRESHOLD for x in cross_costs):
        expected=SHIFT
    elif cross_ok:
        expected=LOCAL
    else:
        expected=INDET

    rule=d.get("classification_rule",{})
    g["FROZEN_V1_CLASSIFICATION_RULE_GATE"]=(
        cross_ok
        and d.get("classification")==expected
        and rule.get("source")=="FROZEN_Q019_V1_RULE"
        and float(rule.get("cross_profile_materiality_threshold",-999))==CROSS_THRESHOLD
        and rule.get("threshold_is_statistical_significance") is False
    )
    g["CLASSIFICATION_GATE"]=g["FROZEN_V1_CLASSIFICATION_RULE_GATE"]

    interp=d.get("interpretation",{})
    g["INTERPRETATION_SAFETY_GATE"]=(
      interp.get("causal_systematic_claim_allowed") is False
      and interp.get("new_physics_claim_allowed") is False
      and interp.get("q018_architecture_gap_used_as_physical_component") is False
      and interp.get("cross_chain_chi2_sum_performed") is False
    )

    mandatory=[
      "Q_IDENTITY_GATE","JOB_COMPLETENESS_GATE","FULL_MF_FREE_GLOBALITY_STABILITY_GATE",
      "PARENT_BEST_NONREGRESSION_GATE","Q016_ENDPOINT_OBJECTIVE_REPRODUCTION_GATE",
      "Q016_ENDPOINT_PENALTY_REPRODUCTION_GATE","NO_GATE_RELAXATION_GATE",
      "NO_CROSS_CHAIN_CHI2_SUM_GATE","Q018_GAP_NONPHYSICAL_GATE","V1_OTHER_GATES_PRESERVED_GATE",
      "FROZEN_V1_CLASSIFICATION_RULE_GATE","CLASSIFICATION_GATE","INTERPRETATION_SAFETY_GATE"
    ]

    final=all(g.get(k) is True for k in mandatory)
    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,"test_type":"MANDATORY_RESULT_TESTS_V3",
      "gates":g,"mandatory":mandatory,"FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "classification":d.get("classification"),
      "expected_classification_from_frozen_v1_rule":expected,
      "cross_profile_materiality_threshold":CROSS_THRESHOLD,
      "threshold_is_statistical_significance":False
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

if __name__=="__main__":
    raise SystemExit(main())
