"""Producer-free V87 validator. Reads archived proof and fresh serialized candidate; no producer imports."""
from fractions import Fraction as F
from copy import deepcopy
from datetime import datetime,timezone
import json,sys,time
from q048_v87_consumer_contract import ROOT,TASK,PARENT,PROOF,RAW,SPEC,load,sha,digest,output,load_spec,validate_spec

def core_validate(r,cp,s,links=True):
    tests=[]
    def t(label,ok):tests.append({'check':label,'pass':bool(ok)})
    try:validate_spec(s,False);t('spec_metadata_contract',True)
    except (ValueError,KeyError,TypeError):t('spec_metadata_contract',False)
    task=load(ROOT/'inputs'/TASK);proof=load(ROOT/'inputs/q048_moving_h_domain_result_v86.json');parent=load(ROOT/'inputs'/PARENT)
    t('q',r['q']==r['target_q']==cp['q']==cp['target_q']=='Q048')
    t('question',r['exact_question']==s['exact_question']==task['exact_question'] and r['question_sha256']==s['question_sha256'])
    t('task',r['task_id']==s['task_id'] and r['task_fingerprint']==s['task_fingerprint'])
    t('program',r['program_id']==s['program_id'])
    t('result_identity',r['result_id']=='LOCAL-Q048-FREC-MOVING-H-ACTUAL-CONSUMER-V87' and r['run_id'].startswith('LOCAL-Q048-FREC-MOVING-H-V87-'))
    t('execution_fingerprint',r['execution_fingerprint']==cp['execution_fingerprint']==s['execution_fingerprint'])
    t('source_capture',r['source_commit']==s['source_commit'] and r['capture_sha256']==s['capture_sha256'])
    t('contract_hash',r['contract_markdown_sha256']==s['contract_markdown_sha256'])
    t('spec_identity',r['spec_sha256']==cp['spec_sha256']==sha(ROOT/SPEC))
    t('cell',r['cell_z']==[1040,1030])
    t('candidate_only',r['technical_state']=='PENDING_VALIDATION' and r['new_actual_accepted']==0 and cp['technical_state']=='PENDING_VALIDATION' and cp['accepted'] is False and cp['checkpoint_kind']=='CANDIDATE_ACTUAL')
    t('count',r['new_actual_cells']==1 and r['new_math_proof_cells']==0)
    t('initial',r['actual_before']==task['initial_actual_state'])
    t('candidate',r['candidate_after']==cp['candidate_after']==task['candidate_success_state'])
    t('parent_hash',r['parent_checkpoint_sha256']==sha(ROOT/'inputs'/PARENT))
    t('proof_hash',r['proof_checkpoint_sha256']==sha(ROOT/'inputs'/PROOF) and r['proof_validation_sha256']==sha(ROOT/'inputs/q048_moving_h_domain_validation_v86.json'))
    t('primary_guard_hash',r['guard_primary_sha256']==task['guard_binding']['primary_row_sha256'])
    t('control_guard_hash',r['guard_control_sha256']==task['guard_binding']['control_row_sha256'])
    primary=task['guard_binding']['primary'];endpoint=r['candidate_after']['endpoint']
    t('endpoint_guard',endpoint=={'a':primary['a1'],'E':primary['E_right'],'Y':primary['Y_right'],'Vbar':primary['V_admitted']})
    expected_source_keys={'model4','fixed_flags','above900','TR','Tgamma','ratio','fit_positive','positive_H','guard_admitted','inherited_domains'}
    t('source_checks',set(r['source_domain_checks'])==expected_source_keys and all(v is True for v in r['source_domain_checks'].values()))
    t('source_flags',r['source_flags']==proof['source_flags'])
    for key in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']:t('source_disabled:'+key,r['source_flags'][key]==0)
    for actual,key in [('a','a'),('B0','B0'),('floor','floor'),('H','H_Mpc_inverse'),('Hs','Hs_per_second'),('Hs_for_K','Hs_for_K'),('TR_eV','TR_eV'),('Tgamma_K','Tgamma_K'),('TM_over_TR','TM_over_TR'),('fit_denominator','fit_denominator'),('Alpha','Alpha'),('Alpha_eq','Alpha_eq'),('R2p2s','R2p2s'),('nH_cm3','nH_cm3'),('Saha_HyRec','Saha_HyRec'),('C_certificate','C_factor_certificate')]:
        t('fresh_coefficient_proof_binding:'+actual,r[actual]==proof[key])
    for key in ['h_domain','w_domain']:t(key,r[key]==proof['comparison'][key])
    def iv(x):return F(x['lo']),F(x['hi'])
    def pos(x):lo,hi=iv(x);return 0<lo<=hi
    t('a_endpoints',iv(r['a'])==(F(1,1041),F(1,1031)))
    t('h_endpoints',iv(r['h_domain'])==(F(task['candidate_success_state']['connected_lower']),F(99999,100000)))
    t('w_endpoints',iv(r['w_domain'])==(F(-1,1000000),F(1,100)))
    t('TR_domain',F('.004')<iv(r['TR_eV'])[0]<=iv(r['TR_eV'])[1]<F('.4'))
    t('Tgamma_domain',1775<iv(r['Tgamma_K'])[0]<=iv(r['Tgamma_K'])[1]<4415)
    for key in ['H','Hs','Hs_for_K','nH_cm3','R2p2s','Saha_HyRec','fit_denominator']:t('positive:'+key,pos(r[key]))
    t('atomic_positive',len(r['Alpha'])==len(r['Alpha_eq'])==2 and all(pos(x) for x in r['Alpha']+r['Alpha_eq']))
    C=r['C_certificate']
    for key in ['L','P','R','gamma_s','gamma_p','D_positive_form','Ns','Np','D_minus_Ns_positive_form','D_minus_Np_positive_form']:t('C_positive:'+key,pos(C[key]))
    t('C_beta',len(C['Beta'])==2 and all(pos(x) for x in C['Beta']))
    for label,num in [('s','Ns'),('p','Np')]:
        lo,hi=iv(C['C_'+label+'_certified']);t('C_unit_interval:'+label,0<lo<=hi==1)
        t('C_lower_quotient:'+label,lo<=F(C[num]['lo'])/F(C['D_positive_form']['hi']))
    Kr=F(r['nH_cm3']['hi'])*(F(r['Alpha'][0]['hi'])+F(r['Alpha'][1]['hi']))/F(r['Hs_for_K']['lo'])
    t('K_fresh_required',F(r['K_required'])==Kr)
    K=F(r['K_upper']);t('K_proof',K==F(proof['comparison']['K_upper']) and K>=Kr)
    c=r['lower_recheck'];initial=F(parent['connected_lower']);eps=F(1,1000000);du=F(10,1031);x=K*eps*du
    t('lower_initial',F(c['initial'])==initial)
    t('lower_parameters',F(c['epsilon'])==eps and F(c['du_upper'])==du and F(c['x'])==x and 0<x<1)
    expupper=1/(1-x);control=eps*initial*(1-x)/(eps+initial*x)
    t('lower_rational_control',F(c['exp_upper'])==expupper and F(c['rational_control_lower'])==control)
    accepted=F(task['candidate_success_state']['connected_lower'])
    t('lower_admission',F(c['accepted_lower'])==accepted and 0<accepted<=control and accepted<=F(proof['comparison']['endpoint_primary']['lo']))
    t('branch_set',set(r['branches'])=={'L','R'})
    for label,q in [('L',eps),('R',F(0))]:
        br=r['branches'][label];t('branch_q:'+label,F(br['q'])==q)
        t('branch_proof_binding:'+label,br==proof['branches'][label]);t('branch_admitted:'+label,br['admitted'] is True)
        t('upper_h_face:'+label,len(br['upper_h_face_terms'])==2 and all(pos(z) for z in br['upper_h_face_terms']))
        th=br['thermal'];t('thermal_denominator:'+label,pos(th['thermal_denominator']))
        t('thermal_beta:'+label,pos(th['beta']))
        blo=F(th['beta']['lo']);low=1-(1+blo)*F(-1,1000000);high=(1+blo)*F(1,100)-1
        t('thermal_faces:'+label,F(th['faces']['lower_face_inward_lower'])==low and F(th['faces']['upper_face_inward_margin'])==high and low>0 and high>0 and th['faces']['admitted'] is True)
    for key in ['physical_reset','q_complete','complete_histories','delta_tau_bounds','accepted_model_change','proof_reexecuted','parent_consumer_reexecuted','guard_regenerated']:t('no_overclaim:'+key,r[key] is False)
    t('NativeP6',r['NativeP6']=='UNRESOLVED')
    t('stop',r['stop']=={'stop_z':1030,'one_cell_only':True,'below1030_authorized':False})
    t('budget_backend',0<=r['runtime']['elapsed_seconds']<300 and r['runtime']['backend']=='LOCAL_RUNTIME')
    t('return',r['return_route']=='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0')
    if links:
        t('raw_hash',cp['result_sha256']==sha(ROOT/RAW))
        t('spec_hash',cp['spec_sha256']==r['spec_sha256']==sha(ROOT/SPEC))
        t('producer_code_hash',r['producer_sha256']==sha(ROOT/'q048_frec_moving_h_v87.py'))
    return tests

