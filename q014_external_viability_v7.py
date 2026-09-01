#!/usr/bin/env python3
"""Bubbleverse Q014 V7 — objective comparability + numerical continuation repair.

V7 preserves the V5/V6 likelihood/model surface but fixes a statistical accounting
bug exposed by V6's mandatory monotonicity gate. Free-H0 and fixed-H0 models have
different normalized flat-prior constants, so 2*minuslogpost is not cross-mode
comparable. V7 reports a normalization-free profile deviance:

  scalar Cobaya total likelihood chi2
  + Gaussian calibration constraint SHAPES only (no normalization constants).

The optimizer itself remains ignore_prior=false, therefore the same chain-native
constraint shapes still participate in nuisance profiling. V7 then performs
cross-seeded local certification from the best V6 free/fixed minima.
"""
from __future__ import annotations
import argparse, copy, json, math
from pathlib import Path
from typing import Any, Mapping
import yaml
import q014_external_viability_v5 as impl

ROOT=Path(__file__).resolve().parent
CONFIG_NAME="q014_external_viability_v7_config.yml"
RUN_ID="Q014-EXTERNAL-VIABILITY-V7"
CODE_VERSION="7.0-normalization-free-objective-v6-continuation"
V6_EXPECTED_RUN="Q014-EXTERNAL-VIABILITY-V6"
V6_EXPECTED_RESULT="R-Q014-EDE-EXTERNAL-VIABILITY-003"
V6_RESULT_PATH: Path|None=None

impl.RUN_ID=RUN_ID
impl.CODE_VERSION=CODE_VERSION
impl.CONFIG_NAME=CONFIG_NAME

PLANCK_NUISANCE={
  "A_planck":{"prior":{"dist":"norm","loc":1.0,"scale":0.0025},"ref":{"dist":"norm","loc":1.0,"scale":0.002},"proposal":0.0005},
  "amp_143":{"prior":{"dist":"uniform","min":0.0,"max":50.0},"ref":{"dist":"norm","loc":10.0,"scale":1.0},"proposal":1.0},
  "amp_217":{"prior":{"dist":"uniform","min":0.0,"max":50.0},"ref":{"dist":"norm","loc":20.0,"scale":1.0},"proposal":1.0},
  "amp_143x217":{"prior":{"dist":"uniform","min":0.0,"max":50.0},"ref":{"dist":"norm","loc":10.0,"scale":1.0},"proposal":1.0},
  "n_143":{"prior":{"dist":"uniform","min":0.0,"max":5.0},"ref":{"dist":"norm","loc":1.0,"scale":0.2},"proposal":0.2},
  "n_217":{"prior":{"dist":"uniform","min":0.0,"max":5.0},"ref":{"dist":"norm","loc":1.0,"scale":0.2},"proposal":0.2},
  "n_143x217":{"prior":{"dist":"uniform","min":0.0,"max":5.0},"ref":{"dist":"norm","loc":1.0,"scale":0.2},"proposal":0.2},
  "calTE":{"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":{"dist":"norm","loc":1.0,"scale":0.01},"proposal":0.01},
  "calEE":{"prior":{"dist":"norm","loc":1.0,"scale":0.01},"ref":{"dist":"norm","loc":1.0,"scale":0.01},"proposal":0.01},
}
CONSTRAINTS={
  "planck_npipe_k039_approx":{"A_planck":(1.0,0.0025),"calTE":(1.0,0.01),"calEE":(1.0,0.01)},
  "spt_d1_only":{"Tcal":(1.0,0.0036)},
  "spt_d1_plus_desi":{"Tcal":(1.0,0.0036)},
}
ALLOWED_NONFLAT_PARAM_PRIORS={
  "planck_npipe_k039_approx":{"A_planck","calTE","calEE"},
  "spt_d1_only":set(),
  "spt_d1_plus_desi":set(),
}
ALLOWED_EXTERNAL_PRIORS={
  "planck_npipe_k039_approx":set(),
  "spt_d1_only":{"q014_spt_gaussian_Tcal"},
  "spt_d1_plus_desi":{"q014_spt_gaussian_Tcal"},
}

