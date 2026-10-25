# BUBBLEVERSE — Q050 CLEAN V2 MATEMATISK RESULTAT

STATUS: OVERLEVERING
WORKFLOW_STATE: READY_FOR_HANDOFF
SCIENTIFIC_STATE: INCONCLUSIVE
TECHNICAL_STATE: PASS
TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
RUN_ID: LOCAL-Q050-CLEAN-V2-PEEBLES-NORMAL-20261025
PROMPT_ID: BUBBLEVERSE.MATHEMATICS
PROMPT_VERSION: 2.3.0
LINEAGE: Q050 CLEAN V1 -> Q050 CLEAN V2
OLD_PRE_RESET_Q050_GITHUB_MATERIAL: REFERENCE_ONLY_NOT_STATE

## V2-opgave

Certificér den one-sided source-real normal/reachability-gate, som CLEAN V1 isolerede ved
`v=Tmat/Trad=T_RATIO_MIN=0.1`, separat under de frosne q-grene, uden at convexify selectoren.

## Autoriseret domæne

Fra den autoriserede Q048/Q049-lineage:
- `t = ln(811/(1+z))`
- `h=xHII`
- `v=Tmat/Trad`
- z=810 start: `h in [346752030166741/10^18, 99999/100000]`
- z=810 start: `v in [0.98,1.000001]`
- inherited path enclosure: `0<h<1` og `0.98 exp(-t) <= v <= 1.000001`
- q behandles separat som `10^-6` og `0`.

## Fresh source-real udledning

Den frosne wrapper vælger PEEBLES ved
`Trad_phys <= TR_MIN || Tmat/Trad <= T_RATIO_MIN`.
Med `T_RATIO_MIN=0.1` tilhører equality PEEBLES-siden.

For den frosne konfiguration er de ekstra temperature-sourceled fra exotic injection og IDM-baryon coupling inaktive. CLASS' sene temperatur-ODE er derfor

`dTmat/dz = 2*Tmat/(1+z) + rate_gamma_b*(Tmat-Trad)/(H*(1+z))`.

Da `Trad=Tcmb*(1+z)`, fås for `v=Tmat/Trad`

`dv/dz = [v + (rate_gamma_b/H)*(v-1)]/(1+z)`.

På selectorfladen `v=0.1`:

`d(v-0.1)/dz = [0.1 - 0.9*(rate_gamma_b/H)]/(1+z)`.

Det afgørende source-real faktum er, at denne temperaturkomponent ved samme state ikke afhænger af, om hydrogen-derivaten i dette øjeblik blev routed til PEEBLES eller non-PEEBLES (HMLA/SWIFT). Hydrogen-selectorens jump ændrer hydrogenfeltet, men skaber ikke to modsatrettede øjeblikkelige normalfelter til ratiofladen.

## Tangens

Normalen kan være nul ved `rate_gamma_b/H=1/9`. Det giver ikke i sig selv en literal-selector no-solution obstruction, fordi begge sider deler samme temperaturkomponent ved kontaktpunktet. V2 påstår ikke uniqueness eller et globalt regularitetsbevis; den afviser kun CLEAN V1's specifikke åbne normal-kompatibilitetsgate som første obstruction.

## V2-resultat

RESULT_ID: LOCAL-Q050-CLEAN-V2-PEEBLES-RATIO-NORMAL-COMPATIBILITY

`LOCAL-Q050-CLEAN-V1-PEEBLES-RATIO-SURFACE-NORMAL` = CLEARED_AS_FIRST_OBSTRUCTION.

Dette er en source-level algebraisk side-kompatibilitetscertificering, ikke et globalt continuation theorem.

## Næste source-real interface

I `rec_dxHIIdlna`, for SWIFT og `z<900`:

`Pion = four_betaB/(3*RLya + L2s1s + four_betaB)`

med

`RLya = LYA_FACT(1,1)*H/nH/(1-xHII)`.

Kilden vælger HMLA ved `Pion < PION_MAX`, hvor `PION_MAX=0.01`; equality går derfor til den modsatte routing og videre gennem SWIFT-logikken.

Her skifter selve hydrogenkomponenten mellem HMLA og SWIFT. CLEAN V2 har ikke certificeret den fulde normalderivat til `Pion-0.01` over hele admitted surface.

FIRST_UNRESOLVED_GATE:
`LOCAL-Q050-CLEAN-V2-PION-SURFACE-NORMAL`.

## Claim firewall

V2 beviser ikke:
- global AC continuation til z=0;
- uniqueness;
- at Pion- eller SWIFT-grid-interface er benigne;
- identiske selectorhistorier for alle starts eller begge q-grene;
- fysisk smallness af latch/reset-forskellen.

## Provenance

Frozen source:
`mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.

Freshly checked source locations:
- `external/HyRec2020/hydrogen.h`: `T_RATIO_MIN=0.1`, `PION_MAX=1e-2`.
- `external/HyRec2020/wrap_hyrec.c`: outer PEEBLES equality/routing.
- `source/thermodynamics.c`: coupled hydrogen and late temperature equations.
- `external/HyRec2020/hydrogen.c`: Pion/HMLA/SWIFT routing.

Old pre-reset Q050 GitHub material was consulted only as reference/cross-check after the clean derivation and is not adopted as state, point history, or proof lineage.

## Pointstatus

PREVIOUS TOTAL POINTS: 110 pts
RUN POINTS: 90 pts
TOTAL POINTS: 200 pts
CYCLE PROGRESS: 200/1000 pts
NEXT SOME MILESTONE: 1000 pts
POINTS TO NEXT PUBLICATION: 800 pts
NEW MILESTONES: NONE
PUBLICATION_STATE: NOT_DUE

## Slutstatus

SCIENTIFIC_STATE: INCONCLUSIVE
Q050_STATE: ACTIVE
CLEARED_GATE: PEEBLES temperature-ratio one-sided normal compatibility
NEXT_ENGINE: BUBBLEVERSE.MATHEMATICS 2.3.0
NEXT_TASK: define `p=Pion-0.01`; reduce p=0 on the frozen admitted domain; derive source-faithful one-sided `dp/ds` from HMLA and SWIFT sides; certify crossing/avoidance or isolate the first concrete obstruction. If cleared, audit the SWIFT fit-grid lower-temperature interface.
