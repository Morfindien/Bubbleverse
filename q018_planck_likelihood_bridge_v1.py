#!/usr/bin/env python3
"""
Bubbleverse Q018 — controlled Planck likelihood bridge V1.

Purpose
-------
Keep the certified Q016 cosmological endpoints frozen and reuse Q017's full
multifrequency CamSpec builder.  The program profiles only Planck nuisance
parameters on four explicitly defined full-MF bridge surfaces:

  full_native
      Q017 full-MF construction and native-prior objective semantics.

  full_likelihood_only
      Same full-MF data/model/nuisance parameterization, but Cobaya minimization
      ignores parameter-prior density. Prior support/reference geometry remains.

  shared3_only
      Full-MF likelihood with the six full-MF foreground parameters fixed at
      their common builder reference values; A_planck/calTE/calEE remain sampled.

  foreground6_only
      Full-MF likelihood with A_planck/calTE/calEE fixed to their certified Q016
      endpoint values; the six full-MF foreground parameters remain sampled.

These are controlled diagnostics, not additive chi-square components.  The
lite->full data/frequency/covariance transformation remains a coupled
architecture bundle unless a valid lower-level adapter can separate it.
"""
from __future__ import annotations
import argparse, json, math, os, signal, time
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q018"
RUN = "Q018-PLANCK-LIKELIHOOD-BRIDGE-V1"
RESULT = "R-Q018-EDE-PLANCK-LIKELIHOOD-BRIDGE-001"
Q016_RUN = "Q016-MATCHED-CMB-SURFACE-V16"
Q016_RESULT = "R-Q016-EDE-MATCHED-CMB-SURFACE-016"
Q017_RUN = "Q017-PLANCK-DIRECTION-LOCALIZATION-V3"
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
BRIDGES = ("full_native","full_likelihood_only","shared3_only","foreground6_only")
ENDPOINTS = ("reference_free_h0","fixed_h0_71p5")
SHARED3 = ("A_planck","calTE","calEE")
FG6 = ("amp_143","amp_217","amp_143x217","n_143","n_217","n_143x217")

def finite(x: Any) -> bool:
    try: return math.isfinite(float(x))
    except Exception: return False

def write_json(path: str|Path, obj: Any) -> None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    os.replace(t,p)

def load_cfg(path: str|Path) -> dict:
    c=yaml.safe_load(Path(path).read_text())
    if c["project"]["q"] != Q: raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    m=c["model"]
    if m["name"]!="ede_n3" or int(m["n_scf"])!=3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"]!="5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if float(c["endpoints"]["free_h0"]) != 67.988328967159:
        raise RuntimeError("FREE_ENDPOINT_GATE=FAIL")
    if float(c["endpoints"]["fixed_h0"]) != 71.5:
        raise RuntimeError("FIXED_ENDPOINT_GATE=FAIL")
    return c

def load_q016_lock(c: Mapping[str,Any]) -> dict:
    p=ROOT/c["parent_q016"]["endpoint_lock"]
    d=json.loads(p.read_text())
    if d.get("q")!="Q016" or d.get("run_id")!=Q016_RUN or d.get("result_id")!=Q016_RESULT:
        raise RuntimeError("Q016_ENDPOINT_LOCK_IDENTITY_GATE=FAIL")
    planck=d["endpoints"]["planck"]
    if abs(float(planck["reference_free_h0"]["minimum"]["H0"])-67.988328967159)>1e-10:
        raise RuntimeError("FREE_ENDPOINT_GATE=FAIL")
    # fixed H0 is fixed by the profile and therefore absent from some minimum rows
    return d

def q017_compatible_cfg(c: Mapping[str,Any]) -> dict:
    """Build only the config keys consumed by Q017's frozen full-MF constructor."""
    return {
        "project":{"q":"Q017","run_id":Q017_RUN,
                   "result_id":"R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-003"},
        "model":{
            "name":"ede_n3","n_scf":3,
            "backend_repository":"mwt5345/class_ede",
            "backend_commit":"5a131c91d657dd9a7c6364cc45b038710f8d0d97",
            "target_h0":71.5
        },
        "parent_q016":{
            "endpoint_lock":c["parent_q016"]["endpoint_lock"],
            "parent_run_id":Q016_RUN,
            "parent_result_id":Q016_RESULT,
            "parent_github_run_id":33785257733,
            "parent_head_sha":"3a154b44cbef4b2a3d10fdb12435105921bfc962",
            "expected_h0":{"reference_free_h0":67.988328967159,"fixed_h0_71p5":71.5}
        },
        "planck":{
            "likelihood":FULL_LIKE,
            "branch":"planck_npipe_k039_approx"
        },
        "nuisance":{
            "all":list(SHARED3+FG6),
            "groups":{
                "calibration":list(SHARED3),
                "foreground_143":["amp_143","n_143"],
                "foreground_143x217":["amp_143x217","n_143x217"],
                "foreground_217":["amp_217","n_217"],
                "foreground_all":list(FG6)
            }
        },
        "execution":{
            "max_evals":int(c["execution"]["max_evals"]),
            "rhoend":float(c["execution"]["rhoend"]),
            "seed_base":int(c["execution"]["seed_base"]),
            "soft_stop_minutes":float(c["execution"]["soft_stop_minutes"])
        }
    }

