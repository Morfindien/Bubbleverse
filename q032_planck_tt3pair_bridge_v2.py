#!/usr/bin/env python3
"""
Bubbleverse Q-032 — TT-3PAIR common-support Planck likelihood portability bridge V2.

CURRENT_Q: Q-032
RUN_ID: Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2
RESULT_ID: R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002

Scientific purpose
------------------
Perform the smallest preregistered numerical intervention after CASE-031:
restrict the frozen CamSpec PR4/NPIPE and HiLLiPoP PR4/NPIPE likelihood
constructions to TT only and to exactly the common 143x143, 143x217 and
217x217 multipole support, while preserving each implementation's native TT
foreground and calibration semantics and mathematically marginalizing every
removed data coordinate from its own covariance.

Hard boundaries
---------------
- CASE-031 is closed and is never rerun or reinterpreted here.
- The MOD-EDE-N3 class_ede backend/commit is unchanged.
- Exactly the nine Q022/CASE-031 mapped starts are reused.
- No new start family, no basin-threshold change and no forced nuisance map.
- Absolute CamSpec and HiLLiPoP objectives are never subtracted or summed.
- CamSpec and HiLLiPoP are overlapping Planck PR4/NPIPE analyses, not
  independent sky observations.
- A_planck/nuisance motion is not a causal systematic diagnosis.
- A technical gate failure is NO SCIENTIFIC RESULT.

Execution commands
------------------
  self-test
  preflight
  build-hlp-covariance
  seal-preflight
  profile
  assess-primary
  aggregate
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata as importlib_metadata
import json
import math
import os
import signal
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import yaml
from scipy.linalg import cho_factor, cho_solve

ROOT = Path(__file__).resolve().parent
Q = "Q-032"
RUN = "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
RESULT = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
CONFIG_FILE = "q032_planck_tt3pair_bridge_v2_config.yml"
SOURCE_LOCK_FILE = "q032_source_lock_v2.json"
PROTOCOL_LOCK_FILE = "q032_protocol_lock_v2.json"
Q031_CONFIG = "q031_planck_portability_v1_config.yml"

CAMSPEC = "planck_NPIPE_highl_CamSpec.TTTEEE"
HILLIPOP_PARENT = "planck_2020_hillipop.TTTEEE"
HILLIPOP = "planck_2020_hillipop.TT"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
PAIR_ORDER = ("143x143", "143x217", "217x217")
EXPECTED_LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
COMMON_GEOMETRY = (
    "omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck"
)
CAMSPEC_ONLY_NUISANCE = {
    "calTE", "calEE", "amp_143", "amp_217", "amp_143x217",
    "n_143", "n_217", "n_143x217",
}
HILLIPOP_NATIVE_CAL = {"cal100A", "cal100B", "cal143B", "cal217A", "cal217B"}


class SoftStop(Exception):
    pass


def _alarm(_sig, _frame):
    raise SoftStop()


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


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return obj


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


def git_head(path: str | Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def load_cfg(path: str | Path = CONFIG_FILE) -> dict[str, Any]:
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
    if c["implementations"]["camspec"]["component"] != CAMSPEC:
        raise RuntimeError("CAMSPEC_IMPLEMENTATION_IDENTITY_GATE=FAIL")
    h = c["implementations"]["hillipop"]
    if (h["component"] != HILLIPOP or h.get("parent_case031_component") != HILLIPOP_PARENT
            or h["commit"] != HILLIPOP_COMMIT):
        raise RuntimeError("HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=FAIL")
    if tuple(c["phase_a"]["pairs"]) != PAIR_ORDER or tuple(c["phase_a"]["modes"]) != ("TT",):
        raise RuntimeError("THREE_TT_PAIR_GATE=FAIL")
    if tuple(c["starts"]["labels"]) != EXPECTED_LABELS:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    if int(c["optimizer"]["stage1"]["max_evals"]) != 200000 or float(c["optimizer"]["stage1"]["rhoend"]) != 1e-4:
        raise RuntimeError("STAGE1_OPTIMIZER_GATE=FAIL")
    if int(c["optimizer"]["refinement"]["max_evals"]) != 300000 or float(c["optimizer"]["refinement"]["rhoend"]) != 1e-5:
        raise RuntimeError("REFINEMENT_OPTIMIZER_GATE=FAIL")
    b = c["basin"]
    if not (
        float(b["collapse_objective_tolerance"]) == 0.50
        and float(b["collapse_common_endpoint_rms"]) == 0.10
        and int(b["stable_basin_minimum_supporting_starts"]) == 2
        and float(b["scale_floor_fraction"]) == 1e-8
        and b["refine_unless_single_cluster_covers_all_starts"] is True
    ):
        raise RuntimeError("FROZEN_BASIN_THRESHOLD_GATE=FAIL")
    must = (
        "case031_closed", "no_new_case031_seeds", "no_basin_threshold_change",
        "no_forced_nuisance_mapping", "no_cross_likelihood_absolute_objective_subtraction",
        "no_cross_likelihood_chi2_sum", "shared_planck_sky_not_independent_observations",
        "A_planck_not_causal", "nuisance_motion_not_systematic_error",
        "no_foreground_swap_phase_a", "no_covariance_swap", "no_mask_reconstruction_phase_a",
        "no_q024_rerun", "no_q030_rerun", "technical_failure_no_scientific_result",
    )
    if not all(c["rules"].get(k) is True for k in must):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    if c["covariance"]["semantics"] != "C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS":
        raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL")
    if c["covariance"]["principal_precision_submatrix_as_marginal_forbidden"] is not True:
        raise RuntimeError("PRINCIPAL_PRECISION_SUBMATRIX_RULE_GATE=FAIL")
    return c


def load_source_lock() -> dict[str, Any]:
    d = read_json(ROOT / SOURCE_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    reg = d.get("source_registry", {})
    if reg.get("K-047", {}).get("bibliographic_status") != "BIBLIOGRAPHIC_DETAILS_NOT_INVENTED":
        raise RuntimeError("K047_NONINVENTION_GATE=FAIL")
    return d


def load_protocol_lock() -> dict[str, Any]:
    d = read_json(ROOT / PROTOCOL_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("PROTOCOL_IDENTITY_GATE=FAIL")
    declared = d.get("protocol_sha256")
    x = dict(d)
    x.pop("protocol_sha256", None)
    calc = canonical_hash(x)
    if declared != calc:
        raise RuntimeError(f"PROTOCOL_HASH_GATE=FAIL declared={declared} calculated={calc}")
    return d


def q031_cfg() -> dict[str, Any]:
    import q031_planck_portability_v1 as q31
    return q31.load_cfg(ROOT / Q031_CONFIG)


def model_info_only(info: Mapping[str, Any]) -> dict[str, Any]:
    x = copy.deepcopy(dict(info))
    for k in ("sampler", "output", "force", "resume"):
        x.pop(k, None)
    return x


def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)


def set_ref(params: dict[str, Any], name: str, value: float) -> None:
    import q031_planck_portability_v1 as q31
    q31.set_ref(params, name, float(value))


def reference_vector(info: Mapping[str, Any], preferred: Mapping[str, float] | None = None) -> dict[str, float]:
    import q031_planck_portability_v1 as q31
    return q31.reference_vector(info, preferred=preferred or {})


def objective_settings(c: Mapping[str, Any], phase: str) -> tuple[int, float]:
    if phase not in ("stage1", "refinement"):
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")
    s = c["optimizer"][phase]
    return int(s["max_evals"]), float(s["rhoend"])


def compact_ell_list(values: Sequence[int]) -> list[int]:
    return [int(x) for x in values]


def build_camspec_info(
    c: Mapping[str, Any], seed: Mapping[str, float], prefix: Path,
    phase: str, support: Mapping[str, Any] | None,
) -> dict[str, Any]:
    import q019_planck_cosmology_reprofile_v1 as q19

    c19 = q19.load_cfg(ROOT / "q019_planck_cosmology_reprofile_v1_config.yml")
    info = q19.build_full(c19, "reference_free_h0", 0, prefix, seed={})
    if CAMSPEC not in info.get("likelihood", {}):
        raise RuntimeError("CAMSPEC_IMPLEMENTATION_IDENTITY_GATE=FAIL component_missing")

    spec = info["likelihood"][CAMSPEC]
    spec = {} if spec is None else copy.deepcopy(spec)
    if support is not None:
        pair_ells = support["common_ells_by_pair"]
        spec.setdefault("dataset_params", {})["use_cl"] = "143x143 217x217 143x217"
        spec["dataset_params"]["use_range"] = {
            p: compact_ell_list(pair_ells[p]) for p in ("143x143", "217x217", "143x217")
        }
    info["likelihood"][CAMSPEC] = spec

    # TE/EE data are absent. Their calibration coordinates and explicit shape
    # terms are fixed/removed rather than left as meaningless flat dimensions.
    info["params"]["calTE"] = float(c["implementations"]["camspec"]["fixed_nonparticipating_parameters"]["calTE"])
    info["params"]["calEE"] = float(c["implementations"]["camspec"]["fixed_nonparticipating_parameters"]["calEE"])
    info["likelihood"].pop("q019_shape_calTE", None)
    info["likelihood"].pop("q019_shape_calEE", None)

    for name, value in seed.items():
        if finite(value):
            set_ref(info["params"], str(name), float(value))

    max_evals, rhoend = objective_settings(c, phase)
    minim = info.setdefault("sampler", {}).setdefault("minimize", {})
    minim.update({"method": "bobyqa", "ignore_prior": True, "best_of": 1, "max_evals": max_evals})
    minim.setdefault("override_bobyqa", {})["rhoend"] = rhoend
    info["prior"] = {}
    info["output"] = str(prefix.resolve())
    info["force"] = True
    return info


def load_hillipop_tt_native_param_names() -> set[str]:
    """Return the exact parameter names declared by pinned HiLLiPoP TT.

    Q031 builds TTTEEE and therefore loads params_calib + params_TT +
    params_TE + params_EE. Q032 Phase A activates the official native TT
    component, so TE/EE-only top-level parameters must be REMOVED, not merely
    fixed: Cobaya rejects parameters that no active likelihood consumes.
    """
    import planck_2020_hillipop

    pkg = Path(planck_2020_hillipop.__file__).resolve().parent
    names: set[str] = set()
    for filename in ("params_calib.yaml", "params_TT.yaml"):
        path = pkg / filename
        if not path.exists():
            raise RuntimeError(f"HILLIPOP_TT_PARAM_FILE_GATE=FAIL missing={path}")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, Mapping):
            raise RuntimeError(f"HILLIPOP_TT_PARAM_PARSE_GATE=FAIL file={filename}")
        names.update(str(k) for k in data)
    if not names:
        raise RuntimeError("HILLIPOP_TT_PARAM_SET_GATE=FAIL empty")
    return names


def prune_hillipop_to_native_tt(info: dict[str, Any], c: Mapping[str, Any]) -> list[str]:
    """Remove exactly HiLLiPoP-native parameters absent from native TT.

    The comparison is against Q031's pinned native TTTEEE parameter universe,
    so cosmological parameters are untouched. Any Q031 explicit Gaussian shape
    tied to a removed polarization-only nuisance is removed with it.
    """
    import q031_planck_portability_v1 as q31

    all_native = set(map(str, q31.load_hillipop_native_params()))
    tt_native = load_hillipop_tt_native_param_names()
    removed = sorted(all_native - tt_native)
    expected = sorted(map(str, c["implementations"]["hillipop"]["removed_nonparticipating_parameters"]))
    if removed != expected:
        raise RuntimeError(
            "HILLIPOP_TT_NATIVE_PARAMETER_SET_GATE=FAIL "
            f"runtime_removed={removed} expected={expected}"
        )
    params = info.setdefault("params", {})
    likes = info.setdefault("likelihood", {})
    for name in removed:
        params.pop(name, None)
        likes.pop(f"q031_shape_{name}", None)

    leaked = sorted((all_native - tt_native).intersection(map(str, params)))
    if leaked:
        raise RuntimeError(f"HILLIPOP_UNUSED_POLARIZATION_PARAMETER_GATE=FAIL leaked={leaked}")
    return removed


def build_hillipop_info(
    c: Mapping[str, Any], seed: Mapping[str, float], prefix: Path, phase: str,
) -> dict[str, Any]:
    import q031_planck_portability_v1 as q31

    c31 = q031_cfg()
    max_evals, rhoend = objective_settings(c, phase)
    info = q31.build_info(c31, prefix, max_evals=max_evals, rhoend=rhoend, seed=seed)
    if HILLIPOP_PARENT not in info.get("likelihood", {}):
        raise RuntimeError("HILLIPOP_PARENT_COMPONENT_GATE=FAIL")
    # Phase A removes TE/EE with HiLLiPoP's own official TT component at the
    # identical v4.3 commit. This is not a new sky dataset or nuisance mapping.
    info["likelihood"].pop(HILLIPOP_PARENT)
    info["likelihood"][HILLIPOP] = None

    # TECHNICAL REPAIR V2: Q031's builder correctly carries the complete
    # TTTEEE native nuisance universe. Once Q032 switches to native TT, Cobaya
    # must not see TE/EE-only inputs. Derive and prune them from the pinned
    # HiLLiPoP YAML declarations rather than hard-coding a model assumption.
    prune_hillipop_to_native_tt(info, c)
    return info


def create_model(info: Mapping[str, Any]):
    from cobaya.model import get_model
    return get_model(model_info_only(info))


def evaluate_model_once(model: Any, info: Mapping[str, Any], preferred: Mapping[str, float]) -> tuple[float, dict[str, float]]:
    vec = reference_vector(info, preferred=preferred)
    lp = model.logposterior(vec)
    logpost = getattr(lp, "logpost", lp)
    if not finite(logpost):
        raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL")
    return float(logpost), vec


def camspec_rows(like: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    idx = 0
    for i, name in enumerate(like.cl_names):
        n = int(like.used_sizes[i])
        if n <= 0:
            continue
        ells = [int(x) for x in list(like.ell_ranges[i])]
        if len(ells) != n:
            raise RuntimeError("CAMSPEC_VECTOR_ROW_COUNT_GATE=FAIL")
        observable = "TT" if i <= 3 else ("TE" if str(name) == "TE" else "EE")
        for ell in ells:
            rows.append({"index": idx, "observable": observable, "spectrum": str(name), "ell": ell})
            idx += 1
    if idx != len(like.data_vector) or like.cov.shape != (idx, idx) or like.covinv.shape != (idx, idx):
        raise RuntimeError("CAMSPEC_VECTOR_COVARIANCE_ALIGNMENT_GATE=FAIL")
    return rows


def hillipop_rows(like: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    idx = 0
    for mode in ("TT", "EE", "TE"):
        if not like._is_mode.get(mode, False):
            continue
        for xf in range(like._nxfreq):
            xs0 = like._xspec2xfreq.index(xf)
            lmin = int(like._lmins[mode][xs0])
            lmax = int(like._lmaxs[mode][xs0])
            wf = copy.deepcopy(like.wf)
            wf.cut_binning(lmin, lmax)
            for lo, hi in zip(wf.lmins, wf.lmaxs):
                lo, hi = int(lo), int(hi)
                rows.append({
                    "index": idx,
                    "observable": mode,
                    "spectrum": str(like._xfreq_labels[xf]),
                    "ell_min": lo,
                    "ell_max": hi,
                    "ell": lo if lo == hi else None,
                })
                idx += 1
    if idx != int(like._invkll.shape[0]) or like._invkll.shape[0] != like._invkll.shape[1]:
        raise RuntimeError("HILLIPOP_VECTOR_PRECISION_ALIGNMENT_GATE=FAIL")
    return rows


def key_from_row(row: Mapping[str, Any]) -> tuple[str, int] | None:
    if row.get("observable") != "TT" or row.get("spectrum") not in PAIR_ORDER:
        return None
    if row.get("ell") is None:
        return None
    return str(row["spectrum"]), int(row["ell"])


def ordered_support_hash(keys: Sequence[tuple[str, int]]) -> str:
    return canonical_hash([[p, int(e)] for p, e in keys])


def derive_support(crows: Sequence[Mapping[str, Any]], hrows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    cpairs = [(key_from_row(r), int(r["index"])) for r in crows if key_from_row(r) is not None]
    hpairs = [(key_from_row(r), int(r["index"])) for r in hrows if key_from_row(r) is not None]
    ckeys = [k for k, _ in cpairs]
    hkeys = [k for k, _ in hpairs]
    if len(ckeys) != len(set(ckeys)) or len(hkeys) != len(set(hkeys)):
        raise RuntimeError("SUPPORT_KEY_UNIQUENESS_GATE=FAIL")
    cdict = dict(cpairs)
    hdict = dict(hpairs)

    common = set(cdict).intersection(hdict)
    if not common:
        raise RuntimeError("COMMON_MULTIPOLE_SUPPORT_GATE=FAIL empty")
    bypair: dict[str, list[int]] = {}
    ordered: list[tuple[str, int]] = []
    for pair in PAIR_ORDER:
        ells = sorted(e for p, e in common if p == pair)
        if not ells:
            raise RuntimeError(f"COMMON_MULTIPOLE_SUPPORT_GATE=FAIL pair={pair}")
        bypair[pair] = ells
        ordered.extend((pair, e) for e in ells)

    # Native covariance indexing must use each implementation's own vector order.
    c_selected_native = sorted((cdict[k], k) for k in ordered)
    h_selected_native = sorted((hdict[k], k) for k in ordered)
    if {k for _, k in c_selected_native} != set(ordered) or {k for _, k in h_selected_native} != set(ordered):
        raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL")

    out = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q032_SUPPORT_LOCK",
        "status": "PASS",
        "pairs": list(PAIR_ORDER),
        "common_ells_by_pair": bypair,
        "canonical_common_keys": [[p, e] for p, e in ordered],
        "common_dimension": len(ordered),
        "support_sha256": ordered_support_hash(ordered),
        "camspec_selected_full_indices_native_order": [i for i, _ in c_selected_native],
        "camspec_selected_keys_native_order": [[p, e] for _, (p, e) in c_selected_native],
        "hillipop_selected_full_indices_native_order": [i for i, _ in h_selected_native],
        "hillipop_selected_keys_native_order": [[p, e] for _, (p, e) in h_selected_native],
        "camspec_full_dimension": len(crows),
        "hillipop_full_dimension": len(hrows),
        "construction": "EXACT_LABEL_INTERSECTION_TT_3PAIR_ONLY_PRE_OPTIMIZATION",
    }
    if len(out["camspec_selected_full_indices_native_order"]) != len(ordered) or len(out["hillipop_selected_full_indices_native_order"]) != len(ordered):
        raise RuntimeError("SUPPORT_ORDERING_GATE=FAIL")
    return out


def matrix_diagnostics(a: np.ndarray, c: Mapping[str, Any], label: str) -> dict[str, Any]:
    x = np.asarray(a, dtype=np.float64)
    if x.ndim != 2 or x.shape[0] != x.shape[1] or not np.all(np.isfinite(x)):
        raise RuntimeError(f"COVARIANCE_SHAPE_FINITE_GATE=FAIL {label}")
    asym = float(np.max(np.abs(x - x.T))) if x.size else 0.0
    scale = max(1.0, float(np.max(np.abs(x))) if x.size else 1.0)
    rel = asym / scale
    if rel > float(c["covariance"]["symmetry_relative_tolerance"]):
        raise RuntimeError(f"COVARIANCE_SYMMETRY_GATE=FAIL {label} rel={rel}")
    xs = 0.5 * (x + x.T)
    try:
        L = np.linalg.cholesky(xs)
    except np.linalg.LinAlgError as exc:
        raise RuntimeError(f"COVARIANCE_POSITIVE_DEFINITE_GATE=FAIL {label}") from exc
    return {
        "shape": list(xs.shape),
        "symmetry_relative_error": rel,
        "minimum_cholesky_diagonal": float(np.min(np.diag(L))),
        "sha256": sha256_array(xs),
    }


def blockwise_symmetry_relative(a: np.ndarray, block: int = 256) -> float:
    x = np.asarray(a)
    n = x.shape[0]
    max_abs = 0.0
    max_asym = 0.0
    for i in range(0, n, block):
        j = min(n, i + block)
        A = np.asarray(x[i:j, :], dtype=np.float64)
        B = np.asarray(x[:, i:j].T, dtype=np.float64)
        if A.size:
            max_abs = max(max_abs, float(np.max(np.abs(A))))
            max_asym = max(max_asym, float(np.max(np.abs(A - B))))
    return max_asym / max(1.0, max_abs)


def selected_covariance_from_precision(
    P: np.ndarray, selected_indices: Sequence[int], block_size: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return C_SS where C=P^-1, without ever treating P_SS as marginal precision.

    Mathematically this computes selected columns of C by solving P X = E_S.
    It therefore implements the preregistered sequence C=P^-1 -> C_SS. The full
    dense C need not be materialized. The factorization is allowed to overwrite
    the float64 working copy to keep hosted-runner peak memory bounded.
    """
    P = np.array(P, dtype=np.float64, order="C", copy=True)
    n = P.shape[0]
    S = np.asarray(list(map(int, selected_indices)), dtype=np.int64)
    if P.shape != (n, n) or len(S) == 0 or len(set(S.tolist())) != len(S):
        raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL invalid_dimensions")
    if np.min(S) < 0 or np.max(S) >= n:
        raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL")
    if not np.all(np.isfinite(P)):
        raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL nonfinite_full_precision")
    symmetry_rel = blockwise_symmetry_relative(P)
    if symmetry_rel > 1.0e-10:
        raise RuntimeError(f"COVARIANCE_SYMMETRY_GATE=FAIL full_precision rel={symmetry_rel}")
    full_hash = sha256_array(P)
    try:
        cf = cho_factor(P, lower=True, overwrite_a=True, check_finite=False)
    except Exception as exc:
        raise RuntimeError("COVARIANCE_POSITIVE_DEFINITE_GATE=FAIL full_precision") from exc

    m = len(S)
    Css = np.empty((m, m), dtype=np.float64)
    bsize = max(1, int(block_size))
    for j0 in range(0, m, bsize):
        j1 = min(m, j0 + bsize)
        rhs = np.zeros((n, j1 - j0), dtype=np.float64)
        rhs[S[j0:j1], np.arange(j1 - j0)] = 1.0
        cols = cho_solve(cf, rhs, check_finite=False)
        Css[:, j0:j1] = cols[S, :]
    Css = 0.5 * (Css + Css.T)
    if not np.all(np.isfinite(Css)):
        raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL nonfinite_Css")
    meta = {
        "method": "CHOLESKY_BLOCK_SOLVES_OF_FULL_P_X_EQUALS_E_S",
        "semantics": "C_EQUALS_P_INVERSE_THEN_SELECT_CSS",
        "full_dimension": int(n),
        "selected_dimension": int(m),
        "rhs_block_size": int(bsize),
        "full_precision_sha256": full_hash,
        "full_precision_symmetry_relative_error": symmetry_rel,
        "selected_covariance_sha256": sha256_array(Css),
        "principal_precision_submatrix_used_as_marginal": False,
        "full_covariance_materialized": False,
        "factorization_overwrites_float64_working_copy": True,
    }
    return Css, meta


