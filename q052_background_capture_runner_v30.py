#!/usr/bin/env python3
"""One read-only pinned background dump. Run only in the existing GitHub native environment."""
import hashlib, importlib.util, json, os, platform, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run():
 if platform.python_version()!="3.11.16":raise RuntimeError("FROZEN_PYTHON")
 v3=mod("q052_v3",ROOT/"q052_validated_diag_v3.py")
 c=v3.package_gate()
 base,bc,source,binary,generated=v3.source_and_base_gate(c)
 generated_path=ROOT/"q052_v3_generated_for_v30.c"
 generated_path.write_text(generated)
 try:
  patched_path=ROOT/"q052_v30_patched.c"
  subprocess.run(["python",str(ROOT/"q052_background_dump_v30.py"),"--source",str(generated_path),"--output",str(patched_path)],check=True)
  patched=patched_path.read_text()
 finally:
  generated_path.unlink(missing_ok=True)
 out=ROOT/"q052_background_dump_v30"
 out.mkdir(exist_ok=False)
 point=out/"point.ini";base.ini(point)
 exe,cmd=v3.compile_wrapper(source,binary,out,patched)
 env=dict(os.environ,Q052_NATIVE_OUT=str(out),Q052_ARM="L",Q052_MODE="nominal",Q052_RUN_ID=os.environ.get("GITHUB_RUN_ID","LOCAL"),OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
 t=time.monotonic()
 with (out/"native.log").open("w") as log:
  cp=subprocess.run([str(exe),str(point)],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
 if cp.returncode:raise RuntimeError(f"NATIVE_EXIT {cp.returncode}")
 p=out/"background_table_hex.jsonl"
 with p.open() as f:
  meta=json.loads(next(f)); rows=[json.loads(line) for line in f]
 if len(rows)!=meta["bt_size"]:raise RuntimeError("TABLE_LENGTH")
 if not all(len(r["background"])==len(r["d2background_dloga2"])==meta["bg_size"] for r in rows):raise RuntimeError("TABLE_WIDTH")
 if not all(rows[i]["i"]==i for i in range(len(rows))):raise RuntimeError("TABLE_INDEX")
 z=[float.fromhex(r["z"]) for r in rows]
 loga=[float.fromhex(r["loga"]) for r in rows]
 if not all(loga[i]<loga[i+1] and z[i]>z[i+1] for i in range(len(rows)-1)):raise RuntimeError("TABLE_ORDER")
 if not z[0]>=810>=809.185>=z[-1]:raise RuntimeError("TABLE_DOMAIN")
 result={"schema":"Q052_BACKGROUND_DUMP_RESULT_V30","status":"RAW_NATIVE_TABLE_CAPTURED_NOT_ERROR_CERTIFICATE","run_id":meta["run_id"],"source_commit":c["source_commit"],"class_binary_sha256":digest(binary),"point_sha256":digest(point),"generated_C_sha256":digest(patched_path),"table_sha256":digest(p),"bt_size":meta["bt_size"],"bg_size":meta["bg_size"],"domain_z":[z[0],z[-1]],"required_two_cells_covered":True,"elapsed_seconds":time.monotonic()-t,"scientific_gate":"UNRESOLVED","compile_command":cmd}
 (out/"Q052_BACKGROUND_DUMP_RESULT_V30.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
if __name__=="__main__":run()
