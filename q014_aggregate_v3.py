#!/usr/bin/env python3
"""Aggregate Q014 independent profile jobs without mixing likelihood normalizations."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT=Path(__file__).resolve().parent
CONFIG_NAME="q014_external_viability_v3_config.yml"


def load_cfg(path: str|Path=CONFIG_NAME)->dict[str,Any]:
    p=Path(path)
    if not p.is_absolute(): p=ROOT/p
    return yaml.safe_load(p.read_text())


def dump(path: str|Path, obj: Any)->None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")


def load_records(paths:list[str])->list[dict[str,Any]]:
    out=[]
    for raw in paths:
        p=Path(raw)
        candidates=list(p.rglob("*.json")) if p.is_dir() else [p]
        for f in candidates:
            try: d=json.loads(f.read_text())
            except Exception: continue
            if d.get("q")=="Q014" and d.get("run_id")=="Q014-EXTERNAL-VIABILITY-V3" and "mode" in d:
                d["_source_file"]=str(f); out.append(d)
    return out


def finite(r:Mapping[str,Any])->bool:
    try: return r.get("status")=="COMPLETE" and math.isfinite(float(r["objective_chi2"]))
    except Exception: return False


def best_two_spread(rows:list[Mapping[str,Any]])->float|None:
    vals=sorted(float(r["objective_chi2"]) for r in rows if finite(r))
    return vals[1]-vals[0] if len(vals)>=2 else None


def aggregate(records:list[dict[str,Any]], c:Mapping[str,Any], depth:str)->dict[str,Any]:
    from q014_external_viability_v3 import expected_tasks
    expected=expected_tasks(c,depth)
    key=lambda x:(x["chain"],x["mode"],x["start_family"])
    expected_keys={key(x) for x in expected}
    returned_keys={key(x) for x in records}
    dupes=sorted(k for k in returned_keys if sum(1 for r in records if key(r)==k)>1)
    missing=sorted(expected_keys-returned_keys)
    source_hashes_by_chain={}
    for chain in c["chains"]:
        hashes=sorted({str(r.get("runtime_source_provenance_sha256")) for r in records
                       if r.get("chain")==chain and finite(r) and r.get("runtime_source_provenance_sha256")})
        source_hashes_by_chain[chain]=hashes
    source_compatible=all(len(v)==1 for v in source_hashes_by_chain.values())

    result={
      "case_id":c["project"]["case_id"],"q":"Q014","run_id":"Q014-EXTERNAL-VIABILITY-V3",
      "result_id":c["project"]["result_id"],"original_case_question":c["project"]["original_case_question"],
      "program_status":"EXECUTION RESULTS AGGREGATED","depth":depth,
      "q011_globality_status_preserved":c["claim_boundary"]["q011_globality_status_preserved"],
      "absolute_chi2_cross_package_comparison_performed":False,
      "planck_spt_chi2_sum_performed":False,"chains":{},
      "job_manifest":{"expected":len(expected_keys),"returned":len(returned_keys),"missing":missing,"duplicates":dupes,
                      "runtime_source_provenance_hashes_by_chain":source_hashes_by_chain,"runtime_source_compatible":source_compatible},
      "validation_status":"PARTIAL","scientifically_usable_result":False,"next_action_required":True,
    }
    min_valid=int(c["validation"]["minimum_valid_starts_per_profile"])
    maxspread=float(c["validation"]["max_best_two_delta_chi2"])
    negtol=float(c["validation"]["fixed_vs_free_negative_tolerance"])

    for chain,spec in c["chains"].items():
        cr={"label":spec["label"],"role":spec["role"],"paper_native_reproduction":spec.get("paper_native_reproduction",False),
            "profiles":{},"status":"PARTIAL","penalties":{}}
        for mode in c["execution"]["modes"]:
            rows=[r for r in records if r.get("chain")==chain and r.get("mode")==mode]
            good=[r for r in rows if finite(r)]
            good=sorted(good,key=lambda r:float(r["objective_chi2"]))
            spread=best_two_spread(good)
            needed=1 if mode=="q011_shared_physics" else min_valid
            stable=(len(good)>=needed and (mode=="q011_shared_physics" or (spread is not None and spread<=maxspread)))
            cr["profiles"][mode]={
              "returned_jobs":len(rows),"finite_jobs":len(good),"minimum_required":needed,
              "best_objective_chi2":float(good[0]["objective_chi2"]) if good else None,
              "best_record":good[0] if good else None,
              "best_two_delta_chi2":spread,"stable":stable,
              "status":"VALIDATED" if stable else ("NUMERICALLY_UNRESOLVED" if good else "TECHNICAL_FAILURE")
            }
        ref=cr["profiles"]["reference_free_h0"]["best_objective_chi2"]
        fix=cr["profiles"]["fixed_h0_71p5"]["best_objective_chi2"]
        shared=cr["profiles"]["q011_shared_physics"]["best_objective_chi2"]
        if ref is not None and fix is not None:
            d=float(fix)-float(ref)
            cr["penalties"]["fixed_h0_profile_delta_chi2"]=d
            cr["penalties"]["fixed_profile_monotonicity_pass"]=d>=-negtol
        else:
            cr["penalties"]["fixed_h0_profile_delta_chi2"]=None
            cr["penalties"]["fixed_profile_monotonicity_pass"]=False
        if ref is not None and shared is not None:
            cr["penalties"]["q011_shared_physics_delta_chi2"]=float(shared)-float(ref)
        else:
            cr["penalties"]["q011_shared_physics_delta_chi2"]=None
        required_modes=all(cr["profiles"][m]["stable"] for m in cr["profiles"])
        cr["status"]="VALIDATED" if required_modes and cr["penalties"]["fixed_profile_monotonicity_pass"] else "NUMERICALLY_UNRESOLVED"
        result["chains"][chain]=cr

    primary=c["validation"]["required_primary_chains"]
    primary_ok=all(result["chains"][x]["status"]=="VALIDATED" for x in primary)
    complete_jobs=(not missing and not dupes and source_compatible)
    if primary_ok and complete_jobs:
        result["validation_status"]="VALIDATED WITH CAVEATS"
        result["scientifically_usable_result"]=True
        result["next_action_required"]=False
        result["case_question_answer_status"]="YES, WITH CAVEATS"
    elif primary_ok:
        result["validation_status"]="PARTIAL"
        result["case_question_answer_status"]="PARTIALLY"
    else:
        result["validation_status"]="NUMERICALLY UNRESOLVED"
        result["case_question_answer_status"]="NO"
    result["claim_boundary"]={
      "planck_branch_is_k039_approximation":True,
      "spt_only_is_primary_independentish_test":True,
      "spt_plus_desi_is_secondary_and_partially_overlapping":True,
      "no_cross_chain_absolute_chi2_interpretation":True,
      "q011_is_not_promoted_to_global":True,
    }
    result["journal_update"]={
      "case_id":c["project"]["case_id"],"q":"Q014",
      "what_was_computed":"Separate external n=3 profile likelihoods for Planck/NPIPE approximation, SPT-only, and secondary SPT+DESI; free-H0 reference, fixed-H0=71.5 reprofile, and exact-Q011-shared-physics test.",
      "program":"q014_external_viability_v3.py","workflow":"q014-external-viability-v3.yml",
      "validation_status":result["validation_status"],
      "scientific_consequence":"Use each chain's reported delta chi2 separately. No cross-package absolute-chi2 sum is licensed.",
      "what_remains_unresolved":([] if result.get("scientifically_usable_result") else ["One or more primary external profiles remain technically incomplete or numerically unstable."]),
      "next_required_action":("ROUTE_VALIDATED_Q014_RESULT" if result.get("scientifically_usable_result") else "RUN_EXPANDED_OR_REPAIR_FAILED_PRIMARY_TASKS_ONLY")
    }
    return result


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default=CONFIG_NAME)
    ap.add_argument("--depth",choices=["standard","expanded"],default="standard")
    ap.add_argument("--inputs",nargs="+",required=True); ap.add_argument("--output",required=True)
    ap.add_argument("--manifest-output",required=True); args=ap.parse_args()
    c=load_cfg(args.config); recs=load_records(args.inputs); result=aggregate(recs,c,args.depth)
    dump(args.output,result); dump(args.manifest_output,result["job_manifest"])
    print(json.dumps({"validation_status":result["validation_status"],"jobs":result["job_manifest"]},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
