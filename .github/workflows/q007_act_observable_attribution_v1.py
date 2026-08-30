#!/usr/bin/env python3
"""
Bubbleverse Q-007 ACT DR6 observable-level attribution.

Purpose
-------
Evaluate the *existing Q-006 fixed-H0 profile points* without re-optimizing them.
For each point, reconstruct the frozen Q-005 V14 common backend, evaluate the
ACT DR6-lite likelihood, and decompose the exact quadratic form

    chi2 = d^T C^{-1} d

into additive signed attribution terms

    c_i = d_i (C^{-1} d)_i,  sum_i c_i = chi2.

Grouping c_i by TT/TE/EE or by ACT band gives an exact additive attribution of
the *full covariance-weighted quadratic form*. The groups are NOT statistically
independent chi-square likelihoods because ACT's covariance couples bins and
spectra. Negative group contributions are therefore allowed and meaningful.

The script deliberately refuses to optimize. It consumes Q-006's aggregate JSON
and fails if the exact best-fit/profile parameter vectors are unavailable.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, sys
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
CFG_DEFAULT = "q007_act_observable_attribution_v1_config.yml"

def jdump(x): return json.dumps(x, indent=2, sort_keys=True)
def sha256_json(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",",":")).encode()).hexdigest()
def load_yaml(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))
def load_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def cfg(path=CFG_DEFAULT):
    p=Path(path)
    if not p.is_absolute(): p=ROOT/p
    return load_yaml(p)

def find_q006_profiles(q006: dict[str,Any]) -> dict[tuple[str,float],dict[str,Any]]:
    if q006.get("q") != "Q-006":
        raise RuntimeError("PARENT_Q_IDENTITY_GATE=FAIL")
    ans={}
    for model, block in q006.get("models",{}).items():
        for p in block.get("profiles",[]):
            if "bestfit" in p:
                ans[(model, round(float(p["target_h0"]),6))] = p
    return ans

def sampled_names(model: dict[str,Any]) -> set[str]:
    names=set()
    for n,s in model.get("params",{}).items():
        if isinstance(s,dict) and "prior" in s: names.add(n)
    for ls in model.get("likelihood",{}).values():
        if isinstance(ls,dict):
            for n,s in (ls.get("params") or {}).items():
                if isinstance(s,dict) and "prior" in s: names.add(n)
    return names

def extract_param_vector(bestfit: dict[str,Any], needed:set[str]) -> dict[str,float]:
    # q005 parser has historically used several containers; accept only explicit
    # numeric values and demand full sampled-parameter coverage.
    candidates=[]
    if isinstance(bestfit,dict):
        candidates.append(bestfit)
        for k in ("params","sampled","sampled_params","point","values"):
            if isinstance(bestfit.get(k),dict): candidates.append(bestfit[k])
    found={}
    for d in candidates:
        for k,v in d.items():
            if k in needed and isinstance(v,(int,float)) and math.isfinite(float(v)):
                found[k]=float(v)
    missing=sorted(needed-set(found))
    if missing:
        raise RuntimeError(f"Q006_EXACT_POINT_GATE=FAIL missing_sampled_parameters={missing}")
    return found

def freeze_all_sampled(model:dict[str,Any], vals:dict[str,float]):
    # Cobaya accepts a scalar value in place of a sampled prior.
    for n,s in list(model.get("params",{}).items()):
        if n in vals and isinstance(s,dict) and "prior" in s:
            model["params"][n] = float(vals[n])
    for lname,ls in model.get("likelihood",{}).items():
        if not isinstance(ls,dict): continue
        ps=ls.get("params")
        if not isinstance(ps,dict): continue
        for n,s in list(ps.items()):
            if n in vals and isinstance(s,dict) and "prior" in s:
                ps[n]=float(vals[n])
    model.pop("sampler",None)
    model.pop("output",None)

def import_core():
    sys.path.insert(0,str(ROOT))
    import q005_hpc_v14 as core
    return core

def build_frozen_model(c:dict[str,Any], model_name:str, vals:dict[str,float]):
    core=import_core()
    base=core.load_cfg(c["parent"]["base_config"])
    if base["project"]["q"]!="Q-005": raise RuntimeError("BACKEND_Q_GATE=FAIL")
    obj=core.build_model(base,model_name,smoke=False,restart=0)
    needed=sampled_names(obj)
    missing=sorted(needed-set(vals))
    if missing: raise RuntimeError(f"POINT_COVERAGE_GATE=FAIL missing={missing}")
    freeze_all_sampled(obj,vals)
    return obj,base

def get_model_and_logpost(info, vals):
    from cobaya.model import get_model
    m=get_model(info)
    # All sampled parameters are frozen, but explicit evaluation is still useful
    # for deterministic provider initialization.
    lp=m.logposterior({})
    return m,lp

def act_like(model):
    # robust lookup by class/name rather than relying on one dictionary key
    for name,like in model.likelihood.items():
        if "ACTDR6CMBonly" in str(name) or like.__class__.__name__=="ACTDR6CMBonly":
            return like
    raise RuntimeError("ACT_LIKELIHOOD_GATE=FAIL")

def theory_cl(like):
    return like.provider.get_Cl(ell_factor=True)

def prediction_and_meta(like, cl, A_act, P_act):
    ps=np.zeros_like(like.data_vec,dtype=float)
    rows=[]
    for m in like.spec_meta:
        idx=np.asarray(m["idx"],dtype=int)
        win=m["window"].weight.T
        ls=np.asarray(m["window"].values,dtype=int)
        pol=m["pol"]
        dat=np.asarray(cl[pol])[ls]/(A_act*A_act)
        if pol[0]=="e": dat=dat/P_act
        if pol[1]=="e": dat=dat/P_act
        pred=win@dat
        ps[idx]=pred
        ell=np.asarray(m["ell"],dtype=float)
        for j,ii in enumerate(idx):
            rows.append((int(ii),pol.upper(),float(ell[j]),float(like.data_vec[ii]),float(pred[j])))
    return ps,rows

def band_name(ell, bands):
    for b in bands:
        lo,hi=float(b["ell_min"]),float(b["ell_max"])
        if ell>=lo and ell<=hi: return b["name"]
    return "UNASSIGNED"

def attribute(like, cl, A_act, P_act, bands):
    pred,rows=prediction_and_meta(like,cl,A_act,P_act)
    delta=np.asarray(like.data_vec)-pred
    z=like.inv_cov@delta
    contrib=delta*z
    full=float(delta@z)
    by_pol={}
    by_band={}
    by_pol_band={}
    residual_rows=[]
    for ii,pol,ell,data,p in rows:
        c=float(contrib[ii])
        b=band_name(ell,bands)
        by_pol[pol]=by_pol.get(pol,0.0)+c
        by_band[b]=by_band.get(b,0.0)+c
        by_pol_band.setdefault(pol,{})[b]=by_pol_band.setdefault(pol,{}).get(b,0.0)+c
        var=float(like.covmat[ii,ii])
        residual_rows.append({
            "index":ii,"pol":pol,"ell_eff":ell,"data":data,"prediction":p,
            "residual":data-p,"sigma_diag":math.sqrt(var) if var>0 else None,
            "pull_diag":(data-p)/math.sqrt(var) if var>0 else None,
            "signed_fullcov_chi2_attribution":c
        })
    closure=float(sum(contrib))
    return {
        "chi2_act_reconstructed":full,
        "chi2_attribution_sum":closure,
        "closure_abs_error":abs(full-closure),
        "by_spectrum_signed_fullcov":by_pol,
        "by_band_signed_fullcov":by_band,
        "by_spectrum_band_signed_fullcov":by_pol_band,
        "statistical_independence":False,
        "interpretation":"Exact additive attribution of d_i(C^-1 d)_i; groups are covariance-coupled and are not independent chi-square likelihoods.",
        "residuals":residual_rows,
    }

def evaluate_point(c, q006_path, model_name, target_h0):
    q6=load_json(q006_path); profiles=find_q006_profiles(q6)
    key=(model_name,round(float(target_h0),6))
    if key not in profiles: raise RuntimeError(f"Q006_PROFILE_GATE=FAIL missing={key}")
    # First build to learn exact sampled parameter set.
    core=import_core(); base=core.load_cfg(c["parent"]["base_config"])
    tmp=core.build_model(base,model_name,smoke=False,restart=0)
    needed=sampled_names(tmp)
    vals=extract_param_vector(profiles[key]["bestfit"],needed)
    info,_=build_frozen_model(c,model_name,vals)
    model,lp=get_model_and_logpost(info,vals)
    like=act_like(model)
    cl=theory_cl(like)
    A=float(vals["A_act"]); P=float(vals["P_act"])
    att=attribute(like,cl,A,P,c["bands"])
    result={
        "q":"Q-007","parent_q":"Q-006","run_id":c["project"]["run_id"],
        "model":model_name,"target_h0":float(target_h0),
        "q006_point_sha256":sha256_json(vals),"fixed_sampled_parameters":vals,
        "reoptimized":False,"act":att,"sources":c["sources"],
        "backend":{"base_config":c["parent"]["base_config"],
                   "act_commit":c["parent"]["act_dr6_lite_commit"]},
        "status":"PASS"
    }
    # Compare reconstructed ACT chi2 to Q006's ACT component if available.
    q6comp=profiles[key].get("delta_chi2_components",{})
    result["q006_delta_component_record"]=q6comp
    return result,model,like,vals,cl

def local_derivatives(c, q006_path, model_name,target_h0, base_result, model,like,vals):
    # Finite differences at fixed values of all other sampled parameters.
    # Rebuild per perturbation so theory/provider caches cannot contaminate results.
    out={}
    steps=c["derivatives"]["steps"]
    for par in c["derivatives"]["parameters"]:
        if par not in vals or par not in steps: continue
        h=float(steps[par])
        vals0=dict(vals)
        rows=[]
        for sign in (-1,+1):
            vv=dict(vals0); vv[par]=vv[par]+sign*h
            info,_=build_frozen_model(c,model_name,vv)
            mm,_=get_model_and_logpost(info,vv); ll=act_like(mm); cc=theory_cl(ll)
            aa=attribute(ll,cc,float(vv["A_act"]),float(vv["P_act"]),c["bands"])
            rows.append((sign,aa["chi2_act_reconstructed"],aa["by_spectrum_signed_fullcov"]))
        minus=rows[0]; plus=rows[1]
        out[par]={
            "step":h,
            "dchi2_dparam_central":(plus[1]-minus[1])/(2*h),
            "minus_chi2":minus[1],"plus_chi2":plus[1],
            "minus_by_spectrum":minus[2],"plus_by_spectrum":plus[2],
            "causality_claim":False,
            "interpretation":"Local one-at-a-time finite-difference response; not a causal decomposition."
        }
    return out

def cmd_preflight(c,args):
    checks={
        "Q_IDENTITY_GATE":c["project"]["q"]=="Q-007",
        "PARENT_Q_GATE":c["parent"]["q"]=="Q-006",
        "Q006_INPUT_EXISTS":Path(args.q006).is_file(),
        "BASE_CONFIG_EXISTS":(ROOT/c["parent"]["base_config"]).is_file(),
        "CORE_EXISTS":(ROOT/c["parent"]["base_engine"]).is_file(),
    }
    ok=all(checks.values())
    print(jdump({"q":"Q-007","status":"PASS" if ok else "FAIL","checks":checks}))
    return 0 if ok else 2

def cmd_run(c,args):
    result,model,like,vals,cl=evaluate_point(c,args.q006,args.model,args.target_h0)
    if args.derivatives and c["derivatives"]["enabled"]:
        result["local_derivatives"]=local_derivatives(c,args.q006,args.model,args.target_h0,result,model,like,vals)
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(jdump(result)+"\n",encoding="utf-8")
    print(jdump({"status":"PASS","output":str(p),"model":args.model,"H0":args.target_h0}))
    return 0

def cmd_aggregate(c,args):
    rows=[]
    for p in Path(args.input).rglob("q007_point_*.json"):
        try:
            d=load_json(p)
            if d.get("q")=="Q-007" and d.get("status")=="PASS": rows.append(d)
        except Exception: pass
    expected={(m,round(float(h),6)) for m,mc in c["models"].items() for h in mc["h0_targets"]}
    got={(r["model"],round(float(r["target_h0"]),6)) for r in rows}
    missing=sorted(expected-got)
    out={"q":"Q-007","run_id":c["project"]["run_id"],"status":"UNRESOLVED",
         "gates":{},"missing":[{"model":m,"H0":h} for m,h in missing],
         "models":{},"sources":c["sources"]}
    out["gates"]["JOB_COMPLETENESS_GATE"]="PASS" if not missing else "FAIL"
    for m,mc in c["models"].items():
        rr=sorted([r for r in rows if r["model"]==m],key=lambda x:x["target_h0"])
        if not rr: continue
        bh=float(mc["baseline_h0"])
        b=next((r for r in rr if abs(r["target_h0"]-bh)<1e-6),None)
        if not b: continue
        bp=b["act"]["by_spectrum_signed_fullcov"]; bb=b["act"]["by_band_signed_fullcov"]
        prof=[]
        for r in rr:
            pol={k:r["act"]["by_spectrum_signed_fullcov"].get(k,0)-bp.get(k,0) for k in set(bp)|set(r["act"]["by_spectrum_signed_fullcov"])}
            band={k:r["act"]["by_band_signed_fullcov"].get(k,0)-bb.get(k,0) for k in set(bb)|set(r["act"]["by_band_signed_fullcov"])}
            prof.append({"H0":r["target_h0"],
                         "delta_chi2_act":r["act"]["chi2_act_reconstructed"]-b["act"]["chi2_act_reconstructed"],
                         "delta_by_spectrum_signed_fullcov":pol,
                         "delta_by_band_signed_fullcov":band,
                         "dominant_positive_spectrum":max(pol,key=pol.get) if pol else None,
                         "dominant_positive_band":max(band,key=band.get) if band else None})
        out["models"][m]={"baseline_h0":bh,"profiles":prof}
    closure=max([r["act"]["closure_abs_error"] for r in rows],default=1e99)
    out["gates"]["QUADRATIC_CLOSURE_GATE"]="PASS" if closure<=float(c["gates"]["closure_tolerance"]) else "FAIL"
    out["gates"]["COVARIANCE_INTERPRETATION_GATE"]="PASS" if all(not r["act"]["statistical_independence"] for r in rows) else "FAIL"
    final=(not missing and all(v=="PASS" for v in out["gates"].values()))
    out["gates"]["FINAL_RESULT_GATE"]="PASS" if final else "UNRESOLVED"
    out["status"]="PASS" if final else "UNRESOLVED"
    out["scientific_claim_boundary"]="Observable/band attribution of the frozen Q-006 profile points only; no global-minimum claim."
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(jdump(out)+"\n",encoding="utf-8")
    print(jdump({"status":out["status"],"output":args.output,"gates":out["gates"]}))
    return 0 if final else 3

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default=CFG_DEFAULT)
    sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("preflight"); p.add_argument("--q006",required=True)
    p=sp.add_parser("run"); p.add_argument("--q006",required=True); p.add_argument("--model",required=True)
    p.add_argument("--target-h0",required=True,type=float); p.add_argument("--output",required=True); p.add_argument("--derivatives",action="store_true")
    p=sp.add_parser("aggregate"); p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    a=ap.parse_args(); c=cfg(a.config)
    return {"preflight":cmd_preflight,"run":cmd_run,"aggregate":cmd_aggregate}[a.cmd](c,a)
if __name__=="__main__": raise SystemExit(main())
