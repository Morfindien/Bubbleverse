"""V90 one-proof hash-bound transition/acceptance/postaccept. Does not run a proof or actual consumer."""
from datetime import datetime,timezone
import json,sys
from q048_v90_proof_contract import ROOT,TASK,PARENT,RAW,SPEC,load,sha,output,require,load_spec,validate_spec
from q048_moving_h_domain_verify_v90 import core_validate

def main():
    s=load_spec()
    if '--preflight' in sys.argv:print(json.dumps({'kind':'ACCEPTOR_METADATA_ONLY_NO_ACCEPTANCE','status':'PASS','checks':len(validate_spec(s))}));return
    r=load(ROOT/RAW);c=load(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json');v=load(ROOT/'q048_moving_h_domain_validation_v90.json');e=load(ROOT/'q048_moving_h_domain_verifier_recomputation_v90.json')
    checks=core_validate(r,c,s,e)
    require(all(x['pass'] for x in checks),'TRANSITION_CORE_FAIL')
    require(v['status']==v['technical_state']=='PASS' and v['checks_passed']==v['checks_total'] and v['mutations_rejected']==v['mutations_total']>=24,'VALIDATION_REQUIRED')
    require(v['result_sha256']==sha(ROOT/RAW) and v['candidate_checkpoint_sha256']==sha(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json') and v['spec_sha256']==sha(ROOT/SPEC),'VALIDATION_HASH_BINDING')
    require(v['validator_sha256']==sha(ROOT/'q048_moving_h_domain_verify_v90.py') and v['verifier_recomputation_sha256']==sha(ROOT/'q048_moving_h_domain_verifier_recomputation_v90.json'),'VERIFIER_CODE_EVIDENCE_BINDING')
    tr={'schema_version':'Q048_MOVING_H_DOMAIN_TRANSITION_V90','q':'Q048','status':'PASS','checks_total':len(checks),'checks_passed':len(checks),'checks':checks,'actual_unchanged':{'count':106,'frontier':1020},'new_actual_paired_cells':0,'new_proof_cells':1,'proof_cell_z':[1020,1010],'result_sha256':sha(ROOT/RAW),'candidate_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json'),'validation_sha256':sha(ROOT/'q048_moving_h_domain_validation_v90.json'),'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint'],'timestamp_utc':datetime.now(timezone.utc).isoformat()}
    output('q048_moving_h_domain_transition_validation_v90.json',tr)
    parent=load(ROOT/'inputs'/PARENT);co=r['comparison']
    cp={'schema_version':'Q048_MOVING_H_DOMAIN_ACCEPTED_CHECKPOINT_V90','q':'Q048','target_q':'Q048','source_result':RAW,'source_result_sha256':sha(ROOT/RAW),'status':'VALIDATED','technical_state':'PASS','checkpoint_kind':'ACCEPTED_MATHEMATICAL_PROOF','proof_cell_z':[1020,1010],'proof_cell_a':['1/1021','1/1011'],'parent_actual_checkpoint_sha256':sha(ROOT/'inputs'/PARENT),'actual_frontiers':parent['frontiers'],'actual_scalar_endpoint':parent['endpoint'],'total_actual_paired_cells':106,'new_actual_paired_cells':0,'new_mathematical_proof_cells':1,'comparison_start_lower':co['initial_lower'],'comparison_endpoint_lower':co['whole_cell_h_min'],'comparison_K_upper':co['K_upper'],'physical_state_reset':False,'task_id':s['task_id'],'task_fingerprint':s['task_fingerprint'],'execution_fingerprint':s['execution_fingerprint'],'q_complete':False,'scientific_scope':'CONDITIONAL_SOURCE_REAL_MOVING_H_PROOF_DOMAIN_ONLY','mathematical_cell_status':r['status'],'validation_sha256':sha(ROOT/'q048_moving_h_domain_validation_v90.json'),'transition_validation_sha256':sha(ROOT/'q048_moving_h_domain_transition_validation_v90.json'),'candidate_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json'),'spec_sha256':sha(ROOT/SPEC),'contract_markdown_sha256':s['contract_markdown_sha256'],'validator_sha256':v['validator_sha256'],'acceptor_sha256':sha(__file__),'guard_primary_row_sha256':r['guard_primary_row_sha256'],'guard_control_row_sha256':r['guard_control_row_sha256'],'question_sha256':s['question_sha256'],'source_commit':s['source_commit'],'capture_sha256':s['capture_sha256'],'NativeP6':'UNRESOLVED','historical_reproducibility_gap':s['historical_provenance_gaps'],'accepted_at_utc':datetime.now(timezone.utc).isoformat(),'resume_rule':'Return once to Result Ingestion2.1.0; actual106/frontier1020 unchanged. No automatic actual consumer or below1010 continuation.'}
    output('q048_moving_h_domain_accepted_checkpoint_v90.json',cp)
    ac={'schema_version':'Q048_MOVING_H_DOMAIN_ACCEPTANCE_V90','q':'Q048','status':'PASS','accepted_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_accepted_checkpoint_v90.json'),'transition_sha256':sha(ROOT/'q048_moving_h_domain_transition_validation_v90.json'),'validation_sha256':sha(ROOT/'q048_moving_h_domain_validation_v90.json'),'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint'],'conditions':['all core checks PASS','all semantic mutations rejected','raw/spec/code/recomputation hashes bound','actual unchanged 106/1020','one proof 1020→1010 only'],'accepted_utc':datetime.now(timezone.utc).isoformat()}
    output('q048_moving_h_domain_acceptance_validation_v90.json',ac)
    saved=load(ROOT/'q048_moving_h_domain_accepted_checkpoint_v90.json');tests=[]
    def t(k,b):tests.append({'check':k,'pass':bool(b)})
    t('checkpoint_hash',sha(ROOT/'q048_moving_h_domain_accepted_checkpoint_v90.json')==ac['accepted_checkpoint_sha256'])
    t('proof_domain',saved['proof_cell_z']==[1020,1010] and saved['proof_cell_a']==['1/1021','1/1011'])
    t('actual_count',saved['total_actual_paired_cells']==106 and saved['new_actual_paired_cells']==0)
    t('actual_frontiers',saved['actual_frontiers']==parent['frontiers'])
    t('actual_endpoint',saved['actual_scalar_endpoint']==parent['endpoint'])
    t('one_proof',saved['new_mathematical_proof_cells']==1 and saved['checkpoint_kind']=='ACCEPTED_MATHEMATICAL_PROOF')
    for k,value in [('source_result_sha256',sha(ROOT/RAW)),('validation_sha256',sha(ROOT/'q048_moving_h_domain_validation_v90.json')),('transition_validation_sha256',sha(ROOT/'q048_moving_h_domain_transition_validation_v90.json')),('parent_actual_checkpoint_sha256',sha(ROOT/'inputs'/PARENT)),('spec_sha256',sha(ROOT/SPEC))]:t(k,saved[k]==value)
    t('comparison_lower',saved['comparison_endpoint_lower']==co['whole_cell_h_min'] and saved['comparison_start_lower']==parent['connected_lower'])
    t('comparison_K',saved['comparison_K_upper']==co['K_upper'])
    t('no_reset',saved['physical_state_reset'] is False)
    t('no_full_Q',saved['q_complete'] is False and saved['NativeP6']=='UNRESOLVED')
    t('question_source',saved['question_sha256']==s['question_sha256'] and saved['source_commit']==s['source_commit'] and saved['capture_sha256']==s['capture_sha256'])
    t('identity',saved['execution_fingerprint']==s['execution_fingerprint'] and saved['task_fingerprint']==s['task_fingerprint'])
    good=all(x['pass'] for x in tests)
    output('q048_moving_h_domain_postaccept_validation_v90.json',{'schema_version':'Q048_MOVING_H_DOMAIN_POSTACCEPT_V90','q':'Q048','status':'PASS' if good else 'FAIL','checks_total':len(tests),'checks_passed':sum(x['pass'] for x in tests),'checks':tests,'accepted_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_accepted_checkpoint_v90.json'),'acceptance_validation_sha256':sha(ROOT/'q048_moving_h_domain_acceptance_validation_v90.json'),'execution_fingerprint':s['execution_fingerprint'],'verified_utc':datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'status':'PASS' if good else 'FAIL','proof':[1020,1010],'actual_unchanged':[106,1020],'postaccept':str(sum(x['pass'] for x in tests))+'/'+str(len(tests))}))
    require(good,'POSTACCEPT_FAIL')
if __name__=='__main__':main()
