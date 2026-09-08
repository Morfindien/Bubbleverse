#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, importlib.util, json, math, tempfile
from pathlib import Path

Q="Q-039"
PROGRAM_ID="Q039-FGPROFILE-V1"
RUN_ID="Q039-NATIVE-FOREGROUND-PROFILE-V1"
RESULT_ID="R-Q039-EDE-NATIVE-FOREGROUND-PROFILE-001"


def write(path,obj): Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def load_module(path):
    spec=importlib.util.spec_from_file_location("q039_fgprofile_v1_static",path)
    if spec is None or spec.loader is None: raise RuntimeError("MODULE_LOAD_GATE=FAIL")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False


def static(args):
    pp=Path(args.program); text=pp.read_text(encoding="utf-8"); tree=ast.parse(text); mod=load_module(pp)
    prereg=json.loads(Path(args.preregister).read_text(encoding="utf-8"))
    source=json.loads(Path(args.source_lock).read_text(encoding="utf-8"))
    # Deterministic synthetic geometry proof.
    rows={"camspec":{},"hillipop":{}}
    for i,label in enumerate(mod.LABELS):
        base={c:0.0 for c in mod.COORDS}
        rows["camspec"][label]=dict(base)
        rows["hillipop"][label]=dict(base)
    zero=mod.calculate_metrics(rows,mod.LABELS)
    synthetic_geometry=(zero["matched_median"]==0.0 and zero["centroid"]==0.0 and zero["pairwise_median_drift"]==0.0 and mod.sufficient(zero))
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cfg=root/"q032_planck_tt3pair_bridge_v2_config.yml"; cfg.write_text("x: 1\n",encoding="utf-8")
        resolved=mod.resolve_q032_config_path(root); absolute_path_gate=(resolved==cfg.resolve())
    gates={
      "PYTHON_PARSE_GATE":isinstance(tree,ast.Module),
      "Q_IDENTITY_GATE":mod.Q==Q,
      "PROGRAM_ID_GATE":mod.PROGRAM_ID==PROGRAM_ID,
      "RUN_ID_GATE":mod.RUN_ID==RUN_ID,
      "RESULT_ID_GATE":mod.RESULT_ID==RESULT_ID,
      "INTERVENTION_IDENTITY_GATE":mod.INTERVENTION=="NATIVE_FOREGROUND_PROFILE_FREEDOM_OFF",
      "Q032_COMMIT_GATE":mod.Q032_EXECUTION_COMMIT=="4dc873a5e880d40858d831a3b421456728f0c032",
      "BACKEND_COMMIT_GATE":mod.BACKEND_COMMIT=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "HILLIPOP_COMMIT_GATE":mod.HILLIPOP_COMMIT=="a09ddde3e7ce11df99f74685feb1f1764cafb251",
      "SUPPORT_HASH_GATE":mod.SUPPORT_HASH=="f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b",
      "SCALE_HASH_GATE":mod.SCALES_HASH=="732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6",
      "THRESHOLD_GATE":mod.THRESHOLD==0.10,
      "PROFILE_COUNT_GATE":len(mod.LABELS)*len(mod.IMPLEMENTATIONS)==18,
      "CAMSPEC_FOREGROUND_SET_GATE":tuple(mod.EXPECTED_CAMSPEC_FOREGROUND)==("amp_143","amp_217","amp_143x217","n_143","n_217","n_143x217"),
      "HILLIPOP_FOREGROUND_SET_GATE":tuple(mod.EXPECTED_HILLIPOP_FOREGROUND)==("Aradio","Adusty","AdustT","beta_dustT","Acib","beta_cib","Atsz","Aksz","xi"),
      "NO_APLANCK_OR_CALIBRATION_IN_FOREGROUND_GATE":not set(mod.EXPECTED_CAMSPEC_FOREGROUND+mod.EXPECTED_HILLIPOP_FOREGROUND).intersection(mod.PROHIBITED_FOREGROUND_NAMES),
      "Q032_ABSOLUTE_CONFIG_PATH_GATE":absolute_path_gate,
      "SYNTHETIC_GEOMETRY_GATE":synthetic_geometry,
      "WITHIN_IMPLEMENTATION_REFERENCE_GATE":"LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION_ONLY" in text,
      "NO_CROSS_OBJECTIVE_GATE":"cross_likelihood_absolute_objective_subtraction_performed" in text and "cross_likelihood_objective_sum_performed" in text,
      "NO_FOREGROUND_ZERO_GATE":"zero foreground" not in text.lower(),
      "NO_CALIBRATION_INTERVENTION_GATE":"calibration_intervention_performed\": False" in text,
      "NO_PRECISION_INTERVENTION_GATE":"precision_intervention_performed\": False" in text,
      "PREREG_IDENTITY_GATE":prereg.get("project",{}).get("q")==Q and prereg.get("project",{}).get("program_id")==PROGRAM_ID,
      "SOURCE_LOCK_IDENTITY_GATE":source.get("q")==Q and source.get("program_id")==PROGRAM_ID,
      "STOP_RULE_GATE":prereg.get("stop_condition",{}).get("no_permutation_expansion") is True,
    }
    status="PASS" if all(gates.values()) else "FAIL"
    write(args.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"STATIC_TESTS","status":status,"gates":gates})
    return 0 if status=="PASS" else 2


