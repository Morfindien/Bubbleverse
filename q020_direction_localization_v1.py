#!/usr/bin/env python3
"""
Bubbleverse Q020 — multidimensional Planck cross-profile direction localization V1.

Scientific contract
-------------------
CURRENT Q: Q020

This program localizes the Q019 asymmetric cross-profile geometry without:
- summing objectives across lite/full-MF likelihood constructions;
- treating Shapley/group diagnostics as independent physical chi2 components;
- converting nuisance sensitivity into a causal instrumental systematic;
- converting cosmological sensitivity into evidence for new physics;
- using the Q018 architecture gap as an additive physical component.

Method
------
Use the exact Q019 V1 free-optimum cosmologies that generated the preserved
cross-profile costs. Partition their shared sampled cosmology into four coupled
blocks and evaluate all 2^4 hybrid vertices separately under:
  - Q016 matched/CamSpec-lite
  - Q017 full-multifrequency CamSpec

At every vertex cosmology is frozen and the architecture-native nuisance
parameters are reprofiled. Two deterministic nuisance starts protect against
simple local-minimum artifacts.

Signed Shapley values and pair interactions are FUNCTIONAL GEOMETRY
DIAGNOSTICS within one likelihood surface. They are not independent chi2
measurements and must not be summed across likelihood constructions.
"""
from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q020"
RUN = "Q020-PLANCK-CROSS-PROFILE-DIRECTION-V1"
RESULT = "R-Q020-EDE-PLANCK-CROSS-PROFILE-DIRECTION-001"
ARCHITECTURES = ("lite", "full_mf")
GROUP_ORDER = ("ede_timing", "primordial", "matter", "h0")
ALL_MASK = (1 << len(GROUP_ORDER)) - 1

def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False

def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                 encoding="utf-8")
    os.replace(t, p)

def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if c["rules"]["no_cross_chain_chi2_sum"] is not True:
        raise RuntimeError("NO_CROSS_CHAIN_CHI2_SUM_GATE=FAIL")
    if c["rules"]["q018_architecture_gap_not_physical_component"] is not True:
        raise RuntimeError("Q018_GAP_NONPHYSICAL_GATE=FAIL")
    groups = c["direction"]["groups"]
    if tuple(groups) != GROUP_ORDER:
        raise RuntimeError("GROUP_IDENTITY_GATE=FAIL")
    flat = [p for g in GROUP_ORDER for p in groups[g]]
    if sorted(flat) != sorted(c["direction"]["sampled_cosmology"]):
        raise RuntimeError("GROUP_COVERAGE_GATE=FAIL")
    return c

def load_source_lock(c: Mapping[str, Any]) -> dict[str, Any]:
    d = json.loads((ROOT / c["provenance"]["source_lock"]).read_text())
    if d.get("q") != Q or d.get("run_id") != RUN:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    return d

def endpoint(c: Mapping[str, Any], name: str) -> dict[str, float]:
    return {str(k): float(v) for k, v in c["endpoints"][name]["cosmology"].items()}

def hybrid_cosmology(c: Mapping[str, Any], mask: int) -> dict[str, float]:
    """
    mask bit 0 => parameter block from Q019 V1 full-MF optimum
    mask bit 1 => parameter block from Q019 V1 lite optimum
    """
    if mask < 0 or mask > ALL_MASK:
        raise RuntimeError("MASK_GATE=FAIL")
    full = endpoint(c, "full_mf_v1")
    lite = endpoint(c, "lite_v1")
    out = dict(full)
    for i, group in enumerate(GROUP_ORDER):
        src = lite if (mask & (1 << i)) else full
        for name in c["direction"]["groups"][group]:
            out[name] = float(src[name])
    return out

def architecture_seed(c: Mapping[str, Any], architecture: str) -> dict[str, float]:
    key = "lite_v1" if architecture == "lite" else "full_mf_v1"
    seed = endpoint(c, key)
    seed.update({str(k): float(v) for k, v in c["endpoints"][key]["nuisance"].items()})
    return seed

