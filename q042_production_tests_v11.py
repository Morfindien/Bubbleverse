#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

Q="Q-042"; PROGRAM_ID="Q042-PROD-V11"
V1_SPEC_SHA256="41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256="0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
PATCHER_SHA256="b8dc1fe134f69068fb5a1c97044b4bb5910b93320156acae009b76135a3f9136"
SELFTEST_SHA256="7f103dd2fd7a6f5575af4de43e8102d3b99893abaf16ee2ea1973a8780de7a69"

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    x=json.loads(Path(p).read_text())
    if not isinstance(x,dict): raise RuntimeError("JSON_OBJECT_GATE=FAIL")
    return x
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")

def static(a):
    spec=read(a.spec); lock=read(a.source_lock); rec=read(a.recovery_spec); reg=read(a.registry_patch)
    pr=Path(a.program).read_text(); wf=Path(a.workflow).read_text(); setup=Path(a.setup).read_text()
    patcher=Path(a.patcher).read_text(); selftest=Path(a.selftest).read_text()
    gates={}
    def gate(n,c):
        if not c: raise RuntimeError(n+"=FAIL")
        gates[n]="PASS"

    gate("Q_IDENTITY",spec.get("q")==Q and lock.get("q")==Q)
    gate("V1_SPEC_BYTE_IDENTITY",sha(a.spec)==V1_SPEC_SHA256)
    gate("V1_SOURCE_LOCK_BYTE_IDENTITY",sha(a.parent_source_lock)==V1_SOURCE_LOCK_SHA256)
    gate("V11_LOCK_IDENTITY",lock.get("program_id")==PROGRAM_ID)
    gate("V11_RECOVERY_IDENTITY",rec.get("program_id")==PROGRAM_ID)
    gate("SCIENCE_UNCHANGED",rec.get("scientific_contract_changed") is False)
    gate("20_CELLS",rec["posterior_recovery"]["fresh_cell_count"]==20)
    gate("BOBYQA_80_REUSED",rec["bobyqa_reuse"]["expected_record_count"]==80 and rec["bobyqa_reuse"]["recompute_in_recovery"]==0)

    gate("PATCHER_HASH",sha(a.patcher)==PATCHER_SHA256)
    gate("SELFTEST_HASH",sha(a.selftest)==SELFTEST_SHA256)
    gate("PATCH_BASE_COMMIT","3ade6445bb3719a6db6f6e81f178765545ffc833" in patcher)
    gate("PATCH_INTERVAL_25","CHECKPOINT_INTERVAL = 25" in patcher and "mod(RTI%nlive(1),25)==0" in patcher)
    gate("PATCH_SAVES_RNG","random_seed(get=seed)" in patcher and "random_seed(put=seed)" in patcher)
    gate("PATCH_SAVES_FULL_LIVE","write(u) RTI%live(:,i,1)" in patcher)
    gate("PATCH_RESTORES_FULL_LIVE","call add_point(point,RTI%live,RTI%nlive,1)" in patcher)
    gate("PATCH_ATOMIC_BINARY","partial_init.tmp" in patcher and "call rename(trim(tmp),trim(final))" in patcher)
    gate("PATCH_CLEANUP_AFTER_STOCK_RESUME","q042_delete_partial_init_checkpoint_done" in patcher)
    gate("SELFTEST_INTERRUPT_RESUME","send_signal(signal.SIGINT)" in selftest)
    gate("SELFTEST_EXACT_BYTE_IDENTITY","PARTIAL_INIT_REPRODUCIBILITY_GATE" in selftest and "exact_resume_byte_identity" in selftest)

    gate("PROGRAM_PARTIAL_DISCOVERY","*.partial_init" in pr and "checkpoint_kind" in pr)
    gate("PROGRAM_SERIAL_ONLY","V11_PARTIAL_INIT_SERIAL_ONLY_GATE" in pr)
    gate("PROGRAM_PATCH_RUNTIME_GATE","PARTIAL_INIT_RUNTIME_CONTENT_GATE" in pr)
    gate("PROGRAM_RESUME_PROGRESS_REQUIRED","RESUME_PROBE_NO_PROGRESS" in pr)
    gate("PROGRAM_V1_MATRIX_BYTE_REUSE","BYTE_IDENTICAL_REDUCED_MATRIX_COPY_GATE" in pr)
    gate("PROGRAM_METADATA_ADAPTER","POLYCHORD_EXECUTABLE_KEYS" in pr and "V1_DICTIONARY_REJECTION_REGRESSION_GATE" in pr)

    gate("WORKFLOW_STANDARD_RUNNER","runs-on: [q042-hpc]" not in wf and "runs-on: ubuntu-24.04" in wf)
    gate("WORKFLOW_NO_HPC_LABEL","q042-hpc" not in wf)
    gate("WORKFLOW_SERIAL","--mpi-ranks 1" in wf)
    gate("WORKFLOW_240M_CANARY","--segment 0 --soft-minutes 240 --mpi-ranks 1" in wf)
    gate("WORKFLOW_RESUME_PROBE","--segment 1 --soft-minutes 10 --mpi-ranks 1 --resume-probe" in wf)
    gate("WORKFLOW_CANARY_BEFORE_FANOUT","polychord-canary-resume-probe" in wf and "needs: [environment, import-bobyqa, polychord-canary-resume-probe]" in wf)
    gate("WORKFLOW_FAIL_FAST","fail-fast: true" in wf)
    gate("WORKFLOW_48_SEGMENTS","max_polychord_segments_per_cell" in wf)
    gate("WORKFLOW_FINAL_EXPECTS_21","EXPECTED=21" in wf)
    gate("WORKFLOW_V11_FINAL","q042-production-final-v11" in wf)
    gate("WORKFLOW_V11_REDUCED_META","q042_hillipop_nonoverlap_precision_prod_v11.json" in wf)
    gate("WORKFLOW_RUNTIME_ADAPTER_CALL","q042_production_tests_v11.py runtime-adapter" in wf)
    gate("TEST_HARNESS_RUNTIME_ADAPTER_SUBCOMMAND","sp.add_parser(\"runtime-adapter\")" in Path(__file__).read_text())

    gate("SETUP_REUSES_FROZEN_RUNTIME","q042_setup_recovery_v8.sh" in setup)
    gate("SETUP_APPLIES_PATCH","q042_patch_polychord_partial_init_v11.py" in setup)
    gate("SETUP_REBUILDS_POLYCHORD","libchord.so MPI=1" in setup)
    gate("SETUP_RUNS_REPRO_TEST","q042_polychord_partial_init_selftest_v11.py" in setup)
    gate("SETUP_RUNTIME_MANIFEST","q042_polychord_partial_init_v11.json" in setup)

    entry=reg.get("patch",{}).get(PROGRAM_ID)
    gate("REGISTRY_ACTIVE",isinstance(entry,dict) and entry.get("status")=="ACTIVE")
    gate("REGISTRY_PARENT",entry.get("technical_parent_program_id")=="Q042-PROD-V10")
    gate("REGISTRY_WORKFLOW",entry.get("workflow_id")=="q042-production-v11.yml")
    gate("V10_MARKED_BLOCKED",reg.get("patch",{}).get("Q042-PROD-V10",{}).get("status")=="BLOCKED")
    gate("V10_FAILURE_CLASS",reg.get("patch",{}).get("Q042-PROD-V10",{}).get("failure_class")=="MISSING_RUNTIME_ADAPTER_TEST_SUBCOMMAND")

    try:
        import yaml
        gate("WORKFLOW_YAML_PARSE",isinstance(yaml.safe_load(wf),dict))
    except Exception as exc:
        raise RuntimeError("WORKFLOW_YAML_PARSE=FAIL "+str(exc))

    write(a.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"Q042_PROD_V11_STATIC_TESTS","status":"PASS","gate_count":len(gates),"gates":gates})
    print(f"Q042_PROD_V11_STATIC_TEST_GATE=PASS_{len(gates)}")
    return 0

