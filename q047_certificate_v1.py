"""Q047 source-defined upper-IVP checker. Actual cosmological admission fails closed.

All proof arithmetic is rational/outward. Conditional input bounds are assumptions;
this program cannot turn an asserted CLASS background/initial error into a proof.
There is no native CLASS, spectrum, likelihood, sampling or workflow subprocess.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, log
import argparse, hashlib, json, os, platform, sys, time
import q047_math_v1 as math

Q='Q-047';ID='Q047-CERTCHECK-V1';VERSION='v1'
SOURCE='5a131c91d657dd9a7c6364cc45b038710f8d0d97'
CASES=('camspec-lcdm','camspec-ede_n3','hillipop-lcdm','hillipop-ede_n3')
ROOT=Path(__file__).resolve().parent
EPS=F(1,1000000)

def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('DUPLICATE_JSON_KEY '+k)
        out[k]=v
    return out

def loads(text):
    if len(text)>5_000_000:raise ValueError('INPUT_SIZE_CAP')
    return json.loads(text,object_pairs_hook=unique,
        parse_constant=lambda s:(_ for _ in ()).throw(ValueError('NONFINITE_JSON '+s)))

def load(path):return loads(Path(path).read_text())

def write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    tmp.replace(path)

def rational(value):
    if isinstance(value,bool) or isinstance(value,float):raise ValueError('EXACT_INPUT_REQUIRED')
    if not isinstance(value,(str,int,F)):raise ValueError('INVALID_RATIONAL')
    if isinstance(value,str) and len(value)>1000:raise ValueError('RATIONAL_SIZE_CAP')
    result=F(value)
    if abs(result)>10**100:raise ValueError('RATIONAL_MAGNITUDE_CAP')
    return result

def interval(pair):
    if not isinstance(pair,list) or len(pair)!=2:raise ValueError('INTERVAL_SHAPE')
    lo,hi=map(rational,pair)
    if lo>hi:raise ValueError('INTERVAL_ORDER')
    return math.I(lo,hi)

def pairs(x):return [str(x.lo),str(x.hi)]

def nonnegative(x):
    if x.hi<0:raise ValueError('POSITIVE_MATRIX_ENCLOSURE')
    return math.I(max(F(0),x.lo),x.hi)

def exponential_integral(rate,h):
    """Integral exp(rate*s), including the continuous zero limit."""
    rate=math.iv(rate)
    if rate.lo==rate.hi==0:return math.I(h)
    if not rate.lo<=0<=rate.hi:
        return nonnegative((math.exp_i(rate*h)-1)/rate)
    return math.I(h)*math.exp_i(math.I(min(F(0),rate.lo*h),max(F(0),rate.hi*h)))

def comparison_matrices(M,h):
    """Enclose exp(Mh) and integral exp(Ms) for a constant 2x2 Metzler M."""
    a,b=M[0];c,d=M[1];h=rational(h)
    if h<0 or b<0 or c<0:raise ValueError('METZLER_OR_TIME_DOMAIN')
    if max(a+b,c+d,F(0))*h>50:raise ValueError('COMPARISON_GROWTH_CAP')
    zero=math.I(0)
    if b==c==0:
        return ([[math.exp_i(math.I(a)*h),zero],[zero,math.exp_i(math.I(d)*h)]],
                [[exponential_integral(math.I(a),h),zero],[zero,exponential_integral(math.I(d),h)]])
    disc=(a-d)**2+4*b*c
    if disc==0:
        # a=d and bc=0: M=aI+N, N^2=0. Exact continuous eigenvalue limit.
        e=math.exp_i(math.I(a)*h);j=exponential_integral(math.I(a),h)
        k=math.I(h*h/2) if a==0 else nonnegative(((math.I(a*h)-1)*e+1)/(a*a))
        return [[e,b*h*e],[c*h*e,e]],[[j,b*k],[c*k,j]]
    gap=math.sqrt_i(math.I(disc))
    if gap.lo<=0:raise ValueError('EIGENVALUE_GAP_NOT_SEPARATED')
    lp=(math.I(a+d)+gap)/2;lm=(math.I(a+d)-gap)/2
    def matrix(vp,vm):
        return [[nonnegative(((a-lm)*vp+(lp-a)*vm)/gap),nonnegative(b*(vp-vm)/gap)],
                [nonnegative(c*(vp-vm)/gap),nonnegative(((d-lm)*vp+(lp-d)*vm)/gap)]]
    return matrix(math.exp_i(lp*h),math.exp_i(lm*h)),matrix(exponential_integral(lp,h),exponential_integral(lm,h))

def poly_at(coeffs,x):
    answer=F(0)
    for a in reversed(coeffs):answer=answer*x+a
    return answer

def poly_range(coeffs):
    """Power-to-Bernstein convex-hull enclosure on xi in [0,1]."""
    if not 1<=len(coeffs)<=7:raise ValueError('POLYNOMIAL_DEGREE_CAP')
    n=len(coeffs)-1
    controls=[sum((coeffs[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)),F(0)) for i in range(n+1)]
    return math.I(min(controls),max(controls))

def field(q,w,t,T0,n0,f,H,gamma0):
    z=2871*math.exp_i(-t)-1
    rho=gamma0*(1+z)**4
    Qrate,Grate,extra=math.flow(q,w,z,T0,n0,f,H,rho)
    return Qrate,Grate,extra,z

def check_upper_packet(packet):
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    if packet.get('actual_reference_qualified'):raise ValueError('UNSUPPORTED_ACTUAL_QUALIFICATION')
    if packet.get('schema')!='Q047-UPPER-PACKET-V1' or packet.get('q')!=Q:raise ValueError('Q_OR_SCHEMA')
    if packet.get('case_id') not in CASES:raise ValueError('CASE_ID')
    if packet.get('source_commit')!=SOURCE:raise ValueError('SOURCE_COMMIT')
    if packet.get('scope')!='CONDITIONAL_LOCAL_UPPER_IVP':raise ValueError('UNSUPPORTED_SCOPE')
    par=packet['parameters'];T0=interval(par['T0']);n0=interval(par['nH0']);f=interval(par['fHe']);gamma=interval(par['gamma0'])
    if min(T0.lo,n0.lo,f.lo,gamma.lo)<=0:raise ValueError('PARAMETER_DOMAIN')
    initial=[interval(v) for v in packet['initial_state']]
    segments=packet['segments']
    if not 1<=len(segments)<=128:raise ValueError('SEGMENT_COUNT_CAP')
    # Validate the entire partition before evaluating any candidate verdict.
    last=None;last_p=None
    for s in segments:
        t0,t1=rational(s['t0']),rational(s['t1'])
        coeff=[[rational(a) for a in row] for row in s['predictor']]
        if len(coeff)!=2 or any(not 1<=len(r)<=7 for r in coeff):raise ValueError('PREDICTOR_SHAPE')
        if t0<0 or t1<=t0 or (last is not None and t0!=last):raise ValueError('PARTITION_GAP_OR_ORDER')
        if last_p is not None and [poly_at(c,F(0)) for c in coeff]!=last_p:raise ValueError('PREDICTOR_DISCONTINUITY')
        last=t1;last_p=[poly_at(c,F(1)) for c in coeff]
    report=dict(q=Q,program_id=ID,case_id=packet['case_id'],scope=packet['scope'],
        input_semantics='Assumed initial-state and continuous background/forcing bounds; no CLASS-continuum qualification',
        conditional_event_gate='UNRESOLVED',final_result_gate='UNRESOLVED',actual_applicability='INSUFFICIENT_EVIDENCE',segments=[])
    previous_radius=None;prefix_separated=True;left_above=False
    for index,s in enumerate(segments):
        t0,t1=rational(s['t0']),rational(s['t1']);h=t1-t0
        coeff=[[rational(a) for a in row] for row in s['predictor']]
        p=[poly_range(c) for c in coeff]
        domain=[interval(v) for v in s['domain']];B=[rational(v) for v in s['radius_budget']]
        if len(domain)!=2 or len(B)!=2 or min(B)<=0:raise ValueError('TUBE_SHAPE')
        if domain[0].lo<=0 or domain[0].hi>=f.lo or domain[1].lo<0 or domain[1].hi>=1:raise ValueError('REGULAR_DOMAIN')
        right_h=rational(s.get('right_neighborhood','0'))
        if right_h<0:raise ValueError('RIGHT_NEIGHBORHOOD')
        ti=math.I(t0,t1+right_h)
        H=interval(s['H_CLASS'])
        if H.lo<=0:raise ValueError('BACKGROUND_POSITIVITY')
        qq=math.A(domain[0],[math.I(1),math.I(0)]);ww=math.A(domain[1],[math.I(0),math.I(1)])
        Qr,Gr,extra,z=field(qq,ww,ti,T0,n0,f,H,gamma)
        if z.lo<=1600 or z.hi>2870 or extra['h'].v.lo<=0 or extra['h'].v.hi>=1 or extra['K'].v.lo<=0:
            raise ValueError('REGULAR_DOMAIN_OR_MODE')
        M=[[Qr.d[0].hi,Qr.d[1].absmax()],[Gr.d[0].absmax(),Gr.d[1].hi]]
        pF=field(p[0],p[1],math.I(t0,t1),T0,n0,f,H,gamma)[:2]
        pd=[poly_range([F(k)*row[k]/h for k in range(1,len(row))] or [F(0)]) for row in coeff]
        delta=[(pd[i]-pF[i]).absmax() for i in range(2)]
        endpoints0=[poly_at(row,F(0)) for row in coeff];endpoints1=[poly_at(row,F(1)) for row in coeff]
        R0=previous_radius if previous_radius is not None else [(initial[i]-endpoints0[i]).absmax() for i in range(2)]
        invariant=all(R0[i]<=B[i] and sum((M[i][j]*B[j] for j in range(2)),F(0))+delta[i]<=0 for i in range(2))
        closure=all(domain[i].lo<p[i].lo-B[i] and p[i].hi+B[i]<domain[i].hi for i in range(2))
        entry=dict(index=index,t0=str(t0),t1=str(t1),predictor_range=[pairs(x) for x in p],
            delta=[str(x) for x in delta],M=[[str(x) for x in row] for row in M],R0=[str(x) for x in R0],
            radius_budget=[str(x) for x in B],invariant_radius_gate=invariant,tube_containment_gate=closure,Q_upper=str(Qr.v.hi),z=pairs(z))
        if not invariant or not closure:
            entry['failure']='INVARIANT_RADIUS_OR_STRICT_TUBE_CLOSURE';report['segments'].append(entry);return report
        E,J=comparison_matrices(M,h)
        Rend=[sum((E[i][j]*R0[j]+J[i][j]*delta[j] for j in range(2)),math.I(0)).hi for i in range(2)]
        if any(Rend[i]>B[i] for i in range(2)):raise ValueError('COMPARISON_ENDPOINT_INCONSISTENT')
        left=math.I(endpoints0[0]-R0[0],endpoints0[0]+R0[0]);right=math.I(endpoints1[0]-Rend[0],endpoints1[0]+Rend[0])
        boundary=field(math.I(EPS),domain[1],ti,T0,n0,f,H,gamma)[2]
        strict_boundary=boundary['D'].hi<0 and boundary['K'].lo>0
        right_mode=rational(s.get('right_neighborhood','0'))>0
        monotone=Qr.v.hi<0
        entry.update(R_end=[str(x) for x in Rend],left_q=pairs(left),right_q=pairs(right),
            D_epsilon=pairs(boundary['D']),boundary_K=pairs(boundary['K']),first_hit_prefix_separated=prefix_separated,
            monotone_upper_rate=monotone,right_mode_neighborhood=right_mode)
        report['segments'].append(entry)
        if prefix_separated and left.lo>EPS and right.hi<EPS and strict_boundary and monotone and right_mode:
            report['conditional_event_gate']='PASS'
            report['event_time_interval']=[str(t0),str(t1)]
            report['event_state_enclosure']={'q':[str(EPS),str(EPS)],'w':pairs(domain[1])}
            report['event_rate_upper']=str(boundary['K'].lo*boundary['D'].hi)
            report['covered_domain']=[segments[0]['t0'],str(t1)]
            return report
        separated=p[0].lo-B[0]>EPS
        # Strictly decreasing source field and strict right endpoint can also
        # exclude an earlier hit over this entire segment without a loose B.
        if monotone and right.lo>EPS:separated=True
        prefix_separated=prefix_separated and separated
        previous_radius=Rend;left_above=left.lo>EPS
    if prefix_separated:report['conditional_nonreachability_gate']='PASS_ON_COVERED_DOMAIN'
    report['covered_domain']=[segments[0]['t0'],segments[-1]['t1']]
    return report

def input_admission(targets):
    if targets.get('q')!=Q or targets.get('source_commit')!=SOURCE or set(targets['cases'])!=set(CASES):
        raise ValueError('TARGET_IDENTITY')
    out={}
    for case,v in targets['cases'].items():
        missing=['qualified_source_continuum_input','qualified_pre_onset_temperature','source_continuum_background_enclosure',
                 'full_enabled_pre_event_path_certificate','all_competing_source_switches_verified','threshold_mapping']
        # A boolean or supplied object is not a proof this checker can verify.
        # V1 exposes no actual-admission success path until those proof formats
        # and their independent verifiers exist. This is an explicit scope limit.
        out[case]={'gate':'FAIL','actual_applicability':'INSUFFICIENT_EVIDENCE','missing_objects':missing,
          'native_meta_status':v['raw_status'],'effective_parameter_export_required':case.endswith('ede_n3'),
          'accepted_z_reio':v['accepted_z_reio']}
    return out

def local_fixture(path):
    """Manufactured local proof-input control. NEVER the actual initial state."""
    row=load(path)['cases']['camspec-lcdm'];native=json.loads(row['native_meta_text']);hint=row['native_hint'];near=row['temperature_neighbor']
    t0=F(str(log(2871/(1+float(hint['z'])))));t1=t0+F('8e-6')
    w=1-F(near['Tb [K]'])/(F('2.7255')*(1+F(near['z'])))
    first=row['first_background_raw'];gamma=F(first['(.)rho_g'])/(1+F(first['z']))**4
    def around(x,r):return [str(F(str(x))-r),str(F(str(x))+r)]
    return {'schema':'Q047-UPPER-PACKET-V1','q':Q,'case_id':'camspec-lcdm','source_commit':SOURCE,
      'scope':'CONDITIONAL_LOCAL_UPPER_IVP','fixture_role':'Manufactured state/path assumptions near a native hint; not measured or validated initial data',
      'parameters':{'T0':['2.725499999','2.725500001'],'nH0':around(native['nH0_m3'],F('1e-12')),
         'fHe':around(native['fHe'],F('1e-12')),'gamma0':[str(gamma*(1-F('1e-8'))),str(gamma*(1+F('1e-8')))]},
      'initial_state':[['0.000001000999','0.000001001001'],[str(w-F('1e-12')),str(w+F('1e-12'))]],
      'segments':[{'t0':str(t0),'t1':str(t1),'predictor':[['0.000001001','-0.000000002'],[str(w)]],
        'domain':[['0.0000007','0.0000013'],[str(w-F('2e-8')),str(w+F('2e-8'))]],
        'radius_budget':['0.0000002','0.00000001'],'H_CLASS':around(hint['H_1_Mpc'],F('.001')),
        'right_neighborhood':'0.00000001'}]}

def run(out):
    start=time.monotonic();targets=load(ROOT/'q047_targets_v1.json');admission=input_admission(targets)
    local=check_upper_packet(local_fixture(ROOT/'q047_control_input_v1.json'))
    result={'q':Q,'program_id':ID,'program_version':VERSION,'scientific_question':targets['scientific_question'],
      'execution_status':'COMPLETE','result_status':'TECHNICAL_QUALIFICATION_ONLY','final_result_gate':'UNRESOLVED',
      'actual_computed_result':'NO_QUALIFIED_FOUR_CASE_TRAJECTORY','actual_applicability':{k:v['actual_applicability'] for k,v in admission.items()},
      'input_admission':admission,'manufactured_conditional_control':local,'new_native_evaluations':0,
      'execution_base_commit':targets['execution_base_commit'],'executed_repository_commit':os.environ.get('GITHUB_SHA','LOCAL_NOT_INSTALLED'),
      'run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),'source_commit':SOURCE,'python':platform.python_version(),
      'elapsed_seconds':time.monotonic()-start,'source_ids':['I-PROPOSED-Q047-METHOD-001','I-PROPOSED-Q047-CONTROLS-001','K-PROPOSED-Q047-SOURCE-001'],
      'input_hashes':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['q047_targets_v1.json','q047_control_input_v1.json']},
      'return_route':'RESULT INGESTION & ROUTING ENGINE','journal_effect':'Actual applicability unresolved; explicit conditional checker and input obligations now implemented.'}
    write(Path(out)/'q047_certificate_final_v1.json',result)
    write(Path(out)/'q047_required_inputs_v1.json',{'q':Q,'program_id':ID,'cases':admission})
    write(Path(out)/'q047_conditional_control_v1.json',local)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--program-id',default=ID)
    parser.add_argument('--out',default='q047_results');parser.add_argument('--packet')
    args=parser.parse_args()
    if args.program_id!=ID:raise ValueError('PROGRAM_ID_GATE')
    if sys.flags.optimize:raise ValueError('OPTIMIZED_ASSERTIONS_UNSUPPORTED')
    if args.packet:
        result=check_upper_packet(load(args.packet));write(Path(args.out)/'q047_conditional_packet_result_v1.json',result)
    else:result=run(args.out)
    print(json.dumps({'q':Q,'program_id':ID,'final_result_gate':result['final_result_gate'],'scope':result.get('scope','TECHNICAL_QUALIFICATION_ONLY')}))

if __name__=='__main__':main()
