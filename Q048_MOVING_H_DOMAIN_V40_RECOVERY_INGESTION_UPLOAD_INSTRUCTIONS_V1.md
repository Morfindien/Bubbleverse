# Q048 V40 recovery ingestion — upload/apply instructions V1

Base repository observed: `Morfindien/Bubbleverse` main@`99f9bea2374bf840a6bbd45d5c75c57ba09b7905`.

Upload the following as **new versioned files at repository root** using exact names:

- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_RESULT_V1.md`
- `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V40_RECOVERY_INGESTED_V1.md`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_BLOCKER_HANDOFF_V1.md`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_EVIDENCE_V1.json`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_STATE_DELTA_V1.json`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_FILES_V1.md`
- `Q048_MOVING_H_DOMAIN_V40_RECOVERY_INGESTION_OUTPUT_MANIFEST_V1.json`

Do not overwrite historical V40, recovery, V39, V38 or earlier files.

After coherent upload, the newest Q048 working journal view may point to `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V40_RECOVERY_INGESTED_V1.md`. Do not change actual state beyond **82/frontier1260** and do not clear `BLOCKED_MISSING_STATE`.

No canonical `CURRENT_STATE` path was verified, so do not create a competing global state file.

Only genuine original byte copies of all seven missing V40 artifacts, each matching its frozen SHA256, can clear the blocker. Re-running Builder or reconstructing files from summaries is not an acceptable substitute.
