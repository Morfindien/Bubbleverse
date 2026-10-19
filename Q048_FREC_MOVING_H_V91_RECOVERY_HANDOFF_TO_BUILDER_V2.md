# Q048 V91 blocker ingestion → Builder2.2.0 recovery configuration V2

STATUS: CONTINUES. CASE LIFECYCLE: ACTIVE. EPISTEMIC STATUS: INCONCLUSIVE.  
HANDOFF_ID: LOCAL-Q048-V91-BLOCKER-RECOVERY-V1-TO-BUILDER; UTC 2026-10-19T09:52:41.433875+00:00; lokal 2026-10-19T11:52:41.434773+02:00. PREPARED_NOT_SENT.  
CURRENT_Q=TARGET_Q=Q048; actual authority **106/frontier1020**.

## Exact task

Implement `LOCAL-Q048-POST-V91-BLOCKER-RECOVERY-ACTUAL-CONSUMER-1020-1010-V2` from `Q048_FREC_MOVING_H_V91_RECOVERY_NEXT_BUILDER_TASK_V2.json`; planning fingerprint `254cb9f9bcbd334215b33f112005901c6d7d01751022cb41bb0fa53b8e0b37fb`. Use a **new V91R1 revision identity**. The previous V1 task remains preserved as BLOCKED_UNEXECUTED and must not be resumed under its old fingerprint.

## Frozen science

Use parent accepted V89 checkpoint SHA256 `96b2b93050581d5b3c82e5023acacb30e9a723008d5067bf88fc3a880a235158` and accepted V90 proof checkpoint SHA256 `4a87612b9adf4da5a75c2df1afe69170e6c492b831a3cfcc1e9dad47a27ad511` for cell **1020→1010**. Primary row43 and all scientific values/criteria are unchanged from the blocked task. Candidate success remains only **107/frontier1010**, endpoint a=1/1011,E=11800560411137753481/200000000000000000,Y=23486715015949958209/500000000000000000,Vbar=11528148189464315529/1000000000000000000, connected lower=273780565158891/500000000000000000.

## Material configuration change

Do **not** require or reconstruct unavailable V89 source code. Instead inspect the eight exact V87 files delivered under `reference_v87/`; every byte/hash is pinned by `Q048_FREC_MOVING_H_V91_RECOVERY_REFERENCE_V87_MAP_V1.json`. These are implementation references only, not evidence that V87/V89/V91 trajectories are identical. Build fresh V91R1 code and independently validate current task semantics.

Mandatory prefreeze behavior: new V91R1 contract/spec before implementation; exact V87 reference hash checks; exact V90 proof artifact checks; exact V89 parent checkpoint check; committed row43 binding; root+nested q047_math_v1.py hash/layout; transitive import with zero science/output; finite tests; producer-free verifier rejecting >=24 meaningful semantic mutations. Freeze separate V91R1 code/input/spec/contract/task/execution identity before at most one producer.

Stop on first obstruction, one accepted actual cell, or 300 science seconds. No new proof, below1010, reset/refit/recapture/tuning/subdivision, postfreeze patch/retry, automatic later task, new Q, model promotion or Q closure. Return exactly once to Result Ingestion2.1.0.

Repository basis VERIFIED at `13c45b5eb4e9d8b896dd64adbce792b1eb4380d2` / `7140500120dd5f07cb4166cdfe4c02bdeac30a94`. New recovery package USER_UPLOAD_PENDING; no repository write/dispatch occurred here.
