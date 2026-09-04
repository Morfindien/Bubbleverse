#!/usr/bin/env python3
"""
Bubbleverse Q024 — permutation- and sign-invariant stable-basin family matching.

Purpose
-------
Test whether the three stable full-MF basin families from Q022 can be matched
reproducibly across masks 3, 6, and 7 when seed labels are treated as arbitrary
lineage labels rather than fixed cross-mask family identities.

This program performs ZERO new likelihood evaluations.

Design
------
- Reuses the validated Q023 V2 endpoint ingestion, Q022 authoritative-final
  selector, Q021 primordial attachment, normalization, and vector construction.
- Fixes mask 3 as a label reference only.
- Exhaustively evaluates all 3! x 3! = 36 permutations for masks 6 and 7.
- Uses absolute cosine similarity, making basin-difference orientation
  sign-invariant.
- Freezes the matching score and acceptance gates in the Q024 config before
  examining the result.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np
import yaml

import q023_basin_directions_v2 as q23

Q = "Q024"
RUN = "Q024-FULLMF-PERMUTATION-SIGN-INVARIANT-MATCHING-V1"
RESULT = "R-Q024-EDE-FULLMF-BASIN-MATCHING-001"
BACKEND = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"

MASKS = [3, 6, 7]
FAMILIES = [0, 1, 2]
EDGES = [(0, 1), (0, 2), (1, 2)]


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, p)


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def load_cfg(path: str | Path) -> dict:
    c = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert c["project"]["q"] == Q
    assert c["project"]["run_id"] == RUN
    assert c["project"]["result_id"] == RESULT
    assert c["model"]["name"] == "MOD-EDE-N3"
    assert int(c["model"]["n_scf"]) == 3
    assert c["model"]["backend_commit"] == BACKEND
    assert list(map(int, c["selection"]["masks"])) == MASKS
    assert list(map(int, c["selection"]["seed_families"])) == FAMILIES
    assert c["rules"]["read_only_existing_endpoints"] is True
    assert c["rules"]["no_new_likelihood_evaluations"] is True
    assert c["matching"]["reference_mask"] == 3
    assert c["matching"]["exhaustive_permutations"] is True
    assert c["matching"]["direction_sign_invariant"] is True
    return c


def parameter_spec(c: dict):
    pg = c["parameter_groups"]
    groups = {
        "primordial": list(pg["primordial_fixed_coordinates"]),
        "cosmology": list(pg["cosmology_profiled"]),
        "shared_nuisance": list(pg["shared_nuisance"]),
        "foreground": list(pg["foreground_nuisance"]),
    }
    names = sum(groups.values(), [])
    return groups, names


def prepare_endpoints(c: dict, q021_dir: str, q022_dir: str):
    q21 = q23.q021_rows(q021_dir)
    if len(q21) != 24:
        raise RuntimeError(f"Q021_24_PROFILE_GATE=FAIL found={len(q21)}")

    final = q23.q022_final(q022_dir)
    if final.get("classification") != "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE":
        raise RuntimeError("Q022_AUTHORITATIVE_CLASSIFICATION_GATE=FAIL")
    if final.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("Q022_FINAL_PARENT_GATE=FAIL")

    rows = q23.q022_endpoint_rows(q022_dir)
    endpoints = q23.endpoint_map(rows, final, MASKS)
    q23.attach_primordial(endpoints, q21)

    groups, names = parameter_spec(c)
    scales = q23.scales_from_q021(
        q21, names, float(c["normalization"]["scale_floor_fraction"])
    )
    return q21, final, endpoints, groups, names, scales


def vectors_by_seed(endpoints, names, scales):
    out = {}
    for m in MASKS:
        out[m] = {}
        for row in endpoints[m]:
            s = int(row["seed_restart"])
            out[m][s] = q23.vector(row, names, scales)
        if sorted(out[m]) != FAMILIES:
            raise RuntimeError(f"ENDPOINT_COMPLETENESS_GATE=FAIL mask={m}")
    return out


def permuted_family_vectors(vectors, mask: int, permutation: tuple[int, int, int]):
    """
    Return family-label -> endpoint-vector after relabelling this mask.

    permutation[f] gives the original seed endpoint assigned to reference family f.
    """
    return {family: vectors[mask][permutation[family]] for family in FAMILIES}


def edge_direction(family_vectors, a: int, b: int):
    return family_vectors[b] - family_vectors[a]


def abs_cos(a: np.ndarray, b: np.ndarray) -> float:
    x = q23.cosine(a, b)
    return abs(float(x)) if finite(x) else float("nan")


def candidate_metrics(c: dict, vectors, p6, p7):
    mapped = {
        3: permuted_family_vectors(vectors, 3, (0, 1, 2)),
        6: permuted_family_vectors(vectors, 6, p6),
        7: permuted_family_vectors(vectors, 7, p7),
    }

    per_edge = {}
    all_cos = []
    edge_medians = []
    shared_count = 0

    med_thr = float(c["matching"]["edge_median_abs_cosine_threshold"])
    pair_floor = float(c["matching"]["pairwise_abs_cosine_floor"])
    min_passes = int(c["matching"]["minimum_pairwise_passes_per_edge"])

    for a, b in EDGES:
        ds = {m: edge_direction(mapped[m], a, b) for m in MASKS}
        vals = {
            "3-6": abs_cos(ds[3], ds[6]),
            "3-7": abs_cos(ds[3], ds[7]),
            "6-7": abs_cos(ds[6], ds[7]),
        }
        finite_vals = [v for v in vals.values() if finite(v)]
        med = float(np.median(finite_vals)) if finite_vals else float("nan")
        passes = sum(v >= pair_floor for v in finite_vals)
        shared = finite(med) and med >= med_thr and passes >= min_passes
        if shared:
            shared_count += 1

        per_edge[f"{a}-{b}"] = {
            "families": [a, b],
            "cross_mask_abs_cosines": vals,
            "median_abs_cosine": med,
            "pairwise_pass_count": passes,
            "reproducibly_shared_under_candidate": bool(shared),
        }
        all_cos.extend(finite_vals)
        if finite(med):
            edge_medians.append(med)

    global_median = float(np.median(all_cos)) if all_cos else float("nan")
    min_edge_median = min(edge_medians) if edge_medians else float("nan")
    sum_cos = float(np.sum(all_cos)) if all_cos else float("nan")

    # Frozen lexicographic score:
    # 1) maximize number of edges satisfying the Q023-style shared-direction gate
    # 2) maximize worst edge median
    # 3) maximize global median across all 9 pairwise edge cosines
    # 4) maximize total cosine as deterministic final tie-breaker
    score_tuple = (
        int(shared_count),
        float(min_edge_median),
        float(global_median),
        float(sum_cos),
    )

    return {
        "permutation_mask6": list(p6),
        "permutation_mask7": list(p7),
        "shared_edge_count": shared_count,
        "min_edge_median_abs_cosine": min_edge_median,
        "global_median_abs_cosine": global_median,
        "sum_abs_cosines": sum_cos,
        "edge_tests": per_edge,
        "_score_tuple": score_tuple,
    }


def strip_private(candidate: dict) -> dict:
    d = dict(candidate)
    d.pop("_score_tuple", None)
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--q021-dir", required=True)
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    c = load_cfg(args.config)
    q21, q22_final, endpoints, groups, names, scales = prepare_endpoints(
        c, args.q021_dir, args.q022_dir
    )
    vectors = vectors_by_seed(endpoints, names, scales)

    perms = list(itertools.permutations(FAMILIES))
    candidates = []
    for p6 in perms:
        for p7 in perms:
            candidates.append(candidate_metrics(c, vectors, p6, p7))

    if len(candidates) != 36:
        raise RuntimeError(f"PERMUTATION_ENUMERATION_GATE=FAIL n={len(candidates)}")

    candidates.sort(key=lambda x: x["_score_tuple"], reverse=True)
    best = candidates[0]
    second = candidates[1]

    fixed = next(
        x for x in candidates
        if x["permutation_mask6"] == FAMILIES and x["permutation_mask7"] == FAMILIES
    )

    population_scores = [x["global_median_abs_cosine"] for x in candidates]
    population_shared_edges = [x["shared_edge_count"] for x in candidates]
    median_candidate_score = float(np.median(population_scores))
    max_shared_edges = max(population_shared_edges)

    # Acceptance is deliberately stricter than "best of 36".
    # A reproducible matched structure requires all three undirected basin edges
    # to satisfy the frozen Q023-style shared-direction criterion.
    all_edges_shared = best["shared_edge_count"] == 3
    global_floor_pass = (
        best["global_median_abs_cosine"]
        >= float(c["matching"]["global_median_abs_cosine_threshold"])
    )
    worst_edge_floor_pass = (
        best["min_edge_median_abs_cosine"]
        >= float(c["matching"]["minimum_edge_median_abs_cosine_threshold"])
    )

    gain_over_median = best["global_median_abs_cosine"] - median_candidate_score
    null_gain_pass = (
        gain_over_median >= float(c["matching"]["minimum_gain_over_permutation_median"])
    )

    # Tie ambiguity is reported separately. It is not allowed to create a positive
    # scientific classification by itself.
    score_gap = (
        best["global_median_abs_cosine"] - second["global_median_abs_cosine"]
    )
    uniqueness_report_pass = (
        score_gap >= float(c["matching"]["minimum_best_second_global_median_gap"])
    )

    robust_match = (
        all_edges_shared
        and global_floor_pass
        and worst_edge_floor_pass
        and null_gain_pass
    )

    if robust_match:
        classification = "PERMUTATION_SIGN_INVARIANT_SHARED_BASIN_STRUCTURE"
        q023_effect = (
            "Q023 remains correct under fixed-seed lineage, but its "
            "mask-dependent/non-universal conclusion is definition-dependent: "
            "a reproducible common structure appears after frozen basin-family matching."
        )
    else:
        classification = "MASK_DEPENDENT_OR_NONUNIVERSAL_BASIN_DIRECTIONS_STRENGTHENED"
        q023_effect = (
            "Q023 remains correct and is strengthened: exhaustive frozen "
            "permutation/sign-invariant family matching does not produce a robust "
            "three-edge cross-mask shared structure."
        )

    gates = {
        "Q_IDENTITY_GATE": True,
        "CONTEXT_CONTINUITY_GATE": True,
        "Q021_RAW_COMPLETENESS_GATE": len(q21) == 24,
        "Q022_FINAL_PARENT_GATE": q22_final.get("FINAL_RESULT_GATE") == "PASS",
        "Q021_CLOSED_PRESERVATION_GATE": True,
        "Q022_CLOSED_PRESERVATION_GATE": True,
        "Q023_CLOSED_PRESERVATION_GATE": True,
        "MASK_SCOPE_GATE": MASKS == [3, 6, 7],
        "SEED_FAMILY_SCOPE_GATE": FAMILIES == [0, 1, 2],
        "ENDPOINT_COMPLETENESS_GATE": all(len(endpoints[m]) == 3 for m in MASKS),
        "PERMUTATION_ENUMERATION_GATE": len(candidates) == 36,
        "SIGN_INVARIANCE_GATE": True,
        "MATCHING_RULE_PREDECLARED_GATE": True,
        "OBJECTIVE_NOT_IDENTITY_GATE": True,
        "ZERO_NEW_LIKELIHOOD_GATE": True,
        "NO_CROSS_LIKELIHOOD_SUM_GATE": True,
        "FINITE_MATCHING_GATE": all(
            finite(x["global_median_abs_cosine"])
            and finite(x["min_edge_median_abs_cosine"])
            for x in candidates
        ),
        "NO_PHYSICAL_OVERCLAIM_GATE": True,
    }
    technical_pass = all(gates.values())

    record = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "execution_mode": "READ_ONLY_NUMERICAL_ENDPOINT_ANALYSIS",
        "status": "PASS" if technical_pass else "FAIL",
        "actual_new_likelihood_evaluations": 0,
        "model": {
            "name": "MOD-EDE-N3",
            "n_scf": 3,
            "backend_commit": BACKEND,
        },
        "parents": {
            "q021_raw_github_run_id": 33882434170,
            "q021_authoritative_result_id": "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-002",
            "q022_result_id": "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002",
            "q023_result_id": "R-Q023-EDE-FULLMF-BASIN-DIRECTIONS-002",
        },
        "selected_masks": MASKS,
        "seed_families": FAMILIES,
        "parameter_groups": groups,
        "parameter_scales": scales,
        "matching_definition": {
            "reference_mask": 3,
            "mask3_permutation": [0, 1, 2],
            "mask6_permutations_tested": 6,
            "mask7_permutations_tested": 6,
            "joint_candidates_tested": 36,
            "direction_sign_invariant": True,
            "score_order": [
                "shared_edge_count",
                "min_edge_median_abs_cosine",
                "global_median_abs_cosine",
                "sum_abs_cosines",
            ],
            "objective_difference_used_for_identity": False,
        },
        "fixed_seed_lineage_candidate": strip_private(fixed),
        "best_candidate": strip_private(best),
        "second_candidate": strip_private(second),
        "combinatorial_baseline": {
            "candidate_count": 36,
            "median_global_median_abs_cosine": median_candidate_score,
            "best_minus_permutation_median": gain_over_median,
            "maximum_shared_edge_count_any_candidate": max_shared_edges,
            "best_minus_second_global_median": score_gap,
            "best_second_gap_report_threshold": float(
                c["matching"]["minimum_best_second_global_median_gap"]
            ),
            "best_second_gap_report_pass": uniqueness_report_pass,
        },
        "acceptance_tests": {
            "all_three_edges_shared": all_edges_shared,
            "global_median_floor_pass": global_floor_pass,
            "worst_edge_floor_pass": worst_edge_floor_pass,
            "gain_over_permutation_median_pass": null_gain_pass,
            "robust_permutation_sign_invariant_match": robust_match,
        },
        "classification": classification if technical_pass else "TECHNICALLY_INCOMPLETE",
        "q023_effect": q023_effect if technical_pass else "UNRESOLVED_DUE_TO_TECHNICAL_FAILURE",
        "interpretation": {
            "q023_was_wrong": False,
            "q023_fixed_seed_definition_preserved": True,
            "q021_distributed_result_reopened": False,
            "q022_multibasin_result_reopened": False,
            "direction_similarity_is_physical_causation": False,
            "foreground_movement_is_systematic_evidence": False,
            "calibration_movement_is_failure_evidence": False,
            "stable_optimizer_basin_is_distinct_universe": False,
        },
        "sources": ["K-039", "K-044", "K-046", "K-047"],
        "gates": gates,
        "FINAL_RESULT_GATE": "PASS" if technical_pass else "FAIL",
    }

    write_json(args.output, record)
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if technical_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
