#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

EXPECTED = "CLASSIFIER_SEMANTICS_MATERIALLY_EXPLAINS_REPORTED_DISCREPANCY"

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--result',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    r=json.loads(Path(a.result).read_text(encoding='utf-8'))
    gates={}
    gates['Q_IDENTITY_GATE']=r.get('q')=='Q-035'
    gates['RESULT_IDENTITY_GATE']=r.get('result_id')=='R-Q035-EDE-CLASSIFIER-HARMONIZATION-001'
    gates['ARTIFACT_ONLY_GATE']=r.get('new_likelihood_evaluations')==0 and r.get('new_optimizer_runs')==0 and r.get('new_sampler_runs')==0
    gates['REFERENCE_REPLAY_GATE']=all(x.get('pass') is True for x in r.get('reference_replay_gates',{}).values())
    cw=r.get('crosswalk',{})
    gates['ENDPOINT_COMPLETENESS_GATE']=set(cw)=={'Q022','Q032','Q034'} and all(cw[k].get('endpoint_count')==9 for k in cw)
    gates['HISTORICAL_ALL_STABLE_GATE']=all(cw[k]['historical_q022']['stable_multibasin'] is True for k in cw)
    gates['LATER_ALL_NONSTABLE_GATE']=all(cw[k]['later_common_graph']['stable_basin_count']==0 and cw[k]['later_common_graph']['stable_multibasin'] is False and len(cw[k]['later_common_graph']['clusters'])==9 for k in cw)
    gates['ALL_ENDPOINTSETS_FLIP_GATE']=r.get('decision_diagnostics',{}).get('all_endpointsets_flip_between_classifiers') is True
    gates['SAME_CLASSIFIER_DISCREPANCY_REMOVED_GATE']=(r.get('decision_diagnostics',{}).get('historical_same_classifier_cross_case_discrepancy') is False and r.get('decision_diagnostics',{}).get('later_same_classifier_cross_case_discrepancy') is False)
    gates['FINAL_CLASSIFICATION_GATE']=r.get('classification')==EXPECTED
    gates['PHYSICAL_SAFETY_GATE']=not any(r.get('physical_interpretation_boundaries',{}).values())
    passed=all(gates.values())
    out={'q':'Q-035','run_id':r.get('run_id'),'result_id':r.get('result_id'),'stage':'Q035_MANDATORY_TESTS','status':'PASS' if passed else 'FAIL','gates':gates,'FINAL_RESULT_GATE':'PASS' if passed else 'FAIL'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('FINAL_RESULT_GATE='+out['FINAL_RESULT_GATE'])
    return 0 if passed else 2

if __name__=='__main__': raise SystemExit(main())
