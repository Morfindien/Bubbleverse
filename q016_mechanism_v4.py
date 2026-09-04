#!/usr/bin/env python3
"""
Q016 CMB mechanism stage V1.

Purpose:
- NEVER re-optimize the certified V16 cosmological profiles.
- Evaluate the exact certified free/fixed endpoints.
- Reuse Q015 V2 covariance-residual machinery for Planck/SPT.
- Reuse Q009 V8 ACT SACC/covariance machinery.
- Attempt official full multifrequency secondary diagnostics with cosmology frozen.
- Preserve structured TECHNICALLY_UNAVAILABLE instead of inventing numbers.

This program does not choose Q016-A/B/C. It produces the finite diagnostic evidence
needed by Result Ingestion to make that scientific decision.
"""
from __future__ import annotations
import argparse, copy, inspect, json, math, os, sys, time, traceback
from pathlib import Path
from typing import Any, Mapping
import numpy as np
import yaml

ROOT=Path(__file__).resolve().parent
Q="Q016"
RUN="Q016-CMB-MECHANISM-V4"
RESULT="R-Q016-EDE-CMB-MECHANISM-004"

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True,default=_json_default)+"\n")
    os.replace(tmp,p)

def _json_default(x):
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,(np.floating,np.integer)): return x.item()
    return str(x)

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def load_cfg(path):
    c=yaml.safe_load(Path(path).read_text())
    p=c["project"]
    if p["q"]!=Q: raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if p["run_id"]!=RUN or p["result_id"]!=RESULT: raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    if c["parent_v16"]["primary_profiles_must_not_be_rerun"] is not True:
        raise RuntimeError("NO_PRIMARY_RERUN_GATE=FAIL")
    return c

def load_endpoint_lock(cfg):
    d=json.loads((ROOT/cfg["parent_v16"]["lock_file"]).read_text())
    p=d["parent"]
    if d.get("q")!=Q: raise RuntimeError("ENDPOINT_LOCK_Q_GATE=FAIL")
    if p.get("run_id")!="Q016-MATCHED-CMB-SURFACE-V16":
        raise RuntimeError("ENDPOINT_LOCK_RUN_GATE=FAIL")
    if p.get("result_id")!="R-Q016-EDE-MATCHED-CMB-SURFACE-016":
        raise RuntimeError("ENDPOINT_LOCK_RESULT_GATE=FAIL")
    if int(p.get("github_run_id",-1))!=33785257733:
        raise RuntimeError("ENDPOINT_LOCK_GITHUB_GATE=FAIL")
    if p.get("head_sha")!="3a154b44cbef4b2a3d10fdb12435105921bfc962":
        raise RuntimeError("ENDPOINT_LOCK_SHA_GATE=FAIL")
    if p.get("primary_endpoint_gate")!="PASS" or p.get("scientifically_usable_primary_endpoint_result") is not True:
        raise RuntimeError("ENDPOINT_LOCK_SCIENCE_GATE=FAIL")
    return d

def endpoint(lock,branch,mode):
    return lock["endpoints"][branch][mode]

def endpoint_values(lock,branch,mode):
    e=endpoint(lock,branch,mode)
    vals=dict(e["minimum"])
    if mode=="fixed_h0_71p5":
        vals["H0"]=71.5
    return vals

def _freeze_sampled_params(info,values):
    """
    Convert every sampled parameter in the already-correct Q016 V16 model definition
    to an exact scalar value from the certified endpoint. Derived/constant parameters
    are retained. This is an evaluation model, never an optimizer.
    """
    params=info.setdefault("params",{})
    unresolved=[]
    for name,spec in list(params.items()):
        if isinstance(spec,dict) and "prior" in spec:
            if name not in values:
                unresolved.append(name)
            else:
                params[name]=float(values[name])
    if unresolved:
        raise RuntimeError("ENDPOINT_PARAMETER_COMPLETENESS_GATE=FAIL "+repr(unresolved))
    info.pop("sampler",None)
    info.pop("output",None)
    info.pop("resume",None)
    info.pop("force",None)
    return info

