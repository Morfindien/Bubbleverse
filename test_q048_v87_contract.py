"""Contract regression: old V79 omission must fail before science."""
import json, sys, unittest, hashlib, importlib.util
from pathlib import Path

SPEC=Path(sys.argv.pop(1)) if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1].endswith('.json') else Path(__file__).with_name('q048_frec_moving_h_spec_v87.json')

class ContractRegression(unittest.TestCase):
    def test_contract_hash_present_before_any_producer(self):
        self.assertIsNotNone(importlib.util.find_spec('q048_v87_consumer_contract'),'V87 metadata implementation missing')
        spec=json.loads(SPEC.read_text())
        self.assertTrue(isinstance(spec.get('contract_markdown_sha256'),str), 'REGRESSION: frozen spec must contain contract_markdown_sha256 before science')
        self.assertEqual(len(spec['contract_markdown_sha256']),64)
        contract=SPEC.parent/spec['contract_markdown_path']
        self.assertEqual(hashlib.sha256(contract.read_bytes()).hexdigest(),spec['contract_markdown_sha256'])

class MetadataRejectionTests(unittest.TestCase):
    def setUp(self):
        from q048_v87_consumer_contract import validate_spec
        self.check=validate_spec;self.spec=json.loads(SPEC.read_text())
    def test_missing_contract_key_rejected_before_science(self):
        self.spec.pop('contract_markdown_sha256',None)
        with self.assertRaises(ValueError):self.check(self.spec)
    def test_wrong_contract_hash_rejected_before_science(self):
        self.spec['contract_markdown_sha256']='0'*64
        with self.assertRaises(ValueError):self.check(self.spec)
    def test_required_metadata_keys_rejected(self):
        for key in ['input_pins','code_pins','contract_markdown_path','task_fingerprint','execution_fingerprint','source_commit','capture_sha256','question_sha256']:
            with self.subTest(key=key):
                altered=dict(self.spec);altered.pop(key)
                with self.assertRaises(ValueError):self.check(altered)
    def test_wrong_code_pin_rejected(self):
        from copy import deepcopy
        from q048_v87_consumer_contract import digest
        x=deepcopy(self.spec);key=next(iter(x['code_pins']));x['code_pins'][key]['sha256']='0'*64
        x['execution_fingerprint_basis']['code_pins']=x['code_pins'];x['execution_fingerprint']=digest(x['execution_fingerprint_basis'])
        with self.assertRaises(ValueError):self.check(x)
    def test_changed_scope_rejected(self):
        self.spec['target_q']='Q049'
        with self.assertRaises(ValueError):self.check(self.spec)
    def test_metadata_preflight_creates_no_scientific_artifacts(self):
        root=SPEC.parent
        before={p.name for p in root.glob('*v87.json')}
        self.check(self.spec)
        self.assertEqual(before,{p.name for p in root.glob('*v87.json')})

if __name__=='__main__':unittest.main()
