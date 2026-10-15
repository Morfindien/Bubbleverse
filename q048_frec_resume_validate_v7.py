"""Producer-free finite validation for Q048 Builder V7 result."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from math import isqrt
import json, hashlib, time
ROOT = Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def root_lower(x):
    den=10**150
    r=F(isqrt((x.numerator*den*den)//x.denominator),den)
    assert r*r <= x < (r+F(1,den))**2
    return r
def hf(x): return F.from_float(float.fromhex(x))

def validate(r,s):
    ck=[]
    def test(n,v): ck.append({'id':n,'pass':bool(v)})
    par=json.loads((ROOT/s['parent_raw']).read_text())
    cp=json.loads((ROOT/s['parent_checkpoint']).read_text())
    pv=json.loads((ROOT/s['parent_validation']).read_text())
    g=json.loads((ROOT/s['guard_raw']).read_text())
    gv=json.loads((ROOT/s['guard_validation']).read_text())
    base=json.loads((ROOT/s['base_raw']).read_text())
    capture=json.loads((ROOT/'sources/q048_prefix_config_v1.json').read_text())

    test('identity', r['q']==r['target_q']=='Q048' and r['question_sha256']==s['question_sha256'])
    test('exact_question', r['exact_question']==par['exact_question'] and hashlib.sha256(r['exact_question'].encode()).hexdigest()==s['question_sha256'])
    test('frozen_spec', sha(ROOT/'q048_frec_resume_spec_v7.json')==r['spec_sha256'])
    test('parent_link', sha(ROOT/s['parent_raw'])==r['parent_raw_sha256']==cp['source_result_sha256']==pv['result_sha256'])
    test('parent_validation', pv['status']=='PASS')
    test('guard_link', sha(ROOT/s['guard_raw'])==r['guard_raw_sha256']==gv['result_sha256'])
    test('guard_validation', gv['technical_state']=='PASS' and gv['checks_total']==gv['checks_passed']==56)
    test('science_identity', g['source_commit']==r['source_commit']==s['source_commit'] and g['capture_sha256']==r['capture_sha256']==s['capture_sha256'])
    test('no_prefix_replay', r['prior_science_reexecuted'] is False and r['retained_accepted_cells_reused']==57 and r['retained_H_to_frec_tubes_reused']==4)
    test('frontier_start', r['initial_frontiers']==cp['frontiers']==s['initial_frontiers'])

    fronts=dict(r['initial_frontiers']); passed=0
    target=[x for x in g['evaluators'][0]['rows'] if x.get('role')=='TARGET_CELL'][0]
    target_start,target_end=map(F,g['target_cell'])
    for i,c in enumerate(r['new_cells']):
        n=c['case']; z0,z1=c['z']; left,right=map(F,[c['a']['lo'],c['a']['hi']]); E=F(c['energy_upper'])
        test(f'{i}:continuity', fronts[n]==z0 and left==F(1,z0+1) and right==F(1,z1+1) and z1==z0-10)
        test(f'{i}:same_source_family', c['parent_source_family']==par['result_id'] and c['retained_base_result']==base['result_id'] and c['new_guard_result']==g['result_id'] and 'same accepted event' in c['correlation'])
        if n=='hillipop-ede_n3':
            if left==target_start:
                expected=F(target['E_left'])
                test(f'{i}:target_energy_binding', E==expected and c['guard_binding']['kind']=='V6_TARGET_WHOLE_CELL' and F(c['guard_binding']['certified_G_lower'])==F(target['G_lower'])>0 and F(c['guard_binding']['certified_E_left'])==expected)
            else:
                expected=F(g['evaluators'][0]['last_E'])
                test(f'{i}:forward_energy_binding', left>=target_end and E==expected and c['guard_binding']['kind']=='V6_ENDPOINT_FORWARD_ENERGY_ONLY' and c['guard_binding']['target_G_margin_reused'] is False and c['guard_binding']['transport_identity']=='e_u=-3X^2<=0')

        # Independent finite-node lower for background at right endpoint.
        bg=capture['cases'][n]['background']; f=bg['fields']; H0=hf(f['H0']); nu=bg['neutrinos'][0]
        base_finite=H0**2*((hf(f['Omega0_g'])+hf(f['Omega0_ur']))/right**4+(hf(f['Omega0_b'])+hf(f['Omega0_cdm']))/right**3+hf(f['Omega0_lambda']))
        mass=hf(nu['fields']['M_ncdm']); fac=hf(nu['fields']['factor_ncdm']); qs=list(map(hf,nu['q_ncdm_bg'])); ws=list(map(hf,nu['w_ncdm_bg']))
        base_finite += fac/right**4*sum(q*q*root_lower(q*q+(right*mass)**2)*w for q,w in zip(qs,ws))
        B=F(c['B0']['lo']); floor=F(c['floor']['lo']); G=F(c['G_lower'])
        test(f'{i}:background_lower', 0<B<=base_finite and floor>=0)
        test(f'{i}:guard_algebra', G==3*B-E+floor)
        admitted=F(c['admitted_G_lower'])
        if c['guard_binding']['kind']=='V6_TARGET_WHOLE_CELL':
            test(f'{i}:admitted_target_bound', admitted==min(G,F(target['G_lower'])) and admitted>0)
        else:
            test(f'{i}:admitted_recomputed_bound', admitted==G)

        if not c['status'].startswith('PASS'):
            test(f'{i}:first_actual_obstruction', i==len(r['new_cells'])-1 and G<=0 and r['blocker']['z']==c['z'] and F(r['blocker']['margin'])==G and r['blocker']['attempted_cell_index']==i)
            test(f'{i}:not_physical_falsification', r['blocker']['method_insufficient_not_physical_falsification'] is True and r['physical_falsification'] is False)
            break

        test(f'{i}:positive_guard', admitted>0 and G>0)
        op=c['operator']
        test(f'{i}:source_domain', F('.004')<F(op['TR_eV']['lo'])<=F(op['TR_eV']['hi'])<F('.4') and F(op['TM_over_TR']['lo'])>F('.1') and F(op['Tgamma_K']['lo'])>1775 and F(op['Tgamma_K']['hi'])<4415 and F(op['fit_denominator']['lo'])>0 and z1>900)
        alo=[F(x['lo']) for x in op['Alpha']]; ahi=[F(x['hi']) for x in op['Alpha']]
        elo=[F(x['lo']) for x in op['Alpha_eq']]; ehi=[F(x['hi']) for x in op['Alpha_eq']]
        slo,shi=map(F,[op['Saha_HyRec']['lo'],op['Saha_HyRec']['hi']])
        test(f'{i}:positive_atomic_denominators', min(alo+elo+[slo,F(op['R2p2s']['lo'])])>0 and 'Beta0+L' in op['positive_C_denominator_identity'])
        for label,q in [('L',F(1,1000000)),('R',F(0))]:
            br=c['branches'][label]; test(f'{i}:{label}:jump_semantics', F(br['q'])==q and br['admitted'])
            for l in range(2):
                for face,key,negative in [(F(c['h_barrier']['lo']),'hydrogen_low_face_terms',True),(F(c['h_barrier']['hi']),'hydrogen_high_face_terms',False)]:
                    lo=alo[l]*face*(face+q)-ehi[l]*shi*(1-face); hi=ahi[l]*face*(face+q)-elo[l]*slo*(1-face)
                    rec=br[key][l]
                    test(f'{i}:{label}:{l}:{key}', F(rec['lo'])<=lo<=hi<=F(rec['hi']) and (hi<0 if negative else lo>0))
            beta=F(br['thermal']['beta']['lo']); faces=br['thermal']['faces']; wl,wh=map(F,[c['w_barrier']['lo'],c['w_barrier']['hi']])
            test(f'{i}:{label}:thermal_inward', beta>0 and F(faces['lower_face_inward_lower'])==1-(1+beta)*wl>0 and F(faces['upper_face_inward_margin'])==(1+beta)*wh-1>0 and faces['admitted'])
        test(f'{i}:invariant_barriers', [c['h_barrier']['lo'],c['h_barrier']['hi']]==s['barriers']['h'] and [c['w_barrier']['lo'],c['w_barrier']['hi']]==s['barriers']['w'])
        fronts[n]=z1; passed+=1

    test('new_count_and_final_frontier', passed==r['new_accepted_cells'] and fronts==r['final_frontiers'])
    test('chain_count', r['retained_accepted_cells_reused']+passed==57+passed)
    test('no_overclaim', not any(r[k] for k in ['complete_a1_certificate','q_complete','final_delta_xe_bounds_computed','final_delta_tau_bounds_computed','physical_falsification','accepted_model_change']) and r['native_P6']=='UNRESOLVED')
    test('finite_budget', r['execution']['elapsed_seconds']<=s['budget_seconds'] and passed<=s['max_new_accepted_cells'])
    test('expected_obstruction_class', r['status']=='PARTIAL_WITH_EXACT_NEW_OBSTRUCTION' and r['blocker']['code'] in ['NEW_WHOLE_CELL_GUARD_NOT_SEPARATED','NEXT_SOURCE_BRANCH_OR_FIT_DOMAIN_NOT_YET_ADMITTED','NEW_CELL_SOURCE_RATE_OR_THERMAL_FACE_NOT_SEPARATED','NEW_CELL_ATOMIC_FACTOR_POSITIVITY_NOT_SEPARATED','FROZEN_BUDGET_CHECKPOINT'])
    return ck

if __name__=='__main__':
    clock=time.monotonic(); raw=ROOT/'q048_frec_resume_result_v7.json'; r=json.loads(raw.read_text()); s=json.loads((ROOT/'q048_frec_resume_spec_v7.json').read_text())
    checks=validate(r,s)
    for f,rec in s['inputs'].items():
        p=ROOT/f
        checks.append({'id':'pin:'+f,'pass':p.exists() and p.stat().st_size==rec['bytes'] and sha(p)==rec['sha256']})
    mutations=[]
    mutation_specs=[
      ('forged_guard',lambda x:x['new_cells'][0].update(G_lower='1')),
      ('broken_frontier',lambda x:x['initial_frontiers'].update({'hillipop-ede_n3':1520})),
      ('wrong_energy',lambda x:x['new_cells'][0].update(energy_upper='0')),
      ('wrong_branch_q',lambda x:x['new_cells'][0]['branches']['L'].update(q='0')),
      ('full_history_overclaim',lambda x:x.update(complete_a1_certificate=True)),
      ('wrong_parent',lambda x:x.update(parent_raw_sha256='0'*64)),
      ('reuse_target_g_forward',lambda x:x['new_cells'][1]['guard_binding'].update(target_G_margin_reused=True)),
    ]
    for label,fn in mutation_specs:
        x=deepcopy(r); fn(x)
        try: rejected=not all(v['pass'] for v in validate(x,s))
        except (ValueError,KeyError,AssertionError,IndexError): rejected=True
        mutations.append({'id':label,'rejected':rejected})
    output={
      'schema_version':'UNVALIDATED_LOCAL_CONTRACT','q':'Q048',
      'status':'PASS' if all(x['pass'] for x in checks) and all(x['rejected'] for x in mutations) else 'FAIL',
      'technical_state':'PASS' if all(x['pass'] for x in checks) and all(x['rejected'] for x in mutations) else 'FAIL',
      'result_sha256':sha(raw),'validator_sha256':sha(ROOT/'q048_frec_resume_validate_v7.py'),
      'checks_total':len(checks),'checks_passed':sum(x['pass'] for x in checks),'checks':checks,
      'mutations_total':len(mutations),'mutations_rejected':sum(x['rejected'] for x in mutations),'mutations':mutations,
      'elapsed_seconds':time.monotonic()-clock,'prior_science_or_prior_validator_reexecuted':False,
      'independence_scope':'Producer-free new-result algebra/continuity/hash/domain checks plus separate exact finite-node background lower. Shared frozen source inputs/formulas; not independent physical evidence.'}
    (ROOT/'q048_frec_resume_validation_v7.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['status','checks_total','checks_passed','mutations_total','mutations_rejected','elapsed_seconds']},indent=2))
    if output['status']!='PASS':
        print('FAILED CHECKS',[x for x in checks if not x['pass']]); print('FAILED MUTATIONS',[x for x in mutations if not x['rejected']]); raise SystemExit(1)