def build_certified_point_model(cfg,lock,branch,mode):
    # Exact known-good V16 model/likelihood construction, but no sampler.
    import q016_objective_reprofile_v16 as q16
    from cobaya.model import get_model
    v16cfg=yaml.safe_load((ROOT/"q016_matched_cmb_surface_v16_config.yml").read_text())
    vals=endpoint_values(lock,branch,mode)
    info=q16.base_info(v16cfg,branch,mode,0,ROOT/"_q016_mechanism_eval")
    if branch=="planck": q16.configure_planck(info,v16cfg)
    elif branch=="spt": q16.configure_spt(info,v16cfg)
    elif branch=="act": q16.configure_act(info,v16cfg)
    else: raise RuntimeError("BRANCH_GATE=FAIL")
    q16.configure_exact_objective(info,branch,v16cfg)
    info=_freeze_sampled_params(info,vals)
    model=get_model(info)
    lp=model.logposterior({})
    if not finite(lp.logpost):
        raise RuntimeError("FINITE_ENDPOINT_EVALUATION_GATE=FAIL")
    # Critical Q015 V2 repair: transport expanded constant params before direct
    # likelihood diagnostics, then endpoint values override.
    expanded=dict(model.parameterization.constant_params())
    expanded.update(vals)
    return model, expanded, lp

def _trace_return_locals(func,*args,**kwargs):
    """
    Reuse Q015's proven residual construction without copying/reimplementing its
    likelihood-private vector logic. Capture selected local arrays at function return.
    """
    captured={}
    old=sys.gettrace()
    def tracer(frame,event,arg):
        if frame.f_code is func.__code__:
            if event=="return":
                for k,v in frame.f_locals.items():
                    if k in {"delta","labels","contrib","cov","cinv","like","clike","wrapper","pars"}:
                        captured[k]=v
            return tracer
        return tracer
    sys.settrace(tracer)
    try:
        result=func(*args,**kwargs)
    finally:
        sys.settrace(old)
    return result,captured

def _band_name(ell,bands):
    for b in bands:
        if float(b["min"])<=float(ell)<=float(b["max"]):
            return str(b["name"])
    return "outside_common"

def _norm_pol(x):
    s=str(x).upper().replace("ET","TE")
    if "TT" in s: return "TT"
    if "TE" in s: return "TE"
    if "EE" in s: return "EE"
    return s

def _extract_meta_ell(meta):
    for k in ("ell","ell_eff","effective_ell","leff","l_eff"):
        if k in meta and finite(meta[k]): return float(meta[k])
    return float("nan")

def _extract_meta_pol(meta):
    for k in ("type","pol","spectrum_type","spec_type"):
        if k in meta: return _norm_pol(meta[k])
    s=str(meta.get("spectrum",""))
    return _norm_pol(s)

def _extract_meta_spectrum(meta):
    for k in ("spectrum","spec","name","label"):
        if k in meta: return str(meta[k])
    return _extract_meta_pol(meta)

def _cov_from_capture(cap,n):
    for key in ("cov",):
        v=cap.get(key)
        if isinstance(v,np.ndarray) and v.ndim==2 and v.shape==(n,n): return np.asarray(v,dtype=float)
    for objkey in ("like","clike","wrapper"):
        obj=cap.get(objkey)
        if obj is None: continue
        for attr in ("covariance","covmat","cov"):
            v=getattr(obj,attr,None)
            if v is not None:
                a=np.asarray(v,dtype=float)
                if a.ndim==2 and a.shape==(n,n): return a
        candl_like=getattr(obj,"candl_like",None)
        if candl_like is not None:
            v=getattr(candl_like,"covariance",None)
            if v is not None:
                a=np.asarray(v,dtype=float)
                if a.ndim==2 and a.shape==(n,n): return a
    return None

