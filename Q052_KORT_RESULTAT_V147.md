# Q052 · V147 · Fejlgrænser på 32 sammenhængende baggrundsceller

**23. november 2026 · Matematikmotor 2.3.0 · Q052 fortsætter**

På blokken fra række 2 til række 34 ligger den største absolutte relative H-afvigelse **mellem 1,7070 × 10⁻¹¹ og 1,7093 × 10⁻¹¹**. Maksimum ligger i den første celle, fra række 2 til 3. Tre ottendedele inde i den celle ligger den gemte H-kurve cirka 1,707018 × 10⁻¹¹ over V73-referencen målt relativt. På hver af de øvrige 31 celler er den maksimale absolutte relative afvigelse under 4,608 × 10⁻¹². Det fastslår, hvilken celle der rummer maksimum. Punktets præcise placering inden for cellen er åben.

Forskellen Δ er den gemte CLASS-spline minus den fastlåste V73-løsning ved samme logkoordinat u = ln(a). Ved den relative H-fejl er nævneren den positive referenceværdi H(u). L og R har de samme 33 baggrundsrækker. Tabellen viser udad afrundede grænser fra standardkørslen.

| Størrelse | Gennem hele blokken | Ved række 34, cirka |
| --- | --- | ---: |
| Δφ, CLASS-feltenheder | [1,9256 × 10⁻⁴⁷, 5,7131 × 10⁻⁴⁵] | +5,713083 × 10⁻⁴⁵ |
| ΔX, CLASS-feltenheder pr. Mpc | [−9,5754 × 10⁻²⁸, −2,2177 × 10⁻²⁸] | −8,961274 × 10⁻²⁸ |
| ΔH, Mpc⁻¹ | [−9,8765 × 10¹⁰, +3,6700 × 10¹¹] | −620.193,4485 |

Den gemte feltværdi ligger over referencen gennem alle 32 celler, og den gemte hastighed X ligger under referencen. For H afhænger fortegnet af cellen. På **19 celler** ligger splinen under referencen overalt. På **én celle**, række 4 til 5, ligger den over referencen overalt. På **12 celler** findes verificerede punkter på begge sider af referencen. Dermed krydser H-kurverne hinanden mindst én gang inden for hver af de 12 celler. Hver celle er navngivet med begge rækkeindekser i CSV-tabellen i reproduktionspakken.

## Hvad sker der med usikkerheden?

Ved hver af de 31 indre knuder er højre endes referenceinterval brugt som venstre endes startinterval for næste celle. Felt, hastighed og positiv Friedmann-rod er kontrolleret igen ved samme logkoordinat. Bredden i tabellen er forskellen mellem de to ender af referenceintervallet. Den måler usikkerheden i den beregnede reference.

| Referenceinterval | Bredde ved række 2, ca. | Bredde ved række 34, ca. | Faktor |
| --- | ---: | ---: | ---: |
| φ | 5,41 × 10⁻⁶¹ | 1,63 × 10⁻⁵⁸ | 300,6 |
| X | 7,23 × 10⁻³⁶ | 1,23 × 10⁻³⁴ | 17,0 |

Ved række 34 er referencehastigheden cirka −8,637440674953 × 10⁻²¹ i CLASS-feltenheder pr. Mpc. Certifikatets felt `end_state` giver de uafrundede intervaller for φ, X og H, de gemte splineværdier og de signerede afvigelser. Det indeholder også forskydningen fra V73's oprindelige feltværdi.

## Beregning og kontrol

Hver celle bruger sine egne endeværdier og andenafledte til de tre gemte kubiske splines. Hastigheden sammenlignes som X = π/exp(u), hvor π er den gemte konforme felthastighed. Den fastlåste V73-gren giver H > 0. Selv den største øvre grænse for den periodiske del af potentialet, U/(3H²), er under 1,8140 × 10⁻⁴² på blokken. Den fælles reference er ført frem med sine oprindelige kildekonstanter.

Sæt Y = −X, K = a²H og C = V′/K. De afledte i u opfylder Y′ = −3Y + V′/H og φ′ = −Y/H. På en celle med længde h og lokal koordinat s fra venstre knude giver integration med positive vægte følgende indeslutninger. C og K er indeholdt i hver sit beregnede interval gennem cellen.

```text
Y(s) ∈ Yᵢ exp(−3s) + C aᵢ² [exp(2s) − exp(−3s)] / 5
φᵢ − φ(s) ∈ Yᵢ aᵢ² [1 − exp(−s)] / K
           + C aᵢ⁴ { [exp(4s)−1]/4 − [1−exp(−s)] } / (5K)
```

Den første beregning samler koefficienterne i forskellen mellem splinen og den indkapslede reference før intervalevaluering. Eksponentialpolynomierne har grad 8 og et udadrettet restled. Kontrolberegningen anvender konstante øvre og nedre kraftgrænser på hvert delinterval og en lokal centreret kubisk udvikling af eksponentialleddet i H. Ekstra halveringer af delintervaller nær mulige nulpunkter forbedrer fortegnskontrollen. De to beregninger deler kildeinput og intervalaritmetik.

| Kørsel | Decimalcifre | Delintervaller pr. celle, hovedberegning / kontrol | Øvre grænse for blokmaksimum, udad afrundet |
| --- | ---: | ---: | ---: |
| Standard | 108 | 256 / 128 | 1,70922 × 10⁻¹¹ |
| Finere kontrol | 128 | 512 / 256 | 1,70905 × 10⁻¹¹ |

En tredje beregning bruger eksakte brøker, heltalskvadratrødder og en eksponentialrække med rationelt restled. Den efterprøver H ved alle 33 knuder, punktet ved 3/8 og begge fortegn på hver celle med et konstateret fortegnsskift. Den fører også referencen direkte fra række 2 til hvert efterfølgende knudepunkt med V146's grænser for hele blokken. Ved alle 32 højre ender overlapper de beregnede intervaller for φ og X dem fra den cellevis videreførte løsning. Kontrollen deler de arkiverede V73-input og V146-grænserne.

## Hvad afgør resultatet for Q052?

Den tekniske delopgave er bestået. Den videnskabelige status for Q052 er **INCONCLUSIVE**. Blokken certificerer den gemte baggrundsspline på ét afgrænset interval. For hele Q052 mangler forbindelsen til CLASS' interne løsningsbane og de to maksimumafvigelser over det krævede domæne for elektronfraktion og Thomson-optisk dybde. Beregningen brugte de eksisterende tabeller og startede nul nye CLASS-kørsler.

**V148** får blokcertifikatet, reproduktionspakken og referenceintervallerne ved række 34 til resultatindtag. Rapporten, den samlede journal, blokcertifikatet, reproduktionspakken og opgaven til V148 er klar til manuel upload til roden af Morfindien/Bubbleverse.

**126 estimerede arbejdspoint** bringer totalen fra 16.705 til **16.831**. Der mangler **169** til M017.

- [V146-input ved den verificerede GitHub-revision](https://github.com/Morfindien/Bubbleverse/tree/43a9e891f4ab44b5f75b08938e2fd244e5817c5d)
- [Fastlåste CLASS-baggrundsligninger](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c#L2697)
- [Fastlåst splineformel](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c#L1858)
