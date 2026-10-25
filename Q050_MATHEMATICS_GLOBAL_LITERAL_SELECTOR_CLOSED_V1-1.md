BUBBLEVERSE — AFSLUTTET SAG

STATUS: AFSLUTTET
WORKFLOW_STATE: CLOSED
SCIENTIFIC_STATE: RESOLVED_WITHIN_SCOPE
TECHNICAL_STATE: PASS
TARGET_Q: Q050
AUTHORIZED_Q_RANGE: Q001–Q050, with clean Q050 lineage and only the inherited frozen Q048/Q049 dependencies explicitly carried into Q050
PROMPT_ID: BUBBLEVERSE.MATHEMATICS
PROMPT_VERSION: 2.3.0
RUN_ID: LOCAL-Q050-MATHEMATICS-GLOBAL-LITERAL-SELECTOR-CLOSURE-20261025-V1
TASK_ID: LOCAL-Q050-GLOBAL-LITERAL-SELECTOR-EXTENSION-CLOSURE-V1
UTC: 2026-10-25T05:25:53+00:00
EUROPE/COPENHAGEN: 2026-10-25T06:25:53+01:00
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
QUESTION_SHA256: 11af5cf58d6c94e34a050e9672a76e47d277c0fcaec14e9acbcf58e96eb22b01

NÆSTE DESTINATION: BV-M14-UNIVERSAL-REVISION 8.0.0 — CLOSED_CASE_REVISION
MOTOR14 STATE: PREPARED_NOT_DISPATCHED

# Dokumenteret svar

**JA — inden for Q050's præcise betingede scope.**

For hver **fast admissibel common background** på `0<=z<=810`, for hver af de to frosne heliumtilstande
`q=xHeII=10^-6` og `q=0`, og fra **enhver tilstand i det validerede z=810-domæne**, eksisterer der mindst én absolut kontinuert Caratheodory-fortsættelse af de **bogstavelige source-real hydrogen/temperatur branch-selection rules** helt til `z=0`.

Selektoren er ikke ændret, glattet, konveksificeret eller erstattet med en Filippov-regel.

Dette er et **eksistensresultat, ikke et entydighedsresultat**.

# Eksakt spørgsmål

For the frozen hillipop-ede_n3 configuration and each fixed admitted common background on 0 <= z <= 810, do the exact source-real low-redshift hydrogen/temperature branch-selection rules admit an absolutely continuous continuation to z=0 from every state in the validated z=810 domain, separately for q=xHeII=10^-6 and q=0, without changing or convexifying the selector?

# Matematisk resultat

Sæt
`t = ln(811/(1+z))`, så `t` vokser mod fremtiden og `t in [0,T]` med `T=ln(811)`.
Tilstanden er `y=(h,v)`, hvor `h=xHII` og `v=Tmat/Trad`.

Den globale lukning følger af fem dele.

## G1 — branchfelterne er source-defined og lokalt regulære

På det allerede dokumenterede sikre domæne er PEEBLES-, HMLA- og SWIFT-felterne endelige og lokalt Lipschitz i state væk fra selectorfladerne.

De frosne atomic-rater interpoleres med endelige stykvise kubiske interpolationer på deres lovlige tabeldomæner. Den arvede SWIFT-kontrol giver `1+DK>0` med positiv margin. De generaliserede C-faktor-denominatorer er positive. Den faste admissible background har `H>0` og `nH>0`.

Den native faktor `1/(1-h)` kræver særskilt omtanke. De arvede branchwise hydrogenbarrierer har en endelig source-real grænse ved `h->1-` og peger strengt nedad dér. Fordi der kun er finit mange aktive branches og tiden/state-tuben er kompakt, findes et fælles nabolag `h>=1-eta`, hvor alle branches stadig peger nedad. Med startgrænsen `h<=99999/100000` følger derfor en uniform
`h<=H_*<1`.
Den faktiske continuation behøver således aldrig evaluere den native division ved `h=1`.

## G2 — alle material state-selector gates har lokal literal eksistens

Ved almindelige punkter bruges den klassiske branch-IVP.

Ved Pion-overfladen er den tidligere korrelerede source-real certificate og den formelle literal-selector lemma allerede etableret:
`L_HMLA F < 0 OR L_SWIFT F > 0`
giver en lokal Caratheodory-løsning uden convexification.

Ved PEEBLES-forholdet `v=1/10` er ikke-tangente punkter dækket af den fælles ikke-nul normal. Den eneste tidligere åbne specialcase var
`A=rate_gamma_b/H=1/9`.
Den nu ingested HPC-certificate viser på hele den materielle tangentstribe og for begge q:
`v_uu < -1/10`.
Da equality bogstaveligt tilhører PEEBLES, går PEEBLES-løsningen kvadratisk ind i sin egen side `v<1/10`.

