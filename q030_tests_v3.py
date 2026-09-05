#!/usr/bin/env python3
"""Mandatory Q030 V3 validation-only repair tests."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml

Q='Q030'
RUN='Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V3'
RESULT='R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-003'
COMMON_SHA='6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63'
EXPECTED_MASK_HASHES={
 '3':'993426ef2b63a9197844a9b7526f2e72a162b7470752ba2b7ad21a006c3b3913',
 '6':'51220e4ef4ed71f4e65d0337d98554c86a014fba573fe773629ca83ba0744a08',
 '7':'e9d6eb8cab66e66599cdf475fe9a22394d9ab4d5365889e75ed0d297fa111968',
}

def load(p): return json.loads(Path(p).read_text())
def check(name, ok, detail=None): return {'test':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def finite(x):
 try: return math.isfinite(float(x))
 except Exception: return False

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--config',required=True); ap.add_argument('--result',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
 c=yaml.safe_load(Path(a.config).read_text()); r=load(a.result); v=c['validation']; ts=[]
 ts.append(check('T001_Q_RUN_RESULT_IDENTITY', r.get('q')==Q and r.get('run_id')==RUN and r.get('result_id')==RESULT and r.get('status')=='COMPLETE'))
 cs=r.get('common_support',{}); ts.append(check('T002_EXACT_Q028_COMMON_SUPPORT', int(cs.get('dimension',-1))==9915 and cs.get('keys_sha256')==COMMON_SHA, cs))
 ts.append(check('T003_V3_ZERO_NEW_SCIENTIFIC_EXECUTION', all(int(r.get(k,-1))==0 for k in ['v3_additional_model_initializations','v3_additional_likelihood_evaluations','v3_additional_optimizer_evaluations','v3_additional_sampling_evaluations','v3_additional_q024_permutations'])))
 src=r.get('source_numerical_result',{}); ts.append(check('T004_V2_MASK_BIT_IMMUTABILITY', src.get('github_run_id')==33961469874 and src.get('head_sha')=='c0d01b8cd9ecc533b37cf82e89710595ff9a34a2' and src.get('mask_json_sha256')==EXPECTED_MASK_HASHES, src))
 ds=r.get('diagnostics',[]); ids={(int(d['mask']),d['edge']) for d in ds}; exp={(m,e) for m in (3,6,7) for e in ('e01','e02','e12')}; ts.append(check('T005_NINE_DIAGNOSTIC_COMPLETENESS',len(ds)==9 and ids==exp,sorted(ids)))
 maxid=max(abs(float(d['Q029_identity_closure_error'])) for d in ds); tol=float(v['q029_identity_closure_abs_tol']); ts.append(check('T006_Q029_IDENTITY_FLOAT64_CLOSURE',finite(maxid) and maxid<=tol,{'max_abs_error':maxid,'tol':tol}))
 maxdm=max(abs(float(d['delta2m_equals_minus_delta2r_max_abs_error'])) for d in ds); dmtol=float(v['delta_m_identity_abs_tol']); ts.append(check('T007_DELTA2M_EQUALS_MINUS_DELTA2R',finite(maxdm) and maxdm<=dmtol,{'max_abs_error':maxdm,'tol':dmtol}))
 maxparent=max(abs(float(d['Q028_parent_closure_error'])) for d in ds); ptol=float(v['q028_parent_interaction_abs_tol']); ts.append(check('T008_Q028_PARENT_FUNCTIONAL_CLOSURE',finite(maxparent) and maxparent<=ptol,{'max_abs_error':maxparent,'tol':ptol}))
 agg=[]
 for d in ds:
  for mode,dist in d['distributions'].items():
   for term,err in dist['closure_error_vs_total'].items(): agg.append((d['mask'],d['edge'],mode,term,abs(float(err))))
 worst=max(agg,key=lambda x:x[-1]); atol=float(v['aggregation_closure_abs_tol']); ts.append(check('T009_GROUP_PAIR_FLOAT64_CLOSURE',finite(worst[-1]) and worst[-1]<=atol,{'worst':worst,'tol':atol}))
 rep=r.get('validation_repair',{}); ts.append(check('T010_REPAIR_IS_VALIDATION_ONLY',rep.get('type')=='FLOAT64_CANCELLATION_TOLERANCE_CALIBRATION_ONLY' and rep.get('scientific_values_changed') is False and rep.get('mask_artifacts_changed') is False and rep.get('common_support_changed') is False and rep.get('interpretation_changed') is False,rep))
 boundary=all(d['interpretation_boundary'].get('T_DM_is_data_only_contribution') is False and d['interpretation_boundary'].get('T_MM_is_physical_model_cause') is False and d['interpretation_boundary'].get('physical_causality_claimed') is False and d['interpretation_boundary'].get('cosmology_calibration_allocation_performed') is False and d['interpretation_boundary'].get('shapley_identification_used') is False for d in ds); ts.append(check('T011_NO_CAUSAL_OR_IDENTIFICATION_OVERCLAIM',boundary))
 finiteok=all(all(finite(x) for x in d['terms'].values()) and finite(d['F_direct_from_residual_quadratic']) for d in ds); ts.append(check('T012_FINITE_RESULT_GATE',finiteok))
 ok=all(t['status']=='PASS' for t in ts); out={'q':Q,'run_id':RUN,'result_id':RESULT,'tests':ts,'test_count':len(ts),'FINAL_RESULT_GATE':'PASS' if ok else 'FAIL'}; Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print('FINAL_RESULT_GATE='+out['FINAL_RESULT_GATE']); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
