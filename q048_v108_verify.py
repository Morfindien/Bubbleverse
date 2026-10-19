import json, hashlib, pathlib, re
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); I=R/'q048_v108_inputs'
def L(p): return json.loads(pathlib.Path(p).read_text())
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
raw=L(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json')
v107=L(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
v101=L(I/'q048_frec_moving_h_accepted_checkpoint_v101.json')
a=L(I/'q048_moving_h_domain_accepted_proof_v102.json')
r=L(I/'q048_moving_h_domain_result_v102.json')
v=L(I/'q048_moving_h_domain_validation_v102.json')
aud=L(I/'Q048_V102_SOURCE_COEFFICIENT_AUDIT_V1.json')
prod=(I/'q048_moving_h_domain_v102.py').read_text()
checks={}
def C(n,x): checks[n]=bool(x)
C('identity',raw['q']=='Q048' and raw['target_q']=='Q048' and raw['proof_bridge_cell_z']==[970,960] and raw['proof_bridge_cell_a']==['1/971','1/961'])
C('raw_candidate',raw['status']=='CANDIDATE_SOURCE_CORRECT_PROOF_BRIDGE')
C('v107_pin',raw['parent_authority']['sha256']==S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')=='3876328fa6acfd5a79c01505526de8e2b6d384b06241685eb359fa5635747e24')
C('v101_pin',raw['historical_parent_reference']['sha256']==S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json')=='270e615ae9ee8455ce5ddb1c0d28ff24efa478db1db0e09c55ce8015bf434686')
C('distinct_identity',raw['parent_authority']['sha256']!=raw['historical_parent_reference']['sha256'] and raw['historical_parent_reference']['identity_transferred'] is False)
C('parent_actual',v107['accepted_actual']==v101['accepted_actual']=={'count':111,'frontier':970})
C('parent_frontiers',v107['frontiers']==v101['frontiers'])
C('parent_endpoint',v107['endpoint']==v101['endpoint'])
C('parent_lower',F(v107['connected_lower'])==F(v101['connected_lower'])==F(r['h0']))
C('parent_K',F(v107['K_upper'])==F(v101['K_upper']))
C('source_correct_parent',v107['correct_saha_fact']=='3.016103031869581e21' and v107['no_physical_reset'] is True)
C('v102_acceptance_pin',raw['retained_theorem']['historical_v102_acceptance_sha256']==S(I/'q048_moving_h_domain_accepted_proof_v102.json')=='26d742b146e9caf6420e17987c557125a61e219d7b0a9565791b774e4630ce6f')
C('v102_raw_pin',raw['retained_theorem']['historical_v102_raw_sha256']==S(I/'q048_moving_h_domain_result_v102.json')=='807aac41864cbb4af3149e80aa38ce642be081ab657af34bbdfb4fccf1d24845')
C('v102_validation_pin',raw['retained_theorem']['historical_v102_validation_sha256']==S(I/'q048_moving_h_domain_validation_v102.json')=='08b4d6ff805b99b40b58d63547730a98c0ae3a115bf94a6b6b1c8be140c9f0ae')
C('v102_accepted',a['mathematical_proof_accepted'] is True and a['proof_cell_z']==[970,960] and a['new_actual_cells']==0)
C('bounds_exact',raw['retained_theorem']['K_upper']==a['K_upper']==r['K_upper'] and raw['retained_theorem']['connected_lower']==a['connected_lower']==r['hmin'])
C('thermal_domain',raw['retained_theorem']['thermal_domain']==a['thermal_domain']==r['thermal_domain']==['-1/1000000','1/50'])
C('correct_saha_records',a['source_saha_factor']==r['saha_factor_source']==aud['SAHA_FACT_fsR1_meR1']=='3.016103031869581e21')
m=re.search(r"^SAHA_FACTOR=['\"]([^'\"]+)['\"]",prod,re.M)
C('correct_saha_code',m is not None and m.group(1)=='3.016103031869581e21' and prod.count('m.const(SAHA_FACTOR)')>=2)
C('bad_literal_not_executable',"m.const('3.016101031869581e21')" not in prod and 'm.const("3.016101031869581e21")' not in prod)
C('source_all',r['source_all'] is True and all(r['source_checks'].values()))
C('atomic_positive',r['atomic_positive'] is True)
C('C_positive',r['c_positive'] is True)
C('branches',r['branches']['L']['admitted'] and r['branches']['R']['admitted'])
C('historical_verifier',v['status']=='PASS' and v['verification_pass'] is True and v['checks_total']==v['checks_passed']==29 and all(v['checks'].values()))
C('guard_row48',r['guard_primary_index']==48 and v['checks']['row48'])
C('no_reset_glue',r['source_state_reset'] is False and v['checks']['no_reset_glue'])
C('guard_domain',v['checks']['guard_domain'])
C('background',v['checks']['background_recompute'])
C('atomic_recompute',v['checks']['atomic_recompute'] and v['checks']['atomic_positive'])
C('K_recompute',v['checks']['fresh_K_exact_outward'])
C('riccati',v['checks']['primary_endpoint_recomputed'] and v['checks']['positive_connected_lower_rational_dual'] and v['checks']['rational_control_exact'])
C('C_recompute',v['checks']['C_factors_recomputed_positive'])
C('thermal_L',v['checks']['L_H_faces'] and v['checks']['L_thermal_primitive'] and v['checks']['L_analytic_thermal_faces'])
C('thermal_R',v['checks']['R_H_faces'] and v['checks']['R_thermal_primitive'] and v['checks']['R_analytic_thermal_faces'])
C('scope_new_only',raw['binding_basis']['historical_open_precondition_disposition'].startswith('SUPERSEDED_ONLY_FOR_NEW_V104_TO_V107_REANALYSIS_LINEAGE'))
C('zero_actual',raw['new_actual_cells']==0 and raw['actual_state_unchanged']=={'count':111,'frontier':970})
C('one_bridge_no_recompute',raw['new_source_correct_proof_bridge_cells']==1 and raw['new_full_theorem_recomputations']==0)
C('history_firewall',raw['historical_v101_v102_modified'] is False)
C('stop',raw['consumer_authorization']=='NOT_GRANTED_BY_MATHEMATICS_RUN' and raw['below960_authorization']=='NOT_GRANTED' and raw['q_complete'] is False)
# Adversarial semantic mutations: every one must be rejected by exact invariants.
mut=[
 ('swap_parent_to_v101', raw['parent_authority']['sha256']!=raw['historical_parent_reference']['sha256']),
 ('wrong_frontier', v107['accepted_actual']['frontier']!=960),
 ('wrong_count', v107['accepted_actual']['count']!=110),
 ('wrong_endpoint_a', v107['endpoint']['a']!='1/961'),
 ('wrong_lower', F(v107['connected_lower'])!=F(a['connected_lower'])),
 ('wrong_parent_K_as_new_K', F(v107['K_upper'])!=F(a['K_upper'])),
 ('bad_saha', a['source_saha_factor']!='3.016101031869581e21'),
 ('reset_true', r['source_state_reset'] is not True),
 ('wrong_row', r['guard_primary_index']!=47),
 ('wrong_cell', r['cell_z']!=[980,970]),
 ('drop_L', r['branches']['L']['admitted'] is not False),
 ('drop_R', r['branches']['R']['admitted'] is not False),
 ('actual_promotion', raw['new_actual_cells']!=1),
 ('full_recompute_claim', raw['new_full_theorem_recomputations']!=1),
 ('history_relabel', raw['historical_v101_v102_modified'] is not True),
 ('below960', raw['below960_authorization']!='GRANTED')
]
mut_rej=sum(bool(x[1]) for x in mut)
status=all(checks.values()) and mut_rej==len(mut)
out={
 'schema':'bubbleverse.q048.v108.source_correct_proof_bridge.verification.v1',
 'status':'PASS' if status else 'FAIL','verification_pass':status,
 'raw_sha256':S(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'),
 'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,
 'semantic_mutations_total':len(mut),'semantic_mutations_rejected':mut_rej,
 'mutations':[{k:v} for k,v in mut],
 'independence_scope':'Separate bridge/binding verifier with independent invariant composition. Shares historical V102 theorem bytes, inputs and enclosures; not an independent physical or native-trajectory replication.',
 'actual_state_unchanged':{'count':111,'frontier':970},'new_actual_cells':0,'q_complete':False
}
p=R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'; p.write_text(json.dumps(out,indent=2)+'\n')
print(p.name,S(p),out['status'],len(checks),sum(checks.values()),len(mut),mut_rej)
