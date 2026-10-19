# Q048 V90 ingestion — filer og manuel upload

Actual er **106/frontier1020**. V90 proof1020→1010 er indlæst; V91 actual-consumer1020→1010 er kun planlagt. Next engine: Execution/HPC Builder2.2.0. Handoff PREPARED_NOT_SENT.

| Fil | Rolle |
|---|---|
| `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V90_INGESTED_V1.md` | Fuld kumulativ journal; incoming V90 journal preserved byteidentically as suffix |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_RESULT_V1.md` | Primært ingestion/result-routing resultat |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_STATE_V1.json` | Actual/evidence/task/route state og provenance |
| `Q048_MOVING_H_DOMAIN_V90_NEXT_BUILDER_TASK_V1.json` | Én planlagt, ikke kørt Builder consumer1020→1010 |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_HANDOFF_TO_BUILDER_V1.md` | Handoff til Execution/HPC Builder2.2.0 |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_HANDOFF_ENVELOPE_V1.json` | Fallback2.1.0 machine-readable envelope |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_GITHUB_MEMORY_UPDATE_V1.json` | GitHub-memory uploadforslag |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_FILES_V1.md` | Dette indeks og uploadvejledning |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_OUTPUT_MANIFEST_V1.json` | Final integrity/repository manifest |
| `Q048_MOVING_H_DOMAIN_V90_INGESTION_VALIDATION_V1.json` | Detached contract/delivery validation |

Repository source freshness is VERIFIED at Morfindien/Bubbleverse@`b103127165b881219f8f8c1721dd5ebb89438be9` / tree `3106ee6fed960c1310b54074c73b801a2be28f9a`. Seven primary V90 files match local Git blobs. V90 repository sync is PARTIAL; exact local machine artifacts remain available and must not be reconstructed.

Upload the 10 new ingestion files to the existing repository root without overwriting V90 or older records. Reconcile if HEAD changes. `GITHUB_SYNC=USER_UPLOAD_PENDING`.

For the next Builder chat, minimum handoff is the full ingested journal, ingestion result, handoff, task JSON and this file index plus existing Builder2.2.0 prompt. The Builder must also use the exact V90 accepted proof package (`q048_moving_h_domain_accepted_checkpoint_v90.json` plus the hash-bound proof artifacts) already delivered in this workflow. It must keep actual106/frontier1020 until a single consumer is accepted and attempt at most one fresh consumer1020→1010.
