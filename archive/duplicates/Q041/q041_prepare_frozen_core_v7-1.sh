#!/usr/bin/env bash
set -euo pipefail

MODE="${1:?usage: q041_prepare_frozen_core_v7.sh camspec|hillipop|both}"
case "$MODE" in
  camspec|hillipop|both) ;;
  *) echo "Q041_CORE_MODE_GATE=FAIL mode=$MODE" >&2; exit 2 ;;
esac

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
PARENT="$ROOT/q032_parent"
CACHE_ROOT="$ROOT/external"
EXPECTED_Q032="4dc873a5e880d40858d831a3b421456728f0c032"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT="a09ddde3e7ce11df99f74685feb1f1764cafb251"

[[ -d "$PARENT/.git" || -f "$PARENT/.git" ]] || {
  echo "Q041_Q032_WORKTREE_GATE=FAIL" >&2
  exit 2
}
test "$(git -C "$PARENT" rev-parse HEAD)" = "$EXPECTED_Q032"

mkdir -p "$CACHE_ROOT/cobaya_packages"

cache_ready=true
[[ -d "$CACHE_ROOT/class_ede/.git" ]] || cache_ready=false
[[ -d "$CACHE_ROOT/hillipop/.git" ]] || cache_ready=false
if [[ "$cache_ready" == true ]]; then
  [[ "$(git -C "$CACHE_ROOT/class_ede" rev-parse HEAD 2>/dev/null || true)" == "$CLASS_COMMIT" ]] || cache_ready=false
  [[ "$(git -C "$CACHE_ROOT/hillipop" rev-parse HEAD 2>/dev/null || true)" == "$HILLIPOP_COMMIT" ]] || cache_ready=false
fi

# HiLLiPoP data are required by the frozen helper even for a CamSpec-only sample
# because the Q032 shared cache identity is sealed as a both-arm runtime.
if [[ "$cache_ready" == true ]]; then
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'invfll_PR4_v4.2_TT.fits' -print -quit)" || cache_ready=false
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'binning_v4.2.fits' -print -quit)" || cache_ready=false
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'dl_PR4_v4.2_*.fits' -print -quit)" || cache_ready=false
fi

if [[ "$cache_ready" == true ]]; then
  echo "Q041_Q032_CACHE_GATE=HIT"
  # Reuse the already validated Q039 wrapper to reinstall Python bindings and
  # re-assert the exact frozen Q032 identity.
  bash "$ROOT/q039_prepare_frozen_env_v4.sh" "$MODE"
else
  echo "Q041_Q032_CACHE_GATE=MISS_BOOTSTRAP"

  HLP_TT_URL="https://portal.nersc.gov/cfs/cmb/planck2020/likelihoods/planck_2020_hillipop_TT_v4.2.tar.gz"
  NERSC_READY=false
  for i in 1 2 3; do
    echo "[INFO] Q041 NERSC TT availability probe attempt=$i/3"
    if curl -fsS --range 0-0 --connect-timeout 10 --max-time 30 -o /dev/null "$HLP_TT_URL"; then
      NERSC_READY=true
      break
    fi
    sleep 10
  done
  if [[ "$NERSC_READY" != true ]]; then
    echo "Q041_NERSC_TT_AVAILABILITY_GATE=FAIL_FAST" >&2
    exit 75
  fi
  echo "Q041_NERSC_TT_AVAILABILITY_GATE=PASS"

  rm -rf "$PARENT/external"
  ln -s "$CACHE_ROOT" "$PARENT/external"
  export COBAYA_PACKAGES_PATH="$CACHE_ROOT/cobaya_packages"

  Q032_SETUP_RUNNER="$PARENT/q032_setup_v2_q041_v7.sh"
  cp "$PARENT/q032_setup_v2.sh" "$Q032_SETUP_RUNNER"

  python - "$Q032_SETUP_RUNNER" <<'PYPATCH'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
old="""for i in 1 2 3 4; do
    echo "[INFO] Q032 cobaya-install planck_2020_hillipop.TT attempt=$i/4"
    if cobaya-install planck_2020_hillipop.TT -p "$COBAYA_PACKAGES_PATH"; then break; fi
    if [[ "$i" == 4 ]]; then
      echo "Q032_HILLIPOP_TT_DATA_INSTALL_GATE=FAIL" >&2
      exit 2
    fi
    sleep 15
  done"""
new="""for i in 1 2; do
    echo "[INFO] Q041 bounded Q032 cobaya-install planck_2020_hillipop.TT attempt=$i/2"
    if timeout --signal=TERM 1200s cobaya-install planck_2020_hillipop.TT -p "$COBAYA_PACKAGES_PATH"; then break; fi
    if [[ "$i" == 2 ]]; then
      echo "Q041_Q032_HILLIPOP_TT_BOUNDED_INSTALL_GATE=FAIL" >&2
      exit 2
    fi
    sleep 15
  done"""
if old not in s:
    raise SystemExit("Q041_Q032_INSTALLER_PATCH_SIGNATURE_GATE=FAIL")
p.write_text(s.replace(old,new,1),encoding="utf-8")
print("Q041_Q032_INSTALLER_PATCH_GATE=PASS")
PYPATCH

  bash "$Q032_SETUP_RUNNER" both
  rm -f "$Q032_SETUP_RUNNER"
fi

test "$(git -C "$CACHE_ROOT/class_ede" rev-parse HEAD)" = "$CLASS_COMMIT"
test "$(git -C "$CACHE_ROOT/hillipop" rev-parse HEAD)" = "$HILLIPOP_COMMIT"

export COBAYA_PACKAGES_PATH="$CACHE_ROOT/cobaya_packages"
python - <<'PY'
import importlib.metadata as m, os, pathlib, sys
assert sys.version_info[:2] == (3,11), sys.version
expected = {
    'cobaya':'3.5.6',
    'PyYAML':'6.0.2',
    'numpy':'1.26.4',
    'scipy':'1.15.3',
    'Py-BOBYQA':'1.5.0',
    'getdist':'1.6.1',
    'sacc':'1.0.2',
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
packages=pathlib.Path(os.environ['COBAYA_PACKAGES_PATH']).resolve()
assert packages.exists()
assert list(packages.rglob('invfll_PR4_v4.2_TT.fits'))
assert list(packages.rglob('binning_v4.2.fits'))
assert list(packages.rglob('dl_PR4_v4.2_*.fits'))
print('Q041_FROZEN_Q032_CORE_GATE=PASS')
PY
