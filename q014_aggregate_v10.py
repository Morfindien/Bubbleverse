#!/usr/bin/env python3
"""Aggregate Q014 V10 basin-replication jobs using the cross-mode-comparable profile deviance."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import yaml
from q014_external_viability_v10 import impl
ROOT=Path(__file__).resolve().parent
CONFIG_NAME="q014_external_viability_v10_config.yml"
RUN="Q014-EXTERNAL-VIABILITY-V10"
BASIS="SCALAR_TOTAL_LIKELIHOOD_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_CONSTRAINT_SHAPES"

def load_cfg(p=CONFIG_NAME):
    p=Path(p); p=p if p.is_absolute() else ROOT/p
    return yaml.safe_load(p.read_text())
def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
def load_records(paths):
    out=[]
    for raw in paths:
        p=Path(raw); fs=list(p.rglob("*.json")) if p.is_dir() else [p]
        for f in fs:
            try:d=json.loads(f.read_text())
            except Exception:continue
            if d.get("q")=="Q014" and d.get("run_id")==RUN and "mode" in d:
                d["_source_file"]=str(f); out.append(d)
    return out
def finite(r):
    try:return r.get("status")=="COMPLETE" and math.isfinite(float(r["objective_chi2"])) and r.get("objective_basis")==BASIS
    except Exception:return False
def spread(rows):
    xs=sorted(float(r["objective_chi2"]) for r in rows if finite(r)); return xs[1]-xs[0] if len(xs)>=2 else None

def aggregate(records,c,depth):
    expected=impl.expected_tasks(c,depth); key=lambda x:(x["chain"],x["mode"],x["start_family"]); ek={key(x) for x in expected}; rk={key(x) for x in records}
    missing=sorted(ek-rk); dupes=sorted(k for k in rk if sum(1 for r in records if key(r)==k)>1)
    source={}
    for chain in c["chains"]:
        hs=sorted({str(r.get("runtime_source_provenance_sha256")) for r in records if r.get("chain")==chain and finite(r) and r.get("runtime_source_provenance_sha256")}); source[chain]=hs
    source_ok=all(len(v)==1 for v in source.values())
    result={"case_id":c["project"]["case_id"],"q":"Q014","run_id":RUN,"result_id":c["project"]["result_id"],"original_case_question":c["project"]["original_case_question"],
      "program_status":"V10 V8-BASIN REPLICATION RESULTS AGGREGATED","depth":depth,"q011_globality_status_preserved":c["claim_boundary"]["q011_globality_status_preserved"],
      "absolute_chi2_cross_package_comparison_performed":False,"planck_spt_chi2_sum_performed":False,"objective_basis":c["scientific_surface"]["optimizer_basis"],"chains":{},
      "v8_numerical_parent":c["parent"]["v8"],"job_manifest":{"expected":len(ek),"returned":len(rk),"missing":missing,"duplicates":dupes,"runtime_source_provenance_hashes_by_chain":source,"runtime_source_compatible":source_ok},
      "validation_status":"PARTIAL","scientifically_usable_result":False,"next_action_required":True}
    minv=int(c["validation"]["minimum_valid_starts_per_profile"]); maxsp=float(c["validation"]["max_best_two_delta_chi2"]); neg=float(c["validation"]["fixed_vs_free_negative_tolerance"])
    for chain,spec in c["chains"].items():
        cr={"label":spec["label"],"role":spec["role"],"paper_native_reproduction":spec.get("paper_native_reproduction",False),"profiles":{},"penalties":{},"status":"PARTIAL"}
        for mode in c["execution"]["modes"]:
            rows=[r for r in records if r.get("chain")==chain and r.get("mode")==mode]; good=sorted([r for r in rows if finite(r)],key=lambda r:float(r["objective_chi2"])); sp=spread(good); needed=1 if mode=="q011_shared_physics" else minv
            stable=len(good)>=needed and (mode=="q011_shared_physics" or (sp is not None and sp<=maxsp)); seedpass=bool(good) and all(r.get("seed_candidate_preservation_pass") is True for r in good)
            cr["profiles"][mode]={"returned_jobs":len(rows),"finite_jobs":len(good),"minimum_required":needed,"best_objective_chi2":float(good[0]["objective_chi2"]) if good else None,"best_record":good[0] if good else None,"best_two_delta_chi2":sp,"stable":stable,"seed_candidate_preservation_pass":seedpass,"status":"VALIDATED" if stable and seedpass else ("NUMERICALLY_UNRESOLVED" if good else "TECHNICAL_FAILURE")}
        ref=cr["profiles"]["reference_free_h0"]["best_objective_chi2"]; fix=cr["profiles"]["fixed_h0_71p5"]["best_objective_chi2"]; sh=cr["profiles"]["q011_shared_physics"]["best_objective_chi2"]
        if ref is not None and fix is not None:
            d=float(fix)-float(ref); cr["penalties"]["fixed_h0_profile_delta_chi2"]=d; cr["penalties"]["fixed_profile_monotonicity_pass"]=d>=-neg
        else: cr["penalties"]["fixed_h0_profile_delta_chi2"]=None; cr["penalties"]["fixed_profile_monotonicity_pass"]=False
        cr["penalties"]["q011_shared_physics_delta_chi2"]=float(sh)-float(ref) if ref is not None and sh is not None else None
        req=all(p["status"]=="VALIDATED" for p in cr["profiles"].values()); cr["status"]="VALIDATED" if req and cr["penalties"]["fixed_profile_monotonicity_pass"] else "NUMERICALLY_UNRESOLVED"; result["chains"][chain]=cr
    primary=c["validation"]["required_primary_chains"]; primary_ok=all(result["chains"][x]["status"]=="VALIDATED" for x in primary); jobs_ok=not missing and not dupes and source_ok
    if primary_ok and jobs_ok:
        result["validation_status"]="VALIDATED WITH CAVEATS"; result["scientifically_usable_result"]=True; result["next_action_required"]=False; result["case_question_answer_status"]="YES, WITH CAVEATS"
    elif primary_ok: result["validation_status"]="PARTIAL"; result["case_question_answer_status"]="PARTIALLY"
    else: result["validation_status"]="NUMERICALLY UNRESOLVED"; result["case_question_answer_status"]="NO"
    result["claim_boundary"]={"planck_branch_is_k039_approximation":True,"spt_only_is_primary_independentish_test":True,"spt_plus_desi_is_secondary_and_partially_overlapping":True,"no_cross_chain_absolute_chi2_interpretation":True,"q011_is_not_promoted_to_global":True,"v8_not_interpreted_as_scientific_result":True,"flat_prior_normalization_constants_excluded_from_cross_mode_delta":True}
    result["journal_update"]={"case_id":c["project"]["case_id"],"q":"Q014","program":"q014_external_viability_v10.py","workflow":"q014-external-viability-v10.yml","validation_status":result["validation_status"],"what_was_computed":"V10 cross-mode-comparable external n=3 profile deviance with V8 two-basin exact+jitter replication certification.","scientific_consequence":"Interpret only after mandatory V10 validation passes; report each chain separately.","what_remains_unresolved":[] if result["scientifically_usable_result"] else ["One or more primary V10 basin-replication profiles remain numerically unstable or fail nesting monotonicity."],"next_required_action":"ROUTE_VALIDATED_Q014_RESULT" if result["scientifically_usable_result"] else "CONTINUE_NUMERICAL_CERTIFICATION"}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default=CONFIG_NAME); ap.add_argument("--depth",choices=["standard","expanded"],default="standard"); ap.add_argument("--inputs",nargs="+",required=True); ap.add_argument("--output",required=True); ap.add_argument("--manifest-output",required=True); a=ap.parse_args(); c=load_cfg(a.config); r=aggregate(load_records(a.inputs),c,a.depth); dump(a.output,r); dump(a.manifest_output,r["job_manifest"]); print(json.dumps({"validation_status":r["validation_status"],"jobs":r["job_manifest"]},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
