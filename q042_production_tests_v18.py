#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
Q="Q-042"; PROGRAM_ID="Q042-PROD-V18"
V1_SPEC_SHA256="41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256="0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
PATCHER_SHA256="22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6"
SELFTEST_SHA256="1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9"
ADAPTER_SHA256="b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    x=json.loads(Path(p).read_text())
    if not isinstance(x,dict): raise RuntimeError("JSON_OBJECT_GATE=FAIL")
    return x
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def static(a):
    spec=read(a.spec);lock=read(a.source_lock);rec=read(a.recovery_spec);reg=read(a.registry_patch)
    pr=Path(a.program).read_text();wf=Path(a.workflow).read_text();setup=Path(a.setup).read_text();patcher=Path(a.patcher).read_text();selftest=Path(a.selftest).read_text();adapter=Path(a.adapter).read_text()
    gates={}
    def gate(n,c):
        if not c: raise RuntimeError(n+"=FAIL")
        gates[n]="PASS"
    gate("Q_IDENTITY",spec.get("q")==Q and lock.get("q")==Q)
    gate("V1_SPEC_BYTE_IDENTITY",sha(a.spec)==V1_SPEC_SHA256)
    gate("V1_SOURCE_LOCK_BYTE_IDENTITY",sha(a.parent_source_lock)==V1_SOURCE_LOCK_SHA256)
    gate("V18_LOCK_IDENTITY",lock.get("program_id")==PROGRAM_ID and lock.get("result_id")=="R-Q042-PRODUCTION-PORTABILITY-018")
    gate("V18_RECOVERY_IDENTITY",rec.get("program_id")==PROGRAM_ID and rec.get("supersedes")=="Q042-PROD-V17")
    gate("SCIENCE_UNCHANGED",rec.get("scientific_contract_changed") is False)
    gate("20_CELLS",rec["posterior_recovery"]["fresh_cell_count"]==20)
    gate("BOBYQA_80_REUSED",rec["bobyqa_reuse"]["expected_record_count"]==80 and rec["bobyqa_reuse"]["recompute_in_recovery"]==0)
    gate("INHERITED_V13_PATCHER_HASH",sha(a.patcher)==PATCHER_SHA256)
    gate("INHERITED_V17_SELFTEST_HASH",sha(a.selftest)==SELFTEST_SHA256)
    gate("V18_ADAPTER_HASH",sha(a.adapter)==ADAPTER_SHA256)
    gate("PATCH_INTERVAL_25_UNCHANGED","CHECKPOINT_INTERVAL = 25" in patcher and "mod(RTI%nlive(1),25)==0" in patcher)
    gate("PATCH_SAVES_RNG","random_seed(get=seed)" in patcher and "random_seed(put=seed)" in patcher)
    gate("PATCH_SAVES_FULL_LIVE","write(u) RTI%live(:,i,1)" in patcher)
    gate("SELFTEST_EXACT_BYTE_IDENTITY","exact_resume_byte_identity" in selftest and "ATOMIC_META_AND_BINARY_DETECT_SIGSTOP_THEN_SIGKILL" in selftest)
    gate("ADAPTER_ADDS_ONLY_MINIMAL_PARTIAL_PATTERN",'if minimal:' in adapter and 'output.prefix + ".partial_init"' in adapter)
    gate("ADAPTER_DELEGATES_STOCK_PATTERNS",'original(output, info=info, minimal=minimal)' in adapter)
    gate("ADAPTER_SELFTEST_REPRODUCES_CLEANUP","baseline_cleanup_observed" in adapter and "check_force_resume" in adapter)
    gate("ADAPTER_SELFTEST_PROVES_PRESERVATION","adapted_partial_checkpoint_preserved" in adapter and "adapted_resuming" in adapter)
    gate("PROGRAM_EXPECTS_V17_PARTIAL_RUNTIME",'q042_polychord_partial_init_v17.json' in pr)
    gate("PROGRAM_EXPECTS_ADAPTER_RUNTIME",'q042_cobaya_partial_resume_adapter_v18.json' in pr and f'COBAYA_PARTIAL_RESUME_ADAPTER_SHA256 = "{ADAPTER_SHA256}"' in pr)
    gate("PROGRAM_INSTALLS_ADAPTER_ON_PARTIAL_RESUME","install_partial_init_resume_detection" in pr and 'partial_file.is_file()' in pr and 'not stock_resume_file.is_file()' in pr)
    gate("PROGRAM_RECORDS_ADAPTER_LIFECYCLE","cobaya_partial_resume_adapter_installed" in pr)
    gate("PROGRAM_REQUIRES_ADAPTER_FOR_PARTIAL_LIFECYCLE",'(before or {}).get("checkpoint_kind") != "PARTIAL_INIT"' in pr)
    gate("PROGRAM_PARTIAL_DISCOVERY","*.partial_init" in pr and "partial_init_accepted" in pr)
    gate("PROGRAM_SERIAL_ONLY","V18_PARTIAL_INIT_SERIAL_ONLY_GATE" in pr)
    gate("PROGRAM_SEMANTIC_PARTIAL_PROGRESS",'aacc > bacc' in pr and 'PARTIAL_ACCEPTED_' in pr)
    gate("PROGRAM_PARTIAL_TO_STOCK_PROGRESS",'PARTIAL_TO_STOCK_RESUME' in pr)
    gate("PROGRAM_STOCK_PROGRESS","STOCK_RESUME_CHANGED" in pr)
    gate("PROGRAM_NO_PROGRESS_FAILS","RESUME_NO_CHECKPOINT_PROGRESS" in pr)
    gate("WORKFLOW_STANDARD_RUNNER","runs-on: [q042-hpc]" not in wf and "runs-on: ubuntu-24.04" in wf)
    gate("WORKFLOW_SERIAL","--mpi-ranks 1" in wf)
    gate("WORKFLOW_240M_SEGMENTS",wf.count("--soft-minutes 240 --mpi-ranks 1")>=3)
    gate("WORKFLOW_CANARY_REAL_RELAY","--segment 1 --soft-minutes 240 --mpi-ranks 1" in wf)
    gate("WORKFLOW_CANARY_BEFORE_FANOUT","polychord-canary-relay-segment1" in wf and "needs: [environment, import-bobyqa, polychord-canary-relay-segment1]" in wf)
    gate("WORKFLOW_MATRIX_FAIL_FAST_DISABLED","fail-fast: false" in wf and "fail-fast: true" not in wf)
    gate("WORKFLOW_48_SEGMENTS","max_polychord_segments_per_cell" in wf)
    gate("WORKFLOW_RELAY_PROGRESS_LOG","Q042_RELAY_PARTIAL_ACCEPTED_BEFORE" in wf and "Q042_RELAY_PARTIAL_ACCEPTED_AFTER" in wf)
    gate("WORKFLOW_ADAPTER_COMPILED_AND_BUNDLED",wf.count("q042_cobaya_partial_resume_adapter_v18.py")>=2)
    gate("WORKFLOW_USES_V18_TESTS","q042_production_tests_v18.py" in wf and "q042_production_tests_v17.py" not in wf)
    gate("WORKFLOW_USES_V18_REDUCED_ENV_FILENAMES","q042_primary_nonoverlap_support_prod_v18.json" in wf and "q042_hillipop_nonoverlap_precision_prod_v18.npy" in wf and "q042_primary_nonoverlap_support_prod_v17.json" not in wf)
    gate("SETUP_INHERITS_EXACT_V17_RUNTIME","bash q042_setup_recovery_v17.sh" in setup)
    gate("SETUP_RUNS_ADAPTER_SELFTEST","q042_cobaya_partial_resume_adapter_v18.py" in setup and "--selftest" in setup)
    gate("SETUP_ADAPTER_RUNTIME_MANIFEST","q042_cobaya_partial_resume_adapter_v18.json" in setup)
    gate("SETUP_EXACT_HASH_ASSERTIONS",PATCHER_SHA256 in setup and SELFTEST_SHA256 in setup and ADAPTER_SHA256 in setup)
    tr=rec.get("technical_change_v18",{})
    gate("RECOVERY_ROOT_CAUSE_EVIDENCE",tr.get("observed_v17_root_run_id")==36673568849 and tr.get("observed_v17_canary_segment0_partial_accepted")==900 and tr.get("observed_v17_canary_segment0_nprior")==6500 and tr.get("observed_v17_relay_job_id")==109827789054)
    gate("RECOVERY_CADENCE_UNCHANGED",tr.get("checkpoint_interval_accepted_points")==25 and tr.get("checkpoint_interval_changed") is False)
    gate("RECOVERY_CHECKPOINT_FORMAT_UNCHANGED",tr.get("checkpoint_format_changed") is False and tr.get("checkpoint_contents_changed") is False)
    entry=reg.get("patch",{}).get(PROGRAM_ID)
    gate("REGISTRY_ACTIVE",isinstance(entry,dict) and entry.get("status")=="ACTIVE")
    gate("REGISTRY_PARENT",entry.get("technical_parent_program_id")=="Q042-PROD-V17")
    gate("REGISTRY_WORKFLOW",entry.get("workflow_id")=="q042-production-v18.yml")
    gate("V17_MARKED_BLOCKED",reg.get("patch",{}).get("Q042-PROD-V17",{}).get("status")=="BLOCKED")
    gate("V17_FAILURE_CLASS",reg.get("patch",{}).get("Q042-PROD-V17",{}).get("failure_class")=="COBAYA_PARTIAL_INIT_RESUME_DETECTION_CLEANUP_RESTART")
    try:
        import yaml; gate("WORKFLOW_YAML_PARSE",isinstance(yaml.safe_load(wf),dict))
    except Exception as exc: raise RuntimeError("WORKFLOW_YAML_PARSE=FAIL "+str(exc))
    write(a.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"Q042_PROD_V18_STATIC_TESTS","status":"PASS","gate_count":len(gates),"gates":gates})
    print(f"Q042_PROD_V18_STATIC_TEST_GATE=PASS_{len(gates)}")
    return 0
