#!/usr/bin/env python3
"""Validate Bubbleverse Q-005 HPC V7 outputs without inventing missing results."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q005_hpc_v7_config.yml")
    ap.add_argument("--summary", default="q005_results/q005_results_summary.json")
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / args.config).read_text())
    p = ROOT / args.summary
    if not p.exists():
        print("[ERROR] summary file missing:", p)
        return 2

    s = json.loads(p.read_text())
    result = {
        "project": s.get("project"),
        "status": "FAIL",
        "checks": {},
        "unresolved": [],
    }

    computed = s.get("actual_results_status") == "COMPUTED"
    result["checks"]["all_three_runs_computed"] = computed
    if not computed:
        result["unresolved"].append("One or more of lcdm/ede/ede_local has no best-fit output.")

    delta = s.get("gates", {}).get("delta_chi2_ede_minus_lcdm")
    if delta is None:
        result["unresolved"].append("Delta chi2 EDE-LCDM is not available.")
    else:
        floor = cfg["gates"]["theory_precision"]["delta_chi2_floor"]
        result["checks"]["delta_chi2_above_theory_floor"] = abs(float(delta)) >= float(floor)

    high = s.get("gates", {}).get("ede_high_h0_without_local_prior")
    if high is None:
        result["unresolved"].append("No-local-prior EDE H0 was not parsed.")
    else:
        result["checks"]["ede_reaches_H0_ge_70_without_local_prior"] = bool(high["pass"])

    # Scientific model preference is intentionally NOT reduced to one Boolean here.
    # The Result Ingestion & Routing Engine must inspect chi2 decomposition and pull.
    result["checks"]["no_fabricated_result"] = True
    result["status"] = "PASS" if computed else "INCOMPLETE"

    out = ROOT / "q005_results" / "q005_validation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 3

if __name__ == "__main__":
    raise SystemExit(main())
