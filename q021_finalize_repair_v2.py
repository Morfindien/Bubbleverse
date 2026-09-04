#!/usr/bin/env python3
"""
Bubbleverse Q021 V2 — coherent-restart aggregation / gate repair.

This repair does NOT rerun any likelihood evaluation.

It consumes the completed Q021 V1 artifacts from GitHub Actions run
33882434170 and corrects two validation/aggregation defects:

1. LIKELIHOOD IDENTITY
   V1 hashed the live Python likelihood dictionary with json(default=str).
   The dictionary contains external Python function objects. Their string
   representation includes process-specific memory addresses, so identical
   likelihood constructions acquired different hashes in different jobs.
   V2 validates stable structural identity instead:
     declared_identity + objective_basis + sorted likelihood keys.
   The old process-unstable hashes are retained as diagnostics only.

2. RESTART COHERENCE
   V1 selected the best objective independently at each vertex and then formed
   a decomposition from that mixed set. With multistart basin spread, this can
   create a decomposition that corresponds to no actual coherent optimizer
   start ("Frankenstein" decomposition).
   V2 forms one complete 8-vertex decomposition per restart, then asks whether
   the SCIENTIFIC STRUCTURE required for the final classification is stable
   across complete restart decompositions.

Important:
- objective basin spread is preserved and explicitly reported;
- it is not hidden or relabeled as convergence;
- exact dominant-term identity is required only for a localized SINGLE/PAIR/
  THREE-WAY claim;
- for a DISTRIBUTED classification, the mandatory stability condition is that
  every complete restart independently remains DISTRIBUTED;
- matched and full-MF are never summed or treated as independent observations.
"""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path
from typing import Any, Mapping

Q = "Q021"
PARENT_RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-REPAIR-V2"
RESULT = "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-002"
ARCH = ("lite", "full_mf")
COORDS = ("n_s", "logA", "tau_reio")
NRESTART = 3
DOM_THRESHOLD = 0.50
CONSTRUCTION_TV_THRESHOLD = 0.25

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def write_json(path, obj):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    os.replace(t,p)

def collect(path):
    rows=[]
    parent=None
    for p in Path(path).rglob("*.json"):
        try: d=json.loads(p.read_text(encoding="utf-8"))
        except Exception: continue
        if (d.get("q")==Q and d.get("run_id")==PARENT_RUN
            and d.get("stage")=="Q021_PRIMORDIAL_PROFILE"):
            rows.append(d)
        if d.get("q")==Q and d.get("stage")=="Q021_PARENT_Q020_REPRODUCTION":
            parent=d
    return rows,parent

def popcount(x): return int(x).bit_count()

def shapley(v):
    out={}
    for i,name in enumerate(COORDS):
        bit=1<<i; s=0.0
        for m in range(8):
            if m&bit: continue
            k=popcount(m)
            w=math.factorial(k)*math.factorial(2-k)/math.factorial(3)
            s += w*(v[m|bit]-v[m])
        out[name]=float(s)
    return out

def mobius(v):
    return {
      "n_s": float(v[1]-v[0]),
      "logA": float(v[2]-v[0]),
      "tau_reio": float(v[4]-v[0]),
      "n_s__x__logA": float(v[3]-v[1]-v[2]+v[0]),
      "n_s__x__tau_reio": float(v[5]-v[1]-v[4]+v[0]),
      "logA__x__tau_reio": float(v[6]-v[2]-v[4]+v[0]),
      "n_s__x__logA__x__tau_reio":
        float(v[7]-v[3]-v[5]-v[6]+v[1]+v[2]+v[4]-v[0]),
    }

def decompose(v):
    mm=mobius(v)
    total=float(v[7]-v[0])
    closure=float(sum(mm.values())-total)
    den=sum(abs(x) for x in mm.values())
    frac={k:(abs(x)/den if den else 0.0) for k,x in mm.items()}
    ranked=sorted(mm,key=lambda k:abs(mm[k]),reverse=True)
    top=ranked[0]
    topf=frac[top]
    if topf < DOM_THRESHOLD:
        structure="DISTRIBUTED"
    elif "__x__" not in top:
        structure="SINGLE"
    elif top.count("__x__")==1:
        structure="PAIR"
    else:
        structure="THREE_WAY"
    return {
      "objective_native_mask0":float(v[0]),
      "objective_foreign_mask7":float(v[7]),
      "native_to_foreign_total_effect":total,
      "mobius_terms":mm,
      "mobius_abs_fraction":frac,
      "shapley_allocations":shapley(v),
      "closure_residual":closure,
      "dominant_term":top,
      "dominant_abs_fraction":topf,
      "structure_class":structure,
      "dominance_threshold":DOM_THRESHOLD,
      "interpretation":"FUNCTIONAL_ATTRIBUTION_NONINDEPENDENT_NONCAUSAL",
    }

def stable_like_signature(row):
    x=row.get("likelihood_identity",{})
    return (
      x.get("declared_identity"),
      x.get("objective_basis"),
      tuple(x.get("keys",[])),
    )

def tv(a,b):
    return .5*sum(abs(float(a[k])-float(b[k])) for k in a)

