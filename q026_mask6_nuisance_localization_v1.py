#!/usr/bin/env python3
"""
Bubbleverse Q026 — targeted coordinate/coupling localization.

Scientific contract
-------------------
CURRENT Q: Q026

Question:
Why does mask 6 transition to shared-nuisance-dominated basin attribution while
masks 3 and 7 remain cosmology-dominated, and can this difference be localized
to specific nuisance coordinates, cosmology–nuisance couplings, or mask-sensitive
CamSpec covariance/data-model structure without assuming an instrumental or
foreground systematic?

Design:
- Reuse authoritative Q022 endpoints through the validated Q025 V2 loader.
- Reuse Q025 V2 endpoint covariance/data-model decomposition read-only.
- No optimization, sampling, endpoint generation, or Q024 permutation rerun.
- For each of 9 basin edges, evaluate:
    base endpoint A
    9 one-coordinate switches A->B
    18 cosmology x shared-nuisance double switches
  = 28 fixed vectors per edge, 252 evaluations total.
- Compute exact 2x2 finite-switch interaction contrasts for each of the
  6 cosmology x 3 shared-nuisance coordinate pairs.
- Coordinate-switch effects and pair contrasts are technical local functional
  diagnostics, not physical causal decomposition.
"""
from __future__ import annotations
import argparse, json, math, os
from pathlib import Path
from typing import Any, Mapping
import yaml

ROOT = Path(__file__).resolve().parent
Q = "Q026"
RUN = "Q026-MASK6-NUISANCE-COUPLING-LOCALIZATION-V1"
RESULT = "R-Q026-EDE-FULLMF-MASK6-COUPLING-001"
MASKS = (3, 6, 7)
EDGES = ((0,1),(0,2),(1,2))
COSMO = ("omega_b","omega_cdm","fEDE","log10z_c","thetai_scf","H0")
NUIS = ("A_planck","calTE","calEE")
COORDS = COSMO + NUIS

def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False

def write_json(path: str|Path, obj: Any) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix+".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str)+"\n", encoding="utf-8")
    os.replace(t,p)

