"""Frozen serial V141 runner: producer -> independent verifier -> acceptance/readback."""
from pathlib import Path
import json,hashlib,subprocess,sys,time,datetime
R=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text())
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def write_x(name,obj):
    with (R/name).open('x') as f:
        json.dump(obj,f,indent=2,ensure_ascii=False); f.write('\n')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    freeze=read(R/'Q048_V141_FREEZE_V1.json')
    spec=read(R/'Q048_V141_SPEC_V1.json')
    def unchanged():
        return all((R/k).is_file() and sha(R/k)==v for k,v in freeze['frozen_files'].items())
    outputs=['Q048_V141_RAW_V1.json','Q048_V141_VERIFICATION_V1.json','Q048_V141_ACCEPTANCE_V1.json','Q048_V141_ACCEPTANCE_READBACK_V1.json','Q048_V141_EXECUTION_V1.json']
    rec={'schema':'bubbleverse.q048.v141.execution.v1','run_id':freeze['run_id'],'started_at_utc':now(),'status':'FAIL',
         'retry_count':0,'postfreeze_edits':False,'historical_mains_executed':0,'native_integrations':0,
         'new_actual_cells':0,'producer_chains_started':0,'accepted_new_proof_cells':0,'phases':[],
         'science_seconds_max':spec['criteria']['science_seconds_max'],'return_route':'BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0'}
    start=time.monotonic()
    terminal_obstruction=False
    try:
        if any((R/x).exists() for x in outputs): raise FileExistsError('PREEXISTING_OUTPUT')
        if not unchanged(): raise ValueError('PREFREEZE_HASH_DRIFT')
        for phase,script in [('producer','q048_v141_proof.py'),('verifier','q048_v141_verify.py')]:
            if phase=='verifier':
                raw=read(R/'Q048_V141_RAW_V1.json')
                if raw.get('status')=='FIRST_MATERIAL_OBSTRUCTION':
                    rec['status']='FIRST_MATERIAL_OBSTRUCTION'; rec['obstruction']=raw.get('obstruction'); terminal_obstruction=True
                    break
                if raw.get('status')!='CANDIDATE_CONDITIONAL_CONNECTED_PROOF': raise ValueError('RAW_STATUS:'+str(raw.get('status')))
                if [x['name'] for x in raw.get('gates',[])]!=spec['baseline_gate_roster'] or not all(x.get('pass') is True for x in raw.get('gates',[])):
                    raise ValueError('RAW_GATE_ROSTER_OR_PASS')
            if time.monotonic()-start>spec['criteria']['science_seconds_max']: raise TimeoutError('BUDGET_BEFORE_'+phase.upper())
            t=time.monotonic()
            cp=subprocess.run([sys.executable,str(R/script)],cwd=R,capture_output=True,text=True)
            if phase=='producer': rec['producer_chains_started']=1
            rec['phases'].append({'phase':phase,'returncode':cp.returncode,'seconds':time.monotonic()-t,'stdout':cp.stdout,'stderr':cp.stderr})
            if cp.returncode: raise RuntimeError(phase.upper()+'_PROCESS_FAIL')
            if time.monotonic()-start>spec['criteria']['science_seconds_max']: raise TimeoutError('BUDGET_AFTER_'+phase.upper())
            if not unchanged(): raise ValueError('POST_PHASE_HASH_DRIFT:'+phase)
            if phase=='producer':
                raw=read(R/'Q048_V141_RAW_V1.json')
                if raw.get('status')=='FIRST_MATERIAL_OBSTRUCTION':
                    rec['status']='FIRST_MATERIAL_OBSTRUCTION'; rec['obstruction']=raw.get('obstruction'); terminal_obstruction=True
                    break
        if not terminal_obstruction:
            raw=read(R/'Q048_V141_RAW_V1.json')
            ver=read(R/'Q048_V141_VERIFICATION_V1.json')
            task=read(R/spec['task']); parent=read(R/spec['parent'])
            required=(raw['status']=='CANDIDATE_CONDITIONAL_CONNECTED_PROOF' and ver['status']=='PASS' and
                      ver['checks_passed']==ver['checks_total'] and ver['checks_total']>=spec['criteria']['baseline_named_checks_min'] and
                      ver['check_roster']==spec['verifier_check_roster'] and ver['check_roster_ok'] is True and
                      ver['semantic_mutations_rejected']==ver['semantic_mutations_total'] and
                      ver['semantic_mutations_total']>=spec['criteria']['semantic_controls_min'] and
                      ver['semantic_control_roster']==spec['semantic_control_roster'] and ver['semantic_control_roster_ok'] is True and
                      ver['semantic_controls_nonvacuous'] is True and all(ver['mutation_failed_checks'].values()))
            if not required: raise ValueError('VALIDATION_OR_ROSTER_GATE')
            accept={'schema':'bubbleverse.q048.v141.acceptance.v1','status':'ACCEPTED_CONDITIONAL_SOURCE_REAL_CONNECTED_PROOF',
                    'accepted_at_utc':now(),'q':'Q048','target_q':'Q048','task_id':task['task_id'],'task_fingerprint':task['task_fingerprint'],
                    'cell_z':[840,830],'cell_a':['1/841','1/831'],
                    'raw_sha256':sha(R/'Q048_V141_RAW_V1.json'),'verification_sha256':sha(R/'Q048_V141_VERIFICATION_V1.json'),
                    'freeze_sha256':sha(R/'Q048_V141_FREEZE_V1.json'),'spec_sha256':sha(R/'Q048_V141_SPEC_V1.json'),
                    'K_upper':raw['comparison']['K_upper'],'connected_lower':raw['comparison']['h_connected_lower'],
                    'h_upper':'99999/100000','thermal_domain':['-1/1000000','1/50'],
                    'operators':['HMLA','SWIFT'],'q_branches':{'L':'1/1000000','R':'0'},
                    'continuation':raw['continuation'],'guard_primary_sha256':raw['guard_primary_sha256'],'guard_control_sha256':raw['guard_control_sha256'],
                    'guard_endpoint_crosscheck_only':task['guard']['expected_primary_endpoint_crosscheck_only'],
                    'baseline_gate_roster':spec['baseline_gate_roster'],'baseline_gate_roster_sha256':hashlib.sha256(canon(spec['baseline_gate_roster'])).hexdigest(),
                    'verifier_check_roster':ver['check_roster'],'verifier_check_roster_sha256':ver['check_roster_sha256'],
                    'semantic_control_roster':ver['semantic_control_roster'],'semantic_control_roster_sha256':ver['semantic_control_roster_sha256'],
                    'new_mathematical_proof_cells':1,'new_actual_cells':0,'actual_unchanged':parent['actual'],'frontiers_unchanged':parent['frontiers'],
                    'consumer_authorization':'NOT_GRANTED_BY_MATHEMATICS','NativeP6':'UNRESOLVED','q_complete':False,
                    'native_error_certificate':False,'exact_selector_existence_uniqueness':False,'trajectory_identity_claim':False,
                    'return_route':'BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0'}
            write_x('Q048_V141_ACCEPTANCE_V1.json',accept)
            if read(R/'Q048_V141_ACCEPTANCE_V1.json')!=accept: raise ValueError('ACCEPTANCE_READBACK_OBJECT')
            rb={'schema':'bubbleverse.q048.v141.acceptance_readback.v1','status':'PASS',
                'acceptance_sha256':sha(R/'Q048_V141_ACCEPTANCE_V1.json'),
                'raw_sha256':sha(R/'Q048_V141_RAW_V1.json'),'verification_sha256':sha(R/'Q048_V141_VERIFICATION_V1.json'),
                'ordered_maps':{'baseline_gate_roster':accept['baseline_gate_roster'],'verifier_check_roster':accept['verifier_check_roster'],'semantic_control_roster':accept['semantic_control_roster']},
                'counts':{'baseline_gates':len(accept['baseline_gate_roster']),'verifier_checks':len(accept['verifier_check_roster']),'semantic_controls':len(accept['semantic_control_roster'])},
                'nonempty':all(len(v)>0 for v in [accept['baseline_gate_roster'],accept['verifier_check_roster'],accept['semantic_control_roster']]),
                'actual_unchanged':accept['actual_unchanged'],'frontiers_unchanged':accept['frontiers_unchanged'],'new_actual_cells':0,'new_mathematical_proof_cells':1}
            write_x('Q048_V141_ACCEPTANCE_READBACK_V1.json',rb)
            if read(R/'Q048_V141_ACCEPTANCE_READBACK_V1.json')!=rb or not rb['nonempty']: raise ValueError('SERIALIZED_READBACK')
            if not unchanged(): raise ValueError('POST_ACCEPT_HASH_DRIFT')
            rec['status']='PASS'; rec['accepted_new_proof_cells']=1
            rec['acceptance_sha256']=sha(R/'Q048_V141_ACCEPTANCE_V1.json'); rec['acceptance_readback_sha256']=sha(R/'Q048_V141_ACCEPTANCE_READBACK_V1.json')
    except Exception as e:
        rec['error']=type(e).__name__+':'+str(e)
    finally:
        rec['finished_at_utc']=now(); rec['science_seconds']=time.monotonic()-start
        rec['deadline_respected']=rec['science_seconds']<=spec['criteria']['science_seconds_max']
        rec['frozen_pins_unchanged']=unchanged()
        write_x('Q048_V141_EXECUTION_V1.json',rec)
    print(json.dumps({'status':rec['status'],'science_seconds':rec['science_seconds'],'deadline_respected':rec['deadline_respected'],'phases':[(x['phase'],x['returncode']) for x in rec['phases']], 'obstruction':rec.get('obstruction'), 'error':rec.get('error')}))
    if rec['status'] in ('PASS','FIRST_MATERIAL_OBSTRUCTION'): return 0
    return 1

if __name__=='__main__': raise SystemExit(main())
