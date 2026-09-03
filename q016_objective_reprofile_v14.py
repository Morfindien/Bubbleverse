#!/usr/bin/env python3
"""Bubbleverse Q016 V14 exact-objective fixed/free reprofile.

V14 changes only the computational objective implementation and continuation logic.
The scientific surface remains the Q016 matched n=3 EDE TT/TE/EE ell=600..2000
surface. Gaussian auxiliary/calibration constraints are represented as
normalization-free likelihood-shape terms and Cobaya minimize uses ignore_prior=True,
so the optimizer objective, candidate-selection objective, multistart objective and
reported fixed-minus-free objective are literally the same scalar.
"""
from __future__ import annotations
import argparse, json, math, os, time, hashlib
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT=Path(__file__).resolve().parent
Q="Q016"
RUN="Q016-MATCHED-CMB-SURFACE-V14"
RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-014"
BASIS="SCALAR_PRIMARY_CMB_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_SHAPE_LIKELIHOODS"

PRIMARY_LIKE={
    "planck":"q016_camspec_npipe_lite",
    "spt":"q016_spt_d1_lite",
    "act":"q016_act_dr6_cmbonly",
}
SHAPE_NAMES={
    "planck":["q016_shape_tau_reio","q016_shape_A_planck","q016_shape_calTE","q016_shape_calEE"],
    "spt":["q016_shape_tau_reio","q016_shape_Tcal"],
    "act":["q016_shape_tau_reio"],
}
ALLOWED_NONFLAT_PARAM_PRIORS={
    "planck":{"A_planck","calTE","calEE"},
    "spt":set(),
    "act":set(),
}
JITTER={
    "omega_b":4.0e-5,"omega_cdm":6.0e-4,"tau_reio":0.003,"n_s":0.0015,
    "logA":0.004,"fEDE":0.004,"log10z_c":0.020,"thetai_scf":0.030,"H0":0.20,
    "A_planck":0.0008,"calEE":0.002,"calTE":0.002,
    "Tcal":0.0010,"Ecal":0.0020,"A_act":0.0020,"P_act":0.0010,
}

def load_cfg(path):
    c=yaml.safe_load(Path(path).read_text())
    if c["project"]["q"]!=Q: raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"]!=RUN or c["project"]["result_id"]!=RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    if c["execution"]["objective"]["basis"]!=BASIS:
        raise RuntimeError("OBJECTIVE_IDENTITY_GATE=FAIL")
    return c

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n")
    os.replace(t,p)

def finite(x):
    try:return math.isfinite(float(x))
    except Exception:return False

def gaussian_shape_logp(x,mu,sigma):
    z=(float(x)-float(mu))/float(sigma)
    return -0.5*z*z

def make_shape_like(param,mu,sigma):
    def shape(**kwargs):
        return gaussian_shape_logp(kwargs[param],mu,sigma)
    shape.__name__=f"q016_shape_{param}"
    return {"external":shape,"input_params":[param]}

def base_info(cfg,branch,mode,restart,output_prefix):
    # Reuse the frozen Q005/Q014 parameterization and bounds only.
    import q014_external_viability_v5 as q14
    q14cfg=yaml.safe_load((ROOT/"q014_external_viability_v14_config.yml").read_text())
    template="spt_d1_only" if branch=="spt" else "planck_npipe_k039_approx"
    info,_=q14.build_info(template,"reference_free_h0","external",restart,
                          q14cfg,{},output_prefix,
                          max_evals=int(cfg["execution"]["optimizer"]["max_evals"]))
    info["likelihood"]={}
    info["prior"]={}
    foreign={"A_planck","calTE","calEE","amp_143","amp_217","amp_143x217",
             "n_143","n_217","n_143x217","Tcal","Ecal","A_act","P_act"}
    params=info.setdefault("params",{})
    for k in list(params):
        if k in foreign: params.pop(k,None)
    if mode=="fixed_h0_71p5":
        params["H0"]=float(cfg["model"]["target_h0"])
    m=info.setdefault("sampler",{}).setdefault("minimize",{})
    m["ignore_prior"]=True
    m["best_of"]=int(cfg["execution"]["optimizer"]["best_of"])
    m["max_evals"]=int(cfg["execution"]["optimizer"]["max_evals"])
    m.setdefault("override_bobyqa",{})["rhoend"]=float(cfg["execution"]["optimizer"]["rhoend"])
    return info

