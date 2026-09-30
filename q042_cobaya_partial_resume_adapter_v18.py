#!/usr/bin/env python3
"""Q042-PROD-V18 Cobaya 3.5.6 partial-init resume adapter.

Cobaya's PolyChord wrapper recognizes only <prefix>.resume as the minimal
resume marker. Q042's pre-stock GenerateLivePoints state lives in
<prefix>.partial_init, so Cobaya 3.5.6 otherwise logs "Did not find an old
sample. Cleaning up and starting anew." and deletes the raw PolyChord folder
before patched PolyChord can read the partial checkpoint.

This adapter changes only Cobaya's *resume-file detection* for PolyChord:
when minimal resume detection is requested, an existing .partial_init file is
also accepted as evidence of a resumable run. Normal output deletion patterns,
PolyChord settings, likelihoods, priors, seeds, checkpoint bytes and sampling
logic are not modified.
"""
from __future__ import annotations
import argparse, json, re, shutil, tempfile
from pathlib import Path

MARKER = "Q042_COBAYA_PARTIAL_RESUME_ADAPTER_V18"


def install_partial_init_resume_detection():
    from cobaya.samplers.polychord.polychord import polychord
    if getattr(polychord, "_q042_partial_resume_adapter_v18", False):
        return False
    original = polychord.output_files_regexps

    def patched(cls, output, info=None, minimal=False):
        entries = list(original(output, info=info, minimal=minimal))
        if minimal:
            entries.append((
                re.compile(re.escape(output.prefix + ".partial_init")),
                cls.get_base_dir(output),
            ))
        return entries

    polychord.output_files_regexps = classmethod(patched)
    polychord._q042_partial_resume_adapter_v18 = True
    polychord._q042_partial_resume_adapter_v18_marker = MARKER
    return True


def _fixture(root: Path):
    from cobaya.output import Output
    from cobaya.samplers.polychord.polychord import polychord
    root.mkdir(parents=True, exist_ok=True)
    prefix = root / "chain"
    # Output only needs the updated-info file to know resume was requested for an
    # existing run; check_force_resume performs the sampler-file detection next.
    Path(str(prefix) + ".updated.yaml").write_text("sampler: {}\n", encoding="utf-8")
    output = Output(str(prefix), resume=True, force=False)
    raw = Path(polychord.get_base_dir(output))
    raw.mkdir(parents=True, exist_ok=True)
    partial = raw / (output.prefix + ".partial_init")
    partial.write_bytes(b"Q042-V18-PARTIAL-RESUME-ADAPTER-SELFTEST")
    return output, partial


def selftest(output_path: str):
    import cobaya
    from cobaya.samplers.polychord.polychord import polychord

    if getattr(cobaya, "__version__", None) != "3.5.6":
        raise SystemExit(f"COBAYA_PARTIAL_RESUME_ADAPTER_VERSION_GATE=FAIL got={getattr(cobaya,'__version__',None)}")

    root = Path(tempfile.mkdtemp(prefix="q042_v18_cobaya_resume_"))
    try:
        # Reproduce the V17 failure with unmodified Cobaya detection.
        base_out, base_partial = _fixture(root / "baseline")
        if not base_out.is_resuming():
            raise SystemExit("COBAYA_PARTIAL_RESUME_BASELINE_PRECONDITION_GATE=FAIL")
        polychord.check_force_resume(base_out, info={})
        baseline_cleanup_observed = (not base_out.is_resuming()) and (not base_partial.exists())
        if not baseline_cleanup_observed:
            raise SystemExit("COBAYA_PARTIAL_RESUME_BASELINE_CLEANUP_GATE=FAIL")

        installed = install_partial_init_resume_detection()
        adapted_out, adapted_partial = _fixture(root / "adapted")
        polychord.check_force_resume(adapted_out, info={})
        adapted_resuming = bool(adapted_out.is_resuming())
        adapted_preserved = adapted_partial.is_file() and adapted_partial.stat().st_size > 0
        if not (adapted_resuming and adapted_preserved):
            raise SystemExit("COBAYA_PARTIAL_RESUME_ADAPTER_PRESERVATION_GATE=FAIL")

        patterns = polychord.output_files_regexps(adapted_out, info={}, minimal=True)
        partial_pattern_present = any(
            getattr(rx, "pattern", "").endswith(re.escape(adapted_out.prefix + ".partial_init"))
            for rx, _ in patterns
        )
        if not partial_pattern_present:
            raise SystemExit("COBAYA_PARTIAL_RESUME_ADAPTER_PATTERN_GATE=FAIL")

        record={
            "q":"Q-042",
            "program_id":"Q042-PROD-V18",
            "stage":"COBAYA_PARTIAL_INIT_RESUME_ADAPTER_SELFTEST_V18",
            "status":"PASS",
            "scientific_result":False,
            "scientific_contract_changed":False,
            "cobaya_version":"3.5.6",
            "marker":MARKER,
            "adapter_installed_now":bool(installed),
            "baseline_cleanup_observed":True,
            "adapted_resuming":True,
            "adapted_partial_checkpoint_preserved":True,
            "normal_output_deletion_patterns_changed":False,
            "minimal_resume_detection_addition":"<prefix>.partial_init",
        }
        p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("Q042_COBAYA_PARTIAL_RESUME_ADAPTER_SELFTEST_V18=PASS")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--output")
    a=ap.parse_args()
    if a.selftest:
        if not a.output: raise SystemExit("--output required with --selftest")
        return selftest(a.output)
    install_partial_init_resume_detection()
    print("Q042_COBAYA_PARTIAL_RESUME_ADAPTER_V18=INSTALLED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
