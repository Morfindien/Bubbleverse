#!/usr/bin/env python3
"""Fast technical self-test for Q042 V13 PolyChord partial-init checkpointing."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, signal, subprocess, sys, time
from pathlib import Path

SEED=314159
NPRIOR=100
NLIVE=10
CHECKPOINT_INTERVAL=25

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run_worker(base: Path, sleep_s: float):
    import numpy as np
    import pypolychord
    from pypolychord.settings import PolyChordSettings
    base.mkdir(parents=True,exist_ok=True)
    def prior(cube):
        return np.asarray(cube,dtype=float)
    def loglike(theta):
        time.sleep(sleep_s)
        x=np.asarray(theta,dtype=float)
        return -0.5*float(np.dot(x-0.37,x-0.37)), []
    settings=PolyChordSettings(
        2,0,base_dir=str(base),file_root="chain",
        nlive=NLIVE,nprior=NPRIOR,num_repeats=2,nfail=NLIVE,
        precision_criterion=0.2,max_ndead=30,do_clustering=False,
        read_resume=True,write_resume=True,write_live=True,write_dead=True,
        write_prior=True,write_stats=True,seed=SEED,feedback=0,
        grade_frac=[2.0],grade_dims=[2],synchronous=True,
    )
    pypolychord.run_polychord(loglike,2,0,settings,prior=prior)

def parse_meta(p: Path):
    d={}
    if not p.exists(): return d
    for line in p.read_text().splitlines():
        if "=" in line:
            k,v=line.split("=",1)
            try: d[k]=int(v)
            except Exception: d[k]=v
    return d

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--sleep",type=float,default=0.02)
    ap.add_argument("--output")
    a=ap.parse_args()
    if a.worker:
        run_worker(Path(a.base),a.sleep)
        return 0

    if not a.output:
        raise SystemExit("--output required")
    root=Path("q042_runtime/q042_partial_init_selftest_work")
    shutil.rmtree(root,ignore_errors=True)
    baseline=root/"baseline"
    segmented=root/"segmented"

    # Reference uninterrupted run.
    subprocess.run([sys.executable,__file__,"--worker","--base",str(baseline),"--sleep","0.0"],check=True)

    # Start slow run and interrupt immediately after a genuine partial checkpoint appears.
    proc=subprocess.Popen([sys.executable,__file__,"--worker","--base",str(segmented),"--sleep","0.05"])
    meta=segmented/"chain.partial_init.meta"
    deadline=time.time()+60
    observed=None
    while time.time()<deadline:
        observed=parse_meta(meta)
        if int(observed.get("accepted",0)) >= CHECKPOINT_INTERVAL:
            break
        if proc.poll() is not None:
            raise SystemExit("PARTIAL_INIT_SELFTEST_EARLY_EXIT_GATE=FAIL")
        time.sleep(0.05)
    else:
        proc.terminate()
        raise SystemExit("PARTIAL_INIT_SELFTEST_CHECKPOINT_APPEAR_GATE=FAIL")

    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try: proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait()

    partial=segmented/"chain.partial_init"
    if not partial.is_file() or partial.stat().st_size<=0:
        raise SystemExit("PARTIAL_INIT_SELFTEST_BINARY_GATE=FAIL")
    before_meta=parse_meta(meta)
    if int(before_meta.get("accepted",0)) < CHECKPOINT_INTERVAL:
        raise SystemExit("PARTIAL_INIT_SELFTEST_COUNT_GATE=FAIL")

    # Resume from partial init to normal completion.
    subprocess.run([sys.executable,__file__,"--worker","--base",str(segmented),"--sleep","0.0"],check=True)

    bresume=baseline/"chain.resume"
    sresume=segmented/"chain.resume"
    if not (bresume.is_file() and sresume.is_file()):
        raise SystemExit("PARTIAL_INIT_SELFTEST_STOCK_RESUME_GATE=FAIL")
    bh,sh=sha(bresume),sha(sresume)
    if bh != sh:
        raise SystemExit(f"PARTIAL_INIT_REPRODUCIBILITY_GATE=FAIL baseline={bh} segmented={sh}")
    if partial.exists() or meta.exists():
        raise SystemExit("PARTIAL_INIT_CLEANUP_GATE=FAIL")

    out={
        "q":"Q-042",
        "program_id":"Q042-PROD-V13",
        "stage":"POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_SELFTEST",
        "status":"PASS",
        "scientific_result":False,
        "seed":SEED,
        "nprior":NPRIOR,
        "nlive":NLIVE,
        "checkpoint_interval":CHECKPOINT_INTERVAL,
        "interrupted_checkpoint_accepted":int(before_meta["accepted"]),
        "baseline_resume_sha256":bh,
        "segmented_resume_sha256":sh,
        "exact_resume_byte_identity":True,
    }
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("Q042_POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_GATE=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
