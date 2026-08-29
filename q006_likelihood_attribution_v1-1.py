#!/usr/bin/env python3
"""Bubbleverse Q-006 likelihood-component attribution V1.

Companion to the frozen Q-005 V14 common backend. It does not perform a blind
model scan. For n=3 EDE and common-backend varying-m_e it profiles the existing
likelihood at a finite set of fixed H0 targets and records non-overlapping
likelihood-component chi2 terms plus profiled parameter shifts.

Scientific claim boundary: common-backend attribution only; this is not an exact
K-036 or K-038 paper-native reproduction.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml

import q005_hpc_v14 as core

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q006_likelihood_attribution_v1_config.yml"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    return load_yaml(ROOT / path)


def canonical_hash(obj: Any) -> str:
    b = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(b).hexdigest()


def sampled_names(model: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for name, spec in model.get("params", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            names.add(name)
    for lspec in model.get("likelihood", {}).values():
        if isinstance(lspec, dict) and isinstance(lspec.get("params"), dict):
            for name, spec in lspec["params"].items():
                if isinstance(spec, dict) and "prior" in spec:
                    names.add(name)
    return names


def set_refs(model: dict[str, Any], refs: dict[str, float], *, skip: set[str] | None = None) -> None:
    skip = skip or set()
    expected = sampled_names(model) - skip
    supplied = set(refs) - skip
    missing = sorted(expected - supplied)
    extra = sorted(supplied - expected)
    if missing or extra:
        raise ValueError(f"REF_COVERAGE_GATE=FAIL missing={missing} extra={extra}")

    for name, spec in model.get("params", {}).items():
        if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
            spec["ref"] = float(refs[name])
    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict) or not isinstance(lspec.get("params"), dict):
            continue
        for name, spec in lspec["params"].items():
            if name in refs and name not in skip and isinstance(spec, dict) and "prior" in spec:
                spec["ref"] = float(refs[name])


def profile_specs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    i = 0
    for model, mcfg in cfg["models"].items():
        baseline = float(mcfg["baseline_h0"])
        for h0 in mcfg["h0_targets"]:
            h0 = float(h0)
            label = "baseline" if abs(h0 - baseline) < 1e-9 else f"h0_{h0:.1f}".replace(".", "p")
            out.append({"model": model, "profile": label, "target_h0": h0, "profile_index": i})
            i += 1
    return out


def plan(cfg: dict[str, Any]) -> dict[str, Any]:
    return {"include": profile_specs(cfg)}


def source_refs(cfg: dict[str, Any], model: str, target_h0: float) -> tuple[dict[str, float], str]:
    recovery = load_yaml(ROOT / cfg["parent"]["recovery_config"])
    mcfg = cfg["models"][model]
    baseline_h0 = float(mcfg["baseline_h0"])
    profile_name = mcfg["baseline_source_profile"] if abs(target_h0 - baseline_h0) < 1e-9 else mcfg["high_h0_source_profile"]
    refs = copy.deepcopy(recovery["profiles"][model][profile_name]["refs"])
    refs["H0"] = float(target_h0)
    return {k: float(v) for k, v in refs.items()}, profile_name


def build_profile(base: dict[str, Any], cfg: dict[str, Any], model: str, target_h0: float,
                  profile_index: int) -> tuple[dict[str, Any], dict[str, float], str]:
    obj = core.build_model(base, model, smoke=False, restart=0)
    refs, source_profile = source_refs(cfg, model, target_h0)
    set_refs(obj, refs, skip={"H0"})
    core.freeze_param_value(obj["params"], "H0", float(target_h0))

    opt = cfg["optimizer"]
    minimize = obj["sampler"]["minimize"]
    minimize["seed"] = int(opt["seed_base"]) + int(profile_index)
    minimize["max_evals"] = int(opt["max_evals"])
    minimize["override_bobyqa"]["rhoend"] = float(opt["rhoend"])
    if base["models"][model].get("kind") == "ede":
        minimize["override_bobyqa"]["rhobeg"] = float(opt["ede_rhobeg"])

    tag = f"q006_{model}_h0_{target_h0:.1f}".replace(".", "p")
    obj["output"] = str((ROOT / cfg["paths"]["results"] / tag).resolve())
    return obj, refs, source_profile


def result_path(cfg: dict[str, Any], model: str, target_h0: float) -> Path:
    tag = f"q006_attribution_{model}_h0_{target_h0:.1f}".replace(".", "p")
    return ROOT / cfg["paths"]["results"] / f"{tag}.json"


def render(base: dict[str, Any], cfg: dict[str, Any], model: str, target_h0: float,
           profile_index: int) -> tuple[Path, dict[str, float], str]:
    obj, refs, source_profile = build_profile(base, cfg, model, target_h0, profile_index)
    d = ROOT / cfg["paths"]["rendered"]
    d.mkdir(parents=True, exist_ok=True)
    p = d / (f"q006_{model}_h0_{target_h0:.1f}.yaml".replace(".", "p"))
    p.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
    return p, refs, source_profile


def collect(base: dict[str, Any], cfg: dict[str, Any], model: str, target_h0: float,
            profile_index: int, rendered: Path, refs: dict[str, float], source_profile: str,
            exit_code: int) -> dict[str, Any]:
    out: dict[str, Any] = {
        "q": "Q-006",
        "run_id": cfg["project"]["run_id"],
        "result_class": "FIXED_H0_PROFILE_COMPONENT_ATTRIBUTION",
        "model": model,
        "target_h0": float(target_h0),
        "profile_index": int(profile_index),
        "parent_q": "Q-005",
        "parent_backend_project": cfg["parent"]["base_project"],
        "parent_recovery_project": cfg["parent"]["recovery_project"],
        "source_profile": source_profile,
        "start_reference": refs,
        "start_reference_sha256": canonical_hash(refs),
        "rendered_yaml": str(rendered),
        "rendered_yaml_sha256": core.sha256_file(rendered),
        "cobaya_exit": int(exit_code),
        "status": "FAIL",
        "claim_boundary": cfg["claim_boundary"],
        "sources": cfg["sources"],
    }
    prefix = Path(yaml.safe_load(rendered.read_text())["output"])
    one = core.find_onepoint(prefix)
    if exit_code == 0 and one is not None:
        parsed = core.parse_onepoint(one, base)
        required = set(base["likelihood_accounting"]["required_nonlocal"])
        finite_ok, reason = core.finite_scientific_point(parsed, required)
        out["bestfit"] = parsed
        out["finite_scientific_gate"] = finite_ok
        if finite_ok:
            out["chi2_components"] = {k: float(parsed["chi2_nonoverlap"][k]) for k in sorted(required)}
            out["chi2_scientific_total"] = sum(out["chi2_components"].values())
            out["status"] = "PASS"
        else:
            out["reason"] = reason
    else:
        out["reason"] = f"COBAYA_EXIT_{exit_code}" if exit_code else "NO_ONEPOINT_RESULT"

    p = result_path(cfg, model, target_h0)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def run_one(cfg: dict[str, Any], model: str, target_h0: float, profile_index: int) -> int:
    if cfg["project"]["q"] != "Q-006":
        raise RuntimeError("Q_IDENTITY_GATE = FAIL")
    base = core.load_cfg(cfg["parent"]["base_config"])
    if base["project"]["q"] != "Q-005":
        raise RuntimeError("PARENT_Q_IDENTITY_GATE = FAIL")
    pf = core.preflight(base)
    if pf["status"] != "PASS":
        print(json.dumps({"q": "Q-006", "status": "FAIL", "gate": "ENVIRONMENT_GATE", "parent_preflight": pf}, indent=2))
        return 5
    rendered, refs, source_profile = render(base, cfg, model, target_h0, profile_index)
    rc = core.cobaya_run(rendered, base)
    print(json.dumps(collect(base, cfg, model, target_h0, profile_index, rendered, refs, source_profile, rc), indent=2))
    return 0


def find_results(root: Path) -> list[Path]:
    return sorted(root.rglob("q006_attribution_*.json"))


def aggregate(cfg: dict[str, Any], artifacts_root: str, output: str) -> dict[str, Any]:
    root = ROOT / artifacts_root
    rows: list[dict[str, Any]] = []
    for p in find_results(root):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if d.get("q") == "Q-006" and d.get("run_id") == cfg["project"]["run_id"]:
            rows.append(d)

    expected = {(x["model"], float(x["target_h0"])) for x in profile_specs(cfg)}
    got = {(r.get("model"), float(r.get("target_h0"))) for r in rows}
    missing = sorted(expected - got)
    out: dict[str, Any] = {
        "q": "Q-006",
        "run_id": cfg["project"]["run_id"],
        "result_class": "LIKELIHOOD_COMPONENT_ATTRIBUTION_AGGREGATE",
        "status": "UNRESOLVED",
        "models": {},
        "gates": {},
        "missing_profiles": [{"model": m, "target_h0": h} for m, h in missing],
        "sources": cfg["sources"],
        "claim_boundary": cfg["claim_boundary"],
    }
    complete = not missing and all(r.get("status") == "PASS" for r in rows)
    out["gates"]["JOB_COMPLETENESS_GATE"] = "PASS" if complete else "FAIL"

    for model, mcfg in cfg["models"].items():
        mr = sorted([r for r in rows if r.get("model") == model and r.get("status") == "PASS"], key=lambda x: float(x["target_h0"]))
        baseline_h0 = float(mcfg["baseline_h0"])
        base_row = next((r for r in mr if abs(float(r["target_h0"]) - baseline_h0) < 1e-9), None)
        if base_row is None:
            out["models"][model] = {"status": "NO_BASELINE"}
            continue
        base_comp = base_row["chi2_components"]
        profiles = []
        for r in mr:
            deltas = {k: float(r["chi2_components"][k]) - float(base_comp[k]) for k in base_comp}
            profiles.append({
                "target_h0": r["target_h0"],
                "chi2_total": r["chi2_scientific_total"],
                "delta_chi2_total": float(r["chi2_scientific_total"]) - float(base_row["chi2_scientific_total"]),
                "delta_chi2_components": deltas,
                "dominant_penalty_component": max(deltas, key=deltas.get),
                "bestfit": r.get("bestfit", {}),
            })
        high = [p for p in profiles if float(p["target_h0"]) >= float(cfg["gates"]["high_h0_threshold"])]
        dominant_counts: dict[str, int] = {}
        for p in high:
            k = p["dominant_penalty_component"]
            dominant_counts[k] = dominant_counts.get(k, 0) + 1
        out["models"][model] = {
            "status": "ATTRIBUTED" if high else "NO_HIGH_H0_PROFILE",
            "baseline_h0": baseline_h0,
            "profiles": profiles,
            "dominant_component_across_high_h0": max(dominant_counts, key=dominant_counts.get) if dominant_counts else None,
            "dominant_counts": dominant_counts,
        }

    attributed = complete and all(v.get("status") == "ATTRIBUTED" for v in out["models"].values())
    out["gates"]["COMPONENT_ATTRIBUTION_GATE"] = "PASS" if attributed else "UNRESOLVED"
    out["gates"]["FINAL_RESULT_GATE"] = "PASS" if attributed else "UNRESOLVED"
    out["status"] = "PASS" if attributed else "UNRESOLVED"
    out["next_required_action"] = (
        "Return component penalties and profiled parameter shifts to Result Ingestion & Routing. "
        "If one component dominates consistently, route the next Q to a targeted Reality Test/Anomaly/Model Integration investigation; "
        "if penalties are distributed, record a multi-dataset barrier."
    )
    op = ROOT / output
    op.parent.mkdir(parents=True, exist_ok=True)
    op.write_text(json.dumps(out, indent=2) + "\n")
    return out


def preflight(cfg: dict[str, Any]) -> int:
    base = core.load_cfg(cfg["parent"]["base_config"])
    checks = {
        "q_identity": cfg["project"]["q"] == "Q-006",
        "parent_q": base["project"]["q"] == "Q-005",
        "base_engine_exists": (ROOT / cfg["parent"]["base_engine"]).exists(),
        "recovery_config_exists": (ROOT / cfg["parent"]["recovery_config"]).exists(),
        "models": set(cfg["models"]) == {"ede_n3", "me_common"},
        "high_h0_gate": float(cfg["gates"]["high_h0_threshold"]) == 71.5,
    }
    d = {"q": "Q-006", "run_id": cfg["project"]["run_id"], "checks": checks, "status": "PASS" if all(checks.values()) else "FAIL"}
    print(json.dumps(d, indent=2))
    return 0 if d["status"] == "PASS" else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight")
    pplan = sub.add_parser("plan"); pplan.add_argument("--json", action="store_true")
    prun = sub.add_parser("run"); prun.add_argument("--model", required=True); prun.add_argument("--target-h0", type=float, required=True); prun.add_argument("--profile-index", type=int, required=True)
    pagg = sub.add_parser("aggregate"); pagg.add_argument("--artifacts-root", required=True); pagg.add_argument("--output", required=True)
    a = ap.parse_args(); cfg = load_cfg(a.config)
    if a.cmd == "preflight": return preflight(cfg)
    if a.cmd == "plan":
        d = plan(cfg); print(json.dumps(d, separators=(",", ":")) if a.json else json.dumps(d, indent=2)); return 0
    if a.cmd == "run": return run_one(cfg, a.model, a.target_h0, a.profile_index)
    if a.cmd == "aggregate": print(json.dumps(aggregate(cfg, a.artifacts_root, a.output), indent=2)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
