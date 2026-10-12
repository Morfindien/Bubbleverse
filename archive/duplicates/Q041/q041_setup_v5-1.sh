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
for i in 1 2 3 4; do
  echo "[INFO] Q041 install ACT DR6 CMB data attempt=$i/4"
  if cobaya-install act_dr6_cmbonly -p "$COBAYA_PACKAGES_PATH"; then break; fi
  [[ "$i" == 4 ]] && { echo Q041_ACT_CMB_DATA_INSTALL_GATE=FAIL >&2; exit 2; }
  sleep 15
done

# ACT DR6 ACT-only baseline lensing likelihood and v1.2 data.
ACT_LENS_COMMIT="b386ddbb5821c1216c709f051c9289292f174d30"
ACT_LENS_DIR="$ROOT/external/act_dr6_lenslike"
clone_exact "https://github.com/ACTCollaboration/act_dr6_lenslike.git" "$ACT_LENS_COMMIT" "$ACT_LENS_DIR"
python -m pip install --disable-pip-version-check --no-deps -e "$ACT_LENS_DIR"
if [[ ! -d "$ACT_LENS_DIR/act_dr6_lenslike/data/v1.2" ]]; then
  for i in 1 2 3 4; do
    echo "[INFO] Q041 install ACT DR6 lensing data attempt=$i/4"
    if (cd "$ACT_LENS_DIR" && bash get-act-data.sh); then break; fi
    [[ "$i" == 4 ]] && { echo Q041_ACT_LENS_DATA_INSTALL_GATE=FAIL >&2; exit 2; }
    sleep 15
  done
fi
test -d "$ACT_LENS_DIR/act_dr6_lenslike/data/v1.2"

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

BAO_DATA_COMMIT="b7b8a36e9bccb063081f811f323cada21ab5fbdd"
BAO_SRC="$ROOT/external/bao_data_v3_6"
clone_exact "https://github.com/CobayaSampler/bao_data.git" "$BAO_DATA_COMMIT" "$BAO_SRC"
rm -rf "$COBAYA_PACKAGES_PATH/data/bao_data"
mkdir -p "$COBAYA_PACKAGES_PATH/data/bao_data"
cp -a "$BAO_SRC/." "$COBAYA_PACKAGES_PATH/data/bao_data/"
test -f "$COBAYA_PACKAGES_PATH/data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
test -f "$COBAYA_PACKAGES_PATH/data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"

python - <<'PY'
import hashlib, importlib, importlib.metadata as md, json, os, pathlib, subprocess
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
assert head(ROOT/'external/bao_data_v3_6')=='b7b8a36e9bccb063081f811f323cada21ab5fbdd'
import act_dr6_cmbonly, act_dr6_lenslike
importlib.import_module('cobaya.likelihoods.bao.desi_dr2')
act_hits=list((packages/'data'/'ACTDR6CMBonly').rglob('dr6_data_cmbonly.fits'))
assert len(act_hits)==1,act_hits
lens=ROOT/'external/act_dr6_lenslike/act_dr6_lenslike/data/v1.2'
assert lens.is_dir()
mean=packages/'data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt'
cov=packages/'data/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'
rec={
 'q':'Q-041','program_id':'Q041-PLANCKPORT-V5','stage':'EXTERNAL_RUNTIME_PROVENANCE','status':'PASS',
 'core_versions':{p:md.version(p) for p in ['cobaya','numpy','scipy','getdist','sacc']},
 'commits':{
   'act_dr6_cmbonly':head(ROOT/'external/act_dr6_cmbonly'),
   'act_dr6_lenslike':head(ROOT/'external/act_dr6_lenslike'),
   'cobaya_desi_dr2_definition':head(ROOT/'external/cobaya_desi_dr2_source'),
   'bao_data':head(ROOT/'external/bao_data_v3_6')},
 'data':{'act_dr6_cmbonly':digest(act_hits[0]),'desi_dr2_mean':digest(mean),'desi_dr2_cov':digest(cov)},
 'act_lensing_data_directory':str(lens),
 'cobaya_upgraded':False
}
pathlib.Path('q041_runtime/q041_external_runtime_provenance_v5.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
print('Q041_EXTERNAL_RUNTIME_PROVENANCE_GATE=PASS')
PY
