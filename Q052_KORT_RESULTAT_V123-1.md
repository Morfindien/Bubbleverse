# BUBBLEVERSE — OVERLEVERING

**V123 består: Det betingede optiske interval er 1,994 % smallere. Q052 er fortsat åbent.**

STATUS: FORTSÆTTER. WORKFLOW_STATE: READY_FOR_HANDOFF.
SCIENTIFIC_STATE: INCONCLUSIVE. TECHNICAL_STATE: PASS.
TARGET_Q: Q052. AUTHORIZED_Q_RANGE: Q052. EVIDENCE_BOUNDARY: Q052 gennem V123.
PROMPT_ID: BUBBLEVERSE.MATHEMATICS. PROMPT_VERSION: 2.3.0.
VALGT NÆSTE MOTOR: BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0.

## Dokumenteret svar

Begge beregningsmetoder er eksakt enige om 1.304 nye bidrag.
Det samlede betingede kilde-reelle Thomson-interval er nu cirka
**[4,81957×10⁻⁶; 4,56102×10⁻⁵]**. Alle størrelser er dimensionsløse.
Den nedre grænse stiger med cirka 8,29899×10⁻⁷. Den øvre er uændret.

Intervalbredden falder fra cirka 4,16205×10⁻⁵ til 4,07906×10⁻⁵:
en reduktion på **1,993968 %**. Den er stadig cirka **10.197,65 gange**
det foreløbige breddekrav 4×10⁻⁹. Det krav er ikke opfyldt.
Reduktionen beskriver vores indhyllingsinterval, ikke en målt ændring
i universet eller selve den fysiske optiske dybde.

Det oprindelige hovedspørgsmål er stadig:

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

V123 besvarer kun den afgrænsede kildeoptiske deltest. De faktiske
native CLASS/P6-baner, deres sammenhæng med kildebanerne og deres
samlede validerede numeriske fejl er fortsat åbne afslutningskrav.

## Beregning, input og kontrol

På [50; 1523417340748759/2199023255552] anvendes de tidligere
certificerede E>q/16-grænser fra V121/V119/V117, q=10⁻⁶ og
de originale positive V66-vægte. Hvert bidrag er
L=floor(2¹⁰⁰·W_l·q/16·((1+c)³−(1+a)³)/3)/2¹⁰⁰.
1.292 vægtrækker bliver til 1.304 delstykker fordelt over 13 bins.
V111's gamle strimmel berøres kun i ét fælles endepunkt og tælles
ikke igen. Alle øvre grænser og fire uberørte bins er bevaret.

Den separate kontrol bygger selv partitionen, traverserer baglæns
og bruger et faktoriseret masseudtryk med heltalsafrunding.
Alle geometrier, uafrundede/afrundede bidrag og globale summer matcher.
Kørslernes samlede wall-tid er 1.070418 sekunder.
Samlet afrundingstab er cirka 5,17×10⁻²⁸; den resterende bredde
skyldes indhyllingerne, ikke dette afrundingstab.

Resultatet er betinget af samme kilde, fælles baggrund B★,
matchede z810-starter og arvede banebeviser. Der er ingen nye
vægtberegninger, dynamiske integrationer eller native par.
R3 dækker den lokale aritmetiske deltest med to implementationer;
fælles arkivforudsætninger og Python Fraction er ikke uafhængig
empirisk evidens. G1 og de lokale G2–G5/G7 er opfyldt; G6 er åben.
MODEL_DIFF: NONE.

## Aktuel overlevering

BLOCKER_ID: LOCAL-Q052-SOURCE-OPTICAL-PRECISION-AND-NATIVE-CERTIFICATE.
Næste motor skal optage dette nye resultat og forberede én ændret
matematiktest ud fra den resterende intervalbredde. Største bin er
z=600–650. Den næste kontrakt skal skelne mellem vægtindhyllingens
og elektronindhyllingens bidrag og fastlægge en gyldig starttilstand,
metode, kontrol, dækningskrav og stopgrænse før ny beregning.

