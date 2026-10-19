"""One immutable V90 execution, after metadata/tests/import preflight; stop first failure."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,time,json,traceback
from q048_v90_proof_contract import ROOT,SPEC,RAW,load,sha,output,validate_spec,require

def stamp():return datetime.now(timezone.utc).isoformat()
def command(args,timeout=30):
 start=time.monotonic();beg=stamp()
 try:
  p=subprocess.run([sys.executable,'-B']+args,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
  return {'command':[sys.executable,'-B']+args,'cwd':str(ROOT),'start_utc':beg,'end_utc':stamp(),'elapsed_seconds':time.monotonic()-start,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 except subprocess.TimeoutExpired as e:
  return {'command':[sys.executable,'-B']+args,'cwd':str(ROOT),'start_utc':beg,'end_utc':stamp(),'elapsed_seconds':time.monotonic()-start,'exit_code':'TIMEOUT','stdout':str(e.stdout or ''),'stderr':str(e.stderr or '')}
def main():
 require(Path.cwd()==ROOT,'FINAL_CWD_REQUIRED')
 require(not (ROOT/'q048_moving_h_domain_freeze_v90.json').exists() and not (ROOT/RAW).exists(),'IMMUTABLE_IDENTITY_ALREADY_USED')
 s=load(ROOT/SPEC);checks=validate_spec(s)
 for rel in s['code_pins']:compile((ROOT/rel).read_text(),rel,'exec')
 logs=[]
 for args in [['-m','unittest','discover','-v'],['q048_moving_h_domain_verify_v90.py','--preflight'],['q048_moving_h_domain_accept_v90.py','--preflight'],['q048_v90_import_probe.py']]:
  logs.append(command(args));require(logs[-1]['exit_code']==0,'PREFLIGHT_FAILED:'+str(args))
 require(not (ROOT/RAW).exists(),'PREFLIGHT_SCIENCE_OUTPUT_FORBIDDEN')
 pre={'status':'PASS','kind':'METADATA_TOY_TESTS_AND_ACTUAL_IMPORT_ONLY','metadata_checks':len(checks),'checks':checks,'commands':logs,'spec_sha256':sha(ROOT/SPEC),'scientific_producer_calls':0,'source_expected_calls':0,'timestamp_utc':stamp()}
 output('q048_moving_h_domain_preflight_v90.json',pre)
 validate_spec(s);spec_hash=sha(ROOT/SPEC)
 output('q048_moving_h_domain_freeze_v90.json',{'schema_version':'Q048_MOVING_H_DOMAIN_FREEZE_V90','preflight_status':'PASS','spec_sha256':spec_hash,'execution_fingerprint':s['execution_fingerprint'],'preflight_sha256':sha(ROOT/'q048_moving_h_domain_preflight_v90.json'),'frozen_utc':stamp(),'max_new_proof_cells':1,'max_new_actual_cells':0,'science_budget_seconds':300})
 start=time.monotonic();stages=[];status='FAIL';failure=None
 try:
  for name in ['q048_moving_h_domain_v90.py','q048_moving_h_domain_verify_v90.py','q048_moving_h_domain_accept_v90.py']:
   remaining=300-(time.monotonic()-start);require(remaining>0,'SCIENCE_BUDGET_EXHAUSTED')
   log=command([name],remaining);stages.append(log)
   require(log['exit_code']==0,'FIRST_STAGE_FAILURE:'+name)
   require(sha(ROOT/SPEC)==spec_hash,'FROZEN_SPEC_CHANGED');validate_spec(s)
   require(time.monotonic()-start<=300,'SCIENCE_BUDGET_EXHAUSTED_AFTER_STAGE')
  status='PASS_ONE_ACCEPTED_PROOF_STOP'
 except Exception as e:failure=type(e).__name__+':'+str(e)
 elapsed=time.monotonic()-start
 output('q048_moving_h_domain_execution_v90.json',{'status':status,'failure':failure,'spec_sha256':spec_hash,'execution_fingerprint':s['execution_fingerprint'],'stages':stages,'elapsed_seconds':elapsed,'budget_seconds':300,'producer_invocations':sum(z['command'][-1]=='q048_moving_h_domain_v90.py' for z in stages),'actual_consumer_invocations':0,'stop_reason':'ONE_ACCEPTED_PROOF' if status.startswith('PASS') else 'FIRST_PRECISE_OBSTRUCTION','actual_unchanged':{'count':106,'frontier':1020},'end_utc':stamp(),'postfreeze_edits':False,'retries':0})
 print(json.dumps({'status':status,'failure':failure,'elapsed_seconds':elapsed,'stages':[{'command':z['command'][-1],'exit_code':z['exit_code'],'stdout':z['stdout']} for z in stages]},indent=2))
 if failure:raise SystemExit(1)
if __name__=='__main__':main()
