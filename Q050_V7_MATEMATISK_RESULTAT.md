# BUBBLEVERSE --- Q050 V7 MATEMATISK RESULTAT

BUBBLEVERSE --- OVERLEVERING

PROMPT_ID: BUBBLEVERSE.MATHEMATICS PROMPT_VERSION: 2.3.0 RUN_ID:
LOCAL-Q050-V7-PION-NORMAL-REDUCTION-20261025 TARGET_Q: Q050
WORKFLOW_STATE: READY_FOR_HANDOFF SCIENTIFIC_STATE: INCONCLUSIVE
TECHNICAL_STATE: PASS

## Genbrugt uden gentagelse

V6's verificerede selector-kontrakt genbruges: den ægte HMLA/SWIFT
`Pion=0.01`-interface findes kun for `650.256650155934722 <= z <= 810`.
Under denne grænse ender begge selectorveje i HMLA.

## Ny matematisk reduktion

Sæt

`B(z)=four_betaB`, `R(z,x)=RLya=A(z)/(1-x)`, `A(z)=LYA_FACT*H(z)/nH(z)`,
`L=L2s1s`.

På `Pion=0.01` gælder præcist

`F(z,x) = 99 B(z) - 3 R(z,x) - L = 0`.

Dermed kan selectorfladen skrives eksplicit som

`1-x_HII = 3 A(z)/(99 B(z)-L)`,

forudsat `99 B(z)>L` og at den resulterende state ligger i det
autoriserede Q050-domæne.

Dette reducerer en todimensional selectorflade til en én-parameter kurve
bestemt af den frosne baggrund.

## Normalderivationen

Langs en løsning:

`dF/dz = 99 B'(z) - 3 R'(z)`,

og

`R'/R = H'/H - 3/(1+z) + x_HII'/(1-x_HII)`,

fordi `nH proportional (1+z)^3`.

Altså

`N = dF/dz = 99 B' - 3 R [H'/H - 3/(1+z) + x_HII'/(1-x_HII)]`.

Den eneste branch-afhængige del ved samme state/background er `x_HII'`.
Derfor

`N_SWIFT - N_HMLA = -3 R (x'_SWIFT-x'_HMLA)/(1-x_HII)`.

Wrapperen giver source-faithfully

`x_HII' = dx_H/dz = -rec_dxHIIdlna/(1+z)`.

HMLA og SWIFT har forskellige `rec_dxHIIdlna`-felter, så
kompatibiliteten kan ikke afgøres symbolsk ved selector-koden alene.

## Afgørelse af denne runde

Den tidligere brede blocker er nu reduceret til en konkret numerisk
certificate-test på én eksplicit kurve og kun i intervallet
`650.256650155934722..810`.

For at afgøre fortegnene universelt kræves de frosne numeriske
baggrundsværdier `H(z), nH(z)` samt HyRec rate-/SWIFT-tabellerne
evalueret på den eksplicitte overflade. Det er en defineret
implementation/execution-opgave og falder derfor uden for næste rene
symbolske skridt.

Q050 lukkes ikke.

## Point

ANALYSIS_POINTS: 40 COMPUTATION_POINTS: 5 SEARCH_POINTS: 15
VALIDATION_POINTS: 10 RUN POINTS: 70 pts TOTAL POINTS: 555 pts CYCLE
PROGRESS: 555/1000 pts NEXT SOME MILESTONE: 1000 pts POINTS TO NEXT
PUBLICATION: 445 pts NEW MILESTONES: NONE PENDING SOME PACKAGES: NONE
PUBLICATION_STATE: NOT_DUE

## NÆSTE MOTOR

**BUBBLEVERSE EXECUTION/HPC MOTOR BUILDER 2.4.0**

NEXT_TASK: Implementér og kør en source-faithful normal-certificate-test
udelukkende på `650.256650155934722 <= z <= 810`, på den eksplicitte
`F=0`-kurve og inden for det autoriserede Q050-state-domæne.

For hver reachable celle/punkt skal motoren beregne: -
`N_HMLA = dF/dz` - `N_SWIFT = dF/dz` - fortegn og intervalbound -
reachability-status - refinement omkring enhver nul-/ambiguous celle.

ACCEPTANCE: hele reachable fladen er enten unreachable eller har
certificeret kompatibel/crossing normaladfærd uden uløste celler.

REJECTION: en valideret reachable del har inkompatible one-sided
normals, som obstruerer den krævede ikke-konveksificerede continuation.

INCONCLUSIVE: mindst én reachable celle forbliver fortegnsmæssigt
uafgjort efter begrundet refinement, eller nødvendige frosne inputs kan
ikke reproduceres.

EXPECTED_OUTPUT_ARTIFACT:
`Q050_V8_PION_NORMAL_CERTIFICATE_EXECUTION_RESULT.json`

GITHUB_READ_STATE: VERIFIED GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD
