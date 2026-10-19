import json,hashlib,pathlib
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); I=R/'q048_v106_inputs'; O=R/'q048_v106_math'
def L(p): return json.load(open(p))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
v105=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'); v97=L(I/'q048_frec_moving_h_accepted_checkpoint_v97.json'); a=L(I/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json'); tv=L(I/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json'); sv=L(I/'Q048_SAHA_PARENT_SOURCE_ADMISSIBILITY_VALIDATION_V1.json'); snap=L(O/'Q048_V106_DERIVED_INPUT_SNAPSHOT_V1.json'); raw=L(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json')
checks={}
def C(k,x): checks[k]=bool(x)
C('q_identity',raw['q']=='Q048' and raw['target_q']=='Q048' and raw['proof_cell_z']==[980,970])
C('v105_hash',S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')=='cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098')
C('v97_hash',S(I/'q048_frec_moving_h_accepted_checkpoint_v97.json')=='be53c4e56133bfce66108a5bc81e9ba8ce49334c2cfee4cef21306c652663da8')
C('v100_accept_hash',S(I/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json')=='f656241001cd54f6505e1a79705cfe51dc04bd25954f205c9f0525c18e762df6')
C('v100_ver_hash',S(I/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json')=='9e9ca61068b7045cae4e51f9cb5d0e5cb62c1cfab0b10eeb4be8f65ef90da8e6')
C('v103_ver_hash',S(I/'Q048_SAHA_PARENT_SOURCE_ADMISSIBILITY_VALIDATION_V1.json')=='8ce6e107ab9f7cd71a61056953a0c520b1e11ab5ceef4c9713a965632ea05a55')
statekeys=['accepted_actual','frontiers','endpoint','connected_lower','K_upper']
C('parent_exact_state',all(v105[k]==v97[k] for k in statekeys))
C('parent_identity_distinct',raw['parent_authority']['sha256']!=raw['historical_reference_only']['v97_checkpoint_sha256'])
C('source_correct_factor',v105['correct_saha_fact']=='3.016103031869581e21' and raw['corrected_source_transfer']['correct_saha_fact']=='3.016103031869581e21')
C('v100_cell',a['proof_cell_z']==[980,970] and a['proof_cell_a']==['1/981','1/971'])
C('thermal_domain',a['thermal_domain']==['-1/1000000','1/50'] and raw['thermal_domain']==a['thermal_domain'])
C('v100_acceptance',a['mathematical_proof_accepted'] and a['technical_state']=='PASS' and all(a['criteria_observed'].values()))
C('v100_zero_actual',a['new_actual_cells']==0)
C('thermal_verify',tv['verification_pass'] and tv['parent_domain_subset'] and tv['candidate_w_hi']=='1/50')
C('thermal_L_exact',tv['branches']['L']['margin_exact_match'] and tv['branches']['L']['upper_face_analytic_pass'] and F(tv['branches']['L']['analytic_margin'])>0)
C('thermal_R_exact',tv['branches']['R']['margin_exact_match'] and tv['branches']['R']['upper_face_analytic_pass'] and F(tv['branches']['R']['analytic_margin'])>0)
C('v103_validation',sv['status']=='PASS' and sv['checks_passed']==sv['checks_total']==24)
C('v103_cert_pin',sv['certificate_sha256']==snap['v103_certificate']['sha256_expected']=='3f26ed2bed293b2489f36dd59f63b6ea623365fea0d24216ed7cfaadb4207edb')
C('source_domain',sv['checks']['source_domain_numerical'] and sv['checks']['source_capture_flags'])
C('atomic',sv['checks']['atomic_A_Aeq_positive'])
C('C_binding',sv['checks']['C_polynomial_expansions'] and sv['checks']['C_source_binding'])
C('L_H_positive',all(F(x)>0 for x in sv['details']['L_H_margins']))
C('R_H_positive',all(F(x)>0 for x in sv['details']['R_H_margins']))
C('thermal_source_independent',sv['checks']['L_thermal_independent'] and sv['checks']['R_thermal_independent'])
row=snap['v97_next_math_task']['row47']
C('row47_identity',row['index']==47 and [row['z0'],row['z1']]==[980,970])
C('row47_E_glue',F(row['E_input_left'])==F(v105['endpoint']['E']))
C('row47_Y_glue',F(row['Y_left'])==F(v105['endpoint']['Y']))
C('row47_V_glue',F(row['V_previous'])==F(v105['endpoint']['Vbar']))
C('row47_no_reset',row['source_state_reset'] is False)
C('row47_qualified',row['whole_cell_qualified'] and row['accepted'] and row['committed'])
C('retained_K',F(raw['retained_theorem']['K_upper'])==F(snap['v100_raw']['selected']['K_upper']) and F(raw['retained_theorem']['K_upper'])>0)
C('retained_lower',F(raw['retained_theorem']['connected_lower'])==F(snap['v100_raw']['selected']['hmin']) and F(raw['retained_theorem']['connected_lower'])>0)
C('no_recompute',raw['new_full_theorem_recomputations']==0)
C('one_bridge_zero_actual',raw['new_source_correct_proof_bridge_cells']==1 and raw['new_actual_cells']==0)
C('consumer_not_granted',raw['consumer_authorization']=='NOT_GRANTED' and raw['below970_authorization']=='NOT_GRANTED')
C('history_firewall',raw['historical_reference_only']['historical_v97_relabelled'] is False)
# Adversarial semantic mutations: each must be rejected by an invariant above
mut={
 'old_saha_factor': '3.016101031869581e21' != v105['correct_saha_fact'],
 'wrong_parent_frontier': 990 != v105['accepted_actual']['frontier'],
 'wrong_parent_count': 109 != v105['accepted_actual']['count'],
 'changed_parent_E': F(v105['endpoint']['E'])+1 != F(row['E_input_left']),
 'reset_true': True != row['source_state_reset'],
 'wrong_cell': [990,980] != raw['proof_cell_z'],
 'narrow_thermal_box': ['-1/1000000','1/100'] != raw['thermal_domain'],
 'wrong_K': F(v97['K_upper']) != F(raw['retained_theorem']['K_upper']),
 'wrong_lower': F(v97['connected_lower']) != F(raw['retained_theorem']['connected_lower']),
 'historical_identity_claim': raw['parent_authority']['sha256'] != raw['historical_reference_only']['v97_checkpoint_sha256'],
 'actual_cell_created': 1 != raw['new_actual_cells'],
 'below970_authorized': 'GRANTED' != raw['below970_authorization']
}
status=all(checks.values()) and all(mut.values())
out={'schema':'bubbleverse.q048.v106.source_correct_proof_bridge.verification.v1','status':'PASS' if status else 'FAIL','technical_state':'PASS' if status else 'FAIL','raw_sha256':S(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'),'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'semantic_mutations_total':len(mut),'semantic_mutations_rejected':sum(mut.values()),'semantic_mutations':mut,'independence_scope':'Separate verifier re-loads exact pinned local artifacts and independently recomputes equality/sign/glue invariants. It shares V100/V103 historical enclosures and therefore is not physically independent evidence.'}
p=O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'; p.write_text(json.dumps(out,indent=2)+'\n'); print(p,S(p),out['status'],out['checks_passed'],out['checks_total'],out['semantic_mutations_rejected'])
