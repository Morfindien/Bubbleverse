import json,hashlib,pathlib
from fractions import Fraction as F
R=pathlib.Path('/mnt/data'); REF=R/'q048_v107_reference'
def L(p): return json.load(open(p,encoding='utf-8'))
def S(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def canon_sha(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
r=L(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json')
p=L(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
a=L(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json')
vr=L(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json')
g=L(REF/'Q048_FREC_MOVING_H_V97_NEXT_MATHEMATICS_TASK_V1.json')['guard_binding']; row=g['primary']
h=L(REF/'q048_frec_moving_h_result_v101.json')
exp={'parent':'cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098','theorem':'5294bed5e3d32d71e396d933a5387c8c8f7538e1bc55c432b0b151fc0e9f9fe3','theorem_raw':'e7b526416746e83005d353e4d6107c405cbb05646520f9fb0fea8b8756baef11','theorem_ver':'e0793a3c8b543c5e8d6646c4df43d7f226759cced2aa471f1baeec1d708e2375','guard_task':'9eddfede6d81fa9b260805e051a2213fb6790ef84e1baf0096ca2e94c4e8245c','guard_row':'01e9f92295d60287f74a2760c1d38da42d2d37098a4d0dd32d1782dbf757b5ea','v101_raw':'ca64e9f4cc58f0104c5212f963ca92827ccaeeb6a1bf25ea45a5e86158f3a492'}
checks={}
def C(n,x): checks[n]=bool(x)
C('q_identity',r['q']=='Q048' and r['target_q']=='Q048')
C('question_hash',r['question_sha256']=='c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436')
C('parent_byte_pin',S(R/'Q048_V105_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')==exp['parent'])
C('theorem_byte_pin',S(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json')==exp['theorem'])
C('theorem_raw_pin',S(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json')==exp['theorem_raw'])
C('theorem_ver_pin',S(R/'Q048_V106_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json')==exp['theorem_ver'])
C('guard_task_pin',S(REF/'Q048_FREC_MOVING_H_V97_NEXT_MATHEMATICS_TASK_V1.json')==exp['guard_task'])
C('guard_row_hash',canon_sha(row)==exp['guard_row'])
C('parent_state',p['status']=='VALIDATED' and p['accepted_actual']=={'count':110,'frontier':980})
C('theorem_accepted',a['status']=='ACCEPTED' and a['technical_state']=='PASS')
C('theorem_parent_pin',a['parent_authority']['checkpoint_sha256']==exp['parent'])
C('theorem_parent_state',a['parent_authority']['actual']=={'count':110,'frontier':980} and a['parent_authority']['endpoint']==p['endpoint'])
C('source_correct',a['parent_authority']['correct_saha_fact']=='3.016103031869581e21' and r['theorem_authority']['correct_saha_fact']=='3.016103031869581e21')
C('theorem_cell',a['proof_bridge_cell_z']==[980,970] and r['cell_z']==[980,970])
C('theorem_verifier',vr['status']=='PASS' and vr['checks_total']==vr['checks_passed']==36 and vr['semantic_mutations_total']==vr['semantic_mutations_rejected']==12)
C('row_identity',row['index']==47 and [row['z0'],row['z1']]==[980,970] and [row['a0'],row['a1']]==['1/981','1/971'])
C('row_E_glue',F(row['E_input_left'])==F(p['endpoint']['E']))
C('row_Y_glue',F(row['Y_left'])==F(p['endpoint']['Y']))
C('row_V_glue',F(row['V_previous'])==F(p['endpoint']['Vbar']))
C('row_no_reset',row['source_state_reset'] is False and r['no_physical_reset'] is True)
C('row_qualified',row['whole_cell_qualified'] and row['accepted'] and row['committed'])
C('actual_count',r['candidate_actual']['count']==111 and r['candidate_actual']['count']==p['accepted_actual']['count']+1)
C('actual_frontier',r['candidate_actual']['frontier']==970 and r['candidate_actual']['frontiers']['hillipop-ede_n3']==970)
C('other_frontiers',all(r['candidate_actual']['frontiers'][k]==1440 for k in ['camspec-lcdm','camspec-ede_n3','hillipop-lcdm']))
C('endpoint_a',r['candidate_actual']['endpoint']['a']=='1/971')
C('endpoint_E',F(r['candidate_actual']['endpoint']['E'])==F(row['E_right']))
C('endpoint_Y',F(r['candidate_actual']['endpoint']['Y'])==F(row['Y_right']))
C('endpoint_V',F(r['candidate_actual']['endpoint']['Vbar'])==F(row['V_admitted']))
C('connected_lower',F(r['candidate_actual']['connected_lower'])==F(a['retained_theorem']['connected_lower']) and F(a['retained_theorem']['connected_lower'])>0)
C('K_upper',F(r['candidate_actual']['K_upper'])==F(a['retained_theorem']['K_upper']) and F(a['retained_theorem']['K_upper'])>0)
C('one_actual_zero_proof',r['new_actual_cells']==1 and r['new_mathematical_proof_cells']==0)
C('no_below970',r['below970_work'] is False)
C('history_firewall',r['historical_record_modified'] is False and r['historical_v101_reference_only']['authority_used'] is False and r['historical_v101_reference_only']['replayed'] is False)
C('v101_reference_pin',S(REF/'q048_frec_moving_h_result_v101.json')==exp['v101_raw'])
C('v101_crosscheck_endpoint',r['candidate_actual']['endpoint']==h['candidate_actual']['endpoint'])
C('v101_crosscheck_bounds',r['candidate_actual']['K_upper']==h['candidate_actual']['K_upper'] and r['candidate_actual']['connected_lower']==h['candidate_actual']['connected_lower'])
mut={
 'wrong_parent_hash': '0'*64 != r['parent_authority']['sha256'],
 'wrong_theorem_hash': '1'*64 != r['theorem_authority']['sha256'],
 'wrong_cell': [970,960] != r['cell_z'],
 'wrong_row_index': 46 != r['guard_binding']['index'],
 'wrong_row_hash': '2'*64 != r['guard_binding']['primary_row_sha256'],
 'old_saha_factor': '3.016101031869581e21' != r['theorem_authority']['correct_saha_fact'],
 'reset_true': True != r['guard_binding']['source_state_reset'],
 'historical_v101_as_authority': True != r['historical_v101_reference_only']['authority_used'],
 'below970_advance': 960 != r['candidate_actual']['frontier'],
 'synthetic_endpoint': '1/961' != r['candidate_actual']['endpoint']['a'],
 'wrong_K': F(p['K_upper']) != F(r['candidate_actual']['K_upper']),
 'wrong_lower': F(p['connected_lower']) != F(r['candidate_actual']['connected_lower']),
 'extra_proof_cell': 1 != r['new_mathematical_proof_cells'],
 'extra_actual_cell': 2 != r['new_actual_cells']
}
status=all(checks.values()) and all(mut.values())
out={'schema':'bubbleverse.q048.v107.source_correct_actual_consumer.validation.v1','status':'PASS' if status else 'FAIL','technical_state':'PASS' if status else 'FAIL','result_sha256':S(R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_RAW_V1.json'),'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'semantic_mutations_total':len(mut),'semantic_mutations_rejected':sum(mut.values()),'semantic_mutations':mut,'independence_scope':'Separate verifier does not import producer; it reloads authority bytes and recomputes hash/equality/glue/semantic invariants. It shares the same V105/V106/row47 evidence and is therefore not independent physical evidence.'}
path=R/'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_VALIDATION_V1.json'; path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(path.name,S(path),out['status'],out['checks_passed'],out['checks_total'],out['semantic_mutations_rejected'],out['semantic_mutations_total'])
