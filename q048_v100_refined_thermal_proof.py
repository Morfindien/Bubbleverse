import sys,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/mnt/data/q048_from_v97/helpers')
import q048_full_tube_reuse_v1 as old
m=old.m; d=old.d; k=old.k; prefix=old.prefix
R=Path('/mnt/data/q048_from_v97')
parent=json.load(open(R/'q048_frec_moving_h_accepted_checkpoint_v97.json'))
guard=json.load(open(R/'q048_guard_local_v_result_v12.json'))
primary,control=[ev['rows'][47] for ev in guard['evaluators']]
cap=json.load(open(R/'q048_prefix_config_v1.json')); prefix.validate_config(cap)
case=cap['cases']['hillipop-ede_n3']; t=prefix.parameters(case)
a=m.I(F(1,981),F(1,971)); import os
w_hi=F(os.environ.get('WHI','0.01'))
w=m.I(F(-1,1000000),w_hi); eps=F(1,1000000); h0=F(parent['connected_lower']); hmax=F(99999,100000)
B,floor,H,Hs=old.background(a,t,F(primary['E_safe_left'])); HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
TR=m.const('8.617343e-5')*t['T0']/a; Tgamma=t['T0']/a; ratio=1-w
p3=json.load(open(R/'q048_p3_scaled_raw_result_v2.json')); fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator'])
alpha,rr=old.load_atomic(R/'q048_p3_scaled_transformed_log_tables_v2.json'); atomic=old.local_atomic(alpha,rr,TR,ratio)
source_checks={'model4':all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),'fixed_flags':all(case['background']['thermal_flags'][z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'above900':970>900,'TR':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma':1775<Tgamma.lo<=Tgamma.hi<4415,'ratio':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'H_positive':HsK.lo>0,'guard_admitted':primary['accepted'] and primary['committed'] and primary['whole_cell_qualified'] and primary['domain']['admitted'] and all(primary['domain']['checks'].values())}
A=list(map(old.fromk,atomic['Alpha'])); Ae=list(map(old.fromk,atomic['Alpha_eq'])); RR=old.fromk(atomic['R2p2s']); n=t['nH0']/a**3*m.const('1e-6')
saha=m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
Beta=[Ae[i]*m.const('3.016101031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
atomic_positive=min(z.lo for z in A+Ae+[RR,n,saha]+Beta)>0
Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo
# exact outward ceil/floor 18 from producer family
ceil18=lambda x:F(-((-x.numerator*10**18)//x.denominator),10**18)
floor18=lambda x:F(x.numerator*10**18//x.denominator,10**18)
K=ceil18(Kexact)
du0=k.log_i(k.I(a.hi/a.lo)); du=m.I(du0.lo,du0.hi);
# primary endpoint
def primary_endpoint(K,epsilon,du,initial):
    if epsilon==0:return initial/(1+K*initial*du)
    return epsilon/((1+epsilon/initial)*m.exp_i(K*epsilon*du)-1)
def rational_lower(K,epsilon,du_upper,initial):
    if epsilon==0:return initial/(1+K*initial*du_upper)
    x=K*epsilon*du_upper
    return epsilon/((1+epsilon/initial)/(1-x)-1)
endpoint=primary_endpoint(K,eps,du,h0); control_lower=rational_lower(K,eps,a.hi/a.lo-1,h0); hmin=floor18(min(endpoint.lo,control_lower)); h=m.I(hmin,hmax)
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,m.I):return {'lo':str(x.lo),'hi':str(x.hi),'display_lo':float(x.lo),'display_hi':float(x.hi)}
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,list):return [enc(v) for v in x]
    return x
L0=m.const('8.2206'); P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
gs=Beta[0]+3*RR+L0; gp=Beta[1]+RR+P; D=(Beta[0]+L0)*(Beta[1]+RR+P)+3*RR*(Beta[1]+P); Ns=L0*gp+3*RR*P; Np=P*gs+RR*L0; ds=Beta[0]*gp+3*RR*Beta[1]; dp=Beta[1]*gs+RR*Beta[0]
c_positive=min(z.lo for z in [L0,P,gs,gp,D,Ns,Np,ds,dp])>0
branches={}
for label,q in [('L',eps),('R',F(0))]:
    high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)]
    thermal=old.thermal_certificate(a,h,q,t,Hs); thermal['faces']=d.thermal_faces(thermal['beta'].lo,thermal['beta'].hi,F(-1,1000000),w_hi)
    checks={'upper_h_0':high[0].lo>0,'upper_h_1':high[1].lo>0,'thermal_denominator':thermal['thermal_denominator'].lo>0,'beta':thermal['beta'].lo>0,'thermal_faces':thermal['faces']['admitted']}
    branches[label]={'q':q,'upper_h_face_terms':high,'thermal':thermal,'checks':checks,'admitted':all(checks.values()),
      'signed_margins':{'upper_h_0':high[0].lo,'upper_h_1':high[1].lo,'thermal_denominator':thermal['thermal_denominator'].lo,'beta':thermal['beta'].lo,'lower_face_inward_lower':thermal['faces']['lower_face_inward_lower'],'upper_face_inward_margin':thermal['faces']['upper_face_inward_margin']}}
out={'source_checks':source_checks,'source_all':all(source_checks.values()),'atomic_positive':atomic_positive,'c_positive':c_positive,'schema_version':'Q048_V97_RESTART_980_970_L_GATE_DIAGNOSTIC_V1','historical_replay':False,'diagnostic_only':True,'cell_z':[980,970],'actual_state_unchanged':{'count':110,'frontier':980},'guard_primary_index':47,'guard_primary_E_safe_left':primary['E_safe_left'],'a':a,'h0':h0,'K_unrounded':Kexact,'K_upper':K,'endpoint_primary':endpoint,'endpoint_control':control_lower,'hmin':hmin,'TR_eV':TR,'Tgamma_K':Tgamma,'ratio':ratio,'A':A,'Ae':Ae,'Saha':saha,'Hs':Hs,'branches':branches}
print(json.dumps(enc(out),indent=2))
