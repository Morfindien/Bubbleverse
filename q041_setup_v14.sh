#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

# V14 does not alter the already validated V13 frozen environment construction.
bash "$ROOT/q041_setup_v13.sh"

python - <<'PY'
import json, pathlib
src=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v13.json")
dst=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v14.json")
d=json.loads(src.read_text(encoding="utf-8"))
assert d.get("q")=="Q-041" and d.get("status")=="PASS" and d.get("cobaya_upgraded") is False
d["program_id"]="Q041-PLANCKPORT-V14"
d["technical_parent_program_id"]="Q041-PLANCKPORT-V13"
d["segmented_resume_execution_only"]=True
dst.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q041_V14_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS")
PY
