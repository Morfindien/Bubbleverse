#!/usr/bin/env python3
"""Q016 V8 staged aggregation and primary endpoint certification."""
import argparse,json,math
from pathlib import Path
import yaml

Q="Q016"; RUN="Q016-MATCHED-CMB-SURFACE-V8"; RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-008"
BASIS="SCALAR_PRIMARY_CMB_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_SHAPE_LIKELIHOODS"
BRANCHES=("planck","spt","act")

def load(p):return json.loads(Path(p).read_text())
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def finite(x):
    try:return math.isfinite(float(x))
    except Exception:return False

def record_gate(d,branch,mode):
    if d.get("q")!=Q or d.get("run_id")!=RUN or d.get("result_id")!=RESULT:return False,"identity"
    if d.get("branch")!=branch or d.get("mode")!=mode:return False,"branch/mode"
    if d.get("status")!="COMPLETE":return False,"not-complete"
    if d.get("objective_basis")!=BASIS:return False,"objective-basis"
    if d.get("exact_optimizer_objective_gate") is not True:return False,"exact-objective"
    if d.get("objective_component_gate") is not True or d.get("objective_self_consistency_gate") is not True:return False,"objective-components"
    if d.get("seed_candidate_preservation_pass") is not True:return False,"seed-preservation"
    if d.get("model_backend_commit")!="5a131c91d657dd9a7c6364cc45b038710f8d0d97":return False,"backend"
    if d.get("ell_range")!=[600,2000] or d.get("observables")!=["TT","TE","EE"]:return False,"surface"
    if not finite(d.get("objective_chi2")):return False,"finite"
    if d.get("cross_chain_chi2_sum_performed") is not False:return False,"cross-chain"
    if mode=="fixed_h0_71p5" and abs(float(d.get("target_h0",999))-71.5)>1e-8:return False,"H0"
    if mode=="reference_free_h0" and d.get("target_h0") is not None:return False,"free-H0"
    return True,"pass"

def profile(records,cfg):
    threshold=float(cfg["execution"]["continuation"]["multistart_delta_objective_max"])
    min_complete=int(cfg["execution"]["continuation"]["minimum_distinct_complete_restarts"])
    minrep=int(cfg["execution"]["continuation"]["minimum_replicates_within_delta_objective"])
    records=sorted(records,key=lambda x:float(x["objective_chi2"]))
    ids=sorted(int(x["restart"]) for x in records)
    complete=len(set(ids))>=min_complete
    if records:
        best=float(records[0]["objective_chi2"])
        near=[x for x in records if float(x["objective_chi2"])-best<=threshold]
        nearids=sorted(int(x["restart"]) for x in near)
        stable=len(set(nearids))>=minrep
        spread=(float(records[1]["objective_chi2"])-best) if len(records)>1 else float("inf")
    else:
        best=None;near=[];nearids=[];stable=False;spread=float("inf")
    return {
        "all":records,"best_record":records[0] if records else None,
        "complete_count":len(records),"distinct_restart_ids":ids,
        "complete_gate":complete,"best_two_spread":spread,
        "replicate_restart_ids_within_delta_objective":nearids,
        "replicate_count_within_delta_objective":len(nearids),
        "stable":stable,
    }

def collect(root,branch,mode):
    out=[];excluded=[]
    for p in sorted(Path(root).glob(f"{branch}_{mode}_*.json")):
        try:d=load(p)
        except Exception as e:excluded.append({"file":p.name,"reason":"parse","error":repr(e)});continue
        ok,why=record_gate(d,branch,mode)
        if ok:out.append(d)
        else:excluded.append({"file":p.name,"reason":why,"status":d.get("status")})
    # Duplicate restart IDs are forbidden within a mode/stage.
    ids=[int(x["restart"]) for x in out]
    if len(ids)!=len(set(ids)):raise RuntimeError(f"DUPLICATE_RESTART_GATE=FAIL {branch} {mode}")
    return out,excluded

def fixed_summary(a,cfg):
    result={"case_id":cfg["project"]["case_id"],"q":Q,"original_case_question":cfg["scientific_question"],
            "run_id":RUN,"result_id":RESULT,"stage":"PHASE1_FIXED_SUMMARY",
            "status":"PASS","branches":{},"excluded_records":[]}
    all_complete=True
    for b in BRANCHES:
        recs,ex=collect(a.input_dir,b,"fixed_h0_71p5")
        pr=profile(recs,cfg); result["branches"][b]=pr; result["excluded_records"]+=ex
        all_complete &= pr["complete_gate"]
    result["status"]="PASS" if all_complete else "FAIL"
    dump(a.output,result)
    if not all_complete:raise SystemExit(2)

