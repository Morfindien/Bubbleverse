#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,re
from pathlib import Path
Q="Q-042";PID="Q042-PREFLIGHT-V10"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def static(a):
 s=read(a.spec);l=read(a.source_lock);p=Path(a.program).read_text(encoding="utf-8");w=Path(a.workflow).read_text(encoding="utf-8");h=Path(a.core_helper).read_text(encoding="utf-8");r=read(a.registry_patch)
 entry=r["entry"][PID]
 gates={
  "Q_IDENTITY":s.get("q")==Q and l.get("q")==Q and s.get("program_id")==PID and l.get("program_id")==PID,
  "SPEC_HASH":l.get("spec_sha256")==sha(a.spec),
  "20_CELL":s.get("authoritative_contract",{}).get("required_cell_count")==20,
  "POLYCHORD_PRODUCTION_FROZEN":s.get("polychord",{}).get("production_frozen",{}).get("nlive")=="25d" and s["polychord"]["production_frozen"]["num_repeats"]=="5d" and s["polychord"]["production_frozen"]["precision_criterion"]==0.001 and s["polychord"]["production_frozen"]["max_ndead"]=="infinity",
  "POLYCHORD_SMOKE_BUDGET":s.get("polychord",{}).get("pilot",{}).get("nlive")=="1d" and s["polychord"]["pilot"]["num_repeats"]==4 and s["polychord"]["pilot"]["nprior"]=="nlive" and s["polychord"]["pilot"]["max_ndead"]==2,
  "BOBYQA_EXTERNAL_STARTS":s.get("bobyqa",{}).get("production_frozen",{}).get("external_starts_per_cell")==4 and s["bobyqa"]["production_frozen"]["cobaya_best_of"]==1,
  "NO_Q040_IMPORT":"import q040" not in p.lower() and "from q040" not in p.lower(),
  "NO_SCIENCE_IN_PREFLIGHT":"scientific_classification\":\"NOT_AVAILABLE" in p.replace(" ","") or "scientific_classification\": \"NOT_AVAILABLE" in p,
  "WORKFLOW_IDENTITY":"PROGRAM_ID: Q042-PREFLIGHT-V10" in w and "CURRENT_Q: Q-042" in w,
  "WORKFLOW_FOUR_PILOTS":"camspec-lcdm" in w and "hillipop-ede" in w,
  "OPENMPI_BUILD_TOOLCHAIN":"openmpi-bin" in w and "libopenmpi-dev" in w and "mpifort" in w,
  "V7_MPI_FAILURE_PRESERVED":"MPI_Comm_dup" in l.get("known_method_risks",{}).get("q042_v7_mpi_resume_failure","") and l.get("technical_repairs",{}).get("v8_process_isolation",{}).get("science_changed") is False,
  "EXACT_V19_BASE_CACHE":"q041-v19-${{ runner.os }}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36" in w,
  "V9_OR_V7_CACHE_REUSE":("q042-v9-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus" in w) or ("q042-v7-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus" in w),
  "SEPARATE_POLYCHORD_CACHE":"q042-v6-polychord-${{ runner.os }}-py311-pc1222" in w and "q042-v5-polychord-${{ runner.os }}-py311-pc1222" in w and "q042-v4-polychord-${{ runner.os }}-py311-pc1222" in w and "path: external/PolyChordLite" in w,
  "Q042_CORE_HELPER_REUSED":"q042_prepare_frozen_core_v4.sh both" in w and "bash q041_prepare_frozen_core_v19.sh both" not in w,
  "NO_SHORT_NERSC_PROBE":"--range 0-0" not in h and "NERSC_TT_AVAILABILITY_GATE" not in h,
  "BOUNDED_OFFICIAL_HILLIPOP_INSTALL":"timeout --signal=TERM --kill-after=30s 1800s cobaya-install planck_2020_hillipop.TT" in h and "attempt=$i/3" in h,
  "PILOT_CACHE_FAIL_CLOSED":"q042-v10-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus" in w and "fail-on-cache-miss: true" in w,
  "EXTERNAL_IDENTITY_SCOPE_REPAIR":"COMMON_EXTERNAL_COMPONENTS" in p and "external_science_signature" in p and "native_auxiliary_likelihoods" in p and "EXTERNAL_COMPONENT_SET_GATE" in p and "ACT_CALIBRATION_CONTRACT_GATE" in p,
  "POLYCHORD_PROCESS_ISOLATION":"polychord-stage" in p and "POLYCHORD_RESUME_FRESH_PROCESS_GATE" in p and "FRESH_PROCESS_PER_POLYCHORD_INVOCATION" in p and "subprocess.run" in p,
  "POLYCHORD_RESUME_STORED_INFO":"OutputReadOnly" in p and "COBAYA_STORED_UPDATED_INFO" in p and "POLYCHORD_RESUME_STORED_INFO_GATE" in p and "allow_changes=True" not in p,
  "POLYCHORD_RESUME_PATCH_REINSTALL":"built_info,_=build_info" in p and "stored=OutputReadOnly" in p,
  "POLYCHORD_RESUME_CONTRACT_HASH":"requested_sampler_contract_sha256" in p and "POLYCHORD_RESUME_SAMPLER_CONTRACT_GATE" in p,
  "BOBYQA_PROCESS_ISOLATION":"bobyqa-stage" in p and "FRESH_PROCESS_PER_EXTERNAL_START" in p and "q042_bobyqa_start" in p,
  "BOBYQA_MAXFUN_POLICY":s.get("bobyqa",{}).get("pilot",{}).get("max_evals")==60 and "EXIT_MAXFUN_WARNING is acceptable" in s.get("bobyqa",{}).get("pilot",{}).get("acceptable_exit","") and "_bobyqa_wrapper_exception_record" in p and "ACCEPTED_MAXFUN_WARNING" in p and "flag>=0" in p.replace(" ",""),
  "BOBYQA_NEGATIVE_FLAGS_REJECTED":"REJECTED_NEGATIVE_OR_UNPARSED_FLAG" in p and "technical_ok=bool(objectiveisnotNoneandflagisnotNoneandflag>=0)" in p.replace(" ",""),
  "NO_INPROCESS_POLYCHORD_RESUME_IN_PILOT":"_,rs=cobaya_run" not in p and "cobaya_run(resume_info" not in p,
  "WORKFLOW_SELF_REFERENCE":"--workflow .github/workflows/q042-planck-portability-v10.yml" in w,
  "WORKFLOW_REGISTRY_PATCH_SELF_REFERENCE":"--registry-patch q042_program_registry_patch_v10.json" in w and "--registry-patch q042_program_registry_patch_v7.json" not in w and "--registry-patch q042_program_registry_patch_v6.json" not in w,
  "NO_ACTIVE_STALE_V9_REFERENCES":not any(x in p or x in w for x in ("q042_v9_cell_preflight","q042_bobyqa_start{start_index}_v9.json","name: q042-pilot-${{ matrix.id }}-v9","q042_preflight_tests_v9.json","q042_pilot_result_v9.json","q042_runtime_preflight_v9.json")),
  "ACTIVE_V10_WORKFLOW_OUTPUTS":all(x in w for x in ("q042_static_program_v10.json","q042_static_tests_v10.json","q042_primary_nonoverlap_support_v10.json","q042_hillipop_nonoverlap_precision_v10.npy","q042_runtime_preflight_v10.json","q042_preflight_final_v10.json")),
  "PILOT_RESULT_VERSION":"q042_pilot_result_v10.json" in p and all(x not in p for x in ("q042_pilot_result_v4.json","q042_pilot_result_v5.json","q042_pilot_result_v6.json","q042_pilot_result_v7.json")),
  "REGISTRY_ARTIFACT_VERSION":all(str(x).endswith("v10") or "*-v10" in str(x) for x in entry.get("result_artifacts",[])) and len(entry.get("result_artifacts",[]))==4,
  "REGISTRY_ENTRY":entry.get("q")==Q and entry.get("status")=="ACTIVE" and entry.get("workflow_id")=="q042-planck-portability-v10.yml",
  "REGISTRY_CORE_HELPER":entry.get("frozen_core_helper")=="q042_prepare_frozen_core_v4.sh",
  "GITHUB_MUTATION_FORBIDDEN":l.get("github_mutation","").startswith("FORBIDDEN_BY_USER")
 }
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V10_STATIC_TEST_GATE=PASS")
def final(a):
 d=read(a.result);mandatory=read(a.spec)["mandatory_preflight_gates"];g=d.get("gates",{})
 gates={"STATUS":d.get("status")=="PASS","NO_SCIENCE":d.get("scientific_classification")=="NOT_AVAILABLE" and d.get("actual_computed_scientific_result") is False,"PILOT_COUNT":d.get("pilot_count")==4,"MANDATORY":all(g.get(x)=="PASS" for x in mandatory)}
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V10_FINAL_TEST_GATE=PASS")
def parser():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
 s=sp.add_parser("static")
 for x in ("spec","source-lock","program","workflow","registry-patch","core-helper","output"):s.add_argument("--"+x,required=True)
 s.set_defaults(func=static)
 s=sp.add_parser("final");s.add_argument("--result",required=True);s.add_argument("--spec",required=True);s.add_argument("--output",required=True);s.set_defaults(func=final)
 return p
if __name__=="__main__":
 a=parser().parse_args();a.func(a)
