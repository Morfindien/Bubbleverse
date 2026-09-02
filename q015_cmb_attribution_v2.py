#!/usr/bin/env python3
"""Bubbleverse Q015 V2 — CMB component / multipole / calibration attribution.

This program DOES NOT reopen Q014 and DOES NOT run a new global optimizer.
It reuses the frozen Q014 V12 best free-H0 and fixed-H0=71.5 profile endpoints.

Stage 0: exact post-processing of Q014's serialized component chi2 and
normalization-free Gaussian constraint-shape terms.

Endpoint attribution: rebuild the same n=3 common-backend chain at each frozen
Q014 endpoint and decompose only the relevant primary CMB likelihood quadratic
form using signed covariance allocations

    c_i = d_i (C^{-1} d)_i,

which sum to the full quadratic chi2 while retaining covariance coupling.
Groups are therefore additive allocations, NOT independent chi-square tests.

Local nuisance probes perturb chain-native calibration parameters while holding
all other endpoint physics fixed. These probes are directional diagnostics, not
causal or reprofiled attribution.

V2 technical repair
-------------------
V1 failed before Planck attribution because direct CamSpec helper calls received
only the serialized Q014 minimum values and therefore missed fixed likelihood
defaults such as use_fg_residual_model=0. V2 transports Cobaya's fully expanded
constant parameterization after model construction. No model, data, likelihood,
endpoint, covariance, constraint, or scientific gate is changed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q015_cmb_attribution_v2_config.yml"
CURRENT_Q = "Q015"
RUN_ID = "Q015-CMB-ATTRIBUTION-V2"
RESULT_ID = "R-Q015-EDE-CMB-ATTRIBUTION-002"


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"CONFIG_GATE=FAIL non-mapping config: {p}")
    return d


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8")
    tmp.replace(p)


def json_default(x: Any) -> Any:
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist()
    return str(x)


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def close(a: float, b: float, tol: float) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=float(tol))


def load_q014(path: str | Path, cfg: Mapping[str, Any]) -> dict[str, Any]:
    p = Path(path)
    d = json.loads(p.read_text(encoding="utf-8"))
    parent = cfg["parent"]["q014"]
    gates = {
        "q": d.get("q") == parent["q"],
        "run_id": d.get("run_id") == parent["run_id"],
        "result_id": d.get("result_id") == parent["result_id"],
        "validation_status": d.get("validation_status") == parent["validation_status"],
        "scientifically_usable_result": d.get("scientifically_usable_result") is True,
        "q011_status_preserved": d.get("q011_globality_status_preserved") == "BEST-OBSERVED MINIMUM ONLY",
        "no_cross_chain_sum": d.get("planck_spt_chi2_sum_performed") is False,
        "no_absolute_cross_package_comparison": d.get("absolute_chi2_cross_package_comparison_performed") is False,
    }
    tol = float(cfg["validation"]["parent_penalty_abs_tol"])
    for chain, expected in parent["expected_penalties"].items():
        got = d["chains"][chain]["penalties"]["fixed_h0_profile_delta_chi2"]
        gates[f"penalty_{chain}"] = close(got, expected, tol)
    if not all(gates.values()):
        raise RuntimeError(f"Q014_PARENT_GATE=FAIL {gates}")
    d["_q015_parent_path"] = str(p)
    d["_q015_parent_sha256"] = sha256_file(p)
    return d


def profile_best(parent: Mapping[str, Any], chain: str, mode: str) -> Mapping[str, Any]:
    p = parent["chains"][chain]["profiles"][mode]
    rec = p.get("best_record")
    if not isinstance(rec, Mapping) or rec.get("status") != "COMPLETE":
        raise RuntimeError(f"Q014_PROFILE_GATE=FAIL {chain}/{mode}")
    if not finite(rec.get("objective_chi2")):
        raise RuntimeError(f"Q014_PROFILE_GATE=FAIL nonfinite objective {chain}/{mode}")
    return rec


def primitive_component_deltas(parent: Mapping[str, Any], chain: str, cfg: Mapping[str, Any]) -> dict[str, float]:
    free = profile_best(parent, chain, "reference_free_h0")
    fixed = profile_best(parent, chain, "fixed_h0_71p5")
    exclusions = set(cfg.get("primitive_component_exclusions", []))
    a = free.get("chi2_components", {})
    b = fixed.get("chi2_components", {})
    keys = sorted((set(a) | set(b)) - exclusions)
    out: dict[str, float] = {}
    for k in keys:
        av = float(a.get(k, 0.0)); bv = float(b.get(k, 0.0))
        out[str(k)] = bv - av
    return out


def constraint_deltas(parent: Mapping[str, Any], chain: str) -> dict[str, float]:
    free = profile_best(parent, chain, "reference_free_h0").get("constraint_shape_penalties", {})
    fixed = profile_best(parent, chain, "fixed_h0_71p5").get("constraint_shape_penalties", {})
    keys = sorted(set(free) | set(fixed))
    return {str(k): float(fixed.get(k, 0.0)) - float(free.get(k, 0.0)) for k in keys}


def numeric_minimum(rec: Mapping[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    row = rec.get("minimum", {})
    for k, v in row.items():
        try:
            x = float(v)
        except Exception:
            continue
        if math.isfinite(x):
            out[str(k)] = x
    return out


def nuisance_movements(parent: Mapping[str, Any], chain: str, cfg: Mapping[str, Any]) -> dict[str, Any]:
    free = numeric_minimum(profile_best(parent, chain, "reference_free_h0"))
    fixed = numeric_minimum(profile_best(parent, chain, "fixed_h0_71p5"))
    specs = cfg.get("nuisance_probes", {}).get(chain, {})
    out: dict[str, Any] = {}
    for name, spec in specs.items():
        if name not in free or name not in fixed:
            continue
        delta = fixed[name] - free[name]
        scale = float(spec["step"])
        entry = {
            "free_value": free[name],
            "fixed_h0_71p5_value": fixed[name],
            "fixed_minus_free": delta,
            "step_or_reference_scale": scale,
            "movement_in_step_units": delta / scale if scale > 0 else None,
        }
        sig = spec.get("constraint_sigma")
        mu = spec.get("constraint_mean")
        if sig is not None and mu is not None:
            sig = float(sig); mu = float(mu)
            entry["free_offset_from_constraint_mean_sigma"] = (free[name] - mu) / sig
            entry["fixed_offset_from_constraint_mean_sigma"] = (fixed[name] - mu) / sig
        out[name] = entry
    return out


def stage0(q014_path: str | Path, output: str | Path, cfg: Mapping[str, Any]) -> dict[str, Any]:
    parent = load_q014(q014_path, cfg)
    chains: dict[str, Any] = {}
    all_pass = True
    tol = float(cfg["validation"]["component_reconstruction_abs_tol"])
    for chain in ("planck_npipe_k039_approx", "spt_d1_only", "spt_d1_plus_desi"):
        comp = primitive_component_deltas(parent, chain, cfg)
        cons = constraint_deltas(parent, chain)
        primitive_sum = float(sum(comp.values()))
        constraint_sum = float(sum(cons.values()))
        reconstructed = primitive_sum + constraint_sum
        target = float(parent["chains"][chain]["penalties"]["fixed_h0_profile_delta_chi2"])
        gate = close(reconstructed, target, tol)
        all_pass &= gate
        chains[chain] = {
            "role": parent["chains"][chain].get("role"),
            "label": parent["chains"][chain].get("label"),
            "paper_native_reproduction": parent["chains"][chain].get("paper_native_reproduction"),
            "fixed_h0_profile_delta_chi2": target,
            "primitive_likelihood_component_deltas": comp,
            "normalization_free_constraint_shape_deltas": cons,
            "primitive_likelihood_sum": primitive_sum,
            "constraint_shape_sum": constraint_sum,
            "reconstructed_profile_delta_chi2": reconstructed,
            "reconstruction_gate": gate,
            "nuisance_movements": nuisance_movements(parent, chain, cfg),
        }

    planck = chains["planck_npipe_k039_approx"]
    pc = planck["primitive_likelihood_component_deltas"]
    planck_cmb = sum(float(pc.get(k, 0.0)) for k in [
        "chi2__planck_2018_lowl.TT",
        "chi2__planck_2018_lowl.EE",
        "chi2__planck_NPIPE_highl_CamSpec.TTTEEE",
        "chi2__planck_2018_lensing.native",
    ])
    planck_lowz = sum(float(pc.get(k, 0.0)) for k in [
        "chi2__bao.sdss_dr12_consensus_final",
        "chi2__bao.sixdf_2011_bao",
        "chi2__bao.sdss_dr7_mgs",
        "chi2__sn.pantheonplus",
    ])
    spt = chains["spt_d1_only"]
    sc = spt["primitive_likelihood_component_deltas"]
    spt_cmb = sum(float(sc.get(k, 0.0)) for k in [
        "chi2__spt_d1_primary_lite",
        "chi2__muse3glike.cobaya.spt3g_2yr_delensed_ee_optimal_pp_muse",
    ])

    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "STAGE0_PARENT_COMPONENT_ATTRIBUTION",
        "status": "PASS" if all_pass else "FAIL",
        "execution_kind": "DETERMINISTIC_POSTPROCESSING_OF_FROZEN_Q014_V12_RESULT",
        "actual_computed_result": True,
        "q014_parent": {
            "q": parent["q"],
            "run_id": parent["run_id"],
            "result_id": parent["result_id"],
            "path": parent["_q015_parent_path"],
            "sha256": parent["_q015_parent_sha256"],
        },
        "cross_chain_absolute_chi2_comparison_performed": False,
        "planck_spt_chi2_sum_performed": False,
        "chains": chains,
        "stage0_interpretive_partition": {
            "planck_cmb_within_chain_delta": planck_cmb,
            "planck_low_z_within_chain_delta": planck_lowz,
            "planck_constraint_shape_delta": planck["constraint_shape_sum"],
            "spt_primary_plus_lensing_within_chain_delta": spt_cmb,
            "spt_tau_information_delta": float(sc.get("chi2__q014_tau_information", 0.0)),
            "spt_constraint_shape_delta": spt["constraint_shape_sum"],
            "warning": "These are within-chain partitions. Do not subtract/sum them as a cross-chain chi-square statistic."
        },
        "next_required_action": "Run covariance-aware endpoint attribution for Planck high-l TTTEEE and SPT D1 primary TT/TE/EE, then aggregate.",
    }
    dump_json(output, result)
    return result


def import_q014():
    import q014_external_viability_v12 as q014
    return q014


def load_q011_vector(q011_path: str | Path, q014_cfg: Mapping[str, Any]) -> dict[str, float]:
    q014 = import_q014()
    return q014.impl.q011_exact_shared_vector(q014_cfg, q011_path)


def collect_fixed_values(info: Mapping[str, Any], row: Mapping[str, float]) -> dict[str, float]:
    vals: dict[str, float] = {}
    for name, spec in info.get("params", {}).items():
        if isinstance(spec, (int, float)) and finite(spec):
            vals[str(name)] = float(spec)
        elif isinstance(spec, Mapping):
            v = spec.get("value")
            if isinstance(v, (int, float)) and finite(v):
                vals[str(name)] = float(v)
    vals.update({str(k): float(v) for k, v in row.items() if finite(v)})
    return vals


def freeze_sampled_to_endpoint(info: dict[str, Any], row: Mapping[str, float], mode: str,
                               cfg: Mapping[str, Any]) -> dict[str, float]:
    params = info.get("params")
    if not isinstance(params, dict):
        raise RuntimeError("MODEL_PARAMETER_GATE=FAIL")
    used: dict[str, float] = {}
    target = float(cfg["scientific_surface"]["target_h0"])
    for name, spec in list(params.items()):
        if not isinstance(spec, Mapping) or "prior" not in spec:
            continue
        if name in row and finite(row[name]):
            x = float(row[name])
        elif name == "H0" and mode == "fixed_h0_71p5":
            x = target
        else:
            raise RuntimeError(f"ENDPOINT_SERIALIZATION_GATE=FAIL sampled parameter missing from Q014 minimum: {name}")
        params[name] = x
        used[name] = x
    info.pop("sampler", None)
    info.pop("output", None)
    info.pop("force", None)
    return used


def build_endpoint_model(chain: str, mode: str, parent: Mapping[str, Any], q011_path: str | Path,
                         cfg: Mapping[str, Any], workdir: str | Path):
    q014 = import_q014()
    q014_cfg = q014.load_cfg("q014_external_viability_v12_config.yml")
    qvec = load_q011_vector(q011_path, q014_cfg)
    rec = profile_best(parent, chain, mode)
    row = numeric_minimum(rec)
    # Legacy q011 start family is only a harmless initializer here; all sampled
    # parameters are immediately frozen to the authoritative Q014 endpoint.
    info, _ = q014.impl.build_info(
        chain, mode, "q011", 0, q014_cfg, qvec,
        Path(workdir) / f"q015_{chain}_{mode}_no_optimizer", max_evals=4
    )
    info = copy.deepcopy(info)
    frozen = freeze_sampled_to_endpoint(info, row, mode, cfg)
    # Q015 needs only the primary high-l likelihood at a frozen endpoint.
    # Restrict model initialisation to that component; this changes no endpoint
    # physics and avoids evaluating unrelated low-l/lensing/low-z likelihoods.
    target_like = (cfg["likelihood_names"]["planck_highl"] if chain == "planck_npipe_k039_approx"
                   else cfg["likelihood_names"]["spt_primary"])
    likes = info.get("likelihood", {})
    if target_like not in likes:
        raise RuntimeError(f"PRIMARY_LIKELIHOOD_GATE=FAIL missing {target_like}")
    info["likelihood"] = {target_like: copy.deepcopy(likes[target_like])}
    # All sampled parameters are frozen; external prior blocks are not needed to
    # generate theory/primary-likelihood residuals. Constraint shapes are added
    # explicitly in the Q015 diagnostic probe from the frozen Q014 source lock.
    info.pop("prior", None)
    from cobaya.model import get_model
    model = get_model(info)
    post = model.logposterior({})
    logpost = float(getattr(post, "logpost", post))
    if not math.isfinite(logpost):
        raise RuntimeError(f"FINITE_ENDPOINT_GATE=FAIL {chain}/{mode}")

    # V2 REPAIR: Q015 directly calls the primary likelihood's internal residual
    # helpers (e.g. CamSpec get_foregrounds/get_cals). Q014 minimum rows contain
    # the optimized sampled parameters, but they intentionally do not serialize
    # every fixed likelihood default loaded by Cobaya from component YAML files.
    # In V1 this caused Planck to fail on the first missing fixed default,
    # use_fg_residual_model. After get_model(), Cobaya's Parameterization is the
    # authoritative expanded parameter transport and includes both the frozen
    # endpoint and likelihood-fixed constants (use_fg_residual_model, cal0,
    # cal2, amp_100, n_100, etc.). Use it instead of reconstructing defaults.
    values: dict[str, float] = {}
    for name, value in model.parameterization.constant_params().items():
        if finite(value):
            values[str(name)] = float(value)
    # Preserve the authoritative serialized endpoint values and explicit freezes
    # as the final override. This does not change the likelihood or endpoint.
    values.update({str(k): float(v) for k, v in row.items() if finite(v)})
    values.update(frozen)

    if chain == "planck_npipe_k039_approx":
        required = {
            "use_fg_residual_model", "cal0", "cal2", "amp_100", "n_100",
            "A_planck", "calTE", "calEE", "amp_143", "amp_217",
            "amp_143x217", "n_143", "n_217", "n_143x217",
        }
    else:
        required = {"Tcal", "Ecal"}
    missing = sorted(required.difference(values))
    if missing:
        raise RuntimeError(
            f"EXPANDED_LIKELIHOOD_PARAMETER_TRANSPORT_GATE=FAIL {chain}/{mode} missing={missing}"
        )

    return model, values, row, rec, info


def ell_band(ell: float, cfg: Mapping[str, Any]) -> str:
    x = float(ell)
    for band in cfg["ell_bands"]:
        if float(band["min"]) <= x <= float(band["max"]):
            return str(band["name"])
    return "unassigned"


def accumulate(labels: list[dict[str, Any]], contrib: np.ndarray, cfg: Mapping[str, Any]) -> dict[str, Any]:
    by_type: dict[str, float] = {}
    by_spectrum: dict[str, float] = {}
    by_band: dict[str, float] = {}
    by_type_band: dict[str, float] = {}
    for meta, c in zip(labels, np.asarray(contrib, dtype=float)):
        typ = str(meta["type"])
        spec = str(meta["spectrum"])
        band = ell_band(float(meta["ell"]), cfg)
        by_type[typ] = by_type.get(typ, 0.0) + float(c)
        by_spectrum[spec] = by_spectrum.get(spec, 0.0) + float(c)
        by_band[band] = by_band.get(band, 0.0) + float(c)
        k = f"{typ}|{band}"
        by_type_band[k] = by_type_band.get(k, 0.0) + float(c)
    return {
        "by_observable": dict(sorted(by_type.items())),
        "by_spectrum": dict(sorted(by_spectrum.items())),
        "by_ell_band": dict(sorted(by_band.items())),
        "by_observable_and_ell_band": dict(sorted(by_type_band.items())),
    }


def diff_groups(fixed: Mapping[str, Any], free: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for group_key in ["by_observable", "by_spectrum", "by_ell_band", "by_observable_and_ell_band"]:
        a = free.get(group_key, {}); b = fixed.get(group_key, {})
        keys = sorted(set(a) | set(b))
        out[group_key] = {k: float(b.get(k, 0.0)) - float(a.get(k, 0.0)) for k in keys}
    return out


def planck_highl_state(model, values: Mapping[str, float], cfg: Mapping[str, Any]) -> dict[str, Any]:
    lname = cfg["likelihood_names"]["planck_highl"]
    like = model.likelihood[lname]
    cls = like.provider.get_Cl(ell_factor=True)
    CT = np.asarray(cls["tt"], dtype=float)
    CTE = np.asarray(cls["te"], dtype=float)
    CEE = np.asarray(cls["ee"], dtype=float)
    pars = dict(values)
    cals = np.asarray(like.get_cals(pars), dtype=float)
    foregrounds = like.get_foregrounds(pars) if np.any(like.cl_used[:4]) else None
    delta = np.asarray(like.data_vector, dtype=float).copy()
    labels: list[dict[str, Any]] = []
    ix = 0
    for i, (cal, n) in enumerate(zip(cals, like.used_sizes)):
        n = int(n)
        if n <= 0:
            continue
        ells = np.asarray(list(like.ell_ranges[i]), dtype=int)
        if len(ells) != n:
            ells = ells[:n]
        if i <= 3:
            model_vec = (CT[ells] + np.asarray(foregrounds[i], dtype=float)[ells]) / float(cal)
            typ = "TT"
        elif i == 4:
            model_vec = CTE[ells] / float(cal)
            typ = "TE"
        elif i == 5:
            model_vec = CEE[ells] / float(cal)
            typ = "EE"
        else:
            raise RuntimeError("PLANCK_SPECTRUM_LAYOUT_GATE=FAIL")
        delta[ix:ix+n] -= model_vec
        spec = str(like.cl_names[i])
        labels.extend({"type":typ, "spectrum":spec, "ell":int(L)} for L in ells)
        ix += n
    if ix != len(delta) or len(labels) != len(delta):
        raise RuntimeError("PLANCK_VECTOR_LENGTH_GATE=FAIL")
    z = np.asarray(like.covinv, dtype=float).dot(delta)
    contrib = delta * z
    chi2 = float(np.dot(delta, z))
    groups = accumulate(labels, contrib, cfg)
    return {
        "chi2": chi2,
        "n_data": len(delta),
        "signed_contribution_sum": float(np.sum(contrib)),
        "groups": groups,
        "_like": like,
        "_cls": {"tt":CT, "te":CTE, "ee":CEE},
        "_values": pars,
    }


def candl_theory_dict(wrapper) -> dict[str, Any]:
    Dls = wrapper.provider.get_Cl(ell_factor=True, units="muK2")
    Dls = {str(k): np.asarray(v).copy() for k, v in Dls.items()}
    if "ell" not in Dls:
        non_ell = next(v for k, v in Dls.items() if k != "ell")
        Dls["ell"] = np.arange(len(non_ell), dtype=int)
    if "pp" in Dls:
        Dls["kk"] = Dls["pp"] * np.pi / 2.0
    clike = wrapper.candl_like
    start_ix = np.argwhere(Dls["ell"] == clike.ell_min)[0][0]
    stop_ix = np.argwhere(Dls["ell"] == clike.ell_max)[0][0] + 1
    for ky in list(Dls.keys()):
        if ky == "ell":
            continue
        if ky in ["pp", "kk"]:
            Dls[ky] = Dls[ky][start_ix:stop_ix]
        else:
            Dls[ky.upper()] = Dls[ky][start_ix:stop_ix]
            if ky.lower() == ky:
                del Dls[ky]
    Dls["ell"] = Dls["ell"][start_ix:stop_ix]
    return Dls


def spt_primary_state(model, values: Mapping[str, float], cfg: Mapping[str, Any]) -> dict[str, Any]:
    lname = cfg["likelihood_names"]["spt_primary"]
    wrapper = model.likelihood[lname]
    clike = wrapper.candl_like
    Dls = candl_theory_dict(wrapper)
    pars = dict(values)
    pars["Dl"] = Dls
    modified = clike.get_model_specs(pars)
    binned = np.asarray(clike.bin_model_specs(modified), dtype=float)
    data = np.asarray(clike._data_bandpowers, dtype=float)
    delta = data - binned
    L = np.asarray(clike.covariance_chol_dec, dtype=float)
    y = np.linalg.solve(L, delta)
    z = np.linalg.solve(L.T, y)
    contrib = delta * z
    chi2 = float(np.dot(delta, z))
    labels: list[dict[str, Any]] = []
    effective = np.asarray(clike.effective_ells, dtype=float)
    for i, spec in enumerate(clike.spec_order):
        a = int(clike.bins_start_ix[i]); b = int(clike.bins_stop_ix[i])
        typ = str(clike.spec_types[i]).upper()
        labels.extend({"type":typ, "spectrum":str(spec), "ell":float(Lell)} for Lell in effective[a:b])
    if len(labels) != len(delta):
        raise RuntimeError("SPT_VECTOR_LENGTH_GATE=FAIL")
    groups = accumulate(labels, contrib, cfg)
    return {
        "chi2": chi2,
        "n_data": len(delta),
        "signed_contribution_sum": float(np.sum(contrib)),
        "groups": groups,
        "_wrapper": wrapper,
        "_Dls": Dls,
        "_values": dict(values),
    }


def gaussian_shape(x: float, mean: float | None, sigma: float | None) -> float:
    if mean is None or sigma is None:
        return 0.0
    return ((float(x) - float(mean)) / float(sigma)) ** 2


def planck_probe_objective(state: Mapping[str, Any], values: Mapping[str, float], cfg: Mapping[str, Any]) -> float:
    like = state["_like"]
    cls = state["_cls"]
    pars = dict(values)
    raw = float(like.chi_squared(cls["tt"], cls["te"], cls["ee"], pars))
    shape = 0.0
    for name, spec in cfg["nuisance_probes"]["planck_npipe_k039_approx"].items():
        shape += gaussian_shape(pars[name], spec.get("constraint_mean"), spec.get("constraint_sigma"))
    return raw + shape


def spt_probe_objective(state: Mapping[str, Any], values: Mapping[str, float], cfg: Mapping[str, Any]) -> float:
    wrapper = state["_wrapper"]
    clike = wrapper.candl_like
    pars = dict(values)
    pars["Dl"] = state["_Dls"]
    modified = clike.get_model_specs(pars)
    binned = np.asarray(clike.bin_model_specs(modified), dtype=float)
    data = np.asarray(clike._data_bandpowers, dtype=float)
    delta = data - binned
    L = np.asarray(clike.covariance_chol_dec, dtype=float)
    y = np.linalg.solve(L, delta)
    raw = float(np.dot(y, y))
    spec = cfg["nuisance_probes"]["spt_d1_only"]["Tcal"]
    shape = gaussian_shape(pars["Tcal"], spec.get("constraint_mean"), spec.get("constraint_sigma"))
    return raw + shape


def nuisance_probe(chain: str, state: Mapping[str, Any], values: Mapping[str, float], cfg: Mapping[str, Any]) -> dict[str, Any]:
    specs = cfg["nuisance_probes"][chain]
    offsets = [float(x) for x in cfg["nuisance_probes"]["offsets"]]
    out: dict[str, Any] = {}
    objective = planck_probe_objective if chain == "planck_npipe_k039_approx" else spt_probe_objective
    for name, spec in specs.items():
        center = float(values[name])
        step = float(spec["step"])
        vals = []
        for off in offsets:
            p = dict(values); p[name] = center + off * step
            f = float(objective(state, p, cfg))
            vals.append({"offset_steps":off, "value":p[name], "conditional_primary_plus_shape_chi2":f})
        f0 = next(x["conditional_primary_plus_shape_chi2"] for x in vals if x["offset_steps"] == 0.0)
        for x in vals:
            x["delta_from_center"] = x["conditional_primary_plus_shape_chi2"] - f0
        minus = min(vals, key=lambda x: abs(x["offset_steps"] + 1.0))
        plus = min(vals, key=lambda x: abs(x["offset_steps"] - 1.0))
        out[name] = {
            "center": center,
            "step": step,
            "points": vals,
            "symmetric_first_derivative_estimate": (plus["conditional_primary_plus_shape_chi2"] - minus["conditional_primary_plus_shape_chi2"]) / (2.0 * step),
            "diagnostic_only": True,
            "causal_attribution": False,
        }
    return out


def strip_private(state: Mapping[str, Any]) -> dict[str, Any]:
    return {k:v for k,v in state.items() if not str(k).startswith("_")}


def endpoint_attribution(chain: str, q014_path: str | Path, q011_path: str | Path,
                         output: str | Path, cfg: Mapping[str, Any]) -> dict[str, Any]:
    if chain not in cfg["scientific_surface"]["primary_chains"]:
        raise RuntimeError("CHAIN_GATE=FAIL Q015 V2 primary endpoint attribution is Planck and SPT-only only")
    parent = load_q014(q014_path, cfg)
    workdir = Path(output).parent / f"work_{chain}"
    modes = ["reference_free_h0", "fixed_h0_71p5"]
    states: dict[str, Any] = {}
    public: dict[str, Any] = {}
    closure_tol = float(cfg["validation"]["covariance_closure_abs_tol"])

    for mode in modes:
        model, values, row, rec, _ = build_endpoint_model(chain, mode, parent, q011_path, cfg, workdir)
        try:
            state = planck_highl_state(model, values, cfg) if chain == "planck_npipe_k039_approx" else spt_primary_state(model, values, cfg)
            parent_key = "chi2__planck_NPIPE_highl_CamSpec.TTTEEE" if chain == "planck_npipe_k039_approx" else "chi2__spt_d1_primary_lite"
            parent_component = float(rec["chi2_components"][parent_key])
            closure = close(state["chi2"], parent_component, closure_tol) and close(state["chi2"], state["signed_contribution_sum"], closure_tol)
            probe = nuisance_probe(chain, state, values, cfg)
            public[mode] = {
                **strip_private(state),
                "parent_serialized_component_chi2": parent_component,
                "parent_component_closure_gate": closure,
                "endpoint_parameters": {k:values[k] for k in cfg["nuisance_probes"][chain] if k in values},
                "nuisance_directional_probe": probe,
            }
            states[mode] = state
        finally:
            try:
                model.close()
            except Exception:
                pass

    delta_groups = diff_groups(public["fixed_h0_71p5"]["groups"], public["reference_free_h0"]["groups"])
    delta_chi2 = public["fixed_h0_71p5"]["chi2"] - public["reference_free_h0"]["chi2"]
    parent_comp = primitive_component_deltas(parent, chain, cfg)
    parent_key = "chi2__planck_NPIPE_highl_CamSpec.TTTEEE" if chain == "planck_npipe_k039_approx" else "chi2__spt_d1_primary_lite"
    expected_delta = float(parent_comp[parent_key])
    delta_gate = close(delta_chi2, expected_delta, float(cfg["validation"]["parent_primary_component_delta_abs_tol"]))
    closures = all(public[m]["parent_component_closure_gate"] for m in modes)

    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "ENDPOINT_COVARIANCE_ATTRIBUTION",
        "chain": chain,
        "status": "PASS" if closures and delta_gate else "FAIL",
        "execution_kind": "FROZEN_Q014_ENDPOINT_REEVALUATION_NO_OPTIMIZER",
        "paper_native_reproduction": False,
        "q011_globality_status_preserved": "BEST-OBSERVED MINIMUM ONLY",
        "exact_q011_vector_used_as_profile_endpoint": False,
        "cross_chain_absolute_chi2_comparison_performed": False,
        "planck_spt_chi2_sum_performed": False,
        "attribution_definition": "signed full-covariance allocation c_i=d_i(C^-1 d)_i; groups are covariance-coupled, not independent chi2 tests",
        "endpoints": public,
        "fixed_minus_free_primary_component_delta_chi2": delta_chi2,
        "parent_q014_primary_component_delta_chi2": expected_delta,
        "parent_primary_component_delta_gate": delta_gate,
        "fixed_minus_free_signed_group_deltas": delta_groups,
        "nuisance_movement_from_q014_parent": nuisance_movements(parent, chain, cfg),
    }
    dump_json(output, result)
    return result


def sorted_drivers(group: Mapping[str, float], n: int = 12) -> list[dict[str, Any]]:
    items = sorted(((str(k), float(v)) for k,v in group.items()), key=lambda kv: abs(kv[1]), reverse=True)
    return [{"group":k, "delta_chi2_allocation":v} for k,v in items[:n]]


def aggregate(stage0_path: str | Path, planck_path: str | Path, spt_path: str | Path,
              output: str | Path, cfg: Mapping[str, Any]) -> dict[str, Any]:
    s0 = json.loads(Path(stage0_path).read_text())
    p = json.loads(Path(planck_path).read_text())
    s = json.loads(Path(spt_path).read_text())
    gates = {
        "stage0": s0.get("q") == CURRENT_Q and s0.get("status") == "PASS",
        "planck": p.get("q") == CURRENT_Q and p.get("chain") == "planck_npipe_k039_approx" and p.get("status") == "PASS",
        "spt": s.get("q") == CURRENT_Q and s.get("chain") == "spt_d1_only" and s.get("status") == "PASS",
        "no_cross_chain_sum_stage0": s0.get("planck_spt_chi2_sum_performed") is False,
        "no_cross_chain_sum_planck": p.get("planck_spt_chi2_sum_performed") is False,
        "no_cross_chain_sum_spt": s.get("planck_spt_chi2_sum_performed") is False,
    }
    pg = p["fixed_minus_free_signed_group_deltas"]
    sg = s["fixed_minus_free_signed_group_deltas"]
    # No cross-chain chi2 statistic is formed. We only present each chain's own
    # internally additive driver ranking side by side.
    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "FINAL",
        "execution_status": "COMPLETE" if all(gates.values()) else "FAILED_VALIDATION",
        "tests_status": "COMPLETE",
        "final_result_gate": "PASS" if all(gates.values()) else "FAIL",
        "scientifically_usable_result": bool(all(gates.values())),
        "gates": gates,
        "q014_penalties_preserved": {
            "planck_npipe_k039_approx": s0["chains"]["planck_npipe_k039_approx"]["fixed_h0_profile_delta_chi2"],
            "spt_d1_only": s0["chains"]["spt_d1_only"]["fixed_h0_profile_delta_chi2"],
            "spt_d1_plus_desi_secondary": s0["chains"]["spt_d1_plus_desi"]["fixed_h0_profile_delta_chi2"],
        },
        "stage0_partition": s0["stage0_interpretive_partition"],
        "planck": {
            "primary_highl_delta_chi2": p["fixed_minus_free_primary_component_delta_chi2"],
            "observable_deltas": pg["by_observable"],
            "ell_band_deltas": pg["by_ell_band"],
            "observable_ell_deltas": pg["by_observable_and_ell_band"],
            "dominant_signed_allocations": sorted_drivers(pg["by_observable_and_ell_band"]),
            "nuisance_movement": p["nuisance_movement_from_q014_parent"],
            "local_nuisance_probes": p["endpoints"]["fixed_h0_71p5"]["nuisance_directional_probe"],
        },
        "spt": {
            "primary_d1_delta_chi2": s["fixed_minus_free_primary_component_delta_chi2"],
            "observable_deltas": sg["by_observable"],
            "ell_band_deltas": sg["by_ell_band"],
            "observable_ell_deltas": sg["by_observable_and_ell_band"],
            "dominant_signed_allocations": sorted_drivers(sg["by_observable_and_ell_band"]),
            "nuisance_movement": s["nuisance_movement_from_q014_parent"],
            "local_nuisance_probes": s["endpoints"]["fixed_h0_71p5"]["nuisance_directional_probe"],
        },
        "cross_chain_absolute_chi2_comparison_performed": False,
        "planck_spt_chi2_sum_performed": False,
        "interpretation_boundary": [
            "Planck and SPT group allocations are reported within each chain only.",
            "Signed allocations can be negative because covariance couples bins/spectra.",
            "Local nuisance probes are conditional diagnostics and are not causal reprofiled decompositions.",
            "Planck remains a public-NPIPE common-backend approximation to K-039.",
            "SPT remains official D1 likelihood products with the common Bubbleverse backend, not exact K-040/AxiCLASS reproduction.",
            "Q011 remains BEST-OBSERVED MINIMUM ONLY."
        ],
        "journal_effect": "UPDATE C-EDE-002 with the component/observable/ell/calibration localization if FINAL_RESULT_GATE passes; preserve Q014 penalties unchanged.",
        "next_required_action": "RESULT INGESTION & ROUTING ENGINE",
    }
    dump_json(output, result)
    return result


def self_test(path: str | Path, output: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text())
    mandatory = {
        "q_identity": d.get("q") == CURRENT_Q,
        "run_identity": d.get("run_id") == RUN_ID,
        "final_stage": d.get("stage") == "FINAL",
        "final_result_gate": d.get("final_result_gate") == "PASS",
        "scientifically_usable": d.get("scientifically_usable_result") is True,
        "no_cross_chain_sum": d.get("planck_spt_chi2_sum_performed") is False,
        "no_absolute_cross_chain_comparison": d.get("cross_chain_absolute_chi2_comparison_performed") is False,
        "planck_present": isinstance(d.get("planck"), Mapping),
        "spt_present": isinstance(d.get("spt"), Mapping),
    }
    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "test_id": "Q015-V2-MANDATORY-RESULT-TESTS",
        "tests": mandatory,
        "status": "PASS" if all(mandatory.values()) else "FAIL",
    }
    dump_json(output, result)
    if result["status"] != "PASS":
        raise RuntimeError(f"FINAL_RESULT_TEST_GATE=FAIL {mandatory}")
    return result


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stage0")
    p.add_argument("--q014", required=True)
    p.add_argument("--output", required=True)
    p = sub.add_parser("endpoint-attribution")
    p.add_argument("--chain", required=True, choices=["planck_npipe_k039_approx", "spt_d1_only"])
    p.add_argument("--q014", required=True)
    p.add_argument("--q011", required=True)
    p.add_argument("--output", required=True)
    p = sub.add_parser("aggregate")
    p.add_argument("--stage0", required=True)
    p.add_argument("--planck", required=True)
    p.add_argument("--spt", required=True)
    p.add_argument("--output", required=True)
    p = sub.add_parser("test")
    p.add_argument("--result", required=True)
    p.add_argument("--output", required=True)
    return ap.parse_args()


def main() -> int:
    a = parse_args()
    cfg = load_yaml(a.config)
    if cfg["project"]["q"] != CURRENT_Q or cfg["project"]["run_id"] != RUN_ID:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL config")
    if a.cmd == "stage0":
        r = stage0(a.q014, a.output, cfg)
    elif a.cmd == "endpoint-attribution":
        r = endpoint_attribution(a.chain, a.q014, a.q011, a.output, cfg)
    elif a.cmd == "aggregate":
        r = aggregate(a.stage0, a.planck, a.spt, a.output, cfg)
    elif a.cmd == "test":
        r = self_test(a.result, a.output)
    else:
        raise AssertionError(a.cmd)
    print(json.dumps({"q":CURRENT_Q,"run_id":RUN_ID,"command":a.cmd,"status":r.get("status",r.get("final_result_gate"))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
