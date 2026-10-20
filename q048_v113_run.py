"""Frozen one-shot V113 admission; no theorem producer or historical main."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent;P='Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    frozen=json.loads((R/(P+'FREEZE_V1.json')).read_bytes())
    if sha(R/(P+'SPEC_V1.json'))!=frozen['spec_sha256']:raise ValueError('FROZEN_SPEC')
    for collection in ['input_hashes','code_hashes']:
        for name,h in frozen[collection].items():
            path=(R/'inputs'/name) if collection=='input_hashes' else R/name
            if sha(path)!=h:raise ValueError('FROZEN_BYTE_PIN:'+name)
    if (R/(P+'RAW_V1.json')).exists():raise ValueError('Refusing existing raw result / duplicate execution')
    start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();records=[];failed=None
    for name in ['q048_v113_actual_consumer.py','q048_v113_verify.py','q048_v113_accept.py','q048_v113_postaccept.py']:
        t=time.monotonic();begin=datetime.now(timezone.utc).isoformat()
        try:
            p=subprocess.run([sys.executable,str(R/name)],capture_output=True,text=True,timeout=60)
            record={'command':[sys.executable,name],'start_utc':begin,'end_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'code_sha256':sha(R/name)}
        except Exception as ex:
            record={'command':[sys.executable,name],'start_utc':begin,'end_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'returncode':None,'exception':{'type':type(ex).__name__,'message':str(ex)},'code_sha256':sha(R/name)}
        records.append(record)
        if record['returncode']!=0:failed=record;break
    result={'schema':'bubbleverse.q048.v113.source_correct_actual_consumer.execution.v1','q':'Q048','target_q':'Q048','compute_backend':'LOCAL_RUNTIME','github_actions_used':False,'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'status':'COMPLETE' if failed is None and len(records)==4 else 'FAILED','first_failure':failed,'commands':records,'actual_consumer_executions':1,'theorem_producer_executions':0,'historical_program_main_executions':0,'below940_executions':0,'retry_count':0,'freeze_sha256':sha(R/(P+'FREEZE_V1.json')),'spec_sha256':frozen['spec_sha256']}
    with (R/(P+'EXECUTION_V1.json')).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':result['status'],'wall_seconds':result['wall_seconds'],'first_failure':failed}))
    for record in records:print(record.get('stdout',''),record.get('stderr',''))
    if result['status']!='COMPLETE':raise SystemExit(1)
if __name__=='__main__':main()
