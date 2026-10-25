# Q050 — CLEAN V3 JOURNAL APPEND

EVENT_ID: LOCAL-Q050-CLEAN-V3-20261025
RUN_ID: LOCAL-Q050-CLEAN-V3-PION-REDUCTION-20261025
TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
ENGINE: BUBBLEVERSE.MATHEMATICS 2.3.0
LINEAGE: CLEAN_V1 -> CLEAN_V2 -> CLEAN_V3

CLEAN V2's first unresolved gate `Pion=PION_MAX=0.01` was reduced from the pinned HyRec source.

On the surface:
`3*RLya = 99*four_betaB - L2s1s`.
Hence feasibility requires `four_betaB > L2s1s/99`.

At fixed z/background:
`∂Pion/∂xHII = -10^-4*(99-L2s1s/four_betaB)/(1-xHII) < 0`
on every non-degenerate surface point.

Thus the surface is strictly transversal in xHII. The branch-dependent one-sided normal difference reduces exactly to `P_x` times the HMLA-vs-SWIFT hydrogen-field difference at the same surface state.

The remaining decision requires source-real interval execution with frozen rate tables/background over the exact active-SWIFT and feasible-Pion surface, separately q=1e-6 and q=0. Sampling alone is insufficient.

SCIENTIFIC_STATE: INCONCLUSIVE
WORKFLOW_STATE: READY_FOR_HANDOFF
BLOCKER_ID: LOCAL-Q050-CLEAN-V3-PION-SURFACE-NORMAL
NEXT_ENGINE: BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER (verify current compatible version at execution)
RETURN_ENGINE: BUBBLEVERSE.MATHEMATICS 2.3.0

RUN POINTS: 105 pts
TOTAL POINTS: 305 pts
CYCLE PROGRESS: 305/1000 pts
NEXT SOME MILESTONE: 1000 pts
POINTS TO NEXT PUBLICATION: 695 pts
SOME DUE: NONE

Discarded pre-reset Q050 repository material was reference-only and was not imported into clean state.
