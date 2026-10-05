"""Finite behavior tests for new diagnostic code, not cosmological validation."""
from pathlib import Path
import importlib.util,json,os,shutil,subprocess,sys,tempfile,unittest

HERE=Path(__file__).resolve().parent

class IntegratorTests(unittest.TestCase):
    def test_new_solvers_preserve_coupling_midpoint_stability_and_finite_failure(self):
        # Catches incorrect stages, sign/coupling loss, nonfinite success or unbounded Newton.
        self.assertTrue((HERE/'q042_reference_integrators_v26.h').is_file(), 'Independent integrator implementation is missing')
        code=r'''
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include "q042_reference_integrators_v26.h"
static int rhs(double s,const double*y,double*f,void*c,char*err,size_t n){(void)c;(void)err;(void)n;f[0]=y[0]+y[1];f[1]=-y[1];return 0;}
static int stiff(double s,const double*y,double*f,void*c,char*err,size_t n){(void)s;(void)c;(void)err;(void)n;f[0]=-100*y[0];f[1]=-100*y[1];return 0;}
static int bad(double s,const double*y,double*f,void*c,char*err,size_t n){(void)s;(void)y;(void)c;(void)err;(void)n;f[0]=NAN;f[1]=1;return 0;}
static int no_root(double s,const double*y,double*f,void*c,char*err,size_t n){(void)s;(void)c;(void)err;(void)n;f[0]=2*y[0]+1;f[1]=2*y[1]+1;return 0;}
int main(void){
 double y[2]={1,2},next[2];char err[256];q042_solver_stats st={0};
 for(int k=0;k<10;k++){assert(q042_step(0,k*.1,.1,y,next,rhs,NULL,&st,err,sizeof err)==0);y[0]=next[0];y[1]=next[1];}
 assert(fabs(y[0]-(2*exp(1.)-exp(-1.)))<1e-5);assert(fabs(y[1]-2*exp(-1.))<1e-6);
 y[0]=y[1]=1;assert(q042_step(1,0,1,y,next,stiff,NULL,&st,err,sizeof err)==0);assert(fabs(next[0]+49./51.)<1e-9);
 assert(q042_step(0,0,.1,y,next,bad,NULL,&st,err,sizeof err)!=0);assert(isnan(st.last_f[0])&&st.last_y[0]==1&&st.last_s==0);
 assert(q042_step(1,0,1,y,next,no_root,NULL,&st,err,sizeof err)!=0);assert(st.max_newton_used<=12);
 y[0]=1;y[1]=2;assert(q042_step(0,0,0,y,next,rhs,NULL,&st,err,sizeof err)==0);assert(next[0]==1&&next[1]==2);
 puts("Q042_INDEPENDENT_SOLVER_TESTS=PASS");return 0;
}'''
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'test.c').write_text(code)
            build=subprocess.run(['gcc','-O2','-std=c99','-Wall','-Wextra','-Wno-unused-parameter','-fno-fast-math','-ffp-contract=off','-I',str(HERE),str(p/'test.c'),'-lm','-o',str(p/'test')],capture_output=True,text=True)
            self.assertEqual(build.returncode,0,build.stderr)
            self.assertEqual(build.stderr,'')
            run=subprocess.run([str(p/'test')],capture_output=True,text=True,timeout=10)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertIn('Q042_INDEPENDENT_SOLVER_TESTS=PASS',run.stdout)

