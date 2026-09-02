#!/usr/bin/env python3
"""Finite Q016 scientific gate test. Never fabricates missing attribution/residual evidence."""
import argparse,json,math
from pathlib import Path
import yaml
def load(p): return json.loads(Path(p).read_text())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",required=True); ap.add_argument("--merged",required=True)
    ap.add_argument("--attribution",required=False); ap.add_argument("--secondary",required=False); ap.add_argument("--output",required=True)
    a=ap.parse_args(); c=yaml.safe_load(Path(a.config).read_text()); m=load(a.merged)
    g={}
    g["Q_IDENTITY_GATE"]=m.get("q")=="Q016"
    g["MODEL_IDENTITY_GATE"]=c["model"]["n_scf"]==3
    g["H0_TARGET_GATE"]=float(c["model"]["target_h0"])==71.5
    g["ENDPOINT_REPROFILE_GATE"]=all(m.get("branches",{}).get(b,{}).get("fixed_minus_free_delta_chi2") is not None for b in ("planck","spt","act"))
    g["Q011_NONPORTABILITY_GATE"]=c["model"]["q011_exact_vector_as_external_endpoint"] is False
    g["COMMON_MULTIPOLE_GATE"]=[c["surface"]["primary"]["ell_min"],c["surface"]["primary"]["ell_max"]]==[600,2000]
    g["COMMON_OBSERVABLE_GATE"]=c["surface"]["primary"]["observables"]==["TT","TE","EE"]
    g["COMMON_TAU_GATE"]=(c["surface"]["tau"]["mean"],c["surface"]["tau"]["sigma"])==(0.051,0.006)
    g["NO_CROSS_CHAIN_CHI2_SUM_GATE"]=m.get("cross_chain_chi2_sum_performed") is False
    g["NO_SHARED_LOWZ_DOUBLECOUNT_GATE"]=c["surface"]["primary"]["low_z_data"]==[]
    # These require files produced by the numerical attribution/mechanism stages.
    att=load(a.attribution) if a.attribution and Path(a.attribution).exists() else {}
    sec=load(a.secondary) if a.secondary and Path(a.secondary).exists() else {}
    g["CHAIN_NATIVE_NUISANCE_GATE"]=att.get("chain_native_nuisance_gate") is True
    g["COVARIANCE_GATE"]=att.get("covariance_gate") is True
    g["FINITE_RESULT_GATE"]=att.get("finite_result_gate") is True
    g["MULTISTART_STABILITY_GATE"]=all(v for k,v in m.get("gates",{}).items() if k.endswith("_multistart"))
    g["RESULT_PROVENANCE_GATE"]=att.get("result_provenance_gate") is True
    g["RESIDUAL_VECTOR_GATE"]=att.get("residual_vector_gate") is True
    g["FULL_VS_LITE_DIAGNOSTIC_GATE"]=sec.get("full_vs_lite_diagnostic_gate") is True
    decision=att.get("common_residual_decision")
    g["COMMON_RESIDUAL_DECISION_GATE"]=decision in ("Q016-A","Q016-B","Q016-C")
    final=all(g.values())
    r={"q":"Q016","run_id":"Q016-MATCHED-CMB-SURFACE-V2","test_type":"FINAL_SCIENTIFIC_GATES",
       "gates":g,"final_result_gate":"PASS" if final else "UNRESOLVED",
       "scientifically_usable_result":final,
       "actual_computed_result":"NOT YET COMPLETE" if not final else "VALIDATED",
       "common_residual_decision":decision}
    Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    if not final: raise SystemExit(2)
if __name__=="__main__": main()
