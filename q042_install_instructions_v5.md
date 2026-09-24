# Q042-PREFLIGHT-V5 — manual upload only

V5 is a technical gate repair of V4. V4 successfully initialized the frozen CamSpec/HiLLiPoP + ACT DR6 + DESI DR2 runtime and then failed because `EXTERNAL_DATA_IDENTITY_GATE` compared arm-native `q019_shape_*` and `q031_shape_*` likelihood terms as if they were external datasets.

## Upload these new files

- `q042_planck_portability_v5.py`
- `q042_planck_portability_tests_v5.py`
- `q042_planck_portability_spec_v5.json`
- `q042_planck_portability_source_lock_v5.json`
- `q042_setup_v5.sh`
- `.github/workflows/q042-planck-portability-v5.yml`
- `q042_program_registry_patch_v5.json`
- `q042_apply_registry_patch_v5.py` (optional helper for your local/manual registry merge)

## Reused unchanged from V4

`q042_prepare_frozen_core_v4.sh` remains the frozen-core helper. Do not rename or modify it for this repair.

## What changed

Only the external-data identity logic. V5 compares the exact contracted common external science blocks:

- `act_dr6_cmbonly.ACTDR6CMBonly` (A6)
- `act_dr6_lenslike.ACTDR6LensLike` (L6)
- `bao.desi_dr2` (D2)
- `sn.pantheonplus` (SN)
- A6 `A_act` / `P_act` parameter definitions and presence of `q041_act_calibration_shape`

Arm-native `q019_shape_*` / `q031_shape_*` terms are preserved and reported but are no longer required to be equal across native Planck implementations.

No model, data, prior, PolyChord setting, BOBYQA setting, materiality threshold, Q040 firewall, or science classification rule changed.

## Start

PROGRAM_ID: `Q042-PREFLIGHT-V5`

Open `🚀 BUBBLEVERSE START`, paste `Q042-PREFLIGHT-V5`, and press **Run workflow** after manually merging the registry entry.
