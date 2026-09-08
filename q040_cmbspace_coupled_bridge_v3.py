#!/usr/bin/env python3
"""Bubbleverse Q-040 CMB-space coupled bridge V3.

V3 is deliberately a thin technical patch over the frozen V2 implementation.
It reuses V2's validated Q032 parent loading, native CamSpec/HiLLiPoP context,
Laplace/Schur compression, validation, endpoint execution, geometry and sealing.
Only the failed MAP mechanism is replaced:

V2: alternating GLS <-> nuisance minimization + Anderson acceleration.
V3: exact-GLS variable projection. The latent identity-multipole CMB vector is
    analytically eliminated at every nuisance evaluation, so the optimizer sees
    only the implementation-native nuisance profile. One independent conditional
    nuisance minimization then verifies the inherited 1e-6 objective / 1e-3
    proposal-scaled fixed-point gates. No science gate, prior, bound, model,
    support, dataset or geometry threshold is weakened.
"""
from __future__ import annotations

import math
import signal
import sys
from typing import Any

import numpy as np
from scipy.optimize import minimize

import q040_cmbspace_coupled_bridge_v2 as base

Q = "Q-040"
PROGRAM_ID = "Q040-CMBSPACE-V3"
RUN_ID = "Q040-CMBSPACE-COUPLED-BRIDGE-V3"
RESULT_ID = "R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-003"
INTERVENTION = "NATIVE_NUISANCE_MARGINALIZED_CMB_SPACE_LAPLACE_SCHUR_V3"
V2_FAILED_RUN_ID = 34203696897

# Preserve the frozen scientific identity from V2/Q032.
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
MARGINALIZED_A_PLANCK = base.MARGINALIZED_A_PLANCK

# Re-export unchanged scientific/utility functions used by tests and downstream.
NativeContext = base.NativeContext
SoftStop = base.SoftStop
finite = base.finite
failure_record = base.failure_record
write_json = base.write_json
calculate_metrics = base.calculate_metrics
sufficient = base.sufficient
_clip_bounds = base._clip_bounds

# Patch V2 module globals before any reused command is executed. Reused V2
# functions resolve these names dynamically from base.__dict__, so all emitted
# metadata and prereg/source-lock checks become V3-identical.
base.Q = Q
base.PROGRAM_ID = PROGRAM_ID
base.RUN_ID = RUN_ID
base.RESULT_ID = RESULT_ID
base.INTERVENTION = INTERVENTION


def _scaled_bounds(ctx: NativeContext, center: np.ndarray) -> list[tuple[float | None, float | None]]:
    scales = np.maximum(np.asarray(ctx.proposal_scales, dtype=float), 1e-12)
    out: list[tuple[float | None, float | None]] = []
    for x0, s, (lo, hi) in zip(np.asarray(center, dtype=float), scales, ctx.bounds):
        zl = None if lo is None else (float(lo) - float(x0)) / float(s)
        zh = None if hi is None else (float(hi) - float(x0)) / float(s)
        out.append((zl, zh))
    return out


def _eta_from_z(ctx: NativeContext, center: np.ndarray, z: np.ndarray) -> np.ndarray:
    scales = np.maximum(np.asarray(ctx.proposal_scales, dtype=float), 1e-12)
    return _clip_bounds(np.asarray(center, dtype=float) + scales * np.asarray(z, dtype=float), ctx.bounds)


def optimize_eta(ctx: NativeContext, cmb: np.ndarray, eta0: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, dict[str, Any]]:
    """High-precision conditional nuisance minimization in proposal units."""
    center = _clip_bounds(np.asarray(eta0, dtype=float), ctx.bounds)
    zbounds = _scaled_bounds(ctx, center)
    z0 = np.zeros(len(center), dtype=float)

    def fun_z(z: np.ndarray) -> float:
        return float(ctx.joint_objective(cmb, _eta_from_z(ctx, center, z), A_planck=A_planck))

    primary = minimize(
        fun_z, z0, method="L-BFGS-B", bounds=zbounds,
        options={"maxiter": 5000, "ftol": 1e-14, "gtol": 2e-7, "maxls": 60, "eps": 2e-5},
    )
    candidates = [(primary, "L-BFGS-B_SCALED")]
    # Derivative-free fallback only if the primary conditional minimizer fails.
    if (not bool(getattr(primary, "success", False))) or (not finite(getattr(primary, "fun", math.inf))):
        try:
            zseed = np.asarray(primary.x if np.all(np.isfinite(primary.x)) else z0, dtype=float)
            pw = minimize(
                fun_z, zseed, method="Powell", bounds=zbounds,
                options={"maxiter": 2500, "xtol": 2e-5, "ftol": 1e-12},
            )
            candidates.append((pw, "POWELL_SCALED_FALLBACK"))
        except Exception:
            pass
    valid = [(r, m) for r, m in candidates if finite(getattr(r, "fun", math.inf)) and float(r.fun) < 1e99]
    if not valid:
        raise RuntimeError("NUISANCE_OPTIMIZATION_GATE=FAIL")
    chosen, method = min(valid, key=lambda rm: float(rm[0].fun))
    eta = _eta_from_z(ctx, center, np.asarray(chosen.x, dtype=float))
    return eta, {
        "method": method,
        "success": bool(getattr(chosen, "success", False)),
        "status": int(getattr(chosen, "status", -1)),
        "message": str(getattr(chosen, "message", "")),
        "fun": float(chosen.fun),
        "nfev": int(getattr(chosen, "nfev", -1)),
        "nit": int(getattr(chosen, "nit", -1)),
        "candidate_methods": [m for _, m in candidates],
    }


