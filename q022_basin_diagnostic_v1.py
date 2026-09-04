#!/usr/bin/env python3
"""Bubbleverse Q022 — read-only coherent optimizer-basin diagnostic V1.

This program performs ZERO new likelihood evaluations. It consumes the completed
Q021 V1 profile artifacts, verifies that the Q021 V2 repair has been reproduced,
and compares full-MF coherent restart endpoints at every primordial vertex.

The output distinguishes association with profiled cosmology versus
shared/foreground nuisance structure. Static endpoint evidence is deliberately
not allowed to prove a purely numerical optimizer artifact; that diagnosis may
only be SUSPECTED/UNRESOLVED here and can trigger a later targeted globality run.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

Q = "Q022"
RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-DIAGNOSTIC-V1"
RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-001"
PARENT_Q = "Q021"
PARENT_RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
PARENT_RESULT = "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"
NRESTART = 3
NMASK = 8


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    os.replace(t, p)


def load_cfg(path: str | Path) -> dict[str, Any]:
    c = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    rules = c["rules"]
    mandatory = (
        "no_new_likelihood_evaluations", "coherent_restart_only",
        "no_frankenstein_vertex_mixing", "v1_process_hash_not_scientific_identity",
        "preserve_q021_basin_spread", "no_cross_chain_chi2_sum",
        "functional_attribution_not_independent_physical_chi2",
        "parameter_difference_not_automatically_physical",
        "higher_objective_not_automatically_artifact",
    )
    if not all(rules.get(k) is True for k in mandatory):
        raise RuntimeError("INTERPRETATION_RULE_GATE=FAIL")
    return c


def load_q021_v2(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("q") != PARENT_Q:
        raise RuntimeError("PARENT_Q_IDENTITY_GATE=FAIL")
    if d.get("result_id") != "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-002":
        raise RuntimeError("PARENT_RESULT_IDENTITY_GATE=FAIL")
    if d.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("PARENT_FINAL_RESULT_GATE=FAIL")
    gates = d.get("gates", {})
    required = (
        "JOB_COMPLETENESS_GATE", "FINITE_RESULT_GATE",
        "LIKELIHOOD_STRUCTURAL_IDENTITY_GATE",
        "COHERENT_RESTART_DECOMPOSITION_GATE",
        "NO_FRANKENSTEIN_VERTEX_MIXING_GATE",
        "NO_CROSS_CHAIN_CHI2_SUM_GATE", "INTERPRETATION_SAFETY_GATE",
    )
    if not all(gates.get(k) is True for k in required):
        raise RuntimeError("PARENT_MANDATORY_GATE=FAIL")
    return d


def collect_raw(root: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in Path(root).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if (d.get("q") == PARENT_Q and d.get("run_id") == PARENT_RUN
                and d.get("result_id") == PARENT_RESULT
                and d.get("stage") == "Q021_PRIMORDIAL_PROFILE"):
            rows.append(d)
    return rows


def flatten_numeric(row: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    minimum = row.get("minimum", {})
    nuisance = row.get("nuisance", {})
    if isinstance(minimum, Mapping):
        for k, v in minimum.items():
            if finite(v):
                out[str(k)] = float(v)
    if isinstance(nuisance, Mapping):
        for k, v in nuisance.items():
            if finite(v):
                out[str(k)] = float(v)
    return out


def complete_full_mf(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], bool]:
    rr = [r for r in rows if r.get("architecture") == "full_mf"
          and r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
    expected = {(m, r) for m in range(NMASK) for r in range(NRESTART)}
    got = {(int(x["mask"]), int(x["restart"])) for x in rr}
    return rr, got == expected and len(rr) == len(expected)


def within_vertex_scales(rows: list[dict[str, Any]], names: list[str], floor_fraction: float) -> dict[str, float]:
    bymask: dict[int, list[dict[str, float]]] = defaultdict(list)
    for r in rows:
        bymask[int(r["mask"])].append(flatten_numeric(r))
    scales: dict[str, float] = {}
    for name in names:
        diffs: list[float] = []
        vals_all: list[float] = []
        for m in range(NMASK):
            vals = [x[name] for x in bymask[m] if name in x]
            vals_all.extend(vals)
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    diffs.append(abs(vals[i] - vals[j]))
        positive = [d for d in diffs if d > 0]
        if positive:
            s = float(np.median(positive))
        elif vals_all:
            span = max(vals_all) - min(vals_all)
            s = float(span) if span > 0 else max(abs(float(np.median(vals_all))) * floor_fraction, floor_fraction)
        else:
            s = 1.0
        scales[name] = max(s, floor_fraction)
    return scales


def rms_distance(a: Mapping[str, float], b: Mapping[str, float], names: list[str], scales: Mapping[str, float]) -> float | None:
    z = []
    for n in names:
        if n in a and n in b and scales.get(n, 0) > 0:
            z.append((a[n] - b[n]) / scales[n])
    if not z:
        return None
    return float(math.sqrt(sum(x * x for x in z) / len(z)))


def bootstrap_ratio(cosmo: list[float], nuisance: list[float], samples: int, seed: int) -> dict[str, float | None]:
    if not cosmo or not nuisance or len(cosmo) != len(nuisance):
        return {"median": None, "p16": None, "p84": None}
    rng = np.random.default_rng(seed)
    ratios = []
    n = len(cosmo)
    for _ in range(samples):
        idx = rng.integers(0, n, size=n)
        c = float(np.mean([cosmo[i] for i in idx]))
        u = float(np.mean([nuisance[i] for i in idx]))
        ratios.append(c / u if u > 0 else math.inf)
    arr = np.asarray(ratios, dtype=float)
    finite_arr = arr[np.isfinite(arr)]
    if finite_arr.size == 0:
        return {"median": math.inf, "p16": math.inf, "p84": math.inf}
    return {
        "median": float(np.quantile(finite_arr, 0.50)),
        "p16": float(np.quantile(finite_arr, 0.16)),
        "p84": float(np.quantile(finite_arr, 0.84)),
    }


def analyse(c: Mapping[str, Any], rows: list[dict[str, Any]], q021: Mapping[str, Any]) -> dict[str, Any]:
    full, complete = complete_full_mf(rows)
    pg = c["parameter_groups"]
    cosmo = list(pg["cosmology_profiled"])
    shared = list(pg["shared_nuisance"])
    foreground = list(pg["foreground_nuisance"])
    nuisance = shared + foreground
    all_names = cosmo + nuisance
    scales = within_vertex_scales(full, all_names, float(c["analysis"]["scale_floor_fraction"]))

    bykey = {(int(r["mask"]), int(r["restart"])): r for r in full}
    vertices = []
    cdist: list[float] = []
    ndist: list[float] = []
    fdist: list[float] = []
    objective_gaps: list[float] = []
    best_restart_sequence: list[int] = []
    near_identity_large_gap = 0

    near_thr = float(c["analysis"]["endpoint_near_identity_rms"])
    obj_thr = float(c["analysis"]["objective_materiality"])

    for m in range(NMASK):
        trio = [bykey[(m, r)] for r in range(NRESTART)] if complete else []
        if not trio:
            continue
        objectives = [float(x["objective_chi2"]) for x in trio]
        best = int(np.argmin(objectives))
        best_restart_sequence.append(best)
        base = flatten_numeric(trio[best])
        comparisons = []
        for r in range(NRESTART):
            if r == best:
                continue
            x = flatten_numeric(trio[r])
            dc = rms_distance(base, x, cosmo, scales)
            dn = rms_distance(base, x, nuisance, scales)
            df = rms_distance(base, x, foreground, scales)
            gap = float(objectives[r] - objectives[best])
            if dc is not None: cdist.append(dc)
            if dn is not None: ndist.append(dn)
            if df is not None: fdist.append(df)
            objective_gaps.append(gap)
            joint = math.sqrt(((dc or 0.0) ** 2 + (dn or 0.0) ** 2) / 2.0)
            if gap >= obj_thr and joint <= near_thr:
                near_identity_large_gap += 1
            comparisons.append({
                "restart": r,
                "delta_objective_from_vertex_best": gap,
                "cosmology_rms": dc,
                "nuisance_rms": dn,
                "foreground_rms": df,
                "joint_rms": joint,
            })
        vertices.append({
            "mask": m,
            "objectives_by_restart": {str(r): objectives[r] for r in range(NRESTART)},
            "best_restart": best,
            "objective_spread": max(objectives) - min(objectives),
            "comparisons_to_vertex_best": comparisons,
        })

    mean_c = float(np.mean(cdist)) if cdist else None
    mean_n = float(np.mean(ndist)) if ndist else None
    mean_f = float(np.mean(fdist)) if fdist else None
    ratio = (mean_c / mean_n) if (mean_c is not None and mean_n not in (None, 0.0)) else None
    ratio_thr = float(c["analysis"]["association_ratio_threshold"])
    informative = sum(1 for v in vertices if v["objective_spread"] >= obj_thr)

    counts = {r: best_restart_sequence.count(r) for r in range(NRESTART)}
    modal = max(counts.values()) if counts else 0
    ordering_stability = modal / len(best_restart_sequence) if best_restart_sequence else 0.0

    if informative < int(c["analysis"]["minimum_informative_vertices"]):
        association = "INSUFFICIENT_OBJECTIVE_SEPARATION"
    elif ratio is not None and ratio >= ratio_thr:
        association = "PRIMARILY_COSMOLOGICAL_ENDPOINT_ASSOCIATION"
    elif ratio is not None and ratio <= 1.0 / ratio_thr:
        association = "PRIMARILY_NUISANCE_FOREGROUND_ENDPOINT_ASSOCIATION"
    elif ratio is not None:
        association = "MIXED_COSMOLOGY_AND_NUISANCE_ASSOCIATION"
    else:
        association = "IDENTIFIABILITY_LIMITED"

    optimizer_status = "NOT_ESTABLISHED_FROM_STATIC_ENDPOINTS"
    if near_identity_large_gap > 0:
        optimizer_status = "NUMERICAL_OPTIMIZER_STRUCTURE_SUSPECTED_NEEDS_TARGETED_GLOBALITY_TEST"
    elif ordering_stability < float(c["analysis"]["ordering_stability_fraction"]):
        optimizer_status = "RESTART_ORDERING_UNSTABLE_COMPATIBLE_WITH_MULTIBASIN_OR_NUMERICAL_STRUCTURE"

    # A static endpoint analysis can associate the spread with parameter groups,
    # but cannot alone prove a numerical artifact or a physical basin.
    if association == "PRIMARILY_COSMOLOGICAL_ENDPOINT_ASSOCIATION":
        classification = "COSMOLOGY-ASSOCIATED BASIN SEPARATION; PHYSICAL DISTINCTNESS NOT YET ESTABLISHED"
    elif association == "PRIMARILY_NUISANCE_FOREGROUND_ENDPOINT_ASSOCIATION":
        classification = "NUISANCE/FOREGROUND-ASSOCIATED BASIN SEPARATION; PHYSICAL DISTINCTNESS NOT YET ESTABLISHED"
    elif association == "MIXED_COSMOLOGY_AND_NUISANCE_ASSOCIATION":
        classification = "MIXED COSMOLOGY + NUISANCE BASIN SEPARATION"
    else:
        classification = "BASIN ORIGIN NOT IDENTIFIABLE FROM REUSED ENDPOINTS ALONE"

    boot = bootstrap_ratio(
        cdist, ndist,
        int(c["analysis"]["bootstrap_samples"]),
        int(c["analysis"]["bootstrap_seed"]),
    )

    return {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q022_READ_ONLY_BASIN_DIAGNOSTIC",
        "execution_mode": "PROGRAM_READ_ONLY_NO_LIKELIHOOD_EVALUATIONS",
        "actual_new_likelihood_evaluations": 0,
        "parent": {
            "q": PARENT_Q,
            "raw_run_id": PARENT_RUN,
            "authoritative_result_id": q021.get("result_id"),
            "authoritative_final_result_gate": q021.get("FINAL_RESULT_GATE"),
        },
        "raw_full_mf_profiles_found": len(full),
        "expected_full_mf_profiles": NMASK * NRESTART,
        "profile_completeness": complete,
        "normalization": {
            "type": "WITHIN_VERTEX_RESTART_SPREAD_NORMALISED_RMS",
            "parameter_scales": scales,
            "interpretation": "IDENTIFIABILITY_DIAGNOSTIC_NOT_PHYSICAL_DISTANCE_METRIC",
        },
        "vertices": vertices,
        "aggregate": {
            "mean_cosmology_rms": mean_c,
            "mean_nuisance_rms": mean_n,
            "mean_foreground_rms": mean_f,
            "cosmology_to_nuisance_ratio": ratio,
            "bootstrap_ratio": boot,
            "informative_vertices": informative,
            "best_restart_counts": counts,
            "best_restart_ordering_stability_fraction": ordering_stability,
            "near_identical_endpoint_large_objective_gap_count": near_identity_large_gap,
        },
        "association": association,
        "optimizer_structure_status": optimizer_status,
        "classification": classification,
        "interpretation_limits": [
            "Parameter endpoint differences do not establish physical distinctness.",
            "A higher objective does not by itself establish a numerical artifact.",
            "The metric is a within-Q021 numerical identifiability diagnostic, not a physical covariance metric.",
            "No matched/full-MF objectives are summed and no functional attribution term is treated as independent evidence.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--q021-v2", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    c = load_cfg(args.config)
    q021 = load_q021_v2(args.q021_v2)
    rows = collect_raw(args.input_dir)
    out = analyse(c, rows, q021)
    out["status"] = "PASS" if out["profile_completeness"] else "FAIL"
    out["FINAL_RESULT_GATE"] = "PROVISIONAL_PENDING_Q022_TESTS" if out["status"] == "PASS" else "FAIL"
    write_json(args.output, out)
    return 0 if out["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
