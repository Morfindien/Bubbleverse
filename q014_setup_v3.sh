#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
case "$CHAIN" in
  planck_npipe_k039_approx|spt_d1_only|spt_d1_plus_desi|all) ;;
  *) echo "Unknown Q014 chain: $CHAIN" >&2; exit 2 ;;
esac
: "${COBAYA_PACKAGES_PATH:=$ROOT/external/cobaya_packages}"
export COBAYA_PACKAGES_PATH
mkdir -p external q014_v3_source_runtime "$COBAYA_PACKAGES_PATH"

# Reuse Q005 V14 dependency pins and CLASS_EDE, but deliberately skip Q005's ACT
# checkout/data because ACT is not part of any Q014 external likelihood chain.
python - <<'PY'
import importlib.metadata as m
expected={'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3','Py-BOBYQA':'1.5.0','Cython':'0.29.37'}
for p,v in expected.items():
    a=m.version(p); assert a==v,(p,a,v)
print('Q014_Q005_DEPENDENCY_REUSE_GATE=PASS')
PY

CLASS_REPO="https://github.com/mwt5345/class_ede.git"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CLASS_DIR="$ROOT/external/class_ede"
if [[ ! -d "$CLASS_DIR/.git" ]]; then git clone "$CLASS_REPO" "$CLASS_DIR"; fi
git -C "$CLASS_DIR" fetch --all --tags
git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"
make -C "$CLASS_DIR" -j2 libclass.a class
rm -rf "$CLASS_DIR/python/build"; rm -f "$CLASS_DIR/python/classy.c"
(
  cd "$CLASS_DIR/python"; export CC=gcc; python setup.py build_ext
)
BUILD_LIB="$(find "$CLASS_DIR/python/build" -maxdepth 1 -type d -name 'lib.*' -print -quit)"
test -n "$BUILD_LIB"
test -n "$(find "$BUILD_LIB" -maxdepth 1 -type f -name 'classy*.so' -print -quit)"
export PYTHONPATH="$BUILD_LIB:$CLASS_DIR:$CLASS_DIR/python:${PYTHONPATH:-}"
python - <<'PY'
import classy,numpy,Cython
assert numpy.__version__=='1.26.4'; assert Cython.__version__=='0.29.37'
assert '/external/class_ede/' in classy.__file__.replace('\\','/')
print('Q014_CLASS_EDE_REUSE_GATE=PASS',classy.__file__)
PY

retry_install() {
  local component="$1"
  for i in 1 2 3 4; do
    if cobaya-install "$component" -p "$COBAYA_PACKAGES_PATH"; then return 0; fi
    [[ "$i" = 4 ]] || sleep 15
  done
  return 1
}

if [[ "$CHAIN" == "planck_npipe_k039_approx" || "$CHAIN" == "all" ]]; then
  for component in \
    planck_2018_lowl.TT \
    planck_2018_lowl.EE \
    planck_NPIPE_highl_CamSpec.TTTEEE \
    planck_2018_lensing.native \
    bao.sdss_dr12_consensus_final \
    bao.sixdf_2011_bao \
    bao.sdss_dr7_mgs \
    sn.pantheonplus
  do retry_install "$component"; done
fi

if [[ "$CHAIN" == spt_d1_* || "$CHAIN" == "all" ]]; then
  python -m pip install "candl-like==2.0.3"
  python - <<'PY'
import candl, importlib.metadata as md
assert md.version('candl-like') == '2.0.3', md.version('candl-like')
print('Q014_CANDL_DISTRIBUTION_GATE=PASS', md.version('candl-like'), candl.__file__)
PY
  SPT_DIR="$ROOT/external/spt_candl_data"
  SPT_COMMIT="2cec6e762a8c540484dd5acafc529f0035856350"
  if [[ ! -d "$SPT_DIR/.git" ]]; then git clone https://github.com/SouthPoleTelescope/spt_candl_data.git "$SPT_DIR"; fi
  git -C "$SPT_DIR" fetch --all --tags --prune
  git -C "$SPT_DIR" checkout --detach "$SPT_COMMIT"
  test "$(git -C "$SPT_DIR" rev-parse HEAD)" = "$SPT_COMMIT"
  python -m pip install -e "$SPT_DIR"

  MUSE_ZIP="$ROOT/external/muse_3g_like_march_2025.zip"
  MUSE_URL="https://lambda.gsfc.nasa.gov/data/suborbital/SPT/muse_3g_like_march_2025.zip"
  curl -fL --retry 5 --retry-delay 5 "$MUSE_URL" -o "$MUSE_ZIP"
  MUSE_SHA="$(sha256sum "$MUSE_ZIP" | awk '{print $1}')"
  printf '%s  %s\n' "$MUSE_SHA" "$MUSE_ZIP" | tee q014_v3_source_runtime/muse_3g_like_march_2025.sha256
  if [[ -n "${Q014_MUSE_EXPECTED_SHA256:-}" ]]; then
    test "$MUSE_SHA" = "$Q014_MUSE_EXPECTED_SHA256" || {
      echo "Q014_MUSE_SOURCE_FREEZE_GATE=FAIL expected=$Q014_MUSE_EXPECTED_SHA256 actual=$MUSE_SHA" >&2; exit 41; }
  fi
  rm -rf "$ROOT/external/muse_3g_like_march_2025"; mkdir -p "$ROOT/external/muse_3g_like_march_2025"
  unzip -q "$MUSE_ZIP" -d "$ROOT/external/muse_3g_like_march_2025"
  MUSE_ROOT="$(python - <<'PY'
from pathlib import Path
root=Path('external/muse_3g_like_march_2025')
for marker in ('pyproject.toml','setup.py'):
    hits=sorted(root.rglob(marker))
    if hits:
        print(hits[0].parent.resolve()); raise SystemExit(0)
raise SystemExit('No installable MUSE Python package found')
PY
)"
  python -m pip install "$MUSE_ROOT"
  if [[ "$CHAIN" == "spt_d1_plus_desi" || "$CHAIN" == "all" ]]; then retry_install bao.desi_dr2; fi
fi

# External likelihood installs must not silently move the frozen Q005 numerical core.
python - <<'PY'
import importlib.metadata as m
expected={'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3','Py-BOBYQA':'1.5.0','Cython':'0.29.37'}
for p,v in expected.items():
    a=m.version(p); assert a==v,(p,a,v)
print('Q014_POST_EXTERNAL_INSTALL_Q005_PIN_GATE=PASS')
PY

CHAIN="$CHAIN" python - <<'PY'
import importlib,json,pathlib,subprocess,importlib.metadata as md,os
chain=os.environ['CHAIN']
out={'chain':chain,'cobaya_version':md.version('cobaya'),'cobaya_git_commit':'6a48864aa3f541df233435070a3c89d65c2ad936',
     'class_ede_commit':'5a131c91d657dd9a7c6364cc45b038710f8d0d97'}
if chain.startswith('spt_') or chain=='all':
    for m in ['candl','spt_candl_data','muse3glike']:
        out[m+'_module']=getattr(importlib.import_module(m),'__file__',None)
    out['candl_distribution']='candl-like'
    out['candl_import_module']='candl'
    out['candl_version']=md.version('candl-like')
    out['spt_candl_data_commit']=subprocess.check_output(['git','-C','external/spt_candl_data','rev-parse','HEAD'],text=True).strip()
    out['muse_sha256']=pathlib.Path('q014_v3_source_runtime/muse_3g_like_march_2025.sha256').read_text().split()[0]
pathlib.Path('q014_v3_source_runtime/setup_imports.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('Q014_SETUP_GATE=PASS',chain)
PY
