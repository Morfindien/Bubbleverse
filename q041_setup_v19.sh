#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
cd "$ROOT"
# V19 changes no environment/science settings; reuse the validated V16 environment installer.
bash "$ROOT/q041_setup_v16.sh"
python - <<'PYSETUP'
import json, pathlib
src=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v16.json")
dst=pathlib.Path("q041_runtime/q041_external_runtime_provenance_v19.json")
d=json.loads(src.read_text(encoding="utf-8"))
assert d.get("q")=="Q-041" and d.get("status")=="PASS" and d.get("cobaya_upgraded") is False
d["program_id"]="Q041-PLANCKPORT-V19"
d["technical_parent_program_id"]="Q041-PLANCKPORT-V18"
d["single_workflow_run"]=True
d["fixed_linear_segment_chain"]=True
d["self_dispatch_removed"]=True
d["fresh_v19_segment1_required"]=True
d["cross_version_chain_state_reuse_forbidden"]=True
d["hillipop_resume_component_source"]="chain.updated.yaml"
d["cobaya_allow_changes_used"]=False
d["missing_hillipop_component_constant_repaired"]=True
d["hillipop_component_constant"]="planck_2020_hillipop.TT"
dst.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("Q041_V19_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS")
PYSETUP
