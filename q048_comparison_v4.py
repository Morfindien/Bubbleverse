"""Positive diagonal comparison for normalized h=1 new cells only.

All physics and outward interval primitives are the frozen Q048 backend.
No stored weight is admitted as proof. Original cells use original certification.
"""
from fractions import Fraction as F
import q048_prefix_v1 as p
m=p.m;old=p.old;pre=p.pre
METHOD='positive_diagonal_v1'
THERMAL_METHOD='he1_outer_lower_v1'

def diagnostic(cell,current,field):
 if cell['t0']!='0' or cell['t1']!='1':raise ValueError('NORMALIZED_CELL_REQUIRED')
 coeff=[[F(v) for v in row] for row in cell['predictor']];n=len(current)
 if n not in (1,2) or len(coeff)!=n or len(cell['box'])!=n:raise ValueError('COMPARISON_DIMENSION')
 box=[old.interval(v) for v in cell['box']];pr=[old.poly_range(row) for row in coeff]
 dr=[old.poly_range([F(k)*row[k] for k in range(1,len(row))] or [F(0)]) for row in coeff]
 r0=[max(abs(current[i].lo-coeff[i][0]),abs(current[i].hi-coeff[i][0])) for i in range(n)]
 fp=field(m.I(0,1),[m.A(v) for v in pr])
 ff=field(m.I(0,1),[m.A(box[i],[m.I(int(i==j)) for j in range(2)]) for i in range(n)])
 delta=[(dr[i]-pre.value(fp[i])).absmax() for i in range(n)]
 M=[[ff[i].d[j].hi if i==j else ff[i].d[j].absmax() for j in range(n)] for i in range(n)]
 return coeff,pr,box,r0,delta,M

def positive_weight(M):
 if M[0][1]<=0 or M[1][0]<=0:raise ValueError('POSITIVE_OFFDIAGONALS_REQUIRED')
 interval=m.sqrt_i(m.I(M[1][0]/M[0][1]));weight=(interval.lo+interval.hi)/2
 if weight<=0:raise ValueError('WEIGHT_POSITIVITY')
 return weight

def weighted_certificate(cell,current,field):
 coeff,pr,box,r0,delta,M=diagnostic(cell,current,field)
 if len(current)!=2:raise ValueError('BACKGROUND_DIMENSION')
 w=positive_weight(M);B=[[M[0][0],M[0][1]*w],[M[1][0]/w,M[1][1]]]
 E,J=old.comparison_matrices(B,F(1));r=[r0[0],r0[1]/w];d=[delta[0],delta[1]/w]
 end=[sum((E[i][j]*r[j]+J[i][j]*d[j] for j in range(2)),m.I(0)) for i in range(2)]
 sigma=max(F(0),-min(B[0][0],B[1][1]));N=[[B[i][j]+(sigma if i==j else 0) for j in range(2)] for i in range(2)]
 EN,_=old.comparison_matrices(N,F(1))
 bound=[sum((EN[i][j]*(r[j]+d[j]) for j in range(2)),m.I(0)) for i in range(2)]
 end=[end[0],end[1]*w];bound=[bound[0],bound[1]*w]
 slack=[min(pr[i].lo-bound[i].hi-box[i].lo,box[i].hi-pr[i].hi-bound[i].hi) for i in range(2)]
 return {'closed':all(s>0 for s in slack),'closure_slack':list(map(str,slack)),
         'initial_error':list(map(str,r0)),'defect_upper':list(map(str,delta)),
         'comparison':[[str(v) for v in row] for row in M],
         'weighted_comparison':[[str(v) for v in row] for row in B],'weight':str(w),
         'alltime_error':list(map(old.pairs,bound)),'endpoint_error':list(map(old.pairs,end)),
         'endpoint':[old.pairs(m.I(old.poly_at(coeff[i],F(1))-end[i].hi,old.poly_at(coeff[i],F(1))+end[i].hi)) for i in range(2)],
         'whole_state':[old.pairs(m.I(pr[i].lo-bound[i].hi,pr[i].hi+bound[i].hi)) for i in range(2)]}

def check_thermal_supersolution(cell,current,field):
 coeff,pr,box,r0,delta,M=diagnostic(cell,current,field)
 if len(current)!=1 or len(coeff[0])!=1 or M[0][0]>=0:raise ValueError('CONTRACTIVE_CONSTANT_THERMAL_REQUIRED')
 R=max(r0[0],delta[0]/(-M[0][0]))
 slack=min(pr[0].lo-R-box[0].lo,box[0].hi-pr[0].hi-R)
 if slack<=0:raise ValueError('THERMAL_SUPERSOLUTION_NOT_CLOSED')
 return R,slack