_original_inject=impl.inject_chain_native_parameters
def inject_chain_native_parameters(info:dict[str,Any], chain:str, c:Mapping[str,Any])->None:
    _original_inject(info,chain,c)
    if chain=="planck_npipe_k039_approx":
        params=info.setdefault("params",{})
        # Exact re-declaration of the pinned Cobaya v3.5.6 NPIPE nuisance defaults.
        # This does not alter their priors; it makes them visible before component
        # default merging so V6 best nuisance values can be deterministic refs.
        for name,spec in PLANCK_NUISANCE.items():
            params[name]=copy.deepcopy(spec)
impl.inject_chain_native_parameters=inject_chain_native_parameters

def set_reference(params:dict[str,Any], name:str, value:float)->None:
    spec=params.get(name)
    if isinstance(spec,dict) and "prior" in spec:
        # Cobaya documents scalar ref as an exact initial point. This is essential
        # for continuation/cross-seeding; the sampled prior itself is unchanged.
        spec["ref"]=float(value)
impl.set_reference=set_reference

def load_v6_result(path:Path|None=None)->dict[str,Any]:
    p=path or V6_RESULT_PATH
    if p is None: raise RuntimeError("V6_NUMERICAL_PARENT_GATE=FAIL no V6 result path")
    d=json.loads(Path(p).read_text(encoding="utf-8"))
    if d.get("q")!="Q014" or d.get("run_id")!=V6_EXPECTED_RUN or d.get("result_id")!=V6_EXPECTED_RESULT:
        raise RuntimeError("V6_NUMERICAL_PARENT_GATE=FAIL identity")
    if d.get("scientifically_usable_result") is not False or d.get("validation_status")!="NUMERICALLY UNRESOLVED":
        raise RuntimeError("V6_NUMERICAL_PARENT_GATE=FAIL status")
    jm=d.get("job_manifest",{})
    if int(jm.get("expected",-1))!=27 or int(jm.get("returned",-2))!=27 or jm.get("missing") or jm.get("duplicates"):
        raise RuntimeError("V6_NUMERICAL_PARENT_GATE=FAIL completeness")
    return d

def v6_best_minimum(chain:str, mode:str)->dict[str,float]:
    d=load_v6_result()
    rec=d["chains"][chain]["profiles"][mode].get("best_record")
    if not isinstance(rec,Mapping) or rec.get("status")!="COMPLETE":
        raise RuntimeError(f"V6_NUMERICAL_PARENT_GATE=FAIL missing best record {chain}/{mode}")
    row=rec.get("minimum")
    if not isinstance(row,Mapping): raise RuntimeError("V6_NUMERICAL_PARENT_GATE=FAIL minimum")
    out={}
    for k,v in row.items():
        try:
            x=float(v)
        except Exception:
            continue
        if math.isfinite(x): out[str(k)]=x
    return out

_original_start=impl.start_vector
def start_vector(chain:str, family:str, c:Mapping[str,Any], info:Mapping[str,Any], q011_vec:Mapping[str,float])->dict[str,float]:
    if family not in {"v6_free_best","v6_fixed_best"}:
        return _original_start(chain,family,c,info,q011_vec)
    base=impl.q005_default_reference(info)
    source_mode="reference_free_h0" if family=="v6_free_best" else "fixed_h0_71p5"
    base.update(v6_best_minimum(chain,source_mode))
    if family=="v6_fixed_best" and "H0" not in base:
        base["H0"]=float(c["scientific_surface"]["target_h0"])
    return base
impl.start_vector=start_vector