def configure_planck(info,cfg):
    from camspec_npipe_lite.camspec_npipe_lite import planck_Camspec_NPIPE_lite
    info["likelihood"][PRIMARY_LIKE["planck"]]={
        "external":planck_Camspec_NPIPE_lite,
        "ell_cuts":{"TT":[600,2000],"TE":[600,2000],"EE":[600,2000]},
    }
    p=info["params"]
    # Retain exact scientific priors; ignore_prior=True removes their normalized
    # density from the optimizer objective. Their variable Gaussian shapes are
    # reintroduced below as normalization-free likelihood terms.
    p["A_planck"]={"prior":{"dist":"norm","loc":1.0,"scale":0.0025},"ref":1.0,"proposal":0.0005}
    p["calTE"]={"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":1.0,"proposal":0.002}
    p["calEE"]={"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":1.0,"proposal":0.002}

def configure_spt(info,cfg):
    from candl.interface import CandlCobayaLikelihood
    import spt_candl_data
    info["likelihood"][PRIMARY_LIKE["spt"]]={
        "external":CandlCobayaLikelihood,
        "data_set_file":spt_candl_data.SPT3G_D1_TnE_lite,
        "data_selection":["ell<600 remove","ell>2000 remove"],
        "clear_internal_priors":True,
        "feedback":True,
        "additional_args":{},
        "wrapper":None,
    }
    p=info["params"]
    p["Tcal"]={"prior":{"min":0.8,"max":1.2},"ref":1.0,"proposal":0.0036}
    p["Ecal"]={"prior":{"min":0.8,"max":1.2},"ref":1.0,"proposal":0.01}

def configure_act(info,cfg):
    try:
        from act_dr6_cmbonly import ACTDR6CMBonly
    except Exception as exc:
        raise RuntimeError("ACT_LIKELIHOOD_IMPORT_GATE=FAIL "+repr(exc))
    info["likelihood"][PRIMARY_LIKE["act"]]={
        "external":ACTDR6CMBonly,
        "ell_cuts":{"TT":[600,2000],"TE":[600,2000],"EE":[600,2000]},
        "stop_at_error":True,
    }
    p=info["params"]
    p["A_act"]={"prior":{"min":0.5,"max":1.5},"ref":1.0,"proposal":0.003}
    p["P_act"]={"prior":{"min":0.9,"max":1.1},"ref":1.0,"proposal":0.01}

def configure_exact_objective(info,branch,cfg):
    # Every Gaussian shape is a likelihood component WITHOUT log-normalization.
    tc=cfg["objective_constraints"]["tau_reio"]
    info["likelihood"]["q016_shape_tau_reio"]=make_shape_like("tau_reio",tc["mean"],tc["sigma"])
    if branch=="planck":
        for name in ("A_planck","calTE","calEE"):
            s=cfg["objective_constraints"]["planck"][name]
            info["likelihood"][f"q016_shape_{name}"]=make_shape_like(name,s["mean"],s["sigma"])
    elif branch=="spt":
        s=cfg["objective_constraints"]["spt"]["Tcal"]
        info["likelihood"]["q016_shape_Tcal"]=make_shape_like("Tcal",s["mean"],s["sigma"])
    # ACT A_act/P_act remain uniform hard bounds only; no invented Gaussian shape.
    m=info["sampler"]["minimize"]
    if m.get("ignore_prior") is not True:
        raise RuntimeError("EXACT_OPTIMIZER_OBJECTIVE_GATE=FAIL ignore_prior")
    if int(m.get("best_of",-1))!=1:
        raise RuntimeError("EXPLICIT_RESTART_OWNERSHIP_GATE=FAIL best_of")