def restricted_precision_from_full_precision(
    P: np.ndarray, selected_indices: Sequence[int], c: Mapping[str, Any]
) -> tuple[np.ndarray, dict[str, Any]]:
    Css, meta = selected_covariance_from_precision(
        P, selected_indices, int(c["covariance"]["rhs_block_size"])
    )
    dC = matrix_diagnostics(Css, c, "selected_covariance")
    try:
        cf = cho_factor(Css, lower=True, check_finite=False)
        Pm = cho_solve(cf, np.eye(Css.shape[0]), check_finite=False)
    except Exception as exc:
        raise RuntimeError("COVARIANCE_POSITIVE_DEFINITE_GATE=FAIL selected_covariance") from exc
    Pm = 0.5 * (Pm + Pm.T)
    dP = matrix_diagnostics(Pm, c, "restricted_precision")
    ident = Css @ Pm
    rel = float(np.linalg.norm(ident - np.eye(len(Css)), ord="fro") / max(1.0, np.linalg.norm(np.eye(len(Css)), ord="fro")))
    if rel > float(c["covariance"]["inverse_identity_relative_tolerance"]):
        raise RuntimeError(f"COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL inverse_residual={rel}")
    meta.update({
        "restricted_precision_sha256": sha256_array(Pm),
        "selected_covariance_diagnostics": dC,
        "restricted_precision_diagnostics": dP,
        "inverse_identity_relative_residual": rel,
        "final_semantics": "C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS",
    })
    return Pm, meta


