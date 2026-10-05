"""Finite behavioral tests. Controlled boundaries are never scientific evidence.
Default: numerical C kernel and collector rejection behavior.
native-fixture ROOT: production native instrumentation with controlled dependency.
"""
from pathlib import Path
import copy,json,os,subprocess,sys,tempfile,unittest
import q042_event_cell_v28 as m
HERE=Path(__file__).resolve().parent
FIXTURE=r'''
#define Q042_ADAPTER_FIXTURE
#include "q042_event_native_v28.c"
#include <assert.h>
static int extra;
static int controlled_derivs(double s,double*y,double*dy,void*workspace,ErrorMsg msg){
 (void)msg;struct thermodynamics_parameters_and_workspace*a=workspace;double z=-s,Tr=a->ptw->Tcmb*(1+z)*kBoltz,Tm=(y[0]+a->ptw->Tcmb*(1+z))*kBoltz;
 if(extra&&Tr>TR_MIN)Tm=.05*Tr;
 int model=Tr<=TR_MIN||Tm/Tr<=T_RATIO_MIN?PEEBLES:MODEL;
 dy[0]=1.;dy[1]=0.;dy[2]=rec_dxHIIdlna(a->ptw->ptdw->phyrec->data,model,y[2],y[2],1.,1.,Tm,Tr,0,z);
 a->ptw->ptdw->x_noreio=y[2];a->ptw->ptdw->x_reio=y[2];return _SUCCESS_;
}
int main(int argc,char**argv){
 assert(argc==4);q042_dir=argv[1];q042_run=getenv("GITHUB_RUN_ID");if(!q042_run)q042_run="LOCAL";q042_config=argv[2];extra=atoi(argv[3]);q042_started=q042_now();q042_original_derivs=controlled_derivs;
 struct thermodynamics th={0};struct precision pr={0};struct thermo_workspace w={0};struct thermo_diffeq_workspace d={0};struct thermo_vector v={0};struct thermohyrec hy={0};HYREC_DATA data={0};REC_COSMOPARAMS cosmo={0};struct thermo_reionization_parameters rp={0};double re[2]={0};
 pr.reionization_z_start_max=50;pr.reionization_start_factor=8;th.reionization_width=.5;th.helium_fullreio_redshift=3.5;th.helium_fullreio_width=.5;w.Tcmb=2.7255;w.ptdw=&d;w.ptrp=&rp;d.ptv=&v;d.phyrec=&hy;d.index_ap_reio=d.ap_current=7;v.ti_size=3;v.index_ti_D_Tmat=0;v.index_ti_x_He=1;v.index_ti_x_H=2;hy.data=&data;data.cosmo=&cosmo;rp.reionization_parameters=re;rp.index_re_reio_redshift=0;rp.index_re_reio_start=1;
 struct thermodynamics_parameters_and_workspace a={0};a.ppr=&pr;a.pth=&th;a.ptw=&w;
 for(int t=0;t<2;t++)for(int n=1;n<=4;n*=2){int rc=q042_probe_trial(&a,t,n);assert(rc==(extra?1:0));}
 return 0;
}
'''
ORIGINAL=r'''
#include <stdio.h>
#include "wrap_hyrec.h"
double rec_HMLA_dxHIIdlna(HYREC_DATA*d,double xe,double xH,double nH,double H,double TM,double TR){(void)d;(void)xe;(void)xH;(void)nH;(void)H;(void)TM;(void)TR;return 2.;}
double rec_TLA_dxHIIdlna(REC_COSMOPARAMS*d,double xe,double xH,double nH,double H,double TM,double TR,double F){(void)d;(void)xe;(void)xH;(void)nH;(void)H;(void)TM;(void)TR;(void)F;return 1.;}
double rec_dxHIIdlna(HYREC_DATA*d,int m,double xe,double xH,double nH,double H,double TM,double TR,unsigned iz,double z){(void)iz;(void)z;d->error=0;return m==PEEBLES?rec_TLA_dxHIIdlna(d->cosmo,xe,xH,nH,H,TM,TR,1):rec_HMLA_dxHIIdlna(d,xe,xH,nH,H,TM,TR);}
'''
def native_fixture(root):
 root=Path(root).resolve();c=m.read(HERE/m.CONTRACT);base=m.identity(c,os.environ.get('GITHUB_RUN_ID','LOCAL'))
 with tempfile.TemporaryDirectory() as tmp:
  tmp=Path(tmp);(tmp/'fixture.c').write_text(FIXTURE);(tmp/'original.c').write_text(ORIGINAL)
  flags=['gcc','-std=c99','-O2','-Wall','-Wextra','-Werror','-Wno-unused-function','-Wno-unused-parameter','-fno-fast-math','-ffp-contract=off','-I'+str(HERE)]
  for d in ['include','external/HyRec2020','external/RecfastCLASS','external/heating']:flags+=['-I'+str(root/d)]
  subprocess.run(flags+['-shared','-fPIC',str(tmp/'original.c'),'-o',str(tmp/'libfixture.so')],check=True,timeout=60)
  subprocess.run(flags+['-rdynamic',str(tmp/'fixture.c'),'-Wl,--no-as-needed',str(tmp/'libfixture.so'),'-Wl,-rpath,'+str(tmp),'-ldl','-lm','-o',str(tmp/'fixture')],check=True,timeout=60)
  for extra in [0,1]:
   out=tmp/str(extra);out.mkdir();subprocess.run([str(tmp/'fixture'),str(out),base['config_sha256'],str(extra)],check=True,capture_output=True,timeout=10)
   for t in m.EXPECTED:
    for n in [1,2,4]:
     b=f'{t}-RK4-L{n}';ss=m.jsonl(out/(b+'_stages.jsonl'));nn=m.jsonl(out/(b+'_nodes.jsonl'));ep=m.read(out/(b+'_endpoint.json'))
     if extra:
      assert ep['execution_status']=='FAILED' and ss[0]['active_extra_event'] and len(ss)==1
      continue
     m.validate_branch(ss,nn,ep,c,base,t,n)
     # Independent integral: controlled pre rate2, post rate1, temperature rate1.
     span=c['protocol']['z_hi']-c['protocol']['z_lo'];pre=c['protocol']['z_hi']-c['protocol']['zstar'];post=c['protocol']['zstar']-c['protocol']['z_lo']
     assert abs(ep['end_y'][2]-(ep['start_y'][2]+2*pre+post))<2e-17
     assert abs(ep['end_y'][0]-(ep['start_y'][0]+span))<2e-13
     assert ss[4*n]['y']==ep['event_y'] # actual restart stage k1
     for mutate in ['missing','coordinate','restart','routing','ratio','nan']:
      bad=copy.deepcopy(ss)
      if mutate=='missing':bad.pop()
      elif mutate=='coordinate':bad[4*n-1]['eval_s']=bad[4*n-1]['logical_s']
      elif mutate=='restart':bad[4*n]['y'][2]+=1e-6
      elif mutate=='routing':bad[0]['model']=0
      elif mutate=='ratio':bad[0]['T_ratio']=.05
      elif mutate=='nan':bad[0]['dy'][2]=float('nan')
      try:m.validate_branch(bad,nn,ep,c,base,t,n)
      except ValueError:pass
      else:raise AssertionError('Accepted broken actual-native fixture '+mutate)
   if not extra and (HERE/'.github/workflows/00-bubbleverse-start.yml').is_file():
    # Exercise complete collection on deliberately labelled controlled artifacts.
    # Copied identity fields test transport/schema, not original-binary execution.
    m.write(out/'native_trial_manifest.json',dict(**base,expected_branches=6,branches=[dict(branch_id=b,child_exit_code=0,execution_status='COMPLETE') for b in c['protocol']['expected_branches']]))
    m.write(out/'execution_provenance.json',dict(**base,class_commit=c['class_commit'],class_binary_sha256=c['class_binary_sha256'],point_sha256=c['point_sha256'],source_tree_gate='PASS',adapter_fixture_gate='PASS',native_event_fixture_gate='PASS',controlled_fixture_only=True))
    (out/'adapter_samples.jsonl').write_text(''.join(json.dumps(dict(**base,probe=j,original_status=0,reduced_status=0,original_dy=[1.,0.,2.],reduced_dy=[1.,0.,2.]))+'\n' for j in range(3)))
    target=tmp/'collected.json';assert m.collect(out,target)==0;result=m.read(target)
    assert len(result['stages'])==112 and len(result['nodes'])==28 and len(result['endpoints'])==6 and not result['scientific_result'] and not result['history_accuracy_qualified']
    assert result['provenance']['controlled_fixture_only'] and result['final_result_gate']=='UNRESOLVED'
    assert result['run_id']==base['run_id']
    manifest=m.read(out/'native_trial_manifest.json');bad=copy.deepcopy(manifest);bad['run_id']='UNRELATED-RUN'
    m.write(out/'native_trial_manifest.json',bad);assert m.collect(out,target)==1
    assert 'RESULT_IDENTITY_GATE=FAIL' in m.read(target)['error']
    m.write(out/'native_trial_manifest.json',manifest)
    (out/'LOWER-RK4-L4_nodes.jsonl').unlink();assert m.collect(out,target)==1
    assert m.read(target)['technical_event_gate']=='FAIL'
 print('NATIVE_EVENT_FIXTURE_GATE=PASS six branches,112 stages, same-state restart, extra active event rejection and six corruption classes; controlled dependency only')
