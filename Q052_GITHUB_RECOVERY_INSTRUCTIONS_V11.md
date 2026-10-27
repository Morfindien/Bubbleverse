# Q052 V11 — what to put on GitHub

The native pair from run `40445054618` already succeeded. **Do not rerun it.**

Upload/replace these files:

1. Replace root `q052_validated_diag_v3.py` with the V11 fixed version.
2. Replace root `test_q052_validated_diag_v3.py` with the V11 regression version.
3. Add root `q052_collect_recovery_v3.py`.
4. Add root `Q052_RUN40445054618_ARTIFACT_MANIFEST_V11.json`.
5. Add `.github/workflows/q052-validateddiag-collect-recovery-v3.yml`.
6. Add the V11 journal/ledger/report/handoff and recovered JSON outputs as repository memory.

Then either:

- use the already reconstructed `recovered_collect/*.json` files directly as the Result Ingestion input, or
- run **Q052 validated diagnostics V3 collector recovery** with `source_run_id=40445054618`; it downloads the existing L/R artifacts and performs no native computation.

Do not use **Q052 validated diagnostics V3** again merely to fix this collector error.
