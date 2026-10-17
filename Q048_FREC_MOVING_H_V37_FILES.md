# Q048 V37 — alle filer

V37 Builder-kørsel: actual80→81, frontier1280→1270. Full Q048 remains ACTIVE/INCONCLUSIVE. GitHub sync USER_UPLOAD_PENDING.

## Leverancer
- [Q048_FREC_MOVING_H_V37_RESULT.md](sandbox:/mnt/data/q048_v37/Q048_FREC_MOVING_H_V37_RESULT.md) — human-readable Builder result
- [Q047_SAMLET_JOURNAL_FREC_MOVING_H_V37_APPENDED_V1.md](sandbox:/mnt/data/q048_v37/Q047_SAMLET_JOURNAL_FREC_MOVING_H_V37_APPENDED_V1.md) — full append-only journal successor with unchanged V36-ingested journal suffix
- [Q048_FREC_MOVING_H_V37_HANDOFF_TO_INGESTION.md](sandbox:/mnt/data/q048_v37/Q048_FREC_MOVING_H_V37_HANDOFF_TO_INGESTION.md) — handoff to Result Ingestion & Routing 2.1.0
- [Q048_FREC_MOVING_H_V37_JOURNAL_APPEND.md](sandbox:/mnt/data/q048_v37/Q048_FREC_MOVING_H_V37_JOURNAL_APPEND.md) — new V37 journal record only
- [Q048_FREC_MOVING_H_V37_UPLOAD_INSTRUCTIONS.md](sandbox:/mnt/data/q048_v37/Q048_FREC_MOVING_H_V37_UPLOAD_INSTRUCTIONS.md) — manual GitHub upload/memory instructions
- [q048_frec_moving_h_spec_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_spec_v37.json) — frozen V37 consumer specification and pins
- [q048_frec_moving_h_result_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_result_v37.json) — raw producer result, PENDING_VALIDATION preserved
- [q048_frec_moving_h_candidate_checkpoint_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_candidate_checkpoint_v37.json) — candidate actual checkpoint, PENDING_VALIDATION preserved
- [q048_frec_moving_h_validation_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_validation_v37.json) — producer-free verifier result and 20 mutation outcomes
- [q048_frec_moving_h_transition_validation_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_transition_validation_v37.json) — six transition tests
- [q048_frec_moving_h_accepted_checkpoint_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_accepted_checkpoint_v37.json) — accepted VALIDATED actual81/frontier1270 checkpoint
- [q048_frec_moving_h_postaccept_validation_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_postaccept_validation_v37.json) — 12 postaccept checks
- [q048_frec_moving_h_input_refs_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_input_refs_v37.json) — input provenance and accepted historical pins
- [q048_frec_moving_h_backend_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_backend_v37.json) — estimate-driven compute backend decision
- [q048_frec_moving_h_preflight_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_preflight_v37.json) — preflight and syntax gate
- [q048_frec_moving_h_run_manifest_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_run_manifest_v37.json) — run identity, invocations, environment and code hashes
- [q048_frec_moving_h_execution_summary_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_execution_summary_v37.json) — execution and validation summary
- [q048_frec_moving_h_state_delta_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_state_delta_v37.json) — minimal proposed active-state delta for ingestion
- [q048_frec_moving_h_delivery_validation_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_delivery_validation_v37.json) — delivery coherence validation
- [q048_frec_moving_h_v37.py](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_v37.py) — V37 actual-cell producer/consumer
- [q048_frec_moving_h_verify_v37.py](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_verify_v37.py) — separate producer-free V37 verifier
- [test_q048_v37_transition.py](sandbox:/mnt/data/q048_v37/test_q048_v37_transition.py) — meaningful transition test suite
- [q048_frec_moving_h_accept_v37.py](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_accept_v37.py) — guarded acceptance helper
- [q048_frec_moving_h_postaccept_v37.py](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_postaccept_v37.py) — postaccept validator
- [validate_q048_v37_delivery.py](sandbox:/mnt/data/q048_v37/validate_q048_v37_delivery.py) — delivery validator
- [q048_frec_moving_h_execution_v37.log](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_execution_v37.log) — producer execution log
- [q048_frec_moving_h_verification_v37.log](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_verification_v37.log) — verifier + explicit mutation failure log
- [q048_v37_transition_suite.log](sandbox:/mnt/data/q048_v37/q048_v37_transition_suite.log) — transition test log
- [q048_frec_moving_h_acceptance_v37.log](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_acceptance_v37.log) — acceptance log
- [producer_time.txt](sandbox:/mnt/data/q048_v37/producer_time.txt) — producer wall-time record
- [verifier_time.txt](sandbox:/mnt/data/q048_v37/verifier_time.txt) — verifier wall-time record
- [q048_frec_moving_h_output_manifest_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_output_manifest_v37.json) — SHA256 manifest of V37 delivered files (self excluded)
- [q048_frec_moving_h_manifest_validation_v37.json](sandbox:/mnt/data/q048_v37/q048_frec_moving_h_manifest_validation_v37.json) — post-manifest hash validation (manifest intentionally excludes this file)
- [validate_q048_v37_manifest.py](sandbox:/mnt/data/q048_v37/validate_q048_v37_manifest.py) — manifest validator
- [Q048_FREC_MOVING_H_V37_FILES.md](sandbox:/mnt/data/q048_v37/Q048_FREC_MOVING_H_V37_FILES.md) — this file index