class ControllerTests(unittest.TestCase):
    def load_controller(self):
        self.assertTrue((HERE/'q042_reference_acquisition_v26.py').is_file(), 'Diagnostic controller implementation is missing')
        spec=importlib.util.spec_from_file_location('reference_v26',HERE/'q042_reference_acquisition_v26.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)

    def test_effective_support_does_not_require_unique_argmin(self):
        self.load_controller()
        # Catches wrong low-index clamp and discarding the special zero branch.
        self.assertEqual(self.m.possible_supports([(10,11),(1,3),(0,2),(1,4),(8,9)]),[3])
        self.assertEqual(self.m.possible_supports([(0,2),(1,3),(2,4),(2,4),(8,9)]),[0,3])

    def test_missing_and_duplicate_branch_outputs_are_not_complete(self):
        self.load_controller()
        # Catches merges accepting subsets, duplicates or a mismatched Q.
        expected=['UPPER-RK4-L1','LOWER-MIDPOINT-L4']
        records=[dict(q='Q-042',program_id='Q042-REFACQ-V26',run_id='7',config_sha256='a'*64,branch_id=b,execution_status='COMPLETE',result_status='RAW_NOT_QUALIFIED') for b in expected]
        good=self.m.completeness(records,expected,'7','a'*64)
        self.assertEqual(good['job_completeness_gate'],'PASS')
        self.assertEqual(self.m.completeness(records[:1],expected,'7','a'*64)['job_completeness_gate'],'FAIL')
        self.assertEqual(self.m.completeness(records+records[:1],expected,'7','a'*64)['merge_compatibility_gate'],'FAIL')
        records[0]['q']='Q-041'
        self.assertEqual(self.m.completeness(records,expected,'7','a'*64)['merge_compatibility_gate'],'FAIL')

    def test_nonfinite_branch_is_accounted_but_never_successful(self):
        self.load_controller()
        r=dict(q='Q-042',program_id='Q042-REFACQ-V26',run_id='8',config_sha256='b'*64,branch_id='UPPER-RK4-L1',execution_status='FAILED',result_status='RAW_NOT_QUALIFIED',error='NONFINITE_RHS')
        result=self.m.completeness([r],['UPPER-RK4-L1'],'8','b'*64)
        self.assertEqual(result['reporting_completeness_gate'],'PASS');self.assertEqual(result['job_completeness_gate'],'FAIL')
        self.assertEqual(result['failed_branches'],['UPPER-RK4-L1'])

    def test_actual_launcher_exact_resolution_and_injection_rejection(self):
        self.load_controller()
        launcher=(HERE/'.github/workflows/00-bubbleverse-start.yml').read_text()
        body=launcher.split("python - <<'PY'\n",1)[1].split('\n          PY',1)[0]
        body='\n'.join(line[10:] for line in body.splitlines())+'\n'
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);shutil.copyfile(HERE/'bubbleverse_program_registry.json',tmp/'bubbleverse_program_registry.json')
            out=tmp/'outputs';env=dict(os.environ,GITHUB_OUTPUT=str(out),RAW_PROGRAM_ID='Q042-REFACQ-V26')
            r=subprocess.run([sys.executable,'-c',body],cwd=tmp,env=env,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr);self.assertIn('workflow_id=q042-reference-acquisition-v26.yml',out.read_text())
            for bad in ['UNKNOWN-ID','Q042-REFACQ-V26; touch injected','$(touch injected)']:
                out.write_text('');env['RAW_PROGRAM_ID']=bad
                r=subprocess.run([sys.executable,'-c',body],cwd=tmp,env=env,capture_output=True,text=True)
                self.assertNotEqual(r.returncode,0);self.assertEqual(out.read_text(),'');self.assertFalse((tmp/'injected').exists())

    def test_mutable_readme_does_not_break_frozen_package(self):
        self.load_controller()
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);shutil.copytree(HERE,tmp/'package',ignore=shutil.ignore_patterns('__pycache__'))
            root=tmp/'package';(root/'README.md').write_text((root/'README.md').read_text()+'\nUnrelated repository documentation update.\n')
            self.m.static(root)
            (root/'q042_reference_point_v26.ini').write_text('H0 = 70\n')
            with self.assertRaisesRegex(ValueError,'PACKAGE_HASH_GATE|POINT_GATE'): self.m.static(root)

    def test_collection_rejects_absent_duplicate_and_malformed_worker_json(self):
        self.load_controller()
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);final=tmp/'final.json';self.assertEqual(self.m.collect(tmp/'absent',final),1)
            self.assertEqual(json.loads(final.read_text())['acquisition_gate'],'FAIL')
            for sub in ['a','b']:
                d=tmp/'collected'/sub;d.mkdir(parents=True);(d/'q042_reference_worker_result_v26.json').write_text('{}')
            self.assertEqual(self.m.collect(tmp/'collected',final),1)
            shutil.rmtree(tmp/'collected'/'b');(tmp/'collected'/'a'/'q042_reference_worker_result_v26.json').write_text('{')
            self.assertEqual(self.m.collect(tmp/'collected',final),1);self.assertIn('UNREADABLE_WORKER_JSON',json.loads(final.read_text())['error'])

    def test_richardson_accuracy_is_unresolved_despite_observed_order(self):
        self.load_controller()
        tables={}
        for method in ['RK4','MIDPOINT']:
            for level,value in [(1,1.),(2,.1),(4,.01)]:
                tables[f'UPPER-{method}-L{level}']=[dict(z=str(i),eta_Mpc=str(10-i),scope='ACQUIRED_REIONIZATION',D_Tmat_K=str(value),x_H=str(value),xe_source=str(value),dkappa_per_Mpc=str(value)) for i in range(5)]
        r=self.m.diagnostics(tables)
        self.assertEqual(r['level_differences']['UPPER-RK4']['x_H']['richardson_estimate'],'UNRESOLVED')
        self.assertIsInstance(r['level_differences']['UPPER-RK4']['x_H']['observed_rms_order'],float)

if __name__=='__main__':unittest.main()
