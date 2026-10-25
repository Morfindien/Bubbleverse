# BUBBLEVERSE --- OVERLEVERING

PROMPT_ID: BUBBLEVERSE.MATHEMATICS PROMPT_VERSION: 2.3.0 TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1 RUN_ID:
LOCAL-Q050-MATH-SELECTOR-RECOVERY-20261025-V1 UTC:
2026-10-25T00:28:09.945574+00:00 WORKFLOW_STATE: ACTIVE
SCIENTIFIC_STATE: INCONCLUSIVE TECHNICAL_STATE: PASS PUBLICATION_STATE:
NOT_DUE

## Hovedspørgsmål

For den frosne hillipop-ede_n3-konfiguration og hver fast admitted
common background på 0 \<= z \<= 810: findes en absolut kontinuert
source-real fortsættelse til z=0 fra enhver tilstand i det validerede
z=810-domæne, separat for q=10\^-6 og q=0, under de eksakte
deterministiske hydrogen/temperatur-selectors uden convexification?

## Adoption

Q050 adopteres i denne runde som et reelt nyt spørgsmål under den
allerede autoriserede session. Q049 forbliver CLOSED og uændret. Ingen
tidligere Q050_V1--V4-fil anvendes som videnskabeligt input eller
historik i denne runde.

## Verificerede pins

-   CLASS/HyRec source commit: 5a131c91d657dd9a7c6364cc45b038710f8d0d97
-   Frozen Bubbleverse config: q048_prefix_config_v1.json
-   Frozen config SHA-256:
    2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b
-   Expected validated V151 checkpoint SHA-256:
    60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96
-   Anchor: actual127/frontier810
-   q branches: 10\^-6 and 0
-   t = ln(811/(1+z)), h=xHII, v=Tb/Tgamma
-   inherited z=810 domain: h in \[346752030166741/10\^18,
    99999/100000\], v in \[0.98,1.000001\]
-   inherited path enclosure: 0\<h\<1 and 0.98 exp(-t) \<= v \<=
    1.000001

## Source-real selector recovery

Pinned wrap_hyrec.c gives the outer hydrogen selector:

-   if Trad_phys \<= TR_MIN OR Tmat/Trad \<= T_RATIO_MIN: model =
    PEEBLES
-   otherwise model remains MODEL = SWIFT

Pinned hydrogen.h gives: - TR_MIN = 0.004 eV - T_RATIO_MIN = 0.1 -
PION_MAX = 0.01 - MODEL = SWIFT in history.h

Pinned hydrogen.c gives the inner SWIFT routing: - for z\<900 compute
Pion - if Pion \< PION_MAX: HMLA - else, in SWIFT mode, if rescaled TR
is below the first SWIFT fit-grid temperature: HMLA - otherwise: SWIFT
correction-function field

Equality conventions are therefore source-real and non-symmetric: - v =
0.1 routes to PEEBLES because the wrapper uses \<= - Pion = 0.01 does
NOT take the Pion\<PION_MAX HMLA branch - the SWIFT-grid lower
comparison uses strict \<

## New mathematical reduction

The Q049 late thermal equation can be written

v' = -v + beta(1-v), beta \>= 0,

with t increasing toward z=0. The thermal normal component on the
selector surface v=0.1 is evaluated from the same CLASS temperature
equation on both hydrogen sides at the same state. Thus the hydrogen
selector changes the h-field, but it does not introduce an instantaneous
jump in the normal v-component itself.

This is useful but is not yet a global continuation theorem. If the
common normal component is nonzero, local crossing is transversal and
the literal selector can be concatenated locally. If it vanishes,
first-order normal information is insufficient: the different h-fields
can change beta after contact, so a higher-order/one-sided crossing
argument is required.

The inherited Q049 enclosure does not exclude v=0.1: its lower barrier
reaches 0.98/811 = 49/40550 ≈ 0.00120838 at z=0. Therefore the PEEBLES
ratio interface cannot be removed from the theorem domain by the
existing invariant alone.

## Result

NEW RESULT ID: LOCAL-Q050-SELECTOR-CALLCHAIN-AND-RATIO-INTERFACE-V1

Source-complete selector recovery is PASS for the outer PEEBLES and
inner HMLA/SWIFT/Pion logic described above.

The first unresolved existence obligation is:

BLOCKER_ID: LOCAL-Q050-RATIO-SURFACE-CROSSING-V1

Prove, on every potentially reachable point of v=0.1 in the inherited
admitted domain and separately for q=10\^-6 and q=0, that the literal
selected field admits continuation through/tangent to the surface. A
first-order proof may use a rigorous bound on

g(t,h)=v'(t,h,0.1) = -0.1 + 0.9 beta(t,h,q).

If 0 is excluded from g on the reachable surface, crossing direction is
certified. If g can contain 0, evaluate the required
one-sided/higher-order condition without convexifying the selector.

After this surface is cleared, repeat the same existence audit for
Pion=0.01 and the SWIFT-fit lower-grid interface if they are potentially
reachable.

No sampling-only existence claim is accepted.

## Termination gate

G1: PASS. G2: PARTIAL PASS --- source/config identity recovered; the
checkpoint identity is inherited/expected from the accepted Q049 state.
G3: NOT YET --- selector existence proof incomplete. G4: NOT YET. G5:
NOT YET. G6: FAIL/OPEN --- ratio selector crossing is
conclusion-critical. G7: PASS for this forward append package;
historical Q001--Q049 content is not rewritten.

Q050 remains ACTIVE / INCONCLUSIVE. No Q051 routing.

## Point event

POINTS_EVENT: RESEARCH_RUN PREVIOUS_POINTS_ENTRY: POINTS_INIT / TOTAL 0
ANALYSIS_POINTS: 45 COMPUTATION_POINTS: 5 SEARCH_POINTS: 25
VALIDATION_POINTS: 20 RUN POINTS: 95 pts TOTAL POINTS: 95 pts CYCLE
PROGRESS: 95/1000 pts NEXT SOME MILESTONE: 1000 pts POINTS TO NEXT
PUBLICATION: 905 pts NEW MILESTONES: NONE PENDING SOME PACKAGES: NONE
POINTS_STATE: VERIFIED PUBLICATION_STATE: NOT_DUE POINTS_BASIS:
Heuristisk redaktionel tæller: fuld motor/start-gate gennemgang,
targeted GitHub state recovery, frozen config recovery, pinned
CLASS/HyRec source/call-chain inspection, selector algebra and first
existence-interface reduction. Ingen native/HPC-kørsel eller trajectory
integration er udført.

## Næste eksekverbare opgave

Bliv i Matematik. Bind beta på v=0.1 til den frosne common background og
source-real reionization map, og lav en rigorøs one-sided
normal/crossing certificate for hele potentielt reachable ratio-surface.
Hvis førsteordensnormalen kan ramme nul, gå direkte til den minimale
højereordens interface-test. Derefter Pion og SWIFT-grid.

GITHUB_READ_STATE: VERIFIED/PARTIAL_TARGETED GITHUB_WRITE_STATE:
READY_FOR_MANUAL_UPLOAD
