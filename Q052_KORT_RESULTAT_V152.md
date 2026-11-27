# Q052 V152 · Resultatindtag og routing

**ACTIVE · CONTINUE · INCONCLUSIVE · teknisk PASS for det afgrænsede arkivindtag.**  
Resultatindtag og routing 2.4.0 · 2026-11-27T09:02:03Z · 2026-11-27T10:02:03+01:00, Europe/Copenhagen.  
Case LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1 · CURRENT_Q = TARGET_Q = Q052.  
Oprindeligt spørgsmål:

> Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

## Resultat

Vi genskabte V151-certifikatet byte for byte fra det leverede reproduktionsarkiv. Det største absolutte feltudsving ligger på trin 25 med række 34 som nedre vidne. Det største udsving i normaliseret felthastighed ligger på trin 23 med række 27 som nedre vidne. Supremumsgrænserne er henholdsvis [7,5606; 7,5830] × 10⁻⁴⁵ og [9,5734; 9,5774] × 10⁻²⁸ i de dokumenterede CLASS-enheder, afrundet udad. V151-posten er indtaget én gang, med de oprindelige data og præmisser bevaret.

**Det første termodynamiske H-opslag i den arkiverede udvikling efter heliuminterventionen er ved z = 810.** Begge arme brugte H = `0x1.a32c73ba0388ap+1` Mpc⁻¹, ca. 3,2747940691252255 Mpc⁻¹. Det er den første `RHS`-post i `fullstate_trace.jsonl` i hver arm, fase 5 med hydrogen aktivt og helium holdt fast. Det tilsvarende HyRec-kald på SWIFT-grenen modtog `0x1.1e9426533631cp-45` s⁻¹. Baggrundsopslaget brugte `u = -0x1.acb06c7e111acp+2` og bracketrækker 31687 og 31688 (nulbaseret, z ≈ 810,47049 og 809,81677). `Z810_PRE_INTERVENTION` og `Z810_POST_INTERVENTION` viser workspace-snapshots. Belægget for, hvad første afledte kald bruger, er den matchede RHS- og HyRec-post.

Genafspilningen genskabte H med de samme binary64-bits i alle 10.851 RHS-poster (5.435 L og 5.416 R) og 9.724 OUTPUT-snapshots. Den kontrollerede HyRec-omregningen i hver RHS-post og verificerede, at de 40.000 lagrede baggrundsrækker matcher ordret på tværs af armene. De 38 gemte koordinatposter blev afstemt med en ny logevaluering. For de øvrige punkter genskabte vi logkoordinaten med Decimal ved 68 cifre og kontrollerede det observerede H. Bitsammenfaldet ved de gemte kald er en reproduktionskontrol. En udadrettet grænse for native fejl mod B★ skal beregnes særskilt, inklusive koordinatbidraget. Ved det første opslag er H_native minus den eksakte tabelkubik på den målte logkoordinat ca. +2,372 × 10⁻¹⁶ Mpc⁻¹. Den eksakte brøk står i evidensfilen.

## Hvor grænsen først mangler

V151 dækker u ≈ −32,23458 til −32,20879, svarende til z ≈ 9,73–9,98 × 10¹³. Termodynamikkens undersøgte domæne er u = −ln(811) til 0, svarende til 0 ≤ z ≤ 810. Ingen af dens registrerede H-kald rammer V151-blokken. Et direkte, brugbart interval for **H_native(810) − H_B★(810)** ved samme fysiske z er det første uafklarede input ved genstarten. V24/V62 og de senere optiske vægtgrænser giver betinget kildeevidens, og V105 giver et anker ved z = 800. De grænser skal afstemmes med den faktisk returnerede H-værdi ved 810, inklusive forskellen mellem det binært returnerede u og det eksakte −ln(811). Gentagelse af den tidlige 32-celleblok løser ikke dette punkt.

| Kald | Hvad arkivet og kilden binder |
|---|---|
| Termodynamikkens afledte | `thermodynamics_derivs` kalder `background_at_z` med `long_info, inter_closeby`, læser tabelkolonnen H og sender den omregnede værdi videre til HyRec. Komptonkoblingen i temperaturudviklingen bruger også H. `thermodynamics_sources` genberegner de afledte ved output. |
| Konform tid og opacitet | `background_tau_of_z` interpolerer konform tid η direkte i z med en særskilt spline. Tidsknuderne i `pth->tau_table` bruges af opacitetens integralspline. Vi afstemte alle 4.861 afrapporterede rækker pr. arm i `history.csv` og `public_table_hex.jsonl` på z, η og opacitet. Øvre snit for begge arme er η(810) = `0x1.57c96c3235bd9p+8` Mpc i det observerede arkiv. Den særskilte kilde-reelle tids- og transportfejl er åben. |

