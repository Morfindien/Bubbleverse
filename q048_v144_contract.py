import json, hashlib, copy, pathlib, re
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parent
TASK_PATH=ROOT/'inputs/Q048_V144_NEXT_BUILDER_TASK_CONTRACT_RECONSTRUCTED_CONSUMER_840_830_V1.json'
PARENT_PATH=ROOT/'inputs/Q048_V140_ACCEPTED_CHECKPOINT_V1.json'
GUARD_PATH=ROOT/'proof_runtime/ref/prior_v126/inputs/q048_guard_local_v_result_v12.json'
PREFIX_PATH=ROOT/'proof_runtime/ref/prior_v126/inputs/q048_prefix_config_v1.json'
V143_PATH=ROOT/'inputs/Q048_V143_RESULT_STATE_V1.json'
AUTH_PATH=ROOT/'inputs/Q048_V143_INGESTION_STATE_V1.json'
PROOF_DIR=ROOT/'proof_runtime'

def load(p):
    with open(p,encoding='utf-8') as f: return json.load(f)
def dump(p,o):
    with open(p,'w',encoding='utf-8') as f: json.dump(o,f,indent=2,ensure_ascii=False); f.write('\\n')
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def objsha(o): return hashlib.sha256(canon(o)).hexdigest()
def frac(s): return Fraction(s)
def getp(o,path):
    cur=o
    for k in path:
        cur=cur[k] if isinstance(k,int) else cur.get(k)
    return cur
def setp(o,path,val):
    cur=o
    for k in path[:-1]: cur=cur[k]
    cur[path[-1]]=val

def select_rows(guard):
    found={False:[],True:[]}
    for ev in guard.get('evaluators',[]):
        c=bool(ev.get('control'))
        for row in ev.get('rows',[]):
            if row.get('z0')==840 and row.get('z1')==830 and row.get('a0')=='1/841' and row.get('a1')=='1/831':
                found[c].append(row)
    if len(found[False])!=1 or len(found[True])!=1:
        raise RuntimeError(f'row uniqueness failed: {len(found[False])}/{len(found[True])}')
    return found[False][0],found[True][0]

def expected_proof_hashes(task):
    return {k:v['sha256'] for k,v in task['theorem_authority']['artifacts'].items()}

