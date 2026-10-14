#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from q048_p3_scaled_arithmetic_v2 import table_log_union,primary_exp_point,control_exp_point

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

raw=json.loads((HERE/'q048_p3_scaled_raw_result_v2.json').read_text())
trans=json.loads((HERE/'q048_p3_scaled_transformed_log_tables_v2.json').read_text())
cfg=json.loads((HERE/'q048_p3_scaled_config_v2.json').read_text())
checks={}
checks['status_pass']=raw['status']=='PASS_BOUNDED_COMPONENT'
checks['stop_reason_pass']=raw['stop_reason']=='BOUNDED_P3_V2_OPERATOR_ADMISSION_QUALIFIED'
checks['all_recorded_checks_pass']=all(c['pass'] for c in raw['checks'])
checks['recorded_check_count_551']=len(raw['checks'])==551
checks['proofcells_30']=raw['proofcells']==30
checks['transforms_16100']=raw['table_node_transforms']==16100
checks['within_compute_cap']=raw['within_compute_cap'] is True and raw['proof_compute_seconds']<=cfg['budget_seconds']
checks['serialized_alpha_count']=len(trans['Alpha_inf.dat']['log_bounds_integer'])==16000
checks['serialized_R_count']=len(trans['R_inf.dat']['log_bounds_integer'])==100
checks['serialized_hash_matches_result']=sha(HERE/'q048_p3_scaled_transformed_log_tables_v2.json')==raw['transformed_tables_sha256']
checks['all_serialized_intervals_ordered']=all(int(a)<=int(b) for rec in trans.values() for a,b in rec['log_bounds_integer'])
checks['all_atomic_primary_positive']=all(F(v['rate_range']['lo'])>0 for v in raw['atomic_global_admission'].values())
checks['all_atomic_control_positive']=all(F(v['control_rate_range']['lo'])>0 for v in raw['atomic_global_admission'].values())
checks['all_fit_primary_denominators_positive']=all(F(v['primary_denominator']['lo'])>0 for v in raw['fit_cases'].values())
checks['all_fit_control_denominators_positive']=all(F(v['control_denominator']['lo'])>0 for v in raw['fit_cases'].values())
# Independent exact R0 re-evaluation from source token.
tok=(ROOT/'p3deps/R_inf.dat').read_text().split()[0]
rec=table_log_union(tok)
pL=primary_exp_point(rec['lo']);pU=primary_exp_point(rec['hi'])
cL=control_exp_point(rec['lo']);cU=control_exp_point(rec['hi'])
checks['R0_primary_lower_strict']=pL.hi_fraction<rec['qlo']
checks['R0_primary_upper_strict']=pU.lo_fraction>rec['qhi']
checks['R0_control_lower_strict']=cL.hi_fraction<rec['qlo']
checks['R0_control_upper_strict']=cU.lo_fraction>rec['qhi']
checks['no_full_Q_claim']=raw['x_e_tau_T_first_event']=='UNRESOLVED' and raw['native_P6']=='UNRESOLVED'
passed=sum(checks.values())
out={
 'schema':'bubbleverse.builder.local_validation',
 'schema_version':'UNVALIDATED_LOCAL_CONTRACT',
 'result_id':raw['result_id'],
 'raw_result_sha256':sha(HERE/'q048_p3_scaled_raw_result_v2.json'),
 'transformed_tables_sha256':sha(HERE/'q048_p3_scaled_transformed_log_tables_v2.json'),
 'tests_log_sha256':sha(HERE/'q048_p3_scaled_tests_v2.log'),
 'reproduction_log_sha256':sha(HERE/'q048_p3_scaled_reproduction_v2.log'),
 'checks':checks,
 'check_summary':{'passed':passed,'total':len(checks)},
 'decision':'PASS_BOUNDED_COMPONENT' if passed==len(checks) else 'VALIDATION_FAIL',
 'scope':'bounded conditional source-real P3 V2 operator admission only',
 'limitations':raw['limitations']
}
(HERE/'q048_p3_scaled_validation_v2.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'decision':out['decision'],'passed':passed,'total':len(checks),
                  'raw_result_sha256':out['raw_result_sha256'],
                  'transformed_tables_sha256':out['transformed_tables_sha256']},indent=2))
raise SystemExit(0 if out['decision']=='PASS_BOUNDED_COMPONENT' else 1)
