"""Q048 V7: finite source-real Camspec direct-guard and He1f/He2 continuation.

Scientific scope is deliberately narrow.  This module does NOT qualify native
floating-point/source-instance identity, does NOT locate the shared q=1e-6 event,
and does NOT compute complete x_e(z) or tau_T(z) latch/reset histories.

The only new machine proof is:
  1. a source-root, trajectory-correlated validated (phi,X) tube for Camspec EDE
     with the exact source guard checked on every certified whole-state cell;
  2. sign-correct positive-w continuation from z=4600 through He1f and He2 to
     z=2870 for both EDE configurations; and
  3. conditional source-real H-entry q bounds at z=2870.

A bounded proof obstruction is returned as UNRESOLVED evidence, never promoted
into a physical crossing or model falsification.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,json,time
import q048_structural_v6 as v6
old=v6.old;p=v6.p;m=v6.m;pre=v6.pre;proof=v6.proof
ROOT=Path(__file__).resolve().parent
ID='Q048-GUARDCONT-V7';VERSION='v7';Q=v6.Q;SOURCE=v6.SOURCE
SCOPE='CONDITIONAL_SOURCE_REAL_GUARD_THERMAL_CONTINUATION'
CONFIG_SHA='abfb92643e8d2e6eca34b36b137e11900e78faa30a80082ed74dfb0992ad0a99'


def fail(condition,message):
 if not condition: raise ValueError(message)

def sha256(path):
 h=hashlib.sha256();
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def git_blob_sha1(path):
 b=Path(path).read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def settings():
 s=old.load(ROOT/'q048_guard_config_v7.json')
 fail(sha256(ROOT/'q048_guard_config_v7.json')==CONFIG_SHA,'CONFIG_HASH')
 fail(s['program_id']==ID and s['q']==Q and s['source_commit']==SOURCE and s['version']==VERSION,'CONFIG_IDENTITY')
 return s

def validate_sources():
 s=settings();v6.validate_sources()
 for name,want in s['reused_git_blob_sha1'].items():fail(git_blob_sha1(ROOT/name)==want,'REUSED_GIT_BLOB '+name)
 fail(sha256(ROOT/s['math007_file'])==s['math007_sha256'],'MATH007_HASH')
 fail(sha256(ROOT/s['journal_file'])==s['journal_sha256'],'JOURNAL_HASH')
 cfg=v6.config();fail(cfg['scientific_question']==s['scientific_question'],'QUESTION_TEXT')
 fail(cfg['question_sha256']==s['question_sha256'],'QUESTION_HASH')
 return s

def _mid(x):return (x.lo+x.hi)/2

def _pairs(x):return proof.pairs(x)

def _background_base(a,t):
 u=dict(t);u['ede']=None;return pre.background(a,u)

def direct_guard(a,whole,t):
 """Direct source guard, plus algebraically equivalent positive margin.

 Source tests ve/(3 H^2)<1/2.  For K=0 and V=ve+floor this is equivalent
 to 3*B(a)+X^2/2+floor-ve > 0.  The margin form avoids interval dependency
 from dividing two phi-dependent quantities and is the acceptance proof.
 """
 fail(t['ede'] is not None and len(whole)==2,'GUARD_EDE_STATE')
 phi,X=whole;base=_background_base(a,t);V,_,ve=pre.potential(phi,t['ede'])
 floor=t['ede']['B']*m.const('3.968e-8');kinetic=pre.square(X)/2
 base3=3*pre.square(base['H']);den=base3+kinetic+V
 fail(den.lo>0,'GUARD_DENOMINATOR')
 ratio=ve/den;margin=base3+kinetic+floor-ve
 return {'ratio':ratio,'margin':margin,'base_H':base['H'],'V':V,'Ve':ve,'kinetic':kinetic,'floor':floor}

def _guard_field(now,end,t):
 width=end-now
 def field(xi,y):
  a=m.I(now)+m.I(width)*xi
  rates=pre.ede_field(a,y,t)[0]
  return [r*m.I(width)/a for r in rates]
 return field

def _predictor_and_box(now,end,current,t):
 field=_guard_field(now,end,t);center=[_mid(x) for x in current]
 k1=[pre.value(x) for x in field(m.I(0),[m.A(c) for c in center])]
 k1m=[_mid(x) for x in k1]
 half=[m.A(center[i]+k1m[i]/2) for i in range(2)]
 k2=[pre.value(x) for x in field(m.I(F(1,2)),half)];k2m=[_mid(x) for x in k2]
 coeff=[];box=[];floors=[F(settings()['guard']['phi_pad_floor']),F(settings()['guard']['x_pad_floor'])]
 for i in range(2):
  row=[center[i],k1m[i],k2m[i]-k1m[i]];pr=proof.poly_range(row)
  err=(current[i].hi-current[i].lo)/2;move=abs(row[1])+abs(row[2])
  pad=max(floors[i],4*err,move/2)
  coeff.append([str(x) for x in row]);box.append([str(pr.lo-pad),str(pr.hi+pad)])
 return field,{'t0':'0','t1':'1','predictor':coeff,'box':box}

def _guard_cell(now,end,current,t):
 field,cell=_predictor_and_box(now,end,current,t)
 try:
  report=pre.certify_cell(cell,current,field)
 except ValueError as exc:
  # The inherited Q047 comparison backend deliberately rejects cells whose
  # normalized Metzler growth bound is too large.  For the V7 adaptive guard
  # trajectory this is a local step-size obstruction, not a scientific result:
  # return a refinement request so guard_trajectory halves the physical cell.
  # All other certificate failures remain fail-closed and are re-raised.
  if str(exc)=='COMPARISON_GROWTH_CAP':
   return None,'CERTIFICATE_COMPARISON_GROWTH_CAP',cell,None,None
  raise
 if not report['closed']:return None,'TRAJECTORY_TUBE_NOT_CLOSED',cell,report,None
 whole=[proof.interval(x) for x in report['whole_state']];g=direct_guard(m.I(now,end),whole,t)
 # The mathematically equivalent margin is the acceptance criterion.  A loose
 # direct ratio interval may exceed 1/2 through dependency without invalidating
 # the stronger equivalent inequality proof.
 if g['margin'].lo<=0:return None,'DIRECT_GUARD_MARGIN_NOT_SEPARATED',cell,report,g
 accepted={'a0':str(now),'a1':str(end),'input':cell,'certificate':report,
  'guard':{k:_pairs(v) for k,v in g.items()}}
 return accepted,None,cell,report,g

def guard_trajectory(row,t,deadline=None,progress=None,resume=None):
 s=settings()['guard'];target=F(s['target_a']);step=F(s['relative_step']);milestones=sorted(map(F,s['milestones']))
 initial,a,state=p.source_initial(row,t);fail(initial['initial_conditions_gate']=='PASS_CONDITIONAL','INITIAL_SOURCE_GATE')
 fail(t['K'].lo==t['K'].hi==0,'GUARD_K_ZERO_REQUIRED')
 now=a.lo;current=state;cells=[];blocker=None;attempts=0
 if resume is not None:
  verified=verify_guard_trajectory(resume,row,t,allow_partial=True)
  cells=copy.deepcopy(resume['cells']);now=F(resume['certified_end_a']);current=[proof.interval(x) for x in resume['endpoint']]
  fail(verified['gate']=='PASS_RECOMPUTED_PREFIX','RESUME_PREFIX')
 start_clock=time.monotonic();deadline=(start_clock+s['case_seconds']) if deadline is None else deadline
 while now<target and len(cells)<s['max_cells'] and time.monotonic()<deadline:
  milestone=min(x for x in milestones if x>now)
  candidate=min(milestone,now*(1+step));accepted=None;reason='NO_ATTEMPT'
  for _ in range(s['max_halvings']+1):
   attempts+=1
   accepted,reason,_,_,_=_guard_cell(now,candidate,current,t)
   if accepted is not None:break
   candidate=(now+candidate)/2
  if accepted is None:
   blocker=reason;break
  cells.append(accepted);current=[proof.interval(x) for x in accepted['certificate']['endpoint']];now=F(accepted['a1'])
  if progress and len(cells)%s['progress_every_cells']==0:progress(cells,now,current,attempts)
 if now<target and blocker is None:
  blocker='WORK_CAP' if len(cells)>=s['max_cells'] else 'WALL_TIME_CAP'
 status='PASS_CONDITIONAL_DIRECT_GUARD' if now==target else 'UNRESOLVED_BOUNDED_OBSTRUCTION'
 margins=[F(c['guard']['margin'][0]) for c in cells]
 ratios=[F(c['guard']['ratio'][1]) for c in cells]
 return {'method':s['method'],'status':status,'requested_end_a':str(target),'certified_end_a':str(now),
  'initial_a':str(a.lo),'initial_state':list(map(_pairs,state)),'cells':cells,'cell_count':len(cells),'attempts':attempts,
  'endpoint':list(map(_pairs,current)),'blocker':blocker,
  'minimum_guard_margin_lower':str(min(margins)) if margins else None,
  'maximum_direct_ratio_interval_upper_diagnostic':str(max(ratios)) if ratios else None,
  'guard_acceptance':'EQUIVALENT_POSITIVE_MARGIN_ON_EVERY_CERTIFIED_WHOLE_STATE_CELL',
  'actual_source_admission':'UNRESOLVED'}

def verify_guard_trajectory(obj,row,t,allow_partial=False):
 s=settings()['guard'];initial,a,state=p.source_initial(row,t);now=a.lo;current=state
 fail(obj['method']==s['method'],'GUARD_METHOD');fail(F(obj['initial_a'])==now,'GUARD_INITIAL_A')
 fail(obj['initial_state']==list(map(_pairs,state)),'GUARD_INITIAL_STATE')
 for stored in obj['cells']:
  end=F(stored['a1']);fail(F(stored['a0'])==now and now<end,'GUARD_PARTITION')
  field=_guard_field(now,end,t);report=pre.certify_cell(stored['input'],current,field)
  fail(report==stored['certificate'] and report['closed'],'GUARD_CELL_RECOMPUTE')
  whole=[proof.interval(x) for x in report['whole_state']];g=direct_guard(m.I(now,end),whole,t)
  fail(g['margin'].lo>0,'GUARD_MARGIN_RECOMPUTE')
  fail(stored['guard']=={k:_pairs(v) for k,v in g.items()},'GUARD_PAYLOAD_RECOMPUTE')
  current=[proof.interval(x) for x in report['endpoint']];now=end
 fail(obj['endpoint']==list(map(_pairs,current)) and F(obj['certified_end_a'])==now,'GUARD_ENDPOINT')
 fail(obj['cell_count']==len(obj['cells']) and F(obj['requested_end_a'])==F(s['target_a']),'GUARD_SUMMARY')
 margins=[F(c['guard']['margin'][0]) for c in obj['cells']];ratios=[F(c['guard']['ratio'][1]) for c in obj['cells']]
 fail(obj['minimum_guard_margin_lower']==(str(min(margins)) if margins else None),'GUARD_MARGIN_SUMMARY')
 fail(obj['maximum_direct_ratio_interval_upper_diagnostic']==(str(max(ratios)) if ratios else None),'GUARD_RATIO_SUMMARY')
 fail(obj['guard_acceptance']=='EQUIVALENT_POSITIVE_MARGIN_ON_EVERY_CERTIFIED_WHOLE_STATE_CELL' and obj['actual_source_admission']=='UNRESOLVED','GUARD_SCOPE_SUMMARY')
 target=F(s['target_a'])
 if obj['status']=='PASS_CONDITIONAL_DIRECT_GUARD':fail(now==target,'GUARD_FALSE_PASS')
 else:fail(allow_partial and now<target,'GUARD_PARTIAL_SCOPE')
 return {'gate':'PASS_RECOMPUTED_PREFIX' if now<target else'PASS_RECOMPUTED_FULL_GUARD','cells':len(obj['cells']),'end_a':str(now)}

def rational_voc_control(current,c,d):
 """Independent rational-only comparison; no exp/sqrt primitives.

 For x>0: 0<exp(-x)<=1/(1+x), and 1/(1+x)<=(1-exp(-x))/x<=1/x.
 This is deliberately looser than the primary rigorous exponential enclosure.
 """
 L,U=current.lo,current.hi;c0,c1=c.lo,c.hi;d0,d1=d.lo,d.hi
 fail(0<L<=U and 0<c0<=c1 and 0<d0<=d1,'POSITIVE_VOC_DOMAIN')
 lower=c0/(1+d1)
 upper=U/(1+d0)+c1/d0
 return m.I.rounded(lower,upper)

def advance_w(mode,a0,a1,current,t,bg):
 fail(mode in ('He1f','He2') and a0<a1,'THERMAL_PHASE')
 whole=m.I(F(0),F(settings()['thermal']['whole_w'][1]));fail(current.lo>0 and current.hi<=whole.hi,'POSITIVE_W_START')
 ai=m.I(a0,a1);width=a1-a0;info=pre.thermal(mode,ai,whole,t,bg);beta=info['beta'];c=m.I(width)/ai;d=c*(1+beta)
 lr=pre.thermal(mode,ai,m.I(whole.lo),t,bg)['rate'];ur=pre.thermal(mode,ai,m.I(whole.hi),t,bg)['rate']
 fail(beta.lo>0 and info['Tmat'].lo>0 and lr.lo>0 and ur.hi<0,'THERMAL_INVARIANT_BARRIER')
 # Sign-aware primary enclosure from Mathematics-007: positive L uses exp(-d_max).
 lo=m.I(current.lo)*m.exp_i(m.I(-d.hi))+m.I(c.lo)*proof.exponential_integral(m.I(-d.hi),F(1))
 hi=m.I(current.hi)*m.exp_i(m.I(-d.lo))+m.I(c.hi)*proof.exponential_integral(m.I(-d.lo),F(1))
 primary=m.I(lo.lo,hi.hi);ind=rational_voc_control(current,c,d)
 L=max(primary.lo,ind.lo);U=min(primary.hi,ind.hi);fail(L<=U and 0<L<=U<=whole.hi,'THERMAL_INDEPENDENT_CONTROL')
 endpoint=m.I(L,U)
 return endpoint,{'mode':mode,'a0':str(a0),'a1':str(a1),'initial_state':_pairs(current),'whole_state':_pairs(whole),
  'endpoint':_pairs(endpoint),'primary_endpoint':_pairs(primary),'independent_endpoint':_pairs(ind),
  'beta':_pairs(beta),'c':_pairs(c),'d':_pairs(d),'Tmat_K':_pairs(info['Tmat']),
  'lower_boundary_rate':_pairs(lr),'upper_boundary_rate':_pairs(ur),'gate':'PASS_CONDITIONAL_SIGN_AWARE_POSITIVE_W'}

def _bg_from_guard_cell(cell,t):
 whole=[proof.interval(x) for x in cell['certificate']['whole_state']];a=m.I(F(cell['a0']),F(cell['a1']))
 b=pre.background(a,t,whole);return {'H':b['H'],'Hs':b['Hs'],'rho_gamma':b['rho_gamma']}

def _energy_bg(a0,a1,t,energy):
 base=_background_base(m.I(a0,a1),t);E=m.I(F(energy['potential_floor'][0]),F(energy['energy_upper']))
 H=m.sqrt_i(pre.square(base['H'])+E/3);return {'H':H,'Hs':H*m.C['c']/m.C['Mpc'],'rho_gamma':base['rho_gamma']}

def saha_transition_control(a,w,t,bg):
 x1=pre.thermal('He1f',m.I(a),w,t,bg)['x'];x2=pre.thermal('He2',m.I(a),w,t,bg)['x']
 # Interval implementations are algebraically identical in exact-real semantics;
 # finite outward representations need only have a nonempty common enclosure.
 lo=max(x1.lo,x2.lo);hi=min(x1.hi,x2.hi);fail(lo<=hi,'SAHA_TRANSITION_DISJOINT')
 return {'a':str(a),'he1f_x':_pairs(x1),'he2_x':_pairs(x2),'common_enclosure':_pairs(m.I(lo,hi)),
  'exact_identity_reference':'I-PROPOSED-Q048-MATHEMATICS-007','gate':'PASS_SOURCE_REAL_SAHA_IDENTITY_CONTROL'}

def thermal_continuation(case,row,t,v6ext,guard=None):
 fail(case in settings()['thermal']['cases'],'THERMAL_CASE')
 current=proof.interval(v6ext['phase']['endpoint']);fail(current.lo>0,'V6_POSITIVE_ENDPOINT_REQUIRED')
 starts=[F(1,4601),F(1,3551),F(1,2871)];modes=['He1f','He2'];cells=[];transition=None
 energy=v6ext['energy']
 if case=='camspec-ede_n3':
  if guard is None or guard['status']!='PASS_CONDITIONAL_DIRECT_GUARD':
   return {'status':'UNRESOLVED_GUARD_INCOMPLETE','start_w':_pairs(current),'cells':[],'h_entry_q':'NOT_COMPUTED','blocker':'CAMPSPEC_DIRECT_GUARD_REQUIRED'}
  gcells=guard['cells']
 for phase,(a0,a1) in enumerate(zip(starts[:-1],starts[1:])):
  mode=modes[phase];now=a0
  if case=='camspec-ede_n3':
   relevant=[c for c in gcells if F(c['a0'])>=a0 and F(c['a1'])<=a1 and F(c['a1'])>a0]
   fail(relevant and F(relevant[0]['a0'])==a0 and F(relevant[-1]['a1'])==a1,'GUARD_THERMAL_COVERAGE')
   for ccell in relevant:
    ca0,ca1=F(ccell['a0']),F(ccell['a1']);bg=_bg_from_guard_cell(ccell,t)
    current,rep=advance_w(mode,ca0,ca1,current,t,bg);cells.append(rep);now=ca1
  else:
   step=F(settings()['thermal']['hillipop_relative_step'])
   while now<a1:
    end=min(a1,now*(1+step));bg=_energy_bg(now,end,t,energy)
    current,rep=advance_w(mode,now,end,current,t,bg);cells.append(rep);now=end
  fail(now==a1,'THERMAL_PHASE_END')
  if a1==F(1,3551):
   bg=_bg_from_guard_cell(next(c for c in gcells if F(c['a1'])==a1),t) if case=='camspec-ede_n3' else _energy_bg(a1,a1,t,energy)
   transition=saha_transition_control(a1,current,t,bg)
 a=F(1,2871);q=pre.onset(current,m.I(a),t)
 return {'status':'PASS_CONDITIONAL_TO_H_ENTRY','method':settings()['thermal']['method'],'independent_method':settings()['thermal']['independent_method'],
  'start_a':'1/4601','end_a':'1/2871','start_w':v6ext['phase']['endpoint'],'endpoint_w':_pairs(current),'h_entry_q':_pairs(q),
  'cells':cells,'saha_transition':transition,'actual_source_admission':'UNRESOLVED'}

def verify_thermal_continuation(case,row,t,v6ext,guard,obj):
 fail(obj['method']==settings()['thermal']['method'] and obj['independent_method']==settings()['thermal']['independent_method'],'THERMAL_METHOD')
 current=proof.interval(v6ext['phase']['endpoint']);fail(obj['start_w']==v6ext['phase']['endpoint'],'THERMAL_START_BINDING')
 start,switch,end=F(1,4601),F(1,3551),F(1,2871);now=start
 fail(obj['start_a']=='1/4601' and obj['end_a']=='1/2871','THERMAL_BOUNDARY_BINDING')
 if case=='camspec-ede_n3':
  fail(guard['status']=='PASS_CONDITIONAL_DIRECT_GUARD','THERMAL_GUARD_REQUIRED');gcells={(F(c['a0']),F(c['a1'])):c for c in guard['cells']}
 expected=[];transition=None
 for stored in obj['cells']:
  mode=stored['mode'];a0,a1=F(stored['a0']),F(stored['a1'])
  fail(a0==now and a0<a1<=end,'THERMAL_PARTITION')
  expected_mode='He1f' if a0<switch else 'He2';fail(mode==expected_mode and not (a0<switch<a1),'THERMAL_MODE_PARTITION')
  if case=='camspec-ede_n3':
   fail((a0,a1) in gcells,'THERMAL_GUARD_CELL_BINDING');bg=_bg_from_guard_cell(gcells[(a0,a1)],t)
  else:bg=_energy_bg(a0,a1,t,v6ext['energy'])
  current,rep=advance_w(mode,a0,a1,current,t,bg);fail(rep==stored,'THERMAL_CELL_RECOMPUTE');expected.append(rep)
  if a1==switch:transition=saha_transition_control(a1,current,t,bg)
  now=a1
 fail(now==end,'THERMAL_FINAL_BOUNDARY')
 fail(obj['cells']==expected and obj['endpoint_w']==_pairs(current),'THERMAL_ENDPOINT_RECOMPUTE')
 fail(obj['saha_transition']==transition and transition is not None,'THERMAL_SAHA_RECOMPUTE')
 q=pre.onset(current,m.I(F(1,2871)),t);fail(obj['h_entry_q']==_pairs(q),'THERMAL_H_ENTRY_Q_RECOMPUTE')
 fail(obj['status']=='PASS_CONDITIONAL_TO_H_ENTRY' and obj['actual_source_admission']=='UNRESOLVED','THERMAL_SCOPE')
 return {'gate':'PASS_RECOMPUTED_THERMAL_CONTINUATION','cells':len(expected),'h_entry_q':obj['h_entry_q']}

def derive(case,progress=None,resume=None):
 fail(case in settings()['thermal']['cases'],'CASE')
 parent=v6.parent_checkpoint(case);v6ext=v6.derive(case,parent);row=v6.config()['cases'][case];t=p.parameters(row)
 fail(v6ext['phase']['endpoint'][0] is not None and F(v6ext['phase']['endpoint'][0])>0,'V6_ENDPOINT_NOT_POSITIVE')
 if case=='camspec-ede_n3':
  deadline=time.monotonic()+settings()['guard']['case_seconds'];guard=guard_trajectory(row,t,deadline=deadline,progress=progress,resume=resume)
 else:
  energy=v6ext['energy'];fail(energy['full_transfer_source_guard']=='PASS','HILLIPOP_V6_GUARD')
  guard={'method':'inherited_v6_source_root_energy_guard','status':'PASS_CONDITIONAL_DIRECT_GUARD_NOT_REQUIRED',
   'requested_end_a':'1/2871','certified_end_a':'1/2871','source':v6.ID,'energy_guard':copy.deepcopy(energy)}
 thermal=thermal_continuation(case,row,t,v6ext,guard if case=='camspec-ede_n3' else None)
 return {'q':Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','program_id':ID,'version':VERSION,'scope':SCOPE,
  'scientific_question':settings()['scientific_question'],'question_sha256':settings()['question_sha256'],'source_commit':SOURCE,'configuration':case,
  'v6_parent_program':v6.ID,'v6_extension_sha256':old.objhash(v6ext),'guard':guard,'thermal':thermal,
  'actual_source_admission':'UNRESOLVED','actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
  'final_result_gate':'UNRESOLVED','return_route':'RESULT INGESTION & ROUTING ENGINE'}

def verify_extension(case,obj):
 fail(case in settings()['thermal']['cases'] and obj['configuration']==case,'VERIFY_CASE')
 parent=v6.parent_checkpoint(case);v6ext=v6.derive(case,parent);row=v6.config()['cases'][case];t=p.parameters(row)
 fail(obj['v6_extension_sha256']==old.objhash(v6ext),'VERIFY_V6_BINDING')
 fail(obj['actual_source_admission']=='UNRESOLVED' and obj['final_result_gate']=='UNRESOLVED','VERIFY_SCOPE')
 if case=='camspec-ede_n3':
  if obj['guard']['status']!='PASS_CONDITIONAL_DIRECT_GUARD':
   verify_guard_trajectory(obj['guard'],row,t,allow_partial=True)
   fail(obj['thermal']['status']=='UNRESOLVED_GUARD_INCOMPLETE' and obj['thermal']['h_entry_q']=='NOT_COMPUTED','PARTIAL_THERMAL_SCOPE')
   return {'gate':'PASS_RECOMPUTED_BOUNDED_OBSTRUCTION','configuration':case}
  guard_check=verify_guard_trajectory(obj['guard'],row,t,allow_partial=False)
 else:
  energy=v6ext['energy'];fail(energy['full_transfer_source_guard']=='PASS','VERIFY_HILLIPOP_GUARD')
  expected_guard={'method':'inherited_v6_source_root_energy_guard','status':'PASS_CONDITIONAL_DIRECT_GUARD_NOT_REQUIRED',
   'requested_end_a':'1/2871','certified_end_a':'1/2871','source':v6.ID,'energy_guard':copy.deepcopy(energy)}
  fail(obj['guard']==expected_guard,'VERIFY_HILLIPOP_GUARD_PAYLOAD');guard_check={'gate':'PASS_INHERITED_V6_GUARD'}
 thermal_check=verify_thermal_continuation(case,row,t,v6ext,obj['guard'],obj['thermal'])
 return {'gate':'PASS_RECOMPUTED_V7_EXTENSION','configuration':case,'guard':guard_check,'thermal':thermal_check}