Resten af Q052 kræver stadig sammenhæng mellem de native og kilde-reelle baner, reproducerbarhed i det relevante omfang og validerede fejlgrænser for elektronfraktionen og Thomson-dybden. Identisk fælles H ved første kald gør ikke følsomheden i de to forløb identisk. Q051's sammenligningsgrundlag er videreført fra V151. Arkivindtaget startede ingen nye CLASS-processer eller GitHub-jobs.

## Én næste motor og stopkriterium

**Matematikmotor 2.4.0 → Q052 V153.** Start ved z = 810. Genfind den betingede V73/B★-tilstand eller afstemt H-indeslutning for eksakt a = 1/811. Brug den positive Friedmann-rod og de kildeparametre, der er bundet i V73 og V142. Byg et signeret, udadrettet punktinterval for H_native − H_B★ med særskilte bidrag for binary64-evaluering, forskel i logkoordinat og tabelrepræsentation mod referenceløsning. Brug rækkerne 31687–31688 og det observerede hex-tal. Stop ved en uafhængigt kontrolleret punktgrænse eller ved den første identificerbare manglende reference eller præmis. Opgaven slutter ved punktet. Den certificerer hverken nabocellen, η eller hele Q052.

## Evidens og reproduktion

- **Kilde.** `thermodynamics.c` SHA-256 `d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6`. Linje 1142 for tidsknuderne, 2578–2588 for H, 2663–2670 for HyRec og 2938–2947 for outputkaldet. Arrayberegningen og de to baggrundsrutiner er også læst ved den fastlåste kildeidentitet. [Fastlåst termodynamikkode](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c)
- **Målearkiv.** Alle fire ZIP-hashes matcher GitHub. De tre rådele giver 38/38 match med målemanifestet. Kørsel 45109440243 forsøg 1, commit `4e6c13ed874d9ffc2418faed018fce6796f94e31`. `q052_audit_v152.py` genskaber tabel- og sporvalideringen lokalt med Python 3.10+ og aktive assertions. Læg filen ved siden af `raw/`. Under `raw/` skal `measured/` ligge, udtrukket fra den gzip-komprimerede tar-strøm dannet ved at sammenkæde ZIP-medlemmerne `measured-00`, `measured-01` og `measured-02` i den rækkefølge. Læg kvitteringsarkivets `diagnostics/measured-manifest.json` i `raw/measured-manifest.json`. Kontrolresultatet er `audit-result.json`. [Arkiveret GitHub-kørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/45109440243)
- **Projekthukommelse.** GitHub `main@b16e58cc4d4c2e35f190707f1e69a904ac3c6ff7` indeholder de fire V151-hovedfiler. Alle fire Git-blob-ID'er matcher de lokale bytes. V151's reproduktions-ZIP er lokalt til rådighed og tjekket mod afleveringsmanifestet. [Basekommit](https://github.com/Morfindien/Bubbleverse/tree/b16e58cc4d4c2e35f190707f1e69a904ac3c6ff7)
- **Kontrakt.** Den vedhæftede Matematikmotor 2.4.0 verificerer den valgte motor. V152 bruger Resultatindtag 2.4.0 efter den ældre V151-overleverings henvisning til 2.3.0. Fallback-kontrakten er udfyldt og lokalt kontrolleret uden et installeret fælles schema. Gemningen er versionsopdelt og V151 er præfiks i den samlede journal. V152-filerne er klar til manuel upload til roden af Morfindien/Bubbleverse. Upload kun nye V152-filer på den observerede base eller efter afstemning med nyere commit. Ingen GitHub-skrivning i denne runde.

## Point og milepæl

**86 estimerede point. Total 17.311. Der mangler 689 til 18.000.** 23 for afgrænsning og analyse, 28 for ny sporafstemning og binær evaluering, 11 for genfinding af kilde og arkiv, 24 for indtag, formlernes kontrol og uafhængig vidneafstemning. V151's 98 point og dets SoMe-pakke er videreført uden dobbeltregistrering.

Den nye afstemning af den målte H-rute er registreret som en afgrænset videnskabelig milepæl `Q052-SCI-V152-THERMO-H-TRACE`. Pakke `Q052-V152-THERMO-H-PUBLIC-R1` er klargjort via de eksisterende SoMe- og ToonBee-prompter v1.1. Ingen pointtærskel er nået. Tekst, prompts og den danske læringsforklaring indgår i den nye journalpost. Publiceringsstatus er Klargjort.

## Filer

- `Q052_KORT_RESULTAT_V152.md`
- `Q052_INGESTION_OG_SAMLET_JOURNAL_V152.md`
- `Q052_EVIDENS_V152.json`
- `Q052_MATEMATIKOPGAVE_V152.json`
- `Q052_SOME_V152.txt`
- `q052_audit_v152.py`
- `Q052_OUTPUT_MANIFEST_V152.json`
