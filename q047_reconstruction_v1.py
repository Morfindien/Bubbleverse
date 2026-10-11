#!/usr/bin/env python3
"""Approved four-case reconstruction. Reuse V1 state checks; never scientific PASS.
The repository is read-only to the authoring agent. This target is user launched.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

import q047_collection_v1 as state
import q047_execution_v1 as acquire

HERE = Path(__file__).resolve().parent
ID = 'Q047-RECONSTRUCTION-V1'
WORKFLOW = 'q047-reconstruction-v1.yml'
CASES = acquire.CASES
EVENTS = ['before_input', 'after_input', 'before_background', 'after_background',
          'before_thermal', 'after_thermal']
CAPTURE_OUTPUTS = set(state.REQUIRED_OUTPUTS) | {'runtime_control_v2.json',
    'capture_receipt.json', 'mapped_dependencies.json', 'native_data.json',
    'native_attempt.json', 'requested_case.ini', 'native.log', 'runtime_preflight.json',
    'golden/background.tsv', 'golden/thermodynamics.tsv', 'observer_build/build_receipt.json'}
need, read, sha, write = state.need, state.read, state.sha, state.write


def base():
    return dict(q='Q-047', program_id=ID, program_version='v1', workflow_version='v1',
                run_id=os.environ.get('GITHUB_RUN_ID', 'LOCAL'),
                run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT', 'LOCAL'),
                execution_commit=os.environ.get('GITHUB_SHA', 'LOCAL'),
                checked_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                origin='NEW_RECONSTRUCTION', historical_export=False,
                contract_sha256=sha(HERE / 'Q047_RECONSTRUCTION_CONTRACT_V1.json')
                    if (HERE / 'Q047_RECONSTRUCTION_CONTRACT_V1.json').is_file() else None,
                collection_lock_sha256=state.LOCK_SHA)


def package():
    c = read(HERE / 'Q047_RECONSTRUCTION_CONTRACT_V1.json')
    need(c['q'] == 'Q-047' and c['program_id'] == ID and c['cases'] == list(CASES), 'CONTRACT_IDENTITY')
    need(c['authorization']['status'] == 'USER_APPROVED' and
         c['authorization']['native_reconstruction'] is True and
         c['authorization']['github_writes_by_agent'] is False, 'AUTHORIZATION_SCOPE')
    need(c['limits']['max_native_processes'] == 4 and c['limits']['native_seconds_per_case'] == 600,
         'CAPTURE_LIMITS')
    for name, digest in c['file_sha256'].items():
        p = HERE / name
        need(p.is_file() and sha(p) == digest, 'PACKAGE_FILE ' + name)
    frozen = state.lock()
    reg = read(HERE / 'bubbleverse_program_registry.json')['programs']
    need(ID in reg and reg[ID]['status'] == 'ACTIVE' and reg[ID]['q'] == 'Q-047', 'REGISTRY_ID')
    e = reg[ID]
    need(e['workflow_id'] == WORKFLOW and e['workflow_path'] == '.github/workflows/' + WORKFLOW and
         e['program_version'] == e['workflow_version'] == e['version'] == 'v1', 'REGISTRY_TARGET')
    launcher = (HERE / '.github/workflows/00-bubbleverse-start.yml').read_text()
    for s in ['json.loads', 'program_id not in programs', "status != 'ACTIVE'", 'gh workflow run']:
        need(s in launcher, 'LAUNCHER_SEMANTICS')
    readme = (HERE / 'README.md').read_text()
    for s in [ID, WORKFLOW, 'bubbleverse_program_registry.json', '00-bubbleverse-start.yml']:
        need(s in readme, 'README_REFERENCE ' + s)
    journal = (HERE / 'Q047_SAMLET_JOURNAL.md').read_text()
    need(frozen['question'] in journal and 'USER_APPROVED' in journal and ID in journal, 'JOURNAL_CONTINUITY')
    return c, frozen


def runtime_gate(obj, case):
    need(obj.get('schema') == 'Q047_RUNTIME_CONTROL_V2' and obj.get('q') == 'Q-047' and
         obj.get('case') == case and obj.get('origin') == 'NEW_RECONSTRUCTION', 'RUNTIME_IDENTITY')
    events = obj['events']
    need([x['checkpoint'] for x in events] == EVENTS, 'FP_CHECKPOINTS')
    for e in events:
        need(type(e['rounding_mode']) is int and e['rounding_mode'] == e['FE_TONEAREST'] and
             type(e['mxcsr']) is int and not (e['mxcsr'] & ((1 << 15) | (1 << 6))) and
             (e['mxcsr'] & (3 << 13)) == 0 and
             type(e['x87_control']) is int and (e['x87_control'] & (3 << 10)) == 0,
             'FP_ENVIRONMENT')
    need(obj['symbol_resolution_kind'] == 'DLSYM_REFERENCE_NOT_CORE_GOT_PROOF', 'SYMBOL_SCOPE')
    need({x['name'] for x in obj['symbols']} == {'cos', 'sincos', 'pow'} and
         all(x['object'] and x['offset'].startswith('0x') for x in obj['symbols']), 'SYMBOL_REFERENCE')
    need(len(obj['cpuid_leaf1']) == len(obj['cpuid_leaf7']) == 4 and
         obj['xcr0'].startswith('0x'), 'CPU_RECORD')
    return dict(status='PASS', historical_environment_identity='NOT_ASSERTED',
                actual_call_domain_error_bounds='NOT_PROVIDED',
                scope='Six new-run FP checkpoints and named dlsym references; no historical or all-call proof')


def file_index(directory):
    return {str(p.relative_to(directory)): sha(p) for p in sorted(directory.rglob('*'))
            if p.is_file() and p.name != 'worker_result.json' and p.suffix != '.zip'}


def branch_gate(directory, obj, case):
    b = base()
    for name in ['q', 'program_id', 'program_version', 'workflow_version', 'run_id', 'run_attempt',
                 'execution_commit', 'contract_sha256', 'collection_lock_sha256']:
        need(obj[name] == b[name], 'BRANCH_IDENTITY ' + name)
    need(obj['case'] == case and obj['origin'] == 'NEW_RECONSTRUCTION' and
         obj['historical_export'] is False, 'BRANCH_CASE')
    need(obj['scientific_verdict'] == 'INSUFFICIENT_EVIDENCE' and
         obj['final_result_gate'] == 'UNRESOLVED', 'SCIENTIFIC_PROMOTION')
    need(type(obj['native_processes_started']) is int and obj['native_processes_started'] in [0, 1] and
         obj['full_cmb_likelihood_evaluations'] == 0, 'BRANCH_EXECUTION_SCOPE')
    for name, digest in obj['files'].items():
        rel = Path(name)
        need(not rel.is_absolute() and '..' not in rel.parts and name != 'worker_result.json', 'MEMBER_PATH')
        p = directory / rel
        need(p.is_file() and not p.is_symlink() and sha(p) == digest, 'MEMBER_HASH ' + name)
    need(obj['files'] == file_index(directory), 'MEMBER_COMPLETENESS')
    if obj['execution_status'] == 'CAPTURE_COMPLETE':
        need(CAPTURE_OUTPUTS <= obj['files'].keys(), 'CAPTURE_OUTPUT_SET')
    return obj['execution_status'] == 'CAPTURE_COMPLETE'


def aggregate(root):
    completed, failed, missing, branches = [], [], [], {}
    started, initializations = 0, 0
    unknown_starts = []
    for case in CASES:
        d = root / case
        p = d / 'worker_result.json'
        if not p.is_file():
            missing.append(case)
            # Preserve a started attempt when a worker was killed before final receipt.
            attempts = list(d.glob('native_attempt.json')) if d.is_dir() else []
            if attempts:
                try:
                    attempt = read(attempts[0])
                    need(attempt['q'] == 'Q-047' and attempt['program_id'] == ID and
                         attempt['case'] == case and attempt['run_id'] == base()['run_id'], 'ATTEMPT_IDENTITY')
                    need(type(attempt['native_processes_started']) is int and
                         attempt['native_processes_started'] == 1, 'ATTEMPT_COUNT')
                    started += attempt['native_processes_started']
                except Exception as e:
                    unknown_starts.append(case)
                    branches[case] = {'attempt_error': str(e), 'attempt_sha256': sha(attempts[0])}
            else:
                unknown_starts.append(case)
            continue
        obj = None
        try:
            obj = read(p)
            okay = branch_gate(d, obj, case)
            started += obj['native_processes_started']
            if obj.get('internal_initializations') is not None:
                initializations += obj['internal_initializations']
            branches[case] = obj
            (completed if okay else failed).append(case)
        except Exception as e:
            failed.append(case)
            unknown_starts.append(case)
            branches[case] = {'rejected_report': obj, 'integrity_error': str(e)}
    need(started <= 4, 'CAMPAIGN_NATIVE_PROCESS_CAP')
    return dict(**base(), execution_status='COMPLETE' if not failed and not missing else 'PARTIAL_OR_FAILED',
                expected_jobs=list(CASES), completed_jobs=completed, failed_jobs=failed, missing_jobs=missing,
                job_completeness_gate='PASS' if not failed and not missing else 'FAIL',
                merge_kind='PROVENANCE_COLLECTION_NO_NUMERICAL_AVERAGING', branches=branches,
                capture_ledger={'native_processes_started': started, 'unknown_start_cases': unknown_starts,
                                'observed_internal_initializations': initializations,
                                'full_cmb_likelihood_evaluations': 0,
                                'inherited_ledger': {'used': 16, 'cap': 52},
                                'accounting_note': 'Four newly authorized bounded capture processes have their own ledger; internal shooting calls are measured, not assumed to cost four inherited units.'},
                historical_state_identity_gate='UNRESOLVED', first_hit_gate='UNRESOLVED',
                scientific_verdict='INSUFFICIENT_EVIDENCE', final_result_gate='UNRESOLVED',
                return_route='RESULT INGESTION & ROUTING ENGINE', automatic_retry=False)


def preserve_dependencies(d, binary, c):
    maps = (d / 'runtime_maps.txt').read_text()
    files = {}
    for line in maps.splitlines():
        row = line.split(maxsplit=5)
        if len(row) == 6 and row[5].startswith('/'):
            need(not row[5].endswith(' (deleted)'), 'DELETED_MAPPED_OBJECT')
            p = Path(row[5]).resolve()
            files[str(p)] = sha(p)
    need(str(binary.resolve()) in files, 'ORIGINAL_CORE_NOT_LOADED')
    dst = d / 'math_dependencies'
    dst.mkdir()
    preserved = {}
    for name in files:
        p = Path(name)
        if p.name.startswith(('libm.so', 'libc.so', 'libgomp.so', 'ld-linux')):
            need(not (dst / p.name).exists(), 'DEPENDENCY_NAME_COLLISION')
            shutil.copyfile(p, dst / p.name)
            preserved[p.name] = {'original_path': name, 'sha256': files[name]}
    need(any(n.startswith('libm.so') for n in preserved) and
         any(n.startswith('libc.so') for n in preserved), 'MATH_LIBRARY_PRESERVATION')
    write(d / 'mapped_dependencies.json', dict(mapped_file_hashes=files, preserved=preserved))
    return files


def worker(case, d):
    d.mkdir(parents=True, exist_ok=False)
    result = dict(**base(), case=case, execution_status='BLOCKED_BEFORE_CAPTURE',
                  native_processes_started=0, internal_initializations=None,
                  full_cmb_likelihood_evaluations=0, structural_gate='UNRESOLVED',
                  runtime_gate='UNRESOLVED', reproduction_gate='UNRESOLVED',
                  scientific_verdict='INSUFFICIENT_EVIDENCE', final_result_gate='UNRESOLVED')
    try:
        contract, frozen = package()
        need(os.environ.get('GITHUB_REPOSITORY') == 'Morfindien/Bubbleverse', 'ORIGINAL_REPOSITORY')
        need(os.environ.get('GITHUB_RUN_ATTEMPT') == '1', 'NO_RUN_REPLAY')
        need(os.environ.get('Q047_CACHE_HIT') == 'true', 'EXACT_CACHE_REQUIRED')
        source = HERE / 'external/class_ede'
        binary = acquire.identify_binary(source, frozen['binary_sha256'])
        from types import SimpleNamespace
        args = SimpleNamespace(source_dir=str(source), binary=str(binary), case=None)
        write(d / 'runtime_preflight.json', state.preflight(args, frozen))
        archive = d / 'original_reference.zip'
        with archive.open('xb') as f, (d / 'reference_download.log').open('x') as log:
            cp = subprocess.run(['gh', 'api', '--method', 'GET',
                  'repos/Morfindien/Bubbleverse/actions/artifacts/' + str(contract['artifacts'][case]['id']) + '/zip'],
                  stdout=f, stderr=log, timeout=240)
        need(cp.returncode == 0, 'REFERENCE_DOWNLOAD')
        bg, th = acquire.original_tables(archive, frozen['cases'][case]['archive_sha256'],
                                        frozen['cases'][case], d / 'golden')
        archive.unlink()
        build = d / 'observer_build'
        build.mkdir()
        ldflags = state.process(['python3-config', '--embed', '--ldflags']).split()
        observer = build / 'q047_observer_v2'
        command = ['gcc', '-std=c11', '-O0', '-fno-fast-math', '-ffp-contract=off', '-rdynamic']
        command += ['-I' + str(source / n) for n in ['include', 'external/HyRec2020', 'external/heating', 'external/RecfastCLASS']]
        command += [str(HERE / 'q047_collect_state_v2.c'), str(binary), '-Wl,-rpath,' + str(binary.parent),
                    '-ldl', '-lm', *ldflags, '-o', str(observer)]
        acquire.command(command, build / 'build.log', 120)
        write(build / 'build_receipt.json', dict(command=command, observer_sha256=sha(observer),
              observer_source_sha256=sha(HERE / 'q047_collect_state_v2.c'), core_sha256=sha(binary),
              core_rebuilt=False, source_commit=frozen['source_commit'], compiler=state.process(['gcc', '--version'])))
        ini = d / 'requested_case.ini'
        ini.write_text(''.join(k + ' = ' + str(v) + '\n' for k, v in frozen['cases'][case]['class_parameters'].items()))
        attempt = dict(**base(), case=case, native_processes_started=1,
                       requested_case_sha256=sha(ini), core_sha256=sha(binary), maximum_seconds=600)
        write(d / 'native_attempt.json', attempt)
        result['native_processes_started'] = 1
        result['execution_status'] = 'CAPTURE_STARTED_NOT_COMPLETE'
        env = dict(os.environ, Q047_CAPTURE_DIR=str(d.resolve()), Q047_CAPTURE_CASE=case,
                   Q047_CAPTURE_AUTHORIZATION='USER_APPROVED_RECONSTRUCTION_V1')
        with (d / 'native.log').open('x') as log:
            proc = subprocess.Popen([str(observer.resolve()), str(ini.resolve())], cwd=source,
                                    stdout=log, stderr=subprocess.STDOUT, env=env, start_new_session=True)
            try:
                code = proc.wait(timeout=600)
            except BaseException:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                raise
        result['native_exit_code'] = code
        need(code == 0, 'NATIVE_CAPTURE_FAILED')
        maps = preserve_dependencies(d, binary, frozen)
        counters = read(d / 'observation_counters.json')
        result['internal_initializations'] = counters['input_shooting_initial_calls'] + counters['final_initial_calls']
        runtime = read(d / 'runtime_control_v2.json')
        result['runtime_control'] = runtime_gate(runtime, case)
        result['runtime_gate'] = 'PASS'
        # V1 receipt and validator stay unchanged and cannot promote a reconstruction.
        write(d / 'capture_receipt.json', dict(case=case, origin='NEW_RECONSTRUCTION',
              execution_status='COMPLETED', lock_sha256=state.LOCK_SHA, binary_sha256=state.BINARY,
              binary_path=str(binary), requested_case_sha256=sha(ini), observer_path=str(observer.resolve()),
              observer_sha256=sha(observer), artifacts={n: sha(d / n) for n in state.REQUIRED_OUTPUTS},
              mapped_file_hashes=maps))
        try:
            result['structural_validation'] = state.validate_state(d, case, frozen)
            result['structural_gate'] = 'PASS'
        except Exception as e:
            result['structural_gate'] = 'FAIL'
            result['structural_error'] = str(e)
        try:
            result['reproduction'] = {'background': state.compare_tables(bg, d / 'native_background.tsv'),
                                      'thermodynamics': state.compare_tables(th, d / 'native_thermodynamics.tsv')}
            result['reproduction_gate'] = 'ALL_BINARY64_OUTPUT_BITS_MATCH'
        except Exception as e:
            result['reproduction_gate'] = 'NOT_MATCHING_ARCHIVE'
            result['reproduction_error'] = str(e)
        # Preserve exact source/header inputs and newly observed mathematical libraries.
        for name in frozen['source_files_sha256']:
            target = d / 'source_objects' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        precision = read(d / 'effective_precision.json')
        data = {}
        bbn = Path(precision['sBBN_file'])
        hyrec = Path(precision['hyrec_path'])
        if not bbn.is_absolute():
            bbn = source / bbn
        if not hyrec.is_absolute():
            hyrec = source / hyrec
        need(hyrec.is_dir(), 'HYREC_DATA_DIRECTORY')
        paths = [bbn]
        paths += sorted(hyrec.glob('*.dat'))
        for i, path in enumerate(paths):
            need(path.is_file(), 'NATIVE_DATA_MISSING')
            target = d / 'native_data' / (str(i) + '-' + path.name)
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(path, target)
            data[str(path)] = {'saved_as': str(target.relative_to(d)), 'sha256': sha(path)}
        write(d / 'native_data.json', data)
        result['execution_status'] = 'CAPTURE_COMPLETE'
    except Exception as e:
        result['error'] = str(e)
        result['failure_class'] = 'EXECUTION_OR_QUALIFICATION_GATE; NOT_PHYSICAL_FALSIFICATION'
    progress = d / 'initialization_progress.jsonl'
    if progress.is_file():
        try:
            result['observed_initialization_progress'] = [read_line for read_line in
                 (state.decode(x) for x in progress.read_text().splitlines())]
            result['internal_initializations'] = len(result['observed_initialization_progress'])
        except Exception as e:
            result['progress_error'] = str(e)
    result['files'] = file_index(d)
    write(d / 'worker_result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['static', 'worker', 'finalize'])
    parser.add_argument('--program-id', required=True)
    parser.add_argument('--case', choices=CASES)
    parser.add_argument('--directory', default='q047_reconstructed')
    parser.add_argument('--output', default='q047_reconstruction_final_v1.json')
    args = parser.parse_args()
    try:
        need(args.program_id == ID, 'PROGRAM_ID_GATE')
        if args.action == 'static':
            package()
            obj = dict(**base(), package_gate='PASS', launcher_gate='PASS', registry_gate='PASS',
                       readme_gate='PASS', repository_consistency_gate='PASS', native_processes_started=0)
        elif args.action == 'worker':
            need(args.case is not None, 'CASE_REQUIRED')
            obj = worker(args.case, Path(args.directory).resolve())
        else:
            package()
            obj = aggregate(Path(args.directory).resolve())
            write(Path(args.output), obj)
        print(json.dumps(obj, indent=2, allow_nan=False))
        return 0 if args.action != 'worker' or obj['execution_status'] == 'CAPTURE_COMPLETE' else 2
    except Exception as e:
        print(json.dumps(dict(**base(), error=str(e), execution_status='BLOCKED_OR_REJECTED',
                             scientific_verdict='INSUFFICIENT_EVIDENCE', final_result_gate='UNRESOLVED')))
        return 2


if __name__ == '__main__':
    sys.exit(main())
