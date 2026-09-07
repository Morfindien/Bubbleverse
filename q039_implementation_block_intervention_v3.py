#!/usr/bin/env python3
"""Bubbleverse Q039 implementation-block intervention experiment.

This program deliberately imports the frozen Q032 implementation from a detached
worktree at Q032_EXECUTION_COMMIT. It never maps CamSpec nuisance parameters onto
HiLLiPoP nuisance parameters. Interventions are defined at block-operation level.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
from typing import Any, Mapping, Sequence

import numpy as np

Q = "Q-039"
PROGRAM_ID = "Q039-IMPLBLOCK-V3"
RUN_ID = "Q039-IMPLEMENTATION-BLOCK-INTERVENTION-V3"
RESULT_ID = "R-Q039-EDE-IMPLEMENTATION-BLOCK-INTERVENTION-001"
SCIENTIFIC_PREREG_PROGRAM_ID = "Q039-IMPLBLOCK-V1"
TECHNICAL_RECOVERY_VERSION = "V3"
Q032_RESULT_ID = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
Q032_GITHUB_RUN = 33994305721
Q032_EXECUTION_COMMIT = "4dc873a5e880d40858d831a3b421456728f0c032"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
SUPPORT_HASH = "f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b"
SCALES_HASH = "732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6"
COORDS = ["omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck"]
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
LABELS = [f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2)]
IMPLEMENTATIONS = ("camspec", "hillipop")
SINGLE_ARMS = ("RELATIVE_CALIBRATION_NEUTRAL", "OFFDIAGONAL_PRECISION_COUPLING_OFF")
COUPLED_ARM = "CALIBRATION_PLUS_PRECISION"
ALL_ARMS = SINGLE_ARMS + (COUPLED_ARM,)
BASELINE = {
    "matched_median": 2.9317906965863507,
    "centroid": 0.8311487237190059,
    "pairwise_median_drift": 1.6367910228418985,
}

class SoftStop(Exception):
    pass


def _alarm(_sig: int, _frame: Any) -> None:
    raise SoftStop("Q039 soft runtime stop")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha256_array(a: np.ndarray) -> str:
    arr = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(arr.shape).encode())
    h.update(arr.dtype.str.encode())
    h.update(arr.tobytes())
    return h.hexdigest()


def git_head(path: str | Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def load_q032(parent_root: str | Path):
    root = Path(parent_root).resolve()
    if git_head(root) != Q032_EXECUTION_COMMIT:
        raise RuntimeError("Q032_EXECUTION_COMMIT_GATE=FAIL")
    sys.path.insert(0, str(root))
    import q032_planck_tt3pair_bridge_v2 as q32  # type: ignore
    if q32.Q != "Q-032" or q32.RESULT != Q032_RESULT_ID:
        raise RuntimeError("Q032_PARENT_IDENTITY_GATE=FAIL")
    return q32

def resolve_q032_config_path(parent_root: str | Path) -> Path:
    """Resolve the frozen Q032 config exactly once as an absolute path."""
    root = Path(parent_root).resolve()
    cfg = (root / "q032_planck_tt3pair_bridge_v2_config.yml").resolve()
    try:
        cfg.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("Q032_CONFIG_CONTAINMENT_GATE=FAIL") from exc
    if not cfg.is_file():
        raise RuntimeError(f"Q032_CONFIG_PATH_GATE=FAIL path={cfg}")
    return cfg


def find_single_json(root: str | Path, predicate) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if predicate(d):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(f"INPUT_UNIQUENESS_GATE=FAIL hits={len(hits)} root={root}")
    return hits[0]


def validate_parent_profile(d: Mapping[str, Any], implementation: str, mask: int, seed: int) -> dict[str, Any]:
    label = f"M{mask}-S{seed}"
    required = {
        "q": "Q-032",
        "run_id": "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2",
        "result_id": Q032_RESULT_ID,
        "stage": "Q032_REFINEMENT",
        "implementation": implementation,
        "source_mask": mask,
        "source_seed": seed,
        "source_label": label,
        "support_sha256": SUPPORT_HASH,
        "status": "COMPLETE",
    }
    for k, v in required.items():
        if d.get(k) != v:
            raise RuntimeError(f"Q032_PARENT_PROFILE_GATE=FAIL {k} got={d.get(k)!r} expected={v!r}")
    minimum = d.get("minimum")
    if not isinstance(minimum, dict):
        raise RuntimeError("Q032_PARENT_MINIMUM_GATE=FAIL")
    for c in COORDS:
        if c not in minimum or not finite(minimum[c]):
            raise RuntimeError(f"Q032_PARENT_MINIMUM_GATE=FAIL coordinate={c}")
    return dict(d)


def load_parent_profile(root: str | Path, implementation: str, mask: int, seed: int) -> dict[str, Any]:
    return validate_parent_profile(
        find_single_json(
            root,
            lambda d: d.get("q") == "Q-032"
            and d.get("stage") == "Q032_REFINEMENT"
            and d.get("implementation") == implementation
            and int(d.get("source_mask", -1)) == mask
            and int(d.get("source_seed", -1)) == seed,
        ),
        implementation,
        mask,
        seed,
    )


def minimum_start(parent: Mapping[str, Any]) -> dict[str, float]:
    return {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}


def _param_is_free(spec: Any) -> bool:
    return isinstance(spec, dict) and ("prior" in spec or "ref" in spec) and not ("value" in spec and not isinstance(spec.get("value"), str))


def apply_calibration_neutral(info: dict[str, Any], implementation: str) -> dict[str, Any]:
    params = info.get("params")
    if not isinstance(params, dict):
        raise RuntimeError("CALIBRATION_BLOCK_GATE=FAIL params")
    before_ap = copy.deepcopy(params.get("A_planck"))
    changed: list[str] = []
    already_neutral: list[str] = []
    if implementation == "camspec":
        # Q032 CamSpec TT already fixes its relative calibration factors to unity.
        for name in ("cal0", "cal2"):
            if name not in params:
                raise RuntimeError(f"CALIBRATION_BLOCK_GATE=FAIL missing_{name}")
            old = params[name]
            if isinstance(old, dict) and _param_is_free(old):
                raise RuntimeError(f"CAMSPEC_RELATIVE_CALIBRATION_BASELINE_GATE=FAIL free_{name}")
            try:
                val = float(old.get("value", old) if isinstance(old, dict) else old)
            except Exception as exc:
                raise RuntimeError(f"CAMSPEC_RELATIVE_CALIBRATION_BASELINE_GATE=FAIL {name}") from exc
            if abs(val - 1.0) > 1e-12:
                raise RuntimeError(f"CAMSPEC_RELATIVE_CALIBRATION_BASELINE_GATE=FAIL {name}={val}")
            params[name] = 1.0
            already_neutral.append(name)
    else:
        names = ("cal100A", "cal100B", "cal143A", "cal143B", "cal217A", "cal217B")
        missing = [n for n in names if n not in params]
        if missing:
            raise RuntimeError(f"HILLIPOP_RELATIVE_CALIBRATION_GATE=FAIL missing={missing}")
        for name in names:
            old = params[name]
            if isinstance(old, (int, float)) and abs(float(old) - 1.0) <= 1e-12:
                already_neutral.append(name)
            else:
                changed.append(name)
            params[name] = 1.0
    if params.get("A_planck") != before_ap:
        raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL")
    return {
        "block": "RELATIVE_CALIBRATION_SEMANTICS",
        "operation": "SET_IMPLEMENTATION_NATIVE_RELATIVE_CALIBRATIONS_TO_NATIVE_NEUTRAL_UNITY",
        "A_planck": "PRESERVED_UNCHANGED_AND_PROFILED",
        "changed_parameters": changed,
        "already_neutral_parameters": already_neutral,
        "cross_implementation_parameter_mapping": False,
    }


def install_precision_patch(q32: Any, implementation: str, hlp_matrix: str | Path | None,
                            hlp_meta: str | Path | None, support: Mapping[str, Any], cfg: Mapping[str, Any]) -> dict[str, Any]:
    runtime: dict[str, Any] = {
        "block": "QUADRATIC_PRECISION_COUPLING",
        "operation": "ZERO_OFFDIAGONAL_PRECISION_TERMS_PRESERVE_NATIVE_PRECISION_DIAGONAL",
        "implementation": implementation,
        "applied": False,
    }
    if implementation == "camspec":
        import cobaya.likelihoods.base_classes.planck_2018_CamSpec_python as cm  # type: ignore
        cls = cm.Planck2018CamSpecPython
        if getattr(cls, "_bubbleverse_q039_precision_patch", False):
            raise RuntimeError("Q039_PRECISION_PATCH_DUPLICATE_GATE=FAIL camspec")
        original = cls.init_params

        def init_params(self, ini, silent=False):
            original(self, ini, silent=silent)
            p = np.asarray(self.covinv, dtype=np.float64)
            if p.ndim != 2 or p.shape[0] != p.shape[1] or not np.all(np.isfinite(p)):
                raise RuntimeError("Q039_CAMSPEC_PRECISION_GATE=FAIL matrix")
            diag = np.diag(p).copy()
            if np.any(diag <= 0):
                raise RuntimeError("Q039_CAMSPEC_PRECISION_GATE=FAIL diagonal")
            off = p - np.diag(diag)
            runtime.update({
                "applied": True,
                "dimension": int(p.shape[0]),
                "original_precision_sha256": sha256_array(p),
                "diagonal_precision_sha256": sha256_array(np.diag(diag)),
                "offdiagonal_frobenius_fraction": float(np.linalg.norm(off) / np.linalg.norm(p)),
            })
            self.covinv = np.diag(diag)
            self._bubbleverse_q039_precision_patch = runtime.copy()

        cls.init_params = init_params
        cls._bubbleverse_q039_precision_patch = True
        return runtime

    if hlp_matrix is None or hlp_meta is None:
        raise RuntimeError("HILLIPOP_RESTRICTED_PRECISION_PARENT_GATE=FAIL")
    q32.install_hillipop_patch(hlp_matrix, hlp_meta, support, cfg)
    import planck_2020_hillipop.hillipop as hm  # type: ignore
    cls = hm.TT
    if getattr(cls, "_bubbleverse_q039_precision_patch", False):
        raise RuntimeError("Q039_PRECISION_PATCH_DUPLICATE_GATE=FAIL hillipop")
    original = cls.initialize

    def initialize(self):
        original(self)
        p = np.asarray(self._q032_precision, dtype=np.float64)
        if p.ndim != 2 or p.shape[0] != p.shape[1] or not np.all(np.isfinite(p)):
            raise RuntimeError("Q039_HILLIPOP_PRECISION_GATE=FAIL matrix")
        diag = np.diag(p).copy()
        if np.any(diag <= 0):
            raise RuntimeError("Q039_HILLIPOP_PRECISION_GATE=FAIL diagonal")
        off = p - np.diag(diag)
        runtime.update({
            "applied": True,
            "dimension": int(p.shape[0]),
            "original_precision_sha256": sha256_array(p),
            "diagonal_precision_sha256": sha256_array(np.diag(diag)),
            "offdiagonal_frobenius_fraction": float(np.linalg.norm(off) / np.linalg.norm(p)),
        })
        self._q032_precision = np.diag(diag)
        self._bubbleverse_q039_precision_patch_meta = runtime.copy()

    cls.initialize = initialize
    cls._bubbleverse_q039_precision_patch = True
    return runtime


def arm_has_calibration(arm: str) -> bool:
    return arm in ("RELATIVE_CALIBRATION_NEUTRAL", COUPLED_ARM)


def arm_has_precision(arm: str) -> bool:
    return arm in ("OFFDIAGONAL_PRECISION_COUPLING_OFF", COUPLED_ARM)


def runtime_preflight(args: argparse.Namespace) -> int:
    """Exercise frozen Q032/Q039 wiring without starting an optimizer."""
    if args.arm not in SINGLE_ARMS or args.implementation not in IMPLEMENTATIONS:
        raise RuntimeError("Q039_PREFLIGHT_ARM_OR_IMPLEMENTATION_GATE=FAIL")
    if f"M{args.mask}-S{args.seed}" not in LABELS:
        raise RuntimeError("Q039_PREFLIGHT_LABEL_GATE=FAIL")
    q32 = load_q032(args.q032_parent_root)
    config_path = resolve_q032_config_path(args.q032_parent_root)
    cfg = q32.load_cfg(config_path)
    pf = q32.load_preflight(args.preflight, sealed=True)
    if pf.get("support_sha256") != SUPPORT_HASH or pf["support_lock"].get("support_sha256") != SUPPORT_HASH:
        raise RuntimeError("Q032_SUPPORT_HASH_GATE=FAIL")
    parent = load_parent_profile(args.parent_profile_dir, args.implementation, args.mask, args.seed)
    start = minimum_start(parent)
    if args.implementation == "hillipop":
        if not args.hlp_matrix or not args.hlp_meta:
            raise RuntimeError("HILLIPOP_PARENT_COVARIANCE_GATE=FAIL")
        q32.install_hillipop_patch(args.hlp_matrix, args.hlp_meta, pf["support_lock"], cfg)
    prefix = Path(args.output).with_suffix("")
    if args.implementation == "camspec":
        info = q32.build_camspec_info(cfg, start, prefix, "refinement", pf["support_lock"])
    else:
        info = q32.build_hillipop_info(cfg, start, prefix, "refinement")
    intervention: dict[str, Any] = {
        "arm": args.arm,
        "scientific_preregister_program_id": SCIENTIFIC_PREREG_PROGRAM_ID,
        "optimizer_started": False,
        "actual_computed_result": False,
    }
    if arm_has_calibration(args.arm):
        intervention["calibration"] = apply_calibration_neutral(info, args.implementation)
    else:
        intervention["calibration"] = "UNCHANGED_NATIVE_Q032"
    if arm_has_precision(args.arm):
        precision = install_precision_patch(q32, args.implementation, args.hlp_matrix, args.hlp_meta, pf["support_lock"], cfg)
        intervention["precision_hook_registered"] = True
        intervention["precision_runtime_before_likelihood_initialization"] = precision
    else:
        intervention["precision_hook_registered"] = False
        intervention["precision"] = "UNCHANGED_NATIVE_Q032"
    params = info.get("params")
    likelihood = info.get("likelihood")
    if not isinstance(params, dict) or not isinstance(likelihood, dict):
        raise RuntimeError("Q039_INFO_BUILD_GATE=FAIL")
    rec = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "scientific_preregister_program_id": SCIENTIFIC_PREREG_PROGRAM_ID,
        "stage": "Q039_RUNTIME_PREFLIGHT_V3", "status": "PASS",
        "implementation": args.implementation, "arm": args.arm,
        "source_label": f"M{args.mask}-S{args.seed}",
        "q032_config_path": str(config_path), "q032_config_path_is_absolute": config_path.is_absolute(),
        "q032_execution_commit": Q032_EXECUTION_COMMIT, "support_sha256": SUPPORT_HASH,
        "optimizer_started": False, "actual_computed_result": False,
        "info_param_count": len(params), "info_likelihood_count": len(likelihood),
        "intervention": intervention,
        "TECHNICAL_PREFLIGHT_ONLY_NOT_SCIENTIFIC_EVIDENCE": True,
    }
    write_json(args.output, rec)
    return 0


def run_profile(args: argparse.Namespace) -> int:
    if args.arm not in ALL_ARMS or args.implementation not in IMPLEMENTATIONS:
        raise RuntimeError("Q039_ARM_OR_IMPLEMENTATION_GATE=FAIL")
    if f"M{args.mask}-S{args.seed}" not in LABELS:
        raise RuntimeError("Q039_LABEL_GATE=FAIL")
    q32 = load_q032(args.q032_parent_root)
    cfg = q32.load_cfg(resolve_q032_config_path(args.q032_parent_root))
    pf = q32.load_preflight(args.preflight, sealed=True)
    if pf.get("support_sha256") != SUPPORT_HASH or pf["support_lock"].get("support_sha256") != SUPPORT_HASH:
        raise RuntimeError("Q032_SUPPORT_HASH_GATE=FAIL")
    parent = load_parent_profile(args.parent_profile_dir, args.implementation, args.mask, args.seed)
    start = minimum_start(parent)

    if args.implementation == "hillipop":
        if not args.hlp_matrix or not args.hlp_meta:
            raise RuntimeError("HILLIPOP_PARENT_COVARIANCE_GATE=FAIL")
        # Always install the Q032 exact-common-support restriction first.
        q32.install_hillipop_patch(args.hlp_matrix, args.hlp_meta, pf["support_lock"], cfg)

    prefix = Path(args.output).with_suffix("")
    if args.implementation == "camspec":
        info = q32.build_camspec_info(cfg, start, prefix, "refinement", pf["support_lock"])
    else:
        info = q32.build_hillipop_info(cfg, start, prefix, "refinement")

    intervention_meta: dict[str, Any] = {
        "arm": args.arm,
        "preregistered_before_result_inspection": True,
        "native_parameter_semantics_preserved": True,
        "forced_nuisance_mapping": False,
        "foreground_swap": False,
        "cross_likelihood_absolute_objective_comparison": False,
        "cross_likelihood_objective_sum": False,
    }
    if arm_has_calibration(args.arm):
        intervention_meta["calibration"] = apply_calibration_neutral(info, args.implementation)
    else:
        intervention_meta["calibration"] = "UNCHANGED_NATIVE_Q032"
    precision_runtime = None
    if arm_has_precision(args.arm):
        precision_runtime = install_precision_patch(
            q32, args.implementation, args.hlp_matrix, args.hlp_meta, pf["support_lock"], cfg
        )
        intervention_meta["precision"] = precision_runtime
    else:
        intervention_meta["precision"] = "UNCHANGED_NATIVE_Q032"

    rec: dict[str, Any] = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "scientific_preregister_program_id": SCIENTIFIC_PREREG_PROGRAM_ID,
        "technical_recovery_version": TECHNICAL_RECOVERY_VERSION,
        "stage": "Q039_INTERVENTION_PROFILE",
        "status": "FAILED",
        "actual_computed_result": False,
        "arm": args.arm,
        "implementation": args.implementation,
        "source_mask": int(args.mask),
        "source_seed": int(args.seed),
        "source_label": f"M{args.mask}-S{args.seed}",
        "parent_q032_result_id": Q032_RESULT_ID,
        "parent_q032_github_run": Q032_GITHUB_RUN,
        "parent_q032_execution_commit": Q032_EXECUTION_COMMIT,
        "parent_q032_objective_chi2": parent.get("objective_chi2"),
        "support_sha256": SUPPORT_HASH,
        "backend_commit": BACKEND_COMMIT,
        "hillipop_commit": HILLIPOP_COMMIT if args.implementation == "hillipop" else None,
        "intervention": intervention_meta,
        "cross_likelihood_absolute_objective_comparison_performed": False,
        "cross_likelihood_objective_sum_performed": False,
    }

    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(args.soft_stop_minutes) * 60))
    try:
        from cobaya.run import run as cobaya_run  # type: ignore
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19  # type: ignore
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        for c in COORDS:
            if c not in row or not finite(row[c]):
                raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL {c}")
        if precision_runtime is not None and not precision_runtime.get("applied"):
            raise RuntimeError("PRECISION_INTERVENTION_APPLICATION_GATE=FAIL")
        rec.update({
            "status": "COMPLETE",
            "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
            "minimizer": {
                "method": "bobyqa",
                "max_evals": 300000,
                "rhoend": 1.0e-5,
                "best_of": 1,
                "ignore_prior": True,
                "start_semantics": "EXACT_VALIDATED_Q032_REFINEMENT_ENDPOINT_SAME_LABEL",
            },
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
        write_json(args.output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def vector(d: Mapping[str, Any]) -> np.ndarray:
    m = d.get("minimum", {})
    return np.asarray([float(m[c]) for c in COORDS], dtype=float)


def metric(a: np.ndarray, b: np.ndarray) -> float:
    s = np.asarray([SCALES[c] for c in COORDS], dtype=float)
    return float(np.sqrt(np.mean(((a - b) / s) ** 2)))


def calculate_geometry(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by = {(str(r["implementation"]), str(r["source_label"])): r for r in rows}
    expected = {(i, l) for i in IMPLEMENTATIONS for l in LABELS}
    if set(by) != expected:
        raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL expected={len(expected)} got={len(by)}")
    for r in rows:
        if r.get("status") != "COMPLETE" or not r.get("actual_computed_result"):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL incomplete_profile")
    matched = {l: metric(vector(by[("camspec", l)]), vector(by[("hillipop", l)])) for l in LABELS}
    cams = np.vstack([vector(by[("camspec", l)]) for l in LABELS])
    hills = np.vstack([vector(by[("hillipop", l)]) for l in LABELS])
    centroid = metric(cams.mean(axis=0), hills.mean(axis=0))
    pairdrifts: dict[str, float] = {}
    for a, b in itertools.combinations(LABELS, 2):
        dc = metric(vector(by[("camspec", a)]), vector(by[("camspec", b)]))
        dh = metric(vector(by[("hillipop", a)]), vector(by[("hillipop", b)]))
        pairdrifts[f"{a}|{b}"] = abs(dc - dh)
    out = {
        "matched_by_label": matched,
        "matched_median": float(np.median(list(matched.values()))),
        "matched_max": float(np.max(list(matched.values()))),
        "centroid": centroid,
        "pairwise_drift_by_pair": pairdrifts,
        "pairwise_median_drift": float(np.median(list(pairdrifts.values()))),
        "pairwise_max_drift": float(np.max(list(pairdrifts.values()))),
    }
    out["material_difference"] = bool(
        out["matched_median"] > THRESHOLD
        or out["centroid"] > THRESHOLD
        or out["pairwise_median_drift"] > THRESHOLD
    )
    out["nonmaterial_all_channels"] = not out["material_difference"]
    return out


def leave_one_out(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for omit in LABELS:
        keep = [l for l in LABELS if l != omit]
        rr = [r for r in rows if r["source_label"] in keep]
        # calculate with temporary label set locally
        by = {(str(r["implementation"]), str(r["source_label"])): r for r in rr}
        matched = [metric(vector(by[("camspec", l)]), vector(by[("hillipop", l)])) for l in keep]
        cams = np.vstack([vector(by[("camspec", l)]) for l in keep])
        hills = np.vstack([vector(by[("hillipop", l)]) for l in keep])
        drifts = []
        for a, b in itertools.combinations(keep, 2):
            dc = metric(vector(by[("camspec", a)]), vector(by[("camspec", b)]))
            dh = metric(vector(by[("hillipop", a)]), vector(by[("hillipop", b)]))
            drifts.append(abs(dc - dh))
        g = {
            "matched_median": float(np.median(matched)),
            "centroid": metric(cams.mean(axis=0), hills.mean(axis=0)),
            "pairwise_median_drift": float(np.median(drifts)),
        }
        g["nonmaterial_all_channels"] = bool(
            g["matched_median"] <= THRESHOLD
            and g["centroid"] <= THRESHOLD
            and g["pairwise_median_drift"] <= THRESHOLD
        )
        results[omit] = g
    return results


def arm_summary(rows: Sequence[Mapping[str, Any]], arm: str) -> dict[str, Any]:
    rr = [r for r in rows if r.get("arm") == arm]
    if len(rr) != 18:
        raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL arm={arm} got={len(rr)}")
    geom = calculate_geometry(rr)
    loo = leave_one_out(rr)
    loo_pass = all(v["nonmaterial_all_channels"] for v in loo.values())
    sufficient = bool(geom["nonmaterial_all_channels"] and loo_pass)
    reductions = {
        "matched_median": BASELINE["matched_median"] - geom["matched_median"],
        "centroid": BASELINE["centroid"] - geom["centroid"],
        "pairwise_median_drift": BASELINE["pairwise_median_drift"] - geom["pairwise_median_drift"],
    }
    return {
        "arm": arm,
        "geometry": geom,
        "baseline_q037": BASELINE,
        "absolute_reductions_vs_q037": reductions,
        "leave_one_label_out": loo,
        "leave_one_label_out_nonmaterial_count": sum(v["nonmaterial_all_channels"] for v in loo.values()),
        "leave_one_label_out_required": 9,
        "sufficient_to_remove_q037_material_geometry": sufficient,
    }


def collect_q039_profiles(root: str | Path) -> list[dict[str, Any]]:
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("stage") == "Q039_INTERVENTION_PROFILE":
            out.append(d)
    return out


def assess_singles(args: argparse.Namespace) -> int:
    rows = collect_q039_profiles(args.input_dir)
    summaries = {arm: arm_summary(rows, arm) for arm in SINGLE_ARMS}
    sufficient = [a for a, s in summaries.items() if s["sufficient_to_remove_q037_material_geometry"]]
    run_coupled = not bool(sufficient)
    rec = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "Q039_SINGLE_BLOCK_ASSESSMENT",
        "status": "PASS",
        "job_completeness_gate": "PASS",
        "single_block_summaries": summaries,
        "single_blocks_sufficient": sufficient,
        "single_block_classification_available": bool(sufficient),
        "run_coupled": run_coupled,
        "foreground_arm": "INCONCLUSIVE_NOT_COMPARABLE_V1",
        "core_likelihood_construction_arm": "INCONCLUSIVE_NOT_COMPARABLE_V1",
    }
    write_json(args.output, rec)
    print("RUN_COUPLED=" + ("true" if run_coupled else "false"))
    return 0


def final_result(args: argparse.Namespace) -> int:
    single = read_json(args.single_assessment)
    if single.get("q") != Q or single.get("stage") != "Q039_SINGLE_BLOCK_ASSESSMENT" or single.get("status") != "PASS":
        raise RuntimeError("SINGLE_ASSESSMENT_PARENT_GATE=FAIL")
    coupled_summary = None
    classification: str
    decisive: list[str]
    if single.get("single_blocks_sufficient"):
        classification = "SINGLE-BLOCK"
        decisive = list(single["single_blocks_sufficient"])
    else:
        if not args.coupled_dir:
            raise RuntimeError("COUPLED_JOB_COMPLETENESS_GATE=FAIL required_but_missing")
        rows = collect_q039_profiles(args.coupled_dir)
        coupled_summary = arm_summary(rows, COUPLED_ARM)
        if coupled_summary["sufficient_to_remove_q037_material_geometry"]:
            classification = "COUPLED-BLOCK"
            decisive = [COUPLED_ARM]
        else:
            classification = "INCONCLUSIVE"
            decisive = []
    final_gate = "PROVISIONAL"
    rec = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "Q039_FINAL",
        "execution_status": "COMPLETE",
        "tests_status": "PENDING_EXTERNAL_TEST_SCRIPT",
        "final_result_gate": final_gate,
        "classification": classification,
        "decisive_tested_blocks": decisive,
        "single_block_assessment": single,
        "coupled_block_summary": coupled_summary,
        "comparability": {
            "RELATIVE_CALIBRATION_SEMANTICS": "COMPARABLE_NATIVE_OPERATION",
            "QUADRATIC_PRECISION_COUPLING": "COMPARABLE_NATIVE_OPERATION",
            "FOREGROUND_TREATMENT": "INCONCLUSIVE_NOT_COMPARABLE_V1",
            "CORE_LIKELIHOOD_CONSTRUCTION": "INCONCLUSIVE_NOT_COMPARABLE_V1",
        },
        "interpretation_limits": [
            "Methodological intervention result, not independent observational evidence.",
            "No cross-likelihood absolute objective subtraction or objective summation was performed.",
            "No native nuisance parameter was mapped one-to-one across implementations.",
            "A successful intervention establishes sufficiency under the preregistered operation, not a physical Planck systematic or instrument failure.",
            "Foreground and deeper core-likelihood construction remain unresolved in V1 because no scientifically defensible matched operation was preregistered for them.",
        ],
        "journal_effect_if_single": "C-036-IMPL methodological causal localization strengthened to tested single-block sufficiency; physical cause remains unestablished.",
        "journal_effect_if_coupled": "Single-block narratives weakened; tested calibration+precision coupling sufficient under Q039 V1 intervention semantics.",
        "journal_effect_if_inconclusive": "C-036-IMPL remains ACTIVE / CAUSE UNRESOLVED; tested calibration/precision arms insufficient and foreground/core blocks remain not comparable in V1.",
    }
    write_json(args.output, rec)
    return 0


def seal_result(args: argparse.Namespace) -> int:
    provisional = read_json(args.provisional)
    tests = read_json(args.tests)
    if provisional.get("q") != Q or provisional.get("program_id") != PROGRAM_ID:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL provisional")
    if provisional.get("final_result_gate") != "PROVISIONAL" or provisional.get("execution_status") != "COMPLETE":
        raise RuntimeError("PROVISIONAL_RESULT_GATE=FAIL")
    if tests.get("q") != Q or tests.get("program_id") != PROGRAM_ID or tests.get("FINAL_RESULT_GATE") != "PASS":
        raise RuntimeError("RESULT_TEST_GATE=FAIL")
    sealed = copy.deepcopy(provisional)
    sealed["stage"] = "Q039_FINAL_SEALED"
    sealed["tests_status"] = "COMPLETE"
    sealed["result_tests"] = tests
    sealed["final_result_gate"] = "PASS"
    write_json(args.output, sealed)
    if args.handoff:
        handoff = {
            "current_q": Q,
            "program_id": PROGRAM_ID,
            "scientific_question": "Can a single native implementation block materially explain/remove the Q037/Q038 common-geometry difference, or are coupled blocks required?",
            "new_result": {"result_id": RESULT_ID, "classification": sealed["classification"]},
            "final_result_gate": "PASS",
            "sources_preserved": ["K-044", "K-045/K-052", "K-046", "K-049", "CAMSPEC_2021_ID_UNRESOLVED"],
            "parent_results_preserved": [
                "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002",
                "R-Q035-EDE-CLASSIFIER-HARMONIZATION-001",
                "R-Q036-EDE-ENDPOINT-GEOMETRY-PORTABILITY-001",
                "R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001",
                "R-Q038-EDE-COORDINATE-LOCALIZATION-001",
            ],
            "unresolved_issues": [k for k,v in sealed.get("comparability",{}).items() if str(v).startswith("INCONCLUSIVE")],
            "return_route": "RESULT INGESTION & ROUTING ENGINE",
        }
        write_json(args.handoff, handoff)
    return 0


def validate_parent_set(args: argparse.Namespace) -> int:
    rows = []
    for impl in IMPLEMENTATIONS:
        for m in (3, 6, 7):
            for s in (0, 1, 2):
                rows.append(load_parent_profile(args.parent_dir, impl, m, s))
    geom = calculate_geometry([
        {
            "implementation": r["implementation"],
            "source_label": r["source_label"],
            "status": "COMPLETE",
            "actual_computed_result": True,
            "minimum": r["minimum"],
        }
        for r in rows
    ])
    checks = {
        k: abs(float(geom[k]) - float(v)) <= 1e-12 for k, v in BASELINE.items()
    }
    if not all(checks.values()):
        raise RuntimeError(f"Q037_BASELINE_REPRODUCTION_GATE=FAIL {checks} got={geom}")
    rec = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "stage": "Q039_PARENT_INPUT_GATE",
        "status": "PASS",
        "q032_run": Q032_GITHUB_RUN,
        "q032_result_id": Q032_RESULT_ID,
        "q032_execution_commit": Q032_EXECUTION_COMMIT,
        "support_sha256": SUPPORT_HASH,
        "q037_baseline_reproduced": {k: geom[k] for k in BASELINE},
        "Q037_BASELINE_REPRODUCTION_GATE": "PASS",
        "JOB_COMPLETENESS_GATE": "PASS",
    }
    write_json(args.output, rec)
    return 0


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    a = sp.add_parser("validate-parent")
    a.add_argument("--parent-dir", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=validate_parent_set)

    a = sp.add_parser("runtime-preflight")
    a.add_argument("--q032-parent-root", required=True)
    a.add_argument("--preflight", required=True)
    a.add_argument("--parent-profile-dir", required=True)
    a.add_argument("--implementation", choices=IMPLEMENTATIONS, required=True)
    a.add_argument("--arm", choices=SINGLE_ARMS, required=True)
    a.add_argument("--mask", type=int, choices=(3, 6, 7), required=True)
    a.add_argument("--seed", type=int, choices=(0, 1, 2), required=True)
    a.add_argument("--hlp-matrix")
    a.add_argument("--hlp-meta")
    a.add_argument("--output", required=True)
    a.set_defaults(func=runtime_preflight)

    a = sp.add_parser("profile")
    a.add_argument("--q032-parent-root", required=True)
    a.add_argument("--preflight", required=True)
    a.add_argument("--parent-profile-dir", required=True)
    a.add_argument("--implementation", choices=IMPLEMENTATIONS, required=True)
    a.add_argument("--arm", choices=ALL_ARMS, required=True)
    a.add_argument("--mask", type=int, choices=(3, 6, 7), required=True)
    a.add_argument("--seed", type=int, choices=(0, 1, 2), required=True)
    a.add_argument("--hlp-matrix")
    a.add_argument("--hlp-meta")
    a.add_argument("--soft-stop-minutes", type=float, default=300.0)
    a.add_argument("--output", required=True)
    a.set_defaults(func=run_profile)

    a = sp.add_parser("assess-singles")
    a.add_argument("--input-dir", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=assess_singles)

    a = sp.add_parser("final")
    a.add_argument("--single-assessment", required=True)
    a.add_argument("--coupled-dir")
    a.add_argument("--output", required=True)
    a.set_defaults(func=final_result)

    a = sp.add_parser("seal")
    a.add_argument("--provisional", required=True)
    a.add_argument("--tests", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--handoff")
    a.set_defaults(func=seal_result)
    return p


def main() -> int:
    args = make_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
