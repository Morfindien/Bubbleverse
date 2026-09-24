#!/usr/bin/env python3
"""Bubbleverse Q042 V1 — V19 artifact diagnosis and execution-mechanism decision.

Artifact-only. It never emits a Q041 physical portability classification.
"""
from __future__ import annotations
import argparse, json, math, statistics, hashlib
from pathlib import Path
from typing import Any
import numpy as np

Q="Q-042"
PROGRAM_ID="Q042-EXECMECH-V1"
RUN_ID="Q042-EXECUTION-MECHANISM-DIAGNOSTIC-V1"
RESULT_ID="R-Q042-EXECUTION-MECHANISM-DIAGNOSTIC-001"
CORE=("omega_b","omega_cdm","fEDE","log10z_c","thetai_scf","H0")
FULL="P_A6_L6_D2"

def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write_json(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
def sha256(p):
    h=hashlib.sha256();
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def parse_progress(p:Path):
    rec=[]
    for line in p.read_text(encoding="utf-8").splitlines():
        s=line.strip()
        if not s or s.startswith("#"): continue
        a=s.split()
        try: rec.append({"N":float(a[0]),"timestamp":a[1],"acceptance_rate":float(a[2]),"Rminus1":float(a[3])})
        except Exception: continue
    if not rec: raise RuntimeError(f"PROGRESS_PARSE_GATE=FAIL path={p}")
    return rec

def parse_chain(p:Path):
    lines=p.read_text(encoding="utf-8").splitlines()
    if len(lines)<2: raise RuntimeError(f"CHAIN_PARSE_GATE=FAIL path={p}")
    names=lines[0].lstrip("#").split()
    arr=np.loadtxt(lines[1:])
    if arr.ndim==1: arr=arr[None,:]
    if arr.shape[1]!=len(names): raise RuntimeError(f"CHAIN_COLUMN_GATE=FAIL path={p}")
    return names,arr

def weighted_quantile(x,w,q):
    order=np.argsort(x); xs=x[order]; ws=w[order]
    c=np.cumsum(ws)/np.sum(ws)
    return float(np.interp(q,c,xs))

def chain_stats(path:Path):
    names,a=parse_chain(path); idx={n:i for i,n in enumerate(names)}
    for n in ("weight",)+CORE:
        if n not in idx: raise RuntimeError(f"CHAIN_REQUIRED_COLUMN_GATE=FAIL missing={n} path={path}")
    w=a[:,idx["weight"]]
    out={}
    for c in CORE:
        x=a[:,idx[c]]; mu=float(np.average(x,weights=w)); var=float(np.average((x-mu)**2,weights=w))
        out[c]={"mean":mu,"sd":math.sqrt(max(var,0.0)),"q95":weighted_quantile(x,w,0.95)}
    theta=a[:,idx["thetai_scf"]]
    out["theta_boundary_fraction_gt_3p05"]=float(w[theta>3.05].sum()/w.sum())
    out["sample_rows"]=int(a.shape[0]); out["weight_sum"]=float(w.sum())
    return out

def load_contract(prereg_path,lock_path):
    p=read_json(prereg_path); l=read_json(lock_path)
    if p.get("q")!=Q or p.get("program_id")!=PROGRAM_ID: raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if l.get("q")!=Q or l.get("program_id")!=PROGRAM_ID: raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if l.get("preregister_sha256")!=sha256(prereg_path): raise RuntimeError("PREREGISTRATION_HASH_GATE=FAIL")
    if l.get("external",{}).get("supernova",{}).get("component")!="sn.pantheonplus": raise RuntimeError("SUPERNOVA_SOURCE_LOCK_GATE=FAIL")
    if set(l.get("forbidden_scientific_inputs",[]))!={"Q040-CMBSPACE-*","Q040-RQMC-*"}: raise RuntimeError("Q040_FIREWALL_GATE=FAIL")
    return p,l

def diagnose(args):
    prereg,lock=load_contract(args.preregister,args.source_lock)
    root=Path(args.artifacts_dir)
    metas=sorted(root.rglob("q041_chain_metadata_v19.json"))
    if len(metas)!=32: raise RuntimeError(f"V19_ARTIFACT_COUNT_GATE=FAIL found={len(metas)} expected=32")
    rows=[]; full={}
    seen=set()
    for mp in metas:
        m=read_json(mp)
        ident=(m.get("implementation"),m.get("combo"),int(m.get("chain",-1)))
        if ident in seen: raise RuntimeError(f"DUPLICATE_CHAIN_GATE=FAIL ident={ident}")
        seen.add(ident)
        if m.get("q")!="Q-041" or m.get("program_id")!="Q041-PLANCKPORT-V19" or str(m.get("series_id"))!="34979609004":
            raise RuntimeError(f"V19_PROVENANCE_GATE=FAIL ident={ident}")
        p=mp.parent/"chain.progress"; c=mp.parent/"chain.1.txt"
        if not p.is_file() or not c.is_file(): raise RuntimeError(f"V19_REQUIRED_FILE_GATE=FAIL ident={ident}")
        prog=parse_progress(p); last=prog[-1]
        r={"implementation":ident[0],"combo":ident[1],"chain":ident[2],"status":m.get("status"),
           "failure_class":m.get("failure_class"),"Rminus1_last":last["Rminus1"],"acceptance_last":last["acceptance_rate"],
           "Rminus1_min":min(x["Rminus1"] for x in prog),"Rminus1_max":max(x["Rminus1"] for x in prog),"N_last":last["N"]}
        rows.append(r)
        if ident[1]==FULL: full[(ident[0],ident[2])]=chain_stats(c)
    if len(seen)!=32 or len(full)!=4: raise RuntimeError("V19_MATRIX_COMPLETENESS_DIAGNOSTIC_GATE=FAIL")
    thr=prereg["diagnostic_thresholds"]
    rlast=[x["Rminus1_last"] for x in rows]; acc=[x["acceptance_last"] for x in rows]
    counts={
      "total_chains":len(rows),"rminus1_last_le_1p05":sum(v<=thr["science_rhat_gate"] for v in rlast),
      "rminus1_last_le_2":sum(v<=2 for v in rlast),"rminus1_last_le_5":sum(v<=5 for v in rlast),
      "acceptance_last_ge_0p95":sum(v>=thr["high_acceptance_threshold"] for v in acc)
    }
    arms={}
    for arm in ("camspec","hillipop"):
        q=[x for x in rows if x["implementation"]==arm]
        arms[arm]={"median_acceptance_last":statistics.median(x["acceptance_last"] for x in q),
                   "median_rminus1_last":statistics.median(x["Rminus1_last"] for x in q),
                   "min_rminus1_last":min(x["Rminus1_last"] for x in q),"max_rminus1_last":max(x["Rminus1_last"] for x in q)}
    sep={}
    for arm in ("camspec","hillipop"):
        a,b=full[(arm,0)],full[(arm,1)]; sep[arm]={}
        for c in CORE:
            den=math.sqrt(0.5*(a[c]["sd"]**2+b[c]["sd"]**2))
            sep[arm][c]=abs(a[c]["mean"]-b[c]["mean"])/den if den>0 else float("inf")
    boundary={f"{arm}_c{ch}":full[(arm,ch)]["theta_boundary_fraction_gt_3p05"] for arm in ("camspec","hillipop") for ch in (0,1)}
    high_stuck=sum(1 for x in rows if x["acceptance_last"]>=thr["high_acceptance_threshold"] and x["Rminus1_last"]>thr["poor_transport_rminus1_threshold"])
    poor_convergence=counts["rminus1_last_le_1p05"]==0
    transport=(high_stuck/len(rows))>=thr["high_acceptance_fraction_threshold"]
    mode_or_ridge=max(v for a in sep.values() for v in a.values())>=thr["full_chain_standardized_separation_threshold"]
    boundary_flag=max(boundary.values())>=thr["theta_i_boundary_mass_threshold"]
    if poor_convergence and (transport or mode_or_ridge or boundary_flag):
        decision="REJECT_MORE_OF_SAME_MCMC__SELECT_POLYCHORD_PLUS_MULTISTART_BOBYQA"
    else:
        decision="UNRESOLVED_EXECUTION_MECHANISM"
    full_means={f"{arm}_c{ch}":{c:full[(arm,ch)][c]["mean"] for c in CORE} for arm in ("camspec","hillipop") for ch in (0,1)}
    out={
      "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"V19_EXECUTION_DIAGNOSIS",
      "status":"PASS" if decision.startswith("REJECT_") else "UNRESOLVED",
      "actual_computed_scientific_result":False,"scientific_classification":"NOT_AVAILABLE",
      "outcome_type":"EXECUTION_MECHANISM_DECISION_NOT_PHYSICAL_INFERENCE",
      "counts":counts,"arms":arms,"full_chain_means":full_means,"full_chain_standardized_separation":sep,
      "full_theta_boundary_fraction_gt_3p05":boundary,"high_acceptance_stuck_chains":high_stuck,
      "diagnostic_flags":{"poor_convergence":poor_convergence,"high_acceptance_local_transport":transport,"mode_or_ridge_structure":mode_or_ridge,"theta_boundary_structure":boundary_flag},
      "execution_decision":decision,"selected_strategy":prereg["prospective_execution_strategy"],
      "science_contract":prereg["authoritative_science_contract"],"original_decision_rule":prereg["original_decision_rule"],
      "supernova_source_lock":lock["external"]["supernova"],
      "claim_boundaries":{"unconverged_v19_values_are_diagnostic_only":True,"q040_scientific_products_used":False,"cross_arm_absolute_chi2_used":False,"v19_modified":False},
      "next_required_action":"Build a new Q042 full-science preflight/campaign using the selected sampler/optimizer strategy; first validate PolyChord installation, exact 20-cell construction, Pantheon+ runtime hashes, LCDM nesting, and representative finite evaluations. Do not start full sampling if that preflight fails."
    }
    write_json(args.output,out)
    print("Q042_EXECUTION_MECHANISM_GATE="+("PASS" if out["status"]=="PASS" else "UNRESOLVED"))
    print("Q042_EXECUTION_DECISION="+decision)
    return 0 if out["status"]=="PASS" else 2

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    d=sub.add_parser("diagnose"); d.add_argument("--artifacts-dir",required=True); d.add_argument("--preregister",required=True); d.add_argument("--source-lock",required=True); d.add_argument("--output",required=True)
    a=ap.parse_args(); return diagnose(a)
if __name__=="__main__": raise SystemExit(main())
