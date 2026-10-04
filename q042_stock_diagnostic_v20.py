#!/usr/bin/env python3
"""Q042 bounded diagnostic. Production execution and automatic dispatch are absent.

Uses one isolated copy of the V18 CamSpec/EDE/FULL stock state, plus one
exact CLASS error-point replay. Observer output changes no sampler settings.
All scientific endpoints remain unavailable until the original full gates pass.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

Q='Q-042'
PROGRAM_ID='Q042-STOCKDIAG-V20'
START='! Q042_DIAGNOSTIC_V20_BEGIN'
END='! Q042_DIAGNOSTIC_V20_END'

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    def metadata(x):
        if isinstance(x,float) and math.isinf(x):return 'infinity' if x>0 else '-infinity'
        if isinstance(x,dict):return {k:metadata(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [metadata(v) for v in x]
        return x
    tmp.write_text(json.dumps(metadata(data),indent=2,sort_keys=True,allow_nan=False)+'\n')
    tmp.replace(path)

def envelope(**kw):
    return dict(q=Q,case_id='NOT DOCUMENTED',program_id=PROGRAM_ID,
                github_run_id=os.environ.get('GITHUB_RUN_ID','NOT DOCUMENTED'),
                execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),
                scientific_result=False,production_restart_authorized=False,**kw)

def load_config(path):
    c=json.loads(Path(path).read_text())
    if c['q']!=Q or c['program_id']!=PROGRAM_ID or c['probe_seconds']!=14400 or c['class_seconds']!=900:
        raise ValueError('DIAGNOSTIC_CONTRACT_GATE=FAIL')
    if c['source_commit']!='d0f92c7f2ce53da32818244f8847f8e745e20c4f':
        raise ValueError('SOURCE_COMMIT_GATE=FAIL')
    return c

def stock_header(text):
    lines=text.splitlines();fields={}
    for i,line in enumerate(lines[:-1]):
        if line.startswith('==='):
            next_line=lines[i+1].strip()
            if next_line and not next_line.startswith(('===','---')):
                fields[line.strip('= ')]=next_line
    names={'ndim':'Number of dimensions','nderived':'Number of derived parameters',
           'ndead':'Number of dead points/iterations','ncluster':'Number of clusters'}
    out={k:int(fields[v]) for k,v in names.items() if v in fields}
    for k,v in [('nlive','Number of live points in each cluster'),('nlike','Number of likelihood calls'),
                ('repeats','Number of repeats'),('grade_dims','positions of grades')]:
        if v in fields:out[k]=[int(x) for x in fields[v].split()]
    for k,v in [('logx','local volume -- log(<X_p>)'),('logx_last_update','last update volume')]:
        if v in fields:out[k]=[float(x.replace('D','E')) for x in fields[v].split()]
    if 'ndead' not in out:raise ValueError('STOCK_HEADER_GATE=FAIL')
    return out

def snapshot(path):
    p=Path(path)
    return dict(stock_header(p.read_text()),sha256=sha(p),size=p.stat().st_size)

def extract_verified(path,digest,dest):
    path=Path(path);dest=Path(dest)
    if sha(path)!=digest:raise ValueError('ARTIFACT_SHA256_GATE=FAIL')
    with zipfile.ZipFile(path) as z:
        names=set();total=0
        for item in z.infolist():
            p=PurePosixPath(item.filename);mode=item.external_attr>>16
            if p.is_absolute() or '..' in p.parts or '\\' in item.filename or str(p) in names or stat.S_ISLNK(mode):
                raise ValueError('ARTIFACT_MEMBER_GATE=FAIL')
            names.add(str(p));total+=item.file_size
            if total>3*1024**3:raise ValueError('ARTIFACT_SIZE_GATE=FAIL')
        if dest.exists():raise ValueError('ARTIFACT_DESTINATION_ALREADY_EXISTS')
        dest.mkdir(parents=True)
        z.extractall(dest)

def fetch_artifact(c,key,dest):
    a=c['artifacts'][key];base=f"https://api.github.com/repos/{c['repository']}/actions/artifacts/{a['id']}"
    token=os.environ.get('GH_TOKEN','')
    headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    if token:headers['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request(base,headers=headers),timeout=60) as r:meta=json.load(r)
    wr=meta['workflow_run']
    if meta['expired'] or meta['name']!=a['name'] or meta['digest']!='sha256:'+a['sha256'] or wr['id']!=a['run_id'] or wr['head_sha']!=c['source_commit']:
        raise ValueError('ARTIFACT_PROVENANCE_GATE=FAIL')
    # gh follows GitHub's redirect without forwarding the bearer token to storage.
    archive=Path(str(dest)+'.zip')
    with archive.open('wb') as f:
        subprocess.run(['gh','api',base+'/zip'],stdout=f,check=True,timeout=1200)
    extract_verified(archive,a['sha256'],dest)
    write_json(Path(dest)/'diagnostic_import.json',envelope(source_artifact=meta,zip_sha256=sha(archive)))

def remove_observer(text):
    return re.sub(r'^[ \t]*'+re.escape(START)+r'\n.*?^[ \t]*'+re.escape(END)+r'\n','',text,flags=re.M|re.S)

def observer_source(text):
    if START in text:
        baseline=remove_observer(text)
        if observer_source(baseline)!=text:raise ValueError('OBSERVER_DRIFT_GATE=FAIL')
        return text
    if len(re.findall(r'^                    if\(replace_point\(settings,RTI,baby_points,cluster_id\)\) then$',text,flags=re.M))!=1:
        raise ValueError('OBSERVER_REPLACEMENT_BOUNDARY_GATE=FAIL')
    inserts=[
      ('        logical :: update\n','        real(dp) :: q042_diag_cpu\n'),
      ('                seed_point = GenerateSeed(settings,RTI,cluster_id)\n',
       "                call cpu_time(q042_diag_cpu)\n                write(*,*) 'Q042_DIAG_BEGIN', RTI%ndead, q042_diag_cpu\n                flush(6)\n"),
      ('                    baby_points = SliceSampling(loglikelihood,prior,settings,logL,seed_point,cholesky,nlike,num_repeats)\n',
       "                    call cpu_time(q042_diag_cpu)\n                    write(*,*) 'Q042_DIAG_SLICE_END', RTI%ndead, q042_diag_cpu, nlike\n                    flush(6)\n"),
      ('                        failures = 0\n',
       "                        call cpu_time(q042_diag_cpu)\n                        write(*,*) 'Q042_DIAG_REPLACE', RTI%ndead, q042_diag_cpu\n                        flush(6)\n"),
    ]
    out=text
    for anchor,addition in inserts:
        pattern='^'+re.escape(anchor)
        if len(re.findall(pattern,out,flags=re.M))!=1:raise ValueError('OBSERVER_ANCHOR_GATE=FAIL '+anchor.strip())
        block='        '+START+'\n'+addition+'        '+END+'\n'
        out=re.sub(pattern,lambda m:anchor+block,out,flags=re.M)
    if remove_observer(out)!=text:raise ValueError('OBSERVER_REMOVAL_GATE=FAIL')
    return out

def diagnose(before,after,log):
    completed=[int(x) for x in re.findall(r'Q042_DIAG_REPLACE\s+(\d+)',log)]
    if after['ndead']>before['ndead'] and after['sha256']!=before['sha256']:
        status='DURABLE_PROGRESS_OBSERVED'
    elif any(n>before['ndead'] for n in completed):status='IN_MEMORY_PROGRESS_WITHOUT_DURABLE_UPDATE'
    else:status='NO_COMPLETE_REPLACEMENT_OBSERVED'
    return envelope(diagnosis=status,before=before,after=after,
                    observed_replacement_count=len(completed),
                    maximum_observed_ndead=max(completed,default=before['ndead']),
                    next_action='RETURN_FOR_RECOVERY_OR_STOP_DECISION',
                    final_result_gate='UNRESOLVED')

def supervise(cmd,log,seconds,grace=30):
    start=time.monotonic();timed_out=False
    with Path(log).open('w') as f:
        p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
        try:p.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            timed_out=True
            for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGKILL):
                try:os.killpg(p.pid,sig)
                except ProcessLookupError:break
                try:p.wait(timeout=grace);break
                except subprocess.TimeoutExpired:continue
            p.wait()
    return dict(returncode=p.returncode,timed_out=timed_out,elapsed_seconds=time.monotonic()-start,
                command=cmd,soft_seconds=seconds)

def parent_driver(c):
    if subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()!=c['source_commit']:
        raise ValueError('FROZEN_CHECKOUT_GATE=FAIL')
    for p,h in c['frozen_files'].items():
        if sha(p)!=h:raise ValueError('FROZEN_FILE_GATE=FAIL '+p)
    sys.path.insert(0,str(Path.cwd()))
    import q042_production_v18 as parent
    parent.load_spec('q042_production_spec_v1.json')
    parent.load_lock('q042_production_source_lock_v18.json','q042_production_spec_v1.json')
    return parent

def baseline_verify(c,out):
    p=parent_driver(c)
    r=p.runtime_gate('q042_runtime/q042_external_runtime_provenance_prod_v1.json')
    inherited=json.loads(Path('env_bundle/q042_runtime/q042_external_runtime_provenance_prod_v1.json').read_text())
    for key in ('cobaya_version','pybobyqa_version','numpy_version','polychord_commit','pantheonplus_manifest_sha256'):
        if r.get(key)!=inherited.get(key):raise ValueError('INHERITED_RUNTIME_EQUIVALENCE_GATE=FAIL '+key)
    if sha('env_bundle/q042_production_spec_v1.json')!=c['frozen_files']['q042_production_spec_v1.json']:
        raise ValueError('ENVIRONMENT_SCIENTIFIC_SPEC_GATE=FAIL')
    pc=Path('external/PolyChordLite')
    if subprocess.check_output(['git','-C',str(pc),'rev-parse','HEAD'],text=True).strip()!=c['polychord_commit']:
        raise ValueError('POLYCHORD_COMMIT_GATE=FAIL')
    record=envelope(status='PASS',source_commit=c['source_commit'],runtime=r,
                    inherited_runtime=inherited,python_version=sys.version,
                    cpu_count=os.cpu_count(),thread_environment={k:os.environ.get(k,'NOT DOCUMENTED') for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS')},
                    parent_manifest=json.loads(Path('q042_runtime/q042_polychord_partial_init_v17.json').read_text()),
                    class_commit=subprocess.check_output(['git','-C','external/class_ede','rev-parse','HEAD'],text=True).strip())
    if record['class_commit']!=c['class_commit']:raise ValueError('CLASS_COMMIT_GATE=FAIL')
    write_json(out,record)

def gaussian_worker(out):
    import numpy as np
    import pypolychord
    from pypolychord.settings import PolyChordSettings
    def like(x):return -0.5*float(np.dot(x,x)),[]
    def prior(cube):return 10*np.asarray(cube)-5
    settings=PolyChordSettings(2,0,nlive=20,num_repeats=10,nprior=40,
       precision_criterion=0.1,seed=421999,base_dir=str(Path(out).resolve()),file_root='chain',
       read_resume=False,write_resume=True,feedback=0)
    pypolychord.run_polychord(like,2,0,settings,prior)

def instrument(c,out):
    out=Path(out);baseline=json.loads((out/'baseline_runtime.json').read_text())
    manifest=baseline['parent_manifest']
    source=Path(manifest['nested_sampling_file']);lib=Path(manifest['libchord_file'])
    for key in ('generate_file','nested_sampling_file','libchord_file'):
        if sha(manifest[key])!=manifest[key.replace('_file','_sha256')]:raise ValueError('BASELINE_MANIFEST_GATE=FAIL')
    s=source.read_text();patched=observer_source(s)
    baseline_run=supervise([sys.executable,str(Path(__file__).resolve()),'gaussian-worker','--out',str(out/'gaussian_baseline')],out/'gaussian_baseline.log',120)
    if baseline_run['returncode']!=0:raise ValueError('BASELINE_GAUSSIAN_GATE=FAIL')
    (out/'nested_sampling_before.F90').write_text(s)
    source.write_text(patched)
    pc=Path('external/PolyChordLite').resolve()
    for name in ('libchord.so','libchord.a'):(pc/'lib'/name).unlink(missing_ok=True)
    subprocess.run(['make','-C',str(pc/'src/polychord'),'clean'],check=True)
    subprocess.run(['make','-C',str(pc),'-e','libchord.so','MPI=1'],check=True)
    subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--force-reinstall','--no-build-isolation','--no-deps',str(pc)],check=True)
    observed_run=supervise([sys.executable,str(Path(__file__).resolve()),'gaussian-worker','--out',str(out/'gaussian_observer')],out/'gaussian_observer.log',120)
    b=out/'gaussian_baseline/chain.resume';a=out/'gaussian_observer/chain.resume'
    if observed_run['returncode']!=0 or not a.exists() or sha(a)!=sha(b):raise ValueError('OBSERVER_GAUSSIAN_BYTE_IDENTITY_GATE=FAIL')
    if 'Q042_DIAG_REPLACE' not in (out/'gaussian_observer.log').read_text():raise ValueError('OBSERVER_LINK_GATE=FAIL')
    write_json(out/'observer_runtime.json',envelope(status='PASS',baseline_manifest=manifest,
       nested_source_sha256=sha(source),observer_lib_sha256=sha(lib),
       gaussian_resume_sha256=sha(a),gaussian_exact_byte_identity=True,
       source_removal_exact_identity=(remove_observer(patched)==s),
       production_checkpoint_format_changed=False,production_settings_changed=False))

def observer_gate(c,out):
    parent=parent_driver(c);out=Path(out)
    baseline=json.loads((out/'baseline_runtime.json').read_text())
    observed=json.loads((out/'observer_runtime.json').read_text())
    m=baseline['parent_manifest'];s=Path(m['nested_sampling_file']).read_text()
    if observed['status']!='PASS' or not observed['gaussian_exact_byte_identity']:
        raise ValueError('OBSERVER_SELFTEST_GATE=FAIL')
    if sha(m['nested_sampling_file'])!=observed['nested_source_sha256'] or sha(m['libchord_file'])!=observed['observer_lib_sha256']:
        raise ValueError('OBSERVER_BINARY_GATE=FAIL')
    if hashlib.sha256(remove_observer(s).encode()).hexdigest()!=m['nested_sampling_sha256']:
        raise ValueError('OBSERVER_SOURCE_EQUIVALENCE_GATE=FAIL')
    if sha(m['generate_file'])!=m['generate_sha256']:raise ValueError('UNCHANGED_PARTIAL_INIT_GATE=FAIL')
    parent.cobaya_partial_resume_adapter_runtime_gate()
    return parent

def probe_worker(c,out):
    out=Path(out);parent=observer_gate(c,out)
    prefix=(out/'isolated_cell/polychord/chain').resolve()
    # V18 constructs the frozen likelihood context before reading stored info.
    # Keep this order so dynamically registered Q032 likelihoods/pickle references exist.
    args=argparse.Namespace(q032_parent_root='q032_parent',
       preflight='env_bundle/q032_preflight/q032_preflight_sealed_v2.json',
       parent_dir='env_bundle/q032_parent_profiles',
       hlp_matrix='env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.npy',
       hlp_meta='env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.json',
       reduced_support='env_bundle/q042_environment/q042_primary_nonoverlap_support_prod_v18.json',
       reduced_hlp_matrix='env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.npy',
       reduced_hlp_meta='env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.json',
       spec='q042_production_spec_v1.json',source_lock='q042_production_source_lock_v18.json',
       external_runtime='q042_runtime/q042_external_runtime_provenance_prod_v1.json')
    parent.v1.build_info(args,'camspec','ede_n3','FULL',prefix)
    # Same stored-info route used by V18; input ZIP and all member bytes are verified.
    info=copy.deepcopy(parent.v1.stored_info(prefix))
    sp=info['sampler']['polychord']
    if int(sp['seed'])!=421100 or sp['nlive']!='25d' or sp['num_repeats']!='5d':
        raise ValueError('STORED_SAMPLER_CONTRACT_GATE=FAIL')
    if Path(sp['path']).resolve()!=Path('external/PolyChordLite').resolve() or Path(info['theory']['classy']['path']).resolve()!=Path('external/class_ede').resolve():
        raise ValueError('STORED_BINARY_ROUTING_GATE=FAIL')
    info['output']=str(prefix);info['force']=False;info['resume']=True
    from cobaya.run import run
    run(info,output=str(prefix),force=False,resume=True,stop_at_error=True)

def probe(c,out):
    out=Path(out);source=Path('diag_inputs/ede');record=json.loads((source/'q042_production_polychord_final_v18.json').read_text())
    if (record['q'],record['program_id'],record['arm'],record['model'],record['combination'],record['seed'],record['segment'])!=(Q,'Q042-PROD-V18','camspec','ede_n3','FULL',421100,7):
        raise ValueError('PROBE_CELL_IDENTITY_GATE=FAIL')
    if sha(source/'cell_state/polychord/chain_polychord_raw/chain.resume')!=record['checkpoint_after']['primary_resume_sha256']:
        raise ValueError('PROBE_CHECKPOINT_LINK_GATE=FAIL')
    job_start=os.environ.get('DIAG_JOB_START_UNIX')
    if job_start and time.time()-float(job_start)>330*60-c['probe_seconds']-600:
        raise ValueError('HPC_REMAINING_JOB_BUDGET_GATE=FAIL no probe started')
    shutil.copytree(source/'cell_state',out/'isolated_cell')
    path=out/'isolated_cell/polychord/chain_polychord_raw/chain.resume'
    before=snapshot(path);write_json(out/'probe_before.json',envelope(**before))
    run=supervise([sys.executable,str(Path(__file__).resolve()),'probe-worker','--config',str(Path(c['_path']).resolve()),'--out',str(out.resolve())],out/'probe_worker.log',c['probe_seconds'])
    after=snapshot(path);result=diagnose(before,after,(out/'probe_worker.log').read_text(errors='replace'))
    entered='Q042_DIAG_BEGIN' in (out/'probe_worker.log').read_text(errors='replace')
    result['runtime_entry_gate']='PASS' if entered else 'FAIL'
    if not entered:result['diagnosis']='PROBE_DID_NOT_ENTER_SAMPLER'
    result.update(worker=run,parent_segment=7,diagnostic_segment=8,parent_run_id=36979159417,
                  accounting='One diagnostic branch; no reset of original 48-segment production budget',
                  observer_selftest=json.loads((out/'observer_runtime.json').read_text()))
    write_json(out/'q042_stock_probe_v20.json',result)
    if not entered:
        raise ValueError('PROBE_RUNTIME_ENTRY_GATE=FAIL')

def class_worker(c,out):
    from cobaya.component import load_external_module
    from cobaya.theories.classy.classy import classy as wrapper
    class_root=Path('external/class_ede').resolve()
    classy=load_external_module('classy',path=str(class_root),min_version=None,get_import_path=wrapper.get_import_path_old)
    if not Path(classy.__file__).resolve().is_relative_to(class_root):
        raise ValueError('CLASS_BINARY_ROUTING_GATE=FAIL')
    model=classy.Class();params=copy.deepcopy(c['class_failure_point'])
    result=envelope(parameters=params,classy_file=classy.__file__,class_binary_sha256=sha(classy.__file__),classy_version=getattr(classy,'__version__','NOT DOCUMENTED'))
    write_json(Path(out)/'class_point_started.json',result)
    start=time.monotonic()
    try:
        model.set(params);model.compute();result['point_result']='FINITE_COMPUTE_RETURN'
    except Exception as exc:
        result.update(point_result='CLASS_EXCEPTION',exception_type=type(exc).__name__,exception=str(exc))
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        write_json(Path(out)/'class_point_raw.json',result)
        try:model.struct_cleanup();model.empty()
        except Exception:pass

def replay_class(c,out):
    out=Path(out);baseline_verify(c,out/'baseline_runtime.json')
    run=supervise([sys.executable,str(Path(__file__).resolve()),'class-worker','--config',str(Path(c['_path']).resolve()),'--out',str(out.resolve())],out/'class_worker.log',c['class_seconds'])
    p=out/'class_point_raw.json'
    raw=json.loads(p.read_text()) if p.exists() else envelope(point_result='NO_COMPUTE_RETURN')
    write_json(out/'q042_class_replay_v20.json',envelope(worker=run,raw_result=raw,
       runtime_entry_gate='PASS' if (out/'class_point_started.json').exists() else 'FAIL',
       diagnosis='TIME_LIMIT' if run['timed_out'] else raw['point_result'],
       final_result_gate='UNRESOLVED',precision_changed=False,stop_at_error_policy_changed=False))
    if run['returncode']!=0 and not run['timed_out']:raise ValueError('CLASS_REPLAY_RUNTIME_GATE=FAIL')

def inspect(c,out):
    import yaml
    rows=[]
    for key,model,seed,nlive,segment in [('ede','ede_n3',421100,450,7),('lcdm','lcdm',421000,375,3)]:
        p=Path('diag_inputs')/key
        record=json.loads((p/'q042_production_polychord_final_v18.json').read_text())
        info=yaml.safe_load((p/'cell_state/polychord/chain.updated.yaml').read_text())
        state=snapshot(p/'cell_state/polychord/chain_polychord_raw/chain.resume')
        if (record['q'],record['program_id'],record['arm'],record['model'],record['combination'],record['segment'],record['seed'])!=(Q,'Q042-PROD-V18','camspec',model,'FULL',segment,seed):raise ValueError('SOURCE_CELL_GATE=FAIL')
        if info['sampler']['polychord']['seed']!=seed or sum(state['nlive'])!=nlive:raise ValueError('STATE_CONFIG_GATE=FAIL')
        if state['sha256']!=record['checkpoint_after']['primary_resume_sha256'] or record['scientific_spec_sha256']!=c['frozen_files']['q042_production_spec_v1.json']:
            raise ValueError('SOURCE_STATE_HASH_LINK_GATE=FAIL')
        rows.append(dict(key=key,state=state,source_record=record,sampler=info['sampler']['polychord']))
    write_json(out,envelope(status='PASS',rows=rows,actual_likelihood_replay=False))

def collect(out):
    out=Path(out);records={};missing=[]
    for name in ('q042_stock_probe_v20.json','q042_class_replay_v20.json'):
        matches=list(Path('collected').rglob(name))
        if len(matches)!=1:missing.append(name);continue
        r=json.loads(matches[0].read_text())
        if r.get('q')!=Q or r.get('program_id')!=PROGRAM_ID or r.get('scientific_result') is not False:
            raise ValueError('DIAGNOSTIC_MERGE_IDENTITY_GATE=FAIL')
        records[name]=r
    valid=not missing and all(r.get('runtime_entry_gate')=='PASS' for r in records.values())
    write_json(out,envelope(execution_status='DIAGNOSTIC_COMPLETE' if valid else 'DIAGNOSTIC_INCOMPLETE',
        final_result_gate='UNRESOLVED',missing_results=missing,results=records,
        job_completeness_gate='FAIL' if missing else 'PASS',
        mandatory_runtime_entry_gate='PASS' if valid else 'FAIL',
        next_motor='BUBBLEVERSE — RESULT INGESTION & ROUTING ENGINE',
        next_action='Decide recovery or documented execution stop from observed progress and CLASS replay; no automatic continuation'))

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['fetch','inspect','verify-runtime','instrument','probe','probe-worker','replay-class','class-worker','gaussian-worker','collect'])
    p.add_argument('--config',default=str(Path(__file__).with_name('q042_stock_diagnostic_contract_v20.json')))
    p.add_argument('--out',default='diag_results');p.add_argument('--key',choices=['ede','lcdm','environment'])
    a=p.parse_args()
    if a.command=='gaussian-worker':gaussian_worker(a.out);return
    c=load_config(a.config);c['_path']=a.config
    if a.command=='fetch':fetch_artifact(c,a.key,a.out);return
    if a.command=='inspect':inspect(c,a.out);return
    if a.command=='collect':collect(a.out);return
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    functions={'verify-runtime':lambda:baseline_verify(c,out/'baseline_runtime.json'),
               'instrument':lambda:instrument(c,out),'probe':lambda:probe(c,out),
               'probe-worker':lambda:probe_worker(c,out),'replay-class':lambda:replay_class(c,out),
               'class-worker':lambda:class_worker(c,out)}
    functions[a.command]()

if __name__=='__main__':main()
