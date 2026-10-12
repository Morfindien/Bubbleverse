"""Three pinned k11 controls with independent finite comparison checks.
Series functions reused from q048_independent_controls_v1.py, SHA256
9b876d03c28a67917191ac5320a381a18010f38ff27a93817dbdb2547a9e093f.
Full root-to-endpoint chain admission is performed in each V3 case job.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,json
import q048_resume_v3 as e
p=e.p;m=p.m;old=p.old

def identity(n):return [[m.I(int(i==j)) for j in range(n)] for i in range(n)]

def multiply(A,B):
 return [[sum((A[i][k]*B[k][j] for k in range(len(A))),m.I(0)) for j in range(len(A))] for i in range(len(A))]

def series_exponential(A,h,terms=200):
 n=len(A);sigma=max(F(0),max(-A[i][i] for i in range(n)))
 K=[[h*(A[i][j]+(sigma if i==j else 0)) for j in range(n)] for i in range(n)]
 if min(v for row in K for v in row)<0:raise ValueError('NONNEGATIVE_GENERATOR')
 rho=max(sum(row) for row in K)
 if rho>51:raise ValueError('SERIES_WORK_DOMAIN')
 S=identity(n);T=identity(n);kI=[[m.I(v) for v in row] for row in K]
 for k in range(1,terms+1):
  P=multiply(T,kI);T=[[v/k for v in row] for row in P]
  S=[[S[i][j]+T[i][j] for j in range(n)] for i in range(n)]
 # ||K^k/k!||_infty <= rho^k/k!, bounded geometric tail after terms.
 term=F(1)
 for k in range(1,terms+2):term*=rho/k
 tail=term/(1-rho/F(terms+2));factor=m.exp_i(m.I(-sigma*h))
 R=[[factor*(v+m.I(0,tail)) for v in row] for row in S]
 return R,{'terms':terms,'row_norm':str(rho),'tail_upper':str(m.up(tail)),'shift':str(sigma)}

def independent_vector(M,r0,delta):
 A=[[F(0) for j in range(4)] for i in range(4)]
 for i in range(2):
  for j in range(2):A[i][j]=M[i][j]
  A[i][i+2]=1
 R,info=series_exponential(A,F(1))
 E=[[R[i][j] for j in range(2)] for i in range(2)];J=[[R[i][j+2] for j in range(2)] for i in range(2)]
 end=[sum((E[i][j]*r0[j]+J[i][j]*delta[j] for j in range(2)),m.I(0)) for i in range(2)]
 sigma=max(F(0),-min(M[0][0],M[1][1]));N=[[M[i][j]+(sigma if i==j else 0) for j in range(2)] for i in range(2)]
 RN,infoN=series_exponential(N,F(1))
 bound=[sum((RN[i][j]*(r0[j]+delta[j]) for j in range(2)),m.I(0)) for i in range(2)]
 return end,bound,info,infoN

def validate():
    settings=e.load(e.ROOT/'q048_resume_config_v3.json')
    cfg=e.load(e.ROOT/settings['source_config_file']);out={}
    small=dict(settings,max_new_cells_per_stage=1,background_seconds=30,thermal_seconds=30)
    for case in ('camspec-ede_n3','hillipop-ede_n3'):
        r,meta,parenthash=e.parent_from_asset(case,settings)
        t=p.parameters(cfg['cases'][case]);now,y=e.cursor(r['background']);n=len(r['background']['cells'])
        e.continue_background(r,t,small,lambda stage:None)
        if len(r['background']['cells'])!=n+1:raise ValueError('K11_BACKGROUND_REQUIRED '+case)
        cell=r['background']['cells'][-1];proof=cell['certificate']
        if F(cell['a1'])-now!=now/F(8192):raise ValueError('K11_STEP_IDENTITY')
        e.verify_background_cell(cell,now,y,t)
        M=[[F(v) for v in row] for row in proof['comparison']]
        r0=list(map(F,proof['initial_error']));delta=list(map(F,proof['defect_upper']))
        end,bound,info,infoN=independent_vector(M,r0,delta)
        pr=[old.poly_range(list(map(F,row))) for row in cell['predictor']];box=[old.interval(v) for v in cell['box']]
        slack=[min(pr[i].lo-bound[i].hi-box[i].lo,box[i].hi-pr[i].hi-bound[i].hi) for i in range(2)]
        original=[old.interval(v) for v in proof['endpoint_error']]
        overlap=[max(end[i].lo,original[i].lo)<=min(end[i].hi,original[i].hi) for i in range(2)]
        if not all(v>0 for v in slack) or not all(overlap):raise ValueError('INDEPENDENT_BACKGROUND_CONTROL')
        if old.interval(cell['forcing']['H']).lo<=0 or old.interval(cell['forcing']['ede_latch']).hi>=F(1,2):raise ValueError('SOURCE_GUARD')
        out[case]={'parent_checkpoint_sha256':parenthash,'halving':11,'cell':cell,
            'independent':{'series':info,'alltime_series':infoN,'closure_slack':list(map(str,slack)),
                           'endpoint_error':list(map(old.pairs,end)),'overlap':overlap},'gate':'PASS_CONDITIONAL_LOCAL_CELL'}
    case='hillipop-ede_n3';r,_,parenthash=e.parent_from_asset(case,settings)
    row=cfg['cases'][case];t=p.parameters(row);now=F(r['thermal']['certified_end_a'])
    y=[old.interval(v) for v in r['thermal']['endpoint']];n=len(r['thermal']['cells'])
    e.continue_thermal(r,row,t,small,(now,y),lambda stage:None)
    if len(r['thermal']['cells'])!=n+1:raise ValueError('K11_THERMAL_REQUIRED')
    cell=r['thermal']['cells'][-1];pr=cell['certificate']
    L=F(pr['comparison'][0][0]);r0=F(pr['initial_error'][0]);delta=F(pr['defect_upper'][0]);lam=-L
    if not 0<lam<1:raise ValueError('INDEPENDENT_SCALAR_DOMAIN')
    equilibrium=delta/lam;upper=r0+max(F(0),equilibrium-r0)*lam
    pred=F(cell['predictor'][0][0]);lo,hi=map(F,cell['box'][0]);slack=min(pred-upper-lo,hi-pred-upper)
    if slack<=0 or old.interval(cell['Tmat_K']).lo<=0:raise ValueError('INDEPENDENT_THERMAL_CONTROL')
    out['hillipop_thermal']={'parent_checkpoint_sha256':parenthash,'halving':11,'cell':cell,
        'independent':{'method':'exp(-x)>=1-x','closure_slack':str(slack),'alltime_upper':str(upper)},
        'gate':'PASS_CONDITIONAL_LOCAL_CELL'}
    # Exact zero and nilpotent limits of exp(M) and its integral.
    for name,M,E,J in [('zero',[[F(0),F(0)],[F(0),F(0)]],[[1,0],[0,1]],[[1,0],[0,1]]),
                       ('nilpotent',[[F(0),F(1)],[F(0),F(0)]],[[1,1],[0,1]],[[1,F(1,2)],[0,1]])]:
        A=[[F(0) for j in range(4)] for i in range(4)]
        for i in range(2):
            for j in range(2):A[i][j]=M[i][j]
            A[i][i+2]=1
        R,info=series_exponential(A,F(1))
        for i in range(2):
            for j in range(2):
                if not R[i][j].lo<=E[i][j]<=R[i][j].hi or not R[i][j+2].lo<=J[i][j]<=R[i][j+2].hi:
                    raise ValueError('ANALYTIC_LIMIT '+name)
        out[name+'_limit']={'gate':'PASS','series':info}
    return {'schema':'Q048_RESUME_CONTROLS_V3','q':e.Q,'program_id':e.ID,'source_commit':e.SOURCE,
            'scope':'CONDITIONAL_SOURCE_REAL_LOCAL_CELLS','controls_gate':'PASS',
            'final_result_gate':'UNRESOLVED','controls':out}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',default='q048_resume_controls_v3.json');args=a.parse_args()
    result=validate();old.write(args.out,result)
    print(json.dumps({'controls_gate':result['controls_gate'],'final_result_gate':result['final_result_gate']}))
