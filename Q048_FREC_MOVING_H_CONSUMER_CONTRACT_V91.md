# Q048 V91 — fresh actual consumer 1020→1010 preimplementation contract

STATUS: **BLOCKED_BEFORE_IMPLEMENTATION**  
Created UTC: 2026-10-19T09:36:51.119942+00:00  
Local Europe/Copenhagen: 2026-10-19T11:36:51.119942+02:00

## Frozen identity
- CURRENT_Q = TARGET_Q = Q048.
- Task: `LOCAL-Q048-POST-V90-ACTUAL-CONSUMER-1020-1010-V1`.
- Planning fingerprint: `99ea8ea12ee521c24e1c16cb81c038e6ada1282cd40379da4f05527b89806a2b`.
- Builder prompt SHA256: `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`.
- Parent actual authority: **106/frontier1020**, checkpoint SHA256 `96b2b93050581d5b3c82e5023acacb30e9a723008d5067bf88fc3a880a235158`.
- Accepted mathematical authority: V90 proof **1020→1010**, checkpoint SHA256 `4a87612b9adf4da5a75c2df1afe69170e6c492b831a3cfcc1e9dad47a27ad511`.
- Candidate success, only if a future frozen producer/verification/acceptance chain passes: **107/frontier1010**.

## Required behavior
The consumer must reuse and inspect the exact accepted V89 consumer reference implementation pinned by the task before writing V91 execution code. It must stage the exact V90 proof package, bind committed guard row43, validate the root+nested `q047_math_v1.py` layout, freeze distinct V91 code/input/spec/task/execution identity, run at most one producer, use a producer-free verifier rejecting at least 24 meaningful semantic mutations, hash-bind transition/acceptance/postaccept, and stop at the first obstruction or one accepted cell. No proof generation, no below1010, no post-freeze patch/retry, no reset/refit/recapture/tuning/subdivision.

## Preimplementation source-recovery gate
**FAIL / BLOCKER.** The eight exact V89 reference source/test files named in the task are not available in the current container, the current GitHub HEAD, the checked GitHub path histories, or the recent Library listing. Their hashes are preserved, but hashes are not executable source bytes. Historical V89 code must not be reconstructed from manifests, hashes or prose.

Therefore no V91 implementation code may be written and no producer may run in this attempt. Actual authority remains **106/frontier1020**.

## Minimum recovery requirement
Recover the exact bytes of the eight pinned V89 reference files listed in `Q048_FREC_MOVING_H_V91_BLOCKER_STATE.json`, each matching its required SHA-256 and byte length. Once those bytes are supplied, resume from this preimplementation checkpoint; do not repeat V90 Mathematics.
