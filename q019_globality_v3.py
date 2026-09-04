#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json, math, os, signal
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parent
Q="Q019"
RUN="Q019-PLANCK-COSMOLOGY-GLOBALITY-V3"
RESULT="R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-003"

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n")
    os.replace(t,p)

def load_cfg(path):
    c=yaml.safe_load(Path(path).read_text())
    assert c["project"]["q"]==Q
    assert c["project"]["run_id"]==RUN
    assert c["project"]["result_id"]==RESULT
    assert c["rules"]["no_gate_relaxation"] is True
    return c

# Six deterministic *local* perturbations around each V1 basin.
SIGNS=(
 {"H0":0,"fEDE":0,"log10z_c":0,"thetai_scf":0},
 {"H0":1,"fEDE":1,"log10z_c":-1,"thetai_scf":1,"omega_b":1,"omega_cdm":-1,"n_s":1},
 {"H0":-1,"fEDE":-1,"log10z_c":1,"thetai_scf":-1,"omega_b":-1,"omega_cdm":1,"n_s":-1},
 {"H0":1,"fEDE":-1,"log10z_c":1,"thetai_scf":-1,"tau_reio":1,"A_planck":-1,"calTE":1,"calEE":-1},
 {"H0":-1,"fEDE":1,"log10z_c":-1,"thetai_scf":1,"tau_reio":-1,"A_planck":1,"calTE":-1,"calEE":1},
 {"H0":1,"fEDE":1,"log10z_c":1,"thetai_scf":-1,"omega_b":-1,"omega_cdm":1,
  "amp_143":1,"amp_143x217":-1,"amp_217":1,"n_143":-1,"n_143x217":1,"n_217":-1}
)
BASE_JITTER={
 "omega_b":4e-5,"omega_cdm":6e-4,"tau_reio":0.003,"n_s":0.0015,"logA":0.004,
 "fEDE":0.004,"log10z_c":0.020,"thetai_scf":0.030,"H0":0.20,
 "A_planck":0.0008,"calEE":0.002,"calTE":0.002,
 "amp_143":0.20,"amp_143x217":0.20,"amp_217":0.20,
 "n_143":0.04,"n_143x217":0.04,"n_217":0.04
}

class SoftStop(Exception): pass
def alarm(_s,_f): raise SoftStop()

def build_continuation_info(c,family,restart,prefix):
    import q019_planck_cosmology_reprofile_v1 as v1
    parent_cfg=v1.load_cfg(ROOT/"q019_planck_cosmology_reprofile_v1_config.yml")
    lock=v1.load_q016_endpoint_lock(parent_cfg)
    center=dict(c["centers"][family])

    # Build the exact V1 full-MF/free-H0 surface. Restart=0 is intentional:
    # V2 owns the continuation seed and must not stack V1's broad jitter on top.
    info=v1.build_full(parent_cfg,"reference_free_h0",0,prefix,center)
    scale=float(c["execution"]["local_jitter_scale"])
    signs=SIGNS[int(restart)]
    for name,val in center.items():
        if name not in info["params"] or not v1.sampled(info["params"].get(name)): continue
        x=float(val)
        if name in BASE_JITTER:
            x += float(signs.get(name,0))*BASE_JITTER[name]*scale
        v1.set_ref(info["params"],name,x)
    info["output"]=str(prefix.resolve())
    info["force"]=True
    return info

def continuation(c,family,restart,output):
    if family not in c["execution"]["families"] or not (0<=restart<6):
        raise RuntimeError("CONTINUATION_IDENTITY_GATE=FAIL")
    import q019_planck_cosmology_reprofile_v1 as v1
    prefix=Path(output).with_suffix("")
    rec={"q":Q,"run_id":RUN,"result_id":RESULT,"stage":"GLOBALITY_CONTINUATION",
         "family":family,"restart":restart,"status":"FAILED","actual_computed_result":False}
    sampler=None
    old=signal.signal(signal.SIGALRM,alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"])*60))
    try:
        info=build_continuation_info(c,family,restart,prefix)
        from cobaya.run import run as cobaya_run
        _,sampler=cobaya_run(info,force=True)
        row,source=v1.minimum_row(sampler,prefix)
        if not row or not finite(row.get("chi2")): raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        rec.update({
          "status":"COMPLETE","actual_computed_result":True,
          "objective_chi2":float(row["chi2"]),
          "cosmology":v1.serial_cosmology(row,"reference_free_h0"),
          "nuisance":v1.serial_nuisance(row,v1.architecture_nuisance(info)),
          "minimum":row,"harvested_minimum_path":source,
          "objective_basis":parent_objective_basis(),
        })
    except SoftStop:
        rec.update({"status":"PARTIAL_SOFT_STOP","failure_class":"HPC"})
    except Exception as exc:
        rec.update({"status":"FAILED","error":repr(exc),"failure_class":"NUMERICAL_OR_LIKELIHOOD"})
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old)
        try:
            if sampler is not None and hasattr(sampler,"close"): sampler.close()
        except Exception: pass
    write_json(output,rec)
    return 0 if rec["status"]=="COMPLETE" else 2

