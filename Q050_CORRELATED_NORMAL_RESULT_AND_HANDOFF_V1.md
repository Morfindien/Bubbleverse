# Q050 — korreleret Pion-normalcertifikat og fortsat åben global opgave

Motor: **Execution HPC Motor Builder v2.4.0**. RUN_ID `LOCAL-Q050-CLEAN-CORRELATED-NORMAL-20261025-V1`.
UTC 2026-10-25T03:43:01.050186+00:00; Europe/Copenhagen 2026-10-25T04:43:01.050186+01:00. CURRENT_Q=TARGET_Q=Q050.
Case `LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1`.

## Det præcise spørgsmål

For the frozen hillipop-ede_n3 configuration and each fixed admitted common background on 0 <= z <= 810, do the exact source-real low-redshift hydrogen/temperature branch-selection rules admit an absolutely continuous continuation to z=0 from every state in the validated z=810 domain, separately for q=xHeII=10^-6 and q=0, without changing or convexifying the selector?

Spørgsmålets SHA256: `11af5cf58d6c94e34a050e9672a76e47d277c0fcaec14e9acbcf58e96eb22b01`.

## Hvad ved vi nu?

Den nye kørsel udelukker det **førsteordens, indadrettede normalmønster** på Pion-skiftefladen i hele det kvalificerede dækningsinterval z=2859858991540483/4398046511104 til810, betinget af den samme faste admitted baggrundsfamilie. Den præcise numeriske disjunktion er

**N_HMLA,z > 0 ELLER N_SWIFT,z < 0**

ved hvert dækket kandidatpunkt på fladen, separat for q=1/1000000 ogq=0. I fysisk evolution u=ln(a), hvor z falder, er det ækvivalent med

**N_HMLA,u < 0 ELLER N_SWIFT,u > 0**.

Her er HMLA-armen på F<0-siden og SWIFT på F>=0-siden. Mindst én arm peger derfor strengt ind i sin egen selector-side. Mønsteret, hvor begge arme peger mod skiftefladen fra hver sin side, er udelukket af dette betingede certifikat. Det er den konkrete førsteordens-obstruktion, der undersøges; ingen source-selector er ændret eller convexified.

**Dette er ikke et globalt AC-fortsættelsesbevis. Q050 er stadig ACTIVE / INCONCLUSIVE.** Den formelle lokale literal-selector-fortsættelseslemma og den samlede completion-audit på0<=z<=810 mangler. Native/P6, baggrundseksistens, realiserbarhed af hvert projektionspunkt og reachability er ikke bevist.

## Faktisk kørsel og dækning

Kun de syv uafklarede parentceller blev genberegnet. De57 øvrige parentceller fra den accepterede64-celledækning blev bevaret uændret som kildeevidens. En ny version opdeler hver af de syv i4 z-intervaller,4 v-intervaller og8 H-intervaller:896 kontinuerte subceller, med112 genbrugte source-nodevidner. J=dlogH/dz beholder sin admitted enclosure. Overlappende endepunkter er tilsigtet.

| Ny kørsel, samme udfald for begge q-grene | Subceller |
|---|---:|
| Begge F_z-normaler strengt negative |624|
| Begge F_z-normaler strengt positive |107|
| Nulindeholdende marginalnormaler, men strengt positiv HMLA-minus-SWIFT-normalforskel |73|
| Certificeret fysisk tom flade |92|
| I alt |896|

Fire af de syv parentceller er nu helt negative i z-retningen: g74:z2/4, g74:z3/4, g75:z0/4 ogg75:z1/4, samlet z=695–705. De73 marginalt nulindeholdende subceller ligger i de tre resterende parentceller, med z-projektion688,75–695. Nulindeholdende intervaller betyder fortsat ikke, at et eksakt nul er bevist.

I alle73 er N_HMLA,z-N_SWIFT,z strengt positiv. Den mindste certificerede positive undergrænse i denne endelige partition er ca.9.5533637e-06 for F_z-normalforskellen; den præcise rationalgrænse står i certifikatet. Begge normaler kan derfor ikke være nul samtidig i disse kandidatbokse, og den indadrettede kombination N_HMLA,z<=0<=N_SWIFT,z kan ikke forekomme. Samme-fortegnsbokse og tomme bokse dækker de andre tilfælde.

Den samlede, heterogene dækningsvisning indeholder57 uændrede parentrecords plus896 nye subrecords, i alt953. Heraf er847 normalrecords og106 tomme; der er1694 q-specifikke normalpar og3388 F_z-normalintervaller. Dette er bevisdomæner, ikke nye trajectorieceller eller uafhængige baggrundsstarts. Q048 actual127/frontier810 er uændret.

## Hvad er ændret i matematik og kode?

Den pinned CLASS/HyRec-konfiguration, tabeller, source-real decimalgrænse Pion=1/100, equality-regler og baggrundsbinding er bevaret. HMLA/SWIFT evalueres på identiske state-/baggrundsdomæner. Den samme dependency `Q050-COMMON-BACKGROUND-92de319899bf911563aff4d1` følger alle celler og begge q-grene. Native H_prime er stadig conformal-time og bruges ikke som z-afledt. Det nødvendige v-path enclosure49/50*(1+z)/811<=v<=1000001/1000000 og det fysiske0<=h<1-snit er fastholdt; z=810-startboksen antages ikke fremtidsinvariant.