def identity_regression(root):
 for run_id in [None,'37344813050']:
  env=os.environ.copy()
  if run_id is None:env.pop('GITHUB_RUN_ID',None)
  else:env['GITHUB_RUN_ID']=run_id
  p=subprocess.run([sys.executable,str(HERE/'q042_event_tests_v28.py'),'native-fixture',str(Path(root).resolve())],env=env,capture_output=True,text=True,timeout=120)
  if p.returncode:raise AssertionError('Native fixture run identity '+str(run_id)+': '+p.stdout+p.stderr)
 print('RUN_IDENTITY_REGRESSION=PASS local and GitHub run-id; unrelated identity still rejected')
class FiniteTests(unittest.TestCase):
 def test_endpoint_contamination_and_failed_rhs_are_caught_by_real_C_kernel(self):
  with tempfile.TemporaryDirectory() as tmp:
   exe=str(Path(tmp)/'test');subprocess.run(['gcc','-std=c99','-O2','-Wall','-Wextra','-Werror','-fno-fast-math','-ffp-contract=off',str(HERE/'q042_event_numerics_test_v28.c'),'-lm','-o',exe],check=True,capture_output=True,timeout=60)
   result=subprocess.run([exe],capture_output=True,text=True,timeout=10);self.assertEqual(result.returncode,0,result.stdout+result.stderr)
 def test_missing_artifact_writes_explicit_failure_and_never_scientific_success(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)/'result.json';self.assertEqual(m.collect(tmp,out),1);result=m.read(out)
   self.assertEqual(result['technical_event_gate'],'FAIL');self.assertFalse(result['scientific_result']);self.assertEqual(result['final_result_gate'],'UNRESOLVED')
   self.assertIn('native_trial_manifest.json',result['error'])
 def test_no_forced_order_when_differences_below_roundoff_diagnostic(self):
  ep=[dict(trial=t,level=n,event_y=[1.,0.,.001],end_y=[1.,0.,.001]) for t in m.EXPECTED for n in [1,2,4]]
  a=m.analyze(ep);self.assertIsNone(a['UPPER']['end_y']['x_H']['observed_log2_order'])
  self.assertFalse(a['LOWER']['end_y']['D_Tmat']['error_bound'])
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='native-fixture':native_fixture(sys.argv[2])
 elif len(sys.argv)>1 and sys.argv[1]=='identity-regression':identity_regression(sys.argv[2])
 else:unittest.main()
