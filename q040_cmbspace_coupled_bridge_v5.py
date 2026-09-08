#!/usr/bin/env python3
"""Bubbleverse Q-040 — V5 controlled seal of V4 compression validation failure.

This is deliberately NOT another numerical rescue attempt. V4 successfully produced
all six preregistered variable-projection MAP states. Its compression stage then
showed two independent validity failures before any Q040 science endpoint was run:

* CamSpec: the selected mode sits on the native amp_143 hard upper bound and the
  symmetric nuisance Hessian is not positive definite.
* HiLLiPoP: the three independently converged CMB MAP representations disagree by
  normalized RMS 0.2878815..., above the frozen 0.10 compression multistart gate.

V5 validates those artifacts and seals the preregistered Outcome D:
COMPRESSION_VALIDATION_FAIL. It never weakens a threshold, modifies a native prior,
adds Hessian jitter, clips eigenvalues, chooses a convenient mode, or launches the
nine-label Q040 science endpoints.
"""
from __future__ import annotations
import argparse, json, math, os, re, sys, hashlib
from pathlib import Path
from typing import Any

Q="Q-040"
PROGRAM_ID="Q040-CMBSPACE-V5"
RUN_ID="Q040-CMBSPACE-COUPLED-BRIDGE-V5"
RESULT_ID="R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-005"
V4_PROGRAM_ID="Q040-CMBSPACE-V4"
V4_RUN_ID="Q040-CMBSPACE-COUPLED-BRIDGE-V4"
V4_RESULT_ID="R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-004"
V4_GITHUB_RUN_ID=34211073134
V4_HEAD_SHA="8790262f02a26e4e9b764790ddf2a693532c599b"
Q032_GITHUB_RUN_ID=33994305721
Q032_COMMIT="4dc873a5e880d40858d831a3b421456728f0c032"
SUPPORT_HASH="f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b"
REPRESENTATION_HASH="f96e2b9cdc27501eb0f2a6aabbf6c79c8d681f1af2d55c54b495b513c1da1f48"
START_FAMILIES=("NATIVE_REFERENCE","Q032_LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION","Q032_FARTHEST_COMPLETE_ENDPOINT_WITHIN_IMPLEMENTATION")
IMPLEMENTATIONS=("camspec","hillipop")
CAMSPEC_AMP143_UPPER=50.0
CAMSPEC_AMP143_PROPOSAL=1.0
ACTIVE_BOUND_PROPOSAL_TOL=1.0e-3
MULTISTART_CMB_RMS_MAX=0.10
MULTISTART_OBJECTIVE_SPREAD_MAX=0.50
GEOMETRY_SUFFICIENCY_THRESHOLD=0.10
EXPECTED_HILLIPOP_RMS=0.28788151156341363


def read_json(p: str|Path)->dict[str,Any]:
    d=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(d,dict): raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return d

def write_json(p: str|Path,d:Any)->None:
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding='utf-8')
    os.replace(tmp,p)

def sha256_file(p: str|Path)->str:
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def finite(x:Any)->bool:
    try:return math.isfinite(float(x))
    except:return False

def load_preregister(path: str|Path)->dict[str,Any]:
    d=read_json(path); p=d.get('project',{})
    if (p.get('q'),p.get('program_id'),p.get('run_id'),p.get('result_id')) != (Q,PROGRAM_ID,RUN_ID,RESULT_ID):
        raise RuntimeError('PREREGISTRATION_IDENTITY_GATE=FAIL')
    if float(d['decision_rules']['hillipop_multistart_cmb_normalized_rms_max']) != MULTISTART_CMB_RMS_MAX:
        raise RuntimeError('COMPRESSION_THRESHOLD_PRESERVATION_GATE=FAIL')
    if float(d['scientific_locks']['q039_geometry_sufficiency_threshold']) != GEOMETRY_SUFFICIENCY_THRESHOLD:
        raise RuntimeError('GEOMETRY_THRESHOLD_PRESERVATION_GATE=FAIL')
    return d

