# Q048 V136 ingestion — upload/apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `main@cc034748529ba1c7097c4ccd56218e3792eeace4`. Reconcile first if main has moved.

Do not overwrite historical V134/V135/V136 source records. Add the new V136-ingestion/V137 files as new versioned records. The new cumulative journal `Q047_SAMLET_JOURNAL_Q048_V136_INGESTED_V1.md` supersedes the current navigation pointer only; it does not delete or rewrite `Q047_SAMLET_JOURNAL_Q048_V136_CONDITIONAL_PROOF_APPENDED_V1.md`.

The commit `cc034748529ba1c7097c4ccd56218e3792eeace4` already contains these V136 top-level files: Q047_SAMLET_JOURNAL_Q048_V136_CONDITIONAL_PROOF_APPENDED_V1.md, Q048_V136_ACCEPTANCE_V1.json, Q048_V136_FILES_V1.md, Q048_V136_RESULT_AND_HANDOFF_V1.md. Do not duplicate them under new identities.

Before V137 freeze, ensure the missing V136 runtime evidence is recoverable at the paths in `Q048_V136_INGESTION_RECOVERY_MAP_V1.json`. Recommended repo paths are under `Q048_V136_RUNTIME/`; exact SHA256 must match. Current search-missing set: Q048_V136_RAW_V1.json, Q048_V136_VERIFICATION_V1.json, Q048_V136_EXECUTION_V1.json, Q048_V136_FREEZE_V1.json, Q048_V136_SPEC_V1.json, Q048_V136_HANDOFF_TO_INGESTION_V1.json, Q048_V136_RESULT_STATE_V1.json.

Upload all files indexed in `Q048_V136_INGESTION_FILES_V1.md`. Treat `Q048_V136_INGESTION_STATE_V1.json` and the new cumulative journal as the new current working view; preserve all older versions. V137 task is prepared only — uploading it is not execution and must not advance actual122/frontier860.

After upload, verify hashes against `Q048_V136_INGESTION_SHA256SUMS.txt`. Then hand `Q048_V137_NEXT_BUILDER_TASK_CONDITIONAL_CONSUMER_860_850_V1.json` plus `Q047_SAMLET_JOURNAL_Q048_V136_INGESTED_V1.md` and recovery map to Builder2.2.0. Stop after one terminal V137 consumer result and return to Result Ingestion.
