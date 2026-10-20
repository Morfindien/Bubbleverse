"""Frozen bounded V118 execution. One producer; separate verifier and real mutation controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time,sys,copy,importlib.util

R=Path(__file__).resolve().parent;P='Q048_V118_SOURCE_CORRECT_PROOF_'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def save(n,o):
    with (R/n).open('x') as f:json.dump(o,f,indent=2);f.write('\n')
def main():
    specpath=R/(P+'SPEC_V1.json');freeze=load(R/(P+'FREEZE_V1.json'));spec=load(specpath)
    if sha(specpath)!=freeze['spec_sha256']:raise ValueError('FROZEN_SPEC')
    for collection in ['input_pins','code_pins']:
        for n,pin in spec[collection].items():
            p=R/n
            if p.stat().st_size!=pin['bytes'] or sha(p)!=pin['sha256']:raise ValueError('FROZEN_BYTE_PIN:'+n)
    start=datetime.now(timezone.utc).isoformat();clock=time.monotonic();records=[];status='RUNNING';obstruction=None
    def remaining():
        x=spec['science_budget_seconds']-(time.monotonic()-clock)
        if x<=0:raise TimeoutError('FROZEN_300_SCIENCE_SECONDS')
        return x
    try:
        cmd=[sys.executable,str(R/'q048_v118_proof.py'),'--spec',str(specpath),'--output',str(R/(P+'RAW_V1.json'))]
        t=time.monotonic();result=subprocess.run(cmd,capture_output=True,text=True,timeout=remaining())
        records.append({'phase':'PRODUCER','command':cmd,'returncode':result.returncode,'wall_seconds':time.monotonic()-t,'stdout':result.stdout,'stderr':result.stderr})
        if result.returncode:raise RuntimeError('PRODUCER_EXECUTION_FAILED')
        raw=load(R/(P+'RAW_V1.json'))
        if raw['status']!='CANDIDATE_PROOF':
            status='FIRST_OBSTRUCTION';obstruction=raw.get('obstruction',{'gate':raw['status']})
        else:
            vs=importlib.util.spec_from_file_location('v118_separate_verifier',R/'q048_v118_verify.py');m=importlib.util.module_from_spec(vs);vs.loader.exec_module(m)
            t=time.monotonic();remaining();v=m.verify(R,spec,raw)
            records.append({'phase':'SEPARATE_VERIFIER','command':'q048_v118_verify.verify(root,spec,raw)','status':v['status'],'wall_seconds':time.monotonic()-t})
            v['raw_sha256']=sha(R/(P+'RAW_V1.json'))
            if v['status']!='PASS':
                save(P+'VERIFICATION_V1.json',v);status='VALIDATION_FAILED';obstruction={'gate':'BASELINE_VERIFIER','failed_checks':[k for k,x in v['checks'].items() if not x]}
            else:
                variants=[('wrong_parent_hash',('parent_checkpoint_sha256',),'0'*64),('wrong_h0',('h0',),'1'),('wrong_cell',('cell_z',),[910,910]),('wrong_a',('cell_a',),['1/911','1/911']),('wrong_row',('guard_primary_index',),48),('reset',('source_state_reset',),True),('bad_saha',('saha_factor_source',),'3.016101031869581e21'),('actual_promotion',('new_actual_cells',),1),('preaccept_proof',('new_mathematical_proof_cells',),1),('below910',('below910_work',),True),('epsilon',('epsilon',),'1/100'),('thermal',('thermal_domain',),['-1/1000000','1/100']),('wrong_fingerprint',('task_fingerprint',),'1'*64),('drop_L',('branches','L'),None),('wrong_K',('K_upper',),'1'),('zero_lower',('hmin',),'0')]
                controls={};details={};t=time.monotonic()
                for name,path,value in variants:
                    remaining();mut=copy.deepcopy(raw);obj=mut
                    for key in path[:-1]:obj=obj[key]
                    if name=='drop_L':del obj[path[-1]]
                    else:obj[path[-1]]=value
                    if mut==raw:raise ValueError('NO_OP_MUTATION:'+name)
                    test=m.verify(R,spec,mut)
                    controls[name]=test['status']=='FAIL' and not test['verification_pass']
                    details[name]=[k for k,x in test['checks'].items() if not x]
                v.update(semantic_mutations_total=len(controls),semantic_mutations_rejected=sum(controls.values()),semantic_mutations=controls,mutation_failed_invariants=details)
                if not all(controls.values()):v['status']='FAIL';v['verification_pass']=False
                records.append({'phase':'REAL_MUTATION_CONTROLS','count':len(controls),'rejected':sum(controls.values()),'wall_seconds':time.monotonic()-t})
                save(P+'VERIFICATION_V1.json',v)
                if v['status']!='PASS':status='VALIDATION_FAILED';obstruction={'gate':'MUTATION_CONTROLS'}
                else:
                    remaining();cmd=[sys.executable,str(R/'q048_v118_accept.py'),'--root',str(R)];t=time.monotonic();result=subprocess.run(cmd,capture_output=True,text=True,timeout=remaining());records.append({'phase':'ACCEPT_AND_READBACK','command':cmd,'returncode':result.returncode,'wall_seconds':time.monotonic()-t,'stdout':result.stdout,'stderr':result.stderr})
                    if result.returncode:raise RuntimeError('ACCEPTANCE_FAILED')
                    status='COMPLETE'
    except Exception as e:
        status='FAILED_OR_BLOCKED';obstruction={'type':type(e).__name__,'message':str(e)}
    finally:
        out={'schema':'bubbleverse.q048.v118.source_correct_proof.execution.v1','task_id':spec['task_id'],'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'science_elapsed_seconds':time.monotonic()-clock,'science_budget_seconds':spec['science_budget_seconds'],'compute_backend':'LOCAL_RUNTIME','github_actions_used':False,'status':status,'obstruction':obstruction,'phases':records,'producer_invocations':1,'historical_program_main_invocations':0,'new_actual_cells':0,'actual_state_unchanged':{'count':116,'frontier':920},'below910_work':False,'no_retry':True,'spec_sha256':sha(specpath),'code_hashes':{n:sha(R/n) for n in spec['code_pins']}}
        save(P+'EXECUTION_V1.json',out);print(json.dumps({'status':status,'seconds':out['science_elapsed_seconds'],'obstruction':obstruction}))
    if status!='COMPLETE':raise SystemExit(1)
if __name__=='__main__':main()