def load_source_lock(path: str|Path)->dict[str,Any]:
    d=read_json(path)
    if (d.get('q'),d.get('program_id')) != (Q,PROGRAM_ID): raise RuntimeError('SOURCE_LOCK_IDENTITY_GATE=FAIL')
    v4=d.get('v4_parent',{})
    if int(v4.get('github_run_id',-1)) != V4_GITHUB_RUN_ID or v4.get('head_sha') != V4_HEAD_SHA:
        raise RuntimeError('V4_PARENT_LOCK_GATE=FAIL')
    q32=d.get('q032_parent',{})
    if int(q32.get('github_run_id',-1)) != Q032_GITHUB_RUN_ID or q32.get('commit') != Q032_COMMIT or q32.get('support_sha256') != SUPPORT_HASH:
        raise RuntimeError('Q032_PARENT_LOCK_GATE=FAIL')
    return d

def collect_maps(root: str|Path)->dict[tuple[str,str],dict[str,Any]]:
    found={}
    for p in Path(root).rglob('*.json'):
        try:d=read_json(p)
        except Exception:continue
        impl=d.get('implementation'); fam=d.get('start_family')
        if impl not in IMPLEMENTATIONS or fam not in START_FAMILIES: continue
        if d.get('q')!=Q or d.get('program_id')!=V4_PROGRAM_ID or d.get('run_id')!=V4_RUN_ID or d.get('result_id')!=V4_RESULT_ID:
            raise RuntimeError(f'V4_MAP_IDENTITY_GATE=FAIL path={p}')
        if d.get('stage')!='COMPRESSION_MAP_START' or d.get('status')!='COMPLETE' or d.get('converged') is not True:
            raise RuntimeError(f'V4_MAP_COMPLETENESS_GATE=FAIL path={p}')
        if d.get('support_sha256')!=SUPPORT_HASH or d.get('representation_sha256')!=REPRESENTATION_HASH:
            raise RuntimeError(f'V4_MAP_SUPPORT_GATE=FAIL path={p}')
        key=(str(impl),str(fam))
        if key in found: raise RuntimeError(f'V4_MAP_UNIQUENESS_GATE=FAIL key={key}')
        found[key]=d
    expected={(i,f) for i in IMPLEMENTATIONS for f in START_FAMILIES}
    if set(found)!=expected: raise RuntimeError(f'V4_MAP_COMPLETENESS_GATE=FAIL keys={sorted(found)}')
    return found

def collect_failures(root: str|Path)->dict[str,dict[str,Any]]:
    out={}
    for p in Path(root).rglob('*.json'):
        try:d=read_json(p)
        except Exception:continue
        impl=d.get('implementation')
        if impl not in IMPLEMENTATIONS: continue
        if d.get('q')!=Q or d.get('program_id')!=V4_PROGRAM_ID or d.get('run_id')!=V4_RUN_ID or d.get('result_id')!=V4_RESULT_ID:
            raise RuntimeError(f'V4_FAILURE_IDENTITY_GATE=FAIL path={p}')
        if d.get('stage')!='COMPRESSION_BUILD' or d.get('status')!='COMPRESSION_BUILD_FAIL':
            continue
        if d.get('support_sha256')!=SUPPORT_HASH or d.get('representation_sha256')!=REPRESENTATION_HASH:
            raise RuntimeError(f'V4_FAILURE_SUPPORT_GATE=FAIL path={p}')
        if impl in out: raise RuntimeError(f'V4_FAILURE_UNIQUENESS_GATE=FAIL impl={impl}')
        out[str(impl)]=d
    if set(out)!=set(IMPLEMENTATIONS): raise RuntimeError(f'V4_FAILURE_COMPLETENESS_GATE=FAIL found={sorted(out)}')
    return out

def parse_hlp_rms(failure:dict[str,Any])->float:
    s=' '.join(str(failure.get(k,'')) for k in ('error','traceback'))
    m=re.search(r'cmb_normalized_rms=([0-9eE+\-.]+)',s)
    if not m: raise RuntimeError('HILLIPOP_RMS_PARSE_GATE=FAIL')
    x=float(m.group(1))
    if not finite(x): raise RuntimeError('HILLIPOP_RMS_FINITE_GATE=FAIL')
    return x

