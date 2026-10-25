# Q050 CLEAN V6 — HPC builder delivery

This is a **new implementation stage**, not another V5 preflight.

V5 established that the repository runner stops because no Q050 literal-normal
cell producer exists. CLEAN V6 builds that producer interface against the
existing frozen Q048 runtime and pinned HyRec source.

During implementation, inspection of the actual Q048 helpers exposed a new,
more specific interface obligation: the Q050 normal contains `H'/H`, while the
reusable EDE background helper requires an admitted EDE state/energy enclosure.
The supplied V5 artifacts do not identify a canonical low-z background-binding
artifact for the full 650.2566501559347..810 surface.

Therefore the V6 program is fail-closed and will emit the concrete blocker
`Q050_LOWZ_BACKGROUND_BINDING_MISSING` unless
`Q050_CLEAN_V6_LOWZ_BACKGROUND_BINDING.json` is present and identity-valid.

This is materially different from V5: V5 stopped at "no evaluator"; V6 provides
the executable producer/validator/workflow and identifies the first missing
scientific-runtime interface inside that evaluator.

Generated UTC: 2026-10-25T01:36:20.575535+00:00
