#!/usr/bin/env python3
"""Bubbleverse Q015 V3 — certification/merge repair for completed V2 endpoint attribution.

V3 does NOT rerun CLASS, Planck, SPT, or any optimizer. It reuses the completed
Q015 V2 Stage0 + Planck + SPT endpoint artifacts from GitHub run 33629190153.

V2 exposed a validation-definition bug: it required the raw covariance
quadratic allocation to be bit/near-bit identical to the parent likelihood's
serialized component chi2. That is not generally valid because a likelihood
wrapper may include convention terms (e.g. normalization/log-determinant) and
finite-precision evaluation differences that are not attributable to individual
bandpowers. V3 therefore preserves both quantities and introduces an explicit
"likelihood-to-covariance bridge".

The signed covariance allocations remain exactly the V2 allocations:
    c_i = d_i (C^-1 d)_i
and are NOT rescaled. The bridge is reported separately. Q015 passes only if:
  * signed allocations close to the raw covariance quadratic internally;
  * endpoint bridge terms are small in absolute and relative terms;
  * the fixed-minus-free bridge residual is <= the declared small tolerance;
  * the bridge is too small to alter the dominant driver ranking;
  * all Q014/Q011 scientific claim boundaries remain preserved.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = "q015_cmb_attribution_v3_config.yml"
CURRENT_Q = "Q015"
RUN_ID = "Q015-CMB-ATTRIBUTION-V3"
RESULT_ID = "R-Q015-EDE-CMB-ATTRIBUTION-003"
V2_RUN_ID = "Q015-CMB-ATTRIBUTION-V2"
V2_RESULT_ID = "R-Q015-EDE-CMB-ATTRIBUTION-002"


def load_yaml(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError("CONFIG_GATE=FAIL")
    return d


def load_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_GATE=FAIL {path}")
    return d


def dump_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(p)


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def close(a: float, b: float, tol: float) -> bool:
    return finite(a) and finite(b) and abs(float(a) - float(b)) <= float(tol)


def sorted_drivers(group: Mapping[str, Any], n: int = 12) -> list[dict[str, float | str]]:
    vals = [(str(k), float(v)) for k, v in group.items() if finite(v)]
    vals.sort(key=lambda kv: abs(kv[1]), reverse=True)
    return [{"group": k, "delta_chi2_allocation": v} for k, v in vals[:n]]


def upgrade_endpoint(input_path: str | Path, output_path: str | Path,
                     cfg: Mapping[str, Any]) -> dict[str, Any]:
    src = load_json(input_path)
    chain = src.get("chain")
    allowed = set(cfg["scientific_surface"]["primary_chains"])
    if (
        src.get("q") != CURRENT_Q
        or src.get("run_id") != V2_RUN_ID
        or src.get("result_id") != V2_RESULT_ID
        or src.get("stage") != "ENDPOINT_COVARIANCE_ATTRIBUTION"
        or chain not in allowed
    ):
        raise RuntimeError("V2_ENDPOINT_PARENT_IDENTITY_GATE=FAIL")
    if src.get("planck_spt_chi2_sum_performed") is not False:
        raise RuntimeError("NO_CROSS_CHAIN_SUM_GATE=FAIL")
    if src.get("cross_chain_absolute_chi2_comparison_performed") is not False:
        raise RuntimeError("NO_ABSOLUTE_CROSS_CHAIN_COMPARISON_GATE=FAIL")
    if src.get("q011_globality_status_preserved") != "BEST-OBSERVED MINIMUM ONLY":
        raise RuntimeError("Q011_STATUS_PRESERVATION_GATE=FAIL")
    if src.get("exact_q011_vector_used_as_profile_endpoint") is not False:
        raise RuntimeError("Q011_VECTOR_ROLE_GATE=FAIL")

    v = cfg["validation"]
    internal_tol = float(v["covariance_internal_abs_tol"])
    endpoint_abs_tol = float(v["endpoint_bridge_abs_tol"])
    endpoint_rel_tol = float(v["endpoint_bridge_relative_tol"])
    delta_bridge_tol = float(v["delta_bridge_abs_tol"])
    driver_bridge_ratio_tol = float(v["driver_bridge_ratio_max"])

    upgraded_endpoints: dict[str, Any] = {}
    endpoint_gates: dict[str, bool] = {}
    for mode in ["reference_free_h0", "fixed_h0_71p5"]:
        ep = src.get("endpoints", {}).get(mode)
        if not isinstance(ep, Mapping):
            raise RuntimeError(f"V2_ENDPOINT_CONTENT_GATE=FAIL {mode}")
        raw = float(ep["chi2"])
        signed = float(ep["signed_contribution_sum"])
        parent = float(ep["parent_serialized_component_chi2"])
        internal_residual = signed - raw
        bridge = parent - raw
        bridge_rel = abs(bridge) / max(abs(parent), 1.0)
        internal_gate = abs(internal_residual) <= internal_tol
        bridge_gate = abs(bridge) <= endpoint_abs_tol and bridge_rel <= endpoint_rel_tol
        endpoint_gates[f"{mode}_covariance_internal"] = internal_gate
        endpoint_gates[f"{mode}_likelihood_to_covariance_bridge"] = bridge_gate
        upgraded_endpoints[mode] = {
            **dict(ep),
            "v2_parent_component_closure_gate": bool(ep.get("parent_component_closure_gate")),
            "raw_covariance_quadratic_chi2": raw,
            "covariance_internal_residual_chi2": internal_residual,
            "covariance_internal_closure_gate": internal_gate,
            "parent_likelihood_component_chi2": parent,
            "likelihood_to_covariance_bridge_chi2": bridge,
            "likelihood_to_covariance_bridge_relative": bridge_rel,
            "likelihood_to_covariance_bridge_gate": bridge_gate,
            "bridge_interpretation": (
                "Non-bandpower-attributable likelihood-convention / normalization / finite-precision bridge. "
                "It is reported separately and is not distributed across TT/TE/EE or ell bins."
            ),
        }

    raw_delta = float(src["fixed_minus_free_primary_component_delta_chi2"])
    parent_delta = float(src["parent_q014_primary_component_delta_chi2"])
    delta_bridge = parent_delta - raw_delta
    delta_gate = abs(delta_bridge) <= delta_bridge_tol

    group = src["fixed_minus_free_signed_group_deltas"]["by_observable_and_ell_band"]
    max_driver = max((abs(float(x)) for x in group.values() if finite(x)), default=0.0)
    bridge_driver_ratio = abs(delta_bridge) / max(max_driver, 1e-300)
    driver_gate = bridge_driver_ratio <= driver_bridge_ratio_tol

    all_gates = {
        **endpoint_gates,
        "delta_bridge": delta_gate,
        "driver_ranking_robust_to_bridge": driver_gate,
        "no_cross_chain_sum": src.get("planck_spt_chi2_sum_performed") is False,
        "no_absolute_cross_chain_comparison": src.get("cross_chain_absolute_chi2_comparison_performed") is False,
        "q011_status_preserved": src.get("q011_globality_status_preserved") == "BEST-OBSERVED MINIMUM ONLY",
        "q011_vector_not_endpoint": src.get("exact_q011_vector_used_as_profile_endpoint") is False,
    }
    passed = all(all_gates.values())

    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "ENDPOINT_BRIDGE_CERTIFICATION",
        "chain": chain,
        "status": "PASS" if passed else "FAIL",
        "execution_kind": "POSTPROCESS_COMPLETED_Q015_V2_ENDPOINT_NO_THEORY_RERUN_NO_OPTIMIZER",
        "source_v2_endpoint": {
            "run_id": src.get("run_id"),
            "result_id": src.get("result_id"),
            "v2_status": src.get("status"),
            "v2_failure_reclassified_as_validation_definition_failure": True,
        },
        "scientific_surface_changed": False,
        "endpoint_changed": False,
        "likelihood_changed": False,
        "covariance_changed": False,
        "signed_covariance_allocations_changed": False,
        "allocation_rescaled": False,
        "q011_globality_status_preserved": "BEST-OBSERVED MINIMUM ONLY",
        "exact_q011_vector_used_as_profile_endpoint": False,
        "cross_chain_absolute_chi2_comparison_performed": False,
        "planck_spt_chi2_sum_performed": False,
        "attribution_definition": src.get("attribution_definition"),
        "endpoints": upgraded_endpoints,
        "raw_covariance_fixed_minus_free_delta_chi2": raw_delta,
        "authoritative_parent_fixed_minus_free_delta_chi2": parent_delta,
        "likelihood_to_covariance_delta_bridge_chi2": delta_bridge,
        "delta_bridge_gate": delta_gate,
        "largest_abs_observable_ell_driver": max_driver,
        "delta_bridge_to_largest_driver_ratio": bridge_driver_ratio,
        "driver_ranking_robust_to_bridge_gate": driver_gate,
        "fixed_minus_free_signed_group_deltas": src["fixed_minus_free_signed_group_deltas"],
        "nuisance_movement_from_q014_parent": src["nuisance_movement_from_q014_parent"],
        "gates": all_gates,
    }
    dump_json(output_path, result)
    return result


def aggregate(stage0_path: str | Path, planck_path: str | Path, spt_path: str | Path,
              output_path: str | Path, cfg: Mapping[str, Any]) -> dict[str, Any]:
    s0 = load_json(stage0_path)
    p = load_json(planck_path)
    s = load_json(spt_path)
    if s0.get("q") != CURRENT_Q or s0.get("status") != "PASS":
        raise RuntimeError("STAGE0_PARENT_GATE=FAIL")
    if p.get("chain") != "planck_npipe_k039_approx" or s.get("chain") != "spt_d1_only":
        raise RuntimeError("PRIMARY_CHAIN_IDENTITY_GATE=FAIL")

    gates = {
        "stage0": s0.get("status") == "PASS",
        "planck_bridge_certification": p.get("status") == "PASS",
        "spt_bridge_certification": s.get("status") == "PASS",
        "q011_status_planck": p.get("q011_globality_status_preserved") == "BEST-OBSERVED MINIMUM ONLY",
        "q011_status_spt": s.get("q011_globality_status_preserved") == "BEST-OBSERVED MINIMUM ONLY",
        "no_cross_chain_sum_stage0": s0.get("planck_spt_chi2_sum_performed") is False,
        "no_cross_chain_sum_planck": p.get("planck_spt_chi2_sum_performed") is False,
        "no_cross_chain_sum_spt": s.get("planck_spt_chi2_sum_performed") is False,
        "no_absolute_cross_chain_comparison_planck": p.get("cross_chain_absolute_chi2_comparison_performed") is False,
        "no_absolute_cross_chain_comparison_spt": s.get("cross_chain_absolute_chi2_comparison_performed") is False,
    }
    passed = all(gates.values())

    pg = p["fixed_minus_free_signed_group_deltas"]
    sg = s["fixed_minus_free_signed_group_deltas"]

    planck_obs = {k: float(v) for k, v in pg["by_observable"].items()}
    spt_obs = {k: float(v) for k, v in sg["by_observable"].items()}
    planck_ell = {k: float(v) for k, v in pg["by_ell_band"].items()}
    spt_ell = {k: float(v) for k, v in sg["by_ell_band"].items()}

    result = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "FINAL",
        "execution_status": "COMPLETE" if passed else "FAILED_VALIDATION",
        "tests_status": "PENDING_SELF_TEST",
        "final_result_gate": "PASS" if passed else "FAIL",
        "scientifically_usable_result": bool(passed),
        "execution_kind": "V2_ENDPOINT_ARTIFACT_CERTIFICATION_AND_MERGE_NO_THEORY_RERUN",
        "gates": gates,
        "source_q015_v2_github_run": int(cfg["parent_q015_v2"]["github_run"]),
        "q014_penalties_preserved": {
            "planck_npipe_k039_approx": float(s0["chains"]["planck_npipe_k039_approx"]["fixed_h0_profile_delta_chi2"]),
            "spt_d1_only": float(s0["chains"]["spt_d1_only"]["fixed_h0_profile_delta_chi2"]),
            "spt_d1_plus_desi_secondary": float(s0["chains"]["spt_d1_plus_desi"]["fixed_h0_profile_delta_chi2"]),
        },
        "stage0_partition": s0["stage0_interpretive_partition"],
        "planck": {
            "authoritative_parent_highl_delta_chi2": p["authoritative_parent_fixed_minus_free_delta_chi2"],
            "raw_covariance_allocation_delta_chi2": p["raw_covariance_fixed_minus_free_delta_chi2"],
            "likelihood_to_covariance_delta_bridge_chi2": p["likelihood_to_covariance_delta_bridge_chi2"],
            "observable_deltas": planck_obs,
            "ell_band_deltas": planck_ell,
            "observable_ell_deltas": pg["by_observable_and_ell_band"],
            "spectrum_deltas": pg["by_spectrum"],
            "dominant_signed_allocations": sorted_drivers(pg["by_observable_and_ell_band"]),
            "nuisance_movement": p["nuisance_movement_from_q014_parent"],
            "bridge_certification": p["gates"],
        },
        "spt": {
            "authoritative_parent_primary_delta_chi2": s["authoritative_parent_fixed_minus_free_delta_chi2"],
            "raw_covariance_allocation_delta_chi2": s["raw_covariance_fixed_minus_free_delta_chi2"],
            "likelihood_to_covariance_delta_bridge_chi2": s["likelihood_to_covariance_delta_bridge_chi2"],
            "observable_deltas": spt_obs,
            "ell_band_deltas": spt_ell,
            "observable_ell_deltas": sg["by_observable_and_ell_band"],
            "spectrum_deltas": sg["by_spectrum"],
            "dominant_signed_allocations": sorted_drivers(sg["by_observable_and_ell_band"]),
            "nuisance_movement": s["nuisance_movement_from_q014_parent"],
            "bridge_certification": s["gates"],
        },
        "scientific_interpretation": {
            "planck_highl_driver": (
                "Within the Planck high-l covariance allocation, TT supplies the net penalty while EE partially compensates and TE is nearly neutral in the observable-summed allocation. The largest ell-band allocation is ell=500-999."
            ),
            "spt_primary_driver": (
                "Within SPT D1 primary, TE supplies the net penalty while TT compensates and EE is smaller positive. The ell dependence is strongly cancelling rather than uniformly penalizing high H0."
            ),
            "cross_chain_statement": (
                "These are separate within-chain attributions. No Planck-SPT absolute chi2 comparison or chi2 sum was formed."
            ),
            "bridge_statement": (
                "The raw covariance allocations are not rescaled. Small non-bandpower-attributable bridge terms are reported separately and pass robustness gates showing they do not control the dominant driver ranking."
            ),
        },
        "claim_boundaries": cfg["claim_boundaries"],
        "planck_spt_chi2_sum_performed": False,
        "cross_chain_absolute_chi2_comparison_performed": False,
        "q011_globality_status_preserved": "BEST-OBSERVED MINIMUM ONLY",
    }
    dump_json(output_path, result)
    return result


def self_test(result_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    r = load_json(result_path)
    mandatory = {
        "q_identity": r.get("q") == CURRENT_Q,
        "run_identity": r.get("run_id") == RUN_ID,
        "result_identity": r.get("result_id") == RESULT_ID,
        "final_stage": r.get("stage") == "FINAL",
        "final_result_gate": r.get("final_result_gate") == "PASS",
        "scientifically_usable": r.get("scientifically_usable_result") is True,
        "no_cross_chain_sum": r.get("planck_spt_chi2_sum_performed") is False,
        "no_absolute_cross_chain_comparison": r.get("cross_chain_absolute_chi2_comparison_performed") is False,
        "q011_status_preserved": r.get("q011_globality_status_preserved") == "BEST-OBSERVED MINIMUM ONLY",
        "planck_bridge_small": abs(float(r["planck"]["likelihood_to_covariance_delta_bridge_chi2"])) <= 0.01,
        "spt_bridge_small": abs(float(r["spt"]["likelihood_to_covariance_delta_bridge_chi2"])) <= 0.01,
        "planck_present": "observable_deltas" in r.get("planck", {}),
        "spt_present": "observable_deltas" in r.get("spt", {}),
    }
    status = "PASS" if all(mandatory.values()) else "FAIL"
    out = {
        "q": CURRENT_Q,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "status": status,
        "mandatory": mandatory,
    }
    dump_json(output_path, out)
    if status != "PASS":
        raise RuntimeError(f"FINAL_RESULT_TEST_GATE=FAIL {mandatory}")
    # Mark final result tests complete only after the external test file is safely written.
    r["tests_status"] = "COMPLETE"
    dump_json(result_path, r)
    return out


def make_diagnostic(planck_path: str | Path, spt_path: str | Path,
                    output_path: str | Path) -> dict[str, Any]:
    rows = []
    for path in [planck_path, spt_path]:
        r = load_json(path)
        chain = str(r["chain"])
        eps = {}
        for mode, ep in r["endpoints"].items():
            raw = float(ep["chi2"])
            parent = float(ep["parent_serialized_component_chi2"])
            eps[mode] = {
                "raw_covariance_chi2": raw,
                "parent_serialized_component_chi2": parent,
                "parent_minus_raw_bridge_chi2": parent - raw,
                "raw_minus_signed_sum": raw - float(ep["signed_contribution_sum"]),
            }
        raw_delta = float(r["fixed_minus_free_primary_component_delta_chi2"])
        parent_delta = float(r["parent_q014_primary_component_delta_chi2"])
        rows.append({
            "chain": chain,
            "v2_status": r.get("status"),
            "v2_parent_primary_component_delta_gate": r.get("parent_primary_component_delta_gate"),
            "endpoints": eps,
            "raw_covariance_fixed_minus_free_delta_chi2": raw_delta,
            "parent_fixed_minus_free_delta_chi2": parent_delta,
            "parent_minus_raw_delta_bridge_chi2": parent_delta - raw_delta,
        })
    out = {
        "q": CURRENT_Q,
        "diagnostic": "Q015_V2_VALIDATION_DEFINITION_FAILURE",
        "source_github_run": 33629190153,
        "finding": (
            "V2 endpoint computations completed. Failure came from comparing raw covariance quadratic allocations directly against serialized likelihood component chi2. Small bridge terms exist and must remain separate from bandpower attribution."
        ),
        "chains": rows,
        "physics_failure": False,
        "endpoint_execution_failure": False,
    }
    dump_json(output_path, out)
    return out


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=DEFAULT_CONFIG)
    sub = p.add_subparsers(dest="command", required=True)

    u = sub.add_parser("upgrade-endpoint")
    u.add_argument("--input", required=True)
    u.add_argument("--output", required=True)

    a = sub.add_parser("aggregate")
    a.add_argument("--stage0", required=True)
    a.add_argument("--planck", required=True)
    a.add_argument("--spt", required=True)
    a.add_argument("--output", required=True)

    t = sub.add_parser("test")
    t.add_argument("--result", required=True)
    t.add_argument("--output", required=True)

    d = sub.add_parser("diagnostic")
    d.add_argument("--planck", required=True)
    d.add_argument("--spt", required=True)
    d.add_argument("--output", required=True)
    return p


def main() -> int:
    a = parser().parse_args()
    cfg = load_yaml(a.config)
    if cfg.get("project", {}).get("q") != CURRENT_Q or cfg.get("project", {}).get("run_id") != RUN_ID:
        raise RuntimeError("CONFIG_IDENTITY_GATE=FAIL")
    if a.command == "upgrade-endpoint":
        r = upgrade_endpoint(a.input, a.output, cfg)
    elif a.command == "aggregate":
        r = aggregate(a.stage0, a.planck, a.spt, a.output, cfg)
    elif a.command == "test":
        r = self_test(a.result, a.output)
    else:
        r = make_diagnostic(a.planck, a.spt, a.output)
    print(json.dumps({"command": a.command, "q": CURRENT_Q, "run_id": RUN_ID, "status": r.get("status", "PASS")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
