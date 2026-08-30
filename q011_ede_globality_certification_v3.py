#!/usr/bin/env python3
"""
Bubbleverse Q011 — n=3 EDE fixed-H0 globality / basin certification V3.

V3 is a technical-gate semantics patch layered on the repaired Q011 orchestration over Q011 V1. It deliberately preserves the
V1/Q005-V14 scientific surface, start-family design, optimizer settings, targets,
priors, bounds, likelihoods and classification logic.

Documented V1 repairs:
1) Q008/profile and Stage-2 endpoint extraction must not require H0 in stored
   sampled vectors because H0 is fixed externally for each profile target.
2) q005_hpc_v14.cobaya_run must be called with (path, cfg), not path alone.
3) A deterministic technical execution gate must pass before the 128-job matrix
   is allowed to launch.

This file imports Q011 V1 and patches orchestration only. Finite multi-start
optimization is never described as a mathematical proof of globality.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any

import yaml

import q005_hpc_v14 as core
import q011_ede_globality_certification_v1 as v1

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q011_ede_globality_certification_v3_config.yml"
CODE_VERSION = "3.0-q011-technical-gate-maxfun-aware"
CURRENT_Q = "Q011"

# Ensure V1 aggregate/result helpers record V3 program identity when delegated.
v1.CODE_VERSION = CODE_VERSION


def deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"CONFIG_GATE=FAIL non-mapping YAML: {p}")
    return data


def cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    overlay = load_yaml(path)
    parent_cfg = overlay.get("v3_patch", {}).get(
        "inherits_config", "q011_ede_globality_certification_v1_config.yml"
    )
    base = load_yaml(parent_cfg)
    merged = deep_merge(base, overlay)
    merged.pop("v3_patch", None)
    return merged


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def q008_seed(c: dict[str, Any], q008: dict[str, Any], target_h0: float) -> dict[str, float]:
    """
    V3 inherited FIX-001:
    H0 is a fixed profile coordinate, not a required coordinate in Q008's stored
    sampled best-fit vector. Extract every sampled coordinate except H0, then
    inject the fixed target explicitly.
    """
    if q008.get("q") != "Q-008":
        raise RuntimeError("Q008_PARENT_IDENTITY_GATE=FAIL")
    profiles = q008.get("profile_targets")
    if not isinstance(profiles, dict):
        raise RuntimeError("Q008_SCHEMA_GATE=FAIL missing profile_targets")
    rec = profiles[v1.numeric_key(profiles, target_h0)]
    bestfit = rec.get("bestfit")
    if not isinstance(bestfit, dict):
        raise RuntimeError("Q008_SCHEMA_GATE=FAIL missing bestfit")

    model = core.build_model(v1.base_cfg(c), "ede_n3", smoke=False, restart=0)
    needed_without_fixed_h0 = set(v1.sampled_specs(model)) - {"H0"}
    vals = v1.extract_vector(bestfit, needed_without_fixed_h0)
    vals["H0"] = float(target_h0)
    return vals


# Make every V1 helper that internally resolves q008_seed use the repaired function.
v1.q008_seed = q008_seed


def parent_endpoint_seed(c: dict[str, Any], parent: dict[str, Any], target: float) -> dict[str, float]:
    """
    V3 inherited FIX-001B:
    The same fixed-H0 rule applies when Stage 2 consumes a Stage-1 endpoint.
    """
    model = core.build_model(v1.base_cfg(c), "ede_n3", smoke=False, restart=0)
    needed_without_fixed_h0 = set(v1.sampled_specs(model)) - {"H0"}
    refs = v1.extract_vector(parent["bestfit"], needed_without_fixed_h0)
    refs["H0"] = float(target)
    return refs


def run_optimizer(
    c: dict[str, Any],
    q008: dict[str, Any],
    target: float,
    family: str,
    idx: int,
    recipe: dict[str, Any],
    stage: str,
    parent: dict[str, Any] | None = None,
) -> int:
    """
    V3 orchestration-equivalent replacement for V1 run_optimizer.

    Scientific model construction and result parsing remain delegated to V1/Q005.
    """
    if parent is None:
        refs, provenance = v1.start_vector(c, q008, target, recipe)
    else:
        if parent.get("status") != "PASS":
            dump_json(v1.result_file(c, stage, target, family), {
                "q": CURRENT_Q,
                "run_id": c["project"]["run_id"],
                "stage": stage,
                "target_h0": float(target),
                "start_family": family,
                "status": "FAIL",
                "reason": "PARENT_STAGE_NOT_PASS",
            })
            return 8
        refs = parent_endpoint_seed(c, parent, target)
        provenance = f"Exact {parent['stage']} endpoint"

    obj = v1.make_model(c, target, refs, stage, idx)
    obj["output"] = str(
        (ROOT / c["paths"]["results"] /
         f"cobaya_q011_{stage}_{v1.htag(target)}_{family}").resolve()
    )
    rendered = v1.render_file(c, stage, target, family)
    rendered.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

    # V3 inherited FIX-002: frozen Q005 V14 interface is cobaya_run(path, cfg).
    base = v1.base_cfg(c)
    rc = core.cobaya_run(rendered, base)

    rec: dict[str, Any] = {
        "q": CURRENT_Q,
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "stage": stage,
        "model": "ede_n3",
        "target_h0": float(target),
        "start_family": family,
        "profile_index": int(idx),
        "start_provenance": provenance,
        "start_vector_sha256": v1.canonical_hash(refs),
        "optimizer": c["optimizer"][stage],
        "rendered_yaml": str(rendered),
        "rendered_yaml_sha256": v1.sha256_file(rendered),
        "cobaya_exit": int(rc),
        "status": "FAIL",
        "scientific_surface": "FROZEN_Q005_V14",
        "v3_inherited_repairs": [
            "FIXED_H0_EXCLUDED_FROM_STORED_VECTOR_REQUIREMENT",
            "COBAYA_RUN_CALLED_WITH_PATH_AND_BASE_CONFIG",
        ],
    }

    prefix = Path(obj["output"])
    one = core.find_onepoint(prefix)
    if rc == 0 and one is not None:
        parsed = core.parse_onepoint(one, base)
        required = set(base["likelihood_accounting"]["required_nonlocal"])
        ok, reason = core.finite_scientific_point(parsed, required)
        rec["bestfit"] = parsed
        rec["finite_scientific_gate"] = bool(ok)
        if ok:
            rec["chi2_components"] = {
                k: float(parsed["chi2_nonoverlap"][k]) for k in sorted(required)
            }
            rec["chi2_scientific_total"] = float(sum(rec["chi2_components"].values()))
            rec["boundary_diagnostics"] = v1.boundary_diagnostics(c, parsed)
            rec["status"] = "PASS"
        else:
            rec["reason"] = reason
    else:
        rec["reason"] = f"COBAYA_EXIT_{rc}" if rc else "NO_ONEPOINT_RESULT"

    if parent and rec.get("status") == "PASS":
        rec["delta_chi2_vs_parent"] = (
            float(rec["chi2_scientific_total"])
            - float(parent["chi2_scientific_total"])
        )

    dump_json(v1.result_file(c, stage, target, family), rec)
    return 0 if rec["status"] == "PASS" else 9


def technical_gate(c: dict[str, Any], q008: dict[str, Any], output: str) -> int:
    """
    Cheap deterministic pre-matrix gate.

    Mandatory checks:
    - Q008-best seed at H0=71.5 constructs without requiring stored H0.
    - Q005 recovery seed constructs.
    - rendered YAML round-trips successfully.
    - the repaired two-argument cobaya_run interface reaches actual frozen-likelihood
      objective evaluations. A deliberate low-budget Py-BOBYQA MAXFUN is accepted
      as technical success only when Q005's own parser proves objective evaluations occurred.

    The gate is technical only and is not a Q011 scientific profile result.
    """
    report: dict[str, Any] = {
        "q": CURRENT_Q,
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "status": "FAIL",
        "scientific_result": False,
        "checks": {},
    }

    # Static/Q identity checks.
    pf = v1.preflight(c, q008)
    report["checks"]["STATIC_PREFLIGHT_GATE"] = pf

    # Confirm frozen backend environment already built by workflow.
    base = v1.base_cfg(c)
    env = core.preflight(base)
    report["checks"]["Q005_V14_ENVIRONMENT_GATE"] = {
        "status": env.get("status"),
        "pass": env.get("status") == "PASS",
    }

    target = float(c["technical_gate"]["target_h0"])
    q8 = q008_seed(c, q008, target)
    report["checks"]["Q008_BEST_SEED_GATE"] = {
        "pass": math.isclose(float(q8["H0"]), target, rel_tol=0.0, abs_tol=1e-12),
        "target_h0": target,
        "vector_sha256": v1.canonical_hash(q8),
    }

    recovery_family = c["technical_gate"]["recovery_family"]
    rseed = v1.recovery_seed(c, recovery_family, target)
    report["checks"]["Q005_RECOVERY_SEED_GATE"] = {
        "pass": math.isclose(float(rseed["H0"]), target, rel_tol=0.0, abs_tol=1e-12),
        "family": recovery_family,
        "vector_sha256": v1.canonical_hash(rseed),
    }

    # Render the same model path used by Stage 1, but with tiny technical workload.
    obj = v1.make_model(c, target, q8, "stage1", int(c["technical_gate"]["profile_index"]))
    minimize = obj["sampler"]["minimize"]
    minimize["max_evals"] = int(c["technical_gate"]["max_evals"])
    obj["output"] = str(
        (ROOT / c["paths"]["results"] / "cobaya_q011_v3_technical_gate").resolve()
    )
    rendered = ROOT / c["paths"]["rendered"] / "q011_v3_technical_gate.yaml"
    rendered.parent.mkdir(parents=True, exist_ok=True)
    rendered.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

    reread = yaml.safe_load(rendered.read_text(encoding="utf-8"))
    yaml_ok = (
        isinstance(reread, dict)
        and isinstance(reread.get("sampler"), dict)
        and "minimize" in reread["sampler"]
        and isinstance(reread.get("params"), dict)
    )
    report["checks"]["RENDERED_YAML_GATE"] = {
        "pass": bool(yaml_ok),
        "path": str(rendered),
        "sha256": v1.sha256_file(rendered),
    }

    # Critical interface smoke. A deliberately tiny BOBYQA run can validly hit
    # MAXFUN after evaluating the real frozen likelihood. That proves the Q011 ->
    # Cobaya -> CLASS/likelihood execution path works, even though it is not a
    # converged scientific minimization. Only this explicit Q005-native MAXFUN
    # classification is accepted as a non-zero technical-gate pass.
    rc = core.cobaya_run(rendered, base)
    logfile = ROOT / base["logs_dir"] / f"{rendered.stem}.log"
    failure = core.parse_minimizer_failure(logfile) if int(rc) != 0 else {}
    evals = int(failure.get("objective_evaluations", 0) or 0)
    maxfun_reached_after_objectives = (
        int(rc) != 0
        and failure.get("status") == "OPTIMIZER_MAXFUN_EXHAUSTED"
        and evals > 0
    )
    execution_ok = int(rc) == 0 or maxfun_reached_after_objectives

    # Preserve the exact Cobaya log inside the Q011 artifact namespace so future
    # diagnosis never loses the decisive evidence again.
    copied_log = ROOT / c["paths"]["results"] / "q011_v3_technical_gate_cobaya.log"
    copied_log.parent.mkdir(parents=True, exist_ok=True)
    if logfile.exists():
        copied_log.write_text(logfile.read_text(errors="replace"), encoding="utf-8")

    report["checks"]["COBAYA_EXECUTION_REACHED_OBJECTIVE_GATE"] = {
        "pass": bool(execution_ok),
        "exit_code": int(rc),
        "required_signature": "cobaya_run(path, cfg)",
        "max_evals": int(c["technical_gate"]["max_evals"]),
        "accepted_nonzero_exit_only_if": "Q005_NATIVE_OPTIMIZER_MAXFUN_EXHAUSTED_WITH_OBJECTIVE_EVALUATIONS_GT_0",
        "q005_failure_classification": failure,
        "objective_evaluations": evals,
        "cobaya_log": str(logfile),
        "artifact_log_copy": str(copied_log) if logfile.exists() else None,
    }

    mandatory = [
        pf.get("status") == "PASS",
        env.get("status") == "PASS",
        report["checks"]["Q008_BEST_SEED_GATE"]["pass"],
        report["checks"]["Q005_RECOVERY_SEED_GATE"]["pass"],
        report["checks"]["RENDERED_YAML_GATE"]["pass"],
        report["checks"]["COBAYA_EXECUTION_REACHED_OBJECTIVE_GATE"]["pass"],
    ]
    report["status"] = "PASS" if all(mandatory) else "FAIL"
    dump_json(output, report)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 12


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("plan")
    p.add_argument("--json", action="store_true")

    p = sp.add_parser("preflight")
    p.add_argument("--q008")

    p = sp.add_parser("technical-gate")
    p.add_argument("--q008", required=True)
    p.add_argument("--output", required=True)

    for stage in ("stage1", "stage2"):
        p = sp.add_parser(stage)
        p.add_argument("--q008", required=True)
        p.add_argument("--target-h0", required=True, type=float)
        p.add_argument("--start-family", required=True)
        p.add_argument("--profile-index", required=True, type=int)
        p.add_argument("--recipe-json", required=True)
        if stage == "stage2":
            p.add_argument("--stage1-root", required=True)

    p = sp.add_parser("aggregate")
    p.add_argument("--q008", required=True)
    p.add_argument("--stage1-root", required=True)
    p.add_argument("--stage2-root", required=True)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = cfg(a.config)

    if a.cmd == "plan":
        matrix = v1.matrix(c)
        print(json.dumps(matrix, separators=(",", ":")) if a.json
              else json.dumps(matrix, indent=2))
        return 0

    if a.cmd == "preflight":
        q8 = v1.load_json(a.q008) if a.q008 else None
        result = v1.preflight(c, q8)
        result["code_version"] = CODE_VERSION
        result["v3_patch_gate"] = (
            c["project"]["run_id"] == "Q011-EDE-GLOBALITY-CERTIFICATION-V3"
        )
        result["status"] = "PASS" if (
            result["status"] == "PASS" and result["v3_patch_gate"]
        ) else "FAIL"
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 4

    q8 = v1.load_json(a.q008)
    if v1.preflight(c, q8)["status"] != "PASS":
        raise SystemExit("Q011_V3_PREFLIGHT_GATE=FAIL")

    if a.cmd == "technical-gate":
        return technical_gate(c, q8, a.output)

    if a.cmd == "stage1":
        return run_optimizer(
            c, q8, a.target_h0, a.start_family, a.profile_index,
            json.loads(a.recipe_json), "stage1"
        )

    if a.cmd == "stage2":
        parent_path = v1.find_result(
            a.stage1_root, "stage1", a.target_h0, a.start_family
        )
        parent = v1.load_json(parent_path)
        return run_optimizer(
            c, q8, a.target_h0, a.start_family, a.profile_index,
            json.loads(a.recipe_json), "stage2", parent=parent
        )

    if a.cmd == "aggregate":
        return v1.aggregate(c, q8, a.stage1_root, a.stage2_root, a.output)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
