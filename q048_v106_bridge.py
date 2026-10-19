import json,hashlib,pathlib,datetime
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); I=R/'q048_v106_inputs'; O=R/'q048_v106_math'
def L(p): return json.load(open(p))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
v105=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
v97=L(I/'q048_frec_moving_h_accepted_checkpoint_v97.json')
v100=L(I/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json')
v100ver=L(I/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json')
v103ver=L(I/'Q048_SAHA_PARENT_SOURCE_ADMISSIBILITY_VALIDATION_V1.json')
snap=L(O/'Q048_V106_DERIVED_INPUT_SNAPSHOT_V1.json')
# Exact-byte pins available locally
assert S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')=='cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098'
assert S(I/'q048_frec_moving_h_accepted_checkpoint_v97.json')=='be53c4e56133bfce66108a5bc81e9ba8ce49334c2cfee4cef21306c652663da8'
assert S(I/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json')=='f656241001cd54f6505e1a79705cfe51dc04bd25954f205c9f0525c18e762df6'
assert S(I/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json')=='9e9ca61068b7045cae4e51f9cb5d0e5cb62c1cfab0b10eeb4be8f65ef90da8e6'
assert S(I/'Q048_SAHA_PARENT_SOURCE_ADMISSIBILITY_VALIDATION_V1.json')=='8ce6e107ab9f7cd71a61056953a0c520b1e11ab5ceef4c9713a965632ea05a55'
# Parent numerical state equality; provenance identity deliberately differs
fields=['accepted_actual','frontiers','endpoint','connected_lower','K_upper']
parent_equal=all(v105[k]==v97[k] for k in fields)
assert parent_equal
assert v105['accepted_actual']=={'count':110,'frontier':980}
assert v105['correct_saha_fact']=='3.016103031869581e21'
assert v105['theorem_checkpoint_sha256']=='4cac1a8fb598001c6907163752a7a9bf6005de649546fade84658bdb0627b691'
# V100 theorem identity and domain
assert v100['mathematical_proof_accepted'] is True
assert v100['parent_actual']=={'count':110,'frontier':980}
assert v100['proof_cell_z']==[980,970] and v100['proof_cell_a']==['1/981','1/971']
assert v100['thermal_domain']==['-1/1000000','1/50']
assert all(v100['criteria_observed'].values())
assert v100['new_actual_cells']==0
# Independent thermal verifier
assert v100ver['verification_pass'] is True and v100ver['parent_domain_subset'] is True
assert v100ver['candidate_w_hi']=='1/50' and v100ver['source_domain_all_pass'] and v100ver['atomic_positive'] and v100ver['c_factor_positive']
assert all(v100ver['branches'][b]['upper_face_analytic_pass'] and v100ver['branches'][b]['all_branch_checks_reported_pass'] for b in ['L','R'])
# V103 corrected-source validation; historical blocker was ancestor provenance, now supplied separately by V105
assert v103ver['status']=='PASS' and v103ver['checks_total']==24 and v103ver['checks_passed']==24
for k in ['factors_decimal_binary_enclosures','Saha_transfer_cross_multiplication','source_domain_numerical','atomic_A_Aeq_positive','L_H_strict_and_exact','R_H_strict_and_exact','L_thermal_independent','R_thermal_independent','C_polynomial_expansions','C_source_binding']:
    assert v103ver['checks'][k] is True
assert v103ver['certificate_sha256']=='3f26ed2bed293b2489f36dd59f63b6ea623365fea0d24216ed7cfaadb4207edb'
# Connector-inspected source records, stored only as a derived selected-field snapshot
rawsel=snap['v100_raw']['selected']; certsel=snap['v103_certificate']['selected']; row=snap['v97_next_math_task']['row47']
assert rawsel['cell_z']==[980,970] and rawsel['source_all'] and rawsel['atomic_positive'] and rawsel['c_positive'] and rawsel['L_admitted'] and rawsel['R_admitted']
assert certsel['true_literal']==v105['correct_saha_fact'] and certsel['checks_passed']==certsel['checks_total']==25
assert certsel['L_new_source_upper_H'] and certsel['R_new_source_upper_H'] and certsel['L_unchanged_thermal_faces'] and certsel['R_unchanged_thermal_faces'] and certsel['retained_comparison_positive']
# Guard glue is exact against new parent and no physical reset
assert row['index']==47 and [row['z0'],row['z1']]==[980,970] and [row['a0'],row['a1']]==['1/981','1/971']
assert row['E_input_left']==v105['endpoint']['E'] and row['Y_left']==v105['endpoint']['Y'] and row['V_previous']==v105['endpoint']['Vbar']
assert row['source_state_reset'] is False and row['whole_cell_qualified'] and row['accepted'] and row['committed']
# Correct-source H margins from V103 verifier are strictly positive
for branch in ['L','R']:
    for m in v103ver['details'][branch+'_H_margins']:
        assert F(m)>0
# Retained V100 theorem values for this exact 980->970 proof cell
newK=rawsel['K_upper']; newlower=rawsel['hmin']
assert F(newK)>0 and F(newlower)>0
out={
 'schema':'bubbleverse.q048.v106.source_correct_proof_bridge.raw.v1','q':'Q048','target_q':'Q048',
 'task_id':'LOCAL-Q048-V106-SOURCE-CORRECT-PROOF-BRIDGE-980-970-V1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PENDING_VALIDATION','technical_state':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE',
 'proof_cell_z':[980,970],'proof_cell_a':['1/981','1/971'],'thermal_domain':['-1/1000000','1/50'],
 'parent_authority':{'record':'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json','sha256':S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'),'actual':v105['accepted_actual'],'endpoint':v105['endpoint'],'correct_saha_fact':v105['correct_saha_fact']},
 'historical_reference_only':{'v97_checkpoint_sha256':S(I/'q048_frec_moving_h_accepted_checkpoint_v97.json'),'numerical_parent_state_exact_match':parent_equal,'historical_v97_relabelled':False},
 'retained_theorem':{'v100_acceptance_sha256':S(I/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json'),'v100_raw_sha256_reported':snap['v100_raw']['sha256_expected'],'v100_thermal_verification_sha256':S(I/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json'),'K_upper':newK,'connected_lower':newlower},
 'corrected_source_transfer':{'v103_certificate_sha256':v103ver['certificate_sha256'],'v103_validation_sha256':S(I/'Q048_SAHA_PARENT_SOURCE_ADMISSIBILITY_VALIDATION_V1.json'),'correct_saha_fact':v105['correct_saha_fact'],'L_H_margins':v103ver['details']['L_H_margins'],'R_H_margins':v103ver['details']['R_H_margins']},
 'guard_binding':{'row_index':47,'row_sha256_reported':row['primary_row_sha256'],'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True},
 'bridge_checks':{'parent_numerical_state_exact':True,'parent_provenance_distinct':True,'source_correct_parent_v105':True,'V100_proof_accepted':True,'V100_thermal_verifier_pass':True,'V103_corrected_source_validation_pass':True,'correct_source_H_margins_positive':True,'atomic_positive_retained':True,'C_factor_positive_retained':True,'comparison_riccati_retained':True,'thermal_faces_retained':True,'guard_glue_exact':True,'no_physical_reset':True,'captured_inputs_unchanged_by_bridge':True,'accepted_z_reio_unchanged_by_bridge':True,'original_q048_physics_unchanged':True},
 'bridge_conclusion':'V100 980->970 theorem content is admissibly rebound to the source-qualified V105 actual110/frontier980 parent under the V103 corrected-source transfer; this is a new current-reassessment proof bridge, not historical V97/V100/V101 identity.',
 'new_source_correct_proof_bridge_cells':1,'new_full_theorem_recomputations':0,'new_actual_cells':0,'consumer_authorization':'NOT_GRANTED','below970_authorization':'NOT_GRANTED','q_complete':False,
 'independence_limit':'Bridge verifier may separately recompute binding and exact rational sign checks, but both bridge and verifier share the historical V100/V103 source enclosures; no physical independence is claimed.'
}
p=O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'; p.write_text(json.dumps(out,indent=2)+'\n')
print(p,S(p))
