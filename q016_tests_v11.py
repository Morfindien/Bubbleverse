#!/usr/bin/env python3
"""Q016 V11 static/runtime objective tests and final gate validation."""
import argparse,ast,json,math
from pathlib import Path
import yaml

RUN="Q016-MATCHED-CMB-SURFACE-V11"
RESULT="R-Q016-EDE-MATCHED-CMB-SURFACE-011"
BASIS="SCALAR_PRIMARY_CMB_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_SHAPE_LIKELIHOODS"

def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")

def static_test(cfg_path,output):
    c=yaml.safe_load(Path(cfg_path).read_text())
    src=Path("q016_objective_reprofile_v11.py").read_text()
    agg=Path("q016_aggregate_v11.py").read_text()
    wf=Path(".github/workflows/q016-matched-cmb-surface-v11.yml").read_text() if Path(".github/workflows/q016-matched-cmb-surface-v11.yml").exists() else Path("q016-matched-cmb-surface-v11.yml").read_text()
    ast.parse(src); ast.parse(agg)
    checks={
        "Q_IDENTITY_GATE":c["project"]["q"]=="Q016",
        "RUN_IDENTITY_GATE":c["project"]["run_id"]==RUN and c["project"]["result_id"]==RESULT,
        "MODEL_IDENTITY_GATE":c["model"]["n_scf"]==3 and c["model"]["backend_commit"]=="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
        "OBJECTIVE_IDENTITY_GATE":c["execution"]["objective"]["basis"]==BASIS,
        "IGNORE_PRIOR_GATE":c["execution"]["optimizer"]["ignore_prior"] is True,
        "MULTISTART_THRESHOLD_UNCHANGED_GATE":float(c["execution"]["continuation"]["multistart_delta_objective_max"])==1.0,
        "MIN_REPLICATES_UNCHANGED_GATE":int(c["execution"]["continuation"]["minimum_replicates_within_delta_objective"])==2,
        "PLANCK_ONLY_EXTENSION_GATE":wf.count("family:")==4 and "branch: spt" not in wf and "branch: act" not in wf,
        "NO_PREVIOUS_PROFILE_RERUN_GATE":"Run exact-objective fixed profile" not in wf and "phase1_fixed_embed, restart: 10" not in wf,
        "V10_PARENT_GATE":"33764943297" in wf and "q016-primary-merged-v10" in wf,
        "NONZERO_PERTURBATION_GATE":"NONZERO_PERTURBATION_GATE" in src and "v10_planck_free_best_cross_a" in src,
        "RECURSIVE_PARENT_DISCOVERY_GATE":".rglob(" in agg,
        "NO_CROSS_CHAIN_SUM_GATE":"cross_chain_chi2_sum_performed" in agg,
    }
    out={"q":"Q016","run_id":RUN,"test":"STATIC","checks":checks,"status":"PASS" if all(checks.values()) else "FAIL"}
    dump(output,out)
    if out["status"]!="PASS":raise SystemExit(2)

def runtime_objective_test(output):
    # Runtime semantics test for the exact V11 objective.
    #
    # Cobaya ignore_prior=True minimizes likelihood but remains subject to prior
    # bounds. For a Gaussian prior, the minimizer constructs finite numerical
    # bounds from confidence_for_unbounded (default 0.9999995 ~= 5 sigma).
    #
    # V7's toy was invalid because it used N(-5,1) with a likelihood optimum x=2:
    # the target lay ~7 sigma outside Cobaya's allowed numerical box. V11 instead
    # uses N(0,1), whose MAP would still differ from the likelihood optimum, while
    # x=2 is safely inside the same unchanged default bounds.
    from cobaya.run import run
    from cobaya.model import get_model
    def exact_shape(x):
        return -0.5*((float(x)-2.0)/0.5)**2
    info={
        "likelihood":{"q016_toy_shape":{"external":exact_shape}},
        "params":{"x":{"prior":{"dist":"norm","loc":0.0,"scale":1.0},"ref":2.1,"proposal":0.1}},
        "sampler":{"minimize":{"method":"bobyqa","ignore_prior":True,"best_of":1,
                               "max_evals":1000,"override_bobyqa":{"rhoend":1e-7}}},
    }
    # Explicitly prove the test target is inside the optimization bounds before
    # using the test to validate ignore_prior semantics.
    model=get_model(info)
    bounds=model.prior.bounds(confidence_for_unbounded=0.9999995)
    lo=float(bounds[0,0]); hi=float(bounds[0,1])
    target_inside_bounds=(lo < 2.0 < hi)
    if not target_inside_bounds:
        out={"q":"Q016","run_id":RUN,"test":"COBAYA_EXACT_OBJECTIVE_RUNTIME",
             "status":"FAIL","failure":"TOY_TARGET_OUTSIDE_PRIOR_BOUNDS",
             "bounds":[lo,hi],"target":2.0}
        dump(output,out)
        raise SystemExit(2)
    _,s=run(info)
    m=s.products()["minimum"]
    try:row=m.data.iloc[0].to_dict()
    except Exception:row=dict(m)
    x=float(row["x"]); chi=float(row["chi2"]); comp=float(row["chi2__q016_toy_shape"])
    checks={
        "TOY_TARGET_INSIDE_PRIOR_BOUNDS_GATE":target_inside_bounds,
        "TOY_LIKELIHOOD_MINIMUM_GATE":abs(x-2.0)<1e-3,
        "TOY_OBJECTIVE_COMPONENT_GATE":abs(chi-comp)<1e-8,
        "TOY_FINITE_GATE":math.isfinite(chi),
    }
    out={"q":"Q016","run_id":RUN,"test":"COBAYA_EXACT_OBJECTIVE_RUNTIME","x":x,"chi2":chi,
         "component":comp,"prior_bounds":[lo,hi],"target":2.0,
         "checks":checks,"status":"PASS" if all(checks.values()) else "FAIL"}
    dump(output,out)
    if out["status"]!="PASS":raise SystemExit(2)

