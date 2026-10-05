"""Q-042 V27: one bounded original-binary fixed-state switch probe; no integration."""
from pathlib import Path
import argparse,csv,hashlib,json,math,os,platform,re,signal,shutil,subprocess,sys,sysconfig,time
HERE=Path(__file__).resolve().parent
Q='Q-042';PROGRAM_ID='Q042-SWITCHPROBE-V27';CONTRACT='q042_switch_contract_v27.json';EXPECTED=['UPPER','LOWER']
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def identity(c,run):
 return dict(q=Q,case_id=c['case_id'],scientific_question=c['scientific_question'],program_id=PROGRAM_ID,run_id=run,config_sha256=sha(HERE/CONTRACT),original_scientific_spec_sha256=c['original_scientific_spec_sha256'],result_status='RAW_NOT_QUALIFIED',scientific_result=False,history_accuracy_qualified=False,prediction_likelihood_qualified=False,reference_truth_gate='BLOCKED',final_result_gate='UNRESOLVED',production_restart_authorized=False)
def static(root=HERE):
 root=Path(root);c=read(root/CONTRACT);m=read(root/'q042_switch_manifest_v27.json')
 if c['q']!=Q or c['program_id']!=PROGRAM_ID or c['expected_trials']!=EXPECTED:raise ValueError('CONTEXT_GATE=FAIL')
 if any(c[k] for k in ['root_search_authorized','production_restart_authorized','reference_truth_qualified']):raise ValueError('SCOPE_GATE=FAIL')
 for n,h in m['immutable_files'].items():
  if not (root/n).is_file() or sha(root/n)!=h:raise ValueError('PACKAGE_HASH_GATE=FAIL '+n)
 reg=read(root/'bubbleverse_program_registry.json')['programs']
 if reg.get(PROGRAM_ID)!=m['registry_entry'] or not (root/m['registry_entry']['workflow_path']).is_file():raise ValueError('REGISTRY_GATE=FAIL')
 if sha(root/'.github/workflows/00-bubbleverse-start.yml')!=m['canonical_launcher_sha256']:raise ValueError('LAUNCHER_IDENTITY_GATE=FAIL')
 doc=(root/'README.md').read_text()
 for n in [PROGRAM_ID,'00-bubbleverse-start.yml','bubbleverse_program_registry.json','RAW_NOT_QUALIFIED']:
  if n not in doc:raise ValueError('README_GATE=FAIL '+n)
 if sha(root/c['point_file'])!=c['point_sha256']:raise ValueError('POINT_GATE=FAIL')
 print('PACKAGE_GATE=PASS REGISTRY_GATE=PASS README_GATE=PASS LAUNCHER_GATE=PASS');return c
def source_preflight(root,c):
 if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=c['class_commit']:raise ValueError('CLASS_COMMIT_GATE=FAIL')
 subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
 for n,h in c['frozen_source_hashes'].items():
  if sha(root/n)!=h:raise ValueError('SOURCE_HASH_GATE=FAIL '+n)
 bins=[x for x in root.rglob('classy*.so') if sha(x)==c['class_binary_sha256']]
 if len(bins)!=1:raise ValueError('BINARY_GATE=FAIL')
 return bins[0]
