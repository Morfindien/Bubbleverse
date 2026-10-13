# BUBBLEVERSE — OVERLEVERING

STATUS:
FORTSÆTTER

VALGT NÆSTE MOTOR:
AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE

Date and time:
2026-10-13T07:45:22+02:00 Europe/Copenhagen

CASE ID:
NOT_ASSIGNED

CURRENT Q:
Q-048 — PROPOSED_UNVERIFIED

QUESTION:
For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Question SHA256:
c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436

Q047 remains CLOSED INCONCLUSIVE. This mathematics pass does not reopen historical-state identity/equivalence.

---

## CHATGPT-SETUPVURDERING FOR NÆSTE TRIN

ANBEFALET PRIMÆRT SETUP:
Current GPT-5.6 Sol with High reasoning is sufficient for the mathematical result derived here. For the next implementation, use a code/computational Work-style setup with strong reasoning and repository/file tooling; if GPT-6 Astra in Work is actually selectable and available, it is an appropriate option, but it is not required for scientific validity.

KAPABILITETSKLASSE:
H + C, with A useful but optional for implementation orchestration.

REASONING-NIVEAU:
High or strongest mathematically reliable available reasoning level.

BEGRUNDELSE:
The remaining task is now a sharply bounded validated implementation, not broad research. The decisive gain comes from changing the proof coordinates and certifying one event/energy anchor, not from larger sampling, likelihood work, or more brute-force Cartesian interval cells.

FALLBACK:
Strongest available reasoning model with exact file access, Python/rational computation and read-only repository inspection.

UPGRADE-TRIGGER:
Escalate to a stronger Work/frontier setup only if implementing the hybrid event certificate reveals a genuinely coupled proof/code problem that cannot be resolved in the bounded current architecture. Do not escalate merely for another replay.

PLUGIN-/TOOLBEHOV:
YES, bounded and specific.

RELEVANTE TOOLS:
- Attached authoritative journal and V7 final JSON.
- Read-only GitHub inspection of the executed Bubbleverse proof code and frozen `mwt5345/class_ede` source.
- Exact Python/rational arithmetic for implementation and independent replay.
- Wolfram Language only as an independent symbolic algebra check.

NOT REQUIRED:
Broad literature search, likelihood evaluation, MCMC/nested sampling, GPU, HPC campaign, or a native CLASS recapture.

---

## SAMLET JOURNAL

The authoritative updated journal is delivered as `Q047_SAMLET_JOURNAL.md`.

Update rule:
- This Mathematics-008 handoff is prepended.
- The complete incoming journal is retained byte-for-byte as the historical tail.
- Incoming journal bytes: 12999343
- Incoming journal SHA256: 4174ec43ca9e15bafdee9cea6ceef774791613b0f95af6bbd8b644ed2187c41d

No prior source, claim mapping, failed method, frozen configuration, Q047 closure, Q048 proposed status, or V7 provenance is deleted.

---

## AKTUEL OVERLEVERING

RESULT ID:
I-PROPOSED-Q048-MATHEMATICS-008

RESULT CLASS:
MATHEMATICAL_RESULT; SOURCE_INSPECTION_RESULT; METHOD_DERIVATION_RESULT; PARTIAL_RESULT; ROUTING_RESULT.

RESULT STATUS:
VALID DISTINCT PROOF ARCHITECTURE DERIVED; NOT YET EXECUTED AS A RIGOROUS NUMERICAL CERTIFICATE. FINAL_RESULT_GATE remains UNRESOLVED.

### 1. Exact remaining mathematical bottleneck

V7 is technically complete. Its Camspec branch stopped with `TRAJECTORY_TUBE_NOT_CLOSED` after 1693 accepted cells; it did not demonstrate a source-guard crossing. Every accepted V7 guard cell retained a positive equivalent guard margin, while the largest stored direct-ratio upper diagnostic remained approximately 0.124465 < 1/2.

The important mathematical diagnosis is that the current state representation, not the guard inequality itself, is the active blocker.

The V7 certificate propagates an axis-aligned Cartesian enclosure in `(phi,X)` through an oscillatory scalar system. Before the stop, the intervals undergo rapid wrapping:

- accepted cell 1598: z≈6749.44, endpoint `X≈[-111.93,-0.288]`;
- accepted cell 1599: z≈6742.85, endpoint `X≈[-113.07,+0.962]`, so the box begins to straddle the sign change;
- accepted cell 1688: z≈6443.43, endpoint `phi≈[-152.73,+152.90]`, `X≈[-1.851e4,+1.841e4]`;
- accepted cell 1692: z≈6443.32, endpoint `phi≈[-2795.80,+2795.98]`, `X≈[-1.412e5,+1.411e5]`.

Despite this enclosure explosion, the stored guard ratio upper diagnostic at the final accepted cell is still only ≈0.124465 and the accepted guard margin remains positive. This is a source-faithful proof/enclosure failure, not evidence that the source guard is physically approached.

The final V7 artifact does not serialize the complete first rejected cell/report after the last accepted prefix. Therefore its exact failed closure slack is NOT DOCUMENTED in the final artifact. The mechanism above is diagnosed from the accepted sequence plus the exact certificate construction; no rejected payload is invented.

### 2. Frozen source equations

For Camspec EDE n=3 at frozen source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`, define

`lambda = 2.435e27 / F`

`A = 4152.39 m^2 F^2`

`theta = lambda phi`

`U(theta) = A (1-cos(theta))^3 = V_e`

`f = V_floor = B_scf * 3.968e-8`

`X = phi_prime/a`

`e = E-f = X^2/2 + U(theta)`.

The source-real scalar equations in `u=ln(a)` are

`phi_u = X/H`

`X_u = -3X - V_phi/H`

with `V_phi = lambda U_theta`.

For K=0,

`H^2 = B0(a) + (e+f)/3`

where `B0(a)` is the frozen non-scalar background contribution.

The frozen source guard is

`U/(3 H^2) < 1/2`.

### 3. New exact phase-energy representation

Differentiating `e=X^2/2+U` along the source equations gives the exact identity

`e_u = -3 X^2 = -6(e-U) <= 0`.

Thus `e` is monotone nonincreasing.

For a fixed sign branch `s=sign(X)` away from a turning point,

`X = s sqrt(2(e-U))`

and

`theta_u = s lambda sqrt(2(e-U))/H`

`e_u = -6(e-U)`.

The source guard is exactly equivalent to

`G(a,theta,e) = 3 B0(a) + e + f - 2 U(theta) > 0`.

This removes the unbounded Cartesian `phi x X` rectangle from the main proof state. The energy coordinate is dissipative, and the phase coordinate is periodic/bounded by event segmentation.

### 4. Turning-point chart

The square-root phase-energy chart is not used across `X=0`. Introduce

`r=|X| >= 0`, `X=s r`.

On a fixed sign branch,

`theta_u = s lambda r/H`

`r_u = -3r - s lambda U_theta/H`

`e = r^2/2 + U(theta)`.

This chart is regular at `r=0` and supplies the event direction.

For `theta in (-pi,0)`, `U_theta<0`.

On the descending branch `s=-1`,

`r_u = -3r + lambda U_theta/H < 0`.

Hence, once the descending trajectory is in `(-pi,0)`, `r` decreases strictly until a turn if it reaches zero. At the event `r=0`, the original equation gives

`X_u = -lambda U_theta/H > 0`,

so the crossing direction is fixed: the physical branch changes from `s=-1` to `s=+1`.

This makes the sign change an event to certify, rather than a Cartesian interval that is allowed to straddle both signs and wrap.

### 5. First-turn existence structure

Suppose an admitted splice enclosure satisfies

- `0 < theta < pi`,
- `X<0`,
- `e-U>0`,
- and `e_upper < U(-pi)_lower = 8 A_lower`.

Because `e` cannot increase, a continuing descending branch cannot reach `theta=-pi` without first reaching `e-U=0`: at `theta=-pi`, `U=8A` would exceed the available energy. Therefore at least one turning event must occur before the branch could reach `-pi` (unless an earlier turn occurs already, which is also acceptable).

This is a structural existence statement, not yet an event-time certificate.

### 6. New post-anchor guard lemma

Let the required final transfer be

`a_T = 1/2871`

and let

`B_T_lower` be the exact lower bound on the same frozen non-scalar background `B0(a_T)`.

Since every non-scalar component used here is nonnegative and nonincreasing over the forward interval, for all `a <= a_T`,

`B0(a) >= B_T_lower`.

Also `U<=e` and `e` is nonincreasing.

Therefore, if at any certified anchor `a_* <= a_T` we prove

`e(a_*) <= e_*`

with

`e_* < 3 B_T_lower + f_lower`,

then for every later `a in [a_*,a_T]`,

`G = 3B0 + e + f - 2U`
`  >= 3B0 + f - e`
`  >= 3B_T_lower + f_lower - e_*`
`  > 0`.

So one sufficiently low certified energy anchor closes the source guard for the entire remaining interval without tracking scalar phase or further oscillations.

Using the already preserved exact V6 Camspec `base_at_transfer` lower endpoint, the displayed orientation value of this threshold is approximately

`3 B_T_lower + f_lower ≈ 2104.2930315`

in the source's inverse-Mpc-squared energy convention.

This displayed decimal is orientation only; the next executable must use the exact rational V6 base and frozen source-constant intervals.

### 7. Why the first turning point is the preferred anchor

At a turning point, `X=0`, hence

`e_turn = U(theta_turn)`.

This removes the kinetic-energy dependency exactly and is therefore the natural place to obtain a tight scalar-energy upper bound.

The prior V6 source-root energy certificate already establishes the source guard through approximately

`z=3562.590282`.

Consequently, the highest-value executable target is:

1. start from a rigorously admitted V7 accepted state before the Cartesian wrapping regime;
2. certify the first scalar turning event with the phase-energy/event chart;
3. preferably show that the event occurs while still inside the independent V6 safe-guard horizon;
4. prove `e_turn_upper < 3 B_T_lower + f_lower`.

If all four hold, then:
- V6 independently covers the source guard before the turn;
- the new post-anchor lemma covers it from the turn to z=2870;
- no full `(phi,X)` tube is needed after the turn.

If the turn is later than the V6 safe horizon, the phase-energy cells may instead evaluate the exact margin `G>0` directly only across the finite bridge to the turn. The method must not revert to the old Cartesian tube.

### 8. Rigorously admitted splice source

A splice must come only from an already accepted V7 cell, never a midpoint or native hint.

A strong diagnostic candidate is zero-based V7 accepted cell 1509:

- endpoint z≈8979.9711;
- certified endpoint `phi≈[0.1915839,0.2001225]`;
- certified endpoint `X≈[-36.2737,-29.2579]`, strictly negative.

Using ordinary floating evaluation only for orientation, the transformed candidate is approximately

- `theta≈[2.44741,2.55648]`, within `(0,pi)`;
- a conservative axis-aligned transformed kinetic-gap diagnostic `e_lower-U_upper≈61.9 >0`;
- transformed `e_upper≈4221.5 < 8A≈4624.1`.

These transformed decimals are explicitly NON-CERTIFIED DIAGNOSTICS. They select a promising proof splice only. The next executable must recompute `theta`, `U`, `e`, all inequalities and source constants with exact outward arithmetic before accepting the splice. If this particular cell fails the exact transformed gate, nearby already-accepted cells may be searched under a predeclared mathematical slack criterion; no new source trajectory may be invented.

### 9. Independent symbolic control

Wolfram Language was used only as an independent algebra check. Under positive-domain assumptions it simplified the four central expressions to

`{-3 X^2, 3 B + e + f - 2 U, sqrt(2) lambda s sqrt(e-U)/H, -6e+6U}`.

This independently confirms:
- cancellation in the energy derivative;
- the guard-margin transformation;
- the signed phase equation;
- `e_u=-6(e-U)`.

Wolfram supplied no physical parameter, trajectory, event location or guard verdict.

### 10. What has and has not been proved in Mathematics-008

[BEREGNET / PROVED]
- The phase-energy change of variables is source-equivalent away from turns.
- The hybrid `r=|X|` event chart is source-equivalent on each fixed-sign branch.
- `e_u=-3X^2<=0`.
- The transformed exact source guard is `3B0+e+f-2U>0`.
- A sufficiently low certified energy anchor below `3B_T+f` proves the source guard for the complete remaining interval.
- A low-energy turning event is therefore a mathematically sufficient target.
- The V7 failure mode is consistent with Cartesian interval wrapping and does not require treating the guard as approached or violated.

[NOT YET PROVED]
- The exact transformed splice gate for candidate cell 1509.
- The first-turn event bracket/time.
- The exact first-turn energy bound.
- `e_turn_upper < 3B_T_lower+f_lower`.
- The Camspec source guard through z=2870.
- Camspec He1f/He2 continuation and H-entry q.
- Native floating-point/source-instance admission.
- Shared first `q=1e-6` cutoff.
- Complete latch/reset `x_e(z)` and `tau_T(z)` difference bounds.

No physical anomaly or model falsification is established.

### 11. Minimal new executable proof target

The next motor should implement one bounded successor method, conceptually:

`source_root_phase_energy_first_turn_guard_v1`

This is a method name, NOT a pre-authorized PROGRAM_ID. The Execution-Mechanism motor must decide whether a new documented program/version is needed.

Required gates:

A. Reverify the entire chosen V7 splice cell from its stored certificate and frozen source.

B. Transform the endpoint outward to `(theta,e)` and prove:
- sign `X<0`;
- `0<theta<pi`;
- positive kinetic gap;
- `e_upper<8A_lower`.

C. Propagate a validated phase-energy branch without Cartesian `(phi,X)` wrapping.

D. Use the smooth `(theta,r,s)` chart to bracket/recompute the first `r=0` turning event and its crossing direction.

E. Compute exact outward `e_turn`.

F. Compare `e_turn_upper` to the exact transfer threshold `3B_T_lower+f_lower`.

G. If the event is within the inherited V6 guard horizon and the threshold passes, combine:
- inherited V6 guard before the event;
- Mathematics-008 energy-anchor lemma after the event.

H. If the event lies outside the V6 safe horizon, require exact transformed guard margin `G>0` on every finite bridge cell up to the event before applying the post-anchor lemma.

I. Only after full Camspec guard coverage is established, continue the already-defined positive-w He1f/He2 thermal calculation to z=2870. Use the Mathematics-007 sign rule and Saha transition control. H bounds may use the source-root energy envelope before the turn and the tightened post-turn energy cap afterward; use phase-energy cells only where a tighter background bound is actually required.

J. Return Camspec conditional H-entry q or a precise bounded obstruction.

K. STOP. Do not launch H/frec/cutoff/full-xe/tau work in the same target.

### 12. Success condition

SUCCESS if the bounded executable produces either:

1. a fully recomputed conditional Camspec source-guard certificate through z=2870 plus He1f/He2 continuation and conditional H-entry q,

or

2. a precise obstruction tied specifically to the new phase-energy/first-turn proof, with the exact failed inequality/event gate preserved.

A technical inability to certify the new sufficient bound is not model falsification.

### 13. Failure/falsification semantics

- `TRAJECTORY_TUBE_NOT_CLOSED` from V7 remains a method obstruction, not a physical result.
- Failure of the new phase-energy certificate is another proof-method result unless the exact admitted source guard itself is shown nonpositive.
- A conditional physical/source guard failure exists only if `G<=0` is rigorously established on an admitted source-real trajectory.
- Native/historical source-instance claims remain separately unresolved.

### 14. Stop condition

Stop the next execution when the finite first-turn/energy-anchor method either:
- proves the Camspec guard and reaches conditional H-entry, or
- returns one precise bounded obstruction that cannot be repaired without changing the mathematical method or adding genuinely new source/native evidence.

Return once to RESULT INGESTION & ROUTING.

Do not rerun V7 unchanged.
Do not increase Cartesian halving/cell counts as a substitute for the new coordinates.
Do not start the shared cutoff/full-history stage automatically.

---

## KILDER TIL NÆSTE MOTOR

### K-PROPOSED-Q048-SOURCE-002 — frozen primary code source
Repository: `mwt5345/class_ede`
Commit: `5a131c91d657dd9a7c6364cc45b038710f8d0d97`
Relevant source: `source/background.c`
Relevant because:
- defines EDE `V_e_scf`, `V_scf`, `dV_scf`;
- defines scalar source units;
- applies the source guard `V_e_scf / rho_crit / 3 < 0.5`.
DOI/arXiv: not required for this code-provenance claim; no invented bibliography.

### K-PROPOSED-Q048-INPUT-001 — frozen captured effective inputs
Origin: run 38140371059
Relevant because:
- supplies the four Q041 FULL/start0 reconstructed configurations;
- contains Camspec EDE F, m, B, initial phi/X, finite-node ncdm realization and fixed accepted z_reio.
External publication metadata: NOT APPLICABLE; internal captured input evidence.

### K-PROPOSED-Q048-GITHUB-RUN-38293480870 — V6 official execution
Role:
- source-root energy certificate;
- exact Camspec transfer-base lower bound;
- independent safe guard horizon through z≈3562.590282;
- verified z=4600 thermal endpoint.

### I-PROPOSED-Q048-MATHEMATICS-007 — prior mathematics
Role:
- sign-aware positive-w formula;
- exact-real He1f/He2 Saha identity;
- exact direct-guard reformulation;
- V7 finite task definition.

### K-PROPOSED-Q048-GITHUB-RUN-38348832247 — V7 official execution
Executed commit:
`c9ca98f232a0c753ce9a8c04437fc5d7ef699dab`
Role:
- accepted Camspec source-real prefix/cells;
- bounded Cartesian tube obstruction;
- successful Hillipop H-entry continuation;
- technical execution provenance.

### I-PROPOSED-Q048-GUARDCONT-GITHUB-38348832247 — V7 internal numerical result
Role:
- 1693 accepted Camspec guard cells;
- final `TRAJECTORY_TUBE_NOT_CLOSED`;
- positive accepted guard margins;
- Hillipop H-entry q.

### I-PROPOSED-Q048-MATHEMATICS-008 — this result
Role:
- Cartesian-wrapping diagnosis;
- phase-energy and turn-event equations;
- post-anchor guard lemma;
- bounded next executable target.

---

## TOOL- OG PLUGINPROVENIENS

Tool: Files
Function: recovered the authoritative updated journal, V7 final result and ingestion handoff.
Underlying data: user-supplied Bubbleverse files.
Role: primary internal evidence retrieval.

Tool: GitHub connector, read-only
Function: inspected the exact V7 proof backend at executed Bubbleverse commit and frozen `class_ede` source.
Underlying objects:
- `Morfindien/Bubbleverse` at `c9ca98f232a0c753ce9a8c04437fc5d7ef699dab`;
- `mwt5345/class_ede` at `5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
Role: code/source provenance; no repository write.

Tool: exact/local Python analysis
Function: inspected accepted V7 cells and computed orientation-only transformed diagnostics.
Underlying data: supplied `q048_guard_final_v7.json`.
Role: method diagnosis and candidate-splice selection. Float diagnostics are explicitly not admitted as certificates.

Tool: Wolfram Language
Function: independent symbolic simplification of the phase-energy algebra.
Underlying data: equations already derived from the frozen source.
Result: exact algebraic cross-check only; no physical input.

No broad external literature search was scientifically necessary.

---

## HOVEDSPØRGSMÅL STATUS

Q048 is NOT answered yet.

The new mathematics materially changes the route: the Camspec obstruction is no longer best attacked by extending the same Cartesian tube. A finite source-equivalent first-turn/energy-anchor certificate now exists as a distinct implementable proof architecture.

Therefore the Mathematics Engine is no longer the best next motor for the immediate uncertainty.

ROUTE:
AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.

The next motor must implement and validate the bounded phase-energy first-turn certificate before any later Q048 cutoff/full-history work is authorized.