def freeze_cosmology(info: dict[str, Any], cosmology: Mapping[str, float],
                     c: Mapping[str, Any]) -> None:
    params = info["params"]
    required = list(c["direction"]["sampled_cosmology"])
    missing = [k for k in required if k not in params]
    if missing:
        raise RuntimeError("COSMOLOGY_PARAMETER_GATE=FAIL " + repr(missing))
    for name in required:
        params[name] = float(cosmology[name])

def build_info(c: Mapping[str, Any], architecture: str, mask: int,
               restart: int, prefix: Path) -> tuple[dict[str, Any], dict[str, float]]:
    import q019_planck_cosmology_reprofile_v1 as q19
    parent = q19.load_cfg(ROOT / c["parents"]["q019_v1"]["config"])
    cosmology = hybrid_cosmology(c, mask)
    seed = architecture_seed(c, architecture)

    if architecture == "lite":
        info = q19.build_lite(parent, "reference_free_h0", 0, prefix, seed)
    elif architecture == "full_mf":
        info = q19.build_full(parent, "reference_free_h0", 0, prefix, seed)
    else:
        raise RuntimeError("ARCHITECTURE_GATE=FAIL")

    freeze_cosmology(info, cosmology, c)

    # Preserve the Q019 objective. Only nuisance references are perturbed.
    nuisance = q19.architecture_nuisance(info)
    sign = (-1.0, 1.0)[int(restart)]
    scale = float(c["execution"]["nuisance_restart_scale"])
    for name in nuisance:
        spec = info["params"].get(name)
        if not q19.sampled(spec):
            continue
        base = seed.get(name, q19.ref_value(spec))
        if base is None:
            raise RuntimeError("NUISANCE_REFERENCE_GATE=FAIL " + name)
        dv = float(q19.JITTER.get(name, 0.0)) * scale * sign
        q19.set_ref(info["params"], name, float(base) + dv)

    m = info.setdefault("sampler", {}).setdefault("minimize", {})
    m["max_evals"] = int(c["execution"]["max_evals"])
    m["best_of"] = 1
    m.setdefault("override_bobyqa", {})["rhoend"] = float(c["execution"]["rhoend"])
    info["output"] = str(prefix.resolve())
    info["force"] = True
    return info, cosmology

def run_profile(c: Mapping[str, Any], architecture: str, mask: int,
                restart: int, output: str | Path) -> int:
    import q019_planck_cosmology_reprofile_v1 as q19
    prefix = Path(output).with_suffix("")
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "HYBRID_VERTEX_PROFILE",
        "architecture": architecture, "mask": int(mask), "restart": int(restart),
        "status": "FAILED", "actual_computed_result": False,
        "cross_chain_chi2_sum_allowed": False,
        "physical_additive_component_interpretation_allowed": False,
    }
    sampler = None
    try:
        info, cosmology = build_info(c, architecture, mask, restart, prefix)
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
            "cosmology": cosmology,
            "nuisance": q19.serial_nuisance(row, nuisance_names),
            "minimum": row,
            "harvested_minimum_path": source,
            "objective_basis":
                "LIKELIHOOD_CHI2_PLUS_EXPLICIT_NORMALIZATION_FREE_SHARED_GAUSSIAN_SHAPES",
        })
    except Exception as exc:
        rec.update({"failure_class": "NUMERICAL_OR_LIKELIHOOD", "error": repr(exc)})
    finally:
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2

