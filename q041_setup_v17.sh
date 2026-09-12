#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"

# V17 changes checkpoint serialization/resume only; reuse the validated V16 environment.
bash "$ROOT/q041_setup_v16.sh"

python - <<'PYSETUP'
import json, pathlib
src=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v16.json")
dst=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v17.json")
d=json.loads(src.read_text(encoding="utf-8"))
assert d.get("q")=="Q-041" and d.get("status")=="PASS" and d.get("cobaya_upgraded") is False
d["program_id"]="Q041-PLANCKPORT-V17"
d["technical_parent_program_id"]="Q041-PLANCKPORT-V16"
d["locked_v16_checkpoint_migration_only"]=True
d["locked_v16_parent_series_id"]="34498890334"
d["hillipop_resume_component_source"]="chain.updated.yaml"
d["cobaya_allow_changes_used"]=False
d["per_chain_compute_segment_budget_preserved"]=True
dst.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q041_V17_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS")
PYSETUP
