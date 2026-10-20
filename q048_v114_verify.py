"""Independent algebraic proof controls; shared physical inputs/interval library.
Does not call the new producer. No new trajectory or physical confirmation.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,argparse,hashlib

SAHA_FACTOR='3.016103031869581e21'

def declared_domain_valid(raw,spec):
    try:
        return raw['task_id']==spec['task_id'] and F(raw['epsilon'])==F(1,1000000) and F(raw['hmax'])==F(99999,100000) and raw['thermal_domain']==['-1/1000000','1/50'] and raw['no_native_trajectory_claim'] is True
    except (KeyError,ValueError,TypeError):return False

def thermal_dual(beta_lo,beta_hi,w_lo,w_hi):
    beta_lo,beta_hi,w_lo,w_hi=map(F,(beta_lo,beta_hi,w_lo,w_hi))
    lower=1-(1+beta_lo)*w_lo;upper=(1+beta_lo)*w_hi-1
    return {'lower':str(lower),'upper':str(upper),'threshold':str(1/(1+beta_lo)) if beta_lo>-1 else None,'admitted':0<beta_lo<=beta_hi and w_lo<0<w_hi<1 and lower>0 and upper>0}

def verify_rational_lower(K,eps,du,h0,hnew):
    K,eps,du,h0,hnew=map(F,(K,eps,du,h0,hnew));x=K*eps*du
    if min(K,h0,hnew)<=0 or min(eps,du)<0 or x>=1:return False
    # Independent simplification of eps/((1+eps/h0)/(1-x)-1).
    limit=h0/(1+K*h0*du) if eps==0 else h0*(1-x)/(1+K*h0*du)
    return hnew<=limit


def semantic_valid(raw,spec,parent,task,g):
    try:
        import copy
        primary=g['evaluators'][0]['rows'][51]
        row_hash=hashlib.sha256(json.dumps(primary,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        return (raw['schema']=='bubbleverse.q048.moving_h.domain.proof.v114'
            and raw['q']==raw['target_q']=='Q048' and raw['task_id']==spec['task_id']==task['task_id']
            and raw['task_fingerprint']==task['task_fingerprint']
            and raw['parent_checkpoint_sha256']==task['parent_authority']['sha256']
            and parent['accepted_actual']==raw['parent_actual']==raw['actual_state_unchanged']=={'count':114,'frontier':940}
            and raw['cell_z']==spec['cell_z']==[940,930] and raw['cell_a']==['1/941','1/931']
            and raw['guard_primary_index']==51 and row_hash==task['guard']['primary_row_sha256']
            and raw['source_state_reset'] is False and primary['source_state_reset'] is False
            and raw['saha_factor_source']==SAHA_FACTOR and F(raw['h0'])==F(parent['connected_lower'])
            and raw['thermal_domain']==spec['thermal_domain']==['-1/1000000','1/50']
            and F(raw['epsilon'])==F(1,1000000) and F(raw['hmax'])==F(99999,100000)
            and raw['new_actual_cells']==raw['new_mathematical_proof_cells']==0
            and raw['no_native_trajectory_claim'] is True and raw['below930_work'] is raw['q_complete'] is raw['historical_record_modified'] is False
            and raw['status']=='CANDIDATE_PROOF' and set(raw['branches'])=={'L','R'}
            and all(F(primary[x])==F(parent['endpoint'][y]) for x,y in [('E_input_left','E'),('Y_left','Y'),('V_previous','Vbar')])
            and primary['a0']==parent['endpoint']['a']=='1/941')
    except (KeyError,IndexError,ValueError,TypeError):return False

def verify(root,spec,raw):
    root=Path(root)
    # Before imports: verify the original input and helper bytes, not their self-reported values.
    for collection in ['input_pins','code_pins']:
        for name,pin in spec[collection].items():
            data=(root/name).read_bytes()
            if len(data)!=pin['bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('FROZEN_PIN:'+name)
    I=root/'inputs';sys.path.insert(0,str(I))
    import q048_full_tube_reuse_v1 as old
    m=old.m;d=old.d;checks={};details={}
    def C(name,x):checks[name]=bool(x)
    iv=lambda x:m.I(F(x['lo']),F(x['hi']))
    parent=json.loads((I/'Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json').read_text());task=json.loads((I/'Q048_V114_NEXT_MATHEMATICS_TASK_V1.json').read_text());g=json.loads((I/'q048_guard_local_v_result_v12.json').read_text());row=g['evaluators'][0]['rows'][51]
    if not semantic_valid(raw,spec,parent,task,g):
        return {'schema':'bubbleverse.q048.moving_h.domain.verification.v114','status':'FAIL','verification_pass':False,'checks_total':1,'checks_passed':0,'checks':{'semantic_gate':False},'new_actual_cells':0}
    cap=json.loads((I/'q048_prefix_config_v1.json').read_text());old.prefix.validate_config(cap);case=cap['cases']['hillipop-ede_n3'];t=old.prefix.parameters(case)
    C('parent_source_correct',parent['status']=='VALIDATED' and parent['correct_saha_fact']==SAHA_FACTOR and raw['parent_checkpoint_sha256']==task['parent_authority']['sha256'])
    C('declared_domain',declared_domain_valid(raw,spec))
    C('source_factor_literal',raw.get('saha_factor_source')==SAHA_FACTOR)
    C('identity',raw['q']==raw['target_q']=='Q048' and raw['cell_z']==[940,930] and raw['cell_a']==['1/941','1/931'] and raw['question_sha256']==cap['question_sha256']==task['question_sha256'])
    C('parent',parent['accepted_actual']==raw['parent_actual']==raw['actual_state_unchanged']=={'count':114,'frontier':940} and F(raw['h0'])==F(parent['connected_lower']))
    C('guard_roles',g['evaluators'][0]['control'] is False and g['evaluators'][1]['control'] is True)
    C('row51',row['index']==raw['guard_primary_index']==51 and [row['z0'],row['z1']]==[940,930])
    C('no_reset_glue',row['source_state_reset'] is False and raw['source_state_reset'] is False and all(F(row[a])==F(parent['endpoint'][b]) for a,b in [('E_input_left','E'),('Y_left','Y'),('V_previous','Vbar')]))
    C('guard_domain',row['accepted'] and row['committed'] and row['whole_cell_qualified'] and row['domain']['admitted'] and all(row['domain']['checks'].values()))
    C('frozen_thermal',raw['thermal_domain']==spec['thermal_domain']==['-1/1000000','1/50'])
    C('no_actual_or_preaccept_proof',raw['new_actual_cells']==raw['new_mathematical_proof_cells']==0 and raw['scientific_state']=='INCONCLUSIVE' and raw['status']=='CANDIDATE_PROOF')
    a=m.I(F(1,941),F(1,931));B,floor,H,Hs=old.background(a,t,F(row['E_safe_left']));HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc'];TR=m.const('8.617343e-5')*t['T0']/a;ratio=m.I(F(49,50),F(1000001,1000000))
    def same(x,y):return F(x['lo'])==y.lo and F(x['hi'])==y.hi
    C('background_recompute',all(same(raw[n],v) for n,v in [('B',B),('floor',floor),('H',H),('Hs',Hs),('HsK',HsK),('TR_eV',TR)]))
    p3=json.loads((I/'q048_p3_scaled_raw_result_v2.json').read_text());fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator']);Tgamma=t['T0']/a
    C('reported_source_enclosures',same(raw['a'],a) and same(raw['ratio'],ratio) and same(raw['fit'],fit) and same(raw['Tgamma_K'],Tgamma) and raw['guard_primary_E_safe_left']==row['E_safe_left'] and raw['source_all'] is True and all(raw['source_checks'].values()))
    C('source_domain',all(z['HyRec_MODEL']==4 for z in case['thermal_starts']) and all(case['background']['thermal_flags'][z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']) and a.hi<F(1,901) and F('.004')<TR.lo<=TR.hi<F('.4') and 1775<Tgamma.lo<=Tgamma.hi<4415 and ratio.lo>F('.1') and fit.lo>0 and HsK.lo>0)
    alpha,rr=old.load_atomic(I/'q048_p3_scaled_transformed_log_tables_v2.json');atoms=old.local_atomic(alpha,rr,TR,ratio)
    A=list(map(old.fromk,atoms['Alpha']));Ae=list(map(old.fromk,atoms['Alpha_eq']));RR=old.fromk(atoms['R2p2s']);n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const(SAHA_FACTOR)*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const(SAHA_FACTOR)*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    C('atomic_recompute',all(same(raw['A'][i],A[i]) and same(raw['Ae'][i],Ae[i]) and same(raw['Beta'][i],Beta[i]) for i in range(2)) and same(raw['R2p2s'],RR) and same(raw['Saha'],saha) and same(raw['n'],n))
    C('atomic_positive',raw['atomic_positive'] is True and min(v.lo for v in A+Ae+[RR,n,saha]+Beta)>0)
    exact=n.hi*(A[0].hi+A[1].hi)/HsK.lo;K=F(raw['K_upper']);target=F(-((-exact.numerator*10**18)//exact.denominator),10**18)
    C('fresh_K_exact_outward',K==target and K>=exact and F(raw['K_unrounded'])==exact)
    eps=F(1,1000000);h0=F(parent['connected_lower']);hmin=F(raw['hmin']);hmax=F(99999,100000);h=m.I(hmin,hmax);du_upper=a.hi/a.lo-1
    logarithm=old.k.log_i(old.k.I(a.hi/a.lo));du=m.I(logarithm.lo,logarithm.hi);primary_endpoint=eps/((1+eps/h0)*m.exp_i(K*eps*du)-1)
    C('primary_endpoint_recomputed',same(raw['du'],du) and same(raw['endpoint_primary'],primary_endpoint) and F(raw['du_rational_upper'])==du_upper)
    C('positive_connected_lower_rational_dual',verify_rational_lower(K,eps,du_upper,h0,hmin))
    simple=h0*(1-K*eps*du_upper)/(1+K*h0*du_upper)
    C('rational_control_exact',simple==F(raw['endpoint_control']))
    C('outward_lower_18',hmin==F((min(F(raw['endpoint_primary']['lo']),simple)*10**18).__floor__(),10**18))
    details['comparison']={'inequality':'h_u >= -K*h*(h+epsilon), K>0; exp(x)<=1/(1-x), log(r)<=r-1 for r>1','x':str(K*eps*du_upper),'independent_rational_lower':str(simple),'hmin':str(hmin),'scope':'Conditional moving lower bound, not a native trajectory sample'}
    L0=m.const('8.2206');P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit;gs=Beta[0]+3*RR+L0;gp=Beta[1]+RR+P
    cf={'L0':L0,'P':P,'gs':gs,'gp':gp,'D':(Beta[0]+L0)*(Beta[1]+RR+P)+3*RR*(Beta[1]+P),'Ns':L0*gp+3*RR*P,'Np':P*gs+RR*L0,'ds':Beta[0]*gp+3*RR*Beta[1],'dp':Beta[1]*gs+RR*Beta[0]}
    C('C_factors_recomputed_positive',raw['c_positive'] is True and all(same(raw['C_factors'][k],v) and v.lo>0 for k,v in cf.items()))
    for label,q in [('L',eps),('R',F(0))]:
        b=raw['branches'][label];terms=[A[i]*m.I(hmax)*(m.I(hmax)+q)-Ae[i]*saha*(1-m.I(hmax)) for i in range(2)]
        C(label+'_H_faces',F(b['q'])==q and all(same(b['upper_h_face_terms'][i],terms[i]) and terms[i].lo>0 for i in range(2)))
        denominator=1+t['fHe']+h+q
        beta=8*m.C['sigma']*(t['gamma']/a**4)*m.C['rhoJ']/(3*m.C['me']*m.C['c']*Hs)*(h+q)/denominator
        C(label+'_thermal_primitive',same(b['thermal']['beta'],beta) and same(b['thermal']['thermal_denominator'],denominator) and denominator.lo>0)
        dual=thermal_dual(beta.lo,beta.hi,F(-1,1000000),F(1,50));details[label]=dual
        margins={'upper_h_0':terms[0].lo,'upper_h_1':terms[1].lo,'thermal_denominator':denominator.lo,'beta':beta.lo,'lower_face_inward_lower':F(dual['lower']),'upper_face_inward_margin':F(dual['upper'])}
        C(label+'_reported_margins',b['admitted'] is True and b['thermal']['faces']['admitted'] is True and all(F(b['signed_margins'][k])==v and v>0 for k,v in margins.items()))
        C(label+'_analytic_thermal_faces',dual['admitted'] and F(b['thermal']['faces']['upper_face_inward_margin'])==F(dual['upper']) and F(b['thermal']['faces']['lower_face_inward_lower'])==F(dual['lower']))
    return {'schema':'bubbleverse.q048.moving_h.domain.verification.v114','status':'PASS' if all(checks.values()) else 'FAIL','verification_pass':all(checks.values()),'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,'independent_algebraic_controls':details,'independence_scope':'Independent rational comparison bound and thermal-face algebra; source/background/atomic/C-factor enclosures separately recomputed with shared pinned helper implementation and exact physical inputs. No independent native or empirical evidence.','authoritative_actual_state_unchanged':parent['accepted_actual'],'new_actual_cells':0,'q_complete':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--raw',required=True);p.add_argument('--output',required=True);args=p.parse_args();sp=Path(args.spec).resolve();spec=json.loads(sp.read_text());raw=json.loads(Path(args.raw).read_text())
    result=verify(sp.parent,spec,raw);result['raw_sha256']=hashlib.sha256(Path(args.raw).read_bytes()).hexdigest();
    with Path(args.output).open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks_total':result['checks_total'],'checks_passed':result['checks_passed']}))
