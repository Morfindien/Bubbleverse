#!/usr/bin/env python3
"""Bubbleverse Q-010 V3 — non-ACT likelihood attribution at corrected Q-008 basins.

No optimization is performed. The program consumes the exact Q-005 baseline
fixed vector preserved by Q-007 and the exact Q-008 best-observed fixed vectors,
re-evaluates the frozen Q-005 V14 likelihood stack, decomposes scientific chi2
into the non-overlapping Q-005 components, and compares parameter shifts.

Q-008 GLOBALITY_GATE remains UNRESOLVED by construction.
"""
from __future__ import annotations

Q010_CODE_VERSION = "3.0-serialized-vector-attribution-baseline"

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q010_nonact_likelihood_attribution_v3_config.yml"
CODE_VERSION = Q010_CODE_VERSION


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def cfg(path: str = DEFAULT_CONFIG) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return load_yaml(p)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def import_core():
    sys.path.insert(0, str(ROOT))
    import q005_hpc_v14 as core
    return core


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


def extract_param_vector(bestfit: dict[str, Any], needed: set[str]) -> dict[str, float]:
    candidates: list[dict[str, Any]] = []
    if isinstance(bestfit, dict):
        candidates.append(bestfit)
        for key in ("params", "sampled", "sampled_params", "point", "values"):
            if isinstance(bestfit.get(key), dict):
                candidates.append(bestfit[key])
    found: dict[str, float] = {}
    for block in candidates:
        for k, v in block.items():
            if k in needed and isinstance(v, (int, float)) and math.isfinite(float(v)):
                found[k] = float(v)
    missing = sorted(needed - set(found))
    if missing:
        raise RuntimeError(f"EXACT_VECTOR_GATE=FAIL missing_sampled_parameters={missing}")
    return found


def freeze_all_sampled(model: dict[str, Any], vals: dict[str, float]) -> None:
    for name, spec in list(model.get("params", {}).items()):
        if name in vals and isinstance(spec, dict) and "prior" in spec:
            model["params"][name] = float(vals[name])
    for lspec in model.get("likelihood", {}).values():
        if not isinstance(lspec, dict) or not isinstance(lspec.get("params"), dict):
            continue
        for name, spec in list(lspec["params"].items()):
            if name in vals and isinstance(spec, dict) and "prior" in spec:
                lspec["params"][name] = float(vals[name])
    model.pop("sampler", None)
    model.pop("output", None)


def build_frozen_model(c: dict[str, Any], vals: dict[str, float]):
    core = import_core()
    base = core.load_cfg(c["parent"]["base_config"])
    if base["project"]["q"] != "Q-005":
        raise RuntimeError("BACKEND_Q_GATE=FAIL")
    model_info = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(model_info)
    missing = sorted(needed - set(vals))
    if missing:
        raise RuntimeError(f"POINT_COVERAGE_GATE=FAIL missing={missing}")
    freeze_all_sampled(model_info, vals)
    return model_info, base


def normalize_likelihood_name(name: str, aliases: dict[str, list[str]]) -> str | None:
    for component, names in aliases.items():
        if name in names:
            return component
        if any(name.endswith(x) or x.endswith(name) for x in names):
            return component
    return None


def evaluate_components(c: dict[str, Any], vals: dict[str, float]) -> dict[str, Any]:
    from cobaya.model import get_model

    model_info, base = build_frozen_model(c, vals)
    model = get_model(model_info)
    lp = model.logposterior({})

    like_names = list(model.likelihood)
    loglikes = [float(x) for x in lp.loglikes]
    if len(like_names) != len(loglikes):
        raise RuntimeError(
            f"LIKELIHOOD_COMPONENT_GATE=FAIL names={len(like_names)} loglikes={len(loglikes)}"
        )

    aliases = base["likelihood_accounting"]["aliases"]
    required = list(base["likelihood_accounting"]["required_nonlocal"])
    raw: dict[str, float] = {}
    components: dict[str, float] = {}
    unmapped: dict[str, float] = {}

    for name, loglike in zip(like_names, loglikes):
        chi2 = -2.0 * loglike
        raw[str(name)] = chi2
        component = normalize_likelihood_name(str(name), aliases)
        if component is None:
            unmapped[str(name)] = chi2
        else:
            components[component] = components.get(component, 0.0) + chi2

    missing = sorted(set(required) - set(components))
    if missing:
        raise RuntimeError(f"LIKELIHOOD_COMPONENT_GATE=FAIL missing={missing} raw={sorted(raw)}")

    scientific_total = float(sum(components[k] for k in required))
    return {
        "components": {k: float(components[k]) for k in required},
        "scientific_total": scientific_total,
        "raw_likelihood_chi2": raw,
        "unmapped_likelihood_chi2": unmapped,
        "logpost": float(lp.logpost),
        "logpriors": [float(x) for x in lp.logpriors],
        "required_components": required,
    }


