#!/usr/bin/env python3
"""Mandatory result gates for Bubbleverse Q019 V1."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml

Q="Q019"
RUN="Q019-PLANCK-COSMOLOGY-REPROFILE-V1"
RESULT="R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-001"
ARCH=("lite","full_mf")
MODES=("reference_free_h0","fixed_h0_71p5")

def finite(x):
    try:return math.isfinite(float(x))
    except Exception:return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    ap.add_argument("--merged",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    c=yaml.safe_load(Path(a.config).read_text())
    d=json.loads(Path(a.merged).read_text())

    g={}
    g["Q_IDENTITY_GATE"]=(d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT)
    g["CONTEXT_CONTINUITY_GATE"]=(
        c["parents"]["q017"]["classification"]=="INDETERMINATE"
        and c["parents"]["q018"]["classification"]=="COUPLED COMPONENTS / LIKELIHOOD-ARCHITECTURE DEPENDENCE"
        and c["rules"]["q018_architecture_gap_not_physical_chi2_component"] is True
        and c["rules"]["no_cross_chain_chi2_sum"] is True
    )
    p=d.get("primary",{})
    jm=p.get("job_manifest",{})
    expected=2*2*int(c["execution"]["restart_patterns"])
    g["JOB_COMPLETENESS_GATE"]=(jm.get("expected")==expected and jm.get("returned")==expected)

    stab=p.get("stability",{})
    g["MULTISTART_STABILITY_GATE"]=all(
        stab.get(f"{x}:{m}",{}).get("pass") is True for x in ARCH for m in MODES
    )

    best=p.get("best",{})
    lf=best.get("lite:reference_free_h0",{})
    lx=best.get("lite:fixed_h0_71p5",{})
    ff=best.get("full_mf:reference_free_h0",{})
    fx=best.get("full_mf:fixed_h0_71p5",{})
    g["FINITE_RESULT_GATE"]=all(
        finite(x.get("objective_chi2")) for x in (lf,lx,ff,fx)
    )

    # Shared cosmological hard-support/prior specification must match between
    # architectures in each corresponding mode.
    g["PRIOR_SUPPORT_COMPATIBILITY_GATE"]=(
        lf.get("cosmology_prior_support_signature")==ff.get("cosmology_prior_support_signature")
        and lx.get("cosmology_prior_support_signature")==fx.get("cosmology_prior_support_signature")
    )

    g["OBJECTIVE_SEMANTICS_GATE"]=all(
        x.get("objective_basis")==c["objective"]["basis"] for x in (lf,lx,ff,fx)
    )

    h0=lf.get("cosmology",{}).get("H0")
    g["Q016_FREE_REFERENCE_GATE"]=(
        finite(h0)
        and abs(float(h0)-float(c["references"]["q016_free_h0"]))
            <= float(c["validation"]["q016_free_h0_abs_tolerance"])
    )
    pen=p.get("reprofiled_high_h0_penalties",{}).get("lite")
    g["Q016_LITE_PENALTY_REFERENCE_GATE"]=(
        finite(pen)
        and abs(float(pen)-float(c["references"]["q016_lite_penalty"]))
            <= float(c["validation"]["q016_lite_penalty_abs_tolerance"])
    )

    costs=d.get("cross_objective_costs",{})
    g["CROSS_PROFILE_COMPLETENESS_GATE"]=set(costs)==set(ARCH)
    tol=float(c["validation"]["negative_cross_cost_tolerance"])
    g["CROSS_PROFILE_NESTING_GATE"]=(
        g["CROSS_PROFILE_COMPLETENESS_GATE"]
        and all(finite(v) and float(v)>=-tol for v in costs.values())
    )

    g["NO_CROSS_CHAIN_CHI2_SUM_GATE"]=(
        p.get("cross_chain_chi2_sum_performed") is False
        and d.get("interpretation_rules",{}).get("no_cross_chain_chi2_sum") is True
    )
    g["Q018_GAP_NONPHYSICAL_GATE"]=(
        d.get("interpretation_rules",{}).get("q018_gap_used_as_physical_component") is False
    )
    g["SCIENTIFIC_INTERPRETATION_GATE"]=(
        d.get("classification") in {
            "LIKELIHOOD CHOICE SHIFTS PREFERRED MOD-EDE-N3 REGION",
            "LIKELIHOOD DEPENDENCE PRIMARILY HIGH-H0 / LOCAL-GEOMETRY",
            "INDETERMINATE",
        }
        and d.get("interpretation_rules",{}).get("causal_systematic_claim_allowed") is False
        and d.get("interpretation_rules",{}).get("new_physics_claim_allowed") is False
    )

    mandatory=[
        "Q_IDENTITY_GATE","CONTEXT_CONTINUITY_GATE","JOB_COMPLETENESS_GATE",
        "MULTISTART_STABILITY_GATE","FINITE_RESULT_GATE",
        "PRIOR_SUPPORT_COMPATIBILITY_GATE","OBJECTIVE_SEMANTICS_GATE",
        "Q016_FREE_REFERENCE_GATE","Q016_LITE_PENALTY_REFERENCE_GATE",
        "CROSS_PROFILE_COMPLETENESS_GATE","CROSS_PROFILE_NESTING_GATE",
        "NO_CROSS_CHAIN_CHI2_SUM_GATE","Q018_GAP_NONPHYSICAL_GATE",
        "SCIENTIFIC_INTERPRETATION_GATE",
    ]
    final=all(g[k] for k in mandatory)
    out={
        "q":Q,"run_id":RUN,"result_id":RESULT,
        "test_type":"MANDATORY_RESULT_TESTS",
        "gates":g,
        "mandatory":mandatory,
        "FINAL_RESULT_GATE":"PASS" if final else "FAIL",
        "classification":d.get("classification"),
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

if __name__=="__main__":
    raise SystemExit(main())
