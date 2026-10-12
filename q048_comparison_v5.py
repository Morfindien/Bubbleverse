"""V4 background/historical scalar semantics plus explicit new finite-time method."""
from fractions import Fraction as F
from q048_comparison_v4 import (diagnostic,positive_weight,weighted_certificate,
                               check_thermal_supersolution,METHOD,THERMAL_METHOD)
FINITE_THERMAL_METHOD='he1_outer_lower_finite_time_v1'

def check_thermal_finite_time(cell,current,field):
    # diagnostic enforces normalized xi in [0,1] and recomputes source error/J.
    coeff,pr,box,r0,delta,M=diagnostic(cell,current,field)
    if len(current)!=1 or len(coeff[0])!=1 or M[0][0]>=0:
        raise ValueError('FINITE_THERMAL_CONTRACTIVE_CONSTANT_DOMAIN')
    lam=-M[0][0]
    U=r0[0]+max(F(0),delta[0]/lam-r0[0])*min(F(1),lam)
    slack=min(pr[0].lo-U-box[0].lo,box[0].hi-pr[0].hi-U)
    if slack<=0:raise ValueError('THERMAL_FINITE_TIME_NOT_CLOSED')
    return U,slack
