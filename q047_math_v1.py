"""Q047 mathematical controls only; no cosmological integration or event claim.
Exact rational outward arithmetic with a fixed decimal lattice, exp Taylor
remainder bounds, integer-square-root enclosures, and two-variable interval AD.
This small evaluator is not a general validated IVP solver.
"""
from fractions import Fraction as F
from math import isqrt, nextafter, inf, exp, sqrt, pi
from pathlib import Path
import json, hashlib, sys

DEN = 10**120
def down(x): return F((x.numerator*DEN)//x.denominator,DEN)
def up(x): return -down(-x)
def frac(x): return x if isinstance(x,F) else F(str(x))
class I:
    def __init__(self,lo,hi=None):
        self.lo=frac(lo);self.hi=frac(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def rounded(lo,hi): return I(down(lo),up(hi))
    def __add__(a,b):
        if isinstance(b,A):return NotImplemented
        b=iv(b);return I.rounded(a.lo+b.lo,a.hi+b.hi)
    __radd__=__add__
    def __neg__(a):return I(-a.hi,-a.lo)
    def __sub__(a,b):
        if isinstance(b,A):return NotImplemented
        return a+-iv(b)
    def __rsub__(a,b):return iv(b)+-a
    def __mul__(a,b):
        if isinstance(b,A):return NotImplemented
        b=iv(b);p=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]
        return I.rounded(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(a,b):
        if isinstance(b,A):return NotImplemented
        b=iv(b);assert not b.lo<=0<=b.hi
        return a*I.rounded(1/b.hi,1/b.lo)
    def __rtruediv__(a,b):return iv(b)/a
    def __pow__(a,n):
        assert isinstance(n,int) and n>=0
        r=I(1)
        for _ in range(n):r=r*a
        return r
    def absmax(a):return max(abs(a.lo),abs(a.hi))
def iv(x):return x if isinstance(x,I) else I(x)
def sqrt_endpoint(x):
    assert x>=0
    n=isqrt((x.numerator*DEN*DEN)//x.denominator)
    lo=F(n,DEN);hi=F(n+1,DEN)
    assert lo*lo<=x<=hi*hi
    return lo,hi
def sqrt_i(x):
    x=iv(x);return I(sqrt_endpoint(x.lo)[0],sqrt_endpoint(x.hi)[1])
def exp_endpoint(x):
    if x>400:raise ValueError('EXP_RANGE_CAP: positive exponential outside bounded checker range')
    if x<=-400:
        # e>2, hence e^-400 < 2^-400 < 10^-120.
        assert F(1,2**400)<F(1,DEN)
        return I(0,F(1,DEN))
    if x<0:return 1/exp_endpoint(-x)
    k=0;y=x
    while y>F(1,8):y/=2;k+=1
    term=F(1);s=term
    for n in range(1,41):term*=y/n;s+=term
    next_term=term*y/41
    # All subsequent term ratios <= y/42; a geometric tail encloses them.
    tail=next_term/(1-y/42)
    r=I.rounded(s,s+tail)
    for _ in range(k):r=r*r
    return r
def exp_i(x):
    x=iv(x);return I(exp_endpoint(x.lo).lo,exp_endpoint(x.hi).hi)
class A:
    def __init__(self,v,d=None):self.v=iv(v);self.d=d or [I(0),I(0)]
    def __add__(a,b):
        b=ad(b);return A(a.v+b.v,[a.d[i]+b.d[i] for i in range(2)])
    __radd__=__add__
    def __neg__(a):return A(-a.v,[-x for x in a.d])
    def __sub__(a,b):return a+-ad(b)
    def __rsub__(a,b):return ad(b)+-a
    def __mul__(a,b):
        b=ad(b);return A(a.v*b.v,[a.d[i]*b.v+a.v*b.d[i] for i in range(2)])
    __rmul__=__mul__
    def __truediv__(a,b):
        b=ad(b);return A(a.v/b.v,[(a.d[i]*b.v-a.v*b.d[i])/(b.v*b.v) for i in range(2)])
    def __rtruediv__(a,b):return ad(b)/a
    def __pow__(a,n):
        assert n>=0;return A(a.v**n,[n*(a.v**(n-1))*v for v in a.d]) if n else A(1)
def ad(x):return x if isinstance(x,A) else A(x)
def root(x):
    if isinstance(x,A):
        v=sqrt_i(x.v);return A(v,[d/(2*v) for d in x.d])
    return sqrt_i(x)
def ex(x):
    if isinstance(x,A):
        v=exp_i(x.v);return A(v,[v*d for d in x.d])
    return exp_i(x)
def const(s):
    # Covers exact source decimal and exact IEEE-754 binary64 parsed value.
    literal=F(s);binary=F.from_float(float(s));return I(min(literal,binary),max(literal,binary))
C={
 'pi':const('3.1415926535897932384626433832795'),
 'me':const('9.10938215e-31'),'hp':const('6.62606896e-34'),
 'kb':const('1.3806504e-23'),'c':const('2.99792458e8'),
 'ionH':const('1.096787737e7'),'ionHe':const('1.98310772e7'),
 'sigma':const('6.6524616e-29'),'Mpc':const('3.085677581282e22'),
 'G':const('6.67428e-11'),'rhoJ':const('0.0151730087')
}
CNR=2*C['pi']*C['me']*C['kb']/(C['hp']**2)
IH=C['hp']*C['c']*C['ionH']/C['kb']
IHe=C['hp']*C['c']*C['ionHe']/C['kb']
# Also encloses strict normal binary64 evaluation of these short source
# products/quotients (gamma_10 < 10^-14). No libm assumption enters this part.
PAD=I(1-F('1e-14'),1+F('1e-14'))
CNR=CNR*PAD;IH=IH*PAD;IHe=IHe*PAD
def hydrogen(q,w,z,T0,n0):
    T=(1-w)*T0*(1+z)
    p=CNR*T/((1+z)**2)
    r=p*root(p)*ex(-IH/T)/n0
    # h^2+(q+r)h-r=0. The positive root increases with r and
    # decreases with q. Corner evaluation avoids repeated-r dependency,
    # which otherwise falsely permits h>=1 near the ionized onset.
    qv=q.v if isinstance(q,A) else iv(q)
    rv=r.v if isinstance(r,A) else iv(r)
    if qv.lo<0 or rv.lo<=0:raise ValueError('HYDROGEN_REGULAR_DOMAIN')
    def corner(qc,rc):
        qq=I(qc);rr=I(rc)
        return 2*rr/(rr+qq+sqrt_i((rr+qq)**2+4*rr))
    hv=I(corner(qv.hi,rv.lo).lo,corner(qv.lo,rv.hi).hi)
    if isinstance(q,A) or isinstance(r,A):
        qa=ad(q);ra=ad(r)
        # Implicit derivatives, with a positive neutral-fraction identity.
        neutral=hv*(hv+qv)/rv
        denominator=2*hv+qv+rv
        h=A(hv,[(neutral*ra.d[i]-hv*qa.d[i])/denominator for i in range(2)])
    else:h=hv
    return h,r,T
def helium_initial(w,z,T0,n0,f):
    T=(1-w)*T0*(1+z);p=CNR*T/((1+z)**2)
    r=4*p*root(p)*ex(-IHe/T)/n0
    return 2*f*r/(1+r+root((1+r)**2+4*f*r))
def flow(q,w,z,T0,n0,f,Hmpc,rhog):
    h,r,T=hydrogen(q,w,z,T0,n0)
    Tg=T0*(1+z);n=n0*((1+z)**3)/10**6;Hs=Hmpc*C['c']/C['Mpc']
    s0=4*const('2.414194e15')*Tg*root(Tg)/n
    s=s0*ex(-const('285325')/Tg)
    y2s=ex(const('46090')/Tg)/s0;y2p=3*ex(const('39101')/Tg)/s0
    # Exact same neutral fraction as 1-h, without subtractive cancellation.
    neutral=h*(h+q)/r
    eta=const('9.15776e22')*Hs/n/neutral
    g=const('1.976e6')/(1-ex(-const('6989')/Tg))
    for a,b in [('6.03e6','19754'),('1.06e8','21539'),('2.18e6','28496'),('3.37e7','29224'),('1.04e6','32414'),('1.51e7','32781')]:
        g=g+const(a)/(ex(const(b)/Tg)-1)
    tau=const('4.277e-8')*n/Hs*(f-q)
    tauc=g*tau/(4*C['pi']**2)/eta
    enh=root(1+C['pi']**2*tauc)+const('7.74')*tauc/(1+70*tauc)
    pesc=enh/tau+(1-ex(-const('1.023e-7')*tau))*(const('0.964525')*ex(const('2947')/Tg)-enh*ex(-const('6.14e13')/eta))/tau
    K=(const('50.94')*y2s+const('1.7989e9')*y2p*pesc)/Hs
    D=(f-q)*s-q*(q+h)
    beta=8*C['sigma']*rhog*C['rhoJ']/(3*C['me']*C['c']*Hs)*(h+q)/(1+f+h+q)
    return K*D,1-(1+beta)*w,{'h':h,'rH':r,'Tmat':T,'beta':beta,'D':D,'K':K}
def js(x):
    if isinstance(x,A):return {'value':js(x.v),'dq':js(x.d[0]),'dw':js(x.d[1])}
    if isinstance(x,I):return {'lo':str(float(x.lo)),'hi':str(float(x.hi)),'lo_exact':str(x.lo),'hi_exact':str(x.hi)}
    return x
def cc_interval(V,E):
    V=float(V);E=float(E);v=F.from_float(V);e=F.from_float(E)
    L=(F.from_float(nextafter(V,-inf))+v)/2-e
    U=(v+F.from_float(nextafter(V,inf)))/2-e
    assert L>0
    c=F.from_float(float('3.968e-8'));unit=F(1,2**53)
    return I(L/(c*(1+unit)),U/(c*(1-unit)))

def independent_float_flow(q,w,z,T0,n0,f,Hmpc,rhog):
    """Binary64 source-style formula; diagnostic cross-check, not a certificate."""
    me=9.10938215e-31;hp=6.62606896e-34;kb=1.3806504e-23;c=2.99792458e8
    T=(1-w)*T0*(1+z);Cnr=2*pi*(me/hp)*(kb/hp);ion=hp*c*1.096787737e7/kb
    r=(Cnr*T/(1+z)**2)**1.5*exp(-ion/T)/n0
    h=2/(1+q/r+sqrt((1+q/r)**2+4/r))
    Tg=T0*(1+z);n=n0*(1+z)**3/1e6;Hs=Hmpc*c/3.085677581282e22
    s0=4*2.414194e15*Tg*sqrt(Tg)/n;s=s0*exp(-285325/Tg)
    eta=9.15776e22*Hs/n/(1-h)
    g=1.976e6/(1-exp(-6989/Tg))
    for a,b in [(6.03e6,19754),(1.06e8,21539),(2.18e6,28496),(3.37e7,29224),(1.04e6,32414),(1.51e7,32781)]:g+=a/(exp(b/Tg)-1)
    tau=4.277e-8*n/Hs*(f-q);tauc=g*tau/(4*pi*pi)/eta
    enh=sqrt(1+pi*pi*tauc)+7.74*tauc/(1+70*tauc)
    pesc=enh/tau+(1-exp(-1.023e-7*tau))*(.964525*exp(2947/Tg)-enh*exp(-6.14e13/eta))/tau
    K=(50.94*exp(46090/Tg)/s0+1.7989e9*3*exp(39101/Tg)/s0*pesc)/Hs
    beta=8*6.6524616e-29*rhog*.0151730087/(3*me*c*Hs)*(h+q)/(1+f+h+q)
    return [K*((f-q)*s-q*(q+h)),1-(1+beta)*w]

def main():
    if sys.flags.optimize:raise RuntimeError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    rootdir=Path(__file__).resolve().parent
    incoming=json.loads((rootdir/'q047_control_input_v1.json').read_text())
    n0=I('.1880','.1889');f=I('.0818','.0820');T0=I('2.7254','2.7256');eps=I('1e-6')
    # Corner extremality follows from explicit monotonic derivatives in the journal.
    hmin,_,_=hydrogen(I('1.5e-6'),I('.01'),I(1600),I(T0.lo),I(n0.hi))
    z=I(1700);tg=I(T0.hi)*(1+z)
    smax=4*const('2.414194e15')*tg*root(tg)*ex(-const('285325')/tg)/(I(n0.lo)*((1+z)**3)/10**6)
    Dmax=(I(f.hi)-eps)*smax-eps*(eps+I(hmin.lo))
    assert Dmax.hi<0
    Tminimum=I('.99')*I(T0.lo)*1601
    damping_loss=I('.01')*(I('1.5')+IH/Tminimum)/(2*I('.99'))
    assert damping_loss.hi<1
    initial_lo=helium_initial(I('.01'),I(2870),I(T0.lo),I(n0.hi),I(f.lo))
    initial_hi=helium_initial(I(0),I(2870),I(T0.hi),I(n0.lo),I(f.hi))
    initial_q=I(initial_lo.lo,initial_hi.hi)
    assert initial_q.lo>eps.hi and initial_q.hi<f.hi
    result={'arithmetic':'Exact rational outward lattice 10^-120; rigorous Taylor exp tails and integer sqrt. Only fixed-box algebra, no trajectory integration.',
      'conditional_box':{'z':[1600,1700],'w':[0,.01],'q':[.5e-6,1.5e-6],'f':[.0818,.0820],'n0_m3':[.1880,.1889],'T0_K':[2.7254,2.7256]},
      'h_lower_bound':js(hmin),'s_upper_bound':js(smax),'D_epsilon_upper_bound':js(Dmax),
      'temperature_damping_fraction_loss_upper':js(damping_loss),'onset_q_box':js(initial_q),'local_certificates':{},'conditional_CC_intervals':{},'new_cosmology_evaluations':0}
    for case,record in incoming['cases'].items():
        row=record['native_hint'];z0=F(row['z']);H0=F(row['H_1_Mpc'])
        near=record['temperature_neighbor'];w0=1-F(near['Tb [K]'])/(F('2.7255')*(1+F(near['z'])))
        assert w0>=0
        # Source background component rho_g = Omega_g H0^2/a^4.
        first=record['first_background_raw'];gamma0=F(first['(.)rho_g'])/(1+F(first['z']))**4
        q=A(I('0.999e-6','1.001e-6'),[I(1),I(0)])
        w=A(I(w0-F('1e-8'),w0+F('1e-8')),[I(0),I(1)])
        assert w.v.lo>=0
        zz=I(z0-F('.001'),z0+F('.001'));HH=I(H0-F('.001'),H0+F('.001'))
        native_n=json.loads(record['native_meta_text'],parse_float=F)['nH0_m3']
        native_f=json.loads(record['native_meta_text'],parse_float=F)['fHe']
        nn=I(native_n-F('1e-12'),native_n+F('1e-12'));ff=I(native_f-F('1e-12'),native_f+F('1e-12'))
        rho=I(gamma0*(1-F('1e-8')),gamma0*(1+F('1e-8')))*(1+zz)**4
        Q,G,extra=flow(q,w,zz,I('2.725499999','2.725500001'),nn,ff,HH,rho)
        a=Q.d[0].hi;b=Q.d[1].absmax();c=G.d[0].absmax();d=G.d[1].hi
        assert a<0 and d<0 and b*c<a*d
        kappa=F(1);weighted=max(a+b*kappa,d+c/kappa)
        assert weighted<F(-230)
        assert extra['K'].v.lo>0 and extra['D'].v.hi<0
        args=[float(z0),2.7255,float(native_n),float(native_f),float(H0),float(gamma0*(1+z0)**4)]
        q0=1e-6;ww=float(w0);fd=[]
        for component in range(2):
            delta=1e-10
            left=independent_float_flow(q0-delta if component==0 else q0,ww-delta if component==1 else ww,*args)
            right=independent_float_flow(q0+delta if component==0 else q0,ww+delta if component==1 else ww,*args)
            column=[(right[i]-left[i])/(2*delta) for i in range(2)]
            for i,field in enumerate([Q,G]):assert float(field.d[component].lo)<=column[i]<=float(field.d[component].hi),(case,i,component,column[i])
            fd.append(column)
        result['local_certificates'][case]={'scope':'Conditional rectangle around native hints, not a reached-state enclosure','z':js(zz),'H_Mpc_inv':js(HH),'w':js(w.v),'f':js(ff),'n0_m3':js(nn),'gamma0_CLASS':str(gamma0),'gamma0_relative_box':1e-8,'T0_K':[2.725499999,2.725500001],'q':js(q.v),'nearest_native_temperature_row':near,'Q':js(Q),'G':js(G),'auxiliary':{k:js(v) for k,v in extra.items()},'comparison_M':[[str(a),str(b)],[str(c),str(d)]],'kappa':str(kappa),'weighted_log_norm_upper':str(weighted),'contraction_verified_on_box':True,'independent_binary64_fd_columns_diagnostic':fd,'fd_inside_interval_derivatives':True}
        if 'scalar_first_row_for_CC' in record:
            r=record['scalar_first_row_for_CC'];result['conditional_CC_intervals'][case]=js(cc_interval(r['V_scf'],r['V_e_scf']))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