def validate_samples(rows,run,config,trials):
 wanted={(t,o,i,s) for t in trials for o in [0,1] for i in [0,1,2] for s in [-1,1]};seen=set()
 for x in rows:
  if any(x.get(k)!=v for k,v in dict(q=Q,program_id=PROGRAM_ID,run_id=run,config_sha256=config).items()):raise ValueError('SAMPLE_IDENTITY_GATE=FAIL')
  if x.get('branch_id')!=x.get('trial'):raise ValueError('BRANCH_IDENTITY_GATE=FAIL')
  key=tuple(x.get(k) for k in ['trial','order','epsilon_index','side'])
  if key not in wanted or key in seen:raise ValueError('SAMPLE_COMPLETENESS_GATE=FAIL duplicate/unexpected')
  seen.add(key);low=x['side']==-1
  if x.get('status')!=0 or x.get('kernel_error')!=0 or x.get('kernel_calls')!=1:raise ValueError('KERNEL_ROUTING_GATE=FAIL')
  if x.get('model')!=(0 if low else 4) or x.get('hmla_calls')!=(0 if low else 1) or x.get('tla_calls')!=(1 if low else 0):raise ValueError('MODEL_ROUTING_GATE=FAIL')
  if not all(math.isfinite(float(v)) for v in x['dy']+x['y']+[x['z'],x['TR_eV'],x['T_ratio']]) or x['dy'][1]!=0:raise ValueError('FINITE_INACTIVE_HE_GATE=FAIL')
  if x['T_ratio']<=.1 or ((x['TR_eV']<=.004)!=low):raise ValueError('THRESHOLD_BRACKET_GATE=FAIL')
  if x.get('epsilon')!=[1e-6,1e-8,1e-10][x['epsilon_index']]:raise ValueError('EPSILON_GATE=FAIL')
 if seen!=wanted:raise ValueError('SAMPLE_COMPLETENESS_GATE=FAIL missing')
def jump_weight_error(method,n,theta,H):
 if method not in ['RK4','MIDPOINT'] or n not in [1,2,4] or not 0<theta<1 or H<=0:raise ValueError('INVALID_WEIGHT_GEOMETRY')
 weights=[(0,1/6),(.5,2/3),(1,1/6)] if method=='RK4' else [(.5,1.)]
 sampled=math.fsum(w/n for j in range(n) for cc,w in weights if (j+cc)/n>=theta)
 return H*(sampled-(1-theta))
def analyze(rows):
 result={}
 for t in EXPECTED:
  r=[x for x in rows if x['trial']==t];jumps=[];repeat=[]
  for i in [0,1,2]:
   pair=[next(x for x in r if x['order']==0 and x['epsilon_index']==i and x['side']==s) for s in [-1,1]]
   jumps.append(dict(epsilon=pair[0]['epsilon'],post_minus_pre=[pair[0]['dy'][j]-pair[1]['dy'][j] for j in [0,2]]))
  for x in r:
   if x['order']==0:
    y=next(y for y in r if y['order']==1 and y['epsilon_index']==x['epsilon_index'] and y['side']==x['side']);repeat.append(max(abs(a-b) for a,b in zip(x['dy'],y['dy'])))
  result[t]=dict(jumps=jumps,max_forward_reverse_derivative_difference=max(repeat),causal_conclusion='UNRESOLVED_FOR_INGESTION',interpretation='Actual one-sided fixed-state derivative differences; finite offsets are not exact limits or global history bounds.')
 return result
def collect(directory,out):
 c=read(HERE/CONTRACT);run=os.environ.get('GITHUB_RUN_ID','LOCAL');base=identity(c,run);d=Path(directory);rows=[];error='';native=None
 try:
  native=read(d/'native_trial_manifest.json')
  if any(native.get(k)!=base[k] for k in ['q','program_id','run_id','config_sha256']):raise ValueError('MANIFEST_IDENTITY_GATE=FAIL')
  if native.get('expected_trials')!=2 or len(native.get('trials',[]))!=2 or {x['trial'] for x in native['trials']}!=set(EXPECTED) or any(x['child_exit_code']!=0 or x['execution_status']!='COMPLETE' for x in native['trials']):raise ValueError('JOB_COMPLETENESS_GATE=FAIL')
  for t in EXPECTED:
   with (d/(t+'_samples.jsonl')).open() as stream:rows.extend(json.loads(line,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('NONSTANDARD_JSON_NUMBER '+x))) for line in stream if line.strip())
  validate_samples(rows,run,base['config_sha256'],EXPECTED)
  for x in rows:
   if x['y']!=next(a['state_D_He_H'] for a in c['anchors'] if a['trial']==x['trial']):raise ValueError('FIXED_STATE_GATE=FAIL')
 except Exception as e:error=type(e).__name__+': '+str(e)
 # Raw files are preserved even when parsing/routing/completeness fails.
 result=dict(**base,execution_status='COMPLETE' if not error else 'PARTIAL_OR_FAILED',technical_probe_gate='PASS' if not error else 'FAIL',error=error,native_manifest=native,samples=rows,diagnostics=analyze(rows) if not error else {},artifacts={p.name:sha(p) for p in d.iterdir() if p.is_file()} if d.is_dir() else {},provenance=read(d/'execution_provenance.json') if (d/'execution_provenance.json').is_file() else 'NOT DOCUMENTED',return_route='Result Ingestion & Routing Engine')
 write(out,result);return 0 if not error else 1
