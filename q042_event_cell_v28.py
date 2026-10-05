"""Q-042 V28: one conditional event-aware crossing cell; no full history/inference."""
from pathlib import Path
import argparse,csv,hashlib,json,math,os,platform,re,signal,shutil,subprocess,sys,sysconfig,time
HERE=Path(__file__).resolve().parent
Q='Q-042';PROGRAM_ID='Q042-EVENTCELL-V28';CONTRACT='q042_event_contract_v28.json';EXPECTED=['UPPER','LOWER']
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
 root=Path(root);c=read(root/CONTRACT);m=read(root/'q042_event_manifest_v28.json')
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

def finite(v):return isinstance(v,(float,int)) and not isinstance(v,bool) and math.isfinite(v)
def require(ok,msg):
 if not ok:raise ValueError(msg+'=FAIL')
def matching(x,base):
 require(all(x.get(k)==base[k] for k in ['q','program_id','run_id','config_sha256']),'RESULT_IDENTITY_GATE')
def validate_branch(stages,nodes,endpoint,c,base,t,n):
 branch=f'{t}-RK4-L{n}';anchor=next(x['state_D_He_H'] for x in c['anchors'] if x['trial']==t)
 limits=[-c['protocol'][k] for k in ['z_hi','zstar','z_lo']]
 matching(endpoint,base)
 require(endpoint.get('branch_id')==branch and endpoint.get('trial')==t and endpoint.get('level')==n,'BRANCH_IDENTITY_GATE')
 require(endpoint.get('execution_status')=='COMPLETE' and endpoint.get('rhs_calls')==8*n,'BRANCH_COMPLETENESS_GATE')
 require(endpoint.get('start_y')==anchor and endpoint.get('zstar')==c['protocol']['zstar'],'FROZEN_START_GATE')
 require(len(stages)==8*n and len(nodes)==2*n,'STAGE_COMPLETENESS_GATE')
 accepted=anchor[:];event=None;index=0;ni=0
 for seg in [0,1]:
  for step in range(n):
   begin=limits[seg] if not step else limits[seg]+(limits[seg+1]-limits[seg])*step/n
   end=limits[seg+1] if step==n-1 else limits[seg]+(limits[seg+1]-limits[seg])*(step+1)/n
   h=end-begin;ks=[]
   for stage in [1,2,3,4]:
    x=stages[index];index+=1;matching(x,base)
    require(all(x.get(k)==v for k,v in dict(branch_id=branch,trial=t,level=n,segment=seg,step=step,stage=stage).items()),'STAGE_ORDER_GATE')
    logical=begin if stage==1 else end if stage==4 else begin+.5*h
    eval_s=math.nextafter(end,-math.inf) if seg==0 and step==n-1 and stage==4 else logical
    require(x.get('logical_s')==logical and x.get('eval_s')==eval_s and x.get('z')==-eval_s,'STAGE_COORDINATE_GATE')
    require(len(x.get('y',[]))==3 and len(x.get('dy',[]))==3,'VECTOR_GATE')
    require(all(finite(v) for v in x['y']+x['dy']+[x.get('TR_eV'),x.get('T_ratio'),x.get('x_noreio'),x.get('x_reio_rhs')]),'FINITE_STAGE_GATE')
    expected=accepted[:]
    if stage>1:
     for j in [0,2]:expected[j]=accepted[j]+h*(1. if stage==4 else .5)*ks[2 if stage==4 else stage-2][j]
    require(x['y']==expected and x['dy'][1]==0.,'STATE_HE_AND_RESTART_GATE')
    require(x.get('kernel_calls')==1 and x.get('kernel_error')==0 and x.get('status')==0 and x.get('stage_gate')=='PASS' and not x.get('error'),'ORIGINAL_RHS_GATE')
    require(x.get('model')==(4 if seg==0 else 0) and x.get('hmla_calls')==(1 if seg==0 else 0) and x.get('tla_calls')==(0 if seg==0 else 1),'KERNEL_ROUTING_GATE')
    require((x['TR_eV']>.004)==(seg==0),'ORIGINAL_THRESHOLD_GATE')
    require(not x.get('active_extra_event') and (seg!=0 or x['T_ratio']>.1),'EXTRA_ACTIVE_EVENT_GATE')
    require(x.get('masked_ratio_predicate')==(seg==1 and x['T_ratio']<=.1),'MASKED_PREDICATE_GATE')
    ks.append(x['dy'])
   for j in [0,2]:accepted[j]+=h*(ks[0][j]+2*ks[1][j]+2*ks[2][j]+ks[3][j])/6.
   require(all(finite(v) for v in accepted),'FINITE_ACCEPTED_STATE_GATE')
   node=nodes[ni];ni+=1;matching(node,base)
   require(all(node.get(k)==v for k,v in dict(branch_id=branch,trial=t,level=n,segment=seg,step=step,s=end).items()) and node.get('y')==accepted,'ACCEPTED_NODE_GATE')
   if seg==0 and step==n-1:event=accepted[:]
 require(endpoint.get('event_y')==event and endpoint.get('end_y')==accepted,'ENDPOINT_GATE')
 return dict(branch_id=branch,stages=len(stages),nodes=len(nodes),minimum_stage_ratio=min(x['T_ratio'] for x in stages),masked_ratio_stages=sum(x['masked_ratio_predicate'] for x in stages),one_sided_endpoint_z=stages[4*n-1]['z'])
