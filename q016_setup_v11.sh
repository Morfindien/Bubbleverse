#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
BRANCH="${1:?branch required: planck|spt|act}"
case "$BRANCH" in planck|spt|act) ;; *) echo "Q016_SETUP_BRANCH_GATE=FAIL $BRANCH" >&2; exit 2;; esac

export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p external "$COBAYA_PACKAGES_PATH" q016_results q016_v11_source_runtime

CURRENT_Q="Q016"
RUN_ID="Q016-MATCHED-CMB-SURFACE-V11"
RESULT_ID="R-Q016-EDE-MATCHED-CMB-SURFACE-011"
STAGE="INITIALIZE"

write_failure() {
  rc=$?
  trap - ERR
  STAGE_LOCAL="$STAGE" BRANCH_LOCAL="$BRANCH" RC_LOCAL="$rc" python - <<'PY'
import json, os, platform
from datetime import datetime, timezone
from pathlib import Path
p=Path("q016_results")/f"q016_setup_failure_{os.environ['BRANCH_LOCAL']}.json"
d={
 "q":"Q016","run_id":"Q016-MATCHED-CMB-SURFACE-V11",
 "result_id":"R-Q016-EDE-MATCHED-CMB-SURFACE-011",
 "status":"TECHNICAL_FAILURE","failure_class":"ENVIRONMENT_OR_NETWORK",
 "stage":os.environ["STAGE_LOCAL"],"branch":os.environ["BRANCH_LOCAL"],
 "exit_code":int(os.environ["RC_LOCAL"]),
 "scientific_model_failure":False,"scientific_result":"NOT_AVAILABLE",
 "timestamp_utc":datetime.now(timezone.utc).isoformat(),
 "python":platform.python_version(),"platform":platform.platform()
}
p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
print(json.dumps(d,indent=2,sort_keys=True))
PY
  exit "$rc"
}
trap write_failure ERR

retry_cobaya_install() {
  local component="$1"
  local i
  for i in 1 2 3 4; do
    echo "[INFO] cobaya-install $component attempt=$i/4"
    if cobaya-install "$component" -p "$COBAYA_PACKAGES_PATH"; then return 0; fi
    [[ "$i" = 4 ]] || sleep 15
  done
  return 1
}

STAGE="FROZEN_DEPENDENCY_GATE"
python - <<'PY'
import importlib.metadata as m
expected={
 'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3',
 'Py-BOBYQA':'1.5.0','getdist':'1.6.1','Cython':'0.29.37','sacc':'1.0.2'
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q016_FROZEN_DEPENDENCY_GATE=PASS")
PY

CLASS_REPO="https://github.com/mwt5345/class_ede.git"
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CLASS_DIR="$ROOT/external/class_ede"

STAGE="CHECKOUT_CLASS_EDE"
if [[ ! -d "$CLASS_DIR/.git" ]]; then git clone "$CLASS_REPO" "$CLASS_DIR"; fi
git -C "$CLASS_DIR" fetch --all --tags
git -C "$CLASS_DIR" checkout --detach "$CLASS_COMMIT"
test "$(git -C "$CLASS_DIR" rev-parse HEAD)" = "$CLASS_COMMIT"

STAGE="BUILD_CLASS_EDE"
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

STAGE="PERSIST_CLASS_EDE_IMPORT"
SITE_PACKAGES="$(python - <<'PY'
import site
p=site.getsitepackages()
assert p
print(p[0])
PY
)"
CLASS_PTH="$SITE_PACKAGES/bubbleverse_q016_class_ede.pth"
printf '%s\n%s\n%s\n' "$BUILD_LIB" "$CLASS_DIR" "$CLASS_DIR/python" > "$CLASS_PTH"
unset PYTHONPATH || true
CLASS_DIR_EXPECTED="$CLASS_DIR" python - <<'PY'
import os, pathlib, classy, numpy, Cython
assert numpy.__version__=="1.26.4",numpy.__version__
assert Cython.__version__=="0.29.37",Cython.__version__
p=pathlib.Path(classy.__file__).resolve()
e=pathlib.Path(os.environ["CLASS_DIR_EXPECTED"]).resolve()
assert str(p).startswith(str(e)+os.sep),(p,e)
print("Q016_CLASS_EDE_PERSISTENCE_GATE=PASS",p)
PY

