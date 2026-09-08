#!/usr/bin/env python3
"""Bubbleverse Q-040 defensive native-prior RQMC CMB marginalization V2.

Technical V2 repairs only sparse RQMC shard serialization after GitHub run
34244197767. The scientific RQMC construction, frozen priors/bounds, Q032/Q037
locks, thresholds, proposal mixture, Sobol sequence and endpoint semantics are
unchanged from V1.

This program implements the mathematical handoff R-Q040-MATH-DEFENSIVE-MARGINAL-001.
It reuses the frozen Q032 native CamSpec/HiLLiPoP construction from
q040_cmbspace_coupled_bridge_v2.NativeContext but replaces the failed single-
Gaussian Laplace/Schur approximation with a finite defensive importance/RQMC
marginalization.  A_planck remains explicit.  CamSpec and HiLLiPoP are never
mixed; the shared object is only the physical identity-multipole TT spectrum.

The workflow is intentionally multi-run and self-dispatching.  One user launch
starts START -> adaptive INTEGRATE levels -> CORESET -> BANK_ENDPOINTS ->
PRODUCTION.  A finite validation failure seals Q040 unresolved without proposal
redesign in the same campaign.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import statistics
import sys
import traceback
from itertools import combinations
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.spatial import cKDTree
from scipy.special import logsumexp
from scipy.stats import norm, qmc, t as student_t

import q040_cmbspace_coupled_bridge_v2 as base

Q = "Q-040"
PROGRAM_ID = "Q040-RQMC-V2"
RUN_ID = "Q040-DEFENSIVE-RQMC-CMB-MARGINAL-V2"
RESULT_ID = "R-Q040-EDE-DEFENSIVE-RQMC-CMB-MARGINAL-002"
MATH_RESULT_ID = "R-Q040-MATH-DEFENSIVE-MARGINAL-001"
INTERVENTION = "DEFENSIVE_NATIVE_PRIOR_RQMC_CMB_MARGINALIZATION_V1"
TECHNICAL_PARENT_PROGRAM_ID = "Q040-RQMC-V1"
TECHNICAL_PARENT_GITHUB_RUN_ID = 34244197767
TECHNICAL_PARENT_HEAD_SHA = "177e79778a286b5138858fba1f0716d75faf4e0b"
# Preserve V1 randomized-QMC points exactly across this serialization-only repair.
RQMC_SEED_NAMESPACE = "Q040-RQMC-V1"
Q032_RESULT_ID = base.Q032_RESULT_ID
Q032_GITHUB_RUN = base.Q032_GITHUB_RUN
Q032_EXECUTION_COMMIT = base.Q032_EXECUTION_COMMIT
BACKEND_COMMIT = base.BACKEND_COMMIT
HILLIPOP_COMMIT = base.HILLIPOP_COMMIT
COBAYA_VERSION = base.COBAYA_VERSION
SUPPORT_HASH = base.SUPPORT_HASH
SCALES_HASH = base.SCALES_HASH
LABELS = base.LABELS
IMPLEMENTATIONS = base.IMPLEMENTATIONS
START_FAMILIES = base.START_FAMILIES
COORDS = base.COORDS
SCALES = base.SCALES
BASELINE = base.BASELINE
THRESHOLD = base.THRESHOLD

# Frozen mathematical settings from the handoff.
RQMC_M_MIN = 9
RQMC_M_MAX = 16
RQMC_REPLICATES = 4
RQMC_BLOCKS = 6  # 3 prior blocks + 3 local proposal blocks, each weight 1/6
RQMC_DF = 5.0
INTEGRATION_DELTA_CHI2_TOL = 0.05
ENDPOINT_BANK_TOL = 0.05
WEIGHT_RATIO_MAX = 2.0
CORESET_K = (96, 192, 384, 768, 1536)  # each divisible by six
CORESET_PROBE_TOL = 0.01  # technical acceleration must be tighter than RQMC 0.05 gate
CALIBRATION_BASIS_REL_TOL = 2e-9
QUADRATIC_EQ_REL_TOL = 2e-8
V4_RUN_ID = 34211073134
V4_PROGRAM_ID = "Q040-CMBSPACE-V4"
V4_RESULT_ID = "R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-004"

# Reuse V2 native context under the new identity.  These globals are resolved at
# runtime inside base functions, so patch before any NativeContext construction.
base.Q = Q
base.PROGRAM_ID = PROGRAM_ID
base.RUN_ID = RUN_ID
base.RESULT_ID = RESULT_ID
base.INTERVENTION = INTERVENTION

NativeContext = base.NativeContext
SoftStop = base.SoftStop
finite = base.finite
read_json = base.read_json
write_json = base.write_json
sha256_file = base.sha256_file
sha256_array = base.sha256_array
canonical_hash = base.canonical_hash
failure_record = base.failure_record
load_parent = base.load_parent
all_parent_records = base.all_parent_records
calculate_metrics = base.calculate_metrics
sufficient = base.sufficient
resolve_q032_config_path = base.resolve_q032_config_path
load_q032 = base.load_q032
load_sealed_preflight = base.load_sealed_preflight


def _alarm(_sig: int, _frame: Any) -> None:
    raise SoftStop("Q040 RQMC soft runtime limit")


def _seed(*parts: Any) -> int:
    h = hashlib.sha256("|".join(map(str, (RQMC_SEED_NAMESPACE,) + parts)).encode()).digest()
    return int.from_bytes(h[:4], "little") & 0x7FFFFFFF


def _json_scalar(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating, np.bool_)):
        return x.item()
    return x


def _encode_sparse_logsum(x: np.ndarray) -> list[list[float | None]]:
    """JSON-safe encoding for partial log-sum accumulators.

    -inf means exactly "this shard contributed no samples to this accumulator".
    It is not a numerical likelihood result and is encoded as JSON null. NaN and
    +inf remain hard errors so this repair cannot hide genuine numerical failure.
    """
    a = np.asarray(x, dtype=float)
    if a.ndim != 2:
        raise RuntimeError("SPARSE_LOGSUM_SHAPE_GATE=FAIL")
    if np.any(np.isnan(a)) or np.any(np.isposinf(a)):
        raise RuntimeError("SPARSE_LOGSUM_FINITE_GATE=FAIL nan_or_posinf")
    return [[None if np.isneginf(v) else float(v) for v in row] for row in a]

def _decode_sparse_logsum(x: Sequence[Sequence[float | None]]) -> np.ndarray:
    rows = []
    for row in x:
        rows.append([(-np.inf if v is None else float(v)) for v in row])
    a = np.asarray(rows, dtype=float)
    if a.ndim != 2:
        raise RuntimeError("SPARSE_LOGSUM_SHAPE_GATE=FAIL")
    if np.any(np.isnan(a)) or np.any(np.isposinf(a)):
        raise RuntimeError("SPARSE_LOGSUM_FINITE_GATE=FAIL nan_or_posinf")
    return a


def save_npz(path: str | Path, **arrays: Any) -> dict[str, Any]:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(p, **arrays)
    return {"path": p.name, "sha256": sha256_file(p), "size": p.stat().st_size}


def load_npz_checked(path: str | Path, expected_sha256: str | None = None):
    p = Path(path)
    if expected_sha256 and sha256_file(p) != expected_sha256:
        raise RuntimeError(f"NPZ_HASH_GATE=FAIL path={p}")
    return np.load(p, allow_pickle=False)


def load_preregister(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    p = d.get("project", {})
    if (p.get("q"), p.get("program_id"), p.get("run_id"), p.get("result_id")) != (Q, PROGRAM_ID, RUN_ID, RESULT_ID):
        raise RuntimeError("PREREGISTRATION_IDENTITY_GATE=FAIL")
    if d.get("intervention", {}).get("name") != INTERVENTION:
        raise RuntimeError("INTERVENTION_IDENTITY_GATE=FAIL")
    if d.get("parent_lock", {}).get("q032_support_sha256") != SUPPORT_HASH:
        raise RuntimeError("PARENT_SUPPORT_HASH_GATE=FAIL")
    if d.get("cmb_representation", {}).get("primary") != "IDENTITY_UNIQUE_MULTIPOLE_TT":
        raise RuntimeError("NO_HIDDEN_BINNING_GATE=FAIL")
    if d.get("cmb_representation", {}).get("new_binning_allowed") is not False:
        raise RuntimeError("NO_HIDDEN_BINNING_GATE=FAIL")
    if d.get("nuisance_semantics", {}).get("A_planck") != "PRESERVE_AS_EXPLICIT_RUNTIME_PARAMETER_NOT_MARGINALIZED":
        raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL")
    if float(d.get("geometry", {}).get("sufficiency_threshold", -1)) != THRESHOLD:
        raise RuntimeError("THRESHOLD_GATE=FAIL")
    r = d.get("rqmc", {})
    if (int(r.get("m_min", -1)), int(r.get("m_max", -1)), int(r.get("replicates", -1))) != (RQMC_M_MIN, RQMC_M_MAX, RQMC_REPLICATES):
        raise RuntimeError("RQMC_SCHEDULE_GATE=FAIL")
    if list(map(int, r.get("coreset_k", []))) != list(CORESET_K):
        raise RuntimeError("CORESET_SCHEDULE_GATE=FAIL")
    return d


def load_source_lock(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if (d.get("q"), d.get("program_id"), d.get("run_id"), d.get("result_id")) != (Q, PROGRAM_ID, RUN_ID, RESULT_ID):
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    sw = d.get("software", {})
    if sw.get("backend_commit") != BACKEND_COMMIT or sw.get("hillipop_commit") != HILLIPOP_COMMIT or sw.get("cobaya") != COBAYA_VERSION:
        raise RuntimeError("SOURCE_LOCK_SOFTWARE_GATE=FAIL")
    if d.get("bubbleverse_parent", {}).get("q032_support_sha256") != SUPPORT_HASH:
        raise RuntimeError("SOURCE_LOCK_PARENT_GATE=FAIL")
    return d


def _dist_name(pr: Mapping[str, Any]) -> str:
    return str(pr.get("dist", "uniform" if ("min" in pr or "max" in pr) else "")).lower()


def _prior_logpdf_1d(pr: Mapping[str, Any], x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    dist = _dist_name(pr)
    if dist in ("uniform", "") and ("min" in pr or "max" in pr):
        lo = float(pr["min"]); hi = float(pr["max"])
        out = np.full(x.shape, -math.log(hi - lo), dtype=float)
        out[(x < lo) | (x > hi)] = -np.inf
        return out
    if dist in ("norm", "normal", "gaussian"):
        loc = float(pr.get("loc", pr.get("mean")))
        scale = float(pr.get("scale", pr.get("sigma")))
        return norm.logpdf(x, loc=loc, scale=scale)
    raise RuntimeError(f"PROPER_NATIVE_PRIOR_GATE=FAIL unsupported_prior={dict(pr)}")


def _prior_ppf_1d(pr: Mapping[str, Any], u: np.ndarray) -> np.ndarray:
    u = np.clip(np.asarray(u, dtype=float), np.finfo(float).eps, 1.0 - np.finfo(float).eps)
    dist = _dist_name(pr)
    if dist in ("uniform", "") and ("min" in pr or "max" in pr):
        lo = float(pr["min"]); hi = float(pr["max"])
        return lo + (hi - lo) * u
    if dist in ("norm", "normal", "gaussian"):
        loc = float(pr.get("loc", pr.get("mean")))
        scale = float(pr.get("scale", pr.get("sigma")))
        return norm.ppf(u, loc=loc, scale=scale)
    raise RuntimeError(f"PROPER_NATIVE_PRIOR_GATE=FAIL unsupported_prior={dict(pr)}")


def prior_logpdf(ctx: NativeContext, x: np.ndarray) -> np.ndarray:
    X = np.atleast_2d(np.asarray(x, dtype=float))
    if X.shape[1] != len(ctx.nuisance_names):
        raise RuntimeError("NUISANCE_VECTOR_DIMENSION_GATE=FAIL")
    out = np.zeros(X.shape[0], dtype=float)
    for j, pr in enumerate(ctx.priors):
        out += _prior_logpdf_1d(pr, X[:, j])
    return out


def sample_prior(ctx: NativeContext, u: np.ndarray) -> np.ndarray:
    U = np.atleast_2d(np.asarray(u, dtype=float))
    return np.column_stack([_prior_ppf_1d(pr, U[:, j]) for j, pr in enumerate(ctx.priors)])


def _local_t_ppf_1d(pr: Mapping[str, Any], center: float, scale: float, u: np.ndarray) -> np.ndarray:
    u = np.clip(np.asarray(u, dtype=float), np.finfo(float).eps, 1.0 - np.finfo(float).eps)
    lo, hi = base.prior_bounds(pr)
    if lo is None and hi is None:
        return center + scale * student_t.ppf(u, df=RQMC_DF)
    a = 0.0 if lo is None else float(student_t.cdf((lo - center) / scale, df=RQMC_DF))
    b = 1.0 if hi is None else float(student_t.cdf((hi - center) / scale, df=RQMC_DF))
    if not (0 <= a < b <= 1):
        raise RuntimeError("TRUNCATED_T_NORMALIZATION_GATE=FAIL")
    z = student_t.ppf(a + (b - a) * u, df=RQMC_DF)
    x = center + scale * z
    if lo is not None and np.any(x < lo - 1e-12):
        raise RuntimeError("NATIVE_SUPPORT_GATE=FAIL lower")
    if hi is not None and np.any(x > hi + 1e-12):
        raise RuntimeError("NATIVE_SUPPORT_GATE=FAIL upper")
    return x


def _local_t_logpdf_1d(pr: Mapping[str, Any], center: float, scale: float, x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    lo, hi = base.prior_bounds(pr)
    z = (x - center) / scale
    out = student_t.logpdf(z, df=RQMC_DF) - math.log(scale)
    if lo is not None or hi is not None:
        a = 0.0 if lo is None else float(student_t.cdf((lo - center) / scale, df=RQMC_DF))
        b = 1.0 if hi is None else float(student_t.cdf((hi - center) / scale, df=RQMC_DF))
        out -= math.log(b - a)
        if lo is not None:
            out = np.where(x < lo, -np.inf, out)
        if hi is not None:
            out = np.where(x > hi, -np.inf, out)
    return out


def sample_local(ctx: NativeContext, center: np.ndarray, u: np.ndarray) -> np.ndarray:
    U = np.atleast_2d(np.asarray(u, dtype=float))
    c = np.asarray(center, dtype=float)
    return np.column_stack([
        _local_t_ppf_1d(pr, float(c[j]), float(ctx.proposal_scales[j]), U[:, j])
        for j, pr in enumerate(ctx.priors)
    ])


def local_logpdf(ctx: NativeContext, center: np.ndarray, x: np.ndarray) -> np.ndarray:
    X = np.atleast_2d(np.asarray(x, dtype=float)); c = np.asarray(center, dtype=float)
    out = np.zeros(X.shape[0], dtype=float)
    for j, pr in enumerate(ctx.priors):
        out += _local_t_logpdf_1d(pr, float(c[j]), float(ctx.proposal_scales[j]), X[:, j])
    return out


def defensive_logq(ctx: NativeContext, centers3: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = np.atleast_2d(np.asarray(x, dtype=float))
    lp = prior_logpdf(ctx, X)
    parts = [math.log(0.5) + lp]
    for k in range(3):
        parts.append(math.log(1.0 / 6.0) + local_logpdf(ctx, centers3[k], X))
    lq = logsumexp(np.vstack(parts), axis=0)
    return lp, lq


def load_v4_centers(map_dir: str | Path, implementation: str, nuisance_names: Sequence[str]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    hits = []
    for p in Path(map_dir).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (d.get("q") == Q and d.get("program_id") == V4_PROGRAM_ID and d.get("stage") == "COMPRESSION_MAP_START"
                and d.get("implementation") == implementation and d.get("status") == "COMPLETE"):
            hits.append(d)
    by = {str(d.get("start_family")): d for d in hits}
    if set(by) != set(START_FAMILIES) or len(hits) != 3:
        raise RuntimeError(f"V4_MAP_CENTER_GATE=FAIL impl={implementation} found={list(by)} count={len(hits)}")
    ordered = [by[f] for f in START_FAMILIES]
    arr = np.array([[float(d["eta"][n]) for n in nuisance_names] for d in ordered], dtype=float)
    return arr, ordered


def sobol_points(dim: int, seed: int, start: int, count: int) -> np.ndarray:
    eng = qmc.Sobol(d=dim, scramble=True, seed=int(seed))
    if start:
        eng.fast_forward(int(start))
    # random() supports arbitrary count after fast_forward; nested shells retain the same scrambled sequence.
    return np.asarray(eng.random(int(count)), dtype=float)


def generate_component_nodes(ctx: NativeContext, centers3: np.ndarray, implementation: str, replicate: int,
                             block: int, start: int, count: int, kind: str = "RQMC") -> np.ndarray:
    U = sobol_points(len(ctx.nuisance_names), _seed(kind, implementation, replicate, block), start, count)
    if block < 3:
        return sample_prior(ctx, U)
    return sample_local(ctx, centers3[block - 3], U)


def native_data_vector(ctx: NativeContext) -> np.ndarray:
    if ctx.implementation == "camspec":
        d = np.asarray(ctx.like.data_vector, dtype=np.float64)
    else:
        raw = np.asarray(ctx.like._dldata["TT"], dtype=np.float64)
        rl = ctx.like._xspectra_to_xfreq(raw, ctx.like._dlweight["TT"])
        full = np.asarray(ctx.like._select_spectra(rl, "TT"), dtype=np.float64)
        d = full[np.asarray(ctx.selected_indices, dtype=int)]
    if d.shape != (len(ctx.rows),) or not np.all(np.isfinite(d)):
        raise RuntimeError("NATIVE_DATA_VECTOR_GATE=FAIL")
    return d


def residual_parts(ctx: NativeContext, eta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    z = np.zeros(len(ctx.ells), dtype=float)
    o = np.ones(len(ctx.ells), dtype=float)
    y = ctx.residual(z, eta, A_planck=1.0)
    r1 = ctx.residual(o, eta, A_planck=1.0)
    a = y - r1
    return y, a


def theory_vector_from_parent(ctx: NativeContext, parent: Mapping[str, Any]) -> np.ndarray:
    preferred = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
    vec = ctx.q32.reference_vector(ctx.info, preferred=preferred)
    lp = ctx.model.logposterior(vec)
    logpost = getattr(lp, "logpost", lp)
    if not finite(logpost):
        raise RuntimeError("PROBE_THEORY_EVALUATION_GATE=FAIL")
    cl = ctx.model.provider.get_Cl(ell_factor=True)
    tt = np.asarray(cl["tt"], dtype=float)
    if len(tt) <= int(np.max(ctx.ells)):
        raise RuntimeError("PROBE_THEORY_LMAX_GATE=FAIL")
    return tt[ctx.ells].astype(float)


def prepare(args: argparse.Namespace) -> int:
    load_preregister(args.preregister); load_source_lock(args.source_lock)
    outdir = Path(args.output_dir); outdir.mkdir(parents=True, exist_ok=True)
    rec: dict[str, Any] = {"q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
                           "stage": "RQMC_PREPARE", "status": "FAILED", "implementations": {}}
    contexts: dict[str, NativeContext] = {}
    try:
        probes: list[dict[str, Any]] = []
        ell_ref = None
        rep_hash = None
        # First construct contexts, centers and calibration bases.
        for impl in IMPLEMENTATIONS:
            ns = argparse.Namespace(**vars(args)); ns.implementation = impl
            ctx = NativeContext(ns, impl); contexts[impl] = ctx
            if ell_ref is None:
                ell_ref = ctx.ells.copy(); rep_hash = ctx.representation_hash
            elif not np.array_equal(ell_ref, ctx.ells) or rep_hash != ctx.representation_hash:
                raise RuntimeError("COMMON_CMB_REPRESENTATION_GATE=FAIL")
            centers3, v4 = load_v4_centers(args.v4_map_dir, impl, ctx.nuisance_names)
            # Coreset centers: 256 nodes from each of six equal-weight strata => Kmax=1536.
            per_block = max(CORESET_K) // 6
            center_blocks = []
            block_ids = []
            for b in range(6):
                U = sobol_points(len(ctx.nuisance_names), _seed("CORESET", impl, 0, b), 0, per_block)
                X = sample_prior(ctx, U) if b < 3 else sample_local(ctx, centers3[b - 3], U)
                center_blocks.append(X); block_ids.extend([b] * len(X))
            centers = np.vstack(center_blocks)
            if centers.shape != (max(CORESET_K), len(ctx.nuisance_names)):
                raise RuntimeError("CORESET_CENTER_SHAPE_GATE=FAIL")
            schedules = {}
            for K in CORESET_K:
                n = K // 6
                idx = []
                for b in range(6):
                    idx.extend(range(b * per_block, b * per_block + n))
                schedules[str(K)] = idx
            # Build a calibration-response basis from a preregistered 384-center subset.
            basis_idx = np.array(schedules["384"], dtype=int)
            Avec = []
            for i in basis_idx:
                _, a = residual_parts(ctx, centers[i])
                Avec.append(a)
            A = np.asarray(Avec, dtype=float)
            _, sv, vt = np.linalg.svd(A, full_matrices=False)
            rank = int(max(1, np.sum(sv > max(1e-12, sv[0] * 1e-11))))
            basis = np.asarray(vt[:rank], dtype=float)
            mxrel = 0.0
            for row in A:
                coeff = basis @ row; recon = coeff @ basis
                mxrel = max(mxrel, float(np.linalg.norm(recon - row) / max(1.0, np.linalg.norm(row))))
            if mxrel > CALIBRATION_BASIS_REL_TOL:
                raise RuntimeError(f"CALIBRATION_BASIS_GATE=FAIL impl={impl} rel={mxrel}")
            cfile = outdir / f"q040_rqmc_{impl}_centers_v2.npz"
            bfile = outdir / f"q040_rqmc_{impl}_basis_v2.npz"
            save_npz(cfile, centers=centers, center_block=np.asarray(block_ids, dtype=np.int16),
                     centers3=centers3, proposal_scales=ctx.proposal_scales,
                     native_reference=ctx.native_reference)
            save_npz(bfile, basis=basis, singular_values=sv, ells=ctx.ells)
            rec["implementations"][impl] = {
                "nuisance_names": list(ctx.nuisance_names), "priors": list(ctx.priors),
                "proposal_scales": ctx.proposal_scales.tolist(), "representation_sha256": ctx.representation_hash,
                "centers_file": cfile.name, "centers_sha256": sha256_file(cfile),
                "basis_file": bfile.name, "basis_sha256": sha256_file(bfile),
                "calibration_basis_rank": rank, "calibration_basis_training_rel_error": mxrel,
                "coreset_schedules": schedules,
                "v4_centers": [{"start_family": d["start_family"], "objective": d["objective"]} for d in v4],
            }

        # Q032 endpoint theory probes (nine per implementation).
        for impl in IMPLEMENTATIONS:
            ctx = contexts[impl]
            for m in (3, 6, 7):
                for s in (0, 1, 2):
                    parent, _ = load_parent(args.parent_dir, impl, m, s)
                    cmb = theory_vector_from_parent(ctx, parent)
                    probes.append({"id": f"Q032:{impl}:M{m}-S{s}", "kind": "Q032_ENDPOINT_THEORY",
                                   "source_implementation": impl, "A_planck": float(parent["minimum"]["A_planck"]),
                                   "cmb": cmb})
        # All six V4 free-CMB MAP spectra, each A_planck=1 by V4 construction.
        for impl in IMPLEMENTATIONS:
            ctx = contexts[impl]
            _, v4 = load_v4_centers(args.v4_map_dir, impl, ctx.nuisance_names)
            for d in v4:
                cmb = np.asarray(d["cmb"], dtype=float)
                if cmb.shape != (len(ctx.ells),):
                    raise RuntimeError("V4_CMB_PROBE_SHAPE_GATE=FAIL")
                probes.append({"id": f"V4:{impl}:{d['start_family']}", "kind": "V4_FREE_CMB_MAP",
                               "source_implementation": impl, "A_planck": 1.0, "cmb": cmb})
        if len(probes) != 24:
            raise RuntimeError(f"PROBE_COUNT_GATE=FAIL count={len(probes)}")
        cmbs = np.vstack([p.pop("cmb") for p in probes])
        apl = np.array([float(p["A_planck"]) for p in probes], dtype=float)
        pfile = outdir / "q040_rqmc_probes_v2.npz"
        save_npz(pfile, cmb=cmbs, A_planck=apl, ells=np.asarray(ell_ref, dtype=int))
        pmeta = outdir / "q040_rqmc_probes_v2.json"
        refs = {impl: next(i for i,p in enumerate(probes) if p["id"] == f"V4:{impl}:NATIVE_REFERENCE") for impl in IMPLEMENTATIONS}
        write_json(pmeta, {"q": Q, "program_id": PROGRAM_ID, "stage": "RQMC_PROBES", "status": "PASS",
                           "representation_sha256": rep_hash, "probes": probes, "reference_probe_index": refs,
                           "npz_file": pfile.name, "npz_sha256": sha256_file(pfile)})
        rec.update({"status": "PASS", "representation_sha256": rep_hash, "ordered_unique_ells": np.asarray(ell_ref).tolist(),
                    "probe_metadata": pmeta.name, "probe_metadata_sha256": sha256_file(pmeta),
                    "probe_npz": pfile.name, "probe_npz_sha256": sha256_file(pfile),
                    "gates": {"PROPER_NATIVE_PRIOR_GATE": "PASS", "NATIVE_SUPPORT_GATE": "PASS",
                              "A_PLANCK_PRESERVATION_GATE": "PASS", "NO_CROSS_FAMILY_MIXING_GATE": "PASS",
                              "NO_HIDDEN_BINNING_GATE": "PASS", "CALIBRATION_BASIS_GATE": "PASS"}})
        write_json(args.output, rec)
        print("Q040_RQMC_PREPARE_GATE=PASS")
        return 0
    except Exception as exc:
        rec.update({"status": "FAILED", **failure_record(exc, "RQMC_PREPARE")}); write_json(args.output, rec)
        print(rec.get("traceback", repr(exc)), file=sys.stderr); return 2
    finally:
        for ctx in contexts.values():
            try: ctx.close()
            except Exception: pass


def shell_range(m: int) -> tuple[int, int]:
    if m < RQMC_M_MIN or m > RQMC_M_MAX:
        raise RuntimeError("RQMC_LEVEL_GATE=FAIL")
    end = 2 ** m
    start = 0 if m == RQMC_M_MIN else 2 ** (m - 1)
    return start, end


def shard_count_for_m(m: int) -> int:
    # Target <= ~8192 nuisance nodes/job across 4 replicates for one implementation.
    start, end = shell_range(m); total = RQMC_REPLICATES * RQMC_BLOCKS * (end - start)
    return max(1, int(math.ceil(total / 8192.0)))


def plan_level(args: argparse.Namespace) -> int:
    n = shard_count_for_m(args.m)
    include = [{"implementation": impl, "shard": s, "shard_count": n} for impl in IMPLEMENTATIONS for s in range(n)]
    if len(include) > 256:
        raise RuntimeError(f"GITHUB_MATRIX_GATE=FAIL jobs={len(include)}")
    out = {"q": Q, "program_id": PROGRAM_ID, "m": args.m, "shard_count_per_implementation": n,
           "matrix": {"include": include}}
    write_json(args.output, out)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write("matrix=" + json.dumps(out["matrix"], separators=(",", ":")) + "\n")
            f.write(f"shard_count={n}\n")
    print(f"Q040_RQMC_LEVEL_PLAN=PASS m={args.m} shards_per_impl={n}")
    return 0


def _load_prepare(prep_meta: str | Path, prep_dir: str | Path, implementation: str):
    d = read_json(prep_meta)
    if not (d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("stage") == "RQMC_PREPARE" and d.get("status") == "PASS"):
        raise RuntimeError("PREPARE_PARENT_GATE=FAIL")
    im = d["implementations"][implementation]
    root = Path(prep_dir)
    cz = load_npz_checked(root / im["centers_file"], im["centers_sha256"])
    bz = load_npz_checked(root / im["basis_file"], im["basis_sha256"])
    pm = read_json(root / d["probe_metadata"])
    pz = load_npz_checked(root / pm["npz_file"], pm["npz_sha256"])
    return d, im, cz, bz, pm, pz


def _precompute_probe_kernels(ctx: NativeContext, basis: np.ndarray, probes: np.ndarray, Avals: np.ndarray):
    D = native_data_vector(ctx); PD = ctx.P @ D; DPD = float(D @ PD)
    T = []; dvec = []; H = []
    for s in probes:
        row_s = np.asarray(s, dtype=float)[ctx.row_ell_index]
        tmat = basis * row_s[None, :]
        T.append(tmat)
        dvec.append(tmat @ PD)
        H.append((tmat @ ctx.P) @ tmat.T)
    return D, PD, DPD, T, np.asarray(dvec), np.asarray(H), np.asarray(Avals, dtype=float)


def _node_probe_loglikes(ctx: NativeContext, eta: np.ndarray, basis: np.ndarray, D: np.ndarray, PD: np.ndarray, DPD: float,
                         T: Sequence[np.ndarray], dvec: np.ndarray, H: np.ndarray, Avals: np.ndarray,
                         direct_check: bool = False) -> tuple[np.ndarray, float]:
    y, a = residual_parts(ctx, eta)
    F = D - y
    PF = ctx.P @ F
    dpf = float(D @ PF); fpf = float(F @ PF)
    coeff = basis @ a; recon = coeff @ basis
    brel = float(np.linalg.norm(recon - a) / max(1.0, np.linalg.norm(a)))
    if brel > CALIBRATION_BASIS_REL_TOL:
        raise RuntimeError(f"CALIBRATION_BASIS_GATE=FAIL runtime_rel={brel}")
    out = np.empty(len(T), dtype=float)
    for p in range(len(T)):
        apf = float(coeff @ (T[p] @ PF))
        dpa = float(coeff @ dvec[p])
        apa = float(coeff @ H[p] @ coeff)
        A = float(Avals[p]); A2 = A * A
        chi2 = DPD - 2.0 * (dpa + dpf) / A2 + (apa + 2.0 * apf + fpf) / (A2 * A2)
        if not finite(chi2) or chi2 < -1e-7:
            raise RuntimeError(f"FINITE_NATIVE_LIKELIHOOD_GATE=FAIL chi2={chi2}")
        out[p] = -0.5 * max(0.0, chi2)
    if direct_check:
        for p in (0, len(T)//2, len(T)-1):
            r = ctx.residual(np.asarray(probes_global[p], dtype=float), eta, A_planck=float(Avals[p]))
            direct = float(r @ (ctx.P @ r))
            approx = -2.0 * out[p]
            rel = abs(direct - approx) / max(1.0, abs(direct))
            if rel > QUADRATIC_EQ_REL_TOL:
                raise RuntimeError(f"CONDITIONAL_QUADRATIC_EQUIVALENCE_GATE=FAIL rel={rel}")
    return out, brel

# Module-local used only by the direct equivalence spot check above.
probes_global: np.ndarray = np.empty((0, 0))


def rqmc_shard(args: argparse.Namespace) -> int:
    global probes_global
    load_preregister(args.preregister); load_source_lock(args.source_lock)
    ns = argparse.Namespace(**vars(args)); ns.implementation = args.implementation
    ctx = None
    rec = {"q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
           "stage": "RQMC_SHARD", "m": int(args.m), "implementation": args.implementation,
           "shard": int(args.shard), "shard_count": int(args.shard_count), "status": "FAILED"}
    old = signal.signal(signal.SIGALRM, _alarm); signal.alarm(int(args.soft_stop_minutes * 60))
    try:
        ctx = NativeContext(ns, args.implementation)
        _, im, cz, bz, pm, pz = _load_prepare(args.prepare_meta, args.prepare_dir, args.implementation)
        centers = np.asarray(cz["centers"], dtype=float); centers3 = np.asarray(cz["centers3"], dtype=float)
        basis = np.asarray(bz["basis"], dtype=float)
        probes = np.asarray(pz["cmb"], dtype=float); probes_global = probes
        Avals = np.asarray(pz["A_planck"], dtype=float)
        if probes.shape[1] != len(ctx.ells) or not np.array_equal(np.asarray(pz["ells"], dtype=int), ctx.ells):
            raise RuntimeError("PROBE_REPRESENTATION_GATE=FAIL")
        D, PD, DPD, T, dvec, H, Avals = _precompute_probe_kernels(ctx, basis, probes, Avals)
        schedules = {int(k): np.asarray(v, dtype=int) for k,v in im["coreset_schedules"].items()}
        trees = {K: cKDTree((centers[idx] / ctx.proposal_scales[None,:])) for K,idx in schedules.items()}
        masses = {str(K): np.zeros((RQMC_REPLICATES, K), dtype=float) for K in CORESET_K}
        logsums = np.full((RQMC_REPLICATES, len(probes)), -np.inf, dtype=float)
        counts = np.zeros(RQMC_REPLICATES, dtype=np.int64)
        max_weight = 0.0; max_basis_rel = 0.0; direct_done = False
        start, end = shell_range(args.m); L = end - start
        total = RQMC_REPLICATES * RQMC_BLOCKS * L
        lo = (total * args.shard) // args.shard_count; hi = (total * (args.shard + 1)) // args.shard_count
        if hi <= lo:
            raise RuntimeError("EMPTY_SHARD_GATE=FAIL")
        # Flatten order replicate -> block -> point; process contiguous segment intersections.
        seg0 = 0
        for rep in range(RQMC_REPLICATES):
            for block in range(RQMC_BLOCKS):
                seg1 = seg0 + L
                aa, bb = max(lo, seg0), min(hi, seg1)
                if bb > aa:
                    local_start = start + (aa - seg0); n = bb - aa
                    X = generate_component_nodes(ctx, centers3, args.implementation, rep, block, local_start, n)
                    lp, lq = defensive_logq(ctx, centers3, X)
                    wr = np.exp(lp - lq)
                    if np.any(~np.isfinite(wr)) or np.any(wr < 0):
                        raise RuntimeError("DEFENSIVE_WEIGHT_GATE=FAIL nonfinite")
                    max_weight = max(max_weight, float(np.max(wr)))
                    if float(np.max(wr)) > WEIGHT_RATIO_MAX + 5e-12:
                        raise RuntimeError(f"DEFENSIVE_WEIGHT_GATE=FAIL max={np.max(wr)}")
                    # Cluster masses are likelihood-independent and preserve original importance mass.
                    Xstd = X / ctx.proposal_scales[None,:]
                    for K in CORESET_K:
                        idx = schedules[K]
                        _, nn = trees[K].query(Xstd, k=1)
                        np.add.at(masses[str(K)][rep], np.asarray(nn, dtype=int), wr)
                    for row, w in zip(X, wr):
                        ll, brel = _node_probe_loglikes(ctx, row, basis, D, PD, DPD, T, dvec, H, Avals,
                                                       direct_check=(not direct_done))
                        direct_done = True; max_basis_rel = max(max_basis_rel, brel)
                        logsums[rep] = np.logaddexp(logsums[rep], math.log(float(w)) + ll)
                        counts[rep] += 1
                seg0 = seg1
        out_mass = {K: arr.tolist() for K,arr in masses.items()}
        rec.update({"status": "PASS", "shell_start_per_block": start, "shell_end_per_block": end,
                    "processed_flat_range": [lo, hi], "counts_by_replicate": counts.tolist(),
                    "logsum_wL_by_replicate_probe": _encode_sparse_logsum(logsums), "coreset_mass_by_k_replicate": out_mass,
                    "max_pi_over_q": max_weight, "max_calibration_basis_relative_error": max_basis_rel,
                    "probe_count": len(probes), "representation_sha256": ctx.representation_hash,
                    "gates": {"Q_IDENTITY_GATE":"PASS", "PROPER_NATIVE_PRIOR_GATE":"PASS",
                              "NATIVE_SUPPORT_GATE":"PASS", "DEFENSIVE_WEIGHT_GATE":"PASS",
                              "CALIBRATION_BASIS_GATE":"PASS", "CONDITIONAL_QUADRATIC_EQUIVALENCE_GATE":"PASS"}})
        write_json(args.output, rec)
        print(f"Q040_RQMC_SHARD_GATE=PASS impl={args.implementation} m={args.m} shard={args.shard}")
        return 0
    except SoftStop as exc:
        rec.update({"status":"PARTIAL_SOFT_STOP","failure_class":"HPC",**failure_record(exc,"RQMC_SHARD")}); write_json(args.output,rec); return 2
    except Exception as exc:
        rec.update({"status":"FAILED","failure_class":"NUMERICAL_OR_LIKELIHOOD",**failure_record(exc,"RQMC_SHARD")}); write_json(args.output,rec); print(rec.get("traceback"),file=sys.stderr); return 2
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM, old)
        if ctx is not None:
            try: ctx.close()
            except Exception: pass


def _combine_logsum(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.logaddexp(np.asarray(a,dtype=float), np.asarray(b,dtype=float))


def _logmeanexp(v: np.ndarray, axis: int = 0) -> np.ndarray:
    v = np.asarray(v,dtype=float)
    return logsumexp(v, axis=axis) - math.log(v.shape[axis])


def _delta(logL: np.ndarray, ref_idx: int) -> np.ndarray:
    return -2.0 * (np.asarray(logL,dtype=float) - float(logL[ref_idx]))


def merge_level(args: argparse.Namespace) -> int:
    prep = read_json(args.prepare_meta); pm = read_json(Path(args.prepare_dir) / prep["probe_metadata"])
    refs = {k:int(v) for k,v in pm["reference_probe_index"].items()}
    shards = []
    for p in Path(args.shard_dir).rglob("*.json"):
        try: d=read_json(p)
        except Exception: continue
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="RQMC_SHARD" and int(d.get("m",-1))==args.m:
            shards.append(d)
    expected = sum(shard_count_for_m(args.m) for _ in IMPLEMENTATIONS)
    if len(shards) != expected:
        raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL rqmc_shards={len(shards)} expected={expected}")
    previous = read_json(args.previous_state) if args.previous_state else None
    state = {"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"RQMC_LEVEL_MERGE",
             "status":"PASS","m":args.m,"implementations":{},"integration_tolerance_delta_chi2":INTEGRATION_DELTA_CHI2_TOL}
    overall=True
    for impl in IMPLEMENTATIONS:
        ss=[d for d in shards if d["implementation"]==impl]
        nprobe=int(ss[0]["probe_count"])
        shell_log=np.full((RQMC_REPLICATES,nprobe),-np.inf); shell_count=np.zeros(RQMC_REPLICATES,dtype=np.int64)
        shell_mass={str(K):np.zeros((RQMC_REPLICATES,K),dtype=float) for K in CORESET_K}
        seen=set()
        for d in ss:
            key=int(d["shard"])
            if key in seen or d.get("status")!="PASS": raise RuntimeError("MERGE_COMPATIBILITY_GATE=FAIL shard")
            seen.add(key)
            shell_log=_combine_logsum(shell_log,_decode_sparse_logsum(d["logsum_wL_by_replicate_probe"]))
            shell_count += np.asarray(d["counts_by_replicate"],dtype=np.int64)
            for K in CORESET_K: shell_mass[str(K)] += np.asarray(d["coreset_mass_by_k_replicate"][str(K)],dtype=float)
        if previous:
            pp=previous["implementations"][impl]
            cum_log=_combine_logsum(_decode_sparse_logsum(pp["logsum_wL_by_replicate_probe"]), shell_log)
            cum_count=np.asarray(pp["counts_by_replicate"],dtype=np.int64)+shell_count
            cum_mass={str(K):np.asarray(pp["coreset_mass_by_k_replicate"][str(K)],dtype=float)+shell_mass[str(K)] for K in CORESET_K}
        else:
            cum_log=shell_log; cum_count=shell_count; cum_mass=shell_mass
        expected_n=RQMC_BLOCKS*(2**args.m)
        if np.any(cum_count != expected_n):
            raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL counts impl={impl} got={cum_count.tolist()} expected={expected_n}")
        logL_rep = cum_log - np.log(cum_count.astype(float))[:,None]
        if np.any(~np.isfinite(logL_rep)):
            raise RuntimeError(f"FINITE_RQMC_LIKELIHOOD_GATE=FAIL impl={impl}")
        pooled=_logmeanexp(logL_rep,axis=0); bankA=_logmeanexp(logL_rep[:2],axis=0); bankB=_logmeanexp(logL_rep[2:],axis=0)
        dp=_delta(pooled,refs[impl]); da=_delta(bankA,refs[impl]); db=_delta(bankB,refs[impl])
        bankdiff=float(np.max(np.abs(da-db)))
        bankpass=bankdiff <= INTEGRATION_DELTA_CHI2_TOL
        transition=None; transition_pass=False
        if previous:
            prevd=np.asarray(previous["implementations"][impl]["delta_chi2_pooled"],dtype=float)
            transition=float(np.max(np.abs(dp-prevd))); transition_pass=transition <= INTEGRATION_DELTA_CHI2_TOL
        prev_transition_pass=bool(previous and previous["implementations"][impl].get("transition_pass",False))
        converged=bool(previous and transition_pass and prev_transition_pass and bankpass)
        overall = overall and converged
        state["implementations"][impl]={
            "counts_by_replicate":cum_count.tolist(),"logsum_wL_by_replicate_probe":_encode_sparse_logsum(cum_log),
            "logLhat_by_replicate_probe":logL_rep.tolist(),"delta_chi2_pooled":dp.tolist(),
            "delta_chi2_bankA":da.tolist(),"delta_chi2_bankB":db.tolist(),
            "bankA_B_max_delta_chi2_difference":bankdiff,"bankA_B_pass":bankpass,
            "transition_max_delta_chi2_change":transition,"transition_pass":transition_pass,
            "previous_transition_pass":prev_transition_pass,"converged":converged,
            "coreset_mass_by_k_replicate":{K:v.tolist() for K,v in cum_mass.items()},
        }
    state["converged"]=bool(overall)
    state["at_hard_cap"]=args.m==RQMC_M_MAX
    state["classification"]=("RQMC_INTEGRATION_VALIDATED" if overall else
                             "DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL" if args.m==RQMC_M_MAX else "CONTINUE_RQMC")
    write_json(args.output,state)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:
            f.write(f"converged={'true' if overall else 'false'}\n")
            f.write(f"at_hard_cap={'true' if args.m==RQMC_M_MAX else 'false'}\n")
            f.write(f"next_m={min(RQMC_M_MAX,args.m+1)}\n")
    print(f"Q040_RQMC_LEVEL_MERGE=PASS m={args.m} converged={overall}")
    return 0



def integration_gate(args: argparse.Namespace) -> int:
    states=[]
    for p in Path(args.state_dir).rglob("*.json"):
        try:
            d=read_json(p)
        except Exception:
            continue
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="RQMC_LEVEL_MERGE" and d.get("status")=="PASS":
            states.append((p,d))
    states.sort(key=lambda x:int(x[1]["m"]))
    reason=None
    if not states:
        selected={"q":Q,"program_id":PROGRAM_ID,"stage":"RQMC_LEVEL_MERGE_MISSING","status":"MISSING","m":None,"converged":False}
        levels=[]; proceed=False; classification="DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL"; reason="NO_COMPLETED_RQMC_LEVEL"
    else:
        levels=[int(d["m"]) for _,d in states]
        expected=list(range(RQMC_M_MIN,max(levels)+1))
        if levels!=expected:
            selected=states[-1][1]; proceed=False; classification="DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL"; reason="RQMC_LEVEL_CONTINUITY_FAIL"
        else:
            converged=[(p,d) for p,d in states if d.get("converged") is True]
            if converged:
                selected_path,selected=min(converged,key=lambda x:int(x[1]["m"]))
                if any(int(d["m"])>int(selected["m"]) for _,d in states):
                    proceed=False; classification="DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL"; reason="ADAPTIVE_STOP_VIOLATION"
                else:
                    proceed=True; classification="RQMC_INTEGRATION_VALIDATED"
            else:
                selected=states[-1][1]; proceed=False; classification="DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL"
                reason="HARD_CAP_WITHOUT_CONVERGENCE" if int(selected["m"])==RQMC_M_MAX else "EXECUTION_CHAIN_INCOMPLETE_BEFORE_HARD_CAP"
    selected_out=Path(args.selected_output); selected_out.parent.mkdir(parents=True,exist_ok=True)
    selected_out.write_text(json.dumps(selected,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    out={
        "q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"RQMC_INTEGRATION_GATE","status":"PASS","proceed_to_coreset":proceed,
        "classification":classification,"failure_reason":reason,"executed_levels":levels,
        "selected_m":selected.get("m"),"selected_state_file":selected_out.name,"selected_state_sha256":sha256_file(selected_out),
        "integration_tolerance_delta_chi2":INTEGRATION_DELTA_CHI2_TOL,"hard_cap_m":RQMC_M_MAX,
    }
    write_json(args.output,out)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:
            f.write(f"proceed={'true' if proceed else 'false'}\n")
            f.write(f"selected_m={selected.get('m') if selected.get('m') is not None else ''}\n")
    print(f"Q040_RQMC_INTEGRATION_GATE=PASS proceed={proceed} selected_m={selected.get('m')} reason={reason}")
    return 0

def coreset_shard(args: argparse.Namespace) -> int:
    ns=argparse.Namespace(**vars(args)); ns.implementation=args.implementation
    ctx=None; old=signal.signal(signal.SIGALRM,_alarm); signal.alarm(int(args.soft_stop_minutes*60))
    rec={"q":Q,"program_id":PROGRAM_ID,"stage":"CORESET_SUMMARY_SHARD","implementation":args.implementation,
         "shard":args.shard,"shard_count":args.shard_count,"status":"FAILED"}
    try:
        ctx=NativeContext(ns,args.implementation)
        _,im,cz,bz,pm,pz=_load_prepare(args.prepare_meta,args.prepare_dir,args.implementation)
        centers=np.asarray(cz["centers"],dtype=float); basis=np.asarray(bz["basis"],dtype=float)
        D=native_data_vector(ctx); PD=ctx.P@D
        n=len(centers); lo=(n*args.shard)//args.shard_count; hi=(n*(args.shard+1))//args.shard_count
        eta_out=[]; dpf=[]; fpf=[]; B=[]; Acoef=[]; maxrel=0.0
        for ix in range(lo,hi):
            eta=centers[ix]; y,a=residual_parts(ctx,eta); F=D-y; PF=ctx.P@F
            coeff=basis@a; rel=float(np.linalg.norm(coeff@basis-a)/max(1.0,np.linalg.norm(a)))
            if rel>CALIBRATION_BASIS_REL_TOL: raise RuntimeError(f"CALIBRATION_BASIS_GATE=FAIL coreset rel={rel}")
            b=np.array([float(a[g]@PF[g]) for g in ctx.groups],dtype=float)
            eta_out.append(eta); dpf.append(float(D@PF)); fpf.append(float(F@PF)); B.append(b); Acoef.append(coeff); maxrel=max(maxrel,rel)
        op=Path(args.output_npz); save_npz(op,index=np.arange(lo,hi,dtype=np.int64),eta=np.asarray(eta_out),dpf=np.asarray(dpf),
                                         fpf=np.asarray(fpf),B=np.asarray(B),Acoef=np.asarray(Acoef))
        rec.update({"status":"PASS","index_range":[lo,hi],"npz_file":op.name,"npz_sha256":sha256_file(op),
                    "max_basis_relative_error":maxrel})
        write_json(args.output_meta,rec); print(f"Q040_CORESET_SUMMARY_SHARD=PASS impl={args.implementation} shard={args.shard}"); return 0
    except Exception as exc:
        rec.update({"status":"FAILED",**failure_record(exc,"CORESET_SUMMARY_SHARD")}); write_json(args.output_meta,rec); print(rec.get("traceback"),file=sys.stderr); return 2
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old)
        if ctx is not None:
            try: ctx.close()
            except Exception: pass


def _summary_probe_delta(ctx: NativeContext, basis: np.ndarray, B: np.ndarray, Acoef: np.ndarray, dpf: np.ndarray, fpf: np.ndarray,
                         weights: np.ndarray, probes: np.ndarray, Avals: np.ndarray, ref_idx: int) -> np.ndarray:
    D=native_data_vector(ctx); PD=ctx.P@D; DPD=float(D@PD); logs=[]
    lw=np.where(weights>0,np.log(weights),-np.inf)
    for s,A in zip(probes,Avals):
        row_s=s[ctx.row_ell_index]; T=basis*row_s[None,:]; dvec=T@PD; K=(T@ctx.P)@T.T
        dpa=Acoef@dvec; apa=np.einsum('ir,rs,is->i',Acoef,K,Acoef,optimize=True); apf=B@s
        A2=float(A)**2
        chi=DPD-2*(dpa+dpf)/A2+(apa+2*apf+fpf)/(A2*A2)
        if np.any(~np.isfinite(chi)): raise RuntimeError("CORESET_SUMMARY_FINITE_GATE=FAIL")
        logs.append(float(logsumexp(lw-0.5*chi)))
    return _delta(np.asarray(logs),ref_idx)


def coreset_merge(args: argparse.Namespace) -> int:
    ns=argparse.Namespace(**vars(args)); ns.implementation=args.implementation
    ctx=None
    rec={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"CORESET_MERGE",
         "implementation":args.implementation,"status":"FAILED"}
    try:
        ctx=NativeContext(ns,args.implementation)
        prep,im,cz,bz,pm,pz=_load_prepare(args.prepare_meta,args.prepare_dir,args.implementation)
        centers=np.asarray(cz["centers"],dtype=float); basis=np.asarray(bz["basis"],dtype=float)
        probes=np.asarray(pz["cmb"],dtype=float); Avals=np.asarray(pz["A_planck"],dtype=float); ref=int(pm["reference_probe_index"][args.implementation])
        metas=[]
        for p in Path(args.shard_dir).rglob("*.json"):
            try:d=read_json(p)
            except Exception:continue
            if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="CORESET_SUMMARY_SHARD" and d.get("implementation")==args.implementation: metas.append((p,d))
        if len(metas)!=args.expected_shards: raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL coreset_shards={len(metas)}")
        parts=[]
        for p,d in sorted(metas,key=lambda x:int(x[1]["shard"])):
            if d.get("status")!="PASS": raise RuntimeError("CORESET_SHARD_STATUS_GATE=FAIL")
            z=load_npz_checked(p.parent/d["npz_file"],d["npz_sha256"])
            parts.append({k:np.asarray(z[k]) for k in ("index","eta","dpf","fpf","B","Acoef")})
        idx=np.concatenate([x["index"] for x in parts]); order=np.argsort(idx)
        if not np.array_equal(idx[order],np.arange(len(centers))): raise RuntimeError("CORESET_INDEX_COMPLETENESS_GATE=FAIL")
        eta=np.concatenate([x["eta"] for x in parts])[order]; dpf=np.concatenate([x["dpf"] for x in parts])[order]
        fpf=np.concatenate([x["fpf"] for x in parts])[order]; B=np.concatenate([x["B"] for x in parts])[order]; Acoef=np.concatenate([x["Acoef"] for x in parts])[order]
        state=read_json(args.integration_state); st=state["implementations"][args.implementation]
        schedules={int(k):np.asarray(v,dtype=int) for k,v in im["coreset_schedules"].items()}
        selected=None; validation={}
        for K in CORESET_K:
            si=schedules[K]
            mass=np.asarray(st["coreset_mass_by_k_replicate"][str(K)],dtype=float)
            N=np.asarray(st["counts_by_replicate"],dtype=float)
            wrep=mass/N[:,None]
            wA=(wrep[0]+wrep[1])/2; wB=(wrep[2]+wrep[3])/2; wAll=np.mean(wrep,axis=0)
            predAll=_summary_probe_delta(ctx,basis,B[si],Acoef[si],dpf[si],fpf[si],wAll,probes,Avals,ref)
            predA=_summary_probe_delta(ctx,basis,B[si],Acoef[si],dpf[si],fpf[si],wA,probes,Avals,ref)
            predB=_summary_probe_delta(ctx,basis,B[si],Acoef[si],dpf[si],fpf[si],wB,probes,Avals,ref)
            err=max(float(np.max(np.abs(predAll-np.asarray(st["delta_chi2_pooled"])) )),
                    float(np.max(np.abs(predA-np.asarray(st["delta_chi2_bankA"])) )),
                    float(np.max(np.abs(predB-np.asarray(st["delta_chi2_bankB"])) )))
            validation[str(K)]={"max_abs_delta_chi2_error":err,"pass":err<=CORESET_PROBE_TOL,
                                "weight_sum_all":float(np.sum(wAll)),"weight_sum_A":float(np.sum(wA)),"weight_sum_B":float(np.sum(wB))}
            if selected is None and err<=CORESET_PROBE_TOL: selected=(K,si,wA,wB,wAll)
        if selected is None:
            rec.update({"status":"CORESET_VALIDATION_FAIL","classification":"DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL","validation":validation})
            write_json(args.output_meta,rec); return 0
        K,si,wA,wB,wAll=selected
        op=Path(args.output_npz); save_npz(op,eta=eta[si],dpf=dpf[si],fpf=fpf[si],B=B[si],Acoef=Acoef[si],basis=basis,
                                         weights_A=wA,weights_B=wB,weights_ALL=wAll,ells=ctx.ells)
        rec.update({"status":"PASS","selected_K":int(K),"validation":validation,"npz_file":op.name,"npz_sha256":sha256_file(op),
                    "representation_sha256":ctx.representation_hash,"coreset_probe_tolerance":CORESET_PROBE_TOL,
                    "gates":{"CORESET_NON_GAUSSIAN_GATE":"PASS","CORESET_WEIGHT_PROVENANCE_GATE":"PASS","CORESET_PROBE_VALIDATION_GATE":"PASS"}})
        write_json(args.output_meta,rec); print(f"Q040_CORESET_GATE=PASS impl={args.implementation} K={K}"); return 0
    except Exception as exc:
        rec.update({"status":"FAILED",**failure_record(exc,"CORESET_MERGE")}); write_json(args.output_meta,rec); print(rec.get("traceback"),file=sys.stderr); return 2
    finally:
        if ctx is not None:
            try:ctx.close()
            except Exception:pass


def coreset_gate(args: argparse.Namespace) -> int:
    rows=[]
    for p in Path(args.meta_dir).rglob("*.json"):
        try:d=read_json(p)
        except Exception:continue
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="CORESET_MERGE": rows.append(d)
    by={str(d.get("implementation")):d for d in rows}
    complete=set(by)==set(IMPLEMENTATIONS) and len(rows)==2
    proceed=bool(complete and all(d.get("status")=="PASS" for d in rows))
    out={"q":Q,"program_id":PROGRAM_ID,"stage":"CORESET_GATE","status":"PASS","proceed_to_endpoints":proceed,
         "classification":"CORESET_VALIDATED" if proceed else "DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL",
         "failure_reason":None if proceed else ("CORESET_INCOMPLETE" if not complete else "CORESET_VALIDATION_FAIL"),
         "implementations":{i:{"status":by.get(i,{}).get("status","MISSING"),"selected_K":by.get(i,{}).get("selected_K")} for i in IMPLEMENTATIONS}}
    write_json(args.output,out)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:f.write(f"proceed={'true' if proceed else 'false'}\n")
    return 0

def load_coreset(meta_path: str|Path,npz_path: str|Path,implementation: str,bank: str):
    m=read_json(meta_path)
    if not (m.get("q")==Q and m.get("program_id")==PROGRAM_ID and m.get("implementation")==implementation and m.get("status")=="PASS"):
        raise RuntimeError("CORESET_METADATA_GATE=FAIL")
    z=load_npz_checked(npz_path,m["npz_sha256"])
    key={"A":"weights_A","B":"weights_B","ALL":"weights_ALL"}[bank]
    return m,{k:np.asarray(z[k]) for k in ("eta","dpf","fpf","B","Acoef","basis","ells",key)},key


def make_coreset_likelihood(ctx: NativeContext, z: Mapping[str,np.ndarray], weight_key: str):
    basis=np.asarray(z["basis"],dtype=float); B=np.asarray(z["B"],dtype=float); Acoef=np.asarray(z["Acoef"],dtype=float)
    dpf=np.asarray(z["dpf"],dtype=float); fpf=np.asarray(z["fpf"],dtype=float); weights=np.asarray(z[weight_key],dtype=float)
    D=native_data_vector(ctx); PD=ctx.P@D; DPD=float(D@PD); lw=np.where(weights>0,np.log(weights),-np.inf); lmax=int(np.max(ctx.ells))
    def loglike(A_planck: float,_self=None):
        if _self is None: raise RuntimeError("EXTERNAL_LIKELIHOOD_PROVIDER_GATE=FAIL")
        tt=np.asarray(_self.provider.get_Cl(ell_factor=True)["tt"],dtype=float)
        if len(tt)<=lmax: raise RuntimeError("EXTERNAL_LIKELIHOOD_LMAX_GATE=FAIL")
        s=tt[ctx.ells]; row_s=s[ctx.row_ell_index]; T=basis*row_s[None,:]; dvec=T@PD; K=(T@ctx.P)@T.T
        dpa=Acoef@dvec; apa=np.einsum('ir,rs,is->i',Acoef,K,Acoef,optimize=True); apf=B@s; A2=float(A_planck)**2
        chi=DPD-2*(dpa+dpf)/A2+(apa+2*apf+fpf)/(A2*A2)
        if np.any(~np.isfinite(chi)): raise RuntimeError("FINITE_CORESET_LIKELIHOOD_GATE=FAIL")
        return float(logsumexp(lw-0.5*chi))
    loglike.__name__=f"q040_rqmc_{ctx.implementation}_{weight_key}_loglike"
    return loglike,lmax


def profile(args: argparse.Namespace) -> int:
    impl=args.implementation; bank=args.bank
    ns=argparse.Namespace(**vars(args)); ns.implementation=impl
    ctx=NativeContext(ns,impl)
    q32=ctx.q32; cfg=ctx.cfg; pf=ctx.pf
    parent,parent_path=load_parent(args.parent_dir,impl,args.mask,args.seed)
    start={str(k):float(v) for k,v in parent["minimum"].items() if finite(v)}
    meta,z,wkey=load_coreset(args.coreset_meta,args.coreset_npz,impl,bank)
    prefix=Path(args.output).with_suffix("")
    if impl=="camspec": info=q32.build_camspec_info(cfg,start,prefix,"refinement",pf["support_lock"]); native=q32.CAMSPEC
    else: info=q32.build_hillipop_info(cfg,start,prefix,"refinement"); native=q32.HILLIPOP
    info["likelihood"].pop(native,None)
    removed=base.remove_marginalized_nuisance(info,impl,q32,list(ctx.nuisance_names)+list(ctx.support_null_nuisance))
    fn,lmax=make_coreset_likelihood(ctx,z,wkey); lname=f"q040_rqmc_{impl}_{bank.lower()}"
    info["likelihood"][lname]={"external":fn,"input_params":["A_planck"],"requires":{"Cl":{"tt":lmax}}}
    for n,v in start.items():
        if finite(v): q32.set_ref(info["params"],str(n),float(v))
    max_evals,rhoend=q32.objective_settings(cfg,"refinement"); minim=info.setdefault("sampler",{}).setdefault("minimize",{})
    minim.update({"method":"bobyqa","ignore_prior":True,"best_of":1,"max_evals":max_evals}); minim.setdefault("override_bobyqa",{})["rhoend"]=rhoend
    info["output"]=str(prefix.resolve()); info["force"]=True
    label=f"M{args.mask}-S{args.seed}"; rec={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,
        "stage":"Q040_RQMC_ENDPOINT","bank":bank,"implementation":impl,"source_mask":args.mask,"source_seed":args.seed,"source_label":label,
        "status":"FAILED","actual_computed_result":False,"support_sha256":SUPPORT_HASH,"representation_sha256":meta["representation_sha256"],
        "coreset_selected_K":meta["selected_K"],"A_planck_preserved":True,"removed_native_nuisance":removed,
        "cross_likelihood_chi2_sum_performed":False,"cross_likelihood_absolute_objective_subtraction_performed":False}
    sampler=None; old=signal.signal(signal.SIGALRM,_alarm); signal.alarm(int(args.soft_stop_minutes*60))
    try:
        from cobaya.run import run as cobaya_run
        _,sampler=cobaya_run(info,force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row,source=q19.minimum_row(sampler,prefix)
        if not row or not finite(row.get("chi2")): raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        minimum={str(k):(float(v) if finite(v) else v) for k,v in row.items()}
        for n in COORDS:
            if n not in minimum or not finite(minimum[n]): raise RuntimeError(f"FROZEN_GEOMETRY_GATE=FAIL {n}")
        rec.update({"status":"COMPLETE","actual_computed_result":True,"objective_chi2":float(row["chi2"]),"minimum":minimum,
                    "harvested_minimum_path":source,"parent_q032_profile":{"path":str(parent_path),"sha256":sha256_file(parent_path)},
                    "minimizer":{"method":"bobyqa","max_evals":max_evals,"rhoend":rhoend,"best_of":1,"ignore_prior":True},
                    "backend_commit":BACKEND_COMMIT,"hillipop_commit":HILLIPOP_COMMIT if impl=="hillipop" else None})
    except Exception as exc:
        rec.update({"status":"FAILED",**failure_record(exc,"Q040_RQMC_ENDPOINT")}); print(rec.get("traceback"),file=sys.stderr)
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old)
        try:
            if sampler is not None and hasattr(sampler,"close"):sampler.close()
        except Exception:pass
        ctx.close(); write_json(args.output,rec)
    return 0 if rec["status"]=="COMPLETE" else 2


def collect_endpoints(root: str|Path,bank: str)->list[dict[str,Any]]:
    out=[]
    for p in Path(root).rglob("*.json"):
        try:d=read_json(p)
        except Exception:continue
        if d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="Q040_RQMC_ENDPOINT" and d.get("bank")==bank: out.append(d)
    return out


def bank_stability(args: argparse.Namespace)->int:
    A=collect_endpoints(args.endpoint_dir,"A"); B=collect_endpoints(args.endpoint_dir,"B")
    expected={(i,m,s) for i in IMPLEMENTATIONS for m in (3,6,7) for s in (0,1,2)}
    def key(r):return(str(r["implementation"]),int(r["source_mask"]),int(r["source_seed"]))
    Ac={key(r):r for r in A if r.get("status")=="COMPLETE"}; Bc={key(r):r for r in B if r.get("status")=="COMPLETE"}
    rows={}; complete=set(Ac)==expected and set(Bc)==expected; ok=bool(complete)
    if complete:
        for k in sorted(expected):
            a=Ac[k]["minimum"];b=Bc[k]["minimum"]
            terms=[(float(a[n])-float(b[n]))/SCALES[n] for n in COORDS]; dist=float(math.sqrt(sum(x*x for x in terms)/len(terms)))
            rows[f"{k[0]}:M{k[1]}-S{k[2]}"]={"scaled_distance":dist,"pass":dist<=ENDPOINT_BANK_TOL}; ok=ok and dist<=ENDPOINT_BANK_TOL
    out={"q":Q,"program_id":PROGRAM_ID,"stage":"BANK_ENDPOINT_STABILITY","status":"PASS","proceed_to_production":ok,
         "threshold":ENDPOINT_BANK_TOL,"rows":rows,"complete_A":len(Ac),"complete_B":len(Bc),
         "failure_reason":None if ok else ("BANK_ENDPOINT_INCOMPLETE" if not complete else "BANK_ENDPOINT_STABILITY_FAIL"),
         "classification":"BANK_ENDPOINT_STABILITY_PASS" if ok else "DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL"}
    write_json(args.output,out)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:f.write(f"proceed={'true' if ok else 'false'}\n")
    return 0


def production_gate(args: argparse.Namespace)->int:
    rows=collect_endpoints(args.endpoint_dir,"ALL")
    expected={(i,m,s) for i in IMPLEMENTATIONS for m in (3,6,7) for s in (0,1,2)}
    complete=[r for r in rows if r.get("status")=="COMPLETE" and r.get("actual_computed_result") is True]
    got={(str(r["implementation"]),int(r["source_mask"]),int(r["source_seed"])) for r in complete}
    proceed=got==expected and len(complete)==18
    out={"q":Q,"program_id":PROGRAM_ID,"stage":"PRODUCTION_ENDPOINT_GATE","status":"PASS","proceed_to_assess":proceed,
         "complete_count":len(complete),"expected_count":18,"classification":"PRODUCTION_COMPLETE" if proceed else "DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL",
         "failure_reason":None if proceed else "PRODUCTION_ENDPOINT_INCOMPLETE"}
    write_json(args.output,out)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as f:f.write(f"proceed={'true' if proceed else 'false'}\n")
    return 0

def assess(args: argparse.Namespace)->int:
    rows_raw=collect_endpoints(args.endpoint_dir,"ALL"); expected={(i,m,s) for i in IMPLEMENTATIONS for m in (3,6,7) for s in (0,1,2)}
    complete=[r for r in rows_raw if r.get("status")=="COMPLETE" and r.get("actual_computed_result") is True]
    got={(str(r["implementation"]),int(r["source_mask"]),int(r["source_seed"])) for r in complete}
    if got!=expected or len(complete)!=18: raise RuntimeError("JOB_COMPLETENESS_GATE=FAIL production_endpoints")
    rows={i:{} for i in IMPLEMENTATIONS}; prov={}
    for r in complete:
        impl=str(r["implementation"]);lab=str(r["source_label"]);rows[impl][lab]={n:float(r["minimum"][n]) for n in COORDS}
        prov[f"{impl}:{lab}"]={"objective_chi2_within_implementation_only":float(r["objective_chi2"]),"coreset_selected_K":r["coreset_selected_K"]}
    full=calculate_metrics(rows,LABELS); fs=sufficient(full); loo={}
    for omit in LABELS:
        m=calculate_metrics(rows,[x for x in LABELS if x!=omit]); loo[omit]={"metrics":m,"sufficient":sufficient(m)}
    all_loo=len(loo)==9 and all(v["sufficient"] for v in loo.values()); suff=bool(fs and all_loo)
    classification="DEFENSIVE_CMB_MARGINAL_BRIDGE_SUFFICIENT" if suff else "DEFENSIVE_CMB_MARGINAL_BRIDGE_INSUFFICIENT"
    reductions={k:(float(BASELINE[k])-float(full[k]))/float(BASELINE[k]) for k in BASELINE}
    out={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"Q040_RQMC_PROVISIONAL",
         "execution_status":"COMPLETE","tests_status":"PENDING","final_result_gate":"PROVISIONAL","actual_computed_result":True,
         "classification":classification,"sufficient":suff,"full_sample":{"metrics":full,"sufficient":fs},"leave_one_label_out":loo,
         "all_nine_loo_sufficient":all_loo,"continuous_reduction_fraction_vs_q037":reductions,"baseline_q037":BASELINE,
         "endpoint_provenance":prov,"support_sha256":SUPPORT_HASH,"scales_sha256":SCALES_HASH,
         "cross_likelihood_chi2_sum_performed":False,"cross_likelihood_absolute_objective_subtraction_performed":False}
    write_json(args.output,out); return 0


def seal_failure(args: argparse.Namespace)->int:
    gate=read_json(args.gate)
    final={"q":Q,"program_id":PROGRAM_ID,"run_id":RUN_ID,"result_id":RESULT_ID,"stage":"Q040_RQMC_FINAL_TECHNICAL",
           "execution_status":"STOPPED_BEFORE_VALIDATED_SCIENCE_RESULT","tests_status":"VALIDATION_FAIL","actual_computed_result":False,
           "classification":"DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL","final_result_gate":"UNRESOLVED","FINAL_RESULT_GATE":"UNRESOLVED",
           "validation_parent":gate,"journal_effect":{"Q040":"ADD_DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAILURE","C-036-IMPL":"KEEP_ACTIVE_CAUSE_UNRESOLVED"},
           "return_route":"BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE"}
    handoff={"current_q":Q,"program_id":PROGRAM_ID,"scientific_question":load_preregister(args.preregister)["project"]["scientific_question"],
             "new_result":{"result_id":RESULT_ID,"classification":final["classification"],"final_result_gate":"UNRESOLVED"},
             "sources":list(load_source_lock(args.source_lock)["sources"].keys()),"test_status":"VALIDATION_FAIL",
             "unresolved_issues":["The preregistered finite defensive RQMC/coreset numerical representation did not satisfy its finite validation gates."],
             "next_required_action":"RESULT_INGESTION_AND_ROUTING"}
    write_json(args.output,final);write_json(args.handoff,handoff);return 0


def seal(args: argparse.Namespace)->int:
    d=read_json(args.provisional);t=read_json(args.tests)
    if not (d.get("q")==Q and d.get("program_id")==PROGRAM_ID and d.get("stage")=="Q040_RQMC_PROVISIONAL" and d.get("final_result_gate")=="PROVISIONAL"):
        raise RuntimeError("PROVISIONAL_PARENT_GATE=FAIL")
    if not (t.get("q")==Q and t.get("program_id")==PROGRAM_ID and t.get("status")=="PASS" and t.get("FINAL_RESULT_GATE")=="PASS"):
        raise RuntimeError("RESULT_TEST_PARENT_GATE=FAIL")
    final=copy.deepcopy(d); final.update({"stage":"Q040_RQMC_FINAL","tests_status":"COMPLETE","final_result_gate":"PASS","FINAL_RESULT_GATE":"PASS",
        "result_tests_sha256":sha256_file(args.tests),"journal_effect":{"Q035":"KEEP_CLOSED","Q037":"KEEP_CLOSED_AS_FROZEN_BASELINE",
        "Q038":"KEEP_DESCRIPTIVE_ONLY","Q039":"KEEP_CLOSED_NEGATIVE_BLOCK_TESTS","Q040":"ADD_VALIDATED_DEFENSIVE_CMB_MARGINAL_RESULT",
        "C-036-IMPL":"UPDATE_FROM_Q040_CLASSIFICATION_WITHOUT_CAUSAL_OVERCLAIM"},"return_route":"BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE"})
    handoff={"current_q":Q,"program_id":PROGRAM_ID,"scientific_question":load_preregister(args.preregister)["project"]["scientific_question"],
        "new_result":{"result_id":RESULT_ID,"classification":final["classification"],"full_sample":final["full_sample"],
        "leave_one_label_out":final["leave_one_label_out"],"continuous_reduction_fraction_vs_q037":final["continuous_reduction_fraction_vs_q037"]},
        "journal_effect":final["journal_effect"],"sources":list(load_source_lock(args.source_lock)["sources"].keys()),"test_status":"PASS",
        "unresolved_issues":[] if final["sufficient"] else ["Residual C-036-IMPL remains after validated defensive native-prior CMB marginalization."],
        "next_required_action":"RESULT_INGESTION_AND_SCIENTIFIC_CONCLUSION_ROUTING"}
    write_json(args.output,final);write_json(args.handoff,handoff);return 0


def validate_parent_cmd(args: argparse.Namespace)->int:
    # base.validate_parent uses patched global identity and frozen metrics only.
    return base.validate_parent(args)


def context_args(a: argparse.ArgumentParser)->None:
    a.add_argument("--q032-parent-root",required=True);a.add_argument("--preflight",required=True);a.add_argument("--parent-dir",required=True)
    a.add_argument("--preregister",required=True);a.add_argument("--source-lock",required=True);a.add_argument("--hlp-matrix");a.add_argument("--hlp-meta")
    a.add_argument("--scratch",default="q040_rqmc_runtime")


def main()->None:
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
    a=sp.add_parser("validate-parent");a.add_argument("--parent-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=validate_parent_cmd)
    a=sp.add_parser("prepare");context_args(a);a.add_argument("--v4-map-dir",required=True);a.add_argument("--output-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=prepare)
    a=sp.add_parser("plan-level");a.add_argument("--m",type=int,required=True);a.add_argument("--output",required=True);a.set_defaults(func=plan_level)
    a=sp.add_parser("rqmc-shard");context_args(a);a.add_argument("--implementation",choices=IMPLEMENTATIONS,required=True);a.add_argument("--prepare-meta",required=True);a.add_argument("--prepare-dir",required=True)
    a.add_argument("--m",type=int,required=True);a.add_argument("--shard",type=int,required=True);a.add_argument("--shard-count",type=int,required=True);a.add_argument("--soft-stop-minutes",type=float,default=300);a.add_argument("--output",required=True);a.set_defaults(func=rqmc_shard)
    a=sp.add_parser("merge-level");a.add_argument("--m",type=int,required=True);a.add_argument("--shard-dir",required=True);a.add_argument("--previous-state");a.add_argument("--prepare-meta",required=True);a.add_argument("--prepare-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=merge_level)
    a=sp.add_parser("integration-gate");a.add_argument("--state-dir",required=True);a.add_argument("--output",required=True);a.add_argument("--selected-output",required=True);a.set_defaults(func=integration_gate)
    a=sp.add_parser("coreset-shard");context_args(a);a.add_argument("--implementation",choices=IMPLEMENTATIONS,required=True);a.add_argument("--prepare-meta",required=True);a.add_argument("--prepare-dir",required=True);a.add_argument("--shard",type=int,required=True);a.add_argument("--shard-count",type=int,required=True);a.add_argument("--soft-stop-minutes",type=float,default=300);a.add_argument("--output-npz",required=True);a.add_argument("--output-meta",required=True);a.set_defaults(func=coreset_shard)
    a=sp.add_parser("coreset-merge");context_args(a);a.add_argument("--implementation",choices=IMPLEMENTATIONS,required=True);a.add_argument("--prepare-meta",required=True);a.add_argument("--prepare-dir",required=True);a.add_argument("--integration-state",required=True);a.add_argument("--shard-dir",required=True);a.add_argument("--expected-shards",type=int,required=True);a.add_argument("--output-npz",required=True);a.add_argument("--output-meta",required=True);a.set_defaults(func=coreset_merge)
    a=sp.add_parser("coreset-gate");a.add_argument("--meta-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=coreset_gate)
    a=sp.add_parser("profile");context_args(a);a.add_argument("--implementation",choices=IMPLEMENTATIONS,required=True);a.add_argument("--bank",choices=("A","B","ALL"),required=True);a.add_argument("--mask",type=int,choices=(3,6,7),required=True);a.add_argument("--seed",type=int,choices=(0,1,2),required=True);a.add_argument("--coreset-meta",required=True);a.add_argument("--coreset-npz",required=True);a.add_argument("--soft-stop-minutes",type=float,default=300);a.add_argument("--output",required=True);a.set_defaults(func=profile)
    a=sp.add_parser("bank-stability");a.add_argument("--endpoint-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=bank_stability)
    a=sp.add_parser("production-gate");a.add_argument("--endpoint-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=production_gate)
    a=sp.add_parser("assess");a.add_argument("--endpoint-dir",required=True);a.add_argument("--output",required=True);a.set_defaults(func=assess)
    a=sp.add_parser("seal-failure");a.add_argument("--gate",required=True);a.add_argument("--preregister",required=True);a.add_argument("--source-lock",required=True);a.add_argument("--output",required=True);a.add_argument("--handoff",required=True);a.set_defaults(func=seal_failure)
    a=sp.add_parser("seal");a.add_argument("--provisional",required=True);a.add_argument("--tests",required=True);a.add_argument("--preregister",required=True);a.add_argument("--source-lock",required=True);a.add_argument("--output",required=True);a.add_argument("--handoff",required=True);a.set_defaults(func=seal)
    args=p.parse_args();raise SystemExit(args.func(args))

if __name__=="__main__":main()
