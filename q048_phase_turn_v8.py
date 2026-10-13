"""Q048 V8: bounded source-real phase/energy first-turn certificate for Camspec.

Scientific scope is deliberately narrow.  This module reuses the official,
validated Q048 V7 result only as a frozen parent witness.  It re-verifies one
selected accepted V7 splice cell against the frozen source and then changes
coordinates from Cartesian (phi,X) to the globally smooth signed variables

    theta = lambda*phi
    y     = -X

so the first scalar turning point is the first y=0 crossing from y>0 to y<0.
The new state avoids V7's oscillatory Cartesian wrapping.  A positive source
guard is checked on every new phase/turn cell.  At the unique first turn,
E_kinetic=0; if the rigorous turn-energy upper bound is below the exact
Mathematics-008 transfer threshold, monotone scalar energy proves the source
guard for every later a through z=2870.  Only then is the existing sign-aware
He1f/He2 thermal continuation recomputed to conditional H-entry.

This program does NOT qualify native floating-point/source-instance identity,
does NOT locate the shared helium q=1e-6 cutoff, and does NOT compute complete
latch/reset x_e(z) or tau_T(z) histories.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,json,time
import q048_guard_continuation_v7 as v7

v6=v7.v6
old=v7.old
p=v7.p
m=v7.m
pre=v7.pre
proof=v7.proof
ROOT=Path(__file__).resolve().parent
ID='Q048-PHASETURN-V8'
VERSION='v8'
Q=v7.Q
SOURCE=v7.SOURCE
SCOPE='CONDITIONAL_SOURCE_REAL_PHASE_ENERGY_TURN_GUARD_THERMAL'
CONFIG_SHA='097b4bf392ae494799676c86fa3d3a9b6f36526b36fa73bc7fd35b603d417f5d'


def fail(condition,message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()


def git_blob_sha1(path):
    b=Path(path).read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def settings():
    s=old.load(ROOT/'q048_phase_turn_config_v8.json')
    fail(sha256(ROOT/'q048_phase_turn_config_v8.json')==CONFIG_SHA,'CONFIG_HASH')
    fail(s['program_id']==ID and s['q']==Q and s['version']==VERSION and s['source_commit']==SOURCE,'CONFIG_IDENTITY')
    fail(s['question_sha256']==v6.config()['question_sha256'],'QUESTION_HASH')
    return s


def validate_sources():
    s=settings()
    # V6 has no journal pin and is safe to revalidate under the new journal.
    v6.validate_sources()
    for name,want in s['reused_git_blob_sha1'].items():
        fail(git_blob_sha1(ROOT/name)==want,'REUSED_GIT_BLOB '+name)
    fail(sha256(ROOT/s['math008_md'])==s['math008_md_sha256'],'MATH008_MD_HASH')
    fail(sha256(ROOT/s['math008_json'])==s['math008_json_sha256'],'MATH008_JSON_HASH')
    fail(sha256(ROOT/s['journal_file'])==s['journal_sha256'],'JOURNAL_HASH')
    mathj=old.load(ROOT/s['math008_json'])
    fail(mathj['q']==Q and mathj['question_sha256']==s['question_sha256'] and mathj['source_commit']==SOURCE,'MATH008_IDENTITY')
    fail(mathj['new_method']['name']=='source_root_phase_energy_first_turn_guard_v1','MATH008_METHOD')
    return s


def load_parent(path):
    s=settings()['parent_v7'];path=Path(path)
    fail(path.is_file(),'PARENT_V7_FILE_MISSING')
    fail(path.stat().st_size<=64_000_000,'PARENT_V7_SIZE_CAP')
    fail(sha256(path)==s['raw_sha256'],'PARENT_V7_RAW_HASH')
    try:
        with path.open('r',encoding='utf-8') as f:obj=json.load(f)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise ValueError('PARENT_V7_JSON') from exc
    fail(obj.get('schema')=='Q048_GUARD_FINAL_V7' and obj.get('q')==Q and obj.get('program_id')=='Q048-GUARDCONT-V7','PARENT_V7_IDENTITY')
    fail(obj.get('source_commit')==SOURCE and obj.get('question_sha256')==settings()['question_sha256'],'PARENT_V7_SOURCE')
    fail(obj.get('execution_status')=='COMPLETE' and obj.get('job_completeness_gate')=='PASS' and obj.get('tests_status')=='COMPLETE_CONDITIONAL','PARENT_V7_COMPLETENESS')
    c=obj['records']['camspec-ede_n3'];h=obj['records']['hillipop-ede_n3']
    fail(c['run_id']==s['run_id'] and c['executed_commit']==s['executed_commit'] and c['config_hash']==s['config_hash'],'PARENT_V7_RUN_BINDING')
    fail(c['extension']['guard']['cell_count']==s['camspec_guard_cell_count'] and c['extension']['guard']['blocker']==s['camspec_blocker'],'PARENT_V7_CAMSPEC_STATE')
    fail(h['extension']['thermal']['status']==s['hillipop_thermal_status'],'PARENT_V7_HILLIPOP_STATE')
    fail(obj['actual_source_admission']=='UNRESOLVED' and obj['final_result_gate']=='UNRESOLVED','PARENT_V7_SCOPE')
    fail(all(obj[k]=='NOT_COMPUTED' for k in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds')),'PARENT_V7_FULL_PRODUCTS')
    return obj


def _pairs(x):return proof.pairs(x)
def _mid(x):return (x.lo+x.hi)/2


def phase_constants(t):
    fail(t['ede'] is not None,'EDE_REQUIRED')
    lam=m.const('2.435e27')/t['ede']['F']
    amp=m.const('4152.39')*pre.square(t['ede']['m'])*pre.square(t['ede']['F'])
    floor=t['ede']['B']*m.const('3.968e-8')
    fail(lam.lo>0 and amp.lo>0 and floor.lo>=0,'PHASE_CONSTANT_DOMAIN')
    return {'lambda':lam,'A':amp,'floor':floor}


def theta_potential(theta,t):
    c=phase_constants(t)
    # q047's validated cell checker evaluates the vector field twice: once on
    # interval predictor states and once on AD states to construct the Jacobian.
    # Preserve AD objects here instead of coercing them through m.iv(), which
    # only accepts scalar/interval inputs.
    theta=theta if isinstance(theta,m.A) else m.iv(theta)
    cosv=pre.trig(theta,True);sinv=pre.trig(theta,False)
    d=1-cosv
    # Exact identity 1-cos(theta)>=0.  Intersect only the value enclosure with
    # the known non-negative range; for AD inputs keep the derivative enclosure
    # unchanged so the Jacobian remains rigorous.
    if isinstance(d,m.A):
        dv=pre.value(d);fail(dv.hi>=0,'PHASE_POTENTIAL_DOMAIN')
        d=m.A(m.I(max(F(0),dv.lo),dv.hi),d.d)
    else:
        fail(d.hi>=0,'PHASE_POTENTIAL_DOMAIN')
        d=m.I(max(F(0),d.lo),d.hi)
    U=c['A']*d**3
    Utheta=3*c['A']*sinv*d**2
    return U,Utheta,c


def phase_values(a,state,t):
    fail(len(state)==2,'PHASE_STATE_DIMENSION')
    theta,y=state;a=m.iv(a)
    U,Utheta,c=theta_potential(theta,t)
    base=v7._background_base(a,t)
    e=pre.square(y)/2+U
    H2=pre.square(base['H'])+(e+c['floor'])/3
    fail(pre.value(H2).lo>0,'PHASE_H_SQUARED')
    # m.root() is the AD-aware square root; m.sqrt_i() is interval-only.
    H=m.root(H2)
    theta_u=-c['lambda']*y/H
    y_u=-3*y+c['lambda']*Utheta/H
    guard_margin=3*pre.square(base['H'])+e+c['floor']-2*U
    guard_ratio=U/(3*pre.square(base['H'])+e+c['floor'])
    return {'U':U,'Utheta':Utheta,'constants':c,'base_H':base['H'],'e':e,'H':H,
            'theta_u':theta_u,'y_u':y_u,'guard_margin':guard_margin,'guard_ratio':guard_ratio}


def verify_splice(parent):
    s=settings()['splice'];case=s['case'];idx=s['cell_index_zero_based']
    fail(case=='camspec-ede_n3','SPLICE_CASE')
    report=parent['records'][case];guard=report['extension']['guard'];cells=guard['cells']
    fail(isinstance(idx,int) and 1<=idx<len(cells),'SPLICE_INDEX')
    prev=cells[idx-1];cell=cells[idx]
    fail(prev['a1']==cell['a0'],'SPLICE_PARTITION')
    current=[proof.interval(x) for x in prev['certificate']['endpoint']]
    now,end=F(cell['a0']),F(cell['a1'])
    row=v6.config()['cases'][case];t=p.parameters(row)
    field=v7._guard_field(now,end,t)
    recomputed=pre.certify_cell(cell['input'],current,field)
    fail(recomputed==cell['certificate'] and recomputed['closed'],'SPLICE_CELL_RECOMPUTE')
    whole=[proof.interval(x) for x in recomputed['whole_state']]
    g=v7.direct_guard(m.I(now,end),whole,t)
    fail(g['margin'].lo>0 and cell['guard']=={k:_pairs(v) for k,v in g.items()},'SPLICE_GUARD_RECOMPUTE')
    phi=proof.interval(recomputed['endpoint'][0]);X=proof.interval(recomputed['endpoint'][1]);y=-X
    # Transform only after constants are independently reconstructed.
    cc=phase_constants(t);theta=cc['lambda']*phi;U,_,_=theta_potential(theta,t);e=pre.square(y)/2+U
    pi=m.C['pi']
    fail((not s['require_x_negative']) or X.hi<0,'SPLICE_X_NEGATIVE')
    fail((not s['require_theta_open_zero_pi']) or (theta.lo>0 and theta.hi<pi.lo),'SPLICE_THETA_DOMAIN')
    # Mathematics-008 requires e-U>0.  Preserve the exact algebraic dependency:
    # e-U = y^2/2.  Subtracting independent interval enclosures e-U would lose
    # the shared U dependency and can falsely cross zero even when y is strictly
    # positive.  The kinetic identity is therefore the rigorous splice gate.
    kinetic=pre.square(y)/2
    fail((not s['require_kinetic_energy_positive']) or kinetic.lo>0,'SPLICE_KINETIC_GAP')
    fail((not s['require_energy_below_eight_A']) or e.hi<8*cc['A'].lo,'SPLICE_EIGHT_A')
    return {'method':s['method'],'parent_program_id':'Q048-GUARDCONT-V7','parent_run_id':settings()['parent_v7']['run_id'],
            'cell_index_zero_based':idx,'a0':str(now),'a1':str(end),'parent_cell_sha256':old.objhash(cell),
            'phi_endpoint':_pairs(phi),'X_endpoint':_pairs(X),'theta_endpoint':_pairs(theta),'y_endpoint':_pairs(y),
            'U_endpoint':_pairs(U),'e_endpoint':_pairs(e),'A':_pairs(cc['A']),'lambda':_pairs(cc['lambda']),'floor':_pairs(cc['floor']),
            'kinetic_energy_exact_identity':_pairs(kinetic),
            'rectangular_e_minus_U_upper_diagnostic':_pairs(e-m.I(U.hi)),
            'v7_direct_guard_margin':_pairs(g['margin']),
            'gate':'PASS_REVERIFIED_V7_SPLICE'},[theta,y],t,row


def _phase_field(now,end,t):
    width=end-now
    def field(xi,state):
        a=m.I(now)+m.I(width)*xi
        v=phase_values(a,state,t)
        scale=m.I(width)/a
        return [v['theta_u']*scale,v['y_u']*scale]
    return field


def _phase_predictor_and_box(now,end,current,t):
    field=_phase_field(now,end,t);center=[_mid(x) for x in current]
    k1=[pre.value(x) for x in field(m.I(0),[m.A(c) for c in center])];k1m=[_mid(x) for x in k1]
    half=[m.A(center[i]+k1m[i]/2) for i in range(2)]
    k2=[pre.value(x) for x in field(m.I(F(1,2)),half)];k2m=[_mid(x) for x in k2]
    ss=settings()['phase_turn'];floors=[F(ss['theta_pad_floor']),F(ss['y_pad_floor'])]
    coeff=[];box=[]
    for i in range(2):
        row=[center[i],k1m[i],k2m[i]-k1m[i]];pr=proof.poly_range(row)
        err=(current[i].hi-current[i].lo)/2;move=abs(row[1])+abs(row[2]);pad=max(floors[i],4*err,move/2)
        coeff.append([str(x) for x in row]);box.append([str(pr.lo-pad),str(pr.hi+pad)])
    return field,{'t0':'0','t1':'1','predictor':coeff,'box':box}


def _phase_cell(now,end,current,t):
    field,cell=_phase_predictor_and_box(now,end,current,t)
    try:report=pre.certify_cell(cell,current,field)
    except ValueError as exc:
        if str(exc)=='COMPARISON_GROWTH_CAP':return None,'CERTIFICATE_COMPARISON_GROWTH_CAP',cell,None,None
        raise
    if not report['closed']:return None,'PHASE_TUBE_NOT_CLOSED',cell,report,None
    whole=[proof.interval(x) for x in report['whole_state']];vals=phase_values(m.I(now,end),whole,t)
    if settings()['phase_turn']['require_direct_guard_every_cell'] and vals['guard_margin'].lo<=0:
        return None,'DIRECT_GUARD_MARGIN_NOT_SEPARATED',cell,report,vals
    pi=m.C['pi']
    # Prove the whole interval lies inside (-pi,+pi) for every admissible
    # true pi in the source-constant enclosure.  pi.lo is the strict side.
    if whole[0].lo<=-pi.lo or whole[0].hi>=pi.lo:
        return None,'PHASE_DOMAIN_NOT_SEPARATED',cell,report,vals
    accepted={'a0':str(now),'a1':str(end),'input':cell,'certificate':report,
              'phase':{k:_pairs(vals[k]) for k in ('U','Utheta','e','H','theta_u','y_u','guard_margin','guard_ratio')}}
    return accepted,None,cell,report,vals


def phase_turn_trajectory(parent):
    splice,current,t,row=verify_splice(parent);ss=settings()['phase_turn'];now=F(splice['a1']);target=F(ss['target_a']);step=F(ss['relative_step'])
    cells=[];attempts=0;blocker=None;event_start=None;event_cells=[];start=time.monotonic();deadline=start+ss['case_seconds']
    while now<target and len(cells)<ss['max_cells'] and time.monotonic()<deadline:
        candidate=min(target,now*(1+step));accepted=None;reason='NO_ATTEMPT'
        for _ in range(ss['max_halvings']+1):
            attempts+=1;accepted,reason,_,_,vals=_phase_cell(now,candidate,current,t)
            if accepted is not None:
                whole=[proof.interval(x) for x in accepted['certificate']['whole_state']]
                endpoint=[proof.interval(x) for x in accepted['certificate']['endpoint']]
                if event_start is None:
                    if whole[1].lo>0:
                        # Entire certified cell is strictly before the first y=0 turn.
                        pass
                    else:
                        # Enter the event bracket only when the whole cell is on the negative-theta
                        # restoring branch and y is rigorously decreasing throughout the cell.
                        if whole[0].hi<0 and vals['y_u'].hi<0 and current[1].lo>0:
                            event_start=len(cells)
                        else:
                            accepted=None;reason='TURN_EVENT_MONOTONICITY_NOT_SEPARATED'
                else:
                    if not (whole[0].hi<0 and vals['y_u'].hi<0):
                        accepted=None;reason='TURN_EVENT_MONOTONICITY_LOST'
                if accepted is not None:break
            candidate=(now+candidate)/2
        if accepted is None:
            blocker=reason;break
        cells.append(accepted);current=[proof.interval(x) for x in accepted['certificate']['endpoint']];now=F(accepted['a1'])
        if event_start is not None:
            event_cells=cells[event_start:]
            # Starting endpoint before event bracket is strictly positive.  Once the
            # certified endpoint is entirely negative, every admitted trajectory has
            # crossed exactly once because y_u<0 throughout the bracket.
            if current[1].hi<0:
                break
    if event_start is None and blocker is None and now<target:
        blocker='WORK_CAP' if len(cells)>=ss['max_cells'] else 'WALL_TIME_CAP'
    if event_start is None and now>=target: blocker='TURN_NOT_BRACKETED_BEFORE_TRANSFER'
    if event_start is not None and current[1].hi>=0 and blocker is None:
        blocker='TURN_NOT_FULLY_CROSSED' if now>=target else ('WORK_CAP' if len(cells)>=ss['max_cells'] else 'WALL_TIME_CAP')
    status='UNRESOLVED_BOUNDED_OBSTRUCTION';event=None;threshold=None
    if event_start is not None and current[1].hi<0:
        event_cells=cells[event_start:]
        first=event_cells[0];last=event_cells[-1]
        prior_y=proof.interval(cells[event_start-1]['certificate']['endpoint'][1]) if event_start>0 else proof.interval(splice['y_endpoint'])
        fail(prior_y.lo>0,'TURN_PRIOR_SIGN')
        theta_whole=[proof.interval(c['certificate']['whole_state'][0]) for c in event_cells]
        theta_hull=m.I(min(x.lo for x in theta_whole),max(x.hi for x in theta_whole))
        Uturn,_,cc=theta_potential(theta_hull,t)
        energy=v6.energy_certificate(row,t);base_transfer=m.I(*map(F,energy['base_at_transfer']));threshold=m.I(3*base_transfer.lo+cc['floor'].lo,3*base_transfer.hi+cc['floor'].hi)
        threshold_pass=Uturn.hi<threshold.lo
        event={'a_bracket':[first['a0'],last['a1']],
               'z_bracket_orientation':[str(float(1/F(last['a1'])-1)),str(float(1/F(first['a0'])-1))],
               'theta_at_event_enclosure':_pairs(theta_hull),'turn_energy_e':_pairs(Uturn),
               'pre_event_y':_pairs(prior_y),'post_event_y':_pairs(current[1]),
               'unique_crossing_gate':'PASS' if all(F(c['phase']['y_u'][1])<0 for c in event_cells) else'FAIL',
               'direction':'X_NEGATIVE_TO_X_POSITIVE','threshold':_pairs(threshold),
               'post_anchor_test':'PASS' if threshold_pass else'FAIL'}
        fail(event['unique_crossing_gate']=='PASS','TURN_UNIQUENESS_RECHECK')
        if threshold_pass:
            status='PASS_CONDITIONAL_PHASE_TURN_GUARD';blocker=None
        else:blocker='TURN_ENERGY_ABOVE_POST_ANCHOR_THRESHOLD'
    margins=[F(c['phase']['guard_margin'][0]) for c in cells]
    return {'method':ss['method'],'state_coordinates':ss['state_coordinates'],'status':status,'splice':splice,
            'requested_end_a':str(target),'certified_end_a':str(now),'cells':cells,'cell_count':len(cells),'attempts':attempts,
            'endpoint':list(map(_pairs,current)),'event_start_cell':event_start,'turn_event':event,'blocker':blocker,
            'minimum_phase_guard_margin_lower':str(min(margins)) if margins else None,
            'transfer_threshold':None if threshold is None else _pairs(threshold),
            'actual_source_admission':'UNRESOLVED'}


def _energy_bg_cap(a0,a1,t,total_energy_upper):
    base=v7._background_base(m.I(a0,a1),t);cc=phase_constants(t)
    E=m.I(cc['floor'].lo,total_energy_upper)
    H=m.sqrt_i(pre.square(base['H'])+E/3)
    return {'H':H,'Hs':H*m.C['c']/m.C['Mpc'],'rho_gamma':base['rho_gamma']},E


def thermal_continuation(row,t,phase_turn):
    if phase_turn['status']!='PASS_CONDITIONAL_PHASE_TURN_GUARD':
        return {'status':'UNRESOLVED_GUARD_INCOMPLETE','cells':[],'h_entry_q':'NOT_COMPUTED','blocker':'PHASE_TURN_GUARD_REQUIRED'}
    parent=v6.parent_checkpoint('camspec-ede_n3');v6ext=v6.derive('camspec-ede_n3',parent);current=proof.interval(v6ext['phase']['endpoint'])
    fail(current.lo>0,'V6_POSITIVE_ENDPOINT_REQUIRED')
    old_cap=F(v6ext['energy']['energy_upper']);event=phase_turn['turn_event'];event_end=F(event['a_bracket'][1]);turn_e_hi=F(event['turn_energy_e'][1]);cc=phase_constants(t);tight_cap=turn_e_hi+cc['floor'].hi
    fail(tight_cap<old_cap,'POST_TURN_CAP_NOT_TIGHTER')
    start,switch,end=F(1,4601),F(1,3551),F(1,2871);step=F(settings()['thermal']['relative_step']);cells=[];transition=None;now=start
    while now<end:
        phase_end=switch if now<switch else end
        cap_switch=event_end if now<event_end<phase_end else phase_end
        target=cap_switch
        mode='He1f' if now<switch else'He2'
        while now<target:
            a1=min(target,now*(1+step));cap=old_cap if a1<=event_end else tight_cap
            bg,E=_energy_bg_cap(now,a1,t,cap);new,rep=v7.advance_w(mode,now,a1,current,t,bg)
            rep=copy.deepcopy(rep);rep['background_energy_cap']=_pairs(E);rep['energy_cap_regime']='PRE_TURN_V6' if cap==old_cap else'POST_TURN_TIGHT'
            cells.append(rep);current=new;now=a1
        if now==event_end and now<phase_end:
            # Continue same thermal mode immediately with the tightened post-turn cap.
            continue
        if now==switch:
            bg,_=_energy_bg_cap(switch,switch,t,tight_cap if switch>=event_end else old_cap)
            transition=v7.saha_transition_control(switch,current,t,bg)
    fail(now==end and transition is not None,'THERMAL_BOUNDARIES')
    q=pre.onset(current,m.I(end),t)
    return {'status':'PASS_CONDITIONAL_TO_H_ENTRY','method':settings()['thermal']['method'],'independent_method':settings()['thermal']['independent_method'],
            'start_a':'1/4601','end_a':'1/2871','start_w':v6ext['phase']['endpoint'],'endpoint_w':_pairs(current),'h_entry_q':_pairs(q),
            'pre_turn_total_energy_upper':str(old_cap),'post_turn_total_energy_upper':str(tight_cap),'turn_event_end_a':str(event_end),
            'cells':cells,'saha_transition':transition,'actual_source_admission':'UNRESOLVED'}


def derive(parent):
    validate_sources();parent=load_parent(parent) if not isinstance(parent,dict) else copy.deepcopy(parent)
    phase=phase_turn_trajectory(parent);row=v6.config()['cases']['camspec-ede_n3'];t=p.parameters(row);thermal=thermal_continuation(row,t,phase)
    return {'q':Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':ID,'version':VERSION,'scope':SCOPE,
            'scientific_question':settings()['scientific_question'],'question_sha256':settings()['question_sha256'],'source_commit':SOURCE,
            'configuration':'camspec-ede_n3','parent_v7_run_id':settings()['parent_v7']['run_id'],'parent_v7_raw_sha256':settings()['parent_v7']['raw_sha256'],
            'phase_turn':phase,'thermal':thermal,'retained_parent_hillipop':copy.deepcopy(parent['records']['hillipop-ede_n3']),
            'retained_parent_lcdm':copy.deepcopy(parent['retained_lcdm']),
            'actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'final_result_gate':'UNRESOLVED','return_route':'RESULT INGESTION & ROUTING ENGINE'}


def verify_phase_turn(obj,parent):
    # Independent full recomputation of the new V8 proof object.  V7 is admitted
    # only through the exact parent artifact plus the one reverified splice cell.
    expected=phase_turn_trajectory(parent)
    fail(obj==expected,'PHASE_TURN_RECOMPUTATION_MISMATCH')
    return {'gate':'PASS_RECOMPUTED_PHASE_TURN','status':obj['status'],'cells':obj['cell_count']}


def verify_thermal(obj,parent,phase):
    row=v6.config()['cases']['camspec-ede_n3'];t=p.parameters(row);expected=thermal_continuation(row,t,phase)
    fail(obj==expected,'THERMAL_RECOMPUTATION_MISMATCH')
    return {'gate':'PASS_RECOMPUTED_THERMAL','status':obj['status'],'cells':len(obj['cells'])}


def verify_extension(obj,parent):
    parent=load_parent(parent) if not isinstance(parent,dict) else copy.deepcopy(parent)
    fail(obj['q']==Q and obj['program_id']==ID and obj['version']==VERSION and obj['configuration']=='camspec-ede_n3','EXTENSION_IDENTITY')
    fail(obj['source_commit']==SOURCE and obj['question_sha256']==settings()['question_sha256'],'EXTENSION_SOURCE')
    fail(obj['actual_source_admission']=='UNRESOLVED' and obj['final_result_gate']=='UNRESOLVED','EXTENSION_SCOPE')
    fail(all(obj[k]=='NOT_COMPUTED' for k in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds')),'EXTENSION_FULL_PRODUCTS')
    phase=verify_phase_turn(obj['phase_turn'],parent);thermal=verify_thermal(obj['thermal'],parent,obj['phase_turn'])
    fail(obj['retained_parent_hillipop']==parent['records']['hillipop-ede_n3'] and obj['retained_parent_lcdm']==parent['retained_lcdm'],'RETAINED_PARENT_CHANGED')
    return {'gate':'PASS_RECOMPUTED_V8_EXTENSION','phase_turn':phase,'thermal':thermal}
