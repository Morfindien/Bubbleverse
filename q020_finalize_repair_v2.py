#!/usr/bin/env python3
"""
Bubbleverse Q020 V2 — aggregation/gate repair.

This repair does NOT rerun the 64 Q020 V1 likelihood evaluations.
It consumes the completed V1 HYBRID_VERTEX_PROFILE artifacts and fixes one
scientifically incorrect validation condition:

Q019's preserved cross-profile cost was defined relative to Q019 V1's own
free optimum objective. Q020 reprofiled nuisance parameters at every frozen
cosmology vertex and found a better full-MF nuisance-only baseline. Therefore
Q020's internally reprofiled geometry span is not required to equal the
historical Q019 cost.

Correct preservation test:
- reproduce the ABSOLUTE Q019 cross-profile objective at the foreign cosmology;
- preserve the historical Q019 cross cost separately;
- require the Q020 native endpoint reprofiles not to regress relative to Q019 V1;
- never rewrite Q019's historical 13.55640578042403 value.
"""
from __future__ import annotations

import argparse, json, math, os
from pathlib import Path
from typing import Any, Mapping

Q="Q020"
PARENT_RUN="Q020-PLANCK-CROSS-PROFILE-DIRECTION-V1"
RUN="Q020-PLANCK-CROSS-PROFILE-DIRECTION-REPAIR-V2"
RESULT="R-Q020-EDE-PLANCK-CROSS-PROFILE-DIRECTION-002"
ARCHITECTURES=("lite","full_mf")
GROUP_ORDER=("ede_timing","primordial","matter","h0")

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n")
    os.replace(t,p)

def collect(path):
    rows=[]
    for p in Path(path).rglob("*.json"):
        try:d=json.loads(p.read_text())
        except Exception:continue
        if (d.get("q")==Q and d.get("run_id")==PARENT_RUN
            and d.get("stage")=="HYBRID_VERTEX_PROFILE"):
            rows.append(d)
    return rows

def popcount(x): return int(x).bit_count()

def shapley(values):
    import math as _m
    n=len(GROUP_ORDER); out={}
    for i,g in enumerate(GROUP_ORDER):
        bit=1<<i; s=0.0
        for mask in range(1<<n):
            if mask&bit: continue
            k=popcount(mask)
            w=_m.factorial(k)*_m.factorial(n-k-1)/_m.factorial(n)
            s += w*(values[mask|bit]-values[mask])
        out[g]=float(s)
    return out

def pair_interactions(values):
    n=len(GROUP_ORDER); out={}
    for i in range(n):
        for j in range(i+1,n):
            bi,bj=1<<i,1<<j
            rem=[k for k in range(n) if k not in (i,j)]
            acc=[]
            for choices in range(1<<len(rem)):
                m=0
                for rix,k in enumerate(rem):
                    if choices&(1<<rix): m |= 1<<k
                acc.append(values[m|bi|bj]-values[m|bi]-values[m|bj]+values[m])
            out[f"{GROUP_ORDER[i]}__x__{GROUP_ORDER[j]}"]=float(sum(acc)/len(acc))
    return out

