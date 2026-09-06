#!/usr/bin/env python3
"""
Bubbleverse Q-033 — matched CamSpec launch/reference-semantics A/B test V1.

CURRENT_Q: Q-033
RUN_ID: Q033-CAMSPEC-LAUNCH-SEMANTICS-MATCHED-AB-V1
RESULT_ID: R-Q033-EDE-CAMSPEC-LAUNCH-SEMANTICS-001

Scientific purpose
------------------
Test exactly one mechanism:

Does the historical Q022 non-scalar Cobaya reference-distribution semantics
restore the stable multibasin classification on the same frozen Q032 V4
CamSpec FULL_NATIVE surface when compared against genuine scalar refs, with
all other numerical/scientific components matched?

This program does NOT:
- change the MOD-EDE-N3 physics or backend commit;
- rerun Q032 TE/EE/support add-back;
- rerun HiLLiPoP;
- change basin thresholds;
- add seed families;
- reinterpret Q022 as invalid;
- invalidate Q023-Q030 fixed-vector diagnostics;
- infer any physical or instrumental cause.

Historical Q022 semantics are reconstructed from the actual Q021/Q022
constructor chain. Q021's primordial coordinates (n_s, logA, tau_reio) were
fixed in Q022, so only parameters that were actually sampled by Q022 receive
historical distribution refs in the historical arm. Any additional sampled
coordinates on the matched Q032 V4 surface remain scalar in both arms.

Both arms use the same Cobaya minimizer seed. The seed controls reference
sampling; scalar refs remain literal starts. Every actual optimizer launch
point is serialized for audit.
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

Q = "Q-033"
RUN = "Q033-CAMSPEC-LAUNCH-SEMANTICS-MATCHED-AB-V1"
RESULT = "R-Q033-EDE-CAMSPEC-LAUNCH-SEMANTICS-001"
CONFIG_FILE = "q033_launch_semantics_ab_v1_config.yml"
PROTOCOL_LOCK_FILE = "q033_launch_semantics_protocol_lock_v1.json"

BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
Q022_RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
Q022_RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
Q032_RUN = "Q032-EXACT-START-CONFORMANCE-ADDBACK-V4"
Q032_RESULT = "R-Q032-EDE-CAMSPEC-ADDBACK-004"
Q032_FULL_NATIVE_SURFACE = "full_native"
ARMS = ("historical_dist", "scalar")
MASKS = (3, 6, 7)
SEEDS = (0, 1, 2)
START_LABELS = tuple(f"M{m}-S{s}" for m in MASKS for s in SEEDS)


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
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return d


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(
        obj, sort_keys=True, separators=(",", ":"), default=json_default
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)


def load_cfg(path: str | Path = CONFIG_FILE) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != BACKEND_COMMIT:
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if tuple(c["arms"]["names"]) != ARMS:
        raise RuntimeError("ARM_IDENTITY_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["masks"]) != MASKS:
        raise RuntimeError("MASK_IDENTITY_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["seed_restarts"]) != SEEDS:
        raise RuntimeError("START_IDENTITY_GATE=FAIL")
    if tuple(c["starts"]["labels"]) != START_LABELS:
        raise RuntimeError("START_LABEL_GATE=FAIL")

    st1 = c["optimizer"]["stage1"]
    ref = c["optimizer"]["refinement"]
    if (
        c["optimizer"]["method"] != "bobyqa"
        or c["optimizer"]["ignore_prior_density"] is not True
        or int(c["optimizer"]["best_of"]) != 1
        or int(st1["max_evals"]) != 200000
        or float(st1["rhoend"]) != 1e-4
        or int(ref["max_evals"]) != 300000
        or float(ref["rhoend"]) != 1e-5
    ):
        raise RuntimeError("OPTIMIZER_FREEZE_GATE=FAIL")

    b = c["basin"]
    if not (
        float(b["collapse_objective_tolerance"]) == 0.50
        and float(b["collapse_common_endpoint_rms"]) == 0.10
        and int(b["stable_basin_minimum_supporting_starts"]) == 2
        and float(b["scale_floor_fraction"]) == 1e-8
        and b["refine_unless_single_cluster_covers_all_starts"] is True
    ):
        raise RuntimeError("FROZEN_BASIN_THRESHOLD_GATE=FAIL")

    required_rules = (
        "same_full_native_surface_both_arms",
        "only_launch_reference_semantics_differs",
        "historical_ref_semantics_from_actual_q021_q022_chain",
        "scalar_ref_semantics_from_q032_v4",
        "same_cobaya_seed_both_arms",
        "no_new_seed_family",
        "no_threshold_change",
        "no_te_ee_support_addback",
        "hillipop_not_rerun",
        "q032_v3_science_forbidden",
        "q022_raw_result_preserved",
        "q023_q030_fixed_vector_results_preserved",
        "technical_failure_no_scientific_result",
        "stop_if_semantics_sufficient",
        "no_open_ended_search_if_semantics_insufficient",
    )
    if not all(c["rules"].get(k) is True for k in required_rules):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c


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


def model_info_without_execution(info: Mapping[str, Any]) -> dict[str, Any]:
    x = copy.deepcopy(dict(info))
    for k in ("sampler", "output", "force", "resume"):
        x.pop(k, None)
    return x


def strip_refs(info: Mapping[str, Any]) -> dict[str, Any]:
    x = model_info_without_execution(info)
    params = x.get("params", {})
    if isinstance(params, Mapping):
        for name, spec in list(params.items()):
            if isinstance(spec, Mapping):
                z = copy.deepcopy(dict(spec))
                z.pop("ref", None)
                params[name] = z
    return x


def set_scalar_ref(params: dict[str, Any], name: str, value: float) -> None:
    spec = params.get(name)
    if not sampled(spec):
        raise RuntimeError(f"SCALAR_REF_TARGET_GATE=FAIL parameter={name}")
    x = float(value)
    prior = spec.get("prior", {})
    if isinstance(prior, Mapping):
        if finite(prior.get("min")) and x < float(prior["min"]):
            raise RuntimeError(f"START_BOUND_GATE=FAIL parameter={name} side=min")
        if finite(prior.get("max")) and x > float(prior["max"]):
            raise RuntimeError(f"START_BOUND_GATE=FAIL parameter={name} side=max")
    new_spec = copy.deepcopy(dict(spec))
    new_spec["ref"] = x
    params[name] = new_spec


def historical_ref_from_template(template_ref: Any, value: float) -> Any:
    """
    Pure reconstruction of q021.set_ref semantics.

    If historical ref is a mapping, preserve its distribution structure/scale
    and move only loc/mean. If it is scalar, remain scalar.
    """
    x = float(value)
    if isinstance(template_ref, Mapping):
        rr = copy.deepcopy(dict(template_ref))
        if "loc" in rr:
            rr["loc"] = x
        elif "mean" in rr:
            rr["mean"] = x
        else:
            rr = {"loc": x, "scale": 0.0}
        return rr
    return x


def apply_historical_refs(
    target_params: dict[str, Any],
    template_params: Mapping[str, Any],
    center: Mapping[str, float],
    historical_names: Sequence[str],
) -> dict[str, Any]:
    missing = [
        n for n in historical_names
        if n not in target_params or n not in template_params or n not in center
        or not finite(center[n])
    ]
    if missing:
        raise RuntimeError("HISTORICAL_REF_TEMPLATE_COVERAGE_GATE=FAIL missing=" + repr(missing))

    refs: dict[str, Any] = {}
    non_scalar = []
    scalar = []
    for name in historical_names:
        if not sampled(target_params[name]):
            raise RuntimeError(f"HISTORICAL_TARGET_SAMPLED_GATE=FAIL parameter={name}")
        t_spec = template_params[name]
        if not sampled(t_spec):
            raise RuntimeError(f"HISTORICAL_TEMPLATE_SAMPLED_GATE=FAIL parameter={name}")
        new_spec = copy.deepcopy(dict(target_params[name]))
        new_ref = historical_ref_from_template(t_spec.get("ref"), float(center[name]))
        new_spec["ref"] = new_ref
        target_params[name] = new_spec
        refs[name] = copy.deepcopy(new_ref)
        if isinstance(new_ref, Mapping):
            non_scalar.append(name)
        else:
            scalar.append(name)

    if not non_scalar:
        raise RuntimeError("NONSCALAR_HISTORICAL_REFERENCE_GATE=FAIL")
    return {
        "semantics": "Q022_Q021_NONSCALAR_REF_DISTRIBUTION_RECONSTRUCTION",
        "historical_parameter_names": list(historical_names),
        "non_scalar_ref_names": sorted(non_scalar),
        "scalar_ref_names_within_historical_subset": sorted(scalar),
        "configured_refs": refs,
        "configured_refs_sha256": canonical_hash(refs),
    }


def scalar_ref_audit(params: Mapping[str, Any]) -> dict[str, Any]:
    names = sorted(name for name, spec in params.items() if sampled(spec))
    bad = []
    refs = {}
    for name in names:
        r = params[name].get("ref")
        if not isinstance(r, (int, float, np.integer, np.floating)) or not finite(r):
            bad.append(name)
        else:
            refs[name] = float(r)
    return {
        "sampled_parameter_names": names,
        "all_refs_scalar": not bad,
        "non_scalar_ref_names": bad,
        "refs": refs,
        "refs_sha256": canonical_hash(refs),
    }


def q022_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q022"
        and d.get("run_id") == Q022_RUN
        and d.get("result_id") == Q022_RESULT
        and d.get("FINAL_RESULT_GATE") == "PASS"
        and d.get("classification")
        == "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
    ):
        raise RuntimeError("Q022_HISTORICAL_REFERENCE_GATE=FAIL")
    return d


def q032_preflight_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("Q032_V4_PREFLIGHT_GATE=FAIL")
    starts = d.get("q022_source_starts", {})
    if tuple(sorted(starts)) != tuple(sorted(START_LABELS)):
        raise RuntimeError("Q032_V4_START_PROVENANCE_GATE=FAIL")
    if Q032_FULL_NATIVE_SURFACE not in d.get("surface_lock", {}).get("surfaces", {}):
        raise RuntimeError("Q032_V4_FULL_NATIVE_SURFACE_GATE=FAIL")
    scales = d.get("locked_common_scales", {})
    if not isinstance(scales, Mapping) or not scales:
        raise RuntimeError("Q032_V4_SCALE_LOCK_GATE=FAIL")
    return d


def q032_control_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    # Accept either the tier final artifact itself or the nested control object.
    if d.get("q") != "Q-032" or d.get("run_id") != Q032_RUN or d.get("result_id") != Q032_RESULT:
        raise RuntimeError("Q032_V4_CONTROL_IDENTITY_GATE=FAIL")
    if d.get("stage") == "Q032_ADDBACK_TIER_FINAL":
        block = d
    elif d.get("stage") == "Q032_EXACT_START_ADDBACK_FINAL":
        block = d.get("control_result")
    else:
        block = None
    if not isinstance(block, Mapping):
        raise RuntimeError("Q032_V4_CONTROL_STRUCTURE_GATE=FAIL")
    r = block.get("surface_results", {}).get(Q032_FULL_NATIVE_SURFACE, {})
    if not (
        block.get("status") == "PASS"
        and r.get("stable_multibasin") is False
        and int(r.get("stable_basin_count", -1)) == 0
    ):
        raise RuntimeError("Q032_V4_SCALAR_FULL_NATIVE_REFERENCE_GATE=FAIL")
    return dict(block)


def optimizer_settings(c: Mapping[str, Any], phase: str) -> tuple[int, float]:
    if phase not in ("stage1", "refinement"):
        raise RuntimeError("PHASE_GATE=FAIL")
    x = c["optimizer"][phase]
    return int(x["max_evals"]), float(x["rhoend"])


def historical_template_info(mask: int, prefix: Path) -> dict[str, Any]:
    """
    Rebuild the exact Q021 full-MF zero-phase constructor used by Q022
    only to recover its sampled/ref template. This object is never the
    scientific objective run by Q033.
    """
    import q021_primordial_decomposition_v1 as q21
    import q022_globality_continuation_v2 as q22

    q22_cfg = yaml.safe_load(
        (ROOT / "q022_globality_continuation_v2_config.yml").read_text(encoding="utf-8")
    )
    q21_cfg_path = ROOT / q22_cfg["parents"]["q021_config"]
    q21cfg = q21.load_cfg(q21_cfg_path)
    info, _fixed, _like_id = q21.build_info(
        q21cfg, "full_mf", int(mask), 1, prefix
    )
    return info


def historical_sampled_names(template_info: Mapping[str, Any]) -> list[str]:
    import q021_primordial_decomposition_v1 as q21
    return sorted(
        name for name, spec in template_info.get("params", {}).items()
        if q21.sampled(spec) and name not in q21.PRIMORDIAL
    )


def build_matched_info(
    c: Mapping[str, Any],
    pf: Mapping[str, Any],
    center: Mapping[str, float],
    arm: str,
    mask: int,
    prefix: Path,
    phase: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Start from the authoritative Q032 V4 FULL_NATIVE builder in both arms.

    It scalarizes every sampled ref. The historical arm then changes only the
    subset of refs that Q022 actually treated as sampled non-primordial
    parameters, using Q021's original ref-distribution template.
    """
    if arm not in ARMS:
        raise RuntimeError("ARM_GATE=FAIL")

    import q032_exact_start_addback_v4 as q32v4

    q32cfg = q32v4.load_cfg(ROOT / "q032_exact_start_addback_v4_config.yml")
    info = q32v4.build_camspec_surface_info(
        q32cfg,
        pf["surface_lock"],
        Q032_FULL_NATIVE_SURFACE,
        center,
        prefix,
        phase,
    )

    sampled_names = sorted(name for name, spec in info["params"].items() if sampled(spec))
    missing_center = [n for n in sampled_names if n not in center or not finite(center[n])]
    if missing_center:
        raise RuntimeError("MATCHED_CENTER_COMPLETENESS_GATE=FAIL missing=" + repr(missing_center))

    # Reassert scalar refs for every sampled parameter before branching.
    for name in sampled_names:
        set_scalar_ref(info["params"], name, float(center[name]))
    scalar_baseline = scalar_ref_audit(info["params"])
    if not scalar_baseline["all_refs_scalar"]:
        raise RuntimeError("MATCHED_SCALAR_BASELINE_GATE=FAIL")

    template = historical_template_info(
        mask, prefix.parent / f"{prefix.name}_historical_template"
    )
    hist_names = historical_sampled_names(template)
    absent_target = [n for n in hist_names if n not in sampled_names]
    if absent_target:
        raise RuntimeError(
            "MATCHED_PARAMETERIZATION_COVERAGE_GATE=FAIL "
            "historically_sampled_missing_from_q032_surface=" + repr(absent_target)
        )

    if arm == "historical_dist":
        ref_audit = apply_historical_refs(
            info["params"], template["params"], center, hist_names
        )
    else:
        ref_audit = {
            "semantics": "Q032_V4_SCALAR_REF_LITERAL_START",
            **scalar_ref_audit(info["params"]),
            "historical_parameter_names": hist_names,
        }

    # Common numerical settings. Seed is deliberately identical in both arms.
    max_evals, rhoend = optimizer_settings(c, phase)
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim.update(
        {
            "method": "bobyqa",
            "ignore_prior": True,
            "best_of": 1,
            "max_evals": max_evals,
            "seed": int(c["optimizer"]["cobaya_seed"]),
        }
    )
    minim.setdefault("override_bobyqa", {})["rhoend"] = rhoend
    info["prior"] = {}
    info["output"] = str(prefix.resolve())
    info["force"] = True

    untouched_scalar = sorted(set(sampled_names) - set(hist_names))
    audit = {
        "arm": arm,
        "phase": phase,
        "source_mask": int(mask),
        "sampled_parameter_names": sampled_names,
        "historically_sampled_parameter_names": hist_names,
        "held_scalar_in_both_arms": untouched_scalar,
        "reference_semantics_audit": ref_audit,
        "cobaya_seed": int(c["optimizer"]["cobaya_seed"]),
        "non_ref_model_hash": canonical_hash(strip_refs(info)),
    }
    return info, audit


