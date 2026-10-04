#!/usr/bin/env python3
"""Finite compiled PolyChord stock-loop interruption/resume regression test.

The Fortran likelihood is deterministic. The test-only libc rename interposer
freezes a worker exactly before or after atomic checkpoint publication. No
fault-injection code is installed in the production sampler.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, signal, struct, subprocess, time
from pathlib import Path

DRIVER = r'''
program q042_reference
    use utils_module, only: dp
    use settings_module, only: program_settings
    use interfaces_module, only: run_polychord
    implicit none
    type(program_settings) :: s
    character(1000) :: directory
    integer :: lu
    call get_command_argument(1,directory)
    s%nDims=2
    s%nDerived=1
    s%nlive=20
    s%nprior=40
    s%num_repeats=4
    s%seed=421999
    s%max_ndead=100
    s%precision_criterion=0d0
    s%compression_factor=exp(-1d0)
    s%do_clustering=.true.
    s%posteriors=.true.
    s%cluster_posteriors=.true.
    s%equals=.true.
    s%read_resume=.true.
    s%write_resume=.true.
    s%write_dead=.true.
    s%write_stats=.true.
    s%write_live=.true.
    s%feedback=0
    s%base_dir=trim(directory)
    s%file_root='chain'
    allocate(s%grade_dims(2),s%grade_frac(2))
    s%grade_dims=[1,1]
    ! Explicit repeat counts isolate checkpointing from speed auto-calibration.
    s%grade_frac=[4d0,8d0]
    open(newunit=lu,file=trim(directory)//'/likelihood_trace.txt',status='replace')
    call run_polychord(likelihood,prior_transform,s)
    close(lu)
contains
    function prior_transform(cube) result(theta)
        real(dp), intent(in) :: cube(:)
        real(dp) :: theta(size(cube))
        theta=10d0*cube-5d0
    end function
    function likelihood(theta,phi) result(loglike)
        real(dp), intent(in) :: theta(:)
        real(dp), intent(out) :: phi(:)
        real(dp) :: loglike
        loglike=-0.5d0*sum(theta**2)
        phi(1)=sum(theta)
        write(lu,'(3ES26.17E3)') theta,loglike
        flush(lu)
    end function
end program
'''
INTERPOSER = r'''
#define _GNU_SOURCE
#include <dlfcn.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int rename(const char *oldpath, const char *newpath) {
    static int (*real_rename)(const char *, const char *) = NULL;
    if (!real_rename) real_rename=dlsym(RTLD_NEXT,"rename");
    const char *requested=getenv("Q042_TEST_NDEAD");
    const char *phase=getenv("Q042_TEST_PHASE");
    int32_t head[11]={0};
    int match=0;
    if (requested && phase && strstr(newpath,".durable_v22")) {
        FILE *f=fopen(oldpath,"rb");
        if (f) { if(fread(head,sizeof(int32_t),11,f)==11) match=head[0]==10422222 && head[5]==atoi(requested); fclose(f); }
    }
    if (match && strcmp(phase,"before")==0) {
        fprintf(stderr,"Q042_TEST_FROZEN_BEFORE %d\n",head[5]); fflush(stderr); raise(SIGSTOP);
    }
    int rc=real_rename(oldpath,newpath);
    if(match && rc==0 && strcmp(phase,"after")==0) {
        fprintf(stderr,"Q042_TEST_FROZEN_AFTER %d\n",head[5]); fflush(stderr); raise(SIGSTOP);
    }
    return rc;
}
'''

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,record):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')

def compile_driver(root,out):
    root=Path(root).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'reference.f90').write_text(DRIVER)
    fc=os.environ.get('FC','gfortran')
    subprocess.run([fc,'-ffree-line-length-none','-I'+str(root/'src/polychord'),str(out/'reference.f90'),'-L'+str(root/'lib'),'-lchord','-Wl,-rpath,'+str(root/'lib'),'-o',str(out/'reference')],check=True)
    (out/'rename_stop.c').write_text(INTERPOSER)
    subprocess.run([os.environ.get('CC','gcc'),'-shared','-fPIC',str(out/'rename_stop.c'),'-ldl','-o',str(out/'rename_stop.so')],check=True)
    return out/'reference',out/'rename_stop.so'

def environment(context=None):
    env=os.environ.copy()
    for name in ['Q042_DURABLE_CONTEXT','Q042_DURABLE_LEGACY','Q042_TEST_NDEAD','Q042_TEST_PHASE','LD_PRELOAD']:
        env.pop(name,None)
    if context:env['Q042_DURABLE_CONTEXT']=context
    return env

def run(exe,directory,env,timeout=60):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);(directory/'clusters').mkdir(exist_ok=True)
    with (directory/'worker.log').open('wb') as log:
        result=subprocess.run([str(exe),str(directory.resolve())],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
    if result.returncode: raise AssertionError(f'WORKER_GATE=FAIL rc={result.returncode}: '+(directory/'worker.log').read_text()[-2200:])

def header(path):
    with Path(path).open('rb') as file:
        words=struct.unpack('=11i',file.read(44));context=file.read(64).decode('ascii')
    if words[0]!=10422222 or words[1]!=1:raise AssertionError('DURABLE_MAGIC_VERSION_GATE=FAIL')
    return {'ndead':words[5],'ncluster':words[6],'nlike_total':words[9],'rng_seed_size':words[10],'context':context,'sha256':sha(path),'size_bytes':Path(path).stat().st_size}

def compare(reference,candidate):
    names=['chain.resume','chain_dead.txt','chain_dead-birth.txt','chain.txt','chain_equal_weights.txt']
    for name in names:
        a=Path(reference)/name;b=Path(candidate)/name
        if not a.exists() or not b.exists() or a.read_bytes()!=b.read_bytes():raise AssertionError('REFERENCE_BYTE_IDENTITY_GATE=FAIL '+name)
    return {name:sha(Path(candidate)/name) for name in names}

def capture(exe,preload,directory,context,ndead,phase):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);(directory/'clusters').mkdir(exist_ok=True)
    env=environment(context);env.update(LD_PRELOAD=str(preload),Q042_TEST_NDEAD=str(ndead),Q042_TEST_PHASE=phase)
    log=(directory/'capture.log').open('wb')
    proc=subprocess.Popen([str(exe),str(directory.resolve())],stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
    try:
        deadline=time.monotonic()+60
        marker='Q042_TEST_FROZEN_'+phase.upper()
        while time.monotonic()<deadline:
            if marker in (directory/'capture.log').read_text(errors='replace'):break
            if proc.poll() is not None:raise AssertionError('CAPTURE_GATE=FAIL process finished before chosen boundary')
            time.sleep(0.01)
        else:raise AssertionError('CAPTURE_GATE=FAIL deadline')
        published=directory/'chain.durable_v22'
        if not published.exists():raise AssertionError('DURABLE_CHECKPOINT_GATE=FAIL new complete-state file absent')
        state=header(published)
        expected=ndead if phase=='after' else ndead-1
        if state['ndead']!=expected:raise AssertionError('ATOMIC_PUBLISHED_BOUNDARY_GATE=FAIL')
        if phase=='before' and not Path(str(published)+'.tmp').exists():raise AssertionError('ATOMIC_TEMP_PRECONDITION_GATE=FAIL')
        os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
        return state,(directory/'likelihood_trace.txt').read_text().splitlines()[:state['nlike_total']]
    finally:
        if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
        log.close()

def selftest(reference_root,patched_root,out):
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    ref,_=compile_driver(reference_root,out/'reference_build')
    patched,preload=compile_driver(patched_root,out/'patched_build')
    context=hashlib.sha256(b'Q-042/Q042-DURABLE-V22/synthetic-v1').hexdigest()
    baseline=out/'stock_uninterrupted';unchanged=out/'patched_uninterrupted'
    run(ref,baseline,environment())
    run(patched,unchanged,environment(context))
    if not (unchanged/'chain.durable_v22').exists():
        raise AssertionError('DURABLE_CHECKPOINT_GATE=FAIL stock loop publishes no complete-state checkpoint')
    compare(baseline,unchanged)
    reference_trace=(baseline/'likelihood_trace.txt').read_text().splitlines()
    if reference_trace!=(unchanged/'likelihood_trace.txt').read_text().splitlines():raise AssertionError('OBSERVER_TRAJECTORY_GATE=FAIL')
    records=[]
    for name,ndead,phase in [('safe_after_update',45,'after'),('interrupted_before_publication',24,'before'),('interrupted_at_update',48,'before')]:
        directory=out/name
        saved,first=capture(patched,preload,directory,context,ndead,phase)
        run(patched,directory,environment(context))
        hashes=compare(baseline,directory)
        combined=first+(directory/'likelihood_trace.txt').read_text().splitlines()
        if combined!=reference_trace:raise AssertionError('RESUMED_LIKELIHOOD_TRAJECTORY_GATE=FAIL '+name)
        if 'Q042_DURABLE_RESTORE' not in (directory/'worker.log').read_text():raise AssertionError('GENUINE_RESTORE_ENTRY_GATE=FAIL')
        records.append({'name':name,'status':'PASS','captured':saved,'final_scientific_output_hashes':hashes,'likelihood_trajectory_exact_identity':True})
    rejection=[]
    for name in ['wrong_context','truncated_checkpoint','legacy_without_permission']:
        directory=out/name;shutil.copytree(unchanged,directory)
        checkpoint=directory/'chain.durable_v22';env=environment(context)
        if name=='wrong_context':env['Q042_DURABLE_CONTEXT']='0'*64
        elif name=='truncated_checkpoint':checkpoint.write_bytes(checkpoint.read_bytes()[:-11])
        else:checkpoint.unlink()
        with (directory/'rejection.log').open('wb') as log:
            result=subprocess.run([str(patched),str(directory)],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=60)
        if result.returncode==0:raise AssertionError('INCOMPATIBLE_STATE_REJECTION_GATE=FAIL '+name)
        if (directory/'likelihood_trace.txt').stat().st_size:raise AssertionError('REJECTION_BEFORE_LIKELIHOOD_GATE=FAIL '+name)
        rejection.append({'name':name,'status':'PASS','returncode':result.returncode})
    report={'q':'Q-042','program_id':'Q042-DURABLE-V22','status':'PASS','scientific_result':False,'production_restart_authorized':False,'serial_only':True,'uninterrupted_stock_vs_patched_byte_identity':True,'uninterrupted_trajectory_exact_identity':True,'scenarios':records,'fail_closed_tests':rejection,'compiler':subprocess.check_output([os.environ.get('FC','gfortran'),'--version'],text=True).splitlines()[0],'limitations':['Deterministic synthetic Fortran likelihood; frozen full Cobaya/CLASS runtime must be validated separately','No historical RNG reconstruction from legacy stock resume','No MPI multi-process continuation','Atomic process-interruption safety; no power-loss/fsync durability guarantee']}
    write_json(out/'q042_durable_selftest_v22.json',report)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--reference-root',required=True);ap.add_argument('--patched-root',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();print(json.dumps(selftest(a.reference_root,a.patched_root,a.out),indent=2))
