#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
# V8 keeps the successful V6 environment/MUSE transport unchanged.
bash "$ROOT/q014_setup_v6.sh" "$CHAIN"
rm -rf q014_v8_source_runtime
cp -a q014_v6_source_runtime q014_v8_source_runtime
python - <<'PY_INNER'
import json,pathlib
p=pathlib.Path('q014_v8_source_runtime/setup_imports.json')
d=json.loads(p.read_text())
d['q014_v8_execution_repair']='V7 normalization-free continuation preserved; V8 restores missing versioned setup delivery and hardens precompute gates'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY_INNER
echo "Q014_V8_SETUP_REUSE_GATE=PASS chain=$CHAIN"
