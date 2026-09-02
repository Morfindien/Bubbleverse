#!/usr/bin/env python3
"""Bubbleverse Q016 V3 branch runner.

This file is deliberately fail-fast. It performs real Cobaya minimisation only when
the required external likelihood adapters are installed and immutably pinned.
It never substitutes Q011's exact vector as an external endpoint and never combines
absolute chi2 across experiments.
"""
from __future__ import annotations
import argparse, json, math, os, signal, time, hashlib
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT = Path(__file__).resolve().parent
CURRENT_Q = "Q016"
RUN_ID = "Q016-MATCHED-CMB-SURFACE-V3"
RESULT_ID = "R-Q016-EDE-MATCHED-CMB-SURFACE-003"

def load_cfg(path):
    d=yaml.safe_load(Path(path).read_text())
    if d["project"]["q"] != CURRENT_Q: raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    return d

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n"); os.replace(t,p)

def base_info(cfg, branch, mode, restart, output_prefix):
    # Reuse Bubbleverse's frozen Q005/Q014 numerical parameterisation instead of rebuilding it.
    import q014_external_viability_v5 as q14
    q14cfg=yaml.safe_load((ROOT/"q014_external_viability_v12_config.yml").read_text())
    template = "spt_d1_only" if branch=="spt" else "planck_npipe_k039_approx"
    info,_ = q14.build_info(template, "reference_free_h0", "external", restart,
                            q14cfg, {}, output_prefix,
                            max_evals=int(cfg["execution"]["optimizer"]["max_evals"]))
    # Remove every old likelihood/prior: Q016 constructs a primary-CMB-only surface.
    info["likelihood"]={}
    info["prior"]={}
    # Strip foreign chain nuisances before the new chain likelihood declares its own.
    foreign={"A_planck","calTE","calEE","amp_143","amp_217","amp_143x217",
             "n_143","n_217","n_143x217","Tcal","Ecal","A_act","P_act"}
    params=info.setdefault("params",{})
    for k in list(params):
        if k in foreign: params.pop(k,None)
    if mode=="fixed_h0_71p5":
        params["H0"]=float(cfg["model"]["target_h0"])
    # Shared tau information: same shape in all three chains.
    mu=float(cfg["surface"]["tau"]["mean"]); sig=float(cfg["surface"]["tau"]["sigma"])
    info["prior"]["q016_tau_information"]=f"lambda tau_reio: stats.norm.logpdf(tau_reio, loc={mu!r}, scale={sig!r})"
    m=info.setdefault("sampler",{}).setdefault("minimize",{})
    m["max_evals"]=int(cfg["execution"]["optimizer"]["max_evals"])
    m.setdefault("override_bobyqa",{})["rhoend"]=float(cfg["execution"]["optimizer"]["rhoend"])
    return info

def configure_spt(info,cfg):
    from candl.interface import CandlCobayaLikelihood
    import spt_candl_data
    sel=["ell<600 remove","ell>2000 remove"]
    info["likelihood"]["q016_spt_d1_lite"]={
        "external":CandlCobayaLikelihood,
        "data_set_file":spt_candl_data.SPT3G_D1_TnE_lite,
        "data_selection":sel,
        "clear_internal_priors":True,
        "feedback":True,
        "additional_args":{},
        "wrapper":None,
    }
    p=info["params"]
    p["Tcal"]={"prior":{"min":0.8,"max":1.2},"ref":1.0,"proposal":0.0036}
    p["Ecal"]={"prior":{"min":0.8,"max":1.2},"ref":1.0,"proposal":0.01}
    mu=cfg["branches"]["spt"]["Tcal_constraint"]["mean"]; s=cfg["branches"]["spt"]["Tcal_constraint"]["sigma"]
    info["prior"]["q016_spt_Tcal"]=f"lambda Tcal: stats.norm.logpdf(Tcal, loc={float(mu)!r}, scale={float(s)!r})"