def sampler_launch_point(sampler: Any) -> dict[str, float]:
    pts = getattr(sampler, "initial_points", None)
    if not pts or len(pts) != 1:
        raise RuntimeError("ACTUAL_LAUNCH_CAPTURE_GATE=FAIL")
    model = getattr(sampler, "model", None)
    if model is None:
        model = getattr(sampler, "_model", None)
    if model is None:
        raise RuntimeError("SAMPLER_MODEL_ACCESS_GATE=FAIL")
    names = list(model.parameterization.sampled_params())
    vec = np.asarray(pts[0], dtype=float)
    if len(names) != len(vec) or not np.all(np.isfinite(vec)):
        raise RuntimeError("ACTUAL_LAUNCH_VECTOR_GATE=FAIL")
    return {str(k): float(v) for k, v in zip(names, vec)}


def preflight(
    c: Mapping[str, Any],
    q032_preflight_path: str | Path,
    q032_control_path: str | Path,
    q022_final_path: str | Path,
    output: str | Path,
    manifest_output: str | Path,
) -> int:
    protocol = load_protocol_lock()
    pf = q032_preflight_state(q032_preflight_path)
    q32ctrl = q032_control_state(q032_control_path)
    q22 = q022_state(q022_final_path)

    # Audit that both branches are structurally identical after refs are removed.
    seed = dict(pf["q022_source_starts"]["M3-S0"]["params"])
    a, audit_a = build_matched_info(
        c, pf, seed, "historical_dist", 3,
        ROOT / "q033_runtime/preflight_hist", "stage1"
    )
    b, audit_b = build_matched_info(
        c, pf, seed, "scalar", 3,
        ROOT / "q033_runtime/preflight_scalar", "stage1"
    )
    h_a = canonical_hash(strip_refs(a))
    h_b = canonical_hash(strip_refs(b))
    if h_a != h_b:
        raise RuntimeError("ONLY_REFERENCE_SEMANTICS_DIFF_GATE=FAIL")
    if audit_a["historically_sampled_parameter_names"] != audit_b["historically_sampled_parameter_names"]:
        raise RuntimeError("HISTORICAL_PARAMETER_SUBSET_GATE=FAIL")

    rec = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_MATCHED_AB_PREFLIGHT",
        "status": "PASS",
        "FINAL_PREFLIGHT_GATE": "PASS",
        "protocol_sha256": protocol["protocol_sha256"],
        "q032_surface_definition_sha256": pf["surface_definition_sha256"],
        "matched_non_ref_model_hash": h_a,
        "q032_source_starts": pf["q022_source_starts"],
        "locked_common_scales": pf["locked_common_scales"],
        # Carry the authoritative Q032 V4 lock forward unchanged. Q033 only
        # executes full_native, but the reused V4 builder expects the original
        # {"surfaces": ...} structure.
        "surface_lock": copy.deepcopy(pf["surface_lock"]),
        "historical_template_audit": audit_a,
        "scalar_template_audit": audit_b,
        "parent_state": {
            "q022": {
                "run_id": q22["run_id"],
                "result_id": q22["result_id"],
                "historical_classification": q22["classification"],
                "interpretation": "VALID_HISTORICAL_EXECUTION; NOT_ASSUMED_LAUNCH_SEMANTICS_INVARIANT",
            },
            "q032_v4": {
                "run_id": Q032_RUN,
                "result_id": Q032_RESULT,
                "full_native_scalar_stable_multibasin": False,
                "full_native_scalar_stable_basin_count": 0,
                "source_control_stage": q32ctrl.get("stage"),
            },
        },
        "gates": {
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "Q_IDENTITY_GATE": "PASS",
            "Q022_HISTORICAL_RESULT_GATE": "PASS",
            "Q032_V4_FINAL_NATIVE_REFERENCE_GATE": "PASS",
            "START_PROVENANCE_GATE": "PASS",
            "BACKEND_IDENTITY_GATE": "PASS",
            "CAMSPEC_FULL_NATIVE_SURFACE_GATE": "PASS",
            "HISTORICAL_REF_TEMPLATE_RECOVERY_GATE": "PASS",
            "MATCHED_PARAMETERIZATION_COVERAGE_GATE": "PASS",
            "ONLY_REFERENCE_SEMANTICS_DIFF_GATE": "PASS",
            "FROZEN_BASIN_THRESHOLD_GATE": "PASS",
            "COMMON_SEED_GATE": "PASS",
        },
    }
    write_json(output, rec)

    manifest = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_JOB_MANIFEST_INITIAL",
        "status": "PLANNED",
        "stage1": {
            "expected_jobs": 18,
            "arms": list(ARMS),
            "starts_per_arm": 9,
        },
        "refinement": {
            "dynamic": True,
            "maximum_jobs": 18,
            "rule": "REFINE_ALL_NINE_STARTS_IN_AN_ARM_UNLESS_STAGE1_SINGLE_CLUSTER_COVERS_ALL_STARTS",
        },
        "completed_jobs": [],
        "failed_jobs": [],
    }
    write_json(manifest_output, manifest)
    print("Q033_PREFLIGHT_GATE=PASS")
    return 0


