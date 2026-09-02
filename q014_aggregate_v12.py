#!/usr/bin/env python3
"""Aggregate Q014 V12 Phase1+Phase2 same-run certification jobs."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml
import q014_external_viability_v12 as eng

ROOT=Path(__file__).resolve().parent
CONFIG_NAME="q014_external_viability_v12_config.yml"
RUN="Q014-EXTERNAL-VIABILITY-V12"
BASIS=eng.BASIS

def load_cfg(p=CONFIG_NAME):
    p=Path(p); p=p if p.is_absolute() else ROOT/p
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def load_records(paths):
    return eng._load_records(paths)

def finite(r):
    return eng._finite_record(r)

def spread(rows):
    xs=sorted(float(r["objective_chi2"]) for r in rows if finite(r))
    return xs[1]-xs[0] if len(xs)>=2 else None

def aggregate(records,c):
    expected=eng.phase_tasks(c,"phase1")+eng.phase_tasks(c,"phase2")
    key=lambda x:(x["chain"],x["mode"],x["start_family"])
    ek={key(x) for x in expected}; rk={key(x) for x in records}
    missing=sorted(ek-rk)
    dupes=sorted(k for k in rk if sum(1 for r in records if key(r)==k)>1)

    source={}
    for chain in c["chains"]:
        hs=sorted({str(r.get("runtime_source_provenance_sha256"))
                   for r in records if r.get("chain")==chain and finite(r)
                   and r.get("runtime_source_provenance_sha256")})
        source[chain]=hs
    source_ok=all(len(v)==1 for v in source.values())

    result={
      "case_id":c["project"]["case_id"],"q":"Q014","run_id":RUN,
      "result_id":c["project"]["result_id"],
      "original_case_question":c["project"]["original_case_question"],
      "program_status":"V12 SAME-RUN CROSS-MODE CERTIFICATION RESULTS AGGREGATED",
      "q011_globality_status_preserved":c["claim_boundary"]["q011_globality_status_preserved"],
      "absolute_chi2_cross_package_comparison_performed":False,
      "planck_spt_chi2_sum_performed":False,
      "objective_basis":c["scientific_surface"]["optimizer_basis"],
      "chains":{},
      "v11_numerical_parent":c["parent"]["v11"],
      "job_manifest":{
        "expected":len(ek),"returned":len(rk),"missing":missing,"duplicates":dupes,
        "phase1_expected":len(eng.phase_tasks(c,"phase1")),
        "phase2_expected":len(eng.phase_tasks(c,"phase2")),
        "runtime_source_provenance_hashes_by_chain":source,
        "runtime_source_compatible":source_ok,
      },
      "validation_status":"PARTIAL","scientifically_usable_result":False,
      "next_action_required":True,
    }

    minv=int(c["validation"]["minimum_valid_starts_per_profile"])
    maxsp=float(c["validation"]["max_best_two_delta_chi2"])
    neg=float(c["validation"]["fixed_vs_free_negative_tolerance"])

    for chain,spec in c["chains"].items():
        cr={"label":spec["label"],"role":spec["role"],
            "paper_native_reproduction":spec.get("paper_native_reproduction",False),
            "profiles":{},"penalties":{},"same_run_embedding":{},"status":"PARTIAL"}

        for mode in c["execution"]["modes"]:
            rows=[r for r in records if r.get("chain")==chain and r.get("mode")==mode]
            good=sorted([r for r in rows if finite(r)],key=lambda r:float(r["objective_chi2"]))
            sp=spread(good)
            needed=1 if mode=="q011_shared_physics" else minv
            stable=len(good)>=needed and (mode=="q011_shared_physics" or (sp is not None and sp<=maxsp))
            seedpass=bool(good) and all(r.get("seed_candidate_preservation_pass") is True for r in good)
            cr["profiles"][mode]={
                "returned_jobs":len(rows),"finite_jobs":len(good),"minimum_required":needed,
                "best_objective_chi2":float(good[0]["objective_chi2"]) if good else None,
                "best_record":good[0] if good else None,
                "best_two_delta_chi2":sp,"stable":stable,
                "seed_candidate_preservation_pass":seedpass,
                "status":"VALIDATED" if stable and seedpass else
                         ("NUMERICALLY_UNRESOLVED" if good else "TECHNICAL_FAILURE"),
            }

        ref=cr["profiles"]["reference_free_h0"]["best_objective_chi2"]
        fix=cr["profiles"]["fixed_h0_71p5"]["best_objective_chi2"]
        sh=cr["profiles"]["q011_shared_physics"]["best_objective_chi2"]

        # Explicitly verify that the exact Phase-1 fixed minimum was embedded
        # into the free-H0 space without changing its physical point. The seed
        # objective must match the Phase-1 source objective (same point, same
        # normalization-free basis) and H0 must be exactly the fixed target.
        embedded=[r for r in records
                  if r.get("chain")==chain and r.get("mode")=="reference_free_h0"
                  and r.get("start_family")=="p1_fixed_best" and finite(r)]
        if embedded:
            er=embedded[0]
            seed=(er.get("seed_candidate") or {})
            seed_obj=seed.get("objective_chi2")
            source_obj=er.get("phase1_source_objective_chi2")
            seed_h0=(seed.get("minimum") or {}).get("H0")
            target=float(c["scientific_surface"]["target_h0"])
            tol=float(c["execution"]["v10_seed_policy"]["seed_objective_tolerance"])
            htol=float(c["validation"]["exact_h0_tolerance"])
            emb_pass=(seed_obj is not None and source_obj is not None and seed_h0 is not None
                      and math.isfinite(float(seed_obj)) and math.isfinite(float(source_obj))
                      and math.isfinite(float(seed_h0))
                      and abs(float(seed_obj)-float(source_obj)) <= tol
                      and abs(float(seed_h0)-target) <= htol
                      and er.get("same_run_fixed_to_free_embedding") is True
                      and er.get("seed_candidate_preservation_pass") is True)
            cr["same_run_embedding"]={
                "phase2_p1_fixed_best_seed_objective":float(seed_obj) if seed_obj is not None else None,
                "phase1_fixed_source_objective":float(source_obj) if source_obj is not None else None,
                "delta_seed_minus_phase1_fixed_source":float(seed_obj)-float(source_obj) if seed_obj is not None and source_obj is not None else None,
                "seed_h0":float(seed_h0) if seed_h0 is not None else None,
                "target_h0":target,
                "final_fixed_best_objective":float(fix) if fix is not None else None,
                "pass":emb_pass,
            }
        else:
            cr["same_run_embedding"]={"pass":False}

        if ref is not None and fix is not None:
            delta=float(fix)-float(ref)
            cr["penalties"]["fixed_h0_profile_delta_chi2"]=delta
            cr["penalties"]["fixed_profile_monotonicity_pass"]=delta>=-neg
        else:
            cr["penalties"]["fixed_h0_profile_delta_chi2"]=None
            cr["penalties"]["fixed_profile_monotonicity_pass"]=False
        cr["penalties"]["q011_shared_physics_delta_chi2"]=float(sh)-float(ref) if ref is not None and sh is not None else None

        req=all(p["status"]=="VALIDATED" for p in cr["profiles"].values())
        cr["status"]="VALIDATED" if req and cr["penalties"]["fixed_profile_monotonicity_pass"] and cr["same_run_embedding"]["pass"] else "NUMERICALLY_UNRESOLVED"
        result["chains"][chain]=cr

    primary=c["validation"]["required_primary_chains"]
    primary_ok=all(result["chains"][x]["status"]=="VALIDATED" for x in primary)
    jobs_ok=not missing and not dupes and source_ok

    if primary_ok and jobs_ok:
        result["validation_status"]="VALIDATED WITH CAVEATS"
        result["scientifically_usable_result"]=True
        result["next_action_required"]=False
        result["case_question_answer_status"]="YES, WITH CAVEATS"
    elif primary_ok:
        result["validation_status"]="PARTIAL"
        result["case_question_answer_status"]="PARTIALLY"
    else:
        result["validation_status"]="NUMERICALLY UNRESOLVED"
        result["case_question_answer_status"]="NO"

    result["claim_boundary"]={
        "planck_branch_is_k039_approximation":True,
        "spt_only_is_primary_independentish_test":True,
        "spt_plus_desi_is_secondary_and_partially_overlapping":True,
        "no_cross_chain_absolute_chi2_interpretation":True,
        "q011_is_not_promoted_to_global":True,
        "v11_not_interpreted_as_scientific_result":True,
        "flat_prior_normalization_constants_excluded_from_cross_mode_delta":True,
        "same_run_fixed_to_free_embedding_required":True,
    }
    result["journal_update"]={
        "case_id":c["project"]["case_id"],"q":"Q014",
        "program":"q014_external_viability_v12.py",
        "workflow":"q014-external-viability-v12.yml",
        "validation_status":result["validation_status"],
        "what_was_computed":"V12 same-run two-phase external n=3 profile-deviance certification: V11-parent Phase1 refinement followed by Phase1-fixed/free seeded free-H0 Phase2 certification.",
        "scientific_consequence":"Interpret only after mandatory V12 validation passes; report each chain separately.",
        "what_remains_unresolved":[] if result["scientifically_usable_result"] else
            ["One or more primary V12 profiles remain numerically unstable, fail same-run embedding, or fail nesting monotonicity."],
        "next_required_action":"ROUTE_VALIDATED_Q014_RESULT" if result["scientifically_usable_result"] else "CONTINUE_NUMERICAL_CERTIFICATION",
    }
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default=CONFIG_NAME)
    ap.add_argument("--inputs",nargs="+",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--manifest-output",required=True)
    a=ap.parse_args()
    c=load_cfg(a.config)
    r=aggregate(load_records(a.inputs),c)
    dump(a.output,r); dump(a.manifest_output,r["job_manifest"])
    print(json.dumps({"validation_status":r["validation_status"],"jobs":r["job_manifest"]},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
