#!/usr/bin/env python3
"""Bubbleverse Q-040 — coupled native-nuisance-marginalized CMB-space bridge V1.

Scientific operation
--------------------
Project the Q032-restricted CamSpec and HiLLiPoP TT likelihoods *separately* to
an identity-multipole CMB TT Gaussian likelihood. Each implementation keeps its
own data, covariance/precision, foreground model, relative-calibration semantics
and native nuisance priors. A_planck remains explicit and is never marginalized.

The compression uses a constrained Laplace/Schur construction:
  1. one free latent CMB D_ell per unique ell on the frozen Q032 support;
  2. alternating exact GLS CMB solves and bound-aware native-nuisance MAP steps;
  3. three preregistered independent nuisance initializations;
  4. finite-difference joint Hessian around the stable joint mode;
  5. Schur-complement marginalization of native nuisance uncertainty;
  6. native-likelihood validation probes before any cosmological endpoint run.

A failed Gaussian/Laplace validation is COMPRESSION_VALIDATION_FAIL and is not
converted into a scientific claim about C-036-IMPL.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata as metadata
import json
import math
import os
from pathlib import Path
import signal
import statistics
import subprocess
import sys
from itertools import combinations
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

Q = "Q-040"
PROGRAM_ID = "Q040-CMBSPACE-V1"
RUN_ID = "Q040-CMBSPACE-COUPLED-BRIDGE-V1"
RESULT_ID = "R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-001"
INTERVENTION = "NATIVE_NUISANCE_MARGINALIZED_CMB_SPACE_LAPLACE_SCHUR_V1"
Q032_RESULT_ID = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
Q032_GITHUB_RUN = 33994305721
Q032_EXECUTION_COMMIT = "4dc873a5e880d40858d831a3b421456728f0c032"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
COBAYA_VERSION = "3.5.6"
SUPPORT_HASH = "f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b"
SCALES_HASH = "732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6"
LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
IMPLEMENTATIONS = ("camspec", "hillipop")
START_FAMILIES = (
    "NATIVE_REFERENCE",
    "Q032_LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION",
    "Q032_FARTHEST_COMPLETE_ENDPOINT_WITHIN_IMPLEMENTATION",
)
COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
SCALES = {
    "omega_b": 3.644915744246274e-05,
    "omega_cdm": 2.9761589951235456e-04,
    "fEDE": 1.0851930861718734e-03,
    "log10z_c": 3.666125981785351e-02,
    "thetai_scf": 1.2826810796868315e-02,
    "H0": 2.253286448991929e-01,
    "A_planck": 3.7111561222435974e-04,
}
BASELINE = {
    "matched_median": 2.9317906965863507,
    "centroid": 0.8311487237190059,
    "pairwise_median_drift": 1.6367910228418985,
}
THRESHOLD = 0.10
MARGINALIZED_A_PLANCK = False


class SoftStop(Exception):
    pass


def _alarm(_sig: int, _frame: Any) -> None:
    raise SoftStop("Q040 soft runtime limit")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating, np.bool_)):
        return x.item()
    return str(x)


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return obj


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False, default=json_default) + "\n", encoding="utf-8")
    os.replace(tmp, p)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=json_default).encode("utf-8")
    ).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_array(a: np.ndarray) -> str:
    x = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    h = hashlib.sha256()
    h.update(str(x.shape).encode("ascii"))
    h.update(x.tobytes())
    return h.hexdigest()


def git_head(path: str | Path = ".") -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def resolve_q032_config_path(parent_root: str | Path) -> Path:
    root = Path(parent_root).resolve()
    cfg = (root / "q032_planck_tt3pair_bridge_v2_config.yml").resolve()
    try:
        cfg.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("Q032_CONFIG_CONTAINMENT_GATE=FAIL") from exc
    if not cfg.is_file():
        raise RuntimeError(f"Q032_CONFIG_PATH_GATE=FAIL path={cfg}")
    return cfg


def load_q032(parent_root: str | Path):
    root = Path(parent_root).resolve()
    if git_head(root) != Q032_EXECUTION_COMMIT:
        raise RuntimeError("Q032_EXECUTION_COMMIT_GATE=FAIL")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import q032_planck_tt3pair_bridge_v2 as q32  # type: ignore
    if q32.Q != "Q-032" or q32.RESULT != Q032_RESULT_ID:
        raise RuntimeError("Q032_PARENT_IDENTITY_GATE=FAIL")
    return q32


def load_preregister(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    p = d.get("project", {})
    if p.get("q") != Q or p.get("program_id") != PROGRAM_ID or p.get("run_id") != RUN_ID or p.get("result_id") != RESULT_ID:
        raise RuntimeError("PREREGISTRATION_IDENTITY_GATE=FAIL")
    if d.get("intervention", {}).get("name") != INTERVENTION:
        raise RuntimeError("INTERVENTION_IDENTITY_GATE=FAIL")
    if d.get("parent_lock", {}).get("q032_support_sha256") != SUPPORT_HASH:
        raise RuntimeError("PARENT_SUPPORT_HASH_GATE=FAIL preregister")
    if d.get("cmb_representation", {}).get("primary") != "IDENTITY_UNIQUE_MULTIPOLE_TT":
        raise RuntimeError("NO_HIDDEN_BINNING_GATE=FAIL preregister")
    if d.get("cmb_representation", {}).get("new_binning_allowed") is not False:
        raise RuntimeError("NO_HIDDEN_BINNING_GATE=FAIL preregister")
    if d.get("nuisance_semantics", {}).get("A_planck") != "PRESERVE_AS_EXPLICIT_RUNTIME_PARAMETER_NOT_MARGINALIZED":
        raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL preregister")
    if float(d.get("geometry", {}).get("sufficiency_threshold", -1)) != THRESHOLD:
        raise RuntimeError("THRESHOLD_GATE=FAIL preregister")
    return d


def load_source_lock(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if d.get("q") != Q or d.get("program_id") != PROGRAM_ID or d.get("run_id") != RUN_ID or d.get("result_id") != RESULT_ID:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    sw = d.get("software", {})
    if sw.get("backend_commit") != BACKEND_COMMIT or sw.get("hillipop_commit") != HILLIPOP_COMMIT or sw.get("cobaya") != COBAYA_VERSION:
        raise RuntimeError("SOURCE_LOCK_SOFTWARE_GATE=FAIL")
    if d.get("bubbleverse_parent", {}).get("q032_support_sha256") != SUPPORT_HASH:
        raise RuntimeError("SOURCE_LOCK_PARENT_GATE=FAIL")
    return d


def load_sealed_preflight(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
        and d.get("result_id") == Q032_RESULT_ID
        and d.get("stage") == "Q032_PREFLIGHT_SEALED"
        and d.get("status") == "PASS"
        and d.get("support_sha256") == SUPPORT_HASH
    ):
        raise RuntimeError("Q032_SEALED_PREFLIGHT_GATE=FAIL")
    if any(v != "PASS" for v in d.get("gates", {}).values()):
        raise RuntimeError("Q032_SEALED_PREFLIGHT_GATE=FAIL mandatory_gate")
    return d


def find_parent_file(root: str | Path, implementation: str, mask: int, seed: int) -> Path:
    hits: list[Path] = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == "Q-032"
            and d.get("stage") == "Q032_REFINEMENT"
            and d.get("implementation") == implementation
            and int(d.get("source_mask", -1)) == int(mask)
            and int(d.get("source_seed", -1)) == int(seed)
        ):
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(f"Q032_PARENT_UNIQUENESS_GATE=FAIL impl={implementation} mask={mask} seed={seed} hits={len(hits)}")
    return hits[0]


def validate_parent_record(d: Mapping[str, Any], implementation: str, mask: int, seed: int) -> None:
    label = f"M{mask}-S{seed}"
    expected = {
        "q": "Q-032",
        "run_id": "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2",
        "result_id": Q032_RESULT_ID,
        "stage": "Q032_REFINEMENT",
        "phase": "refinement",
        "implementation": implementation,
        "source_mask": int(mask),
        "source_seed": int(seed),
        "source_label": label,
        "support_sha256": SUPPORT_HASH,
        "status": "COMPLETE",
        "actual_computed_result": True,
    }
    for k, v in expected.items():
        if d.get(k) != v:
            raise RuntimeError(f"Q032_PARENT_PROFILE_GATE=FAIL {k} got={d.get(k)!r} expected={v!r}")
    if d.get("backend_commit") != BACKEND_COMMIT:
        raise RuntimeError("Q032_PARENT_BACKEND_GATE=FAIL")
    if implementation == "hillipop" and d.get("hillipop_commit") != HILLIPOP_COMMIT:
        raise RuntimeError("Q032_PARENT_HILLIPOP_GATE=FAIL")
    if not finite(d.get("objective_chi2")):
        raise RuntimeError("Q032_PARENT_OBJECTIVE_GATE=FAIL")
    minimum = d.get("minimum")
    if not isinstance(minimum, Mapping):
        raise RuntimeError("Q032_PARENT_MINIMUM_GATE=FAIL")
    for name in COORDS:
        if name not in minimum or not finite(minimum[name]):
            raise RuntimeError(f"Q032_PARENT_COORDINATE_GATE=FAIL {name}")


def load_parent(root: str | Path, implementation: str, mask: int, seed: int) -> tuple[dict[str, Any], Path]:
    p = find_parent_file(root, implementation, mask, seed)
    d = read_json(p)
    validate_parent_record(d, implementation, mask, seed)
    return d, p


def all_parent_records(root: str | Path, implementation: str) -> list[dict[str, Any]]:
    out = []
    for m in (3, 6, 7):
        for s in (0, 1, 2):
            d, _ = load_parent(root, implementation, m, s)
            out.append(d)
    return out


def metric(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    terms = []
    for name in COORDS:
        if not (finite(a.get(name)) and finite(b.get(name))):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coordinate={name}")
        terms.append((float(a[name]) - float(b[name])) / SCALES[name])
    return float(math.sqrt(sum(x * x for x in terms) / len(terms)))


def calculate_metrics(rows: Mapping[str, Mapping[str, Mapping[str, float]]], labels: Sequence[str]) -> dict[str, Any]:
    labels = tuple(labels)
    if len(labels) < 2:
        raise RuntimeError("GEOMETRY_LABEL_COUNT_GATE=FAIL")
    c = rows["camspec"]
    h = rows["hillipop"]
    matched = {label: metric(c[label], h[label]) for label in labels}
    cc = {name: statistics.mean(float(c[l][name]) for l in labels) for name in COORDS}
    hc = {name: statistics.mean(float(h[l][name]) for l in labels) for name in COORDS}
    drift: dict[str, float] = {}
    for a, b in combinations(labels, 2):
        drift[f"{a}|{b}"] = abs(metric(c[a], c[b]) - metric(h[a], h[b]))
    return {
        "labels": list(labels),
        "matched_endpoint_rms": matched,
        "matched_median": float(statistics.median(matched.values())),
        "matched_max": float(max(matched.values())),
        "centroid": metric(cc, hc),
        "pairwise_absolute_drifts": drift,
        "pairwise_median_drift": float(statistics.median(drift.values())),
        "pairwise_max_drift": float(max(drift.values())),
    }


def sufficient(metrics: Mapping[str, Any]) -> bool:
    return (
        float(metrics["matched_median"]) <= THRESHOLD
        and float(metrics["centroid"]) <= THRESHOLD
        and float(metrics["pairwise_median_drift"]) <= THRESHOLD
    )


def validate_parent(args: argparse.Namespace) -> int:
    rows: dict[str, dict[str, dict[str, float]]] = {k: {} for k in IMPLEMENTATIONS}
    provenance = {}
    for implementation in IMPLEMENTATIONS:
        for m in (3, 6, 7):
            for s in (0, 1, 2):
                d, p = load_parent(args.parent_dir, implementation, m, s)
                label = f"M{m}-S{s}"
                rows[implementation][label] = {name: float(d["minimum"][name]) for name in COORDS}
                provenance[f"{implementation}:{label}"] = {"path": str(p), "sha256": sha256_file(p)}
    metrics = calculate_metrics(rows, LABELS)
    deltas = {k: abs(float(metrics[k]) - float(BASELINE[k])) for k in BASELINE}
    if any(v > 1e-12 for v in deltas.values()):
        raise RuntimeError(f"Q037_BASELINE_REPRODUCTION_GATE=FAIL deltas={deltas}")
    write_json(args.output, {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "stage": "PARENT_INPUT_GATE",
        "status": "PASS",
        "baseline_reproduced": True,
        "metrics": metrics,
        "deltas": deltas,
        "parent_provenance": provenance,
        "support_sha256": SUPPORT_HASH,
        "scales_sha256": SCALES_HASH,
    })
    print("Q040_PARENT_INPUT_GATE=PASS")
    return 0


def sampled_names(model: Any) -> tuple[str, ...]:
    raw = model.parameterization.sampled_params()
    if isinstance(raw, Mapping):
        return tuple(map(str, raw.keys()))
    return tuple(map(str, raw))


def to_input_params(model: Any, sampled: Mapping[str, float]) -> dict[str, Any]:
    try:
        out = model.parameterization.to_input(dict(sampled))
        return {str(k): v for k, v in dict(out).items()}
    except Exception:
        names = sampled_names(model)
        arr = np.array([float(sampled[n]) for n in names], dtype=float)
        out = model.parameterization.to_input(arr)
        return {str(k): v for k, v in dict(out).items()}


def ref_value(spec: Any) -> float | None:
    if finite(spec):
        return float(spec)
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


def prior_spec(info: Mapping[str, Any], name: str) -> dict[str, Any]:
    spec = info.get("params", {}).get(name)
    if not isinstance(spec, Mapping) or not isinstance(spec.get("prior"), Mapping):
        raise RuntimeError(f"NATIVE_PRIOR_PARSE_GATE=FAIL name={name}")
    return copy.deepcopy(dict(spec["prior"]))


def prior_bounds(prior: Mapping[str, Any]) -> tuple[float | None, float | None]:
    dist = str(prior.get("dist", "uniform" if ("min" in prior or "max" in prior) else ""))
    if dist in ("uniform", "") and ("min" in prior or "max" in prior):
        lo = float(prior["min"]) if finite(prior.get("min")) else None
        hi = float(prior["max"]) if finite(prior.get("max")) else None
        return lo, hi
    if dist in ("norm", "normal", "gaussian"):
        return None, None
    raise RuntimeError(f"NATIVE_PRIOR_PARSE_GATE=FAIL unsupported={prior}")


def prior_nlp(priors: Sequence[Mapping[str, Any]], u: np.ndarray) -> float:
    total = 0.0
    for pr, x in zip(priors, u):
        dist = str(pr.get("dist", "uniform" if ("min" in pr or "max" in pr) else ""))
        if dist in ("uniform", "") and ("min" in pr or "max" in pr):
            if finite(pr.get("min")) and x < float(pr["min"]):
                return math.inf
            if finite(pr.get("max")) and x > float(pr["max"]):
                return math.inf
        elif dist in ("norm", "normal", "gaussian"):
            loc = float(pr.get("loc", pr.get("mean")))
            scale = float(pr.get("scale", pr.get("sigma")))
            if not (finite(loc) and finite(scale) and scale > 0):
                return math.inf
            total += 0.5 * ((float(x) - loc) / scale) ** 2
        else:
            return math.inf
    return float(total)


def proposal_scale(info: Mapping[str, Any], name: str, pr: Mapping[str, Any]) -> float:
    spec = info.get("params", {}).get(name, {})
    if isinstance(spec, Mapping) and finite(spec.get("proposal")) and float(spec["proposal"]) > 0:
        return float(spec["proposal"])
    if str(pr.get("dist", "")) in ("norm", "normal", "gaussian") and finite(pr.get("scale")):
        return float(pr["scale"])
    lo, hi = prior_bounds(pr)
    if lo is not None and hi is not None and hi > lo:
        return max((hi - lo) * 0.02, 1e-6)
    return 1e-3


class NativeContext:
    def __init__(self, args: argparse.Namespace, implementation: str):
        if implementation not in IMPLEMENTATIONS:
            raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
        self.implementation = implementation
        self.preregister = load_preregister(args.preregister)
        self.source_lock = load_source_lock(args.source_lock)
        self.q32 = load_q032(args.q032_parent_root)
        self.cfg = self.q32.load_cfg(resolve_q032_config_path(args.q032_parent_root))
        self.pf = load_sealed_preflight(args.preflight)
        self.support = self.pf["support_lock"]
        if self.support.get("support_sha256") != SUPPORT_HASH:
            raise RuntimeError("OBSERVATIONAL_SUPPORT_GATE=FAIL")
        parent, _ = load_parent(args.parent_dir, implementation, 3, 0)
        seed = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
        self.patch_meta = None
        if implementation == "hillipop":
            if not args.hlp_matrix or not args.hlp_meta:
                raise RuntimeError("HILLIPOP_RESTRICTED_PRECISION_INPUT_GATE=FAIL")
            self.patch_meta = self.q32.install_hillipop_patch(args.hlp_matrix, args.hlp_meta, self.support, self.cfg)
            self.info = self.q32.build_hillipop_info(self.cfg, seed, Path(args.scratch) / "hlp_context", "refinement")
            component = self.q32.HILLIPOP
        else:
            self.info = self.q32.build_camspec_info(self.cfg, seed, Path(args.scratch) / "cam_context", "refinement", self.support)
            component = self.q32.CAMSPEC
        self.component = component
        self.model = self.q32.create_model(self.info)
        self.like = self.model.likelihood[component]
        if metadata.version("cobaya") != COBAYA_VERSION:
            raise RuntimeError("CAMSPEC_COBAYA_VERSION_GATE=FAIL")
        self.sampled_order = sampled_names(self.model)
        self.base_sampled = self.q32.reference_vector(self.info, preferred=seed)
        if "A_planck" not in self.base_sampled:
            raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL missing")
        self.base_sampled["A_planck"] = 1.0
        raw_nuis = list(self.q32.sampled_nuisance(self.info))
        if "A_planck" not in raw_nuis:
            raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL not_sampled")
        raw_nuis.remove("A_planck")
        self.support_null_nuisance: list[str] = []
        if implementation == "hillipop":
            for n in ("cal100A", "cal100B"):
                if n in raw_nuis:
                    self.support_null_nuisance.append(n)
                    raw_nuis.remove(n)
        self.nuisance_names = tuple(raw_nuis)
        self.priors = tuple(prior_spec(self.info, n) for n in self.nuisance_names)
        self.bounds = tuple(prior_bounds(pr) for pr in self.priors)
        self.proposal_scales = np.array(
            [proposal_scale(self.info, n, pr) for n, pr in zip(self.nuisance_names, self.priors)], dtype=float
        )
        self.native_reference = np.array([float(self.base_sampled[n]) for n in self.nuisance_names], dtype=float)
        if implementation == "camspec":
            self.rows = self.q32.camspec_rows(self.like)
            self.P = np.asarray(self.like.covinv, dtype=np.float64)
        else:
            allrows = self.q32.hillipop_rows(self.like)
            S = np.asarray(self.support["hillipop_selected_full_indices_native_order"], dtype=int)
            self.rows = [allrows[i] for i in S]
            self.P = np.asarray(self.like._q032_precision, dtype=np.float64)
            self.selected_indices = S
        if self.P.shape != (len(self.rows), len(self.rows)) or not np.all(np.isfinite(self.P)):
            raise RuntimeError("DATA_GATE=FAIL native_precision_shape")
        self.ells = np.array(sorted({int(r["ell"]) for r in self.rows if r.get("ell") is not None}), dtype=int)
        if len(self.ells) == 0 or any(r.get("ell") is None for r in self.rows):
            raise RuntimeError("NO_HIDDEN_BINNING_GATE=FAIL non_identity_row")
        self.ell_to_index = {int(e): i for i, e in enumerate(self.ells)}
        self.row_ell_index = np.array([self.ell_to_index[int(r["ell"])] for r in self.rows], dtype=int)
        canonical_parent = {(str(p), int(e)) for p, e in self.support["canonical_common_keys"]}
        runtime_parent = {(str(r["spectrum"]), int(r["ell"])) for r in self.rows}
        if runtime_parent != canonical_parent:
            raise RuntimeError("OBSERVATIONAL_SUPPORT_GATE=FAIL runtime_keys")
        self.representation_hash = canonical_hash({
            "parent_support_sha256": SUPPORT_HASH,
            "representation": "IDENTITY_UNIQUE_MULTIPOLE_TT",
            "ordered_unique_ells": self.ells.tolist(),
        })
        self.groups = [np.flatnonzero(self.row_ell_index == i) for i in range(len(self.ells))]
        if any(len(g) == 0 for g in self.groups):
            raise RuntimeError("CMB_REPRESENTATION_GATE=FAIL empty_group")
        self._verify_support_null()
        self._verify_linear_design()

    def close(self) -> None:
        try:
            self.model.close()
        except Exception:
            pass

    def sampled_with_eta(self, eta: np.ndarray, A_planck: float = 1.0) -> dict[str, float]:
        x = dict(self.base_sampled)
        for n, v in zip(self.nuisance_names, eta):
            x[n] = float(v)
        for n in self.support_null_nuisance:
            x[n] = float(self.base_sampled[n])
        x["A_planck"] = float(A_planck)
        return x

    def input_params(self, eta: np.ndarray, A_planck: float = 1.0) -> dict[str, Any]:
        return to_input_params(self.model, self.sampled_with_eta(eta, A_planck=A_planck))

    def residual(self, cmb: np.ndarray, eta: np.ndarray, A_planck: float = 1.0) -> np.ndarray:
        cmb = np.asarray(cmb, dtype=float)
        if cmb.shape != (len(self.ells),):
            raise RuntimeError("CMB_VECTOR_SHAPE_GATE=FAIL")
        pars = self.input_params(eta, A_planck=A_planck)
        if self.implementation == "camspec":
            fg = np.asarray(self.like.get_foregrounds(pars), dtype=float)
            cals = np.asarray(self.like.get_cals(pars), dtype=float)
            names = [str(x) for x in self.like.cl_names]
            spec_index = {n: i for i, n in enumerate(names)}
            r = np.asarray(self.like.data_vector, dtype=np.float64).copy()
            for row in self.rows:
                idx = int(row["index"])
                si = spec_index[str(row["spectrum"])]
                ell = int(row["ell"])
                ci = float(cals[si])
                if not finite(ci) or ci == 0:
                    raise RuntimeError("CAMSPEC_CALIBRATION_GATE=FAIL")
                r[idx] -= (float(cmb[self.ell_to_index[ell]]) + float(fg[si, ell])) / ci
            return r
        lmax = int(self.like.lmax)
        dl = np.zeros(lmax + 1, dtype=float)
        dl[self.ells] = cmb
        Rspec = self.like._compute_residuals(pars, {"TT": dl}, "TT")
        Rl = self.like._xspectra_to_xfreq(Rspec, self.like._dlweight["TT"])
        Xtt = np.asarray(self.like._select_spectra(Rl, "TT"), dtype=np.float64)
        r = Xtt[self.selected_indices]
        if r.shape != (len(self.rows),):
            raise RuntimeError("HILLIPOP_RESIDUAL_SHAPE_GATE=FAIL")
        return r

    def design(self, eta: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        z = np.zeros(len(self.ells), dtype=float)
        o = np.ones(len(self.ells), dtype=float)
        y = self.residual(z, eta, A_planck=A_planck)
        r1 = self.residual(o, eta, A_planck=A_planck)
        a = y - r1
        if not np.all(np.isfinite(y)) or not np.all(np.isfinite(a)) or np.any(np.abs(a) < 1e-10):
            raise RuntimeError("CMB_LINEAR_DESIGN_GATE=FAIL coefficients")
        return y, a

    def _verify_linear_design(self) -> None:
        eta = self.native_reference.copy()
        y, a = self.design(eta, A_planck=1.0)
        probe = 0.7 + 0.2 * np.sin(self.ells / 97.0) + 0.1 * np.cos(self.ells / 211.0)
        actual = self.residual(probe, eta, A_planck=1.0)
        predicted = y - a * probe[self.row_ell_index]
        rel = float(np.linalg.norm(actual - predicted) / max(1.0, np.linalg.norm(actual)))
        if rel > 1e-10:
            raise RuntimeError(f"CMB_LINEAR_DESIGN_GATE=FAIL rel={rel}")
        self.linear_design_relative_error = rel

    def _verify_support_null(self) -> None:
        if not self.support_null_nuisance:
            self.support_null_response_max = 0.0
            return
        eta = self.native_reference.copy()
        cmb = np.zeros(len(self.ells), dtype=float)
        base = self.residual_without_null_override(cmb, eta, {})
        mx = 0.0
        for n in self.support_null_nuisance:
            v0 = float(self.base_sampled[n])
            dv = 0.01
            pert = self.residual_without_null_override(cmb, eta, {n: v0 + dv})
            mx = max(mx, float(np.max(np.abs(pert - base))))
        if mx > 1e-12:
            raise RuntimeError(f"SUPPORT_NULL_NUISANCE_GATE=FAIL max={mx}")
        self.support_null_response_max = mx

    def residual_without_null_override(self, cmb: np.ndarray, eta: np.ndarray, overrides: Mapping[str, float]) -> np.ndarray:
        saved = dict(self.base_sampled)
        try:
            for k, v in overrides.items():
                self.base_sampled[str(k)] = float(v)
            return self.residual(cmb, eta, A_planck=1.0)
        finally:
            self.base_sampled.clear()
            self.base_sampled.update(saved)

    def prior_nlp(self, eta: np.ndarray) -> float:
        return prior_nlp(self.priors, np.asarray(eta, dtype=float))

    def joint_objective(self, cmb: np.ndarray, eta: np.ndarray, A_planck: float = 1.0) -> float:
        pn = self.prior_nlp(eta)
        if not finite(pn):
            return 1e100
        try:
            r = self.residual(cmb, eta, A_planck=A_planck)
            chi2 = float(r @ (self.P @ r))
        except Exception:
            return 1e100
        if not finite(chi2) or chi2 < 0:
            return 1e100
        return 0.5 * chi2 + pn

    def gls_system(self, eta: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        y, a = self.design(eta, A_planck=A_planck)
        nobs = len(y)
        nell = len(self.ells)
        PA = np.empty((nobs, nell), dtype=np.float64)
        for j, g in enumerate(self.groups):
            PA[:, j] = self.P[:, g] @ a[g]
        H = np.empty((nell, nell), dtype=np.float64)
        for i, g in enumerate(self.groups):
            H[i, :] = a[g] @ PA[g, :]
        H = 0.5 * (H + H.T)
        Py = self.P @ y
        b = np.array([float(a[g] @ Py[g]) for g in self.groups], dtype=float)
        try:
            cf = cho_factor(H, lower=True, check_finite=False)
            cmb = cho_solve(cf, b, check_finite=False)
        except Exception as exc:
            raise RuntimeError("CMB_IDENTITY_CONDITIONING_GATE=FAIL") from exc
        if not np.all(np.isfinite(cmb)):
            raise RuntimeError("FINITE_CMB_MAP_GATE=FAIL")
        return cmb, H, y, a, b

    def grad_cmb(self, cmb: np.ndarray, eta: np.ndarray, A_planck: float = 1.0) -> np.ndarray:
        r = self.residual(cmb, eta, A_planck=A_planck)
        _, a = self.design(eta, A_planck=A_planck)
        Pr = self.P @ r
        return -np.array([float(a[g] @ Pr[g]) for g in self.groups], dtype=float)

    def start_vector(self, parent_dir: str | Path, family: str) -> tuple[np.ndarray, dict[str, Any]]:
        if family not in START_FAMILIES:
            raise RuntimeError("COMPRESSION_START_FAMILY_GATE=FAIL")
        if family == "NATIVE_REFERENCE":
            return self.native_reference.copy(), {"family": family, "source": "runtime_native_ref"}
        records = all_parent_records(parent_dir, self.implementation)
        best = min(records, key=lambda d: float(d["objective_chi2"]))
        def vec(rec: Mapping[str, Any]) -> np.ndarray:
            minimum = rec["minimum"]
            return np.array([
                float(minimum[n]) if n in minimum and finite(minimum[n]) else float(self.base_sampled[n])
                for n in self.nuisance_names
            ], dtype=float)
        bestv = vec(best)
        if family == "Q032_LOWEST_OBJECTIVE_WITHIN_IMPLEMENTATION":
            return bestv, {"family": family, "source_label": best["source_label"], "source_objective_chi2": best["objective_chi2"]}
        candidates = []
        for rec in records:
            v = vec(rec)
            d = float(np.sqrt(np.mean(((v - bestv) / np.maximum(self.proposal_scales, 1e-12)) ** 2)))
            candidates.append((d, rec, v))
        d, rec, v = max(candidates, key=lambda x: (x[0], str(x[1]["source_label"])))
        return v, {"family": family, "source_label": rec["source_label"], "scaled_distance_from_best": d}


def optimize_eta(ctx: NativeContext, cmb: np.ndarray, eta0: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, dict[str, Any]]:
    bounds = list(ctx.bounds)
    def fun(u: np.ndarray) -> float:
        return ctx.joint_objective(cmb, np.asarray(u, dtype=float), A_planck=A_planck)
    primary = minimize(
        fun,
        np.asarray(eta0, dtype=float),
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 5000, "ftol": 1e-12, "gtol": 1e-7, "maxls": 50},
    )
    chosen = primary
    method = "L-BFGS-B"
    if (not primary.success) or (not finite(primary.fun)) or float(primary.fun) >= 1e99:
        fallback = minimize(
            fun,
            np.asarray(eta0, dtype=float),
            method="Powell",
            bounds=bounds,
            options={"maxiter": 5000, "xtol": 1e-8, "ftol": 1e-10},
        )
        if finite(fallback.fun) and (not finite(primary.fun) or float(fallback.fun) <= float(primary.fun)):
            chosen = fallback
            method = "Powell"
    if not finite(chosen.fun) or float(chosen.fun) >= 1e99:
        raise RuntimeError("NUISANCE_OPTIMIZATION_GATE=FAIL")
    return np.asarray(chosen.x, dtype=float), {
        "method": method,
        "success": bool(chosen.success),
        "status": int(getattr(chosen, "status", -1)),
        "message": str(getattr(chosen, "message", "")),
        "fun": float(chosen.fun),
        "nfev": int(getattr(chosen, "nfev", -1)),
        "nit": int(getattr(chosen, "nit", -1)),
    }


def alternating_map(ctx: NativeContext, eta0: np.ndarray) -> dict[str, Any]:
    eta = np.asarray(eta0, dtype=float).copy()
    prev_obj = None
    history = []
    cmb = None
    converged = False
    for outer in range(12):
        cmb0, _, _, _, _ = ctx.gls_system(eta, A_planck=1.0)
        eta_new, opt = optimize_eta(ctx, cmb0, eta, A_planck=1.0)
        cmb_new, H, _, _, _ = ctx.gls_system(eta_new, A_planck=1.0)
        obj = ctx.joint_objective(cmb_new, eta_new, A_planck=1.0)
        scaled_eta = float(np.max(np.abs((eta_new - eta) / np.maximum(ctx.proposal_scales, 1e-12)))) if len(eta) else 0.0
        rel_obj = math.inf if prev_obj is None else abs(obj - prev_obj) / max(1.0, abs(prev_obj))
        history.append({
            "outer": outer,
            "objective": float(obj),
            "relative_objective_change": float(rel_obj) if finite(rel_obj) else None,
            "max_scaled_nuisance_change": scaled_eta,
            "optimizer": opt,
        })
        eta = eta_new
        cmb = cmb_new
        if prev_obj is not None and rel_obj <= 1e-6 and scaled_eta <= 1e-3:
            converged = True
            break
        prev_obj = obj
    if cmb is None:
        raise RuntimeError("COMPRESSION_MAP_GATE=FAIL no_cmb")
    grad = ctx.grad_cmb(cmb, eta)
    grad_rms = float(np.sqrt(np.mean(grad ** 2)))
    return {
        "status": "COMPLETE" if converged else "NOT_CONVERGED",
        "converged": converged,
        "objective": float(ctx.joint_objective(cmb, eta)),
        "eta": {n: float(v) for n, v in zip(ctx.nuisance_names, eta)},
        "cmb": cmb.tolist(),
        "cmb_gradient_rms": grad_rms,
        "outer_iterations": len(history),
        "history": history,
    }


def map_start(args: argparse.Namespace) -> int:
    ctx = NativeContext(args, args.implementation)
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(args.soft_stop_minutes) * 60))
    rec: dict[str, Any] = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "COMPRESSION_MAP_START",
        "implementation": args.implementation,
        "start_family": args.start_family,
        "status": "FAILED",
        "actual_scientific_result": False,
        "support_sha256": SUPPORT_HASH,
        "representation_sha256": ctx.representation_hash,
    }
    try:
        eta0, meta = ctx.start_vector(args.parent_dir, args.start_family)
        out = alternating_map(ctx, eta0)
        rec.update(out)
        rec["start_provenance"] = meta
        rec["nuisance_names"] = list(ctx.nuisance_names)
        rec["support_null_nuisance"] = list(ctx.support_null_nuisance)
        rec["support_null_response_max"] = ctx.support_null_response_max
        rec["linear_design_relative_error"] = ctx.linear_design_relative_error
        if out["status"] != "COMPLETE":
            rec["failure_class"] = "NUMERICAL"
    except SoftStop as exc:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC", "error": repr(exc)})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD", "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        ctx.close()
        write_json(args.output, rec)
    return 0 if rec.get("status") == "COMPLETE" else 2


def hessian_steps(ctx: NativeContext, eta: np.ndarray) -> np.ndarray:
    steps = []
    for i, (x, scale, bound) in enumerate(zip(eta, ctx.proposal_scales, ctx.bounds)):
        h = max(abs(float(scale)) * 0.2, abs(float(x)) * 1e-5, 1e-6)
        lo, hi = bound
        room = math.inf
        if lo is not None:
            room = min(room, float(x) - lo)
        if hi is not None:
            room = min(room, hi - float(x))
        if finite(room):
            h = min(h, 0.25 * room)
        if not finite(h) or h <= 1e-9:
            raise RuntimeError(f"BOUNDARY_HESSIAN_GATE=FAIL name={ctx.nuisance_names[i]}")
        steps.append(h)
    return np.array(steps, dtype=float)


def finite_hessian_eta(ctx: NativeContext, cmb: np.ndarray, eta: np.ndarray, A_planck: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    eta = np.asarray(eta, dtype=float)
    h = hessian_steps(ctx, eta)
    k = len(eta)
    H = np.zeros((k, k), dtype=float)
    f0 = ctx.joint_objective(cmb, eta, A_planck=A_planck)
    if not finite(f0) or f0 >= 1e99:
        raise RuntimeError("NUISANCE_HESSIAN_GATE=FAIL center")
    fp = np.empty(k); fm = np.empty(k)
    for i in range(k):
        xp = eta.copy(); xm = eta.copy(); xp[i] += h[i]; xm[i] -= h[i]
        fp[i] = ctx.joint_objective(cmb, xp, A_planck=A_planck)
        fm[i] = ctx.joint_objective(cmb, xm, A_planck=A_planck)
        H[i, i] = (fp[i] - 2.0 * f0 + fm[i]) / (h[i] ** 2)
    for i in range(k):
        for j in range(i + 1, k):
            xpp = eta.copy(); xpm = eta.copy(); xmp = eta.copy(); xmm = eta.copy()
            xpp[i] += h[i]; xpp[j] += h[j]
            xpm[i] += h[i]; xpm[j] -= h[j]
            xmp[i] -= h[i]; xmp[j] += h[j]
            xmm[i] -= h[i]; xmm[j] -= h[j]
            val = (
                ctx.joint_objective(cmb, xpp, A_planck=A_planck)
                - ctx.joint_objective(cmb, xpm, A_planck=A_planck)
                - ctx.joint_objective(cmb, xmp, A_planck=A_planck)
                + ctx.joint_objective(cmb, xmm, A_planck=A_planck)
            ) / (4.0 * h[i] * h[j])
            H[i, j] = H[j, i] = val
    H = 0.5 * (H + H.T)
    if not np.all(np.isfinite(H)):
        raise RuntimeError("NUISANCE_HESSIAN_GATE=FAIL nonfinite")
    return H, h


def finite_cross_hessian(ctx: NativeContext, cmb: np.ndarray, eta: np.ndarray, steps: np.ndarray) -> np.ndarray:
    k = len(eta); nell = len(cmb)
    X = np.empty((nell, k), dtype=float)
    for j in range(k):
        xp = eta.copy(); xm = eta.copy(); xp[j] += steps[j]; xm[j] -= steps[j]
        gp = ctx.grad_cmb(cmb, xp)
        gm = ctx.grad_cmb(cmb, xm)
        X[:, j] = (gp - gm) / (2.0 * steps[j])
    if not np.all(np.isfinite(X)):
        raise RuntimeError("CROSS_HESSIAN_GATE=FAIL")
    return X


def load_map_candidates(root: str | Path, implementation: str) -> list[dict[str, Any]]:
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("stage") == "COMPRESSION_MAP_START" and d.get("implementation") == implementation:
            out.append(d)
    fams = {d.get("start_family") for d in out if d.get("status") == "COMPLETE"}
    if fams != set(START_FAMILIES) or len(out) != 3:
        raise RuntimeError(f"COMPRESSION_MULTISTART_GATE=FAIL families={fams} count={len(out)}")
    return out


def save_array(path: str | Path, arr: np.ndarray) -> dict[str, Any]:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    np.save(p, np.asarray(arr), allow_pickle=False)
    return {"file": p.name, "file_sha256": sha256_file(p), "array_sha256": sha256_array(np.asarray(arr, dtype=np.float64)), "shape": list(np.asarray(arr).shape)}


def build_compression(args: argparse.Namespace) -> int:
    ctx = NativeContext(args, args.implementation)
    rec: dict[str, Any] = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "COMPRESSION_BUILD", "implementation": args.implementation,
        "status": "FAILED", "actual_scientific_result": False,
        "support_sha256": SUPPORT_HASH, "representation_sha256": ctx.representation_hash,
    }
    try:
        candidates = load_map_candidates(args.map_dir, args.implementation)
        objectives = [float(d["objective"]) for d in candidates]
        spread = max(objectives) - min(objectives)
        if spread > 0.50:
            raise RuntimeError(f"COMPRESSION_MULTISTART_GATE=FAIL objective_spread={spread}")
        best = min(candidates, key=lambda d: float(d["objective"]))
        eta = np.array([float(best["eta"][n]) for n in ctx.nuisance_names], dtype=float)
        cmb = np.array(best["cmb"], dtype=float)
        cmb_check, Hss, _, _, _ = ctx.gls_system(eta)
        if np.linalg.norm(cmb - cmb_check) / max(1.0, np.linalg.norm(cmb_check)) > 1e-8:
            raise RuntimeError("COMPRESSION_MAP_CONSISTENCY_GATE=FAIL")
        max_rms = 0.0
        for d in candidates:
            x = np.array(d["cmb"], dtype=float)
            diff = x - cmb
            rms = float(math.sqrt(max(0.0, float(diff @ (Hss @ diff))) / len(cmb)))
            max_rms = max(max_rms, rms)
        if max_rms > 0.10:
            raise RuntimeError(f"COMPRESSION_MULTISTART_GATE=FAIL cmb_normalized_rms={max_rms}")
        Heta, steps = finite_hessian_eta(ctx, cmb, eta)
        try:
            cf_eta = cho_factor(Heta, lower=True, check_finite=False)
        except Exception as exc:
            raise RuntimeError("NUISANCE_HESSIAN_PD_GATE=FAIL") from exc
        cross = finite_cross_hessian(ctx, cmb, eta, steps)
        correction = cross @ cho_solve(cf_eta, cross.T, check_finite=False)
        P_cmb = 0.5 * ((Hss - correction) + (Hss - correction).T)
        try:
            cf_cmb = cho_factor(P_cmb, lower=True, check_finite=False)
            C_cmb = cho_solve(cf_cmb, np.eye(len(cmb)), check_finite=False)
        except Exception as exc:
            raise RuntimeError("COMPRESSION_COVARIANCE_GATE=FAIL marginal_cmb") from exc
        C_cmb = 0.5 * (C_cmb + C_cmb.T)
        # Nuisance covariance marginalized over CMB, used only for native-boundary validation.
        cf_hss = cho_factor(Hss, lower=True, check_finite=False)
        Heta_marg = Heta - cross.T @ cho_solve(cf_hss, cross, check_finite=False)
        Heta_marg = 0.5 * (Heta_marg + Heta_marg.T)
        try:
            cf_em = cho_factor(Heta_marg, lower=True, check_finite=False)
            Ceta_marg = cho_solve(cf_em, np.eye(len(eta)), check_finite=False)
        except Exception as exc:
            raise RuntimeError("NUISANCE_MARGINAL_COVARIANCE_GATE=FAIL") from exc
        sig = np.sqrt(np.maximum(np.diag(Ceta_marg), 0.0))
        boundary = {}
        for i, n in enumerate(ctx.nuisance_names):
            lo, hi = ctx.bounds[i]
            ds = math.inf
            if lo is not None and sig[i] > 0:
                ds = min(ds, (eta[i] - lo) / sig[i])
            if hi is not None and sig[i] > 0:
                ds = min(ds, (hi - eta[i]) / sig[i])
            boundary[n] = None if not finite(ds) else float(ds)
            if finite(ds) and ds < 2.5:
                raise RuntimeError(f"NATIVE_BOUNDARY_GAUSSIANITY_GATE=FAIL name={n} sigma_distance={ds}")
        outdir = Path(args.output_dir); outdir.mkdir(parents=True, exist_ok=True)
        prefix = f"q040_cmbspace_{args.implementation}_v1"
        f_ells = save_array(outdir / f"{prefix}_ells.npy", ctx.ells.astype(np.int64))
        f_mean = save_array(outdir / f"{prefix}_mean.npy", cmb)
        f_cov = save_array(outdir / f"{prefix}_covariance.npy", C_cmb)
        f_prec = save_array(outdir / f"{prefix}_precision.npy", P_cmb)
        data_prov: dict[str, Any] = {}
        if args.implementation == "camspec":
            cr = ctx.pf.get("camspec_runtime", {})
            required = ("dataset_file_sha256", "data_vector_sha256", "covariance_sha256")
            if not all(cr.get(k) for k in required):
                raise RuntimeError("DATA_HASH_GATE=FAIL camspec")
            data_prov = {k: cr[k] for k in required}
        else:
            hr = ctx.pf.get("hillipop_data_runtime", {})
            if not hr.get("data_hashes") or not hr.get("cross_spectrum_hashes"):
                raise RuntimeError("DATA_HASH_GATE=FAIL hillipop_native")
            hm = read_json(args.hlp_meta)
            if not hm.get("restricted_precision_sha256"):
                raise RuntimeError("DATA_HASH_GATE=FAIL hillipop_restricted")
            data_prov = {
                "native_data_hashes": hr["data_hashes"],
                "cross_spectrum_hashes": hr["cross_spectrum_hashes"],
                "restricted_precision_sha256": hm["restricted_precision_sha256"],
            }
        rec.update({
            "status": "COMPRESSION_BUILT",
            "selected_start_family": best["start_family"],
            "joint_map_objective": float(best["objective"]),
            "multistart_objective_spread": spread,
            "multistart_max_cmb_normalized_rms": max_rms,
            "nuisance_names": list(ctx.nuisance_names),
            "support_null_nuisance_analytically_factorized": list(ctx.support_null_nuisance),
            "support_null_response_max": ctx.support_null_response_max,
            "A_planck_marginalized": False,
            "A_planck_construction_value": 1.0,
            "eta_map": {n: float(v) for n, v in zip(ctx.nuisance_names, eta)},
            "eta_marginal_sigma": {n: float(v) for n, v in zip(ctx.nuisance_names, sig)},
            "native_bound_sigma_distance": boundary,
            "linear_design_relative_error": ctx.linear_design_relative_error,
            "ordered_unique_ells": ctx.ells.tolist(),
            "n_ell": len(ctx.ells),
            "n_native_observations": len(ctx.rows),
            "files": {"ells": f_ells, "mean": f_mean, "covariance": f_cov, "precision": f_prec},
            "precision_sha256": sha256_array(P_cmb),
            "covariance_sha256": sha256_array(C_cmb),
            "data_provenance": data_prov,
            "construction": {
                "method": "CONSTRAINED_LAPLACE_SCHUR_MARGINALIZATION",
                "cosmological_model_used_in_compression": False,
                "foreground_zeroing": False,
                "cross_family_covariance_transfer": False,
                "cross_family_nuisance_mapping": False,
                "hidden_binning": False,
            },
            "gates": {
                "Q_IDENTITY_GATE": "PASS",
                "PARENT_LOCK_GATE": "PASS",
                "OBSERVATIONAL_SUPPORT_GATE": "PASS",
                "NO_HIDDEN_BINNING_GATE": "PASS",
                "NATIVE_NUISANCE_SEMANTICS_GATE": "PASS",
                "A_PLANCK_PRESERVATION_GATE": "PASS",
                "COMPRESSION_MULTISTART_GATE": "PASS",
                "COMPRESSION_COVARIANCE_GATE": "PASS",
                "NATIVE_BOUNDARY_GAUSSIANITY_GATE": "PASS",
            },
        })
        write_json(outdir / f"{prefix}_metadata.json", rec)
        if Path(args.metadata_output) != outdir / f"{prefix}_metadata.json":
            write_json(args.metadata_output, rec)
        print(f"Q040_COMPRESSION_BUILD_GATE=PASS implementation={args.implementation}")
        return 0
    except Exception as exc:
        rec.update({"status": "COMPRESSION_BUILD_FAIL", "failure_class": "VALIDATION_OR_NUMERICAL", "error": repr(exc)})
        write_json(args.metadata_output, rec)
        return 2
    finally:
        ctx.close()


def load_compression(meta_path: str | Path, array_dir: str | Path, implementation: str) -> tuple[dict[str, Any], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    m = read_json(meta_path)
    if not (
        m.get("q") == Q and m.get("program_id") == PROGRAM_ID and m.get("stage") == "COMPRESSION_BUILD"
        and m.get("implementation") == implementation and m.get("status") == "COMPRESSION_BUILT"
        and m.get("support_sha256") == SUPPORT_HASH
    ):
        raise RuntimeError("COMPRESSION_METADATA_GATE=FAIL")
    base = Path(array_dir)
    def arr(which: str) -> np.ndarray:
        rec = m["files"][which]
        p = base / rec["file"]
        if sha256_file(p) != rec["file_sha256"]:
            raise RuntimeError(f"COMPRESSION_FILE_HASH_GATE=FAIL {which}")
        x = np.load(p, allow_pickle=False)
        if sha256_array(np.asarray(x, dtype=np.float64)) != rec["array_sha256"]:
            raise RuntimeError(f"COMPRESSION_ARRAY_HASH_GATE=FAIL {which}")
        return np.asarray(x)
    ells = arr("ells").astype(int)
    mean = arr("mean").astype(float)
    cov = arr("covariance").astype(float)
    prec = arr("precision").astype(float)
    return m, ells, mean, cov, prec


def conditional_laplace_score(ctx: NativeContext, cmb: np.ndarray, eta_seed: np.ndarray, A_planck: float) -> tuple[float, dict[str, Any]]:
    starts = [eta_seed.copy(), ctx.native_reference.copy()]
    sols = []
    for st in starts:
        eta, opt = optimize_eta(ctx, cmb, st, A_planck=A_planck)
        f = ctx.joint_objective(cmb, eta, A_planck=A_planck)
        H, _ = finite_hessian_eta(ctx, cmb, eta, A_planck=A_planck)
        try:
            cf = cho_factor(H, lower=True, check_finite=False)
            logdet = 2.0 * float(np.sum(np.log(np.diag(cf[0]))))
        except Exception as exc:
            raise RuntimeError("CONDITIONAL_LAPLACE_HESSIAN_GATE=FAIL") from exc
        score = 2.0 * f + logdet
        sols.append({"score": score, "eta": eta, "optimizer": opt})
    sols.sort(key=lambda x: float(x["score"]))
    spread = float(sols[-1]["score"] - sols[0]["score"])
    if spread > 0.35:
        raise RuntimeError(f"CONDITIONAL_NUISANCE_MULTISTART_GATE=FAIL score_spread={spread}")
    best = sols[0]
    return float(best["score"]), {
        "multistart_score_spread": spread,
        "eta": {n: float(v) for n, v in zip(ctx.nuisance_names, best["eta"])},
        "optimizer": best["optimizer"],
    }


def validate_compression(args: argparse.Namespace) -> int:
    ctx = NativeContext(args, args.implementation)
    rec: dict[str, Any] = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "COMPRESSION_VALIDATION", "implementation": args.implementation,
        "status": "COMPRESSION_VALIDATION_FAIL", "actual_scientific_result": False,
    }
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(args.soft_stop_minutes) * 60))
    try:
        meta, ells, mean, cov, prec = load_compression(args.compression_meta, args.compression_dir, args.implementation)
        if not np.array_equal(ells, ctx.ells) or meta.get("representation_sha256") != ctx.representation_hash:
            raise RuntimeError("CMB_REPRESENTATION_HASH_GATE=FAIL")
        if mean.shape != (len(ells),) or cov.shape != (len(ells), len(ells)) or prec.shape != cov.shape:
            raise RuntimeError("COMPRESSION_SHAPE_GATE=FAIL")
        if not (np.all(np.isfinite(mean)) and np.all(np.isfinite(cov)) and np.all(np.isfinite(prec))):
            raise RuntimeError("FINITE_COMPRESSION_GATE=FAIL")
        cho_factor(cov, lower=True, check_finite=False)
        cho_factor(prec, lower=True, check_finite=False)
        ident_rel = float(np.linalg.norm(cov @ prec - np.eye(len(ells)), ord="fro") / math.sqrt(len(ells)))
        if ident_rel > 1e-7:
            raise RuntimeError(f"COMPRESSION_INVERSE_GATE=FAIL rel={ident_rel}")
        eta_seed = np.array([float(meta["eta_map"][n]) for n in ctx.nuisance_names], dtype=float)
        ref_score, ref_meta = conditional_laplace_score(ctx, mean, eta_seed, 1.0)
        pivot = float(np.median(ells))
        directions = {
            "CONSTANT": np.ones(len(ells), dtype=float),
            "LOG_TILT": np.log(np.maximum(ells, 2) / pivot),
            "HIGH_ELL_RAMP": np.clip((ells.astype(float) - 1500.0) / 1000.0, 0.0, 1.0),
        }
        probes = []
        maxerr = 0.0
        for name, v in directions.items():
            if np.linalg.norm(v) == 0:
                raise RuntimeError(f"COMPRESSION_PROBE_DIRECTION_GATE=FAIL {name}")
            q = float(v @ (prec @ v))
            if not finite(q) or q <= 0:
                raise RuntimeError(f"COMPRESSION_PROBE_DIRECTION_GATE=FAIL metric {name}")
            alpha = math.sqrt(1.0 / q)
            for signv in (-1, 1):
                s = mean + signv * alpha * v
                native_score, nmeta = conditional_laplace_score(ctx, s, eta_seed, 1.0)
                native_delta = native_score - ref_score
                compressed_delta = float((s - mean) @ (prec @ (s - mean)))
                err = abs(native_delta - compressed_delta)
                maxerr = max(maxerr, err)
                probes.append({
                    "type": "CMB_DIRECTION", "direction": name, "sign": signv,
                    "native_delta_chi2": native_delta, "compressed_delta_chi2": compressed_delta,
                    "abs_error": err, "conditional_nuisance": nmeta,
                })
        aplanck = []
        for da in (-0.0025, 0.0025):
            A = 1.0 + da
            native_score, nmeta = conditional_laplace_score(ctx, mean, eta_seed, A)
            native_delta = native_score - ref_score
            theory = mean / (A ** 2)
            compressed_delta = float((theory - mean) @ (prec @ (theory - mean)))
            err = abs(native_delta - compressed_delta)
            maxerr = max(maxerr, err)
            aplanck.append({
                "A_planck": A, "native_delta_chi2": native_delta,
                "compressed_delta_chi2": compressed_delta, "abs_error": err,
                "conditional_nuisance": nmeta,
            })
        if maxerr > 0.35:
            raise RuntimeError(f"COMPRESSION_GAUSSIAN_APPROXIMATION_GATE=FAIL max_abs_error={maxerr}")
        rec.update({
            "status": "PASS",
            "support_sha256": SUPPORT_HASH,
            "representation_sha256": ctx.representation_hash,
            "inverse_identity_relative_residual": ident_rel,
            "reference_native_laplace_score": ref_score,
            "reference_conditional_nuisance": ref_meta,
            "cmb_direction_probes": probes,
            "A_planck_probes": aplanck,
            "max_abs_native_vs_compressed_delta_chi2_error": maxerr,
            "gates": {
                "FINITE_DATA_VECTOR_GATE": "PASS",
                "COMPRESSION_COVARIANCE_GATE": "PASS",
                "COMPRESSION_GAUSSIAN_APPROXIMATION_GATE": "PASS",
                "A_PLANCK_SEMANTICS_GATE": "PASS",
                "NO_LOST_Q032_MULTIPOLE_GATE": "PASS",
                "COSMOLOGY_INDEPENDENT_COMPRESSION_GATE": "PASS",
                "FINAL_COMPRESSION_VALIDATION_GATE": "PASS",
            },
        })
        write_json(args.output, rec)
        print(f"Q040_COMPRESSION_VALIDATION_GATE=PASS implementation={args.implementation}")
        return 0
    except SoftStop as exc:
        rec.update({"failure_class": "HPC", "error": repr(exc)})
        write_json(args.output, rec)
        return 2
    except Exception as exc:
        rec.update({"failure_class": "VALIDATION", "error": repr(exc)})
        write_json(args.output, rec)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        ctx.close()


def make_cmb_likelihood(ells: np.ndarray, mean: np.ndarray, prec: np.ndarray):
    lmax = int(np.max(ells))
    def loglike(A_planck: float, _self=None):
        if _self is None:
            raise RuntimeError("Q040_EXTERNAL_LIKELIHOOD_PROVIDER_GATE=FAIL")
        cls = _self.provider.get_Cl(ell_factor=True)
        tt = np.asarray(cls["tt"], dtype=float)
        if len(tt) <= lmax:
            raise RuntimeError("Q040_EXTERNAL_LIKELIHOOD_LMAX_GATE=FAIL")
        theory = tt[ells] / (float(A_planck) ** 2)
        d = mean - theory
        chi2 = float(d @ (prec @ d))
        if not finite(chi2) or chi2 < 0:
            raise RuntimeError("Q040_EXTERNAL_LIKELIHOOD_FINITE_GATE=FAIL")
        return -0.5 * chi2
    loglike.__name__ = "q040_cmbspace_tt_loglike"
    return loglike, lmax


def remove_marginalized_nuisance(info: dict[str, Any], implementation: str, q32: Any, names: Sequence[str]) -> list[str]:
    params = info.setdefault("params", {})
    likes = info.setdefault("likelihood", {})
    remove = set(map(str, names))
    if implementation == "hillipop":
        remove.update(map(str, q32.load_hillipop_tt_native_param_names()))
        remove.discard("A_planck")
        prefixes = ("q031_shape_",)
    else:
        # Runtime-fixed TT-only CamSpec implementation parameters plus TE/EE calibration remnants.
        remove.update({"use_fg_residual_model", "cal0", "cal2", "amp_100", "n_100", "calTE", "calEE"})
        prefixes = ("q019_shape_",)
    removed = []
    for n in sorted(remove):
        if n in params:
            params.pop(n, None); removed.append(n)
        for prefix in prefixes:
            likes.pop(prefix + n, None)
    if "A_planck" not in params:
        raise RuntimeError("A_PLANCK_PRESERVATION_GATE=FAIL endpoint_info")
    return removed


def profile(args: argparse.Namespace) -> int:
    implementation = args.implementation
    if implementation not in IMPLEMENTATIONS:
        raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
    q32 = load_q032(args.q032_parent_root)
    cfg = q32.load_cfg(resolve_q032_config_path(args.q032_parent_root))
    pf = load_sealed_preflight(args.preflight)
    validation = read_json(args.validation)
    if not (
        validation.get("q") == Q and validation.get("program_id") == PROGRAM_ID
        and validation.get("implementation") == implementation and validation.get("status") == "PASS"
        and validation.get("gates", {}).get("FINAL_COMPRESSION_VALIDATION_GATE") == "PASS"
    ):
        raise RuntimeError("COMPRESSION_VALIDATION_PARENT_GATE=FAIL")
    meta, ells, mean, cov, prec = load_compression(args.compression_meta, args.compression_dir, implementation)
    parent, parent_path = load_parent(args.parent_dir, implementation, args.mask, args.seed)
    start = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
    prefix = Path(args.output).with_suffix("")
    if implementation == "camspec":
        info = q32.build_camspec_info(cfg, start, prefix, "refinement", pf["support_lock"])
        native_component = q32.CAMSPEC
    else:
        info = q32.build_hillipop_info(cfg, start, prefix, "refinement")
        native_component = q32.HILLIPOP
    if native_component not in info.get("likelihood", {}):
        raise RuntimeError("NATIVE_COMPONENT_GATE=FAIL endpoint")
    info["likelihood"].pop(native_component, None)
    removed = remove_marginalized_nuisance(info, implementation, q32, list(meta["nuisance_names"]) + list(meta.get("support_null_nuisance_analytically_factorized", [])))
    fn, lmax = make_cmb_likelihood(ells, mean, prec)
    like_name = f"q040_cmbspace_{implementation}"
    info["likelihood"][like_name] = {
        "external": fn,
        "input_params": ["A_planck"],
        "requires": {"Cl": {"tt": lmax}},
    }
    for name, value in start.items():
        if finite(value):
            q32.set_ref(info["params"], str(name), float(value))
    max_evals, rhoend = q32.objective_settings(cfg, "refinement")
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim.update({"method": "bobyqa", "ignore_prior": True, "best_of": 1, "max_evals": max_evals})
    minim.setdefault("override_bobyqa", {})["rhoend"] = rhoend
    info["output"] = str(prefix.resolve())
    info["force"] = True
    label = f"M{args.mask}-S{args.seed}"
    rec: dict[str, Any] = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "Q040_ENDPOINT", "implementation": implementation,
        "source_mask": int(args.mask), "source_seed": int(args.seed), "source_label": label,
        "source_semantics": "FROZEN_Q032_Q037_LABEL_PROVENANCE",
        "parent_q032_profile": {"path": str(parent_path), "sha256": sha256_file(parent_path)},
        "support_sha256": SUPPORT_HASH, "representation_sha256": meta["representation_sha256"],
        "status": "FAILED", "actual_computed_result": False,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_chi2_sum_performed": False,
        "marginalized_native_nuisance_removed_from_cosmological_likelihood": removed,
        "A_planck_preserved": True,
        "compression_validation_parent": sha256_file(args.validation),
    }
    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(args.soft_stop_minutes) * 60))
    try:
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        minimum = {str(k): float(v) if finite(v) else v for k, v in row.items()}
        for n in COORDS:
            if n not in minimum or not finite(minimum[n]):
                raise RuntimeError(f"FROZEN_GEOMETRY_GATE=FAIL missing={n}")
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]), "minimum": minimum,
            "harvested_minimum_path": source,
            "minimizer": {"method": "bobyqa", "max_evals": max_evals, "rhoend": rhoend, "best_of": 1, "ignore_prior": True},
            "backend_commit": BACKEND_COMMIT,
            "hillipop_commit": HILLIPOP_COMMIT if implementation == "hillipop" else None,
        })
    except SoftStop as exc:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC", "error": repr(exc)})
    except Exception as exc:
        rec.update({"status": "FAILED", "failure_class": "NUMERICAL_OR_LIKELIHOOD", "error": repr(exc)})
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        try:
            if sampler is not None and hasattr(sampler, "close"):
                sampler.close()
        except Exception:
            pass
        write_json(args.output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def collect_endpoints(root: str | Path) -> list[dict[str, Any]]:
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("stage") == "Q040_ENDPOINT":
            out.append(d)
    return out


def assess(args: argparse.Namespace) -> int:
    rows_raw = collect_endpoints(args.endpoint_dir)
    expected = {(i, m, s) for i in IMPLEMENTATIONS for m in (3, 6, 7) for s in (0, 1, 2)}
    complete = [r for r in rows_raw if r.get("status") == "COMPLETE" and r.get("actual_computed_result") is True]
    got = {(str(r["implementation"]), int(r["source_mask"]), int(r["source_seed"])) for r in complete}
    if got != expected or len(complete) != 18:
        raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL got={len(complete)} unique={len(got)}")
    rows: dict[str, dict[str, dict[str, float]]] = {i: {} for i in IMPLEMENTATIONS}
    provenance = {}
    for r in complete:
        label = str(r["source_label"]); impl = str(r["implementation"])
        rows[impl][label] = {n: float(r["minimum"][n]) for n in COORDS}
        provenance[f"{impl}:{label}"] = {
            "objective_chi2_within_implementation_only": float(r["objective_chi2"]),
            "representation_sha256": r["representation_sha256"],
        }
    full = calculate_metrics(rows, LABELS)
    full_sufficient = sufficient(full)
    loo = {}
    for omitted in LABELS:
        labs = [x for x in LABELS if x != omitted]
        m = calculate_metrics(rows, labs)
        loo[omitted] = {"metrics": m, "sufficient": sufficient(m)}
    all_loo = len(loo) == 9 and all(v["sufficient"] for v in loo.values())
    suff = bool(full_sufficient and all_loo)
    classification = "COUPLED_CMBSPACE_BRIDGE_SUFFICIENT" if suff else "COUPLED_CMBSPACE_BRIDGE_INSUFFICIENT"
    reductions = {k: (float(BASELINE[k]) - float(full[k])) / float(BASELINE[k]) for k in BASELINE}
    out = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "Q040_PROVISIONAL", "execution_status": "COMPLETE",
        "tests_status": "PENDING_EXTERNAL_TEST_SCRIPT", "final_result_gate": "PROVISIONAL",
        "actual_computed_result": True,
        "profile_count": 18, "expected_profile_count": 18,
        "support_sha256": SUPPORT_HASH, "scales_sha256": SCALES_HASH,
        "full_sample": {"metrics": full, "sufficient": full_sufficient},
        "leave_one_label_out": loo,
        "all_nine_loo_sufficient": all_loo,
        "sufficient": suff,
        "classification": classification,
        "baseline_q037": BASELINE,
        "continuous_reduction_fraction_vs_q037": reductions,
        "partial_material_reduction_terminal_label_registered": False,
        "endpoint_provenance": provenance,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_chi2_sum_performed": False,
        "interpretation_limits": [
            "This is methodological evidence about Planck likelihood portability, not independent observational confirmation.",
            "A sufficient bridge does not identify a physical Planck systematic or declare either likelihood wrong.",
            "An insufficient bridge does not prove that no upstream coupled mechanism exists.",
        ],
    }
    write_json(args.output, out)
    print("Q040_PROVISIONAL_ASSESSMENT_GATE=PASS")
    return 0


def seal(args: argparse.Namespace) -> int:
    d = read_json(args.provisional)
    t = read_json(args.tests)
    if not (
        d.get("q") == Q and d.get("program_id") == PROGRAM_ID and d.get("stage") == "Q040_PROVISIONAL"
        and d.get("execution_status") == "COMPLETE" and d.get("final_result_gate") == "PROVISIONAL"
    ):
        raise RuntimeError("PROVISIONAL_PARENT_GATE=FAIL")
    if not (t.get("q") == Q and t.get("program_id") == PROGRAM_ID and t.get("status") == "PASS" and t.get("FINAL_RESULT_GATE") == "PASS"):
        raise RuntimeError("RESULT_TEST_PARENT_GATE=FAIL")
    final = copy.deepcopy(d)
    final.update({
        "stage": "Q040_FINAL",
        "tests_status": "COMPLETE",
        "final_result_gate": "PASS",
        "FINAL_RESULT_GATE": "PASS",
        "result_tests_sha256": sha256_file(args.tests),
        "journal_effect": {
            "Q035": "KEEP_CLOSED",
            "Q037": "KEEP_CLOSED_AS_FROZEN_BASELINE",
            "Q038": "KEEP_DESCRIPTIVE_ONLY",
            "Q039": "KEEP_CLOSED_NEGATIVE_BLOCK_TESTS",
            "Q040": "ADD_VALIDATED_COUPLED_CMBSPACE_RESULT",
            "C-036-IMPL": "UPDATE_FROM_Q040_CLASSIFICATION_WITHOUT_CAUSAL_OVERCLAIM",
        },
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    })
    handoff = {
        "current_q": Q,
        "program_id": PROGRAM_ID,
        "scientific_question": load_preregister(args.preregister)["project"]["scientific_question"],
        "new_result": {
            "result_id": RESULT_ID,
            "classification": final["classification"],
            "full_sample": final["full_sample"],
            "leave_one_label_out": final["leave_one_label_out"],
            "continuous_reduction_fraction_vs_q037": final["continuous_reduction_fraction_vs_q037"],
        },
        "journal_effect": final["journal_effect"],
        "sources": list(load_source_lock(args.source_lock)["sources"].keys()),
        "source_lock_sha256": sha256_file(args.source_lock),
        "preregister_sha256": sha256_file(args.preregister),
        "test_status": "PASS",
        "unresolved_issues": [] if final["sufficient"] else ["Residual C-036-IMPL remains after validated CMB-space coupled projection."],
        "next_required_action": "RESULT_INGESTION_AND_SCIENTIFIC_CONCLUSION_ROUTING",
    }
    write_json(args.output, final)
    write_json(args.handoff, handoff)
    print("Q040_FINAL_RESULT_GATE=PASS")
    print("Q040_CLASSIFICATION=" + str(final["classification"]))
    return 0



def seal_compression_failure(args: argparse.Namespace) -> int:
    gate = read_json(args.gate)
    if not (gate.get("q") == Q and gate.get("program_id") == PROGRAM_ID and gate.get("stage") == "Q040_COMPRESSION_GATE" and gate.get("proceed_to_endpoints") is False):
        raise RuntimeError("COMPRESSION_FAILURE_PARENT_GATE=FAIL")
    final = {
        "q": Q, "program_id": PROGRAM_ID, "run_id": RUN_ID, "result_id": RESULT_ID,
        "stage": "Q040_FINAL_TECHNICAL",
        "execution_status": "STOPPED_BEFORE_SCIENCE_ENDPOINTS",
        "tests_status": "COMPRESSION_VALIDATION_INCOMPLETE_OR_FAILED",
        "actual_computed_result": False,
        "classification": "COMPRESSION_VALIDATION_FAIL",
        "scientific_c036_impl_conclusion_available": False,
        "final_result_gate": "UNRESOLVED",
        "FINAL_RESULT_GATE": "UNRESOLVED",
        "compression_gate": gate,
        "support_sha256": SUPPORT_HASH,
        "scales_sha256": SCALES_HASH,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_chi2_sum_performed": False,
        "journal_effect": {
            "Q035": "KEEP_CLOSED",
            "Q037": "KEEP_CLOSED_AS_FROZEN_BASELINE",
            "Q038": "KEEP_DESCRIPTIVE_ONLY",
            "Q039": "KEEP_CLOSED_NEGATIVE_BLOCK_TESTS",
            "Q040": "ADD_METHOD_VALIDATION_FAILURE_WITHOUT_SCIENTIFIC_C036_CONCLUSION",
            "C-036-IMPL": "KEEP_ACTIVE_CAUSE_UNRESOLVED",
        },
        "interpretation_limits": [
            "Compression validation failure is methodological information and is not evidence that no coupled mechanism exists.",
            "No Q040 cosmological endpoint geometry is scientifically interpretable from this stopped path.",
        ],
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    }
    handoff = {
        "current_q": Q,
        "program_id": PROGRAM_ID,
        "scientific_question": load_preregister(args.preregister)["project"]["scientific_question"],
        "new_result": {"result_id": RESULT_ID, "classification": "COMPRESSION_VALIDATION_FAIL", "final_result_gate": "UNRESOLVED"},
        "journal_effect": final["journal_effect"],
        "sources": list(load_source_lock(args.source_lock)["sources"].keys()),
        "source_lock_sha256": sha256_file(args.source_lock),
        "preregister_sha256": sha256_file(args.preregister),
        "test_status": "COMPRESSION_VALIDATION_FAIL",
        "unresolved_issues": ["Native-nuisance-marginalized identity-multipole CMB compression did not validate sufficiently for Q040 science endpoints."],
        "next_required_action": "RESULT_INGESTION_AND_METHOD_FAILURE_ROUTING",
    }
    write_json(args.output, final)
    write_json(args.handoff, handoff)
    print("Q040_COMPRESSION_FAILURE_SEALED=UNRESOLVED")
    return 0

def main() -> None:
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    a = sp.add_parser("validate-parent")
    a.add_argument("--parent-dir", required=True); a.add_argument("--output", required=True)
    a.set_defaults(func=validate_parent)

    def context_args(a: argparse.ArgumentParser) -> None:
        a.add_argument("--q032-parent-root", required=True)
        a.add_argument("--preflight", required=True)
        a.add_argument("--parent-dir", required=True)
        a.add_argument("--preregister", required=True)
        a.add_argument("--source-lock", required=True)
        a.add_argument("--hlp-matrix")
        a.add_argument("--hlp-meta")
        a.add_argument("--scratch", default="q040_runtime")

    a = sp.add_parser("map-start"); context_args(a)
    a.add_argument("--implementation", required=True, choices=IMPLEMENTATIONS)
    a.add_argument("--start-family", required=True, choices=START_FAMILIES)
    a.add_argument("--soft-stop-minutes", type=float, default=300)
    a.add_argument("--output", required=True); a.set_defaults(func=map_start)

    a = sp.add_parser("build-compression"); context_args(a)
    a.add_argument("--implementation", required=True, choices=IMPLEMENTATIONS)
    a.add_argument("--map-dir", required=True)
    a.add_argument("--output-dir", required=True)
    a.add_argument("--metadata-output", required=True)
    a.set_defaults(func=build_compression)

    a = sp.add_parser("validate-compression"); context_args(a)
    a.add_argument("--implementation", required=True, choices=IMPLEMENTATIONS)
    a.add_argument("--compression-meta", required=True)
    a.add_argument("--compression-dir", required=True)
    a.add_argument("--soft-stop-minutes", type=float, default=300)
    a.add_argument("--output", required=True); a.set_defaults(func=validate_compression)

    a = sp.add_parser("profile")
    a.add_argument("--q032-parent-root", required=True)
    a.add_argument("--preflight", required=True)
    a.add_argument("--parent-dir", required=True)
    a.add_argument("--implementation", required=True, choices=IMPLEMENTATIONS)
    a.add_argument("--mask", required=True, type=int, choices=(3,6,7))
    a.add_argument("--seed", required=True, type=int, choices=(0,1,2))
    a.add_argument("--compression-meta", required=True)
    a.add_argument("--compression-dir", required=True)
    a.add_argument("--validation", required=True)
    a.add_argument("--soft-stop-minutes", type=float, default=300)
    a.add_argument("--output", required=True); a.set_defaults(func=profile)

    a = sp.add_parser("assess")
    a.add_argument("--endpoint-dir", required=True); a.add_argument("--output", required=True); a.set_defaults(func=assess)

    a = sp.add_parser("seal")
    a.add_argument("--provisional", required=True); a.add_argument("--tests", required=True)
    a.add_argument("--preregister", required=True); a.add_argument("--source-lock", required=True)
    a.add_argument("--output", required=True); a.add_argument("--handoff", required=True); a.set_defaults(func=seal)

    a = sp.add_parser("seal-compression-failure")
    a.add_argument("--gate", required=True); a.add_argument("--preregister", required=True); a.add_argument("--source-lock", required=True)
    a.add_argument("--output", required=True); a.add_argument("--handoff", required=True); a.set_defaults(func=seal_compression_failure)

    args = p.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