def analyze(endpoints):
 out={}
 for t in EXPECTED:
  values={x['level']:x for x in endpoints if x['trial']==t};diagnostics={}
  for position in ['event_y','end_y']:
   diagnostics[position]={}
   for j,label in [(0,'D_Tmat'),(2,'x_H')]:
    vals=[values[n][position][j] for n in [1,2,4]];d12=vals[0]-vals[1];d24=vals[1]-vals[2]
    floor=32*sys.float_info.epsilon*max(1.,*(abs(v) for v in vals))
    resolved=min(abs(d12),abs(d24))>floor
    diagnostics[position][label]=dict(values_L1_L2_L4=vals,signed_L1_minus_L2=d12,signed_L2_minus_L4=d24,heuristic_roundoff_floor=floor,absolute_difference_ratio=abs(d12/d24) if resolved else None,observed_log2_order=math.log2(abs(d12/d24)) if resolved else None,order_status='RESOLVED_ABOVE_HEURISTIC_FLOOR' if resolved else 'NOT_RESOLVED_ABOVE_HEURISTIC_ROUNDOFF',error_bound=False,richardson_estimate='WITHHELD_NO_SEGMENT_SMOOTHNESS_OR_ASYMPTOTIC_CERTIFICATION')
  out[t]=diagnostics
 return out
def jsonl(p):
 with Path(p).open() as stream:return [json.loads(line,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('NONSTANDARD_JSON_NUMBER '+x))) for line in stream if line.strip()]