Den nye interpolation centrerer lokale tabelværdier før polynomielevaluering: c+sum(w_i*(node_i-c)), ud fra den eksakte identitet sum(w_i)=1. Dermed undgås store kunstige intervalbidrag fra næsten ens log-værdier. Den samme source-Lagrangebasis evalueres både som polynomium og som produktbasis; gyldige enclosures og den admitted L1-grænse skæres. Cold/hot-temperaturkanaler opdeles før koordinathull, og SWIFT-fit-DK centreres tilsvarende. Dette ændrer enclosures og kode, ikke den frosne operator. Alle112 nye source-noder giver et strengt negativt DK-interval.

På fladen sættes C=99B-L, g=1-h=3*LYA_FACT*H_s/(nH*C), x=h/g=1/g-1 og M=3*LYA_FACT/(1+z). Med A=C_s*Alpha_s+C_p*Alpha_p og E=C_s*Alpha_eq_s+C_p*Alpha_eq_p bliver den samme fulde source-normal

N_z=99B_z-CJ+3C/(1+z)-M*[A*x*((1+q)*x+q)-E*saha/g].

Relationen nH/H_s=3*LYA_FACT/(C*g) fjerner en vigtig afhængighed fra den gamle formel. N_HMLA,z-N_SWIFT,z beregnes med fælles eksplicitte led annulleret, ikke ved ukorreleret subtraktion. For source-C-faktorerne bruges en eksakt faktoriseret forskel mellem R_H=C/3 ogR_S=R_H/(1+DK): fælles positive lineære nævnere og faktoren R_H*DK/(1+DK). Den faktoriserede identitet er testet ved eksakte rationelle kontroller for både positivt og negativt DK. Source-normalen og den korrelerede normal skæres, og de to normale marginaler kontraheres to gange med den gyldige fælles forskel.

## Separat kontrol af fortegnsgeometri

Den på forhånd afgrænsede kontrol ved z=691,25 ogv=0,95 blev også udført. En lille kontinuert projektionsboks giver N_HMLA,z>0>N_SWIFT,z for begge q-grene: et **udadrettet/repellerende** mønster i fysisk u-retning. Det er ikke det indadrettede fejlmønster. Kontrollen er separat producer-free verificeret.

Boksen ligger inden for de parent-projektioner, der er tilladt af bindingen. Den beviser ikke, at en admitted connected baggrund realiserer netop den valgte H/J-kombination, eller at en trajectorie når boksen. Den er derfor ikke et modbevis til Q050. Den viser, hvorfor det ville være et forkert stopkriterium at kræve, at begge normaler altid har samme fortegn i hele overmængden.

## Validering og ressourcer

Piloten havde16 subceller og4 noder og tog1,025s. Derefter blev den endelige896-cellepartition og180s wall cap frosset. Den lokale slutkørsel tog16.052s; den endelige producer-free checker tog17.136s. GitHub Actions var ikke nødvendigt; ingen workflow-dispatch eller betalt ekstern compute er startet.

Den nye checker rekonstruerer source-/tabelvidner, alle subbokse, normaler, forskelle, q-grene, orientering og komplet multidimensional dækning.33 inputhashes er verificeret. Der er3 beståede eksakte/unit-kontroller,14 afviste semantiske mutationer samt den særskilte kontinuerte projektionskontrol. Den endelige tekniske status er **PASS_CONDITIONAL_CORRELATED_REFINEMENT_WITNESSES**. Fælles interval-/tabelprimitiver og centrerede hjælpefunktioner begrænser uafhængigheden; det er ikke fuldstændig uafhængig native replikation.

De oprindelige specbytes er bevaret efter frysning. Et separat metadata-addendum forklarer arvede kompatibilitetsfelter fra parent-spec (bl.a. det gamle240-point estimat); den nye aktive plan og point_estimate230 styrer denne kørsel. Ingen numerisk spec eller råfil er ændret efter udførelse.

## Næste motor

**Result Ingestion & Routing v2.3.0.** Importér dette resultat én gang. Den nye opgave er at vurdere den præcise selv-side-normaldisjunktion og den nødvendige formelle literal-selector-fortsættelseslemma under de frosne regularitets-/domænepræmisser, efterfulgt af global interface/completion-audit. Den numeriske førstordensretning er nu dækket; yderligere generel gridforfining alene for at fjerne alle marginale nulintervaller er ikke den begrundede næste opgave. En Mathematics-route har nu nyt konkret materiale og en afgrænset analytisk forpligtelse, hvis intake vælger den.

Der er0 nye actual trajectory-celler, ingen baggrundseksistens, ingen pre-reset Q050 V8-state/resultater/point og ingen ændring af accepted science. Hele indgående journal bevares byte-for-byte som prefix med dette append; samme case og hele præcise spørgsmål følger handoff.

## Point, SoMe og GitHub-memory

990 arvede point +230 nye = **1220 kumulative point**. En ny event, ingen gentælling af de tidligere resultater.230=ny source/matematik60+implementering65+bounded execution20+verifikation65+integritet20; groft, ukalibreret aktivitetsestimat. SoMe-produktion, journal-kopiering, formatering og lagring giver0. Den nye1000-milepæl `Q050-SOME-M001` har en faktisk engelsk status-/opslags-/kortvideo-/kildepakke og intern manifest. Ingen opslag eller video er offentliggjort/genereret. Næste milepæl2000;780 point til den. Q050 fortsætter uafhængigt af point.

GitHub-memory er læst ved `284bf650f03553cd9742cc46564e290704333fd1`,4536 entries, ikke trunkeret; den indgående journal/rapport matcher aktuelle Git-blob-IDer. MEMORY_WRITE_STATUS=FILES_READY_FOR_MANUAL_UPLOAD; ingen GitHub commit,PR,pointer-opdatering eller kørsel af næste motor er foretaget. Alle filer, inklusive rådata, kildekode og SoMe-pakken, leveres individuelt uden arkiv.
