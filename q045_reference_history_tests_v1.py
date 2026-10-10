from pathlib import Path
import importlib, importlib.util, json, unittest, tempfile, subprocess, sys, os
import numpy as np
try: a=importlib.import_module('q045_reference_history_v1')
except ModuleNotFoundError: a=None

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
  p=Path(__file__).resolve().parent/'.github/workflows/q045-reference-history-v1.yml';self.assertTrue(p.is_file(),'Workflow required at canonical installed path')
 def test_cache_identity_preserves_complete_original_key_and_paths(self):
  import re
  text=(Path(__file__).resolve().parent/'.github/workflows/q045-reference-history-v1.yml').read_text()
  block=re.search(r'uses: actions/cache/restore@v4\n        with:\n          path: \|\n(.*?)          key: (.*?)\n',text,re.S)
  expected=self.api('contract')()['cache_identity'];self.assertEqual([x.strip() for x in block[1].splitlines() if x.strip()],expected['paths']);self.assertEqual(block[2],expected['key'])
  self.assertIn('fail-on-cache-miss: true',text);self.assertNotIn('restore-keys:',text);self.assertNotIn('actions/cache/save',text)
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
 def test_empty_collection_never_passes_and_never_qualifies(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'final.json';self.api('collect')(d,out);r=self.api('read')(out)
   self.assertEqual(r['job_completeness']['gate'],'FAIL');self.assertEqual(r['merge_compatibility_gate'],'FAIL');self.assertEqual(r['reference_truth_gate'],'UNQUALIFIED');self.assertEqual(r['final_result_gate'],'UNRESOLVED')
 def test_duplicate_failed_outcomes_never_pass(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);r=self.api('envelope')();job=self.api('contract')()['expected_jobs'][0]
   r.update(job_id=job,parent_key=job.rsplit('-L',1)[0],level=1,status='FAILED',files={},theory_evaluations_started=0,history_diagnostic_gate='FAIL')
   self.api('write')(p/'workers/one'/a.RESULT,r);self.api('write')(p/'workers/two'/a.RESULT,r)
   self.api('collect')(p,p/'final.json');r=self.api('read')(p/'final.json')
   self.assertTrue(r['job_completeness']['duplicates']);self.assertEqual(r['merge_compatibility_gate'],'FAIL')

HERE=Path(__file__).resolve().parent

def native_fixture(root):
    """Real pinned array bodies plus synthetic callers test observational interposition.
    This fixture cannot certify cosmology or the cached original classy binary.
    """
    root=Path(root).resolve()
    with tempfile.TemporaryDirectory() as t:
        d=Path(t)
        inc=[]
        for sub in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):
            inc+=['-I',str(root/sub)]
        stub=r'''
#include "class.h"
#include <math.h>
int thermodynamics_reionization_get_tau(struct precision *pr,struct background *ba,struct thermodynamics *th,struct thermo_workspace *w){
  (void)pr;(void)ba;int n=3;
  int status=array_spline_table_line_to_line(th->tau_table,n,th->thermodynamics_table,th->th_size,th->index_th_dkappa,th->index_th_dddkappa,_SPLINE_EST_DERIV_,th->error_message);
  if(status)return status;
  status=array_integrate_all_spline_table_line_to_line(th->tau_table,n,th->thermodynamics_table,th->th_size,th->index_th_dkappa,th->index_th_dddkappa,&w->reionization_optical_depth,th->error_message);
  w->reionization_optical_depth *= -1;return status;
}
int thermodynamics_calculate_opticals(struct precision *pr,struct thermodynamics *th){
  (void)pr;
  int s=array_spline_table_line_to_line(th->tau_table,th->tt_size,th->thermodynamics_table,th->th_size,th->index_th_dkappa,th->index_th_dddkappa,_SPLINE_EST_DERIV_,th->error_message);
  if(s)return s;
  s=array_integrate_spline_table_line_to_line(th->tau_table,th->tt_size,th->thermodynamics_table,th->th_size,th->index_th_dkappa,th->index_th_dddkappa,th->index_th_g,th->error_message);
  if(s)return s;
  for(int i=0;i<th->tt_size;i++){int o=i*th->th_size;double expk=exp(th->thermodynamics_table[o+th->index_th_g]);th->thermodynamics_table[o+th->index_th_exp_m_kappa]=expk;th->thermodynamics_table[o+th->index_th_g]=expk*th->thermodynamics_table[o+th->index_th_dkappa];}
  return 0;
}
'''
        driver=r'''
#include "class.h"
#include <assert.h>
#include <dlfcn.h>
#include <string.h>
int main(int argc,char **argv){
  assert(argc==2);void *lib=dlopen(argv[1],RTLD_NOW);if(!lib){fprintf(stderr,"%s\n",dlerror());return 11;}
  typedef int(*sf)(struct precision*,struct background*,struct thermodynamics*,struct thermo_workspace*);
  typedef int(*cf)(struct precision*,struct thermodynamics*);
  sf scalar=(sf)dlsym(lib,"thermodynamics_reionization_get_tau");cf cum=(cf)dlsym(lib,"thermodynamics_calculate_opticals");assert(scalar&&cum);
  struct precision p={0};struct background b={0};struct thermodynamics a={0};struct thermo_workspace w={0};struct thermo_reionization_parameters re={0};
  double z[]={0,1,2,3},eta[]={3,2,1,.5};double table[]={3,9,0,0,0, 2,4,0,0,0, 1,1,0,0,0, .5,.25,0,0,0},baseline[20],params[]={8,12};
  a.tt_size=4;a.th_size=5;a.z_table=z;a.tau_table=eta;a.thermodynamics_table=table;
  a.index_th_xe=0;a.index_th_dkappa=1;a.index_th_dddkappa=2;a.index_th_g=3;a.index_th_exp_m_kappa=4;
  re.reionization_parameters=params;re.index_re_reio_redshift=0;re.index_re_reio_start=1;w.ptrp=&re;
  assert(scalar(&p,&b,&a,&w)==0);double target=w.reionization_optical_depth;memcpy(baseline,table,sizeof(table));
  assert(thermodynamics_reionization_get_tau(&p,&b,&a,&w)==0);assert(target==w.reionization_optical_depth);assert(memcmp(table,baseline,sizeof(table))==0);
  assert(cum(&p,&a)==0);memcpy(baseline,table,sizeof(table));
  assert(thermodynamics_calculate_opticals(&p,&a)==0);assert(memcmp(table,baseline,sizeof(table))==0);
  return 0;
}
'''
        (d/'fixture.c').write_text(stub);(d/'driver.c').write_text(driver)
        subprocess.run(['gcc','-shared','-fPIC','-O2',*inc,str(root/'tools/arrays.c'),str(root/'tools/common.c'),str(d/'fixture.c'),'-lm','-o',str(d/'fixture.so')],check=True)
        subprocess.run(['gcc','-O2','-ffunction-sections','-fdata-sections','-Dmain=q045_unused_main',*inc,'-c',str(HERE/'q045_reference_history_probe_v1.c'),'-o',str(d/'observer.o')],check=True)
        exports=['-Wl,--export-dynamic-symbol='+n for n in ('thermodynamics_reionization_get_tau','thermodynamics_calculate_opticals','array_integrate_all_spline_table_line_to_line','array_integrate_spline_table_line_to_line')]
        subprocess.run(['gcc',*exports,'-Wl,--gc-sections',*inc,str(d/'driver.c'),str(d/'observer.o'),'-Wl,--no-as-needed',str(d/'fixture.so'),'-Wl,-rpath,'+str(d),'-ldl','-lm','-o',str(d/'fixture')],check=True)
        subprocess.run([str(d/'fixture'),str(d/'fixture.so')],env=dict(os.environ,Q045_TRACE_DIR=str(d)),check=True)
        spec=importlib.util.spec_from_file_location('fixture_audit',HERE/'q045_reference_history_v1.py')
        a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
        s=a.table(d/'scalar_001.tsv');c=a.table(d/'cumulative_native.tsv')
        events=[json.loads(x) for x in (d/'native_trace.jsonl').read_text().splitlines()]
        assert len(s['z'])==3 and events[0]['support_rows']==3 and events[0]['argmin']==2
        assert c['native_kappa'][-1]>0 and (c['native_kappa']==a.integrals(c['eta_Mpc'],c['q_1_Mpc'],c['q_second_eta'])['plus']).all()
        print('NATIVE_ARRAY_OBSERVER_FIXTURE=PASS; unchanged real pinned array outputs; synthetic callers only')

if __name__=='__main__':
    if '--native-root' in sys.argv:
        idx=sys.argv.index('--native-root');root=sys.argv[idx+1];del sys.argv[idx:idx+2]
        native_fixture(root)
    unittest.main()