def collect(directory,out):
 c=read(HERE/CONTRACT);run=os.environ.get('GITHUB_RUN_ID','LOCAL');base=identity(c,run);d=Path(directory);stages=[];nodes=[];endpoints=[];checks=[];error='';native=None;provenance='NOT DOCUMENTED'
 try:
  static();native=read(d/'native_trial_manifest.json');matching(native,base)
  expected=c['protocol']['expected_branches'];branches=native.get('branches',[])
  require(native.get('expected_branches')==6 and len(branches)==6 and {x['branch_id'] for x in branches}==set(expected) and all(x['child_exit_code']==0 and x['execution_status']=='COMPLETE' for x in branches),'JOB_COMPLETENESS_GATE')
  provenance=read(d/'execution_provenance.json');matching(provenance,base)
  require(provenance.get('class_binary_sha256')==c['class_binary_sha256'] and provenance.get('class_commit')==c['class_commit'] and provenance.get('point_sha256')==c['point_sha256'] and provenance.get('source_tree_gate')=='PASS' and provenance.get('adapter_fixture_gate')=='PASS' and provenance.get('native_event_fixture_gate')=='PASS','EXECUTION_PROVENANCE_GATE')
  adapter=jsonl(d/'adapter_samples.jsonl');require(len(adapter)==3 and [x['probe'] for x in adapter]==[0,1,2],'ADAPTER_COMPLETENESS_GATE')
  for x in adapter:
   matching(x,base);require(x.get('original_status')==0 and x.get('reduced_status')==0 and len(x['original_dy'])==3 and x['original_dy']==x['reduced_dy'] and all(finite(v) for v in x['original_dy']) and x['reduced_dy'][1]==0,'LIVE_ADAPTER_GATE')
  for t in EXPECTED:
   for n in [1,2,4]:
    b=f'{t}-RK4-L{n}';ss=jsonl(d/(b+'_stages.jsonl'));nn=jsonl(d/(b+'_nodes.jsonl'));ep=read(d/(b+'_endpoint.json'))
    stages+=ss;nodes+=nn;endpoints.append(ep);checks.append(validate_branch(ss,nn,ep,c,base,t,n))
  require(len(stages)==112,'TOTAL_STAGE_GATE')
 except Exception as e:error=type(e).__name__+': '+str(e)
 result=dict(**base,execution_status='COMPLETE' if not error else 'PARTIAL_OR_FAILED',technical_event_gate='PASS' if not error else 'FAIL',local_method_accuracy_status='DIAGNOSTIC_ONLY_NOT_CERTIFIED' if not error else 'UNRESOLVED',error=error,native_manifest=native,branch_checks=checks,endpoints=endpoints,stages=stages,nodes=nodes,diagnostics=analyze(endpoints) if not error else {},artifacts={p.name:sha(p) for p in d.iterdir() if p.is_file()} if d.is_dir() else {},provenance=provenance,return_route='Result Ingestion & Routing Engine',stop='ONE_PASS_COMPLETE_RETURN_NOW; no additional level or history campaign')
 write(out,result);return 0 if not error else 1

def run(out):
 out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True);c=read(HERE/CONTRACT);run=os.environ.get('GITHUB_RUN_ID','LOCAL');base=identity(c,run)
 if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',run):raise ValueError('RUN_ID_GATE=FAIL')
 try:
  if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1':raise ValueError('NO_RETRY_GATE=FAIL')
  if any(out.glob('*_stages.jsonl')):raise ValueError('OUTPUT_REUSE_GATE=FAIL')
  static();root=HERE/'external/class_ede';binary=source_preflight(root,c);exe=out/'q042_event_native_v28'
  with (out/'adapter_fixture.log').open('w') as log:subprocess.run([sys.executable,str(HERE/'q042_event_adapter_selftest_v28.py'),str(root)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
  with (out/'native_fixture.log').open('w') as log:subprocess.run([sys.executable,str(HERE/'q042_event_tests_v28.py'),'native-fixture',str(root)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
  libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
  if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib:raise ValueError('PYTHON_LINK_GATE=FAIL')
  cmd=['gcc','-O2','-std=c99','-fopenmp','-rdynamic','-fno-fast-math','-ffp-contract=off','-I'+str(HERE)]
  for n in ['include','external/HyRec2020','external/RecfastCLASS','external/heating']:cmd+=['-I'+str(root/n)]
  cmd += [str(HERE/'q042_event_native_v28.c'),str(binary),'-L'+libdir,'-l'+ldlib[3:].split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
  with (out/'compile.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
  point=out/'point.ini';shutil.copyfile(HERE/c['point_file'],point)
  env=os.environ.copy();env.update(Q042_REFACQ_DIR=str(out),Q042_REFACQ_RUN=run,Q042_REFACQ_CONFIG_SHA256=base['config_sha256'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
  write(out/'execution_provenance.json',dict(**base,execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),source_tree_gate='PASS',adapter_fixture_gate='PASS',native_event_fixture_gate='PASS',class_commit=c['class_commit'],binary_route=str(binary),class_binary_sha256=sha(binary),point_sha256=sha(point),executable_sha256=sha(exe),compile_command=cmd,command=[str(exe),str(point)],python_version=platform.python_version(),platform=platform.platform(),compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],thread_policy={k:env[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']}))
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
 p=argparse.ArgumentParser();p.add_argument('command',choices=['static','run','collect']);p.add_argument('--out',default='event_cell');p.add_argument('--directory',default='collected');a=p.parse_args()
 if a.command=='static':static();return 0
 return run(a.out) if a.command=='run' else collect(a.directory,a.out)
if __name__=='__main__':sys.exit(main())
