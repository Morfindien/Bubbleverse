# Bubbleverse Q042 Production V1 — manual installation

PROGRAM_ID: `Q042-PROD-V1`

GitHub mutation by the assistant is forbidden. Upload/commit these files manually.

## New production files at repository root
- `q042_production_v1.py`
- `q042_production_tests_v1.py`
- `q042_production_spec_v1.json`
- `q042_production_source_lock_v1.json`
- `q042_setup_prod_v1.sh`
- `q042_program_registry_patch_prod_v1.json`
- `q042_apply_registry_patch_prod_v1.py`

## Workflow
Upload:
- `q042-production-v1.yml`

to:
- `.github/workflows/q042-production-v1.yml`

## Reused unchanged files
The production campaign depends on the already validated V11/Q041 runtime surface:
- `q042_planck_portability_v11.py`
- `q042_setup_v11.sh`
- `q042_prepare_frozen_core_v4.sh`
- `q041_planck_portability_v13.py`
- `q041_setup_v19.sh`

If `q042_prepare_frozen_core_v4.sh` is already present and identical, do not replace it unnecessarily.

## Permanent launcher
Do **not** modify:
- `.github/workflows/00-bubbleverse-start.yml`

It is already the permanent safe exact-registry launcher.

## Registry
After the new files are committed, merge the new entry into the existing registry manually, or run locally before committing:

```bash
python q042_apply_registry_patch_prod_v1.py \
  --registry bubbleverse_program_registry.json \
  --patch q042_program_registry_patch_prod_v1.json
```

The helper is collision-fail-closed: it will not silently overwrite a different existing `Q042-PROD-V1` entry.

## Start
Open `🚀 BUBBLEVERSE START`, paste:

`Q042-PROD-V1`

and press **Run workflow**.

The root production run creates the frozen environment, 20 initial PolyChord production cells, and 80 atomic external Py-BOBYQA starts. Long PolyChord cells continue through genuine checkpoint/resume workflow runs. The collector emits the final production result only after all required final cell/start artifacts exist, or emits a controlled unresolved result when the finite orchestration stop condition is reached.
