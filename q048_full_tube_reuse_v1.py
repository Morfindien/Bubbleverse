"""Q048 corrected constructor: reuse admitted background, build H/frec tubes.
No older weaker sufficient guard may override a compatible retained PASS.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import hashlib,json,time,sys,argparse
import q048_post_event_state_tube_v1 as d
m=d.m;prefix=d.prefix
import q048_p3_scaled_kernel_v2 as k
HERE=Path(__file__).resolve().parent

def inherited_guard_available(record,lo,hi):
    return bool(record['pass_to_exact_frec_boundary'] and F(0)<lo<=hi<=F(1,1601))

def hydrogen_barrier_term(alpha,alpha_eq,s,h,q):
    return alpha*h*(h+q)-alpha_eq*s*(1-h)

def fromk(x):return m.I(x.lo,x.hi)

def centered_local_log(values,norm):
    lo=min(v.lo for v in values);hi=max(v.hi for v in values);center=(lo+hi)/2;radius=(hi-lo)/2
    return k.I(center-norm*radius,center+norm*radius)

def local_atomic(alpha,rr,TR,ratio):
    # Reuse P3's proved sum(weights)=1, 1D l1<=2 and tensor l1<=4.
    # Apply them to the actual four-node/local tensor stencil, not all tables.
    answers=[]
    for reference in ['decimal','binary64']:
        u,v,channels=k.rate_coordinates(k.I(TR.lo,TR.hi),k.I(ratio.lo,ratio.hi),reference)
        us=k.split_coordinate(u,100);vs=k.split_coordinate(v,40)
        eq=[];aa=[]
        for l in range(2):
            eq.append(k.hull([k.exp_i(centered_local_log(alpha[l][39][ix-1:ix+3],F(2))) for ix,_ in us]))
            boxes=[]
            for ch in channels:
                for iy,_ in vs:
                    for ix,_ in us:
                        nodes=[alpha[l+ch][iy-1+j][ix-1+i] for j in range(4) for i in range(4)]
                        boxes.append(k.exp_i(centered_local_log(nodes,F(4))))
            aa.append(k.hull(boxes))
        rt=k.hull([k.exp_i(centered_local_log(rr[ix-1:ix+3],F(2))) for ix,_ in us])
        answers.append({'Alpha':aa,'Alpha_eq':eq,'R2p2s':rt})
    return {'Alpha':[k.hull([o['Alpha'][l] for o in answers]) for l in range(2)],'Alpha_eq':[k.hull([o['Alpha_eq'][l] for o in answers]) for l in range(2)],'R2p2s':k.hull([o['R2p2s'] for o in answers])}

def load_atomic(path):
    x=json.loads(path.read_text())
    def nodes(name):
        item=x[name];scale=1<<item['log_scale_bits']
        return [k.I(F(int(v[0]),scale),F(int(v[1]),scale)) for v in item['log_bounds_integer']]
    return k.loader_alpha(nodes('Alpha_inf.dat')),nodes('R_inf.dat')

def background(a,t,energy):
    B=d.base_h2(a,t);floor=m.I(0) if t['ede'] is None else t['ede']['B']*m.const('3.968e-8')
    H=m.sqrt_i(B+(m.I(0,energy)+floor)/3)
    return B,floor,H,H*m.C['c']/m.C['Mpc']

def thermal_certificate(a,h,q,t,Hs):
    beta=8*m.C['sigma']*(t['gamma']/a**4)*m.C['rhoJ']/(3*m.C['me']*m.C['c']*Hs)*(h+q)/(1+t['fHe']+h+q)
    faces=d.thermal_faces(beta.lo,beta.hi,F(-1,1000000),F(1,100))
    return {'beta':beta,'faces':faces,'thermal_denominator':1+t['fHe']+h+q}

def run(spec):
    ts=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
    for path,record in spec['inputs'].items():
        p=HERE/path;b=p.read_bytes()
        if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']:raise ValueError('INPUT_HASH:'+path)
    read=lambda n:json.loads((HERE/'sources'/n).read_text())
    ev=read('q048_h_event_payload_four_case_composition_v1.json');cap=read('q048_prefix_config_v1.json')
    p2=read('q048_p2p4_state_tube_result_v1.json');p3=read('q048_p3_scaled_raw_result_v2.json');ma=read('q048_math019_frec_boundary_result_v1.json')
    prefix.validate_config(cap);d.validate_event_identity(ev,spec['question_sha256'],spec['case_order'])
    alpha,rr=load_atomic(HERE/'sources/q048_p3_scaled_transformed_log_tables_v2.json')
    eps=F(1,1000000);af=F(1,1601);Hrows=[];Frows=[];block=None
    hbar=m.I(F(spec['h_barrier'][0]),F(spec['h_barrier'][1]));wbar=m.I(F(-1,1000000),F(1,100))
    for name in spec['case_order']:
        t=prefix.parameters(cap['cases'][name]);packet=ev['cases'][name];a0=F(packet['event_state']['a']['lo']);a=m.I(a0,af)
        energy,_=d.raw_energy(packet);B,floor,H,Hs=background(a,t,energy)
        if not inherited_guard_available(p2['cases'][name]['H_to_frec_background_guard'],a.lo,a.hi):raise ValueError('H_GUARD_REUSE_NOT_APPLICABLE')
        row={'case':name,'a':a,'mode':'H','shared_source_event':True,'G_admission':'REUSE_ADMITTED_P2P4_MATH015_016_017_THROUGH_FREC','branches':{}}
        for label,q in [('L',eps),('R',F(0))]:
            beta,dom=d.beta_for(a,wbar,q,t,Hs);tc=thermal_certificate(a,dom['h'],q,t,Hs)
            hh,_,_=m.hydrogen(m.I(q),wbar,m.I(1600),t['T0'],t['nH0'])
            if not tc['faces']['admitted'] or not hbar.lo<hh.lo<=hh.hi<hbar.hi:raise ValueError('H_THERMAL_OR_FREC_INITIALIZATION')
            row['branches'][label]={'q':q,'whole_H_domain':dom,'thermal':tc,'frec_initial_h':hh,'frec_initial_w':wbar,'correlation':'w_L/R are the two source flows from the SAME w_e,a_e and common background; intervals are projections, not new independent initials.'}
        row['status']='PASS_POST_EVENT_H_TO_EXACT_FREC_ENTRY';Hrows.append(row)
    # Frozen new frec stage: invariance barriers, not sample trajectories.
    for name in spec['case_order']:
        t=prefix.parameters(cap['cases'][name]);energy=min(d.anchor_caps(ma,name),default=F(0))
        for z_hi,z_lo in zip(spec['redshift_boundaries'],spec['redshift_boundaries'][1:]):
            if time.monotonic()-clock>spec['kernel_seconds_cap']:raise TimeoutError('FROZEN_WORK_CAP')
            a=m.I(F(1,z_hi+1),F(1,z_lo+1));B,floor,H,Hs=background(a,t,energy)
            G=d.guard_lower(B.lo,energy,floor.lo)
            row={'case':name,'mode':'frec','z':[z_hi,z_lo],'a':a,'B0':B,'energy_upper':energy,'floor':floor,'G_lower':G,'h_barrier':hbar,'w_barrier':wbar,'branches':{},'correlation':'Both q-constant IVPs inherit the linked H/frec map from the same event family; component boxes are invariant proof domains, not independent restarts.'}
            if t['ede'] is not None and G<=0:
                row['status']='UNRESOLVED_NEW_POST_FREC_GUARD_BOUND';Frows.append(row)
                block={'code':'POST_FREC_GUARD_MARGIN_NOT_SEPARATED_BEYOND_RETAINED_EXTENSION','cell':row,'inequality':'3*B0_lower-E_boundary_upper+floor_lower>0','margin':G,'scope':'New cell strictly beyond MATH019 z=1599 endpoint; no retained compatible PASS covers it. A failed sufficient estimate is not a physical crossing.'};break
            TR=m.const('8.617343e-5')*t['T0']/a;ratio=1-wbar
            atoms=local_atomic(alpha,rr,TR,ratio) if spec.get('centered_local_stencils') else k.interpolate_atomic(alpha,rr,k.I(TR.lo,TR.hi),k.I(ratio.lo,ratio.hi))
            A=list(map(fromk,atoms['Alpha']));Ae=list(map(fromk,atoms['Alpha_eq']));R=fromk(atoms['R2p2s'])
            n=t['nH0']/a**3*m.const('1e-6')
            sH=m.const('3.016103031869581e21')*TR*m.sqrt_i(TR)*m.exp_i(-m.const('13.598286071938324')/TR)/n
            fit=d.interval(p3['fit_cases'][name]['primary_denominator'])
            domain={'TR_eV':TR,'Tgamma_K':t['T0']/a,'TM_over_TR':ratio,'fit_denominator':fit,'Alpha':A,'Alpha_eq':Ae,'R2p2s':R,'Saha_HyRec':sH,'active_branch':'SWIFT; z>900, TR>.004, ratio>.1, fit-temperature>1775 and <4415','positive_C_denominator_identity':'(Beta0+L)*(Beta1+R+RL)+3*R*(Beta1+RL)>0; all factors strictly positive'}
            if not F('.004')<TR.lo<=TR.hi<F('.4') or ratio.lo<=F('.1') or fit.lo<=0 or min(v.lo for v in A+Ae+[R,sH])<=0:raise ValueError('FREC_SOURCE_DOMAIN')
            row['operator']=domain
            for label,q in [('L',eps),('R',F(0))]:
                terms_lo=[hydrogen_barrier_term(A[l],Ae[l],sH,m.I(hbar.lo),q) for l in range(2)]
                terms_hi=[hydrogen_barrier_term(A[l],Ae[l],sH,m.I(hbar.hi),q) for l in range(2)]
                tc=thermal_certificate(a,hbar,q,t,Hs)
                ok=all(v.hi<0 for v in terms_lo) and all(v.lo>0 for v in terms_hi) and tc['faces']['admitted']
                row['branches'][label]={'q':q,'hydrogen_low_face_terms':terms_lo,'hydrogen_high_face_terms':terms_hi,'thermal':tc,'admitted':ok}
                if not ok:
                    row['status']='UNRESOLVED_FREC_INVARIANT_FACE';block={'code':'POST_FREC_SOURCE_RATE_INVARIANT_FACE_NOT_SEPARATED','cell':row,'branch':label,'scope':'New exact actual-rate barrier test; method failure only, not source trajectory escape.'};break
            if block:Frows.append(row);break
            row['status']='PASS_PAIRED_FREC_INVARIANT_TUBE';Frows.append(row)
        if block:break
    return d.encode({'schema':'Q048_REUSE_CORRECTED_STATE_TUBE_RESULT','revision':spec.get('revision',3),'q':'Q048','target_q':'Q048','exact_question':cap['scientific_question'],'question_sha256':cap['question_sha256'],'source_commit':cap['source_commit'],'task_id':spec['task_id'],'result_id':'LOCAL-Q048-POST-EVENT-FREC-STATE-TUBE-CONSTRUCTION-V'+str(spec.get('revision',3)),'status':'BLOCKED_EXACT_NEW_CELL_OBLIGATION' if block else 'PASS_FROZEN_FREC_INTERVAL_ONLY','start_utc':ts,'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-clock,'H_to_frec':Hrows,'frec_cells':Frows,'blocker':block,'supersedes_active_blocker':'The V1/V2 local-H loose G obstruction is bypassed by already admitted P2P4/Math015-017 common-background guards. Its outer-set arithmetic remains historical, not an active new premise.','all_four_event_packets_unchanged':True,'complete_a1_certificate':False,'final_delta_xe_bounds_computed':False,'final_delta_tau_bounds_computed':False,'native_P6':'UNRESOLVED','q_complete':False,'physical_falsification':False,'return_route':'RESULT INGESTION & ROUTING ENGINE 2.0.0'})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--spec',required=True);a.add_argument('--output',required=True);p=a.parse_args()
    x=run(json.loads(Path(p.spec).read_text()));Path(p.output).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps({'status':x['status'],'seconds':x['elapsed_seconds'],'H_cases':len(x['H_to_frec']),'frec_passed':sum(c['status'].startswith('PASS') for c in x['frec_cells']),'blocker':x['blocker']['code'] if x['blocker'] else None,'cell':x['blocker']['cell']['z'] if x['blocker'] else None}))
