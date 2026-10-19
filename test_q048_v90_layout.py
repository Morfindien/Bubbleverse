"""Metadata layout mutations; no source-domain computation."""
import unittest,json
from pathlib import Path
import q048_v90_proof_contract as c
class LayoutTests(unittest.TestCase):
 def fixture(self):return c.load(c.ROOT/c.SPEC)
 def mutate(self,mode):
  s=self.fixture();p='inputs/source/q047_math_v1.py'
  if mode=='missing':s['input_pins'].pop(p)
  else:s['input_pins'][p]['sha256']='0'*64
  s['execution_fingerprint_basis']['input_pins']=s['input_pins'];s['execution_fingerprint']=c.digest(s['execution_fingerprint_basis'])
  return s
 def test_missing_nested_pin(self):
  with self.assertRaisesRegex(ValueError,'required_import_layout'):c.validate_spec(self.mutate('missing'))
 def test_wrong_nested_pin(self):
  with self.assertRaisesRegex(ValueError,'required_import_layout'):c.validate_spec(self.mutate('wrong'))
 def test_both_math_locations_identical(self):
  self.assertEqual((c.ROOT/'inputs/q047_math_v1.py').read_bytes(),(c.ROOT/'inputs/source/q047_math_v1.py').read_bytes())
if __name__=='__main__':unittest.main()
