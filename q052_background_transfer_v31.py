#!/usr/bin/env python3
"""Q052 V31: exact stored-spline bounds and CONDITIONAL background transfer.

Usage: python q052_background_transfer_v31.py ORIGINAL_V30.zip --output receipt.json
Requires Python 3.11+ and system MPFR 4.2.1 (LP64 x86_64). No native rerun.

The reference spline interprets the captured binary64 coefficients as exact reals.
The admitted-target theorem is conditional on the retained Q050 fixed-B premises.
The floating-point kernel excludes libm log, compiler and historical table identity.
It must never be reported as a full native/source-real solution certificate.
"""
import argparse, bisect, ctypes as C, ctypes.util, datetime as dt
import hashlib, json, math, platform, sys, time, zipfile
from fractions import Fraction as Q
from pathlib import Path

TABLE_SHA = '2b037acdb209419707c24525d582e390596d92689f7af0d38183e83ca5f7eadd'
SOURCE = '5a131c91d657dd9a7c6364cc45b038710f8d0d97'
BINARY_SHA = 'df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf'
POINT_SHA = '12100006d1e164ce9b7605641e1321d4a6cf4b022bb196d04199e59ee76c237c'
BINDING_SHA = 'bfbe380364983b166658793514526986ae61e0c37a67a07774375ef49a4f7481'
H_B = (Q('1580426358065720928530117/500000000000000000000000'),
       Q('4480552533941654713/1000000000000000000'))
Z_LO = float.fromhex('0x1.9497ae147ae14p+9')
Z_HI = 810.0
U = Q(1, 2**53)
ETA = Q(1, 2**1075)  # half a subnormal step, gradual-underflow model
PREFIX = 'q052_background_dump_v30/'

def fq(x): return Q.from_float(float.fromhex(x))
def sha(b): return hashlib.sha256(b).hexdigest()
def outward(q, up):
    q = Q(q); f = float(q)
    if (Q(f) < q if up else Q(f) > q):
        f = math.nextafter(f, math.inf if up else -math.inf)
    return f
def bound(lo, hi=None):
    lo = Q(lo); hi = lo if hi is None else Q(hi)
    assert lo <= hi
    a,b = outward(lo, False),outward(hi, True)
    return {'hex':[a.hex(),b.hex()], 'display':[a,b]}

class MP(C.Structure):
    _fields_ = [('precision',C.c_long),('sign',C.c_int),
                ('exponent',C.c_long),('limbs',C.POINTER(C.c_ulong))]

def directed_transcendental(op, value, up):
    # Two directed stages: MPFR at 256 bits, then binary64 outward export.
    lib = mpfr(); a,b = MP(),MP(); rnd = 2 if up else 3
    lib.mpfr_init2(C.byref(a),256); lib.mpfr_init2(C.byref(b),256)
    try:
        assert lib.mpfr_set_d(C.byref(a),float(value),0) == 0
        getattr(lib,'mpfr_'+op)(C.byref(b),C.byref(a),rnd)
        out = lib.mpfr_get_d(C.byref(b),rnd)
        assert math.isfinite(out)
        return Q(out)
    finally:
        lib.mpfr_clear(C.byref(a)); lib.mpfr_clear(C.byref(b))

_LIB = None
def mpfr():
    global _LIB
    if _LIB is not None: return _LIB
    assert C.sizeof(C.c_long)==8 and C.sizeof(MP)==32
    assert platform.machine() in ('x86_64','AMD64')
    lib=C.CDLL(C.util.find_library('mpfr') or 'libmpfr.so.6')
    lib.mpfr_get_version.restype=C.c_char_p
    assert lib.mpfr_get_version()==b'4.2.1'
    p=C.POINTER(MP)
    lib.mpfr_init2.argtypes=[p,C.c_long]; lib.mpfr_init2.restype=None
    lib.mpfr_clear.argtypes=[p]; lib.mpfr_clear.restype=None
    lib.mpfr_set_d.argtypes=[p,C.c_double,C.c_int]; lib.mpfr_set_d.restype=C.c_int
    lib.mpfr_get_d.argtypes=[p,C.c_int]; lib.mpfr_get_d.restype=C.c_double
    for op in ('log','exp'):
        f=getattr(lib,'mpfr_'+op); f.argtypes=[p,p,C.c_int]; f.restype=C.c_int
    _LIB=lib
    return lib

