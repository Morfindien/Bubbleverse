# Q052 · V150 · Accepterede NDF15-trin verificeret

**23. november 2026 · Resultatindtag og routing 2.3.0**

GitHub-kørsel **45109440243**, forsøg 1, målte de 33 målrækker i begge arme. **Alle rækker 2–34 blev interpoleret** fra 13 accepterede NDF15-trin med numrene 13–25. Trin, indgående skalartilstande, interpolationskoefficienter og rækkeværdier er byteidentiske mellem L og R efter deres respektive filhoveder.

| Kontrol | Resultat |
| --- | --- |
| GitHub-arkiver og indhold | Fire artefakter matcher GitHubs SHA-256. Alle 38 filer i målesættet matcher kørselsmanifestet. |
| Genberegning | V149-kontrollen genskaber alle 66 målrækker bit for bit. Startkontrollen reproducerer de låste V73-input og består. Begge kontrolrapporter blev genskabt byte for byte. |
| Historisk overlap | Række 2–34 matcher V141 byte for byte. Historik, offentlig tabel og baggrundstabellens datadel matcher de arkiverede V69-hash i begge arme. |
| Kontinuitet i de accepterede tilstande | Hvert accepttrin slutter ved samme logkoordinat og samme binære skalartilstand, som næste trin starter med. |
| Orden og dækning | Tre trin har orden 2, fem har orden 3 og fem har orden 4. Tolv accepterede knudepunkter ligger inde i intervallet fra række 2 til række 34. De yderste trin dækker hver sin kant. |

## Eksakt polynomium og binært output

Jeg evaluerede det eksakte polynomium fra de gemte binary64-koefficienter med rationel aritmetik. Den signerede differens beregnes separat for feltet φ og den konforme felthastighed π. Ved målrækkerne bruges den eksakte normaliserede koordinat s = (u − uₕ)/h i hvert trin.

| Absolut forskel | Øvre grænse over de undersøgte punkter |
| --- | ---: |
| Gemt φ minus eksakt interpolationspolynomium ved de 33 rækker | 1,848 × 10⁻⁴⁵ |
| Gemt π minus eksakt interpolationspolynomium ved de 33 rækker | 6,348 × 10⁻⁵¹ |
| Eksakt φ-polynomium minus accepteret venstre tilstand ved de 13 trin | 1,870 × 10⁻⁴⁵ |
| Eksakt π-polynomium minus accepteret venstre tilstand ved de 13 trin | 1,337 × 10⁻⁵⁰ |

De to sidste forskelle kommer fra at tolke de gemte differenser som eksakte reelle tal. De accepterede binære tilstande er stadig eksakt sammenhængende. Ved fælles knuder skal en sammenligning af de eksakte polynomiestykker derfor bevare begge ensidige værdier.

**Valgt opgave til V151.** Matematikmotor 2.3.0 kan nu sammenligne de 13 målte polynomiestykker med V73 ved samme logkoordinat. Beregningen afgrænses til blokken fra række 2 til 34, som allerede har en valideret reference. Den skal også kontrollere de 12 accepterede knuder i blokken og skelne mellem fejl i den interne polynomielle repræsentation og afvigelsen i den efterfølgende gemte spline. Den slutter ved række 34 eller ved første dokumenterede hindring i beregningen.

**Q052 er fortsat INCONCLUSIVE.** De validerede målinger giver forbindelsen mellem de interne trin og de gemte rækker for denne tidlige blok. De certificerede maksimumafvigelser for elektronfraktion og Thomson-optisk dybde over det fulde domæne står åbne.

**88 estimerede arbejdspoint** bringer totalen til **17.127**, med **873** til M018. M017 er registreret som leveret. V150-filerne er klar til manuel GitHub-upload som enkeltfiler.

- [GitHub-kørsel med målinger og artefakter](https://github.com/Morfindien/Bubbleverse/actions/runs/45109440243)
- [Workflow og scripts ved kørslens revision](https://github.com/Morfindien/Bubbleverse/tree/4e6c13ed874d9ffc2418faed018fce6796f94e31)
