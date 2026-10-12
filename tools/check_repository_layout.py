#!/usr/bin/env python3
"""Read-only cleanup gates. No downloads, dispatch, compilation or campaign work."""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys


def verify(root):
    root = Path(root).resolve()
    errors = []
    checked = 0

    def path(name):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not relative.parts:
            raise ValueError('UNSAFE_PATH ' + name)
        candidate = root / relative
        if not candidate.resolve().is_relative_to(root):
            raise ValueError('UNSAFE_PATH ' + name)
        return candidate

    def digest(candidate):
        return hashlib.sha256(candidate.read_bytes()).hexdigest()

    try:
        manifest = json.loads((root / 'docs/cleanup/relocation_manifest.json').read_text())
        catalog = json.loads((root / 'docs/cleanup/start_catalog.json').read_text())
    except (OSError, ValueError) as error:
        return {'status': 'FAIL', 'errors': [str(error)], 'checked_files': 0}

    for row in manifest['protected_files']:
        try:
            candidate = path(row['path'])
            if candidate.is_symlink() or digest(candidate) != row['sha256']:
                errors.append('PROTECTED_HASH ' + row['path'])
            mode = '100755' if candidate.stat().st_mode & 0o111 else '100644'
            if mode != row['mode']:
                errors.append('PROTECTED_MODE ' + row['path'])
            checked += 1
        except (OSError, ValueError) as error:
            errors.append(str(error))

    for row in manifest['moves']:
        try:
            archived = path(row['new_path'])
            if archived.is_symlink() or digest(archived) != row['sha256']:
                errors.append('ARCHIVE_HASH ' + row['new_path'])
            mode = '100755' if archived.stat().st_mode & 0o111 else '100644'
            if mode != row['mode']:
                errors.append('ARCHIVE_MODE ' + row['new_path'])
            old = path(row['old_path'])
            target = row.get('compatibility_target')
            if target:
                canonical = path(target)
                if (not old.is_symlink() or os.readlink(old) != target
                        or canonical.is_symlink() or digest(old) != row['sha256']):
                    errors.append('ALIAS_TARGET ' + row['old_path'])
            elif old.exists() or old.is_symlink():
                errors.append('OLD_PATH_COLLISION ' + row['old_path'])
            checked += 1
        except (OSError, ValueError) as error:
            errors.append(str(error))

    if 'modified_documentation_lock' in manifest:
        try:
            exception = manifest['modified_documentation_lock']
            original_path = path(exception['original_copy'])
            if digest(original_path) != exception['original_sha256']:
                errors.append('ORIGINAL_LOCK_HASH ' + exception['original_copy'])
            original = json.loads(original_path.read_text())
            current = json.loads(path(exception['path']).read_text())
            if current['file_sha256']['README.md'] != digest(root / 'README.md'):
                errors.append('README_LOCK_HASH')
            comparable = copy.deepcopy(current)
            comparable['file_sha256']['README.md'] = original['file_sha256']['README.md']
            if comparable != original:
                errors.append('DOCUMENTATION_LOCK_CHANGE ' + exception['path'])
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append('DOCUMENTATION_LOCK_CHANGE ' + str(error))

    entries = catalog['entries']
    recorded = {row['source'] for row in entries}
    discovered = {p.relative_to(root).as_posix() for pattern in ('*.py', '*.sh') for p in root.glob(pattern)}
    discovered.update(p.relative_to(root).as_posix() for p in (root / '.github/workflows').glob('*.y*ml'))
    discovered.update(p.relative_to(root).as_posix() for p in (root / '.github/workflows').glob('*.py'))
    if (root / 'action.yml').is_file():
        discovered.add('action.yml')
    for name in sorted(discovered - recorded):
        errors.append('ENTRYPOINT_COVERAGE ' + name)
    ids = [row['id'] for row in entries]
    if len(ids) != len(set(ids)):
        errors.append('DUPLICATE_START_ID')
    try:
        start = (root / 'START_CODES.md').read_text()
        for row in entries:
            if '<!-- entry:' + row['id'] + ' -->' not in start:
                errors.append('START_RECORD ' + row['id'])
            source = path(row['source'])
            if not source.is_file():
                errors.append('START_SOURCE ' + row['source'])
            elif row['kind'] in ('python', 'support_python') and not row.get('commands'):
                tree = ast.parse(source.read_text())
                top_level = [node for node in tree.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                executable = any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                                 and node.func.attr in ('parse_args', 'write_text', 'write_bytes')
                                 for statement in top_level for node in ast.walk(statement))
                if executable:
                    errors.append('EXECUTABLE_COMMAND ' + row['source'])
    except (OSError, ValueError) as error:
        errors.append(str(error))

    docs = [root / 'README.md', root / 'START_CODES.md']
    docs.extend((root / 'cases').glob('*/README.md'))
    for document in docs:
        try:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
                target = target.split('#', 1)[0]
                if not target or re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', target):
                    continue
                if not (document.parent / target).is_file():
                    errors.append('DOC_LINK ' + str(document.relative_to(root)) + ' -> ' + target)
        except OSError as error:
            errors.append(str(error))
    return {'status': 'FAIL' if errors else 'PASS', 'errors': errors,
            'checked_files': checked, 'catalog_entries': len(entries),
            'scope': 'Layout, hashes, permissions, aliases, launch coverage and relative links only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = verify(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