De to state-interfaces kan ikke danne et manglende simultaneous corner:
- reionization start: `z=11.498794555664`
- `TR_MIN` forced PEEBLES: `z≈16.031010835587`
- PEEBLES tangent kan kun være materiel op til `z=4006/49≈81.755102040816`
- SWIFT-fit 1775 K begynder ved `z≈650.256650155935`.

Så PEEBLES-ratio-problemet ligger langt under det z-område, hvor Pion HMLA/SWIFT-state-skiftet er materialt.

## G3 — a-priori invariant tube for hver allerede eksisterende lokal del

Det arvede Q049-argument bruges **ikke** som et skjult globalt eksistensbevis. Det bruges kun som et a-priori first-exit-estimat på hver lokal løsning, efter lokal eksistens allerede er etableret.

Hydrogenbarriererne holder `h` inde i `[0,H_*]` med `H_*<1`.

Temperaturfeltet i future-log-scale har formen
`v'=-v+beta(1-v)`, `beta>=0`.

Med den bevægelige nedre barriere `m(t)=0.98 exp(-t)`:
- ved `v=m(t)<=1` gælder `v'>=-v=m'`;
- ved `v=1.000001` gælder `v'<0`.

Dermed
`0.98 exp(-t) <= v(t) <= 1.000001`.
På hele intervallet fås den strikte globale undergrænse
`v >= 0.98/811 = 49/40550 ≈ 0.001208384710234 > 0`.

Atomic/HMLA/SWIFT lookup-koordinater forbliver derfor i deres dokumenterede domæner, når de branches vælges; udenfor disse domæner vælger wrapperen PEEBLES efter de frosne kildegrænser.

## G4 — Zeno/switch-akkumulation kan ikke stoppe eksistensen

På den kompakte sikre tube er hver af de finit mange source branches begrænset. Lad `M<infinity` være et fælles bound.

Enhver literal løsning opfylder derfor
`|y'(t)|<=M` næsten overalt og er M-Lipschitz.

Antag at en maksimal løsning stopper ved `tau_*<T`, eventuelt fordi uendeligt mange selector-skift akkumulerer ved `tau_*`.
Lipschitz-boundet gør `y(t)` Cauchy, så
`y_* = lim_(t->tau_*-) y(t)`
eksisterer.

Invariant-tuben er lukket i de relevante state-variable, og den strikte hydrogenafstand til `h=1` bevares. Derfor er `y_*` stadig admissibel og source-defined.

Men G1/G2 giver en ny lokal literal løsning fra `(tau_*,y_*)`, også hvis punktet ligger på en selectorflade eller en fast tidsgrænse. Den kan concatenates med den gamle løsning. En mulig RHS-mismatch i selve enkeltpunktet `tau_*` er measure-zero under Caratheodory-semantik.

Det modsiger maksimalitet. Altså kan ingen maksimal løsning stoppe før `T`.

Dette argument dækker samtidig en egentlig Zeno-sekvens af switches; der kræves ikke et positivt minimum mellem switches.

## G5 — fixed-time dispatch og reionisering er ikke en ny blocker

`hydrogen.c` bruger fortsat `x_noreio=h+q` til hydrogen-rekombinationsfeltet.

Temperaturfeltet bruger `x_reio`. For den frosne `reio_camb`-map er
`x_reio` over startredshiften lig `x_noreio`; under startredshiften er den en bounded affine funktion af `xe_before=h+q` plus den frosne positive tanh-heliumterm.

Det giver et bounded, measurable time-dependent temperaturfelt og lokal Lipschitz state-afhængighed på hver side. En eventuel forskel præcis ved den faste starttid er et enkelt tids-punkt og ændrer ikke Caratheodory-ligningen næsten overalt.

Desuden ligger reioniseringsstart under `TR_MIN`-grænsen, hvor hydrogenwrapperen allerede er forced PEEBLES. Der opstår derfor intet nyt samtidig hydrogen-selector-corner.

Det samme concatenation-argument gælder de andre faste time/background dispatch-grænser, herunder 1775 K SWIFT-fit-grænsen og `TR_MIN`.

# Global maximal-extension konklusion

Start med en vilkårlig valideret z=810-state og et fast q.

Lokal eksistens gør mængden af forward literal solutions ikke-tom. Tag en maksimal extension.

Hvis dens højre endpoint var før `T=ln811`, ville G3 holde den i den sikre tube og G1 give et uniformt finite branchbound. Derfor har den en endpoint-limit. G2/G5 giver lokal continuation fra limitpunktet. Det modsiger maksimalitet.

Endpointet er derfor `T`, som svarer til `z=0`.

