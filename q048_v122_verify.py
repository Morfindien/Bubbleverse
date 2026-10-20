"""Separate source/identity/algebra checker;does not import producer."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy
P='Q048_V122_LOW_Z_DISPATCH_DIAGNOSTIC_'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def check(root,s,r):
 root=Path(root);I=root/'inputs';t=load(I/s['task_file']);p=load(I/s['parent']);e=load(I/'identity_journal_excerpt.json');c=(I/'source/hydrogen.c').read_text();k=(I/'q048_full_tube_reuse_v1.py').read_text();g=load(I/s['guard_file']);identity=r['obstruction']['identity'];a=r['threshold_algebra']
 row=g['evaluators'][0]['rows'][55];rh=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 # Polynomial coefficients after clearing a positive denominator and substituting g=1-h.
 cleared={'B':F(100)-1,'Bh':-F(100)+1,'C':-F(1),'Ch':F(1),'A':-F(3)}
 separately_expanded={'B':F(99),'Bh':F(-99),'C':F(-1),'Ch':F(1),'A':F(-3)}
 return {
 'schema':r['schema']=='bubbleverse.q048.v122.low_z_dispatch_diagnostic.raw.v1',
 'q_target':r['q']==r['target_q']==t['q']==t['target_q']=='Q048',
 'task':r['task_id']==s['task_id']==t['task_id'] and r['task_fingerprint']==s['task_fingerprint']==t['task_fingerprint'],
 'question':r['question_sha256']==s['question_sha256']==t['question_sha256'],
 'input_pins':all(sha(root/n)==pin['sha256'] and (root/n).stat().st_size==pin['bytes'] for n,pin in s['input_pins'].items()),
 'parent':r['parent_checkpoint_sha256']==s['parent_sha256']==sha(I/s['parent'])==t['parent_authority']['sha256'],
 'candidate':r['candidate_cell_z']==[900,890] and r['candidate_cell_a']==['1/901','1/891'],
 'row':r['guard_row55_sha256']==rh==t['guard']['primary_row_sha256'],
 'actual':r['actual_state_unchanged']==p['accepted_actual']=={'count':118,'frontier':900},
 'endpoint':r['parent_endpoint_unchanged']==p['endpoint'],
 'left_lower_preserved':r['parent_connected_lower_unchanged']==p['connected_lower'],
 'source_pins':r['source_sha256']=={'hydrogen.c':sha(I/'source/hydrogen.c'),'hydrogen.h':sha(I/'source/hydrogen.h'),'kernel':sha(I/'q048_full_tube_reuse_v1.py')},
 'source_dispatch':all(x in c for x in ['if (z < 900.)','Pion = 1.;','RLya       = LYA_FACT(1.,1.) *H/nH/(1.-xHII);','Pion       = four_betaB/(3.*RLya + L2s1s + four_betaB);','if (Pion < PION_MAX)']),
 'source_rate_identity':r['rate_equation_identity']['source_Dxe2']=='xe*xHII-s*(1-xHII)' and 'Dxe2 = xe*xHII - s*(1.-xHII)' in c,
 'kernel_h_identity':'alpha*h*(h+q)-alpha_eq*s*(1-h)' in k and r['rate_equation_identity']['kernel_barrier_term']=='alpha*h*(h+q)-alpha_eq*s*(1-h)',
 'journal_identity':any('h=xHII' in x['text'] for x in e['matches']) and r['journal_excerpt_sha256']==sha(I/'identity_journal_excerpt.json') and e['source_sha256']==s['journal_input']['sha256'],
 'task_conflict_actual':'h=1-xHII' in '\n'.join(t['source_branch_contract']['tube_obligations']) and identity['incoming_task_h']=='1-xHII',
 'canonical_identity':identity['canonical_h']==a['canonical_h']=='xHII' and identity['canonical_neutral_fraction']==a['neutral_g']=='1-h',
 'obstruction':r['status']=='FIRST_OBSTRUCTION' and r['obstruction']['gate']=='SOURCE_VARIABLE_IDENTITY' and r['obstruction']['code']=='TASK_NEUTRAL_H_CONFLICTS_WITH_CANONICAL_IONIZED_H' and identity['status']=='CONFLICT' and r['obstruction']['first_before_interval_execution'] is True,
 'parent_lower_not_relabelled':identity['affected_parent_lower']=='ionized_h_left_face_only;not neutral_fraction_lower',
 'correct_RLya':identity['correct_RLya']=='A/(1-h)',
 'correct_Pion':a['Pion']=='B/(3*A/(1-h)+C+B)' and a['source_variable']=='xHII',
 'correct_margin':a['margin']=='(1-h)*(99*B-C)-3*A' and identity['correct_threshold']=='(1-h)*(99*B-C)<3*A',
 'polynomial_algebra':cleared==separately_expanded,
 'domain':a['domain']=='0<h<1,A>0,B>0,C>0',
 'strict_HMLA':a['HMLA']=='margin<0',
 'equality_otherwise':a['otherwise']=='margin>=0;captured model/temperature gate still applies' and a['strict_equality_Pion']=='1/100',
 'exact900':a['at_exact900']=='Pion=1 before the low-z formula;not a below900 certificate',
 'zero_cells':r['new_actual_cells']==r['new_proof_cells']==r['new_full_connected_theorems']==0,
 'no_interval_promotion':r['interval_source_enclosures_computed'] is a['new_interval_certificate'] is False and r['new_K_upper']==r['new_connected_lower']=='NOT_COMPUTED',
 'no_trajectory_claim':r['actual_trajectory_claim'] is False,
 'history_firewall':r['historical_record_modified'] is r['q_complete'] is r['source_state_reset'] is False and r['NativeP6']=='UNRESOLVED' and r['scientific_state']=='INCONCLUSIVE',
 'no_authorization':r['consumer_authorization']==r['connected_cell_proof_authorization']=='NOT_GRANTED' and r['return_route']=='RESULT_INGESTION_ROUTING2.1.0',
 }
def mutations(r):
 controls=[('wrong_parent',('parent_checkpoint_sha256',),'0'*64),('wrong_task',('task_id',),'wrong'),('wrong_a',('candidate_cell_a',),['1/900','1/891']),('wrong_row',('guard_row55_sha256',),'1'*64),('source_hash',('source_sha256','hydrogen.c'),'2'*64),('Pion900',('threshold_algebra','at_exact900'),'Pion uses low-z formula at900'),('threshold_equality',('threshold_algebra','HMLA'),'margin<=0'),('drop_HMLA',('threshold_algebra','HMLA'),None),('old_h0_as_lower',('obstruction','identity','affected_parent_lower'),'neutral_fraction_lower'),('actual_promotion',('new_actual_cells',),1),('proof_promotion',('new_proof_cells',),1),('wrong_A',('threshold_algebra','Pion'),'B/(3*A*h+C+B)'),('wrong_B',('threshold_algebra','Pion'),'2*B/(3*A/(1-h)+C+B)'),('wrong_threshold',('threshold_algebra','strict_equality_Pion'),'1/99'),('wrong_small_margin',('threshold_algebra','margin'),'h*(99*B-C)-3*A'),('wrong_large_margin',('threshold_algebra','otherwise'),'margin>0'),('claim_trajectory',('actual_trajectory_claim',),True)]
 for name,path,value in controls:
  m=copy.deepcopy(r);target=m
  for k in path[:-1]:target=target[k]
  target[path[-1]]=value
  if m==r:raise ValueError('NO_OP_MUTATION:'+name)
  yield name,m
def main():
 root=Path(__file__).resolve().parent;s=load(root/(P+'SPEC_V1.json'));r=load(root/(P+'RAW_V1.json'));checks=check(root,s,r);rejected={}
 for name,m in mutations(r):rejected[name]=[k for k,v in check(root,s,m).items() if not v]
 ok=all(checks.values()) and all(rejected.values())
 out={'schema':'bubbleverse.q048.v122.low_z_dispatch_diagnostic.verification.v1','status':'PASS' if ok else 'FAIL','checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'semantic_mutations_total':len(rejected),'semantic_mutations_rejected':sum(bool(x) for x in rejected.values()),'mutation_failed_invariants':rejected,'raw_sha256':sha(root/(P+'RAW_V1.json')),'spec_sha256':sha(root/(P+'SPEC_V1.json')),'independence_scope':'Separate source/variable reconstruction and polynomial coefficient check;no producer import. Shares original pinned source/journal/helper evidence;not empirical replication.'}
 with (root/(P+'VERIFICATION_V1.json')).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({'status':out['status'],'checks':len(checks),'mutations_rejected':sum(bool(x) for x in rejected.values())}))
 if not ok:raise SystemExit(1)
if __name__=='__main__':main()
