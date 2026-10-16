# Q048 V19 ingestion — manual GitHub apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `main@e34e6187e40a56ef790ef0ad2e61f5546b1720b9`  
Status: **USER_UPLOAD_PENDING** — no write was attempted in this ingestion.

## 1. Complete the partial V19 origin upload

The latest observed commit contains 10 V19 root files, but these expected Builder-origin files are still absent:

- `Q048_FREC_MOVING_H_V19_JOURNAL_APPEND.md`
- `q048_frec_moving_h_result_v19.json`
- `q048_frec_moving_h_spec_v19.json`
- `q048_frec_moving_h_v19.py`
- `q048_frec_moving_h_verify_v19.py`
- `q048_frec_moving_h_run_manifest_v19.json`
- `q048_frec_moving_h_execution_diagnostic_v19.json`

Do not omit the raw result `q048_frec_moving_h_result_v19.json` (SHA256 `a275caaab5d3a4836c492fb05fb83fbdaf4838527123bbdcfebad5e1a9b219de`). Preserve all already-uploaded V19/V18/V17/V12 evidence unchanged.

## 2. Add the new V19 ingestion package

Upload these files to repository root following the current project convention:

- `Q048_FREC_MOVING_H_V19_INGESTION_RESULT_V1.md`
- `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V19_INGESTED_V1.md`
- `Q048_FREC_MOVING_H_V19_INGESTION_STATE_DELTA_V1.json`
- `Q048_FREC_MOVING_H_V19_NEXT_MATHEMATICS_TASK_V1.json`
- `Q048_FREC_MOVING_H_V19_INGESTION_HANDOFF_TO_MATHEMATICS_V1.md`
- `Q048_FREC_MOVING_H_V19_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_FREC_MOVING_H_V19_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_FREC_MOVING_H_V19_INGESTION_UPLOAD_INSTRUCTIONS_V1.md`
- `Q048_FREC_MOVING_H_V19_INGESTION_FILES_V1.md`
- `Q048_FREC_MOVING_H_V19_INGESTION_OUTPUT_MANIFEST_V1.json`

## 3. Guarded state rule

After upload, current scientific state may record **72 actual paired-frec cells / Hillipop-EDE frontier1360**. The selected next Mathematics task may add at most one **proof-domain** cell `1360→1350`; it must **not** mark cell73/frontier1350. Actual coverage may advance again only after a later separately authorized Builder consumer passes independent validation.

Do not mark Q048 closed, native P6 qualified, physical falsification, accepted-model change, Motor14 route or Q049+ work.

If repo head has moved since `e34e6187e40a56ef790ef0ad2e61f5546b1720b9`, reconcile append-only before updating any mutable CURRENT_STATE/index pointer. Never overwrite historical journals/results.
