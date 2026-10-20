"""Read the written checkpoint independently; no producer/acceptor imports."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

PRE='Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_'

def S(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def L(p):return json.loads(Path(p).read_bytes())

def check(c,r,v,s,root):
    p=r['parent_authority'];t=r['theorem_authority'];g=r['guard_binding'];a=r['candidate_actual']
    return {
        'schema':c['schema']=='bubbleverse.q048.v119.source_correct_actual_consumer.accepted_checkpoint.v1',
        'identity':c['q']==c['target_q']=='Q048' and c['task_id']==s['task_id'] and c['task_fingerprint']==s['task_fingerprint'],
        'spec_pin':c['spec_sha256']==r['spec_sha256']==S(root/(PRE+'SPEC_V1.json')),
        'status':c['status']=='VALIDATED' and c['technical_state']=='PASS',
        'scientific_state':c['scientific_state']=='INCONCLUSIVE' and c['q_complete'] is False and c['NativeP6']=='UNRESOLVED',
        'raw_pin':c['source_result_sha256']==v['result_sha256']==S(root/(PRE+'RAW_V1.json')),
        'validation_pin':c['validation_sha256']==S(root/(PRE+'VALIDATION_V1.json')),
        'validation_pass':v['status']=='PASS' and v['checks_total']==v['checks_passed']==len(v['checks']) and all(v['checks'].values()),
        'real_mutations':v['semantic_mutations_total']==v['semantic_mutations_rejected']==len(v['mutation_failed_invariants'])==26 and all(v['mutation_failed_invariants'].values()),
        'parent_pin':c['parent_sha256']==p['sha256']==s['input_hashes'][p['record']],
        'actual_before':c['actual_before']=={'count':116,'frontier':920,'accepted_checkpoint_sha256':p['sha256']},
        'actual_after':c['accepted_actual']=={'count':117,'frontier':910} and c['accepted_actual']['count']==c['actual_before']['count']+1,
        'four_frontiers':c['frontiers']==a['frontiers']=={'camspec-lcdm':1440,'camspec-ede_n3':1440,'hillipop-lcdm':1440,'hillipop-ede_n3':910},
        'endpoint':c['endpoint']==a['endpoint']==s['endpoint_crosscheck'],
        'K':c['K_upper']==a['K_upper']==s['retained_theorem']['K_upper'],
        'lower':c['connected_lower']==a['connected_lower']==s['retained_theorem']['connected_lower'],
        'saha':c['correct_saha_fact']==t['correct_saha_fact']==s['correct_saha_fact'],
        'theorem_pin':c['theorem_acceptance_sha256']==t['sha256']==s['input_hashes'][t['record']],
        'theorem_raw_pin':c['theorem_raw_sha256']==t['raw_sha256'],
        'theorem_verifier_pin':c['theorem_verification_sha256']==t['verification_sha256'],
        'guard_source':c['guard_source_sha256']==g['source_record_sha256'],
        'guard_row':c['guard_primary_row_sha256']==g['primary_row_sha256']==s['row_sha256'],
        'authorization':c['authorization_sha256']==r['authorization_sha256'],
        'one_actual_zero_proof':c['new_actual_cells']==1 and c['new_mathematical_proof_cells']==c['new_full_theorem_recomputations']==0,
        'single_consumption':c['theorem_consumptions']==1,
        'no_reset':c['no_physical_reset'] is True,
        'history':c['historical_v101_v102_replayed'] is c['historical_record_modified'] is False,
        'no_below910':c['below910_work'] is False,
        'no_native_claim':c['no_native_trajectory_claim'] is True,
        'stop_rule':c['resume_rule']=='STOP at910. Return exactly once to Result Ingestion2.1.0; no below910 authorization.',
    }


def checkpoint_mutations(original):
    controls=[('wrong_parent',('parent_sha256',),'0'*64),('wrong_theorem',('theorem_acceptance_sha256',),'1'*64),('wrong_row',('guard_primary_row_sha256',),'2'*64),('reset',('no_physical_reset',),False),('below910',('accepted_actual','frontier'),900),('endpoint',('endpoint','E'),'1'),('extra_cell',('new_actual_cells',),2),('new_proof',('new_mathematical_proof_cells',),1)]
    result={}
    for name,path,value in controls:
        m=copy.deepcopy(original);target=m
        for k in path[:-1]:target=target[k]
        target[path[-1]]=value
        if m==original:raise ValueError('NO_OP_CHECKPOINT_MUTATION:'+name)
        result[name]=m
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args();root=args.out
    cp_path=root/(PRE+'ACCEPTED_CHECKPOINT_V1.json')
    c=L(cp_path);r=L(root/(PRE+'RAW_V1.json'));v=L(root/(PRE+'VALIDATION_V1.json'));s=L(root/(PRE+'SPEC_V1.json'))
    checks=check(c,r,v,s,root);mutations={}
    for name,m in checkpoint_mutations(c).items():
        mutations[name]=[k for k,val in check(m,r,v,s,root).items() if not val]
    passed=all(checks.values()) and all(mutations.values())
    report={'schema':'bubbleverse.q048.v119.source_correct_actual_consumer.postaccept_validation.v1','status':'PASS' if passed else 'FAIL','accepted_checkpoint_sha256':S(cp_path),'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'semantic_mutations_total':len(mutations),'semantic_mutations_rejected':sum(bool(x) for x in mutations.values()),'mutation_failed_invariants':mutations,'independence_scope':'Separate process and implementation read back checkpoint, raw, validation and spec; shares frozen premises.'}
    with (root/(PRE+'POSTACCEPT_VALIDATION_V1.json')).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(report['status'],sum(checks.values()),len(checks),'postaccept;',sum(bool(x) for x in mutations.values()),len(mutations),'checkpoint mutations rejected')
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
