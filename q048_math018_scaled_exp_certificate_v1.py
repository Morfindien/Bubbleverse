#!/usr/bin/env python3
import json, math, hashlib, platform, sys, time
from fractions import Fraction
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT/'q048_math018_scaled_exp_config_v1.json').read_text())


def sha256_path(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()


def fl_div(a,b):
    return a//b

def ce_div(a,b):
    return -((-a)//b)

def frac_floor_scaled(q,p):
    S=1<<p
    return (q.numerator*S)//q.denominator

def frac_ceil_scaled(q,p):
    S=1<<p
    return -((-q.numerator*S)//q.denominator)

def frac_iv(q,p):
    return (frac_floor_scaled(q,p), frac_ceil_scaled(q,p))

def iv_add(a,b): return (a[0]+b[0],a[1]+b[1])
def iv_sub(a,b): return (a[0]-b[1],a[1]-b[0])
def iv_mul(a,b,p):
    S=1<<p
    prods=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]]
    return (fl_div(min(prods),S), ce_div(max(prods),S))
def iv_div_pos_int(a,n):
    assert n>0
    return (fl_div(a[0],n),ce_div(a[1],n))
def iv_mul_int(a,n):
    return (a[0]*n,a[1]*n) if n>=0 else (a[1]*n,a[0]*n)

def pow2_frac(e):
    return Fraction(1<<e,1) if e>=0 else Fraction(1,1<<(-e))

def floor_log2_frac(q):
    assert q>0
    e=q.numerator.bit_length()-q.denominator.bit_length()
    while q < pow2_frac(e): e-=1
    while q >= pow2_frac(e+1): e+=1
    return e


def ln_m_from_exact_m(m,p,N):
    # 1 <= m < 2; y exact in [0,1/3)
    assert Fraction(1,1) <= m < Fraction(2,1)
    y=(m-1)/(m+1)
    yiv=frac_iv(y,p)
    y2=iv_mul(yiv,yiv,p)
    yp=yiv
    acc=(0,0)
    for j in range(N):
        term=iv_div_pos_int(yp,2*j+1)
        acc=iv_add(acc,term)
        yp=iv_mul(yp,y2,p)
    acc=iv_mul_int(acc,2)
    # tail <= (9/4)*y^(2N+1)/(2N+1), y<=1/3
    rem_hi=ce_div(9*max(0,yp[1]),4*(2*N+1))
    return (acc[0],acc[1]+rem_hi), y


def ln2_iv(p,N):
    # exact atanh series y=1/3; m=2 is limiting endpoint
    y=Fraction(1,3)
    yiv=frac_iv(y,p)
    y2=iv_mul(yiv,yiv,p)
    yp=yiv
    acc=(0,0)
    for j in range(N):
        term=iv_div_pos_int(yp,2*j+1)
        acc=iv_add(acc,term)
        yp=iv_mul(yp,y2,p)
    acc=iv_mul_int(acc,2)
    rem_hi=ce_div(9*max(0,yp[1]),4*(2*N+1))
    return (acc[0],acc[1]+rem_hi)


def ln_q_iv(q,p,N,l2=None):
    e=floor_log2_frac(q)
    m=q/pow2_frac(e)
    assert Fraction(1,1) <= m < Fraction(2,1)
    lm,_=ln_m_from_exact_m(m,p,N)
    if l2 is None: l2=ln2_iv(p,N)
    return iv_add(lm,iv_mul_int(l2,e)), e, m


def exp_positive_iv(riv,p,N):
    # riv must be positive and < 1. Directed Taylor with conservative tail.
    S=1<<p
    assert riv[0] > 0 and riv[1] < S
    term=(S,S)
    acc=(S,S)
    for n in range(1,N+1):
        term=iv_div_pos_int(iv_mul(term,riv,p),n)
        acc=iv_add(acc,term)
    next_term=iv_div_pos_int(iv_mul(term,riv,p),N+1)
    # since r<1, remaining geometric majorant <= next*(N+2)/(N+1)
    rem_hi=ce_div(max(0,next_term[1])*(N+2),N+1)
    return (acc[0],acc[1]+rem_hi)


def exp_point_primary(x_int,p,Nlog,Nexp,k=-897):
    S=1<<p
    l2=ln2_iv(p,Nlog)
    c=-k
    riv=(x_int+c*l2[0],x_int+c*l2[1])
    guard=(riv[0]>0 and riv[1]<l2[0])
    eiv=exp_positive_iv(riv,p,Nexp)
    return eiv,riv,l2,guard


def exp_point_control(x_int,p,Nlog,Nexp,halvings,k=-897):
    S=1<<p
    l2=ln2_iv(p,Nlog)
    c=-k
    riv=(x_int+c*l2[0],x_int+c*l2[1])
    guard=(riv[0]>0 and riv[1]<l2[0])
    scale=1<<halvings
    uiv=(fl_div(riv[0],scale),ce_div(riv[1],scale))
    eiv=exp_positive_iv(uiv,p,Nexp)
    for _ in range(halvings):
        eiv=iv_mul(eiv,eiv,p)
    return eiv,riv,l2,guard


def scaled_cmp_upper_lt_q(m_hi,p,e2,q):
    assert e2<0
    lhs=m_hi*q.denominator
    rhs=q.numerator*(1<<p)*(1<<(-e2))
    return lhs<rhs, rhs-lhs

def scaled_cmp_lower_gt_q(m_lo,p,e2,q):
    assert e2<0
    lhs=m_lo*q.denominator
    rhs=q.numerator*(1<<p)*(1<<(-e2))
    return lhs>rhs, lhs-rhs


def scaled_mul(a,b,p):
    # a,b = {lo,hi,e2}; positive mantissas
    assert a['lo']>0 and b['lo']>0
    lo=fl_div(a['lo']*b['lo'],1<<p)
    hi=ce_div(a['hi']*b['hi'],1<<p)
    return {'lo':lo,'hi':hi,'e2':a['e2']+b['e2']}

def scaled_recip(a,p):
    assert a['lo']>0
    S=1<<p
    lo=fl_div(S*S,a['hi'])
    hi=ce_div(S*S,a['lo'])
    return {'lo':lo,'hi':hi,'e2':-a['e2']}


def dscaled(m,p,e2,prec=50):
    getcontext().prec=prec
    return Decimal(m)/Decimal(1<<p) * (Decimal(2) ** Decimal(e2))
def dfixed(i,p,prec=70):
    getcontext().prec=prec
    return Decimal(i)/Decimal(1<<p)

def sci(x):
    return format(x,'.40E')


def main():
    t0=time.perf_counter()
    p=int(CFG['primary_scale_bits']); pc=int(CFG['control_scale_bits'])
    Nlog=int(CFG['log_terms']); Nexp=int(CFG['primary_exp_terms'])
    Nctl=int(CFG['control_exp_terms']); halves=int(CFG['control_halvings'])
    slack_bits=int(CFG['log_slack_bits']); k=int(CFG['fixed_binary_exponent'])
    token=CFG['input_token']
    # exact decimal token
    sig,es=token.lower().split('e')
    exp10=int(es); digs=sig.replace('.',''); decs=len(sig.split('.')[1])
    q_dec=Fraction(int(digs),10**decs) * (Fraction(10**exp10,1) if exp10>=0 else Fraction(1,10**(-exp10)))
    q_f=Fraction(*float(token).as_integer_ratio())
    qlo=min(q_dec,q_f); qhi=max(q_dec,q_f)

    l2=ln2_iv(p,Nlog)
    loglo_raw,elo,mlo=ln_q_iv(qlo,p,Nlog,l2)
    loghi_raw,ehi,mhi=ln_q_iv(qhi,p,Nlog,l2)
    slack=1<<(p-slack_bits)
    L=loglo_raw[0]-slack
    U=loghi_raw[1]+slack

    pL,rL,l2p,gL=exp_point_primary(L,p,Nlog,Nexp,k)
    pU,rU,_,gU=exp_point_primary(U,p,Nlog,Nexp,k)

    # same exact bracket endpoints lifted to control precision
    shift=pc-p
    Lc=L<<shift; Uc=U<<shift
    cL,crL,l2c,cgL=exp_point_control(Lc,pc,Nlog,Nctl,halves,k)
    cU,crU,_,cgU=exp_point_control(Uc,pc,Nlog,Nctl,halves,k)

    pl_ok,pl_margin=scaled_cmp_upper_lt_q(pL[1],p,k,qlo)
    pu_ok,pu_margin=scaled_cmp_lower_gt_q(pU[0],p,k,qhi)
    cl_ok,cl_margin=scaled_cmp_upper_lt_q(cL[1],pc,k,qlo)
    cu_ok,cu_margin=scaled_cmp_lower_gt_q(cU[0],pc,k,qhi)

    # certified rate interval generated from the widened log interval
    cert={'lo':pL[0],'hi':pU[1],'e2':k}
    unit={'lo':1<<p,'hi':1<<p,'e2':0}
    prod=scaled_mul(cert,unit,p)
    recip=scaled_recip(cert,p)
    roundtrip=scaled_recip(recip,p)
    downstream_positive=(prod['lo']>0 and recip['lo']>0)
    roundtrip_contains=(roundtrip['e2']==cert['e2'] and roundtrip['lo']<=cert['lo'] and roundtrip['hi']>=cert['hi'])

    checks={
      'input_union_lower_is_exact_decimal': qlo==q_dec,
      'binary64_parse_above_exact_decimal': q_f>q_dec,
      'primary_range_guard_lower': gL,
      'primary_range_guard_upper': gU,
      'control_range_guard_lower': cgL,
      'control_range_guard_upper': cgU,
      'primary_positive_lower_endpoint': pL[0]>0,
      'primary_positive_upper_endpoint': pU[0]>0,
      'control_positive_lower_endpoint': cL[0]>0,
      'control_positive_upper_endpoint': cU[0]>0,
      'primary_inverse_lower_strict': pl_ok,
      'primary_inverse_upper_strict': pu_ok,
      'control_inverse_lower_strict': cl_ok,
      'control_inverse_upper_strict': cu_ok,
      'scaled_unit_product_positive': prod['lo']>0,
      'scaled_unit_product_identity': prod==cert,
      'scaled_reciprocal_positive': recip['lo']>0,
      'reciprocal_roundtrip_contains_original': roundtrip_contains
    }
    passed=sum(bool(v) for v in checks.values()); total=len(checks)
    status='PASS_SUBCOMPONENT' if passed==total else 'FAIL_OBSTRUCTION'

    getcontext().prec=90
    qloD=Decimal(qlo.numerator)/Decimal(qlo.denominator)
    qhiD=Decimal(qhi.numerator)/Decimal(qhi.denominator)
    rel_pl=(qloD-dscaled(pL[1],p,k,90))/qloD
    rel_pu=(dscaled(pU[0],p,k,90)-qhiD)/qhiD
    rel_cl=(qloD-dscaled(cL[1],pc,k,90))/qloD
    rel_cu=(dscaled(cU[0],pc,k,90)-qhiD)/qhiD

    result={
      'schema':'bubbleverse.math.local_result',
      'schema_version':'UNVALIDATED_LOCAL_CONTRACT',
      'result_id':CFG['result_id'], 'task_id':CFG['task_id'],
      'status':status,
      'scope':'R_inf.dat token0 arithmetic admission subcomponent only',
      'input':{
        'token':token,
        'exact_decimal_fraction':{'numerator':str(q_dec.numerator),'denominator':str(q_dec.denominator)},
        'binary64_fraction':{'numerator':str(q_f.numerator),'denominator':str(q_f.denominator)},
        'union_lower_source':'exact_decimal' if qlo==q_dec else 'binary64',
        'union_upper_source':'binary64' if qhi==q_f else 'exact_decimal',
        'union_relative_width_approx':sci((qhiD-qloD)/qloD)
      },
      'frozen_method':{
        'primary_scale_bits':p,'control_scale_bits':pc,'log_terms':Nlog,
        'primary_exp_terms':Nexp,'control_halvings':halves,'control_exp_terms':Nctl,
        'log_slack_bits':slack_bits,'binary_exponent':k,
        'config_sha256':sha256_path(ROOT/'q048_math018_scaled_exp_config_v1.json'),
        'spec_sha256':sha256_path(ROOT/'Q048_MATH018_FROZEN_SPEC_V1.md')
      },
      'log_union':{
        'lower_scaled_integer':str(L),'upper_scaled_integer':str(U),'scale_bits':p,
        'lower_decimal_approx':str(dfixed(L,p,80)),
        'upper_decimal_approx':str(dfixed(U,p,80)),
        'old_display_orientation':'-621.1509893734175'
      },
      'primary':{
        'lower_endpoint_exp_mantissa_interval':[str(pL[0]),str(pL[1])],
        'upper_endpoint_exp_mantissa_interval':[str(pU[0]),str(pU[1])],
        'scale_bits':p,'binary_exponent':k,
        'exp_upper_L_approx':sci(dscaled(pL[1],p,k,70)),
        'exp_lower_U_approx':sci(dscaled(pU[0],p,k,70)),
        'relative_lower_control_margin_approx':sci(rel_pl),
        'relative_upper_control_margin_approx':sci(rel_pu),
        'exact_cross_margin_lower':str(pl_margin),
        'exact_cross_margin_upper':str(pu_margin)
      },
      'independent_control':{
        'method':'8 halvings + directed Taylor + 8 squarings',
        'lower_endpoint_exp_mantissa_interval':[str(cL[0]),str(cL[1])],
        'upper_endpoint_exp_mantissa_interval':[str(cU[0]),str(cU[1])],
        'scale_bits':pc,'binary_exponent':k,
        'relative_lower_control_margin_approx':sci(rel_cl),
        'relative_upper_control_margin_approx':sci(rel_cu),
        'exact_cross_margin_lower':str(cl_margin),
        'exact_cross_margin_upper':str(cu_margin)
      },
      'downstream_scaled_contract':{
        'certified_rate':{kk:str(vv) for kk,vv in cert.items()},
        'unit_product':{kk:str(vv) for kk,vv in prod.items()},
        'reciprocal':{kk:str(vv) for kk,vv in recip.items()},
        'reciprocal_roundtrip':{kk:str(vv) for kk,vv in roundtrip.items()},
        'positive_preserved':downstream_positive,
        'roundtrip_contains_original':roundtrip_contains
      },
      'checks':checks,
      'check_summary':{'passed':passed,'total':total},
      'interpretation':{
        'arithmetic_subcomponent':'QUALIFIED' if status=='PASS_SUBCOMPONENT' else 'NOT_QUALIFIED',
        'full_P3':'NOT_QUALIFIED_BY_THIS_RESULT_ALONE',
        'exact_Q048':'UNRESOLVED',
        'physical_claim':'NO_PHYSICAL_RESULT'
      },
      'execution':{
        'python':platform.python_version(),
        'platform':platform.platform(),
        'elapsed_seconds':time.perf_counter()-t0,
        'proofcells_used':10,
        'randomness':'none'
      }
    }
    out=ROOT/'q048_math018_scaled_exp_result_v1.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    val={
      'result_sha256':sha256_path(out),
      'all_frozen_acceptance_checks_pass':passed==total,
      'check_summary':result['check_summary'],
      'checks':checks,
      'decision':status,
      'notes':['No Decimal value participates in proof decisions; Decimal is display only.',
               'All decision inequalities use exact integers/rationals and outward fixed-point bounds.',
               'This stops at the frozen R0 arithmetic discriminator; full P3 is not promoted.']
    }
    (ROOT/'q048_math018_scaled_exp_validation_v1.json').write_text(json.dumps(val,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':status,'passed':passed,'total':total,
      'log_lower':result['log_union']['lower_decimal_approx'],
      'log_upper':result['log_union']['upper_decimal_approx'],
      'primary_rel_margins':[result['primary']['relative_lower_control_margin_approx'],result['primary']['relative_upper_control_margin_approx']],
      'control_rel_margins':[result['independent_control']['relative_lower_control_margin_approx'],result['independent_control']['relative_upper_control_margin_approx']],
      'elapsed_seconds':result['execution']['elapsed_seconds']},indent=2))
    return 0 if status=='PASS_SUBCOMPONENT' else 1

if __name__=='__main__':
    raise SystemExit(main())
