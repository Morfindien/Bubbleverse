"""Q045 V2: OFFLINE ARTIFACT REANALYSIS ONLY. No native execution entry point."""
from pathlib import Path

import argparse, hashlib, json, math, os, re

import subprocess, sys, zipfile

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
    norm=normalization_check(meta,oldmeta,c['parents'][key]['class_parameters'])
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
    return dict(normalization_comparison=norm,level=level,native_rows=len(nodes['z']),source_rows=source_rows,calibration=cal,
      effective_precision_changed=list(settings(level)) if level else [],opacity_normalization_max_relative_residual=normalization,
      native_plus_replay_max_abs=float(np.max(np.abs(raw['native_kappa']-plus))),
      cubic_gauss2_max_abs=float(np.max(np.abs(minus-gauss))),windows=windows,
      last_scalar=last,negative_redshift_depth_increments=negative_depth_increments,
      native_underflow_rows=int((nodes['exp_minus_kappa']==0).sum()),
      reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
      quadrature_scope='Cubic total xe and linear sampled H in z; exact cubic q in eta. Representation differences only.',
      species_workspace_qualified=False,physical_response='NOT_YET_COMPUTED')

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

HERE=Path(__file__).resolve().parent
Q='Q-045';ID='Q045-REFHIST-V2';RESULT='q045_reference_history_worker_v1.json'
CONFIG='q045_reference_history_contract_v1.json'
def contract():return read(HERE/CONFIG)

def normalization_check(meta,oldmeta,physical):
    import struct
    for name in ('nH0_m3','fHe','sigma_m2','metres_per_Mpc','c_m_s','m_H_kg','not4','reio_parametrization'):
        if meta[name]!=oldmeta[name]:raise ValueError('UNCHANGED_PHYSICAL_NORMALIZATION '+name)
    old,new=oldmeta['YHe'],meta['YHe']
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<v<1 for v in (old,new)):
        raise ValueError('INVALID_YHe')
    # Positive finite binary64 values have monotonically ordered bit patterns.
    bits=lambda v:struct.unpack('>Q',struct.pack('>d',v))[0]
    distance=abs(bits(new)-bits(old))
    derived=physical.get('YHe','BBN')=='BBN'
    if distance and (not derived or distance>1):raise ValueError('YHe_DRIFT_OUTSIDE_DECLARED_OFFLINE_RECOVERY')
    return dict(YHe_old=old,YHe_new=new,YHe_delta=new-old,YHe_ulp_distance=distance,
      YHe_bitwise_equal=(distance==0),YHe_is_BBN_derived=derived,
      normalization_constants_bitwise_equal=True,
      scope='At most one binary64 ULP in BBN-derived output only; explicit inputs and opacity normalization remain exact.',
      physical_reference_qualified=False)

RECOVERY_CONFIG='q045_reference_history_contract_v2.json'
def recovery_contract():return read(HERE/RECOVERY_CONFIG)

def envelope():
    c=recovery_contract()
    return dict(q=Q,program_id=ID,case_id='NOT DOCUMENTED',scientific_question=contract()['scientific_question'],
      config_sha256=sha(HERE/RECOVERY_CONFIG),source_program_id='Q045-REFHIST-V1',source_run_id=c['source_run_id'],
      source_execution_commit=c['source_commit'],run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),
      execution_commit=os.environ.get('GITHUB_SHA','LOCAL_NOT_COMMITTED'),
      execution_mode='OFFLINE_ARTIFACT_REANALYSIS_ONLY',new_theory_evaluations=0,
      final_result_gate='UNRESOLVED',reference_truth_gate='UNQUALIFIED',reference_error_bound=None,
      production_restart_authorized=False,automatic_continuation=False,
      full_matrix_budget_gate='FAIL_FOR_UNMODIFIED_48_FULL_PLAN_AFTER_THIS_STAGE',
      next_motor='Result Ingestion & Routing Engine')

def check_id(value):
    if value!=ID:raise ValueError('PROGRAM_ID_GATE')

def verify_product(directory,item):
    directory=Path(directory)
    files={p.relative_to(directory).as_posix():sha(p) for p in directory.rglob('*') if p.is_file()}
    if files!=item['members_sha256']:raise ValueError('FROZEN_ARTIFACT_MEMBERS '+item['name'])
    return directory

