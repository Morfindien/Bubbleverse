#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
python - <<'PY'
import importlib, json, pathlib, py_compile
report={"q":"Q015","run_id":"Q015-CMB-ATTRIBUTION-V3","status":"PASS","checks":{}}
try:
    importlib.import_module("yaml")
    report["checks"]["pyyaml"] = True
except Exception as e:
    report["checks"]["pyyaml"] = False; report["error"] = repr(e); report["status"]="FAIL"
try:
    py_compile.compile("q015_cmb_attribution_v3.py", doraise=True)
    report["checks"]["python_compile"] = True
except Exception as e:
    report["checks"]["python_compile"] = False; report["error_compile"] = repr(e); report["status"]="FAIL"
pathlib.Path("q015_setup_report_v3.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
if report["status"] != "PASS":
    raise SystemExit("Q015_V3_STATIC_ENV_GATE=FAIL")
print("Q015_V3_STATIC_ENV_GATE=PASS")
PY
