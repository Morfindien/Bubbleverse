# Q042-PROD-V3 — deployment-only repair

Q042-PROD-V2 failed in `import-bobyqa` before the production module could execute because that job did not install NumPy.

Failure:
`ModuleNotFoundError: No module named 'numpy'`

V3 changes exactly one runtime behavior:
- `import-bobyqa` now installs `PyYAML==6.0.2` and `numpy==1.26.4` immediately after `actions/setup-python@v7`.

Everything scientific remains unchanged:
- byte-identical Q042 V1 scientific specification
- same 20 posterior cells
- same 20 PolyChord seeds
- same PolyChord settings and finite segment policy
- same 80 V1 BOBYQA records, with zero BOBYQA recomputation
- same final scientific classifier and fail-closed behavior

V2 is preserved as a documented deployment failure and V3 supersedes it.

Files to add:
- q042_production_v3.py
- q042_production_tests_v3.py
- q042_production_recovery_v3.json
- q042_production_source_lock_v3.json
- q042_setup_recovery_v3.sh
- q042_program_registry_patch_prod_v3.json
- q042_apply_registry_patch_prod_v3.py
- .github/workflows/q042-production-v3.yml

Then apply the registry patch manually:
`python q042_apply_registry_patch_prod_v3.py`

Normal launch:
OPEN: 🚀 BUBBLEVERSE START
PASTE: Q042-PROD-V3
PRESS: Run workflow

The assistant did not upload, commit, rerun, or dispatch anything.
