#!/usr/bin/env python3
"""Bubbleverse Q-008 n=3 EDE fixed-H0 globality validation V1.

Purpose
-------
Test whether the non-monotone Q-006 n=3 EDE profile is primarily an optimizer /
basin artifact or a reproducible feature of the frozen Q-005/Q-006 common
backend.

Scientific invariants
---------------------
* CURRENT_Q is Q-008.
* The Q-005 V14 common backend is reused unchanged.
* H0 is fixed at the Q-006 profile targets.
* Priors, bounds, datasets, likelihoods, nuisance treatment and model definition
  are not changed.
* Original Q-006 results remain historical evidence and are never overwritten.
* "best observed minimum" is never called a documented global minimum.

Execution design
----------------
Stage 1:
    four independent documented start families at each fixed H0 target.
Stage 2:
    re-refine every valid Stage-1 endpoint from its own best-fit coordinates.
Final:
    compare basin convergence, numerical refinement, boundary flags and the
    resulting profile curve against the historical Q-006 profile.

This file intentionally reuses q005_hpc_v14.py and configuration/provenance from
q005_globality_recovery_v14_config.yml rather than recreating the cosmology
backend.
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
DEFAULT_CONFIG = "q008_globality_validation_v1_config.yml"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    return load_yaml(ROOT / path)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def htag(h0: float) -> str:
    return f"{float(h0):.6f}".rstrip("0").rstrip(".").replace(".", "p")


def sampled_names(model: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for name, spec in model.get("params", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            names.add(name)
    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict):
            continue
        pmap = lspec.get("params")
        if not isinstance(pmap, dict):
            continue
        for name, spec in pmap.items():
            if isinstance(spec, dict) and "prior" in spec:
                names.add(name)
    return names


def prior_bounds(model: dict[str, Any]) -> dict[str, tuple[float, float]]:
    blocks = [model.get("params", {})]
    for lspec in model.get("likelihood", {}).values():
        if isinstance(lspec, dict) and isinstance(lspec.get("params"), dict):
            blocks.append(lspec["params"])
    out: dict[str, tuple[float, float]] = {}
    for block in blocks:
        for name, spec in block.items():
            if not isinstance(spec, dict):
                continue
            pr = spec.get("prior")
            if isinstance(pr, dict) and "min" in pr and "max" in pr:
                out[name] = (float(pr["min"]), float(pr["max"]))
    return out


def set_refs(model: dict[str, Any], refs: dict[str, float], skip: set[str] | None = None) -> None:
    skip = skip or set()
    expected = sampled_names(model) - skip
    supplied = set(refs) - skip
    missing = sorted(expected - supplied)
    extra = sorted(supplied - expected)
    if missing or extra:
        raise ValueError(f"REF_COVERAGE_GATE=FAIL missing={missing} extra={extra}")

    bounds = prior_bounds(model)
    for name, value in refs.items():
        if name in skip:
            continue
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"NONFINITE_REF {name}={value}")
        if name in bounds:
            lo, hi = bounds[name]
            if not (lo <= value <= hi):
                raise ValueError(f"REF_OUTSIDE_PRIOR {name}={value} prior=[{lo},{hi}]")

    for name, spec in model.get("params", {}).items():
        if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
            spec["ref"] = float(refs[name])
    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict) or not isinstance(lspec.get("params"), dict):
            continue
        for name, spec in lspec["params"].items():
            if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
                spec["ref"] = float(refs[name])


def base_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    return core.load_cfg(cfg["parent"]["base_config"])


def recovery_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    return load_yaml(ROOT / cfg["parent"]["recovery_config"])


def profile_specs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    i = 0
    for target in cfg["profile"]["h0_targets"]:
        for start in cfg["starts"]["families"]:
            out.append(
                {
                    "model": cfg["profile"]["model"],
                    "target_h0": float(target),
                    "start_family": start,
                    "profile_index": i,
                }
            )
            i += 1
    return out


def plan(cfg: dict[str, Any]) -> dict[str, Any]:
    return {"include": profile_specs(cfg)}


def historical_key_seed(cfg: dict[str, Any], target_h0: float) -> dict[str, float]:
    hist = cfg["historical_q006"]["bestfit_key_parameters"]
    keys = sorted(hist, key=lambda k: abs(float(k) - float(target_h0)))
    return {k: float(v) for k, v in hist[keys[0]].items()}


def stage1_refs(cfg: dict[str, Any], target_h0: float, start_family: str) -> tuple[dict[str, float], str]:
    rcfg = recovery_cfg(cfg)
    if start_family in ("run21_best", "k036_high_h0", "low_fede_control"):
        refs = copy.deepcopy(rcfg["profiles"]["ede_n3"][start_family]["refs"])
        provenance = f"Q005 globality recovery profile ede_n3/{start_family}"
    elif start_family == "q006_historical_shape":
        refs = copy.deepcopy(rcfg["profiles"]["ede_n3"]["k036_high_h0"]["refs"])
        transplant = historical_key_seed(cfg, target_h0)
        for name, value in transplant.items():
            if name != "H0":
                refs[name] = float(value)
        provenance = (
            "Q006 historical best-fit key-parameter shape transplanted onto the "
            "complete Q005 k036_high_h0 nuisance/auxiliary reference"
        )
    else:
        raise KeyError(f"Unknown start family {start_family}")
    refs["H0"] = float(target_h0)
    return {k: float(v) for k, v in refs.items()}, provenance


def make_model(
    cfg: dict[str, Any],
    target_h0: float,
    start_family: str,
    profile_index: int,
    refs: dict[str, float],
    stage: str,
) -> dict[str, Any]:
    base = base_cfg(cfg)
    model_name = cfg["profile"]["model"]
    obj = core.build_model(base, model_name, smoke=False, restart=0)
    set_refs(obj, refs, skip={"H0"})
    core.freeze_param_value(obj["params"], "H0", float(target_h0))

    opt = cfg["optimizer"][stage]
    minimize = obj["sampler"]["minimize"]
    minimize["seed"] = int(opt["seed_base"]) + int(profile_index)
    minimize["max_evals"] = int(opt["max_evals"])
    minimize["override_bobyqa"]["rhoend"] = float(opt["rhoend"])
    minimize["override_bobyqa"]["rhobeg"] = float(opt["ede_rhobeg"])

    tag = f"q008_{stage}_{model_name}_h0_{htag(target_h0)}_{start_family}"
    obj["output"] = str((ROOT / cfg["paths"]["results"] / tag).resolve())
    return obj


def rendered_path(cfg: dict[str, Any], stage: str, target_h0: float, start_family: str) -> Path:
    p = ROOT / cfg["paths"]["rendered"] / f"q008_{stage}_h0_{htag(target_h0)}_{start_family}.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def result_path(cfg: dict[str, Any], stage: str, target_h0: float, start_family: str) -> Path:
    p = ROOT / cfg["paths"]["results"] / f"q008_{stage}_h0_{htag(target_h0)}_{start_family}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def render(
    cfg: dict[str, Any],
    stage: str,
    target_h0: float,
    start_family: str,
    profile_index: int,
    refs: dict[str, float],
) -> Path:
    obj = make_model(cfg, target_h0, start_family, profile_index, refs, stage)
    p = rendered_path(cfg, stage, target_h0, start_family)
    p.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
    return p


def boundary_flags(cfg: dict[str, Any], bestfit: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    for name, spec in cfg["gates"]["boundary_parameters"].items():
        v = bestfit.get(name)
        if not isinstance(v, (int, float)):
            continue
        lo, hi, tol = float(spec["min"]), float(spec["max"]), float(spec["tol"])
        if float(v) <= lo + tol:
            flags.append(f"{name}_NEAR_LOWER_BOUNDARY")
        if float(v) >= hi - tol:
            flags.append(f"{name}_NEAR_UPPER_BOUNDARY")
    return flags


def collect(
    cfg: dict[str, Any],
    stage: str,
    target_h0: float,
    start_family: str,
    profile_index: int,
    refs: dict[str, float],
    provenance: str,
    rendered: Path,
    exit_code: int,
    parent_stage1: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = base_cfg(cfg)
    out: dict[str, Any] = {
        "q": "Q-008",
        "run_id": cfg["project"]["run_id"],
        "result_class": "FIXED_H0_EDE_GLOBALITY_PROFILE",
        "stage": stage,
        "model": cfg["profile"]["model"],
        "target_h0": float(target_h0),
        "start_family": start_family,
        "profile_index": int(profile_index),
        "parent_q": "Q-006",
        "frozen_backend_parent_q": "Q-005",
        "start_reference": refs,
        "start_reference_sha256": canonical_hash(refs),
        "start_provenance": provenance,
        "rendered_yaml": str(rendered),
        "rendered_yaml_sha256": core.sha256_file(rendered),
        "optimizer": cfg["optimizer"][stage],
        "cobaya_exit": int(exit_code),
        "status": "FAIL",
        "claim_boundary": cfg["claim_boundary"],
        "sources": cfg["sources"],
    }
    if parent_stage1 is not None:
        out["parent_stage1_result_sha256"] = canonical_hash(parent_stage1)
        out["parent_stage1_chi2"] = parent_stage1.get("chi2_scientific_total")

    prefix = Path(load_yaml(rendered)["output"])
    one = core.find_onepoint(prefix)
    if exit_code == 0 and one is not None:
        parsed = core.parse_onepoint(one, base)
        required = set(base["likelihood_accounting"]["required_nonlocal"])
        finite_ok, reason = core.finite_scientific_point(parsed, required)
        out["bestfit"] = parsed
        out["finite_scientific_gate"] = finite_ok
        if finite_ok:
            out["chi2_components"] = {
                k: float(parsed["chi2_nonoverlap"][k]) for k in sorted(required)
            }
            out["chi2_scientific_total"] = sum(out["chi2_components"].values())
            out["boundary_flags"] = boundary_flags(cfg, parsed)
            out["status"] = "PASS"
        else:
            out["reason"] = reason
    else:
        out["reason"] = f"COBAYA_EXIT_{exit_code}" if exit_code else "NO_ONEPOINT_RESULT"

    if parent_stage1 is not None and out.get("status") == "PASS" and parent_stage1.get("status") == "PASS":
        out["delta_chi2_vs_stage1"] = (
            float(out["chi2_scientific_total"]) - float(parent_stage1["chi2_scientific_total"])
        )

    p = result_path(cfg, stage, target_h0, start_family)
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def preflight(cfg: dict[str, Any]) -> dict[str, Any]:
    base = base_cfg(cfg)
    rcfg = recovery_cfg(cfg)
    checks = {
        "Q_IDENTITY_GATE": cfg["project"]["q"] == "Q-008",
        "PARENT_Q_GATE": cfg["parent"]["q"] == "Q-006",
        "BASE_Q_GATE": base["project"]["q"] == "Q-005",
        "MODEL_GATE": cfg["profile"]["model"] == "ede_n3",
        "TARGET_GATE": [float(x) for x in cfg["profile"]["h0_targets"]]
        == [70.853292, 71.5, 72.5, 73.5],
        "RECOVERY_PROFILE_GATE": all(
            x in rcfg["profiles"]["ede_n3"]
            for x in ("run21_best", "k036_high_h0", "low_fede_control")
        ),
        "NO_SCIENCE_CHANGE_GATE": bool(cfg["claim_boundary"]["frozen_common_backend"]),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {"q": "Q-008", "status": status, "checks": checks}


def run_stage1(cfg: dict[str, Any], target_h0: float, start_family: str, profile_index: int) -> int:
    pf = preflight(cfg)
    if pf["status"] != "PASS":
        print(json.dumps(pf, indent=2))
        return 5
    base = base_cfg(cfg)
    core_pf = core.preflight(base)
    if core_pf["status"] != "PASS":
        print(json.dumps({"q": "Q-008", "status": "FAIL", "gate": "ENVIRONMENT_GATE", "parent": core_pf}, indent=2))
        return 6

    refs, provenance = stage1_refs(cfg, target_h0, start_family)
    rendered = render(cfg, "stage1", target_h0, start_family, profile_index, refs)
    rc = core.cobaya_run(rendered, base)
    result = collect(
        cfg, "stage1", target_h0, start_family, profile_index,
        refs, provenance, rendered, rc,
    )
    print(json.dumps(result, indent=2))
    return 0


def find_result(root: Path, stage: str, target_h0: float, start_family: str) -> dict[str, Any]:
    name = f"q008_{stage}_h0_{htag(target_h0)}_{start_family}.json"
    matches = sorted(root.rglob(name))
    if not matches:
        raise FileNotFoundError(f"Missing {stage} result {name} under {root}")
    vals = []
    for p in matches:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == "Q-008" and d.get("run_id"):
            vals.append(d)
    if not vals:
        raise RuntimeError(f"No valid Q-008 record for {name}")
    return vals[-1]


def refs_from_bestfit(cfg: dict[str, Any], parent: dict[str, Any], target_h0: float) -> dict[str, float]:
    if parent.get("status") != "PASS":
        raise RuntimeError("STAGE1_PARENT_GATE=FAIL")
    base = base_cfg(cfg)
    obj = core.build_model(base, cfg["profile"]["model"], smoke=False, restart=0)
    needed = sampled_names(obj) - {"H0"}
    bestfit = parent.get("bestfit", {})
    refs: dict[str, float] = {}
    missing = []
    for name in sorted(needed):
        v = bestfit.get(name)
        if not isinstance(v, (int, float)) or not math.isfinite(float(v)):
            missing.append(name)
        else:
            refs[name] = float(v)
    if missing:
        raise RuntimeError(f"STAGE1_BESTFIT_COVERAGE_GATE=FAIL missing={missing}")
    refs["H0"] = float(target_h0)
    return refs


def run_stage2(
    cfg: dict[str, Any],
    target_h0: float,
    start_family: str,
    profile_index: int,
    stage1_root: str,
) -> int:
    pf = preflight(cfg)
    if pf["status"] != "PASS":
        print(json.dumps(pf, indent=2))
        return 5
    root = ROOT / stage1_root
    try:
        parent = find_result(root, "stage1", target_h0, start_family)
    except Exception as exc:
        fail = {
            "q": "Q-008", "run_id": cfg["project"]["run_id"],
            "stage": "stage2", "target_h0": target_h0,
            "start_family": start_family, "status": "FAIL",
            "reason": f"STAGE1_PARENT_MISSING: {exc}",
        }
        result_path(cfg, "stage2", target_h0, start_family).write_text(json.dumps(fail, indent=2)+"\n")
        print(json.dumps(fail, indent=2))
        return 0

    if parent.get("status") != "PASS":
        fail = {
            "q": "Q-008", "run_id": cfg["project"]["run_id"],
            "stage": "stage2", "target_h0": target_h0,
            "start_family": start_family, "status": "SKIPPED",
            "reason": "STAGE1_NOT_VALID",
            "parent_stage1_status": parent.get("status"),
        }
        result_path(cfg, "stage2", target_h0, start_family).write_text(json.dumps(fail, indent=2)+"\n")
        print(json.dumps(fail, indent=2))
        return 0

    base = base_cfg(cfg)
    core_pf = core.preflight(base)
    if core_pf["status"] != "PASS":
        print(json.dumps({"q": "Q-008", "status": "FAIL", "gate": "ENVIRONMENT_GATE", "parent": core_pf}, indent=2))
        return 6

    refs = refs_from_bestfit(cfg, parent, target_h0)
    provenance = "Stage-2 re-refinement from this exact Stage-1 endpoint"
    rendered = render(cfg, "stage2", target_h0, start_family, profile_index, refs)
    rc = core.cobaya_run(rendered, base)
    result = collect(
        cfg, "stage2", target_h0, start_family, profile_index,
        refs, provenance, rendered, rc, parent_stage1=parent,
    )
    print(json.dumps(result, indent=2))
    return 0


def load_all(root: Path, stage: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in sorted(root.rglob(f"q008_{stage}_h0_*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == "Q-008":
            rows.append(d)
    return rows


def aggregate(cfg: dict[str, Any], stage1_root: str, stage2_root: str, output: str) -> dict[str, Any]:
    s1 = load_all(ROOT / stage1_root, "stage1")
    s2 = load_all(ROOT / stage2_root, "stage2")
    specs = profile_specs(cfg)
    expected = {(float(x["target_h0"]), x["start_family"]) for x in specs}

    by1 = {(float(r["target_h0"]), r["start_family"]): r for r in s1 if "target_h0" in r and "start_family" in r}
    by2 = {(float(r["target_h0"]), r["start_family"]): r for r in s2 if "target_h0" in r and "start_family" in r}

    missing_s1 = sorted(expected - set(by1))
    missing_s2 = sorted(expected - set(by2))
    complete = not missing_s1 and not missing_s2

    cluster_tol = float(cfg["gates"]["replication_delta_chi2"])
    refinement_tol = float(cfg["gates"]["refinement_delta_chi2"])
    material = float(cfg["gates"]["material_profile_change_delta_chi2"])
    min_rep = int(cfg["gates"]["minimum_replicated_best_starts"])

    out: dict[str, Any] = {
        "q": "Q-008",
        "run_id": cfg["project"]["run_id"],
        "result_class": "EDE_FIXED_H0_GLOBALITY_VALIDATION",
        "status": "UNRESOLVED",
        "historical_q006_preserved": cfg["historical_q006"],
        "profile_targets": {},
        "new_profile": {},
        "gates": {},
        "missing_stage1": [{"target_h0": h, "start_family": s} for h, s in missing_s1],
        "missing_stage2": [{"target_h0": h, "start_family": s} for h, s in missing_s2],
        "sources": cfg["sources"],
        "claim_boundary": cfg["claim_boundary"],
        "journal_effect": {},
        "next_required_action": None,
    }
    out["gates"]["Q_IDENTITY_GATE"] = "PASS"
    out["gates"]["JOB_COMPLETENESS_GATE"] = "PASS" if complete else "FAIL"

    target_robust = {}
    best_by_target: dict[float, dict[str, Any]] = {}
    all_refinement_ok = True
    all_target_quorum = True
    boundary_any = False

    for target in [float(x) for x in cfg["profile"]["h0_targets"]]:
        rows = []
        for start in cfg["starts"]["families"]:
            key = (target, start)
            r1 = by1.get(key)
            r2 = by2.get(key)
            chosen = r2 if r2 and r2.get("status") == "PASS" else r1
            if chosen and chosen.get("status") == "PASS":
                rows.append(chosen)

        if len(rows) < min_rep:
            all_target_quorum = False
            target_robust[target] = False
            out["profile_targets"][str(target)] = {
                "status": "INSUFFICIENT_VALID_STARTS",
                "valid_count": len(rows),
            }
            continue

        ranked = sorted(rows, key=lambda r: float(r["chi2_scientific_total"]))
        best = ranked[0]
        best_chi = float(best["chi2_scientific_total"])
        deltas = {
            r["start_family"]: float(r["chi2_scientific_total"]) - best_chi
            for r in ranked
        }
        cluster = sorted([k for k, d in deltas.items() if d <= cluster_tol])
        distinct = sorted([k for k, d in deltas.items() if d > cluster_tol])
        replicated = len(cluster) >= min_rep

        ref_deltas = []
        for start in cfg["starts"]["families"]:
            r2 = by2.get((target, start))
            if r2 and r2.get("status") == "PASS" and isinstance(r2.get("delta_chi2_vs_stage1"), (int, float)):
                ref_deltas.append(float(r2["delta_chi2_vs_stage1"]))
        refinement_ok = all(d <= refinement_tol for d in ref_deltas)
        all_refinement_ok &= refinement_ok

        flags = sorted(set(x for r in ranked for x in r.get("boundary_flags", [])))
        boundary_any |= bool(flags)
        target_robust[target] = replicated and refinement_ok
        best_by_target[target] = best

        out["profile_targets"][str(target)] = {
            "status": "ROBUST_BEST_OBSERVED_BASIN_REPLICATED" if target_robust[target] else "UNRESOLVED_BASIN_STRUCTURE",
            "best_observed_chi2": best_chi,
            "best_start_family": best["start_family"],
            "replicated_best_start_families": cluster,
            "distinct_higher_basin_start_families": distinct,
            "delta_chi2_from_best_by_start": deltas,
            "stage2_delta_chi2_vs_stage1": ref_deltas,
            "refinement_gate": "PASS" if refinement_ok else "FAIL",
            "boundary_flags": flags,
            "bestfit": best.get("bestfit", {}),
            "chi2_components": best.get("chi2_components", {}),
        }

    baseline = float(cfg["profile"]["baseline_h0"])
    if baseline in best_by_target:
        bchi = float(best_by_target[baseline]["chi2_scientific_total"])
        for target, best in sorted(best_by_target.items()):
            out["new_profile"][str(target)] = {
                "chi2_total": float(best["chi2_scientific_total"]),
                "delta_chi2_total": float(best["chi2_scientific_total"]) - bchi,
            }

    historical = {float(k): float(v) for k, v in cfg["historical_q006"]["delta_chi2_total"].items()}
    profile_changes = {}
    for target, hdelta in historical.items():
        n = out["new_profile"].get(str(target))
        if n:
            profile_changes[str(target)] = float(n["delta_chi2_total"]) - hdelta
    out["comparison_to_q006"] = {
        "delta_new_minus_historical": profile_changes,
        "material_threshold_abs_delta_chi2": material,
    }

    target_725 = out["new_profile"].get("72.5")
    hist_725 = historical.get(72.5)
    materially_changed_725 = False
    if target_725 is not None and hist_725 is not None:
        materially_changed_725 = abs(float(target_725["delta_chi2_total"]) - hist_725) >= material

    all_robust = (
        complete
        and all_target_quorum
        and len(target_robust) == len(cfg["profile"]["h0_targets"])
        and all(target_robust.values())
        and all_refinement_ok
    )

    out["gates"]["VALID_START_QUORUM_GATE"] = "PASS" if all_target_quorum else "FAIL"
    out["gates"]["REFINEMENT_GATE"] = "PASS" if all_refinement_ok else "FAIL"
    out["gates"]["BEST_BASIN_REPLICATION_GATE"] = "PASS" if all_robust else "UNRESOLVED"
    out["gates"]["BOUNDARY_DIAGNOSTIC_GATE"] = "WARNING" if boundary_any else "PASS"
    out["gates"]["GLOBALITY_GATE"] = (
        "PASS_BEST_OBSERVED_BASIN_ROBUSTLY_REPLICATED"
        if all_robust else "UNRESOLVED"
    )

    if all_robust:
        out["status"] = "PASS"
        if materially_changed_725:
            out["scientific_classification"] = "Q006_PROFILE_MATERIALLY_CORRECTED_BY_GLOBALITY_CONTROL"
            out["journal_effect"] = {
                "Q006_H0_72p5": "SUPERSEDE_ACTIVE_VALUE_PRESERVE_PROVENANCE",
                "Q007_ATTRIBUTION": "REPEAT_ONLY_FOR_MATERIALLY_CHANGED_Q008_MINIMA",
                "global_minimum_claim": "FORBIDDEN_FINITE_RESTARTS_ONLY",
            }
            out["next_required_action"] = (
                "Return to Result Ingestion & Routing. Mark materially changed Q-006 profile "
                "points SUPERSEDED (not deleted), then rerun Q-007 observable attribution only "
                "at the corrected minima."
            )
        else:
            out["scientific_classification"] = "NONMONOTONE_PROFILE_REPRODUCED_UNDER_FINITE_GLOBALITY_CONTROL"
            out["journal_effect"] = {
                "Q006_PROFILE": "STRENGTHEN",
                "Q007_ATTRIBUTION": "KEEP",
                "global_minimum_claim": "FORBIDDEN_FINITE_RESTARTS_ONLY",
            }
            out["next_required_action"] = (
                "Return to Result Ingestion & Routing. Preserve the non-monotone profile as a "
                "technically credible common-backend likelihood feature; no automatic Q-007 rerun."
            )
        out["gates"]["FINAL_RESULT_GATE"] = "PASS"
    else:
        out["scientific_classification"] = "GLOBALITY_STATUS_UNRESOLVED"
        out["journal_effect"] = {
            "Q006_PROFILE": "KEEP_PROVISIONAL",
            "Q007_ATTRIBUTION": "KEEP_FOR_OLD_FROZEN_POINTS",
            "global_minimum_claim": "FORBIDDEN",
        }
        out["next_required_action"] = (
            "Return unresolved globality evidence to Result Ingestion & Routing. Do not interpret "
            "the Q-006 non-monotonicity physically until unresolved basin/refinement failures are isolated."
        )
        out["gates"]["FINAL_RESULT_GATE"] = "UNRESOLVED"

    op = ROOT / output
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("preflight")
    pplan = sub.add_parser("plan")
    pplan.add_argument("--json", action="store_true")

    for name in ("stage1", "stage2"):
        p = sub.add_parser(name)
        p.add_argument("--target-h0", required=True, type=float)
        p.add_argument("--start-family", required=True)
        p.add_argument("--profile-index", required=True, type=int)
        if name == "stage2":
            p.add_argument("--stage1-root", required=True)

    pagg = sub.add_parser("aggregate")
    pagg.add_argument("--stage1-root", required=True)
    pagg.add_argument("--stage2-root", required=True)
    pagg.add_argument("--output", required=True)

    args = ap.parse_args()
    cfg = load_cfg(args.config)

    if args.cmd == "preflight":
        result = preflight(cfg)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 4
    if args.cmd == "plan":
        result = plan(cfg)
        print(json.dumps(result, separators=(",", ":")) if args.json else json.dumps(result, indent=2))
        return 0
    if args.cmd == "stage1":
        return run_stage1(cfg, args.target_h0, args.start_family, args.profile_index)
    if args.cmd == "stage2":
        return run_stage2(cfg, args.target_h0, args.start_family, args.profile_index, args.stage1_root)
    if args.cmd == "aggregate":
        result = aggregate(cfg, args.stage1_root, args.stage2_root, args.output)
        print(json.dumps(result, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
