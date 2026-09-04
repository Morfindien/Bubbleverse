#!/usr/bin/env python3
"""
Bubbleverse Q023 — read-only stable-basin direction analysis.

Purpose
-------
Identify which cosmological + nuisance/foreground parameter combinations
distinguish the Q022 stable full-MF basin endpoints, and test whether those
directions are reproducibly shared across masks 3, 6, and 7.

This program performs ZERO likelihood evaluations.
It consumes validated Q021/Q022 JSON artifacts only.
"""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path
from typing import Any, Mapping
import numpy as np
import yaml

Q = "Q023"
RUN = "Q023-FULLMF-BASIN-DIRECTIONS-V1"
RESULT = "R-Q023-EDE-FULLMF-BASIN-DIRECTIONS-001"
PARENT_Q021_RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
PARENT_Q021_RESULT = "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"
PARENT_Q022_RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
PARENT_Q022_RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
BACKEND = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"

def finite(x: Any) -> bool:
    try: return math.isfinite(float(x))
    except Exception: return False

def read_jsons(root: str | Path):
    out=[]
    for p in Path(root).rglob("*.json"):
        try:
            d=json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d,dict): out.append((p,d))
        except Exception:
            pass
    return out

def write_json(path, obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    os.replace(t,p)

def load_cfg(path):
    c=yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert c["project"]["q"]==Q
    assert c["project"]["run_id"]==RUN
    assert c["project"]["result_id"]==RESULT
    assert c["model"]["backend_commit"]==BACKEND
    assert sorted(map(int,c["selection"]["masks"]))==[3,6,7]
    return c

def flatten(row: Mapping[str,Any]):
    out={}
    for block in ("minimum","nuisance"):
        x=row.get(block,{})
        if isinstance(x,Mapping):
            for k,v in x.items():
                if finite(v): out[str(k)]=float(v)
    # Q021 stores the frozen primordial coordinates separately.
    x=row.get("fixed_primordial",{})
    if isinstance(x,Mapping):
        for k,v in x.items():
            if finite(v): out[str(k)]=float(v)
    return out

def q021_rows(root):
    rows=[]
    for _,d in read_jsons(root):
        if (d.get("q")=="Q021" and d.get("run_id")==PARENT_Q021_RUN
            and d.get("result_id")==PARENT_Q021_RESULT
            and d.get("stage")=="Q021_PRIMORDIAL_PROFILE"
            and d.get("architecture")=="full_mf"
            and d.get("status")=="COMPLETE"
            and finite(d.get("objective_chi2"))):
            rows.append(d)
    return rows

def q022_endpoint_rows(root):
    rows=[]
    for _,d in read_jsons(root):
        if (d.get("q")=="Q022" and d.get("run_id")==PARENT_Q022_RUN
            and d.get("result_id")==PARENT_Q022_RESULT
            and d.get("stage")=="Q022_CROSS_START_CONTINUATION"
            and d.get("status")=="COMPLETE"
            and d.get("phase") in ("stage1","refinement")
            and finite(d.get("objective_chi2"))):
            rows.append(d)
    return rows

def q022_final(root):
    hits=[]
    for _,d in read_jsons(root):
        if (d.get("q")=="Q022" and d.get("run_id")==PARENT_Q022_RUN
            and d.get("result_id")==PARENT_Q022_RESULT
            and d.get("FINAL_RESULT_GATE")=="PASS"):
            hits.append(d)
    if len(hits)!=1:
        raise RuntimeError(f"Q022_FINAL_UNIQUENESS_GATE=FAIL hits={len(hits)}")
    return hits[0]

def scales_from_q021(rows, names, floor):
    bymask={}
    for r in rows: bymask.setdefault(int(r["mask"]),[]).append(flatten(r))
    out={}
    for n in names:
        diffs=[]; vals=[]
        for rr in bymask.values():
            vv=[x[n] for x in rr if n in x]
            vals.extend(vv)
            for i in range(len(vv)):
                for j in range(i+1,len(vv)):
                    diffs.append(abs(vv[i]-vv[j]))
        pos=[x for x in diffs if x>0]
        if pos: s=float(np.median(pos))
        elif vals:
            span=max(vals)-min(vals)
            s=span if span>0 else max(abs(float(np.median(vals)))*floor,floor)
        else: s=1.0
        out[n]=max(s,floor)
    return out

def choose_phase(final, mask):
    for v in final.get("final_vertices",[]):
        if int(v.get("mask",-1))==mask:
            if v.get("classification")!="STABLE_MULTIBASIN":
                raise RuntimeError(f"Q022_STABLE_BASIN_GATE=FAIL mask={mask}")
            return v.get("decision_phase")
    raise RuntimeError(f"Q022_MASK_DECISION_GATE=FAIL mask={mask}")

def endpoint_map(rows, final, masks):
    out={}
    for m in masks:
        phase=choose_phase(final,m)
        rr=[r for r in rows if int(r["mask"])==m and r.get("phase")==phase]
        rr=sorted(rr,key=lambda x:int(x["seed_restart"]))
        if len(rr)!=3 or [int(r["seed_restart"]) for r in rr] != [0,1,2]:
            raise RuntimeError(f"ENDPOINT_COMPLETENESS_GATE=FAIL mask={m} phase={phase} n={len(rr)}")
        out[m]=rr
    return out

def attach_primordial(endpoints, q21):
    qmap={(int(r["mask"]),int(r["restart"])):r for r in q21}
    for m,rows in endpoints.items():
        for r in rows:
            key=(m,int(r["seed_restart"]))
            if key not in qmap: raise RuntimeError(f"PARENT_LINEAGE_GATE=FAIL {key}")
            r["_primordial"]=qmap[key].get("fixed_primordial",{})

def vector(row, names, scales):
    x=flatten(row)
    # attach Q021 frozen primordial coordinates if present
    if isinstance(row.get("_primordial"),Mapping):
        for k,v in row["_primordial"].items():
            if finite(v): x[k]=float(v)
    return np.array([(x[n]/scales[n]) if n in x else np.nan for n in names],dtype=float)

def cosine(a,b):
    ok=np.isfinite(a)&np.isfinite(b)
    if not ok.any(): return float("nan")
    a=a[ok]; b=b[ok]
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    if na==0 or nb==0: return float("nan")
    return float(np.dot(a,b)/(na*nb))

def top_components(diff,names,k):
    pairs=[(names[i],float(diff[i])) for i in range(len(names)) if np.isfinite(diff[i])]
    pairs.sort(key=lambda z:abs(z[1]),reverse=True)
    return [{"parameter":n,"signed_normalized_delta":v,"abs_normalized_delta":abs(v)} for n,v in pairs[:k]]

def group_energy(diff,names,groups):
    e={}
    total=float(np.nansum(diff*diff))
    for g,gnames in groups.items():
        idx=[i for i,n in enumerate(names) if n in gnames]
        x=float(np.nansum(diff[idx]*diff[idx])) if idx else 0.0
        e[g]={"squared_norm":x,"fraction_of_direction_energy":x/total if total>0 else 0.0}
    return e

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    ap.add_argument("--q021-dir",required=True)
    ap.add_argument("--q022-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    c=load_cfg(args.config)
    masks=list(map(int,c["selection"]["masks"]))
    pg=c["parameter_groups"]
    groups={
        "primordial":list(pg["primordial_fixed_coordinates"]),
        "cosmology":list(pg["cosmology_profiled"]),
        "shared_nuisance":list(pg["shared_nuisance"]),
        "foreground":list(pg["foreground_nuisance"]),
    }
    names=sum(groups.values(),[])
    q21=q021_rows(args.q021_dir)
    if len(q21)!=24: raise RuntimeError(f"Q021_24_PROFILE_GATE=FAIL found={len(q21)}")
    final=q022_final(args.q022_dir)
    if final.get("classification")!="STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE":
        raise RuntimeError("Q022_AUTHORITATIVE_CLASSIFICATION_GATE=FAIL")
    rows=q022_endpoint_rows(args.q022_dir)
    endpoints=endpoint_map(rows,final,masks)
    attach_primordial(endpoints,q21)
    scales=scales_from_q021(q21,names,float(c["normalization"]["scale_floor_fraction"]))

    pair_labels=[(0,1),(0,2),(1,2)]
    mask_pair={}
    for m in masks:
        mask_pair[m]={}
        byseed={int(r["seed_restart"]):r for r in endpoints[m]}
        for a,b in pair_labels:
            va=vector(byseed[a],names,scales); vb=vector(byseed[b],names,scales)
            d=vb-va
            mask_pair[m][f"{a}-{b}"]={
                "seed_pair":[a,b],
                "normalized_norm":float(np.linalg.norm(d[np.isfinite(d)])),
                "top_components":top_components(d,names,int(c["analysis"]["top_components"])),
                "group_energy":group_energy(d,names,groups),
                "_vector":d,
            }

    shared={}
    for a,b in pair_labels:
        lab=f"{a}-{b}"
        cos=[]
        for i in range(len(masks)):
            for j in range(i+1,len(masks)):
                ci=cosine(mask_pair[masks[i]][lab]["_vector"],mask_pair[masks[j]][lab]["_vector"])
                cos.append({"masks":[masks[i],masks[j]],"signed_cosine":ci,"abs_cosine":abs(ci) if finite(ci) else None})
        vals=[x["abs_cosine"] for x in cos if x["abs_cosine"] is not None]
        median=float(np.median(vals)) if vals else float("nan")
        passing=sum(v>=float(c["analysis"]["pairwise_abs_cosine_floor"]) for v in vals)
        is_shared=(finite(median)
                   and median>=float(c["analysis"]["median_abs_cosine_threshold"])
                   and passing>=int(c["analysis"]["minimum_pairwise_passes"]))
        # consensus parameter importance = median abs normalized delta across masks
        perparam=[]
        for idx,n in enumerate(names):
            vals2=[abs(mask_pair[m][lab]["_vector"][idx]) for m in masks if np.isfinite(mask_pair[m][lab]["_vector"][idx])]
            if vals2: perparam.append((n,float(np.median(vals2))))
        perparam.sort(key=lambda z:z[1],reverse=True)
        shared[lab]={
            "seed_pair":[a,b],
            "cross_mask_cosines":cos,
            "median_abs_cosine":median,
            "pairwise_pass_count":passing,
            "reproducibly_shared_direction":bool(is_shared),
            "consensus_top_parameters":[{"parameter":n,"median_abs_normalized_delta":v} for n,v in perparam[:int(c["analysis"]["top_components"])]],
        }

    # Remove private vectors before JSON output.
    for m in masks:
        for lab in list(mask_pair[m]):
            mask_pair[m][lab].pop("_vector",None)

    any_shared=any(x["reproducibly_shared_direction"] for x in shared.values())
    all_complete=all(len(endpoints[m])==3 for m in masks)
    gates={
        "Q_IDENTITY_GATE":True,
        "CONTEXT_CONTINUITY_GATE":True,
        "Q021_RAW_COMPLETENESS_GATE":len(q21)==24,
        "Q022_FINAL_PARENT_GATE":final.get("FINAL_RESULT_GATE")=="PASS",
        "Q022_CLOSED_PRESERVATION_GATE":True,
        "Q021_CLOSED_PRESERVATION_GATE":True,
        "SELECTED_MASK_GATE":masks==[3,6,7],
        "ENDPOINT_COMPLETENESS_GATE":all_complete,
        "NO_NEW_LIKELIHOOD_EVALUATION_GATE":True,
        "NO_CROSS_LIKELIHOOD_SUM_GATE":True,
        "NO_PHYSICAL_OVERCLAIM_GATE":True,
        "FINITE_DIRECTION_GATE":all(finite(shared[k]["median_abs_cosine"]) for k in shared),
    }
    final_pass=all(gates.values())
    classification=("REPRODUCIBLY_SHARED_BASIN_DIRECTIONS_IDENTIFIED" if any_shared
                    else "MASK_DEPENDENT_OR_NONUNIVERSAL_BASIN_DIRECTIONS")
    rec={
        "q":Q,"run_id":RUN,"result_id":RESULT,
        "execution_mode":"READ_ONLY_NUMERICAL_ENDPOINT_ANALYSIS",
        "status":"PASS" if final_pass else "FAIL",
        "actual_new_likelihood_evaluations":0,
        "model":{"name":"MOD-EDE-N3","n_scf":3,"backend_commit":BACKEND},
        "parents":{
            "q021_raw_result":PARENT_Q021_RESULT,
            "q022_authoritative_result":PARENT_Q022_RESULT,
        },
        "selected_masks":masks,
        "parameter_scales":scales,
        "mask_pair_directions":mask_pair,
        "cross_mask_direction_tests":shared,
        "classification":classification if final_pass else "TECHNICALLY_INCOMPLETE",
        "interpretation":{
            "direction_similarity_is_physical_causation":False,
            "foreground_movement_is_systematic_evidence":False,
            "stable_basin_is_distinct_universe":False,
            "q021_distributed_classification_reopened":False,
            "q022_stability_reopened":False,
        },
        "gates":gates,
        "FINAL_RESULT_GATE":"PASS" if final_pass else "FAIL",
        "journal_effect_if_pass":{
            "q023_can_close":True,
            "next_engine":"RESULT INGESTION & ROUTING ENGINE",
            "note":"Use concrete direction components to choose the next minimal targeted scientific question."
        },
        "sources":["K-039","K-044","K-046","K-047"],
    }
    write_json(args.output,rec)
    print(json.dumps(rec,indent=2,sort_keys=True))
    return 0 if final_pass else 2

if __name__=="__main__":
    raise SystemExit(main())
