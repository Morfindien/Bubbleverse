"""Finite acquisition tests. Numerical tolerances here are fixture checks only."""
import importlib.util, json, math, tempfile, unittest, subprocess, sys, os
from pathlib import Path

HERE=Path(__file__).resolve().parent

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('audit',HERE/'q045_optical_audit_v1.py')
        cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m)

    def test_source_exists(self):
        self.assertTrue((HERE/'q045_optical_audit_v1.py').is_file(), 'optical audit implementation missing')

    def test_decreasing_quadratic_exact_integral(self):
        # q(eta)=eta^2, eta 3->2->1: physical integral =26/3.
        d=self.m.integrals([3.,2.,1.],[9.,4.,1.],[2.,2.,2.])
        self.assertAlmostEqual(d['minus'][-1],26/3,places=13)
        self.assertAlmostEqual(d['gauss2'][-1],26/3,places=13)
        self.assertAlmostEqual(d['plus'][-1],28/3,places=13)
        self.assertEqual(d['coordinate_units'],'eta Mpc; q 1/Mpc; depth dimensionless')

    def test_reversed_or_nonfinite_history_is_rejected(self):
        for x,q,d in [([1,2],[1,1],[0,0]),([2,2],[1,1],[0,0]),([2,1],[1,float('inf')],[0,0])]:
            with self.assertRaises(ValueError):self.m.integrals(x,q,d)

    def test_calibration_bracket_tracks_actual_trials(self):
        en={'event':'tau_enter','requested_tau':.05,'relative_tolerance':.001}
        trials=[{'event':'scalar','call':i+1,'status':0,'tau':t,'z_reio':z,'support_rows':3,'argmin':3}
                for i,(t,z) in enumerate([(.09,46),(.01,0),(.05,23)])]
        ex={'event':'tau_exit','status':0,'tau':.05,'z_reio':23}
        d=self.m.bracket([en]+trials+[ex])
        self.assertEqual(d['accepted_bracket_tau'],[.05,.09])
        self.assertEqual(d['bisection_trials'],1)
        self.assertFalse(d['native_stopping_condition_met'])
        self.assertEqual(d['last_trial_residual'],0)

    def test_nonfinite_bracket_cannot_be_certified(self):
        e=[{'event':'tau_enter','requested_tau':.05,'relative_tolerance':.001},
           {'event':'scalar','call':1,'status':0,'tau':'Infinity','z_reio':46},
           {'event':'scalar','call':2,'status':0,'tau':.01,'z_reio':0},
           {'event':'tau_exit','status':0,'tau':.01,'z_reio':0}]
        with self.assertRaises(ValueError):self.m.bracket(e)

    def test_duplicate_and_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.json'
            for text in ['{"x":1,"x":2}','{"x":NaN}']:
                p.write_text(text)
                with self.assertRaises(ValueError):self.m.read(p)

    def test_ini_input_preserves_values_and_rejects_injection(self):
        text=self.m.ini({'tau_reio':.05141852352021917,'output':'tCl,pCl,lCl,mPk'})
        self.assertIn('tau_reio = 0.05141852352021917',text)
        with self.assertRaises(ValueError):self.m.ini({'output':'tCl\nH0=99'})

    def test_missing_jobs_do_not_pass_merge(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);o=p/'final.json';self.m.collect(p,o)
            r=self.m.read(o)
            self.assertEqual(r['job_completeness_gate'],'FAIL')
            self.assertEqual(r['final_result_gate'],'UNRESOLVED')

    def test_duplicate_jobs_are_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);r=self.m.envelope()
            r.update(job_id=self.m.contract()['expected_jobs'][0],status='FAILED',files={},theory_evaluations_started=0,observation_gate='FAIL')
            self.m.write(p/'one'/self.m.RESULT,r);self.m.write(p/'two'/self.m.RESULT,r)
            o=p/'final.json';self.m.collect(p,o);result=self.m.read(o)
            self.assertIn('DUPLICATE_OR_UNKNOWN_JOB',result['errors'])
            self.assertEqual(result['merge_compatibility_gate'],'FAIL')

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
        subprocess.run(['gcc','-O2','-ffunction-sections','-fdata-sections','-Dmain=q045_unused_main',*inc,'-c',str(HERE/'q045_optical_audit_probe_v1.c'),'-o',str(d/'observer.o')],check=True)
        exports=['-Wl,--export-dynamic-symbol='+n for n in ('thermodynamics_reionization_get_tau','thermodynamics_calculate_opticals','array_integrate_all_spline_table_line_to_line','array_integrate_spline_table_line_to_line')]
        subprocess.run(['gcc',*exports,'-Wl,--gc-sections',*inc,str(d/'driver.c'),str(d/'observer.o'),'-Wl,--no-as-needed',str(d/'fixture.so'),'-Wl,-rpath,'+str(d),'-ldl','-lm','-o',str(d/'fixture')],check=True)
        subprocess.run([str(d/'fixture'),str(d/'fixture.so')],env=dict(os.environ,Q045_TRACE_DIR=str(d)),check=True)
        spec=importlib.util.spec_from_file_location('fixture_audit',HERE/'q045_optical_audit_v1.py')
        a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
        s=a.table(d/'scalar_001.tsv');c=a.table(d/'cumulative_native.tsv')
        events=[json.loads(x) for x in (d/'native_trace.jsonl').read_text().splitlines()]
        assert len(s['z'])==3 and events[0]['support_rows']==3 and events[0]['argmin']==2
        assert c['native_kappa'][-1]>0 and (c['native_kappa']==a.integrals(c['eta_Mpc'],c['q_1_Mpc'],c['q_second_eta'])['plus']).all()
        print('NATIVE_ARRAY_OBSERVER_FIXTURE=PASS; unchanged real pinned array outputs; synthetic callers only')

if __name__=='__main__':
    if not (HERE/'q045_optical_audit_v1.py').is_file():
        raise SystemExit('FAIL: optical audit implementation missing')
    if '--native-root' in sys.argv:
        idx=sys.argv.index('--native-root');root=sys.argv[idx+1];del sys.argv[idx:idx+2]
        native_fixture(root)
    unittest.main()
