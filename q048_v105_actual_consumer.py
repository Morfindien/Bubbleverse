import json, hashlib, pathlib, datetime
from fractions import Fraction as F
R=pathlib.Path('/mnt/data/q048_v105_builder'); I=R/'inputs'
def L(p): return json.load(open(p))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def H(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
parent=L(I/'q048_frec_moving_h_accepted_checkpoint_v95.json')
guard=L(I/'Q048_MOVING_H_DOMAIN_V96_NEXT_BUILDER_TASK_V1.json')['guard_binding']
th=L(I/'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json')
raw=L(I/'Q048_V104_V96_LINK_REANALYSIS_RAW_V1.json')
ver=L(I/'Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json')
# exact input identities
assert S(I/'q048_frec_moving_h_accepted_checkpoint_v95.json')=='b80dea63f9040b5d1aef01cd6a86e00a9f0ab35ba886eca4c09c9e9289ea3668'
assert S(I/'Q048_MOVING_H_DOMAIN_V96_NEXT_BUILDER_TASK_V1.json')=='fba21ced1163155f6a6e9917a44bc8ba0e7f0dbb3cb541e0f3965a3c74b3a447'
assert S(I/'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json')=='4cac1a8fb598001c6907163752a7a9bf6005de649546fade84658bdb0627b691'
assert S(I/'Q048_V104_V96_LINK_REANALYSIS_RAW_V1.json')==th['source_result_sha256']
assert S(I/'Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json')==th['verification_sha256']
# source-correct theorem
assert th['accepted'] is True and th['analysis_kind']=='NEW_VERSIONED_REANALYSIS_NOT_RECOVERED_V96'
assert th['cell_z']==[990,980] and th['cell_a']==['1/991','1/981']
assert th['correct_saha_fact']=='3.016103031869581e21'
assert th['verification_status']=='PASS_15_OF_15' and ver['status']=='PASS' and ver['checks_passed']==15 and ver['checks_total']==15
assert th['K_upper']=='2493577725162681856783/500000000000000000'
assert th['connected_lower']=='50514140794199/100000000000000000'
assert raw['status']=='PASS_FRESH_SOURCE_CORRECTED_990_980_THEOREM'
assert raw['correct_source_prefactor']=='3.016103031869581e21'
assert raw['new_actual_cells']==0 and raw['actual_consumer_executed'] is False
# parent actual
assert parent['accepted_actual']=={'count':109,'frontier':990}
assert parent['endpoint']=={'a':'1/991','E':'55162016731242447343/1000000000000000000','Y':'43899848634223684893/1000000000000000000','Vbar':'5396455546488157007/500000000000000000'}
assert parent['connected_lower']=='518482452340821/1000000000000000000'
# guard row46 exact canonical hashes and glue
row=guard['primary']; control=guard['control']
assert guard['row_index']==46
assert H(row)==guard['primary_row_sha256']=='cbbe0c68a50fcf51e9adf8ddf99c25ef73817b48ff2fadc95015413fbc40dfcb'
assert H(control)==guard['control_row_sha256']=='11f6f9055e77d32895a8a7bf5b8709c79f23cfd04d5756730c3d56fd6320a55e'
assert row['index']==46 and [row['z0'],row['z1']]==[990,980] and [row['a0'],row['a1']]==['1/991','1/981']
assert row['source_state_reset'] is False and row['whole_cell_qualified'] and row['accepted'] and row['committed']
assert row['E_input_left']==parent['endpoint']['E'] and row['Y_left']==parent['endpoint']['Y'] and row['V_previous']==parent['endpoint']['Vbar']
expected_endpoint={'a':'1/981','E':'13327406922059142279/250000000000000000','Y':'1696710572528996873/40000000000000000','Vbar':'10438035734386161987/1000000000000000000'}
assert row['E_right']==expected_endpoint['E'] and row['Y_right']==expected_endpoint['Y'] and row['V_admitted']==expected_endpoint['Vbar']
# produce exactly one new reanalysis-lineage actual cell
front=dict(parent['frontiers']); front['hillipop-ede_n3']=980
out={
 'schema':'bubbleverse.q048.v105.source_correct_actual_consumer.raw.v1','q':'Q048','target_q':'Q048',
 'exact_question':raw['exact_question'],'question_sha256':raw['question_sha256'],'source_commit':raw['source_commit'],
 'task_id':'LOCAL-Q048-V105-SOURCE-CORRECT-ACTUAL-CONSUMER-990-980-V1','result_id':'LOCAL-Q048-V105-SOURCE-CORRECT-ACTUAL-CONSUMER-990-980',
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PENDING_VALIDATION','technical_state':'PENDING_VALIDATION','scientific_state':'INCONCLUSIVE',
 'lineage':'NEW_REANALYSIS_LINEAGE_NOT_HISTORICAL_V97_REPLAY','cell_z':[990,980],'cell_a':['1/991','1/981'],
 'parent_actual':{'count':109,'frontier':990,'sha256':S(I/'q048_frec_moving_h_accepted_checkpoint_v95.json')},
 'consumed_theorem':{'checkpoint':'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json','sha256':S(I/'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json'),'raw_sha256':S(I/'Q048_V104_V96_LINK_REANALYSIS_RAW_V1.json'),'verification_sha256':S(I/'Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json'),'correct_saha_fact':'3.016103031869581e21','K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
 'guard_binding':{'index':46,'primary_row_sha256':guard['primary_row_sha256'],'control_row_sha256':guard['control_row_sha256'],'guard_source_sha256':guard['raw_sha256'],'control_role':guard['control_role']},
 'consumer_checks':{'theorem_accepted':True,'source_correct_prefactor':True,'verification_15_of_15':True,'parent_exact':True,'row46_hash_exact':True,'row46_glue_exact':True,'source_state_reset':False,'primary_row_committed':True,'connected_lower_positive':F(th['connected_lower'])>0,'K_positive':F(th['K_upper'])>0},
 'candidate_actual':{'count':110,'frontier':980,'frontiers':front,'endpoint':expected_endpoint,'connected_lower':th['connected_lower'],'K_upper':th['K_upper']},
 'new_actual_cells':1,'new_mathematical_proof_cells':0,'historical_v97_replayed':False,'historical_record_modified':False,
 'no_physical_reset':True,'no_native_trajectory_claim':True,'q_complete':False,'NativeP6':'UNRESOLVED',
 'claim_firewall':'Conditional source-real actual admission using fresh source-correct V104 theorem and exact historical row46 guard. This is current reassessment lineage, not historical V97 execution identity or full Q048 closure.'
}
path=R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'; path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'file':str(path),'sha256':S(path),'candidate_actual':out['candidate_actual']},indent=2))
