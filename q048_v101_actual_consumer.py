import json,hashlib,datetime,pathlib
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); I=R/'q048_v101_inputs'
def load(p): return json.load(open(p))
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
parent=load(I/'q048_frec_moving_h_accepted_checkpoint_v97.json')
guardtask=load(I/'Q048_FREC_MOVING_H_V97_NEXT_MATHEMATICS_TASK_V1.json')
acc=load(R/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json')
ver=load(R/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json')
raw=load(R/'V100_FULL_GATE_W002_RAW.json')
manifest=load(R/'Q048_V100_DELIVERY_MANIFEST_V1.json')
# pinned input checks
expected_parent='be53c4e56133bfce66108a5bc81e9ba8ce49334c2cfee4cef21306c652663da8'
assert sha(I/'q048_frec_moving_h_accepted_checkpoint_v97.json')==expected_parent
for x in manifest['files']:
 p=R/x['filename']
 if p.exists(): assert sha(p)==x['sha256'], x['filename']
assert parent['accepted_actual']=={'count':110,'frontier':980}
assert acc['mathematical_proof_accepted'] is True and acc['proof_cell_z']==[980,970]
assert acc['actual_state_after_acceptance']=={'count':110,'frontier':980}
assert ver['verification_pass'] is True and ver['authoritative_actual_state_unchanged']=={'count':110,'frontier':980}
assert raw['source_all'] and raw['atomic_positive'] and raw['c_positive']
assert all(raw['branches'][b]['admitted'] for b in ['L','R'])
row=guardtask['guard_binding']['primary']
assert row['index']==47 and row['z0']==980 and row['z1']==970 and row['a0']=='1/981' and row['a1']=='1/971'
assert row['source_state_reset'] is False and row['whole_cell_qualified'] and row['accepted'] and row['committed']
assert row['E_input_left']==parent['endpoint']['E'] and row['Y_left']==parent['endpoint']['Y'] and row['V_previous']==parent['endpoint']['Vbar']
# accepted proof supplies fresh K/lower for exactly this cell
assert raw['cell_z']==[980,970]
new_lower=raw['hmin']; new_K=raw['K_upper']
assert F(new_lower)>0 and F(new_K)>0
# one actual cell only; endpoint comes from committed primary row47, not control
out={
 'schema':'bubbleverse.q048.frec_moving_h.actual_consumer.v101.raw.v1','q':'Q048','target_q':'Q048',
 'status':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE','technical_state':'PENDING_VALIDATION',
 'task_id':'LOCAL-Q048-V101-ACTUAL-CONSUMER-980-970-V1','cell_z':[980,970],'cell_a':['1/981','1/971'],
 'parent':{'count':110,'frontier':980,'sha256':expected_parent},
 'consumed_proof':{'record':'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1','sha256':sha(R/'Q048_V100_MATHEMATICAL_PROOF_ACCEPTANCE_V1.json'),'independent_verification_sha256':sha(R/'Q048_V100_REFINED_THERMAL_INDEPENDENT_VERIFICATION_V1.json'),'raw_gate_sha256':sha(R/'V100_FULL_GATE_W002_RAW.json')},
 'consumer_checks':{'proof_accepted':True,'independent_verification_pass':True,'source_all':True,'atomic_positive':True,'c_factor_positive':True,'L_branch':True,'R_branch':True,'row47_glue_exact':True,'source_state_reset':False,'primary_row_committed':True,'connected_lower_positive':True,'K_positive':True},
 'candidate_actual':{'count':111,'frontier':970,'frontiers':dict(parent['frontiers'],**{'hillipop-ede_n3':970}),'endpoint':{'a':'1/971','E':row['E_right'],'Y':row['Y_right'],'Vbar':row['V_admitted']},'connected_lower':new_lower,'K_upper':new_K},
 'guard_binding':{'index':47,'primary_row_sha256':guardtask['guard_binding']['primary_row_sha256'],'control_role':guardtask['guard_binding']['control_role'],'guard_source_sha256':guardtask['guard_binding']['raw_sha256']},
 'new_actual_cells':1,'new_mathematical_proof_cells':0,'no_physical_reset':True,'no_native_trajectory_claim':True,
 'claim_firewall':'Conditional source-real actual admission using accepted V100 proof; not native-trajectory identity or independent physical confirmation.'
}
path=R/'q048_frec_moving_h_result_v101.json'; path.write_text(json.dumps(out,indent=2)+'\n')
print(path,sha(path))
