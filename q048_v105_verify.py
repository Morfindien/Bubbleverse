import json, hashlib, pathlib
from fractions import Fraction as F
R=pathlib.Path('/mnt/data/q048_v105_builder'); I=R/'inputs'
def L(p): return json.load(open(p))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def H(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'); p=L(I/'q048_frec_moving_h_accepted_checkpoint_v95.json'); g=L(I/'Q048_MOVING_H_DOMAIN_V96_NEXT_BUILDER_TASK_V1.json')['guard_binding']; t=L(I/'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json'); v=L(I/'Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json'); rr=L(I/'Q048_V104_V96_LINK_REANALYSIS_RAW_V1.json')
row=g['primary']; checks={}
def C(n,x): checks[n]=bool(x)
C('identity',r['q']=='Q048' and r['target_q']=='Q048' and r['cell_z']==[990,980])
C('parent_hash',r['parent_actual']['sha256']==S(I/'q048_frec_moving_h_accepted_checkpoint_v95.json')=='b80dea63f9040b5d1aef01cd6a86e00a9f0ab35ba886eca4c09c9e9289ea3668')
C('parent_state',p['accepted_actual']=={'count':109,'frontier':990})
C('theorem_hash',r['consumed_theorem']['sha256']==S(I/'Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json')=='4cac1a8fb598001c6907163752a7a9bf6005de649546fade84658bdb0627b691')
C('theorem_cell',t['accepted'] and t['cell_z']==[990,980] and t['cell_a']==['1/991','1/981'])
C('source_correct',t['correct_saha_fact']=='3.016103031869581e21' and rr['correct_source_prefactor']=='3.016103031869581e21')
C('theorem_verification',t['verification_status']=='PASS_15_OF_15' and v['status']=='PASS' and v['checks_total']==15 and v['checks_passed']==15)
C('theorem_zero_actual',t['new_actual_cells']==0 and rr['new_actual_cells']==0)
C('row46_hash',H(row)==g['primary_row_sha256']=='cbbe0c68a50fcf51e9adf8ddf99c25ef73817b48ff2fadc95015413fbc40dfcb')
C('control_hash',H(g['control'])==g['control_row_sha256']=='11f6f9055e77d32895a8a7bf5b8709c79f23cfd04d5756730c3d56fd6320a55e')
C('row46_cell',row['index']==46 and [row['z0'],row['z1']]==[990,980] and [row['a0'],row['a1']]==['1/991','1/981'])
C('glue_E',F(row['E_input_left'])==F(p['endpoint']['E']))
C('glue_Y',F(row['Y_left'])==F(p['endpoint']['Y']))
C('glue_V',F(row['V_previous'])==F(p['endpoint']['Vbar']))
C('no_reset',row['source_state_reset'] is False and r['no_physical_reset'] is True)
C('row_committed',row['accepted'] and row['committed'] and row['whole_cell_qualified'])
C('actual_count',r['candidate_actual']['count']==110 and r['new_actual_cells']==1 and r['new_mathematical_proof_cells']==0)
C('actual_frontier',r['candidate_actual']['frontier']==980 and r['candidate_actual']['frontiers']['hillipop-ede_n3']==980)
C('endpoint',r['candidate_actual']['endpoint']=={'a':'1/981','E':row['E_right'],'Y':row['Y_right'],'Vbar':row['V_admitted']})
C('lower',F(r['candidate_actual']['connected_lower'])==F(t['connected_lower']) and F(t['connected_lower'])>0)
C('K',F(r['candidate_actual']['K_upper'])==F(t['K_upper']) and F(t['K_upper'])>0)
C('history_firewall',r['historical_v97_replayed'] is False and r['historical_record_modified'] is False and r['lineage']=='NEW_REANALYSIS_LINEAGE_NOT_HISTORICAL_V97_REPLAY')
C('q_firewall',r['q_complete'] is False and r['NativeP6']=='UNRESOLVED' and r['scientific_state']=='INCONCLUSIVE')
mut=[
 ('wrong_parent_count',110!=p['accepted_actual']['count']),('wrong_parent_frontier',980!=p['accepted_actual']['frontier']),('wrong_cell',[980,970]!=r['cell_z']),('wrong_saha','3.016101031869581e21'!=t['correct_saha_fact']),('old_parent_lower',F(p['connected_lower'])!=F(r['candidate_actual']['connected_lower'])),('old_parent_K',F(p['K_upper'])!=F(r['candidate_actual']['K_upper'])),('synthetic_endpoint',F('1/971')!=F(r['candidate_actual']['endpoint']['a'])),('control_as_actual',g['control']['E_right']!=r['candidate_actual']['endpoint']['E']),('reset_true',True!=row['source_state_reset']),('historical_replay',True!=r['historical_v97_replayed']),('extra_actual',111!=r['candidate_actual']['count']),('below980',970!=r['candidate_actual']['frontier'])]
status=all(checks.values()) and all(x[1] for x in mut)
out={'schema':'bubbleverse.q048.v105.source_correct_actual_consumer.validation.v1','q':'Q048','target_q':'Q048','status':'PASS' if status else 'FAIL','technical_state':'PASS' if status else 'FAIL','result_sha256':S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'),'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'semantic_mutations_total':len(mut),'semantic_mutations_rejected':sum(x[1] for x in mut),'mutations':[{'name':n,'rejected':x} for n,x in mut],'producer_imported_or_executed':False,'verification_scope':'Separate consumer-level semantic recomputation from pinned V104 theorem, exact V95 parent and exact row46 guard. Does not rerun the V104 proof and is not independent physical evidence.'}
path=R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_VALIDATION_V1.json'; path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'file':str(path),'sha256':S(path),'status':out['status'],'checks':f"{out['checks_passed']}/{out['checks_total']}",'mutations':f"{out['semantic_mutations_rejected']}/{out['semantic_mutations_total']}"},indent=2))
