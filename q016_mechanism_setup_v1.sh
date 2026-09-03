#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
BRANCH="${1:?branch required: planck|spt|act}"
case "$BRANCH" in planck|spt|act) ;; *) echo "Q016_MECHANISM_SETUP_BRANCH_GATE=FAIL $BRANCH" >&2; exit 2;; esac

export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH"

# If the workflow downloaded the shared ACT asset, seed it into the exact
# packages path expected by the known-good V16 setup before that setup runs.
if [[ "$BRANCH" == "act" && -f "$ROOT/q016_act_data_v1/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits" ]]; then
  TARGET="$COBAYA_PACKAGES_PATH/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
  mkdir -p "$(dirname "$TARGET")"
  cp "$ROOT/q016_act_data_v1/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits" "$TARGET"
  echo "Q016_MECHANISM_ACT_SHARED_ASSET_SEEDED=PASS"
fi

# q016_setup_v16.sh is the frozen, already-executed environment builder.
# It pins numpy/scipy/Cobaya/Cython/class_ede and the branch likelihood.
bash q016_setup_v16.sh "$BRANCH"

# Q015 attribution module imports candl interfaces. Keep frozen dependencies
# untouched: install package code without allowing dependency upgrades.
python -m pip install --no-deps "candl-like==2.0.3"

# ACT full MF is a SECONDARY DIAGNOSTIC ONLY. Install package code without
# dependency mutation. Failure is allowed and becomes TECHNICALLY_UNAVAILABLE.
if [[ "$BRANCH" == "act" ]]; then
  set +e
  python -m pip install --no-deps \
    "git+https://github.com/ACTCollaboration/act_dr6_mflike.git@4220e14efb3a995f47c9f54cb687479e558c6138"
  ACT_MF_RC=$?
  set -e
  echo "ACT_FULL_MF_INSTALL_RC=${ACT_MF_RC}"
fi

# Ensure the frozen numerical stack has not moved.
python - <<'PY'
import importlib.metadata as m
expected={
  "cobaya":"3.5.6","PyYAML":"6.0.2","numpy":"1.26.4","scipy":"1.15.3",
  "Py-BOBYQA":"1.5.0","Cython":"0.29.37","sacc":"1.0.2"
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q016_MECHANISM_POST_SETUP_FROZEN_STACK_GATE=PASS")
PY
