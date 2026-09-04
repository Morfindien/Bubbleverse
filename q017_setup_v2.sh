#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH" external q017_results q017_source_runtime

STAGE="BOOTSTRAP"
failure() {
  rc=$?
  trap - ERR
  STAGE_LOCAL="$STAGE" RC_LOCAL="$rc" python - <<'PY'
import json, os
from pathlib import Path
p=Path("q017_results/q017_setup_failure_v2.json")
p.write_text(json.dumps({
  "q":"Q017",
  "run_id":"Q017-PLANCK-DIRECTION-LOCALIZATION-V2",
  "result_id":"R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-002",
  "status":"TECHNICALLY_UNAVAILABLE",
  "failure_class":"ENVIRONMENT_OR_FULL_MF_SETUP",
  "stage":os.environ["STAGE_LOCAL"],
  "exit_code":int(os.environ["RC_LOCAL"]),
  "scientific_model_failure":False,
  "q016_result_invalidated":False
},indent=2,sort_keys=True)+"\n")
PY
  exit "$rc"
}
trap failure ERR

STAGE="FROZEN_DEPENDENCIES"
python -m pip install --upgrade pip
python -m pip install -r q005_hpc_v14_requirements.txt
python - <<'PY'
import importlib.metadata as m
expected={
  "cobaya":"3.5.6","PyYAML":"6.0.2","numpy":"1.26.4","scipy":"1.15.3",
  "Py-BOBYQA":"1.5.0","getdist":"1.6.1","Cython":"0.29.37","sacc":"1.0.2"
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q017_V2_FROZEN_DEPENDENCY_GATE=PASS")
PY

STAGE="CLASS_EDE"
CLASS_REPO="https://github.com/mwt5345/class_ede.git"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CLASS_DIR="$ROOT/external/class_ede"
if [[ ! -d "$CLASS_DIR/.git" ]]; then git clone "$CLASS_REPO" "$CLASS_DIR"; fi
git -C "$CLASS_DIR" fetch --all --tags
git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"
make -C "$CLASS_DIR" -j2 libclass.a class
rm -rf "$CLASS_DIR/python/build"
rm -f "$CLASS_DIR/python/classy.c"
(
  cd "$CLASS_DIR/python"
  export CC=gcc
  python setup.py build_ext
)
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
printf '%s\n%s\n%s\n' "$BUILD_LIB" "$CLASS_DIR" "$CLASS_DIR/python" > "$SITE_PACKAGES/bubbleverse_q017_class_ede.pth"
unset PYTHONPATH || true

STAGE="PLANCK_FULL_MF"
retry_install() {
  local component="$1"
  for i in 1 2 3 4; do
    echo "[INFO] cobaya-install $component attempt=$i/4"
    if cobaya-install "$component" -p "$COBAYA_PACKAGES_PATH"; then return 0; fi
    [[ "$i" = 4 ]] || sleep 15
  done
  return 1
}
retry_install planck_NPIPE_highl_CamSpec.TTTEEE

STAGE="CAPABILITY_GATE"
python - <<'PY'
import pathlib, classy, importlib.metadata as md
from cobaya.model import get_model
assert md.version("cobaya")=="3.5.6"
p=pathlib.Path(classy.__file__).resolve()
assert "external/class_ede" in str(p).replace("\\","/"), p
print("Q017_V2_CLASS_EDE_GATE=PASS",p)
print("Q017_V2_PLANCK_FULL_MF_INSTALL_GATE=PASS")
PY

STAGE="SOURCE_PROVENANCE"
python - <<'PY'
import json, subprocess, pathlib, importlib.metadata as md
d={
 "q":"Q017",
 "run_id":"Q017-PLANCK-DIRECTION-LOCALIZATION-V2",
 "result_id":"R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-002",
 "class_ede_commit":subprocess.check_output(["git","-C","external/class_ede","rev-parse","HEAD"],text=True).strip(),
 "cobaya_version":md.version("cobaya"),
 "numpy_version":md.version("numpy"),
 "scipy_version":md.version("scipy"),
 "pybobyqa_version":md.version("Py-BOBYQA"),
 "planck_component":"planck_NPIPE_highl_CamSpec.TTTEEE",
 "q016_cosmological_profiles_rerun":False,
 "q011_endpoint_used":False
}
pathlib.Path("q017_source_runtime/setup.json").write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
print("Q017_V2_RUNTIME_PROVENANCE_GATE=PASS")
PY

STAGE="COMPLETE"
trap - ERR
echo "Q017_V2_SETUP_GATE=PASS"
