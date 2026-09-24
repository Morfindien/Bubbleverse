# Q042-PREFLIGHT-V2 — MANUAL UPLOAD

ChatGPT has not written, committed, dispatched or rerun anything on GitHub.

## Upload to repository root

- q042_planck_portability_spec_v2.json
- q042_planck_portability_source_lock_v2.json
- q042_planck_portability_v2.py
- q042_planck_portability_tests_v2.py
- q042_setup_v2.sh
- q042_program_registry_patch_v2.json
- q042_apply_registry_patch_v2.py (optional local helper)
- q042_delivery_manifest_v2.json

## Upload workflow

Upload `q042-planck-portability-v2.yml` as:

`.github/workflows/q042-planck-portability-v2.yml`

## Registry

Merge the single ADD_ONLY entry from `q042_program_registry_patch_v2.json` into `programs` in `bubbleverse_program_registry.json`. Do not change Q041-PLANCKPORT-V19 and do not change `.github/workflows/00-bubbleverse-start.yml`.

Optional helper:

`python q042_apply_registry_patch_v2.py --registry bubbleverse_program_registry.json --patch q042_program_registry_patch_v2.json --output bubbleverse_program_registry.q042-v2.json`

Inspect the output, then manually replace/upload the registry if correct.

## Start

OPEN: 🚀 BUBBLEVERSE START

PASTE PROGRAM_ID: `Q042-PREFLIGHT-V2`

PRESS: Run workflow

## Expected final artifact

`q042-preflight-final-v2`

This run is PRE-SCIENCE ONLY. It must return `scientific_classification = NOT_AVAILABLE`. If it passes, send that final artifact to Result Ingestion before any production campaign is generated.
