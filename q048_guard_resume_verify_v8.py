"""Producer-free validator for Q048 Guard Resume V8.

Does not import q048_guard_resume_v8.py. Rebuilds identity/linkage, background lowers,
comparison recurrences and whole-cell guards with separate arithmetic.
"""
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_CEILING
from pathlib import Path
import copy, hashlib, json, math, platform, time

ROOT=Path(__file__).resolve().parent
INP=ROOT/'inputs'
D=10**18
getcontext().prec=160

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hf(s): return F.from_float(float.fromhex(s))
def down(x,den=D): return F((x.numerator*den)//x.denominator,den)
def up(x,den=D): return F(-((-x.numerator*den)//x.denominator),den)
def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)
def ceil_dec18(x):
    q=(x*Decimal(D)).to_integral_value(rounding=ROUND_CEILING)
    return F(int(q),D)
def sqrt_lower(x,steps=140):
    assert x>=0
    if x==0:return F(0)
    lo,hi=F(0),max(F(1),x+1)
    for _ in range(steps):
        m=(lo+hi)/2
        if m*m<=x: lo=m
        else: hi=m
    assert lo*lo<=x
    return lo

def bg(case,states):
    e=states[case]['effective_background_hex']; f=e['fields']; n=e['neutrinos'][0]
    return {'H0':hf(f['H0']),'ob':hf(f['Omega0_b']),'oc':hf(f['Omega0_cdm']),
            'og':hf(f['Omega0_g']),'our':hf(f['Omega0_ur']),'ol':hf(f['Omega0_lambda']),
            'M':hf(n['fields']['M_ncdm']),'factor':hf(n['fields']['factor_ncdm']),
            'q':[hf(x) for x in n['q_ncdm_bg']], 'w':[hf(x) for x in n['w_ncdm_bg']]}

def primary_B0(a,b):
    H2=b['H0']**2
    v=H2*(b['og']+b['our'])/a**4+H2*(b['ob']+b['oc'])/a**3+H2*b['ol']
    v+=b['factor']/a**4*sum(q**3*w for q,w in zip(b['q'],b['w']))
    return down(v)

def control_B0(a,b):
    assert b['ol']==0 and b['factor']>0 and b['M']>=0
    rho=sum(q*q*sqrt_lower(q*q+(a*b['M'])**2)*w for q,w in zip(b['q'],b['w']))
    return down(b['H0']**2*((b['og']+b['our'])/a**4+(b['ob']+b['oc'])/a**3)+b['factor']/a**4*rho)

def independent_primary_decay(left,right,kappa):
    # high-precision Decimal direct ln/exp, upward rounded to 1e-18
    x=dec(kappa)*(dec(right).ln()-dec(left).ln())
    d=(-x).exp()
    return d,ceil_dec18(d)

def validate_core(r,cfg):
    checks=[]
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks.append(name)

    v6=json.loads((INP/'q048_guard_resume_result_v6.json').read_text())
    v6val=json.loads((INP/'q048_guard_resume_validation_v6.json').read_text())
    v7=json.loads((INP/'q048_frec_resume_result_v7.json').read_text())
    v7ck=json.loads((INP/'q048_frec_resume_checkpoint_v7.json').read_text())
    v7val=json.loads((INP/'q048_frec_resume_validation_v7.json').read_text())
    states=json.loads((INP/'state_objects_extracted.json').read_text())

    ck('q_identity',r['q']==r['target_q']==cfg['q']==cfg['target_q']=='Q048')
    ck('result_identity',r['result_id']==cfg['result_id'] and r['task_id']==cfg['task_id'])
    ck('prompt_identity',r['prompt_id']=='BUBBLEVERSE.MATHEMATICS' and r['prompt_version']=='2.1.0')
    ck('question_identity',r['question_sha256']==cfg['question_sha256']==v6['question_sha256']==v7['question_sha256'])
    ck('source_capture',r['source_commit']==v7['source_commit']==cfg['source_commit'] and r['capture_sha256']==v7['capture_sha256']==cfg['capture_sha256'])
    ck('config_hash',r['config_sha256']==digest(ROOT/'q048_guard_resume_config_v8.json'))
    ck('contract_hash',r['contract_sha256']==digest(ROOT/'Q048_GUARD_RESUME_TEST_CONTRACT_V8.md'))
    for f,h in cfg['input_hashes'].items(): ck('pin:'+f,digest(INP/f)==h)
    ck('v6_validation',v6['status']=='PASS_GUARD_COMPONENT' and v6val['technical_state']=='PASS' and v6val['result_sha256']==digest(INP/'q048_guard_resume_result_v6.json'))
    ck('v7_validation',v7val['technical_state']=='PASS' and v7ck['source_result_sha256']==digest(INP/'q048_frec_resume_result_v7.json'))
    ck('parent_math_hash',r['parent_math_raw_sha256']==digest(INP/'q048_guard_resume_result_v6.json'))
    ck('parent_builder_hash',r['parent_builder_raw_sha256']==digest(INP/'q048_frec_resume_result_v7.json'))
    ck('parent_ids',r['parent_math_result_id']==v6['result_id'] and r['parent_builder_result_id']==v7['result_id'])
    ck('v7_frontier',v7['final_frontiers']['hillipop-ede_n3']==1490 and v7ck['total_accepted_cells_in_chain']==59)
    ck('v7_blocker_target',v7['blocker']['a']['lo']=='1/1491' and v7['blocker']['a']['hi']=='1/1481')
    ck('resolved_blocker_id',r['resolved_builder_blocker_id']=='POST_GUARD_V6_FORWARD_ENERGY_GUARD_NOT_SEPARATED_Z1490_1480')
    ck('target',r['target_cell']==['1/1491','1/1481'] and r['anchor_a']=='1/1501')
    ck('two_paths',len(r['evaluators'])==2 and {t['control'] for t in r['evaluators']}=={False,True})

    alpha,kappa,beta=map(F,[cfg['alpha'],cfg['kappa'],cfg['beta']])
    ck('weighted_virial_x_coeff',kappa/2-3+alpha==0)
    ck('weighted_virial_u_coeff',kappa-alpha*F(15,4)==0)
    ck('beta_identity',beta==alpha*max(abs(kappa-6),abs(kappa-3)))

    b=bg('hillipop-ede_n3',states)
    ck('background_positive',b['H0']>0 and b['ol']==0 and all(b[k]>=0 for k in ['og','our','ob','oc']))
    expected_anchor={False:cfg['anchors']['primary'],True:cfg['anchors']['control']}
    v6tracks={t['control']:t for t in v6['evaluators']}
    nodes=[F(1,1501),F(1,1491),F(1,1481)]

    for t in r['evaluators']:
        control=t['control']; label='control' if control else 'primary'
        a=expected_anchor[control]
        ck(label+':status',t['status']=='PASS_TO_TARGET')
        ck(label+':lineage','without independent state reset' in t['lineage'])
        ck(label+':v6_anchor',t['anchor_E']==a['E_upper'] and t['anchor_Y']==a['Y_upper'] and t['Vbar']==a['Vbar'] and t['equilibrium_upper']==a['equilibrium_upper'])
        ck(label+':v6_endpoint_match',v6tracks[control]['last_E']==t['anchor_E'] and v6tracks[control]['last_Y']==t['anchor_Y'])
        ck(label+':two_rows',len(t['rows'])==2)
        E,Y,Vbar,eq=map(F,[t['anchor_E'],t['anchor_Y'],t['Vbar'],t['equilibrium_upper']])
        for idx,row in enumerate(t['rows']):
            left,right=nodes[idx],nodes[idx+1]
            rp=f'{label}:{idx}:'
            ck(rp+'geometry',F(row['a0'])==left and F(row['a1'])==right)
            ck(rp+'role',row['role']==('NEW_CONNECTED_BRIDGE' if idx==0 else 'TARGET_CELL'))
            ck(rp+'energy_continuity',F(row['E_left'])==E and F(row['Y_left'])==Y)
            B=control_B0(right,b) if control else primary_B0(right,b)
            ck(rp+'background_lower',F(row['B0_lower'])==B)
            G=down(3*B-E)
            ck(rp+'guard_recompute',F(row['G_lower'])==G)
            ck(rp+'strict_guard',G>0 and row['accepted'] is True and row['status']=='PASS_STRICT_WHOLE_CELL_GUARD')
            if control:
                d=1/(1+kappa*(right-left)/right)
                ck(rp+'control_decay',F(row['decay_upper'])==d)
                Y1=up(eq+(Y-eq)*d) if Y>=eq else eq
            else:
                dlo,dhi=F(row['decay_lower']),F(row['decay_upper'])
                true_d,dalt=independent_primary_decay(left,right,kappa)
                ck(rp+'primary_decay_contains',dec(dlo)<=true_d<=dec(dhi))
                ck(rp+'primary_decay_tight',dhi>=dalt and dhi-dalt<=F(5,10**18))
                Y1=max(up(dlo*Y+(1-dlo)*eq),up(dhi*Y+(1-dhi)*eq))
                # Independently computed direct-ln/exp bound must be no larger than serialized one.
                Yalt=up(eq+(Y-eq)*dalt) if Y>=eq else eq
                ck(rp+'independent_decay_conservative',Y1>=Yalt)
            E1=min(E,up(Y1+alpha*Vbar))
            ck(rp+'Y_right',F(row['Y_right'])==Y1)
            ck(rp+'E_right',F(row['E_right'])==E1 and E1<=E)
            E,Y=E1,Y1
        ck(label+':target_margin',F(t['target_G_lower'])==F(t['rows'][-1]['G_lower']) and F(t['target_G_lower'])>0)
        ck(label+':endpoint',F(t['last_E'])==E and F(t['last_Y'])==Y)

    ck('expected_primary_target',F(r['evaluators'][0]['target_G_lower'])==F(49241552932763639,250000000000000000))
    ck('expected_control_target',F(r['evaluators'][1]['target_G_lower'])==F(49535155239257769,1000000000000000000))
    ck('weakest_margin_positive',min(F(t['target_G_lower']) for t in r['evaluators'])==F(49535155239257769,10**18)>0)
    ck('scope_no_overclaim',r['q_complete'] is False and r['complete_a1_certificate'] is False and r['complete_xe_tau_bounds'] is False and r['native_P6']=='UNRESOLVED')
    ck('no_model_change',r['accepted_model_change'] is False and r['physical_falsification'] is False)
    ck('no_new_hydrogen_thermal',r['hydrogen_thermal_cells_new']==0 and r['retained_frec_cells']==59 and r['retained_H_to_frec_tubes']==4)
    ck('return_route',r['return_route']=='RESULT INGESTION & ROUTING ENGINE 2.1.0')
    ck('budget',r['execution']['elapsed_seconds']<cfg['max_seconds_total'] and r['execution']['native_or_paid_runs']==0)
    return checks

def mutation_suite(r,cfg):
    muts=[]
    def reject(name,fn):
        x=copy.deepcopy(r); fn(x)
        try: validate_core(x,cfg); ok=False
        except Exception: ok=True
        muts.append({'mutation':name,'rejected':ok})
        if not ok: raise AssertionError('mutation accepted:'+name)
    reject('forged_positive_target_margin',lambda x:x['evaluators'][1]['rows'][1].__setitem__('G_lower','1/1'))
    reject('missing_connected_bridge',lambda x:x['evaluators'][0].__setitem__('rows',x['evaluators'][0]['rows'][1:]))
    reject('independent_anchor_restart',lambda x:x['evaluators'][0].__setitem__('lineage','independent state reset'))
    reject('changed_target',lambda x:x.__setitem__('target_cell',['1/1491','1/1471']))
    reject('full_history_overclaim',lambda x:x.__setitem__('q_complete',True))
    reject('wrong_parent_builder',lambda x:x.__setitem__('parent_builder_raw_sha256','0'*64))
    reject('wrong_control_decay',lambda x:x['evaluators'][1]['rows'][1].__setitem__('decay_upper','1/1'))
    reject('broken_energy_continuity',lambda x:x['evaluators'][0]['rows'][1].__setitem__('E_left',x['evaluators'][0]['anchor_E']))
    return muts

def main():
    t=time.monotonic(); started=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
    cfg=json.loads((ROOT/'q048_guard_resume_config_v8.json').read_text())
    raw=ROOT/'q048_guard_resume_result_v8.json'
    r=json.loads(raw.read_text())
    checks=validate_core(r,cfg)
    muts=mutation_suite(r,cfg)
    out={'schema_version':'UNVALIDATED_LOCAL_CONTRACT','q':'Q048','technical_state':'PASS',
         'result_sha256':digest(raw),'checks_total':len(checks),'checks_passed':len(checks),'checks':checks,
         'semantic_mutations':muts,'mutations_total':len(muts),'mutations_rejected':sum(x['rejected'] for x in muts),
         'start_utc':started,'end_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
         'elapsed_seconds':time.monotonic()-t,'python':platform.python_version(),
         'producer_imported':False,'old_science_or_old_validator_reexecuted':False,
         'independence_scope':'Producer-free identity/hash/lineage rebuild; direct Fraction background arithmetic; separate 140-step finite-node sqrt; Decimal160 direct ln/exp enclosure check; shared frozen physical premises and source inputs, not independent physical evidence.',
         'formal_global_schema_validation':False}
    (ROOT/'q048_guard_resume_validation_v8.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'technical_state':'PASS','checks':f"{len(checks)}/{len(checks)}",'mutations':f"{len(muts)}/{len(muts)}",'elapsed':out['elapsed_seconds']},indent=2))

if __name__=='__main__': main()