def configure_act(info,cfg):
    # Official ACT DR6 CMB-only Cobaya likelihood.
    # Exact import is validated before expensive execution.
    try:
        from act_dr6_cmbonly import ACTDR6CMBonly
    except Exception as exc:
        raise RuntimeError("ACT_LIKELIHOOD_IMPORT_GATE=FAIL: "+repr(exc))
    info["likelihood"]["q016_act_dr6_cmbonly"]={
        "external":ACTDR6CMBonly,
        "ell_cuts":{"TT":[600,2000],"TE":[600,2000],"EE":[600,2000]},
        "stop_at_error":True,
    }
    p=info["params"]
    p["A_act"]={
        "prior":{"min":0.5,"max":1.5},
        "ref":{"dist":"norm","loc":1.0,"scale":0.01},
        "proposal":0.003,
    }
    p["P_act"]={
        "prior":{"min":0.9,"max":1.1},
        "ref":{"dist":"norm","loc":1.0,"scale":0.01},
        "proposal":0.01,
    }

def configure_planck(info,cfg):
    from camspec_npipe_lite.camspec_npipe_lite import planck_Camspec_NPIPE_lite
    info["likelihood"]["q016_camspec_npipe_lite"]={
        "external":planck_Camspec_NPIPE_lite,
        "ell_cuts":{"TT":[600,2000],"TE":[600,2000],"EE":[600,2000]},
    }
    # Chain-native CamSpec-lite calibration nuisances required by the likelihood.
    p=info["params"]
    p["A_planck"]={"prior":{"dist":"norm","loc":1.0,"scale":0.0025},"ref":1.0,"proposal":0.0005}
    p["calTE"]={"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":1.0,"proposal":0.002}
    p["calEE"]={"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":1.0,"proposal":0.002}


def _set_ref(params,name,value):
    spec=params.get(name)
    if not isinstance(spec,dict) or "prior" not in spec:
        return
    prior=spec.get("prior")
    x=float(value)
    if isinstance(prior,dict) and "min" in prior and "max" in prior:
        lo=float(prior["min"]); hi=float(prior["max"])
        eps=max((hi-lo)*1e-8,1e-12)
        x=min(max(x,lo+eps),hi-eps)
    proposal=spec.get("proposal",max(abs(x)*0.01,1e-6))
    spec["ref"]={"dist":"norm","loc":x,"scale":float(proposal)}

def apply_multistart_reference(info,branch,restart,cfg):
    params=info.setdefault("params",{})
    bases={
      "planck":{"H0":68.4,"omega_b":0.02245,"omega_cdm":0.124,"tau_reio":0.051,
                "n_s":0.982,"logA":3.06,"fEDE":0.035,"log10z_c":3.85,"thetai_scf":3.01},
      "spt":{"H0":67.96,"omega_b":0.02245,"omega_cdm":0.123,"tau_reio":0.051,
             "n_s":0.975,"logA":3.05,"fEDE":0.030,"log10z_c":3.55,"thetai_scf":2.80},
      "act":{"H0":70.85,"omega_b":0.02274,"omega_cdm":0.127,"tau_reio":0.058,
             "n_s":0.990,"logA":3.10,"fEDE":0.090,"log10z_c":3.56,"thetai_scf":2.65},
    }
    variants=[
      {},
      {"H0":+1.0,"fEDE":+0.030,"log10z_c":+0.10,"thetai_scf":-0.20,
       "omega_cdm":+0.002,"n_s":+0.004},
      {"H0":-1.0,"fEDE":-0.020,"log10z_c":-0.10,"thetai_scf":+0.20,
       "omega_cdm":-0.002,"n_s":-0.004},
      {"H0":+0.50,"fEDE":+0.060,"log10z_c":+0.22,"thetai_scf":-0.40,
       "omega_b":+0.00010,"omega_cdm":+0.003,"n_s":+0.006},
    ]
    base=dict(bases[branch]); tweak=variants[int(restart)%len(variants)]
    for k,dv in tweak.items():
        base[k]=float(base.get(k,0.0))+float(dv)
    for k,v in base.items():
        _set_ref(params,k,v)
    return {"restart_index":int(restart),"reference_family":cfg["execution"]["restart_families"][int(restart)%4],
            "reference_values":{k:float(v) for k,v in base.items() if k in params}}

