# Q050 — CLEAN V2 JOURNAL APPEND

EVENT_ID: LOCAL-Q050-CLEAN-V2-20261025
RUN_ID: LOCAL-Q050-CLEAN-V2-PEEBLES-NORMAL-20261025
TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
ENGINE: BUBBLEVERSE.MATHEMATICS 2.3.0
LINEAGE: CLEAN_V1 -> CLEAN_V2

CLEAN V1's first unresolved gate at `Tmat/Trad=0.1` was re-analysed from the frozen CLASS/HyRec source.

For the frozen configuration, the late temperature field gives
`dv/dz=[v+(rate_gamma_b/H)(v-1)]/(1+z)`.
At `v=0.1`, the normal is
`[0.1-0.9(rate_gamma_b/H)]/(1+z)`.

At a common state this temperature normal is identical whether the hydrogen derivative is routed to PEEBLES or the non-PEEBLES branch. Therefore the PEEBLES ratio selector does not create opposing one-sided normal fields at its own switching surface. Equality remains source-real PEEBLES (`<=`). A possible tangent at `rate_gamma_b/H=1/9` does not by itself require a Filippov/convexified normal.

RESULT: CLEAN V1 PEEBLES-ratio normal gate CLEARED AS FIRST OBSTRUCTION.
Q050 remains ACTIVE / INCONCLUSIVE.

FIRST REMAINING GATE:
`Pion=PION_MAX=0.01`, where the hydrogen component itself changes HMLA/SWIFT routing and the full source-faithful surface normal is not yet certified.

RUN POINTS: 90 pts
TOTAL POINTS: 200 pts
CYCLE PROGRESS: 200/1000 pts
NEXT SOME MILESTONE: 1000 pts
POINTS TO NEXT PUBLICATION: 800 pts
SOME DUE: NONE

NEXT: Pion-surface one-sided normal/crossing certificate; then SWIFT-fit lower-grid interface if needed.
