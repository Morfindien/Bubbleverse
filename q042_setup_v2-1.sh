#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"
: "${COBAYA_PACKAGES_PATH:=$ROOT/external/cobaya_packages}"
export COBAYA_PACKAGES_PATH
mkdir -p external q042_runtime

# Reuse the exact Q041 V19 cosmology/likelihood runtime. This script is environment
# reuse only; no V19 chain state or scientific endpoint is consumed.
bash "$ROOT/q041_setup_v19.sh"

python -m pip install --disable-pip-version-check 'Py-BOBYQA==1.5.0'

retry_install() {
  local component="$1"; local n
  for n in 1 2 3; do
    if cobaya-install "$component" -p "$COBAYA_PACKAGES_PATH"; then return 0; fi
    sleep $((n*10))
  done
  return 1
}
retry_install sn.pantheonplus

POLY="$ROOT/external/PolyChordLite"
if [ ! -d "$POLY/.git" ]; then
  rm -rf "$POLY"
  git clone --depth 1 --branch 1.22.2 https://github.com/PolyChord/PolyChordLite.git "$POLY"
fi
test "$(git -C "$POLY" describe --tags --exact-match)" = "1.22.2"
POLY_COMMIT="$(git -C "$POLY" rev-parse HEAD)"
python -m pip install --disable-pip-version-check --no-deps "$POLY"
python - <<'PYSETUP'
import hashlib, importlib, importlib.metadata as md, json, os, pathlib, platform, subprocess
root=pathlib.Path(os.environ['COBAYA_PACKAGES_PATH']).resolve()
repo=pathlib.Path('external/PolyChordLite').resolve()
assert md.version('cobaya')=='3.5.6', md.version('cobaya')
assert md.version('Py-BOBYQA')=='1.5.0', md.version('Py-BOBYQA')
import pypolychord, pybobyqa
commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
tag=subprocess.check_output(['git','-C',str(repo),'describe','--tags','--exact-match'],text=True).strip()
assert tag=='1.22.2'
hits=[p for p in root.rglob('*') if p.is_file() and 'pantheon' in str(p).lower()]
if not hits: raise SystemExit('PANTHEONPLUS_RUNTIME_FILE_GATE=FAIL')
manifest=[]
for p in sorted(hits):
 h=hashlib.sha256(p.read_bytes()).hexdigest();manifest.append({'path':str(p.relative_to(root)),'size':p.stat().st_size,'sha256':h})
manifest_hash=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest()
out={
 'q':'Q-042','case_id':'NOT DOCUMENTED','program_id':'Q042-PREFLIGHT-V2','run_id':'Q042-POLYCHORD-BOBYQA-PREFLIGHT-V2','result_id':'R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-002','status':'PASS',
 'cobaya_version':md.version('cobaya'),'pybobyqa_version':md.version('Py-BOBYQA'),'numpy_version':md.version('numpy'),
 'python_version':platform.python_version(),'polychord_tag':tag,'polychord_commit':commit,'polychord_path':str(repo),
 'pypolychord_module':str(pathlib.Path(pypolychord.__file__).resolve()),'pybobyqa_module':str(pathlib.Path(pybobyqa.__file__).resolve()),
 'pantheonplus_component':'sn.pantheonplus','pantheonplus_runtime_files':manifest,'pantheonplus_manifest_sha256':manifest_hash,
 'cobaya_upgraded':False,'scientific_result':False
}
path=pathlib.Path('q042_runtime/q042_external_runtime_provenance_v2.json');path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('Q042_V2_RUNTIME_SOURCE_GATE=PASS polychord_commit='+commit+' pantheon_files='+str(len(manifest)))
PYSETUP