def evaluate(map_dir:str|Path,failure_dir:str|Path)->dict[str,Any]:
    maps=collect_maps(map_dir); failures=collect_failures(failure_dir)
    obj={i:[float(maps[(i,f)]['objective']) for f in START_FAMILIES] for i in IMPLEMENTATIONS}
    spread={i:max(v)-min(v) for i,v in obj.items()}
    if any(v>MULTISTART_OBJECTIVE_SPREAD_MAX for v in spread.values()):
        raise RuntimeError(f'V4_OBJECTIVE_SPREAD_PROVENANCE_GATE=FAIL spread={spread}')

    cam_gaps={f:(CAMSPEC_AMP143_UPPER-float(maps[('camspec',f)]['eta']['amp_143']))/CAMSPEC_AMP143_PROPOSAL for f in START_FAMILIES}
    if any((not finite(v)) or v < -1e-8 for v in cam_gaps.values()): raise RuntimeError(f'CAMSPEC_NATIVE_BOUND_PROVENANCE_GATE=FAIL gaps={cam_gaps}')
    cam_active=all(v<=ACTIVE_BOUND_PROPOSAL_TOL for v in cam_gaps.values())
    cam_hessian_fail='NUISANCE_HESSIAN_PD_GATE=FAIL' in (' '.join(str(failures['camspec'].get(k,'')) for k in ('error','traceback')))
    if not cam_hessian_fail: raise RuntimeError('CAMSPEC_V4_FAILURE_CLASS_GATE=FAIL')

    hlp_rms=parse_hlp_rms(failures['hillipop'])
    if abs(hlp_rms-EXPECTED_HILLIPOP_RMS)>1e-12: raise RuntimeError(f'HILLIPOP_V4_RMS_PROVENANCE_GATE=FAIL got={hlp_rms}')
    hlp_fail=hlp_rms>MULTISTART_CMB_RMS_MAX

    gates={
      'Q_IDENTITY_GATE':'PASS',
      'V4_PARENT_RUN_GATE':'PASS',
      'Q032_PARENT_LOCK_GATE':'PASS',
      'V4_SIX_MAP_COMPLETENESS_GATE':'PASS',
      'V4_MAP_SUPPORT_AND_REPRESENTATION_GATE':'PASS',
      'V4_OBJECTIVE_SPREAD_GATE':'PASS',
      'CAMSPEC_NATIVE_HARD_BOUND_DETECTION_GATE':'PASS' if cam_active else 'FAIL',
      'CAMSPEC_SYMMETRIC_LAPLACE_BOUNDARY_COMPATIBILITY_GATE':'FAIL' if cam_active else 'PASS',
      'CAMSPEC_NUISANCE_HESSIAN_PD_GATE':'FAIL' if cam_hessian_fail else 'PASS',
      'HILLIPOP_COMPRESSION_MULTISTART_GATE':'FAIL' if hlp_fail else 'PASS',
      'NO_THRESHOLD_RELAXATION_GATE':'PASS',
      'NO_HESSIAN_JITTER_OR_EIGEN_CLIPPING_GATE':'PASS',
      'NO_MODE_SELECTION_RESCUE_GATE':'PASS',
      'SCIENCE_ENDPOINT_PERMISSION_GATE':'FAIL' if (cam_active or cam_hessian_fail or hlp_fail) else 'PASS',
      'CONTROLLED_METHOD_FAILURE_SEAL_GATE':'PASS',
      'FINAL_RESULT_GATE':'UNRESOLVED' if (cam_active or cam_hessian_fail or hlp_fail) else 'FAIL',
    }
    if not (cam_active and cam_hessian_fail and hlp_fail):
        raise RuntimeError(f'V5_EXPECTED_V4_VALIDATION_SIGNATURE_GATE=FAIL cam_active={cam_active} cam_hessian_fail={cam_hessian_fail} hlp_fail={hlp_fail}')
    return {
      'cam_gaps_in_proposal_units_to_amp143_upper_bound':cam_gaps,
      'camspec_amp143_upper_bound':CAMSPEC_AMP143_UPPER,
      'camspec_active_bound_tolerance_proposal_units':ACTIVE_BOUND_PROPOSAL_TOL,
      'objective_spread':spread,
      'hillipop_cmb_normalized_rms':hlp_rms,
      'hillipop_cmb_normalized_rms_gate':MULTISTART_CMB_RMS_MAX,
      'gates':gates,
      'maps':{f'{i}:{f}':{'objective':float(maps[(i,f)]['objective']),'solver':maps[(i,f)].get('solver'),'eta':maps[(i,f)].get('eta',{})} for i in IMPLEMENTATIONS for f in START_FAMILIES},
      'failure_records':failures,
    }

