# Q052-NATIVEPAIR-V1 — installation/start

1. Upload the root files listed in `FILES_Q052_NATIVEPAIR_V1.md`.
2. Place `q052-native-pair-v1.yml` exactly at `.github/workflows/q052-native-pair-v1.yml`.
3. Merge the single ADD_ONLY entry in `q052_program_registry_patch_v1.json` into the current `bubbleverse_program_registry.json`.
4. Keep `.github/workflows/00-bubbleverse-start.yml` unchanged.
5. Add the text from `README_Q052_NATIVEPAIR_V1.md` to the current README.
6. Commit the installation.
7. Open **🚀 BUBBLEVERSE START**, enter `Q052-NATIVEPAIR-V1`, and run once.
8. Return `Q052_NATIVEPAIR_RESULT_V1.json` and the four raw worker artifacts to Result Ingestion & Routing 2.3.0.

Do not rerun automatically on failure. The first exact conclusion-critical blocker is a valid Q052 result for routing.