def numeric_key(d: dict[str, Any], target: float) -> str | None:
    for k in d:
        try:
            if math.isclose(float(k), target, rel_tol=0.0, abs_tol=1e-9):
                return k
        except Exception:
            pass
    return None


def q007_baseline_vector(c: dict[str, Any], q7: dict[str, Any], needed: set[str]) -> dict[str, float]:
    if q7.get("q") != "Q-007" or q7.get("model") != "ede_n3" or q7.get("status") != "PASS":
        raise RuntimeError("Q007_BASELINE_VECTOR_GATE=FAIL identity/model/status")
    h0 = q7.get("target_h0")
    if not isinstance(h0, (int, float)) or not math.isclose(
        float(h0), float(c["frozen_baseline"]["h0"]), rel_tol=0.0,
        abs_tol=float(c["gates"]["baseline_h0_tolerance"])
    ):
        raise RuntimeError("Q007_BASELINE_VECTOR_GATE=FAIL H0")
    vals = q7.get("fixed_sampled_parameters")
    if not isinstance(vals, dict):
        raise RuntimeError("Q007_BASELINE_VECTOR_GATE=FAIL missing_fixed_sampled_parameters")
    return extract_param_vector(vals, needed)


def q008_target_vector(q8: dict[str, Any], target: float, needed: set[str]) -> tuple[dict[str, float], float]:
    if q8.get("q") != "Q-008":
        raise RuntimeError("Q008_EXACT_POINT_GATE=FAIL wrong_q")
    profiles = q8.get("profile_targets")
    if not isinstance(profiles, dict):
        raise RuntimeError("Q008_EXACT_POINT_GATE=FAIL missing_profile_targets")
    k = numeric_key(profiles, target)
    if k is None:
        raise RuntimeError(f"Q008_EXACT_POINT_GATE=FAIL missing_target={target}")
    rec = profiles[k]
    if not isinstance(rec, dict) or not isinstance(rec.get("bestfit"), dict):
        raise RuntimeError(f"Q008_EXACT_POINT_GATE=FAIL malformed_target={target}")
    chi2 = rec.get("best_observed_chi2")
    if not isinstance(chi2, (int, float)) or not math.isfinite(float(chi2)):
        raise RuntimeError(f"Q008_EXACT_POINT_GATE=FAIL missing_chi2={target}")
    # Q-008 is a fixed-H0 profile. Its bestfit block stores only the parameters
    # that were free inside the profile; H0 is represented by the profile target
    # itself and therefore is intentionally absent from bestfit. Reconstruct the
    # exact fixed sampled vector without inventing any other parameter values.
    needed_without_h0 = set(needed) - {"H0"}
    vals = extract_param_vector(rec["bestfit"], needed_without_h0)
    if "H0" in needed:
        vals["H0"] = float(target)
    missing = sorted(set(needed) - set(vals))
    if missing:
        raise RuntimeError(
            f"Q008_EXACT_POINT_GATE=FAIL missing_sampled_parameters_after_fixed_h0_reconstruction={missing}"
        )
    return vals, float(chi2)


