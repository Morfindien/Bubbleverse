"""Three frozen finite remedies, independently evaluated with fresh inputs."""
import json,argparse,copy
from fractions import Fraction as F
import q048_resume_v4 as e
from q048_resume_controls_v3 import independent_vector
p=e.p

def background_control(case):
 settings=e.load(e.ROOT/'q048_resume_config_v4.json');r,_,_=e.parent_from_asset(case,settings)
 row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=p.parameters(row)
 now,current=e.cursor(r['background']);x=e.load(e.ROOT/'q048_resume_control_fixture_v4.json')['background'][case]
 if str(now)!=x['a0']:raise ValueError('CONTROL_CURRENT_STATE')
 a1=now+(min(F(1,2871),now*F(5,4))-now)/2**x['halving'];width=a1-now
 field=lambda xi,y:[v*width/(now+width*xi) for v in p.pre.ede_field(now+width*xi,y,t)[0]]
 center=[(v.lo+v.hi)/2 for v in current];slopes=list(map(p.pre.value,field(p.m.I(0),[p.m.A(c) for c in center])))
 pred=[[str(center[i]),str((slopes[i].lo+slopes[i].hi)/2)] for i in range(2)];box=e.legacy_box(current,pred)
 candidate={'t0':'0','t1':'1','predictor':pred,'box':box};proof=e.certify_background(candidate,current,field)
 if candidate!=x['cell'] or proof!=x['weighted_proof'] or str(a1)!=x['a1'] or not proof['closed']:raise ValueError('CONTROL_BACKGROUND_PROOF')
 bg=p.pre.background(p.m.I(now,a1),t,[p.old.interval(v) for v in proof['whole_state']])
 cell={'a0':str(now),'a1':str(a1),'predictor':pred,'box':box,'certificate':proof,
       'comparison_method':e.comparison.METHOD,'comparison_weight':proof['weight'],'forcing':{k:p.pairs(v) for k,v in bg.items()}}
 e.verify_background_cell(cell,now,current,t)
 return row,now,current,cell

def independent_background(case):
 row,now,current,cell=background_control(case);proof=cell['certificate'];w=F(proof['weight'])
 M=[[F(v) for v in rr] for rr in proof['comparison']];B=[[M[0][0],M[0][1]*w],[M[1][0]/w,M[1][1]]]
 r=list(map(F,proof['initial_error']));d=list(map(F,proof['defect_upper']))
 end,bound,info,infoN=independent_vector(B,[r[0],r[1]/w],[d[0],d[1]/w]);bound=[bound[0],bound[1]*w]
 pr=[p.old.poly_range(list(map(F,rr))) for rr in cell['predictor']];box=[p.old.interval(v) for v in cell['box']]
 slack=[min(pr[j].lo-bound[j].hi-box[j].lo,box[j].hi-pr[j].hi-bound[j].hi) for j in range(2)]
 whole=[p.m.I(pr[j].lo-bound[j].hi,pr[j].hi+bound[j].hi) for j in range(2)]
 bg=p.pre.background(p.m.I(F(cell['a0']),F(cell['a1'])),p.parameters(row),whole)
 if min(slack)<=0 or bg['H'].lo<=0 or bg['ede_latch'].hi>=F(1,2):raise ValueError('INDEPENDENT_BACKGROUND_CONTROL')
 return {'gate':'PASS','halving':10 if case=='camspec-ede_n3' else 11,'closure_slack':list(map(str,slack)),
         'source_guard':p.pairs(bg['ede_latch']),'positive_H':True,'series':info,'alltime_series':infoN}

def thermal_control():
 case='hillipop-ede_n3';settings=e.load(e.ROOT/'q048_resume_config_v4.json');r,_,_=e.parent_from_asset(case,settings)
 row=e.load(e.ROOT/'q048_prefix_config_v1.json')['cases'][case];t=p.parameters(row)
 now=F(r['thermal']['certified_end_a']);current=[p.old.interval(v) for v in r['thermal']['endpoint']]
 x=e.load(e.ROOT/'q048_resume_control_fixture_v4.json')['thermal']
 boundaries=[1/(1-p.point(s['mz']).lo) for s in row['thermal_starts'][1:5]];j=sum(now>=v for v in boundaries);mode=p.pre.MODES[j]
 cover=next(c for c in r['background']['cells'] if F(c['a0'])<=now<F(c['a1']))
 a1=min(boundaries[j],now*F(5,4),F(cover['a1']));width=a1-now;mid=now+width/2
 getbg=lambda a:e.background_at(a,t,r['background'],cover)
 field=lambda xi,y:[p.pre.thermal(mode,now+width*xi,y[0],t,getbg(now+width*xi))['rate']*width/(now+width*xi)]
 center=(1/(1+p.pre.thermal(mode,p.m.I(mid),p.m.I(0),t,getbg(p.m.I(mid)))['beta'])).lo
 candidate={'t0':'0','t1':'1','predictor':[[str(center)]],'box':[['-1/500000','1/50']]}
 proof=p.certify(candidate,current,field)
 if str(now)!=x['a0'] or str(a1)!=x['a1'] or mode!=x['mode'] or candidate!=x['cell'] or proof!=x['diagnostic']['proof'] or not proof['closed']:raise ValueError('CONTROL_THERMAL_PROOF')
 info=e.thermal_guard(candidate,current,field,mode,t,now,a1,getbg,proof,e.comparison.THERMAL_METHOD)
 R,slack=e.comparison.check_thermal_supersolution(candidate,current,field)
 if slack<=0:raise ValueError('INDEPENDENT_THERMAL_CONTROL')
 return {'gate':'PASS','independent_slack':str(slack),'independent_bound':str(R),'positive_temperature':info['Tmat'].lo>0,
         'mode':mode,'background_coverage':'PASS','unchanged_initial_error':proof['initial_error']}

def controls():
 return {'q':e.Q,'program_id':e.ID,'schema':'Q048_RESUME_CONTROLS_V4','scope':'CONDITIONAL_SOURCE_REAL_SINGLE_CELL_CONTROLS',
         'background':{case:independent_background(case) for case in ('camspec-ede_n3','hillipop-ede_n3')},
         'thermal':thermal_control(),'finite_controls_gate':'PASS','final_result_gate':'UNRESOLVED'}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',default='q048_resume_controls_v4.json');a=parser.parse_args()
 r=controls();p.old.write(a.out,r);print(json.dumps({'finite_controls_gate':r['finite_controls_gate'],'final_result_gate':r['final_result_gate']}))
