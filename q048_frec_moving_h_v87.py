"""Fresh V87 one-cell actual consumer. Reuses source/rate helpers; never executes prior producers."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,sys,time,platform,os
from q048_v87_consumer_contract import ROOT,TASK,PARENT,PROOF,RAW,SPEC,sha,load,require,output,load_spec,digest
sys.path.insert(0,str(ROOT/'inputs'))
import q048_full_tube_reuse_v1 as old
m=old.m;d=old.d;prefix=old.prefix

def produce(s):
    task=load(ROOT/'inputs'/TASK);parent=load(ROOT/'inputs'/PARENT)
    proof=load(ROOT/'inputs/q048_moving_h_domain_result_v86.json')
    cap=load(ROOT/'inputs/q048_prefix_config_v1.json');prefix.validate_config(cap)
    case=cap['cases']['hillipop-ede_n3'];t=prefix.parameters(case);flags=case['background']['thermal_flags']
    guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json')
    primary,control=[next(r for r in ev['rows'] if [r['z0'],r['z1']]==[1040,1030]) for ev in guard['evaluators']]
    co=proof['comparison'];a=m.I(F(1,1041),F(1,1031));h=d.interval(co['h_domain']);w=d.interval(co['w_domain'])
    B,floor,H,Hs=old.background(a,t,F(primary['E_safe_left']))
    TR=m.const('8.617343e-5')*t['T0']/a;Tgamma=t['T0']/a;ratio=1-w
    fit=d.interval(load(ROOT/'inputs/q048_p3_scaled_raw_result_v2.json')['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    sc={'model4':all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),
        'fixed_flags':all(flags[k]==0 for k in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),
        'above900':1030>900,'TR':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma':1775<Tgamma.lo<=Tgamma.hi<4415,
        'ratio':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'positive_H':Hs.lo>0,
        'guard_admitted':primary['accepted'] and primary['committed'] and primary['whole_cell_qualified'] and primary['domain']['admitted'] and all(primary['domain']['checks'].values()),
        'inherited_domains':all(proof['source_domain_checks'].values())}
    require(all(sc.values()),'FRESH_SOURCE_DOMAIN')
    for actual,key in [(a,'a'),(B,'B0'),(floor,'floor'),(H,'H_Mpc_inverse'),(Hs,'Hs_per_second'),(TR,'TR_eV'),(Tgamma,'Tgamma_K'),(ratio,'TM_over_TR'),(fit,'fit_denominator')]:require(d.encode(actual)==proof[key],'FRESH_PROOF_BINDING:'+key)
    alpha,rr=old.load_atomic(ROOT/'inputs/q048_p3_scaled_transformed_log_tables_v2.json')
    atomic=old.local_atomic(alpha,rr,TR,ratio);A=list(map(old.fromk,atomic['Alpha']));Ae=list(map(old.fromk,atomic['Alpha_eq']));R=old.fromk(atomic['R2p2s'])
    n=t['nH0']/a**3*m.const('1e-6');saha=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    beta=[Ae[i]*m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    require(d.encode(HsK)==proof['Hs_for_K'],'FRESH_ORDINARY_H_LOWER')
    K=F(co['K_upper']);Kr=n.hi*(A[0].hi+A[1].hi)/HsK.lo
    require(K>=Kr and min(z.lo for z in A+Ae+[R,n,saha]+beta)>0,'ATOMIC_POSITIVITY_K')
    L=m.const('8.2206');P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=beta[0]+3*R+L;gp=beta[1]+R+P;D=(beta[0]+L)*(beta[1]+R+P)+3*R*(beta[1]+P)
    Ns=L*gp+3*R*P;Np=P*gs+R*L;ds=beta[0]*gp+3*R*beta[1];dp=beta[1]*gs+R*beta[0]
    C={'Beta':beta,'R':R,'L':L,'P':P,'gamma_s':gs,'gamma_p':gp,'D_positive_form':D,'Ns':Ns,'Np':Np,'D_minus_Ns_positive_form':ds,'D_minus_Np_positive_form':dp,'C_s_certified':m.I((Ns/D).lo,1),'C_p_certified':m.I((Np/D).lo,1)}
    require(min(z.lo for z in [L,P,gs,gp,D,Ns,Np,ds,dp])>0,'C_CERTIFICATE_POSITIVE')
    require(d.encode(C)==proof['C_factor_certificate'],'FRESH_C_PROOF_MATCH')
    for values,key in [(A,'Alpha'),(Ae,'Alpha_eq'),(R,'R2p2s'),(n,'nH_cm3'),(saha,'Saha_HyRec')]:require(d.encode(values)==proof[key],'FRESH_ATOMIC_MATCH:'+key)
    initial=F(parent['connected_lower']);accepted=F(task['candidate_success_state']['connected_lower']);eps=F(1,1000000);du=F(10,1031);x=K*eps*du
    require(0<x<1,'RATIONAL_EXP_DOMAIN');expupper=1/(1-x);lower=eps*initial/((initial+eps)*expupper-initial)
    require(0<accepted<=lower and accepted<=F(co['endpoint_primary']['lo']),'CONNECTED_LOWER_CONTROL')
    branches={}
    for label,q in [('L',eps),('R',F(0))]:
        terms=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(h.hi),q) for i in range(2)]
        thermal=old.thermal_certificate(a,h,q,t,Hs)
        require(all(z.lo>0 for z in terms) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and thermal['faces']['admitted'],'FRESH_BRANCH_GATE:'+label)
        branches[label]={'q':q,'upper_h_face_terms':terms,'thermal':thermal,'admitted':True}
        require(d.encode(branches[label])==proof['branches'][label],'FRESH_BRANCH_PROOF_MATCH:'+label)
    return d.encode({'a':a,'h_domain':h,'w_domain':w,'source_domain_checks':sc,'source_flags':flags,'B0':B,'floor':floor,'H':H,'Hs':Hs,'Hs_for_K':HsK,'TR_eV':TR,'Tgamma_K':Tgamma,'TM_over_TR':ratio,'fit_denominator':fit,'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'nH_cm3':n,'Saha_HyRec':saha,'C_certificate':C,'K_upper':K,'K_required':Kr,'lower_recheck':{'initial':initial,'accepted_lower':accepted,'epsilon':eps,'du_upper':du,'x':x,'exp_upper':expupper,'rational_control_lower':lower},'branches':branches,
      'actual_before':task['initial_actual_state'],'candidate_after':task['candidate_success_state'],'guard_primary_sha256':digest(primary),'guard_control_sha256':digest(control)})

def main():
    s=load_spec();require(not (ROOT/RAW).exists(),'IMMUTABLE_RESULT_EXISTS')
    freeze=load(ROOT/'q048_frec_moving_h_freeze_v87.json')
    require(freeze['spec_sha256']==sha(ROOT/SPEC) and freeze['execution_fingerprint']==s['execution_fingerprint'] and freeze['preflight_status']=='PASS','FINAL_FREEZE_REQUIRED')
    output('q048_frec_moving_h_producer_invocation_v87.json',{'kind':'FRESH_SCIENCE_PRODUCER','count':1,'execution_fingerprint':s['execution_fingerprint'],'start_utc':datetime.now(timezone.utc).isoformat(),'command':'python3 q048_frec_moving_h_v87.py','pid':os.getpid()})
    start=time.monotonic();stamp=datetime.now(timezone.utc).isoformat()
    result=produce(s);elapsed=time.monotonic()-start;require(elapsed<300,'SCIENCE_BUDGET_EXCEEDED')
    result.update(schema='bubbleverse.q048.frec_moving_h.actual_consumer.v87',q='Q048',target_q='Q048',exact_question=s['exact_question'],question_sha256=s['question_sha256'],source_commit=s['source_commit'],capture_sha256=s['capture_sha256'],task_id=s['task_id'],task_fingerprint=s['task_fingerprint'],execution_fingerprint=s['execution_fingerprint'],result_id='LOCAL-Q048-FREC-MOVING-H-ACTUAL-CONSUMER-V87',run_id='LOCAL-Q048-FREC-MOVING-H-V87-'+stamp,program_id=s['program_id'],technical_state='PENDING_VALIDATION',status='ONE_NEW_ACTUAL_CELL_PENDING_VALIDATION',new_actual_cells=1,new_actual_accepted=0,new_math_proof_cells=0,cell_z=[1040,1030],spec_sha256=sha(ROOT/SPEC),producer_sha256=sha(Path(__file__)),proof_checkpoint_sha256=sha(ROOT/'inputs'/PROOF),proof_validation_sha256=sha(ROOT/'inputs/q048_moving_h_domain_validation_v86.json'),parent_checkpoint_sha256=sha(ROOT/'inputs'/PARENT),contract_markdown_sha256=s['contract_markdown_sha256'],physical_reset=False,q_complete=False,NativeP6='UNRESOLVED',complete_histories=False,delta_tau_bounds=False,accepted_model_change=False,proof_reexecuted=False,parent_consumer_reexecuted=False,guard_regenerated=False,return_route='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0',stop={'stop_z':1030,'one_cell_only':True,'below1030_authorized':False},runtime={'start_utc':stamp,'elapsed_seconds':elapsed,'python':platform.python_version(),'platform':platform.platform(),'backend':'LOCAL_RUNTIME'},shared_method_disclosure='Pinned source/rate/interval helpers and accepted proof lineage reused; no method independence, native trajectory or independent physical evidence claimed.')
    output(RAW,result)
    cp={'schema':'bubbleverse.q048.frec_moving_h.candidate_checkpoint.v87','q':'Q048','target_q':'Q048','checkpoint_kind':'CANDIDATE_ACTUAL','technical_state':'PENDING_VALIDATION','candidate_after':result['candidate_after'],'result_sha256':sha(ROOT/RAW),'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint'],'accepted':False}
    output('q048_frec_moving_h_candidate_checkpoint_v87.json',cp)
    print(json.dumps({'status':result['status'],'candidate_after':result['candidate_after'],'elapsed_seconds':elapsed},indent=2))
if __name__=='__main__':main()
