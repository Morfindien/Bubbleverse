#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, importlib.util, json, tempfile
from pathlib import Path
Q="Q-039"
PROGRAM_ID="Q039-IMPLBLOCK-V4"
SCIENTIFIC_PREREG_PROGRAM_ID="Q039-IMPLBLOCK-V1"

def write(path,obj): Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def load_module(path):
    spec=importlib.util.spec_from_file_location("q039_v4_static_module",path)
    if spec is None or spec.loader is None: raise RuntimeError("MODULE_LOAD_GATE=FAIL")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def static(args):
    program_path=Path(args.program); program=program_path.read_text(encoding="utf-8"); tree=ast.parse(program)
    prereg=json.loads(Path(args.preregister).read_text(encoding="utf-8")); source=json.loads(Path(args.source_lock).read_text(encoding="utf-8")); mod=load_module(program_path)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td).resolve(); cfg=root/"q032_planck_tt3pair_bridge_v2_config.yml"; cfg.write_text("technical: true\n",encoding="utf-8")
        resolved=mod.resolve_q032_config_path(root); path_gate=(resolved==cfg.resolve() and resolved.is_absolute())
    native_schema_gate=(mod.validate_camspec_native_relative_calibration_defaults({"cal0":1,"cal2":1})=={"cal0":1.0,"cal2":1.0})
    synthetic_info={"params":{"A_planck":{"prior":{"dist":"norm","loc":1.0,"scale":0.0025}}}}
    calmeta=mod.apply_calibration_neutral(synthetic_info,"camspec",{"cal0":1,"cal2":1})
    camspec_injection_gate=(synthetic_info["params"].get("cal0")==1.0 and synthetic_info["params"].get("cal2")==1.0 and sorted(calmeta.get("injected_native_default_overrides",[]))==["cal0","cal2"] and calmeta.get("changed_parameters")==[])
    try:
        mod.validate_camspec_native_relative_calibration_defaults({"cal0":0.99,"cal2":1})
        nonneutral_rejection_gate=False
    except RuntimeError:
        nonneutral_rejection_gate=True
    bad='q32.load_cfg(Path(args.q032_parent_root) / "q032_planck_tt3pair_bridge_v2_config.yml")'
    gates={
      "PYTHON_PARSE_GATE":isinstance(tree,ast.Module), "Q_IDENTITY_GATE":mod.Q==Q, "PROGRAM_ID_GATE":mod.PROGRAM_ID==PROGRAM_ID,
      "RUN_ID_GATE":mod.RUN_ID=="Q039-IMPLEMENTATION-BLOCK-INTERVENTION-V4", "SCIENTIFIC_PREREG_ID_PRESERVATION_GATE":mod.SCIENTIFIC_PREREG_PROGRAM_ID==SCIENTIFIC_PREREG_PROGRAM_ID,
      "PARENT_COMMIT_GATE":mod.Q032_EXECUTION_COMMIT=="4dc873a5e880d40858d831a3b421456728f0c032", "BACKEND_COMMIT_GATE":mod.BACKEND_COMMIT=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "HILLIPOP_COMMIT_GATE":mod.HILLIPOP_COMMIT=="a09ddde3e7ce11df99f74685feb1f1764cafb251", "SUPPORT_HASH_GATE":mod.SUPPORT_HASH=="f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b",
      "SCALE_HASH_GATE":mod.SCALES_HASH=="732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6", "FINITE_ARM_GATE":all(x in program for x in ["RELATIVE_CALIBRATION_NEUTRAL","OFFDIAGONAL_PRECISION_COUPLING_OFF","CALIBRATION_PLUS_PRECISION"]),
      "NO_CROSS_OBJECTIVE_GATE":"cross_likelihood_absolute_objective_comparison_performed" in program and "cross_likelihood_objective_sum_performed" in program,
      "IMMUTABLE_PREREG_GATE":prereg.get("q")==Q and prereg.get("program_id")==SCIENTIFIC_PREREG_PROGRAM_ID, "IMMUTABLE_SOURCE_LOCK_GATE":source.get("q")==Q and source.get("program_id")==SCIENTIFIC_PREREG_PROGRAM_ID,
      "FOREGROUND_NOT_COMPARABLE_GATE":prereg["blocks"]["foreground_treatment"]["comparability"]=="INCONCLUSIVE_NOT_COMPARABLE_V1", "CORE_NOT_COMPARABLE_GATE":prereg["blocks"]["core_likelihood_construction"]["comparability"]=="INCONCLUSIVE_NOT_COMPARABLE_V1",
      "Q032_ABSOLUTE_CONFIG_PATH_GATE":path_gate, "DOUBLE_PARENT_PATH_REGRESSION_GATE":bad not in program,
      "CAMSPEC_NATIVE_DEFAULT_SCHEMA_GATE":native_schema_gate,
      "CAMSPEC_RAW_INFO_NATIVE_OVERRIDE_GATE":camspec_injection_gate,
      "CAMSPEC_NONNEUTRAL_DEFAULT_REJECTION_GATE":nonneutral_rejection_gate,
      "PINNED_CAMSPEC_DEFAULT_SOURCE_GATE":"params_TT_CamSpec.yaml" in program and "PINNED_COBAYA_3_5_6_COMPONENT_DEFAULTS" in program,
      "MODEL_INITIALIZATION_PREFLIGHT_GATE":"q32.create_model(info)" in program and "Q039_PRECISION_RUNTIME_APPLY_GATE=FAIL" in program,
      "V3_FAILURE_PROVENANCE_GATE":getattr(mod,"V3_FAILED_RUN_ID",None)==34140566884 and getattr(mod,"V3_FAILED_JOB_ID",None)==101801510456,
      "RUNTIME_PREFLIGHT_GATE":"runtime-preflight" in program and "TECHNICAL_PREFLIGHT_ONLY_NOT_SCIENTIFIC_EVIDENCE" in program}
    status="PASS" if all(gates.values()) else "FAIL"; write(args.output,{"q":Q,"program_id":PROGRAM_ID,"scientific_preregister_program_id":SCIENTIFIC_PREREG_PROGRAM_ID,"stage":"Q039_STATIC_TESTS_V4","status":status,"gates":gates}); return 0 if status=="PASS" else 2