def validate_raw(raw,root=ROOT):
    task=load(TASK_PATH); parent=load(PARENT_PATH); guard=load(GUARD_PATH); acc=load(PROOF_DIR/'Q048_V142_ACCEPTANCE_V1.json'); v143=load(V143_PATH); auth=load(AUTH_PATH)
    primary,control=select_rows(guard)
    ep={'a':'1/831','E':primary['E_right'],'Y':primary['Y_right'],'Vbar':primary['V_admitted']}
    checks={}
    checks['schema']=raw.get('schema')=='bubbleverse.q048.v144.contract_reconstructed_consumer.raw.v1'
    checks['identity_q']=raw.get('q')=='Q048' and raw.get('target_q')=='Q048'
    checks['question']=raw.get('question_sha256')==task['question_sha256'] and raw.get('exact_question')==task['exact_question']
    checks['identity_task']=raw.get('task_id')==task['task_id']
    checks['task_fingerprint']=raw.get('task_fingerprint')==task['task_fingerprint']==hashlib.sha256(canon(task['task_definition_for_fingerprint'])).hexdigest()
    checks['identity_run']=isinstance(raw.get('run_id'),str) and raw['run_id'].startswith('LOCAL-Q048-V144-')
    checks['program']=raw.get('program_id')=='Q048-CONDITIONAL-CONSUMER-V144-CONTRACT-REPAIR'
    checks['raw_state']=raw.get('status')=='CANDIDATE_NOT_CURRENT' and raw.get('candidate_is_current') is False
    checks['authorization']=raw.get('consumer_authorization')==task['consumer_authorization'] and auth.get('next_task_fingerprint')==task['task_fingerprint']
    checks['repair_strategy']=raw.get('repair_strategy')==task['task_definition_for_fingerprint']['repair_strategy']
    checks['v143_preserved']=raw.get('v143_historical_blockage',{}).get('result_state_sha256')==sha(V143_PATH)==task['v143_historical_blockage']['result_state_sha256'] and v143.get('execution_status')=='BLOCKED'
    checks['parent_hash']=sha(PARENT_PATH)==task['parent_authority']['sha256']==raw.get('parent_authority',{}).get('sha256')
    checks['parent_actual']=raw.get('parent_authority',{}).get('actual')=={'count':124,'frontier':840}==parent.get('actual')
    checks['parent_endpoint']=raw.get('parent_authority',{}).get('endpoint')==parent.get('endpoint')==task['parent_authority']['endpoint']
    checks['source_commit']=raw.get('source_commit')==task['source_commit']==acc.get('continuation',{}).get('background') and False
    # source_commit is not stored in acceptance continuation; override with direct task/raw identity below
    checks['source_commit']=raw.get('source_commit')==task['source_commit']=='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
    checks['capture']=raw.get('capture_sha256')==task['capture_sha256']=='2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b' and sha(PREFIX_PATH)==task['capture_sha256']
    ph=expected_proof_hashes(task); rr=raw.get('theorem_authority',{}).get('artifacts',{})
    checks['theorem_artifact_hashes']=all((PROOF_DIR/f).is_file() and sha(PROOF_DIR/f)==h and rr.get(f)==h for f,h in ph.items())
    checks['theorem_acceptance_hash']=rr.get('Q048_V142_ACCEPTANCE_V1.json')==sha(PROOF_DIR/'Q048_V142_ACCEPTANCE_V1.json')==task['task_definition_for_fingerprint']['v142_acceptance_sha256']
    checks['theorem_raw_hash']=rr.get('Q048_V142_RAW_V1.json')==sha(PROOF_DIR/'Q048_V142_RAW_V1.json')==task['task_definition_for_fingerprint']['v142_raw_sha256']
    checks['theorem_task_identity']=raw.get('theorem_authority',{}).get('task_id')==task['theorem_authority']['task_id']==acc.get('task_id')
    checks['theorem_run_identity']=raw.get('theorem_authority',{}).get('run_id')==task['theorem_authority']['run_id']
    checks['theorem_status']=acc.get('status')=='ACCEPTED_DEPENDENCY_AWARE_CONDITIONAL_SOURCE_REAL_CONNECTED_PROOF'
    checks['theorem_cell']=acc.get('cell_z')==[840,830] and acc.get('cell_a')==['1/841','1/831']
    checks['proof_validation_counts']=len(acc.get('baseline_gate_roster',[]))==40 and len(acc.get('verifier_check_roster',[]))==48 and len(acc.get('semantic_control_roster',[]))==50
    checks['guard_file']=sha(GUARD_PATH)==task['guard_authority']['sha256']==raw.get('guard_binding',{}).get('sha256')
    checks['guard_primary_unique']=objsha(primary)==task['guard_authority']['primary_row_sha256']==raw.get('guard_binding',{}).get('primary_row_sha256') and primary.get('index')==61
    checks['guard_control_unique']=objsha(control)==task['guard_authority']['control_row_sha256']==raw.get('guard_binding',{}).get('control_row_sha256') and control.get('index')==61
    checks['guard_role']=raw.get('guard_binding',{}).get('primary_control') is False
    checks['cell']=raw.get('guard_binding',{}).get('cell_z')==[840,830] and raw.get('guard_binding',{}).get('cell_a')==['1/841','1/831']
    left={'a0':primary['a0'],'E_input_left':primary['E_input_left'],'Y_left':primary['Y_left'],'V_previous':primary['V_previous']}
    checks['left_glue']=left==task['guard_authority']['left_glue'] and parent['endpoint']=={'a':left['a0'],'E':left['E_input_left'],'Y':left['Y_left'],'Vbar':left['V_previous']} and raw.get('guard_binding',{}).get('left_glue')==left
    checks['energy_cap']=raw.get('guard_binding',{}).get('energy_cap_used')==primary['E_input_left']==task['guard_authority']['energy_cap_used']
    checks['safe_energy_distinct']=primary['E_safe_left']==task['guard_authority']['E_safe_left_distinct'] and primary['E_safe_left']!=primary['E_input_left'] and raw.get('guard_binding',{}).get('E_safe_left_distinct')==primary['E_safe_left']
    checks['endpoint_source_binding']=raw.get('candidate_endpoint')==ep and raw.get('guard_binding',{}).get('endpoint')==ep and raw.get('guard_binding',{}).get('endpoint_derivation')=='PRIMARY_ROW61:a1,E_right,Y_right,V_admitted'
    checks['endpoint_crosscheck_only']=ep=={'a':'1/831','E':'15255752724206057963/500000000000000000','Y':'4839471313802804557/200000000000000000','Vbar':'3025529671378252963/500000000000000000'}
    checks['candidate_actual']=raw.get('candidate_actual')=={'count':125,'frontier':830}
    checks['candidate_frontiers']=raw.get('candidate_frontiers')=={'camspec-lcdm':1440,'camspec-ede_n3':1440,'hillipop-lcdm':1440,'hillipop-ede_n3':830}
    checks['current_until_publication']=raw.get('actual_current_until_publication')=={'count':124,'frontier':840}
    rt=raw.get('retained_theorem_values',{})
    checks['theorem_K']=rt.get('K_upper')==acc.get('K_upper')==task['retained_theorem_values']['K_upper']
    checks['theorem_lower']=rt.get('connected_lower')==acc.get('connected_lower')==task['retained_theorem_values']['connected_lower']
    checks['theorem_h_upper']=rt.get('h_upper')==acc.get('h_upper')==task['retained_theorem_values']['h_upper']
    checks['theorem_thermal']=rt.get('thermal_domain')==acc.get('thermal_domain')==task['retained_theorem_values']['thermal_domain']
    checks['theorem_operators']=rt.get('operators')==['HMLA','SWIFT']==acc.get('operators')
    checks['theorem_q_branches']=rt.get('q_branches')=={'L':'1/1000000','R':'0'}==acc.get('q_branches')
    checks['beta_method']=rt.get('beta_dependency_method')=='same_h_monotone'==acc.get('beta_dependency_method')
    checks['beta_values']=rt.get('beta_lower')==acc.get('beta_lower') and all(frac(v)>49 for v in acc.get('beta_lower',{}).values())
    checks['conditional_scope']=raw.get('source_cover_contract',{}).get('no_assumed_future_domain_membership') is True and raw.get('source_cover_contract',{}).get('exact_selector_existence_uniqueness') is False and raw.get('source_cover_contract',{}).get('native_error_certificate') is False and raw.get('source_cover_contract',{}).get('trajectory_identity_claim') is False
    checks['delta_actual']=raw.get('new_actual_cells')==1
    checks['delta_proof']=raw.get('new_mathematical_proof_cells')==0
    checks['delta_recompute']=raw.get('new_theorem_recomputations')==0 and raw.get('theorem_arithmetic_recomputed') is False
    checks['delta_consumption']=raw.get('theorem_consumptions')==1 and raw.get('v142_proof_status_before')=='ACCEPTED_UNCONSUMED'
    checks['no_reset']=raw.get('no_physical_reset') is True
    checks['native']=raw.get('native_error_certificate') is False and raw.get('NativeP6')=='UNRESOLVED'
    checks['selector']=raw.get('exact_selector_existence_uniqueness_established') is False
    checks['trajectory']=raw.get('trajectory_identity_claim') is False
    checks['q_complete']=raw.get('q_complete') is False
    checks['below830']=raw.get('below830_work') is False
    checks['actual126']=raw.get('actual126_created') is False
    checks['history']=raw.get('historical_record_modified') is False and raw.get('historical_science_reexecuted') is False and raw.get('proof_reexecuted') is False
    checks['missing_source_nondependency']=raw.get('missing_v140_historical_sources_required') is False
    checks['return_route']=raw.get('return_route')=='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0'
    return checks

