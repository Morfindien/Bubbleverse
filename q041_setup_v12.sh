#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"
export CURRENT_Q="Q-041"
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p external q041_runtime "$COBAYA_PACKAGES_PATH/data"

python - <<'PY'
import importlib.metadata as m, sys
assert sys.version_info[:2] == (3,11), sys.version
expected={'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3','Py-BOBYQA':'1.5.0','getdist':'1.6.1','sacc':'1.0.2'}
for p,v in expected.items():
    a=m.version(p); assert a==v,(p,a,v)
print('Q041_FROZEN_CORE_DEPENDENCY_GATE=PASS')
PY

clone_exact () {
  local repo="$1" commit="$2" dir="$3"
  if [[ ! -d "$dir/.git" ]]; then
    rm -rf "$dir"
    git init -q "$dir"
    git -C "$dir" remote add origin "$repo"
  fi
  if ! git -C "$dir" cat-file -e "$commit^{commit}" 2>/dev/null; then
    git -C "$dir" fetch --depth 1 origin "$commit"
  fi
  git -C "$dir" checkout -q --detach "$commit"
  test "$(git -C "$dir" rev-parse HEAD)" = "$commit"
}

# ACT DR6 foreground-marginalized primary-CMB likelihood.
ACT_CMB_COMMIT="880eacb40d66722eb1c32d7b5621e91662b4d808"
ACT_CMB_DIR="$ROOT/external/act_dr6_cmbonly"
clone_exact "https://github.com/ACTCollaboration/DR6-ACT-lite.git" "$ACT_CMB_COMMIT" "$ACT_CMB_DIR"
python -m pip install --disable-pip-version-check --no-deps -e "$ACT_CMB_DIR"

# Transport-only repair. ACT upstream commit 627aeafb88ae5ad1aa66b406bea2d65cfa66a27d
# changed only the data URL from NERSC to NASA LAMBDA for the same v1.0 product.
ACT_CMB_LAMBDA_URL="https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz"
ACT_CMB_DATA_ROOT="$COBAYA_PACKAGES_PATH/data/ACTDR6CMBonly"
ACT_CMB_DATA_FILE="$ACT_CMB_DATA_ROOT/v1.0/dr6_data_cmbonly.fits"
if [[ ! -s "$ACT_CMB_DATA_FILE" ]]; then
  tmp="$(mktemp -d)"
  archive="$tmp/dr6_data_cmbonly.tar.gz"
  ok=false
  for i in 1 2 3; do
    echo "[INFO] Q041 official ACT DR6 CMB LAMBDA download attempt=$i/3"
    if curl -fL --retry 2 --retry-all-errors --retry-delay 3       --connect-timeout 15 --max-time 300       -o "$archive" "$ACT_CMB_LAMBDA_URL"; then
      ok=true
      break
    fi
    sleep 5
  done
  [[ "$ok" == true ]] || { rm -rf "$tmp"; echo Q041_ACT_CMB_LAMBDA_DOWNLOAD_GATE=FAIL >&2; exit 2; }
  tar -tzf "$archive" > "$tmp/act_cmb_archive.list"
  grep -qx 'v1.0/dr6_data_cmbonly.fits' "$tmp/act_cmb_archive.list"
  rm -rf "$ACT_CMB_DATA_ROOT/v1.0"
  mkdir -p "$ACT_CMB_DATA_ROOT"
  tar -xzf "$archive" -C "$ACT_CMB_DATA_ROOT"
  rm -rf "$tmp"
fi
test -s "$ACT_CMB_DATA_FILE"
echo "Q041_ACT_CMB_LAMBDA_DATA_GATE=PASS path=$ACT_CMB_DATA_FILE"

# ACT DR6 ACT-only baseline lensing likelihood and v1.2 data.
ACT_LENS_COMMIT="b386ddbb5821c1216c709f051c9289292f174d30"
ACT_LENS_DIR="$ROOT/external/act_dr6_lenslike"
clone_exact "https://github.com/ACTCollaboration/act_dr6_lenslike.git" "$ACT_LENS_COMMIT" "$ACT_LENS_DIR"
python -m pip install --disable-pip-version-check --no-deps -e "$ACT_LENS_DIR"