def prepare(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);r=envelope();r.update(status='FAILED',artifacts=[],errors=[])
    try:
        for item in recovery_contract()['artifacts']:
            target=out/item['name'];arc=out/(str(item['id'])+'.zip')
            with arc.open('wb') as f:
                subprocess.run(['gh','api','repos/Morfindien/Bubbleverse/actions/artifacts/'+str(item['id'])+'/zip'],stdout=f,check=True,timeout=180)
            if arc.stat().st_size!=item['size_in_bytes'] or 'sha256:'+sha(arc)!=item['digest']:raise ValueError('FROZEN_ARTIFACT_ARCHIVE '+item['name'])
            if target.exists():raise ValueError('DO_NOT_MIX_EXISTING_INPUT_DIRECTORY')
            safe_extract(arc,target);verify_product(target,item);arc.unlink()
            r['artifacts'].append(dict(id=item['id'],name=item['name'],archive_digest=item['digest'],gate='PASS'))
        r['status']='COMPLETE'
    except Exception as e:r['errors'].append(type(e).__name__+': '+str(e))
    write(out/'input_preparation_v2.json',r);return int(r['status']!='COMPLETE')

def verify_worker(item,path,c):
    # Original failed records stay failed; their raw data are recovered separately.
    x=read(path/RESULT);job=item['job_id'];key,lev=job.rsplit('-L',1);level=int(lev)
    frozen=dict(q=Q,program_id='Q045-REFHIST-V1',job_id=job,parent_key=key,level=level,
      run_id=c['source_run_id'],execution_commit=c['source_commit'],config_sha256=c['source_config_sha256'],theory_evaluations_started=1)
    if any(x.get(k)!=v for k,v in frozen.items()):raise ValueError('ORIGINAL_WORKER_IDENTITY '+job)
    if x.get('status') not in ('COMPLETE','FAILED'):raise ValueError('ORIGINAL_WORKER_STATUS')
    if x['status']=='FAILED' and x.get('error')!='ValueError: UNCHANGED_PHYSICAL_NORMALIZATION YHe':raise ValueError('UNAPPROVED_FAILURE_RECOVERY')
    if x['provenance']['original_binary_sha256']!=contract()['class_binary_sha256'] or x['provenance']['source_commit']!=contract()['class_commit']:raise ValueError('FROZEN_ORIGINAL_BINARY')
    actual={p.name:sha(p) for p in path.iterdir() if p.is_file() and p.name!=RESULT}
    if actual!=x['files']:raise ValueError('ORIGINAL_WORKER_RAW_INVENTORY')
    ident=read(path/'input_identity.json');physical=contract()['parents'][key]['class_parameters']
    if ident['class_parameters']!=parameters(physical,level) or ident['physical_parameters']!=physical or ident['precision_overrides']!=settings(level):raise ValueError('EXACT_PHYSICAL_INPUT_VECTOR')
    if any(ident.get(k)!=v for k,v in dict(q=Q,program_id='Q045-REFHIST-V1',job_id=job,level=level,parent_run_id=contract()['parent_run_id']).items()):raise ValueError('RAW_INPUT_IDENTITY')
    return x,key,level

