#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
CHAIN="${1:-all}"
export Q015_CHAIN="$CHAIN"

# Q015 changes attribution/diagnostics only. Reuse the validated Q014 V12 environment.
bash "$ROOT/q014_setup_v12.sh" "$CHAIN"

python - <<'PY'
import importlib, json, pathlib
mods = ["cobaya", "numpy", "scipy", "yaml", "q014_external_viability_v12"]
report = {"q":"Q015", "status":"PASS", "imports":{}}
for name in mods:
    try:
        m=importlib.import_module(name)
        report["imports"][name]={"pass":True,"file":getattr(m,"__file__",None)}
    except Exception as e:
        report["imports"][name]={"pass":False,"error":repr(e)}
        report["status"]="FAIL"
import os
chain=os.environ["Q015_CHAIN"]
if chain.startswith("spt_") or chain == "all":
    for name in ["candl", "spt_candl_data"]:
        try:
            m=importlib.import_module(name)
            report["imports"][name]={"pass":True,"file":getattr(m,"__file__",None)}
        except Exception as e:
            report["imports"][name]={"pass":False,"error":repr(e)}
            report["status"]="FAIL"
pathlib.Path("q015_setup_report_v1.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
if report["status"] != "PASS":
    raise SystemExit("Q015_ENVIRONMENT_GATE=FAIL")
print("Q015_ENVIRONMENT_GATE=PASS")
PY
