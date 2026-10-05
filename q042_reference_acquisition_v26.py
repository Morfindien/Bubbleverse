"""Q-042 bounded raw acquisition. Standard library; never a production solver."""
from pathlib import Path
import argparse, csv, hashlib, json, math, os, platform, re, shutil, subprocess, sys, sysconfig, time

HERE = Path(__file__).resolve().parent
Q = 'Q-042'
PROGRAM_ID = 'Q042-REFACQ-V26'
CONTRACT = 'q042_reference_contract_v26.json'
EXPECTED = [f'{t}-{m}-L{n}' for t in ('UPPER','LOWER') for m in ('RK4','MIDPOINT') for n in (1,2,4)]

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def read(p):
    return json.loads(Path(p).read_text())

def write(p, data):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def possible_supports(bounds):
    """Conditional enclosure rule only; inputs must already be credible intervals."""
    groups={}
    for k,(lo,hi) in enumerate(bounds[:-1]):
        if not(math.isfinite(lo) and math.isfinite(hi) and lo<=hi): raise ValueError('INVALID_NODE_INTERVAL')
        N=0 if k==0 else max(3,k)
        if N in groups: groups[N]=(min(groups[N][0],lo),min(groups[N][1],hi))
        else: groups[N]=(lo,hi)
    if not groups: raise ValueError('NO_SUPPORT_CLASSES')
    upper=min(x[1] for x in groups.values())
    return sorted(N for N,(lo,_) in groups.items() if lo<=upper)

def completeness(records,expected,run,config):
    ids=[r.get('branch_id') for r in records]
    mismatch=[r.get('branch_id') for r in records if any(r.get(k)!=v for k,v in dict(q=Q,program_id=PROGRAM_ID,run_id=run,config_sha256=config,result_status='RAW_NOT_QUALIFIED').items())]
    duplicates=sorted({x for x in ids if ids.count(x)>1},key=str)
    unexpected=sorted(set(ids)-set(expected),key=str)
    missing=sorted(set(expected)-set(ids))
    statuses=('COMPLETE','FAILED','NOT_ATTEMPTED_RESOURCE_CAP','NOT_ATTEMPTED_PREFLIGHT_FAILURE')
    compatible=not(mismatch or duplicates or unexpected or any(r.get('execution_status') not in statuses for r in records))
    accounted=compatible and not missing
    failed=[r.get('branch_id') for r in records if r.get('execution_status')!='COMPLETE']
    return dict(merge_compatibility_gate='PASS' if compatible else 'FAIL',reporting_completeness_gate='PASS' if accounted else 'FAIL',job_completeness_gate='PASS' if accounted and not failed else 'FAIL',missing_branches=missing,duplicate_branches=duplicates,unexpected_branches=unexpected,identity_mismatch=mismatch,failed_branches=failed)

def identity(c,run,**extra):
    return dict(q=Q,case_id=c['case_id'],scientific_question=c['scientific_question'],program_id=PROGRAM_ID,run_id=run,config_sha256=sha(HERE/CONTRACT),original_scientific_spec_sha256=c['original_scientific_spec_sha256'],result_status='RAW_NOT_QUALIFIED',scientific_result=False,history_accuracy_qualified=False,prediction_likelihood_qualified=False,reference_truth_gate='BLOCKED',final_result_gate='UNRESOLVED',production_restart_authorized=False,**extra)

def static(root=HERE):
    root=Path(root); c=read(root/CONTRACT); manifest=read(root/'q042_reference_package_manifest_v26.json')
    if c['q']!=Q or c['program_id']!=PROGRAM_ID or c['expected_branches']!=EXPECTED: raise ValueError('CONTEXT_GATE=FAIL')
    if any(c[x] for x in ('production_restart_authorized','root_search_authorized','reference_truth_qualified')): raise ValueError('SCOPE_GATE=FAIL')
    for path,digest in manifest['immutable_files'].items():
        if not(root/path).is_file() or sha(root/path)!=digest: raise ValueError('PACKAGE_HASH_GATE=FAIL '+path)
    reg=read(root/'bubbleverse_program_registry.json')['programs']; entry=reg.get(PROGRAM_ID)
    if entry!=manifest['registry_entry']: raise ValueError('REGISTRY_GATE=FAIL')
    if not(root/entry['workflow_path']).is_file(): raise ValueError('TARGET_GATE=FAIL')
    launcher=root/'.github/workflows/00-bubbleverse-start.yml'
    if sha(launcher)!=manifest['canonical_launcher_sha256']: raise ValueError('LAUNCHER_IDENTITY_GATE=FAIL')
    # Mutable front door is validated semantically, never coupled to a historical byte hash.
    doc=(root/'README.md').read_text()
    for text in (PROGRAM_ID,'00-bubbleverse-start.yml','bubbleverse_program_registry.json','RAW_NOT_QUALIFIED'):
        if text not in doc: raise ValueError('README_GATE=FAIL '+text)
    if sha(root/c['point_file'])!=c['point_sha256']: raise ValueError('POINT_GATE=FAIL')
    print('PACKAGE_GATE=PASS REGISTRY_GATE=PASS README_GATE=PASS LAUNCHER_IDENTITY_GATE=PASS')
    return c

