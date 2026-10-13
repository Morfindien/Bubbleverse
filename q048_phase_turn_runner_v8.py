"""Q048 V8 single-Camspec bounded worker and strict collector."""
from pathlib import Path
import argparse,copy,json,os,platform,time
import q048_phase_turn_v8 as e

old=e.old
proof=e.proof
REPORT_SIZE_CAP=24_000_000


def load_report(path):
    p=Path(path);e.fail(p.is_file(),'V8_REPORT_MISSING');e.fail(p.stat().st_size<=REPORT_SIZE_CAP,'V8_REPORT_SIZE_CAP')
    try:
        with p.open('r',encoding='utf-8') as f:obj=json.load(f)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise ValueError('V8_REPORT_JSON') from exc
    e.fail(isinstance(obj,dict),'V8_REPORT_OBJECT')
    return obj


def make_report(extension):
    s=e.settings()
    return {'schema':'Q048_PHASE_TURN_CASE_V8','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
            'scientific_question':s['scientific_question'],'question_sha256':s['question_sha256'],'program_id':e.ID,'version':e.VERSION,
            'scope':e.SCOPE,'source_commit':e.SOURCE,'configuration':'camspec-ede_n3','run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),
            'executed_commit':os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'),'config_hash':old.objhash(s),'extension':extension,
            'tests_status':'PROVISIONAL','actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED',
            'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'native_evaluations':0,'likelihood_evaluations':0,'python':platform.python_version(),
            'source_ids':['K-PROPOSED-Q048-SOURCE-002','K-PROPOSED-Q048-INPUT-001','K-PROPOSED-Q048-GITHUB-RUN-38293480870',
                          'K-PROPOSED-Q048-GITHUB-RUN-38348832247','I-PROPOSED-Q048-MATHEMATICS-007',
                          'I-PROPOSED-Q048-MATHEMATICS-008','I-PROPOSED-Q048-GUARDCONT-GITHUB-38348832247']}


def verify_report(r,parent,expected_run=None,full=False):
    s=e.settings();expected={'schema':'Q048_PHASE_TURN_CASE_V8','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
      'program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,'configuration':'camspec-ede_n3',
      'config_hash':old.objhash(s),'scientific_question':s['scientific_question'],'question_sha256':s['question_sha256'],
      'actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
      'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED','native_evaluations':0,'likelihood_evaluations':0}
    e.fail(all(r.get(k)==v for k,v in expected.items()),'REPORT_IDENTITY')
    run=r.get('run_id');e.fail(isinstance(run,str) and (run=='LOCAL' or run.isdigit()),'REPORT_RUN')
    e.fail(expected_run is None or run==str(expected_run),'REPORT_EXPECTED_RUN')
    e.fail(r['source_ids']==make_report(r['extension'])['source_ids'],'SOURCE_REGISTER')
    x=r['extension'];e.fail(x['q']==e.Q and x['program_id']==e.ID and x['configuration']=='camspec-ede_n3','EXTENSION_BINDING')
    if full:
        v=e.verify_extension(x,parent)
        e.fail(r.get('post_verification')==v,'POST_VERIFICATION_RECOMPUTE')
        return {'gate':'PASS_FULL_RECOMPUTE','extension':v}
    e.fail(r.get('tests_status') in ('PROVISIONAL','COMPLETE_CONDITIONAL'),'REPORT_TEST_STATUS')
    return {'gate':'PASS_BINDINGS'}


def run(parent_path,out):
    start=time.monotonic();e.validate_sources();parent=e.load_parent(parent_path);ext=e.derive(parent);r=make_report(ext)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    proof.write(out/'camspec-ede_n3_phase_turn_raw_v8.json',r)
    post=e.verify_extension(ext,parent);r['post_verification']=post;r['tests_status']='COMPLETE_CONDITIONAL';r['stage']='FINAL_BOUNDED_COMPONENT';r['elapsed_seconds']=time.monotonic()-start
    proof.write(out/'camspec-ede_n3_phase_turn_v8.json',r)
    print(json.dumps({'case':'camspec-ede_n3','phase_turn_status':ext['phase_turn']['status'],'thermal_status':ext['thermal']['status'],
                      'phase_cells':ext['phase_turn']['cell_count'],'elapsed_seconds':r['elapsed_seconds'],'final_result_gate':'UNRESOLVED'}),flush=True)
    return r


def collect(directory,parent_path,expected_run=None,full=False):
    e.validate_sources();parent=e.load_parent(parent_path);reports=[]
    for path in Path(directory).rglob('camspec-ede_n3_phase_turn_v8.json'):
        reports.append(load_report(path))
    e.fail(len(reports)==1,'JOB_COMPLETENESS')
    r=reports[0];verify_report(r,parent,expected_run=expected_run,full=full)
    ext=r['extension'];guard_pass=ext['phase_turn']['status']=='PASS_CONDITIONAL_PHASE_TURN_GUARD'
    thermal_pass=ext['thermal']['status']=='PASS_CONDITIONAL_TO_H_ENTRY'
    final={'schema':'Q048_PHASE_TURN_FINAL_V8','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':e.ID,
           'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,'scientific_question':e.settings()['scientific_question'],
           'question_sha256':e.settings()['question_sha256'],'execution_status':'COMPLETE','job_completeness_gate':'PASS',
           'merge_compatibility_gate':'PASS','phase_turn_guard_gate':'PASS_CONDITIONAL' if guard_pass else'UNRESOLVED',
           'thermal_h_entry_gate':'PASS_CONDITIONAL' if thermal_pass else'UNRESOLVED','tests_status':'COMPLETE_CONDITIONAL',
           'final_result_gate':'UNRESOLVED','actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
           'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED','camspec_record':r,
           'retained_parent_hillipop':copy.deepcopy(parent['records']['hillipop-ede_n3']),
           'retained_parent_lcdm':copy.deepcopy(parent['retained_lcdm']),
           'parent_v7':{'run_id':e.settings()['parent_v7']['run_id'],'raw_sha256':e.settings()['parent_v7']['raw_sha256'],
                        'executed_commit':e.settings()['parent_v7']['executed_commit']},
           'job_manifest':{'q':e.Q,'program_id':e.ID,'run_id':r['run_id'],'expected_jobs':['camspec-ede_n3'],
                           'completed_jobs':['camspec-ede_n3'],'failed_jobs':[],'pending_jobs':[]},
           'return_route':'RESULT INGESTION & ROUTING ENGINE'}
    return final


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--program-id',default=e.ID);ap.add_argument('--parent',required=True)
    ap.add_argument('--out',default='q048_phase_turn_results');ap.add_argument('--collect');ap.add_argument('--expected-run');ap.add_argument('--full-verify',action='store_true')
    a=ap.parse_args();e.fail(a.program_id==e.ID,'PROGRAM_ID_GATE')
    if a.collect:
        r=collect(a.collect,a.parent,expected_run=a.expected_run,full=a.full_verify);proof.write(a.out,r)
        print(json.dumps({k:r[k] for k in ('execution_status','job_completeness_gate','phase_turn_guard_gate','thermal_h_entry_gate','final_result_gate')}))
    else:run(a.parent,a.out)

if __name__=='__main__':main()
