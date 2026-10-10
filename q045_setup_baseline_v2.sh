#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:?}"
cd "$ROOT"
export COBAYA_PACKAGES_PATH="$ROOT/external/cobaya_packages"
# Reconstruct only pinned Python interfaces; never build or replace CLASS/data.
python -m pip install --disable-pip-version-check -r q045_native_baseline_requirements_v2.txt
# With --no-build-isolation we must supply the pinned lensing build backend.
python -c 'import json,q045_native_baseline_v2 as m; print(json.dumps(m.build_backend_preflight()))'
for DIR in external/hillipop external/act_dr6_cmbonly external/act_dr6_lenslike; do
  test -d "$DIR/.git"
  python -m pip install --disable-pip-version-check --no-deps --no-build-isolation -e "$DIR"
done
# Q032 builders resolve their native backend through this path relocation.
test ! -e q032_parent/external
ln -s "$ROOT/external" q032_parent/external
# Reuse the known-good DESI-definition and pandas compatibility backport.
# clone_exact is read-only here: cached source must already match the pin.
clone_exact() {
  local expected="$2" dir="$3"
  test "$(git -C "$dir" rev-parse HEAD)" = "$expected"
}
export -f clone_exact
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

# Compatibility-only backport from pinned Cobaya commit b76b6fed...
BAO_BASE="$COBAYA_DIR/likelihoods/base_classes/bao.py"
python - "$BAO_BASE" <<'PY'
from pathlib import Path
import re
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")

compat_marker = "type_last_col.__class__ == pd.StringDtype"
if compat_marker not in s:
    pat = re.compile(
        r'(?m)^(?P<indent>[ \t]*)self\.has_type\s*=\s*'
        r'self\.data\.iloc\[:,\s*-1\]\.dtype\s*==\s*'
        r'np\.dtype\((?P<q>["\'])O(?P=q)\)\s*$'
    )
    m = pat.search(s)
    if not m:
        print("Q041_DESI_DR2_BAO_DTYPE_PATCH_DIAGNOSTIC_BEGIN", file=sys.stderr)
        for i, line in enumerate(s.splitlines(), 1):
            if "has_type" in line or "self.data.iloc[:, -1].dtype" in line:
                print(f"{i}: {line}", file=sys.stderr)
        print("Q041_DESI_DR2_BAO_DTYPE_PATCH_DIAGNOSTIC_END", file=sys.stderr)
        raise SystemExit("Q041_DESI_DR2_BAO_DTYPE_PATCH_SIGNATURE_GATE=FAIL")
    indent = m.group("indent")
    replacement = (
        f"{indent}type_last_col = self.data.iloc[:, -1].dtype\n"
        f"{indent}self.has_type = (\n"
        f'{indent}    type_last_col == np.dtype("O")  # pandas < v3\n'
        f"{indent}    or type_last_col.__class__ == pd.StringDtype  # pandas >= v3\n"
        f"{indent})"
    )
    s = s[:m.start()] + replacement + s[m.end():]
    p.write_text(s, encoding="utf-8")

verify = p.read_text(encoding="utf-8")
assert compat_marker in verify
compile(verify, str(p), "exec")
print("Q041_DESI_DR2_BAO_DTYPE_COMPATIBILITY_PATCH_GATE=PASS")
PY

python - <<'PY'
import inspect, pandas as pd
from cobaya.likelihoods.base_classes import BAO
src=inspect.getsource(BAO.initialize)
assert 'type_last_col.__class__ == pd.StringDtype' in src
print("Q041_DESI_DR2_BAO_STRINGDTYPE_RUNTIME_GATE=PASS pandas="+pd.__version__)
PY


# No data download, no solver rebuild, no PolyChord installation or invocation.
