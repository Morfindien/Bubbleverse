"""Q048 V141: fresh source-real connected proof cell 840 -> 830."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
SPEC=json.loads((ROOT/'Q048_V141_SPEC_V1.json').read_text())
IROOT=ROOT/SPEC['helper_root']
sys.path.insert(0,str(IROOT))
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
def floor18(x): return F(x.numerator*10**18//x.denominator,10**18)
def ceil18(x): return -floor18(-x)
def mi(x): return m.I(x.lo,x.hi)
def rational_lower(K,eps,d,h0):
    if not K>0 or eps<0 or d<0 or h0<=0 or K*eps*d>=1: raise ValueError('RICCATI_DOMAIN')
    return h0*(1-K*eps*d)/(1+K*h0*d)
def bind(task,parent,guard,cap):
    b=task['task_fingerprint_basis']
    if hashlib.sha256(canon(b)).hexdigest()!=task['task_fingerprint']: raise ValueError('TASK_FINGERPRINT')
    qh=hashlib.sha256(cap['scientific_question'].encode()).hexdigest()
    if qh!=task['question_sha256'] or cap['scientific_question']!=task['exact_full_question']: raise ValueError('QUESTION_PIN')
    if not task['current_q']==task['target_q']=='Q048': raise ValueError('Q_SCOPE')
    if sha(ROOT/SPEC['parent'])!=task['parent_checkpoint']['file_sha256']: raise ValueError('PARENT_HASH')
    if parent['status']!='ACCEPTED_AFTER_POSTACCEPT' or parent['actual']!={'count':124,'frontier':840}: raise ValueError('PARENT_STATE')
    if parent['frontiers']!=task['parent_checkpoint']['frontiers'] or parent['endpoint']!=task['parent_checkpoint']['endpoint']: raise ValueError('PARENT_PIN')
    if parent['retained_theorem_values']['operators']!=['HMLA','SWIFT'] or parent['retained_theorem_values']['q_branches']!={'L':'1/1000000','R':'0'}: raise ValueError('OPERATOR_PARENT')
    if parent['retained_theorem_values']['thermal_domain']!=['-1/1000000','1/50'] or parent['retained_theorem_values']['h_upper']!='99999/100000' or parent['NativeP6']!='UNRESOLVED': raise ValueError('INITIAL_DOMAIN')
    if not cap['source_commit']==guard['source_commit']==parent['source_commit']==task['source_commit']: raise ValueError('SOURCE_COMMIT')
    if sha(IROOT/'q048_prefix_config_v1.json')!=task['capture_sha256'] or guard['capture_sha256']!=task['capture_sha256'] or parent['capture_sha256']!=task['capture_sha256']: raise ValueError('CAPTURE_PIN')
    if sha(IROOT/'q048_guard_local_v_result_v12.json')!=task['guard']['sha256']: raise ValueError('GUARD_BYTES')
    if [e['control'] for e in guard['evaluators']] != [False,True]: raise ValueError('PRIMARY_CONTROL')
    rows=[]
    for ev in guard['evaluators']:
        rr=[r for r in ev['rows'] if [r['a0'],r['a1']]==['1/841','1/831'] and [r['z0'],r['z1']]==[840,830]]
        if len(rr)!=1: raise ValueError('UNIQUE_GUARD_CELL')
        r=rr[0]
        if r['source_state_reset'] or not all(r[x] for x in ['accepted','committed','whole_cell_qualified']) or not r['domain']['admitted'] or not all(r['domain']['checks'].values()) or F(r['G_lower'])<=0: raise ValueError('GUARD_ADMISSION')
        rows.append(r)
    if hashlib.sha256(canon(rows[0])).hexdigest()!=task['guard']['primary_row_sha256']: raise ValueError('PRIMARY_ROW_HASH')
    if hashlib.sha256(canon(rows[1])).hexdigest()!=task['guard']['control_row_sha256']: raise ValueError('CONTROL_ROW_HASH')
    for rk,pk in [('a0','a'),('E_input_left','E'),('Y_left','Y'),('V_previous','Vbar')]:
        if F(rows[0][rk])!=F(parent['endpoint'][pk]): raise ValueError('EXACT_LEFT_GLUE:'+rk)
    if not 0<F(rows[0]['E_safe_left'])<F(rows[0]['E_input_left']): raise ValueError('CONSERVATIVE_ENERGY_CAP')
    return rows
def produce(spec):
    for rel,pn in spec['input_pins'].items():
        p=ROOT/rel
        if p.stat().st_size!=pn['bytes'] or sha(p)!=pn['sha256']: raise ValueError('INPUT_PIN:'+rel)
    for rel,pn in spec['helper_pins'].items():
        p=IROOT/rel
        if p.stat().st_size!=pn['bytes'] or sha(p)!=pn['sha256']: raise ValueError('HELPER_PIN:'+rel)
    task=read(ROOT/spec['task']); parent=read(ROOT/spec['parent']); guard=read(IROOT/'q048_guard_local_v_result_v12.json'); cap=read(IROOT/'q048_prefix_config_v1.json')
    row,control=bind(task,parent,guard,cap)
    prefix.validate_config(cap); case=cap['cases']['hillipop-ede_n3']; par=prefix.parameters(case)
    out={'schema':'bubbleverse.q048.v141.conditional_connected.raw.v1','q':'Q048','target_q':'Q048','task_id':task['task_id'],'task_fingerprint':task['task_fingerprint'],
      'run_id':spec['run_id'],'question_sha256':task['question_sha256'],'source_commit':cap['source_commit'],'capture_sha256':sha(IROOT/'q048_prefix_config_v1.json'),
      'cell_z':[840,830],'cell_a':['1/841','1/831'],'case':'hillipop-ede_n3','operators':['HMLA','SWIFT'],'q_branches':{'L':'1/1000000','R':'0'},
      'parent_sha256':sha(ROOT/spec['parent']),'actual_unchanged':parent['actual'],'frontiers_unchanged':parent['frontiers'],
      'guard_primary_index':row['index'],'guard_primary_sha256':hashlib.sha256(canon(row)).hexdigest(),'guard_control_sha256':hashlib.sha256(canon(control)).hexdigest(),
      'energy_cap':row['E_input_left'],'energy_safe_left':row['E_safe_left'],'gates':[],'status':'PENDING','branches':{},'new_actual_cells':0,'new_proof_cells':0,
      'NativeP6':'UNRESOLVED','native_error_certificate':False,'exact_selector_existence_uniqueness':False,'trajectory_identity_claim':False,'q_complete':False,
      'source_state_reset':False,'old_operator_enclosure_reused':False,'historical_science_reexecuted':False,'return_route':'BUBBLEVERSE.RESULT_INGESTION_ROUTING2.1.0'}
    def gate(name,ok,margin=None):
        out['gates'].append({'name':name,'pass':bool(ok),'margin':enc(margin)})
        if not ok: out['status']='FIRST_MATERIAL_OBSTRUCTION'; out['obstruction']={'gate':name,'margin':enc(margin)}
        return bool(ok)
    a=m.I(F(1,841),F(1,831)); w=m.I(F(-1,1000000),F(1,50)); ratio=1-w; hmax=F(99999,100000); eps=F(1,1000000); h0=F(parent['retained_theorem_values']['connected_lower'])
    B,fl,H,Hs=tube.background(a,par,F(row['E_input_left'])); Hbase=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']; n=par['nH0']/a**3*m.const('1e-6'); Tg=par['T0']/a; TR=m.const('8.617343e-5')*Tg
    out.update(domain={'a':a,'w':w,'TM_over_TR':ratio,'outer_h':m.I(0,hmax),'outer_g':m.I(1-hmax,1)},background={'B0':B,'floor':fl,'H_Mpc':H,'H_s':Hs,'baseline_H_s':Hbase,'nH_cm3':n,'Tgamma_K':Tg,'TR_eV':TR})
    source=(IROOT/'source/hydrogen.c').read_text(); wrapper=(IROOT/'source/wrap_hyrec.c').read_text()
    sources={'capture_MODEL4_no_error':all(x['HyRec_MODEL']==4 and x['HyRec_error']==0 for x in case['thermal_starts']),
      'fixed_flags':all(case['background']['thermal_flags'][x]==0 for x in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),
      'atomic_TR':TR.lo>m.const('.004').hi and TR.hi<m.const('.4').lo,'atomic_ratio':ratio.lo>F(1,10) and ratio.hi<10,'SWIFT_fit_temperature':1775<=Tg.lo<=Tg.hi<=4415,
      'positive_background':min(Hs.lo,Hbase.lo,n.lo)>0,'operator_source':all(x in source for x in ['Gamma_2p = Beta[1] + R2p2s + RLya;','fitted_RLya = RLya / (1.+DK_K);','Dxe2 = xe*xHII - s*(1.-xHII)','if (z < 900.)']),
      'zero_injection_source':all(x in wrapper for x in ['if (pth->has_exotic_injection == _TRUE_)','else{','phy->data->cosmo->inj_params->ion = 0.;','phy->data->cosmo->inj_params->exclya = 0.;'])}
    out['source_checks']=sources
    for name,ok in sources.items():
        if not gate('SOURCE:'+name,ok): return enc(out)
    raw3=read(IROOT/'q048_p3_scaled_raw_result_v2.json')
    if not gate('ATOMIC_TABLE_HASH',sha(IROOT/'q048_p3_scaled_transformed_log_tables_v2.json')==raw3['transformed_tables_sha256']): return enc(out)
    alpha,rr=tube.load_atomic(IROOT/'q048_p3_scaled_transformed_log_tables_v2.json'); at=tube.local_atomic(alpha,rr,TR,ratio)
    A=list(map(mi,at['Alpha'])); Ae=list(map(mi,at['Alpha_eq'])); R=mi(at['R2p2s'])
    init=raw3['initialized_cases']['hillipop-ede_n3']; params={key:k.I(F(v['lo']),F(v['hi'])) for key,v in init.items() if isinstance(v,dict) and 'lo' in v}
    for key,val in [('T0',par['T0']),('nH0_SI',par['nH0']),('fHe',par['fHe']),('YHe',prefix.point(case['thermal_starts'][0]['constants']['YHe']))]:
        if not gate('FIT_CAPTURE:'+key,(params[key].lo,params[key].hi)==(val.lo,val.hi)): return enc(out)
    fit=k.fit_admission(k.load_fit(IROOT/'source/fit_swift.dat'),params,k.norm_certificate()); fd=mi(fit['primary_denominator'])
    retained=raw3['fit_cases']['hillipop-ede_n3']['primary_denominator']
    if not gate('GLOBAL_FIT_REUSE_DOMAIN',fd.lo==F(retained['lo']) and fd.hi==F(retained['hi']) and Tg.lo>=fit['valid_temperature_K'][0] and Tg.hi<=fit['valid_temperature_K'][1]): return enc(out)
    thermal=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR); photo=thermal*m.exp_i(-m.const('.25')*m.const('13.598286071938324')/TR); saha=thermal*m.exp_i(-m.const('13.598286071938324')/TR)/n
    b=[Ae[0]*photo,Ae[1]*photo/3]; L=m.const('8.2206'); escape=m.const('4.662899067555897e15')*Hs/n/m.I(1-hmax,1)
    coords={mode:k.rate_coordinates(k.I(TR.lo,TR.hi),k.I(ratio.lo,ratio.hi),mode) for mode in ['decimal','binary64']}
    out.update(atomic={'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'beta_photo':b,'Saha':saha,'saha_constant':'3.016103031869581e21','coordinates':coords},fit_denominator=fd,injection={'ion':'0','exclya':'0'},C={})
    for op,e in [('HMLA',escape),('SWIFT',escape/fd)]:
        gs=b[0]+3*R+L; gp=b[1]+R+e; D=(b[0]+L)*(b[1]+R+e)+3*R*(b[1]+e); Ns=L*gp+3*R*e; Np=e*gs+R*L; comp=[b[0]*gp+3*R*b[1],gs*b[1]+R*b[0]]
        margin=min(e.lo,D.lo,Ns.lo,Np.lo,*[c.lo for c in comp]); Cs=[m.I((v/D).lo,min(F(1),(v/D).hi)) for v in [Ns,Np]]
        out['C'][op]={'escape':e,'Gamma_s':gs,'Gamma_p':gp,'D':D,'numerators':[Ns,Np],'complements':comp,'C':Cs,'strict_C_between_0_and_1':margin>0}
        if not gate('POSITIVE_C:'+op,margin>0,margin): return enc(out)
    margin=min(saha.lo,R.lo,fd.lo,*[x.lo for x in A+Ae+b])
    if not gate('POSITIVE_ATOMIC_FIT',margin>0,margin): return enc(out)
    Kexact=n.hi*sum(x.hi for x in A)/Hbase.lo; K=ceil18(Kexact); d=a.hi/a.lo-1; du=k.log_i(k.I(a.hi/a.lo)); u=m.I(du.lo,du.hi)
    lower_exp=eps/((1+eps/h0)*m.exp_i(K*eps*u)-1); lower_rat=rational_lower(K,eps,d,h0); hmin=floor18(min(lower_exp.lo,lower_rat)); h=m.I(hmin,hmax)
    out['comparison']={'K_unrounded':Kexact,'K_upper':K,'delta_u':u,'rational_delta_u_upper':d,'K_epsilon_d':K*eps*d,'initial_h_lower':h0,'exponential_endpoint':lower_exp,
      'rational_endpoint_lower':lower_rat,'h_connected_lower':hmin,'h':h,'g':1-h,'equation':'h_u >= -K h(h+epsilon); u=ln(a)'}
    if not gate('CONNECTED_LOWER',0<hmin<=h0<hmax,hmin): return enc(out)
    for label,q in [('L',eps),('R',F(0))]:
        face=[A[j]*m.I(hmax)*(hmax+q)-Ae[j]*saha*(1-hmax) for j in range(2)]; den=1+par['fHe']+h+q
        beta=8*m.C['sigma']*(par['gamma']/a**4)*m.C['rhoJ']/(3*m.C['me']*m.C['c']*Hs)*(h+q)/den
        margins={'upper_h_0':face[0].lo,'upper_h_1':face[1].lo,'thermal_denominator':den.lo,'beta_lower':beta.lo,'lower_w_inward':1-(1+beta.lo)*w.lo,'upper_w_inward':(1+beta.lo)*w.hi-1}
        rates={op:-n/Hs*sum((out['C'][op]['C'][j]*(A[j]*h*(h+q)-Ae[j]*saha*(1-h)) for j in range(2)),m.I(0)) for op in ['HMLA','SWIFT']}
        out['branches'][label]={'q':q,'operators':['HMLA','SWIFT'],'upper_h_terms':face,'denominator':den,'beta':beta,'margins':margins,'signed_rate_enclosures':rates}
        for name,v in margins.items():
            if not gate('BRANCH:'+label+':'+name,v>0,v): return enc(out)
    out['continuation']={'initial_a':'1/841','endpoint_a':'1/831','initial_h_only':parent['retained_theorem_values']['connected_lower'],'h_upper':str(hmax),'w':['-1/1000000','1/50'],
      'background':'Admitted primary guard row61, exact inherited V140 E/Y/V_previous; E_input_left is conservative whole-cell energy cap; no scalar consumption.',
      'selection':'conv(HMLA,SWIFT) for each fixed q branch','hypothesis':'Existing absolutely-continuous source-real solution under the admitted background and fixed-q two-operator inclusion; no assumed future domain membership. Bounds apply on its existing interval and at a1 whenever an admissible continuation reaches a1. Exact selector existence/uniqueness is not established.',
      'proof':'Positive source/atomic/C premises hold on the outer box. Riccati comparison excludes lower-h exit. Strict upper-h and both thermal inward faces exclude all other exits. Closed-endpoint persistence follows for existing admissible continuations; convex combinations preserve the derivative inequalities.',
      'native_error_certificate':False,'trajectory_identity_claim':False}
    gate_names=[x['name'] for x in out['gates']]
    if gate_names!=spec['baseline_gate_roster'] or len(gate_names)<spec['criteria']['baseline_named_checks_min']:
        out['status']='FIRST_MATERIAL_OBSTRUCTION'
        out['obstruction']={'gate':'FROZEN_GATE_ROSTER','observed':gate_names,'expected':spec['baseline_gate_roster']}
        return enc(out)
    out['gate_roster_sha256']=hashlib.sha256(canon(gate_names)).hexdigest()
    out['status']='CANDIDATE_CONDITIONAL_CONNECTED_PROOF'
    return enc(out)
if __name__=='__main__':
    result=produce(SPEC)
    with (ROOT/'Q048_V141_RAW_V1.json').open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({'status':result['status'],'comparison':result.get('comparison'),'obstruction':result.get('obstruction')}))