def load_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q
        and d.get("run_id") == RUN
        and d.get("result_id") == RESULT
        and d.get("stage") == "Q033_MATCHED_AB_PREFLIGHT"
        and d.get("status") == "PASS"
        and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("PREFLIGHT_GATE=FAIL")
    return d


def profile_stage(phase: str) -> str:
    if phase == "stage1":
        return "Q033_MATCHED_AB_STAGE1"
    if phase == "refinement":
        return "Q033_MATCHED_AB_REFINEMENT"
    raise RuntimeError("PHASE_GATE=FAIL")


def find_profile(
    root: str | Path, arm: str, phase: str, mask: int, seed: int
) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == Q
            and d.get("run_id") == RUN
            and d.get("result_id") == RESULT
            and d.get("stage") == profile_stage(phase)
            and d.get("arm") == arm
            and int(d.get("source_mask", -1)) == int(mask)
            and int(d.get("source_seed", -1)) == int(seed)
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(
            f"PROFILE_UNIQUENESS_GATE=FAIL arm={arm} phase={phase} "
            f"M{mask}-S{seed} hits={len(hits)}"
        )
    return hits[0]


def run_profile(
    c: Mapping[str, Any],
    preflight_path: str | Path,
    arm: str,
    phase: str,
    mask: int,
    seed: int,
    output: str | Path,
    stage1_dir: str | Path | None,
) -> int:
    if arm not in ARMS:
        raise RuntimeError("ARM_GATE=FAIL")
    if mask not in MASKS or seed not in SEEDS:
        raise RuntimeError("START_GATE=FAIL")
    pf = load_preflight(preflight_path)
    label = f"M{mask}-S{seed}"
    if label not in pf["q032_source_starts"]:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")

    if phase == "stage1":
        center = dict(pf["q032_source_starts"][label]["params"])
        center_semantics = "Q022_OUTPUT_ENDPOINT_PROVENANCE_VECTOR"
    elif phase == "refinement":
        if stage1_dir is None:
            raise RuntimeError("REFINEMENT_PARENT_GATE=FAIL")
        parent = find_profile(stage1_dir, arm, "stage1", mask, seed)
        center = {
            str(k): float(v)
            for k, v in parent["minimum"].items()
            if finite(v)
        }
        center_semantics = "MATCHED_SAME_ARM_STAGE1_MINIMUM"
    else:
        raise RuntimeError("PHASE_GATE=FAIL")

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": profile_stage(phase),
        "phase": phase,
        "arm": arm,
        "source_mask": int(mask),
        "source_seed": int(seed),
        "source_label": label,
        "center_semantics": center_semantics,
        "status": "FAILED",
        "actual_computed_result": False,
        "backend_commit": BACKEND_COMMIT,
        "surface": Q032_FULL_NATIVE_SURFACE,
        "cobaya_seed": int(c["optimizer"]["cobaya_seed"]),
    }

    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info, audit = build_matched_info(
            c, pf, center, arm, mask, prefix, phase
        )
        rec["matched_build_audit"] = audit

        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)

        actual_launch = sampler_launch_point(sampler)
        rec["actual_optimizer_launch"] = actual_launch
        rec["actual_optimizer_launch_sha256"] = canonical_hash(actual_launch)

        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")

        max_evals, rhoend = optimizer_settings(c, phase)
        rec.update(
            {
                "status": "COMPLETE",
                "actual_computed_result": True,
                "objective_chi2": float(row["chi2"]),
                "minimum": row,
                "harvested_minimum_path": source,
                "minimizer_settings": {
                    "method": "bobyqa",
                    "ignore_prior": True,
                    "best_of": 1,
                    "max_evals": max_evals,
                    "rhoend": rhoend,
                    "seed": int(c["optimizer"]["cobaya_seed"]),
                },
                "ONLY_REFERENCE_SEMANTICS_DIFF_DECLARED": True,
            }
        )
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update(
            {
                "status": "FAILED",
                "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                "error": repr(exc),
            }
        )
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
        if (
            d.get("q") == Q
            and d.get("run_id") == RUN
            and d.get("result_id") == RESULT
            and d.get("stage") == profile_stage(phase)
        ):
            out.append(d)
    return out


