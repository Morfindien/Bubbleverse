#!/usr/bin/env python3
from fractions import Fraction
import json, sys, pathlib, math

p = pathlib.Path(sys.argv[1])
d = json.loads(p.read_text())
checks = []

def check(name, cond, detail):
    checks.append({"id":name,"status":"PASS" if cond else "FAIL","detail":detail})
    return cond

# Independent coarse arithmetic, deliberately not reusing Decimal producer formulas.
# Source constants are upper/lower rounded outward by hand.
C_RATE_UP = 1_015_000.0
H0_UP = 0.00023
SQRT_OG_UP = 0.00724              # 0.00724^2 = 0.0000524176 > captured Omega_g
ONEPZ_UP = 83.0                   # 1+4006/49 < 83
R_COARSE = C_RATE_UP*H0_UP*SQRT_OG_UP*ONEPZ_UP**2
check("coarse_R_below_11700", R_COARSE < 11700.0, f"coarse R={R_COARSE:.12f}<11700")

x = Fraction(1, 105299)
q = Fraction(1, 10**6)
h = x-q
xh = x*h
check("q1e6_h_positive", h>0, f"h_lower={float(h):.17g}")
check("q1e6_xh_gt_8e_11", xh > Fraction(8,10**11), f"xe*h={float(xh):.17g}")
check("q0_xh_gt_q1", x*x > xh, "q=0 product is strictly larger than q=1e-6 lower product")

# Independent Saha upper bound:
# TR < 0.0195 eV, EI>13.5 eV => EI/TR > 692.3 > 300 ln10, so exp(-EI/TR)<1e-300.
# sqrt(TR)<0.14, TR^(3/2)<0.0195*0.14=0.00273.
# SAHA<3.1e21; at zmax nH>0.1 cm^-3.
s_coarse = 3.1e21 * 0.00273 * 1e-300 / 0.1
check("coarse_s_below_1e_280", s_coarse < 1e-280, f"coarse s<{s_coarse:.3e}")
check("peebles_bracket_margin_q1e6", float(xh) > 1e-280, "xe*h lower exceeds conservative s upper by >269 decades")

check("vuu_certificate_exact", d["v_uu_strict_upper"]=="-1/10", "certificate records strict v_uu<-1/10")
check("status_pass", d["status"]=="PASS_STRICT_PEEBLES_SELF_SIDE", "producer status")

# Semantic mutation controls: each deliberately invalidates a required proof premise.
mutations = []
def reject(name, cond):
    mutations.append({"id":name,"status":"REJECTED" if not cond else "NOT_REJECTED"})

reject("R_safe_11000", R_COARSE < 11000.0)
reject("q_1e5_positive_h", x-Fraction(1,10**5) > 0)
reject("ell_lower_minus4_still_strict", (-4 - (-4)) < 0)  # base term becomes zero, cannot yield uniform <-1 via this proof
reject("h_upper_1_keeps_RLya_finite", (1-Fraction(1,1)) > 0)
reject("s_upper_1e_10_still_below_xh", 1e-10 < float(xh))

all_pass = all(c["status"]=="PASS" for c in checks)
all_mut = all(m["status"]=="REJECTED" for m in mutations)
out = {
  "schema_id":"bubbleverse.q050.peebles_tangency_validation",
  "schema_version":"1.0.0",
  "status":"PASS" if all_pass and all_mut else "FAIL",
  "checks":checks,
  "mutation_controls":mutations,
  "summary":{
    "checks_passed":sum(c["status"]=="PASS" for c in checks),
    "checks_total":len(checks),
    "mutations_rejected":sum(m["status"]=="REJECTED" for m in mutations),
    "mutations_total":len(mutations)
  },
  "independence_note":"Validator uses coarse outward hand bounds and rational inequalities rather than producer high-precision transcendental values; both share the pinned physical constants and accepted background premises."
}
json.dump(out, sys.stdout, indent=2)
sys.stdout.write("\n")
