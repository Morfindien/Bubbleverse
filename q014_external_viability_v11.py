#!/usr/bin/env python3
"""Bubbleverse Q014 V11 — same-run cross-mode numerical certification.

V11 preserves the frozen Q014 V5 likelihood/model surface and the
normalization-free objective introduced in V8. V10 completed all 27 optimizer
jobs but remained numerically unresolved because:
  * Planck free-H0 best-two spread was 1.8765689284 (> 1.0), and
  * SPT fixed-H0 minima improved relative to the V8 parent that had seeded the
    V10 free-H0 jobs, leaving small same-generation nesting violations.

V11 removes that one-generation lag with two phases:
  Phase 1 refines V10 free/fixed minima and re-runs Q011-shared physics.
  Phase 2 waits for Phase 1, then profiles free H0 from the *same-run* Phase-1
  best free and best fixed minima (exact + bounded jitter). The exact fixed
  minimum is embedded in the free-H0 parameter space by releasing H0=71.5.

No scientific likelihood, dataset, parameter bounds, objective basis, or
validation threshold is relaxed.
"""
from __future__ import annotations
import argparse, copy, json, math
from pathlib import Path
from typing import Any, Mapping
import yaml

import q014_external_viability_v10 as prev

impl = prev.impl
ROOT = Path(__file__).resolve().parent
CONFIG_NAME = "q014_external_viability_v11_config.yml"
RUN_ID = "Q014-EXTERNAL-VIABILITY-V11"
RESULT_ID = "R-Q014-EDE-EXTERNAL-VIABILITY-008"
CODE_VERSION = "11.0-same-run-cross-mode-certification"
V10_EXPECTED_RUN = "Q014-EXTERNAL-VIABILITY-V10"
V10_EXPECTED_RESULT = "R-Q014-EDE-EXTERNAL-VIABILITY-007"
BASIS = "SCALAR_TOTAL_LIKELIHOOD_CHI2_PLUS_NORMALIZATION_FREE_GAUSSIAN_CONSTRAINT_SHAPES"

V10_RESULT_PATH: Path | None = None
PHASE1_SUMMARY_PATH: Path | None = None

impl.RUN_ID = RUN_ID
impl.CODE_VERSION = CODE_VERSION
impl.CONFIG_NAME = CONFIG_NAME
# Preserve the V8/V10 objective implementation and chain-native nuisance declarations.
impl.objective_from_row = prev.objective_from_row
impl.inject_chain_native_parameters = prev.inject_chain_native_parameters
impl.set_reference = prev.set_reference

