#!/usr/bin/env python3
"""Finite regression tests for diagnostic integrity; no cosmological compute."""
import hashlib
import io
import tempfile
import unittest
import zipfile
import warnings
import os
from pathlib import Path
import q042_stock_diagnostic_v20 as d

class DiagnosticTests(unittest.TestCase):
    def test_runtime_infinity_is_preserved_as_explicit_metadata(self):
        import json
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'a.json'
            d.write_json(path,{'max_ndead':float('inf')})
            self.assertEqual(json.loads(path.read_text()),{'max_ndead':'infinity'})
    def test_stock_header_has_numeric_progress_not_just_mtime(self):
        text='=== Number of dimensions ===\n18\n=== Number of dead points/iterations ===\n4051\n=== Number of live points in each cluster ===\n450\n=== Number of likelihood calls ===\n4509 59 499 299 1910\n'
        self.assertEqual(d.stock_header(text).get('ndead'),4051)
        self.assertEqual(d.stock_header(text).get('nlike'),[4509,59,499,299,1910])

    def test_replacements_without_checkpoint_are_not_durable_progress(self):
        before={'ndead':4051,'sha256':'same'}
        after={'ndead':4051,'sha256':'same'}
        log='Q042_DIAG_BEGIN 4051\nQ042_DIAG_REPLACE 4052\nQ042_DIAG_REPLACE 4053\n'
        r=d.diagnose(before,after,log)
        self.assertEqual(r.get('diagnosis'),'IN_MEMORY_PROGRESS_WITHOUT_DURABLE_UPDATE')
        self.assertFalse(r.get('production_restart_authorized',True))

    def test_touched_file_does_not_count_as_sampler_progress(self):
        r=d.diagnose({'ndead':4051,'sha256':'a'},{'ndead':4051,'sha256':'b'},'')
        self.assertEqual(r.get('diagnosis'),'NO_COMPLETE_REPLACEMENT_OBSERVED')

    def test_durable_progress_remains_diagnostic_only(self):
        r=d.diagnose({'ndead':4051,'sha256':'a'},{'ndead':4502,'sha256':'b'},'Q042_DIAG_REPLACE 4502\n')
        self.assertEqual(r.get('diagnosis'),'DURABLE_PROGRESS_OBSERVED')
        self.assertFalse(r.get('production_restart_authorized',True))

    def test_zip_hash_failure_writes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);z=p/'a.zip'
            with zipfile.ZipFile(z,'w') as f:f.writestr('valid.txt','raw')
            with self.assertRaises(ValueError):d.extract_verified(z,'0'*64,p/'out')
            self.assertFalse((p/'out').exists())

    def test_unsafe_and_duplicate_zip_members_write_nothing(self):
        for names in [['../escape'],['valid','../escape'],['valid','valid']]:
            with tempfile.TemporaryDirectory() as t:
                p=Path(t);z=p/'a.zip'
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore',UserWarning)
                    with zipfile.ZipFile(z,'w') as f:
                        for n in names:f.writestr(n,'raw')
                with self.assertRaises(ValueError):d.extract_verified(z,hashlib.sha256(z.read_bytes()).hexdigest(),p/'out')
                self.assertFalse((p/'out').exists())

    def test_observer_changes_only_removable_output_statements(self):
        p=Path(os.environ.get('Q042_PINNED_NESTED_SOURCE',str(Path(__file__).parent.parent/'evidence/polychord_nested_sampling_pinned.F90')))
        if not p.exists():self.skipTest('pinned reference tested separately in workflow')
        s=p.read_text();patched=d.observer_source(s)
        self.assertEqual(d.remove_observer(patched),s)
        self.assertEqual(d.observer_source(patched),patched)
        with self.assertRaises(ValueError):d.observer_source(s.replace('if(replace_point(settings,RTI,baby_points,cluster_id)) then','changed'))

    def test_supervisor_kills_uncooperative_process(self):
        import sys
        with tempfile.TemporaryDirectory() as t:
            r=d.supervise([sys.executable,'-c','import signal,time;signal.signal(signal.SIGINT,signal.SIG_IGN);signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)'],Path(t)/'log',0.2,0.1)
            self.assertTrue(r.get('timed_out'))
            self.assertEqual(r.get('returncode'),-9)

if __name__=='__main__':unittest.main()
