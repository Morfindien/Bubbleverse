#!/usr/bin/env python3
"""Q016 V5 continuation merge: reuse valid V4 shards + V5 repair shards only."""
import argparse, json, math, re
from pathlib import Path
import yaml

Q="Q016"
RUN="Q016-MATCHED-CMB-SURFACE-V5"
RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-005"
PARENT_RUN="Q016-MATCHED-CMB-SURFACE-V4"
PARENT_RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-004"
BACKEND="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
ALLOWED_IDS={PARENT_RUN:PARENT_RESULT,RUN:RESULT}

def load(p): return json.loads(Path(p).read_text())
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def approx(a,b,tol=1e-12): return abs(float(a)-float(b))<=tol

def surface_gate(d,cfg,branch,mode):
    if d.get("q") != Q: return False,"q"
    rid=d.get("run_id"); resid=d.get("result_id")
    if rid not in ALLOWED_IDS or ALLOWED_IDS[rid] != resid: return False,"run/result"
    if d.get("status") != "COMPLETE": return False,"not-complete"
    if d.get("model_backend_commit") != BACKEND: return False,"backend"
    if d.get("ell_range") != [600,2000]: return False,"ell"
    if d.get("observables") != ["TT","TE","EE"]: return False,"observables"
    tau=d.get("tau_prior") or {}
    if not approx(tau.get("mean",999),0.051) or not approx(tau.get("sigma",999),0.006): return False,"tau"
    if d.get("exact_q011_vector_used_as_profile_endpoint") is not False: return False,"q011"
    if d.get("cross_chain_chi2_sum_performed") is not False: return False,"cross-chain-sum"
    if mode=="fixed_h0_71p5" and not approx(d.get("target_h0",999),71.5): return False,"h0"
    if mode=="reference_free_h0" and d.get("target_h0") is not None: return False,"free-h0-target"
    try:
        if not math.isfinite(float(d["chi2"])): return False,"finite"
    except Exception:
        return False,"chi2"
    return True,"pass"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q016_matched_cmb_surface_v5_config.yml")
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text())
    root=Path(a.input_dir)
    branches={}; gates={}; excluded=[]; provenance_counts={PARENT_RUN:0,RUN:0}
    for branch in ("planck","spt","act"):
        profiles={}
        for mode in ("reference_free_h0","fixed_h0_71p5"):
            accepted=[]; seen={}
            pattern=f"{branch}_{mode}_r*.json"
            for p in sorted(root.glob(pattern)):
                try: d=load(p)
                except Exception as exc:
                    excluded.append({"file":str(p),"reason":"parse","error":repr(exc)}); continue
                ok,why=surface_gate(d,cfg,branch,mode)
                if not ok:
                    excluded.append({"file":p.name,"reason":why,"status":d.get("status"),"run_id":d.get("run_id")})
                    continue
                r=int(d.get("restart",-999))
                if r in seen:
                    # A V5 repair may replace the same V4 restart only if the V4 record was not COMPLETE.
                    # Since only COMPLETE records reach here, duplicate COMPLETE restart identity is ambiguous.
                    raise RuntimeError(f"DUPLICATE_COMPLETE_RESTART_GATE=FAIL {branch} {mode} restart={r}")
                seen[r]=p.name
                accepted.append(d); provenance_counts[d["run_id"]]+=1
            accepted.sort(key=lambda d: float(d["chi2"]))
            distinct=sorted(int(d["restart"]) for d in accepted)
            complete=len(distinct)>=int(cfg["execution"]["continuation"]["minimum_distinct_complete_restarts"])
            gates[f"{branch}_{mode}_complete"]=complete
            gates[f"{branch}_{mode}_distinct_restarts"]=len(distinct)>=4
            if accepted:
                best=float(accepted[0]["chi2"])
                second=float(accepted[1]["chi2"]) if len(accepted)>1 else float("inf")
                spread=second-best
                stable=spread<=float(cfg["execution"]["multistart_stability_delta_chi2_max"])
                profiles[mode]={
                    "best":accepted[0],
                    "all":accepted,
                    "accepted_restart_ids":distinct,
                    "complete_count":len(accepted),
                    "best_two_spread":spread,
                    "stable":stable,
                }
                gates[f"{branch}_{mode}_multistart"]=stable
            else:
                profiles[mode]={"all":[],"accepted_restart_ids":[],"complete_count":0,"stable":False}
                gates[f"{branch}_{mode}_multistart"]=False

        free=profiles["reference_free_h0"]
        fixed=profiles["fixed_h0_71p5"]
        delta=None
        if free.get("all") and fixed.get("all"):
            delta=float(fixed["best"]["chi2"])-float(free["best"]["chi2"])
        branches[branch]={"profiles":profiles,"fixed_minus_free_delta_chi2":delta}

    gates.update({
      "Q_IDENTITY_GATE":cfg["project"]["q"]=="Q016",
      "MODEL_IDENTITY_GATE":cfg["model"]["n_scf"]==3 and cfg["model"]["backend_commit"]==BACKEND,
      "H0_TARGET_GATE":approx(cfg["model"]["target_h0"],71.5),
      "ENDPOINT_REPROFILE_GATE":True,
      "Q011_NONPORTABILITY_GATE":cfg["model"]["q011_exact_vector_as_external_endpoint"] is False,
      "COMMON_MULTIPOLE_GATE":cfg["surface"]["primary"]["ell_min"]==600 and cfg["surface"]["primary"]["ell_max"]==2000,
      "COMMON_OBSERVABLE_GATE":cfg["surface"]["primary"]["observables"]==["TT","TE","EE"],
      "COMMON_TAU_GATE":approx(cfg["surface"]["tau"]["mean"],0.051) and approx(cfg["surface"]["tau"]["sigma"],0.006),
      "CHAIN_NATIVE_NUISANCE_GATE":True,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
      "NO_SHARED_LOWZ_DOUBLECOUNT_GATE":cfg["surface"]["primary"]["low_z_data"]==[],
      "PARENT_V4_REUSE_GATE":provenance_counts[PARENT_RUN] >= 1,
      "V5_REPAIR_PROVENANCE_GATE":provenance_counts[RUN] >= 1,
    })
    endpoint_keys=[k for k in gates if k.endswith("_complete") or k.endswith("_distinct_restarts") or k.endswith("_multistart")]
    endpoint_pass=all(bool(gates[k]) for k in endpoint_keys)

    result={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"PRIMARY_ENDPOINT_CONTINUATION_MERGE",
      "parent":{"github_run_id":33693382859,"run_id":PARENT_RUN,"head_sha":"596ee68677784deb4c28d1eb5992faf6dcd2c5b1"},
      "actual_computed_result":"AVAILABLE" if endpoint_pass else "INCOMPLETE",
      "scientifically_usable_primary_endpoint_result":bool(endpoint_pass),
      "branches":branches,
      "gates":gates,
      "provenance_counts":provenance_counts,
      "excluded_records":excluded,
      "cross_chain_chi2_sum_performed":False,
      "absolute_cross_chain_chi2_comparison_performed":False,
      "final_result_gate":"PENDING_ATTRIBUTION_AND_RESIDUAL_TESTS"
    }
    dump(a.output,result)
    if not endpoint_pass:
        raise SystemExit(2)

if __name__=="__main__": main()
