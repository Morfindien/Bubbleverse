#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
# V12 changes only continuation scheduling and the fixed-parent H0 embedding.
# Reuse the already validated V11/V10 environment wrapper exactly.
bash "$ROOT/q014_setup_v11.sh" "$CHAIN"
rm -rf q014_v12_source_runtime
cp -a q014_v11_source_runtime q014_v12_source_runtime
python - <<'PY_INNER'
import json,pathlib
p=pathlib.Path('q014_v12_source_runtime/setup_imports.json')
d=json.loads(p.read_text())
d['q014_v12_execution_repair']='V11 likelihood/objective/environment preserved; V12 fixes unconditional H0=71.5 for fixed-parent embedding and adds same-run fixed replication'
p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
PY_INNER
echo "Q014_V12_SETUP_REUSE_GATE=PASS chain=$CHAIN"
