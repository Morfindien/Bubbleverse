"""Accept one V114 mathematical proof; never advance actual state."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import json,hashlib,argparse

P='Q048_V114_SOURCE_CORRECT_PROOF_'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args();r=args.root
    raw=load(r/(P+'RAW_V1.json'));v=load(r/(P+'VERIFICATION_V1.json'));s=load(r/(P+'SPEC_V1.json'))
    parent_path=r/'inputs/Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json';parent=load(parent_path)
    if not(v['status']=='PASS' and v['verification_pass'] is True and v['checks_total']==v['checks_passed'] and all(v['checks'].values()) and v['raw_sha256']==sha(r/(P+'RAW_V1.json')) and v['semantic_mutations_total']==v['semantic_mutations_rejected']==16):raise ValueError('VALIDATION_REQUIRED')
    if not(raw['status']=='CANDIDATE_PROOF' and raw['parent_checkpoint_sha256']==sha(parent_path) and raw['cell_z']==[940,930] and raw['actual_state_unchanged']==parent['accepted_actual']=={'count':114,'frontier':940} and raw['new_actual_cells']==0 and raw['new_mathematical_proof_cells']==0 and F(raw['K_upper'])>0 and F(raw['hmin'])>0):raise ValueError('ACCEPTANCE_DOMAIN')
    cp={'schema':'bubbleverse.q048.v114.source_correct_proof.acceptance.v1','q':'Q048','target_q':'Q048','task_id':s['task_id'],'task_fingerprint':s['task_fingerprint'],'status':'ACCEPTED','mathematical_proof_accepted':True,'technical_state':'PASS','scientific_state':'INCONCLUSIVE','accepted_at_utc':datetime.now(timezone.utc).isoformat(),'proof_cell_z':[940,930],'proof_cell_a':['1/941','1/931'],'parent_checkpoint':parent_path.name,'parent_checkpoint_sha256':sha(parent_path),'parent_actual':parent['accepted_actual'],'parent_endpoint':parent['endpoint'],'parent_connected_lower':parent['connected_lower'],'guard_primary_index':51,'guard_primary_row_sha256':s['guard_primary_row_sha256'],'source_saha_factor':'3.016103031869581e21','source_commit':s['source_commit'],'capture_sha256':s['capture_sha256'],'K_upper':raw['K_upper'],'connected_lower':raw['hmin'],'thermal_domain':raw['thermal_domain'],'raw_sha256':sha(r/(P+'RAW_V1.json')),'verification_sha256':sha(r/(P+'VERIFICATION_V1.json')),'spec_sha256':sha(r/(P+'SPEC_V1.json')),'freeze_sha256':sha(r/(P+'FREEZE_V1.json')),'new_mathematical_proof_cells':1,'new_actual_cells':0,'actual_state_unchanged':parent['accepted_actual'],'consumer_authorization':'NOT_GRANTED','below930_authorization':'NOT_GRANTED','source_state_reset':False,'historical_record_modified':False,'historical_v101_v102_v108_replayed':False,'q_complete':False,'NativeP6':'UNRESOLVED','proof_scope':'ONE_NEW_SOURCE_CORRECT_CONNECTED_CELL_ON_ACCEPTED_V113_PARENT; shared physical/helper premises, no native trajectory claim','return_route':'RESULT_INGESTION_ROUTING2.1.0'}
    dest=r/(P+'ACCEPTANCE_V1.json')
    with dest.open('x') as f:json.dump(cp,f,indent=2);f.write('\n')
    readback=load(dest)
    checks={'accepted':readback['status']=='ACCEPTED','cp_exact_readback':readback==cp,'parent_pin':readback['parent_checkpoint_sha256']==sha(parent_path),'actual_unchanged':readback['actual_state_unchanged']=={'count':114,'frontier':940},'zero_actual':readback['new_actual_cells']==0,'one_proof':readback['new_mathematical_proof_cells']==1,'cell':readback['proof_cell_z']==[940,930],'row51':readback['guard_primary_index']==51,'source_correct':readback['source_saha_factor']=='3.016103031869581e21','positive_K':F(readback['K_upper'])>0,'positive_lower':F(readback['connected_lower'])>0,'raw_pin':readback['raw_sha256']==sha(r/(P+'RAW_V1.json')),'verifier_pin':readback['verification_sha256']==sha(r/(P+'VERIFICATION_V1.json')),'spec_pin':readback['spec_sha256']==sha(r/(P+'SPEC_V1.json')),'freeze_pin':readback['freeze_sha256']==sha(r/(P+'FREEZE_V1.json')),'no_consumer':readback['consumer_authorization']=='NOT_GRANTED','no_below930':readback['below930_authorization']=='NOT_GRANTED','history_unchanged':readback['historical_record_modified'] is False,'no_reset':readback['source_state_reset'] is False,'not_Q_complete':readback['q_complete'] is False}
    post={'schema':'bubbleverse.q048.v114.source_correct_proof.postaccept.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'accepted_checkpoint_sha256':sha(dest),'scope':'Exact acceptance disk readback / provenance / scope. Mathematical recomputation performed by separate verifier.'}
    with (r/(P+'POSTACCEPT_V1.json')).open('x') as f:json.dump(post,f,indent=2);f.write('\n')
    print(json.dumps({'accepted_sha256':sha(dest),'postaccept':post['status'],'checks_passed':sum(checks.values()),'checks_total':len(checks)}))
    if post['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
