#!/usr/bin/env python3
"""Aggregate and validate Bubbleverse Q-005 HPC V14 results.

FIX12 corrects requested-vs-effective restart accounting, while preserving FIX11 semantics.

FIX11 separates:
  - execution coverage: was every requested restart actually attempted/recorded?
  - valid restart quorum: are enough independent scientific minima usable?
  - globality: do the usable independent minima agree in chi2?

A technical optimizer failure is retained as evidence but is not itself a
scientific failure of the model.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_model(cfg: dict[str, Any], name: str) -> dict[str, Any]:
    m = dict(cfg["models"][name])
    if "inherit_model" in m:
        base = resolve_model(cfg, m["inherit_model"])
        base.update({k: v for k, v in m.items() if k != "inherit_model"})
        return base
    return m


def find_results(base: Path) -> list[Path]:
    return sorted(base.rglob("q005_job_result_*.json"))


def compact_failure(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "restart": row.get("restart"),
        "seed": row.get("seed"),
        "status": row.get("status"),
        "reason": row.get("reason"),
        "technical_status": row.get("technical_status"),
        "scientific_status": row.get("scientific_status"),
        "optimizer_diagnostic": row.get("optimizer_diagnostic"),
    }


def required_valid_count(cfg: dict[str, Any], restarts: int) -> int:
    if restarts <= 1:
        return 1
    policy = cfg["runtime_safety"]["restart_result_policy"]
    absolute = int(policy["minimum_valid_restarts"])
    fractional = int(math.ceil(float(policy["minimum_valid_fraction"]) * restarts))
    return min(restarts, max(absolute, fractional))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q005_hpc_v14_config.yml")
    ap.add_argument("--artifacts-root", default="q005_v14_aggregate")
    ap.add_argument("--output", default="q005_v14_aggregate/q005_hpc_v14_final_result.json")
    ap.add_argument("--restarts", type=int, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8"))
    base = ROOT / args.artifacts_root
    requested_restarts = args.restarts or int(cfg["runtime_safety"]["default_restarts"])
    max_restarts = int(cfg["runtime_safety"]["max_restarts"])
    restarts = max(1, min(int(requested_restarts), max_restarts))
    expected_models = list(cfg["runtime_safety"]["enabled_models"])
    required_valid = required_valid_count(cfg, restarts)

    source_lock_path = ROOT / cfg["source_lock_file"]
    source_lock = load(source_lock_path) if source_lock_path.exists() else {
        "status": "MISSING_SOURCE_LOCK"
    }

    files = find_results(base)
    by_model: dict[str, list[dict[str, Any]]] = {}
    for p in files:
        try:
            d = load(p)
        except Exception:
            continue
        if d.get("q") != "Q-005" or d.get("project") != cfg["project"]["id"]:
            continue
        by_model.setdefault(d.get("model", "UNKNOWN"), []).append(d)

    out: dict[str, Any] = {
        "q": "Q-005",
        "project": cfg["project"]["id"],
        "result_class": "COMMON_BACKEND_DIFFERENTIAL",
        "paper_native_reproduction_gate": "BLOCKED_SOURCE_PROVENANCE",
        "status": "FAIL",
        "restart_policy": {
            "requested_restarts_per_model": int(requested_restarts),
            "effective_restarts_per_model": restarts,
            "max_restarts_per_model": max_restarts,
            "requested_restarts_capped": int(requested_restarts) != restarts,
            "required_valid_restarts_per_model": required_valid,
            "coverage_definition": "ONE_MACHINE_READABLE_RECORD_PER_EFFECTIVE_RESTART",
            "valid_definition": "status=PASS AND finite scientific result",
            "technical_failure_semantics":
                "RETAINED_AS_TECHNICAL_EVIDENCE_NOT_AUTOMATIC_MODEL_FAILURE",
        },
        "models": {},
        "comparisons": {},
        "gates": {},
        "warnings": [],
        "source_lock": source_lock,
    }

    execution_coverage = True
    valid_quorum = True
    globality = True
    max_global = float(cfg["gates"]["globality"]["max_restart_delta_chi2"])

    for model in expected_models:
        all_rows = [
            x for x in by_model.get(model, [])
            if isinstance(x.get("restart"), int)
            and 0 <= int(x["restart"]) < restarts
        ]

        # One canonical record per restart. Duplicate records are reported, not hidden.
        grouped: dict[int, list[dict[str, Any]]] = {}
        for x in all_rows:
            grouped.setdefault(int(x["restart"]), []).append(x)
        duplicate_ids = sorted(r for r, xs in grouped.items() if len(xs) > 1)
        if duplicate_ids:
            out["warnings"].append(
                f"{model}: duplicate restart records for {duplicate_ids}; using last sorted record"
            )

        rows_by_restart = {r: xs[-1] for r, xs in grouped.items()}
        expected_ids = set(range(restarts))
        attempted_ids = set(rows_by_restart)
        missing_records = sorted(expected_ids - attempted_ids)
        coverage_pass = not missing_records
        if not coverage_pass:
            execution_coverage = False

        rows = [
            x for r, x in sorted(rows_by_restart.items())
            if x.get("status") == "PASS"
        ]
        failures = [
            compact_failure(x) for r, x in sorted(rows_by_restart.items())
            if x.get("status") != "PASS"
        ]

        quorum_pass = len(rows) >= required_valid
        if not quorum_pass:
            valid_quorum = False

        if not rows:
            out["models"][model] = {
                "status": "NO_VALID_RESULTS",
                "attempted_restart_ids": sorted(attempted_ids),
                "valid_restart_ids": [],
                "missing_restart_records": missing_records,
                "technical_or_invalid_failures": failures,
                "execution_coverage_pass": coverage_pass,
                "valid_restart_quorum_pass": False,
                "required_valid_restarts": required_valid,
                "globality_pass": False,
            }
            globality = False
            continue

        ranked = sorted(rows, key=lambda x: float(x["chi2_scientific_total"]))
        best = ranked[0]
        chis = [float(x["chi2_scientific_total"]) for x in ranked]
        spread = max(chis) - min(chis) if len(chis) >= 2 else None

        # A single valid point is not a globality test.
        global_pass = (
            quorum_pass
            and len(chis) >= 2
            and spread is not None
            and math.isfinite(spread)
            and spread <= max_global
        )
        if not global_pass:
            globality = False

        out["models"][model] = {
            "status": "COMPUTED",
            "selected_restart": best["restart"],
            "selected_seed": best["seed"],
            "chi2_scientific_total": best["chi2_scientific_total"],
            "bestfit": best["bestfit"],
            "restart_spread_chi2": spread,
            "globality_pass": global_pass,
            "attempted_restart_ids": sorted(attempted_ids),
            "valid_restart_ids": sorted(int(x["restart"]) for x in rows),
            "valid_restart_count": len(rows),
            "required_valid_restarts": required_valid,
            "valid_restart_quorum_pass": quorum_pass,
            "missing_restart_records": missing_records,
            "execution_coverage_pass": coverage_pass,
            "technical_or_invalid_failures": failures,
            "duplicate_restart_ids": duplicate_ids,
        }

        if failures:
            out["warnings"].append(
                f"{model}: {len(failures)} restart(s) produced no valid scientific minimum; "
                "retained in technical failure journal"
            )

    out["gates"]["JOB_EXECUTION_COVERAGE_GATE"] = (
        "PASS" if execution_coverage else "FAIL"
    )
    out["gates"]["VALID_RESTART_QUORUM_GATE"] = (
        "PASS" if valid_quorum else "FAIL"
    )
    # Backward-compatible summary name: complete means attempted + enough usable results.
    out["gates"]["JOB_COMPLETENESS_GATE"] = (
        "PASS" if execution_coverage and valid_quorum else "FAIL"
    )
    out["gates"]["GLOBALITY_GATE"] = "PASS" if globality else "UNRESOLVED"

    if all(out["models"].get(m, {}).get("status") == "COMPUTED" for m in expected_models):
        base_model = out["models"]["lcdm"]
        base_chi = float(base_model["chi2_scientific_total"])

        for model in ["ede_n3", "ede_n2", "me_common"]:
            r = out["models"][model]
            dchi = float(r["chi2_scientific_total"]) - base_chi
            k = int(resolve_model(cfg, model).get("extra_parameter_count", 0))
            daic = dchi + 2 * k
            h0 = r["bestfit"].get("H0")
            threshold = float(cfg["gates"]["high_h0_without_local_prior"]["threshold"])
            out["comparisons"][model] = {
                "delta_chi2_vs_lcdm": dchi,
                "extra_parameters": k,
                "delta_AIC_vs_lcdm": daic,
                "H0": h0,
                "high_H0_gate_threshold": threshold,
                "high_H0_gate_pass":
                    isinstance(h0, (int, float)) and float(h0) >= threshold,
            }

        n3 = out["models"]["ede_n3"]["bestfit"]
        n2 = out["models"]["ede_n2"]["bestfit"]
        out["comparisons"]["n3_vs_n2"] = {
            "delta_H0_n2_minus_n3":
                (float(n2["H0"]) - float(n3["H0"]))
                if isinstance(n2.get("H0"), (int, float))
                and isinstance(n3.get("H0"), (int, float))
                else None,
            "delta_chi2_n2_minus_n3":
                float(out["models"]["ede_n2"]["chi2_scientific_total"])
                - float(out["models"]["ede_n3"]["chi2_scientific_total"]),
            "interpretation_boundary":
                "This isolates the common-backend n=2 vs n=3 differential only; "
                "it does not by itself explain the full K-036/K-038 paper discrepancy."
        }

        for model in ("ede_n3", "ede_n2"):
            b = out["models"][model]["bestfit"]
            f = b.get("fEDE")
            z = b.get("log10z_c")
            th = b.get("thetai_scf")
            flags = []
            if isinstance(f, (int, float)) and (float(f) < 0.002 or float(f) > 0.298):
                flags.append("fEDE_NEAR_BOUNDARY")
            if isinstance(z, (int, float)) and (float(z) < 3.02 or float(z) > 4.28):
                flags.append("log10z_c_NEAR_BOUNDARY")
            if isinstance(th, (int, float)) and (float(th) < 0.12 or float(th) > 3.08):
                flags.append("thetai_scf_NEAR_BOUNDARY")
            out["models"][model]["boundary_flags"] = flags

    nesting_files = sorted(base.rglob("q005_nesting_v14.json"))
    if nesting_files:
        nesting = load(nesting_files[0])
        out["nesting"] = nesting
        out["gates"]["NESTING_GATE"] = nesting.get("status", "FAIL")
    else:
        out["gates"]["NESTING_GATE"] = "MISSING"
        execution_coverage = False
        out["gates"]["JOB_EXECUTION_COVERAGE_GATE"] = "FAIL"
        out["gates"]["JOB_COMPLETENESS_GATE"] = "FAIL"

    # Optional H0DN re-optimizations. They remain additional evidence, not a
    # prerequisite unless present and explicitly requested by the workflow.
    h0_pairs = {
        "lcdm": "lcdm_h0dn",
        "ede_n3": "ede_n3_h0dn",
        "ede_n2": "ede_n2_h0dn",
        "me_common": "me_common_h0dn",
    }
    h0_tests = {}
    required_nonlocal = set(cfg["likelihood_accounting"]["required_nonlocal"])
    for base_name, local_name in h0_pairs.items():
        local_rows = [x for x in by_model.get(local_name, []) if x.get("status") == "PASS"]
        if not local_rows or out["models"].get(base_name, {}).get("status") != "COMPUTED":
            continue
        local = min(local_rows, key=lambda x: float(x["chi2_scientific_total"]))
        comps = local["bestfit"].get("chi2_nonoverlap", {})
        if "h0dn" not in comps or not required_nonlocal.issubset(comps):
            continue
        local_cosmo = sum(float(comps[k]) for k in required_nonlocal)
        base_cosmo = float(out["models"][base_name]["chi2_scientific_total"])
        h0_tests[base_name] = {
            "H0_reoptimized": local["bestfit"].get("H0"),
            "delta_cosmology_chi2_after_adding_H0DN": local_cosmo - base_cosmo,
            "H0DN_chi2_at_reoptimized_point": float(comps["h0dn"]),
            "total_with_H0DN": float(local["chi2_scientific_total"]),
        }
    if h0_tests:
        out["h0dn_external_reoptimization"] = h0_tests

    mandatory = [
        out["gates"].get("JOB_EXECUTION_COVERAGE_GATE") == "PASS",
        out["gates"].get("VALID_RESTART_QUORUM_GATE") == "PASS",
        out["gates"].get("GLOBALITY_GATE") == "PASS",
        out["gates"].get("NESTING_GATE") == "PASS",
        all(out["models"].get(m, {}).get("status") == "COMPUTED"
            for m in expected_models),
    ]

    if all(mandatory):
        out["status"] = "PASS_COMMON_BACKEND"
        out["gates"]["FINAL_RESULT_GATE"] = "PASS_COMMON_BACKEND_ONLY"
    elif any(out["models"].get(m, {}).get("status") == "COMPUTED"
             for m in expected_models):
        out["status"] = "UNRESOLVED"
        out["gates"]["FINAL_RESULT_GATE"] = "UNRESOLVED"
    else:
        out["status"] = "FAIL"
        out["gates"]["FINAL_RESULT_GATE"] = "FAIL"

    out["next_required_action"] = (
        "Return this common-backend result to Bubbleverse Result Ingestion & Routing. "
        "Technical restart failures remain in the journal and must not be interpreted "
        "as scientific model rejection. If the n=2/n=3 differential is small, the "
        "K-036/K-038 discrepancy must be sought primarily in likelihood/prior/"
        "statistical/backend differences. Exact paper-native claims remain blocked "
        "until native source provenance is frozen."
    )

    op = ROOT / args.output
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if out["status"] in ("PASS_COMMON_BACKEND", "UNRESOLVED") else 3


if __name__ == "__main__":
    raise SystemExit(main())
