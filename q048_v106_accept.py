import json,hashlib,pathlib,datetime
R=pathlib.Path('/mnt/data'); I=R/'q048_v106_inputs'; O=R/'q048_v106_math'
def L(p): return json.load(open(p))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
raw=L(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'); ver=L(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'); v105=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
assert ver['status']=='PASS' and ver['raw_sha256']==S(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json')
acc={
 'schema':'bubbleverse.q048.v106.source_correct_proof_bridge.acceptance.v1','q':'Q048','target_q':'Q048','task_id':'LOCAL-Q048-V106-SOURCE-CORRECT-PROOF-BRIDGE-980-970-V1',
 'status':'ACCEPTED','technical_state':'PASS','scientific_state':'INCONCLUSIVE','accepted_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'proof_bridge_cell_z':[980,970],'proof_bridge_cell_a':['1/981','1/971'],'thermal_domain':['-1/1000000','1/50'],
 'parent_authority':{'actual':v105['accepted_actual'],'checkpoint_sha256':S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'),'endpoint':v105['endpoint'],'correct_saha_fact':v105['correct_saha_fact']},
 'retained_theorem':{'K_upper':raw['retained_theorem']['K_upper'],'connected_lower':raw['retained_theorem']['connected_lower'],'historical_v100_acceptance_sha256':raw['retained_theorem']['v100_acceptance_sha256'],'historical_v100_raw_sha256_reported':raw['retained_theorem']['v100_raw_sha256_reported'],'historical_v100_thermal_verification_sha256':raw['retained_theorem']['v100_thermal_verification_sha256']},
 'corrected_source_transfer':raw['corrected_source_transfer'],'guard_binding':raw['guard_binding'],
 'raw_sha256':S(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'),'verification_sha256':S(O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'),
 'new_source_correct_proof_bridge_cells':1,'new_full_theorem_recomputations':0,'new_actual_cells':0,'actual_state_unchanged':v105['accepted_actual'],
 'historical_v97_v100_v101_modified':False,'consumer_authorization':'NOT_GRANTED','below970_authorization':'NOT_GRANTED','q_complete':False,
 'claim':'Source-correct proof bridge 980->970 accepted for the V105 reanalysis lineage. Historical V100 theorem content and V103 corrected-source transfer are rebound to the exact-equal V105 numerical parent state; historical execution identity is not transferred.'
}
p=O/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json'; p.write_text(json.dumps(acc,indent=2)+'\n'); print(p,S(p))
