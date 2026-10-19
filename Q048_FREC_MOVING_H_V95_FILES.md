# Q048 V95 — individuelle filer

**Actual109/frontier990 accepteret efter én fresh consumer1000→990.** Q048 ACTIVE/INCONCLUSIVE. Ingen below990 eller ny proof.

| Fil | Formål |
|---|---|
| `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V95_APPENDED_V1.md` | Fuld V94-ingested journal som eksakt byte-prefix + én V95 append |
| `Q048_FREC_MOVING_H_V95_RESULT.md` | V95 resultat/status/claim firewall |
| `Q048_FREC_MOVING_H_V95_HANDOFF_TO_INGESTION.md` | Præcis retur til Result Ingestion2.1.0 |
| `q048_frec_moving_h_accepted_checkpoint_v95.json` | Accepteret actual109/frontier990 checkpoint |
| `q048_frec_moving_h_result_v95.json` | Immutable raw PENDING_VALIDATION producerresultat |
| `q048_frec_moving_h_validation_v95.json` | Producer-free verifier 145/145 + 60/60 mutations |
| `q048_frec_moving_h_orchestration_log_v95.json` | Final frozen authority chain |
| `q048_frec_moving_h_postaccept_validation_v95.json` | Postaccept 18/18 |
| `Q048_FREC_MOVING_H_V95_CONTEXT_INDEX.json` | Evidence/hash/code/input index |
| `Q048_FREC_MOVING_H_V95_GATES_PROVENANCE.json` | Scope/gates/provenance |
| `Q048_FREC_MOVING_H_CONSUMER_CONTRACT_V95.md` | Scientific contract written before implementation |
| `q048_v95_preimplementation_spec.json` | Preimplementation spec written before implementation |
| `q048_frec_moving_h_spec_v95.json` | Frozen execution spec |
| `Q048_FREC_MOVING_H_V95_GITHUB_MEMORY_UPDATE.json` | Proposed GitHub memory update; no write |

Staged `inputs/`, `reference_v93/` and `context/` bytes are preserved and hash-pinned in the context index/spec. Uploading files is not scientific dispatch.
