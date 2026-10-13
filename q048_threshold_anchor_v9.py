"""Q048 V9: finite correlation-preserving threshold-anchor certificate.

Scientific scope is deliberately narrow.  V9 does not extend the V8
rectangular (theta,y) trajectory.  It uses Mathematics-009 to prove, by two
finite outward calculations, that every admitted Camspec source-real trajectory
must acquire a scalar-energy anchor e<T no later than the independently safe V6
guard horizon.  It then combines that existence result with the already-proved
Mathematics-008 post-anchor lemma and recomputes only the sign-aware Camspec
He1f/He2 thermal continuation to conditional H-entry.

The certificate is artifact-bound to official V6/V7/V8 runs and uses V8 only
for the rigorously reverified splice plus one accepted witness cell.  The core
new proof is a 32-bin phase-energy comparison map and a 32-bin timing upper sum.

This program does NOT qualify native floating-point/source-instance identity,
does NOT locate the shared helium q=1e-6 cutoff, and does NOT compute complete
latch/reset x_e(z) or tau_T(z) histories.
"""
from pathlib import Path
from fractions import Fraction as F
import copy, hashlib, json

import q048_phase_turn_v8 as v8

v7=v8.v7
v6=v8.v6
old=v8.old
p=v8.p
m=v8.m
pre=v8.pre
proof=v8.proof

ROOT=Path(__file__).resolve().parent
ID='Q048-THRESHOLD-V9'
VERSION='v9'
Q='Q-048'
SOURCE='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
SCOPE='CONDITIONAL_SOURCE_REAL_THRESHOLD_ANCHOR_GUARD_THERMAL'
CONFIG_SHA='5a32d9ce2c4dafef8c91ab9c7830ee8c2f977e8f894bb1c4602dd4eaa148499d'


