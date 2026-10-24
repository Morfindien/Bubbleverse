# BUBBLEVERSE --- Q050 V3 MATEMATISK RESULTAT OG OVERLEVERING

PROMPT_ID: BUBBLEVERSE.MATHEMATICS PROMPT_VERSION: 2.3.0 TARGET_Q: Q050
RUN_ID: LOCAL-Q050-V3-PION-REDUCTION-20261025 WORKFLOW_STATE:
READY_FOR_HANDOFF SCIENTIFIC_STATE: INCONCLUSIVE TECHNICAL_STATE: PASS

## Resultat

V3 reducerer den resterende Pion-selectorobstruktion til en konkret,
eksekverbar intervaltest.

Den frosne HyRec-kilde bruger for SWIFT og z\<900

`P = B/(3R + L + B)`

med

`B = four_betaB`, `R = RLya = LYA_FACT * H/[nH(1-xHII)]`,
`L = L2s1s = 8.2206 s^-1`, `PION_MAX = 0.01`.

På switchingfladen `P=0.01` gælder derfor eksakt

`3R = 99B - L`.

Fladen kan kun eksistere, hvis

`B > L/99`.

Desuden er

`∂P/∂xHII = -3 B R / [(3R+L+B)^2 (1-xHII)]`.

På `P=0.01` reduceres dette til

`∂P/∂xHII = -10^-4 (99 - L/B)/(1-xHII) < 0`

over enhver ikke-degenereret del af fladen.

Dette viser, at Pion-fladen er transversal i state-koordinaten xHII: P
falder strengt med xHII, når z/background holdes fast.

## One-sided normal derivative

Lad `p=P-0.01`. Langs en source-real løsning:

`dp/ds = P_z z' + P_T T' + P_x x' + P_bg·bg'`.

På samme switching-state er alle eksplicitte background-/radiation-led
fælles for HMLA- og SWIFT-armene. Den branch-afhængige forskel er derfor

`(dp/ds)_HMLA - (dp/ds)_SWIFT = P_x [(dxHII/ds)_HMLA - (dxHII/ds)_SWIFT]`.

Da `P_x<0`, er hele side-kompatibilitetsspørgsmålet reduceret til et
rigorøst enclosure af forskellen mellem de to source-real hydrogenfelter
på selve Pion-fladen.

## SWIFT-fit gate reducerer domænet yderligere

Kilden vælger, når `P>=0.01`, alligevel HMLA hvis

`TR/kBoltz/fsR^2/meR < fit->swift_func[0][0]`.

Den frosne fitfil har første temperaturknude `1775 K`, og den frosne
konfiguration har `fsR=meR=1`.

Derfor er `P=0.01` ikke en HMLA↔SWIFT-diskontinuitet under 1775 K: begge
sider ender i HMLA. Den potentielle diskontinuitet er begrænset til den
del af `0<=z<=810`, hvor `Tcmb(1+z) >= 1775 K`, dvs. omtrent
`z >= 650.25` for den frosne Tcmb. Den endelige verifier skal beregne
tærsklen direkte fra de frosne binary64-input og anvende outward
rounding; dette omtrentlige decimaltal er ikke acceptkriteriet.

## Reachability/enlarged-domain note

Det arvede theorem-domain ved z=810 er bredt (`h` op til 0.99999), så
Pion-fladen må ikke afvises alene som "fysisk usandsynlig". V3 bruger
derfor ikke sampling til at erklære den unreachable. Den næste test skal
enten certificere one-sided crossing/compatibility over hele den
potentielt reachable surface eller levere et konkret
subdomain/counterexample med reachability-status tydeligt adskilt.

## Hvorfor Matematikmotoren stopper her

Den resterende afgørelse kræver source-real evaluation/enclosure af
HMLA- og SWIFT-felterne med HyRec-tabeller, den frosne
CLASS/EDE-background og outward-error control over et kontinuert
surface-domæne. Det er en defineret numerisk/execution-test.
Matematikmotor 2.3.0 siger at route til EXECUTION-MECHANISM / NUMERICAL
/ HPC / MOTOR-BUILDER, når en defineret test kræver
implementation/execution/compute, som den aktuelle matematikrunde ikke
passende kan levere.

