#!/usr/bin/env python3
"""
Bubbleverse Q028 V2 — tolerance-validated common-support residual/precision
counterfactual for the frozen MOD-EDE-N3 full-MF CamSpec chain.

Scientific contract
-------------------
CURRENT Q: Q028

Question:
Can the established cross-mask non-universality of the frozen MOD-EDE-N3
full-MF CamSpec likelihood be separated into residual/data-vector effects
versus mask-specific inverse-covariance/precision effects using a
mathematically valid common-support counterfactual construction, without
changing the physical model or reoptimizing the authoritative Q022 endpoints?

Method:
1. Reuse Q022 V2 endpoints through the validated Q025 V2 loaders.
2. Reuse Q027's four-state omega_cdm x A_planck finite-switch family.
3. Reuse Q017's exact residual construction.
4. Extract each mask's full precision operator and labelled residual vector.
5. Quantify edge-to-edge precision differences using matrix norms and the exact downstream quadratic diagnostics; SHA256 is provenance-only.
6. Construct the exact intersection of labelled data coordinates.
7. Marginalize excluded coordinates from each full Gaussian precision by the
   Schur complement:
       P_common = P_SS - P_ST P_TT^{-1} P_TS
   rather than incorrectly taking P_SS as the marginal precision.
8. On the common coordinate basis evaluate:
       q(r,P) = r^T P r
   and the four-state pair interaction for every residual-mask x precision-mask
   combination.
9. For each lineage edge and each pair of masks use the symmetric two-factor
   Shapley decomposition of the observed diagonal contrast into:
       residual-side contribution + precision-side contribution.
9. Preserve signed accounting. No optimization, sampling, Q024 rerun, model
   change, or physical-causality claim.

Important interpretation boundary:
"Residual-side" means the data-minus-model residual family. It does NOT
separate raw data changes from model/nuisance-vector changes.
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

ROOT = Path(__file__).resolve().parent
Q = "Q028"
RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V2"
RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-002"
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
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=_json_default) + "\n",
                 encoding="utf-8")
    os.replace(t, p)


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_GATE=FAIL {path}")
    return d


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
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
    required_true = (
        "no_optimization", "no_sampling", "no_new_endpoints",
        "no_q024_permutation_rerun", "preserve_signed_accounting",
        "common_support_must_be_validated", "do_not_use_precision_principal_submatrix_as_marginal",
    )
    for key in required_true:
        if c["rules"].get(key) is not True:
            raise RuntimeError(f"{key.upper()}_GATE=FAIL")
    return c


def sha256_array(a: np.ndarray) -> str:
    x = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(x.shape).encode("ascii"))
    h.update(x.tobytes())
    return h.hexdigest()


def row_key(r: Mapping[str, Any]) -> tuple[str, str, int]:
    return (str(r["observable"]), str(r["spectrum"]), int(r["ell"]))


def switch(a: Mapping[str, float], b: Mapping[str, float], names) -> dict[str, float]:
    out = {str(k): float(v) for k, v in a.items()}
    for name in names:
        out[name] = float(b[name])
    return out


def contrast(v: Mapping[str, float]) -> float:
    return float(v["11"]) - float(v["10"]) - float(v["01"]) + float(v["00"])


def raw_state(model: Any, values: Mapping[str, float], c: Mapping[str, Any]) -> dict[str, Any]:
    import q025_fullmf_component_attribution_v2 as q25
    import q017_planck_direction_localization_v1 as q17

    lp = model.logposterior(dict(values))
    logpost = getattr(lp, "logpost", lp)
    if not finite(logpost):
        raise RuntimeError("FINITE_LOGPOST_GATE=FAIL")

    cosmology = {p: float(values[p]) for p in q25.PARAM_GROUPS["cosmology"]}
    cosmology.update({p: float(values[p]) for p in q25.PARAM_GROUPS["primordial"]})
    nuisance = {
        p: float(values[p])
        for group in ("shared_nuisance", "foreground")
        for p in q25.PARAM_GROUPS[group]
    }
    expanded = q17.expanded_values(model, cosmology, nuisance)
    q17_cfg = {"decomposition": {"ell_bands": c["decomposition"]["ell_bands"]}}
    detailed = q17.detailed_planck_state(model, expanded, q17_cfg)

    rows = detailed.get("rows", [])
    if not rows:
        raise RuntimeError("Q017_POINTWISE_ROWS_GATE=FAIL")
    keys = [row_key(r) for r in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("ROW_KEY_UNIQUENESS_GATE=FAIL")

    residual = np.asarray([float(r["residual"]) for r in rows], dtype=np.float64)
    P = np.asarray(model.likelihood[FULL_LIKE].covinv, dtype=np.float64)
    if P.shape != (len(rows), len(rows)):
        raise RuntimeError("PRECISION_SHAPE_GATE=FAIL")
    if not np.all(np.isfinite(P)) or not np.all(np.isfinite(residual)):
        raise RuntimeError("FINITE_MATRIX_VECTOR_GATE=FAIL")

    chi2 = float(residual @ (P @ residual))
    tol = float(c["validation"]["q017_chi2_closure_abs_tol"])
    if abs(chi2 - float(detailed["chi2"])) > tol:
        raise RuntimeError(
            f"Q017_CHI2_CLOSURE_GATE=FAIL raw={chi2} q017={detailed['chi2']}"
        )

    return {
        "objective_minus2logpost": -2.0 * float(logpost),
        "full_highl_chi2": chi2,
        "keys": keys,
        "residual": residual,
        "precision": P,
        "precision_sha256": sha256_array(P),
    }


def validate_spd(P: np.ndarray, c: Mapping[str, Any], label: str) -> dict[str, Any]:
    sym_abs = float(np.max(np.abs(P - P.T))) if P.size else 0.0
    scale = max(1.0, float(np.max(np.abs(P))) if P.size else 1.0)
    sym_rel = sym_abs / scale
    if sym_rel > float(c["validation"]["precision_symmetry_rel_tol"]):
        raise RuntimeError(f"PRECISION_SYMMETRY_GATE=FAIL {label} rel={sym_rel}")
    Ps = 0.5 * (P + P.T)
    try:
        L = np.linalg.cholesky(Ps)
    except np.linalg.LinAlgError as exc:
        raise RuntimeError(f"PRECISION_SPD_GATE=FAIL {label}") from exc
    min_chol_diag = float(np.min(np.diag(L)))
    return {"symmetry_relative_error": sym_rel, "min_cholesky_diagonal": min_chol_diag}


def marginal_precision_from_full_precision(
    P: np.ndarray,
    full_keys: list[tuple[str, str, int]],
    common_keys: list[tuple[str, str, int]],
    c: Mapping[str, Any],
    label: str,
) -> tuple[np.ndarray, dict[str, Any], np.ndarray]:
    """
    Precision of the marginal Gaussian on common support.

    If x=(x_S,x_T) has full precision
       [P_SS P_ST]
       [P_TS P_TT],
    integrating x_T out gives
       P_marg = P_SS - P_ST P_TT^{-1} P_TS.
    """
    full_index = {k: i for i, k in enumerate(full_keys)}
    if any(k not in full_index for k in common_keys):
        raise RuntimeError(f"COMMON_SUPPORT_INDEX_GATE=FAIL {label}")
    S = np.asarray([full_index[k] for k in common_keys], dtype=int)
    keep = np.zeros(len(full_keys), dtype=bool)
    keep[S] = True
    T = np.flatnonzero(~keep)

    P = 0.5 * (P + P.T)
    Pss = P[np.ix_(S, S)]
    if len(T) == 0:
        Pm = Pss.copy()
        method = "IDENTICAL_SUPPORT_FULL_PRECISION"
    else:
        Pst = P[np.ix_(S, T)]
        Ptt = P[np.ix_(T, T)]
        validate_spd(Ptt, c, label + ":excluded_Ptt")
        # Solve; never form Ptt^{-1}.
        correction = Pst @ np.linalg.solve(Ptt, Pst.T)
        Pm = Pss - correction
        method = "SCHUR_COMPLEMENT_MARGINAL_FROM_FULL_PRECISION"
    Pm = 0.5 * (Pm + Pm.T)
    spd = validate_spd(Pm, c, label + ":common")
    meta = {
        "method": method,
        "full_dimension": int(len(full_keys)),
        "common_dimension": int(len(common_keys)),
        "excluded_dimension": int(len(T)),
        "common_fraction": float(len(common_keys) / len(full_keys)),
        "full_precision_sha256": sha256_array(P),
        "common_precision_sha256": sha256_array(Pm),
        **spd,
    }
    return Pm, meta, S


def project_residual(
    state: Mapping[str, Any],
    common_keys: list[tuple[str, str, int]],
) -> np.ndarray:
    idx = {k: i for i, k in enumerate(state["keys"])}
    if any(k not in idx for k in common_keys):
        raise RuntimeError("RESIDUAL_COMMON_SUPPORT_GATE=FAIL")
    return np.asarray([state["residual"][idx[k]] for k in common_keys], dtype=np.float64)


def interaction_for_family(
    family: Mapping[str, Mapping[str, Any]],
    Pcommon: np.ndarray,
    common_keys: list[tuple[str, str, int]],
) -> tuple[float, dict[str, float]]:
    q = {}
    for sid in STATES:
        r = project_residual(family[sid], common_keys)
        q[sid] = float(r @ (Pcommon @ r))
    return contrast(q), q


def shapley_two_factor(Faa: float, Fab: float, Fba: float, Fbb: float) -> dict[str, float]:
    # F(residual source, precision source)
    residual = 0.5 * ((Fba - Faa) + (Fbb - Fab))
    precision = 0.5 * ((Fab - Faa) + (Fbb - Fba))
    total = Fbb - Faa
    return {
        "observed_diagonal_contrast": total,
        "residual_side_shapley": residual,
        "precision_side_shapley": precision,
        "closure_error": total - residual - precision,
    }


def classify(shapley_rows: list[dict[str, Any]], c: Mapping[str, Any]) -> str:
    tol = float(c["validation"]["factorial_zero_abs_tol"])
    if not shapley_rows:
        return "NON_IDENTIFIABLE_NO_VALID_LINEAGE_COMPARISONS"
    rel = []
    for r in shapley_rows:
        a = abs(float(r["residual_side_shapley"]))
        b = abs(float(r["precision_side_shapley"]))
        if max(a, b) <= tol:
            rel.append("NEGLIGIBLE")
        elif a > b:
            rel.append("RESIDUAL")
        elif b > a:
            rel.append("PRECISION")
        else:
            rel.append("TIE")
    nonzero = [x for x in rel if x != "NEGLIGIBLE"]
    if not nonzero:
        return "COMMON_SUPPORT_CROSS_MASK_CONTRASTS_NUMERICALLY_NEGLIGIBLE"
    if all(x == "RESIDUAL" for x in nonzero):
        return "RESIDUAL_SIDE_LARGER_ACROSS_ALL_NONNEGLIGIBLE_LINEAGE_DIAGNOSTICS"
    if all(x == "PRECISION" for x in nonzero):
        return "PRECISION_SIDE_LARGER_ACROSS_ALL_NONNEGLIGIBLE_LINEAGE_DIAGNOSTICS"
    return "IDENTIFIABLE_MIXED_RESIDUAL_AND_PRECISION_CONTRIBUTIONS_ON_COMMON_SUPPORT"



def matrix_difference_metrics(A: np.ndarray, B: np.ndarray) -> dict[str, float]:
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    if A.shape != B.shape:
        raise RuntimeError(f"PRECISION_MATRIX_SHAPE_COMPARISON_GATE=FAIL {A.shape} != {B.shape}")
    D = A - B
    max_abs = float(np.max(np.abs(D))) if D.size else 0.0
    scale_max = max(
        float(np.max(np.abs(A))) if A.size else 0.0,
        float(np.max(np.abs(B))) if B.size else 0.0,
        np.finfo(np.float64).tiny,
    )
    fro = float(np.linalg.norm(D, ord="fro"))
    scale_fro = max(
        float(np.linalg.norm(A, ord="fro")),
        float(np.linalg.norm(B, ord="fro")),
        np.finfo(np.float64).tiny,
    )
    # Spectral norm is conclusion-useful here; matrices are only evaluated three-per-mask.
    spectral = float(np.linalg.norm(D, ord=2))
    scale_spectral = max(
        float(np.linalg.norm(A, ord=2)),
        float(np.linalg.norm(B, ord=2)),
        np.finfo(np.float64).tiny,
    )
    return {
        "max_abs_delta": max_abs,
        "relative_max_delta": max_abs / scale_max,
        "frobenius_delta": fro,
        "relative_frobenius_delta": fro / scale_fro,
        "spectral_delta": spectral,
        "relative_spectral_delta": spectral / scale_spectral,
    }


def precision_functional_difference(
    family: Mapping[str, Mapping[str, Any]],
    Pa: np.ndarray,
    Pb: np.ndarray,
) -> dict[str, Any]:
    """
    Compare two candidate precision operators using the actual four Q028 residual states.
    This is not a replacement for matrix equivalence: it answers whether any matrix
    difference materially changes the exact downstream Q028 quadratic diagnostics.
    """
    qa, qb = {}, {}
    state_abs = {}
    for sid in STATES:
        r = np.asarray(family[sid]["residual"], dtype=np.float64)
        qa[sid] = float(r @ (Pa @ r))
        qb[sid] = float(r @ (Pb @ r))
        state_abs[sid] = abs(qb[sid] - qa[sid])
    ia = contrast(qa)
    ib = contrast(qb)
    return {
        "state_quadratic_A": qa,
        "state_quadratic_B": qb,
        "max_abs_state_quadratic_delta": max(state_abs.values()) if state_abs else 0.0,
        "pair_interaction_A": ia,
        "pair_interaction_B": ib,
        "abs_pair_interaction_delta": abs(ib - ia),
    }


def evaluate_edge_precision_equivalence(
    mask: int,
    families: Mapping[int, Mapping[str, Mapping[str, Any]]],
    edge_precisions: Mapping[int, Mapping[str, np.ndarray]],
    edge_keys: Mapping[int, Mapping[str, list[tuple[str, str, int]]]],
    c: Mapping[str, Any],
) -> dict[str, Any]:
    """
    V2 replacement for the V1 cryptographic-hash scientific gate.

    SHA256 remains provenance-only. Scientific equivalence is determined by:
      (1) exact ordered support equality;
      (2) numerical matrix norms; and
      (3) effect on the exact downstream r^T P r / pair-interaction diagnostics.

    A matrix can therefore fail byte identity yet remain numerically/functionally
    equivalent for Q028.
    """
    edge_names = sorted(edge_precisions[mask])
    reference_edge = edge_names[0]
    reference_keys = edge_keys[mask][reference_edge]
    comparisons = {}
    all_numeric = True
    all_functional = True
    all_support = True

    rel_fro_tol = float(c["validation"]["precision_edge_relative_frobenius_tol"])
    rel_max_tol = float(c["validation"]["precision_edge_relative_max_tol"])
    rel_spec_tol = float(c["validation"]["precision_edge_relative_spectral_tol"])
    q_tol = float(c["validation"]["precision_edge_state_quadratic_abs_tol"])
    pair_tol = float(c["validation"]["precision_edge_pair_interaction_abs_tol"])

    for i, ea in enumerate(edge_names):
        for eb in edge_names[i+1:]:
            ka = edge_keys[mask][ea]
            kb = edge_keys[mask][eb]
            support_equal = ka == kb
            all_support = all_support and support_equal
            rec = {
                "edge_a": ea,
                "edge_b": eb,
                "support_equal_ordered": support_equal,
                "sha256_a": sha256_array(edge_precisions[mask][ea]),
                "sha256_b": sha256_array(edge_precisions[mask][eb]),
                "exact_sha_equal": sha256_array(edge_precisions[mask][ea]) == sha256_array(edge_precisions[mask][eb]),
            }
            if not support_equal:
                rec.update({
                    "numeric_matrix_equivalent": False,
                    "functionally_equivalent_for_q028": False,
                    "reason": "ORDERED_SUPPORT_MISMATCH",
                })
                all_numeric = False
                all_functional = False
                comparisons[f"{ea}_vs_{eb}"] = rec
                continue

            metrics = matrix_difference_metrics(edge_precisions[mask][ea], edge_precisions[mask][eb])
            numeric_ok = (
                metrics["relative_frobenius_delta"] <= rel_fro_tol
                and metrics["relative_max_delta"] <= rel_max_tol
                and metrics["relative_spectral_delta"] <= rel_spec_tol
            )

            # Test both edge residual families, because each candidate P originated
            # from a different edge construction.
            functionals = {}
            functional_ok = True
            for residual_edge in (ea, eb):
                f = precision_functional_difference(
                    families[mask][residual_edge],
                    edge_precisions[mask][ea],
                    edge_precisions[mask][eb],
                )
                functionals[residual_edge] = f
                functional_ok = functional_ok and (
                    f["max_abs_state_quadratic_delta"] <= q_tol
                    and f["abs_pair_interaction_delta"] <= pair_tol
                )

            rec.update({
                "matrix_difference": metrics,
                "numeric_matrix_equivalent": numeric_ok,
                "functional_diagnostics": functionals,
                "functionally_equivalent_for_q028": functional_ok,
            })
            all_numeric = all_numeric and numeric_ok
            all_functional = all_functional and functional_ok
            comparisons[f"{ea}_vs_{eb}"] = rec

    # Proceed if exact support is common and either the matrices are numerically
    # equivalent as operators, or their differences are demonstrably immaterial
    # to every tested downstream Q028 quadratic diagnostic.
    proceed = all_support and (all_numeric or all_functional)
    return {
        "mask": mask,
        "reference_edge": reference_edge,
        "ordered_support_equal_across_edges": all_support,
        "all_pairwise_numeric_matrix_equivalent": all_numeric,
        "all_pairwise_functionally_equivalent_for_q028": all_functional,
        "proceed_with_single_mask_precision_operator": proceed,
        "tolerances": {
            "relative_frobenius": rel_fro_tol,
            "relative_max": rel_max_tol,
            "relative_spectral": rel_spec_tol,
            "state_quadratic_abs": q_tol,
            "pair_interaction_abs": pair_tol,
        },
        "comparisons": comparisons,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q028_common_support_counterfactual_v2_config.yml")
    ap.add_argument("--q021-dir", required=True)
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--q025-result", required=True)
    ap.add_argument("--q026-result", required=True)
    ap.add_argument("--q027-result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    c = load_cfg(a.config)
    q025_parent = read_json(a.q025_result)
    q026_parent = read_json(a.q026_result)
    q027_parent = read_json(a.q027_result)

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

    import q025_fullmf_component_attribution_v2 as q25
    parent25_cfg = q25.load_cfg(ROOT / c["reuse"]["q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)

    # families[mask][edge_key][state]
    families: dict[int, dict[str, dict[str, Any]]] = {}
    edge_precisions: dict[int, dict[str, np.ndarray]] = {}
    edge_keys: dict[int, dict[str, list[tuple[str, str, int]]]] = {}
    eval_count = 0

    for mask in MASKS:
        endpoints = {
            s: q25.load_q022_endpoint(a.q022_dir, a.q021_dir, final22, mask, s)
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
                "10": switch(A, B, [OMEGA]),
                "01": switch(A, B, [APL]),
                "11": switch(A, B, [OMEGA, APL]),
            }
            fam = {}
            try:
                for sid in STATES:
                    fam[sid] = raw_state(model, vectors[sid], c)
                    eval_count += 1
            finally:
                try:
                    model.close()
                except Exception:
                    pass

            hashes = {fam[s]["precision_sha256"] for s in STATES}
            keys = [fam[s]["keys"] for s in STATES]
            if len(hashes) != 1:
                raise RuntimeError(f"PRECISION_INVARIANCE_WITHIN_SWITCH_GATE=FAIL mask={mask} edge={ek}")
            if any(k != keys[0] for k in keys[1:]):
                raise RuntimeError(f"ROW_ALIGNMENT_WITHIN_SWITCH_GATE=FAIL mask={mask} edge={ek}")
            families[mask][ek] = fam
            edge_precisions[mask][ek] = fam["00"]["precision"]
            edge_keys[mask][ek] = fam["00"]["keys"]

    expected = int(c["execution"]["total_expected_likelihood_evaluations"])
    if eval_count != expected:
        raise RuntimeError(f"FIXED_VECTOR_COUNT_GATE=FAIL actual={eval_count} expected={expected}")

    # V2: exact hashes are provenance only. Quantify matrix and functional
    # differences before deciding whether one mask-specific P can represent all edges.
    per_mask_precision = {}
    per_mask_keys = {}
    precision_edge_equivalence = {}
    precision_edge_gate = {}
    materially_distinct_masks = []
    for mask in MASKS:
        diag = evaluate_edge_precision_equivalence(
            mask, families, edge_precisions, edge_keys, c
        )
        precision_edge_equivalence[str(mask)] = diag
        ok = bool(diag["proceed_with_single_mask_precision_operator"])
        precision_edge_gate[str(mask)] = ok
        if not ok:
            materially_distinct_masks.append(mask)
            continue
        ek0 = str(diag["reference_edge"])
        per_mask_precision[mask] = edge_precisions[mask][ek0]
        per_mask_keys[mask] = edge_keys[mask][ek0]

    if materially_distinct_masks:
        out = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "status": "COMPLETE_NEGATIVE_IDENTIFIABILITY_RESULT",
            "actual_new_likelihood_evaluations": eval_count,
            "optimizer_evaluations": 0, "sampling_evaluations": 0,
            "q024_permutations_evaluated": 0,
            "common_support_gate": "NOT_REACHED_AFTER_QUANTIFIED_EDGE_PRECISION_TEST",
            "precision_invariance_across_edges_by_mask": precision_edge_gate,
        "precision_edge_equivalence_diagnostics": precision_edge_equivalence,
            "precision_edge_equivalence_diagnostics": precision_edge_equivalence,
            "scientific_classification":
                "NON_IDENTIFIABLE_AS_SINGLE_MASK_SPECIFIC_PRECISION_OPERATOR_AFTER_QUANTIFIED_NUMERICAL_AND_FUNCTIONAL_TEST",
            "reason":
                "At least one mask has edge-to-edge precision differences that are neither numerically equivalent under the frozen V2 tolerances nor functionally negligible for the exact downstream Q028 quadratic diagnostics.",
            "claim_boundaries": c["claim_boundaries"],
            "journal_preservation": c["journal_preservation"],
        }
        write_json(a.output, out)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    # Exact labelled intersection. Sort deterministically to create one common basis.
    common = set(per_mask_keys[MASKS[0]])
    for mask in MASKS[1:]:
        common &= set(per_mask_keys[mask])
    common_keys = sorted(common, key=lambda k: (k[0], k[1], k[2]))
    if not common_keys:
        raise RuntimeError("COMMON_SUPPORT_NONEMPTY_GATE=FAIL")

    common_precision = {}
    support_meta = {}
    for mask in MASKS:
        validate_spd(per_mask_precision[mask], c, f"mask{mask}:full")
        Pm, meta, _ = marginal_precision_from_full_precision(
            per_mask_precision[mask], per_mask_keys[mask], common_keys, c, f"mask{mask}"
        )
        common_precision[mask] = Pm
        support_meta[str(mask)] = meta

    min_frac = min(v["common_fraction"] for v in support_meta.values())
    interpretability_gate = min_frac >= float(c["validation"]["minimum_common_support_fraction"])

    # Counterfactual matrix per lineage edge: F[residual_mask][precision_mask].
    counterfactual = {}
    shapley_rows = []
    for sa, sb in EDGES:
        ek = f"e{sa}{sb}"
        matrix = {}
        qstates = {}
        for rmask in MASKS:
            matrix[str(rmask)] = {}
            qstates[str(rmask)] = {}
            for pmask in MASKS:
                val, qs = interaction_for_family(
                    families[rmask][ek], common_precision[pmask], common_keys
                )
                matrix[str(rmask)][str(pmask)] = val
                qstates[str(rmask)][str(pmask)] = qs

        comparisons = {}
        for ia, ma in enumerate(MASKS):
            for mb in MASKS[ia + 1:]:
                Faa = matrix[str(ma)][str(ma)]
                Fab = matrix[str(ma)][str(mb)]
                Fba = matrix[str(mb)][str(ma)]
                Fbb = matrix[str(mb)][str(mb)]
                sh = shapley_two_factor(Faa, Fab, Fba, Fbb)
                ck = f"m{ma}_vs_m{mb}"
                comparisons[ck] = sh
                shapley_rows.append({"edge": ek, "mask_pair": [ma, mb], **sh})
        counterfactual[ek] = {
            "interaction_matrix_residual_mask_by_precision_mask": matrix,
            "state_quadratics": qstates,
            "mask_pair_shapley": comparisons,
        }

    closure_tol = float(c["validation"]["shapley_closure_abs_tol"])
    closure_gate = all(abs(float(x["closure_error"])) <= closure_tol for x in shapley_rows)

    # Compare the common-support diagonal with each source-mask full-support diagnostic.
    diagonal_support_effects = {}
    for mask in MASKS:
        diagonal_support_effects[str(mask)] = {}
        for sa, sb in EDGES:
            ek = f"e{sa}{sb}"
            full_q = {
                sid: families[mask][ek][sid]["full_highl_chi2"]
                for sid in STATES
            }
            full_i = contrast(full_q)
            common_i = counterfactual[ek]["interaction_matrix_residual_mask_by_precision_mask"][str(mask)][str(mask)]
            diagonal_support_effects[str(mask)][ek] = {
                "full_support_pair_interaction": full_i,
                "common_support_marginal_pair_interaction": common_i,
                "common_minus_full": common_i - full_i,
            }

    classif = (
        classify(shapley_rows, c)
        if interpretability_gate and closure_gate
        else "DISTRIBUTED_NON_IDENTIFIABLE_UNDER_CURRENT_VALID_COMMON_SUPPORT"
    )

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "status": "COMPLETE",
        "actual_new_likelihood_evaluations": eval_count,
        "optimizer_evaluations": 0,
        "sampling_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "scientific_surface": {
            "model": c["model"],
            "likelihood": FULL_LIKE,
            "masks": list(MASKS),
            "authoritative_endpoints": "Q022_V2_UNCHANGED",
            "parents": c["parents"],
        },
        "common_support": {
            "construction":
                "LABEL_INTERSECTION_PLUS_SCHUR_COMPLEMENT_MARGINAL_PRECISION",
            "dimension": len(common_keys),
            "keys_sha256": hashlib.sha256(
                json.dumps(common_keys, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "mask_metadata": support_meta,
            "minimum_common_support_fraction": min_frac,
            "interpretability_gate": interpretability_gate,
            "principal_precision_submatrix_used_as_marginal": False,
        },
        "precision_invariance_across_edges_by_mask": precision_edge_gate,
        "counterfactual": counterfactual,
        "shapley_rows": shapley_rows,
        "shapley_closure_gate": closure_gate,
        "diagonal_support_effects": diagonal_support_effects,
        "scientific_classification": classif,
        "interpretation": {
            "residual_side_definition":
                "DATA_MINUS_MODEL_RESIDUAL_FAMILY; DOES_NOT SEPARATE RAW DATA FROM MODEL/NUISANCE VECTOR",
            "precision_side_definition":
                "MASK-SPECIFIC MARGINAL PRECISION OPERATOR ON EXACT COMMON LABELLED SUPPORT",
            "lineage_warning":
                "Edge IDs are Q022 lineage labels, not independently established universal physical posterior modes; Q024 non-universality remains preserved.",
            "causal_status":
                "FUNCTIONAL COUNTERFACTUAL ATTRIBUTION WITHIN THE FROZEN CAMSPEC CONSTRUCTION; NOT PHYSICAL CAUSALITY",
        },
        "claim_boundaries": c["claim_boundaries"],
        "journal_preservation": c["journal_preservation"],
        "parents_observed": {
            "q025": q025_parent.get("result_id"),
            "q026": q026_parent.get("result_id"),
            "q027": q027_parent.get("result_id"),
        },
        "stop_condition":
            "Stop after common-support validity, fixed-vector completeness, signed residual×precision counterfactuals, Shapley closure, and mandatory tests. Do not optimize or rerun Q024.",
    }
    write_json(a.output, out)
    print(json.dumps(out, indent=2, sort_keys=True, default=_json_default))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
