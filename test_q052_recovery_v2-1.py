"""Real artifact checks and corrupt-object rejection; no native physics."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import q052_native_pair_v2 as m
import q052_recover_native_v2 as recovery

HERE = Path(__file__).resolve().parent


class OriginalObjectRecovery(unittest.TestCase):
    def test_preserved_original_binary_is_copied_bit_for_bit_without_execution(self):
        with tempfile.TemporaryDirectory() as d:
            receipt = recovery.recover(d)
            self.assertEqual(m.sha(Path(d) / 'classy.so'),
                'df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf')
            self.assertFalse(receipt['core_rebuilt'])
            self.assertFalse(receipt['native_executed'])

    def test_corrupt_preserved_binary_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copyfile(HERE / m.CONTRACT, root / m.CONTRACT)
            (root / 'Q052_ORIGINAL_CLASSY_PINNED.so').write_bytes(b'corrupt fixture')
            # Isolate only the filesystem root; validation and copying stay real.
            with patch.object(recovery, 'HERE', root):
                with self.assertRaisesRegex(ValueError, 'PRESERVED_ORIGINAL_BINARY_HASH'):
                    recovery.recover(root / 'output')
            self.assertFalse((root / 'output/classy.so').exists())

    def test_corrupt_archive_is_rejected_before_extraction(self):
        with tempfile.TemporaryDirectory() as d:
            archive = Path(d) / 'bad.zip'
            archive.write_bytes(b'not the pinned archive')
            with self.assertRaisesRegex(ValueError, 'ORIGINAL_OBJECT_ARCHIVE_HASH'):
                recovery.recover(Path(d) / 'out', archive)
            self.assertFalse((Path(d) / 'out/classy.so').exists())

    def test_scientific_lineage_inputs_match_frozen_hashes(self):
        lineage = m.repository_lineage_gate(m.read(HERE / m.CONTRACT))
        self.assertEqual(len(lineage), 4)

    def test_launcher_consumes_the_q052_registry_mapping(self):
        import os, subprocess, sys
        launcher = HERE / '.github/workflows/00-bubbleverse-start.yml'
        if not launcher.exists():
            launcher = HERE / 'launcher_reference_for_tests.yml'
        if not launcher.exists():
            self.skipTest('Local launcher reference absent; integration check performed separately')
        text = launcher.read_text()
        code = text.split("python - <<'PY'\n", 1)[1].split('\n          PY', 1)[0]
        import textwrap
        code = textwrap.dedent(code)
        entry = json.loads((HERE / 'q052_program_registry_patch_v2.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'bubbleverse_program_registry.json').write_text(json.dumps({'programs': {
                entry['program_id']: entry['entry']}}))
            env = dict(os.environ, RAW_PROGRAM_ID='Q052-NATIVEPAIR-V2', GITHUB_OUTPUT=str(root / 'outputs'))
            cp = subprocess.run([sys.executable, '-c', code], cwd=root, env=env,
                                capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
            self.assertIn('q=Q-052\n', (root / 'outputs').read_text())


if __name__ == '__main__':
    unittest.main()
