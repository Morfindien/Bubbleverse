#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
Q="Q-042"; PROGRAM_ID="Q042-PROD-V15"
V1_SPEC_SHA256="41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256="0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
PATCHER_SHA256="22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6"
SELFTEST_SHA256="7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    x=json.loads(Path(p).read_text());
    if not isinstance(x,dict): raise RuntimeError("JSON_OBJECT_GATE=FAIL")
    return x
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def static(a):
    spec=read(a.spec);lock=read(a.source_lock);rec=read(a.recovery_spec);reg=read(a.registry_patch)
    pr=Path(a.program).read_text();wf=Path(a.workflow).read_text();setup=Path(a.setup).read_text();patcher=Path(a.patcher).read_text();selftest=Path(a.selftest).read_text()
    gates={}
    def gate(n,c):
        if not c: raise RuntimeError(n+"=FAIL")
        gates[n]="PASS"
    gate("Q_IDENTITY",spec.get("q")==Q and lock.get("q")==Q)
    gate("V1_SPEC_BYTE_IDENTITY",sha(a.spec)==V1_SPEC_SHA256)
    gate("V1_SOURCE_LOCK_BYTE_IDENTITY",sha(a.parent_source_lock)==V1_SOURCE_LOCK_SHA256)
    gate("V15_LOCK_IDENTITY",lock.get("program_id")==PROGRAM_ID)
    gate("V15_RECOVERY_IDENTITY",rec.get("program_id")==PROGRAM_ID)
    gate("SCIENCE_UNCHANGED",rec.get("scientific_contract_changed") is False)
    gate("20_CELLS",rec["posterior_recovery"]["fresh_cell_count"]==20)
    gate("BOBYQA_80_REUSED",rec["bobyqa_reuse"]["expected_record_count"]==80 and rec["bobyqa_reuse"]["recompute_in_recovery"]==0)
    gate("INHERITED_V13_PATCHER_HASH",sha(a.patcher)==PATCHER_SHA256)
    gate("INHERITED_V13_SELFTEST_HASH",sha(a.selftest)==SELFTEST_SHA256)
    gate("PATCH_INTERVAL_25","CHECKPOINT_INTERVAL = 25" in patcher and "mod(RTI%nlive(1),25)==0" in patcher)
    gate("PATCH_SAVES_RNG","random_seed(get=seed)" in patcher and "random_seed(put=seed)" in patcher)
    gate("PATCH_SAVES_FULL_LIVE","write(u) RTI%live(:,i,1)" in patcher)
    gate("SELFTEST_EXACT_BYTE_IDENTITY","PARTIAL_INIT_REPRODUCIBILITY_GATE" in selftest and "exact_resume_byte_identity" in selftest)
    gate("PROGRAM_EXPECTS_V13_PATCHER_HASH",f'PARTIAL_INIT_PATCHER_SHA256 = "{PATCHER_SHA256}"' in pr)
    gate("PROGRAM_EXPECTS_V13_SELFTEST_HASH",f'PARTIAL_INIT_SELFTEST_SHA256 = "{SELFTEST_SHA256}"' in pr)
    gate("PROGRAM_ADOPTS_V13_RUNTIME_MANIFEST",'q042_polychord_partial_init_v13.json' in pr)
    gate("PROGRAM_PARTIAL_DISCOVERY","*.partial_init" in pr and "partial_init_accepted" in pr)
    gate("PROGRAM_SERIAL_ONLY","V15_PARTIAL_INIT_SERIAL_ONLY_GATE" in pr)
    gate("PROGRAM_SEMANTIC_PARTIAL_PROGRESS",'aacc > bacc' in pr and 'PARTIAL_ACCEPTED_' in pr)
    gate("PROGRAM_PARTIAL_TO_STOCK_PROGRESS",'PARTIAL_TO_STOCK_RESUME' in pr)
    gate("PROGRAM_STOCK_PROGRESS","STOCK_RESUME_CHANGED" in pr)
    gate("PROGRAM_NO_PROGRESS_FAILS","RESUME_NO_CHECKPOINT_PROGRESS" in pr and "RESUME_PROBE_NO_PROGRESS" in pr)
    gate("WORKFLOW_STANDARD_RUNNER","runs-on: [q042-hpc]" not in wf and "runs-on: ubuntu-24.04" in wf)
    gate("WORKFLOW_NO_HPC_LABEL","q042-hpc" not in wf)
    gate("WORKFLOW_SERIAL","--mpi-ranks 1" in wf)
    gate("WORKFLOW_240M_SEGMENTS",wf.count("--soft-minutes 240 --mpi-ranks 1")>=3)
    gate("WORKFLOW_330M_JOB","timeout-minutes: 330" in wf)
    gate("WORKFLOW_RESUME_PROBE","--segment 1 --soft-minutes 10 --mpi-ranks 1 --resume-probe" in wf)
    gate("WORKFLOW_CANARY_BEFORE_FANOUT","polychord-canary-resume-probe" in wf and "needs: [environment, import-bobyqa, polychord-canary-resume-probe]" in wf)
    gate("WORKFLOW_48_SEGMENTS","max_polychord_segments_per_cell" in wf)
    gate("WORKFLOW_RELAY_PROGRESS_LOG","Q042_RELAY_PARTIAL_ACCEPTED_BEFORE" in wf and "Q042_RELAY_PARTIAL_ACCEPTED_AFTER" in wf)
    first_upload=wf.find('name: q042-v15-${{ inputs.root_run_id }}-checkpoint-')
    first_dispatch=wf.find('name: Dispatch continuation after checkpoint upload')
    gate("WORKFLOW_UPLOAD_BEFORE_CONTINUATION_DISPATCH",first_upload!=-1 and first_dispatch!=-1 and first_upload<first_dispatch)
    gate("WORKFLOW_V15_FINAL","q042-production-final-v15" in wf)
    gate("WORKFLOW_RUNTIME_ADAPTER_CALL","q042_production_tests_v15.py runtime-adapter" in wf)
    gate("SETUP_INHERITS_PROVEN_V13_RUNTIME","bash q042_setup_recovery_v13.sh" in setup)
    gate("SETUP_EXACT_HASH_ASSERTIONS",PATCHER_SHA256 in setup and SELFTEST_SHA256 in setup)
    gate("SETUP_REPRO_ASSERTION","selftest_exact_resume_byte_identity" in setup)
    entry=reg.get("patch",{}).get(PROGRAM_ID)
    gate("REGISTRY_ACTIVE",isinstance(entry,dict) and entry.get("status")=="ACTIVE")
    gate("REGISTRY_PARENT",entry.get("technical_parent_program_id")=="Q042-PROD-V13")
    gate("REGISTRY_WORKFLOW",entry.get("workflow_id")=="q042-production-v15.yml")
    gate("V13_MARKED_BLOCKED",reg.get("patch",{}).get("Q042-PROD-V13",{}).get("status")=="BLOCKED")
    gate("V13_FAILURE_CLASS",reg.get("patch",{}).get("Q042-PROD-V13",{}).get("failure_class")=="PARTIAL_INIT_RUNTIME_EXPECTED_HASH_MISMATCH")
    try:
        import yaml; gate("WORKFLOW_YAML_PARSE",isinstance(yaml.safe_load(wf),dict))
    except Exception as exc: raise RuntimeError("WORKFLOW_YAML_PARSE=FAIL "+str(exc))
    write(a.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"Q042_PROD_V15_STATIC_TESTS","status":"PASS","gate_count":len(gates),"gates":gates})
    print(f"Q042_PROD_V15_STATIC_TEST_GATE=PASS_{len(gates)}")
    return 0