Q050's eksistensspørgsmål er dermed besvaret **JA** inden for det frosne betingede scope.

# Antagelser og claim firewall

Resultatet forudsætter:
- præcis den frosne `hillipop-ede_n3` source/configuration;
- en **fast admissibel common background** som Q050 kvantificerer over;
- den validerede z=810 startdomæne-definition;
- den bogstavelige source selector og dens equality-semantik;
- de allerede validerede Pion- og PEEBLES-local certificates.

Resultatet beviser ikke:
- uniqueness af continuationen;
- eksistensen af common backgrounden selv;
- at alle theorem-domain starts er kosmologisk reachable;
- native/P6 trajectory identity;
- en ny observeret rekombinationshistorie;
- empirisk confirmation/falsification af Bubbleverse eller standardkosmologi.

# Validering

Machine certificate: `Q050_GLOBAL_LITERAL_SELECTOR_EXTENSION_CERTIFICATE_V1.json`.
Structural/semantic validator: `q050_global_extension_validator_v1.py`.
Validation receipt: `Q050_GLOBAL_LITERAL_SELECTOR_EXTENSION_VALIDATION_V1.json`.

Validator:
- 10/10 checks PASS;
- 7/7 indispensable-premise mutation controls rejected.

Validatoren er en strukturel/semantisk kontrol af proof-contracten, ikke en uafhængig generel teoremprover. Den matematiske evidens er derfor stærk inden for det dokumenterede betingede source-real scope, men ikke en uafhængig menneskelig reproduktion.

# Kilder og provenance

Pinned source:
`mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.

Kontrollerede source-objekter:
- `wrap_hyrec.c` `fa44c774cf1fc7dbf6185e01980764f7eb260204`
- `hydrogen.c` `233f174bfb1758fa910866310340ae1bfad703db`
- `hydrogen.h` `088b34a699efe5d6d3aefb158229e9fb83d9a586`
- `hyrectools.c` `5e8ac170fe7839ef391de0b129113c4a7a71af1e`
- `fit_swift.dat` `fd0cfa4f380d30640c4b2da47e4e35d6894b4dcb`
- `thermodynamics.c` `c1683f56b43e0f2ec24a8ba6120133f604cb947c`
- `background.c` `5f6be0fc77c31bd81198d9f28a9d73690a2baabd`.

Bubbleverse repository was reverified read-only at
`main@84962f18ead6a43185b94401dc172a31a97fa7d2`,
tree `e71bb88cb1b50affa1e9051b452814f06e8757c8`, 4580 entries, nontruncated.

The current ingestion journal, ledger, global Mathematics task, audit and handoff were already present on that main snapshot when this run began.

No GitHub write, PR, merge or workflow dispatch was performed by this Mathematics run.

# Point- og SoMe-status

RUN COST: 180 pts
TOTAL WORK POINTS: 1800 pts
SOME INTERVAL: 1000 pts
CYCLE PROGRESS: 800/1000 pts
NEWLY CROSSED SOME MILESTONES: []
NEXT SOME MILESTONE: 2000 pts
POINTS TO NEXT SOME MILESTONE: 200 pts
SOME PACKAGE STATUS: existing `Q050-SOME-M001` READY; preserve, no duplicate/regeneration
EXTERNAL PUBLICATION: NOT_REQUESTED_NOT_POSTED

Point breakdown:
- ANALYSIS: 90
- COMPUTATION: 10
- SEARCH: 40
- VALIDATION: 40
- TOTAL: 180

Alle tidligere 1620 point er arvet én gang. Ingen tidligere Pion-, PEEBLES-, background-, ingestion- eller HPC-charge er genfaktureret. Point ændrer ikke den videnskabelige konklusion.

# Model diff

MODEL_DIFF: NONE.

Q050 etablerer en conditional existence theorem for den frosne literal selector. Det ændrer ikke den accepterede kosmologiske model, parametre eller Q048's historiske uløste native-history-status.

# SAMLET JOURNAL og næste destination

Den komplette successor-journal er:
`Q047_SAMLET_JOURNAL_Q050_GLOBAL_LITERAL_SELECTOR_CLOSED_V1.md`.

Alle indgående `Q047_SAMLET_JOURNAL_Q050_PEEBLES_TANGENCY_INGESTED_V1.md`-bytes bevares som eksakt prefix; denne Mathematics-run tilføjer kun én ny closure-post.

Q050 skal nu **ikke** sendes til endnu en videnskabelig solver. Næste destination er
`BV-M14-UNIVERSAL-REVISION 8.0.0` i `CLOSED_CASE_REVISION` mode til global knowledge revision og valg af næste Q.

Motor 14 er forberedt, men ikke kørt i denne Mathematics-levering.
