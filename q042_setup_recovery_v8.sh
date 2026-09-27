#!/usr/bin/env bash
set -euo pipefail

# Rebuild/reassert the already frozen V1/V11 scientific runtime.
# This does not create a new scientific environment.
bash q042_prepare_frozen_core_v4.sh both
bash q042_setup_prod_v1.sh

python - <<'PY'
import json, hashlib, pathlib

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

assert sha('q042_production_spec_v1.json') == '41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c'
assert sha('q042_production_source_lock_v1.json') == '0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56'

p = pathlib.Path('q042_runtime/q042_external_runtime_provenance_prod_v1.json')
d = json.loads(p.read_text())
assert d.get('q') == 'Q-042'
assert d.get('program_id') == 'Q042-PROD-V1'
assert d.get('status') == 'PASS'
assert d.get('cobaya_version') == '3.5.6'
assert d.get('pybobyqa_version') == '1.5.0'
assert d.get('polychord_commit') == '3ade6445bb3719a6db6f6e81f178765545ffc833'
assert d.get('pantheonplus_manifest_sha256') and d.get('pantheonplus_runtime_files')
print('Q042_PROD_V8_RECOVERED_RUNTIME_GATE=PASS')
PY
