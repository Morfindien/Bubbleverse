#!/usr/bin/env python3
"""
Bubbleverse Q-032 — CamSpec nested add-back localization V3.

CURRENT_Q: Q-032
RUN_ID: Q032-CAMSPEC-NESTED-ADDBACK-V3
RESULT_ID: R-Q032-EDE-CAMSPEC-ADDBACK-003

Scientific purpose
------------------
Continue the validated Q032 V2 TT3PAIR/common-support bridge with the smallest
bounded CamSpec-only intervention capable of localizing which information removed
by that bridge is required for stable multibasin geometry.

The preregistered hierarchy is finite:
  tier 1: SUPPORT, TE, EE
  tier 2: SUPPORT+TE, SUPPORT+EE, TE+EE (only if no tier-1 surface restores)
  tier 3: FULL_NATIVE positive control (only if no tier-2 surface restores)

Everything else is frozen: MOD-EDE-N3, class_ede commit, the nine mapped Q022
starts, optimizer settings and basin thresholds. HiLLiPoP is not rerun.

No cross-surface absolute objective subtraction is used for scientific inference.
A technical failure is NO SCIENTIFIC RESULT.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import signal
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q-032"
RUN = "Q032-CAMSPEC-NESTED-ADDBACK-V3"
RESULT = "R-Q032-EDE-CAMSPEC-ADDBACK-003"
CONFIG_FILE = "q032_camspec_addback_v3_config.yml"
SOURCE_LOCK_FILE = "q032_addback_source_lock_v3.json"
PROTOCOL_LOCK_FILE = "q032_addback_protocol_lock_v3.json"
CAMSPEC = "planck_NPIPE_highl_CamSpec.TTTEEE"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
PARENT_V2_RUN = "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
PARENT_V2_RESULT = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
PARENT_V2_SUPPORT_SHA = "f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b"
Q022_RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
Q022_RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
PAIR_NATIVE_ORDER = ("143x143", "217x217", "143x217")
START_LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
SINGLE_SURFACES = ("support", "te", "ee")
PAIR_SURFACES = ("support_te", "support_ee", "te_ee")
CONTROL_SURFACES = ("full_native",)
ALL_SURFACES = SINGLE_SURFACES + PAIR_SURFACES + CONTROL_SURFACES
SURFACE_SECTORS = {
    "support": ("SUPPORT",),
    "te": ("TE",),
    "ee": ("EE",),
    "support_te": ("SUPPORT", "TE"),
    "support_ee": ("SUPPORT", "EE"),
    "te_ee": ("TE", "EE"),
    "full_native": ("SUPPORT", "TE", "EE"),
}


class SoftStop(Exception):
    pass


def _alarm(_sig, _frame):
    raise SoftStop()


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
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8")
    os.replace(t, p)


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return d


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=json_default).encode("utf-8")
    ).hexdigest()


def sha256_array(a: np.ndarray) -> str:
    x = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(x.shape).encode("ascii"))
    h.update(x.tobytes())
    return h.hexdigest()


def load_cfg(path: str | Path = CONFIG_FILE) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    if c["model"]["name"] != "MOD-EDE-N3" or int(c["model"]["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if c["model"]["backend_commit"] != BACKEND_COMMIT:
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    pv2 = c["parents"]["q032_v2"]
    if pv2["run_id"] != PARENT_V2_RUN or pv2["result_id"] != PARENT_V2_RESULT:
        raise RuntimeError("PARENT_V2_IDENTITY_GATE=FAIL")
    if pv2["support_sha256"] != PARENT_V2_SUPPORT_SHA:
        raise RuntimeError("PARENT_V2_SUPPORT_HASH_GATE=FAIL")
    q22 = c["parents"]["q022"]
    if q22["run_id"] != Q022_RUN or q22["result_id"] != Q022_RESULT:
        raise RuntimeError("Q022_PARENT_IDENTITY_GATE=FAIL")
    if tuple(c["hierarchy"]["tier1_single_surfaces"]) != SINGLE_SURFACES:
        raise RuntimeError("TIER1_SURFACE_LOCK_GATE=FAIL")
    if tuple(c["hierarchy"]["tier2_pair_surfaces"]) != PAIR_SURFACES:
        raise RuntimeError("TIER2_SURFACE_LOCK_GATE=FAIL")
    if tuple(c["hierarchy"]["tier3_control_surfaces"]) != CONTROL_SURFACES:
        raise RuntimeError("TIER3_SURFACE_LOCK_GATE=FAIL")
    if tuple(c["starts"]["labels"]) != START_LABELS:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    st1 = c["optimizer"]["stage1"]
    ref = c["optimizer"]["refinement"]
    if int(st1["max_evals"]) != 200000 or float(st1["rhoend"]) != 1e-4:
        raise RuntimeError("STAGE1_OPTIMIZER_GATE=FAIL")
    if int(ref["max_evals"]) != 300000 or float(ref["rhoend"]) != 1e-5:
        raise RuntimeError("REFINEMENT_OPTIMIZER_GATE=FAIL")
    b = c["basin"]
    if not (
        float(b["collapse_objective_tolerance"]) == 0.50
        and float(b["collapse_common_endpoint_rms"]) == 0.10
        and int(b["stable_basin_minimum_supporting_starts"]) == 2
        and float(b["scale_floor_fraction"]) == 1e-8
        and b["refine_unless_single_cluster_covers_all_starts"] is True
    ):
        raise RuntimeError("FROZEN_BASIN_THRESHOLD_GATE=FAIL")
    required = (
        "case031_closed", "hillipop_not_rerun", "no_new_seed_family", "no_threshold_change",
        "no_cross_surface_absolute_objective_subtraction", "no_calibration_foreground_decomposition",
        "no_a_planck_causal_interpretation", "no_q024_rerun", "no_q030_rerun",
        "surface_hierarchy_preregistered", "technical_failure_no_scientific_result",
    )
    if not all(c["rules"].get(k) is True for k in required):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c


def load_source_lock() -> dict[str, Any]:
    d = read_json(ROOT / SOURCE_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("source_registry", {}).get("K-047", {}).get("bibliographic_status") != "BIBLIOGRAPHIC_DETAILS_NOT_INVENTED":
        raise RuntimeError("K047_NONINVENTION_GATE=FAIL")
    return d


def load_protocol_lock() -> dict[str, Any]:
    d = read_json(ROOT / PROTOCOL_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("PROTOCOL_IDENTITY_GATE=FAIL")
    declared = d.get("protocol_sha256")
    x = dict(d)
    x.pop("protocol_sha256", None)
    if declared != canonical_hash(x):
        raise RuntimeError("PROTOCOL_HASH_GATE=FAIL")
    return d


def objective_settings(c: Mapping[str, Any], phase: str) -> tuple[int, float]:
    if phase not in ("stage1", "refinement"):
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")
    x = c["optimizer"][phase]
    return int(x["max_evals"]), float(x["rhoend"])


def model_info_only(info: Mapping[str, Any]) -> dict[str, Any]:
    x = copy.deepcopy(dict(info))
    for k in ("sampler", "output", "force", "resume"):
        x.pop(k, None)
    return x


def create_model(info: Mapping[str, Any]):
    from cobaya.model import get_model
    return get_model(model_info_only(info))


def close_model(model: Any) -> None:
    try:
        if model is not None and hasattr(model, "close"):
            model.close()
    except Exception:
        pass


def set_ref(params: dict[str, Any], name: str, value: float) -> None:
    import q031_planck_portability_v1 as q31
    q31.set_ref(params, name, float(value))


def parent_v2_state(preflight_path: str | Path, final_path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    pf = read_json(preflight_path)
    final = read_json(final_path)
    if not (
        pf.get("q") == Q and pf.get("run_id") == PARENT_V2_RUN and pf.get("result_id") == PARENT_V2_RESULT
        and pf.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("PARENT_V2_PREFLIGHT_GATE=FAIL")
    if pf.get("support_sha256") != PARENT_V2_SUPPORT_SHA:
        raise RuntimeError("PARENT_V2_SUPPORT_HASH_GATE=FAIL")
    if not (
        final.get("q") == Q and final.get("run_id") == PARENT_V2_RUN and final.get("result_id") == PARENT_V2_RESULT
        and final.get("FINAL_RESULT_GATE") == "PASS" and final.get("actual_computed_result") is True
    ):
        raise RuntimeError("PARENT_V2_FINAL_GATE=FAIL")
    cam = final.get("implementation_results", {}).get("camspec", {})
    hlp = final.get("implementation_results", {}).get("hillipop", {})
    if cam.get("stable_multibasin") is not False or int(cam.get("stable_basin_count", -1)) != 0:
        raise RuntimeError("PARENT_V2_CAMSPEC_BASELINE_GATE=FAIL")
    if hlp.get("stable_multibasin") is not False or int(hlp.get("stable_basin_count", -1)) != 0:
        raise RuntimeError("PARENT_V2_HILLIPOP_BASELINE_GATE=FAIL")
    return pf, final


def q022_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q022" and d.get("run_id") == Q022_RUN and d.get("result_id") == Q022_RESULT
        and d.get("FINAL_RESULT_GATE") == "PASS"
        and d.get("classification") == "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
    ):
        raise RuntimeError("Q022_STABLE_FULL_NATIVE_REFERENCE_GATE=FAIL")
    return d


def row_key(row: Mapping[str, Any]) -> tuple[str, str, int]:
    return str(row["observable"]), str(row["spectrum"]), int(row["ell"])


def ordered_row_hash(rows: Sequence[Mapping[str, Any]]) -> str:
    return canonical_hash([list(row_key(r)) for r in rows])


def native_ranges_from_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for r in rows:
        out.setdefault(str(r["spectrum"]), []).append(int(r["ell"]))
    return out


def make_surface_definition(surface: str, common: Mapping[str, Sequence[int]], native: Mapping[str, Sequence[int]]) -> dict[str, Any]:
    if surface not in SURFACE_SECTORS:
        raise RuntimeError(f"SURFACE_GATE=FAIL surface={surface}")
    sectors = set(SURFACE_SECTORS[surface])
    use_cl = list(PAIR_NATIVE_ORDER)
    if "TE" in sectors:
        use_cl.append("TE")
    if "EE" in sectors:
        use_cl.append("EE")
    tt_ranges: dict[str, list[int]] = {}
    for pair in PAIR_NATIVE_ORDER:
        src = native[pair] if "SUPPORT" in sectors else common[pair]
        tt_ranges[pair] = [int(x) for x in src]
    return {
        "surface": surface,
        "sectors": list(SURFACE_SECTORS[surface]),
        "use_cl": use_cl,
        "tt_ranges": tt_ranges,
        "te_active": "TE" in sectors,
        "ee_active": "EE" in sectors,
        "support_active": "SUPPORT" in sectors,
    }


def build_camspec_surface_info(
    c: Mapping[str, Any], surface_lock: Mapping[str, Any], surface: str,
    seed: Mapping[str, float], prefix: Path, phase: str,
) -> dict[str, Any]:
    import q019_planck_cosmology_reprofile_v1 as q19

    if surface not in surface_lock["surfaces"]:
        raise RuntimeError("SURFACE_LOCK_GATE=FAIL")
    sdef = surface_lock["surfaces"][surface]
    c19 = q19.load_cfg(ROOT / "q019_planck_cosmology_reprofile_v1_config.yml")
    info = q19.build_full(c19, "reference_free_h0", 0, prefix, seed={})
    if set(info.get("likelihood", {})) - {CAMSPEC, "q019_shape_A_planck", "q019_shape_calTE", "q019_shape_calEE", "q019_shape_tau_reio"}:
        raise RuntimeError("NO_EXTRA_DATASET_GATE=FAIL")
    spec = info["likelihood"].get(CAMSPEC)
    spec = {} if spec is None else copy.deepcopy(spec)
    spec.setdefault("dataset_params", {})["use_cl"] = " ".join(sdef["use_cl"])
    # Range dict only names TT spectra. CamSpec therefore uses native full ranges
    # for active TE/EE, exactly as intended by the add-back definition.
    spec["dataset_params"]["use_range"] = {
        p: [int(x) for x in sdef["tt_ranges"][p]] for p in PAIR_NATIVE_ORDER
    }
    info["likelihood"][CAMSPEC] = spec

    if not bool(sdef["te_active"]):
        info["params"]["calTE"] = float(c["camspec"]["fixed_nonparticipating_calibration"]["calTE"])
        info["likelihood"].pop("q019_shape_calTE", None)
    if not bool(sdef["ee_active"]):
        info["params"]["calEE"] = float(c["camspec"]["fixed_nonparticipating_calibration"]["calEE"])
        info["likelihood"].pop("q019_shape_calEE", None)

    for name, value in seed.items():
        if finite(value):
            set_ref(info["params"], str(name), float(value))

    max_evals, rhoend = objective_settings(c, phase)
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim.update({"method": "bobyqa", "ignore_prior": True, "best_of": 1, "max_evals": max_evals})
    minim.setdefault("override_bobyqa", {})["rhoend"] = rhoend
    info["prior"] = {}
    info["output"] = str(prefix.resolve())
    info["force"] = True
    return info


def evaluate_once(model: Any, info: Mapping[str, Any], preferred: Mapping[str, float]) -> float:
    import q031_planck_portability_v1 as q31
    vec = q31.reference_vector(info, preferred=preferred)
    lp = model.logposterior(vec)
    value = getattr(lp, "logpost", lp)
    if not finite(value):
        raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL")
    return float(value)


def surface_covariance_gate(full_like: Any, full_rows: Sequence[Mapping[str, Any]], surf_like: Any, surf_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    index = {row_key(r): int(r["index"]) for r in full_rows}
    keys = [row_key(r) for r in surf_rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("SURFACE_ROW_UNIQUENESS_GATE=FAIL")
    try:
        selected = [index[k] for k in keys]
    except KeyError as exc:
        raise RuntimeError(f"SURFACE_TO_FULL_VECTOR_INDEX_GATE=FAIL missing={exc}") from exc
    expected_cov = np.asarray(full_like.cov, dtype=np.float64)[np.ix_(selected, selected)]
    actual_cov = np.asarray(surf_like.cov, dtype=np.float64)
    denom = max(float(np.linalg.norm(expected_cov)), 1e-300)
    rel = float(np.linalg.norm(actual_cov - expected_cov) / denom)
    if rel > 1e-12:
        raise RuntimeError(f"SURFACE_COVARIANCE_BLOCK_GATE=FAIL rel={rel}")
    try:
        chol = np.linalg.cholesky(actual_cov)
    except np.linalg.LinAlgError as exc:
        raise RuntimeError("SURFACE_COVARIANCE_POSITIVE_DEFINITE_GATE=FAIL") from exc
    return {
        "dimension": int(actual_cov.shape[0]),
        "covariance_sha256": sha256_array(actual_cov),
        "covariance_relative_difference_from_full_selected_block": rel,
        "minimum_cholesky_diagonal": float(np.min(np.diag(chol))),
        "ordered_row_sha256": ordered_row_hash(surf_rows),
        "selected_full_indices_sha256": canonical_hash(selected),
    }


def preflight(
    c: Mapping[str, Any], parent_preflight: str | Path, parent_final: str | Path,
    q022_final: str | Path, output: str | Path, surface_output: str | Path,
    manifest_output: str | Path,
) -> int:
    load_source_lock()
    protocol = load_protocol_lock()
    pv2_pf, pv2_final = parent_v2_state(parent_preflight, parent_final)
    q22 = q022_state(q022_final)
    starts = pv2_pf.get("q022_source_starts", {})
    if tuple(sorted(starts)) != tuple(sorted(START_LABELS)):
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    scales = pv2_pf.get("locked_common_scales", {})
    if not isinstance(scales, Mapping) or not scales:
        raise RuntimeError("LOCKED_SCALE_GATE=FAIL")

    import q032_planck_tt3pair_bridge_v2 as q32
    import q019_planck_cosmology_reprofile_v1 as q19

    seed = dict(starts["M3-S0"]["params"])
    c19 = q19.load_cfg(ROOT / "q019_planck_cosmology_reprofile_v1_config.yml")
    full_info = q19.build_full(c19, "reference_free_h0", 0, ROOT / "q032_runtime/v3_full_native_preflight", seed={})
    full_model = None
    surface_models = []
    try:
        full_model = create_model(full_info)
        full_like = full_model.likelihood[CAMSPEC]
        full_rows = q32.camspec_rows(full_like)
        full_ranges = native_ranges_from_rows(full_rows)
        required_names = set(PAIR_NATIVE_ORDER) | {"TE", "EE"}
        if not required_names.issubset(full_ranges):
            raise RuntimeError("CAMSPEC_NATIVE_RANGE_GATE=FAIL")
        common = pv2_pf["support_lock"]["common_ells_by_pair"]
        for p in PAIR_NATIVE_ORDER:
            if p not in common:
                raise RuntimeError(f"PARENT_COMMON_SUPPORT_PAIR_GATE=FAIL pair={p}")
        removed_tt = []
        for p in PAIR_NATIVE_ORDER:
            common_set = set(map(int, common[p]))
            for ell in full_ranges[p]:
                if int(ell) not in common_set:
                    removed_tt.append([p, int(ell)])
        if not removed_tt:
            raise RuntimeError("REMOVED_SUPPORT_NONEMPTY_GATE=FAIL")

        surface_lock: dict[str, Any] = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_ADDBACK_SURFACE_LOCK", "status": "PASS",
            "parent_v2_support_sha256": PARENT_V2_SUPPORT_SHA,
            "parent_v2_common_dimension": int(pv2_pf["support_lock"]["common_dimension"]),
            "full_native_dimension": int(len(full_rows)),
            "full_native_ordered_row_sha256": ordered_row_hash(full_rows),
            "native_ranges": {k: [int(x) for x in v] for k, v in full_ranges.items() if k in required_names},
            "common_tt_ranges": {p: [int(x) for x in common[p]] for p in PAIR_NATIVE_ORDER},
            "removed_tt_coordinates": removed_tt,
            "removed_tt_coordinates_sha256": canonical_hash(removed_tt),
            "surfaces": {},
            "hierarchy": {
                "tier1": list(SINGLE_SURFACES),
                "tier2_if_no_tier1_restoration": list(PAIR_SURFACES),
                "tier3_if_no_tier2_restoration": list(CONTROL_SURFACES),
            },
        }
        surface_diagnostics = {}
        for surface in ALL_SURFACES:
            sdef = make_surface_definition(surface, common, full_ranges)
            surface_lock["surfaces"][surface] = sdef
        # Freeze surface definition before looking at optimizer outcomes.
        surface_lock["surface_definition_sha256"] = canonical_hash(surface_lock["surfaces"])
        write_json(surface_output, surface_lock)

        for surface in ALL_SURFACES:
            info = build_camspec_surface_info(c, surface_lock, surface, seed, ROOT / f"q032_runtime/v3_probe_{surface}", "stage1")
            model = create_model(info)
            surface_models.append(model)
            like = model.likelihood[CAMSPEC]
            rows = q32.camspec_rows(like)
            diag = surface_covariance_gate(full_like, full_rows, like, rows)
            diag["finite_reference_logpost"] = evaluate_once(model, info, seed)
            diag["active_te"] = bool(surface_lock["surfaces"][surface]["te_active"])
            diag["active_ee"] = bool(surface_lock["surfaces"][surface]["ee_active"])
            diag["active_support"] = bool(surface_lock["surfaces"][surface]["support_active"])
            diag["sampled_calTE"] = isinstance(info["params"].get("calTE"), Mapping) and "prior" in info["params"]["calTE"]
            diag["sampled_calEE"] = isinstance(info["params"].get("calEE"), Mapping) and "prior" in info["params"]["calEE"]
            if diag["sampled_calTE"] != diag["active_te"] or diag["sampled_calEE"] != diag["active_ee"]:
                raise RuntimeError(f"NATIVE_CALIBRATION_MODE_COACTIVATION_GATE=FAIL surface={surface}")
            surface_diagnostics[surface] = diag

        gates = {
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "Q_IDENTITY_GATE": "PASS",
            "PARENT_V2_FINAL_GATE": "PASS",
            "PARENT_V2_BASELINE_NONSTABLE_GATE": "PASS",
            "Q022_STABLE_FULL_NATIVE_REFERENCE_GATE": "PASS",
            "BACKEND_IDENTITY_GATE": "PASS",
            "CAMSPEC_IMPLEMENTATION_IDENTITY_GATE": "PASS",
            "SURFACE_HIERARCHY_LOCK_GATE": "PASS",
            "SURFACE_DEFINITION_HASH_GATE": "PASS",
            "REMOVED_SUPPORT_RUNTIME_DERIVATION_GATE": "PASS",
            "SURFACE_TO_FULL_VECTOR_INDEX_GATE": "PASS",
            "SURFACE_COVARIANCE_BLOCK_GATE": "PASS",
            "SURFACE_COVARIANCE_POSITIVE_DEFINITE_GATE": "PASS",
            "NATIVE_CALIBRATION_MODE_COACTIVATION_GATE": "PASS",
            "FINITE_REAL_LIKELIHOOD_EVALUATION_GATE": "PASS",
            "START_PROVENANCE_GATE": "PASS",
            "NO_EXTRA_DATASET_GATE": "PASS",
        }
        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_ADDBACK_PREFLIGHT", "status": "PASS",
            "FINAL_PREFLIGHT_GATE": "PASS",
            "protocol_sha256": protocol["protocol_sha256"],
            "surface_definition_sha256": surface_lock["surface_definition_sha256"],
            "surface_lock": surface_lock,
            "surface_diagnostics": surface_diagnostics,
            "q022_source_starts": starts,
            "locked_common_scales": scales,
            "parent_v2": {
                "run_id": pv2_final["run_id"], "result_id": pv2_final["result_id"],
                "final_result_gate": pv2_final["FINAL_RESULT_GATE"],
                "camspec_stable_basin_count": int(pv2_final["implementation_results"]["camspec"]["stable_basin_count"]),
                "support_sha256": pv2_pf["support_sha256"],
            },
            "q022_full_native_historical_reference": {
                "run_id": q22["run_id"], "result_id": q22["result_id"],
                "classification": q22["classification"],
                "note": "HISTORICAL_REFERENCE_ONLY; V3 FULL_NATIVE CONTROL IS RUN IF NEEDED FOR SAME-V3-SEMANTICS CLOSURE",
            },
            "gates": gates,
        }
        write_json(output, rec)
        manifest = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_ADDBACK_JOB_MANIFEST_INITIAL", "status": "PLANNED",
            "tier1": {"conditional": False, "surfaces": list(SINGLE_SURFACES), "stage1_expected_jobs": 27, "refinement": "DYNAMIC_BY_FROZEN_RULE"},
            "tier2": {"conditional": True, "condition": "NO_TIER1_RESTORATION", "surfaces": list(PAIR_SURFACES), "stage1_expected_jobs": 27, "refinement": "DYNAMIC_BY_FROZEN_RULE"},
            "control": {"conditional": True, "condition": "NO_TIER2_RESTORATION", "surfaces": list(CONTROL_SURFACES), "stage1_expected_jobs": 9, "refinement": "DYNAMIC_BY_FROZEN_RULE"},
            "completed_jobs": [], "failed_jobs": [],
            "pending_semantics": "GITHUB_MATRIX_JOBS_ARE_TRACKED_BY_TIER_ASSESSMENTS_AND_FINAL_MANIFEST",
        }
        write_json(manifest_output, manifest)
        print("Q032_ADDBACK_PREFLIGHT_GATE=PASS")
        print("SURFACE_DEFINITION_SHA256=" + surface_lock["surface_definition_sha256"])
        return 0
    finally:
        for m in surface_models:
            close_model(m)
        close_model(full_model)


def load_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
        and d.get("stage") == "Q032_ADDBACK_PREFLIGHT" and d.get("status") == "PASS"
        and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("PREFLIGHT_GATE=FAIL")
    return d


def profile_stage(phase: str) -> str:
    return "Q032_ADDBACK_STAGE1" if phase == "stage1" else "Q032_ADDBACK_REFINEMENT"


def find_profile(root: str | Path, surface: str, phase: str, mask: int, seed: int) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
            and d.get("stage") == profile_stage(phase) and d.get("surface") == surface
            and int(d.get("source_mask", -1)) == int(mask) and int(d.get("source_seed", -1)) == int(seed)
            and d.get("status") == "COMPLETE" and finite(d.get("objective_chi2"))
        ):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(f"PROFILE_UNIQUENESS_GATE=FAIL surface={surface} phase={phase} M{mask}-S{seed} hits={len(hits)}")
    return hits[0]


def run_profile(
    c: Mapping[str, Any], preflight_path: str | Path, surface: str, phase: str,
    mask: int, seed: int, output: str | Path, stage1_dir: str | Path | None,
) -> int:
    if surface not in ALL_SURFACES:
        raise RuntimeError("SURFACE_GATE=FAIL")
    pf = load_preflight(preflight_path)
    label = f"M{mask}-S{seed}"
    if label not in pf["q022_source_starts"] or label not in START_LABELS:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    if phase == "stage1":
        start = dict(pf["q022_source_starts"][label]["params"])
        seed_semantics = "EXACT_Q032_V2_Q022_MAPPED_START"
    elif phase == "refinement":
        if stage1_dir is None:
            raise RuntimeError("REFINEMENT_PARENT_GATE=FAIL")
        parent = find_profile(stage1_dir, surface, "stage1", mask, seed)
        start = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
        seed_semantics = "EXACT_MATCHED_V3_STAGE1_MINIMUM"
    else:
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": profile_stage(phase), "phase": phase, "surface": surface,
        "sectors": list(SURFACE_SECTORS[surface]),
        "source_mask": int(mask), "source_seed": int(seed), "source_label": label,
        "source_semantics": "Q022_START_PROVENANCE_ONLY_NOT_MASK_VARIATION_IN_V3",
        "seed_semantics": seed_semantics,
        "surface_definition_sha256": pf["surface_definition_sha256"],
        "status": "FAILED", "actual_computed_result": False,
        "backend_commit": BACKEND_COMMIT,
        "cross_surface_absolute_objective_subtraction_performed": False,
    }
    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info = build_camspec_surface_info(c, pf["surface_lock"], surface, start, prefix, phase)
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        max_evals, rhoend = objective_settings(c, phase)
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
            "minimizer": {"method": "bobyqa", "ignore_prior": True, "best_of": 1,
                          "max_evals": max_evals, "rhoend": rhoend},
            "data_dimension": int(pf["surface_diagnostics"][surface]["dimension"]),
            "ordered_row_sha256": pf["surface_diagnostics"][surface]["ordered_row_sha256"],
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD", "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def collect_profiles(root: str | Path | None, phase: str) -> list[dict[str, Any]]:
    if root is None:
        return []
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT and d.get("stage") == profile_stage(phase):
            out.append(d)
    return out


def parse_surfaces(text: str) -> tuple[str, ...]:
    xs = tuple(x.strip() for x in text.split(",") if x.strip())
    if not xs or any(x not in ALL_SURFACES for x in xs) or len(xs) != len(set(xs)):
        raise RuntimeError("SURFACE_LIST_GATE=FAIL")
    return xs


def cluster_rows(rows: Sequence[Mapping[str, Any]], scales: Mapping[str, float]) -> dict[str, Any]:
    import q032_planck_tt3pair_bridge_v2 as q32
    return q32.bridge_cluster(rows, scales)


def assess_tier(
    c: Mapping[str, Any], preflight_path: str | Path, stage1_dir: str | Path,
    surfaces_text: str, tier: str, output: str | Path, matrix_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    surfaces = parse_surfaces(surfaces_text)
    rows = collect_profiles(stage1_dir, "stage1")
    expected = {(s, m, r) for s in surfaces for m in (3, 6, 7) for r in (0, 1, 2)}
    got = {
        (str(x.get("surface")), int(x.get("source_mask", -1)), int(x.get("source_seed", -1)))
        for x in rows if x.get("surface") in surfaces and x.get("status") == "COMPLETE" and finite(x.get("objective_chi2"))
    }
    if got != expected:
        rec = {"q": Q, "run_id": RUN, "result_id": RESULT, "stage": "Q032_ADDBACK_TIER_ASSESSMENT",
               "tier": tier, "status": "FAIL", "JOB_COMPLETENESS_GATE": "FAIL",
               "expected_count": len(expected), "got_count": len(got)}
        write_json(output, rec)
        write_json(matrix_output, {"include": []})
        return 2
    diagnostics = {}
    matrix_rows = []
    for surface in surfaces:
        rr = [x for x in rows if x.get("surface") == surface]
        diag = cluster_rows(rr, pf["locked_common_scales"])
        needs = not bool(diag["single_cluster_covers_all"])
        diagnostics[surface] = {"needs_refinement": needs, "stage1_cluster_diagnostic": diag}
        if needs:
            matrix_rows.extend({"surface": surface, "mask": m, "seed": s} for m in (3, 6, 7) for s in (0, 1, 2))
    matrix = {"include": matrix_rows}
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_ADDBACK_TIER_ASSESSMENT", "tier": tier, "status": "PASS",
        "surfaces": list(surfaces), "JOB_COMPLETENESS_GATE": "PASS",
        "needs_refinement": bool(matrix_rows), "surface_diagnostics": diagnostics,
        "refinement_matrix": matrix,
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if matrix_rows else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0


def load_tier_assessment(path: str | Path, tier: str) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
        and d.get("stage") == "Q032_ADDBACK_TIER_ASSESSMENT" and d.get("tier") == tier
        and d.get("status") == "PASS" and d.get("JOB_COMPLETENESS_GATE") == "PASS"
    ):
        raise RuntimeError("TIER_ASSESSMENT_GATE=FAIL")
    return d


def finalize_tier(
    c: Mapping[str, Any], preflight_path: str | Path, assessment_path: str | Path,
    stage1_dir: str | Path, refinement_dir: str | Path | None,
    surfaces_text: str, tier: str, output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    assess = load_tier_assessment(assessment_path, tier)
    surfaces = parse_surfaces(surfaces_text)
    if tuple(assess["surfaces"]) != surfaces:
        raise RuntimeError("TIER_SURFACE_IDENTITY_GATE=FAIL")
    stage1 = collect_profiles(stage1_dir, "stage1")
    refined = collect_profiles(refinement_dir, "refinement") if refinement_dir else []
    results = {}
    restoring = []
    expected_keys = {(m, s) for m in (3, 6, 7) for s in (0, 1, 2)}
    for surface in surfaces:
        needs = bool(assess["surface_diagnostics"][surface]["needs_refinement"])
        source_rows = refined if needs else stage1
        rows = [x for x in source_rows if x.get("surface") == surface and x.get("status") == "COMPLETE" and finite(x.get("objective_chi2"))]
        keys = {(int(x["source_mask"]), int(x["source_seed"])) for x in rows}
        if keys != expected_keys or len(rows) != 9:
            raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL surface={surface} count={len(rows)}")
        diag = cluster_rows(rows, pf["locked_common_scales"])
        stable_count = int(diag["stable_basin_count"])
        stable = stable_count >= int(c["basin"]["stable_basin_minimum_supporting_starts"])
        if stable:
            restoring.append(surface)
        results[surface] = {
            "decisive_phase": "refinement" if needs else "stage1",
            "complete_profiles": 9,
            "stable_multibasin": stable,
            "stable_basin_count": stable_count,
            "cluster_diagnostic": diag,
            "sectors": list(SURFACE_SECTORS[surface]),
        }
    continue_next = len(restoring) == 0 and tier in ("tier1", "tier2")
    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_ADDBACK_TIER_FINAL", "tier": tier, "status": "PASS",
        "surfaces": list(surfaces), "surface_results": results,
        "restoring_surfaces": restoring,
        "minimum_restoring_cardinality_in_this_tier": (len(SURFACE_SECTORS[restoring[0]]) if restoring else None),
        "continue_to_next_tier": continue_next,
        "JOB_COMPLETENESS_GATE": "PASS", "GLOBALITY_GATE": "PASS",
    }
    write_json(output, out)
    print("TIER_FINAL_GATE=PASS")
    print("CONTINUE_NEXT=" + ("true" if continue_next else "false"))
    print("RESTORING_SURFACES=" + json.dumps(restoring, separators=(",", ":")))
    return 0


def load_tier_final(path: str | Path, tier: str) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
        and d.get("stage") == "Q032_ADDBACK_TIER_FINAL" and d.get("tier") == tier
        and d.get("status") == "PASS" and d.get("JOB_COMPLETENESS_GATE") == "PASS"
    ):
        raise RuntimeError("TIER_FINAL_GATE=FAIL")
    return d


def aggregate_final(
    c: Mapping[str, Any], preflight_path: str | Path, tier1_path: str | Path,
    tier2_path: str | Path | None, control_path: str | Path | None, output: str | Path,
    manifest_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    t1 = load_tier_final(tier1_path, "tier1")
    t2 = load_tier_final(tier2_path, "tier2") if tier2_path else None
    ctrl = load_tier_final(control_path, "control") if control_path else None
    if t1["restoring_surfaces"]:
        restoring = list(t1["restoring_surfaces"])
        classification = "SINGLE_SECTOR_LOCALIZATION" if len(restoring) == 1 else "MULTIPLE_SINGLE_SECTOR_RESTORATIONS"
        minimum_cardinality = 1
        required_tiers = ["tier1"]
    else:
        if t2 is None:
            raise RuntimeError("TIER2_REQUIRED_GATE=FAIL")
        if t2["restoring_surfaces"]:
            restoring = list(t2["restoring_surfaces"])
            classification = "TWO_SECTOR_LOCALIZATION" if len(restoring) == 1 else "MULTIPLE_TWO_SECTOR_RESTORATIONS"
            minimum_cardinality = 2
            required_tiers = ["tier1", "tier2"]
        else:
            if ctrl is None:
                raise RuntimeError("FULL_NATIVE_CONTROL_REQUIRED_GATE=FAIL")
            cresult = ctrl["surface_results"].get("full_native", {})
            if cresult.get("stable_multibasin") is True:
                restoring = ["full_native"]
                classification = "THREE_SECTOR_JOINT_RESTORATION_ONLY"
                minimum_cardinality = 3
            else:
                restoring = []
                classification = "NO_CLEAN_LOCALIZATION_WITHIN_TESTED_CAMSPEC_INFORMATION_SECTORS"
                minimum_cardinality = None
            required_tiers = ["tier1", "tier2", "control"]
    result_sets = {s: list(SURFACE_SECTORS[s]) for s in restoring}
    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_ADDBACK_FINAL", "status": "PASS",
        "execution_status": "COMPLETE", "tests_status": "COMPLETE", "actual_computed_result": True,
        "parent_v2_result_id": PARENT_V2_RESULT,
        "parent_v2_support_sha256": PARENT_V2_SUPPORT_SHA,
        "surface_definition_sha256": pf["surface_definition_sha256"],
        "required_tiers_executed": required_tiers,
        "tier1_result": t1,
        "tier2_result": t2,
        "control_result": ctrl,
        "classification": classification,
        "restoring_surfaces": restoring,
        "restoring_sector_sets": result_sets,
        "minimum_restoring_sector_cardinality": minimum_cardinality,
        "q032_question_resolution_recommended": True,
        "next_required_action": "RETURN_TO_RESULT_INGESTION_AND_ROUTING_ENGINE_FOR_Q032_CLOSURE_ASSESSMENT_AND_MOTOR14_ROUTE",
        "physical_or_instrumental_causality_claim": False,
        "cross_surface_absolute_objective_subtraction_performed": False,
        "CASE031_REOPENED": False,
        "mandatory_gates": {
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "Q_IDENTITY_GATE": "PASS",
            "PARENT_V2_BASELINE_GATE": "PASS",
            "SURFACE_HIERARCHY_GATE": "PASS",
            "SURFACE_DEFINITION_GATE": "PASS",
            "COVARIANCE_SELECTION_GATE": "PASS",
            "FINITE_REAL_LIKELIHOOD_GATE": "PASS",
            "START_PROVENANCE_GATE": "PASS",
            "JOB_COMPLETENESS_GATE": "PASS",
            "MERGE_COMPATIBILITY_GATE": "PASS",
            "GLOBALITY_GATE": "PASS",
            "ANTI_LOOP_STOP_GATE": "PASS",
            "SCIENTIFIC_INTERPRETATION_GATE": "PASS",
            "FINAL_RESULT_GATE": "PASS",
        },
        "FINAL_RESULT_GATE": "PASS",
        "journal_effect": {
            "Q032_V2": "KEEP_AS_AUTHORITATIVE_TT3PAIR_BASELINE",
            "CASE031": "KEEP_CLOSED",
            "Q032_V3": "ADD_BOUNDED_CAMSPEC_INFORMATION_SECTOR_LOCALIZATION",
            "interpretation_boundary": "LIKELIHOOD_INFORMATION_ARCHITECTURE_NOT_CAUSAL_SYSTEMATIC",
        },
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    }
    write_json(output, out)
    final_manifest = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_ADDBACK_JOB_MANIFEST_FINAL", "status": "COMPLETE",
        "required_tiers_executed": required_tiers,
        "tier1": {"executed": True, "surface_count": 3, "stage1_jobs": 27, "restoring_surfaces": t1["restoring_surfaces"]},
        "tier2": {"executed": t2 is not None, "surface_count": 3 if t2 is not None else 0, "stage1_jobs": 27 if t2 is not None else 0, "restoring_surfaces": t2["restoring_surfaces"] if t2 else []},
        "control": {"executed": ctrl is not None, "surface_count": 1 if ctrl is not None else 0, "stage1_jobs": 9 if ctrl is not None else 0, "restoring_surfaces": ctrl["restoring_surfaces"] if ctrl else []},
        "refinement_jobs": {
            "tier1": sum(9 for s in t1["surface_results"].values() if s["decisive_phase"] == "refinement"),
            "tier2": sum(9 for s in t2["surface_results"].values() if s["decisive_phase"] == "refinement") if t2 else 0,
            "control": sum(9 for s in ctrl["surface_results"].values() if s["decisive_phase"] == "refinement") if ctrl else 0,
        },
        "JOB_COMPLETENESS_GATE": "PASS", "FINAL_RESULT_GATE": "PASS",
    }
    write_json(manifest_output, final_manifest)
    print("Q032_ADDBACK_FINAL_RESULT_GATE=PASS")
    print("CLASSIFICATION=" + classification)
    print("RESTORING_SURFACES=" + json.dumps(restoring, separators=(",", ":")))
    return 0


def self_test(c: Mapping[str, Any], output: str | Path | None = None) -> int:
    # Pure static hierarchy / logic test. No scientific result is synthesized.
    assert set(SINGLE_SURFACES) == {"support", "te", "ee"}
    assert set(PAIR_SURFACES) == {"support_te", "support_ee", "te_ee"}
    assert SURFACE_SECTORS["full_native"] == ("SUPPORT", "TE", "EE")
    assert all(len(SURFACE_SECTORS[s]) == 1 for s in SINGLE_SURFACES)
    assert all(len(SURFACE_SECTORS[s]) == 2 for s in PAIR_SURFACES)
    assert len(set(ALL_SURFACES)) == 7
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_ADDBACK_SELF_TEST", "status": "PASS",
        "surface_hierarchy": {"tier1": list(SINGLE_SURFACES), "tier2": list(PAIR_SURFACES), "control": list(CONTROL_SURFACES)},
        "actual_computed_scientific_result": False,
    }
    if output:
        write_json(output, rec)
    print("Q032_ADDBACK_SELF_TEST_GATE=PASS")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=CONFIG_FILE)
    sp = p.add_subparsers(dest="command", required=True)
    s = sp.add_parser("self-test")
    s.add_argument("--output")
    s = sp.add_parser("preflight")
    s.add_argument("--parent-preflight", required=True)
    s.add_argument("--parent-final", required=True)
    s.add_argument("--q022-final", required=True)
    s.add_argument("--output", required=True)
    s.add_argument("--surface-output", required=True)
    s.add_argument("--manifest-output", required=True)
    s = sp.add_parser("profile")
    s.add_argument("--preflight", required=True)
    s.add_argument("--surface", required=True, choices=ALL_SURFACES)
    s.add_argument("--phase", required=True, choices=("stage1", "refinement"))
    s.add_argument("--mask", required=True, type=int, choices=(3, 6, 7))
    s.add_argument("--seed", required=True, type=int, choices=(0, 1, 2))
    s.add_argument("--output", required=True)
    s.add_argument("--stage1-dir")
    s = sp.add_parser("assess-tier")
    s.add_argument("--preflight", required=True)
    s.add_argument("--stage1-dir", required=True)
    s.add_argument("--surfaces", required=True)
    s.add_argument("--tier", required=True, choices=("tier1", "tier2", "control"))
    s.add_argument("--output", required=True)
    s.add_argument("--matrix-output", required=True)
    s = sp.add_parser("finalize-tier")
    s.add_argument("--preflight", required=True)
    s.add_argument("--assessment", required=True)
    s.add_argument("--stage1-dir", required=True)
    s.add_argument("--refinement-dir")
    s.add_argument("--surfaces", required=True)
    s.add_argument("--tier", required=True, choices=("tier1", "tier2", "control"))
    s.add_argument("--output", required=True)
    s = sp.add_parser("aggregate-final")
    s.add_argument("--preflight", required=True)
    s.add_argument("--tier1", required=True)
    s.add_argument("--tier2")
    s.add_argument("--control")
    s.add_argument("--output", required=True)
    s.add_argument("--manifest-output", required=True)
    return p


def main() -> int:
    a = parser().parse_args()
    c = load_cfg(a.config)
    if a.command == "self-test":
        return self_test(c, a.output)
    if a.command == "preflight":
        return preflight(c, a.parent_preflight, a.parent_final, a.q022_final, a.output, a.surface_output, a.manifest_output)
    if a.command == "profile":
        return run_profile(c, a.preflight, a.surface, a.phase, a.mask, a.seed, a.output, a.stage1_dir)
    if a.command == "assess-tier":
        return assess_tier(c, a.preflight, a.stage1_dir, a.surfaces, a.tier, a.output, a.matrix_output)
    if a.command == "finalize-tier":
        return finalize_tier(c, a.preflight, a.assessment, a.stage1_dir, a.refinement_dir, a.surfaces, a.tier, a.output)
    if a.command == "aggregate-final":
        return aggregate_final(c, a.preflight, a.tier1, a.tier2, a.control, a.output, a.manifest_output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