Ingen global continuation-konklusion gættes.

## NÆSTE MOTOR

**BUBBLEVERSE --- EXECUTION / HPC MOTOR BUILDER, aktuell projektversion
2.3.0 hvis den fortsat er den registrerede aktuelle version.**

Hvis Prompt Registry viser et nyere kompatibelt engine-ID/version, skal
den registrerede aktuelle version bruges uden at ændre testkontrakten.

## NÆSTE OPGAVE --- EXECUTION CONTRACT

BLOCKER_ID: LOCAL-Q050-PION-SURFACE-NORMAL-V3

Formål: Certificér one-sided normalfelter på den potentielt
diskontinuerte `Pion=0.01`-surface i det frosne
`hillipop-ede_n3`-system.

Frosne pins: - CLASS/HyRec source:
`mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97` -
Bubbleverse config source:
`Morfindien/Bubbleverse@d397732f65da2d1566089b9153a4145a605f8557` -
config SHA-256:
`2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b` -
V151 checkpoint SHA-256:
`60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96` - q
branches: `q=10^-6` and `q=0` - z-domain: only the intersection of
`[0,810]` with the exact active-SWIFT-temperature region and the
algebraically feasible `B>L/99` region. - admitted state/invariant
domain inherited from Q049/Q050; do not silently narrow it by sampled
trajectories.

Required implementation: 1. Reconstruct exact Pion surface using
`3R=99B-L`. 2. Use frozen CLASS background values/functions, not a
replacement LCDM approximation. 3. Evaluate both `rec_HMLA_dxHIIdlna`
and `rec_swift_hyrec_dxHIIdlna` on identical surface states. 4. Include
both q branches through `xe=xHII+q` as source-real for this low-z
comparison. 5. Propagate the full normal derivative with the actual
evolution orientation/sign. 6. Use interval/outward bounds or another
auditable enclosure sufficient to certify sign/compatibility; point
sampling is diagnostic only. 7. Partition z/T/state only as needed;
preserve a coverage manifest. 8. Independently reconstruct at least the
algebraic Pion-surface identity and selector equality convention. 9.
Record all source/table hashes actually consumed.

Acceptance: - certified compatible crossing/one-sided existence
condition over every potentially reachable surface cell for both q
branches, OR - certified nonreachability of all unresolved cells from
the declared admitted domain.

Rejection/counterexample: - a certified reachable surface cell where the
literal selector produces incompatible one-sided normal behavior
sufficient to defeat the requested AC continuation.

Inconclusive: - unresolved interval cells remain because bounds overlap
zero/compatibility threshold, or source-real background/table dependency
cannot be enclosed. Return the first unresolved cells and exact missing
certificate; do not replace with sampling.

Expected output: `Q050_V4_PION_SURFACE_EXECUTION_RESULT.json` plus
machine-readable coverage/certificate and execution provenance, routed
back to Matematikmotor 2.3.0 for scientific interpretation.

## Pointledger

PREVIOUS_POINTS_ENTRY: Q050 V2 TOTAL_BEFORE: 200 pts RUN POINTS: 105 pts
POINTS_BREAKDOWN: ANALYSIS 45 + COMPUTATION 10 + SEARCH 25 + VALIDATION
25 = 105 POINTS_BASIS: source-real selector algebra, derivative
reduction, SWIFT-fit gate reconstruction, domain/routing validation;
heuristic editorial counter. TOTAL POINTS: 305 pts CYCLE PROGRESS:
305/1000 pts NEXT SOME MILESTONE: 1000 pts POINTS TO NEXT PUBLICATION:
695 pts NEW MILESTONES: NONE PENDING SOME PACKAGES: NONE POINTS_STATE:
VERIFIED PUBLICATION_STATE: NOT_DUE

## Provenance/status

GITHUB_READ_STATE: VERIFIED GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD

No GitHub write or commit is claimed. Q050 is not CLOSED. Motor 14 is
not the next engine.
