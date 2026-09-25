#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

Q='Q-042'; PROGRAM_ID='Q042-PROD-V1'; WORKFLOW='.github/workflows/q042-production-v1.yml'

def read(p):
    x=json.loads(Path(p).read_text(encoding='utf-8'))
    if not isinstance(x,dict): raise RuntimeError(f'JSON_OBJECT_GATE=FAIL {p}')
    return x

def write(p,x):
    Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def static(a):
    spec=read(a.spec); lock=read(a.source_lock); patch=read(a.registry_patch)
    pr=Path(a.program).read_text(encoding='utf-8'); wf=Path(a.workflow).read_text(encoding='utf-8'); sh=Path(a.setup).read_text(encoding='utf-8')
    ent=patch.get('patch',{}).get(PROGRAM_ID,{})
    seeds=spec.get('polychord_seed_map',{})
    pc=spec.get('polychord_production',{}); bq=spec.get('bobyqa_production',{}); orch=spec.get('orchestration',{})
    # This catches the prior race: each continuation dispatch must textually occur after its checkpoint upload step.
    first_upload=wf.find("name: q042-prod-${{ github.run_id }}-checkpoint-")
    first_dispatch=wf.find('name: Dispatch continuation after checkpoint upload')
    cont_upload=wf.find("name: q042-prod-${{ inputs.root_run_id }}-checkpoint-")
    cont_dispatch=wf.find('name: Dispatch continuation after checkpoint upload', first_dispatch+1)
    gates={
      'Q_IDENTITY': spec.get('q')==Q and spec.get('program_id')==PROGRAM_ID and lock.get('q')==Q and lock.get('program_id')==PROGRAM_ID,
      'SPEC_HASH': lock.get('spec_sha256')==sha(a.spec),
      'V11_PARENT': spec.get('preflight_authority',{}).get('program_id')=='Q042-PREFLIGHT-V11' and spec.get('preflight_authority',{}).get('final_result_gate')=='PREFLIGHT_PASS',
      '20_CELL_SURFACE': spec.get('authoritative_contract',{}).get('required_cell_count')==20 and len(spec.get('authoritative_contract',{}).get('arms',[]))==2 and len(spec.get('authoritative_contract',{}).get('models',[]))==2 and len(spec.get('authoritative_contract',{}).get('data_combinations',{}))==5,
      '20_UNIQUE_SEEDS': len(seeds)==20 and len(set(seeds.values()))==20,
      'POLYCHORD_FROZEN': all([pc.get('nlive')=='25d',pc.get('num_repeats')=='5d',pc.get('nprior')=='10nlive',pc.get('nfail')=='nlive',pc.get('precision_criterion')==0.001,pc.get('max_ndead')=='infinity',pc.get('read_resume') is True,pc.get('write_resume') is True]),
      'BOBYQA_FROZEN': bq.get('external_starts_per_cell')==4 and bq.get('cobaya_best_of')==1 and bq.get('ignore_prior') is True and bq.get('max_evals')=='120d' and bq.get('rhoend')==0.05,
      'Q040_FIREWALL': spec.get('authoritative_contract',{}).get('q040_scientific_endpoints_forbidden') is True and spec.get('analysis_preregister',{}).get('no_q040_endpoints') is True,
      'NO_CROSS_ARM_ABSOLUTE_OBJECTIVE': spec.get('analysis_preregister',{}).get('no_cross_arm_absolute_objective') is True,
      'NO_GAUSSIAN_COMPRESSION': 'no Gaussian compression' in json.dumps(spec),
      'POLYCHORD_COMMIT_LOCK': lock.get('software',{}).get('polychordlite_exact_commit')=='3ade6445bb3719a6db6f6e81f178765545ffc833' and "POLYCHORD_EXACT_COMMIT_GATE=FAIL" in sh,
      'MAX_NDEAD_INFINITY_ADAPTER': 'float("inf")' in pr and lock.get('technical_adapters',{}).get('polychord_max_ndead_infinity_encoding',{}).get('scientific_setting_changed') is False,
      'CAMPAIGN_RUNTIME_IDENTITY': wf.count('Q042_PROD_CAMPAIGN_RUNTIME_IDENTITY_GATE=PASS')==3 and 'pantheonplus_manifest_sha256' in wf,
      'Q032_LOCK': lock.get('q032',{}).get('execution_commit')=='4dc873a5e880d40858d831a3b421456728f0c032',
      'CLASS_EDE_LOCK': lock.get('software',{}).get('class_ede_commit')=='5a131c91d657dd9a7c6364cc45b038710f8d0d97',
      'HILLIPOP_LOCK': lock.get('software',{}).get('hillipop_commit')=='a09ddde3e7ce11df99f74685feb1f1764cafb251',
      'SEGMENT_BUDGET': int(orch.get('soft_polychord_segment_minutes',999)) < int(orch.get('job_timeout_minutes',0)) < int(orch.get('github_hosted_job_hard_limit_minutes',0)),
      'WORKFLOW_MODES': all(x in wf for x in ("inputs.mode == 'bootstrap'","inputs.mode == 'segment'","inputs.mode == 'collect'")),
      'ACTIONS_WRITE_FOR_SELF_DISPATCH': re.search(r'permissions:\s*\n\s+contents:\s*read\s*\n\s+actions:\s*write',wf) is not None,
      'CHECKPOINT_BEFORE_FIRST_DISPATCH': first_upload!=-1 and first_dispatch!=-1 and first_upload < first_dispatch,
      'CHECKPOINT_BEFORE_CONTINUATION_DISPATCH': cont_upload!=-1 and cont_dispatch!=-1 and cont_upload < cont_dispatch,
      'TRUE_RESUME': "--action\",action" in pr and 'COBAYA_STORED_UPDATED_INFO' in pr and 'OutputReadOnly' in pr,
      'BOBYQA_ATOMIC': 'one external start per job' in json.dumps(spec).lower() and 'start_index' in pr,
      'BOBYQA_FULL_DIMENSION_120D': "d=sum(1 for v in info.get(\"params\",{}).values()" in pr and 'maxeval=int(str(bq["max_evals"]).removesuffix("d"))*d' in pr,
      'COLLECTOR_EXPECTS_100': "exp.append(f'q042-prod-{root}-polychord-final" in wf and 'for s in range(4)' in wf and "arms=['camspec','hillipop']" in wf and "mods=['lcdm','ede_n3']" in wf and "cs=['FULL','NO_ACT_PRIMARY','NO_ACT_LENSING','NO_DESI_DR2','NO_SN']" in wf,
      'COLLECTOR_BOUNDED': int(orch.get('max_collector_rounds',0))>0 and 'COLLECTOR_MAX_ROUNDS_WITH_MISSING_ARTIFACTS' in wf,
      'FINAL_3_CLASSES': set(spec.get('final_classes',[]))=={'MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE','SCIENTIFIC_DIFFERENCE_COLLAPSES','MIXED_DATASET_CONDITIONAL'},
      'NO_FORCED_MIXED': 'PRODUCTION_COMPLETE_CLASSIFICATION_RULES_DO_NOT_RESOLVE' in pr and 'else:classification="NOT_AVAILABLE"' in pr,
      'OVERLAP_STABILITY': spec.get('analysis_preregister',{}).get('overlap_primary_bins')==[80,80] and spec.get('analysis_preregister',{}).get('overlap_stability_bins')==[[64,64],[96,96]],
      'REGISTRY_ENTRY': ent.get('q')==Q and ent.get('status')=='ACTIVE' and ent.get('workflow_path')==WORKFLOW and ent.get('workflow_id')=='q042-production-v1.yml',
      'PERMANENT_LAUNCHER_UNCHANGED': ent.get('launcher')=='.github/workflows/00-bubbleverse-start.yml',
      'SETUP_REUSES_V11': 'q042_setup_v11.sh' in sh,
      'NO_GITHUB_MUTATION_BY_ASSISTANT': lock.get('hard_rules',{}).get('github_mutation_by_assistant_forbidden') is True,
    }
    status='PASS' if all(gates.values()) else 'FAIL'
    write(a.output,{'q':Q,'program_id':PROGRAM_ID,'stage':'PRODUCTION_STATIC_TESTS','status':status,'gates':{k:'PASS' if v else 'FAIL' for k,v in gates.items()}})
    if status!='PASS':
        print(json.dumps({k:v for k,v in gates.items() if not v},indent=2)); raise SystemExit(2)
    print(f'Q042_PROD_V1_STATIC_TEST_GATE=PASS gates={len(gates)}')

def parser():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); s=sp.add_parser('static')
    for x in ('spec','source-lock','program','workflow','setup','registry-patch','output'): s.add_argument('--'+x,required=True)
    s.set_defaults(func=static); return p
if __name__=='__main__':
    a=parser().parse_args(); a.func(a)
