"""Separate V113 admission validator. Does not import or execute the producer."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

PARENT = 'Q048_V111_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json'
THEOREM = 'Q048_V112_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json'
RAW = 'Q048_V112_SOURCE_CORRECT_PROOF_RAW_V1.json'
VER = 'Q048_V112_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json'
GUARD = 'q048_guard_local_v_result_v12.json'
INGEST = 'Q048_V112_INGESTION_STATE_V1.json'
POST = 'Q048_V112_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json'
TASKFILE = 'Q048_V113_NEXT_BUILDER_TASK_V1.json'
PINS = {'Q048_V111_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json': '236764f217c6c9d7affd8cffbaeefef20ee3d456ef31c1d8402baafff78d8bb7', 'Q048_V112_INGESTION_STATE_V1.json': '4cf49e206a5b96bd7bfa8b317601a141882f9d4fd3f4741e0f8e0313d1e64e48', 'Q048_V112_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json': '0614968fba0060267b3f8a1d63cf5fd8cb153982a9a4c751670e26c72f5390fe', 'Q048_V112_SOURCE_CORRECT_PROOF_POSTACCEPT_V1.json': 'c6819098da5f4748b1f2fa4aca084fef0ba6eeceee235456d788d4deccab0d85', 'Q048_V112_SOURCE_CORRECT_PROOF_RAW_V1.json': '523f9796b42307529295194a560964740ce9d46d56b81be21b984845b8a7f542', 'Q048_V112_SOURCE_CORRECT_PROOF_VERIFICATION_V1.json': '3688dc054da433971e4ddc456ec93062e1f611cd191ce01a009affd95989e8c7', 'Q048_V113_NEXT_BUILDER_TASK_V1.json': '220feca6865f50c50f9438c53606c2fa24b0193ac2f6069c775d59ffc7a9fb09', 'q048_guard_local_v_result_v12.json': '90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5'}
ROW_HASH = '50f8411d6a53b4bf0184da0eb0f83e8da6422d75e6b48a7698f6f8dba12561f4'
SPEC = 'Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_SPEC_V1.json'
SPEC_HASH = '7e382f44eb73dc623fa84823bfbcf789d1fab28c589d067c61ae7b4824a60790'
PREFIX = 'Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_'
TASK = 'LOCAL-Q048-V113-SOURCE-CORRECT-ACTUAL-CONSUMER-950-940-V1'
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
    row = g['evaluators'][0]['rows'][50]
    c, pa, ta, gb = (r[k] for k in ('candidate_actual', 'parent_authority', 'theorem_authority', 'guard_binding'))
    th = t
    expected_frontiers = dict(p['frontiers'], **{'hillipop-ede_n3': 940})
    # Exact dictionaries intentionally require canonical strings, as well as rational consistency.
    checks = {
        'schema': r['schema'] == 'bubbleverse.q048.v113.source_correct_actual_consumer.raw.v1',
        'q_target': r['q'] == r['target_q'] == p['q'] == t['q'] == 'Q048',
        'task': r['task_id'] == TASK and r['task_fingerprint'] == i['next_task_fingerprint'],
        'question': r['question_sha256'] == QUESTION_HASH == hashlib.sha256(r['exact_question'].encode()).hexdigest(),
        'spec_pin': r['spec_sha256'] == SPEC_HASH,
        'candidate_unaccepted': r['status'] == 'PENDING_VALIDATION',
        'parent_pin': pa['record'] == PARENT and pa['sha256'] == PINS[PARENT],
        'parent_validated': p['status'] == 'VALIDATED' and p['technical_state'] == 'PASS',
        'parent_state': pa['actual'] == p['accepted_actual'] == {'count':113, 'frontier':950},
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
        'consumer_authorized_by_ingestion': i['consumer_authorization'] == 'GRANTED_BY_INGESTION_FOR_EXACTLY_ONE_CELL_950_TO_940' and r['authorization_sha256'] == PINS[INGEST] and i['next_task_id'] == TASK,
        'fresh_proof_schema':t['schema']=='bubbleverse.q048.v112.source_correct_proof.acceptance.v1' and t['mathematical_proof_accepted'] is True,
        'proof_postaccept_pin':r['theorem_postaccept_sha256']==PINS[POST] and sources[POST]['status']=='PASS' and sources[POST]['accepted_checkpoint_sha256']==PINS[THEOREM] and sources[POST]['checks_total']==sources[POST]['checks_passed']==20 and all(sources[POST]['checks'].values()),
        'bounded_task_pin':r['task_authorization_sha256']==PINS[TASKFILE] and sources[TASKFILE]['task_id']==TASK and sources[TASKFILE]['parent_authority']['sha256']==PINS[PARENT] and sources[TASKFILE]['theorem_authority']['sha256']==PINS[THEOREM],
        'mathematics_stop_preserved': t['consumer_authorization'] == 'NOT_GRANTED',
        'cell_z': r['cell_z'] == t['proof_cell_z'] == [950,940],
        'cell_a': r['cell_a'] == t['proof_cell_a'] == ['1/951','1/941'],
        'saha': ta['correct_saha_fact'] == th['source_saha_factor'] == p['correct_saha_fact'] == '3.016103031869581e21',
        'thermal_domain': ta['thermal_domain'] == th['thermal_domain'] == ['-1/1000000','1/50'],
        'guard_source': gb['source_record'] == GUARD and gb['source_record_sha256'] == PINS[GUARD],
        'guard_row_hash': gb['primary_row_sha256'] == rowhash(row) == ROW_HASH,
        'guard_primary_not_control': g['evaluators'][0]['control'] is False and gb['control_role'] == 'GUARD_ONLY',
        'row_identity': gb['index'] == row['index'] == 50 and [row['z0'],row['z1']] == [950,940] and [row['a0'],row['a1']] == ['1/951','1/941'],
        'row_E_glue': gb['E_input_left'] == row['E_input_left'] == p['endpoint']['E'],
        'row_Y_glue': gb['Y_left'] == row['Y_left'] == p['endpoint']['Y'],
        'row_V_glue': gb['V_previous'] == row['V_previous'] == p['endpoint']['Vbar'],
        'row_a_glue': row['a0'] == p['endpoint']['a'],
        'no_reset': gb['source_state_reset'] is row['source_state_reset'] is False and r['no_physical_reset'] is True,
        'guard_commit': gb['whole_cell_qualified'] is row['whole_cell_qualified'] is True and gb['accepted'] is row['accepted'] is True and gb['committed'] is row['committed'] is True,
        'guard_domain': row['domain']['admitted'] is True and all(row['domain']['checks'].values()),
        'actual_count': type(c['count']) is int and c['count'] == p['accepted_actual']['count']+1 == 114,
        'actual_frontier': c['frontier'] == row['z1'] == 940,
        'four_frontiers': c['frontiers'] == expected_frontiers,
        'endpoint_a': c['endpoint']['a'] == row['a1'] == '1/941',
        'endpoint_E': c['endpoint']['E'] == row['E_right'] == '23169291469718832199/500000000000000000',
        'endpoint_Y': c['endpoint']['Y'] == row['Y_right'] == '36842143149632196673/1000000000000000000',
        'endpoint_V': c['endpoint']['Vbar'] == row['V_admitted'] == '2275188699640893309/250000000000000000',
        'theorem_lower': c['connected_lower'] == ta['connected_lower'] == th['connected_lower'] == '228498093366287/500000000000000000' and F(c['connected_lower']) > 0,
        'theorem_K': c['K_upper'] == ta['K_upper'] == th['K_upper'] == '2434080172867495593979/500000000000000000' and F(c['K_upper']) > 0,
        'one_actual_zero_proof': r['new_actual_cells'] == 1 and r['new_mathematical_proof_cells'] == r['new_full_theorem_recomputations'] == 0,
        'single_consumption': r['theorem_consumptions'] == 1,
        'no_below940': r['below940_work'] is False,
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
        ('wrong_cell', ('cell_z',),[940,940]),
        ('wrong_endpoint_a', ('candidate_actual','endpoint','a'),'1/931'),
        ('wrong_endpoint_E', ('candidate_actual','endpoint','E'),'1'),
        ('wrong_endpoint_Y', ('candidate_actual','endpoint','Y'),'1'),
        ('wrong_endpoint_V', ('candidate_actual','endpoint','Vbar'),'1'),
        ('below940_frontier', ('candidate_actual','frontier'),930),
        ('below940_flag', ('below940_work',),True),
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
    report = {'schema':'bubbleverse.q048.v113.source_correct_actual_consumer.validation.v1',
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
