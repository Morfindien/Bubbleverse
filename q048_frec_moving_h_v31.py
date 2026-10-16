"""Q048 V31 one-cell actual paired-frec consumer for Hillipop-EDE 1310->1300.
Consumes accepted V30 moving-h proof, accepted V29 actual checkpoint, and committed V12 row14.
Prior scientific producers/validators are read as immutable evidence and are not executed.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
from copy import deepcopy
import sys,json,hashlib,time,platform,resource
ROOT=Path(__file__).resolve().parent; IN=ROOT/'inputs'; sys.path.insert(0,str(IN))
import q048_full_tube_reuse_v1 as old
m=old.m; d=old.d; prefix=old.prefix
PASS='PASS_PAIRED_FREC_MOVING_H_DOMAIN_BOUND'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def canon_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(ok,code):
    if not ok: raise ValueError(code)

def select_guard(g):
    rows=[]
    for ev in g['evaluators']:
        hit=[r for r in ev['rows'] if [r['z0'],r['z1']]==[1310,1300] and [r['a0'],r['a1']]==['1/1311','1/1301']]
        require(len(hit)==1,'UNIQUE_GUARD_ROW14')
        r=hit[0]
        require(r['accepted'] is True and r['committed'] is True and r['whole_cell_qualified'] is True and r['domain']['admitted'] is True and all(r['domain']['checks'].values()),'GUARD_ROW14_COMMITTED')
        require(F(r['G_lower'])>0 and F(r['derivative_lower'])>0 and r['source_state_reset'] is False,'GUARD_ROW14_POSITIVE')
        rows.append(r)
    require(len(rows)==2,'PRIMARY_CONTROL_REQUIRED')
    return rows

def check_parent(cp,task):
    require(cp['q']=='Q048','PARENT_Q')
    require(cp['technical_state']=='PASS' and cp['admission_state']=='ACCEPTED_AFTER_INDEPENDENT_VALIDATION','PARENT_ACCEPTED')
    require(cp['total_accepted_cells_in_chain']==77,'PARENT_COUNT77')
    require(cp['frontiers']=={'camspec-lcdm':1440,'camspec-ede_n3':1440,'hillipop-lcdm':1440,'hillipop-ede_n3':1310},'PARENT_FRONTIERS_V29')
    require(cp['linked_scalar_endpoint']==task['initial_actual_state']['scalar_endpoint'],'PARENT_SCALAR_ENDPOINT')
    inv=cp['linked_invariant_state']; ti=task['initial_actual_state']['moving_invariant_endpoint']
    require(inv['endpoint_a']==ti['a'] and inv['endpoint_lower_projection']==ti['lower_projection'] and inv['physical_state_reset'] is False,'PARENT_MOVING_ENDPOINT')

def preflight(s):
    for rel,pin in s['inputs'].items():
        p=ROOT/rel; require(p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],'PIN:'+rel)
    require(sha(IN/'Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0.md')=='49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1','PROMPT_PIN')
    task=load(IN/'Q048_MOVING_H_DOMAIN_V30_NEXT_BUILDER_TASK_V1.json')
    require(canon_hash(task['fingerprint_basis'])==task['task_fingerprint'],'TASK_FINGERPRINT_RECOMPUTE')
    require(task['task_id']==s['task_id'] and task['task_fingerprint']==s['task_fingerprint'],'TASK_BINDING')
    for k in ['q','target_q','exact_question','question_sha256','source_commit','capture_sha256']: require(s[k]==task[k],'IDENTITY:'+k)
    require(hashlib.sha256(s['exact_question'].encode()).hexdigest()==s['question_sha256'],'QUESTION_HASH')
    parent=load(IN/'q048_frec_moving_h_accepted_checkpoint_v29.json'); parent_raw=load(IN/'q048_frec_moving_h_result_v29.json'); parent_val=load(IN/'q048_frec_moving_h_validation_v29.json'); parent_post=load(IN/'q048_frec_moving_h_postaccept_validation_v29.json'); parent_trans=load(IN/'q048_frec_moving_h_transition_validation_v29.json')
    check_parent(parent,task)
    require(sha(IN/'q048_frec_moving_h_accepted_checkpoint_v29.json')==task['initial_actual_state']['accepted_checkpoint_sha256']=='a8a43580295c62b345382ccb38434c71bd1eda988df61dcb88e083fd515b679f','PARENT_CHECKPOINT_PIN_V29')
    require(parent_raw['result_id']=='LOCAL-Q048-FREC-MOVING-H-ACTUAL-CONSUMER-V29' and sha(IN/'q048_frec_moving_h_result_v29.json')==parent['source_result_sha256'],'PARENT_RAW_LINK')
    require(parent_val['status']=='PASS' and parent_val['technical_state']=='PASS' and parent_val['checks_passed']==parent_val['checks_total']==110 and parent_val['mutation_rejections']==parent_val['mutation_tests_total']==20 and parent_val['result_sha256']==parent['source_result_sha256'],'PARENT_VALIDATION')
    require(parent_post['status']=='PASS' and parent_post['checks_passed']==parent_post['checks_total']==10 and parent_post['accepted_checkpoint_sha256']==sha(IN/'q048_frec_moving_h_accepted_checkpoint_v29.json'),'PARENT_POSTACCEPT')
    require(parent_trans['status']=='PASS' and parent_trans['checks_passed']==parent_trans['checks_total']==5,'PARENT_TRANSITION')
    proof=load(IN/'q048_moving_h_domain_result_v30.json'); proof_val=load(IN/'q048_moving_h_domain_validation_v30.json'); proof_cp=load(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json'); proof_post=load(IN/'q048_moving_h_domain_postaccept_validation_v30.json'); proof_trans=load(IN/'q048_moving_h_domain_transition_validation_v30.json'); proof_pkg=load(IN/'q048_moving_h_domain_package_validation_v30.json')
    pb=task['proof_binding']
    require(sha(IN/'q048_moving_h_domain_result_v30.json')==pb['raw_sha256'] and sha(IN/'q048_moving_h_domain_validation_v30.json')==pb['validation_sha256'],'V30_RAW_VALIDATION_HASHES')
    require(sha(IN/'q048_moving_h_domain_candidate_checkpoint_v30.json')==pb['candidate_checkpoint_sha256'] and sha(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json')==pb['accepted_checkpoint_sha256'],'V30_CHECKPOINT_HASHES')
    require(sha(IN/'q048_moving_h_domain_postaccept_validation_v30.json')==pb['postaccept_sha256'] and sha(IN/'q048_moving_h_domain_transition_validation_v30.json')==pb['transition_sha256'],'V30_POST_TRANS_HASHES')
    require(sha(IN/'q048_moving_h_domain_spec_v30.json')==pb['spec_sha256'] and sha(IN/'Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V30.md')==pb['contract_sha256'],'V30_SPEC_CONTRACT_HASHES')
    require(sha(IN/'q048_moving_h_domain_package_validation_v30.json')==pb['package_validation_sha256'],'V30_PACKAGE_HASH')
    require(proof['status']=='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL' and proof['new_actual_paired_cells']==0 and proof['retained_actual_paired_cells']==77,'V30_PROOF_STATUS')
    require(proof_val['status']=='PASS' and proof_val['technical_state']=='PASS' and proof_val['checks_passed']==proof_val['checks_total']==82 and proof_val['mutations_rejected']==proof_val['mutations_total']==20 and proof_val['result_sha256']==sha(IN/'q048_moving_h_domain_result_v30.json'),'V30_VALIDATION')
    require(proof_cp['validation_state']=='ACCEPTED_AFTER_INDEPENDENT_VALIDATION' and proof_cp['technical_state']=='PASS' and proof_cp['source_result_sha256']==sha(IN/'q048_moving_h_domain_result_v30.json') and proof_cp['validation_sha256']==sha(IN/'q048_moving_h_domain_validation_v30.json'),'V30_ACCEPTED_CHECKPOINT')
    require(proof_post['status']=='PASS' and proof_post['checks_passed']==proof_post['checks_total']==13 and proof_post['accepted_checkpoint_sha256']==sha(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json'),'V30_POSTACCEPT')
    require(proof_trans['status']=='PASS' and proof_trans['checks_passed']==proof_trans['checks_total']==5,'V30_TRANSITION')
    require(proof_pkg['status']=='PASS' and proof_pkg['checks_passed']==proof_pkg['checks_total']==31,'V30_PACKAGE_AUDIT')
    guard=load(IN/'q048_guard_local_v_result_v12.json'); guard_val=load(IN/'q048_guard_local_v_validation_v12.json')
    require(guard_val['technical_state']=='PASS' and guard_val['phase']=='FINAL' and guard_val['checks_passed']==guard_val['checks_total']==6566 and guard_val['mutations_rejected']==guard_val['mutations_total']==24 and guard_val['result_sha256']==sha(IN/'q048_guard_local_v_result_v12.json'),'GUARD_VALIDATION')
    require(sha(IN/'q048_guard_local_v_result_v12.json')==task['guard_binding']['raw_sha256'],'GUARD_HASH')
    primary,control=select_guard(guard)
    require(canon_hash(primary)==task['guard_binding']['primary_row_sha256'] and canon_hash(control)==task['guard_binding']['control_row_sha256'],'GUARD_ROW_HASHES')
    for k,v in task['guard_binding']['primary'].items(): require(primary.get(k)==v,'TASK_GUARD_ROW_FIELD:'+k)
    ep=parent['linked_scalar_endpoint']; require(F(primary['a0'])==F(ep['a1']) and F(primary['E_input_left'])==F(ep['E_right']) and F(primary['Y_left'])==F(ep['Y_right']) and F(primary['V_previous'])==F(ep['Vbar']),'SCALAR_GLUE')
    require(proof['guard_primary']==primary and proof['guard_primary_row_sha256']==canon_hash(primary) and proof['guard_control_row_sha256']==canon_hash(control),'PROOF_GUARD_GLUE')
    co=proof['comparison']; inv=parent['linked_invariant_state']
    require(co['parent_endpoint_a']=='1/1311' and F(co['initial_lower'])==F(inv['endpoint_lower_projection']) and F(co['parent_endpoint_lower_projection'])==F(inv['endpoint_lower_projection']),'MOVING_PARENT_GLUE')
    require(F(co['K_upper'])==F(pb['K_upper']) and F(co['epsilon'])==F(pb['epsilon']) and F(co['whole_cell_h_min'])==F(pb['whole_cell_h_min']) and F(co['whole_cell_h_min'])>0 and co['source_state_reset'] is False and co['physical_state_reset'] is False and co['comparison_glued_to_parent'] is True and co['gluing_verified'] is True,'MOVING_PROOF_BINDING')
    require(F(co['K_upper'])!=F(inv['K_upper']),'NO_OLD_K_SUBSTITUTION'); require(F(co['initial_lower'])!=F(1,2),'NO_RESET_TO_HALF')
    return task,parent,parent_raw,proof,guard,primary,control

def candidate_checkpoint(parent,row,proof):
    cp=deepcopy(parent); cp['technical_state']='PENDING_VALIDATION'
    for key in ['validation','validation_sha256','candidate_checkpoint_sha256']: cp.pop(key,None)
    cp['new_accepted_cells']=0; cp['retained_prior_accepted_cells']=77; cp['total_accepted_cells_in_chain']=77
    if row['status']!=PASS: return cp
    b=row['guard_binding']; co=proof['comparison']; cp['new_accepted_cells']=1; cp['retained_prior_accepted_cells']=77; cp['total_accepted_cells_in_chain']=78
    cp['frontiers']['hillipop-ede_n3']=1300
    cp['linked_scalar_endpoint']={'a1':b['a1'],'E_right':b['E_right'],'Y_right':b['Y_right'],'Vbar':b['V_admitted']}
    cp['linked_invariant_state']={
      'schema_version':'Q048_MOVING_INVARIANT_STATE_V31','kind':co['method'],'proof_cell_a':['1/1311','1/1301'],
      'parent_endpoint_a':'1/1311','parent_endpoint_lower_projection':co['initial_lower'],'K_upper':co['K_upper'],'epsilon':co['epsilon'],
      'endpoint_a':'1/1301','endpoint_lower_projection':co['whole_cell_h_min'],'upper_h':'99999/100000','w_domain':['-1/1000000','1/100'],'physical_state_reset':False,
      'interpretation':'Validated V30 outer lower projection consumed by one actual paired-frec admission; not a measured h/xe value or independent restart.',
      'proof_result_sha256':sha(IN/'q048_moving_h_domain_result_v30.json'),'proof_validation_sha256':sha(IN/'q048_moving_h_domain_validation_v30.json'),'proof_checkpoint_sha256':sha(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json'),
      'parent_checkpoint_sha256':sha(IN/'q048_frec_moving_h_accepted_checkpoint_v29.json'),'guard_raw_sha256':sha(IN/'q048_guard_local_v_result_v12.json'),'guard_primary_row_sha256':canon_hash(b),
      'source_commit':proof['source_commit'],'capture_sha256':proof['capture_sha256'],'question_sha256':proof['question_sha256'],'continuation_below1300_authorized':False}
    return cp

def qualify(s,task,parent,proof,primary,control):
    cap=load(IN/'q048_prefix_config_v1.json'); prefix.validate_config(cap); require(sha(IN/'q048_prefix_config_v1.json')==s['capture_sha256'],'CAPTURE_PIN')
    case=cap['cases']['hillipop-ede_n3']; flags=case['background']['thermal_flags']; t=prefix.parameters(case)
    a=m.I(F(1,1311),F(1,1301)); co=proof['comparison']; h=d.interval(co['h_domain']); w=d.interval(co['w_domain']); E=F(primary['E_safe_left']); B,floor,H,Hs=old.background(a,t,E)
    TR=m.const('8.617343e-5')*t['T0']/a; Tgamma=t['T0']/a; ratio=1-w; fit=d.interval(load(IN/'q048_p3_scaled_raw_result_v2.json')['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    source_checks={'SWIFT_MODEL4':all(x['HyRec_MODEL']==4 for x in case['thermal_starts']),'no_exotic_or_varying_flags':all(flags[k]==0 for k in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'z1_gt_900':1300>900,'TR_domain':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma_domain':1775<Tgamma.lo<=Tgamma.hi<4415,'ratio_domain':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'positive_H':Hs.lo>0,'proof_source_domains_all_true':all(proof['source_domain_checks'].values()),'same_a':d.encode(a)==proof['a'],'same_B0':d.encode(B)==proof['B0'],'same_floor':d.encode(floor)==proof['floor'],'same_H':d.encode(H)==proof['H_Mpc_inverse'],'same_Hs':d.encode(Hs)==proof['Hs_per_second'],'same_TR':d.encode(TR)==proof['TR_eV'],'same_Tgamma':d.encode(Tgamma)==proof['Tgamma_K'],'same_ratio':d.encode(ratio)==proof['TM_over_TR'],'same_fit':d.encode(fit)==proof['fit_denominator']}
    row={'case':'hillipop-ede_n3','mode':'frec','z':[1310,1300],'a':a,'guard_binding':primary,'guard_control_row_sha256':canon_hash(control),'source_domain_checks':source_checks,'source_flags':flags,'B0':B,'floor':floor,'E_safe_left':E,'H_Mpc_inverse':H,'Hs_per_second':Hs,'TR_eV':TR,'Tgamma_K':Tgamma,'TM_over_TR':ratio,'fit_denominator':fit,'h_domain':h,'w_domain':w,'comparison_receipt':{'result_sha256':sha(IN/'q048_moving_h_domain_result_v30.json'),'validation_sha256':sha(IN/'q048_moving_h_domain_validation_v30.json'),'accepted_checkpoint_sha256':sha(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json'),'comparison':co,'reexecuted':False},'branches':{},'status':'UNRESOLVED_NEW_MOVING_H_CONSUMER'}
    if not all(source_checks.values()): return row,{'code':'NEW_CONSUMER_SOURCE_DOMAIN_OR_BINDING','failed':[k for k,v in source_checks.items() if not v]}
    alpha,rr=old.load_atomic(IN/'q048_p3_scaled_transformed_log_tables_v2.json'); atomic=old.local_atomic(alpha,rr,TR,ratio); A=list(map(old.fromk,atomic['Alpha'])); Ae=list(map(old.fromk,atomic['Alpha_eq'])); R=old.fromk(atomic['R2p2s']); n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n; Beta=[Ae[i]*m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    atomic_same=(d.encode(A)==proof['Alpha'] and d.encode(Ae)==proof['Alpha_eq'] and d.encode(R)==proof['R2p2s'] and d.encode(n)==proof['nH_cm3'] and d.encode(saha)==proof['Saha_HyRec'] and d.encode(Beta)==proof['C_factor_certificate']['Beta'])
    HsK=d.interval(proof['Hs_for_K']); K=F(co['K_upper']); K_required=n.hi*(A[0].hi+A[1].hi)/HsK.lo
    L=m.const('8.2206'); P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit; gs=Beta[0]+3*R+L; gp=Beta[1]+R+P; D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P); Ns=L*gp+3*R*P; Np=P*gs+R*L; ds=Beta[0]*gp+3*R*Beta[1]; dp=Beta[1]*gs+R*Beta[0]
    ccalc={'Beta':Beta,'R':R,'L':L,'P':P,'gamma_s':gs,'gamma_p':gp,'D_positive_form':D,'Ns':Ns,'Np':Np,'D_minus_Ns_positive_form':ds,'D_minus_Np_positive_form':dp,'C_s_certified':m.I((Ns/D).lo,1),'C_p_certified':m.I((Np/D).lo,1)}
    c_same=d.encode(ccalc)==proof['C_factor_certificate']; atomic_positive=min(x.lo for x in A+Ae+[R,saha,n]+Beta)>0; c_positive=all(x.lo>0 for x in [L,P,gs,gp,D,Ns,Np,ds,dp])
    row.update(Alpha=A,Alpha_eq=Ae,R2p2s=R,Saha_HyRec=saha,nH_cm3=n,C_positive_factors=ccalc,atomic_source_exact_match=atomic_same,C_factor_exact_match=c_same,atomic_positive=atomic_positive,C_positive=c_positive,Hs_for_K=HsK,K_required=K_required,K_receipt_bound_sufficient=K>=K_required)
    if not (atomic_same and c_same and atomic_positive and c_positive and K>=K_required): return row,{'code':'NEW_CONSUMER_COEFFICIENT_BINDING_OR_POSITIVITY','atomic_same':atomic_same,'C_same':c_same,'atomic_positive':atomic_positive,'C_positive':c_positive,'K_sufficient':K>=K_required}
    for label,q in [('L',F(1,1000000)),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(h.hi),q) for i in range(2)]; thermal=old.thermal_certificate(a,h,q,t,Hs); pbr=proof['branches'][label]
        exact_match=(d.encode(high)==pbr['upper_h_face_terms'] and d.encode(thermal)==pbr['thermal']); ok=exact_match and all(x.lo>0 for x in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and thermal['faces']['admitted'] and pbr['admitted'] is True
        row['branches'][label]={'q':q,'lower_face':'CONSUMED_VALIDATED_V30_COMMON_EPS_RICCATI','lower_face_proof':pbr['lower_face_comparison'],'upper_h_face_terms':high,'thermal':thermal,'proof_exact_match':exact_match,'admitted':ok}
        if not ok: return row,{'code':'NEW_CONSUMER_BRANCH_FACE_OR_BINDING','branch':label,'method_insufficient_not_physical_falsification':True}
    row['status']=PASS; return row,None

def main():
    clock=time.monotonic(); stamp=datetime.now(timezone.utc).isoformat(); s=load(ROOT/'q048_frec_moving_h_spec_v31.json'); task,parent,parent_raw,proof,guard,primary,control=preflight(s); row,block=qualify(s,task,parent,proof,primary,control); encoded_row=d.encode(row); cp=candidate_checkpoint(parent,encoded_row,proof); success=row['status']==PASS; require(time.monotonic()-clock<s['science_budget_seconds'],'SCIENCE_BUDGET')
    result=d.encode({'schema_version':'Q048_FREC_MOVING_H_RESULT_V31','q':'Q048','target_q':'Q048','prompt_id':'BUBBLEVERSE.EXECUTION_HPC_BUILDER','prompt_version':'2.2.0','program_id':s['program_id'],'program_registry_status':'LOCAL_UNREGISTERED','task_id':s['task_id'],'task_fingerprint':s['task_fingerprint'],'result_id':s['result_id'],'run_id':'LOCAL-Q048-FREC-MOVING-H-V31-'+stamp,'exact_question':s['exact_question'],'question_sha256':s['question_sha256'],'source_commit':s['source_commit'],'capture_sha256':s['capture_sha256'],'spec_sha256':sha(ROOT/'q048_frec_moving_h_spec_v31.json'),'consumer_sha256':sha(Path(__file__)),'parent_raw_sha256':sha(IN/'q048_frec_moving_h_result_v29.json'),'parent_checkpoint_sha256':sha(IN/'q048_frec_moving_h_accepted_checkpoint_v29.json'),'parent_validation_sha256':sha(IN/'q048_frec_moving_h_validation_v29.json'),'parent_postaccept_sha256':sha(IN/'q048_frec_moving_h_postaccept_validation_v29.json'),'math_raw_sha256':sha(IN/'q048_moving_h_domain_result_v30.json'),'math_validation_sha256':sha(IN/'q048_moving_h_domain_validation_v30.json'),'math_checkpoint_sha256':sha(IN/'q048_moving_h_domain_accepted_checkpoint_v30.json'),'math_postaccept_sha256':sha(IN/'q048_moving_h_domain_postaccept_validation_v30.json'),'guard_raw_sha256':sha(IN/'q048_guard_local_v_result_v12.json'),'guard_validation_sha256':sha(IN/'q048_guard_local_v_validation_v12.json'),'actual_parent_result_id':parent_raw['result_id'],'initial_actual_count':77,'initial_frontiers':parent['frontiers'],'initial_scalar_endpoint':parent['linked_scalar_endpoint'],'new_cells':[row],'new_accepted_cells':1 if success else 0,'retained_prior_accepted_cells':77,'candidate_total_actual_count':cp['total_accepted_cells_in_chain'],'candidate_frontiers':cp['frontiers'],'new_mathematical_proof_cells':0,'retained_H_to_frec_tubes':4,'status':'ONE_NEW_ACTUAL_PAIRED_CELL_PENDING_VALIDATION' if success else 'PARTIAL_WITH_EXACT_NEW_CONSUMER_OBSTRUCTION','technical_state':'PENDING_VALIDATION','blocker':block,'stop':{'code':'ONE_CELL_SCOPE_EXHAUSTED' if success else 'FIRST_NEW_OBSTRUCTION','no_continuation_below1300':True,'max_new_actual_cells':1},'q_complete':False,'complete_a1_certificate':False,'final_delta_xe_bounds_computed':False,'final_delta_tau_bounds_computed':False,'native_P6':'UNRESOLVED','physical_falsification':False,'accepted_model_change':False,'prior_science_or_prior_validator_reexecuted':False,'return_route':'BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.1.0','compute_backend':'LOCAL_RUNTIME','github_worthwhile':'NO','execution':{'start_utc':stamp,'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-clock,'python':platform.python_version(),'platform':platform.platform(),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'backend':'LOCAL_RUNTIME','native_or_paid_runs':0}})
    out=ROOT/'q048_frec_moving_h_result_v31.json'; require(not out.exists(),'IMMUTABLE_RESULT_EXISTS'); out.write_text(json.dumps(result,indent=2)+'\n')
    cp.update(schema_version='Q048_MOVING_ACTUAL_CANDIDATE_CHECKPOINT_V31',source_result=out.name,source_result_sha256=sha(out),parent_checkpoint_sha256=result['parent_checkpoint_sha256'],guard_raw_sha256=result['guard_raw_sha256'],math_raw_sha256=result['math_raw_sha256'],math_validation_sha256=result['math_validation_sha256'],math_checkpoint_sha256=result['math_checkpoint_sha256'],admission_state='CANDIDATE_PENDING_INDEPENDENT_VALIDATION',complete_a1=False,stop_reason=result['stop']['code'],resume_condition='Ingest once after independent validation; no continuation below1300 authorized.')
    (ROOT/'q048_frec_moving_h_candidate_checkpoint_v31.json').write_text(json.dumps(cp,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','new_accepted_cells','candidate_total_actual_count','candidate_frontiers','blocker','execution']},indent=2))
if __name__=='__main__': main()
