# Q052 · V144 · Overgangen til den anden baggrundscelle

**23. november 2026 · Resultatindtag og routing 2.3.0 · Q052 fortsætter**

Højre ende af den første celle kan bruges som start for den næste. De to oprindelige CLASS-tabeller, L og R, har identiske data ved det fælles knudepunkt og ved næste række. Vi har overført V73-referencens fulde intervaller for feltet φ og hastigheden X til knudepunktet. Det gør det muligt at måle, hvordan den allerede opståede afvigelse udvikler sig på celle 2.

## Hvad kontrollen viste

| Kontrol | Udfald |
| --- | --- |
| V143-certifikatet fra arkivet | Hovedkørslen ved 106 cifre og kontrolkørslen ved 123 cifre genskabte hver sin arkiverede JSON-fil byte for byte. Begge gentog de rationelle fortegnskontroller. |
| Relativ fejl i ekspansionsraten H | På den første celles fælles interval ligger maksimum af den absolutte relative fejl strengt mellem 2,2113 × 10⁻¹⁰ og 2,3750 × 10⁻¹⁰. Forskellen skifter fortegn mindst to gange. |
| Oprindelige tabeller | Begge filer på 40.000 rækker matcher V141-manifestet. Dataene efter filhovedet matcher V69-fingeraftrykket i V142. Alle logkoordinater er strengt stigende. |
| Knudepunktet | Række 1 matcher V142 byte for byte. En særskilt beregning med eksakte brøker bekræfter, at de tre gemte splineværdier ved knuden ligger i V143-intervallerne. |
| Journal og sporbarhed | V142 er bevaret som bytepræfiks i V143. Den fulde V143-journal er videreført som bytepræfiks i V144. |

Ved knuden er forskellen defineret som *gemt spline minus V73-reference* ved samme u = ln(a). Tallene nedenfor er afrundede læseværdier. Evidensfilen indeholder de fulde intervaller.

| Størrelse | Forskel ved række 1 |
| --- | ---: |
| Skalarfelt φ | ≈ +4,810292 × 10⁻⁴⁸ |
| Hastighed X = φ′η/exp(u), CLASS-feltenheder pr. Mpc | ≈ −7,29425 × 10⁻²⁹ |
| Ekspansionsrate H | ≈ −2.871.480,627 Mpc⁻¹ |

Den gemte værdi for a ved række 1 er lidt større end den eksakte exp(u₁). I sammenligningen bruger begge sider exp(u₁) som nævner for X. Skellet er bevaret i evidensen sammen med koordinatforskydningen ved den oprindelige start.

## Opgaven til V145

Matematikmotor 2.3.0 får ét interval, fra række 1 til række 2, med eksakt bredde 113423850545/140737488355328 i ln(a). Den skal føre referenceintervallerne for φ og X frem, genberegne den positive Friedmann-rod for H og indeslutte de tre signerede afvigelser gennem hele cellen. Højre endes usikkerhed skal kunne genbruges i et senere trin. Der er en særskilt kontrol ved det fælles knudepunkt samt en beregningskontrol på den nye celle.

Den videnskabelige status er **INCONCLUSIVE**. V144 verificerer overgangen mellem de gemte baggrundsceller. Q052 kræver stadig en forbindelse til den interne native bane og certificerede maksimumafvigelser for elektronfraktion og Thomson-optisk dybde. V144 startede ingen nye CLASS-kørsler. Beregningen på celle 2 ligger i V145.

## Filer og point

| Fil | Anvendelse |
| --- | --- |
| Q052_KORT_RESULTAT_V144.md | Denne afgørelse |
| Q052_INGESTION_OG_SAMLET_JOURNAL_V144.md | Hele journalen til og med V144 |
| Q052_EVIDENS_V144.json | Rårækker, kildeinput, kontrolresultater og fuld præcision ved overgangen |
| Q052_MATEMATIKOPGAVE_V144.json | Maskinlæsbar opgave til V145 med input, acceptkriterier og stopbetingelse |

Ved kontrol af GitHub-revision `01f7d128bba4794a8cf4b137025dbd64c2ee386a` lå V142 og begge motorer i roden. De seks V143-leverancer var endnu ikke registreret dér under deres afleverede filnavne. V144-filerne er klar til manuel upload til roden af Morfindien/Bubbleverse sammen med eventuelle manglende V143-filer. V144-evidensen indeholder selv de to rækker, hele V73-inputfilen og intervallerne, som V145 skal bruge.

V144 tilføjer 64 estimerede arbejdspoint for kontrol og overlevering. Totalen går fra 16.469 til **16.533**. Der mangler **467** til M017. V143-beregningen er allerede bogført.

Kilde til det oprindelige tabelpar og den kontrollerede projektversion. [V141-kørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/45061263002) · [Bubbleverse ved den kontrollerede revision](https://github.com/Morfindien/Bubbleverse/tree/01f7d128bba4794a8cf4b137025dbd64c2ee386a)
