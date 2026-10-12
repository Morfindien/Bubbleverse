"""Four independent parent-bound structural workers and strict collection."""
from pathlib import Path
import argparse,copy,json,os,platform,sys,time
from concurrent.futures import ProcessPoolExecutor
import q048_structural_v6 as e
old=e.old;p=e.p;proof=e.proof

def make_report(case,parent,extension,verification):
 cfg=e.config();s=e.settings()
 return {'schema':'Q048_STRUCTURAL_CASE_V6','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
  'scientific_question':cfg['scientific_question'],'question_sha256':cfg['question_sha256'],
  'program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,
  'configuration':case,'run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),'executed_commit':os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'),
  'config_hash':old.objhash(s),'source_config_hash':s['source_config_sha256'],
  'parent_checkpoint_sha256':s['parent_checkpoints'][case],'parent_checkpoint':copy.deepcopy(parent),
  'extension':extension,'parent_verification':verification,'tests_status':'PROVISIONAL',
  'actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED',
  'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
  'python':platform.python_version(),'native_evaluations':0,'likelihood_evaluations':0,
  'source_ids':['K-PROPOSED-Q048-SOURCE-002','K-PROPOSED-Q048-INPUT-001','K-PROPOSED-Q048-MATH-REPO-006',
    'K-PROPOSED-Q048-V5-PACKAGE-008','K-PROPOSED-Q048-GITHUB-RUN-38259814813','I-PROPOSED-Q048-MATHEMATICS-006'],
  'source_admission_audit':{'status':'UNRESOLVED','new_native_work':False,
   'missing_proofs':['actual initialized-instance error linkage','native floating arithmetic/observer equivalence',
   'actual shared first-cutoff event','complete post-event xe and tau propagation'],
   'evidence':'Pinned inherited source_initialization and product fields; no new admissibility proof supplied.'}}

def verify_report(report,full=True,expected_run=None):
 s=e.validate_sources() if full else e.settings();cfg=e.config();case=report.get('configuration');e.fail(case in p.CASES,'REPORT_CASE')
 expected={'schema':'Q048_STRUCTURAL_CASE_V6','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
  'program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,'config_hash':old.objhash(s),
  'source_config_hash':s['source_config_sha256'],'scientific_question':cfg['scientific_question'],
  'question_sha256':cfg['question_sha256'],'parent_checkpoint_sha256':s['parent_checkpoints'][case],
  'actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
  'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED','native_evaluations':0,'likelihood_evaluations':0}
 e.fail(all(report.get(k)==v for k,v in expected.items()),'REPORT_IDENTITY_OR_SCOPE')
 run=report.get('run_id');e.fail(isinstance(run,str)and(run=='LOCAL'or run.isdigit()),'REPORT_RUN_ID')
 e.fail(expected_run is None or run==str(expected_run),'REPORT_EXPECTED_RUN')
 parent=e.parent_checkpoint(case);e.fail(report.get('parent_checkpoint')==parent,'PARENT_CHECKPOINT_REPLACED')
 template=make_report(case,parent,report.get('extension'),report.get('parent_verification'))
 e.fail(report.get('source_admission_audit')==template['source_admission_audit'] and report.get('source_ids')==template['source_ids'],'REPORT_SOURCE_AUDIT_OR_REGISTER')
 e.verify_extension(case,parent,report.get('extension'))
 if not full:return {'gate':'PASS_BINDINGS_ONLY','configuration':case}
 row=cfg['cases'][case];parent_proof,_=old.verify_record(parent['record'],row,p.parameters(row),s['verification_seconds'])
 return {'gate':'PASS_CONDITIONAL_RECOMPUTED','configuration':case,'parent_certificate_verification':parent_proof,
         'extension':'PASS_CONDITIONAL_RECOMPUTED_EXTENSION'}

def run(case,out):
 start=time.monotonic();e.fail(not sys.flags.optimize,'OPTIMIZED_ASSERTIONS_UNSUPPORTED');e.validate_sources()
 parent=e.parent_checkpoint(case);row=e.config()['cases'][case]
 precheck,_=old.verify_record(parent['record'],row,p.parameters(row),e.settings()['verification_seconds'])
 extension=e.derive(case,parent);r=make_report(case,parent,extension,precheck)
 out=Path(out);out.mkdir(parents=True,exist_ok=True);cp=out/(case+'_checkpoint_v6.json')
 r['stage']='RAW_STRUCTURAL_EXTENSION';proof.write(cp,r)
 post=verify_report(r,full=True);r['post_verification']=post
 r['tests_status']='COMPLETE_CONDITIONAL';r['stage']='FINAL_CONDITIONAL_STRUCTURAL_COMPONENT';r['elapsed_seconds']=time.monotonic()-start
 proof.write(cp,r);proof.write(out/(case+'_structural_v6.json'),r)
 print(json.dumps({'case':case,'gate':post['gate'],'phase_end':extension['phase']['a1']if extension['phase']else None,
   'elapsed_seconds':r['elapsed_seconds'],'final_result_gate':'UNRESOLVED'}),flush=True)
 return r

