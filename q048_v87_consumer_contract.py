"""Strict V87 metadata contract: archived lineage and interfaces only, no science mains."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
ROOT=Path(__file__).resolve().parent
TASK='Q048_MOVING_H_DOMAIN_V86_NEXT_BUILDER_TASK_V1.json'
PARENT='q048_frec_moving_h_accepted_checkpoint_v85.json'
PROOF='q048_moving_h_domain_accepted_checkpoint_v86.json'
RAW='q048_frec_moving_h_result_v87.json'
SPEC='q048_frec_moving_h_spec_v87.json'
QUESTION_HASH='c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def require(ok,label):
 if not ok:raise ValueError(label)
def output(name,data):
 with (ROOT/name).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def checked_path(rel):
 p=Path(rel);require(not p.is_absolute() and '..' not in p.parts,'UNSAFE_PATH');return ROOT/p
def validate_spec(s,verify_files=True):
 checks=[]
 def c(k,ok):require(ok,k);checks.append({'check':k,'pass':True})
 fields={'schema':str,'q':str,'target_q':str,'exact_question':str,'question_sha256':str,'task_id':str,'task_fingerprint':str,'program_id':str,'source_commit':str,'capture_sha256':str,'contract_markdown_path':str,'contract_markdown_sha256':str,'input_pins':dict,'code_pins':dict,'execution_fingerprint_basis':dict,'execution_fingerprint':str,'science_budget_seconds':int}
 for k,t in fields.items():c('required:'+k,k in s and type(s[k]) is t)
 c('scope',s['q']==s['target_q']=='Q048');c('question',hashlib.sha256(s['exact_question'].encode()).hexdigest()==s['question_sha256']==QUESTION_HASH)
 c('task_id',s['task_id']=='LOCAL-Q048-POST-V86-ACTUAL-CONSUMER-1040-1030-V1');c('budget',s['science_budget_seconds']==300);c('contract_hash_format',len(s['contract_markdown_sha256'])==64)
 b=s['execution_fingerprint_basis'];c('execution_fingerprint',digest(b)==s['execution_fingerprint'])
 for k in ['task_fingerprint','input_pins','code_pins','contract_markdown_path','contract_markdown_sha256','question_sha256','science_budget_seconds']:c('fingerprint_bind:'+k,b.get(k)==s[k])
 c('one_actual_no_proof',b.get('cell_z')==[1040,1030] and b.get('max_new_actual_cells')==1 and b.get('max_new_math_proof_cells')==0)
 if not verify_files:return checks
 c('contract_bytes',sha(checked_path(s['contract_markdown_path']))==s['contract_markdown_sha256'])
 expected_math='d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d'
 for rel in ['inputs/q047_math_v1.py','inputs/source/q047_math_v1.py']:
  c('required_transitive_path_pin:'+rel,rel in s['input_pins'] and s['input_pins'][rel]=={'sha256':expected_math,'bytes':12617})
  c('required_transitive_path_bytes:'+rel,checked_path(rel).is_file() and sha(checked_path(rel))==expected_math)

 for group in ['input_pins','code_pins']:
  for rel,pin in s[group].items():
   p=checked_path(rel);c(group+':'+rel,p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'])
 task=load(ROOT/'inputs'/TASK);parent=load(ROOT/'inputs'/PARENT);proof=load(ROOT/'inputs'/PROOF);pr=load(ROOT/'inputs/q048_moving_h_domain_result_v86.json')
 c('planning_fingerprint',digest(task['fingerprint_basis'])==task['task_fingerprint']==s['task_fingerprint'])
 c('task_question',task['exact_question']==s['exact_question'] and task['question_sha256']==s['question_sha256'])
 c('fixed_source_capture',task['fingerprint_basis']['source_commit']==parent['source_commit']==proof['source_commit']==s['source_commit'] and task['fingerprint_basis']['capture_sha256']==parent['capture_sha256']==proof['capture_sha256']==s['capture_sha256'])
 c('parent_accepted',parent['checkpoint_kind']=='ACCEPTED_ACTUAL' and parent['status']=='VALIDATED' and parent['technical_state']=='PASS' and parent['accepted_actual']=={'count':104,'frontier':1040})
 initial=task['initial_actual_state'];after=task['candidate_success_state'];pm=task['accepted_math_proof']
 c('parent_hash',sha(ROOT/'inputs'/PARENT)==initial['accepted_checkpoint_sha256'])
 c('parent_state',parent['endpoint']==initial['endpoint'] and parent['frontiers']==initial['frontiers'] and parent['connected_lower']==initial['connected_lower'])
 c('proof_accepted',proof['checkpoint_kind']=='ACCEPTED_MATHEMATICAL_PROOF' and proof['status']=='VALIDATED' and proof['technical_state']=='PASS' and proof['total_actual_paired_cells']==104 and proof['new_actual_paired_cells']==0 and proof['new_mathematical_proof_cells']==1)
 c('proof_hash',sha(ROOT/'inputs'/PROOF)==pm['checkpoint_sha256']==task['fingerprint_basis']['accepted_proof_checkpoint_sha256'])
 c('proof_domain_parent',proof['proof_cell_z']==[1040,1030] and proof['proof_cell_a']==['1/1041','1/1031'] and proof['parent_actual_checkpoint_sha256']==sha(ROOT/'inputs'/PARENT))
 c('proof_actual_retained',proof['actual_frontiers']==parent['frontiers'] and proof['actual_scalar_endpoint']==parent['endpoint'])
 c('proof_lower_K',proof['comparison_start_lower']==parent['connected_lower']==pr['comparison']['initial_lower'] and proof['comparison_endpoint_lower']==after['connected_lower']==pm['whole_cell_lower']==pr['comparison']['whole_cell_h_min'] and proof['comparison_K_upper']==after['K_upper']==pm['K_upper']==pr['comparison']['K_upper'])
 for ver,kind,cp,nc,nm,npost in [(85,'frec_moving_h',parent,109,43,18),(86,'moving_h_domain',proof,107,45,17)]:
  base=f'q048_{kind}_';rp=ROOT/'inputs'/f'{base}result_v{ver}.json';vp=ROOT/'inputs'/f'{base}validation_v{ver}.json';tp=ROOT/'inputs'/f'{base}transition_validation_v{ver}.json';ap=ROOT/'inputs'/f'{base}acceptance_validation_v{ver}.json';pp=ROOT/'inputs'/f'{base}postaccept_validation_v{ver}.json';v,t,a,p=map(load,[vp,tp,ap,pp])
  c('prior_raw:'+str(ver),sha(rp)==cp['source_result_sha256']==v['result_sha256']==t['result_sha256'])
  c('prior_validation:'+str(ver),sha(vp)==cp['validation_sha256']==t['validation_sha256']==a['validation_sha256'])
  c('prior_transition:'+str(ver),sha(tp)==cp['transition_validation_sha256']==a['transition_sha256'])
  c('prior_acceptance:'+str(ver),sha(ROOT/'inputs'/(PARENT if ver==85 else PROOF))==a['accepted_checkpoint_sha256']==p['accepted_checkpoint_sha256'] and sha(ap)==p['acceptance_validation_sha256'])
  c('prior_validation_pass:'+str(ver),v['status']=='PASS' and v['checks_total']==v['checks_passed']==nc and v['mutations_total']==v['mutations_rejected']==nm)
  c('prior_postaccept_pass:'+str(ver),t['status']==a['status']==p['status']=='PASS' and t['checks_total']==t['checks_passed']==nc and p['checks_total']==p['checks_passed']==npost)
 guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json');gv=load(ROOT/'inputs/q048_guard_local_v_validation_v12.json')
 c('guard_raw',sha(ROOT/'inputs/q048_guard_local_v_result_v12.json')==task['guard_binding']['raw_sha256']==gv['result_sha256'])
 c('guard_validation',sha(ROOT/'inputs/q048_guard_local_v_validation_v12.json')==task['guard_binding']['validation_sha256'] and gv['technical_state']=='PASS' and gv['checks_total']==gv['checks_passed']==6566 and gv['mutations_total']==gv['mutations_rejected']==24)
 for label,ev in zip(['primary','control'],guard['evaluators']):
  row=ev['rows'][41];c('guard_domain:'+label,[row['z0'],row['z1']]==[1040,1030] and row['a0']=='1/1041' and row['a1']=='1/1031')
  c('guard_hash:'+label,digest(row)==task['guard_binding'][label+'_row_sha256']==pr['guard_'+label+'_row_sha256'] and row==task['guard_binding'][label])
  c('guard_admission:'+label,row['accepted'] is True and row['committed'] is True and row['whole_cell_qualified'] is True and row['source_state_reset'] is False and row['domain']['admitted'] is True and all(row['domain']['checks'].values()) and F(row['G_lower'])>0)
 row=guard['evaluators'][0]['rows'][41];ep=parent['endpoint']
 c('primary_start_glue',row['a0']==ep['a'] and row['E_input_left']==ep['E'] and row['Y_left']==ep['Y'] and row['V_previous']==ep['Vbar'])
 c('candidate_endpoint',after['count']==105 and after['frontier']==1030 and after['frontiers']=={**parent['frontiers'],'hillipop-ede_n3':1030} and after['endpoint']=={'a':row['a1'],'E':row['E_right'],'Y':row['Y_right'],'Vbar':row['V_admitted']})
 c('capture',sha(ROOT/'inputs/q048_prefix_config_v1.json')==s['capture_sha256'])
 c('prompt',sha(ROOT/'inputs/Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0-52.md')==task['engine']['prompt_sha256']=='49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1')
 return checks
def load_spec():
 s=load(ROOT/SPEC);validate_spec(s);return s
