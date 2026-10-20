"""Fresh Q048 proof910->900. Historical helper bytes are read-only.
No actual consumer, native evolution or old scientific main is invoked.
"""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib, sys, argparse

SAHA_FACTOR='3.016103031869581e21'  # pinned hydrogen.c SAHA_FACT at source commit5a131c91

def source_boundary_certificate(a0,a1,inputs,model=4):
    a0,a1=F(a0),F(a1);inputs=Path(inputs)
    c=(inputs/'source/hydrogen.c').read_bytes();h=(inputs/'source/hydrogen.h').read_bytes()
    ch=hashlib.sha256(c).hexdigest();hh=hashlib.sha256(h).hexdigest()
    if ch!='734800ccd69b41d60b519f200003ce27c3b7640f76a70353499424842ba19616' or hh!='1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52':raise ValueError('SOURCE_BOUNDARY_BYTE_PIN')
    dispatch=c.decode().split('double rec_dxHIIdlna(',1)[1]
    if not ('Pion = 1.;' in dispatch and 'if (z < 900.)' in dispatch and '#define PION_MAX  1e-2' in h.decode() and '#define SWIFT     4' in h.decode()):raise ValueError('SOURCE_BOUNDARY_DISPATCH')
    if not (model==4 and 0<a0<=a1 and F(1)/a1-1>=900):raise ValueError('SOURCE_BOUNDARY_DOMAIN')
    return {'z_min':str(F(1)/a1-1),'z_max':str(F(1)/a0-1),'low_z_branch_active_anywhere':False,'Pion':'1','PION_MAX':'1/100','dispatch':'SWIFT_FIT_SUBJECT_TO_OTHER_DOMAIN_GATES','boundary':'z>=900','hydrogen_c_sha256':ch,'hydrogen_h_sha256':hh}


