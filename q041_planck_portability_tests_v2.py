#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, re, sys

Q='Q-041'; PID='Q041-PLANCKPORT-V2'; RID='R-Q041-EDE-DOWNSTREAM-PORTABILITY-002'
BASE=['P','P_A6','P_L6','P_D2','P_A6_L6_D2']; LOO=['P_L6_D2','P_A6_D2','P_A6_L6']

def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def dump(p,x): pathlib.Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def static(a):
    pre=load(a.preregister); src=load(a.source_lock); reg=load(a.registry)
    assert pre['q']==Q and pre['program_id']==PID and pre['result_id']==RID
    assert pre['baseline_combinations']==BASE and pre['leave_one_out_combinations']==LOO
    assert pre['hard_rules']['q040_scientific_dependency_forbidden'] is True
    assert pre['inference']['hard_science_rhat_gate']==1.05
    assert src['bubbleverse']['q032_execution_commit']=='4dc873a5e880d40858d831a3b421456728f0c032'
    assert src['bubbleverse']['cobaya_version']=='3.5.6'
    assert src['external']['act_dr6_cmbonly']['commit']=='880eacb40d66722eb1c32d7b5621e91662b4d808'
    assert src['external']['act_dr6_lensing']['commit']=='b386ddbb5821c1216c709f051c9289292f174d30'
    assert src['external']['desi_dr2']['bao_data_commit']=='b7b8a36e9bccb063081f811f323cada21ab5fbdd'
    ent=reg['programs'][PID]
    assert ent['q']==Q and ent['status']=='ACTIVE' and ent['workflow_id']=='q041-planck-portability-v2.yml'
    assert ent['scientific_program']=='q041_planck_portability_v2.py'
    wf=pathlib.Path(a.workflow).read_text(encoding='utf-8')
    for token in [PID,'prepare-nonoverlap','runtime-preflight','P_A6_L6_D2','P_L6_D2','P_A6_D2','P_A6_L6','aggregate']:
        assert token in wf,token
    assert 'Q040-RQMC' not in wf and 'Q040-CMBSPACE' not in wf
    program=pathlib.Path(a.program).read_text(encoding='utf-8')
    assert 'PLANCK_NONOVERLAP_MAX=599' in program and 'ACT_ELL_MIN=600' in program
    assert 'no_hybrid_planck_likelihood' in pathlib.Path(a.preregister).read_text(encoding='utf-8')
    out={'q':Q,'program_id':PID,'stage':'STATIC_TESTS','status':'PASS','gates':{
        'IDENTITY':'PASS','REGISTRY':'PASS','WORKFLOW_ROUTING':'PASS','Q032_FREEZE':'PASS','Q040_FIREWALL':'PASS',
        'EXTERNAL_SOURCE_LOCK':'PASS','NONOVERLAP_POLICY':'PASS','CLASSIFICATION_LOCK':'PASS'}}
    dump(a.output,out); print('Q041_STATIC_TEST_GATE=PASS'); return 0

def final(a):
    d=load(a.final)
    assert d['q']==Q and d['program_id']==PID and d['result_id']==RID
    assert d['stage']=='FINAL' and d['status']=='PASS' and d['actual_computed_result'] is True
    assert d['scientific_classification'] in ['MATERIAL_DOWNSTREAM_DIFFERENCE','SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS','CONSTRAINED_MIXED']
    assert all(v=='PASS' for v in d['required_gates'].values())
    for c in BASE+LOO:
        x=d['comparisons'][c]
        assert 0.0 <= float(x['gaussian_bhattacharyya_coefficient']) <= 1.0
        assert float(x['max_standardized_shift']) >= 0.0
    dump(a.output,{'q':Q,'program_id':PID,'stage':'FINAL_TESTS','status':'PASS','classification':d['scientific_classification']})
    print('Q041_FINAL_TEST_GATE=PASS'); return 0

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
    x=s.add_parser('static')
    for k in ['preregister','source-lock','registry','workflow','program','output']: x.add_argument('--'+k,required=True)
    x.set_defaults(func=static)
    x=s.add_parser('final'); x.add_argument('--final',required=True); x.add_argument('--output',required=True); x.set_defaults(func=final)
    a=p.parse_args(); return a.func(a)
if __name__=='__main__': raise SystemExit(main())