def _residual_packet(delta,labels,cov,bands,inv_cov=None):
    d=np.asarray(delta,dtype=float)
    if len(labels)!=len(d): raise RuntimeError("RESIDUAL_LABEL_LENGTH_GATE=FAIL")
    if cov is None:
        raise RuntimeError("RESIDUAL_COVARIANCE_GATE=FAIL")
    if inv_cov is None:
        cinv=np.linalg.pinv(np.asarray(cov,dtype=float),rcond=1e-12)
    else:
        cinv=np.asarray(inv_cov,dtype=float)
        if cinv.shape!=(len(d),len(d)):
            raise RuntimeError("RESIDUAL_INV_COVARIANCE_SHAPE_GATE=FAIL")
    contrib=d*(cinv@d)
    out=[]
    by_obs={}; by_band={}; by_obs_band={}; by_spec={}
    for i,(r,c,m) in enumerate(zip(d,contrib,labels)):
        ell=_extract_meta_ell(m); pol=_extract_meta_pol(m); spec=_extract_meta_spectrum(m)
        band=_band_name(ell,bands)
        var=float(cov[i,i]); sig=math.sqrt(var) if var>0 else None
        row={
            "index":i,"ell":ell,"observable":pol,"spectrum":spec,"common_band":band,
            "residual":float(r),"diag_sigma":sig,
            "diag_standardized_residual":(float(r)/sig if sig and sig>0 else None),
            "signed_fullcov_contribution":float(c),
        }
        out.append(row)
        by_obs[pol]=by_obs.get(pol,0.0)+float(c)
        by_band[band]=by_band.get(band,0.0)+float(c)
        by_obs_band.setdefault(pol,{})
        by_obs_band[pol][band]=by_obs_band[pol].get(band,0.0)+float(c)
        by_spec[spec]=by_spec.get(spec,0.0)+float(c)
    return {
        "residuals":out,
        "chi2_reconstructed":float(d@(cinv@d)),
        "signed_contribution_sum":float(np.sum(contrib)),
        "by_observable_signed_fullcov":by_obs,
        "by_common_band_signed_fullcov":by_band,
        "by_observable_band_signed_fullcov":by_obs_band,
        "by_spectrum_signed_fullcov":by_spec,
    }

def _primary_component(endpoint_rec,branch):
    m=endpoint_rec["minimum"]
    keys={
        "planck":"chi2__q016_camspec_npipe_lite",
        "spt":"chi2__q016_spt_d1_lite",
        "act":"chi2__q016_act_dr6_cmbonly",
    }
    return float(m[keys[branch]])

def _find_primary_like(model,branch):
    target={
        "planck":"q016_camspec_npipe_lite",
        "spt":"q016_spt_d1_lite",
        "act":"q016_act_dr6_cmbonly",
    }[branch]
    for name,like in model.likelihood.items():
        if target in str(name):
            return like
        cls=like.__class__.__name__
        if branch=="planck" and cls=="planck_Camspec_NPIPE_lite":
            return like
        if branch=="act" and cls=="ACTDR6CMBonly":
            return like
    raise RuntimeError(f"{branch.upper()}_PRIMARY_LIKELIHOOD_GATE=FAIL")

def _planck_lite_state(model,vals,bands):
    """Native adapter for the exact Q016 foreground-marginalized CamSpec NPIPE lite likelihood."""
    like=_find_primary_like(model,"planck")
    cl=like.provider.get_Cl(ell_factor=True)
    data=np.asarray(like.data_vec,dtype=float)
    pred=np.zeros_like(data,dtype=float)
    labels=[None]*len(data)
    cals={
        "tt":float(vals["A_planck"])**2,
        "te":float(vals["calTE"])*float(vals["A_planck"])**2,
        "ee":float(vals["calEE"])*float(vals["A_planck"])**2,
    }
    for meta in like.spec_meta:
        idx=np.asarray(meta["idx"],dtype=int)
        ell=np.asarray(meta["ell"],dtype=int)
        pol=str(meta["pol"]).lower()
        theory=np.asarray(cl[pol],dtype=float)[ell]/float(cals[pol])
        pred[idx]=theory
        tr1=str(meta.get("tracer1","?"))
        tr2=str(meta.get("tracer2","?"))
        for j,ii in enumerate(idx):
            labels[int(ii)]={
                "ell":float(ell[j]),
                "pol":pol.upper(),
                "spectrum":f"{pol.upper()} {tr1}x{tr2}",
                "tracer1":tr1,
                "tracer2":tr2,
            }
    for i,row in enumerate(labels):
        if row is None:
            labels[i]={
                "ell":float("nan"),
                "pol":"CULLED",
                "spectrum":"CULLED",
                "tracer1":"CULLED",
                "tracer2":"CULLED",
            }
    residual=data-pred
    packet=_residual_packet(
        residual,labels,np.asarray(like.covmat,dtype=float),bands,
        inv_cov=np.asarray(like.inv_cov,dtype=float)
    )
    packet["native_lite_adapter"]="camspec_npipe_lite.spec_meta/data_vec/covmat/inv_cov"
    packet["calibration_factors"]=cals
    packet["tracer_pairs"]=sorted({
        f'{m.get("tracer1","?")}x{m.get("tracer2","?")}' for m in like.spec_meta
    })
    return packet

