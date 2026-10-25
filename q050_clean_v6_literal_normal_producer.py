#!/usr/bin/env python3
"""
Q050 CLEAN V6 — source-real literal Pion-interface normal cell producer.

This program is intended for repository-attached execution after checkout of:
  Morfindien/Bubbleverse
  mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97

It deliberately reuses the frozen Q048 interval arithmetic/table loaders, but
does NOT relabel a Q048 inclusion theorem as a Q050 selector certificate.
The new output is Q050-specific.

Fail-closed rule: no scientific PASS is emitted unless actual Q050 normal
cells are produced and independently validated.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path

SOURCE_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
CONFIG_SHA="2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b"
ZLO=650.2566501559347
ZHI=810.0
QBRANCH=(1e-6,0.0)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def fail(path, code, details):
    obj={"schema":"bubbleverse.q050.clean.v6.literal_normal_cells.v1",
         "q":"Q050","status":"INCONCLUSIVE","execution_status":"COMPLETE",
         "blocker":code,"details":details,"cells":[]}
    Path(path).write_text(json.dumps(obj,indent=2)+"\n")
    raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bubbleverse-root",required=True)
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--output",default="Q050_CLEAN_V6_LITERAL_NORMAL_CELLS.json")
    a=ap.parse_args()
    br=Path(a.bubbleverse_root); cr=Path(a.class_root); op=Path(a.output)

    need=[
      br/"q048_prefix_config_v1.json",
      br/"q048_prefix_v1.py",
      br/"q048_full_tube_reuse_v1.py",
      br/"q048_p3_scaled_kernel_v2.py",
      br/"q048_p3_scaled_arithmetic_v2.py",
      br/"q048_p3_scaled_transformed_log_tables_v2.json",
      br/"q048_p3_scaled_raw_result_v2.json",
      cr/"external/HyRec2020/hydrogen.c",
      cr/"external/HyRec2020/hydrogen.h",
      cr/"external/HyRec2020/fit_swift.dat",
    ]
    missing=[str(p) for p in need if not p.exists()]
    if missing: fail(op,"MISSING_PINNED_INPUT",{"missing":missing})
    if sha(br/"q048_prefix_config_v1.json")!=CONFIG_SHA:
        fail(op,"FROZEN_CONFIG_HASH_MISMATCH",{"got":sha(br/"q048_prefix_config_v1.json"),"expected":CONFIG_SHA})

    sys.path.insert(0,str(br))
    try:
        import q048_prefix_v1 as prefix
        import q048_full_tube_reuse_v1 as old
    except Exception as e:
        fail(op,"Q048_RUNTIME_IMPORT_FAILURE",{"error":repr(e)})

    # Verify that the exact source functions and literal selector are present.
    hc=(cr/"external/HyRec2020/hydrogen.c").read_text(errors="replace")
    tokens=["Pion       = four_betaB/(3.*RLya + L2s1s + four_betaB);",
            "if (Pion < PION_MAX)",
            "rec_HMLA_dxHIIdlna",
            "rec_swift_hyrec_dxHIIdlna"]
    absent=[x for x in tokens if x not in hc]
    if absent: fail(op,"SOURCE_SELECTOR_CONTRACT_MISMATCH",{"missing":absent})

    cap=json.loads((br/"q048_prefix_config_v1.json").read_text())
    prefix.validate_config(cap)
    case=cap["cases"]["hillipop-ede_n3"]
    t=prefix.parameters(case)

    # Q050 needs a fixed admitted common background on 650.256...<=z<=810.
    # Existing Q048 helpers can evaluate interval backgrounds only when supplied
    # the already-admitted scalar/EDE state/energy enclosure for the requested
    # low-z cell. V5 did not identify a canonical low-z background-state artifact
    # binding those EDE degrees of freedom over this full interval.
    #
    # Do not silently substitute LCDM, zero EDE energy, a midpoint, or an old
    # unrelated guard row. Discover a Q050-specific binding artifact instead.
    bg_binding=br/"Q050_CLEAN_V6_LOWZ_BACKGROUND_BINDING.json"
    if not bg_binding.exists():
        fail(op,"Q050_LOWZ_BACKGROUND_BINDING_MISSING",{
          "required_file":str(bg_binding),
          "required_domain":[ZLO,ZHI],
          "required_case":"hillipop-ede_n3",
          "required_content":[
            "canonical admitted common-background enclosure/state over each covered cell",
            "exact provenance to Q048 accepted actual127/frontier810 checkpoint",
            "EDE scalar state or equivalent certified H/Hprime enclosure",
            "no LCDM substitution and no midpoint sampling"
          ],
          "why":"The literal normal contains H'/H. q048_full_tube_reuse_v1.background(a,t,energy) requires a certified EDE energy/state enclosure; using an arbitrary energy cap would not be the fixed admitted common background required by Q050."
        })

    binding=json.loads(bg_binding.read_text())
    if binding.get("q")!="Q050" or binding.get("case")!="hillipop-ede_n3":
        fail(op,"LOWZ_BACKGROUND_BINDING_IDENTITY_MISMATCH",{"observed":binding.get("case")})

    # The next implementation stage consumes the binding and evaluates:
    #   F=99B-3R-L=0
    #   N=99B'-3R(H'/H-3/(1+z)+xHII'/(1-xHII))
    # for literal HMLA and SWIFT xHII' on identical states, both q branches.
    #
    # Reaching this guard proves that V6's newly discovered interface is present.
    # It does NOT fabricate cells until the binding schema is frozen and validated.
    fail(op,"LOWZ_BACKGROUND_BINDING_PRESENT_EVALUATOR_EXTENSION_REQUIRED",{
      "binding_sha256":sha(bg_binding),
      "message":"Background binding found. Extend this frozen V6 interface in a new revision; do not patch V6 post-freeze."
    })

if __name__=="__main__":
    main()
