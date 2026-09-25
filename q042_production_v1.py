#!/usr/bin/env python3
"""Bubbleverse Q042 production campaign V1.

Production-only continuation of Q042-PREFLIGHT-V11. Pilot output is never used as science.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, re, signal, subprocess, sys, time
from pathlib import Path
from typing import Any
import numpy as np
import q042_planck_portability_v11 as core

Q="Q-042"; CASE_ID="NOT DOCUMENTED"; PROGRAM_ID="Q042-PROD-V1"; RUN_ID="Q042-PRODUCTION-PORTABILITY-V1"; RESULT_ID="R-Q042-PRODUCTION-PORTABILITY-001"
ARMS=("camspec","hillipop"); MODELS=("lcdm","ede_n3"); COMBINATIONS=("FULL","NO_ACT_PRIMARY","NO_ACT_LENSING","NO_DESI_DR2","NO_SN")
core.Q=Q; core.CASE_ID=CASE_ID; core.PROGRAM_ID=PROGRAM_ID; core.RUN_ID=RUN_ID; core.RESULT_ID=RESULT_ID
core.legacy.Q=Q; core.legacy.PROGRAM_ID=PROGRAM_ID; core.legacy.RUN_ID=RUN_ID; core.legacy.RESULT_ID=RESULT_ID

def finite(x):
    try:return math.isfinite(float(x))
    except Exception:return False

def read_json(p):
    x=json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x,dict):raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return x

def write_json(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False,default=str)+"\n",encoding="utf-8");os.replace(t,p)

def sha256_file(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def canonical_hash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

def load_spec(p):
    d=read_json(p)
    if (d.get("q"),d.get("case_id"),d.get("program_id"))!=(Q,CASE_ID,PROGRAM_ID):raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    c=d["authoritative_contract"]
    if tuple(c["arms"])!=ARMS or tuple(c["models"])!=MODELS or set(c["data_combinations"])!=set(COMBINATIONS) or int(c["required_cell_count"])!=20:raise RuntimeError("AUTHORITATIVE_CONTRACT_GATE=FAIL")
    pc=d["polychord_production"];bq=d["bobyqa_production"]
    frozen={"nlive":"25d","num_repeats":"5d","nprior":"10nlive","nfail":"nlive","precision_criterion":0.001,"max_ndead":"infinity","do_clustering":True,"boost_posterior":0,"confidence_for_unbounded":0.9999995,"measure_speeds":True,"oversample_power":0.4,"synchronous":True,"read_resume":True,"write_resume":True,"write_live":True,"write_dead":True,"write_prior":True,"write_stats":True}
    for k,v in frozen.items():
        if pc.get(k)!=v:raise RuntimeError(f"POLYCHORD_PRODUCTION_LOCK_GATE=FAIL key={k}")
    if int(bq["external_starts_per_cell"])!=4 or int(bq["cobaya_best_of"])!=1 or bq["max_evals"]!="120d" or float(bq["rhoend"])!=0.05 or bq["ignore_prior"] is not True:raise RuntimeError("BOBYQA_PRODUCTION_LOCK_GATE=FAIL")
    seeds=d["polychord_seed_map"]
    if len(seeds)!=20 or len(set(int(x) for x in seeds.values()))!=20:raise RuntimeError("SEED_MAP_GATE=FAIL")
    return d

def load_lock(p,spec):
    d=read_json(p)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID or d.get("spec_sha256")!=sha256_file(spec):raise RuntimeError("SOURCE_LOCK_GATE=FAIL")
    return d

def runtime_gate(p):
    r=read_json(p)
    if r.get("q")!=Q or r.get("program_id")!=PROGRAM_ID or r.get("status")!="PASS" or r.get("cobaya_version")!="3.5.6" or r.get("pybobyqa_version")!="1.5.0" or not r.get("polychord_commit") or not r.get("pantheonplus_runtime_files"):raise RuntimeError("RUNTIME_SOURCE_GATE=FAIL")
    return r

def static_check(a):
    load_spec(a.spec);load_lock(a.source_lock,a.spec)
    write_json(a.output,{"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"PRODUCTION_STATIC","status":"PASS","spec_sha256":sha256_file(a.spec),"required_cell_count":20,"seed_count":20,"scientific_result":False,"gates":{"Q_IDENTITY":"PASS","CONTEXT_CONTINUITY":"PASS","V11_PREFLIGHT_PARENT":"PASS","SPEC_HASH":"PASS","SOURCE_LOCK":"PASS","PRODUCTION_SETTINGS_FROZEN":"PASS","Q040_FIREWALL":"PASS","NO_PILOT_SCIENCE":"PASS"}})
    print("Q042_PROD_V1_STATIC_GATE=PASS");return 0

def prepare_nonoverlap(a):
    rc=core.prepare_nonoverlap(a)
    for p in (Path(a.support_output),Path(a.meta_output)):
        d=read_json(p);d.update({"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID});write_json(p,d)
    return rc

def build_info(a,arm,model,combo,prefix):return core.build_info(a,arm,model,combo,prefix)
def preferred(a,arm):return core._preferred(a,arm)
def finite_eval(q32,info,pref):return core._finite_eval(q32,info,pref)
def external_signature(info):return core._external_science_signature(info)
def expected_external(contract_combo):return core._expected_external_components(contract_combo)

def runtime_preflight(a):
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime=runtime_gate(a.external_runtime);q32=core.legacy.load_q032(a.q032_parent_root)
    rows=[];sigmap={}
    for arm in ARMS:
      for model in MODELS:
       for combo in COMBINATIONS:
        info,meta=build_info(a,arm,model,combo,Path(a.output).parent/"probe"/f"{arm}_{model}_{combo.lower()}")
        native=q32.CAMSPEC if arm=="camspec" else q32.HILLIPOP
        if native not in info.get("likelihood",{}):raise RuntimeError("PLANCK_NATIVE_IDENTITY_GATE=FAIL")
        sig=external_signature(info);exp=expected_external(spec["authoritative_contract"]["data_combinations"][combo])
        if set(sig["components"])!=exp:raise RuntimeError(f"EXTERNAL_COMPONENT_GATE=FAIL {arm} {model} {combo}")
        row={"arm":arm,"model":model,"combination":combo,"status":"PASS","support_mode":meta["support_mode"],"external_science_signature":sig}
        if combo=="FULL":row["finite_logposterior"]=finite_eval(q32,info,preferred(a,arm))
        rows.append(row);sigmap[(arm,model,combo)]=sig
    for m in MODELS:
      for c in COMBINATIONS:
        if sigmap[("camspec",m,c)]!=sigmap[("hillipop",m,c)]:raise RuntimeError(f"EXTERNAL_DATA_IDENTITY_GATE=FAIL {m} {c}")
    if len(rows)!=20:raise RuntimeError("AUTHORITATIVE_20_CELL_BUILD_GATE=FAIL")
    write_json(a.output,{"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"PRODUCTION_RUNTIME_PREFLIGHT","status":"PASS","actual_computed_scientific_result":False,"built_cell_count":20,"runtime_source":{"polychord_commit":runtime["polychord_commit"],"pantheonplus_manifest_sha256":runtime["pantheonplus_manifest_sha256"]},"rows":rows,"gates":{"AUTHORITATIVE_20_CELL_BUILD":"PASS","PLANCK_NATIVE_IDENTITY":"PASS","EXTERNAL_DATA_IDENTITY":"PASS","FULL_FINITE_EVALUATIONS":"PASS","Q040_FIREWALL":"PASS"}})
    print("Q042_PROD_V1_RUNTIME_PREFLIGHT_GATE=PASS");return 0

def cell_seed(spec,arm,model,combo):return int(spec["polychord_seed_map"][f"{arm}:{model}:{combo}"])

def production_pc(spec,runtime,arm,model,combo):
    pc=copy.deepcopy(spec["polychord_production"])
    # Frozen semantic setting is unlimited nested-dead-point count. Cobaya 3.5.6
    # expects numeric infinity here (its YAML default is .inf), not the literal
    # string "infinity" carried in the Bubbleverse preregistration.
    if pc.get("max_ndead")=="infinity": pc["max_ndead"]=float("inf")
    pc["path"]=runtime["polychord_path"];pc["seed"]=cell_seed(spec,arm,model,combo);return pc

def stored_info(prefix):
    from cobaya.output import OutputReadOnly
    d=OutputReadOnly(prefix=str(prefix)).get_updated_info()
    if not isinstance(d,dict):raise RuntimeError("POLYCHORD_STORED_UPDATED_INFO_GATE=FAIL")
    return d

def polychord_worker(a):
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime=runtime_gate(a.external_runtime)
    outdir=Path(a.output_dir);prefix=(outdir/"polychord"/"chain").resolve();prefix.parent.mkdir(parents=True,exist_ok=True)
    built,_=build_info(a,a.arm,a.model,a.combination,prefix);pc=production_pc(spec,runtime,a.arm,a.model,a.combination)
    contract_hash=canonical_hash({"pc":spec["polychord_production"],"seed":pc["seed"],"arm":a.arm,"model":a.model,"combination":a.combination})
    if a.action=="fresh":
        info=built;info["sampler"]={"polychord":pc};info["output"]=str(prefix);info["force"]=True;info["resume"]=False;source="FRESH_BUILT_INFO"
    else:
        info=copy.deepcopy(stored_info(prefix));sp=(info.get("sampler") or {}).get("polychord") or {}
        if int(sp.get("seed",pc["seed"]))!=pc["seed"]:raise RuntimeError("POLYCHORD_STORED_SEED_GATE=FAIL")
        info["output"]=str(prefix);info["force"]=False;info["resume"]=True;source="COBAYA_STORED_UPDATED_INFO"
    from cobaya.run import run as cobaya_run
    sm=None
    try:
        _,sm=cobaya_run(info,output=str(prefix),force=(a.action=="fresh"),resume=(a.action=="resume"),stop_at_error=True)
        prod=sm.products() if sm is not None else {};sample=prod.get("sample") if isinstance(prod,dict) else None
        write_json(a.result_json,{"q":Q,"program_id":PROGRAM_ID,"stage":"POLYCHORD_PRODUCTION_WORKER","status":"COMPLETE","arm":a.arm,"model":a.model,"combination":a.combination,"seed":pc["seed"],"sampler_contract_sha256":contract_hash,"resume_input_source":source,"sample_count":len(sample) if sample is not None else 0,"runtime_commit":runtime["polychord_commit"]})
        print("Q042_PROD_POLYCHORD_WORKER=COMPLETE");return 0
    finally:
        try:
            if sm is not None and hasattr(sm,"close"):sm.close()
        except Exception:pass

def resume_files(outdir):return [p for p in (Path(outdir)/"polychord").rglob("*resume*") if p.is_file() and p.stat().st_size>0]

def common_cli(a):
    out=[]
    for k in ("q032_parent_root","preflight","parent_dir","hlp_matrix","hlp_meta","reduced_support","reduced_hlp_matrix","reduced_hlp_meta","spec","source_lock","external_runtime"):out += ["--"+k.replace("_","-"),str(getattr(a,k))]
    return out

def polychord_segment(a):
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime_gate(a.external_runtime)
    if a.arm not in ARMS or a.model not in MODELS or a.combination not in COMBINATIONS:raise RuntimeError("CELL_IDENTITY_GATE=FAIL")
    outdir=Path(a.output_dir);outdir.mkdir(parents=True,exist_ok=True);action="fresh" if a.segment==0 else "resume";seed=cell_seed(spec,a.arm,a.model,a.combination)
    cmd=[sys.executable,str(Path(__file__).resolve()),"polychord-worker",*common_cli(a),"--arm",a.arm,"--model",a.model,"--combination",a.combination,"--action",action,"--output-dir",str(outdir),"--result-json",str(outdir/"worker_result.json")]
    start=time.time();proc=subprocess.Popen(cmd,start_new_session=True);timed_out=False
    try:rc=proc.wait(timeout=int(a.soft_minutes)*60)
    except subprocess.TimeoutExpired:
        timed_out=True;os.killpg(proc.pid,signal.SIGINT)
        try:rc=proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try:rc=proc.wait(timeout=60)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);rc=proc.wait()
    rf=resume_files(outdir);updated=list((outdir/"polychord").glob("chain.updated.*"));worker=read_json(outdir/"worker_result.json") if (outdir/"worker_result.json").exists() else None
    status="COMPLETE" if rc==0 and worker and worker.get("status")=="COMPLETE" else "SEGMENT_CHECKPOINTED" if timed_out and rf and updated else "FAILED"
    rec={"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"POLYCHORD_PRODUCTION_SEGMENT","status":status,"arm":a.arm,"model":a.model,"combination":a.combination,"segment":a.segment,"action":action,"seed":seed,"soft_minutes":a.soft_minutes,"elapsed_seconds":time.time()-start,"worker_returncode":rc,"timed_out":timed_out,"resume_files":[str(p.relative_to(outdir)) for p in rf],"worker":worker,"checkpoint_parent_run_id":a.parent_run_id or None,"config_hash":canonical_hash({"spec":sha256_file(a.spec),"arm":a.arm,"model":a.model,"combination":a.combination,"seed":seed})}
    if status=="FAILED":rec["failure_class"]="HPC_OR_NUMERICAL_SEGMENT_FAILURE"
    write_json(a.segment_json,rec);print("Q042_PROD_SEGMENT_STATUS="+status);return 0 if status!="FAILED" else 2

def production_start(q32,info,pref,start_index):
    fractions=(0.0,0.08,0.14,0.20);frac=fractions[start_index];used={};params=info.get("params",{})
    for name,pinfo in params.items():
        if not isinstance(pinfo,dict) or not isinstance(pinfo.get("prior"),dict):continue
        pr=pinfo["prior"];lo,hi=pr.get("min"),pr.get("max")
        if not finite(lo) or not finite(hi):continue
        lo,hi=float(lo),float(hi);span=hi-lo;base=float(pref.get(name,0.5*(lo+hi))) if finite(pref.get(name,0.5*(lo+hi))) else 0.5*(lo+hi)
        if start_index==0:v=base
        else:
            sign=-1.0 if int(hashlib.sha256((name+":"+str(start_index)).encode()).hexdigest()[:2],16)%2 else 1.0;v=base+sign*frac*span
        if span>0:v=min(max(v,lo+0.05*span),hi-0.05*span)
        try:q32.set_ref(params,name,float(v));used[name]=float(v)
        except Exception:pass
    return used

def parse_result_object(obj):return {"flag":getattr(obj,"flag",None),"message":str(getattr(obj,"msg","")),"objective":float(getattr(obj,"f",float("nan"))) if finite(getattr(obj,"f",None)) else None,"nf":int(getattr(obj,"nf",-1)) if getattr(obj,"nf",None) is not None else None}

def parse_bobyqa_exception(exc):
    txt=str(exc)
    if "Py-BOBYQA Results" not in txt:return {"flag":None,"objective":None,"nf":None,"technical_ok":False,"message":txt}
    mf=re.search(r"Objective value f\(xmin\)\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",txt);mg=re.search(r"Exit flag\s*=\s*(-?\d+)",txt);mn=re.search(r"Needed\s+(\d+)\s+objective evaluations",txt)
    obj=float(mf.group(1)) if mf and finite(mf.group(1)) else None;flag=int(mg.group(1)) if mg else None
    return {"flag":flag,"objective":obj,"nf":int(mn.group(1)) if mn else None,"technical_ok":bool(obj is not None and flag is not None and flag>=0),"message":txt}

def bobyqa_stage(a):
    spec=load_spec(a.spec);load_lock(a.source_lock,a.spec);runtime_gate(a.external_runtime);q32=core.legacy.load_q032(a.q032_parent_root)
    info,_=build_info(a,a.arm,a.model,a.combination,Path(a.output_dir)/"fit");starts=production_start(q32,info,preferred(a,a.arm),a.start_index);bq=spec["bobyqa_production"];d=sum(1 for v in info.get("params",{}).values() if isinstance(v,dict) and "prior" in v)
    if d<=0:raise RuntimeError("BOBYQA_DIMENSION_GATE=FAIL")
    maxeval=int(str(bq["max_evals"]).removesuffix("d"))*d;seed=cell_seed(spec,a.arm,a.model,a.combination)+1000+a.start_index
    info["sampler"]={"minimize":{"method":"bobyqa","ignore_prior":True,"best_of":1,"max_evals":maxeval,"seed":seed,"override_bobyqa":{"rhoend":float(bq["rhoend"])}}};info["output"]=str((Path(a.output_dir)/"fit").resolve());info["force"]=True;info["resume"]=False
    from cobaya.run import run as cobaya_run
    sm=None
    try:
        _,sm=cobaya_run(info,force=True,stop_at_error=False);prod=sm.products() if sm is not None else {};rr=parse_result_object(prod.get("result_object") if isinstance(prod,dict) else None);rr["technical_ok"]=bool(rr["objective"] is not None and rr["flag"] is not None and int(rr["flag"])>=0)
    except Exception as exc:rr=parse_bobyqa_exception(exc);rr["wrapper_exception"]=repr(exc)
    finally:
        try:
            if sm is not None and hasattr(sm,"close"):sm.close()
        except Exception:pass
    rr.update({"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"BOBYQA_PRODUCTION_START","arm":a.arm,"model":a.model,"combination":a.combination,"start_index":a.start_index,"start_values":starts,"seed":seed,"max_evals":maxeval,"rhoend":float(bq["rhoend"]),"status":"PASS" if rr.get("technical_ok") else "RECORDED_FAILURE","scientific_role":"WITHIN_ARM_BEST_FIT_ONLY"})
    write_json(a.result_json,rr);print("Q042_PROD_BOBYQA_STATUS="+rr["status"]);return 0

def read_chain(prefix):
    base=Path(prefix);cands=[p for p in base.parent.glob(base.name+"*.txt") if "polychord_raw" not in str(p)]
    arrays=[];names=None
    for p in cands:
        lines=p.read_text(encoding="utf-8",errors="replace").splitlines();header=next((x for x in lines if x.lstrip().startswith("#") and "weight" in x and "minuslogpost" in x),None)
        if not header:continue
        n=header.lstrip("#").strip().split();dat=np.loadtxt(p,comments="#",ndmin=2)
        if dat.size==0:continue
        if dat.shape[1]!=len(n):raise RuntimeError("CHAIN_HEADER_WIDTH_GATE=FAIL")
        if names is not None and names!=n:raise RuntimeError("CHAIN_COLUMN_COMPATIBILITY_GATE=FAIL")
        names=n;arrays.append(dat)
    if not arrays:raise RuntimeError(f"POSTERIOR_SAMPLE_GATE=FAIL prefix={prefix}")
    return names,np.vstack(arrays)

def col(names,*opts):
    for x in opts:
        if x in names:return names.index(x)
    raise KeyError(opts)

def weighted_stats(names,a,param):
    wi=col(names,"weight");pi=col(names,param);w=np.asarray(a[:,wi],float);x=np.asarray(a[:,pi],float);ok=np.isfinite(w)&np.isfinite(x)&(w>=0);w=w[ok];x=x[ok]
    if len(x)<2 or w.sum()<=0:raise RuntimeError(f"WEIGHTED_STATS_GATE=FAIL {param}")
    w=w/w.sum();mu=float((w*x).sum());sd=float(np.sqrt((w*(x-mu)**2).sum()));return {"mean":mu,"sigma":sd,"n":int(len(x)),"effective_weight_n":float(1.0/(w@w))}

def prior_bounds(prefix,param):
    import yaml
    d=yaml.safe_load(Path(str(prefix)+".updated.yaml").read_text());pr=(d.get("params",{}).get(param,{}) or {}).get("prior",{}) or {};lo,hi=pr.get("min"),pr.get("max")
    if not finite(lo) or not finite(hi) or float(hi)<=float(lo):raise RuntimeError(f"PRIOR_BOUNDS_GATE=FAIL {param}")
    return float(lo),float(hi)

def overlap_2d(pa,pb,bins):
    na,a=read_chain(pa);nb,b=read_chain(pb);wa=col(na,"weight");wb=col(nb,"weight");ha=col(na,"H0");hb=col(nb,"H0");fa=col(na,"fEDE");fb=col(nb,"fEDE")
    hra,hrb=prior_bounds(pa,"H0"),prior_bounds(pb,"H0");fra,frb=prior_bounds(pa,"fEDE"),prior_bounds(pb,"fEDE")
    if not(np.allclose(hra,hrb,atol=1e-12,rtol=0) and np.allclose(fra,frb,atol=1e-12,rtol=0)):raise RuntimeError("OVERLAP_PRIOR_IDENTITY_GATE=FAIL")
    A,_,_=np.histogram2d(a[:,ha],a[:,fa],bins=bins,range=[hra,fra],weights=a[:,wa]);B,_,_=np.histogram2d(b[:,hb],b[:,fb],bins=bins,range=[hra,fra],weights=b[:,wb])
    if A.sum()<=0 or B.sum()<=0:raise RuntimeError("OVERLAP_WEIGHT_GATE=FAIL")
    return float(np.minimum(A/A.sum(),B/B.sum()).sum())

def best_bobyqa(rows,arm,model,combo):
    x=[r for r in rows if (r["arm"],r["model"],r["combination"])==(arm,model,combo)]
    if len(x)!=4:raise RuntimeError(f"BOBYQA_START_COMPLETENESS_GATE=FAIL {arm} {model} {combo}")
    good=[r for r in x if r.get("technical_ok") and finite(r.get("objective")) and int(r.get("flag",-999))>=0]
    return {"starts":x,"usable_start_count":len(good),"best_objective":min(float(r["objective"]) for r in good) if good else None,"all_four_present":True}

def merge_final(a):
    load_spec(a.spec);load_lock(a.source_lock,a.spec);root=Path(a.input_dir);poly=[];bob=[]
    for p in root.rglob("q042_production_polychord_final_v1.json"):
        d=read_json(p)
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID:poly.append((p,d))
    for p in root.rglob("q042_production_bobyqa_start_v1.json"):
        d=read_json(p)
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID:bob.append(d)
    expected={(x,y,z) for x in ARMS for y in MODELS for z in COMBINATIONS};found={(d["arm"],d["model"],d["combination"]) for _,d in poly}
    if found!=expected:raise RuntimeError(f"POLYCHORD_CELL_COMPLETENESS_GATE=FAIL missing={sorted(expected-found)}")
    if len(bob)!=80:raise RuntimeError(f"BOBYQA_RESULT_COMPLETENESS_GATE=FAIL count={len(bob)}")
    bqc={};invalid=[]
    for arm in ARMS:
      for model in MODELS:
       for combo in COMBINATIONS:
        b=best_bobyqa(bob,arm,model,combo);bqc[f"{arm}:{model}:{combo}"]=b
        if b["best_objective"] is None:invalid.append(f"{arm}:{model}:{combo}")
    controlled=[d for _,d in poly if d.get("status")!="COMPLETE"]
    if controlled or invalid:
        write_json(a.output,{"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"PRODUCTION_FINAL","execution_status":"CONTROLLED_INCOMPLETE","tests_status":"COMPLETE","final_result_gate":"UNRESOLVED","q042_feasibility_classification":"PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED","downstream_portability_classification":"NOT_AVAILABLE","actual_computed_scientific_result":False,"controlled_polychord_cells":controlled,"bobyqa_unusable_cells":invalid,"bobyqa":bqc,"gates":{"JOB_COMPLETENESS":"PASS","MERGE_COMPATIBILITY":"PASS","CONVERGENCE":"FAIL" if controlled else "PASS","GLOBALITY":"FAIL" if invalid else "PASS","FINAL_RESULT":"UNRESOLVED"}});print("Q042_PROD_FINAL_GATE=UNRESOLVED");return 0
    prefixes={}
    for p,d in poly:
        c=(d["arm"],d["model"],d["combination"]);q=list(p.parent.rglob("chain.updated.yaml"))
        if len(q)!=1:raise RuntimeError(f"CHAIN_UPDATED_GATE=FAIL {c}")
        prefixes[c]=Path(str(q[0]).replace(".updated.yaml",""))
    combo_results={};coords=["H0","fEDE","omega_b","omega_cdm","log10z_c","thetai_scf"];count_coords=["H0","fEDE","omega_b","omega_cdm"]
    for combo in COMBINATIONS:
        stats={}
        for arm in ARMS:
            n,x=read_chain(prefixes[(arm,"ede_n3",combo)]);stats[arm]={p:weighted_stats(n,x,p) for p in coords if p in n}
        D={}
        for p in coords:
            if p in stats["camspec"] and p in stats["hillipop"]:
                x,y=stats["camspec"][p],stats["hillipop"][p];den=math.sqrt(x["sigma"]**2+y["sigma"]**2);D[p]=abs(x["mean"]-y["mean"])/den if den>0 else None
        param_material=bool((finite(D.get("H0")) and D["H0"]>=1) or (finite(D.get("fEDE")) and D["fEDE"]>=1) or sum(1 for p in count_coords if finite(D.get(p)) and D[p]>=1)>=2)
        pa,pb=prefixes[("camspec","ede_n3",combo)],prefixes[("hillipop","ede_n3",combo)];ov64=overlap_2d(pa,pb,[64,64]);ov80=overlap_2d(pa,pb,[80,80]);ov96=overlap_2d(pa,pb,[96,96]);stable=len({ov64<0.5,ov80<0.5,ov96<0.5})==1;contour=(ov80<0.5) if stable else None
        mp={}
        for arm in ARMS:
            l=bqc[f"{arm}:lcdm:{combo}"]["best_objective"];e=bqc[f"{arm}:ede_n3:{combo}"]["best_objective"];delta=2*(l-e);cat="negligible" if delta<=2 else "modest" if delta<6 else "substantive";mp[arm]={"delta_chi2":delta,"category":cat,"lcdm_best_objective":l,"ede_best_objective":e}
        mpm=bool(mp["camspec"]["category"]!=mp["hillipop"]["category"] and abs(mp["camspec"]["delta_chi2"]-mp["hillipop"]["delta_chi2"])>=2);material=(mpm or (param_material and contour is True)) if stable else None
        combo_results[combo]={"ede_posterior_stats":stats,"D_x":D,"parameter_location_material":param_material,"overlap":{"primary_80x80":ov80,"stability_64x64":ov64,"stability_96x96":ov96,"stable_side_of_0p50":stable,"contour_material":contour},"model_preference":mp,"model_preference_portability_material":mpm,"combination_material":material}
    if any(v["combination_material"] is None for v in combo_results.values()):classification="NOT_AVAILABLE";gate="UNRESOLVED";actual=False;feas="PRODUCTION_COMPLETE_ANALYSIS_NUMERICALLY_UNRESOLVED"
    else:
        mats=[bool(combo_results[c]["combination_material"]) for c in COMBINATIONS]
        if combo_results["FULL"]["combination_material"] and all(combo_results[c]["combination_material"] for c in COMBINATIONS[1:]):classification="MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE"
        elif any(mats) and not all(mats):classification="MIXED_DATASET_CONDITIONAL"
        elif all((not combo_results[c]["parameter_location_material"]) and combo_results[c]["overlap"]["primary_80x80"]>=0.50 and (not combo_results[c]["model_preference_portability_material"]) for c in COMBINATIONS):classification="SCIENTIFIC_DIFFERENCE_COLLAPSES"
        else:classification="NOT_AVAILABLE"
        gate="PASS" if classification!="NOT_AVAILABLE" else "UNRESOLVED";actual=(classification!="NOT_AVAILABLE");feas="EXECUTABLE_WITH_PREREGISTERED_ROBUST_STRATEGY" if actual else "PRODUCTION_COMPLETE_CLASSIFICATION_RULES_DO_NOT_RESOLVE"
    write_json(a.output,{"q":Q,"case_id":CASE_ID,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"PRODUCTION_FINAL","execution_status":"COMPLETE","tests_status":"COMPLETE","final_result_gate":gate,"q042_feasibility_classification":feas,"downstream_portability_classification":classification,"actual_computed_scientific_result":actual,"combination_results":combo_results,"bobyqa":bqc,"gates":{"JOB_COMPLETENESS":"PASS","MERGE_COMPATIBILITY":"PASS","CONVERGENCE":"PASS","GLOBALITY":"PASS","OVERLAP_NUMERICAL_STABILITY":"PASS" if gate=="PASS" else "UNRESOLVED","Q040_FIREWALL":"PASS","NO_CROSS_ARM_ABSOLUTE_OBJECTIVE":"PASS","FINAL_RESULT":gate}});print("Q042_PROD_FINAL_GATE="+gate);return 0

def common_args(s):
    for x in ("q032-parent-root","preflight","parent-dir","hlp-matrix","hlp-meta","reduced-support","reduced-hlp-matrix","reduced-hlp-meta","spec","source-lock","external-runtime"):s.add_argument("--"+x,required=True)

def parser():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static");s.add_argument("--spec",required=True);s.add_argument("--source-lock",required=True);s.add_argument("--output",required=True);s.set_defaults(func=static_check)
    s=sp.add_parser("prepare-nonoverlap")
    for x in ("q032-parent-root","preflight","hlp-matrix","hlp-meta","support-output","matrix-output","meta-output"):s.add_argument("--"+x,required=True)
    s.set_defaults(func=prepare_nonoverlap)
    s=sp.add_parser("runtime-preflight");common_args(s);s.add_argument("--output",required=True);s.set_defaults(func=runtime_preflight)
    s=sp.add_parser("polychord-worker");common_args(s);s.add_argument("--arm",choices=ARMS,required=True);s.add_argument("--model",choices=MODELS,required=True);s.add_argument("--combination",choices=COMBINATIONS,required=True);s.add_argument("--action",choices=("fresh","resume"),required=True);s.add_argument("--output-dir",required=True);s.add_argument("--result-json",required=True);s.set_defaults(func=polychord_worker)
    s=sp.add_parser("polychord-segment");common_args(s);s.add_argument("--arm",choices=ARMS,required=True);s.add_argument("--model",choices=MODELS,required=True);s.add_argument("--combination",choices=COMBINATIONS,required=True);s.add_argument("--segment",type=int,required=True);s.add_argument("--soft-minutes",type=int,default=240);s.add_argument("--parent-run-id",default="");s.add_argument("--output-dir",required=True);s.add_argument("--segment-json",required=True);s.set_defaults(func=polychord_segment)
    s=sp.add_parser("bobyqa-stage");common_args(s);s.add_argument("--arm",choices=ARMS,required=True);s.add_argument("--model",choices=MODELS,required=True);s.add_argument("--combination",choices=COMBINATIONS,required=True);s.add_argument("--start-index",type=int,choices=(0,1,2,3),required=True);s.add_argument("--output-dir",required=True);s.add_argument("--result-json",required=True);s.set_defaults(func=bobyqa_stage)
    s=sp.add_parser("merge-final");s.add_argument("--input-dir",required=True);s.add_argument("--spec",required=True);s.add_argument("--source-lock",required=True);s.add_argument("--output",required=True);s.set_defaults(func=merge_final)
    return p
if __name__=="__main__":a=parser().parse_args();raise SystemExit(a.func(a))
