#!/usr/bin/env python3
"""Q016 V6 merge and multistart basin-replication certification."""
import argparse,json,math
from pathlib import Path
import yaml

Q="Q016"; RUN="Q016-MATCHED-CMB-SURFACE-V6"; RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-006"
V4_RUN="Q016-MATCHED-CMB-SURFACE-V4"; V4_RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-004"
V5_RUN="Q016-MATCHED-CMB-SURFACE-V5"; V5_RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-005"
BACKEND="5a131c91d657dd9a7c6364cc45b038710f8d0d97"
ALLOWED_IDS={V4_RUN:V4_RESULT,V5_RUN:V5_RESULT,RUN:RESULT}
TARGETED={("planck","reference_free_h0"),("spt","fixed_h0_71p5"),("act","fixed_h0_71p5")}

def load(p): return json.loads(Path(p).read_text())
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def approx(a,b,t=1e-12): return abs(float(a)-float(b))<=t

def surface_gate(d,branch,mode):
    if d.get("q")!=Q:return False,"q"
    rid=d.get("run_id")
    if rid not in ALLOWED_IDS or d.get("result_id")!=ALLOWED_IDS[rid]:return False,"run/result"
    if d.get("status")!="COMPLETE":return False,"not-complete"
    if d.get("branch")!=branch or d.get("mode")!=mode:return False,"branch/mode"
    if d.get("model_backend_commit")!=BACKEND:return False,"backend"
    if d.get("ell_range")!=[600,2000]:return False,"ell"
    if d.get("observables")!=["TT","TE","EE"]:return False,"observables"
    tau=d.get("tau_prior") or {}
    if not approx(tau.get("mean",999),.051) or not approx(tau.get("sigma",999),.006):return False,"tau"
    if d.get("exact_q011_vector_used_as_profile_endpoint") is not False:return False,"q011"
    if d.get("cross_chain_chi2_sum_performed") is not False:return False,"cross-chain"
    if mode=="fixed_h0_71p5" and not approx(d.get("target_h0",999),71.5):return False,"H0"
    if mode=="reference_free_h0" and d.get("target_h0") is not None:return False,"freeH0"
    try:
        if not math.isfinite(float(d["chi2"])):return False,"finite"
    except Exception:return False,"chi2"
    return True,"pass"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q016_matched_cmb_surface_v6_config.yml")
    ap.add_argument("--input-dir",required=True); ap.add_argument("--output",required=True)
    a=ap.parse_args()
    cfg=yaml.safe_load(Path(a.config).read_text())
    threshold=float(cfg["execution"]["continuation"]["multistart_delta_chi2_max"])
    minrep=int(cfg["execution"]["continuation"]["minimum_replicates_within_delta_chi2"])
    root=Path(a.input_dir); excluded=[]; branches={}; gates={}
    provenance={V4_RUN:0,V5_RUN:0,RUN:0}

    for branch in ("planck","spt","act"):
      profiles={}
      for mode in ("reference_free_h0","fixed_h0_71p5"):
        recs={}
        for p in sorted(root.glob(f"{branch}_{mode}_r*.json")):
          try:d=load(p)
          except Exception as e:
            excluded.append({"file":p.name,"reason":"parse","error":repr(e)});continue
          ok,why=surface_gate(d,branch,mode)
          if not ok:
            excluded.append({"file":p.name,"reason":why,"run_id":d.get("run_id"),"status":d.get("status")});continue
          r=int(d["restart"])
          old=recs.get(r)
          # Same restart may exist as V4 failure then V5 repair; failures were excluded above.
          # Two COMPLETE records with same restart identity are forbidden.
          if old is not None:
            raise RuntimeError(f"DUPLICATE_COMPLETE_RESTART_GATE=FAIL {branch} {mode} r={r}")
          recs[r]=d
          provenance[d["run_id"]]+=1

        accepted=sorted(recs.values(),key=lambda x:float(x["chi2"]))
        distinct=sorted(recs)
        complete=len(distinct)>=int(cfg["execution"]["continuation"]["minimum_distinct_complete_restarts"])
        if accepted:
          bestchi=float(accepted[0]["chi2"])
          replicas=[x for x in accepted if float(x["chi2"])-bestchi<=threshold]
          repids=sorted(int(x["restart"]) for x in replicas)
          stable=len(set(repids))>=minrep
          v6_near=[x for x in replicas if x["run_id"]==RUN]
          targeted=(branch,mode) in TARGETED
          targeted_gate=(not targeted) or (stable and len(v6_near)>=1)
          spread=(float(accepted[1]["chi2"])-bestchi) if len(accepted)>1 else float("inf")
        else:
          replicas=[];repids=[];stable=False;targeted_gate=False;spread=float("inf")

        profiles[mode]={
          "all":accepted,
          "best":accepted[0] if accepted else None,
          "complete_count":len(accepted),
          "accepted_restart_ids":distinct,
          "best_two_spread":spread,
          "replicate_restart_ids_within_delta_chi2":repids,
          "replicate_count_within_delta_chi2":len(repids),
          "multistart_stable":stable,
          "targeted_basin_replication_gate":targeted_gate,
        }
        prefix=f"{branch}_{mode}"
        gates[prefix+"_complete"]=complete
        gates[prefix+"_multistart"]=stable
        if (branch,mode) in TARGETED:
          gates[prefix+"_targeted_basin_replication"]=targeted_gate

      free=profiles["reference_free_h0"]; fixed=profiles["fixed_h0_71p5"]
      delta=None
      if free["best"] and fixed["best"]:
        delta=float(fixed["best"]["chi2"])-float(free["best"]["chi2"])
      branches[branch]={"profiles":profiles,"fixed_minus_free_delta_chi2":delta}

    gates.update({
      "Q_IDENTITY_GATE":cfg["project"]["q"]=="Q016",
      "MODEL_IDENTITY_GATE":cfg["model"]["n_scf"]==3 and cfg["model"]["backend_commit"]==BACKEND,
      "H0_TARGET_GATE":approx(cfg["model"]["target_h0"],71.5),
      "ENDPOINT_REPROFILE_GATE":True,
      "Q011_NONPORTABILITY_GATE":cfg["model"]["q011_exact_vector_as_external_endpoint"] is False,
      "COMMON_MULTIPOLE_GATE":[cfg["surface"]["primary"]["ell_min"],cfg["surface"]["primary"]["ell_max"]]==[600,2000],
      "COMMON_OBSERVABLE_GATE":cfg["surface"]["primary"]["observables"]==["TT","TE","EE"],
      "COMMON_TAU_GATE":approx(cfg["surface"]["tau"]["mean"],.051) and approx(cfg["surface"]["tau"]["sigma"],.006),
      "CHAIN_NATIVE_NUISANCE_GATE":True,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":True,
      "NO_SHARED_LOWZ_DOUBLECOUNT_GATE":cfg["surface"]["primary"]["low_z_data"]==[],
      "V4_PROVENANCE_GATE":provenance[V4_RUN]>=1,
      "V5_PROVENANCE_GATE":provenance[V5_RUN]>=1,
      "V6_TARGETED_PROVENANCE_GATE":provenance[RUN]>=1,
    })
    primary_pass=all(bool(v) for v in gates.values())
    result={
      "q":Q,"run_id":RUN,"result_id":RESULT,
      "stage":"PRIMARY_ENDPOINT_TARGETED_BASIN_CERTIFICATION",
      "actual_computed_result":"AVAILABLE" if primary_pass else "INCOMPLETE",
      "scientifically_usable_primary_endpoint_result":primary_pass,
      "primary_endpoint_gate":"PASS" if primary_pass else "FAIL",
      "final_result_gate":"PENDING_LATER_STAGES",
      "branches":branches,"gates":gates,"excluded_records":excluded,
      "provenance_counts":provenance,
      "cross_chain_chi2_sum_performed":False,
      "absolute_cross_chain_chi2_comparison_performed":False,
      "interpretation_guard":"Primary endpoint certification is not the final Q016 scientific answer."
    }
    dump(a.output,result)
    if not primary_pass: raise SystemExit(2)

if __name__=="__main__":main()