def runtime_adapter(a):
    import subprocess,sys
    subprocess.run([sys.executable,a.program,"sampler-adapter-regression","--spec",a.spec,"--source-lock",a.source_lock,"--external-runtime",a.external_runtime,"--output",a.output],check=True)
    d=read(a.output)
    if d.get("q")!=Q or d.get("program_id")!=PROGRAM_ID or d.get("status")!="PASS": raise RuntimeError("RUNTIME_ADAPTER_RESULT_GATE=FAIL")
    if d.get("corrected_dictionary_accepted") is not True or d.get("v1_dictionary_rejected") is not True: raise RuntimeError("RUNTIME_ADAPTER_REGRESSION_GATE=FAIL")
    print("Q042_PROD_V15_RUNTIME_ADAPTER_TEST_GATE=PASS");return 0
def parser():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static")
    for x in ("spec","source-lock","parent-source-lock","recovery-spec","program","workflow","setup","registry-patch","patcher","selftest","output"): s.add_argument("--"+x,required=True)
    s.set_defaults(func=static)
    r=sp.add_parser("runtime-adapter")
    for x in ("program","spec","source-lock","external-runtime","output"): r.add_argument("--"+x,required=True)
    r.set_defaults(func=runtime_adapter);return p
if __name__=="__main__":
    a=parser().parse_args();raise SystemExit(a.func(a))
