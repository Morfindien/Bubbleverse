# Q042-PREFLIGHT-V9 — manual install

Upload these files individually to the Bubbleverse repository. Do not archive them.

- q042_planck_portability_v9.py
- q042_planck_portability_tests_v9.py
- q042_planck_portability_spec_v9.json
- q042_planck_portability_source_lock_v9.json
- q042_setup_v9.sh
- q042_prepare_frozen_core_v4.sh
- .github/workflows/q042-planck-portability-v9.yml
- q042_program_registry_patch_v9.json
- q042_apply_registry_patch_v9.py

Apply the registry patch manually according to the repository policy. Do not modify `.github/workflows/00-bubbleverse-start.yml`.

Start with PROGRAM_ID: `Q042-PREFLIGHT-V9`.

V9 repair scope: process isolation only. V7 successfully completed the first bounded PolyChord smoke run and wrote resume state, but the second PolyChord invocation in the same Python process failed after MPI_FINALIZE. V9 runs initial PolyChord and resume PolyChord in separate fresh child processes and likewise isolates each BOBYQA start. V7 pilot numerical settings and all frozen production numerical settings are unchanged.


V9-specific repair: the resume subprocess reinstalls the frozen HiLLiPoP runtime patch, then loads Cobaya's exact stored updated info via OutputReadOnly. It does not regenerate the likelihood dictionary as the resume input and does not use allow_changes.
