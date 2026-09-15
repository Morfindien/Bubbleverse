#!/usr/bin/env python3
"""Bubbleverse Q041 V19 — linear eight-stage execution, V18 constant-definition repair.

V19 preserves the V18 single-workflow linear architecture and every Q041 scientific and
numerical lock. The sole execution repair is restoration of the explicit
HILLIPOP_COMPONENT = "planck_2020_hillipop.TT" constant required by the HiLLiPoP
segment-resume lock. Segment 1 starts fresh; segments 2-8 consume only the immediately
preceding V19 artifact for the same logical chain. No --allow-changes bypass is used.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import time
from typing import Any, Sequence

import numpy as np
import yaml

import q041_planck_portability_v13 as base

Q="Q-041"
PROGRAM_ID="Q041-PLANCKPORT-V19"
RUN_ID="Q041-DOWNSTREAM-SCIENTIFIC-CONSEQUENCE-PORTABILITY-V19"
RESULT_ID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-019"
V13_PROGRAM_ID="Q041-PLANCKPORT-V13"
V13_PARENT_RUN_ID=34379785115
CHAIN_META="q041_chain_metadata_v19.json"
HILLIPOP_COMPONENT="planck_2020_hillipop.TT"
SEGMENT_SOFT_STOP_DEFAULT=300
MAX_SEGMENTS_DEFAULT=8

# Patch only identity globals used by inherited V13 scientific functions.
base.PROGRAM_ID=PROGRAM_ID
base.RUN_ID=RUN_ID
base.RESULT_ID=RESULT_ID

ARMS=base.ARMS
ALL_COMBOS=base.ALL_COMBOS
BASELINE_COMBOS=base.BASELINE_COMBOS
LOO_COMBOS=base.LOO_COMBOS
COMMON_COORDS=base.COMMON_COORDS
FULL_COMBO=base.FULL_COMBO
HARD_RHAT=base.HARD_RHAT
MATERIAL_SIGMA=base.MATERIAL_SIGMA
LOO_MATERIAL_SIGMA=base.LOO_MATERIAL_SIGMA
EQUIV_SIGMA=base.EQUIV_SIGMA
BC_MATERIAL=base.BC_MATERIAL
BC_EQUIV=base.BC_EQUIV


class SegmentSoftStop(Exception):
    pass


def _checkpoint_state(output_dir: str|Path) -> dict[str,Any]:
    p=Path(output_dir)/"chain.checkpoint"
    if not p.exists():
        return {}
    try:
        d=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        m=d.get("sampler",{}).get("mcmc",{}) if isinstance(d,dict) else {}
        return {
            "checkpoint_exists": True,
            "checkpoint_converged": bool(m.get("converged",False)),
            "checkpoint_Rminus1_last": (
                float(m["Rminus1_last"]) if base.finite(m.get("Rminus1_last")) else None
            ),
            "checkpoint_burn_in": m.get("burn_in"),
        }
    except Exception as exc:
        return {"checkpoint_exists":True,"checkpoint_parse_error":repr(exc)}


def _chain_resume_ready(output_dir: str|Path) -> bool:
    d=Path(output_dir)
    required=("chain.1.txt","chain.checkpoint","chain.covmat","chain.updated.yaml")
    return all((d/x).is_file() and (d/x).stat().st_size>0 for x in required)


def _existing_complete_meta(output_dir: str|Path, implementation: str, combo: str, chain: int, series_id: str):
    p=Path(output_dir)/CHAIN_META
    if not p.exists():
        return None
    try:
        d=base.read_json(p)
    except Exception:
        return None
    if (
        d.get("q")==Q and d.get("program_id")==PROGRAM_ID
        and d.get("implementation")==implementation and d.get("combo")==combo
        and int(d.get("chain",-1))==int(chain)
        and str(d.get("series_id",""))==str(series_id)
        and d.get("status")=="COMPLETE" and d.get("actual_computed_result") is True
    ):
        return d
    return None


def _canonical_hash(obj: Any) -> str:
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _frozen_hillipop_resume_component(output_dir: str|Path) -> tuple[dict[str,Any],str]:
    """Load the exact resolved HiLLiPoP TT component recorded by the parent chain."""
    p=Path(output_dir)/"chain.updated.yaml"
    if not p.is_file():
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL missing_chain_updated_yaml")
    d=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    like=d.get("likelihood",{}) if isinstance(d,dict) else {}
    frozen=like.get(HILLIPOP_COMPONENT)
    if not isinstance(frozen,dict):
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL missing_component")
    # These are implementation/data identity fields, not tunable science settings.
    if frozen.get("data_folder")!="planck_2020/hillipop":
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL data_folder")
    if frozen.get("multipoles_range_file")!="data/binning_v4.2.fits":
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL binning")
    if frozen.get("covariance_matrix_file")!="data/invfll_PR4_v4.2_TT.fits":
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL covariance")
    if not isinstance(frozen.get("input_params"),list) or "A_planck" not in frozen["input_params"]:
        raise RuntimeError("V19_HILLIPOP_UPDATED_INFO_GATE=FAIL input_params")
    return copy.deepcopy(frozen),_canonical_hash(frozen)


def _lock_hillipop_resume_info(info: dict[str,Any], output_dir: str|Path) -> str:
    """Feed Cobaya the exact resolved HiLLiPoP component from the checkpoint lineage.

    No --allow-changes path is used. The runtime class patch is installed normally by
    build_info; this only freezes the serializable component options that Cobaya compares
    against chain.updated.yaml before allowing resume.
    """
    frozen,h=_frozen_hillipop_resume_component(output_dir)
    likes=info.setdefault("likelihood",{})
    if HILLIPOP_COMPONENT not in likes:
        raise RuntimeError("V19_HILLIPOP_RESUME_COMPONENT_GATE=FAIL component_not_in_new_info")
    likes[HILLIPOP_COMPONENT]=frozen
    if _canonical_hash(likes[HILLIPOP_COMPONENT])!=h:
        raise RuntimeError("V19_HILLIPOP_RESUME_COMPONENT_GATE=FAIL hash_roundtrip")
    print(f"Q041_V19_HILLIPOP_RESUME_LOCK_GATE=PASS hash={h}")
    return h


def _resume_provenance_gate(output_dir: str|Path, implementation: str, combo: str, chain: int, series_id: str, segment: int) -> dict[str,Any]:
    """Require the immediately preceding V19 stage for the same logical chain."""
    outdir=Path(output_dir)
    if int(segment) <= 1:
        raise RuntimeError("V19_SEGMENT1_FRESH_START_GATE=FAIL")
    if not _chain_resume_ready(outdir):
        raise RuntimeError("V19_CONTINUATION_STATE_GATE=FAIL missing_resume_files")
    meta_path=outdir/CHAIN_META
    if not meta_path.exists():
        raise RuntimeError("V19_CONTINUATION_STATE_GATE=FAIL missing_metadata")
    try:
        d=base.read_json(meta_path)
    except Exception as exc:
        raise RuntimeError(f"V19_RESUME_METADATA_PARSE_GATE=FAIL {exc!r}")
    if not (
        d.get("q")==Q and d.get("program_id")==PROGRAM_ID
        and d.get("implementation")==implementation and d.get("combo")==combo
        and int(d.get("chain",-1))==int(chain)
        and str(d.get("series_id",""))==str(series_id)
        and int(d.get("segment",0) or 0)==int(segment)-1
        and d.get("status") in ("COMPLETE","PARTIAL_SOFT_STOP","NO_SCIENTIFIC_RESULT")
        and 1 <= int(d.get("compute_segments_used",0) or 0) <= MAX_SEGMENTS_DEFAULT
    ):
        raise RuntimeError("V19_LINEAR_PREDECESSOR_PROVENANCE_GATE=FAIL")
    print(
        f"Q041_V19_LINEAR_PREDECESSOR_GATE=PASS series={series_id} "
        f"prior_segment={d.get('segment')} compute_segments_used={d.get('compute_segments_used')}"
    )
    return d

def _write_no_science_final(output: str|Path, reason: str, details: dict[str,Any], required_gates: dict[str,str]|None=None) -> None:
    out={
      "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
      "stage":"FINAL","status":"PASS","final_outcome_valid":True,"actual_computed_result":False,
      "scientific_classification":"NO_SCIENTIFIC_RESULT","outcome_type":"CONTROLLED_NO_SCIENTIFIC_RESULT",
      "no_science_reason":reason,"technical_failure":False,"required_gates":required_gates or {},"details":details,
      "claim_boundaries":{
        "no_cross_arm_chi2_sum":True,"no_hybrid_planck_likelihood":True,"Q040_scientific_products_used":False,
        "controlled_numerical_noncompletion_is_not_physical_evidence":True,
        "technical_failure_would_not_be_encoded_as_green_final":True
      }
    }
    base.write_json(output,out)
    print(f"Q041_FINAL_GATE=PASS classification=NO_SCIENTIFIC_RESULT reason={reason}")


def sample(args: argparse.Namespace) -> int:
    if args.implementation not in ARMS or args.combo not in ALL_COMBOS or args.chain not in (0,1):
        raise RuntimeError("SAMPLE_IDENTITY_GATE=FAIL")
    if not (1 <= int(args.segment) <= int(args.max_segments)):
        raise RuntimeError("SEGMENT_IDENTITY_GATE=FAIL")
    if not (60 <= int(args.soft_stop_minutes) <= 315):
        raise RuntimeError("SEGMENT_SOFT_STOP_GATE=FAIL")
    if not str(args.series_id).strip():
        raise RuntimeError("V19_SERIES_ID_GATE=FAIL")

    outdir=Path(args.output_dir)
    outdir.mkdir(parents=True,exist_ok=True)
    prior=None
    if int(args.segment)==1:
        # One workflow, one lineage: segment 1 is intentionally fresh. No V13-V19 chain state is admissible.
        for name in ("chain.1.txt","chain.checkpoint","chain.covmat","chain.updated.yaml",CHAIN_META):
            if (outdir/name).exists():
                raise RuntimeError(f"V19_FRESH_SEGMENT1_GATE=FAIL unexpected={name}")
        compute_segments_used=0
        resuming=False
        print("Q041_V19_FRESH_SEGMENT1_GATE=PASS")
    else:
        prior=_resume_provenance_gate(outdir,args.implementation,args.combo,args.chain,args.series_id,int(args.segment))
        compute_segments_used=int(prior.get("compute_segments_used",0) or 0)
        resuming=True

    # Terminal chain states simply flow through later fixed stages without consuming compute.
    if prior is not None and prior.get("status") in ("COMPLETE","NO_SCIENTIFIC_RESULT"):
        terminal=copy.deepcopy(prior)
        terminal["segment"]=int(args.segment)
        terminal["reused_terminal_from_segment"]=int(prior.get("segment",0) or 0)
        terminal["segment_action"]=("ALREADY_COMPLETE_NO_RESAMPLE" if prior.get("status")=="COMPLETE"
                                    else "ALREADY_CONTROLLED_NO_SCIENCE_NO_RESAMPLE")
        terminal["technical_failure"]=False
        terminal.update(_checkpoint_state(outdir))
        base.write_json(outdir/CHAIN_META,terminal)
        print(f"Q041_V19_TERMINAL_CHAIN_CARRY_GATE=PASS arm={args.implementation} combo={args.combo} chain={args.chain} status={terminal.get('status')}")
        return 0

    if compute_segments_used >= int(args.max_segments):
        raise RuntimeError("V19_PER_CHAIN_SEGMENT_BUDGET_DISPATCH_GATE=FAIL")

    args.chain_seed=410000+1000*ARMS.index(args.implementation)+10*ALL_COMBOS.index(args.combo)+args.chain
    prefix=outdir/"chain"
    info,meta=base.build_info(args,args.implementation,args.combo,prefix,mcmc=True)
    hillipop_resume_hash=None
    if resuming:
        info["force"]=False; info["resume"]=True
        if args.implementation=="hillipop":
            hillipop_resume_hash=_lock_hillipop_resume_info(info,outdir)
    else:
        info["force"]=True; info["resume"]=False

    rec={
        "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"MCMC_CHAIN","implementation":args.implementation,"combo":args.combo,
        "chain":args.chain,"chain_seed":args.chain_seed,"segment":int(args.segment),"series_id":str(args.series_id),
        "segment_soft_stop_minutes":int(args.soft_stop_minutes),"max_segments":int(args.max_segments),
        "compute_segments_used_before":int(compute_segments_used),"compute_segments_used":int(compute_segments_used),
        "resumed_from_checkpoint":bool(resuming),"status":"FAILED","actual_computed_result":False,"meta":meta,
        "scientific_sampler_lock":{"burn_in":100,"max_samples":20000,"Rminus1_stop":0.02,"Rminus1_cl_stop":0.2,"learn_proposal":True},
        "linear_single_workflow_run":True,
    }
    if hillipop_resume_hash:
        rec["hillipop_resume_component_sha256"]=hillipop_resume_hash
        rec["hillipop_resume_component_source"]="chain.updated.yaml"
    if resuming:
        rec["resume_source_state"]=_checkpoint_state(outdir)

    sampler=None
    from cobaya.samplers.mcmc.mcmc import MCMC
    deadline=time.monotonic()+int(args.soft_stop_minutes)*60.0
    original_metropolis=MCMC.get_new_sample_metropolis
    original_dragging=MCMC.get_new_sample_dragging
    original_run=MCMC.run
    def _deadline_guard(fn):
        def guarded(self,*a,**kw):
            if time.monotonic() >= deadline: raise SegmentSoftStop()
            return fn(self,*a,**kw)
        return guarded
    def _segmented_run(self,*a,**kw):
        try: return original_run(self,*a,**kw)
        except SegmentSoftStop:
            try: self.collection.out_update()
            finally: self.write_checkpoint()
            raise
    MCMC.get_new_sample_metropolis=_deadline_guard(original_metropolis)
    MCMC.get_new_sample_dragging=_deadline_guard(original_dragging)
    MCMC.run=_segmented_run
    try:
        from cobaya.run import run as cobaya_run
        if resuming:
            _,sampler=cobaya_run(info,resume=True,force=False)
        else:
            _,sampler=cobaya_run(info,resume=False,force=True)
        converged=bool(getattr(sampler,"converged",False))
        rlast=getattr(sampler,"Rminus1_last",None)
        rec["sampler_converged"]=converged
        rec["sampler_Rminus1_last"]=float(rlast) if base.finite(rlast) else None
        if not converged:
            rec.update({"status":"NO_SCIENTIFIC_RESULT","actual_computed_result":False,"controlled_no_science":True,
                        "failure_class":"MAX_SAMPLES_WITHOUT_CONVERGENCE","no_science_reason":"MAX_SAMPLES_WITHOUT_CONVERGENCE",
                        "message":"Cobaya returned before convergence; unchanged max_samples=20000 exhausted."})
        else:
            rec.update({"status":"COMPLETE","actual_computed_result":True,"output_prefix":"chain","segment_action":"CONVERGED"})
    except SegmentSoftStop:
        rec.update({"status":"PARTIAL_SOFT_STOP","failure_class":"SEGMENT_BOUNDARY","segment_action":"CHECKPOINT_AND_RESUME_NEXT_SEGMENT"})
    except Exception as exc:
        rec.update({"status":"FAILED","failure_class":"MCMC_OR_LIKELIHOOD","error":repr(exc),"technical_failure":True})
    finally:
        MCMC.get_new_sample_metropolis=original_metropolis
        MCMC.get_new_sample_dragging=original_dragging
        MCMC.run=original_run
        try:
            if sampler is not None and hasattr(sampler,"close"): sampler.close()
        except Exception: pass
        if rec.get("status") in ("PARTIAL_SOFT_STOP","COMPLETE","NO_SCIENTIFIC_RESULT"):
            rec["compute_segments_used"]=int(compute_segments_used)+1
        rec.update(_checkpoint_state(outdir))
        rec["resume_state_files_present"]=_chain_resume_ready(outdir)
        base.write_json(outdir/CHAIN_META,rec)

    if rec["status"]=="PARTIAL_SOFT_STOP":
        if not rec["resume_state_files_present"]: raise RuntimeError("Q041_PARTIAL_RESUME_STATE_GATE=FAIL")
        if int(rec["compute_segments_used"])>int(args.max_segments): raise RuntimeError("V19_PER_CHAIN_SEGMENT_BUDGET_GATE=FAIL")
        print(f"Q041_CHAIN_SEGMENT_GATE=PARTIAL arm={args.implementation} combo={args.combo} chain={args.chain} segment={args.segment} compute_segments_used={rec.get('compute_segments_used')} Rminus1={rec.get('checkpoint_Rminus1_last')}")
        return 0
    if rec["status"]=="NO_SCIENTIFIC_RESULT":
        print(f"Q041_CHAIN_CONTROLLED_NO_SCIENCE_GATE=PASS arm={args.implementation} combo={args.combo} chain={args.chain} reason={rec.get('no_science_reason')}")
        return 0
    if rec["status"]!="COMPLETE":
        raise RuntimeError("Q041_CHAIN_GATE=FAIL "+rec.get("error",rec.get("failure_class","")))
    print(f"Q041_CHAIN_GATE=PASS arm={args.implementation} combo={args.combo} chain={args.chain} segment={args.segment} compute_segments_used={rec.get('compute_segments_used')}")
    return 0

def aggregate(args: argparse.Namespace) -> int:
    base.load_preregister(args.preregister)
    base.load_source_lock(args.source_lock)
    metas=[]
    for p in Path(args.input_dir).rglob(CHAIN_META):
        d=base.read_json(p)
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID:
            metas.append((d,p))
    expected={(a,c,k) for a in ARMS for c in ALL_COMBOS for k in (0,1)}
    complete=[
        (d,p) for d,p in metas
        if d.get("status")=="COMPLETE" and d.get("actual_computed_result") is True
    ]
    found={(d.get("implementation"),d.get("combo"),int(d.get("chain",-1))) for d,_ in complete}
    missing=sorted(expected-found)
    if missing:
        raise RuntimeError(f"CHAIN_COMPLETENESS_GATE=FAIL missing={missing}")

    summaries={}
    for arm in ARMS:
        for combo in ALL_COMBOS:
            cc=[]
            for chain in (0,1):
                d,p=next(
                    (d,p) for d,p in complete
                    if d.get("implementation")==arm and d.get("combo")==combo
                    and int(d.get("chain",-1))==chain
                )
                x,w=base.load_chain_from_meta(p)
                cc.append((x,w))
            rh=base._rhat_for_chains(cc)
            if not np.all(np.isfinite(rh)) or float(np.max(rh))>HARD_RHAT:
                _write_no_science_final(args.output,"FINAL_RHAT_GATE_NOT_REACHED",
                    {"arm":arm,"combo":combo,"rhat":rh.tolist(),"hard_rhat_gate":HARD_RHAT},
                    {"CHAIN_COMPLETENESS":"PASS","ALL_RHAT_LE_1P05":"FAIL",
                     "BOTH_ARMS_ALL_COMBINATIONS":"BLOCKED","Q040_FIREWALL":"PASS",
                     "SEGMENTED_RESUME_COMPLETENESS":"PASS"})
                return 0
            x=np.vstack([z[0] for z in cc])
            w=np.concatenate([z[1] for z in cc])
            mu,cov=base._weighted_stats(x,w)
            summaries[f"{arm}:{combo}"]={
                "mean":dict(zip(COMMON_COORDS,map(float,mu))),
                "covariance":cov.tolist(),
                "rhat":dict(zip(COMMON_COORDS,map(float,rh))),
                "max_rhat":float(np.max(rh)),
                "effective_weight":float(w.sum()),
            }

    comparisons={}
    for combo in ALL_COMBOS:
        A=summaries[f"camspec:{combo}"]
        B=summaries[f"hillipop:{combo}"]
        mu1=np.array([A["mean"][c] for c in COMMON_COORDS])
        mu2=np.array([B["mean"][c] for c in COMMON_COORDS])
        c1=np.asarray(A["covariance"])
        c2=np.asarray(B["covariance"])
        sig=np.sqrt(np.maximum(np.diag(c1)+np.diag(c2),1e-300))
        shifts=np.abs(mu1-mu2)/sig
        comparisons[combo]={
            "standardized_mean_shift":dict(zip(COMMON_COORDS,map(float,shifts))),
            "max_standardized_shift":float(np.max(shifts)),
            "gaussian_bhattacharyya_coefficient":base._bc(mu1,c1,mu2,c2),
        }

    full=comparisons[FULL_COMBO]
    loo=[comparisons[c]["max_standardized_shift"] for c in LOO_COMBOS]
    robust_material=sum(v>=LOO_MATERIAL_SIGMA for v in loo)>=2
    if (
        (full["max_standardized_shift"]>=MATERIAL_SIGMA
         or full["gaussian_bhattacharyya_coefficient"]<=BC_MATERIAL)
        and robust_material
    ):
        classification="MATERIAL_DOWNSTREAM_DIFFERENCE"
    elif (
        full["max_standardized_shift"]<=EQUIV_SIGMA
        and full["gaussian_bhattacharyya_coefficient"]>=BC_EQUIV
        and all(v<=LOO_MATERIAL_SIGMA for v in loo)
    ):
        classification="SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS"
    else:
        classification="CONSTRAINED_MIXED"

    out={
        "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"FINAL","status":"PASS","final_outcome_valid":True,"actual_computed_result":True,
        "outcome_type":"SCIENTIFIC_RESULT","technical_failure":False,"scientific_classification":classification,
        "required_gates":{
            "CHAIN_COMPLETENESS":"PASS","ALL_RHAT_LE_1P05":"PASS",
            "BOTH_ARMS_ALL_COMBINATIONS":"PASS","Q040_FIREWALL":"PASS",
            "SEGMENTED_RESUME_COMPLETENESS":"PASS",
        },
        "summaries":summaries,"comparisons":comparisons,
        "classification_inputs":{"full":full,"loo_max_shifts":dict(zip(LOO_COMBOS,loo))},
        "claim_boundaries":{
            "no_cross_arm_chi2_sum":True,"no_hybrid_planck_likelihood":True,
            "Q040_scientific_products_used":False,
            "bhattacharyya_is_gaussian_summary_of_empirical_posterior_moments":True,
            "segmentation_changes_scientific_target":False,
        },
    }
    base.write_json(args.output,out)
    print(f"Q041_FINAL_GATE=PASS classification={classification}")
    return 0


def finalize_linear(args: argparse.Namespace) -> int:
    """Seal the single workflow run after fixed segment 8."""
    base.load_preregister(args.preregister); base.load_source_lock(args.source_lock)
    rows={}
    for p in Path(args.input_dir).rglob(CHAIN_META):
        try: d=base.read_json(p)
        except Exception: continue
        if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID: continue
        key=(d.get("implementation"),d.get("combo"),int(d.get("chain",-1)))
        if key in rows: raise RuntimeError(f"V19_FINAL_DUPLICATE_CHAIN_META_GATE=FAIL key={key}")
        rows[key]=(d,p)
    expected={(a,c,k) for a in ARMS for c in ALL_COMBOS for k in (0,1)}
    missing=sorted(expected-set(rows))
    if missing: raise RuntimeError(f"V19_FINAL_CHAIN_METADATA_GATE=FAIL missing={missing}")
    known={"COMPLETE","PARTIAL_SOFT_STOP","NO_SCIENTIFIC_RESULT"}
    bad=sorted(k for k,(d,_) in rows.items() if d.get("status") not in known)
    if bad: raise RuntimeError(f"V19_FINAL_TECHNICAL_STATUS_GATE=FAIL bad={bad}")
    wrong_stage=sorted(k for k,(d,_) in rows.items() if int(d.get("segment",0) or 0)!=8)
    if wrong_stage: raise RuntimeError(f"V19_FINAL_SEGMENT8_PROVENANCE_GATE=FAIL bad={wrong_stage}")
    no_science=[k for k,(d,_) in rows.items() if d.get("status")=="NO_SCIENTIFIC_RESULT"]
    if no_science:
        reasons={rows[k][0].get("no_science_reason") for k in no_science}
        if reasons!={"MAX_SAMPLES_WITHOUT_CONVERGENCE"}:
            raise RuntimeError(f"V19_FINAL_CONTROLLED_REASON_GATE=FAIL reasons={sorted(map(str,reasons))}")
        _write_no_science_final(args.output,"MAX_SAMPLES_WITHOUT_CONVERGENCE",
            {"segment":8,"affected_chains":[list(k) for k in sorted(no_science)]},
            {"CHAIN_COMPLETENESS":"BLOCKED","ALL_RHAT_LE_1P05":"BLOCKED","BOTH_ARMS_ALL_COMBINATIONS":"BLOCKED","Q040_FIREWALL":"PASS","SEGMENTED_RESUME_COMPLETENESS":"CONTROLLED_STOP"})
        return 0
    partial=[k for k,(d,_) in rows.items() if d.get("status")=="PARTIAL_SOFT_STOP"]
    if partial:
        under=[k for k in partial if int(rows[k][0].get("compute_segments_used",0) or 0)<8]
        if under: raise RuntimeError(f"V19_FINAL_SEGMENT_BUDGET_ACCOUNTING_GATE=FAIL under={under}")
        _write_no_science_final(args.output,"SEGMENT_BUDGET_EXHAUSTED_WITH_UNCONVERGED_CHAINS",
            {"segment":8,"affected_chains":[list(k) for k in sorted(partial)]},
            {"CHAIN_COMPLETENESS":"BLOCKED","ALL_RHAT_LE_1P05":"BLOCKED","BOTH_ARMS_ALL_COMBINATIONS":"BLOCKED","Q040_FIREWALL":"PASS","SEGMENTED_RESUME_COMPLETENESS":"CONTROLLED_STOP"})
        return 0
    # All 32 are complete. Reuse the unchanged scientific aggregation and hard R-hat gate.
    return aggregate(args)

def static_check(args: argparse.Namespace) -> int:
    return base.static_check(args)


def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="cmd",required=True)

    s=sp.add_parser("static")
    s.add_argument("--preregister",required=True)
    s.add_argument("--source-lock",required=True)
    s.add_argument("--output",required=True)
    s.set_defaults(func=static_check)

    s=sp.add_parser("prepare-nonoverlap")
    for x in ("q032-parent-root","preflight","hlp-matrix","hlp-meta","support-output","matrix-output","meta-output"):
        s.add_argument("--"+x,required=True)
    s.set_defaults(func=base.prepare_nonoverlap)

    s=sp.add_parser("runtime-preflight")
    for x in ("q032-parent-root","preflight","parent-dir","hlp-matrix","hlp-meta","reduced-support",
              "reduced-hlp-matrix","reduced-hlp-meta","preregister","source-lock"):
        s.add_argument("--"+x,required=True)
    s.add_argument("--external-runtime",required=True)
    s.add_argument("--output",required=True)
    s.set_defaults(func=base.runtime_preflight)

    s=sp.add_parser("sample")
    for x in ("q032-parent-root","preflight","parent-dir","hlp-matrix","hlp-meta","reduced-support",
              "reduced-hlp-matrix","reduced-hlp-meta","preregister","source-lock"):
        s.add_argument("--"+x,required=True)
    s.add_argument("--implementation",required=True,choices=ARMS)
    s.add_argument("--combo",required=True,choices=ALL_COMBOS)
    s.add_argument("--chain",required=True,type=int,choices=(0,1))
    s.add_argument("--output-dir",required=True)
    s.add_argument("--segment",required=True,type=int)
    s.add_argument("--series-id",required=True)
    s.add_argument("--soft-stop-minutes",type=int,default=SEGMENT_SOFT_STOP_DEFAULT)
    s.add_argument("--max-segments",type=int,default=MAX_SEGMENTS_DEFAULT)
    s.set_defaults(func=sample,chain_seed=0)

    s=sp.add_parser("finalize-linear")
    s.add_argument("--input-dir",required=True)
    s.add_argument("--preregister",required=True); s.add_argument("--source-lock",required=True); s.add_argument("--output",required=True)
    s.set_defaults(func=finalize_linear)

    s=sp.add_parser("aggregate")
    s.add_argument("--input-dir",required=True)
    s.add_argument("--preregister",required=True)
    s.add_argument("--source-lock",required=True)
    s.add_argument("--output",required=True)
    s.set_defaults(func=aggregate)
    return p


if __name__=="__main__":
    a=parser().parse_args()
    raise SystemExit(a.func(a))
