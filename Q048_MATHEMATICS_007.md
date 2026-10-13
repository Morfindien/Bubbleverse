# BUBBLEVERSE — MATHEMATICS ENGINE HANDOFF

STATUS: CONTINUES

Date and time: 2026-10-12T21:39:00+02:00 Europe/Copenhagen

CASE ID: NOT_ASSIGNED

CURRENT Q: Q-048 — PROPOSED_UNVERIFIED

RESULT ID: I-PROPOSED-Q048-MATHEMATICS-007

## QUESTION

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Q047 remains CLOSED INCONCLUSIVE. Q048 remains PROPOSED_UNVERIFIED. This result does not reopen historical-state identity/equivalence.

## MATHEMATICS-ENGINE RESULT

RESULT CLASS: MATHEMATICAL_RESULT; SOURCE_INSPECTION_RESULT; PARTIAL_RESULT; ROUTING_RESULT.

RESULT STATUS: VALID CONDITIONAL PROOF DECOMPOSITION. FINAL_RESULT_GATE remains UNRESOLVED.

The completed Q048-STRUCTURAL-V6 result is preserved unchanged. Its one-sided EDE He1 endpoints at z=4600 are positive w intervals. The four-configuration first cutoff, full x_e(z) difference and cumulative tau_T(z) difference remain NOT_COMPUTED.

### 1. Exact source phase structure after z=4600

Read-only inspection of mwt5345/class_ede at frozen commit 5a131c91d657dd9a7c6364cc45b038710f8d0d97, source/thermodynamics.c, establishes the source-defined approximation sequence and state semantics.

For brec, He1, He1f and He2, the evolved thermodynamic vector contains D_Tmat only. A dynamical x_He component is introduced only when the H approximation begins at z=2870. Therefore He1f 4600->3550 and He2 3550->2870 do not introduce a new helium ODE state. The dynamical continuation variable is the matter-temperature offset, equivalently dimensionless w defined by Tmat=(1-w)T0/a.

At the He1->He1f boundary z=4600, the w/D_Tmat state transition is the identity; the analytic ionization branch changes and must be evaluated on the new side. At the He1f->He2 boundary z=3550, the two HeII->HeI Saha expressions are algebraically identical representations of the same positive root for identical Tmat, z, fHe and nH0.

Define A=exp[(3/2)log(C_NR*Tmat/(1+z)^2)-Tion_HeI/Tmat]/nH0. Then the He2 source uses R=4A, while He1f uses r=1/R. The source expressions are

x_He1f = 2(1+f)/(1-r+sqrt((1-r)^2+4r(1+f)))

and

x_He2 = (sqrt((R-1)^2+4(1+f)R)-(R-1))/2.

Substitution R=1/r gives exact equality for r>0 and f>0. An independent Wolfram symbolic simplification returned exactly 0 for their difference under those assumptions. Thus z=3550 is not a source-real ionization-state discontinuity; it is a representation/approximation switch. This does not by itself qualify native binary64 equivalence or output-table smoothing.

### 2. Correct sign-aware positive-w comparison

For either non-brec phase, the source-real thermal equation can be written on a normalized interval xi in [0,1] as

dw/dxi = c(xi) - d(xi) w,

with c(xi)>0 and d(xi)=c(xi)(1+beta(xi))>0.

Suppose

0 < L <= w(0) <= U,

c_min <= c(xi) <= c_max,

d_min <= d(xi) <= d_max.

Variation of constants gives

w(1) = w(0) exp(-Integral_0^1 d) + Integral_0^1 exp(-Integral_s^1 d) c(s) ds.

Therefore a valid sign-aware enclosure is

L exp(-d_max) + c_min J(d_max) <= w(1)

and

w(1) <= U exp(-d_min) + c_max J(d_min),

where J(d)=(1-exp(-d))/d and J(0)=1 by continuity.

This proves the handoff warning: once L is positive, the lower homogeneous term uses L*exp(-d_max). Reusing L*exp(-d_min) as a lower term would be invalid. The old V6 L<0 independent-control formula must not be mechanically reused.

### 3. Camspec guard reduced to one precise scalar proof obligation

Frozen class_ede background.c applies the guard

V_e/(3 rho_crit) < 1/2

when the scalar field is present. For K=0 and the source variables used by the Q048 proof backend,

3 rho_crit = 3 B(a) + E,

E = X^2/2 + V_e + V_floor,

dE/dln(a) = -3 X^2 <= 0.

Hence the exact guard condition is equivalent to

V_e < 3 B(a) + X^2/2 + V_floor.

