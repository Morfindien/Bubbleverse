#!/usr/bin/env python3
"""Q048 MATH021 — exact-rational/outward audit for hillipop-ede_n3.

This is a local mathematical audit only. It does not run CLASS/HyRec, perform an IVP,
find an event, write GitHub, change CURRENT_STATE, or close Q048.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
from decimal import Decimal, localcontext
import hashlib, json, sys

JOURNAL = Path('/mnt/data/Q047_SAMLET_JOURNAL_H_EVENT_PAYLOAD_INGESTED_V1.md')
PROMPT = Path('/mnt/data/Bubbleverse_Matematikmotor_2.0.0-10.md')
HANDOFF = Path('/mnt/data/Q048_H_EVENT_PAYLOAD_INGESTION_HANDOFF_V1.md')
OUT = Path('/mnt/data/q048_math021_branch_independent_scalar_enclosure_v1.json')
VAL = Path('/mnt/data/q048_math021_validation_v1.json')

EXPECTED = {
    'journal_sha256': '7b5e9544568c9f75e218d80092662422a66500cc2fb69077adeee6ae8799cd97',
    'prompt_sha256': '60e53cc6a2f725b960537e88d63fd51643d99076b47f6d5d28268dec5b78d1d1',
    'handoff_sha256': 'e040f8699f2712c4686fb00e4175e9c9c35dd19d4ef8abf39ef8fdf8e635b6d0',
    'question_sha256': 'c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436',
    'source_commit': '5a131c91d657dd9a7c6364cc45b038710f8d0d97',
    'capture_sha256': '2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b',
}
QUESTION = ('For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, '
            'what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history '
            'x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 '
            'and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?')

HEX = {
    'H0': '0x1.e0a87807cbe58p-13',
    'Omega0_b': '0x1.81414da191ee2p-5',
    'Omega0_cdm': '0x1.0c0260fc4ee05p-2',
    'Omega0_g': '0x1.b7656d184c7aap-15',
    'Omega0_ur': '0x1.95b4e375d3fa6p-16',
    'Omega0_lambda': '0x0p+0',
    'F_eV': '0x1.419fbeb3d4926p+87',
    'm_eV': '0x1.8c1be6d0d636dp-90',
    'B_floor': '0x1.5eab3adf48e52p+1',
    'M_ncdm': '0x1.64bd78a1e489fp+8',
    'factor_ncdm': '0x1.e63d04703becp-37',
}
QHEX = [
    '0x1.01a190a9342cbp-3','0x1.54b1b39dfb502p-1','0x1.a5aba87e1c094p+0',
    '0x1.8baa6a27e0966p+1','0x1.41dfcbaec45f4p+2','0x1.e0a200b4eb4f7p+2',
    '0x1.5363f359c10c3p+3','0x1.cdcfc7a7ec757p+3','0x1.32dc99949745cp+4',
    '0x1.937bbcc9df2eap+4','0x1.0bfa403e53648p+5'
]
WHEX = [
    '0x1.4009ab2f5de6dp-10','0x1.1006ce715aac3p-9','0x1.9c8eedb3807edp-10',
    '0x1.3596887f2dc85p-11','0x1.e3971fda418acp-14','0x1.9ab390e676f98p-17',
    '0x1.708031cc9cbe6p-21','0x1.3d8abef57be5dp-26','0x1.b8d797c4599acp-33',
    '0x1.5e137d7053544p-41','0x1.0c1275d7b5e1fp-52'
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def exact_hex(s: str) -> F:
    return F.from_float(float.fromhex(s))

def rat(x: F):
    return {'num': str(x.numerator), 'den': str(x.denominator)}

def dec(x: F, digits=30) -> str:
    with localcontext() as c:
        c.prec = digits
        return format(Decimal(x.numerator) / Decimal(x.denominator), 'g')

def sqrt_bounds(x: F, digits: int = 90):
    assert x >= 0
    scale = 10 ** digits
    floor_scaled_sq = (x.numerator * scale * scale) // x.denominator
    k = isqrt(floor_scaled_sq)
    lo = F(k, scale)
    exact = (k*k*x.denominator == x.numerator*scale*scale)
    hi = lo if exact else F(k+1, scale)
    assert lo*lo <= x <= hi*hi
    return lo, hi

def ibox(lo: F, hi: F, digits=24):
    assert lo <= hi
    return {
        'lo_exact': rat(lo), 'hi_exact': rat(hi),
        'lo_display': dec(lo, digits), 'hi_display': dec(hi, digits)
    }

def rho_nu_bounds(a: F, qs, ws, mass: F, factor: F):
    lo_sum = F(0); hi_sum = F(0)
    eps_bounds=[]
    for q,w in zip(qs,ws):
        x = q*q + (a*mass)*(a*mass)
        elo,ehi = sqrt_bounds(x)
        lo_sum += q*q*elo*w
        hi_sum += q*q*ehi*w
        eps_bounds.append((elo,ehi))
    fac = factor / a**4
    return fac*lo_sum, fac*hi_sum, eps_bounds

checks=[]
def ck(name, cond, detail=None):
    checks.append({'check':name,'pass':bool(cond),'detail':detail})
    if not cond:
        raise AssertionError(name)

# Immutable input verification.
ck('journal_sha256', sha(JOURNAL)==EXPECTED['journal_sha256'], sha(JOURNAL))
ck('prompt_sha256', sha(PROMPT)==EXPECTED['prompt_sha256'], sha(PROMPT))
ck('handoff_sha256', sha(HANDOFF)==EXPECTED['handoff_sha256'], sha(HANDOFF))
ck('question_sha256', hashlib.sha256(QUESTION.encode()).hexdigest()==EXPECTED['question_sha256'])
text=JOURNAL.read_text(errors='strict')
for k,v in HEX.items(): ck('source_hex_present_'+k, v in text)
for i,v in enumerate(QHEX): ck(f'q_node_{i}_present', v in text)
for i,v in enumerate(WHEX): ck(f'w_node_{i}_present', v in text)
ck('source_commit_present', EXPECTED['source_commit'] in text)
ck('capture_hash_present', EXPECTED['capture_sha256'] in text)
ck('root_window_preserved', '1600<z_e<1945' in text)
ck('exact_cap_1400_preserved', 'actual cap er 1400' in text)
ck('theta2_boundary_theorem_preserved', '|theta|<2' in text)
ck('B0_monotonic_theorem_preserved', 'B0(a) er nonincreasing' in text)
ck('old_wall_failure_preserved', '696.320960517<energy upper818.962302959' in text)

p={k:exact_hex(v) for k,v in HEX.items()}
qs=[exact_hex(x) for x in QHEX]; ws=[exact_hex(x) for x in WHEX]
ck('positive_source_parameters', all(p[k] > 0 for k in ['H0','Omega0_b','Omega0_cdm','Omega0_g','Omega0_ur','F_eV','m_eV','B_floor','M_ncdm','factor_ncdm']))
ck('positive_quadrature', len(qs)==len(ws)==11 and all(x>0 for x in qs+ws))
ck('flat_lambda_zero', p['Omega0_lambda']==0)

# Frozen source constants and domain.
KAPPA = F(2435 * 10**24, 1)    # 2.435e27 eV, source-defined decimal
C = F(415239,100)               # 4152.39, source-defined decimal
FLOOR_COEF = F(3968,10**11)     # 3.968e-8
E_F_CAP = F(1400,1)             # exact previously proved common actual cap; deliberately conservative
A_MIN = F(1,1946)               # z=1945
A_F = F(1,1601)                 # z=1600
ck('domain_order', 0 < A_MIN < A_F)

H0sq=p['H0']*p['H0']
R=(p['Omega0_g']+p['Omega0_ur'])*H0sq
M=(p['Omega0_b']+p['Omega0_cdm'])*H0sq
LAMBDA = KAPPA/p['F_eV']
A_POT = C*p['m_eV']*p['m_eV']*p['F_eV']*p['F_eV']
FLOOR = p['B_floor']*FLOOR_COEF
ck('R_positive', R>0)
ck('M_positive', M>0)
ck('lambda_positive', LAMBDA>0)
ck('potential_amplitude_positive', A_POT>0)
ck('floor_positive', FLOOR>0)

# Exact finite-neutrino base bounds at the two domain endpoints.
rho_f_lo,rho_f_hi,eps_f = rho_nu_bounds(A_F,qs,ws,p['M_ncdm'],p['factor_ncdm'])
rho_m_lo,rho_m_hi,eps_m = rho_nu_bounds(A_MIN,qs,ws,p['M_ncdm'],p['factor_ncdm'])
B0_f_lo = R/A_F**4 + M/A_F**3 + p['Omega0_lambda']*H0sq + rho_f_lo
B0_f_hi = R/A_F**4 + M/A_F**3 + p['Omega0_lambda']*H0sq + rho_f_hi
B0_m_lo = R/A_MIN**4 + M/A_MIN**3 + p['Omega0_lambda']*H0sq + rho_m_lo
B0_m_hi = R/A_MIN**4 + M/A_MIN**3 + p['Omega0_lambda']*H0sq + rho_m_hi
ck('B0_endpoint_positive', B0_f_lo>0 and B0_m_lo>0)
ck('B0_monotonic_endpoint_order', B0_m_lo > B0_f_lo)

# Backward energy and velocity theorem.
# (a^6 e)_u = 6 a^6 U >= 0 -> e(a) <= E_F_CAP*(A_F/a)^6 for a<=A_F.
E_MIN_MAX = E_F_CAP*(A_F/A_MIN)**6
sqrt_2E_lo,sqrt_2E_hi = sqrt_bounds(2*E_F_CAP)
X_GLOBAL_MAX = sqrt_2E_hi*(A_F/A_MIN)**3
ck('backward_energy_finite', E_MIN_MAX > E_F_CAP and E_MIN_MAX < 10**6)
ck('X_global_finite', X_GLOBAL_MAX > 0)

# Branch-independent displacement: H^2 >= B0(a) >= B0(A_F), and B0(A_F)>=B0_f_lo.
# |X| <= sqrt(2 E_F_CAP)*(A_F/s)^3.
# Integral gives D(a) <= sqrt(2E/Bmin)/3 * ((A_F/a)^3 - 1).
sqrt_B_lo,sqrt_B_hi = sqrt_bounds(B0_f_lo)
D_GLOBAL = (sqrt_2E_hi/sqrt_B_lo) * (((A_F/A_MIN)**3 - 1) / 3)
PHI_ANCHOR = 2/LAMBDA    # closure of the strict Math017 |theta_f|<2 anchor
PHI_GLOBAL = PHI_ANCHOR + D_GLOBAL
ck('displacement_finite', D_GLOBAL > 0 and D_GLOBAL < 10)
ck('phi_anchor_finite', PHI_ANCHOR > 0)
ck('phi_global_finite', PHI_GLOBAL > PHI_ANCHOR and PHI_GLOBAL < 10)

# Global H hull, preserving exact same-time H relation in the certificate itself.
H_GLOBAL_LO = sqrt_B_lo  # H^2 >= B0 >= B0_f_lo; floor/e omitted conservatively
H2_GLOBAL_HI_ARG = B0_m_hi + (E_MIN_MAX + FLOOR)/3
H_GLOBAL_HI_LO,H_GLOBAL_HI = sqrt_bounds(H2_GLOBAL_HI_ARG)
ck('H_global_finite', 0 < H_GLOBAL_LO < H_GLOBAL_HI)
ck('H_upper_square_encloses', H_GLOBAL_HI*H_GLOBAL_HI >= H2_GLOBAL_HI_ARG)

# Sanity: exact potential range is globally valid without a branch cap.
U_GLOBAL_MAX = 8*A_POT
ck('periodic_potential_global_range', U_GLOBAL_MAX>0)
# No requirement that the broad phi outer box stay inside |theta|<2.
THETA_DISPLACEMENT_MAX = LAMBDA*D_GLOBAL
ck('branch_independent_not_wall_reuse', THETA_DISPLACEMENT_MAX > 2)

result={
  'artifact_type':'BUBBLEVERSE_MATHEMATICAL_RESULT',
  'result_id':'LOCAL-Q048-MATH021-HILLIPOP-BRANCH-INDEPENDENT-SCALAR-ENCLOSURE-V1',
  'task_id':'LOCAL-Q048-HILLIPOP-EDE-BRANCH-INDEPENDENT-SCALAR-ENCLOSURE-MATH-V1',
  'q':'Q048',
  'target_q':'Q048',
  'question_sha256':EXPECTED['question_sha256'],
  'case':'hillipop-ede_n3',
  'status':'PASS_FINITE_BRANCH_INDEPENDENT_SCALAR_OUTER_OBJECT',
  'scientific_scope':'CONDITIONAL_SOURCE_REAL_MATHEMATICAL_COMPONENT_ONLY',
  'q_completion_gate':'NOT_SATISFIED',
  'source_commit':EXPECTED['source_commit'],
  'capture_sha256':EXPECTED['capture_sha256'],
  'input_hashes':{
      'journal_sha256':EXPECTED['journal_sha256'],
      'prompt_sha256':EXPECTED['prompt_sha256'],
      'handoff_sha256':EXPECTED['handoff_sha256']},
  'method':{
      'u':'ln(a)',
      'domain_a':ibox(A_MIN,A_F),
      'domain_z_closed_outer':[1600,1945],
      'event_root_prior':'1600 < z_e < 1945; event time itself not localized by this result',
      'boundary_a_f':rat(A_F),
      'boundary_anchor':'Math017 strict |theta(a_f)|<2; use closed outer |phi_f|<=2/lambda',
      'energy_cap_choice':{
          'value_exact':rat(E_F_CAP),
          'display':'1400',
          'reason':'Use the exact inherited proved common cap instead of a displayed approximate later final e_upper.'},
      'identities':[
          'theta=lambda*phi',
          'U=A*(1-cos(theta))^3',
          'e=X^2/2+U',
          'H^2=B0(a)+(e+floor)/3',
          'phi_u=X/H',
          'e_u=-3*X^2',
          '(a^6*e)_u=6*a^6*U>=0'],
      'backward_energy_bound':'e(a)<=E_f*(a_f/a)^6',
      'velocity_bound':'|X(a)|<=sqrt(2E_f)*(a_f/a)^3',
      'base_bound':'B0(a)>=B0(a_f)>=B0_f_lower>0 on the closed domain',
      'displacement_bound':'|phi(a)-phi_f|<=sqrt(2E_f/B0_f_lower)/3*((a_f/a)^3-1)',
      'coupling_rule':'The outer object retains exact e-X-U(phi), H-B0-e, theta-lambda-phi relations; independent hull corners are not claimed to be source solutions.',
      'periodic_rule':'No local trig range cap is used away from a_f; exact periodic U is retained globally.'},
  'source_constants':{
      'hex_binary64':HEX,
      'F_eV_exact':rat(p['F_eV']),
      'm_eV_exact':rat(p['m_eV']),
      'B_floor_exact':rat(p['B_floor']),
      'kappa_eV_exact':rat(KAPPA),
      'C_exact':rat(C),
      'lambda_exact':rat(LAMBDA),
      'lambda_display':dec(LAMBDA),
      'A_potential_exact':rat(A_POT),
      'A_potential_display':dec(A_POT),
      'floor_Mpc_minus2_exact':rat(FLOOR),
      'floor_display':dec(FLOOR),
      'R_exact':rat(R), 'R_display':dec(R),
      'M_matter_exact':rat(M), 'M_matter_display':dec(M)},
  'finite_neutrino':{
      'node_count':len(qs), 'positive_nodes_weights':True,
      'rho_at_af':ibox(rho_f_lo,rho_f_hi),
      'rho_at_amin':ibox(rho_m_lo,rho_m_hi)},
  'bounds':{
      'B0_af':ibox(B0_f_lo,B0_f_hi),
      'B0_amin':ibox(B0_m_lo,B0_m_hi),
      'phi_boundary_abs_max':{'exact':rat(PHI_ANCHOR),'display':dec(PHI_ANCHOR)},
      'phi_displacement_abs_max_over_root_window':{'exact_upper':rat(D_GLOBAL),'display_upper':dec(D_GLOBAL)},
      'phi_abs_max_over_root_window':{'exact_upper':rat(PHI_GLOBAL),'display_upper':dec(PHI_GLOBAL)},
      'theta_displacement_abs_max_from_boundary':{'exact_upper':rat(THETA_DISPLACEMENT_MAX),'display_upper':dec(THETA_DISPLACEMENT_MAX)},
      'e_max_over_root_window':{'exact_upper':rat(E_MIN_MAX),'display_upper':dec(E_MIN_MAX)},
      'X_abs_max_over_root_window_Mpc_minus1':{'exact_upper':rat(X_GLOBAL_MAX),'display_upper':dec(X_GLOBAL_MAX)},
      'H_global_lower_Mpc_minus1':{'exact_lower':rat(H_GLOBAL_LO),'display_lower':dec(H_GLOBAL_LO)},
      'H_global_upper_Mpc_minus1':{'exact_upper':rat(H_GLOBAL_HI),'display_upper':dec(H_GLOBAL_HI)},
      'U_global_range':'0 <= U(phi) <= 8*A exactly from -1<=cos<=1'},
  'event_time_outer_object':{
      'for_any_a_e':'a_e in (1/1946,1/1601)',
      'phi':'|phi_e| <= phi_boundary_abs_max + D(a_e); global closed-window cap supplied above',
      'X':'|X_e| <= sqrt(2E_f)*(a_f/a_e)^3',
      'e':'e_e=X_e^2/2+A*(1-cos(lambda*phi_e))^3 and 0<=e_e<=E_f*(a_f/a_e)^6',
      'H':'H_e^2=B0(a_e)+(e_e+floor)/3 with B0 from the captured photon/ur/matter/finite-neutrino source',
      'event_q':'q_e=1e-6 belongs to the later event packet, not derived here'},
  'claims':{
      'certified':['finite branch-independent scalar outer object across inherited H first-root window',
                   'finite phi/X/e/H bounds linked to captured hillipop-ede_n3 source',
                   'same-time periodic potential and Friedmann correlations retained'],
      'not_certified':['fourth E1/E2/E3 packet','actual event state serialization','paired latch/reset x_e histories',
                       'tau_T differences','native P6','physical confirmation/falsification','Q048 closure']},
  'old_method':'theta=2 wall nonclosure remains preserved; this result is a different global periodic/displacement enclosure, not a retry.',
  'next_route':'RESULT INGESTION & ROUTING ENGINE before any further event-payload implementation or paired histories',
  'reproducibility':'R2_LOCAL_EXACT_RATIONAL_COMPONENT_WITH_OUTWARD_SQRT_BOUNDS'
}
validation={
  'artifact_type':'BUBBLEVERSE_VALIDATION_RESULT',
  'result_id':result['result_id'],
  'validation_status':'PASS_EXACT_RATIONAL_AND_OUTWARD_BOUND_CHECKS',
  'checks_total':len(checks),
  'checks_passed':sum(int(x['pass']) for x in checks),
  'checks':checks,
  'independence_note':'Validation checks exact identities/input binding and outward arithmetic. It is not an independent cosmological trajectory or native implementation.',
  'decision':'ACCEPT scalar outer object within conditional source-real scope; do not promote to fourth event packet or Q completion.'
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
VAL.write_text(json.dumps(validation,indent=2,sort_keys=True)+'\n')
print(json.dumps({
    'status':result['status'], 'checks':f"{validation['checks_passed']}/{validation['checks_total']}",
    'phi_boundary':result['bounds']['phi_boundary_abs_max']['display'],
    'dphi':result['bounds']['phi_displacement_abs_max_over_root_window']['display_upper'],
    'phi_abs':result['bounds']['phi_abs_max_over_root_window']['display_upper'],
    'X_abs':result['bounds']['X_abs_max_over_root_window_Mpc_minus1']['display_upper'],
    'e_max':result['bounds']['e_max_over_root_window']['display_upper'],
    'H_lo':result['bounds']['H_global_lower_Mpc_minus1']['display_lower'],
    'H_hi':result['bounds']['H_global_upper_Mpc_minus1']['display_upper'],
},indent=2))
