"""Exact-identity four-job collection. No physical averaging or PASS promotion."""
import argparse, hashlib, json
from pathlib import Path
import q048_prefix_v1 as p
import q047_certificate_v1 as old

def collect(directory,config):
    directory=Path(directory);expected=set(p.CASES);reports={};raw_hashes={}
    for path in directory.rglob('*_prefix_v1.json'):
        if path.name=='q048_prefix_final_v1.json':continue
        r=old.load(path);case=r.get('configuration')
        if case not in expected:raise ValueError('UNKNOWN_CONFIGURATION')
        if case in reports:raise ValueError('DUPLICATE_CONFIGURATION')
        if r.get('q')!=p.Q or r.get('program_id')!=p.ID or r.get('version')!=p.VERSION:raise ValueError('MERGE_IDENTITY')
        if r.get('source_commit')!=p.SOURCE or r.get('scope')!=p.FINAL_SCOPE:raise ValueError('MERGE_SOURCE_SCOPE')
        if r.get('scientific_question')!=config['scientific_question']:raise ValueError('MERGE_QUESTION')
        if r.get('source_input_hashes')!=config['cases'][case]['source_input_hashes']:raise ValueError('MERGE_INPUT_HASHES')
        if r.get('final_result_gate')!='UNRESOLVED' or r.get('actual_source_admission')!='UNRESOLVED':raise ValueError('UNSUPPORTED_SCIENTIFIC_PASS')
        if r.get('q_assignment')!=config['q_assignment'] or r.get('case_id')!=config['case_id']:raise ValueError('MERGE_CASE_IDENTITY')
        if r.get('new_native_evaluations')!=0 or r.get('likelihood_evaluations')!=0:raise ValueError('EXECUTION_SCOPE_CHANGED')
        reports[case]=r;raw_hashes[case]=hashlib.sha256(path.read_bytes()).hexdigest()
    missing=sorted(expected-set(reports))
    contexts={(r.get('run_id'),r.get('executed_commit')) for r in reports.values()}
    if len(contexts)>1:raise ValueError('MERGE_RUN_COMMIT_COMPATIBILITY')
    complete=not missing and all(r['execution_status']=='COMPLETE' for r in reports.values())
    return {'schema':'Q048_PREFIX_FINAL_V1','q':p.Q,'q_assignment':config['q_assignment'],
        'case_id':config['case_id'],'program_id':p.ID,'version':p.VERSION,
        'scientific_question':config['scientific_question'],'question_sha256':config['question_sha256'],
        'execution_status':'COMPLETE' if complete else 'PARTIAL',
        'job_completeness_gate':'PASS' if complete else 'FAIL','missing_jobs':missing,
        'merge_compatibility_gate':'PASS','scope':p.FINAL_SCOPE,'raw_results':reports,
        'raw_sha256':raw_hashes,'final_result_gate':'UNRESOLVED',
        'actual_computed_result':'CONDITIONAL_PREFIX_CERTIFICATES_ONLY',
        'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
        'source_commit':p.SOURCE,'source_run_id':'38140371059',
        'return_route':'RESULT INGESTION & ROUTING ENGINE'}

def main():
    a=argparse.ArgumentParser();a.add_argument('--directory',required=True)
    a.add_argument('--config',default=str(p.ROOT/'q048_prefix_config_v1.json'))
    a.add_argument('--out',default='q048_prefix_final_v1.json');args=a.parse_args()
    result=collect(args.directory,p.validate_config(old.load(args.config)));old.write(args.out,result)
    print(json.dumps({k:result[k] for k in ('execution_status','job_completeness_gate','final_result_gate')}))
    return 0 if result['job_completeness_gate']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
