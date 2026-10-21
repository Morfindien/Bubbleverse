import subprocess,sys,time,datetime,json
from q048_v144_contract import *
steps=[('q048_v144_consumer.py','Q048_V144_RAW_V1.json'),('q048_v144_validate.py','Q048_V144_VALIDATION_V1.json'),('q048_v144_accept.py','Q048_V144_PROVISIONAL_ACCEPTANCE_V1.json'),('q048_v144_postaccept.py','Q048_V144_POSTACCEPT_VALIDATION_V1.json'),('q048_v144_publish.py','Q048_V144_PUBLICATION_READBACK_V1.json')]
start=time.perf_counter(); events=[]; obstruction=None
for script,outfile in steps:
 t=time.perf_counter(); p=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True); sec=time.perf_counter()-t
 ev={'script':script,'returncode':p.returncode,'seconds':sec,'stdout':p.stdout,'stderr':p.stderr,'output':outfile,'output_sha256':sha(ROOT/outfile) if (ROOT/outfile).exists() else None}; events.append(ev)
 if p.returncode!=0: obstruction={'script':script,'returncode':p.returncode,'stderr':p.stderr}; break
frozen=verify_freeze(); total=time.perf_counter()-start
status='PASS' if obstruction is None and all(frozen.values()) and total<=300 else 'FAIL'
out={'schema':'bubbleverse.q048.v144.execution.v1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'run_id':load(ROOT/'Q048_V144_RUN_CONTEXT_V1.json')['run_id'],'events':events,'first_obstruction':obstruction,'seconds':total,'budget_seconds':300,'chains':1,'retry_count':0,'postfreeze_edits':0,'frozen_files_reverified':len(frozen),'frozen_files_unchanged':sum(frozen.values()),'freeze_all_unchanged':all(frozen.values())}
dump(ROOT/'Q048_V144_EXECUTION_V1.json',out)
if status!='PASS': raise SystemExit(6)
