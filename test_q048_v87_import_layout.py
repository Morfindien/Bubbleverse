"""Regression for omitted transitive math path; no scientific mains."""
from pathlib import Path
import hashlib,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parent
PIN="d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d"
class ImportLayoutRegression(unittest.TestCase):
 def test_nested_math_exact_bytes_are_present(self):
  p=ROOT/"inputs/source/q047_math_v1.py"
  self.assertTrue(p.is_file(),"V84 regression: pinned loader needs nested inputs/source path")
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),PIN)
 def test_real_retained_dependency_chain_imports_without_main(self):
  code="import sys;sys.path.insert(0,'inputs');import q048_full_tube_reuse_v1 as q;print(q.k._m.__file__)"
  r=subprocess.run([sys.executable,"-B","-c",code],cwd=ROOT,text=True,capture_output=True)
  self.assertEqual(r.returncode,0,r.stderr)
  self.assertIn(str(ROOT/"inputs/source/q047_math_v1.py"),r.stdout)
class LayoutRejections(unittest.TestCase):
 def test_required_nested_path_pin_cannot_be_omitted(self):
  import json,copy
  from q048_v87_consumer_contract import validate_spec,digest
  s=json.loads((ROOT/'q048_frec_moving_h_spec_v87.json').read_text());s['input_pins'].pop('inputs/source/q047_math_v1.py');s['execution_fingerprint_basis']['input_pins']=s['input_pins'];s['execution_fingerprint']=digest(s['execution_fingerprint_basis'])
  with self.assertRaisesRegex(ValueError,'required_transitive_path_pin'):validate_spec(s)
 def test_wrong_nested_path_hash_rejected_before_import(self):
  import json
  from q048_v87_consumer_contract import validate_spec,digest
  s=json.loads((ROOT/'q048_frec_moving_h_spec_v87.json').read_text());s['input_pins']['inputs/source/q047_math_v1.py']['sha256']='0'*64;s['execution_fingerprint_basis']['input_pins']=s['input_pins'];s['execution_fingerprint']=digest(s['execution_fingerprint_basis'])
  with self.assertRaisesRegex(ValueError,'required_transitive_path_pin'):validate_spec(s)
 def test_parent_directory_escape_rejected(self):
  from q048_v87_consumer_contract import checked_path
  with self.assertRaisesRegex(ValueError,'UNSAFE_PATH'):checked_path('../q047_math_v1.py')
 def test_absolute_path_rejected(self):
  from q048_v87_consumer_contract import checked_path
  with self.assertRaisesRegex(ValueError,'UNSAFE_PATH'):checked_path('/tmp/q047_math_v1.py')
if __name__=="__main__":unittest.main()
