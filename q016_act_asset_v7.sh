#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
OUT_ROOT="${1:-q016_act_asset_v7}"
TARGET="$OUT_ROOT/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits"
MANIFEST="$OUT_ROOT/q016_act_data_manifest_v7.json"
mkdir -p "$(dirname "$TARGET")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

validate_fits() {
  local f="$1"
  test -s "$f" || return 1
  FILE="$f" python - <<'PY'
import hashlib, json, os
from pathlib import Path
p=Path(os.environ["FILE"])
head=p.read_bytes()[:80]
assert head.startswith(b"SIMPLE"), head[:16]
h=hashlib.sha256()
with p.open("rb") as f:
    for b in iter(lambda:f.read(1024*1024),b""):
        h.update(b)
print(h.hexdigest())
PY
}

ARCHIVE="$TMP/dr6_data_cmbonly.tar.gz"
ok=0
used=""
for URL in \
  "https://lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/dr6_data_cmbonly.tar.gz" \
  "https://portal.nersc.gov/project/act/dr6_data/dr6_data_cmbonly.tar.gz"
do
  echo "[INFO] Q016 ACT data candidate: $URL"
  rm -f "$ARCHIVE"
  if curl -fL \
      --retry 3 --retry-all-errors --retry-delay 5 \
      --connect-timeout 30 --max-time 300 \
      "$URL" -o "$ARCHIVE"; then
    if tar -tzf "$ARCHIVE" >/dev/null 2>&1; then
      rm -rf "$TMP/extract"; mkdir -p "$TMP/extract"
      tar -xzf "$ARCHIVE" -C "$TMP/extract"
      FOUND="$(find "$TMP/extract" -type f -name dr6_data_cmbonly.fits -print -quit)"
      if [[ -n "$FOUND" ]] && validate_fits "$FOUND" >/tmp/q016_act_sha; then
        cp "$FOUND" "$TARGET"
        used="$URL"
        ok=1
        break
      fi
    fi
  fi
done
test "$ok" -eq 1 || { echo "Q016_ACT_DATA_FETCH_GATE=FAIL" >&2; exit 71; }

SHA="$(validate_fits "$TARGET")"
BYTES="$(stat -c %s "$TARGET")"
URL_USED="$used" SHA_USED="$SHA" BYTES_USED="$BYTES" TARGET_USED="$TARGET" MANIFEST_USED="$MANIFEST" python - <<'PY'
import json,os
from pathlib import Path
d={
 "q":"Q016",
 "run_id":"Q016-MATCHED-CMB-SURFACE-V7",
 "result_id":"R-Q016-EDE-MATCHED-CMB-SURFACE-007",
 "asset":"ACT_DR6_CMBONLY",
 "source_url":os.environ["URL_USED"],
 "sha256":os.environ["SHA_USED"],
 "bytes":int(os.environ["BYTES_USED"]),
 "target_relative_path":"data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits",
 "fits_header_gate":"PASS",
 "scientific_surface_changed":False
}
p=Path(os.environ["MANIFEST_USED"]); p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
print(json.dumps(d,indent=2,sort_keys=True))
PY
echo "Q016_ACT_DATA_FETCH_GATE=PASS sha256=$SHA bytes=$BYTES source=$used"