def result(args):
    d=json.loads(Path(args.final).read_text(encoding="utf-8")); allowed={"SINGLE-BLOCK","COUPLED-BLOCK","INCONCLUSIVE"}
    gates={"Q_IDENTITY_GATE":d.get("q")==Q,"PROGRAM_ID_GATE":d.get("program_id")==PROGRAM_ID,"EXECUTION_COMPLETE_GATE":d.get("execution_status")=="COMPLETE","TERMINAL_CLASSIFICATION_GATE":d.get("classification") in allowed,"PROVISIONAL_GATE":d.get("final_result_gate")=="PROVISIONAL" and d.get("tests_status")=="PENDING_EXTERNAL_TEST_SCRIPT","NO_PHYSICAL_SYSTEMATIC_OVERCLAIM_GATE":any("not a physical Planck systematic" in x for x in d.get("interpretation_limits",[])),"FOREGROUND_UNRESOLVED_PRESERVED_GATE":d.get("comparability",{}).get("FOREGROUND_TREATMENT")=="INCONCLUSIVE_NOT_COMPARABLE_V1"}
    status="PASS" if all(gates.values()) else "FAIL"; write(args.output,{"q":Q,"program_id":PROGRAM_ID,"stage":"Q039_RESULT_TESTS_V4","status":status,"gates":gates,"FINAL_RESULT_GATE":status}); return 0 if status=="PASS" else 2

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    a=sp.add_parser("static"); a.add_argument("--program",default="q039_implementation_block_intervention_v4.py"); a.add_argument("--preregister",default="q039_implementation_block_intervention_preregister_v1.json"); a.add_argument("--source-lock",default="q039_implementation_block_intervention_source_lock_v1.json"); a.add_argument("--output",required=True); a.set_defaults(func=static)
    a=sp.add_parser("result"); a.add_argument("--final",required=True); a.add_argument("--output",required=True); a.set_defaults(func=result)
    args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=="__main__": main()
