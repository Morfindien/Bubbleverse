#!/usr/bin/env python3
"""
Bubbleverse Q030 — ORIGINAL-GATE PRECISION AUDIT V1

This is ONE finite numerical precision audit of the already-computed Q030 V2
scientific result.

It does NOT create a new scientific Q and is deliberately NOT named Q030 V4.

Purpose
-------
Determine whether the ORIGINAL frozen Q030 closure gates

    |F_residual - (T_DM + T_MM)| <= 1e-8

and exact spectrum / ell-band group-pair aggregation closure <= 1e-8

can be satisfied from the SAME frozen Q022/Q028/CamSpec numerical objects by
using a better-conditioned but algebraically identical evaluation.

Scientific inputs are immutable:
* Q022 endpoints unchanged.
* Q028 residual states unchanged.
* exact 9915-row support unchanged.
* data vector unchanged.
* precision matrix unchanged.
* model / likelihood / backend unchanged.
* zero new likelihood evaluations.
* zero optimization / sampling / Q024 reruns.

Numerical repair
----------------
V2 evaluated Delta2(x^T P x) by subtracting four large quadratic scalars.
That is algebraically correct but cancellation-prone.

This audit uses the exact factorial expansion for symmetric P:

Let
    x0 = x00
    a  = x10 - x00
    b  = x01 - x00
    c  = x11 - x10 - x01 + x00

Then

Delta2(x^T P x)
 = 2 x0^T P c
 + 2 a^T P b
 + 2 a^T P c
 + 2 b^T P c
 + c^T P c.

No term is defined from F minus another term.
T_DM, T_MM and F_residual are reconstructed independently.

Scalar contractions use np.longdouble accumulation where the runner provides
more precision than float64, with math.fsum fallback. P-actions remain the exact
Q028/Q030 float64 symmetrized precision actions; their linearity residuals are
measured explicitly.

Group-pair decomposition uses the same stable factorial expansion and preserves
unordered within-group and cross-group covariance terms.

A negative result is valid:
the workflow must distinguish AUDIT_EXECUTION_GATE from ORIGINAL_Q030_GATE.
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

import q030_interaction_preserving_decomposition_v2 as q30v2

ROOT = Path(__file__).resolve().parent

Q = "Q030"
RUN = "Q030-ORIGINAL-GATE-PRECISION-AUDIT-V1"
RESULT = "R-Q030-ORIGINAL-GATE-PRECISION-AUDIT-001"

PARENT_V2_RUN = "Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-V2"
PARENT_V2_RESULT = "R-Q030-EDE-INTERACTION-PRESERVING-DECOMPOSITION-002"
PARENT_V2_GITHUB_RUN = 33961469874
PARENT_V2_HEAD_SHA = "c0d01b8cd9ecc533b37cf82e89710595ff9a34a2"

Q028_RUN = 33957937309
Q028_HEAD_SHA = "7f5d35c0725530039162adfa4d71be288e8b4462"

MASKS = (3, 6, 7)
EDGES = ((0, 1), (0, 2), (1, 2))
STATES = ("00", "10", "01", "11")
COMMON_DIM = 9915
COMMON_SHA = "6088165823b7fae224ce51aaef33fdef5a400aefafd1675e454e00c6c1a25a63"

EXPECTED_V2_MASK_SHA256 = {
    3: "993426ef2b63a9197844a9b7526f2e72a162b7470752ba2b7ad21a006c3b3913",
    6: "51220e4ef4ed71f4e65d0337d98554c86a014fba573fe773629ca83ba0744a08",
    7: "e9d6eb8cab66e66599cdf475fe9a22394d9ab4d5365889e75ed0d297fa111968",
}

LD = np.longdouble


def read_json(path: str | Path) -> dict[str, Any]:
    x = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL {path}")
    return x


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def edge_key(sa: int, sb: int) -> str:
    return f"e{int(sa)}{int(sb)}"


def ld_available() -> bool:
    return np.finfo(LD).nmant > np.finfo(np.float64).nmant


def ld_str(x: Any) -> str:
    return np.format_float_scientific(LD(x), precision=24, unique=False, trim="k")


def ext_dot(x: np.ndarray, y: np.ndarray) -> LD:
    """Extended-precision scalar accumulation over frozen float64 operands."""
    a = np.asarray(x, dtype=np.float64)
    b = np.asarray(y, dtype=np.float64)
    if a.shape != b.shape:
        raise RuntimeError(f"DOT_SHAPE_GATE=FAIL {a.shape} != {b.shape}")
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        raise RuntimeError("FINITE_DOT_OPERAND_GATE=FAIL")
    if ld_available():
        return np.sum(a.astype(LD) * b.astype(LD), dtype=LD)
    # Rare platform fallback: correctly-rounded summation of float64 products.
    return LD(math.fsum(float(u) * float(v) for u, v in zip(a, b)))


def ext_sum(values: list[Any]) -> LD:
    if ld_available():
        return np.sum(np.asarray(values, dtype=LD), dtype=LD)
    return LD(math.fsum(float(v) for v in values))


def sym_bilinear(x: np.ndarray, Ax: np.ndarray, y: np.ndarray, Ay: np.ndarray) -> LD:
    """
    Stable scalar for x^T P_sym y.

    Averaging x^T(P y) and y^T(P x) suppresses residual scalar asymmetry while
    preserving the exact Q028/Q030 symmetrized precision semantics.
    """
    return LD("0.5") * (ext_dot(x, Ay) + ext_dot(y, Ax))


def derive_factorial_vectors(states: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    x0 = np.asarray(states["00"], dtype=np.float64)
    a = np.asarray(states["10"], dtype=np.float64) - x0
    b = np.asarray(states["01"], dtype=np.float64) - x0
    c = (
        np.asarray(states["11"], dtype=np.float64)
        - np.asarray(states["10"], dtype=np.float64)
        - np.asarray(states["01"], dtype=np.float64)
        + x0
    )
    return {"x0": x0, "a": a, "b": b, "c": c}


def derive_factorial_actions(actions: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    A0 = np.asarray(actions["00"], dtype=np.float64)
    Aa = np.asarray(actions["10"], dtype=np.float64) - A0
    Ab = np.asarray(actions["01"], dtype=np.float64) - A0
    Ac = (
        np.asarray(actions["11"], dtype=np.float64)
        - np.asarray(actions["10"], dtype=np.float64)
        - np.asarray(actions["01"], dtype=np.float64)
        + A0
    )
    return {"x0": A0, "a": Aa, "b": Ab, "c": Ac}


def stable_factorial_quadratic_from_components(
    comp: Mapping[str, np.ndarray],
    A: Mapping[str, np.ndarray],
) -> tuple[LD, dict[str, LD]]:
    """
    Stable Delta2(x^T P x) from DIRECT P-actions of x0, a, b, c.

    Crucially, P*a/P*b/P*c are not obtained by subtracting large P*x_state
    vectors. They are requested directly from the same frozen precision
    operator, removing a second cancellation channel.
    """
    pieces = {
        "2_x0_P_c": LD(2) * sym_bilinear(comp["x0"], A["x0"], comp["c"], A["c"]),
        "2_a_P_b": LD(2) * sym_bilinear(comp["a"], A["a"], comp["b"], A["b"]),
        "2_a_P_c": LD(2) * sym_bilinear(comp["a"], A["a"], comp["c"], A["c"]),
        "2_b_P_c": LD(2) * sym_bilinear(comp["b"], A["b"], comp["c"], A["c"]),
        "c_P_c": sym_bilinear(comp["c"], A["c"], comp["c"], A["c"]),
    }
    return ext_sum(list(pieces.values())), pieces


def pair_bilinear(
    g: str,
    h: str,
    X: Mapping[str, np.ndarray],
    AX: Mapping[str, np.ndarray],
    Y: Mapping[str, np.ndarray],
    AY: Mapping[str, np.ndarray],
) -> LD:
    if g == h:
        return sym_bilinear(X[g], AX[g], Y[g], AY[g])
    return (
        sym_bilinear(X[g], AX[g], Y[h], AY[h])
        + sym_bilinear(X[h], AX[h], Y[g], AY[g])
    )


def stable_group_distribution(
    ek: str,
    mode: str,
    d: np.ndarray,
    m_comp: Mapping[str, np.ndarray],
    groups: Mapping[str, np.ndarray],
    all_actions: Mapping[str, np.ndarray],
    totals: Mapping[str, LD],
) -> dict[str, Any]:
    names = sorted(groups)

    dgroups: dict[str, np.ndarray] = {}
    C: dict[str, dict[str, np.ndarray]] = {}
    AC: dict[str, dict[str, np.ndarray]] = {}
    for g in names:
        gm = groups[g]
        dgroups[g] = q30v2.masked(d, gm)
        C[g] = {
            k: q30v2.masked(np.asarray(m_comp[k], dtype=np.float64), gm)
            for k in ("x0", "a", "b", "c")
        }
        AC[g] = {
            k: np.asarray(all_actions[f"{ek}|AUDIT|{mode}|{k}|{g}"], dtype=np.float64)
            for k in ("x0", "a", "b", "c")
        }

    pair_rows: dict[str, Any] = {}
    pair_accum: dict[str, list[LD]] = {
        "T_DM_data_model_factorial_coupling": [],
        "T_MM_model_quadratic": [],
        "F_reconstructed": [],
    }

    X0={k:C[k]["x0"] for k in names}; AX0={k:AC[k]["x0"] for k in names}
    XA={k:C[k]["a"] for k in names}; AXA={k:AC[k]["a"] for k in names}
    XB={k:C[k]["b"] for k in names}; AXB={k:AC[k]["b"] for k in names}
    XC={k:C[k]["c"] for k in names}; AXC={k:AC[k]["c"] for k in names}

    for i, g in enumerate(names):
        for h in names[i:]:
            if g == h:
                tdm = LD(-2) * ext_dot(dgroups[g], AC[g]["c"])
            else:
                tdm = LD(-2) * (
                    ext_dot(dgroups[g], AC[h]["c"])
                    + ext_dot(dgroups[h], AC[g]["c"])
                )

            p1 = LD(2) * pair_bilinear(g,h,X0,AX0,XC,AXC)
            p2 = LD(2) * pair_bilinear(g,h,XA,AXA,XB,AXB)
            p3 = LD(2) * pair_bilinear(g,h,XA,AXA,XC,AXC)
            p4 = LD(2) * pair_bilinear(g,h,XB,AXB,XC,AXC)
            p5 = pair_bilinear(g,h,XC,AXC,XC,AXC)
            tmm = ext_sum([p1,p2,p3,p4,p5])
            frec = ext_sum([tdm,tmm])

            pair_accum["T_DM_data_model_factorial_coupling"].append(tdm)
            pair_accum["T_MM_model_quadratic"].append(tmm)
            pair_accum["F_reconstructed"].append(frec)
            pair_rows[f"{g} <-> {h}"] = {
                "T_DM_data_model_factorial_coupling": float(tdm),
                "T_MM_model_quadratic": float(tmm),
                "F_reconstructed": float(frec),
                "extended": {"T_DM":ld_str(tdm),"T_MM":ld_str(tmm),"F":ld_str(frec)},
            }

    sums_ld={k:ext_sum(v) for k,v in pair_accum.items()}
    closure_ld={k:sums_ld[k]-totals[k] for k in sums_ld}

    # Direct-action partition completeness. This measures the exact numerical
    # difference between P applied to the full component and the sum of P
    # applied separately to group-restricted components.
    action_partition_max_abs=0.0
    for k in ("x0","a","b","c"):
        group_sum=np.zeros_like(next(iter(AC.values()))[k])
        for g in names:
            group_sum += AC[g][k]
        full=np.asarray(all_actions[f"{ek}|AUDIT|full|m|{k}"],dtype=np.float64)
        action_partition_max_abs=max(action_partition_max_abs,float(np.max(np.abs(group_sum-full))))

    return {
        "mode": mode,
        "semantics": "STABLE_EXACT_UNORDERED_GROUP_PAIR_FACTORIAL_DECOMPOSITION_WITH_CROSS_GROUP_COVARIANCE_RETAINED; NOT_INDEPENDENT_LIKELIHOODS",
        "groups": names,
        "pairs": pair_rows,
        "sums": {k:float(v) for k,v in sums_ld.items()},
        "sums_extended": {k:ld_str(v) for k,v in sums_ld.items()},
        "closure_error_vs_total": {k:float(v) for k,v in closure_ld.items()},
        "closure_error_vs_total_extended": {k:ld_str(v) for k,v in closure_ld.items()},
        "max_abs_direct_action_partition_residual": action_partition_max_abs,
    }


def load_audit_cfg(path: str | Path) -> dict[str, Any]:
    c = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_RESULT_IDENTITY_GATE=FAIL")
    if float(c["validation"]["original_q029_identity_abs_tol"]) != 1e-8:
        raise RuntimeError("ORIGINAL_IDENTITY_TOLERANCE_MUTATION_GATE=FAIL")
    if float(c["validation"]["original_aggregation_abs_tol"]) != 1e-8:
        raise RuntimeError("ORIGINAL_AGGREGATION_TOLERANCE_MUTATION_GATE=FAIL")
    if float(c["validation"]["delta_m_identity_abs_tol"]) != 1e-11:
        raise RuntimeError("DELTA_M_TOLERANCE_MUTATION_GATE=FAIL")
    if float(c["validation"]["q028_parent_interaction_abs_tol"]) != 2e-4:
        raise RuntimeError("Q028_PARENT_TOLERANCE_MUTATION_GATE=FAIL")
    return c


def phase_mask(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    import q025_fullmf_component_attribution_v2 as q25

    mask = int(a.mask)
    if mask not in MASKS:
        raise RuntimeError("MASK_SCOPE_GATE=FAIL")

    # Freeze the exact parent V2 shard used for comparison.
    v2p = Path(a.v2_mask_result)
    got_v2_sha = sha256_file(v2p)
    if got_v2_sha != EXPECTED_V2_MASK_SHA256[mask]:
        raise RuntimeError(
            f"V2_MASK_IMMUTABILITY_GATE=FAIL mask={mask} got={got_v2_sha}"
        )
    v2 = read_json(v2p)
    if not (
        v2.get("q") == Q
        and v2.get("run_id") == PARENT_V2_RUN
        and v2.get("result_id") == PARENT_V2_RESULT
        and int(v2.get("mask", -1)) == mask
    ):
        raise RuntimeError("V2_PARENT_IDENTITY_GATE=FAIL")

    # Reuse authoritative V2 numerical configuration and helper gates.
    base_cfg = q30v2.load_cfg(ROOT / c["reuse"]["q030_v2_config"])
    families = q30v2.load_mask_families(a.family_dir, mask)
    support = q30v2.load_support(a.support_result, base_cfg)
    common_keys = [tuple(x) for x in support["common_keys"]]
    if len(common_keys) != COMMON_DIM:
        raise RuntimeError("COMMON_DIMENSION_GATE=FAIL")

    first_edge = edge_key(*EDGES[0])
    recipient_keys = [
        tuple(x) for x in families[first_edge]["states"]["00"]["keys"]
    ]
    for ek, fam in families.items():
        for s in STATES:
            if [tuple(x) for x in fam["states"][s]["keys"]] != recipient_keys:
                raise RuntimeError(f"RECIPIENT_ROW_ALIGNMENT_GATE=FAIL {ek}:{s}")

    parent25_cfg = q25.load_cfg(ROOT / base_cfg["reuse"]["q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)
    seed0 = q25.load_q022_endpoint(
        a.q022_dir, a.q021_dir, final22, mask, 0
    )["params"]

    # Model initialization only. No logposterior call.
    model = q25.build_full_model(parent25_cfg, seed0)
    try:
        like = model.likelihood[q30v2.FULL_LIKE]
        d_full = np.asarray(like.data_vector, dtype=np.float64).copy()
        P_raw = np.asarray(like.covinv, dtype=np.float64)

        d = q30v2.project_vector(d_full, recipient_keys, common_keys)
        groupings = {
            "spectrum": q30v2.grouping(common_keys, "spectrum", base_cfg),
            "ell_band": q30v2.grouping(common_keys, "ell_band", base_cfg),
        }

        edge_state: dict[str, Any] = {}
        columns: dict[str, np.ndarray] = {}

        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            fam = families[ek]
            r_states = {
                s: q30v2.project_residual(fam["states"][s], common_keys)
                for s in STATES
            }
            m_states = {s: d - r_states[s] for s in STATES}

            delta_r = (
                r_states["11"] - r_states["10"] - r_states["01"] + r_states["00"]
            )
            delta_m = (
                m_states["11"] - m_states["10"] - m_states["01"] + m_states["00"]
            )
            dm_identity = float(np.max(np.abs(delta_m + delta_r)))
            if dm_identity > float(c["validation"]["delta_m_identity_abs_tol"]):
                raise RuntimeError(
                    f"DELTA_M_EQUALS_MINUS_DELTA_R_GATE=FAIL {ek} {dm_identity}"
                )

            edge_state[ek] = {
                "r_states": r_states,
                "m_states": m_states,
                "delta_m": delta_m,
                "delta_r": delta_r,
                "delta_identity_max_abs": dm_identity,
            }
            q30v2.add_edge_columns(
                columns, ek, d, delta_m, m_states, r_states, groupings
            )

            # Precision-audit columns: direct P-actions of factorial components.
            # This avoids subtracting four large P*x_state vectors.
            m_comp = derive_factorial_vectors(m_states)
            r_comp = derive_factorial_vectors(r_states)
            for k in ("x0", "a", "b", "c"):
                columns[f"{ek}|AUDIT|full|m|{k}"] = m_comp[k]
                columns[f"{ek}|AUDIT|full|r|{k}"] = r_comp[k]
            for mode, groups in groupings.items():
                for g, gm in groups.items():
                    for k in ("x0", "a", "b", "c"):
                        columns[f"{ek}|AUDIT|{mode}|{k}|{g}"] = q30v2.masked(m_comp[k], gm)

        # Exact same Q028 V8 / Q030 V2 symmetrized precision action.
        actions, schur_meta = q30v2.schur_actions(
            P_raw, recipient_keys, common_keys, columns
        )

        diagnostics: dict[str, Any] = {}
        for sa, sb in EDGES:
            ek = edge_key(sa, sb)
            x = edge_state[ek]
            m_states = x["m_states"]
            r_states = x["r_states"]

            m_comp = derive_factorial_vectors(m_states)
            r_comp = derive_factorial_vectors(r_states)
            mA_direct = {
                k: np.asarray(actions[f"{ek}|AUDIT|full|m|{k}"], dtype=np.float64)
                for k in ("x0", "a", "b", "c")
            }
            rA_direct = {
                k: np.asarray(actions[f"{ek}|AUDIT|full|r|{k}"], dtype=np.float64)
                for k in ("x0", "a", "b", "c")
            }

            # Independent stable reconstructions from DIRECT factorial actions.
            tmm, tmm_pieces = stable_factorial_quadratic_from_components(m_comp, mA_direct)
            fres, fres_pieces = stable_factorial_quadratic_from_components(r_comp, rA_direct)
            tdm = LD(-2) * ext_dot(d, mA_direct["c"])
            frec = ext_sum([tdm, tmm])
            identity_error = ext_sum([frec, -fres])

            # Compare direct P*c with the cancellation-prone state-action
            # combination only as a diagnostic; it is not used to force PASS.
            m_state_actions = {
                s: np.asarray(actions[f"{ek}|full|m|{s}"], dtype=np.float64)
                for s in STATES
            }
            mA_combo = derive_factorial_actions(m_state_actions)
            action_delta = mA_combo["c"] - mA_direct["c"]
            action_linearity_max = float(np.max(np.abs(action_delta)))
            action_linearity_l2 = float(np.linalg.norm(action_delta))
            tdm_combo = LD(-2) * ext_dot(d, mA_combo["c"])
            tdm_action_method_spread = tdm_combo - tdm

            totals = {
                "T_DM_data_model_factorial_coupling": tdm,
                "T_MM_model_quadratic": tmm,
                "F_reconstructed": frec,
            }

            distributions = {
                mode: stable_group_distribution(
                    ek, mode, d, m_comp, groups, actions, totals
                )
                for mode, groups in groupings.items()
            }

            v2d = v2["diagnostics"][ek]
            v2_terms = v2d["terms"]

            diagnostics[ek] = {
                "q": Q,
                "mask": mask,
                "edge": ek,
                "method": (
                    "STABLE_FACTORIAL_BILINEAR_EXPANSION_WITH_EXTENDED_SCALAR_"
                    "ACCUMULATION_OVER_FROZEN_FLOAT64_Q028_PRECISION_ACTIONS"
                ),
                "terms": {k: float(v) for k, v in totals.items()},
                "terms_extended": {k: ld_str(v) for k, v in totals.items()},
                "F_direct_from_residual_factorial_stable": float(fres),
                "F_direct_from_residual_factorial_stable_extended": ld_str(fres),
                "Q029_identity_closure_error": float(identity_error),
                "Q029_identity_closure_error_extended": ld_str(identity_error),
                "delta2m_equals_minus_delta2r_max_abs_error": x[
                    "delta_identity_max_abs"
                ],
                "T_DM_state_action_combination": float(tdm_combo),
                "T_DM_direct_vs_state_action_spread": float(
                    tdm_action_method_spread
                ),
                "P_delta_action_linearity_max_abs": action_linearity_max,
                "P_delta_action_linearity_l2": action_linearity_l2,
                "T_MM_factorial_pieces": {
                    k: float(v) for k, v in tmm_pieces.items()
                },
                "F_residual_factorial_pieces": {
                    k: float(v) for k, v in fres_pieces.items()
                },
                "distributions": distributions,
                "parent_v2": {
                    "terms": v2_terms,
                    "Q029_identity_closure_error": v2d[
                        "Q029_identity_closure_error"
                    ],
                    "distribution_closure_errors": {
                        mode: v2d["distributions"][mode][
                            "closure_error_vs_total"
                        ]
                        for mode in ("spectrum", "ell_band")
                    },
                },
                "stable_minus_v2": {
                    "T_DM": float(tdm)
                    - float(
                        v2_terms["T_DM_data_model_factorial_coupling"]
                    ),
                    "T_MM": float(tmm)
                    - float(v2_terms["T_MM_model_quadratic"]),
                    "F": float(frec) - float(v2_terms["F_reconstructed"]),
                },
                "interpretation_boundary": {
                    "T_DM_is_data_only_contribution": False,
                    "T_MM_is_physical_model_cause": False,
                    "unique_data_model_attribution": False,
                    "unique_cosmology_calibration_attribution": False,
                    "physical_causality_claimed": False,
                    "new_physics_claimed": False,
                },
            }

        out = {
            "q": Q,
            "run_id": RUN,
            "result_id": RESULT,
            "phase": "MASK_PRECISION_AUDIT",
            "status": "COMPLETE",
            "mask": mask,
            "parent_v2": {
                "run_id": PARENT_V2_RUN,
                "result_id": PARENT_V2_RESULT,
                "github_run_id": PARENT_V2_GITHUB_RUN,
                "head_sha": PARENT_V2_HEAD_SHA,
                "mask_json_sha256": got_v2_sha,
            },
            "common_support": {
                "dimension": len(common_keys),
                "keys_sha256": support["common_keys_sha256"],
            },
            "precision": {
                "shape": list(P_raw.shape),
                "sha256": q30v2.sha256_array(P_raw),
                "schur": schur_meta,
            },
            "data_vector": {
                "full_sha256": q30v2.sha256_array(d_full),
                "common_sha256": q30v2.sha256_array(d),
            },
            "arithmetic": {
                "numpy_version": np.__version__,
                "float64_eps": float(np.finfo(np.float64).eps),
                "float64_mantissa_bits": int(np.finfo(np.float64).nmant),
                "longdouble_eps": float(np.finfo(LD).eps),
                "longdouble_mantissa_bits": int(np.finfo(LD).nmant),
                "longdouble_has_more_precision_than_float64": ld_available(),
                "scalar_accumulation": (
                    "NUMPY_LONGDOUBLE_PRODUCT_AND_SUM"
                    if ld_available()
                    else "MATH_FSUM_OF_FLOAT64_PRODUCTS"
                ),
            },
            "execution_counts": {
                "model_initializations_without_likelihood_evaluation": 1,
                "new_likelihood_evaluations": 0,
                "optimizer_evaluations": 0,
                "sampling_evaluations": 0,
                "q024_permutations_evaluated": 0,
            },
            "diagnostic_count": len(diagnostics),
            "diagnostics": diagnostics,
        }
        write_json(a.output, out)
        print(
            f"Q030_PRECISION_AUDIT_MASK_GATE=PASS mask={mask} "
            f"diagnostics={len(diagnostics)}"
        )
    finally:
        try:
            model.close()
        except Exception:
            pass

    return 0


def phase_merge(a: argparse.Namespace, c: Mapping[str, Any]) -> int:
    mask_dir = Path(a.mask_dir)
    shards: dict[int, dict[str, Any]] = {}
    diagnostics: list[dict[str, Any]] = []

    for mask in MASKS:
        p = mask_dir / f"q030_precision_audit_m{mask}.json"
        if not p.exists():
            raise RuntimeError(f"AUDIT_MASK_MISSING_GATE=FAIL mask={mask}")
        x = read_json(p)
        if not (
            x.get("q") == Q
            and x.get("run_id") == RUN
            and x.get("result_id") == RESULT
            and x.get("status") == "COMPLETE"
            and int(x.get("mask", -1)) == mask
            and int(x.get("diagnostic_count", -1)) == 3
        ):
            raise RuntimeError(f"AUDIT_MASK_IDENTITY_GATE=FAIL mask={mask}")
        shards[mask] = x
        for ek in ("e01", "e02", "e12"):
            diagnostics.append(dict(x["diagnostics"][ek]))

    if len(diagnostics) != 9:
        raise RuntimeError("NINE_DIAGNOSTIC_COMPLETENESS_GATE=FAIL")

    q28 = read_json(a.q028_final)
    if not (
        q28.get("q") == "Q028"
        and q28.get("FINAL_RESULT_GATE") == "PASS"
        and int(q28["common_support"]["dimension"]) == COMMON_DIM
        and q28["common_support"]["keys_sha256"] == COMMON_SHA
    ):
        raise RuntimeError("Q028_PARENT_IDENTITY_GATE=FAIL")

    q28_diag = q28["diagonal_support_effects"]
    max_parent = 0.0
    for d in diagnostics:
        parent = float(
            q28_diag[str(int(d["mask"]))][d["edge"]][
                "common_support_marginal_pair_interaction"
            ]
        )
        err = float(d["terms"]["F_reconstructed"]) - parent
        d["Q028_parent_common_support_F"] = parent
        d["Q028_parent_closure_error"] = err
        max_parent = max(max_parent, abs(err))

    id_tol = float(c["validation"]["original_q029_identity_abs_tol"])
    agg_tol = float(c["validation"]["original_aggregation_abs_tol"])
    dm_tol = float(c["validation"]["delta_m_identity_abs_tol"])
    parent_tol = float(c["validation"]["q028_parent_interaction_abs_tol"])

    max_identity = max(
        abs(float(d["Q029_identity_closure_error"])) for d in diagnostics
    )
    max_dm = max(
        abs(float(d["delta2m_equals_minus_delta2r_max_abs_error"]))
        for d in diagnostics
    )

    agg_records = []
    max_partition_action = 0.0
    for d in diagnostics:
        for mode, dist in d["distributions"].items():
            max_partition_action = max(
                max_partition_action,
                float(dist["max_abs_direct_action_partition_residual"]),
            )
            for term, err in dist["closure_error_vs_total"].items():
                agg_records.append(
                    {
                        "mask": int(d["mask"]),
                        "edge": d["edge"],
                        "mode": mode,
                        "term": term,
                        "abs_error": abs(float(err)),
                        "signed_error": float(err),
                    }
                )
    worst_agg = max(agg_records, key=lambda x: x["abs_error"])
    max_agg = float(worst_agg["abs_error"])

    original_gate_pass = (
        max_identity <= id_tol
        and max_agg <= agg_tol
        and max_dm <= dm_tol
        and max_parent <= parent_tol
    )

    # Numerical method diagnostics: these do not replace the frozen gates.
    max_delta_action_linearity = max(
        abs(float(d["P_delta_action_linearity_max_abs"]))
        for d in diagnostics
    )
    max_tdm_action_spread = max(
        abs(float(d["T_DM_direct_vs_state_action_spread"]))
        for d in diagnostics
    )

    if original_gate_pass:
        outcome = "ORIGINAL_Q030_GATE_PASS_WITH_STABLE_ARITHMETIC"
        remaining = []
    else:
        outcome = "ORIGINAL_Q030_GATE_FAIL_AFTER_ONE_STABLE_PRECISION_AUDIT"
        remaining = [
            (
                "The original 1e-8 contract is not satisfied by the audited "
                "stable evaluation of the same frozen float64 source objects. "
                "Do not relax the threshold again. Return this negative result "
                "to Result Ingestion for final classification."
            )
        ]

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "phase": "FINAL_PRECISION_AUDIT",
        "status": "COMPLETE",
        "audit_scope": "ONE_AND_ONLY_ONE_ORIGINAL_GATE_PRECISION_AUDIT",
        "scientific_question": c["project"]["question"],
        "parent_v2": {
            "run_id": PARENT_V2_RUN,
            "result_id": PARENT_V2_RESULT,
            "github_run_id": PARENT_V2_GITHUB_RUN,
            "head_sha": PARENT_V2_HEAD_SHA,
        },
        "q028_parent": {
            "github_run_id": Q028_RUN,
            "head_sha": Q028_HEAD_SHA,
            "common_dimension": COMMON_DIM,
            "common_support_sha256": COMMON_SHA,
        },
        "execution_counts": {
            "mask_jobs": 3,
            "model_initializations_without_likelihood_evaluation": 3,
            "new_likelihood_evaluations": 0,
            "optimizer_evaluations": 0,
            "sampling_evaluations": 0,
            "q024_permutations": 0,
        },
        "frozen_original_gates": {
            "Q029_identity_abs_tol": id_tol,
            "aggregation_abs_tol": agg_tol,
            "delta_m_identity_abs_tol": dm_tol,
            "Q028_parent_abs_tol": parent_tol,
        },
        "audit_results": {
            "max_abs_Q029_identity_closure_error": max_identity,
            "max_abs_group_pair_aggregation_closure_error": max_agg,
            "worst_group_pair_aggregation": worst_agg,
            "max_abs_delta2m_plus_delta2r": max_dm,
            "max_abs_Q028_parent_closure_error": max_parent,
            "max_abs_P_delta_action_linearity_residual": max_delta_action_linearity,
            "max_abs_T_DM_direct_vs_state_action_spread": max_tdm_action_spread,
            "max_abs_partitioned_state_action_residual": max_partition_action,
        },
        "ORIGINAL_Q030_GATE": "PASS" if original_gate_pass else "FAIL",
        "AUDIT_OUTCOME": outcome,
        "AUDIT_EXECUTION_GATE": "PROVISIONAL_PENDING_TESTS",
        "diagnostic_count": 9,
        "diagnostics": diagnostics,
        "remaining_uncertainties": remaining,
        "stop_directive": (
            "STOP_AFTER_THIS_AUDIT. DO_NOT CREATE A TOLERANCE-RELAXATION LOOP. "
            "RETURN TO RESULT INGESTION & ROUTING ENGINE."
        ),
        "interpretation_boundaries": {
            "scientific_inputs_changed": False,
            "likelihood_evaluated": False,
            "optimization_performed": False,
            "sampling_performed": False,
            "q024_rerun": False,
            "T_DM_is_data_only_contribution": False,
            "T_MM_is_physical_model_cause": False,
            "causal_allocation_performed": False,
            "new_physics_claimed": False,
        },
    }
    write_json(a.output, out)
    print(
        "Q030_PRECISION_AUDIT_MERGE_GATE=PASS "
        f"ORIGINAL_Q030_GATE={out['ORIGINAL_Q030_GATE']} "
        f"max_identity={max_identity:.12g} max_agg={max_agg:.12g}"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config", default="q030_original_gate_precision_audit_v1_config.yml"
    )
    sub = ap.add_subparsers(dest="phase", required=True)

    pm = sub.add_parser("mask")
    pm.add_argument("--mask", type=int, required=True)
    pm.add_argument("--q021-dir", required=True)
    pm.add_argument("--q022-dir", required=True)
    pm.add_argument("--family-dir", required=True)
    pm.add_argument("--support-result", required=True)
    pm.add_argument("--v2-mask-result", required=True)
    pm.add_argument("--output", required=True)

    pg = sub.add_parser("merge")
    pg.add_argument("--mask-dir", required=True)
    pg.add_argument("--q028-final", required=True)
    pg.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_audit_cfg(a.config)
    if a.phase == "mask":
        return phase_mask(a, c)
    return phase_merge(a, c)


if __name__ == "__main__":
    raise SystemExit(main())