def load_cfg(path: str | Path = CONFIG_NAME) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def finite_number(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False

def load_v10_result(path: str | Path | None = None) -> dict[str, Any]:
    p = Path(path) if path is not None else V10_RESULT_PATH
    if p is None:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL no V10 result path")
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    if d.get("q") != "Q014" or d.get("run_id") != V10_EXPECTED_RUN or d.get("result_id") != V10_EXPECTED_RESULT:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL identity")
    if d.get("scientifically_usable_result") is not False or d.get("validation_status") != "NUMERICALLY UNRESOLVED":
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL status")
    if d.get("objective_basis") != BASIS:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL objective basis")
    jm = d.get("job_manifest", {})
    if int(jm.get("expected", -1)) != 27 or int(jm.get("returned", -2)) != 27:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL completeness")
    if jm.get("missing") or jm.get("duplicates") or jm.get("runtime_source_compatible") is not True:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL provenance")
    # Preserve the exact unresolved reason that motivates V11.
    planck_free = d["chains"]["planck_npipe_k039_approx"]["profiles"]["reference_free_h0"]
    spt_mono = d["chains"]["spt_d1_only"]["penalties"]["fixed_profile_monotonicity_pass"]
    if planck_free.get("stable") is True or spt_mono is True:
        raise RuntimeError("V10_NUMERICAL_PARENT_GATE=FAIL expected unresolved signature absent")
    return d

def best_minimum_from_result(d: Mapping[str, Any], chain: str, mode: str) -> dict[str, float]:
    rec = d["chains"][chain]["profiles"][mode].get("best_record")
    if not isinstance(rec, Mapping) or rec.get("status") != "COMPLETE":
        raise RuntimeError(f"Missing complete best record for {chain}/{mode}")
    row = rec.get("minimum")
    if not isinstance(row, Mapping):
        raise RuntimeError(f"Missing best minimum for {chain}/{mode}")
    out: dict[str, float] = {}
    for k, v in row.items():
        try:
            x = float(v)
        except Exception:
            continue
        if math.isfinite(x):
            out[str(k)] = x
    return out

def v10_best_minimum(chain: str, mode: str) -> dict[str, float]:
    return best_minimum_from_result(load_v10_result(), chain, mode)

JITTER_TWEAKS = dict(prev.JITTER_TWEAKS)

def bounded_jitter(base: dict[str, float], info: Mapping[str, Any], sign: float) -> dict[str, float]:
    # Reuse the already audited V10 bounded-jitter implementation exactly.
    return prev._bounded_jitter(base, info, sign)

def load_phase1_summary(path: str | Path | None = None) -> dict[str, Any]:
    p = Path(path) if path is not None else PHASE1_SUMMARY_PATH
    if p is None:
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL no phase1 summary path")
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    if d.get("q") != "Q014" or d.get("run_id") != RUN_ID or d.get("summary_type") != "PHASE1_SEED_SUMMARY":
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL identity")
    if d.get("status") != "PASS":
        raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL status")
    return d

def phase1_best_minimum(chain: str, mode: str) -> dict[str, float]:
    d = load_phase1_summary()
    row = d["chains"][chain][mode]["best_record"]["minimum"]
    out: dict[str, float] = {}
    for k, v in row.items():
        try:
            x = float(v)
        except Exception:
            continue
        if math.isfinite(x):
            out[str(k)] = x
    return out

_original_start = prev._original_start

def start_vector(chain: str, family: str, c: Mapping[str, Any], info: Mapping[str, Any],
                 q011_vec: Mapping[str, float]) -> dict[str, float]:
    # Phase 1: V10 numerical-parent minima.
    v10_families = {
        "v10_free_best": ("reference_free_h0", False, +1.0),
        "v10_free_jitter": ("reference_free_h0", True, +1.0),
        "v10_fixed_best": ("fixed_h0_71p5", False, -1.0),
        "v10_fixed_jitter": ("fixed_h0_71p5", True, -1.0),
    }
    # Phase 2: same-run Phase-1 minima.
    p1_families = {
        "p1_free_best": ("reference_free_h0", False, +1.0),
        "p1_free_jitter": ("reference_free_h0", True, +1.0),
        "p1_fixed_best": ("fixed_h0_71p5", False, -1.0),
        "p1_fixed_jitter": ("fixed_h0_71p5", True, -1.0),
    }
    if family in v10_families:
        source_mode, jitter, sign = v10_families[family]
        base = impl.q005_default_reference(info)
        base.update(v10_best_minimum(chain, source_mode))
        if source_mode == "fixed_h0_71p5" and "H0" not in base:
            base["H0"] = float(c["scientific_surface"]["target_h0"])
        return bounded_jitter(base, info, sign) if jitter else base
    if family in p1_families:
        source_mode, jitter, sign = p1_families[family]
        base = impl.q005_default_reference(info)
        base.update(phase1_best_minimum(chain, source_mode))
        if source_mode == "fixed_h0_71p5" and "H0" not in base:
            # This is the mathematically required same-run embedding:
            # the Phase-1 fixed point is inserted in the free-H0 space at H0=71.5.
            base["H0"] = float(c["scientific_surface"]["target_h0"])
        return bounded_jitter(base, info, sign) if jitter else base
    # Frozen V5 smoke/preflight families remain untouched.
    return _original_start(chain, family, c, info, q011_vec)

impl.start_vector = start_vector

_original_build = prev._original_build

def build_info(chain, mode, start_family, restart_index, c, q011_vec, output_prefix, max_evals=None):
    info, refs = _original_build(chain, mode, start_family, restart_index, c, q011_vec, output_prefix, max_evals)
    m = info["sampler"]["minimize"]
    phase2 = str(start_family).startswith("p1_")
    if max_evals is not None:
        me = int(max_evals)
    elif phase2:
        me = int(c["execution"]["phase2_minimizer"]["max_evals"])
    else:
        me = int(c["execution"]["minimizer"]["max_evals"])
    m["max_evals"] = me
    rho = c["execution"]["phase2_minimizer"]["rhoend"] if phase2 else c["execution"]["minimizer"]["override_bobyqa"]["rhoend"]
    m.setdefault("override_bobyqa", {})["rhoend"] = float(rho)
    return info, refs

impl.build_info = build_info

def comparable_objective(row: Mapping[str, Any]):
    return prev.comparable_objective(row)

def prior_gate(model, chain: str) -> dict[str, Any]:
    return prev._prior_gate(model, chain)

def seed_evaluation(chain: str, mode: str, family: str, restart: int, q011_path: str | Path,
                    c: Mapping[str, Any], out: Path) -> dict[str, Any]:
    qvec = impl.q011_exact_shared_vector(c, q011_path)
    info, refs = impl.build_info(chain, mode, family, restart, c, qvec,
                                 out.parent / (out.stem + "_seedcheck"), max_evals=4)
    from cobaya.model import get_model
    model = get_model(info)
    gate = prior_gate(model, chain)
    if not gate["pass"]:
        raise RuntimeError("CHAIN_NATIVE_CONSTRAINT_SHAPE_GATE=FAIL " + json.dumps(gate, sort_keys=True))
    sampled = list(model.parameterization.sampled_params())
    if not bool(getattr(model.prior, "reference_is_pointlike", False)):
        raise RuntimeError("DETERMINISTIC_CONTINUATION_GATE=FAIL reference not pointlike")
    ref = model.prior.reference()
    point = {name: float(value) for name, value in zip(sampled, ref)}
    lp = model.logposterior(ref)
    loglikes = list(getattr(lp, "loglikes", []))
    if len(loglikes) != len(model.likelihood):
        raise RuntimeError("SEED_EVALUATION_GATE=FAIL likelihood count")
    row = dict(point)
    try:
        row.update({str(k): float(v) for k, v in model.parameterization.constant_params().items()
                    if isinstance(v, (int, float))})
    except Exception:
        pass
    total = 0.0
    comps: dict[str, float] = {}
    for name, val in zip(model.likelihood.keys(), loglikes):
        x = -2.0 * float(val)
        comps[f"chi2__{name}"] = x
        row[f"chi2__{name}"] = x
        total += x
    row["chi2"] = total
    logpost = getattr(lp, "logpost", None)
    if logpost is not None:
        row["minuslogpost"] = -float(logpost)
    obj, _, basis, pen = comparable_objective(row)
    if obj is None or not math.isfinite(obj):
        raise RuntimeError("SEED_EVALUATION_GATE=FAIL nonfinite")
    return {
        "minimum": row, "objective_chi2": obj, "objective_basis": basis,
        "chi2_components": comps, "constraint_shape_penalties": pen,
        "sampled_parameters": sampled, "prior_gate": gate, "refs": refs,
    }

def run_task_v11(chain: str, mode: str, family: str, restart: int, q011_path: str | Path,
                 v10_path: str | Path, phase1_summary: str | Path | None,
                 output: str | Path, c: Mapping[str, Any], max_evals=None) -> int:
    global V10_RESULT_PATH, PHASE1_SUMMARY_PATH
    V10_RESULT_PATH = Path(v10_path)
    load_v10_result()
    if family.startswith("p1_"):
        if phase1_summary is None:
            raise RuntimeError("PHASE1_SUMMARY_GATE=FAIL phase2 family without summary")
        PHASE1_SUMMARY_PATH = Path(phase1_summary)
        load_phase1_summary()
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        seed = seed_evaluation(chain, mode, family, restart, q011_path, c, out)
    except Exception as exc:
        dump_json(out, {
            "case_id": c["project"]["case_id"], "q": "Q014", "run_id": RUN_ID,
            "chain": chain, "mode": mode, "start_family": family, "restart_index": restart,
            "status": "TECHNICAL_FAILURE", "failure_type": "V11_SEED_OR_PRIOR_GATE",
            "error": repr(exc), "finite_result": False,
        })
        return 9
    rc = impl.run_task(chain, mode, family, restart, q011_path, out, c, max_evals)
    rec = json.loads(out.read_text(encoding="utf-8"))
    rec["v10_numerical_parent"] = {
        "run_id": V10_EXPECTED_RUN, "result_id": V10_EXPECTED_RESULT,
        "scientifically_usable_result": False,
    }
    rec["continuation_phase"] = "PHASE2_SAME_RUN_FREE_CERTIFICATION" if family.startswith("p1_") else "PHASE1_V10_CONTINUATION"
    rec["phase1_source_mode"] = (
        "reference_free_h0" if family.startswith("p1_free") else
        ("fixed_h0_71p5" if family.startswith("p1_fixed") else None)
    )
    rec["same_run_fixed_to_free_embedding"] = bool(family.startswith("p1_fixed") and mode == "reference_free_h0")
    rec["seed_candidate"] = {k: v for k, v in seed.items() if k != "refs"}
    rec["seed_start_vector_sha256"] = impl.canonical_hash(seed["refs"])
    if rec.get("status") == "COMPLETE":
        row = rec.get("minimum", {})
        corrected, comps, basis, pen = comparable_objective(row)
        rec["raw_2minuslogpost_diagnostic"] = 2.0 * float(row["minuslogpost"]) if "minuslogpost" in row else None
        rec["likelihood_chi2_scalar"] = float(row["chi2"]) if "chi2" in row else None
        rec["constraint_shape_penalties"] = pen
        rec["objective_chi2"] = corrected
        rec["objective_basis"] = basis
        rec["chi2_components"] = comps
        tol = float(c["execution"]["v10_seed_policy"]["seed_objective_tolerance"])
        if corrected is None or seed["objective_chi2"] < corrected - tol:
            rec["optimizer_candidate_before_seed_preservation"] = {
                "minimum": row, "objective_chi2": corrected, "objective_basis": basis,
                "constraint_shape_penalties": pen,
            }
            rec["minimum"] = seed["minimum"]
            rec["chi2_components"] = seed["chi2_components"]
            rec["objective_chi2"] = seed["objective_chi2"]
            rec["objective_basis"] = seed["objective_basis"]
            rec["constraint_shape_penalties"] = seed["constraint_shape_penalties"]
            rec["likelihood_chi2_scalar"] = float(seed["minimum"]["chi2"])
            rec["selected_candidate"] = "EXACT_DETERMINISTIC_SEED"
        else:
            rec["selected_candidate"] = "OPTIMIZER_MINIMUM"
        rec["seed_candidate_preservation_pass"] = float(rec["objective_chi2"]) <= float(seed["objective_chi2"]) + tol
        rec["finite_result"] = math.isfinite(float(rec["objective_chi2"]))
    dump_json(out, rec)
    return 0 if rec.get("status") == "COMPLETE" and rec.get("finite_result") else rc

def phase_tasks(c: Mapping[str, Any], phase: str) -> list[dict[str, Any]]:
    families = c["execution"]["phase1_start_families"] if phase == "phase1" else c["execution"]["phase2_start_families"]
    tasks: list[dict[str, Any]] = []
    base_restart = {"reference_free_h0": 10, "fixed_h0_71p5": 20, "q011_shared_physics": 30}
    if phase == "phase2":
        base_restart = {"reference_free_h0": 40, "fixed_h0_71p5": 50, "q011_shared_physics": 60}
    for chain in c["chains"]:
        for mode, fs in families.items():
            for i, family in enumerate(fs):
                tag = f"{chain}-{mode}-{family}".replace("_", "-").replace(".", "-")
                tasks.append({
                    "phase": phase, "chain": chain, "mode": mode, "start_family": family,
                    "restart_index": base_restart[mode] + i, "tag": tag,
                })
    return tasks

def _record_key(r: Mapping[str, Any]) -> tuple[str, str, str]:
    return str(r.get("chain")), str(r.get("mode")), str(r.get("start_family"))

def _load_records(paths: list[str | Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for raw in paths:
        p = Path(raw)
        files = list(p.rglob("*.json")) if p.is_dir() else [p]
        for f in files:
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            if d.get("q") == "Q014" and d.get("run_id") == RUN_ID and "mode" in d:
                d["_source_file"] = str(f)
                out.append(d)
    return out

def _finite_record(r: Mapping[str, Any]) -> bool:
    return r.get("status") == "COMPLETE" and r.get("objective_basis") == BASIS and finite_number(r.get("objective_chi2"))

def select_phase1(inputs: list[str | Path], output: str | Path, c: Mapping[str, Any]) -> int:
    records = _load_records(inputs)
    expected = phase_tasks(c, "phase1")
    ek = {_record_key(x) for x in expected}
    rk = {_record_key(x) for x in records}
    missing = sorted(ek - rk)
    dupes = sorted(k for k in rk if sum(1 for r in records if _record_key(r) == k) > 1)
    result: dict[str, Any] = {
        "q": "Q014", "run_id": RUN_ID, "summary_type": "PHASE1_SEED_SUMMARY",
        "expected": len(ek), "returned": len(rk), "missing": missing, "duplicates": dupes,
        "chains": {}, "status": "FAIL",
    }
    ok = not missing and not dupes
    for chain in c["chains"]:
        result["chains"][chain] = {}
        for mode in ("reference_free_h0", "fixed_h0_71p5"):
            good = sorted(
                [r for r in records if r.get("chain") == chain and r.get("mode") == mode and _finite_record(r)],
                key=lambda r: float(r["objective_chi2"])
            )
            if not good:
                ok = False
                result["chains"][chain][mode] = {"best_record": None, "best_objective_chi2": None}
            else:
                result["chains"][chain][mode] = {
                    "best_record": good[0],
                    "best_objective_chi2": float(good[0]["objective_chi2"]),
                    "finite_candidates": len(good),
                }
    result["status"] = "PASS" if ok else "FAIL"
    dump_json(output, result)
    print(json.dumps({k: result[k] for k in ("summary_type", "expected", "returned", "missing", "duplicates", "status")}, indent=2))
    return 0 if ok else 12

def v10_parent_preflight(path: str | Path) -> dict[str, Any]:
    try:
        d = load_v10_result(path)
        ok, err = True, None
    except Exception as exc:
        d, ok, err = {}, False, repr(exc)
    return {
        "pass": ok, "error": err, "run_id": d.get("run_id"), "result_id": d.get("result_id"),
        "validation_status": d.get("validation_status"),
        "jobs_returned": d.get("job_manifest", {}).get("returned"),
        "planck_free_spread": d.get("chains", {}).get("planck_npipe_k039_approx", {}).get("profiles", {}).get("reference_free_h0", {}).get("best_two_delta_chi2"),
        "spt_only_monotonicity": d.get("chains", {}).get("spt_d1_only", {}).get("penalties", {}).get("fixed_profile_monotonicity_pass"),
    }

def cli() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=CONFIG_NAME)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--phase", choices=["phase1", "phase2"], required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--q011", required=True)
    p.add_argument("--v10-result", required=True)
    p.add_argument("--environment", action="store_true")
    p.add_argument("--chain", choices=list(prev.CONSTRAINTS))
    p.add_argument("--output", required=True)

    p = sub.add_parser("smoke")
    p.add_argument("--chain", choices=list(prev.CONSTRAINTS), required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("select-phase1")
    p.add_argument("--inputs", nargs="+", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("run")
    p.add_argument("--chain", choices=list(prev.CONSTRAINTS), required=True)
    p.add_argument("--mode", choices=["reference_free_h0", "fixed_h0_71p5", "q011_shared_physics"], required=True)
    p.add_argument("--start-family", choices=[
        "v10_free_best", "v10_free_jitter", "v10_fixed_best", "v10_fixed_jitter",
        "p1_free_best", "p1_free_jitter", "p1_fixed_best", "p1_fixed_jitter", "q011"
    ], required=True)
    p.add_argument("--restart-index", type=int, required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--v10-result", required=True)
    p.add_argument("--phase1-summary")
    p.add_argument("--max-evals", type=int)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_cfg(a.config)

    if a.cmd == "plan":
        tasks = phase_tasks(c, a.phase)
        dump_json(a.output, {"include": tasks})
        print(json.dumps({"include": tasks}, separators=(",", ":")))
        return 0
    if a.cmd == "preflight":
        global V10_RESULT_PATH
        V10_RESULT_PATH = Path(a.v10_result)
        r = impl.preflight(c, a.q011, a.environment, a.chain)
        vp = v10_parent_preflight(a.v10_result)
        r["checks"]["V10_NUMERICAL_PARENT_GATE"] = vp["pass"]
        r["v10_parent"] = vp
        r["checks"]["NORMALIZATION_FREE_OBJECTIVE_GATE"] = c["scientific_surface"]["objective_comparability_repair"]["cross_mode_comparable"] is True
        r["checks"]["SAME_RUN_FIXED_TO_FREE_DESIGN_GATE"] = c["execution"]["v11_same_run_policy"]["same_run_fixed_to_free_embedding_required"] is True
        r["status"] = "PASS" if all(r["checks"].values()) else "FAIL"
        dump_json(a.output, r)
        print(json.dumps(r, indent=2))
        return 0 if r["status"] == "PASS" else 7
    if a.cmd == "smoke":
        return impl.smoke(a.chain, a.q011, a.output, c)
    if a.cmd == "select-phase1":
        return select_phase1(a.inputs, a.output, c)
    if a.cmd == "run":
        return run_task_v11(a.chain, a.mode, a.start_family, a.restart_index, a.q011,
                            a.v10_result, a.phase1_summary, a.output, c, a.max_evals)
    return 2

if __name__ == "__main__":
    raise SystemExit(cli())
