# Q048 V20 ingestion — manual GitHub apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `main@ba986110e8fadb6ecfcd5581e61e5b43e102c61a`  
Status: **USER_UPLOAD_PENDING** — no write was attempted in this ingestion.

## 1. Reconcile the partial V20 origin upload

The latest observed commit includes the decisive V20 raw result, validation and accepted checkpoint. It also stores four content-equivalent journal/index/result files under `-1` suffixed names rather than the unsuffixed local canonical names. Preserve those historical uploads; do not overwrite or rename them destructively. Reconcile by hash/cross-reference.

The following V20 support/provenance files were not present in the latest observed commit and should be uploaded if not already added by a later head:

- `Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V20.md`
- `q048_moving_h_domain_candidate_checkpoint_v20.json`
- `q048_moving_h_domain_evidence_manifest_v20.json`
- `q048_moving_h_domain_execution_diagnostic_v20.json`
- `q048_moving_h_domain_execution_v20.log`
- `q048_moving_h_domain_run_manifest_v20.json`
- `q048_moving_h_domain_spec_v20.json`
- `q048_moving_h_domain_v20.py`
- `q048_moving_h_domain_validation_v20.log`
- `q048_moving_h_domain_verify_v20.py`


## 2. Add the new V20 ingestion package

Upload these files as new files following current project convention:

- `Q048_MOVING_H_DOMAIN_V20_INGESTION_RESULT_V1.md`
- `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V20_INGESTED_V1.md`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_STATE_DELTA_V1.json`
- `Q048_MOVING_H_DOMAIN_V20_NEXT_BUILDER_TASK_V1.json`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_HANDOFF_TO_BUILDER_V1.md`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_UPLOAD_INSTRUCTIONS_V1.md`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_FILES_V1.md`
- `Q048_MOVING_H_DOMAIN_V20_INGESTION_OUTPUT_MANIFEST_V1.json`


## 3. Guarded state rule

After upload, current scientific state may record one accepted **mathematical proof-domain cell 1360→1350** while actual paired-frec state remains **72/frontier1360**. Do **not** mark cell73/frontier1350 until the separate Builder actual-consumer task `LOCAL-Q048-POST-V20-MOVING-H-ACTUAL-CONSUMER-ONE-CELL-V1` passes independent validation.

The selected next scientific engine is **BUBBLEVERSE.EXECUTION_HPC_BUILDER 2.2.0**. Uploading files is not scientific dispatch. Do not mark Q048 closed, native P6 qualified, physical falsification, accepted-model change, Motor14 route or Q049+ work.

If repository head has moved since `ba986110e8fadb6ecfcd5581e61e5b43e102c61a`, reconcile append-only before changing any mutable CURRENT_STATE/index pointer. Never overwrite historical journals/results.