def scalarize_existing_ref(spec):
    if not isinstance(spec,dict) or "prior" not in spec:return
    r=spec.get("ref")
    if isinstance(r,(int,float)) and finite(r):return
    if isinstance(r,dict) and finite(r.get("loc")):
        spec["ref"]=float(r["loc"]); return
    pr=spec.get("prior")
    if isinstance(pr,dict):
        if finite(pr.get("min")) and finite(pr.get("max")):
            spec["ref"]=0.5*(float(pr["min"])+float(pr["max"])); return
        if finite(pr.get("loc")):
            spec["ref"]=float(pr["loc"]); return
    raise RuntimeError("POINT_REFERENCE_GATE=FAIL cannot scalarize ref")

def set_point_ref(params,name,value):
    spec=params.get(name)
    if not isinstance(spec,dict) or "prior" not in spec:return False
    x=float(value); pr=spec.get("prior")
    if isinstance(pr,dict) and finite(pr.get("min")) and finite(pr.get("max")):
        lo=float(pr["min"]); hi=float(pr["max"]); eps=max((hi-lo)*1e-8,1e-12)
        x=min(max(x,lo+eps),hi-eps)
    spec["ref"]=x
    return True

def bounded_jitter(base,info,sign):
    out=dict(base); params=info.get("params",{})
    for name,dv in JITTER.items():
        if name not in out or name not in params:continue
        x=float(out[name])+float(sign)*float(dv)
        spec=params.get(name)
        if isinstance(spec,dict):
            pr=spec.get("prior")
            if isinstance(pr,dict) and finite(pr.get("min")) and finite(pr.get("max")):
                lo=float(pr["min"]); hi=float(pr["max"]); eps=max((hi-lo)*1e-6,1e-10)
                if x<=lo+eps or x>=hi-eps:
                    x=float(out[name])-float(sign)*float(dv)
                x=min(max(x,lo+eps),hi-eps)
        out[name]=x
    return out

def load_seed_lock(cfg):
    d=json.loads((ROOT/cfg["execution"]["continuation"]["seed_lock_file"]).read_text())
    if d.get("q")!=Q or d.get("run_id")!=RUN or d.get("result_id")!=RESULT:
        raise RuntimeError("V6_SEED_LOCK_GATE=FAIL identity")
    p=d.get("parent",{})
    if int(p.get("github_run_id",-1))!=33732688762 or p.get("head_sha")!="d14880138ebb537173e49417b537a68454d53602":
        raise RuntimeError("V6_SEED_LOCK_GATE=FAIL parent")
    return d

def load_phase1(path):
    d=json.loads(Path(path).read_text())
    if d.get("q")!=Q or d.get("run_id")!="Q016-MATCHED-CMB-SURFACE-V10" or d.get("result_id")!="R-Q016-EDE-MATCHED-CMB-SURFACE-010" or d.get("stage")!="PHASE1_FIXED_SUMMARY":
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL identity")
    if d.get("status")!="PASS":
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL status")
    return d

def load_v10_primary_parent(path):
    d=json.loads(Path(path).read_text())
    if d.get("q")!="Q016" or d.get("run_id")!="Q016-MATCHED-CMB-SURFACE-V10" or d.get("result_id")!="R-Q016-EDE-MATCHED-CMB-SURFACE-010":
        raise RuntimeError("V10_PRIMARY_PARENT_GATE=FAIL identity")
    g=d.get("gates",{})
    expected_false={"planck_free_multistart","ENDPOINT_REPROFILE_GATE","MULTISTART_STABILITY_GATE"}
    if d.get("primary_endpoint_gate")!="FAIL" or d.get("validation_status")!="NUMERICALLY_UNRESOLVED":
        raise RuntimeError("V10_PRIMARY_PARENT_GATE=FAIL status")
    if g.get("planck_free_multistart") is not False:
        raise RuntimeError("V10_PRIMARY_PARENT_GATE=FAIL expected Planck free multistart")
    for key in ("spt_free_multistart","act_free_multistart","PROFILE_NESTING_GATE","SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE"):
        if g.get(key) is not True:
            raise RuntimeError("V10_PRIMARY_PARENT_GATE=FAIL "+key)
    return d

