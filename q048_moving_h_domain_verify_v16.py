from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json, hashlib, time, platform
HERE=Path(__file__).resolve().parent
RAW=HERE/'q048_moving_h_domain_result_v16.json'
PARENT=HERE/'q048_frec_moving_h_checkpoint_v15.json'
GUARD=HERE/'q048_guard_local_v_result_v12.json'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def frac(x): return F(str(x))
def ceil18(x): return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x): return F(x.numerator*10**18//x.denominator,10**18)
def ctl_lower(K,eps,ratio,h0):
    x=K*eps*(ratio-1)
    if not (0<=x<1): raise ValueError('control x')
    return eps/((1+eps/h0)/(1-x)-1)

def ivlo(x): return frac(x['lo'])
def ivhi(x): return frac(x['hi'])
def verify(r,p,g):
    checks=[]
    def ck(name,cond): checks.append((name,bool(cond)))
    pr=g['evaluators'][0]['rows'][7]; cr=g['evaluators'][1]['rows'][7]
    ck('identity_q',r['q']==r['target_q']=='Q048')
    ck('task',r['task_id']=='LOCAL-Q048-POST-V15-MOVING-H-DOMAIN-1380-1370-MATH-V1')
    ck('source_identity',r['source_commit']==p['linked_invariant_state']['source_commit'] and r['capture_sha256']==p['linked_invariant_state']['capture_sha256'] and r['question_sha256']==p['linked_invariant_state']['question_sha256'])
    ck('parent_hash',r['parent_v15_checkpoint_sha256']==sha(PARENT))
    ck('guard_hash',r['guard_raw_sha256']==sha(GUARD))
    ck('row_hashes',r['guard_primary_row_sha256']==canon_hash(pr) and r['guard_control_row_sha256']==canon_hash(cr))
    ck('row_domain',pr['a0']=='1/1381' and pr['a1']=='1/1371' and cr['a0']=='1/1381' and cr['a1']=='1/1371')
    ck('row_committed',pr['accepted'] and pr['committed'] and cr['accepted'] and cr['committed'])
    ck('row_margins',frac(pr['G_lower'])>0 and frac(cr['G_lower'])>0 and frac(pr['derivative_lower'])>0 and frac(cr['derivative_lower'])>0)
    ck('scalar_glue',frac(pr['E_input_left'])==frac(p['linked_scalar_endpoint']['E_right']) and frac(pr['Y_left'])==frac(p['linked_scalar_endpoint']['Y_right']) and frac(pr['V_previous'])==frac(p['linked_scalar_endpoint']['Vbar']))
    c=r['comparison']; pinv=p['linked_invariant_state']
    ck('parent_projection_glue',c['parent_endpoint_a']=='1/1381' and frac(c['initial_lower_from_parent_projection'])==frac(pinv['endpoint_lower_projection']))
    ck('no_reset',c['source_state_reset'] is False and c['physical_initial_state_reset'] is False and pinv['physical_state_reset'] is False)
    ck('epsilon',frac(c['epsilon'])==F(1,1000000))
    ck('H_role',c['H_divisor_role']=='POSITIVE_ORDINARY_BACKGROUND_LOWER')
    Kexact=ivhi(r['nH_cm3'])*(ivhi(r['Alpha'][0])+ivhi(r['Alpha'][1]))/ivlo(r['Hs_for_K'])
    K=frac(c['K_upper'])
    ck('K_exact_record',frac(c['K_unrounded_upper'])==Kexact)
    ck('K_outward',K==ceil18(Kexact) and K>=Kexact and K-Kexact<=F(1,10**18))
    ratio=F(1381,1371); h0=frac(c['initial_lower_from_parent_projection']); eps=frac(c['epsilon'])
    ctl=ctl_lower(K,eps,ratio,h0)
    ck('control_log',frac(c['control_log_upper'])==ratio-1)
    ck('control_x',frac(c['control_exp_argument'])==K*eps*(ratio-1) and K*eps*(ratio-1)<1)
    ck('control_lower',frac(c['endpoint_control_lower'])==ctl)
    hmin=frac(c['whole_cell_h_min'])
    ck('hmin_control',hmin==floor18(ctl) and 0<hmin<=ctl)
    ck('primary_not_limiting',ivlo(c['endpoint_primary'])>ctl)
    ck('h_domain',ivlo(c['h_domain'])==hmin and ivhi(c['h_domain'])==F(99999,100000))
    ck('w_domain',ivlo(c['w_domain'])==F(-1,1000000) and ivhi(c['w_domain'])==F(1,100))
    ck('source_domains',all(r['source_domain_checks'].values()))
    ck('positive_atomic',all(ivlo(x)>0 for x in r['Alpha']+r['Alpha_eq']+[r['R2p2s'],r['Saha_HyRec'],r['nH_cm3']]))
    cf=r['C_factor_certificate']
    ck('C_positive',ivlo(cf['C_s_certified'])>0 and ivhi(cf['C_s_certified'])==1 and ivlo(cf['C_p_certified'])>0 and ivhi(cf['C_p_certified'])==1)
    ck('C_le1_proof',ivlo(cf['D_minus_Ns_positive_form'])>0 and ivlo(cf['D_minus_Np_positive_form'])>0 and ivlo(cf['D_positive_form'])>0)
    for lab,q in [('L',F(1,1000000)),('R',F(0))]:
        b=r['branches'][lab]
        ck(lab+'_q',frac(b['q'])==q)
        ck(lab+'_upperH',all(ivlo(x)>0 for x in b['upper_h_face_terms']))
        th=b['thermal']; ck(lab+'_thermal_beta',ivlo(th['beta'])>0); ck(lab+'_thermal_den',ivlo(th['thermal_denominator'])>0)
        ck(lab+'_thermal_faces',frac(th['faces']['lower_face_inward_lower'])>0 and frac(th['faces']['upper_face_inward_margin'])>0 and th['faces']['admitted'] is True)
        ck(lab+'_admitted',b['admitted'] is True)
    ck('status',r['status']=='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL')
    ck('math_only',r['new_mathematical_proof_cells']==1 and r['new_actual_paired_cells']==0 and r['retained_actual_paired_cells']==70)
    ck('frontier_fixed',r['actual_frontiers']['hillipop-ede_n3']==1380)
    ck('no_overclaim',r['q_complete'] is False and r['complete_a1_certificate'] is False and r['final_delta_xe_bounds_computed'] is False and r['final_delta_tau_bounds_computed'] is False and r['physical_falsification'] is False and r['accepted_model_change'] is False and r['native_P6']=='UNRESOLVED')
    return checks

def mutate_and_reject(base,p,g):
    muts=[]
    def t(name,fn):
        x=deepcopy(base); fn(x); ok=all(v for _,v in verify(x,p,g)); muts.append({'name':name,'rejected':not ok})
    t('K_UNDERESTIMATE',lambda x:x['comparison'].__setitem__('K_upper','1'))
    t('RESET_LOWER_TO_HALF',lambda x:x['comparison'].__setitem__('initial_lower_from_parent_projection','1/2'))
    t('ADVANCE_ACTUAL71',lambda x:x.__setitem__('retained_actual_paired_cells',71))
    t('ADVANCE_FRONTIER1370',lambda x:x['actual_frontiers'].__setitem__('hillipop-ede_n3',1370))
    t('FORGE_Q_COMPLETE',lambda x:x.__setitem__('q_complete',True))
    t('SOURCE_RESET',lambda x:x['comparison'].__setitem__('source_state_reset',True))
    t('WRONG_H_ROLE',lambda x:x['comparison'].__setitem__('H_divisor_role','UPPER'))
    t('WRONG_EPS',lambda x:x['comparison'].__setitem__('epsilon','1/1000'))
    t('FORGE_CONTROL',lambda x:x['comparison'].__setitem__('endpoint_control_lower','1/2'))
    t('L_UPPER_FACE_FAIL',lambda x:x['branches']['L']['upper_h_face_terms'][0].__setitem__('lo','-1'))
    t('R_THERMAL_FAIL',lambda x:x['branches']['R']['thermal']['faces'].__setitem__('admitted',False))
    t('OVERCLAIM_ACTUAL_CELL',lambda x:x.__setitem__('new_actual_paired_cells',1))
    return muts

def main():
    start=time.monotonic(); stamp=datetime.now(timezone.utc).isoformat(); r=json.load(open(RAW)); p=json.load(open(PARENT)); g=json.load(open(GUARD))
    checks=verify(r,p,g); muts=mutate_and_reject(r,p,g)
    passed=sum(v for _,v in checks); status='PASS' if passed==len(checks) and all(x['rejected'] for x in muts) else 'FAIL'
    val={'schema_version':'Q048_MOVING_H_DOMAIN_VALIDATION_V16','q':'Q048','result_sha256':sha(RAW),'parent_checkpoint_sha256':sha(PARENT),'guard_raw_sha256':sha(GUARD),'status':status,'technical_state':'PASS' if status=='PASS' else 'FAIL','checks_total':len(checks),'checks_passed':passed,'checks':[{'name':n,'pass':v} for n,v in checks],'mutation_tests_total':len(muts),'mutation_rejections':sum(x['rejected'] for x in muts),'mutations':muts,'independence_note':'Producer-free verifier reads serialized result/parent/guard only. K/control/hmin checks use Python Fraction exact arithmetic; it does not import or execute the producer or Bubbleverse interval modules. Primary exp path is non-limiting; acceptance is independently covered by the exact rational control lower, which is smaller and determines hmin.','validated_utc':stamp,'elapsed_seconds':time.monotonic()-start,'python':platform.python_version()}
    out=HERE/'q048_moving_h_domain_validation_v16.json'; out.write_text(json.dumps(val,indent=2)+'\n')
    print(json.dumps({'status':status,'checks':f'{passed}/{len(checks)}','mutations':f"{val['mutation_rejections']}/{len(muts)}",'result_sha256':val['result_sha256'],'validation_sha256':sha(out)},indent=2))
    if status!='PASS': raise SystemExit(1)
if __name__=='__main__': main()
