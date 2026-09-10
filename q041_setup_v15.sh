#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

# V15 changes outcome semantics only. Reuse the validated V14/V13 environment.
bash "$ROOT/q041_setup_v14.sh"

python - <<'PYSETUP'
import json, pathlib
src=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v14.json")
dst=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v15.json")
d=json.loads(src.read_text(encoding="utf-8"))
assert d.get("q")=="Q-041" and d.get("status")=="PASS" and d.get("cobaya_upgraded") is False
d["program_id"]="Q041-PLANCKPORT-V15"
d["technical_parent_program_id"]="Q041-PLANCKPORT-V14"
d["outcome_semantics_only"]=True
d["controlled_no_science_is_green_final"]=True
d["technical_failure_remains_red"]=True
dst.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q041_V15_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS")
PYSETUP
