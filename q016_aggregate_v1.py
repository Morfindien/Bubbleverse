#!/usr/bin/env python3
"""Merge/test Q016 endpoint jobs without cross-chain chi2 operations."""
import argparse, json, math
from pathlib import Path
import yaml

Q="Q016"; RUN="Q016-MATCHED-CMB-SURFACE-V1"; RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-001"
def load(p): return json.loads(Path(p).read_text())
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q016_matched_cmb_surface_v1_config.yml")
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args(); cfg=yaml.safe_load(Path(a.config).read_text())
    root=Path(a.input_dir); branches={}
    gates={}
    for branch in ("planck","spt","act"):
        profiles={}
        for mode in ("reference_free_h0","fixed_h0_71p5"):
            recs=[]
            for p in sorted(root.glob(f"{branch}_{mode}_r*.json")):
                d=load(p)
                if d.get("q")==Q and d.get("run_id")==RUN and d.get("status")=="COMPLETE":
                    recs.append(d)
            profiles[mode]=recs
            gates[f"{branch}_{mode}_complete"]=len(recs)>=4
            if recs:
                recs.sort(key=lambda x: float(x["chi2"]))
                best=float(recs[0]["chi2"])
                second=float(recs[1]["chi2"]) if len(recs)>1 else float("inf")
                spread=second-best
                profiles[mode]={"best":recs[0],"all":recs,"best_two_spread":spread,
                                "stable":spread<=float(cfg["execution"]["multistart_stability_delta_chi2_max"])}
                gates[f"{branch}_{mode}_multistart"]=profiles[mode]["stable"]
        if all(isinstance(profiles[m],dict) and "best" in profiles[m] for m in profiles):
            free=float(profiles["reference_free_h0"]["best"]["chi2"])
            fixed=float(profiles["fixed_h0_71p5"]["best"]["chi2"])
            delta=fixed-free
        else: delta=None
        branches[branch]={"profiles":profiles,"fixed_minus_free_delta_chi2":delta}
    gates.update({
      "Q_IDENTITY_GATE":True,
      "MODEL_IDENTITY_GATE":cfg["model"]["n_scf"]==3 and cfg["model"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "H0_TARGET_GATE":float(cfg["model"]["target_h0"])==71.5,
      "Q011_NONPORTABILITY_GATE":cfg["model"]["q011_exact_vector_as_external_endpoint"] is False,
      "COMMON_MULTIPOLE_GATE":cfg["surface"]["primary"]["ell_min"]==600 and cfg["surface"]["primary"]["ell_max"]==2000,
      "COMMON_OBSERVABLE_GATE":cfg["surface"]["primary"]["observables"]==["TT","TE","EE"],
      "COMMON_TAU_GATE":cfg["surface"]["tau"]["mean"]==0.051 and cfg["surface"]["tau"]["sigma"]==0.006,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
      "NO_SHARED_LOWZ_DOUBLECOUNT_GATE":cfg["surface"]["primary"]["low_z_data"]==[],
    })
    endpoint_pass=all(v for k,v in gates.items() if k.endswith("_complete") or k.endswith("_multistart"))
    result={"q":Q,"run_id":RUN,"result_id":RESULT,"stage":"PRIMARY_ENDPOINT_MERGE",
            "actual_computed_result":"AVAILABLE" if endpoint_pass else "INCOMPLETE",
            "branches":branches,"gates":gates,
            "cross_chain_chi2_sum_performed":False,
            "absolute_cross_chain_chi2_comparison_performed":False,
            "final_result_gate":"PENDING_ATTRIBUTION_AND_RESIDUAL_TESTS"}
    dump(a.output,result)
    if not endpoint_pass: raise SystemExit(2)
if __name__=="__main__": main()
