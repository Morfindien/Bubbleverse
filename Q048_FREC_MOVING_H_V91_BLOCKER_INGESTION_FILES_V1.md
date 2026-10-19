# Q048 V91 blocker ingestion — filer og recovery upload

V91 V1 remains **BLOCKED_UNEXECUTED**. Actual remains **106/frontier1020** and V90 proof1020→1010 remains accepted. Result Ingestion has prepared a separately versioned **V91R1/V2** Builder route using exact V87 code only as implementation reference.

## Core recovery package

- `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V91_BLOCKER_INGESTED_V1.md` — full append-only journal successor; incoming blocked journal exact suffix.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_RESULT_V1.md` — ingestion/recovery decision.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_STATE_V1.json` — blocker assessment, authority, route and provenance.
- `Q048_FREC_MOVING_H_V91_RECOVERY_NEXT_BUILDER_TASK_V2.json` — new V2/V91R1 Builder task; V1 is not resumed.
- `Q048_FREC_MOVING_H_V91_RECOVERY_HANDOFF_TO_BUILDER_V2.md` — exact Builder handoff.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_HANDOFF_ENVELOPE_V1.json` — machine-readable handoff.
- `Q048_FREC_MOVING_H_V91_RECOVERY_REFERENCE_V87_MAP_V1.json` — exact V87 reference pin map.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_GITHUB_MEMORY_UPDATE_V1.json` — proposed GitHub memory update.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_OUTPUT_MANIFEST_V1.json` — delivered-file integrity manifest.
- `Q048_FREC_MOVING_H_V91_BLOCKER_INGESTION_VALIDATION_V1.json` — detached validation.

## Exact V87 implementation-reference bytes

- `reference_v87/q048_frec_moving_h_v87.py` — SHA256 `52afe960775c6d4f146dbba1a1ba17f02b2f02cab0ecb48df321ea5b172344e8`, 8453 bytes.
- `reference_v87/q048_frec_moving_h_verify_v87.py` — SHA256 `be7a390f91dc6f1bfa07a90e0d4f31d1e731c7e54ae9fc8765b3d44a36fb9972`, 13214 bytes.
- `reference_v87/q048_frec_moving_h_accept_v87.py` — SHA256 `572bd4acfb5166962e126eb2f04483c2c88381e6a6783b4f54d5e5904344f903`, 7219 bytes.
- `reference_v87/q048_v87_consumer_contract.py` — SHA256 `68ae7b054fd472fca8f3fa51c3005c9d87e03e745caf92d354c5971cbce2db8d`, 8624 bytes.
- `reference_v87/q048_v87_import_probe.py` — SHA256 `755d43c04f43679b180e1f05e84e4216353d216089631bcf04362dc24077a1cc`, 2326 bytes.
- `reference_v87/q048_v87_freeze_and_execute.py` — SHA256 `a3f4b4dd7d91f864f1d67a4d7294c60846793f25360b37e2a1b759e4dc66ac50`, 6203 bytes.
- `reference_v87/test_q048_v87_contract.py` — SHA256 `fc9d848c4efc60eff927a0afa930fb5cf76ace860a8fefb5bea0b024d3438ca7`, 2809 bytes.
- `reference_v87/test_q048_v87_import_layout.py` — SHA256 `0dc2a2537de489d4d11649ac19f3acae34921e6a72e992178e0a3b9a6991252f`, 2374 bytes.

These eight files are historical V87 bytes recovered exactly from Library. They are **not** reconstructed V89 source and must never be described as such. Upload them with the Builder handoff so V91R1 can inspect the exact reference bytes.

Repository source freshness VERIFIED at `13c45b5eb4e9d8b896dd64adbce792b1eb4380d2` / `7140500120dd5f07cb4166cdfe4c02bdeac30a94`; V91 blocker package is already present there. Add the new files without overwriting older V91/V90/V89 records. Reconcile if HEAD changes. `GITHUB_SYNC=USER_UPLOAD_PENDING`.
