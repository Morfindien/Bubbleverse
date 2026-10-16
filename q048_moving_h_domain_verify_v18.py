"""Producer-free verification for Q048 V18 moving-h cell 1370->1360.
Does not import or execute q048_moving_h_domain_v18.py. Riccati/log/exp,
background, C-factor and thermal checks use separate Fraction algebra. The frozen
P3 source helper is used only to cross-check serialized atomic interpolation.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from copy import deepcopy
import json,time,hashlib,sys
ROOT=Path(__file__).resolve().parent; INPUTS=ROOT/'inputs'; sys.path.insert(0,str(INPUTS))
import q048_full_tube_reuse_v1 as source_old

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads((ROOT/p).read_text())
def iv(d): return F(d['lo']),F(d['hi'])
def add(a,b): return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    x=[u*v for u in a for v in b]; return min(x),max(x)
def div(a,b):
    assert b[0]>0; return mul(a,(1/b[1],1/b[0]))
def power(a,n):
    out=(F(1),F(1))
    for _ in range(n): out=mul(out,a)
    return out
def cn(s):
    a,b=F(s),F.from_float(float(s)); return min(a,b),max(a,b)
def pt(s):
    a=F.from_float(float.fromhex(s)); return a,a
def scale(a,x): return mul(a,(F(x),F(x)))
def encloses(d,x):
    a=iv(d); return a[0]<=x[0]<=x[1]<=a[1]
def sqrt_b(x):
    den=10**160; n=isqrt(x.numerator*den*den//x.denominator); return F(n,den),F(n+1,den)
def log_b(r):
    assert r>=1
    t=(r-1)/(r+1); N=100
    low=2*sum((t**(2*j+1)/(2*j+1) for j in range(N)),F(0))
    tail=2*t**(2*N+1)/((2*N+1)*(1-t*t)); return low,low+tail
def exp_b(x):
    assert 0<=x<1
    N=60; term=F(1); low=term
    for j in range(1,N+1): term*=x/j; low+=term
    tail=term*x/(N+1)/(1-x/(N+2)); return low,low+tail
def background(bg,a):
    f=bg['fields']; H=pt(f['H0'])[0]
    b=H*H*((pt(f['Omega0_g'])[0]+pt(f['Omega0_ur'])[0])/a**4+(pt(f['Omega0_b'])[0]+pt(f['Omega0_cdm'])[0])/a**3+pt(f['Omega0_lambda'])[0]); out=(b,b)
    for nu in bg['neutrinos']:
        mass=pt(nu['fields']['M_ncdm'])[0]; fac=pt(nu['fields']['factor_ncdm'])[0]
        for q,w in zip(nu['q_ncdm_bg'],nu['w_ncdm_bg']):
            q,w=pt(q)[0],pt(w)[0]; out=add(out,scale(sqrt_b(q*q+(a*mass)**2),fac*q*q*w/a**4))
    return out
def row_sha(row): return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def symbolic_C_identities():
    def plus(*ps):
        d={}
        for p in ps:
            for mon,c in p.items(): d[mon]=d.get(mon,F(0))+c
        return {k:v for k,v in d.items() if v}
    def times(a,b):
        d={}
        for x,u in a.items():
            for y,v in b.items():
                key=tuple(i+j for i,j in zip(x,y)); d[key]=d.get(key,F(0))+u*v
        return d
    def sc(a,n): return {k:v*n for k,v in a.items()}
    b0,b1,R,L,P=[{tuple(1 if j==i else 0 for j in range(5)):F(1)} for i in range(5)]
    gs=plus(b0,sc(R,3),L); gp=plus(b1,R,P)
    D=plus(times(gs,gp),sc(times(R,R),-3)); Ns=plus(times(L,gp),sc(times(R,P),3)); Np=plus(times(P,gs),times(R,L))
    positiveD=plus(times(plus(b0,L),plus(b1,R,P)),sc(times(R,plus(b1,P)),3)); ds=plus(times(b0,gp),sc(times(R,b1),3)); dp=plus(times(b1,gs),times(R,b0))
    return D==positiveD and plus(D,sc(Ns,-1))==ds and plus(D,sc(Np,-1))==dp and all(v>0 for p in [positiveD,Ns,Np,ds,dp] for v in p.values())

def validate(r,s,cp,atomic_ref):
    checks=[]
    def test(k,x): checks.append({'id':k,'pass':bool(x)})
    p=load('inputs/q048_frec_moving_h_result_v17.json'); pcp=load('inputs/q048_frec_moving_h_accepted_checkpoint_v17.json'); pv=load('inputs/q048_frec_moving_h_validation_v17.json'); post=load('inputs/q048_frec_moving_h_postaccept_validation_v17.json')
    v16=load('inputs/q048_moving_h_domain_result_v16.json'); v16v=load('inputs/q048_moving_h_domain_validation_v16.json'); v16cp=load('inputs/q048_moving_h_domain_accepted_checkpoint_v16.json')
    v14=load('inputs/q048_moving_h_result_v14.json'); v14v=load('inputs/q048_moving_h_validation_v14.json')
    g=load('inputs/q048_guard_local_v_result_v12.json'); gv=load('inputs/q048_guard_local_v_validation_v12.json')
    task=load('inputs/Q048_FREC_MOVING_H_V17_NEXT_MATHEMATICS_TASK_V1.json')
    cap=load('inputs/sources/q048_prefix_config_v1.json'); case=cap['cases']['hillipop-ede_n3']
    test('Q_task',r['q']==r['target_q']=='Q048' and r['task_id']==s['task_id']==task['task_id'] and r['task_fingerprint']==s['task_fingerprint']==task['task_fingerprint'] and r['result_id']==s['result_id'])
    test('source_identity',all(r[k]==s[k]==task[k]==p[k]==v16[k]==v14[k]==g[k] for k in ['source_commit','capture_sha256','question_sha256']) and hashlib.sha256(r['exact_question'].encode()).hexdigest()==r['question_sha256'])
    test('spec_contract',r['spec_sha256']==sha(ROOT/'q048_moving_h_domain_spec_v18.json') and r['proof_contract_sha256']==sha(ROOT/'Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V18.md') and r['prompt_sha256']==sha(INPUTS/'Bubbleverse_Matematikmotor_2.1.0.md') and r['task_contract_sha256']==sha(INPUTS/'Q048_FREC_MOVING_H_V17_NEXT_MATHEMATICS_TASK_V1.json'))
    test('v17_receipt',r['parent_v17_raw_sha256']==sha(INPUTS/'q048_frec_moving_h_result_v17.json')==pv['result_sha256']==pcp['source_result_sha256'] and r['parent_v17_checkpoint_sha256']==sha(INPUTS/'q048_frec_moving_h_accepted_checkpoint_v17.json')==post['accepted_checkpoint_sha256'] and r['parent_v17_validation_sha256']==sha(INPUTS/'q048_frec_moving_h_validation_v17.json')==pcp['validation_sha256'] and r['parent_v17_postaccept_sha256']==sha(INPUTS/'q048_frec_moving_h_postaccept_validation_v17.json') and pv['status']=='PASS' and post['status']=='PASS')
    test('v16_receipt',r['prior_v16_raw_sha256']==sha(INPUTS/'q048_moving_h_domain_result_v16.json')==v16v['result_sha256']==v16cp['source_result_sha256'] and r['prior_v16_validation_sha256']==sha(INPUTS/'q048_moving_h_domain_validation_v16.json')==v16cp['validation_sha256'] and r['prior_v16_accepted_checkpoint_sha256']==sha(INPUTS/'q048_moving_h_domain_accepted_checkpoint_v16.json') and v16v['status']=='PASS' and v16cp['technical_state']=='PASS')
    test('v14_receipt',r['parent_v14_math_raw_sha256']==sha(INPUTS/'q048_moving_h_result_v14.json')==v14v['result_sha256'] and r['parent_v14_math_validation_sha256']==sha(INPUTS/'q048_moving_h_validation_v14.json') and r['parent_v14_contract_sha256']==sha(INPUTS/'Q048_MOVING_H_PROOF_CONTRACT_V14.md') and v14v['status']=='PASS')
    test('guard_receipt',r['guard_raw_sha256']==sha(INPUTS/'q048_guard_local_v_result_v12.json')==gv['result_sha256'] and r['guard_validation_sha256']==sha(INPUTS/'q048_guard_local_v_validation_v12.json') and gv['technical_state']=='PASS')
    cert=g['evaluators'][0]['rows'][8]; ctrl=g['evaluators'][1]['rows'][8]
    test('exact_committed_row8',r['guard_primary']==cert and cert['accepted'] and cert['committed'] and ctrl['accepted'] and ctrl['committed'] and r['guard_primary_row_sha256']==row_sha(cert)==task['guard_binding']['primary_row_sha256'] and r['guard_control_row_sha256']==row_sha(ctrl)==task['guard_binding']['control_row_sha256'] and F(cert['G_lower'])>0 and F(ctrl['G_lower'])>0 and F(cert['derivative_lower'])>0 and F(ctrl['derivative_lower'])>0)
    a0,a1=iv(r['a']); test('new_cell',r['z']==[1370,1360] and a0==F(1,1371)==F(cert['a0']) and a1==F(1,1361)==F(cert['a1']))
    linked=pcp['linked_scalar_endpoint']; test('scalar_link',F(cert['a0'])==F(linked['a1']) and F(cert['E_input_left'])==F(linked['E_right']) and F(cert['Y_left'])==F(linked['Y_right']) and F(cert['V_previous'])==F(linked['Vbar']) and r['actual_scalar_endpoint']==linked)
    test('E_safe',F(r['E_safe_left'])==F(cert['E_safe_left']) and F(r['E_safe_left'])<F(cert['E_input_left']))
    inv=pcp['linked_invariant_state']; co=r['comparison']; h0=F(co['initial_lower']); eps=F(co['epsilon']); K=F(co['K_upper']); hmin=F(co['whole_cell_h_min']); hhi=F(99999,100000)
    test('comparison_gluing',co['method']=='COMMON_EPS_SOURCE_SIGN_RICCATI_GLUED_V18' and co['orientation']=='ell_u <= F_q' and co['parent_method']==inv['kind'] and F(co['parent_endpoint_a'])==a0 and F(co['parent_endpoint_lower_projection'])==h0==F(inv['endpoint_lower_projection']) and F(co['initial_a'])==a0 and co['gluing_verified'] and co['comparison_glued_to_parent'] and co['physical_state_reset'] is False and co['source_state_reset'] is False and co['initial_lower_role']=='INHERITED_CERTIFIED_AUXILIARY_PROJECTION_NOT_PHYSICAL_RESET')
    test('previous_hmin_glue',h0==F(v16cp['comparison']['whole_cell_h_min'])!=F(1,2) and co['historical_original_ell0']=='1/2 at a=1/1391 only')
    test('actual_parent71',pcp['total_accepted_cells_in_chain']==71 and pcp['frontiers']['hillipop-ede_n3']==s['actual_frontier_must_remain'] and pcp['total_accepted_cells_in_chain']==s['actual_count_must_remain'] and r['actual_frontiers']==pcp['frontiers'] and r['retained_actual_paired_cells']==71 and r['new_actual_paired_cells']==0)
    flags=case['background']['thermal_flags']; test('source_flags',r['source_flags']==flags and all(flags[x]==0 for x in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']) and all(x['HyRec_MODEL']==4 for x in case['thermal_starts']))
    test('new_h_domain',iv(co['h_domain'])==(hmin,hhi) and 0<hmin<h0 and iv(co['w_domain'])==(F(-1,1000000),F(1,100)))
    # Independent background / units.
    bg=case['background']; fields=bg['fields']; constants=case['thermal_starts'][0]['constants']; Blo,Bhi=iv(r['B0'])
    test('bg_enclosure',0<Blo<=background(bg,a1)[0] and Bhi>=background(bg,a0)[1])
    cl,ch=cn('2.99792458e8'); ml,mh=cn('3.085677581282e22'); Kl,Kh=iv(r['Hs_for_K'])
    test('K_H_lower',0<Kl and (Kl/(cl/mh))**2<=Blo)
    Elo=F(r['E_safe_left']); fl,fh=iv(r['floor']); Hlo,Hhi=iv(r['H_Mpc_inverse']); Hslo,Hshi=iv(r['Hs_per_second'])
    test('whole_H_upper_lower',fl>=0 and Hhi**2>=Bhi+(Elo+fh)/3 and 0<Hlo**2<=Blo+fl/3 and 0<Hslo<=Hlo*cl/mh and Hshi>=Hhi*ch/ml)
    nlo,nhi=iv(r['nH_cm3']); n0=pt(constants['nH0_SI'])[0]
    test('nH_units',0<nlo<=n0/a1**3/F(10**6) and nhi>=n0/a0**3/F(10**6))
    TR=iv(r['TR_eV']); Tg=iv(r['Tgamma_K']); ratio=iv(r['TM_over_TR']); fit=iv(r['fit_denominator'])
    test('source_domain',all(r['source_domain_checks'].values()) and F('.004')<TR[0]<=TR[1]<F('.4') and Tg[0]>1775 and Tg[1]<4415 and ratio==(F(99,100),F(1000001,1000000)) and fit[0]>0)
    A=list(map(iv,r['Alpha'])); Ae=list(map(iv,r['Alpha_eq'])); S=iv(r['Saha_HyRec']); test('positive_atomic',min(x[0] for x in A+Ae+[iv(r['R2p2s']),S])>0)
    A2,Ae2,R2=atomic_ref; test('p3_source_recompute',all(A[i]==A2[i] and Ae[i]==Ae2[i] for i in range(2)) and iv(r['R2p2s'])==R2)
    exact=nhi*(A[0][1]+A[1][1])/Kl
    test('fresh_K_bound',F(co['K_unrounded_upper'])==exact and K>=exact and 0<=K-exact<F(1,10**18) and co['K_requalified_on_new_domain'] and co['K_reused_without_proof'] is False and K!=F(co['old_cell_K']))
    du=log_b(a1/a0); test('independent_log',encloses(co['du'],du))
    xlo,xhi=K*eps*du[0],K*eps*du[1]; el=exp_b(xlo)[0]; eh=exp_b(xhi)[1]
    primary=(eps/((1+eps/h0)*eh-1),eps/((1+eps/h0)*el-1)); test('independent_Riccati_endpoint',encloses(co['endpoint_primary'],primary))
    x=K*eps*(a1/a0-1); control=eps/((1+eps/h0)/(1-x)-1)
    test('rational_control',x<1 and F(co['control_log_upper'])==a1/a0-1 and F(co['control_exp_argument'])==x and F(co['endpoint_control_lower'])==control)
    target=min(F(co['endpoint_primary']['lo']),control); test('whole_cell_min',0<hmin<=target and target-hmin<F(1,10**18))
    test('q_ordering',co['q_ordering']=='q<=epsilon implies -K*h*(h+epsilon)<=-K*h*(h+q)')
    test('symbolic_C_identities',symbolic_C_identities()); cc=r['C_factor_certificate']
    test('C_positive_domain',all(iv(cc[x])[0]>0 for x in ['R','L','P','D_positive_form','Ns','Np','gamma_s','gamma_p']) and all(iv(x)[0]>0 for x in cc['Beta']) and all(0<iv(cc[x])[0]<=iv(cc[x])[1]==1 for x in ['C_s_certified','C_p_certified']))
    P=div(div(scale(iv(r['Hs_per_second']),F('4.662899067555897e15')),iv(r['nH_cm3'])),(1-hhi,1-hmin)); P=div(P,fit); test('positive_RLya_source',encloses(cc['P'],P))
    outcomes=[]; gamma=scale(mul(pt(fields['Omega0_g']),power(pt(fields['H0']),2)),1); gamma=div(gamma,power((a0,a1),4)); fhe=pt(constants['fHe_CLASS']); denbase=add((F(1),F(1)),fhe)
    for label,q in [('L',eps),('R',F(0))]:
        br=r['branches'][label]; test(label+':q',F(br['q'])==q and br['lower_face_comparison']=='ell_u=-K_new*ell*(ell+epsilon) <= -K_new*ell*(ell+q) <= F_q')
        goodhigh=True
        for i in range(2):
            pos=scale(A[i],hhi*(hhi+q)); neg=scale(mul(Ae[i],S),1-hhi); term=(pos[0]-neg[1],pos[1]-neg[0])
            test(label+':high'+str(i),encloses(br['upper_h_face_terms'][i],term)); goodhigh &= F(br['upper_h_face_terms'][i]['lo'])>0
        hq=(hmin+q,hhi+q); den=add(denbase,hq); factor=scale(mul(cn('6.6524616e-29'),cn('0.0151730087')),8); top=mul(factor,gamma); bottom=scale(mul(mul(cn('9.10938215e-31'),cn('2.99792458e8')),iv(r['Hs_per_second'])),3); beta=mul(div(top,bottom),div(hq,den)); th=br['thermal']
        test(label+':thermal_beta',encloses(th['beta'],beta)); test(label+':thermal_den',den[0]>0 and encloses(th['thermal_denominator'],den))
        bl=F(th['beta']['lo']); low=1+(1+bl)/10**6; high=(1+bl)/100-1; faces=th['faces']
        test(label+':thermal_faces',F(faces['lower_face_inward_lower'])==low and F(faces['upper_face_inward_margin'])==high and faces['admitted']==(low>0 and high>0))
        admitted=goodhigh and bl>0 and low>0 and high>0; test(label+':admission',br['admitted']==admitted); outcomes.append(admitted)
    success=len(outcomes)==2 and all(outcomes)
    test('result_status',(r['status']=='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL')==success and r['new_mathematical_proof_cells']==(1 if success else 0))
    test('checkpoint_math_only',cp['source_result_sha256']==sha(ROOT/'q048_moving_h_domain_result_v18.json') and cp['parent_actual_checkpoint_sha256']==sha(INPUTS/'q048_frec_moving_h_accepted_checkpoint_v17.json') and cp['actual_frontiers']==r['actual_frontiers']==pcp['frontiers'] and cp['actual_scalar_endpoint']==pcp['linked_scalar_endpoint'] and cp['total_actual_paired_cells']==71 and cp['new_actual_paired_cells']==0 and cp['new_mathematical_proof_cells']==r['new_mathematical_proof_cells'] and F(cp['comparison_start_lower'])==h0 and F(cp['comparison_endpoint_lower'])==hmin and F(cp['comparison_K_upper'])==K and cp['physical_state_reset'] is False and cp['technical_state']=='PENDING_VALIDATION')
    test('no_overclaim',not any(r[k] for k in ['q_complete','complete_a1_certificate','physical_falsification','accepted_model_change','final_delta_xe_bounds_computed','final_delta_tau_bounds_computed','prior_science_or_prior_validator_reexecuted']) and r['native_P6']=='UNRESOLVED' and r['technical_state']=='PENDING_VALIDATION' and r['scientific_state']=='INCONCLUSIVE')
    test('bounded_execution',r['execution']['elapsed_seconds']<300 and r['execution']['native_or_paid_runs']==0 and r['return_route']=='RESULT INGESTION & ROUTING ENGINE2.1.0')
    return checks

def fast_contract(x,baseline,pcp,cert):
    try:
        co=x['comparison']; eps=F(co['epsilon']); K=F(co['K_upper']); hmin=F(co['whole_cell_h_min'])
        return all([
            x['q']==x['target_q']=='Q048',x['task_id']==baseline['task_id'],x['source_commit']==baseline['source_commit'],x['capture_sha256']==baseline['capture_sha256'],
            x['z']==[1370,1360],iv(x['a'])==(F(1,1371),F(1,1361)),x['guard_primary']==cert and cert['committed'] is True,
            co['orientation']=='ell_u <= F_q',co['comparison_glued_to_parent'] is True,co['physical_state_reset'] is False,co['source_state_reset'] is False,co['K_reused_without_proof'] is False,
            F(co['initial_a'])==F(pcp['linked_invariant_state']['endpoint_a']),F(co['initial_lower'])==F(pcp['linked_invariant_state']['endpoint_lower_projection'])!=F(1,2),
            K>=F(co['K_unrounded_upper'])>0,0<hmin<=F(co['endpoint_primary']['lo']),hmin<=F(co['endpoint_control_lower']),
            F(x['branches']['L']['q'])==eps,F(x['branches']['R']['q'])==0,x['branches']['L']['admitted'],x['branches']['R']['admitted'],F(x['branches']['L']['thermal']['faces']['upper_face_inward_margin'])>0,F(x['branches']['R']['thermal']['faces']['upper_face_inward_margin'])>0,
            x['retained_actual_paired_cells']==71,x['new_actual_paired_cells']==0,x['actual_frontiers']['hillipop-ede_n3']==1370,x['actual_scalar_endpoint']==pcp['linked_scalar_endpoint'],
            x['status']=='PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL',x['new_mathematical_proof_cells']==1,not x['complete_a1_certificate'],not x['physical_falsification'],not x['accepted_model_change'],x['native_P6']=='UNRESOLVED',x['technical_state']=='PENDING_VALIDATION'
        ])
    except Exception: return False

def main():
    clock=time.monotonic(); r=load('q048_moving_h_domain_result_v18.json'); cp=load('q048_moving_h_domain_candidate_checkpoint_v18.json'); s=load('q048_moving_h_domain_spec_v18.json')
    TR0=iv(r['TR_eV']); ratio0=iv(r['TM_over_TR']); alpha,rr=source_old.load_atomic(INPUTS/'sources/q048_p3_scaled_transformed_log_tables_v2.json'); atom=source_old.local_atomic(alpha,rr,source_old.m.I(*TR0),source_old.m.I(*ratio0)); atomic_ref=([ (x.lo,x.hi) for x in map(source_old.fromk,atom['Alpha']) ],[ (x.lo,x.hi) for x in map(source_old.fromk,atom['Alpha_eq']) ],(source_old.fromk(atom['R2p2s']).lo,source_old.fromk(atom['R2p2s']).hi))
    checks=validate(r,s,cp,atomic_ref)
    for path,pin in s['inputs'].items():
        p=ROOT/path; checks.append({'id':'pin:'+path,'pass':p.is_file() and p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256']})
    pcp=load('inputs/q048_frec_moving_h_accepted_checkpoint_v17.json'); cert=load('inputs/q048_guard_local_v_result_v12.json')['evaluators'][0]['rows'][8]
    edits=[
      ('reset_to_half',lambda x:x['comparison'].update(initial_lower='1/2')),('wrong_gluing_a',lambda x:x['comparison'].update(initial_a='1/1370')),('false_physical_reset',lambda x:x['comparison'].update(physical_state_reset=True)),('reuse_old_K',lambda x:x['comparison'].update(K_reused_without_proof=True)),('K_underestimate',lambda x:x['comparison'].update(K_upper='1')),('wrong_direction',lambda x:x['comparison'].update(orientation='ell_u >= F_q')),('wrong_q_L',lambda x:x['branches']['L'].update(q='0')),('wrong_source',lambda x:x.update(source_commit='x')),('wrong_capture',lambda x:x.update(capture_sha256='x')),('wrong_guard_row',lambda x:x['guard_primary'].update(a0='1/1381')),('uncommitted_guard',lambda x:x['guard_primary'].update(committed=False)),('false_lower_bound',lambda x:x['comparison'].update(whole_cell_h_min='1/2')),('thermal_face_forged',lambda x:x['branches']['L']['thermal']['faces'].update(upper_face_inward_margin='-1')),('actual_count72',lambda x:x.update(retained_actual_paired_cells=72)),('frontier_advanced',lambda x:x['actual_frontiers'].update(**{'hillipop-ede_n3':1360})),('consumer_claim',lambda x:x.update(new_actual_paired_cells=1)),('full_history_claim',lambda x:x.update(complete_a1_certificate=True)),('physical_falsification_claim',lambda x:x.update(physical_falsification=True)),('accepted_model_claim',lambda x:x.update(accepted_model_change=True)),('promoted_before_validation',lambda x:x.update(technical_state='PASS'))]
    muts=[]
    for name,fn in edits:
        x=deepcopy(r); fn(x); muts.append({'id':name,'rejected':not fast_contract(x,r,pcp,cert)})
    good=all(c['pass'] for c in checks) and all(m['rejected'] for m in muts)
    out={'schema_version':'Q048_MOVING_H_DOMAIN_VALIDATION_V18','q':'Q048','status':'PASS' if good else 'FAIL','technical_state':'PASS' if good else 'FAIL','result_sha256':sha(ROOT/'q048_moving_h_domain_result_v18.json'),'candidate_checkpoint_sha256':sha(ROOT/'q048_moving_h_domain_candidate_checkpoint_v18.json'),'validator_sha256':sha(Path(__file__)),'checks_total':len(checks),'checks_passed':sum(c['pass'] for c in checks),'checks':checks,'mutations_total':len(muts),'mutations_rejected':sum(m['rejected'] for m in muts),'mutations':muts,'elapsed_seconds':time.monotonic()-clock,'prior_science_or_prior_validator_reexecuted':False,'independence_scope':__doc__}
    (ROOT/'q048_moving_h_domain_validation_v18.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','checks_total','checks_passed','mutations_total','mutations_rejected','elapsed_seconds']},indent=2))
    if not good:
        print('FAILED CHECKS',[c for c in checks if not c['pass']]); print('FAILED MUTATIONS',[m for m in muts if not m['rejected']]); raise SystemExit(1)
if __name__=='__main__': main()