def build_info(c: Mapping[str,Any], lock: Mapping[str,Any], endpoint: str,
               restart: int, bridge: str, prefix: Path):
    import q017_planck_direction_localization_v1 as q17
    qc=q017_compatible_cfg(c)

    # First build obtains the exact Q017 full-MF nuisance reference vector.
    info0, cosmology, starts0, sampled0 = q17.build_full_mf_info(
        qc, lock, endpoint, restart, prefix
    )
    lock_values={}
    if bridge=="shared3_only":
        lock_values={k:float(starts0[k]) for k in FG6}
    elif bridge=="foreground6_only":
        row=q17.endpoint_record(lock,endpoint)["minimum"]
        lock_values={k:float(row[k]) for k in SHARED3}
    elif bridge not in ("full_native","full_likelihood_only"):
        raise RuntimeError("BRIDGE_MODE_GATE=FAIL")

    if lock_values:
        info, cosmology, starts, sampled = q17.build_full_mf_info(
            qc, lock, endpoint, restart, prefix, locked_values=lock_values
        )
    else:
        info, cosmology, starts, sampled = info0, cosmology, starts0, sampled0

    if bridge=="full_likelihood_only":
        m=info.setdefault("sampler",{}).setdefault("minimize",{})
        m["ignore_prior"]=True

    return info, cosmology, starts, sampled, lock_values

class SoftStop(Exception): pass
def _alarm(_sig,_frame): raise SoftStop()

def profile(c, lock, endpoint, restart, bridge, output):
    if endpoint not in ENDPOINTS: raise RuntimeError("ENDPOINT_GATE=FAIL")
    if bridge not in BRIDGES: raise RuntimeError("BRIDGE_MODE_GATE=FAIL")
    prefix=Path(output).with_suffix("")
    rec={
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"BRIDGE_PROFILE",
        "endpoint":endpoint,"restart":int(restart),"bridge":bridge,
        "status":"FAILED","actual_computed_result":False,
        "additive_component_interpretation_allowed":False
    }
    old=signal.signal(signal.SIGALRM,_alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"])*60))
    sampler=None
    try:
        info,cosmo,starts,sampled,locked=build_info(c,lock,endpoint,restart,bridge,prefix)
        rec.update({"frozen_cosmology":cosmo,"nuisance_start":starts,
                    "nuisance_locked":locked,"sampled_nuisance_expected":sampled,
                    "ignore_prior":bool(info["sampler"]["minimize"].get("ignore_prior",False))})
        from cobaya.run import run as cobaya_run
        import q017_planck_direction_localization_v1 as q17
        _updated,sampler=cobaya_run(info,force=True)
        row,harvested=q17.minimum_row(sampler,prefix)
        if not row: raise RuntimeError("MINIMUM_GATE=FAIL")
        # Cobaya row["chi2"] is the normalization-free sum of likelihood chi2 terms.
        if not finite(row.get("chi2")): raise RuntimeError("FINITE_RESULT_GATE=FAIL chi2")
        if bridge=="full_native":
            objective, comps, basis, shapes=q17.comparable_objective(row)
        else:
            objective=float(row["chi2"])
            comps={k:float(v) for k,v in row.items() if str(k).startswith("chi2__") and finite(v)}
            basis="LIKELIHOOD_CHI2_WITH_FROZEN_COSMOLOGY"
            shapes={}
        best={}
        for n in SHARED3+FG6:
            if n in row and finite(row[n]): best[n]=float(row[n])
            elif n in locked: best[n]=float(locked[n])
            else: raise RuntimeError("NUISANCE_SERIALIZATION_GATE=FAIL "+n)
        rec.update({"status":"COMPLETE","actual_computed_result":True,
                    "objective_chi2":float(objective),"objective_basis":basis,
                    "chi2_components":comps,"shape_penalties":shapes,
                    "nuisance_bestfit":best,"minimum":row,
                    "harvested_minimum_path":harvested})
    except SoftStop:
        rec.update({"status":"PARTIAL_SOFT_STOP","failure_class":"HPC"})
    except Exception as exc:
        rec.update({"status":"FAILED","failure_class":"NUMERICAL_OR_LIKELIHOOD","error":repr(exc)})
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old)
        try:
            if sampler is not None and hasattr(sampler,"close"): sampler.close()
        except Exception: pass
    write_json(output,rec)
    return 0 if rec["status"]=="COMPLETE" else 2