def source_preflight(root,c):
    commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if commit!=c['class_commit']: raise ValueError('CLASS_COMMIT_GATE=FAIL '+commit)
    subprocess.run(['git','-C',str(root),'diff','--exit-code','HEAD','--','include','source','tools','external','Makefile'],check=True,stdout=subprocess.DEVNULL)
    for relative,digest in c['frozen_source_hashes'].items():
        if sha(root/relative)!=digest: raise ValueError('CLASS_SOURCE_HASH_GATE=FAIL '+relative)
    binaries=[p for p in root.rglob('classy*.so') if sha(p)==c['class_binary_sha256']]
    if len(binaries)!=1: raise ValueError('CLASS_BINARY_GATE=FAIL matches='+str(len(binaries)))
    return binaries[0]

def load_nodes(path,base,branch):
    rows=[]
    with Path(path).open(newline='') as f:
        for r in csv.DictReader(f):
            for k in ('q','program_id','run_id','config_sha256'):
                if r[k]!=base[k]: raise ValueError('NODE_IDENTITY_GATE=FAIL '+k)
            if r['branch_id']!=branch: raise ValueError('NODE_BRANCH_GATE=FAIL')
            rows.append(r)
    if not rows: raise ValueError('EMPTY_NODE_TABLE')
    return rows

def fnumber(x):
    return float(x) if x!='NOT_COMPUTED' else float('nan')

def branch_validate(record,rows):
    if record['execution_status']!='COMPLETE': return
    if any(r['scope']=='NOT_ACQUIRED' for r in rows): raise ValueError('MISSING_NATIVE_OUTPUT')
    if any(not math.isfinite(fnumber(r[k])) for r in rows for k in ('z','eta_Mpc','xe_source','dkappa_per_Mpc')): raise ValueError('NONFINITE_COMPLETE_NODE_TABLE')
    if any(not math.isfinite(fnumber(r[k])) for r in rows if r['scope']=='ACQUIRED_REIONIZATION' for k in ('D_Tmat_K','x_H','x_He','x_noreio','x_reio_rhs')): raise ValueError('NONFINITE_ACQUIRED_STATE')
    z=[fnumber(r['z']) for r in rows]; eta=[fnumber(r['eta_Mpc']) for r in rows]
    if any(b<=a for a,b in zip(z,z[1:])) or any(b>=a for a,b in zip(eta,eta[1:])): raise ValueError('NATIVE_GRID_ORDER_GATE=FAIL')
    k=min(range(len(rows)-1),key=lambda i:fnumber(rows[i]['xe_source'])); N=0 if k==0 else max(3,k)
    if record['minimum_row']!=k or record['effective_n']!=N: raise ValueError('EFFECTIVE_SUPPORT_GATE=FAIL')
    if N and any(not math.isfinite(fnumber(rows[i]['dddkappa_eta'])) for i in range(N)): raise ValueError('ETA_COEFFICIENT_GATE=FAIL')
    if not math.isfinite(fnumber(record['tau_correct_same_spline'])): raise ValueError('NONFINITE_TAU')
    if record['rhs_calls']>1200000 or record['max_newton_used']>12: raise ValueError('BRANCH_RESOURCE_GATE=FAIL')

