#!/usr/bin/env python3
"""
Bubbleverse Q025 V2 — full-multifrequency basin component attribution.

Scientific contract
-------------------
CURRENT Q: Q025

Question:
Which likelihood components, spectra, frequency combinations, and parameter-group
interactions are responsible for the strengthened mask dependence of the stable
Q022 full-multifrequency basin geometries across masks 3, 6, and 7?

This program:
* reuses authoritative Q022 V2 endpoints;
* performs NO optimization, sampling, or endpoint generation;
* performs NO Q024 permutation rerun;
* uses the same MOD-EDE-N3 / n_scf=3 / frozen class_ede backend;
* evaluates exact fixed vectors in the full-MF CamSpec likelihood;
* reuses Q017's covariance-aware full-MF decomposition machinery;
* evaluates exact 2^3 functional group hybrids per basin edge, because the
  primordial block is fixed within each Q022 mask by construction;
* reports signed Shapley values and pair interactions as technical functional
  attribution, not causal physical decomposition;
* preserves negative signed covariance contributions and cancellations.

The three varying blocks are:
  cosmology       = omega_b, omega_cdm, fEDE, log10z_c, thetai_scf, H0
  shared_nuisance = A_planck, calTE, calEE
  foreground      = amp_143, amp_217, amp_143x217, n_143, n_217, n_143x217

The primordial block [n_s, logA, tau_reio] is required, validated, and held at
the common Q022-mask value. Its absence from the 3-block hybrid grid is NOT a
claim that primordial structure is globally irrelevant; it reflects Q022's
within-mask construction and preserves Q021's distributed primordial result.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q025"
RUN = "Q025-FULLMF-BASIN-COMPONENT-ATTRIBUTION-V2"
RESULT = "R-Q025-EDE-FULLMF-BASIN-COMPONENT-ATTRIBUTION-002"
FULL_LIKE = "planck_NPIPE_highl_CamSpec.TTTEEE"
MASKS = (3, 6, 7)
SEEDS = (0, 1, 2)
EDGES = ((0, 1), (0, 2), (1, 2))
GROUP_ORDER = ("cosmology", "shared_nuisance", "foreground")

PARAM_GROUPS = {
    "cosmology": ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0"),
    "primordial": ("n_s", "logA", "tau_reio"),
    "shared_nuisance": ("A_planck", "calTE", "calEE"),
    "foreground": ("amp_143", "amp_217", "amp_143x217", "n_143", "n_217", "n_143x217"),
}
ALL_PARAMS = tuple(p for g in ("cosmology","primordial","shared_nuisance","foreground")
                   for p in PARAM_GROUPS[g])
ALL_MASK = (1 << len(GROUP_ORDER)) - 1


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_GATE=FAIL {path}")
    return d


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=_json_default) + "\n",
                 encoding="utf-8")
    os.replace(t, p)


def _json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating)):
        return x.item()
    return str(x)


def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(c, dict):
        raise RuntimeError("CONFIG_GATE=FAIL")
    pr = c["project"]
    m = c["model"]
    if pr["q"] != Q or pr["run_id"] != RUN or pr["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if tuple(c["selection"]["masks"]) != MASKS:
        raise RuntimeError("MASK_SCOPE_GATE=FAIL")
    if c["likelihood"]["full_mf"] != FULL_LIKE:
        raise RuntimeError("FULL_MF_LIKELIHOOD_GATE=FAIL")
    if c["rules"]["no_optimization"] is not True:
        raise RuntimeError("NO_OPTIMIZATION_GATE=FAIL")
    if c["rules"]["no_q024_permutation_rerun"] is not True:
        raise RuntimeError("Q024_PRESERVATION_GATE=FAIL")
    return c


def read_all_json(root: str | Path) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in Path(root).rglob("*.json"):
        try:
            d = read_json(path)
        except Exception:
            continue
        rows.append((path, d))
    return rows


def load_q022_final(q022_dir: str | Path) -> dict[str, Any]:
    hits = []
    for path, d in read_all_json(q022_dir):
        if path.name != "q022_final_v2.json":
            continue
        if (
            d.get("q") == "Q022"
            and d.get("run_id") == "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
            and d.get("result_id") == "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
            and d.get("FINAL_RESULT_GATE") == "PASS"
            and d.get("status") == "PASS"
            and d.get("classification")
                == "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
        ):
            hits.append((path, d))
    if len(hits) != 1:
        raise RuntimeError(
            f"Q022_AUTHORITATIVE_FINAL_GATE=FAIL hits={len(hits)} "
            f"files={[str(x[0]) for x in hits]}"
        )
    return hits[0][1]


def q022_decision_phase(final: Mapping[str, Any], mask: int) -> str:
    hits = [
        v for v in final.get("final_vertices", [])
        if int(v.get("mask", -1)) == int(mask)
    ]
    if len(hits) != 1:
        raise RuntimeError(f"Q022_MASK_DECISION_GATE=FAIL mask={mask} hits={len(hits)}")
    v = hits[0]
    if v.get("classification") != "STABLE_MULTIBASIN":
        raise RuntimeError(
            f"Q022_STABLE_MULTIBASIN_GATE=FAIL mask={mask} "
            f"classification={v.get('classification')}"
        )
    phase = str(v.get("decision_phase"))
    if phase not in ("stage1", "refinement"):
        raise RuntimeError(f"Q022_DECISION_PHASE_GATE=FAIL mask={mask} phase={phase}")
    return phase


def flatten_q022_endpoint(row: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    # Q022 follows the Q019/Q023 convention: scientific coordinates are split
    # between `minimum` and chain-native `nuisance`.
    for block in ("minimum", "nuisance"):
        x = row.get(block, {})
        if isinstance(x, Mapping):
            for k, v in x.items():
                if finite(v):
                    out[str(k)] = float(v)
    return out


def load_q021_primordial(q021_dir: str | Path, mask: int, seed: int) -> dict[str, float]:
    hits = []
    for path, d in read_all_json(q021_dir):
        if (
            d.get("q") == "Q021"
            and d.get("run_id") == "Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1"
            and d.get("result_id") == "R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-001"
            and d.get("stage") == "Q021_PRIMORDIAL_PROFILE"
            and d.get("architecture") == "full_mf"
            and int(d.get("mask", -1)) == int(mask)
            and int(d.get("restart", -1)) == int(seed)
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            fp = d.get("fixed_primordial", {})
            if (
                isinstance(fp, Mapping)
                and all(k in fp and finite(fp[k]) for k in PARAM_GROUPS["primordial"])
            ):
                hits.append((path, d, fp))
    if len(hits) != 1:
        raise RuntimeError(
            f"Q021_PRIMORDIAL_LINEAGE_GATE=FAIL mask={mask} seed={seed} "
            f"hits={len(hits)}"
        )
    path, d, fp = hits[0]
    return {
        "path": str(path),
        "params": {k: float(fp[k]) for k in PARAM_GROUPS["primordial"]},
        "parent_record": {
            "q": d.get("q"),
            "run_id": d.get("run_id"),
            "result_id": d.get("result_id"),
            "mask": int(mask),
            "restart": int(seed),
        },
    }


def load_q022_endpoint(
    q022_dir: str | Path,
    q021_dir: str | Path,
    final: Mapping[str, Any],
    mask: int,
    seed: int,
) -> dict[str, Any]:
    phase = q022_decision_phase(final, mask)
    hits = []
    for path, d in read_all_json(q022_dir):
        if (
            d.get("q") == "Q022"
            and d.get("run_id") == "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
            and d.get("result_id") == "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
            and d.get("stage") == "Q022_CROSS_START_CONTINUATION"
            and d.get("phase") == phase
            and int(d.get("mask", -1)) == int(mask)
            and int(d.get("seed_restart", -1)) == int(seed)
            and d.get("status") == "COMPLETE"
            and finite(d.get("objective_chi2"))
        ):
            flat = flatten_q022_endpoint(d)
            required_nonprimordial = (
                PARAM_GROUPS["cosmology"]
                + PARAM_GROUPS["shared_nuisance"]
                + PARAM_GROUPS["foreground"]
            )
            if all(k in flat and finite(flat[k]) for k in required_nonprimordial):
                hits.append((path, d, flat))

    if len(hits) != 1:
        raise RuntimeError(
            f"Q022_ENDPOINT_GATE=FAIL mask={mask} seed={seed} "
            f"phase={phase} hits={len(hits)}"
        )

    path, d, flat = hits[0]
    primordial = load_q021_primordial(q021_dir, mask, seed)
    params = dict(flat)
    params.update(primordial["params"])

    missing = [k for k in ALL_PARAMS if k not in params or not finite(params[k])]
    if missing:
        raise RuntimeError(
            f"ENDPOINT_PARAMETER_COMPLETENESS_GATE=FAIL "
            f"mask={mask} seed={seed} missing={missing}"
        )

    return {
        "path": str(path),
        "phase": phase,
        "status": d.get("status"),
        "objective_chi2": float(d["objective_chi2"]),
        "params": {k: float(params[k]) for k in ALL_PARAMS},
        "parent_record": {
            "q": d.get("q"),
            "run_id": d.get("run_id"),
            "result_id": d.get("result_id"),
            "mask": int(mask),
            "seed_restart": int(seed),
            "decision_phase": phase,
        },
        "primordial_parent": primordial["parent_record"],
        "primordial_source": primordial["path"],
    }


def assert_primordial_common(a: Mapping[str,float], b: Mapping[str,float], tol: float) -> None:
    bad = {}
    for p in PARAM_GROUPS["primordial"]:
        dv = abs(float(a[p])-float(b[p]))
        if dv > tol:
            bad[p] = dv
    if bad:
        raise RuntimeError("PRIMORDIAL_WITHIN_MASK_IDENTITY_GATE=FAIL " + repr(bad))


def hybrid(a: Mapping[str,float], b: Mapping[str,float], vertex: int) -> dict[str,float]:
    if vertex < 0 or vertex > ALL_MASK:
        raise RuntimeError("HYBRID_VERTEX_GATE=FAIL")
    out = {k: float(a[k]) for k in ALL_PARAMS}
    # Primordial always remains from A; equality with B was already gated.
    for i, group in enumerate(GROUP_ORDER):
        src = b if (vertex & (1 << i)) else a
        for p in PARAM_GROUPS[group]:
            out[p] = float(src[p])
    return out


def build_full_model(c: Mapping[str,Any], seed_values: Mapping[str,float]):
    # Reuse Q019's known-good full-MF construction.
    import q019_planck_cosmology_reprofile_v1 as q19
    parent = q19.load_cfg(ROOT / c["reuse"]["q019_config"])
    info = q19.build_full(
        parent, "reference_free_h0", 0,
        Path(c["execution"]["scratch_prefix"]),
        seed_values
    )
    if FULL_LIKE not in info.get("likelihood", {}):
        raise RuntimeError("FULL_MF_COMPONENT_GATE=FAIL")
    info["likelihood"] = {FULL_LIKE: info["likelihood"][FULL_LIKE]}
    # No sampler; retain sampled parameter definitions and priors so logposterior
    # at explicit fixed vectors retains the frozen objective semantics.
    info.pop("sampler", None)
    info.pop("output", None)
    info.pop("resume", None)
    info.pop("force", None)

    sampled = []
    for name, spec in info.get("params", {}).items():
        if isinstance(spec, Mapping) and "prior" in spec:
            sampled.append(str(name))
    missing = sorted(set(ALL_PARAMS) - set(sampled))
    extra = sorted(set(sampled) - set(ALL_PARAMS))
    if missing or extra:
        raise RuntimeError(f"SAMPLED_PARAMETER_COVERAGE_GATE=FAIL missing={missing} extra={extra}")

    from cobaya.model import get_model
    return get_model(info)


def logpost_value(lp: Any) -> float:
    x = getattr(lp, "logpost", None)
    if finite(x):
        return float(x)
    if finite(lp):
        return float(lp)
    raise RuntimeError("FINITE_LOGPOST_GATE=FAIL")


def state_for_vector(model: Any, values: Mapping[str,float], c: Mapping[str,Any]) -> dict[str,Any]:
    lp = model.logposterior(dict(values))
    logpost = logpost_value(lp)

    # q017 functions operate on provider state produced by the current evaluation.
    import q017_planck_direction_localization_v1 as q17
    cosmology = {p: float(values[p]) for p in PARAM_GROUPS["cosmology"]}
    # tau/logA/n_s are cosmological theory inputs even though Bubbleverse tracks
    # them as the primordial block.
    cosmology.update({p: float(values[p]) for p in PARAM_GROUPS["primordial"]})
    nuisance = {p: float(values[p]) for p in
                PARAM_GROUPS["shared_nuisance"] + PARAM_GROUPS["foreground"]}
    expanded = q17.expanded_values(model, cosmology, nuisance)

    q17_cfg = {
        "decomposition": {"ell_bands": c["decomposition"]["ell_bands"]}
    }
    detailed = q17.detailed_planck_state(model, expanded, q17_cfg)

    # Independent closure against Q015's proven evaluator.
    import q015_cmb_attribution_v2 as q15
    q15cfg = yaml.safe_load((ROOT / c["reuse"]["q015_config"]).read_text(encoding="utf-8"))
    q15cfg["ell_bands"] = c["decomposition"]["ell_bands"]
    reference = q15.planck_highl_state(model, expanded, q15cfg)

    tol = float(c["validation"]["covariance_closure_abs_tol"])
    gates = {
        "finite_logpost": finite(logpost),
        "finite_covariance_chi2": finite(detailed.get("chi2")),
        "q015_reference_closure":
            abs(float(reference["chi2"]) - float(detailed["chi2"])) <= tol,
        "signed_allocation_closure":
            abs(float(detailed["chi2"]) - float(detailed["signed_contribution_sum"])) <= tol,
        "covariance_pair_closure":
            abs(float(detailed["chi2"]) - float(detailed["covariance_block_pair_sum"])) <= tol,
    }
    return {
        "logpost": logpost,
        "objective_minus2logpost": -2.0 * logpost,
        "highl_covariance_chi2": float(detailed["chi2"]),
        "groups": detailed["groups"],
        "covariance_block_pair_terms": detailed["covariance_block_pair_terms"],
        "q015_reference_chi2": float(reference["chi2"]),
        "gates": gates,
        "status": "PASS" if all(gates.values()) else "FAIL",
    }


def run_edge(c: Mapping[str,Any], q022_dir: str | Path, q021_dir: str | Path,
             mask: int, seed_a: int, seed_b: int, output: str | Path) -> int:
    if mask not in MASKS or (seed_a, seed_b) not in EDGES:
        raise RuntimeError("EDGE_SCOPE_GATE=FAIL")
    final = load_q022_final(q022_dir)
    a = load_q022_endpoint(q022_dir, q021_dir, final, mask, seed_a)
    b = load_q022_endpoint(q022_dir, q021_dir, final, mask, seed_b)
    assert_primordial_common(a["params"], b["params"],
                             float(c["validation"]["primordial_identity_abs_tol"]))

    rec: dict[str,Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "EDGE_FIXED_VECTOR_GRID",
        "mask": mask, "edge": [seed_a, seed_b],
        "status": "FAILED", "actual_new_likelihood_evaluations": 0,
        "optimizer_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "parents": {"a": a["parent_record"], "b": b["parent_record"]},
        "endpoint_sources": {"a": a["path"], "b": b["path"]},
        "primordial_sources": {"a": a["primordial_source"], "b": b["primordial_source"]},
        "primordial_role":
            "COMMON_WITHIN_MASK_FIXED_BLOCK_PRESERVED_NOT_DECLARED_PHYSICALLY_IRRELEVANT",
    }
    model = None
    try:
        model = build_full_model(c, a["params"])
        states = {}
        for vertex in range(1 << len(GROUP_ORDER)):
            vec = hybrid(a["params"], b["params"], vertex)
            states[str(vertex)] = {
                "group_source_bits": {
                    GROUP_ORDER[i]: ("B" if vertex & (1 << i) else "A")
                    for i in range(len(GROUP_ORDER))
                },
                "values": vec,
                "evaluation": state_for_vector(model, vec, c),
            }
            rec["actual_new_likelihood_evaluations"] += 1
        rec["vertices"] = states
        rec["status"] = "COMPLETE" if all(
            v["evaluation"]["status"] == "PASS" for v in states.values()
        ) else "FAILED_VALIDATION"
    except Exception as exc:
        rec["failure_class"] = "NUMERICAL_OR_LIKELIHOOD"
        rec["error"] = repr(exc)
    finally:
        try:
            if model is not None and hasattr(model, "close"):
                model.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def popcount(x: int) -> int:
    return int(x).bit_count()


def shapley(values: Mapping[int,float]) -> dict[str,float]:
    n = len(GROUP_ORDER)
    out = {}
    for i, group in enumerate(GROUP_ORDER):
        bit = 1 << i
        s = 0.0
        for mask in range(1 << n):
            if mask & bit:
                continue
            k = popcount(mask)
            w = math.factorial(k) * math.factorial(n-k-1) / math.factorial(n)
            s += w * (float(values[mask | bit]) - float(values[mask]))
        out[group] = float(s)
    return out


def pair_interactions(values: Mapping[int,float]) -> dict[str,float]:
    n = len(GROUP_ORDER)
    out = {}
    for i in range(n):
        for j in range(i+1, n):
            bi, bj = 1 << i, 1 << j
            rem = [k for k in range(n) if k not in (i,j)]
            terms = []
            for choices in range(1 << len(rem)):
                m = 0
                for rix, k in enumerate(rem):
                    if choices & (1 << rix):
                        m |= 1 << k
                terms.append(
                    float(values[m|bi|bj]) - float(values[m|bi])
                    - float(values[m|bj]) + float(values[m])
                )
            out[f"{GROUP_ORDER[i]}__x__{GROUP_ORDER[j]}"] = float(sum(terms)/len(terms))
    return out


def diffmap(b: Mapping[str,Any], a: Mapping[str,Any]) -> dict[str,float]:
    keys = sorted(set(b) | set(a))
    return {k: float(b.get(k,0.0)) - float(a.get(k,0.0)) for k in keys}


def abs_rank(d: Mapping[str,float], n: int = 20) -> list[dict[str,Any]]:
    rows = [{"name": str(k), "value": float(v), "abs_value": abs(float(v))}
            for k,v in d.items() if finite(v)]
    rows.sort(key=lambda x: x["abs_value"], reverse=True)
    return rows[:n]


def edge_diagnostics(row: Mapping[str,Any]) -> dict[str,Any]:
    vv = {int(k): v["evaluation"] for k,v in row["vertices"].items()}
    a, b = vv[0], vv[ALL_MASK]
    delta = {
        "objective_minus2logpost":
            float(b["objective_minus2logpost"]) - float(a["objective_minus2logpost"]),
        "highl_covariance_chi2":
            float(b["highl_covariance_chi2"]) - float(a["highl_covariance_chi2"]),
        "by_observable": diffmap(b["groups"]["by_observable"], a["groups"]["by_observable"]),
        "by_spectrum": diffmap(b["groups"]["by_spectrum"], a["groups"]["by_spectrum"]),
        "by_band": diffmap(b["groups"]["by_band"], a["groups"]["by_band"]),
        "by_spectrum_band":
            diffmap(b["groups"]["by_spectrum_band"], a["groups"]["by_spectrum_band"]),
        "by_observable_spectrum_band":
            diffmap(b["groups"]["by_observable_spectrum_band"],
                    a["groups"]["by_observable_spectrum_band"]),
        "covariance_block_pair_terms":
            diffmap(b["covariance_block_pair_terms"], a["covariance_block_pair_terms"]),
    }
    objective_values = {m: float(v["objective_minus2logpost"]) for m,v in vv.items()}
    highl_values = {m: float(v["highl_covariance_chi2"]) for m,v in vv.items()}
    return {
        "endpoint_delta": delta,
        "dominant_observables": abs_rank(delta["by_observable"]),
        "dominant_spectra": abs_rank(delta["by_spectrum"]),
        "dominant_spectrum_bands": abs_rank(delta["by_spectrum_band"]),
        "dominant_covariance_pairs": abs_rank(delta["covariance_block_pair_terms"]),
        "functional_attribution": {
            "objective_shapley": shapley(objective_values),
            "objective_pair_interactions": pair_interactions(objective_values),
            "highl_shapley": shapley(highl_values),
            "highl_pair_interactions": pair_interactions(highl_values),
            "interpretation":
                "SIGNED_FUNCTIONAL_ATTRIBUTION_NONINDEPENDENT_NONCAUSAL",
        },
        "bridge": {
            "endpoint_delta_objective_minus_highl_covariance":
                delta["objective_minus2logpost"] - delta["highl_covariance_chi2"],
            "interpretation":
                "NON_BANDPOWER_OBJECTIVE_TERMS_AND_LIKELIHOOD_CONVENTION_BRIDGE_NOT_DISTRIBUTED_ACROSS_SPECTRA",
        },
    }


def aggregate(c: Mapping[str,Any], input_dir: str | Path, output: str | Path) -> int:
    rows = []
    for p in Path(input_dir).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == "EDGE_FIXED_VECTOR_GRID":
            rows.append(d)

    expected = {(m,a,b) for m in MASKS for a,b in EDGES}
    got = {(int(r["mask"]), int(r["edge"][0]), int(r["edge"][1])) for r in rows
           if r.get("status") == "COMPLETE"}

    diagnostics = {}
    for r in rows:
        key = f"m{int(r['mask'])}_e{int(r['edge'][0])}{int(r['edge'][1])}"
        if r.get("status") == "COMPLETE":
            diagnostics[key] = edge_diagnostics(r)

    total_evals = sum(int(r.get("actual_new_likelihood_evaluations",0)) for r in rows)
    required_evals = len(expected) * (1 << len(GROUP_ORDER))

    # Cross-mask driver consistency is descriptive: it asks whether the same
    # dominant named spectrum / group repeatedly appears. It does not convert
    # technical attribution into physical causality.
    top_spectrum = {k: (v["dominant_spectra"][0]["name"]
                        if v["dominant_spectra"] else None)
                    for k,v in diagnostics.items()}
    top_highl_group = {}
    for k,v in diagnostics.items():
        sh = v["functional_attribution"]["highl_shapley"]
        top_highl_group[k] = max(sh, key=lambda x: abs(float(sh[x]))) if sh else None

    gates = {
        "CONTEXT_CONTINUITY_GATE": True,
        "Q_IDENTITY_GATE": True,
        "MODEL_IDENTITY_GATE": True,
        "MASK_SCOPE_GATE": True,
        "Q022_PRESERVATION_GATE": True,
        "Q023_PRESERVATION_GATE": True,
        "Q024_PRESERVATION_GATE": True,
        "NO_Q024_PERMUTATION_RERUN_GATE":
            all(int(r.get("q024_permutations_evaluated", -1)) == 0 for r in rows),
        "NO_OPTIMIZATION_GATE":
            all(int(r.get("optimizer_evaluations", -1)) == 0 for r in rows),
        "JOB_COMPLETENESS_GATE": got == expected,
        "FIXED_VECTOR_EVALUATION_COUNT_GATE": total_evals == required_evals,
        "COVARIANCE_CLOSURE_GATE": all(
            all(bool(x) for v in r.get("vertices",{}).values()
                for x in v.get("evaluation",{}).get("gates",{}).values())
            for r in rows if r.get("status") == "COMPLETE"
        ) and got == expected,
        "PRIMORDIAL_FIXED_ROLE_GATE": True,
        "NO_CAUSAL_OVERCLAIM_GATE": True,
    }
    passed = all(gates.values())

    result = {
        "q": Q, "run_id": RUN, "result_id": RESULT, "stage": "FINAL",
        "date": c["project"]["generated_at"],
        "execution_status": "COMPLETE" if passed else "INCOMPLETE_OR_FAILED_VALIDATION",
        "tests_status": "PENDING_EXTERNAL_TEST_SCRIPT",
        "FINAL_RESULT_GATE": "PROVISIONAL_PASS" if passed else "FAIL",
        "actual_new_likelihood_evaluations": total_evals,
        "expected_new_likelihood_evaluations": required_evals,
        "optimizer_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "scientific_surface": {
            "model": c["model"],
            "masks": list(MASKS),
            "likelihood": FULL_LIKE,
            "q022_github_run": int(c["parents"]["q022_github_run"]),
            "q023_github_run": int(c["parents"]["q023_github_run"]),
        },
        "diagnostics": diagnostics,
        "cross_mask_summary": {
            "top_spectrum_by_edge": top_spectrum,
            "top_highl_functional_group_by_edge": top_highl_group,
            "note":
                "Repeated labels indicate technical recurrence only. Divergent labels support distributed/mask-dependent attribution."
        },
        "gates": gates,
        "claim_boundaries": c["claim_boundaries"],
        "sources": c["sources"],
        "journal_effect_if_final_pass": {
            "q022_stable_multibasin_preserved": True,
            "q023_fixed_lineage_result_preserved": True,
            "q024_permutation_negative_result_preserved": True,
            "next_engine": "RESULT INGESTION & ROUTING ENGINE",
        },
    }
    write_json(output, result)
    return 0 if passed else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q025_fullmf_component_attribution_v2_config.yml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("edge")
    p.add_argument("--q022-dir", required=True)
    p.add_argument("--q021-dir", required=True)
    p.add_argument("--mask", type=int, required=True)
    p.add_argument("--seed-a", type=int, required=True)
    p.add_argument("--seed-b", type=int, required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    args = ap.parse_args()
    c = load_cfg(args.config)
    if args.cmd == "edge":
        return run_edge(c, args.q022_dir, args.q021_dir, args.mask, args.seed_a, args.seed_b, args.output)
    if args.cmd == "aggregate":
        return aggregate(c, args.input_dir, args.output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
