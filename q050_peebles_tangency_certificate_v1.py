#!/usr/bin/env python3
from decimal import Decimal, getcontext
from fractions import Fraction
import json, sys
getcontext().prec = 90

# Frozen Q047/Q049 capture values (binary64-decoded values where applicable)
H0 = Decimal("0.00022919563365907353")       # CLASS H0 in 1/Mpc
OMEGA_G = Decimal("0.00005238010834530901")
T0_K = Decimal("2.7255")
NH0_M3 = Decimal("0.18806240632995103")
FHE = Decimal("0.081852545572712224")

# Pinned CLASS/HyRec source constants
SIGMA_T = Decimal("6.6524616e-29")
M_E = Decimal("9.10938215e-31")
C = Decimal("2.99792458e8")
MPC_M = Decimal("3.085677581282e22")
J_PER_M3_PER_MPC2 = Decimal("0.0151730087")
KB_EV_K = Decimal("8.617343e-5")
SAHA_FACT = Decimal("3.016103031869581e21")
EI_EV = Decimal("13.598286071938324")

Z_MAX = Decimal(4006) / Decimal(49)
ONEPZ_MAX = Decimal(1) + Z_MAX

# At v=Tmat/Trad=0.1, A=Gamma_gamma_b/H.
# Write A = R(z) * x/(1+fHe+x), where R is electron-fraction independent.
C_RATE = (Decimal(2)*SIGMA_T/(M_E*C))*(Decimal(4)/Decimal(3))*J_PER_M3_PER_MPC2*(MPC_M/C)

# Frozen positive flat background gives H_CLASS >= H0*sqrt(Omega_g)*(1+z)^2,
# hence R(z) <= C_RATE*H0*sqrt(Omega_g)*(1+z)^2.
R_BOUND_DECIMAL = C_RATE * H0 * OMEGA_G.sqrt() * ONEPZ_MAX**2

# Use an intentionally rounded-up proof constant that is also independently verifiable.
R_SAFE = Decimal("11700")
if not R_BOUND_DECIMAL < R_SAFE:
    raise SystemExit("R_SAFE does not dominate direct bound")

# Tangency A=1/9 forces x/(1+f+x)=1/(9R) >= 1/(9 R_SAFE).
# Since f>=0: x >= y/(1-y) = 1/(9 R_SAFE - 1).
x_lower = Fraction(1, 9*11700 - 1)
qL = Fraction(1, 10**6)
qR = Fraction(0, 1)
hL_lower = x_lower - qL
hR_lower = x_lower
if hL_lower <= 0:
    raise SystemExit("left-q tangent lower bound does not force positive h")
xhL_lower = x_lower*hL_lower
xhR_lower = x_lower*hR_lower

# Source-real Saha term s is monotone increasing over the material strip because
# d ln s / d ln(1+z) = -3/2 + EI/TR > 0 there. Evaluate its maximum at zmax.
TR_MAX = KB_EV_K*T0_K*ONEPZ_MAX
nH_MAX_cm3 = NH0_M3*Decimal("1e-6")*ONEPZ_MAX**3
s_max_decimal = SAHA_FACT*TR_MAX*TR_MAX.sqrt()*(-EI_EV/TR_MAX).exp()/nH_MAX_cm3

# Strong, independently checkable coarse proof bound.
s_safe = Decimal("1e-280")
if not s_max_decimal < s_safe:
    raise SystemExit("Saha proof bound failed")
if not Decimal(xhL_lower.numerator)/Decimal(xhL_lower.denominator) > s_safe:
    raise SystemExit("q=1e-6 Peebles bracket sign not certified")
if not Decimal(xhR_lower.numerator)/Decimal(xhR_lower.denominator) > s_safe:
    raise SystemExit("q=0 Peebles bracket sign not certified")

# On v=0.1, alpha_B(Tm)>alpha_B(Tr)>0 because source alphaB_PPB(T)
# is strictly decreasing and Tm=0.1 Tr. Therefore x*h>s is stronger than needed:
# alpha_TM*x*h - alpha_TR*s*(1-h) > 0.
# With positive nH/H and C-factor, h_u<0.
#
# Above reionization start on the tangent strip, x_reio=x_noreio=h+q and q is fixed,
# so x_u=h_u<0.
#
# A_u/A = -4 - ell + (1+f)/(x(1+f+x))*x_u.
# Inherited admitted-background bound ell=dlnH/dlna >= -3, so A_u/A < -1.
# At A=1/9: A_u < -1/9.
# v_uu=(1-v)A_u at v_u=0 -> v_uu < (9/10)*(-1/9)=-1/10.
vuu_strict_upper = Fraction(-1, 10)

out = {
  "schema_id":"bubbleverse.q050.peebles_tangency_numeric_certificate",
  "schema_version":"1.0.0",
  "status":"PASS_STRICT_PEEBLES_SELF_SIDE",
  "z_material_strip":{
    "lower_open_approx":"16.0310108356",
    "upper_exact":"4006/49",
    "upper_decimal":str(Z_MAX)
  },
  "tangent":{"v":"1/10","A":"1/9"},
  "electron_independent_rate_bound":{
    "C_rate_decimal":str(C_RATE),
    "R_direct_upper_decimal":str(R_BOUND_DECIMAL),
    "R_safe_integer":11700
  },
  "tangent_forced_lower_bounds":{
    "x_e_exact":f"{x_lower.numerator}/{x_lower.denominator}",
    "x_e_decimal":str(Decimal(x_lower.numerator)/Decimal(x_lower.denominator)),
    "q_1e6_h_exact":f"{hL_lower.numerator}/{hL_lower.denominator}",
    "q_1e6_xe_times_h_exact":f"{xhL_lower.numerator}/{xhL_lower.denominator}",
    "q_1e6_xe_times_h_decimal":str(Decimal(xhL_lower.numerator)/Decimal(xhL_lower.denominator)),
    "q_0_h_exact":f"{hR_lower.numerator}/{hR_lower.denominator}",
    "q_0_xe_times_h_exact":f"{xhR_lower.numerator}/{xhR_lower.denominator}",
    "q_0_xe_times_h_decimal":str(Decimal(xhR_lower.numerator)/Decimal(xhR_lower.denominator))
  },
  "saha":{
    "TR_max_eV":str(TR_MAX),
    "nH_at_zmax_cm3":str(nH_MAX_cm3),
    "s_direct_max_decimal":str(s_max_decimal),
    "s_safe_upper":"1e-280",
    "monotonicity":"dlns/dln(1+z)=-3/2+EI/TR>0 on strip"
  },
  "sign_chain":[
    "source alphaB_PPB(T) is strictly decreasing; at v=0.1 alpha_TM>alpha_TR>0",
    "xe*h > s >= s*(1-h) implies alpha_TM*xe*h-alpha_TR*s*(1-h)>0",
    "injection=0 and Peebles C,nH,H are positive/finite on inherited h<=99999/100000 domain",
    "therefore h_u<0 for q=1e-6 and q=0",
    "z>reionization_start throughout material strip, so x_u=h_u<0",
    "ell=dlnH/dlna>=-3 gives A_u/A<-1",
    "at A=1/9, A_u<-1/9",
    "at v=1/10 and v_u=0, v_uu=(9/10)A_u<-1/10"
  ],
  "v_uu_strict_upper":"-1/10",
  "conclusion":"The source-real equality-assigned PEEBLES branch departs quadratically into v<1/10 at every admissible tangent state in the material strip, for both q branches."
}
json.dump(out, sys.stdout, indent=2)
sys.stdout.write("\n")
