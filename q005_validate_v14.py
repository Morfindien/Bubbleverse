#!/usr/bin/env python3
"""Aggregate and validate Bubbleverse Q-005 HPC V14 results."""
from __future__ import annotations
import argparse
import json
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q005_hpc_v14_config.yml")
    ap.add_argument("--artifacts-root", default="q005_v14_aggregate")
    ap.add_argument("--output", default="q005_v14_aggregate/q005_hpc_v14_final_result.json")
    ap.add_argument("--restarts", type=int, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / args.config).read_text())
    base = ROOT / args.artifacts_root
    restarts = args.restarts or int(cfg["runtime_safety"]["default_restarts"])
    expected_models = list(cfg["runtime_safety"]["enabled_models"])

    source_lock = load(ROOT / cfg["source_lock_file"])
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
        "models": {},
        "comparisons": {},
        "gates": {},
        "warnings": [],
        "source_lock": source_lock,
    }

    completeness = True
    globality = True
    max_global = float(cfg["gates"]["globality"]["max_restart_delta_chi2"])

    for model in expected_models:
        rows = [x for x in by_model.get(model, []) if x.get("status") == "PASS"]
        rows.sort(key=lambda x: int(x.get("restart", 999)))
        expected_ids = set(range(restarts))
        got_ids = {int(x["restart"]) for x in rows}
        missing = sorted(expected_ids - got_ids)
        if missing:
            completeness = False

        if not rows:
            out["models"][model] = {"status": "NO_VALID_RESULTS", "missing_restarts": missing}
            continue

        ranked = sorted(rows, key=lambda x: float(x["chi2_scientific_total"]))
        best = ranked[0]
        chis = [float(x["chi2_scientific_total"]) for x in ranked]
        spread = max(chis) - min(chis) if len(chis) >= 2 else None
        global_pass = spread is not None and spread <= max_global
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
            "missing_restarts": missing,
        }

    out["gates"]["JOB_COMPLETENESS_GATE"] = "PASS" if completeness else "FAIL"
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
            out["comparisons"][model] = {
                "delta_chi2_vs_lcdm": dchi,
                "extra_parameters": k,
                "delta_AIC_vs_lcdm": daic,
                "H0": h0,
                "high_H0_gate_threshold": cfg["gates"]["high_h0_without_local_prior"]["threshold"],
                "high_H0_gate_pass": isinstance(h0, (int, float)) and
                    float(h0) >= float(cfg["gates"]["high_h0_without_local_prior"]["threshold"]),
            }

        n3 = out["models"]["ede_n3"]["bestfit"]
        n2 = out["models"]["ede_n2"]["bestfit"]
        out["comparisons"]["n3_vs_n2"] = {
            "delta_H0_n2_minus_n3":
                (float(n2["H0"]) - float(n3["H0"]))
                if isinstance(n2.get("H0"), (int, float)) and isinstance(n3.get("H0"), (int, float))
                else None,
            "delta_chi2_n2_minus_n3":
                float(out["models"]["ede_n2"]["chi2_scientific_total"]) -
                float(out["models"]["ede_n3"]["chi2_scientific_total"]),
            "interpretation_boundary":
                "This isolates the common-backend n=2 vs n=3 differential only; it does not by itself explain the full K-036/K-038 paper discrepancy."
        }

        # Boundary diagnostics
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

    # Nesting result if downloaded.
    nesting_files = sorted(base.rglob("q005_nesting_v14.json"))
    if nesting_files:
        nesting = load(nesting_files[0])
        out["nesting"] = nesting
        out["gates"]["NESTING_GATE"] = nesting.get("status", "FAIL")
    else:
        out["gates"]["NESTING_GATE"] = "MISSING"
        completeness = False

    # Optional H0DN re-optimizations.
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
        out["gates"].get("JOB_COMPLETENESS_GATE") == "PASS",
        out["gates"].get("GLOBALITY_GATE") == "PASS",
        out["gates"].get("NESTING_GATE") == "PASS",
        all(out["models"].get(m, {}).get("status") == "COMPUTED" for m in expected_models),
    ]
    if all(mandatory):
        out["status"] = "PASS_COMMON_BACKEND"
        out["gates"]["FINAL_RESULT_GATE"] = "PASS_COMMON_BACKEND_ONLY"
    elif any(out["models"].get(m, {}).get("status") == "COMPUTED" for m in expected_models):
        out["status"] = "UNRESOLVED"
        out["gates"]["FINAL_RESULT_GATE"] = "UNRESOLVED"
    else:
        out["status"] = "FAIL"
        out["gates"]["FINAL_RESULT_GATE"] = "FAIL"

    out["next_required_action"] = (
        "Return this common-backend result to Bubbleverse Result Ingestion & Routing. "
        "If the n=2/n=3 differential is small, the K-036/K-038 discrepancy must be sought "
        "primarily in likelihood/prior/statistical/backend differences. Exact paper-native "
        "claims remain blocked until native source provenance is frozen."
    )

    op = ROOT / args.output
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if out["status"] in ("PASS_COMMON_BACKEND", "UNRESOLVED") else 3


if __name__ == "__main__":
    raise SystemExit(main())