def seal(args:argparse.Namespace)->int:
    load_preregister(args.preregister); load_source_lock(args.source_lock)
    ev=evaluate(args.map_dir,args.failure_dir)
    final={
      'q':Q,'program_id':PROGRAM_ID,'run_id':RUN_ID,'result_id':RESULT_ID,
      'stage':'Q040_V5_CONTROLLED_COMPRESSION_SEAL','execution_status':'COMPLETE','tests_status':'COMPLETE',
      'classification':'COMPRESSION_VALIDATION_FAIL','q040_status':'UNRESOLVED_CONTINUES',
      'final_result_gate':'UNRESOLVED','actual_q040_c036_geometry_result':False,
      'science_endpoints_executed':False,'science_endpoints_permitted':False,
      'methodological_result':{
        'camspec':'SINGLE_GAUSSIAN_SYMMETRIC_LAPLACE_NOT_VALIDATED_ON_NATIVE_BOUNDARY',
        'hillipop':'INDEPENDENTLY_CONVERGED_MAP_CMB_REPRESENTATIONS_FAIL_FROZEN_MULTISTART_STABILITY',
        'combined':'THE_V4_SINGLE_GAUSSIAN_LAPLACE_SCHUR_CMB_COMPRESSION_IS_NOT_VALIDATED_FOR_Q040_SCIENCE'
      },
      'interpretation':[
        'This is Outcome D from the Q040 research preregistration: compression validation failed before science endpoints.',
        'It does not show that C-036-IMPL survives a valid bound-aware or multimodal CMB-space marginalization.',
        'It does not show that no scientifically defensible coupled structural bridge exists.',
        'No physical Planck systematic, pipeline superiority, or new physics conclusion follows.'
      ],
      'journal_effect':{
        'action':'ADD',
        'statement':'Single-Gaussian symmetric Laplace/Schur Q040 CMB-space compression is not validated: CamSpec is boundary-limited in amp_143 and HiLLiPoP fails the frozen independent-start CMB stability gate.',
        'preserve':['C-036-IMPL ACTIVE / CAUSE UNRESOLVED','Q035 CLOSED','Q037 CLOSED','Q038 DESCRIPTIVE ONLY','Q039 CLOSED']
      },
      'next_required_action':'Preregister a mathematically explicit native-bound-aware and multimodal nuisance marginalization, or document that no such finite construction is presently defensible. Do not reuse the failed single-Gaussian Laplace assumption.',
      'next_motor':'BUBBLEVERSE — MATHEMATICS ENGINE',
      'return_route':'RESULT INGESTION & ROUTING ENGINE',
      'evidence':ev,
      'sources':['K-044','K-045/K-052','K-049','K-053','K-054','CAMSPEC_2021_ID_UNRESOLVED'],
      'provenance':{'v4_github_run_id':V4_GITHUB_RUN_ID,'v4_head_sha':V4_HEAD_SHA,'q032_github_run_id':Q032_GITHUB_RUN_ID,'q032_commit':Q032_COMMIT,'support_sha256':SUPPORT_HASH,'representation_sha256':REPRESENTATION_HASH}
    }
    handoff={
      'q':Q,'program_id':PROGRAM_ID,'result_id':RESULT_ID,'status':'CONTINUES_UNRESOLVED',
      'classification':'COMPRESSION_VALIDATION_FAIL','final_result_gate':'UNRESOLVED',
      'new_result':final['methodological_result'],'journal_effect':final['journal_effect'],
      'sources':final['sources'],'provenance':final['provenance'],'test_status':'COMPLETE',
      'unresolved_issues':['A valid native-bound-aware CamSpec nuisance marginalization remains unconstructed.','A valid multimodal/flat-direction HiLLiPoP nuisance marginalization remains unconstructed.','C-036-IMPL geometry under a validated coupled CMB-space bridge remains unknown.'],
      'next_required_action':final['next_required_action'],'next_motor':final['next_motor']
    }
    write_json(args.final_output,final); write_json(args.handoff_output,handoff)
    print('Q040_V5_CONTROLLED_SEAL_GATE=PASS classification=COMPRESSION_VALIDATION_FAIL final_result_gate=UNRESOLVED')
    return 0

def main()->int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('seal-v4')
    s.add_argument('--map-dir',required=True); s.add_argument('--failure-dir',required=True)
    s.add_argument('--preregister',required=True); s.add_argument('--source-lock',required=True)
    s.add_argument('--final-output',required=True); s.add_argument('--handoff-output',required=True)
    a=ap.parse_args()
    if a.cmd=='seal-v4': return seal(a)
    return 2
if __name__=='__main__': raise SystemExit(main())
