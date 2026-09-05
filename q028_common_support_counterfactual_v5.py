#!/usr/bin/env python3
"""
Bubbleverse Q028 V5 — split/checkpointed Criterion B+ continuation.

V5 supersedes V4 as an execution architecture, not as a scientific result.

Why V5 exists
-------------
V4 fixed the raw precision symmetry issue, but two independent hosted-runner
attempts were terminated after all nine model/family constructions and before
a scientific result was written. V5 removes the monolithic memory/runtime
shape.

Architecture
------------
Phase A: FAMILY
  9 independent mask×edge jobs.
  Each job performs exactly 4 frozen fixed-vector likelihood evaluations and
  writes only keys, residual vectors, full-support chi2 values, and provenance.
  No dense precision matrix is serialized.

Phase B: SUPPORT
  Pure deterministic merge of the 9 family checkpoints.
  Computes the exact global labelled common support.

Phase C: PRECISION
  9 independent recipient mask×edge jobs.
  Each job reconstructs exactly one frozen precision operator without any new
  likelihood evaluation, symmetrizes it algebraically, and evaluates the full
  cross-donor Criterion B+ functional domain in one batched matrix operation.
  The mathematically valid Schur-marginal quadratic is evaluated without ever
  materializing a giant common-support precision matrix.

Phase D: MERGE
  Pure deterministic merge.
  Applies Criterion B+, then either:
    A) VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY
  or
    B) VALID_COMMON_SUPPORT_SEPARATION + signed Shapley decomposition.

Scientific constraints
----------------------
- Q028 only.
- frozen MOD-EDE-N3, n_scf=3.
- backend commit unchanged.
- full-MF CamSpec TTTEEE unchanged.
- Q022 V2 endpoints unchanged.
- no optimization.
- no sampling.
- no Q024 rerun.
- exactly 36 new likelihood evaluations total, all in Phase A.
- no tolerance change from V2.
- state-level q invariance is diagnostic only, never the Criterion B+ gate.
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
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V5"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-005"
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


def json_default(x: Any) -> Any:
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
        json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL {path}")
    return obj


def edge_key(sa: int, sb: int) -> str:
    if (sa, sb) not in EDGES:
        raise RuntimeError(f"EDGE_SCOPE_GATE=FAIL {(sa, sb)}")
    return f"e{sa}{sb}"


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))

    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_RESULT_IDENTITY_GATE=FAIL")
    if c["model"]["name"] != "MOD-EDE-N3" or int(c["model"]["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if c["model"]["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if c["likelihood"]["full_mf"] != FULL_LIKE:
        raise RuntimeError("LIKELIHOOD_GATE=FAIL")
    if tuple(map(int, c["execution"]["masks"])) != MASKS:
        raise RuntimeError("MASK_SCOPE_GATE=FAIL")
    if tuple(tuple(map(int, x)) for x in c["execution"]["edges"]) != EDGES:
        raise RuntimeError("EDGE_SCOPE_GATE=FAIL")
    if int(c["execution"]["total_expected_likelihood_evaluations"]) != 36:
        raise RuntimeError("FIXED_VECTOR_BUDGET_GATE=FAIL")
    if int(c["execution"]["family_jobs"]) != 9:
        raise RuntimeError("FAMILY_JOB_COUNT_GATE=FAIL")
    if int(c["execution"]["precision_jobs"]) != 9:
        raise RuntimeError("PRECISION_JOB_COUNT_GATE=FAIL")
    if int(c["execution"]["likelihood_evaluations_per_family_job"]) != 4:
        raise RuntimeError("FAMILY_EVAL_BUDGET_GATE=FAIL")

    must_true = (
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
        "precision_symmetrization_required",
        "no_dense_precision_checkpoint_artifacts",
        "no_materialized_full_common_precision_in_v5",
        "reuse_v2_full_precision_spd_provenance",
    )
    for k in must_true:
        if c["rules"].get(k) is not True:
            raise RuntimeError(f"{k.upper()}_GATE=FAIL")

    if float(c["validation"]["precision_edge_pair_interaction_abs_tol"]) != 2.0e-4:
        raise RuntimeError("FROZEN_INTERACTION_TOLERANCE_GATE=FAIL")
    return c


def load_parents(c: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    p25 = read_json(args.q025_result)
    p26 = read_json(args.q026_result)
    p27 = read_json(args.q027_result)
    p28 = read_json(args.q028_v2_result)

    if not (
        p25.get("q") == "Q025"
        and p25.get("result_id") == c["parents"]["q025_result_id"]
        and p25.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("Q025_PARENT_GATE=FAIL")
    if not (
        p26.get("q") == "Q026"
        and p26.get("result_id") == c["parents"]["q026_result_id"]
        and p26.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("Q026_PARENT_GATE=FAIL")
    if not (
        p27.get("q") == "Q027"
        and p27.get("result_id") == c["parents"]["q027_result_id"]
        and p27.get("FINAL_RESULT_GATE") == "PASS"
        and p27.get("cross_mask_summary", {}).get("spatial_localization")
        == "DISTRIBUTED_BEYOND_TT600_999_TRIAD"
        and p27.get("cross_mask_summary", {}).get("within_mask_mechanism")
        == "RESIDUAL_CHANGE_UNDER_FIXED_INVERSE_COVARIANCE"
    ):
        raise RuntimeError("Q027_PARENT_GATE=FAIL")
    if not (
        p28.get("q") == Q
        and p28.get("result_id") == c["parents"]["q028_v2_result_id"]
        and p28.get("FINAL_RESULT_GATE") == "PASS"
        and int(p28.get("actual_new_likelihood_evaluations", -1)) == 36
    ):
        raise RuntimeError("Q028_V2_PARENT_GATE=FAIL")
    return {"q025": p25, "q026": p26, "q027": p27, "q028_v2": p28}


def family_filename(mask: int, ek: str) -> str:
    return f"q028_v5_family_m{mask}_{ek}.json"


def precision_filename(mask: int, ek: str) -> str:
    return f"q028_v5_precision_m{mask}_{ek}.json"


def load_all_family_files(directory: str | Path) -> dict[int, dict[str, dict[str, Any]]]:
    d = Path(directory)
    out: dict[int, dict[str, dict[str, Any]]] = {m: {} for m in MASKS}
    for mask in MASKS:
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            p = d / family_filename(mask, ek)
            if not p.exists():
                raise RuntimeError(f"FAMILY_CHECKPOINT_MISSING_GATE=FAIL {p}")
            x = read_json(p)
            if (
                x.get("q") != Q
                or x.get("run_id") != RUN
                or x.get("phase") != "FAMILY"
                or int(x.get("mask", -1)) != mask
                or x.get("edge") != ek
                or int(x.get("likelihood_evaluations", -1)) != 4
            ):
                raise RuntimeError(f"FAMILY_CHECKPOINT_IDENTITY_GATE=FAIL {p}")
            out[mask][ek] = x
    return out


def phase_family(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    import q025_fullmf_component_attribution_v2 as q25

    mask = int(a.mask)
    sa, sb = int(a.sa), int(a.sb)
    if mask not in MASKS:
        raise RuntimeError("FAMILY_MASK_GATE=FAIL")
    ek = edge_key(sa, sb)

    parent25_cfg = q25.load_cfg(ROOT / c["reuse"]["q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)
    endpoints = {
        s: q25.load_q022_endpoint(a.q022_dir, a.q021_dir, final22, mask, s)
        for s in (sa, sb)
    }
    A = endpoints[sa]["params"]
    B = endpoints[sb]["params"]

    vectors = {
        "00": dict(A),
        "10": v2.switch(A, B, [OMEGA]),
        "01": v2.switch(A, B, [APL]),
        "11": v2.switch(A, B, [OMEGA, APL]),
    }

    model = q25.build_full_model(parent25_cfg, A)
    fam: dict[str, Any] = {}
    try:
        for sid in STATES:
            st = v2.raw_state(model, vectors[sid], c)
            fam[sid] = {
                "objective_minus2logpost": float(st["objective_minus2logpost"]),
                "full_highl_chi2": float(st["full_highl_chi2"]),
                "keys": st["keys"],
                "residual": np.asarray(st["residual"], dtype=np.float64).tolist(),
                "precision_sha256": st["precision_sha256"],
            }
    finally:
        try:
            model.close()
        except Exception:
            pass

    hashes = {fam[s]["precision_sha256"] for s in STATES}
    keys0 = fam["00"]["keys"]
    if len(hashes) != 1:
        raise RuntimeError("WITHIN_FAMILY_PRECISION_INVARIANCE_GATE=FAIL")
    if any(fam[s]["keys"] != keys0 for s in STATES[1:]):
        raise RuntimeError("WITHIN_FAMILY_ROW_ALIGNMENT_GATE=FAIL")

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "phase": "FAMILY",
        "status": "COMPLETE",
        "mask": mask,
        "edge": ek,
        "lineage_endpoints": [sa, sb],
        "likelihood_evaluations": 4,
        "optimizer_evaluations": 0,
        "sampling_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "state_ids": list(STATES),
        "row_count": len(keys0),
        "ordered_support_sha256": hashlib.sha256(
            json.dumps(keys0, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "within_family_precision_sha256": next(iter(hashes)),
        "states": fam,
    }
    write_json(a.output, out)
    print(f"Q028_V5_FAMILY_GATE=PASS mask={mask} edge={ek} rows={len(keys0)}")
    return 0


def phase_support(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    families = load_all_family_files(a.family_dir)
    supports = []
    support_meta = {}
    for mask in MASKS:
        support_meta[str(mask)] = {}
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            keys = [tuple(x) for x in families[mask][ek]["states"]["00"]["keys"]]
            supports.append(set(keys))
            support_meta[str(mask)][ek] = {
                "dimension": len(keys),
                "ordered_support_sha256": families[mask][ek]["ordered_support_sha256"],
            }

    common = set.intersection(*supports)
    if not common:
        raise RuntimeError("COMMON_SUPPORT_NONEMPTY_GATE=FAIL")
    common_keys = sorted(common, key=lambda k: (str(k[0]), str(k[1]), int(k[2])))

    fractions = {}
    for mask in MASKS:
        fractions[str(mask)] = {}
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            n = int(support_meta[str(mask)][ek]["dimension"])
            fractions[str(mask)][ek] = len(common_keys) / n

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "phase": "SUPPORT",
        "status": "COMPLETE",
        "family_checkpoint_count": 9,
        "common_keys": common_keys,
        "common_dimension": len(common_keys),
        "common_keys_sha256": hashlib.sha256(
            json.dumps(common_keys, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "support_metadata": support_meta,
        "common_fraction_by_mask_and_edge": fractions,
        "minimum_common_support_fraction": min(
            v for pm in fractions.values() for v in pm.values()
        ),
        "minimum_required_common_support_fraction": float(
            c["validation"]["minimum_common_support_fraction"]
        ),
        "principal_precision_submatrix_used_as_marginal": False,
        "construction": "EXACT_LABEL_INTERSECTION; SCHUR APPLIED IN PRECISION PHASE",
    }
    write_json(a.output, out)
    print(
        "Q028_V5_COMMON_SUPPORT_GATE=PASS "
        f"dimension={len(common_keys)} min_fraction={out['minimum_common_support_fraction']}"
    )
    return 0


def blockwise_precision_diagnostics(P: np.ndarray, block: int = 256) -> dict[str, float]:
    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        raise RuntimeError("PRECISION_SHAPE_GATE=FAIL")
    n = P.shape[0]
    max_abs = 0.0
    max_asym = 0.0
    for i in range(0, n, block):
        j = min(n, i + block)
        A = np.asarray(P[i:j, :], dtype=np.float64)
        B = np.asarray(P[:, i:j].T, dtype=np.float64)
        max_abs = max(max_abs, float(np.max(np.abs(A))) if A.size else 0.0)
        max_asym = max(
            max_asym, float(np.max(np.abs(A - B))) if A.size else 0.0
        )
    scale = max(1.0, max_abs)
    return {
        "raw_max_abs_precision_element": max_abs,
        "raw_max_abs_antisymmetry": max_asym,
        "raw_relative_antisymmetry": max_asym / scale,
    }


def batch_schur_quadratics(
    P_raw: np.ndarray,
    recipient_keys: list[tuple[str, str, int]],
    common_keys: list[tuple[str, str, int]],
    donor_columns: list[tuple[str, np.ndarray]],
) -> tuple[dict[str, float], dict[str, Any]]:
    """
    Compute r_S^T (P_SS - P_ST P_TT^-1 P_TS) r_S for many residuals
    without materializing P_marg.

    P_sym action is evaluated as 0.5*(P@X + P.T@X), so the antisymmetric
    floating component is removed algebraically without a second full matrix.
    """
    n = len(recipient_keys)
    if P_raw.shape != (n, n):
        raise RuntimeError("PRECISION_ROW_ALIGNMENT_GATE=FAIL")

    idx = {k: i for i, k in enumerate(recipient_keys)}
    if len(idx) != n:
        raise RuntimeError("RECIPIENT_KEY_UNIQUENESS_GATE=FAIL")
    if any(k not in idx for k in common_keys):
        raise RuntimeError("COMMON_SUPPORT_INDEX_GATE=FAIL")

    S = np.asarray([idx[k] for k in common_keys], dtype=np.int64)
    keep = np.zeros(n, dtype=bool)
    keep[S] = True
    T = np.flatnonzero(~keep)

    X = np.zeros((n, len(donor_columns)), dtype=np.float64)
    for col, (_, r_common) in enumerate(donor_columns):
        if len(r_common) != len(common_keys):
            raise RuntimeError("DONOR_COMMON_VECTOR_LENGTH_GATE=FAIL")
        X[S, col] = r_common

    # Symmetric precision action without allocating P_sym.
    PX = np.asarray(P_raw @ X, dtype=np.float64)
    PTX = np.asarray(P_raw.T @ X, dtype=np.float64)
    Y = 0.5 * (PX + PTX)
    q = np.sum(X * Y, axis=0)

    schur_meta: dict[str, Any] = {
        "full_dimension": n,
        "common_dimension": len(S),
        "excluded_dimension": len(T),
        "common_fraction": len(S) / n,
        "materialized_common_precision": False,
        "principal_precision_submatrix_used_as_marginal": False,
    }

    if len(T) == 0:
        schur_meta["method"] = "IDENTICAL_SUPPORT_FULL_PRECISION_ACTION"
        schur_meta["excluded_block_cholesky"] = "NOT_REQUIRED"
    else:
        Ptt_raw = np.asarray(P_raw[np.ix_(T, T)], dtype=np.float64)
        Ptt = 0.5 * (Ptt_raw + Ptt_raw.T)
        try:
            L = np.linalg.cholesky(Ptt)
        except np.linalg.LinAlgError as exc:
            raise RuntimeError("EXCLUDED_PTT_SPD_GATE=FAIL") from exc

        B = Y[T, :]
        Z = np.linalg.solve(Ptt, B)
        correction = np.sum(B * Z, axis=0)
        q = q - correction

        solve_resid = Ptt @ Z - B
        denom = max(1.0, float(np.linalg.norm(B)))
        schur_meta.update(
            {
                "method": "SCHUR_COMPLEMENT_QUADRATIC_ACTION_NO_PMATERIALIZATION",
                "excluded_block_min_cholesky_diagonal": float(np.min(np.diag(L))),
                "schur_solve_relative_residual": float(
                    np.linalg.norm(solve_resid) / denom
                ),
            }
        )

    if not np.all(np.isfinite(q)):
        raise RuntimeError("FINITE_SCHUR_QUADRATIC_GATE=FAIL")

    return {donor_columns[i][0]: float(q[i]) for i in range(len(donor_columns))}, schur_meta


def phase_precision(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    import q025_fullmf_component_attribution_v2 as q25

    mask = int(a.mask)
    sa, sb = int(a.sa), int(a.sb)
    if mask not in MASKS:
        raise RuntimeError("PRECISION_MASK_GATE=FAIL")
    ek = edge_key(sa, sb)

    families = load_all_family_files(a.family_dir)
    support = read_json(a.support_result)
    if (
        support.get("phase") != "SUPPORT"
        or support.get("run_id") != RUN
        or int(support.get("family_checkpoint_count", -1)) != 9
    ):
        raise RuntimeError("SUPPORT_PARENT_GATE=FAIL")
    common_keys = [tuple(x) for x in support["common_keys"]]

    parent25_cfg = q25.load_cfg(ROOT / c["reuse"]["q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)
    A = q25.load_q022_endpoint(
        a.q022_dir, a.q021_dir, final22, mask, sa
    )["params"]

    # Precision reconstruction only: model construction initializes the frozen
    # CamSpec covariance/precision. No logposterior call is made here.
    model = q25.build_full_model(parent25_cfg, A)
    try:
        P_raw = np.asarray(model.likelihood[FULL_LIKE].covinv, dtype=np.float64)
        recipient_keys = [
            tuple(x) for x in families[mask][ek]["states"]["00"]["keys"]
        ]
        if P_raw.shape != (len(recipient_keys), len(recipient_keys)):
            raise RuntimeError("PRECISION_SHAPE_GATE=FAIL")
        if not np.all(np.isfinite(P_raw)):
            raise RuntimeError("FINITE_PRECISION_GATE=FAIL")

        precision_diag = blockwise_precision_diagnostics(P_raw)

        donor_columns: list[tuple[str, np.ndarray]] = []
        column_descriptor: dict[str, dict[str, Any]] = {}
        donor_common_index_cache: dict[tuple[int, str], list[int]] = {}

        for rmask in MASKS:
            for ra, rb in EDGES:
                rek = edge_key(ra, rb)
                fam = families[rmask][rek]
                donor_keys = [tuple(x) for x in fam["states"]["00"]["keys"]]
                donor_idx = {k: i for i, k in enumerate(donor_keys)}
                if any(k not in donor_idx for k in common_keys):
                    raise RuntimeError("DONOR_COMMON_SUPPORT_GATE=FAIL")
                selection = [donor_idx[k] for k in common_keys]
                donor_common_index_cache[(rmask, rek)] = selection

                for sid in STATES:
                    residual = np.asarray(
                        fam["states"][sid]["residual"], dtype=np.float64
                    )
                    r_common = residual[selection]
                    cid = f"m{rmask}:{rek}:{sid}"
                    donor_columns.append((cid, r_common))
                    column_descriptor[cid] = {
                        "residual_mask": rmask,
                        "residual_edge": rek,
                        "state": sid,
                    }

        if len(donor_columns) != 36:
            raise RuntimeError("CROSS_DONOR_COLUMN_COUNT_GATE=FAIL")

        q_by_column, schur_meta = batch_schur_quadratics(
            P_raw, recipient_keys, common_keys, donor_columns
        )

        donor_cases = {}
        for rmask in MASKS:
            for ra, rb in EDGES:
                rek = edge_key(ra, rb)
                qstates = {
                    sid: q_by_column[f"m{rmask}:{rek}:{sid}"] for sid in STATES
                }
                interaction = v2.contrast(qstates)
                donor_cases[f"residual_mask_{rmask}:{rek}"] = {
                    "residual_mask": rmask,
                    "residual_edge": rek,
                    "state_quadratics": qstates,
                    "interaction": float(interaction),
                }

        raw_sha = v2.sha256_array(P_raw)
    finally:
        try:
            model.close()
        except Exception:
            pass

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "phase": "PRECISION",
        "status": "COMPLETE",
        "recipient_precision_mask": mask,
        "candidate_precision_edge": ek,
        "lineage_endpoints": [sa, sb],
        "new_likelihood_evaluations": 0,
        "precision_model_constructions": 1,
        "optimizer_evaluations": 0,
        "sampling_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "raw_precision_sha256": raw_sha,
        "precision_symmetrization": "P_sym action = 0.5*(P_raw@X + P_raw.T@X)",
        "raw_antisymmetry_scientific_gate": False,
        "full_precision_spd_revalidated_in_v5": False,
        "full_precision_spd_provenance": (
            "REUSED_FROM_SUCCESSFUL_Q028_V2_VALIDATED_PRECISION_CONSTRUCTION; "
            "V5 REVALIDATES ONLY EXCLUDED P_TT WHEN SCHUR EXCLUSION IS NONEMPTY"
        ),
        "precision_diagnostics": precision_diag,
        "schur_metadata": schur_meta,
        "common_keys_sha256": support["common_keys_sha256"],
        "donor_case_count": len(donor_cases),
        "donor_cases": donor_cases,
    }
    write_json(a.output, out)
    print(
        "Q028_V5_PRECISION_FUNCTIONAL_GATE=PASS "
        f"recipient_mask={mask} candidate_edge={ek} donor_cases={len(donor_cases)}"
    )
    return 0


def load_all_precision_files(directory: str | Path) -> dict[int, dict[str, dict[str, Any]]]:
    d = Path(directory)
    out: dict[int, dict[str, dict[str, Any]]] = {m: {} for m in MASKS}
    for mask in MASKS:
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            p = d / precision_filename(mask, ek)
            if not p.exists():
                raise RuntimeError(f"PRECISION_CHECKPOINT_MISSING_GATE=FAIL {p}")
            x = read_json(p)
            if (
                x.get("q") != Q
                or x.get("run_id") != RUN
                or x.get("phase") != "PRECISION"
                or int(x.get("recipient_precision_mask", -1)) != mask
                or x.get("candidate_precision_edge") != ek
                or int(x.get("new_likelihood_evaluations", -1)) != 0
                or int(x.get("donor_case_count", -1)) != 9
            ):
                raise RuntimeError(f"PRECISION_CHECKPOINT_IDENTITY_GATE=FAIL {p}")
            out[mask][ek] = x
    return out


def phase_merge(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    parents = load_parents(c, a)
    families = load_all_family_files(a.family_dir)
    precisions = load_all_precision_files(a.precision_dir)
    support = read_json(a.support_result)

    if (
        support.get("phase") != "SUPPORT"
        or support.get("run_id") != RUN
        or int(support.get("family_checkpoint_count", -1)) != 9
    ):
        raise RuntimeError("SUPPORT_PARENT_GATE=FAIL")

    # Exact global execution accounting.
    family_eval_total = sum(
        int(families[m][edge_key(a0, b0)]["likelihood_evaluations"])
        for m in MASKS for a0, b0 in EDGES
    )
    precision_eval_total = sum(
        int(precisions[m][edge_key(a0, b0)]["new_likelihood_evaluations"])
        for m in MASKS for a0, b0 in EDGES
    )
    if family_eval_total != 36 or precision_eval_total != 0:
        raise RuntimeError(
            f"FIXED_VECTOR_COUNT_GATE=FAIL family={family_eval_total} "
            f"precision={precision_eval_total}"
        )

    tol = float(c["validation"]["precision_edge_pair_interaction_abs_tol"])
    candidate_edges = [edge_key(x, y) for x, y in EDGES]

    bplus_diag = {}
    identified = {}
    global_max_spread = 0.0

    for pmask in MASKS:
        cases = {}
        mask_ok = True
        for rmask in MASKS:
            for ra, rb in EDGES:
                rek = edge_key(ra, rb)
                case_id = f"residual_mask_{rmask}:{rek}"
                vals = {
                    pek: float(
                        precisions[pmask][pek]["donor_cases"][case_id]["interaction"]
                    )
                    for pek in candidate_edges
                }
                pairwise = {}
                spread = 0.0
                for i, ea in enumerate(candidate_edges):
                    for eb in candidate_edges[i + 1:]:
                        d = abs(vals[ea] - vals[eb])
                        pairwise[f"{ea}_vs_{eb}"] = d
                        spread = max(spread, d)
                ok = spread <= tol
                mask_ok = mask_ok and ok
                global_max_spread = max(global_max_spread, spread)
                cases[case_id] = {
                    "residual_mask": rmask,
                    "residual_edge": rek,
                    "interaction_by_precision_candidate_edge": vals,
                    "pairwise_abs_interaction_differences": pairwise,
                    "edge_choice_spread": spread,
                    "tolerance": tol,
                    "criterion_b_plus_case_pass": ok,
                }
        bplus_diag[str(pmask)] = {
            "recipient_precision_mask": pmask,
            "candidate_precision_edges": candidate_edges,
            "donor_case_count": len(cases),
            "donor_cases": cases,
            "max_edge_choice_spread": max(
                (v["edge_choice_spread"] for v in cases.values()), default=0.0
            ),
            "criterion_b_plus_mask_pass": mask_ok,
        }
        identified[str(pmask)] = mask_ok

    bplus_ok = all(identified.values())
    min_fraction = float(support["minimum_common_support_fraction"])
    support_ok = min_fraction >= float(
        c["validation"]["minimum_common_support_fraction"]
    )

    common_support_summary = {
        "construction": (
            "EXACT_LABEL_INTERSECTION_PLUS_SCHUR_QUADRATIC_ACTION; "
            "NO MATERIALIZED FULL COMMON PRECISION"
        ),
        "dimension": int(support["common_dimension"]),
        "keys_sha256": support["common_keys_sha256"],
        "minimum_common_support_fraction": min_fraction,
        "minimum_required_common_support_fraction": float(
            c["validation"]["minimum_common_support_fraction"]
        ),
        "interpretability_gate": support_ok,
        "principal_precision_submatrix_used_as_marginal": False,
        "materialized_common_precision": False,
    }

    base = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "status": "COMPLETE",
        "actual_new_likelihood_evaluations": 36,
        "family_checkpoint_jobs": 9,
        "precision_functional_jobs": 9,
        "precision_model_constructions_without_likelihood_evaluation": 9,
        "optimizer_evaluations": 0,
        "sampling_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "state_level_invariance_required": False,
        "criterion_b_plus": {
            "name": "COMMON_SUPPORT_CROSS_DONOR_TARGET_FUNCTIONAL_INVARIANCE",
            "functional": "F(R,P)=q11-q10-q01+q00=Tr(P K_R)",
            "tolerance": tol,
            "diagnostics_by_recipient_precision_mask": bplus_diag,
            "identified_by_mask": identified,
            "global_max_edge_choice_spread": global_max_spread,
            "gate": bplus_ok,
        },
        "common_support": common_support_summary,
        "execution_architecture": {
            "version": "V5_SPLIT_CHECKPOINTED",
            "v4_status": "INFRASTRUCTURE_LIMITED_NO_SCIENTIFIC_RESULT",
            "dense_precision_artifacts_serialized": False,
            "dense_common_precision_materialized": False,
            "family_jobs_restartable_independently": True,
            "precision_jobs_restartable_independently": True,
        },
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
            "q025": parents["q025"].get("result_id"),
            "q026": parents["q026"].get("result_id"),
            "q027": parents["q027"].get("result_id"),
            "q028_v2": parents["q028_v2"].get("result_id"),
        },
    }

    if not bplus_ok:
        out = {
            **base,
            "resolution_class": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "scientific_classification": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "reason": (
                "At least one recipient-mask precision has edge-choice spread "
                "above the frozen 2e-4 interaction tolerance for a donor "
                "residual family required by the Q028 counterfactual."
            ),
            "counterfactual": {},
            "shapley_rows": [],
            "shapley_closure_gate": "NOT_REACHED_VALID_NEGATIVE_STOP",
            "stop_condition_reached": True,
        }
        write_json(a.output, out)
        print("Q028_V5_RESOLUTION=VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY")
        return 0

    if not support_ok:
        out = {
            **base,
            "resolution_class": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "scientific_classification": "VALID_TARGET_FUNCTIONAL_NON_IDENTIFIABILITY",
            "reason": (
                "Criterion B+ passed, but exact common support is below the "
                "frozen minimum common-support fraction required for "
                "interpretable Q028 attribution."
            ),
            "counterfactual": {},
            "shapley_rows": [],
            "shapley_closure_gate": "NOT_REACHED_VALID_NEGATIVE_STOP",
            "stop_condition_reached": True,
        }
        write_json(a.output, out)
        print("Q028_V5_RESOLUTION=VALID_COMMON_SUPPORT_FRACTION_NEGATIVE_STOP")
        return 0

    representative_edge = "e01"
    counterfactual = {}
    shapley_rows = []

    for sa, sb in EDGES:
        ek = edge_key(sa, sb)
        matrix = {}
        qstates = {}
        for rmask in MASKS:
            matrix[str(rmask)] = {}
            qstates[str(rmask)] = {}
            case_id = f"residual_mask_{rmask}:{ek}"
            for pmask in MASKS:
                rec = precisions[pmask][representative_edge]["donor_cases"][case_id]
                matrix[str(rmask)][str(pmask)] = float(rec["interaction"])
                qstates[str(rmask)][str(pmask)] = {
                    s: float(v) for s, v in rec["state_quadratics"].items()
                }

        comparisons = {}
        for i, ma in enumerate(MASKS):
            for mb in MASKS[i + 1:]:
                Faa = matrix[str(ma)][str(ma)]
                Fab = matrix[str(ma)][str(mb)]
                Fba = matrix[str(mb)][str(ma)]
                Fbb = matrix[str(mb)][str(mb)]
                sh = v2.shapley_two_factor(Faa, Fab, Fba, Fbb)
                ck = f"m{ma}_vs_m{mb}"
                comparisons[ck] = sh
                shapley_rows.append({"edge": ek, "mask_pair": [ma, mb], **sh})

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

    diagonal_support_effects = {}
    for mask in MASKS:
        diagonal_support_effects[str(mask)] = {}
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            full_q = {
                sid: float(families[mask][ek]["states"][sid]["full_highl_chi2"])
                for sid in STATES
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
        "resolution_class": "VALID_COMMON_SUPPORT_SEPARATION",
        "scientific_classification": attribution_class,
        "representative_precision_edge_by_mask": {
            str(mask): representative_edge for mask in MASKS
        },
        "representative_selection_reason": (
            "Deterministic e01 representative; Criterion B+ established that "
            "edge choice changes every required target-functional evaluation "
            "by no more than the frozen interaction tolerance."
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
                "PRECISION ACTION ON EXACT COMMON LABELLED SUPPORT"
            ),
            "state_level_invariance": (
                "NOT REQUIRED; COMMON-MODE q_s SHIFTS MAY CANCEL IN THE "
                "DEFINED FACTORIAL CONTRAST"
            ),
            "lineage_warning": (
                "Edge IDs are Q022 lineage labels, not independently "
                "established universal physical posterior modes; Q024 "
                "non-universality remains preserved."
            ),
            "causal_status": (
                "FUNCTIONAL COUNTERFACTUAL ATTRIBUTION WITHIN THE FROZEN "
                "CAMSPEC CONSTRUCTION; NOT PHYSICAL CAUSALITY"
            ),
        },
        "stop_condition_reached": True,
    }
    write_json(a.output, out)
    print(f"Q028_V5_RESOLUTION=VALID_COMMON_SUPPORT_SEPARATION class={attribution_class}")
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config", default="q028_common_support_counterfactual_v5_config.yml"
    )
    sp = ap.add_subparsers(dest="phase", required=True)

    fam = sp.add_parser("family")
    fam.add_argument("--mask", required=True, type=int)
    fam.add_argument("--sa", required=True, type=int)
    fam.add_argument("--sb", required=True, type=int)
    fam.add_argument("--q021-dir", required=True)
    fam.add_argument("--q022-dir", required=True)
    fam.add_argument("--output", required=True)

    sup = sp.add_parser("support")
    sup.add_argument("--family-dir", required=True)
    sup.add_argument("--output", required=True)

    pre = sp.add_parser("precision")
    pre.add_argument("--mask", required=True, type=int)
    pre.add_argument("--sa", required=True, type=int)
    pre.add_argument("--sb", required=True, type=int)
    pre.add_argument("--q021-dir", required=True)
    pre.add_argument("--q022-dir", required=True)
    pre.add_argument("--family-dir", required=True)
    pre.add_argument("--support-result", required=True)
    pre.add_argument("--output", required=True)

    mer = sp.add_parser("merge")
    mer.add_argument("--family-dir", required=True)
    mer.add_argument("--precision-dir", required=True)
    mer.add_argument("--support-result", required=True)
    mer.add_argument("--q025-result", required=True)
    mer.add_argument("--q026-result", required=True)
    mer.add_argument("--q027-result", required=True)
    mer.add_argument("--q028-v2-result", required=True)
    mer.add_argument("--output", required=True)
    return ap


def main() -> int:
    a = parser().parse_args()
    c = load_cfg(a.config)
    if a.phase == "family":
        return phase_family(a, c)
    if a.phase == "support":
        return phase_support(a, c)
    if a.phase == "precision":
        return phase_precision(a, c)
    if a.phase == "merge":
        return phase_merge(a, c)
    raise RuntimeError("PHASE_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
