#!/usr/bin/env python3
"""Static + mandatory result gates for Q014 V6 execution repair."""
from __future__ import annotations
import argparse,json,math,subprocess
from pathlib import Path
from typing import Any
import yaml
ROOT=Path(__file__).resolve().parent
RUN="Q014-EXTERNAL-VIABILITY-V6"
QUESTION="Når den samme n=3 EDE-model anvendes, hvor stor ekstern likelihood-penalty får high-H₀-regionen omkring det aktive Q011-punkt ved H₀=71.5 km s⁻¹ Mpc⁻¹ i Planck NPIPE- og SPT-3G D1-kæderne, når hver kædes egne nuisance-parametre og relevante kosmologiske parametre profileres korrekt og datasetoverlap ikke dobbeltregnes?"
EXPECTED_MUSE="4933ceb993ceb92e48b2191b8ccb1595d182bc4bc3862c1fbad61d5f82136e9b"

def dump(p,o): Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
def sha(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def static():
    main=(ROOT/'q014_external_viability_v6.py').read_text(); setup=(ROOT/'q014_setup_v6.sh').read_text(); wf=(ROOT/'.github/workflows/q014-external-viability-v6.yml').read_text() if (ROOT/'.github/workflows/q014-external-viability-v6.yml').exists() else (ROOT/'q014-external-viability-v6.yml').read_text()
    cfg=yaml.safe_load((ROOT/'q014_external_viability_v5_config.yml').read_text())
    gates={
      'CASE_QUESTION_IDENTITY_GATE':cfg['project']['original_case_question'].strip()==QUESTION,
      'CASE_ID_NONINVENTION_GATE':cfg['project']['case_id']=='NOT DOCUMENTED',
      'V5_SCIENCE_SURFACE_REUSE_GATE':('import q014_external_viability_v5 as impl' in main and 'q014_external_viability_v5_config.yml' in main),
      'V5_CORE_SHA_GATE':sha(ROOT/'q014_external_viability_v5.py')=='94b32c67abbb8816a4b1f285b59ea54d1de7d028dd5870b4d0cb20cb5045636b',
      'V5_CONFIG_SHA_GATE':sha(ROOT/'q014_external_viability_v5_config.yml')=='95bc7aa92843fdacca956fb6f08325545a78287f8ae7b6f9c7b2cb923ebabe90',
      'V5_SETUP_SHA_GATE':sha(ROOT/'q014_setup_v5.sh')=='7c57dd6b3a35fcb5a9302dc833046c57749911fd242c8c47e6d455c2a15dfbe5',
      'MUSE_SINGLE_FETCH_GATE':('q014-v6-spt-muse-source' in wf and 'Q014_MUSE_SINGLE_FETCH_GATE=PASS' in wf and EXPECTED_MUSE in wf),
      'MUSE_REUSE_INTERCEPT_GATE':('Q014_MUSE_CURL_INTERCEPT_GATE=PASS' in setup and EXPECTED_MUSE in setup),
      'SHARED_VECTOR_MAXFUN_REPAIR_GATE':('max_evals = 960' in main and 'q011_shared_physics' in main),
      'MANDATORY_RESULT_EXIT_GATE':('exit "$TEST_RC"' in wf),
      'NO_H0DN_GATE':'h0dn' not in json.dumps(cfg['chains']).lower() and 'sh0es' not in json.dumps(cfg['chains']).lower(),
      'NO_ACT_NUISANCE_GATE':'a_act' not in json.dumps(cfg['chains']).lower() and 'p_act' not in json.dumps(cfg['chains']).lower(),
      'CHAIN_SEPARATION_GATE':cfg['claim_boundary']['planck_plus_spt_direct_chi2_sum_forbidden'] is True,
    }
    return {'q':'Q014','run_id':RUN,'test_type':'STATIC','gates':gates,'status':'PASS' if all(gates.values()) else 'FAIL'}

def result(path):
    c=yaml.safe_load((ROOT/'q014_external_viability_v5_config.yml').read_text()); r=json.loads(Path(path).read_text()); gates={}
    gates['Q_IDENTITY_GATE']=r.get('q')=='Q014' and r.get('run_id')==RUN
    gates['CASE_QUESTION_IDENTITY_GATE']=r.get('original_case_question','').strip()==QUESTION
    gates['Q011_STATUS_PRESERVATION_GATE']=r.get('q011_globality_status_preserved')=='BEST-OBSERVED MINIMUM ONLY'
    gates['NO_CROSS_CHAIN_CHI2_SUM_GATE']=r.get('planck_spt_chi2_sum_performed') is False
    gates['JOB_COMPLETENESS_GATE']=not r.get('job_manifest',{}).get('missing') and not r.get('job_manifest',{}).get('duplicates')
    gates['SOURCE_PROVENANCE_COMPATIBILITY_GATE']=r.get('job_manifest',{}).get('runtime_source_compatible') is True
    finite=stable=monotonic=True
    for name in c['validation']['required_primary_chains']:
        ch=r.get('chains',{}).get(name,{})
        for mode in ('reference_free_h0','fixed_h0_71p5','q011_shared_physics'):
            p=ch.get('profiles',{}).get(mode,{}); x=p.get('best_objective_chi2')
            finite &= x is not None and math.isfinite(float(x)); stable &= p.get('stable') is True
        monotonic &= ch.get('penalties',{}).get('fixed_profile_monotonicity_pass') is True
    gates['FINITE_RESULT_GATE']=finite; gates['MULTISTART_STABILITY_GATE']=stable; gates['FIXED_PROFILE_MONOTONICITY_GATE']=monotonic
    gates['FINAL_VALIDATION_GATE']=r.get('scientifically_usable_result') is True and r.get('validation_status')=='VALIDATED WITH CAVEATS'
    return {'q':'Q014','run_id':RUN,'test_type':'RESULT','result_id':r.get('result_id'),'gates':gates,'status':'PASS' if all(gates.values()) else 'FAIL'}

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('static'); p.add_argument('--output',required=True)
    p=sub.add_parser('result'); p.add_argument('--result',required=True); p.add_argument('--output',required=True)
    a=ap.parse_args(); rep=static() if a.cmd=='static' else result(a.result); dump(a.output,rep); print(json.dumps(rep,indent=2)); return 0 if rep['status']=='PASS' else 10
if __name__=='__main__': raise SystemExit(main())
