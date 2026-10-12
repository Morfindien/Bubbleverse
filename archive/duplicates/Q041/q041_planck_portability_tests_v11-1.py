#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, re, sys

Q='Q-041'; PID='Q041-PLANCKPORT-V11'; RID='R-Q041-EDE-DOWNSTREAM-PORTABILITY-011'
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
    assert ent['q']==Q and ent['status']=='ACTIVE' and ent['workflow_id']=='q041-planck-portability-v11.yml'
    assert ent['scientific_program']=='q041_planck_portability_v11.py'
    wf=pathlib.Path(a.workflow).read_text(encoding='utf-8')
    for token in [PID,'q041_prepare_frozen_core_v11.sh','prepare-nonoverlap','runtime-preflight','P_A6_L6_D2','P_L6_D2','P_A6_D2','P_A6_L6','aggregate']:
        assert token in wf,token
    assert 'Q040-RQMC' not in wf and 'Q040-CMBSPACE' not in wf
    # Immutable authoritative Q032 parent must remain V2 even when Q041 revisions advance.
    for token in [
        'q032-preflight-sealed-v2',
        'q032-hillipop-covariance-v2',
        'q032_preflight_sealed_v2.json',
        'q032_hillipop_tt3pair_precision_v2.npy',
        'q032_hillipop_tt3pair_precision_v2.json',
    ]:
        assert token in wf, token
    for forbidden in [
        'q032-preflight-sealed-v3','q032-preflight-sealed-v4',
        'q032-hillipop-covariance-v3','q032-hillipop-covariance-v4',
        'q032_preflight_sealed_v3.json','q032_preflight_sealed_v4.json',
        'q032_hillipop_tt3pair_precision_v3.npy','q032_hillipop_tt3pair_precision_v4.npy',
    ]:
        assert forbidden not in wf, forbidden
    program=pathlib.Path(a.program).read_text(encoding='utf-8')
    setup=pathlib.Path('q041_setup_v11.sh').read_text(encoding='utf-8')
    core=pathlib.Path('q041_prepare_frozen_core_v11.sh').read_text(encoding='utf-8')
    assert 'PLANCK_NONOVERLAP_MAX=599' in program and 'ACT_ELL_MIN=600' in program
    assert 'q032_planck_tt3pair_bridge_v2' in program
    assert 'q032_planck_tt3pair_bridge_v2_config.yml' in program
    assert 'q32.load_cfg(Path(root).resolve()/"q032_planck_tt3pair_bridge_v2_config.yml")' in program
    assert 'q32.load_cfg(Path(root)/"q032_planck_tt3pair_bridge_v2_config.yml")' not in program
    assert 'q032_planck_tt3pair_bridge_v3' not in program
    assert 'q032_planck_tt3pair_bridge_v4' not in program
    assert 'external/bao_data_v2_6' in setup
    assert 'external/bao_data_v3_6' not in setup
    assert 'printf \'%s\' \'v2.6\' > "$COBAYA_PACKAGES_PATH/data/bao_data/version.dat"' in setup
    assert 'Q041_DESI_DR2_COBAYA_VERSION_METADATA_GATE=PASS' in setup
    assert 'desi_bao_all.is_installed(path=packages, show_error=True) is True' in setup
    assert 'q041_chain_metadata_v11.json' in program
    assert 'q041_chain_metadata_v7.json' not in program
    assert program.count('q041_chain_metadata_v11.json') == 2
    assert 'Restore prior V10 full environment cache' in wf
    assert 'https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz' in setup
    assert 'Q041_ACT_CMB_LAMBDA_DATA_GATE=PASS' in setup
    assert 'cobaya-install act_dr6_cmbonly -p "$COBAYA_PACKAGES_PATH"' not in setup
    assert 'https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr6/likelihood/data/ACT_dr6_likelihood_v1.2.tgz' in setup
    assert 'Q041_ACT_LENS_LAMBDA_DATA_GATE=PASS' in setup
    assert 'cobaya-install act_dr6_lenslike.ACTDR6LensLike -p "$COBAYA_PACKAGES_PATH"' not in setup
    assert '627aeafb88ae5ad1aa66b406bea2d65cfa66a27d' in setup
    assert 'tar -tzf "$archive" | grep' not in setup
    assert 'tar -tzf "$archive" > "$tmp/act_cmb_archive.list"' in setup
    assert 'grep -qx \'v1.0/dr6_data_cmbonly.fits\' "$tmp/act_cmb_archive.list"' in setup
    assert 'tar -tzf "$archive" > "$tmp/act_lens_archive.list"' in setup
    assert 'grep -q \'^v1.2/\' "$tmp/act_lens_archive.list"' in setup
    assert 'name: q041-chain-${{ matrix.implementation }}-${{ matrix.combo }}-c${{ matrix.chain }}-v11' in wf
    assert 'pattern: q041-chain-*-v11' in wf
    assert 'q041-chain-${{ matrix.implementation }}-${{ matrix.combo }}-c${{ matrix.chain }}-v3' not in wf
    assert 'pattern: q041-chain-*-v6' not in wf
    assert wf.count('actions/cache/save@v4') >= 2
    assert 'q041-v11-q032core-' in wf
    assert 'fail-on-cache-miss: true' in wf
    assert 'Q041_NERSC_TT_AVAILABILITY_GATE=FAIL_FAST' in core
    assert 'timeout --signal=TERM 1200s cobaya-install planck_2020_hillipop.TT' in core
    current_runtime_refs = [
        'q041_planck_portability_v11.py',
        'q041_planck_portability_tests_v11.py',
        'q041_planck_portability_preregister_v11.json',
        'q041_planck_portability_source_lock_v11.json',
        'q041_setup_v11.sh',
        'q041_prepare_frozen_core_v11.sh',
        'q041-static-v11',
        'q041-environment-v11',
        'q041-chain-*-v11',
        'q041-final-v11',
    ]
    for token in current_runtime_refs:
        assert token in wf, token
    stale_runtime_patterns = [
        r'q041_planck_portability_tests_v(?:[3-9]|10)\\.py',
        r'q041_planck_portability_preregister_v(?:[3-9]|10)\\.json',
        r'q041_planck_portability_source_lock_v(?:[3-9]|10)\\.json',
        r'q041_planck_portability_v(?:[3-9]|10)\\.py',
        r'q041_setup_v(?:[3-9]|10)\\.sh',
        r'q041_prepare_frozen_core_v(?:[3-9]|10)\\.sh',
        r'q041-(?:static|environment|final)-v(?:[3-9]|10)\\b',
        r'q041-chain-[^\\n]*-v(?:[3-9]|10)\\b',
    ]
    for pat in stale_runtime_patterns:
        assert not re.search(pat, wf), pat
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
