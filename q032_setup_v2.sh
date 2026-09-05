#!/usr/bin/env bash
set -euo pipefail

export CURRENT_Q="Q-032"
MODE="${1:-both}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH" external q032_runtime

if [[ "$MODE" != "camspec" && "$MODE" != "hillipop" && "$MODE" != "both" ]]; then
  echo "Q032_SETUP_MODE_GATE=FAIL mode=$MODE" >&2
  exit 2
fi

# CamSpec side reuses the already validated Q017 full-MF bootstrap. It does not
# install or execute CamSpec-lite.
if [[ "$MODE" == "camspec" || "$MODE" == "both" ]]; then
  bash q017_setup_v3.sh
fi

# HiLLiPoP side reuses CASE-031's exact software/backend freeze but deliberately
# installs the official native TT data product, not the 7.08-GB TTTEEE precision
# product. TE/EE removal is therefore performed by the package-native TT
# component at the same v4.3 source commit.
if [[ "$MODE" == "hillipop" || "$MODE" == "both" ]]; then
  python - <<'PY'
import sys
assert sys.version_info[:2] == (3,11),sys.version
print('Q032_PYTHON_311_GATE=PASS',sys.version.split()[0])
PY

  python -m pip install --disable-pip-version-check -r q005_hpc_v14_requirements.txt
  python -m pip install --disable-pip-version-check "astropy==7.2.2"
  python - <<'PY'
import importlib.metadata as m
expected={
  'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3',
  'Py-BOBYQA':'1.5.0','getdist':'1.6.1','Cython':'0.29.37','sacc':'1.0.2','astropy':'7.2.2'
}
for p,v in expected.items():
    a=m.version(p); assert a==v,(p,a,v)
print('Q032_FROZEN_DEPENDENCY_GATE=PASS')
PY

  CLASS_REPO="https://github.com/mwt5345/class_ede.git"
  CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
  CLASS_DIR="$ROOT/external/class_ede"
  if [[ ! -d "$CLASS_DIR/.git" ]]; then git clone "$CLASS_REPO" "$CLASS_DIR"; fi
  git -C "$CLASS_DIR" fetch --all --tags
  git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
  test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"

  PY_ABI="$(python - <<'PY'
import sys
print(f'cpython-{sys.version_info.major}{sys.version_info.minor}')
PY
)"
  MATCHING_SO="$(find "$CLASS_DIR/python/build" -type f -name 'classy*.so' -path "*${PY_ABI}*" -print -quit 2>/dev/null || true)"
  if [[ -z "$MATCHING_SO" ]]; then
    make -C "$CLASS_DIR" -j2 libclass.a class
    rm -rf "$CLASS_DIR/python/build"
    rm -f "$CLASS_DIR/python/classy.c"
    (
      cd "$CLASS_DIR/python"
      export CC=gcc
      python setup.py build_ext
    )
  fi
  BUILD_LIB="$(find "$CLASS_DIR/python/build" -maxdepth 1 -type d -name "lib.*${PY_ABI}*" -print -quit)"
  if [[ -z "$BUILD_LIB" ]]; then
    SO_PATH="$(find "$CLASS_DIR/python/build" -type f -name 'classy*.so' -path "*${PY_ABI}*" -print -quit)"
    test -n "$SO_PATH"
    BUILD_LIB="$(dirname "$SO_PATH")"
  fi
  test -n "$BUILD_LIB"
  USER_SITE="$(python - <<'PY'
import site
print(site.getusersitepackages())
PY
)"
  mkdir -p "$USER_SITE"
  printf '%s\n%s\n%s\n' "$BUILD_LIB" "$CLASS_DIR" "$CLASS_DIR/python" > "$USER_SITE/bubbleverse_q032_class_ede_v2.pth"
  export PYTHONPATH="$BUILD_LIB:$CLASS_DIR:$CLASS_DIR/python${PYTHONPATH:+:$PYTHONPATH}"

  HILLIPOP_REPO="https://github.com/planck-npipe/hillipop.git"
  HILLIPOP_COMMIT="a09ddde3e7ce11df99f74685feb1f1764cafb251"
  HILLIPOP_DIR="$ROOT/external/hillipop"
  if [[ ! -d "$HILLIPOP_DIR/.git" ]]; then git clone "$HILLIPOP_REPO" "$HILLIPOP_DIR"; fi
  git -C "$HILLIPOP_DIR" fetch --all --tags
  git -C "$HILLIPOP_DIR" checkout --detach "$HILLIPOP_COMMIT"
  test "$(git -C "$HILLIPOP_DIR" rev-parse HEAD)" = "$HILLIPOP_COMMIT"
  python -m pip install --disable-pip-version-check --no-deps -e "$HILLIPOP_DIR"

  for i in 1 2 3 4; do
    echo "[INFO] Q032 cobaya-install planck_2020_hillipop.TT attempt=$i/4"
    if cobaya-install planck_2020_hillipop.TT -p "$COBAYA_PACKAGES_PATH"; then break; fi
    if [[ "$i" == 4 ]]; then
      echo "Q032_HILLIPOP_TT_DATA_INSTALL_GATE=FAIL" >&2
      exit 2
    fi
    sleep 15
  done

  python - <<'PY'
