#!/usr/bin/env python3
"""Bubbleverse CASE-031 V1 validation and certification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT=Path(__file__).resolve().parent
Q="CASE-031"
RUN="CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1"
RESULT="R-CASE031-EDE-PLANCK-PORTABILITY-001"
HILLIPOP_COMMIT="a09ddde3e7ce11df99f74685feb1f1764cafb251"
BACKEND_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"

def read_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def write_json(p,obj):
    Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def canon(obj: Any) -> str:
    return hashlib.sha256(json.dumps(
        obj,sort_keys=True,separators=(",",":"),default=str
    ).encode()).hexdigest()

def static(output: str) -> int:
    c=yaml.safe_load((ROOT/"q031_planck_portability_v1_config.yml").read_text(encoding="utf-8"))
    s=read_json(ROOT/"q031_source_lock_v1.json")
    p=read_json(ROOT/"q031_protocol_lock_v1.json")
    x=dict(p); declared=x.pop("protocol_sha256")
    gates={
      "Q_IDENTITY_GATE":
        c["project"]["q"]==Q and s["q"]==Q and p["q"]==Q,
      "RUN_IDENTITY_GATE":
        c["project"]["run_id"]==RUN and s["run_id"]==RUN and p["run_id"]==RUN,
      "RESULT_IDENTITY_GATE":
        c["project"]["result_id"]==RESULT and s["result_id"]==RESULT,
      "BACKEND_COMMIT_GATE":
        c["model"]["backend_commit"]==BACKEND_COMMIT
        and s["bubbleverse"]["backend"]["commit"]==BACKEND_COMMIT,
      "HILLIPOP_COMMIT_GATE":
        c["independent_likelihood"]["commit"]==HILLIPOP_COMMIT
        and s["independent_likelihood"]["commit"]==HILLIPOP_COMMIT
        and p["independent_likelihood"]["commit"]==HILLIPOP_COMMIT,
      "PROTOCOL_HASH_GATE": declared==canon(x),
      "NO_CROSS_LIKELIHOOD_CHI2_GATE":
        c["rules"]["no_cross_likelihood_chi2_sum"] is True
        and c["rules"]["no_cross_likelihood_absolute_objective_subtraction"] is True,
      "NO_FORCED_NUISANCE_MAPPING_GATE":
        c["rules"]["no_forced_nuisance_mapping"] is True,
      "Q030_TOLERANCE_PRESERVATION_GATE":
        float(c["parents"]["q030"]["inherited_precision_floor"])==2.0e-4
        and float(c["coupling_test"]["inherited_numerical_resolution_floor"])==2.0e-4,
      "CORE_DATASET_SCOPE_GATE":
        c["independent_likelihood"]["core_only_high_l"] is True
        and c["independent_likelihood"]["add_low_l"] is False
        and c["independent_likelihood"]["add_lensing"] is False
        and c["independent_likelihood"]["add_ACT"] is False
        and c["independent_likelihood"]["add_SPT"] is False,
    }
    ok=all(gates.values())
    rec={"q":Q,"run_id":RUN,"stage":"Q031_STATIC_VALIDATION",
         "status":"PASS" if ok else "FAIL","gates":gates}
    write_json(output,rec)
    return 0 if ok else 2

def validate(result_path: str, output: str) -> int:
    d=read_json(result_path)
    gates={
      "Q_IDENTITY_GATE": d.get("q")==Q,
      "RUN_IDENTITY_GATE": d.get("run_id")==RUN,
      "RESULT_IDENTITY_GATE": d.get("result_id")==RESULT,
      "FINAL_STAGE_GATE": d.get("stage")=="Q031_FINAL",
      "CLAIM_BOUNDARY_GATE":
        d.get("claim_boundaries",{}).get("physical_causality_claimed") is False
        and d.get("claim_boundaries",{}).get("instrumental_systematic_proven") is False
        and d.get("claim_boundaries",{}).get("new_physics_detected") is False
        and d.get("claim_boundaries",{}).get("cross_likelihood_chi2_sum_performed") is False,
      "NONCOMPARABLE_LIST_GATE": bool(d.get("non_comparable_quantities")),
      "RETURN_ROUTE_GATE": d.get("return_route")=="RESULT INGESTION & ROUTING ENGINE",
    }

    verdict=d.get("portability_verdict")
    cls=d.get("final_classification")
    core=d.get("core_gates",{})
    if verdict=="PORTABILITY_SURVIVES":
        semantic=(
          cls=="PRESERVE"
          and core.get("INDEPENDENT_IMPLEMENTATION_GATE")=="PASS"
          and core.get("MATERIAL_STABLE_MULTIBASIN_GATE")=="PASS"
          and core.get("DISTRIBUTED_PRIMORDIAL_RESPONSE_GATE")=="PASS"
          and core.get("NO_SINGLE_UNIVERSAL_BASIN_DIRECTION_GATE")=="PASS"
          and core.get("CONSTRUCTION_DEPENDENT_COMPENSATION_GATE")=="PASS"
          and d.get("geometry_classification")
             =="CROSS-IMPLEMENTATION PLANCK n=3 EDE LIKELIHOOD GEOMETRY"
        )
    elif verdict=="PORTABILITY_FAILS":
        semantic=(
          cls=="DOWNGRADE"
          and core.get("INDEPENDENT_IMPLEMENTATION_GATE")=="PASS"
          and d.get("scientific_nonportability") is True
          and d.get("geometry_classification")
             =="IMPLEMENTATION-SPECIFIC INTERNAL LIKELIHOOD GEOMETRY"
        )
    elif verdict=="PORTABILITY_QUALIFIED":
        semantic=(cls=="QUALIFY" and d.get("scientific_nonportability") is False)
    elif verdict=="UNRESOLVED_IMPLEMENTATION_FAILURE":
        semantic=(
          cls=="QUALIFY"
          and d.get("scientific_nonportability") is False
          and core.get("INDEPENDENT_IMPLEMENTATION_GATE")=="FAIL"
        )
    else:
        semantic=False

    gates["SCIENTIFIC_VERDICT_SEMANTICS_GATE"]=semantic

    # A failed hypothesis is a valid final scientific result. These gates validate
    # execution/interpretation, not whether portability itself survived.
    if core.get("INDEPENDENT_IMPLEMENTATION_GATE")=="PASS":
        gates["PRIMARY_NUMERICAL_RESULT_GATE"] = (
            d.get("primary",{}).get("status")=="PASS"
            and d.get("primary",{}).get("actual_computed_result") is True
        )
    else:
        gates["PRIMARY_NUMERICAL_RESULT_GATE"] = (
            verdict=="UNRESOLVED_IMPLEMENTATION_FAILURE"
        )

    # If multibasin survives, primordial must either be validly computed or the
    # final verdict must remain qualified rather than pretending full survival.
    if core.get("MATERIAL_STABLE_MULTIBASIN_GATE")=="PASS":
        if verdict=="PORTABILITY_SURVIVES":
            gates["PRIMORDIAL_REQUIRED_FOR_SURVIVAL_GATE"]=(
                isinstance(d.get("primordial"),Mapping)
                and d["primordial"].get("status")=="PASS"
            )
        else:
            gates["PRIMORDIAL_REQUIRED_FOR_SURVIVAL_GATE"]=True
    else:
        gates["PRIMORDIAL_REQUIRED_FOR_SURVIVAL_GATE"]=True

    ok=all(gates.values())
    rec={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"Q031_RESULT_VALIDATION",
      "status":"PASS" if ok else "FAIL",
      "validated_portability_verdict":verdict,
      "validated_final_classification":cls,
      "gates":gates,
      "negative_scientific_result_is_valid_if_technically_valid":True,
    }
    write_json(output,rec)
    return 0 if ok else 2

def certify(result_path: str, validation_path: str, output: str) -> int:
    d=read_json(result_path)
    v=read_json(validation_path)
    if v.get("status")!="PASS":
        raise SystemExit("VALIDATION_GATE=FAIL")
    d["validation_status"]="COMPLETE"
    d["FINAL_RESULT_GATE"]="PASS"
    d["result_test_plan_status"]="COMPLETE"
    d["validation"]=v
    d["final_result_status"]="PASS"
    write_json(output,d)
    print("FINAL_RESULT_GATE=PASS")
    print("PORTABILITY_VERDICT="+str(d.get("portability_verdict")))
    return 0

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("static"); p.add_argument("--output",required=True)
    p=sub.add_parser("validate")
    p.add_argument("--result",required=True); p.add_argument("--output",required=True)
    p=sub.add_parser("certify")
    p.add_argument("--result",required=True)
    p.add_argument("--validation",required=True)
    p.add_argument("--output",required=True)
    a=ap.parse_args()
    if a.cmd=="static": return static(a.output)
    if a.cmd=="validate": return validate(a.result,a.output)
    if a.cmd=="certify": return certify(a.result,a.validation,a.output)
    return 2

if __name__=="__main__":
    raise SystemExit(main())