def mutations(r,cp,s):
    edits=[
     ('WRONG_Q',lambda x,y,z:x.update(q='Q049')),('WRONG_TARGET',lambda x,y,z:x.update(target_q='Q047')),
     ('WRONG_TASK',lambda x,y,z:x.update(task_fingerprint='bad')),('WRONG_EXECUTION',lambda x,y,z:x.update(execution_fingerprint='bad')),
     ('MISSING_SPEC_CONTRACT_HASH',lambda x,y,z:z.pop('contract_markdown_sha256')),('WRONG_SPEC_CONTRACT_HASH',lambda x,y,z:z.update(contract_markdown_sha256='0'*64)),
     ('MISSING_RESULT_SPEC_HASH',lambda x,y,z:x.pop('spec_sha256')),('WRONG_RESULT_SPEC_HASH',lambda x,y,z:x.update(spec_sha256='0'*64)),
     ('WRONG_RESULT_CONTRACT_HASH',lambda x,y,z:x.update(contract_markdown_sha256='0'*64)),('WRONG_PROOF',lambda x,y,z:x.update(proof_checkpoint_sha256='bad')),
     ('WRONG_PARENT',lambda x,y,z:x.update(parent_checkpoint_sha256='bad')),('ACTUAL_COUNT106',lambda x,y,z:x['candidate_after'].update(count=106)),
     ('FRONTIER1020',lambda x,y,z:x['candidate_after'].update(frontier=1020)),('FORGED_ENDPOINT',lambda x,y,z:x['candidate_after']['endpoint'].update(E='1')),
     ('RESET_LOWER',lambda x,y,z:x['lower_recheck'].update(initial='1/2')),('OLD_K',lambda x,y,z:x.update(K_upper=load(ROOT/'inputs'/PARENT)['K_upper'])),
     ('FORGED_CONTROL_LOWER',lambda x,y,z:x['lower_recheck'].update(rational_control_lower='1')),('SOURCE_FLAG',lambda x,y,z:x['source_flags'].update(has_varconst=1)),
     ('SOURCE_DOMAIN_FALSE',lambda x,y,z:x['source_domain_checks'].update(TR=False)),('EMPTY_SOURCE_CHECKS',lambda x,y,z:x.update(source_domain_checks={})),
     ('NEGATIVE_C_DENOM',lambda x,y,z:x['C_certificate']['D_positive_form'].update(lo='-1')),('C_UPPER_GT1',lambda x,y,z:x['C_certificate']['C_s_certified'].update(hi='2')),
     ('FORGED_ALPHA',lambda x,y,z:x['Alpha'][0].update(lo='0')),('FORGED_HS_K',lambda x,y,z:x['Hs_for_K'].update(lo='1')),
     ('MISSING_R_BRANCH',lambda x,y,z:x['branches'].pop('R')),('WRONG_Q_R',lambda x,y,z:x['branches']['R'].update(q='1/1000000')),
     ('L_NOT_ADMITTED',lambda x,y,z:x['branches']['L'].update(admitted=False)),('UPPER_FACE_NEGATIVE',lambda x,y,z:x['branches']['R']['upper_h_face_terms'][0].update(lo='-1')),
     ('THERMAL_MARGIN_NEGATIVE',lambda x,y,z:x['branches']['L']['thermal']['faces'].update(upper_face_inward_margin='-1')),('THERMAL_BETA_ZERO',lambda x,y,z:x['branches']['R']['thermal']['beta'].update(lo='0')),
     ('WRONG_GUARD_PRIMARY',lambda x,y,z:x.update(guard_primary_sha256='bad')),('WRONG_PROOF_VALIDATION',lambda x,y,z:x.update(proof_validation_sha256='bad')),('WRONG_ACTUAL_START',lambda x,y,z:x['actual_before'].update(count=101)),
     ('NEW_PROOF',lambda x,y,z:x.update(new_math_proof_cells=1)),('PREMATURE_ACCEPTED',lambda x,y,z:y.update(accepted=True)),
     ('RESET',lambda x,y,z:x.update(physical_reset=True)),('FULL_Q',lambda x,y,z:x.update(q_complete=True)),('TAU',lambda x,y,z:x.update(delta_tau_bounds=True)),
     ('HISTORIES',lambda x,y,z:x.update(complete_histories=True)),('PROOF_REPLAY',lambda x,y,z:x.update(proof_reexecuted=True)),('BELOW1030',lambda x,y,z:x['stop'].update(below1030_authorized=True)),
     ('MODEL_PROMOTION',lambda x,y,z:x.update(accepted_model_change=True)),('GUARD_CONTROL',lambda x,y,z:x.update(guard_control_sha256='bad'))]
    answer=[]
    for name,edit in edits:
        x,y,z=deepcopy(r),deepcopy(cp),deepcopy(s)
        try:
            edit(x,y,z);checks=core_validate(x,y,z,False);fail=[v['check'] for v in checks if not v['pass']]
        except (KeyError,ValueError,TypeError,ZeroDivisionError) as e:fail=[type(e).__name__+':'+str(e)]
        answer.append({'name':name,'rejected':bool(fail),'rejecting_checks':fail[:6]})
    return answer

