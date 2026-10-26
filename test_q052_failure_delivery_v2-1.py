"""Regression: empty-worker failures must survive as machine-readable files.

The fixture contains no trajectories and cannot establish a scientific result.
Point Q052_CONTROLLER at V1 to reproduce the original defect.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
CONTROLLER = Path(os.environ.get('Q052_CONTROLLER', HERE / 'q052_native_pair_v2.py'))


class FailureDelivery(unittest.TestCase):
    def test_empty_worker_directory_persists_original_error_and_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            empty = root / 'empty'
            empty.mkdir()
            output = root / 'result.json'
            env = dict(os.environ, GITHUB_RUN_ID='fixture-run', GITHUB_RUN_ATTEMPT='1')
            cp = subprocess.run([sys.executable, str(CONTROLLER), 'collect',
                                 '--directory', str(empty), '--output', str(output)],
                                capture_output=True, text=True, env=env)
            self.assertNotEqual(cp.returncode, 0)
            self.assertTrue(output.is_file(), cp.stdout + cp.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result['execution_status'], 'BLOCKED_OR_FAILED')
            self.assertIn('JOB_COUNT L-nominal 0', result['error'])
            self.assertIsNone(result['actual_computed_result'])
            self.assertFalse(result['scientific_falsification'])
            self.assertEqual(result['run_id'], 'fixture-run')
            self.assertEqual(result['final_result_gate'], 'UNRESOLVED')

    def test_upstream_failure_preserves_branch_and_original_log(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            log = root / 'native.log'
            log.write_text('fixture: exact environment unavailable\n')
            output = root / 'branch_failure.json'
            cp = subprocess.run([sys.executable, str(CONTROLLER), 'failure',
                '--output', str(output), '--stage', 'NATIVE_JOB', '--arm', 'R',
                '--mode', 'refined', '--error', 'setup failure', '--log', str(log)],
                capture_output=True, text=True)
            self.assertEqual(cp.returncode, 2)
            report = json.loads(output.read_text())
            self.assertEqual((report['arm'], report['mode']), ('R', 'refined'))
            self.assertEqual(report['original_error_text'], log.read_text())
            self.assertIsNone(report['actual_computed_result'])


if __name__ == '__main__':
    unittest.main()
