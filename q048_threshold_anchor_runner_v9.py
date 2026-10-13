"""Q048 V9 single-Camspec finite threshold-anchor worker and strict collector."""
from pathlib import Path
import argparse, copy, json, os, platform, time

import q048_threshold_anchor_v9 as e

proof=e.proof
REPORT_SIZE_CAP=16_000_000


def load_report(path):
    p=Path(path)
    e.fail(p.is_file(),'V9_REPORT_MISSING')
    e.fail(p.stat().st_size<=REPORT_SIZE_CAP,'V9_REPORT_SIZE_CAP')
    try:
        with p.open('r',encoding='utf-8') as f:
            obj=json.load(f)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise ValueError('V9_REPORT_JSON') from exc
    e.fail(isinstance(obj,dict),'V9_REPORT_OBJECT')
    return obj


def make_report(extension):
    s=e.settings()
    return {'schema':'Q048_THRESHOLD_ANCHOR_CASE_V9','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED',
            'case_id':'NOT_ASSIGNED','scientific_question':s['scientific_question'],
            'question_sha256':s['question_sha256'],'program_id':e.ID,'version':e.VERSION,
            'scope':e.SCOPE,'source_commit':e.SOURCE,'configuration':'camspec-ede_n3',
            'run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),
            'executed_commit':os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'),
            'config_hash':e.old.objhash(s),'extension':extension,'tests_status':'PROVISIONAL',
            'actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED',
            'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED',
            'actual_tau_T_bounds':'NOT_COMPUTED','native_evaluations':0,'likelihood_evaluations':0,
            'python':platform.python_version(),
            'source_ids':['K-PROPOSED-Q048-SOURCE-002','K-PROPOSED-Q048-INPUT-001',
                          'K-PROPOSED-Q048-GITHUB-RUN-38293480870',
                          'K-PROPOSED-Q048-GITHUB-RUN-38348832247',
                          'K-PROPOSED-Q048-GITHUB-RUN-38361759433',
                          'I-PROPOSED-Q048-MATHEMATICS-008',
                          'I-PROPOSED-Q048-MATHEMATICS-009',
                          'I-PROPOSED-Q048-PHASETURN-GITHUB-38361759433']}


def verify_report(r,v6_parent,v7_parent,v8_parent,expected_run=None,full=False):
    s=e.settings()
    expected={'schema':'Q048_THRESHOLD_ANCHOR_CASE_V9','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED',
              'case_id':'NOT_ASSIGNED','program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,
              'source_commit':e.SOURCE,'configuration':'camspec-ede_n3',
              'config_hash':e.old.objhash(s),'scientific_question':s['scientific_question'],
              'question_sha256':s['question_sha256'],'actual_source_admission':'UNRESOLVED',
              'final_result_gate':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
              'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
              'native_evaluations':0,'likelihood_evaluations':0}
    e.fail(all(r.get(k)==v for k,v in expected.items()),'REPORT_IDENTITY')
    run=r.get('run_id')
    e.fail(isinstance(run,str) and (run=='LOCAL' or run.isdigit()),'REPORT_RUN')
    e.fail(expected_run is None or run==str(expected_run),'REPORT_EXPECTED_RUN')
    e.fail(r['source_ids']==make_report(r['extension'])['source_ids'],'SOURCE_REGISTER')
    x=r['extension']
    e.fail(x['q']==e.Q and x['program_id']==e.ID and x['configuration']=='camspec-ede_n3','EXTENSION_BINDING')
    if full:
        v=e.verify_extension(x,v6_parent,v7_parent,v8_parent)
        e.fail(r.get('post_verification')==v,'POST_VERIFICATION_RECOMPUTE')
        return {'gate':'PASS_FULL_RECOMPUTE','extension':v}
    e.fail(r.get('tests_status') in ('PROVISIONAL','COMPLETE_CONDITIONAL'),'REPORT_TEST_STATUS')
    if r.get('tests_status')=='COMPLETE_CONDITIONAL':
        e.fail(r.get('post_verification',{}).get('gate')=='PASS_RECOMPUTED_V9_EXTENSION','REPORT_POST_VERIFICATION')
    return {'gate':'PASS_BINDINGS'}


