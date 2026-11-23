# Q052 · V149 · Observatør for accepterede NDF15-trin

**23. november 2026 · Execution/HPC Builder 2.4.0**

Målepakken er klar til **én nominel L/R-kørsel**. Den følger række 2–34 i CLASS’ baggrundstabel tilbage til de accepterede NDF15-trin. Den første kørsel på det nominelle par ligger efter V149. Q052 er fortsat **INCONCLUSIVE**.

| Målepunkt | Registrering |
| --- | --- |
| Accepteret trin efter opdatering af bagudrettede differenser | Trinnummer, begge logkoordinater, skalartilstand ved venstre og højre ende, trinlængde, orden og fejlestimat. |
| NDF15-interpolatorens kald | Gitterrække, skalarkomponenternes maske og de bagudrettede differenser, der bruges til at beregne værdien. |
| Indgang til CLASS’ outputfunktion | Samme trin og række, direkte eller interpoleret gren samt det indgående felt og dets konforme hastighed. |
| Efter en række er skrevet | Skalafaktor, H, feltet og den konforme felthastighed. |

De fire GDB-målepunkter er kontrolleret mod den samme binær med SHA-256 som i V141. De afløser V141’s fire målepunkter efter den etablerede startkvittering. Målekoden læser registret, hukommelsen og tabelrækkerne og fortsætter det observerede forløb. Hver arm kan levere højst 33 række- og 33 trinposter. Hvis et trin producerer flere rækker, deler de trin-ID. Trin uden output i målområdet tælles, og deres tilstande indgår kun, når de leverer en målrække.

Det statiske tjek godkendte 40 instruktioner og tre DWARF-placeringer. C-kontrollen af interpolation brugte 33 syntetiske rækker, testede direkte output og alle fem interpolationsordener og afviste tre konstruerede fejl i målestrømmen. Workflowet bestod actionlint. Wrapperen kunne bygges med de arvede flag og kobles til den fastlåste CLASS-binær efter kontrol af 315 kildefiler.

## Sådan bruges pakken

1. Læg de fem Python-filer i den eksisterende mappe `tools/` i Morfindien/Bubbleverse.
2. Læg `q052-accepted-background-v149.yml` i `.github/workflows/`. Brug denne version, hvis filen allerede er lagt ind.
3. Start **Q052 V149 - Accepted background NDF15 steps** én gang fra GitHub Actions. Workflowet læser de fem kildefiler direkte og genbruger de eksisterende filer `Q052_EVIDENS_V146.json`, `Q052_STARTOBSERVATOER_V136.zip` og `q052_v141.py`.

Kørslen afleverer diagnostik og rådata. Resultatet genberegner hver interpoleret skalartilstand og sammenligner de observerede felter med den fulde gemte tabel. Den lokaliserer første afvigende byte i målområdet mod V141. For fuld historik, offentlig tabel og hele baggrundstabellens datadel registreres hashmatch. V150 skal tage imod de faktisk målte artefakter og afgøre, om de kan bruges til næste numeriske sammenligning.

**130 estimerede arbejdspoint** bringer totalen til **17.039**. **M017** følger som publiceringsklar tekst, kortfilmoplæg og intern evidens. Der mangler **961 point** til M018.

- [Det verificerede V148-input på GitHub](https://github.com/Morfindien/Bubbleverse/tree/2a2da6c39fd14f851f8700791634523427a9529a)
- [Det fastlåste NDF15-outputforløb](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/evolver_ndf15.c#L535-L577)