def profiled_state(ctx: NativeContext, eta: np.ndarray, A_planck: float = 1.0) -> tuple[float, np.ndarray]:
    """Exact nuisance-profile objective after analytic GLS elimination of CMB."""
    eta = _clip_bounds(np.asarray(eta, dtype=float), ctx.bounds)
    pn = ctx.prior_nlp(eta)
    if not finite(pn):
        return 1e100, np.full(len(ctx.ells), np.nan)
    cmb, _, y, a, _ = ctx.gls_system(eta, A_planck=A_planck)
    r = y - a * cmb[ctx.row_ell_index]
    chi2 = float(r @ (ctx.P @ r))
    if not finite(chi2) or chi2 < 0:
        return 1e100, cmb
    return float(0.5 * chi2 + pn), cmb


def optimize_profiled_eta(ctx: NativeContext, eta0: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Direct variable-projection minimization over nuisance coordinates only."""
    center = _clip_bounds(np.asarray(eta0, dtype=float), ctx.bounds)
    zbounds = _scaled_bounds(ctx, center)
    z0 = np.zeros(len(center), dtype=float)
    cache: dict[tuple[float, ...], tuple[float, np.ndarray]] = {}

    def evaluate(z: np.ndarray) -> tuple[float, np.ndarray]:
        eta = _eta_from_z(ctx, center, np.asarray(z, dtype=float))
        key = tuple(np.round(eta, 14))
        if key not in cache:
            cache[key] = profiled_state(ctx, eta, A_planck=A_planck)
        return cache[key]

    def fun_z(z: np.ndarray) -> float:
        return float(evaluate(z)[0])

    attempts: list[tuple[Any, str]] = []
    lb = minimize(
        fun_z, z0, method="L-BFGS-B", bounds=zbounds,
        options={"maxiter": 5000, "ftol": 1e-14, "gtol": 2e-7, "maxls": 60, "eps": 2e-5},
    )
    attempts.append((lb, "L-BFGS-B_PROFILE_SCALED"))
    try:
        zseed = np.asarray(lb.x if np.all(np.isfinite(lb.x)) else z0, dtype=float)
        pw = minimize(
            fun_z, zseed, method="Powell", bounds=zbounds,
            options={"maxiter": 3000, "xtol": 2e-5, "ftol": 1e-12},
        )
        attempts.append((pw, "POWELL_PROFILE_SCALED"))
    except Exception:
        pass
    valid = [(r, m) for r, m in attempts if finite(getattr(r, "fun", math.inf)) and float(r.fun) < 1e99]
    if not valid:
        raise RuntimeError("PROFILED_NUISANCE_OPTIMIZATION_GATE=FAIL")
    best, method = min(valid, key=lambda rm: float(rm[0].fun))
    try:
        polish = minimize(
            fun_z, np.asarray(best.x, dtype=float), method="L-BFGS-B", bounds=zbounds,
            options={"maxiter": 5000, "ftol": 5e-15, "gtol": 1e-7, "maxls": 80, "eps": 1e-5},
        )
        attempts.append((polish, "L-BFGS-B_PROFILE_POLISH"))
        if finite(polish.fun) and float(polish.fun) <= float(best.fun):
            best, method = polish, "L-BFGS-B_PROFILE_POLISH"
    except Exception:
        pass
    eta = _eta_from_z(ctx, center, np.asarray(best.x, dtype=float))
    obj, cmb = profiled_state(ctx, eta, A_planck=A_planck)
    return eta, cmb, {
        "method": method,
        "success": bool(getattr(best, "success", False)),
        "status": int(getattr(best, "status", -1)),
        "message": str(getattr(best, "message", "")),
        "fun": float(obj),
        "nfev": int(getattr(best, "nfev", -1)),
        "nit": int(getattr(best, "nit", -1)),
        "native_profile_evaluations": len(cache),
        "attempts": [
            {"method": m, "success": bool(getattr(r, "success", False)),
             "fun": float(r.fun) if finite(getattr(r, "fun", math.inf)) else None,
             "nfev": int(getattr(r, "nfev", -1)), "nit": int(getattr(r, "nit", -1)),
             "message": str(getattr(r, "message", ""))}
            for r, m in attempts
        ],
    }


def variable_projection_map(ctx: NativeContext, eta0: np.ndarray) -> dict[str, Any]:
    """Direct profile solve plus one inherited fixed-point verification."""
    eta = _clip_bounds(np.asarray(eta0, dtype=float), ctx.bounds)
    history: list[dict[str, Any]] = []
    final_cmb: np.ndarray | None = None
    converged = False
    verification: dict[str, Any] = {}

    # Primary solve + at most one preregistered verification-triggered polish.
    for profile_pass in range(2):
        eta_star, cmb_star, opt = optimize_profiled_eta(ctx, eta, A_planck=1.0)
        obj_star, cmb_star = profiled_state(ctx, eta_star, A_planck=1.0)
        eta_cond, cond_opt = optimize_eta(ctx, cmb_star, eta_star, A_planck=1.0)
        obj_cond, cmb_cond = profiled_state(ctx, eta_cond, A_planck=1.0)
        scaled_eta = float(np.max(np.abs((eta_cond - eta_star) / np.maximum(ctx.proposal_scales, 1e-12)))) if len(eta_star) else 0.0
        rel_obj = abs(float(obj_cond) - float(obj_star)) / max(1.0, abs(float(obj_star)))
        verification = {
            "profile_pass": profile_pass,
            "profile_objective": float(obj_star),
            "conditional_then_gls_objective": float(obj_cond),
            "relative_objective_change": float(rel_obj),
            "max_scaled_nuisance_change": float(scaled_eta),
            "conditional_optimizer": cond_opt,
        }
        history.append({"profile_pass": profile_pass, "profile_optimizer": opt, "verification": verification})
        if rel_obj <= 1e-6 and scaled_eta <= 1e-3:
            eta, final_cmb, converged = eta_star, cmb_star, True
            break
        eta, final_cmb = eta_cond, cmb_cond

    if final_cmb is None:
        raise RuntimeError("COMPRESSION_MAP_GATE=FAIL no_cmb")
    eta = _clip_bounds(np.asarray(eta, dtype=float), ctx.bounds)
    obj, final_cmb = profiled_state(ctx, eta, A_planck=1.0)
    grad = ctx.grad_cmb(final_cmb, eta)
    return {
        "status": "COMPLETE" if converged else "NOT_CONVERGED",
        "converged": converged,
        "solver": "EXACT_GLS_VARIABLE_PROJECTION_PROFILED_NUISANCE_MAP_V3",
        "objective": float(obj),
        "eta": {n: float(v) for n, v in zip(ctx.nuisance_names, eta)},
        "cmb": final_cmb.tolist(),
        "cmb_gradient_rms": float(np.sqrt(np.mean(grad ** 2))),
        "profile_passes": len(history),
        "verification": verification,
        "history": history,
    }


def map_start(args: Any) -> int:
    ctx = None
    old = signal.signal(signal.SIGALRM, base._alarm)
    signal.alarm(int(float(args.soft_stop_minutes) * 60))
    rec: dict[str, Any] = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "COMPRESSION_MAP_START", "implementation": args.implementation,
        "start_family": args.start_family, "status": "FAILED",
        "actual_scientific_result": False, "support_sha256": SUPPORT_HASH,
        "technical_supersession": f"Q040-CMBSPACE-V2_RUN_{V2_FAILED_RUN_ID}_HILLIPOP_VARIABLE_PROJECTION_REPAIR",
    }
    stage = "NATIVE_CONTEXT_INIT"
    try:
        ctx = NativeContext(args, args.implementation)
        rec["representation_sha256"] = ctx.representation_hash
        stage = "START_VECTOR"
        eta0, meta = ctx.start_vector(args.parent_dir, args.start_family)
        stage = "VARIABLE_PROJECTION_MAP"
        out = variable_projection_map(ctx, eta0)
        rec.update(out)
        rec["start_provenance"] = meta
        rec["nuisance_names"] = list(ctx.nuisance_names)
        rec["support_null_nuisance"] = list(ctx.support_null_nuisance)
        rec["support_null_response_max"] = ctx.support_null_response_max
        rec["linear_design_relative_error"] = ctx.linear_design_relative_error
        if out["status"] != "COMPLETE":
            rec["failure_class"] = "NUMERICAL_NONCONVERGENCE"
            rec["failure_stage"] = stage
    except SoftStop as exc:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC", **failure_record(exc, stage)})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD", **failure_record(exc, stage)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if ctx is not None:
                ctx.close()
        except Exception as exc:
            rec.setdefault("close_error", repr(exc))
        write_json(args.output, rec)
        if rec.get("status") == "COMPLETE":
            print(f"Q040_V3_MAP_GATE=PASS implementation={args.implementation} start={args.start_family}")
        else:
            print(f"Q040_V3_MAP_GATE=FAIL implementation={args.implementation} start={args.start_family} status={rec.get('status')} stage={rec.get('failure_stage')}", file=sys.stderr)
            if rec.get("error"):
                print(rec.get("traceback", rec["error"]), file=sys.stderr)
    return 0 if rec.get("status") == "COMPLETE" else 2


# Install V3 numerical functions into reused V2 downstream logic. In particular,
# compression validation calls base.optimize_eta, so it must use the V3 scaled
# conditional solver rather than the old V2 implementation.
base.optimize_eta = optimize_eta
base.accelerated_map = variable_projection_map
base.map_start = map_start


def main() -> None:
    base.main()


if __name__ == "__main__":
    main()