The V6 source-root certificate used the deliberately looser implication V_e<=E0-V_floor together with E<=E0. That sufficient bound is proven only to z~3562.590282 for Camspec and therefore cannot certify the fixed z=3550 phase boundary. Its failure beyond that point is a proof limitation, not a demonstrated source crossing.

The finite remedy is now precise: construct a trajectory-correlated validated enclosure for (phi,X) for Camspec using the frozen source ODE and finite-node neutrino realization, and evaluate the guard directly cell by cell. The proof may use the existing rational interval/certificate machinery, but must recompute each guard from the certified whole-state tube. A direct guard certificate is preferred over further global E0-only bounding because the latter intentionally discards the phi-X correlation that makes the current cap loose.

Hillipop does not share this blocker: its existing conservative source-root guard is already certified through z=2870.

### 4. Scope of the next finite computation

The next executable proof must be bounded and must not become a new fit, MCMC, native capture campaign or unchanged V6 replay.

Required order:

A. Preserve every frozen Q048 input, source commit, V5 parent, V6 endpoint and accepted z_reio.

B. For Camspec EDE only, create a validated scalar trajectory/guard certificate sufficient to cover z=4600 -> 2870, or return a precise mathematical obstruction. The source guard must be checked directly on certified whole-state intervals.

C. Continue both EDE w intervals from z=4600 through He1f to z=3550 and He2 to z=2870 using sign-correct interval propagation. The fixed boundary transition for w is identity. At z=3550 independently verify the exact He1f/He2 Saha identity.

D. At z=2870 compute the conditional H-entry helium state q from the source-real Saha map using the certified w interval. Do not substitute captured midpoint hints.

E. Stop and return to RESULT INGESTION & ROUTING. Do not automatically launch the later H/frec/cutoff/full-xe/tau stage in the same step unless a separately documented routing decision authorizes it.

### 5. Scientific status after this mathematics pass

[CALCULATED] The positive-w endpoint comparison formula is fixed and independently reason-checked.

[CALCULATED] The exact-real He1f/He2 Saha transition at z=3550 is algebraically continuous for identical inputs.

[FACT] In the frozen source, D_Tmat is the only evolved thermodynamic state in He1f/He2; dynamical helium evolution begins at the H phase at z=2870.

[UNRESOLVED] Camspec continuous source guard to z=2870.

[UNRESOLVED] Native floating-point/source-instance admission.

[NOT COMPUTED] Shared first q=10^-6 cutoff event.

[NOT COMPUTED] Complete latch-vs-reset x_e(z) difference bounds.

[NOT COMPUTED] Complete cumulative Thomson optical-depth difference bounds.

No physical anomaly, model falsification or Q048 closure is established here.

## SOURCE / TOOL PROVENANCE

K-PROPOSED-Q048-SOURCE-002: mwt5345/class_ede, frozen commit 5a131c91d657dd9a7c6364cc45b038710f8d0d97. Read-only source inspection used source/thermodynamics.c approximation setup, vector initialization, ionization fractions, temperature derivative and output smoothing; source/background.c guard implementation.

K-PROPOSED-Q048-GITHUB-RUN-38293480870 and the supplied V6 worker/final artifacts remain the numerical/provenance basis for the z=4600 endpoint intervals and existing guard horizons.

Wolfram Language was used only as an independent symbolic check of the He1f/He2 algebraic identity. It supplied no physical input.

A separate non-certified floating-point trajectory diagnostic was used only for orientation while assessing the Camspec proof strategy. It is NOT admitted as scientific evidence, supplies no bound, and does not alter any journal value or gate.

## ROUTING

SELECTED NEXT ENGINE: AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.

Reason: the mathematics has reduced the remaining upstream problem to a finite validated interval implementation. No HPC, sampling, likelihood or broad research is indicated. The next engine should first test whether the existing Q047/Q048 rational certificate machinery can implement the direct Camspec guard plus sign-aware thermal continuation without constructing a new general motor. If a tiny extension is required, it must have a new documented PROGRAM_ID/version and preserve all frozen inputs.

SUCCESS CONDITION FOR NEXT ENGINE: finite validated guard+He1f/He2 continuation to z=2870 for both EDE configurations, or a precise scoped obstruction, with independent control and no upgrade of native/source admission claims.

STOP CONDITION: return once that bounded proof result exists. Do not rerun unchanged V6.

## JOURNAL CONTINUITY

This header is prepended to the complete incoming authoritative journal. The incoming journal tail is preserved byte-for-byte.

Incoming journal bytes: 12962468
Incoming journal SHA256: 6f98b0378d48382c253f3dc2b9f781bd34a3c55965695b4356133420b57b6d5c

---

