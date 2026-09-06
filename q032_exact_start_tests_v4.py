#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, yaml
import q032_exact_start_addback_v4 as v4

ROOT=pathlib.Path(__file__).resolve().parent
def write(path,obj): pathlib.Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def static(output: str) -> int:
    c=v4.load_cfg(ROOT/v4.CONFIG_FILE); src=v4.load_source_lock(); prot=v4.load_protocol_lock(); gates={}
    gates['Q_IDENTITY_GATE']=c['project']['q']=='Q-032'
    gates['RUN_IDENTITY_GATE']=c['project']['run_id']==v4.RUN
    gates['RESULT_IDENTITY_GATE']=c['project']['result_id']==v4.RESULT
    gates['PARENT_V2_IDENTITY_GATE']=c['parents']['q032_v2']['result_id']==v4.PARENT_V2_RESULT
    gates['PARENT_V2_SUPPORT_HASH_GATE']=c['parents']['q032_v2']['support_sha256']==v4.PARENT_V2_SUPPORT_SHA
    gates['BASELINE_SURFACE_GATE']=v4.BASELINE_SURFACES==('baseline_tt3',) and v4.SURFACE_SECTORS['baseline_tt3']==()
    gates['SURFACE_COUNT_GATE']=len(v4.ALL_SURFACES)==8
    gates['TIER1_CARDINALITY_GATE']=all(len(v4.SURFACE_SECTORS[x])==1 for x in v4.SINGLE_SURFACES)
    gates['TIER2_CARDINALITY_GATE']=all(len(v4.SURFACE_SECTORS[x])==2 for x in v4.PAIR_SURFACES)
    gates['CONTROL_CARDINALITY_GATE']=len(v4.SURFACE_SECTORS['full_native'])==3
    gates['EXACT_SCALAR_REF_RULE_GATE']=c['rules']['exact_scalar_ref_required'] is True
    gates['V3_SCIENTIFIC_RESULT_FORBIDDEN_GATE']=c['rules']['v3_scientific_result_forbidden'] is True
    gates['NO_OPEN_ENDED_SEARCH_GATE']=c['hierarchy']['open_ended_combinatorial_search_forbidden'] is True
    gates['NO_HILLIPOP_RERUN_GATE']=c['rules']['hillipop_not_rerun'] is True
    gates['NO_THRESHOLD_CHANGE_GATE']=c['rules']['no_threshold_change'] is True
    gates['PROTOCOL_HASH_GATE']=bool(prot['protocol_sha256'])
    gates['K047_NONINVENTION_GATE']=src['source_registry']['K-047']['bibliographic_status']=='BIBLIOGRAPHIC_DETAILS_NOT_INVENTED'
    gates['COBAYA_EXACT_REF_SOURCE_GATE']='COBAYA_3_5_6_SCALAR_REF' in src['source_registry']
    gates['RESULT_TEST_PLAN_FINITE_GATE']=len(c['result_test_plan']['mandatory_for_final_pass'])==11
    gates['NO_HARDCODED_REMOVED_SUPPORT_RANGE_IN_CONFIG_GATE']='30-49' not in (ROOT/v4.CONFIG_FILE).read_text(encoding='utf-8')
    # Direct helper behavior: mapping ref must become scalar.
    params={'x':{'prior':{'min':0.0,'max':2.0},'ref':{'dist':'norm','loc':1.0,'scale':0.3}}}
    audit=v4.apply_exact_refs(params,{'x':1.25})
    gates['EXACT_SCALAR_REFERENCE_HELPER_GATE']=params['x']['ref']==1.25 and audit['all_refs_scalar'] is True
    ok=all(gates.values())
    rec={'q':'Q-032','run_id':v4.RUN,'result_id':v4.RESULT,'stage':'Q032_EXACT_START_STATIC_TESTS','status':'PASS' if ok else 'FAIL','gates':gates,'actual_computed_scientific_result':False}
    write(output,rec); v4.self_test(c,ROOT/'q032_exact_start_self_test_v4.json')
    print('Q032_EXACT_START_STATIC_GATE='+('PASS' if ok else 'FAIL')); return 0 if ok else 2

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True); s=sp.add_parser('static'); s.add_argument('--output',required=True); a=p.parse_args(); return static(a.output)
if __name__=='__main__': raise SystemExit(main())
