"""One source-variable identity diagnostic. No connected-cell theorem or evolution."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
P='Q048_V122_LOW_Z_DISPATCH_DIAGNOSTIC_'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def check_source(c,h,model):
 if model!=4:raise ValueError('CAPTURED_MODEL')
 if hashlib.sha256(c).hexdigest()!='734800ccd69b41d60b519f200003ce27c3b7640f76a70353499424842ba19616' or hashlib.sha256(h).hexdigest()!='1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52':raise ValueError('SOURCE_BYTE_PIN')
 if not all(z in c.decode() for z in ['Pion = 1.;','if (z < 900.)','Pion       = four_betaB/(3.*RLya + L2s1s + four_betaB);','if (Pion < PION_MAX)','(1.-xHII)']):raise ValueError('SOURCE_DISPATCH_TEXT')
 return True
def point_dispatch(z,neutral_fraction,A,B,C,temperature_gate):
 z,g,A,B,C=map(F,(z,neutral_fraction,A,B,C))
 if min(g,A,B,C)<=0 or g>1:raise ValueError('POSITIVE_SOURCE_DOMAIN')
 pi=F(1) if z>=900 else B/(3*A/g+C+B)
 dispatch='HMLA' if pi<F(1,100) or temperature_gate=='BELOW' else ('SWIFT' if temperature_gate=='READY' else 'SWIFT_SUBJECT_TO_TEMPERATURE_GATE')
 return {'Pion':str(pi),'dispatch':dispatch}
def reachable_tube_status(h_lower):
 return 'UNRESOLVED_NO_CONNECTED_H_LOWER' if h_lower is None else 'CONDITIONAL_PREMISE_ONLY'
def interval_cover(glo,ghi,Alo,Ahi,Blo,Bhi,Clo,Chi):
 glo,ghi,Alo,Ahi,Blo,Bhi,Clo,Chi=map(F,(glo,ghi,Alo,Ahi,Blo,Bhi,Clo,Chi))
 if not (0<glo<=ghi<=1 and 0<Alo<=Ahi and 0<Blo<=Bhi and 0<Clo<=Chi):raise ValueError('INTERVAL_DOMAIN')
 # Independent enclosure of strict threshold margin g*(99B-C)-3A.
 products=[g*d for g in (glo,ghi) for d in (99*Blo-Chi,99*Bhi-Clo)]
 lo=min(products)-3*Ahi;hi=max(products)-3*Alo
 return (['HMLA'] if lo<0 else [])+(['SWIFT_SUBJECT_TO_TEMPERATURE_GATE'] if hi>=0 else [])
def variable_identity(task,kernel,journal):
 stated='\n'.join(task['source_branch_contract']['tube_obligations'])
 if 'h=xHII' not in journal or 'alpha*h*(h+q)-alpha_eq*s*(1-h)' not in kernel:raise ValueError('CANONICAL_H_EVIDENCE_UNRESOLVED')
 return {'status':'CONFLICT' if 'h=1-xHII' in stated else 'CONSISTENT','canonical_h':'xHII','canonical_neutral_fraction':'1-h','incoming_task_h':'1-xHII' if 'h=1-xHII' in stated else 'NOT_CONFLICTING','affected_parent_lower':'ionized_h_left_face_only;not neutral_fraction_lower','correct_RLya':'A/(1-h)','correct_threshold':'(1-h)*(99*B-C)<3*A','C':'L2s1s','incoming_threshold':'h*(99*B-L2s1s)<3*A'}
def produce(root,spec):
 root=Path(root);I=root/'inputs'
 for name,pin in spec['input_pins'].items():
  p=root/name
  if sha(p)!=pin['sha256'] or p.stat().st_size!=pin['bytes']:raise ValueError('INPUT_PIN:'+name)
 task=load(I/spec['task_file']);parent=load(I/spec['parent']);state=load(I/spec['ingestion_state']);guard=load(I/spec['guard_file'])
 if sha(I/spec['parent'])!=task['parent_authority']['sha256'] or parent['accepted_actual']!={'count':118,'frontier':900}:raise ValueError('PARENT')
 if state['next_task_id']!=spec['task_id'] or task['task_fingerprint']!=spec['task_fingerprint']:raise ValueError('AUTHORIZATION')
 check_source((I/'source/hydrogen.c').read_bytes(),(I/'source/hydrogen.h').read_bytes(),4)
 cap=load(I/'q048_prefix_config_v1.json');case=cap['cases']['hillipop-ede_n3']
 if not all(x['HyRec_MODEL']==4 for x in case['thermal_starts']):raise ValueError('CAPTURED_MODEL')
 evidence=load(I/'identity_journal_excerpt.json');journal='\n'.join(x['text'] for x in evidence['matches'])
 identity=variable_identity(task,(I/'q048_full_tube_reuse_v1.py').read_text(),journal)
 if identity['status']!='CONFLICT':raise ValueError('EXPECTED_SOURCE_CONTRACT_DIAGNOSTIC_CHANGED')
 row=guard['evaluators'][0]['rows'][55]
 return {'schema':'bubbleverse.q048.v122.low_z_dispatch_diagnostic.raw.v1','q':'Q048','target_q':'Q048','task_id':spec['task_id'],'task_fingerprint':spec['task_fingerprint'],'question_sha256':spec['question_sha256'],'status':'FIRST_OBSTRUCTION','technical_state':'PENDING_VERIFICATION','scientific_state':'INCONCLUSIVE','obstruction':{'gate':'SOURCE_VARIABLE_IDENTITY','code':'TASK_NEUTRAL_H_CONFLICTS_WITH_CANONICAL_IONIZED_H','first_before_interval_execution':True,'identity':identity},'source_sha256':{'hydrogen.c':sha(I/'source/hydrogen.c'),'hydrogen.h':sha(I/'source/hydrogen.h'),'kernel':sha(I/'q048_full_tube_reuse_v1.py')},'parent_checkpoint_sha256':sha(I/spec['parent']),'candidate_cell_z':[900,890],'candidate_cell_a':['1/901','1/891'],'guard_row55_sha256':hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),'journal_excerpt_sha256':sha(I/'identity_journal_excerpt.json'),'threshold_algebra':{'source_variable':'xHII','canonical_h':'xHII','neutral_g':'1-h','domain':'0<h<1,A>0,B>0,C>0','Pion':'B/(3*A/(1-h)+C+B)','margin':'(1-h)*(99*B-C)-3*A','HMLA':'margin<0','otherwise':'margin>=0;captured model/temperature gate still applies','at_exact900':'Pion=1 before the low-z formula;not a below900 certificate','strict_equality_Pion':'1/100','new_interval_certificate':False},'rate_equation_identity':{'source_Dxe2':'xe*xHII-s*(1-xHII)','canonical_substitution':'xe=h+q gives h*(h+q)-s*(1-h)','kernel_barrier_term':'alpha*h*(h+q)-alpha_eq*s*(1-h)','neutral_relabel_would_change':'recombination product and inherited connected_lower meaning'},'required_repair':'New versioned ingestion task must retain h=xHII,define separate neutral_g=1-h,and use neutral_g in RLya/Pion threshold. Do not relabel old checkpoints or copy ionized h0 into neutral g0.','actual_state_unchanged':parent['accepted_actual'],'parent_endpoint_unchanged':parent['endpoint'],'parent_connected_lower_unchanged':parent['connected_lower'],'source_state_reset':False,'new_actual_cells':0,'new_proof_cells':0,'new_full_connected_theorems':0,'interval_source_enclosures_computed':False,'new_K_upper':'NOT_COMPUTED','new_connected_lower':'NOT_COMPUTED','actual_trajectory_claim':False,'historical_record_modified':False,'q_complete':False,'NativeP6':'UNRESOLVED','consumer_authorization':'NOT_GRANTED','connected_cell_proof_authorization':'NOT_GRANTED','return_route':'RESULT_INGESTION_ROUTING2.1.0'}
def main():
 root=Path(__file__).resolve().parent;s=load(root/(P+'SPEC_V1.json'));r=produce(root,s)
 with (root/(P+'RAW_V1.json')).open('x') as f:json.dump(r,f,indent=2);f.write('\n')
 print(json.dumps({'status':r['status'],'obstruction':r['obstruction']['code'],'new_actual_cells':0,'new_proof_cells':0}))
if __name__=='__main__':main()
