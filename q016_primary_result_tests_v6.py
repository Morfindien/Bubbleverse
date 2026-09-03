#!/usr/bin/env python3
import argparse,json
from pathlib import Path
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--merged",required=True); ap.add_argument("--output",required=True)
 a=ap.parse_args(); d=json.loads(Path(a.merged).read_text())
 gates=d.get("gates",{})
 primary=bool(d.get("scientifically_usable_primary_endpoint_result")) and all(bool(v) for v in gates.values())
 out={
  "q":"Q016","run_id":"Q016-MATCHED-CMB-SURFACE-V6","result_id":"R-Q016-EDE-MATCHED-CMB-SURFACE-006",
  "stage":"PRIMARY_ENDPOINT_CERTIFICATION",
  "PRIMARY_ENDPOINT_GATE":"PASS" if primary else "FAIL",
  "FINAL_RESULT_GATE":"PENDING_LATER_STAGES",
  "remaining_mandatory_work":[
    "covariance-aware TT/TE/EE and multipole-band attribution",
    "residual-vector and delta-residual comparison across Planck/SPT/ACT",
    "secondary ell=1000-2000 full-vs-lite/frequency/nuisance mechanism tests",
    "COMMON_RESIDUAL_DECISION_GATE"
  ],
  "scientific_result":"PRIMARY_ENDPOINTS_CERTIFIED_Q016_CONTINUES" if primary else "PRIMARY_ENDPOINTS_NOT_CERTIFIED",
  "gates":gates
 }
 dump(a.output,out)
 if not primary: raise SystemExit(2)
if __name__=="__main__":main()