def matched_planck(cfg,lock):
    branch="planck"; states={}
    bands=cfg["frozen_surface"]["common_bands"]
    for mode in ("reference_free_h0","fixed_h0_71p5"):
        model,vals,lp=build_certified_point_model(cfg,lock,branch,mode)
        packet=_planck_lite_state(model,vals,bands)
        packet["endpoint_objective_chi2"]=float(endpoint(lock,branch,mode)["objective_chi2"])
        packet["endpoint_primary_chi2"]=_primary_component(endpoint(lock,branch,mode),branch)
        packet["endpoint_h0"]=float(vals["H0"])
        packet["nuisance"]={
            "A_planck":float(vals["A_planck"]),
            "calTE":float(vals["calTE"]),
            "calEE":float(vals["calEE"]),
        }
        states[mode]=packet
        try:model.close()
        except Exception:pass
    return compare_endpoint_packets(cfg,lock,branch,states)

def matched_spt_q015(cfg,lock):
    # Reference implementation only. V4 imports the already successful V3 matched-SPT artifact.
    import q015_cmb_attribution_v2 as q15
    adapter=yaml.safe_load((ROOT/"q015_cmb_attribution_v2_config.yml").read_text())
    adapter["ell_bands"]=copy.deepcopy(cfg["frozen_surface"]["common_bands"])
    adapter["likelihood_names"]["spt_primary"]="q016_spt_d1_lite"
    states={}
    for mode in ("reference_free_h0","fixed_h0_71p5"):
        model,vals,lp=build_certified_point_model(cfg,lock,"spt",mode)
        state,cap=_trace_return_locals(q15.spt_primary_state,model,vals,adapter)
        delta=cap.get("delta"); labels=cap.get("labels")
        if delta is None or labels is None:
            raise RuntimeError("Q015_SPT_RESIDUAL_CAPTURE_GATE=FAIL")
        d=np.asarray(delta,dtype=float)
        cov=_cov_from_capture(cap,len(d))
        packet=_residual_packet(d,labels,cov,cfg["frozen_surface"]["common_bands"])
        packet["q015_state_summary"]={k:v for k,v in state.items() if not str(k).startswith("_")}
        packet["endpoint_objective_chi2"]=float(endpoint(lock,"spt",mode)["objective_chi2"])
        packet["endpoint_primary_chi2"]=_primary_component(endpoint(lock,"spt",mode),"spt")
        packet["endpoint_h0"]=float(vals["H0"])
        states[mode]=packet
        try:model.close()
        except Exception:pass
    return compare_endpoint_packets(cfg,lock,"spt",states)