def poly_value(c,t):
    v=Q(0)
    for x in reversed(c): v=v*t+x
    return v
def restrict_power(c,l,r):
    # p(l+(r-l)s), in powers of s.
    return [sum((c[k]*math.comb(k,j)*l**(k-j)*(r-l)**j
                 for k in range(j,len(c))),Q(0)) for j in range(len(c))]
def bernstein(c):
    n=len(c)-1
    return [sum((c[j]*Q(math.comb(k,j),math.comb(n,j))
                 for j in range(k+1)),Q(0)) for k in range(n+1)]
def enclosure(c,l=Q(0),r=Q(1)):
    b=bernstein(restrict_power(c,l,r)); return min(b),max(b)
def derivative(c,h=Q(1)): return [k*c[k]/h for k in range(1,len(c))]
def add(a,b):
    return [(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0))
            for i in range(max(len(a),len(b)))]
def multiply(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c
def spline(a,b,col):
    h=fq(b['loga'])-fq(a['loga'])
    y0,y1=fq(a['background'][col]),fq(b['background'][col])
    m0,m1=fq(a['d2background_dloga2'][col]),fq(b['d2background_dloga2'][col])
    return [y0,y1-y0+h*h*(-2*m0-m1)/6,h*h*m0/2,h*h*(m1-m0)/6]

class RI:
    """Exact rational interval, no floating operations."""
    def __init__(self,a,b=None): self.lo=Q(a); self.hi=Q(a if b is None else b); assert self.lo<=self.hi
    def __add__(self,b): return RI(self.lo+b.lo,self.hi+b.hi)
    def __sub__(self,b): return RI(self.lo-b.hi,self.hi-b.lo)
    def __mul__(self,b):
        p=[x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)];return RI(min(p),max(p))
    def __truediv__(self,b):
        assert b.lo*b.hi>0
        return self*RI(1/b.hi,1/b.lo)
    def mag(self): return max(abs(self.lo),abs(self.hi))
    def minabs(self): return min(abs(self.lo),abs(self.hi)) if self.lo*self.hi>0 else Q(0)

class FP:
    """Exact ideal range + absolute error of RN-binary64 C-expression evaluation.

    Every operation: |fl(v)-v| <= 2^-53 |v| + 2^-1075, no overflow.
    All input floats are exact; gradual underflow, no reassociation/contraction.
    """
    max_intermediate=Q(0)
    def __init__(self,x,err=Q(0)):
        self.r=x if isinstance(x,RI) else RI(x); self.e=Q(err)
    @classmethod
    def rounded(cls,r,e):
        mag=r.mag()+e
        assert mag < Q(2)**1023
        cls.max_intermediate=max(cls.max_intermediate,mag)
        return cls(r,e+U*mag+ETA)
    def __add__(self,b):
        b=b if isinstance(b,FP) else FP(b)
        return self.rounded(self.r+b.r,self.e+b.e)
    __radd__=__add__
    def __sub__(self,b):
        b=b if isinstance(b,FP) else FP(b)
        return self.rounded(self.r-b.r,self.e+b.e)
    def __rsub__(self,b): return FP(b)-self
    def __mul__(self,b):
        b=b if isinstance(b,FP) else FP(b)
        e=self.r.mag()*b.e+b.r.mag()*self.e+self.e*b.e
        return self.rounded(self.r*b.r,e)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=b if isinstance(b,FP) else FP(b)
        m=b.r.minabs(); assert m>b.e
        e=self.e/(m-b.e)+self.r.mag()*b.e/(m*(m-b.e))
        return self.rounded(self.r/b.r,e)

def fp_kernel(a,b,col):
    x0,x1=fq(a['loga']),fq(b['loga']); x=FP(RI(x0,x1))
    h=FP(x1)-x0; bb=(x-x0)/h; aa=1-bb
    y0,y1=fq(a['background'][col]),fq(b['background'][col])
    m0,m1=fq(a['d2background_dloga2'][col]),fq(b['d2background_dloga2'][col])
    # Exact expression tree of pinned arrays.c, including left associativity.
    ans=aa*y0+bb*y1+((aa*aa*aa-aa)*m0+(bb*bb*bb-bb)*m1)*h*h/6
    return ans.e

