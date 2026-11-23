# Q052 · V148 · Overgang fra gemt baggrundsspline til interne CLASS-trin

**23. november 2026 · Resultatindtag og routing 2.3.0**

V147 er indtaget og verificeret. Alle tre genkørsler genskabte de arkiverede resultater byte for byte. På de 32 gemte celler fra række 2 til 34 ligger den største absolutte relative afvigelse i H strengt mellem **1,7070 × 10⁻¹¹ og 1,7093 × 10⁻¹¹**. Den ligger i cellen fra række 2 til 3.

Den oprindelige række 34 er byteidentisk i de to V141-tabeller. En genberegning ved 150 cifre bekræftede de gemte splineværdier ved samme eksakte u = ln(a), og den positive Friedmann-rod overlapper V147's referenceinterval. Referenceintervallerne for φ og X er bevaret med fuld præcision til videre arbejde. Ved række 34 er φ-forskydningen fra det oprindelige felt cirka 5,713083 × 10⁻⁴⁵ i CLASS-feltenheder.

## Hvor de interne trin mangler

| Kilde | Hvad den dokumenterer |
| --- | --- |
| De to V141-baggrundstabeller | Gitteret i ln(a), værdierne i tabellen og de gemte andenafledte. |
| V141's startkvitteringer | Initialiseringen og det første kald til baggrundens differentialligninger i den endelige NDF15-kørsel. |
| V141's termodynamiske spor | RHS-evalueringer, output og fasehændelser. De fulde tilstandsspor omfatter z fra 810 til 0. |
| CLASS-koden | Når et accepteret trin rammer et outputpunkt, overføres trinets tilstand direkte. Hvis trinet går forbi punktet, beregner NDF15 en interpoleret tilstand, som sendes til samme outputfunktion. |

Række 34 ligger ved ln(a) ≈ −32,2087898543, svarende til z ≈ 9,73 × 10¹³. Arkivkontrollen fandt ingen accepteret baggrundstilstand eller NDF15-koefficienter knyttet til denne række. V147 afgrænser den gemte kubiske baggrundsspline. For at sammenligne med den interne NDF15-bane skal vi kunne knytte hver tidlig outputrække til det accepterede trin, der producerede den.

## Valgt opgave til V149

**Execution/HPC Builder 2.4.0** skal klargøre en passiv observatør til et nyt nominelt L/R-par. Den skal kunne registrere de accepterede baggrundstrin, der leverer række 2–34, samt tilstanden ved begge ender af hvert trin. Der skal være en entydig kobling mellem trinnummer, gitterrække og den direkte eller interpolerede tilstand, der sendes til output. For interpolerede rækker skal de nødvendige input til NDF15-interpolationen med i målingen. Dette giver et afgrænset sæt data til en efterfølgende sammenligning på samme koordinat.

Den autentificerede CLASS-binær har symboler for NDF15, interpolatoren og baggrundens outputfunktion samt DWARF-data. Der findes en fastlåst observatørpakke og en tidligere fungerende målekørsel. V149 skal verificere de konkrete målepunkter mod den binære fil, da optimerede lokale variabler kan kræve kontrol af registre eller instruktioner. Handoffet angiver en kapacitetsgrænse og registrering af eventuel manglende dækning. V149 slutter med en statisk verificeret målepakke eller en præcis hindring i den eksisterende binær. En måling kræver et senere køretrin.

Q052 fortsætter som **INCONCLUSIVE**. V148 brugte arkiverede data. Den fulde forbindelse til CLASS' interne bane og de validerede maksimummer for elektronfraktion og Thomson-optisk dybde er fortsat åbne.

V148 giver **78 estimerede arbejdspoint**. Total **16.909**, med **91** til M017. GitHub havde alle fire vedhæftede V147-filer med samme bytes. Reproduktionsarkivet blev verificeret fra den oprindeligt afleverede ZIP. V148-filerne er klar til manuel upload.

- [V147-filerne ved den verificerede GitHub-revision](https://github.com/Morfindien/Bubbleverse/tree/479ba72c33483e379554ce492747d676ae110a0a)
- [NDF15's accepterede trin og outputvalg](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/evolver_ndf15.c#L535-L577)
- [CLASS' baggrundsgitter og outputfunktion](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c#L1959)
- [V141-kørslen med det observerede startkald](https://github.com/Morfindien/Bubbleverse/actions/runs/45061263002)
