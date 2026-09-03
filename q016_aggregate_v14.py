#!/usr/bin/env python3
"""Q016 V14 targeted Planck-free multistart continuation aggregator."""
import argparse,json,math
from pathlib import Path
import yaml

Q="Q016"; RUN="Q016-MATCHED-CMB-SURFACE-V14"; RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-014"
BASIS="SCALAR_PRIMARY_CMB_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_SHAPE_LIKELIHOODS"
BRANCHES=("planck","spt","act")
PARENT_RUN="Q016-MATCHED-CMB-SURFACE-V10"
PARENT_RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-010"

def load(p): return json.loads(Path(p).read_text())
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def finite(x):
    try:return math.isfinite(float(x))
    except Exception:return False

def record_gate(d,branch,mode,expected_run,expected_result):
    if d.get("q")!=Q or d.get("run_id")!=expected_run or d.get("result_id")!=expected_result:return False,"identity"
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
    if mode=="reference_free_h0" and d.get("target_h0") is not None:return False,"free-H0"
    return True,"pass"

def collect(root,branch,mode,expected_run,expected_result):
    out=[];excluded=[]
    for p in sorted(Path(root).rglob(f"{branch}_{mode}_*.json")):
        try:d=load(p)
        except Exception as e:
            excluded.append({"file":str(p),"reason":"parse","error":repr(e)});continue
        ok,why=record_gate(d,branch,mode,expected_run,expected_result)
        if ok:out.append(d)
        else:excluded.append({"file":str(p),"reason":why,"status":d.get("status")})
    return out,excluded

def profile(records,cfg):
    threshold=float(cfg["execution"]["continuation"]["multistart_delta_objective_max"])
    min_complete=int(cfg["execution"]["continuation"]["minimum_distinct_complete_restarts"])
    minrep=int(cfg["execution"]["continuation"]["minimum_replicates_within_delta_objective"])
    records=sorted(records,key=lambda x:float(x["objective_chi2"]))
    ids=[int(x["restart"]) for x in records]
    if len(ids)!=len(set(ids)): raise RuntimeError("DUPLICATE_RESTART_GATE=FAIL")
    complete=len(set(ids))>=min_complete
    if records:
        best=float(records[0]["objective_chi2"])
        near=[x for x in records if float(x["objective_chi2"])-best<=threshold]
        stable=len({int(x["restart"]) for x in near})>=minrep
        spread=float(records[1]["objective_chi2"])-best if len(records)>1 else float("inf")
    else:
        best=None;near=[];stable=False;spread=float("inf")
    return {"all":records,"best_record":records[0] if records else None,
            "complete_count":len(records),"distinct_restart_ids":sorted(ids),
            "complete_gate":complete,"best_two_spread":spread,
            "replicate_restart_ids_within_delta_objective":sorted(int(x["restart"]) for x in near),
            "replicate_count_within_delta_objective":len(near),"stable":stable}