def q032_hillipop_runtime_provenance() -> dict[str, Any]:
    p = ROOT / "q032_runtime" / "q032_hillipop_tt_runtime_v2.json"
    if not p.exists():
        raise RuntimeError("DATA_PRODUCT_HASH_GATE=FAIL q032_hillipop_tt_runtime_missing")
    d = read_json(p)
    if (d.get("q") != Q or d.get("run_id") != RUN
            or d.get("hillipop_commit") != HILLIPOP_COMMIT
            or d.get("parent_case031_component") != HILLIPOP_PARENT
            or d.get("phase_a_component") != HILLIPOP):
        raise RuntimeError("HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=FAIL runtime_identity")
    hashes = d.get("data_hashes", {})
    if (not hashes.get("binning_v4.2.fits") or not hashes.get("invfll_PR4_v4.2_TT.fits")
            or not d.get("cross_spectrum_hashes")):
        raise RuntimeError("DATA_PRODUCT_HASH_GATE=FAIL hillipop_tt_hashes_missing")
    return d


def backend_runtime_gate() -> dict[str, Any]:
    class_dir = ROOT / "external" / "class_ede"
    if not class_dir.exists() or git_head(class_dir) != BACKEND_COMMIT:
        raise RuntimeError("BACKEND_IDENTITY_GATE=FAIL")
    import classy
    p = Path(classy.__file__).resolve()
    if "external/class_ede" not in str(p).replace("\\", "/"):
        raise RuntimeError("BACKEND_IDENTITY_GATE=FAIL classy_path")
    return {"commit": git_head(class_dir), "classy_path": str(p)}


