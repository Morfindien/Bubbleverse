# BUBBLEVERSE — OVERLEVERING

**Q052 · V117 · Matematikmotor 2.3.0**  
STATUS: FORTSÆTTER  
WORKFLOW_STATE: READY_FOR_HANDOFF  
SCIENTIFIC_STATE: INCONCLUSIVE for hovedspørgsmålet  
TECHNICAL_STATE: PASS  
Lokalt resultat: SUPPORTED_WITHIN_TESTED_DOMAIN, betinget af de fastlåste forudsætninger.

**Den nye q/16-grænse består.** På hele cellen fra z=692,77 ned til
z≈692,2725 holder elektronforskellen sig strengt over
**q/16 = 6,25×10⁻⁸**, under de nedarvede kilde-, baggrunds- og baneforudsætninger.

| Kontrol | Resultat |
|---|---:|
| Primær normaliseret indadrettet margin | >3,7378×10⁻⁵ |
| Separat helcellemargin | >1,1917×10⁻⁵ |
| Lukkede delintervaller | 16 af 16 dækket |
| Blandet grenvalg | 5 dækket; 11 strengt udelukket |
| Nye native par / optiske evalueringer / integrationer | 0 / 0 / 0 |

Marginerne gælder E′/|f_R| på kontaktfladen. De er **ikke** en beregnet
afstand over q/16 ved slutpunktet. De eksakte brøker, ensidige grenfelter,
forudsætninger og det fulde Saha-bevis findes i `PROOF_V117.md` og
`result117.json` i ZIP-filen. Der er udført én primær test og én separat
numerisk kontrol samt 16 eksakte algebraiske checks.

## Hvad er stadig åbent?

Hovedspørgsmålet kræver, at de faktiske native CLASS/P6-historier kan
dokumenteres med deres samlede numeriske fejl og kobles til de fastlåste
kildeligninger. Det er ikke afgjort her. Der er ikke beregnet nye globale
værdier af sup|Δx_e| eller sup|Δτ_T|, og q/16-grænsen er endnu ikke
kontrolleret under cellens nedre endepunkt. Tidligere gyldige resultater
og V115's halv-q-metodebegrænsning bevares.

## Aktuel overlevering

NÆSTE MOTOR: **Resultatindtag og routing 2.3.0**.  
BLOCKER_ID: LOCAL-Q052-Q16-CONTINUATION-BELOW-ROW234.  
Den fastlagte V116-stopregel er nået. Optag dette afgrænsede bevis og
forbered én matematikopgave for q/16 på de efterfølgende V62-rækker
235–244 med V89's arkiverede selectorarbejde som grundlag. Næste opgave
skal kontrollere nye projektioner, hele domænet og begge ensidige felter.
Den må ikke genkøre V117 eller V115 på uændrede input.

Den præcise kontrakt står i `Q052_RESULTATINDTAG_OPGAVE_V117.json`. Den er forberedt,
ikke udført. Godkendelse af en bredere grænse kræver et nyt bestået
matematisk certifikat. Et manglende input eller en utilstrækkelig margin
skal fastholdes som en konkret usikkerhed.

## Journal, point og udgivelse

Den fulde indgående V116-journal er bevaret byteidentisk som præfiks i
`Q052_MATEMATIK_OG_SAMLET_JOURNAL_V117.md`; den nye post er tilføjet bagefter.
TARGET_Q er Q052; evidensgrænsen er Q052 til og med V117.

RUN POINTS: **110**; TOTAL POINTS: **14365**.  
CYCLE PROGRESS: 365/1000; NEXT SOME MILESTONE: 15000.  
POINTS TO NEXT PUBLICATION: **635**.  
POINTS_STATE: VERIFIED; PUBLICATION_STATE: NOT_DUE; PENDING PACKAGES: NONE.

Fordeling: analyse 50, beregning 20, kildekontrol 5, validering 35.
Det er et heuristisk redaktionelt skøn over det nye arbejde, ikke målte
credits eller et mål for hvor tæt hovedspørgsmålet er på at være løst.
Gamle beregninger og pakning er ikke talt igen. M014 er registreret leveret.
RUN_ID: `LOCAL-Q052-V117-CONSTANT-Q-OVER-16-CELL235`. Forrige pointpost: V116 /
Q052-ACTIVITY-WEAKER-BARRIER-INTAKE-V116. Ledger: `activity_ledger117.json`.

## ChatGPT-setupvurdering

Aktuelt setup: Codex Work Mode med lokal Python, MPFR 4.2.1, eksakte
brøker, SymPy og GitHub-læsning. Kapabilitetsklasse: H/C/A.
Modelvariant og et særskilt reasoning-niveau er ikke eksternt verificeret.
Ingen subagenter eller ekstern HPC er brugt. Det samme setup anbefales
til næste afgrænsede intervaltest; det er tilgængeligt her. Ved et
uforeneligt runtime skal den pakkede Linux-version bruges i et
kompatibelt miljø. Opgradering er kun relevant, hvis en konkret
domæne-/kontrolfejl kræver en anden metode; verificerede cachetal
genbruges, når de er tilstrækkelige. En anbefaling er ikke en ny kørsel.

## Provenance og levering

Fysikkilden er [class_ede@5a131c9](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c).
V116-filer og motoridentiteter er verificeret på
[Bubbleverse@b0b7cd5](https://github.com/Morfindien/Bubbleverse/tree/b0b7cd5b02177e24a7e536901c1b791a6dfb0edb).
GITHUB_READ_STATE: VERIFIED for disse identiteter.
GITHUB_WRITE_STATE: **READY_FOR_MANUAL_UPLOAD** for V117; ingen upload påstås.

ZIP-filen rummer bevis, fuld journal, overlevering, input, kode, runtime,
resultater og kontroller. Den numeriske reproduktion kræver ikke de gamle
V115 ZIP-dele. Kør `python reproduce117.py` efter udpakning i et kompatibelt
Linux-miljø. Den portable wrapper er syntakskontrolleret og ikke genkørt
i denne runde. Alle leverede filer er under 25.000.000 bytes.

Kontraktfelter og JSON er kontrolleret lokalt; der påstås ingen validering
mod et centralt schema. Hovedspørgsmålets termination gate er ikke opfyldt.
Der er ingen ændring af accepteret fysisk model.