def parent_test(result_path,output):
    d=json.loads(Path(result_path).read_text()); g=d.get("gates",{})
    checks={
        "V10_IDENTITY_GATE":d.get("q")=="Q016" and d.get("run_id")=="Q016-MATCHED-CMB-SURFACE-V10" and d.get("result_id")=="R-Q016-EDE-MATCHED-CMB-SURFACE-010",
        "V10_EXPECTED_PRIMARY_FAIL_GATE":d.get("primary_endpoint_gate")=="FAIL" and d.get("validation_status")=="NUMERICALLY_UNRESOLVED",
        "PLANCK_FREE_MULTISTART_ONLY_BRANCH_FAILURE_GATE":
            g.get("planck_free_multistart") is False and
            g.get("spt_free_multistart") is True and g.get("act_free_multistart") is True and
            g.get("planck_fixed_multistart") is True and g.get("spt_fixed_multistart") is True and g.get("act_fixed_multistart") is True,
        "NESTING_ALREADY_PASS_GATE":g.get("PROFILE_NESTING_GATE") is True,
        "EMBEDDING_ALREADY_PASS_GATE":g.get("SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE") is True,
        "ALL_COMPLETENESS_GATES":all(g.get(f"{b}_{m}_complete") is True for b in ("planck","spt","act") for m in ("fixed","free")),
    }
    out={"q":"Q016","run_id":RUN,"test":"V10_PARENT_AUDIT","checks":checks,"status":"PASS" if all(checks.values()) else "FAIL"}
    dump(output,out)
    if out["status"]!="PASS":raise SystemExit(2)

def final_test(result_path,output):
    d=json.loads(Path(result_path).read_text())
    checks={
        "IDENTITY_GATE":d.get("q")=="Q016" and d.get("run_id")==RUN and d.get("result_id")==RESULT,
        "VALIDATION_GATE":d.get("validation_status")=="VALIDATED",
        "PRIMARY_ENDPOINT_GATE":d.get("primary_endpoint_gate")=="PASS",
        "ENDPOINT_REPROFILE_GATE":d.get("gates",{}).get("ENDPOINT_REPROFILE_GATE") is True,
        "PROFILE_NESTING_GATE":d.get("gates",{}).get("PROFILE_NESTING_GATE") is True,
        "SAME_RUN_EMBEDDING_GATE":d.get("gates",{}).get("SAME_RUN_FIXED_TO_FREE_EMBEDDING_GATE") is True,
        "MULTISTART_GATE":d.get("gates",{}).get("MULTISTART_STABILITY_GATE") is True,
        "NO_CROSS_CHAIN_SUM_GATE":d.get("cross_chain_chi2_sum_performed") is False,
        "FINAL_Q016_STILL_PENDING_GATE":str(d.get("final_result_gate","")).startswith("PENDING_"),
    }
    out={"q":"Q016","run_id":RUN,"result_id":RESULT,"test":"PRIMARY_FINAL",
         "checks":checks,"status":"PASS" if all(checks.values()) else "FAIL",
         "scientific_routing":"RESULT_INGESTION_THEN_ATTRIBUTION_RESIDUAL_STAGE" if all(checks.values()) else "NUMERICAL_EXECUTION_REMAINS_REQUIRED"}
    dump(output,out)
    if out["status"]!="PASS":raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("static");p.add_argument("--config",default="q016_matched_cmb_surface_v11_config.yml");p.add_argument("--output",required=True)
    p=sub.add_parser("runtime");p.add_argument("--output",required=True)
    p=sub.add_parser("parent");p.add_argument("--result",required=True);p.add_argument("--output",required=True)
    p=sub.add_parser("final");p.add_argument("--result",required=True);p.add_argument("--output",required=True)
    a=ap.parse_args()
    if a.cmd=="static":static_test(a.config,a.output)
    elif a.cmd=="runtime":runtime_objective_test(a.output)
    elif a.cmd=="parent":parent_test(a.result,a.output)
    else:final_test(a.result,a.output)
if __name__=="__main__":main()
