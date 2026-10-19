# Q048 V90 — filer og manuel upload

**Accepted proof1020→1010; actual remains106/frontier1020.** Next engine is Result Ingestion2.1.0. Handoff PREPARED_NOT_SENT.

| Fil | Rolle |
|---|---|
| `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V90_APPENDED_V1.md` | Fuld append-only journal; incoming V89 ingested journal preserved byteidentically as suffix |
| `Q048_MOVING_H_DOMAIN_V90_RESULT.md` | Primært human-readable Mathematics result |
| `Q048_MOVING_H_DOMAIN_V90_HANDOFF_TO_INGESTION.md` | Én route tilbage til Result Ingestion2.1.0 |
| `Q048_MOVING_H_DOMAIN_V90_INPUT_MAP.md` | Frozen input hashes/layout og provenance-only parent hashes |
| `Q048_MOVING_H_DOMAIN_V90_GATES_PROVENANCE.json` | Machine-readable proof/gate provenance |
| `Q048_MOVING_H_DOMAIN_V90_GITHUB_MEMORY_UPDATE.json` | Manual GitHub-memory update proposal |
| `Q048_MOVING_H_DOMAIN_PROOF_CONTRACT_V90.md` | Preimplementation scientific contract |
| `Q048_MOVING_H_DOMAIN_PREIMPLEMENTATION_SPEC_V90.json` | Machine preimplementation spec created before code |
| `q048_moving_h_domain_spec_v90.json` | Frozen execution spec |
| `q048_v90_proof_contract.py` | V90 strict metadata/provenance contract |
| `q048_moving_h_domain_v90.py` | Fresh V90 one-cell mathematical producer |
| `q048_moving_h_domain_verify_v90.py` | Producer-free V90 verifier |
| `q048_moving_h_domain_accept_v90.py` | Hash-bound V90 acceptor |
| `q048_v90_import_probe.py` | Actual transitive import preflight |
| `q048_v90_freeze_and_execute.py` | One immutable frozen execution launcher |
| `test_q048_moving_h_v90.py` | Finite toy/metadata tests |
| `test_q048_v90_layout.py` | Nested import-layout mutation tests |
| `q048_moving_h_domain_preflight_v90.json` | Frozen metadata/test/import preflight |
| `q048_moving_h_domain_freeze_v90.json` | Frozen identity record |
| `q048_moving_h_domain_execution_v90.json` | Ordered execution record |
| `q048_moving_h_domain_producer_invocation_v90.json` | Producer invocation record |
| `q048_moving_h_domain_verifier_invocation_v90.json` | Verifier invocation record |
| `q048_moving_h_domain_result_v90.json` | Producer raw result |
| `q048_moving_h_domain_candidate_checkpoint_v90.json` | Pending candidate checkpoint before validation |
| `q048_moving_h_domain_verifier_recomputation_v90.json` | Independent verifier recomputation |
| `q048_moving_h_domain_validation_v90.json` | Producer-free validation |
| `q048_moving_h_domain_transition_validation_v90.json` | Hash-bound transition validation |
| `q048_moving_h_domain_accepted_checkpoint_v90.json` | Accepted mathematical proof authority |
| `q048_moving_h_domain_acceptance_validation_v90.json` | Acceptance record |
| `q048_moving_h_domain_postaccept_validation_v90.json` | Detached postaccept checks |

Two additional final files are `Q048_MOVING_H_DOMAIN_V90_OUTPUT_MANIFEST.json` and `Q048_MOVING_H_DOMAIN_V90_DELIVERY_VALIDATION.json` (created after this index to avoid circular hashes).

Upload new V90 files to the existing Bubbleverse repository/root without overwriting V89 or older records. Reconcile repository HEAD first; V89 ingestion recorded its own bundle as USER_UPLOAD_PENDING. `GITHUB_SYNC=USER_UPLOAD_PENDING`. No archive is required.

For the next chat/engine, the minimal operator handoff set is the full journal, `Q048_MOVING_H_DOMAIN_V90_RESULT.md`, this file index and `Q048_MOVING_H_DOMAIN_V90_HANDOFF_TO_INGESTION.md`, together with the existing Result Ingestion2.1.0 engine prompt. Machine artifacts remain individually available for verification.
