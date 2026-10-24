#!/usr/bin/env python3
"""
Q050 V8 — literal-selector normal certificate runner.

This is deliberately fail-closed. It verifies the frozen source checkout,
selector contract, active SWIFT gate, and exact Pion surface. It then requires
a source-real background/evaluator hook before any normal sign is certified.
It never fabricates a scientific certificate.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from pathlib import Path

Q="Q050"
ZMIN=650.2566501559347
ZMAX=810.0
PION_MAX=1.0e-2
TCMB=2.7255
SWIFT_T0=1775.0
CLASS_COMMIT="5a131c91d657dd9a7c6364cc45b038710f8d0d97"

def sha256(p: Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def emit(path:Path, **kw):
    base={
      "schema":"bubbleverse.q050.v8.pion_normal_certificate.execution_result.v1",
      "q":Q,
      "execution_status":"COMPLETE",
      "result_validation_status":"UNRESOLVED",
      "scientific_outcome":"INCONCLUSIVE",
      "case_lifecycle":"OPEN",
      "actual_computed_result":"NO_CERTIFICATE"
    }
    base.update(kw)
    path.write_text(json.dumps(base,indent=2)+"\n")
    print(json.dumps(base,indent=2))

def die(out:Path, blocker:str, details):
    emit(out, blocker=blocker, details=details)
    raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--bubbleverse-root",required=True)
    ap.add_argument("--output",default="Q050_V8_PION_NORMAL_CERTIFICATE_EXECUTION_RESULT.json")
    a=ap.parse_args()
    cr=Path(a.class_root); br=Path(a.bubbleverse_root); op=Path(a.output)

    hc=cr/"external/HyRec2020/hydrogen.c"
    hh=cr/"external/HyRec2020/hydrogen.h"
    fs=cr/"external/HyRec2020/fit_swift.dat"
    wh=cr/"external/HyRec2020/wrap_hyrec.c"
    cfg=br/"q048_prefix_config_v1.json"

    missing=[str(p) for p in (hc,hh,fs,wh,cfg) if not p.exists()]
    if missing: die(op,"MISSING_PINNED_INPUT",{"missing":missing})

    hct=hc.read_text(errors="replace")
    hht=hh.read_text(errors="replace")
    wht=wh.read_text(errors="replace")

    required=[
      "if (Pion<PION_MAX)",
      "rec_HMLA_dxHIIdlna",
      "rec_swift_hyrec_dxHIIdlna",
      "fit->swift_func[0][0]"
    ]
    absent=[s for s in required if s not in hct]
    if absent: die(op,"SOURCE_SELECTOR_CONTRACT_MISMATCH",{"missing_source_tokens":absent})

    if not re.search(r"#define\s+PION_MAX\s+1e-2",hht):
        die(op,"PION_MAX_MISMATCH",{})
    if "dx_H_dz" not in wht or "rec_dxHIIdlna" not in wht:
        die(op,"WRAPPER_CONTRACT_MISMATCH",{})

    first=None
    for line in fs.read_text(errors="replace").splitlines():
        s=line.strip()
        if not s or s.startswith("#"): continue
        try:
            first=float(s.split()[0]); break
        except ValueError: continue
    if first is None or abs(first-SWIFT_T0)>1e-12:
        die(op,"SWIFT_FIRST_TEMPERATURE_MISMATCH",{"observed":first,"expected":SWIFT_T0})

    zfit=SWIFT_T0/TCMB-1.0
    if abs(zfit-ZMIN)>1e-12:
        die(op,"ACTIVE_SWIFT_GATE_MISMATCH",{"computed":zfit,"expected":ZMIN})

    cfg_sha=sha256(cfg)
    expected_cfg="2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b"
    if cfg_sha!=expected_cfg:
        die(op,"FROZEN_CONFIG_HASH_MISMATCH",{"observed":cfg_sha,"expected":expected_cfg})

    # The source-real normal requires H(z), H'(z), nH(z), B(z), B'(z),
    # and both branch x'_HII values on the explicit F=0 state.
    # Existing Q048 inclusion code is NOT accepted as a literal-selector certificate.
    #
    # A valid implementation must provide an evaluator artifact with interval cells:
    # z_lo,z_hi, reachable, N_HMLA_lo,N_HMLA_hi,N_SWIFT_lo,N_SWIFT_hi
    candidate=br/"Q050_V8_LITERAL_NORMAL_CELLS.json"
    if not candidate.exists():
        die(op,"LITERAL_NORMAL_EVALUATOR_OUTPUT_MISSING",{
          "required_file":str(candidate),
          "required_domain":[ZMIN,ZMAX],
          "required_fields":[
            "z_lo","z_hi","reachable",
            "N_HMLA_lo","N_HMLA_hi","N_SWIFT_lo","N_SWIFT_hi"
          ],
          "note":"Implement the source-real evaluator against the pinned CLASS/EDE background and HyRec tables. Sampling-only or Q048 convexified inclusion output is not sufficient."
        })

    cells=json.loads(candidate.read_text())
    if not isinstance(cells,list) or not cells:
        die(op,"EMPTY_NORMAL_COVERAGE",{})

    unresolved=[]; incompatible=[]; covered=[]
    for i,c in enumerate(cells):
        try:
            zl=float(c["z_lo"]); zh=float(c["z_hi"])
            reach=bool(c["reachable"])
            h0=float(c["N_HMLA_lo"]); h1=float(c["N_HMLA_hi"])
            s0=float(c["N_SWIFT_lo"]); s1=float(c["N_SWIFT_hi"])
        except Exception as e:
            die(op,"INVALID_CELL_SCHEMA",{"index":i,"error":str(e)})
        covered.append([zl,zh])
        if not reach: continue
        hs = 1 if h0>0 else (-1 if h1<0 else 0)
        ss = 1 if s0>0 else (-1 if s1<0 else 0)
        if hs==0 or ss==0:
            unresolved.append({"index":i,**c})
        elif hs!=ss:
            incompatible.append({"index":i,**c})

    covered.sort()
    cursor=ZMIN
    gaps=[]
    for lo,hi in covered:
        if lo>cursor+1e-12: gaps.append([cursor,lo])
        cursor=max(cursor,hi)
    if cursor<ZMAX-1e-12: gaps.append([cursor,ZMAX])
    if gaps: die(op,"INCOMPLETE_SURFACE_COVERAGE",{"gaps":gaps})

    if unresolved:
        emit(op,
          blocker="AMBIGUOUS_REACHABLE_NORMAL_CELLS",
          details={"count":len(unresolved),"cells":unresolved},
          provenance={"config_sha256":cfg_sha,"hydrogen_c_sha256":sha256(hc),
                      "hydrogen_h_sha256":sha256(hh),"fit_swift_sha256":sha256(fs)})
        return

    if incompatible:
        emit(op,
          result_validation_status="VALIDATED",
          scientific_outcome="NEGATIVE",
          actual_computed_result="CERTIFIED_INCOMPATIBLE_ONE_SIDED_NORMAL_CELL",
          blocker=None,
          details={"count":len(incompatible),"cells":incompatible},
          provenance={"config_sha256":cfg_sha,"hydrogen_c_sha256":sha256(hc),
                      "hydrogen_h_sha256":sha256(hh),"fit_swift_sha256":sha256(fs)})
        return

    emit(op,
      result_validation_status="VALIDATED",
      scientific_outcome="POSITIVE",
      actual_computed_result="CERTIFIED_COMPATIBLE_PION_INTERFACE_NORMALS",
      blocker=None,
      details={"domain":[ZMIN,ZMAX],"reachable_cells":sum(bool(c["reachable"]) for c in cells)},
      provenance={"config_sha256":cfg_sha,"hydrogen_c_sha256":sha256(hc),
                  "hydrogen_h_sha256":sha256(hh),"fit_swift_sha256":sha256(fs)})

if __name__=="__main__":
    main()
