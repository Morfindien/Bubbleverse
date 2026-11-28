# Q052 V158 · Dækningen fra z = 800 til 810 er kontrolleret

**Resultatindtaget bekræfter, at den relative fejl i tabellens udvidelseshastighed højst er 0,0065 % gennem hele det lukkede interval z = 800–810.** Grænsen gælder den fastlåste model, reference og beregningsopsætning. V157-resultatet er registreret én gang.

| Kontrol | Resultat |
|---|---|
| Genkørsel | V157-certifikatet er byteidentisk. Alle seks filer i V157-handoffets referenceliste matcher. |
| Intervaldækning | 1.024 delintervaller fra V157 og 256 fra V155. De deler endepunktet z = 7123223648197587 / 8796093022208 ≈ 809,8167709474. |
| Samling | V157's punktgrænse ligger inden for V155's første delinterval for både absolut og relativ signeret forskel. |
| Samlet relativ forskel | Fra −0,00645999964515 % til +0,00634633591546 %, udad afrundet. Den faktiske fejl kan have begge fortegn. |
| Arkivedata for næste interval | Begge arme har samme H-værdier og andenafledte på de fem udtrukne rækker. Der er to RHS-kald og to outputposter i hver arm på z = 799–800. |

## Første udækkede afhængighed

Umiddelbart under z = 800 mangler en valideret sammenligning af det arkiverede tabelopslag med den samme kilde-reelle reference B★. De verificerede tabeldata dækker begge nødvendige kubiske stykker. V105's skalarcelle 142 ender ved a = 1/801. Dens slutintervaller for φ, X og energi kan bruges som startdata til at afgrænse referencen længere frem. V107 og V108 dokumenterer betingede elektronforskelle for kildeligningerne under z = 800.

## Én opgave til V159

**Matematikmotor 2.4.0 skal afgrænse den signerede H-fejl på z = 799–800.** Opgaven afstemmer slutpunktet fra V105, validerer referencen for det nye interval og medregner koordinat-, spline- og afrundingsfejl. Kildens energilov kan afgrænse referencen fra z = 800, når løsningens eksistens og den positive Friedmann-rod er etableret på hele intervallet. Resultatet skal passe med V157 ved z = 800. Den faktiske forplantning til elektronfraktion og Thomson-dybde er fortsat åben. Q052 forbliver ACTIVE · CONTINUE · INCONCLUSIVE.

## Aktivitet og arkivering

44 estimerede aktivitetspoint fordelt på 11 analyse, 8 beregning, 9 kildearbejde og 16 validering. Samlet **17.725**, med **275** til 18.000. V158 verificerer V157 og afgrænser næste test. SoMe-pakken og læringsforklaringen fra V157 er bevaret i journalen. V158 udløser ingen ny pakke.

V157's journal, rapport, certifikat og handoff matcher indholdet på den observerede main-revision. V158-filerne er klargjort som nye versionsfiler i projektets rod. Upload af V158 afventer. [7b4d2858f4fabc2b4297b4e265f0ce217ed39840](https://github.com/Morfindien/Bubbleverse/tree/7b4d2858f4fabc2b4297b4e265f0ce217ed39840)

Kørsel 2026-11-28T08:26:10+01:00 (Europe/Copenhagen). Evidensen er i Q052_EVIDENS_V158.json. Auditkoden q052_audit_v158.py bruger V157-filerne og begge armes tabel- og sporingsfiler fra det fastlåste V152-målearkiv.
