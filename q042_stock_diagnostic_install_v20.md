# Q042-STOCKDIAG-V20 — installation og én afgrænset diagnose

Q-042 er fortsat UNRESOLVED. Dette er en diagnosticeringspakke; den er ikke en ny produktion eller en dokumenteret recovery-fix. Assistenten har ikke ændret GitHub eller startet jobs.

Læg filerne ind på disse steder i `Morfindien/Bubbleverse`:

| Leveret fil | Repository-sti |
|---|---|
| q042_stock_diagnostic_v20.py | q042_stock_diagnostic_v20.py |
| q042_stock_diagnostic_tests_v20.py | q042_stock_diagnostic_tests_v20.py |
| q042_stock_diagnostic_contract_v20.json | q042_stock_diagnostic_contract_v20.json |
| q042_install_stock_diagnostic_v20.py | q042_install_stock_diagnostic_v20.py |
| q042_stock_diagnostic_install_v20.md | q042_stock_diagnostic_install_v20.md |
| q042_execution_handoff_v20.md | q042_execution_handoff_v20.md |
| q042_stock_diagnostic_manifest_v20.json | q042_stock_diagnostic_manifest_v20.json |
| q042-stock-diagnostic-v20.yml | .github/workflows/q042-stock-diagnostic-v20.yml |

De gamle V1/V18-filer og den permanente launcher skal blive liggende. Programmet checker det nøjagtige V18-commit ud til runtime. Det nuværende repository skal derfor stadig kunne hente dette commit og Q032-parenten. De to `.resume`-referencefiler er bevaret som rå evidens og skal ikke lægges i repository'et.

Kør i repository-roden:

```bash
python q042_install_stock_diagnostic_v20.py
python q042_install_stock_diagnostic_v20.py --check
```

Helperen tilføjer kun den nye registry-entry og retter README's launcherbeskrivelse og Q042-diagnoseafsnit. Den afviser en konflikt og ændrer ikke eksisterende PROGRAM_ID-statusser. Den committer og dispatcher aldrig. Læg de forberedte filer samt de resulterende ændringer i `bubbleverse_program_registry.json` og `README.md` ind i samme repository-ændring.

Derefter:

**OPEN:** 🚀 BUBBLEVERSE START  
**PASTE:** Q042-STOCKDIAG-V20  
**PRESS:** Run workflow

Workflowet bruger kun `contents: read` og `actions: read`. Dets interne jobs dispatcher ikke andre workflows. Den permanente launcher beholder sin eksisterende dispatch-rettighed.

Den importerede EDE-celle er CamSpec/EDE/FULL fra V18, segment 7. Proben får højst 240 minutters sampling i en separat kopi, med samme prior, seed, samplerindstillinger og `stop_at_error=True`. Observeren tilføjer kun output og CPU-tidsmålinger. Baseline-manifestet ændres ikke; observeren får sit eget manifest. To små syntetiske kørsler skal give byte-identiske resume-filer før proben må starte. Ingen finer checkpoint-frekvens eller ændret covariance-adaptation er implementeret.

CLASS-jobbet evaluerer det præcise fejlpunkt én gang med samme faste input, inklusive `l_max_scalars=9001` og `hmcode`. Det har en 15-minutters compute-grænse. Ingen precision-indstillinger, priorgrænser eller fejlpolitikker ændres.

Før sampling kontrolleres artifact-ID, navn, run-ID, commit, expiry og SHA-256 før unzip. Metadata, rå logs, før/efter-tilstand, observerens kilde og binærhashes bevares. Cache-miss, udløbet artifact, hashfejl, mislykket syntetisk test eller utilstrækkelig jobmargin stopper proben. Der er ingen automatisk retry eller fortsættelse af produktionsceller.

Returnér disse tre artifacts og dette handoff til Result Ingestion & Routing Engine:

- `q042-v20-<RUN_ID>-diagnostic-final`
- `q042-v20-<RUN_ID>-stock-diagnostic`
- `q042-v20-<RUN_ID>-class-diagnostic`

Et grønt diagnostic-workflow er ikke et fysisk Q042-resultat. Collector holder `final_result_gate=UNRESOLVED` og `production_restart_authorized=false`, også hvis holdbar fremdrift observeres.

Diagnosticeringen slutter efter dette ene forsøg. Dens output skal afgøre, om en konkret recovery kan retfærdiggøres, eller om den testede hosted-runtime må dokumenteres som utilstrækkelig. Samme uændrede matrix må ikke bare køres igen. Hvis en senere recovery bruger diagnostic-grenen, skal dens compute og segment 8 indgå i det eksisterende budget; de tidligere segmenter og maksimum 48 må ikke nulstilles.

Lokalt er parser-, provenance-, processtop-, observer-kilde- og installationskontrol udført. Cobaya/CLASS/Fortran-runtime og syntetisk checkpoint-byteidentitet er endnu ikke eksekveret i denne chat; de er obligatoriske runtime-gates, ikke påståede PASS-resultater.