def result(args):
    d=json.loads(Path(args.final).read_text(encoding="utf-8"))
    refs=d.get("reference_selection",{}).get("references",{})
    full=d.get("full_sample",{})
    loo=d.get("leave_one_label_out",{})
    sufficient_expected=bool(full.get("sufficient")) and len(loo)==9 and all(bool(x.get("sufficient")) for x in loo.values())
    classification_expected=(
        "SINGLE-BLOCK_NATIVE_FOREGROUND_PROFILE_FREEDOM_SUFFICIENT" if sufficient_expected
        else "NATIVE_FOREGROUND_PROFILE_FREEDOM_REJECTED_AS_SUFFICIENT"
    )
    metrics=full.get("metrics",{})
    finite_metrics=all(finite(metrics.get(k)) for k in ("matched_median","centroid","pairwise_median_drift"))
    loo_finite=(len(loo)==9 and all(all(finite(v.get("metrics",{}).get(k)) for k in ("matched_median","centroid","pairwise_median_drift")) for v in loo.values()))
    reference_gate=(set(refs)=={"camspec","hillipop"} and all(refs[i].get("selection_semantics")=="LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION_ONLY" for i in refs))
    gates={
      "Q_IDENTITY_GATE":d.get("q")==Q,
      "PROGRAM_ID_GATE":d.get("program_id")==PROGRAM_ID,
      "RUN_ID_GATE":d.get("run_id")==RUN_ID,
      "RESULT_ID_GATE":d.get("result_id")==RESULT_ID,
      "EXECUTION_COMPLETE_GATE":d.get("execution_status")=="COMPLETE",
      "PROFILE_COMPLETENESS_GATE":d.get("profile_count")==18 and d.get("expected_profile_count")==18,
      "REFERENCE_SELECTION_GATE":reference_gate,
      "FINITE_FULL_GEOMETRY_GATE":finite_metrics,
      "NINE_LOO_GATE":len(loo)==9 and loo_finite,
      "THRESHOLD_GATE":d.get("threshold")==0.10,
      "CLASSIFICATION_CONSISTENCY_GATE":d.get("classification")==classification_expected and bool(d.get("sufficient"))==sufficient_expected,
      "PROVISIONAL_GATE":d.get("final_result_gate")=="PROVISIONAL" and d.get("tests_status")=="PENDING_EXTERNAL_TEST_SCRIPT",
      "NO_CROSS_OBJECTIVE_GATE":d.get("cross_likelihood_absolute_objective_subtraction_performed") is False and d.get("cross_likelihood_objective_sum_performed") is False,
      "PREVIOUS_Q039_PRESERVED_GATE":d.get("previous_q039_results_preserved",{}).get("authoritative_run")==34161368438,
      "CORE_NOT_COMPARABLE_GATE":d.get("comparability",{}).get("CORE_LIKELIHOOD_CONSTRUCTION")=="NOT_COMPARABLE_AS_SINGLE_NATIVE_BLOCK",
      "NO_PHYSICAL_SYSTEMATIC_OVERCLAIM_GATE":any("not by itself establish physical foreground contamination" in x for x in d.get("interpretation_limits",[])),
    }
    status="PASS" if all(gates.values()) else "FAIL"
    write(args.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"RESULT_TESTS","status":status,"gates":gates,"FINAL_RESULT_GATE":status})
    return 0 if status=="PASS" else 2


def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    a=sp.add_parser("static"); a.add_argument("--program",required=True); a.add_argument("--preregister",required=True); a.add_argument("--source-lock",required=True); a.add_argument("--output",required=True); a.set_defaults(func=static)
    a=sp.add_parser("result"); a.add_argument("--final",required=True); a.add_argument("--output",required=True); a.set_defaults(func=result)
    args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=="__main__": main()
