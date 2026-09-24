#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,re
from pathlib import Path
Q="Q-042";PID="Q042-PREFLIGHT-V2"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def static(a):
 s=read(a.spec);l=read(a.source_lock);p=Path(a.program).read_text(encoding="utf-8");w=Path(a.workflow).read_text(encoding="utf-8");r=read(a.registry_patch)
 entry=r["entry"][PID]
 gates={
  "Q_IDENTITY":s.get("q")==Q and l.get("q")==Q and s.get("program_id")==PID and l.get("program_id")==PID,
  "SPEC_HASH":l.get("spec_sha256")==sha(a.spec),
  "20_CELL":s.get("authoritative_contract",{}).get("required_cell_count")==20,
  "POLYCHORD_FROZEN":s.get("polychord",{}).get("production_frozen",{}).get("nlive")=="25d" and s["polychord"]["production_frozen"]["num_repeats"]=="5d",
  "BOBYQA_EXTERNAL_STARTS":s.get("bobyqa",{}).get("production_frozen",{}).get("external_starts_per_cell")==4 and s["bobyqa"]["production_frozen"]["cobaya_best_of"]==1,
  "NO_Q040_IMPORT":"import q040" not in p.lower() and "from q040" not in p.lower(),
  "NO_SCIENCE_IN_PREFLIGHT":"scientific_classification\":\"NOT_AVAILABLE" in p.replace(" ","") or "scientific_classification\": \"NOT_AVAILABLE" in p,
  "WORKFLOW_IDENTITY":"PROGRAM_ID: Q042-PREFLIGHT-V2" in w and "CURRENT_Q: Q-042" in w,
  "WORKFLOW_FOUR_PILOTS":"camspec-lcdm" in w and "hillipop-ede" in w,
  "REGISTRY_ENTRY":entry.get("q")==Q and entry.get("status")=="ACTIVE" and entry.get("workflow_id")=="q042-planck-portability-v2.yml",
  "GITHUB_MUTATION_FORBIDDEN":l.get("github_mutation","").startswith("FORBIDDEN_BY_USER")
 }
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"STATIC_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V2_STATIC_TEST_GATE=PASS")
def final(a):
 d=read(a.result);mandatory=read(a.spec)["mandatory_preflight_gates"];g=d.get("gates",{})
 gates={"STATUS":d.get("status")=="PASS","NO_SCIENCE":d.get("scientific_classification")=="NOT_AVAILABLE" and d.get("actual_computed_scientific_result") is False,"PILOT_COUNT":d.get("pilot_count")==4,"MANDATORY":all(g.get(x)=="PASS" for x in mandatory)}
 status="PASS" if all(gates.values()) else "FAIL";write(a.output,{"q":Q,"program_id":PID,"stage":"FINAL_TESTS","status":status,"gates":{k:("PASS" if v else "FAIL") for k,v in gates.items()}})
 if status!="PASS":raise SystemExit(2)
 print("Q042_V2_FINAL_TEST_GATE=PASS")
def parser():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
 s=sp.add_parser("static")
 for x in ("spec","source-lock","program","workflow","registry-patch","output"):s.add_argument("--"+x,required=True)
 s.set_defaults(func=static)
 s=sp.add_parser("final");s.add_argument("--result",required=True);s.add_argument("--spec",required=True);s.add_argument("--output",required=True);s.set_defaults(func=final)
 return p
if __name__=="__main__":
 a=parser().parse_args();a.func(a)
