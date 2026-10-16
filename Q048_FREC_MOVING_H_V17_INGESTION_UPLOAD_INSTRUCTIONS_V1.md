# Q048 V17 ingestion — manual GitHub apply instructions

Repository: `Morfindien/Bubbleverse`  
Verified read base: `main@5d38ea102dd9fb2366c897ecf0424307d314151d`  
Status: **USER_UPLOAD_PENDING** — no write was attempted in this run.

The observed main does **not** contain the V17 Builder result, complete V17 journal or V17 handoff. Therefore first apply the existing V17 Builder package using `Q048_FREC_MOVING_H_V17_UPLOAD_INSTRUCTIONS.md` (or upload V17 and this ingestion package in one coherent commit/PR). Do not treat this ingestion package as a substitute for its origin evidence.

Then add these ingestion files as new root-level files:

- `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V17_INGESTED_V1.md`
- `Q048_FREC_MOVING_H_V17_INGESTION_RESULT_V1.md`
- `Q048_FREC_MOVING_H_V17_INGESTION_STATE_DELTA_V1.json`
- `Q048_FREC_MOVING_H_V17_NEXT_MATHEMATICS_TASK_V1.json`
- `Q048_FREC_MOVING_H_V17_INGESTION_HANDOFF_TO_MATHEMATICS_V1.md`
- `Q048_FREC_MOVING_H_V17_INGESTION_HANDOFF_ENVELOPE_V1.json`
- `Q048_FREC_MOVING_H_V17_INGESTION_GITHUB_MEMORY_UPDATE_V1.json`
- `Q048_FREC_MOVING_H_V17_INGESTION_UPLOAD_INSTRUCTIONS_V1.md`
- `Q048_FREC_MOVING_H_V17_INGESTION_FILES_V1.md`
- `Q048_FREC_MOVING_H_V17_INGESTION_OUTPUT_MANIFEST_V1.json`

Do not overwrite V15/V16/V17 historical raw evidence or earlier journal versions. This complete journal is a **new version** whose prefix is the exact supplied V17-appended journal.

Before changing any mutable CURRENT_STATE/index pointer, re-read current main and reconcile any commits after `5d38ea102dd9fb2366c897ecf0424307d314151d`. Only after the origin V17 files and this ingestion package are present coherently may a current pointer state **actual71/frontier1370** and route the next task to Mathematics. Uploading files is not scientific dispatch.

Next scientific action after upload: run `BUBBLEVERSE.MATHEMATICS 2.1.0` with `Q048_FREC_MOVING_H_V17_NEXT_MATHEMATICS_TASK_V1.json` and the complete ingested journal. Do not count a 1370→1360 proof or cell72 until that future run actually validates it.