def runtime_adapter(a):
    import subprocess,sys
    subprocess.run([sys.executable,a.program,"sampler-adapter-regression","--spec",a.spec,"--source-lock",a.source_lock,"--external-runtime",a.external_runtime,"--output",a.output],check=True)
    d=read(a.output)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID or d.get("status")!="PASS": raise RuntimeError("RUNTIME_ADAPTER_RESULT_GATE=FAIL")
    if d.get("corrected_dictionary_accepted") is not True or d.get("v1_dictionary_rejected") is not True: raise RuntimeError("RUNTIME_ADAPTER_REGRESSION_GATE=FAIL")
    print("Q042_PROD_V18_RUNTIME_ADAPTER_TEST_GATE=PASS");return 0
def parser():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static")
    for x in ("spec","source-lock","parent-source-lock","recovery-spec","program","workflow","setup","registry-patch","patcher","selftest","adapter","output"): s.add_argument("--"+x,required=True)
    s.set_defaults(func=static)
    r=sp.add_parser("runtime-adapter")
    for x in ("program","spec","source-lock","external-runtime","output"): r.add_argument("--"+x,required=True)
    r.set_defaults(func=runtime_adapter);return p
if __name__=="__main__":
    a=parser().parse_args();raise SystemExit(a.func(a))