def fail(condition,message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def git_blob_sha1(path):
    b=Path(path).read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def _pairs(x):
    return proof.pairs(x)


def settings():
    s=old.load(ROOT/'q048_threshold_anchor_config_v9.json')
    fail(sha256(ROOT/'q048_threshold_anchor_config_v9.json')==CONFIG_SHA,'CONFIG_HASH')
    fail(s['program_id']==ID and s['q']==Q and s['version']==VERSION,'CONFIG_IDENTITY')
    fail(s['source_commit']==SOURCE and s['scope']==SCOPE,'CONFIG_SOURCE_SCOPE')
    fail(s['question_sha256']==v6.config()['question_sha256'],'QUESTION_HASH')
    return s


def validate_sources():
    s=settings()
    # V6 validation is journal-independent and preserves the frozen source
    # implementation.  V7/V8 validate_sources are intentionally not called,
    # because those historical versions pin older journal snapshots.
    v6.validate_sources()
    for name,want in s['reused_git_blob_sha1'].items():
        fail(git_blob_sha1(ROOT/name)==want,'REUSED_GIT_BLOB '+name)
    fail(sha256(ROOT/s['math009_md'])==s['math009_md_sha256'],'MATH009_MD_HASH')
    fail(sha256(ROOT/s['math009_json'])==s['math009_json_sha256'],'MATH009_JSON_HASH')
    fail(sha256(ROOT/s['journal_file'])==s['journal_sha256'],'JOURNAL_HASH')
    mj=old.load(ROOT/s['math009_json'])
    fail(mj['q']==Q and mj['question_sha256']==s['question_sha256'],'MATH009_IDENTITY')
    fail(mj['source_commit']==SOURCE and mj['method_name']=='source_root_phase_threshold_anchor_v1','MATH009_METHOD')
    fail(mj['orientation_is_certificate'] is False and mj['final_result_gate']=='UNRESOLVED','MATH009_SCOPE')
    return s


def _load_json_exact(path,size_cap,raw_hash,error_prefix):
    path=Path(path)
    fail(path.is_file(),error_prefix+'_FILE_MISSING')
    fail(path.stat().st_size<=size_cap,error_prefix+'_SIZE_CAP')
    fail(sha256(path)==raw_hash,error_prefix+'_RAW_HASH')
    try:
        with path.open('r',encoding='utf-8') as f:
            return json.load(f)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise ValueError(error_prefix+'_JSON') from exc


def load_v6(path):
    s=settings()['parent_v6']
    obj=_load_json_exact(path,32_000_000,s['raw_sha256'],'PARENT_V6')
    fail(obj.get('schema')=='Q048_STRUCTURAL_FINAL_V6' and obj.get('program_id')=='Q048-STRUCTURAL-V6','PARENT_V6_IDENTITY')
    fail(obj.get('source_commit')==SOURCE and obj.get('question_sha256')==settings()['question_sha256'],'PARENT_V6_SOURCE')
    fail(obj.get('execution_status')=='COMPLETE' and obj.get('job_completeness_gate')=='PASS' and obj.get('merge_compatibility_gate')=='PASS','PARENT_V6_COMPLETENESS')
    c=obj['records']['camspec-ede_n3']
    fail(c['run_id']==s['run_id'] and c['executed_commit']==s['executed_commit'] and c['config_hash']==s['config_hash'],'PARENT_V6_RUN_BINDING')
    fail(c['tests_status']=='COMPLETE_CONDITIONAL' and c['post_verification']['gate']=='PASS_CONDITIONAL_RECOMPUTED','PARENT_V6_VALIDATION')
    return obj


def load_v7(path):
    s=settings()['parent_v7']
    obj=_load_json_exact(path,64_000_000,s['raw_sha256'],'PARENT_V7')
    # Reuse the exact V8 parent validator, which does not invoke the old
    # journal-bound V7 source-validation suite.
    validated=v8.load_parent(path)
    fail(validated==obj,'PARENT_V7_RELOAD')
    return obj


def load_v8(path):
    s=settings()['parent_v8']
    obj=_load_json_exact(path,32_000_000,s['raw_sha256'],'PARENT_V8')
    fail(obj.get('schema')=='Q048_PHASE_TURN_FINAL_V8' and obj.get('program_id')=='Q048-PHASETURN-V8','PARENT_V8_IDENTITY')
    fail(obj.get('source_commit')==SOURCE and obj.get('question_sha256')==settings()['question_sha256'],'PARENT_V8_SOURCE')
    fail(obj.get('execution_status')=='COMPLETE' and obj.get('job_completeness_gate')=='PASS' and obj.get('merge_compatibility_gate')=='PASS','PARENT_V8_COMPLETENESS')
    fail(obj.get('tests_status')=='COMPLETE_CONDITIONAL' and obj.get('final_result_gate')=='UNRESOLVED','PARENT_V8_SCOPE')
    r=obj['camspec_record']
    fail(r['run_id']==str(s['run_id']) and r['executed_commit']==s['executed_commit'] and r['config_hash']==s['config_hash'],'PARENT_V8_RUN_BINDING')
    fail(r.get('post_verification',{}).get('gate')=='PASS_RECOMPUTED_V8_EXTENSION','PARENT_V8_VALIDATION')
    fail(r['extension']['phase_turn']['status']=='UNRESOLVED_BOUNDED_OBSTRUCTION','PARENT_V8_EXPECTED_STATE')
    fail(r['extension']['phase_turn']['blocker']=='TURN_EVENT_MONOTONICITY_NOT_SEPARATED','PARENT_V8_BLOCKER')
    return obj


def verify_artifact_chain(v6_parent,v7_parent,v8_parent):
    s=settings()
    fail(v8_parent['parent_v7']['run_id']==str(s['parent_v7']['run_id']),'V8_V7_RUN_CHAIN')
    fail(v8_parent['parent_v7']['raw_sha256']==s['parent_v7']['raw_sha256'],'V8_V7_HASH_CHAIN')
    c6=v6_parent['records']['camspec-ede_n3']
    fail(c6['extension']['q']==Q and c6['extension']['source_commit']==SOURCE,'V6_EXTENSION_CHAIN')
    c7=v7_parent['records']['camspec-ede_n3']
    fail(c7['extension']['q']==Q and c7['extension']['source_commit']==SOURCE,'V7_EXTENSION_CHAIN')
    c8=v8_parent['camspec_record']['extension']
    fail(c8['q']==Q and c8['source_commit']==SOURCE,'V8_EXTENSION_CHAIN')
    return {'gate':'PASS_OFFICIAL_V6_V7_V8_CHAIN',
            'v6_run':s['parent_v6']['run_id'],'v7_run':s['parent_v7']['run_id'],'v8_run':s['parent_v8']['run_id']}


def reverify_witness(v7_parent,v8_parent):
    ss=settings()['witness']
    splice,current,t,row=v8.verify_splice(v7_parent)
    stored_phase=v8_parent['camspec_record']['extension']['phase_turn']
    fail(splice==stored_phase['splice'],'V8_SPLICE_PAYLOAD_BINDING')
    cells=stored_phase['cells'];idx=ss['v8_cell_zero_based']
    fail(len(cells)>idx and idx>0,'V8_WITNESS_INDEX')
    fail(stored_phase['cell_count']==len(cells),'V8_CELL_COUNT')
    for i,c in enumerate(cells[:idx]):
        endpoint=[proof.interval(x) for x in c['certificate']['endpoint']]
        fail(endpoint[0].hi>=F(ss['theta_upper_below']),'V8_WITNESS_NOT_FIRST')
    cell=cells[idx];prev=cells[idx-1]
    fail(prev['a1']==cell['a0'],'V8_WITNESS_PARTITION')
    current=[proof.interval(x) for x in prev['certificate']['endpoint']]
    accepted,reason,_,_,_=v8._phase_cell(F(cell['a0']),F(cell['a1']),current,t)
    fail(reason is None and accepted==cell,'V8_WITNESS_RECOMPUTE')
    endpoint=[proof.interval(x) for x in cell['certificate']['endpoint']]
    fail(endpoint[0].hi<F(ss['theta_upper_below']),'V8_WITNESS_THETA')
    fail(endpoint[1].lo>0,'V8_WITNESS_Y_POSITIVE')
    H=proof.interval(cell['phase']['H'])
    fail(H.lo>0,'V8_WITNESS_H')
    return {'gate':'PASS_REVERIFIED_V8_WITNESS',
            'cell_index_zero_based':idx,'a27':cell['a1'],
            'theta_endpoint':cell['certificate']['endpoint'][0],
            'y_endpoint':cell['certificate']['endpoint'][1],
            'H_whole':cell['phase']['H'],
            'stored_cell_sha256':old.objhash(cell),
            'splice':splice},t,row


def threshold_constants(v6_parent,t):
    c=settings()['certificate']
    rec=v6_parent['records']['camspec-ede_n3']['extension']['energy']
    live=v6.energy_certificate(v6.config()['cases']['camspec-ede_n3'],t)
    for key in ('potential_floor','base_at_transfer','guard_certified_to_a','guard_bracket_a','energy_upper'):
        fail(live[key]==rec[key],'V6_ENERGY_RECOMPUTE '+key)
    cc=v8.phase_constants(t)
    floor_art=proof.interval(rec['potential_floor'])
    fail(_pairs(cc['floor'])==rec['potential_floor'],'V6_FLOOR_BINDING')
    base=proof.interval(rec['base_at_transfer'])
    T=3*base.lo+cc['floor'].lo
    fail(T>0 and cc['lambda'].lo>0 and cc['A'].lo>0,'THRESHOLD_CONSTANT_DOMAIN')
    return {'T':T,'base_transfer':base,'floor':cc['floor'],'lambda':cc['lambda'],'A':cc['A'],
            'safe_a':F(rec['guard_certified_to_a']),'old_total_energy_upper':F(rec['energy_upper']),
            'phase_start':F(c['energy_phase_start']),'phase_end':F(c['energy_phase_end'])}


def potential_cap(abs_theta,t):
    abs_theta=F(abs_theta)
    fail(abs_theta>=0 and abs_theta<m.C['pi'].lo,'POTENTIAL_CAP_PHASE_DOMAIN')
    U,_,_=v8.theta_potential(m.I(abs_theta),t)
    return U


def static_threshold_gates(constants,t):
    T=constants['T'];out={}
    for label,value in [('2.1',F(21,10)),('2',F(2)),('1',F(1))]:
        U=potential_cap(value,t)
        fail(U.hi<T,'STATIC_POTENTIAL_THRESHOLD_'+label)
        out[label]={'U':_pairs(U),'margin_lower':str(T-U.hi)}
    return {'gate':'PASS_STATIC_THRESHOLD_GATES','values':out}


def _tanh_interval(x):
    x=m.iv(x)
    fail(x.lo>=0,'TANH_NONNEGATIVE_DOMAIN')
    e=m.exp_i(2*x)
    return (e-1)/(e+1)


def energy_map(constants,t,E0,bins=None):
    c=settings()['certificate'];bins=int(bins or c['energy_bins'])
    start=F(c['energy_phase_start']);end=F(c['energy_phase_end'])
    fail(start>end and bins>=1,'ENERGY_MAP_PARTITION_DOMAIN')
    h=(start-end)/bins;T=constants['T'];lam_hi=constants['lambda'].hi
    sqrt6=m.sqrt_i(m.I(6))
    d=sqrt6*m.I(h)/(2*lam_hi)
    tanh_d=_tanh_interval(d)
    # Smaller d/tanh means less certified energy decrease, hence is the
    # conservative choice for an upper envelope.
    tlo=tanh_d.lo
    Ehi=F(E0);fail(Ehi>T,'ENERGY_MAP_START_ABOVE_THRESHOLD')
    steps=[];early=None
    for j in range(bins):
        right=start-j*h;left=right-h
        r=max(abs(left),abs(right))
        U=potential_cap(r,t);Uhi=U.hi
        fail(Uhi<T,'ENERGY_BIN_POTENTIAL_BELOW_T')
        if Ehi<=T:
            early=j;break
        fail(Ehi>Uhi,'ENERGY_BIN_REAL_SQRT')
        w2=(Ehi-Uhi)/(Ehi+T);fail(0<w2<1,'ENERGY_BIN_W2_DOMAIN')
        w=m.sqrt_i(m.I(w2))
        if w.hi<=tlo:
            early=j
            Ehi=Uhi
            steps.append({'bin':j,'theta_hi':str(right),'theta_lo':str(left),'U_cap':_pairs(U),
                          'E_in_upper':str((Uhi+T*w.hi*w.hi)/(1-w.hi*w.hi)),
                          'threshold_reached_inside_bin':True})
            break
        num=w.hi-tlo;den=1-w.hi*tlo
        fail(num>0 and den>0,'ENERGY_BIN_MOBIUS_DOMAIN')
        wn=num/den;fail(0<wn<1,'ENERGY_BIN_WNEW_DOMAIN')
        Enew=(Uhi+T*wn*wn)/(1-wn*wn)
        fail(Enew<Ehi,'ENERGY_BIN_MONOTONE')
        steps.append({'bin':j,'theta_hi':str(right),'theta_lo':str(left),'U_cap':_pairs(U),
                      'E_in_upper':str(Ehi),'w_upper':str(w.hi),'tanh_d_lower':str(tlo),
                      'E_out_upper':str(Enew),'threshold_reached_inside_bin':False})
        Ehi=Enew
    passed=Ehi<T
    return {'gate':'PASS_ENERGY_MAP' if passed else'UNRESOLVED_ENERGY_MAP',
            'bins_requested':bins,'bins_completed':len(steps),'phase_start':str(start),'phase_end':str(end),
            'width':str(h),'T_lower':str(T),'tanh_d':_pairs(tanh_d),'steps':steps,
            'final_E_upper':str(Ehi),'margin_lower':str(T-Ehi),'early_threshold_bin':early}


def _log_lower_gt_one(x,terms):
    x=F(x);fail(x>1,'LOG_RATIO_NOT_GT_ONE')
    y=(x-1)/(x+1);fail(0<y<1,'LOG_ATANH_DOMAIN')
    y2=y*y;power=y;s=F(0)
    for k in range(terms):
        s += power/F(2*k+1)
        power *= y2
    return 2*s


def timing_sum(constants,witness,t,bins=None):
    c=settings()['certificate'];bins=int(bins or c['timing_bins'])
    lo=F(c['timing_phase_low']);hi=F(c['timing_phase_high']);fail(hi>lo,'TIMING_PARTITION_DOMAIN')
    h=(hi-lo)/bins;T=constants['T'];Hhi=F(witness['H_whole'][1]);lam_lo=constants['lambda'].lo
    fail(Hhi>0 and lam_lo>0,'TIMING_CONSTANT_DOMAIN')
    s=F(0);steps=[]
    for j in range(bins):
        left=lo+j*h;right=left+h;r=max(abs(left),abs(right))
        U=potential_cap(r,t);Uhi=U.hi;fail(Uhi<T,'TIMING_BIN_POTENTIAL_BELOW_T')
        denom=2*(T-Uhi);root=m.sqrt_i(m.I(denom));fail(root.lo>0,'TIMING_BIN_ROOT')
        term=h/root.lo;s+=term
        steps.append({'bin':j,'theta_lo':str(left),'theta_hi':str(right),'U_cap':_pairs(U),
                      'sqrt_lower':str(root.lo),'integral_term_upper':str(term)})
    J=Hhi/lam_lo*s
    a27=F(witness['a27']);safe=constants['safe_a'];fail(safe>a27,'TIMING_SAFE_AFTER_WITNESS')
    ratio=safe/a27;terms=int(c['log_series_terms'])
    loglo=_log_lower_gt_one(ratio,terms)
    passed=J<loglo
    return {'gate':'PASS_TIMING_SUM' if passed else'UNRESOLVED_TIMING_SUM',
            'bins':bins,'phase_low':str(lo),'phase_high':str(hi),'width':str(h),
            'H27_upper':str(Hhi),'lambda_lower':str(lam_lo),'integral_upper':str(s),
            'J_upper':str(J),'a27':str(a27),'safe_a':str(safe),'ratio':str(ratio),
            'log_series_terms':terms,'delta_u_safe_lower':str(loglo),'margin_lower':str(loglo-J)}


def finite_certificate(v6_parent,v7_parent,v8_parent):
    chain=verify_artifact_chain(v6_parent,v7_parent,v8_parent)
    witness,t,row=reverify_witness(v7_parent,v8_parent)
    constants=threshold_constants(v6_parent,t)
    static=static_threshold_gates(constants,t)
    E0=F(witness['splice']['e_endpoint'][1])
    energy=energy_map(constants,t,E0)
    timing=timing_sum(constants,witness,t)
    # A finer partition is an independent implementation-level control, not a
    # replacement acceptance criterion.
    refine_bins=int(settings()['certificate']['refinement_bins'])
    energy_ref=energy_map(constants,t,E0,refine_bins)
    timing_ref=timing_sum(constants,witness,t,refine_bins)
    if energy['gate']=='PASS_ENERGY_MAP':
        fail(energy_ref['gate']=='PASS_ENERGY_MAP','ENERGY_REFINEMENT_CONTROL')
        fail(F(energy_ref['final_E_upper'])<=F(energy['final_E_upper']),'ENERGY_REFINEMENT_DIRECTION')
    if timing['gate']=='PASS_TIMING_SUM':
        fail(timing_ref['gate']=='PASS_TIMING_SUM','TIMING_REFINEMENT_CONTROL')
        fail(F(timing_ref['J_upper'])<=F(timing['J_upper']),'TIMING_REFINEMENT_DIRECTION')
    if energy['gate']!='PASS_ENERGY_MAP':
        status='UNRESOLVED_BOUNDED_OBSTRUCTION';blocker='ENERGY_MAP_NOT_BELOW_THRESHOLD'
    elif timing['gate']!='PASS_TIMING_SUM':
        status='UNRESOLVED_BOUNDED_OBSTRUCTION';blocker='TIMING_SUM_NOT_BEFORE_SAFE_HORIZON'
    else:
        status='PASS_CONDITIONAL_THRESHOLD_ANCHOR_GUARD';blocker=None
    return {'method':'source_root_phase_threshold_anchor_v1','status':status,'artifact_chain':chain,
            'witness':witness,'threshold':{'T_lower':str(constants['T']),'base_transfer':_pairs(constants['base_transfer']),
            'floor':_pairs(constants['floor']),'lambda':_pairs(constants['lambda']),'A':_pairs(constants['A']),
            'safe_a':str(constants['safe_a']),'old_total_energy_upper':str(constants['old_total_energy_upper'])},
            'static_gates':static,'energy_map_32':energy,'timing_sum_32':timing,
            'refinement_control':{'bins':refine_bins,'energy':{k:energy_ref[k] for k in ('gate','final_E_upper','margin_lower')},
                                  'timing':{k:timing_ref[k] for k in ('gate','J_upper','delta_u_safe_lower','margin_lower')}},
            'theorem_gate':'PASS_THRESHOLD_OR_TURN_EXISTENCE_BEFORE_V6_SAFE_HORIZON' if status.startswith('PASS') else'UNRESOLVED',
            'guard_consequence':'PASS_CONDITIONAL_SOURCE_GUARD_TO_Z2870' if status.startswith('PASS') else'UNRESOLVED',
            'blocker':blocker,'actual_anchor_redshift':'NOT_LOCALIZED_AND_NOT_REQUIRED',
            'actual_source_admission':'UNRESOLVED'},constants,t,row


def _energy_bg_cap(a0,a1,t,total_upper):
    base=v7._background_base(m.I(a0,a1),t)
    cc=v8.phase_constants(t)
    E=m.I(cc['floor'].lo,total_upper)
    H=m.sqrt_i(pre.square(base['H'])+E/3)
    return {'H':H,'Hs':H*m.C['c']/m.C['Mpc'],'rho_gamma':base['rho_gamma']}


def thermal_continuation(v6_parent,certificate,constants,t):
    if certificate['status']!='PASS_CONDITIONAL_THRESHOLD_ANCHOR_GUARD':
        return {'status':'UNRESOLVED_GUARD_INCOMPLETE','cells':[],'h_entry_q':'NOT_COMPUTED',
                'blocker':'MATHEMATICS_009_CERTIFICATE_REQUIRED'}
    rec=v6_parent['records']['camspec-ede_n3']['extension']
    current=proof.interval(rec['phase']['endpoint']);fail(current.lo>0,'V6_POSITIVE_ENDPOINT_REQUIRED')
    start=F(1,4601);switch=F(1,3551);end=F(1,2871);safe=constants['safe_a']
    fail(start<safe<switch<end,'THERMAL_SAFE_HORIZON_ORDER')
    old_cap=constants['old_total_energy_upper']
    tight_cap=constants['T']+constants['floor'].hi
    fail(tight_cap<old_cap,'POST_ANCHOR_CAP_NOT_TIGHTER')
    step=F(settings()['thermal']['relative_step']);cells=[];now=start
    while now<end:
        mode='He1f' if now<switch else'He2'
        milestone=safe if now<safe else (switch if now<switch else end)
        nxt=min(milestone,now*(1+step))
        cap=old_cap if nxt<=safe else tight_cap
        bg=_energy_bg_cap(now,nxt,t,cap)
        current,rep=v7.advance_w(mode,now,nxt,current,t,bg)
        rep=copy.deepcopy(rep);rep['energy_cap_upper']=str(cap)
        rep['energy_cap_regime']='V6_PRE_ANCHOR' if nxt<=safe else'MATH009_POST_ANCHOR'
        cells.append(rep);now=nxt
    fail(now==end,'THERMAL_END')
    bg=_energy_bg_cap(switch,switch,t,tight_cap)
    transition=v7.saha_transition_control(switch,proof.interval(next(c['endpoint'] for c in cells if F(c['a1'])==switch)),t,bg)
    q=pre.onset(current,m.I(end),t)
    return {'status':'PASS_CONDITIONAL_TO_H_ENTRY',
            'method':'sign_aware_positive_voc_v1_with_v6_pre_anchor_and_math009_post_anchor_energy_caps',
            'independent_method':v7.settings()['thermal']['independent_method'],
            'start_a':str(start),'safe_a':str(safe),'switch_a':str(switch),'end_a':str(end),
            'start_w':rec['phase']['endpoint'],'endpoint_w':_pairs(current),'h_entry_q':_pairs(q),
            'old_energy_cap_upper':str(old_cap),'post_anchor_total_energy_cap_upper':str(tight_cap),
            'cells':cells,'saha_transition':transition,'actual_source_admission':'UNRESOLVED'}


def derive(v6_parent,v7_parent,v8_parent):
    cert,constants,t,row=finite_certificate(v6_parent,v7_parent,v8_parent)
    thermal=thermal_continuation(v6_parent,cert,constants,t)
    return {'q':Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':ID,'version':VERSION,
            'scope':SCOPE,'scientific_question':settings()['scientific_question'],'question_sha256':settings()['question_sha256'],
            'source_commit':SOURCE,'configuration':'camspec-ede_n3','certificate':cert,'thermal':thermal,
            'retained_parent_hillipop':copy.deepcopy(v8_parent['retained_parent_hillipop']),
            'retained_parent_lcdm':copy.deepcopy(v8_parent['retained_parent_lcdm']),
            'actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED',
            'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
            'final_result_gate':'UNRESOLVED','return_route':'RESULT INGESTION & ROUTING ENGINE'}


def verify_thermal(v6_parent,certificate,stored):
    constants={'T':F(certificate['threshold']['T_lower']),
               'safe_a':F(certificate['threshold']['safe_a']),
               'old_total_energy_upper':F(certificate['threshold']['old_total_energy_upper']),
               'floor':proof.interval(certificate['threshold']['floor'])}
    # Recover frozen source parameters without using a new numerical trajectory.
    row=v6.config()['cases']['camspec-ede_n3'];t=p.parameters(row)
    recomputed=thermal_continuation(v6_parent,certificate,constants,t)
    fail(recomputed==stored,'THERMAL_RECOMPUTE')
    return {'gate':'PASS_RECOMPUTED_THERMAL','status':stored['status'],'cells':len(stored['cells']),
            'h_entry_q':stored['h_entry_q']}


def verify_extension(obj,v6_parent,v7_parent,v8_parent):
    fail(obj['q']==Q and obj['program_id']==ID and obj['scope']==SCOPE,'VERIFY_IDENTITY')
    fail(obj['question_sha256']==settings()['question_sha256'] and obj['source_commit']==SOURCE,'VERIFY_SOURCE')
    cert,_,_,_=finite_certificate(v6_parent,v7_parent,v8_parent)
    fail(cert==obj['certificate'],'CERTIFICATE_RECOMPUTE')
    thermal=verify_thermal(v6_parent,cert,obj['thermal'])
    fail(obj['actual_source_admission']=='UNRESOLVED' and obj['final_result_gate']=='UNRESOLVED','VERIFY_SCOPE')
    fail(obj['actual_event_redshift']=='NOT_COMPUTED' and obj['actual_xe_history_bounds']=='NOT_COMPUTED' and obj['actual_tau_T_bounds']=='NOT_COMPUTED','VERIFY_FULL_PRODUCTS')
    return {'gate':'PASS_RECOMPUTED_V9_EXTENSION',
            'certificate':{'gate':'PASS_RECOMPUTED_FINITE_CERTIFICATE','status':cert['status']},
            'thermal':thermal}
