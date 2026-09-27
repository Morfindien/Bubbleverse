# Q042-PROD-V6 — reduced-environment provenance repair

V5 failed at `Q041_REDUCED_PRECISION_META_GATE` during runtime-preflight.

V6 does not relax that gate. It restores the V1 architecture:
- rebuild reduced Planck/ACT support + HiLLiPoP precision from the same frozen Q032 inputs
- stamp the regenerated products with V6 execution identity
- require support hash, precision-array hash, semantics and key order to match V1 parent
- only then run the unchanged 20-cell preflight

All science, seeds, PolyChord settings, 80 reused V1 BOBYQA records, runtime budgets and final classification rules remain unchanged.

START THIS:
Q042-PROD-V6
