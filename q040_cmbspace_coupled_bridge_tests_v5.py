#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path

def load_module(path:Path):
 spec=importlib.util.spec_from_file_location('q040v5',path); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m

def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument('--program',default='q040_cmbspace_coupled_bridge_v5.py'); ap.add_argument('--preregister',default='q040_cmbspace_coupled_bridge_preregister_v5.json'); ap.add_argument('--source-lock',default='q040_cmbspace_coupled_bridge_source_lock_v5.json'); ap.add_argument('--map-dir'); ap.add_argument('--failure-dir'); ap.add_argument('--final'); ap.add_argument('--output',required=True); a=ap.parse_args()
 m=load_module(Path(a.program)); gates={}
 def gate(n,c): gates[n]='PASS' if c else 'FAIL';
 gate('Q_IDENTITY_GATE',m.Q=='Q-040'); gate('PROGRAM_ID_GATE',m.PROGRAM_ID=='Q040-CMBSPACE-V5'); gate('V4_RUN_LOCK_GATE',m.V4_GITHUB_RUN_ID==34211073134); gate('Q032_RUN_LOCK_GATE',m.Q032_GITHUB_RUN_ID==33994305721); gate('SUPPORT_HASH_GATE',m.SUPPORT_HASH=='f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b'); gate('REPRESENTATION_HASH_GATE',m.REPRESENTATION_HASH=='f96e2b9cdc27501eb0f2a6aabbf6c79c8d681f1af2d55c54b495b513c1da1f48'); gate('HILLIPOP_MULTISTART_THRESHOLD_GATE',m.MULTISTART_CMB_RMS_MAX==0.10); gate('GEOMETRY_THRESHOLD_GATE',m.GEOMETRY_SUFFICIENCY_THRESHOLD==0.10); gate('CAMSPEC_NATIVE_BOUND_GATE',m.CAMSPEC_AMP143_UPPER==50.0 and m.CAMSPEC_AMP143_PROPOSAL==1.0); gate('NO_THRESHOLD_RELAXATION_STATIC_GATE',m.ACTIVE_BOUND_PROPOSAL_TOL==0.001)
 try: m.load_preregister(a.preregister); gate('PREREGISTRATION_GATE',True)
 except Exception: gate('PREREGISTRATION_GATE',False)
 try: m.load_source_lock(a.source_lock); gate('SOURCE_LOCK_GATE',True)
 except Exception: gate('SOURCE_LOCK_GATE',False)
 if a.map_dir and a.failure_dir:
  try:
   ev=m.evaluate(a.map_dir,a.failure_dir); gate('REAL_V4_ARTIFACT_EVALUATION_GATE',True); gate('CAMSPEC_CONTROLLED_FAILURE_GATE',ev['gates']['CAMSPEC_SYMMETRIC_LAPLACE_BOUNDARY_COMPATIBILITY_GATE']=='FAIL' and ev['gates']['CAMSPEC_NUISANCE_HESSIAN_PD_GATE']=='FAIL'); gate('HILLIPOP_CONTROLLED_FAILURE_GATE',ev['gates']['HILLIPOP_COMPRESSION_MULTISTART_GATE']=='FAIL'); gate('SCIENCE_ENDPOINT_BLOCK_GATE',ev['gates']['SCIENCE_ENDPOINT_PERMISSION_GATE']=='FAIL')
  except Exception as e: gate('REAL_V4_ARTIFACT_EVALUATION_GATE',False); gates['artifact_error']=repr(e)
 if a.final:
  try:
   d=json.load(open(a.final)); gate('FINAL_CLASSIFICATION_GATE',d.get('classification')=='COMPRESSION_VALIDATION_FAIL'); gate('FINAL_RESULT_UNRESOLVED_GATE',d.get('final_result_gate')=='UNRESOLVED'); gate('NO_SCIENCE_ENDPOINT_GATE',d.get('science_endpoints_executed') is False and d.get('science_endpoints_permitted') is False)
  except Exception as e: gate('FINAL_FILE_GATE',False); gates['final_error']=repr(e)
 ok=all(v=='PASS' for k,v in gates.items() if k.endswith('_GATE'))
 out={'q':m.Q,'program_id':m.PROGRAM_ID,'status':'PASS' if ok else 'FAIL','gates':gates}; Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(f"Q040_V5_TESTS={'PASS' if ok else 'FAIL'} gates={sum(v=='PASS' for v in gates.values())}"); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