def main():
    s=load_spec()
    if '--preflight' in sys.argv:
        print(json.dumps({'kind':'METADATA_ONLY_PREFLIGHT_NO_SCIENCE','status':'PASS','checks':len(validate_spec(s))}));return
    clock=time.monotonic();output('q048_frec_moving_h_verifier_invocation_v87.json',{'kind':'PRODUCER_FREE_VERIFIER','command':'python3 q048_frec_moving_h_verify_v87.py','execution_fingerprint':s['execution_fingerprint'],'start_utc':datetime.now(timezone.utc).isoformat()})
    r=load(ROOT/RAW);cp=load(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json')
    checks=core_validate(r,cp,s);mm=mutations(r,cp,s)
    good=all(c['pass'] for c in checks) and all(m['rejected'] for m in mm) and len(mm)>=24
    out={'schema':'bubbleverse.q048.frec_moving_h.validation.v87','q':'Q048','target_q':'Q048','status':'PASS' if good else 'FAIL','technical_state':'PASS' if good else 'FAIL','result_sha256':sha(ROOT/RAW),'candidate_checkpoint_sha256':sha(ROOT/'q048_frec_moving_h_candidate_checkpoint_v87.json'),'spec_sha256':sha(ROOT/SPEC),'execution_fingerprint':s['execution_fingerprint'],'validator_sha256':sha(__file__),'checks_total':len(checks),'checks_passed':sum(c['pass'] for c in checks),'checks':checks,'mutations_total':len(mm),'mutations_rejected':sum(m['rejected'] for m in mm),'mutations':mm,'elapsed_seconds':time.monotonic()-clock,'validated_utc':datetime.now(timezone.utc).isoformat(),'producer_imported_or_executed':False,'prior_producer_or_validator_executed':False,'independence_scope':'Separate validation implementation, rational control and serialized certificate/positive-gate checks. Archived accepted proof and input helpers share source lineage; not method independence or physical replication.'}
    output('q048_frec_moving_h_validation_v87.json',out)
    print(json.dumps({'status':out['status'],'checks':str(out['checks_passed'])+'/'+str(out['checks_total']),'mutations':str(out['mutations_rejected'])+'/'+str(out['mutations_total']),'failed':[c['check'] for c in checks if not c['pass']],'unrejected':[m['name'] for m in mm if not m['rejected']]}))
    if not good:raise SystemExit(1)
if __name__=='__main__':main()
