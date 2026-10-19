"""Pre-freeze actual import probe; no producer/scientific entry-point calls."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
def main():
 sys.dont_write_bytecode=True
 s=json.loads((ROOT/'q048_moving_h_domain_spec_v90.json').read_text())
 for rel in ['inputs/q047_math_v1.py','inputs/source/q047_math_v1.py']:
  p=ROOT/rel; pin=s['input_pins'].get(rel)
  if pin!={'bytes':12617,'sha256':'d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d'} or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('IMPORT_LAYOUT_HASH:'+rel)
 if Path.cwd()!=ROOT:raise ValueError('FINAL_CWD_REQUIRED')
 before={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 blocked={'main','produce','proof_cell','source_expected','construct','run','core_validate'}
 def profile(frame,event,arg):
  if event=='call' and frame.f_code.co_name in blocked and str(ROOT) in frame.f_code.co_filename:raise RuntimeError('FORBIDDEN_SCIENCE_CALL_DURING_IMPORT:'+frame.f_code.co_name)
 sys.setprofile(profile)
 try:
  import q048_moving_h_domain_v90 as producer
 finally:sys.setprofile(None)
 resolved={}
 for name,module,expected in [('producer',producer,ROOT/'q048_moving_h_domain_v90.py'),('full_tube',producer.old,ROOT/'inputs/q048_full_tube_reuse_v1.py'),('flat_math',producer.m,ROOT/'inputs/q047_math_v1.py'),('kernel',producer.old.k,ROOT/'inputs/q048_p3_scaled_kernel_v2.py'),('nested_math',producer.old.k._m,ROOT/'inputs/source/q047_math_v1.py')]:
  p=Path(module.__file__).resolve()
  if p!=expected:raise ValueError('RESOLVED_MODULE_PATH:'+name)
  resolved[name]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 after={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 if before!=after:raise ValueError('IMPORT_CREATED_OR_REMOVED_FILES')
 print(json.dumps({'status':'PASS','kind':'ACTUAL_PRODUCER_TRANSITIVE_IMPORT_ONLY','cwd':str(ROOT),'resolved':resolved,'scientific_entry_points_called':0,'files_created':0,'note':'Retained primitive/constants initialization only;no main/produce/run/construct/validator called.'},indent=2))
if __name__=='__main__':main()
