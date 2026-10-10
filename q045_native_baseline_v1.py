"""Q045 finite native baseline acquisition. No repair, optimizer or reference run."""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, math, os, platform, re
import signal, subprocess, sys, time, zipfile

HERE=Path(__file__).resolve().parent
Q='Q-045'; ID='Q045-BASELINE-V1'; CONTRACT='q045_native_baseline_contract_v1.json'
RESULT='q045_worker_result_v1.json'

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError('DUPLICATE_JSON_KEY '+k)
        d[k]=v
    return d

def read(p):
    return json.loads(Path(p).read_text(),object_pairs_hook=unique,
                      parse_constant=lambda s:(_ for _ in ()).throw(ValueError('NONFINITE_JSON '+s)))

def write(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(d,indent=2,allow_nan=False,ensure_ascii=False)+'\n')
    tmp.replace(p)

def contract(): return read(HERE/CONTRACT)

def base():
    c=contract()
    return dict(q=Q,q_status=c['q_status'],program_id=ID,
                scientific_question=c['scientific_question'],run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),
                config_sha256=sha(HERE/CONTRACT),execution_commit=os.environ.get('GITHUB_SHA','LOCAL_NOT_COMMITTED'),
                scientific_result=False,final_result_gate='UNRESOLVED',result_status='RAW_NOT_QUALIFIED',
                history_accuracy_gate='UNRESOLVED',reference_truth_gate='BLOCKED',
                decision_margin_gate='MISSING_ACTUAL_MARGIN',production_restart_authorized=False,
                next_motor='Result Ingestion & Routing Engine')

def check_id(s):
    if not re.fullmatch(r'[A-Z0-9][A-Z0-9-]{2,63}',s or '') or s!=ID:
        raise ValueError('PROGRAM_ID_GATE')
    return s

def static():
    c=contract();m=read(HERE/'q045_native_baseline_manifest_v1.json')
    if c['q']!=Q or c['program_id']!=ID or c['start_index']!=0 or c['native_treatment']!='00':
        raise ValueError('Q_SCOPE_GATE')
    if any(c[k] for k in ('production_restart_authorized','reference_treatments_authorized',
                         'optimization_authorized','posterior_inference_authorized')): raise ValueError('SCOPE_GATE')
    for n,h in m['immutable_files'].items():
        if not (HERE/n).is_file() or sha(HERE/n)!=h: raise ValueError('PACKAGE_HASH '+n)
    for n,h in c['frozen_reused_files'].items():
        if sha(HERE/n)!=h: raise ValueError('REUSED_SOURCE_HASH '+n)
    if sha(HERE/'.github/workflows/00-bubbleverse-start.yml')!=m['launcher_sha256']:
        raise ValueError('LAUNCHER_GATE')
    reg=read(HERE/'bubbleverse_program_registry.json')['programs']
    if reg.get(ID)!=m['registry_entry'] or reg[ID]['status']!='ACTIVE': raise ValueError('REGISTRY_GATE')
    if not (HERE/reg[ID]['workflow_path']).is_file(): raise ValueError('TARGET_GATE')
    if sha(HERE/c['parent_journal_file'])!=c['parent_journal_sha256']: raise ValueError('JOURNAL_CONTINUITY_GATE')
    if 'Q042-CONTEXT-V29' in reg and reg['Q042-CONTEXT-V29']['status']!='COMPLETED':
        raise ValueError('HISTORICAL_RELAUNCH_GATE')
    for word in (ID,'RAW_NOT_QUALIFIED','00-bubbleverse-start.yml','bubbleverse_program_registry.json'):
        if word not in (HERE/'README.md').read_text(): raise ValueError('README_GATE '+word)
    print('PACKAGE_GATE=PASS LAUNCHER_GATE=PASS README_GATE=PASS REPOSITORY_CONSISTENCY_GATE=PASS')
    return c

def extract(p,dest):
    dest=Path(dest).resolve()
    with zipfile.ZipFile(p) as z:
        if sum(i.file_size for i in z.infolist())>contract()['resource_caps']['input_uncompressed_bytes']:
            raise ValueError('ARCHIVE_SIZE_GATE')
        seen=set()
        for i in z.infolist():
            name=i.filename
            if name in seen: raise ValueError('ARCHIVE_DUPLICATE')
            seen.add(name)
            target=(dest/name).resolve()
            if '\\' in name or Path(name).is_absolute() or not target.is_relative_to(dest):
                raise ValueError('ARCHIVE_PATH_GATE')
            if ((i.external_attr >> 16)&0o170000)==0o120000: raise ValueError('ARCHIVE_SYMLINK_GATE')
        z.extractall(dest)

