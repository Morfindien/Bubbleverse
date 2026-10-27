#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
REG=HERE/'bubbleverse_program_registry.json'; README=HERE/'README.md'; LAUNCH=HERE/'.github/workflows/00-bubbleverse-start.yml'
PATCH=HERE/'q052_program_registry_patch_validateddiag_v3.json'; SECTION=HERE/'README_Q052_VALIDATEDDIAG_V3_SECTION.md'; MANIFEST=HERE/'Q052_INSTALL_MANIFEST_VALIDATEDDIAG_V3.json'
EXPECTED={'registry':'f6f6540c205f051a64abd5bb290751312b80e405','readme':'2fe5d3fefe080d349767d8b1304e88d357a47a3c','launcher':'7f22c617fb98d1508a0b22a42dd3735a74d8288e'}

def die(x): raise SystemExit(x)
def blob(p): return subprocess.check_output(['git','hash-object',str(p)],text=True).strip()
def sha(p):
 h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()

def main():
 for p in [REG,README,LAUNCH,PATCH,SECTION,MANIFEST]:
  if not p.is_file():die('INSTALL_MISSING '+str(p))
 if blob(REG)!=EXPECTED['registry']:die('INSTALL_REGISTRY_BASE_CHANGED')
 if blob(README)!=EXPECTED['readme']:die('INSTALL_README_BASE_CHANGED')
 if blob(LAUNCH)!=EXPECTED['launcher']:die('INSTALL_LAUNCHER_CHANGED')
 m=json.loads(MANIFEST.read_text())
 for rel,digest in m['package_sha256'].items():
  p=HERE/rel
  if not p.is_file() or sha(p)!=digest:die('INSTALL_PACKAGE_HASH '+rel)
 patch=json.loads(PATCH.read_text());pid=patch['program_id'];r=json.loads(REG.read_text())
 programs=r.get('programs')
 if not isinstance(programs,dict):die('INSTALL_REGISTRY_SCHEMA')
 if pid in programs:die('INSTALL_PROGRAM_ALREADY_PRESENT')
 programs[pid]=patch['entry']
 REG.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 sec=SECTION.read_text().rstrip()+'\n\n---\n\n'
 README.write_text(sec+README.read_text())
 subprocess.run([sys.executable,'-m','unittest','-v','test_q052_validated_diag_v3.py'],cwd=HERE,check=True)
 print('Q052_VALIDATEDDIAG_V3_INSTALL_GATE=PASS')
if __name__=='__main__':main()
