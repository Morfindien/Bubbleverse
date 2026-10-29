# Q052 V24 — anden celle består med videreført fejl

**Betinget PASS i begge arme. De første to celler er nu sammenkædet med et valideret, ikke-nul fejlbudget. Hele Q052 er fortsat ACTIVE / INCONCLUSIVE. Næste motor: Result Ingestion & Routing 2.3.0.**

Dato: 2026-10-29T10:16:47.157388+01:00 (Europe/Copenhagen). UTC:2026-10-29T09:16:47.157388+00:00. Run:`LOCAL-Q052-SECOND-CELL-CONTINUATION-20261029-V24`. CASE:LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1. CURRENT_Q=TARGET_Q=Q052. Den vedhæftede Execution/HPC/Motor-builder2.4.0-prompt er byteidentisk med den allerede verificerede prompt, SHA256 `5e97deb69af1e16192c5130820a484fa7839378f9d5ada7d682ae5700c01b47d`.

## Det præcise spørgsmål

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

## Faktisk resultat

Den nye celle er z=`0x1.94d75c28f5c29p+9`→`0x1.9497ae147ae14p+9`, cirka809.6825→809.185. V22’s øvre slutfejlvektor er videreført som indgang i hver arm. Sammenføjningen af de eksakte h/D-rekonstruktioner og den eksakte v-konvertering giver mismatch(0,0). Begyndelsesfejlen er **ikke nulstillet**.

| Arm | h-slutfejl højst | v-slutfejl højst | h-fejl på hele celle2 højst | v-fejl på hele celle2 højst |
|---|---:|---:|---:|---:|
| L | 3.679309e−5 | 1.765865e−4 | 3.714058e−5 | 1.782543e−4 |
| R | 3.679011e−5 | 1.765851e−4 | 3.713748e−5 | 1.782524e−4 |

Tabellen er afrundet opad. Receiptets eksakte rettede hex-endpoints er autoritative. De normaliserede hele-celle-lofter er L:(0.9285142566763951,0.35650848246895284) og R:(0.9284368714847318,0.35650462919253373), alle strengt under1. De gælder de på forhånd fastlagte radier h=4e−5,v=5e−4.

Resultatet giver en betinget sammenkædning fra z=810 til809.185. De nye fejlbudgetter er større end første celles, fordi de omfatter akkumulation. Det er forventeligt og ændrer ikke V22’s tidligere resultat. Det er ingen påstand om nøjagtigheden af hele den native historiestrækning.

Tallene begrænser den definerede Hermite-rekonstruktions afvigelse fra den betingede kilde-real løsning. Rekonstruktionen er ikke den native integrators dense output. Positive intervaller omkring sammenligningsudtryk er ikke positive nedre grænser for faktisk fejl. Faktisk absolut fejl ligger mellem0 og det relevante øvre endpoint. Forskellen mellem L/R-fejlbudgetter er ikke et fysisk L−R-signal.

## Hvad blev udført?

Der blev beregnet64nye rationale x-underceller per arm med deres faktiske ikke-uniforme u-bredder,128i alt. Den oprindelige V20-feltkode blev genbrugt på de **nye** kurve-/rørdata; dens gamle producent/main blev ikke kørt. V22’s sammenlignings-/matrixfunktioner blev genbrugt på de nye defekt-/Jacobianintervaller. Der er256nye feltkald og ingen førstecelle-feltkald.

Det faste V23-radiepar,256bit MPFR4.2.1,RNDD/RNDU,rettet binær64-eksport og matrixgrad16 er uændrede. h-radius var allerede fordoblet i V23-kontrakten før denne beregning. Der er ingen efterfølgende radius-/gitter-/præcisionssøgning og ingen udviklingsfejl eller ændret spec. Spec-SHA256:`9991551bd82d9db6a219fbbeedd39c70baaad2ee567ac672761b5b5ed85a351a`.

