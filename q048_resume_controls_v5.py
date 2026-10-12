"""Current V4-cursor controls, freshly reconstructed and independently bounded."""
from fractions import Fraction as F
import argparse,json
import q048_resume_v5 as e
from q048_resume_controls_v3 import independent_vector,series_exponential
p=e.p

def background_control(case):
 settings=e.load(e.ROOT/'q048_resume_config_v5.json');r,_,_=e.parent_from_asset(case,settings)
 row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=p.parameters(row)
 x=e.load(e.ROOT/'q048_resume_control_fixture_v5.json')[case]['background']
 now,current=e.cursor(r['background']);a1=now+(min(F(1,2871),now*F(5,4))-now)/4096;width=a1-now
 field=lambda xi,y:[v*width/(now+width*xi) for v in p.pre.ede_field(now+width*xi,y,t)[0]]
 center=[(v.lo+v.hi)/2 for v in current];slopes=list(map(p.pre.value,field(p.m.I(0),[p.m.A(v) for v in center])))
 pred=[[str(center[i]),str((slopes[i].lo+slopes[i].hi)/2)] for i in range(2)]
 candidate={'t0':'0','t1':'1','predictor':pred,'box':e.legacy_box(current,pred)}
 proof=e.certify_background(candidate,current,field)
 if (candidate!=x['candidate'] or proof!=x['certificate'] or str(now)!=x['a0'] or str(a1)!=x['a1']
     or list(map(p.pairs,current))!=x['current'] or not proof['closed']):raise ValueError('CONTROL_BACKGROUND_PROOF')
 bg=p.pre.background(p.m.I(now,a1),t,[p.old.interval(v) for v in proof['whole_state']])
 cell={'a0':str(now),'a1':str(a1),'predictor':pred,'box':candidate['box'],'certificate':proof,
       'comparison_method':e.comparison.METHOD,'comparison_weight':proof['weight'],'forcing':{k:p.pairs(v) for k,v in bg.items()}}
 e.verify_background_cell(cell,now,current,t)
 _,pr,box,r0,delta,M=e.comparison.diagnostic(candidate,current,field)
 w=e.comparison.positive_weight(M);B=[[M[0][0],M[0][1]*w],[M[1][0]/w,M[1][1]]]
 ep,bound,si,sn=independent_vector(B,[r0[0],r0[1]/w],[delta[0],delta[1]/w])
 ep=[ep[0],ep[1]*w];bound=[bound[0],bound[1]*w]
 slack=[min(pr[i].lo-bound[i].hi-box[i].lo,box[i].hi-pr[i].hi-bound[i].hi) for i in range(2)]
 whole=[p.m.I(pr[i].lo-bound[i].hi,pr[i].hi+bound[i].hi) for i in range(2)]
 independent_bg=p.pre.background(p.m.I(now,a1),t,whole)
 overlap=[max(ep[i].lo,p.old.interval(proof['endpoint_error'][i]).lo)<=min(ep[i].hi,p.old.interval(proof['endpoint_error'][i]).hi) for i in range(2)]
 if min(slack)<=0 or not all(overlap) or independent_bg['H'].lo<=0 or independent_bg['ede_latch'].hi>=F(1,2):
  raise ValueError('INDEPENDENT_BACKGROUND_CONTROL')
 report={'gate':'PASS','halving':12,'closure_slack':list(map(str,slack)),
         'endpoint_overlap':overlap,'positive_H':True,'source_guard':p.pairs(independent_bg['ede_latch']),
         'signed_series':si,'majorant_series':sn}
 return row,now,current,cell,report

