# Q048 V138 — GitHub upload/apply instructions

Base observed before V138 execution: `Morfindien/Bubbleverse` `main@6ec31f4d97883a781411231efeb16a07395e0c8b`. Re-check HEAD before applying; do not overwrite historical files.

Upload the new V138 top-level result/handoff/journal/manifest files as new immutable records. Runtime/code evidence may be placed under the repository's established `Q048_V138_RUNTIME/` convention if that convention is used; preserve exact bytes and names.

The authoritative current actual state remains actual123/frontier850. Do not publish actual124 or a V138 consumer result as part of this package.

After upload, verify SHA-256 against `Q048_V138_SHA256SUMS.txt`, then run Result Ingestion 2.1.0 on `Q048_V138_HANDOFF_TO_INGESTION_V1.json` plus the cumulative journal.
