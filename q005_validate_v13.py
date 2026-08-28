#!/usr/bin/env python3
"""Aggregate and validate Bubbleverse Q-005 HPC V13 split-restart outputs. Smoke is single-evaluate only."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
MODELS = ("lcdm", "ede", "ede_local")
RESTARTS = (0, 1)
REQ = ("planck_lowl", "act_dr6", "desi_dr2", "bbn")

def parse_onepoint(path: Path):
    lines=[x.strip() for x in path.read_text(errors="replace").splitlines() if x.strip()]
    if len(lines)<2: return {"parse_status":"INSUFFICIENT_LINES","raw_file":str(path)}
    h=lines[0].lstrip("#").split(); v=lines[-1].split()
    if len(h)!=len(v): return {"parse_status":"COLUMN_MISMATCH","raw_file":str(path)}
    d={"parse_status":"PASS","raw_file":str(path)}
    for k,x in zip(h,v):
        try:d[k]=float(x)
        except ValueError:d[k]=x
    aliases={
      "planck_lowl":["chi2__planck_2018_lowl.EE_sroll2"],
      "act_dr6":["chi2__act_dr6_cmbonly.ACTDR6CMBonly"],
      "desi_dr2":["chi2__bao.desi_dr2"],
      "bbn":["chi2__bbn_omega_b"],
      "h0dn":["chi2__h0dn"],
    }
    c={}
    for label,keys in aliases.items():
        for k in keys:
            if isinstance(d.get(k),(int,float)):
                c[label]=float(d[k]); break
    d["chi2_nonoverlap"]=c
    return d

def find_restart_bestfit(base: Path, model: str, restart: int):
    found=[]
    for pat in (f"{model}_r{restart}.bestfit.txt", f"{model}_r{restart}.minimum.txt"):
        found.extend(base.rglob(pat))
    return sorted(found)[0] if found else None

def valid_restart(d, model):
    if d.get("parse_status")!="PASS": return False, "parse failure"
    c=d.get("chi2_nonoverlap",{})
    required=set(REQ)|({"h0dn"} if model=="ede_local" else set())
    if not required.issubset(c): return False, f"missing terms {sorted(required-set(c))}"
    if model!="ede_local" and "h0dn" in c: return False, "unexpected H0DN term"
    expected=sum(c[k] for k in required)
    d["chi2_scientific_total"]=expected
    raw=d.get("chi2")
    if isinstance(raw,(int,float)) and abs(float(raw)-expected)>1e-4:
        return False, f"non-overlap sum {expected} != Cobaya chi2 {raw}"
    return True, "PASS"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",default="q005_hpc_v13_config.yml")
    ap.add_argument("--artifacts-root",default="q005_aggregate")
    ap.add_argument("--output",default="q005_aggregate/q005_validation_v11.json")
    a=ap.parse_args()
    cfg=yaml.safe_load((ROOT/a.config).read_text())
    base=ROOT/a.artifacts_root
    out={"project":"Q-005-HPC-V13","bubbleverse_q":"Q-005",
         "question":cfg["q_memory"]["original_question"],"status":"FAIL",
         "models":{},"checks":{},"gates":{},"restart_policy":cfg["runtime_safety"],
         "v9_status":"PRELIMINARY_NOT_DISCARDED"}
    all_restarts_present=True; model_ok=True
    for model in MODELS:
        candidates=[]; records=[]
        for rid in RESTARTS:
            fp=find_restart_bestfit(base,model,rid)
            if fp is None:
                records.append({"restart":rid,"status":"MISSING"})
                all_restarts_present=False; continue
            d=parse_onepoint(fp); ok,reason=valid_restart(d,model)
            records.append({"restart":rid,"seed":1701+rid,"status":"VALID" if ok else "INVALID",
                            "reason":reason,"file":str(fp),"bestfit":d})
            if ok:candidates.append((float(d["chi2_scientific_total"]),rid,d,fp))
        if not candidates:
            out["models"][model]={"status":"NO_VALID_RESTART","restarts":records}
            model_ok=False; continue
        candidates.sort(key=lambda x:x[0])
        chi,rid,best,fp=candidates[0]
        out["models"][model]={"status":"COMPUTED","selected_restart":rid,"selected_seed":1701+rid,
            "selected_file":str(fp),"selected_chi2_scientific_total":chi,"bestfit":best,"restarts":records}
    out["checks"]["all_six_restarts_present"]=all_restarts_present
    out["checks"]["at_least_one_valid_restart_per_model"]=model_ok
    if model_ok:
        L=out["models"]["lcdm"]["bestfit"]; E=out["models"]["ede"]["bestfit"]; EL=out["models"]["ede_local"]["bestfit"]
        dl=E["chi2_scientific_total"]-L["chi2_scientific_total"]
        out["gates"]["delta_chi2_ede_minus_lcdm"]=dl
        out["gates"]["ede_high_h0_without_local_prior"]={"threshold":70.0,"value":E.get("H0"),
            "pass":isinstance(E.get("H0"),(int,float)) and E["H0"]>=70.0}
        out["checks"]["h0dn_active_in_ede_local"]="h0dn" in EL["chi2_nonoverlap"]
        keys=("H0","omega_b","omega_cdm","fraction_axion_ac","log10_axion_ac")
        same=all(E.get(k)==EL.get(k) for k in keys)
        out["checks"]["ede_local_optimum_distinct_from_ede"]=not same
        if same: out.setdefault("warnings",[]).append("Selected EDE and EDE_LOCAL optima are exactly identical; inspect restart logs.")
        out["checks"]["delta_chi2_above_theory_floor"]=abs(dl)>=float(cfg["gates"]["theory_precision"]["delta_chi2_floor"])
    if model_ok and all_restarts_present and out["checks"].get("h0dn_active_in_ede_local",False):
        out["status"]="PASS"
    elif model_ok:
        out["status"]="PARTIAL"
    else:
        out["status"]="FAIL"
    op=ROOT/a.output; op.parent.mkdir(parents=True,exist_ok=True)
    op.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return 0 if out["status"] in ("PASS","PARTIAL") else 3

if __name__=="__main__":
    raise SystemExit(main())
