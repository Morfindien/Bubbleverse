#!/usr/bin/env bash
set -euo pipefail
export CURRENT_Q=Q019

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p "$COBAYA_PACKAGES_PATH"

test -f q017_setup_v3.sh
test -f q016_setup_v6.sh
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

# ENVIRONMENT-ONLY REPAIR:
# Q019 reused Q016's CamSpec-lite builder, but the original Q019 setup did not
# install the frozen CamSpec-lite dependency. This reproduces Q016's certified
# Planck-lite dependency bootstrap without changing model, likelihood definition,
# priors, bounds, objective semantics, or result gates.
PLANCK_LITE_DIR="$ROOT/external/camspec_npipe-lite"
PLANCK_LITE_COMMIT="e387852d2ae8863735814449c682b089c3059318"

if [[ ! -d "$PLANCK_LITE_DIR/.git" ]]; then
  git clone https://github.com/HTJense/camspec_npipe-lite.git "$PLANCK_LITE_DIR"
fi

git -C "$PLANCK_LITE_DIR" fetch --all --tags
git -C "$PLANCK_LITE_DIR" checkout --detach "$PLANCK_LITE_COMMIT"
test "$(git -C "$PLANCK_LITE_DIR" rev-parse HEAD)" = "$PLANCK_LITE_COMMIT"

python -m pip install --no-deps -e "$PLANCK_LITE_DIR"

for i in 1 2 3 4; do
  echo "[INFO] Q019 cobaya-install camspec_npipe_lite attempt=$i/4"
  if cobaya-install camspec_npipe_lite -p "$COBAYA_PACKAGES_PATH"; then
    break
  fi
  if [[ "$i" = 4 ]]; then
    echo "Q019_PLANCK_LITE_INSTALL_GATE=FAIL" >&2
    exit 2
  fi
  sleep 15
done

PLANCK_LITE_DIR_EXPECTED="$PLANCK_LITE_DIR" python - <<'PY'
import os, pathlib, camspec_npipe_lite
from camspec_npipe_lite import planck_Camspec_NPIPE_lite

p = pathlib.Path(camspec_npipe_lite.__file__).resolve()
e = pathlib.Path(os.environ["PLANCK_LITE_DIR_EXPECTED"]).resolve()
assert str(p).startswith(str(e) + os.sep), (p, e)
print("Q019_PLANCK_LITE_MODULE_GATE=PASS", p)
PY

mkdir -p q019_source_runtime
python - <<'PY'
import json, subprocess, importlib.metadata as md
from pathlib import Path

d = {
  "q": "Q019",
  "run_id": "Q019-PLANCK-COSMOLOGY-REPROFILE-V1",
  "result_id": "R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-001",
  "environment_bootstrap_reused": "q017_setup_v3.sh",
  "q016_lite_builder_reused": "q016_objective_reprofile_v16.py",
  "q016_planck_lite_bootstrap_reused_from": "q016_setup_v6.sh",
  "camspec_npipe_lite_commit": subprocess.check_output(
      ["git", "-C", "external/camspec_npipe-lite", "rev-parse", "HEAD"],
      text=True
  ).strip(),
  "q017_full_mf_builder_lineage":
      "q014_external_viability_v12.py / q017_planck_direction_localization_v1.py",
  "class_ede_commit": subprocess.check_output(
      ["git", "-C", "external/class_ede", "rev-parse", "HEAD"],
      text=True
  ).strip(),
  "cobaya_version": md.version("cobaya"),
  "full_planck_component": "planck_NPIPE_highl_CamSpec.TTTEEE",
  "q017_classification_preserved": "INDETERMINATE",
  "q018_classification_preserved":
      "COUPLED COMPONENTS / LIKELIHOOD-ARCHITECTURE DEPENDENCE"
}

assert d["camspec_npipe_lite_commit"] == \
    "e387852d2ae8863735814449c682b089c3059318"

Path("q019_source_runtime/setup.json").write_text(
    json.dumps(d, indent=2, sort_keys=True) + "\n"
)
print("Q019_RUNTIME_PROVENANCE_GATE=PASS")
PY

python -m py_compile q019_planck_cosmology_reprofile_v1.py q019_tests_v1.py

python - <<'PY'
import json, yaml, importlib.util

c = yaml.safe_load(open("q019_planck_cosmology_reprofile_v1_config.yml"))
s = json.load(open("q019_source_lock_v1.json"))

assert c["project"]["q"] == "Q019"
assert s["q"] == "Q019"
assert c["model"]["backend_commit"] == \
    "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
assert importlib.util.find_spec("camspec_npipe_lite") is not None

print("Q019_STATIC_ENV_GATE=PASS")
PY
