# Q048 V18 ingestion — manual GitHub apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `main@9e498167c2e59ad3cf76d9ba174800aa12bd44da`  
Status: **USER_UPLOAD_PENDING** — no write was attempted in this ingestion.

## 1. Complete the partial V18 origin upload

The latest observed commit contains 10 expected V18 origin paths but the following 9 are still absent at the repository root:

- `Q048_MOVING_H_DOMAIN_V18_RESULT.md`
- `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V18_APPENDED_V1.md`
- `Q048_MOVING_H_DOMAIN_V18_JOURNAL_APPEND.md`
- `q048_moving_h_domain_result_v18.json`
- `q048_moving_h_domain_candidate_checkpoint_v18.json`
- `q048_moving_h_domain_execution_v18.log`
- `q048_moving_h_domain_validation_v18.log`
- `Q048_MOVING_H_DOMAIN_V18_GITHUB_MEMORY_UPDATE.json`
- `Q048_MOVING_H_DOMAIN_V18_FILES.md`

At minimum, do not omit the raw result `q048_moving_h_domain_result_v18.json` (SHA256 `fcbe51cee49799c2126806a8e25776861ad1ff16cde7b6b93651a8930e522e64`) or the complete V18 journal (SHA256 `b3c975646fe7f71780a9afefd48ca61e1d9db2e3262566ec66361957906b5ba1`). Preserve all already-uploaded V18 files unchanged.

## 2. Add the new V18 ingestion package

Upload these files to repository root following the current project convention:

- `Q048_MOVING_H_DOMAIN_V18_INGESTION_RESULT_V1.md`
- `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V18_INGESTED_V1.md`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_STATE_DELTA_V1.json`
- `Q048_MOVING_H_DOMAIN_V18_NEXT_BUILDER_TASK_V1.json`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_HANDOFF_TO_BUILDER_V1.md`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_UPLOAD_INSTRUCTIONS_V1.md`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_FILES_V1.md`
- `Q048_MOVING_H_DOMAIN_V18_INGESTION_OUTPUT_MANIFEST_V1.json`

## 3. Guarded state rule

After upload, current scientific state may record one accepted **mathematical proof cell 1370→1360** while actual state remains **71/frontier1370**. Do **not** mark cell72/frontier1360 until the separate Builder actual-consumer task passes independent validation. Do not mark Q048 closed, native P6 qualified, or accepted model changed.

The selected next scientific task is `LOCAL-Q048-POST-V18-MOVING-H-ACTUAL-CONSUMER-ONE-CELL-V1` for `BUBBLEVERSE.EXECUTION_HPC_BUILDER 2.2.0`. Uploading files is not scientific dispatch.

If repo head has moved since `9e498167c2e59ad3cf76d9ba174800aa12bd44da`, reconcile append-only before updating any mutable CURRENT_STATE/index pointer. Never overwrite prior journal/result history.