if [[ "$BRANCH" == "planck" ]]; then
  STAGE="INSTALL_PLANCK_NPIPE_LITE"
  PDIR="$ROOT/external/camspec_npipe-lite"
  PCOMMIT="e387852d2ae8863735814449c682b089c3059318"
  if [[ ! -d "$PDIR/.git" ]]; then git clone https://github.com/HTJense/camspec_npipe-lite.git "$PDIR"; fi
  git -C "$PDIR" fetch --all --tags
  git -C "$PDIR" checkout --detach "$PCOMMIT"
  test "$(git -C "$PDIR" rev-parse HEAD)" = "$PCOMMIT"
  python -m pip install --no-deps -e "$PDIR"
  retry_cobaya_install camspec_npipe_lite
  python - <<'PY'
import camspec_npipe_lite, pathlib, os
from camspec_npipe_lite import planck_Camspec_NPIPE_lite
print("Q016_PLANCK_MODULE_GATE=PASS",camspec_npipe_lite.__file__)
PY
fi

if [[ "$BRANCH" == "spt" ]]; then
  STAGE="INSTALL_SPT_D1_LITE"
  python -m pip install "candl-like==2.0.3"
  SDIR="$ROOT/external/spt_candl_data"
  SCOMMIT="2cec6e762a8c540484dd5acafc529f0035856350"
  if [[ ! -d "$SDIR/.git" ]]; then git clone https://github.com/SouthPoleTelescope/spt_candl_data.git "$SDIR"; fi
  git -C "$SDIR" fetch --all --tags --prune
  git -C "$SDIR" checkout --detach "$SCOMMIT"
  test "$(git -C "$SDIR" rev-parse HEAD)" = "$SCOMMIT"
  if command -v git-lfs >/dev/null 2>&1; then git -C "$SDIR" lfs pull || true; fi
  python -m pip install -e "$SDIR"
  python - <<'PY'
import candl, spt_candl_data, importlib.metadata as md, pathlib
assert md.version("candl-like")=="2.0.3",md.version("candl-like")
p=pathlib.Path(spt_candl_data.SPT3G_D1_TnE_lite)
assert p.is_file(),p
print("Q016_SPT_LITE_GATE=PASS",p)
PY
fi

if [[ "$BRANCH" == "act" ]]; then
  STAGE="INSTALL_ACT_DR6_LITE_CODE"
  ADIR="$ROOT/external/DR6-ACT-lite"
  ACOMMIT="0e0cd2c703c62a0e980470b572602233b27750e1"
  if [[ ! -d "$ADIR/.git" ]]; then git clone https://github.com/ACTCollaboration/DR6-ACT-lite.git "$ADIR"; fi
  git -C "$ADIR" fetch --all --tags
  git -C "$ADIR" checkout --detach "$ACOMMIT"
  test "$(git -C "$ADIR" rev-parse HEAD)" = "$ACOMMIT"
  python -m pip install --no-deps -e "$ADIR"

  STAGE="VALIDATE_ACT_DR6_DATA"
  TARGET="$COBAYA_PACKAGES_PATH/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
  if [[ ! -s "$TARGET" ]]; then
    echo "[INFO] Shared ACT asset not preseeded; bounded standalone fallback."
    TMPA="$(mktemp -d)"
    trap 'rm -rf "$TMPA"' RETURN
    ok=0
    for URL in       "https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz"       "https://portal.nersc.gov/project/act/dr6_data/dr6_data_cmbonly.tar.gz"
    do
      ARCH="$TMPA/dr6_data_cmbonly.tar.gz"
      rm -f "$ARCH"
      if curl -fL --retry 3 --retry-all-errors --retry-delay 5           --connect-timeout 30 --max-time 300 "$URL" -o "$ARCH"; then
        rm -rf "$TMPA/extract"; mkdir -p "$TMPA/extract"
        if tar -xzf "$ARCH" -C "$TMPA/extract"; then
          FOUND="$(find "$TMPA/extract" -type f -name dr6_data_cmbonly.fits -print -quit)"
          if [[ -n "$FOUND" ]]; then
            mkdir -p "$(dirname "$TARGET")"; cp "$FOUND" "$TARGET"; ok=1; break
          fi
        fi
      fi
    done
    test "$ok" -eq 1
  fi
  TARGET="$TARGET" python - <<'PY'
