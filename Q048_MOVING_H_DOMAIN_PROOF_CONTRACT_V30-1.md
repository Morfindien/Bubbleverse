# Q048 MOVING-H PROOF CONTRACT V30

TASK: `LOCAL-Q048-POST-V29-MOVING-H-DOMAIN-1310-1300-MATH-V1`

Prove and independently validate exactly one connected moving-h proof-domain cell for Hillipop-EDE,
`z=1310→1300`, `a=[1/1311,1/1301]`, starting from the accepted V29 actual checkpoint.

Requirements:
- preserve actual state exactly at 77 accepted paired cells and Hillipop-EDE frontier 1310;
- use V12 committed row14 primary as the scalar track and row14 control only as conservative guard evidence;
- glue the inherited moving lower exactly from the accepted V29 endpoint; never reset it to 1/2;
- recompute a fresh source-faithful K on the new cell and a strictly positive connected whole-cell lower;
- bind both q branches `q_L=10^-6` and `q_R=0` to the same source/C/upper-h/thermal domain;
- use positive ordinary-background Hs LOWER in the negative-rate comparison; `E_safe_left` is only for thermal upper-H/background qualification;
- run a separate producer-free verifier before writing an accepted mathematical checkpoint.

Stop after one validated proof cell, the first exact obstruction, or 300 s of executed science.
No actual consumer, no continuation below 1300, no V29 consumer replay, no V28 proof replay for reassurance,
no V12 guard regeneration, no subdivision/tuning campaign, no native/P6/refit/recapture/HPC/paid run,
no Q049+, and no accepted-model promotion.

A failed sufficient inequality is METHOD_INSUFFICIENT unless independent evidence establishes a physical contradiction.
Return exactly once to Result Ingestion & Routing 2.1.0.
