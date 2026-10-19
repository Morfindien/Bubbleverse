# Q048 V107 ingestion — upload/apply instructions

Base observed before this ingestion package: `Morfindien/Bubbleverse@0a5c39da6d80cd0bc57efd122cbcf6f020a65d23`.

Upload each delivered file individually to the repository root using the exact filename. Create new files; do not overwrite historical V101/V102/V107 artifacts. The complete journal successor `Q047_SAMLET_JOURNAL_Q048_V107_INGESTED_SOURCE_CORRECT_V1.md` is a new append-only journal version, not a replacement of historical journal bytes.

After upload, verify the committed SHA-256 values against `Q048_V107_INGESTION_OUTPUT_MANIFEST_V1.json` and update the existing current-state/index/route pointers to reference V107 as current source-correct actual111/frontier970 and V108 Mathematics bridge as the next task.

Do not mark V108 executed or V102 relabelled until Mathematics returns a separately validated bridge artifact.