import hashlib,os
from pathlib import Path
p=Path(os.environ["TARGET"])
assert p.is_file() and p.stat().st_size>0,p
with p.open("rb") as f: head=f.read(80)
assert head.startswith(b"SIMPLE"),head[:16]
h=hashlib.sha256()
with p.open("rb") as f:
    for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
print("Q016_ACT_DATA_GATE=PASS",p.stat().st_size,h.hexdigest())
PY
  python - <<'PY'
import act_dr6_cmbonly
from act_dr6_cmbonly import ACTDR6CMBonly
print("Q016_ACT_MODULE_GATE=PASS",act_dr6_cmbonly.__file__)
PY
fi

STAGE="POST_EXTERNAL_PIN_GATE"
python - <<'PY'
import importlib.metadata as m
expected={
 'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3',
 'Py-BOBYQA':'1.5.0','Cython':'0.29.37','sacc':'1.0.2'
}
for p,v in expected.items():
    a=m.version(p)
    assert a==v,(p,a,v)
print("Q016_POST_EXTERNAL_PIN_GATE=PASS")
PY

STAGE="WRITE_RUNTIME_PROVENANCE"
BRANCH_LOCAL="$BRANCH" python - <<'PY'
import json, os, pathlib, subprocess, importlib.metadata as md, importlib
d={
 "q":"Q016","run_id":"Q016-MATCHED-CMB-SURFACE-V11",
 "result_id":"R-Q016-EDE-MATCHED-CMB-SURFACE-011",
 "branch":os.environ["BRANCH_LOCAL"],
 "class_ede_commit":"5a131c91d657dd9a7c6364cc45b038710f8d0d97",
 "versions":{
   "cobaya":md.version("cobaya"),"numpy":md.version("numpy"),
   "scipy":md.version("scipy"),"Cython":md.version("Cython"),"sacc":md.version("sacc")
 }
}
b=d["branch"]
if b=="planck":
 d["camspec_npipe_lite_commit"]=subprocess.check_output(["git","-C","external/camspec_npipe-lite","rev-parse","HEAD"],text=True).strip()
elif b=="spt":
 d["candl_version"]=md.version("candl-like")
 d["spt_candl_data_commit"]=subprocess.check_output(["git","-C","external/spt_candl_data","rev-parse","HEAD"],text=True).strip()
elif b=="act":
 d["act_dr6_lite_commit"]=subprocess.check_output(["git","-C","external/DR6-ACT-lite","rev-parse","HEAD"],text=True).strip()
 target=pathlib.Path(os.environ["COBAYA_PACKAGES_PATH"])/"data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
 import hashlib
 h=hashlib.sha256()
 with target.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 d["act_dr6_data_sha256"]=h.hexdigest()
 d["act_dr6_data_bytes"]=target.stat().st_size
p=pathlib.Path("q016_v11_source_runtime")/f"setup_{b}.json"
p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
print("Q016_RUNTIME_PROVENANCE_GATE=PASS",p)
PY

STAGE="COMPLETE"
trap - ERR
echo "Q016_SETUP_GATE=PASS branch=$BRANCH"