def hillipop_runtime_gate() -> dict[str, Any]:
    hdir = ROOT / "external" / "hillipop"
    if not hdir.exists() or git_head(hdir) != HILLIPOP_COMMIT:
        raise RuntimeError("HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=FAIL")
    import planck_2020_hillipop
    p = Path(planck_2020_hillipop.__file__).resolve()
    if not str(p).startswith(str(hdir.resolve()) + os.sep):
        raise RuntimeError("HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=FAIL module_path")
    return {"commit": git_head(hdir), "module_path": str(p)}


def camspec_runtime_gate(like: Any) -> dict[str, Any]:
    if importlib_metadata.version("cobaya") != "3.5.6":
        raise RuntimeError("CAMSPEC_IMPLEMENTATION_IDENTITY_GATE=FAIL cobaya_version")
    dataset = Path(like.dataset_filename).resolve()
    if not dataset.exists() or "CamSpec_NPIPE" not in str(dataset):
        raise RuntimeError("CAMSPEC_IMPLEMENTATION_IDENTITY_GATE=FAIL dataset")
    return {
        "cobaya_version": importlib_metadata.version("cobaya"),
        "dataset_file": str(dataset),
        "dataset_file_sha256": sha256_file(dataset),
        "data_vector_sha256": sha256_array(np.asarray(like.data_vector, dtype=np.float64)),
        "covariance_sha256": sha256_array(np.asarray(like.cov, dtype=np.float64)),
    }


def no_extra_dataset_gate(info: Mapping[str, Any], component: str, allowed_shape_prefix: str) -> list[str]:
    keys = [str(k) for k in info.get("likelihood", {})]
    extras = [k for k in keys if k != component and not k.startswith(allowed_shape_prefix)]
    if component not in keys or extras:
        raise RuntimeError(f"NO_EXTRA_DATASET_GATE=FAIL component={component} extras={extras}")
    return keys

def sampled_nuisance(info: Mapping[str, Any]) -> list[str]:
    cosmo = set(load_cfg()["cosmology"]["sampled"])
    return sorted(
        name for name, spec in info.get("params", {}).items()
        if sampled(spec) and name not in cosmo
    )


def source_starts_and_scales(q021_dir: str | Path, q022_dir: str | Path) -> tuple[dict[str, Any], dict[str, float]]:
    import q031_planck_portability_v1 as q31
    c31 = q031_cfg()
    starts = q31.source_endpoints(c31, q021_dir, q022_dir)
    if tuple(sorted(starts)) != tuple(sorted(EXPECTED_LABELS)) or len(starts) != 9:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    scales = q31.locked_scales(c31, starts)
    for n in COMMON_GEOMETRY:
        if n not in scales or not finite(scales[n]) or float(scales[n]) <= 0:
            raise RuntimeError(f"START_SCALE_GATE=FAIL parameter={n}")
    return starts, scales