def collect(directory,out):
    directory=Path(directory);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    c=recovery_contract();r=envelope();errors=[];records=[];analyses={};paths={};comparisons={};native_started=0
    try:
        import numpy as np
        if np.__version__!=c['numpy_version']:raise ValueError('PINNED_NUMPY_GATE')
        r['reanalysis_runtime']=dict(python=sys.version,numpy=np.__version__,
          original_python=contract()['python_version'],original_numpy=contract()['numpy_version'],
          successful_original_summaries_required_bitwise_equal=True)
        if sha(HERE/CONFIG)!=c['source_config_sha256']:raise ValueError('FROZEN_SCIENTIFIC_CONTRACT')
        items=c['artifacts']
        if len(items)!=10 or len({x['id'] for x in items})!=10 or len({x['name'] for x in items})!=10:raise ValueError('ARTIFACT_COMPLETENESS')
        for item in items:verify_product(directory/item['name'],item)
        parent_item=next(x for x in items if x['role']=='parents');parents=directory/parent_item['name']
        original_final=read(directory/next(x for x in items if x['role']=='final')['name']/'q045_reference_history_final_v1.json')
        if original_final['run_id']!=c['source_run_id'] or original_final['execution_commit']!=c['source_commit']:raise ValueError('ORIGINAL_FINAL_IDENTITY')
        r['preserved_original_final']=original_final
        for item in (x for x in items if x['role']=='worker'):
            p=directory/item['name']/'q045_output';x,key,level=verify_worker(item,p,c);job=x['job_id']
            if job in paths:raise ValueError('DUPLICATE_WORKER')
            paths[job]=p;native_started+=x['theory_evaluations_started']
            a=analyze(p,key,level,parents,emit=False)
            if x['status']=='COMPLETE' and {k:v for k,v in a.items() if k!='normalization_comparison'}!=x['analysis']:raise ValueError('SUCCESSFUL_DIAGNOSTIC_CHANGED '+job)
            analyses[job]=a
            write(out.parent/'recovered_workers'/(job+'.json'),dict(**envelope(),job_id=job,
              original_status=x['status'],original_error=x['error'],original_worker_sha256=sha(p/RESULT),
              recovery_status='COMPLETE',history_diagnostic_gate='PASS_COMPONENT_ONLY',analysis=a))
            records.append(dict(job_id=job,original_status=x['status'],original_error=x['error'],
              original_worker_sha256=sha(p/RESULT),recovery_status='COMPLETE',analysis=a))
        jobs=completeness(contract()['expected_jobs'],list(paths))
        if jobs['gate']!='PASS' or native_started!=8:raise ValueError('ALL_EIGHT_NATIVE_OUTCOMES_REQUIRED')
        for key in contract()['parents']:
            p0=parent(parents,key);a0=analyze(p0,key,0,parents,emit=False)
            comparisons[key]=compare_levels(key,[p0,paths[key+'-L1'],paths[key+'-L2']],
              [a0,analyses[key+'-L1'],analyses[key+'-L2']],out.parent)
        r['job_completeness']=jobs
    except Exception as e:errors.append(type(e).__name__+': '+str(e))
    r.update(execution_status='COMPLETE' if not errors else 'PARTIAL',result_status='TECHNICALLY_VALIDATED_HISTORY_DIAGNOSTIC' if not errors else 'INVALID_RECOVERY',
      original_execution_status='FAILED_POSTPROCESSING',original_native_evaluations_started=8,
      recovered_records=records,errors=errors,history_comparisons=comparisons,
      merge_compatibility_gate='PASS' if not errors else 'FAIL',history_diagnostic_gate='PASS_COMPONENT_ONLY' if not errors else 'FAIL',
      tests_status='COMPLETE' if not errors else 'INCOMPLETE',original_evaluations_inherited=8,
      evaluations_consumed_total=16,inherited_total_budget=52,remaining_budget=36,
      actual_computed_scientific_result='NOT_YET_COMPUTED',
      terminal_stage_reason='Offline recovery ends here. No native rerun, CMB response, likelihood response or qualified continuum/reference error bound.')
    products=[out.parent/'recovered_workers'/(x['job_id']+'.json') for x in records]
    products += [out.parent/(key+'_common_grid.tsv') for key in comparisons]
    r['derived_files_sha256']={p.relative_to(out.parent).as_posix():sha(p) for p in sorted(products)}
    write(out,r);return int(bool(errors))

def static():
    c=recovery_contract();m=read(HERE/'q045_reference_history_manifest_v2.json')
    if c['q']!=Q or c['program_id']!=ID or c['new_theory_evaluations_max']!=0 or c['execution_mode']!='OFFLINE_ARTIFACT_REANALYSIS_ONLY':raise ValueError('ZERO_NATIVE_SCOPE_GATE')
    if sha(HERE/CONFIG)!=c['source_config_sha256']:raise ValueError('SCIENTIFIC_CONTRACT_GATE')
    if sha(HERE/'Q045_SAMLET_JOURNAL.md')!=c['journal_sha256'] or sha(HERE/'Q045_EXECUTION_HANDOFF.md')!=c['handoff_sha256']:raise ValueError('JOURNAL_CONTINUITY_GATE')
    for name,digest in m['files'].items():
        if sha(HERE/name)!=digest:raise ValueError('PACKAGE_HASH '+name)
    reg=read(HERE/'bubbleverse_program_registry.json')['programs']
    if reg.get(ID)!=m['registry_entry'] or reg[ID]['status']!='ACTIVE' or reg[ID]['program_id']!=ID:raise ValueError('REGISTRY_GATE')
    if reg['Q045-REFHIST-V1']['status']!='COMPLETED_WITH_POSTPROCESSING_FAILURE':raise ValueError('DO_NOT_REPEAT_NATIVE_CAMPAIGN')
    if sha(HERE/'.github/workflows/00-bubbleverse-start.yml')!=m['launcher_sha256']:raise ValueError('LAUNCHER_GATE')
    if reg[ID]['q']!=Q or reg[ID]['current_q']!=Q or reg[ID]['workflow_id']!='q045-reference-history-v2.yml' or reg[ID]['workflow_path']!='.github/workflows/q045-reference-history-v2.yml' or reg[ID]['new_theory_evaluations_max']!=0:raise ValueError('REGISTRY_Q_TARGET_SCOPE')
    for word in (ID,'UNQUALIFIED','00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if word not in (HERE/'README.md').read_text():raise ValueError('README_GATE')
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS ZERO_NEW_THEORY=PASS')

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('static')
    q=sub.add_parser('prepare');q.add_argument('--out',required=True)
    q=sub.add_parser('collect');q.add_argument('--directory',required=True);q.add_argument('--out',required=True)
    args=p.parse_args()
    if args.command=='static':static();return 0
    if args.command=='prepare':return prepare(args.out)
    return collect(args.directory,args.out)

if __name__=='__main__':sys.exit(main())
