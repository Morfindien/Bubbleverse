#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib
Q="Q-041"; PID="Q041-PLANCKPORT-V19"; RID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-019"
SCIENCE_CLASSES={"MATERIAL_DOWNSTREAM_DIFFERENCE","SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS","CONSTRAINED_MIXED"}
def load(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def dump(p,x): pathlib.Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def static(a):
    pre=load(a.preregister); src=load(a.source_lock); reg=load(a.registry)
    wf=pathlib.Path(a.workflow).read_text(encoding="utf-8"); program=pathlib.Path(a.program).read_text(encoding="utf-8")
    assert 'HILLIPOP_COMPONENT="planck_2020_hillipop.TT"' in program, "HILLIPOP_COMPONENT_CONSTANT_GATE=FAIL"
    assert pre["q"]==Q and pre["program_id"]==PID and pre["result_id"]==RID
    inf=pre["inference"]
    assert inf["independent_chains_per_arm_combination"]==2 and inf["Rminus1_stop"]==0.02 and inf["Rminus1_cl_stop"]==0.2
    assert inf["max_samples_per_chain"]==20000 and inf["hard_science_rhat_gate"]==1.05
    tr=pre["technical_revision"]
    assert tr["scientific_and_numerical_settings_changed_from_v18"] is False
    assert tr["single_workflow_run"] is True and tr["fixed_linear_segment_chain"] is True and tr["self_dispatch_removed"] is True
    assert tr["fresh_v19_segment1_required"] is True and tr["immediate_predecessor_artifact_only"] is True
    assert tr["hillipop_resume_component_source"]=="chain.updated.yaml" and tr["hillipop_resume_component_hash_gate"] is True
    assert tr["cobaya_allow_changes_used"] is False and tr["max_compute_segments_per_chain"]==8
    assert tr["matrix_jobs_per_segment"]==32 and tr["matrix_jobs_total"]==256 and tr["max_parallel_jobs_per_segment"]==6
    assert src["bubbleverse"]["q032_execution_commit"]=="4dc873a5e880d40858d831a3b421456728f0c032" and src["bubbleverse"]["cobaya_version"]=="3.5.6"
    ent=reg.get("programs",{}).get(PID)
    if ent is None: raise AssertionError("REGISTRY_V19_GATE=FAIL missing Q041-PLANCKPORT-V19")
    assert ent["status"]=="ACTIVE" and ent["workflow_id"]=="q041-planck-portability-v19.yml"
    parent=reg.get("programs",{}).get("Q041-PLANCKPORT-V18")
    if parent is None: raise AssertionError("REGISTRY_V18_PARENT_GATE=FAIL missing Q041-PLANCKPORT-V17")
    assert parent["status"]=="BROKEN" and parent["superseded_by"]==PID
    for n in range(1,9):
        assert f"segment{n}:" in wf and f"COMPUTE SEGMENT {n}/8 — NOT FINAL" in wf
        if n>1:
            assert f"needs: segment{n-1}" in wf
            assert f"-seg{n-1}-v19" in wf
        assert f"--segment '{n}'" in wf and f"-seg{n}-v19" in wf
    assert "needs: environment" in wf and "needs: segment8" in wf
    for token in ["max-parallel: 6","matrix:","implementation: [camspec, hillipop]","chain: [0, 1]",
                  "FINAL — Q041 VALID OUTCOME","finalize-linear","q041-final-v19","q041-environment-v19",
                  "q032-preflight-sealed-v2","q032-hillipop-covariance-v2","actions/download-artifact@v4"]:
        assert token in wf, token
    for forbidden in ["/dispatches","Dispatch next","inputs.segment","inputs.series_id","q041-state-v19-","V16_PARENT_SERIES_ID"]:
        assert forbidden not in wf, forbidden
    for token in ["V19_FRESH_SEGMENT1_GATE","V19_LINEAR_PREDECESSOR_PROVENANCE_GATE","_lock_hillipop_resume_info",
                  "V19_HILLIPOP_RESUME_LOCK_GATE","cobaya_run(info,resume=True,force=False)","cobaya_run(info,resume=False,force=True)",
                  "finalize_linear","SEGMENT_BUDGET_EXHAUSTED_WITH_UNCONVERGED_CHAINS","FINAL_RHAT_GATE_NOT_REACHED"]:
        assert token in program, token
    assert "allow_changes=True" not in (wf+program)
    dump(a.output,{"q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":"PASS","gates":{
      "IDENTITY":"PASS","SCIENCE_LOCK":"PASS","SINGLE_WORKFLOW_RUN":"PASS","EIGHT_LINEAR_SEGMENTS":"PASS",
      "NO_SELF_DISPATCH":"PASS","IMMEDIATE_PREDECESSOR_ARTIFACT":"PASS","HILLIPOP_EXACT_RESUME_LOCK":"PASS","HILLIPOP_COMPONENT_CONSTANT":"PASS",
      "NO_ALLOW_CHANGES":"PASS","MATRIX_32_X_8":"PASS","TECHNICAL_FAILURE_RED":"PASS","CONTROLLED_NO_SCIENCE_GREEN_FINAL":"PASS"}})
    print("Q041_V19_STATIC_TEST_GATE=PASS"); return 0
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
    print(f"Q041_V19_FINAL_TEST_GATE=PASS classification={cls}"); return 0
def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    s=sp.add_parser("static")
    for k in ["preregister","source-lock","registry","workflow","program","output"]: s.add_argument("--"+k,required=True)
    s.set_defaults(func=static)
    s=sp.add_parser("final"); s.add_argument("--final",required=True); s.add_argument("--output",required=True); s.set_defaults(func=final)
    a=p.parse_args(); return a.func(a)
if __name__=="__main__": raise SystemExit(main())