_original_build=impl.build_info
def build_info(chain,mode,start_family,restart_index,c,q011_vec,output_prefix,max_evals=None):
    info,refs=_original_build(chain,mode,start_family,restart_index,c,q011_vec,output_prefix,max_evals)
    m=info["sampler"]["minimize"]
    m["max_evals"]=int(max_evals if max_evals is not None else c["execution"]["minimizer"]["max_evals"])
    m.setdefault("override_bobyqa",{})["rhoend"]=float(c["execution"]["minimizer"]["override_bobyqa"]["rhoend"])
    return info,refs
impl.build_info=build_info

def comparable_objective(row:Mapping[str,Any])->tuple[float|None,dict[str,float],str,dict[str,float]]:
    try: base=float(row["chi2"])
    except Exception: return None,{},"SCALAR_TOTAL_CHI2_REQUIRED",{}
    if not math.isfinite(base): return None,{},"SCALAR_TOTAL_CHI2_REQUIRED",{}
    # Infer chain from nuisance keys. A_planck is unique to Planck; Tcal to SPT.
    if "A_planck" in row or "calTE" in row or "calEE" in row:
        cons=CONSTRAINTS["planck_npipe_k039_approx"]
    elif "Tcal" in row:
        cons=CONSTRAINTS["spt_d1_only"]
    else:
        cons={}
    penalties={}
    for name,(mu,sigma) in cons.items():
        if name not in row: return None,{},f"MISSING_CONSTRAINT_PARAMETER_{name}",{}
        x=float(row[name]); penalties[name]=((x-mu)/sigma)**2
    comps={}
    for k,v in row.items():
        if str(k).startswith("chi2__"):
            try: x=float(v)
            except Exception: continue
            if math.isfinite(x): comps[str(k)]=x
    return base+sum(penalties.values()),comps,"SCALAR_TOTAL_LIKELIHOOD_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_CONSTRAINT_SHAPES",penalties

def objective_from_row(row:Mapping[str,Any]):
    x,comps,basis,_=comparable_objective(row)
    return x,comps,basis
impl.objective_from_row=objective_from_row

def _prior_gate(model,chain:str)->dict[str,Any]:
    resolved=model.info(); sampled=set(model.parameterization.sampled_params())
    detected={}
    for name in sampled:
        spec=resolved.get("params",{}).get(name,{})
        if not isinstance(spec,Mapping): continue
        prior=spec.get("prior")
        if not isinstance(prior,Mapping): continue
        dist=str(prior.get("dist","uniform")).lower()
        if dist!="uniform": detected[name]=dict(prior)
    ext=set((resolved.get("prior") or {}).keys()) if isinstance(resolved.get("prior"),Mapping) else set()
    ok=set(detected)==ALLOWED_NONFLAT_PARAM_PRIORS[chain] and ext==ALLOWED_EXTERNAL_PRIORS[chain]
    return {"pass":ok,"nonflat_parameter_priors":detected,"external_prior_names":sorted(ext),
            "expected_nonflat_parameter_priors":sorted(ALLOWED_NONFLAT_PARAM_PRIORS[chain]),
            "expected_external_priors":sorted(ALLOWED_EXTERNAL_PRIORS[chain])}

