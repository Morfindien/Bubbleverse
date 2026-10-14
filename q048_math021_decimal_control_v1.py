#!/usr/bin/env python3
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import json, hashlib
RAW=Path('/mnt/data/q048_math021_branch_independent_scalar_enclosure_v1.json')
OUT=Path('/mnt/data/q048_math021_independent_decimal_control_v1.json')
r=json.loads(RAW.read_text())
D=Decimal
with localcontext() as c:
    c.prec=90
    hx=r['source_constants']['hex_binary64']
    def dh(k): return D.from_float(float.fromhex(hx[k]))
    H0=dh('H0'); Og=dh('Omega0_g'); Our=dh('Omega0_ur'); Ob=dh('Omega0_b'); Oc=dh('Omega0_cdm')
    Fv=dh('F_eV'); B=dh('B_floor'); mass=dh('M_ncdm'); factor=dh('factor_ncdm')
    qs=[D.from_float(float.fromhex(x)) for x in [
      '0x1.01a190a9342cbp-3','0x1.54b1b39dfb502p-1','0x1.a5aba87e1c094p+0','0x1.8baa6a27e0966p+1','0x1.41dfcbaec45f4p+2','0x1.e0a200b4eb4f7p+2','0x1.5363f359c10c3p+3','0x1.cdcfc7a7ec757p+3','0x1.32dc99949745cp+4','0x1.937bbcc9df2eap+4','0x1.0bfa403e53648p+5']]
    ws=[D.from_float(float.fromhex(x)) for x in [
      '0x1.4009ab2f5de6dp-10','0x1.1006ce715aac3p-9','0x1.9c8eedb3807edp-10','0x1.3596887f2dc85p-11','0x1.e3971fda418acp-14','0x1.9ab390e676f98p-17','0x1.708031cc9cbe6p-21','0x1.3d8abef57be5dp-26','0x1.b8d797c4599acp-33','0x1.5e137d7053544p-41','0x1.0c1275d7b5e1fp-52']]
    af=D(1)/D(1601); amin=D(1)/D(1946); E=D(1400)
    R=(Og+Our)*H0*H0; M=(Ob+Oc)*H0*H0
    def rhonu(a): return factor/a**4*sum(q*q*(q*q+(a*mass)**2).sqrt()*w for q,w in zip(qs,ws))
    Bf=R/af**4+M/af**3+rhonu(af)
    Bm=R/amin**4+M/amin**3+rhonu(amin)
    lam=D('2.435e27')/Fv
    anchor=D(2)/lam
    dphi=(D(2)*E/Bf).sqrt()/D(3)*((af/amin)**3-D(1))
    phimax=anchor+dphi
    xmax=(D(2)*E).sqrt()*(af/amin)**3
    emax=E*(af/amin)**6
    floor=B*D('3.968e-8')
    hlo=Bf.sqrt()
    hhi=(Bm+(emax+floor)/D(3)).sqrt()
    vals={'phi_boundary_abs_max':anchor,'phi_displacement_abs_max_over_root_window':dphi,'phi_abs_max_over_root_window':phimax,'X_abs_max_over_root_window_Mpc_minus1':xmax,'e_max_over_root_window':emax,'H_global_lower_Mpc_minus1':hlo,'H_global_upper_Mpc_minus1':hhi}
    def qdec(q): return D(q['num'])/D(q['den'])
    checks=[]
    for k,v in vals.items():
        obj=r['bounds'][k]
        if 'exact' in obj:
            lo=hi=qdec(obj['exact'])
        elif 'exact_upper' in obj:
            lo=D('-Infinity'); hi=qdec(obj['exact_upper'])
        elif 'exact_lower' in obj:
            lo=qdec(obj['exact_lower']); hi=D('Infinity')
        else: raise KeyError(k)
        tol=D('1e-80'); ok=(v>=lo-tol and v<=hi+tol)
        checks.append({'check':k,'pass':ok,'decimal_value':str(v),'claimed_lo':str(lo),'claimed_hi':str(hi)})
        if not ok: raise AssertionError(k)
    # For exact anchor, Decimal route differs only by precision; accept tiny ulp against the exact rational display instead of equality.
    # Replace that exact check with a 1e-80 consistency check.
    anchor_exact=qdec(r['bounds']['phi_boundary_abs_max']['exact'])
    checks[0]['pass']=abs(anchor-anchor_exact)<D('1e-80')
    if not checks[0]['pass']: raise AssertionError('anchor')
    out={'artifact_type':'BUBBLEVERSE_NUMERICAL_CONTROL','result_id':r['result_id'],'status':'PASS_DECIMAL90_CONTROL','checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),'checks':checks,'independence_scope':'Separate Decimal90 arithmetic path; shares source inputs and mathematical formulas, so not independent physical evidence.','raw_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest()}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'checks':f"{out['checks_passed']}/{out['checks_total']}"}))
