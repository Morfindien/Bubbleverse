# Q052 V155 · Ensartet fejlgrænse for det første H-interval

**Teknisk PASS_CONDITIONAL_SCOPED. Q052 er ACTIVE · CONTINUE · INCONCLUSIVE.**

Under samme fastlåste model, B★-reference og binære opslagsalgoritme er den absolutte relative forskel i H højst **0,005 % på hele det lukkede interval z ∈ [809,8167709474…; 810]**. Det svarer til 50 milliontedele. Fortegnet er uafgjort. Der indgår ingen nye fysiske observationer i kontrollen.

| Resultat | Udadrettet interval |
|---|---|
| H_native(RN64(z)) − H_B★(z), Mpc⁻¹ | [−0,0001633091110616; +0,0001505314796613] |
| Samme forskel divideret med H_B★(z) | [−0,0000498887830453; +0,0000459688139887] |
| I procent | [−0,00498887830453 %; +0,00459688139887 %] |
| Letlæselig øvre grænse på absolut relativ forskel | 0,005 % |
| Genafspillede RHS-kald inden for intervallet | 19 af 19 |
| Sammenhængende delintervaller | 256 |

Den eksakte nedre grænse er 7123223648197587/8796093022208. RN64 er afrunding til nærmeste binary64-tal med lige sidste bit ved lighed. Den valgte udvidelse til reelt z bevarer inputtet ved alle de faktisk arkiverede kald.

## Hvorfor grænsen dækker mellem kald

V153’s validerede energi ved 810 og scalarfeltets ligning giver −6e ≤ de/dln(a) ≤ 0. Ved lavere z indrammes energien derfor af e810_nedre·((1+z)/811)^6 og e810_øvre. Det giver en gyldig, konservativ reference på hele stykket. V105’s 142. nye referencecelle indeholder hele domænet. Vi genbruger dens validerede forudsætninger og V153’s startindeslutning.

Domænet opdeles i 256 sammenhængende intervaller med eksakte rationelle grænser. Positive monotone tæthedsled og den positive Friedmann-rod afgrænser H_B★ på hvert interval. Tabellens kubikker har negativ afledt på de relevante stykker. Deres værdier kan derfor indrammes ved intervalenderne.

Inputafrunding og logaritmeafrunding giver en samlet u-fejl mindre end 5,142 × 10⁻¹⁶. Den påviste absolutte splinehældning er under 6. Det uafhængige kontrolbudget for H’s koordinatbidrag er derfor under 3,086 × 10⁻¹⁵ Mpc⁻¹. En automatisk fejludbredelse gennem hver binary64-operation giver et skarpere aritmetikbudget på cirka 3,681 × 10⁻¹⁵ Mpc⁻¹. Den særskilte konservative kontrol bruger 4096·2⁻⁵³ ≈ 4,548 × 10⁻¹³ Mpc⁻¹. Slutintervallet omfatter begge kontrolvejes grænser.

Ved den nederste rødforskydning ligger det eksakte u en smule over den lagrede knude 31688. Begge kubikstykker 31687–31688 og 31688–31689 indgår i afgrænsningen. De har samme lagrede H ved fælles knude, og begge hældninger er kontrolleret. Dermed er også det lille stykke på den anden side af knuden medregnet.

## Kontrol og forudsætninger

Den primære beregning bruger rationelle tal og udadrettet dyadisk aritmetik. Kontrolvejen bruger mpmath.iv ved 95 decimalcifre, en anden neutrinoformel og rækkefølge af summen, splinens knudeform og et særskilt større budget for koordinat- og operationsfejl. De to regneveje deler det arvede referencebevis og energitransporten. Certifikatet gemmer alle 256 intervaller og deres grænser.

De 19 arkiverede kald er genafspillet med de observerede H-bits, og deres punktvise fejlindeslutninger ligger inden for slutgrænsen. Slutgrænsen indeholder V153’s punktinterval ved 810. Sampling er en ekstra kontrol. Intervalregningen og energiloven leverer dækningen mellem kaldene.

Betingelserne omfatter den fastlåste reelle model, V105/V153-valideringen, den registrerede MPFR-logkoordinat med korrekt afrunding samt binary64-operationer i kildens rækkefølge. Certifikatet vedrører denne algoritme med disse forudsætninger. En anden compilerindstilling, FMA-sammenlægning eller omgruppering kræver afstemning.

Den fastlåste interpolationskilde er læst igen. Reproduktionspakken indeholder et kildeudsnit, udledning, startcertifikat, V154-evidens, vidner og al ny kode. En ren genkørsel skal genskabe V155-certifikatet byte for byte. [Interpolationskilde](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c) · [Målearkiv](https://github.com/Morfindien/Bubbleverse/actions/runs/45109440243)

## Overlevering og journal

Resultatindtag og routing 2.4.0 modtager V155 til Q052 V156. Indtag den ensartede intervalgrænse én gang, kontroller dens forudsætninger og identificér den næste manglende H-dækning eller den første nødvendige fejloverførsel til elektronberegningen. Vælg derefter én afgrænset opgave. Den konforme tid og de fulde suprema for elektronfraktion og Thomson-dybde forbliver åbne.

V154’s 17.442 aktivitetspoint suppleres med 96 estimerede point, heraf 25 for analyse, 31 for beregning, 10 for kildearbejde og 30 for validering. Total 17.538. Der mangler 462 til 18.000. Den nye videnskabelige milepæl Q052-SCI-V155-H-FIRST-SEGMENT begrunder SoMe-pakken. Pointtærsklen er endnu ikke nået.

Den samlede V154-journal bevares som byteidentisk præfiks. De nye V155-filer er klar til manuel GitHub-arkivering. Den senest verificerede base er 341a45b8806354178b3508de3378ebd65c6d9591, hvor V154-opgavefilens Git-blob var afstemt. Ingen ekstern skrivning er udført i denne runde.

Kørsel 2026-11-27T12:44:28+00:00 UTC · Europe/Copenhagen er UTC+01:00 på kørselsdatoen.
