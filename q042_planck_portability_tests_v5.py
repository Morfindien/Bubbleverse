#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,re
from pathlib import Path
Q="Q-042";PID="Q042-PREFLIGHT-V5"
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
  "POLYCHORD_FROZEN":s.get("polychord",{}).get("production_frozen",{}).get("nlive")=="25d" and s["polychord"]["production_frozen"]["num_repeats"]=="5d",
  "BOBYQA_EXTERNAL_STARTS":s.get("bobyqa",{}).get("production_frozen",{}).get("external_starts_per_cell")==4 and s["bobyqa"]["production_frozen"]["cobaya_best_of"]==1,
  "NO_Q040_IMPORT":"import q040" not in p.lower() and "from q040" not in p.lower(),
  "NO_SCIENCE_IN_PREFLIGHT":"scientific_classification\":\"NOT_AVAILABLE" in p.replace(" ","") or "scientific_classification\": \"NOT_AVAILABLE" in p,
  "WORKFLOW_IDENTITY":"PROGRAM_ID: Q042-PREFLIGHT-V5" in w and "CURRENT_Q: Q-042" in w,
  "WORKFLOW_FOUR_PILOTS":"camspec-lcdm" in w and "hillipop-ede" in w,
  "OPENMPI_BUILD_TOOLCHAIN":"openmpi-bin" in w and "libopenmpi-dev" in w and "mpifort" in w,
  "V4_FAILURE_PRESERVED":l.get("technical_parent",{}).get("program_id")=="Q042-PREFLIGHT-V4" and l.get("technical_parent",{}).get("scientific_result")=="NONE",
  "EXACT_V19_BASE_CACHE":"q041-v19-${{ runner.os }}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36" in w,
  "V4_CACHE_REUSE":"q042-v4-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus" in w and "restore-keys:" in w,
  "SEPARATE_POLYCHORD_CACHE":"q042-v5-polychord-${{ runner.os }}-py311-pc1222" in w and "q042-v4-polychord-${{ runner.os }}-py311-pc1222" in w and "path: external/PolyChordLite" in w,
  "Q042_CORE_HELPER_REUSED":"q042_prepare_frozen_core_v4.sh both" in w and "bash q041_prepare_frozen_core_v19.sh both" not in w,
  "NO_SHORT_NERSC_PROBE":"--range 0-0" not in h and "NERSC_TT_AVAILABILITY_GATE" not in h,
  "BOUNDED_OFFICIAL_HILLIPOP_INSTALL":"timeout --signal=TERM --kill-after=30s 1800s cobaya-install planck_2020_hillipop.TT" in h and "attempt=$i/3" in h,
  "PILOT_CACHE_FAIL_CLOSED":"q042-v5-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus" in w and "fail-on-cache-miss: true" in w,
  "EXTERNAL_IDENTITY_SCOPE_REPAIR":"COMMON_EXTERNAL_COMPONENTS" in p and "external_science_signature" in p and "native_auxiliary_likelihoods" in p and "EXTERNAL_COMPONENT_SET_GATE" in p and "ACT_CALIBRATION_CONTRACT_GATE" in p,
  "REGISTRY_ENTRY":entry.get("q")==Q and entry.get("status")=="ACTIVE" and entry.get("workflow_id")=="q042-planck-portability-v5.yml",
  "GITHUB_MUTATION_FORBIDDEN":l.get("github_mutation","").startswith("FORBIDDEN_BY_USER")
 }
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V5_STATIC_TEST_GATE=PASS")
def final(a):
 d=read(a.result);mandatory=read(a.spec)["mandatory_preflight_gates"];g=d.get("gates",{})
 gates={"STATUS":d.get("status")=="PASS","NO_SCIENCE":d.get("scientific_classification")=="NOT_AVAILABLE" and d.get("actual_computed_scientific_result") is False,"PILOT_COUNT":d.get("pilot_count")==4,"MANDATORY":all(g.get(x)=="PASS" for x in mandatory)}
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V5_FINAL_TEST_GATE=PASS")
def parser():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
 s=sp.add_parser("static")
 for x in ("spec","source-lock","program","workflow","registry-patch","core-helper","output"):s.add_argument("--"+x,required=True)
 s.set_defaults(func=static)
 s=sp.add_parser("final");s.add_argument("--result",required=True);s.add_argument("--spec",required=True);s.add_argument("--output",required=True);s.set_defaults(func=final)
 return p
if __name__=="__main__":
 a=parser().parse_args();a.func(a)
