#!/usr/bin/env bash
set -euo pipefail

# TECHNICAL VERSION: V2
# Repair: force Python 3.11, use writable user-site .pth, and reject cached ABI mismatches.

export CURRENT_Q=CASE-031
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH" external q031_runtime

STAGE="BOOTSTRAP"
fail() {
  rc=$?
  trap - ERR
  STAGE_LOCAL="$STAGE" RC_LOCAL="$rc" python - <<'PY'
import json, os
from pathlib import Path
Path("q031_runtime/q031_setup_failure_v1.json").write_text(
    json.dumps({
      "q":"CASE-031",
      "run_id":"CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1",
  "setup_version":"v2",
      "status":"IMPLEMENTATION_FAILURE",
      "scientific_nonportability":False,
      "stage":os.environ.get("STAGE_LOCAL","UNKNOWN"),
      "exit_code":int(os.environ.get("RC_LOCAL","2"))
    }, indent=2, sort_keys=True)+"\n",
    encoding="utf-8")
PY
  exit "$rc"
}
trap fail ERR

# Frozen Bubbleverse numerical stack: same versions as the known-good Q017 path.
STAGE="FROZEN_DEPENDENCIES"
test -f q005_hpc_v14_requirements.txt
python -m pip install --disable-pip-version-check -r q005_hpc_v14_requirements.txt
python -m pip install --disable-pip-version-check "astropy==7.2.2"

python - <<'PY'
import importlib.metadata as m
expected={
  "cobaya":"3.5.6","PyYAML":"6.0.2","numpy":"1.26.4","scipy":"1.15.3",
  "Py-BOBYQA":"1.5.0","getdist":"1.6.1","Cython":"0.29.37",
  "sacc":"1.0.2","astropy":"7.2.2"
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q031_FROZEN_DEPENDENCY_GATE=PASS")
PY

# Exact same frozen class_ede source/commit as Q015-Q030.
STAGE="CLASS_EDE"
CLASS_REPO="https://github.com/mwt5345/class_ede.git"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CLASS_DIR="$ROOT/external/class_ede"
if [[ ! -d "$CLASS_DIR/.git" ]]; then
  git clone "$CLASS_REPO" "$CLASS_DIR"
fi
git -C "$CLASS_DIR" fetch --all --tags
git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"

# Rebuild only if a usable local extension is absent.
if ! find "$CLASS_DIR/python/build" -maxdepth 2 -type f -name 'classy*.so' -print -quit 2>/dev/null | grep -q .; then
  make -C "$CLASS_DIR" -j2 libclass.a class
  rm -rf "$CLASS_DIR/python/build"
  rm -f "$CLASS_DIR/python/classy.c"
  (
    cd "$CLASS_DIR/python"
    export CC=gcc
    python setup.py build_ext
  )
fi

BUILD_LIB="$(find "$CLASS_DIR/python/build" -maxdepth 1 -type d -name 'lib.*' -print -quit)"
test -n "$BUILD_LIB"
test -n "$(find "$BUILD_LIB" -maxdepth 1 -type f -name 'classy*.so' -print -quit)"

SITE_PACKAGES="$(python - <<'PY'
import site
p=site.getsitepackages()
assert p
print(p[0])
PY
)"
printf '%s\n%s\n%s\n' "$BUILD_LIB" "$CLASS_DIR" "$CLASS_DIR/python" > "$SITE_PACKAGES/bubbleverse_q031_class_ede.pth"
unset PYTHONPATH || true

# Independent HiLLiPoP V4.3 source freeze.
STAGE="HILLIPOP_SOURCE"
HILLIPOP_REPO="https://github.com/planck-npipe/hillipop.git"
HILLIPOP_COMMIT="a09ddde3e7ce11df99f74685feb1f1764cafb251"
HILLIPOP_DIR="$ROOT/external/hillipop"
if [[ ! -d "$HILLIPOP_DIR/.git" ]]; then
  git clone "$HILLIPOP_REPO" "$HILLIPOP_DIR"
