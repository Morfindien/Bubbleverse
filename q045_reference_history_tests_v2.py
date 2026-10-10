from pathlib import Path
import math, unittest, tempfile
import numpy as np
import q045_reference_history_v2 as a

class RecoveryTests(unittest.TestCase):
 def original(self):
  return dict(nH0_m3=.18806240632995103,fHe=.08185254557271222,YHe=.24532709446649748,sigma_m2=6.65e-29,metres_per_Mpc=3.08e22,c_m_s=299792458.,m_H_kg=1.67e-27,not4=3.97,reio_parametrization=1)
 def test_observed_one_ulp_derived_YHe_is_recorded(self):
  old=self.original();new=dict(old,YHe=math.nextafter(old['YHe'],math.inf))
  result=a.normalization_check(new,old,{'tau_reio':.05})
  self.assertFalse(result['YHe_bitwise_equal']);self.assertEqual(result['YHe_ulp_distance'],1)
 def test_two_ulp_YHe_drift_is_rejected(self):
  old=self.original();new=dict(old,YHe=math.nextafter(math.nextafter(old['YHe'],math.inf),math.inf))
  with self.assertRaises(ValueError):a.normalization_check(new,old,{'tau_reio':.05})
 def test_explicit_helium_is_not_exempted(self):
  old=self.original();new=dict(old,YHe=math.nextafter(old['YHe'],math.inf))
  with self.assertRaises(ValueError):a.normalization_check(new,old,{'YHe':old['YHe']})
 def test_normalization_inputs_stay_exact(self):
  old=self.original()
  for key in ('nH0_m3','fHe','sigma_m2','metres_per_Mpc','c_m_s','m_H_kg','not4'):
   with self.subTest(key=key),self.assertRaises(ValueError):a.normalization_check(dict(old,**{key:math.nextafter(old[key],math.inf)}),old,{})
 def test_equal_YHe_has_zero_distance(self):
  old=self.original();self.assertEqual(a.normalization_check(old,old,{})['YHe_ulp_distance'],0)
 def test_nonfinite_helium_is_rejected(self):
  old=self.original()
  for value in (math.nan,math.inf,-math.inf):
   with self.assertRaises(ValueError):a.normalization_check(dict(old,YHe=value),old,{})
 def test_recovery_cannot_execute_a_native_worker(self):
  import subprocess,sys
  result=subprocess.run([sys.executable,str(Path(a.__file__)),'worker'],capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0);self.assertIn('invalid choice',result.stderr)
  self.assertFalse(hasattr(a,'worker'));self.assertFalse(hasattr(a,'bounded'))
 def test_missing_archives_fail_without_physical_qualification(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   output=Path(d)/'out/result.json';self.assertEqual(a.collect(d,output),1);r=a.read(output)
   self.assertEqual(r['merge_compatibility_gate'],'FAIL');self.assertEqual(r['new_theory_evaluations'],0)
   self.assertEqual(r['reference_truth_gate'],'UNQUALIFIED');self.assertEqual(r['final_result_gate'],'UNRESOLVED')
 def test_artifact_member_tampering_is_rejected(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'raw';p.write_text('original');item={'name':'test','members_sha256':{'raw':a.sha(p)}}
   a.verify_product(d,item);p.write_text('changed')
   with self.assertRaises(ValueError):a.verify_product(d,item)
 def test_original_failure_is_not_broadly_ignored(self):
  c=a.recovery_contract();item=next(x for x in c['artifacts'] if x['role']=='worker')
  key,lev=item['job_id'].rsplit('-L',1)
  record=dict(q=a.Q,program_id='Q045-REFHIST-V1',job_id=item['job_id'],parent_key=key,level=int(lev),
   run_id=c['source_run_id'],execution_commit=c['source_commit'],config_sha256=c['source_config_sha256'],
   theory_evaluations_started=1,status='FAILED',error='OTHER_FAILURE')
  with tempfile.TemporaryDirectory() as d:
   path=Path(d);a.write(path/a.RESULT,record)
   with self.assertRaisesRegex(ValueError,'UNAPPROVED_FAILURE_RECOVERY'):a.verify_worker(item,path,c)


class HistoryTests(unittest.TestCase):
 def api(self,name):
  self.assertTrue(a is not None and hasattr(a,name),'Missing required history diagnostic: '+name)
  return getattr(a,name)
 def test_three_agreeing_levels_cannot_pass_reference_truth(self):
  r=self.api('convergence')([1.,1.,1.]);self.assertEqual(r['reference_truth_gate'],'UNQUALIFIED');self.assertIsNone(r['reference_error_bound'])
 def test_richardson_estimate_is_labeled_empirical(self):
  r=self.api('convergence')([1.25,1.0625,1.015625]);self.assertAlmostEqual(r['observed_order'],2);self.assertEqual(r['estimate_status'],'EMPIRICAL_NOT_A_BOUND')
 def test_controls_halve_only_numerical_error_and_spacing(self):
  f=self.api('settings');s=f(2);self.assertEqual(s['thermo_Nz_lin'],80000);self.assertEqual(s['background_Nloga'],160000);self.assertEqual(s['reionization_sampling'],.00375);self.assertNotIn('tau_reio',s);self.assertNotIn('helium_fullreio_redshift',s)
 def test_physical_input_precision_collision_is_rejected(self):
  with self.assertRaises(ValueError):self.api('parameters')({'tau_reio':.05,'thermo_Nz_lin':42},1)
 def test_physical_vector_is_not_mutated(self):
  p={'tau_reio':.05,'H0':68.,'n_scf':3};r=self.api('parameters')(p,1);self.assertEqual(p,{'tau_reio':.05,'H0':68.,'n_scf':3});self.assertEqual(r['H0'],68.)
 def test_independent_redshift_integral_matches_exact_constant_electron_history(self):
  z=np.array([0.,1.,2.]);xe=np.ones(3);H=np.ones(3)
  depth=self.api('redshift_depth')(z,xe,np.zeros(3),H,2.,16)
  np.testing.assert_allclose(depth,[0.,14/3,52/3],rtol=2e-15,atol=1e-14)
 def test_redshift_integral_rejects_nonpositive_H(self):
  with self.assertRaises(ValueError):self.api('redshift_depth')(np.array([0.,1.]),np.ones(2),np.zeros(2),np.array([1.,0.]),1.,16)
 def test_exact_cubic_orientation_and_curvature_sign(self):
  f=self.api('integrals')([2.,1.,0.],[4.,1.,0.],[2.,2.,2.]);self.assertAlmostEqual(f['minus'][-1],8/3);self.assertGreater(f['plus'][-1],f['minus'][-1])
 def test_duplicate_parent_json_is_rejected(self):
  f=self.api('read')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.json';p.write_text('{"q":1,"q":2}')
   with self.assertRaises(ValueError):f(p)
 def test_partial_jobs_never_merge_as_complete(self):
  f=self.api('completeness');self.assertEqual(f(['a','b'],['a'])['gate'],'FAIL');self.assertEqual(f(['a','b'],['a','a','b'])['gate'],'FAIL')
 def test_installed_workflow_path_is_canonical(self):
  p=Path(__file__).resolve().parent/'.github/workflows/q045-reference-history-v2.yml';self.assertTrue(p.is_file(),'Workflow required at canonical installed path')
 def test_precision_paths_remain_strings_and_are_compared(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'precision.tsv';p.write_text('data_path\t/frozen/path\naccuracy\t1e-6\n')
   self.assertEqual(self.api('precision')(p),{'data_path':'/frozen/path','accuracy':1e-6})
 def test_cubic_projection_reproduces_quadratic(self):
  f=self.api('cubic_at');z=np.array([0.,1.,2.]);x=np.array([.25,1.5,2.])
  np.testing.assert_allclose(f(z,z*z,np.ones(3)*2,x),x*x,rtol=0,atol=1e-15)
 def test_redshift_history_sign_is_preserved_without_clipping(self):
  f=self.api('redshift_depth');depth=f(np.array([0.,1.]),-np.ones(2),np.zeros(2),np.ones(2),1.,16)
  self.assertLess(depth[-1],0)

if __name__=='__main__':unittest.main()

