"""Separate V109 admission validator. Does not import or execute the producer."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

PARENT = 'Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
THEOREM = 'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json'
RAW = 'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_RAW_V1.json'
VER = 'Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_VERIFICATION_V1.json'
GUARD = 'q048_guard_local_v_result_v12.json'
INGEST = 'Q048_V108_INGESTION_STATE_V1.json'
PINS = {
    PARENT:'3876328fa6acfd5a79c01505526de8e2b6d384b06241685eb359fa5635747e24',
    THEOREM:'4356c7f697c2df5897a64bfb7dc5f155af0b5dbaea7345f1f0af804d6963c5e7',
    RAW:'df25316ce4a19f9177d99d3d256754dc640773f4ac9d0420d02c2f8e7412e928',
    VER:'c201bbdf75f7529f3c3f3d03a6c75df2197542d63fcad2d86d60c740e1ab7c8b',
    GUARD:'90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5',
    INGEST:'adb1f7efda7eeb75a6da68781e2af8db195bcc634d3d8335b3d5c69c0742aed0'
}
ROW_HASH = '98b31afe3cc6371533b59edf6ef673c0da6219122d145a8ca997276c270301cf'
SPEC = 'Q048_V109_SOURCE_CORRECT_ACTUAL_CONSUMER_SPEC_V1.json'
SPEC_HASH = '5834ed32cb0cf80dc2e8609efa0d8f6145f25171c683303729b1e8a07879cad1'
PREFIX = 'Q048_V109_SOURCE_CORRECT_ACTUAL_CONSUMER_'
TASK = 'LOCAL-Q048-V109-SOURCE-CORRECT-ACTUAL-CONSUMER-970-960-V1'
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
    row = g['evaluators'][0]['rows'][48]
    c, pa, ta, gb = (r[k] for k in ('candidate_actual', 'parent_authority', 'theorem_authority', 'guard_binding'))
    th = t['retained_theorem']
    expected_frontiers = dict(p['frontiers'], **{'hillipop-ede_n3': 960})
    # Exact dictionaries intentionally require canonical strings, as well as rational consistency.
    checks = {
        'schema': r['schema'] == 'bubbleverse.q048.v109.source_correct_actual_consumer.raw.v1',
        'q_target': r['q'] == r['target_q'] == p['q'] == t['q'] == 'Q048',
        'task': r['task_id'] == TASK and r['task_fingerprint'] == i['next_task_fingerprint'],
        'question': r['question_sha256'] == QUESTION_HASH == hashlib.sha256(r['exact_question'].encode()).hexdigest(),
        'spec_pin': r['spec_sha256'] == SPEC_HASH,
        'candidate_unaccepted': r['status'] == 'PENDING_VALIDATION',
        'parent_pin': pa['record'] == PARENT and pa['sha256'] == PINS[PARENT],
        'parent_validated': p['status'] == 'VALIDATED' and p['technical_state'] == 'PASS',
        'parent_state': pa['actual'] == p['accepted_actual'] == {'count':111, 'frontier':970},
        'parent_endpoint': pa['endpoint'] == p['endpoint'],
        'parent_frontiers': pa['frontiers'] == p['frontiers'],
        'theorem_pin': ta['record'] == THEOREM and ta['sha256'] == PINS[THEOREM],
        'theorem_raw_pin': ta['raw_sha256'] == t['raw_sha256'] == PINS[RAW],
        'theorem_ver_pin': ta['verification_sha256'] == t['verification_sha256'] == PINS[VER],
        'theorem_accepted': t['status'] == 'ACCEPTED' and t['technical_state'] == 'PASS',
        'theorem_parent_hash': t['parent_authority']['sha256'] == PINS[PARENT],
        'theorem_parent_full_state': all(t['parent_authority'][k] == p[k] for k in ('accepted_actual','frontiers','endpoint','connected_lower','K_upper','correct_saha_fact')),
        'theorem_raw_binding': tr['parent_authority'] == t['parent_authority'] and tr['retained_theorem'] == th,
        'retained_verifier': tv['status'] == 'PASS' and tv['verification_pass'] is True and tv['raw_sha256'] == PINS[RAW] and tv['checks_total'] == tv['checks_passed'] == 40 and all(tv['checks'].values()) and tv['semantic_mutations_total'] == tv['semantic_mutations_rejected'] == 16,
        'consumer_authorized_by_ingestion': i['consumer_authorization'] == 'GRANTED_BY_INGESTION_FOR_EXACTLY_ONE_CELL_970_TO_960' and r['authorization_sha256'] == PINS[INGEST] and i['next_task_id'] == TASK,
        'mathematics_stop_preserved': t['consumer_authorization'] == 'NOT_GRANTED',
        'cell_z': r['cell_z'] == t['proof_bridge_cell_z'] == [970,960],
        'cell_a': r['cell_a'] == t['proof_bridge_cell_a'] == ['1/971','1/961'],
        'saha': ta['correct_saha_fact'] == th['source_saha_factor'] == p['correct_saha_fact'] == '3.016103031869581e21',
        'thermal_domain': ta['thermal_domain'] == th['thermal_domain'] == ['-1/1000000','1/50'],
        'guard_source': gb['source_record'] == GUARD and gb['source_record_sha256'] == PINS[GUARD],
        'guard_row_hash': gb['primary_row_sha256'] == rowhash(row) == ROW_HASH,
        'guard_primary_not_control': g['evaluators'][0]['control'] is False and gb['control_role'] == 'GUARD_ONLY',
        'row_identity': gb['index'] == row['index'] == 48 and [row['z0'],row['z1']] == [970,960] and [row['a0'],row['a1']] == ['1/971','1/961'],
        'row_E_glue': gb['E_input_left'] == row['E_input_left'] == p['endpoint']['E'],
        'row_Y_glue': gb['Y_left'] == row['Y_left'] == p['endpoint']['Y'],
        'row_V_glue': gb['V_previous'] == row['V_previous'] == p['endpoint']['Vbar'],
        'row_a_glue': row['a0'] == p['endpoint']['a'],
        'no_reset': gb['source_state_reset'] is row['source_state_reset'] is False and r['no_physical_reset'] is True,
        'guard_commit': gb['whole_cell_qualified'] is row['whole_cell_qualified'] is True and gb['accepted'] is row['accepted'] is True and gb['committed'] is row['committed'] is True,
        'guard_domain': row['domain']['admitted'] is True and all(row['domain']['checks'].values()),
        'actual_count': type(c['count']) is int and c['count'] == p['accepted_actual']['count']+1 == 112,
        'actual_frontier': c['frontier'] == row['z1'] == 960,
        'four_frontiers': c['frontiers'] == expected_frontiers,
        'endpoint_a': c['endpoint']['a'] == row['a1'] == '1/961',
        'endpoint_E': c['endpoint']['E'] == row['E_right'] == '49737668672811936943/1000000000000000000',
        'endpoint_Y': c['endpoint']['Y'] == row['Y_right'] == '39560432998711765483/1000000000000000000',
        'endpoint_V': c['endpoint']['Vbar'] == row['V_admitted'] == '4876592093839665491/500000000000000000',
        'theorem_lower': c['connected_lower'] == ta['connected_lower'] == th['connected_lower'] == '479774678212513/1000000000000000000' and F(c['connected_lower']) > 0,
        'theorem_K': c['K_upper'] == ta['K_upper'] == th['K_upper'] == '1001919080623370229873/200000000000000000' and F(c['K_upper']) > 0,
        'one_actual_zero_proof': r['new_actual_cells'] == 1 and r['new_mathematical_proof_cells'] == r['new_full_theorem_recomputations'] == 0,
        'single_consumption': r['theorem_consumptions'] == 1,
        'no_below960': r['below960_work'] is False,
        'history_firewall': r['historical_record_modified'] is False and r['historical_v101_v102_replayed'] is False,
        'claim_firewall': r['scientific_state'] == 'INCONCLUSIVE' and r['q_complete'] is False and r['NativeP6'] == 'UNRESOLVED' and r['no_native_trajectory_claim'] is True,
    }
    return checks


def mutations(original):
    controls = [
        ('wrong_parent_hash', ('parent_authority','sha256'), '0'*64),
        ('historical_parent_identity', ('parent_authority','record'), 'q048_frec_moving_h_accepted_checkpoint_v101.json'),
        ('wrong_theorem_hash', ('theorem_authority','sha256'), '1'*64),
        ('wrong_row_hash', ('guard_binding','primary_row_sha256'), '2'*64),
        ('wrong_row_index', ('guard_binding','index'),47),
        ('reset_true', ('guard_binding','source_state_reset'),True),
        ('wrong_cell', ('cell_z',),[960,950]),
        ('wrong_endpoint_a', ('candidate_actual','endpoint','a'),'1/951'),
        ('wrong_endpoint_E', ('candidate_actual','endpoint','E'),'1'),
        ('wrong_endpoint_Y', ('candidate_actual','endpoint','Y'),'1'),
        ('wrong_endpoint_V', ('candidate_actual','endpoint','Vbar'),'1'),
        ('below960_frontier', ('candidate_actual','frontier'),950),
        ('below960_flag', ('below960_work',),True),
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
        result[name] = item
    return result


def main():
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument('--inputs', type=Path, default=here.parent/'inputs')
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
    passed = all(checks.values()) and all(rejected.values())
    report = {'schema':'bubbleverse.q048.v109.source_correct_actual_consumer.validation.v1',
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
