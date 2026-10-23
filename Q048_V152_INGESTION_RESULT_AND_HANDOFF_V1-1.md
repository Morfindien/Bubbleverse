# Q048 V152 — terminal technical failure ingested once

V152 is now registered exactly once as a **technical execution failure**, not a scientific negative result. GitHub commit `642d81b730bcf825bb542d5a713fcdc2737490fd` contains the V152 ledger, terminal-failure record, machine-readable state and full journal path. The existing V152 **52-point** source charge is already finalized in Ledger V17 and is **not billed again**.

Current accepted state remains **actual127/frontier810**; the other three frontiers remain 1440/1440/1440. V150 proof820→810 remains **ACCEPTED_CONSUMED_ONCE**. V152 established **no** new proof cell and produced no RAW/verifier/acceptance/readback. Q048 remains **ACTIVE / INCONCLUSIVE**; NativeP6 and the complete four-case x_e(z)/tau_T(z) bounds remain unresolved.

## What failed

The frozen V152 runtime had the correct `q047_math_v1.py` bytes at `.../inputs/q047_math_v1.py`, but the pinned kernel dynamically required `.../inputs/source/q047_math_v1.py`. Producer import therefore failed before theorem arithmetic. This is a path-binding/configuration defect, not evidence against the mathematics or physics.

## Exact next route

The single next engine is **BUBBLEVERSE.MATHEMATICS2.2.0** with `Q048_V153_NEXT_MATHEMATICS_TASK_REPAIR_810_800_V1.json` (fingerprint `6247478ac387030b22bf9f537b4aa24d7a3ecf4c695e5f1e767c5e055d30217d`). This same-engine route is allowed because V152 did not complete the proof and exposed a specific new failure mode. V153 must restore/hash-verify the transitive `source/q047_math_v1.py` path and pass a no-science import-closure smoke test **before freeze**, then run one fresh810→800 proof chain.

No V153 dispatch has occurred. Estimate **54 pts**, maximum **65 pts**, not reserved or charged.

RUN COST: 26 pts
USED: 736/1000 pts
REMAINING: 264 pts

Budget `LOCAL-Q048-SHARED-1000PT-BUDGET-V1`, ledger V17→V18. New unique ingestion charge `LOCAL-Q048-BUDGET-CHARGE-V152-INGESTION-V1`. Cost: state/input recovery4 + routing/materiality5 + computation/hash1 + repository reconciliation4 + integrity validation5 + journal/ledger/handoff delivery7 =26pts. Reservation32 finalized,6 released; no outstanding reservation or overrun.

## Persistence

The incoming V152 state is verified on GitHub. New V152-ingestion/V153-handoff files are prepared as new versioned artifacts and historical V152 files remain unchanged. Because the complete continued journal is ~15 MB and coherent multi-file atomic writeback is not available through the current connector path, this new bundle is marked **USER_UPLOAD_PENDING** rather than partially pretending synchronization.
