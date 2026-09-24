# Q042-PREFLIGHT-V6 — manual upload only

V6 is a version-integrity repair of V5. V5 passed its scientific-program static gate, then its static validator exited 2 because the workflow passed the V4 workflow filename to the V5 validator. A pre-execution audit also found stale V4 pilot-result filenames and V4 result-artifact names in the V5 registry patch.

## Upload these files

- `q042_planck_portability_v6.py`
- `q042_planck_portability_tests_v6.py`
- `q042_planck_portability_spec_v6.json`
- `q042_planck_portability_source_lock_v6.json`
- `q042_setup_v6.sh`
- `.github/workflows/q042-planck-portability-v6.yml`
- `q042_program_registry_patch_v6.json`
- `q042_apply_registry_patch_v6.py` (optional local/manual registry merge helper)

## Reused unchanged

- `q042_prepare_frozen_core_v4.sh`

## V6 repair only

1. The static validator now validates `.github/workflows/q042-planck-portability-v6.yml`.
2. Pilot output is consistently `q042_pilot_result_v6.json`.
3. Registry result artifacts are consistently V6.
4. V5 external-data identity repair remains unchanged: only A6/L6/D2/SN + ACT calibration contract must match across Planck arms; native arm-specific nuisance likelihoods remain distinct.
5. No model, data, prior, PolyChord, BOBYQA, materiality or science-classification setting changed.

PROGRAM_ID: `Q042-PREFLIGHT-V6`
