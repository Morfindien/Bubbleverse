#!/usr/bin/env python3
"""Q014 V8 static and mandatory result validation."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent
RUN='Q014-EXTERNAL-VIABILITY-V8'
QUESTION='Når den samme n=3 EDE-model anvendes, hvor stor ekstern likelihood-penalty får high-H₀-regionen omkring det aktive Q011-punkt ved H₀=71.5 km s⁻¹ Mpc⁻¹ i Planck NPIPE- og SPT-3G D1-kæderne, når hver kædes egne nuisance-parametre og relevante kosmologiske parametre profileres korrekt og datasetoverlap ikke dobbeltregnes?'
BASIS='SCALAR_TOTAL_LIKELIHOOD_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_CONSTRAINT_SHAPES'
MUSE='4933ceb993ceb92e48b2191b8ccb1595d182bc4bc3862c1fbad61d5f82136e9b'
def dump(p,o): Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def static():
    c=yaml.safe_load((ROOT/'q014_external_viability_v8_config.yml').read_text()); p=(ROOT/'q014_external_viability_v8.py').read_text(); w=((ROOT/'.github/workflows/q014-external-viability-v8.yml') if (ROOT/'.github/workflows/q014-external-viability-v8.yml').exists() else (ROOT/'q014-external-viability-v8.yml')).read_text(); s=(ROOT/'q014_setup_v8.sh').read_text(); cons=c['scientific_surface']['normalization_free_constraints']
    gates={
      'CASE_QUESTION_IDENTITY_GATE':c['project']['original_case_question'].strip()==QUESTION,
      'CASE_ID_NONINVENTION_GATE':c['project']['case_id']=='NOT DOCUMENTED',
      'V6_NUMERICAL_PARENT_GATE':c['parent']['v6']['github_run']==33483557343 and c['parent']['v6']['result_id']=='R-Q014-EDE-EXTERNAL-VIABILITY-003' and c['parent']['v6']['scientifically_usable_result'] is False,
      'SCALAR_TOTAL_CHI2_GATE':'row["chi2"]' in p and 'SCALAR_TOTAL_CHI2_REQUIRED' in p,
      'NO_CHI2_COMPONENT_DOUBLECOUNT_GATE':'sum(comps.values())' not in p,
      'NORMALIZATION_FREE_OBJECTIVE_GATE':'flat-prior constants' in p and 'NORMALIZATION_FREE_GAUSSIAN_CONSTRAINT_SHAPES' in p,
      'PLANCK_CONSTRAINT_SHAPE_GATE':cons['planck_npipe_k039_approx']['A_planck']['scale']==0.0025 and cons['planck_npipe_k039_approx']['calTE']['scale']==0.01 and cons['planck_npipe_k039_approx']['calEE']['scale']==0.01,
      'SPT_CONSTRAINT_SHAPE_GATE':cons['spt_d1_only']['Tcal']['scale']==0.0036 and cons['spt_d1_plus_desi']['Tcal']['scale']==0.0036,
      'DETERMINISTIC_V6_CONTINUATION_GATE':c['execution']['standard_start_families']['reference_free_h0']==['v6_free_best','v6_fixed_best'] and 'spec["ref"]=float(value)' in p,
      'CROSS_SEED_NESTING_GATE':c['execution']['standard_start_families']['fixed_h0_71p5']==['v6_fixed_best','v6_free_best'],
      'SEED_CANDIDATE_PRESERVATION_GATE':'EXACT_DETERMINISTIC_SEED' in p and 'seed_candidate_preservation_pass' in p,
      'TIGHT_LOCAL_REFINEMENT_GATE':c['execution']['minimizer']['max_evals']==960 and c['execution']['minimizer']['override_bobyqa']['rhoend']==0.005,
      'MUSE_FROZEN_REUSE_GATE':MUSE in w and 'q014-v8-spt-muse-source' in w and 'q014_setup_v6.sh' in s,
      'V6_MUSE_ARTIFACT_PROVENANCE_GATE':'9790864493' in w and 'sha256:03446830394786015fc512f76c6c298719487816eb93c77554d31c16f1d862ca' in w and 'q014-v6-spt-muse-source' in w,
      'V6_PARENT_ARTIFACT_PROVENANCE_GATE':'9795008419' in w and 'sha256:efe77e9bd2a4550299b1488f12e5e6eb851d6af906c372f845b226c6f35a0b4c' in w and '--v6-result' in w,
      'V5_REPOSITORY_BLOB_IDENTITY_GATE':all(x in w for x in ['f5fa9cc237b2fc8a28bf8561b1471d885072dc01','0f2c9caef194bcee3ee8f7895f8ef2ea9ab8b71b','e67e713de478e00340fbbc5b3b4e1e00e0406ef1','git rev-parse \"HEAD:$file\"','git hash-object \"$file\"']),
      'PREPARE_FAILURE_AGGREGATE_SUPPRESSION_GATE':"always() && needs.prepare.result == 'success'" in w,
      'GITHUB_ACTION_VERSION_GATE':'actions/checkout@v5' in w and 'actions/setup-python@v5' in w and 'actions/download-artifact@v5' in w and 'actions/upload-artifact@v5' in w and 'actions/checkout@v8' not in w and 'actions/setup-python@v8' not in w,
      'MANDATORY_RESULT_EXIT_GATE':'exit "$TEST_RC"' in w,
      'NO_H0DN_GATE':'h0dn' not in json.dumps(c['chains']).lower() and 'sh0es' not in json.dumps(c['chains']).lower(),
      'NO_ACT_NUISANCE_GATE':'a_act' not in json.dumps(c['chains']).lower() and 'p_act' not in json.dumps(c['chains']).lower(),
      'CHAIN_SEPARATION_GATE':c['claim_boundary']['planck_plus_spt_direct_chi2_sum_forbidden'] is True,
      'N3_MODEL_GATE':c['scientific_surface']['model']=='ede_n3' and c['scientific_surface']['n_scf']==3,
    }
    return {'q':'Q014','run_id':RUN,'test_type':'STATIC','gates':gates,'status':'PASS' if all(gates.values()) else 'FAIL'}
def result(path):
    c=yaml.safe_load((ROOT/'q014_external_viability_v8_config.yml').read_text()); r=json.loads(Path(path).read_text()); g={}
    g['Q_IDENTITY_GATE']=r.get('q')=='Q014' and r.get('run_id')==RUN and r.get('result_id')=='R-Q014-EDE-EXTERNAL-VIABILITY-005'
    g['CASE_QUESTION_IDENTITY_GATE']=r.get('original_case_question','').strip()==QUESTION
    g['Q011_STATUS_PRESERVATION_GATE']=r.get('q011_globality_status_preserved')=='BEST-OBSERVED MINIMUM ONLY'
    g['V6_NUMERICAL_PARENT_GATE']=r.get('v6_numerical_parent',{}).get('github_run')==33483557343 and r.get('v6_numerical_parent',{}).get('scientifically_usable_result') is False
    g['NO_CROSS_CHAIN_CHI2_SUM_GATE']=r.get('planck_spt_chi2_sum_performed') is False
    jm=r.get('job_manifest',{}); g['JOB_COMPLETENESS_GATE']=jm.get('expected')==15 and jm.get('returned')==15 and not jm.get('missing') and not jm.get('duplicates')
    g['SOURCE_PROVENANCE_COMPATIBILITY_GATE']=jm.get('runtime_source_compatible') is True
    finite=stable=mono=seed=basis=True
    for name in c['validation']['required_primary_chains']:
        ch=r.get('chains',{}).get(name,{})
        for mode in ('reference_free_h0','fixed_h0_71p5','q011_shared_physics'):
            pr=ch.get('profiles',{}).get(mode,{}); x=pr.get('best_objective_chi2'); finite &= x is not None and math.isfinite(float(x)); stable &= pr.get('stable') is True; seed &= pr.get('seed_candidate_preservation_pass') is True
            br=pr.get('best_record') or {}; basis &= br.get('objective_basis')==BASIS and br.get('likelihood_chi2_scalar') is not None
        mono &= ch.get('penalties',{}).get('fixed_profile_monotonicity_pass') is True
    g['FINITE_RESULT_GATE']=finite; g['MULTISTART_STABILITY_GATE']=stable; g['FIXED_PROFILE_MONOTONICITY_GATE']=mono; g['SEED_CANDIDATE_PRESERVATION_GATE']=seed; g['NORMALIZATION_FREE_OBJECTIVE_GATE']=basis
    g['FINAL_VALIDATION_GATE']=r.get('scientifically_usable_result') is True and r.get('validation_status')=='VALIDATED WITH CAVEATS'
    return {'q':'Q014','run_id':RUN,'test_type':'RESULT','result_id':r.get('result_id'),'gates':g,'status':'PASS' if all(g.values()) else 'FAIL'}
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); a=sub.add_parser('static'); a.add_argument('--output',required=True); b=sub.add_parser('result'); b.add_argument('--result',required=True); b.add_argument('--output',required=True); x=ap.parse_args(); rep=static() if x.cmd=='static' else result(x.result); dump(x.output,rep); print(json.dumps(rep,indent=2)); return 0 if rep['status']=='PASS' else 10
if __name__=='__main__': raise SystemExit(main())
