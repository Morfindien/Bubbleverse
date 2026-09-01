#!/usr/bin/env python3
"""Q014 V6 aggregator wrapper over frozen V5 aggregation logic."""
from __future__ import annotations
import json, math
from pathlib import Path
import q014_aggregate_v5 as impl

impl.CONFIG_NAME = "q014_external_viability_v5_config.yml"
V6_RUN = "Q014-EXTERNAL-VIABILITY-V6"
V6_RESULT = "R-Q014-EDE-EXTERNAL-VIABILITY-003"

def _load_records(paths):
    out=[]
    for raw in paths:
        p=Path(raw)
        candidates=list(p.rglob("*.json")) if p.is_dir() else [p]
        for f in candidates:
            try: d=json.loads(f.read_text())
            except Exception: continue
            if d.get("q")=="Q014" and d.get("run_id")==V6_RUN and "mode" in d:
                d["_source_file"]=str(f); out.append(d)
    return out

_original_aggregate = impl.aggregate

def _aggregate(records, c, depth):
    r=_original_aggregate(records,c,depth)
    r["run_id"]=V6_RUN
    r["result_id"]=V6_RESULT
    r["program_status"]="V6 EXECUTION RESULTS AGGREGATED"
    j=r.get("journal_update",{})
    j["program"]="q014_external_viability_v6.py"
    j["workflow"]="q014-external-viability-v6.yml"
    r["v6_execution_repair"]={
      "scientific_surface":"BYTE-FOR-BYTE V5 CONFIG/LIKELIHOOD SURFACE REUSED",
      "muse_distribution":"single frozen source artifact, SHA256 4933ceb993ceb92e48b2191b8ccb1595d182bc4bc3862c1fbad61d5f82136e9b",
      "shared_vector_max_evals":960,
      "v5_failed_run":33472696719,
    }
    return r

impl.load_records=_load_records
impl.aggregate=_aggregate

if __name__=="__main__":
    raise SystemExit(impl.main())
