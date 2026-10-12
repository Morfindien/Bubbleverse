"""Finite adversarial admission tests for the distinct energy/He1 extension."""
import copy,unittest
from fractions import Fraction as F
from pathlib import Path
import q048_resume_v5 as old
import q048_structural_v6 as e

class Structural(unittest.TestCase):
 def test_api_exists(self):
  self.assertTrue(hasattr(e,'derive'),'Source-root extension has not been implemented')
 def test_original_start_and_material_phase_horizon(self):
  for case in ('camspec-ede_n3','hillipop-ede_n3'):
   parent=e.parent_checkpoint(case);before=old.objhash(parent)
   ext=e.derive(case,parent)
   phase=ext['phase']
   self.assertEqual(phase['initial_state'],parent['record']['thermal']['endpoint'][0])
   self.assertEqual(F(phase['a1']),F(1,4601));self.assertGreater(F(phase['a1']),F(phase['a0']))
   self.assertEqual(old.objhash(parent),before)
   self.assertEqual(phase['method'],'source_root_energy_he1_invariant_voc_v1')
   self.assertGreater(F(phase['endpoint'][0]),0)
   self.assertLess(F(phase['endpoint'][1]),F('0.02'))
 def test_source_guard_keeps_camspec_limitation(self):
  c=e.derive('camspec-ede_n3',e.parent_checkpoint('camspec-ede_n3'))
  h=e.derive('hillipop-ede_n3',e.parent_checkpoint('hillipop-ede_n3'))
  self.assertEqual(c['energy']['full_transfer_source_guard'],'NOT_ESTABLISHED_BY_THIS_BOUND')
  self.assertEqual(h['energy']['full_transfer_source_guard'],'PASS')
  self.assertLess(F(c['energy']['guard_certified_to_a']),F(1,2871))
 def test_forged_cap_endpoint_method_and_scope_rejected(self):
  case='hillipop-ede_n3';parent=e.parent_checkpoint(case);ext=e.derive(case,parent)
  for section,key,value in [('energy','energy_upper','0'),('phase','endpoint',['0','0']),('phase','method','unknown'),('phase','a1','1/2871')]:
   bad=copy.deepcopy(ext);bad[section][key]=value
   with self.assertRaises(ValueError):e.verify_extension(case,parent,bad)
  bad=copy.deepcopy(ext);bad['actual_source_admission']='PASS'
  with self.assertRaises(ValueError):e.verify_extension(case,parent,bad)
 def test_lcdm_retains_existing_component(self):
  for case in ('camspec-lcdm','hillipop-lcdm'):
   x=e.derive(case,e.parent_checkpoint(case))
   self.assertEqual(x['status'],'RETAINED_COMPLETE_CONDITIONAL_LCDM_PREFIX')
   self.assertIsNone(x['phase']);self.assertIsNone(x['energy'])
 def test_negative_source_domain_rejected(self):
  row=old.p.validate_config(old.load(old.ROOT/'q048_prefix_config_v1.json'))['cases']['camspec-ede_n3']
  t=old.p.parameters(row);t['matter']=old.p.m.I(-1)
  with self.assertRaises(ValueError):e.energy_certificate(row,t)
 def test_invalid_initial_phase_and_thermal_domain_rejected(self):
  case='camspec-ede_n3';row=old.load(old.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=old.p.parameters(row)
  r=copy.deepcopy(e.parent_checkpoint(case)['record']);r['thermal']['certified_end_a']='1/4601'
  with self.assertRaises(ValueError):e.phase_certificate(r,row,t)
  r=copy.deepcopy(e.parent_checkpoint(case)['record']);r['thermal']['endpoint']=[['-1','2']]
  with self.assertRaises(ValueError):e.phase_certificate(r,row,t)
 def test_exp_free_control_contains_endpoint(self):
  case='camspec-ede_n3';x=e.derive(case,e.parent_checkpoint(case));p=x['phase'];c=e.independent_control(p)
  self.assertGreater(F(c['endpoint'][0]),0)
  self.assertLessEqual(F(c['endpoint'][0]),F(p['endpoint'][1]))
  self.assertGreaterEqual(F(c['endpoint'][1]),F(p['endpoint'][0]))

class Execution(unittest.TestCase):
 def test_execution_api_exists(self):
  self.assertTrue(hasattr(e,'run'), 'Four-case execution layer missing')
 def test_missing_and_duplicate_case_collection(self):
  import tempfile
  with tempfile.TemporaryDirectory()as d:
   r=e.collect(d,full=False);self.assertEqual(r['job_completeness_gate'],'FAIL')
   self.assertEqual(r['execution_status'],'PARTIAL')
   parent=e.parent_checkpoint('camspec-lcdm');x=e.make_report('camspec-lcdm',parent,e.derive('camspec-lcdm',parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
   old.p.old.write(Path(d)/'camspec-lcdm_structural_v6.json',x)
   self.assertEqual(e.collect(d,full=False)['job_completeness_gate'],'FAIL')
   old.p.old.write(Path(d)/'duplicate_structural_v6.json',x)
   with self.assertRaises(ValueError):e.collect(d,full=False)
 def test_report_parent_and_scope_cannot_be_rebound(self):
  case='camspec-lcdm';parent=e.parent_checkpoint(case);r=e.make_report(case,parent,e.derive(case,parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
  e.verify_report(r,full=False)
  for section,key,value in [('extension','actual_source_admission','PASS'),('parent_checkpoint','schema','Q048_CHECKPOINT_V6')]:
   bad=copy.deepcopy(r);bad[section][key]=value
   with self.assertRaises(ValueError):e.verify_report(bad,full=False)
  bad=copy.deepcopy(r);bad['parent_checkpoint']['record']['thermal']['endpoint']=[['0','0']]
  with self.assertRaises(ValueError):e.verify_report(bad,full=False)
 def test_wrong_run_and_config_collection_rejected(self):
  case='camspec-lcdm';parent=e.parent_checkpoint(case);r=e.make_report(case,parent,e.derive(case,parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
  bad=copy.deepcopy(r);bad['config_hash']='0'*64
  with self.assertRaises(ValueError):e.verify_report(bad,full=False)
  with self.assertRaises(ValueError):e.verify_report(r,full=False,expected_run='foreign')

class CollectorHardening(unittest.TestCase):
 def test_conflicting_checkpoint_cannot_be_ignored(self):
  import tempfile
  case='camspec-lcdm';parent=e.parent_checkpoint(case)
  r=e.make_report(case,parent,e.derive(case,parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
  r.update(tests_status='COMPLETE_CONDITIONAL',stage='FINAL_CONDITIONAL_STRUCTURAL_COMPONENT')
  with tempfile.TemporaryDirectory()as d:
   old.p.old.write(Path(d)/(case+'_structural_v6.json'),r)
   bad=copy.deepcopy(r);bad['run_id']='999999999'
   old.p.old.write(Path(d)/(case+'_checkpoint_v6.json'),bad)
   with self.assertRaises(ValueError):e.collect(d,full=False)
 def test_duplicate_checkpoint_cannot_be_ignored(self):
  import tempfile
  case='camspec-lcdm';parent=e.parent_checkpoint(case)
  r=e.make_report(case,parent,e.derive(case,parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
  with tempfile.TemporaryDirectory()as d:
   old.p.old.write(Path(d)/(case+'_checkpoint_v6.json'),r)
   old.p.old.write(Path(d)/'duplicate_checkpoint_v6.json',r)
   with self.assertRaises(ValueError):e.collect(d,full=False)
 def test_forged_source_admission_audit_rejected(self):
  case='camspec-lcdm';parent=e.parent_checkpoint(case)
  r=e.make_report(case,parent,e.derive(case,parent),{'gate':'PASS_CONDITIONAL_RECOMPUTED'})
  r['source_admission_audit']['status']='PASS'
  with self.assertRaises(ValueError):e.verify_report(r,full=False)

if __name__=='__main__':unittest.main()
