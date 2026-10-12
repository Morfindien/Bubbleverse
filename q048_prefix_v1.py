"""Q048 finite source-real prefix computation, exact outward proof arithmetic.

Reuses the pinned Q047 residual/Metzler verifier. Captured binary64 inputs
define conditional exact-real parameters. Native solver tolerances/starts are
not error certificates. No native process, shooting, MCMC, or physical fit.
This component NEVER advertises full-history or actual-source admission PASS.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json, os, platform, sys, time
import q047_math_v1 as m
import q047_certificate_v1 as old
import q047_precursor_check_v1 as pre
from math import factorial

Q='Q-048';ID='Q048-PREFIX-V1';VERSION='v1'
FINAL_SCOPE='CONDITIONAL_SOURCE_REAL_PREFIX'
SOURCE='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
BASE='24f380ba4bc0129ac3bfcd1dcb105c597191b47a'
CASES=old.CASES
ROOT=Path(__file__).resolve().parent
PINNED_TRIG=pre.trig

def trig32(x,cosine=False):
    """Degree32 Taylor + Lagrange/1-Lipschitz remainder, exact outward.

    Absolute derivatives of sin/cos are <=1. On x=[c-r,c+r], the
    polynomial error is <=|c|^33/33!+r. No statistical accuracy assumption.
    Its AD derivative uses separately enclosed sin/cos. Wider proof bounds
    replace degree160 work; unchanged source functions and physical inputs.
    """
    if isinstance(x,m.A):
        val=trig32(x.v,cosine);der=-trig32(x.v) if cosine else trig32(x.v,True)
        return m.A(val,[der*d for d in x.d])
    x=m.iv(x);c=(x.lo+x.hi)/2;r=(x.hi-x.lo)/2
    if abs(c)>16:raise ValueError('TRIG_RANGE_CAP_UNRESOLVED')
    total=F(0)
    for k in range(0 if cosine else 1,33,2):
        total+=(-1)**(k//2 if cosine else (k-1)//2)*c**k/factorial(k)
    rem=abs(c)**33/factorial(33)+r
    b=m.I.rounded(total-rem,total+rem)
    return m.I(max(F(-1),b.lo),min(F(1),b.hi))

# The reused source evaluator resolves this global primitive at call time.
# Only the numerical enclosure primitive changes, in this process.
pre.trig=trig32

def exact(value):return old.rational(value)
def point(hexstr):
    if not isinstance(hexstr,str) or '0x' not in hexstr:raise ValueError('C99_HEX_REQUIRED')
    try:return m.I(F.from_float(float.fromhex(hexstr)))
    except (ValueError,OverflowError):raise ValueError('NONFINITE_HEX')
def pairs(x):return old.pairs(pre.value(x))

def validate_config(c):
    if c.get('actual_reference_qualified'):raise ValueError('BOOLEAN_ADMISSION_FORBIDDEN')
    if c.get('schema')!='Q048_PREFIX_CONFIG_V1' or c.get('q')!=Q:raise ValueError('Q_SCHEMA')
    if c.get('q_assignment')!='PROPOSED_UNVERIFIED' or c.get('case_id')!='NOT_ASSIGNED':raise ValueError('CANONICAL_IDENTITY_NOT_GRANTED')
    if c.get('source_commit')!=SOURCE or set(c['cases'])!=set(CASES):raise ValueError('SOURCE_CASE_IDENTITY')
    question=c['scientific_question']
    if hashlib.sha256(question.encode()).hexdigest()!=c['question_sha256']:raise ValueError('EXACT_QUESTION_CHANGED')
    if c['question_sha256']!='c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436':raise ValueError('QUESTION_IDENTITY')
    settings=c['numerics']
    if not 1<=settings['max_cells_per_stage']<=256 or not 0<=settings['max_halvings']<=20:raise ValueError('WORK_CAP')
    if not 1<=settings['case_seconds']<=180:raise ValueError('WALL_TIME_CAP')
    for name,row in c['cases'].items():
        bg=row['background'];starts=row['thermal_starts']
        if bg['case']!=name or bg['origin']!='NEW_RECONSTRUCTION' or len(starts)!=7:raise ValueError('CAPTURE_IDENTITY')
        if [s['phase'] for s in starts]!=list(range(7)):raise ValueError('PHASE_IDENTITY')
        if bg['N_ncdm']!=1 or len(bg['neutrinos'])!=1:raise ValueError('REDUCED_NCDM_VARIANT')
        for flag in ('has_idm','has_idr','has_dcdm','has_dr','has_fld','has_curvature'):
            if bg['flags'].get(flag)!=0:raise ValueError('UNSUPPORTED_BACKGROUND_BRANCH '+flag)
        for flag in ('has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr'):
            if bg['thermal_flags'].get(flag)!=0:raise ValueError('UNSUPPORTED_THERMAL_BRANCH '+flag)
        if bg['thermal_flags']['recombination']!=1 or starts[0]['HyRec_MODEL']!=4:raise ValueError('RECOMBINATION_VARIANT')
        if bg['flags']['has_scf']!=int(name.endswith('ede_n3')):raise ValueError('MODEL_IDENTITY')
        if point(bg['fields']['K']).lo!=0:raise ValueError('CURVATURE')
        if starts[0]['y']!=['0x0p+0']:raise ValueError('EARLIEST_THERMAL_STATE')
        if -point(starts[4]['mz']).lo!=2870:raise ValueError('H_PHASE_BOUNDARY')
        if starts[0]['constants']['Tcmb']!=bg['fields']['T_cmb']:raise ValueError('TEMPERATURE_INPUT_MISMATCH')
        if name.endswith('ede_n3'):
            sc=bg['scalar']
            if sc['attractor_ic_scf']!=0 or point(sc['scf_parameters'][0]).lo!=3:raise ValueError('SCF_VARIANT')
            if point(sc['fields']['phi_prime_ini_scf']).lo!=0:raise ValueError('NONZERO_SCF_INITIAL_DERIVATIVE_UNSUPPORTED')
    return c

def parameters(row):
    bg=row['background'];v=bg['fields'];k=row['thermal_starts'][0]['constants']
    H=point(v['H0']);square=pre.square(H)
    t={'H0':H,'gamma':point(v['Omega0_g'])*square,
       'ur':point(v['Omega0_ur'])*square,
       'matter':(point(v['Omega0_b'])+point(v['Omega0_cdm']))*square,
       'lambda':point(v['Omega0_lambda'])*square,'K':point(v['K']),
       'T0':point(v['T_cmb']),'nH0':point(k['nH0_SI']),
       'fHe':point(k['fHe_CLASS']),'neutrinos':[],'ede':None}
    if k['fHe_CLASS']!=k['fHe_HyRec']:raise ValueError('HELIUM_NORMALIZATION')
    for n in bg['neutrinos']:
        if n['got_files']!=0:raise ValueError('EXTERNAL_DISTRIBUTION_UNSUPPORTED')
        nodes=list(map(point,n['q_ncdm_bg']));weights=list(map(point,n['w_ncdm_bg']))
        if len(nodes)!=len(weights) or not 1<=len(nodes)<=64:raise ValueError('NCDM_NODE_SHAPE')
        t['neutrinos'].append({'mass':point(n['fields']['M_ncdm']),
            'factor':point(n['fields']['factor_ncdm']),
            'nodes':nodes,'weights':weights,'reference':'FINITE_NATIVE'})
    if bg['flags']['has_scf']:
        sc=bg['scalar']['scf_parameters']
        t['ede']={'F':point(sc[1]),'m':point(sc[2]),'B':point(sc[3])}
    if min(t[z].lo for z in ('H0','gamma','T0','nH0','fHe'))<=0:raise ValueError('PARAMETER_DOMAIN')
    return t

def source_initial(row,t):
    """Compute finite-node initial branch inequalities, not native error bars."""
    a=point(row['precision']['a_ini_over_a_today_default'])
    state=None if t['ede'] is None else [point(row['background']['scalar']['fields']['phi_ini_scf']),m.I(0)]
    b=pre.background(a,t,state)
    radiation=(t['gamma']+t['ur'])/a**4
    neutrino_checks=[]
    for n in t['neutrinos']:
        rho,p=pre.neutrino_sum(a,n);r=p/rho-F(1,3)
        tol=point(row['precision']['tol_ncdm_initial_w'])
        neutrino_checks.append({'p_over_rho_minus_third':pairs(r),'tolerance':pairs(tol),
                               'proved_default_epoch_relativistic':r.absmax()<tol.lo})
        radiation+=3*p
    if state is not None:
        _,_,ve=pre.potential(state[0],t['ede']);radiation+=pre.square(state[1])/2-ve
    omega=radiation/(pre.square(b['H'])+t['K']/a**2)
    tol=point(row['precision']['tol_initial_Omega_r'])
    radiation_ok=(omega-1).absmax()<tol.lo
    branch_ok=all(x['proved_default_epoch_relativistic'] for x in neutrino_checks)
    return {'scope':'CONDITIONAL_EXACT_REAL_INITIALIZATION','a':pairs(a),
        'scalar_state':None if state is None else list(map(pairs,state)),
        'neutrinos':neutrino_checks,'Omega_r':pairs(omega),
        'radiation_test_proved':radiation_ok,
        'source_EDE_guard_proved':b['ede_latch'].hi<F(1,2),
        'initial_conditions_gate':'PASS_CONDITIONAL' if branch_ok and radiation_ok and b['ede_latch'].hi<F(1,2) else 'UNRESOLVED',
        'H_CLASS_1_Mpc':pairs(b['H']),'rho_gamma_CLASS':pairs(b['rho_gamma']),
        'actual_instance_error_linkage':'UNRESOLVED'},a,state

def certify(cell,initial,field):
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    return pre.certify_cell(cell,initial,field)

def background_prefix(t,a0,state,end,settings,deadline):
    if state is None:
        b=pre.background(m.I(a0.lo,end),t)
        return {'status':'COMPLETE_ANALYTIC_FINITE_NODE_REFERENCE','requested_end_a':str(end),
                'certified_end_a':str(end),'cells':[],
                'scope':'CONDITIONAL_COMMON_BACKGROUND','positive_H':b['H'].lo>0}
    now=a0.lo;current=state;cells=[];reason='WORK_CAP'
    while now<end and len(cells)<settings['max_cells_per_stage'] and time.monotonic()<deadline:
        candidate_end=min(end,now*F(5,4));accepted=None
        center=[(y.lo+y.hi)/2 for y in current]
        for halving in range(settings['max_halvings']+1):
            if time.monotonic()>=deadline:reason='WALL_TIME_CAP';break
            width=candidate_end-now
            field=lambda xi,y:[r*width/(now+width*xi) for r in pre.ede_field(now+width*xi,y,t)[0]]
            try:
                slopes=list(map(pre.value,field(m.I(0),[m.A(c) for c in center])))
                predictor=[[str(center[i]),str((slopes[i].lo+slopes[i].hi)/2)] for i in range(2)]
                box=[]
                for i in range(2):
                    step=abs(F(predictor[i][1]));err=(current[i].hi-current[i].lo)/2
                    pad=max(F('1e-9') if i==0 else F('1e-15'),err*2,step*2)
                    box.append([str(center[i]-pad-step),str(center[i]+pad+step)])
                cell={'t0':'0','t1':'1','predictor':predictor,'box':box}
                report=certify(cell,current,field)
                ys=[old.interval(v) for v in report['whole_state']]
                if report['closed']:
                    bg=pre.background(m.I(now,candidate_end),t,ys)
                    if bg['ede_latch'].hi>=F(1,2):reason='SOURCE_EDE_GUARD_NOT_SEPARATED'
                    else:
                        accepted={'a0':str(now),'a1':str(candidate_end),'predictor':predictor,
                                  'certificate':report,'forcing':{k:pairs(v) for k,v in bg.items()}}
                        break
                else:reason='BACKGROUND_TUBE_NOT_CLOSED'
            except (ValueError,AssertionError,ZeroDivisionError) as e:reason=type(e).__name__+':'+str(e)
            candidate_end=(now+candidate_end)/2
        if accepted is None:break
        cells.append(accepted);current=[old.interval(v) for v in accepted['certificate']['endpoint']];now=candidate_end
    if time.monotonic()>=deadline and now<end:reason='WALL_TIME_CAP'
    return {'status':'COMPLETE' if now==end else 'PARTIAL','scope':'CONDITIONAL_COMMON_BACKGROUND',
            'requested_end_a':str(end),'certified_end_a':str(now),'cells':cells,
            'endpoint':list(map(pairs,current)),'blocker':None if now==end else reason}

def thermal_prefix(row,t,bg,settings,deadline):
    start=1/(1-point(row['thermal_starts'][0]['mz']).lo)
    end=F(1,2871)
    if F(bg['certified_end_a'])<start:
        return {'status':'NOT_EXECUTED','blocker':'BACKGROUND_DOES_NOT_REACH_EARLIEST_THERMAL_EPOCH','cells':[],
                'certified_end_a':None,'requested_end_a':str(end)}
    boundary=[1/(1-point(s['mz']).lo) for s in row['thermal_starts'][1:5]]
    if not 0<start<boundary[0]<boundary[1]<boundary[2]<boundary[3]==end:raise ValueError('THERMAL_SOURCE_PARTITION')
    now=start;current=[m.I(0)];cells=[];reason='WORK_CAP'
    while now<end and len(cells)<settings['max_cells_per_stage'] and time.monotonic()<deadline:
        j=sum(now>=v for v in boundary);mode=pre.MODES[j]
        cell_end=min(boundary[j],now*F(5,4));accepted=None;bgcell=None
        if t['ede'] is not None:
            covering=[b for b in bg['cells'] if F(b['a0'])<=now<F(b['a1'])]
            if len(covering)!=1:reason='COMMON_BACKGROUND_CELL_MISSING';break
            bgcell=covering[0];cell_end=min(cell_end,F(bgcell['a1']))
        for halving in range(settings['max_halvings']+1):
            if time.monotonic()>=deadline:reason='WALL_TIME_CAP';break
            width=cell_end-now;mid=now+width/2
            ys=None if bgcell is None else [old.interval(v) for v in bgcell['certificate']['whole_state']]
            getbg=lambda a:pre.background(a,t,ys)
            field=lambda xi,y:[pre.thermal(mode,now+width*xi,y[0],t,getbg(now+width*xi))['rate']*width/(now+width*xi)]
            try:
                if mode=='brec':center=(current[0].lo+current[0].hi)/2
                else:
                    beta=pre.thermal(mode,m.I(mid),m.I(0),t,getbg(m.I(mid)))['beta']
                    center=(1/(1+beta)).lo
                cell={'t0':'0','t1':'1','predictor':[[str(center)]],
                      'box':[['-1/1000000','1/50']]}
                report=certify(cell,current,field)
                if report['closed']:
                    a=m.I(now,cell_end);state=old.interval(report['whole_state'][0])
                    info=pre.thermal(mode,a,state,t,getbg(a))
                    # The inherited source warning domain is entirely below this prefix (z>=2870).
                    if (1/a-1).lo<2870:raise ValueError('PREFIX_WARNING_DOMAIN')
                    accepted={'a0':str(now),'a1':str(cell_end),'mode':mode,'predictor':cell['predictor'],
                              'certificate':report,'Tmat_K':pairs(info['Tmat']),'xe_thermal':pairs(info['x'])}
                    break
                reason='THERMAL_TUBE_NOT_CLOSED'
            except (ValueError,AssertionError,ZeroDivisionError) as e:reason=type(e).__name__+':'+str(e)
            cell_end=(now+cell_end)/2
        if accepted is None:break
        cells.append(accepted);current=[old.interval(report['endpoint'][0])];now=cell_end
    if time.monotonic()>=deadline and now<end:reason='WALL_TIME_CAP'
    full=now==end
    onset=pairs(pre.onset(current[0],m.I(end),t)) if full else None
    return {'status':'COMPLETE' if full else 'PARTIAL','scope':FINAL_SCOPE,
            'requested_end_a':str(end),'certified_end_a':str(now),'cells':cells,
            'onset_w':pairs(current[0]) if full else None,'onset_q':onset,
            'blocker':None if full else reason}

def run_case(c,name,out):
    validate_config(c);started=time.monotonic();row=c['cases'][name];t=parameters(row)
    result={'q':Q,'q_assignment':c['q_assignment'],'case_id':c['case_id'],'configuration':name,
            'program_id':ID,'version':VERSION,'scientific_question':c['scientific_question'],
            'scope':FINAL_SCOPE,'source_commit':SOURCE,'source_run_id':'38140371059',
            'source_input_hashes':row['source_input_hashes'],'execution_status':'COMPLETE',
            'final_result_gate':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
            'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'new_native_evaluations':0,'likelihood_evaluations':0,'actual_source_admission':'UNRESOLVED',
            'return_route':'RESULT INGESTION & ROUTING ENGINE'}
    try:
        initial,a,state=source_initial(row,t);result['source_initialization']=initial
        if initial['initial_conditions_gate']!='PASS_CONDITIONAL':
            result['first_blocker']='SOURCE_INITIAL_BRANCH_NOT_SEPARATED'
        else:
            deadline=started+c['numerics']['case_seconds']
            bg=background_prefix(t,a,state,F(1,2871),c['numerics'],deadline);result['background']=bg
            th=thermal_prefix(row,t,bg,c['numerics'],deadline);result['thermal']=th
            result['conditional_H_entry_gate']='PASS_CONDITIONAL' if th['status']=='COMPLETE' else 'UNRESOLVED'
            result['first_blocker']= ('ACTUAL_REFERENCE_LINKAGE_AND_TWO_STATE_FIRST_EVENT_CERTIFICATE'
                if th['status']=='COMPLETE' else th.get('blocker') or bg.get('blocker'))
    except (ValueError,AssertionError,ZeroDivisionError,KeyError) as e:
        result.update(execution_status='COMPONENT_FAILURE',first_blocker=type(e).__name__+':'+str(e))
    result.update(elapsed_seconds=time.monotonic()-started,python=platform.python_version(),
                  run_id=os.environ.get('GITHUB_RUN_ID','LOCAL'),
                  executed_commit=os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'))
    old.write(Path(out)/(name+'_prefix_v1.json'),result)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--program-id',default=ID)
    parser.add_argument('--case',choices=CASES);parser.add_argument('--config',default=str(ROOT/'q048_prefix_config_v1.json'))
    parser.add_argument('--out',default='q048_prefix_results')
    a=parser.parse_args()
    if a.program_id!=ID:raise ValueError('PROGRAM_ID_GATE')
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    c=validate_config(old.load(a.config));names=[a.case] if a.case else list(CASES)
    for name in names:
        r=run_case(c,name,a.out)
        print(json.dumps({'configuration':name,'execution_status':r['execution_status'],
            'conditional_H_entry_gate':r.get('conditional_H_entry_gate','UNRESOLVED'),
            'final_result_gate':r['final_result_gate'],'first_blocker':r.get('first_blocker')}),flush=True)
        if r['execution_status']=='COMPONENT_FAILURE':return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
