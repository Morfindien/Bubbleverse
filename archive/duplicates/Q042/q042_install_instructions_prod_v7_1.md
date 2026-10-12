# Q042-PROD-V7 — canary checkpoint/resume gate

V6 proved PolyChord starts, but 240-minute fresh segments can still be inside initial live-point generation. At pinned PolyChordLite commit 3ade6445..., fresh-run resume state is written only after GenerateLivePoints returns.

V7 runs one real high-cost canary first (HiLLiPoP/EDE/FULL) for up to 330 minutes. If it cannot complete or create a valid checkpoint, the remaining 19 cells never start. If checkpointed, V7 restores it in a separate job and resumes for 5 minutes before releasing the remaining 19 cells. The canary work is real Q42 science work, not discarded smoke compute.

Science settings, seeds, 80 reused BOBYQA records and classifier are unchanged.

START THIS:
Q042-PROD-V7

Production continuation safety: every timed resume segment must persist a changed resume-file SHA-256 before another continuation is dispatched. The 5-minute canary resume probe is disposable and the real canary continuation restarts from the untouched s0 artifact.
