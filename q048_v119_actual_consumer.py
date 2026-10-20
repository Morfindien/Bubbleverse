"""One bounded admission of committed row53 under accepted V118 fresh theorem."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from fractions import Fraction

PREFIX='Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_'
SPEC_HASH='e1d3625668227a3ed4f5cd75eaa341ffa779bb42b3bc95521f1582cb3d6a928f'

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
    p=inp['Q048_V117_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json']
    t=inp['Q048_V118_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json']
    proof_post=inp['Q048_V118_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'];task=inp['Q048_V119_NEXT_BUILDER_TASK_V1.json']
    tr=inp['Q048_V118_SOURCE_CORRECT_PROOF_RAW_V1.json']
    tv=inp['Q048_V118_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json']
    g=inp['q048_guard_local_v_result_v12.json'];i=inp['Q048_V118_INGESTION_STATE_V1.json']
    row=g['evaluators'][0]['rows'][53]; th=t; pins=s['input_hashes']
    parent_name='Q048_V117_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
    theorem_name='Q048_V118_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json'
    require(p['status']=='VALIDATED' and p['accepted_actual']==s['actual_before'],'parent status/state')
    require(t['status']=='ACCEPTED' and t['technical_state']=='PASS','theorem status')
    require(t['parent_checkpoint_sha256']==pins[parent_name],'theorem parent identity')
    require(t['schema']=='bubbleverse.q048.v118.source_correct_proof.acceptance.v1' and t['mathematical_proof_accepted'] is True,'fresh proof schema')
    require(t['parent_actual']==p['accepted_actual'] and t['parent_endpoint']==p['endpoint'] and t['parent_connected_lower']==p['connected_lower'],'fresh theorem parent fields')
    require(t['proof_cell_z']==s['cell_z'] and t['proof_cell_a']==s['cell_a'],'theorem cell')
    require(tv['status']=='PASS' and tv['checks_total']==tv['checks_passed']==30 and all(tv['checks'].values()),'retained theorem validation')
    require(tv['raw_sha256']==t['raw_sha256']==pins['Q048_V118_SOURCE_CORRECT_PROOF_RAW_V1.json'],'theorem raw pin')
    require(t['verification_sha256']==pins['Q048_V118_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json'],'theorem verifier pin')
    require(tv['semantic_mutations_total']==tv['semantic_mutations_rejected']==16,'retained mutation status')
    require(tr['parent_checkpoint_sha256']==pins[parent_name] and tr['parent_actual']==p['accepted_actual'] and tr['K_upper']==t['K_upper'] and tr['hmin']==t['connected_lower'],'raw bridge consistency')
    require(i['next_task_id']==s['task_id'] and i['consumer_authorization']=='GRANTED_BY_INGESTION_FOR_EXACTLY_ONE_CELL_920_TO_910','downstream authorization')
    require(proof_post['status']=='PASS' and proof_post['accepted_checkpoint_sha256']==pins[theorem_name] and proof_post['checks_total']==proof_post['checks_passed']==20 and all(proof_post['checks'].values()),'theorem postaccept')
    require(task['task_id']==s['task_id'] and task['task_fingerprint']==s['task_fingerprint'] and task['parent_authority']['sha256']==pins[parent_name] and task['theorem_authority']['sha256']==pins[theorem_name],'bounded task binding')
    row_hash=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    require(row_hash==s['row_sha256'] and g['evaluators'][0]['control'] is False,'primary row hash')
    require(row['index']==53 and [row['z0'],row['z1']]==s['cell_z'] and [row['a0'],row['a1']]==s['cell_a'],'row cell')
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
    r={'schema':'bubbleverse.q048.v119.source_correct_actual_consumer.raw.v1',
       'q':'Q048','target_q':'Q048','task_id':s['task_id'],'task_fingerprint':s['task_fingerprint'],
       'program_id':s['program_id'],'program_registration':'LOCAL_NOT_REGISTERED',
       'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'status':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE',
       'exact_question':s['exact_question'],'question_sha256':s['question_sha256'],'spec_sha256':SPEC_HASH,
       'task_authorization_sha256':pins['Q048_V119_NEXT_BUILDER_TASK_V1.json'],'theorem_postaccept_sha256':pins['Q048_V118_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'],'authorization_sha256':pins['Q048_V118_INGESTION_STATE_V1.json'],
       'lineage':'SOURCE_CORRECT_REASSESSMENT_V104_V105_V106_V107_V108_V109_V110_V111_V112_V113_V114_V115_V116_V117_V118_V119',
       'cell_z':s['cell_z'],'cell_a':s['cell_a'],
       'parent_authority':{'record':parent_name,'sha256':pins[parent_name],'actual':p['accepted_actual'],'frontiers':p['frontiers'],'endpoint':p['endpoint']},
       'theorem_authority':{'record':theorem_name,'sha256':pins[theorem_name],'raw_sha256':t['raw_sha256'],'verification_sha256':t['verification_sha256'],'correct_saha_fact':th['source_saha_factor'],'thermal_domain':th['thermal_domain'],'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
       'guard_binding':{'source_record':'q048_guard_local_v_result_v12.json','source_record_sha256':pins['q048_guard_local_v_result_v12.json'],'primary_row_sha256':row_hash,'index':53,'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True,'control_role':'GUARD_ONLY'},
       'candidate_actual':c,'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,'theorem_consumptions':1,
       'below910_work':False,'historical_record_modified':False,'historical_v101_v102_replayed':False,
       'no_physical_reset':True,'no_native_trajectory_claim':True,'q_complete':False,'NativeP6':'UNRESOLVED',
       'claim_firewall':'One exact theorem-backed admission, not native trajectory integration, new proof or complete four-case xe/tau bounds.'}
    with output.open('x') as f: json.dump(r,f,indent=2);f.write('\n')
    print(output.name,sha(output),'actual117/frontier910; pending validation')

if __name__=='__main__':main()
