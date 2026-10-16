# Q048 — Matematikmotor 2.1.0 V16: moving-h domain 1380→1370

UTC producer start `2026-10-16T04:39:33.295412+00:00`. Package prepared 2026-10-16 around 04:40Z / 06:40 Europe/Copenhagen.

## Identity and frozen boundary

- TARGET_Q: Q048 only; no Q049+ scientific input.
- TASK_ID: `LOCAL-Q048-POST-V15-MOVING-H-DOMAIN-1380-1370-MATH-V1`.
- RESULT_ID: `LOCAL-Q048-POST-V15-MOVING-H-DOMAIN-V16`.
- Question SHA256: `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`.
- Source commit: `5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
- Capture SHA256: `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`.
- Parent actual checkpoint: V15, SHA256 `be854ef0d1b6fe5435c1066c3b659c519804c7f95331d1b46667c5306cc7c57c`; inherited actual count **70**, Hillipop-EDE frontier **1380**.
- V12 primary/control row7 on a=[1/1381,1/1371] are accepted+committed and strictly positive.

## Direct mathematical output

[BEREGNET/INFERRED, conditional source-real] **PASS_NEW_MOVING_H_DOMAIN_PROOF_CELL** for Hillipop-EDE `1380→1370`, a=[1/1381,1/1371]. This is one new mathematical proof-domain cell, not an actual paired-frec cell.

The V15 certified parent lower projection is reused as the comparison boundary condition, not as a physical reset: `h0=10535292182867437/500000000000000000` ≈ 0.021070584365734873. The old V14 cell K is not reused. Recomputing the rate bound on the new row7 domain gives

`K_upper=6216964748839156953643/1000000000000000000` ≈ 6216.964748839156528.

The common-epsilon comparison remains `ell_u=-K ell(ell+epsilon)` with epsilon=10^-6 and q<=epsilon. Primary interval arithmetic gives endpoint lower ≈ 0.010793969614902249. The independent exact-rational control using `log(r)<=r-1` and `exp(x)<=1/(1-x)` gives endpoint lower `1444323060731006005110919975173890576777009/134047540119607589080024826109423222991000000` ≈ 0.010774707685364978. The conservative whole-cell lower is therefore

`h_min=10774707685364977/1000000000000000000` = 0.010774707685364976.

Both q branches pass the new whole-cell source/C/upper-h/thermal obligations. L upper-h lower bounds are ≈1.3174352538e-13 and 3.1031559928e-13; R lower bounds ≈1.3174339363e-13 and 3.1031528895e-13, all strictly positive. Thermal beta lower is ≈4744.1144 (L) and ≈4743.6764 (R); both thermal faces and denominators are strictly admitted. Source domains TR/Tgamma/ratio/fit/H and atomic/C positivity pass.

## Validation

Separate producer-free verifier: **43/43 checks PASS; 12/12 deliberate mutations rejected**. The verifier recomputes K and the limiting control lower with exact `Fraction` arithmetic and does not import or execute the producer or Bubbleverse interval modules. The primary exponential path is non-limiting because the exact-rational control is smaller and sets h_min. Producer wall time 0.575544s; verifier 0.072505s; local Python only, no HPC/native/paid run.

## Three interpretation layers

DIRECT: one validated math proof cell exists on 1380→1370.

TECHNICAL: the V14 Riccati theorem is composably extended by a newly qualified row7 K/source/rate/thermal domain, glued from V15's certified endpoint projection. Technical state PASS within this bounded domain.

PHYSICAL: no new observation, no measured h/xe trajectory, no physical reset, no native-P6 qualification, no Delta x_e(z) or Delta tau_T(z) final bounds, no falsification and no accepted-model change. Q048 remains ACTIVE/INCONCLUSIVE.

## State delta and stop

ADDS: one validated mathematical proof-domain cell 1380→1370.
CONFIRMS: V15 actual state remains 70 cells/frontier1380.
LEAVES UNCHANGED: all earlier actual cells, other three frontiers1440, historical failures, Q047 CLOSED INCONCLUSIVE, source/capture/z_reio and accepted model.

STOP: no actual consumer was run; no continuation below1370; no subdivision/tuning/method campaign/refit/recapture/likelihood/native/HPC/paid run. Return exactly once to **Result Ingestion & Routing Engine 2.1.0**.
