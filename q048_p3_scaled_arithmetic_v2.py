"""Q048 P3 V2 dynamic scaled/relative arithmetic.

New candidate only. Preserves positive sub-1e-120 values with significant
binary fixed-point mantissas and explicit binary exponents. It is a
conditional source-real arithmetic component, not native libc/P6 evidence.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from functools import lru_cache

PRIMARY_BITS=384
CONTROL_BITS=448
LOG_TERMS=140
PRIMARY_EXP_TERMS=100
CONTROL_EXP_TERMS=40
CONTROL_HALVINGS=8
LOG_SLACK_BITS=180
ARGUMENT_CAP=4096

def fl_div(a,b): return a//b
def ce_div(a,b): return -((-a)//b)

def pow2_frac(e):
    return F(1<<e,1) if e>=0 else F(1,1<<(-e))

def frac_floor_scaled(q,p):
    q=F(q); return (q.numerator*(1<<p))//q.denominator

def frac_ceil_scaled(q,p):
    q=F(q); return -((-q.numerator*(1<<p))//q.denominator)

def frac_iv(q,p): return (frac_floor_scaled(q,p),frac_ceil_scaled(q,p))
def iv_add(a,b): return (a[0]+b[0],a[1]+b[1])
def iv_mul_int(a,n): return (a[0]*n,a[1]*n) if n>=0 else (a[1]*n,a[0]*n)
def iv_div_pos_int(a,n): return (fl_div(a[0],n),ce_div(a[1],n))

def iv_mul(a,b,p):
    S=1<<p
    ps=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return (fl_div(min(ps),S),ce_div(max(ps),S))

def iv_recip_pos(a,p):
    if a[0]<=0: raise ValueError("RECIP_NONPOSITIVE")
    S=1<<p
    return (fl_div(S*S,a[1]),ce_div(S*S,a[0]))

def floor_log2_frac(q):
    q=F(q)
    if q<=0: raise ValueError("LOG_NONPOSITIVE")
    e=q.numerator.bit_length()-q.denominator.bit_length()
    while q<pow2_frac(e): e-=1
    while q>=pow2_frac(e+1): e+=1
    return e

def ln_m_from_exact_m(m,p,N):
    if not F(1)<=m<F(2): raise ValueError("LOG_MANTISSA_DOMAIN")
    y=(m-1)/(m+1)
    yiv=frac_iv(y,p); y2=iv_mul(yiv,yiv,p); yp=yiv; acc=(0,0)
    for j in range(N):
        acc=iv_add(acc,iv_div_pos_int(yp,2*j+1))
        yp=iv_mul(yp,y2,p)
    acc=iv_mul_int(acc,2)
    rem_hi=ce_div(9*max(0,yp[1]),4*(2*N+1))
    return (acc[0],acc[1]+rem_hi)

@lru_cache(None)
def ln2_iv(p,N=LOG_TERMS):
    y=F(1,3); yiv=frac_iv(y,p); y2=iv_mul(yiv,yiv,p); yp=yiv; acc=(0,0)
    for j in range(N):
        acc=iv_add(acc,iv_div_pos_int(yp,2*j+1))
        yp=iv_mul(yp,y2,p)
    acc=iv_mul_int(acc,2)
    rem_hi=ce_div(9*max(0,yp[1]),4*(2*N+1))
    return (acc[0],acc[1]+rem_hi)

def ln_q_iv(q,p=PRIMARY_BITS,N=LOG_TERMS,l2=None):
    q=F(q); e=floor_log2_frac(q); m=q/pow2_frac(e)
    lm=ln_m_from_exact_m(m,p,N)
    if l2 is None: l2=ln2_iv(p,N)
    return iv_add(lm,iv_mul_int(l2,e))

def decimal_binary_union(token):
    dec=F(token)
    binary=F.from_float(float(token))
    return min(dec,binary),max(dec,binary),dec,binary

def table_log_union(token,p=PRIMARY_BITS,N=LOG_TERMS,slack_bits=LOG_SLACK_BITS):
    qlo,qhi,dec,binary=decimal_binary_union(token)
    if qlo<=0: raise ValueError("LOG_INPUT_NONPOSITIVE")
    l2=ln2_iv(p,N)
    lo=ln_q_iv(qlo,p,N,l2)[0]
    hi=ln_q_iv(qhi,p,N,l2)[1]
    slack=1<<(p-slack_bits)
    return {
        "lo_int":lo-slack, "hi_int":hi+slack, "scale_bits":p,
        "lo":F(lo-slack,1<<p),"hi":F(hi+slack,1<<p),
        "qlo":qlo,"qhi":qhi,"decimal":dec,"binary64":binary
    }

def _nearest_integer(q):
    q=F(q); n=q.numerator//q.denominator
    # nearest with ties away from relying on float
    if q-F(n)>=F(1,2): n+=1
    return int(n)

def _reduced_fixed(x,p):
    x=F(x)
    if abs(x)>ARGUMENT_CAP: raise ValueError("EXP_ARGUMENT_DOMAIN")
    l2=ln2_iv(p,LOG_TERMS)
    mid=F(l2[0]+l2[1],2*(1<<p))
    k=_nearest_integer(x/mid)
    xlo=frac_floor_scaled(x,p); xhi=frac_ceil_scaled(x,p)
    if k>=0:
        r=(xlo-k*l2[1],xhi-k*l2[0])
    else:
        r=(xlo-k*l2[0],xhi-k*l2[1])
    S=1<<p
    # nearest reduction should place |r| < ~ln2/2; explicit guard
    if r[0]<=-S or r[1]>=S:
        raise ValueError("REDUCED_ARGUMENT_DOMAIN")
    return k,r,l2

def exp_positive_iv(riv,p,N):
    S=1<<p
    if riv[0]<0 or riv[1]>=S: raise ValueError("POS_EXP_DOMAIN")
    term=(S,S); acc=(S,S)
    for n in range(1,N+1):
        term=iv_div_pos_int(iv_mul(term,riv,p),n)
        acc=iv_add(acc,term)
    nxt=iv_div_pos_int(iv_mul(term,riv,p),N+1)
    # r < 1 => remaining terms <= next*(N+2)/(N+1)
    rem_hi=ce_div(max(0,nxt[1])*(N+2),N+1)
    return (acc[0],acc[1]+rem_hi)

def exp_signed_iv(riv,p,N):
    if riv[0]>=0:
        return exp_positive_iv(riv,p,N)
    if riv[1]<=0:
        pos=(-riv[1],-riv[0])
        return iv_recip_pos(exp_positive_iv(pos,p,N),p)
    # monotonic split at zero
    lower=iv_recip_pos(exp_positive_iv((0,-riv[0]),p,N),p)[0]
    upper=exp_positive_iv((0,riv[1]),p,N)[1]
    return (lower,upper)

@dataclass(frozen=True)
class ScaledInterval:
    lo:int
    hi:int
    p:int
    e2:int
    def __post_init__(self):
        if self.lo<=0 or self.lo>self.hi: raise ValueError("SCALED_INTERVAL_DOMAIN")
    @property
    def lo_fraction(self): return F(self.lo,1<<self.p)*pow2_frac(self.e2)
    @property
    def hi_fraction(self): return F(self.hi,1<<self.p)*pow2_frac(self.e2)

def primary_exp_point(x):
    k,r,_=_reduced_fixed(F(x),PRIMARY_BITS)
    m=exp_signed_iv(r,PRIMARY_BITS,PRIMARY_EXP_TERMS)
    return ScaledInterval(m[0],m[1],PRIMARY_BITS,k)

def control_exp_point(x):
    k,r,_=_reduced_fixed(F(x),CONTROL_BITS)
    scale=1<<CONTROL_HALVINGS
    u=(fl_div(r[0],scale),ce_div(r[1],scale))
    m=exp_signed_iv(u,CONTROL_BITS,CONTROL_EXP_TERMS)
    for _ in range(CONTROL_HALVINGS):
        m=iv_mul(m,m,CONTROL_BITS)
    return ScaledInterval(m[0],m[1],CONTROL_BITS,k)

def scaled_mul(a,b):
    if a.p!=b.p: raise ValueError("SCALE_BITS_MISMATCH")
    p=a.p; S=1<<p
    return ScaledInterval(fl_div(a.lo*b.lo,S),ce_div(a.hi*b.hi,S),p,a.e2+b.e2)

def scaled_recip(a):
    p=a.p; S=1<<p
    return ScaledInterval(fl_div(S*S,a.hi),ce_div(S*S,a.lo),p,-a.e2)

def unit_scaled(p=PRIMARY_BITS):
    return ScaledInterval(1<<p,1<<p,p,0)

def encode_scaled(a):
    return {"lo":str(a.lo),"hi":str(a.hi),"scale_bits":a.p,"binary_exponent":a.e2,
            "lo_fraction":str(a.lo_fraction),"hi_fraction":str(a.hi_fraction)}
