"""Q052-NATIVEPAIR-V2 controller.

Builds one new intervention wrapper against the immutable original classy.so.
No copied hydrogen-rate implementation is accepted. The C layer changes only
the z=810 branch event/orchestration and calls the pinned source routines.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, os, platform, shutil, subprocess, sys, sysconfig, time

HERE=Path(__file__).resolve().parent
Q="Q052"; ID="Q052-NATIVEPAIR-V2"
CONTRACT="Q052_NATIVEPAIR_CONTRACT_V2.json"
LOCK="Q047_COLLECTION_LOCK_V1.json"
CACHE_BINARY="df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf"

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def read(p): return json.loads(Path(p).read_text())
def write(p,o):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
def need(x,msg):
    if not x: raise ValueError(msg)

def package_gate():
    c=read(HERE/CONTRACT)
    need(c["q"]==Q and c["program_id"]==ID,"CONTRACT_ID")
    need(c["source_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97","SOURCE")
    need(c["native_intervention"]["reionization"]["tau_shooting"] is False,"TAU_SHOOT")
    need(c["native_intervention"]["event_redshift"]==810.0,"EVENT")
    for f in ["q052_native_pair_v2.c","q052_native_pair_v2.py","test_q052_native_pair_v2.py",
              "q052_program_registry_patch_v2.json",".github/workflows/q052-native-pair-v2.yml"]:
        need((HERE/f).is_file(),"MISSING "+f)
    return c


def repository_lineage_gate(c):
    lineage={
      "q048_prefix_config_v1.json":c["frozen_lineage"]["q048_capture_sha256"],
      "Q050_CLEAN_BG_BINDING_V1.json":c["frozen_lineage"]["q050_background_binding_sha256"],
      "Q048_V151_ACCEPTED_CHECKPOINT_V1.json":c["frozen_lineage"]["q048_z810_checkpoint_sha256"],
      "Q047_COLLECTION_LOCK_V1.json":c["frozen_lineage"]["q047_collection_lock_sha256"],
    }
    for name,digest in lineage.items():
        need((HERE/name).is_file() and sha(HERE/name)==digest,"FROZEN_LINEAGE "+name)
    return lineage

def source_gate(source,c):
    commit=subprocess.check_output(["git","-C",str(source),"rev-parse","HEAD"],text=True).strip()
    need(commit==c["source_commit"],"CLASS_COMMIT "+commit)
    for rel,d in c["source_hashes"].items():
        need(sha(source/rel)==d,"SOURCE_HASH "+rel)
    import q047_execution_v1 as acquire
    binary=acquire.identify_binary(source,c["class_binary_sha256"])
    need(sha(binary)==CACHE_BINARY,"BINARY_HASH")
    return binary

def fixed_parameters():
    lock=read(HERE/LOCK)
    need(sha(HERE/LOCK)=="4b64c2b4724ae5ee1fed8c099625a33653ef6ac8d3f3ada0cfa7fcdeec1f6b7a","LOCK_HASH")
    case=lock["cases"]["hillipop-ede_n3"]
    p=dict(case["class_parameters"])
    accepted=float(case["accepted_z_reio"])
    need(accepted==float.fromhex("0x1.dfec4p+2"),"ZREIO_ID")
    p.pop("tau_reio",None)
    p["z_reio"]=format(accepted,".17g")
    return p

def ini(path):
    p=fixed_parameters()
    Path(path).write_text("".join(f"{k} = {v}\n" for k,v in p.items()))
    return p

def compile_wrapper(source,binary,out):
    libdir=sysconfig.get_config_var("LIBDIR"); ldlib=sysconfig.get_config_var("LDLIBRARY")
    need(libdir and ldlib and ldlib.startswith("libpython") and ".so" in ldlib,"PYTHON_LINK")
    exe=out/"q052_native_pair_v2"
    cmd=["gcc","-O2","-std=c99","-fopenmp","-rdynamic","-fno-fast-math","-ffp-contract=off"]
    cmd += ["-I"+str(source/p) for p in ["include","external/HyRec2020","external/heating","external/RecfastCLASS"]]
    cmd += [str(HERE/"q052_native_pair_v2.c"),str(binary),"-L"+libdir,"-l"+ldlib[3:].split(".so")[0],
            "-Wl,-rpath,"+str(binary.parent),"-Wl,-rpath,"+libdir,"-ldl","-lm","-o",str(exe)]
    with (out/"compile.log").open("w") as log:
        subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
    return exe,cmd

def parse_history(p):
    with Path(p).open(newline="") as f:
        rows=list(csv.DictReader(f))
    need(rows,"EMPTY_HISTORY")
    for r in rows:
        for k in r: 
            if k!="": float(r[k])
    return rows

def validate_worker(out,arm,mode,c):
    start=read(out/"z810_start.json"); ident=read(out/"effective_identity.json"); runtime=read(out/"runtime_result.json")
    rows=parse_history(out/"history.csv")
    need(start["arm"]==arm and start["mode"]==mode,"START_ID")
    need(float.fromhex(start["z"])==810.0 and float.fromhex(start["mz"])==-810.0,"START_Z")
    need(start["phase"]==start["index_ap_frec"] and start["require_H"]==1 and start["require_He_pre"]==1,"START_PHASE")
    q=1e-6 if arm=="L" else 0.0
    need(float.fromhex(start["q_xHeII_post"])==q,"Q_VALUE")
    v=float.fromhex(start["Tmat_over_Trad"])
    need(-1e-6 <= v-1 <= 0.02,"Q051_THERMAL_START_DOMAIN")
    h=float.fromhex(start["x_H"]); need(0<=h<=0.99999,"Q051_H_START_DOMAIN")
    need(ident["solve_interposed"] and ident["start_written"],"INTERPOSITION")
    need(float.fromhex(ident["z_reio"])==float.fromhex(c["native_intervention"]["reionization"]["z_reio_hex"]),"FIXED_ZREIO")
    capture=read(HERE/"q048_prefix_config_v1.json")["cases"]["hillipop-ede_n3"]["background"]["fields"]
    for k in ("H0","K","Omega0_b","Omega0_cdm","Omega0_g","Omega0_lambda","Omega0_ur","T_cmb"):
        need(ident["fields"][k]==capture[k],"EFFECTIVE_BACKGROUND_CAPTURE "+k)
    need(runtime["execution_status"]=="COMPLETE","RUNTIME")
    need(rows[0]["z"]=="0" or abs(float(rows[0]["z"]))<1e-14,"Z0")
    need(float(rows[-1]["z"])<=810.0+1e-12,"ZMAX")
    return {"start":start,"identity":ident,"runtime":runtime,"rows":rows}

def worker(arm,mode,directory):
    need(platform.python_version()=="3.11.16", "FROZEN_PYTHON_REQUIRED 3.11.16 actual="+platform.python_version())
    c=package_gate()
    repository_lineage_gate(c)
    need(arm in ("L","R") and mode in ("nominal","refined"),"JOB")
    out=Path(directory).resolve();out.mkdir(parents=True,exist_ok=False)
    source=HERE/"external/class_ede"
    binary=source_gate(source,c)
    point=out/"point.ini"; params=ini(point)
    exe,cmd=compile_wrapper(source,binary,out)
    env=dict(os.environ,Q052_NATIVE_OUT=str(out),Q052_ARM=arm,Q052_MODE=mode,
             Q052_RUN_ID=os.environ.get("GITHUB_RUN_ID","LOCAL"),
             OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
    t=time.monotonic()
    with (out/"native.log").open("w") as log:
        cp=subprocess.run([str(exe),str(point)],cwd=HERE,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
    elapsed=time.monotonic()-t
    need(cp.returncode==0,"NATIVE_EXIT "+str(cp.returncode))
    v=validate_worker(out,arm,mode,c)
    artifacts={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}
    result={"schema":"BV-Q052-WORKER-1.0.0","q":Q,"program_id":ID,"arm":arm,"mode":mode,
            "execution_status":"COMPLETE","source_commit":c["source_commit"],"binary_sha256":sha(binary),
            "point_sha256":sha(point),"compile_command":cmd,"elapsed_seconds":elapsed,
            "python":platform.python_version(),"execution_commit":os.environ.get("GITHUB_SHA","LOCAL_NOT_INSTALLED"),
            "start":v["start"],"effective_identity":v["identity"],"rows":len(v["rows"]),"artifacts":artifacts}
    write(out/"worker_result.json",result)
    return result

def common_grid(a,b):
    need(len(a)==len(b),"GRID_LENGTH")
    for x,y in zip(a,b):
        need(x["z"]==y["z"] and x["eta_Mpc"]==y["eta_Mpc"],"GRID_IDENTITY")

def diff_series(a,b,key):
    return [float(x[key])-float(y[key]) for x,y in zip(a,b)]

def supabs(x): return max(abs(v) for v in x) if x else 0.0

def load_job(root,arm,mode):
    matches=list(Path(root).rglob(f"{arm}-{mode}/worker_result.json"))
    need(len(matches)==1,f"JOB_COUNT {arm}-{mode} {len(matches)}")
    d=matches[0].parent; wr=read(matches[0])
    need(wr["arm"]==arm and wr["mode"]==mode and wr["execution_status"]=="COMPLETE","WORKER_ID")
    for name,digest in wr["artifacts"].items():
        p=d/name;need(p.is_file() and sha(p)==digest,"ARTIFACT "+name)
    return wr,read(d/"z810_start.json"),read(d/"effective_identity.json"),parse_history(d/"history.csv")

def collect(directory,output):
    c=package_gate()
    jobs={}
    for arm in ("L","R"):
        for mode in ("nominal","refined"):
            jobs[(arm,mode)]=load_job(directory,arm,mode)
    for mode in ("nominal","refined"):
        L=jobs[("L",mode)];R=jobs[("R",mode)]
        for k in ("D_Tmat_K","x_H","Tgamma_K","Tmat_over_Trad"):
            need(L[1][k]==R[1][k],"MATCHED_Z810_"+mode+"_"+k)
        need(L[2]["fields"]==R[2]["fields"],"BACKGROUND_IDENTITY_"+mode)
        common_grid(L[3],R[3])
    # Background is numerical-identical across precision levels too; only thermodynamics tolerance changes.
    need(jobs[("L","nominal")][2]["fields"]==jobs[("L","refined")][2]["fields"],"BACKGROUND_LEVEL_IDENTITY")
    common_grid(jobs[("L","nominal")][3],jobs[("R","nominal")][3])
    common_grid(jobs[("L","refined")][3],jobs[("R","refined")][3])

    Ln,Rn=jobs[("L","nominal")][3],jobs[("R","nominal")][3]
    Lr,Rr=jobs[("L","refined")][3],jobs[("R","refined")][3]
    dxn=diff_series(Ln,Rn,"xe"); dtn=diff_series(Ln,Rn,"cumulative_tau_T")
    dxr=diff_series(Lr,Rr,"xe"); dtr=diff_series(Lr,Rr,"cumulative_tau_T")
    common_grid(Ln,Lr);common_grid(Rn,Rr)
    refinement_dx=supabs([a-b for a,b in zip(dxn,dxr)])
    refinement_dt=supabs([a-b for a,b in zip(dtn,dtr)])
    sup_dx=supabs(dxn);sup_dt=supabs(dtn)
    bx=c["q051_envelopes"]["sup_abs_delta_x_e_max"];bt=c["q051_envelopes"]["sup_abs_delta_tau_T_max_strict"]
    within=(sup_dx<=bx and sup_dt<bt)
    result={
      "schema":"BV-Q052-NATIVEPAIR-RESULT-1.0.0","q":Q,"program_id":ID,
      "execution_status":"COMPLETE","job_completeness_gate":"PASS","merge_compatibility_gate":"PASS",
      "start_state_pair_gate":"PASS","background_identity_gate":"PASS",
      "actual_computed_result":{
        "representation":"native CLASS output grid plus exact z=810 intervention state",
        "sup_abs_delta_x_e_on_native_grid":sup_dx,
        "sup_abs_delta_tau_T_on_native_grid":sup_dt,
        "q051_envelope_comparison":{"x_e_bound":bx,"tau_bound":bt,"within_both_on_native_grid":within}
      },
      "numerical_validation":{
        "nominal_vs_refined_pair_discrepancy_x_e":refinement_dx,
        "nominal_vs_refined_pair_discrepancy_tau_T":refinement_dt,
        "certificate_scope":"OBSERVED_REFINEMENT_DISCREPANCY_AND_INDEPENDENT_SERIALIZED_READBACK",
        "rigorous_truncation_error_bound":False,
        "status":"PROVISIONAL_NOT_A_RIGOROUS_ERROR_THEOREM"
      },
      "result_validation_status":"PROVISIONAL",
      "scientific_outcome":"NOT_FINAL_UNTIL_NUMERICAL_ERROR_CERTIFICATE_SCOPE_IS_ACCEPTED_OR_STRENGTHENED",
      "final_result_gate":"UNRESOLVED",
      "first_remaining_blocker":"RIGOROUS_NATIVE_NUMERICAL_ERROR_CERTIFICATE_NOT_ESTABLISHED_BY_TWO_LEVEL_REFINEMENT_ALONE",
      "return_route":c["return_route"]
    }
    write(output,result);return result

def static():
    c=package_gate()
    repository_lineage_gate(c)
    src=(HERE/"q052_native_pair_v2.c").read_text()
    for token in ["thermodynamics_solve","Q052_MZ_EVENT","evolver_ndf15","thermodynamics_derivs","Q052_TAU_SHOOTING_FORBIDDEN"]:
        need(token in src,"C_SEMANTIC "+token)
    wf=(HERE/".github/workflows/q052-native-pair-v2.yml").read_text()
    for token in ["Q052-NATIVEPAIR-V2","q052_recover_native_v2.py","matrix:","nominal","refined","collect"]:
        need(token in wf,"WORKFLOW "+token)
    return {"package_gate":"PASS","science_freeze_gate":"PASS","static_semantics_gate":"PASS",
            "program_id_registry_gate":"PENDING_INSTALL","launcher_gate":"PENDING_INSTALL"}

def persist_failure(output, error, stage, arm=None, mode=None, error_log=None):
    report={"schema":"BV-Q052-FAILURE-2.0.0","q":Q,"program_id":ID,
      "run_id":os.environ.get("GITHUB_RUN_ID","LOCAL"),
      "run_attempt":os.environ.get("GITHUB_RUN_ATTEMPT","LOCAL"),
      "execution_commit":os.environ.get("GITHUB_SHA","LOCAL_NOT_INSTALLED"),
      "stage":stage,"arm":arm,"mode":mode,
      "execution_status":"BLOCKED_OR_FAILED","error":str(error),
      "actual_computed_result":None,"scientific_falsification":False,
      "result_validation_status":"NOT_RUN","scientific_outcome":"NOT_ASSESSED",
      "final_result_gate":"UNRESOLVED","return_route":"BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0"}
    if error_log and Path(error_log).is_file():
        report["original_error_log"]={"path":str(error_log),"sha256":sha(error_log)}
        report["original_error_text"]=Path(error_log).read_text(errors="replace")
    write(output,report)
    return report

def main():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    sp.add_parser("static")
    w=sp.add_parser("worker");w.add_argument("--arm",required=True,choices=["L","R"]);w.add_argument("--mode",required=True,choices=["nominal","refined"]);w.add_argument("--directory",required=True)
    c=sp.add_parser("collect");c.add_argument("--directory",required=True);c.add_argument("--output",default="Q052_NATIVEPAIR_RESULT_V2.json")
    f=sp.add_parser("failure")
    f.add_argument("--output",required=True);f.add_argument("--stage",required=True)
    f.add_argument("--error",required=True);f.add_argument("--arm");f.add_argument("--mode");f.add_argument("--log")
    a=p.parse_args()
    try:
        if a.cmd=="failure":
            print(json.dumps(persist_failure(a.output,a.error,a.stage,a.arm,a.mode,a.log),indent=2));return 2
        if a.cmd=="static": out=static()
        elif a.cmd=="worker": out=worker(a.arm,a.mode,a.directory)
        else: out=collect(a.directory,a.output)
        print(json.dumps(out,indent=2,allow_nan=False));return 0
    except Exception as e:
        output=getattr(a,"output",None)
        if not output:
            directory=getattr(a,"directory",None)
            output=str(Path(directory)/"failure.json") if directory else "Q052_STATIC_RESULT_V2.json"
        report=persist_failure(output,f"{type(e).__name__}: {e}",a.cmd,
                               getattr(a,"arm",None),getattr(a,"mode",None))
        print(json.dumps(report,indent=2));return 2

if __name__=="__main__": raise SystemExit(main())