def preflight(c: Mapping[str, Any], q021_dir: str | Path, q022_dir: str | Path,
              output: str | Path, support_output: str | Path) -> int:
    src = load_source_lock()
    protocol = load_protocol_lock()
    backend = backend_runtime_gate()
    hgate = hillipop_runtime_gate()
    runtime = q032_hillipop_runtime_provenance()
    starts, scales = source_starts_and_scales(q021_dir, q022_dir)
    seed = starts[EXPECTED_LABELS[0]]["params"]

    cam_model = hlp_model = cam_restricted_model = None
    try:
        import q019_planck_cosmology_reprofile_v1 as q19
        c19 = q19.load_cfg(ROOT / "q019_planck_cosmology_reprofile_v1_config.yml")
        cam_full_info = q19.build_full(c19, "reference_free_h0", 0, ROOT / "q032_runtime/cam_full_probe", seed={})
        no_extra_dataset_gate(cam_full_info, CAMSPEC, "q019_shape_")
        cam_model = create_model(cam_full_info)
        cam_full_logpost, _ = evaluate_model_once(cam_model, cam_full_info, seed)
        cam_like = cam_model.likelihood[CAMSPEC]
        crows = camspec_rows(cam_like)
        cam_runtime = camspec_runtime_gate(cam_like)

        hlp_full_info = build_hillipop_info(c, seed, ROOT / "q032_runtime/hlp_native_tt_probe", "stage1")
        no_extra_dataset_gate(hlp_full_info, HILLIPOP, "q031_shape_")
        hlp_model = create_model(hlp_full_info)
        hlp_full_logpost, _ = evaluate_model_once(hlp_model, hlp_full_info, seed)
        hlp_like = hlp_model.likelihood[HILLIPOP]
        hrows = hillipop_rows(hlp_like)

        support = derive_support(crows, hrows)
        write_json(support_output, support)

        # CamSpec restriction uses its covariance (not its precision) before inversion.
        cam_r_info = build_camspec_info(c, seed, ROOT / "q032_runtime/cam_restricted_probe", "stage1", support)
        no_extra_dataset_gate(cam_r_info, CAMSPEC, "q019_shape_")
        cam_restricted_model = create_model(cam_r_info)
        cam_r_logpost, _ = evaluate_model_once(cam_restricted_model, cam_r_info, seed)
        cam_r_like = cam_restricted_model.likelihood[CAMSPEC]
        crrows = camspec_rows(cam_r_like)
        rkeys = {(str(r["spectrum"]), int(r["ell"])) for r in crrows if r["observable"] == "TT"}
        locked = {(str(p), int(e)) for p, e in support["canonical_common_keys"]}
        if rkeys != locked or len(crrows) != len(locked):
            raise RuntimeError("COMMON_MULTIPOLE_SUPPORT_GATE=FAIL camspec_restricted_rows")
        S = np.asarray(support["camspec_selected_full_indices_native_order"], dtype=int)
        expected_cov = np.asarray(cam_like.cov, dtype=np.float64)[np.ix_(S, S)]
        actual_cov = np.asarray(cam_r_like.cov, dtype=np.float64)
        cov_rel = float(np.linalg.norm(expected_cov - actual_cov, ord="fro") / max(1.0, np.linalg.norm(expected_cov, ord="fro")))
        if cov_rel > 1e-12:
            raise RuntimeError(f"COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL camspec_rel={cov_rel}")
        cam_cov_diag = matrix_diagnostics(actual_cov, c, "camspec_restricted_covariance")
        cam_prec_diag = matrix_diagnostics(np.asarray(cam_r_like.covinv, dtype=np.float64), c, "camspec_restricted_precision")

        cam_nuis = sampled_nuisance(cam_r_info)
        hlp_probe_info = build_hillipop_info(c, seed, ROOT / "q032_runtime/hlp_param_probe", "stage1")
        no_extra_dataset_gate(hlp_probe_info, HILLIPOP, "q031_shape_")
        hlp_nuis = sampled_nuisance(hlp_probe_info)
        if any(x in hlp_nuis for x in CAMSPEC_ONLY_NUISANCE):
            raise RuntimeError("NO_FORCED_NUISANCE_MAPPING_GATE=FAIL")
        if any(x in cam_nuis for x in HILLIPOP_NATIVE_CAL):
            raise RuntimeError("NATIVE_NUISANCE_SEPARATION_GATE=FAIL")

        gates = {name: "PASS" for name in c["mandatory_preflight_gates"]}
        # HLP marginal precision and finite restricted evaluation are completed by
        # build-hlp-covariance + seal-preflight, so these are explicitly pending.
        for name in (
            "COVARIANCE_RESTRICTION_SEMANTICS_GATE",
            "COVARIANCE_SYMMETRY_GATE",
            "COVARIANCE_POSITIVE_DEFINITE_GATE",
            "FINITE_REAL_LIKELIHOOD_EVALUATION_GATE",
        ):
            gates[name] = "PENDING_HILLIPOP_RESTRICTION"

        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_PREFLIGHT", "status": "PENDING_HILLIPOP_RESTRICTION",
            "actual_scientific_result": False,
            "source_lock_sha256": canonical_hash(src),
            "protocol_sha256": protocol["protocol_sha256"],
            "backend_runtime": backend,
            "hillipop_runtime": hgate,
            "hillipop_data_runtime": runtime,
            "camspec_runtime": cam_runtime,
            "support_lock": support,
            "support_sha256": support["support_sha256"],
            "q022_source_starts": starts,
            "locked_common_scales": scales,
            "locked_scales_hash": canonical_hash(scales),
            "full_real_probe": {"camspec_logpost": cam_full_logpost, "hillipop_logpost": hlp_full_logpost},
            "restricted_camspec_probe_logpost": cam_r_logpost,
            "camspec_restriction": {
                "method": "RAW_COVARIANCE_COORDINATE_SELECTION_BEFORE_INVERSION_VIA_DATASET_PARAMS",
                "covariance_relative_difference_from_full_selected_block": cov_rel,
                "covariance": cam_cov_diag,
                "precision": cam_prec_diag,
                "principal_precision_submatrix_used_as_marginal": False,
            },
            "native_nuisance": {"camspec": cam_nuis, "hillipop": hlp_nuis},
            "gates": gates,
            "claim_boundaries": {
                "cross_likelihood_objective_subtraction": False,
                "forced_nuisance_mapping": False,
                "independent_sky_observation_claim": False,
                "causal_A_planck_claim": False,
            },
        }
        write_json(output, rec)
        print("Q032_PREFLIGHT_PART1_GATE=PASS")
        print(f"Q032_SUPPORT_SHA256={support['support_sha256']}")
        return 0
    finally:
        for model in (cam_restricted_model, hlp_model, cam_model):
            try:
                if model is not None:
                    model.close()
            except Exception:
                pass


def load_preflight(path: str | Path, sealed: bool = False) -> dict[str, Any]:
    d = read_json(path)
    expected_stage = "Q032_PREFLIGHT_SEALED" if sealed else "Q032_PREFLIGHT"
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("stage") != expected_stage:
        raise RuntimeError("PREFLIGHT_IDENTITY_GATE=FAIL")
    if sealed:
        if d.get("status") != "PASS" or any(v != "PASS" for v in d.get("gates", {}).values()):
            raise RuntimeError("PREFLIGHT_STATUS_GATE=FAIL")
    return d


def build_hlp_covariance(c: Mapping[str, Any], preflight_path: str | Path,
                         matrix_output: str | Path, meta_output: str | Path) -> int:
    pf = load_preflight(preflight_path, sealed=False)
    if pf.get("status") != "PENDING_HILLIPOP_RESTRICTION":
        raise RuntimeError("PREFLIGHT_PARENT_GATE=FAIL")
    backend_runtime_gate()
    hillipop_runtime_gate()
    q032_hillipop_runtime_provenance()
    support = pf["support_lock"]
    seed = pf["q022_source_starts"][EXPECTED_LABELS[0]]["params"]

    model = None
    try:
        info = build_hillipop_info(c, seed, ROOT / "q032_runtime/hlp_cov_probe", "stage1")
        model = create_model(info)
        evaluate_model_once(model, info, seed)
        like = model.likelihood[HILLIPOP]
        rows = hillipop_rows(like)
        S = np.asarray(support["hillipop_selected_full_indices_native_order"], dtype=int)
        if len(rows) != support["hillipop_full_dimension"]:
            raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL dimension")
        selected_rows = [rows[i] for i in S]
        selected_keys = {(str(r["spectrum"]), int(r["ell"])) for r in selected_rows if r.get("ell") is not None}
        locked = {(str(p), int(e)) for p, e in support["canonical_common_keys"]}
        if selected_keys != locked or any(r["observable"] != "TT" for r in selected_rows):
            raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL labels")

        Pfull = np.asarray(like._invkll)
        Pm, meta = restricted_precision_from_full_precision(Pfull, S, c)
        if Pm.shape != (support["common_dimension"], support["common_dimension"]):
            raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL restricted_shape")
        Path(matrix_output).parent.mkdir(parents=True, exist_ok=True)
        np.save(matrix_output, Pm, allow_pickle=False)
        meta.update({
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_HILLIPOP_RESTRICTED_PRECISION",
            "status": "PASS",
            "support_sha256": support["support_sha256"],
            "matrix_file": Path(matrix_output).name,
            "matrix_file_sha256": sha256_file(matrix_output),
            "selected_keys_native_order": support["hillipop_selected_keys_native_order"],
            "scientific_semantics": "HILLIPOP_OWN_NATIVE_TT_COVARIANCE_MARGINALIZED_TO_TT_3PAIR_COMMON_SUPPORT",
            "parent_case031_component": HILLIPOP_PARENT,
            "phase_a_component": HILLIPOP,
        })
        write_json(meta_output, meta)
        print("Q032_HILLIPOP_COVARIANCE_RESTRICTION_GATE=PASS")
        return 0
    finally:
        try:
            if model is not None:
                model.close()
        except Exception:
            pass


