#!/usr/bin/env python3
"""Static and scientific-result gates for Bubbleverse Q014 V1."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from typing import Any
import yaml

ROOT=Path(__file__).resolve().parent
QUESTION="Når den samme n=3 EDE-model anvendes, hvor stor ekstern likelihood-penalty får high-H₀-regionen omkring det aktive Q011-punkt ved H₀=71.5 km s⁻¹ Mpc⁻¹ i Planck NPIPE- og SPT-3G D1-kæderne, når hver kædes egne nuisance-parametre og relevante kosmologiske parametre profileres korrekt og datasetoverlap ikke dobbeltregnes?"

def dump(p:str|Path,o:Any): Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")

def static(config:str,source_lock:str)->dict[str,Any]:
    c=yaml.safe_load(Path(config).read_text()); s=json.loads(Path(source_lock).read_text())
    gates={}
    gates["CASE_QUESTION_IDENTITY_GATE"]=c["project"]["original_case_question"].strip()==QUESTION
    gates["CASE_ID_NONINVENTION_GATE"]=c["project"]["case_id"]=="NOT DOCUMENTED"
    gates["N3_MODEL_GATE"]=c["scientific_surface"]["model"]=="ede_n3" and c["scientific_surface"]["n_scf"]==3
    gates["CHAIN_NATIVE_NUISANCE_CONSTRAINT_GATE"]=c["execution"]["minimizer"]["ignore_prior"] is False
    chaintext=json.dumps(c["chains"]).lower()
    gates["NO_H0DN_GATE"]="h0dn" not in chaintext and "sh0es" not in chaintext
    gates["NO_ACT_NUISANCE_GATE"]="a_act" not in chaintext and "p_act" not in chaintext
    gates["PLANCK_APPROXIMATION_CLAIM_GATE"]=(not c["chains"]["planck_npipe_k039_approx"]["paper_native_reproduction"] and
                                                s["planck_k039_approx"]["claim_status"]=="COMMON_BACKEND_APPROXIMATION_ONLY")
    gates["SPT_NO_DESI_PRIMARY_GATE"]=(not c["chains"]["spt_d1_only"]["include_desi_dr2"] and
                                         c["chains"]["spt_d1_plus_desi"]["include_desi_dr2"])
    gates["SPT_LENSING_NO_PRIMARY_CMB_DOUBLECOUNT_GATE"]=(c["chains"]["spt_d1_only"]["lensing_likelihood"]["components"]==["ϕϕ"])
    gates["CHAIN_SEPARATION_GATE"]=(c["claim_boundary"]["planck_plus_spt_direct_chi2_sum_forbidden"] and
                                      c["claim_boundary"]["absolute_chi2_cross_package_comparison_forbidden"])
    gates["MUSE_HASH_NONINVENTION_GATE"]=(s["spt_k040"]["muse_archive_sha256"] is None and
                                            "CAPTURE" in s["spt_k040"]["muse_archive_hash_policy"])
    return {"q":"Q014","test_type":"STATIC","gates":gates,"status":"PASS" if all(gates.values()) else "FAIL"}

def result_tests(config:str,result_path:str)->dict[str,Any]:
    c=yaml.safe_load(Path(config).read_text()); r=json.loads(Path(result_path).read_text()); gates={}
    gates["Q_IDENTITY_GATE"]=r.get("q")=="Q014" and r.get("run_id")=="Q014-EXTERNAL-VIABILITY-V1"
    gates["CASE_QUESTION_IDENTITY_GATE"]=r.get("original_case_question","").strip()==QUESTION
    gates["Q011_STATUS_PRESERVATION_GATE"]=r.get("q011_globality_status_preserved")=="BEST-OBSERVED MINIMUM ONLY"
    gates["NO_CROSS_CHAIN_CHI2_SUM_GATE"]=r.get("planck_spt_chi2_sum_performed") is False
    gates["JOB_COMPLETENESS_GATE"]=(not r.get("job_manifest",{}).get("missing") and not r.get("job_manifest",{}).get("duplicates"))
    gates["SOURCE_PROVENANCE_COMPATIBILITY_GATE"]=r.get("job_manifest",{}).get("runtime_source_compatible") is True
    primary=c["validation"]["required_primary_chains"]
    finite=True; stable=True; monotonic=True
    for name in primary:
        ch=r.get("chains",{}).get(name,{})
        for mode in ("reference_free_h0","fixed_h0_71p5","q011_shared_physics"):
            p=ch.get("profiles",{}).get(mode,{})
            x=p.get("best_objective_chi2")
            finite &= x is not None and math.isfinite(float(x))
            stable &= p.get("stable") is True
        monotonic &= ch.get("penalties",{}).get("fixed_profile_monotonicity_pass") is True
    gates["FINITE_RESULT_GATE"]=finite
    gates["MULTISTART_STABILITY_GATE"]=stable
    gates["FIXED_PROFILE_MONOTONICITY_GATE"]=monotonic
    gates["FINAL_VALIDATION_GATE"]=(r.get("scientifically_usable_result") is True and r.get("validation_status")=="VALIDATED WITH CAVEATS")
    return {"q":"Q014","test_type":"RESULT","result_id":r.get("result_id"),"gates":gates,
            "status":"PASS" if all(gates.values()) else "FAIL",
            "caveats":["K-039 branch is a public NPIPE common-backend approximation.",
                       "SPT branch uses official likelihood products but Bubbleverse common backend/optimizer."]}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default="q014_external_viability_v1_config.yml")
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("static"); p.add_argument("--source-lock",default="q014_external_viability_v1_source_lock.json"); p.add_argument("--output",required=True)
    p=sub.add_parser("result"); p.add_argument("--result",required=True); p.add_argument("--output",required=True)
    a=ap.parse_args(); rep=static(a.config,a.source_lock) if a.cmd=="static" else result_tests(a.config,a.result)
    dump(a.output,rep); print(json.dumps(rep,indent=2)); return 0 if rep["status"]=="PASS" else 10
if __name__=="__main__": raise SystemExit(main())
