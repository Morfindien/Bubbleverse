#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

Q="Q-042"; PROGRAM_ID="Q042-PROD-V19"
V1_SPEC_SHA="41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_LOCK_SHA="0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V18_LOCK_SHA="6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde"

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    x=json.loads(Path(p).read_text())
    if not isinstance(x,dict): raise RuntimeError("JSON_OBJECT_GATE=FAIL")
    return x
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")

def static(a):
    spec=read(a.spec); lock=read(a.source_lock); rec=read(a.recovery_spec)
    pr=Path(a.program).read_text(); wf=Path(a.workflow).read_text()
    gates={}
    def gate(n,c):
        if not c: raise RuntimeError(n+"=FAIL")
        gates[n]="PASS"
    gate("Q_IDENTITY",spec.get("q")==Q and lock.get("q")==Q)
    gate("V1_SPEC_BYTE_IDENTITY",sha(a.spec)==V1_SPEC_SHA)
    gate("V1_SOURCE_LOCK_BYTE_IDENTITY",sha(a.parent_v1_lock)==V1_LOCK_SHA)
    gate("V18_SOURCE_LOCK_BYTE_IDENTITY",sha(a.parent_v18_lock)==V18_LOCK_SHA)
    gate("V19_LOCK_IDENTITY",lock.get("program_id")==PROGRAM_ID and lock.get("result_id")=="R-Q042-PRODUCTION-PORTABILITY-019")
    gate("V19_RECOVERY_IDENTITY",rec.get("program_id")==PROGRAM_ID and rec.get("supersedes")=="Q042-PROD-V18")
    gate("MERGE_ONLY_RECOVERY",rec.get("recovery_class")=="MERGE_ONLY_EXISTING_V18_ARTIFACTS")
    gate("SCIENCE_UNCHANGED",rec.get("scientific_contract_changed") is False)
    tc=rec.get("technical_change_v19",{})
    gate("NO_NEW_POLYCHORD",tc.get("new_polychord_compute") is False)
    gate("NO_NEW_BOBYQA",tc.get("new_bobyqa_compute") is False)
    gate("NO_CLASSIFIER_CHANGE",tc.get("classification_rules_changed") is False and tc.get("thresholds_changed") is False)
    obs=rec.get("observed_v18_failure",{})
    gate("V18_FAILURE_EVIDENCE",obs.get("collector_run_id")==37151674348 and obs.get("collector_job_id")==111286678009 and obs.get("failed_gate")=="V13_POLYCHORD_FINAL_COUNT_GATE=FAIL")
    gate("V18_READY_21",obs.get("collector_readiness",{}).get("found")==21 and obs.get("collector_readiness",{}).get("expected")==21)
    gate("PROGRAM_READS_V18_POLYCHORD_FINALS",'q042_production_polychord_final_v18.json' in pr)
    gate("PROGRAM_READS_INHERITED_V13_BOBYQA",'q042_production_bobyqa_start_v13.json' in pr)
    gate("PROGRAM_CREATES_V1_SHADOWS",'q042_production_polychord_final_v1.json' in pr and 'q042_production_bobyqa_start_v1.json' in pr)
    gate("PROGRAM_DELETES_SHADOWS",'p.unlink()' in pr)
    gate("PROGRAM_REUSES_V1_MERGE",'rc = v1.merge_final(a)' in pr)
    gate("PROGRAM_SOURCE_IDENTITY_IS_V18",'v1.PROGRAM_ID = SOURCE_PROGRAM_ID' in pr)
    gate("PROGRAM_EXPOSES_ONLY_STATIC_AND_MERGE",'sp.add_parser("polychord-segment")' not in pr and 'sp.add_parser("bobyqa-stage")' not in pr)
    gate("WORKFLOW_MERGE_ONLY_NAME",'merge-only recovery' in wf)
    gate("WORKFLOW_FROZEN_ROOT",'36731879692' in wf)
    gate("WORKFLOW_FROZEN_V18_COMMIT",'d0f92c7f2ce53da32818244f8847f8e745e20c4f' in wf)
    gate("WORKFLOW_EXPECTS_21_ARTIFACTS",'selected_artifact_count' in wf and 'count=21' in wf)
    gate("WORKFLOW_DIGEST_VERIFICATION",'V19_ARTIFACT_ZIP_DIGEST_GATE=FAIL' in wf and 'sha256sum' in wf)
    gate("WORKFLOW_NO_SETUP_RUNTIME",'q042_setup_recovery' not in wf)
    gate("WORKFLOW_NO_POLYCHORD_EXECUTION",'polychord-segment' not in wf and '--soft-minutes' not in wf)
    gate("WORKFLOW_NO_BOBYQA_EXECUTION",'bobyqa-stage' not in wf)
    try:
        import yaml; gate("WORKFLOW_YAML_PARSE",isinstance(yaml.safe_load(wf),dict))
    except Exception as exc: raise RuntimeError("WORKFLOW_YAML_PARSE=FAIL "+str(exc))
    write(a.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"Q042_PROD_V19_STATIC_TESTS","status":"PASS","gate_count":len(gates),"gates":gates})
    print(f"Q042_PROD_V19_STATIC_TEST_GATE=PASS_{len(gates)}")
    return 0

def parser():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static")
    for x in ("spec","parent-v1-lock","parent-v18-lock","source-lock","recovery-spec","program","workflow","output"): s.add_argument("--"+x,required=True)
    s.set_defaults(func=static); return p
if __name__=="__main__":
    a=parser().parse_args(); raise SystemExit(a.func(a))
