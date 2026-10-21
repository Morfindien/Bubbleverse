"""Independent V141 verifier; does not import or invoke producer."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,copy
ROOT=Path(__file__).resolve().parent; SPEC=json.loads((ROOT/'Q048_V141_SPEC_V1.json').read_text()); IROOT=ROOT/SPEC['helper_root']; sys.path.insert(0,str(IROOT))
import q047_math_v1 as m
import q048_prefix_v1 as prefix
import q048_full_tube_reuse_v1 as tube
import q048_p3_scaled_kernel_v2 as k
def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def enc(x):
    if isinstance(x,(m.I,k.I)): return {'lo':str(x.lo),'hi':str(x.hi)}
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {a:enc(b) for a,b in x.items()}
    if isinstance(x,(tuple,list)): return [enc(v) for v in x]
    return x
def eq(x,y): return x==enc(y)
def reconstruct():
    for rel,pn in SPEC['input_pins'].items():
        p=ROOT/rel
        if p.stat().st_size!=pn['bytes'] or sha(p)!=pn['sha256']: raise ValueError('INPUT_PIN:'+rel)
    for rel,pn in SPEC['helper_pins'].items():
        p=IROOT/rel
        if p.stat().st_size!=pn['bytes'] or sha(p)!=pn['sha256']: raise ValueError('HELPER_PIN:'+rel)
    task=read(ROOT/SPEC['task']); parent=read(ROOT/SPEC['parent']); guard=read(IROOT/'q048_guard_local_v_result_v12.json'); cap=read(IROOT/'q048_prefix_config_v1.json')
    if hashlib.sha256(canon(task['task_fingerprint_basis'])).hexdigest()!=task['task_fingerprint']: raise ValueError('FINGERPRINT')
    if hashlib.sha256(cap['scientific_question'].encode()).hexdigest()!=task['question_sha256'] or cap['scientific_question']!=task['exact_full_question']: raise ValueError('QUESTION')
    if sha(ROOT/SPEC['parent'])!=task['parent_checkpoint']['file_sha256'] or parent['actual']!={'count':124,'frontier':840}: raise ValueError('PARENT')
    if parent['endpoint']!=task['parent_checkpoint']['endpoint'] or parent['frontiers']!=task['parent_checkpoint']['frontiers']: raise ValueError('PARENT_PIN')
    if cap['source_commit']!=guard['source_commit'] or cap['source_commit']!=parent['source_commit'] or cap['source_commit']!=task['source_commit']: raise ValueError('SOURCE')
    if sha(IROOT/'q048_prefix_config_v1.json')!=task['capture_sha256'] or guard['capture_sha256']!=task['capture_sha256']: raise ValueError('CAPTURE')
    selected=[]
    for ev in guard['evaluators']:
        rr=[r for r in ev['rows'] if [r['a0'],r['a1']]==['1/841','1/831'] and [r['z0'],r['z1']]==[840,830]]
        if len(rr)!=1: raise ValueError('ROW')
        r=rr[0]
        if r['source_state_reset'] or not all(r[x] for x in ['accepted','committed','whole_cell_qualified']) or not r['domain']['admitted'] or not all(r['domain']['checks'].values()) or F(r['G_lower'])<=0: raise ValueError('GUARD')
        selected.append(r)
    row,control=selected
    if hashlib.sha256(canon(row)).hexdigest()!=task['guard']['primary_row_sha256'] or hashlib.sha256(canon(control)).hexdigest()!=task['guard']['control_row_sha256']: raise ValueError('ROW_HASH')
    if any(F(row[r])!=F(parent['endpoint'][p]) for r,p in [('a0','a'),('E_input_left','E'),('Y_left','Y'),('V_previous','Vbar')]): raise ValueError('GLUE')
    if not 0<F(row['E_safe_left'])<F(row['E_input_left']): raise ValueError('ENERGY')
    prefix.validate_config(cap); case=cap['cases']['hillipop-ede_n3']; par=prefix.parameters(case)
    a=m.I(F(1,841),F(1,831)); w=m.I(F(-1,1000000),F(1,50)); ratio=1-w; hm=F(99999,100000); eps=F(1,1000000)
    B,fl,H,Hs=tube.background(a,par,F(row['E_input_left'])); Hb=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']; n=par['nH0']/a**3*m.const('1e-6'); Tg=par['T0']/a; TR=m.const('8.617343e-5')*Tg
    alpha,rr=tube.load_atomic(IROOT/'q048_p3_scaled_transformed_log_tables_v2.json'); at=tube.local_atomic(alpha,rr,TR,ratio)
    A=[m.I(x.lo,x.hi) for x in at['Alpha']]; Ae=[m.I(x.lo,x.hi) for x in at['Alpha_eq']]; R=m.I(at['R2p2s'].lo,at['R2p2s'].hi)
    raw3=read(IROOT/'q048_p3_scaled_raw_result_v2.json'); init=raw3['initialized_cases']['hillipop-ede_n3']; params={key:k.I(F(v['lo']),F(v['hi'])) for key,v in init.items() if isinstance(v,dict) and 'lo' in v}
    fit=k.fit_admission(k.load_fit(IROOT/'source/fit_swift.dat'),params,k.norm_certificate()); fd=m.I(fit['primary_denominator'].lo,fit['primary_denominator'].hi)
    thermal=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR); s=thermal*m.exp_i(-m.const('13.598286071938324')/TR)/n; ph=thermal*m.exp_i(-m.const('.25')*m.const('13.598286071938324')/TR); b=[Ae[0]*ph,Ae[1]*ph/3]
    coords={mode:k.rate_coordinates(k.I(TR.lo,TR.hi),k.I(ratio.lo,ratio.hi),mode) for mode in ['decimal','binary64']}
    return locals()
def check(raw,v):
    task=v['task']; parent=v['parent']; row=v['row']; control=v['control']; a=v['a']; w=v['w']; ratio=v['ratio']; hm=v['hm']; eps=v['eps']; B=v['B'];fl=v['fl'];H=v['H'];Hs=v['Hs'];Hb=v['Hb'];n=v['n'];Tg=v['Tg'];TR=v['TR'];A=v['A'];Ae=v['Ae'];R=v['R'];fd=v['fd'];s=v['s'];b=v['b'];coords=v['coords'];par=v['par'];fit=v['fit']
    checks={}
    def test(name,ok): checks[name]=bool(ok)
    try:
        test('schema',raw['schema']=='bubbleverse.q048.v141.conditional_connected.raw.v1')
        test('identity_q',raw['q']==raw['target_q']=='Q048')
        test('identity_task',raw['task_id']==task['task_id'] and raw['task_fingerprint']==task['task_fingerprint'])
        test('identity_run',raw['run_id']==SPEC['run_id'])
        test('identity_question',raw['question_sha256']==task['question_sha256'])
        test('parent_hash_pin',raw['parent_sha256']==task['parent_checkpoint']['file_sha256'])
        test('source_pin',raw['source_commit']==parent['source_commit']==task['source_commit'])
        test('capture_pin',raw['capture_sha256']==parent['capture_sha256']==task['capture_sha256'])
        test('cell',raw['cell_z']==[840,830] and raw['cell_a']==['1/841','1/831'] and raw['case']=='hillipop-ede_n3')
        test('operators',raw['operators']==['HMLA','SWIFT'] and raw['q_branches']=={'L':'1/1000000','R':'0'})
        test('parent_contract',parent['retained_theorem_values']['operators']==raw['operators'] and parent['retained_theorem_values']['q_branches']==raw['q_branches'] and parent['retained_theorem_values']['thermal_domain']==['-1/1000000','1/50'])
        test('guard_primary',raw['guard_primary_index']==row['index'] and raw['guard_primary_sha256']==hashlib.sha256(canon(row)).hexdigest())
        test('guard_control',raw['guard_control_sha256']==hashlib.sha256(canon(control)).hexdigest())
        test('energy_cap',raw['energy_cap']==row['E_input_left'] and raw['energy_safe_left']==row['E_safe_left'] and F(raw['energy_safe_left'])<F(raw['energy_cap']))
        test('outer_domains',raw['domain']==enc({'a':a,'w':w,'TM_over_TR':ratio,'outer_h':m.I(0,hm),'outer_g':m.I(1-hm,1)}))
        test('background',raw['background']==enc({'B0':B,'floor':fl,'H_Mpc':H,'H_s':Hs,'baseline_H_s':Hb,'nH_cm3':n,'Tgamma_K':Tg,'TR_eV':TR}))
        test('atomic',raw['atomic']==enc({'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'beta_photo':b,'Saha':s,'saha_constant':'3.016103031869581e21','coordinates':coords}))
        test('fit',eq(raw['fit_denominator'],fd) and fd.lo>0 and Tg.lo>=fit['valid_temperature_K'][0] and Tg.hi<=fit['valid_temperature_K'][1])
        source=(IROOT/'source/hydrogen.c').read_text(); wr=(IROOT/'source/wrap_hyrec.c').read_text()
        test('source_checks_count',len(raw['source_checks'])==8)
        test('source_checks_true',all(raw['source_checks'].values()))
        test('source_formulas',all(x in source for x in ['Gamma_2p = Beta[1] + R2p2s + RLya;','fitted_RLya = RLya / (1.+DK_K);','Dxe2 = xe*xHII - s*(1.-xHII)','if (z < 900.)']))
        test('zero_injection',raw['injection']=={'ion':'0','exclya':'0'} and all(x in wr for x in ['if (pth->has_exotic_injection == _TRUE_)','else{','phy->data->cosmo->inj_params->ion = 0.;','phy->data->cosmo->inj_params->exclya = 0.;']))
        test('fresh_enclosure',raw['old_operator_enclosure_reused'] is False)
        L=m.const('8.2206'); escape=m.const('4.662899067555897e15')*Hs/n/m.I(1-hm,1)
        for op,esc in [('HMLA',escape),('SWIFT',escape/fd)]:
            gs=b[0]+3*R+L; gp=b[1]+R+esc; D=(b[0]+L)*gp+3*R*(b[1]+esc); nums=[L*gp+3*R*esc,esc*gs+R*L]; comps=[b[0]*gp+3*R*b[1],gs*b[1]+R*b[0]]; cs=[m.I((num/D).lo,min(F(1),(num/D).hi)) for num in nums]
            test('C_'+op,raw['C'][op]==enc({'escape':esc,'Gamma_s':gs,'Gamma_p':gp,'D':D,'numerators':nums,'complements':comps,'C':cs,'strict_C_between_0_and_1':True}) and min(esc.lo,D.lo,*[x.lo for x in nums+comps])>0)
        cmp=raw['comparison']; h0=F(parent['retained_theorem_values']['connected_lower']); K=F(cmp['K_upper']); hmin=F(cmp['h_connected_lower']); d=F(10,831); exact=n.hi*sum(x.hi for x in A)/Hb.lo
        test('K_cross_product',K*Hb.lo>=n.hi*sum(x.hi for x in A) and K-exact<F(1,10**18) and F(cmp['K_unrounded'])==exact)
        du0=k.log_i(k.I(F(841,831))); du=m.I(du0.lo,du0.hi)
        test('log_width',cmp['delta_u']==enc(du) and F(cmp['rational_delta_u_upper'])==d and 0<du.lo<=du.hi<=d)
        rat=h0*(1-K*eps*d)/(1+K*h0*d); expo=eps/((1+eps/h0)*m.exp_i(K*eps*du)-1)
        test('comparison_values',eq(cmp['exponential_endpoint'],expo) and F(cmp['rational_endpoint_lower'])==rat and F(cmp['K_epsilon_d'])==K*eps*d)
        test('rational_lower_cross_product',0<K*eps*d<1 and 0<hmin<h0 and (1+K*h0*d)*hmin<=h0*(1-K*eps*d) and hmin<=expo.lo)
        test('rounding',min(expo.lo,rat)-F(1,10**18)<hmin<=min(expo.lo,rat))
        h=m.I(hmin,hm); test('connected_domains',cmp['initial_h_lower']==str(h0) and cmp['h']==enc(h) and cmp['g']==enc(1-h))
        for label,q in [('L',eps),('R',F(0))]:
            br=raw['branches'][label]; terms=[A[j]*m.I(hm)*(hm+q)-Ae[j]*s*(1-hm) for j in range(2)]; den=1+par['fHe']+h+q; beta=8*m.C['sigma']*(par['gamma']/a**4)*m.C['rhoJ']/(3*m.C['me']*m.C['c']*Hs)*(h+q)/den
            margins={'upper_h_0':terms[0].lo,'upper_h_1':terms[1].lo,'thermal_denominator':den.lo,'beta_lower':beta.lo,'lower_w_inward':1-(1+beta.lo)*w.lo,'upper_w_inward':(1+beta.lo)*w.hi-1}
            test('branch_'+label+'_identity',br['q']==str(q) and br['operators']==['HMLA','SWIFT'])
            test('branch_'+label+'_math',br['upper_h_terms']==enc(terms) and br['denominator']==enc(den) and br['beta']==enc(beta) and br['margins']==enc(margins) and all(F(x)>0 for x in br['margins'].values()))
        cont=raw['continuation']
        test('continuation_interval',cont['initial_a']=='1/841' and cont['endpoint_a']=='1/831' and cont['initial_h_only']==parent['retained_theorem_values']['connected_lower'] and cont['h_upper']=='99999/100000' and cont['w']==['-1/1000000','1/50'])
        test('continuation_scope','Existing absolutely-continuous' in cont['hypothesis'] and 'no assumed future domain membership' in cont['hypothesis'] and cont['selection']=='conv(HMLA,SWIFT) for each fixed q branch' and cont['native_error_certificate'] is False and cont['trajectory_identity_claim'] is False)
        test('frozen_gate_names',[x['name'] for x in raw['gates']]==SPEC['baseline_gate_roster'])
        test('frozen_gates_pass',len(raw['gates'])==len(SPEC['baseline_gate_roster'])>=30 and all(x['pass'] is True for x in raw['gates']))
        test('no_state_advance',raw['actual_unchanged']==parent['actual'] and raw['frontiers_unchanged']==parent['frontiers'] and raw['new_actual_cells']==raw['new_proof_cells']==0)
        test('scope_limits',all(raw[x] is False for x in ['native_error_certificate','exact_selector_existence_uniqueness','trajectory_identity_claim','q_complete','source_state_reset','historical_science_reexecuted']) and raw['NativeP6']=='UNRESOLVED')
        test('candidate_status',raw['status']=='CANDIDATE_CONDITIONAL_CONNECTED_PROOF' and raw['return_route']=='BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0')
    except (KeyError,TypeError,ValueError,ZeroDivisionError):
        checks['structure_or_domain']=False
    return checks
def main():
    raw=read(ROOT/'Q048_V141_RAW_V1.json'); v=reconstruct(); base=check(raw,v)
    mutations=[('wrong_question',['question_sha256'],'0'*64),('wrong_task_id',['task_id'],'WRONG-TASK'),('wrong_task_fingerprint',['task_fingerprint'],'0'*64),('wrong_run',['run_id'],'WRONG-RUN'),('wrong_parent',['parent_sha256'],'0'*64),('source_drift',['source_commit'],'0'*40),('capture_drift',['capture_sha256'],'0'*64),('below830',['cell_z'],[840,820]),('wrong_cell_a',['cell_a'],['1/841','1/821']),('wrong_guard',['guard_primary_index'],60),('control_as_primary',['guard_primary_sha256'],raw['guard_control_sha256']),('silent_cap_swap',['energy_cap'],raw['energy_safe_left']),('drop_HMLA',['operators'],['SWIFT']),('drop_SWIFT',['operators'],['HMLA']),('wrong_q',['q_branches','L'],'0'),('h_not_g',['domain','outer_g'],raw['domain']['outer_h']),('wrong_Saha',['atomic','saha_constant'],'3.016e21'),('drop_channel',['atomic','coordinates','decimal',2],[0]),('wrong_atomic',['atomic','Alpha',0,'lo'],'1'),('unqualified_fit',['fit_denominator','lo'],'0'),('nonpositive_C',['C','HMLA','C',0,'lo'],'0'),('wrong_escape',['C','SWIFT','escape','lo'],'1'),('omit_injection',['injection'],{}),('understate_K',['comparison','K_upper'],'1'),('old_h0_wholecell',['comparison','h_connected_lower'],raw['comparison']['initial_h_lower']),('nonpositive_lower',['comparison','h_connected_lower'],'0'),('wrong_log',['comparison','delta_u','lo'],'0'),('wrong_rounding',['comparison','rational_delta_u_upper'],'1/1000'),('reverse_upper_h',['branches','L','margins','upper_h_0'],'-1'),('old_thermal_face',['continuation','w'],['-1/1000000','1/100']),('reverse_thermal',['branches','R','margins','upper_w_inward'],'-1'),('future_domain_assumption',['continuation','hypothesis'],'Assume future domain membership'),('native_promotion',['native_error_certificate'],True),('selector_existence',['exact_selector_existence_uniqueness'],True),('trajectory_identity',['trajectory_identity_claim'],True),('actual125',['actual_unchanged','count'],125),('proof_before_accept',['new_proof_cells'],1),('Q_closure',['q_complete'],True),('old_cache',['old_operator_enclosure_reused'],True),('physical_reset',['source_state_reset'],True),('empty_gates',['gates'],[]),('malformed_gate_pass',['gates',0,'pass'],False)]
    rejected={}
    for name,path,value in mutations:
        x=copy.deepcopy(raw); node=x
        for part in path[:-1]: node=node[part]
        if node[path[-1]]==value: raise ValueError('NOOP_MUTATION:'+name)
        node[path[-1]]=value; rejected[name]=[k for k,ok in check(x,v).items() if not ok]
    check_roster=list(base.keys()); mutation_roster=[x[0] for x in mutations]
    check_roster_ok=check_roster==SPEC['verifier_check_roster'] and len(check_roster)>=SPEC['criteria']['baseline_named_checks_min']
    semantic_roster_ok=mutation_roster==SPEC['semantic_control_roster'] and len(mutation_roster)>=SPEC['criteria']['semantic_controls_min']
    nonvacuous=all(bool(v) for v in rejected.values()) and all(len(v)>0 for v in rejected.values())
    passed=all(base.values()) and check_roster_ok and semantic_roster_ok and nonvacuous
    out={'schema':'bubbleverse.q048.v141.verification.v1','status':'PASS' if passed else 'FAIL','checks':base,'checks_passed':sum(base.values()),'checks_total':len(base),
      'check_roster':check_roster,'check_roster_sha256':hashlib.sha256(canon(check_roster)).hexdigest(),'check_roster_ok':check_roster_ok,
      'semantic_control_roster':mutation_roster,'semantic_control_roster_sha256':hashlib.sha256(canon(mutation_roster)).hexdigest(),'semantic_control_roster_ok':semantic_roster_ok,
      'semantic_mutations_rejected':sum(bool(v) for v in rejected.values()),'semantic_mutations_total':len(rejected),'semantic_controls_nonvacuous':nonvacuous,'mutation_failed_checks':rejected,
      'raw_sha256':sha(ROOT/'Q048_V141_RAW_V1.json'),'spec_sha256':sha(ROOT/'Q048_V141_SPEC_V1.json'),
      'independence':'Does not import producer. Reconstructs task/source/guard binding, atomic/C, comparison and thermal faces independently while sharing pinned exact helpers/source authorities; not independent native or empirical replication.'}
    with (ROOT/'Q048_V141_VERIFICATION_V1.json').open('x') as f: json.dump(out,f,indent=2); f.write('\n')
    print(json.dumps({'status':out['status'],'checks':[out['checks_passed'],out['checks_total']],'semantic':[out['semantic_mutations_rejected'],out['semantic_mutations_total']]}))
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
