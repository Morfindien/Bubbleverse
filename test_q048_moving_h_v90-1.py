"""Finite V90 tests. Toy ODE fixtures only; never execute a prior or current science main."""
import importlib.util,unittest,json
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parent
class ComparisonFixtureTests(unittest.TestCase):
    def backend(self):
        located=importlib.util.find_spec('q048_moving_h_domain_v90')
        self.assertIsNotNone(located,'Missing V90 bounded comparison implementation')
        import q048_moving_h_domain_v90 as p
        return p
    def test_zero_K_retains_initial(self):
        p=self.backend();result=p.primary_endpoint(F(0),F(1,100),p.m.I(0,F(1,100)),F(1,2))
        self.assertLessEqual(result.lo,F(1,2));self.assertGreaterEqual(result.hi,F(1,2))
        self.assertEqual(p.rational_lower(F(0),F(1,100),F(1,100),F(1,2)),F(1,2))
    def test_zero_epsilon_riccati_limit(self):
        p=self.backend();answer=p.primary_endpoint(F(2),F(0),p.m.I(F(1,10)),F(1,2))
        expected=F(5,11);self.assertLessEqual(answer.lo,expected);self.assertGreaterEqual(answer.hi,expected)
        self.assertEqual(p.rational_lower(F(2),F(0),F(1,10),F(1,2)),expected)
    def test_invalid_control_domain_rejected(self):
        p=self.backend()
        with self.assertRaises(ValueError):p.rational_lower(F(100),F(1),F(1),F(1,2))
    def test_positive_control_decreases_from_initial(self):
        p=self.backend();x=p.rational_lower(F(2),F(1,100),F(1,100),F(1,2));self.assertTrue(0<x<F(1,2))

class MetadataTests(unittest.TestCase):
    def backend(self):
        located=importlib.util.find_spec('q048_v90_proof_contract')
        self.assertIsNotNone(located,'Missing V90 strict pre-science metadata contract')
        import q048_v90_proof_contract as c
        return c
    def test_missing_contract_hash_rejected(self):
        c=self.backend();s=json.loads((ROOT/c.SPEC).read_text());s.pop('contract_markdown_sha256')
        with self.assertRaises(ValueError):c.validate_spec(s)
    def test_wrong_contract_hash_rejected(self):
        c=self.backend();s=json.loads((ROOT/c.SPEC).read_text());s['contract_markdown_sha256']='0'*64
        with self.assertRaises(ValueError):c.validate_spec(s)
    def test_missing_required_fields_rejected(self):
        c=self.backend();s=json.loads((ROOT/c.SPEC).read_text())
        for key in ['input_pins','code_pins','execution_fingerprint','task_fingerprint','question_sha256','source_commit','capture_sha256']:
            with self.subTest(key=key):
                x=dict(s);x.pop(key)
                with self.assertRaises(ValueError):c.validate_spec(x)
    def test_wrong_scope_rejected(self):
        c=self.backend();s=json.loads((ROOT/c.SPEC).read_text());s['target_q']='Q049'
        with self.assertRaises(ValueError):c.validate_spec(s)
    def test_metadata_no_science_output(self):
        c=self.backend();before={p.name for p in ROOT.glob('*v90.json')};c.validate_spec(json.loads((ROOT/c.SPEC).read_text()));self.assertEqual(before,{p.name for p in ROOT.glob('*v90.json')})
if __name__=='__main__':unittest.main()
