"""Q048 Builder V7: resume from the exact V5 checkpoint using the admitted Guard V6 target.

Reuses historical atomic/source primitives without replaying prior accepted cells.
Stops on the first new material source/guard/branch/face obstruction, bounded budget,
or complete prerequisite continuation.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, platform, resource
import q048_full_tube_reuse_v1 as old

d = old.d
m = old.m
prefix = old.prefix
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def energy_for_cell(guard, left, right):
    """Bind V6 target energy exactly; after target use only forward e_u<=0 cap.

    G itself is always recomputed by construct_cell for the actual whole cell.
    """
    if guard.get('q') != 'Q048' or guard.get('status') != 'PASS_GUARD_COMPONENT':
        raise ValueError('GUARD_IDENTITY')
    start, end = map(F, guard['target_cell'])
    left, right = F(left), F(right)
    if not 0 < left < right:
        raise ValueError('CELL_ORIENTATION')
    tr = guard['evaluators'][0]
    if tr.get('control') or tr.get('status') != 'PASS_TO_TARGET':
        raise ValueError('PRIMARY_GUARD_REQUIRED')
    target = [r for r in tr['rows'] if r.get('role') == 'TARGET_CELL']
    if len(target) != 1:
        raise ValueError('GUARD_TARGET_ROW')
    row = target[0]
    if F(row['a0']) != start or F(row['a1']) != end or F(row['G_lower']) <= 0:
        raise ValueError('GUARD_TARGET_LINK')
    if left == start and right <= end:
        return F(row['E_left']), 'GUARD_V6_TARGET_LEFT_ENERGY', {'kind':'V6_TARGET_WHOLE_CELL','certified_G_lower':row['G_lower'],'certified_E_left':row['E_left'],'a0':row['a0'],'a1':row['a1'],'guard_result_id':guard['result_id']}
    if left >= end:
        # V6 handoff explicitly permits endpoint-energy transport forward via e_u=-3X^2<=0,
        # but not reuse of the target G margin. The actual cell G is recomputed below.
        return F(tr['last_E']), 'FORWARD_MONOTONE_GUARD_V6_ENDPOINT_ENERGY_RECOMPUTE_G', {'kind':'V6_ENDPOINT_FORWARD_ENERGY_ONLY','endpoint_a':str(end),'endpoint_E_upper':tr['last_E'],'transport_identity':'e_u=-3X^2<=0','target_G_margin_reused':False,'guard_result_id':guard['result_id']}
    raise ValueError('NO_QUALIFIED_ENERGY_LINK')


def resume_frontiers(parent, checkpoint):
    if parent.get('q') != 'Q048' or parent.get('target_q') != 'Q048' or checkpoint.get('q') != 'Q048':
        raise ValueError('PARENT_Q')
    if checkpoint.get('source_result_sha256') != sha(HERE / 'parent_v5/q048_frec_resume_result_v5.json'):
        raise ValueError('PARENT_RESULT_CHECKPOINT_LINK')
    if parent.get('new_accepted_cells') != checkpoint.get('new_accepted_cells'):
        raise ValueError('PARENT_NEW_COUNT')
    if parent.get('final_frontiers') != checkpoint.get('frontiers'):
        raise ValueError('PARENT_FRONTIER')
    retained = checkpoint.get('retained_parent_accepted_cells', 0) + checkpoint.get('new_accepted_cells', 0)
    if retained != 57:
        raise ValueError('RETAINED_CELL_COUNT')
    return dict(checkpoint['frontiers']), retained


def construct_cell(name, z0, z1, energy, t, alpha, rr, p3, hbar, wbar):
    a = m.I(F(1, z0 + 1), F(1, z1 + 1))
    B, floor, H, Hs = old.background(a, t, energy)
    G = d.guard_lower(B.lo, energy, floor.lo)
    row = {
        'case': name, 'mode': 'frec', 'z': [z0, z1], 'a': a,
        'B0': B, 'energy_upper': energy, 'floor': floor, 'G_lower': G,
        'h_barrier': hbar, 'w_barrier': wbar, 'branches': {},
        'correlation': 'same accepted event/captured-source common background and both jump-map IVPs inherited through the V4+V5 connected invariant tubes; no independent restart'
    }
    if t['ede'] is not None and G <= 0:
        row.update(status='UNRESOLVED_NEW_WHOLE_CELL_GUARD')
        return row, {
            'code': 'NEW_WHOLE_CELL_GUARD_NOT_SEPARATED',
            'inequality': '3*B0_lower-E_forward_upper+floor_lower>0',
            'margin': G,
            'method_insufficient_not_physical_falsification': True
        }

    TR = m.const('8.617343e-5') * t['T0'] / a
    ratio = 1 - wbar
    Tgamma = t['T0'] / a
    fit = d.interval(p3['fit_cases'][name]['primary_denominator'])
    source_conditions = {
        'z1_gt_900': z1 > 900,
        'TR_domain': F('.004') < TR.lo <= TR.hi < F('.4'),
        'TM_over_TR_lower': ratio.lo > F('.1'),
        'Tgamma_domain': Tgamma.lo > 1775 and Tgamma.hi < 4415,
        'fit_denominator_positive': fit.lo > 0,
    }
    if not all(source_conditions.values()):
        row.update(
            status='UNRESOLVED_NEW_SOURCE_BRANCH_OR_FIT_DOMAIN',
            TR=TR, ratio=ratio, Tgamma=Tgamma, fit_denominator=fit,
            source_domain_checks=source_conditions,
        )
        failed = [k for k, v in source_conditions.items() if not v]
        return row, {
            'code': 'NEXT_SOURCE_BRANCH_OR_FIT_DOMAIN_NOT_YET_ADMITTED',
            'failed_conditions': failed,
            'scope': 'No extrapolation of retained SWIFT/P3/source mode beyond its qualified whole-cell domain; actual fallback/reio/macro transition must be separately admitted.'
        }

    atoms = old.local_atomic(alpha, rr, TR, ratio)
    A = list(map(old.fromk, atoms['Alpha']))
    Ae = list(map(old.fromk, atoms['Alpha_eq']))
    R = old.fromk(atoms['R2p2s'])
    n = t['nH0'] / a**3 * m.const('1e-6')
    saha = m.const('3.016103031869581e21') * TR * m.sqrt_i(TR) * m.exp_i(-m.const('13.598286071938324') / TR) / n
    row['operator'] = {
        'TR_eV': TR, 'Tgamma_K': Tgamma, 'TM_over_TR': ratio,
        'fit_denominator': fit, 'Alpha': A, 'Alpha_eq': Ae, 'R2p2s': R,
        'Saha_HyRec': saha,
        'active_branch': 'inherited qualified SWIFT domain; both TM/TR channel families, same w=0 transverse gluing',
        'positive_C_denominator_identity': '(Beta0+L)*(Beta1+R+RL)+3*R*(Beta1+RL)>0 for positive source factors'
    }
    if min(v.lo for v in A + Ae + [R, saha]) <= 0:
        row['status'] = 'UNRESOLVED_ATOMIC_POSITIVITY'
        return row, {'code': 'NEW_CELL_ATOMIC_FACTOR_POSITIVITY_NOT_SEPARATED'}

    for label, q in [('L', F(1, 1000000)), ('R', F(0))]:
        lo = [old.hydrogen_barrier_term(A[l], Ae[l], saha, m.I(hbar.lo), q) for l in range(2)]
        hi = [old.hydrogen_barrier_term(A[l], Ae[l], saha, m.I(hbar.hi), q) for l in range(2)]
        tc = old.thermal_certificate(a, hbar, q, t, Hs)
        ok = all(v.hi < 0 for v in lo) and all(v.lo > 0 for v in hi) and tc['faces']['admitted']
        row['branches'][label] = {
            'q': q,
            'hydrogen_low_face_terms': lo,
            'hydrogen_high_face_terms': hi,
            'thermal': tc,
            'admitted': ok,
        }
        if not ok:
            row['status'] = 'UNRESOLVED_NEW_FREC_INVARIANT_FACE'
            return row, {
                'code': 'NEW_CELL_SOURCE_RATE_OR_THERMAL_FACE_NOT_SEPARATED',
                'branch': label,
                'method_insufficient_not_physical_falsification': True,
            }
    row['status'] = 'PASS_PAIRED_FREC_INVARIANT_TUBE'
    return row, None


def run():
    start = time.monotonic()
    stamp = datetime.now(timezone.utc).isoformat()
    spec_path = HERE / 'q048_frec_resume_spec_v7.json'
    spec = json.loads(spec_path.read_text())

    for path, rec in spec['inputs'].items():
        p = HERE / path
        b = p.read_bytes()
        if len(b) != rec['bytes'] or hashlib.sha256(b).hexdigest() != rec['sha256']:
            raise ValueError('INPUT_PIN:' + path)

    load = lambda f: json.loads((HERE / f).read_text())
    parent = load(spec['parent_raw'])
    cp = load(spec['parent_checkpoint'])
    parent_validation = load(spec['parent_validation'])
    guard = load(spec['guard_raw'])
    gv = load(spec['guard_validation'])
    base = load(spec['base_raw'])

    if parent_validation.get('status') != 'PASS' or parent_validation.get('result_sha256') != sha(HERE / spec['parent_raw']):
        raise ValueError('PARENT_VALIDATION_LINK')
    if gv.get('technical_state') != 'PASS' or gv.get('result_sha256') != sha(HERE / spec['guard_raw']):
        raise ValueError('GUARD_VALIDATION_LINK')
    if parent['question_sha256'] != spec['question_sha256'] or guard['question_sha256'] != spec['question_sha256']:
        raise ValueError('SCIENCE_IDENTITY')
    if guard['source_commit'] != spec['source_commit'] or guard['capture_sha256'] != spec['capture_sha256']:
        raise ValueError('SOURCE_IDENTITY')

    cap = load('sources/q048_prefix_config_v1.json')
    prefix.validate_config(cap)
    if sha(HERE / 'sources/q048_prefix_config_v1.json') != spec['capture_sha256']:
        raise ValueError('CAPTURE_HASH')

    fronts, retained = resume_frontiers(parent, cp)
    initial = dict(fronts)
    alpha, rr = old.load_atomic(HERE / 'sources/q048_p3_scaled_transformed_log_tables_v2.json')
    p3 = load('sources/q048_p3_scaled_raw_result_v2.json')
    hbar = m.I(*map(F, spec['barriers']['h']))
    wbar = m.I(*map(F, spec['barriers']['w']))
    rows, block = [], None
    count = 0
    init_s = time.monotonic() - start

    while max(fronts.values()) > 0:
        if time.monotonic() - start >= spec['budget_seconds'] or count >= spec['max_new_accepted_cells']:
            block = {'code': 'FROZEN_BUDGET_CHECKPOINT', 'new_accepted_cells': count}
            break
        name = max(spec['case_order'], key=lambda n: fronts[n])
        z0 = fronts[name]
        z1 = max(0, z0 - spec['redshift_step'])

        if name == 'hillipop-ede_n3':
            energy, policy, guard_binding = energy_for_cell(guard, F(1, z0 + 1), F(1, z1 + 1))
        elif 'ede_n3' in name:
            passed = [r for r in base['frec_cells'] if r['case'] == name and r['status'].startswith('PASS')]
            if not passed:
                raise ValueError('BASE_EDE_FRONTIER_MISSING:' + name)
            energy = F(passed[-1]['energy_upper'])
            policy = 'RETAINED_V4_FORWARD_MONOTONE_ENERGY'
            guard_binding = {'kind':'RETAINED_V4_FORWARD_ENERGY','target_G_margin_reused':False}
        else:
            energy = F(0)
            policy = 'LCDM_NO_SCALAR'
            guard_binding = {'kind':'LCDM_NO_SCALAR'}

        t = prefix.parameters(cap['cases'][name])
        row, obstruction = construct_cell(name, z0, z1, energy, t, alpha, rr, p3, hbar, wbar)
        row.update(
            energy_provenance=policy,
            parent_source_family=parent['result_id'],
            retained_base_result=base['result_id'],
            new_guard_result=guard['result_id'],
            guard_binding=guard_binding,
        )
        if guard_binding.get('kind') == 'V6_TARGET_WHOLE_CELL':
            row['admitted_G_lower'] = str(min(F(row['G_lower']), F(guard_binding['certified_G_lower'])))
        else:
            row['admitted_G_lower'] = row['G_lower']
        rows.append(row)
        if obstruction:
            block = dict(obstruction, case=name, z=[z0, z1], a=row['a'], attempted_cell_index=len(rows) - 1)
            break
        fronts[name] = z1
        count += 1

    result = d.encode({
        'schema_version': 'UNVALIDATED_LOCAL_CONTRACT',
        'task_type': 'SCIENTIFIC_CASE_EXECUTION',
        'program_id': spec['program_id'],
        'program_registry_status': 'LOCAL_UNREGISTERED',
        'run_id': 'LOCAL-Q048-FREC-RESUME-V7-' + stamp,
        'result_id': spec['result_id'],
        'task_id': spec['task_id'],
        'resume_revision': spec['resume_revision'],
        'q': 'Q048', 'target_q': 'Q048',
        'exact_question': parent['exact_question'],
        'question_sha256': spec['question_sha256'],
        'source_commit': spec['source_commit'],
        'capture_sha256': spec['capture_sha256'],
        'prompt_version': '2.2.0',
        'parent_handoff_id': 'LOCAL-Q048-GUARD-V6-INGESTION-RECEIPT-V1',
        'spec_sha256': sha(spec_path),
        'parent_raw_sha256': sha(HERE / spec['parent_raw']),
        'parent_checkpoint_sha256': sha(HERE / spec['parent_checkpoint']),
        'guard_raw_sha256': sha(HERE / spec['guard_raw']),
        'guard_validation_sha256': sha(HERE / spec['guard_validation']),
        'status': 'PARTIAL_WITH_EXACT_NEW_OBSTRUCTION' if block else 'COMPLETE_PREREQUISITES_CANDIDATE',
        'scope': 'CONDITIONAL_SOURCE_REAL_NEW_PAIRED_FREC_INVARIANT_CELLS_ONLY',
        'initial_frontiers': initial,
        'final_frontiers': fronts,
        'retained_accepted_cells_reused': retained,
        'retained_H_to_frec_tubes_reused': 4,
        'prior_science_reexecuted': False,
        'new_accepted_cells': count,
        'new_cells': rows,
        'blocker': block,
        'complete_a1_certificate': not block and all(z == 0 for z in fronts.values()),
        'final_delta_xe_bounds_computed': False,
        'final_delta_tau_bounds_computed': False,
        'native_P6': 'UNRESOLVED',
        'q_complete': False,
        'physical_falsification': False,
        'accepted_model_change': False,
        'return_route': 'RESULT INGESTION & ROUTING ENGINE 2.1.0',
        'execution': {
            'start_utc': stamp,
            'end_utc': datetime.now(timezone.utc).isoformat(),
            'elapsed_seconds': time.monotonic() - start,
            'initialization_and_pin_seconds': init_s,
            'python': platform.python_version(),
            'platform': platform.platform(),
            'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'backend': 'LOCAL_RUNTIME',
            'native_or_paid_runs': 0,
        },
    })
    out = HERE / 'q048_frec_resume_result_v7.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    checkpoint = {
        'schema_version': 'UNVALIDATED_LOCAL_CONTRACT',
        'q': 'Q048',
        'source_result': out.name,
        'source_result_sha256': sha(out),
        'parent_raw_sha256': sha(HERE / spec['parent_raw']),
        'guard_raw_sha256': sha(HERE / spec['guard_raw']),
        'frontiers': fronts,
        'new_accepted_cells': count,
        'retained_prior_accepted_cells': retained,
        'total_accepted_cells_in_chain': retained + count,
        'linked_invariant_state': 'branch q/jump maps and h/w barriers remain projections of the same connected source/event IVPs; no independent Cartesian restart',
        'resume_condition': 'resolve the exact new material source/guard/face obligation, or resume a frozen budget checkpoint with identical pins',
        'complete_a1': result['complete_a1_certificate'],
    }
    (HERE / 'q048_frec_resume_checkpoint_v7.json').write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(json.dumps({
        'status': result['status'],
        'new_accepted_cells': count,
        'retained_cells': retained,
        'total_accepted_cells_in_chain': retained + count,
        'frontiers': fronts,
        'blocker': result['blocker'],
        'execution': result['execution'],
    }, indent=2))


if __name__ == '__main__':
    run()