def difference(left,right,column):
    if len(left)!=len(right) or any(a['z']!=b['z'] or a['eta_Mpc']!=b['eta_Mpc'] for a,b in zip(left,right)): raise ValueError('GRID_COMPATIBILITY_GATE=FAIL')
    pairs=[(fnumber(a[column]),fnumber(b[column])) for a,b in zip(left,right) if a['scope']=='ACQUIRED_REIONIZATION' and b['scope']=='ACQUIRED_REIONIZATION']
    if not pairs or any(not math.isfinite(a) or not math.isfinite(b) for a,b in pairs): raise ValueError('NO_FINITE_DIFFERENCE_SERIES')
    d=[abs(a-b) for a,b in pairs]
    return dict(nodes=len(d),maximum=max(d),rms=math.sqrt(math.fsum(x*x for x in d)/len(d)))

def diagnostics(tables):
    result=dict(level_differences={},cross_method_differences={},credible_node_intervals='NOT AVAILABLE',support_stability='UNRESOLVED',richardson_status='CONDITIONAL_ONLY_NOT_AN_ENCLOSURE',dense_defect_status='POINT_SAMPLED_NOT_A_GLOBAL_BOUND')
    for trial in ('UPPER','LOWER'):
        for method,order in (('RK4',4),('MIDPOINT',2)):
            ids=[f'{trial}-{method}-L{n}' for n in (1,2,4)]
            if not all(x in tables for x in ids): continue
            values={}
            for col in ('D_Tmat_K','x_H','xe_source','dkappa_per_Mpc'):
                a=difference(tables[ids[0]],tables[ids[1]],col); b=difference(tables[ids[1]],tables[ids[2]],col)
                p=math.log2(a['rms']/b['rms']) if a['rms']>0 and b['rms']>0 else None
                values[col]=dict(coarse_medium=a,medium_fine=b,observed_rms_order=p,formal_order=order,richardson_estimate='UNRESOLVED',conditional_formula='fine-medium norm / '+str(2**order-1),assumptions_not_established=['asymptotic regime','shared prefix/IC accuracy','global stability/error propagation'])
            result['level_differences'][f'{trial}-{method}']=values
        for level in (1,2,4):
            a=f'{trial}-RK4-L{level}'; b=f'{trial}-MIDPOINT-L{level}'
            if a in tables and b in tables: result['cross_method_differences'][f'{trial}-L{level}']={col:difference(tables[a],tables[b],col) for col in ('D_Tmat_K','x_H','xe_source','dkappa_per_Mpc')}
    return result

