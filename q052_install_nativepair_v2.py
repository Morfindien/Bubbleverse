"""Guarded add-only registry install and README prefix; launcher stays untouched."""
from pathlib import Path
import argparse
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def install(apply=False):
    manifest = json.loads((HERE / 'Q052_INSTALL_MANIFEST_V2.json').read_text())
    for name, expected in manifest['package_files'].items():
        path = HERE / name
        if not path.is_file() or digest(path) != expected:
            raise ValueError('PACKAGE_FILE_HASH ' + name)
    patch = json.loads((HERE / 'q052_program_registry_patch_v2.json').read_text())
    registry_path = HERE / 'bubbleverse_program_registry.json'
    registry = json.loads(registry_path.read_text())
    program_id = patch['program_id']
    entry = patch['entry']
    if entry['q'] != 'Q-052' or entry['scientific_q'] != 'Q052':
        raise ValueError('LAUNCHER_Q_MAPPING')
    existing = registry['programs'].get(program_id)
    if existing is not None and existing != entry:
        raise ValueError('EXISTING_TARGET_CONFLICT')
    if existing is None and digest(registry_path) != manifest['base_registry_sha256']:
        raise ValueError('REGISTRY_BASE_CHANGED_RECONCILE_FIRST')
    readme_path = HERE / 'README.md'
    readme = readme_path.read_text()
    prefix = manifest['readme_prefix']
    marker = '# Q052 native pair V2 — exact original object recovery'
    if marker in readme and not readme.startswith(prefix):
        raise ValueError('README_PREFIX_CONFLICT')
    if marker not in readme and digest(readme_path) != manifest['base_readme_sha256']:
        raise ValueError('README_BASE_CHANGED_RECONCILE_FIRST')
    status = 'INSTALLED' if existing == entry and readme.startswith(prefix) else 'INSTALLABLE'
    if apply:
        registry['programs'][program_id] = entry
        if not readme.startswith(prefix):
            readme = prefix + readme
        # All guards above pass before either active file is changed.
        for path, text in [(registry_path, json.dumps(registry, indent=2, ensure_ascii=False) + '\n'),
                           (readme_path, readme)]:
            temporary = path.with_name(path.name + '.q052-v2.tmp')
            temporary.write_text(text)
            os.replace(temporary, path)
        status = 'INSTALLED'
    return {'q': 'Q052', 'program_id': program_id, 'status': status,
            'launcher_modified': False, 'workflow_dispatched': False,
            'registry_q': 'Q-052', 'scientific_q': 'Q052'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.apply), indent=2))
        return 0
    except Exception as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
