#!/usr/bin/env python3
"""Q047 bounded orchestration; reuse V1 capture; never rebuild CLASS or dispatch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
ID = 'Q047-COLLECTION-PREFLIGHT-V1'
Q = 'Q-047'
WORKFLOW = 'q047-collection-preflight-v1.yml'
REPO = 'Morfindien/Bubbleverse'
CASES = ('camspec-lcdm', 'camspec-ede_n3', 'hillipop-lcdm', 'hillipop-ede_n3')

def need(ok, why):
    if not ok:
        raise ValueError(why)

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'DUPLICATE_KEY ' + k)
        d[k] = v
    return d

def read(p):
    return json.loads(Path(p).read_text(), object_pairs_hook=unique,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()

def write(p, d):
    with Path(p).open('x') as f:
        json.dump(d, f, indent=2, allow_nan=False)
        f.write('\n')

def base():
    return dict(q=Q, program_id=ID, program_version='v1', workflow_version='v1',
        run_id=os.environ.get('GITHUB_RUN_ID', 'LOCAL'),
        run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT', 'LOCAL'),
        execution_commit=os.environ.get('GITHUB_SHA', 'LOCAL'),
        checked_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        final_result_gate='UNRESOLVED', scientific_verdict='INSUFFICIENT_EVIDENCE',
        return_route='RESULT INGESTION & ROUTING ENGINE')

def package(root=HERE):
    p = read(root / 'Q047_EXECUTION_PACKAGE_V1.json')
    need(p['q'] == Q and p['program_id'] == ID and tuple(p['cases']) == CASES, 'PACKAGE_IDENTITY')
    for name, digest in p['file_sha256'].items():
        need((root / name).is_file() and sha(root / name) == digest, 'PACKAGE_FILE ' + name)
    c = read(root / 'Q047_COLLECTION_LOCK_V1.json')
    need(c['q'] == Q and c['question'] == p['question'] and set(c['cases']) == set(CASES), 'SCIENCE_LOCK')
    reg = read(root / 'bubbleverse_program_registry.json')['programs']
    need(ID in reg and reg[ID]['q'] == Q and reg[ID]['status'] == 'ACTIVE', 'REGISTRY_ID')
    need(reg[ID]['workflow_id'] == WORKFLOW and reg[ID]['workflow_path'] == '.github/workflows/' + WORKFLOW,
        'REGISTRY_TARGET')
    need(reg[ID]['version'] == reg[ID]['program_version'] == reg[ID]['workflow_version'] == 'v1', 'REGISTRY_VERSION')
    need((root / reg[ID]['workflow_path']).is_file(), 'WORKFLOW_MISSING')
    readme = (root / 'README.md').read_text()
    for s in (ID, WORKFLOW, 'bubbleverse_program_registry.json', '00-bubbleverse-start.yml'):
        need(s in readme, 'README_REFERENCE ' + s)
    journal = (root / 'Q047_SAMLET_JOURNAL.md').read_text()
    need(c['question'] in journal and 'K-PROPOSED-Q047-' in journal and 'INSUFFICIENT_EVIDENCE' in journal,
        'JOURNAL_CONTINUITY')
    return p, c

def command(argv, log, timeout):
    # No shell interpolation. One attempt, with finite wall time.
    with Path(log).open('x') as f:
        completed = subprocess.run(argv, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
    need(completed.returncode == 0, 'COMMAND_FAILED ' + Path(log).name)

def original_tables(archive, digest, expected, out):
    need(sha(archive) == digest, 'ORIGINAL_ARCHIVE_HASH')
    out.mkdir(parents=True, exist_ok=False)
    wanted = {'background.tsv': expected['background_sha256'],
              'thermodynamics.tsv': expected['thermodynamics_sha256']}
    found = {}
    index = []
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        need(len(infos) <= 256 and len({i.filename for i in infos}) == len(infos), 'ARCHIVE_MEMBERS')
        need(sum(i.file_size for i in infos) <= 512 * 1024 * 1024, 'ARCHIVE_EXPANSION_CAP')
        for i in infos:
            if i.is_dir():
                continue
            h = hashlib.sha256()
            with z.open(i) as f:
                for b in iter(lambda: f.read(1048576), b''):
                    h.update(b)
            digest_i = h.hexdigest()
            index.append(dict(member=i.filename, bytes=i.file_size, sha256=digest_i))
            for name, target in wanted.items():
                if digest_i == target:
                    need(name not in found, 'DUPLICATE_GOLDEN_MEMBER')
                    # Select by digest; never extract caller-controlled paths.
                    with z.open(i) as src, (out / name).open('xb') as dst:
                        for b in iter(lambda: src.read(1048576), b''):
                            dst.write(b)
                    found[name] = i.filename
    need(set(found) == set(wanted), 'GOLDEN_MEMBERS_MISSING')
    write(out / 'original_member_index.json', dict(index=index, selected=found, archive_sha256=sha(archive)))
    return out / 'background.tsv', out / 'thermodynamics.tsv'

def identify_binary(source, expected):
    matches = [p.resolve() for p in source.rglob('classy*.so') if p.is_file() and sha(p) == expected]
    need(matches, 'ORIGINAL_BINARY_NOT_IN_RESTORED_CACHE')
    # Equal bytes can exist in the Python build and install trees. Use stable source path.
    return sorted(set(matches), key=lambda p: str(p))[0]

def worker(out):
    out.mkdir(parents=True, exist_ok=False)
    p, c = package()
    need(os.environ.get('GITHUB_REPOSITORY') == REPO, 'ORIGINAL_REPOSITORY_REQUIRED')
    need(os.environ.get('GITHUB_RUN_ATTEMPT') == '1', 'NO_AUTOMATIC_RUN_REPLAY')
    need(os.environ.get('Q047_CACHE_HIT') == 'true', 'EXACT_CACHE_HIT_REQUIRED')
    source = HERE / 'external/class_ede'
    binary = identify_binary(source, c['binary_sha256'])
    driver = HERE / 'q047_collection_v1.py'
    common = [sys.executable, str(driver)]
    native = ['--source-dir', str(source), '--binary', str(binary)]
    manifest = dict(**base(), expected_cases=list(CASES),
        source_commit=c['source_commit'], binary_sha256=c['binary_sha256'],
        collection_lock_sha256=sha(HERE / 'Q047_COLLECTION_LOCK_V1.json'),
        execution_package_sha256=sha(HERE / 'Q047_EXECUTION_PACKAGE_V1.json'),
        journal_sha256=sha(HERE / 'Q047_SAMLET_JOURNAL.md'), budget_before=c['budget'],
        new_native_or_theory_evaluations=0, initialized_cases=[], core_rebuilt=False,
        capture_gate='UNRESOLVED_SHOOTING_ACCOUNTING_UNIT',
        qualified_precursor_packet_created=False, retry_configured=False, files={})
    write(out / 'worker_start.json', manifest)
    command(common + ['preflight'] + native, out / 'runtime_preflight.json', 120)
    goldens = {}
    # All four original inputs qualify before any native initialization.
    for case in CASES:
        archive = out / (case + '.zip')
        with archive.open('xb') as f, (out / (case + '_download.log')).open('x') as log:
            r = subprocess.run(['gh', 'api', '--method', 'GET',
                'repos/' + REPO + '/actions/artifacts/' + str(p['artifacts'][case]['id']) + '/zip'],
                stdout=f, stderr=log, timeout=240)
        need(r.returncode == 0, 'ORIGINAL_ARTIFACT_DOWNLOAD ' + case)
        goldens[case] = original_tables(archive, c['cases'][case]['archive_sha256'],
            c['cases'][case], out / 'golden' / case)
        bg, th = goldens[case]
        command(common + ['preflight'] + native + ['--case', case, '--baseline-background', str(bg),
            '--baseline-thermal', str(th)], out / (case + '_preflight.json'), 120)
    build = out / 'observer_build'
    command(common + ['build-observer'] + native + ['--output', str(build)], out / 'build.json', 180)
    # Preserve the recovered binary as an individual object; do not execute it.
    objects = out / 'original_objects'; objects.mkdir()
    import shutil
    shutil.copyfile(binary, objects / 'classy.so')
    for name in c['source_files_sha256']:
        target = out / 'original_sources' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    manifest['execution_status'] = 'PREFLIGHT_COMPLETE_NO_NATIVE_WORK'
    manifest['files'] = {str(f.relative_to(out)): sha(f) for f in sorted(out.rglob('*'))
        if f.is_file() and f.suffix != '.zip' and f.name != 'worker_start.json'}
    write(out / 'worker_manifest.json', manifest)


def aggregate(root, manifest):
    b = base()
    for name in ('q', 'program_id', 'run_id', 'run_attempt', 'execution_commit'):
        need(manifest[name] == b[name], 'MERGE_IDENTITY ' + name)
    need(manifest['expected_cases'] == list(CASES), 'EXPECTED_CASE_SET')
    need(manifest['execution_status'] == 'PREFLIGHT_COMPLETE_NO_NATIVE_WORK' and
        manifest['new_native_or_theory_evaluations'] == 0 and manifest['initialized_cases'] == [] and
        manifest['core_rebuilt'] is False, 'NO_NATIVE_WORK_GATE')
    p, c = package()
    need(manifest['source_commit'] == c['source_commit'] and manifest['binary_sha256'] == c['binary_sha256'], 'MERGE_SOURCE')
    need(manifest['collection_lock_sha256'] == sha(HERE / 'Q047_COLLECTION_LOCK_V1.json') and
        manifest['execution_package_sha256'] == sha(HERE / 'Q047_EXECUTION_PACKAGE_V1.json') and
        manifest['journal_sha256'] == sha(HERE / 'Q047_SAMLET_JOURNAL.md'), 'MERGE_INPUTS')
    mandatory = {'runtime_preflight.json', 'build.json', 'original_objects/classy.so',
        'observer_build/observer_build_receipt.json', 'observer_build/q047_observer', 'observer_build/observer_build.log'}
    for case in CASES:
        mandatory |= {case + '_download.log', case + '_preflight.json', 'golden/' + case + '/background.tsv',
            'golden/' + case + '/thermodynamics.tsv', 'golden/' + case + '/original_member_index.json'}
    mandatory |= {'original_sources/' + name for name in c['source_files_sha256']}
    need(set(manifest['files']) == mandatory, 'OUTPUT_COMPLETENESS_GATE')
    for name, digest in manifest['files'].items():
        # Paths are fixed by the equality above, never supplied to extraction/shell.
        f = root / name
        need(f.is_file() and not f.is_symlink() and sha(f) == digest, 'OUTPUT_HASH ' + name)
    need(sha(root / 'original_objects/classy.so') == c['binary_sha256'], 'RECOVERED_ORIGINAL_BINARY_HASH')
    pf = read(root / 'runtime_preflight.json')
    need(pf['binary_sha256'] == c['binary_sha256'] and pf['source_commit'] == c['source_commit'] and
        pf['python'] == '3.11.16' and pf['native_library_loaded'] is False and pf['initialization_executed'] is False,
        'PREFLIGHT_RECORD')
    br = read(root / 'observer_build/observer_build_receipt.json')
    need(br['binary_sha256'] == c['binary_sha256'] and br['source_commit'] == c['source_commit'] and
        br['observer_source_sha256'] == c['observer_source_sha256'] and br['core_rebuilt'] is False and
        br['native_initialization_executed'] is False and br['observer_sha256'] == sha(root / 'observer_build/q047_observer'),
        'OBSERVER_BUILD_RECORD')
    for name, digest in c['source_files_sha256'].items():
        need(sha(root / 'original_sources' / name) == digest, 'ORIGINAL_SOURCE_HASH')
    for case in CASES:
        d = root / 'golden' / case
        need(sha(d / 'background.tsv') == c['cases'][case]['background_sha256'] and
            sha(d / 'thermodynamics.tsv') == c['cases'][case]['thermodynamics_sha256'], 'GOLDEN_IDENTITY')
        cp = read(root / (case + '_preflight.json'))
        need(all(cp[k] == pf[k] for k in ('source_commit', 'binary_sha256', 'binary_path', 'python', 'platform', 'native_library_loaded', 'initialization_executed')), 'CASE_RUNTIME_IDENTITY')
    return dict(**b, execution_status='PREFLIGHT_COMPLETE_NO_NATIVE_WORK',
        result_status='ORIGINAL_OBJECTS_RECOVERED_AND_CHECKED; NO_CAPTURE_RESULT',
        job_completeness_gate='PASS', merge_compatibility_gate='PASS', new_native_or_theory_evaluations=0,
        native_capture='NOT_EXECUTED', budget_before=manifest['budget_before'], budget_after=manifest['budget_before'],
        source_continuum_admission='UNRESOLVED', capture_gate='UNRESOLVED_SHOOTING_ACCOUNTING_UNIT',
        PT01='UNRESOLVED', PT03='UNRESOLVED', recovered_file_sha256=manifest['files'],
        next_action='Use preserved original core/reference/build objects. Define a justified bounded shooting/capture accounting policy before a separately versioned capture campaign. No unchanged preflight replay.')


def finalize(root, out):
    try:
        result = aggregate(root, read(root / 'worker_manifest.json'))
        code = 0
    except Exception as e:
        result = dict(**base(), execution_status='INCOMPLETE_OR_REJECTED', result_status='NOT_AVAILABLE',
            job_completeness_gate='FAIL', merge_compatibility_gate='UNRESOLVED', error=str(e),
            next_action='Inspect preserved failure/stage logs; change the concrete failed condition before any new campaign.')
        code = 2
    write(out, result)
    return code

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['static', 'worker', 'finalize'])
    ap.add_argument('--directory', default='q047_capture')
    ap.add_argument('--output', default='q047_collection_preflight_final_v1.json')
    ap.add_argument('--program-id', required=True)
    a = ap.parse_args()
    try:
        need(a.program_id == ID, 'EXACT_PROGRAM_ID')
        if a.action == 'static':
            package()
            print(json.dumps(dict(**base(), package_gate='PASS', README_GATE='PASS',
                native_work='NOT_EXECUTED', repository_consistency_gate='PASS')))
        elif a.action == 'worker':
            worker(Path(a.directory).resolve())
        else:
            return finalize(Path(a.directory).resolve(), Path(a.output))
        return 0
    except Exception as e:
        print(json.dumps(dict(**base(), error=str(e), execution_status='BLOCKED_OR_REJECTED')))
        return 2

if __name__ == '__main__':
    sys.exit(main())