def native_float_eval(a,b,col,z):
    x=-math.log(1.0+z); x0=float.fromhex(a['loga']); x1=float.fromhex(b['loga'])
    h=x1-x0; bb=(x-x0)/h; aa=1-bb
    y0=float.fromhex(a['background'][col]);y1=float.fromhex(b['background'][col])
    m0=float.fromhex(a['d2background_dloga2'][col]);m1=float.fromhex(b['d2background_dloga2'][col])
    return aa*y0+bb*y1+((aa*aa*aa-aa)*m0+(bb*bb*bb-bb)*m1)*h*h/6.0

def validate_algebra(rows):
    checks=0
    for a,b in zip(rows,rows[1:]):
        h=fq(b['loga'])-fq(a['loga'])
        for col in range(32):
            c=spline(a,b,col); y0,y1=fq(a['background'][col]),fq(b['background'][col])
            m0,m1=fq(a['d2background_dloga2'][col]),fq(b['d2background_dloga2'][col])
            for t in (Q(0),Q(1,7),Q(1,2),Q(6,7),Q(1)):
                aa=1-t;direct=aa*y0+t*y1+((aa**3-aa)*m0+(t**3-t)*m1)*h*h/6
                assert poly_value(c,t)==direct;checks+=1
            assert poly_value(derivative(derivative(c,h),h),0)==m0
            assert poly_value(derivative(derivative(c,h),h),1)==m1
            checks+=2
            # Independent de Casteljau restriction versus power substitution.
            controls=bernstein(c)
            def split(v,t):
                left=[v[0]];right=[v[-1]]
                while len(v)>1:
                    v=[(1-t)*v[i]+t*v[i+1] for i in range(len(v)-1)]
                    left.append(v[0]);right.append(v[-1])
                return left,list(reversed(right))
            l,r=Q(1,7),Q(6,7)
            right=split(controls,l)[1];want=split(right,(r-l)/(1-l))[0]
            assert want==bernstein(restrict_power(c,l,r));checks+=1
    return checks