def _verify(r,expected_run):return r['configuration'],verify_report(r,full=True,expected_run=expected_run)

def collect(directory,full=True,expected_run=None):
 s=e.settings();cfg=e.config();reports={};partial={};contexts=set()
 for path in Path(directory).rglob('*_structural_v6.json'):
  r=old.load(path);case=r.get('configuration');e.fail(case in p.CASES and case not in reports and case not in partial,'MERGE_DUPLICATE_OR_UNKNOWN_CASE')
  verify_report(r,full=False,expected_run=expected_run);contexts.add((r['run_id'],r['executed_commit'],r['config_hash']))
  if r.get('tests_status')=='COMPLETE_CONDITIONAL'and r.get('stage')=='FINAL_CONDITIONAL_STRUCTURAL_COMPONENT':reports[case]=r
  else:partial[case]=r
 checkpoint_cases=set()
 for path in Path(directory).rglob('*_checkpoint_v6.json'):
  r=old.load(path);case=r.get('configuration')
  e.fail(case not in checkpoint_cases,'MERGE_DUPLICATE_CHECKPOINT');checkpoint_cases.add(case)
  verify_report(r,full=False,expected_run=expected_run)
  if case in reports or case in partial:
   e.fail(r==(reports.get(case)or partial[case]),'MERGE_CHECKPOINT_REPORT_CONFLICT')
  else:partial[case]=r
  contexts.add((r['run_id'],r['executed_commit'],r['config_hash']))
 e.fail(len(contexts)<=1,'MERGE_RUN_CONFIG_COMPATIBILITY');verified={}
 if full and reports:
  with ProcessPoolExecutor(max_workers=min(4,len(reports)))as pool:
   futures=[pool.submit(_verify,r,expected_run)for r in reports.values()]
   for f in futures:
    case,result=f.result();verified[case]=result
 missing=sorted(set(p.CASES)-set(reports));complete=not missing
 return {'schema':'Q048_STRUCTURAL_FINAL_V6','q':e.Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED',
  'program_id':e.ID,'version':e.VERSION,'scope':e.SCOPE,'source_commit':e.SOURCE,'scientific_question':cfg['scientific_question'],
  'question_sha256':cfg['question_sha256'],'config_hash':old.objhash(s),'execution_status':'COMPLETE'if complete else'PARTIAL',
  'job_completeness_gate':'PASS'if complete else'FAIL','merge_compatibility_gate':'PASS',
  'tests_status':'COMPLETE_CONDITIONAL'if complete and full else'PROVISIONAL',
  'final_result_gate':'UNRESOLVED','actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
  'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED','records':reports,'partial_records':partial,
  'merge_verification':verified,'job_manifest':{'q':e.Q,'program_id':e.ID,'run_id':next(iter(contexts))[0]if contexts else None,
   'expected_jobs':list(p.CASES),'completed_jobs':sorted(reports),'failed_jobs':sorted(partial),'pending_jobs':missing},
  'return_route':'RESULT INGESTION & ROUTING ENGINE'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--program-id',default=e.ID);parser.add_argument('--case',choices=p.CASES)
 parser.add_argument('--out',default='q048_structural_results');parser.add_argument('--collect');parser.add_argument('--expected-run')
 a=parser.parse_args();e.fail(a.program_id==e.ID,'PROGRAM_ID_GATE');e.fail(not sys.flags.optimize,'OPTIMIZED_ASSERTIONS_UNSUPPORTED');e.validate_sources()
 if a.collect:
  e.fail(a.case is None,'CLI_OPERATION');r=collect(a.collect,expected_run=a.expected_run);proof.write(a.out,r)
  print(json.dumps({k:r[k]for k in ('execution_status','job_completeness_gate','tests_status','final_result_gate')}))
  if r['job_completeness_gate']!='PASS':raise SystemExit(2)
 else:e.fail(a.case is not None,'CLI_CASE_REQUIRED');run(a.case,a.out)
if __name__=='__main__':main()
