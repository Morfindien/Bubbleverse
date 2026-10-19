# RECONSTRUCTED / NON-AUTHORITATIVE / DIAGNOSTIC ONLY
# NOT the original historical V98 byte stream.
# Basis: preserved V92 family code + V98 spec/freeze/execution evidence.
# Never use to claim historical V98 SHA256 or accepted proof.
# V98-only additions absent from V92 are unknown and intentionally not invented.
"""Strict V98 metadata and lineage checks; no mathematical producer runs here."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parent
TASK='Q048_FREC_MOVING_H_V91R1_NEXT_MATHEMATICS_TASK_V1.json'
PARENT='q048_frec_moving_h_accepted_checkpoint_v91r1.json'
RAW='q048_moving_h_domain_result_v98.json'
SPEC='q048_moving_h_domain_spec_v98.json'
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x): return hashlib.sha256(canonical(x)).hexdigest()
def require(ok,label):
    if not ok: raise ValueError(label)
def output(name,data):
    with (ROOT/name).open('x') as f: json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
def safe(rel):
    p=Path(rel); require(not p.is_absolute() and '..' not in p.parts,'UNSAFE_PATH'); resolved=(ROOT/p).resolve(); require(resolved.is_relative_to(ROOT),'UNSAFE_PATH'); return resolved
def validate_spec(s,verify_files=True):
    checks=[]
    def c(k,ok): require(ok,k); checks.append({'check':k,'pass':True})
    fields={'schema':str,'q':str,'target_q':str,'exact_question':str,'question_sha256':str,'source_commit':str,'capture_sha256':str,'task_id':str,'task_fingerprint':str,'program_id':str,'contract_markdown_path':str,'contract_markdown_sha256':str,'input_pins':dict,'code_pins':dict,'execution_fingerprint_basis':dict,'execution_fingerprint':str,'science_budget_seconds':int,'parent_raw_sha256_inherited':str,'parent_validation_sha256_inherited':str,'preimplementation_spec_sha256':str}
    for k,t in fields.items(): c('required:'+k,k in s and type(s[k]) is t)
    c('Q_boundary',s['q']==s['target_q']=='Q048')
    c('question',hashlib.sha256(s['exact_question'].encode()).hexdigest()==s['question_sha256']=='c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436')
    c('task_id',s['task_id']=='LOCAL-Q048-POST-V91R1-MOVING-H-DOMAIN-1010-1000-MATH-V1')
    c('budget',s['science_budget_seconds']==300)
    b=s['execution_fingerprint_basis']; c('fingerprint',digest(b)==s['execution_fingerprint'])
    for k in ['input_pins','code_pins','contract_markdown_path','contract_markdown_sha256','task_fingerprint','question_sha256','science_budget_seconds','parent_raw_sha256_inherited','parent_validation_sha256_inherited','preimplementation_spec_sha256','source_commit','capture_sha256','program_id']: c('fingerprint_bind:'+k,b.get(k)==s[k])
    c('one_proof_only',b.get('cell_z')==[1010,1000] and b.get('max_new_math_proof_cells')==1 and b.get('max_new_actual_cells')==0)
    required_math={'bytes':12617,'sha256':'d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d'}
    for rel in ['inputs/q047_math_v1.py','inputs/source/q047_math_v1.py']: c('required_import_layout:'+rel,s['input_pins'].get(rel)==required_math)
    c('required_code_set',set(s['code_pins'])=={'q048_v98_proof_contract.py','q048_moving_h_domain_v98.py','q048_moving_h_domain_verify_v98.py','q048_moving_h_domain_accept_v98.py','q048_v98_import_probe.py','q048_v98_freeze_and_execute.py','test_q048_moving_h_v98.py','test_q048_v98_layout.py','test_q048_v98_paths.py'})
    if not verify_files: return checks
    c('preimplementation_bytes',sha(ROOT/'q048_v98_preimplementation_spec.json')==s['preimplementation_spec_sha256'])
    c('exact_task_identity',s['task_fingerprint']=='05f22a5747b13f1c861d0b5aada266a4819704e75c89f276e2786bb91cb475b2')
    c('contract_bytes',safe(s['contract_markdown_path']).is_file() and sha(safe(s['contract_markdown_path']))==s['contract_markdown_sha256'])
    for group in ['input_pins','code_pins']:
        for rel,pin in s[group].items():
            p=safe(rel); c(group+':'+rel,p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'])
    task=load(ROOT/'inputs'/TASK); cp=load(ROOT/'inputs'/PARENT)
    c('planning_identity',digest(task['fingerprint_basis'])==task['task_fingerprint']==s['task_fingerprint'])
    c('question_task',task['exact_question']==s['exact_question'] and task['question_sha256']==s['question_sha256'])
    c('fixed_source',task['fingerprint_basis']['source_commit']==s['source_commit']==cp['source_commit'])
    c('fixed_capture',task['fingerprint_basis']['capture_sha256']==s['capture_sha256']==cp['capture_sha256'])
    initial=task['initial_actual_state']
    c('parent_hash',sha(ROOT/'inputs'/PARENT)==initial['accepted_checkpoint_sha256'])
    c('parent_accepted',cp['checkpoint_kind']=='ACCEPTED_ACTUAL' and cp['status']=='VALIDATED' and cp['technical_state']=='PASS' and cp['accepted_actual']=={'count':107,'frontier':1010})
    c('parent_endpoint',cp['endpoint']==initial['endpoint'] and cp['frontiers']==initial['frontiers'])
    c('parent_lower',cp['connected_lower']==initial['connected_lower'] and F(cp['connected_lower'])>0)
    c('preserve_actual',task['accepted_actual_state_must_remain']==initial)
    c('parent_raw_provenance',cp['source_result_sha256']==s['parent_raw_sha256_inherited']==task['fingerprint_basis']['parent_raw_sha256'])
    c('parent_validation_provenance',cp['validation_sha256']==s['parent_validation_sha256_inherited']==task['fingerprint_basis']['parent_validation_sha256'])
    # Archived parent evidence is inspected as metadata, never replayed.
    pr=load(ROOT/'inputs/q048_frec_moving_h_result_v91r1.json');pv=load(ROOT/'inputs/q048_frec_moving_h_validation_v91r1.json');pt=load(ROOT/'inputs/q048_frec_moving_h_transition_validation_v91r1.json');pa=load(ROOT/'inputs/q048_frec_moving_h_acceptance_validation_v91r1.json');pp=load(ROOT/'inputs/q048_frec_moving_h_postaccept_validation_v91r1.json');po=load(ROOT/'inputs/q048_frec_moving_h_orchestration_log_v91r1.json')
    c('parent_raw_exact',sha(ROOT/'inputs/q048_frec_moving_h_result_v91r1.json')==cp['source_result_sha256']==pv['result_sha256']==pt['result_sha256'])
    c('parent_validation_exact',sha(ROOT/'inputs/q048_frec_moving_h_validation_v91r1.json')==cp['validation_sha256']==pt['validation_sha256']==pa['validation_sha256'])
    c('parent_transition_exact',sha(ROOT/'inputs/q048_frec_moving_h_transition_validation_v91r1.json')==cp['transition_validation_sha256']==pa['transition_sha256'])
    c('parent_acceptance_exact',sha(ROOT/'inputs'/PARENT)==pa['accepted_checkpoint_sha256']==pp['accepted_checkpoint_sha256'] and sha(ROOT/'inputs/q048_frec_moving_h_acceptance_validation_v91r1.json')==pp['acceptance_validation_sha256'])
    c('parent_science_validation',pv['status']==pp['status']==pa['status']==pt['status']=='PASS' and pv['checks_total']==pv['checks_passed']==118 and pv['mutations_total']==pv['mutations_rejected']==52 and pp['checks_total']==pp['checks_passed']==18)
    c('parent_final_orchestration',po['status']=='COMPLETE_ONE_ACCEPTED_CELL_STOP' and po['failure'] is None and po['producer_process_attempts']==1 and po['science_chain_seconds']<=300 and po['frozen_pins_unchanged'] and po['authoritative_actual']=={'count':107,'frontier':1010})
    c('parent_orchestration_pin',sha(ROOT/'inputs/q048_frec_moving_h_orchestration_log_v91r1.json')==task['fingerprint_basis']['parent_orchestration_sha256'])
    for name,pin in task['reference_code_pins'].items():c('reference_exact:'+name,sha(ROOT/'reference_v90'/name)==pin['sha256'] and (ROOT/'reference_v90'/name).stat().st_size==pin['bytes'])
    c('task_cell_and_guard',task['fingerprint_basis']['cell_z']==[1010,1000] and task['guard_binding']['row_index']==44 and task['fingerprint_basis']['current_source_Saha_Beta_prefactor']=='3.016101031869581e21')
    c('full_journal_exact',sha(ROOT/'context/Q047_SAMLET_JOURNAL_FREC_MOVING_H_V91R1_INGESTED_V1.md')==task['journal_ref']['sha256'])

    guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json'); gv=load(ROOT/'inputs/q048_guard_local_v_validation_v12.json')
    c('guard_hashes',sha(ROOT/'inputs/q048_guard_local_v_result_v12.json')==task['guard_binding']['raw_sha256']==gv['result_sha256'] and sha(ROOT/'inputs/q048_guard_local_v_validation_v12.json')==task['guard_binding']['validation_sha256'])
    c('guard_validation',gv['technical_state']=='PASS' and gv['checks_passed']==gv['checks_total']==6566 and gv['mutations_rejected']==gv['mutations_total']==24)
    for label,ev in zip(['primary','control'],guard['evaluators']):
        row=ev['rows'][44]
        c('guard_'+label+'_domain',[row['z0'],row['z1']]==[1010,1000] and [row['a0'],row['a1']]==['1/1011','1/1001'])
        c('guard_'+label+'_hash',digest(row)==task['guard_binding'][label+'_row_sha256'] and row==task['guard_binding'][label])
        c('guard_'+label+'_admission',row['accepted'] is True and row['committed'] is True and row['whole_cell_qualified'] is True and row['domain']['admitted'] is True and all(row['domain']['checks'].values()) and row['source_state_reset'] is False and F(row['G_lower'])>0)
    primary=guard['evaluators'][0]['rows'][44]; ep=cp['endpoint']
    c('primary_glue',F(primary['a0'])==F(ep['a']) and F(primary['E_input_left'])==F(ep['E']) and F(primary['Y_left'])==F(ep['Y']) and F(primary['V_previous'])==F(ep['Vbar']))
    c('capture_bytes',sha(ROOT/'inputs/q048_prefix_config_v1.json')==s['capture_sha256'])
    c('prompt_bytes',sha(ROOT/'inputs/Bubbleverse_Matematikmotor_2.1.0-53.md')=='3594851ec3b827d643ba89c410a04ca454e80648011dde549f229a69f085475b')
    return checks
def load_spec():
    s=load(ROOT/SPEC); validate_spec(s); return s