def acquire(out):
    out=Path(out).resolve(); out.mkdir(parents=True,exist_ok=True)
    c=read(HERE/CONTRACT); run=os.environ.get('GITHUB_RUN_ID','LOCAL')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',run): raise ValueError('UNSAFE_RUN_ID')
    base=identity(c,run); started=time.monotonic(); error=''; rc=None; provenance={}; records=[]; tables={}
    write(out/'expected_branch_manifest.json',dict(**base,expected_branches=EXPECTED,execution_status='PLANNED'))
    try:
        if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1': raise ValueError('NO_AUTOMATIC_RETRY_GATE=FAIL')
        if any(out.glob('*_result.json')): raise ValueError('OUTPUT_REUSE_GATE=FAIL')
        static(HERE)
        root=HERE/'external/class_ede'; binary=source_preflight(root,c)
        # The finite source adapter fixture must pass before common-prefix execution.
        with (out/'adapter_selftest.log').open('w') as log:
            log.write(json.dumps(base)+'\n');log.flush()
            subprocess.run([sys.executable,str(HERE/'q042_reference_adapter_selftest_v26.py'),str(root)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        libdir=sysconfig.get_config_var('LIBDIR'); ldlib=sysconfig.get_config_var('LDLIBRARY')
        if not libdir or not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib: raise ValueError('PYTHON_LINK_GATE=FAIL')
        exe=out/'q042_reference_native_v26'
        cmd=['gcc','-O2','-std=c99','-fopenmp','-rdynamic','-fno-fast-math','-ffp-contract=off','-I'+str(HERE)]
        for p in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'): cmd+=['-I'+str(root/p)]
        cmd += [str(HERE/'q042_reference_native_v26.c'),str(binary),'-L'+libdir,'-l'+ldlib[3:].split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        with (out/'compile.log').open('w') as log:
            log.write(json.dumps(base)+'\n');log.flush()
            subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
        point=out/'point.ini'; shutil.copyfile(HERE/c['point_file'],point)
        env=os.environ.copy(); env.update(Q042_REFACQ_DIR=str(out),Q042_REFACQ_RUN=run,Q042_REFACQ_CONFIG_SHA256=base['config_sha256'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
        provenance=dict(class_commit=c['class_commit'],class_binary_sha256=sha(binary),source_tree_gate='PASS',binary_route=str(binary),executable_sha256=sha(exe),compile_command=cmd,command=[str(exe),str(point)],point_sha256=sha(point),execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),python_version=platform.python_version(),platform=platform.platform(),compiler_version=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],thread_policy={k:env[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},package_hashes=read(HERE/'q042_reference_package_manifest_v26.json')['immutable_files'])
        write(out/'execution_provenance.json',dict(**base,**provenance))
        # Poll only the owned subprocess; cap total wall time and output storage.
        with (out/'native_campaign.log').open('w') as log:
            log.write(json.dumps(base)+'\n');log.flush()
            p=subprocess.Popen([str(exe),str(point)],cwd=HERE,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            deadline=time.monotonic()+1600
            while p.poll() is None:
                size=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
                if time.monotonic()>deadline or size>256*1024*1024:
                    import signal
                    os.killpg(p.pid,signal.SIGKILL); p.wait(); raise ValueError('CAMPAIGN_WALL_OR_STORAGE_CAP')
                time.sleep(.2)
            rc=p.returncode
        if rc!=0: raise ValueError('NATIVE_CAMPAIGN_GATE=FAIL exit='+str(rc))
        entry=read(out/'accepted_entry.json')
        if entry['source_rhs_comparison']!='PASS' or entry['tau_search_executed'] is not False: raise ValueError('ACCEPTED_ENTRY_GATE=FAIL')
        for k in ('q','program_id','run_id','config_sha256'):
            if entry[k]!=base[k]: raise ValueError('ENTRY_IDENTITY_GATE=FAIL '+k)
        archived=c['archived_entry']; equality={k:entry.get(k)==v for k,v in archived.items()}
        write(out/'accepted_entry_comparison.json',dict(**base,archived_equality=equality,differences={k:dict(archived=archived[k],actual=entry.get(k)) for k,v in equality.items() if not v},conditioning_scope='SHARED_PREFIX_AND_ACCEPTED_INITIAL_STATE_NOT_INDEPENDENT_REFERENCE'))
    except Exception as e:
        error=type(e).__name__+': '+str(e)
    try: native=read(out/'native_branch_manifest.json') if (out/'native_branch_manifest.json').is_file() else None
    except Exception as e: native=None; error+='; NATIVE_MANIFEST_UNREADABLE: '+str(e)
    for b in EXPECTED:
        file=out/f'{b}_result.json'
        if not file.is_file():
            r=dict(**base,branch_id=b,execution_status='NOT_ATTEMPTED_PREFLIGHT_FAILURE' if native is None and not (out/'accepted_entry.json').exists() else 'FAILED',error=error or 'MISSING_NATIVE_TERMINAL_RECORD_ATTEMPT_STATUS_UNRESOLVED')
            write(file,r)
        else:
            try: r=read(file)
            except Exception as e: r=dict(**base,branch_id=b,execution_status='FAILED',error='RAW_BRANCH_JSON_UNREADABLE: '+str(e))
        if r.get('execution_status')=='COMPLETE':
            try:
                rows=load_nodes(out/f'{b}_nodes.csv',base,b); branch_validate(r,rows)
                parent=[x for x in native['branches'] if x['branch_id']==b] if native else []
                if len(parent)!=1 or parent[0]['execution_status']!='COMPLETE' or parent[0]['child_exit_code']!=0: raise ValueError('PARENT_CHILD_GATE=FAIL')
                tables[b]=rows
            except Exception as e:
                # Preserve raw child bytes. Annotation never overwrites the measurement.
                r=dict(r,execution_status='FAILED',validation_error=type(e).__name__+': '+str(e))
        records.append(r)
    gates=completeness(records,EXPECTED,run,base['config_sha256'])
    try: measured=diagnostics(tables)
    except Exception as e: measured=dict(error=type(e).__name__+': '+str(e)); gates['merge_compatibility_gate']='FAIL'
    files={f.name:sha(f) for f in out.iterdir() if f.is_file()}
    status='COMPLETE' if gates['job_completeness_gate']=='PASS' and gates['merge_compatibility_gate']=='PASS' and not error else 'PARTIAL'
    result=dict(**base,execution_status=status,acquisition_gate='PASS' if status=='COMPLETE' else 'FAIL',common_execution_error=error,native_exit_code=rc,elapsed_seconds=time.monotonic()-started,branches=records,expected_branches=EXPECTED,tests=gates,diagnostics=measured,provenance=provenance,artifacts=files,actual_computed_result='RAW_DIAGNOSTICS_ONLY' if tables else 'NOT YET COMPUTED',next_motor='Result Ingestion & Routing Engine',journal_effect='ADD technical acquisition evidence; KEEP scientific contract and prior failures',unresolved_issues=['history-to-prediction/likelihood accuracy budget absent','shared prefix/background/initial-state accuracy not independently established','reference-truth qualification blocked'])
    write(out/'q042_reference_worker_result_v26.json',result)
    return 0 if status=='COMPLETE' else 1

def collect(directory,out):
    c=read(HERE/CONTRACT); run=os.environ.get('GITHUB_RUN_ID','LOCAL'); base=identity(c,run)
    found=list(Path(directory).rglob('q042_reference_worker_result_v26.json')) if Path(directory).exists() else []
    if len(found)!=1:
        result=dict(**base,execution_status='PARTIAL',acquisition_gate='FAIL',error='WORKER_ARTIFACT_COMPLETENESS_GATE=FAIL count='+str(len(found)),actual_computed_result='NOT AVAILABLE',expected_branches=EXPECTED)
    else:
        try: result=read(found[0])
        except Exception as e:
            result=dict(**base,execution_status='PARTIAL',acquisition_gate='FAIL',error='UNREADABLE_WORKER_JSON: '+str(e),branches=[])
        problems=[]
        for k in ('q','program_id','run_id','config_sha256'):
            if result.get(k)!=base[k]: problems.append('WORKER_IDENTITY '+k)
        for name,digest in result.get('artifacts',{}).items():
            p=found[0].parent/name
            if Path(name).name!=name or not p.is_file() or sha(p)!=digest: problems.append('ARTIFACT_HASH '+name)
        required={'accepted_entry.json','accepted_grid.csv','adapter_samples.jsonl','SHARED_PREFIX_nodes.csv','execution_provenance.json','native_branch_manifest.json','point.ini'}
        for b in EXPECTED:
            required.update({b+'_result.json',b+'_nodes.csv',b+'_accepted_nodes.csv',b+'_defects.csv',b+'_native.log'})
        if result.get('acquisition_gate')=='PASS' and not required.issubset(result.get('artifacts',{})):
            problems.append('REQUIRED_RAW_ARTIFACTS_MISSING')
        if result.get('acquisition_gate')=='PASS' and (result.get('provenance',{}).get('class_binary_sha256')!=c['class_binary_sha256'] or result.get('provenance',{}).get('source_tree_gate')!='PASS'):
            problems.append('FROZEN_EXECUTION_PROVENANCE_GATE=FAIL')
        g=completeness(result.get('branches',[]),EXPECTED,run,base['config_sha256'])
        result['collection_tests']=g
        if problems or g['job_completeness_gate']!='PASS' or g['merge_compatibility_gate']!='PASS':
            result.update(execution_status='PARTIAL',acquisition_gate='FAIL',collection_errors=problems)
    result.update(final_result_gate='UNRESOLVED',reference_truth_gate='BLOCKED',result_status='RAW_NOT_QUALIFIED',scientific_result=False,production_restart_authorized=False)
    write(out,result)
    return 0 if result.get('acquisition_gate')=='PASS' else 1

def main():
    p=argparse.ArgumentParser(description=__doc__); sp=p.add_subparsers(dest='command',required=True)
    a=sp.add_parser('static'); a.add_argument('--root',type=Path,default=HERE)
    a=sp.add_parser('run'); a.add_argument('--out',default='reference_acquisition')
    a=sp.add_parser('collect'); a.add_argument('--directory',default='collected'); a.add_argument('--out',default='q042_reference_final_v26.json')
    a=p.parse_args()
    if a.command=='static': static(a.root); return 0
    if a.command=='run': return acquire(a.out)
    return collect(a.directory,a.out)

if __name__=='__main__': sys.exit(main())