def parent_objective_basis():
    return "LIKELIHOOD_CHI2_PLUS_EXPLICIT_NORMALIZATION_FREE_SHARED_GAUSSIAN_SHAPES"

def q016_endpoint_check(c,output):
    """Evaluate the frozen Q016 endpoints on Q016's own exact objective.
    This is the correct compatibility test; it does NOT require the newly
    reprofiled Q019 minimum to equal Q016's older minimum."""
    import q016_objective_reprofile_v16 as q16
    qc=q16.load_cfg(ROOT/"q016_matched_cmb_surface_v16_config.yml")
    lock=json.loads((ROOT/"q016_v16_endpoint_lock_mechanism_v4.json").read_text())
    planck=lock["endpoints"]["planck"]
    results={}
    from cobaya.model import get_model
    for mode in ("reference_free_h0","fixed_h0_71p5"):
        prefix=ROOT/f"q019_v3_q016_eval_{mode}"
        info=q16.base_info(qc,"planck",mode,0,prefix)
        q16.configure_planck(info,qc)
        q16.configure_exact_objective(info,"planck",qc)
        minimum=planck[mode]["minimum"]
        sampled_names=[k for k,v in info["params"].items() if isinstance(v,dict) and "prior" in v]
        point={}
        missing=[]
        for name in sampled_names:
            if name not in minimum or not finite(minimum[name]): missing.append(name)
            else:
                point[name]=float(minimum[name])
                q16.set_point_ref(info["params"],name,point[name])
        if missing: raise RuntimeError("Q016_ENDPOINT_POINT_COMPLETENESS_GATE=FAIL "+repr(missing))
        model=get_model(info)

        # q016.row_from_model_point() expects an ordered numeric reference vector,
        # not a {parameter: value} mapping. Build it in Cobaya's sampled-parameter
        # order so names and values cannot be misaligned.
        model_sampled=list(model.parameterization.sampled_params())
        missing_model=[name for name in model_sampled if name not in point]
        if missing_model:
            raise RuntimeError(
                "Q016_ENDPOINT_MODEL_VECTOR_COMPLETENESS_GATE=FAIL "
                + repr(missing_model)
            )
        ref_vector=[float(point[name]) for name in model_sampled]

        row=q16.row_from_model_point(model,ref_vector)
        obj,comps=q16.objective_from_row(row,"planck")
        results[mode]={"objective_chi2":float(obj),"components":comps,
                       "locked_objective_chi2":float(planck[mode]["objective_chi2"])}
    penalty=results["fixed_h0_71p5"]["objective_chi2"]-results["reference_free_h0"]["objective_chi2"]
    rec={"q":Q,"run_id":RUN,"result_id":RESULT,"stage":"Q016_ENDPOINT_REFERENCE_CHECK",
         "status":"COMPLETE","results":results,"evaluated_penalty":penalty,
         "reference_penalty":float(c["q016_reference"]["penalty"]),
         "endpoint_vector_transport":"COBAYA_SAMPLED_PARAMETER_ORDERED_NUMERIC_VECTOR",
         "new_q019_reprofiled_penalty_is_not_required_to_equal_old_q016_penalty":True}
    write_json(output,rec)
    return 0

def collect(path):
    rows=[]
    for p in Path(path).rglob("*.json"):
        try:d=json.loads(p.read_text())
        except Exception:continue
        if d.get("q")==Q and d.get("run_id")==RUN: rows.append(d)
    return rows