CROSS_A_SIGNS={
    "omega_b":1,"omega_cdm":-1,"tau_reio":1,"n_s":-1,"logA":1,"fEDE":-1,
    "log10z_c":1,"thetai_scf":-1,"H0":1,"A_planck":-1,"calEE":1,"calTE":-1,
}
CROSS_B_SIGNS={k:-v for k,v in CROSS_A_SIGNS.items()}

def patterned_jitter(base,info,pattern):
    out=dict(base); params=info.get("params",{})
    if pattern=="plus": signs={k:1 for k in JITTER}
    elif pattern=="minus": signs={k:-1 for k in JITTER}
    elif pattern=="cross_a": signs=CROSS_A_SIGNS
    elif pattern=="cross_b": signs=CROSS_B_SIGNS
    else: raise RuntimeError("JITTER_PATTERN_GATE=FAIL")
    changed=0
    for name,dv in JITTER.items():
        if name not in out or name not in params: continue
        sign=float(signs.get(name,0))
        if sign==0: continue
        x=float(out[name])+sign*float(dv)
        spec=params.get(name)
        if isinstance(spec,dict):
            pr=spec.get("prior")
            if isinstance(pr,dict) and finite(pr.get("min")) and finite(pr.get("max")):
                lo=float(pr["min"]); hi=float(pr["max"]); eps=max((hi-lo)*1e-6,1e-10)
                if x<=lo+eps or x>=hi-eps:
                    x=float(out[name])-sign*float(dv)
                x=min(max(x,lo+eps),hi-eps)
        if abs(x-float(out[name]))>0:
            changed+=1
        out[name]=x
    if changed==0:
        raise RuntimeError("NONZERO_PERTURBATION_GATE=FAIL")
    return out,changed

def source_vector(info,branch,mode,family,cfg,phase1_path=None,parent_free_result=None):
    lock=load_seed_lock(cfg)
    if family.startswith("parent_fixed"):
        base=dict(lock["profiles"][branch]["fixed_h0_71p5"]["minimum"])
        source={"kind":"V6_HISTORY_FIXED_OBJECTIVE_BEST",
                "objective":lock["profiles"][branch]["fixed_h0_71p5"]["objective_best_from_v6_history"]}
        sign=+1 if family.endswith("_plus") else (-1 if family.endswith("_minus") else 0)
    elif family=="parent_free_projected" or family=="parent_free_best":
        base=dict(lock["profiles"][branch]["reference_free_h0"]["minimum"])
        source={"kind":"V6_HISTORY_FREE_OBJECTIVE_BEST",
                "objective":lock["profiles"][branch]["reference_free_h0"]["objective_best_from_v6_history"]}
        sign=0
    elif family.startswith("phase1_fixed_embed"):
        if phase1_path is None: raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL missing")
        p1=load_phase1(phase1_path)
        best=p1["branches"][branch]["best_record"]
        base=dict(best["minimum"])
        source={"kind":"CONTINUATION_PHASE1_FIXED_BEST",
                "objective":float(best["objective_chi2"]),
                "source_family":best["start_family"],
                "source_restart":best["restart"],
                "source_run_id":best.get("run_id"),
                "source_result_id":best.get("result_id")}
        base["H0"]=float(cfg["model"]["target_h0"])
        sign=+1 if family.endswith("_plus") else (-1 if family.endswith("_minus") else 0)
    elif family.startswith("v10_planck_free_best_"):
        if branch!="planck" or mode!="reference_free_h0":
            raise RuntimeError("PLANCK_EXTENSION_SCOPE_GATE=FAIL")
        if parent_free_result is None:
            raise RuntimeError("V10_PRIMARY_PARENT_GATE=FAIL missing")
        parent=load_v10_primary_parent(parent_free_result)
        best=parent["branches"]["planck"]["reference_free_h0"]["best_record"]
        if int(best.get("restart",-1))!=13 or abs(float(best.get("objective_chi2",999))-4198.257976875995)>1e-9:
            raise RuntimeError("V10_PLANCK_BEST_LOCK_GATE=FAIL")
        base=dict(best["minimum"])
        pattern=family.removeprefix("v10_planck_free_best_jitter_") if "jitter_" in family else family.removeprefix("v10_planck_free_best_")
        if pattern not in ("plus","minus","cross_a","cross_b"):
            raise RuntimeError("START_FAMILY_GATE=FAIL "+family)
        base,changed=patterned_jitter(base,info,pattern)
        source={"kind":"V10_PLANCK_FREE_BEST_NONZERO_PERTURBATION",
                "objective":float(best["objective_chi2"]),
                "H0":float(best["minimum"]["H0"]),
                "source_family":best["start_family"],
                "source_restart":best["restart"],
                "source_run_id":best.get("run_id"),
                "source_result_id":best.get("result_id"),
                "jitter_pattern":pattern,
                "nonzero_perturbation":True,
                "changed_parameter_count":changed}
        sign=0
    else:
        raise RuntimeError("START_FAMILY_GATE=FAIL "+family)

    # Stored fixed minima intentionally omit H0. Any fixed->free embedding MUST
    # restore the exact fixed target before optional jitter.
    if family.startswith("parent_fixed") and mode=="reference_free_h0":
        base["H0"]=float(cfg["model"]["target_h0"])
    if mode=="fixed_h0_71p5":
        base["H0"]=float(cfg["model"]["target_h0"])
    if sign:
        base=bounded_jitter(base,info,sign)

    params=info["params"]; applied={}
    for name,value in base.items():
        if name=="H0" and mode=="fixed_h0_71p5": continue
        if finite(value) and set_point_ref(params,name,value):
            applied[name]=float(value)
    for name,spec in params.items():
        if isinstance(spec,dict) and "prior" in spec:
            scalarize_existing_ref(spec)
    return base,source,applied