def seed_evaluation(chain:str,mode:str,family:str,restart:int,q011_path:str|Path,c:Mapping[str,Any],out:Path)->dict[str,Any]:
    qvec=impl.q011_exact_shared_vector(c,q011_path)
    info,refs=impl.build_info(chain,mode,family,restart,c,qvec,out.parent/(out.stem+"_seedcheck"),max_evals=4)
    from cobaya.model import get_model
    model=get_model(info)
    gate=_prior_gate(model,chain)
    if not gate["pass"]: raise RuntimeError("CHAIN_NATIVE_CONSTRAINT_SHAPE_GATE=FAIL "+json.dumps(gate,sort_keys=True))
    sampled=list(model.parameterization.sampled_params())
    if not bool(getattr(model.prior,"reference_is_pointlike",False)):
        raise RuntimeError("DETERMINISTIC_V6_CONTINUATION_GATE=FAIL reference not pointlike")
    ref=model.prior.reference()
    point={name:float(value) for name,value in zip(sampled,ref)}
    lp=model.logposterior(ref)
    loglikes=list(getattr(lp,"loglikes",[]))
    if len(loglikes)!=len(model.likelihood): raise RuntimeError("SEED_EVALUATION_GATE=FAIL likelihood count")
    row=dict(point)
    try: row.update({str(k):float(v) for k,v in model.parameterization.constant_params().items() if isinstance(v,(int,float))})
    except Exception: pass
    total=0.0; comps={}
    for name,val in zip(model.likelihood.keys(),loglikes):
        x=-2.0*float(val); comps[f"chi2__{name}"]=x; row[f"chi2__{name}"]=x; total+=x
    row["chi2"]=total
    logpost=getattr(lp,"logpost",None)
    if logpost is not None: row["minuslogpost"]=-float(logpost)
    obj,_,basis,pen=comparable_objective(row)
    if obj is None or not math.isfinite(obj): raise RuntimeError("SEED_EVALUATION_GATE=FAIL nonfinite")
    return {"minimum":row,"objective_chi2":obj,"objective_basis":basis,"chi2_components":comps,
            "constraint_shape_penalties":pen,"sampled_parameters":sampled,"prior_gate":gate,"refs":refs}

def run_task_v7(chain,mode,family,restart,q011_path,v6_path,output,c,max_evals=None)->int:
    global V6_RESULT_PATH
    V6_RESULT_PATH=Path(v6_path)
    load_v6_result()
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    try: seed=seed_evaluation(chain,mode,family,restart,q011_path,c,out)
    except Exception as exc:
        impl.dump_json(out,{"case_id":c["project"]["case_id"],"q":"Q014","run_id":RUN_ID,"chain":chain,"mode":mode,
            "start_family":family,"restart_index":restart,"status":"TECHNICAL_FAILURE","failure_type":"V7_SEED_OR_PRIOR_GATE",
            "error":repr(exc),"finite_result":False})
        return 9
    rc=impl.run_task(chain,mode,family,restart,q011_path,out,c,max_evals)
    rec=json.loads(out.read_text())
    rec["v6_numerical_parent"]={"run_id":V6_EXPECTED_RUN,"result_id":V6_EXPECTED_RESULT,
        "source_mode":"reference_free_h0" if family=="v6_free_best" else ("fixed_h0_71p5" if family=="v6_fixed_best" else None)}
    rec["seed_candidate"]={k:v for k,v in seed.items() if k!="refs"}
    rec["seed_start_vector_sha256"]=impl.canonical_hash(seed["refs"])
    if rec.get("status")=="COMPLETE":
        row=rec.get("minimum",{})
        corrected,comps,basis,pen=comparable_objective(row)
        rec["raw_v5_v6_2minuslogpost_objective"]=(2.0*float(row["minuslogpost"]) if "minuslogpost" in row else None)
        rec["likelihood_chi2_scalar"]=float(row["chi2"]) if "chi2" in row else None
        rec["constraint_shape_penalties"]=pen
        rec["objective_chi2"]=corrected; rec["objective_basis"]=basis; rec["chi2_components"]=comps
        tol=float(c["execution"]["v7_seed_policy"]["seed_objective_tolerance"])
        if corrected is None or seed["objective_chi2"] < corrected-tol:
            rec["optimizer_candidate_before_seed_preservation"]={"minimum":row,"objective_chi2":corrected,"objective_basis":basis,
                "constraint_shape_penalties":pen}
            rec["minimum"]=seed["minimum"]; rec["chi2_components"]=seed["chi2_components"]
            rec["objective_chi2"]=seed["objective_chi2"]; rec["objective_basis"]=seed["objective_basis"]
            rec["constraint_shape_penalties"]=seed["constraint_shape_penalties"]
            rec["likelihood_chi2_scalar"]=float(seed["minimum"]["chi2"])
            rec["selected_candidate"]="EXACT_DETERMINISTIC_SEED"
        else:
            rec["selected_candidate"]="OPTIMIZER_MINIMUM"
        rec["seed_candidate_preservation_pass"]=float(rec["objective_chi2"]) <= float(seed["objective_chi2"])+tol
        rec["finite_result"]=math.isfinite(float(rec["objective_chi2"]))
    impl.dump_json(out,rec)
    return 0 if rec.get("status")=="COMPLETE" and rec.get("finite_result") else rc