def collect(input_dir: str | Path) -> list[dict[str, Any]]:
    rows = []
    for p in Path(input_dir).rglob("*.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == "HYBRID_VERTEX_PROFILE":
            rows.append(d)
    return rows

def popcount(x: int) -> int:
    return int(x).bit_count()

def shapley(values: Mapping[int, float]) -> dict[str, float]:
    """Exact 4-group Shapley change from mask 0 (full cosmology) to mask 15 (lite)."""
    import math as _m
    n = len(GROUP_ORDER)
    out = {}
    for i, group in enumerate(GROUP_ORDER):
        bit = 1 << i
        s = 0.0
        for mask in range(1 << n):
            if mask & bit:
                continue
            k = popcount(mask)
            w = _m.factorial(k) * _m.factorial(n-k-1) / _m.factorial(n)
            s += w * (values[mask | bit] - values[mask])
        out[group] = float(s)
    return out

def pair_interactions(values: Mapping[int, float]) -> dict[str, float]:
    """
    Exact second-order finite interaction averaged over the remaining two groups.
    Diagnostic only: not an independent physical chi2 decomposition.
    """
    n = len(GROUP_ORDER)
    out = {}
    for i in range(n):
        for j in range(i+1, n):
            bi, bj = 1 << i, 1 << j
            rem = [k for k in range(n) if k not in (i, j)]
            acc = []
            for choices in range(1 << len(rem)):
                m = 0
                for rix, k in enumerate(rem):
                    if choices & (1 << rix):
                        m |= 1 << k
                acc.append(values[m|bi|bj] - values[m|bi] - values[m|bj] + values[m])
            out[f"{GROUP_ORDER[i]}__x__{GROUP_ORDER[j]}"] = float(sum(acc) / len(acc))
    return out

def aggregate(c: Mapping[str, Any], input_dir: str | Path, output: str | Path) -> int:
    rows = collect(input_dir)
    expected = {(a, m, r) for a in ARCHITECTURES for m in range(16) for r in (0,1)}
    got = {(r["architecture"], int(r["mask"]), int(r["restart"])) for r in rows}
    complete = [r for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]

    by = {}
    stability = {}
    best_rows = {}
    for a in ARCHITECTURES:
        vals = {}
        stab = {}
        for m in range(16):
            rr = sorted(
                [r for r in complete if r["architecture"] == a and int(r["mask"]) == m],
                key=lambda x: float(x["objective_chi2"])
            )
            if rr:
                vals[m] = float(rr[0]["objective_chi2"])
                best_rows[str(m)] = rr[0]
            if len(rr) == 2:
                stab[m] = float(rr[1]["objective_chi2"]) - float(rr[0]["objective_chi2"])
            else:
                stab[m] = None
        by[a] = vals
        stability[a] = stab

    complete_grid = all(len(by[a]) == 16 for a in ARCHITECTURES)
    diagnostics = {}
    if complete_grid:
        for a in ARCHITECTURES:
            vals = by[a]
            sv = shapley(vals)
            total = vals[15] - vals[0]  # full cosmology -> lite cosmology
            abs_total = sum(abs(v) for v in sv.values())
            diagnostics[a] = {
                "objective_at_full_cosmology_mask0": vals[0],
                "objective_at_lite_cosmology_mask15": vals[15],
                "signed_full_to_lite_objective_change": total,
                "own_endpoint_cross_cost": (
                    vals[0] - vals[15] if a == "lite" else vals[15] - vals[0]
                ),
                "shapley_signed_objective_change": sv,
                "shapley_abs_fraction": {
                    k: (abs(v) / abs_total if abs_total else 0.0) for k, v in sv.items()
                },
                "pair_interactions": pair_interactions(vals),
                "interpretation":
                    "FUNCTIONAL_GEOMETRY_DIAGNOSTIC_NONINDEPENDENT_NONCAUSAL",
            }

    tol = float(c["validation"]["cross_cost_abs_tolerance"])
    stab_tol = float(c["validation"]["restart_delta_objective_max"])
    gates = {
        "Q_IDENTITY_GATE": True,
        "MODEL_IDENTITY_GATE": True,
        "JOB_COMPLETENESS_GATE": got == expected and len(complete) == len(expected),
        "FINITE_RESULT_GATE": len(complete) == len(expected),
        "VERTEX_GRID_COMPLETENESS_GATE": complete_grid,
        "NUISANCE_RESTART_STABILITY_GATE": (
            complete_grid and all(
                stability[a][m] is not None and stability[a][m] <= stab_tol
                for a in ARCHITECTURES for m in range(16)
            )
        ),
        "NO_CROSS_CHAIN_CHI2_SUM_GATE": c["rules"]["no_cross_chain_chi2_sum"] is True,
        "Q018_GAP_NONPHYSICAL_GATE":
            c["rules"]["q018_architecture_gap_not_physical_component"] is True,
        "Q017_CAUSAL_STATUS_PRESERVED_GATE":
            c["rules"]["q017_causal_status_preserved"] == "INDETERMINATE",
        "INTERPRETATION_SAFETY_GATE":
            c["rules"]["causal_systematic_claim_allowed"] is False
            and c["rules"]["new_physics_claim_allowed"] is False,
    }
    if complete_grid:
        gates["Q019_CROSS_FULL_MF_REPRODUCTION_GATE"] = (
            abs(diagnostics["full_mf"]["own_endpoint_cross_cost"]
                - float(c["references"]["q019_cross_full_mf"])) <= tol
        )
        gates["Q019_CROSS_LITE_REPRODUCTION_GATE"] = (
            abs(diagnostics["lite"]["own_endpoint_cross_cost"]
                - float(c["references"]["q019_cross_lite"])) <= tol
        )
    else:
        gates["Q019_CROSS_FULL_MF_REPRODUCTION_GATE"] = False
        gates["Q019_CROSS_LITE_REPRODUCTION_GATE"] = False

    final = all(gates.values())
    classification = "UNRESOLVED"
    localization = {}
    if final:
        full_sv = diagnostics["full_mf"]["shapley_signed_objective_change"]
        ranked = sorted(full_sv, key=lambda k: abs(full_sv[k]), reverse=True)
        top = ranked[0]
        frac = diagnostics["full_mf"]["shapley_abs_fraction"][top]
        localization = {
            "ranked_full_mf_groups": ranked,
            "dominant_group": top,
            "dominant_abs_shapley_fraction": frac,
            "dominance_threshold": float(c["validation"]["dominant_abs_fraction_threshold"]),
        }
        if frac >= localization["dominance_threshold"]:
            classification = "LIMITED MULTIDIMENSIONAL DIRECTION LOCALIZED"
        else:
            classification = "DISTRIBUTED / COUPLED MULTIDIMENSIONAL RESPONSE"

    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "Q020_FINAL",
        "status": "PASS" if final else "FAIL",
        "FINAL_RESULT_GATE": "PASS" if final else "FAIL",
        "classification": classification,
        "gates": gates,
        "diagnostics": diagnostics,
        "localization": localization,
        "stability": stability,
        "rules": {
            "cross_chain_chi2_sum_performed": False,
            "q018_architecture_gap_used_as_physical_component": False,
            "shapley_values_are_independent_chi2_components": False,
            "causal_systematic_claim": False,
            "new_physics_claim": False,
        },
        "unresolved_issues": [
            "A localized functional direction is not by itself a causal physical or instrumental mechanism.",
            "Likelihood/data-vector/covariance architecture may still create or rotate the localized direction."
        ] if final else ["Mandatory Q020 execution/validation gates did not all pass."],
    }
    write_json(output, out)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if final else 2

