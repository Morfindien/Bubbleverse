"""Hash-bound one-cell V87 transition/acceptance/postaccept; never runs science."""
from datetime import datetime,timezone
from copy import deepcopy
import json,sys
from q048_v87_consumer_contract import ROOT,TASK,PARENT,PROOF,RAW,SPEC,sha,load,output,require,load_spec,validate_spec
from q048_frec_moving_h_verify_v87 import core_validate

def main():
    s=load_spec()
    if '--preflight' in sys.argv:
        print(json.dumps({'kind':'METADATA_ONLY_ACCEPTOR_PREFLIGHT_NO_ACCEPTANCE','status':'PASS','checks':len(validate_spec(s))}));return
    r=load(ROOT/RAW);c=load(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json');v=load(ROOT/'q048_frec_moving_h_validation_v87.json');task=load(ROOT/'inputs'/TASK)
    checks=core_validate(r,c,s)
    require(all(z['pass'] for z in checks),'CORE_TRANSITION_CHECKS')
    require(v['status']==v['technical_state']=='PASS' and v['checks_passed']==v['checks_total'] and v['mutations_rejected']==v['mutations_total']>=24,'VALIDATION_PASS')
    require(v['result_sha256']==sha(ROOT/RAW) and v['candidate_checkpoint_sha256']==sha(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json') and v['spec_sha256']==sha(ROOT/SPEC),'VALIDATION_HASH_BINDING')
    require(v['validator_sha256']==sha(ROOT/'q048_frec_moving_h_verify_v87.py'),'VALIDATOR_CODE_BINDING')
    trans={'schema':'bubbleverse.q048.frec_moving_h.transition.v87','q':'Q048','target_q':'Q048','status':'PASS','actual_before':{'count':104,'frontier':1040},'proposed_after':{'count':105,'frontier':1030},'result_sha256':sha(ROOT/RAW),'candidate_checkpoint_sha256':sha(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json'),'validation_sha256':sha(ROOT/'q048_frec_moving_h_validation_v87.json'),'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint'],'checks_total':len(checks),'checks_passed':len(checks),'checks':checks,'timestamp_utc':datetime.now(timezone.utc).isoformat()}
    output('q048_frec_moving_h_transition_validation_v87.json',trans)
    parent=load(ROOT/'inputs'/PARENT);cp={k:deepcopy(parent[k]) for k in ['question_sha256','source_commit','capture_sha256','other_frontiers','scientific_scope','q_complete','NativeP6','no_physical_reset','no_native_trajectory_claim']}
    after=task['candidate_success_state'];fronts=deepcopy(parent['frontiers']);fronts['hillipop-ede_n3']=1030
    cp.update(schema='bubbleverse.q048.frec_moving_h.accepted_checkpoint.v87',q='Q048',target_q='Q048',status='VALIDATED',technical_state='PASS',checkpoint_kind='ACCEPTED_ACTUAL',actual_before=task['initial_actual_state'],accepted_actual={'count':105,'frontier':1030},frontiers=fronts,endpoint=after['endpoint'],connected_lower=after['connected_lower'],K_upper=r['K_upper'],candidate_checkpoint_sha256=sha(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json'),parent_sha256=sha(ROOT/'inputs'/PARENT),proof_accepted_checkpoint_sha256=sha(ROOT/'inputs'/PROOF),proof_validation_sha256=r['proof_validation_sha256'],source_result_sha256=sha(ROOT/RAW),validation_sha256=sha(ROOT/'q048_frec_moving_h_validation_v87.json'),transition_validation_sha256=sha(ROOT/'q048_frec_moving_h_transition_validation_v87.json'),task_id=s['task_id'],task_fingerprint=s['task_fingerprint'],execution_fingerprint=s['execution_fingerprint'],spec_sha256=sha(ROOT/SPEC),contract_markdown_sha256=s['contract_markdown_sha256'],new_actual_cells=1,new_mathematical_proof_cells=0,accepted_at_utc=datetime.now(timezone.utc).isoformat(),technical_adapter_revision='V87 fresh consumer1040→1030 from accepted V85 actual and V86 proof; unchanged retained source-real science.',missing_historical_evidence=s['historical_provenance_gaps'],resume_rule='Return exactly once to Result Ingestion2.1.0; no below1030 continuation.')
    # A clean checkpoint contains no inherited acceptance/adapter identity from its parent.
    cp.pop('acceptance_validation_sha256',None)
    cp['acceptor_sha256']=sha(__file__)
    output('q048_frec_moving_h_accepted_checkpoint_v87.json',cp)
    ac={'schema':'bubbleverse.q048.frec_moving_h.acceptance.v87','q':'Q048','status':'PASS','accepted_checkpoint_sha256':sha(ROOT/'q048_frec_moving_h_accepted_checkpoint_v87.json'),'transition_sha256':sha(ROOT/'q048_frec_moving_h_transition_validation_v87.json'),'validation_sha256':sha(ROOT/'q048_frec_moving_h_validation_v87.json'),'candidate_checkpoint_sha256':sha(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json'),'execution_fingerprint':s['execution_fingerprint'],'acceptor_sha256':sha(__file__),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'conditions':['verified core transition','all required verifier checks PASS','all semantic mutations rejected','unchanged science scope','new contract and frozen identity','exact one-cell increment']}
    output('q048_frec_moving_h_acceptance_validation_v87.json',ac)
    saved=load(ROOT/'q048_frec_moving_h_accepted_checkpoint_v87.json');tests=[]
    def t(name,condition):tests.append({'check':name,'pass':bool(condition)})
    t('accepted_hash',sha(ROOT/'q048_frec_moving_h_accepted_checkpoint_v87.json')==ac['accepted_checkpoint_sha256'])
    t('count_frontier',saved['accepted_actual']=={'count':105,'frontier':1030})
    t('frontiers',saved['frontiers']==fronts and all(saved['frontiers'][k]==1440 for k in ['camspec-lcdm','camspec-ede_n3','hillipop-lcdm']))
    t('endpoint',saved['endpoint']==after['endpoint']);t('lower',saved['connected_lower']==after['connected_lower']);t('K',saved['K_upper']==r['K_upper'])
    for key,value in [('source_result_sha256',sha(ROOT/RAW)),('validation_sha256',sha(ROOT/'q048_frec_moving_h_validation_v87.json')),('transition_validation_sha256',sha(ROOT/'q048_frec_moving_h_transition_validation_v87.json')),('parent_sha256',sha(ROOT/'inputs'/PARENT)),('proof_accepted_checkpoint_sha256',sha(ROOT/'inputs'/PROOF)),('spec_sha256',sha(ROOT/SPEC))]:t(key,saved[key]==value)
    t('question',saved['question_sha256']==s['question_sha256']);t('source',saved['source_commit']==s['source_commit']);t('capture',saved['capture_sha256']==s['capture_sha256'])
    t('identity',saved['execution_fingerprint']==s['execution_fingerprint'] and saved['task_fingerprint']==s['task_fingerprint']);t('single_cell',saved['new_actual_cells']==1 and saved['new_mathematical_proof_cells']==0)
    t('no_overclaim',saved['q_complete'] is False and saved['NativeP6']=='UNRESOLVED' and saved['no_physical_reset'] is True and saved['no_native_trajectory_claim'] is True)
    good=all(z['pass'] for z in tests)
    output('q048_frec_moving_h_postaccept_validation_v87.json',{'schema':'bubbleverse.q048.frec_moving_h.postaccept.v87','q':'Q048','status':'PASS' if good else 'FAIL','checks_total':len(tests),'checks_passed':sum(z['pass'] for z in tests),'checks':tests,'accepted_checkpoint_sha256':sha(ROOT/'q048_frec_moving_h_accepted_checkpoint_v87.json'),'acceptance_validation_sha256':sha(ROOT/'q048_frec_moving_h_acceptance_validation_v87.json'),'execution_fingerprint':s['execution_fingerprint'],'timestamp_utc':datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'status':'PASS' if good else 'FAIL','actual':saved['accepted_actual'],'postaccept':str(sum(z['pass'] for z in tests))+'/'+str(len(tests))}))
    require(good,'POSTACCEPT_FAIL')
if __name__=='__main__':main()
