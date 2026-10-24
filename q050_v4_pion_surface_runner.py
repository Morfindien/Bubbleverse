#!/usr/bin/env python3
import hashlib,json,math,os,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=Path(os.environ.get("CLASS_EDE_ROOT", ROOT/"class_ede"))
BV=Path(os.environ.get("BUBBLEVERSE_ROOT", ROOT))
SPEC=json.loads((ROOT/"Q050_V4_PION_SURFACE_EXECUTION_SPEC.json").read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(reason,details=None):
    o={"schema":"bubbleverse.q050.v4.pion_surface_execution.result.v1","q":"Q050",
       "status":"INCONCLUSIVE","execution_status":"COMPLETE","result_validation_status":"UNRESOLVED",
       "scientific_outcome":"INCONCLUSIVE","blocker":reason,"details":details or {},
       "actual_computed_result":"NO_CERTIFICATE"}
    Path("Q050_V4_PION_SURFACE_EXECUTION_RESULT.json").write_text(json.dumps(o,indent=2)+"\n")
    print(json.dumps(o)); sys.exit(2)
hc=SRC/"external/HyRec2020/hydrogen.c"; hh=SRC/"external/HyRec2020/hydrogen.h"; fit=SRC/"external/HyRec2020/fit_swift.dat"
for p,key in [(hc,"hydrogen_c_sha256"),(hh,"hydrogen_h_sha256"),(fit,"fit_swift_sha256")]:
    if not p.exists(): fail("MISSING_PINNED_SOURCE",{"path":str(p)})
    if sha(p)!=SPEC["source"][key]: fail("SOURCE_HASH_MISMATCH",{"path":str(p),"got":sha(p),"expected":SPEC["source"][key]})
text=hc.read_text()
required=["if (z < 900.)","Pion = four_betaB/(3.*RLya + L2s1s + four_betaB);",
          "if (Pion < PION_MAX)","rec_HMLA_dxHIIdlna","rec_swift_hyrec_dxHIIdlna"]
if not all(x in text for x in required): fail("SOURCE_SELECTOR_CONTRACT_MISMATCH")
first=float(fit.read_text().split()[0])
if first!=1775.0: fail("SWIFT_FIT_GATE_MISMATCH",{"first_temperature_K":first})
# The rigorous V3 contract requires interval/outward evaluation of both source-real
# hydrogen fields on the Pion surface. Reuse only if the required proven Q048
# interval machinery is actually present in this checkout.
deps=["q048_p3_scaled_arithmetic_v2.py","q048_p3_scaled_kernel_v2.py",
      "q048_p3_scaled_transformed_log_tables_v2.json","q048_prefix_config_v1.json"]
missing=[x for x in deps if not (BV/x).exists()]
if missing: fail("MISSING_INTERVAL_DEPENDENCIES",{"missing":missing})
# Deliberate fail-closed guard: the current package does not pretend that old Q048
# inclusion bounds are a literal-selector normal certificate. A dedicated evaluator
# must be implemented/verified before a scientific PASS/FAIL can be emitted.
fail("DEDICATED_LITERAL_SELECTOR_NORMAL_EVALUATOR_NOT_YET_IMPLEMENTED",
     {"preflight":"PASS","source_hashes":"PASS","selector_contract":"PASS",
      "reason":"Existing Q048 machinery certifies two-operator inclusion bounds, not the V3 literal-selector one-sided normal derivative. Reusing it as the requested certificate would overclaim."})