Nye hele-rør- og undercellechecks kvalificerer samme cold/SWIFT-gren. Pion er over0.2030556, v er under0.999773574, rate-stencils er dækket, og relevante rater/denominatorer er positive. C-faktorernes1+DK>0 er fortsat den oprindelige **arvede betingelse**; et native DK-interval er ikke opfundet. Samme faste eksisterende admitted B, samme q-parametre og de samme kildekonstanter bruges gennem begge celler. H-projektionen fra den oprindelige kildecelle810..800 dækker det nye domæne.

Den fortegnsbevarede termiske diagonal og uvægtede defektlofter bruges i den affine transport. V22’s hele-undercelle-argument kontrollerer alle mellempunkter gennem en koefficientvis majorant; der er ikke kun kontrolleret endepunkter. Den største Taylor-rest er under1.715e−49 og indgår i intervallerne. Q052_SECOND_CELL_APPLICATION_NOTE_V24.md forklarer den konkrete sammenkædning og dens forudsætninger.

## Validering og dens grænse

Alle **otte nye tests** bestod med0fejl,0errors og0skip. De kontrollerer ny celle-/fejlbinding, selvstændig eksakt power-basis-geometri og v-afledte, hele domænet/rater/denominatorer, rationelle termiske punktværdier, signed-diagonal/uvægtet forcing, eksakte tidsbredder, alternativ matrixaritmetik, faktisk ikke-nul komposition og streng afvisning ved lighed/nulstilling/beskadiget input.

Den alternative kontrol omfatter128logaritmeintervaller,136ushiftede rationelle matrixpunkter med1224elementkontroller,128eksakte rationelle termiske RHS/Jacobianpunkter og384kurve-/afledt-punkter. De gamle oracle-funktioner er genbrugt på nye data. De gamle testsuiter er ikke genkørt. Antal punkter/intervalposter er ikke et antal uafhængige videnskabelige eksperimenter.

Punkt-oracles understøtter aritmetikken; de erstatter ikke det hele-tids-bevis, som allerede er begrundet i V22. Samme forfatter og oprindelige kildepræmisser begrænser uafhængigheden. Der er ingen ekstern reviewer, formel teoremprover eller uafhængig native reproduktion. Reproducerbarhedsgrad:R2 for denne afgrænsede beregning.

Producenten tog18.052939s inklusive input/initialisering og beregning. De nye tests tog1.656299s. Python3.12.14,MPFR4.2.1,lokal runtime. Dette ligger inden for den tidligere grove kerneprognose10–120s; samlet tilpasning/filaflevering er ikke målt computetid. Peak-RAM, priser og eksterne køtider er ikke målt. Ingen GitHub-workflow, ny native CLASS-kørsel, refit, tau-shooting eller betalt compute er startet.

## Betydning for hele Q052

`conditional_second_cell_certificate=true` og `conditional_first_two_cell_chain_certificate=true`, med de angivne præmisser. `source_real_certificate=false`, `native_background_membership_certified=false` og `full_q052_gate=UNRESOLVED`. Globale r/beta/native_a/E0/L og realiserede sup|Delta xe|/sup|Delta tau| forbliver null.

Det er stadig uafklaret, hvordan den faktisk native beregning opfylder de nødvendige baggrunds-/anvendelighedsforpligtelser. Resten af domænet, events, smoothing og observerbar overførsel/integration/suprema mangler. Dette arbejde beviser ikke familiens ikke-tomhed eller en native pre810-fejlgrænse. Ingen ny empirisk anomali eller accepteret modelændring er konstateret. Tidligere fejl og metode-INCONCLUSIVE bevares historisk.

## Næste motor

