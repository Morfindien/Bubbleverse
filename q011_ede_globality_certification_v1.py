#!/usr/bin/env python3
"""
Bubbleverse Q011 — n=3 EDE fixed-H0 globality / basin certification V1.

Purpose
-------
Perform a materially stronger basin search than Q008 on the EXACT frozen Q005 V14
scientific likelihood surface at H0 = 70.853292, 71.5, 72.5, 73.5 km/s/Mpc.

This program:
* reuses q005_hpc_v14.py as the scientific backend;
* consumes the latest successful Q008 final result as authoritative corrected seeds;
* preserves Q008 historical and Q005 recovery seed families;
* adds deterministic Sobol/dispersed, boundary-aware, and anti-basin starts;
* runs two refinement stages without changing the scientific model/data/priors/bounds;
* clusters valid endpoints into basins in normalized parameter space + chi2;
* applies an explicit numerical-certification criterion;
* never calls a finite search a mathematically proven global minimum.

Scientific outputs are BEST-OBSERVED / NUMERICALLY CERTIFIED only unless a genuine
mathematical proof is supplied externally (this program does not claim one).
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.stats import qmc

import q005_hpc_v14 as core

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q011_ede_globality_certification_v1_config.yml"
CODE_VERSION = "1.0-frozen-q005-v14-expanded-basin-certification"


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    return load_yaml(path)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def htag(h0: float) -> str:
    return f"{float(h0):.6f}".rstrip("0").rstrip(".").replace(".", "p")


def base_cfg(c: dict[str, Any]) -> dict[str, Any]:
    return core.load_cfg(c["parent"]["base_config"])


def recovery_cfg(c: dict[str, Any]) -> dict[str, Any]:
    return load_yaml(c["parent"]["recovery_config"])


def sampled_specs(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name, spec in model.get("params", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            out[name] = spec
    for lspec in model.get("likelihood", {}).values():
        if isinstance(lspec, dict) and isinstance(lspec.get("params"), dict):
            for name, spec in lspec["params"].items():
                if isinstance(spec, dict) and "prior" in spec:
                    out[name] = spec
    return out


def bounds_from_specs(specs: dict[str, dict[str, Any]]) -> dict[str, tuple[float, float]]:
    out = {}
    for name, spec in specs.items():
        pr = spec.get("prior")
        if isinstance(pr, dict) and "min" in pr and "max" in pr:
            out[name] = (float(pr["min"]), float(pr["max"]))
    return out


def set_refs(model: dict[str, Any], refs: dict[str, float], skip: set[str] | None = None) -> None:
    skip = skip or set()
    needed = set(sampled_specs(model)) - skip
    have = set(refs) - skip
    missing = sorted(needed - have)
    extra = sorted(have - needed)
    if missing:
        raise RuntimeError(f"REF_COVERAGE_GATE=FAIL missing={missing}")
    # Extra keys are allowed only when they are derived/non-sampled output aliases.
    bounds = bounds_from_specs(sampled_specs(model))
    for name, value in refs.items():
        if name in skip or name not in needed:
            continue
        value = float(value)
        if not math.isfinite(value):
            raise RuntimeError(f"NONFINITE_REF {name}={value}")
        if name in bounds:
            lo, hi = bounds[name]
            if not (lo <= value <= hi):
                raise RuntimeError(f"REF_OUTSIDE_PRIOR {name}={value} prior=[{lo},{hi}]")

    for name, spec in model.get("params", {}).items():
        if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
            spec["ref"] = float(refs[name])
    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict) or not isinstance(lspec.get("params"), dict):
            continue
        for name, spec in lspec["params"].items():
            if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
                spec["ref"] = float(refs[name])


def extract_vector(bestfit: dict[str, Any], needed: set[str]) -> dict[str, float]:
    blocks = [bestfit]
    for k in ("params", "sampled", "sampled_params", "point", "values"):
        if isinstance(bestfit.get(k), dict):
            blocks.append(bestfit[k])
    found: dict[str, float] = {}
    for block in blocks:
        for k, v in block.items():
            if k in needed and isinstance(v, (int, float)) and math.isfinite(float(v)):
                found[k] = float(v)
    missing = sorted(needed - set(found))
    if missing:
        raise RuntimeError(f"Q008_VECTOR_GATE=FAIL missing={missing}")
    return found


def numeric_key(d: dict[str, Any], target: float) -> str:
    for k in d:
        try:
            if math.isclose(float(k), float(target), rel_tol=0.0, abs_tol=1e-9):
                return k
        except Exception:
            pass
    raise KeyError(target)


def q008_seed(c: dict[str, Any], q008: dict[str, Any], target_h0: float) -> dict[str, float]:
    if q008.get("q") != "Q-008":
        raise RuntimeError("Q008_PARENT_IDENTITY_GATE=FAIL")
    profiles = q008.get("profile_targets")
    if not isinstance(profiles, dict):
        raise RuntimeError("Q008_SCHEMA_GATE=FAIL missing profile_targets")
    rec = profiles[numeric_key(profiles, target_h0)]
    bestfit = rec.get("bestfit")
    if not isinstance(bestfit, dict):
        raise RuntimeError("Q008_SCHEMA_GATE=FAIL missing bestfit")
    base = base_cfg(c)
    m = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = set(sampled_specs(m))
    vals = extract_vector(bestfit, needed)
    vals["H0"] = float(target_h0)
    return vals


def recovery_seed(c: dict[str, Any], family: str, target_h0: float) -> dict[str, float]:
    rcfg = recovery_cfg(c)
    refs = copy.deepcopy(rcfg["profiles"]["ede_n3"][family]["refs"])
    refs["H0"] = float(target_h0)
    return {k: float(v) for k, v in refs.items()}


def historical_seed(c: dict[str, Any], target_h0: float) -> dict[str, float]:
    # Start with a complete validated Q005 recovery vector, then transplant only
    # historical coordinates explicitly documented in Q008 config.
    refs = recovery_seed(c, "k036_high_h0", target_h0)
    hist = c["historical_q008"]["historical_pre_q008_key_parameters"]
    key = min(hist, key=lambda k: abs(float(k) - float(target_h0)))
    for k, v in hist[key].items():
        if k != "H0":
            refs[k] = float(v)
    refs["H0"] = float(target_h0)
    return refs


def sobol_unit(index: int, dim: int, scramble_seed: int) -> np.ndarray:
    # Deterministic low-discrepancy point. Generate enough points and select index.
    m = max(1, math.ceil(math.log2(index + 1)))
    eng = qmc.Sobol(d=dim, scramble=True, seed=scramble_seed)
    pts = eng.random_base2(m=m)
    return pts[index]


def dispersed_seed(
    c: dict[str, Any],
    q008: dict[str, Any],
    target_h0: float,
    recipe: dict[str, Any],
) -> dict[str, float]:
    base = q008_seed(c, q008, target_h0)
    model = core.build_model(base_cfg(c), "ede_n3", smoke=False, restart=0)
    specs = sampled_specs(model)
    bounds = bounds_from_specs(specs)
    names = sorted(k for k in bounds if k != "H0")
    kind = recipe["kind"]

    if kind == "sobol":
        u = sobol_unit(int(recipe["index"]), len(names), int(c["starts"]["sobol_scramble_seed"]))
        for name, x in zip(names, u):
            lo, hi = bounds[name]
            # Stay a little off exact boundaries for generic dispersed starts.
            eps = float(c["starts"]["interior_fraction"])
            base[name] = lo + (eps + (1.0 - 2.0 * eps) * float(x)) * (hi - lo)

    elif kind in ("boundary_low", "boundary_high"):
        frac = float(c["starts"]["boundary_fraction"])
        for j, name in enumerate(names):
            lo, hi = bounds[name]
            choose_low = ((j + int(recipe.get("phase", 0))) % 2 == 0)
            if kind == "boundary_high":
                choose_low = not choose_low
            base[name] = lo + (frac if choose_low else 1.0 - frac) * (hi - lo)

    elif kind == "anti_q008":
        q8 = q008_seed(c, q008, target_h0)
        for name in names:
            lo, hi = bounds[name]
            x = float(q8[name])
            mirrored = lo + hi - x
            eps = float(c["starts"]["interior_fraction"]) * (hi - lo)
            base[name] = min(hi - eps, max(lo + eps, mirrored))
    else:
        raise KeyError(kind)

    base["H0"] = float(target_h0)
    return base


def recipes(c: dict[str, Any]) -> list[dict[str, Any]]:
    out = [
        {"name": "q008_best", "kind": "q008_best"},
        {"name": "q005_run21_best", "kind": "recovery", "family": "run21_best"},
        {"name": "q005_k036_high_h0", "kind": "recovery", "family": "k036_high_h0"},
        {"name": "q005_low_fede_control", "kind": "recovery", "family": "low_fede_control"},
        {"name": "historical_pre_q008", "kind": "historical"},
        {"name": "boundary_low", "kind": "boundary_low", "phase": 0},
        {"name": "boundary_high", "kind": "boundary_high", "phase": 1},
        {"name": "anti_q008", "kind": "anti_q008"},
    ]
    for i in range(int(c["starts"]["sobol_count"])):
        out.append({"name": f"sobol_{i:02d}", "kind": "sobol", "index": i})
    return out


def start_vector(c: dict[str, Any], q008: dict[str, Any], target: float, recipe: dict[str, Any]) -> tuple[dict[str, float], str]:
    kind = recipe["kind"]
    if kind == "q008_best":
        return q008_seed(c, q008, target), "Exact Q008 best-observed full sampled vector"
    if kind == "recovery":
        fam = recipe["family"]
        return recovery_seed(c, fam, target), f"Q005 V14 globality-recovery family {fam}"
    if kind == "historical":
        return historical_seed(c, target), "Historical pre-Q008 key coordinates on complete Q005 recovery vector"
    return dispersed_seed(c, q008, target, recipe), f"Deterministic {kind} start generated inside frozen prior bounds"


def matrix(c: dict[str, Any]) -> dict[str, Any]:
    inc = []
    idx = 0
    for h0 in c["profile"]["h0_targets"]:
        for recipe in recipes(c):
            inc.append({
                "target_h0": float(h0),
                "start_family": recipe["name"],
                "recipe_kind": recipe["kind"],
                "recipe": recipe,
                "profile_index": idx,
            })
            idx += 1
    return {"include": inc}


def make_model(c: dict[str, Any], target: float, refs: dict[str, float], stage: str, idx: int) -> dict[str, Any]:
    base = base_cfg(c)
    obj = core.build_model(base, "ede_n3", smoke=False, restart=0)
    set_refs(obj, refs, skip={"H0"})
    core.freeze_param_value(obj["params"], "H0", float(target))
    opt = c["optimizer"][stage]
    minimize = obj["sampler"]["minimize"]
    minimize["seed"] = int(opt["seed_base"]) + int(idx)
    minimize["max_evals"] = int(opt["max_evals"])
    minimize["override_bobyqa"]["rhoend"] = float(opt["rhoend"])
    minimize["override_bobyqa"]["rhobeg"] = float(opt["rhobeg"])
    return obj


def result_file(c: dict[str, Any], stage: str, target: float, family: str) -> Path:
    p = ROOT / c["paths"]["results"] / f"q011_{stage}_h0_{htag(target)}_{family}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def render_file(c: dict[str, Any], stage: str, target: float, family: str) -> Path:
    p = ROOT / c["paths"]["rendered"] / f"q011_{stage}_h0_{htag(target)}_{family}.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def boundary_diagnostics(c: dict[str, Any], bestfit: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for name, spec in c["gates"]["boundary_parameters"].items():
        v = bestfit.get(name)
        if not isinstance(v, (int, float)):
            continue
        lo, hi = float(spec["min"]), float(spec["max"])
        span = hi - lo
        if span <= 0:
            continue
        frac = min((float(v)-lo)/span, (hi-float(v))/span)
        out.append({
            "parameter": name,
            "value": float(v),
            "distance_fraction_to_nearest_boundary": float(frac),
            "near_boundary": frac <= float(spec["fraction_tol"]),
        })
    return out


def run_optimizer(c: dict[str, Any], q008: dict[str, Any], target: float, family: str, idx: int, recipe: dict[str, Any], stage: str, parent: dict[str, Any] | None = None) -> int:
    if parent is None:
        refs, provenance = start_vector(c, q008, target, recipe)
    else:
        if parent.get("status") != "PASS":
            dump_json(result_file(c, stage, target, family), {
                "q": "Q011", "run_id": c["project"]["run_id"], "stage": stage,
                "target_h0": target, "start_family": family, "status": "FAIL",
                "reason": "PARENT_STAGE_NOT_PASS",
            })
            return 8
        refs = extract_vector(parent["bestfit"], set(sampled_specs(core.build_model(base_cfg(c), "ede_n3", smoke=False, restart=0))))
        refs["H0"] = float(target)
        provenance = f"Exact {parent['stage']} endpoint"

    obj = make_model(c, target, refs, stage, idx)
    obj["output"] = str((ROOT / c["paths"]["results"] / f"cobaya_q011_{stage}_{htag(target)}_{family}").resolve())
    rendered = render_file(c, stage, target, family)
    rendered.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

    rc = core.cobaya_run(rendered)
    base = base_cfg(c)
    rec: dict[str, Any] = {
        "q": "Q011",
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "stage": stage,
        "model": "ede_n3",
        "target_h0": float(target),
        "start_family": family,
        "profile_index": int(idx),
        "start_provenance": provenance,
        "start_vector_sha256": canonical_hash(refs),
        "optimizer": c["optimizer"][stage],
        "rendered_yaml": str(rendered),
        "rendered_yaml_sha256": sha256_file(rendered),
        "cobaya_exit": int(rc),
        "status": "FAIL",
        "scientific_surface": "FROZEN_Q005_V14",
    }

    prefix = Path(obj["output"])
    one = core.find_onepoint(prefix)
    if rc == 0 and one is not None:
        parsed = core.parse_onepoint(one, base)
        required = set(base["likelihood_accounting"]["required_nonlocal"])
        ok, reason = core.finite_scientific_point(parsed, required)
        rec["bestfit"] = parsed
        rec["finite_scientific_gate"] = bool(ok)
        if ok:
            rec["chi2_components"] = {k: float(parsed["chi2_nonoverlap"][k]) for k in sorted(required)}
            rec["chi2_scientific_total"] = float(sum(rec["chi2_components"].values()))
            rec["boundary_diagnostics"] = boundary_diagnostics(c, parsed)
            rec["status"] = "PASS"
        else:
            rec["reason"] = reason
    else:
        rec["reason"] = f"COBAYA_EXIT_{rc}" if rc else "NO_ONEPOINT_RESULT"

    if parent and rec.get("status") == "PASS":
        rec["delta_chi2_vs_parent"] = float(rec["chi2_scientific_total"]) - float(parent["chi2_scientific_total"])
    dump_json(result_file(c, stage, target, family), rec)
    return 0 if rec["status"] == "PASS" else 9


def find_result(root: str | Path, stage: str, target: float, family: str) -> Path:
    name = f"q011_{stage}_h0_{htag(target)}_{family}.json"
    hits = list(Path(root).rglob(name))
    if len(hits) != 1:
        raise RuntimeError(f"RESULT_LOOKUP_GATE=FAIL stage={stage} h0={target} family={family} hits={len(hits)}")
    return hits[0]


def norm_distance(a: dict[str, Any], b: dict[str, Any], bounds: dict[str, tuple[float,float]], names: list[str]) -> float:
    ss = 0.0
    n = 0
    for name in names:
        av, bv = a.get(name), b.get(name)
        if not isinstance(av, (int,float)) or not isinstance(bv, (int,float)):
            continue
        lo, hi = bounds.get(name, (0.0, 0.0))
        span = hi-lo
        if span <= 0:
            continue
        ss += ((float(av)-float(bv))/span)**2
        n += 1
    return math.sqrt(ss/max(1,n))


def cluster_records(c: dict[str, Any], recs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    m = core.build_model(base_cfg(c), "ede_n3", smoke=False, restart=0)
    bounds = bounds_from_specs(sampled_specs(m))
    names = sorted(k for k in bounds if k != "H0")
    dmax = float(c["gates"]["basin_parameter_rms_fraction"])
    cmax = float(c["gates"]["basin_delta_chi2"])
    clusters: list[dict[str, Any]] = []
    for rec in sorted(recs, key=lambda r: float(r["chi2_scientific_total"])):
        assigned = None
        for cl in clusters:
            rep = cl["representative"]
            if abs(float(rec["chi2_scientific_total"])-float(rep["chi2_scientific_total"])) <= cmax:
                if norm_distance(rec["bestfit"], rep["bestfit"], bounds, names) <= dmax:
                    assigned = cl
                    break
        if assigned is None:
            assigned = {"basin_id": f"BASIN-{len(clusters)+1:02d}", "representative": rec, "members": []}
            clusters.append(assigned)
        assigned["members"].append({
            "stage": rec["stage"],
            "start_family": rec["start_family"],
            "chi2": rec["chi2_scientific_total"],
        })
    for cl in clusters:
        cl["member_count"] = len(cl["members"])
        cl["chi2_min"] = min(float(x["chi2"]) for x in cl["members"])
        cl["chi2_max"] = max(float(x["chi2"]) for x in cl["members"])
    return clusters


def classify_target(c: dict[str, Any], target: float, recs: list[dict[str, Any]], q008: dict[str, Any]) -> dict[str, Any]:
    valid = [r for r in recs if r.get("status") == "PASS"]
    if not valid:
        return {"target_h0": target, "classification": "NUMERICALLY UNSTABLE / UNRESOLVED", "reason": "NO_VALID_STARTS"}

    valid.sort(key=lambda r: float(r["chi2_scientific_total"]))
    best = valid[0]
    best_chi2 = float(best["chi2_scientific_total"])
    clusters = cluster_records(c, valid)
    rep_tol = float(c["gates"]["replication_delta_chi2"])
    near = [r for r in valid if float(r["chi2_scientific_total"]) <= best_chi2 + rep_tol]
    distinct_families = sorted({r["start_family"] for r in near})
    boundary = [x for x in best.get("boundary_diagnostics", []) if x.get("near_boundary")]

    profiles = q008["profile_targets"]
    q8rec = profiles[numeric_key(profiles, target)]
    q8chi = float(q8rec["best_observed_chi2"])
    improvement = best_chi2 - q8chi
    q8_reproduced = any(abs(float(r["chi2_scientific_total"]) - q8chi) <= rep_tol for r in valid)
    materially_lower = improvement <= -float(c["gates"]["material_improvement_delta_chi2"])

    min_valid = int(c["gates"]["minimum_valid_starts"])
    min_rep = int(c["gates"]["minimum_replicating_families"])
    spread = max(float(r["chi2_scientific_total"]) for r in near) - min(float(r["chi2_scientific_total"]) for r in near)

    if len(valid) < min_valid:
        classification = "NUMERICALLY UNSTABLE / UNRESOLVED"
        reason = "INSUFFICIENT_VALID_STARTS"
    elif materially_lower:
        classification = "BEST-OBSERVED MINIMUM ONLY"
        reason = "Q008_SUPERSEDED_BY_MATERIALLY_LOWER_BASIN"
    elif len(distinct_families) >= min_rep and not boundary and spread <= rep_tol:
        classification = "GLOBALITY NOT PROVEN BUT STRONG NUMERICAL CERTIFICATION ACHIEVED"
        reason = "BROAD_START_FAMILY_REPLICATION_WITHOUT_MATERIAL_LOWER_COMPETITOR"
    else:
        classification = "BEST-OBSERVED MINIMUM ONLY"
        reason = "FINITE_SEARCH_DID_NOT_MEET_STRONG_CERTIFICATION_GATE"

    return {
        "target_h0": float(target),
        "classification": classification,
        "classification_reason": reason,
        "mathematical_globality_proven": False,
        "best_chi2": best_chi2,
        "best_record": best,
        "q008_best_observed_chi2": q8chi,
        "delta_chi2_best_minus_q008": improvement,
        "q008_minimum_reproduced": q8_reproduced,
        "materially_lower_than_q008": materially_lower,
        "valid_independent_results": len(valid),
        "replicating_start_families": distinct_families,
        "replication_count": len(distinct_families),
        "replication_spread": spread,
        "boundary_flags_best": boundary,
        "distinct_basin_count": len(clusters),
        "basins": clusters,
    }


def preflight(c: dict[str, Any], q008: dict[str, Any] | None = None) -> dict[str, Any]:
    base = base_cfg(c)
    checks = {
        "Q_IDENTITY_GATE": c["project"]["q"] == "Q011",
        "BASE_Q_GATE": base["project"]["q"] == "Q-005",
        "MODEL_GATE": c["profile"]["model"] == "ede_n3",
        "TARGET_GATE": [float(x) for x in c["profile"]["h0_targets"]] == [70.853292, 71.5, 72.5, 73.5],
        "FROZEN_BACKEND_GATE": bool(c["claim_boundary"]["frozen_q005_v14_surface"]),
        "NO_BOUND_CHANGE_GATE": bool(c["claim_boundary"]["no_primary_science_changes"]),
    }
    if q008 is not None:
        checks["Q008_PARENT_GATE"] = q008.get("q") == "Q-008" and isinstance(q008.get("profile_targets"), dict)
    return {"q": "Q011", "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}


def aggregate(c: dict[str, Any], q008: dict[str, Any], s1root: str, s2root: str, output: str) -> int:
    inv = matrix(c)["include"]
    all_by_target: dict[float, list[dict[str, Any]]] = {float(h): [] for h in c["profile"]["h0_targets"]}
    failures = []
    missing = []
    for spec in inv:
        h, fam = float(spec["target_h0"]), spec["start_family"]
        for stage, root in (("stage1", s1root), ("stage2", s2root)):
            try:
                p = find_result(root, stage, h, fam)
                r = load_json(p)
                if r.get("q") != "Q011":
                    raise RuntimeError("Q_IDENTITY_GATE=FAIL")
                if r.get("status") == "PASS":
                    all_by_target[h].append(r)
                else:
                    failures.append(r)
            except Exception as e:
                missing.append({"stage": stage, "target_h0": h, "start_family": fam, "error": str(e)})

    targets = {}
    ref = float(c["profile"]["authoritative_reference_chi2"])
    for h in c["profile"]["h0_targets"]:
        h = float(h)
        rec = classify_target(c, h, all_by_target[h], q008)
        if "best_chi2" in rec:
            rec["delta_chi2_vs_optimizer_native_reference"] = float(rec["best_chi2"]) - ref
        targets[str(h)] = rec

    classifications = [x["classification"] for x in targets.values()]
    if missing:
        combined = "NUMERICALLY UNSTABLE / UNRESOLVED"
    elif all(x == "GLOBALITY NOT PROVEN BUT STRONG NUMERICAL CERTIFICATION ACHIEVED" for x in classifications):
        combined = "GLOBALITY NOT PROVEN BUT STRONG NUMERICAL CERTIFICATION ACHIEVED"
    elif any(x == "NUMERICALLY UNSTABLE / UNRESOLVED" for x in classifications):
        combined = "NUMERICALLY UNSTABLE / UNRESOLVED"
    else:
        combined = "BEST-OBSERVED MINIMUM ONLY"

    result = {
        "q": "Q011",
        "run_id": c["project"]["run_id"],
        "result_identifier": c["project"]["result_id"],
        "code_version": CODE_VERSION,
        "status": "COMPLETE" if not missing else "PARTIAL",
        "scientific_question": c["project"]["scientific_question"],
        "frozen_scientific_configuration": c["frozen_scientific_configuration"],
        "search_design": {
            "start_recipes": recipes(c),
            "starts_per_target": len(recipes(c)),
            "targets": c["profile"]["h0_targets"],
            "stages": c["optimizer"],
            "basin_equivalence": {
                "delta_chi2_max": c["gates"]["basin_delta_chi2"],
                "normalized_parameter_rms_max": c["gates"]["basin_parameter_rms_fraction"],
            },
        },
        "job_inventory": {
            "expected_stage1": len(inv),
            "expected_stage2": len(inv),
            "expected_total_optimizer_jobs": 2 * len(inv),
            "missing_records": missing,
            "failure_records": failures,
        },
        "profile_targets": targets,
        "combined_globality_classification": combined,
        "mathematical_globality_proven": False,
        "authoritative_reference": {
            "h0": c["profile"]["authoritative_reference_h0"],
            "chi2": ref,
            "type": "optimizer-native",
        },
        "supersession_rule": (
            "If any Q011 target is materially lower than Q008, that Q008 target becomes "
            "superseded as the active best-observed minimum and Q009/Q010 attribution must "
            "be repeated only for materially changed targets."
        ),
        "routing_recommendation": (
            "If all high-H0 targets achieve strong numerical certification: route to external "
            "viability / physical-consistency testing. If lower minima are found: update profile "
            "and rerun only affected attribution. If unresolved: remain in numerical/HPC globality."
        ),
        "sources": c["sources"],
        "gates": {
            "Q_IDENTITY_GATE": "PASS",
            "FROZEN_BACKEND_GATE": "PASS",
            "JOB_COMPLETENESS_GATE": "PASS" if not missing else "FAIL",
            "GLOBALITY_GATE": combined,
            "FINAL_RESULT_GATE": "PASS" if not missing else "UNRESOLVED",
        },
    }
    dump_json(output, result)
    return 0 if not missing else 10


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("plan")
    p.add_argument("--json", action="store_true")

    p = sp.add_parser("preflight")
    p.add_argument("--q008")

    for stage in ("stage1", "stage2"):
        p = sp.add_parser(stage)
        p.add_argument("--q008", required=True)
        p.add_argument("--target-h0", required=True, type=float)
        p.add_argument("--start-family", required=True)
        p.add_argument("--profile-index", required=True, type=int)
        p.add_argument("--recipe-json", required=True)
        if stage == "stage2":
            p.add_argument("--stage1-root", required=True)

    p = sp.add_parser("aggregate")
    p.add_argument("--q008", required=True)
    p.add_argument("--stage1-root", required=True)
    p.add_argument("--stage2-root", required=True)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = cfg(a.config)

    if a.cmd == "plan":
        m = matrix(c)
        print(json.dumps(m, separators=(",", ":")) if a.json else json.dumps(m, indent=2))
        return 0

    if a.cmd == "preflight":
        q8 = load_json(a.q008) if a.q008 else None
        r = preflight(c, q8)
        print(json.dumps(r, indent=2))
        # Environment/scientific-backend validation is intentionally performed
        # inside the optimizer jobs after q005_setup_v14.sh has built the frozen
        # external backend. The planning job must not require that heavy setup.
        return 0 if r["status"] == "PASS" else 4

    q8 = load_json(a.q008)
    if preflight(c, q8)["status"] != "PASS":
        raise SystemExit("Q011_PREFLIGHT_GATE=FAIL")

    if a.cmd == "stage1":
        recipe = json.loads(a.recipe_json)
        return run_optimizer(c, q8, a.target_h0, a.start_family, a.profile_index, recipe, "stage1")

    if a.cmd == "stage2":
        recipe = json.loads(a.recipe_json)
        p = find_result(a.stage1_root, "stage1", a.target_h0, a.start_family)
        parent = load_json(p)
        return run_optimizer(c, q8, a.target_h0, a.start_family, a.profile_index, recipe, "stage2", parent=parent)

    if a.cmd == "aggregate":
        return aggregate(c, q8, a.stage1_root, a.stage2_root, a.output)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
