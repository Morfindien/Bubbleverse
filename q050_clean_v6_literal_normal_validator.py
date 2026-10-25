#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("result"); a=ap.parse_args()
x=json.loads(Path(a.result).read_text())
required={"schema","q","status","execution_status","blocker","cells"}
missing=sorted(required-set(x))
if missing: raise SystemExit("SCHEMA_MISSING:"+",".join(missing))
if x["q"]!="Q050": raise SystemExit("Q_IDENTITY")
if not isinstance(x["cells"],list): raise SystemExit("CELLS_TYPE")
allowed={"Q050_LOWZ_BACKGROUND_BINDING_MISSING",
         "LOWZ_BACKGROUND_BINDING_PRESENT_EVALUATOR_EXTENSION_REQUIRED",
         "MISSING_PINNED_INPUT","FROZEN_CONFIG_HASH_MISMATCH",
         "Q048_RUNTIME_IMPORT_FAILURE","SOURCE_SELECTOR_CONTRACT_MISMATCH",
         "LOWZ_BACKGROUND_BINDING_IDENTITY_MISMATCH"}
if x["blocker"] not in allowed: raise SystemExit("UNEXPECTED_BLOCKER:"+str(x["blocker"]))
print(json.dumps({"status":"PASS","validated_blocker":x["blocker"],"cells":len(x["cells"])},indent=2))
