# Q042-EXECMECH-V1 — MANUAL INSTALL

No GitHub write, commit, dispatch, rerun, or file mutation was performed by ChatGPT.

Upload these files to repository root:
- q042_execution_mechanism_preregister_v1.json
- q042_execution_mechanism_source_lock_v1.json
- q042_v19_diagnostic_reference_v1.json
- q042_execution_mechanism_v1.py
- q042_execution_mechanism_tests_v1.py
- q042_program_registry_patch_v1.json
- q042_apply_registry_patch_v1.py (helper only; not called by the workflow)

Upload this file to:
- .github/workflows/q042-execution-mechanism-v1.yml
  (source file delivered as q042-execution-mechanism-v1.yml)

Registry:
- Do NOT replace or rename .github/workflows/00-bubbleverse-start.yml.
- Add the object in q042_program_registry_patch_v1.json under bubbleverse_program_registry.json -> programs.
- The patch is ADD-ONLY; it does not modify Q041-PLANCKPORT-V19.
- Optional local helper: python q042_apply_registry_patch_v1.py --registry bubbleverse_program_registry.json
  This writes bubbleverse_program_registry.q042-v1.json for you to inspect and manually upload as the registry replacement.

Then start:
OPEN: 🚀 BUBBLEVERSE START
PASTE PROGRAM_ID: Q042-EXECMECH-V1
PRESS: Run workflow

Expected artifact:
q042-execmech-v1

Expected successful decision:
REJECT_MORE_OF_SAME_MCMC__SELECT_POLYCHORD_PLUS_MULTISTART_BOBYQA

This run is diagnostic/methodological only. It must not be interpreted as a Q041 cosmological result.
