#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,os
from pathlib import Path
import numpy as np
import yaml

Q="Q016"; RUN="Q016-CMB-MECHANISM-V3"; RESULT="R-Q016-EDE-CMB-MECHANISM-003"

def write_json(p,o):
    Path(p).write_text(json.dumps(o,indent=2,sort_keys=True,default=lambda x:x.tolist() if isinstance(x,np.ndarray) else str(x))+"\n")

def load_jsons(root,stage):
    rows={}
    for p in Path(root).rglob("*.json"):
        try:d=json.loads(p.read_text())
        except Exception:continue
        if d.get("q")==Q and d.get("run_id")==RUN and d.get("result_id")==RESULT and d.get("stage")==stage:
            rows[d["branch"]]=d
    return rows

def vector_band_compress(rec):
    # Diagnostic only: mean delta residual and mean standardized change per
    # experiment/observable/band. Never a cross-experiment chi2/significance.
    out={}
    rows=rec["delta"]["residual_vector_fixed_minus_free"]
    for r in rows:
        k=(r["observable"],r["common_band"])
        if r["common_band"]=="outside_common":continue
        out.setdefault(k,[]).append(float(r["delta_residual_fixed_minus_free"]))
    return {f"{k[0]}::{k[1]}":{
        "mean_delta_residual":float(np.mean(v)),
        "median_delta_residual":float(np.median(v)),
        "sign":int(np.sign(np.mean(v))),
        "n":len(v)
    } for k,v in out.items() if v}

def common_shape_diagnostic(matched):
    comp={b:vector_band_compress(r) for b,r in matched.items()}
    keys=sorted(set.intersection(*(set(x) for x in comp.values()))) if len(comp)==3 else []
    rows=[]
    for k in keys:
        signs={b:comp[b][k]["sign"] for b in ("planck","spt","act")}
        rows.append({
            "observable_band":k,
            "signs":signs,
            "all_same_nonzero_sign":len(set(signs.values()))==1 and 0 not in signs.values(),
            "means":{b:comp[b][k]["mean_delta_residual"] for b in ("planck","spt","act")}
        })
    return {
        "band_compressed_by_experiment":comp,
        "common_cells":rows,
        "same_sign_cell_count":sum(bool(r["all_same_nonzero_sign"]) for r in rows),
        "common_cell_count":len(rows),
        "interpretation":"Shape/sign concordance diagnostic only; no cross-experiment covariance or combined significance."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True);ap.add_argument("--matched-dir",required=True);ap.add_argument("--secondary-dir",required=True);ap.add_argument("--output",required=True)
    a=ap.parse_args();cfg=yaml.safe_load(Path(a.config).read_text())
    matched=load_jsons(a.matched_dir,"MATCHED_RESIDUAL")
    secondary=load_jsons(a.secondary_dir,"SECONDARY_MECHANISM")
    expected={"planck","spt","act"}
    matched_complete=set(matched)==expected and all(matched[b].get("status")=="PASS" for b in expected)
    secondary_explicit=set(secondary)==expected and all(secondary[b].get("status") in {"PASS","TECHNICALLY_UNAVAILABLE"} for b in expected)

    closure={}
    for b,r in matched.items():
        direct=float(r["delta"]["primary_chi2_fixed_minus_free"])
        recon=float(r["delta"]["reconstructed_chi2_fixed_minus_free"])
        closure[b]={"direct_primary_delta":direct,"reconstructed_delta":recon,"difference":recon-direct,"pass":abs(recon-direct)<=float(cfg["validation"]["primary_component_delta_abs_tol"])}

    guards={
        "cross_chain_chi2_sum_performed":False,
        "combined_cross_experiment_sigma_performed":False,
        "shared_cosmic_variance_acknowledged":True,
    }
    common=common_shape_diagnostic(matched) if matched_complete else {}
    all_closure=matched_complete and all(x["pass"] for x in closure.values())
    gate=bool(matched_complete and secondary_explicit and all_closure)

    out={
        "q":Q,"run_id":RUN,"result_id":RESULT,"case_id":"NOT DOCUMENTED",
        "stage":"MECHANISM_MERGED",
        "execution_status":"COMPLETE" if matched_complete and secondary_explicit else "PARTIAL",
        "tests_status":"PENDING_FINAL_TEST_JOB",
        "diagnostic_result_gate":"PASS" if gate else "FAIL",
        "final_result_gate":"PENDING_FINAL_TEST_JOB",
        "matched_residual":matched,
        "secondary_mechanism":secondary,
        "covariance_closure":closure,
        "common_residual_shape_diagnostic":common,
        "guards":guards,
        "decision":{
            "owner":"RESULT_INGESTION_ENGINE",
            "allowed_outcomes":["Q016-A","Q016-B","Q016-C"],
            "q016_outcome":"PENDING_RESULT_INGESTION",
            "reason":"Numerical engine provides diagnostics; causal scientific classification is not forced by arbitrary post-hoc thresholds."
        },
        "interpretation_guard":[
            "Signed covariance allocations are not independent chi2 components.",
            "Absolute chi2 values are never summed across Planck/SPT/ACT.",
            "No combined sigma is produced without a cross-experiment covariance model.",
            "Secondary full-MF diagnostics do not replace the certified V16 primary matched surface.",
            "TECHNICALLY_UNAVAILABLE secondary diagnostics are technical limitations, not physical evidence."
        ]
    }
    write_json(a.output,out)
    if not gate: raise SystemExit(2)

if __name__=="__main__":main()