def thermal_control(case):
 settings=e.load(e.ROOT/'q048_resume_config_v5.json');r,_,_=e.parent_from_asset(case,settings)
 row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=p.parameters(row)
 x=e.load(e.ROOT/'q048_resume_control_fixture_v5.json')[case]['thermal']
 now=F(r['thermal']['certified_end_a']);current=[p.old.interval(v) for v in r['thermal']['endpoint']]
 boundaries=[1/(1-p.point(s['mz']).lo) for s in row['thermal_starts'][1:5]];j=sum(now>=v for v in boundaries);mode=p.pre.MODES[j]
 cover=next(c for c in r['background']['cells'] if F(c['a0'])<=now<F(c['a1']))
 end=min(boundaries[j],now*F(5,4),F(1,2871),F(r['background']['certified_end_a']),F(cover['a1']))
 a1=now+(end-now)/128;width=a1-now;getbg=lambda a:e.background_at(a,t,r['background'],cover)
 field=lambda xi,y:[p.pre.thermal(mode,now+width*xi,y[0],t,getbg(now+width*xi))['rate']*width/(now+width*xi)]
 center=(1/(1+p.pre.thermal(mode,p.m.I(now+width/2),p.m.I(0),t,getbg(p.m.I(now+width/2)))['beta'])).lo
 candidate={'t0':'0','t1':'1','predictor':[[str(center)]],'box':[['-1/500000','1/50']]}
 proof=p.certify(candidate,current,field)
 if (candidate!=x['candidate'] or proof!=x['primary'] or str(now)!=x['a0'] or str(a1)!=x['a1']
     or e.objhash(cover)!=x['covering_background_sha256'] or not proof['closed']):raise ValueError('CONTROL_THERMAL_PROOF')
 try:e.legacy.thermal_guard(candidate,current,field,mode,t,now,a1,getbg,proof,e.comparison.THERMAL_METHOD)
 except ValueError as err:
  if str(err)!='THERMAL_SUPERSOLUTION_NOT_CLOSED':raise
 else:raise ValueError('LEGACY_FAILURE_NOT_REPRODUCED')
 info=e.thermal_guard(candidate,current,field,mode,t,now,a1,getbg,proof,e.comparison.FINITE_THERMAL_METHOD)
 U,slack=e.comparison.check_thermal_finite_time(candidate,current,field)
 _,_,_,r0,delta,M=e.comparison.diagnostic(candidate,current,field)
 A=[[M[0][0],F(1)],[F(0),F(0)]];E,series=series_exponential(A,F(1))
 enderr=E[0][0]*r0[0]+E[0][1]*delta[0];bound=max(r0[0],enderr.hi)
 independent_slack=min(center-bound-F(candidate['box'][0][0]),F(candidate['box'][0][1])-center-bound)
 if independent_slack<=0 or bound>U:raise ValueError('INDEPENDENT_FINITE_THERMAL_CONTROL')
 cell={'a0':str(now),'a1':str(a1),'mode':mode,'predictor':candidate['predictor'],'box':candidate['box'],
       'certificate':proof,'thermal_tube_method':e.comparison.FINITE_THERMAL_METHOD,
       'Tmat_K':p.pairs(info['Tmat']),'xe_thermal':p.pairs(info['x'])}
 return row,now,current,cell,getbg,{'gate':'PASS','halving':7,'finite_upper':str(U),
        'finite_slack':str(slack),'independent_slack':str(independent_slack),'series':series,
        'legacy_stationary_failure':'REPRODUCED','positive_temperature':True,'positive_beta':True}

def controls():
 return {'schema':'Q048_RESUME_CONTROLS_V5','q':e.Q,'program_id':e.ID,
  'scope':'CONDITIONAL_SOURCE_REAL_SINGLE_CELL_CONTROLS',
  'background':{c:background_control(c)[-1] for c in ('camspec-ede_n3','hillipop-ede_n3')},
  'thermal':{c:thermal_control(c)[-1] for c in ('camspec-ede_n3','hillipop-ede_n3')},
  'finite_controls_gate':'PASS','final_result_gate':'UNRESOLVED'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',default='q048_resume_controls_v5.json');args=a.parse_args()
 r=controls();p.old.write(args.out,r);print(json.dumps({'finite_controls_gate':r['finite_controls_gate'],'final_result_gate':'UNRESOLVED'}))