def matched_act(cfg,lock):
    import q009_act_corrected_minima_attribution_v8 as q9
    branch="act"; states={}
    bands=cfg["frozen_surface"]["common_bands"]
    for mode in ("reference_free_h0","fixed_h0_71p5"):
        model,vals,lp=build_certified_point_model(cfg,lock,branch,mode)
        like=q9.act_like(model)
        cl=q9.theory_cl(like)
        pred,rows=q9.prediction_and_meta(like,cl,float(vals["A_act"]),float(vals["P_act"]))
        data=np.asarray(like.data_vec,dtype=float)
        cov=np.asarray(like.covmat,dtype=float)
        residual=data-np.asarray(pred,dtype=float)
        labels=[None]*len(residual)
        # Q009 V8 returns exact tuples:
        # (index, pol.upper(), ell, data_value, prediction_value)
        for ii,pol,ell,data_value,prediction_value in rows:
            i=int(ii)
            labels[i]={
                "ell":float(ell),
                "pol":str(pol).upper(),
                "spectrum":str(pol).upper(),
                "q009_data_value":float(data_value),
                "q009_prediction_value":float(prediction_value),
            }
        for i,row in enumerate(labels):
            if row is None:
                labels[i]={"ell":float("nan"),"pol":"CULLED","spectrum":"CULLED"}
        packet=_residual_packet(
            residual,labels,cov,bands,
            inv_cov=np.asarray(like.inv_cov,dtype=float)
        )
        packet["endpoint_objective_chi2"]=float(endpoint(lock,branch,mode)["objective_chi2"])
        packet["endpoint_primary_chi2"]=_primary_component(endpoint(lock,branch,mode),branch)
        packet["endpoint_h0"]=float(vals["H0"])
        packet["nuisance"]={"A_act":float(vals["A_act"]),"P_act":float(vals["P_act"])}
        states[mode]=packet
        try: model.close()
        except Exception: pass
    return compare_endpoint_packets(cfg,lock,branch,states)

def compare_endpoint_packets(cfg,lock,branch,states):
    free=states["reference_free_h0"]; fixed=states["fixed_h0_71p5"]
    rf=free["residuals"]; rx=fixed["residuals"]
    if len(rf)!=len(rx): raise RuntimeError("FREE_FIXED_VECTOR_LENGTH_GATE=FAIL")
    delta_rows=[]
    for a,b in zip(rf,rx):
        keya=(a["observable"],a["spectrum"],a["common_band"])
        keyb=(b["observable"],b["spectrum"],b["common_band"])
        if keya!=keyb: raise RuntimeError("FREE_FIXED_LABEL_ALIGNMENT_GATE=FAIL")
        delta_rows.append({
            "index":a["index"],"ell":a["ell"],"observable":a["observable"],
            "spectrum":a["spectrum"],"common_band":a["common_band"],
            "delta_residual_fixed_minus_free":float(b["residual"])-float(a["residual"]),
            "free_residual":a["residual"],"fixed_residual":b["residual"],
            "free_diag_standardized_residual":a["diag_standardized_residual"],
            "fixed_diag_standardized_residual":b["diag_standardized_residual"],
            "delta_signed_fullcov_contribution":
                float(b["signed_fullcov_contribution"])-float(a["signed_fullcov_contribution"]),
        })
    direct_primary_delta=float(fixed["endpoint_primary_chi2"])-float(free["endpoint_primary_chi2"])
    reconstructed_delta=float(fixed["chi2_reconstructed"])-float(free["chi2_reconstructed"])
    return {
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"MATCHED_RESIDUAL","branch":branch,
        "status":"PASS",
        "parent_v16":{"run_id":"Q016-MATCHED-CMB-SURFACE-V16","result_id":"R-Q016-EDE-MATCHED-CMB-SURFACE-016"},
        "free":free,"fixed":fixed,
        "delta":{
            "primary_chi2_fixed_minus_free":direct_primary_delta,
            "reconstructed_chi2_fixed_minus_free":reconstructed_delta,
            "residual_vector_fixed_minus_free":delta_rows,
            "by_observable_signed_fullcov":{
                k:float(fixed["by_observable_signed_fullcov"].get(k,0))-float(free["by_observable_signed_fullcov"].get(k,0))
                for k in sorted(set(free["by_observable_signed_fullcov"])|set(fixed["by_observable_signed_fullcov"]))
            },
            "by_common_band_signed_fullcov":{
                k:float(fixed["by_common_band_signed_fullcov"].get(k,0))-float(free["by_common_band_signed_fullcov"].get(k,0))
                for k in sorted(set(free["by_common_band_signed_fullcov"])|set(fixed["by_common_band_signed_fullcov"]))
            },
            "by_spectrum_signed_fullcov":{
                k:float(fixed["by_spectrum_signed_fullcov"].get(k,0))-float(free["by_spectrum_signed_fullcov"].get(k,0))
                for k in sorted(set(free["by_spectrum_signed_fullcov"])|set(fixed["by_spectrum_signed_fullcov"]))
            },
        },
        "interpretation_guard":{
            "signed_components_are_independent_chi2":False,
            "cross_chain_chi2_sum_performed":False,
            "combined_cross_experiment_sigma_performed":False,
            "shared_cosmic_variance_acknowledged":True,
        }
    }