CONTROL_SPECS=[
('wrong_q','identity_q',['q'],'Q999'),('wrong_target_q','identity_q',['target_q'],'Q999'),('wrong_question','question',['question_sha256'],'deadbeef'),('wrong_task','identity_task',['task_id'],'WRONG'),('wrong_fingerprint','task_fingerprint',['task_fingerprint'],'0'*64),('wrong_run','identity_run',['run_id'],'BAD'),('wrong_program','program',['program_id'],'BAD'),('premature_status','raw_state',['status'],'CURRENT'),('candidate_current','raw_state',['candidate_is_current'],True),('wrong_authorization','authorization',['consumer_authorization'],'BAD'),('wrong_repair','repair_strategy',['repair_strategy'],'V143_REPLAY'),('rewrite_v143','v143_preserved',['v143_historical_blockage','result_state_sha256'],'1'*64),('wrong_parent_hash','parent_hash',['parent_authority','sha256'],'2'*64),('wrong_parent_count','parent_actual',['parent_authority','actual','count'],123),('wrong_parent_frontier','parent_actual',['parent_authority','actual','frontier'],850),('wrong_parent_E','parent_endpoint',['parent_authority','endpoint','E'],'0'),('wrong_source','source_commit',['source_commit'],'bad'),('wrong_capture','capture',['capture_sha256'],'3'*64),('wrong_accept_hash','theorem_acceptance_hash',['theorem_authority','artifacts','Q048_V142_ACCEPTANCE_V1.json'],'4'*64),('wrong_raw_hash','theorem_raw_hash',['theorem_authority','artifacts','Q048_V142_RAW_V1.json'],'5'*64),('wrong_proof_task','theorem_task_identity',['theorem_authority','task_id'],'BAD'),('wrong_proof_run','theorem_run_identity',['theorem_authority','run_id'],'BAD'),('wrong_guard','guard_file',['guard_binding','sha256'],'6'*64),('wrong_primary_row','guard_primary_unique',['guard_binding','primary_row_sha256'],'7'*64),('wrong_control_row','guard_control_unique',['guard_binding','control_row_sha256'],'8'*64),('control_as_primary','guard_role',['guard_binding','primary_control'],True),('wrong_cell','cell',['guard_binding','cell_z'],[830,820]),('wrong_left_glue','left_glue',['guard_binding','left_glue','E_input_left'],'0'),('silent_cap_swap','energy_cap',['guard_binding','energy_cap_used'],'1969354442793606491/62500000000000000'),('safe_equals_cap','safe_energy_distinct',['guard_binding','E_safe_left_distinct'],'15881004977532652117/500000000000000000'),('copied_wrong_endpoint_E','endpoint_source_binding',['candidate_endpoint','E'],'0'),('wrong_endpoint_a','endpoint_source_binding',['candidate_endpoint','a'],'1/821'),('wrong_endpoint_Y','endpoint_source_binding',['candidate_endpoint','Y'],'0'),('wrong_endpoint_V','endpoint_source_binding',['candidate_endpoint','Vbar'],'0'),('actual126','candidate_actual',['candidate_actual','count'],126),('wrong_frontier','candidate_actual',['candidate_actual','frontier'],820),('wrong_branch_frontier','candidate_frontiers',['candidate_frontiers','hillipop-ede_n3'],820),('premature_current_125','current_until_publication',['actual_current_until_publication','count'],125),('wrong_K','theorem_K',['retained_theorem_values','K_upper'],'1'),('wrong_lower','theorem_lower',['retained_theorem_values','connected_lower'],'1'),('wrong_hupper','theorem_h_upper',['retained_theorem_values','h_upper'],'1'),('wrong_thermal','theorem_thermal',['retained_theorem_values','thermal_domain'],['-1','1']),('drop_operator','theorem_operators',['retained_theorem_values','operators'],['HMLA']),('wrong_qbranch','theorem_q_branches',['retained_theorem_values','q_branches','L'],'0'),('naive_beta_method','beta_method',['retained_theorem_values','beta_dependency_method'],'naive_interval'),('beta_tamper','beta_values',['retained_theorem_values','beta_lower','L'],'48'),('future_domain','conditional_scope',['source_cover_contract','no_assumed_future_domain_membership'],False),('native_promotion','native',['native_error_certificate'],True),('selector_promotion','selector',['exact_selector_existence_uniqueness_established'],True),('trajectory_promotion','trajectory',['trajectory_identity_claim'],True),('q_closure','q_complete',['q_complete'],True),('theorem_recompute','delta_recompute',['new_theorem_recomputations'],1),('double_consumption','delta_consumption',['theorem_consumptions'],2),('physical_reset','no_reset',['no_physical_reset'],False),('below830','below830',['below830_work'],True),('actual126_flag','actual126',['actual126_created'],True),('history_rewrite','history',['historical_record_modified'],True),('proof_replay','history',['proof_reexecuted'],True),('require_missing_sources','missing_source_nondependency',['missing_v140_historical_sources_required'],True),('wrong_return','return_route',['return_route'],'WRONG')]

