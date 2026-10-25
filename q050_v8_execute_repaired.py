#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math,os,re,subprocess,sys
from pathlib import Path

BV=Path(os.environ["BUBBLEVERSE_ROOT"])
CE=Path(os.environ["CLASS_EDE_ROOT"])
OUT=Path(os.environ["RESULT_DIR"])
OUT.mkdir(parents=True,exist_ok=True)
RESULT=OUT/"Q050_V8_PION_NORMAL_CERTIFICATE_EXECUTION_RESULT.json"

CFG_SHA="2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b"
SRC_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
ZFIT=650.2566501559347
ZMAX=810.0

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def finish(**kw):
    d={
      "schema":"bubbleverse.q050.v8.execution_result.v2",
      "q":"Q050","revision":"V8",
      "execution_status":"COMPLETE",
      "result_validation_status":"UNRESOLVED",
      "scientific_outcome":"INCONCLUSIVE",
      "actual_computed_result":"NO_CERTIFICATE",
      "domain_z":[ZFIT,ZMAX],
      "q_branches":[1e-6,0.0],
      "next_engine":"BUBBLEVERSE.MATHEMATICS 2.3.0"
    }
    d.update(kw)
    RESULT.write_text(json.dumps(d,indent=2)+"\n")
    print(json.dumps(d,indent=2))
    return 0

cfg=BV/"q048_prefix_config_v1.json"
hc=CE/"external/HyRec2020/hydrogen.c"
hh=CE/"external/HyRec2020/hydrogen.h"
fit=CE/"external/HyRec2020/fit_swift.dat"
wrap=CE/"external/HyRec2020/wrap_hyrec.c"
for p in (cfg,hc,hh,fit,wrap):
    if not p.exists():
        sys.exit(finish(blocker="MISSING_PINNED_INPUT",details={"path":str(p)}))

if sha(cfg)!=CFG_SHA:
    sys.exit(finish(blocker="FROZEN_CONFIG_HASH_MISMATCH",
                    details={"got":sha(cfg),"expected":CFG_SHA}))

commit=subprocess.check_output(["git","-C",str(CE),"rev-parse","HEAD"],text=True).strip()
if commit!=SRC_COMMIT:
    sys.exit(finish(blocker="SOURCE_COMMIT_MISMATCH",
                    details={"got":commit,"expected":SRC_COMMIT}))

txt=hc.read_text()
# Semantic/whitespace-tolerant source contract check.
# Historical V8 used a brittle literal string and falsely rejected the pinned
# source because hydrogen.c aligns `Pion       = ...` with extra whitespace.
contract_patterns = {
    "low_z_gate": r"if\s*\(\s*z\s*<\s*900\.\s*\)",
    "pion_formula": r"Pion\s*=\s*four_betaB\s*/\s*\(\s*3\.\s*\*\s*RLya\s*\+\s*L2s1s\s*\+\s*four_betaB\s*\)\s*;",
    "pion_threshold": r"if\s*\(\s*Pion\s*<\s*PION_MAX\s*\)",
    "hmla_call": r"rec_HMLA_dxHIIdlna\s*\(",
    "swift_call": r"rec_swift_hyrec_dxHIIdlna\s*\("
}
missing=[name for name,pat in contract_patterns.items()
         if re.search(pat,txt,re.MULTILINE) is None]
if missing:
    sys.exit(finish(blocker="SOURCE_SELECTOR_CONTRACT_MISMATCH",
                    details={"missing_semantic_contract_items":missing}))

first=None
for line in fit.read_text().splitlines():
    s=line.strip()
    if not s or s.startswith("#"): continue
    try: first=float(s.split()[0]); break
    except: pass
if first!=1775.0:
    sys.exit(finish(blocker="SWIFT_GATE_MISMATCH",details={"first_temperature_K":first}))

# V8 must not silently substitute a new cosmology.  The repo already contains the
# Q048 source-real machinery.  Require the V8 numerical producer to be present;
# if it is present, execute it.  This permits the Action package to remain stable
# while the scientific evaluator is versioned and reviewed independently.
engine=BV/"q050_v8_literal_normal_evaluator.py"
if not engine.exists():
    # Produce a useful, source-bound answer rather than a broken/missing artifact.
    sys.exit(finish(
      blocker="V8_LITERAL_NORMAL_EVALUATOR_NOT_INSTALLED",
      actual_computed_result="SOURCE_AND_BACKEND_PREFLIGHT_PASS_EVALUATOR_ABSENT",
      provenance={
        "config_sha256":sha(cfg),
        "hydrogen_c_sha256":sha(hc),
        "hydrogen_h_sha256":sha(hh),
        "fit_swift_sha256":sha(fit),
        "source_commit":commit
      },
      details={
        "cleared":["pinned checkout","config identity","selector source contract","SWIFT first-knot gate"],
        "required_next_file":"q050_v8_literal_normal_evaluator.py",
        "warning":"No normal signs were fabricated."
      }))

cp=subprocess.run([sys.executable,str(engine),
                   "--bubbleverse-root",str(BV),
                   "--class-ede-root",str(CE),
                   "--output",str(RESULT)],text=True)
if not RESULT.exists():
    sys.exit(finish(blocker="EVALUATOR_RETURNED_WITHOUT_RESULT",
                    details={"returncode":cp.returncode}))
sys.exit(0 if cp.returncode==0 else cp.returncode)