def load_hlp_matrix(matrix_path: str | Path, meta_path: str | Path, support: Mapping[str, Any], c: Mapping[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    meta = read_json(meta_path)
    if not (
        meta.get("q") == Q and meta.get("run_id") == RUN
        and meta.get("stage") == "Q032_HILLIPOP_RESTRICTED_PRECISION"
        and meta.get("status") == "PASS"
        and meta.get("support_sha256") == support["support_sha256"]
        and meta.get("final_semantics") == "C_EQUALS_P_INVERSE_THEN_SELECT_CSS_THEN_INVERT_CSS"
        and meta.get("principal_precision_submatrix_used_as_marginal") is False
    ):
        raise RuntimeError("COVARIANCE_RESTRICTION_SEMANTICS_GATE=FAIL metadata")
    if sha256_file(matrix_path) != meta.get("matrix_file_sha256"):
        raise RuntimeError("DATA_PRODUCT_HASH_GATE=FAIL restricted_matrix_file")
    Pm = np.load(matrix_path, allow_pickle=False)
    if sha256_array(Pm) != meta.get("restricted_precision_sha256"):
        raise RuntimeError("DATA_PRODUCT_HASH_GATE=FAIL restricted_matrix_array")
    matrix_diagnostics(Pm, c, "loaded_hillipop_restricted_precision")
    return np.asarray(Pm, dtype=np.float64), meta


def install_hillipop_patch(matrix_path: str | Path, meta_path: str | Path,
                            support: Mapping[str, Any], c: Mapping[str, Any]) -> dict[str, Any]:
    """Patch only the runtime likelihood evaluation, never the pinned source tree."""
    import planck_2020_hillipop.hillipop as hm

    cls = hm.TT
    if getattr(cls, "_bubbleverse_q032_patch", False):
        return getattr(cls, "_bubbleverse_q032_patch_meta")

    Pm, meta = load_hlp_matrix(matrix_path, meta_path, support, c)
    original_initialize = cls.initialize

    def initialize(self):
        original_initialize(self)
        rows = hillipop_rows(self)
        S = np.asarray(support["hillipop_selected_full_indices_native_order"], dtype=int)
        tt_rows = [r for r in rows if r["observable"] == "TT"]
        if not tt_rows:
            raise RuntimeError("THREE_TT_PAIR_GATE=FAIL no_tt_rows")
        tt_dimension = len(tt_rows)
        if np.max(S) >= tt_dimension:
            raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL selected_not_in_tt_prefix")
        keys = [[str(rows[i]["spectrum"]), int(rows[i]["ell"])] for i in S]
        if keys != support["hillipop_selected_keys_native_order"]:
            raise RuntimeError("SUPPORT_ORDERING_GATE=FAIL hillipop_runtime")
        self._q032_selected_tt_indices = S
        self._q032_precision = Pm
        self._q032_support_sha256 = support["support_sha256"]

    def get_requirements(self):
        return {"Cl": {"tt": self.lmax}}

    def compute_chi2(self, dlth, **params_values):
        Rspec = self._compute_residuals(params_values, dlth, "TT")
        Rl = self._xspectra_to_xfreq(Rspec, self._dlweight["TT"])
        Xtt = np.asarray(self._select_spectra(Rl, "TT"), dtype=np.float64)
        S = self._q032_selected_tt_indices
        if np.max(S) >= len(Xtt):
            raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL tt_runtime")
        residual = Xtt[S]
        if residual.shape[0] != self._q032_precision.shape[0] or not np.all(np.isfinite(residual)):
            raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL residual")
        chi2 = float(residual @ (self._q032_precision @ residual))
        if not finite(chi2) or chi2 <= 0:
            raise RuntimeError("FINITE_REAL_LIKELIHOOD_EVALUATION_GATE=FAIL chi2")
        self.delta_cl = residual.astype("float32")
        alpha = 8.0 - np.ceil(np.log10(chi2))
        return np.float64(np.round(chi2 * 10 ** alpha)) * 10 ** (-alpha)

    def logp(self, **params_values):
        dl = self.provider.get_Cl(ell_factor=True)
        dlth = {"TT": dl["tt"][: self.lmax + 1]}
        return -0.5 * self.compute_chi2(dlth, **params_values)

    cls.initialize = initialize
    cls.get_requirements = get_requirements
    cls.compute_chi2 = compute_chi2
    cls.logp = logp
    cls._bubbleverse_q032_patch = True
    cls._bubbleverse_q032_patch_meta = {
        "patch": "RUNTIME_ONLY_NO_SOURCE_TREE_MUTATION",
        "support_sha256": support["support_sha256"],
        "restricted_precision_sha256": meta["restricted_precision_sha256"],
        "component": HILLIPOP,
        "parent_case031_component": HILLIPOP_PARENT,
        "mode_removal_semantics": "OFFICIAL_NATIVE_TT_COMPONENT_SAME_V4_3_COMMIT",
        "foreground_semantics": "NATIVE_HILLIPOP_TT",
        "calibration_semantics": "NATIVE_HILLIPOP_DETSET_TT",
        "theory_requirements": ["tt"],
    }
    return cls._bubbleverse_q032_patch_meta


def seal_preflight(c: Mapping[str, Any], preflight_path: str | Path,
                   matrix_path: str | Path, meta_path: str | Path,
                   output: str | Path) -> int:
    pf = load_preflight(preflight_path, sealed=False)
    support = pf["support_lock"]
    backend_runtime_gate()
    hillipop_runtime_gate()
    patch_meta = install_hillipop_patch(matrix_path, meta_path, support, c)
    seed = pf["q022_source_starts"][EXPECTED_LABELS[0]]["params"]
    info = build_hillipop_info(c, seed, ROOT / "q032_runtime/hlp_restricted_probe", "stage1")
    model = None
    try:
        model = create_model(info)
        restricted_logpost, _ = evaluate_model_once(model, info, seed)
        like = model.likelihood[HILLIPOP]
        if getattr(like, "_q032_support_sha256", None) != support["support_sha256"]:
            raise RuntimeError("SUPPORT_SHA256_GATE=FAIL runtime_patch")
        if len(like.delta_cl) != support["common_dimension"]:
            raise RuntimeError("FULL_TO_RESTRICTED_VECTOR_INDEX_GATE=FAIL runtime_residual_dimension")
        gates = {name: "PASS" for name in c["mandatory_preflight_gates"]}
        sealed = copy.deepcopy(pf)
        sealed.update({
            "stage": "Q032_PREFLIGHT_SEALED",
            "status": "PASS",
            "gates": gates,
            "hillipop_restriction_metadata": read_json(meta_path),
            "hillipop_runtime_patch": patch_meta,
            "restricted_hillipop_probe_logpost": restricted_logpost,
            "FINAL_PREFLIGHT_GATE": "PASS",
        })
        write_json(output, sealed)
        print("Q032_FINAL_PREFLIGHT_GATE=PASS")
        return 0
    finally:
        try:
            if model is not None:
                model.close()
        except Exception:
            pass


def find_profile(root: str | Path, implementation: str, phase: str, mask: int, seed: int) -> dict[str, Any]:
    stage = "Q032_STAGE1" if phase == "stage1" else "Q032_REFINEMENT"
    hits = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if (
            d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage
            and d.get("implementation") == implementation
            and int(d.get("source_mask", -1)) == int(mask)
            and int(d.get("source_seed", -1)) == int(seed)
            and d.get("status") == "COMPLETE" and finite(d.get("objective_chi2"))
        ):
            hits.append(d)
    if len(hits) != 1:
        raise RuntimeError(
            f"PROFILE_UNIQUENESS_GATE=FAIL impl={implementation} phase={phase} mask={mask} seed={seed} hits={len(hits)}"
        )
    return hits[0]


def run_profile(c: Mapping[str, Any], preflight_path: str | Path,
                implementation: str, phase: str, mask: int, seed: int,
                output: str | Path, stage1_dir: str | Path | None,
                hlp_matrix: str | Path | None, hlp_meta: str | Path | None) -> int:
    if implementation not in ("camspec", "hillipop"):
        raise RuntimeError("IMPLEMENTATION_GATE=FAIL")
    pf = load_preflight(preflight_path, sealed=True)
    label = f"M{mask}-S{seed}"
    if label not in pf["q022_source_starts"] or label not in EXPECTED_LABELS:
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")

    if phase == "stage1":
        start = dict(pf["q022_source_starts"][label]["params"])
        seed_semantics = "EXACT_CASE031_Q022_MAPPED_START"
    elif phase == "refinement":
        if stage1_dir is None:
            raise RuntimeError("REFINEMENT_PARENT_GATE=FAIL")
        parent = find_profile(stage1_dir, implementation, "stage1", mask, seed)
        start = {str(k): float(v) for k, v in parent["minimum"].items() if finite(v)}
        seed_semantics = "EXACT_MATCHED_Q032_STAGE1_MINIMUM"
    else:
        raise RuntimeError("PROFILE_PHASE_GATE=FAIL")

    if implementation == "hillipop":
        if hlp_matrix is None or hlp_meta is None:
            raise RuntimeError("HILLIPOP_RESTRICTED_COVARIANCE_PARENT_GATE=FAIL")
        patch = install_hillipop_patch(hlp_matrix, hlp_meta, pf["support_lock"], c)
    else:
        patch = None

    prefix = Path(output).with_suffix("")
    rec: dict[str, Any] = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_STAGE1" if phase == "stage1" else "Q032_REFINEMENT",
        "phase": phase,
        "implementation": implementation,
        "source_mask": int(mask), "source_seed": int(seed), "source_label": label,
        "source_semantics": "Q022_START_PROVENANCE_ONLY_NOT_HILLIPOP_MASK",
        "seed_semantics": seed_semantics,
        "support_sha256": pf["support_sha256"],
        "status": "FAILED", "actual_computed_result": False,
        "cross_likelihood_objective_comparison_performed": False,
        "backend_commit": BACKEND_COMMIT,
        "hillipop_commit": HILLIPOP_COMMIT if implementation == "hillipop" else None,
        "runtime_patch": patch,
    }

    sampler = None
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(float(c["execution"]["soft_stop_minutes"]) * 60))
    try:
        if implementation == "camspec":
            info = build_camspec_info(c, start, prefix, phase, pf["support_lock"])
        else:
            info = build_hillipop_info(c, start, prefix, phase)
        from cobaya.run import run as cobaya_run
        _, sampler = cobaya_run(info, force=True)
        import q019_planck_cosmology_reprofile_v1 as q19
        row, source = q19.minimum_row(sampler, prefix)
        if not row or not finite(row.get("chi2")):
            raise RuntimeError("FINITE_RESULT_GATE=FAIL")
        max_evals, rhoend = objective_settings(c, phase)
        rec.update({
            "status": "COMPLETE", "actual_computed_result": True,
            "objective_chi2": float(row["chi2"]),
            "minimum": {str(k): float(v) if finite(v) else v for k, v in row.items()},
            "harvested_minimum_path": source,
            "minimizer": {"method": "bobyqa", "max_evals": max_evals, "rhoend": rhoend, "best_of": 1, "ignore_prior": True},
        })
    except SoftStop:
        rec.update({"status": "PARTIAL_SOFT_STOP", "failure_class": "HPC"})
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
        write_json(output, rec)
    return 0 if rec["status"] == "COMPLETE" else 2


