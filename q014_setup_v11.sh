#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
# V11 changes only continuation scheduling and same-run seeding.
# Reuse the already validated V10 environment wrapper exactly.
bash "$ROOT/q014_setup_v10.sh" "$CHAIN"
rm -rf q014_v11_source_runtime
cp -a q014_v10_source_runtime q014_v11_source_runtime
python - <<'PY_INNER'
import json,pathlib
p=pathlib.Path('q014_v11_source_runtime/setup_imports.json')
d=json.loads(p.read_text())
d['q014_v11_execution_repair']='V10 likelihood/objective/environment preserved; V11 adds same-run Phase1->Phase2 fixed-to-free certification only'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY_INNER
echo "Q014_V11_SETUP_REUSE_GATE=PASS chain=$CHAIN"
