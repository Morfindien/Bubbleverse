"""Regression gates for cleanup packaging; fixtures contain no scientific data."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

VERIFIER = Path(__file__).resolve().parents[1] / 'tools/check_repository_layout.py'


class LayoutTests(unittest.TestCase):
    def module(self):
        self.assertTrue(VERIFIER.is_file(), 'Cleanup verifier is missing')
        spec = importlib.util.spec_from_file_location('layout_verifier', VERIFIER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def fixture(self, root):
        (root / 'docs/cleanup').mkdir(parents=True)
        (root / 'docs/history').mkdir()
        (root / 'archive').mkdir()
        engine = b"if __name__ == '__main__':\n    print('fixture')\n"
        (root / 'engine.py').write_bytes(engine)
        (root / 'alias.py').symlink_to('engine.py')
        (root / 'archive/alias.py').write_bytes(engine)
        (root / 'input.json').write_text('{"fixture":true}\n')
        (root / 'README.md').write_text('[Launches](START_CODES.md)\n')
        (root / 'START_CODES.md').write_text('<!-- entry:fixture-engine -->\n<!-- entry:fixture-alias -->\n')
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        manifest = {'protected_files': [{'path': 'input.json', 'sha256': digest(root / 'input.json'), 'mode': '100644'}],
                    'moves': [{'old_path': 'alias.py', 'new_path': 'archive/alias.py', 'sha256': digest(root / 'engine.py'),
                               'mode': '100644', 'compatibility_target': 'engine.py'}]}
        catalog = {'entries': [{'id': 'fixture-engine', 'source': 'engine.py', 'kind': 'python'},
                               {'id': 'fixture-alias', 'source': 'alias.py', 'kind': 'python'}]}
        lock = {'q': 'FIXTURE', 'file_sha256': {'README.md': digest(root / 'README.md')}}
        (root / 'package.json').write_text(json.dumps(lock))
        (root / 'docs/history/package_before.json').write_text(json.dumps(lock))
        manifest['modified_documentation_lock'] = {
            'path': 'package.json', 'original_copy': 'docs/history/package_before.json',
            'original_sha256': digest(root / 'docs/history/package_before.json')}
        (root / 'docs/cleanup/relocation_manifest.json').write_text(json.dumps(manifest))
        (root / 'docs/cleanup/start_catalog.json').write_text(json.dumps(catalog))
        return manifest, catalog

    def run_fixture(self, mutate=None):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest, catalog = self.fixture(root)
            if mutate:
                mutate(root, manifest, catalog)
            return module.verify(root)

    def test_valid_archive_and_compatibility_alias(self):
        self.assertEqual(self.run_fixture()['status'], 'PASS')

    def test_changed_scientific_input_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'input.json').write_text('changed'))
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any('PROTECTED_HASH' in item for item in result['errors']))

    def test_damaged_archive_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'archive/alias.py').write_text('changed'))
        self.assertTrue(any('ARCHIVE_HASH' in item for item in result['errors']))

    def test_alias_redirect_to_archive_fails(self):
        def mutate(root, *_):
            (root / 'alias.py').unlink()
            (root / 'alias.py').symlink_to('archive/alias.py')
        result = self.run_fixture(mutate)
        self.assertTrue(any('ALIAS_TARGET' in item for item in result['errors']))

    def test_manifest_traversal_fails(self):
        def mutate(root, manifest, _):
            manifest['protected_files'][0]['path'] = '../input.json'
            (root / 'docs/cleanup/relocation_manifest.json').write_text(json.dumps(manifest))
        result = self.run_fixture(mutate)
        self.assertTrue(any('UNSAFE_PATH' in item for item in result['errors']))

    def test_undocumented_entrypoint_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'new_program.py').write_text("print('fixture')\n"))
        self.assertTrue(any('ENTRYPOINT_COVERAGE' in item for item in result['errors']))

    def test_broken_readme_link_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'README.md').write_text('[Lost](missing.md)\n'))
        self.assertTrue(any('DOC_LINK' in item for item in result['errors']))

    def test_missing_start_record_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'START_CODES.md').write_text('empty\n'))
        self.assertTrue(any('START_RECORD' in item for item in result['errors']))

    def test_permission_change_fails(self):
        result = self.run_fixture(lambda root, *_: (root / 'input.json').chmod(0o755))
        self.assertTrue(any('PROTECTED_MODE' in item for item in result['errors']))

    def test_top_level_script_cannot_be_excluded_as_import_only(self):
        def mutate(root, _, catalog):
            (root / 'helper.py').write_text('import argparse\np = argparse.ArgumentParser()\na = p.parse_args()\n')
            catalog['entries'].append({'id': 'fixture-helper', 'source': 'helper.py',
                                       'kind': 'python', 'commands': [],
                                       'exclusion_reason': 'Import-only module'})
            (root / 'docs/cleanup/start_catalog.json').write_text(json.dumps(catalog))
            with (root / 'START_CODES.md').open('a') as stream:
                stream.write('<!-- entry:fixture-helper -->\n')
        result = self.run_fixture(mutate)
        self.assertTrue(any('EXECUTABLE_COMMAND' in item for item in result['errors']))

    def test_documentation_exception_cannot_change_scientific_lock(self):
        def mutate(root, *_):
            lock = json.loads((root / 'package.json').read_text())
            lock['q'] = 'CHANGED'
            (root / 'package.json').write_text(json.dumps(lock))
        result = self.run_fixture(mutate)
        self.assertTrue(any('DOCUMENTATION_LOCK_CHANGE' in item for item in result['errors']))

    def test_preserved_original_lock_cannot_be_rewritten(self):
        result = self.run_fixture(lambda root, *_: (root / 'docs/history/package_before.json').write_text('{}'))
        self.assertTrue(any('ORIGINAL_LOCK_HASH' in item for item in result['errors']))


if __name__ == '__main__':
    unittest.main()
