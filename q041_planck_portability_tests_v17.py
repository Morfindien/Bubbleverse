#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib
Q="Q-041"; PID="Q041-PLANCKPORT-V17"; RID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-017"
SCIENCE_CLASSES={"MATERIAL_DOWNSTREAM_DIFFERENCE","SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS","CONSTRAINED_MIXED"}
def load(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def dump(p,x): pathlib.Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def static(a):
    pre=load(a.preregister); src=load(a.source_lock); reg=load(a.registry)
    wf=pathlib.Path(a.workflow).read_text(encoding="utf-8"); program=pathlib.Path(a.program).read_text(encoding="utf-8")
    assert pre["q"]==Q and pre["program_id"]==PID and pre["result_id"]==RID
    inf=pre["inference"]; assert inf["independent_chains_per_arm_combination"]==2
    assert inf["Rminus1_stop"]==0.02 and inf["Rminus1_cl_stop"]==0.2 and inf["max_samples_per_chain"]==20000 and inf["hard_science_rhat_gate"]==1.05
    tr=pre["technical_revision"]; assert tr["scientific_and_numerical_settings_changed_from_v16"] is False
    assert tr["locked_v16_checkpoint_migration_only"] is True and tr["same_v17_series_resume_after_migration"] is True
    assert tr["hillipop_resume_component_source"]=="chain.updated.yaml" and tr["hillipop_resume_component_hash_gate"] is True
    assert tr["cobaya_allow_changes_used"] is False and tr["per_chain_compute_segment_budget_preserved"] is True
    assert tr["controlled_no_science_is_green_final"] is True and tr["technical_failure_remains_red"] is True
    assert tr["segment_soft_stop_minutes"]==300 and tr["github_job_timeout_minutes"]==330 and tr["max_compute_segments_per_chain"]==8
    assert src["bubbleverse"]["q032_execution_commit"]=="4dc873a5e880d40858d831a3b421456728f0c032" and src["bubbleverse"]["cobaya_version"]=="3.5.6"
    ent=reg["programs"][PID]; assert ent["status"]=="ACTIVE" and ent["workflow_id"]=="q041-planck-portability-v17.yml"
    assert ent["locked_v16_checkpoint_migration_only"] is True and ent["hillipop_resume_component_lock"] is True
    assert reg["programs"]["Q041-PLANCKPORT-V16"]["status"]=="BROKEN" and reg["programs"]["Q041-PLANCKPORT-V16"]["superseded_by"]==PID
    for token in ["Q041-PLANCKPORT-V17","R-Q041-EDE-DOWNSTREAM-PORTABILITY-017","series_id:",
                  "q041-state-v17-${{ inputs.series_id }}-","q041_chain_metadata_v17.json",
                  "Restore locked V16 parent chain state for one-time migration","q041_chain_metadata_v16.json",
                  "V16_PARENT_SERIES_ID: '34498890334'",
                  "NO_SCIENTIFIC_RESULT","controlled_no_science","technical_failure",
                  "FINAL VALID OUTCOME — NO SCIENTIFIC RESULT","FINAL SCIENTIFIC RESULT — Q041",
                  "COMPUTE SEGMENT ${{ inputs.segment }} — NOT FINAL","timeout-minutes: 330","max-parallel: 6",
                  "q032-preflight-sealed-v2","q032-hillipop-covariance-v2","Dispatch next V17 segment",
                  '"series_id":os.environ["SERIES_ID"]']:
        assert token in wf, token
    for forbidden in ["Restore V13 partial chain","_adopt_v14_metadata","allow_changes=True"]:
        assert forbidden not in (wf+program), forbidden
    for token in ["_resume_provenance_gate","V17_SAME_SERIES_RESUME_PROVENANCE_GATE","_adopt_v16_state_gate",
                  "_lock_hillipop_resume_info","V17_HILLIPOP_RESUME_LOCK_GATE","compute_segments_used",
                  "_write_no_science_final","finalize_no_science",'"status":"NO_SCIENTIFIC_RESULT"',
                  '"FINAL_RHAT_GATE_NOT_REACHED"','"technical_failure":True',
                  'cobaya_run(info,resume=True,force=False)',
                  '"burn_in":100,"max_samples":20000,"Rminus1_stop":0.02']:
        assert token in program, token
    assert "Q040-RQMC" not in wf and "Q040-CMBSPACE" not in wf
    dump(a.output,{"q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":"PASS","gates":{
      "IDENTITY":"PASS","V16_SCIENCE_LOCK":"PASS","LOCKED_V16_MIGRATION":"PASS","SAME_SERIES_RESUME_ONLY":"PASS",
      "HILLIPOP_EXACT_RESUME_LOCK":"PASS","NO_ALLOW_CHANGES":"PASS","PER_CHAIN_SEGMENT_BUDGET":"PASS","CONTROLLED_NO_SCIENCE_GREEN_FINAL":"PASS",
      "TECHNICAL_FAILURE_RED":"PASS","Q032_V2_FREEZE":"PASS"}})
    print("Q041_V17_STATIC_TEST_GATE=PASS"); return 0
def final(a):
    d=load(a.final); assert d["q"]==Q and d["program_id"]==PID and d["result_id"]==RID
    assert d["stage"]=="FINAL" and d["status"]=="PASS" and d.get("final_outcome_valid") is True and d.get("technical_failure") is False
    cls=d["scientific_classification"]
    if cls in SCIENCE_CLASSES:
        assert d["actual_computed_result"] is True and d.get("outcome_type")=="SCIENTIFIC_RESULT"
        assert all(v=="PASS" for v in d["required_gates"].values())
    else:
        assert cls=="NO_SCIENTIFIC_RESULT" and d["actual_computed_result"] is False and d.get("outcome_type")=="CONTROLLED_NO_SCIENTIFIC_RESULT"
        assert d.get("no_science_reason") in {"MAX_SAMPLES_WITHOUT_CONVERGENCE","SEGMENT_BUDGET_EXHAUSTED_WITH_UNCONVERGED_CHAINS","FINAL_RHAT_GATE_NOT_REACHED"}
    dump(a.output,{"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":"PASS","classification":cls,"outcome_type":d.get("outcome_type")})
    print(f"Q041_V17_FINAL_TEST_GATE=PASS classification={cls}"); return 0
def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    x=s.add_parser("static")
    for k in ["preregister","source-lock","registry","workflow","program","output"]: x.add_argument("--"+k,required=True)
    x.set_defaults(func=static)
    x=s.add_parser("final"); x.add_argument("--final",required=True); x.add_argument("--output",required=True); x.set_defaults(func=final)
    a=p.parse_args(); return a.func(a)
if __name__=="__main__": raise SystemExit(main())
