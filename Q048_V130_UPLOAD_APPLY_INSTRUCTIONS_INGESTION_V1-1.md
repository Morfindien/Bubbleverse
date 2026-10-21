# Q048 V130 ingestion — upload/apply instructions

Base observed: `Morfindien/Bubbleverse@61ea41aaaf1f8cf2c598e3244622d71897ca74ad`.

1. Upload the new ingestion files listed in `Q048_V130_INGESTION_OUTPUT_MANIFEST_V1.json` to repository root using their exact filenames.
2. Add the locally verified V130 producer payloads that are still missing at the observed root: `Q048_V130_RAW_V1.json`, `Q048_V130_SPEC_V1.json`, `Q048_V130_FREEZE_V1.json`, `Q048_V130_EXECUTION_V1.json`, `Q048_V130_DELIVERY_VALIDATION_V1.json`, `Q048_V130_SOURCE_PROVENANCE_V1.json`, and the immutable parent `Q048_V129_TWO_OPERATOR_CONDITIONAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json` when following the existing root convention.
3. Do **not** overwrite or rename the existing V130 producer journal/result objects. The new complete journal is a new version: `Q047_SAMLET_JOURNAL_Q048_V130_INGESTED_V1.md`.
4. Treat `Q048_V131_NEXT_BUILDER_TASK_TWO_OPERATOR_CONDITIONAL_CONSUMER_880_870_V1.json` as the one next handoff. Do not run V130 mathematics again unchanged.
5. After upload, the repository head/commit should be recorded by the next engine; this package does not claim synchronization.

Preferred apply mode: one coherent commit containing the complete ingestion package and missing immutable producer payloads.
