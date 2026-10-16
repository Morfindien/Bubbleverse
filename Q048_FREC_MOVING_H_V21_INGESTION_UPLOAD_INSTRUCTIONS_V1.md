# Q048 V21 ingestion — manual GitHub apply instructions

Repository: `Morfindien/Bubbleverse`  
Observed base: `main@9da3c6cffbbec4a6793855ef32288b08da407727`  
Status: **USER_UPLOAD_PENDING** — no write was attempted in this ingestion.

## 1. Reconcile the partial V21 origin upload

The latest observed commit contains the decisive V21 complete journal/result/handoff plus raw result, validation, accepted checkpoint, post-accept audit and output manifest. Preserve those uploads unchanged.

If still absent at the current head, add the remaining V21 implementation/provenance files from the delivered V21 package, including the journal append, spec, producer/verifier/accept/postaccept code, candidate checkpoint, run manifest, execution diagnostic and logs. Reconcile by exact hashes; never overwrite historical V20/V19/V12 evidence.

## 2. Add the new V21 ingestion package

Upload these files as new files following current project convention:

- `Q048_FREC_MOVING_H_V21_INGESTION_RESULT_V1.md`
- `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V21_INGESTED_V1.md`
- `Q048_FREC_MOVING_H_V21_INGESTION_STATE_DELTA_V1.json`
- `Q048_FREC_MOVING_H_V21_NEXT_MATHEMATICS_TASK_V1.json`
- `Q048_FREC_MOVING_H_V21_INGESTION_HANDOFF_TO_MATHEMATICS_V1.md`
- `Q048_FREC_MOVING_H_V21_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_FREC_MOVING_H_V21_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_FREC_MOVING_H_V21_INGESTION_UPLOAD_INSTRUCTIONS_V1.md`
- `Q048_FREC_MOVING_H_V21_INGESTION_FILES_V1.md`
- `Q048_FREC_MOVING_H_V21_INGESTION_OUTPUT_MANIFEST_V1.json`

## 3. Guarded state rule

After upload, current scientific state may record **73 actual paired-frec cells / Hillipop-EDE frontier1350**. The selected next Mathematics task may add at most one **proof-domain** cell `1350→1340`; it must **not** mark cell74/frontier1340. Actual coverage may advance again only after a later separately authorized Builder consumer passes independent validation.

Do not mark Q048 closed, native P6 qualified, physical falsification, accepted-model change, Motor14 route or Q049+ work.

If repo head has moved since `9da3c6cffbbec4a6793855ef32288b08da407727`, reconcile append-only before updating any mutable CURRENT_STATE/index pointer. Never overwrite historical journals/results.