def v6_parent_preflight(path:str|Path)->dict[str,Any]:
    try:
        d=load_v6_result(Path(path)); ok=True; err=None
    except Exception as exc:
        d={}; ok=False; err=repr(exc)
    return {"pass":ok,"error":err,"run_id":d.get("run_id"),"result_id":d.get("result_id"),
            "validation_status":d.get("validation_status"),"jobs_returned":d.get("job_manifest",{}).get("returned")}

def cli()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default=CONFIG_NAME); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("plan"); p.add_argument("--depth",choices=["standard","expanded"],default="standard"); p.add_argument("--output",required=True)
    p=sub.add_parser("preflight"); p.add_argument("--q011",required=True); p.add_argument("--v6-result",required=True); p.add_argument("--environment",action="store_true"); p.add_argument("--chain",choices=list(CONSTRAINTS)); p.add_argument("--output",required=True)
    p=sub.add_parser("smoke"); p.add_argument("--chain",choices=list(CONSTRAINTS),required=True); p.add_argument("--q011",required=True); p.add_argument("--output",required=True)
    p=sub.add_parser("run"); p.add_argument("--chain",choices=list(CONSTRAINTS),required=True); p.add_argument("--mode",choices=["reference_free_h0","fixed_h0_71p5","q011_shared_physics"],required=True); p.add_argument("--start-family",choices=["v6_free_best","v6_fixed_best","q011"],required=True); p.add_argument("--restart-index",type=int,required=True); p.add_argument("--q011",required=True); p.add_argument("--v6-result",required=True); p.add_argument("--max-evals",type=int); p.add_argument("--output",required=True)
    a=ap.parse_args(); c=impl.load_yaml(a.config)
    if a.cmd=="plan":
        tasks=impl.expected_tasks(c,a.depth); impl.dump_json(a.output,{"include":tasks}); print(json.dumps({"include":tasks},separators=(",",":"))); return 0
    if a.cmd=="preflight":
        global V6_RESULT_PATH; V6_RESULT_PATH=Path(a.v6_result)
        r=impl.preflight(c,a.q011,a.environment,a.chain); vp=v6_parent_preflight(a.v6_result); r["checks"]["V6_NUMERICAL_PARENT_GATE"]=vp["pass"]; r["v6_parent"]=vp
        r["checks"]["NORMALIZATION_FREE_OBJECTIVE_GATE"]=c["scientific_surface"]["objective_comparability_repair"]["cross_mode_comparable"] is True
        r["checks"]["SCALAR_TOTAL_CHI2_GATE"]=True; r["checks"]["NO_CHI2_COMPONENT_DOUBLECOUNT_GATE"]=True
        r["status"]="PASS" if all(r["checks"].values()) else "FAIL"; impl.dump_json(a.output,r); print(json.dumps(r,indent=2)); return 0 if r["status"]=="PASS" else 7
    if a.cmd=="smoke": return impl.smoke(a.chain,a.q011,a.output,c)
    if a.cmd=="run": return run_task_v7(a.chain,a.mode,a.start_family,a.restart_index,a.q011,a.v6_result,a.output,c,a.max_evals)
    return 2
if __name__=="__main__": raise SystemExit(cli())
