#!/usr/bin/env python3
"""One diagnostic branch: complete serial publication, interrupt, genuine resume.

No production fan-out, optimizer starts, CLASS replay or workflow dispatch.
The existing V21 retrieval/runtime helpers are reused only after their hash gate.
"""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, os, shutil, signal
import struct, subprocess, sys, time
from pathlib import Path
from q042_patch_durable_v22 import apply, fields
from q042_durable_selftest_v22 import selftest

Q='Q-042';PROGRAM_ID='Q042-DURABLE-V22'
REUSED_SHA='c7a253a8a8d9965e7f9857b9124674d5dfb23b56ea604916e2943f4d5d88dd10'

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=Path(str(path)+'.tmp');temp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');temp.replace(path)

def envelope(**kw):
    return dict(q=Q,case_id='NOT DOCUMENTED',program_id=PROGRAM_ID,
        execution_commit=os.environ.get('GITHUB_SHA','NOT DOCUMENTED'),
        github_run_id=os.environ.get('GITHUB_RUN_ID','NOT DOCUMENTED'),
        scientific_result=False,production_restart_authorized=False,**kw)

def config(path):
    c=json.loads(Path(path).read_text())
    if (c['q'],c['program_id'],c['probe_seconds'],c['maximum_probe_count'],c['new_bobyqa_starts'],c['production_restart_authorized'])!=(Q,PROGRAM_ID,14400,1,0,False):
        raise ValueError('DURABLE_CONTRACT_GATE=FAIL')
    c['_path']=str(Path(path).resolve());return c

