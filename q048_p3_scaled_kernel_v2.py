"""Q048 P3 V2 conditional source-real operator admission with MATH018 scaled arithmetic."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json, hashlib, importlib.util
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
_spec=importlib.util.spec_from_file_location('retained_q047_math',HERE/'source/q047_math_v1.py')
_m=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_m)
I=_m.I;iv=_m.iv;const=_m.const;exp_endpoint=_m.exp_endpoint;exp_i=_m.exp_i
Q=2**160
TERMS=42

def ceildiv(a,b): return -(-a//b)
def _atanh_log(m):
    if not 1<=m<=2:raise ValueError('LOG_MANTISSA_DOMAIN')
    t=(m-1)/(m+1)
    tl=(t.numerator*Q)//t.denominator;tu=ceildiv(t.numerator*Q,t.denominator)
    t2l=tl*tl//Q;t2u=ceildiv(tu*tu,Q)
    pl=tl;pu=tu;sl=su=0
    for j in range(TERMS):
        d=2*j+1;sl+=pl//d;su+=ceildiv(pu,d)
        pl=pl*t2l//Q;pu=ceildiv(pu*t2u,Q)
    tail=ceildiv(2*pu*Q,(2*TERMS+1)*(Q-t2u))
    return I(F(2*sl,Q),F(2*su+tail,Q))
LOG2=_atanh_log(F(2))
def log_endpoint(x):
    x=F(x)
    if x<=0:raise ValueError('LOG_NONPOSITIVE')
    k=x.numerator.bit_length()-x.denominator.bit_length()
    m=x/F(2)**k
    if m<1:k-=1;m*=2
    if m>=2:k+=1;m/=2
    assert 1<=m<2
    # Use exact endpoint sums, retaining Q-grid; no hidden libm.
    a=_atanh_log(m)
    return I(a.lo+k*(LOG2.lo if k>=0 else LOG2.hi),
             a.hi+k*(LOG2.hi if k>=0 else LOG2.lo))
def log_i(x):
    x=iv(x)
    if x.lo<=0:raise ValueError('LOG_NONPOSITIVE')
    return I(log_endpoint(x.lo).lo,log_endpoint(x.hi).hi)
def hull(values):return I(min(v.lo for v in values),max(v.hi for v in values))
def encode(x):
    if isinstance(x,I):return {'lo':str(x.lo),'hi':str(x.hi),'display_lo':float(x.lo),'display_hi':float(x.hi)}
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x
def poly_add(a,b):
    n=max(len(a),len(b));return [(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(n)]
def poly_mul(a,b):
    r=[F(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):r[i+j]+=v*w
    return r
def poly_eval(p,x):
    result=iv(0) if isinstance(x,I) else F(0)
    for v in reversed(p):result=result*x+v
    return result
def basis_polynomials():
    return [[F(0),F(-1,3),F(1,2),F(-1,6)],
            [F(1),F(-1,2),F(-1),F(1,2)],
            [F(0),F(1),F(1,2),F(-1,2)],
            [F(0),F(-1,6),F(0),F(1,6)]]
def lagrange_polynomials():
    result=[]
    for j in [-1,0,1,2]:
        p=[F(1)]
        for k in [-1,0,1,2]:
            if j!=k:p=poly_mul(p,[F(-k,j-k),F(1,j-k)])
        result.append(p)
    return result
def weights(x):return [poly_eval(p,iv(x)) for p in basis_polynomials()]
def lagrange_weights(x):
    # Independent product implementation, used by interval subregion control.
    result=[]
    for j in [-1,0,1,2]:
        p=I(1)
        for k in [-1,0,1,2]:
            if j!=k:p=p*(x-k)/(j-k)
        result.append(p)
    return result
def bernstein(p,a,b):
    n=len(p)-1
    c=[sum(p[k]*comb(k,j)*a**(k-j)*(b-a)**j for k in range(j,n+1)) for j in range(n+1)]
    return [sum(c[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
def norm_certificate():
    ps=basis_polynomials()
    if ps!=lagrange_polynomials():raise ValueError('SOURCE_BASIS_NOT_LAGRANGE')
    regions=[];control=[];derivative=F(0)
    for a,signs in [(-1,[1,1,-1,1]),(0,[-1,1,1,-1]),(1,[1,-1,1,1])]:
        b=a+1;p=[F(0)]*4
        for sign,w in zip(signs,ps):p=poly_add(p,[sign*c for c in w])
        coeff=bernstein(p,F(a),F(b))
        dl=sum(max(abs(v) for v in bernstein([i*w[i] for i in range(1,4)],F(a),F(b))) for w in ps)
        derivative=max(derivative,dl)
        regions.append({'domain':[F(a),F(b)],'signed_sum':p,'bernstein':coeff,'l1_upper':max(coeff),'derivative_l1_upper':dl})
    for k in range(12):
        a=F(-1)+F(k,4);b=a+F(1,4)
        upper=sum(w.absmax() for w in lagrange_weights(I(a,b)))
        control.append({'domain':[a,b],'l1_upper':upper})
    return {'primary_regions':regions,'primary_norm':max(r['l1_upper'] for r in regions),
            'control_regions':control,'control_norm':max(r['l1_upper'] for r in control),
            'derivative_l1_upper':derivative,'tensor_norm':F(4),
            'continuity':'C0 across stencil changes; derivative uses either one-sided stencil, not globally C1'}
def stencil(u,n):
    if n<4 or not 0<=u<=n-1:raise ValueError('STENCIL_DOMAIN')
    ix=max(1,min(n-3,u.numerator//u.denominator));return ix,u-ix
def split_coordinate(u,n):
    if n<4 or u.lo<0 or u.hi>n-1:raise ValueError('COORDINATE_DOMAIN')
    parts=[]
    for k in range(u.lo.numerator//u.lo.denominator,u.hi.numerator//u.hi.denominator+1):
        left=max(u.lo,F(k));right=min(u.hi,F(k+1))
        ix=max(1,min(n-3,k))
        parts.append((ix,I(left-ix,right-ix)))
    return parts
def interp1(nodes,u):
    answers=[]
    for ix,x in split_coordinate(u,len(nodes)):
        answers.append(sum((nodes[ix-1+j]*w for j,w in enumerate(weights(x))),I(0)))
    return hull(answers)
def interp2(nodes,v,u):
    answers=[]
    for j,x in split_coordinate(v,len(nodes)):
        for i,y in split_coordinate(u,len(nodes[0])):
            wx=weights(x);wy=weights(y)
            answers.append(sum((nodes[j-1+k][i-1+l]*wx[k]*wy[l] for k in range(4) for l in range(4)),I(0)))
    return hull(answers)
def rate_coordinates(TR,ratio,reference='decimal'):
    TR=iv(TR);ratio=iv(ratio)
    if reference not in ['decimal','binary64']:raise ValueError('REFERENCE_MODE')
    def c(s):return F(s) if reference=='decimal' else F.from_float(float(s))
    trmin=c('.004');trmax=c('.4');rmin=c('.1')
    if TR.lo<trmin or TR.hi>trmax or ratio.lo<rmin or ratio.hi>1/rmin:raise ValueError('LOOKUP_DOMAIN')
    base=log_i(I(trmin));step=(log_i(I(trmax))-base)/99
    rawu=(log_i(TR)-base)/step
    u=I(max(F(0),rawu.lo),min(F(99),rawu.hi))
    branches=[];vs=[]
    if ratio.lo<=1:
        branches.append(0);vs.append((I(ratio.lo,min(ratio.hi,F(1)))-rmin)/((1-rmin)/39))
    if ratio.hi>1:
        branches.append(2);vs.append((1/I(max(ratio.lo,F(1)),ratio.hi)-rmin)/((1-rmin)/39))
    return u,I(max(F(0),min(v.lo for v in vs)),min(F(39),max(v.hi for v in vs))),branches
def loader_alpha(values):
    if len(values)!=16000:raise ValueError('ALPHA_LOADER_LENGTH')
    return [[[values[(i*40+j)*4+l] for i in range(100)] for j in range(40)] for l in range(4)]
def load_tokens(path):return path.read_text().split()
def load_fit(path):
    tok=load_tokens(path)
    if len(tok)!=1325:raise ValueError('FIT_LOADER_LENGTH')
    rows=[[const(s) for s in tok[5*j:5*j+5]] for j in range(265)]
    if any(r[0].lo!=1775+10*j or r[0].hi!=1775+10*j for j,r in enumerate(rows)):raise ValueError('FIT_GRID')
    return rows
def initialize_cases(cap,old):
    expected=['camspec-lcdm','camspec-ede_n3','hillipop-lcdm','hillipop-ede_n3']
    if sorted(cap['cases'])!=sorted(expected) or sorted(old['cases'])!=sorted(expected):raise ValueError('CASE_SET')
    out={}
    for name in expected:
        starts=cap['cases'][name]['thermal_starts'];c=starts[0]['constants']
        keys=['Tcmb','nH0_SI','YHe','fHe_CLASS','fHe_HyRec']
        if len(starts)!=7 or any(any(s['constants'][k]!=c[k] for k in keys) or s['HyRec_MODEL']!=4 for s in starts):raise ValueError('INITIALIZATION_BINDING')
        if c['fHe_CLASS']!=c['fHe_HyRec']:raise ValueError('FHE_BINDING')
        p={k:I(F(v['lo']),F(v['hi'])) for k,v in old['cases'][name]['initialized_parameters'].items() if isinstance(v,dict) and 'lo' in v}
        p.update({k:I(F.from_float(float.fromhex(c[src]))) for k,src in [('T0','Tcmb'),('nH0_SI','nH0_SI'),('YHe','YHe'),('fHe','fHe_HyRec')]})
        p.update(nH0_cm3=p['nH0_SI']*const('1e-6'),fsR=I(1),meR=I(1))
        bg=cap['cases'][name]['background'];fields=bg['fields']
        if any(bg['thermal_flags'][k]!=0 for k in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']):raise ValueError('UNQUALIFIED_PHYSICS_FLAGS')
        h=F.from_float(float.fromhex(fields['H0']))*F(299792458,100000)
        ob=F.from_float(float.fromhex(fields['Omega0_b']))
        oc=F.from_float(float.fromhex(fields['Omega0_cdm']))
        for key,value in [('h',h),('obh2',ob*h*h),('ocbh2',(ob+oc)*h*h)]:
            if not p[key].lo<=value<=p[key].hi:raise ValueError('RETAINED_INIT_SOURCE_BINDING:'+key)
        if p['T0'].lo!=F.from_float(float.fromhex(fields['T_cmb'])):raise ValueError('TCMB_SOURCE_BINDING')
        if min(p[k].lo for k in ['T0','nH0_cm3','h','obh2','ocbh2','Neff','fHe'])<=0 or not 0<p['YHe'].lo<=p['YHe'].hi<1:raise ValueError('COSMO_DOMAIN')
        out[name]=p
    return out
def fit_admission(rows,p,norm):
    factor=(const('2.7255')/p['T0'])**3
    diffs=[(p['ocbh2']-const('.14175'))*factor,
           (p['obh2']*(1-p['YHe'])-const('.02242')*(1-const('.246738546372')))*factor,
           p['Neff']-const('3.046')]
    combined=[r[1]+sum((d*r[j+2] for j,d in enumerate(diffs)),I(0)) for r in rows]
    m=min(v.lo for v in combined);M=max(v.hi for v in combined);center=(m+M)/2;radius=(M-m)/2
    primary=I(center-norm['primary_norm']*radius,center+norm['primary_norm']*radius)
    # Separate column bound, using product-Lagrange interval control norm.
    columns=[max(r[j].absmax() for r in rows) for j in range(1,5)]
    control_abs=norm['control_norm']*(columns[0]+sum(d.absmax()*columns[j+1] for j,d in enumerate(diffs)))
    control=I(-control_abs,control_abs)
    pd=1+primary;cd=1+control
    if pd.lo<=0 or cd.lo<=0:raise ValueError('FIT_DENOMINATOR_NOT_CERTIFIED')
    return {'diff':diffs,'combined_nodal_range':I(m,M),'primary_DK':primary,'control_DK':control,
            'primary_denominator':pd,'control_denominator':cd,'high_T_DK':I(0),
            'primary_dDK_dT_abs_upper':norm['derivative_l1_upper']*radius/10,
            'valid_temperature_K':[1775,4415],'requires_radiation_identity':True}
def global_log_admission(nodes,norm,dimensions):
    values=[v for row in nodes for v in row] if dimensions==2 else nodes
    lo=min(v.lo for v in values);hi=max(v.hi for v in values)
    center=(lo+hi)/2;radius=(hi-lo)/2
    factor=norm['primary_norm']**dimensions
    bracket=I(center-factor*radius,center+factor*radius)
    if bracket.lo<=-400 or bracket.hi>=400:raise ValueError('EXP_REFERENCE_CAP')
    result=exp_i(bracket)
    if result.lo<=0:raise ValueError('EXP_POSITIVE_LOWER_REQUIRED')
    return {'nodes_log_range':I(lo,hi),'operator_log_range':bracket,'rate_range':result,
            'nodal_log_width_max':max(v.hi-v.lo for v in values),
            'nodal_error_amplification':factor,
            'dlog_dnormalized_coordinate_abs_upper':norm['derivative_l1_upper']*radius*norm['primary_norm']**(dimensions-1)}
def interpolate_atomic(alpha,rr,TR,ratio,reference='decimal'):
    u,v,channels=rate_coordinates(TR,ratio,reference)
    def bounded_exp(local,nodes,dimensions):
        # Intersect with the independently proved global centered bound before
        # exponentiating wide coordinate intervals; interval dependency alone
        # must not cause a spurious source-domain failure.
        vals=[t for row in nodes for t in row] if dimensions==2 else nodes
        mn=min(t.lo for t in vals);mx=max(t.hi for t in vals)
        c=(mn+mx)/2;radius=(mx-mn)/2;f=F(2)**dimensions
        bracket=I(max(local.lo,c-f*radius),min(local.hi,c+f*radius))
        if not -400<bracket.lo<=bracket.hi<400:raise ValueError('EXP_REFERENCE_CAP')
        return exp_i(bracket)
    eq=[bounded_exp(interp1(alpha[l][39],u),alpha[l][39],1) for l in range(2)]
    a=[hull([bounded_exp(interp2(alpha[l+ch],v,u),alpha[l+ch],2) for ch in channels]) for l in range(2)]
    return {'Alpha':a,'Alpha_eq':eq,'DAlpha':[a[l]-eq[l] for l in range(2)],'R2p2s':bounded_exp(interp1(rr,u),rr,1)}
def verify_inputs(config):
    for path,rec in config['inputs'].items():
        data=(ROOT/path).read_bytes()
        if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:raise ValueError('INPUT_HASH:'+path)


# ==================== P3 V2 SCALED-ARITHMETIC OVERRIDES ====================
from q048_p3_scaled_arithmetic_v2 import (
    primary_exp_point as _v2_primary_exp_point,
    control_exp_point as _v2_control_exp_point,
    table_log_union as v2_table_log_union,
    scaled_mul as v2_scaled_mul,
    scaled_recip as v2_scaled_recip,
    unit_scaled as v2_unit_scaled,
    encode_scaled as v2_encode_scaled,
)

def exp_endpoint(x):
    """V2 primary dynamic scaled exp, converted to exact Fraction interval."""
    s=_v2_primary_exp_point(F(x))
    return I(s.lo_fraction,s.hi_fraction)

def exp_control_endpoint(x):
    s=_v2_control_exp_point(F(x))
    return I(s.lo_fraction,s.hi_fraction)

def exp_i(x):
    x=iv(x)
    return I(exp_endpoint(x.lo).lo,exp_endpoint(x.hi).hi)

def global_log_admission(nodes,norm,dimensions):
    values=[v for row in nodes for v in row] if dimensions==2 else nodes
    lo=min(v.lo for v in values);hi=max(v.hi for v in values)
    center=(lo+hi)/2;radius=(hi-lo)/2
    factor=norm['primary_norm']**dimensions
    bracket=I(center-factor*radius,center+factor*radius)
    # V2 has no absolute +/-400 exp cap. It uses dynamic binary range reduction.
    lower_primary=exp_endpoint(bracket.lo); upper_primary=exp_endpoint(bracket.hi)
    lower_control=exp_control_endpoint(bracket.lo); upper_control=exp_control_endpoint(bracket.hi)
    result=I(lower_primary.lo,upper_primary.hi)
    control=I(lower_control.lo,upper_control.hi)
    if result.lo<=0 or control.lo<=0:
        raise ValueError('SCALED_EXP_POSITIVE_LOWER_REQUIRED')
    return {'nodes_log_range':I(lo,hi),'operator_log_range':bracket,'rate_range':result,
            'control_rate_range':control,
            'nodal_log_width_max':max(v.hi-v.lo for v in values),
            'nodal_error_amplification':factor,
            'dlog_dnormalized_coordinate_abs_upper':norm['derivative_l1_upper']*radius*norm['primary_norm']**(dimensions-1)}

def interpolate_atomic(alpha,rr,TR,ratio,reference='decimal'):
    u,v,channels=rate_coordinates(TR,ratio,reference)
    def bounded_exp(local,nodes,dimensions):
        vals=[t for row in nodes for t in row] if dimensions==2 else nodes
        mn=min(t.lo for t in vals);mx=max(t.hi for t in vals)
        c=(mn+mx)/2;radius=(mx-mn)/2;f=F(2)**dimensions
        bracket=I(max(local.lo,c-f*radius),min(local.hi,c+f*radius))
        if bracket.lo>bracket.hi:raise ValueError('EMPTY_OPERATOR_INTERSECTION')
        return exp_i(bracket)
    eq=[bounded_exp(interp1(alpha[l][39],u),alpha[l][39],1) for l in range(2)]
    a=[hull([bounded_exp(interp2(alpha[l+ch],v,u),alpha[l+ch],2) for ch in channels]) for l in range(2)]
    return {'Alpha':a,'Alpha_eq':eq,'DAlpha':[a[l]-eq[l] for l in range(2)],'R2p2s':bounded_exp(interp1(rr,u),rr,1)}

def verify_inputs(config):
    for path,rec in config['inputs'].items():
        data=(ROOT/path).read_bytes()
        if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:
            raise ValueError('INPUT_HASH:'+path)


# V2 display override: exact fractions remain authoritative; Decimal display avoids
# binary64 underflow-to-0.0 in user-facing orientation fields.
from decimal import Decimal as _D, localcontext as _lc
def _v2_display_fraction(x):
    x=F(x)
    with _lc() as ctx:
        ctx.prec=28
        return format(_D(x.numerator)/_D(x.denominator),'.20E')
def encode(x):
    if isinstance(x,I):
        return {'lo':str(x.lo),'hi':str(x.hi),
                'display_lo':_v2_display_fraction(x.lo),
                'display_hi':_v2_display_fraction(x.hi)}
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x
