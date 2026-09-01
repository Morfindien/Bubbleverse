#!/usr/bin/env python3
"""Q014 V11 static and mandatory result validation."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import yaml
import q014_external_viability_v11 as eng

ROOT=Path(__file__).resolve().parent
RUN="Q014-EXTERNAL-VIABILITY-V11"
RESULT_ID="R-Q014-EDE-EXTERNAL-VIABILITY-008"
QUESTION="Når den samme n=3 EDE-model anvendes, hvor stor ekstern likelihood-penalty får high-H₀-regionen omkring det aktive Q011-punkt ved H₀=71.5 km s⁻¹ Mpc⁻¹ i Planck NPIPE- og SPT-3G D1-kæderne, når hver kædes egne nuisance-parametre og relevante kosmologiske parametre profileres korrekt og datasetoverlap ikke dobbeltregnes?"
BASIS=eng.BASIS
MUSE="4933ceb993ceb92e48b2191b8ccb1595d182bc4bc3862c1fbad61d5f82136e9b"

def dump(p,o):
    Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def static():
    c=yaml.safe_load((ROOT/"q014_external_viability_v11_config.yml").read_text(encoding="utf-8"))
    p=(ROOT/"q014_external_viability_v11.py").read_text(encoding="utf-8")
    wp=ROOT/".github/workflows/q014-external-viability-v11.yml"
    if not wp.exists(): wp=ROOT/"q014-external-viability-v11.yml"
    w=wp.read_text(encoding="utf-8")
    s=(ROOT/"q014_setup_v11.sh").read_text(encoding="utf-8")
    ph1=eng.phase_tasks(c,"phase1"); ph2=eng.phase_tasks(c,"phase2")
    ph1keys={(x["chain"],x["mode"],x["start_family"]) for x in ph1}
    ph2keys={(x["chain"],x["mode"],x["start_family"]) for x in ph2}
    gates={
      "CASE_QUESTION_IDENTITY_GATE":c["project"]["original_case_question"].strip()==QUESTION,
      "CASE_ID_NONINVENTION_GATE":c["project"]["case_id"]=="NOT DOCUMENTED",
      "V10_NUMERICAL_PARENT_GATE":c["parent"]["v10"]["github_run"]==33533089788 and c["parent"]["v10"]["artifact_id"]==9813716460 and c["parent"]["v10"]["result_id"]=="R-Q014-EDE-EXTERNAL-VIABILITY-007" and c["parent"]["v10"]["scientifically_usable_result"] is False,
      "V10_FAILURE_SIGNATURE_GATE":c["parent"]["v10"]["observed"]["planck_npipe_k039_approx"]["reference_free_h0"]["spread"]>1.0 and c["parent"]["v10"]["observed"]["spt_d1_only"]["fixed_profile_monotonicity_pass"] is False,
      "SCALAR_TOTAL_CHI2_GATE":BASIS in p and "comparable_objective" in p,
      "NORMALIZATION_FREE_OBJECTIVE_GATE":c["scientific_surface"]["objective_comparability_repair"]["cross_mode_comparable"] is True,
      "NO_CHI2_COMPONENT_DOUBLECOUNT_GATE":"sum(comps.values())" not in p,
      "PHASE1_JOB_COUNT_GATE":len(ph1)==18 and len(ph1keys)==18,
      "PHASE2_JOB_COUNT_GATE":len(ph2)==12 and len(ph2keys)==12,
      "TOTAL_JOB_COUNT_GATE":len(ph1)+len(ph2)==30,
      "SAME_RUN_FIXED_TO_FREE_DESIGN_GATE":c["execution"]["v11_same_run_policy"]["same_run_fixed_to_free_embedding_required"] is True and "p1_fixed_best" in c["execution"]["phase2_start_families"]["reference_free_h0"],
      "PHASE2_DEPENDENCY_GATE":"needs: [prepare, spt-assets, smoke, phase1, phase1-select]" in w or "needs: [prepare, spt-assets, smoke, phase1-select]" in w,
      "PHASE1_SELECTOR_GATE":"select-phase1" in p and "q014_phase1_seed_summary_v11.json" in w,
      "STABILITY_THRESHOLD_PRESERVATION_GATE":c["validation"]["max_best_two_delta_chi2"]==1.0 and c["execution"]["v11_same_run_policy"]["multistart_threshold_unchanged"]==1.0,
      "MONOTONICITY_THRESHOLD_PRESERVATION_GATE":c["validation"]["fixed_vs_free_negative_tolerance"]==0.25 and c["execution"]["v11_same_run_policy"]["fixed_vs_free_negative_tolerance_unchanged"]==0.25,
      "SEED_CANDIDATE_PRESERVATION_GATE":"EXACT_DETERMINISTIC_SEED" in p and "seed_candidate_preservation_pass" in p,
      "PHASE2_LOCAL_REFINEMENT_GATE":c["execution"]["phase2_minimizer"]["max_evals"]==1600 and c["execution"]["phase2_minimizer"]["rhoend"]==0.001,
      "LEGACY_SMOKE_COMPATIBILITY_GATE":"return _original_start(chain, family, c, info, q011_vec)" in p,
      "MUSE_FROZEN_REUSE_GATE":MUSE in w and "q014-v11-spt-muse-source" in w and "q014_setup_v10.sh" in s,
      "V10_PARENT_ARTIFACT_PROVENANCE_GATE":"9813716460" in w and "sha256:823b13455a7810f30c8c0e0bb4836ca7968facb13acc49adec71eeece8c3c499" in w,
      "VERSIONED_OUTPUT_FILENAMES_GATE":all(x in w for x in ["q014_job_manifest_v11.json","q014_test_manifest_v11.json","q014_result_ingestion_handoff_v11.json","q014_parent_preflight_v11.json","q014_phase1_matrix_v11.json","q014_phase2_matrix_v11.json"]) and all(x not in w for x in ["q014_job_manifest_v9.json","q014_test_manifest_v9.json","q014_result_ingestion_handoff_v9.json"]),
      "MANDATORY_RESULT_EXIT_GATE":'exit "$TEST_RC"' in w,
      "PRECOMPUTE_FAIL_FAST_GATE":"needs.prepare.result == 'success'" in w and "needs.smoke.result == 'success'" in w and "needs.phase1-select.result == 'success'" in w,
      "NO_H0DN_GATE":"h0dn" not in json.dumps(c["chains"]).lower() and "sh0es" not in json.dumps(c["chains"]).lower(),
      "NO_ACT_NUISANCE_GATE":"a_act" not in json.dumps(c["chains"]).lower() and "p_act" not in json.dumps(c["chains"]).lower(),
      "CHAIN_SEPARATION_GATE":c["claim_boundary"]["planck_plus_spt_direct_chi2_sum_forbidden"] is True,
      "N3_MODEL_GATE":c["scientific_surface"]["model"]=="ede_n3" and c["scientific_surface"]["n_scf"]==3,
    }
    return {"q":"Q014","run_id":RUN,"test_type":"STATIC","gates":gates,"status":"PASS" if all(gates.values()) else "FAIL"}

def result(path):
    c=yaml.safe_load((ROOT/"q014_external_viability_v11_config.yml").read_text(encoding="utf-8"))
    r=json.loads(Path(path).read_text(encoding="utf-8"))
    g={}
    g["Q_IDENTITY_GATE"]=r.get("q")=="Q014" and r.get("run_id")==RUN and r.get("result_id")==RESULT_ID
    g["CASE_QUESTION_IDENTITY_GATE"]=r.get("original_case_question","").strip()==QUESTION
    g["Q011_STATUS_PRESERVATION_GATE"]=r.get("q011_globality_status_preserved")=="BEST-OBSERVED MINIMUM ONLY"
    g["V10_NUMERICAL_PARENT_GATE"]=r.get("v10_numerical_parent",{}).get("github_run")==33533089788 and r.get("v10_numerical_parent",{}).get("scientifically_usable_result") is False
    g["NO_CROSS_CHAIN_CHI2_SUM_GATE"]=r.get("planck_spt_chi2_sum_performed") is False
    jm=r.get("job_manifest",{})
    g["JOB_COMPLETENESS_GATE"]=jm.get("expected")==30 and jm.get("returned")==30 and jm.get("phase1_expected")==18 and jm.get("phase2_expected")==12 and not jm.get("missing") and not jm.get("duplicates")
    g["SOURCE_PROVENANCE_COMPATIBILITY_GATE"]=jm.get("runtime_source_compatible") is True

    finite=stable=mono=seed=basis=embed=True
    for name in c["validation"]["required_primary_chains"]:
        ch=r.get("chains",{}).get(name,{})
        for mode in ("reference_free_h0","fixed_h0_71p5","q011_shared_physics"):
            pr=ch.get("profiles",{}).get(mode,{})
            x=pr.get("best_objective_chi2")
            finite &= x is not None and math.isfinite(float(x))
            stable &= pr.get("stable") is True
            seed &= pr.get("seed_candidate_preservation_pass") is True
            br=pr.get("best_record") or {}
            basis &= br.get("objective_basis")==BASIS and br.get("likelihood_chi2_scalar") is not None
        mono &= ch.get("penalties",{}).get("fixed_profile_monotonicity_pass") is True
        embed &= ch.get("same_run_embedding",{}).get("pass") is True

    g["FINITE_RESULT_GATE"]=finite
    g["MULTISTART_STABILITY_GATE"]=stable
    g["FIXED_PROFILE_MONOTONICITY_GATE"]=mono
    g["SEED_CANDIDATE_PRESERVATION_GATE"]=seed
    g["NORMALIZATION_FREE_OBJECTIVE_GATE"]=basis
    g["SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE"]=embed
    g["FINAL_VALIDATION_GATE"]=r.get("scientifically_usable_result") is True and r.get("validation_status")=="VALIDATED WITH CAVEATS"
    return {"q":"Q014","run_id":RUN,"test_type":"RESULT","result_id":r.get("result_id"),"gates":g,"status":"PASS" if all(g.values()) else "FAIL"}

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("static"); a.add_argument("--output",required=True)
    b=sub.add_parser("result"); b.add_argument("--result",required=True); b.add_argument("--output",required=True)
    x=ap.parse_args()
    rep=static() if x.cmd=="static" else result(x.result)
    dump(x.output,rep); print(json.dumps(rep,indent=2))
    return 0 if rep["status"]=="PASS" else 10

if __name__=="__main__":
    raise SystemExit(main())