Returnér én gang til [Result Ingestion & Routing2.3.0](https://chatgpt.com/library?file_id=libfile_9d002c0c58648191a0c5f2170b951be2&account_id=personal). Promptens eksisterende bytes er verificeret med SHA256 `b75a691938076af695cbe67b00726732eb2d16edbedc9810f9a9c3bcc7dca9c8`. Status:PREPARED_NOT_SENT. Motoren skal indtage de faktiske V24-resultater og point én gang og vælge én nødvendig, afgrænset næste forpligtelse ud fra det opdaterede fejlbudget og de åbne native-/domæne-/observablekrav.

Der er ikke bestilt en automatisk celle3-kørsel eller hel domænekampagne. En senere celle kræver sin egen kvalifikation og nye koefficienter, faktisk videreført slutfejl og valideret mismatch. De nye radier/matricer må ikke kopieres blindt. Der er heller ikke grundlag for at genkøre denne uændrede celle, gentage det generelle transportbevis eller lukke Q052 til Motor14.

## Filer, journal og GitHub

De tre vedhæftede V23-hovedfiler matcher [main@9b1e6bc53490](https://github.com/Morfindien/Bubbleverse/commit/9b1e6bc5349041d63800e6ea1da30b867e0bc3d7). V23-hovedfilerne er dermed nu observeret uploadet. Det komplette træ viste ingen V24,CURRENT_STATE eller AGENTS; README og programregistry har de tidligere verificerede, uændrede blobs. Denne opgave kræver ingen launcherændring.

Hele den vedhæftede V23-journal er bevaret som uændret præfiks:128928bytes,SHA256 `70757cfd247828049f7ce2aa1f56d8bf33033510937469c9a9bc5db6dda53a13`. Samme ledger videreføres med alle23gamle entries og tre milepælsrecords. Kilder, gamle resultater, rå logs og beviser er fortsat recoverable via den allerede leverede [V23-inputpakke](https://chatgpt.com/library?file_id=libfile_a0fd0504114c8191a6389fcc1cf9d141&account_id=personal), SHA256 `81a65513251251770650dfcb22caf1e11b4bded1f48d76feac38e00b99df623f`. Ingen af de historiske videnskabelige records overskrives.

Upload alle nye V24-filer til repository-roden efter kollisionskontrol på aktuel main. Bevar gamle versioner. Flyt først aktuelle Q052-pointere til V24-journal/resultat/handoff/indeks, når de sammenhængende filer og afhængigheder findes. Handoffet indeholder den konkrete memory-delta. V24 er USER_UPLOAD_PENDING; der er ingen ny commit,PR,registryændring eller dispatch. MEMORY_BACKEND:GITHUB;lokal udførelse er uafhængig af repository-synkronisering.

## Point og stop

RUN POINTS:240. **TOTAL:3760=3520+240.** Næste SoMe-milepæl4000,afstand240. Ingen ny SoMe-pakke. M001/M002/M003 er allerede leveret og bevares; ekstern posting er ikke verificeret. Fordeling45analyse/kontrakt,85nyadapter/beregning,30provenance,80validering. Det indledende240-estimat fastholdes. Point er en grov aktivitetstæller, ikke penge, beregningstid, evidensstyrke eller en forskningsgrænse. Gammelt arbejde og fil-/syncarbejde er ikke talt igen.

Den afgrænsede task er færdig, og dens obligatoriske checks er bestået. Ingen ekstra test eller genkørsel er nødvendig uden en konkret ny grund. Næste indtagelsesmotor er klargjort, ikke startet. START_STATUS:NOT_APPLICABLE_DIRECT_LOCAL_COMPLETED.

## Reproduktion ved et konkret behov

Brug de leverede kode-/specfiler og den eksisterende V23-inputpakke. Kilde-/matrix-/backendbytes findes i pakken og kræver ingen manuel samling. Python3,MPFR4.2.1 og samme platformforudsætninger skal være tilgængelige. Skriv nye replay-filer og bevar originalerne:

```bash
python q052_second_cell_v24.py --bundle Q052_SECOND_CELL_EXECUTION_INPUTS_V23.json --output replay_receipt.json
Q052_BUNDLE=Q052_SECOND_CELL_EXECUTION_INPUTS_V23.json Q052_RESULT=replay_receipt.json Q052_TEST_SUMMARY=replay_test_summary.json python test_q052_second_cell_v24.py
```

Dette er en reproduktionsvej, ikke en instruktion om automatisk genkørsel eller genoptælling af point. Originalreceipt-SHA256:`863b0664140bce242bcbf05848ec840e43d809681a71feeb1e1b864c1f7f2bf8`.
