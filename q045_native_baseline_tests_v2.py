"""Offline integrity tests. Synthetic fixtures are never scientific results."""
import copy, importlib.util, json, tempfile, unittest, zipfile
from unittest.mock import patch
from pathlib import Path

class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path(__file__).with_name('q045_native_baseline_v2.py')
        cls.engine=None
        if p.exists():
            s=importlib.util.spec_from_file_location('baseline',p)
            cls.engine=importlib.util.module_from_spec(s);s.loader.exec_module(cls.engine)
    def engine_ready(self):
        self.assertIsNotNone(self.engine,'Baseline integrity implementation is absent')
        return self.engine
    def test_missing_build_backend_fails_before_editable_install(self):
        m=self.engine_ready()
        with patch('importlib.metadata.version',return_value='3.12.0'), \
             patch('importlib.import_module',side_effect=ModuleNotFoundError('flit_core')):
            with self.assertRaisesRegex(ValueError,'BUILD_BACKEND_GATE'):
                m.build_backend_preflight()
    def test_wrong_build_backend_version_is_rejected(self):
        m=self.engine_ready()
        with patch('importlib.metadata.version',return_value='4.0.0'):
            with self.assertRaisesRegex(ValueError,'BUILD_BACKEND_GATE'):
                m.build_backend_preflight()
    def test_missing_fourth_job_cannot_complete(self):
        m=self.engine_ready()
        with tempfile.TemporaryDirectory() as td:
            result=m.collect(Path(td),Path(td)/'final.json')
            self.assertEqual(result['job_completeness_gate'],'FAIL')
            self.assertEqual(result['final_result_gate'],'UNRESOLVED')
            self.assertFalse(result['scientific_result'])
    def test_three_completed_jobs_remain_visible_when_fourth_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root)
            import shutil
            shutil.rmtree(root/m.contract()['expected_jobs'][-1])
            r=m.collect(root,root/'final.json')
            self.assertEqual(r['job_completeness_gate'],'FAIL')
            self.assertEqual(len(r['completed_jobs']),3)
    def test_zip_path_traversal_is_rejected(self):
        m=self.engine_ready()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'input.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('../escaped','bad')
            with self.assertRaisesRegex(ValueError,'ARCHIVE_PATH'):m.extract(p,Path(td)/'out')
            self.assertFalse((Path(td)/'escaped').exists())
    def test_duplicate_json_cannot_hide_q(self):
        m=self.engine_ready()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.json';p.write_text('{"q":"Q-042","q":"Q-045"}')
            with self.assertRaisesRegex(ValueError,'DUPLICATE'):m.read(p)
    def test_nonfinite_input_rejected(self):
        m=self.engine_ready()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.json';p.write_text('{"loglike":NaN}')
            with self.assertRaises(ValueError):m.read(p)
    def test_unsafe_program_id_rejected_before_lookup(self):
        m=self.engine_ready()
        for s in ('Q045-BASELINE-V2;touch bad','$(id)','../Q045-BASELINE-V2'):
            with self.assertRaisesRegex(ValueError,'PROGRAM_ID'):m.check_id(s)

    def fixture(self,root):
        m=self.engine_ready();c=m.contract();b=m.base()
        for key in c['expected_jobs']:
            d=root/key;d.mkdir()
            for name in ('sampled_vector.json','likelihood.json','product_manifest.json'):
                m.write(d/name,dict(**b,job_id=key,fixture_only=True))
            m.write(d/'runtime_input_manifest.json',dict(**b,job_id=key,fixture_only=True,
                     external_signature={'same_external_data':True}))
            for name in ('spectra.tsv','background.tsv','thermodynamics.tsv','native.log'):
                (d/name).write_text('synthetic integrity fixture, not data\n')
            files={p.name:m.sha(p) for p in d.iterdir()}
            m.write(d/m.RESULT,dict(**b,job_id=key,status='COMPLETE',artifacts=files,
               provenance={'class_binary_sha256':c['class_binary_sha256'],'cached_data_sha256':{'file':'frozen-fixture'}}))
        return m

    def test_four_integrity_fixtures_still_cannot_pass_scientific_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root);r=m.collect(root,root/'final.json')
            self.assertEqual(r['job_completeness_gate'],'PASS')
            self.assertEqual(r['final_result_gate'],'UNRESOLVED')
            self.assertFalse(r['scientific_result'])

    def test_tampered_spectrum_cannot_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root)
            next(root.glob('*/spectra.tsv')).write_text('changed bytes')
            r=m.collect(root,root/'final.json')
            self.assertEqual(r['merge_compatibility_gate'],'FAIL')
            self.assertIn('RESULT_ARTIFACT_HASH',r['errors'][0])

    def test_different_external_data_cannot_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root);p=next(root.glob('*/'+m.RESULT))
            r=m.read(p);r['provenance']['cached_data_sha256']={'file':'different'};m.write(p,r)
            r=m.collect(root,root/'final.json')
            self.assertEqual(r['merge_compatibility_gate'],'FAIL')
            self.assertIn('MATCHED_EXTERNAL_INPUT',r['errors'][0])

    def test_wrong_q_cannot_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root);p=next(root.glob('*/'+m.RESULT))
            r=m.read(p);r['q']='Q-042';m.write(p,r)
            r=m.collect(root,root/'final.json')
            self.assertEqual(r['merge_compatibility_gate'],'FAIL')
            self.assertIn('MERGE_IDENTITY q',r['errors'][0])

if __name__=='__main__':unittest.main(verbosity=2)
