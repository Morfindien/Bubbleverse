# Q048 V142 upload/apply instructions

Upload the V142 delivery files individually to `Morfindien/Bubbleverse` on top of the verified base commit recorded in `Q048_V142_GITHUB_MEMORY_UPDATE_V1.json`.

Important: preserve all existing V141 files unchanged. V142 is a new accepted repair proof, not a replacement for the V141 obstruction.

After upload, Result Ingestion should use `Q048_V142_HANDOFF_TO_INGESTION_V1.json` and the cumulative journal as the authoritative incoming package. Do not run a consumer before ingestion registers the proof exactly once.
