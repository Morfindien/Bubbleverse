# Q048 V26 ingestion — upload/apply instructions

Verified project-memory base: `Morfindien/Bubbleverse@b1819ddc2e459a214e80fd450160d3d613867249`. No GitHub write was performed by this ingestion.

Upload the files in this ingestion package as **new files**. Do **not** overwrite or delete the existing V26 origin files, the `metadata_draft_v1` history, V25 actual artifacts, V24 proof history or V12 guard history.

For the next Builder run, the minimum operator handoff is:

1. `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0.md` — existing verified prompt, SHA256 `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`.
2. `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V26_INGESTED_V1.md`.
3. `Q048_MOVING_H_DOMAIN_V26_INGESTION_HANDOFF_TO_BUILDER_V1.md`.
4. `Q048_MOVING_H_DOMAIN_V26_INGESTION_RESULT_V1.md`.
5. `Q048_MOVING_H_DOMAIN_V26_NEXT_BUILDER_TASK_V1.json` when the runtime can consume structured task input.

The task JSON carries verified Library file IDs for current V26 proof/correction bytes, V25 parent bytes, V12 guard bytes and V25 consumer implementation patterns. The next engine must recover those exact objects rather than reconstructing them from summaries.

Repository target paths are proposed as root-level filenames to match the current Bubbleverse upload pattern. No CURRENT_STATE/global registry path was verified or modified. If `main` has advanced beyond `b1819ddc2e459a214e80fd450160d3d613867249`, reconcile before any replacement-style write; ordinary new-file uploads remain append-only.

After a Builder result returns, route exactly once back to Result Ingestion & Routing2.1.0. Do not continue below1320 automatically.
