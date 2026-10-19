import json, hashlib, pathlib, re, datetime
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); I=R/'q048_v108_inputs'

def L(p): return json.loads(pathlib.Path(p).read_text())
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def exact_eq(a,b):
    if isinstance(a,str) and isinstance(b,str):
        try: return F(a)==F(b)
        except Exception: return a==b
    return a==b

PINS={
 'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json':'3876328fa6acfd5a79c01505526de8e2b6d384b06241685eb359fa5635747e24',
 str(I/'q048_frec_moving_h_accepted_checkpoint_v101.json'):'270e615ae9ee8455ce5ddb1c0d28ff24efa478db1db0e09c55ce8015bf434686',
 str(I/'q048_moving_h_domain_accepted_proof_v102.json'):'26d742b146e9caf6420e17987c557125a61e219d7b0a9565791b774e4630ce6f',
 str(I/'q048_moving_h_domain_result_v102.json'):'807aac41864cbb4af3149e80aa38ce642be081ab657af34bbdfb4fccf1d24845',
 str(I/'q048_moving_h_domain_validation_v102.json'):'08b4d6ff805b99b40b58d63547730a98c0ae3a115bf94a6b6b1c8be140c9f0ae',
 str(I/'Q048_V102_SOURCE_COEFFICIENT_AUDIT_V1.json'):'c147db8aaa3596c0a7bd1e6bf36b51e235a48808b6a65fd8f74229d8fc08abe1',
 str(I/'q048_moving_h_domain_spec_v102.json'):'c54bc8ac547c66349f6797bd15b98fd4b9bb98915bd5e0004b630bf3f2149d63',
 str(I/'Q048_MOVING_H_DOMAIN_FREEZE_V102.json'):'a4be9ad22c1dc76542a0350174d560b26619cb6f1054be8c512584ac04047d5c',
 str(I/'q048_moving_h_domain_v102.py'):'84e1dd4ef937f6d61d0dd4e5a697507ac0139778d472175bc36366b4c4a63f57',
 str(I/'q048_moving_h_domain_verify_v102.py'):'09066cd3b531dd721b168da06b566f12a11132354110d5570ddf28c659faedab',
 'Bubbleverse_Matematikmotor_2.1.0-144.md':'3594851ec3b827d643ba89c410a04ca454e80648011dde549f229a69f085475b',
 'Q048_V108_HANDOFF_TO_MATHEMATICS_SOURCE_CORRECT_PROOF_BRIDGE_V1.md':'4df960b993ddfc3321768e5c0a47499dc43d573b6cae593a624a96398a77d52c'
}
for p,h in PINS.items():
    pp=pathlib.Path(p)
    if not pp.is_absolute(): pp=R/pp
    assert pp.exists(), p
    assert S(pp)==h, (p,S(pp),h)

v107=L(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
v101=L(I/'q048_frec_moving_h_accepted_checkpoint_v101.json')
v102a=L(I/'q048_moving_h_domain_accepted_proof_v102.json')
v102r=L(I/'q048_moving_h_domain_result_v102.json')
v102v=L(I/'q048_moving_h_domain_validation_v102.json')
audit=L(I/'Q048_V102_SOURCE_COEFFICIENT_AUDIT_V1.json')
spec=L(I/'q048_moving_h_domain_spec_v102.json')
prod=(I/'q048_moving_h_domain_v102.py').read_text()

# Exact parent-state equivalence while preserving distinct identities.
assert v107['accepted_actual']==v101['accepted_actual']=={'count':111,'frontier':970}
assert v107['frontiers']==v101['frontiers']
assert v107['endpoint']==v101['endpoint']
assert F(v107['connected_lower'])==F(v101['connected_lower'])
assert F(v107['K_upper'])==F(v101['K_upper'])
assert S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json') != S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json')
assert v107['correct_saha_fact']=='3.016103031869581e21'
assert v107['no_physical_reset'] is True

# Historical V102 theorem validity and local source semantics.
assert v102a['mathematical_proof_accepted'] is True
assert v102a['proof_cell_z']==[970,960] and v102a['proof_cell_a']==['1/971','1/961']
assert v102a['new_actual_cells']==0 and v102a['new_mathematical_proof_cells']==1
assert v102a['parent_checkpoint_sha256']==S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json')
assert v102a['source_saha_factor']=='3.016103031869581e21'
assert v102a['raw_sha256']==S(I/'q048_moving_h_domain_result_v102.json')
assert v102a['validation_sha256']==S(I/'q048_moving_h_domain_validation_v102.json')
assert v102a['freeze_sha256']==S(I/'Q048_MOVING_H_DOMAIN_FREEZE_V102.json')
assert v102a['spec_sha256']==S(I/'q048_moving_h_domain_spec_v102.json')
assert v102r['saha_factor_source']=='3.016103031869581e21'
assert v102r['source_all'] and v102r['atomic_positive'] and v102r['c_positive']
assert all(v102r['branches'][b]['admitted'] for b in ['L','R'])
assert v102r['source_state_reset'] is False and v102r['guard_primary_index']==48
assert v102r['parent_actual']=={'count':111,'frontier':970}
assert F(v102r['h0'])==F(v101['connected_lower'])==F(v107['connected_lower'])
assert v102r['K_upper']==v102a['K_upper']
assert v102r['hmin']==v102a['connected_lower']
assert v102r['thermal_domain']==v102a['thermal_domain']==['-1/1000000','1/50']
assert v102v['status']=='PASS' and v102v['verification_pass'] is True
assert v102v['checks_total']==v102v['checks_passed']==29 and all(v102v['checks'].values())
for k in ['parent','row48','no_reset_glue','guard_domain','source_factor_literal','background_recompute','atomic_recompute','atomic_positive','fresh_K_exact_outward','primary_endpoint_recomputed','positive_connected_lower_rational_dual','C_factors_recomputed_positive','L_H_faces','L_thermal_primitive','R_H_faces','R_thermal_primitive']:
    assert v102v['checks'][k] is True, k

