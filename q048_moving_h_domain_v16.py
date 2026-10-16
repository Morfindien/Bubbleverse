from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import json, hashlib, time, platform, resource
import q048_full_tube_reuse_v1 as old
m=old.m; prefix=old.prefix; d=old.d; k=old.k
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ceil18(x): return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x): return F(x.numerator*10**18//x.denominator,10**18)
def lower_endpoint(K,eps,t,h0):
    t=m.iv(t); return eps/((1+eps/h0)*m.exp_i(K*eps*t)-1)
def control_lower(K,eps,ratio,h0):
    x=K*eps*(ratio-1)
    if not (0 <= x < 1): raise ValueError('CONTROL_EXP_X')
    return eps/((1+eps/h0)/(1-x)-1)
def enc(x): return d.encode(x)

def run():
    start=time.monotonic(); stamp=datetime.now(timezone.utc).isoformat()
    guard=json.load(open(HERE/'q048_guard_local_v_result_v12.json'))
    cp=json.load(open(HERE/'q048_frec_moving_h_checkpoint_v15.json'))
    cap=json.load(open(HERE/'q048_prefix_config_v1.json')); prefix.validate_config(cap)
    p3=json.load(open(HERE/'q048_p3_scaled_raw_result_v2.json'))
    primary=guard['evaluators'][0]['rows'][7]; control=guard['evaluators'][1]['rows'][7]
    assert [primary['a0'],primary['a1']]==['1/1381','1/1371']
    assert primary['accepted'] and primary['committed'] and control['accepted'] and control['committed']
    assert F(primary['G_lower'])>0 and F(control['G_lower'])>0
    assert cp['total_accepted_cells_in_chain']==70 and cp['frontiers']['hillipop-ede_n3']==1380
    assert F(primary['E_input_left'])==F(cp['linked_scalar_endpoint']['E_right'])
    assert F(primary['Y_left'])==F(cp['linked_scalar_endpoint']['Y_right'])
    assert F(primary['V_previous'])==F(cp['linked_scalar_endpoint']['Vbar'])
    inv=cp['linked_invariant_state']; h0=F(inv['endpoint_lower_projection']); eps=F(inv['epsilon'])
    assert inv['endpoint_a']=='1/1381' and inv['physical_state_reset'] is False
    case=cap['cases']['hillipop-ede_n3']; flags=case['background']['thermal_flags']
    assert all(flags[x]==0 for x in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr'])
    assert all(x['HyRec_MODEL']==4 for x in case['thermal_starts'])
    t=prefix.parameters(case); a=m.I(F(1,1381),F(1,1371)); hmax=F(99999,100000); w=m.I(F(-1,1000000),F(1,100)); E=F(primary['E_safe_left'])
    B,floor,H,Hs=old.background(a,t,E); HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a; Tgamma=t['T0']/a; ratio=1-w
    fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    domain={'z1_gt_900':1370>900,'TR_domain':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma_domain':Tgamma.lo>1775 and Tgamma.hi<4415,'ratio_domain':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'H_positive':HsK.lo>0}
    assert all(domain.values())
    alpha,rr=old.load_atomic(HERE/'q048_p3_scaled_transformed_log_tables_v2.json')
    atomic=old.local_atomic(alpha,rr,TR,ratio); A=list(map(old.fromk,atomic['Alpha'])); Ae=list(map(old.fromk,atomic['Alpha_eq'])); R=old.fromk(atomic['R2p2s']); n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    assert min(x.lo for x in A+Ae+[R,saha,n]+Beta)>0
    Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo; K=ceil18(Kexact)
    du_k=k.log_i(k.I(a.hi/a.lo)); du=m.I(du_k.lo,du_k.hi)
    ep=lower_endpoint(K,eps,du,h0); ctl=control_lower(K,eps,a.hi/a.lo,h0); hmin=floor18(min(ep.lo,ctl)); assert 0<hmin<=h0
    h=m.I(hmin,hmax); L=m.const('8.2206'); P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*R+L; gp=Beta[1]+R+P; D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P); Ns=L*gp+3*R*P; Np=P*gs+R*L
    assert all(x.lo>0 for x in [P,D,Ns,Np,gs,gp])
    cert={'Beta':Beta,'R':R,'L':L,'P':P,'gamma_s':gs,'gamma_p':gp,'D_positive_form':D,'Ns':Ns,'Np':Np,'D_minus_Ns_positive_form':Beta[0]*gp+3*R*Beta[1],'D_minus_Np_positive_form':Beta[1]*gs+R*Beta[0],'C_s_certified':m.I((Ns/D).lo,1),'C_p_certified':m.I((Np/D).lo,1)}
    branches={}
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)]
        thermal=old.thermal_certificate(a,h,q,t,Hs); ok=all(x.lo>0 for x in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and thermal['faces']['admitted']
        branches[label]={'q':q,'lower_face_comparison':'ell_u=-K*ell*(ell+epsilon) <= -K*ell*(ell+q) <= F_q','upper_h_face_terms':high,'thermal':thermal,'admitted':ok}
    success=all(v['admitted'] for v in branches.values())
    result=enc({
      'schema_version':'Q048_MOVING_H_DOMAIN_RESULT_V16','q':'Q048','target_q':'Q048','prompt_id':'BUBBLEVERSE.MATHEMATICS','prompt_version':'2.1.0',
      'task_id':'LOCAL-Q048-POST-V15-MOVING-H-DOMAIN-1380-1370-MATH-V1','result_id':'LOCAL-Q048-POST-V15-MOVING-H-DOMAIN-V16','run_id':'LOCAL-Q048-MOVING-H-DOMAIN-V16-'+stamp,
      'exact_question':cap['scientific_question'],'question_sha256':cap['question_sha256'],'source_commit':cap['source_commit'],'capture_sha256':cp['linked_invariant_state']['capture_sha256'],
      'parent_v15_checkpoint_sha256':sha(HERE/'q048_frec_moving_h_checkpoint_v15.json'),'parent_v15_result_sha256':cp['source_result_sha256'],'parent_v14_proof_result_sha256':inv['proof_result_sha256'],'parent_v14_validation_sha256':cp['math_validation_sha256'],
      'guard_raw_sha256':sha(HERE/'q048_guard_local_v_result_v12.json'),'guard_primary_row_sha256':canon_hash(primary),'guard_control_row_sha256':canon_hash(control),'guard_primary':primary,
      'source_flags':flags,'source_domain_checks':domain,'a':a,'z':[1380,1370],'B0':B,'floor':floor,'E_safe_left':E,'H_Mpc_inverse':H,'Hs_per_second':Hs,'Hs_for_K':HsK,'nH_cm3':n,'TR_eV':TR,'Tgamma_K':Tgamma,'TM_over_TR':ratio,'fit_denominator':fit,'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'Saha_HyRec':saha,'C_factor_certificate':cert,
      'comparison':{'method':'COMMON_EPS_SOURCE_SIGN_RICCATI_CONTINUATION','orientation':'ell_u <= F_q','parent_endpoint_a':'1/1381','initial_lower_from_parent_projection':h0,'epsilon':eps,'K_unrounded_upper':Kexact,'K_upper':K,'H_divisor_role':'POSITIVE_ORDINARY_BACKGROUND_LOWER','du':du,'exp_argument':K*eps*du,'endpoint_primary':ep,'control_log_upper':a.hi/a.lo-1,'control_exp_argument':K*eps*(a.hi/a.lo-1),'endpoint_control_lower':ctl,'whole_cell_h_min':hmin,'h_domain':h,'w_domain':w,'zero_q_limit':'h0/(1+K*h0*t)','q_ordering':'q<=epsilon implies -K*h*(h+epsilon)<=-K*h*(h+q)','source_state_reset':False,'physical_initial_state_reset':False},
      'branches':branches,'status':'PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL' if success else 'METHOD_INSUFFICIENT_MOVING_H_DOMAIN','technical_state':'PENDING_VALIDATION','stop':{'code':'ONE_NEW_MOVING_H_DOMAIN_PROOF_CELL_PENDING_INDEPENDENT_VALIDATION' if success else 'FIRST_NEW_DOMAIN_OBSTRUCTION','no_actual_consumer_run':True,'no_continuation_below1370':True},
      'new_mathematical_proof_cells':1 if success else 0,'new_actual_paired_cells':0,'retained_actual_paired_cells':70,'actual_frontiers':cp['frontiers'],'actual_scalar_endpoint':cp['linked_scalar_endpoint'],'physical_falsification':False,'q_complete':False,'complete_a1_certificate':False,'final_delta_xe_bounds_computed':False,'final_delta_tau_bounds_computed':False,'native_P6':'UNRESOLVED','accepted_model_change':False,'prior_science_or_prior_validator_reexecuted':False,'return_route':'RESULT INGESTION & ROUTING ENGINE2.1.0',
      'execution':{'start_utc':stamp,'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'python':platform.python_version(),'platform':platform.platform(),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'backend':'LOCAL_RUNTIME','native_or_paid_runs':0}
    })
    out=HERE/'q048_moving_h_domain_result_v16.json'; out.write_text(json.dumps(result,indent=2)+'\n')
    ck={'schema_version':'Q048_MOVING_H_DOMAIN_CHECKPOINT_V16','q':'Q048','source_result':out.name,'source_result_sha256':sha(out),'mathematical_cell_status':result['status'],'proof_cell_a':['1/1381','1/1371'],'parent_actual_checkpoint_sha256':result['parent_v15_checkpoint_sha256'],'actual_frontiers':cp['frontiers'],'actual_scalar_endpoint':cp['linked_scalar_endpoint'],'total_actual_paired_cells':70,'new_actual_paired_cells':0,'comparison_parent_lower':str(h0),'comparison_endpoint_lower':str(hmin),'K_upper':str(K),'epsilon':str(eps),'stop':result['stop'],'resume_rule':'Ingest this validated math component once. No actual checkpoint advance. Any consumer must explicitly bind this V16 proof cell and row7 scalar guard.'}
    (HERE/'q048_moving_h_domain_checkpoint_v16.json').write_text(json.dumps(ck,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'K_upper':str(K),'h_parent':str(h0),'endpoint_primary_lo':str(ep.lo),'endpoint_control_lower':str(ctl),'whole_cell_h_min':str(hmin),'L':branches['L']['admitted'],'R':branches['R']['admitted'],'seconds':result['execution']['elapsed_seconds']},indent=2))
if __name__=='__main__': run()
