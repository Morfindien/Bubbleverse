#!/usr/bin/env bash
set -euo pipefail
MODE="${1:?usage: q039_prepare_frozen_env_v4.sh camspec|hillipop|both}"
case "$MODE" in camspec|hillipop|both) ;; *) echo "Q039_ENV_MODE_GATE=FAIL mode=$MODE" >&2; exit 2;; esac
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
PARENT="$ROOT/q032_parent"
CACHE_ROOT="$ROOT/external"
EXPECTED_Q032="4dc873a5e880d40858d831a3b421456728f0c032"
[[ -d "$PARENT/.git" || -f "$PARENT/.git" ]] || { echo "Q039_Q032_WORKTREE_GATE=FAIL" >&2; exit 2; }
test "$(git -C "$PARENT" rev-parse HEAD)" = "$EXPECTED_Q032"
test -d "$CACHE_ROOT/cobaya_packages"
test -d "$CACHE_ROOT/class_ede"
test -d "$CACHE_ROOT/hillipop"
if [[ "$MODE" == "hillipop" || "$MODE" == "both" ]]; then
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'invfll_PR4_v4.2_TT.fits' -print -quit)"
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'binning_v4.2.fits' -print -quit)"
  test -n "$(find "$CACHE_ROOT/cobaya_packages" -type f -name 'dl_PR4_v4.2_*.fits' -print -quit)"
fi
rm -rf "$PARENT/external"
ln -s "$CACHE_ROOT" "$PARENT/external"
export COBAYA_PACKAGES_PATH="$PARENT/external/cobaya_packages"
bash "$PARENT/q032_setup_v2.sh" "$MODE"
test "$(git -C "$PARENT/external/class_ede" rev-parse HEAD)" = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
test "$(git -C "$PARENT/external/hillipop" rev-parse HEAD)" = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
python - <<'PYENV'
import importlib.metadata as m, os, pathlib
expected={'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3','Py-BOBYQA':'1.5.0'}
for p,v in expected.items():
    a=m.version(p); assert a==v,(p,a,v)
packages=pathlib.Path(os.environ['COBAYA_PACKAGES_PATH']).resolve(); assert packages.exists()
print('Q039_AUTHORITATIVE_Q032_CACHE_ENV_GATE=PASS')
PYENV