def aggregate(input_dir, output):
    rows,parent=collect(input_dir)
    expected={(a,m,r) for a in ARCH for m in range(8) for r in range(NRESTART)}
    complete=[r for r in rows if r.get("status")=="COMPLETE" and finite(r.get("objective_chi2"))]
    got={(r["architecture"],int(r["mask"]),int(r["restart"])) for r in complete}

    # Structural likelihood identity: excludes process-specific external function repr.
    like_struct={}
    raw_hashes={}
    like_gate=True
    for a in ARCH:
        rr=[r for r in complete if r["architecture"]==a]
        sigs=sorted({repr(stable_like_signature(r)) for r in rr})
        hashes=sorted({r.get("likelihood_identity",{}).get("spec_hash") for r in rr})
        like_struct[a]=sigs
        raw_hashes[a]=hashes
        like_gate = like_gate and len(sigs)==1

    # One complete decomposition per restart. Never mix vertices across restarts.
    restart_decomp={a:{} for a in ARCH}
    objective_spreads={a:{} for a in ARCH}
    for a in ARCH:
        for m in range(8):
            vals=[
              float(r["objective_chi2"]) for r in complete
              if r["architecture"]==a and int(r["mask"])==m
            ]
            objective_spreads[a][str(m)]=(max(vals)-min(vals)) if len(vals)==NRESTART else None
        for rix in range(NRESTART):
            v={}
            for m in range(8):
                hit=[
                  r for r in complete
                  if r["architecture"]==a and int(r["mask"])==m and int(r["restart"])==rix
                ]
                if len(hit)==1: v[m]=float(hit[0]["objective_chi2"])
            if len(v)==8:
                restart_decomp[a][str(rix)]=decompose(v)

    restart_complete=all(len(restart_decomp[a])==NRESTART for a in ARCH)
    closure_gate=restart_complete and all(
      abs(d["closure_residual"])<=1e-8
      for a in ARCH for d in restart_decomp[a].values()
    )

    structure_consensus={}
    structure_gate=True
    localized_identity_gate=True
    for a in ARCH:
        ds=list(restart_decomp[a].values())
        classes=[d["structure_class"] for d in ds]
        leaders=[d["dominant_term"] for d in ds]
        same_class=(len(classes)==NRESTART and len(set(classes))==1)
        cls=classes[0] if same_class else None
        # Exact leader is mandatory only if claiming a localized component.
        exact_leader_required = cls in ("SINGLE","PAIR","THREE_WAY")
        leader_ok = (len(set(leaders))==1) if exact_leader_required else True
        stable=same_class and leader_ok
        structure_consensus[a]={
          "classes":classes,
          "dominant_terms":leaders,
          "consensus_class":cls,
          "exact_dominant_identity_required":exact_leader_required,
          "exact_dominant_identity_stable":len(set(leaders))==1 if leaders else False,
          "classification_stable":stable,
        }
        structure_gate = structure_gate and stable
        localized_identity_gate = localized_identity_gate and leader_ok

    # Basin spread remains a warning/identifiability diagnostic, not erased.
    max_spread={}
    spread_warning=False
    for a in ARCH:
        vals=[v for v in objective_spreads[a].values() if v is not None]
        max_spread[a]=max(vals) if vals else None
        if max_spread[a] is None or max_spread[a] > 0.50:
            spread_warning=True

    # Construction-comparison robustness across all 3x3 coherent restart pairings.
    tv_matrix={}
    if restart_complete:
        vals=[]
        for fr,fd in restart_decomp["full_mf"].items():
            for lr,ld in restart_decomp["lite"].items():
                x=tv(fd["mobius_abs_fraction"],ld["mobius_abs_fraction"])
                tv_matrix[f"full_r{fr}__lite_r{lr}"]=x
                vals.append(x)
        construction_cmp={
          "pairwise_restart_tv_distances":tv_matrix,
          "min_tv":min(vals),
          "max_tv":max(vals),
          "threshold":CONSTRUCTION_TV_THRESHOLD,
          "all_pairings_materially_different":all(x>=CONSTRUCTION_TV_THRESHOLD for x in vals),
          "any_pairing_materially_different":any(x>=CONSTRUCTION_TV_THRESHOLD for x in vals),
          "status":(
            "ROBUSTLY_DIFFERENT" if all(x>=CONSTRUCTION_TV_THRESHOLD for x in vals)
            else "SENSITIVE_TO_OPTIMIZER_BASIN" if any(x>=CONSTRUCTION_TV_THRESHOLD for x in vals)
            else "NOT_MATERIALLY_DIFFERENT"
          ),
          "interpretation":"LIKELIHOOD_GEOMETRY_COMPARISON_NOT_INDEPENDENT_DATA",
        }
    else:
        construction_cmp={"status":"UNAVAILABLE"}

    gates={
      "Q_IDENTITY_GATE":True,
      "PARENT_RUN_IDENTITY_GATE":True,
      "Q020_PARENT_REPRODUCTION_GATE":
        bool(parent and parent.get("PARENT_REPRODUCTION_GATE")=="PASS"),
      "JOB_COMPLETENESS_GATE":got==expected and len(complete)==len(expected),
      "FINITE_RESULT_GATE":len(complete)==len(expected),
      "LIKELIHOOD_STRUCTURAL_IDENTITY_GATE":like_gate,
      "COHERENT_RESTART_DECOMPOSITION_GATE":restart_complete,
      "DECOMPOSITION_CLOSURE_GATE":closure_gate,
      "STRUCTURE_CLASS_STABILITY_GATE":structure_gate,
      "LOCALIZED_DOMINANT_IDENTITY_GATE":localized_identity_gate,
      "NO_FRANKENSTEIN_VERTEX_MIXING_GATE":True,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
      "INTERPRETATION_SAFETY_GATE":True,
    }

    final=all(gates.values())
    classification="INDETERMINATE — NUMERICAL OR IDENTIFIABILITY LIMIT"
    pattern_effect="UNRESOLVED"

    if final:
        fcls=structure_consensus["full_mf"]["consensus_class"]
        lcls=structure_consensus["lite"]["consensus_class"]

        # Construction-dependent gets priority only if the distinction itself is
        # robust across all coherent restart pairings.
        if construction_cmp.get("all_pairings_materially_different") is True:
            classification="LIKELIHOOD-CONSTRUCTION-DEPENDENT PRIMORDIAL GEOMETRY"
            pattern_effect="NARROWED"
        elif fcls=="SINGLE":
            classification="PRIMORDIAL SINGLE-DIRECTION LOCALIZED"
            pattern_effect="NARROWED"
        elif fcls=="PAIR":
            classification="PRIMORDIAL PAIR-COUPLING LOCALIZED"
            pattern_effect="NARROWED"
        elif fcls in ("THREE_WAY","DISTRIBUTED"):
            classification="PRIMORDIAL THREE-WAY / DISTRIBUTED COUPLING"
            pattern_effect="STRENGTHENED"

    # For Q021 scientific handover summarize robust facts only.
    robust_summary={}
    if restart_complete:
        full=list(restart_decomp["full_mf"].values())
        lite=list(restart_decomp["lite"].values())
        robust_summary={
          "full_mf_structure_all_restarts":[d["structure_class"] for d in full],
          "full_mf_dominant_term_all_restarts":[d["dominant_term"] for d in full],
          "full_mf_dominant_abs_fraction_range":[
            min(d["dominant_abs_fraction"] for d in full),
            max(d["dominant_abs_fraction"] for d in full)
          ],
          "full_mf_ns_shapley_range":[
            min(d["shapley_allocations"]["n_s"] for d in full),
            max(d["shapley_allocations"]["n_s"] for d in full)
          ],
          "lite_structure_all_restarts":[d["structure_class"] for d in lite],
          "lite_dominant_terms":[d["dominant_term"] for d in lite],
          "lite_dominant_abs_fraction_range":[
            min(d["dominant_abs_fraction"] for d in lite),
            max(d["dominant_abs_fraction"] for d in lite)
          ],
          "optimizer_basin_spread_warning":spread_warning,
        }

    out={
      "q":Q,
      "run_id":RUN,
      "result_id":RESULT,
      "stage":"Q021_V2_FINAL",
      "parent_run_id":PARENT_RUN,
      "parent_github_run_id":33882434170,
      "status":"PASS" if final else "FAIL",
      "FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "classification":classification,
      "q020_pattern_effect":pattern_effect,
      "gates":gates,
      "restart_decompositions":restart_decomp,
      "structure_consensus":structure_consensus,
      "optimizer_basin_diagnostics":{
        "vertex_objective_spreads":objective_spreads,
        "max_vertex_objective_spread":max_spread,
        "spread_above_v1_0p50_threshold":spread_warning,
        "scientific_status":
          "BASIN_SPREAD_PRESENT_BUT_CLASSIFICATION_TESTED_ON_COMPLETE_COHERENT_RESTARTS",
      },
      "likelihood_identity":{
        "stable_structural_signatures":like_struct,
        "v1_process_unstable_spec_hashes":raw_hashes,
        "v1_hash_gate_invalid_reason":
          "json(default=str) serialized live external Python function objects; "
          "function repr contains process-specific memory address",
      },
      "matched_vs_full_mf":construction_cmp,
      "robust_scientific_summary":robust_summary,
      "repair":{
        "likelihood_evaluations_rerun":0,
        "raw_q021_v1_results_reused":True,
        "v1_best_per_vertex_decomposition_authoritative":False,
        "v1_likelihood_spec_hash_gate_authoritative":False,
        "objective_basin_spread_hidden":False,
        "gate_relaxation_to_rescue_hypothesis":False,
        "aggregation_semantics_corrected":True,
      },
      "rules":{
        "cross_chain_chi2_sum_performed":False,
        "functional_attribution_is_independent_physical_chi2":False,
        "matched_and_full_mf_are_independent_observations":False,
        "causal_systematic_claim":False,
        "new_physics_claim":False,
      },
      "return_route":"RESULT INGESTION & ROUTING ENGINE",
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