def run(path):
    tick=time.perf_counter(); start=dt.datetime.now(dt.timezone.utc).isoformat()
    with zipfile.ZipFile(path) as zf:
        def read(name): return zf.read(PREFIX+name)
        metadata=json.loads(read('Q052_BACKGROUND_DUMP_RESULT_V30.json'))
        assert metadata['source_commit']==SOURCE and metadata['class_binary_sha256']==BINARY_SHA
        assert metadata['point_sha256']==POINT_SHA and sha(read('point.ini'))==POINT_SHA
        table=read('background_table_hex.jsonl');assert sha(table)==TABLE_SHA==metadata['table_sha256']
        lines=table.splitlines(); header=json.loads(lines[0]);assert header['bt_size']==40000 and header['bg_size']==32
        rows=[json.loads(l) for l in lines[1:]];assert len(rows)==40000
        xs=[fq(r['loga']) for r in rows]
        for i,r in enumerate(rows):
            assert r['i']==i and len(r['background'])==len(r['d2background_dloga2'])==32
            for v in [r['loga'],r['tau'],r['z']]+r['background']+r['d2background_dloga2']:
                assert math.isfinite(float.fromhex(v))
            if i: assert xs[i]>xs[i-1] and fq(r['z'])<fq(rows[i-1]['z'])
        # z+1 is exact at these endpoints (binary64 exponent is unchanged).
        assert Q(Z_LO)+1==Q(1.0+Z_LO)
        xlo=-directed_transcendental('log',1.0+Z_HI,True)
        xhi=-directed_transcendental('log',1.0+Z_LO,False)
        ids=[i for i in range(len(xs)-1) if xs[i]<=xhi and xs[i+1]>=xlo]
        assert ids==[31687,31688]
        selected=[rows[i] for i in [ids[0],ids[0]+1,ids[1]+1]]
        identity=json.loads(read('effective_identity.json'));f=identity['fields']
        assert f['H0']=='0x1.e0a87807cbe58p-13' and f['Omega0_g']=='0x1.b7656d184c7aap-15'
        rho0=fq(f['H0'])**2*fq(f['Omega0_g'])
        results=[]; allH=[]; allrho=[]; rhoerrs=[]; hround=[]; rround=[]; hslopes=[]
        for i in ids:
            a,b=rows[i],rows[i+1];x0,x1=xs[i:i+2];h=x1-x0
            l=(max(xlo,x0)-x0)/h;r=(min(xhi,x1)-x0)/h
            cols=[]
            for j in range(32):
                c=spline(a,b,j); v=enclosure(c,l,r);d=enclosure(derivative(c,h),l,r)
                e=fp_kernel(a,b,j)
                cols.append({'index':j,'reference_range':bound(*v),'derivative_dloga':bound(*d),
                             'fp_arithmetic_abs_error_upper':bound(0,e)})
                if j==1:
                    allH.append(v);hround.append(e)
                    hslopes.append(max(map(abs,enclosure(derivative(c,h)))))
                if j==3: allrho.append(v);rround.append(e)
            # rho_gamma exact target is rho0 exp(-4x). Use its stable ODE.
            pc=spline(a,b,3);res=add(derivative(pc,h),[4*v for v in pc])
            # 32 exact Bernstein subdivisions reduce cancellation width, no sampling claim.
            res_bounds=[enclosure(res,Q(k,32),Q(k+1,32)) for k in range(32)]
            rmax=max(abs(v) for pair in res_bounds for v in pair)
            assert Q(-4*float(x0)) == -4*x0
            r0lo=rho0*directed_transcendental('exp',-4*float(x0),False)
            r0hi=rho0*directed_transcendental('exp',-4*float(x0),True)
            e0=max(abs(pc[0]-r0lo),abs(pc[0]-r0hi))
            erho=e0+h*rmax;rhoerrs.append(erho)
            # Exact table-column consistency diagnostic, not a source-solution error.
            dc=add(multiply(multiply(spline(a,b,0),spline(a,b,1)),derivative(spline(a,b,1),h)),
                   [-v for v in spline(a,b,2)])
            results.append({'left_row':i,'right_row':i+1,'loga_endpoints':[a['loga'],b['loga']],
              'restricted_t_rational':[str(l),str(r)],'columns':cols,
              'photon_residual_dPdx_plus_4P':bound(-rmax,rmax),
              'photon_node_error_upper':bound(0,e0),'photon_reference_error_upper':bound(0,erho),
              'Hprime_column_consistency_defect_at_left_knot':bound(dc[0]),
              'Hprime_defect_definition':'P_a*P_H*dP_H/dloga - P_Hprime_eta; stored polynomial columns only'})
        hlo=min(x[0] for x in allH);hhi=max(x[1] for x in allH);assert hlo>0
        deltaH=max(abs(H_B[0]-hhi),abs(H_B[1]-hlo))
        dw=max(abs(1/H_B[0]-1/hhi),abs(1/H_B[1]-1/hlo))
        rhomax=rho0*(1+Q(Z_HI))**4;erho=max(rhoerrs)
        drho_over_H=rhomax*dw+erho/hlo
        trace=[json.loads(l) for l in read('fullstate_trace.jsonl').splitlines()]
        chosen=[d for d in trace if Z_LO<=float.fromhex(d['z'])<=Z_HI]
        equal=0;maxdiff=Q(0);mismatches=[]
        for k,d in enumerate(chosen):
            zz=float.fromhex(d['z']);xx=Q(-math.log(1+zz));ii=bisect.bisect_right(xs,xx)-1
            assert ii in ids
            for j,sv in enumerate(d['pvecback_normal']):
                ref=native_float_eval(rows[ii],rows[ii+1],j,zz);native=float.fromhex(sv)
                delta=abs(Q(ref)-Q(native));maxdiff=max(maxdiff,delta)
                if ref.hex()==native.hex():equal+=1
                else:mismatches.append({'trace':k,'column':j,'difference':float(delta)})
        checks=validate_algebra(selected)
        result={'schema':'Q052_BACKGROUND_TRANSFER_V31','run_id':'LOCAL-Q052-MATH-BACKGROUND-TRANSFER-20261030-V31',
          'status':'PASS_REFERENCE_SPLINE_AND_CONDITIONAL_TARGET_TRANSFER',
          'case_id':'LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1','target_q':'Q052',
          'source_run_id':metadata['run_id'],'source_commit':SOURCE,
          'input_zip_sha256':sha(Path(path).read_bytes()),'table_sha256':TABLE_SHA,'binding_sha256':BINDING_SHA,
          'program_sha256':sha(Path(__file__).read_bytes()),
          'domain_z_hex':[Z_LO.hex(),Z_HI.hex()],'reference_loga_enclosure':bound(xlo,xhi),
          'rows_checked':len(rows),'selected_segments':ids,'segments':results,
          'reference_H_range':bound(hlo,hhi),'Q050_H_projection':bound(*H_B),
          'projection_compatibility':H_B[0]<=hlo and hhi<=H_B[1],
          'reference_photon_error_to_analytic_target':bound(0,erho),
          'conditional_transfer':{'quantifier':'every one fixed existing admitted Q050 B; same B throughout both cells and q branches',
             'H_abs_difference_upper':bound(0,deltaH),'inverse_H_abs_difference_upper':bound(0,dw),
             'rho_gamma_over_H_abs_difference_upper':bound(0,drho_over_H),
             'photon_target_definition':'Omega0_g * H0^2 * (1+z)^4, exact captured binary64 constants',
             'native_table_integration_error_separate_required':False,
             'reason':'Total difference between the stored reference curve and any admitted target is bounded directly. This does not prove family membership, a sharp IVP error, or existence of the inherited target.'},
          'arithmetic_kernel':{'H_abs_error_upper':bound(0,max(hround)),
             'rho_gamma_abs_error_upper':bound(0,max(rround)),
             'max_intermediate_magnitude_upper':bound(0,FP.max_intermediate),
             'H_reference_lipschitz_in_loga_upper':bound(0,max(hslopes)),
             'assumptions':['IEEE754 binary64 round-to-nearest, gradual underflow',
                            'pinned C expression order, no reassociation or contraction',
                            'exact input table and supplied binary64 loga inside the certified table segments'],
             'native_log_error_bound':None,'historical_binary_execution_model_verified':False,
             'coordinate_transfer_rule':'On the covered intervals: add max|dP_H/dloga| * epsilon_log to H arithmetic error; epsilon_log and interval coverage must be certified independently.'},
          'sample_replay':{'scope':'current local libm/Python evaluation versus V30 saved workspace snapshots; finite diagnostic only',
             'trace_records':len(chosen),'values':sum(len(d['pvecback_normal']) for d in chosen),
             'bitwise_equal_values':equal,'max_abs_difference':bound(0,maxdiff),'mismatches':mismatches},
          'validation':{'exact_algebra_and_independent_de_casteljau_checks':checks,
             'source_formula_scope':'pinned background.c background_at_z and arrays.c array_interpolate_spline',
             'independence_limit':'Independent algebraic representation; shared captured table and source formula'},
          'source_real_certificate':False,'native_background_membership_certified':False,
          'full_q052_gate':'UNRESOLVED','global_realized_suprema':None,'new_native_runs':0,
          'remaining_gaps':['certified historical log/rounding/compiler contract and binding V30 table to original L/R tables',
             'source-real initial/native solver/output error and whole-domain observable transfer',
             'existence/applicability of the inherited admitted target remains a stated premise'],
          'execution':{'start_utc':start,'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'elapsed_seconds':time.perf_counter()-tick,'python':sys.version,'MPFR':'4.2.1',
             'precision_bits':256,'transcendentals_rounding':'RNDD/RNDU plus outward binary64 export'}}
        return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('zip',type=Path);ap.add_argument('--output',type=Path)
    args=ap.parse_args();r=run(args.zip);s=json.dumps(r,indent=2,ensure_ascii=False)+'\n'
    if args.output: args.output.write_text(s)
    else: print(s,end='')
    if args.output: print(json.dumps({k:r[k] for k in ['status','reference_H_range','reference_photon_error_to_analytic_target','conditional_transfer','sample_replay','validation','execution']},indent=2))