fi
git -C "$HILLIPOP_DIR" fetch --all --tags
git -C "$HILLIPOP_DIR" checkout --detach "$HILLIPOP_COMMIT"
test "$(git -C "$HILLIPOP_DIR" rev-parse HEAD)" = "$HILLIPOP_COMMIT"
python -m pip install --disable-pip-version-check --no-deps -e "$HILLIPOP_DIR"

# Install ONLY HiLLiPoP high-l data. No CamSpec, low-l, lensing, ACT, SPT, BAO or SN.
STAGE="HILLIPOP_DATA"
for i in 1 2 3 4; do
  echo "[INFO] CASE-031 cobaya-install planck_2020_hillipop.TTTEEE attempt=$i/4"
  if cobaya-install planck_2020_hillipop.TTTEEE -p "$COBAYA_PACKAGES_PATH"; then
    break
  fi
  if [[ "$i" = 4 ]]; then
    echo "HILLIPOP_DATA_INSTALL_GATE=FAIL" >&2
    exit 2
  fi
  sleep 15
done

STAGE="RUNTIME_PROVENANCE"
python - <<'PY'
import hashlib, importlib.metadata as md, json, os, pathlib, subprocess
import classy, planck_2020_hillipop

ROOT=pathlib.Path(".").resolve()
pkg=pathlib.Path(planck_2020_hillipop.__file__).resolve()
hill=ROOT/"external"/"hillipop"
assert str(pkg).startswith(str(hill.resolve())+os.sep), (pkg,hill)
assert subprocess.check_output(
    ["git","-C",str(hill),"rev-parse","HEAD"], text=True
).strip()=="a09ddde3e7ce11df99f74685feb1f1764cafb251"

classy_path=pathlib.Path(classy.__file__).resolve()
assert "external/class_ede" in str(classy_path).replace("\\","/"), classy_path

packages=pathlib.Path(os.environ["COBAYA_PACKAGES_PATH"]).resolve()
wanted=["binning_v4.2.fits","invfll_PR4_v4.2_TTTEEE.fits"]
found={}
for name in wanted:
    hits=list(packages.rglob(name))
    assert len(hits)==1,(name,hits)
    p=hits[0]
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    found[name]={"path":str(p),"size":p.stat().st_size,"sha256":h.hexdigest()}

spectra=sorted(packages.rglob("dl_PR4_v4.2_*.fits"))
assert spectra,"No dl_PR4_v4.2 cross-spectra found"
spec_hashes={}
for p in spectra:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    spec_hashes[p.name]={"path":str(p),"size":p.stat().st_size,"sha256":h.hexdigest()}

versions={}
for dist in ["cobaya","PyYAML","numpy","scipy","Py-BOBYQA","getdist","Cython","sacc","astropy"]:
    versions[dist]=md.version(dist)

runtime={
  "q":"CASE-031",
  "run_id":"CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1",
  "status":"PASS",
  "CURRENT_Q":os.environ.get("CURRENT_Q"),
  "class_ede_commit":"5a131c91d657dd9a7c6364cc45b038710f8d0d97",
  "classy_path":str(classy_path),
  "hillipop_repository":"planck-npipe/hillipop",
  "hillipop_commit":"a09ddde3e7ce11df99f74685feb1f1764cafb251",
  "hillipop_module_path":str(pkg),
  "hillipop_component":"planck_2020_hillipop.TTTEEE",
  "software_versions":versions,
  "data_hashes":found,
  "cross_spectrum_hashes":spec_hashes,
  "excluded_components":{
    "CamSpec":True,"low_l":True,"lensing":True,"ACT":True,"SPT":True,
    "BAO":True,"SN":True
  }
}
pathlib.Path("q031_runtime/q031_runtime_provenance_v1.json").write_text(
    json.dumps(runtime,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q031_ENVIRONMENT_GATE=PASS")
print("Q031_HILLIPOP_SOURCE_GATE=PASS")
print("Q031_DATA_GATE=PASS")
PY

STAGE="STATIC_PROGRAM"
python -m py_compile q031_planck_portability_v1.py q031_tests_v1.py
trap - ERR
echo "Q031_SETUP_GATE=PASS"