def collect_profiles(path: str|Path):
    rows=[]
    for p in Path(path).rglob("*.json"):
        try:d=json.loads(p.read_text())
        except Exception:continue
        if d.get("q")==Q and d.get("run_id")==RUN and d.get("stage")=="BRIDGE_PROFILE":
            rows.append(d)
    return rows

def aggregate(c, input_dir, output):
    rows=collect_profiles(input_dir)
    best={}
    stability={}
    for bridge in BRIDGES:
        for ep in ENDPOINTS:
            cand=[r for r in rows if r.get("bridge")==bridge and r.get("endpoint")==ep
                  and r.get("status")=="COMPLETE" and finite(r.get("objective_chi2"))]
            cand=sorted(cand,key=lambda x:float(x["objective_chi2"]))
            key=f"{bridge}:{ep}"
            if cand:
                best[key]=cand[0]
                vals=[float(x["objective_chi2"]) for x in cand]
                stability[key]={"complete":len(vals),"best_two_spread":
                    (vals[1]-vals[0]) if len(vals)>1 else None}
    penalties={}
    for bridge in BRIDGES:
        a=best.get(f"{bridge}:reference_free_h0")
        b=best.get(f"{bridge}:fixed_h0_71p5")
        if a and b:
            penalties[bridge]=float(b["objective_chi2"])-float(a["objective_chi2"])

    lite=float(c["references"]["q016_lite_penalty"])
    full=float(c["references"]["q017_full_mf_penalty"])
    out={
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"MERGED",
        "status":"COMPLETE" if len(penalties)==len(BRIDGES) else "PARTIAL",
        "authoritative_reference_penalties":{
            "q016_lite":lite,"q017_full_mf":full,
            "architecture_gap_not_a_physical_chi2_component":full-lite
        },
        "computed_bridge_penalties":penalties,
        "stability":stability,
        "interpretation_rules":{
            "penalties_are_surface_diagnostics_not_independent_tests":True,
            "lock_surfaces_are_not_additive_components":True,
            "frequency_covariance_foreground_architecture_may_be_inseparable":True,
            "no_causal_systematic_claim":True
        },
        "actual_computed_result":bool(penalties)
    }
    write_json(output,out)
    return 0 if out["status"]=="COMPLETE" else 2

def make_plan(c, output):
    matrix=[{"bridge":b,"endpoint":e,"restart":r}
            for b in BRIDGES for e in ENDPOINTS
            for r in range(int(c["execution"]["restarts"]))]
    write_json(output,{
        "q":Q,"run_id":RUN,"result_id":RESULT,"stage":"PLAN","status":"PASS",
        "matrix":{"include":matrix},"expected_profile_jobs":len(matrix),
        "execution_strategy":"PARALLEL_ATOMIC_NUISANCE_PROFILES_THEN_DETERMINISTIC_MERGE",
        "checkpointing":False,
        "checkpoint_reason":"Independent BOBYQA nuisance profiles; no reliable serialized optimizer state required."
    })
    return 0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("plan"); p.add_argument("--output",required=True)
    p=sp.add_parser("profile")
    p.add_argument("--endpoint",required=True,choices=ENDPOINTS)
    p.add_argument("--bridge",required=True,choices=BRIDGES)
    p.add_argument("--restart",required=True,type=int); p.add_argument("--output",required=True)
    p=sp.add_parser("aggregate"); p.add_argument("--input-dir",required=True); p.add_argument("--output",required=True)
    a=ap.parse_args(); c=load_cfg(a.config); lock=load_q016_lock(c)
    if a.cmd=="plan": return make_plan(c,a.output)
    if a.cmd=="profile": return profile(c,lock,a.endpoint,a.restart,a.bridge,a.output)
    if a.cmd=="aggregate": return aggregate(c,a.input_dir,a.output)
    raise RuntimeError("COMMAND_GATE=FAIL")
if __name__=="__main__": raise SystemExit(main())
