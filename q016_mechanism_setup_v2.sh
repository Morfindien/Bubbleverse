#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
BRANCH="${1:?branch required: planck|spt|act}"
case "$BRANCH" in
  planck|spt|act) ;;
  *) echo "Q016_MECHANISM_V2_SETUP_BRANCH_GATE=FAIL $BRANCH" >&2; exit 2 ;;
esac

export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH"

# V1 repair: reproduce the exact prerequisite used by the successful V16 workflow.
python -m pip install --upgrade pip
python -m pip install -r q005_hpc_v14_requirements.txt

python - <<'PY'
import importlib.metadata as m
expected={
 'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3',
 'Py-BOBYQA':'1.5.0','getdist':'1.6.1','Cython':'0.29.37','sacc':'1.0.2'
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q016_MECHANISM_V2_PRE_V16_FROZEN_DEPENDENCY_GATE=PASS")
PY

# Reuse V1's already successful ACT-lite artifact instead of downloading it again.
if [[ "$BRANCH" == "act" && -f "$ROOT/q016_act_data_v1/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits" ]]; then
  TARGET="$COBAYA_PACKAGES_PATH/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
  mkdir -p "$(dirname "$TARGET")"
  cp "$ROOT/q016_act_data_v1/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits" "$TARGET"
  echo "Q016_MECHANISM_V2_V1_ACT_ASSET_REUSE_GATE=PASS"
fi

# Unchanged known-good V16 branch setup.
bash q016_setup_v16.sh "$BRANCH"

# Optional ACT full-MF package: secondary diagnostic only; must not mutate frozen stack.
if [[ "$BRANCH" == "act" ]]; then
  set +e
  python -m pip install --no-deps     "git+https://github.com/ACTCollaboration/act_dr6_mflike.git@4220e14efb3a995f47c9f54cb687479e558c6138"
  ACT_MF_RC=$?
  set -e
  echo "ACT_FULL_MF_INSTALL_RC=${ACT_MF_RC}"
fi

python - <<'PY'
import importlib.metadata as m
expected={
 'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3',
 'Py-BOBYQA':'1.5.0','getdist':'1.6.1','Cython':'0.29.37','sacc':'1.0.2'
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q016_MECHANISM_V2_POST_SETUP_FROZEN_STACK_GATE=PASS")
PY
