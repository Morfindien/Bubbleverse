"""Producer-free V90 verification with fresh source recomputation and exponent-free rational control.
No producer import, no previous scientific main/validator execution. Shared source/rate/interval primitives are disclosed.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
from copy import deepcopy
import sys,json,time
from q048_v90_proof_contract import ROOT,TASK,PARENT,RAW,SPEC,load,sha,digest,output,load_spec,validate_spec
sys.path.insert(0,str(ROOT/'inputs'))
import q048_full_tube_reuse_v1 as old
m=old.m;d=old.d;k=old.k

def source_expected():
    cap=load(ROOT/'inputs/q048_prefix_config_v1.json');old.prefix.validate_config(cap);case=cap['cases']['hillipop-ede_n3'];t=old.prefix.parameters(case);flags=case['background']['thermal_flags']
    parent=load(ROOT/'inputs'/PARENT);guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json');row=guard['evaluators'][0]['rows'][43]
    a=m.I(F(1,1021),F(1,1011));w=m.I(F(-1,1000000),F(1,100));eps=F(1,1000000);h0=F(parent['connected_lower']);hmax=F(99999,100000)
    B,floor,H,Hs=old.background(a,t,F(row['E_safe_left']));HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a;Tgamma=t['T0']/a;ratio=1-w;fit=d.interval(load(ROOT/'inputs/q048_p3_scaled_raw_result_v2.json')['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    alpha,rr=old.load_atomic(ROOT/'inputs/q048_p3_scaled_transformed_log_tables_v2.json');atom=old.local_atomic(alpha,rr,TR,ratio)
    A=[old.fromk(x) for x in atom['Alpha']];Ae=[old.fromk(x) for x in atom['Alpha_eq']];R=old.fromk(atom['R2p2s']);n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo;K=F(-((-Kexact.numerator*10**18)//Kexact.denominator),10**18)
    logarithm=k.log_i(k.I(a.hi/a.lo));du=m.I(logarithm.lo,logarithm.hi);exp_arg=K*eps*du;E=m.exp_i(exp_arg)
    endpoint=eps/((1+eps/h0)*E-1)
    control_du=F(10,1011);x=K*eps*control_du
    if not 0<=x<1:raise ValueError('VERIFIER_RATIONAL_CONTROL_DOMAIN')
    # Independent exact rational algebra: no log/exp or interval helper in this control.
    rational=eps*h0*(1-x)/(eps+h0*x)
    chosen=min(endpoint.lo,rational);hmin=F(chosen.numerator*10**18//chosen.denominator,10**18)
    h=m.I(hmin,hmax);L=m.const('8.2206');P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*R+L;gp=Beta[1]+R+P;D=(Beta[0]+L)*(Beta[1]+R+P)+3*R*(Beta[1]+P);Ns=L*gp+3*R*P;Np=P*gs+R*L;ds=Beta[0]*gp+3*R*Beta[1];dp=Beta[1]*gs+R*Beta[0]
    C={'Beta':Beta,'R':R,'L':L,'P':P,'gamma_s':gs,'gamma_p':gp,'D_positive_form':D,'Ns':Ns,'Np':Np,'D_minus_Ns_positive_form':ds,'D_minus_Np_positive_form':dp,'C_s_certified':m.I((Ns/D).lo,1),'C_p_certified':m.I((Np/D).lo,1)}
    source={'model4':all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),'fixed_flags':all(flags[z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'above900':1010>900,'TR':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma':1775<Tgamma.lo<=Tgamma.hi<4415,'ratio':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'H_positive':HsK.lo>0,'guard_admitted':row['accepted'] and row['committed'] and row['whole_cell_qualified'] and row['domain']['admitted'] and all(row['domain']['checks'].values())}
    branches={}
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)];thermal=old.thermal_certificate(a,h,q,t,Hs)
        branches[label]={'q':q,'upper_h_face_terms':high,'thermal':thermal,'admitted':all(v.lo>0 for v in high) and thermal['thermal_denominator'].lo>0 and thermal['beta'].lo>0 and thermal['faces']['admitted']}
    # Second interval algebra for the same closed form. It is not assumed byte-identical.
    alternative=eps*h0/((h0+eps)*E-h0)
    expected=d.encode({'a':a,'z':[1020,1010],'source_flags':flags,'source_domain_checks':source,'B0':B,'floor':floor,'E_safe_left':F(row['E_safe_left']),'H_Mpc_inverse':H,'Hs_per_second':Hs,'Hs_for_K':HsK,'nH_cm3':n,'TR_eV':TR,'Tgamma_K':Tgamma,'TM_over_TR':ratio,'fit_denominator':fit,'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'Saha_HyRec':saha,'C_factor_certificate':C,'branches':branches})
    expected['comparison_expected']=d.encode({'K_unrounded_upper':Kexact,'K_upper':K,'du':du,'exp_argument':exp_arg,'endpoint_primary':endpoint,'control_log_upper':control_du,'control_exp_argument':x,'endpoint_control_lower':rational,'whole_cell_h_min':hmin,'h_domain':h,'w_domain':w})
    expected['dual_interval_lower']=str(alternative.lo)
    return expected

def core_validate(r,cp,s,expected,links=True):
    checks=[]
    def t(k,b):checks.append({'check':k,'pass':bool(b)})
    try:validate_spec(s,False);t('metadata_contract',True)
    except (ValueError,KeyError,TypeError):t('metadata_contract',False)
    task=load(ROOT/'inputs'/TASK);parent=load(ROOT/'inputs'/PARENT);guard=load(ROOT/'inputs/q048_guard_local_v_result_v12.json');co=r['comparison']
    t('scope',r['q']==r['target_q']==cp['q']==cp['target_q']=='Q048')
    t('exact_question',r['exact_question']==s['exact_question']==task['exact_question'] and r['question_sha256']==s['question_sha256'])
    t('task_identity',r['task_id']==s['task_id'] and r['task_fingerprint']==s['task_fingerprint'])
    t('execution_identity',r['execution_fingerprint']==cp['execution_fingerprint']==s['execution_fingerprint'])
    t('program',r['program_id']==s['program_id'])
    t('result_identity',r['result_id']=='LOCAL-Q048-MOVING-H-DOMAIN-V90' and r['run_id'].startswith('LOCAL-Q048-MOVING-H-DOMAIN-V90-'))
    t('contract_hash',r['proof_contract_sha256']==s['contract_markdown_sha256'])
    t('spec_identity',r['spec_sha256']==cp['spec_sha256']==sha(ROOT/SPEC))
    t('source_capture',r['source_commit']==s['source_commit'] and r['capture_sha256']==s['capture_sha256'])
    t('parent_hash',r['parent_actual_checkpoint_sha256']==cp['parent_actual_checkpoint_sha256']==sha(ROOT/'inputs'/PARENT))
    t('parent_raw_provenance',r['parent_result_sha256']==s['parent_raw_sha256_inherited'] and r['parent_raw_bytes_consumed'] is False)
    t('parent_validation_provenance',r['parent_validation_sha256']==s['parent_validation_sha256_inherited'] and r['parent_validation_bytes_consumed'] is False)
    t('guard_hash',r['guard_raw_sha256']==sha(ROOT/'inputs/q048_guard_local_v_result_v12.json') and r['guard_validation_sha256']==sha(ROOT/'inputs/q048_guard_local_v_validation_v12.json'))
    for label,ev in zip(['primary','control'],guard['evaluators']):
        t('guard_'+label,r['guard_'+label]==ev['rows'][43] and r['guard_'+label+'_row_sha256']==digest(ev['rows'][43])==task['guard_binding'][label+'_row_sha256'])
    t('cell',r['z']==cp['proof_cell_z']==[1020,1010] and cp['proof_cell_a']==['1/1021','1/1011'])
    t('actual_count',r['retained_actual_paired_cells']==cp['total_actual_paired_cells']==106 and r['new_actual_paired_cells']==cp['new_actual_paired_cells']==0)
    t('actual_frontiers',r['actual_frontiers']==cp['actual_frontiers']==parent['frontiers'])
    t('actual_scalar',r['actual_scalar_endpoint']==cp['actual_scalar_endpoint']==parent['endpoint'])
    t('proof_count',r['new_mathematical_proof_cells']==cp['new_mathematical_proof_cells']==1)
    t('pending_only',r['technical_state']==cp['technical_state']=='PENDING_VALIDATION' and cp['checkpoint_kind']=='CANDIDATE_MATHEMATICAL_PROOF' and cp['accepted'] is False)
    t('status',r['status']=='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL')
    for key,value in expected.items():
        if key not in ['comparison_expected','dual_interval_lower']:t('fresh_source_recomputation:'+key,r[key]==value)
    for key,value in expected['comparison_expected'].items():t('fresh_comparison:'+key,co[key]==value)
    t('comparison_identity',co['method']=='COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V90' and co['orientation']=='ell_u <= F_q')
    h0=F(parent['connected_lower']);eps=F(1,1000000);K=F(co['K_upper']);Kexact=F(co['K_unrounded_upper']);lower=F(co['whole_cell_h_min']);x=K*eps*F(10,1011)
    t('initial_lower',F(co['initial_lower'])==F(co['parent_endpoint_lower_projection'])==h0 and h0>0)
    t('initial_a',co['initial_a']==co['parent_endpoint_a']==parent['endpoint']['a']=='1/1021')
    t('epsilon',F(co['epsilon'])==eps)
    t('old_K_history',co['old_cell_K']==parent['K_upper'])
    t('fresh_K',co['K_requalified_on_new_domain'] is True and co['K_reused_without_proof'] is False and K>=Kexact>0 and K-Kexact<F(1,10**18))
    t('H_divisor',co['H_divisor_role']=='POSITIVE_ORDINARY_BACKGROUND_LOWER')
    t('source_checks',len(r['source_domain_checks'])==9 and all(v is True for v in r['source_domain_checks'].values()))
    rational=eps*h0*(1-x)/(eps+h0*x)
    t('independent_rational_control',0<=x<1 and F(co['endpoint_control_lower'])==rational and F(co['control_exp_argument'])==x)
    t('safe_positive_lower',0<lower<=h0 and lower<=rational and lower<=F(co['endpoint_primary']['lo']) and lower<=F(expected['dual_interval_lower']))
    chosen=min(F(co['endpoint_primary']['lo']),rational);floor18=F(chosen.numerator*10**18//chosen.denominator,10**18)
    t('conservative_rounding',lower==floor18)
    t('comparison_no_reset',co['physical_state_reset'] is False and co['source_state_reset'] is False and co['comparison_glued_to_parent'] is True)
    t('h_domain',F(co['h_domain']['lo'])==lower and F(co['h_domain']['hi'])==F(99999,100000))
    t('w_domain',F(co['w_domain']['lo'])==F(-1,1000000) and F(co['w_domain']['hi'])==F(1,100))
    t('candidate_numbers',cp['comparison_start_lower']==co['initial_lower'] and cp['comparison_endpoint_lower']==co['whole_cell_h_min'] and cp['comparison_K_upper']==co['K_upper'] and cp['physical_state_reset'] is False)
    def pos(v):return 0<F(v['lo'])<=F(v['hi'])
    C=r['C_factor_certificate']
    for key in ['L','P','R','gamma_s','gamma_p','D_positive_form','Ns','Np','D_minus_Ns_positive_form','D_minus_Np_positive_form']:t('C_positive:'+key,pos(C[key]))
    for label in ['s','p']:t('C_bounded:'+label,0<F(C['C_'+label+'_certified']['lo'])<=F(C['C_'+label+'_certified']['hi'])==1)
    t('branches',set(r['branches'])=={'L','R'})
    for label,q in [('L',eps),('R',F(0))]:
        br=r['branches'][label];th=br['thermal'];b=F(th['beta']['lo'])
        t('branch_q:'+label,F(br['q'])==q);t('branch_admitted:'+label,br['admitted'] is True)
        t('upper_h:'+label,len(br['upper_h_face_terms'])==2 and all(pos(z) for z in br['upper_h_face_terms']))
        t('thermal:'+label,pos(th['beta']) and pos(th['thermal_denominator']) and th['faces']['admitted'] is True and F(th['faces']['lower_face_inward_lower'])==1+(1+b)*F(1,1000000) and F(th['faces']['upper_face_inward_margin'])==(1+b)*F(1,100)-1>0)
    for key in ['q_complete','complete_a1_certificate','final_delta_xe_bounds_computed','final_delta_tau_bounds_computed','physical_falsification','accepted_model_change','prior_science_reexecuted','actual_consumer_executed','guard_regenerated']:t('no_overclaim:'+key,r[key] is False)
    t('NativeP6',r['native_P6']=='UNRESOLVED')
    t('return',r['return_route']=='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0')
    t('stop',r['stop']=={'stop_z':1010,'no_continuation_below1010':True,'max_new_proof_cells':1,'max_new_actual_cells':0})
    t('backend_budget',r['execution']['backend']=='LOCAL_RUNTIME' and 0<=r['execution']['elapsed_seconds']<300 and r['execution']['native_or_paid_runs']==0)
    if links:
        t('raw_hash',cp['source_result_sha256']==sha(ROOT/RAW))
        t('spec_hash',r['spec_sha256']==cp['spec_sha256']==sha(ROOT/SPEC))
        t('producer_code',r['producer_sha256']==sha(ROOT/'q048_moving_h_domain_v90.py'))
    return checks

def mutations(r,cp,s,e):
    edits=[
      ('WRONG_Q',lambda x,y,z:x.update(q='Q049')),('WRONG_TARGET',lambda x,y,z:x.update(target_q='Q047')),('WRONG_TASK',lambda x,y,z:x.update(task_fingerprint='bad')),('WRONG_EXECUTION',lambda x,y,z:x.update(execution_fingerprint='bad')),
      ('MISSING_CONTRACT_HASH',lambda x,y,z:z.pop('contract_markdown_sha256')),('WRONG_CONTRACT_HASH',lambda x,y,z:x.update(proof_contract_sha256='0'*64)),('WRONG_PARENT',lambda x,y,z:x.update(parent_actual_checkpoint_sha256='bad')),
      ('MISSING_SPEC_HASH',lambda x,y,z:x.pop('spec_sha256')),('WRONG_SPEC_HASH',lambda x,y,z:x.update(spec_sha256='0'*64)),('MISSING_SPEC_CODE_PINS',lambda x,y,z:z.pop('code_pins')),('WRONG_SPEC_FINGERPRINT',lambda x,y,z:z.update(execution_fingerprint='bad')),
      ('WRONG_CELL',lambda x,y,z:x.update(z=[1020,1000])),('WRONG_A',lambda x,y,z:x['a'].update(hi='1/1010')),('OLD_K_SUBSTITUTION',lambda x,y,z:x['comparison'].update(K_upper=x['comparison']['old_cell_K'])),
      ('FALSE_K_QUALIFICATION',lambda x,y,z:x['comparison'].update(K_requalified_on_new_domain=False)),('RESET_INITIAL_LOWER',lambda x,y,z:x['comparison'].update(initial_lower='1/2')),('FORGED_LOWER',lambda x,y,z:x['comparison'].update(whole_cell_h_min='1/2')),
      ('FORGED_CONTROL',lambda x,y,z:x['comparison'].update(endpoint_control_lower='1')),('BAD_DU',lambda x,y,z:x['comparison'].update(control_log_upper='0')),('BAD_EPSILON',lambda x,y,z:x['comparison'].update(epsilon='0')),
      ('SOURCE_FLAG',lambda x,y,z:x['source_flags'].update(has_varconst=1)),('FALSE_SOURCE_DOMAIN',lambda x,y,z:x['source_domain_checks'].update(TR=False)),('EMPTY_SOURCE_DOMAINS',lambda x,y,z:x.update(source_domain_checks={})),
      ('NEGATIVE_ALPHA',lambda x,y,z:x['Alpha'][0].update(lo='-1')),('BAD_H_DIVISOR',lambda x,y,z:x['Hs_for_K'].update(lo='1')),('NEGATIVE_C_D',lambda x,y,z:x['C_factor_certificate']['D_positive_form'].update(lo='-1')),('C_ABOVE_ONE',lambda x,y,z:x['C_factor_certificate']['C_s_certified'].update(hi='2')),
      ('GUARD_UNCOMMITTED',lambda x,y,z:x['guard_primary'].update(committed=False)),('GUARD_CONTROL_HASH',lambda x,y,z:x.update(guard_control_row_sha256='bad')),('MISSING_R_BRANCH',lambda x,y,z:x['branches'].pop('R')),('WRONG_R_Q',lambda x,y,z:x['branches']['R'].update(q='1/1000000')),
      ('NEGATIVE_HIGH_FACE',lambda x,y,z:x['branches']['L']['upper_h_face_terms'][0].update(lo='-1')),('NEGATIVE_THERMAL_MARGIN',lambda x,y,z:x['branches']['R']['thermal']['faces'].update(upper_face_inward_margin='-1')),('FALSE_BRANCH',lambda x,y,z:x['branches']['L'].update(admitted=False)),
      ('ACTUAL_COUNT107',lambda x,y,z:x.update(retained_actual_paired_cells=107)),('ACTUAL_FRONTIER1010',lambda x,y,z:x['actual_frontiers'].update({'hillipop-ede_n3':1010})),('ACTUAL_CONSUMER',lambda x,y,z:x.update(actual_consumer_executed=True)),('NEW_ACTUAL',lambda x,y,z:y.update(new_actual_paired_cells=1)),
      ('RESET',lambda x,y,z:x['comparison'].update(physical_state_reset=True)),('FALSE_GLUE',lambda x,y,z:x['comparison'].update(comparison_glued_to_parent=False)),('FORGE_ACCEPTANCE',lambda x,y,z:y.update(accepted=True)),('FULL_Q',lambda x,y,z:x.update(q_complete=True)),('TAU_BOUNDS',lambda x,y,z:x.update(final_delta_tau_bounds_computed=True)),('BELOW1010',lambda x,y,z:x['stop'].update(no_continuation_below1010=False)),('PRIOR_SCIENCE',lambda x,y,z:x.update(prior_science_reexecuted=True))]
    answer=[]
    for name,edit in edits:
        x,y,z=deepcopy(r),deepcopy(cp),deepcopy(s)
        try:edit(x,y,z);cs=core_validate(x,y,z,e,False);bad=[c['check'] for c in cs if not c['pass']]
        except (ValueError,KeyError,TypeError,ZeroDivisionError) as err:bad=[type(err).__name__+':'+str(err)]
        answer.append({'name':name,'rejected':bool(bad),'rejecting_checks':bad[:6]})
    return answer

def main():
    s=load_spec()
    if '--preflight' in sys.argv:print(json.dumps({'kind':'METADATA_ONLY_NO_SCIENCE','status':'PASS','checks':len(validate_spec(s))}));return
    output('q048_moving_h_domain_verifier_invocation_v90.json',{'kind':'PRODUCER_FREE_VERIFIER','command':'python3 q048_moving_h_domain_verify_v90.py','start_utc':datetime.now(timezone.utc).isoformat(),'execution_fingerprint':s['execution_fingerprint']})
    start=time.monotonic();r=load(ROOT/RAW);cp=load(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json');expected=source_expected()
    output('q048_moving_h_domain_verifier_recomputation_v90.json',expected)
    checks=core_validate(r,cp,s,expected);mm=mutations(r,cp,s,expected);good=all(c['pass'] for c in checks) and all(z['rejected'] for z in mm) and len(mm)>=24
    result={'schema_version':'Q048_MOVING_H_DOMAIN_VALIDATION_V90','q':'Q048','target_q':'Q048','status':'PASS' if good else 'FAIL','technical_state':'PASS' if good else 'FAIL','checks_total':len(checks),'checks_passed':sum(c['pass'] for c in checks),'checks':checks,'mutations_total':len(mm),'mutations_rejected':sum(z['rejected'] for z in mm),'mutations':mm,'result_sha256':sha(ROOT/RAW),'candidate_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_candidate_checkpoint_v90.json'),'spec_sha256':sha(ROOT/SPEC),'validator_sha256':sha(__file__),'verifier_recomputation_sha256':sha(ROOT/'q048_moving_h_domain_verifier_recomputation_v90.json'),'execution_fingerprint':s['execution_fingerprint'],'elapsed_seconds':time.monotonic()-start,'validated_utc':datetime.now(timezone.utc).isoformat(),'producer_imported_or_executed':False,'prior_producer_or_validator_executed':False,'independence_note':'Separate verifier implementation recomputes fresh source/C/upper-h/thermal coefficients using shared pinned primitives. Exact rational inverse-form Bernoulli control avoids log/exp; alternate interval closed form cross-checks lower. Shared source/rate/theorem lineage remains; no full method independence or physical replication.'}
    output('q048_moving_h_domain_validation_v90.json',result)
    print(json.dumps({'status':result['status'],'checks':str(result['checks_passed'])+'/'+str(result['checks_total']),'mutations':str(result['mutations_rejected'])+'/'+str(result['mutations_total']),'failed':[c['check'] for c in checks if not c['pass']],'unrejected':[z['name'] for z in mm if not z['rejected']]}))
    if not good:raise SystemExit(1)
if __name__=='__main__':main()
