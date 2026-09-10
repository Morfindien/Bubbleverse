#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

# V16 changes chain-state provenance only. Reuse the validated V15/V14/V13 environment.
bash "$ROOT/q041_setup_v15.sh"

python - <<'PYSETUP'
import json, pathlib
src=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v15.json")
dst=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v16.json")
d=json.loads(src.read_text(encoding="utf-8"))
assert d.get("q")=="Q-041" and d.get("status")=="PASS" and d.get("cobaya_upgraded") is False
d["program_id"]="Q041-PLANCKPORT-V16"
d["technical_parent_program_id"]="Q041-PLANCKPORT-V15"
d["same_series_resume_only"]=True
d["cross_version_chain_state_reuse_forbidden"]=True
d["cobaya_allow_changes_used"]=False
dst.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q041_V16_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS")
PYSETUP
