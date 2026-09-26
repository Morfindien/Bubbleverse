# Bubbleverse Q042 Production V2 — bounded technical recovery

PROGRAM_ID: `Q042-PROD-V2`

This package is a **technical recovery** of Q042-PROD-V1. It does not change the
authoritative Q042 scientific specification.

## What V2 changes

- Keeps `q042_production_spec_v1.json` byte-identical.
- Keeps all frozen PolyChord settings and all 20 seeds.
- Keeps `seed_policy` and `max_ndead_runtime_encoding` as scientific/provenance metadata.
- Excludes those two metadata fields from the executable Cobaya `sampler.polychord` dictionary.
- Adds a real Cobaya 3.5.6 `update_info` regression gate.
- Reuses the existing 80 Q042-PROD-V1 Py-BOBYQA records from root run `36133813540`.
- Verifies V1 artifact names, source run, head SHA, artifact SHA-256, record identity and seed.
- Preserves the two recorded failed optimizer starts.
- Recomputes **zero** BOBYQA starts.
- Starts the 20 PolyChord posterior cells fresh because V1 produced no valid sampler checkpoints.
- Uses the existing 240-minute segment / 330-minute job / 48-segment finite policy.
- Reuses the frozen V1 scientific merge/classification logic.
- Remains fail-closed: missing required evidence => `UNRESOLVED`.

## New files

Repository root:

- `q042_production_v2.py`
- `q042_production_tests_v2.py`
- `q042_production_recovery_v2.json`
- `q042_production_source_lock_v2.json`
- `q042_setup_recovery_v2.sh`
- `q042_program_registry_patch_prod_v2.json`
- `q042_apply_registry_patch_prod_v2.py`
- `q042_apply_readme_patch_v2.py`
- `q042_install_instructions_prod_v2.md`
- `q042_delivery_manifest_prod_v2.json`

Workflow:

- `.github/workflows/q042-production-v2.yml`

## Existing files reused unchanged

- `q042_production_v1.py`
- `q042_production_spec_v1.json`
- `q042_production_source_lock_v1.json`
- `q042_setup_prod_v1.sh`
- `q042_planck_portability_v11.py`
- `q042_setup_v11.sh`
- `q042_prepare_frozen_core_v4.sh`
- `q041_planck_portability_v13.py`
- `.github/workflows/00-bubbleverse-start.yml`

Do **not** edit `q042_production_spec_v1.json`.

## Registry

The inspected live registry currently contains no Q042 entry. Apply the V2 entry
after the files are in the repository:

```bash
python q042_apply_registry_patch_prod_v2.py \
  --registry bubbleverse_program_registry.json \
  --patch q042_program_registry_patch_prod_v2.json
```

The helper is collision-fail-closed.

## README

The inspected README still tells the operator to select the historical
`000 🚀 BUBBLEVERSE START — SEGMENTED V5` display name.

Apply the differential README correction:

```bash
python q042_apply_readme_patch_v2.py
```

This documents the actual canonical launcher:

`.github/workflows/00-bubbleverse-start.yml`

No launcher code change is required.

## Execution

After manually adding/committing the files and applying the registry/README
patches:

1. Open **🚀 BUBBLEVERSE START**
2. Enter `Q042-PROD-V2`
3. Press **Run workflow**

The assistant did not upload, commit or dispatch anything.

START THIS:

`Q042-PROD-V2`