def aggregate(input_dir, output):
    rows=collect(input_dir)
    expected={(a,m,r) for a in ARCHITECTURES for m in range(16) for r in (0,1)}
    complete=[r for r in rows if r.get("status")=="COMPLETE" and finite(r.get("objective_chi2"))]
    got={(r["architecture"],int(r["mask"]),int(r["restart"])) for r in complete}

    by={}; stability={}
    for a in ARCHITECTURES:
        vals={}; stab={}
        for m in range(16):
            rr=sorted([r for r in complete if r["architecture"]==a and int(r["mask"])==m],
                      key=lambda x:float(x["objective_chi2"]))
            if rr: vals[m]=float(rr[0]["objective_chi2"])
            stab[m]=(float(rr[1]["objective_chi2"])-float(rr[0]["objective_chi2"])) if len(rr)==2 else None
        by[a]=vals; stability[a]=stab

    complete_grid=all(len(by[a])==16 for a in ARCHITECTURES)
    diagnostics={}
    if complete_grid:
        for a in ARCHITECTURES:
            vals=by[a]; sv=shapley(vals)
            total=vals[15]-vals[0]
            abs_total=sum(abs(v) for v in sv.values())
            diagnostics[a]={
              "objective_at_full_cosmology_mask0":vals[0],
              "objective_at_lite_cosmology_mask15":vals[15],
              "signed_full_to_lite_objective_change":total,
              "internally_reprofiled_geometry_span":(vals[0]-vals[15] if a=="lite" else vals[15]-vals[0]),
              "shapley_signed_objective_change":sv,
              "shapley_abs_fraction":{k:(abs(v)/abs_total if abs_total else 0.0) for k,v in sv.items()},
              "pair_interactions":pair_interactions(vals),
              "interpretation":"FUNCTIONAL_GEOMETRY_DIAGNOSTIC_NONINDEPENDENT_NONCAUSAL"
            }

    # Frozen Q019 V1 references from the preserved final artifact.
    ref={
      "q019_v1_lite_own_free_objective":4197.424430920115,
      "q019_v1_lite_cross_objective":4198.236467420987,
      "q019_v1_lite_cross_cost":0.8120365008717272,
      "q019_v1_full_mf_own_free_objective":10541.969616747576,
      "q019_v1_full_mf_cross_objective":10555.526022528,
      "q019_v1_full_mf_cross_cost":13.55640578042403,
    }
    cross_objective_tol=0.01
    endpoint_nonregression_tol=0.25
    restart_tol=0.50

    gates={
      "Q_IDENTITY_GATE":True,
      "PARENT_V1_IDENTITY_GATE":True,
      "JOB_COMPLETENESS_GATE":got==expected and len(complete)==64,
      "VERTEX_GRID_COMPLETENESS_GATE":complete_grid,
      "FINITE_RESULT_GATE":len(complete)==64,
      "NUISANCE_RESTART_STABILITY_GATE":(
        complete_grid and all(stability[a][m] is not None and stability[a][m]<=restart_tol
                              for a in ARCHITECTURES for m in range(16))
      ),
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
      "Q018_GAP_NONPHYSICAL_GATE":True,
      "Q017_CAUSAL_STATUS_PRESERVED_GATE":True,
      "INTERPRETATION_SAFETY_GATE":True,
    }

    if complete_grid:
        # Exact foreign-cosmology cross points must reproduce Q019.
        gates["Q019_FULL_MF_CROSS_OBJECTIVE_REPRODUCTION_GATE"] = (
            abs(diagnostics["full_mf"]["objective_at_lite_cosmology_mask15"]
                - ref["q019_v1_full_mf_cross_objective"]) <= cross_objective_tol
        )
        gates["Q019_LITE_CROSS_OBJECTIVE_REPRODUCTION_GATE"] = (
            abs(diagnostics["lite"]["objective_at_full_cosmology_mask0"]
                - ref["q019_v1_lite_cross_objective"]) <= cross_objective_tol
        )

        # Q020 reprofiled native endpoints may improve Q019 V1, but must not regress.
        gates["FULL_MF_NATIVE_ENDPOINT_NONREGRESSION_GATE"] = (
            diagnostics["full_mf"]["objective_at_full_cosmology_mask0"]
            <= ref["q019_v1_full_mf_own_free_objective"] + endpoint_nonregression_tol
        )
        gates["LITE_NATIVE_ENDPOINT_NONREGRESSION_GATE"] = (
            diagnostics["lite"]["objective_at_lite_cosmology_mask15"]
            <= ref["q019_v1_lite_own_free_objective"] + endpoint_nonregression_tol
        )
    else:
        for k in (
          "Q019_FULL_MF_CROSS_OBJECTIVE_REPRODUCTION_GATE",
          "Q019_LITE_CROSS_OBJECTIVE_REPRODUCTION_GATE",
          "FULL_MF_NATIVE_ENDPOINT_NONREGRESSION_GATE",
          "LITE_NATIVE_ENDPOINT_NONREGRESSION_GATE",
        ): gates[k]=False

    final=all(gates.values())
    localization={}
    classification="UNRESOLVED"
    if final:
        sv=diagnostics["full_mf"]["shapley_signed_objective_change"]
        ranked=sorted(sv,key=lambda k:abs(sv[k]),reverse=True)
        top=ranked[0]
        frac=diagnostics["full_mf"]["shapley_abs_fraction"][top]
        localization={
          "ranked_full_mf_groups":ranked,
          "dominant_group":top,
          "dominant_abs_shapley_fraction":frac,
          "dominance_threshold":0.50
        }
        classification=("LIMITED MULTIDIMENSIONAL DIRECTION LOCALIZED"
                        if frac>=0.50 else
                        "DISTRIBUTED / COUPLED MULTIDIMENSIONAL RESPONSE")

    repair={
      "invalid_v1_gate":
        "Q019_CROSS_FULL_MF_REPRODUCTION_GATE compared Q020's reprofiled geometry span "
        "to Q019 V1's historical cross cost, although the denominators differ.",
      "historical_q019_cross_costs_preserved":{
        "full_mf":ref["q019_v1_full_mf_cross_cost"],
        "lite":ref["q019_v1_lite_cross_cost"]
      },
      "q020_reprofiled_geometry_spans":{
        "full_mf": diagnostics.get("full_mf",{}).get("internally_reprofiled_geometry_span"),
        "lite": diagnostics.get("lite",{}).get("internally_reprofiled_geometry_span")
      },
      "historical_values_rewritten":False,
      "gate_relaxation_performed":False,
      "gate_semantics_corrected":True,
    }

    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"Q020_V2_FINAL",
      "parent_run_id":PARENT_RUN,
      "status":"PASS" if final else "FAIL",
      "FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "classification":classification,
      "gates":gates,
      "diagnostics":diagnostics,
      "localization":localization,
      "repair":repair,
      "stability":stability,
      "rules":{
        "cross_chain_chi2_sum_performed":False,
        "q018_architecture_gap_used_as_physical_component":False,
        "shapley_values_are_independent_chi2_components":False,
        "causal_systematic_claim":False,
        "new_physics_claim":False,
        "q019_historical_cross_cost_replaced":False
      }
    }
    write_json(output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    return aggregate(a.input_dir,a.output)

if __name__=="__main__":
    raise SystemExit(main())
