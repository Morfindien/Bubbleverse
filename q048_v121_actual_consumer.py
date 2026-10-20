"""One bounded admission of committed row54 under accepted V120 fresh theorem."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from fractions import Fraction

PREFIX='Q048_V121_SOURCE_CORRECT_ACTUAL_CONSUMER_'
SPEC_HASH='9d8ede2d16482462e97ec426b29a7f8c7be7aa68646b3d6cb577774cb0ffb045'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_bytes())
def require(ok,label):
    if not ok: raise ValueError(label)

def main():
    ap=argparse.ArgumentParser();here=Path(__file__).resolve().parent
    ap.add_argument('--inputs',type=Path,default=here/'inputs');ap.add_argument('--out',type=Path,default=here)
    args=ap.parse_args(); output=args.out/(PREFIX+'RAW_V1.json')
    require(not output.exists(),'Already executed: refusing overwrite/replay')
    specpath=args.out/(PREFIX+'SPEC_V1.json');require(sha(specpath)==SPEC_HASH,'spec hash')
    s=load(specpath); inp={}
    for n,h in s['input_hashes'].items():
        require(sha(args.inputs/n)==h,'Input byte pin: '+n);inp[n]=load(args.inputs/n)
    p=inp['Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json']
    t=inp['Q048_V120_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json']
    proof_post=inp['Q048_V120_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'];task=inp['Q048_V121_NEXT_BUILDER_TASK_V1.json']
    tr=inp['Q048_V120_SOURCE_CORRECT_PROOF_RAW_V1.json']
    tv=inp['Q048_V120_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json']
    g=inp['q048_guard_local_v_result_v12.json'];i=inp['Q048_V120_INGESTION_STATE_V1.json']
    row=g['evaluators'][0]['rows'][54]; th=t; pins=s['input_hashes']
    parent_name='Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
    theorem_name='Q048_V120_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json'
    require(p['status']=='VALIDATED' and p['accepted_actual']==s['actual_before'],'parent status/state')
    require(t['status']=='ACCEPTED' and t['technical_state']=='PASS','theorem status')
    require(t['parent_checkpoint_sha256']==pins[parent_name],'theorem parent identity')
    require(t['schema']=='bubbleverse.q048.v120.source_correct_proof.acceptance.v1' and t['mathematical_proof_accepted'] is True,'fresh proof schema')
    require(t['parent_actual']==p['accepted_actual'] and t['parent_endpoint']==p['endpoint'] and t['parent_connected_lower']==p['connected_lower'],'fresh theorem parent fields')
    require(t['proof_cell_z']==s['cell_z'] and t['proof_cell_a']==s['cell_a'],'theorem cell')
    require(tv['status']=='PASS' and tv['checks_total']==tv['checks_passed']==31 and all(tv['checks'].values()),'retained theorem validation')
    require(tv['raw_sha256']==t['raw_sha256']==pins['Q048_V120_SOURCE_CORRECT_PROOF_RAW_V1.json'],'theorem raw pin')
    require(t['verification_sha256']==pins['Q048_V120_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json'],'theorem verifier pin')
    require(tv['semantic_mutations_total']==tv['semantic_mutations_rejected']==18,'retained mutation status')
    require(tr['parent_checkpoint_sha256']==pins[parent_name] and tr['parent_actual']==p['accepted_actual'] and tr['K_upper']==t['K_upper'] and tr['hmin']==t['connected_lower'],'raw bridge consistency')
    require(i['next_task_id']==s['task_id'] and i['consumer_authorization']=='GRANTED_BY_INGESTION_FOR_EXACTLY_ONE_CELL_910_TO_900','downstream authorization')
    require(proof_post['status']=='PASS' and proof_post['accepted_checkpoint_sha256']==pins[theorem_name] and proof_post['checks_total']==proof_post['checks_passed']==21 and all(proof_post['checks'].values()),'theorem postaccept')
    require(task['task_id']==s['task_id'] and task['task_fingerprint']==s['task_fingerprint'] and task['parent_authority']['sha256']==pins[parent_name] and task['theorem_authority']['sha256']==pins[theorem_name],'bounded task binding')

    expected_boundary={'z_min': '900', 'z_max': '910', 'low_z_branch_active_anywhere': False, 'Pion': '1', 'PION_MAX': '1/100', 'dispatch': 'SWIFT_FIT_SUBJECT_TO_OTHER_DOMAIN_GATES', 'boundary': 'z>=900', 'hydrogen_c_sha256': '734800ccd69b41d60b519f200003ce27c3b7640f76a70353499424842ba19616', 'hydrogen_h_sha256': '1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52'}
    expected_counts={'verification_checks': 31, 'semantic_mutations_rejected': 18, 'postaccept_checks': 21, 'delivery_checks': 35, 'preflight_binding_tests': 5}
    ps=inp['Q048_V120_SOURCE_CORRECT_PROOF_SPEC_V1.json'];pf=inp['Q048_V120_SOURCE_CORRECT_PROOF_FREEZE_V1.json'];pd=inp['Q048_V120_SOURCE_CORRECT_PROOF_DELIVERY_VALIDATION_V1.json']
    require(s['source_boundary_certificate']==t.get('source_boundary_certificate')==tr.get('source_boundary_certificate')==ps['source_boundary_preflight']['source_boundary_certificate']==task['source_boundary_contract']['certificate']==expected_boundary,'endpoint900 boundary certificate')
    require(t['proof_cell_z']==tr['cell_z']==[910,900] and t['proof_cell_a']==tr['cell_a']==['1/911','1/901'],'certificate/cell correspondence')
    require(tv['checks'].get('source_boundary_certificate') is True and proof_post['checks'].get('source_boundary_certificate') is True and all(tv['semantic_mutations'].values()) and all(tv['mutation_failed_invariants'].values()) and all(tv['semantic_mutations'].get(n) is True and 'source_boundary_certificate' in tv['mutation_failed_invariants'].get(n,[]) for n in ['boundary_missing','boundary_below900']),'proof boundary checks')
    require(t['spec_sha256']==pf['spec_sha256']==pins['Q048_V120_SOURCE_CORRECT_PROOF_SPEC_V1.json'] and t['freeze_sha256']==pins['Q048_V120_SOURCE_CORRECT_PROOF_FREEZE_V1.json'] and pd['status']=='PASS' and pd['checks_total']==pd['checks_passed']==35 and all(pd['checks'].values()) and ps['preflight']['binding_contract_tests'].startswith('5/5') and ps['source_boundary_preflight']['status']=='PASS' and all(ps['source_boundary_preflight']['other_domain_checks'].values()),'proof support pins/domain/delivery')
    require(s['proof_validation_requirements']==task['theorem_authority']['validation_requirements']==expected_counts,'proof validation requirements')
    require(t['consumer_authorization']=='NOT_GRANTED' and t['below900_authorization']=='NOT_GRANTED','mathematics stop preserved')
    require(t['source_commit']==task['theorem_authority']['source_commit'] and t['capture_sha256']==task['theorem_authority']['capture_sha256'],'source/capture binding')
    row_hash=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    require(row_hash==s['row_sha256'] and g['evaluators'][0]['control'] is False,'primary row hash')
    require(row['index']==54 and [row['z0'],row['z1']]==s['cell_z'] and [row['a0'],row['a1']]==s['cell_a'],'row cell')
    require(row['E_input_left']==p['endpoint']['E'] and row['Y_left']==p['endpoint']['Y'] and row['V_previous']==p['endpoint']['Vbar'] and row['a0']==p['endpoint']['a'],'exact left glue')
    require(row['source_state_reset'] is False and row['whole_cell_qualified'] and row['accepted'] and row['committed'],'whole cell/no reset')
    require(row['domain']['admitted'] and all(row['domain']['checks'].values()),'guard domain')
    require(th['source_saha_factor']==p['correct_saha_fact']==s['correct_saha_fact'],'source prefactor')
    require(all(th[k]==v for k,v in s['retained_theorem'].items()),'retained bounds/domain')
    require(Fraction(th['K_upper'])>0 and Fraction(th['connected_lower'])>0,'positive theorem bounds')
    # Endpoints come from the committed row; the supplied expected values only cross-check them.
    endpoint={'a':row['a1'],'E':row['E_right'],'Y':row['Y_right'],'Vbar':row['V_admitted']}
    require(endpoint==s['endpoint_crosscheck'],'endpoint crosscheck')
    c={'count':p['accepted_actual']['count']+1,'frontier':row['z1'],
       'frontiers':dict(p['frontiers'],**{'hillipop-ede_n3':row['z1']}),
       'endpoint':endpoint,'connected_lower':th['connected_lower'],'K_upper':th['K_upper']}
    r={'schema':'bubbleverse.q048.v121.source_correct_actual_consumer.raw.v1',
       'source_boundary_certificate':expected_boundary,'proof_validation_requirements':expected_counts,
       'q':'Q048','target_q':'Q048','task_id':s['task_id'],'task_fingerprint':s['task_fingerprint'],
       'program_id':s['program_id'],'program_registration':'LOCAL_NOT_REGISTERED',
       'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'status':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE',
       'exact_question':s['exact_question'],'question_sha256':s['question_sha256'],'spec_sha256':SPEC_HASH,
       'task_authorization_sha256':pins['Q048_V121_NEXT_BUILDER_TASK_V1.json'],'theorem_postaccept_sha256':pins['Q048_V120_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'],'authorization_sha256':pins['Q048_V120_INGESTION_STATE_V1.json'],
       'lineage':'SOURCE_CORRECT_REASSESSMENT_V104_V105_V106_V107_V108_V109_V110_V111_V112_V113_V114_V115_V116_V117_V118_V119_V120_V121',
       'cell_z':s['cell_z'],'cell_a':s['cell_a'],
       'parent_authority':{'record':parent_name,'sha256':pins[parent_name],'actual':p['accepted_actual'],'frontiers':p['frontiers'],'endpoint':p['endpoint']},
       'theorem_authority':{'record':theorem_name,'sha256':pins[theorem_name],'raw_sha256':t['raw_sha256'],'verification_sha256':t['verification_sha256'],'correct_saha_fact':th['source_saha_factor'],'thermal_domain':th['thermal_domain'],'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
       'guard_binding':{'source_record':'q048_guard_local_v_result_v12.json','source_record_sha256':pins['q048_guard_local_v_result_v12.json'],'primary_row_sha256':row_hash,'index':54,'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True,'control_role':'GUARD_ONLY'},
       'candidate_actual':c,'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,'theorem_consumptions':1,
       'below900_work':False,'historical_record_modified':False,'historical_v101_v102_replayed':False,
       'no_physical_reset':True,'no_native_trajectory_claim':True,'q_complete':False,'NativeP6':'UNRESOLVED',
       'claim_firewall':'One exact theorem-backed admission, not native trajectory integration, new proof or complete four-case xe/tau bounds.'}
    with output.open('x') as f: json.dump(r,f,indent=2);f.write('\n')
    print(output.name,sha(output),'actual118/frontier900; pending validation')

if __name__=='__main__':main()