def verify_inputs(d):
    c=contract();d=Path(d)
    for n,h in c['frozen_input_files'].items():
        if not (d/n).is_file() or sha(d/n)!=h: raise ValueError('INPUT_HASH '+n)
    return c

def prepare(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);b=base();error=''
    try:
        c=static();a=c['environment_artifact']
        if os.environ.get('GITHUB_REPOSITORY')!='Morfindien/Bubbleverse': raise ValueError('REPOSITORY_GATE')
        # GitHub transports an internal artifact archive. No archive is a user deliverable.
        arc=out/'source.zip'
        with arc.open('wb') as f:
            subprocess.run(['gh','api',f"repos/Morfindien/Bubbleverse/actions/artifacts/{a['id']}/zip"],
                           stdout=f,check=True,timeout=c['resource_caps']['download_seconds'])
        if arc.stat().st_size!=a['size_in_bytes'] or sha(arc)!=a['sha256']: raise ValueError('ARTIFACT_DIGEST_GATE')
        extract(arc,out/'inputs');verify_inputs(out/'inputs');arc.unlink()
        status='COMPLETE'
    except Exception as e:
        status='FAILED';error=type(e).__name__+': '+str(e)
    write(out/'input_preparation.json',dict(**b,status=status,error=error))
    return int(bool(error))

def head(p): return subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()

