"""One bounded source-root energy/He1 extension. Frozen V5 parent is immutable.

No stored PASS or math006 endpoint is admitted as a certificate. Recompute the
root energy and phase bounds; inherited certificates are reverified by V5.
All full/native physical products remain NOT_COMPUTED/UNRESOLVED.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,json,os,platform,sys,time
import q048_resume_v5 as old
p=old.p;m=p.m;pre=p.pre;proof=p.old
ROOT=Path(__file__).resolve().parent
ID='Q048-STRUCTURAL-V6';VERSION='v6';Q=p.Q;SOURCE=p.SOURCE
SCOPE='CONDITIONAL_SOURCE_REAL_STRUCTURAL_EXTENSION'
METHOD='source_root_energy_he1_invariant_voc_v1'
CONFIG_SHA='585e10632bca1b3bd268b6b0268901da44616bfd9c5e8b6792a8e6116856b264'  # Filled by package builder; exact frozen contract hash.
_CACHE={}

def fail(condition,message):
 if not condition:raise ValueError(message)

def settings():
 s=old.load(ROOT/'q048_structural_config_v6.json')
 fail(old.digest(ROOT/'q048_structural_config_v6.json')==CONFIG_SHA,'STRUCTURAL_CONFIG_HASH')
 fail(s['program_id']==ID and s['q']==Q and s['source_commit']==SOURCE,'CONFIG_IDENTITY')
 return s

def validate_sources():
 s=settings()
 for name,want in s['reused_source_sha256'].items():fail(old.digest(ROOT/name)==want,'SOURCE_PIN '+name)
 fail(old.digest(ROOT/s['parent_file'])==s['parent_file_sha256'],'PARENT_RAW_HASH')
 fail(old.digest(ROOT/'Q048_V5_STRUCTURAL_MATHEMATICS.json')==s['mathematics_sha256'],'MATH_INPUT_PIN')
 fail(old.digest(ROOT/'Q048_V5_INDEPENDENT_REVIEW.json')==s['review_sha256'],'REVIEW_INPUT_PIN')
 return s

def config():return p.validate_config(old.load(ROOT/settings()['source_config_file']))

def parent_checkpoint(case):
 s=settings();fail(case in p.CASES,'CASE')
 if 'raw' not in _CACHE:
  fail(old.digest(ROOT/s['parent_file'])==s['parent_file_sha256'],'PARENT_RAW_HASH')
  raw=old.load(ROOT/s['parent_file'])
  fail(raw['schema']=='Q048_RESUME_FINAL_V5' and raw['program_id']==old.ID and raw['config_hash']==s['parent_config_hash'] and raw['job_completeness_gate']=='PASS','PARENT_RAW_IDENTITY')
  fail(set(raw['records'])==set(p.CASES),'PARENT_CASE_COMPLETENESS')
  _CACHE['raw']=raw
 raw=_CACHE['raw'];x={'schema':'Q048_CHECKPOINT_V5','metadata':raw['checkpoints'][case]['metadata'],'record':raw['records'][case]}
 encoded=(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 import hashlib
 fail(hashlib.sha256(encoded).hexdigest()==s['parent_checkpoints'][case],'PARENT_CHECKPOINT_HASH')
 fail(x['metadata']['run_id']==s['parent_run_id'] and x['record']['run_id']==s['parent_run_id'],'PARENT_RUN')
 old.validate_checkpoint(x,case,old.load(ROOT/'q048_resume_config_v5.json'))
 return copy.deepcopy(x)

def energy_certificate(row,t):
 fail(t['ede'] is not None,'EDE_REQUIRED')
 initial,a,state=p.source_initial(row,t)
 fail(initial['initial_conditions_gate']=='PASS_CONDITIONAL','INITIAL_SOURCE_GATE')
 V,_,_=pre.potential(state[0],t['ede']);floor=t['ede']['B']*m.const('3.968e-8')
 E0=pre.square(state[1])/2+V;cap=E0.hi;rad=t['gamma']+t['ur']
 fail(floor.lo>=0 and cap>=floor.lo and rad.lo>0 and t['matter'].lo>=0 and t['lambda'].lo>=0 and t['K'].lo==t['K'].hi==0,'ENERGY_POSITIVITY_DOMAIN')
 for n in t['neutrinos']:
  fail(n.get('reference','FINITE_NATIVE')=='FINITE_NATIVE' and n['mass'].lo>=0 and n['factor'].lo>=0 and all(q.lo>=0 for q in n['nodes']) and all(w.lo>=0 for w in n['weights']),'NEUTRINO_ENERGY_DOMAIN')
 Xcap=m.sqrt_i(m.I(2*(cap-floor.lo))).hi
 def box(end):
  disp=m.I(Xcap)*(end*end-a.lo*a.lo)/(2*m.sqrt_i(rad))
  return [m.I(state[0].lo-disp.hi,state[0].hi+disp.hi),m.I(-Xcap,Xcap)]
 def fraction(end):
  base=rad/end**4+t['matter']/end**3+t['lambda']
  for n in t['neutrinos']:base+=pre.neutrino_sum(m.I(end),n)[0]
  fail(base.lo>0,'BASE_POSITIVITY')
  return m.I(cap-floor.lo)/(3*base+m.I(cap)),base
 transfer=F(1,2871);ratio,base=fraction(transfer);low=a.lo;high=transfer
 if ratio.hi>=F(1,2):
  for _ in range(32):
   mid=(low+high)/2
   if fraction(mid)[0].hi<F(1,2):low=mid
   else:high=mid
 else:low=high=transfer
 fail(fraction(low)[0].hi<F(1,2),'ENERGY_SAFE_HORIZON')
 return {'method':'source_root_dissipative_energy_v1','identity':'dE/dln(a)=-3*X^2',
  'constant_semantics':'Same fixed source constants shared by V and V_phi; intervals only enclose them.',
  'initial_a':str(a.lo),'initial_state':list(map(proof.pairs,state)),'initial_conditions_gate':initial['initial_conditions_gate'],
  'potential_floor':proof.pairs(floor),'energy0':proof.pairs(E0),'energy_upper':str(cap),'X_abs_upper':str(Xcap),
  'radiation_lower':str(rad.lo),'box_at_transfer':list(map(proof.pairs,box(transfer))),
  'source_fraction_at_transfer':proof.pairs(ratio),'base_at_transfer':proof.pairs(base),
  'guard_certified_to_a':str(low),'guard_bracket_a':[str(low),str(high)],'guard_fraction_at_safe_end':proof.pairs(fraction(low)[0]),
  'full_transfer_source_guard':'PASS' if low==transfer else 'NOT_ESTABLISHED_BY_THIS_BOUND',
  'scope':'SOURCE_ROOTED_CONTINUOUS_CONDITIONAL_ENERGY_CERTIFICATE','initial_intervals_replaced':False}

def phase_certificate(record,row,t):
 energy=energy_certificate(row,t)  # Never trust a caller-supplied energy cap.
 now=old.coordinate(record['thermal']['certified_end_a']);current=proof.interval(record['thermal']['endpoint'][0])
 boundaries=[1/(1-p.point(s['mz']).lo)for s in row['thermal_starts'][1:5]]
 j=sum(now>=v for v in boundaries)
 fail(j==1 and pre.MODES[j]=='He1','HE1_PHASE_REQUIRED')
 end=boundaries[j];fail(end==F(1,4601) and now<end<=F(energy['guard_certified_to_a']),'PHASE_SOURCE_GUARD')
 whole=m.I(current.lo,F('0.02'));fail(current.lo<0<current.hi<=whole.hi,'HE1_INITIAL_INTERVAL_DOMAIN')
 width=end-now;ai=m.I(now,end);base_t=dict(t);base_t['ede']=None
 base=pre.background(ai,base_t);E=m.I(F(energy['potential_floor'][0]),F(energy['energy_upper']))
 H=m.sqrt_i(pre.square(base['H'])+E/3)
 bg={'H':H,'Hs':H*m.C['c']/m.C['Mpc'],'rho_gamma':base['rho_gamma']}
 info=pre.thermal('He1',ai,whole,t,bg);beta=info['beta'];c=m.I(width)/ai
 lr=pre.thermal('He1',ai,m.I(whole.lo),t,bg)['rate'];ur=pre.thermal('He1',ai,m.I(whole.hi),t,bg)['rate']
 fail(H.lo>0 and info['Tmat'].lo>0 and beta.lo>0 and lr.lo>0 and ur.hi<0,'HE1_INVARIANT_BARRIER')
 d=c*(1+beta)
 lower=m.exp_i(m.I(-d.lo))*current.lo+proof.exponential_integral(m.I(-d.hi),F(1))*c.lo
 upper=m.exp_i(m.I(-d.lo))*current.hi+proof.exponential_integral(m.I(-d.lo),F(1))*c.hi
 endpoint=m.I(lower.lo,upper.hi)
 fail(whole.lo<=endpoint.lo<=endpoint.hi<=whole.hi,'HE1_ENDPOINT_INCLUSION')
 phase={'method':METHOD,'mode':'He1','a0':str(now),'a1':str(end),'end_z':'4600',
  'initial_state':proof.pairs(current),'whole_state':proof.pairs(whole),'endpoint':proof.pairs(endpoint),
  'background_energy':proof.pairs(E),'background_H_CLASS_inverse_Mpc':proof.pairs(H),'beta':proof.pairs(beta),
  'Tmat_K':proof.pairs(info['Tmat']),'lower_boundary_rate':proof.pairs(lr),'upper_boundary_rate':proof.pairs(ur),
  'c':proof.pairs(c),'d':proof.pairs(d),'source_guard_horizon_a':energy['guard_certified_to_a'],
  'gate':'PASS_CONDITIONAL_REMAINING_HE1_PHASE','initial_interval_narrowed':False,
  'phase_transition_not_crossed':True,'native_or_full_history_admission':False,
  'background_method':'independent_source_root_energy_envelope_not_an_extrapolated_old_cell'}
 independent_control(phase)
 return phase

def independent_control(phase):
 """Exact rational comparison; independent of exp_i and exponential_integral."""
 L,U=map(F,phase['initial_state']);c0,c1=map(F,phase['c']);d0,d1=map(F,phase['d'])
 fail(L<0<U and 0<c0<=c1 and 0<d0<=d1,'INDEPENDENT_COEFFICIENT_DOMAIN')
 emin=(1+d0/64)**-64;emax=(1+d1/64)**-64
 lower=L*emin+c0*(1-emax)/d1;upper=U*emin+c1/d0
 # Outward serialization avoids enormous exact denominator strings, without
 # changing the inherited interval or weakening the rational inequality.
 lower=m.I.rounded(lower,lower).lo;upper=m.I.rounded(upper,upper).hi
 lo,hi=map(F,phase['whole_state']);pl,pu=map(F,phase['endpoint'])
 fail(lo<=lower<=upper<=hi and lower>0 and max(lower,pl)<=min(upper,pu),'INDEPENDENT_ENDPOINT_CONTROL')
 return {'method':'rational_exp_upper_v1','lemma':'exp(-d)<=(1+d/64)^(-64)',
  'endpoint':[str(lower),str(upper)],'gate':'PASS_CONDITIONAL_INDEPENDENT_CONTROL'}

def derive(case,parent):
 row=config()['cases'][case];r=parent['record'];t=p.parameters(row)
 fail(r['q']==Q and r['configuration']==case and r['source_commit']==SOURCE and r['source_input_hashes']==row['source_input_hashes'],'PARENT_SOURCE_IDENTITY')
 fail(r['actual_source_admission']=='UNRESOLVED' and r['final_result_gate']=='UNRESOLVED' and all(r[k]=='NOT_COMPUTED'for k in ('actual_event_redshift','actual_xe_history_bounds','actual_tau_T_bounds')),'PARENT_SCIENTIFIC_SCOPE')
 energy=energy_certificate(row,t)if t['ede'] else None
 phase=phase_certificate(r,row,t)if t['ede'] else None
 return {'q':Q,'q_assignment':'PROPOSED_UNVERIFIED','case_id':'NOT_ASSIGNED','source_commit':SOURCE,
  'scientific_question':row.get('scientific_question',config()['scientific_question']),
  'source_input_hashes':row['source_input_hashes'],'scope':SCOPE,'configuration':case,
  'status':'NEW_CONDITIONAL_ENERGY_HE1_PHASE_CERTIFICATE'if phase else'RETAINED_COMPLETE_CONDITIONAL_LCDM_PREFIX',
  'energy':energy,'phase':phase,'independent_control':independent_control(phase)if phase else None,
  'parent_record_sha256':old.objhash(r),'parent_checkpoint_sha256':settings()['parent_checkpoints'][case],
  'old_background_and_thermal_unchanged':True,'actual_source_admission':'UNRESOLVED','final_result_gate':'UNRESOLVED',
  'actual_event_redshift':'NOT_COMPUTED','actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED'}

def verify_extension(case,parent,extension):
 fail(extension==derive(case,parent),'STRUCTURAL_CERTIFICATE_RECOMPUTATION_MISMATCH')
 return {'gate':'PASS_CONDITIONAL_RECOMPUTED_EXTENSION','configuration':case}



def make_report(*args,**kwargs):
 from q048_structural_runner_v6 import make_report as operation
 return operation(*args,**kwargs)

def verify_report(*args,**kwargs):
 from q048_structural_runner_v6 import verify_report as operation
 return operation(*args,**kwargs)

def run(*args,**kwargs):
 from q048_structural_runner_v6 import run as operation
 return operation(*args,**kwargs)

def collect(*args,**kwargs):
 from q048_structural_runner_v6 import collect as operation
 return operation(*args,**kwargs)
