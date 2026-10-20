"""Separate V117 admission validator. Does not import or execute the producer."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

PARENT = 'Q048_V115_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
THEOREM = 'Q048_V116_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json'
RAW = 'Q048_V116_SOURCE_CORRECT_PROOF_RAW_V1.json'
VER = 'Q048_V116_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json'
GUARD = 'q048_guard_local_v_result_v12.json'
INGEST = 'Q048_V116_INGESTION_STATE_V1.json'
POST = 'Q048_V116_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'
TASKFILE = 'Q048_V117_NEXT_BUILDER_TASK_V1.json'
PINS = {'Q048_V115_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json': '0b69e1f1d37f213d833a23016e5bcbc9874bb0967584625828fcb5351a7e887a', 'Q048_V116_INGESTION_STATE_V1.json': '6a91c2cf4255bc456ef513401b079e9e2080978f78aa5c9f9b0fd3f5f8845b33', 'Q048_V116_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json': '5c5e44f868c1c75ab453c5529139d4619af61dfa5374d986c5085c2799606929', 'Q048_V116_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json': 'd455ac922a3855cf935bbe1e482b8754c099c2a3991002af238d01cb01f6cc8d', 'Q048_V116_SOURCE_CORRECT_PROOF_RAW_V1.json': 'c51eef3334fe9c237afe2735eca93d0538611b98d5023707bc9e544dda2d871f', 'Q048_V116_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json': '58bd7305ee69d3552922f0dba72e680d211ca7ca41d49cbc287105b3d8edf282', 'Q048_V117_NEXT_BUILDER_TASK_V1.json': 'e92c800fcf527cac1cc657c732ce998f12485e1b19e276521b16382d7cf3d629', 'q048_guard_local_v_result_v12.json': '90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5'}
ROW_HASH = '7b1b3f0656c9b2c92e8cdcd032b0fdc130846692fadb03613b05b127734034d3'
SPEC = 'Q048_V117_SOURCE_CORRECT_ACTUAL_CONSUMER_SPEC_V1.json'
SPEC_HASH = '18a1de0fb7ce8f746f31979ffe876bdc2e824b186119b7dee2c80ae7ad129e3a'
PREFIX = 'Q048_V117_SOURCE_CORRECT_ACTUAL_CONSUMER_'
TASK = 'LOCAL-Q048-V117-SOURCE-CORRECT-ACTUAL-CONSUMER-930-920-V1'
QUESTION_HASH = 'c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def rowhash(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def load_authorities(root):
    result = {}
    for name, expected in PINS.items():
        if sha(root / name) != expected:
            raise ValueError('authority byte pin: ' + name)
        result[name] = load(root / name)
    return result


def check_result(r, sources):
    p, t, tr, tv, g, i = (sources[n] for n in (PARENT, THEOREM, RAW, VER, GUARD, INGEST))
    row = g['evaluators'][0]['rows'][52]
    c, pa, ta, gb = (r[k] for k in ('candidate_actual', 'parent_authority', 'theorem_authority', 'guard_binding'))
    th = t
    expected_frontiers = dict(p['frontiers'], **{'hillipop-ede_n3': 920})
    # Exact dictionaries intentionally require canonical strings, as well as rational consistency.
    checks = {
        'schema': r['schema'] == 'bubbleverse.q048.v117.source_correct_actual_consumer.raw.v1',
        'q_target': r['q'] == r['target_q'] == p['q'] == t['q'] == 'Q048',
        'task': r['task_id'] == TASK and r['task_fingerprint'] == i['next_task_fingerprint'],
        'question': r['question_sha256'] == QUESTION_HASH == hashlib.sha256(r['exact_question'].encode()).hexdigest(),
        'spec_pin': r['spec_sha256'] == SPEC_HASH,
        'candidate_unaccepted': r['status'] == 'PENDING_VALIDATION',
        'parent_pin': pa['record'] == PARENT and pa['sha256'] == PINS[PARENT],
        'parent_validated': p['status'] == 'VALIDATED' and p['technical_state'] == 'PASS',
        'parent_state': pa['actual'] == p['accepted_actual'] == {'count':115, 'frontier':930},
        'parent_endpoint': pa['endpoint'] == p['endpoint'],
        'parent_frontiers': pa['frontiers'] == p['frontiers'],
        'theorem_pin': ta['record'] == THEOREM and ta['sha256'] == PINS[THEOREM],
        'theorem_raw_pin': ta['raw_sha256'] == t['raw_sha256'] == PINS[RAW],
        'theorem_ver_pin': ta['verification_sha256'] == t['verification_sha256'] == PINS[VER],
        'theorem_accepted': t['status'] == 'ACCEPTED' and t['technical_state'] == 'PASS',
        'theorem_parent_hash': t['parent_checkpoint_sha256'] == PINS[PARENT],
        'theorem_parent_full_state': t['parent_actual']==p['accepted_actual'] and t['parent_endpoint']==p['endpoint'] and t['parent_connected_lower']==p['connected_lower'],
        'theorem_raw_binding': tr['parent_checkpoint_sha256']==PINS[PARENT] and tr['parent_actual']==p['accepted_actual'] and tr['K_upper']==t['K_upper'] and tr['hmin']==t['connected_lower'],
        'retained_verifier': tv['status'] == 'PASS' and tv['verification_pass'] is True and tv['raw_sha256'] == PINS[RAW] and tv['checks_total'] == tv['checks_passed'] == 30 and all(tv['checks'].values()) and tv['semantic_mutations_total'] == tv['semantic_mutations_rejected'] == 16,
        'consumer_authorized_by_ingestion': i['consumer_authorization'] == 'GRANTED_BY_INGESTION_FOR_EXACTLY_ONE_CELL_930_TO_920' and r['authorization_sha256'] == PINS[INGEST] and i['next_task_id'] == TASK,
        'fresh_proof_schema':t['schema']=='bubbleverse.q048.v116.source_correct_proof.acceptance.v1' and t['mathematical_proof_accepted'] is True,
        'proof_postaccept_pin':r['theorem_postaccept_sha256']==PINS[POST] and sources[POST]['status']=='PASS' and sources[POST]['accepted_checkpoint_sha256']==PINS[THEOREM] and sources[POST]['checks_total']==sources[POST]['checks_passed']==20 and all(sources[POST]['checks'].values()),
        'bounded_task_pin':r['task_authorization_sha256']==PINS[TASKFILE] and sources[TASKFILE]['task_id']==TASK and sources[TASKFILE]['parent_authority']['sha256']==PINS[PARENT] and sources[TASKFILE]['theorem_authority']['sha256']==PINS[THEOREM],
        'mathematics_stop_preserved': t['consumer_authorization'] == 'NOT_GRANTED',
        'cell_z': r['cell_z'] == t['proof_cell_z'] == [930,920],
        'cell_a': r['cell_a'] == t['proof_cell_a'] == ['1/931','1/921'],
        'saha': ta['correct_saha_fact'] == th['source_saha_factor'] == p['correct_saha_fact'] == '3.016103031869581e21',
        'thermal_domain': ta['thermal_domain'] == th['thermal_domain'] == ['-1/1000000','1/50'],
        'guard_source': gb['source_record'] == GUARD and gb['source_record_sha256'] == PINS[GUARD],
        'guard_row_hash': gb['primary_row_sha256'] == rowhash(row) == ROW_HASH,
        'guard_primary_not_control': g['evaluators'][0]['control'] is False and gb['control_role'] == 'GUARD_ONLY',
        'row_identity': gb['index'] == row['index'] == 52 and [row['z0'],row['z1']] == [930,920] and [row['a0'],row['a1']] == ['1/931','1/921'],
        'row_E_glue': gb['E_input_left'] == row['E_input_left'] == p['endpoint']['E'],
        'row_Y_glue': gb['Y_left'] == row['Y_left'] == p['endpoint']['Y'],
        'row_V_glue': gb['V_previous'] == row['V_previous'] == p['endpoint']['Vbar'],
        'row_a_glue': row['a0'] == p['endpoint']['a'],
        'no_reset': gb['source_state_reset'] is row['source_state_reset'] is False and r['no_physical_reset'] is True,
        'guard_commit': gb['whole_cell_qualified'] is row['whole_cell_qualified'] is True and gb['accepted'] is row['accepted'] is True and gb['committed'] is row['committed'] is True,
        'guard_domain': row['domain']['admitted'] is True and all(row['domain']['checks'].values()),
        'actual_count': type(c['count']) is int and c['count'] == p['accepted_actual']['count']+1 == 116,
        'actual_frontier': c['frontier'] == row['z1'] == 920,
        'four_frontiers': c['frontiers'] == expected_frontiers,
        'endpoint_a': c['endpoint']['a'] == row['a1'] == '1/921',
        'endpoint_E': c['endpoint']['E'] == row['E_right'] == '21553673409627471439/500000000000000000',
        'endpoint_Y': c['endpoint']['Y'] == row['Y_right'] == '133823577632185643/3906250000000000',
        'endpoint_V': c['endpoint']['Vbar'] == row['V_admitted'] == '2119955747339110627/250000000000000000',
        'theorem_lower': c['connected_lower'] == ta['connected_lower'] == th['connected_lower'] == '54513832861587/125000000000000000' and F(c['connected_lower']) > 0,
        'theorem_K': c['K_upper'] == ta['K_upper'] == th['K_upper'] == '1220855076846709617829/250000000000000000' and F(c['K_upper']) > 0,
        'one_actual_zero_proof': r['new_actual_cells'] == 1 and r['new_mathematical_proof_cells'] == r['new_full_theorem_recomputations'] == 0,
        'single_consumption': r['theorem_consumptions'] == 1,
        'no_below920': r['below920_work'] is False,
        'history_firewall': r['historical_record_modified'] is False and r['historical_v101_v102_replayed'] is False,
        'claim_firewall': r['scientific_state'] == 'INCONCLUSIVE' and r['q_complete'] is False and r['NativeP6'] == 'UNRESOLVED' and r['no_native_trajectory_claim'] is True,
    }
    return checks


def mutations(original):
    controls = [('wrong_raw_schema',('schema',),'bubbleverse.invalid.raw'),
        ('wrong_parent_hash', ('parent_authority','sha256'), '0'*64),
        ('historical_parent_identity', ('parent_authority','record'), 'q048_frec_moving_h_accepted_checkpoint_v101.json'),
        ('wrong_theorem_hash', ('theorem_authority','sha256'), '1'*64),
        ('wrong_row_hash', ('guard_binding','primary_row_sha256'), '2'*64),
        ('wrong_row_index', ('guard_binding','index'),48),
        ('reset_true', ('guard_binding','source_state_reset'),True),
        ('wrong_cell', ('cell_z',),[920,920]),
        ('wrong_endpoint_a', ('candidate_actual','endpoint','a'),'1/911'),
        ('wrong_endpoint_E', ('candidate_actual','endpoint','E'),'1'),
        ('wrong_endpoint_Y', ('candidate_actual','endpoint','Y'),'1'),
        ('wrong_endpoint_V', ('candidate_actual','endpoint','Vbar'),'1'),
        ('below920_frontier', ('candidate_actual','frontier'),910),
        ('below920_flag', ('below920_work',),True),
        ('wrong_K', ('candidate_actual','K_upper'),'1'),
        ('wrong_lower', ('candidate_actual','connected_lower'),'1'),
        ('old_saha', ('theorem_authority','correct_saha_fact'),'3.016101031869581e21'),
        ('uncommitted_row', ('guard_binding','committed'),False),
        ('extra_actual', ('new_actual_cells',),2),
        ('extra_proof', ('new_mathematical_proof_cells',),1),
        ('double_consumption', ('theorem_consumptions',),2),
        ('historical_replay', ('historical_v101_v102_replayed',),True),
        ('wrong_left_glue', ('guard_binding','Y_left'),'0'),
        ('unauthorized', ('authorization_sha256',),'3'*64),
        ('Q_closed', ('q_complete',),True),
    ]
    result = {}
    for name, path, value in controls:
        item = copy.deepcopy(original)
        target = item
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        if item==original:raise ValueError('NO_OP_MUTATION:'+name)
        result[name] = item
    return result


def authority_mutations(sources):
    changed=copy.deepcopy(sources)
    changed[THEOREM]['schema']='bubbleverse.invalid.theorem_acceptance'
    if changed==sources:raise ValueError('NO_OP_AUTHORITY_MUTATION')
    return {'wrong_theorem_schema':changed}


def main():
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument('--inputs', type=Path, default=here/'inputs')
    parser.add_argument('--out', type=Path, default=here)
    args = parser.parse_args()
    if sha(args.out/SPEC) != SPEC_HASH:
        raise ValueError('spec byte pin')
    a = load_authorities(args.inputs)
    source = args.out/(PREFIX+'RAW_V1.json')
    r = load(source)
    checks = check_result(r,a)
    rejected = {}
    failed_checks = {}
    for name, mutated in mutations(r).items():
        mchecks = check_result(mutated,a)
        failed_checks[name] = [key for key,val in mchecks.items() if not val]
        rejected[name] = bool(failed_checks[name])
    for name,mutated_sources in authority_mutations(a).items():
        mchecks=check_result(r,mutated_sources)
        failed_checks[name]=[key for key,val in mchecks.items() if not val]
        rejected[name]=bool(failed_checks[name])
    passed = all(checks.values()) and all(rejected.values())
    report = {'schema':'bubbleverse.q048.v117.source_correct_actual_consumer.validation.v1',
              'status':'PASS' if passed else 'FAIL', 'result_sha256':sha(source),
              'spec_sha256':SPEC_HASH, 'authority_pins':PINS,
              'checks_total':len(checks),'checks_passed':sum(checks.values()),'checks':checks,
              'semantic_mutations_total':len(rejected),'semantic_mutations_rejected':sum(rejected.values()),
              'mutations_rejected':rejected,'mutation_failed_invariants':failed_checks,
              'independence_scope':'Separate invariant composition and authority readback; no producer import. Shared frozen theorem/source premises, not independent physics.'}
    dest = args.out/(PREFIX+'VALIDATION_V1.json')
    with dest.open('x') as f: json.dump(report,f,indent=2); f.write('\n')
    print(report['status'],report['checks_passed'],len(checks),'checks;',sum(rejected.values()),len(rejected),'real mutations rejected')
    if not passed: raise SystemExit(1)


if __name__ == '__main__':
    main()