def main_final(a,cfg):
    fixed=load(a.phase1_summary)
    if fixed.get("q")!=Q or fixed.get("run_id")!=PARENT_RUN or fixed.get("result_id")!=PARENT_RESULT or fixed.get("stage")!="PHASE1_FIXED_SUMMARY" or fixed.get("status")!="PASS":
        raise RuntimeError("PARENT_FIXED_SUMMARY_GATE=FAIL")
    parent_merged=load(a.parent_merged)
    pg=parent_merged.get("gates",{})
    if parent_merged.get("run_id")!=PARENT_RUN or parent_merged.get("result_id")!=PARENT_RESULT:
        raise RuntimeError("V10_PARENT_GATE=FAIL identity")
    if parent_merged.get("primary_endpoint_gate")!="FAIL" or pg.get("planck_free_multistart") is not False:
        raise RuntimeError("V10_PARENT_GATE=FAIL expected failure")
    for k in ("spt_free_multistart","act_free_multistart","PROFILE_NESTING_GATE","SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE"):
        if pg.get(k) is not True: raise RuntimeError("V10_PARENT_GATE=FAIL "+k)

    tolneg=float(cfg["execution"]["continuation"]["fixed_vs_free_negative_tolerance"])
    embedtol=float(cfg["execution"]["continuation"]["embedding_equivalence_tolerance"])
    branches={};gates={};excluded=[];extension_records=[]
    for b in BRANCHES:
        parent_free,ex=collect(a.parent_free_dir,b,"reference_free_h0",PARENT_RUN,PARENT_RESULT); excluded+=ex
        if len(parent_free)!=4: raise RuntimeError(f"V10_PARENT_FREE_COUNT_GATE=FAIL {b} {len(parent_free)}")
        combined=list(parent_free)
        if b=="planck":
            extension,ex2=collect(a.extension_dir,b,"reference_free_h0",RUN,RESULT); excluded+=ex2
            extension_records=extension
            if len(extension)!=4: raise RuntimeError(f"V14_PLANCK_EXTENSION_COUNT_GATE=FAIL {len(extension)}")
            for r in extension:
                sm=r.get("source_vector_meta") or {}
                if sm.get("kind")!="V10_PLANCK_FREE_BEST_NONZERO_PERTURBATION" or sm.get("nonzero_perturbation") is not True:
                    raise RuntimeError("NONZERO_PERTURBATION_GATE=FAIL")
            combined.extend(extension)

        fixed_pr=fixed["branches"][b]
        free_pr=profile(combined,cfg)
        fb=fixed_pr["best_record"]; fr=free_pr["best_record"]
        delta=float(fb["objective_chi2"])-float(fr["objective_chi2"])
        nesting=float(fr["objective_chi2"])<=float(fb["objective_chi2"])+tolneg
        embeds=[r for r in parent_free if r.get("start_family")=="phase1_fixed_embed"]
        embedding=False;detail=None
        if len(embeds)==1:
            detail=(embeds[0].get("seed_candidate") or {}).get("same_run_embedding")
            if isinstance(detail,dict):
                embedding=bool(detail.get("pass")) and abs(float(detail.get("delta",999)))<=embedtol

        branches[b]={"fixed_h0_71p5":fixed_pr,"reference_free_h0":free_pr,
                     "fixed_minus_free_delta_objective":delta,
                     "profile_nesting_pass":nesting,
                     "same_run_fixed_to_free_embedding_pass":embedding,
                     "same_run_embedding":detail}
        gates[f"{b}_fixed_complete"]=bool(fixed_pr["complete_gate"])
        gates[f"{b}_fixed_multistart"]=bool(fixed_pr["stable"])
        gates[f"{b}_free_complete"]=bool(free_pr["complete_gate"])
        gates[f"{b}_free_multistart"]=bool(free_pr["stable"])
        gates[f"{b}_same_run_embedding"]=embedding
        gates[f"{b}_profile_nesting"]=nesting

    # Diagnostic only: do not replace or relax the original multistart gate.
    best=float(branches["planck"]["reference_free_h0"]["best_record"]["objective_chi2"])
    raw_near=[]
    for r in extension_records:
        raw=(r.get("raw_optimizer_candidate") or {})
        if finite(raw.get("objective_chi2")) and float(raw["objective_chi2"])-best<=1.0:
            raw_near.append({"restart":r["restart"],"objective_chi2":raw["objective_chi2"],
                             "H0":(raw.get("minimum") or {}).get("H0")})

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
      "V10_PARENT_FAILURE_IDENTITY_GATE":True,
      "V10_PARENT_FREE_RECORD_COUNT_GATE":True,
      "V14_PLANCK_EXTENSION_COMPLETE_GATE":len(extension_records)==4,
      "V14_NONZERO_PERTURBATION_GATE":all((r.get("source_vector_meta") or {}).get("nonzero_perturbation") is True for r in extension_records),
    })
    gates["PROFILE_NESTING_GATE"]=all(gates[f"{b}_profile_nesting"] for b in BRANCHES)
    gates["SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE"]=all(gates[f"{b}_same_run_embedding"] for b in BRANCHES)
    gates["MULTISTART_STABILITY_GATE"]=all(gates[f"{b}_fixed_multistart"] and gates[f"{b}_free_multistart"] for b in BRANCHES)
    gates["ENDPOINT_REPROFILE_GATE"]=all(
        gates[f"{b}_fixed_complete"] and gates[f"{b}_fixed_multistart"] and
        gates[f"{b}_free_complete"] and gates[f"{b}_free_multistart"] and
        gates[f"{b}_same_run_embedding"] and gates[f"{b}_profile_nesting"] for b in BRANCHES)
    primary=all(bool(v) for v in gates.values())
    result={"case_id":cfg["project"]["case_id"],"q":Q,"original_case_question":cfg["scientific_question"],
            "run_id":RUN,"result_id":RESULT,"stage":"PRIMARY_ENDPOINT_EXACT_OBJECTIVE_CERTIFICATION",
            "validation_status":"VALIDATED" if primary else "NUMERICALLY_UNRESOLVED",
            "scientifically_usable_primary_endpoint_result":primary,
            "primary_endpoint_gate":"PASS" if primary else "FAIL",
            "final_result_gate":"PENDING_ATTRIBUTION_RESIDUAL_AND_SECONDARY_MECHANISM_STAGES",
            "objective_basis":BASIS,"branches":branches,"gates":gates,
            "planck_extension_diagnostic":{"raw_optimizer_records_within_delta_1_of_combined_best":raw_near,
                                           "raw_optimizer_replicate_count":len(raw_near),
                                           "note":"Diagnostic only; original selected-candidate multistart gate remains authoritative."},
            "excluded_records":excluded,"cross_chain_chi2_sum_performed":False,
            "absolute_cross_chain_chi2_comparison_performed":False,
            "interpretation_guard":"Branch-local fixed-minus-free objectives only; no cross-chain sum. V14 changes no scientific threshold."}
    dump(a.output,result)
    if not primary: raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q016_matched_cmb_surface_v14_config.yml")
    sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("final")
    p.add_argument("--phase1-summary",required=True)
    p.add_argument("--parent-merged",required=True)
    p.add_argument("--parent-free-dir",required=True)
    p.add_argument("--extension-dir",required=True)
    p.add_argument("--output",required=True)
    a=ap.parse_args(); cfg=yaml.safe_load(Path(a.config).read_text())
    main_final(a,cfg)

if __name__=="__main__": main()
