#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

Q="Q026"
RUN="Q026-MASK6-NUISANCE-COUPLING-LOCALIZATION-V1"
RESULT="R-Q026-EDE-FULLMF-MASK6-COUPLING-001"
COSMO=("omega_b","omega_cdm","fEDE","log10z_c","thetai_scf","H0")
NUIS=("A_planck","calTE","calEE")

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--result",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    r=json.loads(Path(a.result).read_text(encoding="utf-8"))
    diag=r.get("diagnostics",{})
    expected={f"m{m}_e{a}{b}" for m in (3,6,7) for a,b in ((0,1),(0,2),(1,2))}
    gates={
      "Q_IDENTITY_GATE": r.get("q")==Q,
      "RUN_RESULT_IDENTITY_GATE": r.get("run_id")==RUN and r.get("result_id")==RESULT,
      "MODEL_BACKEND_GATE": r.get("scientific_surface",{}).get("model",{}).get("backend_commit")
        =="5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "LIKELIHOOD_GATE": r.get("scientific_surface",{}).get("likelihood")
        =="planck_NPIPE_highl_CamSpec.TTTEEE",
      "EDGE_COMPLETENESS_GATE": set(diag)==expected,
      "FIXED_VECTOR_COUNT_GATE": int(r.get("actual_new_likelihood_evaluations",-1))==252,
      "NO_OPTIMIZATION_GATE": int(r.get("optimizer_evaluations",-1))==0,
      "NO_Q024_RERUN_GATE": int(r.get("q024_permutations_evaluated",-1))==0,
      "COORDINATE_COMPLETENESS_GATE": all(
        set(v.get("coordinate_switch_effects",{}))==set(COSMO+NUIS) for v in diag.values()),
      "PAIR_COMPLETENESS_GATE": all(
        set(v.get("cosmology_x_shared_nuisance_pair_interactions",{}))
        =={f"{c}__x__{n}" for c in COSMO for n in NUIS} for v in diag.values()),
      "FINITE_GATE": all(
        all(finite(x) for x in v.get("coordinate_switch_effects",{}).values())
        and all(finite(x) for x in v.get("cosmology_x_shared_nuisance_pair_interactions",{}).values())
        for v in diag.values()),
      "Q025_COVARIANCE_PARENT_GATE": all(
        isinstance(v.get("q025_covariance_data_model_parent",{}).get("by_spectrum"),dict)
        and isinstance(v.get("q025_covariance_data_model_parent",{}).get("covariance_block_pair_terms"),dict)
        for v in diag.values()),
      "PARENT_PRESERVATION_GATE": all(r.get("journal_preservation",{}).values()),
      "NO_CAUSAL_OVERCLAIM_GATE": r.get("claim_boundaries",{}).get("physical_causality_claimed") is False,
    }
    ok=all(gates.values())
    out={"q":Q,"run_id":RUN,"result_id":RESULT,"stage":"Q026_MANDATORY_TESTS",
         "gates":gates,"tests_status":"COMPLETE","FINAL_RESULT_GATE":"PASS" if ok else "FAIL"}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0 if ok else 2

if __name__=="__main__":
    raise SystemExit(main())
