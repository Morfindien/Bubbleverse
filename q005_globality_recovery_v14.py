#!/usr/bin/env python3
"""Bubbleverse Q-005 V14 deterministic globality recovery.

This is a companion to q005_hpc_v14.py. It deliberately reuses the frozen V14
model/likelihood/source machinery and changes only optimizer starting references
and documented numerical refinement settings. It does NOT modify scientific
priors, bounds, datasets, likelihoods, physical model definitions, or claim
boundaries.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml

import q005_hpc_v14 as core

ROOT = Path(__file__).resolve().parent
DEFAULT_RECOVERY_CONFIG = "q005_globality_recovery_v14_config.yml"


def load_recovery(path: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def canonical_hash(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sampled_parameter_names(model: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for name, spec in model.get("params", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            names.add(name)
    for spec in model.get("likelihood", {}).values():
        if not isinstance(spec, dict):
            continue
        pmap = spec.get("params")
        if not isinstance(pmap, dict):
            continue
        for name, pspec in pmap.items():
            if isinstance(pspec, dict) and "prior" in pspec:
                names.add(name)
    return names


def prior_bounds(model: dict[str, Any]) -> dict[str, tuple[float, float]]:
    out: dict[str, tuple[float, float]] = {}
    blocks: list[dict[str, Any]] = [model.get("params", {})]
    for spec in model.get("likelihood", {}).values():
        if isinstance(spec, dict) and isinstance(spec.get("params"), dict):
            blocks.append(spec["params"])
    for block in blocks:
        for name, spec in block.items():
            if not isinstance(spec, dict):
                continue
            pr = spec.get("prior")
            if isinstance(pr, dict) and "min" in pr and "max" in pr:
                out[name] = (float(pr["min"]), float(pr["max"]))
    return out


def set_fixed_refs(model: dict[str, Any], refs: dict[str, float]) -> None:
    expected = sampled_parameter_names(model)
    supplied = set(refs)
    if supplied != expected:
        missing = sorted(expected - supplied)
        extra = sorted(supplied - expected)
        raise ValueError(f"Fixed-ref coverage mismatch: missing={missing}, extra={extra}")

    bounds = prior_bounds(model)
    for name, value in refs.items():
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"Non-finite ref {name}={value}")
        if name in bounds:
            lo, hi = bounds[name]
            if not (lo <= value <= hi):
                raise ValueError(f"Ref outside prior: {name}={value}, prior=[{lo},{hi}]")

    for name, spec in model.get("params", {}).items():
        if name in refs and isinstance(spec, dict) and "prior" in spec:
            spec["ref"] = float(refs[name])

    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict):
            continue
        pmap = lspec.get("params")
        if not isinstance(pmap, dict):
            continue
        for name, spec in pmap.items():
            if name in refs and isinstance(spec, dict) and "prior" in spec:
                spec["ref"] = float(refs[name])


def profile_entry(rcfg: dict[str, Any], model: str, profile: str) -> dict[str, Any]:
    try:
        return rcfg["profiles"][model][profile]
    except KeyError as exc:
        raise KeyError(f"Unknown recovery model/profile: {model}/{profile}") from exc


def plan(rcfg: dict[str, Any]) -> dict[str, Any]:
    include = []
    for model, profiles in rcfg["profiles"].items():
        for index, profile in enumerate(profiles):
            include.append({"model": model, "profile": profile, "profile_index": index})
    return {"include": include}


def build_recovery_model(base_cfg: dict[str, Any], rcfg: dict[str, Any],
                         model: str, profile: str, profile_index: int) -> dict[str, Any]:
    entry = profile_entry(rcfg, model, profile)
    obj = core.build_model(base_cfg, model, smoke=False, restart=0)
    refs = {k: float(v) for k, v in entry["refs"].items()}
    set_fixed_refs(obj, refs)

    opt = rcfg["optimizer_recovery"]
    minimize = obj["sampler"]["minimize"]
    minimize["seed"] = 62001 + int(profile_index)
    minimize["max_evals"] = int(opt["max_evals"])
    minimize["override_bobyqa"]["rhoend"] = float(opt["rhoend"])
    if base_cfg["models"][model].get("kind") == "ede":
        minimize["override_bobyqa"]["rhobeg"] = float(opt["ede_rhobeg"])

    out_prefix = ROOT / base_cfg["results_dir"] / f"globality_{model}_{profile}"
    obj["output"] = str(out_prefix.resolve())
    return obj


def render(base_cfg: dict[str, Any], rcfg: dict[str, Any], model: str,
           profile: str, profile_index: int) -> Path:
    d = ROOT / base_cfg["rendered_dir"]
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"q005_v14_globality_{model}_{profile}.yaml"
    obj = build_recovery_model(base_cfg, rcfg, model, profile, profile_index)
    p.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
    return p


def result_path(base_cfg: dict[str, Any], model: str, profile: str) -> Path:
    return ROOT / base_cfg["results_dir"] / f"q005_globality_result_{model}_{profile}.json"


def collect(base_cfg: dict[str, Any], rcfg: dict[str, Any], model: str,
            profile: str, profile_index: int, rendered: Path, exit_code: int) -> dict[str, Any]:
    entry = profile_entry(rcfg, model, profile)
    prefix = ROOT / base_cfg["results_dir"] / f"globality_{model}_{profile}"
    out: dict[str, Any] = {
        "q": "Q-005",
        "project": rcfg["project"]["id"],
        "parent_project": rcfg["project"]["parent_project"],
        "parent_github_run_id": rcfg["parent_result"]["github_run_id"],
        "model": model,
        "profile": profile,
        "profile_index": int(profile_index),
        "profile_role": entry["role"],
        "profile_provenance": entry["provenance"],
        "start_reference": entry["refs"],
        "start_reference_sha256": canonical_hash(entry["refs"]),
        "rendered_yaml": str(rendered),
        "rendered_yaml_sha256": core.sha256_file(rendered),
        "cobaya_exit": int(exit_code),
        "optimizer_recovery": rcfg["optimizer_recovery"],
        "claim_boundary": rcfg["frozen_claim_boundary"],
        "status": "FAIL",
    }

    one = core.find_onepoint(prefix)
    if exit_code == 0 and one is not None:
        parsed = core.parse_onepoint(one, base_cfg)
        required = set(base_cfg["likelihood_accounting"]["required_nonlocal"])
        finite_ok, finite_reason = core.finite_scientific_point(parsed, required)
        out["bestfit"] = parsed
        out["finite_scientific_gate"] = finite_ok
        if finite_ok:
            out["chi2_scientific_total"] = sum(
                float(parsed["chi2_nonoverlap"][k]) for k in required
            )
            out["status"] = "PASS"
        else:
            out["reason"] = finite_reason
    else:
        logfile = ROOT / base_cfg["logs_dir"] / f"q005_v14_globality_{model}_{profile}.log"
        out["optimizer_diagnostic"] = core.parse_minimizer_failure(logfile)
        out["reason"] = f"COBAYA_EXIT_{exit_code}" if exit_code else "NO_ONEPOINT_RESULT"

    p = result_path(base_cfg, model, profile)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def run_one(base_cfg: dict[str, Any], rcfg: dict[str, Any], model: str,
            profile: str, profile_index: int) -> int:
    if base_cfg["project"]["q"] != "Q-005" or rcfg["project"]["q"] != "Q-005":
        raise RuntimeError("Q_IDENTITY_GATE = FAIL")
    if base_cfg["project"]["id"] != rcfg["project"]["parent_project"]:
        raise RuntimeError("PARENT_PROJECT_GATE = FAIL")

    pf = core.preflight(base_cfg)
    if pf["status"] != "PASS":
        print(json.dumps(pf, indent=2))
        return 5

    rendered = render(base_cfg, rcfg, model, profile, profile_index)
    rc = core.cobaya_run(rendered, base_cfg)
    result = collect(base_cfg, rcfg, model, profile, profile_index, rendered, rc)
    print(json.dumps(result, indent=2))
    # Technical failures are preserved as result records. Workflow job itself
    # remains successful once the record exists, so aggregation can classify it.
    return 0


def find_recovery_results(base: Path) -> list[Path]:
    return sorted(base.rglob("q005_globality_result_*.json"))


def boundary_flags(base_cfg: dict[str, Any], model: str, bestfit: dict[str, Any]) -> list[str]:
    if base_cfg["models"][model].get("kind") != "ede":
        return []
    flags = []
    vals = {
        "fEDE": (bestfit.get("fEDE"), 0.001, 0.3, 0.001),
        "log10z_c": (bestfit.get("log10z_c"), 3.0, 4.3, 0.02),
        "thetai_scf": (bestfit.get("thetai_scf"), 0.1, 3.1, 0.02),
    }
    for name, (v, lo, hi, tol) in vals.items():
        if isinstance(v, (int, float)) and (float(v) <= lo + tol or float(v) >= hi - tol):
            flags.append(f"{name}_NEAR_BOUNDARY")
    return flags


def aggregate(base_cfg: dict[str, Any], rcfg: dict[str, Any], artifacts_root: str,
              output: str) -> dict[str, Any]:
    base = ROOT / artifacts_root
    files = find_recovery_results(base)
    rows = []
    for p in files:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == "Q-005" and d.get("project") == rcfg["project"]["id"]:
            rows.append(d)

    threshold = float(rcfg["gates"]["globality_delta_chi2"])
    min_cluster = int(rcfg["gates"]["minimum_replicated_best_profiles"])
    min_valid = int(rcfg["gates"]["minimum_valid_profiles_per_model"])

    out: dict[str, Any] = {
        "q": "Q-005",
        "project": rcfg["project"]["id"],
        "parent_project": rcfg["project"]["parent_project"],
        "parent_result": rcfg["parent_result"],
        "result_class": "DETERMINISTIC_GLOBALITY_RECOVERY",
        "status": "UNRESOLVED",
        "models": {},
        "comparisons": {},
        "gates": {},
        "technical_changes_only": {
            "fixed_start_references": True,
            "max_evals": rcfg["optimizer_recovery"]["max_evals"],
            "rhoend": rcfg["optimizer_recovery"]["rhoend"],
            "ede_rhobeg": rcfg["optimizer_recovery"]["ede_rhobeg"],
            "science_configuration_changed": False,
        },
        "claim_boundary": rcfg["frozen_claim_boundary"],
        "warnings": [],
    }

    coverage_all = True
    recovery_all = True
    strict_globality_all = True

    for model, expected_profiles_map in rcfg["profiles"].items():
        expected_profiles = list(expected_profiles_map)
        mrows = [r for r in rows if r.get("model") == model]
        by_profile: dict[str, list[dict[str, Any]]] = {}
        for r in mrows:
            by_profile.setdefault(str(r.get("profile")), []).append(r)
        duplicates = sorted(k for k, v in by_profile.items() if len(v) > 1)
        if duplicates:
            out["warnings"].append(f"{model}: duplicate recovery profiles {duplicates}; using last record")
        canonical = {k: v[-1] for k, v in by_profile.items()}
        missing = sorted(set(expected_profiles) - set(canonical))
        coverage = not missing
        coverage_all &= coverage

        valid = [canonical[p] for p in expected_profiles if p in canonical and canonical[p].get("status") == "PASS"]
        failures = [canonical[p] for p in expected_profiles if p in canonical and canonical[p].get("status") != "PASS"]
        quorum = len(valid) >= min_valid
        if not quorum:
            recovery_all = False
            strict_globality_all = False
            out["models"][model] = {
                "status": "INSUFFICIENT_VALID_PROFILES",
                "expected_profiles": expected_profiles,
                "missing_profiles": missing,
                "valid_profiles": [x.get("profile") for x in valid],
                "failed_profiles": [x.get("profile") for x in failures],
                "coverage_pass": coverage,
                "valid_profile_quorum_pass": False,
            }
            continue

        ranked = sorted(valid, key=lambda r: float(r["chi2_scientific_total"]))
        best = ranked[0]
        best_chi = float(best["chi2_scientific_total"])
        deltas = {str(r["profile"]): float(r["chi2_scientific_total"]) - best_chi for r in ranked}
        spread = max(deltas.values()) if deltas else None
        best_cluster = [name for name, delta in deltas.items() if delta <= threshold]
        distinct = [name for name, delta in deltas.items() if delta > threshold]

        strict_pass = bool(spread is not None and math.isfinite(spread) and spread <= threshold)
        replicated_best = len(best_cluster) >= min_cluster
        multiple_characterized = replicated_best and bool(distinct)
        recovery_pass = strict_pass or multiple_characterized

        strict_globality_all &= strict_pass
        recovery_all &= recovery_pass

        out["models"][model] = {
            "status": "RECOVERED" if recovery_pass else "UNRESOLVED",
            "classification": (
                "STABLE_GLOBAL_MINIMUM" if strict_pass else
                "PERSISTENT_MULTIPLE_BASINS_CHARACTERIZED_BEST_REPLICATED" if multiple_characterized else
                "BEST_BASIN_NOT_REPLICATED"
            ),
            "selected_profile": best["profile"],
            "chi2_scientific_total": best_chi,
            "bestfit": best["bestfit"],
            "boundary_flags": boundary_flags(base_cfg, model, best["bestfit"]),
            "profile_delta_chi2_from_best": deltas,
            "recovery_spread_chi2": spread,
            "best_cluster_profiles": best_cluster,
            "distinct_higher_basin_profiles": distinct,
            "strict_globality_pass": strict_pass,
            "replicated_best_basin": replicated_best,
            "multiple_basins_characterized": multiple_characterized,
            "globality_recovery_pass": recovery_pass,
            "expected_profiles": expected_profiles,
            "missing_profiles": missing,
            "coverage_pass": coverage,
            "valid_profile_count": len(valid),
            "failed_profiles": [
                {
                    "profile": r.get("profile"),
                    "reason": r.get("reason"),
                    "optimizer_diagnostic": r.get("optimizer_diagnostic"),
                }
                for r in failures
            ],
        }

    out["gates"]["RECOVERY_EXECUTION_COVERAGE_GATE"] = "PASS" if coverage_all else "FAIL"
    out["gates"]["GLOBALITY_GATE"] = "PASS" if strict_globality_all else "UNRESOLVED"
    out["gates"]["GLOBALITY_RECOVERY_GATE"] = "PASS" if recovery_all and coverage_all else "UNRESOLVED"

    if all(out["models"].get(m, {}).get("bestfit") for m in rcfg["profiles"]):
        lcdm = out["models"]["lcdm"]
        base_chi = float(lcdm["chi2_scientific_total"])
        high_h0 = float(rcfg["gates"]["high_h0_threshold"])
        for model in ("ede_n3", "ede_n2", "me_common"):
            mr = out["models"][model]
            chi = float(mr["chi2_scientific_total"])
            h0 = mr["bestfit"].get("H0")
            k = int(core.resolve_model(base_cfg, model).get("extra_parameter_count", 0))
            dchi = chi - base_chi
            out["comparisons"][model] = {
                "delta_chi2_vs_recovered_lcdm": dchi,
                "extra_parameters": k,
                "delta_AIC_vs_recovered_lcdm": dchi + 2 * k,
                "H0": h0,
                "high_H0_gate_threshold": high_h0,
                "high_H0_gate_pass": isinstance(h0, (int, float)) and float(h0) >= high_h0,
            }

        n2 = out["models"]["ede_n2"]
        low_profile = next((r for r in rows if r.get("model") == "ede_n2" and r.get("profile") == "low_fede_lcdm" and r.get("status") == "PASS"), None)
        if low_profile:
            delta_low_vs_selected = float(low_profile["chi2_scientific_total"]) - float(n2["chi2_scientific_total"])
            out["comparisons"]["ede_n2_low_fede_test"] = {
                "low_fede_profile_chi2": low_profile["chi2_scientific_total"],
                "selected_n2_chi2": n2["chi2_scientific_total"],
                "delta_chi2_low_fede_minus_selected": delta_low_vs_selected,
                "interpretation": (
                    "If the low-fEDE profile converges to the selected best basin and is dramatically better than "
                    "the run21 catastrophic n=2 point, the parent catastrophic result is optimizer trapping. "
                    "If it remains catastrophically poor reproducibly, classify this as persistent common-backend behavior, "
                    "not native K-038 falsification."
                ),
            }

    if coverage_all and recovery_all:
        out["status"] = "PASS_GLOBALITY_RECOVERY"
        out["gates"]["FINAL_RECOVERY_RESULT_GATE"] = "PASS"
        out["next_required_action"] = (
            "Return the recovered minima and basin classification to Bubbleverse Result Ingestion & Routing. "
            "Do not rerun H0DN until Result Ingestion decides it remains material."
        )
    else:
        out["status"] = "UNRESOLVED_AFTER_TARGETED_RECOVERY"
        out["gates"]["FINAL_RECOVERY_RESULT_GATE"] = "UNRESOLVED"
        out["next_required_action"] = (
            "Return GLOBALITY UNRESOLVED AFTER TARGETED RECOVERY to Bubbleverse Result Ingestion & Routing. "
            "Do not generate additional blind seeds automatically."
        )

    op = ROOT / output
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


def validate_config(base_cfg: dict[str, Any], rcfg: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["q_match"] = base_cfg["project"]["q"] == rcfg["project"]["q"] == "Q-005"
    checks["parent_project_match"] = base_cfg["project"]["id"] == rcfg["project"]["parent_project"]
    checks["globality_threshold_unchanged"] = (
        float(base_cfg["gates"]["globality"]["max_restart_delta_chi2"])
        == float(rcfg["gates"]["globality_delta_chi2"])
    )
    checks["high_h0_threshold_unchanged"] = (
        float(base_cfg["gates"]["high_h0_without_local_prior"]["threshold"])
        == float(rcfg["gates"]["high_h0_threshold"])
    )
    checks["no_h0dn_discovery"] = rcfg["runtime"].get("h0dn_reoptimization") is False
    checks["finite_job_plan"] = len(plan(rcfg)["include"]) == 11

    profile_refs_valid = True
    errors = []
    for item in plan(rcfg)["include"]:
        try:
            obj = build_recovery_model(base_cfg, rcfg, item["model"], item["profile"], item["profile_index"])
            if not obj.get("sampler", {}).get("minimize"):
                raise ValueError("Missing minimize sampler")
        except Exception as exc:
            profile_refs_valid = False
            errors.append(f"{item['model']}/{item['profile']}: {exc}")
    checks["all_fixed_refs_cover_sampled_parameters_and_bounds"] = profile_refs_valid

    out = {
        "q": "Q-005",
        "project": rcfg["project"]["id"],
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "errors": errors,
        "job_count": len(plan(rcfg)["include"]),
        "recovery_config_sha256": core.sha256_file(ROOT / DEFAULT_RECOVERY_CONFIG),
    }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-config", default="q005_hpc_v14_config.yml")
    ap.add_argument("--recovery-config", default=DEFAULT_RECOVERY_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("plan")
    pp.add_argument("--json", action="store_true")

    sub.add_parser("preflight")

    rr = sub.add_parser("run")
    rr.add_argument("--model", required=True)
    rr.add_argument("--profile", required=True)
    rr.add_argument("--profile-index", type=int, required=True)

    aa = sub.add_parser("aggregate")
    aa.add_argument("--artifacts-root", default="q005_v14_globality_aggregate")
    aa.add_argument("--output", default="q005_v14_globality_aggregate/q005_v14_globality_recovery_result.json")

    args = ap.parse_args()
    base_cfg = core.load_cfg(args.base_config)
    rcfg = load_recovery(args.recovery_config)

    if args.cmd == "plan":
        v = validate_config(base_cfg, rcfg)
        if v["status"] != "PASS":
            print(json.dumps({"error": "RECOVERY_CONFIG_GATE_FAIL", "validation": v}, indent=2))
            return 2
        p = plan(rcfg)
        print(json.dumps(p, separators=(",", ":") if args.json else None))
        return 0

    if args.cmd == "preflight":
        v = validate_config(base_cfg, rcfg)
        print(json.dumps(v, indent=2))
        return 0 if v["status"] == "PASS" else 3

    if args.cmd == "run":
        return run_one(base_cfg, rcfg, args.model, args.profile, args.profile_index)

    if args.cmd == "aggregate":
        out = aggregate(base_cfg, rcfg, args.artifacts_root, args.output)
        return 0 if out["status"] in ("PASS_GLOBALITY_RECOVERY", "UNRESOLVED_AFTER_TARGETED_RECOVERY") else 4

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
