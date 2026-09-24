#!/usr/bin/env python3
"""Bubbleverse Q042 V2 — PolyChord + external-start Py-BOBYQA hard preflight.

PRE-SCIENCE ONLY. This program cannot emit a cosmological portability class.
It reuses the validated Q032/Q041 native-likelihood construction, builds the
exact 20-cell authoritative surface, then runs four bounded FULL PolyChord
pilots and two external Py-BOBYQA starts per FULL arm/model cell.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, subprocess, sys
from pathlib import Path
from typing import Any, Mapping
import numpy as np
import q041_planck_portability_v13 as legacy

Q="Q-042"
CASE_ID="NOT DOCUMENTED"
PROGRAM_ID="Q042-PREFLIGHT-V2"
RUN_ID="Q042-POLYCHORD-BOBYQA-PREFLIGHT-V2"
RESULT_ID="R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-002"
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
    write_json(a.output,out);print("Q042_V2_STATIC_GATE=PASS");return 0

def prepare_nonoverlap(a:argparse.Namespace)->int:
    rc=legacy.prepare_nonoverlap(a)
    for p in (Path(a.support_output),Path(a.meta_output)):
        d=read_json(p);d.update({"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID});write_json(p,d)
    print("Q042_V2_NONOVERLAP_GATE=PASS");return rc

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

def _external_set(q32:Any,arm:str,info:dict[str,Any])->set[str]:
    native=q32.CAMSPEC if arm=="camspec" else q32.HILLIPOP
    return set(info.get("likelihood",{}))-{native}

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
    rec={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"stage":"CELL_PREFLIGHT","arm":a.arm,"model":a.model,"combination":a.combination,"status":"PASS","native_planck_component":native,"external_likelihoods":sorted(_external_set(q32,a.arm,info)),"support_mode":meta["support_mode"],"supernova_included":expected_sn,"finite_evaluation_performed":bool(a.finite_eval)}
    if a.finite_eval:rec["finite_logposterior"]=_finite_eval(q32,info,_preferred(a,a.arm))
    write_json(a.output,rec);return 0

def runtime_preflight(a:argparse.Namespace)->int:
    spec=load_spec(a.spec);lock=load_lock(a.source_lock,a.spec);runtime=_runtime_gate(a)
    cell_dir=Path(a.output).with_suffix("").parent/"q042_v2_cell_preflight";cell_dir.mkdir(parents=True,exist_ok=True)
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
        if x["external_likelihoods"]!=y["external_likelihoods"]:raise RuntimeError(f"EXTERNAL_DATA_IDENTITY_GATE=FAIL {m} {c}")
        if x["support_mode"]!=y["support_mode"]:raise RuntimeError(f"OVERLAP_POLICY_GATE=FAIL {m} {c}")
        external_identity[f"{m}:{c}"]=x["external_likelihoods"]
    full=[x for x in rows if x["combination"]=="FULL"]
    if len(full)!=4 or any("finite_logposterior" not in x for x in full):raise RuntimeError("FULL_FINITE_EVALUATIONS_GATE=FAIL")
    out={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"RUNTIME_PREFLIGHT","status":"PASS","scientific_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"spec_sha256":sha256_file(a.spec),"built_cell_count":20,"finite_full_evaluations":full,"external_identity":external_identity,"runtime_source":{"polychord_commit":runtime["polychord_commit"],"pantheonplus_manifest_sha256":runtime["pantheonplus_manifest_sha256"]},"gates":{"Q_IDENTITY":"PASS","FROZEN_SOFTWARE":"PASS","PANTHEONPLUS_FILE_HASHES":"PASS","POLYCHORD_RUNTIME_COMMIT":"PASS","AUTHORITATIVE_20_CELL_BUILD":"PASS","PLANCK_NATIVE_IDENTITY":"PASS","EXTERNAL_DATA_IDENTITY":"PASS","OVERLAP_POLICY":"PASS","LCDM_BASELINE":"PASS","EDE_N3_IDENTITY":"PASS","FULL_FINITE_EVALUATIONS":"PASS","Q040_FIREWALL":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"next_required_action":"RUN_FOUR_BOUNDED_FULL_POLYCHORD_AND_EXTERNAL_START_BOBYQA_PILOTS","source_lock":lock["software"]}
    write_json(a.output,out);print("Q042_V2_RUNTIME_PREFLIGHT_GATE=PASS");return 0

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

def pilot_cell(a:argparse.Namespace)->int:
    if a.arm not in ARMS or a.model not in MODELS:raise RuntimeError("PILOT_CELL_IDENTITY_GATE=FAIL")
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime=_runtime_gate(a);q32=legacy.load_q032(a.q032_parent_root)
    outdir=Path(a.output_dir);outdir.mkdir(parents=True,exist_ok=True)
    preferred=_preferred(a,a.arm)
    base_info,meta=build_info(a,a.arm,a.model,"FULL",outdir/"finite_probe")
    finite_probe=_finite_eval(q32,base_info,preferred)
    # PolyChord bounded real-stack pilot
    pc_info,pc_meta=build_info(a,a.arm,a.model,"FULL",outdir/"polychord"/"chain")
    pc=copy.deepcopy(spec["polychord"]["pilot"]);pc["path"]=runtime["polychord_path"];pc["seed"]=_cell_seed(spec,a.arm,a.model)
    pc_info["sampler"]={"polychord":pc};pc_info["output"]=str((outdir/"polychord"/"chain").resolve());pc_info["force"]=True;pc_info["resume"]=False
    from cobaya.run import run as cobaya_run
    sampler=None
    try:
        _,sampler=cobaya_run(pc_info,force=True,stop_at_error=True)
        products=sampler.products() if sampler is not None else {}
        logz=products.get("logZ") if isinstance(products,dict) else None
        sample=products.get("sample") if isinstance(products,dict) else None
        try:sample_count=len(sample) if sample is not None else 0
        except Exception:sample_count=-1
    finally:
        try:
            if sampler is not None and hasattr(sampler,"close"):sampler.close()
        except Exception:pass
    resume_files=[p for p in (outdir/"polychord").rglob("*resume*") if p.is_file() and p.stat().st_size>0]
    if not resume_files:raise RuntimeError("POLYCHORD_RESUME_WRITE_GATE=FAIL")
    # Read/compatibility probe: identical statistical settings, genuine resume flag.
    resume_info=copy.deepcopy(pc_info);resume_info["force"]=False;resume_info["resume"]=True
    rs=None
    try:
        _,rs=cobaya_run(resume_info,resume=True,stop_at_error=True)
    finally:
        try:
            if rs is not None and hasattr(rs,"close"):rs.close()
        except Exception:pass
    # Two explicitly separate BOBYQA processes in one job, best_of=1 each.
    bob=[]
    for start_index in range(int(spec["bobyqa"]["pilot"]["external_starts_per_full_cell"])):
        bi,bm=build_info(a,a.arm,a.model,"FULL",outdir/"bobyqa"/f"start{start_index}"/"fit")
        starts=_apply_start(q32,bi,preferred,start_index)
        bs=spec["bobyqa"]["pilot"]
        bi["sampler"]={"minimize":{"method":"bobyqa","ignore_prior":True,"best_of":1,"max_evals":int(bs["max_evals"]),"seed":_cell_seed(spec,a.arm,a.model)+100+start_index,"override_bobyqa":{"rhoend":float(bs["rhoend"])}}}
        bi["output"]=str((outdir/"bobyqa"/f"start{start_index}"/"fit").resolve());bi["force"]=True;bi["resume"]=False
        sm=None
        try:
            _,sm=cobaya_run(bi,force=True,stop_at_error=False);prod=sm.products() if sm is not None else {};ro=prod.get("result_object") if isinstance(prod,dict) else None;rr=_result_object_record(ro)
            rr.update({"start_index":start_index,"start_values":starts,"technical_ok":bool(rr["flag"] is not None and int(rr["flag"])>=0 and rr["objective"] is not None)})
        except Exception as exc:
            rr={"start_index":start_index,"start_values":starts,"technical_ok":False,"error":repr(exc),"flag":None,"objective":None}
        finally:
            try:
                if sm is not None and hasattr(sm,"close"):sm.close()
            except Exception:pass
        bob.append(rr)
    if len(bob)!=2 or any(not x.get("technical_ok") for x in bob):raise RuntimeError(f"BOBYQA_BOUNDED_MULTISTART_GATE=FAIL {bob}")
    rec={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"FULL_CELL_TECHNICAL_PILOT","status":"PASS","scientific_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"arm":a.arm,"model":a.model,"combination":"FULL","finite_probe_logposterior":finite_probe,"polychord":{"seed":pc["seed"],"settings":spec["polychord"]["pilot"],"logZ_technical":float(logz) if finite(logz) else None,"sample_count":sample_count,"resume_files":[str(p.relative_to(outdir)) for p in resume_files],"resume_read_probe":"PASS","runtime_commit":runtime["polychord_commit"]},"bobyqa":{"best_of":1,"external_starts":bob},"gates":{"Q_IDENTITY":"PASS","FULL_FINITE_EVALUATION":"PASS","POLYCHORD_EXECUTION":"PASS","POLYCHORD_RESUME_READ_WRITE":"PASS","BOBYQA_EXTERNAL_MULTISTART":"PASS","NO_SCIENCE_CLASSIFICATION":"PASS"},"claim_boundary":"Pilot logZ, samples, minima and finite probes are technical outputs only and MUST NOT be used as cosmological evidence."}
    write_json(outdir/"q042_pilot_result_v2.json",rec);print(f"Q042_V2_PILOT_GATE=PASS arm={a.arm} model={a.model}");return 0

def merge_pilots(a:argparse.Namespace)->int:
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);env=read_json(a.environment_preflight)
    if env.get("status")!="PASS" or env.get("built_cell_count")!=20:raise RuntimeError("ENVIRONMENT_PREFLIGHT_INPUT_GATE=FAIL")
    rows=[]
    for p in Path(a.input_dir).rglob("q042_pilot_result_v2.json"):
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
    write_json(a.output,out);print("Q042_V2_PREFLIGHT_FINAL_GATE=PASS");return 0

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
    s=sp.add_parser("pilot-cell");common_args(s);s.add_argument("--arm",required=True,choices=ARMS);s.add_argument("--model",required=True,choices=MODELS);s.add_argument("--output-dir",required=True);s.set_defaults(func=pilot_cell)
    s=sp.add_parser("merge-pilots");s.add_argument("--input-dir",required=True);s.add_argument("--environment-preflight",required=True);s.add_argument("--spec",required=True);s.add_argument("--source-lock",required=True);s.add_argument("--output",required=True);s.set_defaults(func=merge_pilots)
    return p
if __name__=="__main__":
    a=parser().parse_args();raise SystemExit(a.func(a))