def final(a,cfg):
    fixed=load(a.phase1_summary)
    if fixed.get("q")!=Q or fixed.get("run_id")!=RUN or fixed.get("stage")!="PHASE1_FIXED_SUMMARY":
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL")
    if fixed.get("status")!="PASS":raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL status")
    tolneg=float(cfg["execution"]["continuation"]["fixed_vs_free_negative_tolerance"])
    embedtol=float(cfg["execution"]["continuation"]["embedding_equivalence_tolerance"])
    branches={};gates={};excluded=[]
    for b in BRANCHES:
        fixed_pr=fixed["branches"][b]
        freerecs,ex=collect(a.input_dir,b,"reference_free_h0"); excluded+=ex
        free_pr=profile(freerecs,cfg)
        fb=fixed_pr["best_record"]; fr=free_pr["best_record"]
        delta=None; nesting=False
        if fb and fr:
            delta=float(fb["objective_chi2"])-float(fr["objective_chi2"])
            nesting=float(fr["objective_chi2"])<=float(fb["objective_chi2"])+tolneg

        embeds=[r for r in freerecs if r.get("start_family")=="phase1_fixed_embed"]
        embedding=False; embedding_detail=None
        if len(embeds)==1:
            e=(embeds[0].get("seed_candidate") or {}).get("same_run_embedding")
            if isinstance(e,dict):
                embedding=bool(e.get("pass")) and abs(float(e.get("delta",999)))<=embedtol
                embedding_detail=e

        branches[b]={
            "fixed_h0_71p5":fixed_pr,
            "reference_free_h0":free_pr,
            "fixed_minus_free_delta_objective":delta,
            "profile_nesting_pass":nesting,
            "same_run_fixed_to_free_embedding_pass":embedding,
            "same_run_embedding":embedding_detail,
        }
        gates[f"{b}_fixed_complete"]=bool(fixed_pr["complete_gate"])
        gates[f"{b}_fixed_multistart"]=bool(fixed_pr["stable"])
        gates[f"{b}_free_complete"]=bool(free_pr["complete_gate"])
        gates[f"{b}_free_multistart"]=bool(free_pr["stable"])
        gates[f"{b}_same_run_embedding"]=embedding
        gates[f"{b}_profile_nesting"]=nesting

    gates.update({
        "Q_IDENTITY_GATE":cfg["project"]["q"]=="Q016",
        "MODEL_IDENTITY_GATE":cfg["model"]["n_scf"]==3 and cfg["model"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "H0_TARGET_GATE":abs(float(cfg["model"]["target_h0"])-71.5)<=1e-8,
        "OBJECTIVE_IDENTITY_GATE":cfg["execution"]["objective"]["basis"]==BASIS,
        "EXACT_OPTIMIZER_OBJECTIVE_GATE":cfg["execution"]["optimizer"]["ignore_prior"] is True,
        "COMMON_MULTIPOLE_GATE":[cfg["surface"]["primary"]["ell_min"],cfg["surface"]["primary"]["ell_max"]]==[600,2000],
        "COMMON_OBSERVABLE_GATE":cfg["surface"]["primary"]["observables"]==["TT","TE","EE"],
        "COMMON_TAU_GATE":abs(float(cfg["surface"]["tau"]["mean"])-0.051)<1e-12 and abs(float(cfg["surface"]["tau"]["sigma"])-0.006)<1e-12,
        "Q011_NONPORTABILITY_GATE":cfg["model"]["q011_exact_vector_as_external_endpoint"] is False,
        "NO_SHARED_LOWZ_DOUBLECOUNT_GATE":cfg["surface"]["primary"]["low_z_data"]==[],
        "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
        "RESULT_PROVENANCE_GATE":True,
    })
    computed_endpoint_reprofile=all(
        gates[f"{b}_fixed_complete"] and gates[f"{b}_fixed_multistart"] and
        gates[f"{b}_free_complete"] and gates[f"{b}_free_multistart"] and
        gates[f"{b}_same_run_embedding"] and gates[f"{b}_profile_nesting"]
        for b in BRANCHES
    )
    gates["ENDPOINT_REPROFILE_GATE"]=computed_endpoint_reprofile
    gates["PROFILE_NESTING_GATE"]=all(gates[f"{b}_profile_nesting"] for b in BRANCHES)
    gates["SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE"]=all(gates[f"{b}_same_run_embedding"] for b in BRANCHES)
    gates["MULTISTART_STABILITY_GATE"]=all(
        gates[f"{b}_fixed_multistart"] and gates[f"{b}_free_multistart"] for b in BRANCHES)
    primary=all(bool(v) for v in gates.values())
    result={
        "case_id":cfg["project"]["case_id"],"q":Q,"original_case_question":cfg["scientific_question"],
        "run_id":RUN,"result_id":RESULT,"stage":"PRIMARY_ENDPOINT_EXACT_OBJECTIVE_CERTIFICATION",
        "validation_status":"VALIDATED" if primary else "NUMERICALLY_UNRESOLVED",
        "scientifically_usable_primary_endpoint_result":primary,
        "primary_endpoint_gate":"PASS" if primary else "FAIL",
        "final_result_gate":"PENDING_ATTRIBUTION_RESIDUAL_AND_SECONDARY_MECHANISM_STAGES",
        "objective_basis":BASIS,"branches":branches,"gates":gates,
        "excluded_records":excluded,
        "cross_chain_chi2_sum_performed":False,
        "absolute_cross_chain_chi2_comparison_performed":False,
        "interpretation_guard":"Report branch-local fixed-minus-free objective values side-by-side only. Primary endpoint certification is not the final Q016 answer."
    }
    dump(a.output,result)
    if not primary:raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q016_matched_cmb_surface_v8_config.yml")
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("fixed-summary");p.add_argument("--input-dir",required=True);p.add_argument("--output",required=True)
    p=sub.add_parser("final");p.add_argument("--input-dir",required=True);p.add_argument("--phase1-summary",required=True);p.add_argument("--output",required=True)
    a=ap.parse_args();cfg=yaml.safe_load(Path(a.config).read_text())
    if a.cmd=="fixed-summary":fixed_summary(a,cfg)
    else:final(a,cfg)
if __name__=="__main__":main()