def _theory_dls_from_model(model):
    d=model.provider.get_Cl(ell_factor=True,units="muK2")
    out={str(k):np.asarray(v,dtype=float) for k,v in d.items()}
    for upper,lower in (("TT","tt"),("TE","te"),("EE","ee"),("BB","bb")):
        if lower in out:
            out[upper]=out[lower]
    for required in ("TT","TE","EE"):
        if required not in out:
            raise RuntimeError(f"SPT_FULL_DL_KEY_GATE=FAIL missing={required}")
    if "ell" not in out:
        out["ell"]=np.arange(len(out["TT"]),dtype=int)
    return out

def secondary_planck(cfg,lock):
    # The primary CamSpec state is already multifrequency. Reuse the matched Planck
    # residual packet and expose endpoint nuisance movement + frequency directions.
    matched=matched_planck(cfg,lock)
    f=endpoint_values(lock,"planck","reference_free_h0")
    x=endpoint_values(lock,"planck","fixed_h0_71p5")
    spectrum_delta=matched["delta"]["by_spectrum_signed_fullcov"]
    wanted={}
    for key,val in spectrum_delta.items():
        s=str(key).replace(" ","").lower()
        if any(t in s for t in ("143x143","143x217","217x143","217x217")):
            wanted[key]=val
    return {
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"SECONDARY_MECHANISM","branch":"planck",
        "status":"PASS",
        "surface_role":"DIAGNOSTIC_ON_CERTIFIED_MATCHED_ENDPOINTS",
        "nuisance_free":{"A_planck":f.get("A_planck"),"calTE":f.get("calTE"),"calEE":f.get("calEE")},
        "nuisance_fixed":{"A_planck":x.get("A_planck"),"calTE":x.get("calTE"),"calEE":x.get("calEE")},
        "nuisance_shift_fixed_minus_free":{
            k:float(x[k])-float(f[k]) for k in ("A_planck","calTE","calEE")
        },
        "tt_frequency_signed_fullcov_delta":wanted,
        "frequency_specific_status":(
            "AVAILABLE_FROM_LITE_TRACER_LABELS" if wanted
            else "NOT_AVAILABLE_IN_FOREGROUND_MARGINALIZED_LITE_TRACER_LABELS"
        ),
        "all_spectrum_signed_fullcov_delta":spectrum_delta,
        "historical_context":"Q015 identified ell~500-999 and 143x217 structure; Q016 matched causal decision uses ell>=600 only.",
        "matched_residual_reference_embedded":True,
        "causal_claim_allowed":False,
    }

def _structured_unavailable(branch,exc,details=None):
    return {
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"SECONDARY_MECHANISM","branch":branch,
        "status":"TECHNICALLY_UNAVAILABLE",
        "failure_class":"SECONDARY_FULL_MULTIFREQUENCY_DIAGNOSTIC_UNAVAILABLE",
        "error":repr(exc),
        "details":details or {},
        "scientific_interpretation":"NONE",
        "primary_v16_result_invalidated":False,
        "rerun_primary_profiles":False,
    }

def _load_official_spt_full():
    import candl, spt_candl_data
    shortcut=getattr(spt_candl_data,"SPT3G_D1_TnE")
    # The full MF diagnostic is deliberately cropped to the matched primary window.
    return candl.Like(shortcut,data_selection=["ell<600 remove","ell>2000 remove"])

