"""Finite admission and adversarial provenance regressions for Q048 V4."""
import copy,unittest
from fractions import Fraction as F
from pathlib import Path
import q048_resume_v5 as e

class Controls(unittest.TestCase):
 def test_new_background_method_is_recomputed(self):
  from q048_resume_controls_v5 import background_control
  for case in ('camspec-ede_n3','hillipop-ede_n3'):
   row,now,current,cell,_=background_control(case)
   e.verify_background_cell(cell,now,current,e.p.parameters(row))
   for key,value in [('comparison_weight','1'),('comparison_method','unknown')]:
    bad=copy.deepcopy(cell);bad[key]=value
    with self.assertRaises(ValueError):e.verify_background_cell(bad,now,current,e.p.parameters(row))

 def test_new_thermal_control_and_supersolution(self):
  from q048_resume_controls_v5 import thermal_control
  report=thermal_control('hillipop-ede_n3')[-1]
  self.assertGreater(F(report['independent_slack']),0)
  self.assertTrue(report['positive_temperature'])

 def test_exact_parent_migration(self):
  settings=e.load(e.ROOT/'q048_resume_config_v5.json')
  for case in e.p.CASES:
   r,meta,sha=e.parent_from_asset(case,settings)
   self.assertEqual(sha,settings['parent_checkpoints'][case])
   self.assertEqual(meta['run_id'],'38249121532')
   self.assertEqual(r['v4_parent_root']['checkpoint_sha256'],sha)

 def test_parent_tamper_and_lost_prefix_fail(self):
  settings=e.load(e.ROOT/'q048_resume_config_v5.json');case='camspec-ede_n3'
  bad=copy.deepcopy(settings);bad['parent_checkpoints'][case]='0'*64
  with self.assertRaisesRegex(ValueError,'PARENT_CHECKPOINT_HASH'):e.parent_from_asset(case,bad)
  x=fixture(case);x['record']['background']['cells'][0]['certificate']['closed']=False
  with self.assertRaisesRegex(ValueError,'PINNED_PARENT_PREFIX'):e.validate_checkpoint(x,case,settings)

 def test_metadata_lineage_and_scientific_scope_fail_closed(self):
  settings=e.load(e.ROOT/'q048_resume_config_v5.json');case='camspec-lcdm'
  for key,value in [('run_id','different'),('config_hash','0'*64),('parent_checkpoint_sha256','0'*64)]:
   x=fixture(case);x['metadata'][key]=value
   with self.assertRaises(ValueError):e.validate_checkpoint(x,case,settings)
  row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case]
  for key,value in [('scientific_question','different'),('actual_source_admission','PASS')]:
   r=fixture(case)['record'];r[key]=value
   with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(r,row,e.p.parameters(row),5)

 def test_missing_merge_fails_and_preserves_partial(self):
  import tempfile
  import q048_resume_merge_v5 as merge
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(merge.collect(d)['job_completeness_gate'],'FAIL')
   e.p.old.write(Path(d)/'camspec-lcdm_checkpoint_v5.json',fixture('camspec-lcdm'))
   r=merge.collect(d);self.assertEqual(r['job_completeness_gate'],'FAIL')
   self.assertIn('camspec-lcdm',r['partial_records'])

 def test_original_background_certificate_unchanged(self):
  case='camspec-ede_n3';settings=e.load(e.ROOT/'q048_resume_config_v5.json')
  r,_,_=e.parent_from_asset(case,settings);row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=e.p.parameters(row)
  _,a,y=e.p.source_initial(row,t);cell=r['background']['cells'][0];before=e.objhash(cell)
  e.verify_background_cell(cell,a.lo,y,t);self.assertEqual(before,e.objhash(cell))

 def test_work_settings_and_coordinates(self):
  settings=e.load(e.ROOT/'q048_resume_config_v5.json');e.validate_settings(settings)
  bad=copy.deepcopy(settings);bad['max_halvings']=11
  with self.assertRaises(ValueError):e.validate_settings(bad)
  for key,value in [('source_config_sha256','0'*64),('parent_file_sha256','0'*64),('parent_run_id','different')]:
   bad=copy.deepcopy(settings);bad[key]=value
   with self.assertRaisesRegex(ValueError,'FROZEN_SCIENTIFIC_INPUTS'):e.validate_settings(bad)
  self.assertEqual(e.coordinate('1/'+str(10**1100+1)),F('1/'+str(10**1100+1)))
  with self.assertRaises(ValueError):e.coordinate(0.01)

 def test_unsupported_full_scientific_products_rejected(self):
  case='camspec-lcdm';settings=e.load(e.ROOT/'q048_resume_config_v5.json')
  row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case]
  for key in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds'):
   x=fixture(case);x['record'][key]='PASS'
   with self.assertRaisesRegex(ValueError,'NOT_COMPUTED'):e.validate_checkpoint(x,case,settings)
   with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(x['record'],row,e.p.parameters(row),5)

 def test_mutually_forged_first_parent_pointer_rejected(self):
  case='camspec-lcdm';settings=e.load(e.ROOT/'q048_resume_config_v5.json')
  for forged in ('0'*64,'f'*64):
   x=fixture(case);x['metadata']['parent_checkpoint_sha256']=forged;x['record']['parent_checkpoint_sha256']=forged
   with self.assertRaisesRegex(ValueError,'PARENT_LINEAGE|IMMEDIATE_V4_PARENT'):e.validate_checkpoint(x,case,settings)

 def test_new_certificate_tampering_cannot_be_rebound(self):
  from q048_resume_controls_v5 import background_control
  case='camspec-ede_n3';row,now,current,cell,_=background_control(case)
  for key,value in [('closed',False),('endpoint',[['0','0'],['0','0']]),('initial_error',['0','0'])]:
   bad=copy.deepcopy(cell);bad['certificate'][key]=value
   with self.assertRaisesRegex(ValueError,'CERTIFICATE_MISMATCH'):e.verify_background_cell(bad,now,current,e.p.parameters(row))

 def test_wrong_thermal_method_or_phase_rejected(self):
  for mode,method,box in [('He1','unknown',[['-1/500000','1/50']]),
                          ('He2',e.comparison.THERMAL_METHOD,[['-1/500000','1/50']]),
                          ('He1',None,[['-1/500000','1/50']])]:
   with self.assertRaisesRegex(ValueError,'THERMAL_TUBE'):
    e.thermal_guard({'box':box},None,None,mode,{'ede':{}},None,None,None,None,method)

 def test_duplicate_merge_case_rejected(self):
  import tempfile
  import q048_resume_merge_v5 as merge
  with tempfile.TemporaryDirectory() as d:
   for folder in ('one','two'):
    path=Path(d)/folder;path.mkdir()
    e.p.old.write(path/'camspec-lcdm_checkpoint_v5.json',fixture('camspec-lcdm'))
   with self.assertRaisesRegex(ValueError,'DUPLICATE'):merge.collect(d)

 def test_retained_artifact_run_must_match_selection(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'checkpoint.json';e.p.old.write(path,fixture('camspec-lcdm'))
   with self.assertRaisesRegex(ValueError,'RETAINED_ARTIFACT_RUN_ID'):
    e.run('camspec-lcdm',Path(d)/'out',path,expected_checkpoint_run='99999')
   with self.assertRaisesRegex(ValueError,'EXPECTED_RETAINED_CHECKPOINT_REQUIRED'):
    e.run('camspec-lcdm',Path(d)/'out',expected_checkpoint_run='99999')

def fixture(case):
 settings=e.load(e.ROOT/'q048_resume_config_v5.json');r,m,sha=e.parent_from_asset(case,settings)
 r.update(program_id=e.ID,version=e.VERSION,run_id='LOCAL',tests_status='PROVISIONAL',parent_checkpoint_sha256=sha,parent_record_run_id=settings['parent_run_id'],
          inherited_counts={s:len(r[s]['cells']) for s in ('background','thermal')},
          inherited_cells_hashes={s:e.objhash(r[s]['cells']) for s in ('background','thermal')})
 r['v5_parent_lineage']=[{'program_id':'Q048-RESUME-V4','run_id':settings['parent_run_id'],
                        'config_hash':settings['parent_config_hash'],'checkpoint_sha256':sha}]
 meta=dict(m,program_id=e.ID,version=e.VERSION,run_id='LOCAL',config_hash=e.objhash(settings),stage='RAW_CONTINUATION_DONE',
           parent_checkpoint_sha256=sha,v3_parent_root=r['v3_parent_root'],v4_parent_root=r['v4_parent_root'],v5_parent_lineage=r['v5_parent_lineage'])
 return {'schema':'Q048_CHECKPOINT_V5','metadata':meta,'record':r}


"""Scoped V5 finite-time and migration regressions."""
import copy,unittest
from unittest.mock import patch
from fractions import Fraction as F
import q048_resume_v4 as original

class NewMethod(unittest.TestCase):
 def test_genuine_v5_resume_preserves_root_and_appends_actual_parent(self):
  import q048_resume_v5 as e
  import tempfile
  from pathlib import Path
  # Small completed LCDM prefix: actual CLI/library resume, no synthetic run state.
  parent=e.ROOT/'local-results/camspec-lcdm/camspec-lcdm_checkpoint_v5.json'
  if not parent.exists():
   # GitHub preflight starts without local results: create a fully verified
   # completed LCDM parent using the same production path first.
   with tempfile.TemporaryDirectory() as first:
    e.run('camspec-lcdm',first)
    with tempfile.TemporaryDirectory() as second:
     path=Path(first)/'camspec-lcdm_checkpoint_v5.json'
     result=e.run('camspec-lcdm',second,path,expected_checkpoint_run=e.load(path)['metadata']['run_id'])
     self.assertEqual(len(result['v5_parent_lineage']),2)
     self.assertEqual(result['v5_parent_lineage'][-1]['checkpoint_sha256'],e.digest(path))
  else:
   with tempfile.TemporaryDirectory() as second:
    result=e.run('camspec-lcdm',second,parent,expected_checkpoint_run=e.load(parent)['metadata']['run_id'])
    self.assertEqual(len(result['v5_parent_lineage']),2)
    self.assertEqual(result['v5_parent_lineage'][-1]['checkpoint_sha256'],e.digest(parent))

 def test_changed_parent_run_cannot_bypass_exact_root_pointer(self):
  import q048_resume_v5 as e
  settings=e.load(e.ROOT/'q048_resume_config_v5.json');x=fixture('camspec-lcdm')
  x['record']['parent_record_run_id']='FAKE'
  x['metadata']['parent_checkpoint_sha256']=x['record']['parent_checkpoint_sha256']='f'*64
  with self.assertRaises(ValueError):e.validate_checkpoint(x,'camspec-lcdm',settings)

 def test_missing_prior_artifact_cannot_restart_from_root(self):
  import q048_resume_v5 as e
  import re,textwrap,io,os,tempfile,json
  script=textwrap.dedent(re.findall(r"python - <<'PY'\n(.*?)\n\s*PY",(e.ROOT/'.github/workflows/q048-resume-v5.yml').read_text(),re.S)[1])
  with tempfile.NamedTemporaryFile() as out:
   env={'PRIOR_RUNS':'[123]','GITHUB_REPOSITORY':'Morfindien/Bubbleverse',
        'CASE':'camspec-lcdm','GH_TOKEN':'TEST_ONLY','GITHUB_OUTPUT':out.name}
   with patch.dict(os.environ,env),patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps({'artifacts':[]}).encode())):
    with self.assertRaisesRegex(ValueError,'MISSING_RETAINED'):exec(compile(script,'workflow-retained','exec'),{})

 def test_mutated_config_file_cannot_redefine_frozen_inputs(self):
  import q048_resume_v5 as e
  settings=e.load(e.ROOT/'q048_resume_config_v5.json');bad=copy.deepcopy(settings)
  bad['source_config_sha256']='0'*64
  with patch.object(e,'load',return_value=bad):
   with self.assertRaisesRegex(ValueError,'FROZEN_SCIENTIFIC_INPUTS'):e.validate_settings(bad)

 def test_finite_time_remedy_is_separate_and_closes(self):
  import q048_comparison_v5 as v5
  p=original.p
  cell={'t0':'0','t1':'1','predictor':[['0']],'box':[['-1/500000','1/50']]}
  field=lambda xi,y:[-y[0]/2+p.m.I(F(6,5)*F('1e-6'))]
  current=[p.m.I(-F('1e-6'),F('1e-6'))]
  with self.assertRaisesRegex(ValueError,'SUPERSOLUTION_NOT_CLOSED'):
   original.comparison.check_thermal_supersolution(cell,current,field)
  U,slack=v5.check_thermal_finite_time(cell,current,field)
  self.assertEqual(U,F('1.7e-6'));self.assertGreater(slack,0)

 def test_finite_time_domain_rejected(self):
  import q048_comparison_v5 as v5
  p=original.p;current=[p.m.I(0)]
  good={'t0':'0','t1':'1','predictor':[['0']],'box':[['-1/500000','1/50']]}
  for key,value in [('t1','2'),('predictor',[['0','1']])]:
   bad=copy.deepcopy(good);bad[key]=value
   with self.assertRaises(ValueError):v5.check_thermal_finite_time(bad,current,lambda xi,y:[-y[0]])
  with self.assertRaises(ValueError):v5.check_thermal_finite_time(good,current,lambda xi,y:[y[0]])


if __name__=='__main__':unittest.main(verbosity=2)
