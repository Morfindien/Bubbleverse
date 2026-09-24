# Q042-PREFLIGHT-V3 — MANUAL UPLOAD

Q042-PREFLIGHT-V2 failed technically during the PolyChordLite build before any science result. V3 changes only the deployment/build layer: OpenMPI prerequisites are installed and gated because PolyChordLite setup.py defaults to MPI=1. The scientific contract and frozen PolyChord/BOBYQA numerical settings are unchanged.

ChatGPT has not written, committed, dispatched or rerun anything on GitHub.

## Upload to repository root

- q042_planck_portability_spec_v3.json
- q042_planck_portability_source_lock_v3.json
- q042_planck_portability_v3.py
- q042_planck_portability_tests_v3.py
- q042_setup_v3.sh
- q042_program_registry_patch_v3.json
- q042_apply_registry_patch_v3.py (optional local helper)
- q042_delivery_manifest_v3.json

## Upload workflow

Upload `q042-planck-portability-v3.yml` as:

`.github/workflows/q042-planck-portability-v3.yml`

## Registry

Merge the single ADD_ONLY V3 entry from `q042_program_registry_patch_v3.json` into `programs` in `bubbleverse_program_registry.json`. Do not change Q041-PLANCKPORT-V19 and do not change `.github/workflows/00-bubbleverse-start.yml`.

If you previously registered `Q042-PREFLIGHT-V2`, mark it `BROKEN` or `SUPERSEDED` in your manual registry maintenance; do not silently redirect it.

Optional helper:

`python q042_apply_registry_patch_v3.py --registry bubbleverse_program_registry.json --patch q042_program_registry_patch_v3.json --output bubbleverse_program_registry.q042-v3.json`

Inspect the output, then manually replace/upload the registry if correct.

## Start

OPEN: 🚀 BUBBLEVERSE START

PASTE PROGRAM_ID: `Q042-PREFLIGHT-V3`

PRESS: Run workflow

## Expected final artifact

`q042-preflight-final-v3`

This run remains PRE-SCIENCE ONLY. It must return `scientific_classification = NOT_AVAILABLE`. If it passes, send that final artifact to Result Ingestion before any production campaign is generated.