def _candl_default_nuisance_from_priors(like):
    vals={}
    # Gaussian priors in candl provide a scientifically native center.
    for pr in getattr(like,"priors",[]):
        names=list(getattr(pr,"par_names",[]))
        mean=np.atleast_1d(getattr(pr,"central_value",getattr(pr,"mean",[])))
        for i,n in enumerate(names):
            if len(mean)>i and finite(mean[i]): vals[str(n)]=float(mean[i])
    # Conservative conventional identity/zero defaults are permitted ONLY as an
    # optimizer initial point; they are never reported as a result unless optimized.
    for n in getattr(like,"required_nuisance_parameters",[]):
        if n in vals: continue
        low=str(n).lower()
        vals[n]=1.0 if any(k in low for k in ("cal","beta_pol","pol_eff","eff")) else 0.0
    return vals

def _candl_params(Dls,nuis):
    # candl's public API expects theory Dls under "Dl".
    return {"Dl":Dls,**nuis}

def _profile_candl_nuisance(like,Dls,start,maxiter=2500):
    """
    Nuisance-only profiling. The cosmological CMB spectra are frozen.
    Internal candl priors remain part of the full chain-native diagnostic.
    No cosmological parameter is allowed to move.
    """
    from scipy.optimize import minimize
    names=list(getattr(like,"required_nuisance_parameters",[]))
    x0=np.array([float(start[n]) for n in names],dtype=float)
    def f(x):
        p=_candl_params(Dls,{n:float(v) for n,v in zip(names,x)})
        # candl log_like is positive -logL; include official internal priors if present.
        val=float(like.log_like(p))
        try: val+=float(like.prior_logl(p))
        except Exception: pass
        return val
    res=minimize(f,x0,method="Powell",options={"maxiter":int(maxiter),"xtol":1e-5,"ftol":1e-6})
    if not finite(res.fun): raise RuntimeError("SPT_FULL_NUISANCE_FINITE_GATE=FAIL")
    nuis={n:float(v) for n,v in zip(names,res.x)}
    return nuis,{"success":bool(res.success),"message":str(res.message),"objective_minusloglike":float(res.fun),"nfev":int(res.nfev)}

def _candl_full_state(like,Dls,nuis,bands):
    params=_candl_params(Dls,nuis)
    model_specs=np.asarray(like.get_model_specs(params),dtype=float)
    binned=np.asarray(like.bin_model_specs(model_specs),dtype=float)
    data=np.asarray(like.data_bandpowers,dtype=float)
    cov=np.asarray(like.covariance,dtype=float)
    residual=data-binned
    labels=[]
    # candl exposes exact spectrum order/frequency and effective ell arrays.
    ix=0
    eff=np.asarray(like.effective_ells,dtype=float)
    for i,(spec,n) in enumerate(zip(like.spec_order,like.N_bins)):
        n=int(n)
        typ=str(like.spec_types[i]) if i<len(like.spec_types) else str(spec).split()[0]
        freqs=like.spec_freqs[i] if i<len(like.spec_freqs) else ["?","?"]
        for j in range(n):
            labels.append({
                "ell":float(eff[ix+j]),
                "pol":typ,
                "spectrum":f"{typ} {freqs[0]}x{freqs[1]}",
                "freq1":str(freqs[0]),"freq2":str(freqs[1]),
            })
        ix+=n
    return _residual_packet(residual,labels,cov,bands)

def secondary_spt(cfg,lock):
    try:
        like=_load_official_spt_full()
        start=_candl_default_nuisance_from_priors(like)
        states={}
        for mode in ("reference_free_h0","fixed_h0_71p5"):
            model,vals,lp=build_certified_point_model(cfg,lock,"spt",mode)
            Dls=_theory_dls_from_model(model)
            nuis,opt=_profile_candl_nuisance(like,Dls,start)
            state=_candl_full_state(like,Dls,nuis,cfg["frozen_surface"]["common_bands"])
            state["nuisance_bestfit"]=nuis; state["optimizer"]=opt; state["endpoint_h0"]=vals["H0"]
            states[mode]=state
            start=nuis
            try:model.close()
            except Exception:pass
        # Frequency/nuisance secondary diagnostic only.
        return {
            "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"SECONDARY_MECHANISM","branch":"spt",
            "status":"PASS",
            "surface_role":"OFFICIAL_FULL_MULTIFREQUENCY_DIAGNOSTIC_WITH_COSMOLOGY_FROZEN",
            "free":states["reference_free_h0"],"fixed":states["fixed_h0_71p5"],
            "nuisance_shift_fixed_minus_free":{
                k:float(states["fixed_h0_71p5"]["nuisance_bestfit"].get(k,0))-
                  float(states["reference_free_h0"]["nuisance_bestfit"].get(k,0))
                for k in sorted(set(states["fixed_h0_71p5"]["nuisance_bestfit"])|
                                set(states["reference_free_h0"]["nuisance_bestfit"]))
            },
            "primary_surface_replaced":False,
            "causal_claim_allowed":False,
        }
    except Exception as exc:
        return _structured_unavailable("spt",exc,{"traceback":traceback.format_exc()[-8000:]})

