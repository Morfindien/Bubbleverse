"""Collect four fully rechecked conditional reports, preserving raw chains."""
from pathlib import Path
import argparse,json
from concurrent.futures import ProcessPoolExecutor
import q048_resume_v5 as e

def verify_collected(case,record,row,seconds):
    report,_=e.verify_record(record,row,e.p.parameters(row),seconds)
    return case,report

def collect(directory):
    settings=e.load(e.ROOT/'q048_resume_config_v5.json')
    cfg=e.p.validate_config(e.load(e.ROOT/settings['source_config_file']))
    records={};checkpoints={};partial={};incomplete={};seen=set()
    for path in Path(directory).rglob('*_checkpoint_v5.json'):
        x=e.load(path);m=x['metadata'];r=x['record'];case=m['case']
        if case not in e.p.CASES or case in seen:raise ValueError('MERGE_CASE_DUPLICATE_OR_UNKNOWN')
        seen.add(case)
        e.validate_checkpoint(x,case,settings)
        if (r.get('scope')!=e.p.FINAL_SCOPE or r.get('q_assignment')!='PROPOSED_UNVERIFIED'
            or r.get('case_id')!='NOT_ASSIGNED' or r.get('actual_source_admission')!='UNRESOLVED'
            or r.get('final_result_gate')!='UNRESOLVED' or r.get('scientific_question')!=cfg['scientific_question']
            or r.get('source_input_hashes')!=cfg['cases'][case]['source_input_hashes']
            or any(r.get(k)!='NOT_COMPUTED' for k in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds'))):
            raise ValueError('MERGE_SCIENTIFIC_SCOPE')
        checkpoints[case]={'sha256':e.digest(path),'metadata':m}
        if m.get('stage')!='FINAL_CONDITIONAL_COMPONENT':
            partial[case]=r;incomplete[case]='FINAL_STAGE_NOT_REACHED:'+str(m.get('stage'))
            continue
        for stage,n in r['inherited_counts'].items():
            if (stage not in ('background','thermal') or type(n) is not int or n<0
                or n>len(r[stage]['cells']) or e.objhash(r[stage]['cells'][:n])!=r['inherited_cells_hashes'][stage]):
                raise ValueError('MERGE_INHERITED_CERTIFICATES')
        records[case]=r
    # Recompute every root/cell proof independently of stored flags and payload hashes.
    verified={}
    if records:
        with ProcessPoolExecutor(max_workers=min(4,len(records))) as pool:
            futures=[pool.submit(verify_collected,case,r,cfg['cases'][case],settings['verification_seconds'])
                     for case,r in records.items()]
            for f in futures:
                case,report=f.result();verified[case]=report
    missing=sorted(set(e.p.CASES)-set(records))
    contexts={(x['metadata']['run_id'],x['metadata']['config_hash'],x['metadata']['source_config_hash']) for x in checkpoints.values()}
    if len(contexts)>1:raise ValueError('MERGE_RUN_CONFIG_COMPATIBILITY')
    return {'schema':'Q048_RESUME_FINAL_V5','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
            'scientific_question':cfg['scientific_question'],'question_sha256':cfg['question_sha256'],
            'program_id':e.ID,'version':e.VERSION,'source_commit':e.SOURCE,'config_hash':e.objhash(settings),
            'execution_status':'PARTIAL' if missing else 'COMPLETE','missing_jobs':missing,
            'job_completeness_gate':'FAIL' if missing else 'PASS','merge_compatibility_gate':'PASS',
            'tests_status':'PARTIAL' if missing else 'COMPLETE_CONDITIONAL',
            'final_result_gate':'UNRESOLVED','scope':e.p.FINAL_SCOPE,'actual_source_admission':'UNRESOLVED',
            'actual_event_redshifts':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'records':records,'partial_records':partial,'incomplete_cases':incomplete,
            'job_manifest':{'q':e.Q,'program_id':e.ID,'run_id':next(iter(contexts))[0] if contexts else None,
                            'expected_jobs':list(e.p.CASES),'completed_jobs':sorted(records),'failed_jobs':sorted(incomplete),'pending_jobs':missing},
            'merge_verification':verified,'checkpoints':checkpoints,'return_route':'RESULT INGESTION & ROUTING ENGINE'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',required=True);p.add_argument('--out',default='q048_resume_final_v5.json');a=p.parse_args()
    result=collect(a.directory);e.p.old.write(a.out,result)
    print(json.dumps({k:result[k] for k in ('execution_status','job_completeness_gate','tests_status','final_result_gate')}))
    if result['missing_jobs']:raise SystemExit(2)
