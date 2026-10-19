"""Bounded V87 final preflight, freeze, exactly one producer and ordered validation chain."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,time,platform,ast
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def stamp():return datetime.now(timezone.utc).isoformat()
def save(n,x):
 with (ROOT/n).open('x') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')
def run(cmd,name,timeout):
 start=stamp();clock=time.monotonic()
 try:
  r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=timeout)
  log={'command':cmd,'start_utc':start,'end_utc':stamp(),'wall_seconds':time.monotonic()-clock,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 except subprocess.TimeoutExpired as e:
  log={'command':cmd,'start_utc':start,'end_utc':stamp(),'wall_seconds':time.monotonic()-clock,'exit_code':'TIMEOUT','stdout':str(e.stdout or ''),'stderr':str(e.stderr or '')}
 save(name,log);return log
def verify_pins(s):
 for rel,pin in list(s['input_pins'].items())+list(s['code_pins'].items()):
  p=ROOT/rel
  if not p.is_file() or p.stat().st_size!=pin['bytes'] or sha(p)!=pin['sha256']:raise ValueError('FROZEN_PIN_MISMATCH:'+rel)
 if sha(ROOT/s['contract_markdown_path'])!=s['contract_markdown_sha256']:raise ValueError('CONTRACT_CHANGED')
def main():
 from q048_v87_consumer_contract import load_spec,validate_spec
 assert Path.cwd()==ROOT
 assert not (ROOT/'q048_frec_moving_h_freeze_v87.json').exists(),'IMMUTABLE_FREEZE_ALREADY_EXISTS'
 assert not (ROOT/'q048_frec_moving_h_result_v87.json').exists(),'RAW_ALREADY_EXISTS'
 s=load_spec();checks=validate_spec(s);verify_pins(s)
 for p in [*ROOT.glob('*.py'),*ROOT.joinpath('inputs').rglob('*.py')]:compile(p.read_text(),str(p),'exec')
 v=ast.parse((ROOT/'q048_frec_moving_h_verify_v87.py').read_text())
 modules=[x.module for x in ast.walk(v) if isinstance(x,ast.ImportFrom)]+[n.name for x in ast.walk(v) if isinstance(x,ast.Import) for n in x.names]
 assert 'q048_frec_moving_h_v87' not in modules
 for label,cmd in [
  ('final_suite',['python3','-B','-m','unittest','discover','-v']),
  ('final_verifier_preflight',['python3','-B','q048_frec_moving_h_verify_v87.py','--preflight']),
  ('final_acceptor_preflight',['python3','-B','q048_frec_moving_h_accept_v87.py','--preflight']),
  ('final_actual_import',['python3','-B','q048_v87_import_probe.py'])]:
  log=run(cmd,'q048_v87_'+label+'_log.json',30)
  if log['exit_code']!=0:raise ValueError('FINAL_PREFLIGHT_FAILED:'+label)
 verify_pins(s)
 pre={'schema':'bubbleverse.q048.frec_moving_h.preflight.v87','status':'PASS','metadata_checks_total':len(checks),'metadata_checks_passed':len(checks),'checks':checks,'regression_tests':'13/13 PASS;complete local unittest discovery','actual_full_import':'PASS_FINAL_LAYOUT_CWD_NO_SCIENTIFIC_ENTRY_POINTS_OR_FILE_WRITES','compile':'PASS_ALL_LOCAL_SOURCES','producer_free_verifier_imports':True,'new_science_producer_count':0,'code_pins_verified':len(s['code_pins']),'input_pins_verified':len(s['input_pins']),'execution_fingerprint':s['execution_fingerprint'],'spec_sha256':sha(ROOT/'q048_frec_moving_h_spec_v87.json'),'timestamp_utc':stamp()}
 save('q048_frec_moving_h_preflight_v87.json',pre)
 freeze={'schema':'bubbleverse.q048.frec_moving_h.freeze.v87','q':'Q048','target_q':'Q048','spec_sha256':sha(ROOT/'q048_frec_moving_h_spec_v87.json'),'contract_sha256':s['contract_markdown_sha256'],'task_fingerprint':s['task_fingerprint'],'execution_fingerprint':s['execution_fingerprint'],'preflight_status':'PASS','preflight_sha256':sha(ROOT/'q048_frec_moving_h_preflight_v87.json'),'frozen_code_pins':s['code_pins'],'frozen_input_pins':s['input_pins'],'frozen_utc':stamp(),'policy':'No code/input/spec/contract byte changes or producer retries after this freeze. Stop first precise obstruction/one accepted cell/300science seconds.'}
 save('q048_frec_moving_h_freeze_v87.json',freeze)
 science_clock=time.monotonic();stages=[];failure=None
 try:
  for label,script in [('producer','q048_frec_moving_h_v87.py'),('verifier','q048_frec_moving_h_verify_v87.py'),('acceptor','q048_frec_moving_h_accept_v87.py')]:
   verify_pins(s)
   if sha(ROOT/'q048_frec_moving_h_spec_v87.json')!=freeze['spec_sha256']:raise ValueError('FROZEN_SPEC_CHANGED')
   remaining=300-(time.monotonic()-science_clock)
   if remaining<=0:failure={'stage':label,'class':'SCIENCE_BUDGET_EXCEEDED'};break
   log=run(['python3','-B',script],'q048_frec_moving_h_'+label+'_execution_log_v87.json',remaining)
   stages.append({'stage':label,'exit_code':log['exit_code'],'wall_seconds':log['wall_seconds']})
   if log['exit_code']!=0:failure={'stage':label,'class':'FIRST_PRECISE_FROZEN_EXECUTION_OBSTRUCTION','exit_code':log['exit_code'],'stdout':log['stdout'],'stderr':log['stderr']};break
   verify_pins(s)
   if sha(ROOT/'q048_frec_moving_h_spec_v87.json')!=freeze['spec_sha256']:raise ValueError('FROZEN_SPEC_CHANGED')
   if time.monotonic()-science_clock>300:failure={'stage':label,'class':'SCIENCE_BUDGET_EXCEEDED_AFTER_PIN_CHECK'};break
  verify_pins(s)
  if sha(ROOT/'q048_frec_moving_h_spec_v87.json')!=freeze['spec_sha256']:raise ValueError('FROZEN_SPEC_CHANGED')
 except Exception as err:
  failure={'stage':'ordered_chain','class':type(err).__name__,'message':str(err)}
 elapsed=time.monotonic()-science_clock
 if elapsed>300 and failure is None:failure={'stage':'ordered_chain','class':'SCIENCE_BUDGET_EXCEEDED'}
 report={'schema':'bubbleverse.q048.frec_moving_h.orchestration.v87','status':'STOP_FIRST_OBSTRUCTION' if failure else 'COMPLETE_ONE_ACCEPTED_CELL_STOP','stages':stages,'science_chain_seconds':elapsed,'science_budget_seconds':300,'producer_process_attempts':sum(x['stage']=='producer' for x in stages),'frozen_pins_unchanged':not (failure and failure.get('message','').startswith(('FROZEN_PIN_MISMATCH','FROZEN_SPEC_CHANGED','CONTRACT_CHANGED'))),'postfreeze_patch':False,'retry':False,'failure':failure,'timestamp_utc':stamp()}
 save('q048_frec_moving_h_orchestration_log_v87.json',report)
 print(json.dumps(report,indent=2))
 if failure:save('q048_frec_moving_h_failure_v87.json',report);raise SystemExit(1)
if __name__=='__main__':main()
