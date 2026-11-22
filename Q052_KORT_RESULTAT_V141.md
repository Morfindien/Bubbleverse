# Q052 V141 · Klar til manuel GitHub-kørsel

V141 har klargjort og lokalt valideret målingen af skalar- og neutrinoinput ved det første CLASS-kald. Pakken kan registrere både en bitvis overensstemmelse med V73 og en afvigelse med arm, felt og bits. **Der er startet 0 nye CLASS-processer og 0 GitHub-kørsler. Q052 står fortsat som INCONCLUSIVE.**

## Filer til GitHub

| Fil | Sti i `Morfindien/Bubbleverse` | Formål |
| --- | --- | --- |
| `q052_v141.py` | `q052_v141.py` | Bygger den nye observatør fra den hashbundne V136-kode og sammenligner de to rå kvitteringer |
| `q052-first-rhs-v141.yml` | `.github/workflows/q052-first-rhs-v141.yml` | Manuel kørsel med ét nominelt L/R-par |
| `Q052_INGESTION_OG_SAMLET_JOURNAL_V141.md` | `Q052_INGESTION_OG_SAMLET_JOURNAL_V141.md` | Hele den vedhæftede journal med V141 som ny post |
| `Q052_RESULTATINDTAG_OPGAVE_V141.json` | `Q052_RESULTATINDTAG_OPGAVE_V141.json` | Maskinlæsbar handoff, proveniens, point og filhashes |
| `Q052_KORT_RESULTAT_V141.md` | `Q052_KORT_RESULTAT_V141.md` | Resultat og kørselsvejledning |

De to øverste filer er nødvendige for workflowet. Efter upload på `main`, åbn [Actions](https://github.com/Morfindien/Bubbleverse/actions), vælg **Q052 V141 - First RHS effective inputs**, og vælg **Run workflow** én gang på `main`. Workflowet bruger `Q052_STARTOBSERVATOER_V136.zip`, som allerede er verificeret på `main` ved `6459e99d2889c87eebdf7fe5114b8f4decaa3926`.

Hent `q052-v141-receipts-<run_id>-<attempt>`, og giv det, run-URL'en og `Q052_RESULTATINDTAG_OPGAVE_V141.json` til Resultatindtag og routing 2.3.0. Artefaktet indeholder begge tilgængelige `scalar_start_receipt.json`-filer, `comparison141.json`, build- og procesdiagnostik. Ved et tidligt stop viser `diagnostics/outcomes.txt` det første trin, der fejlede. Større rå eksportdata gemmes som separate GitHub-artefakter med højst 18.000.000 rå bytes pr. del. Manifestet dokumenterer de målte filhashes.

| Status i `comparison141.json` | Betydning |
| --- | --- |
| `CAPTURED_EXACT_INPUT_MATCH` | Begge arme matcher V73 på alle 30 inputfelter, længderne på begge vektorer og de to ledsagefelter ved initialisering. V136's startup-kontrol bestod. |
| `CAPTURED_DISCREPANCY` | Mindst ét input eller en længde afviger i det observerede par. Kvitteringerne giver de målte værdier og comparatorens feltrækker identificerer forskellene. |
| `CAPTURE_INCOMPLETE` | En kvittering, felt-, proces- eller startup-kontrol mangler eller er ugyldig. Diagnostikken angiver omfanget. |

En eksakt overensstemmelse gælder det første observerede RHS-kald i det kommende par. Q052's fejlcertifikat for hele banen og de to certificerede suprema forbliver åbne. V69-eksporternes hashmatch er et særskilt mål i kvitteringen.

## Hvad er verificeret?

- V140-opgavens fingerprint, V136-arkivet, V137-workflowet, CLASS-biblioteket, begge punktfiler og referencehashen bag V73. Det relevante capture er genfundet med samme hash i V135 gennem V136-arkivet. V140-arkivet kunne ikke hentes fra GitHub ved revisionen ovenfor.
- Disassembleringen viser kaldet til `background_functions` ved `0x67aaa` og breakpointet ved `0x67abe` på stien efter returværdikontrollen. De eksisterende NDF15- og final-call-kontroller bruges videre.
- Wrapperen kompilerede med de historiske flag under GCC 14.2.0. Alle 315 fastlåste kildeblobs og loaderens afhængigheder bestod. Der er gennemført 84 syntetiske felt-, kontrol- og læsetests, seks kommandolinjetests samt shell-, Actions- og artefakttests, inklusive en simuleret checkoutfejl. Den kommende runner måler selv adgang til de fire hardware-breakpoints.

Klargøringen er lokal og færdig. Den fremtidige måling bruger den GitHub-runner, hvor V137-job `137135333394` gennemførte. Lokalt mangler GDB, og V137 dokumenterede afvist debuggeradgang i det daværende lokale miljø. GitHub-jobbet beholder V137's 20-minutters grænse. Et praktisk skøn er 4–12 minutter for checkout, preflight, build, ét par og artefakter i selve jobkørslen, plus eventuel køtid. Skønnet er usikkert, især for pakkeinstallation og upload. Første relevante genvurdering er en fejl i hardware- eller kildevalideringen.

**Point** 80 estimerede arbejdspoint. Total **16.297** og **703** til M017. M016 er seneste leverede SoMe-pakke.

- [Q052-opgaven på GitHub](https://github.com/Morfindien/Bubbleverse/blob/6459e99d2889c87eebdf7fe5114b8f4decaa3926/Q052_EXECUTION_OPGAVE_V140.json)
- [Den kvalificerende V137-kørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/44998731473)
