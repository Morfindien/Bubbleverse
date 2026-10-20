from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,sys,subprocess
P='Q048_V122_LOW_Z_DISPATCH_DIAGNOSTIC_';R=Path(__file__).resolve().parent
S=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 fr=json.loads((R/(P+'FREEZE_V1.json')).read_bytes())
 if S(R/(P+'SPEC_V1.json'))!=fr['spec_sha256']:raise ValueError('SPEC_PIN')
 for n,h in fr['code_hashes'].items():
  if S(R/n)!=h:raise ValueError('CODE_PIN:'+n)
 for n,p in fr['input_pins'].items():
  if S(R/n)!=p['sha256']:raise ValueError('INPUT_PIN:'+n)
 if (R/(P+'RAW_V1.json')).exists():raise ValueError('DUPLICATE_EXECUTION')
 start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();phases=[]
 for n in ['q048_v122_diagnostic.py','q048_v122_verify.py','q048_v122_accept.py']:
  tic=time.monotonic();r=subprocess.run([sys.executable,str(R/n)],capture_output=True,text=True,timeout=min(60,max(.001,300-(time.monotonic()-clock))))
  phases.append({'command':[sys.executable,n],'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'wall_seconds':time.monotonic()-tic,'code_sha256':S(R/n)})
  if r.returncode:break
 ok=len(phases)==3 and all(x['returncode']==0 for x in phases)
 out={'schema':'bubbleverse.q048.v122.low_z_dispatch_diagnostic.execution.v1','status':'COMPLETE' if ok else 'FAILED','start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'phases':phases,'diagnostic_producer_invocations':1,'historical_program_main_invocations':0,'new_actual_cells':0,'new_proof_cells':0,'new_full_connected_theorems':0,'source_interval_evaluations':0,'science_budget_seconds':300,'retry_count':0,'postfreeze_edits':False,'spec_sha256':fr['spec_sha256'],'freeze_sha256':S(R/(P+'FREEZE_V1.json'))}
 with (R/(P+'EXECUTION_V1.json')).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps(out,indent=2))
 if not ok:raise SystemExit(1)
if __name__=='__main__':main()