def plan(c: Mapping[str, Any], output: str | Path) -> int:
    full = endpoint(c, "full_mf_v3")
    lite = endpoint(c, "lite_v1")
    scales = {str(k): float(v) for k, v in c["direction"]["screening_scales"].items()}
    rows = {}
    for k in c["direction"]["sampled_cosmology"]:
        d = lite[k] - full[k]
        rows[k] = {"lite_minus_full_v3": d, "in_q019_restart_scale_units": d / scales[k]}
    write_json(output, {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "SERIALIZED_DIRECTION_SCREEN",
        "status": "COMPLETE",
        "actual_likelihood_evaluation": False,
        "diagnostic_only": True,
        "displacements": rows,
    })
    return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("plan")
    p.add_argument("--output", required=True)

    p = sp.add_parser("profile")
    p.add_argument("--architecture", choices=ARCHITECTURES, required=True)
    p.add_argument("--mask", type=int, required=True)
    p.add_argument("--restart", type=int, choices=(0,1), required=True)
    p.add_argument("--output", required=True)

    p = sp.add_parser("aggregate")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_cfg(a.config)
    load_source_lock(c)

    if a.cmd == "plan":
        return plan(c, a.output)
    if a.cmd == "profile":
        return run_profile(c, a.architecture, a.mask, a.restart, a.output)
    return aggregate(c, a.input_dir, a.output)

if __name__ == "__main__":
    raise SystemExit(main())