Opgaven står i `Q052_RESULTATINDTAG_OPGAVE_V123.json`. Accept kræver konsistente hashes,
eksakte receipts, uændret præfiks og korrekt støtte uden overlap.
Et domænebrud, dobbeltregning eller uforenelig sum afviser den
berørte opdatering. Manglende nødvendige input giver INCONCLUSIVE
eller en konkret blokering. Ingen af de gennemførte V123-metoder
skal genkøres på uændrede inputs. Genoptagelse kræver blot denne
pakke i Resultatindtagsmotoren. Næste opgave er forberedt, ikke udført.

## Samlet journal og proveniens

`Q052_MATEMATIK_OG_SAMLET_JOURNAL_V123.md` indeholder hele den leverede V122-journal i uændrede
bytes og én ny V123-post. ZIP-filen indeholder beviset `PROOF_V123.md`,
kode, begge receipts, execution, validator, frosne inputhashes,
ledger, kildeoversigt og den originale V122-pakke.

GitHub-base: `3a588f12b301237f9566a1f6dfeaec38ca98026b`. Alle fem vedhæftede inputs matcher
repositoryets bytes. Fysikkilde: `5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
Capture: `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`.
Baggrund: `Q050-COMMON-BACKGROUND-92de319899bf911563aff4d1`.
Kilder K1–K5 og claim-evidens står i `source_register123.json`.
GITHUB_READ_STATE: VERIFIED. GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD.
Upload de fire nye V123-filer til roden efter den eksisterende
navngivning; tidligere versioner bevares. Ingen GitHub-upload er udført her.

## ChatGPT-setupvurdering

AKTUELT SETUP: Codex i Work Mode, Default, lokal Python-standardpakke,
filer og verificeret GitHub-læsning. Det præcise modelnavn og
reasoning-niveau er ikke eksponeret. ANBEFALET PRIMÆRT SETUP:
samme tilgængelige runtime til indtag. KAPABILITETSKLASSE: H/C/A.
Begrundelse: endelig rationalaritmetik og arkivkontrol kan udføres her.
Fallback: gemt evidenskontrol og konkret inputblokering.
Upgrade-trigger: en næste native/banetest kræver en faktisk build-
eller valideringskapabilitet, der mangler. Downgrade-trigger:
frosne inputs kan behandles med almindelig standardbibliotekskode.
Ingen agenter, modelskift eller HPC er anvendt. Kontraktfelter og
referencer er lokalt kontrolleret; ingen ekstern schema-validation hævdes.

## Point og udgivelse

RUN_ID: `LOCAL-Q052-V123-Q16-SIGNED-OPTICAL-LOWER-50-TO-BRIDGE`. PREVIOUS_POINTS_ENTRY: `Q052-ACTIVITY-Q16-PHASE5-OPTICAL-INTAKE-V122`.
RUN POINTS: **100** (analyse 35, beregning 25, kildesporing 5, validering 35).
TOTAL POINTS: **14.880**. CYCLE PROGRESS: 880/1000.
NEXT SOME MILESTONE: 15.000. POINTS TO NEXT PUBLICATION: **120**.
POINTS_STATE: VERIFIED. PUBLICATION_STATE: NOT_DUE.
NEW MILESTONES: NONE. PENDING SOME PACKAGES: NONE.
M001–M014 er videreført som leveret. Point er en redaktionel tæller,
ikke et mål for bevisstyrke eller procentvis færdiggørelse.

Redaktionelt skøn: bevis for additiv opdatering uden overlap, én eksakt 1304-stykkers sum og én separat omvendt konstruktion, GitHub/inputidentitet samt eksakt sammenligning af bidrag, bins, bevarede grænser og afrunding. Ingen nye point for V121-feltbevis, V122-geometriforberedelse, historiske integralbidrag, arkivpakning eller genlevering.