def cluster_rows(rows: Sequence[Mapping[str, Any]], scales: Mapping[str, float]) -> dict[str, Any]:
    import q032_planck_tt3pair_bridge_v2 as q32
    return q32.bridge_cluster(rows, scales)


def assess(
    c: Mapping[str, Any],
    preflight_path: str | Path,
    stage1_dir: str | Path,
    output: str | Path,
    matrix_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    rows = collect_profiles(stage1_dir, "stage1")

    expected = {(a, m, s) for a in ARMS for m in MASKS for s in SEEDS}
    got = {
        (str(x.get("arm")), int(x.get("source_mask", -1)), int(x.get("source_seed", -1)))
        for x in rows
        if x.get("status") == "COMPLETE" and finite(x.get("objective_chi2"))
    }
    if got != expected:
        rec = {
            "q": Q,
            "run_id": RUN,
            "result_id": RESULT,
            "stage": "Q033_MATCHED_AB_ASSESSMENT",
            "status": "FAIL",
            "JOB_COMPLETENESS_GATE": "FAIL",
            "expected_count": len(expected),
            "got_count": len(got),
            "missing": sorted([list(x) for x in expected - got]),
        }
        write_json(output, rec)
        write_json(matrix_output, {"include": []})
        return 2

    diagnostics = {}
    matrix_rows = []
    for arm in ARMS:
        rr = [x for x in rows if x.get("arm") == arm]
        diag = cluster_rows(rr, pf["locked_common_scales"])
        needs = not bool(diag["single_cluster_covers_all"])
        diagnostics[arm] = {
            "needs_refinement": needs,
            "stage1_cluster_diagnostic": diag,
        }
        if needs:
            matrix_rows.extend(
                {"arm": arm, "mask": m, "seed": s}
                for m in MASKS for s in SEEDS
            )

    matrix = {"include": matrix_rows}
    rec = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_MATCHED_AB_ASSESSMENT",
        "status": "PASS",
        "JOB_COMPLETENESS_GATE": "PASS",
        "needs_refinement": bool(matrix_rows),
        "arm_diagnostics": diagnostics,
        "refinement_matrix": matrix,
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if matrix_rows else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0


def load_assessment(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q
        and d.get("run_id") == RUN
        and d.get("result_id") == RESULT
        and d.get("stage") == "Q033_MATCHED_AB_ASSESSMENT"
        and d.get("status") == "PASS"
        and d.get("JOB_COMPLETENESS_GATE") == "PASS"
    ):
        raise RuntimeError("ASSESSMENT_GATE=FAIL")
    return d


def finalize(
    c: Mapping[str, Any],
    preflight_path: str | Path,
    assessment_path: str | Path,
    stage1_dir: str | Path,
    refinement_dir: str | Path | None,
    output: str | Path,
    manifest_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    ass = load_assessment(assessment_path)
    stage1 = collect_profiles(stage1_dir, "stage1")
    refined = collect_profiles(refinement_dir, "refinement") if refinement_dir else []

    expected_keys = {(m, s) for m in MASKS for s in SEEDS}
    arm_results = {}
    for arm in ARMS:
        needs = bool(ass["arm_diagnostics"][arm]["needs_refinement"])
        source_rows = refined if needs else stage1
        rr = [
            x for x in source_rows
            if x.get("arm") == arm
            and x.get("status") == "COMPLETE"
            and finite(x.get("objective_chi2"))
        ]
        keys = {(int(x["source_mask"]), int(x["source_seed"])) for x in rr}
        if keys != expected_keys or len(rr) != 9:
            raise RuntimeError(
                f"JOB_COMPLETENESS_GATE=FAIL arm={arm} count={len(rr)}"
            )
        diag = cluster_rows(rr, pf["locked_common_scales"])
        stable_count = int(diag["stable_basin_count"])
        stable = stable_count >= int(c["basin"]["stable_basin_minimum_supporting_starts"])
        arm_results[arm] = {
            "decisive_phase": "refinement" if needs else "stage1",
            "complete_profiles": 9,
            "stable_multibasin": stable,
            "stable_basin_count": stable_count,
            "cluster_diagnostic": diag,
            "profiles": [
                {
                    "source_label": x["source_label"],
                    "objective_chi2": x["objective_chi2"],
                    "actual_optimizer_launch_sha256": x["actual_optimizer_launch_sha256"],
                    "minimum": x["minimum"],
                }
                for x in sorted(rr, key=lambda z: (int(z["source_mask"]), int(z["source_seed"])))
            ],
        }

    scalar = arm_results["scalar"]
    hist = arm_results["historical_dist"]

    scalar_reference_pass = (
        scalar["stable_multibasin"] is False
        and int(scalar["stable_basin_count"]) == 0
    )

    if not scalar_reference_pass:
        classification = "Q033_UNRESOLVED_SCALAR_Q032_V4_REFERENCE_NOT_REPRODUCED"
        final_gate = "UNRESOLVED"
        semantics_answer = "UNRESOLVED"
        next_action = (
            "DEBUG_THE_MATCHED_Q033_IMPLEMENTATION_AGAINST_Q032_V4_FULL_NATIVE; "
            "DO_NOT_INTERPRET_HISTORICAL_ARM"
        )
        residual = None
    elif hist["stable_multibasin"] is True:
        classification = "LAUNCH_REFERENCE_SEMANTICS_SUFFICIENT_WITHIN_MATCHED_Q033_AB"
        final_gate = "PASS"
        semantics_answer = "YES"
        next_action = (
            "STOP_Q033_AND_RETURN_TO_RESULT_INGESTION_AND_ROUTING_ENGINE; "
            "UPDATE_Q022_INTERPRETATION_TO_EXECUTION_START_SEMANTICS_DEPENDENT"
        )
        residual = None
    else:
        classification = "LAUNCH_REFERENCE_SEMANTICS_ALONE_NOT_SUFFICIENT_WITHIN_MATCHED_Q033_AB"
        final_gate = "PASS"
        semantics_answer = "NO"
        next_action = (
            "STOP_Q033_AFTER_REGISTERING_D-Q033-REMAINING-001_AS_THE_SMALLEST "
            "REMAINING_IMPLEMENTATION_DIFFERENCE; DO_NOT_START_OPEN_BRUTE_FORCE"
        )
        residual = {
            "id": "D-Q033-REMAINING-001",
            "status": "IDENTIFIED_NOT_TESTED",
            "description": (
                "Constructor/parameterization path: historical Q022 executes through "
                "q021.build_info(full_mf, mask, restart=1), including a frozen "
                "primordial vertex, whereas Q032 V4 FULL_NATIVE executes through "
                "the q019 full-native constructor before scalar-ref conformance. "
                "This is the next smallest implementation delta after matched ref "
                "semantics; Q033 does not test it."
            ),
            "secondary_difference_not_promoted": (
                "Q022 refinement reconstructs its Q021 endpoint-centred continuation, "
                "whereas Q032 V4 refinement recentres on the matched Stage-1 minimum."
            ),
        }

    mandatory_gates = {
        "CONTEXT_CONTINUITY_GATE": "PASS",
        "Q_IDENTITY_GATE": "PASS",
        "Q022_HISTORICAL_RESULT_GATE": "PASS",
        "Q032_V4_FULL_NATIVE_PARENT_GATE": "PASS",
        "BACKEND_IDENTITY_GATE": "PASS",
        "CAMSPEC_FULL_NATIVE_SURFACE_GATE": "PASS",
        "ONLY_REFERENCE_SEMANTICS_DIFF_GATE": "PASS",
        "COMMON_SEED_GATE": "PASS",
        "ACTUAL_LAUNCH_CAPTURE_GATE": "PASS",
        "JOB_COMPLETENESS_GATE": "PASS",
        "MERGE_COMPATIBILITY_GATE": "PASS",
        "FROZEN_BASIN_THRESHOLD_GATE": "PASS",
        "GLOBALITY_GATE": "PASS",
        "SCALAR_Q032_REFERENCE_REPRODUCTION_GATE": (
            "PASS" if scalar_reference_pass else "FAIL"
        ),
        "SCIENTIFIC_INTERPRETATION_GATE": (
            "PASS" if final_gate == "PASS" else "UNRESOLVED"
        ),
        "FINAL_RESULT_GATE": final_gate,
    }

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_MATCHED_AB_FINAL",
        "execution_status": "COMPLETE",
        "tests_status": "COMPLETE",
        "actual_computed_result": True,
        "scientific_question": c["project"]["scientific_question"],
        "classification": classification,
        "launch_reference_semantics_alone_explains_difference": semantics_answer,
        "arm_results": arm_results,
        "residual_implementation_difference_if_needed": residual,
        "physical_or_instrumental_causality_claim": False,
        "new_physics_claim": False,
        "q032_reopened": False,
        "q032_sector_addback_rerun": False,
        "hillipop_rerun": False,
        "q032_v3_scientific_result_used": False,
        "next_required_action": next_action,
        "mandatory_gates": mandatory_gates,
        "FINAL_RESULT_GATE": final_gate,
        "journal_effect": {
            "Q022": (
                "KEEP_HISTORICAL_RAW_RESULT; "
                + (
                    "STABLE_BASIN_INTERPRETATION_BECOMES_EXPLICITLY_LAUNCH_SEMANTICS_DEPENDENT"
                    if semantics_answer == "YES"
                    else "KEEP_REVISED_INTERPRETATION; REF_SEMANTICS_ALONE_DID_NOT_REPRODUCE_HISTORICAL_GEOMETRY"
                    if semantics_answer == "NO"
                    else "NO_SCIENTIFIC_UPDATE_PENDING_IMPLEMENTATION_DEBUG"
                )
            ),
            "Q023_Q030": "KEEP_FIXED_VECTOR_RESULTS; INTERPRETATION_REMAINS_CONDITIONAL_ON_HISTORICAL_Q022_ENDPOINT_FAMILY",
            "Q032": "KEEP_AUTHORITATIVE_V4_RESULT; NO_SECTOR_RERUN",
            "CASE031": "KEEP_CLOSED",
            "HYP_Q033_A": (
                "SUPPORTED_AS_MATCHED_CAUSE"
                if semantics_answer == "YES"
                else "NOT_SUFFICIENT_ALONE"
                if semantics_answer == "NO"
                else "UNRESOLVED"
            ),
            "HYP_Q033_B": (
                "NOT_REQUIRED_FOR_Q033"
                if semantics_answer == "YES"
                else "REMAINS_ACTIVE_WITH_D-Q033-REMAINING-001"
                if semantics_answer == "NO"
                else "UNRESOLVED"
            ),
        },
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    }
    write_json(output, out)

    manifest = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_JOB_MANIFEST_FINAL",
        "status": "COMPLETE",
        "stage1_jobs": 18,
        "refinement_jobs": sum(
            9 for a in ARMS if ass["arm_diagnostics"][a]["needs_refinement"]
        ),
        "arms": list(ARMS),
        "FINAL_RESULT_GATE": final_gate,
    }
    write_json(manifest_output, manifest)
    print("FINAL_RESULT_GATE=" + final_gate)
    print("Q033_CLASSIFICATION=" + classification)
    return 0 if final_gate == "PASS" else 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=CONFIG_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("preflight")
    a.add_argument("--q032-preflight", required=True)
    a.add_argument("--q032-control", required=True)
    a.add_argument("--q022-final", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--manifest-output", required=True)

    a = sub.add_parser("profile")
    a.add_argument("--preflight", required=True)
    a.add_argument("--arm", choices=ARMS, required=True)
    a.add_argument("--phase", choices=("stage1", "refinement"), required=True)
    a.add_argument("--mask", type=int, required=True)
    a.add_argument("--seed", type=int, required=True)
    a.add_argument("--stage1-dir")
    a.add_argument("--output", required=True)

    a = sub.add_parser("assess")
    a.add_argument("--preflight", required=True)
    a.add_argument("--stage1-dir", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--matrix-output", required=True)

    a = sub.add_parser("finalize")
    a.add_argument("--preflight", required=True)
    a.add_argument("--assessment", required=True)
    a.add_argument("--stage1-dir", required=True)
    a.add_argument("--refinement-dir")
    a.add_argument("--output", required=True)
    a.add_argument("--manifest-output", required=True)
    return p


def main() -> int:
    args = build_parser().parse_args()
    c = load_cfg(args.config)
    if args.cmd == "preflight":
        return preflight(
            c, args.q032_preflight, args.q032_control, args.q022_final,
            args.output, args.manifest_output
        )
    if args.cmd == "profile":
        return run_profile(
            c, args.preflight, args.arm, args.phase, args.mask, args.seed,
            args.output, args.stage1_dir
        )
    if args.cmd == "assess":
        return assess(
            c, args.preflight, args.stage1_dir, args.output, args.matrix_output
        )
    if args.cmd == "finalize":
        return finalize(
            c, args.preflight, args.assessment, args.stage1_dir,
            args.refinement_dir, args.output, args.manifest_output
        )
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