def run(out):
 out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True);c=read(HERE/CONTRACT);run=os.environ.get('GITHUB_RUN_ID','LOCAL');base=identity(c,run)
 if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',run):raise ValueError('RUN_ID_GATE=FAIL')
 try:
  if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1':raise ValueError('NO_RETRY_GATE=FAIL')
  if any(out.glob('*_samples.jsonl')):raise ValueError('OUTPUT_REUSE_GATE=FAIL')
  static();root=HERE/'external/class_ede';binary=source_preflight(root,c);exe=out/'q042_switch_native_v27'
  with (out/'adapter_fixture.log').open('w') as log:subprocess.run([sys.executable,str(HERE/'q042_switch_adapter_selftest_v27.py'),str(root)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
  libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
  if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib:raise ValueError('PYTHON_LINK_GATE=FAIL')
  cmd=['gcc','-O2','-std=c99','-fopenmp','-rdynamic','-fno-fast-math','-ffp-contract=off','-I'+str(HERE)]
  for n in ['include','external/HyRec2020','external/RecfastCLASS','external/heating']:cmd+=['-I'+str(root/n)]
  cmd += [str(HERE/'q042_switch_native_v27.c'),str(binary),'-L'+libdir,'-l'+ldlib[3:].split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
  with (out/'compile.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
  point=out/'point.ini';shutil.copyfile(HERE/c['point_file'],point)
  env=os.environ.copy();env.update(Q042_REFACQ_DIR=str(out),Q042_REFACQ_RUN=run,Q042_REFACQ_CONFIG_SHA256=base['config_sha256'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
  write(out/'execution_provenance.json',dict(**base,execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),source_tree_gate='PASS',adapter_fixture_gate='PASS',class_commit=c['class_commit'],binary_route=str(binary),class_binary_sha256=sha(binary),point_sha256=sha(point),executable_sha256=sha(exe),compile_command=cmd,command=[str(exe),str(point)],python_version=platform.python_version(),platform=platform.platform(),compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],thread_policy={k:env[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']}))
  with (out/'native.log').open('w') as log:
   p=subprocess.Popen([str(exe),str(point)],cwd=HERE,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);deadline=time.monotonic()+160
   while p.poll() is None:
    if time.monotonic()>deadline or sum(x.stat().st_size for x in out.rglob('*') if x.is_file())>16*1024*1024:
     os.killpg(p.pid,signal.SIGKILL);p.wait();raise ValueError('WALL_OR_STORAGE_CAP')
    time.sleep(.2)
   if p.returncode:raise ValueError('NATIVE_EXIT_GATE=FAIL '+str(p.returncode))
 except Exception as e:
  write(out/'execution_failure.json',dict(**base,error=type(e).__name__+': '+str(e)));raise
 return collect(out,out/'worker_result.json')
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['static','run','collect']);p.add_argument('--out',default='switch_probe');p.add_argument('--directory',default='collected');a=p.parse_args()
 if a.command=='static':static();return 0
 return run(a.out) if a.command=='run' else collect(a.directory,a.out)
if __name__=='__main__':sys.exit(main())
