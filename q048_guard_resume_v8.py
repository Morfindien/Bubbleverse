"""Q048 Mathematics Guard Resume V8.

Extends the already-qualified Guard V6 connected scalar/Y/energy family from a=1/1501
through the Builder-V7 admitted 1500->1490 interval and certifies the new
1490->1480 target guard. It does not replay prior science or construct H/thermal cells.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform, sys, time, resource

ROOT=Path(__file__).resolve().parent
INP=ROOT/'inputs'
sys.path.insert(0,str(INP))
import q048_math015_weighted_virial_v1 as p

D=10**18

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def fs(x): return f"{x.numerator}/{x.denominator}"
def root_bisection(x, steps=112):
    assert x>=0
    if x==0: return F(0),F(0)
    lo,hi=F(0),max(F(1),x+1)
    for _ in range(steps):
        m=(lo+hi)/2
        if m*m==x: return m,m
        if m*m<x: lo=m
        else: hi=m
    assert lo*lo<=x<=hi*hi
    return lo,hi

def finite_node_base(a,b):
    assert a>0 and b['ol']==0 and b['factor']>0 and b['M']>=0
    assert len(b['q'])==len(b['w'])==11 and all(t>0 for t in b['q']+b['w'])
    rho=sum(q*q*root_bisection(q*q+(a*b['M'])**2)[0]*w for q,w in zip(b['q'],b['w']))
    return p.down(b['H0']**2*((b['og']+b['our'])/a**4+(b['ob']+b['oc'])/a**3)+b['factor']/a**4*rho)

def validate_lineage(cfg,v6,v6ck,v6val,v7,v7ck,v7val):
    assert cfg['q']==cfg['target_q']==v6['q']==v7['q']=='Q048'
    assert v6['status']=='PASS_GUARD_COMPONENT'
    assert v6val['technical_state']=='PASS' and v6val['result_sha256']==digest(INP/'q048_guard_resume_result_v6.json')
    assert v6ck['source_raw_sha256']==digest(INP/'q048_guard_resume_result_v6.json')
    assert v6ck['validation_sha256']==digest(INP/'q048_guard_resume_validation_v6.json')
    assert v7['status']=='PARTIAL_WITH_EXACT_NEW_OBSTRUCTION'
    assert v7val['technical_state']=='PASS'
    assert v7ck['source_result_sha256']==digest(INP/'q048_frec_resume_result_v7.json')
    assert v7['guard_raw_sha256']==digest(INP/'q048_guard_resume_result_v6.json')
    assert v7['guard_validation_sha256']==digest(INP/'q048_guard_resume_validation_v6.json')
    assert v7['final_frontiers']['hillipop-ede_n3']==1490
    assert v7ck['total_accepted_cells_in_chain']==cfg['retained_frec_cells']==59
    assert v7['blocker']['a']['lo']==cfg['target_a0'] and v7['blocker']['a']['hi']==cfg['target_a1']
    assert v7['blocker']['code']=='NEW_WHOLE_CELL_GUARD_NOT_SEPARATED'
    assert cfg['question_sha256']==v6['question_sha256']==v7['question_sha256']
    assert cfg['source_commit']==v6['source_commit']==v7['source_commit']
    assert cfg['capture_sha256']==v6['capture_sha256']==v7['capture_sha256']
    assert cfg['parent_math_result']==v6['result_id']
    assert cfg['parent_builder_result']==v7['result_id']
    tracks={t['control']:t for t in v6['evaluators']}
    assert set(tracks)=={False,True}
    for control,key in [(False,'primary'),(True,'control')]:
        t=tracks[control]
        assert t['status']=='PASS_TO_TARGET'
        assert t['rows'][-1]['a1']==cfg['anchor_a']
        a=cfg['anchors'][key]
        assert t['last_E']==a['E_upper'] and t['last_Y']==a['Y_upper']
        assert t['Vbar']==a['Vbar'] and t['equilibrium_upper']==a['equilibrium_upper']
    return tracks

def run():
    start=time.monotonic(); started=datetime.now(timezone.utc).isoformat()
    cfg=json.loads((ROOT/'q048_guard_resume_config_v8.json').read_text())
    for f,h in cfg['input_hashes'].items():
        assert digest(INP/f)==h, f
    v6=json.loads((INP/'q048_guard_resume_result_v6.json').read_text())
    v6ck=json.loads((INP/'q048_guard_resume_checkpoint_v6.json').read_text())
    v6val=json.loads((INP/'q048_guard_resume_validation_v6.json').read_text())
    v7=json.loads((INP/'q048_frec_resume_result_v7.json').read_text())
    v7ck=json.loads((INP/'q048_frec_resume_checkpoint_v7.json').read_text())
    v7val=json.loads((INP/'q048_frec_resume_validation_v7.json').read_text())
    states=json.loads((INP/'state_objects_extracted.json').read_text())
    validate_lineage(cfg,v6,v6ck,v6val,v7,v7ck,v7val)

    alpha,kappa,beta=[F(cfg[x]) for x in ['alpha','kappa','beta']]
    assert kappa/2-3+alpha==0
    assert kappa-alpha*F(15,4)==0
    assert beta==alpha*max(abs(kappa-6),abs(kappa-3))
    nodes=list(map(F,cfg['nodes']))
    assert nodes==[F(1,1501),F(1,1491),F(1,1481)]

    bg=p.bg('hillipop-ede_n3',states)
    src=p.source_intervals('hillipop-ede_n3',states)
    assert bg['H0']>0 and bg['ol']==0 and all(bg[k]>=0 for k in ['og','our','ob','oc'])
    assert src['Alo']>0 and src['lamlo']>0 and src['floorlo']>=0

    out={
      'schema_version':'UNVALIDATED_LOCAL_CONTRACT',
      'result_id':cfg['result_id'],'task_id':cfg['task_id'],
      'q':'Q048','target_q':'Q048','exact_question':cfg['exact_question'],
      'question_sha256':cfg['question_sha256'],'prompt_id':cfg['prompt_id'],'prompt_version':cfg['prompt_version'],
      'source_commit':cfg['source_commit'],'capture_sha256':cfg['capture_sha256'],
      'scope':'CONDITIONAL_SOURCE_REAL_GUARD_COMPONENT_ONLY',
      'parent_handoff':cfg['parent_handoff'],'parent_math_result_id':v6['result_id'],
      'parent_builder_result_id':v7['result_id'],
      'parent_math_raw_sha256':digest(INP/'q048_guard_resume_result_v6.json'),
      'parent_builder_raw_sha256':digest(INP/'q048_frec_resume_result_v7.json'),
      'config_sha256':digest(ROOT/'q048_guard_resume_config_v8.json'),
      'contract_sha256':digest(ROOT/'Q048_GUARD_RESUME_TEST_CONTRACT_V8.md'),
      'input_hashes':cfg['input_hashes'],
      'anchor_a':cfg['anchor_a'],'target_cell':[cfg['target_a0'],cfg['target_a1']],
      'resolved_builder_blocker_id':'POST_GUARD_V6_FORWARD_ENERGY_GUARD_NOT_SEPARATED_Z1490_1480',
      'equations':{
        'G':'3B0+e+floor-2U',
        'guard_sufficient':'3B0_lower(right)-E_upper(left)>0; floor>=0 and U<=e<=E_upper',
        'Y':'e+(24/23)V',
        'comparison':'Y_u+(90/23)Y<=(1152/529)Vbar',
        'energy':'E_right=min(E_left,Y_right+(24/23)Vbar)'
      },
      'units':{'a_u_theta_coefficients':'dimensionless','E_Y_V_G_B0_floor':'Mpc^-2','H_X':'Mpc^-1'},
      'evaluators':[],
      'old_science_reexecuted':False,'hydrogen_thermal_cells_new':0,
      'retained_frec_cells':59,'retained_H_to_frec_tubes':4,
      'q_complete':False,'complete_a1_certificate':False,'complete_xe_tau_bounds':False,
      'native_P6':'UNRESOLVED','accepted_model_change':False,'physical_falsification':False
    }

    for control,key in [(False,'primary'),(True,'control')]:
        anchor=cfg['anchors'][key]
        E,Y,Vbar,eq=map(F,[anchor['E_upper'],anchor['Y_upper'],anchor['Vbar'],anchor['equilibrium_upper']])
        track={
          'path':'RATIONAL_BERNOULLI_CONTROL' if control else 'EXACT_SERIES_PRIMARY',
          'control':control,'anchor_a':cfg['anchor_a'],'anchor_E':fs(E),'anchor_Y':fs(Y),
          'Vbar':fs(Vbar),'equilibrium_upper':fs(eq),
          'lineage':'Exact Guard V6 endpoint family at a=1/1501; propagated through Builder-V7 admitted 1500->1490 interval without independent state reset',
          'rows':[]
        }
        for idx,(left,right) in enumerate(zip(nodes,nodes[1:])):
            if time.monotonic()-start>cfg['max_seconds_total']:
                track['status']='BUDGET_CHECKPOINT'; break
            B=finite_node_base(right,bg) if control else p.B0_lower(right,bg)
            G=p.down(3*B-E)
            role='NEW_CONNECTED_BRIDGE' if idx==0 else 'TARGET_CELL'
            row={'index':idx,'role':role,'a0':fs(left),'a1':fs(right),
                 'z0':int(1/left-1),'z1':int(1/right-1),
                 'E_left':fs(E),'Y_left':fs(Y),'B0_lower':fs(B),'G_lower':fs(G),'accepted':G>0}
            if G<=0:
                row['status']='METHOD_INSUFFICIENT'
                track['rows'].append(row); track['status']='METHOD_INSUFFICIENT'; break
            if control:
                d=1/(1+kappa*(right-left)/right)
                Y1=p.up(eq+(Y-eq)*d) if Y>=eq else eq
                row.update(decay_upper=fs(d),decay_method='RATIONAL_BERNOULLI_LOG_LOWER',Y_above_equilibrium=Y>=eq)
            else:
                ll,lh=p.log_bounds(right/left)
                dl,dh=p.exp_minus_bounds(kappa*ll,kappa*lh)
                Y1=max(p.up(dl*Y+(1-dl)*eq),p.up(dh*Y+(1-dh)*eq))
                row.update(log_lower=fs(ll),log_upper=fs(lh),decay_lower=fs(dl),decay_upper=fs(dh),
                           decay_width=fs(dh-dl),decay_method='EXACT_SERIES_OUTWARD')
            E1=min(E,p.up(Y1+alpha*Vbar))
            assert E1<=E
            row.update(Y_right=fs(Y1),E_right=fs(E1),status='PASS_STRICT_WHOLE_CELL_GUARD')
            track['rows'].append(row); E,Y=E1,Y1
        else:
            track['status']='PASS_TO_TARGET'
        track.update(last_E=fs(E),last_Y=fs(Y))
        if track['status']=='PASS_TO_TARGET':
            track['target_G_lower']=track['rows'][-1]['G_lower']
            track['minimum_G_lower']=fs(min(F(r['G_lower']) for r in track['rows']))
        out['evaluators'].append(track)

    pass_all=all(t['status']=='PASS_TO_TARGET' for t in out['evaluators'])
    out['status']='PASS_GUARD_COMPONENT' if pass_all else 'METHOD_INSUFFICIENT_OR_CHECKPOINT'
    out['workflow_state']='READY_FOR_HANDOFF'
    out['scientific_state']='SUPPORTED_WITHIN_TESTED_DOMAIN' if pass_all else 'INCONCLUSIVE'
    out['technical_state']='PENDING_VALIDATION'
    out['interpretation']='The V7 negative constant-energy sufficient bound is superseded only as the active guard-method obstruction on z1490->1480; historical V7 output remains unchanged.'
    out['return_route']='RESULT INGESTION & ROUTING ENGINE 2.1.0'
    out['execution']={
      'run_id':'LOCAL-Q048-GUARD-RESUME-V8-'+started,'start_utc':started,
      'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,
      'python':platform.python_version(),'platform':platform.platform(),
      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'command':'python3 q048_guard_resume_v8.py','backend':'LOCAL_CPU_EXACT_RATIONAL',
      'native_or_paid_runs':0,'source_solution_integration':False,'old_science_reexecuted':False
    }
    path=ROOT/'q048_guard_resume_result_v8.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({
      'status':out['status'],
      'tracks':[{'path':t['path'],'target_G_lower':str(float(F(t.get('target_G_lower','0')))),
                 'last_E':str(float(F(t['last_E']))),'last_Y':str(float(F(t['last_Y'])))} for t in out['evaluators']],
      'run_id':out['execution']['run_id'],'elapsed':out['execution']['elapsed_seconds']
    },indent=2))

if __name__=='__main__': run()
