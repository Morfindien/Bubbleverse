"""Q-042 real-table interval RHS. MPFR 4.2.1, 256-bit intermediates.

All arithmetic endpoints use MPFR_RNDD/RNDU, including binary64 export.
This does NOT certify the original binary's arithmetic or a solution history.
Domain/cap failures are returned to the caller, never clipped into success.
Only the frozen no-injection/no-varconst/reio_camb/HyRec domain is supported.
"""
import ctypes as C
import ctypes.util
import hashlib, math, platform
from pathlib import Path

class BackendError(ValueError): pass

class MP(C.Structure):
    _fields_=[('precision',C.c_long),('sign',C.c_int),('exponent',C.c_long),('limbs',C.POINTER(C.c_ulong))]

if platform.machine() not in ('x86_64','AMD64') or C.sizeof(C.c_long)!=8 or C.sizeof(MP)!=32:
    raise BackendError('MPFR_ABI_GATE: requires Linux x86_64 LP64')
lib=C.CDLL(ctypes.util.find_library('mpfr') or 'libmpfr.so.6')
lib.mpfr_get_version.restype=C.c_char_p
VERSION=lib.mpfr_get_version().decode()
if VERSION!='4.2.1': raise BackendError('MPFR_VERSION_GATE: '+VERSION)
P=C.POINTER(MP)
lib.mpfr_init2.argtypes=[P,C.c_long];lib.mpfr_init2.restype=None
lib.mpfr_clear.argtypes=[P];lib.mpfr_clear.restype=None
lib.mpfr_set_d.argtypes=[P,C.c_double,C.c_int];lib.mpfr_set_d.restype=C.c_int
lib.mpfr_get_d.argtypes=[P,C.c_int];lib.mpfr_get_d.restype=C.c_double
lib.mpfr_print_rnd_mode.argtypes=[C.c_int];lib.mpfr_print_rnd_mode.restype=C.c_char_p
if lib.mpfr_print_rnd_mode(2)!=b'MPFR_RNDU' or lib.mpfr_print_rnd_mode(3)!=b'MPFR_RNDD':
    raise BackendError('MPFR_ROUNDING_ENUM_GATE')
for name in ('add','sub','mul','div'):
    f=getattr(lib,'mpfr_'+name);f.argtypes=[P,P,P,C.c_int];f.restype=C.c_int
for name in ('exp','log','sqrt','tanh'):
    f=getattr(lib,'mpfr_'+name);f.argtypes=[P,P,C.c_int];f.restype=C.c_int