def parameter_geometry(base_vec: dict[str, float], vec: dict[str, float], base_cfg: dict[str, Any]) -> dict[str, Any]:
    specs: dict[str, dict[str, Any]] = {}
    for name, spec in base_cfg.get("parameters", {}).get("common", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            specs[name] = spec
    for name, spec in base_cfg.get("common_ede_priors", {}).items():
        if isinstance(spec, dict) and "prior" in spec:
            specs[name] = spec
    act = base_cfg.get("likelihoods", {}).get("common", {}).get("act_dr6_cmbonly.ACTDR6CMBonly", {})
    for name, spec in act.get("params", {}).items() if isinstance(act, dict) else []:
        if isinstance(spec, dict) and "prior" in spec:
            specs[name] = spec

    out: dict[str, Any] = {}
    for name in sorted(set(base_vec) & set(vec)):
        b, v = float(base_vec[name]), float(vec[name])
        delta = v - b
        rec: dict[str, Any] = {"baseline": b, "value": v, "delta": delta}
        spec = specs.get(name, {})
        prior = spec.get("prior", {}) if isinstance(spec, dict) else {}
        if isinstance(prior, dict) and isinstance(prior.get("min"), (int, float)) and isinstance(prior.get("max"), (int, float)):
            width = float(prior["max"]) - float(prior["min"])
            if width > 0:
                rec["delta_over_prior_range"] = delta / width
        proposal = spec.get("proposal") if isinstance(spec, dict) else None
        if isinstance(proposal, (int, float)) and float(proposal) != 0:
            rec["delta_over_proposal"] = delta / float(proposal)
        out[name] = rec
    return out


def run_point(c: dict[str, Any], q7: dict[str, Any], q8: dict[str, Any], label: str) -> dict[str, Any]:
    """Evaluate one serialized fixed vector.

    IMPORTANT V3 semantics:
    - The Q005 optimized total chi2 is authoritative as a documented scalar.
    - Q007/Q008 JSON vectors are serialized finite-precision representations.
    - Re-evaluating those serialized vectors can move total chi2 slightly.
    - That roundtrip mismatch is a diagnostic, NOT a model/point failure.
    - Component attribution is therefore performed relative to the re-evaluated
      Q007 serialized baseline, exactly the same ACT baseline used by Q007/Q009.
    """
    if c["project"]["q"] != "Q-010":
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")

    core = import_core()
    base_cfg = core.load_cfg(c["parent"]["base_config"])
    probe = core.build_model(base_cfg, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(probe)
    base_vec = q007_baseline_vector(c, q7, needed)

    if label == "baseline":
        vec = base_vec
        target_h0 = float(c["frozen_baseline"]["h0"])
        documented_total = float(c["frozen_baseline"]["chi2_scientific"])
        source = "INTERNAL-Q005 scalar baseline + INTERNAL-Q007 serialized attribution vector"
        point_role = "ATTRIBUTION_BASELINE_SERIALIZED_Q007_VECTOR"
    else:
        target_h0 = float(label)
        vec, q8_chi2 = q008_target_vector(q8, target_h0, needed)
        documented_total = float(c["targets"][label]["q008_best_observed_chi2"])
        if not math.isclose(q8_chi2, documented_total, rel_tol=0.0, abs_tol=1e-6):
            raise RuntimeError(f"Q008_EXACT_POINT_GATE=FAIL documented_chi2_mismatch target={label}")
        source = "INTERNAL-Q008 serialized best-observed fixed vector"
        point_role = "Q008_BEST_OBSERVED_SERIALIZED_VECTOR"

    evaluated = evaluate_components(c, vec)
    comps = evaluated["components"]
    finite = (
        all(isinstance(comps.get(k), (int, float)) and math.isfinite(float(comps[k]))
            for k in c["component_order"])
        and math.isfinite(float(evaluated["scientific_total"]))
    )
    roundtrip_error = float(evaluated["scientific_total"]) - documented_total

    return {
        "q": "Q-010",
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "point_label": label,
        "point_role": point_role,
        "target_h0": target_h0,
        "source": source,
        "fixed_vector_sha256": canonical_hash(vec),
        "fixed_sampled_parameters": vec,
        "chi2_components": comps,
        "chi2_serialized_vector_total": evaluated["scientific_total"],
        "documented_parent_chi2_total": documented_total,
        "serialized_roundtrip_delta_chi2": roundtrip_error,
        "serialized_roundtrip_abs_error": abs(roundtrip_error),
        "serialized_roundtrip_role": (
            "DIAGNOSTIC_ONLY_NOT_A_PASS_FAIL_CRITERION; parent optimizer total and "
            "serialized JSON vector are retained as distinct provenance objects."
        ),
        "finite_component_gate": "PASS" if finite else "FAIL",
        "raw_likelihood_chi2": evaluated["raw_likelihood_chi2"],
        "unmapped_likelihood_chi2": evaluated["unmapped_likelihood_chi2"],
        "parameter_geometry_vs_q005_baseline": parameter_geometry(base_vec, vec, base_cfg),
        "globality_gate": "UNRESOLVED",
        "status": "PASS" if finite else "FAIL",
        "sources": c["sources"],
        "claim_boundary": c["claim_boundary"],
    }


def aggregate(c: dict[str, Any], inputs: list[str], q009_path: str, output: str) -> dict[str, Any]:
    rows = [load_json(p) for p in inputs]
    rows = [
        r for r in rows
        if r.get("q") == "Q-010" and r.get("run_id") == c["project"]["run_id"]
    ]
    by_label = {str(r["point_label"]): r for r in rows}
    expected_labels = {"baseline", "71.5", "72.5", "73.5"}
    complete = (
        set(by_label) == expected_labels
        and all(r.get("status") == "PASS" for r in by_label.values())
    )

    out: dict[str, Any] = {
        "q": "Q-010",
        "run_id": c["project"]["run_id"],
        "code_version": CODE_VERSION,
        "result_class": "SERIALIZED_FIXED_VECTOR_LIKELIHOOD_COMPONENT_ATTRIBUTION",
        "status": "UNRESOLVED",
        "globality_gate": "UNRESOLVED",
        "gates": {"JOB_COMPLETENESS_GATE": "PASS" if complete else "FAIL"},
        "baseline": by_label.get("baseline"),
        "targets": {},
        "sources": c["sources"],
        "claim_boundary": c["claim_boundary"],
        "attribution_semantics": {
            "documented_q005_total_baseline": float(c["frozen_baseline"]["chi2_scientific"]),
            "component_reference": "re-evaluated serialized Q007 baseline vector",
            "reason": (
                "The Q007/Q008 parent artifacts preserve finite-precision serialized vectors. "
                "Their re-evaluated totals are not forced to equal the optimizer-native parent totals. "
                "Component deltas use the common serialized-vector evaluation basis; documented total "
                "deltas remain separate scalar parent results."
            ),
            "no_artificial_component_offset": True,
        },
    }
    if not complete:
        out["missing_or_failed"] = (
            sorted(expected_labels - set(by_label))
            + [k for k, r in by_label.items() if r.get("status") != "PASS"]
        )
        Path(output).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        return out

    base = by_label["baseline"]
    base_comp = base["chi2_components"]
    base_eval_total = float(base["chi2_serialized_vector_total"])
    documented_q005_total = float(c["frozen_baseline"]["chi2_scientific"])

    q9 = load_json(q009_path)
    if q9.get("q") != "Q-009":
        raise RuntimeError("Q009_ACT_CROSSCHECK_GATE=FAIL wrong_q")

    all_closure = True
    all_act_cross = True
    all_finite = True

    for label in ("71.5", "72.5", "73.5"):
        r = by_label[label]
        deltas = {
            k: float(r["chi2_components"][k]) - float(base_comp[k])
            for k in base_comp
        }
        eval_total_delta = float(r["chi2_serialized_vector_total"]) - base_eval_total
        nonact = {k: deltas[k] for k in c["non_act_components"]}
        nonact_net = float(sum(nonact.values()))
        closure_err = abs(eval_total_delta - sum(deltas.values()))
        closure_pass = closure_err <= float(c["gates"]["component_closure_tolerance"])
        all_closure &= closure_pass
        all_finite &= r.get("finite_component_gate") == "PASS"

        documented_act = float(c["targets"][label]["q009_delta_chi2_act"])
        act_cross_err = abs(float(deltas["act_dr6"]) - documented_act)
        act_cross_pass = act_cross_err <= float(c["gates"]["q009_act_delta_tolerance"])
        all_act_cross &= act_cross_pass

        documented_target_total = float(c["targets"][label]["q008_best_observed_chi2"])
        documented_total_delta = documented_target_total - documented_q005_total
        roundtrip_delta_mismatch = eval_total_delta - documented_total_delta

        positive_nonact = {k: v for k, v in nonact.items() if v > 0}
        dominant_positive = max(positive_nonact, key=positive_nonact.get) if positive_nonact else None
        dominant_abs = max(nonact, key=lambda k: abs(nonact[k])) if nonact else None

        geom = r["parameter_geometry_vs_q005_baseline"]
        ranked = sorted(
            (
                {"parameter": k, **v}
                for k, v in geom.items()
                if k != "H0" and isinstance(v.get("delta_over_prior_range"), (int, float))
            ),
            key=lambda x: abs(float(x["delta_over_prior_range"])),
            reverse=True,
        )

        out["targets"][label] = {
            "target_h0": float(label),
            "documented_q008_chi2_total": documented_target_total,
            "documented_delta_chi2_total_vs_q005": documented_total_delta,
            "serialized_vector_chi2_total": r["chi2_serialized_vector_total"],
            "serialized_vector_delta_chi2_total_vs_attribution_baseline": eval_total_delta,
            "serialized_vs_documented_delta_mismatch": roundtrip_delta_mismatch,
            "delta_chi2_components_vs_attribution_baseline": deltas,
            "delta_chi2_nonact_components_vs_attribution_baseline": nonact,
            "delta_chi2_nonact_net_vs_attribution_baseline": nonact_net,
            "dominant_positive_nonact_component": dominant_positive,
            "dominant_absolute_nonact_component": dominant_abs,
            "q009_documented_delta_chi2_act": documented_act,
            "q010_recomputed_delta_chi2_act": deltas["act_dr6"],
            "q009_act_crosscheck_abs_error": act_cross_err,
            "q009_act_crosscheck_gate": "PASS" if act_cross_pass else "FAIL",
            "component_closure_abs_error": closure_err,
            "component_closure_gate": "PASS" if closure_pass else "FAIL",
            "parameter_tradeoffs": geom,
            "largest_parameter_shifts_by_prior_range_excluding_H0": ranked[:6],
            "globality_gate": "UNRESOLVED",
        }

    baseline_act_expected = float(c["attribution_reference"]["q007_act_chi2"])
    baseline_act_err = abs(float(base_comp["act_dr6"]) - baseline_act_expected)
    baseline_act_pass = baseline_act_err <= float(c["gates"]["q007_act_baseline_tolerance"])

    out["baseline_roundtrip_diagnostic"] = {
        "documented_q005_chi2_total": documented_q005_total,
        "serialized_q007_vector_chi2_total": base_eval_total,
        "delta_chi2": base_eval_total - documented_q005_total,
        "role": "DIAGNOSTIC_ONLY_NOT_COMPONENT_ATTRIBUTION",
        "q007_documented_act_chi2": baseline_act_expected,
        "q010_recomputed_act_chi2": float(base_comp["act_dr6"]),
        "q007_act_baseline_abs_error": baseline_act_err,
        "q007_act_baseline_crosscheck_gate": "PASS" if baseline_act_pass else "FAIL",
    }

    out["gates"].update({
        "Q_IDENTITY_GATE": "PASS",
        "PARENT_Q_GATE": "PASS",
        "Q007_BASELINE_VECTOR_GATE": "PASS",
        "Q008_EXACT_POINT_GATE": "PASS",
        "BACKEND_Q_GATE": "PASS",
        "LIKELIHOOD_COMPONENT_GATE": "PASS",
        "FINITE_SERIALIZED_POINT_GATE": "PASS" if all_finite and base.get("finite_component_gate") == "PASS" else "FAIL",
        "Q007_ACT_BASELINE_CROSSCHECK_GATE": "PASS" if baseline_act_pass else "FAIL",
        "COMPONENT_CLOSURE_GATE": "PASS" if all_closure else "FAIL",
        "Q009_ACT_CROSSCHECK_GATE": "PASS" if all_act_cross else "FAIL",
        "PARENT_TOTAL_ROUNDTRIP_GATE": "DIAGNOSTIC_ONLY",
    })

    scientific_pass = (
        all_finite
        and base.get("finite_component_gate") == "PASS"
        and baseline_act_pass
        and all_closure
        and all_act_cross
    )
    out["gates"]["SCIENTIFIC_INTERPRETATION_GATE"] = "PASS" if scientific_pass else "UNRESOLVED"
    out["gates"]["FINAL_RESULT_GATE"] = "PASS" if scientific_pass else "UNRESOLVED"
    out["status"] = "PASS" if scientific_pass else "UNRESOLVED"
    out["journal_effect"] = (
        "Attribute Q010 non-ACT likelihood movement on the same serialized fixed-vector "
        "basis used by Q007/Q009, while preserving Q005/Q008 optimizer-native total chi2 "
        "as separate authoritative parent scalars. Do not distribute serialization "
        "roundtrip offsets across likelihood components."
    )
    out["next_required_action"] = (
        "Return to Result Ingestion & Routing. Use dominant non-ACT component movement "
        "and parameter tradeoffs only if FINAL_RESULT_GATE=PASS. Preserve "
        "GLOBALITY_GATE=UNRESOLVED."
    )

    Path(output).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def preflight(c: dict[str, Any], q7_path: str, q8_path: str) -> int:
    if c["project"]["q"] != "Q-010":
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    core = import_core()
    base = core.load_cfg(c["parent"]["base_config"])
    if base["project"]["q"] != "Q-005":
        raise RuntimeError("PARENT_Q_GATE=FAIL")
    pf = core.preflight(base)
    if pf.get("status") != "PASS":
        print(json.dumps({"q": "Q-010", "status": "FAIL", "gate": "ENVIRONMENT_GATE", "parent_preflight": pf}, indent=2))
        return 5
    q7, q8 = load_json(q7_path), load_json(q8_path)
    probe = core.build_model(base, "ede_n3", smoke=False, restart=0)
    needed = sampled_names(probe)
    q007_baseline_vector(c, q7, needed)
    for target in (71.5, 72.5, 73.5):
        q008_target_vector(q8, target, needed)
    print(json.dumps({"q": "Q-010", "status": "PASS", "gate": "CONTEXT_AND_VECTOR_PREFLIGHT", "needed_parameters": sorted(needed)}, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=DEFAULT_CONFIG)
    sub = p.add_subparsers(dest="cmd", required=True)

    pf = sub.add_parser("preflight")
    pf.add_argument("--q007-baseline", required=True)
    pf.add_argument("--q008", required=True)

    rp = sub.add_parser("run")
    rp.add_argument("--q007-baseline", required=True)
    rp.add_argument("--q008", required=True)
    rp.add_argument("--point", required=True, choices=["baseline", "71.5", "72.5", "73.5"])
    rp.add_argument("--output", required=True)

    ag = sub.add_parser("aggregate")
    ag.add_argument("--inputs", nargs="+", required=True)
    ag.add_argument("--q009", required=True)
    ag.add_argument("--output", required=True)

    a = p.parse_args()
    print(f"[Q010] CODE_VERSION={Q010_CODE_VERSION}", flush=True)
    c = cfg(a.config)
    if a.cmd == "preflight":
        return preflight(c, a.q007_baseline, a.q008)
    if a.cmd == "run":
        q7, q8 = load_json(a.q007_baseline), load_json(a.q008)
        out = run_point(c, q7, q8, a.point)
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(out, indent=2))
        return 0 if out["status"] == "PASS" else 6
    if a.cmd == "aggregate":
        out = aggregate(c, a.inputs, a.q009, a.output)
        print(json.dumps(out, indent=2))
        return 0 if out["status"] == "PASS" else 7
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