def prior_gate(model,branch):
    resolved=model.info()
    sampled=set(model.parameterization.sampled_params())
    nonflat={}
    for name in sampled:
        spec=resolved.get("params",{}).get(name,{})
        if not isinstance(spec,Mapping):continue
        pr=spec.get("prior")
        if not isinstance(pr,Mapping):continue
        dist=str(pr.get("dist","uniform")).lower()
        if dist!="uniform":nonflat[name]=dict(pr)
    ext=set((resolved.get("prior") or {}).keys()) if isinstance(resolved.get("prior"),Mapping) else set()
    expected=ALLOWED_NONFLAT_PARAM_PRIORS[branch]
    return {
        "pass":set(nonflat)==expected and not ext,
        "nonflat_parameter_priors":nonflat,
        "expected_nonflat_parameter_priors":sorted(expected),
        "external_prior_names":sorted(ext),
        "expected_external_prior_names":[],
    }

def objective_from_row(row,branch):
    expected=[PRIMARY_LIKE[branch],*SHAPE_NAMES[branch]]
    comps={}
    for name in expected:
        key=f"chi2__{name}"
        if key not in row or not finite(row[key]):
            raise RuntimeError("OBJECTIVE_COMPONENT_GATE=FAIL missing="+key)
        comps[name]=float(row[key])
    extras={}
    for k,v in row.items():
        if str(k).startswith("chi2__") and str(k)[6:] not in expected and finite(v):
            extras[str(k)[6:]]=float(v)
    if extras:
        raise RuntimeError("OBJECTIVE_COMPONENT_GATE=FAIL unexpected="+json.dumps(extras,sort_keys=True))
    objective=sum(comps.values())
    scalar=float(row.get("chi2",float("nan")))
    if not finite(scalar) or abs(scalar-objective)>1e-5:
        raise RuntimeError(f"OBJECTIVE_SELF_CONSISTENCY_GATE=FAIL scalar={scalar} components={objective}")
    return objective,comps