import hashlib, importlib.metadata as md, json, os, pathlib, subprocess, sys
import classy, planck_2020_hillipop
ROOT=pathlib.Path('.').resolve()
packages=pathlib.Path(os.environ['COBAYA_PACKAGES_PATH']).resolve()
hill=ROOT/'external'/'hillipop'
classdir=ROOT/'external'/'class_ede'
assert subprocess.check_output(['git','-C',str(hill),'rev-parse','HEAD'],text=True).strip() == 'a09ddde3e7ce11df99f74685feb1f1764cafb251'
assert subprocess.check_output(['git','-C',str(classdir),'rev-parse','HEAD'],text=True).strip() == '5a131c91d657dd9a7c6364cc45b038710f8d0d97'
assert str(pathlib.Path(planck_2020_hillipop.__file__).resolve()).startswith(str(hill.resolve())+os.sep)
assert 'external/class_ede' in str(pathlib.Path(classy.__file__).resolve()).replace('\\','/')

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return {'path':str(p),'size':p.stat().st_size,'sha256':h.hexdigest()}

def one(name):
    hits=list(packages.rglob(name)); assert len(hits)==1,(name,hits)
    return digest(hits[0])

spectra=sorted(packages.rglob('dl_PR4_v4.2_*.fits'))
assert spectra,'No HiLLiPoP PR4 cross spectra installed'
runtime={
  'q':'Q-032','run_id':'Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2',
  'result_id':'R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002','status':'PASS',
  'python_version':sys.version.split()[0],
  'class_ede_commit':'5a131c91d657dd9a7c6364cc45b038710f8d0d97',
  'classy_path':str(pathlib.Path(classy.__file__).resolve()),
  'hillipop_repository':'planck-npipe/hillipop',
  'hillipop_commit':'a09ddde3e7ce11df99f74685feb1f1764cafb251',
  'hillipop_module_path':str(pathlib.Path(planck_2020_hillipop.__file__).resolve()),
  'parent_case031_component':'planck_2020_hillipop.TTTEEE',
  'phase_a_component':'planck_2020_hillipop.TT',
  'mode_removal_semantics':'OFFICIAL_NATIVE_TT_COMPONENT_SAME_RELEASE_AND_COMMIT',
  'software_versions':{p:md.version(p) for p in ['cobaya','PyYAML','numpy','scipy','Py-BOBYQA','getdist','Cython','sacc','astropy']},
  'data_hashes':{
    'binning_v4.2.fits':one('binning_v4.2.fits'),
    'invfll_PR4_v4.2_TT.fits':one('invfll_PR4_v4.2_TT.fits'),
  },
  'cross_spectrum_hashes':{p.name:digest(p) for p in spectra},
  'excluded_observational_components':['TE','EE','low_l','lensing','ACT','SPT','BAO','SN']
}
pathlib.Path('q032_runtime/q032_hillipop_tt_runtime_v2.json').write_text(
    json.dumps(runtime,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('Q032_BACKEND_IDENTITY_GATE=PASS')
print('Q032_HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=PASS')
print('Q032_HILLIPOP_TT_DATA_GATE=PASS')
PY
fi

export CURRENT_Q="Q-032"
python - <<'PY'
import os, sys
assert os.environ.get('CURRENT_Q')=='Q-032'
assert sys.version_info[:2]==(3,11),sys.version
print('Q032_CONTEXT_CONTINUITY_GATE=PASS')
print('Q032_PYTHON_311_GATE=PASS')
PY
