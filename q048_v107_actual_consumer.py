import json, hashlib, pathlib, datetime
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); REF=R/'q048_v107_reference'

def L(p): return json.load(open(p,encoding='utf-8'))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def canon_sha(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

PARENT=R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
THM=R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json'
THM_RAW=R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'
THM_VER=R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'
GUARD=REF/'Q048_FREC_MOVING_H_V97_NEXT_MATHEMATICS_TASK_V1.json'
V101=REF/'q048_frec_moving_h_result_v101.json'

expected={
 'parent':'cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098',
 'theorem':'5294bed5e3d32d71e396d933a5387c8c8f7538e1bc55c432b0b151fc0e9f9fe3',
 'theorem_raw':'e7b526416746e83005d353e4d6107c405cbb05646520f9fb0fea8b8756baef11',
 'theorem_ver':'e0793a3c8b543c5e8d6646c4df43d7f226759cced2aa471f1baeec1d708e2375',
 'guard_task':'9eddfede6d81fa9b260805e051a2213fb6790ef84e1baf0096ca2e94c4e8245c',
 'guard_row':'01e9f92295d60287f74a2760c1d38da42d2d37098a4d0dd32d1782dbf757b5ea',
 'v101_raw':'ca64e9f4cc58f0104c5212f963ca92827ccaeeb6a1bf25ea45a5e86158f3a492'
}
for p,k in [(PARENT,'parent'),(THM,'theorem'),(THM_RAW,'theorem_raw'),(THM_VER,'theorem_ver'),(GUARD,'guard_task'),(V101,'v101_raw')]:
 assert S(p)==expected[k], (p,S(p),expected[k])
parent=L(PARENT); theorem=L(THM); t_raw=L(THM_RAW); t_ver=L(THM_VER); guard=L(GUARD)['guard_binding']; hist=L(V101)
row=guard['primary']
assert canon_sha(row)==expected['guard_row']
assert parent['status']=='VALIDATED' and parent['accepted_actual']=={'count':110,'frontier':980}
assert theorem['status']=='ACCEPTED' and theorem['technical_state']=='PASS'
assert theorem['parent_authority']['checkpoint_sha256']==expected['parent']
assert theorem['parent_authority']['actual']=={'count':110,'frontier':980}
assert theorem['parent_authority']['endpoint']==parent['endpoint']
assert theorem['parent_authority']['correct_saha_fact']=='3.016103031869581e21'
assert theorem['proof_bridge_cell_z']==[980,970] and theorem['proof_bridge_cell_a']==['1/981','1/971']
assert theorem['raw_sha256']==expected['theorem_raw'] and theorem['verification_sha256']==expected['theorem_ver']
assert t_ver['status']=='PASS' and t_ver['checks_total']==t_ver['checks_passed']==36 and t_ver['semantic_mutations_total']==t_ver['semantic_mutations_rejected']==12
assert t_raw['bridge_checks']['guard_glue_exact'] and t_raw['bridge_checks']['no_physical_reset']
assert row['index']==47 and [row['z0'],row['z1']]==[980,970] and [row['a0'],row['a1']]==['1/981','1/971']
assert row['E_input_left']==parent['endpoint']['E'] and row['Y_left']==parent['endpoint']['Y'] and row['V_previous']==parent['endpoint']['Vbar']
assert row['source_state_reset'] is False and row['whole_cell_qualified'] and row['accepted'] and row['committed']
K=theorem['retained_theorem']['K_upper']; lower=theorem['retained_theorem']['connected_lower']
assert F(K)>0 and F(lower)>0
candidate={
 'count':111,'frontier':970,
 'frontiers':dict(parent['frontiers'],**{'hillipop-ede_n3':970}),
 'endpoint':{'a':'1/971','E':row['E_right'],'Y':row['Y_right'],'Vbar':row['V_admitted']},
 'connected_lower':lower,'K_upper':K
}
# Historical V101 is reference-only, but its numerical endpoint/bounds are an allowed cross-check.
assert candidate['endpoint']==hist['candidate_actual']['endpoint']
assert candidate['connected_lower']==hist['candidate_actual']['connected_lower']
assert candidate['K_upper']==hist['candidate_actual']['K_upper']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
question='For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?'
out={
 'schema':'bubbleverse.q048.v107.source_correct_actual_consumer.raw.v1','q':'Q048','target_q':'Q048',
 'exact_question':question,'question_sha256':hashlib.sha256(question.encode()).hexdigest(),
 'task_id':'LOCAL-Q048-V107-SOURCE-CORRECT-ACTUAL-CONSUMER-980-970-V1','program_id':'Q048-V107-SOURCE-CORRECT-CONSUMER-V1',
 'created_at_utc':now,'status':'PENDING_VALIDATION','technical_state':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE',
 'lineage':'NEW_SOURCE_CORRECT_REANALYSIS_LINEAGE_NOT_HISTORICAL_V101_REPLAY','cell_z':[980,970],'cell_a':['1/981','1/971'],
 'parent_authority':{'record':PARENT.name,'sha256':expected['parent'],'actual':parent['accepted_actual'],'frontiers':parent['frontiers'],'endpoint':parent['endpoint']},
 'theorem_authority':{'record':THM.name,'sha256':expected['theorem'],'raw_sha256':expected['theorem_raw'],'verification_sha256':expected['theorem_ver'],'correct_saha_fact':'3.016103031869581e21','K_upper':K,'connected_lower':lower,'thermal_domain':theorem['thermal_domain']},
 'guard_binding':{'index':47,'source_record':GUARD.name,'source_record_sha256':expected['guard_task'],'primary_row_sha256':expected['guard_row'],'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True},
 'consumer_checks':{'parent_validated':True,'theorem_accepted':True,'theorem_verifier_pass':True,'source_correct_prefactor':True,'parent_exact':True,'row47_hash_exact':True,'row47_glue_exact':True,'source_state_reset':False,'primary_row_committed':True,'connected_lower_positive':True,'K_positive':True},
 'candidate_actual':candidate,
 'historical_v101_reference_only':{'raw_sha256':expected['v101_raw'],'accepted_checkpoint_sha256':'270e615ae9ee8455ce5ddb1c0d28ff24efa478db1db0e09c55ce8015bf434686','numerical_endpoint_K_lower_match':True,'authority_used':False,'replayed':False},
 'new_actual_cells':1,'new_mathematical_proof_cells':0,'below970_work':False,'historical_record_modified':False,'no_physical_reset':True,'no_native_trajectory_claim':True,
 'q_complete':False,'NativeP6':'UNRESOLVED',
 'claim_firewall':'Validated source-correct actual admission may establish only this one 980->970 reanalysis-lineage cell. It does not transfer historical V101 execution identity, establish NativeP6, complete four-case histories/tau bounds, or close Q048.'
}
path=R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'; path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(path.name,S(path))