def run(v6_path,v7_path,v8_path,out):
    start=time.monotonic();out=Path(out);out.mkdir(parents=True,exist_ok=True)
    try:
        e.validate_sources()
        p6=e.load_v6(v6_path);p7=e.load_v7(v7_path);p8=e.load_v8(v8_path)
        ext=e.derive(p6,p7,p8);r=make_report(ext)
        proof.write(out/'camspec-ede_n3_threshold_anchor_raw_v9.json',r)
        post=e.verify_extension(ext,p6,p7,p8)
        r['post_verification']=post;r['tests_status']='COMPLETE_CONDITIONAL'
        r['stage']='FINAL_BOUNDED_COMPONENT';r['elapsed_seconds']=time.monotonic()-start
        proof.write(out/'camspec-ede_n3_threshold_anchor_v9.json',r)
        cert=ext['certificate'];therm=ext['thermal']
        print(json.dumps({'case':'camspec-ede_n3','certificate_status':cert['status'],
                          'energy_gate':cert['energy_map_32']['gate'],
                          'timing_gate':cert['timing_sum_32']['gate'],
                          'thermal_status':therm['status'],
                          'h_entry_q':therm['h_entry_q'],
                          'elapsed_seconds':r['elapsed_seconds'],
                          'final_result_gate':'UNRESOLVED'}),flush=True)
        return r
    except Exception as exc:
        failure={'schema':'Q048_THRESHOLD_ANCHOR_TECHNICAL_FAILURE_V9','q':e.Q,'program_id':e.ID,
                 'failure_class':'SOFTWARE_OR_NUMERICAL_EXCEPTION','exception_type':type(exc).__name__,
                 'message':str(exc),'elapsed_seconds':time.monotonic()-start,
                 'scientific_result_available':False,'final_result_gate':'UNRESOLVED'}
        proof.write(out/'camspec-ede_n3_threshold_anchor_failure_v9.json',failure)
        raise


def collect(directory,v6_path,v7_path,v8_path,expected_run=None,full=False):
    e.validate_sources();p6=e.load_v6(v6_path);p7=e.load_v7(v7_path);p8=e.load_v8(v8_path)
    reports=[load_report(x) for x in Path(directory).rglob('camspec-ede_n3_threshold_anchor_v9.json')]
    e.fail(len(reports)==1,'JOB_COMPLETENESS')
    r=reports[0];verify_report(r,p6,p7,p8,expected_run=expected_run,full=full)
    ext=r['extension']
    cert_pass=ext['certificate']['status']=='PASS_CONDITIONAL_THRESHOLD_ANCHOR_GUARD'
    thermal_pass=ext['thermal']['status']=='PASS_CONDITIONAL_TO_H_ENTRY'
    final={'schema':'Q048_THRESHOLD_ANCHOR_FINAL_V9','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED',
           'case_id':'NOT_ASSIGNED','program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,
           'source_commit':e.SOURCE,'scientific_question':e.settings()['scientific_question'],
           'question_sha256':e.settings()['question_sha256'],'execution_status':'COMPLETE',
           'job_completeness_gate':'PASS','merge_compatibility_gate':'PASS',
           'threshold_anchor_guard_gate':'PASS_CONDITIONAL' if cert_pass else'UNRESOLVED',
           'thermal_h_entry_gate':'PASS_CONDITIONAL' if thermal_pass else'UNRESOLVED',
           'tests_status':'COMPLETE_CONDITIONAL','final_result_gate':'UNRESOLVED',
           'actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
           'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
           'camspec_record':r,'retained_parent_hillipop':copy.deepcopy(ext['retained_parent_hillipop']),
           'retained_parent_lcdm':copy.deepcopy(ext['retained_parent_lcdm']),
           'parents':{'v6':{'run_id':e.settings()['parent_v6']['run_id'],'raw_sha256':e.settings()['parent_v6']['raw_sha256']},
                      'v7':{'run_id':e.settings()['parent_v7']['run_id'],'raw_sha256':e.settings()['parent_v7']['raw_sha256']},
                      'v8':{'run_id':e.settings()['parent_v8']['run_id'],'raw_sha256':e.settings()['parent_v8']['raw_sha256']}},
           'job_manifest':{'q':e.Q,'program_id':e.ID,'run_id':r['run_id'],
                           'expected_jobs':['camspec-ede_n3'],'completed_jobs':['camspec-ede_n3'],
                           'failed_jobs':[],'pending_jobs':[]},
           'return_route':'RESULT INGESTION & ROUTING ENGINE'}
    return final


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--program-id',default=e.ID)
    ap.add_argument('--v6-parent',required=True)
    ap.add_argument('--v7-parent',required=True)
    ap.add_argument('--v8-parent',required=True)
    ap.add_argument('--out',default='q048_threshold_anchor_results')
    ap.add_argument('--collect')
    ap.add_argument('--expected-run')
    ap.add_argument('--full-verify',action='store_true')
    a=ap.parse_args()
    e.fail(a.program_id==e.ID,'PROGRAM_ID_GATE')
    if a.collect:
        r=collect(a.collect,a.v6_parent,a.v7_parent,a.v8_parent,expected_run=a.expected_run,full=a.full_verify)
        proof.write(a.out,r)
        print(json.dumps({k:r[k] for k in ('execution_status','job_completeness_gate',
                                           'threshold_anchor_guard_gate','thermal_h_entry_gate',
                                           'final_result_gate')}))
    else:
        run(a.v6_parent,a.v7_parent,a.v8_parent,a.out)

if __name__=='__main__':
    main()
