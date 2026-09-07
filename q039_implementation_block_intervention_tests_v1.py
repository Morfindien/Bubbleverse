#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json
from pathlib import Path

Q='Q-039'; PROGRAM_ID='Q039-IMPLBLOCK-V1'


def write(path, obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


def static(args):
    program=Path(args.program).read_text(encoding='utf-8')
    tree=ast.parse(program)
    prereg=json.loads(Path(args.preregister).read_text(encoding='utf-8'))
    source=json.loads(Path(args.source_lock).read_text(encoding='utf-8'))
    required_strings=[
        'Q-039','Q039-IMPLBLOCK-V1','4dc873a5e880d40858d831a3b421456728f0c032',
        '5a131c91d657dd9a7c6364cc45b038710f8d0d97','a09ddde3e7ce11df99f74685feb1f1764cafb251',
        'RELATIVE_CALIBRATION_NEUTRAL','OFFDIAGONAL_PRECISION_COUPLING_OFF','CALIBRATION_PLUS_PRECISION',
        'CROSS_LIKELIHOOD' if False else 'cross_likelihood_absolute_objective_comparison_performed',
    ]
    gates={
        'PYTHON_PARSE_GATE': isinstance(tree,ast.Module),
        'Q_IDENTITY_GATE': all(x in program for x in required_strings[:2]),
        'PARENT_COMMIT_GATE': required_strings[2] in program,
        'BACKEND_COMMIT_GATE': required_strings[3] in program,
        'HILLIPOP_COMMIT_GATE': required_strings[4] in program,
        'FINITE_ARM_GATE': all(x in program for x in required_strings[5:8]),
        'NO_CROSS_OBJECTIVE_GATE': 'cross_likelihood_absolute_objective_comparison_performed' in program and 'cross_likelihood_objective_sum_performed' in program,
        'PREREG_Q_GATE': prereg.get('q')==Q and prereg.get('program_id')==PROGRAM_ID,
        'SOURCE_LOCK_Q_GATE': source.get('q')==Q and source.get('program_id')==PROGRAM_ID,
        'FOREGROUND_NOT_COMPARABLE_GATE': prereg['blocks']['foreground_treatment']['comparability']=='INCONCLUSIVE_NOT_COMPARABLE_V1',
        'CORE_NOT_COMPARABLE_GATE': prereg['blocks']['core_likelihood_construction']['comparability']=='INCONCLUSIVE_NOT_COMPARABLE_V1',
    }
    status='PASS' if all(gates.values()) else 'FAIL'
    write(args.output,{'q':Q,'program_id':PROGRAM_ID,'stage':'Q039_STATIC_TESTS','status':status,'gates':gates})
    return 0 if status=='PASS' else 2


def result(args):
    d=json.loads(Path(args.final).read_text(encoding='utf-8'))
    allowed={'SINGLE-BLOCK','COUPLED-BLOCK','INCONCLUSIVE'}
    gates={
        'Q_IDENTITY_GATE': d.get('q')==Q,
        'PROGRAM_ID_GATE': d.get('program_id')==PROGRAM_ID,
        'EXECUTION_COMPLETE_GATE': d.get('execution_status')=='COMPLETE',
        'TERMINAL_CLASSIFICATION_GATE': d.get('classification') in allowed,
        'PROVISIONAL_GATE': d.get('final_result_gate')=='PROVISIONAL' and d.get('tests_status')=='PENDING_EXTERNAL_TEST_SCRIPT',
        'NO_PHYSICAL_SYSTEMATIC_OVERCLAIM_GATE': any('not a physical Planck systematic' in x for x in d.get('interpretation_limits',[])),
        'FOREGROUND_UNRESOLVED_PRESERVED_GATE': d.get('comparability',{}).get('FOREGROUND_TREATMENT')=='INCONCLUSIVE_NOT_COMPARABLE_V1',
    }
    status='PASS' if all(gates.values()) else 'FAIL'
    write(args.output,{'q':Q,'program_id':PROGRAM_ID,'stage':'Q039_RESULT_TESTS','status':status,'gates':gates,'FINAL_RESULT_GATE':status})
    return 0 if status=='PASS' else 2


def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('static'); a.add_argument('--program',default='q039_implementation_block_intervention_v1.py'); a.add_argument('--preregister',default='q039_implementation_block_intervention_preregister_v1.json'); a.add_argument('--source-lock',default='q039_implementation_block_intervention_source_lock_v1.json'); a.add_argument('--output',required=True); a.set_defaults(func=static)
    a=sp.add_parser('result'); a.add_argument('--final',required=True); a.add_argument('--output',required=True); a.set_defaults(func=result)
    args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=='__main__': main()
