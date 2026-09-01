#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
# V10 changes only wrapper compatibility; reuse the V8 environment transport exactly.
bash "$ROOT/q014_setup_v8.sh" "$CHAIN"
rm -rf q014_v10_source_runtime
cp -a q014_v8_source_runtime q014_v10_source_runtime
python - <<'PY_INNER'
import json,pathlib
p=pathlib.Path('q014_v10_source_runtime/setup_imports.json')
d=json.loads(p.read_text())
d['q014_v10_execution_repair']='V8 normalization-free science surface and V10 basin-replication design preserved; V10 repairs inherited V5 legacy start-family delegation for smoke/preflight compatibility'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY_INNER
echo "Q014_V10_SETUP_REUSE_GATE=PASS chain=$CHAIN"
