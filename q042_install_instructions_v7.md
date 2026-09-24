# Q042-PREFLIGHT-V7 — manual installation

V7 is a technical runtime-budget repair of V6. GitHub is read-only for ChatGPT; you manually upload/commit/run these files.

## Root files

- `q042_planck_portability_spec_v7.json`
- `q042_planck_portability_source_lock_v7.json`
- `q042_planck_portability_v7.py`
- `q042_planck_portability_tests_v7.py`
- `q042_setup_v7.sh`
- `q042_prepare_frozen_core_v4.sh` (unchanged helper; keep this exact filename)
- `q042_program_registry_patch_v7.json`
- `q042_apply_registry_patch_v7.py` (optional local/manual helper)
- `q042_delivery_manifest_v7.json`

## Workflow

Upload `q042-planck-portability-v7.yml` to:

`.github/workflows/q042-planck-portability-v7.yml`

## Registry

Manually ADD the `Q042-PREFLIGHT-V7` entry from `q042_program_registry_patch_v7.json` to `bubbleverse_program_registry.json`. Do not alter the permanent launcher.

## What V7 changes

Only the non-scientific PolyChord smoke/resume pilot budget changes: `nlive=1d`, `num_repeats=4`, `nprior=nlive`, `max_ndead=2`. V6 timed out after about 5h31m inside the preflight pilot. Production remains frozen at `nlive=25d`, `num_repeats=5d`, `precision_criterion=0.001`, `max_ndead=infinity`. BOBYQA settings are unchanged.

## Start

Open `🚀 BUBBLEVERSE START`, enter:

`Q042-PREFLIGHT-V7`

Expected final artifact on success: `q042-preflight-final-v7`. A PASS is still pre-science only and must return to Result Ingestion before production is generated.
