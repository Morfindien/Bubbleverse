# Q042-PROD-V8 — parent-matrix adoption + PolyChord canary/resume gate

V7 failed before PolyChord fan-out because the regenerated reduced HiLLiPoP
precision matrix did not reproduce V1's restricted_precision_sha256 exactly.

V8 does not weaken that evidence. It stops recomputing the already validated
scientific matrix.

Environment policy:
- download the authoritative V1 environment artifact
- validate V1 support/meta/file/array hashes
- copy the V1 reduced precision matrix byte-for-byte
- restamp only execution provenance for V8
- Q041 runtime gates still validate the active V8 metadata and actual matrix

PolyChord cost-control policy:
- run ONE real canary first: hillipop / ede_n3 / FULL
- fresh canary gets 315 minutes inside a 350-minute job
- if it has no valid resumable checkpoint by then, fail immediately
- if checkpointed, restore it in a separate process and run a 10-minute resume probe
- remaining 19 production cells cannot start until that resume probe passes
- initial 19-cell matrix is fail-fast
- normal resumed segments additionally fail if a 240-minute segment produces no new checkpoint progress

No science changes:
same V1 scientific specification, datasets, 20 cells, seeds, PolyChord settings,
80 reused BOBYQA records, finite budget and final classifier.

START THIS:
Q042-PROD-V8
