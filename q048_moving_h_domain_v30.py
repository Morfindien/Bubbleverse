"""Q048 Mathematics V30: exactly one connected moving-h proof-domain cell 1310->1300.
Reuses the validated V28 theorem/implementation lineage but recomputes the source-faithful K and
whole-cell source/C/upper-h/thermal admission on committed V12 row14. The initial
lower is the accepted V29 endpoint projection. No actual paired-frec consumer runs.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import json, hashlib, time, platform, resource, sys
ROOT=Path(__file__).resolve().parent
INPUTS=ROOT/'inputs'; sys.path.insert(0,str(INPUTS))
import q048_full_tube_reuse_v1 as old
m=old.m; prefix=old.prefix; d=old.d; k=old.k
SPEC='q048_moving_h_domain_spec_v30.json'
CONTRACT='Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V30.md'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(rel): return json.loads((ROOT/rel).read_text())
def require(ok,code):
    if not ok: raise ValueError(code)
def ceil18(x): return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x): return F(x.numerator*10**18//x.denominator,10**18)
def lower_endpoint(K,eps,t,h0):
    K,eps,h0=map(F,[K,eps,h0]); t=m.iv(t)
    require(K>=0 and eps>=0 and h0>0 and t.lo>=0,'COMPARISON_DOMAIN')
    if eps==0: return h0/(1+K*h0*t)
    return eps/((1+eps/h0)*m.exp_i(K*eps*t)-1)
def control_lower(K,eps,ratio,h0):
    K,eps,ratio,h0=map(F,[K,eps,ratio,h0]); require(K>=0 and eps>=0 and ratio>=1 and h0>0,'CONTROL_DOMAIN')
    if eps==0: return h0/(1+K*h0*(ratio-1))
    x=K*eps*(ratio-1); require(x<1,'CONTROL_EXP_X_NOT_LT1')
    return eps/((1+eps/h0)/(1-x)-1)
def digest_row(row): return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run():
    start=time.monotonic(); stamp=datetime.now(timezone.utc).isoformat(); s=load(SPEC)
    require(not (ROOT/'q048_moving_h_domain_result_v30.json').exists() and not (ROOT/'q048_moving_h_domain_candidate_checkpoint_v30.json').exists(),'IMMUTABLE_OUTPUT_EXISTS')
    for rel,pin in s['inputs'].items():
        p=ROOT/rel; require(p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],'PIN:'+rel)
    parent=load('inputs/q048_frec_moving_h_result_v29.json')
    cp=load('inputs/q048_frec_moving_h_accepted_checkpoint_v29.json')
    pv=load('inputs/q048_frec_moving_h_validation_v29.json')
    post=load('inputs/q048_frec_moving_h_postaccept_validation_v29.json')
    trans=load('inputs/q048_frec_moving_h_transition_validation_v29.json')
    guard=load('inputs/q048_guard_local_v_result_v12.json')
    gv=load('inputs/q048_guard_local_v_validation_v12.json')
    v28=load('inputs/q048_moving_h_domain_result_v28.json')
    v28v=load('inputs/q048_moving_h_domain_validation_v28.json')
    v28cp=load('inputs/q048_moving_h_domain_accepted_checkpoint_v28.json')
    v28post=load('inputs/q048_moving_h_domain_postaccept_validation_v28.json')
    task=load('inputs/Q048_FREC_MOVING_H_V29_NEXT_MATHEMATICS_TASK_V1.json')
    # Identity / no-repeat / accepted-parent gates.
    require(s['task_id']==task['task_id'] and s['task_fingerprint']==task['task_fingerprint'],'TASK_CONTRACT')
    basis=json.dumps(task['fingerprint_basis'],sort_keys=True,separators=(',',':')).encode()
    require(hashlib.sha256(basis).hexdigest()==task['task_fingerprint'],'TASK_FINGERPRINT')
    require(parent['q']==parent['target_q']==s['q']==s['target_q']=='Q048','Q')
    require(parent['result_id']=='LOCAL-Q048-FREC-MOVING-H-ACTUAL-CONSUMER-V29','PARENT_RESULT')
    require(pv['status']=='PASS' and pv['technical_state']=='PASS' and pv['checks_passed']==pv['checks_total']==110 and pv['mutation_rejections']==pv['mutation_tests_total']==20 and pv['result_sha256']==sha(INPUTS/'q048_frec_moving_h_result_v29.json'),'PARENT_VALIDATION')
    require(post['status']=='PASS' and post['checks_passed']==post['checks_total']==10 and post['accepted_checkpoint_sha256']==sha(INPUTS/'q048_frec_moving_h_accepted_checkpoint_v29.json'),'PARENT_POSTACCEPT')
    require(trans['status']=='PASS' and trans['checks_passed']==trans['checks_total']==5,'PARENT_TRANSITION')
    require(cp['source_result_sha256']==sha(INPUTS/'q048_frec_moving_h_result_v29.json') and cp['validation_sha256']==sha(INPUTS/'q048_frec_moving_h_validation_v29.json'),'PARENT_CP_BIND')
    require(cp['technical_state']=='PASS' and cp['admission_state']=='ACCEPTED_AFTER_INDEPENDENT_VALIDATION' and cp['total_accepted_cells_in_chain']==77 and cp['frontiers']['hillipop-ede_n3']==1310,'ACTUAL_PARENT77')
    require(parent['candidate_total_actual_count']==77 and parent['candidate_frontiers']==cp['frontiers'],'PARENT_FRONTIER')
    for key in ['source_commit','capture_sha256','question_sha256']:
        require(parent[key]==guard[key]==s[key]==task[key],'SOURCE_IDENTITY:'+key)
    # Previous proof lineage is accepted and exactly the one consumed by V29.
    require(v28v['status']=='PASS' and v28v['technical_state']=='PASS' and v28v['result_sha256']==sha(INPUTS/'q048_moving_h_domain_result_v28.json'),'V28_VALID')
    require(v28cp['technical_state']=='PASS' and v28cp['source_result_sha256']==sha(INPUTS/'q048_moving_h_domain_result_v28.json') and v28cp['validation_sha256']==sha(INPUTS/'q048_moving_h_domain_validation_v28.json'),'V28_CP')
    require(v28post['status']=='PASS' and v28post['accepted_checkpoint_sha256']==sha(INPUTS/'q048_moving_h_domain_accepted_checkpoint_v28.json'),'V28_POST')
    inv=cp['linked_invariant_state']
    require(inv['proof_result_sha256']==sha(INPUTS/'q048_moving_h_domain_result_v28.json') and inv['proof_validation_sha256']==sha(INPUTS/'q048_moving_h_domain_validation_v28.json') and inv['proof_checkpoint_sha256']==sha(INPUTS/'q048_moving_h_domain_accepted_checkpoint_v28.json'),'V29_INVARIANT_LINEAGE')
    # V12 committed row14.
    idx=s['guard_row_index']; primary=guard['evaluators'][0]['rows'][idx]; control=guard['evaluators'][1]['rows'][idx]
    for row in (primary,control):
        require(row['accepted'] is True and row['committed'] is True and row['whole_cell_qualified'] is True and row['domain']['admitted'] is True and all(row['domain']['checks'].values()),'COMMON_COMMITTED_GUARD')
        require(F(row['G_lower'])>0 and F(row['derivative_lower'])>0,'COMMON_POSITIVE_GUARD')
        require([row['a0'],row['a1']]==s['cell']['a'],'EXACT_NEW_CELL')
    require(digest_row(primary)==task['guard_binding']['primary_row_sha256'],'PRIMARY_ROW_HASH')
    require(digest_row(control)==task['guard_binding']['control_row_sha256'],'CONTROL_ROW_HASH')
    linked=cp['linked_scalar_endpoint']
    require(F(primary['a0'])==F(linked['a1']),'SCALAR_A_GLUE')
    require(F(primary['E_input_left'])==F(linked['E_right']),'SCALAR_E_GLUE')
    require(F(primary['Y_left'])==F(linked['Y_right']),'SCALAR_Y_GLUE')
    require(F(primary['V_previous'])==F(linked['Vbar']),'SCALAR_V_GLUE')
    # Connected moving lower from accepted V29; never reset to 1/2.
    eps=F(inv['epsilon']); h0=F(inv['endpoint_lower_projection']); hmax=F(inv['upper_h'])
    require(inv['kind']=='COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V28' and inv['endpoint_a']=='1/1311' and h0>0,'MOVING_PARENT')
    require(h0==F(v28cp['comparison']['whole_cell_h_min']) and h0!=F(1,2),'NO_ELL_RESET_AND_V28_GLUE')
    require(h0==F(task['fingerprint_basis']['initial_lower_projection']),'TASK_INITIAL_LOWER')
    # Frozen captured source.
    cap=load('inputs/sources/q048_prefix_config_v1.json'); prefix.validate_config(cap); case=cap['cases']['hillipop-ede_n3']; flags=case['background']['thermal_flags']
    require(all(flags[x]==0 for x in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'SOURCE_FLAGS')
    require(all(x['HyRec_MODEL']==4 for x in case['thermal_starts']),'SOURCE_MODEL_SWIFT')
    t=prefix.parameters(case); a=m.I(F(1,1311),F(1,1301)); w=m.I(F(-1,1000000),F(1,100)); E=F(primary['E_safe_left'])
    B,floor,H,Hs=old.background(a,t,E); Hs_K=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a; Tgamma=t['T0']/a; ratio=1-w
    p3=load('inputs/sources/q048_p3_scaled_raw_result_v2.json'); fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    source_domain=dict(z1_gt_900=1300>900,TR_domain=F('.004')<TR.lo<=TR.hi<F('.4'),Tgamma_domain=Tgamma.lo>1775 and Tgamma.hi<4415,ratio_domain=ratio.lo>F('.1'),fit_positive=fit.lo>0,H_positive=Hs_K.lo>0)
    require(all(source_domain.values()),'SOURCE_DOMAIN_NEW_CELL')
    alpha,rr=old.load_atomic(INPUTS/'sources/q048_p3_scaled_transformed_log_tables_v2.json')
    atomic=old.local_atomic(alpha,rr,TR,ratio); A=list(map(old.fromk,atomic['Alpha'])); Ae=list(map(old.fromk,atomic['Alpha_eq'])); R=old.fromk(atomic['R2p2s'])
    n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    require(min(x.lo for x in A+Ae+[R,saha,n]+Beta)>0,'ATOMIC_SOURCE_POSITIVITY')
    # Fresh K on row14/new cell.
    Kexact=n.hi*(A[0].hi+A[1].hi)/Hs_K.lo; K=ceil18(Kexact); require(K>0,'K_POSITIVE')
    require(K!=F(v28['comparison']['K_upper']),'FRESH_K_DIFFERS_FROM_V28_CELL')
    du_k=k.log_i(k.I(a.hi/a.lo)); du=m.I(du_k.lo,du_k.hi)
    endpoint=lower_endpoint(K,eps,du,h0); control_min=control_lower(K,eps,a.hi/a.lo,h0)
    hmin=floor18(min(endpoint.lo,control_min)); require(0<hmin<=h0,'POSITIVE_NEW_LOWER')
    # C/source/upper-h/thermal whole-cell certificate.
    h=m.I(hmin,hmax); L=m.const('8.2206'); P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*R+L; gp=Beta[1]+R+P
    D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P); Ns=L*gp+3*R*P; Np=P*gs+R*L
    Ccert=dict(Beta=Beta,R=R,L=L,P=P,gamma_s=gs,gamma_p=gp,D_positive_form=D,Ns=Ns,Np=Np,D_minus_Ns_positive_form=Beta[0]*gp+3*R*Beta[1],D_minus_Np_positive_form=Beta[1]*gs+R*Beta[0],C_s_certified=m.I((Ns/D).lo,1),C_p_certified=m.I((Np/D).lo,1))
    require(all(x.lo>0 for x in [P,D,Ns,Np,gs,gp]),'C_DENOMINATORS')
    branches={}; obstruction=None
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)]
        thermal=old.thermal_certificate(a,h,q,t,Hs); faces=thermal['faces']
        ok=all(x.lo>0 for x in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and faces['admitted']
        branches[label]=dict(q=q,lower_face_comparison='ell_u=-K_new*ell*(ell+epsilon) <= -K_new*ell*(ell+q) <= F_q',upper_h_face_terms=high,thermal=thermal,admitted=ok)
        if not ok:
            obstruction=dict(code='NEW_MOVING_LOWER_JOINT_FACE_OBSTRUCTION',branch=label,upper_hydrogen_pass=all(x.lo>0 for x in high),thermal_pass=faces['admitted'],method_insufficient_not_physical_falsification=True)
            break
    success=obstruction is None
    stop=obstruction or dict(code='ONE_NEW_MOVING_H_PROOF_DOMAIN_CELL_PENDING_INDEPENDENT_VALIDATION',no_continuation_below1300=True)
    elapsed=time.monotonic()-start; require(elapsed<s['max_scientific_seconds'],'SCIENTIFIC_BUDGET')
    result=d.encode(dict(
        schema_version='Q048_MOVING_H_DOMAIN_RESULT_V30',q='Q048',target_q='Q048',prompt_id='BUBBLEVERSE.MATHEMATICS',prompt_version='2.1.0',
        task_id=s['task_id'],task_fingerprint=s['task_fingerprint'],result_id=s['result_id'],run_id='LOCAL-Q048-MOVING-H-DOMAIN-V30-'+stamp,
        exact_question=parent['exact_question'],question_sha256=s['question_sha256'],source_commit=s['source_commit'],capture_sha256=s['capture_sha256'],
        spec_sha256=sha(ROOT/SPEC),proof_contract_sha256=sha(ROOT/CONTRACT),prompt_sha256=sha(INPUTS/'Bubbleverse_Matematikmotor_2.1.0.md'),task_contract_sha256=sha(INPUTS/'Q048_FREC_MOVING_H_V29_NEXT_MATHEMATICS_TASK_V1.json'),
        parent_v29_raw_sha256=sha(INPUTS/'q048_frec_moving_h_result_v29.json'),parent_v29_checkpoint_sha256=sha(INPUTS/'q048_frec_moving_h_accepted_checkpoint_v29.json'),parent_v29_validation_sha256=sha(INPUTS/'q048_frec_moving_h_validation_v29.json'),parent_v29_postaccept_sha256=sha(INPUTS/'q048_frec_moving_h_postaccept_validation_v29.json'),parent_v29_transition_sha256=sha(INPUTS/'q048_frec_moving_h_transition_validation_v29.json'),
        prior_v28_raw_sha256=sha(INPUTS/'q048_moving_h_domain_result_v28.json'),prior_v28_validation_sha256=sha(INPUTS/'q048_moving_h_domain_validation_v28.json'),prior_v28_accepted_checkpoint_sha256=sha(INPUTS/'q048_moving_h_domain_accepted_checkpoint_v28.json'),prior_v28_postaccept_sha256=sha(INPUTS/'q048_moving_h_domain_postaccept_validation_v28.json'),
        guard_raw_sha256=sha(INPUTS/'q048_guard_local_v_result_v12.json'),guard_validation_sha256=sha(INPUTS/'q048_guard_local_v_validation_v12.json'),guard_primary_row_sha256=digest_row(primary),guard_control_row_sha256=digest_row(control),guard_primary=primary,guard_control_role='CONSERVATIVE_ALIGNED_GUARD_TRACK_NOT_PRIMARY_ACTUAL_STATE',
        source_flags=flags,source_domain_checks=source_domain,a=a,z=[1310,1300],B0=B,floor=floor,E_safe_left=E,H_Mpc_inverse=H,Hs_per_second=Hs,Hs_for_K=Hs_K,nH_cm3=n,TR_eV=TR,Tgamma_K=Tgamma,TM_over_TR=ratio,fit_denominator=fit,Alpha=A,Alpha_eq=Ae,R2p2s=R,Saha_HyRec=saha,C_factor_certificate=Ccert,
        comparison=dict(method='COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V30',orientation='ell_u <= F_q',parent_method=inv['kind'],parent_endpoint_a=inv['endpoint_a'],parent_endpoint_lower_projection=inv['endpoint_lower_projection'],initial_a=a.lo,initial_lower=h0,initial_lower_role='INHERITED_CERTIFIED_AUXILIARY_PROJECTION_NOT_PHYSICAL_RESET',historical_original_ell0='1/2 at a=1/1391 only',epsilon=eps,old_cell_K=inv['K_upper'],old_cell_hmin=inv['endpoint_lower_projection'],K_requalified_on_new_domain=True,K_reused_without_proof=False,K_unrounded_upper=Kexact,K_upper=K,H_divisor_role='POSITIVE_ORDINARY_BACKGROUND_LOWER',du=du,exp_argument=K*eps*du,endpoint_primary=endpoint,control_log_upper=a.hi/a.lo-1,control_exp_argument=K*eps*(a.hi/a.lo-1),endpoint_control_lower=control_min,whole_cell_h_min=hmin,h_domain=h,w_domain=w,zero_q_limit='h0/(1+K*h0*t)',q_ordering='q<=epsilon implies -K*h*(h+epsilon)<=-K*h*(h+q)',source_state_reset=False,physical_state_reset=False,comparison_glued_to_parent=True,gluing_verified=True),
        branches=branches,status='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL' if success else 'METHOD_INSUFFICIENT_NEW_MOVING_H_DOMAIN',technical_state='PENDING_VALIDATION',scientific_state='INCONCLUSIVE',stop=stop,
        new_mathematical_proof_cells=1 if success else 0,new_actual_paired_cells=0,retained_actual_paired_cells=77,actual_frontiers=cp['frontiers'],actual_scalar_endpoint=cp['linked_scalar_endpoint'],actual_invariant_parent=inv,
        physical_falsification=False,q_complete=False,complete_a1_certificate=False,final_delta_xe_bounds_computed=False,final_delta_tau_bounds_computed=False,native_P6='UNRESOLVED',accepted_model_change=False,prior_science_or_prior_validator_reexecuted=False,return_route='RESULT INGESTION & ROUTING ENGINE2.1.0',
        execution=dict(start_utc=stamp,end_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=elapsed,python=platform.python_version(),platform=platform.platform(),peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,backend='LOCAL_RUNTIME',native_or_paid_runs=0)))
    out=ROOT/'q048_moving_h_domain_result_v30.json'; out.write_text(json.dumps(result,indent=2)+'\n')
    checkpoint=dict(schema_version='Q048_MOVING_H_DOMAIN_CANDIDATE_CHECKPOINT_V30',q='Q048',target_q='Q048',source_result=out.name,source_result_sha256=sha(out),mathematical_cell_status=result['status'],technical_state='PENDING_VALIDATION',proof_cell_a=['1/1311','1/1301'],proof_cell_z=[1310,1300],parent_actual_checkpoint_sha256=sha(INPUTS/'q048_frec_moving_h_accepted_checkpoint_v29.json'),actual_frontiers=cp['frontiers'],actual_scalar_endpoint=cp['linked_scalar_endpoint'],total_actual_paired_cells=77,new_actual_paired_cells=0,new_mathematical_proof_cells=result['new_mathematical_proof_cells'],comparison_start_lower=str(h0),comparison_endpoint_lower=str(hmin),comparison_K_upper=str(K),physical_state_reset=False,stop=result['stop'],resume_rule='Candidate only until producer-free validation PASS. Actual paired count/frontier remain 77/1310. Return to Result Ingestion after acceptance; no automatic consumer.')
    (ROOT/'q048_moving_h_domain_candidate_checkpoint_v30.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],K_upper=str(K),K_display=float(K),old_K=str(inv['K_upper']),initial_lower=str(h0),whole_cell_h_min=str(hmin),hmin_display=float(hmin),primary_endpoint_lo=float(endpoint.lo),control_lower=float(control_min),branches={x:{'admitted':y['admitted'],'thermal_beta_lower':float(y['thermal']['beta'].lo),'thermal_upper_margin':str(y['thermal']['faces']['upper_face_inward_margin'])} for x,y in branches.items()},actual_count=77,frontier=1310,elapsed=elapsed,stop=stop),indent=2))
if __name__=='__main__': run()
