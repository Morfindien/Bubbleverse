#!/usr/bin/env python3
"""
Bubbleverse Q030 V2 — exact interaction-preserving Q029 decomposition.

CURRENT Q
---------
Q030

Scientific target
-----------------
On the exact Q028 V8 common support, reconstruct for each of the nine
mask x edge diagnostics

    F = T_DM + T_MM

with

    T_DM = -2 d^T P Delta2(m)
    T_MM = Delta2(m^T P m)
    Delta2(m) = -Delta2(r)

where r = d - m.

The terms are exact likelihood functionals. They are NOT identified physical
causes and MUST NOT be renamed "data contribution" or "model cause".

Execution contract
------------------
* Reuse Q028 V8 family residual checkpoints.
* Extract d directly from the initialized frozen CamSpec likelihood object.
* Reconstruct the same symmetrized Schur precision action used by Q028 V8.
* Perform zero new likelihood evaluations, zero optimization, zero sampling.
* Reuse authoritative Q022 V2 endpoints only to initialize the frozen model.
* Preserve signed covariance coupling.
* Spectrum and multipole distributions retain explicit group-pair interactions;
  covariance-coupled group terms are not independent likelihoods.
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

Q = "Q030"
RUN = "Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V2"
RESULT = "R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-002"

PARENT_Q028_Q = "Q028"
PARENT_Q028_RUN = "Q028-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-V8"
PARENT_Q028_RESULT = "R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-008"

FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
MASKS = (3, 6, 7)
EDGES = ((0, 1), (0, 2), (1, 2))
STATES = ("00", "10", "01", "11")

EXPECTED_COMMON_DIMENSION = 9915
EXPECTED_COMMON_SHA256 = "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"
SUPERSEDED_MISRECORDED_COMMON_SHA256 = "054220c018e58e902eab98b879eec4a823fb3238a1774ddbacc649bddca8b666"
EXPECTED_Q028_HEAD_SHA = "7f5d35c0725530039162adfa4d71be288e8b4462"
EXPECTED_Q028_ARTIFACT_ID = 9967068363
EXPECTED_Q028_ARTIFACT_SHA256 = "7dfbd1f27251ff311dd1de6118539dd691ab03d9afdb08539b3b13586c50d5af"
EXPECTED_BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"


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


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL {path}")
    return obj


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def sha256_jsonable(x: Any) -> str:
    return hashlib.sha256(
        json.dumps(x, separators=(",", ":"), sort_keys=False).encode("utf-8")
    ).hexdigest()


def sha256_array(a: np.ndarray) -> str:
    x = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(x.shape).encode("ascii"))
    h.update(x.tobytes())
    return h.hexdigest()


def edge_key(sa: int, sb: int) -> str:
    if (int(sa), int(sb)) not in EDGES:
        raise RuntimeError(f"EDGE_SCOPE_GATE=FAIL {(sa, sb)}")
    return f"e{int(sa)}{int(sb)}"


def contrast(values: Mapping[str, float]) -> float:
    return (
        float(values["11"])
        - float(values["10"])
        - float(values["01"])
        + float(values["00"])
    )


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(c, dict):
        raise RuntimeError("CONFIG_GATE=FAIL")

    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_RESULT_IDENTITY_GATE=FAIL")

    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend"] != "mwt5345/class_ede":
        raise RuntimeError("BACKEND_REPOSITORY_GATE=FAIL")
    if m["backend_commit"] != EXPECTED_BACKEND_COMMIT:
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")

    if c["likelihood"]["full_mf"] != FULL_LIKE:
        raise RuntimeError("LIKELIHOOD_GATE=FAIL")
    if tuple(map(int, c["execution"]["masks"])) != MASKS:
        raise RuntimeError("MASK_SCOPE_GATE=FAIL")
    if tuple(tuple(map(int, e)) for e in c["execution"]["edges"]) != EDGES:
        raise RuntimeError("EDGE_SCOPE_GATE=FAIL")

    q28 = c["parents"]["q028_v8"]
    if int(q28["github_run_id"]) != 33957937309:
        raise RuntimeError("Q028_RUN_GATE=FAIL")
    if q28["head_sha"] != EXPECTED_Q028_HEAD_SHA:
        raise RuntimeError("Q028_HEAD_SHA_GATE=FAIL")
    if int(q28["final_artifact_id"]) != EXPECTED_Q028_ARTIFACT_ID:
        raise RuntimeError("Q028_ARTIFACT_ID_GATE=FAIL")
    if q28["final_artifact_sha256"] != EXPECTED_Q028_ARTIFACT_SHA256:
        raise RuntimeError("Q028_ARTIFACT_SHA256_GATE=FAIL")
    if int(q28["common_dimension"]) != EXPECTED_COMMON_DIMENSION:
        raise RuntimeError("Q028_COMMON_DIMENSION_CONFIG_GATE=FAIL")
    if q28["common_support_sha256"] != EXPECTED_COMMON_SHA256:
        raise RuntimeError("Q028_COMMON_SHA_CONFIG_GATE=FAIL")
    if q28.get("misrecorded_common_support_sha256_rejected") != SUPERSEDED_MISRECORDED_COMMON_SHA256:
        raise RuntimeError("Q028_MISRECORDED_COMMON_SHA_PROVENANCE_GATE=FAIL")

    must_true = (
        "no_optimization",
        "no_sampling",
        "no_q024_rerun",
        "no_new_likelihood_evaluations",
        "reuse_q028_family_residuals",
        "extract_data_vector_without_logposterior",
        "reuse_q028_schur_semantics",
        "preserve_signed_accounting",
        "preserve_covariance_cross_terms",
        "no_data_only_contribution",
        "no_causal_allocation",
        "no_cosmology_calibration_allocation",
        "group_pair_terms_are_not_independent_likelihoods",
    )
    for key in must_true:
        if c["rules"].get(key) is not True:
            raise RuntimeError(f"{key.upper()}_GATE=FAIL")

    bands = c["decomposition"].get("ell_bands", [])
    if not bands or not all(
        isinstance(b, Mapping)
        and {"name", "min", "max"}.issubset(b)
        and int(b["min"]) <= int(b["max"])
        for b in bands
    ):
        raise RuntimeError("ELL_BAND_SCHEMA_GATE=FAIL")

    return c


def family_filename(mask: int, ek: str) -> str:
    return f"q028_v8_family_m{mask}_{ek}.json"


def load_mask_families(directory: str | Path, mask: int) -> dict[str, dict[str, Any]]:
    d = Path(directory)
    out: dict[str, dict[str, Any]] = {}
    baseline_keys = None
    for sa, sb in EDGES:
        ek = edge_key(sa, sb)
        p = d / family_filename(mask, ek)
        if not p.exists():
            raise RuntimeError(f"Q028_FAMILY_CHECKPOINT_MISSING_GATE=FAIL {p}")
        x = read_json(p)
        if not (
            x.get("q") == PARENT_Q028_Q
            and x.get("run_id") == PARENT_Q028_RUN
            and x.get("result_id") == PARENT_Q028_RESULT
            and x.get("phase") == "FAMILY"
            and x.get("status") == "COMPLETE"
            and int(x.get("mask", -1)) == mask
            and x.get("edge") == ek
            and int(x.get("likelihood_evaluations", -1)) == 4
        ):
            raise RuntimeError(f"Q028_FAMILY_IDENTITY_GATE=FAIL {p}")
        if set(x.get("states", {})) != set(STATES):
            raise RuntimeError(f"Q028_FAMILY_STATE_GATE=FAIL {p}")
        keys = x["states"]["00"]["keys"]
        if any(x["states"][s]["keys"] != keys for s in STATES):
            raise RuntimeError(f"Q028_FAMILY_WITHIN_EDGE_ROW_GATE=FAIL {p}")
        if baseline_keys is None:
            baseline_keys = keys
        elif keys != baseline_keys:
            raise RuntimeError("Q028_FAMILY_WITHIN_MASK_ROW_GATE=FAIL")
        out[ek] = x
    return out


def load_support(path: str | Path, c: Mapping[str, Any]) -> dict[str, Any]:
    s = read_json(path)
    if not (
        s.get("q") == PARENT_Q028_Q
        and s.get("run_id") == PARENT_Q028_RUN
        and s.get("result_id") == PARENT_Q028_RESULT
        and s.get("phase") == "SUPPORT"
        and s.get("status") == "COMPLETE"
    ):
        raise RuntimeError("Q028_SUPPORT_IDENTITY_GATE=FAIL")

    common_keys = s.get("common_keys")
    if not isinstance(common_keys, list):
        raise RuntimeError("Q028_COMMON_KEYS_GATE=FAIL")
    if int(s.get("common_dimension", -1)) != EXPECTED_COMMON_DIMENSION:
        raise RuntimeError("Q028_COMMON_DIMENSION_GATE=FAIL")
    if s.get("common_keys_sha256") != EXPECTED_COMMON_SHA256:
        raise RuntimeError("Q028_COMMON_SUPPORT_SHA_GATE=FAIL")
    if sha256_jsonable(common_keys) != EXPECTED_COMMON_SHA256:
        raise RuntimeError("Q028_COMMON_SUPPORT_REHASH_GATE=FAIL")
    if c["parents"]["q028_v8"]["common_support_sha256"] != EXPECTED_COMMON_SHA256:
        raise RuntimeError("Q028_COMMON_SUPPORT_CONFIG_GATE=FAIL")
    return s


def project_vector(
    full_vector: np.ndarray,
    full_keys: list[tuple[str, str, int]],
    common_keys: list[tuple[str, str, int]],
) -> np.ndarray:
    idx = {k: i for i, k in enumerate(full_keys)}
    if len(idx) != len(full_keys):
        raise RuntimeError("RECIPIENT_ROW_KEY_UNIQUENESS_GATE=FAIL")
    if any(k not in idx for k in common_keys):
        raise RuntimeError("COMMON_SUPPORT_INDEX_GATE=FAIL")
    return np.asarray([full_vector[idx[k]] for k in common_keys], dtype=np.float64)


def project_residual(
    state: Mapping[str, Any],
    common_keys: list[tuple[str, str, int]],
) -> np.ndarray:
    keys = [tuple(x) for x in state["keys"]]
    residual = np.asarray(state["residual"], dtype=np.float64)
    if residual.shape != (len(keys),):
        raise RuntimeError("RESIDUAL_SHAPE_GATE=FAIL")
    return project_vector(residual, keys, common_keys)


def schur_actions(
    P_raw: np.ndarray,
    recipient_keys: list[tuple[str, str, int]],
    common_keys: list[tuple[str, str, int]],
    columns: Mapping[str, np.ndarray],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    """
    Apply the exact Q028 V8 symmetrized Schur-marginal precision operator
    to many common-support vectors without materializing P_common.

    For X supported only on S:
        Y = P_sym X
        P_marg X_S = Y_S - P_ST P_TT^-1 Y_T
    with P_sym = (P_raw + P_raw.T)/2.
    """
    P_raw = np.asarray(P_raw, dtype=np.float64)
    n = len(recipient_keys)
    if P_raw.shape != (n, n):
        raise RuntimeError(f"PRECISION_SHAPE_GATE=FAIL {P_raw.shape} != {(n, n)}")
    if not np.all(np.isfinite(P_raw)):
        raise RuntimeError("FINITE_PRECISION_GATE=FAIL")
    if not columns:
        raise RuntimeError("SCHUR_COLUMN_GATE=FAIL empty")

    idx = {k: i for i, k in enumerate(recipient_keys)}
    if len(idx) != n:
        raise RuntimeError("RECIPIENT_ROW_KEY_UNIQUENESS_GATE=FAIL")
    if any(k not in idx for k in common_keys):
        raise RuntimeError("SCHUR_COMMON_INDEX_GATE=FAIL")

    S = np.asarray([idx[k] for k in common_keys], dtype=np.int64)
    keep = np.zeros(n, dtype=bool)
    keep[S] = True
    T = np.flatnonzero(~keep)

    names = list(columns)
    X = np.zeros((n, len(names)), dtype=np.float64)
    for j, name in enumerate(names):
        v = np.asarray(columns[name], dtype=np.float64)
        if v.shape != (len(common_keys),):
            raise RuntimeError(f"SCHUR_VECTOR_SHAPE_GATE=FAIL {name} {v.shape}")
        if not np.all(np.isfinite(v)):
            raise RuntimeError(f"SCHUR_VECTOR_FINITE_GATE=FAIL {name}")
        X[S, j] = v

    # This is the exact Q028 V8 precision symmetrization.
    Y = 0.5 * (
        np.asarray(P_raw @ X, dtype=np.float64)
        + np.asarray(P_raw.T @ X, dtype=np.float64)
    )
    A = np.asarray(Y[S, :], dtype=np.float64)

    meta: dict[str, Any] = {
        "method": "Q028_V8_SYMMETRIZED_SCHUR_ACTION_NO_COMMON_PRECISION_MATERIALIZATION",
        "full_dimension": n,
        "common_dimension": int(len(S)),
        "excluded_dimension": int(len(T)),
        "column_count": int(len(names)),
        "materialized_common_precision": False,
        "principal_precision_submatrix_used_as_marginal": False,
    }

    if len(T):
        Ptt_raw = np.asarray(P_raw[np.ix_(T, T)], dtype=np.float64)
        Ptt = 0.5 * (Ptt_raw + Ptt_raw.T)
        try:
            L = np.linalg.cholesky(Ptt)
        except np.linalg.LinAlgError as exc:
            raise RuntimeError("EXCLUDED_PTT_SPD_GATE=FAIL") from exc

        # Y_T = P_TS X_S. Solve P_TT Z = Y_T.
        B = np.asarray(Y[T, :], dtype=np.float64)
        Z = np.linalg.solve(Ptt, B)

        # Need P_ST Z. Apply P_sym to a vector supported on T.
        V = np.zeros_like(X)
        V[T, :] = Z
        W = 0.5 * (
            np.asarray(P_raw @ V, dtype=np.float64)
            + np.asarray(P_raw.T @ V, dtype=np.float64)
        )
        A -= W[S, :]

        solve_resid = Ptt @ Z - B
        denom = max(1.0, float(np.linalg.norm(B)))
        meta.update(
            {
                "excluded_block_min_cholesky_diagonal": float(np.min(np.diag(L))),
                "schur_solve_relative_residual": float(np.linalg.norm(solve_resid) / denom),
            }
        )
    else:
        meta.update(
            {
                "method": "Q028_V8_IDENTICAL_SUPPORT_FULL_SYMMETRIZED_PRECISION_ACTION",
                "schur_solve_relative_residual": 0.0,
            }
        )

    if not np.all(np.isfinite(A)):
        raise RuntimeError("FINITE_SCHUR_ACTION_GATE=FAIL")

    return {name: A[:, j].copy() for j, name in enumerate(names)}, meta


def band_name(ell: int, c: Mapping[str, Any]) -> str:
    for b in c["decomposition"]["ell_bands"]:
        if int(b["min"]) <= int(ell) <= int(b["max"]):
            return str(b["name"])
    raise RuntimeError(f"ELL_BAND_COVERAGE_GATE=FAIL ell={ell}")


def grouping(
    common_keys: list[tuple[str, str, int]],
    mode: str,
    c: Mapping[str, Any],
) -> dict[str, np.ndarray]:
    labels: list[str] = []
    for obs, spec, ell in common_keys:
        if mode == "spectrum":
            labels.append(str(spec))
        elif mode == "ell_band":
            labels.append(band_name(int(ell), c))
        else:
            raise RuntimeError(f"GROUPING_MODE_GATE=FAIL {mode}")

    groups: dict[str, np.ndarray] = {}
    a = np.asarray(labels, dtype=object)
    for name in sorted(set(labels)):
        groups[name] = a == name

    cover = np.zeros(len(common_keys), dtype=np.int64)
    for mask in groups.values():
        cover += mask.astype(np.int64)
    if not np.all(cover == 1):
        raise RuntimeError(f"GROUP_PARTITION_GATE=FAIL mode={mode}")
    return groups


def masked(v: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(v, dtype=np.float64)
    out[mask] = v[mask]
    return out


def add_edge_columns(
    columns: dict[str, np.ndarray],
    ek: str,
    d: np.ndarray,
    delta_m: np.ndarray,
    m_states: Mapping[str, np.ndarray],
    r_states: Mapping[str, np.ndarray],
    groupings: Mapping[str, Mapping[str, np.ndarray]],
) -> None:
    columns[f"{ek}|full|delta_m"] = delta_m
    for s in STATES:
        columns[f"{ek}|full|m|{s}"] = m_states[s]
        columns[f"{ek}|full|r|{s}"] = r_states[s]

    for mode, groups in groupings.items():
        for g, gm in groups.items():
            columns[f"{ek}|{mode}|delta_m|{g}"] = masked(delta_m, gm)
            for s in STATES:
                columns[f"{ek}|{mode}|m|{s}|{g}"] = masked(m_states[s], gm)


def pair_distribution(
    ek: str,
    mode: str,
    d: np.ndarray,
    delta_m: np.ndarray,
    m_states: Mapping[str, np.ndarray],
    groups: Mapping[str, np.ndarray],
    actions: Mapping[str, np.ndarray],
    totals: Mapping[str, float],
) -> dict[str, Any]:
    names = sorted(groups)
    pairs: dict[str, dict[str, float]] = {}

    for i, g in enumerate(names):
        mg = groups[g]
        dg = masked(d, mg)
        for h in names[i:]:
            mh = groups[h]
            dh = masked(d, mh)

            A_dmh = actions[f"{ek}|{mode}|delta_m|{h}"]
            if g == h:
                tdm = -2.0 * float(dg @ A_dmh)
            else:
                A_dmg = actions[f"{ek}|{mode}|delta_m|{g}"]
                tdm = -2.0 * (
                    float(dg @ A_dmh)
                    + float(dh @ A_dmg)
                )

            qpair: dict[str, float] = {}
            for s in STATES:
                m_g = masked(m_states[s], mg)
                A_m_h = actions[f"{ek}|{mode}|m|{s}|{h}"]
                if g == h:
                    qpair[s] = float(m_g @ A_m_h)
                else:
                    m_h = masked(m_states[s], mh)
                    A_m_g = actions[f"{ek}|{mode}|m|{s}|{g}"]
                    qpair[s] = float(m_g @ A_m_h) + float(m_h @ A_m_g)

            tmm = contrast(qpair)
            f = tdm + tmm
            pairs[f"{g} <-> {h}"] = {
                "T_DM_data_model_factorial_coupling": float(tdm),
                "T_MM_model_quadratic": float(tmm),
                "F_reconstructed": float(f),
            }

    sums = {
        "T_DM_data_model_factorial_coupling": float(
            sum(x["T_DM_data_model_factorial_coupling"] for x in pairs.values())
        ),
        "T_MM_model_quadratic": float(
            sum(x["T_MM_model_quadratic"] for x in pairs.values())
        ),
        "F_reconstructed": float(sum(x["F_reconstructed"] for x in pairs.values())),
    }
    closure = {
        k: float(sums[k] - float(totals[k]))
        for k in sums
    }
    return {
        "mode": mode,
        "semantics": (
            "EXACT_UNORDERED_GROUP_PAIR_DECOMPOSITION_WITH_CROSS_GROUP_COVARIANCE_"
            "TERMS_RETAINED; TERMS_ARE_NOT_INDEPENDENT_LIKELIHOODS_OR_CAUSAL_CAUSES"
        ),
        "groups": names,
        "pairs": pairs,
        "sums": sums,
        "closure_error_vs_total": closure,
    }


def phase_mask(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    import q025_fullmf_component_attribution_v2 as q25

    mask = int(a.mask)
    if mask not in MASKS:
        raise RuntimeError("MASK_GATE=FAIL")

    families = load_mask_families(a.family_dir, mask)
    support = load_support(a.support_result, c)
    common_keys = [tuple(x) for x in support["common_keys"]]

    # All three Q028 family checkpoints in this mask have the exact same row basis.
    first_edge = edge_key(*EDGES[0])
    recipient_keys = [tuple(x) for x in families[first_edge]["states"]["00"]["keys"]]
    for ek, fam in families.items():
        for s in STATES:
            if [tuple(x) for x in fam["states"][s]["keys"]] != recipient_keys:
                raise RuntimeError(f"RECIPIENT_ROW_ALIGNMENT_GATE=FAIL {ek}:{s}")

    # Reuse the authoritative Q022 V2 endpoint only as a seed for model construction.
    # No logposterior call is made anywhere in Q030.
    parent25_cfg = q25.load_cfg(ROOT / c["reuse"]["q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)
    seed0 = q25.load_q022_endpoint(
        a.q022_dir, a.q021_dir, final22, mask, 0
    )["params"]

    model = q25.build_full_model(parent25_cfg, seed0)
    try:
        like = model.likelihood[FULL_LIKE]
        d_full = np.asarray(like.data_vector, dtype=np.float64).copy()
        P_raw = np.asarray(like.covinv, dtype=np.float64)

        if d_full.shape != (len(recipient_keys),):
            raise RuntimeError(
                f"DATA_VECTOR_SHAPE_GATE=FAIL {d_full.shape} != {(len(recipient_keys),)}"
            )
        if P_raw.shape != (len(recipient_keys), len(recipient_keys)):
            raise RuntimeError("PRECISION_SHAPE_GATE=FAIL")
        if not np.all(np.isfinite(d_full)):
            raise RuntimeError("FINITE_DATA_VECTOR_GATE=FAIL")

        d = project_vector(d_full, recipient_keys, common_keys)
        if d.shape != (EXPECTED_COMMON_DIMENSION,):
            raise RuntimeError("COMMON_DATA_VECTOR_SHAPE_GATE=FAIL")

        groupings = {
            "spectrum": grouping(common_keys, "spectrum", c),
            "ell_band": grouping(common_keys, "ell_band", c),
        }

        edge_state: dict[str, Any] = {}
        columns: dict[str, np.ndarray] = {}

        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            fam = families[ek]
            r_states = {
                s: project_residual(fam["states"][s], common_keys)
                for s in STATES
            }
            m_states = {s: d - r_states[s] for s in STATES}

            delta_r = (
                r_states["11"] - r_states["10"] - r_states["01"] + r_states["00"]
            )
            delta_m = (
                m_states["11"] - m_states["10"] - m_states["01"] + m_states["00"]
            )
            delta_identity_max_abs = float(np.max(np.abs(delta_m + delta_r)))
            if delta_identity_max_abs > float(c["validation"]["delta_m_identity_abs_tol"]):
                raise RuntimeError(
                    f"DELTA_M_EQUALS_MINUS_DELTA_R_GATE=FAIL {ek} "
                    f"max_abs={delta_identity_max_abs}"
                )

            edge_state[ek] = {
                "r_states": r_states,
                "m_states": m_states,
                "delta_r": delta_r,
                "delta_m": delta_m,
                "delta_identity_max_abs": delta_identity_max_abs,
            }
            add_edge_columns(
                columns, ek, d, delta_m, m_states, r_states, groupings
            )

        actions, schur_meta = schur_actions(
            P_raw, recipient_keys, common_keys, columns
        )

        diagnostics: dict[str, Any] = {}
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            x = edge_state[ek]
            delta_m = x["delta_m"]
            m_states = x["m_states"]
            r_states = x["r_states"]

            tdm = -2.0 * float(
                d @ actions[f"{ek}|full|delta_m"]
            )

            qm = {
                s: float(m_states[s] @ actions[f"{ek}|full|m|{s}"])
                for s in STATES
            }
            tmm = contrast(qm)

            qr = {
                s: float(r_states[s] @ actions[f"{ek}|full|r|{s}"])
                for s in STATES
            }
            f_residual = contrast(qr)
            f_reconstructed = tdm + tmm
            identity_closure = float(f_reconstructed - f_residual)

            totals = {
                "T_DM_data_model_factorial_coupling": float(tdm),
                "T_MM_model_quadratic": float(tmm),
                "F_reconstructed": float(f_reconstructed),
            }

            distributions = {
                mode: pair_distribution(
                    ek,
                    mode,
                    d,
                    delta_m,
                    m_states,
                    groups,
                    actions,
                    totals,
                )
                for mode, groups in groupings.items()
            }

            mag_dm = abs(tdm)
            mag_mm = abs(tmm)
            if math.isclose(mag_dm, mag_mm, rel_tol=0.0, abs_tol=float(c["validation"]["term_tie_abs_tol"])):
                dominance = "SIGNED_MAGNITUDES_TIED_WITHIN_TOLERANCE"
            elif mag_dm > mag_mm:
                dominance = "DATA_MODEL_FACTORIAL_COUPLING_LARGER_ABSOLUTE_MAGNITUDE"
            else:
                dominance = "MODEL_QUADRATIC_LARGER_ABSOLUTE_MAGNITUDE"

            denom = max(mag_dm + mag_mm, np.finfo(np.float64).tiny)
            cancellation_fraction = float(
                1.0 - abs(f_reconstructed) / denom
            )

            diagnostics[ek] = {
                "mask": mask,
                "edge": ek,
                "lineage_endpoints": [sa, sb],
                "terms": totals,
                "F_direct_from_residual_quadratic": float(f_residual),
                "Q029_identity_closure_error": identity_closure,
                "delta2m_equals_minus_delta2r_max_abs_error": float(
                    x["delta_identity_max_abs"]
                ),
                "absolute_magnitudes": {
                    "abs_T_DM": mag_dm,
                    "abs_T_MM": mag_mm,
                    "abs_F": abs(f_reconstructed),
                },
                "signed_cancellation_fraction": cancellation_fraction,
                "magnitude_relation": dominance,
                "distributions": distributions,
                "interpretation_boundary": {
                    "T_DM_name": "DATA_MODEL_FACTORIAL_COUPLING",
                    "T_DM_is_data_only_contribution": False,
                    "T_MM_name": "MODEL_QUADRATIC_FUNCTIONAL_TERM",
                    "T_MM_is_physical_model_cause": False,
                    "physical_causality_claimed": False,
                    "cosmology_calibration_allocation_performed": False,
                    "shapley_identification_used": False,
                },
            }

        out = {
            "q": Q,
            "run_id": RUN,
            "result_id": RESULT,
            "phase": "MASK",
            "status": "COMPLETE",
            "mask": mask,
            "scientific_question": c["project"]["question"],
            "model": c["model"],
            "likelihood": c["likelihood"],
            "q028_parent": c["parents"]["q028_v8"],
            "common_support": {
                "dimension": EXPECTED_COMMON_DIMENSION,
                "sha256": EXPECTED_COMMON_SHA256,
            },
            "data_vector": {
                "extraction": (
                    "DIRECT_FROM_INITIALIZED_FROZEN_CAMSPEC_LIKELIHOOD_OBJECT_"
                    "like.data_vector_WITHOUT_LOGPOSTERIOR"
                ),
                "full_dimension": int(len(d_full)),
                "common_dimension": int(len(d)),
                "full_sha256": sha256_array(d_full),
                "common_sha256": sha256_array(d),
            },
            "precision": {
                "extraction": "DIRECT_FROM_INITIALIZED_FROZEN_CAMSPEC_LIKELIHOOD_OBJECT_like.covinv",
                "full_shape": list(P_raw.shape),
                "full_sha256": sha256_array(P_raw),
                "action": schur_meta,
            },
            "execution_counts": {
                "model_initializations": 1,
                "new_likelihood_evaluations": 0,
                "optimizer_evaluations": 0,
                "sampling_evaluations": 0,
                "q024_permutations_evaluated": 0,
            },
            "diagnostic_count": len(diagnostics),
            "diagnostics": diagnostics,
            "claim_boundaries": c["claim_boundaries"],
        }
        write_json(a.output, out)
        print(
            f"Q030_MASK_GATE=PASS mask={mask} diagnostics={len(diagnostics)} "
            f"new_likelihood_evaluations=0"
        )
        return 0
    finally:
        try:
            model.close()
        except Exception:
            pass


def load_q028_final(path: str | Path, c: Mapping[str, Any]) -> dict[str, Any]:
    q28 = read_json(path)
    if not (
        q28.get("q") == PARENT_Q028_Q
        and q28.get("run_id") == PARENT_Q028_RUN
        and q28.get("result_id") == PARENT_Q028_RESULT
        and q28.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("Q028_FINAL_PARENT_GATE=FAIL")

    cs = q28.get("common_support", {})
    if int(cs.get("dimension", -1)) != EXPECTED_COMMON_DIMENSION:
        raise RuntimeError("Q028_FINAL_COMMON_DIMENSION_GATE=FAIL")
    if cs.get("keys_sha256") != EXPECTED_COMMON_SHA256:
        raise RuntimeError("Q028_FINAL_COMMON_SHA_GATE=FAIL")

    expected = c["parents"]["q028_v8"]
    if expected["head_sha"] != EXPECTED_Q028_HEAD_SHA:
        raise RuntimeError("Q028_CONFIG_HEAD_SHA_GATE=FAIL")
    return q28


def load_mask_results(directory: str | Path) -> dict[int, dict[str, Any]]:
    d = Path(directory)
    out: dict[int, dict[str, Any]] = {}
    for mask in MASKS:
        p = d / f"q030_v2_mask_m{mask}.json"
        if not p.exists():
            raise RuntimeError(f"Q030_MASK_RESULT_MISSING_GATE=FAIL {p}")
        x = read_json(p)
        if not (
            x.get("q") == Q
            and x.get("run_id") == RUN
            and x.get("result_id") == RESULT
            and x.get("phase") == "MASK"
            and x.get("status") == "COMPLETE"
            and int(x.get("mask", -1)) == mask
            and int(x.get("diagnostic_count", -1)) == 3
        ):
            raise RuntimeError(f"Q030_MASK_RESULT_IDENTITY_GATE=FAIL {p}")
        out[mask] = x
    return out


def phase_merge(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    masks = load_mask_results(a.mask_dir)
    q28 = load_q028_final(a.q028_final, c)

    q28_diag = q28.get("diagonal_support_effects", {})
    tol = float(c["validation"]["q028_parent_interaction_abs_tol"])

    diagnostics: list[dict[str, Any]] = []
    max_parent_error = 0.0
    total_new_evals = 0
    total_opt = 0
    total_sampling = 0
    total_q024 = 0
    total_model_initializations = 0

    lineage_objects = {}
    for mask in MASKS:
        lineage_objects[str(mask)] = {
            "data_vector": masks[mask]["data_vector"],
            "precision": masks[mask]["precision"],
        }
        counts = masks[mask]["execution_counts"]
        total_model_initializations += int(counts["model_initializations"])
        total_new_evals += int(counts["new_likelihood_evaluations"])
        total_opt += int(counts["optimizer_evaluations"])
        total_sampling += int(counts["sampling_evaluations"])
        total_q024 += int(counts["q024_permutations_evaluated"])

        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            diag = dict(masks[mask]["diagnostics"][ek])
            parent_f = float(
                q28_diag[str(mask)][ek]["common_support_marginal_pair_interaction"]
            )
            this_f = float(diag["terms"]["F_reconstructed"])
            err = float(this_f - parent_f)
            max_parent_error = max(max_parent_error, abs(err))
            diag["Q028_parent_common_support_F"] = parent_f
            diag["Q028_parent_closure_error"] = err
            diagnostics.append(diag)

    if len(diagnostics) != 9:
        raise RuntimeError("NINE_DIAGNOSTIC_COMPLETENESS_GATE=FAIL")
    if max_parent_error > tol:
        raise RuntimeError(
            f"Q028_PARENT_FUNCTIONAL_CLOSURE_GATE=FAIL "
            f"max_abs={max_parent_error} tol={tol}"
        )
    if any((total_new_evals, total_opt, total_sampling, total_q024)):
        raise RuntimeError("ZERO_NEW_EXECUTION_GATE=FAIL")

    tdm = np.asarray(
        [d["terms"]["T_DM_data_model_factorial_coupling"] for d in diagnostics],
        dtype=np.float64,
    )
    tmm = np.asarray(
        [d["terms"]["T_MM_model_quadratic"] for d in diagnostics],
        dtype=np.float64,
    )
    ff = np.asarray(
        [d["terms"]["F_reconstructed"] for d in diagnostics],
        dtype=np.float64,
    )

    dominance_counts: dict[str, int] = {}
    for d in diagnostics:
        k = str(d["magnitude_relation"])
        dominance_counts[k] = dominance_counts.get(k, 0) + 1

    def stats(x: np.ndarray) -> dict[str, float]:
        return {
            "signed_sum": float(np.sum(x)),
            "mean": float(np.mean(x)),
            "median": float(np.median(x)),
            "mean_absolute": float(np.mean(np.abs(x))),
            "median_absolute": float(np.median(np.abs(x))),
            "max_absolute": float(np.max(np.abs(x))),
        }

    by_mask: dict[str, Any] = {}
    for mask in MASKS:
        rows = [d for d in diagnostics if int(d["mask"]) == mask]
        by_mask[str(mask)] = {
            "T_DM": stats(np.asarray(
                [r["terms"]["T_DM_data_model_factorial_coupling"] for r in rows]
            )),
            "T_MM": stats(np.asarray(
                [r["terms"]["T_MM_model_quadratic"] for r in rows]
            )),
            "F": stats(np.asarray([r["terms"]["F_reconstructed"] for r in rows])),
        }

    by_edge: dict[str, Any] = {}
    for sa, sb in EDGES:
        ek = edge_key(sa, sb)
        rows = [d for d in diagnostics if d["edge"] == ek]
        by_edge[ek] = {
            "T_DM": stats(np.asarray(
                [r["terms"]["T_DM_data_model_factorial_coupling"] for r in rows]
            )),
            "T_MM": stats(np.asarray(
                [r["terms"]["T_MM_model_quadratic"] for r in rows]
            )),
            "F": stats(np.asarray([r["terms"]["F_reconstructed"] for r in rows])),
        }

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "phase": "MERGE",
        "status": "COMPLETE",
        "scientific_question": c["project"]["question"],
        "classification": "EXACT_INTERACTION_PRESERVING_TERMS_NUMERICALLY_RECONSTRUCTED",
        "actual_model_initializations_without_likelihood_evaluation": total_model_initializations,
        "actual_new_likelihood_evaluations": total_new_evals,
        "actual_optimizer_evaluations": total_opt,
        "actual_sampling_evaluations": total_sampling,
        "actual_q024_permutations": total_q024,
        "diagnostic_count": len(diagnostics),
        "diagnostics": diagnostics,
        "global_summary": {
            "T_DM_data_model_factorial_coupling": stats(tdm),
            "T_MM_model_quadratic": stats(tmm),
            "F_reconstructed": stats(ff),
            "magnitude_relation_counts": dominance_counts,
            "by_mask": by_mask,
            "by_edge": by_edge,
            "max_abs_Q028_parent_F_closure_error": float(max_parent_error),
            "unique_data_vector_hash_count_across_masks": len({
                lineage_objects[str(m)]["data_vector"]["full_sha256"] for m in MASKS
            }),
            "unique_precision_hash_count_across_masks": len({
                lineage_objects[str(m)]["precision"]["full_sha256"] for m in MASKS
            }),
        },
        "lineage_objects": lineage_objects,
        "common_support": {
            "dimension": EXPECTED_COMMON_DIMENSION,
            "keys_sha256": EXPECTED_COMMON_SHA256,
        },
        "q028_parent": c["parents"]["q028_v8"],
        "provenance": {
            "q027_correct_commit": c["parents"]["q027"]["commit"],
            "q028_correct_execution_head_sha": EXPECTED_Q028_HEAD_SHA,
            "q028_misrecorded_sha_rejected": c["parents"]["q028_v8"]["misrecorded_sha_rejected"],
            "q028_final_artifact": c["parents"]["q028_v8"]["final_artifact"],
            "q028_final_artifact_id": EXPECTED_Q028_ARTIFACT_ID,
            "q028_final_artifact_sha256": EXPECTED_Q028_ARTIFACT_SHA256,
            "q028_authoritative_common_support_sha256": EXPECTED_COMMON_SHA256,
            "q028_misrecorded_common_support_sha256_rejected": SUPERSEDED_MISRECORDED_COMMON_SHA256,
            "q030_v1_failed_run_id": 33961119891,
            "q030_v1_failed_head_sha": "7c7a5baebf50d1fcce1d47b3a55eff7d3bcea738",
            "q030_v2_repair": "COMMON_SUPPORT_HASH_PROVENANCE_CORRECTION_ONLY",
        },
        "interpretation": {
            "T_DM": (
                "EXACT DATA_MODEL_FACTORIAL_COUPLING; NOT AN IDENTIFIED DATA-ONLY "
                "CONTRIBUTION AND NOT PHYSICAL CAUSATION"
            ),
            "T_MM": (
                "EXACT MODEL_QUADRATIC FUNCTIONAL TERM; NOT AN IDENTIFIED "
                "PHYSICAL MODEL CAUSE"
            ),
            "distribution_semantics": (
                "SPECTRUM AND ELL-BAND RESULTS RETAIN UNORDERED WITHIN- AND "
                "CROSS-GROUP COVARIANCE TERMS; THEY ARE NOT INDEPENDENT LIKELIHOODS"
            ),
            "unique_data_model_attribution_claimed": False,
            "cosmology_calibration_attribution_claimed": False,
            "new_physics_claimed": False,
            "shapley_as_identification_used": False,
        },
        "claim_boundaries": c["claim_boundaries"],
        "FINAL_RESULT_GATE": "PROVISIONAL_PENDING_Q030_TESTS",
    }
    write_json(a.output, out)
    print(
        f"Q030_MERGE_GATE=PASS diagnostics=9 "
        f"max_parent_error={max_parent_error:.6g}"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--config",
        default="q030_interaction_preserving_decomposition_v2_config.yml",
    )
    sub = p.add_subparsers(dest="phase", required=True)

    m = sub.add_parser("mask")
    m.add_argument("--mask", type=int, required=True)
    m.add_argument("--q021-dir", required=True)
    m.add_argument("--q022-dir", required=True)
    m.add_argument("--family-dir", required=True)
    m.add_argument("--support-result", required=True)
    m.add_argument("--output", required=True)

    g = sub.add_parser("merge")
    g.add_argument("--mask-dir", required=True)
    g.add_argument("--q028-final", required=True)
    g.add_argument("--output", required=True)
    return p


def main() -> int:
    p = parser()
    a = p.parse_args()
    c = load_cfg(a.config)
    if a.phase == "mask":
        return phase_mask(a, c)
    if a.phase == "merge":
        return phase_merge(a, c)
    raise RuntimeError("PHASE_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
