"""Q045: four original-binary optical observations, no treatment or inference.

The exact-spline integral and Gauss check qualify a representation component
only. No reference-history remainder bound is silently inferred from agreement.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, platform, re, signal
import subprocess, sys, sysconfig, time, zipfile

HERE=Path(__file__).resolve().parent
Q='Q-045'; ID='Q045-OPTICAL-AUDIT-V1'
CONFIG='q045_optical_audit_contract_v1.json'; RESULT='q045_optical_audit_worker_v1.json'

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('DUPLICATE_JSON_KEY '+k)
        d[k]=v
    return d

def read(p):
    return json.loads(Path(p).read_text(),object_pairs_hook=unique,
        parse_constant=lambda s:(_ for _ in ()).throw(ValueError('NONFINITE_JSON '+s)))

def write(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n');tmp.replace(p)

def contract():return read(HERE/CONFIG)

def envelope():
    return dict(q=Q,program_id=ID,case_id='NOT DOCUMENTED',
        scientific_question=contract()['scientific_question'],
        run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),
        execution_commit=os.environ.get('GITHUB_SHA','LOCAL_NOT_COMMITTED'),
        config_sha256=sha(HERE/CONFIG),scientific_result=False,
        final_result_gate='UNRESOLVED',reference_truth_gate='UNQUALIFIED',
        production_restart_authorized=False,reference_treatments_executed=[],
        next_motor='Result Ingestion & Routing Engine')

def check_id(x):
    if x!=ID:raise ValueError('PROGRAM_ID_GATE')
    return x

def ini(parameters):
    rows=[]
    for k,v in parameters.items():
        if not re.fullmatch(r'[A-Za-z0-9_./-]+',k):raise ValueError('INI_KEY')
        if isinstance(v,str):s=v
        elif isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v):s=repr(v)
        else:raise ValueError('INI_VALUE '+k)
        if any(ch in s for ch in '\n\r\x00#='):raise ValueError('INI_INJECTION '+k)
        rows.append(k+' = '+s)
    return '\n'.join(rows)+'\n'

def integrals(eta,q,second):
    import numpy as np
    x,y,d=[np.asarray(a,dtype=np.float64) for a in (eta,q,second)]
    if any(a.ndim!=1 or len(a)<2 or not np.isfinite(a).all() for a in (x,y,d)) or not(len(x)==len(y)==len(d)):
        raise ValueError('HISTORY_FINITE_OR_SHAPE')
    h=np.diff(x)
    if not (h<0).all() or not(y>=0).all():raise ValueError('HISTORY_ORIENTATION_OR_OPACITY')
    trap=(y[:-1]+y[1:])*h/2
    curvature=(d[:-1]+d[1:])*h*h*h/24
    # Independently evaluate the cubic at the two Gauss nodes. It is exact
    # in real arithmetic for that cubic, not for an unknown continuum history.
    gauss=np.zeros(len(h))
    for t in (.5-.5/math.sqrt(3),.5+.5/math.sqrt(3)):
        a=1-t;b=t
        sample=a*y[:-1]+b*y[1:]+((a*a*a-a)*d[:-1]+(b*b*b-b)*d[1:])*h*h/6
        gauss+=sample*h/2
    prefix=lambda a:np.concatenate(([0.],-np.cumsum(a))).tolist()
    return dict(plus=prefix(trap+curvature),minus=prefix(trap-curvature),gauss2=prefix(gauss),
        coordinate_units='eta Mpc; q 1/Mpc; depth dimensionless',
        physical_reference_qualified=False,uncertainty='UNQUALIFIED_CONTINUUM_HISTORY')

def bracket(events):
    enter=[x for x in events if x['event']=='tau_enter'];leave=[x for x in events if x['event']=='tau_exit']
    trials=[x for x in events if x['event']=='scalar']
    if len(enter)!=1 or len(leave)!=1 or len(trials)<2:raise ValueError('CALIBRATION_EVENT_COMPLETENESS')
    if [x['call'] for x in trials]!=list(range(1,len(trials)+1)):raise ValueError('CALIBRATION_EVENT_SEQUENCE')
    values=[enter[0]['requested_tau'],enter[0]['relative_tolerance'],leave[0]['tau'],leave[0]['z_reio']]
    values+=[x[k] for x in trials for k in ('tau','z_reio')]
    if any(not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x) for x in values):
        raise ValueError('NONFINITE_CALIBRATION_BRACKET')
    if leave[0]['status']!=0 or any(x['status']!=0 for x in trials):raise ValueError('CALIBRATION_CALL_FAILURE')
    target=enter[0]['requested_tau'];tol=enter[0]['relative_tolerance']
    if target<=0 or tol<=0:raise ValueError('CALIBRATION_TARGET')
    upper,lower=trials[:2]
    if not(lower['tau']<=target<=upper['tau']) or not(lower['z_reio']<=upper['z_reio']):raise ValueError('CALIBRATION_INITIAL_BRACKET')
    for m in trials[2:]:
        if m['z_reio']!=.5*(upper['z_reio']+lower['z_reio']):raise ValueError('BISECTION_MIDPOINT')
        if m['tau']>target:upper=m
        else:lower=m
    if leave[0]['tau']!=trials[-1]['tau'] or leave[0]['z_reio']!=trials[-1]['z_reio']:raise ValueError('LAST_TRIAL_IDENTITY')
    return dict(requested_tau=target,relative_tolerance=tol,initial_bracket_tau=[trials[1]['tau'],trials[0]['tau']],
        accepted_bracket_tau=[lower['tau'],upper['tau']],accepted_bracket_z=[lower['z_reio'],upper['z_reio']],
        last_trial_residual=trials[-1]['tau']-target,bisection_trials=len(trials)-2,
        native_stopping_condition_met=(upper['tau']-lower['tau']<=target*tol),
        reconstruction='Replay of the pinned branch comparison; no smooth monotonicity assumption through selector jumps')

def table(p):
    import numpy as np
    with Path(p).open() as f:header=f.readline().removeprefix('# ').rstrip('\n').split('\t')
    a=np.loadtxt(p,skiprows=1,delimiter='\t',ndmin=2)
    if a.shape[1]!=len(header):raise ValueError('TABLE_COLUMNS '+str(p))
    return {k:a[:,i] for i,k in enumerate(header)}

def verify_worker(d,key):
    c=contract();d=Path(d);w=read(d/'q045_worker_result_v2.json')
    for k,v in dict(q=Q,program_id='Q045-BASELINE-V2',run_id=c['baseline_run_id'],job_id=key,
                    execution_commit=c['baseline_commit'],config_sha256=c['baseline_config_sha256'],status='COMPLETE').items():
        if w.get(k)!=v:raise ValueError('BASELINE_IDENTITY '+k)
    for n,h in c['baseline_workers'][key]['files'].items():
        if Path(n).name!=n or not(d/n).is_file() or sha(d/n)!=h:raise ValueError('BASELINE_HASH '+n)
    for n,h in w['artifacts'].items():
        if Path(n).name!=n or sha(d/n)!=h:raise ValueError('BASELINE_MEMBER '+n)
    if w['provenance']['class_binary_sha256']!=c['class_binary_sha256']:raise ValueError('BASELINE_BINARY')
    im=read(d/'runtime_input_manifest.json')
    if im['class_parameters']!=c['baseline_workers'][key]['class_parameters']:raise ValueError('BASELINE_VECTOR')
    return w

def safe_extract(archive,directory):
    root=Path(directory).resolve();root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        if sum(x.file_size for x in z.infolist())>contract()['caps']['input_bytes']:raise ValueError('INPUT_STORAGE_CAP')
        names=set()
        for x in z.infolist():
            p=(root/x.filename).resolve()
            if x.filename in names or Path(x.filename).is_absolute() or '\\' in x.filename or not p.is_relative_to(root) or ((x.external_attr>>16)&0o170000)==0o120000:
                raise ValueError('ARCHIVE_PATH_DUPLICATE_SYMLINK')
            names.add(x.filename)
        z.extractall(root)

def prepare(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);r=envelope();r.update(status='FAILED',error='')
    try:
        for key,item in contract()['baseline_workers'].items():
            arc=out/(key+'.zip')
            with arc.open('wb') as f:
                subprocess.run(['gh','api','repos/Morfindien/Bubbleverse/actions/artifacts/'+str(item['artifact_id'])+'/zip'],stdout=f,check=True,timeout=180)
            if arc.stat().st_size!=item['artifact_bytes'] or sha(arc)!=item['artifact_sha256']:raise ValueError('OFFICIAL_ARTIFACT_DIGEST '+key)
            safe_extract(arc,out/key);verify_worker(out/key,key);arc.unlink()
        r['status']='COMPLETE'
    except Exception as e:r['error']=type(e).__name__+': '+str(e)
    write(out/'input_preparation.json',r);return int(r['status']!='COMPLETE')

def static():
    c=contract();m=read(HERE/'q045_optical_audit_manifest_v1.json')
    if c['q']!=Q or c['program_id']!=ID or c['new_theory_evaluations_max']!=4 or c['inherited_evaluations_completed']!=4:
        raise ValueError('SCOPE_IDENTITY_GATE')
    if any(c[k] for k in ('source_patch','reference_treatments_authorized','optimization_authorized','production_restart_authorized')):raise ValueError('NO_TREATMENT_SCOPE_GATE')
    for n,h in m['files'].items():
        if sha(HERE/n)!=h:raise ValueError('PACKAGE_HASH '+n)
    reg=read(HERE/'bubbleverse_program_registry.json')['programs']
    if reg.get(ID)!=m['registry_entry'] or reg[ID]['status']!='ACTIVE':raise ValueError('REGISTRY_GATE')
    if reg['Q045-BASELINE-V2']['status']!='COMPLETED':raise ValueError('DO_NOT_REPEAT_BASELINE')
    if sha(HERE/'.github/workflows/00-bubbleverse-start.yml')!=m['launcher_sha256']:raise ValueError('LAUNCHER_GATE')
    if not(HERE/reg[ID]['workflow_path']).is_file():raise ValueError('TARGET_GATE')
    if sha(HERE/'Q045_SAMLET_JOURNAL.md')!=c['journal_sha256']:raise ValueError('JOURNAL_CONTINUITY_GATE')
    if sha(HERE/'Q045_INGESTION_RESULT.json')!=c['ingestion_sha256']:raise ValueError('INGESTION_GATE')
    for word in (ID,'UNQUALIFIED','00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if word not in (HERE/'README.md').read_text():raise ValueError('README_GATE '+word)
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')

def no_repeat():
    if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1':raise ValueError('NO_AUTOMATIC_RETRY_GATE')
    if os.environ.get('GITHUB_REPOSITORY')!='Morfindien/Bubbleverse':raise ValueError('REPOSITORY_GATE')
    current=os.environ['GITHUB_RUN_ID']
    rows=json.loads(subprocess.check_output(['gh','api','repos/Morfindien/Bubbleverse/actions/workflows/q045-optical-audit-v1.yml/runs?event=workflow_dispatch&per_page=100'],text=True,timeout=60))
    if any(str(r['id'])!=current for r in rows['workflow_runs']):raise ValueError('NO_REPEAT_CAMPAIGN_GATE: prior launch exists; return its records for a recovery decision')

def bounded(cmd,log,seconds,env=None,out=None):
    with Path(log).open('w') as f:
        p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
        try:
            deadline=time.monotonic()+seconds
            while p.poll() is None:
                if time.monotonic()>deadline:raise ValueError('PROCESS_TIME_CAP')
                if out and sum(x.stat().st_size for x in Path(out).rglob('*') if x.is_file())>contract()['caps']['output_bytes']:raise ValueError('OUTPUT_STORAGE_CAP')
                time.sleep(.1)
            if p.returncode:raise ValueError('PROCESS_EXIT '+str(p.returncode))
        finally:
            if p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait()

def analyze(out,baseline):
    import numpy as np
    out=Path(out);baseline=Path(baseline)
    e=[json.loads(x,object_pairs_hook=unique) for x in (out/'native_trace.jsonl').read_text().splitlines()]
    final=[x for x in e if x['event']=='final']
    if len(final)!=1 or final[0]['cumulative_calls']!=1 or final[0]['scalar_calls']!=len([x for x in e if x['event']=='scalar']):raise ValueError('INTERPOSITION_TRACE_GATE')
    cal=bracket(e)
    if not cal['native_stopping_condition_met']:raise ValueError('NATIVE_CALIBRATION_STOP_GATE')
    meta=read(out/'native_meta.json');nodes=table(out/'final_native_nodes.tsv');old=table(baseline/'thermodynamics.tsv')
    if any(not np.isfinite(v).all() for v in nodes.values()):raise ValueError('FINAL_HISTORY_NONFINITE')
    with (out/'source_species.tsv').open() as f:source_rows=sum(1 for _ in f)-1
    if source_rows!=final[0]['source_rows'] or source_rows<1:raise ValueError('SOURCE_OUTPUT_COMPLETENESS')
    expected=read(baseline/'runtime_input_manifest.json')['class_parameters']['tau_reio']
    # The pinned tau-input route leaves pth->tau_reio equal to the request;
    # the actually evaluated last trial is separately preserved in the bracket.
    if cal['requested_tau']!=expected or meta['tau_reported']!=expected:raise ValueError('CALIBRATION_INPUT_OUTPUT_IDENTITY')
    cols={'z':'z','eta_Mpc':'conf. time [Mpc]','xe':'x_e','q_1_Mpc':"kappa' [Mpc^-1]",'exp_minus_kappa':'exp(-kappa)','g_1_Mpc':'g [Mpc^-1]'}
    comparisons={a:bool(np.array_equal(nodes[a],old[b])) for a,b in cols.items()}
    if not all(comparisons.values()):raise ValueError('OBSERVATIONAL_TABLE_IDENTITY '+str(comparisons))
    if any(meta[k] for k in ('has_exotic_injection','has_varconst','has_idm_g')):raise ValueError('REFERENCE_DOMAIN_GATE')
    raw=table(out/'cumulative_native.tsv');calc=integrals(raw['eta_Mpc'],raw['q_1_Mpc'],raw['q_second_eta'])
    if not np.array_equal(raw['eta_Mpc'],nodes['eta_Mpc']) or not np.array_equal(raw['q_1_Mpc'],nodes['q_1_Mpc']):raise ValueError('CUMULATIVE_HISTORY_IDENTITY')
    normal=meta['nH0_m3']*meta['sigma_m2']*meta['metres_per_Mpc']
    physical=normal*nodes['xe']*(1+nodes['z'])**2
    scale=np.maximum(np.abs(nodes['q_1_Mpc']),np.finfo(float).tiny)
    normalization=float(np.max(np.abs(physical-nodes['q_1_Mpc'])/scale))
    plus=np.asarray(calc['plus']);minus=np.asarray(calc['minus']);gauss=np.asarray(calc['gauss2'])
    delta=plus-minus
    np.savetxt(out/'cumulative_component_comparison.tsv',np.column_stack((nodes['z'],raw['native_kappa'],plus,minus,gauss,delta)),delimiter='\t',fmt='%.17g',header='z\tnative_original_kappa\tdecoded_plus\texact_cubic_minus\tgauss2_cubic\tplus_minus')
    summaries=[]
    for event in [x for x in e if x['event']=='scalar']:
        n=event['support_rows'];i=event['call']
        if n==0:
            if event['tau']!=0:raise ValueError('ZERO_SUPPORT_TAU')
            summaries.append(dict(event,component_integrals=None));continue
        t=table(out/f'scalar_{i:03d}.tsv')
        if len(t['z'])!=n or t['z'][-1]!=event['endpoint_z']:raise ValueError('SCALAR_SUPPORT_GATE')
        f=integrals(t['eta_Mpc'],t['q_1_Mpc'],t['q_second_eta'])
        summaries.append(dict(event,component_integrals={k:f[k][-1] for k in ('plus','minus','gauss2')},
            native_replay_difference=f['plus'][-1]-event['tau'],spline_bias=f['plus'][-1]-f['minus'][-1]))
    write(out/'scalar_component_comparison.json',dict(q=Q,program_id=ID,trials=summaries,history_accuracy='UNQUALIFIED'))
    # Preserve a redshift-space node trapezoid as a coordinate/history diagnostic.
    # It is NOT called a converged Thomson reference or an error bound.
    hz=nodes['H_1_Mpc'];z=nodes['z']
    if not np.isfinite(hz).all() or not(hz>0).all():raise ValueError('BACKGROUND_UNITS_OR_FINITE')
    z_depth=np.concatenate(([0.],np.cumsum(np.diff(z)*(physical[:-1]/hz[:-1]+physical[1:]/hz[1:])/2)))
    np.savetxt(out/'redshift_node_diagnostic.tsv',np.column_stack((z,z_depth,minus)),delimiter='\t',fmt='%.17g',header='z\tz_node_trapezoid\teta_exact_cubic')
    return dict(observational_table_identity=comparisons,calibration=cal,
        opacity_normalization_max_relative_residual=normalization,
        original_binary_cumulative_vs_decoded_plus_max_abs=float(np.max(np.abs(raw['native_kappa']-plus))),
        cubic_minus_vs_gauss2_max_abs=float(np.max(np.abs(minus-gauss))),
        plus_minus_max_abs=float(np.max(np.abs(delta))),
        native_underflow_rows=int((nodes['exp_minus_kappa']==0).sum()),
        reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
        reason='Same-history cubic controls acquired. Continuum/history/event and calibration remainder qualification, matched refinement levels and consumed-observable response are absent.',
        requested_tau=expected,actual_computed_scientific_result='NOT_YET_COMPUTED')

def worker(key,inputs,out,class_root):
    c=contract();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);started=time.monotonic()
    r=envelope();r.update(job_id=key,status='FAILED',error='',theory_evaluations_started=0)
    try:
        if key not in c['expected_jobs']:raise ValueError('JOB_ID_GATE')
        if platform.python_version()!=c['python_version'] or platform.system()!='Linux' or platform.machine()!='x86_64':raise ValueError('RUNTIME_GATE')
        if any(os.environ.get(n)!='1' for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')):raise ValueError('THREAD_GATE')
        baseline=Path(inputs).resolve()/key;verify_worker(baseline,key)
        root=Path(class_root).resolve()
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=c['class_commit']:raise ValueError('SOURCE_COMMIT')
        subprocess.run(['git','-C',str(root),'diff','--quiet','HEAD'],check=True)
        for n,h in c['frozen_class_sources'].items():
            if sha(root/n)!=h:raise ValueError('SOURCE_HASH '+n)
        binary=root/c['binary_relative_path']
        if sha(binary)!=c['class_binary_sha256']:raise ValueError('ORIGINAL_BINARY_GATE')
        ldlib=sysconfig.get_config_var('LDLIBRARY');libdir=sysconfig.get_config_var('LIBDIR')
        if not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib or not libdir:raise ValueError('PYTHON_LINK_GATE')
        params=c['baseline_workers'][key]['class_parameters'];(out/'point.ini').write_text(ini(params))
        write(out/'input_identity.json',dict(q=Q,program_id=ID,job_id=key,class_parameters=params,
            baseline_run_id=c['baseline_run_id'],baseline_worker_sha256=sha(baseline/'q045_worker_result_v2.json'),
            original_sampled_vector=read(baseline/'sampled_vector.json'),original_runtime_manifest_sha256=sha(baseline/'runtime_input_manifest.json')))
        exe=out/'q045_original_binary_observer';cmd=['gcc','-O2','-fopenmp','-rdynamic','-Wall','-Wextra']
        for sub in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):cmd+=['-I',str(root/sub)]
        cmd +=[str(HERE/'q045_optical_audit_probe_v1.c'),str(binary),'-L'+libdir,'-l'+ldlib.removeprefix('lib').split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        bounded(cmd,out/'compile.log',120)
        r['provenance']=dict(original_binary_sha256=sha(binary),observer_executable_sha256=sha(exe),
            source_commit=c['class_commit'],compile_command=cmd,compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
            original_binary_compiler='NOT DOCUMENTED',python=platform.python_version(),platform=platform.platform(),
            observer_scope='Background + thermodynamics only; no new spectrum or likelihood evaluation')
        r['theory_evaluations_started']=1;write(out/'attempt.json',r)
        bounded([str(exe),str(out/'point.ini')],out/'native.log',c['caps']['native_seconds'],dict(os.environ,Q045_TRACE_DIR=str(out)),out)
        if sha(binary)!=c['class_binary_sha256']:raise ValueError('BINARY_MUTATION_GATE')
        r['analysis']=analyze(out,baseline);r['status']='COMPLETE';r['observation_gate']='PASS_NATIVE_COMPONENT_ONLY'
    except Exception as e:r['error']=type(e).__name__+': '+str(e);r['failure_class']='OBSERVATION_OR_VALIDATION';r['observation_gate']='FAIL'
    r['wall_seconds']=time.monotonic()-started
    r['files']={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!=RESULT}
    write(out/RESULT,r);return int(r['status']!='COMPLETE')

def collect(directory,out):
    c=contract();r=envelope();records=[];errors=[];seen=set()
    files=sorted(Path(directory).rglob(RESULT))
    for p in files:
        try:
            x=read(p);records.append(x);key=x['job_id']
            if key in seen or key not in c['expected_jobs']:raise ValueError('DUPLICATE_OR_UNKNOWN_JOB')
            seen.add(key)
            for k in ('q','program_id','config_sha256','run_id','execution_commit'):
                if x[k]!=r[k]:raise ValueError('MERGE_IDENTITY '+k)
            for n,h in x['files'].items():
                if Path(n).name!=n or sha(p.parent/n)!=h:raise ValueError('RAW_PRODUCT_HASH '+n)
            if x['status']!='COMPLETE' or x['observation_gate']!='PASS_NATIVE_COMPONENT_ONLY':raise ValueError('WORKER_INCOMPLETE '+key)
            a=analyze(p.parent,Path(directory)/'baselines'/key)
            if a!=x['analysis']:raise ValueError('RESULT_RECONSTRUCTION '+key)
        except Exception as e:errors.append(str(e))
    if seen!=set(c['expected_jobs']) or len(files)!=len(c['expected_jobs']):errors.append('JOB_COMPLETENESS')
    started=sum(x.get('theory_evaluations_started',0) for x in records)
    if started>4:errors.append('EVALUATION_BUDGET')
    r.update(execution_status='COMPLETE' if not errors else 'PARTIAL',result_status='RAW_COMPONENT_ONLY',
        job_completeness_gate='PASS' if not errors else 'FAIL',merge_compatibility_gate='PASS' if not errors else 'FAIL',
        observation_gate='PASS_NATIVE_COMPONENT_ONLY' if not errors else 'FAIL',tests_status='COMPLETE' if not errors else 'INCOMPLETE',
        records=records,errors=errors,expected_jobs=c['expected_jobs'],completed_jobs=[x['job_id'] for x in records if x['status']=='COMPLETE'],
        failed_jobs=[x['job_id'] for x in records if x['status']!='COMPLETE'],pending_jobs=sorted(set(c['expected_jobs'])-seen),
        evaluations_inherited=4,evaluations_started_this_target=started,evaluations_total_upper_bound_this_target=8,
        inherited_total_budget=52,automatic_continuation=False,
        actual_computed_scientific_result='NOT_YET_COMPUTED',
        terminal_stage_reason='Reference history/remainder gate is UNQUALIFIED; no treatments or extra refinements auto-dispatched.')
    write(out,r);return int(bool(errors))

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    s.add_parser('static');s.add_parser('no-repeat')
    a=s.add_parser('prepare');a.add_argument('--out',required=True)
    a=s.add_parser('worker');a.add_argument('--job',required=True);a.add_argument('--inputs',required=True);a.add_argument('--out',required=True);a.add_argument('--class-root',required=True)
    a=s.add_parser('collect');a.add_argument('--directory',required=True);a.add_argument('--out',required=True)
    a=p.parse_args()
    if a.command=='static':static();return 0
    if a.command=='no-repeat':no_repeat();return 0
    if a.command=='prepare':return prepare(a.out)
    if a.command=='worker':return worker(a.job,a.inputs,a.out,a.class_root)
    return collect(a.directory,a.out)

if __name__=='__main__':sys.exit(main())