def runtime_preflight(inputs):
    c=verify_inputs(inputs)
    if platform.python_version()!=c['python_version']: raise ValueError('PYTHON_VERSION_GATE')
    if platform.system()!='Linux' or platform.machine()!='x86_64': raise ValueError('PLATFORM_GATE')
    versions={p:importlib.metadata.version(p) for p in c['software_versions']}
    if versions!=c['software_versions']: raise ValueError('DEPENDENCY_VERSION_GATE '+str(versions))
    roots={n:HERE/'external'/n for n in c['external_source_commits']}
    for n,p in roots.items():
        if head(p)!=c['external_source_commits'][n]: raise ValueError('SOURCE_COMMIT_GATE '+n)
        subprocess.run(['git','-C',str(p),'diff','--quiet','HEAD'],check=True)
    for n,h in c['frozen_class_sources'].items():
        if sha(roots['class_ede']/n)!=h: raise ValueError('CLASS_SOURCE_HASH '+n)
    binary=roots['class_ede']/ 'python/build/lib.linux-x86_64-cpython-311/classy.cpython-311-x86_64-linux-gnu.so'
    if not binary.is_file() or sha(binary)!=c['class_binary_sha256']: raise ValueError('ORIGINAL_BINARY_GATE')
    if head(HERE/'q032_parent')!=c['q032_execution_commit']: raise ValueError('Q032_COMMIT_GATE')
    runtime=read(Path(inputs)/'q042_runtime/q042_external_runtime_provenance_prod_v1.json')
    packages=HERE/'external/cobaya_packages'
    for x in runtime['pantheonplus_runtime_files']:
        if sha(packages/x['path'])!=x['sha256']: raise ValueError('SN_DATA_HASH '+x['path'])
    pf=read(Path(inputs)/'q032_preflight/q032_preflight_sealed_v2.json')
    for x in list(pf['hillipop_data_runtime']['data_hashes'].values())+list(pf['hillipop_data_runtime']['cross_spectrum_hashes'].values()):
        old=x['path'];rel=old.split('/external/cobaya_packages/',1)[1]
        if sha(packages/rel)!=x['sha256']: raise ValueError('PLANCK_DATA_HASH '+rel)
    ds=pf['camspec_runtime']['dataset_file'].split('/external/cobaya_packages/',1)[1]
    if sha(packages/ds)!=pf['camspec_runtime']['dataset_file_sha256']: raise ValueError('CAMSPEC_DATASET_HASH')
    # Complete current data snapshot is retained and compared across workers.
    # Hashes not present in the frozen parent records are not claimed independently qualified.
    data={str(p.relative_to(packages)):sha(p) for p in sorted((packages/'data').rglob('*'))
          if p.is_file() and '.git' not in p.parts}
    env={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')}
    if any(v!='1' for v in env.values()): raise ValueError('THREAD_POLICY_GATE')
    return dict(class_binary_sha256=sha(binary),class_commit=c['class_commit'],binary_path=str(binary),
                python=platform.python_version(),platform=platform.platform(),software_versions=versions,
                external_source_commits=c['external_source_commits'],cached_data_sha256=data,
                thread_policy=env,complete_parent_data_hash_qualification=False,
                parent_binary_equivalence='UNRESOLVED_BEYOND_DOCUMENTED_DIAGNOSTIC_BINARY')

def safe_number(x):
    y=float(x)
    if not math.isfinite(y): raise ValueError('NONFINITE_NUMERICAL_VALUE')
    return y

def table(out,name,columns,required):
    import numpy as np
    if not set(required).issubset(columns): raise ValueError('PRODUCT_COLUMNS '+name)
    names=list(columns);arrays=[np.asarray(columns[n],dtype=float) for n in names]
    if not arrays or any(a.ndim!=1 or a.size<3 or not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError('PRODUCT_FINITE '+name)
    if len({a.size for a in arrays})!=1: raise ValueError('PRODUCT_LENGTH '+name)
    np.savetxt(out/(name+'.tsv'),np.column_stack(arrays),delimiter='\t',fmt='%.17g',header='\t'.join(names))
    return dict(file=name+'.tsv',columns=names,rows=int(arrays[0].size),sha256=sha(out/(name+'.tsv')))

def worker(arm,model_name,inputs,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);inputs=Path(inputs).resolve()
    key=arm+'-'+model_name;b=base();started=time.monotonic();rec=dict(**b,job_id=key,status='FAILED',error='',artifacts={})
    write(out/'attempt.json',dict(**b,job_id=key,status='PREFLIGHT_PENDING'))
    model=None
    try:
        c=contract()
        if key not in c['expected_jobs']: raise ValueError('JOB_ID_GATE')
        if os.environ.get('GITHUB_RUN_ATTEMPT','1')!='1': raise ValueError('NO_RETRY_GATE')
        if (out/RESULT).exists(): raise ValueError('OUTPUT_REUSE_GATE')
        provenance=runtime_preflight(inputs);rec['provenance']=provenance
        # Actual builders and start rule are reused byte-for-byte, not reimplemented.
        import q042_production_v1 as prod
        a=argparse.Namespace(q032_parent_root=str(HERE/'q032_parent'),
          preflight=str(inputs/'q032_preflight/q032_preflight_sealed_v2.json'),
          parent_dir=str(inputs/'q032_parent_profiles'),
          hlp_matrix=str(inputs/'q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.npy'),
          hlp_meta=str(inputs/'q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.json'),
          reduced_support=str(inputs/'q042_environment/q042_primary_nonoverlap_support_prod_v1.json'),
          reduced_hlp_matrix=str(inputs/'q042_environment/q042_hillipop_nonoverlap_precision_prod_v1.npy'),
          reduced_hlp_meta=str(inputs/'q042_environment/q042_hillipop_nonoverlap_precision_prod_v1.json'))
        q32=prod.core.legacy.load_q032(a.q032_parent_root)
        info,meta=prod.build_info(a,arm,model_name,'FULL',out/'unused_sampler_prefix')
        pref=prod.preferred(a,arm);starts=prod.production_start(q32,info,pref,0)
        # Preferred raw parent must NOT overwrite the 5%-interior clipping in start 0.
        vec=q32.reference_vector(info,preferred=starts)
        if any(not math.isfinite(float(v)) for v in vec.values()): raise ValueError('VECTOR_FINITE_GATE')
        write(out/'sampled_vector.json',dict(**b,job_id=key,start_index=0,values=vec,start_rule_values=starts,
             scientific_role='DIAGNOSTIC_START_NOT_OPTIMIZED_MINIMUM',parent_metadata=meta))
        # get_model has no sampler; retains all fixed/derived/prior/likelihood definitions.
        model=q32.create_model(info)
        sampled=list(model.parameterization.sampled_params())
        if set(sampled)!=set(vec): raise ValueError('FULL_VECTOR_GATE')
        backends=[t for t in model.theory.values() if hasattr(t,'classy_module') and hasattr(t,'classy')]
        if len(backends)!=1: raise ValueError('ONE_CLASS_BACKEND_GATE')
        backend=backends[0]
        if sha(Path(backend.classy_module.__file__).resolve())!=c['class_binary_sha256']:
            raise ValueError('ACTUAL_BINARY_ROUTE_GATE')
        names=list(model.likelihood)
        required=set(prod.COMMON_EXTERNAL_COMPONENTS) if hasattr(prod,'COMMON_EXTERNAL_COMPONENTS') else set(prod.core.COMMON_EXTERNAL_COMPONENTS)
        if not required.issubset(names): raise ValueError('FULL_EXTERNAL_DATA_GATE')
        native=q32.CAMSPEC if arm=='camspec' else q32.HILLIPOP
        if native not in names: raise ValueError('NATIVE_ARM_GATE')
        # No new requirements, no precision change, no calibration fix, one evaluation.
        lp=model.logposterior(vec)
        logpost=safe_number(lp.logpost);loglikes=[safe_number(x) for x in lp.loglikes]
        logpriors=[safe_number(x) for x in lp.logpriors]
        if len(loglikes)!=len(names): raise ValueError('LIKELIHOOD_COMPONENT_GATE')
        write(out/'likelihood.json',dict(**b,job_id=key,logposterior=logpost,
            loglikelihood_components=dict(zip(names,loglikes)),loglikelihood_sum=math.fsum(loglikes),
            logprior_components=logpriors,likelihood_is_not_posterior=True))
        cls=model.provider.get_Cl(ell_factor=False,units='muK2')
        therm=backend.classy.get_thermodynamics();background=backend.classy.get_background()
        products=[table(out,'spectra',{n:cls[n] for n in ('ell','tt','te','ee')},('ell','tt','te','ee')),
                  table(out,'thermodynamics',therm,('z','x_e')),
                  table(out,'background',background,('z','H [1/Mpc]'))]
        import numpy as np
        z=np.asarray(therm['z']);xe=np.asarray(therm['x_e'])
        if not (z[0]==0 and np.all(np.diff(z)>0) and np.all(xe>=0)):
            raise ValueError('THERMODYNAMICS_ORDER_OR_POSITIVITY')
        if not (len(cls['ell'])>=9001 and np.array_equal(np.asarray(cls['ell']),np.arange(len(cls['ell'])))):
            raise ValueError('FULL_SPECTRUM_SUPPORT')
        # Available total x_e is not a qualified separate hydrogen/helium trajectory.
        write(out/'product_manifest.json',dict(**b,job_id=key,products=products,
            units={'spectra':'C_ell, muK^2, no ell factor','thermodynamics':'native CLASS column labels; x_e electrons per H nucleus',
                   'background':'native CLASS column labels; H [1/Mpc], conformal time [Mpc]'},
            separate_species_history_qualified=False,upstream_accuracy_qualified=False))
        write(out/'runtime_input_manifest.json',dict(**b,job_id=key,
            class_parameters=dict(backend.classy.pars),parent_metadata=meta,
            external_signature=prod.external_signature(info),likelihood_names=names,
            model_info=prod.core._canonical_jsonable(q32.model_info_only(info)),
            stop='No modified integration or posterior result is implied.'))
        rec.update(status='COMPLETE',baseline_gate='PASS_NATIVE_DIAGNOSTIC_ONLY')
    except Exception as e:
        rec.update(error=type(e).__name__+': '+str(e),baseline_gate='FAIL',failure_class='VALIDATION_OR_NATIVE_NUMERICAL')
    finally:
        if model is not None:
            try:model.close()
            except Exception as e:rec['cleanup_error']=repr(e)
    rec['elapsed_seconds']=time.monotonic()-started
    rec['artifacts']={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!=RESULT}
    write(out/RESULT,rec)
    return int(rec['status']!='COMPLETE')

def run(arm,model_name,inputs,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);b=base();key=arm+'-'+model_name
    write(out/'attempt.json',dict(**b,job_id=key,status='PENDING'))
    cmd=[sys.executable,str(HERE/'q045_native_baseline_v1.py'),'worker',
         '--arm',arm,'--model',model_name,'--inputs',str(inputs),'--out',str(out)]
    proc=None;error=''
    try:
        with (out/'native.log').open('w') as log:
            proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            deadline=time.monotonic()+contract()['resource_caps']['native_evaluation_seconds']
            while proc.poll() is None:
                if time.monotonic()>deadline: raise ValueError('NATIVE_WALL_TIME_CAP')
                if sum(p.stat().st_size for p in out.rglob('*') if p.is_file())>contract()['resource_caps']['output_bytes']:
                    raise ValueError('OUTPUT_STORAGE_CAP')
                time.sleep(.25)
    except Exception as e:error=type(e).__name__+': '+str(e)
    finally:
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid,signal.SIGKILL);proc.wait()
    if error or not (out/RESULT).is_file():
        r=dict(**b,job_id=key,status='FAILED',baseline_gate='FAIL',error=error or 'WORKER_NO_RESULT',
               failure_class='HPC_OR_NATIVE_PROCESS',artifacts={})
    else:r=read(out/RESULT)
    r['process_returncode']=proc.returncode if proc else None
    if r['process_returncode']!=0: r['status']='FAILED';r['baseline_gate']='FAIL'
    r['artifacts']={p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!=RESULT}
    write(out/RESULT,r)
    return int(r['status']!='COMPLETE')

def collect(directory,out):
    c=contract();b=base();found=list(Path(directory).rglob(RESULT));rows=[];errors=[];seen=set()
    required={'sampled_vector.json','likelihood.json','spectra.tsv','background.tsv','thermodynamics.tsv',
              'product_manifest.json','runtime_input_manifest.json','native.log'}
    try:
        rows=[read(p) for p in found]
        if len(found)!=4: raise ValueError('JOB_COMPLETENESS count='+str(len(found)))
        signatures=[];data=[]
        # Retain every independently completed/failed record even if one gate fails.
        for p in found:
            r=read(p);key=r.get('job_id')
            if key in seen or key not in c['expected_jobs']: raise ValueError('JOB_DUPLICATE_OR_UNEXPECTED')
            seen.add(key)
            for k in ('q','program_id','run_id','config_sha256','execution_commit'):
                if r.get(k)!=b[k]: raise ValueError('MERGE_IDENTITY '+k)
            for n,h in r['artifacts'].items():
                if Path(n).name!=n or not (p.parent/n).is_file() or sha(p.parent/n)!=h:
                    raise ValueError('RESULT_ARTIFACT_HASH '+n)
            if r['status']!='COMPLETE' or not required.issubset(r['artifacts']): raise ValueError('BASELINE_INCOMPLETE '+key)
            if r['provenance']['class_binary_sha256']!=c['class_binary_sha256']: raise ValueError('MERGE_BINARY')
            im=read(p.parent/'runtime_input_manifest.json');pm=read(p.parent/'product_manifest.json')
            for x in (im,pm,read(p.parent/'likelihood.json'),read(p.parent/'sampled_vector.json')):
                for k in ('q','program_id','run_id','config_sha256','job_id'):
                    if x.get(k)!=r[k]: raise ValueError('PRODUCT_IDENTITY '+k)
            signatures.append(im['external_signature']);data.append(r['provenance']['cached_data_sha256'])
        if seen!=set(c['expected_jobs']): raise ValueError('JOB_SET_GATE')
        if any(x!=signatures[0] for x in signatures) or any(x!=data[0] for x in data):
            raise ValueError('MATCHED_EXTERNAL_INPUT_GATE')
    except Exception as e:errors.append(type(e).__name__+': '+str(e))
    result=dict(**b,execution_status='COMPLETE' if not errors else 'PARTIAL_OR_FAILED',
        job_completeness_gate='PASS' if not errors else 'FAIL',merge_compatibility_gate='PASS' if not errors else 'FAIL',
        baseline_gate='PASS_NATIVE_DIAGNOSTIC_ONLY' if not errors else 'FAIL',tests_status='BASELINE_CHECKS_COMPLETE' if not errors else 'INCOMPLETE',
        expected_jobs=c['expected_jobs'],completed_jobs=[r['job_id'] for r in rows if r.get('status')=='COMPLETE'],
        failed_jobs=[r.get('job_id') for r in rows if r.get('status')!='COMPLETE'],
        pending_jobs=[j for j in c['expected_jobs'] if j not in {r.get('job_id') for r in rows}],
        errors=errors,worker_results=rows,actual_computed_scientific_result='NOT_AVAILABLE',
        next_required_action='Ingest raw baselines or failed gate. Qualify histories/reference and actual inference margins before integration-treatment tests.',
        journal_effect='ADD finite technical acquisition only; KEEP all prior scientific boundaries.')
    write(out,result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('static','prepare','run','worker','collect'))
    p.add_argument('--arm',choices=('camspec','hillipop'));p.add_argument('--model',choices=('lcdm','ede_n3'))
    p.add_argument('--inputs',default='recovered/inputs');p.add_argument('--out',default='q045_output')
    p.add_argument('--directory',default='collected');a=p.parse_args()
    if a.command=='static':static();return 0
    if a.command=='prepare':return prepare(a.out)
    if a.command=='collect':return int(collect(a.directory,a.out)['job_completeness_gate']!='PASS')
    if not a.arm or not a.model:p.error('--arm and --model required')
    return (worker if a.command=='worker' else run)(a.arm,a.model,a.inputs,a.out)

if __name__=='__main__':sys.exit(main())
