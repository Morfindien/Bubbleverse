# Q042-PROD-V5 — static lineage-test repair

Observed Q042-PROD-V4 failure:

- `Q042_PROD_V4_STATIC_GATE=PASS`
- `q042_production_tests_v4.py` then failed at `REGISTRY_PARENT`.
- The V4 registry entry correctly had `technical_parent_program_id = Q042-PROD-V3`.
- The V4 test incorrectly required `Q042-PROD-V1`.

This mixed two different provenance layers:

1. Frozen scientific/runtime provenance parent: `Q042-PROD-V1`
2. Immediate deployment/version parent: the previous recovery version

V5 fixes only that static lineage assertion and strengthens tests so both relations
are checked separately.

No science changes:
- byte-identical V1 scientific spec
- same datasets and likelihood locks
- same 20 cells and 20 PolyChord seeds
- same PolyChord settings
- same 80 V1 BOBYQA records and zero optimizer recomputation
- same finite runtime policy
- same frozen scientific classifier

V3 NumPy/PyYAML import fix and V4 version-integrity fix are preserved.

The full GitHub static command was executed locally against the real V1
`q042_production_spec_v1.json` and `q042_production_source_lock_v1.json`
before delivery.

Manual install only. The assistant did not upload, commit, rerun or dispatch.

START THIS:
Q042-PROD-V5