def runtime_adapter(a):
    import subprocess,sys
    cmd=[
        sys.executable,a.program,"sampler-adapter-regression",
        "--spec",a.spec,
        "--source-lock",a.source_lock,
        "--external-runtime",a.external_runtime,
        "--output",a.output,
    ]
    subprocess.run(cmd,check=True)
    d=read(a.output)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID or d.get("status")!="PASS":
        raise RuntimeError("RUNTIME_ADAPTER_RESULT_GATE=FAIL")
    if d.get("corrected_dictionary_accepted") is not True or d.get("v1_dictionary_rejected") is not True:
        raise RuntimeError("RUNTIME_ADAPTER_REGRESSION_GATE=FAIL")
    print("Q042_PROD_V11_RUNTIME_ADAPTER_TEST_GATE=PASS")
    return 0

def parser():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static")
    for x in ("spec","source-lock","parent-source-lock","recovery-spec","program","workflow","setup","registry-patch","patcher","selftest","output"):
        s.add_argument("--"+x,required=True)
    s.set_defaults(func=static)
    r=sp.add_parser("runtime-adapter")
    for x in ("program","spec","source-lock","external-runtime","output"):
        r.add_argument("--"+x,required=True)
    r.set_defaults(func=runtime_adapter)
    return p

if __name__=="__main__":
    a=parser().parse_args(); raise SystemExit(a.func(a))