def run_controls(raw):
    out=[]
    for cid,expected,path,bad in CONTROL_SPECS:
        m=copy.deepcopy(raw); before=objsha(m); setp(m,path,bad); after=objsha(m)
        ck=validate_raw(m); failed=[k for k,v in ck.items() if not v]
        out.append({'id':cid,'nonnoop':before!=after,'expected_invariant':expected,'failed_invariants':failed,'rejected':(before!=after and expected in failed)})
    return out

def verify_freeze():
    f=load(ROOT/'Q048_V144_FREEZE_V1.json'); out={}
    for rel,h in f['frozen_files'].items():
        p=ROOT/rel; out[rel]=p.exists() and sha(p)==h
    return out

def validate_checkpoint(cp,postaccept_sha=None):
    task=load(TASK_PATH); parent=load(PARENT_PATH); guard=load(GUARD_PATH); acc=load(PROOF_DIR/'Q048_V142_ACCEPTANCE_V1.json'); primary,_=select_rows(guard)
    ep={'a':'1/831','E':primary['E_right'],'Y':primary['Y_right'],'Vbar':primary['V_admitted']}
    c={}
    c['schema']=cp.get('schema')=='bubbleverse.q048.v144.accepted_checkpoint.v1'
    c['status']=cp.get('status')=='ACCEPTED_AFTER_POSTACCEPT'
    c['identity']=cp.get('q')=='Q048' and cp.get('target_q')=='Q048' and cp.get('question_sha256')==task['question_sha256'] and cp.get('task_id')==task['task_id'] and cp.get('task_fingerprint')==task['task_fingerprint']
    c['actual']=cp.get('actual')=={'count':125,'frontier':830}
    c['frontiers']=cp.get('frontiers')=={'camspec-lcdm':1440,'camspec-ede_n3':1440,'hillipop-lcdm':1440,'hillipop-ede_n3':830}
    c['endpoint']=cp.get('endpoint')==ep
    c['parent']=cp.get('parent_sha256')==sha(PARENT_PATH)==task['parent_authority']['sha256']
    c['capture']=cp.get('capture_sha256')==task['capture_sha256']
    c['source']=cp.get('source_commit')==task['source_commit']
    c['theorem']=cp.get('theorem_acceptance_sha256')==task['task_definition_for_fingerprint']['v142_acceptance_sha256']
    c['K']=cp.get('retained_theorem_values',{}).get('K_upper')==acc.get('K_upper')
    c['beta_method']=cp.get('retained_theorem_values',{}).get('beta_dependency_method')=='same_h_monotone'
    c['guard']=cp.get('guard_primary_row_sha256')==task['guard_authority']['primary_row_sha256']
    c['delta']=cp.get('new_actual_cells')==1 and cp.get('new_mathematical_proof_cells')==0 and cp.get('new_theorem_recomputations')==0 and cp.get('theorem_consumptions')==1
    c['v142_consumed_once']=cp.get('v142_proof_state_after')=='ACCEPTED_CONSUMED_ONCE'
    c['v143_preserved']=cp.get('v143_historical_status')=='IMMUTABLE_TERMINAL_PREFREEZE_INPUT_AVAILABILITY_BLOCKAGE'
    c['native']=cp.get('NativeP6')=='UNRESOLVED' and cp.get('native_error_certificate') is False
    c['qcomplete']=cp.get('q_complete') is False
    c['selector']=cp.get('exact_selector_existence_uniqueness_established') is False
    c['trajectory']=cp.get('trajectory_identity_claim') is False
    c['below']=cp.get('below830_work') is False and cp.get('actual126_created') is False
    if postaccept_sha is not None: c['postaccept']=cp.get('postaccept_sha256')==postaccept_sha
    return c
