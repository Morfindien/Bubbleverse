# BUBBLEVERSE --- OVERLEVERING

STATUS: FORTSÆTTER --- PEEBLES-ratiofladen er ryddet som den første
continuation-obstruktion; næste præcise interface er Pion=0.01.
WORKFLOW_STATE: ACTIVE SCIENTIFIC_STATE: INCONCLUSIVE TECHNICAL_STATE:
PASS TARGET_Q: Q050 PROMPT_ID: BUBBLEVERSE.MATHEMATICS PROMPT_VERSION:
2.3.0 RUN_ID: LOCAL-Q050-V2-PEEBLES-NORMAL-20261025

## Hovedspørgsmål

For den frosne `hillipop-ede_n3`-konfiguration og hver fast admitted
common background på `0 <= z <= 810`: tillader de eksakte source-real
low-redshift hydrogen/temperature branch-selection-regler en absolut
kontinuert continuation til `z=0` fra enhver tilstand i det validerede
`z=810`-domæne, separat for `q=xHeII=10^-6` og `q=0`, uden at ændre
eller convexify selectoren?

## Nyt resultat i V2

V1 lokaliserede den første potentielle blocker til

`g(z,y) = Tmat/Trad - T_RATIO_MIN = 0`, med `T_RATIO_MIN=0.1`.

Den frosne wrapper vælger PEEBLES ved equality:

`Trad_phys <= TR_MIN || Tmat/Trad <= T_RATIO_MIN`.

V2 kontrollerer den faktiske CLASS/HyRec-kobling. I
`thermodynamics_derivs` beregnes hydrogen-derivaten gennem den valgte
HyRec-gren, men den sene materietemperatur-ligning er ved den samme
state

`dTmat/dz = 2*Tmat/(1+z) + rate_gamma_b*(Tmat-Trad)/(H*(1+z))`

for den frosne konfiguration, fordi `has_exotic_injection=0` og
`has_idm_b=0`. `rate_gamma_b` afhænger af den aktuelle electron
fraction/state, men ikke af om hydrogen-derivaten i netop dette punkt
blev evalueret med PEEBLES eller SWIFT/HMLA.

Da `Trad = Tcmb*(1+z)`, fås

`d(Tmat/Trad)/dz = [Tmat/Trad + (rate_gamma_b/H)*(Tmat/Trad - 1)]/(1+z)`.

På selectorfladen `Tmat/Trad=0.1`:

`dg/dz = [0.1 - 0.9*(rate_gamma_b/H)]/(1+z)`.

**Afgørende:** dette udtryk er identisk fra PEEBLES-siden og
non-PEEBLES-siden ved samme state. Hydrogen-selectorens jump giver
derfor ikke modsatrettede one-sided normalfelter på denne surface.
Equality-konventionen (`<=` til PEEBLES) skaber ikke i sig selv en
instantaneous switch-back/no-solution-obstruktion i normalretningen.

Dette er et stærkere resultat end V1:
`LOCAL-Q050-PEEBLES-RATIO-SURFACE-NORMAL-V1` er ryddet som den første
præcise blocker. Det er ikke endnu et globalt continuation theorem.

## Hvorfor tangens ikke genåbner V1-blockeren

`dg/dz` kan principielt være nul, når `rate_gamma_b/H = 1/9`. Det ændrer
ikke ovenstående side-kompatibilitet: begge selectorarme har samme
temperaturkomponent ved den samme state. En eventuel tangens kræver
derfor ikke en Filippov/convexified normalretning for at forene to
modsatrettede temperaturfelter. Hydrogenkomponenten kan stadig være
diskontinuert, og dens downstream påvirkning af `x` og senere temperatur
skal behandles gennem de resterende selectorinterfaces.

V2 påstår derfor ikke uniqueness eller global regularity; kun at den
specifikke V1-obstruktion baseret på ukendt one-sided normalretning ved
`Tmat/Trad=0.1` ikke består efter source-real udledning.

## Næste præcise interface: Pion = PION_MAX

Den frosne `rec_dxHIIdlna` har for `MODEL=SWIFT` og `z<900`:

`Pion = four_betaB / (3*RLya + L2s1s + four_betaB)`

og vælger HMLA når

`Pion < PION_MAX`, med `PION_MAX=1e-2`.

Ellers fortsætter SWIFT-routingen og kan senere vælge HMLA ud fra
SWIFT-tabellens temperaturgrænse.

Dette Pion-interface er state-dependent gennem blandt andet

`RLya = LYA_FACT(1,1)*H/nH/(1-xHII)`.

Her ændres selve hydrogenkomponenten mellem HMLA og SWIFT. V2 har ikke
certificeret fortegnet af den fulde normalderivat til `Pion-0.01` på
hele den admitted surface. Derfor flyttes den første resterende
source-real continuation-gæld til:

`LOCAL-Q050-PION-SURFACE-NORMAL-V2`.

## Fixed-input checks

-   `hillipop-ede_n3` har i den frosne config `has_varconst=0`,
    `has_exotic_injection=0`, `has_idm_b=0`, `has_idm_g=0`,
    `has_idm_dr=0`, recombination=HyRec.
-   HyRec `MODEL=SWIFT`.
-   `T_RATIO_MIN=0.1`.
-   `PION_MAX=1e-2`.
-   V151-checkpointets tidligere byteverificerede SHA-256 bevares:
    `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`.
-   Source pin:
    `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
-   Bubbleverse frozen config pin:
    `Morfindien/Bubbleverse@d397732f65da2d1566089b9153a4145a605f8557`.

## Claim-strength firewall

V2 beviser **ikke**: - global AC continuation til z=0, - uniqueness, -
at Pion- eller SWIFT-grid-flader er benigne, - at alle admitted starts
følger samme selectorhistorik, - fysisk lille latch/reset-forskel.

V2 beviser på source-real ligningsniveau den mere afgrænsede påstand, at
PEEBLES temperature-ratio-selectorens to arme har samme øjeblikkelige
normal-komponent til dens egen switching surface ved en fælles state
under den frosne konfiguration.

## Termination-gate status

G1 PASS --- spørgsmål og domæne er faste. G2 PASS for V2's
PEEBLES-normalclaim --- source/config pins er identificeret. G3 PASS for
den symbolske normaludledning; PARTIAL for hele Q050. G4 PARTIAL ---
side-kompatibilitet er algebraisk, men resterende interfaces er ikke
ryddet. G5 PARTIAL --- source/call-chain cross-check udført; ingen
separat interval-verifier for Pion endnu. G6 NOT SATISFIED --- global
continuation er stadig uafgjort. G7 PASS --- V1 bevares og V2 lægges
ovenpå.

Q050 forbliver ACTIVE / INCONCLUSIVE.

## Næste forskningsopgave

Fortsæt i Matematikmotor 2.3.0 på samme Q050.

1.  Definér `p=Pion-PION_MAX`.
2.  Reducér `p=0` algebraisk med den frosne background og admitted
    `(xHII,Tmat,q)`-domain.
3.  Beregn source-faithful `dp/ds` fra HMLA- og SWIFT-siden med korrekt
    evolutionsfortegn.
4.  Certificér crossing/avoidance eller isolér en konkret obstruction.
5.  Hvis Pion ryddes, behandl SWIFT-fit temperaturinterface på samme
    måde.
6.  Først når alle reachable selectorflader er dækket, kan det globale
    AC-continuation theorem vurderes.

Sampling alene er fortsat utilstrækkeligt.

## Point- og udgivelsesstatus

PREVIOUS_POINTS_ENTRY: Q050 V1, TOTAL 110. RUN POINTS: 90 pts.
POINTS_BREAKDOWN: ANALYSIS 40 + COMPUTATION 5 + SEARCH 25 + VALIDATION
20 = 90. POINTS_BASIS: source-level symbolic normal-field derivation,
frozen-config flag verification, selector reconstruction and cross-check
against V1 blocker; heuristic editorial research counter. TOTAL POINTS:
200 pts. CYCLE PROGRESS: 200/1000 pts. NEXT SOME MILESTONE: 1000 pts.
POINTS TO NEXT PUBLICATION: 800 pts. NEW MILESTONES: NONE. PENDING SOME
PACKAGES: NONE. POINTS_STATE: VERIFIED. PUBLICATION_STATE: NOT_DUE.

## CHATGPT-SETUPVURDERING

AKTUELT SETUP: GPT-5.6 Sol med Files/Library, GitHub connector og lokal
filgenerering. ANBEFALET PRIMÆRT SETUP: samme proof-critical setup med
exact/interval arithmetic til Pion-fladen. KAPABILITETSKLASSE: H + A +
C. BEGRUNDELSE: næste gate er en endelig source-real
inequality/normal-field-certificering, ikke en observationsfit.
FALLBACK: isolér den første del af Pion-surface hvor fortegn ikke kan
certificeres og aflever et bounded proof-handoff. UPGRADE-TRIGGER: hvis
Pion-normalen ikke kan boundes med den frosne background og almindelig
intervalaritmetik. DOWNGRADE-TRIGGER: når problemet er reduceret til en
endelig liste af eksakte/interval-inequalities, kan en mindre
deterministisk verifier kontrollere certifikatet.

## GitHub/provenance

GITHUB_READ_STATE: VERIFIED for de nævnte source/config-filer.
GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD. Ingen GitHub-write eller
commit påstås i V2.

Foreslået destination: en ny versionsbestemt Q050-revisionsmappe i
eksisterende Bubbleverse-struktur; eksisterende historiske V1/Q049/Q048
records må ikke overskrives.
