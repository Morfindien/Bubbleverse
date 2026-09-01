#!/usr/bin/env python3
"""Bubbleverse Q014 — n=3 EDE external likelihood viability V5.

Scientific target
-----------------
For each external evidence chain, compare a chain-specific free-H0 n=3 profile
minimum with a fixed-H0=71.5 reprofile, and separately evaluate/profile the exact
Q011 shared-physics vector. Absolute chi2 values are NEVER compared across chains.

Claim boundary
--------------
* Planck/NPIPE branch is a public-likelihood common-backend approximation to K-039,
  not an exact paper-native reproduction of its modified CamSpec construction.
* SPT branch uses official D1 candl/MUSE likelihood products, but the cosmological
  backend/optimizer remains the frozen Bubbleverse Q005 V14 common backend.
* Q011 is preserved as BEST-OBSERVED MINIMUM ONLY; this program does not reopen its
  internal globality question.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import random
import signal
import sys
import time
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_NAME = "q014_external_viability_v5_config.yml"
CURRENT_Q = "Q014"
RUN_ID = "Q014-EXTERNAL-VIABILITY-V5"
CODE_VERSION = "4.0-class-ede-persistent-import"


def load_yaml(path: str | Path = CONFIG_NAME) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"CONFIG_GATE=FAIL non-mapping YAML: {p}")
    return data


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=_json_default) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def _json_default(x: Any) -> Any:
    try:
        import numpy as np
        if isinstance(x, np.generic):
            return x.item()
    except Exception:
        pass
    return str(x)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=_json_default).encode()
    return hashlib.sha256(raw).hexdigest()


def import_core():
    import q005_hpc_v14 as core
    return core


def load_base_cfg(c: Mapping[str, Any]) -> dict[str, Any]:
    core = import_core()
    return core.load_cfg(c["parent"]["q005_config"])


def numeric_profile_record(q011: Mapping[str, Any], target: float) -> Mapping[str, Any]:
    profiles = q011.get("profile_targets")
    if not isinstance(profiles, Mapping):
        raise RuntimeError("Q011_SCHEMA_GATE=FAIL missing profile_targets")
    for key, value in profiles.items():
        try:
            if math.isclose(float(key), target, rel_tol=0.0, abs_tol=1e-10):
                if isinstance(value, Mapping):
                    return value
        except Exception:
            continue
    raise RuntimeError(f"Q011_TARGET_GATE=FAIL missing H0={target}")


def _flatten_mapping(obj: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out[key] = v
            out.update(_flatten_mapping(v, key))
    return out


def extract_value(obj: Mapping[str, Any], aliases: list[str]) -> float:
    # First look for exact keys anywhere in nested mappings, then terminal-name matches.
    flat = _flatten_mapping(obj)
    for alias in aliases:
        for k, v in flat.items():
            if k == alias or k.endswith("." + alias):
                try:
                    x = float(v)
                except Exception:
                    continue
                if math.isfinite(x):
                    return x
    raise RuntimeError(f"Q011_EXACT_VECTOR_GATE=FAIL missing aliases={aliases}")


def q011_parent_record(c: Mapping[str, Any], q011_path: str | Path) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    """Validate the authoritative Q011 parent and return its fixed-H0 profile record.

    Q011 V4 intentionally excludes the fixed H0 parameter from the stored Cobaya
    best-fit vector. The authoritative fixed value is therefore the profile record's
    ``target_h0`` field, while the remaining shared physics parameters live under
    ``best_record.bestfit``. This preserves, rather than weakens, the exact-parent gate.
    """
    q011 = json.loads(Path(q011_path).read_text(encoding="utf-8"))
    parent = c["parent"]["q011"]
    if q011.get("q") != "Q011":
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL q")
    if q011.get("run_id") != "Q011-EDE-GLOBALITY-CERTIFICATION-V4":
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL run_id")
    if q011.get("result_identifier") != parent["result_id"]:
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL result_id")
    if q011.get("combined_globality_classification") != parent["classification"]:
        raise RuntimeError("Q011_CLASSIFICATION_GATE=FAIL")
    if q011.get("mathematical_globality_proven") is not False:
        raise RuntimeError("Q011_GLOBALITY_GATE=FAIL")

    target = float(c["scientific_surface"]["target_h0"])
    rec = numeric_profile_record(q011, target)
    record_h0 = float(rec.get("target_h0"))
    if not math.isclose(record_h0, target, rel_tol=0.0,
                        abs_tol=float(c["validation"]["exact_h0_tolerance"])):
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL target_h0")

    best_chi2 = float(rec.get("best_chi2"))
    if not math.isclose(best_chi2, float(parent["best_chi2_optimizer_native"]), rel_tol=0.0,
                        abs_tol=float(c["validation"]["q011_parent_chi2_tolerance"])):
        raise RuntimeError("Q011_PARENT_CHI2_GATE=FAIL")

    best_record = rec.get("best_record")
    if not isinstance(best_record, Mapping):
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL missing best_record")
    if best_record.get("q") != "Q011" or best_record.get("run_id") != "Q011-EDE-GLOBALITY-CERTIFICATION-V4":
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL best_record provenance")
    if best_record.get("model") != "ede_n3":
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL model")
    if not math.isclose(float(best_record.get("target_h0")), target, rel_tol=0.0,
                        abs_tol=float(c["validation"]["exact_h0_tolerance"])):
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL best_record target_h0")

    bestfit = best_record.get("bestfit")
    if not isinstance(bestfit, Mapping):
        raise RuntimeError("Q011_PARENT_IDENTITY_GATE=FAIL missing bestfit")
    if not math.isclose(float(bestfit.get("chi2")), best_chi2, rel_tol=0.0,
                        abs_tol=float(c["validation"]["q011_parent_chi2_tolerance"])):
        raise RuntimeError("Q011_PARENT_CHI2_GATE=FAIL bestfit")
    return q011, rec


def q011_exact_shared_vector(c: Mapping[str, Any], q011_path: str | Path) -> dict[str, float]:
    _, rec = q011_parent_record(c, q011_path)
    target = float(c["scientific_surface"]["target_h0"])
    bestfit = rec["best_record"]["bestfit"]

    # IMPORTANT: Q011 V4 deliberately omitted fixed H0 from the stored bestfit
    # vector (FIXED_H0_EXCLUDED_FROM_STORED_VECTOR_REQUIREMENT). Therefore H0
    # comes exactly from the authoritative profile record's target_h0. Every
    # other shared-physics value comes exactly from best_record.bestfit.
    aliases = {
        "omega_b": ["omega_b", "omegabh2", "ombh2"],
        "omega_cdm": ["omega_cdm", "omegach2", "omch2"],
        "tau_reio": ["tau_reio", "tau"],
        "n_s": ["n_s", "ns"],
        "logA": ["logA", "logA_s", "logA10", "log(10^10A_s)"],
        "fEDE": ["fEDE", "f_EDE", "f_ede"],
        "log10z_c": ["log10z_c", "log10_z_c", "log10zc"],
        "thetai_scf": ["thetai_scf", "theta_i", "theta_i_scf"],
    }
    vector = {"H0": float(rec["target_h0"])}
    vector.update({name: extract_value(bestfit, names) for name, names in aliases.items()})
    if not math.isclose(vector["H0"], target, rel_tol=0.0,
                        abs_tol=float(c["validation"]["exact_h0_tolerance"])):
        raise RuntimeError("Q011_EXACT_VECTOR_GATE=FAIL H0")
    return vector


def source_file_gates(c: Mapping[str, Any]) -> dict[str, Any]:
    expected = {
        "q005_hpc_v14.py": "2c69d6b57f523f910207683eb67c07548e61bef9",
        "q005_hpc_v14_config.yml": "02ab4816fa2f41f3da616d60a4f71a210dd5882e",
        "q005_setup_v14.sh": "546101534136ffe2b46233b7daea57b9c22ff18c",
        "q005_hpc_v14_requirements.txt": "495270dff0e733309eebfa90aadecfc107dcc6e2",
    }
    checks: dict[str, Any] = {}
    for name, git_blob in expected.items():
        p = ROOT / name
        if not p.exists():
            checks[name] = {"exists": False, "pass": False, "expected_git_blob": git_blob}
            continue
        import subprocess
        proc = subprocess.run(["git", "hash-object", str(p)], cwd=ROOT, text=True, capture_output=True)
        actual = proc.stdout.strip() if proc.returncode == 0 else None
        checks[name] = {
            "exists": True,
            "expected_git_blob": git_blob,
            "actual_git_blob": actual,
            "pass": actual == git_blob,
        }
    return checks


def _remove_local_h0_likelihood(info: dict[str, Any]) -> None:
    likes = info.get("likelihood")
    if isinstance(likes, dict):
        for k in list(likes):
            if "h0dn" in str(k).lower() or "sh0es" in str(k).lower():
                likes.pop(k, None)


def build_chain_likelihoods(chain: str, c: Mapping[str, Any]) -> dict[str, Any]:
    spec = c["chains"][chain]
    if chain == "planck_npipe_k039_approx":
        return {name: None for name in spec["likelihoods"]}

    if chain in {"spt_d1_only", "spt_d1_plus_desi"}:
        from candl.interface import CandlCobayaLikelihood
        import spt_candl_data
        like: dict[str, Any] = {
            "spt_d1_primary_lite": {
                "external": CandlCobayaLikelihood,
                "data_set_file": spt_candl_data.SPT3G_D1_TnE,
                "variant": "lite",
                "additional_args": {},
                "clear_internal_priors": True,
                "feedback": True,
                "wrapper": None,
            },
            spec["lensing_likelihood"]["plugin"]: {
                "components": list(spec["lensing_likelihood"]["components"]),
            },
        }
        tau = spec["tau_information"]
        core = import_core()
        like["q014_tau_information"] = core.gaussian_likelihood(
            float(tau["mean"]), float(tau["sigma"]), "tau_reio"
        )
        if bool(spec.get("include_desi_dr2")):
            like["bao.desi_dr2"] = None
        return like
    raise KeyError(f"Unknown chain: {chain}")


def inject_chain_native_parameters(info: dict[str, Any], chain: str, c: Mapping[str, Any]) -> None:
    """Add external-chain nuisance parameters that are not part of Q005.

    SPT-3G D1 TnE SPTlite requires both Tcal and Ecal as explicit Cobaya
    parameters. The pinned official SPT Cobaya lite YAML gives uniform bounds
    0.8..1.2 for both and an additional Gaussian constraint only for Tcal,
    N(1, 0.0036^2). These are chain-native nuisance parameters and remain
    profiled even in q011_shared_physics mode.
    """
    if chain not in {"spt_d1_only", "spt_d1_plus_desi"}:
        return
    params = info.setdefault("params", {})
    if not isinstance(params, dict):
        raise RuntimeError("SPT_NATIVE_CALIBRATION_NUISANCE_GATE=FAIL params block")
    nuisance = c["chains"][chain]["primary_likelihood"]["nuisance_parameters"]
    for name in ("Tcal", "Ecal"):
        spec = nuisance[name]
        lo = float(spec["prior"]["min"]); hi = float(spec["prior"]["max"])
        ref = float(spec["ref"]); proposal = float(spec["proposal"])
        params[name] = {
            "prior": {"min": lo, "max": hi},
            "ref": {"dist": "norm", "loc": ref, "scale": proposal},
            "proposal": proposal,
        }
    priors = info.get("prior")
    if priors is None:
        priors = {}
        info["prior"] = priors
    if not isinstance(priors, dict):
        raise RuntimeError("SPT_NATIVE_CALIBRATION_NUISANCE_GATE=FAIL prior block")
    tcal = nuisance["Tcal"]["gaussian_constraint"]
    priors["q014_spt_gaussian_Tcal"] = (
        "lambda Tcal: stats.norm.logpdf(Tcal, loc=%r, scale=%r)"
        % (float(tcal["mean"]), float(tcal["sigma"]))
    )


def freeze_param(params: dict[str, Any], name: str, value: float) -> None:
    if name not in params:
        raise RuntimeError(f"PARAMETER_GATE=FAIL cannot freeze missing {name}")
    params[name] = float(value)


def set_reference(params: dict[str, Any], name: str, value: float) -> None:
    spec = params.get(name)
    if not isinstance(spec, dict) or "prior" not in spec:
        return
    scale = spec.get("proposal")
    if scale is None:
        prior = spec.get("prior")
        if isinstance(prior, dict) and "min" in prior and "max" in prior:
            scale = max((float(prior["max"]) - float(prior["min"])) / 20.0, 1e-8)
        else:
            scale = max(abs(float(value)) * 0.01, 1e-6)
    spec["ref"] = {"dist": "norm", "loc": float(value), "scale": float(scale)}


def q005_default_reference(info: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for name, spec in info.get("params", {}).items():
        if not isinstance(spec, Mapping):
            continue
        ref = spec.get("ref")
        if isinstance(ref, Mapping) and "loc" in ref:
            try:
                out[name] = float(ref["loc"])
            except Exception:
                pass
    return out


def start_vector(chain: str, family: str, c: Mapping[str, Any], info: Mapping[str, Any],
                 q011_vec: Mapping[str, float]) -> dict[str, float]:
    base = q005_default_reference(info)
    if family == "q011":
        base.update(q011_vec)
    elif family == "external":
        base.update({k: float(v) for k, v in c["chains"][chain].get("start_reference", {}).items()})
    elif family == "baseline":
        pass
    elif family in {"jitter_a", "jitter_b"}:
        # Deterministic small perturbations around the Q011/external region. They are
        # start points only; priors/bounds/objective are unchanged.
        base.update(q011_vec if family == "jitter_a" else
                    {k: float(v) for k, v in c["chains"][chain].get("start_reference", {}).items()})
        signs = 1.0 if family == "jitter_a" else -1.0
        tweaks = {
            "omega_b": 0.00008 * signs,
            "omega_cdm": 0.0012 * signs,
            "n_s": 0.003 * signs,
            "logA": 0.008 * signs,
            "fEDE": 0.008 * signs,
            "log10z_c": 0.04 * signs,
            "thetai_scf": 0.05 * signs,
            "H0": 0.35 * signs,
        }
        for k, dv in tweaks.items():
            if k in base:
                base[k] = float(base[k]) + dv
    else:
        raise KeyError(f"Unknown start family {family}")
    return base


def build_info(chain: str, mode: str, start_family: str, restart_index: int,
               c: Mapping[str, Any], q011_vec: Mapping[str, float], output_prefix: Path,
               max_evals: int | None = None) -> tuple[dict[str, Any], dict[str, float]]:
    core = import_core()
    base_cfg = load_base_cfg(c)
    info = core.build_model(base_cfg, c["scientific_surface"]["model"], smoke=False,
                            restart=int(restart_index))
    info = copy.deepcopy(info)
    info["likelihood"] = build_chain_likelihoods(chain, c)
    _remove_local_h0_likelihood(info)
    inject_chain_native_parameters(info, chain, c)

    params = info.get("params")
    if not isinstance(params, dict):
        raise RuntimeError("MODEL_GATE=FAIL missing params")

    refs = start_vector(chain, start_family, c, info, q011_vec)
    for name, value in refs.items():
        if name in params:
            set_reference(params, name, value)

    target = float(c["scientific_surface"]["target_h0"])
    if mode == "fixed_h0_71p5":
        freeze_param(params, "H0", target)
    elif mode == "q011_shared_physics":
        for name, value in q011_vec.items():
            if name not in params:
                raise RuntimeError(f"Q011_SHARED_VECTOR_GATE=FAIL model missing {name}")
            freeze_param(params, name, float(value))
    elif mode != "reference_free_h0":
        raise KeyError(f"Unknown mode {mode}")

    mincfg = copy.deepcopy(c["execution"]["minimizer"])
    mincfg["seed"] = 140000 + int(restart_index)
    if max_evals is not None:
        mincfg["max_evals"] = int(max_evals)
    info["sampler"] = {"minimize": mincfg}
    info["output"] = str(output_prefix.resolve())
    info["packages_path"] = str((ROOT / base_cfg["packages_path"]).resolve())
    return info, refs


def minimum_to_row(minimum: Any) -> dict[str, Any]:
    # Cobaya OnePoint/SampleCollection compatibility across minor versions.
    data = getattr(minimum, "data", None)
    if data is not None:
        try:
            if hasattr(data, "iloc") and len(data) > 0:
                return {str(k): _json_default(v) for k, v in data.iloc[0].to_dict().items()}
        except Exception:
            pass
    if isinstance(minimum, Mapping):
        return {str(k): _json_default(v) for k, v in minimum.items()}
    if hasattr(minimum, "to_dict"):
        try:
            d = minimum.to_dict()
            if isinstance(d, Mapping):
                return {str(k): _json_default(v) for k, v in d.items()}
        except Exception:
            pass
    # OnePoint supports minimum[parameter], but discovering all names is version
    # dependent. The on-disk minimum parser is used as the final fallback.
    return {}


def parse_minimum_text(path: Path) -> dict[str, Any]:
    lines = [x.strip() for x in path.read_text(errors="replace").splitlines() if x.strip()]
    if len(lines) < 2:
        return {}
    header = lines[0].lstrip("#").strip().split()
    vals = lines[-1].lstrip("#").strip().split()
    if len(header) != len(vals):
        return {}
    out: dict[str, Any] = {}
    for k, v in zip(header, vals):
        try:
            out[k] = float(v)
        except Exception:
            out[k] = v
    return out


def harvest_output_prefix(prefix: Path) -> tuple[dict[str, Any], str | None]:
    patterns = [
        prefix.name + ".minimum.txt",
        prefix.name + "*.minimum.txt",
        prefix.name + "*.minimum",
        prefix.name + "*.bestfit*",
    ]
    candidates: list[Path] = []
    for pat in patterns:
        candidates.extend(sorted(prefix.parent.glob(pat)))
    for p in candidates:
        if p.is_file():
            row = parse_minimum_text(p)
            if row:
                return row, str(p)
    return {}, None


def objective_from_row(row: Mapping[str, Any]) -> tuple[float | None, dict[str, float], str]:
    comps: dict[str, float] = {}
    for k, v in row.items():
        if str(k).startswith("chi2__"):
            try:
                x = float(v)
            except Exception:
                continue
            if math.isfinite(x):
                comps[str(k)] = x
    # Q014 intentionally keeps chain-native nuisance constraints. With flat Q005
    # science priors, 2*minuslogpost differs from pure chi2 only by those nuisance
    # constraints plus constants that cancel in within-chain profile differences.
    for key in ("minuslogpost", "minuslogp"):
        if key in row:
            try:
                x = 2.0 * float(row[key])
            except Exception:
                continue
            if math.isfinite(x):
                return x, comps, f"2X_{key.upper()}_CHAIN_CONSTRAINED_PROFILE_OBJECTIVE"
    if comps:
        return float(sum(comps.values())), comps, "SUM_COBAYA_CHI2_COMPONENTS_FALLBACK"
    if "minusloglike" in row:
        try:
            x=2.0*float(row["minusloglike"])
            if math.isfinite(x): return x, {}, "2X_MINUSLOGLIKE_FALLBACK"
        except Exception:
            pass
    return None, {}, "UNAVAILABLE"


def direct_evaluate_if_no_sampled(info: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    from cobaya.model import get_model
    model = get_model(info)
    sampled = list(model.parameterization.sampled_params())
    if sampled:
        return None, sampled
    logpost = model.logposterior([])
    # LogPosterior object exposes loglikes/logpost in Cobaya; preserve robustly.
    row: dict[str, Any] = {}
    lp = getattr(logpost, "logpost", None)
    if lp is not None:
        row["minuslogpost"] = -float(lp)
    names = list(getattr(model, "likelihood", {}).keys())
    vals = getattr(logpost, "loglikes", None)
    if vals is not None:
        try:
            for name, value in zip(names, vals):
                row[f"chi2__{name}"] = -2.0 * float(value)
        except Exception:
            pass
    for name in model.parameterization.constant_params():
        try:
            row[name] = model.parameterization.constant_params()[name]
        except Exception:
            pass
    return row, sampled


def run_task(chain: str, mode: str, start_family: str, restart_index: int,
             q011_path: str | Path, output: str | Path, c: Mapping[str, Any],
             max_evals: int | None = None) -> int:
    started = time.time()
    q011_vec = q011_exact_shared_vector(c, q011_path)
    outp = Path(output)
    outp.parent.mkdir(parents=True, exist_ok=True)
    prefix = outp.parent / (outp.stem + "_cobaya")
    info, refs = build_info(chain, mode, start_family, restart_index, c, q011_vec, prefix, max_evals)

    runtime_source: dict[str, Any] = {}
    rsp = ROOT / "q014_v5_source_runtime" / "setup_imports.json"
    if rsp.exists():
        try:
            runtime_source = json.loads(rsp.read_text(encoding="utf-8"))
        except Exception:
            runtime_source = {"status": "UNREADABLE_RUNTIME_SOURCE_PROVENANCE"}

    rec: dict[str, Any] = {
        "case_id": c["project"]["case_id"],
        "q": CURRENT_Q,
        "original_case_question": c["project"]["original_case_question"],
        "run_id": RUN_ID,
        "code_version": CODE_VERSION,
        "chain": chain,
        "chain_label": c["chains"][chain]["label"],
        "mode": mode,
        "start_family": start_family,
        "restart_index": int(restart_index),
        "model": "ede_n3",
        "n_scf": 3,
        "target_h0": float(c["scientific_surface"]["target_h0"]),
        "start_vector_sha256": canonical_hash(refs),
        "q011_exact_shared_vector_sha256": canonical_hash(q011_vec),
        "q011_globality_status_preserved": c["claim_boundary"]["q011_globality_status_preserved"],
        "paper_native_reproduction": bool(c["chains"][chain].get("paper_native_reproduction", False)),
        "absolute_chi2_cross_chain_comparison_allowed": False,
        "runtime_source_provenance": runtime_source,
        "runtime_source_provenance_sha256": canonical_hash(runtime_source),
        "status": "FAILED",
        "runtime_seconds": None,
    }

    try:
        # Shared-vector SPTlite can have no sampled parameters after the common
        # physics is frozen. In that case a direct likelihood evaluation is the
        # mathematically correct operation; do not invent a meaningless optimizer.
        if mode == "q011_shared_physics":
            direct, sampled = direct_evaluate_if_no_sampled(info)
            rec["sampled_parameters_after_freeze"] = sampled
            if direct is not None:
                row = direct
                rec["execution_kind"] = "DIRECT_FIXED_SHARED_PHYSICS_EVALUATION"
            else:
                row = {}
        else:
            row = {}

        if not row:
            from cobaya.run import run as cobaya_run
            rec["execution_kind"] = "COBAYA_BOBYQA_PROFILE"
            try:
                _updated, sampler = cobaya_run(info, force=True)
                minimum = sampler.products()["minimum"]
                row = minimum_to_row(minimum)
                rec["optimizer_exit"] = "CONVERGED_OR_COBAYA_COMPLETED"
            except KeyboardInterrupt:
                rec["optimizer_exit"] = "SOFT_RUNTIME_INTERRUPT"
                row, minimum_path = harvest_output_prefix(prefix)
                rec["harvested_minimum_path"] = minimum_path
                if not row:
                    raise

        if not row:
            row, minimum_path = harvest_output_prefix(prefix)
            rec["harvested_minimum_path"] = minimum_path
        chi2, comps, basis = objective_from_row(row)
        rec["minimum"] = row
        rec["chi2_components"] = comps
        rec["objective_chi2"] = chi2
        rec["objective_basis"] = basis
        rec["finite_result"] = chi2 is not None and math.isfinite(float(chi2))
        rec["status"] = "COMPLETE" if rec["finite_result"] else "INVALID"
    except KeyboardInterrupt:
        rec["status"] = "CONTINUATION_REQUIRED"
        rec["failure_type"] = "SOFT_RUNTIME_NO_FINITE_MINIMUM_HARVESTED"
    except Exception as exc:
        rec["status"] = "TECHNICAL_FAILURE"
        rec["failure_type"] = type(exc).__name__
        rec["error"] = repr(exc)
    finally:
        rec["runtime_seconds"] = time.time() - started
        dump_json(outp, rec)
    return 0 if rec["status"] == "COMPLETE" else 9


def expected_tasks(c: Mapping[str, Any], depth: str = "standard") -> list[dict[str, Any]]:
    if depth not in {"standard", "expanded"}:
        raise ValueError("depth must be standard or expanded")
    tasks: list[dict[str, Any]] = []
    idx = 0
    for chain in c["chains"]:
        for mode in c["execution"]["modes"]:
            families = list(c["execution"]["standard_start_families"][mode])
            if depth == "expanded":
                families += list(c["execution"]["expanded_extra_start_families"][mode])
            for family in families:
                idx += 1
                tasks.append({
                    "chain": chain,
                    "mode": mode,
                    "start_family": family,
                    "restart_index": idx,
                    "tag": f"{chain}-{mode}-{family}".replace("_", "-"),
                })
    return tasks


def preflight(c: Mapping[str, Any], q011_path: str | Path | None = None,
              require_environment: bool = False, chain: str | None = None) -> dict[str, Any]:
    report: dict[str, Any] = {
        "case_id": c["project"]["case_id"],
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "status": "FAIL",
        "checks": {},
    }
    report["checks"]["CASE_QUESTION_IDENTITY_GATE"] = (
        c["project"]["q"] == CURRENT_Q and
        "Planck NPIPE" in c["project"]["original_case_question"] and
        "SPT-3G D1" in c["project"]["original_case_question"]
    )
    report["checks"]["CASE_ID_NONINVENTION_GATE"] = c["project"]["case_id"] == "NOT DOCUMENTED"
    report["checks"]["N3_MODEL_GATE"] = (
        c["scientific_surface"]["model"] == "ede_n3" and
        int(c["scientific_surface"]["n_scf"]) == 3
    )
    text = json.dumps(c).lower()
    report["checks"]["NO_H0DN_GATE"] = (
        c["scientific_surface"]["no_local_h0_prior"] is True and
        "h0dn" not in json.dumps(c["chains"]).lower() and
        "sh0es" not in json.dumps(c["chains"]).lower()
    )
    report["checks"]["NO_ACT_NUISANCE_GATE"] = (
        "a_act" not in json.dumps(c["chains"]).lower() and
        "p_act" not in json.dumps(c["chains"]).lower()
    )
    report["checks"]["PLANCK_APPROXIMATION_CLAIM_GATE"] = (
        c["chains"]["planck_npipe_k039_approx"]["paper_native_reproduction"] is False and
        "APPROX" in c["chains"]["planck_npipe_k039_approx"]["label"]
    )
    report["checks"]["SPT_NO_DESI_PRIMARY_GATE"] = (
        c["chains"]["spt_d1_only"]["include_desi_dr2"] is False and
        c["chains"]["spt_d1_plus_desi"]["include_desi_dr2"] is True
    )
    report["checks"]["SPT_LENSING_NO_PRIMARY_CMB_DOUBLECOUNT_GATE"] = (
        c["chains"]["spt_d1_only"]["lensing_likelihood"]["components"] == ["ϕϕ"]
    )
    try:
        spt_nuis = c["chains"]["spt_d1_only"]["primary_likelihood"]["nuisance_parameters"]
        report["checks"]["SPT_NATIVE_CALIBRATION_NUISANCE_GATE"] = (
            set(spt_nuis) == {"Tcal", "Ecal"}
            and float(spt_nuis["Tcal"]["prior"]["min"]) == 0.8
            and float(spt_nuis["Tcal"]["prior"]["max"]) == 1.2
            and float(spt_nuis["Ecal"]["prior"]["min"]) == 0.8
            and float(spt_nuis["Ecal"]["prior"]["max"]) == 1.2
            and float(spt_nuis["Tcal"]["gaussian_constraint"]["mean"]) == 1.0
            and float(spt_nuis["Tcal"]["gaussian_constraint"]["sigma"]) == 0.0036
            and spt_nuis["Ecal"].get("gaussian_constraint") is None
        )
    except Exception:
        report["checks"]["SPT_NATIVE_CALIBRATION_NUISANCE_GATE"] = False
    report["checks"]["CHAIN_SEPARATION_GATE"] = (
        c["claim_boundary"]["planck_plus_spt_direct_chi2_sum_forbidden"] is True and
        c["claim_boundary"]["report_each_external_chain_separately"] is True
    )

    sf = source_file_gates(c)
    report["source_files"] = sf
    report["checks"]["FROZEN_Q005_SOURCE_GATE"] = bool(sf) and all(x["pass"] for x in sf.values())

    if q011_path is not None:
        try:
            q011_parent_record(c, q011_path)
            report["checks"]["Q011_PARENT_IDENTITY_GATE"] = True
        except Exception as exc:
            report["checks"]["Q011_PARENT_IDENTITY_GATE"] = False
            report["checks"]["Q011_EXACT_VECTOR_GATE"] = False
            report["q011_parent_error"] = repr(exc)
        else:
            try:
                vec = q011_exact_shared_vector(c, q011_path)
                report["q011_exact_vector"] = vec
                report["q011_exact_vector_sha256"] = canonical_hash(vec)
                report["checks"]["Q011_EXACT_VECTOR_GATE"] = True
            except Exception as exc:
                report["checks"]["Q011_EXACT_VECTOR_GATE"] = False
                report["q011_vector_error"] = repr(exc)
    else:
        report["checks"]["Q011_PARENT_IDENTITY_GATE"] = False
        report["checks"]["Q011_EXACT_VECTOR_GATE"] = False

    if require_environment:
        if chain not in {"planck_npipe_k039_approx", "spt_d1_only", "spt_d1_plus_desi"}:
            report["environment"] = {"error": "--chain is required with --environment"}
            report["checks"]["EXTERNAL_ENVIRONMENT_GATE"] = False
        else:
            # V5: environment requirements are chain-native. Planck jobs must not
            # fail merely because SPT-only Python modules are intentionally absent.
            required_modules = ["cobaya", "classy"]
            if chain.startswith("spt_"):
                required_modules += ["candl", "spt_candl_data", "muse3glike"]
            env: dict[str, Any] = {"chain": chain, "required_modules": required_modules}
            module_checks: dict[str, Any] = {}
            for mod in required_modules:
                try:
                    m = __import__(mod)
                    mod_file = getattr(m, "__file__", None)
                    passed = True
                    detail: dict[str, Any] = {"pass": True, "file": mod_file}
                    if mod == "classy":
                        normalized = str(mod_file or "").replace("\\", "/")
                        passed = "/external/class_ede/" in normalized
                        detail["expected_origin"] = "frozen external/class_ede build"
                        detail["pass"] = passed
                    module_checks[mod] = detail
                except Exception as exc:
                    module_checks[mod] = {"pass": False, "error": repr(exc)}
            env["modules"] = module_checks
            report["environment"] = env
            report["checks"]["EXTERNAL_ENVIRONMENT_GATE"] = all(v["pass"] for v in module_checks.values())
    mandatory = list(report["checks"].values())
    report["status"] = "PASS" if all(mandatory) else "FAIL"
    return report


def smoke(chain: str, q011_path: str | Path, output: str | Path, c: Mapping[str, Any]) -> int:
    q011_vec = q011_exact_shared_vector(c, q011_path)
    prefix = Path(output).with_suffix("").with_name(Path(output).stem + "_cobaya")
    info, _ = build_info(chain, "reference_free_h0", "external", 999, c, q011_vec, prefix, max_evals=4)
    report: dict[str, Any] = {
        "case_id": c["project"]["case_id"], "q": CURRENT_Q, "run_id": RUN_ID,
        "chain": chain, "scientific_result": False, "status": "FAIL", "checks": {}
    }
    try:
        from cobaya.model import get_model
        model = get_model(info)
        sampled = list(model.parameterization.sampled_params())
        ref = model.prior.reference()
        lp = model.logposterior(ref)
        loglikes = getattr(lp, "loglikes", None)
        finite = loglikes is not None and all(math.isfinite(float(x)) for x in loglikes)
        report["checks"]["MODEL_INITIALIZATION_GATE"] = True
        report["checks"]["REFERENCE_POINT_GATE"] = bool(finite)
        report["sampled_parameter_count"] = len(sampled)
        report["sampled_parameters"] = sampled
        if chain.startswith("spt_"):
            cal_ok = {"Tcal", "Ecal"}.issubset(set(sampled))
            report["checks"]["SPT_CALIBRATION_PROFILE_GATE"] = cal_ok
        else:
            cal_ok = True
        report["status"] = "PASS" if finite and cal_ok else "FAIL"
    except Exception as exc:
        report["checks"]["MODEL_INITIALIZATION_GATE"] = False
        report["error"] = repr(exc)
    dump_json(output, report)
    return 0 if report["status"] == "PASS" else 8


def cli() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=CONFIG_NAME)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--depth", choices=["standard", "expanded"], default="standard")
    p.add_argument("--output", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--q011", required=True)
    p.add_argument("--environment", action="store_true")
    p.add_argument("--chain", choices=["planck_npipe_k039_approx", "spt_d1_only", "spt_d1_plus_desi"])
    p.add_argument("--output", required=True)

    p = sub.add_parser("smoke")
    p.add_argument("--chain", choices=["planck_npipe_k039_approx", "spt_d1_only", "spt_d1_plus_desi"], required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("run")
    p.add_argument("--chain", choices=["planck_npipe_k039_approx", "spt_d1_only", "spt_d1_plus_desi"], required=True)
    p.add_argument("--mode", choices=["reference_free_h0", "fixed_h0_71p5", "q011_shared_physics"], required=True)
    p.add_argument("--start-family", choices=["external", "q011", "baseline", "jitter_a", "jitter_b"], required=True)
    p.add_argument("--restart-index", type=int, required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--max-evals", type=int)
    p.add_argument("--output", required=True)

    args = ap.parse_args()
    c = load_yaml(args.config)
    if args.cmd == "plan":
        tasks = expected_tasks(c, args.depth)
        dump_json(args.output, {"include": tasks})
        print(json.dumps({"include": tasks}, separators=(",", ":")))
        return 0
    if args.cmd == "preflight":
        r = preflight(c, args.q011, args.environment, args.chain)
        dump_json(args.output, r)
        print(json.dumps(r, indent=2))
        return 0 if r["status"] == "PASS" else 7
    if args.cmd == "smoke":
        return smoke(args.chain, args.q011, args.output, c)
    if args.cmd == "run":
        return run_task(args.chain, args.mode, args.start_family, args.restart_index,
                        args.q011, args.output, c, args.max_evals)
    return 2


if __name__ == "__main__":
    raise SystemExit(cli())
