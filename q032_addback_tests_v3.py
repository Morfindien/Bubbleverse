#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, yaml
import q032_camspec_addback_v3 as v3

ROOT=pathlib.Path(__file__).resolve().parent

def write(path,obj):
    pathlib.Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def static(output: str) -> int:
    c=v3.load_cfg(ROOT/v3.CONFIG_FILE)
    src=v3.load_source_lock()
    prot=v3.load_protocol_lock()
    gates={}
    gates['Q_IDENTITY_GATE']=c['project']['q']=='Q-032'
    gates['RUN_IDENTITY_GATE']=c['project']['run_id']==v3.RUN
    gates['RESULT_IDENTITY_GATE']=c['project']['result_id']==v3.RESULT
    gates['PARENT_V2_IDENTITY_GATE']=c['parents']['q032_v2']['result_id']==v3.PARENT_V2_RESULT
    gates['PARENT_V2_SUPPORT_HASH_GATE']=c['parents']['q032_v2']['support_sha256']==v3.PARENT_V2_SUPPORT_SHA
    gates['SURFACE_COUNT_GATE']=len(v3.ALL_SURFACES)==7
    gates['TIER1_CARDINALITY_GATE']=all(len(v3.SURFACE_SECTORS[x])==1 for x in v3.SINGLE_SURFACES)
    gates['TIER2_CARDINALITY_GATE']=all(len(v3.SURFACE_SECTORS[x])==2 for x in v3.PAIR_SURFACES)
    gates['CONTROL_CARDINALITY_GATE']=len(v3.SURFACE_SECTORS['full_native'])==3
    gates['NO_OPEN_ENDED_SEARCH_GATE']=c['hierarchy']['open_ended_combinatorial_search_forbidden'] is True
    gates['NO_HILLIPOP_RERUN_GATE']=c['rules']['hillipop_not_rerun'] is True
    gates['NO_THRESHOLD_CHANGE_GATE']=c['rules']['no_threshold_change'] is True
    gates['PROTOCOL_HASH_GATE']=bool(prot['protocol_sha256'])
    gates['K047_NONINVENTION_GATE']=src['source_registry']['K-047']['bibliographic_status']=='BIBLIOGRAPHIC_DETAILS_NOT_INVENTED'
    gates['RESULT_TEST_PLAN_FINITE_GATE']=len(c['result_test_plan']['mandatory_for_final_pass'])==10
    gates['NO_HARDCODED_REMOVED_SUPPORT_RANGE_IN_CONFIG_GATE']='30-49' not in (ROOT/v3.CONFIG_FILE).read_text(encoding='utf-8')
    ok=all(gates.values())
    rec={'q':'Q-032','run_id':v3.RUN,'result_id':v3.RESULT,'stage':'Q032_ADDBACK_STATIC_TESTS','status':'PASS' if ok else 'FAIL','gates':gates,'actual_computed_scientific_result':False}
    write(output,rec)
    v3.self_test(c, ROOT/'q032_addback_self_test_v3.json')
    print('Q032_ADDBACK_STATIC_GATE='+('PASS' if ok else 'FAIL'))
    return 0 if ok else 2

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    s=sp.add_parser('static'); s.add_argument('--output',required=True)
    a=p.parse_args()
    if a.cmd=='static': return static(a.output)
    return 2

if __name__=='__main__':
    raise SystemExit(main())
