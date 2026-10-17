"""Q048 Mathematics V54: exactly one connected moving-h proof-domain cell 1190->1180.
Parent is accepted V53 actual state 89/frontier1190. No actual consumer runs.
The producer executes once and writes a candidate only; independent validation is separate.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import json, hashlib, time, platform, resource, sys
ROOT=Path(__file__).resolve().parent; IN=ROOT/'inputs'; sys.path.insert(0,str(IN))
import q048_full_tube_reuse_v1 as old
m=old.m; prefix=old.prefix; d=old.d; k=old.k
SPEC='q048_moving_h_domain_spec_v54.json'; CONTRACT='Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V54.md'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads((ROOT/p).read_text())
def req(x,c):
    if not x: raise ValueError(c)
def row_sha(r): return hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ceil18(x): return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x): return F(x.numerator*10**18//x.denominator,10**18)
def lower_endpoint(K,eps,t,h0):
    K,eps,h0=map(F,[K,eps,h0]); t=m.iv(t); req(K>=0 and eps>=0 and h0>0 and t.lo>=0,'COMPARISON_DOMAIN')
    if eps==0: return h0/(1+K*h0*t)
    return eps/((1+eps/h0)*m.exp_i(K*eps*t)-1)
def control_lower(K,eps,ratio,h0):
    K,eps,ratio,h0=map(F,[K,eps,ratio,h0]); req(K>=0 and eps>=0 and ratio>=1 and h0>0,'CONTROL_DOMAIN')
    if eps==0: return h0/(1+K*h0*(ratio-1))
    x=K*eps*(ratio-1); req(x<1,'CONTROL_EXP_X_NOT_LT1')
    return eps/((1+eps/h0)/(1-x)-1)
def run():
    start=time.monotonic(); stamp=datetime.now(timezone.utc).isoformat(); s=load(SPEC)
    out=ROOT/'q048_moving_h_domain_result_v54.json'; cand=ROOT/'q048_moving_h_domain_candidate_checkpoint_v54.json'
    req(not out.exists() and not cand.exists(),'IMMUTABLE_OUTPUT_EXISTS')
    for rel,pin in s['inputs'].items():
        p=ROOT/rel; req(p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],'PIN:'+rel)
    task=load('inputs/Q048_FREC_MOVING_H_V53_NEXT_MATHEMATICS_TASK_V1.json')
    cp=load('inputs/q048_frec_moving_h_accepted_checkpoint_v53.json'); pv=load('inputs/q048_frec_moving_h_validation_v53.json'); dv=load('inputs/q048_frec_moving_h_delivery_validation_v53.json')
    guard=load('inputs/q048_guard_local_v_result_v12.json'); gv=load('inputs/q048_guard_local_v_validation_v12.json')
    req(s['task_id']==task['task_id'] and s['task_fingerprint']==task['task_fingerprint'],'TASK_CONTRACT')
    basis=json.dumps(task['fingerprint_basis'],sort_keys=True,separators=(',',':')).encode(); req(hashlib.sha256(basis).hexdigest()==task['task_fingerprint'],'TASK_FINGERPRINT')
    req(task['q']==task['target_q']==s['q']==s['target_q']=='Q048','Q')
    req(sha(IN/'q048_frec_moving_h_accepted_checkpoint_v53.json')==s['parent_actual_checkpoint_sha256']==task['initial_actual_state']['accepted_checkpoint_sha256'],'PARENT_CP_HASH')
    req(cp['status']=='VALIDATED' and cp['checkpoint_kind']=='ACCEPTED_ACTUAL' and cp['accepted_actual']=={'count':89,'frontier':1190},'PARENT89')
    req(cp['endpoint']==task['initial_actual_state']['endpoint'] and F(cp['numerics']['connected_lower'])==F(task['initial_actual_state']['connected_lower']),'PARENT_STATE')
    req(pv['status']=='PASS' and pv['checks_passed']==pv['checks_total']==35 and pv['mutations_rejected']==pv['mutations_total']==24,'PARENT_VALIDATION')
    req(dv['status']=='PASS' and dv['checks_passed']==dv['checks_total'],'PARENT_DELIVERY')
    req(sha(IN/'q048_guard_local_v_result_v12.json')==s['guard_raw_sha256']==task['guard_binding']['raw_sha256'],'GUARD_RAW')
    req(sha(IN/'q048_guard_local_v_validation_v12.json')==s['guard_validation_sha256']==task['guard_binding']['validation_sha256'],'GUARD_VAL_HASH')
    req(gv['technical_state']=='PASS' and gv['phase']=='FINAL' and gv['checks_passed']==gv['checks_total']==6566 and gv['mutations_rejected']==gv['mutations_total']==24 and gv['result_sha256']==sha(IN/'q048_guard_local_v_result_v12.json'),'GUARD_VALIDATION')
    req(guard['source_commit']==s['source_commit']==task['fingerprint_basis']['source_commit'],'SOURCE_IDENTITY:source_commit'); req(guard['capture_sha256']==s['capture_sha256']==task['fingerprint_basis']['capture_sha256'],'SOURCE_IDENTITY:capture_sha256'); canonical_qhash=hashlib.sha256(task['exact_question'].encode()).hexdigest(); req(canonical_qhash==guard['question_sha256']==s['question_sha256'],'SOURCE_IDENTITY:canonical_question_sha256'); req(task['question_sha256']==task['fingerprint_basis']['question_sha256'] and len(task['question_sha256'])==61 and task['question_sha256']!=canonical_qhash,'TASK_QUESTION_HASH_DEFECT_EXPECTED')
    idx=s['guard_row_index']; primary=guard['evaluators'][0]['rows'][idx]; control=guard['evaluators'][1]['rows'][idx]
    for row in (primary,control):
        req(row['accepted'] and row['committed'] and row['whole_cell_qualified'] and row['domain']['admitted'] and all(row['domain']['checks'].values()),'COMMON_COMMITTED_GUARD')
        req(F(row['G_lower'])>0 and F(row['derivative_lower'])>0,'COMMON_POSITIVE_GUARD')
        req([row['a0'],row['a1']]==s['cell']['a'] and [row['z0'],row['z1']]==s['cell']['z'],'EXACT_NEW_CELL')
    req(row_sha(primary)==s['guard_primary_row_sha256']==task['guard_binding']['primary_row_sha256'],'PRIMARY_ROW_HASH')
    req(row_sha(control)==s['guard_control_row_sha256']==task['guard_binding']['control_row_sha256'],'CONTROL_ROW_HASH')
    ep=cp['endpoint']; req(F(primary['a0'])==F(ep['a']) and F(primary['E_input_left'])==F(ep['E']) and F(primary['Y_left'])==F(ep['Y']) and F(primary['V_previous'])==F(ep['Vbar']),'V53_ROW26_GLUE')
    eps=F(s['epsilon']); h0=F(s['initial_lower_projection']); hmax=F(s['upper_h'])
    req(h0==F(cp['numerics']['connected_lower'])==F(task['initial_actual_state']['connected_lower']) and h0>0 and h0!=F(1,2),'NO_RESET_PARENT_LOWER')
    req(cp['no_physical_reset'] is True,'NO_PHYSICAL_RESET')
    cap=load('inputs/sources/q048_prefix_config_v1.json'); prefix.validate_config(cap); case=cap['cases']['hillipop-ede_n3']; flags=case['background']['thermal_flags']
    req(cap['question_sha256']==s['question_sha256'] and cap['source_commit']==s['source_commit'],'CAPTURE_IDENTITY')
    req(all(flags[x]==0 for x in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'SOURCE_FLAGS')
    req(all(x['HyRec_MODEL']==4 for x in case['thermal_starts']),'SOURCE_MODEL_SWIFT')
    t=prefix.parameters(case); a=m.I(F(1,1191),F(1,1181)); w=m.I(F(-1,1000000),F(1,100)); E=F(primary['E_safe_left'])
    B,floor,H,Hs=old.background(a,t,E); HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a; Tgamma=t['T0']/a; ratioI=1-w
    p3=load('inputs/sources/q048_p3_scaled_raw_result_v2.json'); fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    source_domain=dict(z1_gt_900=1180>900,TR_domain=F('.004')<TR.lo<=TR.hi<F('.4'),Tgamma_domain=Tgamma.lo>1775 and Tgamma.hi<4415,ratio_domain=ratioI.lo>F('.1'),fit_positive=fit.lo>0,H_positive=HsK.lo>0)
    req(all(source_domain.values()),'SOURCE_DOMAIN_NEW_CELL')
    alpha,rr=old.load_atomic(IN/'sources/q048_p3_scaled_transformed_log_tables_v2.json'); atom=old.local_atomic(alpha,rr,TR,ratioI)
    A=list(map(old.fromk,atom['Alpha'])); Ae=list(map(old.fromk,atom['Alpha_eq'])); R=old.fromk(atom['R2p2s']); n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    req(min(x.lo for x in A+Ae+[R,saha,n]+Beta)>0,'ATOMIC_SOURCE_POSITIVITY')
    Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo; K=ceil18(Kexact); req(K>0,'K_POSITIVE'); req(K!=F(cp['numerics']['K_upper']),'FRESH_K_NOT_OLD_K')
    du_k=k.log_i(k.I(a.hi/a.lo)); du=m.I(du_k.lo,du_k.hi); endpoint=lower_endpoint(K,eps,du,h0); ctrl=control_lower(K,eps,a.hi/a.lo,h0); hmin=floor18(min(endpoint.lo,ctrl)); req(0<hmin<=h0,'POSITIVE_NEW_LOWER')
    h=m.I(hmin,hmax); L=m.const('8.2206'); P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*R+L; gp=Beta[1]+R+P; D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P); Ns=L*gp+3*R*P; Np=P*gs+R*L
    Ccert=dict(Beta=Beta,R=R,L=L,P=P,gamma_s=gs,gamma_p=gp,D_positive_form=D,Ns=Ns,Np=Np,D_minus_Ns_positive_form=Beta[0]*gp+3*R*Beta[1],D_minus_Np_positive_form=Beta[1]*gs+R*Beta[0],C_s_certified=m.I((Ns/D).lo,1),C_p_certified=m.I((Np/D).lo,1))
    req(all(x.lo>0 for x in [P,D,Ns,Np,gs,gp]),'C_DENOMINATORS')
    branches={}; obstruction=None
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)]; thermal=old.thermal_certificate(a,h,q,t,Hs)
        faces=thermal['faces']; ok=all(x.lo>0 for x in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and faces['admitted']
        branches[label]=dict(q=q,lower_face_comparison='ell_u=-K_new*ell*(ell+epsilon) <= -K_new*ell*(ell+q) <= F_q',upper_h_face_terms=high,thermal=thermal,admitted=ok)
        if not ok: obstruction=dict(code='NEW_MOVING_LOWER_JOINT_FACE_OBSTRUCTION',branch=label,method_insufficient_not_physical_falsification=True)
    success=obstruction is None; stop=obstruction or dict(code='ONE_NEW_MOVING_H_PROOF_DOMAIN_CELL_PENDING_INDEPENDENT_VALIDATION',no_continuation_below1180=True)
    elapsed=time.monotonic()-start; req(elapsed<s['max_scientific_seconds'],'SCIENTIFIC_BUDGET')
    frontiers={'camspec-lcdm':1440,'camspec-ede_n3':1440,'hillipop-lcdm':1440,'hillipop-ede_n3':1190}
    result=d.encode(dict(
      schema_version='Q048_MOVING_H_DOMAIN_RESULT_V54',q='Q048',target_q='Q048',prompt_id='BUBBLEVERSE.MATHEMATICS',prompt_version='2.1.0',version='V54',
      task_id=s['task_id'],task_fingerprint=s['task_fingerprint'],result_id=s['result_id'],run_id='LOCAL-Q048-MOVING-H-DOMAIN-V54-'+stamp,exact_question=task['exact_question'],question_sha256=s['question_sha256'],task_question_sha256_reported=task['question_sha256'],task_question_sha256_defect='REPORTED_61_HEX_TRUNCATION_CORRECTED_BY_EXACT_QUESTION_HASH',source_commit=s['source_commit'],capture_sha256=s['capture_sha256'],
      producer_sha256=sha(Path(__file__)),spec_sha256=sha(ROOT/SPEC),proof_contract_sha256=sha(ROOT/CONTRACT),prompt_sha256=sha(IN/'Bubbleverse_Matematikmotor_2.1.0.md'),task_contract_sha256=sha(IN/'Q048_FREC_MOVING_H_V53_NEXT_MATHEMATICS_TASK_V1.json'),handoff_sha256=sha(IN/'Q048_FREC_MOVING_H_V53_INGESTION_HANDOFF_TO_MATHEMATICS_V1.md'),
      parent_v53_checkpoint_sha256=sha(IN/'q048_frec_moving_h_accepted_checkpoint_v53.json'),parent_v53_validation_sha256=sha(IN/'q048_frec_moving_h_validation_v53.json'),parent_v53_delivery_sha256=sha(IN/'q048_frec_moving_h_delivery_validation_v53.json'),
      guard_raw_sha256=sha(IN/'q048_guard_local_v_result_v12.json'),guard_validation_sha256=sha(IN/'q048_guard_local_v_validation_v12.json'),guard_primary_row_sha256=row_sha(primary),guard_control_row_sha256=row_sha(control),guard_primary=primary,guard_control_role='CONSERVATIVE_ALIGNED_GUARD_TRACK_NOT_PRIMARY_ACTUAL_STATE',
      source_flags=flags,source_domain_checks=source_domain,a=a,z=[1190,1180],B0=B,floor=floor,E_safe_left=E,H_Mpc_inverse=H,Hs_per_second=Hs,Hs_for_K=HsK,nH_cm3=n,TR_eV=TR,Tgamma_K=Tgamma,TM_over_TR=ratioI,fit_denominator=fit,Alpha=A,Alpha_eq=Ae,R2p2s=R,Saha_HyRec=saha,C_factor_certificate=Ccert,
      comparison=dict(method='COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V54',orientation='ell_u <= F_q',parent_method='V53_ACCEPTED_CONNECTED_LOWER',parent_endpoint_a=ep['a'],parent_endpoint_lower_projection=cp['numerics']['connected_lower'],initial_a=a.lo,initial_lower=h0,initial_lower_role='INHERITED_CERTIFIED_AUXILIARY_PROJECTION_NOT_PHYSICAL_RESET',epsilon=eps,old_cell_K=cp['numerics']['K_upper'],K_requalified_on_new_domain=True,K_reused_without_proof=False,K_unrounded_upper=Kexact,K_upper=K,H_divisor_role='POSITIVE_ORDINARY_BACKGROUND_LOWER',du=du,exp_argument=K*eps*du,endpoint_primary=endpoint,control_log_upper=a.hi/a.lo-1,control_exp_argument=K*eps*(a.hi/a.lo-1),endpoint_control_lower=ctrl,whole_cell_h_min=hmin,h_domain=h,w_domain=w,zero_q_limit='h0/(1+K*h0*t)',q_ordering='q<=epsilon implies -K*h*(h+epsilon)<=-K*h*(h+q)',source_state_reset=False,physical_state_reset=False,comparison_glued_to_parent=True,gluing_verified=True),
      branches=branches,status='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL' if success else 'METHOD_INSUFFICIENT_NEW_MOVING_H_DOMAIN',technical_state='PENDING_VALIDATION',scientific_state='INCONCLUSIVE',stop=stop,new_mathematical_proof_cells=1 if success else 0,new_actual_paired_cells=0,retained_actual_paired_cells=89,actual_frontiers=frontiers,actual_scalar_endpoint=ep,
      physical_falsification=False,q_complete=False,complete_a1_certificate=False,final_delta_xe_bounds_computed=False,final_delta_tau_bounds_computed=False,native_P6='UNRESOLVED',accepted_model_change=False,prior_science_or_prior_validator_reexecuted=False,return_route='RESULT INGESTION & ROUTING ENGINE2.1.0',repository_read_head=s['repository_read']['observed_head'],
      execution=dict(start_utc=stamp,end_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=elapsed,python=platform.python_version(),platform=platform.platform(),peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,backend='LOCAL_RUNTIME',native_or_paid_runs=0)))
    out.write_text(json.dumps(result,indent=2)+'\n')
    checkpoint=dict(schema_version='Q048_MOVING_H_DOMAIN_CANDIDATE_CHECKPOINT_V54',q='Q048',target_q='Q048',source_result=out.name,source_result_sha256=sha(out),mathematical_cell_status=result['status'],technical_state='PENDING_VALIDATION',proof_cell_a=['1/1201','1/1191'],proof_cell_z=[1190,1180],parent_actual_checkpoint_sha256=sha(IN/'q048_frec_moving_h_accepted_checkpoint_v53.json'),actual_frontiers=frontiers,actual_scalar_endpoint=ep,total_actual_paired_cells=89,new_actual_paired_cells=0,new_mathematical_proof_cells=result['new_mathematical_proof_cells'],comparison_start_lower=str(h0),comparison_endpoint_lower=str(hmin),comparison_K_upper=str(K),physical_state_reset=False,stop=result['stop'],resume_rule='Candidate only until producer-free validation PASS. Actual paired count/frontier remain 89/1190. Return to Result Ingestion after acceptance; no automatic consumer or below1180 continuation.')
    cand.write_text(json.dumps(checkpoint,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'K_upper':str(K),'K_display':float(K),'old_K':cp['numerics']['K_upper'],'initial_lower':str(h0),'whole_cell_h_min':str(hmin),'hmin_display':float(hmin),'primary_endpoint_lo':float(endpoint.lo),'control_lower':float(ctrl),'branches':{x:{'admitted':y['admitted'],'thermal_beta_lower':float(y['thermal']['beta'].lo)} for x,y in branches.items()},'actual_count':89,'frontier':1190,'elapsed':elapsed,'stop':stop},indent=2))
if __name__=='__main__': run()