def secondary_act(cfg,lock):
    """
    ACT full-MF is intentionally capability-gated. The official package is pinned.
    We do not fabricate a nuisance model by guessing its private API. If the official
    package exposes a directly usable Cobaya likelihood in this environment, record
    capability metadata; otherwise emit TECHNICALLY_UNAVAILABLE. The mandatory ACT
    matched-lite residual is still computed independently in matched_act().
    """
    try:
        import act_dr6_mflike
        pkgfile=str(Path(act_dr6_mflike.__file__).resolve())
        # Inspect the official YAML/systematics resources. A full nuisance-only fit
        # is allowed only if the package exposes a callable Cobaya likelihood class
        # and installed data resources are discoverable.
        pkgroot=Path(pkgfile).parent
        yaml_path=pkgroot/"act_dr6.yaml"
        sys_path=pkgroot/"params_systematics.yaml"
        if not yaml_path.exists() or not sys_path.exists():
            raise RuntimeError("ACT_FULL_MF_RESOURCE_GATE=FAIL")
        y=yaml.safe_load(yaml_path.read_text())
        sy=yaml.safe_load(sys_path.read_text())
        # V1 deliberately refuses to guess a private evaluator contract. This is a
        # structured capability result, not a scientific failure. The exact package
        # inventory is returned so a V2 patch, if materially required after ingestion,
        # can target the official API without reopening V16 profiles.
        raise RuntimeError(
            "ACT_FULL_MF_EVALUATOR_ADAPTER_NOT_YET_CERTIFIED: official package/resources present; "
            "do not infer full-MF numbers until adapter is reference-tested"
        )
    except Exception as exc:
        return _structured_unavailable("act",exc,{
            "required_repository":"ACTCollaboration/act_dr6_mflike",
            "required_commit":"4220e14efb3a995f47c9f54cb687479e558c6138",
            "traceback":traceback.format_exc()[-8000:]
        })

def run_matched(cfg,lock,branch):
    if branch=="planck": return matched_planck(cfg,lock)
    if branch=="spt": return matched_spt_q015(cfg,lock)
    if branch=="act": return matched_act(cfg,lock)
    raise RuntimeError("BRANCH_GATE=FAIL")

def run_secondary(cfg,lock,branch):
    if branch=="planck": return secondary_planck(cfg,lock)
    if branch=="spt": return secondary_spt(cfg,lock)
    if branch=="act": return secondary_act(cfg,lock)
    raise RuntimeError("BRANCH_GATE=FAIL")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("matched"); a.add_argument("--branch",choices=["planck","spt","act"],required=True); a.add_argument("--output",required=True)
    b=sub.add_parser("secondary"); b.add_argument("--branch",choices=["planck","spt","act"],required=True); b.add_argument("--output",required=True)
    args=ap.parse_args()
    cfg=load_cfg(args.config); lock=load_endpoint_lock(cfg)
    try:
        if args.cmd=="matched": out=run_matched(cfg,lock,args.branch)
        else: out=run_secondary(cfg,lock,args.branch)
    except Exception as exc:
        out={
            "q":Q,"run_id":RUN,"result_id":RESULT,"stage":args.cmd.upper(),"branch":args.branch,
            "status":"FAIL","failure_class":"EXECUTION","error":repr(exc),
            "traceback":traceback.format_exc()[-12000:],
            "primary_v16_result_invalidated":False,
        }
        write_json(args.output,out)
        raise
    write_json(args.output,out)

if __name__=="__main__":
    main()
