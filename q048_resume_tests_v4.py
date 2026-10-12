"""Finite admission and adversarial provenance regressions for Q048 V4."""
import copy,unittest
from fractions import Fraction as F
from pathlib import Path
import q048_resume_v4 as e

class Controls(unittest.TestCase):
 def test_new_background_method_is_recomputed(self):
  from q048_resume_controls_v4 import background_control
  for case in ('camspec-ede_n3','hillipop-ede_n3'):
   row,now,current,cell=background_control(case)
   e.verify_background_cell(cell,now,current,e.p.parameters(row))
   for key,value in [('comparison_weight','1'),('comparison_method','unknown')]:
    bad=copy.deepcopy(cell);bad[key]=value
    with self.assertRaises(ValueError):e.verify_background_cell(bad,now,current,e.p.parameters(row))

 def test_new_thermal_control_and_supersolution(self):
  from q048_resume_controls_v4 import thermal_control
  report=thermal_control()
  self.assertGreater(F(report['independent_slack']),0)
  self.assertTrue(report['positive_temperature'])

 def test_exact_parent_migration(self):
  settings=e.load(e.ROOT/'q048_resume_config_v4.json')
  for case in e.p.CASES:
   r,meta,sha=e.parent_from_asset(case,settings)
   self.assertEqual(sha,settings['parent_checkpoints'][case])
   self.assertEqual(meta['run_id'],'38230594450')
   self.assertEqual(r['v3_parent_root']['checkpoint_sha256'],sha)

 def test_parent_tamper_and_lost_prefix_fail(self):
  settings=e.load(e.ROOT/'q048_resume_config_v4.json');case='camspec-ede_n3'
  bad=copy.deepcopy(settings);bad['parent_checkpoints'][case]='0'*64
  with self.assertRaisesRegex(ValueError,'PARENT_CHECKPOINT_HASH'):e.parent_from_asset(case,bad)
  x=fixture(case);x['record']['background']['cells'][0]['certificate']['closed']=False
  with self.assertRaisesRegex(ValueError,'PINNED_PARENT_PREFIX'):e.validate_checkpoint(x,case,settings)

 def test_metadata_lineage_and_scientific_scope_fail_closed(self):
  settings=e.load(e.ROOT/'q048_resume_config_v4.json');case='camspec-lcdm'
  for key,value in [('run_id','different'),('config_hash','0'*64),('parent_checkpoint_sha256','0'*64)]:
   x=fixture(case);x['metadata'][key]=value
   with self.assertRaises(ValueError):e.validate_checkpoint(x,case,settings)
  row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case]
  for key,value in [('scientific_question','different'),('actual_source_admission','PASS')]:
   r=fixture(case)['record'];r[key]=value
   with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(r,row,e.p.parameters(row),5)

 def test_missing_merge_fails_and_preserves_partial(self):
  import tempfile
  import q048_resume_merge_v4 as merge
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(merge.collect(d)['job_completeness_gate'],'FAIL')
   e.p.old.write(Path(d)/'camspec-lcdm_checkpoint_v4.json',fixture('camspec-lcdm'))
   r=merge.collect(d);self.assertEqual(r['job_completeness_gate'],'FAIL')
   self.assertIn('camspec-lcdm',r['partial_records'])

 def test_original_background_certificate_unchanged(self):
  case='camspec-ede_n3';settings=e.load(e.ROOT/'q048_resume_config_v4.json')
  r,_,_=e.parent_from_asset(case,settings);row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=e.p.parameters(row)
  _,a,y=e.p.source_initial(row,t);cell=r['background']['cells'][0];before=e.objhash(cell)
  e.verify_background_cell(cell,a.lo,y,t);self.assertEqual(before,e.objhash(cell))

 def test_work_settings_and_coordinates(self):
  settings=e.load(e.ROOT/'q048_resume_config_v4.json');e.validate_settings(settings)
  bad=copy.deepcopy(settings);bad['max_halvings']=12
  with self.assertRaises(ValueError):e.validate_settings(bad)
  for key,value in [('source_config_sha256','0'*64),('parent_file_sha256','0'*64),('parent_run_id','different')]:
   bad=copy.deepcopy(settings);bad[key]=value
   with self.assertRaisesRegex(ValueError,'FROZEN_SCIENTIFIC_INPUTS'):e.validate_settings(bad)
  self.assertEqual(e.coordinate('1/'+str(10**1100+1)),F('1/'+str(10**1100+1)))
  with self.assertRaises(ValueError):e.coordinate(0.01)

 def test_unsupported_full_scientific_products_rejected(self):
  case='camspec-lcdm';settings=e.load(e.ROOT/'q048_resume_config_v4.json')
  row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case]
  for key in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds'):
   x=fixture(case);x['record'][key]='PASS'
   with self.assertRaisesRegex(ValueError,'NOT_COMPUTED'):e.validate_checkpoint(x,case,settings)
   with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(x['record'],row,e.p.parameters(row),5)

 def test_mutually_forged_first_parent_pointer_rejected(self):
  case='camspec-lcdm';settings=e.load(e.ROOT/'q048_resume_config_v4.json')
  for forged in ('0'*64,'f'*64):
   x=fixture(case);x['metadata']['parent_checkpoint_sha256']=forged;x['record']['parent_checkpoint_sha256']=forged
   with self.assertRaisesRegex(ValueError,'IMMEDIATE_V3_PARENT'):e.validate_checkpoint(x,case,settings)

 def test_new_certificate_tampering_cannot_be_rebound(self):
  from q048_resume_controls_v4 import background_control
  case='camspec-ede_n3';row,now,current,cell=background_control(case)
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
  import q048_resume_merge_v4 as merge
  with tempfile.TemporaryDirectory() as d:
   for folder in ('one','two'):
    path=Path(d)/folder;path.mkdir()
    e.p.old.write(path/'camspec-lcdm_checkpoint_v4.json',fixture('camspec-lcdm'))
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
 settings=e.load(e.ROOT/'q048_resume_config_v4.json');r,m,sha=e.parent_from_asset(case,settings)
 r.update(program_id=e.ID,version=e.VERSION,run_id='LOCAL',tests_status='PROVISIONAL',parent_checkpoint_sha256=sha,parent_record_run_id=settings['parent_run_id'],
          inherited_counts={s:len(r[s]['cells']) for s in ('background','thermal')},
          inherited_cells_hashes={s:e.objhash(r[s]['cells']) for s in ('background','thermal')})
 meta=dict(m,program_id=e.ID,version=e.VERSION,run_id='LOCAL',config_hash=e.objhash(settings),stage='RAW_CONTINUATION_DONE',
           parent_checkpoint_sha256=sha,v3_parent_root=r['v3_parent_root'])
 return {'schema':'Q048_CHECKPOINT_V4','metadata':meta,'record':r}

if __name__=='__main__':unittest.main(verbosity=2)
