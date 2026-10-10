"""Package, launcher, provenance and mandatory result-set tests."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('q047_package_check_v1'),'Package verifier is required')
        import q047_package_check_v1 as p
        self.p=p

    def test_launcher_exact_lookup_rejects_shell_input_and_unknown(self):
        p=self.p
        registry=p.c.load(ROOT/'bubbleverse_program_registry.json')
        good=p.resolve(registry,p.c.ID)
        self.assertEqual(good['q'],'Q-047')
        for bad in ['Q047-CERTCHECK-V1; echo BAD','Q047-UNKNOWN-V1','$(id)','']:
            with self.assertRaises(ValueError):p.resolve(registry,bad)

    def test_package_identity_and_unchanged_launcher(self):
        result=self.p.static(ROOT)
        self.assertEqual(result['package_gate'],'PASS')
        self.assertEqual(result['launcher_gate'],'PASS')
        self.assertEqual(result['readme_gate'],'PASS')
        self.assertEqual(result['repository_consistency_gate'],'PASS')

    def test_package_rejects_mutated_file(self):
        p=self.p
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            manifest={'q':'Q-047','program_id':p.c.ID,'file_sha256':{'victim.txt':'0'*64}}
            (root/'q047_package_v1.json').write_text(json.dumps(manifest))
            (root/'victim.txt').write_text('wrong')
            with self.assertRaisesRegex(ValueError,'PACKAGE_HASH'):p.verify_hashes(root)

    def test_inherited_registry_entries_cannot_be_changed(self):
        p=self.p
        registry=p.c.load(ROOT/'bubbleverse_program_registry.json')
        manifest=p.c.load(ROOT/'q047_package_v1.json')
        key=manifest['inherited_registry_keys'][0]
        registry['programs'][key]['status']='FORGED'
        with self.assertRaisesRegex(ValueError,'INHERITED_REGISTRY_CHANGED'):
            p.verify_inherited_registry(registry,manifest)

    def test_result_set_rejects_missing_or_forged_final_gate(self):
        p=self.p
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,'OUTPUT_COMPLETENESS'):p.results(root)
            p.c.run(root)
            # A valid job needs the independent regional calculation too.
            with self.assertRaisesRegex(ValueError,'OUTPUT_COMPLETENESS'):p.results(root)
            import subprocess,sys
            got=subprocess.run([sys.executable,str(ROOT/'q047_math_v1.py')],capture_output=True,check=True)
            (root/'q047_regional_controls_v1.json').write_bytes(got.stdout)
            report=p.results(root)
            self.assertEqual(report['technical_result_gate'],'PASS')
            self.assertEqual(report['final_result_gate'],'UNRESOLVED')
            f=root/'q047_certificate_final_v1.json';d=p.c.load(f);d['final_result_gate']='PASS';p.c.write(f,d)
            with self.assertRaisesRegex(ValueError,'FALSE_SCIENTIFIC_CLOSURE'):p.results(root)

if __name__=='__main__':unittest.main(verbosity=2)