def row_from_model_point(model,ref):
    lp=model.logposterior(ref)
    if not finite(getattr(lp,"logpost",float("nan"))):
        raise RuntimeError("FINITE_REFERENCE_GATE=FAIL")
    sampled=list(model.parameterization.sampled_params())
    row={name:float(v) for name,v in zip(sampled,ref)}
    try:
        row.update({str(k):float(v) for k,v in model.parameterization.constant_params().items()
                    if isinstance(v,(int,float))})
    except Exception:
        pass
    loglikes=list(getattr(lp,"loglikes",[]))
    if len(loglikes)!=len(model.likelihood):
        raise RuntimeError("SEED_EVALUATION_GATE=FAIL likelihood count")
    total=0.0
    for name,val in zip(model.likelihood.keys(),loglikes):
        x=-2.0*float(val); row[f"chi2__{name}"]=x; total+=x
    row["chi2"]=total
    row["minuslogpost"]=-float(lp.logpost)
    return row

def minimum_to_row(minimum):
    try:return minimum.data.iloc[0].to_dict()
    except Exception:
        try:return dict(minimum)
        except Exception as exc:
            raise RuntimeError("MINIMUM_SERIALIZATION_GATE=FAIL "+repr(exc))

def run_task(args):
    cfg=load_cfg(args.config)
    branch=args.branch; mode=args.mode; family=args.start_family
    phase="phase1_fixed" if mode=="fixed_h0_71p5" else "phase2_free"
    allowed=(cfg["execution"]["continuation"]["phase1_families"] if phase=="phase1_fixed"
             else cfg["execution"]["continuation"]["phase2_families"])
    if family not in allowed:raise RuntimeError("START_FAMILY_GATE=FAIL")
    if phase=="phase2_free" and not args.phase1_summary:
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL missing")
    start=time.monotonic(); out=Path(args.output)
    status={
        "case_id":cfg["project"]["case_id"],"q":Q,"original_case_question":cfg["scientific_question"],
        "run_id":RUN,"result_id":RESULT,"branch":branch,"mode":mode,"phase":phase,
        "start_family":family,"restart":args.restart,"status":"STARTED",
        "objective_basis":BASIS,"exact_optimizer_objective":True,"ignore_prior":True,
        "exact_q011_vector_used_as_profile_endpoint":False,
        "cross_chain_chi2_sum_performed":False,
        "absolute_cross_chain_chi2_comparison_performed":False,
        "parent":{"github_run_id":33764943297,"head_sha":"81a90d30abf8b5e28d2db2b5f5b22f03b4f998a8",
                  "run_id":"Q016-MATCHED-CMB-SURFACE-V10","role":"TARGETED_PLANCK_FREE_MULTISTART_PARENT"}
    }
    write_json(out,status)

    info=base_info(cfg,branch,mode,args.restart,out.with_suffix(""))
    if branch=="planck":configure_planck(info,cfg)
    elif branch=="spt":configure_spt(info,cfg)
    else:configure_act(info,cfg)
    configure_exact_objective(info,branch,cfg)
    raw_source,source_meta,applied=source_vector(
        info,branch,mode,family,cfg,args.phase1_summary,args.parent_free_result)

    from cobaya.model import get_model
    model=get_model(info)
    pg=prior_gate(model,branch)
    if not pg["pass"]:
        raise RuntimeError("PRIOR_STRUCTURE_GATE=FAIL "+json.dumps(pg,sort_keys=True))
    if not bool(model.prior.reference_is_pointlike):
        raise RuntimeError("POINT_REFERENCE_GATE=FAIL reference not pointlike")
    ref=model.prior.reference(max_tries=10000,warn_if_no_ref=True)
    seed_row=row_from_model_point(model,ref)
    seed_obj,seed_comps=objective_from_row(seed_row,branch)
    seed={
        "minimum":seed_row,"objective_chi2":seed_obj,"objective_components":seed_comps,
        "source":source_meta,"applied_reference_values":applied,
        "reference_is_pointlike":True,"prior_structure_gate":pg,
    }
    if family=="phase1_fixed_embed":
        src=float(source_meta["objective"])
        tol=float(cfg["execution"]["continuation"]["embedding_equivalence_tolerance"])
        delta=seed_obj-src
        seed["same_run_embedding"]={
            "source_fixed_objective":src,"free_space_seed_objective":seed_obj,
            "delta":delta,"tolerance":tol,"pass":abs(delta)<=tol,
            "H0":float(seed_row["H0"]),
        }
        if not seed["same_run_embedding"]["pass"]:
            raise RuntimeError("SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE=FAIL "+json.dumps(seed["same_run_embedding"],sort_keys=True))

    status.update({"status":"RUNNING","seed_candidate":seed,"source_vector_meta":source_meta,
                   "runtime_provenance_file":f"q016_v14_source_runtime/setup_{branch}.json"})
    write_json(out,status)

    from cobaya.run import run as cobaya_run
    updated,sampler=cobaya_run(info)
    minimum=sampler.products().get("minimum")
    if minimum is None:raise RuntimeError("MINIMUM_GATE=FAIL")
    opt_row=minimum_to_row(minimum)
    opt_obj,opt_comps=objective_from_row(opt_row,branch)
    if not finite(opt_obj):raise RuntimeError("FINITE_RESULT_GATE=FAIL")
    tol=float(cfg["execution"]["continuation"]["seed_objective_tolerance"])
    if seed_obj < opt_obj-tol:
        selected_row=seed_row; selected_obj=seed_obj; selected_comps=seed_comps
        selected="EXACT_DETERMINISTIC_SEED"
    else:
        selected_row=opt_row; selected_obj=opt_obj; selected_comps=opt_comps
        selected="OPTIMIZER_MINIMUM"
    preservation=selected_obj<=seed_obj+tol

    status.update({
        "status":"COMPLETE","selected_candidate":selected,
        "minimum":selected_row,"objective_chi2":selected_obj,
        "objective_components":selected_comps,
        "raw_optimizer_candidate":{"minimum":opt_row,"objective_chi2":opt_obj,"objective_components":opt_comps},
        "seed_candidate_preservation_pass":preservation,
        "seed_objective_tolerance":tol,
        "elapsed_seconds":time.monotonic()-start,
        "model_backend_commit":cfg["model"]["backend_commit"],
        "target_h0":cfg["model"]["target_h0"] if mode=="fixed_h0_71p5" else None,
        "ell_range":[cfg["surface"]["primary"]["ell_min"],cfg["surface"]["primary"]["ell_max"]],
        "observables":cfg["surface"]["primary"]["observables"],
        "objective_component_gate":True,
        "objective_self_consistency_gate":True,
        "exact_optimizer_objective_gate":True,
    })
    if not preservation:
        raise RuntimeError("SEED_CANDIDATE_PRESERVATION_GATE=FAIL")
    write_json(out,status)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default=str(ROOT/"q016_matched_cmb_surface_v14_config.yml"))
    ap.add_argument("--branch",required=True,choices=["planck","spt","act"])
    ap.add_argument("--mode",required=True,choices=["reference_free_h0","fixed_h0_71p5"])
    ap.add_argument("--start-family",required=True)
    ap.add_argument("--restart",required=True,type=int)
    ap.add_argument("--phase1-summary")
    ap.add_argument("--parent-free-result")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    try:run_task(a)
    except Exception as exc:
        p=Path(a.output)
        old={}
        try:old=json.loads(p.read_text())
        except Exception:pass
        old.update({
            "q":Q,"run_id":RUN,"result_id":RESULT,"branch":a.branch,"mode":a.mode,
            "start_family":a.start_family,"restart":a.restart,
            "status":"TECHNICAL_FAILURE","failure_class":"ENVIRONMENT_LIKELIHOOD_OR_NUMERICAL",
            "error":repr(exc),"scientific_model_failure":False,
            "objective_basis":BASIS,"exact_optimizer_objective":True,
            "cross_chain_chi2_sum_performed":False
        })
        write_json(p,old)
        raise

if __name__=="__main__":main()
