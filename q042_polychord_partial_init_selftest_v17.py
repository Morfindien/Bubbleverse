#!/usr/bin/env python3
"""Robust technical self-test for Q042 V17 PolyChord partial-init checkpointing.

This is a deployment/test-harness repair only. It does not alter the V13
PolyChord patch, checkpoint format, production sampler settings, or science.
The synthetic capture worker is intentionally slowed so the parent has a wide
window to observe a completed atomic checkpoint. Once both the metadata file
and binary checkpoint are present, the worker is SIGSTOP-frozen before teardown
can delete the checkpoint, then SIGKILLed. The saved checkpoint is subsequently
resumed to completion and must reproduce the uninterrupted stock .resume bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

SEED = 314159
NPRIOR = 100
NLIVE = 10
CHECKPOINT_INTERVAL = 25
CAPTURE_ATTEMPTS = 3
CAPTURE_SLEEP_S = 0.25
CAPTURE_DEADLINE_S = 120.0
POLL_S = 0.02


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run_worker(base: Path, sleep_s: float):
    import numpy as np
    import pypolychord
    from pypolychord.settings import PolyChordSettings

    base.mkdir(parents=True, exist_ok=True)

    def prior(cube):
        return np.asarray(cube, dtype=float)

    def loglike(theta):
        if sleep_s:
            time.sleep(sleep_s)
        x = np.asarray(theta, dtype=float)
        return -0.5 * float(np.dot(x - 0.37, x - 0.37)), []

    settings = PolyChordSettings(
        2,
        0,
        base_dir=str(base),
        file_root="chain",
        nlive=NLIVE,
        nprior=NPRIOR,
        num_repeats=2,
        nfail=NLIVE,
        precision_criterion=0.2,
        max_ndead=30,
        do_clustering=False,
        read_resume=True,
        write_resume=True,
        write_live=True,
        write_dead=True,
        write_prior=True,
        write_stats=True,
        seed=SEED,
        feedback=0,
        grade_frac=[2.0],
        grade_dims=[2],
        synchronous=True,
    )
    pypolychord.run_polychord(loglike, 2, 0, settings, prior=prior)


def parse_meta(p: Path):
    d = {}
    if not p.exists():
        return d
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            try:
                d[k] = int(v)
            except Exception:
                d[k] = v
    return d


def stop_process(proc: subprocess.Popen):
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def capture_checkpoint(worker_file: str, segmented: Path):
    """Capture a fully renamed partial checkpoint without racing cleanup."""
    if not hasattr(signal, "SIGSTOP"):
        raise SystemExit("PARTIAL_INIT_SELFTEST_SIGSTOP_GATE=FAIL")

    failures = []
    for attempt in range(1, CAPTURE_ATTEMPTS + 1):
        shutil.rmtree(segmented, ignore_errors=True)
        proc = subprocess.Popen(
            [
                sys.executable,
                worker_file,
                "--worker",
                "--base",
                str(segmented),
                "--sleep",
                str(CAPTURE_SLEEP_S),
            ]
        )
        meta = segmented / "chain.partial_init.meta"
        partial = segmented / "chain.partial_init"
        deadline = time.time() + CAPTURE_DEADLINE_S
        observed = {}
        frozen = False

        try:
            while time.time() < deadline:
                observed = parse_meta(meta)
                accepted = int(observed.get("accepted", 0) or 0)
                if (
                    accepted >= CHECKPOINT_INTERVAL
                    and partial.is_file()
                    and partial.stat().st_size > 0
                ):
                    # Freeze immediately after observing both atomically-renamed final
                    # files. This prevents a fast synthetic run from finishing and
                    # deleting the partial checkpoint before the parent verifies it.
                    try:
                        os.kill(proc.pid, signal.SIGSTOP)
                        frozen = True
                    except ProcessLookupError:
                        frozen = False

                    if frozen:
                        time.sleep(0.05)
                        observed2 = parse_meta(meta)
                        if (
                            proc.poll() is None
                            and int(observed2.get("accepted", 0) or 0)
                            >= CHECKPOINT_INTERVAL
                            and partial.is_file()
                            and partial.stat().st_size > 0
                        ):
                            before_hash = sha(partial)
                            before_size = partial.stat().st_size
                            # SIGKILL is deliberate here: the checkpoint file is already
                            # closed and atomically renamed. Killing a frozen synthetic
                            # process guarantees teardown cannot remove it.
                            os.kill(proc.pid, signal.SIGKILL)
                            proc.wait()
                            return {
                                "attempt": attempt,
                                "meta": observed2,
                                "partial_sha256": before_hash,
                                "partial_size": before_size,
                            }
                        # If the post-freeze verification failed, let the process move
                        # again so cleanup below can terminate it normally.
                        try:
                            os.kill(proc.pid, signal.SIGCONT)
                        except ProcessLookupError:
                            pass
                        frozen = False

                if proc.poll() is not None:
                    failures.append(
                        f"attempt={attempt}:worker_exited rc={proc.returncode} accepted={accepted}"
                    )
                    break
                time.sleep(POLL_S)
            else:
                failures.append(
                    f"attempt={attempt}:deadline accepted={int(observed.get('accepted', 0) or 0)}"
                )
        finally:
            if frozen and proc.poll() is None:
                try:
                    os.kill(proc.pid, signal.SIGCONT)
                except ProcessLookupError:
                    pass
            stop_process(proc)

    raise SystemExit(
        "PARTIAL_INIT_SELFTEST_CAPTURE_GATE=FAIL " + ";".join(failures)
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--sleep", type=float, default=CAPTURE_SLEEP_S)
    ap.add_argument("--output")
    a = ap.parse_args()

    if a.worker:
        run_worker(Path(a.base), a.sleep)
        return 0

    if not a.output:
        raise SystemExit("--output required")

    root = Path("q042_runtime/q042_partial_init_selftest_work_v17")
    shutil.rmtree(root, ignore_errors=True)
    baseline = root / "baseline"
    segmented = root / "segmented"

    # Reference uninterrupted run.
    subprocess.run(
        [sys.executable, __file__, "--worker", "--base", str(baseline), "--sleep", "0.0"],
        check=True,
    )

    capture = capture_checkpoint(__file__, segmented)
    meta = segmented / "chain.partial_init.meta"
    partial = segmented / "chain.partial_init"
    before_meta = parse_meta(meta)

    if not partial.is_file() or partial.stat().st_size <= 0:
        raise SystemExit("PARTIAL_INIT_SELFTEST_BINARY_GATE=FAIL")
    if int(before_meta.get("accepted", 0)) < CHECKPOINT_INTERVAL:
        raise SystemExit("PARTIAL_INIT_SELFTEST_COUNT_GATE=FAIL")
    if sha(partial) != capture["partial_sha256"]:
        raise SystemExit("PARTIAL_INIT_SELFTEST_FROZEN_BINARY_IDENTITY_GATE=FAIL")

    # Resume from the captured partial init to normal completion.
    subprocess.run(
        [sys.executable, __file__, "--worker", "--base", str(segmented), "--sleep", "0.0"],
        check=True,
    )

    bresume = baseline / "chain.resume"
    sresume = segmented / "chain.resume"
    if not (bresume.is_file() and sresume.is_file()):
        raise SystemExit("PARTIAL_INIT_SELFTEST_STOCK_RESUME_GATE=FAIL")

    bh, sh = sha(bresume), sha(sresume)
    if bh != sh:
        raise SystemExit(
            f"PARTIAL_INIT_REPRODUCIBILITY_GATE=FAIL baseline={bh} segmented={sh}"
        )
    if partial.exists() or meta.exists():
        raise SystemExit("PARTIAL_INIT_CLEANUP_GATE=FAIL")

    out = {
        "q": "Q-042",
        "program_id": "Q042-PROD-V17",
        "stage": "POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_SELFTEST_V17",
        "status": "PASS",
        "scientific_result": False,
        "scientific_contract_changed": False,
        "seed": SEED,
        "nprior": NPRIOR,
        "nlive": NLIVE,
        "checkpoint_interval": CHECKPOINT_INTERVAL,
        "capture_attempts_max": CAPTURE_ATTEMPTS,
        "capture_attempt_used": capture["attempt"],
        "capture_sleep_seconds": CAPTURE_SLEEP_S,
        "capture_method": "ATOMIC_META_AND_BINARY_DETECT_SIGSTOP_THEN_SIGKILL",
        "interrupted_checkpoint_accepted": int(before_meta["accepted"]),
        "captured_partial_sha256": capture["partial_sha256"],
        "captured_partial_size": capture["partial_size"],
        "baseline_resume_sha256": bh,
        "segmented_resume_sha256": sh,
        "exact_resume_byte_identity": True,
    }
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Q042_POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_GATE_V17=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
