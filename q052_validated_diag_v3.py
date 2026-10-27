#!/usr/bin/env python3
"""Controller/collector for Q052-VALIDATEDDIAG-V3.

One newly instrumented nominal L/R pair only. The target deliberately cannot
promote capture success to a source-real numerical certificate. It returns
PARTIAL plus the exact remaining validated-numerics obligations.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, math, os, platform, subprocess, sys, sysconfig, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
Q="Q052"; ID="Q052-VALIDATEDDIAG-V3"
CONTRACT="Q052_VALIDATED_DIAGNOSTICS_CONTRACT_V10.json"
V8="Q052_VALIDATED_NUMERICS_CONTRACT_V8.json"
BASE_PY="q052_native_pair_v2.py"
BUILDER="q052_build_validated_diag_v3.py"


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p): return json.loads(Path(p).read_text())
def write(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
def need(x,msg):
    if not x: raise ValueError(msg)
def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def package_gate():
    c=read(HERE/CONTRACT)
    need(c["q"]==Q and c["program_id"]==ID,"CONTRACT_ID")
    need(c["source_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97","SOURCE_COMMIT")
    need(c["class_binary_sha256"]=="df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf","BINARY")
    need(c["execution"]["modes"]==["nominal"] and c["execution"]["arms"]==["L","R"],"ONE_NOMINAL_PAIR_ONLY")
    need(c["scientific_result_gate"]=="FORCED_PARTIAL_UNTIL_VALIDATED_RESIDUAL_CERTIFICATE","NO_ACCIDENTAL_PASS")
    for f in [BASE_PY,"q052_native_pair_v2.c",BUILDER,CONTRACT,V8,"q052_recover_native_v2.py"]:
        need((HERE/f).is_file(),"MISSING "+f)
    return c

def base_module(): return loadmod("q052_v2_base",HERE/BASE_PY)
def builder_module(): return loadmod("q052_v3_builder",HERE/BUILDER)

def source_and_base_gate(c):
    base=base_module();bc=base.package_gate();base.repository_lineage_gate(bc)
    source=HERE/"external/class_ede";binary=base.source_gate(source,bc)
    builder=builder_module();src=builder.gate_base(HERE/"q052_native_pair_v2.c");patched=builder.patch_source(src)
    need('#define Q052_ID "Q052-VALIDATEDDIAG-V3"' in patched,"PATCH_ID")
    return base,bc,source,binary,patched

def compile_wrapper(source,binary,out,patched):
    cfile=out/"q052_validated_diag_v3.c";cfile.write_text(patched)
    libdir=sysconfig.get_config_var("LIBDIR");ldlib=sysconfig.get_config_var("LDLIBRARY")
    need(libdir and ldlib and ldlib.startswith("libpython") and ".so" in ldlib,"PYTHON_LINK")
    exe=out/"q052_validated_diag_v3"
    cmd=["gcc","-O2","-std=c99","-fopenmp","-rdynamic","-fno-fast-math","-ffp-contract=off"]
    cmd += ["-I"+str(source/p) for p in ["include","external/HyRec2020","external/heating","external/RecfastCLASS"]]
    cmd += [str(cfile),str(binary),"-L"+libdir,"-l"+ldlib[3:].split(".so")[0],"-Wl,-rpath,"+str(binary.parent),"-Wl,-rpath,"+libdir,"-ldl","-lm","-o",str(exe)]
    with (out/"compile.log").open("w") as log: subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
    return exe,cmd

def jsonl(p):
    rows=[]
    with Path(p).open() as f:
        for i,line in enumerate(f,1):
            if line.strip():
                try: rows.append(json.loads(line))
                except Exception as e: raise ValueError(f"JSONL {p} line {i}: {e}")
    return rows

def validate_diag(out,arm):
    man=read(out/"diagnostic_manifest.json")
    need(man["program_id"]==ID and man["arm"]==arm,"DIAG_ID")
    need(man["rhs_records"]>0 and man["output_records"]>0 and man["guard_records"]>0,"DIAG_COUNTS")
    state=jsonl(out/"fullstate_trace.jsonl"); event=jsonl(out/"event_phase_trace.jsonl"); guard=jsonl(out/"hyrec_guard_trace.jsonl")
    outputs=[r for r in state if r.get("tag")=="OUTPUT"]
    need(outputs,"NO_OUTPUT_STATE")
    zs=[float.fromhex(r["z"]) for r in outputs]
    need(min(zs)<=1e-12 and max(zs)<810.0,"OUTPUT_DOMAIN")
    pre=[r for r in event if r.get("tag")=="Z810_PRE_INTERVENTION"]
    post=[r for r in event if r.get("tag")=="Z810_POST_INTERVENTION"]
    need(len(pre)==1 and len(post)==1,"Z810_EVENT_COUNT")
    need(float.fromhex(pre[0]["z"])==810.0 and float.fromhex(post[0]["z"])==810.0,"Z810_EVENT_Z")
    need(any(r.get("model_observed") in (0,4) for r in guard),"HYREC_DISPATCH_NOT_OBSERVED")
    for r in state:
        need(r.get("background_snapshot_kind")=="workspace_after_original_callback","BACKGROUND_ROLE")
        need(len(r["y"])==r["ti_size"] and len(r["dy"])==r["ti_size"],"STATE_SIZE")
    return {"manifest":man,"state_records":len(state),"output_records":len(outputs),"event_records":len(event),"guard_records":len(guard),"output_z_min":min(zs),"output_z_max":max(zs)}

def worker(arm,directory):
    need(platform.python_version()=="3.11.16","FROZEN_PYTHON_REQUIRED 3.11.16 actual="+platform.python_version())
    c=package_gate();need(arm in ("L","R"),"ARM")
    base,bc,source,binary,patched=source_and_base_gate(c)
    out=Path(directory).resolve();out.mkdir(parents=True,exist_ok=False)
    point=out/"point.ini";base.ini(point)
    exe,cmd=compile_wrapper(source,binary,out,patched)
    env=dict(os.environ,Q052_NATIVE_OUT=str(out),Q052_ARM=arm,Q052_MODE="nominal",Q052_RUN_ID=os.environ.get("GITHUB_RUN_ID","LOCAL"),OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
    t=time.monotonic()
    with (out/"native.log").open("w") as log: cp=subprocess.run([str(exe),str(point)],cwd=HERE,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
    elapsed=time.monotonic()-t;need(cp.returncode==0,"NATIVE_EXIT "+str(cp.returncode))
    basev=base.validate_worker(out,arm,"nominal",bc);diag=validate_diag(out,arm)
    artifacts={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}
    wr={"schema":"BV-Q052-VALIDATEDDIAG-WORKER-1.0.0","q":Q,"program_id":ID,"arm":arm,"mode":"nominal","execution_status":"COMPLETE","scientific_status":"RAW_DIAGNOSTIC_NOT_CERTIFICATE","source_commit":c["source_commit"],"binary_sha256":sha(binary),"point_sha256":sha(point),"compile_command":cmd,"elapsed_seconds":elapsed,"python":platform.python_version(),"execution_commit":os.environ.get("GITHUB_SHA","LOCAL_NOT_INSTALLED"),"start":basev["start"],"effective_identity":basev["identity"],"history_rows":len(basev["rows"]),"diagnostic":diag,"artifacts":artifacts}
    write(out/"worker_result.json",wr);return wr

def find_job(root,arm):
    ms=list(Path(root).rglob(f"{arm}-nominal/worker_result.json"));need(len(ms)==1,f"JOB_COUNT {arm} {len(ms)}")
    d=ms[0].parent;wr=read(ms[0]);need(wr["program_id"]==ID and wr["arm"]==arm and wr["execution_status"]=="COMPLETE","WORKER_ID")
    for name,digest in wr["artifacts"].items(): need((d/name).is_file() and sha(d/name)==digest,"ARTIFACT "+name)
    return d,wr

def collect(directory,output):
    c=package_gate();base=base_module();jobs={}
    for arm in ("L","R"):
        d,wr=find_job(directory,arm);start=read(d/"z810_start.json");ident=read(d/"effective_identity.json");hist=base.parse_history(d/"history.csv");diag=validate_diag(d,arm);jobs[arm]=(d,wr,start,ident,hist,diag)
    L,R=jobs["L"],jobs["R"];base.common_grid(L[4],R[4])
    for k in ("D_Tmat_K","x_H","Tgamma_K","Tmat_over_Trad"): need(L[2][k]==R[2][k],"START_PAIR "+k)
    grid_x=base.supabs(base.diff_series(L[4],R[4],"xe"));grid_tau=base.supabs(base.diff_series(L[4],R[4],"cumulative_tau_T"))
    run=os.environ.get("GITHUB_RUN_ID","LOCAL")
    receipt={"schema":"Q052_NATIVE_DIAGNOSTIC_RUN_RECEIPT_V3","q":Q,"program_id":ID,"run_id":run,"execution_status":"COMPLETE","pair":"ONE_NEW_INSTRUMENTED_NOMINAL_LR","source_commit":c["source_commit"],"class_binary_sha256":c["class_binary_sha256"],"start_pair_gate":"PASS","background_parameter_identity_gate":"PASS_REUSED_V2_GATE_NOT_INTERVAL_MEMBERSHIP_CERTIFICATE","grid_sup_abs_delta_x_e":grid_x,"grid_sup_abs_delta_tau_T":grid_tau,"capture_gate":"PASS","scientific_result_gate":"PARTIAL","final_q052_gate":"UNRESOLVED"}
    trace={"schema":"Q052_FULLSTATE_TRACE_MANIFEST_V3","q":Q,"run_id":run,"representation":"raw JSONL fullstate/output callback records plus exact z810 boundary states; no claim that RHS calls are accepted solver steps","arms":{}}
    for arm,(d,wr,start,ident,hist,diag) in jobs.items():
        trace["arms"][arm]={"diagnostic":diag,"files":{n:sha(d/n) for n in ["fullstate_trace.jsonl","event_phase_trace.jsonl","hyrec_guard_trace.jsonl","diagnostic_manifest.json","z810_start.json","history.csv"]}}
    closure={"schema":"Q052_BACKGROUND_EVENT_CLOSURE_V3","q":Q,"run_id":run,"status":"PARTIAL_CAPTURE_ONLY","captured":["full active thermo vector at every original output callback","derivative vector supplied to each output callback","literal phase/require flags and phase limits","workspace x_H/x_He/x_noreio/x_reio/Tmat","normal background workspace vector at callbacks","exact z810 pre/post state","observed HyRec model/child-dispatch arguments"],"not_yet_certified":["whole-cell admitted-background tube/membership over every segment","Pion and threshold guard interval signs including equality slabs","validated source/table/libm arithmetic enclosure","event-boundary derivative/source evaluation without perturbing run state","whole-cell residual and tube closure","observable-map error and final tau kernel transfer"],"first_remaining_blocker":"LOCAL-Q052-VALIDATED-WHOLE-CELL-RESIDUAL-BACKGROUND-ARITHMETIC-ENGINE-MISSING-V10","physical_falsification":false}
    cert={"schema":"Q052_SOURCE_REAL_ERROR_CERTIFICATE_V3","q":Q,"run_id":run,"status":"UNRESOLVED_NOT_A_CERTIFICATE","reason":"Diagnostic capture supplies the missing raw state/dispatch/terminal-boundary evidence, but no validated interval residual/background/libm propagation has yet been executed. Capture success cannot be promoted to a source-real error theorem.","inherited_saved_interpolant_certificate":"Q052_SERIALIZED_INTERPOLANT_CERTIFICATE_V8.json","actual_grid_observation":{"sup_abs_delta_x_e":grid_x,"sup_abs_delta_tau_T":grid_tau},"full_0_to_810_source_real_certified":false,"within_q051_envelopes_source_real_certified":false,"next_exact_obligation":closure["first_remaining_blocker"]}
    for name,obj in [("LOCAL_Q052_NATIVE_DIAGNOSTIC_RUN_RECEIPT.json",receipt),("LOCAL_Q052_FULLSTATE_TRACE_MANIFEST.json",trace),("LOCAL_Q052_BACKGROUND_EVENT_CLOSURE.json",closure),("LOCAL_Q052_SOURCE_REAL_ERROR_CERTIFICATE.json",cert)]: write(name,obj)
    result={"schema":"BV-Q052-VALIDATEDDIAG-RESULT-1.0.0","q":Q,"program_id":ID,"execution_status":"COMPLETE","diagnostic_capture":"PASS","scientific_status":"PARTIAL","final_result_gate":"UNRESOLVED","first_remaining_blocker":closure["first_remaining_blocker"],"return_route":"BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0","artifacts":["LOCAL_Q052_NATIVE_DIAGNOSTIC_RUN_RECEIPT.json","LOCAL_Q052_FULLSTATE_TRACE_MANIFEST.json","LOCAL_Q052_BACKGROUND_EVENT_CLOSURE.json","LOCAL_Q052_SOURCE_REAL_ERROR_CERTIFICATE.json"]}
    write(output,result);return result

def static():
    c=package_gate();builder=builder_module();src=builder.gate_base(HERE/"q052_native_pair_v2.c");patched=builder.patch_source(src)
    forbidden=["tau_shoot","Filippov","selector smoothing"]
    need('Q052-VALIDATEDDIAG-V3' in patched,"ID")
    need('hyrec_guard_trace.jsonl' in patched and 'fullstate_trace.jsonl' in patched,"CAPTURE")
    need(c["execution"]["new_native_branch_cap"]==2,"CAP")
    return {"schema":"Q052_VALIDATEDDIAG_STATIC_V3","package_gate":"PASS","base_patch_gate":"PASS","abi_capture_design":"PASS_SOURCE_VERIFIED","compile_gate":"DEFERRED_TO_PINNED_GITHUB_ENVIRONMENT","native_dispatch":"NOT_PERFORMED","scientific_result_gate":"FORCED_PARTIAL"}

def persist_failure(output,error,stage,arm=None,log=None):
    o={"schema":"BV-Q052-VALIDATEDDIAG-FAILURE-1.0.0","q":Q,"program_id":ID,"run_id":os.environ.get("GITHUB_RUN_ID","LOCAL"),"stage":stage,"arm":arm,"error":error,"execution_status":"FAILED","scientific_status":"NO_NEW_RESULT","final_q052_gate":"UNRESOLVED"}
    if log and Path(log).is_file():o["log_tail"]=Path(log).read_text(errors='replace')[-12000:]
    Path(output).parent.mkdir(parents=True,exist_ok=True);write(output,o);return o

def main():
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('static')
    w=sp.add_parser('worker');w.add_argument('--arm',required=True);w.add_argument('--directory',required=True)
    c=sp.add_parser('collect');c.add_argument('--directory',required=True);c.add_argument('--output',default='Q052_VALIDATEDDIAG_RESULT_V3.json')
    f=sp.add_parser('failure');f.add_argument('--output',required=True);f.add_argument('--stage',required=True);f.add_argument('--arm');f.add_argument('--error',required=True);f.add_argument('--log')
    a=ap.parse_args()
    try:
        if a.cmd=='static':out=static()
        elif a.cmd=='worker':out=worker(a.arm,a.directory)
        elif a.cmd=='collect':out=collect(a.directory,a.output)
        else:out=persist_failure(a.output,a.error,a.stage,a.arm,a.log)
        print(json.dumps(out,indent=2,allow_nan=False));return 0 if a.cmd!='failure' else 2
    except Exception as e:
        output=getattr(a,'output',None) or (str(Path(getattr(a,'directory','.') or '.')/'failure.json'))
        report=persist_failure(output,f"{type(e).__name__}: {e}",a.cmd,getattr(a,'arm',None),getattr(a,'log',None));print(json.dumps(report,indent=2));return 2
if __name__=='__main__':raise SystemExit(main())
