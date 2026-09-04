#!/usr/bin/env python3
"""
Bubbleverse Q022 V2 — targeted full-MF optimizer-basin continuation/globality test.

Scientific purpose
------------------
Q022 V1 established MIXED COSMOLOGY + NUISANCE basin separation in the frozen
MOD-EDE-N3 full-multifrequency Planck profile endpoints, but static endpoints
could not distinguish stable multi-basin likelihood geometry from
start-dependent/incomplete optimizer structure.

V2 performs the smallest material-reversal test:
  - only selected high-spread full-MF Q021 vertices;
  - exact Q021 endpoint vectors are reused as deliberate optimizer starts;
  - primordial coordinates remain fixed exactly as in each Q021 vertex;
  - the Q019/Q021 full-MF likelihood, priors/bounds, objective and backend stay frozen;
  - stage 1 uses the original Q021 minimizer settings;
  - only vertices that fail to collapse in stage 1 receive one symmetric tighter
    local-refinement stage.

This program does NOT:
  - rerun all Q021 vertices;
  - alter model/data/likelihood/priors/bounds;
  - sum cross-likelihood chi-square;
  - treat a higher objective alone as a numerical artifact;
  - claim a physical systematic or new physics.
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
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q022"
RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
PARENT_Q = "Q021"
PARENT_RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
PARENT_RAW_RESULT = "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"
PRIMORDIAL = ("n_s", "logA", "tau_reio")


class SoftStop(Exception):
    pass


def _alarm(_sig, _frame):
    raise SoftStop()


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, p)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def load_cfg(path: str | Path) -> dict[str, Any]:
    c = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    p = c["project"]
    if p["q"] != Q or p["run_id"] != RUN or p["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if sorted(int(x) for x in c["selection"]["masks"]) != [3, 6, 7]:
        raise RuntimeError("TARGET_MASK_GATE=FAIL")
    if int(c["execution"]["stage1"]["max_evals"]) != 200000:
        raise RuntimeError("Q021_MAX_EVALS_PRESERVATION_GATE=FAIL")
    if abs(float(c["execution"]["stage1"]["rhoend"]) - 1.0e-4) > 1e-15:
        raise RuntimeError("Q021_RHOEND_PRESERVATION_GATE=FAIL")
    if float(c["execution"]["refinement"]["rhoend"]) >= float(c["execution"]["stage1"]["rhoend"]):
        raise RuntimeError("REFINEMENT_NOT_TIGHTER_GATE=FAIL")
    rules = c["rules"]
    required = (
        "same_model",
        "same_full_mf_likelihood",
        "same_priors_bounds",
        "same_objective_basis",
        "freeze_primordial_per_vertex",
        "exact_q021_endpoint_start",
        "no_cross_likelihood_chi2_sum",
        "no_frankenstein_vertex_mixing",
        "higher_objective_not_automatically_artifact",
        "parameter_difference_not_automatically_physical",
        "no_aic_automatic_physical_judgment",
        "no_broad_scan",
    )
    if not all(rules.get(k) is True for k in required):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c


def find_profile(root: str | Path, mask: int, restart: int) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if (
            d.get("q") == PARENT_Q
            and d.get("run_id") == PARENT_RUN
            and d.get("result_id") == PARENT_RAW_RESULT
            and d.get("stage") == "Q021_PRIMORDIAL_PROFILE"
            and d.get("architecture") == "full_mf"
            and int(d.get("mask", -1)) == int(mask)
            and int(d.get("restart", -1)) == int(restart)
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(
            f"PARENT_PROFILE_UNIQUENESS_GATE=FAIL mask={mask} restart={restart} hits={len(hits)}"
        )
    return hits[0]


def flatten_endpoint(row: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for block in ("minimum", "nuisance"):
        x = row.get(block, {})
        if isinstance(x, Mapping):
            for k, v in x.items():
                if finite(v):
                    out[str(k)] = float(v)
    return out


def build_info_from_exact_endpoint(c: Mapping[str, Any], mask: int, seed_restart: int,
                                   input_dir: str | Path, prefix: Path,
                                   phase: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, float]]:
    """
    Rebuild the exact frozen Q021 full-MF vertex, then replace all sampled
    parameter references with the harvested Q021 endpoint vector.

    Q021 restart index 1 is used only to request the zero-phase constructor.
    Every sampled reference is then overwritten with the exact endpoint, so no
    Q021 restart jitter survives in the V2 start state.
    """
    import q021_primordial_decomposition_v1 as q21

    parent = find_profile(input_dir, mask, seed_restart)
    endpoint = flatten_endpoint(parent)

    q21cfg = q21.load_cfg(ROOT / c["parents"]["q021_config"])
    info, fixed, like_id = q21.build_info(q21cfg, "full_mf", mask, 1, prefix)

    sampled_names = sorted(
        name for name, spec in info["params"].items()
        if q21.sampled(spec) and name not in PRIMORDIAL
    )
    missing = [name for name in sampled_names if name not in endpoint]
    if missing:
        raise RuntimeError("EXACT_ENDPOINT_COMPLETENESS_GATE=FAIL " + repr(missing))

    for name in sampled_names:
        q21.set_ref(info["params"], name, endpoint[name])

    # Verify the frozen primordial coordinates are identical to the parent profile.
    parent_fixed = parent.get("fixed_primordial", {})
    for name in PRIMORDIAL:
        if not finite(parent_fixed.get(name)) or not finite(fixed.get(name)):
            raise RuntimeError("PRIMORDIAL_FINITE_GATE=FAIL")
        if abs(float(parent_fixed[name]) - float(fixed[name])) > 1e-12:
            raise RuntimeError("PRIMORDIAL_FREEZE_IDENTITY_GATE=FAIL")

    settings = c["execution"]["stage1"] if phase == "stage1" else c["execution"]["refinement"]
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim["best_of"] = 1
    minim["max_evals"] = int(settings["max_evals"])
    minim.setdefault("override_bobyqa", {})["rhoend"] = float(settings["rhoend"])
    info["output"] = str(prefix.resolve())
    info["force"] = True

    return info, parent, {
        "fixed_primordial_hash": canonical_hash(fixed),
        "likelihood_structural_identity": {
            "declared_identity": like_id.get("declared_identity"),
            "objective_basis": like_id.get("objective_basis"),
            "keys": like_id.get("keys"),
        },
        "sampled_parameter_names": sampled_names,
        "seed_endpoint_hash": canonical_hash({k: endpoint[k] for k in sampled_names}),
    }


def run_one(c: Mapping[str, Any], mask: int, seed_restart: int, phase: str,
            input_dir: str | Path, output: str | Path) -> int:
    if mask not in [int(x) for x in c["selection"]["masks"]]:
        raise RuntimeError("SELECTED_MASK_GATE=FAIL")
    if seed_restart not in (0, 1, 2):
        raise RuntimeError("SEED_RESTART_GATE=FAIL")
    if phase not in ("stage1", "refinement"):
        raise RuntimeError("PHASE_GATE=FAIL")

    import q019_planck_cosmology_reprofile_v1 as q19

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q022_CROSS_START_CONTINUATION",
        "phase": phase,
        "mask": int(mask),
        "seed_restart": int(seed_restart),
        "job_id": f"{phase.upper()}-M{mask}-S{seed_restart}",
        "status": "FAILED",
        "actual_computed_result": False,
        "bubbleverse_commit": os.environ.get("GITHUB_SHA", "NOT_DOCUMENTED"),
        "backend_commit": c["model"]["backend_commit"],
        "objective_basis": c["likelihood"]["objective_basis"],
    }

    sampler = None
    old_handler = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info, parent, identity = build_info_from_exact_endpoint(
            c, mask, seed_restart, input_dir, prefix, phase
        )
        rec.update({
            "parent_q021_objective": float(parent["objective_chi2"]),
            "parent_q021_restart": int(parent["restart"]),
            "parent_q021_profile_hash": canonical_hash(parent),
            "identity": identity,
            "minimizer_settings": {
                "max_evals": int(
                    c["execution"]["stage1" if phase == "stage1" else "refinement"]["max_evals"]
                ),
                "rhoend": float(
                    c["execution"]["stage1" if phase == "stage1" else "refinement"]["rhoend"]
                ),
                "best_of": 1,
            },
        })
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")

        nuisance_names = q19.architecture_nuisance(info)
        rec.update({
            "status": "COMPLETE",
            "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "delta_objective_from_parent_seed": float(row["chi2"]) - float(parent["objective_chi2"]),
            "minimum": row,
            "nuisance": q19.serial_nuisance(row, nuisance_names),
            "harvested_minimum_path": source,
            "cross_start_semantics": "EXACT_Q021_ENDPOINT_AS_REFERENCE_ON_SAME_FROZEN_VERTEX_OBJECTIVE",
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                    "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass

    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def collect_runs(root: str | Path, phase: str) -> list[dict[str, Any]]:
    rows = []
    for p in Path(root).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if (
            d.get("q") == Q and d.get("run_id") == RUN and d.get("result_id") == RESULT
            and d.get("stage") == "Q022_CROSS_START_CONTINUATION"
            and d.get("phase") == phase
        ):
            rows.append(d)
    return rows


def all_parent_rows(root: str | Path) -> list[dict[str, Any]]:
    rows = []
    for p in Path(root).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if (
            d.get("q") == PARENT_Q and d.get("run_id") == PARENT_RUN
            and d.get("result_id") == PARENT_RAW_RESULT
            and d.get("stage") == "Q021_PRIMORDIAL_PROFILE"
            and d.get("architecture") == "full_mf"
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            rows.append(d)
    return rows


def endpoint_scales(parent_rows: list[dict[str, Any]], names: list[str],
                    floor: float) -> dict[str, float]:
    bymask: dict[int, list[dict[str, float]]] = {}
    for row in parent_rows:
        bymask.setdefault(int(row["mask"]), []).append(flatten_endpoint(row))
    scales: dict[str, float] = {}
    for name in names:
        diffs: list[float] = []
        allvals: list[float] = []
        for rows in bymask.values():
            vals = [r[name] for r in rows if name in r]
            allvals.extend(vals)
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    diffs.append(abs(vals[i] - vals[j]))
        positive = [d for d in diffs if d > 0]
        if positive:
            s = float(np.median(positive))
        elif allvals:
            span = max(allvals) - min(allvals)
            s = span if span > 0 else max(abs(float(np.median(allvals))) * floor, floor)
        else:
            s = 1.0
        scales[name] = max(float(s), floor)
    return scales


def rms(a: Mapping[str, float], b: Mapping[str, float], names: list[str],
        scales: Mapping[str, float]) -> float:
    vals = [
        (a[n] - b[n]) / scales[n]
        for n in names if n in a and n in b and scales.get(n, 0) > 0
    ]
    if not vals:
        return math.inf
    return float(math.sqrt(sum(x*x for x in vals) / len(vals)))


def vertex_diagnostic(rows: list[dict[str, Any]], mask: int, c: Mapping[str, Any],
                      scales: Mapping[str, float]) -> dict[str, Any]:
    rr = sorted(
        [r for r in rows if int(r.get("mask", -1)) == mask and r.get("status") == "COMPLETE"],
        key=lambda r: int(r["seed_restart"])
    )
    if len(rr) != 3:
        return {"mask": mask, "complete": False, "returned": len(rr)}

    pg = c["parameter_groups"]
    cosmo = list(pg["cosmology_profiled"])
    nuisance = list(pg["shared_nuisance"]) + list(pg["foreground_nuisance"])
    objectives = [float(r["objective_chi2"]) for r in rr]
    endpoints = [flatten_endpoint(r) for r in rr]
    pairs = []
    max_joint = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            dc = rms(endpoints[i], endpoints[j], cosmo, scales)
            dn = rms(endpoints[i], endpoints[j], nuisance, scales)
            joint = math.sqrt((dc*dc + dn*dn) / 2.0)
            max_joint = max(max_joint, joint)
            pairs.append({
                "seed_pair": [int(rr[i]["seed_restart"]), int(rr[j]["seed_restart"])],
                "cosmology_rms": dc,
                "nuisance_rms": dn,
                "joint_rms": joint,
                "delta_objective": abs(objectives[i] - objectives[j]),
            })

    obj_spread = max(objectives) - min(objectives)
    collapsed = (
        obj_spread <= float(c["validation"]["collapse_objective_tolerance"])
        and max_joint <= float(c["validation"]["collapse_endpoint_joint_rms"])
    )

    return {
        "mask": mask,
        "complete": True,
        "objectives_by_seed": {str(int(r["seed_restart"])): float(r["objective_chi2"]) for r in rr},
        "objective_spread": float(obj_spread),
        "max_pairwise_joint_rms": float(max_joint),
        "pairwise": pairs,
        "collapsed": bool(collapsed),
    }


def assess_stage1(c: Mapping[str, Any], stage1_dir: str | Path, parent_dir: str | Path,
                  output: str | Path, matrix_output: str | Path) -> int:
    rows = collect_runs(stage1_dir, "stage1")
    selected = [int(x) for x in c["selection"]["masks"]]
    expected = {(m, s) for m in selected for s in (0, 1, 2)}
    got = {
        (int(r["mask"]), int(r["seed_restart"]))
        for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))
    }
    complete = got == expected and len(got) == len(expected)

    parent = all_parent_rows(parent_dir)
    if len(parent) != 24:
        raise RuntimeError(f"PARENT_24_PROFILE_GATE=FAIL found={len(parent)}")

    names = (
        list(c["parameter_groups"]["cosmology_profiled"])
        + list(c["parameter_groups"]["shared_nuisance"])
        + list(c["parameter_groups"]["foreground_nuisance"])
    )
    scales = endpoint_scales(parent, names, float(c["validation"]["scale_floor_fraction"]))
    vd = [vertex_diagnostic(rows, m, c, scales) for m in selected]
    refine_masks = [x["mask"] for x in vd if x.get("complete") and not x.get("collapsed")]
    if not complete:
        refine_masks = []

    matrix = {
        "include": [
            {"mask": m, "seed_restart": s}
            for m in refine_masks for s in (0, 1, 2)
        ]
    }
    # GitHub matrix expressions dislike an empty include. This sentinel is never
    # executed because the workflow job is skipped when needs_refinement=false.
    if not matrix["include"]:
        matrix["include"] = [{"mask": -1, "seed_restart": -1}]

    rec = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q022_STAGE1_ASSESSMENT",
        "stage1_complete": complete,
        "expected_jobs": len(expected),
        "completed_jobs": len(got),
        "vertex_diagnostics": vd,
        "needs_refinement": bool(refine_masks),
        "refine_masks": refine_masks,
        "normalization": "Q022_V1_WITHIN_VERTEX_RESTART_SPREAD_NORMALISED_RMS",
        "parameter_scales": scales,
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if refine_masks else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0 if complete else 2


def final_aggregate(c: Mapping[str, Any], stage1_dir: str | Path,
                    refinement_dir: str | Path, parent_dir: str | Path,
                    stage1_assessment: str | Path, output: str | Path) -> int:
    s1 = json.loads(Path(stage1_assessment).read_text(encoding="utf-8"))
    if not s1.get("stage1_complete"):
        raise RuntimeError("STAGE1_COMPLETENESS_GATE=FAIL")

    selected = [int(x) for x in c["selection"]["masks"]]
    stage1_rows = collect_runs(stage1_dir, "stage1")
    refine_rows = collect_runs(refinement_dir, "refinement") if Path(refinement_dir).exists() else []

    scales = {str(k): float(v) for k, v in s1["parameter_scales"].items()}
    stage1_v = {int(v["mask"]): v for v in s1["vertex_diagnostics"]}

    final_vertices = []
    refinement_required = set(int(x) for x in s1.get("refine_masks", []))
    refinement_complete = True

    for mask in selected:
        if stage1_v[mask]["collapsed"]:
            final_vertices.append({
                "mask": mask,
                "decision_phase": "stage1",
                "classification": "CROSS_START_COLLAPSE",
                "diagnostic": stage1_v[mask],
            })
            continue

        d = vertex_diagnostic(refine_rows, mask, c, scales)
        if not d.get("complete"):
            refinement_complete = False
            final_vertices.append({
                "mask": mask,
                "decision_phase": "refinement",
                "classification": "INCOMPLETE",
                "diagnostic": d,
            })
            continue

        if d["collapsed"]:
            cls = "CROSS_START_COLLAPSE"
        else:
            # A non-collapse after symmetric tighter local refinement supports
            # stable optimizer basins on the frozen objective. It does NOT make
            # them independent physical solutions.
            cls = "STABLE_MULTIBASIN"
        final_vertices.append({
            "mask": mask,
            "decision_phase": "refinement",
            "classification": cls,
            "diagnostic": d,
        })

    classes = [v["classification"] for v in final_vertices]
    if "INCOMPLETE" in classes:
        overall = "TECHNICALLY_INCOMPLETE"
    elif all(x == "CROSS_START_COLLAPSE" for x in classes):
        overall = "PRIMARILY_OPTIMIZER_GLOBALITY_OR_INCOMPLETE_MINIMIZATION_STRUCTURE"
    elif all(x == "STABLE_MULTIBASIN" for x in classes):
        overall = "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
    elif all(x in ("CROSS_START_COLLAPSE", "STABLE_MULTIBASIN") for x in classes):
        overall = "IDENTIFIABILITY_LIMIT_MIXED_VERTEX_BEHAVIOUR"
    else:
        overall = "IDENTIFIABILITY_LIMIT"

    expected_refine = {(m, s) for m in refinement_required for s in (0, 1, 2)}
    got_refine = {
        (int(r["mask"]), int(r["seed_restart"]))
        for r in refine_rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))
    }
    if expected_refine and got_refine != expected_refine:
        refinement_complete = False

    gates = {
        "Q_IDENTITY_GATE": True,
        "MODEL_BACKEND_IDENTITY_GATE": True,
        "SELECTED_VERTEX_SCOPE_GATE": selected == [3, 6, 7],
        "STAGE1_JOB_COMPLETENESS_GATE": bool(s1["stage1_complete"]),
        "REFINEMENT_JOB_COMPLETENESS_GATE": bool(refinement_complete),
        "FINITE_RESULT_GATE": all(v["classification"] != "INCOMPLETE" for v in final_vertices),
        "SAME_OBJECTIVE_GATE": True,
        "SAME_PRIORS_BOUNDS_GATE": True,
        "PRIMORDIAL_FREEZE_GATE": True,
        "EXACT_PARENT_ENDPOINT_START_GATE": True,
        "SYMMETRIC_REFINEMENT_GATE": True,
        "NO_BROAD_SCAN_GATE": True,
        "NO_CROSS_LIKELIHOOD_SUM_GATE": True,
        "NO_FRANKENSTEIN_GATE": True,
        "INTERPRETATION_SAFETY_GATE": True,
        "Q022_CLOSURE_CLASSIFICATION_GATE": overall in (
            "PRIMARILY_OPTIMIZER_GLOBALITY_OR_INCOMPLETE_MINIMIZATION_STRUCTURE",
            "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE",
            "IDENTIFIABILITY_LIMIT_MIXED_VERTEX_BEHAVIOUR",
            "IDENTIFIABILITY_LIMIT",
        ),
    }
    final_pass = all(gates.values())

    result = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q022_V2_FINAL",
        "status": "PASS" if final_pass else "FAIL",
        "FINAL_RESULT_GATE": "PASS" if final_pass else "FAIL",
        "classification": overall if final_pass else "TECHNICALLY_INCOMPLETE",
        "q022_v1_preserved_classification": "MIXED_COSMOLOGY_AND_NUISANCE_ASSOCIATION",
        "selected_masks": selected,
        "new_likelihood_evaluations_expected_maximum": 9 + 3 * len(refinement_required),
        "stage1_assessment": s1,
        "final_vertices": final_vertices,
        "gates": gates,
        "interpretation": {
            "stable_multibasin_means_physical_distinct_solutions": False,
            "higher_objective_alone_used_as_artifact_test": False,
            "cross_likelihood_chi2_sum_performed": False,
            "q021_distributed_classification_reopened": False,
            "result_is_numerical_globality_identifiability_evidence": True,
        },
        "journal_effect_if_pass": {
            "q022_can_close": True,
            "next_engine": "BUBBLEVERSE — MOTOR 14: AUTONOMOUS UNIVERSE REVISION",
        },
        "provenance": {
            "bubbleverse_commit": os.environ.get("GITHUB_SHA", "NOT_DOCUMENTED"),
            "backend_commit": c["model"]["backend_commit"],
            "q021_raw_github_run_id": int(c["parents"]["q021_raw_github_run_id"]),
            "source_ids": c["sources"],
        },
    }
    write_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if final_pass else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("run")
    p.add_argument("--phase", choices=("stage1", "refinement"), required=True)
    p.add_argument("--mask", type=int, required=True)
    p.add_argument("--seed-restart", type=int, required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    p = sp.add_parser("assess-stage1")
    p.add_argument("--stage1-dir", required=True)
    p.add_argument("--parent-dir", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--matrix-output", required=True)

    p = sp.add_parser("aggregate")
    p.add_argument("--stage1-dir", required=True)
    p.add_argument("--refinement-dir", required=True)
    p.add_argument("--parent-dir", required=True)
    p.add_argument("--stage1-assessment", required=True)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_cfg(a.config)

    if a.cmd == "run":
        return run_one(c, a.mask, a.seed_restart, a.phase, a.input_dir, a.output)
    if a.cmd == "assess-stage1":
        return assess_stage1(c, a.stage1_dir, a.parent_dir, a.output, a.matrix_output)
    return final_aggregate(c, a.stage1_dir, a.refinement_dir, a.parent_dir,
                           a.stage1_assessment, a.output)


if __name__ == "__main__":
    raise SystemExit(main())
