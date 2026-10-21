# Q048 V141 implementation plan

- Task: one fresh conditional source-real connected proof cell 840→830; +1 proof, +0 actual.
- Parent: V140 accepted checkpoint SHA `2ee7bd4496a7a4d0cc923417fa65372626b921ea79e0dade055b817564ce8201`; current actual124/frontier840 remains unchanged throughout Mathematics.
- Guard: unique row61 for control=false is primary; control=true is comparison only. E_input_left is the conservative whole-cell cap; E_safe_left stays distinct.
- Method: V138 code is read-only reference. V141 producer/verifier/runner are separately versioned and never execute a historical main.
- Proof topology: fresh source/background/atomic/C enclosure, new K_upper and connected lower h bound, strict upper-h and thermal inward faces, conditional first-exit/closed-endpoint continuation for existing admissible AC solutions, convex HMLA/SWIFT inclusion for fixed q branches.
- Validation: 30 producer gates, 42 independent verifier checks, 42 frozen real semantic mutations, serialized acceptance + readback.
- Compute backend: LOCAL_RUNTIME. GitHub Actions not worthwhile; V138 same-class chain measured 3.145258567s and V141 has one adjacent cell / one chain / 300 s cap.
- Retry/postfreeze policy: 0 retries; no post-freeze edits. First obstruction is terminal.
- Forbidden: actual125, any below-z830 work, theorem consumption, native integration, selector existence/uniqueness claim, trajectory identity, Q closure or model promotion.
