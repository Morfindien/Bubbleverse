#!/usr/bin/env bash
set -euo pipefail
export CURRENT_Q=Q019

test -f q017_setup_v3.sh
test -f q016_objective_reprofile_v16.py
test -f q016_v16_endpoint_lock_mechanism_v4.json
test -f q014_external_viability_v12.py
test -f q019_planck_cosmology_reprofile_v1.py
test -f q019_planck_cosmology_reprofile_v1_config.yml
test -f q019_tests_v1.py
test -f q019_source_lock_v1.json

# Reuse the known-good Q017 full-MF environment bootstrap.
bash q017_setup_v3.sh
export CURRENT_Q=Q019

mkdir -p q019_source_runtime
python - <<'PY'
import json, subprocess, importlib.metadata as md
from pathlib import Path
d={
  "q":"Q019",
  "run_id":"Q019-PLANCK-COSMOLOGY-REPROFILE-V1",
  "result_id":"R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-001",
  "environment_bootstrap_reused":"q017_setup_v3.sh",
  "q016_lite_builder_reused":"q016_objective_reprofile_v16.py",
  "q017_full_mf_builder_lineage":"q014_external_viability_v12.py / q017_planck_direction_localization_v1.py",
  "class_ede_commit":subprocess.check_output(
      ["git","-C","external/class_ede","rev-parse","HEAD"],text=True).strip(),
  "cobaya_version":md.version("cobaya"),
  "full_planck_component":"planck_NPIPE_highl_CamSpec.TTTEEE",
  "q017_classification_preserved":"INDETERMINATE",
  "q018_classification_preserved":"COUPLED COMPONENTS / LIKELIHOOD-ARCHITECTURE DEPENDENCE"
}
Path("q019_source_runtime/setup.json").write_text(
    json.dumps(d,indent=2,sort_keys=True)+"\n")
print("Q019_RUNTIME_PROVENANCE_GATE=PASS")
PY

python -m py_compile q019_planck_cosmology_reprofile_v1.py q019_tests_v1.py
python - <<'PY'
import json,yaml
c=yaml.safe_load(open("q019_planck_cosmology_reprofile_v1_config.yml"))
s=json.load(open("q019_source_lock_v1.json"))
assert c["project"]["q"]=="Q019"
assert s["q"]=="Q019"
assert c["model"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
print("Q019_STATIC_ENV_GATE=PASS")
PY