# Verify local producer source uses the correct coefficient as executable constant.
m=re.search(r"^SAHA_FACTOR=['\"]([^'\"]+)['\"]",prod,re.M)
assert m and m.group(1)=='3.016103031869581e21'
assert "m.const(SAHA_FACTOR)" in prod
assert "m.const('3.016101031869581e21')" not in prod and 'm.const("3.016101031869581e21")' not in prod
assert audit['SAHA_FACT_fsR1_meR1']=='3.016103031869581e21'
assert audit['V102_resolution'].startswith('Use authoritative pinned-source constant')
assert audit['no_old_science_replay'] is True

# Parent-dependent scope audit from actual historical implementation:
# producer validates accepted_actual, endpoint glue, endpoint a and connected_lower/h0.
required_parent_fields=['accepted_actual','endpoint','connected_lower']
for f in required_parent_fields:
    assert f in v107 and f in v101
assert "parent['accepted_actual']" in prod
assert "parent['endpoint']" in prod
assert "parent['connected_lower']" in prod
# Full handoff additionally requires exact frontiers and K equality; checked above.

checks={
 'q_target_identity': v107['q']=='Q048' and v107['target_q']=='Q048' and v102a['q']=='Q048' and v102a['target_q']=='Q048',
 'v107_validated': v107['status']=='VALIDATED' and v107['technical_state']=='PASS',
 'parent_actual_exact': v107['accepted_actual']==v101['accepted_actual'],
 'parent_frontiers_exact': v107['frontiers']==v101['frontiers'],
 'parent_endpoint_exact': v107['endpoint']==v101['endpoint'],
 'parent_lower_exact': F(v107['connected_lower'])==F(v101['connected_lower']),
 'parent_K_exact': F(v107['K_upper'])==F(v101['K_upper']),
 'identity_distinct': S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')!=S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json'),
 'v107_source_correct': v107['correct_saha_fact']=='3.016103031869581e21',
 'v107_no_reset': v107['no_physical_reset'] is True,
 'v102_accepted': v102a['mathematical_proof_accepted'] is True,
 'v102_cell_exact': v102a['proof_cell_z']==[970,960] and v102a['proof_cell_a']==['1/971','1/961'],
 'v102_parent_pin_historical_v101': v102a['parent_checkpoint_sha256']==S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json'),
 'v102_zero_actual': v102a['new_actual_cells']==0,
 'v102_correct_saha_acceptance': v102a['source_saha_factor']=='3.016103031869581e21',
 'v102_correct_saha_raw': v102r['saha_factor_source']=='3.016103031869581e21',
 'v102_correct_saha_executable': bool(m and m.group(1)=='3.016103031869581e21'),
 'v100_bad_literal_not_executable_local': "m.const('3.016101031869581e21')" not in prod and 'm.const("3.016101031869581e21")' not in prod,
 'v102_source_all': v102r['source_all'] is True and all(v102r['source_checks'].values()),
 'v102_atomic_positive': v102r['atomic_positive'] is True,
 'v102_C_positive': v102r['c_positive'] is True,
 'v102_branches_admitted': all(v102r['branches'][b]['admitted'] for b in ['L','R']),
 'v102_validation_29_29': v102v['verification_pass'] is True and v102v['checks_total']==29 and v102v['checks_passed']==29,
 'guard_row48': v102v['checks']['row48'] and v102r['guard_primary_index']==48,
 'guard_no_reset_glue': v102v['checks']['no_reset_glue'] and v102r['source_state_reset'] is False,
 'guard_domain': v102v['checks']['guard_domain'],
 'background_recompute': v102v['checks']['background_recompute'],
 'atomic_recompute': v102v['checks']['atomic_recompute'],
 'K_recompute': v102v['checks']['fresh_K_exact_outward'],
 'riccati_lower_recompute': v102v['checks']['primary_endpoint_recomputed'] and v102v['checks']['positive_connected_lower_rational_dual'],
 'C_factor_recompute': v102v['checks']['C_factors_recomputed_positive'],
 'thermal_L': v102v['checks']['L_H_faces'] and v102v['checks']['L_thermal_primitive'] and v102v['checks']['L_analytic_thermal_faces'],
 'thermal_R': v102v['checks']['R_H_faces'] and v102v['checks']['R_thermal_primitive'] and v102v['checks']['R_analytic_thermal_faces'],
 'h0_transfer_exact': F(v102r['h0'])==F(v107['connected_lower']),
 'theorem_bounds_retained': v102r['K_upper']==v102a['K_upper'] and v102r['hmin']==v102a['connected_lower'],
 'thermal_domain_retained': v102r['thermal_domain']==v102a['thermal_domain']==['-1/1000000','1/50'],
 'historical_status_not_modified': True,
 'zero_actual_cells_v108': True,
 'no_below960': True,
}
assert all(checks.values()), [k for k,v in checks.items() if not v]

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
out={
 'schema':'bubbleverse.q048.v108.source_correct_proof_bridge.raw.v1',
 'q':'Q048','target_q':'Q048',
 'task_id':'LOCAL-Q048-V108-SOURCE-CORRECT-PROOF-BRIDGE-970-960-V1',
 'task_fingerprint':'97f34c36077fedbe1949fcd39b325aba48c1e55f43908c1c71bb8f43ca8fbeaa',
 'created_at_utc':now,
 'status':'CANDIDATE_SOURCE_CORRECT_PROOF_BRIDGE',
 'scientific_state':'INCONCLUSIVE','technical_state':'PENDING_VERIFICATION',
 'proof_bridge_cell_z':[970,960],'proof_bridge_cell_a':['1/971','1/961'],
 'parent_authority':{
   'record':'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json',
   'sha256':S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'),
   'accepted_actual':v107['accepted_actual'],'frontiers':v107['frontiers'],'endpoint':v107['endpoint'],
   'connected_lower':v107['connected_lower'],'K_upper':v107['K_upper'],'correct_saha_fact':v107['correct_saha_fact']},
 'historical_parent_reference':{
   'record':'q048_frec_moving_h_accepted_checkpoint_v101.json','sha256':S(I/'q048_frec_moving_h_accepted_checkpoint_v101.json'),
   'role':'REFERENCE_ONLY_NUMERICAL_PARENT_EQUIVALENCE','identity_transferred':False},
 'retained_theorem':{
   'historical_v102_acceptance_sha256':S(I/'q048_moving_h_domain_accepted_proof_v102.json'),
   'historical_v102_raw_sha256':S(I/'q048_moving_h_domain_result_v102.json'),
   'historical_v102_validation_sha256':S(I/'q048_moving_h_domain_validation_v102.json'),
   'historical_v102_spec_sha256':S(I/'q048_moving_h_domain_spec_v102.json'),
   'historical_v102_freeze_sha256':S(I/'Q048_MOVING_H_DOMAIN_FREEZE_V102.json'),
   'K_upper':v102a['K_upper'],'connected_lower':v102a['connected_lower'],'thermal_domain':v102a['thermal_domain'],
   'source_saha_factor':v102a['source_saha_factor'],
   'historical_scope':v102a['proof_scope'],
   'new_scope':'SOURCE_CORRECT_REANALYSIS_LINEAGE_ON_V107_PARENT'},
 'binding_basis':{
   'exact_parent_fields':['accepted_actual','frontiers','endpoint','connected_lower','K_upper'],
   'historical_implementation_parent_dependencies':['accepted_actual','endpoint','connected_lower'],
   'guard_row_index':48,
   'source_state_reset':False,
   'v102_validation_checks_retained':v102v['checks_total'],
   'v102_validation_checks_passed':v102v['checks_passed'],
   'source_coefficient_audit_sha256':S(I/'Q048_V102_SOURCE_COEFFICIENT_AUDIT_V1.json'),
   'historical_open_precondition_disposition':'SUPERSEDED_ONLY_FOR_NEW_V104_TO_V107_REANALYSIS_LINEAGE_BY_SOURCE_CORRECT_PARENT; HISTORICAL_V102_STATUS_UNCHANGED'},
 'checks':checks,
 'new_source_correct_proof_bridge_cells':1,
 'new_full_theorem_recomputations':0,
 'new_actual_cells':0,
 'actual_state_unchanged':v107['accepted_actual'],
 'historical_v101_v102_modified':False,
 'consumer_authorization':'NOT_GRANTED_BY_MATHEMATICS_RUN',
 'below960_authorization':'NOT_GRANTED',
 'no_native_trajectory_claim':True,
 'independence_limit':'Bridge verifier checks binding/provenance logic and retained theorem invariants; it is not an independent physical replication because V108 reuses V102 theorem inputs and enclosures.',
 'q_complete':False,'NativeP6':'UNRESOLVED'
}
path=R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(path.name,S(path),len(checks),sum(checks.values()))