# The pinned ACT lensing code already uses NASA LAMBDA as its authoritative source.
ACT_LENS_LAMBDA_URL="https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_dr6/likelihood/data/ACT_dr6_likelihood_v1.2.tgz"
ACT_LENS_DATA_ROOT="$COBAYA_PACKAGES_PATH/data/ACT_dr6_likelihood"
ACT_LENS_DATA_DIR="$ACT_LENS_DATA_ROOT/v1.2"
if [[ ! -d "$ACT_LENS_DATA_DIR" ]] || [[ -z "$(find "$ACT_LENS_DATA_DIR" -type f -print -quit 2>/dev/null)" ]]; then
  tmp="$(mktemp -d)"
  archive="$tmp/ACT_dr6_likelihood_v1.2.tgz"
  ok=false
  for i in 1 2 3; do
    echo "[INFO] Q041 official ACT DR6 lensing LAMBDA download attempt=$i/3"
    if curl -fL --retry 2 --retry-all-errors --retry-delay 3       --connect-timeout 15 --max-time 600       -o "$archive" "$ACT_LENS_LAMBDA_URL"; then
      ok=true
      break
    fi
    sleep 5
  done
  [[ "$ok" == true ]] || { rm -rf "$tmp"; echo Q041_ACT_LENS_LAMBDA_DOWNLOAD_GATE=FAIL >&2; exit 2; }
  tar -tzf "$archive" > "$tmp/act_lens_archive.list"
  grep -q '^v1.2/' "$tmp/act_lens_archive.list"
  rm -rf "$ACT_LENS_DATA_ROOT/v1.2"
  mkdir -p "$ACT_LENS_DATA_ROOT"
  tar -xzf "$archive" -C "$ACT_LENS_DATA_ROOT"
  rm -rf "$tmp"
fi
test -d "$ACT_LENS_DATA_DIR"
test -n "$(find "$ACT_LENS_DATA_DIR" -type f -print -quit)"
echo "Q041_ACT_LENS_LAMBDA_DATA_GATE=PASS path=$ACT_LENS_DATA_DIR"

# Backport only Cobaya's DESI DR2 component definition into the frozen 3.5.6 runtime.
# Do not upgrade Cobaya: Q032 CamSpec execution depends on the frozen 3.5.6 stack.
DESI_DEF_COMMIT="b76b6fed2a6c8c5594c6f92d5058bef10079746a"
DESI_SRC="$ROOT/external/cobaya_desi_dr2_source"
clone_exact "https://github.com/CobayaSampler/cobaya.git" "$DESI_DEF_COMMIT" "$DESI_SRC"
COBAYA_DIR="$(python - <<'PY'
import pathlib, cobaya
print(pathlib.Path(cobaya.__file__).resolve().parent)
PY
)"
rm -rf "$COBAYA_DIR/likelihoods/bao/desi_dr2"
cp -a "$DESI_SRC/cobaya/likelihoods/bao/desi_dr2" "$COBAYA_DIR/likelihoods/bao/desi_dr2"

# Compatibility-only backport from pinned Cobaya commit b76b6fed...
BAO_BASE="$COBAYA_DIR/likelihoods/base_classes/bao.py"
python - "$BAO_BASE" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
old='            self.has_type = self.data.iloc[:, -1].dtype == np.dtype("O")\\n'
new=(
'            type_last_col = self.data.iloc[:, -1].dtype\\n'
'            self.has_type = (\\n'
'                type_last_col == np.dtype("O")\\n'
'                or type_last_col.__class__ == pd.StringDtype\\n'
'            )\\n'
)
if old in s:
    p.write_text(s.replace(old,new,1),encoding="utf-8")
elif new not in s:
    raise SystemExit("Q041_DESI_DR2_BAO_DTYPE_PATCH_SIGNATURE_GATE=FAIL")
assert new in p.read_text(encoding="utf-8")
print("Q041_DESI_DR2_BAO_DTYPE_COMPATIBILITY_PATCH_GATE=PASS")
PY

python - <<'PY'
import inspect, pandas as pd
from cobaya.likelihoods.base_classes import BAO
src=inspect.getsource(BAO.initialize)
assert 'type_last_col.__class__ == pd.StringDtype' in src
print("Q041_DESI_DR2_BAO_STRINGDTYPE_RUNTIME_GATE=PASS pandas="+pd.__version__)
PY

BAO_DATA_COMMIT="b7b8a36e9bccb063081f811f323cada21ab5fbdd"
BAO_SRC="$ROOT/external/bao_data_v2_6"
clone_exact "https://github.com/CobayaSampler/bao_data.git" "$BAO_DATA_COMMIT" "$BAO_SRC"
rm -rf "$COBAYA_PACKAGES_PATH/data/bao_data"
mkdir -p "$COBAYA_PACKAGES_PATH/data/bao_data"
cp -a "$BAO_SRC/." "$COBAYA_PACKAGES_PATH/data/bao_data/"
test -f "$COBAYA_PACKAGES_PATH/data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
test -f "$COBAYA_PACKAGES_PATH/data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"

