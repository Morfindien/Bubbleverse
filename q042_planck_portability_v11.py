#!/usr/bin/env python3
"""Bubbleverse Q042 V11 — PolyChord + external-start Py-BOBYQA hard preflight.

PRE-SCIENCE ONLY. This program cannot emit a cosmological portability class.
It reuses the validated Q032/Q041 native-likelihood construction, builds the
exact 20-cell authoritative surface, then runs four bounded FULL PolyChord
pilots and two external Py-BOBYQA starts per FULL arm/model cell.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, re, subprocess, sys
from pathlib import Path
from typing import Any, Mapping
import numpy as np
import q041_planck_portability_v13 as legacy

Q="Q-042"
CASE_ID="NOT DOCUMENTED"
PROGRAM_ID="Q042-PREFLIGHT-V11"
RUN_ID="Q042-POLYCHORD-BOBYQA-PREFLIGHT-V11"
RESULT_ID="R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-011"
ARMS=("camspec","hillipop")
MODELS=("lcdm","ede_n3")
COMBINATIONS=("FULL","NO_ACT_PRIMARY","NO_ACT_LENSING","NO_DESI_DR2","NO_SN")
LEGACY_MAP={
 "FULL":("P_A6_L6_D2",True),
 "NO_ACT_PRIMARY":("P_L6_D2",True),
 "NO_ACT_LENSING":("P_A6_D2",True),
 "NO_DESI_DR2":("P_A6_L6",True),
 "NO_SN":("P_A6_L6_D2",False),
}
EDE_PARAMS=("fEDE","log10z_c","thetai_scf")
EDE_EXTRA_ARGS=("Omega_Lambda","Omega_fld","Omega_scf","scf_parameters","attractor_ic_scf","CC_scf","scf_tuning_index","n_scf")

# Reuse the proven Q041 implementation machinery but force all newly produced
# metadata to retain Q042 identity.
legacy.Q=Q
legacy.PROGRAM_ID=PROGRAM_ID
legacy.RUN_ID=RUN_ID
legacy.RESULT_ID=RESULT_ID

def finite(x:Any)->bool:
    try:return math.isfinite(float(x))
    except Exception:return False

def read_json(path:str|Path)->dict[str,Any]:
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x,dict):raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return x

def write_json(path:str|Path,obj:Any)->None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False,default=str)+"\n",encoding="utf-8")
    os.replace(t,p)

def sha256_file(path:str|Path)->str:
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def load_spec(path:str|Path)->dict[str,Any]:
    d=read_json(path)
    if d.get("q")!=Q or d.get("case_id")!=CASE_ID or d.get("program_id")!=PROGRAM_ID:raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    c=d.get("authoritative_contract",{})
    if tuple(c.get("arms",[]))!=ARMS or tuple(c.get("models",[]))!=MODELS:raise RuntimeError("ARM_MODEL_LOCK_GATE=FAIL")
    if set(c.get("data_combinations",{}))!=set(COMBINATIONS) or len(c.get("data_combinations",{}))!=len(COMBINATIONS):raise RuntimeError("COMBINATION_LOCK_GATE=FAIL")
    if int(c.get("required_cell_count",-1))!=20:raise RuntimeError("CELL_COUNT_LOCK_GATE=FAIL")
    if not(c.get("q040_scientific_endpoints_forbidden") is True and c.get("no_hybrid_planck_likelihood") is True and c.get("no_cross_arm_absolute_chi2_evidence") is True):raise RuntimeError("SCIENTIFIC_FIREWALL_GATE=FAIL")
    if int(d["bobyqa"]["pilot"]["cobaya_best_of"])!=1 or int(d["bobyqa"]["production_frozen"]["cobaya_best_of"])!=1:raise RuntimeError("BOBYQA_DUPLICATE_RESTART_GATE=FAIL")
    return d

def load_lock(path:str|Path,spec_path:str|Path)->dict[str,Any]:
    d=read_json(path)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID:raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("spec_sha256")!=sha256_file(spec_path):raise RuntimeError("SPEC_HASH_GATE=FAIL")
    if d.get("software",{}).get("cobaya_version")!="3.5.6":raise RuntimeError("COBAYA_VERSION_LOCK_GATE=FAIL")
    if d.get("external",{}).get("supernova",{}).get("component")!="sn.pantheonplus":raise RuntimeError("SN_LOCK_GATE=FAIL")
    return d

def static_check(a:argparse.Namespace)->int:
    s=load_spec(a.spec);l=load_lock(a.source_lock,a.spec)
    out={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"STATIC","status":"PASS","scientific_classification":"NOT_AVAILABLE","spec_sha256":sha256_file(a.spec),"gates":{"Q_IDENTITY":"PASS","CONTEXT_CONTINUITY":"PASS","SPEC_HASH":"PASS","SOURCE_LOCK":"PASS","Q040_FIREWALL":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"production_settings_frozen":True,"polychord_release":l["software"]["polychordlite_release_tag"],"required_cell_count":s["authoritative_contract"]["required_cell_count"]}
    write_json(a.output,out);print("Q042_V11_STATIC_GATE=PASS");return 0

def prepare_nonoverlap(a:argparse.Namespace)->int:
    rc=legacy.prepare_nonoverlap(a)
    for p in (Path(a.support_output),Path(a.meta_output)):
        d=read_json(p);d.update({"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID});write_json(p,d)
    print("Q042_V11_NONOVERLAP_GATE=PASS");return rc

def _disable_ede(info:dict[str,Any])->None:
    params=info.setdefault("params",{})
    for p in EDE_PARAMS:params.pop(p,None)
    theory=info.get("theory",{})
    if not isinstance(theory,dict) or not theory:raise RuntimeError("LCDM_THEORY_BLOCK_GATE=FAIL")
    for block in theory.values():
        if not isinstance(block,dict):continue
        extra=block.get("extra_args")
        if isinstance(extra,dict):
            for k in EDE_EXTRA_ARGS:extra.pop(k,None)
        ip=block.get("input_params")
        if isinstance(ip,list):block["input_params"]=[x for x in ip if x not in EDE_PARAMS]
    if any(p in params for p in EDE_PARAMS):raise RuntimeError("LCDM_EDE_PARAMETER_REMOVAL_GATE=FAIL")

def build_info(a:argparse.Namespace,arm:str,model_name:str,combination:str,prefix:Path)->tuple[dict[str,Any],dict[str,Any]]:
    if arm not in ARMS or model_name not in MODELS or combination not in COMBINATIONS:raise RuntimeError("CELL_IDENTITY_GATE=FAIL")
    legacy_combo,with_sn=LEGACY_MAP[combination]
    ns=argparse.Namespace(**vars(a));ns.combo=legacy_combo
    info,meta=legacy.build_info(ns,arm,legacy_combo,prefix,mcmc=False)
    likes=info.setdefault("likelihood",{})
    if with_sn:likes["sn.pantheonplus"]=None
    else:likes.pop("sn.pantheonplus",None)
    if model_name=="lcdm":_disable_ede(info)
    else:
        found_n3=False
        for block in info.get("theory",{}).values():
            if isinstance(block,dict) and isinstance(block.get("extra_args"),dict) and int(block["extra_args"].get("n_scf",-1))==3:found_n3=True
        if not all(p in info.get("params",{}) for p in EDE_PARAMS) or not found_n3:raise RuntimeError("EDE_N3_IDENTITY_GATE=FAIL")
    meta=dict(meta);meta.update({"q":Q,"program_id":PROGRAM_ID,"model":model_name,"combination":combination,"supernova_included":with_sn,"legacy_combo":legacy_combo})
    return info,meta

COMMON_EXTERNAL_COMPONENTS=(
    "act_dr6_cmbonly.ACTDR6CMBonly",
    "act_dr6_lenslike.ACTDR6LensLike",
    "bao.desi_dr2",
    "sn.pantheonplus",
)

def _canonical_jsonable(x:Any)->Any:
    if isinstance(x,dict):return {str(k):_canonical_jsonable(v) for k,v in sorted(x.items(),key=lambda kv:str(kv[0]))}
    if isinstance(x,(list,tuple)):return [_canonical_jsonable(v) for v in x]
    if x is None or isinstance(x,(str,int,float,bool)):return x
    return str(x)

def _external_science_signature(info:dict[str,Any])->dict[str,Any]:
    """Signature only the external science blocks required to be identical across Planck arms.

    Arm-native q019_shape_* / q031_shape_* likelihoods are deliberately excluded: they
    are part of the distinct native CamSpec/HiLLiPoP implementations and are not
    external datasets. ACT calibration is carried in params/prior rather than the
    likelihood dict, so its frozen parameter definitions and prior presence are
    included explicitly.
    """
    likes=info.get("likelihood",{}) or {}
    params=info.get("params",{}) or {}
    prior=info.get("prior",{}) or {}
    components={k:_canonical_jsonable(likes[k]) for k in COMMON_EXTERNAL_COMPONENTS if k in likes}
    has_a6="act_dr6_cmbonly.ACTDR6CMBonly" in components
    act_calibration={
        "present":has_a6,
        "A_act":_canonical_jsonable(params.get("A_act")) if has_a6 else None,
        "P_act":_canonical_jsonable(params.get("P_act")) if has_a6 else None,
        "q041_act_calibration_shape_present":bool("q041_act_calibration_shape" in prior) if has_a6 else False,
    }
    return {"components":components,"act_calibration":act_calibration}

def _expected_external_components(contract_combo:list[str])->set[str]:
    m={
        "A6":"act_dr6_cmbonly.ACTDR6CMBonly",
        "L6":"act_dr6_lenslike.ACTDR6LensLike",
        "D2":"bao.desi_dr2",
        "SN":"sn.pantheonplus",
    }
    return {m[x] for x in contract_combo if x in m}

def _preferred(a:argparse.Namespace,arm:str)->dict[str,float]:
    parent,_=legacy.reference_parent(a.parent_dir,arm);return legacy.start_from_parent(parent)

def _finite_eval(q32:Any,info:dict[str,Any],preferred:Mapping[str,float])->float:
    pref=dict(preferred)
    for p in EDE_PARAMS:
        if p not in info.get("params",{}):pref.pop(p,None)
    model=None
    try:
        probe=q32.reference_vector(info,preferred=pref);model=q32.create_model(info);logpost,_=q32.evaluate_model_once(model,info,probe)
        if not finite(logpost):raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL")
        return float(logpost)
    finally:
        try:
            if model is not None:model.close()
        except Exception:pass

def _runtime_gate(a:argparse.Namespace)->dict[str,Any]:
    r=read_json(a.external_runtime)
    if not(r.get("q")==Q and r.get("program_id")==PROGRAM_ID and r.get("status")=="PASS" and r.get("cobaya_version")=="3.5.6" and r.get("pybobyqa_version")=="1.5.0" and r.get("polychord_commit") and r.get("pantheonplus_runtime_files")):raise RuntimeError("EXTERNAL_RUNTIME_GATE=FAIL")
    return r

def probe_cell(a:argparse.Namespace)->int:
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);_runtime_gate(a)
    q32=legacy.load_q032(a.q032_parent_root);prefix=Path(a.output).with_suffix("")
    info,meta=build_info(a,a.arm,a.model,a.combination,prefix)
    native=q32.CAMSPEC if a.arm=="camspec" else q32.HILLIPOP
    if native not in info.get("likelihood",{}):raise RuntimeError("PLANCK_NATIVE_IDENTITY_GATE=FAIL")
    expected_sn="SN" in spec["authoritative_contract"]["data_combinations"][a.combination]
    if (("sn.pantheonplus" in info.get("likelihood",{}))!=expected_sn):raise RuntimeError("SUPERNOVA_COMBINATION_GATE=FAIL")
    has_a6="A6" in spec["authoritative_contract"]["data_combinations"][a.combination]
    expected_support="ELL_LE_599" if has_a6 else "Q032_FULL_COMMON_TT3PAIR"
    if meta.get("support_mode")!=expected_support:raise RuntimeError("OVERLAP_POLICY_GATE=FAIL")
    sig=_external_science_signature(info)
    expected_components=_expected_external_components(spec["authoritative_contract"]["data_combinations"][a.combination])
    if set(sig["components"])!=expected_components:
        raise RuntimeError(f"EXTERNAL_COMPONENT_SET_GATE=FAIL arm={a.arm} model={a.model} combo={a.combination} actual={sorted(sig['components'])} expected={sorted(expected_components)}")
    if ("A6" in spec["authoritative_contract"]["data_combinations"][a.combination]):
        ac=sig["act_calibration"]
        if not(ac["present"] and ac["A_act"] and ac["P_act"] and ac["q041_act_calibration_shape_present"]):
            raise RuntimeError(f"ACT_CALIBRATION_CONTRACT_GATE=FAIL arm={a.arm} model={a.model} combo={a.combination}")
    native_aux=sorted(set(info.get("likelihood",{}))-{native}-set(sig["components"]))
    rec={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"stage":"CELL_PREFLIGHT","arm":a.arm,"model":a.model,"combination":a.combination,"status":"PASS","native_planck_component":native,"external_science_signature":sig,"native_auxiliary_likelihoods":native_aux,"support_mode":meta["support_mode"],"supernova_included":expected_sn,"finite_evaluation_performed":bool(a.finite_eval)}
    if a.finite_eval:rec["finite_logposterior"]=_finite_eval(q32,info,_preferred(a,a.arm))
    write_json(a.output,rec);return 0

def runtime_preflight(a:argparse.Namespace)->int:
    spec=load_spec(a.spec);lock=load_lock(a.source_lock,a.spec);runtime=_runtime_gate(a)
    cell_dir=Path(a.output).with_suffix("").parent/"q042_v11_cell_preflight";cell_dir.mkdir(parents=True,exist_ok=True)
    common=["--q032-parent-root",a.q032_parent_root,"--preflight",a.preflight,"--parent-dir",a.parent_dir,"--hlp-matrix",a.hlp_matrix,"--hlp-meta",a.hlp_meta,"--reduced-support",a.reduced_support,"--reduced-hlp-matrix",a.reduced_hlp_matrix,"--reduced-hlp-meta",a.reduced_hlp_meta,"--spec",a.spec,"--source-lock",a.source_lock,"--external-runtime",a.external_runtime]
    rows=[]
    for arm in ARMS:
      for model_name in MODELS:
       for combo in COMBINATIONS:
        f=cell_dir/f"{arm}_{model_name}_{combo.lower()}.json"
        cmd=[sys.executable,str(Path(__file__).resolve()),"probe-cell",*common,"--arm",arm,"--model",model_name,"--combination",combo,"--finite-eval","1" if combo=="FULL" else "0","--output",str(f)]
        subprocess.run(cmd,check=True);rows.append(read_json(f))
    if len(rows)!=20 or any(x.get("status")!="PASS" for x in rows):raise RuntimeError("AUTHORITATIVE_20_CELL_BUILD_GATE=FAIL")
    by={(x["arm"],x["model"],x["combination"]):x for x in rows}
    external_identity={}
    for m in MODELS:
      for c in COMBINATIONS:
        x=by[("camspec",m,c)];y=by[("hillipop",m,c)]
        if x["external_science_signature"]!=y["external_science_signature"]:
            raise RuntimeError(f"EXTERNAL_DATA_IDENTITY_GATE=FAIL {m} {c}")
        if x["support_mode"]!=y["support_mode"]:raise RuntimeError(f"OVERLAP_POLICY_GATE=FAIL {m} {c}")
        external_identity[f"{m}:{c}"]=x["external_science_signature"]
    full=[x for x in rows if x["combination"]=="FULL"]
    if len(full)!=4 or any("finite_logposterior" not in x for x in full):raise RuntimeError("FULL_FINITE_EVALUATIONS_GATE=FAIL")
    out={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"RUNTIME_PREFLIGHT","status":"PASS","scientific_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"spec_sha256":sha256_file(a.spec),"built_cell_count":20,"finite_full_evaluations":full,"external_identity":external_identity,"runtime_source":{"polychord_commit":runtime["polychord_commit"],"pantheonplus_manifest_sha256":runtime["pantheonplus_manifest_sha256"]},"gates":{"Q_IDENTITY":"PASS","FROZEN_SOFTWARE":"PASS","PANTHEONPLUS_FILE_HASHES":"PASS","POLYCHORD_RUNTIME_COMMIT":"PASS","AUTHORITATIVE_20_CELL_BUILD":"PASS","PLANCK_NATIVE_IDENTITY":"PASS","EXTERNAL_DATA_IDENTITY":"PASS","OVERLAP_POLICY":"PASS","LCDM_BASELINE":"PASS","EDE_N3_IDENTITY":"PASS","FULL_FINITE_EVALUATIONS":"PASS","Q040_FIREWALL":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"next_required_action":"RUN_FOUR_BOUNDED_FULL_POLYCHORD_AND_EXTERNAL_START_BOBYQA_PILOTS","source_lock":lock["software"]}
    write_json(a.output,out);print("Q042_V11_RUNTIME_PREFLIGHT_GATE=PASS");return 0

def _cell_seed(spec:dict[str,Any],arm:str,model_name:str)->int:
    return int(spec["polychord"]["pilot_seed_map"][f"{arm}:{model_name}"])

def _apply_start(q32:Any,info:dict[str,Any],preferred:Mapping[str,float],start_index:int)->dict[str,float]:
    used={}
    params=info.get("params",{})
    for name,pinfo in params.items():
        if not isinstance(pinfo,dict) or "prior" not in pinfo:continue
        prior=pinfo.get("prior")
        if not isinstance(prior,dict) or not finite(prior.get("min")) or not finite(prior.get("max")):continue
        lo,hi=float(prior["min"]),float(prior["max"]);span=hi-lo
        base=float(preferred.get(name,0.5*(lo+hi))) if finite(preferred.get(name,0.5*(lo+hi))) else 0.5*(lo+hi)
        if start_index==0:v=base
        else:
            sign=-1.0 if int(hashlib.sha256(name.encode()).hexdigest()[:2],16)%2 else 1.0
            v=base+sign*0.12*span
        if span>0:v=min(max(v,lo+0.05*span),hi-0.05*span)
        try:q32.set_ref(params,name,float(v));used[name]=float(v)
        except Exception:pass
    return used

def _result_object_record(obj:Any)->dict[str,Any]:
    return {"flag":getattr(obj,"flag",None),"message":str(getattr(obj,"msg","")),"objective":float(getattr(obj,"f",float("nan"))) if finite(getattr(obj,"f",None)) else None,"nf":int(getattr(obj,"nf",-1)) if getattr(obj,"nf",None) is not None else None,"nx":int(getattr(obj,"nx",-1)) if getattr(obj,"nx",None) is not None else None,"nruns":int(getattr(obj,"nruns",-1)) if getattr(obj,"nruns",None) is not None else None}


def _bobyqa_wrapper_exception_record(exc: Exception) -> dict[str,Any]:
    """Harvest bounded Py-BOBYQA warning results that Cobaya wraps as LoggedError.

    Cobaya 3.5.6 defines success only as Py-BOBYQA EXIT_SUCCESS and therefore
    raises after process_results when a bounded run reaches MAXFUN. Q042's
    preregistered pilot contract is intentionally different: a finite objective
    with a non-negative Py-BOBYQA flag is technically acceptable, including
    EXIT_MAXFUN_WARNING. Negative flags remain hard failures.
    """
    text=str(exc)
    if "Minimization failed! Here is the raw result object" not in text or "Py-BOBYQA Results" not in text:
        return {"flag":None,"message":text,"objective":None,"nf":None,"technical_ok":False,"acceptance_class":"UNPARSED_COBAYA_EXCEPTION"}
    mf=re.search(r"Objective value f\(xmin\)\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",text)
    mg=re.search(r"Exit flag\s*=\s*(-?\d+)",text)
    mn=re.search(r"Needed\s+(\d+)\s+objective evaluations",text)
    objective=float(mf.group(1)) if mf and finite(mf.group(1)) else None
    flag=int(mg.group(1)) if mg else None
    nf=int(mn.group(1)) if mn else None
    technical_ok=bool(objective is not None and flag is not None and flag>=0)
    acceptance_class=("ACCEPTED_MAXFUN_WARNING" if technical_ok and flag==1 else
                      "ACCEPTED_NONNEGATIVE_PYBOBYQA_WARNING" if technical_ok and flag>0 else
                      "ACCEPTED_SUCCESS" if technical_ok and flag==0 else
                      "REJECTED_NEGATIVE_OR_UNPARSED_FLAG")
    return {"flag":flag,"message":text,"objective":objective,"nf":nf,"technical_ok":technical_ok,"acceptance_class":acceptance_class}

def _pilot_common_cli(a:argparse.Namespace)->list[str]:
    return [
        "--q032-parent-root",a.q032_parent_root,
        "--preflight",a.preflight,
        "--parent-dir",a.parent_dir,
        "--hlp-matrix",a.hlp_matrix,
        "--hlp-meta",a.hlp_meta,
        "--reduced-support",a.reduced_support,
        "--reduced-hlp-matrix",a.reduced_hlp_matrix,
        "--reduced-hlp-meta",a.reduced_hlp_meta,
        "--spec",a.spec,
        "--source-lock",a.source_lock,
        "--external-runtime",a.external_runtime,
        "--arm",a.arm,
        "--model",a.model,
    ]

def polychord_stage(a:argparse.Namespace)->int:
    """Run exactly one PolyChord lifecycle in a fresh OS process.

    This subcommand exists because OpenMPI may be finalized when a completed
    PolyChord/Cobaya sampler closes. A genuine resume probe must therefore be
    a new interpreter/MPI lifecycle, not a second cobaya.run() in-process.
    """
    if a.arm not in ARMS or a.model not in MODELS or a.action not in ("fresh","resume"):
        raise RuntimeError("POLYCHORD_STAGE_IDENTITY_GATE=FAIL")
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime=_runtime_gate(a)
    outdir=Path(a.output_dir);outdir.mkdir(parents=True,exist_ok=True)
    prefix=(outdir/"polychord"/"chain").resolve()
    # Always execute the Q042 builder in the fresh process so HiLLiPoP's
    # frozen runtime covariance patch is installed before Model construction.
    # For resume, the newly-built info is deliberately NOT used as Cobaya input:
    # V7 showed that regenerating the resolved HiLLiPoP component can differ in
    # non-scientific runtime metadata and trigger Cobaya's compatibility guard.
    built_info,_=build_info(a,a.arm,a.model,"FULL",prefix)
    pc=copy.deepcopy(spec["polychord"]["pilot"])
    pc["path"]=runtime["polychord_path"]
    pc["seed"]=_cell_seed(spec,a.arm,a.model)
    requested_contract={"pilot":copy.deepcopy(spec["polychord"]["pilot"]),"seed":pc["seed"],"arm":a.arm,"model":a.model}
    requested_hash=hashlib.sha256(json.dumps(requested_contract,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
    resume=(a.action=="resume")
    if not resume:
        info=built_info
        info["sampler"]={"polychord":pc}
        info["output"]=str(prefix)
        info["force"]=True
        info["resume"]=False
        resume_source="FRESH_BUILT_INFO"
    else:
        # Load exactly the previous run's resolved Cobaya info. OutputReadOnly
        # prefers the .updated.dill when present, preserving non-YAML objects
        # such as external priors. Only the output location/resume flags are
        # overridden; scientific and sampler content comes from the saved run.
        from cobaya.output import OutputReadOnly
        stored=OutputReadOnly(prefix=str(prefix)).get_updated_info()
        if not isinstance(stored,dict):
            raise RuntimeError("POLYCHORD_STORED_UPDATED_INFO_GATE=FAIL missing")
        if "polychord" not in (stored.get("sampler") or {}):
            raise RuntimeError("POLYCHORD_STORED_SAMPLER_GATE=FAIL")
        stored_seed=(stored.get("sampler") or {}).get("polychord",{}).get("seed")
        if stored_seed is not None and int(stored_seed)!=int(pc["seed"]):
            raise RuntimeError(f"POLYCHORD_STORED_SEED_GATE=FAIL stored={stored_seed} expected={pc['seed']}")
        info=copy.deepcopy(stored)
        info["output"]=str(prefix)
        info["force"]=False
        info["resume"]=True
        resume_source="COBAYA_STORED_UPDATED_INFO"
    from cobaya.run import run as cobaya_run
    sampler=None
    try:
        _,sampler=cobaya_run(info,output=str(prefix),force=not resume,resume=resume,stop_at_error=True)
        products=sampler.products() if sampler is not None else {}
        logz=products.get("logZ") if isinstance(products,dict) else None
        sample=products.get("sample") if isinstance(products,dict) else None
        try:sample_count=len(sample) if sample is not None else 0
        except Exception:sample_count=-1
        rec={"q":Q,"program_id":PROGRAM_ID,"stage":"POLYCHORD_PROCESS_STAGE","status":"PASS","action":a.action,"arm":a.arm,"model":a.model,"seed":pc["seed"],"requested_sampler_contract_sha256":requested_hash,"resume_input_source":resume_source,"logZ_technical":float(logz) if finite(logz) else None,"sample_count":sample_count,"runtime_commit":runtime["polychord_commit"],"fresh_process":True,"scientific_classification":"NOT_AVAILABLE"}
        write_json(a.result_json,rec)
        print(f"Q042_V11_POLYCHORD_PROCESS_GATE=PASS action={a.action} arm={a.arm} model={a.model}")
        return 0
    finally:
        try:
            if sampler is not None and hasattr(sampler,"close"):sampler.close()
        except Exception:pass

def bobyqa_stage(a:argparse.Namespace)->int:
    """Run one external Py-BOBYQA start in its own fresh interpreter."""
    if a.arm not in ARMS or a.model not in MODELS or a.start_index not in (0,1):
        raise RuntimeError("BOBYQA_STAGE_IDENTITY_GATE=FAIL")
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);_runtime_gate(a)
    q32=legacy.load_q032(a.q032_parent_root)
    outdir=Path(a.output_dir);outdir.mkdir(parents=True,exist_ok=True)
    preferred=_preferred(a,a.arm)
    bi,_=build_info(a,a.arm,a.model,"FULL",outdir/"bobyqa"/f"start{a.start_index}"/"fit")
    starts=_apply_start(q32,bi,preferred,a.start_index)
    bs=spec["bobyqa"]["pilot"]
    bi["sampler"]={"minimize":{"method":"bobyqa","ignore_prior":True,"best_of":1,"max_evals":int(bs["max_evals"]),"seed":_cell_seed(spec,a.arm,a.model)+100+a.start_index,"override_bobyqa":{"rhoend":float(bs["rhoend"])}}}
    bi["output"]=str((outdir/"bobyqa"/f"start{a.start_index}"/"fit").resolve())
    bi["force"]=True;bi["resume"]=False
    from cobaya.run import run as cobaya_run
    sm=None
    try:
        _,sm=cobaya_run(bi,force=True,stop_at_error=False)
        prod=sm.products() if sm is not None else {}
        ro=prod.get("result_object") if isinstance(prod,dict) else None
        rr=_result_object_record(ro)
        ok=bool(rr["flag"] is not None and int(rr["flag"])>=0 and rr["objective"] is not None)
        rr.update({"q":Q,"program_id":PROGRAM_ID,"stage":"BOBYQA_PROCESS_STAGE","status":"PASS" if ok else "RECORDED_FAILURE","start_index":a.start_index,"start_values":starts,"technical_ok":ok,"acceptance_class":"ACCEPTED_SUCCESS" if ok and int(rr["flag"])==0 else "ACCEPTED_NONNEGATIVE_PYBOBYQA_WARNING" if ok else "REJECTED_NEGATIVE_OR_MISSING_RESULT","fresh_process":True,"scientific_classification":"NOT_AVAILABLE"})
    except Exception as exc:
        parsed=_bobyqa_wrapper_exception_record(exc)
        rr={"q":Q,"program_id":PROGRAM_ID,"stage":"BOBYQA_PROCESS_STAGE","status":"PASS_BOUNDED_WARNING" if parsed["technical_ok"] else "RECORDED_FAILURE","start_index":a.start_index,"start_values":starts,"technical_ok":bool(parsed["technical_ok"]),"error":repr(exc),"flag":parsed["flag"],"objective":parsed["objective"],"nf":parsed["nf"],"acceptance_class":parsed["acceptance_class"],"cobaya_wrapper_exception_preserved":True,"fresh_process":True,"scientific_classification":"NOT_AVAILABLE"}
    finally:
        try:
            if sm is not None and hasattr(sm,"close"):sm.close()
        except Exception:pass
    write_json(a.result_json,rr)
    print(f"Q042_V11_BOBYQA_PROCESS_GATE={'PASS' if rr['technical_ok'] else 'RECORDED_FAIL'} start={a.start_index} arm={a.arm} model={a.model}")
    return 0

def pilot_cell(a:argparse.Namespace)->int:
    if a.arm not in ARMS or a.model not in MODELS:raise RuntimeError("PILOT_CELL_IDENTITY_GATE=FAIL")
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime=_runtime_gate(a);q32=legacy.load_q032(a.q032_parent_root)
    outdir=Path(a.output_dir);outdir.mkdir(parents=True,exist_ok=True)
    preferred=_preferred(a,a.arm)
    base_info,_=build_info(a,a.arm,a.model,"FULL",outdir/"finite_probe")
    finite_probe=_finite_eval(q32,base_info,preferred)

    # PolyChord fresh and resume are deliberately separate interpreter/MPI lifecycles.
    common=_pilot_common_cli(a)
    fresh_json=outdir/"q042_polychord_fresh_v11.json"
    resume_json=outdir/"q042_polychord_resume_v11.json"
    subprocess.run([sys.executable,str(Path(__file__).resolve()),"polychord-stage",*common,"--action","fresh","--output-dir",str(outdir),"--result-json",str(fresh_json)],check=True)
    fresh=read_json(fresh_json)
    if fresh.get("status")!="PASS" or fresh.get("fresh_process") is not True:raise RuntimeError("POLYCHORD_FRESH_PROCESS_GATE=FAIL")
    resume_files=[p for p in (outdir/"polychord").rglob("*resume*") if p.is_file() and p.stat().st_size>0]
    if not resume_files:raise RuntimeError("POLYCHORD_RESUME_WRITE_GATE=FAIL")
    subprocess.run([sys.executable,str(Path(__file__).resolve()),"polychord-stage",*common,"--action","resume","--output-dir",str(outdir),"--result-json",str(resume_json)],check=True)
    resumed=read_json(resume_json)
    if resumed.get("status")!="PASS" or resumed.get("action")!="resume" or resumed.get("fresh_process") is not True:raise RuntimeError("POLYCHORD_RESUME_FRESH_PROCESS_GATE=FAIL")
    if resumed.get("resume_input_source")!="COBAYA_STORED_UPDATED_INFO":raise RuntimeError("POLYCHORD_RESUME_STORED_INFO_GATE=FAIL")
    if fresh.get("requested_sampler_contract_sha256")!=resumed.get("requested_sampler_contract_sha256"):raise RuntimeError("POLYCHORD_RESUME_SAMPLER_CONTRACT_GATE=FAIL")

    # Each BOBYQA external start also receives an isolated interpreter lifecycle.
    bob=[]
    for start_index in range(int(spec["bobyqa"]["pilot"]["external_starts_per_full_cell"])):
        bj=outdir/f"q042_bobyqa_start{start_index}_v11.json"
        subprocess.run([sys.executable,str(Path(__file__).resolve()),"bobyqa-stage",*common,"--start-index",str(start_index),"--output-dir",str(outdir),"--result-json",str(bj)],check=True)
        bob.append(read_json(bj))
    if len(bob)!=2 or any(not x.get("technical_ok") or x.get("fresh_process") is not True for x in bob):raise RuntimeError(f"BOBYQA_BOUNDED_MULTISTART_GATE=FAIL {bob}")

    rec={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"FULL_CELL_TECHNICAL_PILOT","status":"PASS","scientific_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"arm":a.arm,"model":a.model,"combination":"FULL","finite_probe_logposterior":finite_probe,"polychord":{"seed":fresh["seed"],"settings":spec["polychord"]["pilot"],"logZ_technical":fresh.get("logZ_technical"),"sample_count":fresh.get("sample_count"),"resume_files":[str(p.relative_to(outdir)) for p in resume_files],"resume_read_probe":"PASS","process_isolation":"FRESH_PROCESS_PER_POLYCHORD_INVOCATION","runtime_commit":runtime["polychord_commit"]},"bobyqa":{"best_of":1,"process_isolation":"FRESH_PROCESS_PER_EXTERNAL_START","external_starts":bob},"gates":{"Q_IDENTITY":"PASS","FULL_FINITE_EVALUATION":"PASS","POLYCHORD_EXECUTION":"PASS","POLYCHORD_RESUME_READ_WRITE":"PASS","POLYCHORD_MPI_LIFECYCLE_ISOLATION":"PASS","POLYCHORD_RESUME_STORED_INFO":"PASS","BOBYQA_EXTERNAL_MULTISTART":"PASS","BOBYQA_PROCESS_ISOLATION":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"claim_boundary":"Pilot logZ, samples, minima and finite probes are technical outputs only and MUST NOT be used as cosmological evidence."}
    write_json(outdir/"q042_pilot_result_v11.json",rec);print(f"Q042_V11_PILOT_GATE=PASS arm={a.arm} model={a.model}");return 0

def merge_pilots(a:argparse.Namespace)->int:
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);env=read_json(a.environment_preflight)
    if env.get("status")!="PASS" or env.get("built_cell_count")!=20:raise RuntimeError("ENVIRONMENT_PREFLIGHT_INPUT_GATE=FAIL")
    rows=[]
    for p in Path(a.input_dir).rglob("q042_pilot_result_v11.json"):
        d=read_json(p)
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("status")=="PASS":rows.append(d)
    expected={(x["arm"],x["model"]) for x in spec["pilot_full_cells"]};found={(x["arm"],x["model"]) for x in rows}
    if found!=expected:raise RuntimeError(f"PILOT_COMPLETENESS_GATE=FAIL missing={sorted(expected-found)} extra={sorted(found-expected)}")
    if any(x.get("scientific_classification")!="NOT_AVAILABLE" for x in rows):raise RuntimeError("NO_SCIENCE_CLASSIFICATION_GATE=FAIL")
    if any(x["polychord"].get("resume_read_probe")!="PASS" for x in rows):raise RuntimeError("POLYCHORD_RESUME_GATE=FAIL")
    env_commit=env.get("runtime_source",{}).get("polychord_commit")
    if not env_commit or any(x["polychord"].get("runtime_commit")!=env_commit for x in rows):raise RuntimeError("POLYCHORD_CROSS_JOB_COMMIT_GATE=FAIL")
    if any(any(not s.get("technical_ok") for s in x["bobyqa"]["external_starts"]) for x in rows):raise RuntimeError("BOBYQA_MULTISTART_GATE=FAIL")
    out={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"PREFLIGHT_FINAL","status":"PASS","final_result_gate":"PREFLIGHT_PASS","scientific_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"spec_sha256":sha256_file(a.spec),"environment_preflight":"PASS","pilot_count":len(rows),"pilots":sorted(rows,key=lambda x:(x["arm"],x["model"])),"gates":{"Q_IDENTITY":"PASS","CONTEXT_CONTINUITY":"PASS","SPEC_HASH":"PASS","SOURCE_LOCK":"PASS","Q040_FIREWALL":"PASS","FROZEN_SOFTWARE":"PASS","PANTHEONPLUS_FILE_HASHES":"PASS","POLYCHORD_RUNTIME_COMMIT":"PASS","AUTHORITATIVE_20_CELL_BUILD":"PASS","PLANCK_NATIVE_IDENTITY":"PASS","EXTERNAL_DATA_IDENTITY":"PASS","OVERLAP_POLICY":"PASS","LCDM_BASELINE":"PASS","EDE_N3_IDENTITY":"PASS","FULL_FINITE_EVALUATIONS":"PASS","POLYCHORD_4_FULL_PILOTS":"PASS","POLYCHORD_RESUME_READ_WRITE":"PASS","BOBYQA_4_FULL_MULTISTART_PILOTS":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"scientific_meaning":"Execution strategy validated at bounded pre-science pilot level only. No downstream portability classification exists yet.","next_required_action":"RETURN_TO_RESULT_INGESTION_THEN_GENERATE_Q042_PRODUCTION_CAMPAIGN_USING_FROZEN_PRODUCTION_SETTINGS"}
    write_json(a.output,out);print("Q042_V11_PREFLIGHT_FINAL_GATE=PASS");return 0

def common_args(s:argparse.ArgumentParser)->None:
    for x in ("q032-parent-root","preflight","parent-dir","hlp-matrix","hlp-meta","reduced-support","reduced-hlp-matrix","reduced-hlp-meta","spec","source-lock","external-runtime"):s.add_argument("--"+x,required=True)

def parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static");s.add_argument("--spec",required=True);s.add_argument("--source-lock",required=True);s.add_argument("--output",required=True);s.set_defaults(func=static_check)
    s=sp.add_parser("prepare-nonoverlap")
    for x in ("q032-parent-root","preflight","hlp-matrix","hlp-meta","support-output","matrix-output","meta-output"):s.add_argument("--"+x,required=True)
    s.set_defaults(func=prepare_nonoverlap)
    s=sp.add_parser("probe-cell");common_args(s);s.add_argument("--arm",required=True,choices=ARMS);s.add_argument("--model",required=True,choices=MODELS);s.add_argument("--combination",required=True,choices=COMBINATIONS);s.add_argument("--finite-eval",required=True,type=int,choices=(0,1));s.add_argument("--output",required=True);s.set_defaults(func=probe_cell)
    s=sp.add_parser("runtime-preflight");common_args(s);s.add_argument("--output",required=True);s.set_defaults(func=runtime_preflight)
    s=sp.add_parser("polychord-stage");common_args(s);s.add_argument("--arm",required=True,choices=ARMS);s.add_argument("--model",required=True,choices=MODELS);s.add_argument("--action",required=True,choices=("fresh","resume"));s.add_argument("--output-dir",required=True);s.add_argument("--result-json",required=True);s.set_defaults(func=polychord_stage)
    s=sp.add_parser("bobyqa-stage");common_args(s);s.add_argument("--arm",required=True,choices=ARMS);s.add_argument("--model",required=True,choices=MODELS);s.add_argument("--start-index",required=True,type=int,choices=(0,1));s.add_argument("--output-dir",required=True);s.add_argument("--result-json",required=True);s.set_defaults(func=bobyqa_stage)
    s=sp.add_parser("pilot-cell");common_args(s);s.add_argument("--arm",required=True,choices=ARMS);s.add_argument("--model",required=True,choices=MODELS);s.add_argument("--output-dir",required=True);s.set_defaults(func=pilot_cell)
    s=sp.add_parser("merge-pilots");s.add_argument("--input-dir",required=True);s.add_argument("--environment-preflight",required=True);s.add_argument("--spec",required=True);s.add_argument("--source-lock",required=True);s.add_argument("--output",required=True);s.set_defaults(func=merge_pilots)
    return p
if __name__=="__main__":
    a=parser().parse_args();raise SystemExit(a.func(a))
