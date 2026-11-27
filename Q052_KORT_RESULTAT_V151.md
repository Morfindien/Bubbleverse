# BUBBLEVERSE — OVERLEVERING

**Q052 · V151 · 26. november 2026**  
STATUS: FORTSÆTTER · WORKFLOW_STATE: READY_FOR_HANDOFF · SCIENTIFIC_STATE: INCONCLUSIVE · TECHNICAL_STATE: PASS  
BUBBLEVERSE.MATHEMATICS 2.4.0 → BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0

## Oprindeligt spørgsmål

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

Den leverede motor 2.4.0 anvendes på den præcise numeriske V151-opgave fra V150, hvor 2.3.0 var angivet. Den aktuelle ugepost W48 og den ældre V150-journal er bevaret. Evidensgrænsen for fysikken er det fastlåste Q052-arkiv til og med V150.

## Resultat ved fælles logkoordinat

V151 sammenligner de eksakte polynomier fra de to arkiverede CLASS-processers fælles baggrund med V73 ved samme u = ln(a). For hele det klippede interval fra række 2 til 34 ligger feltet højere end referencen, og den normaliserede hastighed X = π/exp(u) ligger lavere. Det gælder også de 12 accepterede binære tilstande mellem stykkerne. Hvert af de 13 lukkede stykker omfatter begge sine randværdier inden for blokken.

| Størrelse | Signeret interval over alle 13 stykker | Indeslutning af sup af absolut afvigelse | Eneste mulige trin | Punktvidne |
|---|---|---|---:|---:|
| Δφ, CLASS-feltenheder | [1,9256 × 10⁻⁴⁷, 7,5830 × 10⁻⁴⁵] | [7,5606, 7,5830] × 10⁻⁴⁵ | 25 | række 34 |
| ΔX, CLASS-feltenheder/Mpc | [−9,5774, −1,9584] × 10⁻²⁸ | [9,5734, 9,5774] × 10⁻²⁸ | 23 | række 27 |

Alle decimalgrænser i tabellen er rundet udad. For φ er øvre grænse på alle andre trin 6,0264 × 10⁻⁴⁵. For X er den 9,5236 × 10⁻²⁸. Hvert punktvidne overstiger den tilsvarende grænse på de øvrige trin. Punktvidnet leverer en nedre grænse for supremum. Placeringen inde i det identificerede trin er fortsat åben.

Ved de 12 accepterede knuder ligger Δφ inden for [1,9256 × 10⁻⁴⁷, 5,7131 × 10⁻⁴⁵] og ΔX inden for [−9,5192, −1,9586] × 10⁻²⁸. Den accepterede binære højretilstand er præcis næste trins venstretilstand. De to eksakte polynomier fra de gemte koefficienter har forskellige ensidige værdier i φ ved 12 af 12 knuder og i π ved 11 af 12. Certifikatet opbevarer hver side og den accepterede tilstand særskilt.

## Regnevej og uafhængige kontroller

Antagelserne er V73's fastlåste kilde, parametre, positive Friedmann-rod og arvede startintervaller. V147 dækker hele den samme blok med 32 celler. Dens lokale eksistens- og grenindeslutning giver H > 2,0424 × 10²² Mpc⁻¹ og U/(3H²) < 1,8140 × 10⁻⁴², langt under grengrænsen 0,5 i denne konfiguration. Den oprindelige V147-reference blev genkørt ved 108 cifre. Både certifikatet og den separate rationelle V147-kontrol matchede arkivfilerne byte for byte.

Lad P betegne NDF15's bagudinterpolationspolynomium, S den gemte kubiske spline og R kildereferencen. På fælles u er P−R=(P−S)+(S−R). Det første led beregnes på ny. Det andet kommer fra V147's certificerede signerede interval for hver celle. For X er første led (Pπ−Sπ)/exp(u). Dermed bevares forskellen mellem den interne matematiske rekonstruktion og den senere spline. Certifikatet giver begge bidrag via de pr. stykke noterede differenser og V147-cellen.

De 13 trin skæres ved række 2, række 34 og de mellemliggende splineknuder. Det giver 44 sammenhængende delintervaller uden huller. I NDF15 bruges s=(u−u_hi)/h og vægtene b₀=1, bⱼ=bⱼ₋₁(s+j−1)/j til de gemte baguddifferenser. Differenspolynomiet har grad højst fire. Vi bestemmer dets Bernstein-koefficienter med eksakte brøker. Da Bernstein-vægtene er positive eller nul og summerer til én, indeslutter den mindste og største koefficient hele kurven. Konvertering og exp-indeslutning bruger udadrettede grænser. Kun de ydre snit med den certificerede blok indgår.

