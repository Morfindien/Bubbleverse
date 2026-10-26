"""Installer tests use real files and real guarded mutations in temporary roots."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import q052_install_nativepair_v2 as installer

HERE = Path(__file__).resolve().parent


class GuardedInstallation(unittest.TestCase):
    def prepare(self, root):
        manifest = json.loads((HERE / 'Q052_INSTALL_MANIFEST_V2.json').read_text())
        for name in ['Q052_INSTALL_MANIFEST_V2.json'] + list(manifest['package_files']):
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / name, destination)
        # A separately labelled synthetic active-state base keeps the regression
        # independent of whether the real repository is already installed.
        registry = root / 'bubbleverse_program_registry.json'
        registry.write_text(json.dumps({'programs': {'EXISTING-TARGET': {
            'q': 'Q-001', 'status': 'ACTIVE', 'historical_field': 'preserve'}}}, indent=2) + '\n')
        readme = root / 'README.md'
        readme.write_text('# Synthetic fixture: preserved operational history\n')
        manifest['base_registry_sha256'] = installer.digest(registry)
        manifest['base_readme_sha256'] = installer.digest(readme)
        (root / 'Q052_INSTALL_MANIFEST_V2.json').write_text(json.dumps(manifest))

    def test_add_only_install_preserves_history_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.prepare(root)
            original = json.loads((root / 'bubbleverse_program_registry.json').read_text())
            old_readme = (root / 'README.md').read_text()
            with patch.object(installer, 'HERE', root):
                self.assertEqual(installer.install()['status'], 'INSTALLABLE')
                installer.install(True)
                first = (root / 'bubbleverse_program_registry.json').read_bytes()
                installer.install(True)
                self.assertEqual(first, (root / 'bubbleverse_program_registry.json').read_bytes())
            current = json.loads(first)
            for key, value in original['programs'].items():
                self.assertEqual(current['programs'][key], value)
            self.assertEqual(current['programs']['Q052-NATIVEPAIR-V2']['q'], 'Q-052')
            self.assertTrue((root / 'README.md').read_text().endswith(old_readme))

    def test_changed_registry_base_blocks_all_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.prepare(root)
            registry = root / 'bubbleverse_program_registry.json'
            registry.write_text(registry.read_text() + '\n')
            old = (root / 'README.md').read_bytes()
            with patch.object(installer, 'HERE', root):
                with self.assertRaisesRegex(ValueError, 'REGISTRY_BASE_CHANGED'):
                    installer.install(True)
            self.assertEqual((root / 'README.md').read_bytes(), old)
            self.assertNotIn('Q052-NATIVEPAIR-V2', json.loads(registry.read_text())['programs'])


if __name__ == '__main__':
    unittest.main()
