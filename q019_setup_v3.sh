#!/usr/bin/env bash
set -euo pipefail
export CURRENT_Q=Q019
test -f q019_setup_v1.sh
test -f q019_globality_v2.py
test -f q019_globality_v2_config.yml
test -f q019_tests_v2.py
test -f q019_planck_cosmology_reprofile_v1.py
test -f q016_objective_reprofile_v16.py
test -f q016_matched_cmb_surface_v16_config.yml
test -f q016_v16_endpoint_lock_mechanism_v4.json

# Reuse repaired Q019 V1 environment: class_ede + full-MF + pinned CamSpec-lite.
bash q019_setup_v1.sh
export CURRENT_Q=Q019

python -m py_compile q019_globality_v2.py q019_tests_v2.py
python - <<'PY'
import yaml
c=yaml.safe_load(open("q019_globality_v2_config.yml"))
assert c["project"]["q"]=="Q019"
assert c["rules"]["no_gate_relaxation"] is True
assert c["execution"]["restarts_per_family"]==6
print("Q019_V2_STATIC_ENV_GATE=PASS")
PY
