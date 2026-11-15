# BUBBLEVERSE — OVERLEVERING

**V115: Randtesten er nu beregnet og kontrolleret separat.** I den brede
intervalboks findes et punkt, hvor feltet peger ud gennem grænsen E=q/2.
Den uniforme halv-q-randtest på hele boksen holder derfor ikke.

Det er **ikke dokumenteret, at den fastlåste kosmologiske bane når punktet**.
Hovedspørgsmålet Q052 er fortsat åbent. De tidligere gyldige resultater bevares.

STATUS: FORTSÆTTER  
WORKFLOW_STATE: READY_FOR_HANDOFF  
SCIENTIFIC_STATE: INCONCLUSIVE  
TECHNICAL_STATE: PASS  
TARGET_Q: Q052; ingen senere Q anvendt.  
PROMPT_ID / VERSION: BUBBLEVERSE.MATHEMATICS / 2.3.0  
VALGT NÆSTE MOTOR: **Resultatindtag og routing 2.3.0**  
CONTINUE_SAME_Q: true

## Hvad er nyt?

Ét på forhånd valgt punkt ved z≈692,280273 er undersøgt med begge atomare
kanaler, temperaturafhængighed, fotoionisation og de præcise selectorregler.
Den primære metode og en separat Gamma-kontrol giver begge en negativ afledt.
Deres udad afrundede indhegninger er henholdsvis
[-8,952e-7; -2,401e-7] og [-8,864e-7; -2,285e-7] pr. logaritmisk skalafaktor.

Begge fælles grenpar har fortsat et betinget positivt analytisk randbidrag;
det er den blandede SWIFT/HMLA-gren, der forhindrer den uniforme halv-q-test.
Ingen nye optiske integraler, native simulationspar eller fulde baner er kørt.
Producent og separat kontrol tog samlet 1.013 sekunder
inden for grænsen på 300 sekunder. MPFR 4.2.1 blev faktisk indlæst og kontrolleret.

## Overlevering

BLOCKER_ID: LOCAL-Q052-HALF-Q-MIXED-FACE-RELAXATION-V115.
Punktets H er valgt inden for en fælles boks; dets tilhørsforhold til den præcise
Bstar-baggrund og de matchede baner er ikke verificeret.

Resultatindtag skal optage denne metodebegrænsning og forberede en ændret
matematikopgave: en svagere positiv eller variabel nedre barriere gennem
den samme celle. Den skal arve V111's start og dække begge ensidige felter.
En bestemt ny barriere er endnu ikke bevist. Gentag ikke den uændrede halv-q-test.

Den konkrete opgave med accept-, afvisnings- og stopkriterier findes i
Q052_RESULTATINDTAG_OPGAVE_V115.json. Beregninger, forbehold, kilder og den
uafhængige kontrol står i PROOF_V115.md og calc/ inde i ZIP-pakken.

## Journal, point og publicering

Den fulde leverede V114-journal er bevaret byte-for-byte som præfiks i
Q052_MATEMATIK_OG_SAMLET_JOURNAL_V115.md, efterfulgt af den nye post.
Der er ikke opfundet manglende historiske poster eller omskrevet tidligere resultater.

RUN_ID: LOCAL-Q052-V115-MIXED-HALF-Q-FACE-RECOVERY.  
PREVIOUS_POINTS_ENTRY: V114, activity_ledger.json.  
RUN POINTS: 120; TOTAL POINTS: 14215.  
CYCLE PROGRESS: 215/1000; NEXT SOME MILESTONE: 15000.  
POINTS TO NEXT PUBLICATION: 785.  
BREAKDOWN: analyse 50 + beregningsarbejde 30 + kildekontrol 10 + validering 30.  
POINTS_STATE: VERIFIED for regnskab; pointvurderingen er et redaktionelt skøn.  
PUBLICATION_STATE: NOT_DUE. Ingen nye milepæle eller udestående pakker.
M014's leveringsstatus videreføres. Genlevering, filpakning og gammel forskning giver 0 nye point.

## Setup og evidens

AKTUELT SETUP: Codex i Work Mode, Python 3.12.14, MPFR 4.2.1,
256-bit mellemregning og udadrettede binary64-intervaller. Præcist modelnavn
og reasoning-niveau er ikke verificeret. Klasse: H/C.
ANBEFALET PRIMÆRT SETUP: samme lokale matematik- og intervalsetup.
Fallback: den medfølgende kode på kompatibel Linux x86-64 med GMP og libc.
Opgradering er først relevant ved en konkret ny opgaves ressourcebehov;
arkivkontrol og eksakt algebra kræver ikke en ny simulation.

Filer, lokal kodekørsel og GitHub-læsning er verificeret tilgængelige.
Kilderne er de fastlåste CLASS/HyRec-kildebytes og V62/V77/V87/V111-artefakterne.
Ingen nye observationsdata er tilføjet. Evidensen for den lokale metodefejl
er stærk inden for relaksationen; det fulde Q052-svar kan endnu ikke afgøres.
Reproducerbarhed: R2 for dokumenteret execution, med separat algebraisk kontrol;
tabeller, interpolation og intervalprimitiver er delte afhængigheder.

GITHUB_READ_STATE: VERIFIED for journal, opgave og motoridentiteter ved
Morfindien/Bubbleverse@fa77297a6808ffd07676e30e5d907a5ad6f921c2.  
GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD. Ingen upload til GitHub er påstået.
Den strukturerede memory-update ligger i manifest115.json.

Hent begge ZIP-dele og pak dem ud i samme mappe. Hver leveringsfil er under
25.000.000 byte. De er almindelige ZIP-filer og skal ikke sammenføjes.
