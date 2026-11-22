# Q052 V142 · V141-parret matcher V73 ved første CLASS-kald

**Begge arme matcher bit for bit på de målte skalar- og neutrinoinput ved det første kald til baggrundsligningerne.** Det gælder også skalarmassen m, potentialets konstant B og samtlige 11 neutrinoknuder og 11 vægte. Begge processer afsluttede normalt. Q052 fortsætter, fordi det samlede fejlcertifikat og de to fejlindesluttede maksimumværdier stadig er åbne.

| Kontrol | Resultat |
| --- | --- |
| Direkte sammenligning med V73 | 34/34 pr. arm, inklusive heltal, længder og to initialiseringsfelter |
| GitHub-arkiver og gendannede filer | 4/4 ZIP-hashes, 36/36 manifestposter og 6/6 byteidentiske filer i overlap med kvitteringspakken |
| V69-reproduktion | Historik, offentlig tabel og 40.000 baggrundsdatarækker matcher de respektive V69-hashes i hver arm |
| Første skalafaktor | Otte binary64-trin under værdien før logaritmen, præcis −2⁻⁹⁶ |
| GitHub-job | `137327490481`, run `45061263002`, forsøg 1, status `success` |

Den direkte inputmåling gælder det nye par ved det første uforstyrrede RHS-kald efter `background_functions`. Samme fastlåste CLASS-bibliotek blev brugt med en genbygget wrapper og en libm med anden hash end i V37-arkivet. Det målte eksportmatch gælder på tværs af den miljøforskel. Ved z = 810 bekræfter startkvitteringerne fælles hydrogen og temperaturdifferens og de to fastlåste heliumvalg.

## Hvad der skal prøves nu

**Matematikmotor 2.3.0** får den første gemte baggrundssplinecelle. Den skal bruge rækker 0–1 og deres gemte andenafledte til en fælles-koordinat-fejlgrænse for skalarfelt, hastighed og H. Den skal tage højde for det lille startgab mellem native og matematisk koordinat. Denne nye prøve stopper efter én celle eller den første konkrete valideringshindring og kræver ingen ny CLASS-kørsel. Hele banen og de ultimative elektron- og optiske fejlgrænser bliver stående åbne.

## Filer til Bubbleverse

Alle fire V142-dokumenter er nye filer til roden af `Morfindien/Bubbleverse`. Send journalen, evidensfilen og opgavefilen til Matematikmotor 2.3.0. Opgaven peger på de allerede verificerede kilde- og V73-filer. Evidensfilen indeholder begge kvitteringers oprindelige bytes som UTF-8, bitkontroller og de første to tabelrækker. De gendannede GitHub-arkiver kan bevares med de oprindelige rådele 01 og 02.

- [Q052_KORT_RESULTAT_V142.md](Q052_KORT_RESULTAT_V142.md)
- [Q052_INGESTION_OG_SAMLET_JOURNAL_V142.md](Q052_INGESTION_OG_SAMLET_JOURNAL_V142.md)
- [Q052_EVIDENS_V142.json](Q052_EVIDENS_V142.json)
- [Q052_MATEMATIKOPGAVE_V142.json](Q052_MATEMATIKOPGAVE_V142.json)

**Forskningspoint** 76 nye estimerede point, **16.373** i alt og **627** til M017. Ingen ny SoMe-pakke.

- [Den målte kørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/45061263002)
- [Den verificerede matematikmotor](https://github.com/Morfindien/Bubbleverse/blob/37a41f595e298f72a3743988552d33f8a47ebc69/Bubbleverse_Matematikmotor_2.3.0.md)
