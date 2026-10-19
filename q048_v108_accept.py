import json,hashlib,pathlib,datetime
R=pathlib.Path('/mnt/data')
def L(p):return json.loads(pathlib.Path(p).read_text())
def S(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
raw=L(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json');ver=L(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json')
assert ver['status']=='PASS' and ver['verification_pass'] and ver['raw_sha256']==S(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json')
assert raw['new_source_correct_proof_bridge_cells']==1 and raw['new_full_theorem_recomputations']==0 and raw['new_actual_cells']==0
assert raw['actual_state_unchanged']=={'count':111,'frontier':970}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cp={
 'schema':'bubbleverse.q048.v108.source_correct_proof_bridge.acceptance.v1','q':'Q048','target_q':'Q048',
 'task_id':raw['task_id'],'status':'ACCEPTED','technical_state':'PASS','scientific_state':'INCONCLUSIVE','accepted_at_utc':now,
 'proof_bridge_cell_z':raw['proof_bridge_cell_z'],'proof_bridge_cell_a':raw['proof_bridge_cell_a'],
 'parent_authority':raw['parent_authority'],'retained_theorem':raw['retained_theorem'],'binding_basis':raw['binding_basis'],
 'raw_sha256':S(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'),
 'verification_sha256':S(R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'),
 'new_source_correct_proof_bridge_cells':1,'new_full_theorem_recomputations':0,'new_actual_cells':0,
 'actual_state_unchanged':raw['actual_state_unchanged'],'historical_v101_v102_modified':False,
 'consumer_authorization':'NOT_GRANTED','below960_authorization':'NOT_GRANTED','q_complete':False,'NativeP6':'UNRESOLVED',
 'claim':'Source-correct proof bridge 970->960 accepted for the V104->V107 reassessment lineage. Historical V102 theorem content is rebound to the exact-equal V107 numerical parent state; historical execution identity is not transferred.'
}
p=R/'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json';p.write_text(json.dumps(cp,indent=2)+'\n')
print(p.name,S(p))
