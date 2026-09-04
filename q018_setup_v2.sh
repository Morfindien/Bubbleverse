#!/usr/bin/env bash
set -euo pipefail
export CURRENT_Q=Q018
test -f q017_setup_v3.sh
test -f q017_planck_direction_localization_v1.py
test -f q016_v16_endpoint_lock_mechanism_v4.json
test -f q014_external_viability_v12.py
# Q017 setup is the frozen known-good full-MF environment.
bash q017_setup_v3.sh
# Q017 setup is reused only as the frozen environment bootstrap.  Write a
# separate Q018 provenance record so execution identity is never inherited.
mkdir -p q018_source_runtime
python - <<'PY'
import json, subprocess, importlib.metadata as md
from pathlib import Path
d={
  "q":"Q018",
  "run_id":"Q018-PLANCK-LIKELIHOOD-BRIDGE-V2",
  "result_id":"R-Q018-EDE-PLANCK-LIKELIHOOD-BRIDGE-002",
  "environment_bootstrap_reused":"q017_setup_v3.sh",
  "class_ede_commit":subprocess.check_output(
      ["git","-C","external/class_ede","rev-parse","HEAD"],text=True).strip(),
  "cobaya_version":md.version("cobaya"),
  "planck_component":"planck_NPIPE_highl_CamSpec.TTTEEE",
  "q016_cosmological_profiles_rerun":False,
  "q017_scientific_result_reopened":False
}
Path("q018_source_runtime/setup.json").write_text(
    json.dumps(d,indent=2,sort_keys=True)+"\\n")
print("Q018_RUNTIME_PROVENANCE_GATE=PASS")
PY
python -m py_compile q018_planck_likelihood_bridge_v2.py q018_tests_v2.py
python - <<'PY'
import yaml,json
yaml.safe_load(open("q018_planck_likelihood_bridge_v2_config.yml"))
json.load(open("q018_source_lock_v1.json"))
print("Q018_STATIC_ENV_GATE=PASS")
PY
