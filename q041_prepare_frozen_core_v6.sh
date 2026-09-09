#!/usr/bin/env bash
set -euo pipefail

MODE="${1:?usage: q041_prepare_frozen_core_v6.sh camspec|hillipop|both}"
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
  # Cold-cache path: make Q032's own exact setup write into the root external
  # cache, then let the same locked Q032 setup build both native Planck arms.
  rm -rf "$PARENT/external"
  ln -s "$CACHE_ROOT" "$PARENT/external"
  export COBAYA_PACKAGES_PATH="$CACHE_ROOT/cobaya_packages"
  bash "$PARENT/q032_setup_v2.sh" both
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
