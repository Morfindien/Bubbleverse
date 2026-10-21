# Q048 V139 ingestion — GitHub upload/apply instructions

Base observed before packaging: `Morfindien/Bubbleverse` `main@fc704a128f1a5cd88245f3db92094f4cd219aa73`. Re-check HEAD before applying. Preserve all V139 files already committed; do not overwrite or relabel V139 FAIL.

Upload the new V139-ingestion/V140 files at repository root using the filenames in `Q048_V139_INGESTION_OUTPUT_MANIFEST_V1.json`. They are new append-only/current-routing records. The new cumulative journal is `Q047_SAMLET_JOURNAL_Q048_V139_INGESTED_V1.md`; retain every older journal unchanged.

Critical next-engine inputs are the new cumulative journal, `Q048_V139_INGESTION_STATE_V1.json`, `Q048_V140_NEXT_BUILDER_TASK_REPAIRED_CONDITIONAL_CONSUMER_850_840_V1.json`, `Q048_V139_INGESTION_RECOVERY_MAP_V1.json`, plus the immutable V139 failure artifacts and V138 proof runtime referenced by exact hashes.

Do not mark actual124 current in GitHub indexes yet. That may occur only after a future V140 accepted checkpoint/readback. Current remains actual123/frontier850; V138 proof remains accepted/unconsumed.

If HEAD changed since `fc704a128f1a5cd88245f3db92094f4cd219aa73`, reconcile before upload; never overwrite another writer or historical V139/V138 artifacts.
