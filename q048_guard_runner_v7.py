"""Q048 V7 two-EDE finite workers, atomic progress, strict collection."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,json,os,platform,time
import q048_guard_continuation_v7 as e
old=e.old;proof=e.proof;v6=e.v6
CASES=tuple(e.settings()['thermal']['cases'])

def progress_writer(path,case):
 path=Path(path)
 def emit(cells,now,current,attempts):
  obj={'schema':'Q048_GUARD_PROGRESS_V7','q':e.Q,'program_id':e.ID,'case':case,'run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),
   'certified_end_a':str(now),'endpoint':[proof.pairs(x) for x in current],'cell_count':len(cells),'attempts':attempts,
   'cells':copy.deepcopy(cells),'status':'PROVISIONAL_PROGRESS_NOT_SCIENTIFIC_FINAL'}
  proof.write(path,obj)
 return emit

def make_report(case,extension):
 s=e.settings();return {'schema':'Q048_GUARD_CASE_V7','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
  'scientific_question':s['scientific_question'],'question_sha256':s['question_sha256'],'program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,
  'source_commit':e.SOURCE,'configuration':case,'run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),
  'executed_commit':os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'),'config_hash':old.objhash(s),'extension':extension,
  'tests_status':'PROVISIONAL','actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED',
  'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
  'native_evaluations':0,'likelihood_evaluations':0,'python':platform.python_version(),
  'source_ids':['K-PROPOSED-Q048-SOURCE-002','K-PROPOSED-Q048-INPUT-001','K-PROPOSED-Q048-GITHUB-RUN-38293480870',
   'I-PROPOSED-Q048-MATHEMATICS-007','I-PROPOSED-Q048-STRUCTURAL-GITHUB-38293480870']}

def verify_report(r,expected_run=None,full=False):
 s=e.settings();case=r.get('configuration');e.fail(case in CASES,'REPORT_CASE')
 expected={'schema':'Q048_GUARD_CASE_V7','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':e.ID,
  'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,'configuration':case,'config_hash':old.objhash(s),
  'scientific_question':s['scientific_question'],'question_sha256':s['question_sha256'],'actual_source_admission':'UNRESOLVED',
  'final_result_gate':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
  'native_evaluations':0,'likelihood_evaluations':0}
 e.fail(all(r.get(k)==v for k,v in expected.items()),'REPORT_IDENTITY')
 run=r.get('run_id');e.fail(isinstance(run,str) and (run=='LOCAL' or run.isdigit()),'REPORT_RUN')
 e.fail(expected_run is None or run==str(expected_run),'REPORT_EXPECTED_RUN')
 tmpl=make_report(case,r['extension']);e.fail(r['source_ids']==tmpl['source_ids'],'SOURCE_REGISTER')
 if full:e.verify_extension(case,r['extension'])
 else:
  x=r['extension'];e.fail(x['configuration']==case and x['actual_source_admission']=='UNRESOLVED' and x['final_result_gate']=='UNRESOLVED','EXTENSION_SCOPE')
 return {'gate':'PASS_FULL_RECOMPUTE' if full else'PASS_BINDINGS','configuration':case}

def run(case,out,resume=None):
 start=time.monotonic();e.validate_sources();out=Path(out);out.mkdir(parents=True,exist_ok=True)
 progress=progress_writer(out/(case+'_progress_v7.json'),case) if case=='camspec-ede_n3' else None
 seed=None
 if resume:
  seed=old.load(resume);e.fail(seed.get('case')==case and seed.get('program_id')==e.ID,'RESUME_IDENTITY')
  row=e.v6.config()['cases'][case];t=e.v6.p.parameters(row);_,a0,state0=e.v6.p.source_initial(row,t)
  cells=seed['cells'];margins=[F(c['guard']['margin'][0]) for c in cells];ratios=[F(c['guard']['ratio'][1]) for c in cells]
  seed={'method':e.settings()['guard']['method'],'status':'UNRESOLVED_BOUNDED_OBSTRUCTION','requested_end_a':e.settings()['guard']['target_a'],
   'certified_end_a':seed['certified_end_a'],'initial_a':str(a0.lo),
   'initial_state':[proof.pairs(x) for x in state0],
   'cells':cells,'cell_count':len(cells),'attempts':seed['attempts'],'endpoint':seed['endpoint'],'blocker':'RESUME_SEED',
   'minimum_guard_margin_lower':str(min(margins)) if margins else None,
   'maximum_direct_ratio_interval_upper_diagnostic':str(max(ratios)) if ratios else None,
   'guard_acceptance':'EQUIVALENT_POSITIVE_MARGIN_ON_EVERY_CERTIFIED_WHOLE_STATE_CELL','actual_source_admission':'UNRESOLVED'}
 ext=e.derive(case,progress=progress,resume=seed);r=make_report(case,ext);r['tests_status']='COMPLETE_CONDITIONAL';r['stage']='FINAL_BOUNDED_COMPONENT';r['elapsed_seconds']=time.monotonic()-start
 proof.write(out/(case+'_guard_v7.json'),r);proof.write(out/(case+'_checkpoint_v7.json'),r)
 print(json.dumps({'case':case,'guard_status':ext['guard']['status'],'thermal_status':ext['thermal']['status'],'elapsed_seconds':r['elapsed_seconds'],'final_result_gate':'UNRESOLVED'}),flush=True)
 return r

def collect(directory,expected_run=None,full=False):
 e.validate_sources();reports={};contexts=set()
 for path in Path(directory).rglob('*_guard_v7.json'):
  r=old.load(path);case=r.get('configuration');e.fail(case in CASES and case not in reports,'MERGE_DUPLICATE_OR_UNKNOWN')
  verify_report(r,expected_run=expected_run,full=full);reports[case]=r;contexts.add((r['run_id'],r['executed_commit'],r['config_hash']))
 e.fail(len(contexts)<=1,'MERGE_CONTEXT');missing=sorted(set(CASES)-set(reports));complete=not missing
 retained={}
 for case in e.settings()['retained_lcdm_cases']:
  parent=v6.parent_checkpoint(case);x=v6.derive(case,parent);retained[case]={'parent_record_sha256':old.objhash(parent['record']),
   'status':x['status'],'thermal_onset_w':parent['record']['thermal'].get('onset_w'),'thermal_onset_q':parent['record']['thermal'].get('onset_q')}
 guard_pass=complete and reports['camspec-ede_n3']['extension']['guard']['status']=='PASS_CONDITIONAL_DIRECT_GUARD'
 thermal_pass=complete and all(reports[c]['extension']['thermal']['status']=='PASS_CONDITIONAL_TO_H_ENTRY' for c in CASES)
 return {'schema':'Q048_GUARD_FINAL_V7','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':e.ID,'version':e.VERSION,
  'scope':e.SCOPE,'source_commit':e.SOURCE,'scientific_question':e.settings()['scientific_question'],'question_sha256':e.settings()['question_sha256'],
  'execution_status':'COMPLETE' if complete else'PARTIAL','job_completeness_gate':'PASS' if complete else'FAIL','merge_compatibility_gate':'PASS',
  'guard_continuation_gate':'PASS_CONDITIONAL' if guard_pass else'UNRESOLVED','thermal_h_entry_gate':'PASS_CONDITIONAL' if thermal_pass else'UNRESOLVED',
  'tests_status':'COMPLETE_CONDITIONAL' if complete else'PROVISIONAL','final_result_gate':'UNRESOLVED','actual_source_admission':'UNRESOLVED',
  'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED','records':reports,
  'retained_lcdm':retained,'job_manifest':{'q':e.Q,'program_id':e.ID,'run_id':next(iter(contexts))[0] if contexts else None,
   'expected_jobs':list(CASES),'completed_jobs':sorted(reports),'failed_jobs':[],'pending_jobs':missing},'return_route':'RESULT INGESTION & ROUTING ENGINE'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--program-id',default=e.ID);ap.add_argument('--case',choices=CASES);ap.add_argument('--out',default='q048_guard_results')
 ap.add_argument('--resume');ap.add_argument('--collect');ap.add_argument('--expected-run');ap.add_argument('--full-verify',action='store_true');a=ap.parse_args()
 e.fail(a.program_id==e.ID,'PROGRAM_ID_GATE')
 if a.collect:
  r=collect(a.collect,expected_run=a.expected_run,full=a.full_verify);proof.write(a.out,r);print(json.dumps({k:r[k] for k in ('execution_status','job_completeness_gate','guard_continuation_gate','thermal_h_entry_gate','final_result_gate')}))
  if r['job_completeness_gate']!='PASS':raise SystemExit(2)
 else:e.fail(a.case is not None,'CLI_CASE_REQUIRED');run(a.case,a.out,a.resume)
if __name__=='__main__':main()
