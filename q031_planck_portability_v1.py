#!/usr/bin/env python3
"""
Bubbleverse CASE-031 — independent Planck-likelihood portability V1.

CURRENT_Q: CASE-031

This executable performs a pre-registered, cross-implementation falsification
of the Q021-Q030 Planck n=3 EDE likelihood geometry using independent HiLLiPoP
PR4/NPIPE provenance.

Scientific boundaries:
- Same frozen MOD-EDE-N3 / class_ede backend.
- Independent high-l likelihood: planck_2020_hillipop.TTTEEE only.
- Q022 endpoints are mapped STARTS, not observations and not HiLLiPoP masks.
- CamSpec-only nuisance coordinates are never forced into HiLLiPoP.
- Absolute objective values are compared only WITHIN the same HiLLiPoP
  construction. No cross-likelihood chi2 subtraction or summation occurs.
- Stable optimizer basins are likelihood geometry, not physical universes.
- Shapley/Mobius and coordinate-switch interactions are non-causal diagnostics.
- Implementation failure is never converted into scientific non-portability.

Commands:
  preflight
  profile
  assess-primary
  aggregate-primary
  hybrid-profile
  aggregate-hybrid
  support-audit
  finalize
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import signal
import statistics
import textwrap
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
Q = "CASE-031"
RUN = "CASE031-PLANCK-LIKELIHOOD-PORTABILITY-V1"
RESULT = "R-CASE031-EDE-PLANCK-PORTABILITY-001"
COMPONENT = "planck_2020_hillipop.TTTEEE"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"

CAMSPEC_NUISANCE = (
    "A_planck", "calTE", "calEE",
    "amp_143", "amp_217", "amp_143x217",
    "n_143", "n_217", "n_143x217",
)

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

def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()

def load_cfg(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    if c["model"]["name"] != "MOD-EDE-N3" or int(c["model"]["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if c["model"]["backend_commit"] != BACKEND_COMMIT:
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    il = c["independent_likelihood"]
    if il["component"] != COMPONENT or il["commit"] != HILLIPOP_COMMIT:
        raise RuntimeError("INDEPENDENT_LIKELIHOOD_IDENTITY_GATE=FAIL")
    required_rules = (
        "independent_provenance_mandatory",
        "same_physics_backend",
        "no_cross_likelihood_chi2_sum",
        "no_cross_likelihood_absolute_objective_subtraction",
        "no_forced_nuisance_mapping",
        "source_masks_are_start_labels_only",
        "implementation_failure_separate_from_scientific_nonportability",
        "technical_failure_not_scientific_falsification",
    )
    if not all(c["rules"].get(k) is True for k in required_rules):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c

def load_source_lock(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / "q031_source_lock_v1.json"
    d = read_json(p)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d["independent_likelihood"]["commit"] != c["independent_likelihood"]["commit"]:
        raise RuntimeError("SOURCE_LOCK_HILLIPOP_GATE=FAIL")
    if d["bubbleverse"]["backend"]["commit"] != c["model"]["backend_commit"]:
        raise RuntimeError("SOURCE_LOCK_BACKEND_GATE=FAIL")
    return d

def load_protocol(c: Mapping[str, Any]) -> dict[str, Any]:
    p = ROOT / "q031_protocol_lock_v1.json"
    d = read_json(p)
    if d.get("q") != Q or d.get("run_id") != RUN:
        raise RuntimeError("PROTOCOL_IDENTITY_GATE=FAIL")
    declared = d.get("protocol_sha256")
    x = dict(d)
    x.pop("protocol_sha256", None)
    calc = canonical_hash(x)
    if declared != calc:
        raise RuntimeError(f"PROTOCOL_HASH_GATE=FAIL declared={declared} calculated={calc}")
    if d["independent_likelihood"]["commit"] != c["independent_likelihood"]["commit"]:
        raise RuntimeError("PROTOCOL_LIKELIHOOD_GATE=FAIL")
    return d

def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)

def ref_value(spec: Any) -> float | None:
    if not isinstance(spec, Mapping):
        return None
    r = spec.get("ref")
    if finite(r):
        return float(r)
    if isinstance(r, Mapping):
        for k in ("loc", "mean"):
            if finite(r.get(k)):
                return float(r[k])
    pr = spec.get("prior")
    if isinstance(pr, Mapping):
        for k in ("loc", "mean"):
            if finite(pr.get(k)):
                return float(pr[k])
        if finite(pr.get("min")) and finite(pr.get("max")):
            return 0.5 * (float(pr["min"]) + float(pr["max"]))
    return None

def set_ref(params: dict[str, Any], name: str, value: float) -> None:
    if name not in params or not isinstance(params[name], Mapping):
        return
    spec = copy.deepcopy(params[name])
    if not sampled(spec):
        return
    x = float(value)
    pr = spec.get("prior", {})
    if isinstance(pr, Mapping) and finite(pr.get("min")) and finite(pr.get("max")):
        lo, hi = float(pr["min"]), float(pr["max"])
        eps = max(1e-12, (hi - lo) * 1e-8)
        x = min(max(x, lo + eps), hi - eps)
    r = spec.get("ref")
    if isinstance(r, Mapping):
        rr = dict(r)
        if "loc" in rr:
            rr["loc"] = x
        elif "mean" in rr:
            rr["mean"] = x
        else:
            rr["loc"] = x
        spec["ref"] = rr
    else:
        spec["ref"] = x
    params[name] = spec

def gaussian_shape(name: str, mean: float, sigma: float):
    def f(**kwargs):
        z = (float(kwargs[name]) - float(mean)) / float(sigma)
        return -0.5 * z * z
    f.__name__ = f"q031_shape_{name}"
    return {"external": f, "input_params": [name]}

def load_hillipop_native_params() -> dict[str, Any]:
    import planck_2020_hillipop
    pkg = Path(planck_2020_hillipop.__file__).resolve().parent
    merged: dict[str, Any] = {}
    for name in ("params_calib.yaml", "params_TT.yaml", "params_TE.yaml", "params_EE.yaml"):
        p = pkg / name
        if not p.exists():
            raise RuntimeError(f"HILLIPOP_PARAM_FILE_GATE=FAIL missing={p}")
        text = textwrap.dedent(p.read_text(encoding="utf-8"))
        d = yaml.safe_load(text) or {}
        if not isinstance(d, Mapping):
            raise RuntimeError(f"HILLIPOP_PARAM_PARSE_GATE=FAIL file={name}")
        for k, v in d.items():
            if k in merged and canonical_hash(merged[k]) != canonical_hash(v):
                # Duplicate TE/EE dust declarations are expected to be identical.
                raise RuntimeError(f"HILLIPOP_DUPLICATE_PARAM_GATE=FAIL param={k}")
            merged[str(k)] = copy.deepcopy(v)
    return merged

def build_info(c: Mapping[str, Any], prefix: Path,
               max_evals: int, rhoend: float,
               seed: Mapping[str, float] | None = None,
               fixed: Mapping[str, float] | None = None) -> dict[str, Any]:
    """
    Reuse the frozen Bubbleverse class_ede constructor, replace CamSpec by
    independently sourced HiLLiPoP, restore exact HiLLiPoP-native nuisance
    declarations, and express every native Gaussian constraint as a
    normalization-free likelihood shape while minimizer prior densities are
    ignored. Hard support is preserved.
    """
    import q019_planck_cosmology_reprofile_v1 as q19

    q19cfg = q19.load_cfg(ROOT / "q019_planck_cosmology_reprofile_v1_config.yml")
    info = q19.build_full(
        q19cfg, "reference_free_h0", 0, prefix, seed={}
    )

    # Remove CamSpec-only nuisance declarations. A_planck is then reintroduced
    # from HiLLiPoP's own upstream defaults, not copied from CamSpec.
    params = info.setdefault("params", {})
    for name in CAMSPEC_NUISANCE:
        params.pop(name, None)

    native = load_hillipop_native_params()
    for name, spec in native.items():
        params[name] = copy.deepcopy(spec)

    info["likelihood"] = {COMPONENT: None}
    for name, spec in c["normalization_free_gaussian_shapes"].items():
        info["likelihood"][f"q031_shape_{name}"] = gaussian_shape(
            name, float(spec["mean"]), float(spec["sigma"])
        )

    info["prior"] = {}
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim["method"] = "bobyqa"
    minim["ignore_prior"] = True
    minim["best_of"] = 1
    minim["max_evals"] = int(max_evals)
    minim.setdefault("override_bobyqa", {})["rhoend"] = float(rhoend)

    if seed:
        for name, value in seed.items():
            if finite(value):
                set_ref(params, str(name), float(value))

    if fixed:
        for name, value in fixed.items():
            if name not in params:
                raise RuntimeError(f"FIXED_PARAMETER_GATE=FAIL missing={name}")
            params[name] = float(value)

    info["output"] = str(prefix.resolve())
    info["force"] = True
    return info

def reference_vector(info: Mapping[str, Any],
                     preferred: Mapping[str, float] | None = None) -> dict[str, float]:
    preferred = preferred or {}
    out: dict[str, float] = {}
    missing = []
    for name, spec in info.get("params", {}).items():
        if not sampled(spec):
            continue
        if name in preferred and finite(preferred[name]):
            out[name] = float(preferred[name])
            continue
        r = ref_value(spec)
        if r is None:
            missing.append(name)
        else:
            out[name] = float(r)
    if missing:
        raise RuntimeError("REFERENCE_VECTOR_GATE=FAIL " + repr(sorted(missing)))
    return out

def source_endpoints(c: Mapping[str, Any], q021_dir: str | Path,
                     q022_dir: str | Path) -> dict[str, dict[str, Any]]:
    import q025_fullmf_component_attribution_v2 as q25

    q25cfg = q25.load_cfg(ROOT / c["parents"]["q025"]["config"])
    final22 = q25.load_q022_final(q022_dir)
    if final22.get("result_id") != c["parents"]["q022"]["result_id"]:
        raise RuntimeError("Q022_PARENT_RESULT_GATE=FAIL")
    out: dict[str, dict[str, Any]] = {}
    for mask in c["primary_multistart"]["source_start_labels"]["masks"]:
        for seed in c["primary_multistart"]["source_start_labels"]["seed_restarts"]:
            ep = q25.load_q022_endpoint(
                q022_dir, q021_dir, final22, int(mask), int(seed)
            )
            p = ep.get("params", {})
            if not isinstance(p, Mapping):
                raise RuntimeError("Q022_ENDPOINT_PARAMS_GATE=FAIL")
            label = f"M{int(mask)}-S{int(seed)}"
            out[label] = {
                "mask": int(mask),
                "seed_restart": int(seed),
                "source_semantics": "Q022_START_PROVENANCE_ONLY_NOT_HILLIPOP_MASK",
                "params": {str(k): float(v) for k, v in p.items() if finite(v)},
            }
    if len(out) != 9:
        raise RuntimeError("Q022_NINE_START_GATE=FAIL")
    return out

def locked_scales(c: Mapping[str, Any],
                  starts: Mapping[str, Mapping[str, Any]]) -> dict[str, float]:
    """
    Freeze geometry scales from Q022 source endpoints BEFORE HiLLiPoP results.
    For Q022-profiled parameters and A_planck use the Q022 within-source-mask
    pair-difference semantics. Primordial scales use all nine source endpoints
    because those coordinates were fixed within a Q022 mask.
    """
    floor = float(c["pre_registered_geometry"]["q022_style_scale_floor_fraction"])
    profiled = set(c["cosmology"]["q022_profiled_common"]) | {"A_planck"}
    direction = list(c["cosmology"]["direction_common"])
    rows = list(starts.values())
    result: dict[str, float] = {}

    for name in direction:
        diffs: list[float] = []
        vals: list[float] = []
        if name in profiled:
            bymask: dict[int, list[float]] = {}
            for r in rows:
                p = r["params"]
                if name in p:
                    vals.append(float(p[name]))
                    bymask.setdefault(int(r["mask"]), []).append(float(p[name]))
            for vv in bymask.values():
                for a, b in combinations(vv, 2):
                    d = abs(a - b)
                    if d > 0:
                        diffs.append(d)
        else:
            for r in rows:
                p = r["params"]
                if name in p:
                    vals.append(float(p[name]))
            for a, b in combinations(vals, 2):
                d = abs(a - b)
                if d > 0:
                    diffs.append(d)

        if diffs:
            s = float(statistics.median(diffs))
        elif vals:
            span = max(vals) - min(vals)
            med = float(statistics.median(vals))
            s = span if span > 0 else max(abs(med) * floor, floor)
        else:
            raise RuntimeError(f"SCALE_SOURCE_GATE=FAIL missing={name}")
        result[name] = max(float(s), floor)
    return result

def metric_rms(a: Mapping[str, Any], b: Mapping[str, Any],
               names: Sequence[str], scales: Mapping[str, float]) -> float:
    vals = []
    for n in names:
        if finite(a.get(n)) and finite(b.get(n)) and finite(scales.get(n)) and float(scales[n]) > 0:
            vals.append((float(a[n]) - float(b[n])) / float(scales[n]))
    if not vals:
        return math.inf
    return float(math.sqrt(sum(x*x for x in vals) / len(vals)))

def native_nuisance_rms(c: Mapping[str, Any], a: Mapping[str, Any],
                        b: Mapping[str, Any]) -> float:
    vals = []
    for n in c["native_nuisance"]["sampled"]:
        s = c["native_nuisance"]["proposal_scales"].get(n)
        if finite(a.get(n)) and finite(b.get(n)) and finite(s) and float(s) > 0:
            vals.append((float(a[n]) - float(b[n])) / float(s))
    if not vals:
        return math.inf
    return float(math.sqrt(sum(x*x for x in vals) / len(vals)))

def preflight(c: Mapping[str, Any], q021_dir: str | Path,
              q022_dir: str | Path, output: str | Path) -> int:
    src = load_source_lock(c)
    protocol = load_protocol(c)
    starts = source_endpoints(c, q021_dir, q022_dir)
    mapped = list(c["primary_multistart"]["mapped_start_parameters"])
    for label, rec in starts.items():
        missing = [n for n in mapped if n not in rec["params"]]
        if missing:
            raise RuntimeError(f"MAPPED_START_COMPLETENESS_GATE=FAIL {label} {missing}")

    scales = locked_scales(c, starts)

    # Verify exact external source checkout at runtime.
    hill = ROOT / "external" / "hillipop"
    if not (hill / ".git").exists():
        raise RuntimeError("HILLIPOP_REPOSITORY_GATE=FAIL")
    import subprocess
    head = subprocess.check_output(["git", "-C", str(hill), "rev-parse", "HEAD"],
                                   text=True).strip()
    if head != HILLIPOP_COMMIT:
        raise RuntimeError("HILLIPOP_COMMIT_GATE=FAIL")

    # One real model/likelihood evaluation: technical capability gate only.
    first = starts[sorted(starts)[0]]["params"]
    info = build_info(
        c, ROOT / "q031_preflight_smoke",
        max_evals=1, rhoend=float(c["primary_multistart"]["stage1"]["rhoend"]),
        seed=first
    )
    native_expected = set(c["native_nuisance"]["sampled"])
    missing_native = sorted(native_expected - set(info["params"]))
    if missing_native:
        raise RuntimeError("HILLIPOP_NATIVE_NUISANCE_GATE=FAIL " + repr(missing_native))

    model_info = copy.deepcopy(info)
    for k in ("sampler", "output", "force"):
        model_info.pop(k, None)
    from cobaya.model import get_model
    model = get_model(model_info)
    vec = reference_vector(info, first)
    lp = model.logposterior(vec)
    x = getattr(lp, "logpost", lp)
    if not finite(x):
        raise RuntimeError("REFERENCE_EVALUATION_GATE=FAIL")
    try:
        if hasattr(model, "close"):
            model.close()
    except Exception:
        pass

    runtime = {}
    rp = ROOT / "q031_runtime" / "q031_runtime_provenance_v1.json"
    if rp.exists():
        runtime = read_json(rp)

    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q031_PREFLIGHT",
        "status": "PASS",
        "implementation_failure": False,
        "actual_scientific_portability_result": False,
        "source_lock_sha256": canonical_hash(src),
        "protocol_sha256": protocol["protocol_sha256"],
        "hillipop_commit": head,
        "component": COMPONENT,
        "q022_source_starts": starts,
        "mapped_start_parameters": mapped,
        "locked_common_scales": scales,
        "locked_scales_hash": canonical_hash(scales),
        "native_nuisance_proposal_scales": c["native_nuisance"]["proposal_scales"],
        "reference_evaluation_finite": True,
        "runtime_provenance": runtime,
        "claim_boundaries": {
            "q022_masks_are_hillipop_masks": False,
            "cross_likelihood_absolute_objectives_compared": False,
            "forced_nuisance_mapping": False,
        },
    }
    write_json(output, rec)
    print("Q031_PREFLIGHT_GATE=PASS")
    return 0

def load_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("stage") != "Q031_PREFLIGHT":
        raise RuntimeError("PREFLIGHT_IDENTITY_GATE=FAIL")
    if d.get("status") != "PASS":
        raise RuntimeError("PREFLIGHT_STATUS_GATE=FAIL")
    return d

def find_profile(root: str | Path, stage: str, mask: int, seed: int) -> dict[str, Any]:
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage
            and int(d.get("source_mask", -1)) == int(mask)
            and int(d.get("source_seed", -1)) == int(seed)
            and d.get("status") == "COMPLETE"):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(f"PROFILE_UNIQUENESS_GATE=FAIL stage={stage} mask={mask} seed={seed} hits={len(hits)}")
    return hits[0]

def run_profile(c: Mapping[str, Any], preflight_path: str | Path,
                phase: str, mask: int, seed: int,
                output: str | Path,
                stage1_dir: str | Path | None = None) -> int:
    pf = load_preflight(preflight_path)
    label = f"M{mask}-S{seed}"
    if label not in pf["q022_source_starts"]:
        raise RuntimeError("SOURCE_START_LABEL_GATE=FAIL")

    if phase == "stage1":
        start = dict(pf["q022_source_starts"][label]["params"])
        settings = c["primary_multistart"]["stage1"]
        stage_name = "Q031_PRIMARY_STAGE1"
        seed_semantics = "MAPPED_Q022_ENDPOINT"
    elif phase == "refinement":
        if stage1_dir is None:
            raise RuntimeError("REFINEMENT_PARENT_GATE=FAIL")
        parent = find_profile(stage1_dir, "Q031_PRIMARY_STAGE1", mask, seed)
        start = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
        settings = c["primary_multistart"]["refinement"]
        stage_name = "Q031_PRIMARY_REFINEMENT"
        seed_semantics = "EXACT_STAGE1_HILLIPOP_MINIMUM"
    else:
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": stage_name,
        "phase": phase,
        "source_mask": int(mask),
        "source_seed": int(seed),
        "source_label": label,
        "source_semantics": "START_PROVENANCE_ONLY_NOT_HILLIPOP_MASK",
        "seed_semantics": seed_semantics,
        "status": "FAILED",
        "actual_computed_result": False,
        "component": COMPONENT,
        "hillipop_commit": HILLIPOP_COMMIT,
        "backend_commit": BACKEND_COMMIT,
        "objective_basis": c["objective"]["basis"],
    }

    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info = build_info(
            c, prefix,
            max_evals=int(settings["max_evals"]),
            rhoend=float(settings["rhoend"]),
            seed=start
        )
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        rec.update({
            "status": "COMPLETE",
            "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
            "minimizer": {
                "max_evals": int(settings["max_evals"]),
                "rhoend": float(settings["rhoend"]),
                "best_of": 1,
                "ignore_prior": True,
            },
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED",
                    "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                    "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2

def collect_primary(root: str | Path, stage: str) -> list[dict[str, Any]]:
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage:
            out.append(d)
    return out

def common_geometry_names(c: Mapping[str, Any]) -> list[str]:
    return list(c["cosmology"]["q022_profiled_common"]) + ["A_planck"]

def endpoint_of(row: Mapping[str, Any]) -> Mapping[str, Any]:
    x = row.get("minimum", {})
    return x if isinstance(x, Mapping) else {}

def cluster_rows(c: Mapping[str, Any], rows: Sequence[Mapping[str, Any]],
                 scales: Mapping[str, float]) -> dict[str, Any]:
    rr = [r for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
    rr = sorted(rr, key=lambda r: str(r.get("source_label")))
    n = len(rr)
    names = common_geometry_names(c)
    dtol = float(c["pre_registered_geometry"]["collapse_common_endpoint_rms"])
    otol = float(c["pre_registered_geometry"]["collapse_objective_tolerance"])

    adjacency = {i: set() for i in range(n)}
    pairwise = []
    for i, j in combinations(range(n), 2):
        a, b = rr[i], rr[j]
        d = metric_rms(endpoint_of(a), endpoint_of(b), names, scales)
        od = abs(float(a["objective_chi2"]) - float(b["objective_chi2"]))
        same = d <= dtol and od <= otol
        if same:
            adjacency[i].add(j)
            adjacency[j].add(i)
        pairwise.append({
            "a": a["source_label"], "b": b["source_label"],
            "common_rms": d, "delta_objective": od,
            "same_basin_edge": bool(same)
        })

    seen = set()
    comps = []
    for i in range(n):
        if i in seen:
            continue
        stack = [i]
        comp = []
        while stack:
            k = stack.pop()
            if k in seen:
                continue
            seen.add(k)
            comp.append(k)
            stack.extend(adjacency[k] - seen)
        comps.append(sorted(comp))

    min_support = int(c["pre_registered_geometry"]["stable_basin_minimum_supporting_starts"])
    clusters = []
    for ci, idxs in enumerate(comps):
        members = [rr[i] for i in idxs]
        rep = min(members, key=lambda r: (float(r["objective_chi2"]), str(r["source_label"])))
        clusters.append({
            "cluster_id": ci,
            "support": len(members),
            "stable": len(members) >= min_support,
            "members": [m["source_label"] for m in members],
            "objective_min": float(min(float(m["objective_chi2"]) for m in members)),
            "objective_max": float(max(float(m["objective_chi2"]) for m in members)),
            "representative_source": rep["source_label"],
            "representative": rep,
        })

    stable = [x for x in clusters if x["stable"]]
    return {
        "complete_rows": n,
        "clusters": clusters,
        "stable_basin_count": len(stable),
        "stable_cluster_ids": [x["cluster_id"] for x in stable],
        "pairwise": pairwise,
        "single_cluster_covers_all": len(clusters) == 1 and n > 0,
    }

def assess_primary(c: Mapping[str, Any], preflight_path: str | Path,
                   stage1_dir: str | Path, output: str | Path,
                   matrix_output: str | Path) -> int:
    pf = load_preflight(preflight_path)
    rows = collect_primary(stage1_dir, "Q031_PRIMARY_STAGE1")
    expected = {(int(m), int(s))
                for m in c["primary_multistart"]["source_start_labels"]["masks"]
                for s in c["primary_multistart"]["source_start_labels"]["seed_restarts"]}
    got = {(int(r["source_mask"]), int(r["source_seed"]))
           for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))}
    complete = got == expected and len(got) == 9
    if not complete:
        rec = {
            "q": Q, "run_id": RUN, "stage": "Q031_PRIMARY_STAGE1_ASSESSMENT",
            "status": "FAIL", "STAGE1_JOB_COMPLETENESS_GATE": "FAIL",
            "expected": sorted(expected), "got": sorted(got),
            "needs_refinement": False,
        }
        write_json(output, rec)
        write_json(matrix_output, {"include": [{"mask": -1, "seed": -1}]})
        return 2

    diag = cluster_rows(c, rows, pf["locked_common_scales"])
    needs = not bool(diag["single_cluster_covers_all"])
    matrix = {"include": [
        {"mask": int(m), "seed": int(s)}
        for m, s in sorted(expected)
    ]} if needs else {"include": [{"mask": -1, "seed": -1}]}

    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q031_PRIMARY_STAGE1_ASSESSMENT",
        "status": "PASS",
        "STAGE1_JOB_COMPLETENESS_GATE": "PASS",
        "needs_refinement": needs,
        "reason": (
            "CANDIDATE_MULTIBASIN_OR_FRAGMENTED_GEOMETRY"
            if needs else
            "ALL_NINE_MAPPED_STARTS_COLLAPSE_TO_ONE_PRE_REGISTERED_BASIN"
        ),
        "diagnostic": diag,
        "refinement_seed_semantics": "EXACT_MATCHED_STAGE1_HILLIPOP_MINIMUM",
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if needs else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0

def unit_vector(a: Mapping[str, Any], b: Mapping[str, Any],
                names: Sequence[str], scales: Mapping[str, float]) -> np.ndarray:
    v = []
    for n in names:
        if not (finite(a.get(n)) and finite(b.get(n)) and finite(scales.get(n))):
            raise RuntimeError(f"DIRECTION_PARAMETER_GATE=FAIL {n}")
        v.append((float(b[n]) - float(a[n])) / float(scales[n]))
    x = np.asarray(v, dtype=float)
    norm = float(np.linalg.norm(x))
    if norm <= 0:
        raise RuntimeError("ZERO_DIRECTION_GATE=FAIL")
    return x / norm

def direction_diagnostic(c: Mapping[str, Any],
                         stable_clusters: Sequence[Mapping[str, Any]],
                         scales: Mapping[str, float]) -> dict[str, Any]:
    minimum = int(c["direction_test"]["minimum_stable_basins_for_test"])
    if len(stable_clusters) < minimum:
        return {
            "status": "NOT_TESTABLE",
            "reason": f"stable_basin_count={len(stable_clusters)} < {minimum}",
            "no_single_universal_direction_gate": "NOT_TESTABLE",
        }

    reps = [x["representative"] for x in stable_clusters]
    names = list(c["cosmology"]["direction_common"])
    edges = []
    vectors = []
    for i, j in combinations(range(len(reps)), 2):
        u = unit_vector(endpoint_of(reps[i]), endpoint_of(reps[j]), names, scales)
        label = f"C{stable_clusters[i]['cluster_id']}-C{stable_clusters[j]['cluster_id']}"
        edges.append(label)
        vectors.append(u)

    cosines = []
    for i, j in combinations(range(len(vectors)), 2):
        cs = abs(float(np.dot(vectors[i], vectors[j])))
        cosines.append({"edge_a": edges[i], "edge_b": edges[j], "abs_cosine": cs})
    vals = [x["abs_cosine"] for x in cosines]
    med = float(statistics.median(vals)) if vals else 1.0
    floor = float(c["direction_test"]["pairwise_abs_cosine_floor"])
    medthr = float(c["direction_test"]["median_abs_cosine_threshold"])
    npass = sum(v >= floor for v in vals)
    universal = med >= medthr and npass >= int(c["direction_test"]["minimum_pairwise_passes"])
    return {
        "status": "PASS",
        "edge_labels": edges,
        "pairwise_abs_cosines": cosines,
        "median_abs_cosine": med,
        "pairwise_floor": floor,
        "median_threshold": medthr,
        "pairwise_passes": npass,
        "universal_direction": bool(universal),
        "no_single_universal_direction_gate": "PASS" if not universal else "FAIL",
    }

def choose_representative_pair(c: Mapping[str, Any],
                               stable: Sequence[Mapping[str, Any]],
                               scales: Mapping[str, float]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if len(stable) < 2:
        raise RuntimeError("REPRESENTATIVE_PAIR_GATE=FAIL")
    names = common_geometry_names(c)
    candidates = []
    for a, b in combinations(stable, 2):
        ra, rb = a["representative"], b["representative"]
        d = metric_rms(endpoint_of(ra), endpoint_of(rb), names, scales)
        osum = float(ra["objective_chi2"]) + float(rb["objective_chi2"])
        key = tuple(sorted((str(ra["source_label"]), str(rb["source_label"]))))
        candidates.append((d, -osum, tuple(reversed(key)), a, b))
    # Explicit sort rather than tuple max with mapping objects.
    candidates = sorted(
        candidates,
        key=lambda x: (-x[0], -x[1], sorted((
            str(x[3]["representative"]["source_label"]),
            str(x[4]["representative"]["source_label"])
        )))
    )
    a, b = candidates[0][3], candidates[0][4]
    ra, rb = a["representative"], b["representative"]
    common = metric_rms(endpoint_of(ra), endpoint_of(rb), names, scales)
    nuis = native_nuisance_rms(c, endpoint_of(ra), endpoint_of(rb))
    od = abs(float(ra["objective_chi2"]) - float(rb["objective_chi2"]))
    diag = {
        "cluster_a": a["cluster_id"], "cluster_b": b["cluster_id"],
        "source_a": ra["source_label"], "source_b": rb["source_label"],
        "common_rms": common,
        "native_nuisance_rms": nuis,
        "delta_objective": od,
        "near_degenerate_separated_pair": bool(
            od <= float(c["pre_registered_geometry"]["near_degenerate_objective_tolerance"])
            and common > float(c["pre_registered_geometry"]["collapse_common_endpoint_rms"])
        ),
        "compensation_gate": bool(
            common > float(c["pre_registered_geometry"]["compensation_common_rms_threshold"])
            and nuis > float(c["pre_registered_geometry"]["compensation_native_nuisance_rms_threshold"])
        ),
    }
    return ra, rb, diag

def aggregate_primary(c: Mapping[str, Any], preflight_path: str | Path,
                      stage1_dir: str | Path, assessment_path: str | Path,
                      refinement_dir: str | Path | None,
                      output: str | Path) -> int:
    pf = load_preflight(preflight_path)
    ass = read_json(assessment_path)
    if ass.get("status") != "PASS":
        raise RuntimeError("PRIMARY_ASSESSMENT_GATE=FAIL")
    needs = bool(ass.get("needs_refinement"))
    if needs:
        if refinement_dir is None:
            raise RuntimeError("REFINEMENT_DIR_GATE=FAIL")
        rows = collect_primary(refinement_dir, "Q031_PRIMARY_REFINEMENT")
        decision_phase = "refinement"
    else:
        rows = collect_primary(stage1_dir, "Q031_PRIMARY_STAGE1")
        decision_phase = "stage1"

    expected = 9
    complete = [r for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
    if len(complete) != expected:
        raise RuntimeError(f"PRIMARY_COMPLETENESS_GATE=FAIL {len(complete)}/{expected}")

    diag = cluster_rows(c, complete, pf["locked_common_scales"])
    stable = [x for x in diag["clusters"] if x["stable"]]
    multibasin = len(stable) >= 2
    rep_pair = None
    endpoint_a = None
    endpoint_b = None
    if multibasin:
        ra, rb, rep_pair = choose_representative_pair(c, stable, pf["locked_common_scales"])
        endpoint_a = ra
        endpoint_b = rb

    direction = direction_diagnostic(c, stable, pf["locked_common_scales"])

    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q031_PRIMARY_FINAL",
        "status": "PASS",
        "actual_computed_result": True,
        "implementation_valid_at_primary_stage": True,
        "decision_phase": decision_phase,
        "primary_multistart_complete": True,
        "stable_multibasin_gate": "PASS" if multibasin else "FAIL",
        "stable_basin_count": len(stable),
        "cluster_diagnostic": diag,
        "representative_pair": rep_pair,
        "representative_endpoint_a": endpoint_a,
        "representative_endpoint_b": endpoint_b,
        "direction_diagnostic": direction,
        "locked_common_scales_hash": pf["locked_scales_hash"],
        "claim_boundaries": {
            "stable_basins_are_physical_universes": False,
            "source_masks_are_hillipop_masks": False,
            "cross_likelihood_chi2_comparison": False,
        },
    }
    write_json(output, rec)
    print("HAS_MULTIBASIN=" + ("true" if multibasin else "false"))
    print("DIRECTION_STATUS=" + str(direction.get("no_single_universal_direction_gate")))
    return 0

def load_primary(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("stage") != "Q031_PRIMARY_FINAL":
        raise RuntimeError("PRIMARY_RESULT_IDENTITY_GATE=FAIL")
    if d.get("status") != "PASS":
        raise RuntimeError("PRIMARY_RESULT_STATUS_GATE=FAIL")
    return d

def representative_vectors(primary: Mapping[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    if primary.get("stable_multibasin_gate") != "PASS":
        raise RuntimeError("REPRESENTATIVE_MULTIBASIN_GATE=FAIL")
    a = primary["representative_endpoint_a"]["minimum"]
    b = primary["representative_endpoint_b"]["minimum"]
    A = {str(k): float(v) for k, v in a.items() if finite(v)}
    B = {str(k): float(v) for k, v in b.items() if finite(v)}
    return A, B

def midpoint(A: Mapping[str, float], B: Mapping[str, float]) -> dict[str, float]:
    return {k: 0.5 * (float(A[k]) + float(B[k]))
            for k in sorted(set(A) & set(B)) if finite(A[k]) and finite(B[k])}

def hybrid_fixed(A: Mapping[str, float], B: Mapping[str, float],
                 coords: Sequence[str], mask: int) -> dict[str, float]:
    if mask < 0 or mask >= (1 << len(coords)):
        raise RuntimeError("HYBRID_MASK_GATE=FAIL")
    out = {}
    for i, n in enumerate(coords):
        if n not in A or n not in B:
            raise RuntimeError(f"HYBRID_COORDINATE_GATE=FAIL {n}")
        out[n] = float(B[n] if (mask & (1 << i)) else A[n])
    return out

def run_hybrid_profile(c: Mapping[str, Any], primary_path: str | Path,
                       kind: str, mask: int, restart: int,
                       output: str | Path) -> int:
    primary = load_primary(primary_path)
    A, B = representative_vectors(primary)
    if kind == "primordial":
        coords = list(c["primordial_test"]["coordinates"])
        vertices = int(c["primordial_test"]["vertices"])
        max_evals = int(c["primordial_test"]["max_evals"])
        rhoend = float(c["primordial_test"]["rhoend"])
        stage = "Q031_PRIMORDIAL_PROFILE"
    elif kind == "coupling":
        coords = list(c["coupling_test"]["coordinates"])
        vertices = int(c["coupling_test"]["vertices"])
        max_evals = int(c["primordial_test"]["max_evals"])
        rhoend = float(c["primordial_test"]["rhoend"])
        stage = "Q031_COUPLING_PROFILE"
    else:
        raise RuntimeError("HYBRID_KIND_GATE=FAIL")
    if mask < 0 or mask >= vertices or restart not in (0, 1, 2):
        raise RuntimeError("HYBRID_JOB_IDENTITY_GATE=FAIL")

    seeds = [A, B, midpoint(A, B)]
    fixed = hybrid_fixed(A, B, coords, mask)
    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": stage, "kind": kind,
        "mask": int(mask), "restart": int(restart),
        "fixed_coordinates": fixed,
        "seed_semantics": ["REPRESENTATIVE_A", "REPRESENTATIVE_B", "MIDPOINT"][restart],
        "status": "FAILED", "actual_computed_result": False,
        "objective_basis": c["objective"]["basis"],
    }

    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        info = build_info(c, prefix, max_evals=max_evals, rhoend=rhoend,
                          seed=seeds[restart], fixed=fixed)
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_HYBRID_RESULT_GATE=FAIL")
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD",
                    "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2

def collect_hybrid(root: str | Path, kind: str) -> list[dict[str, Any]]:
    stage = "Q031_PRIMORDIAL_PROFILE" if kind == "primordial" else "Q031_COUPLING_PROFILE"
    rows = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage:
            rows.append(d)
    return rows

def popcount(x: int) -> int:
    return int(x).bit_count()

def shapley3(values: Mapping[int, float]) -> dict[str, float]:
    coords = ("n_s", "logA", "tau_reio")
    out = {}
    n = 3
    for i, name in enumerate(coords):
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

def mobius3(v: Mapping[int, float]) -> dict[str, float]:
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

def decompose3(values: Mapping[int, float], threshold: float) -> dict[str, Any]:
    mm = mobius3(values)
    sv = shapley3(values)
    total = float(values[7] - values[0])
    closure = float(sum(mm.values()) - total)
    abs_sum = sum(abs(x) for x in mm.values())
    frac = {k: (abs(v)/abs_sum if abs_sum else 0.0) for k, v in mm.items()}
    ranked = sorted(mm, key=lambda k: abs(mm[k]), reverse=True)
    top = ranked[0]
    topf = frac[top]
    if topf < threshold:
        cls = "DISTRIBUTED"
    elif "__x__" not in top:
        cls = "SINGLE"
    elif top.count("__x__") == 1:
        cls = "PAIR"
    else:
        cls = "THREE_WAY"
    indiv = sorted(("n_s", "logA", "tau_reio"),
                   key=lambda n: abs(sv[n]), reverse=True)
    return {
        "total_effect": total,
        "mobius_terms": mm,
        "mobius_abs_fraction": frac,
        "shapley_allocations": sv,
        "individual_shapley_abs_ranking": indiv,
        "n_s_is_largest_individual_shapley": indiv[0] == "n_s",
        "dominant_term": top,
        "dominant_abs_fraction": topf,
        "structure_class": cls,
        "closure_residual": closure,
        "interpretation": "FUNCTIONAL_GEOMETRY_NONCAUSAL",
    }

def aggregate_hybrid(c: Mapping[str, Any], kind: str,
                     input_dir: str | Path, output: str | Path) -> int:
    rows = collect_hybrid(input_dir, kind)
    if kind == "primordial":
        vertices = 8
        spread_tol = float(c["primordial_test"]["restart_objective_spread_max"])
        closure_tol = float(c["primordial_test"]["closure_abs_tolerance"])
        dom = float(c["primordial_test"]["dominant_abs_mobius_fraction_threshold"])
    elif kind == "coupling":
        vertices = 4
        spread_tol = float(c["coupling_test"]["restart_objective_spread_max"])
        closure_tol = float(c["coupling_test"]["closure_abs_tolerance"])
        dom = 0.5
    else:
        raise RuntimeError("AGGREGATE_HYBRID_KIND_GATE=FAIL")

    expected = {(m, r) for m in range(vertices) for r in (0, 1, 2)}
    complete = [r for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
    got = {(int(r["mask"]), int(r["restart"])) for r in complete}
    completeness = got == expected and len(complete) == len(expected)

    values: dict[int, float] = {}
    spreads = {}
    best_rows = {}
    for m in range(vertices):
        rr = sorted([r for r in complete if int(r["mask"]) == m],
                    key=lambda r: float(r["objective_chi2"]))
        if rr:
            values[m] = float(rr[0]["objective_chi2"])
            best_rows[str(m)] = rr[0]
        spreads[m] = (
            max(float(x["objective_chi2"]) for x in rr) -
            min(float(x["objective_chi2"]) for x in rr)
            if len(rr) == 3 else None
        )
    stability = completeness and all(v is not None and float(v) <= spread_tol for v in spreads.values())

    if kind == "primordial":
        diagnostic = decompose3(values, dom) if len(values) == 8 else {}
        restart_decomp = {}
        for ri in (0, 1, 2):
            rv = {}
            for m in range(8):
                hit = [x for x in complete if int(x["mask"]) == m and int(x["restart"]) == ri]
                if len(hit) == 1:
                    rv[m] = float(hit[0]["objective_chi2"])
            if len(rv) == 8:
                restart_decomp[str(ri)] = decompose3(rv, dom)
        ranking_stable = (
            len(restart_decomp) == 3
            and len({x["structure_class"] for x in restart_decomp.values()}) == 1
            and len({x["dominant_term"] for x in restart_decomp.values()}) == 1
        )
        closure = abs(float(diagnostic.get("closure_residual", math.inf))) <= closure_tol
        distributed = diagnostic.get("structure_class") == "DISTRIBUTED"
        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q031_PRIMORDIAL_FINAL",
            "status": "PASS" if completeness and stability and ranking_stable and closure else "FAIL",
            "actual_computed_result": completeness,
            "job_completeness_gate": completeness,
            "multistart_objective_stability_gate": stability,
            "multistart_ranking_stability_gate": ranking_stable,
            "decomposition_closure_gate": closure,
            "distributed_primordial_gate": "PASS" if distributed else "FAIL",
            "n_s_persistent_but_not_single": bool(
                diagnostic.get("n_s_is_largest_individual_shapley")
                and diagnostic.get("structure_class") != "SINGLE"
            ),
            "diagnostic": diagnostic,
            "restart_decompositions": restart_decomp,
            "vertex_spreads": {str(k): v for k, v in spreads.items()},
            "best_rows": best_rows,
        }
    else:
        if len(values) == 4:
            interaction = float(values[3] - values[1] - values[2] + values[0])
        else:
            interaction = math.nan
        resolved = finite(interaction) and abs(interaction) > float(
            c["coupling_test"]["inherited_numerical_resolution_floor"]
        )
        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q031_COUPLING_FINAL",
            "status": "PASS" if completeness and stability and finite(interaction) else "FAIL",
            "actual_computed_result": completeness,
            "job_completeness_gate": completeness,
            "multistart_objective_stability_gate": stability,
            "coordinates": c["coupling_test"]["coordinates"],
            "interaction_contrast": interaction,
            "resolved_above_inherited_q030_floor": bool(resolved),
            "resolution_floor": c["coupling_test"]["inherited_numerical_resolution_floor"],
            "gate_role": "SUPPORTING_NOT_CORE",
            "causal_interpretation": False,
            "vertex_spreads": {str(k): v for k, v in spreads.items()},
            "best_rows": best_rows,
        }
    write_json(output, rec)
    return 0 if rec["status"] == "PASS" else 2

def get_like_instance(model):
    try:
        return model.likelihood[COMPONENT]
    except Exception:
        for k in model.likelihood:
            if str(k) == COMPONENT or str(k).endswith("hillipop.TTTEEE"):
                return model.likelihood[k]
    raise RuntimeError("HILLIPOP_INSTANCE_GATE=FAIL")

def like_index_map(like) -> list[dict[str, Any]]:
    from copy import deepcopy
    rows = []
    idx = 0
    for mode in ("TT", "EE", "TE"):
        if not like._is_mode.get(mode, False):
            continue
        for xf in range(like._nxfreq):
            xs = like._xspec2xfreq.index(xf)
            lmin = int(like._lmins[mode][xs])
            lmax = int(like._lmaxs[mode][xs])
            wf = deepcopy(like.wf)
            wf.cut_binning(lmin, lmax)
            label = str(like._xfreq_labels()[xf]) if callable(like._xfreq_labels) else str(like._xfreq_labels[xf])
            for lo, hi in zip(wf.lmins, wf.lmaxs):
                rows.append({
                    "index": idx, "mode": mode, "xfreq": label,
                    "lmin": int(lo), "lmax": int(hi),
                })
                idx += 1
    if idx != len(like.delta_cl):
        raise RuntimeError(f"HILLIPOP_INDEX_MAP_GATE=FAIL mapped={idx} residual={len(like.delta_cl)}")
    return rows

def term(r: np.ndarray, P: np.ndarray, I: Sequence[int], J: Sequence[int]) -> float:
    ii = np.asarray(list(I), dtype=int)
    jj = np.asarray(list(J), dtype=int)
    if len(ii) == 0 or len(jj) == 0:
        return 0.0
    x = float(r[ii] @ P[np.ix_(ii, jj)] @ r[jj])
    if set(ii.tolist()) == set(jj.tolist()):
        return x
    return 2.0 * x

def support_audit(c: Mapping[str, Any], primary_path: str | Path,
                  output: str | Path) -> int:
    primary = load_primary(primary_path)
    rec: dict[str, Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q031_SUPPORT_AUDIT",
        "status": "UNAVAILABLE_NONCORE",
        "gate_role": "SUPPORTING_NOT_CORE",
        "causal_partition": False,
    }
    if primary.get("stable_multibasin_gate") != "PASS":
        rec.update({"reason": "NO_REPRESENTATIVE_MULTIBASIN_PAIR"})
        write_json(output, rec)
        return 0

    model = None
    try:
        A, B = representative_vectors(primary)
        info = build_info(c, ROOT / "q031_support_model", max_evals=1,
                          rhoend=float(c["primary_multistart"]["stage1"]["rhoend"]),
                          seed=A)
        model_info = copy.deepcopy(info)
        for k in ("sampler", "output", "force"):
            model_info.pop(k, None)
        from cobaya.model import get_model
        model = get_model(model_info)
        valsA = reference_vector(info, A)
        valsB = reference_vector(info, B)

        lpA = model.logposterior(valsA)
        like = get_like_instance(model)
        rA = np.asarray(like.delta_cl, dtype=float).copy()
        P = np.asarray(like._invkll, dtype=float).copy()
        index = like_index_map(like)

        lpB = model.logposterior(valsB)
        like = get_like_instance(model)
        rB = np.asarray(like.delta_cl, dtype=float).copy()
        if rA.shape != rB.shape or P.shape != (len(rA), len(rA)):
            raise RuntimeError("SUPPORT_DIMENSION_GATE=FAIL")

        chiA = float(rA @ P @ rA)
        chiB = float(rB @ P @ rB)
        freq_labels = sorted({x["xfreq"] for x in index})
        groups = {f: [x["index"] for x in index if x["xfreq"] == f] for f in freq_labels}

        pair_terms = {}
        closureA = 0.0
        closureB = 0.0
        for i, f1 in enumerate(freq_labels):
            for j in range(i, len(freq_labels)):
                f2 = freq_labels[j]
                a = term(rA, P, groups[f1], groups[f2])
                b = term(rB, P, groups[f1], groups[f2])
                closureA += a
                closureB += b
                pair_terms[f"{f1}__x__{f2}"] = {
                    "A": a, "B": b, "delta_B_minus_A": b-a
                }

        target1, target2 = c["residual_covariance_support_test"]["exact_pair_target"]
        target_key = f"{target1}__x__{target2}"
        if target_key not in pair_terms:
            # canonical order can differ
            target_key = f"{target2}__x__{target1}"
        if target_key not in pair_terms:
            raise RuntimeError("TARGET_FREQUENCY_PAIR_SUPPORT_GATE=FAIL")

        def partition(lo: int, hi: int):
            S = [x["index"] for x in index if x["lmin"] >= lo and x["lmax"] <= hi]
            R = [x["index"] for x in index if x["index"] not in set(S)]
            return {
                "range": [lo, hi], "dimension": len(S),
                "A_internal": term(rA, P, S, S),
                "A_cross_rest": term(rA, P, S, R),
                "B_internal": term(rB, P, S, S),
                "B_cross_rest": term(rB, P, S, R),
            }

        target_band = partition(*map(int, c["residual_covariance_support_test"]["multipole_target"]))
        low_band = partition(*map(int, c["residual_covariance_support_test"]["legacy_lowell_check_band"]))
        for d in (target_band, low_band):
            d["delta_internal"] = d["B_internal"] - d["A_internal"]
            d["delta_cross_rest"] = d["B_cross_rest"] - d["A_cross_rest"]
            d["delta_partition_associated"] = d["delta_internal"] + d["delta_cross_rest"]

        pair_rank = sorted(
            pair_terms,
            key=lambda k: abs(pair_terms[k]["delta_B_minus_A"]),
            reverse=True
        )
        floor = float(c["coupling_test"]["inherited_numerical_resolution_floor"])
        target_delta = float(pair_terms[target_key]["delta_B_minus_A"])
        closure_err = max(abs(closureA-chiA), abs(closureB-chiB))

        rec.update({
            "status": "PASS",
            "component": COMPONENT,
            "residual_dimension": len(rA),
            "raw_hillipop_chi2": {"A": chiA, "B": chiB, "delta": chiB-chiA},
            "frequency_pair_terms": pair_terms,
            "frequency_pair_exact_aggregation_closure": {
                "A_error": closureA-chiA,
                "B_error": closureB-chiB,
                "max_abs_error": closure_err,
            },
            "target_frequency_pair": {
                "key": target_key,
                "diagnostic": pair_terms[target_key],
                "absolute_delta_rank": pair_rank.index(target_key)+1,
                "number_of_pair_terms": len(pair_rank),
                "resolved_above_inherited_q030_floor": abs(target_delta) > floor,
            },
            "multipole_target": target_band,
            "legacy_600_999_check": low_band,
            "index_map_hash": canonical_hash(index),
            "interpretation": (
                "EXACT_PAIR_PRESERVING_QUADRATIC_DIAGNOSTIC; "
                "NO_UNIQUE_DATA_ONLY_OR_MODEL_ONLY_CAUSAL_ALLOCATION"
            ),
        })
    except Exception as exc:
        rec.update({"status": "UNAVAILABLE_NONCORE", "error": repr(exc)})
    finally:
        try:
            if model is not None and hasattr(model, "close"):
                model.close()
        except Exception:
            pass
    write_json(output, rec)
    return 0

def optional_json(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    p = Path(path)
    return read_json(p) if p.exists() else None

def finalize(c: Mapping[str, Any], preflight_path: str | Path,
             primary_path: str | Path,
             primordial_path: str | Path | None,
             coupling_path: str | Path | None,
             support_path: str | Path | None,
             output: str | Path) -> int:
    pf = load_preflight(preflight_path)
    primary = load_primary(primary_path)
    primordial = optional_json(primordial_path)
    coupling = optional_json(coupling_path)
    support = optional_json(support_path)

    implementation_valid = (
        pf.get("status") == "PASS"
        and primary.get("status") == "PASS"
        and primary.get("implementation_valid_at_primary_stage") is True
    )
    multibasin = primary.get("stable_multibasin_gate") == "PASS"

    core = {
        "INDEPENDENT_IMPLEMENTATION_GATE": "PASS" if implementation_valid else "FAIL",
        "MATERIAL_STABLE_MULTIBASIN_GATE": "PASS" if multibasin else "FAIL",
        "DISTRIBUTED_PRIMORDIAL_RESPONSE_GATE": "NOT_RUN",
        "NO_SINGLE_UNIVERSAL_BASIN_DIRECTION_GATE":
            primary.get("direction_diagnostic", {}).get("no_single_universal_direction_gate", "NOT_TESTABLE"),
        "CONSTRUCTION_DEPENDENT_COMPENSATION_GATE": "NOT_RUN",
    }

    if multibasin:
        core["CONSTRUCTION_DEPENDENT_COMPENSATION_GATE"] = (
            "PASS" if primary.get("representative_pair", {}).get("compensation_gate") is True else "FAIL"
        )
        if primordial is not None and primordial.get("status") == "PASS":
            core["DISTRIBUTED_PRIMORDIAL_RESPONSE_GATE"] = primordial.get(
                "distributed_primordial_gate", "FAIL"
            )
        else:
            core["DISTRIBUTED_PRIMORDIAL_RESPONSE_GATE"] = "UNRESOLVED"

    if not implementation_valid:
        verdict = "UNRESOLVED_IMPLEMENTATION_FAILURE"
        classification = "QUALIFY"
        geometry_class = "NOT_ESTABLISHED"
        scientific_nonportability = False
    elif not multibasin:
        verdict = "PORTABILITY_FAILS"
        classification = "DOWNGRADE"
        geometry_class = "IMPLEMENTATION-SPECIFIC INTERNAL LIKELIHOOD GEOMETRY"
        scientific_nonportability = True
    else:
        vals = [
            core["DISTRIBUTED_PRIMORDIAL_RESPONSE_GATE"],
            core["NO_SINGLE_UNIVERSAL_BASIN_DIRECTION_GATE"],
            core["CONSTRUCTION_DEPENDENT_COMPENSATION_GATE"],
        ]
        if all(v == "PASS" for v in vals):
            verdict = "PORTABILITY_SURVIVES"
            classification = "PRESERVE"
            geometry_class = "CROSS-IMPLEMENTATION PLANCK n=3 EDE LIKELIHOOD GEOMETRY"
            scientific_nonportability = False
        elif any(v == "NOT_TESTABLE" or v == "UNRESOLVED" or v == "NOT_RUN" for v in vals):
            verdict = "PORTABILITY_QUALIFIED"
            classification = "QUALIFY"
            geometry_class = "CROSS-IMPLEMENTATION STATUS PARTIALLY RESOLVED"
            scientific_nonportability = False
        else:
            verdict = "PORTABILITY_FAILS"
            classification = "DOWNGRADE"
            geometry_class = "IMPLEMENTATION-SPECIFIC INTERNAL LIKELIHOOD GEOMETRY"
            scientific_nonportability = True

    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q031_FINAL",
        "execution_status": "COMPLETE" if implementation_valid else "FAILED_OR_INCOMPLETE",
        "actual_computed_result": True,
        "validation_status": "PROVISIONAL_PENDING_q031_tests_v1",
        "FINAL_RESULT_GATE": "PROVISIONAL",
        "portability_verdict": verdict,
        "final_classification": classification,
        "geometry_classification": geometry_class,
        "scientific_nonportability": scientific_nonportability,
        "core_gates": core,
        "primary": primary,
        "primordial": primordial,
        "coupling_supporting": coupling,
        "residual_covariance_supporting": support,
        "non_comparable_quantities": [
            "absolute CamSpec versus HiLLiPoP objective constants",
            "CamSpec calTE/calEE versus HiLLiPoP map calibrations",
            "CamSpec amp_143/amp_217/amp_143x217/n_* versus HiLLiPoP foreground amplitudes",
            "Q022 source mask labels versus HiLLiPoP likelihood masks",
            "likelihood variants as independent observations",
        ],
        "claim_boundaries": {
            "physical_causality_claimed": False,
            "instrumental_systematic_proven": False,
            "new_physics_detected": False,
            "Shapley_causal": False,
            "nuisance_motion_is_systematic": False,
            "cross_likelihood_chi2_sum_performed": False,
        },
        "journal_effect": {
            "if_survives": "UPGRADE_TO_CROSS_IMPLEMENTATION_PLANCK_N3_EDE_LIKELIHOOD_GEOMETRY",
            "if_fails": "DOWNGRADE_Q021_Q030_TO_IMPLEMENTATION_SPECIFIC_INTERNAL_LIKELIHOOD_GEOMETRY",
            "if_qualified": "PRESERVE_Q021_Q030_INTERNAL_RESULTS_BUT_DO_NOT_GENERALIZE",
        },
        "return_route": "RESULT INGESTION & ROUTING ENGINE",
        "next_required_action": (
            "INGEST_VALIDATED_CASE031_RESULT"
            if implementation_valid else
            "REPAIR_IMPLEMENTATION_ONLY; DO_NOT ALTER SCIENTIFIC CLASSIFICATION"
        ),
    }
    write_json(output, rec)
    print("PORTABILITY_VERDICT=" + verdict)
    print("FINAL_CLASSIFICATION=" + classification)
    return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q031_planck_portability_v1_config.yml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight")
    p.add_argument("--q021-dir", required=True)
    p.add_argument("--q022-dir", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--preflight", required=True)
    p.add_argument("--phase", choices=["stage1", "refinement"], required=True)
    p.add_argument("--mask", type=int, required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--stage1-dir")
    p.add_argument("--output", required=True)

    p = sub.add_parser("assess-primary")
    p.add_argument("--preflight", required=True)
    p.add_argument("--stage1-dir", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--matrix-output", required=True)

    p = sub.add_parser("aggregate-primary")
    p.add_argument("--preflight", required=True)
    p.add_argument("--stage1-dir", required=True)
    p.add_argument("--assessment", required=True)
    p.add_argument("--refinement-dir")
    p.add_argument("--output", required=True)

    p = sub.add_parser("hybrid-profile")
    p.add_argument("--primary", required=True)
    p.add_argument("--kind", choices=["primordial", "coupling"], required=True)
    p.add_argument("--mask", type=int, required=True)
    p.add_argument("--restart", type=int, required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("aggregate-hybrid")
    p.add_argument("--kind", choices=["primordial", "coupling"], required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("support-audit")
    p.add_argument("--primary", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("finalize")
    p.add_argument("--preflight", required=True)
    p.add_argument("--primary", required=True)
    p.add_argument("--primordial")
    p.add_argument("--coupling")
    p.add_argument("--support")
    p.add_argument("--output", required=True)

    a = ap.parse_args()
    c = load_cfg(a.config)
    load_source_lock(c)
    load_protocol(c)

    if a.cmd == "preflight":
        return preflight(c, a.q021_dir, a.q022_dir, a.output)
    if a.cmd == "profile":
        return run_profile(c, a.preflight, a.phase, a.mask, a.seed,
                           a.output, a.stage1_dir)
    if a.cmd == "assess-primary":
        return assess_primary(c, a.preflight, a.stage1_dir,
                              a.output, a.matrix_output)
    if a.cmd == "aggregate-primary":
        return aggregate_primary(c, a.preflight, a.stage1_dir, a.assessment,
                                 a.refinement_dir, a.output)
    if a.cmd == "hybrid-profile":
        return run_hybrid_profile(c, a.primary, a.kind,
                                  a.mask, a.restart, a.output)
    if a.cmd == "aggregate-hybrid":
        return aggregate_hybrid(c, a.kind, a.input_dir, a.output)
    if a.cmd == "support-audit":
        return support_audit(c, a.primary, a.output)
    if a.cmd == "finalize":
        return finalize(c, a.preflight, a.primary, a.primordial,
                        a.coupling, a.support, a.output)
    raise RuntimeError("COMMAND_GATE=FAIL")

if __name__ == "__main__":
    raise SystemExit(main())