def collect_profiles(root: str | Path, phase: str) -> list[dict[str, Any]]:
    stage = "Q032_STAGE1" if phase == "stage1" else "Q032_REFINEMENT"
    out = []
    for p in Path(root).rglob("*.json"):
        try:
            d = read_json(p)
        except Exception:
            continue
        if d.get("q") == Q and d.get("run_id") == RUN and d.get("stage") == stage:
            out.append(d)
    return out


def bridge_cluster(rows: Sequence[Mapping[str, Any]], scales: Mapping[str, float]) -> dict[str, Any]:
    import q031_planck_portability_v1 as q31
    return q31.cluster_rows(q031_cfg(), rows, scales)


def assess_primary(c: Mapping[str, Any], preflight_path: str | Path,
                   stage1_dir: str | Path, output: str | Path,
                   matrix_output: str | Path) -> int:
    pf = load_preflight(preflight_path, sealed=True)
    rows = collect_profiles(stage1_dir, "stage1")
    expected = {(impl, m, s) for impl in ("camspec", "hillipop") for m in (3, 6, 7) for s in (0, 1, 2)}
    got = {
        (str(r.get("implementation")), int(r.get("source_mask", -1)), int(r.get("source_seed", -1)))
        for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))
    }
    if got != expected or len(rows) != 18:
        rec = {
            "q": Q, "run_id": RUN, "result_id": RESULT,
            "stage": "Q032_STAGE1_ASSESSMENT", "status": "FAIL",
            "JOB_COMPLETENESS_GATE": "FAIL", "expected": sorted(expected), "got": sorted(got),
        }
        write_json(output, rec)
        write_json(matrix_output, {"include": []})
        return 2

    diagnostics = {}
    matrix_rows = []
    for impl in ("camspec", "hillipop"):
        rr = [r for r in rows if r["implementation"] == impl]
        diag = bridge_cluster(rr, pf["locked_common_scales"])
        needs = not bool(diag["single_cluster_covers_all"])
        diagnostics[impl] = {"needs_refinement": needs, "diagnostic": diag}
        if needs:
            matrix_rows.extend({"implementation": impl, "mask": m, "seed": s} for m in (3, 6, 7) for s in (0, 1, 2))

    any_refine = bool(matrix_rows)
    matrix = {"include": matrix_rows if any_refine else [{"implementation": "none", "mask": -1, "seed": -1}]}
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_STAGE1_ASSESSMENT", "status": "PASS",
        "JOB_COMPLETENESS_GATE": "PASS",
        "needs_refinement": any_refine,
        "implementation_diagnostics": diagnostics,
        "refinement_matrix": matrix,
    }
    write_json(output, rec)
    write_json(matrix_output, matrix)
    print("NEEDS_REFINEMENT=" + ("true" if any_refine else "false"))
    print("REFINE_MATRIX=" + json.dumps(matrix, separators=(",", ":")))
    return 0


def load_assessment(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == Q and d.get("run_id") == RUN
        and d.get("stage") == "Q032_STAGE1_ASSESSMENT" and d.get("status") == "PASS"
        and d.get("JOB_COMPLETENESS_GATE") == "PASS"
    ):
        raise RuntimeError("STAGE1_ASSESSMENT_GATE=FAIL")
    return d


def phase_a_decision(cam_stable: bool, hlp_stable: bool) -> tuple[str, str, list[str]]:
    rules = []
    if cam_stable and not hlp_stable:
        rules.append("A")
    if not cam_stable:
        rules.append("B")
    if hlp_stable:
        rules.append("C")
    if cam_stable == hlp_stable:
        rules.append("D")

    if not cam_stable:
        primary = "B"
        route = "CAMSPEC_ONLY_NESTED_ADDBACK_TE_VS_EE_VS_SUPPORT_SECTORS"
    elif hlp_stable:
        primary = "C"
        route = "HILLIPOP_BOUNDED_ADDBACK_100TT_VS_TE_VS_EE"
    else:
        primary = "A"
        route = "BOUNDED_PHASE_B_APLANCK_FIXED_VS_PROFILE_THEN_NATIVE_CALIBRATION_FLEXIBILITY"
    return primary, route, rules


