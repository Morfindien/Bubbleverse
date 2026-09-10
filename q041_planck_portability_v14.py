#!/usr/bin/env python3
"""Bubbleverse Q041 V14 — segmented exact-resume execution wrapper.

Scientific model/data/priors/sampler thresholds/classification logic are inherited
unchanged from Q041-PLANCKPORT-V13. V14 changes only execution orchestration so a
single MCMC chain may span multiple GitHub-hosted jobs without exceeding the
per-job runtime limit.
"""
from __future__ import annotations

import argparse
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
PROGRAM_ID="Q041-PLANCKPORT-V14"
RUN_ID="Q041-DOWNSTREAM-SCIENTIFIC-CONSEQUENCE-PORTABILITY-V14"
RESULT_ID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-014"
V13_PROGRAM_ID="Q041-PLANCKPORT-V13"
V13_PARENT_RUN_ID=34379785115
CHAIN_META="q041_chain_metadata_v14.json"
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


def _existing_complete_meta(output_dir: str|Path, implementation: str, combo: str, chain: int):
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
        and d.get("status")=="COMPLETE" and d.get("actual_computed_result") is True
    ):
        return d
    return None


def sample(args: argparse.Namespace) -> int:
    if args.implementation not in ARMS or args.combo not in ALL_COMBOS or args.chain not in (0,1):
        raise RuntimeError("SAMPLE_IDENTITY_GATE=FAIL")
    if not (1 <= int(args.segment) <= int(args.max_segments)):
        raise RuntimeError("SEGMENT_IDENTITY_GATE=FAIL")
    if not (60 <= int(args.soft_stop_minutes) <= 315):
        raise RuntimeError("SEGMENT_SOFT_STOP_GATE=FAIL")

    outdir=Path(args.output_dir)
    outdir.mkdir(parents=True,exist_ok=True)

    complete=_existing_complete_meta(outdir,args.implementation,args.combo,args.chain)
    if complete is not None:
        if not _chain_resume_ready(outdir):
            raise RuntimeError("COMPLETE_CHAIN_STATE_FILE_GATE=FAIL")
        prior_segment=int(complete.get("segment",0) or 0)
        complete["segment"]=int(args.segment)
        complete["reused_complete_from_segment"]=prior_segment
        complete["segment_action"]="ALREADY_COMPLETE_NO_RESAMPLE"
        complete.update(_checkpoint_state(outdir))
        base.write_json(outdir/CHAIN_META,complete)
        print(
            f"Q041_CHAIN_ALREADY_COMPLETE_GATE=PASS arm={args.implementation} "
            f"combo={args.combo} chain={args.chain}"
        )
        return 0

    args.chain_seed=410000+1000*ARMS.index(args.implementation)+10*ALL_COMBOS.index(args.combo)+args.chain
    prefix=outdir/"chain"
    resuming=_chain_resume_ready(outdir)

    info,meta=base.build_info(args,args.implementation,args.combo,prefix,mcmc=True)
    # Exact V13 sampler definition is retained. Only output continuation flags differ.
    info["force"]=not resuming
    info["resume"]=resuming

    rec={
        "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"MCMC_CHAIN","implementation":args.implementation,"combo":args.combo,
        "chain":args.chain,"chain_seed":args.chain_seed,"segment":int(args.segment),
        "segment_soft_stop_minutes":int(args.soft_stop_minutes),
        "max_segments":int(args.max_segments),
        "resumed_from_checkpoint":bool(resuming),
        "status":"FAILED","actual_computed_result":False,"meta":meta,
        "scientific_sampler_lock":{
            "burn_in":100,"max_samples":20000,"Rminus1_stop":0.02,
            "Rminus1_cl_stop":0.2,"learn_proposal":True,
        },
    }
    if resuming:
        rec["resume_source_state"]=_checkpoint_state(outdir)

    sampler=None
    # Do not use an asynchronous alarm inside CLASS/likelihood code. Instead patch
    # the Cobaya MCMC proposal boundary: once the wall-clock deadline is reached,
    # stop before the next proposal, flush the collection and checkpoint, then
    # return a resumable PARTIAL state.
    from cobaya.samplers.mcmc.mcmc import MCMC
    deadline=time.monotonic()+int(args.soft_stop_minutes)*60.0
    original_metropolis=MCMC.get_new_sample_metropolis
    original_dragging=MCMC.get_new_sample_dragging
    original_run=MCMC.run

    def _deadline_guard(fn):
        def guarded(self,*a,**kw):
            if time.monotonic() >= deadline:
                raise SegmentSoftStop()
            return fn(self,*a,**kw)
        return guarded

    def _segmented_run(self,*a,**kw):
        try:
            return original_run(self,*a,**kw)
        except SegmentSoftStop:
            try:
                self.collection.out_update()
            finally:
                self.write_checkpoint()
            raise

    MCMC.get_new_sample_metropolis=_deadline_guard(original_metropolis)
    MCMC.get_new_sample_dragging=_deadline_guard(original_dragging)
    MCMC.run=_segmented_run
    try:
        from cobaya.run import run as cobaya_run
        _,sampler=cobaya_run(
            info,
            resume=True if resuming else False,
            force=False if resuming else True,
        )
        converged=bool(getattr(sampler,"converged",False))
        rlast=getattr(sampler,"Rminus1_last",None)
        rec["sampler_converged"]=converged
        rec["sampler_Rminus1_last"]=float(rlast) if base.finite(rlast) else None
        if not converged:
            rec.update({
                "status":"FAILED",
                "failure_class":"MAX_SAMPLES_WITHOUT_CONVERGENCE",
                "error":"Cobaya returned before convergence; unchanged max_samples=20000 exhausted.",
            })
        else:
            rec.update({
                "status":"COMPLETE","actual_computed_result":True,
                "output_prefix":"chain","segment_action":"CONVERGED",
            })
    except SegmentSoftStop:
        rec.update({
            "status":"PARTIAL_SOFT_STOP",
            "failure_class":"SEGMENT_BOUNDARY",
            "segment_action":"CHECKPOINT_AND_RESUME_NEXT_SEGMENT",
        })
    except Exception as exc:
        rec.update({
            "status":"FAILED","failure_class":"MCMC_OR_LIKELIHOOD","error":repr(exc),
        })
    finally:
        MCMC.get_new_sample_metropolis=original_metropolis
        MCMC.get_new_sample_dragging=original_dragging
        MCMC.run=original_run
        try:
            if sampler is not None and hasattr(sampler,"close"):
                sampler.close()
        except Exception:
            pass
        rec.update(_checkpoint_state(outdir))
        rec["resume_state_files_present"]=_chain_resume_ready(outdir)
        base.write_json(outdir/CHAIN_META,rec)

    if rec["status"]=="PARTIAL_SOFT_STOP":
        if not rec["resume_state_files_present"]:
            raise RuntimeError("Q041_PARTIAL_RESUME_STATE_GATE=FAIL")
        print(
            f"Q041_CHAIN_SEGMENT_GATE=PARTIAL arm={args.implementation} "
            f"combo={args.combo} chain={args.chain} segment={args.segment} "
            f"Rminus1={rec.get('checkpoint_Rminus1_last')}"
        )
        return 0
    if rec["status"]!="COMPLETE":
        raise RuntimeError("Q041_CHAIN_GATE=FAIL "+rec.get("error",rec.get("failure_class","")))
    print(
        f"Q041_CHAIN_GATE=PASS arm={args.implementation} combo={args.combo} "
        f"chain={args.chain} segment={args.segment}"
    )
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
                raise RuntimeError(
                    f"CONVERGENCE_GATE=FAIL arm={arm} combo={combo} rhat={rh.tolist()}"
                )
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
        "stage":"FINAL","status":"PASS","actual_computed_result":True,
        "scientific_classification":classification,
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
    s.add_argument("--soft-stop-minutes",type=int,default=SEGMENT_SOFT_STOP_DEFAULT)
    s.add_argument("--max-segments",type=int,default=MAX_SEGMENTS_DEFAULT)
    s.set_defaults(func=sample,chain_seed=0)

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
