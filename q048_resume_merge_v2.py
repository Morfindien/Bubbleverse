"""Complete four-case collection with exact checkpoint compatibility."""
from pathlib import Path
import argparse,json
import q048_resume_v2 as e

def collect(directory):
    records={};checkpoints={}
    settings=e.load(e.ROOT/'q048_resume_config_v2.json')
    config=e.p.validate_config(e.load(e.ROOT/'q048_prefix_config_v1.json'))
    for path in Path(directory).rglob('*_checkpoint_v2.json'):
        x=e.load(path);m=x['metadata'];r=x['record'];case=m['case']
        if case not in e.p.CASES or case in records:raise ValueError('MERGE_CASE_DUPLICATE_OR_UNKNOWN')
        if x.get('schema')!='Q048_CHECKPOINT_V2' or m['q']!=e.Q or m['program_id']!=e.ID or m['source_commit']!=e.SOURCE or r['program_id']!=e.ID or r['configuration']!=case or r['final_result_gate']!='UNRESOLVED':raise ValueError('MERGE_IDENTITY_SCOPE')
        if (r.get('scope')!=e.p.FINAL_SCOPE or r.get('actual_source_admission')!='UNRESOLVED'
            or r.get('q_assignment')!='PROPOSED_UNVERIFIED' or r.get('case_id')!='NOT_ASSIGNED'
            or r.get('scientific_question')!=config['scientific_question']
            or r.get('source_input_hashes')!=config['cases'][case]['source_input_hashes']):raise ValueError('MERGE_SCIENTIFIC_SCOPE')
        if (m['config_hash']!=e.objhash(settings) or m['source_config_hash']!=settings['source_config_sha256']
            or m['background_end_a']!=r['background']['certified_end_a']
            or m['thermal_end_a']!=r['thermal'].get('certified_end_a')):raise ValueError('MERGE_CHECKPOINT_CONFIG_CURSOR')
        if m['stage']!='FINAL_CONDITIONAL_COMPONENT':raise ValueError('CASE_REPORT_INCOMPLETE')
        records[case]=r;checkpoints[case]={'sha256':e.digest(path),'metadata':m}
    missing=sorted(set(e.p.CASES)-set(records))
    contexts={(m['metadata']['run_id'],m['metadata']['config_hash'],m['metadata']['source_config_hash']) for m in checkpoints.values()}
    if len(contexts)>1:raise ValueError('MERGE_RUN_CONFIG_COMPATIBILITY')
    return {'schema':'Q048_RESUME_FINAL_V2','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
            'program_id':e.ID,'version':'v2','source_commit':e.SOURCE,
            'execution_status':'PARTIAL' if missing else 'COMPLETE','missing_jobs':missing,
            'job_completeness_gate':'FAIL' if missing else 'PASS','merge_compatibility_gate':'PASS',
            'final_result_gate':'UNRESOLVED','scope':e.p.FINAL_SCOPE,
            'actual_event_redshifts':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'records':records,'checkpoints':checkpoints,'return_route':'RESULT INGESTION & ROUTING ENGINE'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',required=True);p.add_argument('--out',default='q048_resume_final_v2.json');a=p.parse_args()
    result=collect(a.directory);e.p.old.write(a.out,result)
    print(json.dumps({k:result[k] for k in ('execution_status','job_completeness_gate','final_result_gate')}))
    if result['missing_jobs']:raise SystemExit(2)