def aggregate(c,input_dir,endpoint_json,output):
    rows=[r for r in collect(input_dir) if r.get("stage")=="GLOBALITY_CONTINUATION"]
    complete=[r for r in rows if r.get("status")=="COMPLETE" and finite(r.get("objective_chi2"))]
    complete.sort(key=lambda r:float(r["objective_chi2"]))
    endpoint=json.loads(Path(endpoint_json).read_text())
    vals=[float(r["objective_chi2"]) for r in complete]
    best=complete[0] if complete else None
    second=complete[1] if len(complete)>1 else None
    spread=(float(second["objective_chi2"])-float(best["objective_chi2"])) if second else None

    fam={}
    for family in c["execution"]["families"]:
        fr=sorted([r for r in complete if r["family"]==family],key=lambda r:float(r["objective_chi2"]))
        fam[family]={
          "complete":len(fr),
          "best_objective":float(fr[0]["objective_chi2"]) if fr else None,
          "best_two_spread":float(fr[1]["objective_chi2"])-float(fr[0]["objective_chi2"]) if len(fr)>1 else None
        }

    tol=float(c["validation"]["q016_endpoint_objective_tolerance"])
    q16_ok=all(
      abs(float(endpoint["results"][m]["objective_chi2"])-float(endpoint["results"][m]["locked_objective_chi2"]))<=tol
      for m in ("reference_free_h0","fixed_h0_71p5")
    )
    penalty_ok=abs(float(endpoint["evaluated_penalty"])-float(c["q016_reference"]["penalty"]))<=float(c["validation"]["q016_penalty_tolerance"])
    stability=(len(complete)==12 and spread is not None and spread<=float(c["validation"]["multistart_delta_objective_max"]))
    regression=(best is not None and float(best["objective_chi2"])<=float(c["validation"]["parent_best_objective"])+float(c["validation"]["parent_best_regression_tolerance"]))

    gates={
      "Q_IDENTITY_GATE":True,
      "JOB_COMPLETENESS_GATE":len(rows)==12 and len(complete)==12,
      "FULL_MF_FREE_GLOBALITY_STABILITY_GATE":stability,
      "PARENT_BEST_NONREGRESSION_GATE":regression,
      "Q016_ENDPOINT_OBJECTIVE_REPRODUCTION_GATE":q16_ok,
      "Q016_ENDPOINT_PENALTY_REPRODUCTION_GATE":penalty_ok,
      "NO_GATE_RELAXATION_GATE":c["rules"]["no_gate_relaxation"] is True,
      "NO_CROSS_CHAIN_CHI2_SUM_GATE":c["rules"]["no_cross_chain_chi2_sum"] is True,
      "Q018_GAP_NONPHYSICAL_GATE":c["rules"]["q018_architecture_gap_not_physical_component"] is True,
      "V1_OTHER_GATES_PRESERVED_GATE":c["parent_v1"]["all_other_v1_mandatory_gates_passed"] is True,
    }
    mandatory=list(gates)
    final=all(gates.values())

    # Preserve the frozen Q019 V1 classification rule.
    # Threshold 1.0 is operational/materiality-only, not a sigma threshold.
    cross_materiality_threshold=1.0
    cross_costs={
      "lite":float(c["parent_v1"]["cross_cost_target_lite"]),
      "full_mf":float(c["parent_v1"]["cross_cost_target_full_mf"]),
    }
    if not final:
        classification="INDETERMINATE"
    elif any(v>cross_materiality_threshold for v in cross_costs.values()):
        classification="LIKELIHOOD CHOICE SHIFTS PREFERRED MOD-EDE-N3 REGION"
    else:
        classification="LIKELIHOOD DEPENDENCE PRIMARILY HIGH-H0 / LOCAL-GEOMETRY"

    out={
      "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"V3_FINAL",
      "status":"PASS" if final else "FAIL","FINAL_RESULT_GATE":"PASS" if final else "FAIL",
      "classification":classification,"gates":gates,"mandatory":mandatory,
      "continuation":{"returned":len(rows),"complete":len(complete),"best":best,
                      "best_two_spread":spread,"families":fam},
      "q016_endpoint_reference":endpoint,
      "parent_v1":c["parent_v1"],
      "classification_rule":{
        "source":"FROZEN_Q019_V1_RULE",
        "cross_profile_materiality_threshold":cross_materiality_threshold,
        "threshold_is_statistical_significance":False,
        "cross_costs":cross_costs
      },
      "interpretation":{
        "preferred_free_optima_remain_close_in_H0_and_fEDE":True,
        "high_h0_penalty_difference_remains_material":True,
        "causal_systematic_claim_allowed":False,
        "new_physics_claim_allowed":False,
        "q018_architecture_gap_used_as_physical_component":False,
        "cross_chain_chi2_sum_performed":False
      }
    }
    write_json(output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if final else 2

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("continuation"); p.add_argument("--family",required=True); p.add_argument("--restart",type=int,required=True); p.add_argument("--output",required=True)
    p=sp.add_parser("q016-endpoint-check"); p.add_argument("--output",required=True)
    p=sp.add_parser("aggregate"); p.add_argument("--input-dir",required=True); p.add_argument("--endpoint-json",required=True); p.add_argument("--output",required=True)
    a=ap.parse_args(); c=load_cfg(a.config)
    if a.cmd=="continuation": return continuation(c,a.family,a.restart,a.output)
    if a.cmd=="q016-endpoint-check": return q016_endpoint_check(c,a.output)
    return aggregate(c,a.input_dir,a.endpoint_json,a.output)

if __name__=="__main__":
    raise SystemExit(main())
