# Q042-PREFLIGHT-V4 — MANUAL UPLOAD

Q042-PREFLIGHT-V3 failed technically before Q042 runtime/science because the inherited Q041 cold-cache helper performed three 10-second NERSC availability probes and exited 75.

V4 changes only transport/bootstrap. It first tries the exact Q041 V19 base cache. If the required HiLLiPoP TT payload is absent, it keeps the exact Q032 V2 setup and official `planck_2020_hillipop.TT` v4.2 source, but replaces the short probe with three bounded real `cobaya-install` attempts (max 1800 s each).

No GitHub write, commit, dispatch or rerun was performed by ChatGPT. GitHub was used read-only.

## Upload to repository root

- q042_planck_portability_spec_v4.json
- q042_planck_portability_source_lock_v4.json
- q042_planck_portability_v4.py
- q042_planck_portability_tests_v4.py
- q042_prepare_frozen_core_v4.sh
- q042_setup_v4.sh
- q042_program_registry_patch_v4.json
- q042_apply_registry_patch_v4.py (optional local helper)
- q042_delivery_manifest_v4.json

## Workflow

Upload `q042-planck-portability-v4.yml` as:

`.github/workflows/q042-planck-portability-v4.yml`

## Registry

Merge the single ADD_ONLY `Q042-PREFLIGHT-V4` entry into `programs` in `bubbleverse_program_registry.json`. Do not modify Q041-PLANCKPORT-V19 or `.github/workflows/00-bubbleverse-start.yml`.

If V3 is registered, mark it BROKEN/SUPERSEDED manually.

Optional helper:

`python q042_apply_registry_patch_v4.py --registry bubbleverse_program_registry.json --patch q042_program_registry_patch_v4.json --output bubbleverse_program_registry.q042-v4.json`

## Start

OPEN: 🚀 BUBBLEVERSE START

PASTE PROGRAM_ID: `Q042-PREFLIGHT-V4`

PRESS: Run workflow

Expected final artifact: `q042-preflight-final-v4`

PRE-SCIENCE ONLY: `scientific_classification = NOT_AVAILABLE`.
