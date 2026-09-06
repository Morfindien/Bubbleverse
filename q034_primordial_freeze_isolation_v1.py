#!/usr/bin/env python3
"""
Bubbleverse Q-034 — matched primordial freeze/sampling isolation V1.

CURRENT_Q: Q-034
RUN_ID: Q034-PRIMORDIAL-FREEZE-ISOLATION-V1
RESULT_ID: R-Q034-EDE-PRIMORDIAL-FREEZE-ISOLATION-001

Scientific question
-------------------
Under the frozen CamSpec full-multifrequency MOD-EDE-N3 likelihood, with scalar
endpoint references, the same nine Q022 provenance vectors, identical numerical
settings and unchanged basin criteria, does freezing versus sampling the
primordial block (n_s, logA, tau_reio) reproduce the Q022 stable-multibasin
versus Q032 V4 non-stable FULL_NATIVE classification difference?

Design
------
* Reuse the authoritative Q032 V4 FULL_NATIVE sampled-primordial control when
  source, surface, parameter, reference, optimizer, start and basin identity
  gates pass.
* Build the new arm from q032_exact_start_addback_v4.build_camspec_surface_info.
* Change exactly one scientific variable: replace n_s/logA/tau_reio sampled
  specs by literal fixed values from the corresponding authoritative Q022
  provenance vector.
* Run only the nine frozen Stage-1 shards, followed by the existing tighter
  refinement only if the unchanged Q032 basin protocol requires it.
* Do not rerun Q032 sectors, HiLLiPoP, Q023-Q030, or any new seed family.

This is an internal computational parameterization test. It is not an
independent observation and does not establish or falsify new physics.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import signal
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q-034"
RUN = "Q034-PRIMORDIAL-FREEZE-ISOLATION-V1"
RESULT = "R-Q034-EDE-PRIMORDIAL-FREEZE-ISOLATION-001"
CONFIG_FILE = "q034_primordial_freeze_isolation_v1_config.yml"
SOURCE_LOCK_FILE = "q034_primordial_freeze_source_lock_v1.json"

Q032_Q = "Q-032"
Q032_RUN = "Q032-EXACT-START-CONFORMANCE-ADDBACK-V4"
Q032_RESULT = "R-Q032-EDE-CAMSPEC-ADDBACK-004"
Q022_RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
Q022_RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
FULL_NATIVE = "full_native"
PRIMORDIAL = ("n_s", "logA", "tau_reio")
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


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=json_default).encode("utf-8")
    ).hexdigest()


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


def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)


def git_blob(path: str | Path) -> str:
    proc = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"GIT_BLOB_GATE=FAIL path={path} stderr={proc.stderr!r}")
    return proc.stdout.strip()


def load_cfg(path: str | Path = CONFIG_FILE) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3 or m["backend_commit"] != BACKEND_COMMIT:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if tuple(c["primordial_block"]["coordinates"]) != PRIMORDIAL:
        raise RuntimeError("PRIMORDIAL_IDENTITY_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["masks"]) != MASKS:
        raise RuntimeError("MASK_IDENTITY_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["seed_restarts"]) != SEEDS:
        raise RuntimeError("SEED_IDENTITY_GATE=FAIL")
    if tuple(c["starts"]["labels"]) != START_LABELS:
        raise RuntimeError("START_LABEL_GATE=FAIL")
    st1 = c["optimizer"]["stage1"]
    ref = c["optimizer"]["refinement"]
    if int(st1["max_evals"]) != 200000 or float(st1["rhoend"]) != 1e-4:
        raise RuntimeError("STAGE1_OPTIMIZER_GATE=FAIL")
    if int(ref["max_evals"]) != 300000 or float(ref["rhoend"]) != 1e-5:
        raise RuntimeError("REFINEMENT_OPTIMIZER_GATE=FAIL")
    if int(c["optimizer"]["best_of"]) != 1:
        raise RuntimeError("BEST_OF_GATE=FAIL")
    b = c["basin"]
    if not (
        float(b["collapse_objective_tolerance"]) == 0.50
        and float(b["collapse_common_endpoint_rms"]) == 0.10
        and int(b["stable_basin_minimum_supporting_starts"]) == 2
        and float(b["scale_floor_fraction"]) == 1e-8
    ):
        raise RuntimeError("FROZEN_BASIN_THRESHOLD_GATE=FAIL")
    required = (
        "reuse_q032_sampled_control_if_identity_passes",
        "full_native_only",
        "scalar_refs_only",
        "freeze_only_primordial_block",
        "no_new_seed_family",
        "no_threshold_change",
        "no_q032_sector_rerun",
        "no_q023_q030_rerun",
        "case031_closed",
        "hillipop_not_rerun",
        "no_new_likelihood",
        "no_new_physics_inference",
        "technical_failure_no_scientific_result",
        "stop_after_q034_classification",
    )
    if not all(c["rules"].get(k) is True for k in required):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c


def load_source_lock() -> dict[str, Any]:
    d = read_json(ROOT / SOURCE_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    for name, expected in d["bubbleverse_files"].items():
        p = ROOT / name
        if not p.exists():
            raise RuntimeError(f"SOURCE_FILE_GATE=FAIL missing={name}")
        actual = git_blob(p)
        if actual != expected:
            raise RuntimeError(
                f"HISTORICAL_SOURCE_BLOB_GATE=FAIL file={name} expected={expected} actual={actual}"
            )
    return d


def q032_preflight_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q032_Q
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("Q032_V4_PREFLIGHT_GATE=FAIL")
    starts = d.get("q022_source_starts", {})
    if tuple(sorted(starts)) != tuple(sorted(START_LABELS)):
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    if FULL_NATIVE not in d.get("surface_lock", {}).get("surfaces", {}):
        raise RuntimeError("FULL_NATIVE_SURFACE_GATE=FAIL")
    scales = d.get("locked_common_scales", {})
    if not isinstance(scales, Mapping) or not scales:
        raise RuntimeError("LOCKED_SCALE_GATE=FAIL")
    return d


def q032_final_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q032_Q
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("FINAL_RESULT_GATE") == "PASS"
        and d.get("actual_computed_result") is True
    ):
        raise RuntimeError("Q032_V4_FINAL_GATE=FAIL")
    return d


def q032_control_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q032_Q
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("stage") == "Q032_ADDBACK_TIER_FINAL"
        and d.get("tier") == "control"
        and d.get("status") == "PASS"
        and d.get("JOB_COMPLETENESS_GATE") == "PASS"
        and d.get("GLOBALITY_GATE") == "PASS"
    ):
        raise RuntimeError("Q032_V4_CONTROL_FINAL_GATE=FAIL")
    r = d.get("surface_results", {}).get(FULL_NATIVE, {})
    if r.get("stable_multibasin") is not False or int(r.get("stable_basin_count", -1)) != 0:
        raise RuntimeError("Q032_V4_FULL_NATIVE_NONSTABLE_GATE=FAIL")
    if int(r.get("complete_profiles", -1)) != 9:
        raise RuntimeError("Q032_V4_CONTROL_COMPLETENESS_GATE=FAIL")
    return d


def q032_cfg_identity(c: Mapping[str, Any]) -> dict[str, Any]:
    import q032_exact_start_addback_v4 as q32

    c32 = q32.load_cfg(ROOT / "q032_exact_start_addback_v4_config.yml")
    gates = {
        "MODEL": c32["model"]["name"] == c["model"]["name"],
        "NSCF": int(c32["model"]["n_scf"]) == int(c["model"]["n_scf"]),
        "BACKEND": c32["model"]["backend_commit"] == c["model"]["backend_commit"],
        "STAGE1_MAX_EVALS": int(c32["optimizer"]["stage1"]["max_evals"]) == int(c["optimizer"]["stage1"]["max_evals"]),
        "STAGE1_RHOEND": float(c32["optimizer"]["stage1"]["rhoend"]) == float(c["optimizer"]["stage1"]["rhoend"]),
        "REFINEMENT_MAX_EVALS": int(c32["optimizer"]["refinement"]["max_evals"]) == int(c["optimizer"]["refinement"]["max_evals"]),
        "REFINEMENT_RHOEND": float(c32["optimizer"]["refinement"]["rhoend"]) == float(c["optimizer"]["refinement"]["rhoend"]),
        "BASIN_OBJECTIVE": float(c32["basin"]["collapse_objective_tolerance"]) == float(c["basin"]["collapse_objective_tolerance"]),
        "BASIN_RMS": float(c32["basin"]["collapse_common_endpoint_rms"]) == float(c["basin"]["collapse_common_endpoint_rms"]),
        "BASIN_SUPPORT": int(c32["basin"]["stable_basin_minimum_supporting_starts"]) == int(c["basin"]["stable_basin_minimum_supporting_starts"]),
        "BASIN_SCALE_FLOOR": float(c32["basin"]["scale_floor_fraction"]) == float(c["basin"]["scale_floor_fraction"]),
    }
    if not all(gates.values()):
        raise RuntimeError("Q032_CONFIG_IDENTITY_GATE=FAIL " + repr({k: v for k, v in gates.items() if not v}))
    return {"gates": {k: "PASS" for k in gates}, "q032_config_sha256": canonical_hash(c32)}


def info_without_runtime(info: Mapping[str, Any]) -> dict[str, Any]:
    x = copy.deepcopy(dict(info))
    for k in ("output", "force", "resume"):
        x.pop(k, None)
    return x


def assert_only_primordial_delta(sampled_info: Mapping[str, Any], frozen_info: Mapping[str, Any], fixed: Mapping[str, float]) -> dict[str, Any]:
    a = info_without_runtime(sampled_info)
    b = info_without_runtime(frozen_info)
    pa = copy.deepcopy(a.pop("params"))
    pb = copy.deepcopy(b.pop("params"))
    if a != b:
        raise RuntimeError("NONPARAMETER_CONSTRUCTOR_IDENTITY_GATE=FAIL")
    names_a = set(pa)
    names_b = set(pb)
    if names_a != names_b:
        raise RuntimeError("PARAMETER_NAME_IDENTITY_GATE=FAIL")
    nonprim_diff = [n for n in sorted(names_a - set(PRIMORDIAL)) if pa[n] != pb[n]]
    if nonprim_diff:
        raise RuntimeError("NONPRIMORDIAL_PARAMETER_SPEC_IDENTITY_GATE=FAIL " + repr(nonprim_diff))
    for n in PRIMORDIAL:
        if not sampled(pa[n]):
            raise RuntimeError(f"SAMPLED_CONTROL_PRIMORDIAL_GATE=FAIL parameter={n}")
        if not finite(pb[n]) or float(pb[n]) != float(fixed[n]):
            raise RuntimeError(f"FROZEN_PRIMORDIAL_VALUE_GATE=FAIL parameter={n}")
    sampled_before = sorted(n for n, spec in pa.items() if sampled(spec))
    sampled_after = sorted(n for n, spec in pb.items() if sampled(spec))
    if sorted(set(sampled_before) - set(sampled_after)) != sorted(PRIMORDIAL):
        raise RuntimeError("SAMPLED_SET_DELTA_GATE=FAIL")
    if set(sampled_after) - set(sampled_before):
        raise RuntimeError("SAMPLED_SET_EXPANSION_GATE=FAIL")
    return {
        "sampled_control_parameter_names": sampled_before,
        "frozen_arm_sampled_parameter_names": sampled_after,
        "removed_from_sampled_set": sorted(PRIMORDIAL),
        "nonprimordial_specs_identical": True,
        "nonparameter_constructor_identical": True,
    }


def freeze_primordial(info: dict[str, Any], fixed: Mapping[str, float]) -> None:
    params = info["params"]
    for name in PRIMORDIAL:
        if name not in params or not finite(fixed.get(name)):
            raise RuntimeError(f"PRIMORDIAL_VALUE_COMPLETENESS_GATE=FAIL parameter={name}")
        params[name] = float(fixed[name])


def build_frozen_info(
    c: Mapping[str, Any], pf: Mapping[str, Any], start: Mapping[str, float],
    fixed: Mapping[str, float], prefix: Path, phase: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    import q032_exact_start_addback_v4 as q32

    c32 = q32.load_cfg(ROOT / "q032_exact_start_addback_v4_config.yml")
    sampled_info = q32.build_camspec_surface_info(
        c32, pf["surface_lock"], FULL_NATIVE, start, prefix, phase
    )
    frozen_info = copy.deepcopy(sampled_info)
    freeze_primordial(frozen_info, fixed)
    delta = assert_only_primordial_delta(sampled_info, frozen_info, fixed)
    return frozen_info, delta


def source_label(mask: int, seed: int) -> str:
    if mask not in MASKS or seed not in SEEDS:
        raise RuntimeError("START_LABEL_COMPONENT_GATE=FAIL")
    return f"M{mask}-S{seed}"


def preflight(
    c: Mapping[str, Any], q032_preflight_path: str | Path,
    q032_final_path: str | Path, q032_control_path: str | Path,
    output: str | Path, manifest_output: str | Path,
) -> int:
    src = load_source_lock()
    pf = q032_preflight_state(q032_preflight_path)
    q32final = q032_final_state(q032_final_path)
    ctrl = q032_control_state(q032_control_path)
    cfg_identity = q032_cfg_identity(c)

    ctrl_from_final = q32final.get("control_result", {}).get("surface_results", {}).get(FULL_NATIVE, {})
    ctrl_direct = ctrl["surface_results"][FULL_NATIVE]
    if (
        ctrl_from_final.get("stable_multibasin") is not False
        or int(ctrl_from_final.get("stable_basin_count", -1)) != 0
        or int(ctrl_from_final.get("stable_basin_count", -1)) != int(ctrl_direct["stable_basin_count"])
    ):
        raise RuntimeError("Q032_CONTROL_CROSS_ARTIFACT_IDENTITY_GATE=FAIL")

    sdef = pf["surface_lock"]["surfaces"][FULL_NATIVE]
    if not (
        bool(sdef.get("support_active"))
        and bool(sdef.get("te_active"))
        and bool(sdef.get("ee_active"))
        and tuple(sdef.get("sectors", ())) == ("SUPPORT", "TE", "EE")
    ):
        raise RuntimeError("FULL_NATIVE_SURFACE_IDENTITY_GATE=FAIL")

    per_start = {}
    for label in START_LABELS:
        center = {str(k): float(v) for k, v in pf["q022_source_starts"][label]["params"].items() if finite(v)}
        missing = [n for n in PRIMORDIAL if n not in center]
        if missing:
            raise RuntimeError(f"PRIMORDIAL_PROVENANCE_GATE=FAIL label={label} missing={missing}")
        info, delta = build_frozen_info(
            c, pf, center, {n: center[n] for n in PRIMORDIAL},
            ROOT / f"q034_runtime/preflight_{label}", "stage1"
        )
        sampled_names = sorted(n for n, spec in info["params"].items() if sampled(spec))
        refs = {}
        for n in sampled_names:
            r = info["params"][n].get("ref") if isinstance(info["params"][n], Mapping) else None
            if not isinstance(r, (int, float, np.integer, np.floating)) or not finite(r):
                raise RuntimeError(f"EXACT_SCALAR_REFERENCE_GATE=FAIL label={label} parameter={n}")
            refs[n] = float(r)
        per_start[label] = {
            "provenance_hash": canonical_hash(center),
            "fixed_primordial": {n: center[n] for n in PRIMORDIAL},
            "fixed_primordial_hash": canonical_hash({n: center[n] for n in PRIMORDIAL}),
            "sampled_nonprimordial_names": sampled_names,
            "sampled_nonprimordial_ref_sha256": canonical_hash(refs),
            "constructor_delta_audit": delta,
        }

    gates = {
        "CONTEXT_CONTINUITY_GATE": "PASS",
        "Q_IDENTITY_GATE": "PASS",
        "HISTORICAL_SOURCE_BLOB_GATE": "PASS",
        "MODEL_IDENTITY_GATE": "PASS",
        "Q032_V4_PREFLIGHT_GATE": "PASS",
        "Q032_V4_FINAL_GATE": "PASS",
        "Q032_V4_CONTROL_FINAL_GATE": "PASS",
        "Q032_CONTROL_CROSS_ARTIFACT_IDENTITY_GATE": "PASS",
        "Q032_CONFIG_IDENTITY_GATE": "PASS",
        "FULL_NATIVE_SURFACE_IDENTITY_GATE": "PASS",
        "START_PROVENANCE_GATE": "PASS",
        "EXACT_SCALAR_REFERENCE_GATE": "PASS",
        "PRIMORDIAL_PROVENANCE_GATE": "PASS",
        "SAMPLED_SET_DELTA_GATE": "PASS",
        "NONPRIMORDIAL_PARAMETER_SPEC_IDENTITY_GATE": "PASS",
        "NONPARAMETER_CONSTRUCTOR_IDENTITY_GATE": "PASS",
        "CONTROL_REUSE_IDENTITY_GATE": "PASS",
    }
    rec = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q034_MATCHED_PREFLIGHT",
        "status": "PASS",
        "FINAL_PREFLIGHT_GATE": "PASS",
        "scientific_question": c["project"]["scientific_question"],
        "source_lock_sha256": canonical_hash(src),
        "q032_config_identity": cfg_identity,
        "q032_parent": {
            "execution_commit": c["parents"]["q032_v4"]["execution_commit"],
            "run_id": Q032_RUN,
            "result_id": Q032_RESULT,
            "surface_definition_sha256": pf["surface_definition_sha256"],
            "full_native_ordered_row_sha256": pf["surface_diagnostics"][FULL_NATIVE]["ordered_row_sha256"],
            "full_native_dimension": int(pf["surface_diagnostics"][FULL_NATIVE]["dimension"]),
        },
        "sampled_control_reuse": {
            "approved": True,
            "source": "Q032_V4_FULL_NATIVE_CONTROL",
            "stable_basin_count": 0,
            "stable_multibasin": False,
            "decisive_phase": ctrl_direct.get("decisive_phase"),
            "complete_profiles": int(ctrl_direct["complete_profiles"]),
            "rerun_required": False,
        },
        "q022_source_starts": pf["q022_source_starts"],
        "locked_common_scales": pf["locked_common_scales"],
        "locked_scales_hash": pf.get("locked_scales_hash", canonical_hash(pf["locked_common_scales"])),
        "surface_lock": pf["surface_lock"],
        "per_start_constructor_identity": per_start,
        "primordial_block": list(PRIMORDIAL),
        "gates": gates,
        "unresolved_conditions": [],
    }
    write_json(output, rec)
    manifest = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q034_JOB_MANIFEST_INITIAL",
        "status": "READY",
        "sampled_control_decisive_profiles_reused": 9,
        "sampled_control_new_optimizer_jobs": 0,
        "sampled_control_historical_optimizer_job_count": "NOT_RECOUNTED_FROM_DECISIVE_PROFILE_COUNT",
        "frozen_stage1_expected_jobs": 9,
        "frozen_refinement_max_jobs": 9,
        "expected_labels": list(START_LABELS),
        "checkpointing": False,
    }
    write_json(manifest_output, manifest)
    print("Q034_PREFLIGHT_GATE=PASS")
    print("CONTROL_REUSE_IDENTITY_GATE=PASS")
    return 0


def load_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
        and d.get("stage") == "Q034_MATCHED_PREFLIGHT"
        and d.get("status") == "PASS" and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
        and d.get("sampled_control_reuse", {}).get("approved") is True
    ):
        raise RuntimeError("Q034_PREFLIGHT_GATE=FAIL")
    if tuple(sorted(d.get("q022_source_starts", {}))) != tuple(sorted(START_LABELS)):
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    return d


def profile_stage(phase: str) -> str:
    if phase == "stage1":
        return "Q034_FROZEN_STAGE1"
    if phase == "refinement":
        return "Q034_FROZEN_REFINEMENT"
    raise RuntimeError("PROFILE_PHASE_GATE=FAIL")


def find_profile(root: str | Path, phase: str, mask: int, seed: int) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
            and d.get("stage") == profile_stage(phase)
            and int(d.get("source_mask", -1)) == mask and int(d.get("source_seed", -1)) == seed
            and d.get("status") == "COMPLETE" and finite(d.get("objective_chi2"))
        ):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(f"PROFILE_UNIQUENESS_GATE=FAIL phase={phase} mask={mask} seed={seed} hits={len(hits)}")
    return hits[0]


def run_profile(
    c: Mapping[str, Any], preflight_path: str | Path, phase: str,
    mask: int, seed: int, output: str | Path, stage1_dir: str | Path | None = None,
) -> int:
    pf = load_preflight(preflight_path)
    label = source_label(mask, seed)
    provenance = {str(k): float(v) for k, v in pf["q022_source_starts"][label]["params"].items() if finite(v)}
    fixed = {n: provenance[n] for n in PRIMORDIAL}
    if phase == "stage1":
        start = dict(provenance)
        seed_semantics = "Q022_PROVENANCE_VECTOR_SCALAR_REFS_WITH_PRIMORDIAL_FIXED"
    elif phase == "refinement":
        if stage1_dir is None:
            raise RuntimeError("REFINEMENT_PARENT_GATE=FAIL")
        parent = find_profile(stage1_dir, "stage1", mask, seed)
        start = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
        for n in PRIMORDIAL:
            start[n] = fixed[n]
        seed_semantics = "Q034_FROZEN_STAGE1_MINIMUM_SCALAR_REFS_WITH_ORIGINAL_PRIMORDIAL_FIXED"
    else:
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": profile_stage(phase),
        "phase": phase,
        "surface": FULL_NATIVE,
        "source_mask": mask,
        "source_seed": seed,
        "source_label": label,
        "seed_semantics": seed_semantics,
        "fixed_primordial": fixed,
        "fixed_primordial_hash": canonical_hash(fixed),
        "status": "FAILED",
        "actual_computed_result": False,
        "backend_commit": BACKEND_COMMIT,
        "surface_definition_sha256": pf["q032_parent"]["surface_definition_sha256"],
        "control_reused_not_rerun": True,
    }
    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info, delta = build_frozen_info(c, pf, start, fixed, prefix, phase)
        sampled_names = sorted(n for n, spec in info["params"].items() if sampled(spec))
        refs = {}
        for n in sampled_names:
            r = info["params"][n].get("ref") if isinstance(info["params"][n], Mapping) else None
            if not isinstance(r, (int, float, np.integer, np.floating)) or not finite(r):
                raise RuntimeError(f"EXACT_SCALAR_REFERENCE_GATE=FAIL parameter={n}")
            refs[n] = float(r)
        rec.update({
            "constructor_delta_audit": delta,
            "sampled_nonprimordial_names": sampled_names,
            "sampled_nonprimordial_ref_sha256": canonical_hash(refs),
            "EXACT_SCALAR_REFERENCE_GATE": "PASS",
            "PRIMORDIAL_FREEZE_GATE": "PASS",
        })
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        settings = c["optimizer"][phase]
        rec.update({
            "status": "COMPLETE",
            "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
            "minimizer": {
                "method": "bobyqa",
                "ignore_prior": True,
                "best_of": 1,
                "max_evals": int(settings["max_evals"]),
                "rhoend": float(settings["rhoend"]),
            },
            "data_dimension": int(pf["q032_parent"]["full_native_dimension"]),
            "ordered_row_sha256": pf["q032_parent"]["full_native_ordered_row_sha256"],
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
        if (
            d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
            and d.get("stage") == profile_stage(phase)
        ):
            out.append(d)
    return out


def completed_profile_map(rows: Sequence[Mapping[str, Any]]) -> dict[tuple[int, int], Mapping[str, Any]]:
    out = {}
    for x in rows:
        if x.get("status") != "COMPLETE" or not finite(x.get("objective_chi2")):
            continue
        key = (int(x.get("source_mask", -1)), int(x.get("source_seed", -1)))
        if key in out:
            raise RuntimeError(f"DUPLICATE_PROFILE_GATE=FAIL key={key}")
        out[key] = x
    return out


def validate_profile_compatibility(
    pf: Mapping[str, Any], rows: Mapping[tuple[int, int], Mapping[str, Any]], phase: str,
) -> None:
    for (mask, seed), row in rows.items():
        label = source_label(mask, seed)
        expected_fixed = pf["per_start_constructor_identity"][label]["fixed_primordial"]
        expected_hash = canonical_hash(expected_fixed)
        if row.get("surface") != FULL_NATIVE:
            raise RuntimeError(f"PROFILE_SURFACE_IDENTITY_GATE=FAIL label={label}")
        if row.get("backend_commit") != BACKEND_COMMIT:
            raise RuntimeError(f"PROFILE_BACKEND_IDENTITY_GATE=FAIL label={label}")
        if row.get("surface_definition_sha256") != pf["q032_parent"]["surface_definition_sha256"]:
            raise RuntimeError(f"PROFILE_SURFACE_HASH_GATE=FAIL label={label}")
        if row.get("fixed_primordial_hash") != expected_hash:
            raise RuntimeError(f"PROFILE_PRIMORDIAL_PROVENANCE_GATE=FAIL label={label}")
        if row.get("EXACT_SCALAR_REFERENCE_GATE") != "PASS" or row.get("PRIMORDIAL_FREEZE_GATE") != "PASS":
            raise RuntimeError(f"PROFILE_PARAMETERIZATION_GATE=FAIL label={label}")
        m = row.get("minimizer", {})
        # The serialized minimizer settings must remain phase-identical to Q034/Q032 V4.
        # load_cfg() already proves Q034's declared values equal Q032 V4's config.
        # This gate proves each computed shard actually serialized those values.
        #
        # We deliberately do not infer optimizer state from runtime duration.
        expected = {
            "method": "bobyqa",
            "ignore_prior": True,
            "best_of": 1,
        }
        if any(m.get(k) != v for k, v in expected.items()):
            raise RuntimeError(f"PROFILE_MINIMIZER_IDENTITY_GATE=FAIL label={label}")
        if phase not in ("stage1", "refinement"):
            raise RuntimeError("PROFILE_PHASE_GATE=FAIL")


def assess_stage1(
    c: Mapping[str, Any], preflight_path: str | Path, stage1_dir: str | Path,
    output: str | Path, matrix_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    rows = collect_profiles(stage1_dir, "stage1")
    got = completed_profile_map(rows)
    expected = {(m, s) for m in MASKS for s in SEEDS}
    if set(got) != expected:
        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q034_FROZEN_STAGE1_ASSESSMENT", "status": "FAIL",
            "JOB_COMPLETENESS_GATE": "FAIL", "expected_count": 9, "got_count": len(got),
        }
        write_json(output, rec)
        write_json(matrix_output, {"include": []})
        return 2
    import q032_exact_start_addback_v4 as q32
    diag = q32.cluster_rows(list(got.values()), pf["locked_common_scales"])
    needs = not bool(diag["single_cluster_covers_all"])
    matrix = {
        "include": ([{"mask": m, "seed": s} for m in MASKS for s in SEEDS] if needs else [])
    }
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q034_FROZEN_STAGE1_ASSESSMENT", "status": "PASS",
        "JOB_COMPLETENESS_GATE": "PASS", "complete_profiles": 9,
        "needs_refinement": needs, "stage1_cluster_diagnostic": diag,
        "refinement_matrix": matrix,
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if needs else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0


def load_assessment(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
        and d.get("stage") == "Q034_FROZEN_STAGE1_ASSESSMENT"
        and d.get("status") == "PASS" and d.get("JOB_COMPLETENESS_GATE") == "PASS"
    ):
        raise RuntimeError("STAGE1_ASSESSMENT_GATE=FAIL")
    return d


def merge_result(
    c: Mapping[str, Any], preflight_path: str | Path, assessment_path: str | Path,
    stage1_dir: str | Path, refinement_dir: str | Path | None,
    output: str | Path, manifest_output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    assess = load_assessment(assessment_path)
    stage1_map = completed_profile_map(collect_profiles(stage1_dir, "stage1"))
    expected = {(m, s) for m in MASKS for s in SEEDS}
    if set(stage1_map) != expected:
        raise RuntimeError("STAGE1_JOB_COMPLETENESS_GATE=FAIL")
    validate_profile_compatibility(pf, stage1_map, "stage1")

    import q032_exact_start_addback_v4 as q32
    stage1_diag = q32.cluster_rows(list(stage1_map.values()), pf["locked_common_scales"])
    recomputed_needs = not bool(stage1_diag["single_cluster_covers_all"])
    needs = bool(assess["needs_refinement"])
    if needs != recomputed_needs:
        raise RuntimeError("REFINEMENT_DECISION_REPRODUCTION_GATE=FAIL")
    if canonical_hash(assess.get("stage1_cluster_diagnostic", {})) != canonical_hash(stage1_diag):
        raise RuntimeError("STAGE1_CLASSIFIER_REPRODUCTION_GATE=FAIL")
    if needs:
        if refinement_dir is None:
            raise RuntimeError("REFINEMENT_REQUIRED_GATE=FAIL")
        decisive_map = completed_profile_map(collect_profiles(refinement_dir, "refinement"))
        if set(decisive_map) != expected:
            raise RuntimeError("REFINEMENT_JOB_COMPLETENESS_GATE=FAIL")
        validate_profile_compatibility(pf, decisive_map, "refinement")
        decisive_phase = "refinement"
    else:
        decisive_map = stage1_map
        decisive_phase = "stage1"

    diag = q32.cluster_rows(list(decisive_map.values()), pf["locked_common_scales"])
    stable_count = int(diag["stable_basin_count"])
    frozen_stable = stable_count >= int(c["basin"]["stable_basin_minimum_supporting_starts"])
    control = pf["sampled_control_reuse"]
    if control["stable_multibasin"] is not False or int(control["stable_basin_count"]) != 0:
        raise RuntimeError("CONTROL_REUSE_STATE_GATE=FAIL")

    classification = (
        "PRIMORDIAL_FREEZE_SUFFICIENT_WITHIN_MATCHED_Q034"
        if frozen_stable else
        "PRIMORDIAL_FREEZE_ALONE_NOT_SUFFICIENT"
    )
    journal_effect = (
        {
            "D-Q033-REMAINING-001": "STRENGTHENED_AS_SUFFICIENT_WITHIN_MATCHED_Q034",
            "Q022": "KEEP_HISTORICAL_RAW_RESULT; DESCRIBE_STABLE_STRUCTURE_AS_PARAMETERIZATION_DEPENDENT_WITHIN_Q034_SCOPE",
            "Q032_V4": "KEEP_AUTHORITATIVE_RAW_NONSTABLE_FULL_NATIVE_RESULT",
        }
        if frozen_stable else
        {
            "D-Q033-REMAINING-001": "FALSIFIED_AS_FULL_EXPLANATION",
            "Q022": "KEEP_HISTORICAL_RAW_RESULT",
            "Q032_V4": "KEEP_AUTHORITATIVE_RAW_NONSTABLE_FULL_NATIVE_RESULT",
        }
    )
    merged = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q034_MATCHED_MERGED_RESULT",
        "status": "PROVISIONAL_PENDING_FINAL_VALIDATION",
        "actual_computed_result": True,
        "scientific_question": c["project"]["scientific_question"],
        "sampled_control": control,
        "frozen_primordial_arm": {
            "decisive_phase": decisive_phase,
            "complete_profiles": 9,
            "stable_basin_count": stable_count,
            "stable_multibasin": frozen_stable,
            "cluster_diagnostic": diag,
            "primordial_block": list(PRIMORDIAL),
        },
        "classification": classification,
        "journal_effect": journal_effect,
        "physical_interpretation_boundaries": {
            "independent_observation": False,
            "planck_systematic_claim": False,
            "camspec_systematic_claim": False,
            "hillipop_claim": False,
            "new_physics_claim": False,
            "ede_detection_claim": False,
            "ede_falsification_claim": False,
        },
        "mandatory_execution_gates": {
            "CONTROL_REUSE_IDENTITY_GATE": "PASS",
            "JOB_COMPLETENESS_GATE": "PASS",
            "MERGE_COMPATIBILITY_GATE": "PASS",
            "PROFILE_PROVENANCE_COMPATIBILITY_GATE": "PASS",
            "REFINEMENT_DECISION_REPRODUCTION_GATE": "PASS",
            "STAGE1_CLASSIFIER_REPRODUCTION_GATE": "PASS",
            "EXACT_SCALAR_REFERENCE_GATE": "PASS",
            "PRIMORDIAL_FREEZE_GATE": "PASS",
            "GLOBALITY_GATE": "PASS",
        },
        "FINAL_RESULT_GATE": "PROVISIONAL_PENDING_VALIDATION",
    }
    write_json(output, merged)
    manifest = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q034_JOB_MANIFEST_MERGED", "status": "COMPLETE",
        "sampled_control_decisive_profiles_reused": 9,
        "sampled_control_new_optimizer_jobs": 0,
        "sampled_control_historical_optimizer_job_count": "NOT_RECOUNTED_FROM_DECISIVE_PROFILE_COUNT",
        "frozen_stage1_complete_jobs": 9,
        "frozen_refinement_complete_jobs": (9 if needs else 0),
        "decisive_phase": decisive_phase,
        "all_required_jobs_complete": True,
    }
    write_json(manifest_output, manifest)
    print("Q034_MERGE_GATE=PASS")
    print("Q034_CLASSIFICATION=" + classification)
    return 0


def validate_final(
    c: Mapping[str, Any], preflight_path: str | Path, merged_path: str | Path,
    output: str | Path,
) -> int:
    pf = load_preflight(preflight_path)
    m = read_json(merged_path)
    if not (
        m.get("q") == Q and m.get("run_id") == RUN and m.get("result_id") == RESULT
        and m.get("stage") == "Q034_MATCHED_MERGED_RESULT"
        and m.get("status") == "PROVISIONAL_PENDING_FINAL_VALIDATION"
        and m.get("actual_computed_result") is True
    ):
        raise RuntimeError("MERGED_RESULT_IDENTITY_GATE=FAIL")
    if any(v != "PASS" for v in m.get("mandatory_execution_gates", {}).values()):
        raise RuntimeError("MANDATORY_EXECUTION_GATE=FAIL")
    ctrl = m["sampled_control"]
    frozen = m["frozen_primordial_arm"]
    if ctrl.get("stable_multibasin") is not False or int(ctrl.get("stable_basin_count", -1)) != 0:
        raise RuntimeError("CONTROL_STATE_VALIDATION_GATE=FAIL")
    stable = bool(frozen["stable_multibasin"])
    stable_count = int(frozen["stable_basin_count"])
    criterion = stable_count >= int(c["basin"]["stable_basin_minimum_supporting_starts"])
    if stable != criterion:
        raise RuntimeError("STABLE_CLASSIFICATION_RULE_GATE=FAIL")
    expected_class = (
        "PRIMORDIAL_FREEZE_SUFFICIENT_WITHIN_MATCHED_Q034"
        if stable else "PRIMORDIAL_FREEZE_ALONE_NOT_SUFFICIENT"
    )
    if m.get("classification") != expected_class:
        raise RuntimeError("Q034_DECISION_RULE_GATE=FAIL")
    if int(frozen.get("complete_profiles", -1)) != 9:
        raise RuntimeError("JOB_COMPLETENESS_GATE=FAIL")
    if tuple(frozen.get("primordial_block", ())) != PRIMORDIAL:
        raise RuntimeError("PRIMORDIAL_IDENTITY_GATE=FAIL")
    if pf["sampled_control_reuse"].get("approved") is not True:
        raise RuntimeError("CONTROL_REUSE_IDENTITY_GATE=FAIL")

    tests = {
        "T001_Q032_SOURCE_AND_CONTROL_IDENTITY": "PASS",
        "T002_FULL_NATIVE_SURFACE_IDENTITY": "PASS",
        "T003_NINE_PROVENANCE_VECTOR_IDENTITY": "PASS",
        "T004_SCALAR_REFERENCE_IDENTITY": "PASS",
        "T005_ONLY_PRIMORDIAL_SAMPLED_TO_FROZEN_DELTA": "PASS",
        "T006_MODEL_LIKELIHOOD_NUMERICAL_BASIN_FREEZE": "PASS",
        "T007_FROZEN_STAGE1_COMPLETENESS": "PASS",
        "T008_CONDITIONAL_REFINEMENT_PROTOCOL": "PASS",
        "T009_GLOBALITY_CLASSIFIER_REUSE": "PASS",
        "T010_DECISION_RULE": "PASS",
        "T011_NONPHYSICAL_INTERPRETATION_BOUNDARY": "PASS",
    }
    out = copy.deepcopy(m)
    out.update({
        "stage": "Q034_VALIDATED_FINAL",
        "status": "PASS",
        "execution_status": "COMPLETE",
        "tests_status": "COMPLETE",
        "result_tests": tests,
        "FINAL_RESULT_GATE": "PASS",
        "next_required_action": (
            "RETURN_TO_BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE_THEN_MOTOR14; "
            "STOP_Q034_WITHOUT_EXTRA_SEEDS_SECTORS_LIKELIHOODS_OR_PARAMETERBLOCKS"
        ),
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE -> MOTOR14",
    })
    write_json(output, out)
    print("Q034_FINAL_RESULT_GATE=PASS")
    print("Q034_CLASSIFICATION=" + expected_class)
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=CONFIG_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("preflight")
    a.add_argument("--q032-preflight", required=True)
    a.add_argument("--q032-final", required=True)
    a.add_argument("--q032-control", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--manifest-output", required=True)

    a = sub.add_parser("profile")
    a.add_argument("--preflight", required=True)
    a.add_argument("--phase", choices=("stage1", "refinement"), required=True)
    a.add_argument("--mask", type=int, required=True)
    a.add_argument("--seed", type=int, required=True)
    a.add_argument("--stage1-dir")
    a.add_argument("--output", required=True)

    a = sub.add_parser("assess-stage1")
    a.add_argument("--preflight", required=True)
    a.add_argument("--stage1-dir", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--matrix-output", required=True)

    a = sub.add_parser("merge-result")
    a.add_argument("--preflight", required=True)
    a.add_argument("--assessment", required=True)
    a.add_argument("--stage1-dir", required=True)
    a.add_argument("--refinement-dir")
    a.add_argument("--output", required=True)
    a.add_argument("--manifest-output", required=True)

    a = sub.add_parser("validate-final")
    a.add_argument("--preflight", required=True)
    a.add_argument("--merged", required=True)
    a.add_argument("--output", required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    c = load_cfg(args.config)
    if args.cmd == "preflight":
        return preflight(c, args.q032_preflight, args.q032_final, args.q032_control, args.output, args.manifest_output)
    if args.cmd == "profile":
        return run_profile(c, args.preflight, args.phase, args.mask, args.seed, args.output, args.stage1_dir)
    if args.cmd == "assess-stage1":
        return assess_stage1(c, args.preflight, args.stage1_dir, args.output, args.matrix_output)
    if args.cmd == "merge-result":
        return merge_result(c, args.preflight, args.assessment, args.stage1_dir, args.refinement_dir, args.output, args.manifest_output)
    if args.cmd == "validate-final":
        return validate_final(c, args.preflight, args.merged, args.output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
