"""Accept only a pinned, separately validated V109 raw admission."""
import argparse
from datetime import datetime,timezone
from pathlib import Path
import json
import q048_v109_verify as verify

def main():
    ap=argparse.ArgumentParser(); here=Path(__file__).resolve().parent
    ap.add_argument('--inputs',type=Path,default=here.parent/'inputs');ap.add_argument('--out',type=Path,default=here)
    args=ap.parse_args(); root=args.out; pre=verify.PREFIX
    r=verify.load(root/(pre+'RAW_V1.json'));v=verify.load(root/(pre+'VALIDATION_V1.json'))
    authorities=verify.load_authorities(args.inputs)
    if verify.sha(root/verify.SPEC)!=verify.SPEC_HASH: raise ValueError('spec pin')
    if not (v['status']=='PASS' and v['result_sha256']==verify.sha(root/(pre+'RAW_V1.json'))
            and v['checks_total']==v['checks_passed']==len(v['checks']) and all(v['checks'].values())
            and v['semantic_mutations_total']==v['semantic_mutations_rejected']==24
            and all(v['mutations_rejected'].values()) and all(verify.check_result(r,authorities).values())):
        raise ValueError('acceptance validation gate')
    c=r['candidate_actual']
    cp={'schema':'bubbleverse.q048.v109.source_correct_actual_consumer.accepted_checkpoint.v1',
        'q':'Q048','target_q':'Q048','status':'VALIDATED','technical_state':'PASS','scientific_state':'INCONCLUSIVE',
        'checkpoint_kind':'ACCEPTED_ACTUAL_REANALYSIS_LINEAGE','task_id':r['task_id'],
        'task_fingerprint':r['task_fingerprint'],'spec_sha256':verify.SPEC_HASH,
        'actual_before':{'count':111,'frontier':970,'accepted_checkpoint_sha256':verify.PINS[verify.PARENT]},
        'accepted_actual':{'count':c['count'],'frontier':c['frontier']},
        'frontiers':c['frontiers'],'endpoint':c['endpoint'],'connected_lower':c['connected_lower'],'K_upper':c['K_upper'],
        'correct_saha_fact':r['theorem_authority']['correct_saha_fact'],
        'parent_sha256':verify.PINS[verify.PARENT],'theorem_acceptance_sha256':verify.PINS[verify.THEOREM],
        'theorem_raw_sha256':verify.PINS[verify.RAW],'theorem_verification_sha256':verify.PINS[verify.VER],
        'guard_source_sha256':verify.PINS[verify.GUARD],'guard_primary_row_sha256':verify.ROW_HASH,
        'authorization_sha256':verify.PINS[verify.INGEST],
        'source_result_sha256':verify.sha(root/(pre+'RAW_V1.json')),
        'validation_sha256':verify.sha(root/(pre+'VALIDATION_V1.json')),
        'accepted_at_utc':datetime.now(timezone.utc).isoformat(),
        'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,'theorem_consumptions':1,
        'historical_v101_v102_replayed':False,'historical_record_modified':False,'no_physical_reset':True,
        'no_native_trajectory_claim':True,'below960_work':False,'q_complete':False,'NativeP6':'UNRESOLVED',
        'resume_rule':'STOP at960. Return exactly once to Result Ingestion2.1.0; no below960 authorization.'}
    dest=root/(pre+'ACCEPTED_CHECKPOINT_V1.json')
    with dest.open('x') as f:json.dump(cp,f,indent=2);f.write('\n')
    print(dest.name,verify.sha(dest))

if __name__=='__main__':main()
