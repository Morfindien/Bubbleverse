"""Q-042 bounded initialization capture + real-table interval qualification.
One original prefix, 24 independent diagnostic points, no trajectory or search.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,re,signal,subprocess,sys,sysconfig,time,urllib.request

HERE=Path(__file__).resolve().parent
ID='Q042-CONTEXT-V29';Q='Q-042';CONTRACT='q042_context_contract_v29.json';MANIFEST='q042_context_manifest_v29.json'
RESULT='q042_context_result_v29.json'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('DUPLICATE_JSON_KEY '+k)
        out[k]=v
    return out
def read(p): return json.loads(Path(p).read_text(),object_pairs_hook=unique_pairs)
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def base():
    c=read(HERE/CONTRACT)
    return dict(q=Q,case_id=c['case_id'],scientific_question=c['scientific_question'],program_id=ID,run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),config_sha256=sha(HERE/CONTRACT),original_scientific_spec_sha256=c['original_scientific_spec_sha256'],result_status='PROVISIONAL_TECHNICAL_PREREQUISITE',scientific_result=False,history_accuracy_gate='BLOCKED',reference_truth_gate='BLOCKED',binary_arithmetic_bound_gate='UNRESOLVED',final_result_gate='UNRESOLVED',production_restart_authorized=False)

def static():
    c=read(HERE/CONTRACT);m=read(HERE/MANIFEST)
    if c['q']!=Q or c['program_id']!=ID or c['version']!=29: raise ValueError('CONTEXT_GATE')
    for k in ('production_restart_authorized','history_integration_authorized','root_search_authorized'):
        if c[k]: raise ValueError('SCOPE_GATE '+k)
    for n,h in m['immutable_files'].items():
        if not(HERE/n).is_file() or sha(HERE/n)!=h: raise ValueError('PACKAGE_HASH_GATE '+n)
    reg=read(HERE/'bubbleverse_program_registry.json')['programs']
    if reg.get(ID)!=m['registry_entry']: raise ValueError('REGISTRY_GATE')
    if reg[ID]['q']!=Q or reg[ID]['status']!='ACTIVE' or reg[ID]['workflow_id']!='q042-context-v29.yml': raise ValueError('TARGET_GATE')
    for old in ('Q042-REFACQ-V26','Q042-SWITCHPROBE-V27','Q042-EVENTCELL-V28'):
        if reg[old]['status']!='COMPLETED': raise ValueError('OLD_CAMPAIGN_RETIREMENT_GATE')
    if sha(HERE/'.github/workflows/00-bubbleverse-start.yml')!=m['canonical_launcher_sha256']: raise ValueError('LAUNCHER_GATE')
    doc=(HERE/'README.md').read_text()
    for s in (ID,'00-bubbleverse-start.yml','bubbleverse_program_registry.json','real-table','UNRESOLVED'):
        if s not in doc: raise ValueError('README_GATE '+s)
    if sha(HERE/c['point_file'])!=c['point_sha256']: raise ValueError('POINT_GATE')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS REGISTRY_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')
    return c

def one_attempt():
    if os.environ.get('GITHUB_RUN_ATTEMPT')!='1': raise ValueError('NO_RETRY_GATE')
    repo=os.environ.get('GITHUB_REPOSITORY');run=os.environ.get('GITHUB_RUN_ID')
    if repo!='Morfindien/Bubbleverse' or not run or not run.isdecimal(): raise ValueError('AUTHORIZED_REPOSITORY_RUN_GATE')
    req=urllib.request.Request('https://api.github.com/repos/'+repo+'/actions/workflows/q042-context-v29.yml/runs?event=workflow_dispatch&per_page=100',headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=30) as r: response=json.load(r)
    others=[x['id'] for x in response['workflow_runs'] if str(x['id'])!=run]
    if others or response['total_count']!=1: raise ValueError('ONE_CAMPAIGN_GATE previous_or_parallel_runs='+str(others))

def source_preflight(root,c):
    commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if commit!=c['class_commit']: raise ValueError('CLASS_COMMIT_GATE '+commit)
    subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
    for n,h in c['frozen_source_hashes'].items():
        if sha(root/n)!=h: raise ValueError('SOURCE_HASH_GATE '+n)
    binaries=[p for p in root.rglob('classy*.so') if sha(p)==c['class_binary_sha256']]
    if len(binaries)!=1: raise ValueError('ORIGINAL_BINARY_GATE matches='+str(len(binaries)))
    return binaries[0]

def qualify(out):
    from q042_interval_v29 import Evaluator,I,VERSION,jsonable
    context=read(out/'initialized_context.json');grid=read(out/'native_grid_hex.json');identity=base()
    for x in (context,grid):
        for k in ('q','program_id','run_id','config_sha256'):
            if x[k]!=identity[k]: raise ValueError('CAPTURE_IDENTITY '+k)
    if context.get('fixture_only') or context['grid_size']!=28333 or len(grid['rows'])!=28333 or context['tau_search_executed'] or context['history_integrated']: raise ValueError('CAPTURE_SCOPE_GATE')
    if context['accepted_D_He_H']!=[float(x).hex() for x in (-86.955287923490403,1.2261504557092879e-5,.00024187860481588748)]:
        # C %a omits insignificant trailing zeroes; compare exact binary64 bits.
        if [float.fromhex(x) for x in context['accepted_D_He_H']]!=[-86.955287923490403,1.2261504557092879e-5,.00024187860481588748]: raise ValueError('ENTRY_GATE')
    rows=[[float.fromhex(x) for x in row] for row in grid['rows']]
    if any(b[0]<=a[0] or b[1]>=a[1] or b[2]<=a[2] for a,b in zip(rows,rows[1:])): raise ValueError('GRID_ORDER_GATE')
    if any(rows[i][0]!=-rows[-1-i][2] for i in range(len(rows))): raise ValueError('GRID_INDEX_MAPPING_GATE')
    e=Evaluator(context);positivity=e.positivity()
    points=[json.loads(s) for s in (out/'original_rhs_points.jsonl').read_text().splitlines()]
    expected={(t,j) for t in ('UPPER','LOWER') for j in range(12)}
    keys=[(x['branch_id'],x['point']) for x in points]
    if len(keys)!=24 or set(keys)!=expected: raise ValueError('POINT_COMPLETENESS_GATE')
    boxes=[]
    for p in points:
        for key in ('q','program_id','run_id','config_sha256'):
            if p[key]!=identity[key]: raise ValueError('POINT_IDENTITY '+key)
        if p['original_status']!=0 or p['dy_D_He_H'][1]!=0: raise ValueError('POINT_ORIGINAL_STATUS')
        z=float.fromhex(p['z']);D,he,xh=map(float.fromhex,p['D_He_H'])
        # Directed construction of the fixed nonzero diagnostic boxes.
        zb=(I(z)+I(-1e-8,1e-8)).intersect(0.,50.)
        db=I(D)+I(-1e-6,1e-6);hb=I(xh)+I(-1e-9,1e-9)
        r=e.rhs(zb,db,hb,p['branch_id']);r.update(e.source_xe_dkappa(zb,r['xe_noreio'],r['xe_reio']))
        if not r['dD_ds'].contains(p['dy_D_He_H'][0]) or not r['dxH_ds'].contains(p['dy_D_He_H'][2]): raise ValueError('ORIGINAL_POINT_CONTAINMENT_DIAGNOSTIC point='+str((p['branch_id'],p['point'])))
        boxes.append({'trial':p['branch_id'],'point':p['point'],'z':jsonable(zb),'D':jsonable(db),'xH':jsonable(hb),'output':jsonable(r)})
    maps=Path('/proc/self/maps').read_text().splitlines()
    libs=sorted({s.split()[-1] for s in maps if ('libmpfr' in s or 'libgmp' in s or 'libm.so' in s) and s.split()[-1].startswith('/')})
    context_manifest={'q':Q,'program_id':ID,'run_id':identity['run_id'],'config_sha256':identity['config_sha256'],'context_sha256':sha(out/'initialized_context.json'),'grid_sha256':sha(out/'native_grid_hex.json'),'dimensions':{'background_rows':len(e.bg),'background_columns':5,'logAlpha':[4,40,100],'logR':100,'native_grid_rows':28333},'number_encoding':'C99 hexadecimal exact binary64','units':{'z':'dimensionless','D':'K','xH':'H-nucleus fraction','xHe':'He-nucleus fraction','H':'Mpc^-1','rho_g':'Mpc^-2','TR':'eV','nH0':'m^-3','logAlpha':'ln(cm^3/s)','logR':'ln(s^-1)'},'arithmetic':{'MPFR':VERSION,'precision':256,'endpoint_rounding':'RNDD/RNDU including binary64 export','loaded_library_sha256':{p:sha(p) for p in libs}}}
    write(out/'initialized_context_manifest.json',context_manifest)
    result={'q':Q,'program_id':ID,'real_table_box_gate':'PASS_EXPLICIT_BOXES_ONLY','background_positivity':positivity,'box_count':len(boxes),'boxes':boxes,'proof_scope':'Interval composition with directed elementary functions and enumeration of all intersected stencils; explicit admissible boxes only. Original-point containment is a diagnostic, not the enclosure proof.','binary_arithmetic_bound_gate':'UNRESOLVED','upstream_accuracy_gate':'UNRESOLVED','history_accuracy_gate':'BLOCKED'}
    write(out/'interval_qualification.json',result)
    return result

def run(out):
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True);b=base();started=time.monotonic();error='';provenance={};q=None
    write(out/'attempt.json',dict(**b,status='PREFLIGHT_PENDING'))
    try:
        if any((out/n).exists() for n in (RESULT,'initialized_context.json')): raise ValueError('OUTPUT_REUSE_GATE')
        c=static();one_attempt();root=HERE/'external/class_ede';binary=source_preflight(root,c)
        with (out/'unit_tests.log').open('w') as log: subprocess.run([sys.executable,'-m','unittest','discover','-s',str(HERE),'-p','q042_interval_tests_v29.py','-v'],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
        with (out/'source_fixture.log').open('w') as log:
            subprocess.run([sys.executable,str(HERE/'q042_source_check_v29.py'),str(root),str(out/'source_fixture.json')],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        libdir=sysconfig.get_config_var('LIBDIR');ldlib=sysconfig.get_config_var('LDLIBRARY')
        if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib: raise ValueError('PYTHON_LINK_GATE')
        exe=out/'q042_context_native_v29';cmd=['gcc','-O2','-std=c99','-fopenmp','-rdynamic','-fno-fast-math','-ffp-contract=off']
        for p in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'): cmd+=['-I'+str(root/p)]
        cmd += [str(HERE/'q042_context_native_v29.c'),str(binary),'-L'+libdir,'-l'+ldlib[3:].split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        with (out/'compile.log').open('w') as log: subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        env=os.environ.copy();env.update(Q042_CONTEXT_DIR=str(out),Q042_CONTEXT_RUN=b['run_id'],Q042_CONTEXT_CONFIG_SHA256=b['config_sha256'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
        provenance=dict(class_commit=c['class_commit'],class_binary_sha256=sha(binary),point_sha256=sha(HERE/c['point_file']),execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),executable_sha256=sha(exe),compile_command=cmd,command=[str(exe),str(HERE/c['point_file'])],python=platform.python_version(),platform=platform.platform(),compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],thread_policy={k:env[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')})
        write(out/'execution_provenance.json',dict(**b,provenance=provenance))
        with (out/'original_capture.log').open('w') as log:
            proc=subprocess.Popen(provenance['command'],cwd=HERE,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            deadline=time.monotonic()+600
            try:
                while proc.poll() is None:
                    if time.monotonic()>deadline or sum(p.stat().st_size for p in out.rglob('*') if p.is_file())>128*1024*1024: raise ValueError('CAPTURE_WALL_STORAGE_CAP')
                    time.sleep(.2)
            finally:
                if proc.poll() is None: os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            if proc.returncode: raise ValueError('NATIVE_CAPTURE_GATE exit='+str(proc.returncode))
        # Separate bounded process: interval work cannot restart initialization.
        with (out/'qualification.log').open('w') as log:
            subprocess.run([sys.executable,str(HERE/'q042_context_v29.py'),'qualify','--out',str(out)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=300)
        q=read(out/'interval_qualification.json')
    except Exception as exc: error=type(exc).__name__+': '+str(exc)
    files={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!=RESULT}
    write(out/'job_manifest.json',dict(**b,expected_jobs=['capture_and_qualify'],completed_jobs=['capture_and_qualify'] if q else [],failed_jobs=[] if q else ['capture_and_qualify'],pending_jobs=[],status='COMPLETE' if q else 'PARTIAL'))
    files['job_manifest.json']=sha(out/'job_manifest.json')
    result=dict(**b,execution_status='COMPLETE' if q is not None and not error else 'PARTIAL',context_gate='PASS' if q else 'FAIL_OR_NOT_QUALIFIED',real_table_box_gate=q['real_table_box_gate'] if q else 'NOT_ESTABLISHED',error=error,elapsed_seconds=time.monotonic()-started,provenance=provenance,artifacts=files,actual_computed_result='INITIALIZED_CONTEXT_AND_REAL_TABLE_BOXES' if q else 'NO_QUALIFIED_PREREQUISITE',expected_jobs=['capture_and_qualify'],next_motor='Result Ingestion & Routing Engine',stop='No retry; ingest success or concrete failure. No production or history authorization.')
    write(out/RESULT,result);return 0 if result['execution_status']=='COMPLETE' else 1

def collect(directory,out):
    b=base();found=list(Path(directory).rglob(RESULT));errors=[];result=None
    try:
        if len(found)!=1: raise ValueError('JOB_COMPLETENESS_GATE count='+str(len(found)))
        result=read(found[0])
        for k in ('q','program_id','run_id','config_sha256'):
            if result[k]!=b[k]: raise ValueError('MERGE_IDENTITY '+k)
        for n,h in result['artifacts'].items():
            if Path(n).name!=n or not(found[0].parent/n).is_file() or sha(found[0].parent/n)!=h: raise ValueError('ARTIFACT_HASH '+n)
        required={'initialized_context.json','initialized_context_manifest.json','native_grid_hex.json','original_rhs_points.jsonl','interval_qualification.json','source_fixture.json','execution_provenance.json','adapter_samples.jsonl','SHARED_PREFIX_nodes.csv'}
        if result['execution_status']!='COMPLETE' or not required.issubset(result['artifacts']): raise ValueError('PREREQUISITE_COMPLETENESS')
        c=read(HERE/CONTRACT)
        if result['provenance']['class_binary_sha256']!=c['class_binary_sha256'] or result['provenance']['class_commit']!=c['class_commit']: raise ValueError('COLLECT_PROVENANCE')
    except Exception as exc: errors.append(type(exc).__name__+': '+str(exc))
    final=dict(**b,execution_status='COMPLETE' if not errors else 'PARTIAL',job_completeness_gate='PASS' if not errors else 'FAIL',merge_compatibility_gate='PASS' if not errors else 'FAIL',errors=errors,worker_result=result,next_motor='Result Ingestion & Routing Engine')
    write(out,final);return int(bool(errors))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['static','run','qualify','collect']);p.add_argument('--out',default='context_v29');p.add_argument('--directory',default='collected');a=p.parse_args()
    if a.command=='static': static();return 0
    if a.command=='run': return run(a.out)
    if a.command=='qualify': qualify(Path(a.out));return 0
    return collect(a.directory,a.out)
if __name__=='__main__': sys.exit(main())