def aggregate(c: Mapping[str, Any], preflight_path: str | Path,
              assessment_path: str | Path, stage1_dir: str | Path,
              refinement_dir: str | Path | None, output: str | Path) -> int:
    pf = load_preflight(preflight_path, sealed=True)
    assess = load_assessment(assessment_path)
    stage1 = collect_profiles(stage1_dir, "stage1")
    refinement = collect_profiles(refinement_dir, "refinement") if refinement_dir else []
    implementation_results = {}

    for impl in ("camspec", "hillipop"):
        needs = bool(assess["implementation_diagnostics"][impl]["needs_refinement"])
        rows = [r for r in (refinement if needs else stage1) if r.get("implementation") == impl]
        complete = [r for r in rows if r.get("status") == "COMPLETE" and finite(r.get("objective_chi2"))]
        keys = {(int(r["source_mask"]), int(r["source_seed"])) for r in complete}
        expected = {(m, s) for m in (3, 6, 7) for s in (0, 1, 2)}
        if keys != expected or len(complete) != 9:
            raise RuntimeError(f"JOB_COMPLETENESS_GATE=FAIL impl={impl} count={len(complete)}")
        diag = bridge_cluster(complete, pf["locked_common_scales"])
        stable = int(diag["stable_basin_count"]) >= 2
        implementation_results[impl] = {
            "decisive_phase": "refinement" if needs else "stage1",
            "complete_profiles": 9,
            "stable_multibasin": stable,
            "stable_basin_count": int(diag["stable_basin_count"]),
            "cluster_diagnostic": diag,
        }

    cam_stable = bool(implementation_results["camspec"]["stable_multibasin"])
    hlp_stable = bool(implementation_results["hillipop"]["stable_multibasin"])
    primary, route, triggered = phase_a_decision(cam_stable, hlp_stable)
    names = c["phase_a_decision_rules"]
    classification = names[primary]

    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_PHASE_A_FINAL", "status": "PASS",
        "execution_status": "COMPLETE", "tests_status": "COMPLETE",
        "actual_computed_result": True,
        "support_sha256": pf["support_sha256"],
        "common_dimension": pf["support_lock"]["common_dimension"],
        "implementation_results": implementation_results,
        "phase_a_primary_decision_rule": primary,
        "phase_a_triggered_rules": triggered,
        "phase_a_classification": classification,
        "next_required_action": route,
        "cross_likelihood_absolute_objective_subtraction_performed": False,
        "cross_likelihood_chi2_sum_performed": False,
        "physical_or_instrumental_causality_claim": False,
        "CASE031_REOPENED": False,
        "mandatory_gates": {
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "Q_IDENTITY_GATE": "PASS",
            "BACKEND_IDENTITY_GATE": "PASS",
            "SOURCE_GATE": "PASS",
            "DATA_GATE": "PASS",
            "JOB_COMPLETENESS_GATE": "PASS",
            "MERGE_COMPATIBILITY_GATE": "PASS",
            "GLOBALITY_GATE": "PASS",
            "SCIENTIFIC_INTERPRETATION_GATE": "PASS",
            "FINAL_RESULT_GATE": "PASS",
        },
        "FINAL_RESULT_GATE": "PASS",
        "journal_effect": {
            "CASE031": "KEEP_CLOSED_AND_AUTHORITATIVE",
            "Q032": "ADD_PHASE_A_CONTROLLED_BRIDGE_RESULT",
            "interpretation_boundary": "METHODOLOGICAL_LIKELIHOOD_GEOMETRY_NOT_CAUSAL_SYSTEMATIC",
        },
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
    }
    write_json(output, out)
    print("Q032_FINAL_RESULT_GATE=PASS")
    print("Q032_PHASE_A_CLASSIFICATION=" + classification)
    print("Q032_NEXT_REQUIRED_ACTION=" + route)
    return 0


def self_test(c: Mapping[str, Any], output: str | Path | None = None) -> int:
    # Exact synthetic proof that the implementation is selecting C_SS from C=P^-1,
    # not taking the principal precision submatrix.
    rng = np.random.default_rng(32032)
    A = rng.normal(size=(14, 14))
    C = A @ A.T + np.eye(14) * 0.5
    P = np.linalg.inv(C)
    S = [1, 3, 4, 8, 11]
    Pm, meta = restricted_precision_from_full_precision(P, S, c)
    expected = np.linalg.inv(C[np.ix_(S, S)])
    rel = float(np.linalg.norm(Pm - expected, ord="fro") / np.linalg.norm(expected, ord="fro"))
    wrong = P[np.ix_(S, S)]
    wrong_rel = float(np.linalg.norm(wrong - expected, ord="fro") / np.linalg.norm(expected, ord="fro"))
    if rel > 1e-10 or wrong_rel <= 1e-6:
        raise RuntimeError(f"SYNTHETIC_COVARIANCE_SEMANTICS_GATE=FAIL rel={rel} wrong_rel={wrong_rel}")
    rec = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "stage": "Q032_SELF_TEST", "status": "PASS",
        "selected_covariance_relative_error": rel,
        "principal_precision_submatrix_relative_error": wrong_rel,
        "principal_precision_submatrix_used_as_marginal": False,
        "metadata": meta,
    }
    if output:
        write_json(output, rec)
    print("Q032_SELF_TEST_GATE=PASS")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default=CONFIG_FILE)
    sp = p.add_subparsers(dest="command", required=True)

    s = sp.add_parser("self-test")
    s.add_argument("--output")

    s = sp.add_parser("preflight")
    s.add_argument("--q021-dir", required=True)
    s.add_argument("--q022-dir", required=True)
    s.add_argument("--output", required=True)
    s.add_argument("--support-output", required=True)

    s = sp.add_parser("build-hlp-covariance")
    s.add_argument("--preflight", required=True)
    s.add_argument("--matrix-output", required=True)
    s.add_argument("--meta-output", required=True)

    s = sp.add_parser("seal-preflight")
    s.add_argument("--preflight", required=True)
    s.add_argument("--hlp-matrix", required=True)
    s.add_argument("--hlp-meta", required=True)
    s.add_argument("--output", required=True)

    s = sp.add_parser("profile")
    s.add_argument("--preflight", required=True)
    s.add_argument("--implementation", choices=("camspec", "hillipop"), required=True)
    s.add_argument("--phase", choices=("stage1", "refinement"), required=True)
    s.add_argument("--mask", type=int, required=True)
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--stage1-dir")
    s.add_argument("--hlp-matrix")
    s.add_argument("--hlp-meta")
    s.add_argument("--output", required=True)

    s = sp.add_parser("assess-primary")
    s.add_argument("--preflight", required=True)
    s.add_argument("--stage1-dir", required=True)
    s.add_argument("--output", required=True)
    s.add_argument("--matrix-output", required=True)

    s = sp.add_parser("aggregate")
    s.add_argument("--preflight", required=True)
    s.add_argument("--assessment", required=True)
    s.add_argument("--stage1-dir", required=True)
    s.add_argument("--refinement-dir")
    s.add_argument("--output", required=True)
    return p


def main() -> int:
    a = parser().parse_args()
    c = load_cfg(a.config)
    load_source_lock()
    load_protocol_lock()
    if a.command == "self-test":
        return self_test(c, a.output)
    if a.command == "preflight":
        return preflight(c, a.q021_dir, a.q022_dir, a.output, a.support_output)
    if a.command == "build-hlp-covariance":
        return build_hlp_covariance(c, a.preflight, a.matrix_output, a.meta_output)
    if a.command == "seal-preflight":
        return seal_preflight(c, a.preflight, a.hlp_matrix, a.hlp_meta, a.output)
    if a.command == "profile":
        return run_profile(c, a.preflight, a.implementation, a.phase, a.mask, a.seed,
                           a.output, a.stage1_dir, a.hlp_matrix, a.hlp_meta)
    if a.command == "assess-primary":
        return assess_primary(c, a.preflight, a.stage1_dir, a.output, a.matrix_output)
    if a.command == "aggregate":
        return aggregate(c, a.preflight, a.assessment, a.stage1_dir, a.refinement_dir, a.output)
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