def load_cfg(path: str|Path) -> dict[str,Any]:
    c = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if c["project"]["q"] != Q or c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("Q_OR_RUN_IDENTITY_GATE=FAIL")
    if c["model"]["name"] != "MOD-EDE-N3" or int(c["model"]["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if c["model"]["backend_commit"] != "5a131c91d657dd9a7c6364cc45b038710f8d0d97":
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if c["likelihood"]["full_mf"] != "planck_NPIPE_highl_CamSpec.TTTEEE":
        raise RuntimeError("LIKELIHOOD_GATE=FAIL")
    for k in ("no_optimization","no_sampling","no_new_endpoints","no_q024_permutation_rerun"):
        if c["rules"].get(k) is not True:
            raise RuntimeError(f"{k.upper()}_GATE=FAIL")
    return c

def switch(a: Mapping[str,float], b: Mapping[str,float], names) -> dict[str,float]:
    out = {k: float(v) for k,v in a.items()}
    for n in names:
        out[n] = float(b[n])
    return out

def objective(model, values: Mapping[str,float]) -> float:
    lp = model.logposterior(dict(values))
    x = getattr(lp, "logpost", lp)
    if not finite(x):
        raise RuntimeError("FINITE_OBJECTIVE_GATE=FAIL")
    return float(-2.0*float(x))

def get_endpoint_delta_from_q025(q025: Mapping[str,Any], key: str) -> Mapping[str,Any]:
    d = q025.get("diagnostics",{}).get(key)
    if not isinstance(d, Mapping):
        raise RuntimeError(f"Q025_DIAGNOSTIC_GATE=FAIL key={key}")
    ed = d.get("endpoint_delta",{})
    if not isinstance(ed, Mapping):
        raise RuntimeError(f"Q025_ENDPOINT_DELTA_GATE=FAIL key={key}")
    return ed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="q026_mask6_nuisance_localization_v1_config.yml")
    ap.add_argument("--q021-dir", required=True)
    ap.add_argument("--q022-dir", required=True)
    ap.add_argument("--q025-result", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    c = load_cfg(a.config)

    import q025_fullmf_component_attribution_v2 as q25

    q025 = json.loads(Path(a.q025_result).read_text(encoding="utf-8"))
    if q025.get("q") != "Q025" or q025.get("result_id") != "R-Q025-EDE-FULLMF-BASIN-COMPONENT-ATTRIBUTION-002":
        raise RuntimeError("Q025_PARENT_IDENTITY_GATE=FAIL")
    if q025.get("FINAL_RESULT_GATE") not in (None,"PASS"):
        raise RuntimeError("Q025_PARENT_FINAL_GATE=FAIL")

    parent25 = q25.load_cfg(ROOT / c["parent_q025_config"])
    final22 = q25.load_q022_final(a.q022_dir)
    diagnostics = {}
    eval_count = 0

    for mask in MASKS:
        endpoints = {
            s: q25.load_q022_endpoint(a.q022_dir, a.q021_dir, final22, mask, s)
            for s in (0,1,2)
        }
        for sa,sb in EDGES:
            key = f"m{mask}_e{sa}{sb}"
            A = endpoints[sa]["params"]; B = endpoints[sb]["params"]

            # Primordial and foreground remain exactly at endpoint A in the
            # coordinate-localization experiment. Only COSMO+shared nuisance switch.
            model = q25.build_full_model(parent25, A)

            f0 = objective(model, A); eval_count += 1
            singles = {}
            for p in COORDS:
                singles[p] = objective(model, switch(A,B,[p])); eval_count += 1

            pairs = {}
            for cp in COSMO:
                for np in NUIS:
                    f2 = objective(model, switch(A,B,[cp,np])); eval_count += 1
                    # 2x2 finite-switch interaction contrast:
                    # f(cp,np)-f(cp)-f(np)+f(base)
                    pairs[f"{cp}__x__{np}"] = float(
                        f2 - singles[cp] - singles[np] + f0
                    )

            single_effects = {p: float(singles[p]-f0) for p in COORDS}
            q025_delta = get_endpoint_delta_from_q025(q025,key)

            diagnostics[key] = {
                "mask": mask, "edge": [sa,sb],
                "base_objective": f0,
                "coordinate_switch_effects": single_effects,
                "cosmology_x_shared_nuisance_pair_interactions": pairs,
                "largest_abs_nuisance_switch": max(
                    NUIS, key=lambda p: abs(single_effects[p])
                ),
                "largest_abs_cosmology_switch": max(
                    COSMO, key=lambda p: abs(single_effects[p])
                ),
                "largest_abs_pair_interaction": max(
                    pairs, key=lambda p: abs(pairs[p])
                ),
                "q025_covariance_data_model_parent": {
                    "by_spectrum": q025_delta.get("by_spectrum",{}),
                    "by_spectrum_band": q025_delta.get("by_spectrum_band",{}),
                    "covariance_block_pair_terms": q025_delta.get("covariance_block_pair_terms",{}),
                },
                "interpretation":
                    "LOCAL_FIXED_VECTOR_FUNCTIONAL_DIAGNOSTIC_NONCAUSAL"
            }

    expected = 9*(1+len(COORDS)+len(COSMO)*len(NUIS))
    if eval_count != expected:
        raise RuntimeError(f"EVALUATION_COUNT_GATE=FAIL actual={eval_count} expected={expected}")

    # Cross-mask summary: mask 6 compared with masks 3/7.
    def abs_med(vals):
        z=sorted(abs(float(x)) for x in vals)
        n=len(z)
        return z[n//2] if n%2 else 0.5*(z[n//2-1]+z[n//2])

    nuisance_by_mask = {}
    pair_by_mask = {}
    for m in MASKS:
        rows=[v for v in diagnostics.values() if v["mask"]==m]
        nuisance_by_mask[m]={
            p: abs_med([r["coordinate_switch_effects"][p] for r in rows]) for p in NUIS
        }
        pair_by_mask[m]={
            pair: abs_med([r["cosmology_x_shared_nuisance_pair_interactions"][pair] for r in rows])
            for pair in [f"{c0}__x__{n0}" for c0 in COSMO for n0 in NUIS]
        }

    out = {
        "q": Q, "run_id": RUN, "result_id": RESULT,
        "status": "COMPLETE",
        "actual_new_likelihood_evaluations": eval_count,
        "optimizer_evaluations": 0,
        "q024_permutations_evaluated": 0,
        "scientific_surface": {
            "model": c["model"],
            "likelihood": c["likelihood"]["full_mf"],
            "masks": list(MASKS),
            "authoritative_endpoints": "Q022_V2_UNCHANGED",
            "q025_parent": "R-Q025-EDE-FULLMF-BASIN-COMPONENT-ATTRIBUTION-002"
        },
        "diagnostics": diagnostics,
        "cross_mask_summary": {
            "median_abs_nuisance_switch_by_mask": nuisance_by_mask,
            "median_abs_cosmology_x_nuisance_pair_by_mask": pair_by_mask
        },
        "claim_boundaries": {
            "physical_causality_claimed": False,
            "calibration_failure_proven": False,
            "instrumental_systematic_proven": False,
            "foreground_systematic_proven": False,
            "distinct_physical_cosmologies_proven": False
        },
        "journal_preservation": {
            "q022_preserved": True,
            "q023_preserved": True,
            "q024_preserved": True,
            "q025_preserved": True
        }
    }
    write_json(a.output,out)
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
