"""Fresh one-cell V90 moving-H mathematical certificate 1020→1010; no actual consumer."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import sys,json,time,platform,os
from q048_v90_proof_contract import ROOT,TASK,PARENT,RAW,SPEC,sha,load,output,require,load_spec,digest
sys.path.insert(0,str(ROOT/'inputs'))
import q048_full_tube_reuse_v1 as old
m=old.m;d=old.d;k=old.k;prefix=old.prefix

def ceil18(x):return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x):return F(x.numerator*10**18//x.denominator,10**18)
def primary_endpoint(K,epsilon,du,initial):
    K,epsilon,initial=map(F,[K,epsilon,initial]);du=m.iv(du)
    require(K>=0 and epsilon>=0 and initial>0 and du.lo>=0,'RICCATI_DOMAIN')
    if epsilon==0:return initial/(1+K*initial*du)
    return epsilon/((1+epsilon/initial)*m.exp_i(K*epsilon*du)-1)
def rational_lower(K,epsilon,du_upper,initial):
    K,epsilon,du_upper,initial=map(F,[K,epsilon,du_upper,initial])
    require(K>=0 and epsilon>=0 and initial>0 and du_upper>=0,'CONTROL_DOMAIN')
    if epsilon==0:return initial/(1+K*initial*du_upper)
    x=K*epsilon*du_upper;require(x<1,'CONTROL_X_LT_ONE')
    return epsilon/((1+epsilon/initial)/(1-x)-1)

def proof_cell(s):
    task=load(ROOT/'inputs'/TASK);parent=load(ROOT/'inputs'/PARENT)
    guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json');primary,control=[ev['rows'][43] for ev in guard['evaluators']]
    cap=load(ROOT/'inputs/q048_prefix_config_v1.json');prefix.validate_config(cap);case=cap['cases']['hillipop-ede_n3'];flags=case['background']['thermal_flags'];t=prefix.parameters(case)
    require(all(flags[z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']) and all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),'FIXED_SWIFT_SOURCE')
    a=m.I(F(1,1021),F(1,1011));w=m.I(F(-1,1000000),F(1,100));eps=F(1,1000000);h0=F(parent['connected_lower']);hmax=F(99999,100000)
    B,floor,H,Hs=old.background(a,t,F(primary['E_safe_left']));HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a;Tgamma=t['T0']/a;ratio=1-w
    fit=d.interval(load(ROOT/'inputs/q048_p3_scaled_raw_result_v2.json')['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    source={'model4':all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),'fixed_flags':all(flags[z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'above900':1010>900,'TR':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma':1775<Tgamma.lo<=Tgamma.hi<4415,'ratio':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'H_positive':HsK.lo>0,'guard_admitted':primary['accepted'] and primary['committed'] and primary['whole_cell_qualified'] and primary['domain']['admitted'] and all(primary['domain']['checks'].values())}
    require(all(source.values()),'NEW_CELL_SOURCE_DOMAIN')
    alpha,rr=old.load_atomic(ROOT/'inputs/q048_p3_scaled_transformed_log_tables_v2.json');atomic=old.local_atomic(alpha,rr,TR,ratio)
    A=list(map(old.fromk,atomic['Alpha']));Ae=list(map(old.fromk,atomic['Alpha_eq']));R=old.fromk(atomic['R2p2s']);n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    require(min(z.lo for z in A+Ae+[R,n,saha]+Beta)>0,'ATOMIC_POSITIVE')
    Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo;K=ceil18(Kexact)
    du0=k.log_i(k.I(a.hi/a.lo));du=m.I(du0.lo,du0.hi);endpoint=primary_endpoint(K,eps,du,h0);duupper=a.hi/a.lo-1;control_lower=rational_lower(K,eps,duupper,h0);hmin=floor18(min(endpoint.lo,control_lower))
    require(K>0 and 0<hmin<=h0,'POSITIVE_CONNECTED_LOWER')
    h=m.I(hmin,hmax);L=m.const('8.2206');P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*R+L;gp=Beta[1]+R+P;D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P);Ns=L*gp+3*R*P;Np=P*gs+R*L;ds=Beta[0]*gp+3*R*Beta[1];dp=Beta[1]*gs+R*Beta[0]
    C={'Beta':Beta,'R':R,'L':L,'P':P,'gamma_s':gs,'gamma_p':gp,'D_positive_form':D,'Ns':Ns,'Np':Np,'D_minus_Ns_positive_form':ds,'D_minus_Np_positive_form':dp,'C_s_certified':m.I((Ns/D).lo,1),'C_p_certified':m.I((Np/D).lo,1)}
    require(min(z.lo for z in [L,P,gs,gp,D,Ns,Np,ds,dp])>0,'C_POSITIVE')
    branches={}
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)];thermal=old.thermal_certificate(a,h,q,t,Hs)
        admitted=all(z.lo>0 for z in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and thermal['faces']['admitted']
        branches[label]={'q':q,'upper_h_face_terms':high,'thermal':thermal,'admitted':admitted}
        require(admitted,'NEW_CELL_UPPER_H_THERMAL:'+label)
    return d.encode({'a':a,'z':[1020,1010],'source_flags':flags,'source_domain_checks':source,'B0':B,'floor':floor,'E_safe_left':F(primary['E_safe_left']),'H_Mpc_inverse':H,'Hs_per_second':Hs,'Hs_for_K':HsK,'nH_cm3':n,'TR_eV':TR,'Tgamma_K':Tgamma,'TM_over_TR':ratio,'fit_denominator':fit,'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'Saha_HyRec':saha,'C_factor_certificate':C,
      'comparison':{'method':'COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V90','orientation':'ell_u <= F_q','initial_a':a.lo,'initial_lower':h0,'parent_endpoint_a':parent['endpoint']['a'],'parent_endpoint_lower_projection':h0,'epsilon':eps,'old_cell_K':parent['K_upper'],'K_unrounded_upper':Kexact,'K_upper':K,'K_requalified_on_new_domain':True,'K_reused_without_proof':False,'H_divisor_role':'POSITIVE_ORDINARY_BACKGROUND_LOWER','du':du,'exp_argument':K*eps*du,'endpoint_primary':endpoint,'control_log_upper':duupper,'control_exp_argument':K*eps*duupper,'endpoint_control_lower':control_lower,'whole_cell_h_min':hmin,'h_domain':h,'w_domain':w,'source_state_reset':False,'physical_state_reset':False,'comparison_glued_to_parent':True},'branches':branches,'guard_primary':primary,'guard_control':control,'guard_primary_row_sha256':digest(primary),'guard_control_row_sha256':digest(control),'actual_frontiers':parent['frontiers'],'actual_scalar_endpoint':parent['endpoint']})

def main():
    s=load_spec();freeze=load(ROOT/'q048_moving_h_domain_freeze_v90.json')
    require(freeze['spec_sha256']==sha(ROOT/SPEC) and freeze['execution_fingerprint']==s['execution_fingerprint'] and freeze['preflight_status']=='PASS','FINAL_FREEZE_REQUIRED')
    require(not (ROOT/RAW).exists(),'IMMUTABLE_OUTPUT_EXISTS')
    output('q048_moving_h_domain_producer_invocation_v90.json',{'kind':'FRESH_ONE_CELL_MATH_PRODUCER','count':1,'execution_fingerprint':s['execution_fingerprint'],'start_utc':datetime.now(timezone.utc).isoformat(),'command':'python3 q048_moving_h_domain_v90.py','pid':os.getpid()})
    start=time.monotonic();stamp=datetime.now(timezone.utc).isoformat();r=proof_cell(s);elapsed=time.monotonic()-start;require(elapsed<300,'SCIENCE_BUDGET')
    r.update(schema_version='Q048_MOVING_H_DOMAIN_RESULT_V90',q='Q048',target_q='Q048',prompt_id='BUBBLEVERSE.MATHEMATICS',prompt_version='2.1.0',exact_question=s['exact_question'],question_sha256=s['question_sha256'],source_commit=s['source_commit'],capture_sha256=s['capture_sha256'],task_id=s['task_id'],task_fingerprint=s['task_fingerprint'],execution_fingerprint=s['execution_fingerprint'],result_id='LOCAL-Q048-MOVING-H-DOMAIN-V90',run_id='LOCAL-Q048-MOVING-H-DOMAIN-V90-'+stamp,program_id=s['program_id'],spec_sha256=sha(ROOT/SPEC),producer_sha256=sha(__file__),proof_contract_sha256=s['contract_markdown_sha256'],parent_actual_checkpoint_sha256=sha(ROOT/'inputs'/PARENT),parent_result_sha256=s['parent_raw_sha256_inherited'],parent_validation_sha256=s['parent_validation_sha256_inherited'],parent_raw_bytes_consumed=False,parent_validation_bytes_consumed=False,guard_raw_sha256=sha(ROOT/'inputs/q048_guard_local_v_result_v12.json'),guard_validation_sha256=sha(ROOT/'inputs/q048_guard_local_v_validation_v12.json'),status='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL',technical_state='PENDING_VALIDATION',scientific_state='INCONCLUSIVE',new_mathematical_proof_cells=1,new_actual_paired_cells=0,retained_actual_paired_cells=106,q_complete=False,complete_a1_certificate=False,final_delta_xe_bounds_computed=False,final_delta_tau_bounds_computed=False,native_P6='UNRESOLVED',physical_falsification=False,accepted_model_change=False,prior_science_reexecuted=False,actual_consumer_executed=False,guard_regenerated=False,return_route='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0',stop={'stop_z':1010,'no_continuation_below1010':True,'max_new_proof_cells':1,'max_new_actual_cells':0},historical_reproducibility_gap=s['historical_provenance_gaps'],execution={'start_utc':stamp,'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':elapsed,'python':platform.python_version(),'platform':platform.platform(),'backend':'LOCAL_RUNTIME','native_or_paid_runs':0})
    output(RAW,r)
    cp={'schema_version':'Q048_MOVING_H_DOMAIN_CANDIDATE_CHECKPOINT_V90','q':'Q048','target_q':'Q048','source_result':RAW,'source_result_sha256':sha(ROOT/RAW),'technical_state':'PENDING_VALIDATION','checkpoint_kind':'CANDIDATE_MATHEMATICAL_PROOF','accepted':False,'proof_cell_z':[1020,1010],'proof_cell_a':['1/1021','1/1011'],'parent_actual_checkpoint_sha256':r['parent_actual_checkpoint_sha256'],'actual_frontiers':r['actual_frontiers'],'actual_scalar_endpoint':r['actual_scalar_endpoint'],'total_actual_paired_cells':106,'new_actual_paired_cells':0,'new_mathematical_proof_cells':1,'comparison_start_lower':r['comparison']['initial_lower'],'comparison_endpoint_lower':r['comparison']['whole_cell_h_min'],'comparison_K_upper':r['comparison']['K_upper'],'physical_state_reset':False,'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint']}
    output('q048_moving_h_domain_candidate_checkpoint_v90.json',cp)
    print(json.dumps({'status':r['status'],'K_upper':r['comparison']['K_upper'],'connected_lower':r['comparison']['whole_cell_h_min'],'actual_count':106,'actual_frontier':1020,'elapsed_seconds':elapsed},indent=2))
if __name__=='__main__':main()