def ceil18(x):
    x=F(x);return F(-((-x.numerator*10**18)//x.denominator),10**18)
def floor18(x):
    x=F(x);return F(x.numerator*10**18//x.denominator,10**18)
def rational_lower(K,eps,du,h0):
    K,eps,du,h0=map(F,(K,eps,du,h0));x=K*eps*du
    if K<=0 or eps<0 or du<0 or h0<=0 or x>=1:raise ValueError('RICCATI_DOMAIN')
    if eps==0:return h0/(1+K*h0*du)
    return eps/((1+eps/h0)/(1-x)-1) if du else h0

def validate_binding(parent,task,guard):
    if parent.get('status')!='VALIDATED' or parent.get('correct_saha_fact')!='3.016103031869581e21':raise ValueError('PARENT_SOURCE_QUALIFICATION')
    if parent['q']!='Q048' or parent['target_q']!='Q048' or task['current_q']!='Q048' or task['target_q']!='Q048':raise ValueError('Q_IDENTITY')
    if parent['accepted_actual']!={'count':117,'frontier':910} or task['parent_authority']['accepted_actual']!=parent['accepted_actual']:raise ValueError('PARENT_IDENTITY')
    if task['cell_z']!=[910,900] or task['cell_a']!=['1/911','1/901']:raise ValueError('CELL_IDENTITY')
    if guard['evaluators'][0]['control'] is not False or guard['evaluators'][1]['control'] is not True:raise ValueError('PRIMARY_CONTROL_ROLE')
    rows=[]
    for evaluator in guard['evaluators']:
        candidates=[r for r in evaluator['rows'] if r['index']==54]
        if len(candidates)!=1:raise ValueError('ROW54_IDENTITY')
        r=candidates[0]
        if [r['z0'],r['z1']]!=[910,900] or [r['a0'],r['a1']]!=['1/911','1/901']:raise ValueError('CELL_ROW')
        if r['source_state_reset'] is not False:raise ValueError('STATE_RESET')
        if not all(r[k] for k in ['accepted','committed','whole_cell_qualified']) or not r['domain']['admitted'] or not all(r['domain']['checks'].values()):raise ValueError('ROW_DOMAIN')
        rows.append(r)
    p=rows[0]
    for a,b in [('E_input_left','E'),('Y_left','Y'),('V_previous','Vbar')]:
        if F(p[a])!=F(parent['endpoint'][b]) or F(parent['endpoint'][b])!=F(task['parent_authority']['endpoint'][b]):raise ValueError('EXACT_GLUE_'+b)
    if parent['endpoint']['a']!='1/911':raise ValueError('PARENT_A')
    return rows

def load_environment(root):
    path=str(Path(root)/'inputs')
    if path not in sys.path:sys.path.insert(0,path)
    import q048_full_tube_reuse_v1 as old
    return old

def produce(root,spec):
    root=Path(root);I=root/'inputs';old=load_environment(root);m,d,k,prefix=old.m,old.d,old.k,old.prefix
    read=lambda name:json.loads((I/name).read_text())
    parent=read('Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json');task=read('Q048_V120_NEXT_MATHEMATICS_TASK_V1.json');guard=read('q048_guard_local_v_result_v12.json')
    primary,control=validate_binding(parent,task,guard)
    parent_hash=hashlib.sha256((I/'Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json').read_bytes()).hexdigest()
    if parent_hash!=task['parent_authority']['sha256']:raise ValueError('PARENT_BYTE_IDENTITY')
    if spec['cell_z']!=[910,900] or spec['thermal_domain']!=['-1/1000000','1/50']:raise ValueError('FROZEN_DOMAIN')
    cap=read('q048_prefix_config_v1.json');prefix.validate_config(cap)
    if cap['question_sha256']!=task['question_sha256']:raise ValueError('QUESTION_CAPTURE')
    case=cap['cases']['hillipop-ede_n3'];t=prefix.parameters(case)
    a=m.I(F(1,911),F(1,901));w=m.I(F(-1,10**6),F(1,50));eps=F(1,10**6);h0=F(parent['connected_lower']);hmax=F(99999,100000)
    B,floor,H,Hs=old.background(a,t,F(primary['E_safe_left']));HsK=m.sqrt_i(m.I(B.lo))*m.C['c']/m.C['Mpc']
    TR=m.const('8.617343e-5')*t['T0']/a;Tgamma=t['T0']/a;ratio=1-w
    p3=read('q048_p3_scaled_raw_result_v2.json');fit=d.interval(p3['fit_cases']['hillipop-ede_n3']['primary_denominator'])
    out={'schema':'bubbleverse.q048.moving_h.domain.proof.v120','q':'Q048','target_q':'Q048','task_id':spec['task_id'],'question_sha256':task['question_sha256'],'cell_z':[910,900],'cell_a':['1/911','1/901'],'parent_checkpoint_sha256':parent_hash,'task_fingerprint':task['task_fingerprint'],'parent_actual':parent['accepted_actual'],'actual_state_unchanged':parent['accepted_actual'],'guard_primary_index':54,'source_state_reset':False,'guard_primary_E_safe_left':primary['E_safe_left'],'thermal_domain':['-1/1000000','1/50'],'saha_factor_source':SAHA_FACTOR,'source_correction':'V120_NEW_SOURCE_CORRECT_PROOF_ON_V119; historical V101/V102 unchanged; no old execution identity transferred','epsilon':eps,'h0':h0,'hmax':hmax,'a':a,'B':B,'floor':floor,'H':H,'Hs':Hs,'HsK':HsK,'TR_eV':TR,'Tgamma_K':Tgamma,'ratio':ratio,'fit':fit,'branches':{},'new_actual_cells':0,'new_mathematical_proof_cells':0,'scientific_state':'INCONCLUSIVE','status':'PENDING_VALIDATION','no_native_trajectory_claim':True}
    def gate(name,passed,margin=None):
        if not passed:
            out['status']='FIRST_OBSTRUCTION';out['obstruction']={'gate':name,'signed_margin':margin};return False
        return True
    source={'model4':all(z['HyRec_MODEL']==4 for z in case['thermal_starts']),'fixed_flags':all(case['background']['thermal_flags'][z]==0 for z in ['has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr']),'z_ge900':F(1)/a.hi-1>=900,'TR':F('.004')<TR.lo<=TR.hi<F('.4'),'Tgamma':1775<Tgamma.lo<=Tgamma.hi<4415,'ratio':ratio.lo>F('.1'),'fit_positive':fit.lo>0,'H_positive':HsK.lo>0,'guard_admitted':primary['accepted'] and primary['committed'] and primary['whole_cell_qualified'] and primary['domain']['admitted'] and all(primary['domain']['checks'].values())}
    out['source_boundary_certificate']=source_boundary_certificate(a.lo,a.hi,I,4)
    out['source_checks']=source
    for name,passed in source.items():
        if not gate('SOURCE:'+name,passed):return d.encode(out)
    out['source_all']=True
    alpha,rr=old.load_atomic(I/'q048_p3_scaled_transformed_log_tables_v2.json');atoms=old.local_atomic(alpha,rr,TR,ratio)
    A=list(map(old.fromk,atoms['Alpha']));Ae=list(map(old.fromk,atoms['Alpha_eq']));RR=old.fromk(atoms['R2p2s']);n=t['nH0']/a**3*m.const('1e-6')
    saha=m.const(SAHA_FACTOR)*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
    Beta=[Ae[i]*m.const(SAHA_FACTOR)*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/(4*TR))/(2*i+1) for i in range(2)]
    out.update(A=A,Ae=Ae,R2p2s=RR,n=n,Saha=saha,Beta=Beta)
    atom_margin=min(x.lo for x in A+Ae+[RR,n,saha]+Beta);out['atomic_positive']=atom_margin>0
    if not gate('ATOMIC_POSITIVITY',atom_margin>0,atom_margin):return d.encode(out)
    Kexact=n.hi*(A[0].hi+A[1].hi)/HsK.lo;K=ceil18(Kexact)
    du0=k.log_i(k.I(a.hi/a.lo));du=m.I(du0.lo,du0.hi)
    endpoint=eps/((1+eps/h0)*m.exp_i(K*eps*du)-1)
    control_lower=rational_lower(K,eps,a.hi/a.lo-1,h0);hmin=floor18(min(endpoint.lo,control_lower));h=m.I(hmin,hmax)
    out.update(K_unrounded=Kexact,K_upper=K,du=du,du_rational_upper=a.hi/a.lo-1,endpoint_primary=endpoint,endpoint_control=control_lower,hmin=hmin)
    if not gate('CONNECTED_LOWER',hmin>0,hmin):return d.encode(out)
    L0=m.const('8.2206');P=m.const('4.662899067555897e15')*Hs/n/(1-h)/fit
    gs=Beta[0]+3*RR+L0;gp=Beta[1]+RR+P;D=(Beta[0]+L0)*(Beta[1]+RR+P)+3*RR*(Beta[1]+P);Ns=L0*gp+3*RR*P;Np=P*gs+RR*L0;ds=Beta[0]*gp+3*RR*Beta[1];dp=Beta[1]*gs+RR*Beta[0]
    cf={'L0':L0,'P':P,'gs':gs,'gp':gp,'D':D,'Ns':Ns,'Np':Np,'ds':ds,'dp':dp};out['C_factors']=cf;cm=min(z.lo for z in cf.values());out['c_positive']=cm>0
    if not gate('C_FACTOR_POSITIVITY',cm>0,cm):return d.encode(out)
    for label,q in [('L',eps),('R',F(0))]:
        high=[old.hydrogen_barrier_term(A[i],Ae[i],saha,m.I(hmax),q) for i in range(2)]
        thermal=old.thermal_certificate(a,h,q,t,Hs);thermal['faces']=d.thermal_faces(thermal['beta'].lo,thermal['beta'].hi,w.lo,w.hi)
        margins={'upper_h_0':high[0].lo,'upper_h_1':high[1].lo,'thermal_denominator':thermal['thermal_denominator'].lo,'beta':thermal['beta'].lo,'lower_face_inward_lower':thermal['faces']['lower_face_inward_lower'],'upper_face_inward_margin':thermal['faces']['upper_face_inward_margin']}
        out['branches'][label]={'q':q,'upper_h_face_terms':high,'thermal':thermal,'signed_margins':margins,'admitted':all(x>0 for x in margins.values())}
        for name,margin in margins.items():
            if not gate('BRANCH:'+label+':'+name,margin>0,margin):return d.encode(out)
    out['status']='CANDIDATE_PROOF';return d.encode(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--output',required=True);args=p.parse_args();sp=Path(args.spec).resolve();spec=json.loads(sp.read_text())
    for path,pin in spec['input_pins'].items():
        b=(sp.parent/path).read_bytes()
        if len(b)!=pin['bytes'] or hashlib.sha256(b).hexdigest()!=pin['sha256']:raise ValueError('INPUT_PIN:'+path)
    result=produce(sp.parent,spec);result['below900_work']=False;result['q_complete']=False;result['historical_record_modified']=False;result['correct_source_lineage']='V104_TO_V119_SOURCE_CORRECT_REASSESSMENT';
    with Path(args.output).open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'obstruction':result.get('obstruction'),'K_upper':result.get('K_upper'),'hmin':result.get('hmin')}))