def reused():
    path=Path(__file__).with_name('q042_stock_diagnostic_v21.py')
    if sha(path)!=REUSED_SHA:raise ValueError('REUSED_V21_HELPER_HASH_GATE=FAIL')
    spec=importlib.util.spec_from_file_location('q042_reused_v21',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.PROGRAM_ID=PROGRAM_ID
    return module

def inspect_binary(path,context=None):
    """Validate every native-ABI field, bounds and footer before using a state.

    The ABI is deliberately restricted to little-endian GNU Fortran on x86_64.
    This reader is independent of the Fortran restore; the restore also checks.
    """
    path=Path(path);data=path.read_bytes()
    if sys.byteorder!='little' or len(data)<120 or len(data)>2*1024**3:raise ValueError('BINARY_SIZE_ABI_GATE=FAIL')
    head=struct.unpack_from('<11i',data);ctx=data[44:108].decode('ascii')
    if head[0:2]!=(10422222,1) or len(ctx)!=64 or any(x not in '0123456789abcdef' for x in ctx):raise ValueError('BINARY_HEADER_GATE=FAIL')
    if context and ctx!=context:raise ValueError('BINARY_CONTEXT_GATE=FAIL')
    if not(0<head[7]<=100 and 0<head[10]<=1000):raise ValueError('BINARY_GRADES_RNG_GATE=FAIL')
    offset=108+4*(head[7]+head[10]);values={}
    schema=json.loads(Path(__file__).with_name('q042_durable_contract_v22.json').read_text())['rti_schema']
    for name,kind,rank in schema:
        width=4 if kind=='i' else 8
        if rank:
            allocated=struct.unpack_from('<i',data,offset)[0];offset+=4
            if allocated not in (0,1):raise ValueError('BINARY_ALLOCATION_GATE=FAIL')
            if not allocated:values[name]=None;continue
            dims=struct.unpack_from('<'+'i'*rank,data,offset);offset+=4*rank
            count=1
            for dim in dims:
                if dim<0 or dim>100000000:raise ValueError('BINARY_SHAPE_GATE=FAIL')
                count*=dim
            if count>500000000 or offset+count*width>len(data)-4:raise ValueError('BINARY_ARRAY_EXTENT_GATE=FAIL')
            values[name]={'shape':list(dims),'elements':count}
            offset+=count*width
        else:
            values[name]=struct.unpack_from('<i' if kind=='i' else '<d',data,offset)[0];offset+=width
    if offset+4!=len(data) or struct.unpack_from('<i',data,offset)[0]!=10422223:raise ValueError('BINARY_FOOTER_GATE=FAIL')
    if (values['ndead'],values['ncluster'])!=(head[5],head[6]):raise ValueError('BINARY_STATE_HEADER_GATE=FAIL')
    return {'ndead':head[5],'ndim':head[2],'nderived':head[3],'ncluster':head[6],
        'nlike_total':head[9],'rng_seed_size':head[10],'context':ctx,
        'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data),'fields':values}

def build(c,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    pc=Path('external/PolyChordLite').resolve()
    baseline=json.loads((out/'baseline_runtime.json').read_text());m=baseline['parent_manifest']
    for key in ('generate_file','nested_sampling_file','libchord_file'):
        if sha(m[key])!=m[key.replace('_file','_sha256')]:raise ValueError('BASELINE_BINARY_MANIFEST_GATE=FAIL')
    reference=out/'reference_polychord';shutil.copytree(pc,reference)
    patch=apply(pc,out/'q042_durable_patch_manifest_v22.json')
    for name in ('libchord.so','libchord.a'):(pc/'lib'/name).unlink(missing_ok=True)
    subprocess.run(['make','-C',str(pc/'src/polychord'),'clean'],check=True)
    subprocess.run(['make','-C',str(pc),'-e','libchord.so','MPI=1','COMPILER_TYPE=gnu'],check=True)
    # Fresh Python processes load the rebuilt library. No dependency versions change.
    subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--force-reinstall','--no-build-isolation','--no-deps',str(pc)],check=True)
    report=selftest(reference,pc,out/'compiled_reference')
    for scenario in report['scenarios']:
        inspect_binary(out/'compiled_reference'/scenario['name']/'chain.durable_v22')
    if sha(m['generate_file'])!=m['generate_sha256']:raise ValueError('UNCHANGED_V13_GENERATE_GATE=FAIL')
    save(out/'durable_runtime.json',envelope(status='PASS',patch=patch,
        libchord_sha256=sha(pc/'lib/libchord.so'),generate_sha256=sha(m['generate_file']),
        compiled_reference=report,compiler=subprocess.check_output(['gfortran','--version'],text=True).splitlines()[0]))

def runtime_gate(c,out):
    module=reused();parent=module.parent_driver(c);out=Path(out)
    r=json.loads((out/'durable_runtime.json').read_text())
    baseline=json.loads((out/'baseline_runtime.json').read_text());m=baseline['parent_manifest']
    if r['status']!='PASS' or r['compiled_reference']['status']!='PASS':raise ValueError('COMPILED_REFERENCE_GATE=FAIL')
    if sha(m['generate_file'])!=r['generate_sha256'] or sha(m['nested_sampling_file'])!=r['patch']['after_sha256'] or sha(m['libchord_file'])!=r['libchord_sha256']:
        raise ValueError('DURABLE_BINARY_ROUTE_GATE=FAIL')
    parent.cobaya_partial_resume_adapter_runtime_gate()
    return parent

def worker(c,out):
    out=Path(out);parent=runtime_gate(c,out)
    prefix=(out/'isolated_cell/polychord/chain').resolve()
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
    info=copy.deepcopy(parent.v1.stored_info(prefix));sp=info['sampler']['polychord']
    if (int(sp['seed']),sp['nlive'],sp['num_repeats'])!=(421100,'25d','5d'):raise ValueError('STORED_SAMPLER_GATE=FAIL')
    if Path(sp['path']).resolve()!=Path('external/PolyChordLite').resolve() or Path(info['theory']['classy']['path']).resolve()!=Path('external/class_ede').resolve():raise ValueError('STORED_BINARY_ROUTE_GATE=FAIL')
    info['output']=str(prefix);info['force']=False;info['resume']=True
    from cobaya.run import run
    run(info,output=str(prefix),force=False,resume=True,stop_at_error=True)

def stop(proc):
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGKILL):
        if proc.poll() is not None:break
        try:os.killpg(proc.pid,sig)
        except ProcessLookupError:break
        try:proc.wait(timeout=10)
        except subprocess.TimeoutExpired:continue
    return proc.wait(timeout=5)

def phase(c,out,context,minimum_ndead,deadline,label,legacy=False):
    out=Path(out);checkpoint=out/'isolated_cell/polychord/chain_polychord_raw/chain.durable_v22'
    env=os.environ.copy();env['Q042_DURABLE_CONTEXT']=context
    env.pop('Q042_DURABLE_LEGACY',None)
    if legacy:env['Q042_DURABLE_LEGACY']='DIAGNOSTIC'
    cmd=[sys.executable,str(Path(__file__).resolve()),'worker','--config',c['_path'],'--out',str(out.resolve())]
    started=time.monotonic();reason='TIME_LIMIT';state=None
    with (out/(label+'.log')).open('wb') as log:
        proc=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:
            while time.monotonic()<deadline:
                if checkpoint.exists():
                    state=inspect_binary(checkpoint,context)
                    if (state['ndim'],state['nderived'])!=(18,17):raise ValueError('PILOT_DIMENSIONS_GATE=FAIL')
                    if state['ndead']>minimum_ndead:reason='COMPLETE_STATE_ADVANCED';break
                if proc.poll() is not None:reason='WORKER_EXIT';break
                time.sleep(1)
            stop(proc)
        finally:
            if proc.poll() is None:stop(proc)
    if checkpoint.exists():state=inspect_binary(checkpoint,context)
    return dict(reason=reason,returncode=proc.returncode,elapsed_seconds=time.monotonic()-started,
        minimum_ndead=minimum_ndead,checkpoint=state,log=label+'.log',legacy_import=legacy)

def pilot(c,out):
    out=Path(out);runtime_gate(c,out);module=reused();source=Path('diag_inputs/ede')
    record=json.loads((source/'q042_production_polychord_final_v18.json').read_text())
    if (record['q'],record['program_id'],record['arm'],record['model'],record['combination'],record['seed'],record['segment'])!=(Q,'Q042-PROD-V18','camspec','ede_n3','FULL',421100,7):raise ValueError('SOURCE_CELL_GATE=FAIL')
    original=source/'cell_state/polychord/chain_polychord_raw/chain.resume'
    if sha(original)!=c['legacy_resume_sha256'] or sha(original)!=record['checkpoint_after']['primary_resume_sha256']:raise ValueError('SOURCE_CHECKPOINT_GATE=FAIL')
    if list((source/'cell_state').rglob('*.durable_v22')):raise ValueError('LEGACY_IMPORT_EXPECTATION_GATE=FAIL')
    job_start=os.environ.get('DIAG_JOB_START_UNIX')
    if not job_start or time.time()-float(job_start)>330*60-c['probe_seconds']-600:raise ValueError('REMAINING_JOB_BUDGET_GATE=FAIL no pilot started')
    shutil.copytree(source/'cell_state',out/'isolated_cell')
    before=module.snapshot(original);runtime=json.loads((out/'durable_runtime.json').read_text())
    provenance=envelope(contract_sha256=sha(c['_path']),scientific_spec_sha256=c['frozen_files']['q042_production_spec_v1.json'],
        source_commit=c['source_commit'],source_artifact=c['artifacts']['ede'],parent_resume=before,
        stored_info_sha256=sha(source/'cell_state/polychord/chain.updated.yaml'),
        compiler=runtime['compiler'],libchord_sha256=runtime['libchord_sha256'],
        polychord_commit=c['polychord_commit'],class_commit=c['class_commit'],
        parent_run_id=36979159417,parent_segment=7,diagnostic_segment=9,
        previous_diagnostic_run_id=37196661426,previous_diagnostic_seconds=14409.634021145,
        branch='DIAGNOSTIC_LEGACY_IMPORT_WITH_UNKNOWN_HISTORICAL_RNG_AND_STACK',
        historical_trajectory_reconstructed=False,original_48_segment_budget_reset=False)
    context=hashlib.sha256(json.dumps(provenance,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    save(out/'checkpoint_context.json',dict(provenance,context_sha256=context))
    started=time.monotonic();deadline=started+c['probe_seconds']
    first=phase(c,out,context,before['ndead'],min(deadline,started+c['first_phase_seconds']),'first',legacy=True)
    second=None;accepted=False
    cp=out/'isolated_cell/polychord/chain_polychord_raw/chain.durable_v22'
    if first['reason']=='COMPLETE_STATE_ADVANCED' and first['checkpoint']['ndead']>before['ndead'] and time.monotonic()<deadline-60:
        if sha(cp)!=first['checkpoint']['sha256']:raise ValueError('PARENT_CHECKPOINT_HASH_GATE=FAIL')
        shutil.copy2(cp,out/'first_complete.durable_v22')
        save(out/'first_checkpoint_lineage.json',envelope(parent=before,current=first['checkpoint'],context=context))
        second=phase(c,out,context,first['checkpoint']['ndead'],deadline,'second')
        log=(out/'second.log').read_text(errors='replace')
        import re
        restored=[int(x) for x in re.findall(r'Q042_DURABLE_RESTORE\s+(\d+)',log)]
        accepted=second['reason']=='COMPLETE_STATE_ADVANCED' and restored==[first['checkpoint']['ndead']] and 'Q042_LEGACY_DIAGNOSTIC_ONLY' not in log
        second['restored_ndead']=restored
        second['parent_checkpoint_sha256']=first['checkpoint']['sha256']
        if cp.exists():shutil.copy2(cp,out/'second_complete.durable_v22')
    result=envelope(execution_status='DIAGNOSTIC_COMPLETE' if accepted else 'DIAGNOSTIC_INCOMPLETE',
        technical_gate='PASS' if accepted else 'FAIL',final_result_gate='UNRESOLVED',
        initial=before,first=first,second=second,context=context,
        elapsed_seconds=time.monotonic()-started,soft_seconds=c['probe_seconds'],
        source_checkpoint_unchanged=sha(original)==before['sha256'],new_bobyqa_starts=0,
        class_blocker_resolved=False,historical_trajectory_reconstructed=False,
        next_motor='BUBBLEVERSE — RESULT INGESTION & ROUTING ENGINE')
    save(out/'q042_durable_pilot_v22.json',result)
    if not accepted:raise ValueError('DURABLE_PILOT_GATE=FAIL see preserved diagnostic record; no retry')

def collect(out):
    matches=list(Path('collected').rglob('q042_durable_pilot_v22.json'))
    records=[json.loads(p.read_text()) for p in matches]
    valid=len(records)==1 and records[0].get('q')==Q and records[0].get('program_id')==PROGRAM_ID and records[0].get('technical_gate')=='PASS' and records[0].get('github_run_id')==os.environ.get('GITHUB_RUN_ID') and records[0].get('execution_commit')==os.environ.get('GITHUB_SHA') and records[0].get('scientific_result') is False and records[0].get('production_restart_authorized') is False
    save(out,envelope(execution_status='DIAGNOSTIC_COMPLETE' if valid else 'DIAGNOSTIC_INCOMPLETE',
        job_completeness_gate='PASS' if valid else 'FAIL',technical_gate='PASS' if valid else 'FAIL',
        final_result_gate='UNRESOLVED',class_blocker_resolved=False,new_bobyqa_starts=0,
        results=records,next_motor='BUBBLEVERSE — RESULT INGESTION & ROUTING ENGINE',
        next_action='Ingest the finite repair result; no automatic pilot retry or production restart'))
    if not valid:raise ValueError('DIAGNOSTIC_COMPLETENESS_GATE=FAIL final failure record preserved')

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['fetch','verify-runtime','build','pilot','worker','collect','inspect'])
    p.add_argument('--config',default=str(Path(__file__).with_name('q042_durable_contract_v22.json')))
    p.add_argument('--out',default='diag_results');p.add_argument('--key',choices=['ede','environment'])
    a=p.parse_args();c=config(a.config)
    if a.command=='fetch':reused().fetch_artifact(c,a.key,a.out);return
    if a.command=='collect':collect(a.out);return
    if a.command=='inspect':print(json.dumps(inspect_binary(a.out),indent=2));return
    Path(a.out).mkdir(parents=True,exist_ok=True)
    if a.command=='verify-runtime':reused().baseline_verify(c,Path(a.out)/'baseline_runtime.json');return
    {'build':build,'pilot':pilot,'worker':worker}[a.command](c,a.out)

if __name__=='__main__':main()
