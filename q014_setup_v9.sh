#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
# V9 changes only numerical continuation. Reuse the V8 environment transport exactly.
bash "$ROOT/q014_setup_v8.sh" "$CHAIN"
rm -rf q014_v9_source_runtime
cp -a q014_v8_source_runtime q014_v9_source_runtime
python - <<'PY_INNER'
import json,pathlib
p=pathlib.Path('q014_v9_source_runtime/setup_imports.json')
d=json.loads(p.read_text())
d['q014_v9_execution_repair']='V8 normalization-free science surface preserved; V9 performs two-basin exact+jitter replication certification'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY_INNER
echo "Q014_V9_SETUP_REUSE_GATE=PASS chain=$CHAIN"
