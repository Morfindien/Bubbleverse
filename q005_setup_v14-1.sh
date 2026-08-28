#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

CONFIG="${Q005_CONFIG:-q005_hpc_v14_config.yml}"
PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
export COBAYA_PACKAGES_PATH="$PACKAGES_PATH"

mkdir -p external "$PACKAGES_PATH"

CLASS_REPO="https://github.com/mwt5345/class_ede.git"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CLASS_DIR="$ROOT/external/class_ede"

ACT_REPO="https://github.com/ACTCollaboration/DR6-ACT-lite.git"
ACT_COMMIT="0e0cd2c703c62a0e980470b572602233b27750e1"
ACT_DIR="$ROOT/external/DR6-ACT-lite"

echo "[INFO] Checkout frozen CLASS_EDE"
if [ ! -d "$CLASS_DIR/.git" ]; then
  git clone "$CLASS_REPO" "$CLASS_DIR"
fi
git -C "$CLASS_DIR" fetch --all --tags
git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"

echo "[INFO] Build frozen CLASS_EDE C core"
# IMPORTANT: do not run the default `make all` target here.
# `all` also invokes the legacy Python/Cython wrapper before we can control its
# NumPy/Cython compatibility environment.
make -C "$CLASS_DIR" -j2 libclass.a class

echo "[INFO] Build frozen CLASS_EDE Python wrapper with legacy-compatible NumPy/Cython"
python - <<'PY'
import numpy, Cython
print("[VALIDATION] NumPy for CLASS_EDE wrapper:", numpy.__version__)
print("[VALIDATION] Cython for CLASS_EDE wrapper:", Cython.__version__)
assert numpy.__version__ == "1.26.4"
assert Cython.__version__ == "0.29.37"
PY

rm -rf "$CLASS_DIR/python/build"
rm -f "$CLASS_DIR/python/classy.c"
(
  cd "$CLASS_DIR/python"
  export CC=gcc
  # Build only; do not let upstream `make all` run setup.py install implicitly.
  python setup.py build_ext
)
BUILD_LIB="$(find "$CLASS_DIR/python/build" -maxdepth 1 -type d -name 'lib.*' -print -quit)"
test -n "$BUILD_LIB"
CLASSY_SO="$(find "$BUILD_LIB" -maxdepth 1 -type f -name 'classy*.so' -print -quit)"
test -n "$CLASSY_SO"
export PYTHONPATH="$BUILD_LIB:$CLASS_DIR:$CLASS_DIR/python:${PYTHONPATH:-}"

python - <<'PY'
import classy, numpy, Cython
print("[VALIDATION] classy:", classy.__file__)
print("[VALIDATION] numpy:", numpy.__version__)
print("[VALIDATION] Cython:", Cython.__version__)
assert "/external/class_ede/" in classy.__file__.replace("\\", "/")
assert numpy.__version__ == "1.26.4"
assert Cython.__version__ == "0.29.37"
PY

echo "[INFO] Checkout frozen ACT DR6-lite"
if [ ! -d "$ACT_DIR/.git" ]; then
  git clone "$ACT_REPO" "$ACT_DIR"
fi
git -C "$ACT_DIR" fetch --all --tags
git -C "$ACT_DIR" checkout --detach "$ACT_COMMIT"
test "$(git -C "$ACT_DIR" rev-parse HEAD)" = "$ACT_COMMIT"
python -m pip install -e "$ACT_DIR"

echo "[INFO] Install ACT DR6 likelihood data"
TARGET="$PACKAGES_PATH/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
mkdir -p "$(dirname "$TARGET")"
install_ok=0

if cobaya-install act_dr6_cmbonly.ACTDR6CMBonly -p "$PACKAGES_PATH"; then
  if [ -s "$TARGET" ]; then install_ok=1; fi
fi

if [ "$install_ok" -ne 1 ]; then
  FOUND="$(find "$PACKAGES_PATH" -type f -name dr6_data_cmbonly.fits -print -quit || true)"
  if [ -n "$FOUND" ] && [ -s "$FOUND" ]; then
    cp "$FOUND" "$TARGET"
    install_ok=1
  fi
fi

if [ "$install_ok" -ne 1 ]; then
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  ARCHIVE="$TMP/dr6_data_cmbonly.tar.gz"

  ok=0
  for URL in \
    "https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz" \
    "https://portal.nersc.gov/project/act/dr6_data/dr6_data_cmbonly.tar.gz"
  do
    if curl -fL --retry 3 --retry-delay 10 --connect-timeout 30 --max-time 600 \
      "$URL" -o "$ARCHIVE"; then
      ok=1
      break
    fi
  done
  test "$ok" -eq 1
  test -s "$ARCHIVE"
  tar -xzf "$ARCHIVE" -C "$TMP"
  FOUND="$(find "$TMP" -type f -name dr6_data_cmbonly.fits -print -quit)"
  test -n "$FOUND"
  cp "$FOUND" "$TARGET"
fi

test -s "$TARGET"
export TARGET
python - <<'PY'
import hashlib, os
p=os.environ["TARGET"]
h=hashlib.sha256()
with open(p,"rb") as f:
    for chunk in iter(lambda:f.read(1024*1024),b""):
        h.update(chunk)
with open(p,"rb") as f:
    head=f.read(80)
assert head.startswith(b"SIMPLE"), "ACT data is not a FITS file"
print("[VALIDATION] ACT_BYTES =", os.path.getsize(p))
print("[VALIDATION] ACT_SHA256 =", h.hexdigest())
PY

echo "[INFO] Install remaining likelihood data"
cobaya-install planck_2018_lowl.EE_sroll2 -p "$PACKAGES_PATH"
cobaya-install bao.desi_dr2 -p "$PACKAGES_PATH"

echo "[INFO] Full Bubbleverse preflight"
python q005_hpc_v14.py --config "$CONFIG" preflight