def run(args):
    cfg=load_cfg(args.config)
    if args.branch not in ("planck","spt","act"): raise RuntimeError("BRANCH_GATE=FAIL")
    if args.mode not in cfg["execution"]["modes"]: raise RuntimeError("MODE_GATE=FAIL")
    start=time.monotonic()
    out=Path(args.output)
    status={"q":CURRENT_Q,"run_id":RUN_ID,"result_id":RESULT_ID,"branch":args.branch,
            "mode":args.mode,"restart":args.restart,"status":"STARTED",
            "exact_q011_vector_used_as_profile_endpoint":False,
            "cross_chain_chi2_sum_performed":False,
            "absolute_cross_chain_chi2_comparison_performed":False}
    write_json(out,status)
    info=base_info(cfg,args.branch,args.mode,args.restart,out.with_suffix(""))
    if args.branch=="spt": configure_spt(info,cfg)
    elif args.branch=="act": configure_act(info,cfg)
    else: configure_planck(info,cfg)
    restart_reference=apply_multistart_reference(info,args.branch,args.restart,cfg)
    # Build once before minimisation: imports, data, covariance and theory must all initialise.
    from cobaya.model import get_model
    model=get_model(info)
    if not model.prior.reference_is_pointlike:
        raise RuntimeError("REFERENCE_GATE=FAIL reference is not pointlike")
    ref=model.prior.reference()
    lp=model.logposterior(ref)
    if not math.isfinite(float(lp.logpost)): raise RuntimeError("FINITE_REFERENCE_GATE=FAIL")
    # Actual minimisation.
    from cobaya.run import run as cobaya_run
    updated,sampler=cobaya_run(info)
    products=sampler.products()
    minimum=products.get("minimum")
    if minimum is None: raise RuntimeError("MINIMUM_GATE=FAIL")
    # Cobaya collection row -> JSON-safe mapping
    try: row=minimum.data.iloc[0].to_dict()
    except Exception:
        try: row=dict(minimum)
        except Exception as exc: raise RuntimeError("MINIMUM_SERIALIZATION_GATE=FAIL "+repr(exc))
    chi=float(row.get("chi2",float("nan")))
    if not math.isfinite(chi): raise RuntimeError("FINITE_RESULT_GATE=FAIL")
    status.update({"status":"COMPLETE","chi2":chi,"minimum":row,
                   "elapsed_seconds":time.monotonic()-start,
                   "model_backend_commit":cfg["model"]["backend_commit"],
                   "target_h0":cfg["model"]["target_h0"] if args.mode=="fixed_h0_71p5" else None,
                   "ell_range":[cfg["surface"]["primary"]["ell_min"],cfg["surface"]["primary"]["ell_max"]],
                   "observables":cfg["surface"]["primary"]["observables"],
                   "tau_prior":cfg["surface"]["tau"],
                   "restart_reference":restart_reference,
                   "runtime_provenance_file":f"q016_v3_source_runtime/setup_{args.branch}.json"})
    write_json(out,status)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default=str(ROOT/"q016_matched_cmb_surface_v3_config.yml"))
    ap.add_argument("--branch",required=True,choices=["planck","spt","act"])
    ap.add_argument("--mode",required=True,choices=["reference_free_h0","fixed_h0_71p5"])
    ap.add_argument("--restart",required=True,type=int)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    try: run(args)
    except Exception as exc:
        write_json(args.output,{"q":CURRENT_Q,"run_id":RUN_ID,"result_id":RESULT_ID,
            "branch":args.branch,"mode":args.mode,"restart":args.restart,
            "status":"TECHNICAL_FAILURE","failure_class":"ENVIRONMENT_OR_LIKELIHOOD_OR_NUMERICAL",
            "error":repr(exc),"scientific_model_failure":False,
            "exact_q011_vector_used_as_profile_endpoint":False,
            "cross_chain_chi2_sum_performed":False})
        raise
if __name__=="__main__": main()
