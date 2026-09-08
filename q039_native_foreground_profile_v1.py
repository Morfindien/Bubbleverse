#!/usr/bin/env python3
"""Bubbleverse Q-039 — native foreground profile freedom intervention V1.

Scientific intervention
-----------------------
Freeze, within each likelihood implementation separately, the complete sampled
native TT foreground nuisance vector to the values from that implementation's
lowest-objective authoritative Q032 refinement endpoint. Re-optimize all nine
Q032 labels while preserving each likelihood's native foreground model form,
data vector, covariance/precision, calibration semantics, A_planck treatment,
exact TT common support, cosmological model and Q031 geometry scales.

This is NOT a cross-likelihood nuisance mapping and does NOT test whether the
CamSpec and HiLLiPoP foreground models are physically equivalent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import statistics
import subprocess
import sys
from itertools import combinations
from typing import Any, Mapping, Sequence

import numpy as np

Q = "Q-039"
PROGRAM_ID = "Q039-FGPROFILE-V1"
RUN_ID = "Q039-NATIVE-FOREGROUND-PROFILE-V1"
RESULT_ID = "R-Q039-EDE-NATIVE-FOREGROUND-PROFILE-001"
PARENT_Q039_RESULT_ID = "R-Q039-EDE-IMPLEMENTATION-BLOCK-INTERVENTION-001"
PARENT_Q039_SUCCESSFUL_RUN = 34161368438
Q032_RESULT_ID = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
Q032_GITHUB_RUN = 33994305721
Q032_EXECUTION_COMMIT = "4dc873a5e880d40858d831a3b421456728f0c032"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
COBAYA_VERSION = "3.5.6"
SUPPORT_HASH = "f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b"
SCALES_HASH = "732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6"
INTERVENTION = "NATIVE_FOREGROUND_PROFILE_FREEDOM_OFF"
LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
IMPLEMENTATIONS = ("camspec", "hillipop")
COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
SCALES = {
    "omega_b": 3.644915744246274e-05,
    "omega_cdm": 2.9761589951235456e-04,
    "fEDE": 1.0851930861718734e-03,
    "log10z_c": 3.666125981785351e-02,
    "thetai_scf": 1.2826810796868315e-02,
    "H0": 2.253286448991929e-01,
    "A_planck": 3.7111561222435974e-04,
}
THRESHOLD = 0.10
BASELINE = {
    "matched_median": 2.9317906965863507,
    "centroid": 0.8311487237190059,
    "pairwise_median_drift": 1.6367910228418985,
}
EXPECTED_CAMSPEC_FOREGROUND = (
    "amp_143", "amp_217", "amp_143x217", "n_143", "n_217", "n_143x217"
)
EXPECTED_HILLIPOP_FOREGROUND = (
    "Aradio", "Adusty", "AdustT", "beta_dustT", "Acib", "beta_cib", "Atsz", "Aksz", "xi"
)
PROHIBITED_FOREGROUND_NAMES = {"A_planck", "cal0", "cal2", "cal100A", "cal100B", "cal143A", "cal143B", "cal217A", "cal217B"}


class SoftStop(Exception):
    pass


def _alarm(_sig: int, _frame: Any) -> None:
    raise SoftStop("Q039 foreground-profile soft stop")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return obj


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_head(path: str | Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def resolve_q032_config_path(parent_root: str | Path) -> Path:
    root = Path(parent_root).resolve()
    cfg = (root / "q032_planck_tt3pair_bridge_v2_config.yml").resolve()
    try:
        cfg.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("Q032_CONFIG_CONTAINMENT_GATE=FAIL") from exc
    if not cfg.is_file():
        raise RuntimeError(f"Q032_CONFIG_PATH_GATE=FAIL path={cfg}")
    return cfg


def load_q032(parent_root: str | Path):
    root = Path(parent_root).resolve()
    if git_head(root) != Q032_EXECUTION_COMMIT:
        raise RuntimeError("Q032_EXECUTION_COMMIT_GATE=FAIL")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import q032_planck_tt3pair_bridge_v2 as q32  # type: ignore
    if q32.Q != "Q-032" or q32.RESULT != Q032_RESULT_ID:
        raise RuntimeError("Q032_PARENT_IDENTITY_GATE=FAIL")
    return q32


def find_parent_file(root: str | Path, implementation: str, mask: int, seed: int) -> Path:
    hits: list[Path] = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == "Q-032"
            and d.get("stage") == "Q032_REFINEMENT"
            and d.get("implementation") == implementation
            and int(d.get("source_mask", -1)) == int(mask)
            and int(d.get("source_seed", -1)) == int(seed)
        ):
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(
            f"Q032_PARENT_UNIQUENESS_GATE=FAIL impl={implementation} mask={mask} seed={seed} hits={len(hits)}"
        )
    return hits[0]


def validate_parent_record(d: Mapping[str, Any], implementation: str, mask: int, seed: int) -> None:
    label = f"M{mask}-S{seed}"
    expected = {
        "q": "Q-032",
        "run_id": "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2",
        "result_id": Q032_RESULT_ID,
        "stage": "Q032_REFINEMENT",
        "phase": "refinement",
        "implementation": implementation,
        "source_mask": int(mask),
        "source_seed": int(seed),
        "source_label": label,
        "support_sha256": SUPPORT_HASH,
        "status": "COMPLETE",
        "actual_computed_result": True,
    }
    for k, v in expected.items():
        if d.get(k) != v:
            raise RuntimeError(f"Q032_PARENT_PROFILE_GATE=FAIL {k} got={d.get(k)!r} expected={v!r}")
    if d.get("backend_commit") != BACKEND_COMMIT:
        raise RuntimeError("Q032_PARENT_BACKEND_GATE=FAIL")
    if implementation == "hillipop" and d.get("hillipop_commit") != HILLIPOP_COMMIT:
        raise RuntimeError("Q032_PARENT_HILLIPOP_GATE=FAIL")
    if not finite(d.get("objective_chi2")):
        raise RuntimeError("Q032_PARENT_OBJECTIVE_GATE=FAIL")
    minimum = d.get("minimum")
    if not isinstance(minimum, Mapping):
        raise RuntimeError("Q032_PARENT_MINIMUM_GATE=FAIL")
    for name in COORDS:
        if name not in minimum or not finite(minimum[name]):
            raise RuntimeError(f"Q032_PARENT_COORDINATE_GATE=FAIL {name}")


def load_parent(root: str | Path, implementation: str, mask: int, seed: int) -> tuple[dict[str, Any], Path]:
    p = find_parent_file(root, implementation, mask, seed)
    d = read_json(p)
    validate_parent_record(d, implementation, mask, seed)
    return d, p


def start_from_parent(parent: Mapping[str, Any]) -> dict[str, float]:
    return {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}


def sampled_yaml_names(path: Path) -> tuple[str, ...]:
    import yaml  # type: ignore
    d = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(d, Mapping):
        raise RuntimeError(f"NATIVE_PARAM_SCHEMA_GATE=FAIL path={path}")
    names = []
    for name, spec in d.items():
        if isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping):
            names.append(str(name))
    return tuple(names)


def native_foreground_names(implementation: str) -> tuple[tuple[str, ...], dict[str, Any]]:
    if implementation == "camspec":
        import importlib.metadata as metadata
        import cobaya  # type: ignore
        version = metadata.version("cobaya")
        if version != COBAYA_VERSION:
            raise RuntimeError(f"CAMSPEC_COBAYA_VERSION_GATE=FAIL got={version}")
        path = Path(cobaya.__file__).resolve().parent / "likelihoods" / "planck_NPIPE_highl_CamSpec" / "params_TT_CamSpec.yaml"
        names = sampled_yaml_names(path)
        expected = EXPECTED_CAMSPEC_FOREGROUND
    elif implementation == "hillipop":
        import planck_2020_hillipop  # type: ignore
        path = Path(planck_2020_hillipop.__file__).resolve().parent / "params_TT.yaml"
        names = sampled_yaml_names(path)
        expected = EXPECTED_HILLIPOP_FOREGROUND
    else:
        raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
    if tuple(names) != tuple(expected):
        raise RuntimeError(
            f"NATIVE_FOREGROUND_PARAMETER_SET_GATE=FAIL impl={implementation} runtime={names} expected={expected}"
        )
    if set(names).intersection(PROHIBITED_FOREGROUND_NAMES):
        raise RuntimeError("FOREGROUND_CALIBRATION_SEPARATION_GATE=FAIL")
    return tuple(names), {
        "implementation": implementation,
        "schema_file": str(path),
        "schema_sha256": sha256_file(path),
        "sampled_native_tt_foreground_parameters": list(names),
    }


def metric(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    terms = []
    for name in COORDS:
        if not (finite(a.get(name)) and finite(b.get(name))):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coordinate={name}")
        terms.append((float(a[name]) - float(b[name])) / SCALES[name])
    return float(math.sqrt(sum(x * x for x in terms) / len(terms)))


def calculate_metrics(rows: Mapping[str, Mapping[str, Mapping[str, float]]], labels: Sequence[str]) -> dict[str, Any]:
    labels = tuple(labels)
    if len(labels) < 2:
        raise RuntimeError("GEOMETRY_LABEL_COUNT_GATE=FAIL")
    c = rows["camspec"]
    h = rows["hillipop"]
    matched = {label: metric(c[label], h[label]) for label in labels}
    cc = {name: statistics.mean(float(c[l][name]) for l in labels) for name in COORDS}
    hc = {name: statistics.mean(float(h[l][name]) for l in labels) for name in COORDS}
    drift: dict[str, float] = {}
    for a, b in combinations(labels, 2):
        drift[f"{a}|{b}"] = abs(metric(c[a], c[b]) - metric(h[a], h[b]))
    return {
        "labels": list(labels),
        "matched_endpoint_rms": matched,
        "matched_median": float(statistics.median(matched.values())),
        "matched_max": float(max(matched.values())),
        "centroid": metric(cc, hc),
        "pairwise_absolute_drifts": drift,
        "pairwise_median_drift": float(statistics.median(drift.values())),
        "pairwise_max_drift": float(max(drift.values())),
    }


def sufficient(metrics: Mapping[str, Any]) -> bool:
    return (
        float(metrics["matched_median"]) <= THRESHOLD
        and float(metrics["centroid"]) <= THRESHOLD
        and float(metrics["pairwise_median_drift"]) <= THRESHOLD
    )


def validate_parent(args: argparse.Namespace) -> int:
    rows: dict[str, dict[str, dict[str, float]]] = {k: {} for k in IMPLEMENTATIONS}
    provenance = {}
    for implementation in IMPLEMENTATIONS:
        for m in (3, 6, 7):
            for s in (0, 1, 2):
                d, p = load_parent(args.parent_dir, implementation, m, s)
                label = f"M{m}-S{s}"
                rows[implementation][label] = {name: float(d["minimum"][name]) for name in COORDS}
                provenance[f"{implementation}:{label}"] = {"path": str(p), "sha256": sha256_file(p)}
    metrics = calculate_metrics(rows, LABELS)
    deltas = {
        "matched_median": abs(metrics["matched_median"] - BASELINE["matched_median"]),
        "centroid": abs(metrics["centroid"] - BASELINE["centroid"]),
        "pairwise_median_drift": abs(metrics["pairwise_median_drift"] - BASELINE["pairwise_median_drift"]),
    }
    if any(v > 1e-12 for v in deltas.values()):
        raise RuntimeError(f"Q037_BASELINE_REPRODUCTION_GATE=FAIL deltas={deltas}")
    write_json(args.output, {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "stage": "PARENT_INPUT_GATE",
        "status": "PASS", "baseline_reproduced": True, "metrics": metrics, "deltas": deltas,
        "parent_provenance": provenance, "support_sha256": SUPPORT_HASH, "scales_sha256": SCALES_HASH,
    })
    print("Q039_FGPROFILE_PARENT_INPUT_GATE=PASS")
    return 0


def load_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
        and d.get("stage") == "Q032_PREFLIGHT_SEALED"
        and d.get("status") == "PASS"
        and d.get("support_sha256") == SUPPORT_HASH
    ):
        raise RuntimeError("Q032_SEALED_PREFLIGHT_GATE=FAIL")
    return d


def prepare_reference(args: argparse.Namespace) -> int:
    # Native schemas are derived from the pinned runtime, not from the handoff text.
    refs: dict[str, Any] = {}
    for implementation in IMPLEMENTATIONS:
        names, schema = native_foreground_names(implementation)
        candidates = []
        for m in (3, 6, 7):
            for s in (0, 1, 2):
                d, p = load_parent(args.parent_dir, implementation, m, s)
                candidates.append((float(d["objective_chi2"]), f"M{m}-S{s}", d, p))
        candidates.sort(key=lambda x: (x[0], x[1]))
        objective, label, chosen, path = candidates[0]
        values: dict[str, float] = {}
        for name in names:
            if name not in chosen["minimum"] or not finite(chosen["minimum"][name]):
                raise RuntimeError(f"FOREGROUND_REFERENCE_COORDINATE_GATE=FAIL impl={implementation} name={name}")
            values[name] = float(chosen["minimum"][name])
        refs[implementation] = {
            "selection_semantics": "LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION_ONLY",
            "cross_likelihood_objective_comparison_performed": False,
            "source_label": label,
            "source_mask": int(chosen["source_mask"]),
            "source_seed": int(chosen["source_seed"]),
            "source_objective_chi2": float(objective),
            "source_parent_file": str(path),
            "source_parent_sha256": sha256_file(path),
            "schema": schema,
            "foreground_parameter_names": list(names),
            "foreground_fixed_values": values,
        }
    write_json(args.output, {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "FOREGROUND_REFERENCE_SELECTION", "status": "PASS", "intervention": INTERVENTION,
        "references": refs,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_objective_sum_performed": False,
    })
    print("Q039_FGPROFILE_REFERENCE_GATE=PASS")
    return 0


def load_reference(path: str | Path, implementation: str) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("run_id") == RUN_ID
        and d.get("stage") == "FOREGROUND_REFERENCE_SELECTION" and d.get("status") == "PASS"
        and d.get("intervention") == INTERVENTION
    ):
        raise RuntimeError("FOREGROUND_REFERENCE_IDENTITY_GATE=FAIL")
    ref = d.get("references", {}).get(implementation)
    if not isinstance(ref, Mapping):
        raise RuntimeError("FOREGROUND_REFERENCE_IMPLEMENTATION_GATE=FAIL")
    names, _ = native_foreground_names(implementation)
    if tuple(ref.get("foreground_parameter_names", [])) != names:
        raise RuntimeError("FOREGROUND_REFERENCE_SCHEMA_GATE=FAIL")
    vals = ref.get("foreground_fixed_values")
    if not isinstance(vals, Mapping) or set(vals) != set(names) or not all(finite(vals[n]) for n in names):
        raise RuntimeError("FOREGROUND_REFERENCE_VALUES_GATE=FAIL")
    return dict(ref)


def build_intervened_info(
    q32: Any, cfg: Mapping[str, Any], parent: Mapping[str, Any], implementation: str,
    prefix: Path, support: Mapping[str, Any], reference: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    start = start_from_parent(parent)
    if implementation == "camspec":
        info = q32.build_camspec_info(cfg, start, prefix, "refinement", support)
    elif implementation == "hillipop":
        info = q32.build_hillipop_info(cfg, start, prefix, "refinement")
    else:
        raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
    params = info.get("params")
    if not isinstance(params, dict):
        raise RuntimeError("INFO_PARAMS_GATE=FAIL")
    before_ap = json.dumps(params.get("A_planck"), sort_keys=True, default=str)
    fixed = reference["foreground_fixed_values"]
    names = tuple(reference["foreground_parameter_names"])
    for name in names:
        if name in PROHIBITED_FOREGROUND_NAMES:
            raise RuntimeError("FOREGROUND_CALIBRATION_SEPARATION_GATE=FAIL")
        params[name] = float(fixed[name])
    after_ap = json.dumps(params.get("A_planck"), sort_keys=True, default=str)
    if before_ap != after_ap:
        raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL")
    intervention_meta = {
        "intervention": INTERVENTION,
        "implementation": implementation,
        "foreground_parameter_names": list(names),
        "foreground_fixed_values": {n: float(fixed[n]) for n in names},
        "reference_source_label": reference["source_label"],
        "reference_parent_sha256": reference["source_parent_sha256"],
        "A_planck_preserved": True,
        "calibration_intervention_performed": False,
        "precision_intervention_performed": False,
        "foreground_model_form_changed": False,
        "data_vector_changed": False,
        "covariance_or_precision_changed_by_q039_intervention": False,
        "cross_implementation_nuisance_mapping": False,
    }
    return info, intervention_meta


def runtime_preflight(args: argparse.Namespace) -> int:
    q32 = load_q032(args.q032_parent_root)
    cfg = q32.load_cfg(resolve_q032_config_path(args.q032_parent_root))
    pf = load_preflight(args.preflight)
    support = pf["support_lock"]
    parent, _ = load_parent(args.parent_dir, args.implementation, args.mask, args.seed)
    reference = load_reference(args.reference, args.implementation)
    patch = None
    if args.implementation == "hillipop":
        if not args.hlp_matrix or not args.hlp_meta:
            raise RuntimeError("HILLIPOP_RESTRICTED_PRECISION_INPUT_GATE=FAIL")
        patch = q32.install_hillipop_patch(args.hlp_matrix, args.hlp_meta, support, cfg)
    prefix = Path(args.output).with_suffix("")
    info, meta = build_intervened_info(q32, cfg, parent, args.implementation, prefix, support, reference)
    model = None
    try:
        model = q32.create_model(info)
        logpost, _ = q32.evaluate_model_once(model, info, start_from_parent(parent))
        if not finite(logpost):
            raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL")
    finally:
        try:
            if model is not None:
                model.close()
        except Exception:
            pass
    write_json(args.output, {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "stage": "RUNTIME_PREFLIGHT",
        "status": "PASS", "implementation": args.implementation, "source_label": f"M{args.mask}-S{args.seed}",
        "intervention": meta, "q032_runtime_patch": patch, "finite_logposterior": float(logpost),
        "optimizer_started": False, "actual_computed_result": False,
        "TECHNICAL_PREFLIGHT_ONLY_NOT_SCIENTIFIC_EVIDENCE": True,
    })
    print(f"Q039_FGPROFILE_RUNTIME_PREFLIGHT_GATE=PASS impl={args.implementation}")
    return 0


def run_profile(args: argparse.Namespace) -> int:
    q32 = load_q032(args.q032_parent_root)
    cfg = q32.load_cfg(resolve_q032_config_path(args.q032_parent_root))
    pf = load_preflight(args.preflight)
    support = pf["support_lock"]
    parent, parent_path = load_parent(args.parent_dir, args.implementation, args.mask, args.seed)
    reference = load_reference(args.reference, args.implementation)
    patch = None
    if args.implementation == "hillipop":
        if not args.hlp_matrix or not args.hlp_meta:
            raise RuntimeError("HILLIPOP_RESTRICTED_PRECISION_INPUT_GATE=FAIL")
        patch = q32.install_hillipop_patch(args.hlp_matrix, args.hlp_meta, support, cfg)
    prefix = Path(args.output).with_suffix("")
    info, intervention_meta = build_intervened_info(
        q32, cfg, parent, args.implementation, prefix, support, reference
    )
    rec: dict[str, Any] = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "FOREGROUND_PROFILE", "status": "FAILED", "actual_computed_result": False,
        "implementation": args.implementation, "source_mask": int(args.mask), "source_seed": int(args.seed),
        "source_label": f"M{args.mask}-S{args.seed}", "intervention": intervention_meta,
        "parent_q032_file": str(parent_path), "parent_q032_sha256": sha256_file(parent_path),
        "support_sha256": SUPPORT_HASH, "backend_commit": BACKEND_COMMIT,
        "hillipop_commit": HILLIPOP_COMMIT if args.implementation == "hillipop" else None,
        "q032_runtime_patch": patch,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_objective_sum_performed": False,
    }
    sampler = None
    old_handler = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(300 * 60)
    try:
        from cobaya.run import run as cobaya_run  # type: ignore
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19  # type: ignore
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        minimum = {str(k): float(v) if finite(v) else v for k, v in row.items()}
        for coord in COORDS:
            if coord not in minimum or not finite(minimum[coord]):
                raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coord={coord}")
        harvested_fixed_parameter_checks = {}
        for name, value in intervention_meta["foreground_fixed_values"].items():
            if name in minimum and finite(minimum[name]):
                if abs(float(minimum[name]) - float(value)) > 1e-10:
                    raise RuntimeError(f"FOREGROUND_LOCK_APPLICATION_GATE=FAIL name={name}")
                harvested_fixed_parameter_checks[name] = "PRESENT_AND_MATCHED"
            else:
                # Cobaya minimum products need not serialize fixed parameters.
                # The scientific application gate is the scalar top-level param
                # override validated before optimizer construction.
                harvested_fixed_parameter_checks[name] = "FIXED_PARAMETER_NOT_SERIALIZED_IN_MINIMUM"
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]), "minimum": minimum,
            "harvested_minimum_path": source,
            "minimizer": {"method": "bobyqa", "ignore_prior": True, "best_of": 1, "max_evals": 300000, "rhoend": 1e-5},
            "FOREGROUND_LOCK_APPLICATION_GATE": "PASS",
            "harvested_fixed_parameter_checks": harvested_fixed_parameter_checks,
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD", "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
        write_json(args.output, rec)
    return 0 if rec.get("status") == "COMPLETE" else 2


def collect_profiles(root: str | Path, reference: Mapping[str, Any]) -> tuple[dict[str, dict[str, dict[str, float]]], list[dict[str, Any]]]:
    rows: dict[str, dict[str, dict[str, float]]] = {k: {} for k in IMPLEMENTATIONS}
    records: list[dict[str, Any]] = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("stage") == "FOREGROUND_PROFILE":
            records.append(d)
    expected = {(i, l) for i in IMPLEMENTATIONS for l in LABELS}
    got = {(str(d.get("implementation")), str(d.get("source_label"))) for d in records if d.get("status") == "COMPLETE"}
    if got != expected or len(records) != 18:
        raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL expected=18 complete={len(got)} records={len(records)}")
    for d in records:
        impl = str(d["implementation"])
        label = str(d["source_label"])
        if d.get("status") != "COMPLETE" or d.get("FOREGROUND_LOCK_APPLICATION_GATE") != "PASS":
            raise RuntimeError("PROFILE_STATUS_GATE=FAIL")
        if d.get("support_sha256") != SUPPORT_HASH or d.get("backend_commit") != BACKEND_COMMIT:
            raise RuntimeError("PROFILE_PROVENANCE_GATE=FAIL")
        if impl == "hillipop" and d.get("hillipop_commit") != HILLIPOP_COMMIT:
            raise RuntimeError("PROFILE_HILLIPOP_COMMIT_GATE=FAIL")
        ref = reference["references"][impl]
        meta = d.get("intervention", {})
        if meta.get("foreground_fixed_values") != ref.get("foreground_fixed_values"):
            raise RuntimeError("FOREGROUND_REFERENCE_REUSE_GATE=FAIL")
        if meta.get("calibration_intervention_performed") is not False or meta.get("precision_intervention_performed") is not False:
            raise RuntimeError("SINGLE_BLOCK_ISOLATION_GATE=FAIL")
        minimum = d.get("minimum", {})
        rows[impl][label] = {name: float(minimum[name]) for name in COORDS}
    return rows, records


def assess(args: argparse.Namespace) -> int:
    reference = read_json(args.reference)
    if reference.get("stage") != "FOREGROUND_REFERENCE_SELECTION" or reference.get("status") != "PASS":
        raise RuntimeError("FOREGROUND_REFERENCE_GATE=FAIL")
    rows, records = collect_profiles(args.profile_dir, reference)
    full = calculate_metrics(rows, LABELS)
    loo = {}
    for omitted in LABELS:
        labels = tuple(x for x in LABELS if x != omitted)
        mm = calculate_metrics(rows, labels)
        loo[omitted] = {"metrics": mm, "sufficient": sufficient(mm)}
    full_sufficient = sufficient(full)
    all_loo_sufficient = all(x["sufficient"] for x in loo.values())
    is_sufficient = bool(full_sufficient and all_loo_sufficient)
    classification = (
        "SINGLE-BLOCK_NATIVE_FOREGROUND_PROFILE_FREEDOM_SUFFICIENT"
        if is_sufficient
        else "NATIVE_FOREGROUND_PROFILE_FREEDOM_REJECTED_AS_SUFFICIENT"
    )
    result = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "parent_q039_result_id": PARENT_Q039_RESULT_ID, "parent_q039_successful_run": PARENT_Q039_SUCCESSFUL_RUN,
        "stage": "PROVISIONAL_FINAL", "execution_status": "COMPLETE", "tests_status": "PENDING_EXTERNAL_TEST_SCRIPT",
        "final_result_gate": "PROVISIONAL", "FINAL_RESULT_GATE": "PROVISIONAL",
        "intervention": INTERVENTION, "classification": classification, "sufficient": is_sufficient,
        "full_sample": {"metrics": full, "sufficient": full_sufficient},
        "leave_one_label_out": loo, "leave_one_label_out_sufficient_count": sum(int(x["sufficient"]) for x in loo.values()),
        "threshold": THRESHOLD, "baseline_q037": BASELINE,
        "profile_count": len(records), "expected_profile_count": 18,
        "reference_selection": reference,
        "comparability": {
            "NATIVE_FOREGROUND_PROFILE_FREEDOM": "COMPARABLE_TESTED",
            "FULL_FOREGROUND_MODEL_HARMONIZATION": "NOT_COMPARABLE",
            "CORE_LIKELIHOOD_CONSTRUCTION": "NOT_COMPARABLE_AS_SINGLE_NATIVE_BLOCK",
        },
        "previous_q039_results_preserved": {
            "RELATIVE_CALIBRATION_NEUTRAL": "REJECTED_AS_SUFFICIENT",
            "OFFDIAGONAL_PRECISION_COUPLING_OFF": "REJECTED_AS_SUFFICIENT",
            "CALIBRATION_PLUS_PRECISION": "REJECTED_AS_SUFFICIENT",
            "authoritative_run": PARENT_Q039_SUCCESSFUL_RUN,
        },
        "interpretation_limits": [
            "This tests native foreground nuisance profiling freedom, not equivalence of the full foreground model forms.",
            "A sufficient result would not by itself establish physical foreground contamination or a Planck systematic.",
            "A failed result does not establish that foregrounds have no role in the broader CamSpec/HiLLiPoP difference.",
            "CamSpec and HiLLiPoP remain overlapping analyses of the same broad Planck PR4/NPIPE sky data family.",
        ],
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_objective_sum_performed": False,
        "journal_effect_if_pass": "NATIVE_FOREGROUND_PROFILE_FREEDOM_SUFFICIENT_SINGLE_BLOCK_UNDER_TESTED_INTERVENTION",
        "journal_effect_if_fail": "NATIVE_FOREGROUND_PROFILE_FREEDOM_REJECTED_AS_SUFFICIENT_UNDER_TESTED_INTERVENTION",
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    }
    write_json(args.output, result)
    print(f"Q039_FGPROFILE_PROVISIONAL_CLASSIFICATION={classification}")
    return 0


def seal(args: argparse.Namespace) -> int:
    d = read_json(args.provisional)
    t = read_json(args.tests)
    if not (
        d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("final_result_gate") == "PROVISIONAL"
        and t.get("q") == Q and t.get("program_id") == PROGRAM_ID and t.get("status") == "PASS"
        and t.get("FINAL_RESULT_GATE") == "PASS"
    ):
        raise RuntimeError("SEAL_INPUT_GATE=FAIL")
    out = dict(d)
    out["stage"] = "SEALED_FINAL"
    out["tests_status"] = "COMPLETE"
    out["final_result_gate"] = "PASS"
    out["FINAL_RESULT_GATE"] = "PASS"
    out["sealed"] = True
    out["result_test_record_sha256"] = sha256_file(args.tests)
    write_json(args.output, out)
    if args.handoff:
        write_json(args.handoff, {
            "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
            "status": "SEALED_RESULT_READY_FOR_INGESTION", "classification": out["classification"],
            "sufficient": out["sufficient"], "FINAL_RESULT_GATE": "PASS",
            "sources": ["K-044", "K-045/K-052", "K-046", "K-049", "K-053", "K-054", "CAMSPEC_2021_ID_UNRESOLVED"],
            "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
            "unresolved_issue": "C-036-IMPL" if not out["sufficient"] else "PHYSICAL_CAUSALITY_NOT_ESTABLISHED",
        })
    print("Q039_FGPROFILE_FINAL_RESULT_GATE=PASS")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sp = p.add_subparsers(dest="command", required=True)

    a = sp.add_parser("validate-parent")
    a.add_argument("--parent-dir", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=validate_parent)

    a = sp.add_parser("prepare-reference")
    a.add_argument("--parent-dir", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=prepare_reference)

    for cmd, fn in (("runtime-preflight", runtime_preflight), ("profile", run_profile)):
        a = sp.add_parser(cmd)
        a.add_argument("--q032-parent-root", required=True)
        a.add_argument("--preflight", required=True)
        a.add_argument("--parent-dir", required=True)
        a.add_argument("--reference", required=True)
        a.add_argument("--implementation", choices=IMPLEMENTATIONS, required=True)
        a.add_argument("--mask", type=int, choices=(3, 6, 7), required=True)
        a.add_argument("--seed", type=int, choices=(0, 1, 2), required=True)
        a.add_argument("--hlp-matrix")
        a.add_argument("--hlp-meta")
        a.add_argument("--output", required=True)
        a.set_defaults(func=fn)

    a = sp.add_parser("assess")
    a.add_argument("--profile-dir", required=True)
    a.add_argument("--reference", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=assess)

    a = sp.add_parser("seal")
    a.add_argument("--provisional", required=True)
    a.add_argument("--tests", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--handoff")
    a.set_defaults(func=seal)
    return p


def main() -> int:
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
