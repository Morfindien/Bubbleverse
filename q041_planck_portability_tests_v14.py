#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys

Q="Q-041"
PID="Q041-PLANCKPORT-V14"
RID="R-Q041-EDE-DOWNSTREAM-PORTABILITY-014"

def load(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def dump(p,x): pathlib.Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def static(a):
    pre=load(a.preregister); src=load(a.source_lock); reg=load(a.registry)
    wf=pathlib.Path(a.workflow).read_text(encoding="utf-8")
    program=pathlib.Path(a.program).read_text(encoding="utf-8")

    assert pre["q"]==Q and pre["program_id"]==PID and pre["result_id"]==RID
    assert pre["inference"]["independent_chains_per_arm_combination"]==2
    assert pre["inference"]["Rminus1_stop"]==0.02
    assert pre["inference"]["Rminus1_cl_stop"]==0.2
    assert pre["inference"]["max_samples_per_chain"]==20000
    assert pre["inference"]["hard_science_rhat_gate"]==1.05
    assert pre["technical_revision"]["scientific_and_numerical_settings_changed_from_v13"] is False
    assert pre["technical_revision"]["segment_soft_stop_minutes"]==300
    assert pre["technical_revision"]["github_job_timeout_minutes"]==330
    assert pre["technical_revision"]["max_segments"]==8

    assert src["bubbleverse"]["q032_execution_commit"]=="4dc873a5e880d40858d831a3b421456728f0c032"
    assert src["bubbleverse"]["cobaya_version"]=="3.5.6"
    assert src["technical_revision"]["execution_change"]=="segmented exact Cobaya resume across GitHub-hosted jobs"
    assert src["technical_revision"]["v13_partial_parent_run_id"]==34379785115

    ent=reg["programs"][PID]
    assert ent["status"]=="ACTIVE" and ent["workflow_id"]=="q041-planck-portability-v14.yml"
    assert ent["scientific_and_numerical_settings_changed_from_v13"] is False
    assert ent["segmented_mcmc_resume"] is True

    for token in [
        "Q041-PLANCKPORT-V14","segment","q041-state-v14-",
        "V13_PARENT_RUN_ID: '34379785115'",
        "q041-chain-${{ matrix.implementation }}-${{ matrix.combo }}-c${{ matrix.chain }}-seg${{ inputs.segment }}-v14",
        "actions/cache/restore@v4","actions/cache/save@v4",
        "Restore V13 partial chain when V14 state is absent",
        "Dispatch next V14 segment","q041-planck-portability-v14.yml",
        "timeout-minutes: 330","max-parallel: 6",
        "q032-preflight-sealed-v2","q032-hillipop-covariance-v2",
    ]:
        assert token in wf, token

    assert "permissions:" in wf and "actions: write" in wf
    assert "SEGMENT_SOFT_STOP_MINUTES: '300'" in wf
    assert "MAX_SEGMENTS: '8'" in wf
    assert "if: always()" in wf
    assert "pattern: q041-chain-*-seg${{ inputs.segment }}-v14" in wf

    for token in [
        "import q041_planck_portability_v13 as base",
        'base.PROGRAM_ID=PROGRAM_ID','base.RUN_ID=RUN_ID','base.RESULT_ID=RESULT_ID',
        'cobaya_run(',"resume=True if resuming else False",
        "force=False if resuming else True",
        "SegmentSoftStop","time.monotonic",
        '"status":"PARTIAL_SOFT_STOP"',
        "MAX_SAMPLES_WITHOUT_CONVERGENCE",
        "MCMC.get_new_sample_metropolis=_deadline_guard(original_metropolis)",
        "self.collection.out_update()",
        "self.write_checkpoint()",
        'CHAIN_META="q041_chain_metadata_v14.json"',
        '"burn_in":100,"max_samples":20000,"Rminus1_stop":0.02',
        '"Rminus1_cl_stop":0.2,"learn_proposal":True',
    ]:
        assert token in program, token

    # Never loosen or replace V13 science thresholds.
    assert '"Rminus1_stop":0.02' in program
    assert '"Rminus1_cl_stop":0.2' in program
    assert '"max_samples":20000' in program
    assert "HARD_RHAT=base.HARD_RHAT" in program
    assert "Q040" not in wf

    dump(a.output,{
        "q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":"PASS",
        "gates":{
            "IDENTITY":"PASS","V13_SCIENCE_LOCK":"PASS","SEGMENT_RESUME":"PASS",
            "GITHUB_330_MINUTE_BOUNDARY":"PASS","V13_PARTIAL_SALVAGE":"PASS",
            "Q032_V2_FREEZE":"PASS","AUTO_CONTINUATION":"PASS",
        }
    })
    print("Q041_V14_STATIC_TEST_GATE=PASS")
    return 0

def final(a):
    d=load(a.final)
    assert d["q"]==Q and d["program_id"]==PID and d["result_id"]==RID
    assert d["stage"]=="FINAL" and d["status"]=="PASS" and d["actual_computed_result"] is True
    assert d["scientific_classification"] in [
        "MATERIAL_DOWNSTREAM_DIFFERENCE",
        "SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS",
        "CONSTRAINED_MIXED",
    ]
    assert all(v=="PASS" for v in d["required_gates"].values())
    dump(a.output,{"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":"PASS",
                   "classification":d["scientific_classification"]})
    print("Q041_V14_FINAL_TEST_GATE=PASS")
    return 0

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    x=s.add_parser("static")
    for k in ["preregister","source-lock","registry","workflow","program","output"]:
        x.add_argument("--"+k,required=True)
    x.set_defaults(func=static)
    x=s.add_parser("final")
    x.add_argument("--final",required=True); x.add_argument("--output",required=True)
    x.set_defaults(func=final)
    a=p.parse_args(); return a.func(a)

if __name__=="__main__":
    raise SystemExit(main())
