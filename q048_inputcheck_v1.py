#!/usr/bin/env python3
"""Q-048 pinned metadata admission, not a trajectory solver or no-hit proof.

Exact JSON/hex/hash ingestion is reused from q047_collection_v1.py at
Morfindien/Bubbleverse commit 76d6b4a4b02ddd929899008f476e99da29c1f931,
blob c5f6739da36b68c01dab5c720cf0d948c25eb2dd. Native code is never loaded.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import re
import struct
import sys
import time

Q = 'Q-048'
ID = 'Q048-INPUTCHECK-V1'
CONTRACT_SHA = 'feabddeaec3b178c299b21548284150f26403f4cdbab2d69ee112a48a7ac5faf'
MEMBERS = {'worker_result.json':'worker', 'effective_background_hex.json':'background',
    'effective_precision.json':'precision', 'thermal_starts_hex.jsonl':'thermal',
    'native_data.json':'native_data'}
PHASES = {'brec':0,'He1':1,'He1f':2,'He2':3,'H':4,'frec':5,'reio':6}
HEX = re.compile(r'-?0x[0-9a-f]+(?:\.[0-9a-f]*)?p[+-]?[0-9]+\Z')

class GateError(ValueError): pass
def need(value, reason):
    if not value: raise GateError(reason)
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'DUPLICATE_JSON_KEY '+k); out[k]=v
    return out
def decode(s):
    return json.loads(s,object_pairs_hook=unique,
        parse_constant=lambda s:(_ for _ in ()).throw(GateError('NONFINITE_JSON '+s)))
def read(path): return decode(Path(path).read_text(encoding='utf-8'))
def write(path,data):
    with Path(path).open('x',encoding='utf-8') as f:
        json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False); f.write('\n')
def bits(x): return struct.pack('>d',x)
def native(s):
    need(isinstance(s,str) and len(s)<=128 and HEX.fullmatch(s),'HEX_ENCODING')
    try: x=float.fromhex(s)
    except (ValueError,OverflowError) as e: raise GateError('HEX_ENCODING') from e
    need(math.isfinite(x),'NONFINITE_HEX')
    mantissa,power=s.lstrip('-')[2:].split('p')
    digits=mantissa.replace('.','')
    after=len(mantissa.split('.')[1]) if '.' in mantissa else 0
    exact=Fraction((-1 if s.startswith('-') else 1)*int(digits,16))*Fraction(2)**(int(power)-4*after)
    need(Fraction.from_float(x)==exact,'HEX_NOT_EXACT_BINARY64')
    return x
def exact(s): return Fraction.from_float(native(s))
def rational(x): return {'num':str(x.numerator),'den':str(x.denominator)}
def verified_member(root,name,digest,size):
    rel=PurePosixPath(name)
    need(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name,'MEMBER_PATH')
    root=Path(root).absolute(); p=root
    need(not root.is_symlink(),'ROOT_SYMLINK')
    for part in rel.parts:
        p=p/part; need(not p.is_symlink(),'MEMBER_SYMLINK')
    need(p.is_file() and p.stat().st_size==size,'MEMBER_SIZE '+name)
    need(sha(p)==digest,'MEMBER_HASH '+name)
    return p

def validate_case(case,d,c):
    w,b,precision,rows,nd=(d[k] for k in ['worker','background','precision','thermal','native_data'])
    for k,v in c['worker_identity'].items():
        need(type(w.get(k)) is type(v) and w.get(k)==v,'WORKER_IDENTITY '+k)
    need(w.get('case')==case,'WORKER_CASE')
    need(w.get('execution_status')=='CAPTURE_COMPLETE' and type(w.get('native_processes_started')) is int
         and w.get('native_processes_started')==1,
         'CAPTURE_INCOMPLETE')
    need(w.get('final_result_gate')=='UNRESOLVED' and w.get('scientific_verdict')=='INSUFFICIENT_EVIDENCE',
         'HISTORICAL_SCIENTIFIC_PROMOTION')
    for filename,spec in c['cases'][case]['members'].items():
        if filename!='worker_result.json': need(w['files'].get(filename)==spec['sha256'],'WORKER_MEMBER '+filename)
    for name,digest in c['source_member_sha256'].items(): need(w['files'].get(name)==digest,'SOURCE_MANIFEST '+name)
    need(b['schema']=='Q047_CAPTURE_V1' and b['case']==case and b['origin']=='NEW_RECONSTRUCTION',
         'BACKGROUND_CONTEXT')
    need(b['number_encoding']=='C99_hex_binary64','BACKGROUND_ENCODING')
    need(bits(native(b['z_reio']))==bits(native(c['cases'][case]['accepted_z_reio'])),'ACCEPTED_Z_REIO')
    tf=b['thermal_flags']
    need(set(tf)=={'has_varconst','has_exotic_injection','has_idm_b','has_idm_g','has_idm_dr','recombination'},
         'THERMAL_FLAG_SET')
    need(all(type(v) is int and v==(1 if k=='recombination' else 0) for k,v in tf.items()),
         'UNSUPPORTED_THERMAL_VARIANT')
    need(set(precision)==set(c['precision_names']),'PRECISION_FIELD_COVERAGE')
    for name in c['precision_hex_names']: native(precision[name])
    need(len(rows)==7,'THERMAL_PHASE_COUNT')
    last=None; first=rows[0]; summary=[]
    for i,row in enumerate(rows):
        need(row['schema']=='Q047_CAPTURE_V1' and row['case']==case and row['origin']=='NEW_RECONSTRUCTION'
             and row['number_encoding']=='C99_hex_binary64','THERMAL_CONTEXT')
        need(type(row['event']) is int and row['event']==i+1 and row['phase_indices']==PHASES
             and type(row['phase']) is int and row['phase']==i,'THERMAL_SEQUENCE')
        mz=exact(row['mz']); need(mz<=0 and (last is None or mz>last),'THERMAL_CHRONOLOGY'); last=mz
        need(all(type(row[k]) is int and row[k] in (0,1) for k in ['require_H','require_He']),
             'THERMAL_REQUIRE_FLAGS')
        ids=[row['D_index']]+[row[key] for flag,key in [('require_H','H_index'),('require_He','He_index')] if row[flag]]
        y=[exact(v) for v in row['y']]
        need(len(set(ids))==len(ids)==len(y) and all(type(j) is int and 0<=j<len(y) for j in ids),
             'THERMAL_VECTOR_MAPPING')
        need(set(row['constants'])==set(c['thermal_constant_names']),'THERMAL_CONSTANT_SET')
        need(row['constants']==first['constants'],'CHANGING_THERMAL_CONSTANTS')
        need(all(exact(v)>0 for v in row['constants'].values()),'THERMAL_CONSTANT_DOMAIN')
        need(bits(native(row['constants']['fHe_CLASS']))==bits(native(row['constants']['fHe_HyRec'])),
             'HELIUM_NORMALIZATION')
        need(bits(native(row['constants']['Tcmb']))==bits(native(b['fields']['T_cmb'])),'TCMB_LINK')
        need(type(row['HyRec_error']) is int and row['HyRec_error']==0 and
             type(row['HyRec_MODEL']) is int and row['HyRec_MODEL']==4,'HYREC_VARIANT')
        need(row['ap_limits']==first['ap_limits'] and row['ap_deltas']==first['ap_deltas'],
             'CHANGING_PHASE_BOUNDARIES')
        lim=[exact(v) for v in row['ap_limits']]; wid=[exact(v) for v in row['ap_deltas']]
        need(len(lim)==len(wid)==7 and lim[-1]==0 and all(a>b for a,b in zip(lim,lim[1:]))
             and all(v>=0 for v in wid),'PHASE_BOUNDARY_DOMAIN')
        if i: need(mz==-lim[i-1],'PHASE_BOUNDARY_LINK')
        item={'event':i+1,'phase':i,'mz_hex':row['mz'],'native_y_hex':row['y']}
        if row['require_He']:
            q=exact(row['y'][row['He_index']]); f=exact(row['constants']['fHe_CLASS'])
            item.update(x_He_native=rational(q),q_xHeII=rational(q*f),
                        q_minus_exact_epsilon=rational(q*f-Fraction(1,10**6)),
                        q_xHeII_vs_exact_epsilon='ABOVE' if q*f>Fraction(1,10**6) else 'AT_OR_BELOW',
                        semantics='CLASS vector x_He is abundance per helium; q=fHe*x_He per hydrogen')
        summary.append(item)
    need(exact(first['y'][first['D_index']])==0,'EARLY_THERMAL_INITIAL_D')
    need(len(nd)==8 and all(v['saved_as'] in w['files'] and w['files'][v['saved_as']]==v['sha256']
                           for v in nd.values()),'RATE_DATA_MANIFEST_LINK')
    late=[r for r in rows if r['phase'] in (5,6)]
    qhex=[r['y'][r['He_index']] for r in late]
    return {'metadata_gate':'PASS','phase_start_records':summary,'thermal_start_events':len(rows),
        'accepted_z_reio_hex':b['z_reio'],'late_phase_samples':{
            'x_He_at_frec':qhex[0],'x_He_at_reio':qhex[1],
            'same_binary64_x_He':bits(native(qhex[0]))==bits(native(qhex[1])),
            'q_at_frec':rational(exact(qhex[0])*exact(first['constants']['fHe_CLASS'])),
            'q_at_reio':rational(exact(qhex[1])*exact(first['constants']['fHe_CLASS']))},
        'rate_data_manifest_gate':'PASS_DECLARATIONS_ONLY',
        'source_manifest_gate':'PASS_DECLARATIONS_ONLY',
        'reionization_effective_fields_gate':'UNRESOLVED_NOT_IN_CHECKED_METADATA',
        'continuous_no_hit_gate':'UNRESOLVED', 'first_hit_gate':'UNRESOLVED',
        'full_history_gate':'UNRESOLVED','final_result_gate':'UNRESOLVED',
        'scope':'Five metadata files only; source/data payloads and trajectories are not validated here'}

def audit(root,c):
    start=time.monotonic(); cases={}; failed=[]; links=[]
    for name,spec in c['cases'].items():
        try:
            data={}; local=[]
            for filename,pin in spec['members'].items():
                p=verified_member(root,name+'/'+filename,pin['sha256'],pin['bytes'])
                data[MEMBERS[filename]]=[decode(s) for s in p.read_text().splitlines()] if filename.endswith('.jsonl') else read(p)
                local.append({'case':name,'member':filename,'sha256':pin['sha256'],'bytes':pin['bytes']})
            cases[name]=validate_case(name,data,c); links.extend(local)
        except (GateError,KeyError,TypeError,ValueError,OSError) as e:
            failed.append(name); cases[name]={'metadata_gate':'FAIL','failure':str(e),'final_result_gate':'UNRESOLVED'}
    return {'schema':'Q048_INPUTCHECK_RESULT_V1','q':Q,'q_assignment':'PROPOSED_UNVERIFIED',
        'program_id':ID,'scientific_question':c['scientific_question'],'question_sha256':c['question_sha256'],
        'source_run_id':c['worker_identity']['run_id'],'source_execution_commit':c['worker_identity']['execution_commit'],
        'current_execution_commit':os.environ.get('GITHUB_SHA','LOCAL_UNCOMMITTED'),
        'current_run_id':os.environ.get('GITHUB_RUN_ID','LOCAL'),
        'execution_status':'COMPLETE' if not failed else 'PARTIAL',
        'job_completeness_gate':'PASS' if not failed else 'FAIL',
        'metadata_gate':'PASS' if not failed else 'FAIL','final_result_gate':'UNRESOLVED',
        'actual_xe_history_bounds':'NOT_COMPUTED','actual_tau_T_bounds':'NOT_COMPUTED',
        'cases':cases,'failed_cases':failed,'verified_members':links,
        'seconds':time.monotonic()-start,'python':platform.python_version(),
        'checked_utc':datetime.now(timezone.utc).isoformat(),
        'new_native_processes':0,'new_likelihood_evaluations':0,
        'next_required_action':'Qualify the common continuous first event or no reach before paired completion integration',
        'return_route':'RESULT INGESTION & ROUTING ENGINE'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root',type=Path,required=True,help='Directory containing the four case directories')
    ap.add_argument('--contract',type=Path,default=Path(__file__).with_name('Q048_INPUTCHECK_CONTRACT_V1.json'))
    ap.add_argument('--program-id',default=ID); ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    need(args.program_id==ID,'PROGRAM_ID_GATE')
    need(sha(args.contract)==CONTRACT_SHA,'CONTRACT_HASH')
    c=read(args.contract); need(c['q']==Q and c['program_id']==ID,'CONTRACT_CONTEXT')
    out=audit(args.input_root,c); out['contract_sha256']=sha(args.contract); out['program_sha256']=sha(__file__)
    args.output.parent.mkdir(parents=True,exist_ok=True); write(args.output,out)
    print(json.dumps({k:out[k] for k in ['q','program_id','execution_status','metadata_gate','final_result_gate','seconds']}))
    return 0 if out['metadata_gate']=='PASS' else 2

if __name__=='__main__':
    try: sys.exit(main())
    except (GateError,OSError) as e: print('INPUTCHECK_GATE=FAIL '+str(e),file=sys.stderr); sys.exit(2)
