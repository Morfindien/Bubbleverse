"""Q047 source-real precursor backend. No native build/init/re-shoot/production.

Exact primitive boxes define a CONDITIONAL reference. This backend recomputes
defects, Jacobians and finite-growth slacks; exported metadata is never an
actual initialization certificate. Full-path admission and downstream M06
event qualification remain separate, explicit gates.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import argparse, hashlib, json, os, sys, time, platform
import q047_math_v1 as m
import q047_certificate_v1 as old

Q=old.Q
ID='Q047-PRECURSORCHECK-V1'
SOURCE=old.SOURCE
ROOT=Path(__file__).resolve().parent
MODES=('brec','He1','He1f','He2')

def value(x): return x.v if isinstance(x,m.A) else m.iv(x)

def square(x):
    if isinstance(x,m.A):
        return m.A(square(x.v),[2*x.v*d for d in x.d])
    x=m.iv(x)
    return m.I.rounded(0 if x.lo<=0<=x.hi else min(x.lo*x.lo,x.hi*x.hi),max(x.lo*x.lo,x.hi*x.hi))

def scalar_envelope(L,h,r0,delta):
    L,h,r0,delta=map(old.rational,(L,h,r0,delta))
    if h<0 or min(r0,delta)<0:raise ValueError('ERROR_ENVELOPE_DOMAIN')
    end=m.exp_i(m.I(L*h))*r0+old.exponential_integral(m.I(L),h)*delta
    return end,m.I(max(r0,end.lo),max(r0,end.hi))

def vector_envelope(M,h,r0,delta):
    h=old.rational(h)
    if len(r0)!=2 or len(delta)!=2 or min(r0+delta)<0:raise ValueError('ERROR_VECTOR_DOMAIN')
    E,J=old.comparison_matrices(M,h)
    end=[sum((E[i][j]*r0[j]+J[i][j]*delta[j] for j in range(2)),m.I(0)) for i in range(2)]
    sigma=max(F(0),-min(M[0][0],M[1][1]))
    N=[[M[i][j]+(sigma if i==j else 0) for j in range(2)] for i in range(2)]
    EN,_=old.comparison_matrices(N,h)
    bound=[sum((EN[i][j]*(r0[j]+h*delta[j]) for j in range(2)),m.I(0)) for i in range(2)]
    return end,bound

def trig(x,cosine=False):
    """Rational Taylor at midpoint + derivative<=1 range bound, degree160.
    No floating libm participates in proof arithmetic. |midpoint|<=16 cap.
    """
    if isinstance(x,m.A):
        v=trig(x.v,cosine);d=-trig(x.v,False) if cosine else trig(x.v,True)
        return m.A(v,[d*t for t in x.d])
    x=m.iv(x);c=(x.lo+x.hi)/2;r=(x.hi-x.lo)/2
    if abs(c)>16:raise ValueError('TRIG_RANGE_CAP_UNRESOLVED')
    degree=160;total=F(0)
    for k in range(0 if cosine else 1,degree+1,2):
        total+=(-1)**(k//2 if cosine else (k-1)//2)*c**k/factorial(k)
    rem=abs(c)**(degree+1)/factorial(degree+1)+r
    out=m.I.rounded(total-rem,total+rem)
    # sin/cos range intersects exact [-1,1]; valid even at zero.
    return m.I(max(F(-1),out.lo),min(F(1),out.hi))

def neutrino_sum(a,s):
    a=m.iv(a);mu=a*s['mass'];nodes=s['nodes'];weights=s['weights']
    if a.lo<=0 or s['mass'].lo<0 or s['factor'].lo<0:raise ValueError('NCDM_DOMAIN')
    if not 1<=len(nodes)<=4096 or len(nodes)!=len(weights):raise ValueError('NCDM_NODE_SHAPE')
    rho=m.I(0);p=m.I(0)
    for q,w in zip(nodes,weights):
        if q.lo<0 or w.lo<0:raise ValueError('NCDM_NODE_WEIGHT_SIGN')
        en=m.sqrt_i(square(q)+square(mu))
        rho+=square(q)*en*w
        if en.lo==0:
            # q^4/sqrt(q^2+mu^2)<=q^3, including continuous (0,0).
            p+=m.I(0,(q**3*w/3).hi)
        else:p+=q**4*w/(3*en)
    return s['factor']/a**4*rho,s['factor']/a**4*p

def fd_moments(a,mass,xi,factor,Qmax,cells):
    """Analytic FD reference only. Distinct from finite-node realization.
    Rational cell ranges and analytic tail; never reclose Lambda or B.
    """
    if not isinstance(cells,int) or not 1<=cells<=4096:raise ValueError('FD_CELL_CAP')
    Qmax=old.rational(Qmax);a=m.iv(a);mu=a*mass
    if Qmax<=0 or Qmax>100 or a.lo<=0 or mass.lo<0 or factor.lo<0:raise ValueError('FD_DOMAIN')
    rho=m.I(0);press=m.I(0);scale=1/(2*m.C['pi'])**3
    for j in range(cells):
        q=m.I(Qmax*j/cells,Qmax*(j+1)/cells)
        dist=scale*(1/(m.exp_i(q-xi)+1)+1/(m.exp_i(q+xi)+1))
        en=m.sqrt_i(square(q)+square(mu))
        rho+=Qmax/cells*square(q)*en*dist
        if en.lo==0:press+=Qmax/cells*m.I(0,(q**3*dist/3).hi)
        else:press+=Qmax/cells*q**4*dist/(3*en)
    A=(m.exp_i(xi)+m.exp_i(-xi))*scale
    P2=Qmax**2+2*Qmax+2;P3=Qmax**3+3*Qmax**2+6*Qmax+6
    tr=A*m.exp_i(m.I(-Qmax))*(P3+mu.hi*P2)
    tp=A*m.exp_i(m.I(-Qmax))*P3/3
    scale2=factor/a**4
    return scale2*(rho+m.I(0,tr.hi)),scale2*(press+m.I(0,tp.hi)),[scale2*tr,scale2*tp]

def common_neutrinos(a,s):
    finite=neutrino_sum(a,s)
    fd=fd_moments(a,s['mass'],s['xi'],s['factor'],s['Qmax'],s['cells'])[:2]
    hull=[m.I(min(x.lo,y.lo),max(x.hi,y.hi)) for x,y in zip(finite,fd)]
    return {'rho':hull[0],'p':hull[1],'finite':finite,'fd':fd,
            'quadrature_difference':[x-y for x,y in zip(finite,fd)]}

def potential(phi,s):
    if s['F'].lo<=0 or s['m'].lo<0:raise ValueError('SCF_PARAMETER_DOMAIN')
    angle=phi*m.const('2.435e27')/s['F']
    d=1-trig(angle,True)
    # 1-cos>=0 (intersection already established by trig).
    ve=m.const('4152.39')*square(s['m'])*square(s['F'])*d**3
    vp=m.const('4152.39')*m.const('2.435e27')*square(s['m'])*s['F']*3*trig(angle)*square(d)
    return ve+s['B']*m.const('3.968e-8'),vp,ve

def background(a,t,state=None):
    a=m.iv(a)
    if a.lo<=0 or t['gamma'].lo<=0:raise ValueError('BACKGROUND_POSITIVITY')
    rg=t['gamma']/a**4;rad=(t['gamma']+t['ur'])/a**4
    rho=rad+t['matter']/a**3+t['lambda'];p=rad/3-t['lambda'];ve=m.I(0)
    for s in t['neutrinos']:
        if s.get('reference','FINITE_NATIVE')=='FINITE_NATIVE':r,v=neutrino_sum(a,s)
        elif s['reference']=='FD_ANALYTIC':r,v,_=fd_moments(a,s['mass'],s['xi'],s['factor'],s['Qmax'],s['cells'])
        elif s['reference']=='COMMON_FINITE_FD':
            both=common_neutrinos(a,s);r,v=both['rho'],both['p']
        else:raise ValueError('NCDM_REFERENCE_SEMANTICS')
        rho+=r;p+=v
    if t['ede'] is not None:
        if state is None or len(state)!=2:raise ValueError('SCF_STATE_REQUIRED')
        phi,X=state;V,_,ve=potential(phi,t['ede'])
        rho+=(square(X)/2+V)/3;p+=(square(X)/2-V)/3
    H2=rho-t['K']/a**2
    if value(H2).lo<=0:raise ValueError('H_SQUARED_NOT_POSITIVE')
    H=m.root(H2);ell=-3*(rho+p)/(2*H2)+t['K']/(a*a*H2)
    return {'H':H,'Hs':H*m.C['c']/m.C['Mpc'],'rho_gamma':rg,'rho_plus_p':rho+p,'ell':ell,'ede_latch':ve/(3*H2)}

def ede_field(a,state,t):
    b=background(a,t,state);phi,X=state;_,Vp,_=potential(phi,t['ede'])
    return [X/b['H'],-3*X-Vp/b['H']],b

def thermal(mode,a,w,t,b):
    if mode not in MODES:raise ValueError('THERMAL_MODE')
    T=(1-w)*t['T0']/a;f=t['fHe']
    if value(T).lo<=0 or f.lo<=0 or t['nH0'].lo<=0:raise ValueError('THERMAL_REGULAR_DOMAIN')
    if mode in ('brec','He1'):
        S=m.I(1);aa=1+f;bb=1+2*f
        ion=m.C['hp']*m.C['c']*m.const('4.389088863e7')/m.C['kb']*m.PAD
    else:S=m.I(4);aa=m.I(1);bb=1+f;ion=m.IHe
    # Evaluate the value separately; differentiating the quotient directly
    # loses the exact Saha cancellation at very large r. The implicit
    # 0<=dln(x)/dln(r)<=(B-A)/(2B-A) bound remains uniform there.
    Tv=value(T)
    r=S*(m.CNR*Tv)*m.sqrt_i(m.CNR*Tv)*a**3/t['nH0']*m.exp_i(-ion/Tv)
    xv=aa+2*r*(bb-aa)/(aa+r+m.sqrt_i(square(aa+r)+4*r*(bb-aa)))
    # Exact positive root lies in [A,B]; intersect a valid algebraic enclosure.
    xv=m.I(max(aa.lo,xv.lo),min(bb.hi,xv.hi))
    x=xv
    if isinstance(w,m.A):
        eta=m.I(0,((bb-aa)/(2*bb-aa)).hi)
        logxw=-eta*(m.I(F(3,2))+ion/Tv)/(1-w.v)
        x=m.A(xv,[xv*logxw*d for d in w.d])
    beta=8*m.C['sigma']/(3*m.C['me']*m.C['c'])*b['rho_gamma']*m.C['rhoJ']/b['Hs']*x/(1+f+x)
    if value(beta).lo<=0:raise ValueError('BETA_NOT_POSITIVE')
    rate=w+(b['ell']+3)/beta if mode=='brec' else 1-(1+beta)*w
    # Thermal x is not the x_H/x_He sentinels assigned elsewhere in CLASS.
    return {'rate':rate,'x':x,'beta':beta,'Tmat':T,'r':r}

def onset(w,a,t):
    T=(1-w)*t['T0']/a
    if value(T).lo<=0:raise ValueError('ONSET_TEMPERATURE')
    r=4*(m.CNR*T)*m.root(m.CNR*T)*a**3/t['nH0']*m.ex(-m.IHe/T)
    return 2*t['fHe']*r/(1+r+m.root(square(1+r)+4*t['fHe']*r))

def certify_cell(cell,initial,field):
    """Recompute whole-cell defect, Jacobian, envelope, closure and endpoint.
    Predictor power coefficients use xi=(u-t0)/h. Supplied residuals/booleans
    are ignored by design, never promoted to proof inputs.
    """
    t0,t1=old.rational(cell['t0']),old.rational(cell['t1']);h=t1-t0
    if h<=0 or h>1:raise ValueError('CELL_TIME_DOMAIN')
    coeff=[[old.rational(x) for x in row] for row in cell['predictor']]
    n=len(initial)
    if n not in (1,2) or len(coeff)!=n or len(cell['box'])!=n:raise ValueError('CELL_DIMENSION')
    box=[old.interval(v) for v in cell['box']]
    pr=[old.poly_range(row) for row in coeff]
    dr=[old.poly_range([F(k)*row[k]/h for k in range(1,len(row))] or [F(0)]) for row in coeff]
    r0=[max(abs(initial[i].lo-coeff[i][0]),abs(initial[i].hi-coeff[i][0])) for i in range(n)]
    pp=[m.A(pr[i]) for i in range(n)]
    yy=[m.A(box[i],[m.I(int(i==j)) for j in range(2)]) for i in range(n)]
    fp=field(m.I(t0,t1),pp);ff=field(m.I(t0,t1),yy)
    delta=[(dr[i]-value(fp[i])).absmax() for i in range(n)]
    M=[[ff[i].d[j].hi if i==j else ff[i].d[j].absmax() for j in range(n)] for i in range(n)]
    if n==1:
        e,b=scalar_envelope(M[0][0],h,r0[0],delta[0]);end=[e];bound=[b]
    else:end,bound=vector_envelope(M,h,r0,delta)
    slacks=[min(pr[i].lo-bound[i].hi-box[i].lo,box[i].hi-pr[i].hi-bound[i].hi) for i in range(n)]
    endpoints=[m.I(old.poly_at(coeff[i],F(1))-end[i].hi,old.poly_at(coeff[i],F(1))+end[i].hi) for i in range(n)]
    return {'closed':all(s>0 for s in slacks),'closure_slack':list(map(str,slacks)),
            'initial_error':list(map(str,r0)),'defect_upper':list(map(str,delta)),
            'comparison':[[str(v) for v in row] for row in M],
            'alltime_error':[old.pairs(v) for v in bound],
            'endpoint_error':[old.pairs(v) for v in end],
            'endpoint':[old.pairs(v) for v in endpoints],
            'whole_state':[old.pairs(m.I(pr[i].lo-bound[i].hi,pr[i].hi+bound[i].hi)) for i in range(n)]}

def decode_field(obj,unit):
    if not isinstance(obj,dict) or obj.get('unit')!=unit or not obj.get('source_field'):raise ValueError('EFFECTIVE_FIELD_METADATA')
    x=old.interval(obj['bounds'])
    if 'native_hex' in obj:
        v=float.fromhex(obj['native_hex'])
        try:r=F.from_float(v)
        except (ValueError,OverflowError):raise ValueError('NATIVE_HEX_NONFINITE')
        if not x.lo<=r<=x.hi:raise ValueError('NATIVE_HEX_OUTSIDE_BOUNDS')
    return x

def generate_cells(initial,start,end,field,box,max_cells=128,max_halvings=20):
    """Finite Euler predictor construction; every accepted cell is certified.
    User supplies a prospective physical domain. No tolerance is fabricated;
    exhausting that domain/work budget returns preserved PARTIAL/UNRESOLVED.
    """
    start,end=old.rational(start),old.rational(end)
    if end<=start or not 1<=max_cells<=2048 or not 0<=max_halvings<=30:raise ValueError('GENERATOR_DOMAIN')
    now=start;current=initial;cells=[];attempts=0
    while now<end and len(cells)<max_cells:
        h=min(end-now,F(1,100));accepted=None
        center=[(x.lo+x.hi)/2 for x in current]
        slopes=[value(v) for v in field(m.I(now),[m.A(x) for x in center])]
        for halving in range(max_halvings+1):
            attempts+=1
            predictor=[[str(center[i]),str((slopes[i].lo+slopes[i].hi)/2*h)] for i in range(len(current))]
            candidate={'t0':str(now),'t1':str(now+h),'predictor':predictor,'box':box}
            report=certify_cell(candidate,current,field)
            if report['closed']:accepted=(candidate,report);break
            h/=2
        if accepted is None:break
        candidate,report=accepted;candidate['certificate']=report;cells.append(candidate)
        current=[old.interval(v) for v in report['endpoint']];now+=h
    return {'status':'COMPLETE' if now==end else 'UNRESOLVED_WORK_CAP',
            'requested_end':str(end),'certified_end':str(now),'attempts':attempts,'cells':cells,
            'endpoint':[old.pairs(v) for v in current]}

def threshold_report():
    native=F.from_float(float.fromhex('0x1.0c6f7a0b5ed8dp-20'))
    return {'exact_epsilon':str(old.EPS),'native_epsilon':str(native),
            'difference_native_minus_exact':str(native-old.EPS),
            'binary_equivalence_gate':'UNRESOLVED',
            'reason':'Exact-real source reference is separate from compiled guard-product rounding and source-to-binary linkage.'}

def audit_export(export,contract_path):
    """Read-only completeness/representation audit, not origin attestation.
    There is intentionally no native initialization or archive inverse here.
    """
    contract=old.load(contract_path)
    if export.get('q')!=Q or export.get('source_commit')!=SOURCE or export.get('case') not in old.CASES:raise ValueError('EXPORT_IDENTITY')
    fields=export.get('fields',{});required=contract['required_theta_fields'];missing=[];invalid={};checked=[]
    groups=['background_common','thermal']
    if 'ede' in export['case']:groups.append('ede_only')
    for group in groups:
        for key,description in required[group].items():
            if key not in fields:missing.append(key);continue
            try:
                obj=fields[key]
                # Arrays/booleans are represented separately, never converted to numbers.
                if key=='scf_parameters':
                    if not isinstance(obj,list) or len(obj)<6:raise ValueError('SCF_ARRAY')
                    for v in obj:decode_field(v,'1')
                elif key=='attractor_ic_scf':
                    if obj is not False:raise ValueError('ATTRACTOR_UNSUPPORTED')
                else:
                    if not isinstance(obj,dict) or not obj.get('native_hex') or not obj.get('raw_link') or not obj.get('bound_type'):raise ValueError('EFFECTIVE_HEX_RAW_LINK_REQUIRED')
                    decode_field(obj,obj.get('unit'))
                    if not obj.get('unit'):raise ValueError('UNIT_REQUIRED')
                checked.append(key)
            except (ValueError,TypeError,KeyError,AssertionError) as e:invalid[key]=str(e)
    for group in ('background_flags','thermal_flags','arithmetic','mode_boundaries'):
        values=export.get(group,{})
        for key in required[group]:
            if key not in values or values[key] is None:missing.append(group+'::'+key)
    for j,s in enumerate(export.get('neutrino_species',[])):
        for key in required['neutrino_per_species']:
            if key not in s:missing.append(f'neutrino[{j}]::{key}')
    if export.get('background_flags',{}).get('N_ncdm',1)!=len(export.get('neutrino_species',[])):
        invalid['N_ncdm']='SPECIES_COUNT_MISMATCH_OR_MISSING'
    return {'q':Q,'case':export['case'],'checked_fields':checked,'missing':missing,'invalid':invalid,
            'effective_field_gate':'PASS_REPRESENTATION_ONLY' if not missing and not invalid else 'FAIL',
            'actual_admission_gate':'UNRESOLVED','reason':'Completeness does not verify accepted initialized-instance origin, compiled arithmetic, inverse completeness or IVP accuracy.'}

def package_gate(root=ROOT):
    root=Path(root);lock=old.load(root/'q047_precursor_package_v1.json')
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    if digest(root/'.github/workflows/00-bubbleverse-start.yml')!=lock['launcher_sha256']:raise ValueError('UNCHANGED_LAUNCHER_HASH')
    for path,expected in lock['files'].items():
        if digest(root/path)!=expected:raise ValueError('PACKAGE_HASH '+path)
    reg=old.load(root/'bubbleverse_program_registry.json')
    prior={k:v for k,v in reg['programs'].items() if k!=ID}
    canonical=hashlib.sha256(json.dumps(prior,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    if canonical!=lock['protected_registry_entries_sha256']:raise ValueError('EXISTING_REGISTRY_CHANGED')
    entry=reg['programs'].get(ID,{})
    target='.github/workflows/q047-precursor-check-v1.yml'
    if entry.get('q')!=Q or entry.get('status')!='ACTIVE' or entry.get('workflow_path')!=target or entry.get('workflow_id')!=Path(target).name or entry.get('version')!='v1':raise ValueError('REGISTRY_Q_VERSION_TARGET')
    readme=(root/'README.md').read_text()
    if ID not in readme or target not in readme or 'CONDITIONAL' not in readme:raise ValueError('README_SCOPE_OR_PATH')
    if digest(root/'Q047_PRECURSOR_CONTRACT_V1.json')!=lock['contract_sha256']:raise ValueError('MATHEMATICAL_CONTRACT_CHANGED')
    journal=(root/'Q047_SAMLET_JOURNAL.md').read_bytes()
    marker=b'# COMPLETE RECEIVED Q047 ASSESSMENT AND INHERITED JOURNAL \xe2\x80\x94 VERBATIM HISTORICAL BYTES FOLLOW\n\n'
    if marker not in journal or hashlib.sha256(journal.split(marker,1)[1]).hexdigest()!=lock['historical_tail_sha256']:raise ValueError('JOURNAL_HISTORY_CHANGED')
    question=old.load(root/'Q047_PRECURSOR_CONTRACT_V1.json')['question']
    if question.encode() not in journal:raise ValueError('EXACT_QUESTION_LOST')
    return {'q':Q,'program_id':ID,'launcher_gate':'PASS','registry_gate':'PASS_CANDIDATE_LOCAL',
            'readme_gate':'PASS','repository_consistency_gate':'PASS_CANDIDATE_LOCAL',
            'remote_installed':False,'base_commit':lock['repository_base_commit']}

def verify_packet(packet):
    if packet.get('actual_reference_qualified'):raise ValueError('ASSERTED_ACTUAL_QUALIFICATION_REFUSED')
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    if packet.get('schema')!='Q047-PRECURSOR-PACKET-V1' or packet.get('q')!=Q:raise ValueError('Q_OR_SCHEMA')
    if packet.get('source_commit')!=SOURCE or packet.get('case') not in old.CASES:raise ValueError('SOURCE_OR_CASE')
    if packet.get('scope')!='CONDITIONAL_SOURCE_REAL_PREFIX' or packet.get('coordinate')!='a':raise ValueError('REFERENCE_SCOPE_OR_COORDINATE')
    omitted=('has_fld','has_idm','has_idr','has_dcdm','has_dr','has_varconst','has_exotic_injection',
             'has_idm_b','has_idm_g','has_idm_dr','has_ap_idmtca')
    if any(packet['flags'].get(k) is not False for k in omitted):raise ValueError('REDUCED_VARIANT_UNSUPPORTED_OR_MISSING_FLAG')
    t={k:old.interval(packet['parameters'][k]) for k in ('H0','gamma','ur','matter','lambda','K','T0','nH0','fHe')}
    if min(t[k].lo for k in ('H0','gamma','T0','nH0','fHe'))<=0 or min(t['ur'].lo,t['matter'].lo)<0:raise ValueError('PARAMETER_DOMAIN')
    t['neutrinos']=[]
    if len(packet['neutrinos'])>8:raise ValueError('NCDM_SPECIES_CAP')
    for s in packet['neutrinos']:
        obj={'mass':old.interval(s['mass']),'factor':old.interval(s['factor']),'reference':s['reference']}
        if s['reference'] in ('FINITE_NATIVE','COMMON_FINITE_FD'):
            obj.update(nodes=[old.interval(v) for v in s['nodes']],weights=[old.interval(v) for v in s['weights']])
        if s['reference'] in ('FD_ANALYTIC','COMMON_FINITE_FD'):
            obj.update(xi=old.interval(s['xi']),Qmax=old.rational(s['Qmax']),cells=s['cells'])
        elif s['reference']!='FINITE_NATIVE':raise ValueError('NCDM_REFERENCE_SEMANTICS')
        t['neutrinos'].append(obj)
    t['ede']=None
    if packet['ede'] is not None:
        if packet['ede'].get('n')!=3 or packet['ede'].get('attractor_ic') is not False:raise ValueError('SCF_VARIANT')
        t['ede']={k:old.interval(packet['ede'][k]) for k in ('F','m','B')}
    # Reject noncontiguous input before any candidate PASS.
    for key in ('background_cells','thermal_cells'):
        cells=packet[key]
        if len(cells)>2048:raise ValueError('CELL_COUNT_CAP_UNRESOLVED')
        previous=None
        for cell in cells:
            lo,hi=old.rational(cell['t0']),old.rational(cell['t1'])
            if hi<=lo or lo<=0 or (previous is not None and lo!=previous):raise ValueError('CELL_PARTITION')
            previous=hi
    bg_reports=[];bg_ok=True
    if t['ede'] is not None:
        current=[old.interval(v) for v in packet['background_initial_state']]
        begin=old.rational(packet['background_initial_a'])
        if not packet['background_cells'] or old.rational(packet['background_cells'][0]['t0'])!=begin:raise ValueError('BACKGROUND_INITIAL_PARTITION')
        for cell in packet['background_cells']:
            report=certify_cell(cell,current,lambda a,y:[v/a for v in ede_field(a,y,t)[0]])
            state=[old.interval(v) for v in report['whole_state']]
            b=background(m.I(old.rational(cell['t0']),old.rational(cell['t1'])),t,state)
            report['source_latch_excluded']=value(b['ede_latch']).hi<F(1,2)
            report['forcing']={k:old.pairs(value(v)) for k,v in b.items()}
            report['t0']=cell['t0'];report['t1']=cell['t1']
            bg_reports.append(report);bg_ok&=report['closed'] and report['source_latch_excluded']
            if not bg_ok:break
            current=[old.interval(v) for v in report['endpoint']]
    elif packet['background_cells']:
        raise ValueError('LCDM_BACKGROUND_ODE_NOT_REQUIRED')
    boundaries=list(map(old.rational,packet['source_mode_a']))
    if len(boundaries)!=4 or not 0<boundaries[0]<boundaries[1]<boundaries[2]<boundaries[3]:raise ValueError('SOURCE_BOUNDARY_ORDER')
    if boundaries[3]!=F(1,2871):raise ValueError('Q047_ONSET_BOUNDARY')
    z_end,z_start=map(old.rational,packet['warning_z'])
    if not 0<=z_start<z_end:raise ValueError('WARNING_DOMAIN')
    current=[old.interval(v) for v in packet['thermal_initial_state']]
    if len(current)!=1 or current[0].lo!=0 or current[0].hi!=0:raise ValueError('THERMAL_D_INITIAL_NOT_ZERO')
    init=old.rational(packet['thermal_initial_a'])
    tcells=packet['thermal_cells']
    if not tcells or old.rational(tcells[0]['t0'])!=init or init>=boundaries[0]:raise ValueError('THERMAL_INITIAL_PARTITION')
    reports=[];thermal_ok=bg_ok;mode_ok=True;latch_ok=True
    for cell in tcells:
        lo,hi=old.rational(cell['t0']),old.rational(cell['t1'])
        j=sum(lo>=v for v in boundaries)
        if j>=4 or hi>boundaries[j] or cell['mode']!=MODES[j]:mode_ok=False;break
        if t['ede'] is None:
            getbg=lambda a:background(a,t)
        else:
            candidates=[b for b in bg_reports if old.rational(b['t0'])<=lo and old.rational(b['t1'])>=hi and b['closed']]
            if len(candidates)!=1:thermal_ok=False;break
            ys=[old.interval(v) for v in candidates[0]['whole_state']]
            getbg=lambda a:background(a,t,ys)
        report=certify_cell(cell,current,lambda a,y:[thermal(cell['mode'],a,y[0],t,getbg(a))['rate']/a])
        a=m.I(lo,hi);state=old.interval(report['whole_state'][0]);b=getbg(a)
        info=thermal(cell['mode'],a,state,t,b)
        z=1/a-1
        warning_excluded=(z.lo>=z_end or z.hi<=z_start or value(info['x']).hi<=1)
        report['source_warning_excluded']=warning_excluded
        report['mode']=cell['mode'];report['t0']=cell['t0'];report['t1']=cell['t1']
        report['forcing']={k:old.pairs(value(v)) for k,v in b.items()}
        report['Tmat']=old.pairs(value(info['Tmat']));report['x']=old.pairs(value(info['x']))
        reports.append(report);thermal_ok&=report['closed'];latch_ok&=warning_excluded
        if not thermal_ok:break
        # Source D/w carry is continuous; previous endpoint becomes next initial.
        current=[old.interval(v) for v in report['endpoint']]
    prefix_ok=bg_ok and thermal_ok and mode_ok and latch_ok and len(reports)==len(tcells)
    full=prefix_ok and old.rational(tcells[-1]['t1'])==boundaries[3]
    qb=onset(current[0],m.I(boundaries[3]),t) if full else None
    onset_ok=qb is not None and value(qb).lo>old.EPS
    pred={f'PT{i:02d}':{'status':'UNRESOLVED_ACTUAL_INPUT_OR_LINKAGE'} for i in range(1,12)}
    pred['PT02']={'status':'PASS_CONDITIONAL_REDUCED_VARIANT'}
    pred['PT04']={'status':'PASS_DECLARED_REFERENCE_ONLY','references':[s['reference'] for s in t['neutrinos']]}
    pred['PT05']={'status':'PASS_CONDITIONAL_BACKGROUND' if bg_ok else 'FAIL','cells':len(bg_reports)}
    pred['PT06']={'status':'PASS_CONDITIONAL_D_ZERO_INITIALIZATION'}
    pred['PT07']={'status':('PASS_CONDITIONAL_COMPLETE_PATH' if full else 'PASS_FOR_DECLARED_PREFIX_ONLY') if prefix_ok else 'FAIL'}
    pred['PT08']={'status':'PASS_CONDITIONAL_SOURCE_MODE_CARRY' if mode_ok and latch_ok else 'FAIL','compiled_guard_mapping':'UNRESOLVED'}
    pred['PT09']={'status':'PASS_CONDITIONAL_ONSET' if onset_ok else 'UNRESOLVED','q0':old.pairs(value(qb)) if qb is not None else None}
    pred['PT10']={'status':'NOT_EXECUTED','requirement':'Unchanged M06 full prefix/bracket/rate/right-neighborhood/switch certificate; V1 local fixture is insufficient.'}
    pred['PT11']={'status':'PASS_NO_NATIVE_EXECUTION_SCOPE'}
    return {'q':Q,'case':packet['case'],'scope':packet['scope'],'coordinate':'a',
            'conditional_prefix_gate':'PASS' if prefix_ok else 'FAIL','complete_source_precursor':full,
            'background_cells':bg_reports,'thermal_cells':reports,'predicates':pred,
            'actual_applicability':'INSUFFICIENT_EVIDENCE','final_result_gate':'UNRESOLVED',
            'onset_w':old.pairs(current[0]) if full else None,'thresholds':threshold_report()}

def source_gate(directory,download=False):
    contract=old.load(ROOT/'Q047_PRECURSOR_CONTRACT_V1.json');directory=Path(directory);records={}
    for path,digest in contract['source_sha256'].items():
        local=directory/path
        if download:
            import urllib.request
            url=f'https://raw.githubusercontent.com/mwt5345/class_ede/{SOURCE}/{path}'
            with urllib.request.urlopen(url,timeout=20) as r:data=r.read(2_000_001)
            if len(data)>2_000_000:raise ValueError('SOURCE_SIZE_CAP')
            if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('SOURCE_HASH '+path)
            local.parent.mkdir(parents=True,exist_ok=True);local.write_bytes(data)
        data=local.read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('SOURCE_HASH '+path)
        records[path]={'sha256':digest,'bytes':len(data)}
    return {'q':Q,'source_commit':SOURCE,'source_gate':'PASS_SOURCE_BYTES_ONLY','files':records}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--program-id',default=ID)
    ap.add_argument('--out',default='q047_precursor_results')
    ap.add_argument('--packet');ap.add_argument('--audit-effective')
    ap.add_argument('--source-dir');ap.add_argument('--download-sources',action='store_true')
    ap.add_argument('--static',action='store_true');args=ap.parse_args()
    if args.program_id!=ID or os.getenv('CURRENT_Q',Q)!=Q:raise SystemExit('PROGRAM_ID_OR_Q_GATE')
    out=Path(args.out);started=time.monotonic()
    try:
        import signal
        def limit(signum,frame):raise TimeoutError('FINITE_EXECUTION_TIME_CAP_UNRESOLVED')
        signal.signal(signal.SIGALRM,limit);signal.alarm(90)
        static=package_gate();old.write(out/'q047_precursor_static_v1.json',static)
        if args.static:return
        sources=source_gate(args.source_dir or out/'sourcepins',args.download_sources)
        old.write(out/'q047_precursor_sources_v1.json',sources)
        if args.audit_effective:
            export=old.load(args.audit_effective)
            old.write(out/'q047_effective_audit_v1.json',audit_export(export,ROOT/'Q047_PRECURSOR_CONTRACT_V1.json'))
        packet=old.load(args.packet or ROOT/'q047_precursor_packet_control_v1.json')
        result=verify_packet(packet);old.write(out/'q047_precursor_conditional_v1.json',result)
        contract=old.load(ROOT/'Q047_PRECURSOR_CONTRACT_V1.json')
        actual={key:{'actual_applicability':'INSUFFICIENT_EVIDENCE','inherited_predicate_evidence':v['current_evidence'],
                     'reason':'No admitted source-real effective/init packet is present. The finite control is artificial.'} for key,v in contract['cases'].items()}
        final={'q':Q,'case_id':'NOT_DOCUMENTED','program_id':ID,'result_type':'BUBBLEVERSE_TECHNICAL_EVIDENCE',
               'execution_status':'COMPLETE_FINITE_BACKEND_CONTROL','technical_gate':'PASS',
               'conditional_control_gate':result['conditional_prefix_gate'],
               'control_complete_source_precursor':result['complete_source_precursor'],
               'actual_cases':actual,'final_result_gate':'UNRESOLVED','new_native_evaluations':0,
               'ledger':contract['budget'],'execution_commit':os.getenv('GITHUB_SHA','LOCAL_NOT_REMOTE'),
               'github_run_id':os.getenv('GITHUB_RUN_ID','LOCAL'), 'python':platform.python_version(),
               'duration_seconds':time.monotonic()-started,'sources':contract['sources'],
               'return_route':'RESULT INGESTION & ROUTING ENGINE',
               'scope_limits':['Conditional exact-real source backend only; actual initialized-instance accuracy/linkage unadmitted.',
                 'Finite Taylor work caps and fixed rational boundary primitives; uncertain boundaries need explicit enlargement.',
                 'No native interpolation/binary equivalence; no optical-depth, likelihood or cosmological inference.',
                 'M06 actual downstream first-event certificate not executed.']}
        if result['conditional_prefix_gate']!='PASS' and not args.packet:raise ValueError('MANDATORY_CONTROL_GATE')
        old.write(out/'q047_precursor_final_v1.json',final)
        print(json.dumps({'q':Q,'program_id':ID,'conditional_gate':result['conditional_prefix_gate'],'final_result_gate':'UNRESOLVED'}))
    except Exception as e:
        old.write(out/'q047_precursor_failure_v1.json',{'q':Q,'program_id':ID,'execution_status':'FAILED_OR_UNRESOLVED',
                  'exception':type(e).__name__,'error':str(e),'final_result_gate':'UNRESOLVED','new_native_evaluations':0})
        raise
    finally:
        if 'signal' in locals():signal.alarm(0)

if __name__=='__main__':main()