# Cobaya's normal GitHub-release installer writes this metadata file.
# Without it InstallableLikelihood interprets the release as 0.0.
printf '%s' 'v2.6' > "$COBAYA_PACKAGES_PATH/data/bao_data/version.dat"
test "$(cat "$COBAYA_PACKAGES_PATH/data/bao_data/version.dat")" = "v2.6"

python - <<'PY'
import os
from cobaya.likelihoods.bao.desi_dr2.desi_bao_all import desi_bao_all
packages = os.environ["COBAYA_PACKAGES_PATH"]
assert desi_bao_all.is_installed(path=packages, show_error=True) is True
print("Q041_DESI_DR2_COBAYA_VERSION_METADATA_GATE=PASS")
PY

python - <<'PY'
import hashlib, importlib, importlib.metadata as md, json, os, pathlib, subprocess, pandas as pd
ROOT=pathlib.Path('.').resolve()
packages=pathlib.Path(os.environ['COBAYA_PACKAGES_PATH']).resolve()

def head(p): return subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
def digest(p):
    p=pathlib.Path(p); h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return {'path':str(p),'size':p.stat().st_size,'sha256':h.hexdigest()}
assert md.version('cobaya')=='3.5.6'
assert head(ROOT/'external/act_dr6_cmbonly')=='880eacb40d66722eb1c32d7b5621e91662b4d808'
assert head(ROOT/'external/act_dr6_lenslike')=='b386ddbb5821c1216c709f051c9289292f174d30'
assert head(ROOT/'external/cobaya_desi_dr2_source')=='b76b6fed2a6c8c5594c6f92d5058bef10079746a'
assert head(ROOT/'external/bao_data_v2_6')=='b7b8a36e9bccb063081f811f323cada21ab5fbdd'
import act_dr6_cmbonly, act_dr6_lenslike
bao_base=pathlib.Path(importlib.import_module('cobaya.likelihoods.base_classes.bao').__file__).resolve()
bao_base_text=bao_base.read_text(encoding='utf-8')
assert 'type_last_col.__class__ == pd.StringDtype' in bao_base_text
importlib.import_module('cobaya.likelihoods.bao.desi_dr2')
act_hits=list((packages/'data'/'ACTDR6CMBonly').rglob('dr6_data_cmbonly.fits'))
assert len(act_hits)==1,act_hits
lens=packages/'data/ACT_dr6_likelihood/v1.2'
assert lens.is_dir()
mean=packages/'data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt'
cov=packages/'data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'
bao_version=packages/'data/bao_data/version.dat'
assert bao_version.read_text(encoding='utf-8').strip()=='v2.6'
rec={
 'q':'Q-041','program_id':'Q041-PLANCKPORT-V12','stage':'EXTERNAL_RUNTIME_PROVENANCE','status':'PASS',
 'core_versions':{p:md.version(p) for p in ['cobaya','numpy','scipy','getdist','sacc','pandas']},
 'bao_base_compatibility':{
   'frozen_cobaya_version':'3.5.6',
   'compatibility_source_commit':'b76b6fed2a6c8c5594c6f92d5058bef10079746a',
   'compatibility_scope':'BAO pandas StringDtype recognition only',
   'patched_bao_base':digest(bao_base)
 },
 'commits':{
   'act_dr6_cmbonly':head(ROOT/'external/act_dr6_cmbonly'),
   'act_dr6_lenslike':head(ROOT/'external/act_dr6_lenslike'),
   'cobaya_desi_dr2_definition':head(ROOT/'external/cobaya_desi_dr2_source'),
   'bao_data':head(ROOT/'external/bao_data_v2_6')},
 'data':{'act_dr6_cmbonly':digest(act_hits[0]),'desi_dr2_mean':digest(mean),'desi_dr2_cov':digest(cov),'bao_version':digest(bao_version)},
 'act_lensing_data_directory':str(lens),
 'transport':{
   'act_dr6_cmbonly':'NASA_LAMBDA_OFFICIAL',
   'act_dr6_cmbonly_url':'https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz',
   'act_dr6_cmbonly_transport_change_commit':'627aeafb88ae5ad1aa66b406bea2d65cfa66a27d',
   'act_dr6_lensing':'NASA_LAMBDA_PINNED_UPSTREAM'
 },
 'cobaya_upgraded':False
}
pathlib.Path('q041_runtime/q041_external_runtime_provenance_v12.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
print('Q041_EXTERNAL_RUNTIME_PROVENANCE_GATE=PASS')
PY
