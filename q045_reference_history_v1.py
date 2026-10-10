"""Q045: eight original-binary background/thermodynamics refinements; no CMB treatment or inference.

The exact-spline integral and Gauss check qualify a representation component
only. No reference-history remainder bound is silently inferred from agreement.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, platform, re, signal
import subprocess, sys, sysconfig, time, zipfile

HERE=Path(__file__).resolve().parent
Q='Q-045'; ID='Q045-REFHIST-V1'
CONFIG='q045_reference_history_contract_v1.json'; RESULT='q045_reference_history_worker_v1.json'

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
        full_matrix_budget_gate='FAIL_FOR_UNMODIFIED_48_FULL_PLAN_AFTER_THIS_STAGE',
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

BASE_SETTINGS=dict(tol_thermo_integration=1e-6,thermo_integration_stepsize=.1,
 thermo_Nz_lin=20000,thermo_Nz_log=5000,reionization_sampling=.015,
 reionization_optical_depth_tol=1e-4,tol_background_integration=1e-10,
 background_integration_stepsize=.5,background_Nloga=40000)
GRID_CONTROLS={'thermo_Nz_lin','thermo_Nz_log','background_Nloga'}

def settings(level):
    if isinstance(level,bool) or level not in (0,1,2):raise ValueError('LEVEL_GATE')
    return {k:(v*2**level if k in GRID_CONTROLS else v/2**level) for k,v in BASE_SETTINGS.items()}

def parameters(physical,level):
    if set(physical)&set(BASE_SETTINGS):raise ValueError('PHYSICAL_PRECISION_COLLISION')
    return dict(physical,**settings(level))

def precision(path):
    rows=Path(path).read_text().splitlines();d={}
    for row in rows:
        k,v=row.split('\t')
        if k in d:raise ValueError('DUPLICATE_PRECISION')
        try:d[k]=float(v)
        except ValueError:d[k]=v
    if any(isinstance(v,float) and not math.isfinite(v) for v in d.values()):raise ValueError('NONFINITE_PRECISION')
    return d

def convergence(values):
    if len(values)!=3 or any(not math.isfinite(x) for x in values):raise ValueError('CONVERGENCE_INPUT')
    d0=values[0]-values[1];d1=values[1]-values[2];p=None;estimate=None
    if d0 and d1 and d0/d1>0:
        p=math.log2(abs(d0/d1))
        if 0<p<50:estimate=abs(d1)/math.expm1(p*math.log(2))
    return dict(values=values,level_differences=[d0,d1],observed_order=p,
        empirical_remaining_estimate=estimate,estimate_status='EMPIRICAL_NOT_A_BOUND',
        reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
        caveat='Simultaneous solver/grid/calibration refinements; no asymptotic regime or continuum error certificate established.')

def completeness(expected,actual):
    duplicates=sorted({x for x in actual if actual.count(x)>1})
    missing=sorted(set(expected)-set(actual));unknown=sorted(set(actual)-set(expected))
    return dict(gate='PASS' if not(missing or unknown or duplicates) and len(actual)==len(expected) else 'FAIL',
                missing=missing,unknown=unknown,duplicates=duplicates)

def redshift_depth(z,xe,second_xe,H,normal,order):
    """Gauss integration of cubic xe / linear native H. Representation diagnostic only."""
    import numpy as np
    z,xe,second_xe,H=[np.asarray(a,dtype=float) for a in (z,xe,second_xe,H)]
    if any(a.ndim!=1 or len(a)!=len(z) or not np.isfinite(a).all() for a in (z,xe,second_xe,H)):
        raise ValueError('REDSHIFT_SHAPE_FINITE')
    if len(z)<2 or z[0]!=0 or not(np.diff(z)>0).all() or not(H>0).all():raise ValueError('REDSHIFT_DOMAIN')
    if not math.isfinite(normal) or normal<=0 or order not in (16,32):raise ValueError('REDSHIFT_QUADRATURE')
    t,w=np.polynomial.legendre.leggauss(order);t=(t+1)/2;w=w/2;a=1-t
    pieces=[]
    for start in range(0,len(z)-1,2048):
        end=min(len(z)-1,start+2048);h=np.diff(z)[start:end,None]
        value=a*xe[start:end,None]+t*xe[start+1:end+1,None]
        value+=((a**3-a)*second_xe[start:end,None]+(t**3-t)*second_xe[start+1:end+1,None])*h*h/6
        zz=z[start:end,None]+t*h;hh=a*H[start:end,None]+t*H[start+1:end+1,None]
        # No clipping of interpolated electrons: unexpected signs are retained.
        pieces.append(normal*(h[:,0]*((value*(1+zz)**2/hh)*w).sum(axis=1)))
    depth=np.r_[0.,np.cumsum(np.concatenate(pieces))]
    if not np.isfinite(depth).all():raise ValueError('REDSHIFT_DEPTH_NONFINITE')
    return depth

def parent(inputs,key):
    d=Path(inputs)/key/'q045_output';c=contract();item=c['parents'][key]
    if {p.name for p in d.iterdir() if p.is_file()}!=set(item['files']):raise ValueError('PARENT_INVENTORY '+key)
    for n,h in item['files'].items():
        if Path(n).name!=n or sha(d/n)!=h:raise ValueError('PARENT_HASH '+key+' '+n)
    w=read(d/'q045_optical_audit_worker_v3.json')
    for k,v in dict(q=Q,program_id='Q045-OPTICAL-AUDIT-V3',job_id=key,status='COMPLETE',
       observation_gate='PASS_NATIVE_COMPONENT_ONLY',run_id=c['parent_run_id'],
       execution_commit=c['parent_commit'],config_sha256=c['parent_config_sha256']).items():
        if w.get(k)!=v:raise ValueError('PARENT_IDENTITY '+k)
    if w['provenance']['original_binary_sha256']!=c['class_binary_sha256']:raise ValueError('PARENT_BINARY')
    if read(d/'input_identity.json')['class_parameters']!=item['class_parameters']:raise ValueError('PARENT_PHYSICAL_VECTOR')
    p=precision(d/'effective_precision.tsv')
    if any(p[k]!=v for k,v in settings(0).items()) or p['thermo_evolver']!=1 or p['background_evolver']!=1:
        raise ValueError('PARENT_PRECISION')
    return d

def prepare(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);r=envelope();r.update(status='FAILED',error='')
    try:
        for key,item in contract()['parents'].items():
            arc=out/(key+'.zip')
            with arc.open('wb') as f:subprocess.run(['gh','api','repos/Morfindien/Bubbleverse/actions/artifacts/'+str(item['artifact_id'])+'/zip'],stdout=f,check=True,timeout=180)
            if arc.stat().st_size!=item['artifact_bytes'] or sha(arc)!=item['artifact_sha256']:raise ValueError('OFFICIAL_ARTIFACT_DIGEST '+key)
            safe_extract(arc,out/key);parent(out,key);arc.unlink()
        r['status']='COMPLETE'
    except Exception as e:r['error']=type(e).__name__+': '+str(e)
    write(out/'input_preparation.json',r);return int(r['status']!='COMPLETE')

def analyze(out,key,level,parents,emit=True):
    import numpy as np
    out=Path(out);old=parent(parents,key);c=contract()
    e=[json.loads(x,object_pairs_hook=unique) for x in (out/'native_trace.jsonl').read_text().splitlines()]
    final=[x for x in e if x['event']=='final']
    if len(final)!=1 or final[0]['cumulative_calls']!=1 or final[0]['scalar_calls']!=len([x for x in e if x['event']=='scalar']):raise ValueError('INTERPOSITION_TRACE_GATE')
    cal=bracket(e)
    if not cal['native_stopping_condition_met']:raise ValueError('CALIBRATION_STOP_GATE')
    actual=precision(out/'effective_precision.tsv');expected=precision(old/'effective_precision.tsv');expected.update(settings(level))
    if actual!=expected:raise ValueError('ONLY_DECLARED_PRECISION_CHANGES')
    meta=read(out/'native_meta.json');nodes=table(out/'final_native_nodes.tsv');raw=table(out/'cumulative_native.tsv')
    if meta['source_patch'] or meta['precision_changed']!=bool(level) or meta['q']!=Q or meta['treatment']!='00':raise ValueError('NATIVE_SCOPE_GATE')
    if any(meta[k] for k in ('has_exotic_injection','has_varconst','has_idm_g')):raise ValueError('REFERENCE_DOMAIN_GATE')
    oldmeta=read(old/'native_meta.json')
    for name in ('nH0_m3','fHe','YHe','sigma_m2','metres_per_Mpc','c_m_s','m_H_kg','not4','reio_parametrization'):
        if meta[name]!=oldmeta[name]:raise ValueError('UNCHANGED_PHYSICAL_NORMALIZATION '+name)
    if any(not np.isfinite(v).all() for v in nodes.values()):raise ValueError('NATIVE_HISTORY_NONFINITE')
    if len(nodes['z'])!=meta['rows'] or len(nodes['z'])>c['caps']['nodes'] or not np.array_equal(nodes['row'],np.arange(len(nodes['z']))):raise ValueError('NATIVE_ROWS')
    if cal['requested_tau']!=c['parents'][key]['class_parameters']['tau_reio'] or meta['tau_reported']!=cal['requested_tau'] or cal['relative_tolerance']!=settings(level)['reionization_optical_depth_tol']:raise ValueError('CALIBRATION_INPUT')
    with (out/'source_species.tsv').open() as f:source_rows=sum(1 for _ in f)-1
    if source_rows!=final[0]['source_rows'] or source_rows<1:raise ValueError('SOURCE_COMPLETENESS')
    if not np.array_equal(raw['eta_Mpc'],nodes['eta_Mpc']) or not np.array_equal(raw['q_1_Mpc'],nodes['q_1_Mpc']):raise ValueError('CUMULATIVE_HISTORY_IDENTITY')
    f=integrals(raw['eta_Mpc'],raw['q_1_Mpc'],raw['q_second_eta']);minus=np.asarray(f['minus']);plus=np.asarray(f['plus']);gauss=np.asarray(f['gauss2'])
    normal=meta['nH0_m3']*meta['sigma_m2']*meta['metres_per_Mpc'];physical=normal*nodes['xe']*(1+nodes['z'])**2
    normalization=float(np.max(np.abs(physical-nodes['q_1_Mpc'])/np.maximum(np.abs(nodes['q_1_Mpc']),np.finfo(float).tiny)))
    d16=redshift_depth(nodes['z'],nodes['xe'],nodes['d2xe_dz2'],nodes['H_1_Mpc'],normal,16)
    d32=redshift_depth(nodes['z'],nodes['xe'],nodes['d2xe_dz2'],nodes['H_1_Mpc'],normal,32)
    trials=[]
    for event in [x for x in e if x['event']=='scalar']:
        if event['support_rows']==0:
            if event['tau']!=0:raise ValueError('ZERO_SUPPORT_TAU')
            trials.append(dict(event,components=None));continue
        t=table(out/f"scalar_{event['call']:03d}.tsv")
        if len(t['z'])!=event['support_rows'] or t['z'][-1]!=event['endpoint_z']:raise ValueError('SCALAR_SUPPORT')
        b=integrals(t['eta_Mpc'],t['q_1_Mpc'],t['q_second_eta'])
        trials.append(dict(event,components={k:b[k][-1] for k in ('plus','minus','gauss2')}))
    last=trials[-1]
    if last['components'] is None:raise ValueError('LAST_SUPPORT_EMPTY')
    windows={}
    for bound in (30,50,1500,float(nodes['z'][-1])):
        mask=nodes['z']<=bound
        windows[str(bound)]=dict(plus_minus_max_abs=float(np.max(np.abs(plus[mask]-minus[mask]))),
          redshift16_32_max_abs=float(np.max(np.abs(d16[mask]-d32[mask]))),
          redshift32_eta_cubic_max_abs=float(np.max(np.abs(d32[mask]-minus[mask]))))
    negative_depth_increments=int((np.diff(d32)<0).sum())
    if emit:
        np.savetxt(out/'representation_comparison.tsv',np.c_[nodes['z'],raw['native_kappa'],plus,minus,gauss,d16,d32],delimiter='\t',fmt='%.17g',header='z\tnative_kappa\tplus\teta_cubic_minus\tgauss2\tz_gauss16\tz_gauss32')
        write(out/'scalar_comparison.json',dict(q=Q,program_id=ID,level=level,trials=trials,reference_truth_gate='UNQUALIFIED'))
    return dict(level=level,native_rows=len(nodes['z']),source_rows=source_rows,calibration=cal,
      effective_precision_changed=list(settings(level)) if level else [],opacity_normalization_max_relative_residual=normalization,
      native_plus_replay_max_abs=float(np.max(np.abs(raw['native_kappa']-plus))),
      cubic_gauss2_max_abs=float(np.max(np.abs(minus-gauss))),windows=windows,
      last_scalar=last,negative_redshift_depth_increments=negative_depth_increments,
      native_underflow_rows=int((nodes['exp_minus_kappa']==0).sum()),
      reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
      quadrature_scope='Cubic total xe and linear sampled H in z; exact cubic q in eta. Representation differences only.',
      species_workspace_qualified=False,physical_response='NOT_YET_COMPUTED')

def worker(key,level,inputs,out,class_root):
    c=contract();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);started=time.monotonic()
    job=key+'-L'+str(level);r=envelope();r.update(job_id=job,parent_key=key,level=level,status='FAILED',error='',theory_evaluations_started=0)
    try:
        if job not in c['expected_jobs'] or level not in (1,2):raise ValueError('JOB_ID_GATE')
        if platform.python_version()!=c['python_version'] or platform.system()!='Linux' or platform.machine()!='x86_64':raise ValueError('RUNTIME_GATE')
        import numpy as np
        if np.__version__!=c['numpy_version']:raise ValueError('NUMPY_GATE')
        if any(os.environ.get(n)!='1' for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')):raise ValueError('THREAD_GATE')
        old=parent(inputs,key);root=Path(class_root).resolve()
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=c['class_commit']:raise ValueError('SOURCE_COMMIT')
        subprocess.run(['git','-C',str(root),'diff','--quiet','HEAD'],check=True)
        for n,h in c['frozen_class_sources'].items():
            if sha(root/n)!=h:raise ValueError('SOURCE_HASH '+n)
        binary=root/c['binary_relative_path']
        if sha(binary)!=c['class_binary_sha256']:raise ValueError('ORIGINAL_BINARY_GATE')
        ldlib=sysconfig.get_config_var('LDLIBRARY');libdir=sysconfig.get_config_var('LIBDIR')
        if not ldlib or not ldlib.startswith('libpython') or '.so' not in ldlib or not libdir:raise ValueError('PYTHON_LINK_GATE')
        params=parameters(c['parents'][key]['class_parameters'],level);(out/'point.ini').write_text(ini(params))
        write(out/'input_identity.json',dict(q=Q,program_id=ID,job_id=job,level=level,class_parameters=params,
          physical_parameters=c['parents'][key]['class_parameters'],precision_overrides=settings(level),
          parent_run_id=c['parent_run_id'],parent_worker_sha256=sha(old/'q045_optical_audit_worker_v3.json')))
        exe=out/'q045_history_observer';cmd=['gcc','-O2','-fopenmp','-rdynamic','-Wall','-Wextra']
        for sub in ('include','external/HyRec2020','external/RecfastCLASS','external/heating'):cmd+=['-I',str(root/sub)]
        cmd +=[str(HERE/'q045_reference_history_probe_v1.c'),str(binary),'-L'+libdir,'-l'+ldlib.removeprefix('lib').split('.so')[0],'-Wl,-rpath,'+str(binary.parent),'-Wl,-rpath,'+libdir,'-ldl','-lm','-o',str(exe)]
        bounded(cmd,out/'compile.log',120)
        r['provenance']=dict(original_binary_sha256=sha(binary),observer_executable_sha256=sha(exe),
          source_commit=c['class_commit'],compile_command=cmd,compiler=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
          original_binary_compiler='NOT DOCUMENTED',python=platform.python_version(),platform=platform.platform(),
          parent_worker_sha256=sha(old/'q045_optical_audit_worker_v3.json'),effective_input_sha256=sha(out/'point.ini'),
          run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT','LOCAL'),runner=os.environ.get('RUNNER_NAME','NOT DOCUMENTED'),
          cpu=platform.processor() or 'NOT DOCUMENTED',thread_controls={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},
          config_sha256=sha(HERE/CONFIG),started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
          observer_scope='Background + thermodynamics only; no spectrum/likelihood evaluation; declared numerical settings changed')
        r['theory_evaluations_started']=1;write(out/'attempt.json',r)
        bounded([str(exe),str(out/'point.ini')],out/'native.log',c['caps']['native_seconds'],dict(os.environ,Q045_TRACE_DIR=str(out)),out)
        if sha(binary)!=c['class_binary_sha256']:raise ValueError('BINARY_MUTATION_GATE')
        r['analysis']=analyze(out,key,level,inputs);r['status']='COMPLETE';r['history_diagnostic_gate']='PASS_COMPONENT_ONLY'
    except Exception as e:r['error']=type(e).__name__+': '+str(e);r['failure_class']='ENVIRONMENT_OR_HISTORY_VALIDATION';r['history_diagnostic_gate']='FAIL'
    r['wall_seconds']=time.monotonic()-started
    r['files']={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!=RESULT}
    write(out/RESULT,r);return int(r['status']!='COMPLETE')

def cubic_at(z,y,second,requested):
    import numpy as np
    requested=np.asarray(requested);i=np.clip(np.searchsorted(z,requested,side='right')-1,0,len(z)-2)
    if requested.min()<z[0] or requested.max()>z[-1]:raise ValueError('COMMON_GRID_DOMAIN')
    h=z[i+1]-z[i];b=(requested-z[i])/h;a=1-b
    return a*y[i]+b*y[i+1]+((a**3-a)*second[i]+(b**3-b)*second[i+1])*h*h/6

def compare_levels(key,paths,analyses,out):
    import numpy as np
    nodes=[table(p/'final_native_nodes.tsv') for p in paths];z=nodes[0]['z'];columns=[z];report={}
    for field,second in (('xe','d2xe_dz2'),('q_1_Mpc','d2q_dz2')):
        v=[cubic_at(n['z'],n[field],n[second],z) for n in nodes];columns.extend(v)
        report[field]={str(bound):dict(max_L0_L1=float(np.max(np.abs(v[0][z<=bound]-v[1][z<=bound]))),
          max_L1_L2=float(np.max(np.abs(v[1][z<=bound]-v[2][z<=bound])))) for bound in (30,50,1500,float(z[-1]))}
    labels='z\txe_L0\txe_L1\txe_L2\tq_L0\tq_L1\tq_L2'
    np.savetxt(out/(key+'_common_grid.tsv'),np.column_stack(columns),delimiter='\t',fmt='%.17g',header=labels)
    report['scalar_sequences']={}
    funcs={'actual_tau':lambda a:a['last_scalar']['tau'],
      'accepted_z_reio':lambda a:a['last_scalar']['z_reio'],
      'selector_endpoint_z':lambda a:a['last_scalar']['endpoint_z'],
      'accepted_cubic_depth':lambda a:a['last_scalar']['components']['minus'],
      'scalar_plus_minus':lambda a:a['last_scalar']['components']['plus']-a['last_scalar']['components']['minus']}
    for label,get in funcs.items():report['scalar_sequences'][label]=convergence([float(get(a)) for a in analyses])
    report.update(reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
       projection='Native cubic xe/q projected onto original L0 z grid; calibration and selector drift included, not isolated continuum error.',
       source_history_certificate='ABSENT',calibration_error_enclosure='ABSENT',species_continuum_certificate='ABSENT')
    return report

def collect(directory,out):
    directory=Path(directory);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    c=contract();r=envelope();records=[];errors=[];paths={};analyses={}
    files=sorted((directory/'workers').rglob(RESULT))
    for p in files:
        try:
            x=read(p);records.append(x);job=x['job_id']
            if job in paths or job not in c['expected_jobs']:raise ValueError('DUPLICATE_OR_UNKNOWN_JOB')
            paths[job]=p.parent
            for k in ('q','program_id','config_sha256','run_id','execution_commit'):
                if x[k]!=r[k]:raise ValueError('MERGE_IDENTITY '+k)
            if x['level'] not in (1,2) or job!=x['parent_key']+'-L'+str(x['level']):raise ValueError('MERGE_LEVEL')
            if x.get('theory_evaluations_started') not in (0,1):raise ValueError('STARTED_COUNT')
            if {f.name for f in p.parent.iterdir() if f.is_file() and f.name!=RESULT}!=set(x['files']):raise ValueError('RAW_PRODUCT_INVENTORY')
            for n,h in x['files'].items():
                if Path(n).name!=n or sha(p.parent/n)!=h:raise ValueError('RAW_PRODUCT_HASH '+n)
            if x['status']!='COMPLETE' or x['history_diagnostic_gate']!='PASS_COMPONENT_ONLY':raise ValueError('WORKER_INCOMPLETE '+job)
            a=analyze(p.parent,x['parent_key'],x['level'],directory/'parents',emit=False)
            if a!=x['analysis']:raise ValueError('SUMMARY_RECONSTRUCTION '+job)
            ident=read(p.parent/'input_identity.json')
            if ident['class_parameters']!=parameters(c['parents'][x['parent_key']]['class_parameters'],x['level']):raise ValueError('INPUT_RECONSTRUCTION')
            analyses[job]=a
        except Exception as e:errors.append(str(e))
    jobs=completeness(c['expected_jobs'],[x['job_id'] for x in records]);started=sum(x.get('theory_evaluations_started',0) for x in records)
    if jobs['gate']!='PASS':errors.append('JOB_COMPLETENESS')
    if started>8:errors.append('EVALUATION_BUDGET')
    comparisons={}
    if not errors:
        try:
            for key in c['parents']:
                p0=parent(directory/'parents',key);a0=analyze(p0,key,0,directory/'parents',emit=False)
                comparisons[key]=compare_levels(key,[p0,paths[key+'-L1'],paths[key+'-L2']],
                    [a0,analyses[key+'-L1'],analyses[key+'-L2']],out.parent)
        except Exception as e:errors.append(str(e))
    r.update(execution_status='COMPLETE' if not errors else 'PARTIAL',result_status='PROVISIONAL_HISTORY_DIAGNOSTIC',
       job_completeness=jobs,merge_compatibility_gate='PASS' if not errors else 'FAIL',
       history_diagnostic_gate='PASS_COMPONENT_ONLY' if not errors else 'FAIL',tests_status='COMPLETE' if not errors else 'INCOMPLETE',
       records=records,errors=errors,history_comparisons=comparisons,expected_jobs=c['expected_jobs'],
       evaluations_inherited=8,evaluations_started_this_target=started,evaluations_total_upper_bound_this_target=16,
       observed_started_count_is_lower_bound=(jobs['gate']!='PASS'),
       inherited_total_budget=52,remaining_budget_lower_bound=36,automatic_continuation=False,
       actual_computed_scientific_result='NOT_YET_COMPUTED',reference_error_bound=None,
       terminal_stage_reason='Finite history stage ends here. Uniform continuum/species/calibration qualification remains absent; no CMB or likelihood response authorized.')
    write(out,r);return int(bool(errors))

def static():
    c=contract();m=read(HERE/'q045_reference_history_manifest_v1.json')
    if c['q']!=Q or c['program_id']!=ID or c['new_theory_evaluations_max']!=8 or c['inherited_evaluations_completed']!=8 or c['inherited_total_evaluation_budget']!=52:raise ValueError('SCOPE_GATE')
    if c['expected_jobs']!=[key+'-L'+str(level) for key in sorted(c['parents']) for level in (1,2)]:raise ValueError('MATRIX_GATE')
    if any(c[k] for k in ('source_patch','reference_treatments_authorized','optimization_authorized','production_restart_authorized')):raise ValueError('NO_TREATMENT_GATE')
    if c['precision_levels']!={str(i):settings(i) for i in (0,1,2)}:raise ValueError('PRECISION_PLAN_GATE')
    for n,h in m['files'].items():
        if sha(HERE/n)!=h:raise ValueError('PACKAGE_HASH '+n)
    reg=read(HERE/'bubbleverse_program_registry.json')['programs']
    if reg.get(ID)!=m['registry_entry'] or reg[ID]['status']!='ACTIVE' or reg[ID]['program_id']!=ID:raise ValueError('REGISTRY_GATE')
    if reg['Q045-OPTICAL-AUDIT-V3']['status']!='COMPLETED' or reg['Q045-BASELINE-V2']['status']!='COMPLETED':raise ValueError('DO_NOT_REPEAT_PARENTS')
    if sha(HERE/'.github/workflows/00-bubbleverse-start.yml')!=m['launcher_sha256']:raise ValueError('LAUNCHER_GATE')
    if not(HERE/reg[ID]['workflow_path']).is_file():raise ValueError('TARGET_GATE')
    if sha(HERE/'Q045_SAMLET_JOURNAL.md')!=c['journal_sha256']:raise ValueError('JOURNAL_CONTINUITY_GATE')
    if sha(HERE/'Q045_OPTICAL_AUDIT_INGESTION_RESULT.json')!=c['ingestion_sha256']:raise ValueError('INGESTION_GATE')
    for word in (ID,'UNQUALIFIED','00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if word not in (HERE/'README.md').read_text():raise ValueError('README_GATE '+word)
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')

def no_repeat():
    if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1':raise ValueError('NO_AUTOMATIC_RETRY_GATE')
    if os.environ.get('GITHUB_REPOSITORY')!='Morfindien/Bubbleverse':raise ValueError('REPOSITORY_GATE')
    current=os.environ['GITHUB_RUN_ID']
    rows=json.loads(subprocess.check_output(['gh','api','repos/Morfindien/Bubbleverse/actions/workflows/q045-reference-history-v1.yml/runs?event=workflow_dispatch&per_page=100'],text=True,timeout=60))
    if any(str(r['id'])!=current for r in rows['workflow_runs']):raise ValueError('NO_REPEAT_CAMPAIGN_GATE: prior launch exists; ingest its records and decide recovery explicitly')

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    s.add_parser('static');s.add_parser('no-repeat')
    a=s.add_parser('prepare');a.add_argument('--out',required=True)
    a=s.add_parser('worker');a.add_argument('--job',required=True);a.add_argument('--level',required=True,type=int);a.add_argument('--inputs',required=True);a.add_argument('--out',required=True);a.add_argument('--class-root',required=True)
    a=s.add_parser('collect');a.add_argument('--directory',required=True);a.add_argument('--out',required=True)
    a=p.parse_args()
    if a.command=='static':static();return 0
    if a.command=='no-repeat':no_repeat();return 0
    if a.command=='prepare':return prepare(a.out)
    if a.command=='worker':return worker(a.job,a.level,a.inputs,a.out,a.class_root)
    return collect(a.directory,a.out)

if __name__=='__main__':sys.exit(main())

