# BUBBLEVERSE — Q050 CLEAN V3 MATEMATISK RESULTAT OG OVERLEVERING

PROMPT_ID: BUBBLEVERSE.MATHEMATICS
PROMPT_VERSION: 2.3.0
TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
RUN_ID: LOCAL-Q050-CLEAN-V3-PION-REDUCTION-20261025
WORKFLOW_STATE: READY_FOR_HANDOFF
SCIENTIFIC_STATE: INCONCLUSIVE
TECHNICAL_STATE: PASS
LINEAGE: Q050 CLEAN V1 -> CLEAN V2 -> CLEAN V3
OLD_PRE_RESET_Q050_GITHUB_MATERIAL: REFERENCE_ONLY_NOT_STATE

## Resultat

CLEAN V3 reducerer den resterende `Pion=0.01` selector-gate til en konkret source-real intervaltest.

For SWIFT og z<900 bruger den frosne HyRec-kilde

`P = B/(3R + L + B)`

med
`B=four_betaB`,
`R=RLya=LYA_FACT*H/[nH(1-xHII)]`,
`L=L2s1s=8.2206 s^-1`,
`PION_MAX=0.01`.

På switchingfladen `P=0.01` gælder eksakt

`3R = 99B - L`.

Da `R>0`, kan fladen kun eksistere når

`B > L/99`.

Med den frosne `Trad=Tcmb(1+z)` og source-formlen for `four_betaB` falder B monotont kraftigt mod lavere z i det relevante interval. En direkte binary64-diagnostisk løsning med de sourcekonstanter, der er læst fra den pinned kilde, placerer `B=L/99` ved ca. `z=671.8885`. Dette decimaltal er kun diagnostisk; den endelige execution-certificering skal bruge de frosne inputs og outward enclosure.

## State-transversalitet

Ved fast z/background:

`R = C/[1-xHII]`, hvor `C=LYA_FACT*H/nH > 0`.

Derfor

`dR/dxHII = R/(1-xHII)`.

For `P=B/(3R+L+B)` fås

`∂P/∂xHII = -3BR / [(3R+L+B)^2 (1-xHII)]`.

På `P=0.01`, hvor nævneren er `(100B)^2` og `3R=99B-L`, reduceres dette til

`∂P/∂xHII = -10^-4 * (99-L/B)/(1-xHII) < 0`

på enhver ikke-degenereret del af switchingfladen.

Pion-fladen er altså strikt transversal i state-koordinaten `xHII`.

## One-sided normal reduction

Lad `p=P-0.01`. Langs source-real evolution:

`dp/ds = explicit_common_terms + P_x * dxHII/ds`.

På samme switching-state er de eksplicitte background-/radiation-led fælles for HMLA- og SWIFT-armene. Derfor er branch-forskellen eksakt

`(dp/ds)_HMLA - (dp/ds)_SWIFT = P_x * [(dxHII/ds)_HMLA - (dxHII/ds)_SWIFT]`.

Da `P_x<0`, er det resterende compatibility-spørgsmål reduceret til et rigorøst enclosure af HMLA- og SWIFT-hydrogenfelterne på selve `P=0.01`-fladen.

## SWIFT-fit gate

Når `P>=0.01`, vælger source stadig HMLA hvis

`TR/kBoltz/fsR^2/meR < fit->swift_func[0][0]`.

Den kendte frosne SWIFT-fit lower node er 1775 K, med `fsR=meR=1`. Derfor er Pion-fladen kun en faktisk HMLA↔SWIFT-discontinuity i intersectionen mellem:
1. `0<=z<=810`,
2. den algebraisk feasible region `B>L/99`,
3. den aktive SWIFT-fit temperaturregion.

Den algebraiske `B>L/99` gate er i praksis strammere end den omtrentlige 1775 K gate for denne frozen configuration; endelig interval execution skal afgøre dette med outward bounds, ikke decimaldiagnostik.

## Reachability firewall

Det arvede admitted z=810-domain er bredt:
`h in [346752030166741/10^18, 99999/100000]`,
`v in [0.98,1.000001]`.

V3 afviser derfor ikke Pion-fladen som “fysisk usandsynlig” og bruger ikke trajectory sampling som reachability-bevis.

## Stop/routing

Den næste afgørelse kræver faktisk source-real evaluation/enclosure af `rec_HMLA_dxHIIdlna` og `rec_swift_hyrec_dxHIIdlna` over et kontinuert surface-domain med de frosne HyRec-tabeller og den frosne CLASS/EDE-background.

Matematikmotorens analytiske reduktion er derfor færdig for denne runde.

BLOCKER_ID: LOCAL-Q050-CLEAN-V3-PION-SURFACE-NORMAL

NEXT_ENGINE: BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER (aktuel kompatibel projektversion; tidligere projektmateriale viser 2.4.0, men registry/version skal verificeres ved execution).

## Execution contract

1. Reconstruct `P=0.01` via `3R=99B-L`.
2. Restrict to exact intersection of `[0,810]`, `B>L/99`, and active SWIFT temperature region.
3. Use frozen CLASS/EDE background, not replacement LCDM.
4. Evaluate HMLA and SWIFT hydrogen derivatives on identical surface states.
5. Treat q=`1e-6` and q=`0` separately through source-real `xe=xHII+q`.
6. Propagate full normal derivative in actual evolution orientation.
7. Use outward interval bounds or equivalent auditable enclosure; sampling is diagnostic only.
8. Partition only as needed and preserve full coverage manifest.
9. Independently verify Pion identity, equality convention, and all source/table hashes consumed.
10. Return compatible-crossing certificate, certified nonreachability, certified reachable obstruction, or exact unresolved cells.

Expected scientific result:
`Q050_CLEAN_V4_PION_SURFACE_EXECUTION_RESULT.json` plus coverage/certificate/provenance, returned to Mathematics 2.3.0.

## Claim firewall

CLEAN V3 does NOT prove global AC continuation, uniqueness, Pion compatibility, SWIFT compatibility, or nonreachability. It proves the algebraic surface reduction and strict `xHII`-transversality and specifies the finite decisive execution test.

## Pointledger

PREVIOUS TOTAL: 200 pts
RUN POINTS: 105 pts
TOTAL POINTS: 305 pts
CYCLE PROGRESS: 305/1000 pts
NEXT SOME MILESTONE: 1000 pts
POINTS TO NEXT PUBLICATION: 695 pts
NEW MILESTONES: NONE
PUBLICATION_STATE: NOT_DUE

## Provenance

Frozen source: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
Frozen config SHA256: `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`.
Checkpoint SHA256: `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`.

Fresh source inspection used `hydrogen.c` and `hydrogen.h`. Only after the clean derivation was complete, discarded pre-reset Q050 V3 material was consulted as a reference cross-check. It was not imported as scientific state, execution result, journal lineage, or points.

GITHUB_READ_STATE: VERIFIED
GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD
