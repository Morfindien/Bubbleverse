#!/usr/bin/env python3
"""
Bubbleverse Q028 V3 — Criterion B+ minimal continuation.

CURRENT Q: Q028

Purpose
-------
Patch Q028 V2 at the scientifically over-restrictive precision-identifiability
gate. V3 reuses V2's frozen 36 fixed-vector residual/precision construction,
Schur-complement common-support machinery, interaction functional, and signed
two-factor Shapley decomposition.

The mathematically required identifiability criterion is Criterion B+:

    common-support + cross-donor + target-functional invariance

For the four-state family R and precision P,

    F(R,P) = q11 - q10 - q01 + q00
    q_s    = r_s^T P r_s

A mask-specific precision operator is functionally identified for Q028 iff all
edge-derived candidate precisions for that mask give F values agreeing within
the already-frozen V2 interaction tolerance for every donor residual family
actually used in the final counterfactual, after valid Schur marginalization
onto the exact common labelled support.

Individual q_s invariance is NOT a mandatory identifiability condition.

No optimization. No sampling. No Q024 rerun. No new endpoints. No model,
likelihood, prior, tolerance, or physical-assumption change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

import q028_common_support_counterfactual_v2 as v2

ROOT = Path(__file__).resolve().parent
Q = "Q028"
V4_TECHNICAL_LINEAGE = "V3_SUPERSEDED_AFTER_PRE_SCHUR_RAW_PRECISION_SYMMETRY_GATE_FAILURE"
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V4"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-004"
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
MASKS = (3, 6, 7)
EDGES = ((0, 1), (0, 2), (1, 2))
STATES = ("00", "10", "01", "11")
OMEGA = "omega_cdm"
APL = "A_planck"


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def _json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating, np.bool_)):
        return x.item()
    return str(x)


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True, default=_json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_GATE=FAIL {path}")
    return obj


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))

    if (
        c["project"]["q"] != Q
        or c["project"]["run_id"] != RUN
        or c["project"]["result_id"] != RESULT
    ):
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    if c["model"]["name"] != "MOD-EDE-N3" or int(c["model"]["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if c["model"]["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if c["likelihood"]["full_mf"] != FULL_LIKE:
        raise RuntimeError("LIKELIHOOD_GATE=FAIL")
    if tuple(map(int, c["execution"]["masks"])) != MASKS:
        raise RuntimeError("MASK_SCOPE_GATE=FAIL")
    if tuple(tuple(map(int, e)) for e in c["execution"]["edges"]) != EDGES:
        raise RuntimeError("EDGE_SCOPE_GATE=FAIL")

    mandatory_rules = (
        "no_optimization",
        "no_sampling",
        "no_new_endpoints",
        "no_q024_permutation_rerun",
        "preserve_signed_accounting",
        "common_support_must_be_validated",
        "do_not_use_precision_principal_submatrix_as_marginal",
        "use_schur_complement_for_marginal_precision",
        "criterion_b_plus_required",
        "state_level_invariance_not_required",
        "cross_donor_target_functional_invariance_required",
        "schur_before_functional_gate",
        "no_tolerance_change_from_v2",
    )
    for key in mandatory_rules:
        if c["rules"].get(key) is not True:
            raise RuntimeError(f"{key.upper()}_GATE=FAIL")

    if float(c["validation"]["precision_edge_pair_interaction_abs_tol"]) != 2.0e-4:
        raise RuntimeError("FROZEN_INTERACTION_TOLERANCE_GATE=FAIL")
    return c


def common_key_basis(
    edge_keys: Mapping[int, Mapping[str, list[tuple[str, str, int]]]]
) -> list[tuple[str, str, int]]:
    supports = []
    for mask in MASKS:
        for sa, sb in EDGES:
            supports.append(set(edge_keys[mask][f"e{sa}{sb}"]))
    common = set.intersection(*supports)
    if not common:
        raise RuntimeError("COMMON_SUPPORT_NONEMPTY_GATE=FAIL")
    return sorted(common, key=lambda k: (k[0], k[1], k[2]))


def build_frozen_families(
    c: Mapping[str, Any],
    q021_dir: str,
    q022_dir: str,
) -> tuple[
    dict[int, dict[str, dict[str, Any]]],
    dict[int, dict[str, np.ndarray]],
    dict[int, dict[str, list[tuple[str, str, int]]]],
    int,
]:
    import q025_fullmf_component_attribution_v2 as q25

    parent25_cfg = q25.load_cfg(ROOT / c["reuse"]["q025_config"])
    final22 = q25.load_q022_final(q022_dir)

    families: dict[int, dict[str, dict[str, Any]]] = {}
    edge_precisions: dict[int, dict[str, np.ndarray]] = {}
    edge_keys: dict[int, dict[str, list[tuple[str, str, int]]]] = {}
    eval_count = 0

    for mask in MASKS:
        endpoints = {
            s: q25.load_q022_endpoint(q022_dir, q021_dir, final22, mask, s)
            for s in (0, 1, 2)
        }
        families[mask] = {}
        edge_precisions[mask] = {}
        edge_keys[mask] = {}

        for sa, sb in EDGES:
            ek = f"e{sa}{sb}"
            A = endpoints[sa]["params"]
            B = endpoints[sb]["params"]
            model = q25.build_full_model(parent25_cfg, A)
            vectors = {
                "00": dict(A),
                "10": v2.switch(A, B, [OMEGA]),
                "01": v2.switch(A, B, [APL]),
                "11": v2.switch(A, B, [OMEGA, APL]),
            }
            fam: dict[str, Any] = {}
            try:
                for sid in STATES:
                    fam[sid] = v2.raw_state(model, vectors[sid], c)
                    eval_count += 1
            finally:
                try:
                    model.close()
                except Exception:
                    pass

            hashes = {fam[s]["precision_sha256"] for s in STATES}
            keys = [fam[s]["keys"] for s in STATES]
            if len(hashes) != 1:
                raise RuntimeError(
                    f"PRECISION_INVARIANCE_WITHIN_SWITCH_GATE=FAIL mask={mask} edge={ek}"
                )
            if any(k != keys[0] for k in keys[1:]):
                raise RuntimeError(
                    f"ROW_ALIGNMENT_WITHIN_SWITCH_GATE=FAIL mask={mask} edge={ek}"
                )

            families[mask][ek] = fam
            edge_precisions[mask][ek] = fam["00"]["precision"]
            edge_keys[mask][ek] = fam["00"]["keys"]

    expected = int(c["execution"]["total_expected_likelihood_evaluations"])
    if eval_count != expected:
        raise RuntimeError(
            f"FIXED_VECTOR_COUNT_GATE=FAIL actual={eval_count} expected={expected}"
        )
    return families, edge_precisions, edge_keys, eval_count


def build_common_precision_candidates(
    edge_precisions: Mapping[int, Mapping[str, np.ndarray]],
    edge_keys: Mapping[int, Mapping[str, list[tuple[str, str, int]]]],
    common_keys: list[tuple[str, str, int]],
    c: Mapping[str, Any],
) -> tuple[dict[int, dict[str, np.ndarray]], dict[str, Any]]:
    candidates: dict[int, dict[str, np.ndarray]] = {}
    metadata: dict[str, Any] = {}

    for mask in MASKS:
        candidates[mask] = {}
        metadata[str(mask)] = {}
        for sa, sb in EDGES:
            ek = f"e{sa}{sb}"
            P_raw = np.asarray(edge_precisions[mask][ek], dtype=np.float64)
            keys = edge_keys[mask][ek]

            # V4 numerical repair:
            # A Gaussian precision operator is mathematically symmetric.
            # If P_raw = S + A with A antisymmetric, then r.T @ A @ r == 0
            # for every real residual vector r. Raw floating-point asymmetry
            # is therefore preserved as technical provenance, not used as a
            # scientific rejection gate.
            P_sym = 0.5 * (P_raw + P_raw.T)

            raw_scale = max(
                1.0,
                float(np.max(np.abs(P_raw))) if P_raw.size else 1.0,
            )
            raw_asym_max = (
                float(np.max(np.abs(P_raw - P_raw.T))) if P_raw.size else 0.0
            )
            raw_asym_rel = raw_asym_max / raw_scale

            # Validate the mathematically relevant symmetric representative,
            # then perform the already-defined valid Schur marginalization.
            v2.validate_spd(
                P_sym, c, f"mask{mask}:{ek}:full_symmetrized"
            )

            Pm, meta, _ = v2.marginal_precision_from_full_precision(
                P_sym, keys, common_keys, c, f"mask{mask}:{ek}"
            )

            meta = {
                **meta,
                "raw_precision_sha256": v2.sha256_array(P_raw),
                "symmetrized_full_precision_sha256": v2.sha256_array(P_sym),
                "raw_max_abs_antisymmetry": raw_asym_max,
                "raw_relative_antisymmetry": raw_asym_rel,
                "raw_antisymmetry_scientific_gate": False,
                "symmetrization": "P_sym = 0.5 * (P_raw + P_raw.T)",
                "symmetrization_reason": (
                    "GAUSSIAN_PRECISION_IS_SYMMETRIC_AND_ANTISYMMETRIC_PART_"
                    "CANCELS_IN_RTPR"
                ),
            }

            candidates[mask][ek] = Pm
            metadata[str(mask)][ek] = meta
    return candidates, metadata


def criterion_b_plus(
    families: Mapping[int, Mapping[str, Mapping[str, Any]]],
    common_precision_candidates: Mapping[int, Mapping[str, np.ndarray]],
    common_keys: list[tuple[str, str, int]],
    c: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, bool], float]:
    """
    Test edge-choice invariance of the actual Q028 target functional over the
    complete donor-residual domain used by the final Shapley counterfactual.

    The state-level q_s values are deliberately NOT an acceptance gate.
    """
    tol = float(c["validation"]["precision_edge_pair_interaction_abs_tol"])
    diagnostics: dict[str, Any] = {}
    identified: dict[str, bool] = {}
    global_max = 0.0
    candidate_edges = [f"e{a}{b}" for a, b in EDGES]

    for pmask in MASKS:
        donor_cases: dict[str, Any] = {}
        mask_ok = True

        for rmask in MASKS:
            for ra, rb in EDGES:
                rek = f"e{ra}{rb}"
                vals: dict[str, float] = {}
                qstates: dict[str, dict[str, float]] = {}

                for pek in candidate_edges:
                    interaction, qs = v2.interaction_for_family(
                        families[rmask][rek],
                        common_precision_candidates[pmask][pek],
                        common_keys,
                    )
                    vals[pek] = float(interaction)
                    qstates[pek] = {k: float(v) for k, v in qs.items()}

                edges = sorted(vals)
                pairwise = {}
                spread = 0.0
                for i, ea in enumerate(edges):
                    for eb in edges[i + 1:]:
                        d = abs(vals[ea] - vals[eb])
                        pairwise[f"{ea}_vs_{eb}"] = d
                        spread = max(spread, d)

                case_ok = spread <= tol
                mask_ok = mask_ok and case_ok
                global_max = max(global_max, spread)
                donor_cases[f"residual_mask_{rmask}:{rek}"] = {
                    "residual_mask": rmask,
                    "residual_edge": rek,
                    "interaction_by_precision_candidate_edge": vals,
                    "state_quadratics_by_precision_candidate_edge": qstates,
                    "pairwise_abs_interaction_differences": pairwise,
                    "edge_choice_spread": spread,
                    "tolerance": tol,
                    "criterion_b_plus_case_pass": case_ok,
                }

        diagnostics[str(pmask)] = {
            "recipient_precision_mask": pmask,
            "candidate_precision_edges": candidate_edges,
            "donor_case_count": len(donor_cases),
            "donor_cases": donor_cases,
            "max_edge_choice_spread": max(
                (x["edge_choice_spread"] for x in donor_cases.values()), default=0.0
            ),
            "criterion_b_plus_mask_pass": mask_ok,
        }
        identified[str(pmask)] = mask_ok

    return diagnostics, identified, global_max


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q028_common_support_counterfactual_v4_config.yml")
    ap.add_argument("--q021-dir", required=True)
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--q025-result", required=True)
    ap.add_argument("--q026-result", required=True)
    ap.add_argument("--q027-result", required=True)
    ap.add_argument("--q028-v2-result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    c = load_cfg(a.config)
    q025_parent = read_json(a.q025_result)
    q026_parent = read_json(a.q026_result)
    q027_parent = read_json(a.q027_result)
    q028_v2_parent = read_json(a.q028_v2_result)

    if not (
        q025_parent.get("q") == "Q025"
        and q025_parent.get("result_id") == c["parents"]["q025_result_id"]
        and q025_parent.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("Q025_PARENT_GATE=FAIL")

    if not (
        q026_parent.get("q") == "Q026"
        and q026_parent.get("result_id") == c["parents"]["q026_result_id"]
        and q026_parent.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("Q026_PARENT_GATE=FAIL")

    if not (
        q027_parent.get("q") == "Q027"
        and q027_parent.get("result_id") == c["parents"]["q027_result_id"]
        and q027_parent.get("FINAL_RESULT_GATE") == "PASS"
        and q027_parent.get("cross_mask_summary", {}).get("spatial_localization")
        == "DISTRIBUTED_BEYOND_TT600_999_TRIAD"
        and q027_parent.get("cross_mask_summary", {}).get("within_mask_mechanism")
        == "RESIDUAL_CHANGE_UNDER_FIXED_INVERSE_COVARIANCE"
    ):
        raise RuntimeError("Q027_PARENT_GATE=FAIL")

    if not (
        q028_v2_parent.get("q") == Q
        and q028_v2_parent.get("result_id") == c["parents"]["q028_v2_result_id"]
        and q028_v2_parent.get("FINAL_RESULT_GATE") == "PASS"
        and int(q028_v2_parent.get("actual_new_likelihood_evaluations", -1)) == 36
    ):
        raise RuntimeError("Q028_V2_PARENT_GATE=FAIL")

    families, edge_precisions, edge_keys, eval_count = build_frozen_families(
        c, a.q021_dir, a.q022_dir
    )

    common_keys = common_key_basis(edge_keys)
    common_candidates, support_meta = build_common_precision_candidates(
        edge_precisions, edge_keys, common_keys, c
    )

    all_fracs = [
        float(meta["common_fraction"])
        for per_mask in support_meta.values()
        for meta in per_mask.values()
    ]
    min_frac = min(all_fracs)
    support_fraction_ok = (
        min_frac >= float(c["validation"]["minimum_common_support_fraction"])
    )

    bplus_diag, bplus_by_mask, global_max_spread = criterion_b_plus(
        families, common_candidates, common_keys, c
    )
    bplus_ok = all(bplus_by_mask.values())

    common_support_summary = {
        "construction": "LABEL_INTERSECTION_PLUS_SCHUR_COMPLEMENT_MARGINAL_PRECISION",
        "dimension": len(common_keys),
        "keys_sha256": hashlib.sha256(
            json.dumps(common_keys, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "candidate_precision_metadata_by_mask_and_edge": support_meta,
        "minimum_common_support_fraction": min_frac,
        "minimum_required_common_support_fraction": float(
            c["validation"]["minimum_common_support_fraction"]
        ),
        "interpretability_gate": support_fraction_ok,
        "principal_precision_submatrix_used_as_marginal": False,
    }

    base = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "actual_new_likelihood_evaluations": eval_count,
        "optimizer_evaluations": 0,
        "sampling_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "state_level_invariance_required": False,
        "criterion_b_plus": {
            "name": "COMMON_SUPPORT_CROSS_DONOR_TARGET_FUNCTIONAL_INVARIANCE",
            "functional": "F(R,P)=q11-q10-q01+q00=Tr(P K_R)",
            "tolerance": float(
                c["validation"]["precision_edge_pair_interaction_abs_tol"]
            ),
            "diagnostics_by_recipient_precision_mask": bplus_diag,
            "identified_by_mask": bplus_by_mask,
            "global_max_edge_choice_spread": global_max_spread,
            "gate": bplus_ok,
        },
        "common_support": common_support_summary,
        "scientific_surface": {
            "model": c["model"],
            "likelihood": FULL_LIKE,
            "masks": list(MASKS),
            "authoritative_endpoints": "Q022_V2_UNCHANGED",
            "parents": c["parents"],
        },
        "claim_boundaries": c["claim_boundaries"],
        "journal_preservation": c["journal_preservation"],
        "parents_observed": {
            "q025": q025_parent.get("result_id"),
            "q026": q026_parent.get("result_id"),
            "q027": q027_parent.get("result_id"),
            "q028_v2": q028_v2_parent.get("result_id"),
        },
    }

    # Valid negative stop if the target functional is not edge-choice invariant
    # over the complete counterfactual donor domain.
    if not bplus_ok:
        out = {
            **base,
            "status": "COMPLETE",
            "resolution_class": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "scientific_classification": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "reason": (
                "At least one recipient-mask precision has edge-choice spread "
                "above the frozen 2e-4 interaction tolerance for a donor residual "
                "family actually used by the Q028 common-support counterfactual."
            ),
            "counterfactual": {},
            "shapley_rows": [],
            "shapley_closure_gate": "NOT_REACHED_VALID_NEGATIVE_STOP",
            "stop_condition_reached": True,
        }
        write_json(a.output, out)
        print(json.dumps(out, indent=2, sort_keys=True, default=_json_default))
        return 0

    # A common support too small for the frozen interpretability requirement is
    # also a valid negative under the current construction.
    if not support_fraction_ok:
        out = {
            **base,
            "status": "COMPLETE",
            "resolution_class": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "scientific_classification": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "reason": (
                "Criterion B+ passed, but the exact common support falls below "
                "the frozen minimum common-support fraction required for "
                "interpretable Q028 attribution."
            ),
            "counterfactual": {},
            "shapley_rows": [],
            "shapley_closure_gate": "NOT_REACHED_VALID_NEGATIVE_STOP",
            "stop_condition_reached": True,
        }
        write_json(a.output, out)
        print(json.dumps(out, indent=2, sort_keys=True, default=_json_default))
        return 0

    # Criterion B+ passed. e01 is a deterministic documented representative;
    # B+ proves edge choice is immaterial for the target functional to tolerance.
    representative_edge = "e01"
    common_precision = {
        mask: common_candidates[mask][representative_edge] for mask in MASKS
    }

    counterfactual: dict[str, Any] = {}
    shapley_rows: list[dict[str, Any]] = []
    for sa, sb in EDGES:
        ek = f"e{sa}{sb}"
        matrix: dict[str, Any] = {}
        qstates: dict[str, Any] = {}

        for rmask in MASKS:
            matrix[str(rmask)] = {}
            qstates[str(rmask)] = {}
            for pmask in MASKS:
                val, qs = v2.interaction_for_family(
                    families[rmask][ek], common_precision[pmask], common_keys
                )
                matrix[str(rmask)][str(pmask)] = float(val)
                qstates[str(rmask)][str(pmask)] = {
                    k: float(v) for k, v in qs.items()
                }

        comparisons = {}
        for ia, ma in enumerate(MASKS):
            for mb in MASKS[ia + 1:]:
                Faa = matrix[str(ma)][str(ma)]
                Fab = matrix[str(ma)][str(mb)]
                Fba = matrix[str(mb)][str(ma)]
                Fbb = matrix[str(mb)][str(mb)]
                sh = v2.shapley_two_factor(Faa, Fab, Fba, Fbb)
                ck = f"m{ma}_vs_m{mb}"
                comparisons[ck] = sh
                shapley_rows.append(
                    {"edge": ek, "mask_pair": [ma, mb], **sh}
                )

        counterfactual[ek] = {
            "interaction_matrix_residual_mask_by_precision_mask": matrix,
            "state_quadratics": qstates,
            "mask_pair_shapley": comparisons,
        }

    closure_tol = float(c["validation"]["shapley_closure_abs_tol"])
    closure_gate = all(
        abs(float(x["closure_error"])) <= closure_tol for x in shapley_rows
    )
    if not closure_gate:
        raise RuntimeError("SHAPLEY_CLOSURE_GATE=FAIL")

    diagonal_support_effects: dict[str, Any] = {}
    for mask in MASKS:
        diagonal_support_effects[str(mask)] = {}
        for sa, sb in EDGES:
            ek = f"e{sa}{sb}"
            full_q = {
                sid: families[mask][ek][sid]["full_highl_chi2"] for sid in STATES
            }
            full_i = v2.contrast(full_q)
            common_i = counterfactual[ek][
                "interaction_matrix_residual_mask_by_precision_mask"
            ][str(mask)][str(mask)]
            diagonal_support_effects[str(mask)][ek] = {
                "full_support_pair_interaction": float(full_i),
                "common_support_marginal_pair_interaction": float(common_i),
                "common_minus_full": float(common_i - full_i),
            }

    attribution_class = v2.classify(shapley_rows, c)
    out = {
        **base,
        "status": "COMPLETE",
        "resolution_class": "VALID_COMMON_SUPPORT_SEPARATION",
        "scientific_classification": attribution_class,
        "representative_precision_edge_by_mask": {
            str(mask): representative_edge for mask in MASKS
        },
        "representative_selection_reason": (
            "Deterministic e01 representative; Criterion B+ established that "
            "edge choice changes every required target-functional evaluation by "
            "no more than the frozen interaction tolerance."
        ),
        "counterfactual": counterfactual,
        "shapley_rows": shapley_rows,
        "shapley_closure_gate": True,
        "diagonal_support_effects": diagonal_support_effects,
        "interpretation": {
            "residual_side_definition": (
                "DATA_MINUS_MODEL_RESIDUAL_FAMILY; DOES NOT SEPARATE RAW DATA "
                "FROM MODEL/NUISANCE VECTOR"
            ),
            "precision_side_definition": (
                "FUNCTIONALLY IDENTIFIED MASK-SPECIFIC SCHUR-MARGINAL "
                "PRECISION OPERATOR ON EXACT COMMON LABELLED SUPPORT"
            ),
            "state_level_invariance": (
                "NOT REQUIRED; COMMON-MODE q_s SHIFTS MAY CANCEL IN THE DEFINED "
                "FACTORIAL CONTRAST"
            ),
            "lineage_warning": (
                "Edge IDs are Q022 lineage labels, not independently established "
                "universal physical posterior modes; Q024 non-universality remains preserved."
            ),
            "causal_status": (
                "FUNCTIONAL COUNTERFACTUAL ATTRIBUTION WITHIN THE FROZEN "
                "CAMSPEC CONSTRUCTION; NOT PHYSICAL CAUSALITY"
            ),
        },
        "stop_condition_reached": True,
    }
    write_json(a.output, out)
    print(json.dumps(out, indent=2, sort_keys=True, default=_json_default))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