For begge komponenter og alle 44 stykker blev Bernstein-polynomiet kontrolleret på to yderligere rationelle punkter. Alle 33 gemte koordinater blev også direkte sammenlignet med V147’s reference ved rækken og kontrolleret mod V150’s eksakte punktresidual. Ved de 12 indre knuder gav en separat kraftindeslutning en kontrol af begge sider og den accepterede tilstand: Y=−X følger Y′=−3Y+V′/H. En konstant nedre og øvre kraft på den oprindelige splinecelle afgrænser Y ved knuden. V′>0 og Y>0 giver faldende referencefelt og et selvstændigt feltinterval fra cellens referencerande. Kontrollerne deler V73-starten og de historiske certificerede data. En ren udpakning og genkørsel genskabte V151-resultatet byte for byte.

## Rækkevidde

V151 måler en beregningsafvigelse i en tidlig baggrundsblok. De to arme genbruger de samme trin. Resultatet giver derfor ingen direkte parforskel i elektronfraktionen og ingen integreret Thomson-dybde. Det globale Q052-kriterium kræver valideret fejltransport til begge kurver over z = 0–810. Nul nye CLASS-processer og nul GitHub-dispatches.

## Overlevering til V152

Genkør V151-certifikatet fra reproduktionspakken, kontrollér placeringen af de to lokale maksima og indtag resultatet i samme Q-ledger én gang. Undersøg derefter, hvilke arkiverede baggrundsopslag der faktisk føder termodynamikberegningen i z-intervallet 0–810, og identificér det første opslag, hvor en fejlgrænse stadig mangler. Brug dette til at prioritere næste certifikat.

Accepter indtag ved byteidentisk replay, afstemte vidner, intervaller og journalpræfiks. Ved uforenelige intervaller stands den berørte påstand og gem første afvigelse. Ved manglende sporbarhed til et termodynamisk opslag registreres den første manglende inputreference. Det forventede V152-artefakt er en versionsbundet evidenspost og én præcis efterfølgende forskningsopgave. V151 standser ved række 34 efter aftalen i V150. Gentagelse af hele den native måling har ingen rolle i dette indtag.

## Point, publicering og forskningscheckpoint

RUN POINTS 98 estimeret: analyse 24 for koordineret fejltransfer og supremumkriterium, beregning 35 for 44 delintervaller og knuderekonstruktion, søgning 8 for versionsbundet evidens, validering 31 for genkørsler, punkt- og ODE-kontroller. Forrige total 17.127, ny total 17.225, cyklus 225/1000, næste tærskel M018 ved 18.000, 775 tilbage. Tidligere M001–M017 er videreført. Den nye videnskabelige milepæl udløser én SoMe-pakke. Status Klargjort for alle fem platforme. Journal og læring er integreret. Ingen bekræftet ekstern publicering.

Run-ID LOCAL-Q052-V151-VALIDATE-NDF15-DENSE-BLOCK-ROWS-2-34. Pointpost Q052-ACTIVITY-V151-DENSE-CERTIFICATE. Forrige post Q052-ACTIVITY-V150-AUTHENTICATE-ACCEPTED-NDF15-STEPS. Milepæl Q052-SCI-V151-DENSE-BLOCK. Pakke Q052-V151-DENSE-BLOCK-PUBLIC-R1. Tekstfil Q052_SOME_V151.txt og fuldt arkiv Q052_SOME_V151.zip.

## Setup og proveniens

Aktuelt setup er Codex med Python 3.12, eksakte brøker, styret decimalafrunding, filadgang og læst GitHub-reference. Klasse C/H. Samme lokale miljø er anbefalet til V152-indtag. Et særskilt reasoning-niveau er ikke verificeret. Ved forskellig bytehash identificeres første afvigelse. Alternativ kontrol kan bruge en anden intervalimplementation. Et korrekt replay kan indtages med en enklere sammenligningskørsel.

GitHub-kilderne er Morfindien/Bubbleverse ved 5098ad25dd894baed26c04d85af80ddcc0efec8a for V150-opgaven og arkivkørsel 45109440243 ved 4e6c13ed874d9ffc2418faed018fce6796f94e31. CLASS-kilden er mwt5345/class_ede ved 5a131c91d657dd9a7c6364cc45b038710f8d0d97. Resultatindtagskontrakten følger den læste V147-overleverings struktur. Lokal kontraktvalidering, uden et formelt fælles JSON-schema.

Samlet journal: Q052_MATEMATIK_OG_SAMLET_JOURNAL_V151.md. Certifikat: Q052_CERTIFIKAT_V151.json. Reproduktion: Q052_REPRODUKTION_V151.zip. Maskinlæsbar overlevering: Q052_RESULTATINDTAG_OPGAVE_V151.json. Filerne er klar til manuel upload til Morfindien/Bubbleverse. Den fulde journal med W48 var et præfiks på 9842368 bytes med SHA-256 91e86fea65450048159920c2c267f869d42196272c6de27dfa7d539050d549ac.

[Fastlåst V150-opgave](https://github.com/Morfindien/Bubbleverse/blob/5098ad25dd894baed26c04d85af80ddcc0efec8a/Q052_MATEMATIKOPGAVE_V150.json) · [Målekørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/45109440243)
