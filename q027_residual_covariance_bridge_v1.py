#!/usr/bin/env python3
"""
Bubbleverse Q027 — residual / inverse-covariance bridge for the Q026
omega_cdm x A_planck compensation.

Scientific contract
-------------------
CURRENT Q: Q027

Question:
Can the mask-6 A_planck–omega_cdm compensation identified in Q026 be traced,
within the same frozen CamSpec construction, to specific changes in the residual
vector and inverse-covariance weighting of the TT 143x143, 143x217, and 217x217
ell=600–999 blocks, or does the effect remain a distributed consequence of
broader mask-sensitive data-model geometry?

Design:
- Reuse authoritative Q022 endpoints through Q025 V2 loaders.
- Reuse Q017's exact CamSpec residual/covariance decomposition.
- Reuse Q026's omega_cdm x A_planck finite-switch definition.
- For every Q022 edge in masks 3, 6, 7 evaluate exactly four fixed vectors:
    00: endpoint A
    10: omega_cdm switched A->B
    01: A_planck switched A->B
    11: omega_cdm + A_planck switched A->B
  = 4 * 9 = 36 fixed-vector likelihood evaluations.
- No optimization, sampling, new endpoints, Q024 permutation rerun, or basin search.
- Preserve signed covariance terms and cancellation.

Key mathematical distinction:
Within one frozen CamSpec mask, covinv P is a property of the likelihood
construction and must remain unchanged across the four parameter switches.
Therefore parameter-switch effects arise from changes in the residual family r,
while P controls how those residual changes are weighted/coupled. Q027 verifies
that invariance by hashing P at all four states and then measures:
  d2 r  = r11 - r10 - r01 + r00
  d2 Pr = (Pr)11 - (Pr)10 - (Pr)01 + (Pr)00
  d2 c  = [r_i(Pr)_i]11 - ... + [r_i(Pr)_i]00
plus exact finite contrasts of Q017 covariance block-pair terms.

These are technical likelihood diagnostics, not physical causal derivatives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q027"
RUN = "Q027-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-V1"
RESULT = "R-Q027-EDE-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-001"
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
MASKS = (3, 6, 7)
EDGES = ((0, 1), (0, 2), (1, 2))
OMEGA = "omega_cdm"
APL = "A_planck"
PAIR_KEY = "omega_cdm__x__A_planck"


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, default=_json_default) + "\n",
                 encoding="utf-8")


def _json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return str(x)


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
    if tuple(tuple(map(int, x)) for x in c["execution"]["edges"]) != EDGES:
        raise RuntimeError("EDGE_SCOPE_GATE=FAIL")
    for k in ("no_optimization", "no_sampling", "no_new_endpoints",
              "no_q024_permutation_rerun", "preserve_signed_covariance_terms"):
        if c["rules"].get(k) is not True:
            raise RuntimeError(f"{k.upper()}_GATE=FAIL")
    return c


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_GATE=FAIL {path}")
    return d


def switch(a: Mapping[str, float], b: Mapping[str, float], names) -> dict[str, float]:
    out = {k: float(v) for k, v in a.items()}
    for n in names:
        out[n] = float(b[n])
    return out


def logpost_value(lp: Any) -> float:
    x = getattr(lp, "logpost", lp)
    if not finite(x):
        raise RuntimeError("FINITE_LOGPOST_GATE=FAIL")
    return float(x)


def norm_spec(s: str) -> str:
    return str(s).lower().replace(" ", "").replace("×", "x").replace("_", "")


def precision_hash(model: Any) -> tuple[str, list[int]]:
    like = model.likelihood[FULL_LIKE]
    P = np.ascontiguousarray(np.asarray(like.covinv, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(P.shape).encode("ascii"))
    h.update(P.tobytes())
    return h.hexdigest(), list(P.shape)


def state_for_vector(model: Any, values: Mapping[str, float], c: Mapping[str, Any]) -> dict[str, Any]:
    import q025_fullmf_component_attribution_v2 as q25
    import q017_planck_direction_localization_v1 as q17

    lp = model.logposterior(dict(values))
    logpost = logpost_value(lp)

    cosmology = {p: float(values[p]) for p in q25.PARAM_GROUPS["cosmology"]}
    cosmology.update({p: float(values[p]) for p in q25.PARAM_GROUPS["primordial"]})
    nuisance = {
        p: float(values[p])
        for g in ("shared_nuisance", "foreground")
        for p in q25.PARAM_GROUPS[g]
    }
    expanded = q17.expanded_values(model, cosmology, nuisance)
    q17_cfg = {"decomposition": {"ell_bands": c["decomposition"]["ell_bands"]}}
    detailed = q17.detailed_planck_state(model, expanded, q17_cfg)
    if not isinstance(detailed.get("rows"), list) or not detailed["rows"]:
        raise RuntimeError("Q017_POINTWISE_ROWS_GATE=FAIL")
    ph, pshape = precision_hash(model)
    return {
        "objective_minus2logpost": -2.0 * logpost,
        "highl_covariance_chi2": float(detailed["chi2"]),
        "rows": detailed["rows"],
        "covariance_block_pair_terms": detailed["covariance_block_pair_terms"],
        "precision_sha256": ph,
        "precision_shape": pshape,
    }


def contrast(v00: float, v10: float, v01: float, v11: float) -> float:
    return float(v11) - float(v10) - float(v01) + float(v00)


def row_key(r: Mapping[str, Any]) -> tuple[str, str, int, str]:
    return (str(r["observable"]), str(r["spectrum"]), int(r["ell"]), str(r["band"]))


def align_rows(states: Mapping[str, Mapping[str, Any]]) -> list[tuple[dict[str, Any], ...]]:
    order = ("00", "10", "01", "11")
    base = states["00"]["rows"]
    out = []
    for i in range(len(base)):
        rr = tuple(states[s]["rows"][i] for s in order)
        keys = [row_key(x) for x in rr]
        if len(set(keys)) != 1:
            raise RuntimeError(f"ROW_ALIGNMENT_GATE=FAIL index={i} keys={keys}")
        out.append(rr)
    if any(len(states[s]["rows"]) != len(base) for s in order):
        raise RuntimeError("ROW_LENGTH_GATE=FAIL")
    return out


def target_row(r: Mapping[str, Any], c: Mapping[str, Any]) -> bool:
    if str(r["observable"]).upper() != "TT":
        return False
    if norm_spec(r["spectrum"]) not in {norm_spec(x) for x in c["target"]["spectra"]}:
        return False
    ell = int(r["ell"])
    return int(c["target"]["ell_min"]) <= ell <= int(c["target"]["ell_max"])


def add(m: dict[str, float], k: str, v: float) -> None:
    m[k] = m.get(k, 0.0) + float(v)


def median(vals) -> float:
    a = sorted(float(x) for x in vals)
    if not a:
        return float("nan")
    n = len(a)
    return a[n // 2] if n % 2 else 0.5 * (a[n // 2 - 1] + a[n // 2])


def summarize_edge(states: Mapping[str, Mapping[str, Any]], c: Mapping[str, Any]) -> dict[str, Any]:
    aligned = align_rows(states)
    rows_out = []
    all_abs_c = 0.0
    target_abs_c = 0.0
    all_signed_c = 0.0
    target_signed_c = 0.0
    all_r2 = 0.0
    target_r2 = 0.0
    all_z2 = 0.0
    target_z2 = 0.0
    by_spectrum: dict[str, dict[str, float]] = {}

    target_groups = set()

    for r00, r10, r01, r11 in aligned:
        dr = contrast(r00["residual"], r10["residual"], r01["residual"], r11["residual"])
        dz = contrast(r00["precision_weighted_residual"],
                      r10["precision_weighted_residual"],
                      r01["precision_weighted_residual"],
                      r11["precision_weighted_residual"])
        dc = contrast(r00["signed_fullcov_contribution"],
                      r10["signed_fullcov_contribution"],
                      r01["signed_fullcov_contribution"],
                      r11["signed_fullcov_contribution"])
        is_target = target_row(r00, c)
        spec = str(r00["spectrum"])
        all_abs_c += abs(dc)
        all_signed_c += dc
        all_r2 += dr * dr
        all_z2 += dz * dz
        d = by_spectrum.setdefault(spec, {
            "signed_pointwise_pair_contrast": 0.0,
            "absolute_pointwise_pair_contrast": 0.0,
            "residual_pair_contrast_l2_sq": 0.0,
            "weighted_residual_pair_contrast_l2_sq": 0.0,
        })
        d["signed_pointwise_pair_contrast"] += dc
        d["absolute_pointwise_pair_contrast"] += abs(dc)
        d["residual_pair_contrast_l2_sq"] += dr * dr
        d["weighted_residual_pair_contrast_l2_sq"] += dz * dz
        if is_target:
            target_abs_c += abs(dc)
            target_signed_c += dc
            target_r2 += dr * dr
            target_z2 += dz * dz
            target_groups.add(f'{r00["observable"]}|{r00["spectrum"]}|{r00["band"]}')
        if is_target or bool(c["output"].get("store_all_pointwise_rows", False)):
            rows_out.append({
                "index": int(r00["index"]),
                "observable": str(r00["observable"]),
                "spectrum": spec,
                "ell": int(r00["ell"]),
                "band": str(r00["band"]),
                "target": is_target,
                "residual_pair_contrast": dr,
                "precision_weighted_residual_pair_contrast": dz,
                "signed_fullcov_pointwise_pair_contrast": dc,
            })

    pair_keys = set(states["00"]["covariance_block_pair_terms"])
    if not all(set(states[s]["covariance_block_pair_terms"]) == pair_keys for s in ("10", "01", "11")):
        raise RuntimeError("COVARIANCE_PAIR_KEY_ALIGNMENT_GATE=FAIL")

    cov_parts = {
        "target_target_signed": 0.0,
        "target_outside_signed": 0.0,
        "outside_outside_signed": 0.0,
        "target_target_absolute": 0.0,
        "target_outside_absolute": 0.0,
        "outside_outside_absolute": 0.0,
    }
    pair_contrasts = {}
    for k in sorted(pair_keys):
        v = contrast(
            states["00"]["covariance_block_pair_terms"][k],
            states["10"]["covariance_block_pair_terms"][k],
            states["01"]["covariance_block_pair_terms"][k],
            states["11"]["covariance_block_pair_terms"][k],
        )
        pair_contrasts[k] = v
        try:
            g, h = k.split(" <-> ", 1)
        except ValueError:
            raise RuntimeError(f"COVARIANCE_PAIR_KEY_PARSE_GATE=FAIL key={k}")
        nt = int(g in target_groups) + int(h in target_groups)
        if nt == 2:
            part = "target_target"
        elif nt == 1:
            part = "target_outside"
        else:
            part = "outside_outside"
        cov_parts[f"{part}_signed"] += v
        cov_parts[f"{part}_absolute"] += abs(v)

    p_hashes = {states[s]["precision_sha256"] for s in ("00", "10", "01", "11")}
    p_shapes = {tuple(states[s]["precision_shape"]) for s in ("00", "10", "01", "11")}
    precision_fixed = len(p_hashes) == 1 and len(p_shapes) == 1

    objective_pair = contrast(
        states["00"]["objective_minus2logpost"],
        states["10"]["objective_minus2logpost"],
        states["01"]["objective_minus2logpost"],
        states["11"]["objective_minus2logpost"],
    )
    highl_pair = contrast(
        states["00"]["highl_covariance_chi2"],
        states["10"]["highl_covariance_chi2"],
        states["01"]["highl_covariance_chi2"],
        states["11"]["highl_covariance_chi2"],
    )
    cov_pair_sum = sum(pair_contrasts.values())
    if abs(cov_pair_sum - highl_pair) > float(c["validation"]["covariance_pair_closure_abs_tol"]):
        raise RuntimeError(
            f"COVARIANCE_PAIR_CONTRAST_CLOSURE_GATE=FAIL pair_sum={cov_pair_sum} highl={highl_pair}"
        )

    return {
        "precision_fixed_across_four_parameter_states": precision_fixed,
        "precision_sha256": sorted(p_hashes),
        "precision_shape": [list(x) for x in sorted(p_shapes)],
        "objective_pair_interaction": objective_pair,
        "highl_covariance_pair_interaction": highl_pair,
        "objective_minus_highl_bridge": objective_pair - highl_pair,
        "target_tt_ell600_999": {
            "spectra": list(c["target"]["spectra"]),
            "ell_min": int(c["target"]["ell_min"]),
            "ell_max": int(c["target"]["ell_max"]),
            "target_group_labels": sorted(target_groups),
            "signed_pointwise_pair_contrast": target_signed_c,
            "absolute_pointwise_pair_contrast": target_abs_c,
            "absolute_share_of_all_pointwise_pair_contrast":
                (target_abs_c / all_abs_c if all_abs_c > 0 else 0.0),
            "residual_pair_contrast_l2_share":
                (target_r2 / all_r2 if all_r2 > 0 else 0.0),
            "precision_weighted_residual_pair_contrast_l2_share":
                (target_z2 / all_z2 if all_z2 > 0 else 0.0),
        },
        "all_rows": {
            "signed_pointwise_pair_contrast": all_signed_c,
            "absolute_pointwise_pair_contrast": all_abs_c,
            "residual_pair_contrast_l2_sq": all_r2,
            "precision_weighted_residual_pair_contrast_l2_sq": all_z2,
        },
        "by_spectrum": by_spectrum,
        "covariance_pair_interaction_partition": cov_parts,
        "covariance_block_pair_interaction_contrasts": pair_contrasts,
        "pointwise_pair_contrasts": rows_out,
    }


def classify(diag: Mapping[str, Any], c: Mapping[str, Any]) -> dict[str, Any]:
    mask_rows = {m: [v for v in diag.values() if int(v["mask"]) == m] for m in MASKS}
    med_abs_share = {
        str(m): median([
            r["decomposition"]["target_tt_ell600_999"]["absolute_share_of_all_pointwise_pair_contrast"]
            for r in mask_rows[m]
        ])
        for m in MASKS
    }
    med_r_share = {
        str(m): median([
            r["decomposition"]["target_tt_ell600_999"]["residual_pair_contrast_l2_share"]
            for r in mask_rows[m]
        ])
        for m in MASKS
    }
    med_z_share = {
        str(m): median([
            r["decomposition"]["target_tt_ell600_999"]["precision_weighted_residual_pair_contrast_l2_share"]
            for r in mask_rows[m]
        ])
        for m in MASKS
    }
    all_fixed = all(
        r["decomposition"]["precision_fixed_across_four_parameter_states"]
        for r in diag.values()
    )
    per_mask_hashes = {}
    for m in MASKS:
        hs = set()
        for r in mask_rows[m]:
            hs.update(r["decomposition"]["precision_sha256"])
        per_mask_hashes[str(m)] = sorted(hs)
    cross_mask_precision_distinct = len({
        tuple(per_mask_hashes[str(m)]) for m in MASKS
    }) > 1

    m6 = med_abs_share["6"]
    threshold = float(c["classification"]["target_absolute_share_threshold"])
    margin = float(c["classification"]["mask6_control_margin"])
    control = max(med_abs_share["3"], med_abs_share["7"])
    if m6 >= threshold and m6 >= control + margin:
        spatial = "MASK6_TT600_999_TRIAD_CONCENTRATED"
    elif m6 < threshold:
        spatial = "DISTRIBUTED_BEYOND_TT600_999_TRIAD"
    else:
        spatial = "MIXED_OR_WEAKLY_LOCALIZED"

    if all_fixed:
        within_mask = "RESIDUAL_CHANGE_UNDER_FIXED_INVERSE_COVARIANCE"
    else:
        within_mask = "PRECISION_INVARIANCE_GATE_FAILED"

    if all_fixed and cross_mask_precision_distinct:
        cross_mask = (
            "MASK_SPECIFIC_PRECISION_PRESENT; RESIDUAL_VS_PRECISION CAUSE NOT "
            "UNIQUELY IDENTIFIABLE WITHOUT A COUNTERFACTUAL COMMON-SUPPORT PRECISION SWAP"
        )
    elif all_fixed:
        cross_mask = "NO_CROSS_MASK_PRECISION_DIFFERENCE_DETECTED_BY_HASH; RESIDUAL_GEOMETRY_DOMINATES"
    else:
        cross_mask = "UNRESOLVED"

    return {
        "median_target_absolute_pointwise_share_by_mask": med_abs_share,
        "median_target_residual_l2_share_by_mask": med_r_share,
        "median_target_weighted_residual_l2_share_by_mask": med_z_share,
        "precision_hashes_by_mask": per_mask_hashes,
        "precision_fixed_within_parameter_switches": all_fixed,
        "cross_mask_precision_distinct": cross_mask_precision_distinct,
        "within_mask_mechanism": within_mask,
        "cross_mask_identifiability": cross_mask,
        "spatial_localization": spatial,
        "classification_thresholds": c["classification"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q027_residual_covariance_bridge_v1_config.yml")
    ap.add_argument("--q021-dir", required=True)
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--q025-result", required=True)
    ap.add_argument("--q026-result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    c = load_cfg(a.config)
    q025 = read_json(a.q025_result)
    q026 = read_json(a.q026_result)
    if q025.get("q") != "Q025" or q025.get("result_id") != c["parents"]["q025_result_id"] \
       or q025.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("Q025_PARENT_GATE=FAIL")
    if q026.get("q") != "Q026" or q026.get("result_id") != c["parents"]["q026_result_id"] \
       or q026.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("Q026_PARENT_GATE=FAIL")

    import q025_fullmf_component_attribution_v2 as q25
    parent25 = q25.load_cfg(ROOT / c["parent_q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)

    diagnostics = {}
    eval_count = 0
    parent_match_diffs = []

    for mask in MASKS:
        endpoints = {
            s: q25.load_q022_endpoint(a.q022_dir, a.q021_dir, final22, mask, s)
            for s in (0, 1, 2)
        }
        for sa, sb in EDGES:
            key = f"m{mask}_e{sa}{sb}"
            A = endpoints[sa]["params"]
            B = endpoints[sb]["params"]
            model = q25.build_full_model(parent25, A)

            vectors = {
                "00": dict(A),
                "10": switch(A, B, [OMEGA]),
                "01": switch(A, B, [APL]),
                "11": switch(A, B, [OMEGA, APL]),
            }
            states = {}
            for sid in ("00", "10", "01", "11"):
                states[sid] = state_for_vector(model, vectors[sid], c)
                eval_count += 1

            dec = summarize_edge(states, c)
            pdiag = q026.get("diagnostics", {}).get(key, {})
            parent_pair = pdiag.get("cosmology_x_shared_nuisance_pair_interactions", {}).get(PAIR_KEY)
            if not finite(parent_pair):
                raise RuntimeError(f"Q026_PARENT_PAIR_GATE=FAIL key={key}")
            diff = dec["objective_pair_interaction"] - float(parent_pair)
            parent_match_diffs.append(abs(diff))

            diagnostics[key] = {
                "mask": mask,
                "edge": [sa, sb],
                "q022_endpoint_parent": {
                    "a": endpoints[sa]["parent_record"],
                    "b": endpoints[sb]["parent_record"],
                },
                "q026_parent_pair_interaction": float(parent_pair),
                "q027_recomputed_objective_pair_interaction": dec["objective_pair_interaction"],
                "q026_parent_reproduction_difference": diff,
                "decomposition": dec,
                "interpretation":
                    "FIXED_VECTOR_RESIDUAL_AND_PRECISION_WEIGHTING_DIAGNOSTIC_NONCAUSAL",
            }

    expected = int(c["execution"]["total_expected_likelihood_evaluations"])
    if eval_count != expected:
        raise RuntimeError(f"EVALUATION_COUNT_GATE=FAIL actual={eval_count} expected={expected}")

    tol = float(c["validation"]["q026_pair_reproduction_abs_tol"])
    parent_repro_gate = max(parent_match_diffs) <= tol if parent_match_diffs else False
    summary = classify(diagnostics, c)

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
            "q025_parent": c["parents"]["q025_result_id"],
            "q026_parent": c["parents"]["q026_result_id"],
        },
        "diagnostics": diagnostics,
        "cross_mask_summary": summary,
        "parent_reproduction": {
            "q026_omega_cdm_x_A_planck_pair_gate": parent_repro_gate,
            "max_abs_difference": max(parent_match_diffs) if parent_match_diffs else None,
            "tolerance": tol,
        },
        "claim_boundaries": {
            "physical_causality_claimed": False,
            "calibration_failure_proven": False,
            "instrumental_systematic_proven": False,
            "foreground_systematic_proven": False,
            "independent_observational_evidence_claimed": False,
            "counterfactual_cross_mask_precision_swap_performed": False,
        },
        "journal_preservation": {
            "q019_preserved": True,
            "q020_preserved": True,
            "q021_preserved": True,
            "q022_preserved": True,
            "q023_preserved": True,
            "q024_preserved": True,
            "q025_preserved": True,
            "q026_preserved": True,
        },
        "stop_condition": (
            "Q027 completes if all mandatory gates pass and the result establishes "
            "(a) whether P is fixed across the four parameter states, "
            "(b) how the omega_cdm x A_planck residual/Pr/contribution contrasts "
            "localize to TT 143x143/143x217/217x217 ell=600-999, and "
            "(c) whether the remaining cross-mask residual-vs-precision attribution "
            "is identifiable under this decomposition."
        ),
    }
    write_json(a.output, out)
    print(json.dumps(out, indent=2, sort_keys=True, default=_json_default))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
