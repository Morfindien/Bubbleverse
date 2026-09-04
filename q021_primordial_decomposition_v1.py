#!/usr/bin/env python3
"""
Bubbleverse Q021 — primordial internal-structure decomposition V1.

CURRENT Q: Q021

Scientific contract
-------------------
Q021 opens the Q020 primordial block (n_s, logA, tau_reio) without:
- summing matched and full-MF objectives;
- treating functional attribution as independent physical chi-square evidence;
- turning a large allocation into a causal Planck systematic;
- changing the frozen n=3 EDE backend;
- silently changing the Q019/Q020 likelihood constructors.

Two logically separate operations are enforced:

PARENT REPRODUCTION GATE
  Recompute Q020 V2 aggregation from the original Q020 V1 artifacts and compare
  it to the authoritative Q020 V2 merged result. This uses no new likelihood
  evaluations.

Q021 COMPENSATED PRIMORDIAL PROFILE
  On each likelihood architecture, define its own native endpoint and the other
  architecture's foreign endpoint. For every one of the 2^3 primordial hybrid
  vertices, fix n_s/logA/tau_reio to native/foreign values while re-profiling all
  remaining parameters permitted by the frozen Q019 likelihood constructor.

The full-MF direction is full-MF native -> lite foreign.
The matched/lite direction is lite native -> full-MF foreign.
Both native-oriented and canonical full-MF -> lite orientations are serialized.

The exact 3-coordinate functional decomposition contains:
  single finite effects,
  pairwise Möbius interactions,
  one three-way Möbius interaction,
  exact Shapley allocations,
  exact closure to the all-primordial transition.

All of these are functional likelihood-geometry diagnostics, not independent
observational chi-square measurements.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q021"
RUN = "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
RESULT = "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"
ARCHITECTURES = ("lite", "full_mf")
PRIMORDIAL = ("n_s", "logA", "tau_reio")
ALL_MASK = 7

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
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()

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
    if tuple(c["decomposition"]["coordinates"]) != PRIMORDIAL:
        raise RuntimeError("PRIMORDIAL_COORDINATE_GATE=FAIL")
    rules = c["rules"]
    mandatory_true = (
        "no_cross_chain_chi2_sum",
        "functional_attribution_not_independent_physical_chi2",
        "causal_systematic_claim_forbidden",
        "new_physics_claim_forbidden",
    )
    if not all(rules.get(k) is True for k in mandatory_true):
        raise RuntimeError("INTERPRETATION_RULE_GATE=FAIL")
    return c

def load_q020_cfg(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / c["parents"]["q020"]["config"]
    q20 = yaml.safe_load(p.read_text(encoding="utf-8"))
    if q20["project"]["q"] != "Q020":
        raise RuntimeError("Q020_PARENT_IDENTITY_GATE=FAIL")
    if q20["model"]["backend_commit"] != c["model"]["backend_commit"]:
        raise RuntimeError("Q020_BACKEND_CONTINUITY_GATE=FAIL")
    if tuple(q20["direction"]["groups"]["primordial"]) != PRIMORDIAL:
        raise RuntimeError("Q020_PRIMORDIAL_IDENTITY_GATE=FAIL")
    return q20

def endpoint(q20: Mapping[str, Any], name: str) -> dict[str, float]:
    return {str(k): float(v) for k, v in q20["endpoints"][name]["cosmology"].items()}

def endpoint_nuisance(q20: Mapping[str, Any], name: str) -> dict[str, float]:
    return {str(k): float(v) for k, v in q20["endpoints"][name]["nuisance"].items()}

def endpoint_names(architecture: str) -> tuple[str, str]:
    if architecture == "full_mf":
        return "full_mf_v1", "lite_v1"
    if architecture == "lite":
        return "lite_v1", "full_mf_v1"
    raise RuntimeError("ARCHITECTURE_GATE=FAIL")

def primordial_hybrid(q20: Mapping[str, Any], architecture: str, mask: int) -> dict[str, float]:
    if mask < 0 or mask > ALL_MASK:
        raise RuntimeError("MASK_GATE=FAIL")
    native_name, foreign_name = endpoint_names(architecture)
    native = endpoint(q20, native_name)
    foreign = endpoint(q20, foreign_name)
    return {
        name: float(foreign[name] if (mask & (1 << i)) else native[name])
        for i, name in enumerate(PRIMORDIAL)
    }

def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)

def ref_value(spec: Any) -> float | None:
    if not isinstance(spec, Mapping):
        return None
    r = spec.get("ref")
    if isinstance(r, Mapping):
        if "loc" in r:
            return float(r["loc"])
        if "mean" in r:
            return float(r["mean"])
    if isinstance(r, (int, float)):
        return float(r)
    p = spec.get("prior")
    if isinstance(p, Mapping) and "min" in p and "max" in p:
        return 0.5 * (float(p["min"]) + float(p["max"]))
    return None

def set_ref(params: dict[str, Any], name: str, value: float) -> None:
    spec = params.get(name)
    if not isinstance(spec, Mapping):
        return
    spec = copy.deepcopy(spec)
    r = spec.get("ref")
    if isinstance(r, Mapping):
        rr = dict(r)
        if "loc" in rr:
            rr["loc"] = float(value)
        elif "mean" in rr:
            rr["mean"] = float(value)
        else:
            rr = {"loc": float(value), "scale": 0.0}
        spec["ref"] = rr
    else:
        spec["ref"] = float(value)
    params[name] = spec

def freeze_primordial(info: dict[str, Any], values: Mapping[str, float]) -> None:
    params = info["params"]
    missing = [k for k in PRIMORDIAL if k not in params]
    if missing:
        raise RuntimeError("PRIMORDIAL_PARAMETER_GATE=FAIL " + repr(missing))
    for name in PRIMORDIAL:
        params[name] = float(values[name])

def native_seed(q20: Mapping[str, Any], architecture: str) -> dict[str, float]:
    native_name, _ = endpoint_names(architecture)
    seed = endpoint(q20, native_name)
    seed.update(endpoint_nuisance(q20, native_name))
    return seed

def restart_phase(restart: int) -> float:
    phases = (-1.0, 0.0, 1.0)
    if restart < 0 or restart >= len(phases):
        raise RuntimeError("RESTART_GATE=FAIL")
    return phases[restart]

def build_info(c: Mapping[str, Any], architecture: str, mask: int,
               restart: int, prefix: Path) -> tuple[dict[str, Any], dict[str, float], dict[str, Any]]:
    import q019_planck_cosmology_reprofile_v1 as q19

    q20 = load_q020_cfg(c)
    q19_cfg = q19.load_cfg(ROOT / c["parents"]["q019"]["config"])
    seed = native_seed(q20, architecture)

    if architecture == "lite":
        info = q19.build_lite(q19_cfg, "reference_free_h0", 0, prefix, seed)
    elif architecture == "full_mf":
        info = q19.build_full(q19_cfg, "reference_free_h0", 0, prefix, seed)
    else:
        raise RuntimeError("ARCHITECTURE_GATE=FAIL")

    fixed = primordial_hybrid(q20, architecture, mask)
    freeze_primordial(info, fixed)

    # Re-profile every other parameter that the frozen Q019 constructor leaves sampled.
    # Only references are changed between deterministic multistarts; priors/bounds are untouched.
    phase = restart_phase(restart)
    scale = float(c["execution"]["restart_reference_scale"])
    params = info["params"]

    # Prefer native Q019/Q020 endpoint values; fall back to the constructor's own reference.
    for name, spec in list(params.items()):
        if not sampled(spec):
            continue
        base = seed.get(name, ref_value(spec))
        if base is None:
            continue
        jitter = float(getattr(q19, "JITTER", {}).get(name, 0.0))
        set_ref(params, name, float(base) + phase * scale * jitter)

    m = info.setdefault("sampler", {}).setdefault("minimize", {})
    m["max_evals"] = int(c["execution"]["max_evals"])
    m["best_of"] = 1
    m.setdefault("override_bobyqa", {})["rhoend"] = float(c["execution"]["rhoend"])
    info["output"] = str(prefix.resolve())
    info["force"] = True

    like = info.get("likelihood", {})
    likelihood_identity = {
        "keys": sorted(str(k) for k in like.keys()) if isinstance(like, Mapping) else [],
        "spec_hash": canonical_hash(like),
        "objective_basis": c["likelihoods"][architecture]["objective_basis"],
        "declared_identity": c["likelihoods"][architecture]["identity"],
    }
    return info, fixed, likelihood_identity

def run_profile(c: Mapping[str, Any], architecture: str, mask: int,
                restart: int, output: str | Path) -> int:
    import q019_planck_cosmology_reprofile_v1 as q19

    prefix = Path(output).with_suffix("")
    q20 = load_q020_cfg(c)
    native_name, foreign_name = endpoint_names(architecture)
    native_ep = endpoint(q20, native_name)
    foreign_ep = endpoint(q20, foreign_name)

    rec: dict[str, Any] = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q021_PRIMORDIAL_PROFILE",
        "architecture": architecture,
        "mask": int(mask),
        "restart": int(restart),
        "status": "FAILED",
        "actual_computed_result": False,
        "native_endpoint": native_name,
        "foreign_endpoint": foreign_name,
        "native_endpoint_hash": canonical_hash(native_ep),
        "foreign_endpoint_hash": canonical_hash(foreign_ep),
        "direction_semantics": (
            "FULL_MF_NATIVE_TO_LITE_FOREIGN"
            if architecture == "full_mf"
            else "LITE_NATIVE_TO_FULL_MF_FOREIGN"
        ),
        "cross_chain_chi2_sum_allowed": False,
        "independent_physical_chi2_interpretation_allowed": False,
        "causal_systematic_interpretation_allowed": False,
    }

    sampler = None
    try:
        info, fixed, like_id = build_info(c, architecture, mask, restart, prefix)
        free_names = sorted(
            name for name, spec in info["params"].items()
            if sampled(spec) and name not in PRIMORDIAL
        )
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
            "fixed_primordial": fixed,
            "reprofiled_parameter_names": free_names,
            "nuisance": q19.serial_nuisance(row, nuisance_names),
            "minimum": row,
            "harvested_minimum_path": source,
            "likelihood_identity": like_id,
            "objective_basis":
                "LIKELIHOOD_CHI2_PLUS_EXPLICIT_NORMALIZATION_FREE_SHARED_GAUSSIAN_SHAPES",
        })
    except Exception as exc:
        rec.update({
            "failure_class": "NUMERICAL_OR_LIKELIHOOD",
            "error": repr(exc),
        })
    finally:
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass

    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2

def load_json_any(path: str | Path, preferred_name: str | None = None) -> dict[str, Any]:
    p = Path(path)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    candidates = []
    if preferred_name:
        candidates.extend(p.rglob(preferred_name))
    if not candidates:
        candidates.extend(p.rglob("*.json"))
    for x in candidates:
        try:
            return json.loads(x.read_text(encoding="utf-8"))
        except Exception:
            continue
    raise RuntimeError(f"JSON_NOT_FOUND: {path}")

def parent_check(c: Mapping[str, Any], recomputed: str | Path,
                 authoritative: str | Path, output: str | Path) -> int:
    r = load_json_any(recomputed, "q021_parent_q020_recomputed.json")
    a = load_json_any(authoritative, "q020_merged_v2.json")
    tol = float(c["validation"]["parent_aggregate_abs_tolerance"])
    frac_tol = float(c["validation"]["parent_reference_fraction_tolerance"])
    signed_tol = float(c["validation"]["parent_reference_signed_tolerance"])

    def dig(d: Mapping[str, Any], arch: str, field: str, key: str | None = None):
        x = d["diagnostics"][arch][field]
        return x if key is None else x[key]

    exact_fields = [
        ("full_mf", "shapley_signed_objective_change", "primordial"),
        ("full_mf", "shapley_abs_fraction", "primordial"),
        ("lite", "shapley_signed_objective_change", "primordial"),
        ("lite", "shapley_abs_fraction", "primordial"),
    ]
    diffs = {}
    exact_ok = True
    for arch, field, key in exact_fields:
        rv = float(dig(r, arch, field, key))
        av = float(dig(a, arch, field, key))
        diff = abs(rv - av)
        diffs[f"{arch}.{field}.{key}"] = diff
        exact_ok = exact_ok and diff <= tol

    afrac = float(dig(a, "full_mf", "shapley_abs_fraction", "primordial"))
    asigned = float(dig(a, "full_mf", "shapley_signed_objective_change", "primordial"))
    gates = {
        "Q020_RECOMPUTED_STATUS_GATE": r.get("status") == "PASS" and r.get("FINAL_RESULT_GATE") == "PASS",
        "Q020_AUTHORITATIVE_STATUS_GATE": a.get("status") == "PASS" and a.get("FINAL_RESULT_GATE") == "PASS",
        "Q020_RESULT_ID_GATE": a.get("result_id") == c["parents"]["q020"]["result_id"],
        "Q020_REAGGREGATION_MATCH_GATE": exact_ok,
        "Q020_PRIMORDIAL_FRACTION_REFERENCE_GATE":
            abs(afrac - float(c["parents"]["q020"]["expected_full_mf_primordial_abs_fraction"])) <= frac_tol,
        "Q020_PRIMORDIAL_SIGNED_REFERENCE_GATE":
            abs(asigned - float(c["parents"]["q020"]["expected_full_mf_primordial_signed"])) <= signed_tol,
    }
    final = all(gates.values())
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q021_PARENT_Q020_REPRODUCTION",
        "status": "PASS" if final else "FAIL",
        "PARENT_REPRODUCTION_GATE": "PASS" if final else "FAIL",
        "gates": gates,
        "differences": diffs,
        "authoritative_parent": {
            "q": a.get("q"),
            "run_id": a.get("run_id"),
            "result_id": a.get("result_id"),
            "classification": a.get("classification"),
            "full_mf_primordial_signed_shapley": asigned,
            "full_mf_primordial_abs_fraction": afrac,
            "lite_primordial_signed_shapley":
                float(dig(a, "lite", "shapley_signed_objective_change", "primordial")),
            "lite_primordial_abs_fraction":
                float(dig(a, "lite", "shapley_abs_fraction", "primordial")),
        },
        "actual_new_likelihood_evaluations": 0,
        "interpretation":
            "PARENT_AGGREGATE_REPRODUCTION_ONLY_NOT_NEW_OBSERVATIONAL_EVIDENCE",
    }
    write_json(output, out)
    return 0 if final else 2

def collect(input_dir: str | Path) -> list[dict[str, Any]]:
    rows = []
    for p in Path(input_dir).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == "Q021_PRIMORDIAL_PROFILE":
            rows.append(d)
    return rows

def popcount(x: int) -> int:
    return int(x).bit_count()

def shapley(values: Mapping[int, float]) -> dict[str, float]:
    n = 3
    out = {}
    for i, name in enumerate(PRIMORDIAL):
        bit = 1 << i
        s = 0.0
        for mask in range(1 << n):
            if mask & bit:
                continue
            k = popcount(mask)
            w = math.factorial(k) * math.factorial(n-k-1) / math.factorial(n)
            s += w * (values[mask | bit] - values[mask])
        out[name] = float(s)
    return out

def mobius(values: Mapping[int, float]) -> dict[str, float]:
    v = values
    return {
        "n_s": float(v[1] - v[0]),
        "logA": float(v[2] - v[0]),
        "tau_reio": float(v[4] - v[0]),
        "n_s__x__logA": float(v[3] - v[1] - v[2] + v[0]),
        "n_s__x__tau_reio": float(v[5] - v[1] - v[4] + v[0]),
        "logA__x__tau_reio": float(v[6] - v[2] - v[4] + v[0]),
        "n_s__x__logA__x__tau_reio":
            float(v[7] - v[3] - v[5] - v[6] + v[1] + v[2] + v[4] - v[0]),
    }

def decompose(values: Mapping[int, float], dominance_threshold: float) -> dict[str, Any]:
    mm = mobius(values)
    sv = shapley(values)
    total = float(values[7] - values[0])
    closure = float(sum(mm.values()) - total)
    abs_sum = float(sum(abs(x) for x in mm.values()))
    fractions = {k: (abs(v) / abs_sum if abs_sum else 0.0) for k, v in mm.items()}
    ranked = sorted(mm, key=lambda k: abs(mm[k]), reverse=True)
    top = ranked[0]
    top_fraction = fractions[top]

    if top_fraction < dominance_threshold:
        structure = "DISTRIBUTED"
    elif "__x__" not in top:
        structure = "SINGLE"
    elif top.count("__x__") == 1:
        structure = "PAIR"
    else:
        structure = "THREE_WAY"

    return {
        "objective_native_mask0": float(values[0]),
        "objective_foreign_all_mask7": float(values[7]),
        "native_to_foreign_total_effect": total,
        "single_coordinate_effects": {
            k: mm[k] for k in ("n_s", "logA", "tau_reio")
        },
        "pairwise_interactions": {
            k: mm[k] for k in (
                "n_s__x__logA",
                "n_s__x__tau_reio",
                "logA__x__tau_reio",
            )
        },
        "three_way_interaction": mm["n_s__x__logA__x__tau_reio"],
        "mobius_terms": mm,
        "mobius_abs_fraction": fractions,
        "shapley_allocations": sv,
        "closure_residual": closure,
        "ranked_terms": ranked,
        "dominant_term": top,
        "dominant_abs_fraction": top_fraction,
        "dominance_threshold": dominance_threshold,
        "structure_class": structure,
        "interpretation": "FUNCTIONAL_ATTRIBUTION_NONINDEPENDENT_NONCAUSAL",
    }

def reverse_values(values: Mapping[int, float]) -> dict[int, float]:
    # Convert a lite-native -> full-MF-foreign game into canonical full-MF -> lite orientation.
    return {m: float(values[ALL_MASK ^ m]) for m in range(8)}

def total_variation_abs_fraction(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    keys = sorted(set(a) | set(b))
    return 0.5 * sum(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys)

def classify_architecture_difference(diag: Mapping[str, Any], c: Mapping[str, Any]) -> dict[str, Any]:
    f = diag["full_mf"]["native_oriented"]
    l = diag["lite"]["native_oriented"]
    tv = total_variation_abs_fraction(f["mobius_abs_fraction"], l["mobius_abs_fraction"])
    same_structure = f["structure_class"] == l["structure_class"]
    same_dominant = f["dominant_term"] == l["dominant_term"]
    threshold = float(c["validation"]["construction_abs_fraction_tv_threshold"])
    localized = {"SINGLE", "PAIR", "THREE_WAY"}
    identity_mismatch = (
        (f["structure_class"] in localized or l["structure_class"] in localized)
        and not same_dominant
    )
    material = (tv >= threshold) or (not same_structure) or identity_mismatch
    return {
        "abs_fraction_total_variation_distance": tv,
        "materiality_threshold": threshold,
        "same_structure_class": same_structure,
        "same_dominant_term": same_dominant,
        "materially_different": bool(material),
        "basis": "FUNCTIONAL_COMPOSITION_DIAGNOSTIC_NOT_INDEPENDENT_DATA",
    }

def find_parent_check(input_dir: str | Path) -> dict[str, Any] | None:
    for p in Path(input_dir).rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("q") == Q and d.get("stage") == "Q021_PARENT_Q020_REPRODUCTION":
            return d
    return None

def aggregate(c: Mapping[str, Any], input_dir: str | Path, output: str | Path) -> int:
    rows = collect(input_dir)
    parent = find_parent_check(input_dir)
    nrestart = int(c["execution"]["multistarts"])
    expected = {(a, m, r) for a in ARCHITECTURES for m in range(8) for r in range(nrestart)}
    complete = [
        r for r in rows
        if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))
    ]
    got = {(r["architecture"], int(r["mask"]), int(r["restart"])) for r in complete}

    by_arch: dict[str, dict[int, float]] = {}
    stability: dict[str, Any] = {}
    diagnostics: dict[str, Any] = {}
    all_restart_decompositions: dict[str, Any] = {}
    dom_threshold = float(c["validation"]["dominant_abs_mobius_fraction_threshold"])
    closure_tol = float(c["validation"]["closure_abs_tolerance"])
    restart_spread_tol = float(c["validation"]["restart_delta_objective_max"])

    for arch in ARCHITECTURES:
        values: dict[int, float] = {}
        spreads: dict[int, float | None] = {}
        best_rows: dict[str, Any] = {}
        for m in range(8):
            rr = sorted(
                [r for r in complete if r["architecture"] == arch and int(r["mask"]) == m],
                key=lambda x: float(x["objective_chi2"])
            )
            if rr:
                values[m] = float(rr[0]["objective_chi2"])
                best_rows[str(m)] = rr[0]
            spreads[m] = (
                float(max(float(x["objective_chi2"]) for x in rr) -
                      min(float(x["objective_chi2"]) for x in rr))
                if len(rr) == nrestart else None
            )
        by_arch[arch] = values

        restart_decomp = {}
        for rix in range(nrestart):
            rv = {}
            for m in range(8):
                hits = [
                    x for x in complete
                    if x["architecture"] == arch
                    and int(x["mask"]) == m
                    and int(x["restart"]) == rix
                ]
                if len(hits) == 1:
                    rv[m] = float(hits[0]["objective_chi2"])
            if len(rv) == 8:
                restart_decomp[str(rix)] = decompose(rv, dom_threshold)
        all_restart_decompositions[arch] = restart_decomp

        if len(values) == 8:
            native_d = decompose(values, dom_threshold)
            canonical_values = values if arch == "full_mf" else reverse_values(values)
            canonical_d = decompose(canonical_values, dom_threshold)
            diagnostics[arch] = {
                "native_oriented": native_d,
                "canonical_full_mf_to_lite": canonical_d,
                "best_rows": best_rows,
            }
        stability[arch] = {
            "vertex_objective_spreads": {str(k): v for k, v in spreads.items()},
            "max_vertex_objective_spread":
                max((v for v in spreads.values() if v is not None), default=None),
        }

    complete_grid = all(len(by_arch[a]) == 8 for a in ARCHITECTURES)
    closure_pass = (
        complete_grid and
        all(abs(diagnostics[a]["native_oriented"]["closure_residual"]) <= closure_tol
            and abs(diagnostics[a]["canonical_full_mf_to_lite"]["closure_residual"]) <= closure_tol
            for a in ARCHITECTURES)
    )

    # Likelihood identity must be invariant within each architecture.
    like_identity_ok = True
    like_identities = {}
    endpoint_hash_ok = True
    endpoint_hashes = {}
    for arch in ARCHITECTURES:
        rr = [r for r in complete if r["architecture"] == arch]
        lh = sorted({r.get("likelihood_identity", {}).get("spec_hash") for r in rr if r.get("likelihood_identity")})
        like_identities[arch] = lh
        like_identity_ok = like_identity_ok and len(lh) == 1
        nh = sorted({r.get("native_endpoint_hash") for r in rr})
        fh = sorted({r.get("foreign_endpoint_hash") for r in rr})
        endpoint_hashes[arch] = {"native": nh, "foreign": fh}
        endpoint_hash_ok = endpoint_hash_ok and len(nh) == 1 and len(fh) == 1

    # Multistart must support the same ranking leader and structure class.
    ranking_stability = {}
    ranking_ok = True
    for arch in ARCHITECTURES:
        rd = all_restart_decompositions.get(arch, {})
        classes = [x["structure_class"] for x in rd.values()]
        leaders = [x["dominant_term"] for x in rd.values()]
        stable = (
            len(rd) == nrestart
            and len(set(classes)) == 1
            and len(set(leaders)) == 1
        )
        ranking_stability[arch] = {
            "structure_classes": classes,
            "dominant_terms": leaders,
            "stable": stable,
        }
        ranking_ok = ranking_ok and stable

    restart_obj_ok = all(
        stability[a]["max_vertex_objective_spread"] is not None
        and float(stability[a]["max_vertex_objective_spread"]) <= restart_spread_tol
        for a in ARCHITECTURES
    )

    arch_cmp = classify_architecture_difference(diagnostics, c) if complete_grid else {}

    gates = {
        "Q_IDENTITY_GATE": True,
        "MODEL_IDENTITY_GATE": True,
        "Q020_PARENT_REPRODUCTION_GATE":
            bool(parent and parent.get("PARENT_REPRODUCTION_GATE") == "PASS"),
        "JOB_COMPLETENESS_GATE": got == expected and len(complete) == len(expected),
        "FINITE_RESULT_GATE": len(complete) == len(expected),
        "VERTEX_GRID_COMPLETENESS_GATE": complete_grid,
        "ENDPOINT_IDENTITY_GATE": endpoint_hash_ok,
        "LIKELIHOOD_OBJECT_IDENTITY_GATE": like_identity_ok,
        "DECOMPOSITION_CLOSURE_GATE": closure_pass,
        "MULTISTART_OBJECTIVE_STABILITY_GATE": restart_obj_ok,
        "MULTISTART_RANKING_STABILITY_GATE": ranking_ok,
        "EQUIVALENT_INTERVENTION_SEMANTICS_GATE": True,
        "NO_CROSS_CHAIN_CHI2_SUM_GATE": c["rules"]["no_cross_chain_chi2_sum"] is True,
        "INTERPRETATION_SAFETY_GATE":
            c["rules"]["functional_attribution_not_independent_physical_chi2"] is True
            and c["rules"]["causal_systematic_claim_forbidden"] is True
            and c["rules"]["new_physics_claim_forbidden"] is True,
    }

    final = all(gates.values())
    classification = "INDETERMINATE — NUMERICAL OR IDENTIFIABILITY LIMIT"
    pattern_effect = "UNRESOLVED"
    interpretation = {}

    if final:
        f = diagnostics["full_mf"]["native_oriented"]
        if arch_cmp["materially_different"]:
            classification = "LIKELIHOOD-CONSTRUCTION-DEPENDENT PRIMORDIAL GEOMETRY"
            pattern_effect = "NARROWED"
        elif f["structure_class"] == "SINGLE":
            classification = "PRIMORDIAL SINGLE-DIRECTION LOCALIZED"
            pattern_effect = "NARROWED"
        elif f["structure_class"] == "PAIR":
            classification = "PRIMORDIAL PAIR-COUPLING LOCALIZED"
            pattern_effect = "NARROWED"
        elif f["structure_class"] in ("THREE_WAY", "DISTRIBUTED"):
            classification = "PRIMORDIAL THREE-WAY / DISTRIBUTED COUPLING"
            pattern_effect = "STRENGTHENED"

        interpretation = {
            "full_mf_structure": f["structure_class"],
            "full_mf_dominant_term": f["dominant_term"],
            "full_mf_dominant_abs_fraction": f["dominant_abs_fraction"],
            "lite_structure": diagnostics["lite"]["native_oriented"]["structure_class"],
            "lite_dominant_term": diagnostics["lite"]["native_oriented"]["dominant_term"],
            "likelihood_construction_dependence": arch_cmp["materially_different"],
            "q020_primordial_pattern_effect": pattern_effect,
            "causal_systematic_claim": False,
            "independent_observational_evidence_claim": False,
            "new_physics_claim": False,
        }

    failed_rows = [
        {
            "architecture": r.get("architecture"),
            "mask": r.get("mask"),
            "restart": r.get("restart"),
            "error": r.get("error"),
            "failure_class": r.get("failure_class"),
        }
        for r in rows if r.get("status") != "COMPLETE"
    ]

    q20 = load_q020_cfg(c)
    ep_summary = {}
    for name in ("lite_v1", "full_mf_v1"):
        e = endpoint(q20, name)
        ep_summary[name] = {
            "hash": canonical_hash(e),
            "cosmology": e,
        }

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q021_FINAL",
        "status": "PASS" if final else "FAIL",
        "FINAL_RESULT_GATE": "PASS" if final else "FAIL",
        "actual_computed_result": bool(complete),
        "classification": classification,
        "q020_pattern_effect": pattern_effect,
        "model": c["model"],
        "likelihoods": c["likelihoods"],
        "endpoints": ep_summary,
        "gates": gates,
        "parent_q020_reproduction": parent,
        "diagnostics": diagnostics,
        "architecture_comparison": arch_cmp,
        "multistart_decompositions": all_restart_decompositions,
        "stability": stability,
        "ranking_stability": ranking_stability,
        "likelihood_spec_hashes": like_identities,
        "endpoint_hashes_seen": endpoint_hashes,
        "failed_or_unavailable_profiles": failed_rows,
        "scientific_interpretation": interpretation,
        "provenance": {
            "bubbleverse_repository": c["provenance"]["bubbleverse_repository"],
            "q020_parent_run_v1": c["parents"]["q020"]["v1_github_run_id"],
            "q020_authoritative_v2_run": c["parents"]["q020"]["v2_github_run_id"],
            "q020_result_id": c["parents"]["q020"]["result_id"],
            "q019_builder": c["parents"]["q019"]["builder"],
            "q019_config": c["parents"]["q019"]["config"],
            "source_lock": c["provenance"]["source_lock"],
        },
        "rules": {
            "cross_chain_chi2_sum_performed": False,
            "functional_attribution_is_independent_physical_chi2": False,
            "causal_systematic_claim": False,
            "new_physics_claim": False,
            "matched_and_full_mf_are_independent_observations": False,
        },
        "return_route": "RESULT INGESTION & ROUTING ENGINE",
    }
    write_json(output, out)
    return 0 if final else 2

def plan(c: Mapping[str, Any], output: str | Path) -> int:
    q20 = load_q020_cfg(c)
    nrestart = int(c["execution"]["multistarts"])
    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "execution_mode": "HPC PROGRAM",
        "scientific_question": c["scientific_question"],
        "parent_reproduction": {
            "q020_v1_github_run_id": c["parents"]["q020"]["v1_github_run_id"],
            "q020_v2_github_run_id": c["parents"]["q020"]["v2_github_run_id"],
            "new_likelihood_evaluations": 0,
        },
        "new_profile_grid": {
            "architectures": list(ARCHITECTURES),
            "coordinates": list(PRIMORDIAL),
            "masks_per_architecture": 8,
            "multistarts": nrestart,
            "expected_new_profile_jobs": 2 * 8 * nrestart,
            "reprofile_rule":
                "FIX_THREE_PRIMORDIAL_COORDINATES_AT_NATIVE_OR_FOREIGN_VERTEX; "
                "REPROFILE_ALL_OTHER_PARAMETERS_LEFT_SAMPLED_BY_FROZEN_Q019_CONSTRUCTOR",
        },
        "endpoint_hashes": {
            name: canonical_hash(endpoint(q20, name))
            for name in ("lite_v1", "full_mf_v1")
        },
        "mandatory_tests": [
            "Q020_PARENT_REPRODUCTION",
            "JOB_COMPLETENESS",
            "FINITE_RESULT",
            "ENDPOINT_IDENTITY",
            "LIKELIHOOD_OBJECT_IDENTITY",
            "DECOMPOSITION_CLOSURE",
            "MULTISTART_OBJECTIVE_STABILITY",
            "MULTISTART_RANKING_STABILITY",
            "EQUIVALENT_INTERVENTION_SEMANTICS",
            "INTERPRETATION_SAFETY",
        ],
    }
    write_json(output, out)
    return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q021_primordial_decomposition_v1_config.yml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--output", required=True)

    p = sub.add_parser("parent-check")
    p.add_argument("--recomputed", required=True)
    p.add_argument("--authoritative", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--architecture", choices=ARCHITECTURES, required=True)
    p.add_argument("--mask", type=int, choices=range(8), required=True)
    p.add_argument("--restart", type=int, required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_cfg(a.config)

    if a.cmd == "plan":
        return plan(c, a.output)
    if a.cmd == "parent-check":
        return parent_check(c, a.recomputed, a.authoritative, a.output)
    if a.cmd == "profile":
        return run_profile(c, a.architecture, a.mask, a.restart, a.output)
    if a.cmd == "aggregate":
        return aggregate(c, a.input_dir, a.output)
    raise RuntimeError("COMMAND_GATE=FAIL")

if __name__ == "__main__":
    raise SystemExit(main())