def rounded(op,a,b=None,up=False):
    """Exact double import; monotone directed double rounding at both stages."""
    vals=[MP(),MP(),MP()];rnd=2 if up else 3
    for v in vals: lib.mpfr_init2(C.byref(v),256)
    try:
        if lib.mpfr_set_d(C.byref(vals[1]),a,0)!=0: raise BackendError('INEXACT_IMPORT')
        if b is None: getattr(lib,'mpfr_'+op)(C.byref(vals[0]),C.byref(vals[1]),rnd)
        else:
            if lib.mpfr_set_d(C.byref(vals[2]),b,0)!=0: raise BackendError('INEXACT_IMPORT')
            getattr(lib,'mpfr_'+op)(C.byref(vals[0]),C.byref(vals[1]),C.byref(vals[2]),rnd)
        x=lib.mpfr_get_d(C.byref(vals[0]),rnd)
        if not math.isfinite(x): raise BackendError('NONFINITE_ENDPOINT: '+op)
        return x
    finally:
        for v in vals: lib.mpfr_clear(C.byref(v))

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        if isinstance(lo,I): self.lo,self.hi=lo.lo,lo.hi;return
        self.lo=float(lo);self.hi=float(lo if hi is None else hi)
        if not(math.isfinite(self.lo) and math.isfinite(self.hi) and self.lo<=self.hi): raise BackendError('INVALID_INTERVAL')
    def pair(self): return [self.lo,self.hi]
    def hex(self): return [self.lo.hex(),self.hi.hex()]
    def contains(self,x): return self.lo<=x<=self.hi
    def __neg__(self): return I(-self.hi,-self.lo)
    def __add__(self,b):
        b=I(b);return I(rounded('add',self.lo,b.lo),rounded('add',self.hi,b.hi,True))
    __radd__=__add__
    def __sub__(self,b): return self+-I(b)
    def __rsub__(self,b): return I(b)+-self
    def __mul__(self,b):
        b=I(b);pairs=[(a,c) for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(min(rounded('mul',a,c) for a,c in pairs),max(rounded('mul',a,c,True) for a,c in pairs))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=I(b)
        if b.contains(0): raise BackendError('ZERO_DENOMINATOR')
        pairs=[(a,c) for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(min(rounded('div',a,c) for a,c in pairs),max(rounded('div',a,c,True) for a,c in pairs))
    def __rtruediv__(self,b): return I(b)/self
    def exp(self): return I(rounded('exp',self.lo),rounded('exp',self.hi,up=True))
    def log(self):
        if self.lo<=0: raise BackendError('LOG_DOMAIN')
        return I(rounded('log',self.lo),rounded('log',self.hi,up=True))
    def sqrt(self):
        if self.lo<0: raise BackendError('SQRT_DOMAIN')
        return I(rounded('sqrt',self.lo),rounded('sqrt',self.hi,up=True))
    def tanh(self): return I(rounded('tanh',self.lo),rounded('tanh',self.hi,up=True))
    def power(self,p): return (self.log()*p).exp()
    def intersect(self,lo,hi):
        a=max(self.lo,lo);b=min(self.hi,hi)
        return I(a,b) if a<=b else None

def hull(xs):
    xs=list(xs)
    if not xs: raise BackendError('EMPTY_BRANCH_UNION')
    return I(min(x.lo for x in xs),max(x.hi for x in xs))

def cells(q,n):
    """All possible clamped floor stencils, including boundary closures."""
    for j in range(1,n-2):
        lo=q.lo if j==1 else float(j)
        hi=q.hi if j==n-3 else float(j+1)
        part=q.intersect(lo,hi)
        if part is not None: yield j,part-j

def coeff(t): return [t*(t-1)*(2-t)/6,(1+t)*(1-t)*(2-t)/2,(1+t)*t*(2-t)/2,(1+t)*t*(t-1)/6]
def dot(a,b): return sum((I(x)*y for x,y in zip(a,b)),I(0))

def spline_piece(x,x0,x1,y0,y1,m0,m1):
    h=I(x1)-x0;a=(I(x1)-x)/h;b=(x-x0)/h
    return a*y0+b*y1+((a*a*a-a)*m0+(b*b*b-b)*m1)*h*h/6

def bernstein(y0,y1,m0,m1,h):
    h=I(h);p1=I(y1)-y0+h*h*(-2*I(m0)-m1)/6;p2=h*h*m0/2
    return [I(y0),I(y0)+p1/3,I(y0)+2*p1/3+p2/3,I(y1)]

def positive_controls(b,depth=0):
    """Finite continuous cubic positivity certificate by Bernstein subdivision."""
    if min(x.lo for x in b)>0: return min(x.lo for x in b),1
    if depth==8: raise BackendError('BACKGROUND_POSITIVITY_NOT_PROVED_WITHIN_CAP')
    a=[(b[i]+b[i+1])/2 for i in range(3)]
    c=[(a[i]+a[i+1])/2 for i in range(2)];d=(c[0]+c[1])/2
    left,n=positive_controls([b[0],a[0],c[0],d],depth+1)
    right,m=positive_controls([d,c[1],a[2],b[3]],depth+1)
    return min(left,right),n+m

class Evaluator:
    def __init__(self,context):
        self.c=context;self.k={k:I(float.fromhex(v)) for k,v in context['constants'].items()}
        self.a=[[[float.fromhex(v) for v in row] for row in plane] for plane in context['logAlpha']]
        self.r=[float.fromhex(v) for v in context['logR']]
        self.dlog=I(float.fromhex(context['DlogTR']));self.dt=I(float.fromhex(context['DT_RATIO']))
        self.bg=[[float.fromhex(v) for v in row] for row in context['background']]
        self.fit=float.fromhex(context['fit_first_K'])
        self.calls=0
        if len(self.a)!=4 or any(len(p)!=40 or any(len(r)!=100 for r in p) for p in self.a) or len(self.r)!=100: raise BackendError('TABLE_DIMENSIONS')
        if self.dlog.lo<=0 or self.dt.lo<=0 or any(not math.isfinite(v) for p in self.a for r in p for v in r): raise BackendError('TABLE_VALUES')
        if any(not math.isfinite(v) for v in self.r): raise BackendError('TABLE_VALUES')
        if len(self.bg)<2 or len(self.bg)>200000 or any(len(r)!=5 or any(not math.isfinite(v) for v in r) for r in self.bg): raise BackendError('BACKGROUND_SHAPE')
        if any(b[0]<=a[0] for a,b in zip(self.bg,self.bg[1:])): raise BackendError('BACKGROUND_ORDER')
        if context['flags']!={'hyrec':True,'reio_camb':True,'no_exotic':True,'no_varconst':True,'no_idm':True,'no_idr':True,'no_idm_b':True,'require_H':True,'require_He':False,'phase_reio':True,'MODEL_SWIFT':True,'hyrec_error_zero':True,'fsR_meR_one':True}: raise BackendError('FROZEN_DOMAIN_FLAGS')
        if not(self.k['fHe'].lo>=0 and self.k['helium'].lo>=0 and (self.k['fHe']*self.k['helium']).hi<self.k['helium_cutoff'].lo): raise BackendError('HELIUM_DOMAIN')

    def background(self,z):
        x=-(1+z).log()
        if x.lo<self.bg[0][0] or x.hi>self.bg[-1][0]: raise BackendError('BACKGROUND_RANGE')
        hs=[];rs=[];count=0
        for a,b in zip(self.bg,self.bg[1:]):
            part=x.intersect(a[0],b[0])
            if part is None: continue
            count+=1
            if count>128: raise BackendError('BACKGROUND_BOX_CELL_CAP')
            hs.append(spline_piece(part,a[0],b[0],a[1],b[1],a[3],b[3]))
            rs.append(spline_piece(part,a[0],b[0],a[2],b[2],a[4],b[4]))
        h=hull(hs);r=hull(rs)
        if h.lo<=0 or r.lo<=0: raise BackendError('BACKGROUND_BOX_POSITIVITY')
        return h,r,count

    def positivity(self):
        x=-(I(1,51).log());count=0;leaves=0;bounds=[math.inf,math.inf]
        if x.lo<self.bg[0][0] or x.hi>self.bg[-1][0]: raise BackendError('BACKGROUND_FULL_RANGE')
        for a,b in zip(self.bg,self.bg[1:]):
            if x.intersect(a[0],b[0]) is None: continue
            count+=1
            if count>10000: raise BackendError('BACKGROUND_SEGMENT_CAP')
            for j in (1,2):
                low,n=positive_controls(bernstein(a[j],b[j],a[j+2],b[j+2],I(b[0])-a[0]))
                bounds[j-1]=min(bounds[j-1],low);leaves+=n
        return {'gate':'PASS_REAL_FROZEN_CUBICS','z':[0,50],'segments':count,'bernstein_leaves':leaves,'strict_lower_H_rhog':bounds}

    def rates(self,tr,ratio):
        k=self.k
        if tr.lo<k['TR_MIN'].lo or tr.hi>k['TR_MAX'].hi or ratio.lo<k['T_RATIO_MIN'].lo: raise BackendError('HYREC_TABLE_DOMAIN')
        qt=(tr.log()-k['TR_MIN'].log())/self.dlog
        outs=[];stencils=[]
        branches=[]
        low=ratio.intersect(ratio.lo,1.)
        if low is not None: branches.append((0,low))
        high=ratio.intersect(1.,ratio.hi)
        if high is not None: branches.append((2,1/high))
        for offset,rr in branches:
            qm=(rr-k['T_RATIO_MIN'])/self.dt
            for it,ft in cells(qt,100):
                ct=coeff(ft)
                ae=[dot(self.a[l][39][it-1:it+3],ct).exp() for l in range(2)]
                beta=[ae[l]*k['SAHA']*tr*tr.sqrt()*(-k['EI']/4/tr).exp()/(2*l+1) for l in range(2)]
                r=dot(self.r[it-1:it+3],ct).exp()
                for im,fm in cells(qm,40):
                    stencils.append([offset,it,im])
                    if len(stencils)>128: raise BackendError('HYREC_BOX_STENCIL_CAP')
                    cm=coeff(fm)
                    aa=[dot([dot(self.a[l+offset][im-1+j][it-1:it+3],ct) for j in range(4)],cm).exp() for l in range(2)]
                    outs.append(aa+[aa[l]-ae[l] for l in range(2)]+beta+[r])
        return [hull(row[j] for row in outs) for j in range(7)],stencils

    def alphaB(self,t):
        v=t/self.k['kBoltz']/1e4
        return self.k['alpha_pref']*v.power(self.k['alpha_pow1'])/(1+self.k['alpha_den']*v.power(self.k['alpha_pow2']))

    def tla(self,xe,xh,nh,h,tm,tr):
        k=self.k;rl=k['LYA']*h/nh/(1-xh);am=self.alphaB(tm);ar=self.alphaB(tr)
        beta=k['SAHA']*tr*tr.sqrt()*(-k['EI']/4/tr).exp()*ar
        cc=(3*rl+k['L2s'])/(3*rl+k['L2s']+beta)
        s=k['SAHA']*tr*tr.sqrt()*(-k['EI']/tr).exp()/nh
        delta=xe*xh-s*(1-xh)
        return -nh*(s*(1-xh)*(am-ar)+delta*am)*cc/h

    def hmla(self,xe,xh,nh,h,tr,ratio):
        k=self.k
        # The nested SWIFT predicate is still evaluated on its entire box.
        rl=k['LYA']*h/nh/(1-xh)
        fourbeta=k['SAHA']*tr*tr.sqrt()*(-k['EI']/4/tr).exp()*self.alphaB(tr)
        pion=fourbeta/(3*rl+k['L2s']+fourbeta)
        if (tr/k['kBoltz']).hi>=self.fit: raise BackendError('UNSUPPORTED_SWIFT_FIT_BRANCH')
        rr,stencils=self.rates(tr,ratio)
        a0,a1,da0,da1,b0,b1,r=rr
        g0=b0+3*r+k['L2s'];g1=b1+r+rl
        c0=(k['L2s']+3*r*rl/g1)/(g0-3*r*r/g1)
        c1=(rl+r*k['L2s']/g0)/(g1-r*3*r/g0)
        s=k['SAHA']*tr*tr.sqrt()*(-k['EI']/tr).exp()/nh
        delta=xe*xh-s*(1-xh)
        return -nh/h*((s*(1-xh)*da0+a0*delta)*c0+(s*(1-xh)*da1+a1*delta)*c1),stencils,pion

    def reio(self,z,xn,trial):
        p={k:I(float.fromhex(v)) for k,v in self.c['trials'][trial].items()}
        vals=[]
        if z.hi>p['start'].lo: vals.append(xn)
        zz=z.intersect(z.lo,p['start'].hi)
        if zz is not None:
            exponent=p['exponent'];one=1+p['center']
            arg=(one.power(exponent)-(1+zz).power(exponent))/(exponent*one.power(exponent-1))/p['width']
            vals.append((p['after']-xn)*(arg.tanh()+1)/2+xn+p['he_fraction']*((p['he_center']-zz)/p['he_width']).tanh()/2+p['he_fraction']/2)
        return hull(vals)

    def rhs(self,z,D,xh,trial):
        self.calls+=1
        if self.calls>256: raise BackendError('TOTAL_BOX_CAP')
        z=I(z);D=I(D);xh=I(xh);k=self.k
        if z.lo<0 or z.hi>50 or xh.lo<0 or xh.hi>=1: raise BackendError('ADMISSIBLE_BOX_DOMAIN')
        hc,rho,ncell=self.background(z);h=hc*k['c']/k['Mpc'];w=1+z
        nh=k['nH0']*w*w*w;trad=k['Tcmb']*w;tmat=D+trad
        if tmat.lo<=0: raise BackendError('TM_POSITIVITY')
        ratio=tmat/trad;tr=trad*k['kBoltz'];tm=tmat*k['kBoltz']
        xn=xh+k['fHe']*k['helium'];xr=self.reio(z,xn,trial)
        rate=(2*k['sigma']/k['me']/k['c'])*(I(4)/3*rho*k['Jm3'])*xr/(1+xr+k['fHe'])
        if rate.lo<0: raise BackendError('RATE_POSITIVITY')
        fd=-(2*tmat/w+rate*(tmat-trad)/(h*w)-k['Tcmb'])
        xs=[];branches=[];stencils=[];pion=None
        if tr.lo<=k['TR_MIN'].hi or ratio.lo<=k['T_RATIO_MIN'].hi:
            xs.append(self.tla(xn,xh,nh*k['cm3'],h,tm,tr)/w);branches.append('PEEBLES')
        if tr.hi>k['TR_MIN'].lo and ratio.hi>k['T_RATIO_MIN'].lo:
            t=tr.intersect(k['TR_MIN'].lo,tr.hi);rr=ratio.intersect(k['T_RATIO_MIN'].lo,ratio.hi)
            x,stencils,pion=self.hmla(xn,xh,nh*k['cm3'],h,t,rr)
            xs.append(x/w);branches.append('HMLA_BOTH_VALID_SWIFT_PATHS')
        return {'dD_ds':fd,'dxH_ds':hull(xs),'xe_noreio':xn,'xe_reio':xr,'branches':branches,'stencils':stencils,'background_cells':ncell,'Pion':pion}

    def source_xe_dkappa(self,z,xn,xr):
        """Source-write smoothing for the captured reio<-frec transition."""
        p=self.c['phase'];k=self.k
        if p['previous']!=p['full_recombination'] or p['current']!=p['reio']: raise BackendError('SOURCE_PHASE')
        limit=I(float.fromhex(p['previous_limit']));delta=I(float.fromhex(p['smoothing_delta']))
        if delta.lo<=0 or z.hi>limit.lo: raise BackendError('SOURCE_PHASE_DOMAIN')
        boundary=limit-2*delta;vals=[]
        if z.lo<=boundary.hi: vals.append(xr)
        zz=z.intersect(boundary.lo,z.hi)
        if zz is not None:
            s=(limit-zz)/(2*delta);weight=s*s*(I(.5)-s/3)*6
            vals.append(weight*xr+(1-weight)*xn)
        xe=hull(vals);w=1+z
        return {'xe_source':xe,'dkappa_per_Mpc':w*w*k['nH0']*xe*k['sigma']*k['Mpc']}

def jsonable(obj):
    if isinstance(obj,I): return {'binary64_hex_bounds':obj.hex(),'decimal_bounds':obj.pair()}
    if isinstance(obj,dict): return {k:jsonable(v) for k,v in obj.items()}
    if isinstance(obj,list): return [jsonable(v) for v in obj]
    return obj
