# Q-042 — V21 bounded diagnostic recovery

Date: 2026-10-04 UTC. Execution mechanism: existing Numerical Execution / HPC Engine + code + read-only GitHub evidence. The current Codex coding/reasoning environment is sufficient. No new motor is required.

CURRENT Q: Q-042. CASE ID: NOT DOCUMENTED.

EXACT QUESTION:
Kan den oprindelige Q041 downstream-portabilitetstest udføres med en ny præregistreret, konvergensrobust inference-strategi, der nøjagtigt bevarer den oprindelige scientific contract — begge native Planck-arme, ΛCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, én identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpræferenceregler — uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at ændre kriterier efter resultaterne?

## A–H. Scientific requirement, journal and provenance

V20 run 37195728280, commit 85518349123e012cce3f21f11800bd988ea5da42, passed the installation/static gate. Stock-probe failed before resume because fetch_artifact opened diag_inputs/ede.zip without creating diag_inputs. This is a software bug in the delivered V20 program. The failure is reproducible locally and repaired by creating archive.parent after source provenance validation, before opening the archive.

The independent CLASS replay completed. Its precise point returned CLASS_EXCEPTION / CosmoComputationError, with the perturbations error reporting negative tau_c=-2.403414e+09 and x_e=-1.174788e-03 at z=5.663014e-02. That output is preserved, including parameters, binary SHA, frozen runtime, exception and timing. It is a numerical execution failure at this point, not physical falsification. No precision, output, reionisation setting or stop-at-error policy is changed to make it pass.

The complete previous handoff and journal are appended below byte-for-byte. This report adds a differential technical record; it does not rebuild scientific history. The 80 optimizer records (78 flag 0; two flag -3), all source IDs actually recorded in the parent, V18 raw states, frozen question/spec/classifier and V19 UNRESOLVED / CONTROLLED_INCOMPLETE science status survive unchanged. No new posterior result exists.

## I–L. Repository and launcher

Search/reuse/patch: V20 program, tests, contract, workflow, installer, current README/registry and actual V20 artifacts were inspected through the GitHub connection. Pinned V18 setup/source environment and Q032 parent are reused. The permanent launcher .github/workflows/00-bubbleverse-start.yml is unchanged.

PROGRAM_ID: Q042-STOCKDIAG-V21. Version 21 identifies the corrected executable and CLASS-import recovery. Prepared registry adds V21 ACTIVE and marks V20 BROKEN; all other registry entries are preserved. README updates only its bounded Q042 diagnosis instructions. Live installation and registration are pending manual application. No commit or dispatch was made here.

## M–O. Runtime, jobs and finite gates

Four jobs: static gate (10 min); exact CLASS artifact import (25 min, no CLASS calculation); one isolated CamSpec/EDE/FULL stock probe (330 min hard job timeout, unchanged 240 min compute soft limit); collector (10 min). Original source segment 7 is copied to one diagnostic branch segment 8. The production 48-segment budget is not reset. Probe settings and seeds, likelihoods, data, bounds, priors and science classification remain frozen. No auto-dispatch or retry is added.

Finite mandatory gates: package/config/registry/README identity; artifact metadata plus cryptographic ZIP validation before extraction; exact reused CLASS JSON identity and parameters; inherited runtime equivalence; observer source removal equivalence; two tiny Gaussian baseline/observer runs with exact resume-byte identity; actual sampler entry; both diagnostic records and final identity/completeness. Diagnostics stay UNRESOLVED scientifically even if complete.

Required runtime gates were not executed locally. They remain before the costly probe. GitHub limits are not redesigned here; this repair retains the previously verified 330/240-minute job design. Setup in V20 #3 completed in approximately two minutes, but total probe runtime is still unknown. The absolute new cosmological probe budget is 4 compute-hours, plus setup and the finite synthetic observer gate. CLASS and BOBYQA compute added by V21: zero.

## P–U. Files, installation and validation

REUSE frozen V18/Q032/environment/scientific inputs and completed V20 CLASS artifact. CREATE versioned V21 program/tests/contract/workflow/installer/notes/manifest/full handoff. PATCH canonical README and registry. KEEP V20 historical code and permanent launcher.

Installation destinations are in q042_stock_diagnostic_install_v21.md. Root Python code stays in the root; only the YAML belongs in .github/workflows. Prepared README_GATE and REPOSITORY_CONSISTENCY_GATE are checked offline; live gates remain pending manual installation. Full compiled observer/likelihood execution and repository-wide HPC tests are not claimed as locally validated.

## V–W. Return and stop

Return both artifacts, q042_stock_diagnostic_final_v21.json, this full handoff and the preserved original CLASS record to the Result Ingestion & Routing Engine. Successful diagnostics may determine a recovery or a documented execution stop; they do not authorize restarting the production matrix. Stop after this single missing probe. No further computation is automatic. Q-042 remains UNRESOLVED; no Motor 14 closure is asserted here.

START THIS (after installation): Q042-STOCKDIAG-V21

## Reused CLASS evidence and claim mapping

Artifact ID 11300612265; name q042-v20-37195728280-class-diagnostic; source run 37195728280; execution commit 85518349123e012cce3f21f11800bd988ea5da42.
ZIP SHA-256 f1e1eee3b1907f5f99fb1b7e4aae374e9452aae257b4e7d74ddef124480c10c5.
Raw CLASS replay record SHA-256 5a68edb84ee7f6db7a81ab9df1aeaaf581a0944a411ffc54645e3bce98345658.

Raw record → CLASS entered successfully and reproduced a numerical exception under the exact frozen point. Run jobs → static success, stock download failure, CLASS replay completed, collector completed. Program source and regression test → missing archive-parent directory causes stock import failure. V21 import wraps the unchanged original record in explicitly labelled reuse provenance; it never rewrites its V20 program/run/commit identity. These are Bubbleverse internal technical evidence, not external publications. No external research was necessary to repair a filesystem operation.

---

# Complete preserved V20 handoff (historical, unchanged)

# BUBBLEVERSE — EXECUTION-MECHANISM / NUMERICAL / HPC HANDOFF

RD OF THE UNIVERSE

DATE AND TIME: 2026-10-04T08:24:40.259590+00:00

**DECISION:** Én afgrænset stock-resume-diagnose + én exact CLASS replay. Ingen ny fuld produktion og ingen påstået recovery-fix. Q-042 forbliver UNRESOLVED.

## A. CURRENT Q

CURRENT Q: **Q-042**  
CASE ID: **NOT DOCUMENTED**. CASE-041 er historisk parent.

QUESTION — EXACT AUTHORITATIVE TEXT:

Kan den oprindelige Q041 downstream-portabilitetstest udføres med en ny præregistreret, konvergensrobust inference-strategi, der nøjagtigt bevarer den oprindelige scientific contract — begge native Planck-arme, ΛCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, én identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpræferenceregler — uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at ændre kriterier efter resultaterne?

## B. RECOMMENDED CHATGPT SETTING

**GPT-6 Astra / High**, hvis den er valgbar, til den koblede runtime-/checkpoint-diagnose og efterfølgende recovery-or-stop-vurdering. Afgrænset agentic coding/Work; Max er ikke begrundet af den nuværende evidens. Til almindelig filinstallation er en generel coding-model tilstrækkelig.

Miljøets agent-interface viser gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-6-luna og gpt-5.6-sol; dette er ikke dokumentation for brugerens modelvælger. Ingen modelændring eller subagent blev udført. Den gamle anbefaling GPT-5.6 er historisk, ikke en permanent regel.

## C–D. CAPABILITIES / EXECUTION DECISION

**USE:** GitHub read-only, lokale hashes/JSON/YAML/analyse og officielt versionslåst PolyChord/Cobaya-kildemateriale. Bibliografisk research kan ikke levere de manglende posteriors.

**EXECUTION MODE:** EXISTING NUMERICAL / HPC MOTOR + ONE BOUNDED DIAGNOSTIC PROGRAM + GITHUB READ.

Kode er nødvendig for at måle runtime-fremdrift; en ny motor er ikke nødvendig. Assistenten har hverken skrevet til GitHub, committet eller dispatcheret. GitHub-plugin blev brugt til retrieval; underliggende artifacts og pinned kode er evidensen.

## E–G. REQUIREMENT, JOURNAL, SOURCES AND PROVENANCE

Bevar den frosne V1 scientific contract, alle 80 optimizer-records inklusive de to flag−3 failures, begge native arme, begge modeller, FULL+fire LOO, kilder, seed map, runtime-pins og klassifikationsregler. Ingen optimizer-start beregnes igen. Ingen Q040-endpoint, hybrid Planck eller cross-arm absolute arithmetic indføres.

**JOURNAL CONTINUITY:** Det komplette vedhæftede V19-handoff er bevaret byte-identisk i Appendix A. Det indeholder den faktisk genfundne historiske journal og dokumenterer sine egne mangler. Dette tillæg erstatter ikke den journal med en ny opsummering.

**KEEP:** V19's tekniske finalisering, 20 kontrollerede posterior-failures/0 completed posterior cells, 80 optimizer-records, fysisk UNRESOLVED, tidligere negative og invaliderede resultater.

**ADD:** To faktiske stock-checkpoint-artifacts er downloadet og deres ZIP-SHA-256 verificeret mod V19-manifestet: EDE artifact 11224420078, run 36979159417, digest `01ac6da88043fbf84fde35713d717cf0b4ea0b53bf5b4d6d13527ada6f563bf6`; LCDM artifact 11170053204, run 36854623733, digest `a1862aa50f99c445dcdb5ed1c4342ba8cfb52ccc7809d2ac4fda0cab8ee5350e`. Begge commit `d0f92c7f2ce53da32818244f8847f8e745e20c4f`.

| Raw state | ndim | nlive | ndead | SHA-256 of raw .resume |
|---|---:|---:|---:|---|
| ede | 18 | 450 | 4051 | `c30e41c032d805d1b987fa362b77db5ad303a382c33d3a96ece13c86a57ed054` |
| lcdm | 15 | 375 | 3376 | `00d26623c43d2807409ac1d0ce1001088b461e6d3298e33561e439d6ce5688fa` |

Begge checkpoints har én cluster og identitetsmatricer for covariance og Cholesky. Deres `ndead` er henholdsvis 9×450+1 og 9×375+1. Det passer med prior-reduktionen fra `nprior=10×nlive`, efterfulgt af den første sampling-udskiftning. Det er stærkere evidens for det konkrete holdbare stadium end et uændret fil-mtime alene. Det siger stadig ikke, hvor meget arbejde der skete i RAM i det efterfølgende segment.

Den pinnede stock-loop skriver `RTI` ved compression-update, **før** den efterfølgende `calculate_covmats(settings,RTI)` i samme update. Stock-reader læser de lagrede matrices; den udfører ikke denne efterfølgende covariance-opdatering ved resume. Den første dokumenterede overgang kan derfor genoptages med de gamle identitetsmatricer. Dette er en præcis kode-/state-observation; det er endnu ikke målt, at den alene forklarer alle 19 timeouts.

Stock `write_resume_file`/`read_resume_file` gemmer/genindlæser RTI men ingen `random_seed`-tilstand. Projektets V13 partial-init-patch gemmer RNG under initialisering, men udvider ikke stock-writeren. Derfor påstås stock-resume ikke at være en byte-identisk fortsættelse af et uafbrudt stokastisk forløb. Der er ikke tilføjet en ny RNG/checkpoint-format-patch i denne leverance.

**UNRESOLVED:** Segment-latens, antal fuldførte replacements i RAM, timing til næste durable write og reproducerbarheden af CLASS-fejlpunktet. Ingen CLASS- eller sampler-evaluering er kørt lokalt.

**PHYSICAL INTERPRETATION:** Uændret. Ingen EDE/ΛCDM-falsifikation, H0-måling eller portabilitetsklasse følger. Tekniske fejl bevares som tekniske fejl.

### New evidence register and mappings

- **I-Q042-V20-001:** De to faktiske V18 terminal ZIP-artifacts og deres raw `.resume`, updated-info og terminal JSON. Underliggende interne Bubbleverse-outputs; byte-hashes ovenfor. Retrieval: GitHub-plugin, lokal SHA/ZIP/state-inspektion.
- **I-Q042-V20-002:** `q042_stock_state_inspection_v20.json`: faktisk lokal offline parser-/identity-kontrol. Ingen runtime-replay.
- **I-Q042-V20-003:** Leveret diagnostic-kontrakt, observer/program, workflow, lokale regressionstests og installationsfixture. Forberedt teknisk mekanisme; ikke et scientific result.
- **K-Q042-V20-001:** PolyChordLite `read_write.F90`, commit `3ade6445bb3719a6db6f6e81f178765545ffc833`. https://github.com/PolyChord/PolyChordLite/blob/3ade6445bb3719a6db6f6e81f178765545ffc833/src/polychord/read_write.F90 . Primær officiel kilde til RTI-serialisering og fravær af RNG-state.
- **K-Q042-V20-002:** Samme commit, `nested_sampling.F90`; supplement til allerede bevaret K-Q042-V19-002. https://github.com/PolyChord/PolyChordLite/blob/3ade6445bb3719a6db6f6e81f178765545ffc833/src/polychord/nested_sampling.F90 . Primær officiel kilde til compression-update og rækkefølgen checkpoint → covariance-opdatering.
- **K-Q042-V20-003:** Cobaya 3.5.6, `classy.py`. https://github.com/CobayaSampler/cobaya/blob/v3.5.6/cobaya/theories/classy/classy.py . Primær officiel kilde til specific-path CLASS-module routing, inklusive den gamle CLASS-wrapper-layout.
- **K-Q042-V20-004:** GitHub officielle Actions limits, læst 2026-10-04. https://docs.github.com/en/actions/reference/limits . Hosted job-grænse 6 timer. Ikke en kosmologisk kilde.

**CLAIM → SOURCE:** Checkpoint-tal og identitetsmatricer → I-Q042-V20-001/002. Stock-write/covariance-rækkefølge og RNG-begrænsning → K-Q042-V20-001/002 + V13-patcher på det frosne V18-commit. CLASS-fejlpunkt → V19's bevarede rå log + I-Q042-V20-003-kontrakt. Runtime-grænse → K-Q042-V20-004. Ingen fysisk claim tilføjes.

## H–I. EXISTING MOTOR / GITHUB SEARCH

**EXISTING MOTOR SUFFICIENT:** YES — Numerical Execution / HPC Engine.

Repository-tree, README, permanent launcher og canonical registry er læst på current main `7af1298c5f1db17557d7671d2ea38ca6d67b7df1`. V18-kode, setup V18/V17/V13/V8/V11, partial-init-patcher og pinned upstream-kode er undersøgt. Version 20 og det nye ID er ikke fundet i tree/registry ved inspektionen.

**KNOWN GOOD REUSE:** V18 setup og partial-init self-test, frosne V1/V18 specs/locks, stored-info resume-route, Q032 parent, exact artifacts og original classifier.

**PREVIOUS FAILURES:** Metadata leak er historisk rettet; V18 stale final filename blev rettet af V19. Nuværende problemer er stock durable-progress og separat CLASS-fejl. Ingen af de gamle fixes genleveres som en ny løsning.

**LAUNCHER:** Den aktuelle permanente launcher findes med displaynavn 🚀 BUBBLEVERSE START. Den checker registry/syntax og dispatcher ét target; den tracker ikke selv child-resultatet.

**REGISTRY:** Ingen Q042-entry findes i den læste canonical registry. Ny entry er forberedt via den differential installer. Live status er PENDING MANUAL INSTALL.

**README:** Har stadig gammel launcher-displaytekst og beskriver kontroller/tracking, der ikke findes i den læste launcher. Helperen korrigerer dette konkret og tilføjer det afgrænsede diagnostic-target.

## J–L. NUMERICAL CONTRACT / PROGRAM_ID / REGISTRATION

**PROGRAM_ID:** Q042-STOCKDIAG-V20  
**LAUNCHER:** 🚀 BUBBLEVERSE START  
**LAUNCHER FILE:** .github/workflows/00-bubbleverse-start.yml  
**REGISTRY:** bubbleverse_program_registry.json  
**TARGET:** .github/workflows/q042-stock-diagnostic-v20.yml  
**REGISTERED LIVE:** NO — prepared installation only.

Én isoleret CamSpec/EDE/FULL resume fra segment 7, seed 421100, ndim18, nlive450, samme `25d/5d/10nlive`, tolerance og infinity-semantik. Ingen ændret blocking, prior eller likelihood. `stop_at_error=True` bevares. Observeren tilføjer kun output, flush og CPU-tidsmåling; den kalder hverken RNG, checkpoint-writer eller covariance-opdatering ekstra. Parent-manifestet forbliver historisk; observer-binæren får eget manifest.

Én præcis CLASS-replay med native input fra den oprindelige CamSpec/ΛCDM/FULL exception, seed er ikke relevant for dette deterministiske punkt. Input inklusive output-string, hmcode, lmax9001 og alle seks variable cosmological værdier er frosset i kontrakten. Ingen reduktion i lmax eller ændret interpolation er en del af testen.

## M–N. RUNTIME / JOB PLAN

Fire jobs: static → to parallelle diagnostics → collector.

1. Static/install/registry/README/package-gates: jobtimeout10min.
2. CLASS replay: setup med cap60min, environment-import cap20min, højst15min compute; jobtimeout120min.
3. Stock probe: setup cap60min, import cap25min, observer rebuild/selftest cap10min; højst240min sampler-compute; jobtimeout330min. En sidste remaining-budget gate kræver mindst240min+10min tilbage, ellers starter den ikke proben. Processgruppen får SIGINT→SIGTERM→SIGKILL og outputmargin.
4. Collector: jobtimeout10min, præcis to diagnostic-records kræves. Manglende records giver DIAGNOSTIC_INCOMPLETE.

Officiel hosted hard-grænse er verificeret til360min. Sampler-softbudgettet øges ikke; maximum48 production-segmenter øges/nulstilles ikke. Den nye diagnostik bruger højst4h15min heavyweight compute plus små synthetic-/inherited setup-selftests. Den samlede nominelle jobtimeout-sum er470runner-minutter. Dette er et loft, ikke en målt runtime; workflowets walltime afhænger af parallelitet, kø, cache og setup. Ingen BOBYQA-compute.

**Checkpoint:** Den eksisterende stock-state læses/kopieres; normale stock-writes observeres. Der er ingen ny recovery-checkpoint-implementering. Diagnostic-state og logs uploades, og ingen automatisk continuation følger.

## O. FINITE MANDATORY TEST PLAN

- T001: package/registry/launcher/README consistency before compute.
- T002: exact frozen source/spec/runtime/data identities, artifact metadata and SHA before extraction.
- T003: raw state/seed/binary-routing identity; original inputs immutable.
- T004: observer-source removal equals baseline source exactly; Gaussian baseline versus observer produces exact `.resume` bytes; observer markers present in actual linked binary's execution.
- T005: one bounded real stock resume; capture before/after SHA+ndead and observed replacement counts, preserve all failures/logs.
- T006: one bounded exact CLASS failure-point replay; preserve return, exception or time-limit outcome.
- T007: two-record completeness/identity at collector; science stays UNRESOLVED regardless of diagnostic success.

**LOCAL VALIDATION:** Nine regression tests, compilation and YAML/JSON parsing were exercised; actual two-cell state inspection passed. Final installation/launcher fixture validation is recorded in the accompanying validation JSON. Cobaya/CLASS/Fortran are unavailable locally. T004's compiled synthetic equivalence and T005/T006's real evaluations are NOT YET EXECUTED; mandatory workflow gates retain that distinction.

## P–R. FILE / README DECISION AND ACTUAL DELIVERABLES

**REUSE:** Frozen V1 spec/classifier, pinned V18 source/setup/partial-init implementation, original datasets/likelihoods and 80 optimizer records.  
**CREATE:** Diagnostic program, contract/source/artifact pins, tests, workflow, differential installer, install instructions, this cumulative handoff and delivery manifest.  
**PATCH:** Canonical registry and README only after manual installation.  
**UNCHANGED:** Permanent launcher, scientific spec, original state and frozen source files.  
**REFERENCE ONLY:** Two preserved raw stock checkpoints and state-inspection/validation reports.

**README ACTION:** UPDATE through the explicit differential helper. Prepared fixture validation is separate from live repository validation.

Individual files; no archive delivery. See `q042_stock_diagnostic_install_v20.md` for exact installation destinations. The .resume reference files belong to evidence, not repository installation.

## S–U. EXECUTION, OUTPUTS AND GATES

After installation/check:

OPEN: 🚀 BUBBLEVERSE START  
PASTE: Q042-STOCKDIAG-V20  
PRESS: Run workflow

Expected outputs: exact import metadata, baseline runtime manifest, observer source/bin hashes, two synthetic checkpoints, probe trace and before/after state, CLASS exact inputs/exception/return, and `q042_stock_diagnostic_final_v20.json`.

**CURRENT ACTUAL COMPUTED SCIENTIFIC RESULT:** NOT AVAILABLE.  
**FINAL_RESULT_GATE:** UNRESOLVED.  
**PRODUCTION_RESTART_AUTHORIZED:** FALSE.  
**LIVE LAUNCHER/REGISTRY/README/REPOSITORY CONSISTENCY:** PENDING MANUAL INSTALL.  
**PREPARED PACKAGE:** local checks described above; full runtime validation pending.

A durable-write observation is useful execution evidence. It is not sufficient to accept the 20-cell scientific result. A touched/rewritten file without increased ndead is not counted as sampler progress. An observer/runtime failure is preserved as a diagnostic failure, not silently rerun.

## V. RETURN ROUTE AND STOP CONDITION

Return to the existing Result Ingestion & Routing Engine with Q-042, exact question, this full cumulative journal, sources/IDs, both diagnostic artifacts, final diagnostic JSON, runtime/observer hashes, actual run ID/commit, test status and unresolved limitations.

The single next decision is **RECOVERY OR DOCUMENTED EXECUTION STOP**, based on observed replacement/durable progress and exact CLASS replay. Further recovery requires a demonstrated cause and a finite semantics-preserving test. This package does not itself approve another matrix. In-memory work without durable output supports investigating write-boundary design; no complete replacement leaves the latency/seed/CLASS path unresolved. A reproducible CLASS exception confirms numerical failure at that exact point, not physical falsification.

Stop this diagnostic after its one probe and one point. Do not add arbitrary variants or unchanged retries. If the exact Q becomes defensibly answerable as a documented feasibility limitation, send the complete case to Motor14. Until that assessment is supported, keep Q-042 open rather than inventing a cosmological answer.

## W. START THIS

**Q042-STOCKDIAG-V20 — only after manual installation and installation check.**

---

## APPENDIX A — COMPLETE PRIOR V19 HANDOFF, UNMODIFIED

Historical declarations in the prior handoff retain their original dates and validation scope. Its explicit statement that checkpoint bytes were not downloaded is updated by this new differential evidence, not silently rewritten. The content below is the entire supplied handoff, byte-identical.

# BUBBLEVERSE — RESULT INGESTION & ROUTING HANDOFF

**RD OF THE UNIVERSE**

**DATE AND TIME:** 2026-10-04T09:51:55+02:00

**STATUS:** CONTINUES  
**CASE ID:** NOT DOCUMENTED — preserved from the authoritative production specification and final output. CASE-041 is the historical parent. No new CASE-042 identifier is silently assigned.  
**CURRENT Q:** Q-042  
**INGESTION RESULT ID:** R-Q042-INGESTION-PROD-V19-001  
**INPUT RESULT ID:** R-Q042-PRODUCTION-PORTABILITY-019

**QUESTION — EXACT AUTHORITATIVE TEXT:**

Kan den oprindelige Q041 downstream-portabilitetstest udføres med en ny præregistreret, konvergensrobust inference-strategi, der nøjagtigt bevarer den oprindelige scientific contract — begge native Planck-arme, ΛCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, én identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpræferenceregler — uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at ændre kriterier efter resultaterne?

**DECISION:** V19 successfully finalized the existing V18 terminal artifact set using the frozen V1 scientific merger. The recovered scientific outcome remains `UNRESOLVED`: 20 terminal PolyChord records, zero completed posterior cells. Nineteen report unchanged stock checkpoints during a resumed segment; the remaining CamSpec/ΛCDM/FULL cell has a documented CLASS computation error. This establishes a technical non-result under the executed conditions. It neither establishes cosmological portability nor proves that the frozen inference strategy is intrinsically infeasible.

One bounded diagnosis can materially resolve the remaining execution uncertainty. Route to the existing Numerical Execution / HPC Engine. Do not restart V2, repeat V19 finalization, repeat any BOBYQA start, or launch another unchanged 20-cell campaign. This handoff authorizes no GitHub mutation or dispatch by the assistant.

---

## RECOMMENDED CHATGPT EXECUTION PROFILE

**AVAILABLE CONFIGURATIONS CONSIDERED:** The environment exposes `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna` and `gpt-5.6-sol`, with reasoning tiers. These are observed agent-interface options, not verified user subscription/model-picker access. No model switch or subagent was performed. Unexposed future systems are not assumed available.

**RECOMMENDED MODEL / MODE:** For this ingestion, GPT-6.1 Sol with High reasoning in Work mode is sufficient. For the next coupled runtime/checkpoint diagnosis, GPT-6 Astra with High reasoning in an agentic coding/Work environment is appropriate if selectable. This escalation is justified by the repeated recovery history and the need to distinguish checkpoint persistence, expensive likelihood work, sampler progress and numerical failure without changing inference semantics.

**RECOMMENDED REASONING LEVEL:** High; maximum reasoning is not required by the evidence currently available.  
**RECOMMENDED EXECUTION STYLE:** Bounded autonomous read-only artifact/code diagnosis, followed by one decision-ready repair specification or a documented recovery limitation.  
**WHY:** The bottleneck is durable progress after stock-resume initialization and numerical evaluation reliability, not a new cosmological hypothesis.  
**RECOMMENDED PLUGINS / TOOLS:** GitHub read-only for pinned code, logs and artifact metadata; Python/file analysis; persistent scientific handoff retrieval; official version-pinned Cobaya/PolyChord/CLASS sources as needed.  
**OPTIONAL PLUGINS / TOOLS:** Literature tools are available but have no demonstrated value for supplying missing posterior evidence. Browser control and further agents are unnecessary for this routing decision.  
**CAPABILITY LIMITATIONS:** No likelihood, sampler or checkpoint was replayed. Actual V18 checkpoint bytes, updated-info files and complete runtime bundles were not downloaded. Their reuse compatibility remains to be established. The full journal was not recovered beyond the complete historical handoff and the version histories actually retrieved. Native web access to two official GitHub pages failed; the GitHub connector successfully retrieved the pinned primary code. One workflow-specific run-list URL was rejected; direct run and purpose-built artifact/job/log reads succeeded. No failed lookup is represented as evidence.

---

## SELECTED NEXT BUBBLEVERSE ENGINE

**BUBBLEVERSE — NUMERICAL EXECUTION / HPC ENGINE**

Exactly one existing engine is selected. Its existence and execution function are documented in the recovered parent handoff and operating history. The engine catalog has not been independently recovered in full; no new engine is invented. Motor 14 is reserved for a documented Q closure. The Report Writer is excluded.

---

## SAMLET JOURNAL

**Continuity status: PARTIALLY RECOVERED, preserved in full to the extent retrieved.** Appendix A contains the complete 167,050-byte Q042 V1 ingestion handoff, including its recovered Q041 handoff, Q031–Q040 journal, source register, claim mapping, source locks and historical execution instructions. It is historical text: old CURRENT Q labels, pending routes and startup claims do not override this handoff. Appendix C carries the complete retrieved V18 technical-history source lock. Missing intervening full journals and old bibliographic identities remain NOT DOCUMENTED. Their absence is not filled with conversation-memory guesses.

| Journal element | Current scientific or technical state | Update |
|---|---|---|
| Q031–Q034 | Native-arm implementation, exact-common-support parent and rejected historical explanatory shortcuts remain as documented in Appendix A. | LEAVES UNCHANGED |
| Q035 | Old binary basin-label discrepancy collapses under classifier harmonization; raw endpoints survive. | LEAVES UNCHANGED |
| Q036–Q038 | Continuous, multivariate fitted-geometry discrepancy survives the documented support comparisons; its physical cause remains unresolved. | LEAVES UNCHANGED |
| Q039 | Tested calibration/precision/native-foreground interventions were insufficient under their conditions. | LEAVES UNCHANGED; KEEP DEAD |
| Q040 | Gaussian and finite defensive-RQMC scientific endpoints failed their validation; forbidden inputs remain forbidden. | LEAVES UNCHANGED |
| Q041 V19 | Historical MCMC noncompletion and mismatch to the original full scientific contract remain preserved. These are distinct from Q042-PROD-V19. | HISTORICAL |
| Q042 V1 | All 20 posterior cells failed before sampling because descriptive metadata leaked into executable sampler arguments. Eighty optimizer records were produced. | HISTORICAL; PRESERVED |
| Q042 V2 delivery | The user-supplied narrative describes a prepared metadata-adapter recovery and manual-install route. It is not a newly executed V2 run or evidence of current live launcher/registry state. | HISTORICAL; CURRENT START INSTRUCTION SUPERSEDED |
| Q042 recovery history | V18 source lock preserves the V3–V18 dependency, identity, matrix, initialization-checkpoint, binary relink, canary and resume-detection repairs. These declarations are retained as provenance, not independently replayed tests. | ADDS RECOVERED HISTORY |
| Q042 V18 posterior branch | All 20 terminal cells have controlled technical failure at segment indices 2–10. Before/after metadata report resumable stock state with unchanged checksum and mtime. | ADDS |
| Q042 V18 main failure | 19 cells report `POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS`; their terminal return code is −2 after a 240-minute soft timeout. | ADDS |
| Q042 V18 distinct failure | CamSpec/ΛCDM/FULL at segment 3 returns 1 without soft timeout. Direct log identifies CLASS perturbation/thermodynamic evaluation failure. | REFINES GENERIC FAILURE LABEL |
| Q042 V18 merger | The collector found its expected 21 artifacts but searched a stale V13 PolyChord filename. | HISTORICAL; FIXED BY V19 FINALIZATION |
| Q042 V19 | Merge-only compatibility filename adapter reuses V1 scientific logic; no new PolyChord or BOBYQA compute. Artifact completeness passes; convergence fails; scientific class is unavailable. | ADDS |
| Q042 optimizer branch | All 80 V1 records retained, 78 flag 0 and two flag−3; each cell has a recorded eligible candidate minimum. | CONFIRMS; NO RECOMPUTATION |
| Q042 inference feasibility | The campaign has not demonstrated the full scientific test. Terminal stock-state failures occurred before the maximum 48-segment policy was exhausted. | UNRESOLVED |
| Bubbleverse physical state | No EDE detection/falsification, ΛCDM falsification, new H0 measurement or downstream portability class follows. Inherited geometry remains unchanged. | LEAVES UNCHANGED |

### Frozen scientific contract

Two native Planck arms × ΛCDM/n=3 EDE × five combinations = 20 cells. FULL comprises P+A6+L6+D2+SN; the four LOO combinations omit ACT primary, ACT lensing, DESI DR2 or the same frozen SN likelihood. Both arms use identical external blocks. Q040 endpoints, pilot science, hybrid Planck likelihood and cross-arm absolute-objective arithmetic remain forbidden.

Location is assessed with `D_x=abs(x_A−x_B)/sqrt(sigma_A²+sigma_B²)`. H0 or fEDE at D≥1, or at least two eligible primary coordinates at D≥1, triggers location materiality. Weakly identified log10z_c/thetai_scf cannot alone trigger it. Contour overlap uses weighted empirical (H0,fEDE) histograms: 80² primary, 64² and 96² stability, threshold 0.50; threshold-side instability blocks classification. Within-arm Δχ² is χ²_LCDM−χ²_EDE; categories and full/LOO classification remain exactly as the raw specification in Appendix B.

The original production spec bytes and seed map remain frozen. V18 has documented deployment envelopes that differ from the old V2 prose: its source lock carries a 315-minute fresh checkpoint window, while the observed terminal resumed segments use 240 minutes. Do not rewrite that historical execution as uniform 240-minute segments or silently adopt it as a new contract. Exact timeout/job envelopes for any proposed follow-up must be read from the pinned workflow and documented; no budget extension is authorized by this ingestion.

---

## NEW RESULT

**RESULT ID:** R-Q042-PRODUCTION-PORTABILITY-019  
**ORIGIN:** User-uploaded `q042-production-final-v19.zip`, corroborated against live GitHub final-artifact metadata and two representative direct job logs.  
**RESULT CLASS:** PARTIAL_RESULT; RUN_FAILURE for the posterior branch; preserved FIT_RESULT records for optimization; VALIDATION_RESULT for merge/identity checks.  
**RESULT STATUS:** TECHNICALLY VALIDATED for artifact identity, record inventory and the documented terminal state. No validated posterior or physical portability result. No scientific ROBUST/REPRODUCED designation.

### DIRECT OUTPUT

| Field | Original value |
|---|---|
| program_id | Q042-PROD-V19 |
| execution_status | CONTROLLED_INCOMPLETE |
| final_result_gate | UNRESOLVED |
| actual_computed_scientific_result | false |
| downstream_portability_classification | NOT_AVAILABLE |
| q042_feasibility_classification | PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED |
| tests_status | COMPLETE |
| JOB_COMPLETENESS / MERGE_COMPATIBILITY | PASS / PASS |
| CONVERGENCE / GLOBALITY | FAIL / PASS |
| source_polychord_final_count | 20 |
| completed posterior cells | 0 |
| source_bobyqa_record_count | 80 |
| polychord_recomputed_in_v19 / bobyqa_recomputed_in_v19 | 0 / 0 |
| scientific_contract_changed | false |

The 29 static gates in the supplied V19 static report are PASS. Their scope is preparation/structure; they do not override CONVERGENCE=FAIL. The independent ingestion audit passed 36 checks of hashes, identity, completeness, eligibility and observed log evidence. Neither report is a production science replay.

### TECHNICAL INTERPRETATION

V19 repairs artifact discovery/finalization, not sampling. It temporarily exposes V18 terminal records and inherited V13-named optimizer records under the V1 merger's expected filenames, calls the original scientific merger, removes shadows and labels the technical envelope V19. The source-final records retain V18 provenance.

`JOB_COMPLETENESS=PASS` means all required terminal records exist. They are all failures. `GLOBALITY=PASS` means four starts are recorded and an eligible finite optimizer candidate exists in each cell; it is not proof of a mathematical global optimum.

For all 20 cells, the JSON records `STOCK_RESUME` both before and after, nonempty resume files, matching stored seed checks and `resume_lifecycle_ok=true`. The checkpoint checksum and mtime are identical across the terminal segment. A successful format/detection check does not demonstrate completion or durable forward progress.

The CamSpec/EDE/FULL terminal log confirms that Cobaya found the existing run and PolyChord reported a stock resume. At the 240-minute interrupt the Python stack is inside `classy.compute()`. The resulting KeyboardInterrupt is the programmed soft stop, not evidence of a human cancellation. It does not establish that one CLASS evaluation consumed the entire four hours, that CLASS was permanently hung, or that no internal sampler work occurred earlier.

The pinned upstream PolyChord main loop writes stock resume state at its compression-triggered update points and at loop termination. Therefore unchanged on-disk state is consistent with work that had not yet reached a durable write boundary. This is an evidence-based candidate explanation, not a demonstrated root cause of all 19 failures. The actual compiled V18 runtime also carries a project partial-initialization patch; its exact executable state and stock-state behavior must be checked before proposing any checkpoint modification. Touching a file, deleting the no-progress gate, or declaring an unchanged checksum as success cannot recover lost work.

The CamSpec/ΛCDM/FULL log identifies a separate CLASS `CosmoComputationError`: negative scattering timescale `tau_c=-2.403414e+09` at `z=5.663014e-02`, with `x_e=-1.174788e-03`. The diagnostic suggests interpolation of a poorly sampled reionization history as a possibility; that suggestion is not independently proven. The precise input point and fixed CLASS settings survive in the raw log appendix. The log's suggestion to set `stop_at_error=False` is not adopted: blanket rejection of numerically problematic in-prior points could change effective support and requires a scientific/numerical justification.

### PHYSICAL INTERPRETATION

No completed, validated posterior matrix supports parameter-location materiality, empirical overlap, complete LOO decisions or a physical portability class. Technical failure does not falsify EDE, ΛCDM or either native Planck likelihood. The data have not been shown incapable of distinguishing the hypotheses; the execution has not supplied the evidence needed to apply the frozen rule.

The existing optimizer candidate values reproduce the earlier within-arm diagnostic differences. Negative values are preserved and not clipped. They are not a final model-preference verdict or certified global optima. `start_values` remain initial values, not posterior means or fitted endpoints.

| Combination | CamSpec candidate Δχ² | HiLLiPoP candidate Δχ² |
|---|---:|---:|
| FULL | −5.202886578 | −7.807410915 |
| NO_ACT_PRIMARY | −0.160213990 | 5.070110608 |
| NO_ACT_LENSING | −6.102295794 | −2.545895003 |
| NO_DESI_DR2 | −4.648358940 | −4.743352581 |
| NO_SN | 2.781484517 | −7.122963998 |

These require no new optimization campaign for current routing. No absolute objective is subtracted across arms.

**ANOMALY STATUS:** Preserved technical checkpoint discrepancy and one numerical CLASS failure. No new candidate physical anomaly is established. Existing optimizer discrepancies and inherited geometry survive without reinterpretation.

---

## INTERNAL RESULT PROVENANCE

| Field | Recorded/recovered value |
|---|---|
| Repository | https://github.com/Morfindien/Bubbleverse |
| V19 merge run | https://github.com/Morfindien/Bubbleverse/actions/runs/37185888043 |
| V19 execution commit | `7af1298c5f1db17557d7671d2ea38ca6d67b7df1` |
| V19 workflow | `.github/workflows/q042-production-v19.yml` |
| V19 run created / updated | 2026-10-04T07:28:30Z / 2026-10-04T07:29:04Z |
| Live Actions status | completed / success, attempt 1; technical execution status only |
| Final artifact | ID 11296144394; q042-production-final-v19; 30,912 bytes; created 2026-10-04T07:29:02Z |
| Uploaded ZIP SHA-256 | `394baf90b4f28b821c5071f3e59636c64ea81f968f1343a28a23ae0475a208d0`; exact match to live artifact digest |
| Final JSON SHA-256 | `95f024b5ffdde740ae796e54a7dbd02340c14f340b7ea935b70082e0ea607e07`; exact match to artifact index |
| V18 source root | 36731879692 |
| V18 execution commit | `d0f92c7f2ce53da32818244f8847f8e745e20c4f` |
| V18 failed collector run / job | 37151674348 / 111286678009 |
| V18 collector defect | V13_POLYCHORD_FINAL_COUNT_GATE=FAIL; stale final filename |
| V18 program SHA-256 | `19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962`; matched retrieved pinned source |
| V18 source-lock SHA-256 | `6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde`; matched retrieved bytes |
| V1 scientific spec SHA-256 | `41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c` |
| V1 source-lock SHA-256 | `0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56`; matched retrieved bytes |
| BOBYQA origin | V1 root 36133813540; commit `6c44a4117449145afd0a3ae6eb238490686a8c6d` |
| Optimizer reuse lineage | computed_by V1; imported records retain V18 reuse envelope and V13-named source files; V19 creates no new records |
| CamSpec/EDE/FULL terminal evidence | run 36979159417, job 110749510805, segment 7 |
| CamSpec/ΛCDM/FULL terminal evidence | run 36854623733, job 110344069372, segment 3 |
| Source artifact selection | 21 exact-name, exact-V18-commit artifacts; IDs, digests and producing run IDs carried in raw manifest |
| Selection manifest SHA-256 | `0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f` |
| Runtime locks | Cobaya 3.5.6; NumPy 1.26.4; Py-BOBYQA 1.5.0; PolyChordLite 1.22.2/base commit `3ade6445bb3719a6db6f6e81f178765545ffc833`; project checkpoint patch retained in source lock |
| Observed log Python | 3.11.16; locked major/minor 3.11 |
| Observed execution | serial worker, mpi_ranks=1; GitHub hosted runner; compiler commands and environment survive in logs |
| Per-cell state | all 20 seeds/config hashes, terminal checkpoint metadata, parents, segments and elapsed values in unmodified final JSON |
| CPU total / full runtime audit / exact sample counts | NOT DOCUMENTED; terminal elapsed values are not a complete campaign accounting |

The upload-to-GitHub-final-artifact identity is independently checked. The 21 underlying V18 ZIPs were not redownloaded to independently reproduce their digest verification; the manifest and V19 workflow report that verification. The distinction survives in the audit. No branch, file, registry, workflow or scientific state was modified on GitHub.

---

## WEB / PLUGIN / TOOL RESEARCH

**RESEARCH PERFORMED:** YES — targeted technical primary-source and internal provenance research.  
**CAPABILITIES USED:** Library historical handoff recovery; local ZIP/JSON/hash analysis; GitHub pinned code, direct run/artifact/job metadata and direct logs; attempted native web opens of official sources.  
**QUESTIONS INVESTIGATED:** Does the upload belong to the final merge run? Does artifact completeness imply posterior success? What do the terminal records and representative runtime logs establish? Can stock checkpoint cadence materially explain the next bottleneck? Which old journal and optimizer results survive?  
**NEW EXTERNAL EVIDENCE:** Version-pinned official PolyChord main-loop and Cobaya wrapper code; methodological context only. No new cosmological observation or constraint.  
**NEW SOURCES:** I-Q042-V19-001–009 and K-Q042-V19-001–002 below.  
**CONTRADICTORY EVIDENCE:** All 20 controlled failures contradict interpreting V19's green run, artifact count or static PASS as scientific success. Logs refine a generic runner/numerical label to one concrete CLASS error. Stock-update code prevents inferring zero internal computation solely from an unchanged checkpoint.  
**IMPACT ON INTERPRETATION:** Finalization recovery succeeded; inference remained incomplete. The current blocker is stock-state durability/latency and numerical evaluation, not the historical two-field V1 parser defect.  
**IMPACT ON JOURNAL:** Add terminal inventory and runtime refinements, preserve full previous journal, freeze physical conclusions.

Research stops here. Wider literature and repeat finalization cannot supply missing validated posteriors or change the single selected route. Further runtime diagnosis belongs to the selected engine.

---

## ACTIVE SOURCE REGISTER

The full inherited source register and mappings are actually reproduced in Appendix A, including historical K and I IDs and their disclosed gaps. They are neither renumbered nor silently upgraded. Appendix C retains the exact software/data identities and repair history.

| New ID | Source and evidence class | Supported scope |
|---|---|---|
| I-Q042-V19-001 | User-uploaded q042-production-final-v19.zip; eight raw members reproduced in Appendix B; internal Bubbleverse result | Authoritative output, spec, locks, artifact selection and terminal records |
| I-Q042-V19-002 | GitHub run 37185888043 and artifact 11296144394; metadata reproduced in Appendix D | Current merge execution identity and exact uploaded ZIP digest |
| I-Q042-V19-003 | https://github.com/Morfindien/Bubbleverse/blob/7af1298c5f1db17557d7671d2ea38ca6d67b7df1/q042_production_v19.py | Merge-only adapter and original classifier reuse; internal code |
| I-Q042-V19-004 | https://github.com/Morfindien/Bubbleverse/blob/d0f92c7f2ce53da32818244f8847f8e745e20c4f/q042_production_v18.py | Segment controller, interrupt policy, checkpoint-progress rule; pinned source hash matched |
| I-Q042-V19-005 | https://github.com/Morfindien/Bubbleverse/actions/runs/36979159417/job/110749510805; complete retrieved log in Appendix E | Actual stock-resume invocation and interrupt in CLASS for representative no-progress failure |
| I-Q042-V19-006 | https://github.com/Morfindien/Bubbleverse/actions/runs/36854623733/job/110344069372; complete retrieved log in Appendix E | Exact CLASS exception, input point, timing and settings |
| I-Q042-V19-007 | Complete historical Q042_PROD_V1_INGESTION_HANDOFF.md; Appendix A; source identity libfile_03d75535bb188191ae16252bc97e9592 | Recovered scientific journal, Q identity, historical sources and rejected material |
| I-Q042-V19-008 | Complete V18 source lock; Appendix C; pinned V1 source lock carried in Appendix A | Technical repair history and frozen implementations; source-lock declarations remain declarations |
| I-Q042-V19-009 | This ingestion's deterministic audit, source and output in Appendix F | 36 local identity/consistency checks and within-arm diagnostic arithmetic |
| K-Q042-V19-001 | https://github.com/PolyChord/PolyChordLite/blob/3ade6445bb3719a6db6f6e81f178765545ffc833/src/polychord/nested_sampling.F90; official primary code, retrieved 2026-10-04 | Stock-resume read and compression-triggered durable-write cadence; not proof of the cause of every failure |
| K-Q042-V19-002 | https://github.com/CobayaSampler/cobaya/blob/v3.5.6/cobaya/samplers/polychord/polychord.py; official primary code, retrieved 2026-10-04 | Pinned sampler interface and run path; does not replace project-patched binary audit |

**Inherited active implementation locks:** n=3 EDE class_ede `5a131c91d657dd9a7c6364cc45b038710f8d0d97`; HiLLiPoP `a09ddde3e7ce11df99f74685feb1f1764cafb251`; ACT primary `880eacb40d66722eb1c32d7b5621e91662b4d808`; ACT lensing `b386ddbb5821c1216c709f051c9289292f174d30`; DESI data `b7b8a36e9bccb063081f811f323cada21ab5fbdd` and Cobaya definition `b76b6fed2a6c8c5594c6f92d5058bef10079746a`; frozen `sn.pantheonplus`. Titles, release labels and original URLs remain in the reproduced parent source register. No new runtime-data validation is claimed from a lock alone.

---

## CLAIM-TO-SOURCE MAP

| Claim | Source relationship |
|---|---|
| C-Q042-V19-001: Exact Q, matrix and original decision rules remain authoritative | I-Q042-V19-001, 007, 008 |
| C-Q042-V19-002: Uploaded ZIP is the actual V19 final artifact | I-Q042-V19-001, 002, 009 |
| C-Q042-V19-003: 20 terminal records, zero completed posterior cells; 19 no-progress failures and one other failure | I-Q042-V19-001, 009 |
| C-Q042-V19-004: Representative no-progress worker resumed stock state and was interrupted inside CLASS | I-Q042-V19-004, 005 |
| C-Q042-V19-005: Generic CamSpec/ΛCDM/FULL failure is a specific CLASS numerical exception | I-Q042-V19-006 |
| C-Q042-V19-006: Unchanged persisted state does not alone prove no in-memory work | I-Q042-V19-004, 005; K-Q042-V19-001; inference explicitly bounded |
| C-Q042-V19-007: V19 adds no optimizer or posterior compute; merger reuses frozen science | I-Q042-V19-001, 003, 009 |
| C-Q042-V19-008: 80 optimizer records and their original failure flags survive | I-Q042-V19-001, 007, 009 |
| C-Q042-V19-009: No physical portability class is warranted | C-Q042-V19-001, 003; original completeness/classifier contract |
| C-Q042-V19-010: Bounded diagnosis is material, unchanged dispatch/remerge is not | C-Q042-V19-003–006; routing inference, not measured cosmology |

All inherited claim-to-source relationships survive verbatim in Appendix A. Unknown bibliographic mappings remain explicitly unknown.

---

## WHAT CHANGED

The case has advanced from the historical V2 preparation narrative to an executed V18 terminal matrix and a verified V19 merge-only finalization. The obsolete filename defect is resolved. The remaining blockers are documented stock-checkpoint nonprogress and one independently observed numerical CLASS error. The record count, successful merge and static tests now have explicitly limited meanings.

## WHAT DID NOT CHANGE

Exact CURRENT Q, recorded CASE ID, scientific spec bytes, data/model matrix, all original thresholds, seed map, Q040 firewall, completed optimizer evidence and the physical status of the inherited discrepancy remain fixed. No new scientific program ID is created by ingestion. Actual posterior inference and its final classification remain unavailable.

## FALSIFIED / REJECTED / SUPERSEDED MATERIAL

- **SUPERSEDED AS CURRENT ACTION:** Start Q042-PROD-V2; the attached newer output controls this ingestion.
- **SUPERSEDED AS CURRENT BLOCKER:** All cells die before sampling because of the V1 metadata leak. V18 reaches stock resume and likelihood evaluation in observed logs.
- **REPAIRED:** V18 stale merge-filename discovery, within V19 finalization's documented scope.
- **REJECTED:** Green Actions status, 21 artifacts or static PASS proves convergence/scientific success.
- **REJECTED:** Another unchanged V19 merge or BOBYQA campaign could create the missing posterior evidence.
- **NOT ESTABLISHED:** All 19 workers are permanently hung; one likelihood call consumed each entire segment; every computation was lost; exact current checkpoint reuse is compatible; the 48-segment ceiling was exhausted.
- **KEEP DEAD:** All inherited Q040 invalidated endpoints and earlier rejected physical shortcuts; no threshold change, cross-arm absolute χ² evidence, hybrid likelihood or unsupported global-optimum claim.
- **PRESERVED:** Negative optimizer candidate differences, two flag−3 failures, all terminal checkpoint metadata and the CLASS error point.

No physical model is falsified by this ingestion.

## OPEN UNCERTAINTIES

1. Did stock-state work fail to reach a durable write boundary because of coarse update cadence, a very costly/stalled likelihood evaluation, or another specific runtime/checkpoint defect? No-progress metadata alone does not discriminate.
2. Can the identified V18 stock state be continued with exact software/state compatibility and a scientifically neutral durability repair, without restarting all cells?
3. Is the CamSpec/ΛCDM numerical error a demonstrable precision/interpolation issue under the frozen scientific domain? Its treatment must not silently change effective likelihood support.
4. Complete posterior geometry, convergence and original full/LOO classification remain unavailable. Full historical journal continuity and independently checked runtime-data/checkpoint bytes remain partial.

Only the first three, as one execution-recovery decision, are the next material task. Do not turn each uncertainty into a separate campaign.

---

## Q-COMPLETION GATE

**STATUS: NOT YET SATISFIED.**

The executed campaign did not complete the intended test. However, the exact Q asks whether the preserved strategy can execute that test; a known persistence/latency ambiguity and one specific numerical failure remain materially diagnosable. The terminal cells stopped at segment indices 2–10, below the frozen maximum of 48. Closure as a physical no/yes, data inability to distinguish, or intrinsic strategy impossibility is not supported.

This is not an instruction for indefinite repair. One bounded recovery-or-limitation decision is allowed next. A subsequent documented conclusion that no scientifically neutral, resource-bounded recovery is justified can close the execution-feasibility Q as INCONCLUSIVE under the available conditions, without asserting a physical portability answer.

## MATERIAL-REVERSAL TEST

**PASS for targeted diagnosis.** Distinguishing slow/coarse durable-write cadence from an actual runtime dead end can change whether the exact frozen test is executable. Resolving the existing CLASS error point can also change the baseline cell's execution feasibility. Another unchanged full dispatch, new optimizer starts, repeated merge, wider cosmology search or relaxed scientific gates fails this necessity test.

## ROUTING REASON

The existing Numerical Execution / HPC Engine owns checkpoint serialization, runtime compatibility, latency diagnostics, exact-point numerical checks and bounded recovery design. A theory/anomaly/publication engine cannot create the required valid posterior evidence. No new engine is needed.

---

## NEXT TASK

**Produce one decision-ready stock-resume/numerical recovery specification, or one documented conclusion that a justified bounded recovery is unavailable, using the existing V18 artifacts first.**

1. Inspect the already identified terminal state for two representative failure types: CamSpec/EDE/FULL run 36979159417/job 110749510805 and CamSpec/ΛCDM/FULL run 36854623733/job 110344069372. Their parent checkpoint run IDs are recorded in the final JSON. Resolve exact artifact names, commits, digests, updated info, raw stock state, available dead/live/stats files and original logs. Preserve bytes. Additional cells are read only if these representatives expose a concrete arm/model-specific uncertainty.
2. Audit the exact compiled/patched PolyChord path, stock write cadence, runtime counters and recorded likelihood latency. Determine whether work is progressing in memory without durable commits, trapped in a particular evaluation, or rejected by an incorrect state/progress check. Do not label mtime touches or gate removal as progress.
3. Audit the precise CLASS error point and settings already recorded in the ΛCDM log. If a single-point replay is needed, define its finite timeout prospectively. Do not narrow priors, change model/data, substitute arbitrary −∞ likelihoods, or disable error handling globally to conceal numerical failures. Any precision/domain change must be explicitly classified and justified.
4. Reuse all 80 V1 BOBYQA records. Keep both flag−3 records. No new optimizer start is required. Reuse V18 posterior/checkpoint state only after actual byte/version compatibility is established; this handoff's JSON metadata is not such a proof.
5. If a repair is supported, specify the exact execution/serialization change, state/RNG equivalence requirements, frozen science, one finite diagnostic budget and one pilot before any fan-out. A synthetic interrupt/resume test must compare actual durable state and resumed output to uninterrupted output, not merely a marker file. New safe-point checkpoint writes must preserve complete sampler state and not alter evidence weights, stopping rules or the trajectory contract. A need to change inference semantics is a versioned scientific change, not a technical relabel.
6. The prospective diagnostic computation budget, if necessary after artifact/code audit, is at most one stock-resume pilot segment with the existing 240-minute soft window, plus one bounded exact-point CLASS replay; no whole-matrix launch or budget extension. Remaining production segment accounting must carry already consumed work rather than resetting the 48-segment allowance silently. These are prospective handoff limits; this ingestion starts neither computation.
7. Deliver exactly one recovery-or-stop decision. If repairing repository functionality, follow the inherited BV-EXEC-README-001 instructions: inspect actual README/launcher/registry/workflows, supply differential documentation and consistency checks for the prepared package. GitHub remains read-only for the assistant; deliver individual files for manual installation. Pure diagnosis does not require manufacturing a README change or new program ID.

## FIXED / FROZEN ELEMENTS

The exact question and original spec bytes; recorded CASE ID; native Planck arms; ΛCDM and n=3 EDE definitions; identical frozen external likelihoods/priors/bounds and seeds; original empirical-overlap and materiality/model-preference rules; no Q040 or pilot science; no cross-arm absolute objective; original V1 optimizer records; immutable V18/V19 evidence and parent commits; finite production stopping contract and consumed-segment accounting; no unannounced budget extension or automatic full-matrix restart.

## VARIABLE ELEMENTS

Diagnostic extraction, representative state inspection, likelihood latency instrumentation and prospective state-preserving technical recovery design. No scientific change is made by the audit. A demonstrated necessary numerical/domain change must be explicitly versioned and evaluated against the exact Q, not called a byte-identical recovery.

## SUCCESS CONDITION

The next engine identifies the specific material limitation and delivers a justified finite recovery plan or stop decision. A recovery must preserve science and prove actual compatible durable progress before fan-out. A physical class requires all original posterior validity/convergence, eligible within-arm fit and FULL/LOO/classifier conditions; successful serialization or a green pilot alone is insufficient.

## FAILURE / FALSIFICATION CONDITION

Unverifiable state compatibility, inability to preserve numerical semantics, inability to distinguish/recover the bottleneck within the defined finite diagnostic budget, or need for unsupported likelihood-support changes blocks automatic recovery. Record a methodological/execution limitation. No missing/failed evidence is transformed into a physical falsification, and no original class is emitted when its gates fail.

## STOP CONDITION

**Stop this ingestion now:** raw result identity, all terminal states, representative runtime refinements and a material single route are documented. More retrieval or repeat validation is not necessary for routing.

**Stop the next diagnosis after one recovery-or-limitation decision.** Do not create an indefinite version/test loop. If the frozen test completes with defensible evidence, or if bounded diagnosis establishes that no further necessary, materially informative recovery is justified under the available conditions, close the exact Q with its honest epistemic scope and route the complete case directly to **BUBBLEVERSE — MOTOR 14: AUTONOMOUS UNIVERSE REVISION**. An INCONCLUSIVE execution-feasibility closure must state that downstream physical portability remains unmeasured.

---

## PRESERVATION AND DELIVERY

This handoff embeds the entire recovered parent handoff, all eight raw uploaded JSON members, the recovered V18 history lock, retrieved run/artifact metadata, both representative raw logs and the deterministic ingestion audit. Historical text remains historical; no missing old artifact or bibliography is invented. JSON member byte hashes and the parent handoff hash are recorded in the preservation manifest. Embedded text can be reconstructed using UTF-8 and the retained terminal newlines. The original uploaded ZIP remains the authoritative archive.

No production program is implemented, registered or dispatched by this ingestion. README_GATE and REPOSITORY_CONSISTENCY_GATE are **NOT APPLICABLE to a repository modification**, because none is delivered. The handoff does not assert live launcher/registry readiness for an uncreated successor.


# APPENDIX A — COMPLETE PRESERVED HISTORICAL HANDOFF

The following text is historical. All CURRENT Q labels, routes and instructions inside this appendix are subordinate to the current Q-042/V19 ingestion decision. Materialized source bytes: 167050; SHA-256: `3f608302a625abafd28d9ada487ee4a2c17681717be62e8e84d97af574a993c4`.

<!-- BEGIN PRESERVED PARENT TEXT -->
# BUBBLEVERSE — RESULT INGESTION & ROUTING HANDOFF

**RD OF THE UNIVERSE**

**DATE AND TIME:** 2026-09-26T22:10:27+02:00

**STATUS:** CONTINUES  
**CASE ID:** NOT DOCUMENTED — retained exactly from the production specification, source lock and final result. CASE-041 belongs to the historical parent; CASE-042 is not silently assigned.  
**CURRENT Q:** Q-042  
**INGESTION RESULT ID:** R-Q042-INGESTION-PROD-V1-001  
**INPUT RESULT ID:** R-Q042-PRODUCTION-PORTABILITY-001

**QUESTION — exact authoritative text:**

Kan den oprindelige Q041 downstream-portabilitetstest udføres med en ny præregistreret, konvergensrobust inference-strategi, der nøjagtigt bevarer den oprindelige scientific contract — begge native Planck-arme, ΛCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, én identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpræferenceregler — uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at ændre kriterier efter resultaterne?

**DECISION:** The submitted V1 campaign ended with a controlled technical non-result. All 20 PolyChord cells failed at input validation, before posterior sampling. The original scientific feasibility question remains unresolved. A specific, demonstrated configuration defect is materially repairable, so the next route is the existing Numerical Execution / HPC Engine. This is not a Motor 14 closure and does not authorize another unchanged campaign.

---

## RECOMMENDED CHATGPT EXECUTION PROFILE

**AVAILABLE CONFIGURATIONS CONSIDERED:** The environment advertises `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol` and `gpt-5.6-terra` in its agent configuration interface, with reasoning tiers. These advertised choices do not verify the active parent model, the user's model picker, or subscription access. No model switch or subagent invocation was performed. No unexposed future model was assumed to exist.

**RECOMMENDED MODEL / MODE:** For the next bounded coding repair, `gpt-6-sol` with high reasoning in an agentic coding environment is the task-matched recommendation, if selectable. The current high-reasoning Work environment is also adequate. `gpt-6-astra` with high reasoning is appropriate if subsequent scientific evidence conflicts require deeper adjudication; maximum reasoning has no demonstrated benefit for the identified two-field interface defect. Fast/general models can format inventories but need not be separately invoked.

**RECOMMENDED REASONING LEVEL:** High.  
**RECOMMENDED EXECUTION STYLE:** Autonomous file/repository analysis and bounded implementation verification, respecting the existing no-GitHub-write/no-dispatch instruction.  
**WHY:** The bottleneck is translating a frozen scientific specification into valid sampler arguments, preserving provenance and completed optimization outputs. It is not a new cosmological hypothesis.

**RECOMMENDED PLUGINS / TOOLS:** Local Python and file analysis; GitHub read access to pinned code, logs and artifacts; persistent file delivery; official Cobaya/Py-BOBYQA documentation when necessary.  
**OPTIONAL PLUGINS / TOOLS:** None required for the present routing decision. Browser automation, broad literature searches and additional agents add no material information here.  
**CAPABILITY LIMITATIONS:** No production likelihood or sampler was rerun. The complete historical Q-042 journal was not found. The 278 MB runtime artifact was identified but not downloaded; runtime/data hashes inside it were not independently re-audited. Available model names are an environment observation, not a permanent catalog.

---

## SELECTED NEXT BUBBLEVERSE ENGINE

**BUBBLEVERSE — NUMERICAL EXECUTION / HPC ENGINE**

This established engine is identified in the recovered historical handoff and the retrieved HPC operating prompt. Exactly one engine is selected. The Report Writer is excluded.

---

## SAMLET JOURNAL

**Continuity status: PARTIALLY RECOVERED; preserved in full to the extent actually retrieved.** The four-file uploaded ZIP contains a final result, artifact index, frozen specification and source lock; it contains no cumulative journal. The recovered Q041 handoff explicitly already disclosed gaps in Q041 V1–V18 history and old K-ID bibliography. A complete Q042 chain of all intermediate handoffs was not located by bounded Library and repository search. Those gaps remain **NOT DOCUMENTED**, rather than being reconstructed as facts.

Appendix A carries the complete retrieved extended Q041 handoff, including its Q031–Q040 journal, sources, original outputs and historical routing instructions. Its 2026-09-23 status/routing is **HISTORICAL**, not the current route. The shorter earlier edition is preserved separately in the evidence package. Appendix B carries the full Q042 V11 technical-history source lock. Appendix C carries the complete authoritative production specification and production source lock. Current Q remains Q-042 throughout.

| Journal entry | Preserved or new state | Update |
|---|---|---|
| Q031–Q035 | Historical native-arm implementation, harmonization and classifier findings remain as recorded in Appendix A; raw results and rejected historical label interpretations remain recoverable. | LEAVES UNCHANGED |
| Q036–Q039 | The inherited continuous fitted-geometry discrepancy and its tested localization/intervention history remain unresolved at the physical-cause level. No new result here modifies those findings. | LEAVES UNCHANGED |
| Q040 | Failed single-Gaussian and defensive-RQMC science endpoints remain forbidden scientific inputs. | LEAVES UNCHANGED; FIREWALL PRESERVED |
| Q041 V19 | Historical MCMC noncompletion and the documented difference between its executed contract and the original requested test remain recorded. Its outputs are not imported as valid Q042 posterior evidence. | HISTORICAL; LEAVES UNCHANGED |
| Q042 execution strategy | The recovered source lock records selection of PolyChord plus four external Py-BOBYQA starts per cell and rejection of another unchanged V19 MCMC campaign. | PRESERVED |
| Q042 preflight history | MPI prerequisites, cache transport, external-component identity, separate MPI interpreter lifecycle, stored resume-info, bounded warning harvest and merge dependency bootstrap remain recorded in full in Appendix B. | PRESERVED |
| V11 preflight authority | Production specification records PREFLIGHT_PASS, program hash `3dd736334f355d9f5e2232c2900c563587e8330413185fd9f897193c66f46f32`, spec hash `183139bf7bab9dcf1bf0e591762dbb1ddb4160244065a400709e2522d3241ebe`. These are technical authority references, not posterior evidence. | PRESERVED; NOT PROMOTED |
| Q042 scientific contract | Two native Planck arms × two models × five combinations; same external blocks; original decision rules and no Q040/cross-arm absolute-objective shortcut. | LEAVES UNCHANGED |
| Q042 V1 posterior branch | 20/20 terminal records, 0/20 completed posteriors, all failed in fresh segment 0 with return code 1 and no checkpoint. | ADDS |
| Q042 V1 root cause | `production_pc()` copies descriptive metadata into Cobaya sampler arguments. Both representative arm logs reject `seed_policy` and `max_ndead_runtime_encoding`. The same leak is reproduced in all 20 generated dictionaries. | ADDS; TECHNICALLY DOCUMENTED |
| Q042 V1 optimization branch | 80/80 recorded external starts; 78 flag-0 eligible results and two preserved flag−3 failures. Every cell has an eligible recorded best candidate. | ADDS; PARTIAL RESULT |
| Q042 diagnostics | Candidate within-arm objective differences can be calculated; posterior means, uncertainties, D_x and empirical overlaps cannot. | ADDS; DIAGNOSTIC ONLY |
| Earlier production readiness claim | Static checks and V11 preflight did not validate the exact production sampler dictionary. Treat “production built/33 gates passed” as historical validation of a limited scope, not demonstrated runtime readiness. | REFINES; READINESS INFERENCE CONTRADICTED |
| Q042 physical answer | No downstream portability class, EDE detection/falsification, new physics, or changed H0 benchmark is established. | LEAVES UNCHANGED |
| Current route | One bounded technical recovery task goes to Numerical Execution / HPC; completed optimization records are preserved. | ADDS |

---

## NEW RESULT

**RESULT ID:** R-Q042-PRODUCTION-PORTABILITY-001  
**ORIGIN:** User-supplied production ZIP; corroborating pinned repository source, GitHub run/artifact metadata and two direct job logs.  
**RESULT CLASS:** PARTIAL_RESULT; RUN_FAILURE in the posterior branch; NUMERICAL_RESULT in the optimization branch; VALIDATION_RESULT for the ingestion audit.  
**RESULT STATUS:** The technical failure and record aggregation are documented. The production science result is **UNRESOLVED / NOT AVAILABLE**. No ROBUST or REPRODUCED cosmological status is assigned.

### DIRECT OUTPUT

| Field | Original value |
|---|---|
| execution_status | CONTROLLED_INCOMPLETE |
| final_result_gate | UNRESOLVED |
| actual_computed_scientific_result | false |
| q042_feasibility_classification | PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED |
| downstream_portability_classification | NOT_AVAILABLE |
| tests_status | COMPLETE |
| JOB_COMPLETENESS | PASS |
| MERGE_COMPATIBILITY | PASS |
| CONVERGENCE | FAIL |
| GLOBALITY | PASS |
| FINAL_RESULT | UNRESOLVED |

All 20 PolyChord records have `CONTROLLED_TECHNICAL_FAILURE`, `segment=0`, `action=fresh`, `worker_returncode=1`, `timed_out=false`, `worker=null`, and an empty `resume_files` list. Recorded worker elapsed times span **0.718863–4.628415 seconds**; these are not whole-job durations or a CPU accounting total.

The two failed Py-BOBYQA starts remain in the unmodified final JSON:

| Cell | Start index | Flag | Recorded objective | Evaluations | Error |
|---|---:|---:|---:|---:|---|
| HiLLiPoP / EDE / FULL | 1 | −3 | 1264.667475 | 207 | Singular matrix in mini-model interpolation |
| HiLLiPoP / ΛCDM / NO_DESI_DR2 | 3 | −3 | 1225.17065 | 882 | Singular matrix in mini-model interpolation |

The other 78 records have flag 0. The frozen eligibility rule excludes the two failed starts, retains their raw records and permits the remaining candidates. No failure was erased and no additional optimizer starts were created.

### TECHNICAL INTERPRETATION

The failure chain is directly traceable:

1. The frozen `polychord_production` specification includes numerical options and two descriptive fields.
2. `production_pc()` deep-copies that entire object, converts the unlimited-dead-point value to numeric infinity, and adds `path` and `seed`.
3. `polychord_worker()` assigns that dictionary to `info['sampler']['polychord']`.
4. Cobaya rejects the two unknown fields during input processing. Both the CamSpec/ΛCDM/FULL and HiLLiPoP/EDE/FULL logs show this error before sampling.

The infinity conversion itself is present and was preserved by the local diagnostic. The required repair is a separation between metadata and executable sampler options, retaining both metadata fields in the scientific record. It is not a change of sampler, threshold or numerical stopping criterion.

The 33 static checks inspect specification values, strings and workflow structure. The runtime preflight builds model/likelihood information and checks finite FULL evaluations and matching external signatures, but does not call the production sampler dictionary builder through Cobaya's sampler input validation. This explains the specific validation coverage gap without implying that every prior gate was worthless.

`CONVERGENCE=FAIL` is the aggregator's label for the incomplete posterior branch. It is **not evidence of a measured PolyChord convergence failure after a sampling attempt**. The 48-segment convergence budget was not exercised. Likewise, GitHub's green job/run status means the controlled failure was recorded and collected successfully.

`GLOBALITY=PASS` is narrowly implemented: all four starts must be present and each cell must retain at least one finite eligible candidate. It does not test equality of minima or establish a mathematical global optimum. Official Py-BOBYQA documentation describes it as a local solver and does not promise a global optimum even with its optional global heuristic [K-Q042-ING-002].

### PHYSICAL INTERPRETATION

No posterior distributions were produced by the 20 required cells. H0/fEDE parameter-location comparisons, their uncertainty denominators, empirical 64²/80²/96² overlap checks, and the complete required LOO classification cannot be evaluated. The result neither falsifies nor confirms ΛCDM, EDE or either Planck likelihood.

For preservation only, the recorded best candidate objectives imply the following **within-arm** differences under the frozen convention Δχ² = 2(objective_LCDM − objective_EDE):

| Combination | CamSpec candidate Δχ² | HiLLiPoP candidate Δχ² |
|---|---:|---:|
| FULL | -5.202886578 | -7.807410915 |
| NO_ACT_PRIMARY | -0.160213990 | 5.070110608 |
| NO_ACT_LENSING | -6.102295794 | -2.545895003 |
| NO_DESI_DR2 | -4.648358940 | -4.743352581 |
| NO_SN | 2.781484517 | -7.122963998 |

These numbers are diagnostic partial results, not a final model-preference or portability verdict. No absolute objective was subtracted across Planck arms. Negative values are preserved without clipping or “correction.” Four local starts and flag 0 do not establish global optima; the numerical/domain explanation for those values is not resolved by this ingestion. The JSON's `start_values` are initial values, **not fitted parameter estimates or posterior means**.

**ANOMALY STATUS:** Documented software/configuration defect; preserved candidate optimization discrepancies. No candidate physical anomaly is established by this campaign. The inherited fitted-geometry discrepancy remains in the journal without reinterpretation.

---

## INTERNAL RESULT PROVENANCE

| Field | Recorded/recovered value |
|---|---|
| Repository | [Morfindien/Bubbleverse](https://github.com/Morfindien/Bubbleverse) |
| Branch / execution commit | main / `6c44a4117449145afd0a3ae6eb238490686a8c6d` |
| Program / run label | Q042-PROD-V1 / Q042-PRODUCTION-PORTABILITY-V1 |
| Workflow | `.github/workflows/q042-production-v1.yml` |
| Root GitHub run | [36133813540](https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540), observed attempt 2 |
| Root created / latest attempt started / updated | 2026-09-25T12:14:39Z / 2026-09-25T21:58:11Z / 2026-09-26T19:19:05Z |
| Collector run | [36256885294](https://github.com/Morfindien/Bubbleverse/actions/runs/36256885294), attempt 1; same execution commit |
| Collector created / updated | 2026-09-26T16:50:16Z / 2026-09-26T19:52:13Z |
| Final artifact | ID 10914048163; q042-production-final-v1; 15,099 bytes; created 2026-09-26T19:52:10Z |
| Uploaded ZIP SHA-256 | `1c68943755e19c4dad7ffe4ad53182eedba1f24ff31eeb956e24aa390d725d79`; exact match to GitHub artifact digest |
| Final JSON SHA-256 | `921aaeb7033557627ecacf5a85ea9257d8ad4efc909ce227f9d182de3733a2c1`; matches artifact index |
| Production specification SHA-256 | `41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c`; matches source lock |
| Production source-lock SHA-256 | `0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56` |
| Production program SHA-256 | `889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642` |
| CamSpec log | [job 108266634302](https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540/job/108266634302) |
| HiLLiPoP log | [job 108266637238](https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540/job/108266637238) |
| Runtime artifact | q042-prod-36133813540-environment; ID 10862038917; 278,412,344 bytes; digest `sha256:162b99026d025d1021fa8a83dbf4290b7bd0c2c53917ea56cbf04f8b169bff4a`; metadata inspected, bytes not downloaded |
| Observed representative runner | GitHub-hosted Ubuntu 24.04.5; runner 2.337.0; image ubuntu-24.04 version 20260920.314.1 |
| Q032 parent | R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002; run 33994305721; commit `4dc873a5e880d40858d831a3b421456728f0c032` |
| Locked runtime versions | Python 3.11; Cobaya 3.5.6; NumPy 1.26.4; Py-BOBYQA 1.5.0; PolyChordLite 1.22.2, commit `3ade6445bb3719a6db6f6e81f178765545ffc833` |
| Seed/config/optimizer records | All 20 frozen sampler seeds/config hashes and all 80 recorded optimizer seeds, starts, evaluation counts and statuses remain in original inputs and generated CSV inventories |
| Exact endpoint parameters and full per-cell updated configs | Not contained in uploaded final ZIP; not fetched here. Initial `start_values` do not substitute for endpoints. |
| Full runtime data hashes, compiler/hardware matrix, CPU accounting | NOT DOCUMENTED as independently verified values in this ingestion |

No scientific code, registry or workflow was modified or dispatched. Seven fetched source files were matched to their Git blob hashes. The local audit performed 62 passing checks of identity, record completeness, best-objective aggregation and the demonstrated configuration leak. This is not a rerun of the production science or a claim that all scientific gates passed.

---

## WEB / PLUGIN / TOOL RESEARCH

**RESEARCH PERFORMED:** YES — targeted technical documentation, project-state retrieval and provenance inspection.  
**CAPABILITIES USED:** GitHub connector; Library search/read for prior handoffs, not for the uploaded attachment; local Python, AST extraction and SHA checks; web search/open for official method documentation.  
**QUESTIONS INVESTIGATED:** Why did all posterior cells fail immediately? What does the aggregator actually check? Does the ZIP belong to the stated production collector? Which completed results and prior journal entries can be retained?  
**NEW EXTERNAL EVIDENCE:** Official sampler option schema and optimizer semantics only; no new observations or cosmological constraints.  
**NEW SOURCES:** K-Q042-ING-001 through K-Q042-ING-003 below.  
**CONTRADICTORY EVIDENCE:** Direct job errors contradict a reading of static PASS as production runtime readiness. Source code contradicts a strong interpretation of GLOBALITY=PASS as proof of global optimization.  
**IMPACT ON INTERPRETATION:** Configuration rejection, not demonstrated sampler convergence failure or physical falsification.  
**IMPACT ON JOURNAL:** Add exact technical cause, complete recorded optimizer counts and bounded repair route; preserve inherited science.

Research stops here because wider cosmological literature cannot provide the missing posterior samples or change the demonstrated startup defect. Current documentation is contextual; the retrieved **v3.5.6** option file and the execution logs control the version-specific diagnosis.

---

## ACTIVE SOURCE REGISTER

New IDs are scoped to this ingestion. Existing historical IDs are neither renumbered nor reused.

| ID | Source / evidence class | Scope |
|---|---|---|
| I-Q042-ING-001 | User-uploaded q042-production-final-v1.zip and its four unchanged JSON members; Bubbleverse internal computational output | Direct result, specification, source lock, index and raw preservation |
| I-Q042-ING-002 | GitHub root/collector metadata and final artifact ID 10914048163 | Exact execution identity, dates, attempt and ZIP digest |
| I-Q042-ING-003 | [q042_production_v1.py at execution commit](https://github.com/Morfindien/Bubbleverse/blob/6c44a4117449145afd0a3ae6eb238490686a8c6d/q042_production_v1.py) | Sampler builder, worker, optimizer aggregation and controlled-final semantics |
| I-Q042-ING-004 | [CamSpec/ΛCDM/FULL job log](https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540/job/108266634302) | Actual unsupported-option error before sampling |
| I-Q042-ING-005 | [HiLLiPoP/EDE/FULL job log](https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540/job/108266637238) | Same observed error in other arm/model |
| I-Q042-ING-006 | [production tests at execution commit](https://github.com/Morfindien/Bubbleverse/blob/6c44a4117449145afd0a3ae6eb238490686a8c6d/q042_production_tests_v1.py) | Static validation scope and missed sampler-dictionary validation |
| I-Q042-ING-007 | [production workflow at execution commit](https://github.com/Morfindien/Bubbleverse/blob/6c44a4117449145afd0a3ae6eb238490686a8c6d/.github/workflows/q042-production-v1.yml) | Jobs, controlled failure collection, continuation and artifact lineage |
| I-Q042-ING-008 | [V11 source lock](https://github.com/Morfindien/Bubbleverse/blob/6c44a4117449145afd0a3ae6eb238490686a8c6d/q042_planck_portability_source_lock_v11.json), V11 program, Q041 diagnostic reference | Technical history, frozen runtime and forbidden science inputs |
| I-Q042-ING-009 | Q041_V19_INGESTION_HANDOFF(1).md, `libfile_6caea79cefe4819182fa56d2475ce2cb`; shorter original `libfile_bb856baf00108191adf5e834b28ec5ee` | Full recovered parent journal and old source map, explicitly historical |
| I-Q042-ING-010 | Indsat markdown(8).md, `libfile_bc5ab16630ec8191829550b716070d44` | Existing Numerical Execution/HPC engine role and continuity requirements; operating prompt, not a scientific journal |
| I-Q042-ING-011 | audit_ingestion.py, ingestion_audit.json, four CSVs in evidence package | Deterministic internal audit, counts and within-arm diagnostic arithmetic |
| K-Q042-ING-001 | [CobayaSampler/cobaya v3.5.6 PolyChord defaults](https://github.com/CobayaSampler/cobaya/blob/v3.5.6/cobaya/samplers/polychord/polychord.yaml), Git blob `3cfca12f4ce06995abf49a974c83754894842b0f`; official technical source, accessed 2026-09-26 | Version-pinned sampler-option schema |
| K-Q042-ING-002 | [Using Py-BOBYQA, v1.5.0](https://numericalalgorithmsgroup.github.io/pybobyqa/build/html/userguide.html); official documentation, accessed 2026-09-26 | Local-optimizer scope, flags and absence of global-optimum guarantees |
| K-Q042-ING-003 | [Cobaya PolyChord documentation](https://cobaya.readthedocs.io/en/latest/sampler_polychord.html); official current documentation, accessed 2026-09-26 | Context for sampler options and outputs; does not supersede the pinned runtime |

The following inherited implementation identities remain **SOURCE-LOCK REFERENCES**, not new external observational evidence or a fresh runtime-data validation:

| Component | Preserved identity |
|---|---|
| n=3 EDE backend | [mwt5345/class_ede](https://github.com/mwt5345/class_ede), commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97` |
| HiLLiPoP | `planck_2020_hillipop.TT`, v4.2 source lineage, commit `a09ddde3e7ce11df99f74685feb1f1764cafb251` |
| ACT DR6 primary | [ACTCollaboration/DR6-ACT-lite](https://github.com/ACTCollaboration/DR6-ACT-lite), v1.0.1, commit `880eacb40d66722eb1c32d7b5621e91662b4d808`; ell_min 600 |
| ACT DR6 lensing | [ACTCollaboration/act_dr6_lenslike](https://github.com/ACTCollaboration/act_dr6_lenslike), v1.2.1, commit `b386ddbb5821c1216c709f051c9289292f174d30` |
| DESI DR2 | `bao.desi_dr2`; [CobayaSampler/bao_data](https://github.com/CobayaSampler/bao_data) v2.6, commit `b7b8a36e9bccb063081f811f323cada21ab5fbdd`; definition commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a` |
| Supernova | `sn.pantheonplus`, frozen prospectively; Q014 reference R-Q014-EDE-EXTERNAL-VIABILITY-009, run 33597153303; runtime-file hashes required |
| PolyChordLite | [PolyChord/PolyChordLite](https://github.com/PolyChord/PolyChordLite), release 1.22.2, commit `3ade6445bb3719a6db6f6e81f178765545ffc833` |

Appendix A retains all recovered historical source IDs and mappings, including K-044 through K-058 where present, K-Q041-DOC-001 and I-Q041-001–013. Incomplete bibliographic identities remain incomplete. This ingestion does not use those unrefreshed references to make new cosmological claims.

---

## CLAIM-TO-SOURCE MAP

| Claim | Evidence |
|---|---|
| C-Q042-ING-001: Exact question, 20-cell matrix and criteria remain frozen | I-Q042-ING-001, Appendix C |
| C-Q042-ING-002: The uploaded ZIP is the stated final GitHub artifact | I-Q042-ING-001, 002, 011 |
| C-Q042-ING-003: All 20 posterior records failed in segment 0; no completed posterior branch | I-Q042-ING-001, 011 |
| C-Q042-ING-004: Unsupported metadata causes the observed startup defect | I-Q042-ING-003, 004, 005, 011; K-Q042-ING-001 |
| C-Q042-ING-005: Prior static/runtime checks did not cover this exact production sampler dictionary | I-Q042-ING-003, 006 |
| C-Q042-ING-006: 80 optimizer records, 78 eligible, 2 preserved failures, 20 retained candidate minima | I-Q042-ING-001, 003, 011 |
| C-Q042-ING-007: GLOBALITY=PASS is not proof of global optimality | I-Q042-ING-003; K-Q042-ING-002 |
| C-Q042-ING-008: Listed Δχ² values are reproducible within-arm candidate arithmetic | I-Q042-ING-001, 011; frozen formula in Appendix C |
| C-Q042-ING-009: No physical portability class follows | C-Q042-ING-001, 003, 006; frozen completeness and classification requirements |
| C-Q042-ING-010: Historical science survives without Q040 resurrection | I-Q042-ING-008, 009; Appendices A–C |
| C-Q042-ING-011: One targeted HPC repair can materially change the answer | C-Q042-ING-003–005 plus exact Q; routing inference, not measured physics |

---

## WHAT CHANGED

The case now has an artifact-linked diagnosis of production startup failure, exact accounting of completed optimizer records, a checked aggregation of their best candidates, and an explicit validation coverage gap. The description “numerically unresolved” is refined by the observed reason: rejection of invalid sampler arguments before inference.

## WHAT DID NOT CHANGE

The question, scientific contract, likelihood identities, priors/bounds, seeds, production tolerances, decision thresholds, Q040 firewall and prohibition on cross-arm absolute-objective evidence remain fixed. No cosmological model or observational benchmark changes. The previous physical geometry discrepancy is neither explained nor erased.

## FALSIFIED / REJECTED / SUPERSEDED MATERIAL

- **REJECTED FOR EXECUTION:** The unmodified V1 production sampler-input path; rerunning it reproduces an invalid dictionary.
- **CONTRADICTED:** Treating the historical 33 static passes as proof that the actual production sampler could initialize.
- **NOT ESTABLISHED:** Calling this a failed PolyChord convergence experiment or exhausted 48-segment campaign.
- **NOT ESTABLISHED:** Global optimum certification from the named GLOBALITY gate, or fitted cosmological parameters from `start_values`.
- **PRESERVED, NOT PROMOTED:** The two flag−3 optimizer records and all negative candidate Δχ² values.
- **STILL FORBIDDEN:** Q040 invalidated science endpoints, V11 pilot science, unconverged V19 cosmological endpoints, retrospective criterion changes, and automatic return to the rejected unchanged MCMC route.
- No physical hypothesis is falsified by this technical failure.

## OPEN UNCERTAINTIES

The corrected production interface has not been executed through full inference. Posterior completion/convergence, actual posterior geometry, required LOO decisions and the ultimate portability answer remain unresolved. Global optimality of the recorded candidates is not demonstrated. Full endpoint configs, runtime data identities and complete Q042 journal continuity remain only partially recovered.

These are distinct uncertainties. The immediate blocker is the proven input-validation defect. Do not turn every listed limitation into an independent new computational campaign.

---

## Q-COMPLETION GATE

**STATUS:** NOT YET SATISFIED.

**WHY:** V1 as delivered cannot execute the intended posterior inference, but that does not answer whether the frozen strategy can perform the test after a technical interface repair. No posterior was generated and the finite scientific stopping policy was not exercised. A known, localized defect can materially change the answer. Closing now as physically resolved would confuse program failure with evidence about the science.

## MATERIAL-REVERSAL TEST

**PASS — further targeted work is material.** Removing only the two metadata fields from the executable sampler dictionary, while retaining the metadata and every numerical setting, can change the outcome from immediate parser rejection to an actual inference attempt. Additional unchanged BOBYQA runs, broad literature review, altered thresholds and generic robustness scans fail the current necessity test.

## ROUTING REASON

The existing Numerical Execution / HPC Engine owns the configuration adapter, runtime validation, artifact reuse and finite execution mechanics. These are the current bottleneck. An anomaly, theory or report-writing engine would not supply the missing validated inference.

---

## NEXT TASK

**Objective:** Deliver a versioned, narrowly scoped production repair and recovery path for the existing Q-042 contract.

1. Preserve V1 and this diagnosis as historical evidence. Give any repair its own implementation identity; do not silently replace the failed campaign or claim the patch has already run.
2. Translate the scientific `polychord_production` object into only supported Cobaya sampler options. Keep `seed_policy` and `max_ndead_runtime_encoding` in the scientific/provenance objects, but outside the executable `sampler.polychord` dictionary. Preserve numeric `float('inf')`, all frozen sampler values and all 20 seeds.
3. Add one meaningful regression check that fails on the V1 dictionary and validates the actual production sampler options using the pinned Cobaya 3.5.6 interface. Validate the exact production path before a large dispatch. Do not count another string-presence gate as proof of parser acceptance.
4. Recover the existing campaign runtime and the individual BOBYQA artifacts from root run 36133813540. Verify input/runtime identity and retain all 80 recorded starts, including the two failures, in the continuation lineage. Reuse compatible completed work. Do not rerun all optimization jobs merely because the program version changes, and do not relabel V1 outputs as newly computed.
5. Proceed only with the missing posterior work after the corrected path passes its bounded execution check. These cells have no sampler checkpoints to resume; they must begin from their frozen fresh state. Future segments must use the already-established separate-interpreter/stored-info resume method.
6. Keep final aggregation fail-closed: require the frozen posterior, within-arm fit, geometry, numerical-binning and LOO conditions. Record which checks actually ran. Preserve `UNRESOLVED` if required evidence remains unavailable.
7. Carry forward this handoff, Appendices A–C, raw outputs, source map, failure history and explicit journal gaps. Recover any additional existing journal context where directly available; do not manufacture it.

**Execution boundary:** This ingestion supplies the concrete diagnosis and handoff. It does not implement or dispatch the next engine's campaign. The existing instruction prohibiting assistant GitHub mutation/dispatch is retained. No permission is requested merely to deliver the handoff.

## FIXED / FROZEN ELEMENTS

- Exact Q and case-ID status; original production spec and source lock, hashes above.
- CamSpec/HiLLiPoP; ΛCDM/n=3 EDE; FULL, NO_ACT_PRIMARY, NO_ACT_LENSING, NO_DESI_DR2 and NO_SN.
- Same frozen ACT DR6 primary/lensing, DESI DR2 and Pantheon+ in corresponding arms; no hybrid Planck likelihood.
- PolyChord: `nlive=25d`, `num_repeats=5d`, `nprior=10nlive`, `nfail=nlive`, precision 0.001, unlimited dead points, clustering and the other exact settings in Appendix C; exact seed map.
- Py-BOBYQA: four external starts, `best_of=1`, `ignore_prior=true`, `max_evals=120d`, `rhoend=0.05`, frozen starts and acceptance rule.
- 240-minute soft sampler segments, 330-minute job timeout and 48-segment policy; no automatic budget extension or tolerance relaxation.
- D_x, weak-identification protection, histogram overlap threshold 0.50 and grids 64²/80²/96²; within-arm model-preference rules; original final class logic.
- Permanent launcher, scientific firewalls and historical exclusions.

## VARIABLE ELEMENTS

Only the technical adapter between specification and runtime arguments, directly relevant regression coverage, and explicit import/lineage mechanics for reusing compatible existing artifacts. A new program/source-lock record may reference the unchanged original scientific specification. Any scientifically material change requires its own prospective documented configuration, not a retrospective rewrite of V1.

## SUCCESS CONDITION

The corrected executable sampler dictionary is accepted by pinned Cobaya and the required production matrix reaches a documented terminal outcome under the unchanged finite policy. A physical portability class may be emitted only when all its frozen evidence requirements are satisfied. Completed work is reused with verified lineage; the scientific journal and sources accompany the result.

## FAILURE / FALSIFICATION CONDITION

Unsupported options remain; runtime/source identity cannot be established; necessary posterior outputs fail or exhaust their frozen budget; a required geometry/fit/LOO gate fails; or the frozen classification rules cannot resolve. Preserve the exact failure and its scope. Technical failure is not physical model falsification. No selective rerun or altered threshold is permitted merely to obtain a preferred physical answer.

## STOP CONDITION

Stop this ingestion now: the routing uncertainty has been resolved. Do not launch another validation loop here.

The next engine stops once the narrowly defined technical defect is tested and the unchanged finite production policy produces its documented outcome. When the exact Q has a defensible answer—either a valid completed test or an honestly bounded unresolved result with no remaining necessary, materially informative action—close it and route the complete case directly to **BUBBLEVERSE — MOTOR 14: AUTONOMOUS UNIVERSE REVISION**. Do not extend budgets or change samplers/criteria to rescue a result. If a new material execution blocker appears, document it explicitly before any further routing; “run more” is not a task.

---

## EVIDENCE PACKAGE AND PRESERVATION NOTES

The companion `Q042_PROD_V1_INGESTION_EVIDENCE.zip` contains this handoff, the original unmodified uploaded ZIP and its four JSON members, the full recovered parent handoffs, Q042 technical-history references, pinned source snapshots, two raw job logs, run/artifact metadata, the deterministic ingestion audit script and its outputs. Original source code is archived for traceability, not modified or installed.

The historical handoff texts were reconstructed from complete Library reads; their byte counts, with the terminal newline retained, match the reported source sizes. Their original text SHA was not supplied by Library, so this is not an independent cryptographic identity claim. Retrieved GitHub source snapshots were separately matched to their Git blob hashes. References to older evidence packages inside the historical appendix remain references; their full old package contents were not silently invented or reconstructed.

**No new physical result was manufactured. No completed optimization result was discarded. Q-042 remains open for one concrete, evidence-based technical recovery task.**

---

# APPENDIX A — COMPLETE RECOVERED PARENT HANDOFF / HISTORICAL JOURNAL

The following is preserved historical text. Its old active-Q labels, pending routes and instructions do not override the current Q-042 decision above.

**BUBBLEVERSE — HANDOFF**

**STATUS:** CONTINUES  
**CASE ID:** CASE-041  
**CURRENT Q:** Q041; råfilerne bruger identifikatoren `Q-041`.  
**CASE:** Downstream Scientific-Consequence Portability of Planck-Likelihood Geometry  
**QUESTION:** Har den validerede CamSpec–HiLLiPoP fitted-geometry-forskel en materiel downstream kosmologisk konsekvens under identiske eksterne data?  
**SELECTED NEXT ENGINE:** Numerical Execution / HPC Engine  
**DATE AND TIME:** 2026-09-23T20:51:13+00:00

**INSTRUCTION UPDATE:** 2026-09-23T20:59:28+00:00 — BV-EXEC-README-001 v1.0 er indarbejdet i denne overlevering til den eksisterende Numerical Execution / HPC Engine. Tillægget udvider kravene til repository-leverancer; den oprindelige ingestion-dato, Q041-resultaterne og den historiske journal bevares. Motorens fulde grundprompt er ikke vedlagt. Det fulde genbrugelige tillæg findes også som `BUBBLEVERSE_EXECUTION_ENGINE_README_ADDENDUM.md` og i bilag D.

**Afgørelse**

V19 er afsluttet med et dokumenteret, kontrolleret stop uden videnskabeligt resultat. Q041 er fortsat åben. Ingen af de tre tilladte videnskabelige portabilitetsklasser kan vælges på dette grundlag.

Der er udført reelle MCMC-beregninger. Slutfilen klassificerer 30 af 32 planlagte kæder som `MAX_SAMPLES_WITHOUT_CONVERGENCE`. De to øvrige er også ukonvergerede: deres sidste joblogs viser `PARTIAL` efter otte beregningssegmenter. Der er således **0 af 32 kæder med dokumenteret COMPLETE-status** i den afsluttede V19-matrix. Dette udsagn sammenholder slutfilens komplette stopliste med de sidste logs for netop de to kæder, som ikke står på listen; det bygger ikke på en antagelse om, at fravær på stoplisten betyder succes.

En anden, selvstændig hindring er dokumenteret: den udførte V19-præregistrering er ikke den samme videnskabelige test som den fremsendte specifikation fra 9. september. V19 mangler ΛCDM-modkontrollen og supernova-likelihooden og bruger andre beslutningsregler. Selv en konvergeret V19-kørsel ville derfor ikke i sig selv dokumentere hele den oprindeligt beskrevne test.

**SAMLET JOURNAL — aktiv videnskabelig tilstand**

Dette er en tilføjelse til den eksisterende journal. De genfundne Q031–Q040-journalposter er bevaret som historisk tekst i bilag C og i evidenspakken. Deres karakter af retrospektive rekonstruktioner, manglende oplysninger og gamle fortolkninger bevares. Aktiv fortolkning følger den senere evidens og brugerens aktuelle Q041-spørgsmål.

En komplet selvstændig Q041-journal med alle mellemoverleveringer V1–V18 blev ikke leveret eller identificeret. Registryens dokumenterede versionshistorik medfølger som kilde, men ukendte beslutninger rekonstrueres ikke som fakta. Det fulde historiske kilderegister med bibliografiske detaljer bag alle gamle K-numre er heller ikke dokumenteret i det læste journaluddrag. Disse mangler er markeret frem for udfyldt med antagelser.

| Journalpost | Aktiv viden efter ingestion | Ændring fra V19 |
|---|---|---|
| Q031 | Den uafhængige HiLLiPoP-implementering og dens råresultater bevares. Den gamle binære basinfortolkning læses sammen med Q035, ikke som en invariant fysisk opdeling. | LEAVES UNCHANGED |
| Q032 | Valideret exact-common-TT-materiale er en dokumenteret teknisk forælder. Senere add-back-resultater fandt ingen ren SUPPORT/TE/EE-lokalisering under de testede betingelser. | LEAVES UNCHANGED |
| Q033 | Historisk scalar/reference-semantik var allerede ens; denne forklaring på den tidligere klassifikationsforskel blev afvist. | LEAVES UNCHANGED |
| Q034 | Frysning af primordialblokken alene genskabte ikke den historiske basinfortolkning under den senere klassifikator. | LEAVES UNCHANGED |
| Q035 | Forskellen mellem de gamle stable/non-stable labels forsvinder ved klassifikatorharmonisering. Råendpoints bevares. | LEAVES UNCHANGED |
| Q036 | Kontinuert, reproducerbar CamSpec–HiLLiPoP-geometriforskel under fælles koordinater/skalaer er etableret i den historiske test. | LEAVES UNCHANGED |
| Q037 | Geometriforskellen overlever exact-common-TT-support. Det fastslår ikke en fysisk Planck-systematik. | LEAVES UNCHANGED |
| Q038 | Den deskriptive forskel er multivariat. Den minimale robuste delmængde er omega_b, omega_cdm, f_EDE og theta_i,scf. | LEAVES UNCHANGED |
| Q039 | De testede calibration-, precision-, kombinerede calibration/precision- og native foreground-profile-interventioner var utilstrækkelige. Dybere årsag uafklaret. | LEAVES UNCHANGED |
| Q040 | Single-Gaussian-kompression bestod ikke valideringen. Den endelige defensive RQMC-kampagne bestod heller ikke sine numeriske kriterier. Ingen validerede science-endpoints fra disse spor. | LEAVES UNCHANGED |
| Q041 historisk design | Den fremsendte plan kræver matched native Planck-arme, ΛCDM/EDE, ACT primary, ACT lensing, DESI DR2 og én fælles SN-likelihood, FULL + fire LOO-kombinationer. | PRESERVED; ikke automatisk erstattet af kode |
| Q041 execution | V19 er registreret og faktisk kørt på et identificeret commit; den gamle påstand om, at intet konkret executable target findes, er historisk. | SUPERSEDES den gamle launcher/execution-pending-status |
| Q041 numerik | 30 kæder har sample-cap-stop; to har segmentbudget-stop. Ingen færdig valideret posterior-matrix. | ADDS |
| Q041 kontrakt | V19 implementerer en smallere, anderledes klassificeret EDE-only-test. En godkendt overgang fra den fremsendte 20-cell test er ikke dokumenteret i det inspicerede materiale. | ADDS en material provenance/scope-afvigelse |
| Q041 fysik | Materiel downstream-forskel, kollaps og mixed-dataset-conditional er fortsat uafgjort. | LEAVES UNCHANGED |
| Bubbleverse-model | Ingen ny fysisk modelændring, ingen EDE-detektion/falsifikation og ingen ændring af H0-benchmarks på grundlag af V19. | NONE |

Den genfundne bog slutter med et ældre forslag om, at Q041 skulle lokalisere Q040's RQMC-instabilitet. Det forslag bevares som **HISTORICAL / SUPERSEDED FOR CURRENT ROUTING**. Det erstatter ikke det downstream-portabilitetsspørgsmål, brugeren udtrykkeligt har angivet her. Q040 genåbnes ikke gennem denne ingestion.

**NEW RESULT INGESTED**

**RESULT ID:** `R-Q041-EDE-DOWNSTREAM-PORTABILITY-019`  
**ORIGIN:** Bubbleverse Numerical Execution / HPC, GitHub Actions, samt brugerens uændrede slut-ZIP.  
**RESULT CLASS:** `PARTIAL_RESULT`, `CONVERGENCE_RESULT`, `VALIDATION_RESULT`; programmets egen type er `CONTROLLED_NO_SCIENTIFIC_RESULT`.  
**RESULT STATUS:** Kontrolleret numerisk noncompletion er dokumenteret. Råfilsidentitet og slutvalidatorens tilstandskontrakt er verificeret. Kosmologiske posteriorer er ikke teknisk valideret til inferens.  
**ANOMALY STATUS:** Ingen ny fysisk anomali etableret. Manglende konvergens er en bevaret numerisk observation med endnu uafklaret grundårsag. Q036–Q039's arvede metodiske geometriforskel forbliver uafklaret.

**DIRECT OUTPUT — lag 1**

| Felt i q041_final_v19.json | Uændret værdi |
|---|---|
| stage | FINAL |
| status | PASS |
| final_outcome_valid | true |
| actual_computed_result | false |
| scientific_classification | NO_SCIENTIFIC_RESULT |
| outcome_type | CONTROLLED_NO_SCIENTIFIC_RESULT |
| no_science_reason | MAX_SAMPLES_WITHOUT_CONVERGENCE |
| technical_failure | false |
| details.segment | 8 |
| affected_chains | 30: 14 CamSpec og 16 HiLLiPoP |
| CHAIN_COMPLETENESS | BLOCKED |
| ALL_RHAT_LE_1P05 | BLOCKED |
| BOTH_ARMS_ALL_COMBINATIONS | BLOCKED |
| Q040_FIREWALL | PASS |
| SEGMENTED_RESUME_COMPLETENESS | CONTROLLED_STOP |

`q041_final_tests_v19.json` har også `status=PASS` og `classification=NO_SCIENTIFIC_RESULT`. Den originale slutvalidator er kørt lokalt mod den indsendte JSON. Det resulterende testobjekt er identisk med det indsendte testobjekt. Det er en kontrol af den definerede sluttilstand, ikke en reproduktion af MCMC eller bevis for at alle oprindelige T001–T019 er bestået.

De to supplerende joblogs indeholder:

| Arm/kombination/kæde | Sidste dokumenterede status | Compute-segmenter brugt | Sidste Cobaya R−1 |
|---|---|---:|---:|
| CamSpec / P_A6 / c1 | PARTIAL ved segment 8 | 8 | 7.914737960669388 |
| CamSpec / P_A6_L6_D2 / c1 | PARTIAL ved segment 8 | 8 | 3.2084382274105185 |

I begge logs er den sidste viste konvergenstest foretaget ved 19.440 accepterede samples. Det er ikke en opgørelse af den endelige kædefils længde. Loggen skriver henholdsvis testen kl. 13:46:11 og 13:18:38 UTC og segmentstoppet kl. 14:11:08 og 14:13:11 UTC den 23. september.

V19 kræver `Rminus1_stop=0.02` og `Rminus1_cl_stop=0.2`. Disse Cobaya-stopdiagnostikker skal ikke forveksles med programmets særskilte slutkrav `hard_science_rhat_gate=1.05`. Der er ikke observeret et målt samlet R-hat-resultat i slutfilen; den gate er BLOCKED.

**TECHNICAL INTERPRETATION — lag 2**

Den fastlagte samplergrænse er `max_samples=20000` pr. kæde, `burn_in=100` og `learn_proposal=True`. Hver kæde kan bruge højst otte beregningssegmenter, hver med et soft stop på 300 minutter; jobtimeout er 330 minutter.

V19-koden markerer normal sampler-return uden `sampler.converged` som `MAX_SAMPLES_WITHOUT_CONVERGENCE`. Senere segmenter genbruger terminale `NO_SCIENTIFIC_RESULT`-tilstande uden ny sampling. Denne adfærd er både læst i koden og set i HiLLiPoP / P_A6_L6_D2 / c0's segment-8-log. Et hurtigt, grønt senere segment er derfor ikke dokumentation for konvergens.

Finalizeren undersøger max-sample-stop før de resterende `PARTIAL_SOFT_STOP`-tilstande. Derfor nævner den indsendte slutfil kun de 30 kæder med sample-cap-stop, selv om de to andre også er uafsluttede. Den originale JSON ændres ikke; journalen tilføjer den fulde tilstandsbeskrivelse fra joblogs.

I de to CamSpec-logs ses meget store sidste R−1-værdier samt beskeder om, at proposal-opdatering afventer en bedre konvergenstest. Det begrunder en målrettet undersøgelse af sampling og adaptation. Det identificerer ikke alene grundårsagen som eksempelvis multimodalitet, fejl i startpunkt, proposal-skala, priorgrænse eller resume-logik.

De 30 cap-stop er programrapporterede. Deres individuelle kædefiler og checks er ikke genberegnet her. Slut-ZIP'en indeholder kun to JSON-filer, ingen sample arrays, traceplots, best fits eller konvergenshistorik.

**PHYSICAL INTERPRETATION — lag 3**

V19 dokumenterer hverken, at den etablerede geometriforskel bliver kosmologisk materiel, at den kollapser, eller at den afhænger af datakombination. Manglende konvergens falsificerer hverken EDE, ΛCDM, CamSpec eller HiLLiPoP. Det understøtter heller ikke ny fysik.

Der er ikke beregnet en tilladt fysisk evidensforskel mellem absolutte CamSpec- og HiLLiPoP-χ². Ingen sådan beregning indføres i denne overlevering. `NO_SCIENTIFIC_RESULT` er en numerisk sluttilstand, ikke en fjerde fysisk portabilitetsklasse.

**Den faktisk udførte V19-matrix**

P betegner den Q032-afledte Planck exact-common-TT-konstruktion. A6 er ACT DR6 primary, L6 er ACT DR6 lensing, D2 er DESI DR2 BAO. Alle nedenstående celler bruger MOD-EDE-N3. Variabelnavnet `baseline_combinations` i koden betyder datakombinationer; det er ikke en ΛCDM-reference.

| Datakombination | CamSpec c0 | CamSpec c1 | HiLLiPoP c0 | HiLLiPoP c1 |
|---|---|---|---|---|
| P | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |
| P_A6 | sample-cap-stop | segmentbudget / PARTIAL | sample-cap-stop | sample-cap-stop |
| P_L6 | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |
| P_D2 | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |
| P_A6_L6_D2 | sample-cap-stop | segmentbudget / PARTIAL | sample-cap-stop | sample-cap-stop |
| P_L6_D2 | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |
| P_A6_D2 | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |
| P_A6_L6 | sample-cap-stop | sample-cap-stop | sample-cap-stop | sample-cap-stop |

Det er 2 arme × 8 datakombinationer × 1 model = 16 model/data-celler og 32 kæder. Det er ikke den oprindelige 2 × 5 × 2 = 20-cell matrix med to modeller.

**Kontraktkontrol: fremsendt design versus V19**

| Emne | Fremsendt Q041-design | V19 på execution-commit | Vurdering |
|---|---|---|---|
| Modeller | ΛCDM og samme frozen n=3 EDE i begge arme | MOD-EDE-N3; ingen særskilt ΛCDM-celle | Manglende reference/modelpræference-test |
| Eksterne data | ACT primary + ACT lensing + DESI DR2 + fælles SN-likelihood | A6 + L6 + D2; SN findes ikke i manifestets datamatrix eller add_external_data | Manglende krævet likelihood |
| FULL | Alle fire eksterne blokke | P_A6_L6_D2 | Forskellig FULL-definition |
| LOO | Fire fratrækninger fra samme FULL | Tre LOO-kombinationer uden SN | Opfylder ikke den fremsendte matrix |
| Planck-information | Native CamSpec PR4/NPIPE og native HiLLiPoP PR4/NPIPE | Q032 exact-common-TT; yderligere ell ≤ 599 med A6 | Dokumenteret smallere support; ikke dokumentation for en fuld native TTTEEE-test |
| Overlap | Valideret, frozen Planck/ACT-overlapimplementering | Planck TT ≤599, ACT TT/TE/EE ≥600; cross-covariance=0 er en eksplicit antagelse | Konstruktionsvalg dokumenteret; oprindeligt valideringskrav ikke automatisk bestået |
| Parameterregel | H0 eller f_EDE D≥1, eller mindst to primære kosmologiske koordinater; svagt identificerede EDE-timingkoordinater må ikke alene drive resultatet | Maksimum af seks standardized mean shifts ≥1 kan bidrage alene | Forskellig beslutningsregel; den oprindelige identifikationsbeskyttelse er ikke etableret her |
| Konturer | Numerisk posterior/profile-overlap i (H0,f_EDE), material ved overlap <0.50 | Seksdimensional Gaussian Bhattacharyya-summary af posterior moments, material ved ≤0.50 | Anden størrelse og approximation |
| Materialitet | Materiel within-arm modelpræferenceforskel ELLER både parameterlocation OG contour geometry | Mean-shift ELLER Gaussian-summary, kombineret med V19-LOO-regel | Ikke samme logik |
| Modelpræference | Δχ²_LCDM−EDE inden for hver arm; negligible/modest/substantive | Ingen sådan ΛCDM/EDE-tabel i comparator | Ikke implementeret i denne matrix |
| Robust materialitet | Overlever samtlige krævede valide LOO-tests | Mindst 2 af 3 LOO max shifts ≥0.75 | Forskelligt krav |
| Equivalent/collapse | Den fremsendte trevejsregel | Max FULL shift ≤0.50, Gaussian coefficient ≥0.80 og alle tre LOO shifts ≤0.75 | Ikke samme klasse-definition |
| Mixed | Mindst én valid material og én valid ikke-material kombination | `CONSTRAINED_MIXED` som restkategori | Ikke logisk ækvivalente klasser |
| Validering | T001–T019 | Fem science-gates i finalobjektet samt V19-specifikke statiske tests | Navnet PASS erstatter ikke de oprindelige krav |

V19's Gaussian Bhattacharyya-summary er ikke i sig selv en genoplivning af Q040's fejlslagne latent-likelihood-kompression. Det er et andet summarisk mål. Problemet her er, at det ikke er det aftalte numeriske overlapmål, og at der ikke er konvergerede posteriorer at anvende det på.

V19 har sin egen præregistrering før dette slutresultat. Afvigelsen beviser derfor ikke i sig selv retroaktiv målpostflytning. Den viser, at de to tests ikke må omtales som identiske, og at en godkendt ændrings-/scopehistorik mangler i det inspicerede grundlag. Den senest fremsendte brugerdefinition fastholdes som opgavekrav.

**INTERNAL RESULT PROVENANCE**

| Felt | Dokumenteret værdi |
|---|---|
| Repository | Morfindien/Bubbleverse |
| Repository URL | https://github.com/Morfindien/Bubbleverse |
| Program ID | Q041-PLANCKPORT-V19 |
| Internt run ID | Q041-DOWNSTREAM-SCIENTIFIC-CONSEQUENCE-PORTABILITY-V19 |
| GitHub Actions run ID | 34979609004 |
| GitHub run attempt | 4 ved inspektionen; ikke lig med fire fulde videnskabelige gentagelser |
| Branch | main |
| Execution commit | a962ba70077422f8b69642dea4e8272e1d00e5ff |
| Workflow | .github/workflows/q041-planck-portability-v19.yml |
| Workflow oprettet/startet | 2026-09-15T14:08:17Z |
| Seneste attempts start | 2026-09-23T07:27:48Z |
| Run opdateret efter afslutning | 2026-09-23T14:13:43Z |
| GitHub status/conclusion | completed / success |
| Final artifact | q041-final-v19; ID 10754769330; 1.152 bytes |
| Final artifact oprettet | 2026-09-23T14:13:40Z |
| ZIP SHA-256 | 2284518ecbaaf1ff0d0093977827d5162ec29549ba2b81880f266c250311ca2b |
| ZIP-tilknytning | Lokalt beregnet SHA-256 matcher GitHubs registrerede artifact digest præcist |
| q041_final_v19.json SHA-256 | 0062874ed3529004f46cfb542a708d5b8e8dde55d1b4fd1c2ac7c394e6c8be79 |
| q041_final_tests_v19.json SHA-256 | 95fe1e63c78033de8559f609f0d8a1f4d48ee1b4123f3bb8f845b3ac6e5797ab |
| V19 preregistration SHA-256 | 663f971dc59e84aeeaf2df0a23e8a5d1347cd1e774887d795458c97d853e26b4 |
| Videnskabelig kode | q041_planck_portability_v19.py; arver funktioner fra q041_planck_portability_v13.py |
| Validator | q041_planck_portability_tests_v19.py |
| Q032-forælder | run 33994305721; execution commit 4dc873a5e880d40858d831a3b421456728f0c032; R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002 |
| EDE-backend lock | class_ede commit 5a131c91d657dd9a7c6364cc45b038710f8d0d97; n_scf=3 |
| HiLLiPoP lock | a09ddde3e7ce11df99f74685feb1f1764cafb251 |
| Cobaya | 3.5.6 i source lock og de inspicerede joblogs |
| Øvrige versioner i de tre logs | numpy 1.26.4, scipy 1.15.3, getdist 1.6.1, PyYAML 6.0.2, Py-BOBYQA 1.5.0; fulde lister i logs |
| Seeds, kodeformel | 410000 + 1000×arm_index + 10×combo_index + chain_index; ordener bevaret i kode |
| Eksakte priors/nuisance-/runtime-configs for hver kæde | Ikke udlæst fra chain.updated.yaml i denne ingestion; NOT DOCUMENTED her som fuld numerisk tabel |
| Hardware, compiler og alle runtime-dataset-hashes | Ikke fuldt revideret; NOT DOCUMENTED her |
| Beregnet samlet CPU-forbrug | NOT DOCUMENTED; kalenderforløb og opgivne segmentlofter erstatter ikke en opgørelse |

[Den konkrete GitHub-kørsel](https://github.com/Morfindien/Bubbleverse/actions/runs/34979609004).

Otte læste repository-filer er bevaret bytepræcist og deres Git-blob-SHA kontrolleret. Registryens blob på execution-commit matcher den inspicerede registry. Filer og individuelle SHA-256 findes i `source_snapshot_manifest.json`. De 32 segment-8-artefakter er identificeret med ID, navn, størrelse og digest i `provenance.json`; en listing er ikke en påstand om, at deres indhold er valideret.

Tre chain-artifact-referencer kunne hentes via GitHub-forbindelsen, men overførsel af selve ZIP-bytes gav HTTP 403 / error 1010. Ingen adgangsbegrænsning blev omgået. De dokumenterede joblogs blev i stedet læst gennem GitHub-forbindelsen. Dette begrænser råkæde-diagnostikken, ikke identifikationen af den indsendte slutfil.

Brugerens instruks er fastholdt: **ingen filer skrives til GitHub, og ingen nye workflows startes af denne ingestion**. Overleveringen og evidenspakken leveres som filer.

**TARGETED WEB RESEARCH**

**RESEARCH PERFORMED:** YES — afgrænset metode-/proveniensopslag.  
**QUESTIONS INVESTIGATED:** Hvad betyder Cobayas samplegrænse og konvergensstop, hvor findes diagnostikken, og matcher V19 faktisk den fremsendte test?  
**NEW EXTERNAL EVIDENCE:** Ingen nye kosmologiske målinger eller observationsmæssige constraints.  
**NEW SOURCES:** `K-Q041-DOC-001`, officiel Cobaya MCMC-dokumentation. Repository-kode, Actions-metadata og logs registreres særskilt som Bubbleverse-genereret evidens, selv om de er hentet online.

Cobayas officielle dokumentation beskriver `max_samples` som et loft over accepterede steps. `.progress` indeholder acceptancerate og R−1-historik; samplerens stopbetingelser er særskilte. R−1 alene er ikke et tilstrækkeligt bevis for konvergens i vanskelige fordelinger. Det gør eksisterende progress-/chain-filer til det relevante næste diagnostiske input. Den læste dokumentationsside var version 3.6.2; V19's låste 3.5.6-version er ikke ændret eller erstattet. Specifikke V19-indstillinger er dokumenteret af V19-koden og logs.

Kilde: [Cobaya — mcmc sampler](https://cobaya.readthedocs.io/en/latest/sampler_mcmc.html), læst 2026-09-23.

**CONTRADICTORY EVIDENCE:** V19-manifestet modsiger, at den oprindelige fulde 20-cell ΛCDM/EDE/SN-test er udført. De to supplerende logs afviser en mulig læsning af slutfilen som “30 stoppet, 2 færdige”.  
**IMPACT ON RESULT INTERPRETATION:** PASS må læses som korrekt håndteret noncompletion; ikke som videnskabelig succes.  
**IMPACT ON JOURNAL:** Execution-proveniens og scopeafvigelse tilføjes. Den fysiske konklusion ændres ikke. Mere litteratursøgning er ikke nødvendig for denne routingbeslutning.

**ACTIVE SOURCE REGISTER OG CLAIM-TO-SOURCE MAPPING**

Nye kilde-ID'er er afgrænset til Q041-ingestion, så ældre K-numre ikke omnummereres eller genbruges med en anden betydning.

| ID | Kilde / evidenstype | Understøttede claims |
|---|---|---|
| I-Q041-001 | Brugerens q041-final-v19.zip; to uændrede JSON-filer; SHA-256 ovenfor | Direkte slutstatus, 30 affected chains, blokerede gates, rapporteret firewall |
| I-Q041-002 | GitHub run 34979609004 og final artifact 10754769330; original API-metadata i provenance.json | Execution-commit, kørselsidentitet, tider, attempt, kryptografisk kobling til upload |
| I-Q041-003 | q041_planck_portability_v19.py på execution-commit; Git-blob 2190b0a63abfa563f57da20515b5058a4b7b209f | Tilstandsautomat, terminal carry, prioritering af stopårsager, aggregator |
| I-Q041-004 | q041_planck_portability_v13.py på samme commit; Git-blob 34367ef4bb73ed00ebdf4df06460543318d41e58 | Otte EDE-kombinationer, samplerindstillinger, externe likelihoods, support og summaryfunktioner |
| I-Q041-005 | V19 preregistration; Git-blob 36bf90f3112a305db0adbf68b8a32339f16acf5c | V19-spørgsmål, datamatrix, overlapvalg, beslutningsregler og numeriske locks |
| I-Q041-006 | V19 source lock; Git-blob caabb6cbc573f00bb435e00af8ebf47f64481673 | Forældre, eksterne repositories/tags/commits, Q040-forbud |
| I-Q041-007 | V19 tests; Git-blob f88240c5c1f3580d19d7cf213c3b12e354b00850; lokal final-test-replay | Den konkrete betydning af PASS i FINAL_TESTS |
| I-Q041-008 | V19 workflow og registry på execution-commit | 32 jobs pr. segment, otte stadier, faktisk registreret executable target |
| I-Q041-009 | Job 107116595734, CamSpec P_A6 c1, segment 8 | PARTIAL, otte segmenter, R−1=7.914737960669388 |
| I-Q041-010 | Job 107116595751, CamSpec P_A6_L6_D2 c1, segment 8 | PARTIAL, otte segmenter, R−1=3.2084382274105185 |
| I-Q041-011 | Job 107116597145, HiLLiPoP P_A6_L6_D2 c0, segment 8 | Terminal NO_SCIENTIFIC_RESULT videreført uden sampling |
| I-Q041-012 | Brugerens fremsendte Q041-design/handoff dateret 2026-09-09 i denne samtale | CASE-041, dansk exact question, 20-cell krav, original materialitet, T001–T019 |
| I-Q041-013 | bubblevers 0.40mmmtt(5).docx, Q031–Q040-journal; bibliotek-ID libfile_7f564bc99bd88191b790c9addf4804ca | Arvet historik, parent-resultater, gamle kilde-ID'er, afviste/supersedede fortolkninger |
| K-Q041-DOC-001 | Officiel Cobaya mcmc-dokumentation, læst version 3.6.2 | Metodisk forklaring på sampleloft, konvergensdiagnostik og .progress; ingen ny fysik |

Permanente kodelinks findes i `source_snapshot_manifest.json`. Joblinks er `https://github.com/Morfindien/Bubbleverse/actions/runs/34979609004/job/<job-id>` med de dokumenterede ID'er ovenfor.

De eksterne implementation/data-locks bæres videre som tekniske primærkilder, uden at en source lock forveksles med genvaliderede runtime-data:

| Komponent | Repository/version/commit | Claim |
|---|---|---|
| n=3 EDE backend | mwt5345/class_ede; 5a131c91d657dd9a7c6364cc45b038710f8d0d97 | Fælles låst modelbackend |
| HiLLiPoP | commit a09ddde3e7ce11df99f74685feb1f1764cafb251 | Låst native implementationsafstamning |
| ACT primary | ACTCollaboration/DR6-ACT-lite, v1.0.1, 880eacb40d66722eb1c32d7b5621e91662b4d808 | A6-definition og TT/TE/EE ell 600–8500 |
| ACT lensing | ACTCollaboration/act_dr6_lenslike, v1.2.1, b386ddbb5821c1216c709f051c9289292f174d30 | act_baseline, lens_only=false, lmax=4000 |
| DESI DR2 BAO | CobayaSampler/bao_data v2.6, b7b8a36e9bccb063081f811f323cada21ab5fbdd | D2-dataprodukt; mean blob 8aff444fdb42c0946342aa0011ab287eda097c4c; covariance blob fd8e5697ab61379b07b52efb781ea6713417a4d9 |
| DESI Cobaya-definition | b76b6fed2a6c8c5594c6f92d5058bef10079746a | bao.desi_dr2 backport til frozen Cobaya 3.5.6 |

Arvede kilde-ID'er bevares med den identifikation, der faktisk står i journalen:

| Arvet ID | Overleveret identifikation / claimrelation |
|---|---|
| K-044 | CamSpec PR4; metodekontekst for Q032/Q038/Q040 |
| K-045, K-052 | Sammenligningskilder nævnt i Q038; fuld bibliografisk identitet NOT DOCUMENTED i læst uddrag |
| K-046 | Cobaya 3.5.6 teknisk dokumentation/implementation; historisk kørselssemantik |
| K-049 | HiLLiPoP PR4; metodekontekst for Q038/Q040 |
| K-053, K-054 | Officielle implementationer nævnt i Q040; præcis individuel bibliografisk mapping NOT DOCUMENTED i uddrag |
| K-055 | Boundary statistics; historisk Q040-metodekontekst |
| K-056 | Mixed Laplace; historisk Q040-metodekontekst |
| K-057 | Defensive importance sampling; historisk Q040-metodekontekst |
| K-058 | RQMC; historisk Q040-metodekontekst |

Journalens yderligere navngivne eksterne referencer bevares som arvede referencer: Rosenberg et al. 2022, arXiv:2205.10869; Efstathiou & Gratton 2021, arXiv:1910.00483; Tristram et al. 2024, DOI 10.1051/0004-6361/202348015; Jense et al. 2026, arXiv:2510.09430; Efstathiou, Rosenberg & Poulin 2024; McDonough et al. 2024. Manglende titler/DOI'er og entydige K-mappinger er ikke opfundet. Disse referencer er ikke genlæst for at erklære nogen ny fysisk konklusion.

**WHAT CHANGED**

V19 har nu et verificerbart execution-commit, run ID og slutartefakt. Numerisk noncompletion er dokumenteret for hele 32-kæde-matrixen. De to manglende sluttilstande er genfundet. Den konkrete kontraktforskel mellem den fremsendte plan og den udførte test er registreret. Næste nødvendige arbejde er en afgrænset diagnose/recovery-beslutning, ikke blind gentagelse.

**WHAT DID NOT CHANGE**

Exact CURRENT Q, CASE-041, MOD-EDE-N3's fysiske status, Q031's implementationsvaliditet, Q035-harmoniseringen, Q036–Q038-geometrien, Q039's negative interventioner og Q040's numeriske fejlgrænser bevares. Ingen EDE/ΛCDM-konklusion eller fysisk Planck-systematik tilføjes.

**FALSIFIED / REJECTED / SUPERSEDED MATERIAL**

V19 falsificerer ingen fysisk model. Følgende fortolkninger af det nye materiale er afvist: “PASS betyder, at Q041 er videnskabeligt løst”; “de to kæder, som ikke står i affected_chains, er færdige”; “V19 er den fulde oprindelige 20-cell ΛCDM/EDE/SN-test”.

Den gamle execution-status “target endnu ikke registreret / execution commit ukendt” er superseded som aktuel status. Starting-state commit `90461ac0f011dfa1f8c359c56956e770fcff4420` bevares som historisk designreference og må ikke bruges som V19-execution-commit.

KEEP DEAD fra tidligere journal: endpointforskel ⇒ fysisk Planck-systematik; endpointforskel ⇒ særskilt fysisk basin; calibration-neutralisering alene som tilstrækkelig Q036-forklaring; off-diagonal removal som tilstrækkelig forklaring; native foreground-profile freedom som tilstrækkelig forklaring; Q040's fejlslagne Gaussian/RQMC-spor som valideret endpointgenerator; direkte fysisk evidens fra absolut χ²_CamSpec−χ²_HiLLiPoP. Ingen af disse genoplives.

**OPEN UNCERTAINTIES**

1. Hvorfor mixer de faktiske kæder utilstrækkeligt under den låste V19-konstruktion? Grænserne er identificeret; den dybere sampler-/posteriorårsag er ikke.
2. Hvilke existing-chain diagnostics, checkpoints og samples kan genbruges som diagnostik eller som en lovligt versionsdokumenteret fortsættelse? V19 forbyder selv ubeskrevet reuse på tværs af programversioner.
3. Hvilken dokumenteret beslutning forbinder det fremsendte 20-cell design med V19's EDE-only common-TT-test? Ingen sådan overgang er etableret her.
4. Det oprindelige within-arm ΛCDM/EDE-resultat, de numeriske (H0,f_EDE)-konturer, SN-robustheden og hele materialitetsmatricen er fortsat ubestemte.

De konkrete gamle numeriske målinger i Q031–Q040 behøver ikke gentages for at besvare disse spørgsmål. En ny kosmologisk litteratursweep er heller ikke et krav til næste trin.

**Q-COMPLETION GATE**

**STATUS: NOT YET SATISFIED.**

Nedenfor er en audit af den fremsendte testkontrakt, ikke et opdigtet originalt T001–T019-testreport:

| Krav | Hvad evidensen tillader at skrive nu |
|---|---|
| T001 Q_IDENTITY | Q-041/program/result-ID stemmer; CASE-041 genfundet fra brugerens handoff |
| T002 CONTEXT_CONTINUITY | Arvet videnskabelig kontekst bevaret; kontraktovergangen til V19 er udokumenteret |
| T003 SOURCE_VERSION | Execution-commit og kodefiler verificeret; fuld runtime-dataaudit ikke udført |
| T004 PLANCK_NATIVE_IDENTITY | Native-afstamning/source locks dokumenteret; V19 bruger restricted common TT, ikke dokumenteret fuld original surface |
| T005 EXTERNAL_DATA_IDENTITY | A6/L6/D2 i begge arme dokumenteret i kode; krævet SN mangler |
| T006 OVERLAP_POLICY | ell-cut og antagelse dokumenteret; oprindeligt valideringskrav ikke bevist af finalfilen |
| T007 REFERENCE | Originalt specificeret reference-testreport ikke leveret |
| T008 LCDM_BASELINE | Ikke opfyldt af V19-matrixen |
| T009 JOB_COMPLETENESS | V19 final/segment-8-artefakter findes; oprindelig 20-cell model/data-matrix er ikke beregnet af V19 |
| T010 MERGE_COMPATIBILITY | V19's lineage-checks findes; ikke et bestået originalt posterior/profile-merge |
| T011 CONVERGENCE | Ikke opfyldt; 30 cap-stop og to PARTIAL-stop |
| T012 EDE_NESTING | Krævet original testresultat NOT DOCUMENTED |
| T013 GLOBALITY / RESTART | Krævet best-fit/globality-report NOT DOCUMENTED |
| T014 NUMERICAL_PRECISION | Krævet præcisionstestresultat NOT DOCUMENTED |
| T015 POSTERIOR/PROFILE_VALIDITY | Blokeret af noncompletion og manglende original model/data-matrix |
| T016 MATERIALITY HASH | V19-prereg hash verificeret; definitionen afviger fra brugerens fremsendte regel |
| T017 LOO_COMPLETENESS | Ikke opfyldt for den fremsendte FULL + fire-LOO-test |
| T018 SCIENTIFIC_FIREWALL | V19 rapporterer Q040_FIREWALL=PASS og blokerer science; ingen fysisk slutning udledes her |
| T019 FINAL_RESULT | Ikke opfyldt som videnskabeligt Q041-resultat |

Spørgsmålet kan ikke lukkes med en af de tre fysiske portabilitetsklasser. Stopårsagen “budget opbrugt” er heller ikke i sig selv bevis for, at den kosmologiske forskel principielt er uafgørlig med de relevante data.

**MATERIAL-REVERSAL TEST**

**YES.** En korrekt specificeret og tilstrækkeligt konvergeret test kan stadig give hver af de tre fysiske konklusioner. Desuden kan en læsning af de allerede producerede chain/progress/checkpoint-filer afgøre, om en begrænset, målrettet recovery er meningsfuld eller skal opgives. Det er en konkret udestående usikkerhed, ikke et ønske om flere generelle robusthedstests.

**ROUTING REASON**

Der vælges præcis én eksisterende motor: **Numerical Execution / HPC Engine**. Den er eksplicit identificeret i den fremsendte arkitektur, og repositoryets workflow/registry dokumenterer dens konkrete execution-funktion. Den kan undersøge samplerdiagnostik og genbrug af eksisterende numeriske tilstande samt specificere en korrekt afgrænset efterfølger. Der er ikke behov for at opfinde en motor.

Motor 14 er destinationen ved dokumenteret Q-afslutning; det er ikke den aktuelle tilstand. Report Writer er udelukket. Et komplet separat katalog over alle mulige Bubbleverse-motorer er ikke læst eller opfundet; valget bygger på de motorer og funktioner, som faktisk er dokumenteret i denne kontekst.

**NEXT TASK — ét præcist mål**

**Afgør på eksisterende V19-artefakter, om og hvordan den præcise oprindelige Q041-test kan bringes til en valid afgørelse med én afgrænset recovery, uden først at starte en ny fuld kampagne.**

Leverancen er én beslutningsklar recovery-specifikation eller en begrundet konklusion om, at recovery ikke er fagligt/teknisk forsvarlig under de tilgængelige betingelser. Den skal anvende denne journal og de eksisterende råartefakter; den må ikke kræve, at modtagende motor rekonstruerer spørgsmålet.

Den afgrænsede audit skal:

1. Bruge de identificerede 32 segment-8-artefakter og kun hente tidligere segmenter ved en konkret lineage-/resume-usikkerhed. Læse metadata, chain.updated.yaml, checkpoint, .progress og samples; bevare originalerne.
2. Skelne sample-cap, segment-cap, langsom adaptation, fastlåste retninger og eventuelle implementationsfejl. Se på udviklingen i R−1, accepterede samples, acceptancerate, relevante traces og faktisk sampled/nuisance-set. Beregn ikke kosmologiske konklusioner fra ikke-validerede kæder.
3. Lave en eksplicit mapping til den fremsendte 20-cell kontrakt. Eksisterende EDE-kæder kan ikke fremtrylle manglende ΛCDM- eller SN-celler. Afklar også den dokumenterede ændring af Planck-support, når A6 udelades.
4. Hvis en målrettet reparation er begrundet, beskrive præcis hvad der ændres, hvad der kan genbruges, det maksimale ekstra budget og den på forhånd fastlagte stopregel. En ny model/data-/beslutningsregel skal versionsføres som videnskabelig ændring; den må ikke kaldes en ren teknisk reparation.
5. Afslutte auditten med en konkret beslutning. Ingen automatisk eskalation til flere seeds, samplere, priors eller større kampagner.
6. Ved oprettelse eller ændring af repository-funktionalitet eller en konkret repository-opdateringspakke følge BV-EXEC-README-001: inspicere den kanoniske README og den aktuelle filstruktur, kontrollere launcher/registry/workflows/resultatstruktur, opdatere README differentielt ved ændringer af betydning for læser eller operatør, levere den faktiske README-fil ved UPDATE/CREATE og evaluere README_GATE samt REPOSITORY_CONSISTENCY_GATE. Ved ren diagnose uden repository-ændringer må der ikke opfindes en gennemført repository-opdatering.

Dette handoff starter ingen beregning og registrerer ikke noget nyt program-ID. Det er ikke en instruks om at genkøre V19 uændret. Brugerens forbud mod at skrive til GitHub gælder også en eventuel efterfølger: kode/specifikationer skal leveres som filer, medmindre brugeren senere ændrer instruktionen.

**FIXED / FROZEN ELEMENTS**

CASE-041 og exact CURRENT Q; den oprindelige indsendte rå-ZIP og dens resultater; V19's historiske preregistration/source lock/execution-commit; Q031–Q040's aktive konklusioner og afvisninger; ingen Q040-endpointgenoplivning; separate native Planck-arme; identiske eksterne data mellem armene i enhver matched sammenligning; samme n=3 EDE-modeldefinition; ingen direkte cross-arm absolut χ²-evidens; ingen lempelse af kriterier for at få et ønsket resultat. Råresultaterne må ikke omskrives efterfølgende.

For den fremsendte oprindelige test bevares desuden:

- 20 model/data-celler: to arme × ΛCDM/EDE × FULL samt minus ACT primary, ACT lensing, DESI DR2 og SN.
- Fælles rapportering: H0, f_EDE, log10(z_c), theta_i,scf, omega_b og omega_cdm; øvrige relevante cosmological/nuisance-parametre i den validerede implementation.
- D_x = abs(x_A−x_B)/sqrt(sigma_A²+sigma_B²); material location ved H0 eller f_EDE D≥1, eller mindst to primære koordinater. Svagt identificerede log10(z_c)/theta_i ved f_EDE nær nul må ikke alene afgøre materialitet.
- Numerisk (H0,f_EDE)-regionoverlap: material <0.50; substantial ≥0.50.
- Within-arm Δχ² = χ²_LCDM,best − χ²_EDE,best: negligible ≤2, modest mellem 2 og 6, substantive ≥6. Portabilitetsforskel kræver forskellige kategorier og forskel mindst 2.
- En datakombination er material ved materiel modelpræferenceforskel ELLER ved både material location OG material contour geometry.
- MATERIAL SCIENTIFIC PORTABILITY DIFFERENCE kræver material FULL og alle krævede valide LOO-tests. SCIENTIFIC DIFFERENCE COLLAPSES kræver de specificerede ikke-materiale/overlappende/portable resultater i FULL og alle valide LOO. MIXED-DATASET-CONDITIONAL kræver mindst én valid material og én valid ikke-material kombination.
- T001–T019 må ikke erstattes af et enklere grønt programstatusfelt.

**VARIABLE ELEMENTS**

I næste afgrænsede audit: diagnostiske udtræk, dokumenteret tilstandsvurdering og prospective recovery-design. Ingen ny fysisk model, likelihood, prior, tærskel eller eksisterende kæde ændres af selve auditten. Eventuelle senere ændringer skal begrundes og versionsføres med bevaret gammel evidens.

**SUCCESS CONDITION**

Auditten leverer en dokumenteret årsags-/begrænsningsvurdering og én konkret, budgetafgrænset beslutning, der faktisk kan reducere den relevante usikkerhed. En egentlig videnskabelig succes kræver derefter den korrekte matched test, de nødvendige gates og anvendelse af den dokumenterede frozen beslutningsregel. Et grønt workflow alene tæller ikke.

Hvis leverancen omfatter ny eller ændret repository-funktionalitet, er den først komplet, når README er kontrolleret, nødvendige ændringer faktisk er leveret, og både `README_GATE=PASS` og `REPOSITORY_CONSISTENCY_GATE=PASS` er dokumenteret for det kontrollerede filgrundlag. Ved filleverance angives, at gates gælder den forberedte pakke mod det inspicerede repository, ikke en allerede anvendt ændring på GitHub.

**FAILURE / FALSIFICATION CONDITION**

Hvis kompatibelt genbrug ikke kan dokumenteres, en konkret samplerreparation ikke kan begrundes, eller den korrekte test ikke kan gennemføres under et begrundet endeligt budget, registreres det som metodisk/numerisk begrænsning. Det er ikke EDE- eller ΛCDM-falsifikation. Ingen oprindelig fysisk portabilitetsklasse vælges ved fejlede gates.

En forkert, forældet eller udokumenteret README-beskrivelse af den leverede funktionalitet giver `README_GATE=FAIL`. Uoverensstemmelse mellem Q, PROGRAM_ID, program, config, workflow, registry, launcher, jobstruktur, checkpoint-system, tests og README giver `REPOSITORY_CONSISTENCY_GATE=FAIL`. Repository-leverancen må da ikke erklæres komplet. Dokumentations-/konsistensfejl er ikke fysisk modelfalsifikation.

**STOP CONDITION**

Stop denne ingestion nu: filidentitet, sluttilstand, de to manglende kædetilstande og kontraktforskellen er tilstrækkeligt dokumenteret til routing. Mere webresearch eller gentagelse af samme slutvalidator kan ikke ændre denne beslutning.

Stop den næste audit, så snart den har leveret den ene recovery-/begrænsningsbeslutning. Start ikke endnu en ubestemt valideringssløjfe.

Stop den aktive Q og route direkte til **BUBBLEVERSE — MOTOR 14: AUTONOMOUS UNIVERSE REVISION**, når enten (a) den korrekte test har bestået de krævede gates og kan klassificeres legitimt, eller (b) en afgrænset undersøgelse har dokumenteret en tilstrækkelig INCONCLUSIVE/begrænsningskonklusion, hvor intet konkret resterende arbejde med rimelighed forventes at ændre Q-svaret. Mulighed (b) giver ingen tilladelse til at vælge en fysisk portabilitetsklasse med fejlede gates. V19's sampleloft alene opfylder ikke denne afslutningsbegrundelse.

Ved repository-leverancer gælder desuden de ti README-stopkriterier i bilag D. Arbejdet er ikke færdigt, før den kanoniske README er inspiceret, nødvendige rettelser leveret, referencer og operatørinstruktioner kontrolleret, og begge gates faktisk evalueret. Et FAIL bevares og skal løses inden en påstand om en komplet repository-opdatering. README-kontrollen erstatter hverken de videnskabelige gates eller Q-completion-reglen.

**FILE DECISIONS — obligatorisk README-post ved repository-leverancer**

Medtag altid den faktiske kanoniske README-sti. Vælg `UNCHANGED`, `UPDATE` eller `CREATE` med en konkret begrundelse fra de inspicerede filer. Brug `UNCHANGED`, når kontrollen viser, at ingen relevant oplysning skal ændres. Ved `UPDATE` eller `CREATE` leveres den faktiske fil sammen med funktionaliteten. Opret ikke en konkurrerende README, hvis en anden fil allerede er kanonisk.

**README STATUS — påkrævet svarblok ved repository-leverancer**

```text
README:
ACTION: UNCHANGED / UPDATE / CREATE
FILE: README.md (eller den verificerede kanoniske README-sti)
REASON: <konkret begrundelse>
README_GATE: PASS / FAIL
REPOSITORY_CONSISTENCY_GATE: PASS / FAIL
VALIDATION_SCOPE: <inspiceret repository-commit og eventuel forberedt filpakke>
DELIVERY: <den faktiske README-fil ved UPDATE/CREATE; ellers UNCHANGED>
APPLICATION_STATUS: <PREPARED FILE PACKAGE eller faktisk dokumenteret anvendelse>
```

Blokken er en instruktion til næste repository-leverance, ikke en erklæring om beståede gates nu. Denne revision tilføjer motorinstruktioner til overleveringen; den foretager ingen repository-modifikation og hævder ingen ny README-validering. Brugerens instruks om ikke at skrive til GitHub eller starte workflows gælder fortsat.

**START THIS:** Intet nyt executable target er oprettet eller startet. Ingen GitHub-mutation er udført.

**Bilag A — uændrede direkte outputs**

**q041_final_v19.json**

```json
{
  "actual_computed_result": false,
  "claim_boundaries": {
    "Q040_scientific_products_used": false,
    "controlled_numerical_noncompletion_is_not_physical_evidence": true,
    "no_cross_arm_chi2_sum": true,
    "no_hybrid_planck_likelihood": true,
    "technical_failure_would_not_be_encoded_as_green_final": true
  },
  "details": {
    "affected_chains": [
      [
        "camspec",
        "P",
        0
      ],
      [
        "camspec",
        "P",
        1
      ],
      [
        "camspec",
        "P_A6",
        0
      ],
      [
        "camspec",
        "P_A6_D2",
        0
      ],
      [
        "camspec",
        "P_A6_D2",
        1
      ],
      [
        "camspec",
        "P_A6_L6",
        0
      ],
      [
        "camspec",
        "P_A6_L6",
        1
      ],
      [
        "camspec",
        "P_A6_L6_D2",
        0
      ],
      [
        "camspec",
        "P_D2",
        0
      ],
      [
        "camspec",
        "P_D2",
        1
      ],
      [
        "camspec",
        "P_L6",
        0
      ],
      [
        "camspec",
        "P_L6",
        1
      ],
      [
        "camspec",
        "P_L6_D2",
        0
      ],
      [
        "camspec",
        "P_L6_D2",
        1
      ],
      [
        "hillipop",
        "P",
        0
      ],
      [
        "hillipop",
        "P",
        1
      ],
      [
        "hillipop",
        "P_A6",
        0
      ],
      [
        "hillipop",
        "P_A6",
        1
      ],
      [
        "hillipop",
        "P_A6_D2",
        0
      ],
      [
        "hillipop",
        "P_A6_D2",
        1
      ],
      [
        "hillipop",
        "P_A6_L6",
        0
      ],
      [
        "hillipop",
        "P_A6_L6",
        1
      ],
      [
        "hillipop",
        "P_A6_L6_D2",
        0
      ],
      [
        "hillipop",
        "P_A6_L6_D2",
        1
      ],
      [
        "hillipop",
        "P_D2",
        0
      ],
      [
        "hillipop",
        "P_D2",
        1
      ],
      [
        "hillipop",
        "P_L6",
        0
      ],
      [
        "hillipop",
        "P_L6",
        1
      ],
      [
        "hillipop",
        "P_L6_D2",
        0
      ],
      [
        "hillipop",
        "P_L6_D2",
        1
      ]
    ],
    "segment": 8
  },
  "final_outcome_valid": true,
  "no_science_reason": "MAX_SAMPLES_WITHOUT_CONVERGENCE",
  "outcome_type": "CONTROLLED_NO_SCIENTIFIC_RESULT",
  "program_id": "Q041-PLANCKPORT-V19",
  "q": "Q-041",
  "required_gates": {
    "ALL_RHAT_LE_1P05": "BLOCKED",
    "BOTH_ARMS_ALL_COMBINATIONS": "BLOCKED",
    "CHAIN_COMPLETENESS": "BLOCKED",
    "Q040_FIREWALL": "PASS",
    "SEGMENTED_RESUME_COMPLETENESS": "CONTROLLED_STOP"
  },
  "result_id": "R-Q041-EDE-DOWNSTREAM-PORTABILITY-019",
  "run_id": "Q041-DOWNSTREAM-SCIENTIFIC-CONSEQUENCE-PORTABILITY-V19",
  "scientific_classification": "NO_SCIENTIFIC_RESULT",
  "stage": "FINAL",
  "status": "PASS",
  "technical_failure": false
}
```

**q041_final_tests_v19.json**

```json
{
  "classification": "NO_SCIENTIFIC_RESULT",
  "outcome_type": "CONTROLLED_NO_SCIENTIFIC_RESULT",
  "program_id": "Q041-PLANCKPORT-V19",
  "q": "Q-041",
  "stage": "FINAL_TESTS",
  "status": "PASS"
}
```

**Bilag B — fil- og kildeoversigt**

Den oprindelige evidenspakke fra V19-ingestion indeholder den oprindelige overlevering, den originale indsendte ZIP, de to udtrukne uændrede JSON-filer, den lokale final-test-replay, machine-readable ingestion decision, provenance.json, source_snapshot_manifest.json, de otte læste repository-filer, tre joblogs med diagnostiske udtræk og den genfundne arvede journaltekst. Denne overlevering er efterfølgende suppleret med README-motorinstruktionerne; den tidligere evidenspakke er bevaret uændret som historisk kilde. `bundle_manifest_sha256.json` muliggør kontrol af de medfølgende bytes. Kædernes sample/checkpoint-ZIP'er er ikke med i pakken, da bytehentningen ikke lykkedes; deres præcise GitHub-artifact-identiteter medfølger.

**Bilag C — bevaret historisk Q031–Q040-journaltekst**

Kilde: bubblevers 0.40mmmtt(5).docx, journalafsnit Q031–Q040, læst 2026-09-23. Nedenfor bevares den returnerede tekst, inklusive historiske statusser, henvisninger og eventuelle tekstudtræksartefakter. Det er et historisk bilag; aktiv fortolkning og routing står ovenfor. Især bogens tidligere Q041-forslag om RQMC må ikke erstatte det aktive downstream-portabilitetsspørgsmål.

BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q031
Date/time: 2026-09-05, successful run completed 18:54 UTC
Status: REJECTED
<PARSED TEXT FOR PAGE: 301 / 348>
Question: Does the distributed, multibasin, mask-dependent, covariance-coupled 
n=3 EDE geometry found in frozen Planck NPIPE/CamSpec survive materially under
an independent Planck PR4/NPIPE likelihood implementation?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; n_scf=3; active/constrained; 
class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited results: Q021–Q030 established distributed primordial response, stable 
mixed cosmology–nuisance CamSpec basins, no universal basin direction, 
distributed attribution, ω_cdm×A_planck coupling, common-support separation, 
and exact validated factorial geometry.
Constraint: test portability without changing frozen physics, retrospectively 
redefining basin criteria, summing cross-likelihood objectives, or forcing nuisance 
equivalence.
3. HYPOTHESES
Tested:
H1: Q022-type stable multibasin geometry survives in independent HiLLiPoP.
H2: Geometry remains separated but fails reproducible stable-basin support.
H3: Implementation fails, leaving portability unresolved.
Rejected: H1 — stable_basin_count=0. H3 — implementation and validation passed.
<PARSED TEXT FOR PAGE: 302 / 348>
Surviving: H2 — implementation-specific likelihood geometry; residual separated 
endpoints remain.
4. METHOD & EVIDENCE
Method: HiLLiPoP PR4/NPIPE TTTEEE v4.3, same frozen n=3 backend; 9 mapped 
multistarts + mandatory tighter refinement; frozen Q022 stability criterion 
Δobjective 0.50 and normalized RMS 0.10 with repeated support. ≤ ≤
Sources: HiLLiPoP/Planck PR4 literature; Tristram et al. 2024; Efstathiou, Rosenberg 
& Poulin 2024; McDonough et al. 2024.
Program/workflow: q031_planck_portability_v1.py; .github/workflows/q031-planck￾portability-v4.yml.
Tests: independent-implementation, completeness, multibasin, final-result/claim￾boundary validation.
5. KEY RESULTS
9/9 primary starts completed; 9/9 refinements completed.
Stable_basin_count=0.
MATERIAL_STABLE_MULTIBASIN_GATE=FAIL.
Direction gate=NOT_TESTABLE; downstream primordial/compensation 
gates=NOT_RUN by preregistered stop logic.
Near-degenerate separated examples:
<PARSED TEXT FOR PAGE: 303 / 348>
M3-S0 M7-S2: Δobjective=0.2335; RMS=3.4915. ↔
M6-S2 M7-S1: Δobjective=0.3803; RMS=7.8245. ↔
Final result: Q021–Q030 stable CamSpec geometry does not port to HiLLiPoP under 
the frozen criterion.
Limitation: one independent likelihood tested; mechanism causing non-portability 
remains unidentified.
Contradiction: none fundamental; CamSpec vs HiLLiPoP creates implementation￾structure tension.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 environment/setup; V2 Python/cache configuration; V3 Q022 
stage/refinement artifact collision. All technical, no scientific result.
Mikami Graveyard: “Cross-implementation Planck n=3 EDE likelihood geometry” — 
rejected under Q031. Universal interpretation of Q021–Q030 deleted; internal 
CamSpec results preserved.
7. MODEL CHANGE
Before: Q021–Q030 geometry potentially generalizable beyond CamSpec.
After: IMPLEMENTATION-SPECIFIC INTERNAL LIKELIHOOD GEOMETRY.
Change: CONSTRAINED / GENERALIZATION REJECTED.
Reason: validated independent HiLLiPoP portability failure.
<PARSED TEXT FOR PAGE: 304 / 348>
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Successful commit: ff621d6e0a425a976bb7a55f9194a0de8a87f18f
Workflow: q031-planck-portability-v4.yml
Run: 33975028436
Result: R-CASE031-EDE-PLANCK-PORTABILITY-001
Artifact: q031-final-v1, ID 9975019737
Validated file: q031_final_validated_v1.json
HiLLiPoP commit: a09ddde3e7ce11df99f74685feb1f1764cafb251.
9. REPRODUCIBILITY
Checkout recorded commit; obtain frozen Q021/Q022 parents and HiLLiPoP PR4 
data; run V4 workflow with recorded backend/criteria; compare 
q031_final_validated_v1.json; require the same frozen portability gates.
10.CONCLUSION
Q031 rejected cross-implementation portability of the stable Q022-type CamSpec 
basin geometry. The internal Q021–Q030 calculations remain valid, but their scope 
is narrowed to the frozen CamSpec implementation. No Planck systematic, 
calibration failure, EDE falsification, or new physics was established.
11.NEXT-Q HANDOFF
<PARSED TEXT FOR PAGE: 305 / 348>
Next Q: Q032
Reason: portability failure is established; its implementation-level cause is not.
Next question: Can the CamSpec–HiLLiPoP portability failure be localized to 
foreground modelling, calibration/nuisance structure, covariance, 
frequency/support construction, or a distributed interaction among them?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Portability rejected under the frozen Q031 test.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Universal cross-implementation geometry killed; 
internal CamSpec geometry retained.
MODEL CHANGE SUMMARY: General Planck interpretation implementation- →
specific CamSpec geometry.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; run 33975028436; commit 
ff621d6e…; V4 workflow; validated result above.
NEXT-Q HANDOFF: Q032 — identify the cause of CamSpec–HiLLiPoP non￾portability.
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
<PARSED TEXT FOR PAGE: 306 / 348>
Q-ID: Q032
Date/time: 2026-09-06, final result; exact completion time not independently 
recorded here
Status: CONFIRMED
Question: Can the CASE-031 portability failure be localized to one or a small 
preregistered set of differences between the frozen Planck NPIPE/CamSpec full￾multifrequency likelihood and HiLLiPoP PR4/NPIPE, or does the loss of stable 
multibasin structure remain distributed across implementation changes?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; n_scf=3; mwt5345/class_ede 
5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited: Q022 historical stable CamSpec multibasin classification; CASE-031 
HiLLiPoP portability failure (stable_basin_count=0).
Constraints: same model/priors/basin thresholds; 9 starts M3/M6/M7; no new seeds; 
no Q024/Q030 reruns; no causal A_planck interpretation.
3. HYPOTHESES
Tested:
H1: removed TT SUPPORT causes loss.
H2: TE or EE causes loss.
H3: a small combination of SUPPORT/TE/EE restores stable geometry.
<PARSED TEXT FOR PAGE: 307 / 348>
Rejected: H1–H3; no single, pairwise, or full three-sector restoration recovered 
stable multibasin structure.
Surviving: broader likelihood/execution-semantics dependence.
4. METHOD & EVIDENCE
Method: common-support bridge followed by corrected exact-scalar-start CamSpec 
add-back hierarchy: SUPPORT, TE, EE all pairs FULL_NATIVE. → →
Sources: K-044 CamSpec PR4; K-046 Cobaya 3.5.6 technical implementation; 
HiLLiPoP v4.3 technical source.
Programs/workflows: q032_exact_start_addback_v4.py; .github/workflows/q032-
exact-start-addback-v4.yml.
Run: GitHub Actions 34015845246.
Tests: exact scalar reference/start provenance; covariance selection; finite 
likelihood; completeness; globality; interpretation; FINAL_RESULT_GATE.
5. KEY RESULTS
Exact-start TT3 baseline: stable_basin_count=0.
SUPPORT, TE, EE: all 0.
SUPPORT+TE, SUPPORT+EE, TE+EE: all 0.
FULL_NATIVE SUPPORT+TE+EE: 0.
Final result: 
NO_CLEAN_LOCALIZATION_WITHIN_TESTED_CAMSPEC_INFORMATION_SECTORS.
<PARSED TEXT FOR PAGE: 308 / 348>
Limitations: methodological likelihood geometry only; does not identify 
physical/systematic cause or confirm/falsify EDE.
Contradiction: historical Q022 stable classification is not reproduced under genuine 
scalar exact-start semantics.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: Q032 V1 nuisance leakage technical failure; Q032 V3 optimizer →
failure plus incorrect non-scalar start semantics no scientific result. →
Graveyard: clean SUPPORT-only, TE-only, EE-only, pairwise, and three-sector 
restoration explanations killed. V2 claim that removed information was materially 
required is superseded.
7. MODEL CHANGE
Before: historical CamSpec geometry treated as stable multibasin, with CASE-031 
showing non-portability.
After: historical endpoint geometry retained, but stable-basin interpretation is 
execution-semantics dependent; no small CamSpec sector explains portability loss.
Change: MODIFIED / CONSTRAINED.
Reason: Q032 V4 exact-start full-native result.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
V4 execution HEAD: fbde93aee01ec3bed183207518ff315c96a45c3c
Workflow: .github/workflows/q032-exact-start-addback-v4.yml
<PARSED TEXT FOR PAGE: 309 / 348>
Program: q032_exact_start_addback_v4.py
Result: R-Q032-EDE-CAMSPEC-ADDBACK-004
Run: 34015845246
Provenance: Q022 endpoint vectors + frozen CamSpec/model configuration; V4 
corrected Cobaya refs to literal scalar starts.
9. REPRODUCIBILITY
Checkout recorded commit obtain frozen inputs/Q022 vectors run V4 workflow → →
unchanged compare baseline/tier/control outputs apply basin criteria → →
Δobjective 0.50, RMS 0.10, support 2 and mandatory gates. ≤ ≤ ≥
10.CONCLUSION
Q032 found no clean localization of the CASE-031 portability failure to SUPPORT, TE,
EE, or their combinations. Even full-native CamSpec remains non-stable under 
corrected exact-start semantics. The historical geometry is therefore best treated as 
likelihood/execution-dependent endpoint geometry, not an execution-invariant 
stable-basin property.
11.NEXT-Q HANDOFF
Why: determine whether launch/reference semantics alone explain the 
Q022 Q032 difference. ↔
Next Q: Q033
Question: Under frozen full-MF CamSpec MOD-EDE-N3, can the historical Q022 
stable classification versus Q032 V4 non-stability be explained by 
<PARSED TEXT FOR PAGE: 310 / 348>
launch-point/reference-distribution semantics alone with all other components 
matched?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No clean small-sector localization; execution semantics materially 
matter.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: SUPPORT/TE/EE localization routes killed.
MODEL CHANGE SUMMARY: Q022 stable-basin interpretation constrained to 
historical execution semantics.
REPRODUCIBILITY / GITHUB: R-Q032-EDE-CAMSPEC-ADDBACK-004, run 
34015845246, HEAD fbde93a….
NEXT-Q HANDOFF: Q033 — isolate launch/reference semantics.
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q033
Date/time: 2026-09-06 21:45 CEST
Status: CONFIRMED
Journal type: RETROSPECTIVE RECONSTRUCTION
Reconstructed on: 2026-09-08
<PARSED TEXT FOR PAGE: 311 / 348>
Question: Can Q022’s stable-multibasin versus Q032 V4’s non-stable FULL_NATIVE 
result be explained by launch/reference-distribution semantics alone?
2. STARTING STATE
Model: MOD-EDE-N3; (n_{\rm scf}=3); frozen ”mwt5345/class_ede” commit 
”5a131c91…”.
Inherited: Q022 
”STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE”; Q032 V4 
”stable_basin_count=0”, ”NO_CLEAN_LOCALIZATION…”.
Constraint: Preserve model, likelihood, numerical settings and historical execution; 
test only launch/reference semantics.
3. HYPOTHESES
H1 / HYP-Q033-A: Q022 used non-scalar refs while Q032 used scalar refs.
H2 / HYP-Q033-B: Launch semantics are insufficient; another implementation 
difference exists.
Rejected: H1 — historical runtime reconstruction showed Q022 refs were already 
scalar.
Surviving: H2 — strengthened.
4. METHOD & EVIDENCE
<PARSED TEXT FOR PAGE: 312 / 348>
Method: Source/provenance audit of Q019 Q021 Q022 versus Q032 V4; no new → →
likelihood optimization.
Programs: ”q033_launch_semantics_protocol_audit_v2.py”; config/source-lock/tests; 
workflow ”.github/workflows/q033-launch-semantics-protocol-audit-v2.yml”.
Evidence: Q022 run ”33902262660”; Q032 V4 run ”34015845246”; Cobaya 3.5.6 
semantics; frozen historical source blobs.
5. KEY RESULTS
- Q022 sampled non-primordial refs: scalar before/after recentering.
- Q032 V4 sampled refs: scalar.
- Remaining sampled-set difference: Q032 additionally samples ”n_s”, ”logA”, 
”tau_reio”; Q022 freezes them.
- Final result: 
”LAUNCH_REFERENCE_SEMANTICS_ALREADY_IDENTICAL_NOT_CAUSAL”.
Limit: Cause of Q022/Q032 discrepancy remains unresolved.
Contradiction: Stable Q022 versus non-stable Q032 remains a technical 
parameterization/implementation tension, not a physical anomaly.
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q033 V1 preflight: 
”NONSCALAR_HISTORICAL_REFERENCE_GATE=FAIL”; no scientific likelihood result.
<PARSED TEXT FOR PAGE: 313 / 348>
Graveyard: HYP-Q033-A and planned 18-job distribution-vs-scalar campaign — 
killed because the proposed historical distribution arm never existed.
7. MODEL CHANGE
Before: Q022/Q032 difference partly attributed to launch/reference semantics.
After: That explanation removed; ”D-Q033-REMAINING-001” registered: frozen vs 
sampled primordial block.
Change: Technical interpretation corrected; physical EDE/H₀ conclusions 
unchanged.
8. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Q022 commit: ”16a7902c…”
Q032 commit: ”fbde93aee…”
Q033 files added: ”b03a1ac5…”; workflow placement ”614b227c…”
Result: ”R-Q033-EDE-LAUNCH-SEMANTICS-AUDIT-002”
Q033 GitHub run ID: NOT RECORDED IN SUPPLIED FINAL ARTIFACT.
9. REPRODUCIBILITY
Checkout recorded versions obtain Q022/Q032 artifacts run Q033 V2 audit with → →
frozen source lock verify scalar-ref identity and sampled-set delta require → →
”FINAL_RESULT_GATE=PASS”.
<PARSED TEXT FOR PAGE: 314 / 348>
10.CONCLUSION
NO. Launch/reference representation cannot explain the Q022/Q032 classification 
difference because both executed paths used scalar pointlike refs. The smallest 
identified remaining difference is whether ”n_s”, ”logA”, ”tau_reio” are frozen or 
sampled.
11.NEXT-Q HANDOFF
Next Q: Q034
Question: Under otherwise matched FULL_NATIVE CamSpec conditions, does 
freezing versus sampling ”n_s”, ”logA”, ”tau_reio” reproduce the stable-versus-non￾stable classification difference?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: NO — launch/reference semantics were already identical.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: HYP-Q033-A + unnecessary 18-job V1 route killed.
MODEL CHANGE SUMMARY: Launch-semantics explanation removed; frozen-vs￾sampled primordial block becomes next candidate.
REPRODUCIBILITY / GITHUB: Repo, commits, workflow and result Ids above.
NEXT-Q HANDOFF: Q034 tests ”n_s/logA/tau_reio” freeze versus sampling.
BUBBLEVERSE — Q-JOURNAL
<PARSED TEXT FOR PAGE: 315 / 348>
1. IDENTITY
Q-ID: Q034
Date/time: 2026-09-06–07
Status: CONSTRAINED
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:40 CEST
Question: Does fixing n_s,\log A,\tau_{\rm reio} in the later full-native CamSpec 
construction restore the stable multibasin structure reported historically in Q022?
2. STARTING STATE
Model entering Q: MOD-EDE-N3 / ACTIVE, CONSTRAINED / not established new 
physics.
Inherited:
- Q032 V4 FULL_NATIVE: stable_basin_count = 0.
- Q033: scalar-vs-distribution launch semantics rejected; fixed-vs-sampled 
primordial block remained candidate difference.
Constraint: Change only primordial fixed/sampled status; preserve backend, 
likelihood construction, starts, optimizer and classifier.
3. HYPOTHESES
<PARSED TEXT FOR PAGE: 316 / 348>
H1: Primordial freezing restores stable basins.
H2: It does not.
Rejected: H1.
Surviving: H2 under the later common-geometry classifier.
4. METHOD & EVIDENCE
Method: Artifact-locked matched isolation. Q032 FULL_NATIVE sampled control 
reused; Q034 fixed n_s,\log A,\tau_{\rm reio} and repeated required refinement.
Primary evidence: Morfindien/Bubbleverse; Q032 V4 artifacts; frozen 
mwt5345/class_ede commit ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Programs/workflows:
”q034_primordial_freeze_isolation_v1.py”
”q034_primordial_freeze_isolation_v1_config.yml”
”.github/workflows/q034-primordial-freeze-isolation-v1.yml”
Run: GitHub Actions ”34059649759”, head 
”8b8035795a9e6064583379afb8663cdc28961764”.
5. KEY RESULTS
- Sampled Q032 control: stable_basin_count = 0.
<PARSED TEXT FOR PAGE: 317 / 348>
- Frozen Q034 arm: stable_basin_count = 0; stable_multibasin = false.
- After refinement: 9 singleton clusters, not repeated stable basins.
Final result: Freezing the primordial block is insufficient to restore stable 
multibasin structure under the later classifier.
Limitation: Historical Q022 used a different basin classifier; global Q022 Q034 ↔
comparison therefore remains unresolved.
Contradiction: Historical Q022 “stable” and later “non-stable” labels are not 
classifier-equivalent.
6. NEGATIVE RESULTS / MIKAMI
Failed hypothesis: Fixed-vs-sampled primordial parameters alone explain the 
discrepancy.
Graveyard: ”D-Q033-REMAINING-001” — rejected as sufficient under the 
Q031/Q032/Q034 common-geometry classifier.
7. MODEL CHANGE
Before: Primordial parameterization remained leading unresolved implementation 
difference.
After: Insufficient under later classifier; classifier semantics become conclusion￾critical.
Change: CONSTRAINED.
Reason: Frozen arm still produced zero stable basins.
<PARSED TEXT FOR PAGE: 318 / 348>
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: ”8b8035795a9e6064583379afb8663cdc28961764”
Workflow: ”q034-primordial-freeze-isolation-v1.yml”
Artifact: ”q034-final-v1”, ID ”9998302123”
SHA-256: ”0df519645906dfaaf3b270d9791a74c0f33f25e9fdcfa8ca344ad2add70f8a87”
9. REPRODUCIBILITY
Checkout recorded commits obtain Q032 decisive artifacts run Q034 workflow → →
with frozen primordial coordinates verify nine completed/refined endpoints → →
apply identical later graph-classifier thresholds and compare final artifact.
10.CONCLUSION
Q034 rejects primordial freezing as a sufficient explanation within the later 
classifier. It does not invalidate Q022, Q032, or Q034 raw results. The remaining 
discrepancy is methodological because Q022 and Q031–Q034 used different basin￾classification definitions.
11.NEXT-Q HANDOFF
Next Q: Q035
Why: Determine whether the stable/non-stable discrepancy survives use of identical
classifiers.
<PARSED TEXT FOR PAGE: 319 / 348>
Next question: When the decisive Q022, Q032 V4 FULL_NATIVE and Q034 frozen 
endpoint sets are evaluated under both classifier definitions, does the reported 
discrepancy survive classifier harmonization?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Primordial freezing does not restore stable basins under the later 
classifier.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Fixed-vs-sampled primordial block killed as 
sufficient explanation under later classifier.
MODEL CHANGE SUMMARY: MOD-EDE-N3 unchanged physically; methodological 
interpretation constrained.
REPRODUCIBILITY / GITHUB: Run ”34059649759”; head ”8b803579…”; artifact ”q034-
final-v1”.
NEXT-Q HANDOFF: Q035 — classifier harmonization.
BUBBLEVERSE — Q-JOURNAL
Q-ID: Q035
Date/time: 2026-09-08 20:42 CEST
Status: CONFIRMED
Question: When the same decisive Q022, Q032 V4 FULL_NATIVE and Q034 frozen￾primordial endpoints are evaluated under both the historical Q022 classifier and 
<PARSED TEXT FOR PAGE: 320 / 348>
later Q031/Q032 classifier, does the reported stable/non-stable discrepancy survive 
harmonization?
1. STARTING STATE
Model: MOD-EDE-N3; n_scf=3; class_ede 
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”; active/constrained, not 
established new physics.
Inherited: Q022 = historically STABLE_MULTIBASIN; Q032/Q034 = non-stable under 
later common-geometry classifier. Q033 rejected launch/reference semantics as 
cause.
Constraint: Existing endpoints only; no new likelihood, optimization, sampling, 
seeds, thresholds or physics changes.
2. HYPOTHESES
H1: Discrepancy survives same-classifier comparison. REJECTED.
H2: Classifier semantics materially explain discrepancy. CONFIRMED.
H3: Primordial freeze/sample difference is required explanation. REJECTED as 
necessary/sufficient.
3. METHOD & EVIDENCE
Deterministic artifact-only cross-classification of the same Q022/Q032/Q034 
endpoint sets with both source-locked classifier definitions.
<PARSED TEXT FOR PAGE: 321 / 348>
Evidence: Q022 run ”33902262660”; Q032 run ”34015845246”; Q034 run 
”34059649759”.
Programs: ”q022_globality_continuation_v2.py”; ”q031_planck_portability_v1.py”; 
”q032_planck_tt3pair_bridge_v2.py”; ”q035_classifier_harmonization_v1.py”.
Tests: endpoint completeness; reference replay; historical-all-stable; later-all￾nonstable; all-sets-flip; same-classifier-discrepancy-removed; physical-safety; 
FINAL_RESULT_GATE.
4. KEY RESULTS
Historical Q022 classifier: Q022/Q032/Q034 = STABLE.
Later common-geometry classifier: Q022/Q032/Q034 = NON-STABLE.
Thus both same-classifier cross-case discrepancies = FALSE and all endpoint sets flip
together with classifier choice.
Final result: 
”CLASSIFIER_SEMANTICS_MATERIALLY_EXPLAINS_REPORTED_DISCREPANCY”.
Limitations: Does not determine which classifier is physically preferable; does not 
establish identical raw geometry, Planck systematics, EDE evidence/falsification or 
new physics.
Contradiction discovered: CASE-031 negative portability interpretation is weakened 
because Q022 also fails its stable-basin gate under the same later classifier.
5. NEGATIVE RESULTS / MIKAMI
Original Q035 GitHub workflow failed with ”FileNotFoundError” from Q022 artifact 
path layout; technical failure only, no scientific evidence.
<PARSED TEXT FOR PAGE: 322 / 348>
Graveyard: same-classifier assumption; primordial freeze/sample as 
necessary/sufficient cause; interpretation that Q022 stable Q032/Q034 non-stable →
demonstrated disappearance of physical basin structure.
6. MODEL CHANGE
Before: Q022 stable vs later non-stable treated as potentially genuine cross-case 
geometry change.
After: Stable/non-stable label explicitly classifier-dependent; raw endpoints 
retained. CASE-031 portability conclusion reopened.
Change: Methodological interpretation modified; physical MOD-EDE-N3/H₀ status 
unchanged.
7. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Commits: Q022 ”16a7902…”; Q031 ”ff621d6…”; Q032 ”fbde93a…”; Q034 ”8b80357…”; 
Q035 program ”b1166e8…”; Q035 V2 workflow ”e12bab3…”.
Workflow: ”.github/workflows/q035-classifier-harmonization-v2.yml”
Outputs: ”q035_classifier_crosswalk_v1.json/.csv”, ”q035_tests_v1.json”, 
source-lock/config files.
Note: Successful Q035 V2 Actions run ID NOT RECORDED / NOT AVAILABLE.
8. REPRODUCIBILITY
<PARSED TEXT FOR PAGE: 323 / 348>
Checkout recorded versions obtain authoritative Q022/Q032/Q034 artifacts run → →
Q035 crosswalk unchanged reproduce both classifier outputs require recorded → →
gates and final classification. No endpoint rounding or threshold tuning.
9. CONCLUSION
The former Q022-versus-Q032/Q034 stable/non-stable discrepancy disappears when 
classifier choice is controlled. The endpoints remain valid; the basin label is not 
classifier-invariant.
10.NEXT-Q HANDOFF
Next: Q036 — HIGH
Question: Under identical Q031 common coordinates/scales and without binary 
stable labels, do Q022 CamSpec and CASE-031 HiLLiPoP endpoints show a material 
reproducible geometric difference supporting implementation-specific non￾portability?
Start motor: NUMERICAL / HPC / MOTOR-BUILDER; preferably artifact-only.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No; classifier semantics materially explain the reported 
discrepancy.
Q-JOURNAL: This entry.
MIKAMI: Same-classifier assumption and freeze/sample global explanation retired.
MODEL CHANGE: Basin ontology classifier-dependent; physical model →
unchanged.
<PARSED TEXT FOR PAGE: 324 / 348>
REPRODUCIBILITY: ”Morfindien/Bubbleverse”, sources/runs/commits above.
NEXT-Q: Q036 — harmonized CamSpec–HiLLiPoP raw-geometry portability test.
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:43 CEST
1. IDENTITY
Q-ID: Q036
Date/time: 2026-09-07 09:44 CEST
Status: CONFIRMED
Question: Do Q022 CamSpec and CASE-031 HiLLiPoP endpoints show a material, 
reproducible difference under the same Q031 common coordinates/scales when 
stable/non-stable labels are not the sole discriminator?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW 
PHYSICS.
Inherited:
Q035: classifier semantics explain the former stable/non-stable discrepancy.
<PARSED TEXT FOR PAGE: 325 / 348>
Q022 CamSpec + CASE-031 HiLLiPoP validated endpoint sets.
Constraints: Seven Q031 common coordinates; locked scales; threshold 0.10; no 
cross-likelihood χ²/objective subtraction or summation; no new likelihood/optimizer
runs.
3. HYPOTHESES
Tested:
H1: Material continuous geometry difference survives.
H2: Difference disappears under common geometry.
H3: Classifier semantics explain the entire portability signal.
Rejected: H2/H3 — continuous location and shape differences remain large.
Surviving: H1 — CONFIRMED within tested geometry.
4. METHOD & EVIDENCE
Method: Deterministic artifact-only comparison of 9 matched endpoints plus 36 
internal pairwise distances.
Evidence: Q022 run 33902262660; CASE-031 run 33975028436; Q035 classifier 
harmonization.
<PARSED TEXT FOR PAGE: 326 / 348>
Program: q036_endpoint_geometry_portability_v1.py
Workflow: .github/workflows/q036-endpoint-geometry-portability-v5.yml
Authoritative run: 34105942065
Tests: identity/provenance; common-coordinate/scale lock; finite results; 
permutation invariance; Q031 replay; decision replay; no-cross-likelihood-objective 
gate.
5. KEY RESULTS
Matched median RMS = 2.3623; 9/9 > 0.10.
Pairwise median drift = 2.2590; 36/36 > 0.10.
Centroid shift = 1.5371.
Q031 replay error = 8.88×10⁻¹⁶.
FINAL_RESULT_GATE = PASS.
Final result: MATERIAL_REPRODUCIBLE_COMMON_GEOMETRY_DIFFERENCE.
Limitations: Does not identify the cause, a physical Planck systematic, preferred 
likelihood, or evidence for/against EDE. CamSpec/HiLLiPoP share Planck 
information.
Contradictions: None with Q035; Q035 concerns classifier labels, Q036 continuous 
geometry.
<PARSED TEXT FOR PAGE: 327 / 348>
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q036 V4 failed provenance gate from one incorrect artifact digest; 
technical only, superseded by V5.
Graveyard additions:
“No material CamSpec–HiLLiPoP geometry difference” — rejected.
Stable/non-stable label as sole portability evidence remains dead from Q035.
7. MODEL CHANGE
Before: CASE-031 portability interpretation weakened after Q035.
After: 
NARROWED_IMPLEMENTATION_SPECIFIC_NON_PORTABILITY_REHABILITATED.
Change: MODIFIED / REFINED.
Reason: Continuous common-geometry difference survives classifier 
harmonization.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Q036 execution commit: 095f90565cf694a7c3383d1fbe736707ab187751
<PARSED TEXT FOR PAGE: 328 / 348>
Parent commits: Q022 16a790…; Q031 ff621d…
Workflow: q036-endpoint-geometry-portability-v5.yml
Outputs: q036-final-v1, q036-tests-v1, q036-return-handoff-v1, q036-run-manifest-v1.
Provenance: Existing validated Q022/Q031 artifacts only; no new likelihood 
evaluations.
9. REPRODUCIBILITY
Checkout recorded commits obtain locked Q022/Q031 artifacts run Q036 V5 → →
workflow compare outputs with q036-final-v1 apply locked 0.10 location/shape → →
criteria.
10.CONCLUSION
Q036 confirms a large reproducible CamSpec–HiLLiPoP endpoint-geometry 
difference under identical normalized coordinates/scales. Q035 remains correct: the
old binary classifier argument was invalid, but continuous non-portability survives.
11.NEXT-Q HANDOFF
Why: Cause of the implementation-dependent geometry remains unresolved.
Next Q: Q037
Question: Does the same material continuous geometry difference survive when 
Q032’s exact TT common-support CamSpec/HiLLiPoP endpoints are compared using 
the Q036 metric?
<PARSED TEXT FOR PAGE: 329 / 348>
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: YES — material continuous common-geometry difference 
confirmed.
Q-JOURNAL: This entry.
MIKAMI: No-difference route rejected; classifier-only portability route remains 
dead.
MODEL CHANGE: CASE-031 narrowed non-portability rehabilitated.
REPRODUCIBILITY: Q036 V5, run 34105942065, listed commits/artifacts.
NEXT-Q: Q037 — common-support replay.
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q037
Date/time: 2026-09-07, CEST
Status: SUPPORTED
Question: When Q032’s validated CamSpec/HiLLiPoP exact-TT common-support 
endpoints are tested with Q036’s continuous seven-coordinate geometry, Q031 
locked scales and 0.10 threshold, does the material location/shape difference 
persist?
<PARSED TEXT FOR PAGE: 330 / 348>
2. STARTING STATE
Model: MOD-EDE-N3; ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW PHYSICS.
Inherited: Q032 exact-TT matched endpoints; Q035 classifier discrepancy resolved; 
Q036 continuous geometry difference established.
Constraint: Artifact-only deterministic replay; same 7 coordinates/scales/threshold; 
no new likelihood/optimizer execution.
3. HYPOTHESES
H1: Exact matched TT support removes the geometry difference.
H2: Difference persists under matched TT support.
H3: Evidence is technically inconclusive.
Rejected: H1, H3.
Surviving: H2 — supported.
4. METHOD & EVIDENCE
Method: Compare 9 paired CamSpec/HiLLiPoP endpoints in normalized 7-D 
geometry; test matched displacement, centroid and pairwise-shape drift.
Evidence: Q032 authoritative endpoints, run 33994305721, commit 
”4dc873a5e880d40858d831a3b421456728f0c032”.
Program: ”q037_common_support_endpoint_geometry_v1.py” (”Q037-TTGEOM-V1”)
Workflow: ”.github/workflows/q037-common-support-endpoint-geometry-v1.yml”
<PARSED TEXT FOR PAGE: 331 / 348>
Tests: finite/replay, permutation invariance, common-support identity, locked-scale 
identity, threshold and preservation gates.
5. KEY RESULTS
Matched displacement: median 2.93179, max 5.22954, 9/9 >0.10.
Centroid displacement: 0.83115.
Pairwise drift: median 1.63679, max 4.75557, 36/36 >0.10.
Replay max absolute difference: 0.0; FINAL_RESULT_GATE: PASS.
Final result: The material CamSpec–HiLLiPoP geometry difference persists on exact 
matched TT support.
Limitation: No causal implementation component identified; shared Planck 
PR4/NPIPE data are not independent observations.
Contradiction: None; Q037 narrows Q036.
6. NEGATIVE RESULTS / MIKAMI
Failed scientific attempts: None recorded. Earlier repository-registration 403 was 
technical and later superseded.
Graveyard: “Unequal TT support is sufficient/primary explanation” — rejected for 
the tested bridge because the difference survives exact common support.
7. MODEL CHANGE
Before: C-036-IMPL active; TT-support mismatch remained plausible.
After: C-036-IMPL strengthened; tested TT-support mismatch weakened as primary 
cause.
<PARSED TEXT FOR PAGE: 332 / 348>
Change: CONSTRAINED.
Reason: 9/9 matched and 36/36 pairwise differences remain material.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commits: ”9ff5f29d6ae1f5f5f702ccb98e034fb1075326ba”; 
”c49d9885a5bf1e290f4b42f15c59d228c7c036cf”
Result: ”R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001”; ”q037_final_v1.json”
GitHub scientific run ID: NOT RECORDED.
Provenance: Deterministic replay of Q032 validated endpoints; no new physics 
execution.
9. REPRODUCIBILITY
Checkout recorded commits obtain Q032 artifacts run Q037 workflow/program → →
→ → compare with ”q037_final_v1.json” require same locked geometry and 0.10 
criterion plus FINAL_RESULT_GATE PASS.
10.CONCLUSION
Exact matching of TT information support does not remove the CamSpec–HiLLiPoP 
endpoint-geometry difference. This strengthens an unresolved implementation￾level discrepancy but establishes no physical Planck systematic, EDE 
detection/falsification, H₀ change or new physics.
11.NEXT-Q HANDOFF
<PARSED TEXT FOR PAGE: 333 / 348>
Next Q: Q038
Question: Is the surviving common-support geometry difference concentrated in a 
reproducible minimal subset of the seven coordinates, or distributed across several 
coordinates?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: YES — the material geometry difference persists under exact 
matched TT support.
Q-JOURNAL: This record.
MIKAMI: TT-support mismatch rejected as sufficient/primary explanation for the 
tested discrepancy.
MODEL CHANGE: C-036-IMPL strengthened/constrained; cause unresolved.
REPRODUCIBILITY: Q032 run 33994305721 + Q037 program/workflow/commits 
above.
NEXT-Q: Q038 — coordinate localization.
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q038
<PARSED TEXT FOR PAGE: 334 / 348>
Date/time: 2026-09-07 13:48 CEST
Status: CONFIRMED
Question: When Q037’s paired CamSpec/HiLLiPoP exact-common-support endpoints
are decomposed coordinate-by-coordinate under the seven Q031 locked scales, is 
the surviving implementation-geometry difference concentrated in a reproducible 
minimal subset or distributed across several coordinates?
2. STARTING STATE
Model: MOD-EDE-N3; n_{\rm scf}=3; ACTIVE / CONSTRAINED / NOT ESTABLISHED
NEW PHYSICS. Frozen ”mwt5345/class_ede” commit ”5a131c91…”.
Inherited: Q035 removed classifier semantics as a valid geometry discriminator; 
Q036 established a material continuous implementation difference; Q037 showed 
exact TT common support does not remove it.
Constraints: Same seven Q031 coordinates/scales; no new 
likelihood/CLASS/optimizer/sampler runs; no cross-likelihood objective arithmetic; 
causal attribution forbidden.
3. HYPOTHESES
Tested:
H1: discrepancy concentrated in 2 coordinates. ≤
H2: discrepancy distributed across 3 coordinates. ≥
H3: apparent localization fails robustness tests.
<PARSED TEXT FOR PAGE: 335 / 348>
Rejected: H1 — no 1-, 2-, or 3-coordinate subset met the preregistered joint criterion.
Surviving: H2 — distributed multivariate geometry.
4. METHOD & EVIDENCE
Deterministic artifact-only decomposition of validated Q037 endpoints. All 127 non￾empty subsets tested in matched-location, centroid and pairwise-shape channels; 
full capture 0.80; leave-one-label-out 0.70 with 8/9 passes. ≥ ≥ ≥
Primary evidence: Q032/Q037 endpoint artifacts; CamSpec/HiLLiPoP Planck 
PR4/NPIPE methodology (K-044, K-049; comparison K-045/K-052).
Program/workflow: ”q038_coordinate_localization_v1.py”; ”.github/workflows/q038-
coordinate-localization-v1.yml”.
GitHub run: ”34121000822”; head ”02ddda7c13a53cd7ad20880bf527a86e17ac4d79”.
5. KEY RESULTS
Minimal qualifying subset size: 4
Unique subset: \omega_b,\omega_{\rm cdm},f_{\rm EDE},\theta_{i,\rm scf}
Capture: 90.89% matched / 88.48% centroid / 87.20% pairwise-shape.
LOO robustness: 9/9 in all three channels.
FINAL_RESULT_GATE: PASS.
<PARSED TEXT FOR PAGE: 336 / 348>
Final result: The surviving CamSpec/HiLLiPoP implementation-geometry difference 
is DISTRIBUTED, not concentrated in one or two common coordinates.
Limitations: Parameter-space localization is not causal attribution; 
CamSpec/HiLLiPoP are not independent observations; no H₀ benchmark or EDE 
viability conclusion changes.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed routes: Single-coordinate, H₀-only, A_{\rm Planck}-only and two-coordinate
concentration explanations are insufficient under the frozen criterion.
Mikami Graveyard:
- 2-coordinate concentration — rejected. ≤
- Simple H₀-only / A_{\rm Planck}-only explanation — weakened.
 Reason: neither appears in the unique minimal robust explanation of the complete
geometry.
7. MODEL CHANGE
Before: C-036-IMPL = material implementation-dependent geometry difference; 
cause unresolved.
After: C-036-IMPL = material, exact-common-support-surviving, distributed 
multivariate geometry difference; cause unresolved.
<PARSED TEXT FOR PAGE: 337 / 348>
Change: PRÆCISERET / CONSTRAINED.
MOD-EDE-N3 status: unchanged.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Parent Q037 run: ”34115280043”, head ”c49d9885…”
Q038 run: ”34121000822”, head ”02ddda7c…”
Program: ”q038_coordinate_localization_v1.py”
Workflow: ”.github/workflows/q038-coordinate-localization-v1.yml”
Result: ”R-Q038-EDE-COORDINATE-LOCALIZATION-001”
Provenance: deterministic reanalysis of validated Q037/Q032 endpoint lineage; no 
new observational data or likelihood execution.
9. REPRODUCIBILITY
Checkout recorded commits obtain Q037 endpoint artifact run Q038 → →
program/workflow with locked Q031 scales and preregistered thresholds verify →
subset captures/LOO tests require FINAL_RESULT_GATE PASS and classification →
replay.
10.CONCLUSION
Q038 establishes that the surviving CamSpec/HiLLiPoP implementation difference is
genuinely multivariate under the tested geometry. At least four common 
coordinates are required for a robust compact representation. The calculation 
<PARSED TEXT FOR PAGE: 338 / 348>
narrows the methodological problem but does not identify which likelihood 
implementation component causes it.
11.NEXT-Q HANDOFF
Why: Causal implementation source remains unresolved.
Next Q: Q039
Question: Can a controlled matched intervention isolate one implementation block 
as sufficient to explain/reduce C-036-IMPL, or are coupled implementation changes 
required?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: DISTRIBUTED; unique minimal robust subset = \omega_b+
\omega_{\rm cdm}+f_{\rm EDE}+\theta_{i,\rm scf}.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: 2-coordinate concentration rejected; simple ≤
H₀/A_{\rm Planck}-only narratives weakened.
MODEL CHANGE SUMMARY: C-036-IMPL refined to distributed multivariate 
geometry; MOD-EDE-N3 unchanged.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; runs ”34115280043”, 
”34121000822”; Q038 workflow/program above.
NEXT-Q HANDOFF: Q039 — causal implementation-block attribution.
BUBBLEVERSE — Q-JOURNAL
<PARSED TEXT FOR PAGE: 339 / 348>
1. IDENTITY
Q-ID: Q039
Date/time: 2026-09-08 20:46 CEST
Status: INCONCLUSIVE
Question: When CamSpec and HiLLiPoP on Q032 exact TT common support are 
investigated with preregistered, native-parameter-respecting matched interventions
in their implementation blocks, can one single implementation block materially 
explain/reduce the Q037/Q038 distributed common-geometry difference, or are 
coupled changes across multiple blocks required?
2. STARTING STATE
Model: MOD-EDE-N3, n_{\rm scf}=3, ACTIVE / CONSTRAINED / NOT ESTABLISHED 
NEW PHYSICS.
Inherited: Q037 common-support discrepancy: matched 2.93179, centroid 0.83115, 
pairwise 1.63679. Q038: discrepancy DISTRIBUTED; minimal robust subset 
\omega_b,\omega_{\rm cdm},f_{\rm EDE},\theta_{i,\rm scf}.
Constraints: Frozen Q032 TT support/backend/scales; threshold 0.10; no cross- ≤
likelihood objective comparison; native parameter semantics only.
3. HYPOTHESES
Tested:
H1 relative calibration explains discrepancy.
H2 off-diagonal precision coupling explains discrepancy.
<PARSED TEXT FOR PAGE: 340 / 348>
H3 calibration+precision explains discrepancy.
H4 native foreground profiling freedom explains discrepancy.
Rejected as sufficient: H1–H4; all remained far above threshold, 0/9 LOO sufficient.
Surviving: deeper coupled likelihood/data/foreground/covariance construction 
remains possible but unproven.
4. METHOD & EVIDENCE
Methods: Matched implementation interventions; BOBYQA reoptimization; full￾sample geometry + 9 leave-one-label-out tests.
Sources: Rosenberg et al. 2022, arXiv:2205.10869; Efstathiou & Gratton 2021, 
arXiv:1910.00483; Tristram et al. 2024, DOI 10.1051/0004-6361/202348015; Jense et al.
2026, arXiv:2510.09430; HiLLiPoP commit a09ddde3; Cobaya 3.5.6.
5. KEY RESULTS
Calibration: 2.84864 / 0.87392 / 1.48583.
Precision: 2.60701 / 0.84119 / ~1.62217.
Calibration+precision: 3.07861 / 1.19445 / 1.87403.
Foreground-profile: 2.98293 / 1.05547 / 1.63532, LOO sufficient 0/9.
Final result: No tested scientifically matchable single block explains C-036-IMPL. 
Deeper coupled construction remains unresolved.
<PARSED TEXT FOR PAGE: 341 / 348>
Limitations: Full foreground/core-likelihood harmonization cannot be isolated as a 
clean native single-block intervention. No physical systematic or new physics 
established.
6. NEGATIVE RESULTS / MIKAMI
Failed technical attempts: Q039 V1–V4 and early FGPROFILE launcher/static 
failures; workflow/infrastructure only, no scientific evidence.
Graveyard: calibration-only, precision-only, calibration+precision, native 
foreground-profile freedom as sufficient explanations. Synthetic cross-likelihood 
nuisance/core hybrids rejected as scientifically invalid designs.
7. MODEL CHANGE
Before: C-036-IMPL active with several possible isolated implementation causes.
After: C-036-IMPL remains active, but single-block explanation space is strongly 
narrowed.
Change: CONSTRAINED.
Reason: validated negative Q039 interventions.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Backend: class_ede ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”
Q032: run 33994305721, commit ”4dc873a5e880d40858d831a3b421456728f0c032”
<PARSED TEXT FOR PAGE: 342 / 348>
Q039 V5: run 34161368438, commit 
”365217d4a4ca21e0af3b296c0e6b23df7e07ba60”, workflow ”q039-implementation￾block-intervention-v5.yml”
FGPROFILE: run 34184346582, commit 
”449fe096e49a793446c0c859cf8caf0fcdaf4c8f”, workflow ”q039-native-foreground￾profile-v1.yml”
Results: R-Q039-EDE-IMPLEMENTATION-BLOCK-INTERVENTION-001; R-Q039-EDE￾NATIVE-FOREGROUND-PROFILE-001. FINAL_RESULT_GATE PASS.
9. REPRODUCIBILITY
Checkout recorded commits obtain frozen Q032 endpoints/support run → →
recorded workflows with frozen parameters reproduce geometry/LOO outputs → →
apply 0.10 sufficiency criterion. ≤
10.CONCLUSION
Q039 closes INCONCLUSIVE but strongly constraining. The CamSpec–HiLLiPoP 
discrepancy survives all scientifically clean tested single-block interventions. Its 
remaining cause lies, if identifiable, in deeper coupled implementation structure. 
This is methodological evidence only.
11.NEXT-Q HANDOFF
Next Q: Q040
Why: determine whether a finite, scientifically defensible coupled structural 
intervention can explain C-036-IMPL without constructing a meaningless synthetic 
likelihood.
<PARSED TEXT FOR PAGE: 343 / 348>
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No tested clean single implementation block is sufficient; coupled 
deeper structure remains unresolved.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Calibration, precision, calibration+precision and 
native foreground-profile freedom killed as sufficient explanations.
MODEL CHANGE SUMMARY: C-036-IMPL retained but substantially constrained.
REPRODUCIBILITY / GITHUB: Runs 34161368438 and 34184346582; commits and 
workflows above.
NEXT-Q HANDOFF: Q040 — test whether a scientifically valid coupled structural 
bridge can be defined.
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q040
Date/time: 2026-09-08 22:47 CEST
Status: INCONCLUSIVE
Question: Can a finite, preregistered and scientifically defensible coupled structural 
intervention involving documented CamSpec-versus-HiLLiPoP differences in 
foreground-model form, data-vector construction/weighting and 
covariance/likelihood construction materially reduce C-036-IMPL on the Q032 
<PARSED TEXT FOR PAGE: 344 / 348>
matched-support architecture without constructing a scientifically meaningless 
synthetic likelihood?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3 — ACTIVE / CONSTRAINED / NOT 
ESTABLISHED NEW PHYSICS.
Inherited: Q036–Q038 established reproducible, distributed CamSpec–HiLLiPoP 
geometry discrepancy; Q039 rejected calibration, precision coupling and native 
foreground profiling as sufficient explanations.
Constraints: Frozen Q032 TT support, 7D geometry, threshold 0.10; 
CamSpec/HiLLiPoP remain native separate likelihoods; no synthetic likelihood; 
A_planck explicit.
3. HYPOTHESES
Tested:
H1: Valid common-CMB latent representation exists.
H2: Single-Gaussian nuisance marginalization can support the test.
H3: Defensive non-Gaussian RQMC can produce validated endpoints.
Rejected: H2 — CamSpec boundary/non-PD Hessian and HiLLiPoP multistart 
instability.
Surviving: H1 mathematically supported; H3 numerically unresolved. C-036-DEEP￾STRUCTURAL remains active/unresolved.
<PARSED TEXT FOR PAGE: 345 / 348>
4. METHOD & EVIDENCE
Methods: Native nuisance marginalization; Laplace/Schur validation; defensive 
importance sampling + Owen-scrambled Sobol RQMC, 4 replicates, m=9–16.
Sources: K-044 CamSpec; K-049 HiLLiPoP; K-053/K-054 official implementations; 
K-055 boundary statistics; K-056 mixed Laplace; K-057 defensive importance 
sampling; K-058 RQMC.
Programs/workflows: ”q040_defensive_rqmc_v4.py”; ”.github/workflows/q040-
defensive-rqmc-v4.yml”; GitHub run 34258155387.
Tests: Frozen Δχ² convergence 0.05; Bank A/B 0.05; downstream science ≤ ≤
endpoints allowed only after validation.
5. KEY RESULTS
Single-Gaussian compression: COMPRESSION_VALIDATION_FAIL.
RQMC reached hard cap m=16 / 393,216 nodes per replicate/implementation.
CamSpec: transition 16.5899; Bank A/B 28.4438.
HiLLiPoP: transition 61.1260; Bank A/B 63.1116.
Required: 0.05. ≤
<PARSED TEXT FOR PAGE: 346 / 348>
Final result: ”DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL”.
Science endpoints, final geometry and 9/9 LOO were correctly blocked.
Limitation: No conclusion on whether a successfully validated structural bridge 
would reduce C-036-IMPL.
Contradictions: None; Q036–Q039 remain compatible.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: CMB-space V1–V3 technical failures; RQMC V1 serialization, V2 
GitHub artifact transport, V3 deployment failure. No physical evidence.
Graveyard additions: Single-Gaussian Laplace/Schur route killed for Q040 science; 
finite Q040 RQMC campaign killed as numerically validated bridge at frozen hard 
cap.
7. MODEL CHANGE
Before: C-036-IMPL active; deeper structural origin unresolved.
After: Same physical/model status, but deeper bridge is mathematically defined and 
tested numerical routes constrained.
Change: CONSTRAINED / REFINED.
Reason: Both Gaussian compression and finite defensive RQMC failed preregistered 
validation.
<PARSED TEXT FOR PAGE: 347 / 348>
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: 855a28c58246dbdd52d01cae1f40e0611103d96b
Workflow: ”.github/workflows/q040-defensive-rqmc-v4.yml”
Program: ”q040_defensive_rqmc_v4.py”
Result: R-Q040-EDE-DEFENSIVE-RQMC-CMB-MARGINAL-004
Artifacts: ”q040-rqmc-final-v4”; ”q040-rqmc-integration-final-v4”; ”q040-rqmc-state￾m16-v4”.
Provenance: Frozen Q032/Q037 architecture + native CamSpec/HiLLiPoP 
likelihoods; preregistered finite campaign completed through hard cap.
9. REPRODUCIBILITY
Checkout recorded commits; obtain Q032/Q037 parent artifacts and native 
likelihoods; run Q040-RQMC-V4 with frozen parameters; reproduce m9–m16 states; 
apply unchanged 0.05 validation gates and 0.10 science criterion.
10.CONCLUSION
A scientifically defensible common native-nuisance-marginalized CMB 
representation exists mathematically, but Q040 did not obtain a numerically 
validated implementation capable of testing whether it materially reduces C-036-
IMPL. The discrepancy therefore remains active and unexplained; no pipeline 
superiority, EDE confirmation/falsification or new physics is established.
11.NEXT-Q HANDOFF
<PARSED TEXT FOR PAGE: 348 / 348>
Why: The dominant source of RQMC instability remains unidentified.
Next Q: Q041
Question: Is Q040’s finite defensive-RQMC nonconvergence dominated by a small 
identifiable subset of nuisance dimensions, boundaries, proposal strata or 
likelihood-specific directions, or is it broadly distributed?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: INCONCLUSIVE — valid bridge definition exists, but finite 
numerical validation failed.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Gaussian compression and Q040 finite-RQMC science
route rejected under tested conditions.
MODEL CHANGE SUMMARY: Model unchanged; methodological space narrowed.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse, commit 855a28c…, run 
34258155387, Q040-RQMC-V4.
NEXT-Q HANDOFF: Q041 — localize the source of RQMC instability.



---

**Bilag D — BV-EXEC-README-001: automatisk README-vedligeholdelse**

Følgende er det fulde tillæg til den eksisterende execution engine. Det er en fremadrettet driftsregel, ikke et nyt Q041-resultat. Den komplette tekst medfølger, så næste motor modtager kravene sammen med Q, journal og proveniens.

# BUBBLEVERSE — EXECUTION ENGINE ADDENDUM

**ADDENDUM ID:** BV-EXEC-README-001  
**VERSION:** 1.0  
**DATE:** 2026-09-23  
**TARGET:** Existing Bubbleverse Numerical Execution / HPC Engine  
**PURPOSE:** Add mandatory repository README maintenance to the existing engine's workflow, deliverables, validation, response structure and stop criteria.

This is an additive instruction module for the existing engine. It is not a replacement execution engine and does not replace CURRENT Q, CASE ID, SAMLET JOURNAL, sources, provenance, scientific gates or the existing anti-loop rules.

Apply the requirements below when creating or changing repository functionality or preparing a repository update package for the user. Preserve the user's current authorization: do not write to GitHub or start GitHub workflows. When changes are prepared as files, include any actual README update in the same deliverable, validate it against the prepared file set and the inspected repository state, and describe the result as a prepared package, not an applied repository change. These documentation requirements do not grant permission to publish, push, commit remotely or dispatch workflows.

The mandatory PASS/FAIL gates below apply to repository modifications and prepared repository modification packages. Do not claim that a live repository was changed merely because a package was validated. Adding this instruction module alone does not establish that a repository README or repository consistency gate has passed.

---

ADD TO THE EXISTING BUBBLEVERSE EXECUTION ENGINE

AUTOMATIC REPOSITORY README MAINTENANCE

Whenever this engine creates, modifies, replaces, registers, supersedes, or removes Bubbleverse repository functionality, it must also inspect and update the repository README when the change affects information that a reader or operator should know.

The README is part of the repository deliverable.

A PROGRAM CHANGE IS NOT COMPLETE UNTIL THE README HAS BEEN CHECKED.

The engine must determine whether the repository currently contains:

README.md

or another canonical repository README.

If a canonical README exists:

UPDATE IT.

If no README exists and the repository needs one:

CREATE README.md.

Do not create competing duplicate README files without reason.

---

README PURPOSE

The README must provide a concise human-readable entry point to the repository.

It must explain the repository as it actually exists now.

It must not become a dump of:

- full journals
- giant numerical outputs
- complete source registries
- every debugging log
- obsolete workflow history
- internal implementation noise

Detailed scientific and technical material belongs in the appropriate repository files.

The README should function as:

REPOSITORY FRONT DOOR.

---

README MUST REFLECT CURRENT REPOSITORY STATE

Whenever relevant, maintain information about:

- repository purpose
- Bubbleverse project purpose
- current architecture
- major directories
- active execution system
- permanent Bubbleverse Start launcher
- PROGRAM_ID system
- how programs are started
- job splitting
- checkpoint / resume support
- result testing
- reproducibility
- provenance
- current supported or active Q range where appropriate
- important models/program groups
- where results live
- where journals live
- where source/provenance information lives
- where accepted/candidate model material lives when applicable
- contact information if already part of the repository specification

Do not claim features that do not actually exist in the repository.

---

README MUST BE UPDATED FROM REAL FILES

Before editing README.md:

1. inspect the existing README
2. inspect the current repository structure
3. inspect the files being added or modified
4. inspect the launcher
5. inspect the program registry
6. inspect relevant workflows
7. inspect relevant result/test structure
8. preserve useful existing README content
9. remove or correct obsolete descriptions
10. add only repository functionality that actually exists

Do not invent repository structure.

---

README UPDATE IS DIFFERENTIAL

Do not rewrite the entire README every time unless necessary.

Prefer:

KEEP
UPDATE
ADD
REMOVE
CORRECT

Preserve useful stable sections.

Update only what has materially changed.

---

PROGRAM CREATION MUST UPDATE README

Whenever a new runnable program is added, assess whether the README should expose it.

The README does not need a giant permanent catalogue of every historical program.

Prefer documenting:

- the permanent start mechanism
- how PROGRAM_ID works
- active or important executable campaigns
- where the complete registry can be found

Example:

## Running Bubbleverse

Open the GitHub Actions workflow:

🚀 BUBBLEVERSE START

Enter the PROGRAM_ID supplied by the current Bubbleverse execution package and press Run workflow.

Program routing is controlled by:

bubbleverse_program_registry.json

Adapt wording to the actual repository.

---

README MUST DOCUMENT THE PERMANENT START BUTTON

When the launcher exists, the README must clearly explain that the normal user-facing execution path is:

🚀 BUBBLEVERSE START
↓
ENTER PROGRAM_ID
↓
RUN WORKFLOW

The user should not need to search through the internal workflow list.

Document the actual launcher filename, normally:

.github/workflows/00-bubbleverse-start.yml

if that is the canonical implemented path.

---

README MUST DOCUMENT PROGRAM_ID

Explain briefly that:

PROGRAM_ID

identifies the exact registered executable Bubbleverse program/version.

Example:

Q041-PLANCKPORT-V3

The README should point to the canonical program registry rather than manually duplicating every registry field.

---

README MUST DOCUMENT JOB SPLITTING

When the repository supports automatic job splitting, state that long computations may be divided into:

- parallel shards
- sequential checkpointed segments
- test shards
- merge jobs

to avoid unsafe single-job runtimes.

Do not hardcode a GitHub runtime limit in README unless there is a specific reason and the value is maintained against current official rules.

Prefer wording such as:

«Long computations are automatically partitioned into safe GitHub Actions jobs when a single job is not expected to complete with sufficient runtime margin.»

---

README MUST DOCUMENT CHECKPOINT / RESUME

If implemented, explain that long stateful executions can:

RUN
→ CHECKPOINT
→ CONTINUE IN NEXT JOB

and that checkpoints preserve Q/run provenance.

Do not claim resume support unless the actual workflow implements true continuation.

---

README MUST DOCUMENT RESULT VALIDATION

The README should make clear that:

PROGRAM COMPLETION IS NOT AUTOMATICALLY SCIENTIFIC VALIDATION.

Where implemented, describe the basic chain:

EXECUTION
↓
COMPLETENESS
↓
MERGE
↓
REQUIRED RESULT TESTS
↓
FINAL RESULT GATE

Keep detailed test definitions outside the README.

---

README MUST PRESERVE Q CONTEXT

When describing current executable scientific work, preserve the correct Q identity.

Do not describe a Q-specific program without its Q association.

Example:

Q041 — Downstream scientific-consequence portability...

when relevant.

Do not silently relabel Qs.

---

README MUST NOT REPLACE THE JOURNAL

README.md is not SAMLET JOURNAL.

The README may explain where journals live and what they are for.

It must not become the authoritative scientific memory.

The authoritative scientific state remains the Bubbleverse journal system.

---

README MUST NOT REPLACE SOURCE REGISTRY

README may describe provenance architecture and link internally to relevant repository locations.

Do not copy the complete source registry into README without a concrete reason.

---

README MUST FOLLOW REPOSITORY CLEANUP

If files are:

- superseded
- renamed
- moved
- removed
- canonicalized

README references must be checked.

Broken links or references must be corrected.

---

README MUST FOLLOW VERSION CHANGES

If README explicitly mentions an active version or PROGRAM_ID that is replaced:

Q041-PLANCKPORT-V3
→
Q041-PLANCKPORT-V4

update the README when appropriate.

Do not leave the front page pointing users toward an obsolete executable.

Historical versions remain in provenance or registry as appropriate.

---

README MUST FOLLOW LAUNCHER CHANGES

If:

00-bubbleverse-start.yml

is patched or its interface changes, inspect README instructions immediately.

README execution instructions must match the real launcher.

---

README MUST FOLLOW REGISTRY CHANGES

If the canonical program registry path changes, update README.

Example:

OLD:
programs.json

NEW:
bubbleverse_program_registry.json

Do not leave stale documentation.

---

README VALIDATION

Before completing repository modification, verify:

README exists if required?
README reflects current architecture?
Launcher path correct?
Registry path correct?
PROGRAM_ID instructions correct?
Important file references valid?
No removed files still referenced?
No obsolete active program documented?
No invented features?
Markdown structure valid?

Then report:

README_GATE = PASS

or:

README_GATE = FAIL

---

README PROVENANCE

Treat README changes as part of the same repository modification.

Where repository modifications are actually performed, README changes should be committed together with the functionality they document when practical.

Example conceptual change:

Q041 program
+
workflow
+
registry entry
+
launcher compatibility
+
README update
=
ONE COHERENT REPOSITORY UPDATE

---

FILE DECISION OUTPUT MUST INCLUDE README

The engine's file-decision section must now always consider:

README.md

and classify it as:

UNCHANGED
UPDATE
CREATE

Example:

FILE:
README.md

ACTION:
UPDATE

REASON:
Added permanent Bubbleverse Start / PROGRAM_ID execution instructions.

---

REQUIRED REPOSITORY MODIFICATION SEQUENCE

When code is created or modified, use:

SEARCH REPOSITORY
↓
PRESERVE Q + JOURNAL + SOURCES
↓
REUSE / PATCH / BUILD
↓
CREATE PROGRAM
↓
CREATE / UPDATE WORKFLOW
↓
ASSIGN PROGRAM_ID
↓
UPDATE PROGRAM REGISTRY
↓
VALIDATE BUBBLEVERSE START
↓
DESIGN SAFE JOB SPLITTING
↓
CREATE CHECKPOINT / MERGE / TEST SYSTEM
↓
INSPECT README
↓
UPDATE README IF REQUIRED
↓
VALIDATE README
↓
FINAL REPOSITORY CONSISTENCY CHECK

---

REPOSITORY CONSISTENCY GATE

Before declaring repository work complete, verify that these components agree where applicable:

Q
PROGRAM_ID
PROGRAM
CONFIG
WORKFLOW
PROGRAM REGISTRY
BUBBLEVERSE START
JOB STRUCTURE
CHECKPOINT SYSTEM
RESULT TESTS
README

If they disagree:

REPOSITORY_CONSISTENCY_GATE = FAIL

Do not declare the repository update complete.

---

ADD TO STOP CRITERIA

The engine is not finished until:

1. README.md has been inspected
2. README has been updated if repository-facing information changed
3. obsolete README references have been corrected
4. the permanent launcher is documented correctly
5. PROGRAM_ID usage is documented correctly
6. relevant job-splitting behavior is documented correctly
7. result-validation architecture is documented correctly where applicable
8. README matches actual repository structure
9. README_GATE has been evaluated
10. REPOSITORY_CONSISTENCY_GATE has been evaluated

---

ADD TO REQUIRED RESPONSE STRUCTURE

README STATUS

Always include for repository modifications:

README:

ACTION:
UNCHANGED / UPDATE / CREATE

FILE:
README.md

REASON:
<reason>

README_GATE:
PASS / FAIL

If README was modified and actual file creation is available:

DELIVER OR APPLY THE ACTUAL README UPDATE.

Do not merely recommend that somebody update it later.

---

UPDATED ABSOLUTE REPOSITORY RULE

Whenever this engine modifies the Bubbleverse repository:

CHECK README.

If the repository's public or operator-facing reality changed:

UPDATE README.

The repository must not contain one architecture while README describes another.

Therefore a complete computational implementation is:

Q + JOURNAL + SOURCES
↓
PROGRAM / MOTOR
↓
PROGRAM_ID
↓
REGISTRY
↓
🚀 BUBBLEVERSE START
↓
SAFE JOB STRUCTURE
↓
CHECKPOINT / MERGE
↓
RESULT TESTS
↓
README UPDATE
↓
CONSISTENCY VALIDATION
↓
RETURN TO BUBBLEVERSE

CODE AND DOCUMENTATION MUST MOVE TOGETHER.


---

# APPENDIX B — COMPLETE Q042 V11 TECHNICAL-HISTORY SOURCE LOCK

```json
{
  "case_id": "NOT DOCUMENTED",
  "external": {
    "act_dr6_lensing": {
      "commit": "b386ddbb5821c1216c709f051c9289292f174d30",
      "component": "act_dr6_lenslike.ACTDR6LensLike",
      "repository": "ACTCollaboration/act_dr6_lenslike",
      "tag": "v1.2.1"
    },
    "act_dr6_primary": {
      "commit": "880eacb40d66722eb1c32d7b5621e91662b4d808",
      "component": "act_dr6_cmbonly.ACTDR6CMBonly",
      "ell_min": 600,
      "repository": "ACTCollaboration/DR6-ACT-lite",
      "tag": "v1.0.1"
    },
    "desi_dr2": {
      "bao_data_commit": "b7b8a36e9bccb063081f811f323cada21ab5fbdd",
      "bao_data_tag": "v2.6",
      "cobaya_definition_commit": "b76b6fed2a6c8c5594c6f92d5058bef10079746a",
      "component": "bao.desi_dr2"
    },
    "supernova": {
      "component": "sn.pantheonplus",
      "reference_q014_github_run_id": 33597153303,
      "reference_q014_result_id": "R-Q014-EDE-EXTERNAL-VIABILITY-009",
      "runtime_file_hash_manifest_required": true,
      "selection_status": "PROSPECTIVELY_FROZEN_FOR_Q042_BEFORE_Q042_SCIENCE_RESULTS"
    }
  },
  "forbidden_operations": [
    "hybrid CamSpec/HiLLiPoP likelihood",
    "cross-arm absolute chi2/objective subtraction as physical evidence",
    "promotion of unconverged V19 chains to science",
    "retroactive threshold changes",
    "automatic fallback to V19 MCMC"
  ],
  "forbidden_scientific_inputs": [
    "Q040-CMBSPACE-*",
    "Q040-RQMC-*"
  ],
  "github_mutation": "FORBIDDEN_BY_USER; GitHub may be read for technical memory, but all Q042-V11 files are delivered for manual upload only",
  "historical_parent": {
    "q041_v19_attempt": 4,
    "q041_v19_execution_commit": "a962ba70077422f8b69642dea4e8272e1d00e5ff",
    "q041_v19_program_id": "Q041-PLANCKPORT-V19",
    "q041_v19_result_id": "R-Q041-EDE-DOWNSTREAM-PORTABILITY-019",
    "q041_v19_run_id": 34979609004,
    "q042_v1_decision": "REJECT_MORE_OF_SAME_MCMC__SELECT_POLYCHORD_PLUS_MULTISTART_BOBYQA",
    "q042_v1_preregister_sha256": "5243a0b385285aa70294a14842c39789a69273eb1d1dbc52257025c3f4e8f332",
    "q042_v1_program_id": "Q042-EXECMECH-V1",
    "q042_v1_result_id": "R-Q042-EXECUTION-MECHANISM-DIAGNOSTIC-001"
  },
  "known_good_v19_runtime_provenance": {
    "environment_artifact_digest": "sha256:a160b8ca6011cf1808bfd0644925a2ba554a0db668ec743df9733c592543ab80",
    "environment_artifact_id": 10401161073,
    "environment_artifact_name": "q041-environment-v19",
    "execution_commit": "a962ba70077422f8b69642dea4e8272e1d00e5ff",
    "github_run_id": 34979609004,
    "historical_cache_key": "q041-v19-${{ runner.os }}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36",
    "role": "KNOWN_GOOD_BASE_RUNTIME_CACHE_IDENTITY_ONLY; no Q041 V19 posterior chain state is reused as Q042 science."
  },
  "known_method_risks": {
    "polychord_2026_open_issue": "PolyChordLite issue #139 reports a hang after live generation for a multi-survey Python log-likelihood in some circumstances. Q042-V3 therefore uses bounded real-stack pilots with job timeouts; no patch is assumed valid in advance.",
    "polychord_v2_build_failure": "Q042-PREFLIGHT-V2 installed gfortran/gcc/g++/make but not an OpenMPI development toolchain. PolyChordLite setup.py defaults to MPI=1 and invokes make -e libchord.so; V3 supplies and gates the missing MPI compiler/header/library prerequisites. This is a technical deployment repair only.",
    "pybobyqa_bubbleverse_history": "Earlier Bubbleverse optimization runs recorded singular interpolation matrices and duplicate restart architecture. Q042-V3 uses best_of=1 and external preregistered starts.",
    "q042_v10_merge_dependency_failure": "Fresh GitHub-hosted jobs do not inherit Python packages from prior jobs; merge-preflight must explicitly bootstrap NumPy/PyYAML even though it only merges technical artifacts.",
    "q042_v3_cache_failure": "V3 failed before PolyChord/Q042 runtime because the inherited Q041 helper used three 10-second NERSC availability probes on a cold cache. No scientific result exists from V3.",
    "q042_v4_identity_gate_failure": "V4 gate compared all non-Planck likelihood keys, which included native q019_shape_* versus q031_shape_* arm-specific nuisance/shape terms. V5 limits cross-arm identity to contracted external science blocks A6/L6/D2/SN and the common ACT calibration contract.",
    "q042_v6_pilot_timeout": "V6 reached real PolyChord execution for the camspec EDE FULL pilot but the technical pilot did not finish within the 330-minute GitHub job budget. The cancellation is a runtime-budget failure, not a scientific or sampler-validity result.",
    "q042_v7_hillipop_resume_info_failure": "A V7 hillipop-ede pilot completed fresh PolyChord sampling but Cobaya rejected same-process resume because regenerated planck_2020_hillipop.TT resolved info differed from stored updated info. V9 resumes from Cobaya stored updated info after reinstalling the frozen runtime patch.",
    "q042_v7_mpi_resume_failure": "A V7 camspec-ede pilot completed the bounded PolyChord fresh smoke run and wrote resume state, but a second PolyChord invocation in the same Python process aborted when MPI_Comm_dup was called after MPI_FINALIZE. V8/V9 preserve the repair of one fresh interpreter/MPI lifecycle per PolyChord invocation.",
    "q042_v9_bobyqa_wrapper_false_failure": "V9 showed that Cobaya 3.5.6 raises LoggedError when Py-BOBYQA reaches maxfun even though Q042 preregistration explicitly accepts a finite objective with non-negative Py-BOBYQA flag, including EXIT_MAXFUN_WARNING. V11 harvests the raw result from that wrapper exception and applies the frozen Q042 acceptance rule.",
    "v4_transport_policy": "V4 first attempts the exact Q041 V19 base cache. On cold cache it keeps the same official planck_2020_hillipop.TT component/data source and exact Q032 setup, changing only the retry envelope: no preliminary range probe; 3 bounded real installs of at most 1800 seconds each."
  },
  "program_id": "Q042-PREFLIGHT-V11",
  "q": "Q-042",
  "q032_parent": {
    "execution_commit": "4dc873a5e880d40858d831a3b421456728f0c032",
    "github_run_id": 33994305721,
    "result_id": "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
  },
  "q041_v20_role": "REFERENCE_ONLY_UNEXECUTED; code concepts may be reused but it is not scientific evidence",
  "result_id": "R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-011",
  "run_id": "Q042-POLYCHORD-BOBYQA-PREFLIGHT-V11",
  "software": {
    "class_ede_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "class_ede_repository": "mwt5345/class_ede",
    "cobaya_version": "3.5.6",
    "cold_cache_hillipop_transport": "same official planck_2020_hillipop.TT v4.2 source via frozen q032_setup_v2.sh; only retry wrapper changed to 3 x timeout 1800s; no short NERSC availability probe",
    "hillipop_commit": "a09ddde3e7ce11df99f74685feb1f1764cafb251",
    "numpy_version": "1.26.4",
    "openmpi_runtime": "Ubuntu packages openmpi-bin + libopenmpi-dev; exact package versions recorded at runtime with dpkg-query",
    "poly_build_isolation": "pip --no-build-isolation --no-deps after explicit make -e libchord.so MPI=1 gate",
    "polychord_build_mode": "MPI=1 (PolyChordLite setup.py default)",
    "polychordlite_exact_commit": "MUST_BE_RESOLVED_AND_RECORDED_BY_PREFLIGHT_BEFORE_ANY_POLYCHORD_PILOT",
    "polychordlite_release_tag": "1.22.2",
    "polychordlite_repository": "PolyChord/PolyChordLite",
    "pybobyqa_version": "1.5.0",
    "python_version": "3.11",
    "q041_v19_base_cache_key": "q041-v19-${runner.os}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36",
    "v19_base_cache_key": "q041-v19-${{ runner.os }}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36",
    "v19_base_cache_policy": "EXACT_PATH_LIST_AND_KEY_FAIL_ON_MISS",
    "v4_environment_cache_key": "q042-v4-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus",
    "v4_environment_cache_role": "KNOWN_GOOD_RUNTIME_BASE_FOR_V5; V4 reached real likelihood initialization before a local metadata gate failed.",
    "v7_environment_cache_key": "q042-v7-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus",
    "v7_environment_cache_role": "KNOWN_GOOD_RUNTIME_BASE_FOR_V9; V7 environment and initial bounded PolyChord smoke executed successfully before the same-process resume MPI lifecycle failure."
  },
  "spec_sha256": "183139bf7bab9dcf1bf0e591762dbb1ddb4160244065a400709e2522d3241ebe",
  "technical_parent": {
    "failure_class": "MERGE_PREFLIGHT_FRESH_RUNNER_MISSING_NUMPY_DEPENDENCY",
    "failure_detail": "merge-preflight failed before merge logic at import numpy as np with ModuleNotFoundError because the fresh runner had actions/setup-python but no pip dependency install.",
    "program_id": "Q042-PREFLIGHT-V10",
    "scientific_result": "NONE",
    "status": "TECHNICAL_FAILURE_IN_MERGE_PREFLIGHT"
  },
  "technical_repairs": {
    "q042_v7_pilot_budget_repair": "Only the pre-science PolyChord smoke/resume pilot budget is reduced to nlive=1d, num_repeats=4, nprior=nlive and max_ndead=2. Production PolyChord and all BOBYQA settings are unchanged. V7 also corrects registry metadata so frozen_core_helper points to q042_prepare_frozen_core_v4.sh.",
    "v11_bobyqa_bounded_warning_harvest": {
      "bobyqa_settings_changed": false,
      "cobaya_wrapper_behavior": "Cobaya 3.5.6 only counts Py-BOBYQA EXIT_SUCCESS as minimizer success and raises if all bounded starts return warnings",
      "negative_flags": "rejected",
      "polychord_settings_changed": false,
      "production_settings_changed": false,
      "q042_gate": "finite objective AND raw Py-BOBYQA flag >= 0; Exit flag 1 / MAXFUN accepted exactly as preregistered",
      "science_changed": false,
      "unparsed_or_unrelated_exceptions": "rejected"
    },
    "v11_merge_dependency_bootstrap": {
      "bobyqa_settings_changed": false,
      "merge_job_dependencies": [
        "numpy==1.26.4",
        "PyYAML==6.0.2"
      ],
      "polychord_settings_changed": false,
      "production_settings_changed": false,
      "program_logic_changed": false,
      "scientific_settings_changed": false,
      "scope": "WORKFLOW_BOOTSTRAP_ONLY"
    },
    "v8_process_isolation": {
      "bobyqa_external_starts": "one fresh Python interpreter per external start",
      "polychord_fresh": "fresh Python interpreter/MPI lifecycle",
      "polychord_resume": "separate fresh Python interpreter/MPI lifecycle, same output prefix and resume file",
      "sampler_settings_changed": false,
      "science_changed": false
    },
    "v9_stored_resume_info": {
      "allow_changes": false,
      "bobyqa_settings_changed": false,
      "polychord_resume": "fresh Python/MPI lifecycle; reinstall runtime patch, then resume from Cobaya OutputReadOnly stored updated info",
      "production_settings_changed": false,
      "scientific_settings_changed": false
    }
  }
}
```

---

# APPENDIX C — COMPLETE FROZEN PRODUCTION SPECIFICATION AND SOURCE LOCK

## q042_production_spec_v1.json

```json
{
  "analysis_preregister": {
    "bobyqa_chi2": "best_chi2 = 2 * minimum finite Py-BOBYQA objective because Cobaya minimize(ignore_prior=True) minimizes -log(likelihood)",
    "globality": "all four external starts must be present; negative/missing results are preserved; at least one finite non-negative result per cell is required for a usable best fit",
    "material_count_coordinates": [
      "H0",
      "fEDE",
      "omega_b",
      "omega_cdm"
    ],
    "no_cross_arm_absolute_objective": true,
    "no_pilot_science": true,
    "no_q040_endpoints": true,
    "overlap_method": "weighted 2D histogram overlap coefficient sum(min(Pij,Qij)) on common frozen-prior bounds in (H0,fEDE)",
    "overlap_primary_bins": [
      80,
      80
    ],
    "overlap_stability_bins": [
      [
        64,
        64
      ],
      [
        96,
        96
      ]
    ],
    "overlap_stability_rule": "if primary and either stability grid fall on different sides of 0.50, contour geometry is UNRESOLVED_NUMERICAL_BINNING and no final scientific class may be emitted",
    "parameter_location_coordinates": [
      "H0",
      "fEDE",
      "omega_b",
      "omega_cdm",
      "log10z_c",
      "thetai_scf"
    ],
    "posterior_summary": "weighted mean and weighted population standard deviation from final nested-sampling weighted samples",
    "primary_geometry_model": "ede_n3",
    "weak_identification_guard": "log10z_c and thetai_scf are reported but never allowed by themselves to trigger parameter-location materiality; conservative implementation of the frozen weak-identification rule."
  },
  "authoritative_contract": {
    "arms": [
      "camspec",
      "hillipop"
    ],
    "data_combinations": {
      "FULL": [
        "P",
        "A6",
        "L6",
        "D2",
        "SN"
      ],
      "NO_ACT_LENSING": [
        "P",
        "A6",
        "D2",
        "SN"
      ],
      "NO_ACT_PRIMARY": [
        "P",
        "L6",
        "D2",
        "SN"
      ],
      "NO_DESI_DR2": [
        "P",
        "A6",
        "L6",
        "SN"
      ],
      "NO_SN": [
        "P",
        "A6",
        "L6",
        "D2"
      ]
    },
    "models": [
      "lcdm",
      "ede_n3"
    ],
    "no_cross_arm_absolute_chi2_evidence": true,
    "no_hybrid_planck_likelihood": true,
    "q040_scientific_endpoints_forbidden": true,
    "reporting_coordinates": [
      "H0",
      "fEDE",
      "log10z_c",
      "thetai_scf",
      "omega_b",
      "omega_cdm"
    ],
    "required_cell_count": 20,
    "same_external_data_both_planck_arms": true
  },
  "bobyqa_production": {
    "cobaya_best_of": 1,
    "external_starts_per_cell": 4,
    "globality_gate": "within each arm/model/data cell, retain the best finite likelihood minimum only after all four external starts complete; negative Py-BOBYQA linear-algebra/input flags fail that start and must be preserved",
    "ignore_prior": true,
    "max_evals": "120d",
    "rhoend": 0.05,
    "start_rule": "start 0 = frozen Q032 parent reference; starts 1-3 = deterministic bounded signed perturbations of sampled coordinates using 0.08, 0.14 and 0.20 of each finite prior span, clipped 5 percent inside hard bounds; EDE sector remains n=3; no internal multi-start layer"
  },
  "case_id": "NOT DOCUMENTED",
  "controlled_nonresult_classes": [
    "CONTROLLED_NO_SCIENTIFIC_RESULT",
    "PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED"
  ],
  "created_date": "2026-09-25",
  "final_classes": [
    "MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE",
    "SCIENTIFIC_DIFFERENCE_COLLAPSES",
    "MIXED_DATASET_CONDITIONAL"
  ],
  "orchestration": {
    "artifact_campaign_namespace": "root GitHub run id",
    "bobyqa_atomicity": "one external start per job; optimizer settings are not split or altered",
    "collector_checks_per_run": 5,
    "collector_sleep_minutes": 45,
    "github_hosted_job_hard_limit_minutes": 360,
    "github_job_limit_source": "https://docs.github.com/en/actions/reference/limits",
    "github_limits_verified_date": "2026-09-25",
    "github_workflow_run_limit_days": 35,
    "job_timeout_minutes": 330,
    "max_collector_rounds": 80,
    "max_polychord_segments_per_cell": 48,
    "segment_behavior": "fresh segment 0; later segments resume exact transferred Cobaya/PolyChord state in a fresh interpreter/MPI lifecycle",
    "soft_polychord_segment_minutes": 240
  },
  "original_decision_rule": {
    "combination_materiality": "material if model-preference portability is material OR both parameter-location and contour geometry are material",
    "contour_overlap": {
      "coordinates": [
        "H0",
        "fEDE"
      ],
      "material_if": "overlap_coefficient<0.50",
      "method": "empirical weighted two-dimensional posterior/profile overlap; no Gaussian compression",
      "substantial_if": "overlap_coefficient>=0.50"
    },
    "final_classification": {
      "MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE": "FULL material AND materiality survives every required valid leave-one-out test",
      "MIXED_DATASET_CONDITIONAL": "at least one valid required combination is material and at least one valid required combination is non-material",
      "SCIENTIFIC_DIFFERENCE_COLLAPSES": "FULL and every valid leave-one-out are non-material in parameter location, have substantial contour overlap, and have portable EDE/LCDM conclusions"
    },
    "model_preference": {
      "categories": {
        "modest": "2<DeltaChi2<6",
        "negligible": "DeltaChi2<=2",
        "substantive": "DeltaChi2>=6"
      },
      "formula": "DeltaChi2_EDE_arm=Chi2_LCDM_best_arm-Chi2_EDE_best_arm",
      "portability_material_if": "arms occupy different categories AND abs(DeltaChi2_A-DeltaChi2_B)>=2",
      "within_arm_only": true
    },
    "parameter_location": {
      "formula": "D_x=abs(x_A-x_B)/sqrt(sigma_A^2+sigma_B^2)",
      "material_if": "D_H0>=1 OR D_fEDE>=1 OR at least two eligible primary cosmological coordinates have D>=1",
      "weak_identification_rule": "log10z_c and thetai_scf cannot by themselves make parameter-location material when fEDE is weakly identified/prior dominated."
    }
  },
  "polychord_production": {
    "boost_posterior": 0,
    "confidence_for_unbounded": 0.9999995,
    "do_clustering": true,
    "max_ndead": "infinity",
    "max_ndead_runtime_encoding": "Python float(\"inf\") passed to Cobaya 3.5.6; preserves frozen semantic max_ndead=infinity without changing the numerical stopping contract",
    "measure_speeds": true,
    "nfail": "nlive",
    "nlive": "25d",
    "nprior": "10nlive",
    "num_repeats": "5d",
    "oversample_power": 0.4,
    "precision_criterion": 0.001,
    "read_resume": true,
    "seed_policy": "deterministic unique seed per arm/model/combination; exact seeds generated and frozen in the production program before any production result is inspected",
    "synchronous": true,
    "write_dead": true,
    "write_live": true,
    "write_prior": true,
    "write_resume": true,
    "write_stats": true
  },
  "polychord_seed_map": {
    "camspec:ede_n3:FULL": 421100,
    "camspec:ede_n3:NO_ACT_LENSING": 421102,
    "camspec:ede_n3:NO_ACT_PRIMARY": 421101,
    "camspec:ede_n3:NO_DESI_DR2": 421103,
    "camspec:ede_n3:NO_SN": 421104,
    "camspec:lcdm:FULL": 421000,
    "camspec:lcdm:NO_ACT_LENSING": 421002,
    "camspec:lcdm:NO_ACT_PRIMARY": 421001,
    "camspec:lcdm:NO_DESI_DR2": 421003,
    "camspec:lcdm:NO_SN": 421004,
    "hillipop:ede_n3:FULL": 422100,
    "hillipop:ede_n3:NO_ACT_LENSING": 422102,
    "hillipop:ede_n3:NO_ACT_PRIMARY": 422101,
    "hillipop:ede_n3:NO_DESI_DR2": 422103,
    "hillipop:ede_n3:NO_SN": 422104,
    "hillipop:lcdm:FULL": 422000,
    "hillipop:lcdm:NO_ACT_LENSING": 422002,
    "hillipop:lcdm:NO_ACT_PRIMARY": 422001,
    "hillipop:lcdm:NO_DESI_DR2": 422003,
    "hillipop:lcdm:NO_SN": 422004
  },
  "preflight_authority": {
    "artifact": "q042-preflight-final-v11",
    "final_result_gate": "PREFLIGHT_PASS",
    "program_id": "Q042-PREFLIGHT-V11",
    "program_sha256": "3dd736334f355d9f5e2232c2900c563587e8330413185fd9f897193c66f46f32",
    "result_id": "R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-011",
    "spec_sha256": "183139bf7bab9dcf1bf0e591762dbb1ddb4160244065a400709e2522d3241ebe"
  },
  "program_id": "Q042-PROD-V1",
  "q": "Q-042",
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V1",
  "scientific_question": "Kan den oprindelige Q041 downstream-portabilitetstest udf\u00f8res med en ny pr\u00e6registreret, konvergensrobust inference-strategi, der n\u00f8jagtigt bevarer den oprindelige scientific contract \u2014 begge native Planck-arme, \u039bCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, \u00e9n identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpr\u00e6ferenceregler \u2014 uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at \u00e6ndre kriterier efter resultaterne?",
  "status": "PREREGISTERED_PRODUCTION"
}
```

## q042_production_source_lock_v1.json

```json
{
  "case_id": "NOT DOCUMENTED",
  "external": {
    "act_dr6_lensing": {
      "commit": "b386ddbb5821c1216c709f051c9289292f174d30",
      "component": "act_dr6_lenslike.ACTDR6LensLike",
      "repository": "ACTCollaboration/act_dr6_lenslike",
      "tag": "v1.2.1"
    },
    "act_dr6_primary": {
      "commit": "880eacb40d66722eb1c32d7b5621e91662b4d808",
      "component": "act_dr6_cmbonly.ACTDR6CMBonly",
      "ell_min": 600,
      "repository": "ACTCollaboration/DR6-ACT-lite",
      "tag": "v1.0.1"
    },
    "desi_dr2": {
      "bao_data_commit": "b7b8a36e9bccb063081f811f323cada21ab5fbdd",
      "bao_data_tag": "v2.6",
      "cobaya_definition_commit": "b76b6fed2a6c8c5594c6f92d5058bef10079746a",
      "component": "bao.desi_dr2"
    },
    "supernova": {
      "component": "sn.pantheonplus",
      "reference_q014_github_run_id": 33597153303,
      "reference_q014_result_id": "R-Q014-EDE-EXTERNAL-VIABILITY-009",
      "runtime_file_hash_manifest_required": true,
      "selection_status": "PROSPECTIVELY_FROZEN_FOR_Q042_BEFORE_Q042_SCIENCE_RESULTS"
    }
  },
  "hard_rules": {
    "github_mutation_by_assistant_forbidden": true,
    "no_cross_arm_absolute_objective_evidence": true,
    "no_retroactive_threshold_changes": true,
    "pilot_outputs_forbidden_as_science": true,
    "q040_scientific_endpoints_forbidden": true
  },
  "preflight_parent": {
    "program_id": "Q042-PREFLIGHT-V11",
    "result_id": "R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-011",
    "scientific_result": false,
    "status": "PREFLIGHT_PASS"
  },
  "program_id": "Q042-PROD-V1",
  "q": "Q-042",
  "q032": {
    "artifacts": [
      "q032-refine-*",
      "q032-preflight-sealed-v2",
      "q032-hillipop-covariance-v2"
    ],
    "execution_commit": "4dc873a5e880d40858d831a3b421456728f0c032",
    "github_run_id": 33994305721,
    "result_id": "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
  },
  "q041_v19_runtime_reference": {
    "attempt": 4,
    "environment_artifact": "q041-environment-v19",
    "environment_artifact_id": "10401161073",
    "environment_digest": "sha256:a160b8ca6011cf1808bfd0644925a2ba554a0db668ec743df9733c592543ab80",
    "execution_commit": "a962ba70077422f8b69642dea4e8272e1d00e5ff",
    "github_run_id": 34979609004,
    "role": "KNOWN_GOOD_BASE_RUNTIME_CACHE_IDENTITY_ONLY_NO_SCIENCE_ENDPOINTS"
  },
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V1",
  "software": {
    "class_ede_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "class_ede_repository": "mwt5345/class_ede",
    "cobaya_version": "3.5.6",
    "cold_cache_hillipop_transport": "same official planck_2020_hillipop.TT v4.2 source via frozen q032_setup_v2.sh; only retry wrapper changed to 3 x timeout 1800s; no short NERSC availability probe",
    "hillipop_commit": "a09ddde3e7ce11df99f74685feb1f1764cafb251",
    "numpy_version": "1.26.4",
    "openmpi_runtime": "Ubuntu packages openmpi-bin + libopenmpi-dev; exact package versions recorded at runtime with dpkg-query",
    "poly_build_isolation": "pip --no-build-isolation --no-deps after explicit make -e libchord.so MPI=1 gate",
    "polychord_build_mode": "MPI=1 (PolyChordLite setup.py default)",
    "polychordlite_exact_commit": "3ade6445bb3719a6db6f6e81f178765545ffc833",
    "polychordlite_release_tag": "1.22.2",
    "polychordlite_repository": "PolyChord/PolyChordLite",
    "pybobyqa_version": "1.5.0",
    "python_version": "3.11",
    "q041_v19_base_cache_key": "q041-v19-${runner.os}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36",
    "v19_base_cache_key": "q041-v19-${{ runner.os }}-py311-q032-4dc873a-actcmb-880eacb-lens-b386ddb-desi-b7b8a36",
    "v19_base_cache_policy": "EXACT_PATH_LIST_AND_KEY_FAIL_ON_MISS",
    "v4_environment_cache_key": "q042-v4-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus",
    "v4_environment_cache_role": "KNOWN_GOOD_RUNTIME_BASE_FOR_V5; V4 reached real likelihood initialization before a local metadata gate failed.",
    "v7_environment_cache_key": "q042-v7-${{ runner.os }}-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus",
    "v7_environment_cache_role": "KNOWN_GOOD_RUNTIME_BASE_FOR_V9; V7 environment and initial bounded PolyChord smoke executed successfully before the same-process resume MPI lifecycle failure."
  },
  "spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
  "technical_adapters": {
    "polychord_max_ndead_infinity_encoding": {
      "bubbleverse_spec_value": "infinity",
      "cobaya_3_5_6_runtime_value": "Python float(\"inf\")",
      "frozen_semantics": "max_ndead=infinity",
      "reason": "Cobaya polychord.initialize converts numeric np.inf to internal unlimited sentinel -1 before NumberWithUnits processing; literal string infinity is not a valid d-unit value.",
      "scientific_setting_changed": false
    }
  },
  "v11_program_sha256": "3dd736334f355d9f5e2232c2900c563587e8330413185fd9f897193c66f46f32"
}
```
<!-- END PRESERVED PARENT TEXT -->


# APPENDIX B — EIGHT ORIGINAL UPLOADED JSON MEMBERS

No JSON member is edited or reformatted. Digests refer to original bytes extracted for reading from the unchanged upload.


## q042_production_final_v19.json

**Raw member SHA-256:** `95f024b5ffdde740ae796e54a7dbd02340c14f340b7ea935b70082e0ea607e07`; bytes: 287166.

```json
{
  "actual_computed_scientific_result": false,
  "bobyqa": {
    "camspec:ede_n3:FULL": {
      "all_four_present": true,
      "best_objective": 1258.0116695658376,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 485,
          "objective": 1310.760609951041,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422103,
          "source_artifact_digest": "sha256:44a4a5b2f3dff41f8e01ddbd88598eb58385c73a1d1e0a7f8e3874647c578d4b",
          "source_artifact_id": 10882725917,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-FULL-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "395a416cfc8a453e376a947c8ac76e7140c88892585c9639da06a4f42263cb48",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "fEDE": 0.1026521798252027,
            "log10z_c": 3.601464518222328,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165,
            "thetai_scf": 2.323499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 528,
          "objective": 1271.3193836874348,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422102,
          "source_artifact_digest": "sha256:d625bf1954a1b66d1360687aea9148fd06b08878dfa65c39f77e149425680e7e",
          "source_artifact_id": 10884386701,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-FULL-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "8c7b52a769215ac2818cc03ee1a1ae76dac00005b9d612217335ec677c8d5684",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "fEDE": 0.01595,
            "log10z_c": 3.679464518222328,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916,
            "thetai_scf": 2.95
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 375,
          "objective": 1258.0116695658376,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422101,
          "source_artifact_digest": "sha256:aa82d0f2034f0d82c07c68c2cf34b8fc6a4a0f37e54be9a2c739183cc2077607",
          "source_artifact_id": 10880625672,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-FULL-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "22645e3d32af5ab5874ebe566cc291df0d0661c887b95263e534ea5ea7a41eb6",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "fEDE": 0.018932179825202688,
            "log10z_c": 3.757464518222328,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917,
            "thetai_scf": 2.6834998625062294
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 138,
          "objective": 1264.6005207646394,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422100,
          "source_artifact_digest": "sha256:7f25c8706c09abb91337d9422b83097b234fe85e45be4df2197121ff0a42fbba",
          "source_artifact_id": 10874659342,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-FULL-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "44808294beec55a5bfe3487f67e4f78423cb2c9b702bc64f2b2e97a3bb73cef9",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "fEDE": 0.04285217982520269,
            "log10z_c": 3.861464518222328,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917,
            "thetai_scf": 2.923499862506229
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:ede_n3:NO_ACT_LENSING": {
      "all_four_present": true,
      "best_objective": 1252.0734632677068,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 186,
          "objective": 1252.0734632677068,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422102,
          "source_artifact_digest": "sha256:bd6b56683485022786ece2b33836eb55aaee0d7fc8af0bf59fdd811d09d0cb16",
          "source_artifact_id": 10883844111,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_LENSING-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "f3a22dc721b6583b588102c38671aa35e88e2c7f11eac3480c16e7c9562e99b3",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "fEDE": 0.04285217982520269,
            "log10z_c": 3.861464518222328,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917,
            "thetai_scf": 2.923499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 380,
          "objective": 1257.3042268794843,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422103,
          "source_artifact_digest": "sha256:df8a6b84012741d7ab634ed8cc204fbad77cc85d307e742d6d9187c7e2029c6e",
          "source_artifact_id": 10885156006,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_LENSING-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "1374833adb38579584c8edbe4b32502fa0f71bb1e2dcdae7e90c5ac3683960c2",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "fEDE": 0.018932179825202688,
            "log10z_c": 3.757464518222328,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917,
            "thetai_scf": 2.6834998625062294
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 333,
          "objective": 1259.401197685925,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422104,
          "source_artifact_digest": "sha256:bd6d702f9d7a74609fe9398a529c4f0885fcd57d78078957f00f5094d14d050a",
          "source_artifact_id": 10893490809,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_LENSING-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "64d4e0966970916dfed9857ed754ad4f82d6f03839298ab8c5c403da33cf876c",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "fEDE": 0.01595,
            "log10z_c": 3.679464518222328,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916,
            "thetai_scf": 2.95
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 434,
          "objective": 1296.3799948056062,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422105,
          "source_artifact_digest": "sha256:129f7e985e71cfa7805b7a2af88b6df68a31727e4079ac87f373be45d3b10424",
          "source_artifact_id": 10886778725,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_LENSING-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "468779d412b8c7ff3275058dc5a6d6cd9469461e90c826de2c83e39283b2e3a6",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "fEDE": 0.1026521798252027,
            "log10z_c": 3.601464518222328,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165,
            "thetai_scf": 2.323499862506229
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:ede_n3:NO_ACT_PRIMARY": {
      "all_four_present": true,
      "best_objective": 3920.043888456994,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1920,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 141,
          "objective": 3920.043888456994,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422101,
          "source_artifact_digest": "sha256:521e265a5cc5232be6c02df5ba2b0eac8d186ac73bca27a0cc65c5ed817dec46",
          "source_artifact_id": 10877690927,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_PRIMARY-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "30a931dbb2412d652f60d55b9f40f165194d08922133e67d5d92854252ceb36c",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "H0": 68.16599436660475,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "fEDE": 0.04285217982520269,
            "log10z_c": 3.861464518222328,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917,
            "thetai_scf": 2.923499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1920,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 439,
          "objective": 3929.9202598738457,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422103,
          "source_artifact_digest": "sha256:9f1843eb21896b4beef170d486929a0198b3cd979ab66489f88958d00fc385ed",
          "source_artifact_id": 10882092874,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_PRIMARY-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "cfae3e6edf73c3e09fd3954d7c7dc7f59991762092524a4ab245683653af4659",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "H0": 63.96599436660475,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "fEDE": 0.01595,
            "log10z_c": 3.679464518222328,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916,
            "thetai_scf": 2.95
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1920,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 230,
          "objective": 3925.8277919157317,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422102,
          "source_artifact_digest": "sha256:f33f253978ba5dd83badda12802a34a3f65d2ffdd1f467407377d733f1d644b1",
          "source_artifact_id": 10880131707,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_PRIMARY-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "98e0fc3fbd0cd7285e23fabc49cde9389fdee92a3adc747079752335c6de2ea1",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "H0": 70.56599436660476,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "fEDE": 0.018932179825202688,
            "log10z_c": 3.757464518222328,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917,
            "thetai_scf": 2.6834998625062294
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1920,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 354,
          "objective": 3929.967348605755,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422104,
          "source_artifact_digest": "sha256:9254bdfb9d4d88d5f0da212089591c34e7620b8ea9eb842280c98c5e3ceb3cd6",
          "source_artifact_id": 10882309909,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_ACT_PRIMARY-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "4f2c40ac0a706471ab4c5f109821fe59b1d8f17eeb75ebcb2bdb9ab6b574f7d2",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "H0": 74.16599436660475,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "fEDE": 0.1026521798252027,
            "log10z_c": 3.601464518222328,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165,
            "thetai_scf": 2.323499862506229
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:ede_n3:NO_DESI_DR2": {
      "all_four_present": true,
      "best_objective": 1247.2678075204017,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 411,
          "objective": 1266.1564296057916,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422106,
          "source_artifact_digest": "sha256:925fcdb3e5a3126e4ca3741fa2b86f85745c83892ce30a751745e251584b7f5f",
          "source_artifact_id": 10893203959,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_DESI_DR2-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "b564ef61557a3cd6c9953656295d30bbffbee22c85319c1b3520b40a84a42e33",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "fEDE": 0.1026521798252027,
            "log10z_c": 3.601464518222328,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165,
            "thetai_scf": 2.323499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 115,
          "objective": 1247.2678075204017,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422103,
          "source_artifact_digest": "sha256:230b4de454b1bde97a75eea511d8c450594eda2c9e6dd5d81254912729f858c9",
          "source_artifact_id": 10886285209,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_DESI_DR2-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "141060eebb04da2fe27bff23f9e379d5c7fb63d143810d3ec7eb131a76858c25",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "fEDE": 0.04285217982520269,
            "log10z_c": 3.861464518222328,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917,
            "thetai_scf": 2.923499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 231,
          "objective": 1266.9838578407398,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422104,
          "source_artifact_digest": "sha256:e676fdaeab5e6d2085dc3f2823bf7a08b00488880141950b0b1818ad42a8cf22",
          "source_artifact_id": 10890817532,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_DESI_DR2-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "4fcc1b3cdbf9f6c3168641dc9975366f57a8f75f0bdf0ae915ad37602e5535ce",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "fEDE": 0.018932179825202688,
            "log10z_c": 3.757464518222328,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917,
            "thetai_scf": 2.6834998625062294
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 322,
          "objective": 1254.3390621689987,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422105,
          "source_artifact_digest": "sha256:e076a837e48e384af01f695d815d75d7ad629701fca94b7a06f8c3c221a2d53d",
          "source_artifact_id": 10892646330,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_DESI_DR2-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "bba0c42acba4695790a9567389407c14e01c706c9d42d9597e6a2f6b137aee23",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "fEDE": 0.01595,
            "log10z_c": 3.679464518222328,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916,
            "thetai_scf": 2.95
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:ede_n3:NO_SN": {
      "all_four_present": true,
      "best_objective": 553.0700961078186,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 367,
          "objective": 561.4149610869697,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422105,
          "source_artifact_digest": "sha256:db8001592599157b225c9dbce26be492673b6ea70f003f96d297b0c1659c4c71",
          "source_artifact_id": 10894268298,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_SN-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "8cf5159b4775bef2caf536689caa64caf9d0757798ae1b96ba224f40cba6c19e",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "fEDE": 0.018932179825202688,
            "log10z_c": 3.757464518222328,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917,
            "thetai_scf": 2.6834998625062294
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 406,
          "objective": 565.4080337852134,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422106,
          "source_artifact_digest": "sha256:3aad90fbd7a91baf82222ce3507eae917ed47ea3858f183eae1a7b3e78cd97da",
          "source_artifact_id": 10895816750,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_SN-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "dd70ed5934ec2d927d44b88c2f17b7225b79c17b85f00c1c0fe8a8e2c4988c0a",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "fEDE": 0.01595,
            "log10z_c": 3.679464518222328,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916,
            "thetai_scf": 2.95
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 552,
          "objective": 565.1330318173518,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422107,
          "source_artifact_digest": "sha256:b1958909ba938826a3774bb69c7129cd9de83ec8b8c17da1f45f0c2667614629",
          "source_artifact_id": 10896990855,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_SN-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "306c35e7cc3d8e39f5fe67874ac027dbd3ab20c9ab88ca2768c6bb145246cfa7",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "fEDE": 0.1026521798252027,
            "log10z_c": 3.601464518222328,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165,
            "thetai_scf": 2.323499862506229
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2160,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 262,
          "objective": 553.0700961078186,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422104,
          "source_artifact_digest": "sha256:de240bff6d63667a4e39efcfd15c50e425094102fd1768c7bd744d005ad67d99",
          "source_artifact_id": 10892462528,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-ede_n3-NO_SN-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "687e9c04a4bb9aad09107c33468bdb7fb1d651177f92fd8b2ca53c8de5ed9810",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "fEDE": 0.04285217982520269,
            "log10z_c": 3.861464518222328,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917,
            "thetai_scf": 2.923499862506229
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:lcdm:FULL": {
      "all_four_present": true,
      "best_objective": 1255.4102262766746,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 172,
          "objective": 1255.4102262766746,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422000,
          "source_artifact_digest": "sha256:f035af8b8cde36fb9aacbb3c2ea4ff8abb1062aa4801219675b8105b53f5e12b",
          "source_artifact_id": 10865282550,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-FULL-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "d77c0e456cc6c12be301b53d1745e5854f042d9b6651733fb4c0c4bda65c3c3e",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 277,
          "objective": 1262.6485589706954,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422002,
          "source_artifact_digest": "sha256:42a301a5801bd63539469efc43836aaa4eb8b8f127b386a7f3050b3803adfdf9",
          "source_artifact_id": 10866056136,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-FULL-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "08cc3f2a8122fe04b7fc441db9415efec62d369223082f5409fe47b69a0d92d6",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 194,
          "objective": 1279.097876568888,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422001,
          "source_artifact_digest": "sha256:7e08d0d6bb73344ddc08ee888b808571662f3e4d53e32e638e3bd380d72a7d7d",
          "source_artifact_id": 10865553140,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-FULL-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "b1368014ccc4544bb059bbc30deb2ae3146cb46ed66fd64c86efe45a3794a7a1",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 530,
          "objective": 1257.4504600973855,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422003,
          "source_artifact_digest": "sha256:a9b37611988120b157d6c4deeff4cc5de060b655dfab50cadb3d5dede7f0f07c",
          "source_artifact_id": 10867063658,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-FULL-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "001cc3be133d89c8035cd50607ae23d975d6ea534f3e9389748c3976db19d628",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:lcdm:NO_ACT_LENSING": {
      "all_four_present": true,
      "best_objective": 1249.0223153705638,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 115,
          "objective": 1257.074063746064,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422002,
          "source_artifact_digest": "sha256:6660059335949ed8df63244667134ea37515f548b85451aa0e89cdc05ea92cd1",
          "source_artifact_id": 10867561315,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_LENSING-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "0f337184131f15ac59f2c109749819c7b2ed46724fa0b04a4273c6412a661a7e",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 352,
          "objective": 1251.0753236903672,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422005,
          "source_artifact_digest": "sha256:fea4e9247a85ed9c5d5bb2e8b7adcd92d123064401fac4bd46a9c1a7851f2f56",
          "source_artifact_id": 10871131301,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_LENSING-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "8312a9e39f3a03724a8c88535f2fb4417a79bfd46327a257596843841532cc07",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 338,
          "objective": 1254.2229785461795,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422003,
          "source_artifact_digest": "sha256:a8c8204db43852f092fbd4b516ff886cc0e4f6eb7d0b9e38bb57816c246ac8a2",
          "source_artifact_id": 10869818794,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_LENSING-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "325a46e6b65d85e5d114e88f31e9ad65aaa61692ab0c87ab370ac99217f51fd9",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 298,
          "objective": 1249.0223153705638,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422004,
          "source_artifact_digest": "sha256:ffbe8eddbbbf3d0fb0023b098b08435ffc8dae38b967e1d6b408e7e0c0583c0c",
          "source_artifact_id": 10869757700,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_LENSING-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "a68608bf1272e3839a191c0413c389c57c14f00e24dc664a8a4952f0ef7ae675",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:lcdm:NO_ACT_PRIMARY": {
      "all_four_present": true,
      "best_objective": 3919.963781461909,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1560,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 219,
          "objective": 3920.5849317594257,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422002,
          "source_artifact_digest": "sha256:cec1e78ab4f91c1d8e4845168b96cc900ed4378669a0824d95ce804b62df3b5b",
          "source_artifact_id": 10866362614,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_PRIMARY-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "13a99e57ccb7808419a9c6b48958f81e818c47a76a31c7a41e8957010416cda3",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "H0": 70.56599436660476,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1560,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 440,
          "objective": 3919.963781461909,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422004,
          "source_artifact_digest": "sha256:80e8f72fa98026eea92eb58967f730860b7db239c27107ee8bf66542008cbe8d",
          "source_artifact_id": 10867232983,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_PRIMARY-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "6024638c7bb5e727d239a2f31bb3b27e4f97f3b34575ded9255d5c67b1207908",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "H0": 74.16599436660475,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1560,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 325,
          "objective": 3930.3402505300724,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422003,
          "source_artifact_digest": "sha256:9e88050df118760c8a2c3728c3f9c499504cd7faf1cc3652eb1eee8d3d85a36c",
          "source_artifact_id": 10867606946,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_PRIMARY-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "9f1a76a53ae1d41e04bc4c3fde6b52ddf1b17030d72c94f05df0604da6b9e1c5",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "H0": 63.96599436660475,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1560,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 140,
          "objective": 3922.464250022087,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422001,
          "source_artifact_digest": "sha256:a530d451394bd84c760fad402109db731cb9628f9e3159fa14ab78816f1c3d0c",
          "source_artifact_id": 10866380166,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_ACT_PRIMARY-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "3eed50ff89907fc9ccb813cf3c2be7c4b9487c6c8d0ff804fb2859a19c63b8d3",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "H0": 68.16599436660475,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:lcdm:NO_DESI_DR2": {
      "all_four_present": true,
      "best_objective": 1244.9436280501968,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 381,
          "objective": 1270.1428494323795,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422006,
          "source_artifact_digest": "sha256:2212e52da16d26cc6e15131e04250991b192b65cd78e47e7f7724bed7862025f",
          "source_artifact_id": 10873458136,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_DESI_DR2-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "851b6ad194af4e52ccbffdfbd4ff14007633f585a4b9e67d56d071f68fdc30e7",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 126,
          "objective": 1244.9436280501968,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422003,
          "source_artifact_digest": "sha256:be3664a6fbfdc73c4640f983abc4596783990a4bd919bf37f87f0f74a83d7af8",
          "source_artifact_id": 10869068972,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_DESI_DR2-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "8bafd38f4463bb1ab114bb498d2f97d7243301400df55b33ba2040eefef1989e",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 306,
          "objective": 1251.5121462175684,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422005,
          "source_artifact_digest": "sha256:7456677f5fe1e22e940ac90f47398f6b36b3606910601a5787651ce82df523e2",
          "source_artifact_id": 10871112984,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_DESI_DR2-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "c385acee7bcc30794a49cfce26a1eaf84bc3bd2a2d85d77a39a2d3098c03c4d9",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 346,
          "objective": 1251.3031562445617,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422004,
          "source_artifact_digest": "sha256:b5c96f574bde0fe810cd7185ba4c1396b4ba4ca87219dbba81520185d86a463d",
          "source_artifact_id": 10872505526,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_DESI_DR2-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "a87d2db780f2dfb06436e16c4163b61b63bdf6bc125f67a19a63a5a12598b242",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "camspec:lcdm:NO_SN": {
      "all_four_present": true,
      "best_objective": 554.460838366523,
      "starts": [
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 137,
          "objective": 554.460838366523,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422004,
          "source_artifact_digest": "sha256:8288fb6f83fbf68368ac8d185a64fcd3fd8470140959a0e0a7f2c1b23b38a2d4",
          "source_artifact_id": 10872301186,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_SN-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "4e34b0bcd2d95ffd39cdea904c325703b9b8fdf87ee34f68472e2b747d907903",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "H0": 68.16599436660475,
            "P_act": 1.0,
            "amp_143": 19.06097111007752,
            "amp_143x217": 9.859995605449981,
            "amp_217": 12.94407930006934,
            "logA": 3.038051350703181,
            "n_143": 0.9532159371018946,
            "n_143x217": 1.3698548766627547,
            "n_217": 1.3084047024607666,
            "n_s": 0.9698398276398953,
            "omega_b": 0.02228900853774718,
            "omega_cdm": 0.12397402627882406,
            "tau_reio": 0.05141852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 500,
          "objective": 583.2643743330707,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422007,
          "source_artifact_digest": "sha256:5db047c6265bd87f3238ea8897fdd1115f5cc44e0843a0a7e7c5ffc830e3d346",
          "source_artifact_id": 10875828576,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_SN-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "28c5a739ae5ebe557d7fe00ff310a95275fe55018fd9e8f52918221cef6f0d02",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "H0": 74.16599436660475,
            "P_act": 0.96,
            "amp_143": 29.06097111007752,
            "amp_143x217": 2.5,
            "amp_217": 2.9440793000693404,
            "logA": 2.898051350703181,
            "n_143": 0.25,
            "n_143x217": 0.36985487666275474,
            "n_217": 0.30840470246076657,
            "n_s": 1.0098398276398952,
            "omega_b": 0.02388900853774718,
            "omega_cdm": 0.13997402627882405,
            "tau_reio": 0.029418523520219165
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 261,
          "objective": 567.3523986399714,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422005,
          "source_artifact_digest": "sha256:3fc3cd452aaa04358dc333941f3e9870db302305baa0022681be112a19589204",
          "source_artifact_id": 10873447663,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_SN-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "f23dccbdcf0cd5ada27ec551392f3538c6276eeb84d3a36fa838eb80c142f35a",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "H0": 70.56599436660476,
            "P_act": 1.016,
            "amp_143": 15.06097111007752,
            "amp_143x217": 13.859995605449981,
            "amp_217": 8.94407930006934,
            "logA": 2.982051350703181,
            "n_143": 1.3532159371018946,
            "n_143x217": 1.7698548766627549,
            "n_217": 1.7084047024607667,
            "n_s": 0.9538398276398953,
            "omega_b": 0.02292900853774718,
            "omega_cdm": 0.11757402627882406,
            "tau_reio": 0.06021852352021917
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "camspec",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 1800,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 377,
          "objective": 554.5354266568906,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 422006,
          "source_artifact_digest": "sha256:c8629e63ea45ad00787d72f26827c6ff831024fbd34f812ff13a07e5502adea2",
          "source_artifact_id": 10875520517,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-camspec-lcdm-NO_SN-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "40e139a5c4d1ba5cc1896f779e5d3627d4ec1d347c597dd8354701a150469925",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "H0": 63.96599436660475,
            "P_act": 1.028,
            "amp_143": 12.06097111007752,
            "amp_143x217": 16.85999560544998,
            "amp_217": 5.9440793000693395,
            "logA": 3.136051350703181,
            "n_143": 0.2532159371018945,
            "n_143x217": 2.0698548766627547,
            "n_217": 2.0084047024607665,
            "n_s": 0.9418398276398953,
            "omega_b": 0.02116900853774718,
            "omega_cdm": 0.11277402627882406,
            "tau_reio": 0.06681852352021916
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:ede_n3:FULL": {
      "all_four_present": true,
      "best_objective": 1233.5847218881304,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 586,
          "objective": 1243.8699017895094,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423102,
          "source_artifact_digest": "sha256:ee6d475d814fe586566ba5c9b82f1c35876a549899b599e25807cd8e6fbe0466",
          "source_artifact_id": 10904745534,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-FULL-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "c80e4b16ef3be8ce17d0b21b79856d5a8cd97e28b0b618dfb00a896aa0975efb",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "fEDE": 0.01595,
            "log10z_c": 3.5682704155779823,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "thetai_scf": 2.95,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 233,
          "objective": 1233.5847218881304,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423100,
          "source_artifact_digest": "sha256:9eb209f5f3e77d9cde5e4abeec38e350f87e7023ca5f8554d8aefb7f162a4456",
          "source_artifact_id": 10902321426,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-FULL-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "7dfce3beb07266cec49020c63a8d06bef116c54bdaa45e16b61cadd8cdc0deb0",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "fEDE": 0.047853456097294196,
            "log10z_c": 3.7502704155779822,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "thetai_scf": 2.95,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": -3,
          "max_evals": 3120,
          "message": "Minimization failed! Here is the raw result object:\n****** Py-BOBYQA Results ******\nSolution xmin = [-1.43778034e+00  2.77171856e+00 -5.50792728e+00 -2.27555837e-02\n  3.25313865e+00  3.28184237e+00 -6.36662723e-01  1.09086423e+00\n -2.58381287e+01 -1.86415329e+01 -1.04759520e+01  1.29798774e+00\n  8.72101868e+00  2.30105137e+00 -1.31202216e+00  3.39511829e+01\n  3.11873133e+01 -5.57199684e+00  7.18159469e-01  1.94658038e+00\n  1.83675197e+00 -4.42870904e+00  9.43852330e+00 -6.42858044e+00\n  2.25507570e+01 -1.16033960e+00]\nObjective value f(xmin) = 1264.667475\nNeeded 207 objective evaluations (at 207 points)\nApproximate gradient = [ -4.60040838  12.00329157   1.28578869   9.23002535  -7.22054645\n   9.46196185  -4.9059196  -15.81402281  -8.37381605   6.66732481\n   3.08872876   5.04948983   2.69175003   4.45546986  -4.60376072\n   0.53557611   1.44229747   2.8213782    1.95377891   9.08274698\n  -0.48487179  -4.8432523   -9.27565662   5.11870651   0.94341174\n   8.87595169]\nNot showing approximate Hessian because it is too long; check self.hessian\nExit flag = -3\nError (linear algebra): Singular matrix in mini-model interpolation (main loop)\n******************************\n",
          "model": "ede_n3",
          "nf": 207,
          "objective": 1264.667475,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423101,
          "source_artifact_digest": "sha256:81414935a4315c4481da9cdedc0cda19f195d22cd9737a4e9fe92671c9cdd6c0",
          "source_artifact_id": 10902388535,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-FULL-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "87f200d1495d9fe344ebf030be32d13c5d4d0a7dee6161632a07d2dc4735b5ec",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "fEDE": 0.023933456097294196,
            "log10z_c": 3.646270415577982,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "thetai_scf": 2.7133966874881033,
            "xi": 0.3928374089428436
          },
          "status": "RECORDED_FAILURE",
          "technical_ok": false,
          "wrapper_exception": "LoggedError('Minimization failed! Here is the raw result object:\\n****** Py-BOBYQA Results ******\\nSolution xmin = [-1.43778034e+00  2.77171856e+00 -5.50792728e+00 -2.27555837e-02\\n  3.25313865e+00  3.28184237e+00 -6.36662723e-01  1.09086423e+00\\n -2.58381287e+01 -1.86415329e+01 -1.04759520e+01  1.29798774e+00\\n  8.72101868e+00  2.30105137e+00 -1.31202216e+00  3.39511829e+01\\n  3.11873133e+01 -5.57199684e+00  7.18159469e-01  1.94658038e+00\\n  1.83675197e+00 -4.42870904e+00  9.43852330e+00 -6.42858044e+00\\n  2.25507570e+01 -1.16033960e+00]\\nObjective value f(xmin) = 1264.667475\\nNeeded 207 objective evaluations (at 207 points)\\nApproximate gradient = [ -4.60040838  12.00329157   1.28578869   9.23002535  -7.22054645\\n   9.46196185  -4.9059196  -15.81402281  -8.37381605   6.66732481\\n   3.08872876   5.04948983   2.69175003   4.45546986  -4.60376072\\n   0.53557611   1.44229747   2.8213782    1.95377891   9.08274698\\n  -0.48487179  -4.8432523   -9.27565662   5.11870651   0.94341174\\n   8.87595169]\\nNot showing approximate Hessian because it is too long; check self.hessian\\nExit flag = -3\\nError (linear algebra): Singular matrix in mini-model interpolation (main loop)\\n******************************\\n')"
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 842,
          "objective": 1246.0255762612032,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423103,
          "source_artifact_digest": "sha256:dded44bf7cd2313adf3d78edfec087f8f6d8f48ec697c6e22e818c4f539968dd",
          "source_artifact_id": 10904802681,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-FULL-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "0b53c31eff88c4b59c3e2f7ea31d7c3c52c13f07d17cf708b4d805366c723f54",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "fEDE": 0.1076534560972942,
            "log10z_c": 3.4902704155779825,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "thetai_scf": 2.3533966874881034,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 3
    },
    "hillipop:ede_n3:NO_ACT_LENSING": {
      "all_four_present": true,
      "best_objective": 1223.830108490833,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 188,
          "objective": 1223.830108490833,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423102,
          "source_artifact_digest": "sha256:9c88ae12c0bab58aaa7975c147cdedbb5af90a81e158586f3051919c0f8eec4a",
          "source_artifact_id": 10905187494,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_LENSING-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "1282d36e3402812aab241729a9ec565a838215653655cdf4d19e740eb6caa3b2",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "fEDE": 0.047853456097294196,
            "log10z_c": 3.7502704155779822,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "thetai_scf": 2.95,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 453,
          "objective": 1231.2483840889513,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423104,
          "source_artifact_digest": "sha256:17ca7a1698df7f3bc6e68787d7db2c42f4a745be44177c6fbe7e681b32bdb840",
          "source_artifact_id": 10907635534,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_LENSING-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "b6debcfb9b267b1bd1f94ba94b6295520db947ef9f97c02cfb7f6b972859a0c0",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "fEDE": 0.01595,
            "log10z_c": 3.5682704155779823,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "thetai_scf": 2.95,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 518,
          "objective": 1225.9561821774723,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423103,
          "source_artifact_digest": "sha256:8c57e5e620c0a2a68ec86599b39ded431f6bd30ef95ec056ef27a42b5d7f7feb",
          "source_artifact_id": 10905829859,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_LENSING-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "3a7d981282ff2f2be9b1fd552eb01b11285654ce76f0340a1ff546d7a452e7ac",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "fEDE": 0.023933456097294196,
            "log10z_c": 3.646270415577982,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "thetai_scf": 2.7133966874881033,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 379,
          "objective": 1238.6343611542065,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423105,
          "source_artifact_digest": "sha256:d1bf8676d8d12319861833e2b9f1113c17590081839516a9c3221b7ef7b05961",
          "source_artifact_id": 10906159784,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_LENSING-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "66201e2eb73b4c41b54594aa631e42ce0ea78f883ee5758f5d306c150f01e2bd",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "fEDE": 0.1076534560972942,
            "log10z_c": 3.4902704155779825,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "thetai_scf": 2.3533966874881034,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:ede_n3:NO_ACT_PRIMARY": {
      "all_four_present": true,
      "best_objective": 3757.736941078028,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2880,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 628,
          "objective": 3772.746204702667,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423103,
          "source_artifact_digest": "sha256:5051b4abfe6a16655333a2d63e5d4890b906f647ca32a923fa77828dad3e0f6f",
          "source_artifact_id": 10905210123,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_PRIMARY-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "7e3ea17b7589ba78b5fa3ad04b4630ac3be032063d2717de37c19771bd10ab5b",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "fEDE": 0.01595,
            "log10z_c": 3.5682704155779823,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "thetai_scf": 2.95,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2880,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 885,
          "objective": 3774.3563534939813,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423104,
          "source_artifact_digest": "sha256:70e3ee1550ba7a8169067587c767ed0a9a8a16ece3e5f3247268c68f8e757218",
          "source_artifact_id": 10906538081,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_PRIMARY-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "79c00cc305838c92f33e1f3261bb047130f0068dd5345112e9199be98ad33085",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "fEDE": 0.1076534560972942,
            "log10z_c": 3.4902704155779825,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "thetai_scf": 2.3533966874881034,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2880,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 643,
          "objective": 3757.736941078028,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423102,
          "source_artifact_digest": "sha256:19bc8eb85b6f9e38072651eacafbddd2364959f47078af2b2b21bd79b23bd8a3",
          "source_artifact_id": 10904019152,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_PRIMARY-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "b623e29591abd400dadb18833093b189d271db80474e98cab777593790038309",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "fEDE": 0.023933456097294196,
            "log10z_c": 3.646270415577982,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "thetai_scf": 2.7133966874881033,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2880,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 234,
          "objective": 3759.128149613546,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423101,
          "source_artifact_digest": "sha256:18598dc17d79e5ff829f0b30ba74b4cc0675720e1dbefa4e75bb6373924f532f",
          "source_artifact_id": 10903455812,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_ACT_PRIMARY-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "49bed090b3f4a32ba89abe59ce82abe01249c05f4cec43d1fc7c7f2ecd298a2b",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "fEDE": 0.047853456097294196,
            "log10z_c": 3.7502704155779822,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "thetai_scf": 2.95,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:ede_n3:NO_DESI_DR2": {
      "all_four_present": true,
      "best_objective": 1220.8442534423452,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 920,
          "objective": 1241.5444260996205,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423106,
          "source_artifact_digest": "sha256:847a4ab1f5e95541cc8b1e59d7016f858eb143406128f6c4e3e4ac2d272a2051",
          "source_artifact_id": 10911975974,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_DESI_DR2-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "604ecf86fc3d22c8ee57b5a924e29da9fda1920835490c792f9942628505d2c6",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "fEDE": 0.1076534560972942,
            "log10z_c": 3.4902704155779825,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "thetai_scf": 2.3533966874881034,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 222,
          "objective": 1220.8442534423452,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423103,
          "source_artifact_digest": "sha256:08d6048e99d3ec257b3335a88e6711bba01f195be40cd60413b74a392dc80b5e",
          "source_artifact_id": 10906949246,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_DESI_DR2-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "b591dac8c7370e468f32079024023f9192100df9ec755096f8a7f07bd45bd476",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "fEDE": 0.047853456097294196,
            "log10z_c": 3.7502704155779822,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "thetai_scf": 2.95,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 865,
          "objective": 1239.8928676347464,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423105,
          "source_artifact_digest": "sha256:b8bd79b27dff0a3ba370d922e54512265fff350d006c96dac1b91d5f42301d76",
          "source_artifact_id": 10909819748,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_DESI_DR2-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "e647442ac7eb1b8c5e990c99005cae8d1db7697440e56f276f13920a056c7b48",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "fEDE": 0.01595,
            "log10z_c": 3.5682704155779823,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "thetai_scf": 2.95,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 530,
          "objective": 1220.9095399498385,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423104,
          "source_artifact_digest": "sha256:21ea8262b1f5a5d3952ceadac4f2619a53d29cd0abc6414f70911d9b3c11405b",
          "source_artifact_id": 10909654336,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_DESI_DR2-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "fff9a67e969f6444439f42d092daec7b1a8769aad43d3d5a07ba6c8483be94db",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "fEDE": 0.023933456097294196,
            "log10z_c": 3.646270415577982,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "thetai_scf": 2.7133966874881033,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:ede_n3:NO_SN": {
      "all_four_present": true,
      "best_objective": 529.1299116083803,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 515,
          "objective": 529.8369154067473,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423107,
          "source_artifact_digest": "sha256:f522ff2adac833c604be90897e30fbe5c9620bc6f059f59323b4fafe6aef3866",
          "source_artifact_id": 10912398276,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_SN-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "7302e07b89f78bf8f10ec91802e310f232fb1de0ba4d70d7cf25a5d6c3eb818a",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "fEDE": 0.1076534560972942,
            "log10z_c": 3.4902704155779825,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "thetai_scf": 2.3533966874881034,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 566,
          "objective": 531.5183517942988,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423105,
          "source_artifact_digest": "sha256:b27eecd6ceafe99c229041a058b2586548b018e69e288aeb744311fca128e8ce",
          "source_artifact_id": 10911154043,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_SN-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "cea94adf1e3d54e6858af62acdbc48bd746c48679c1d421443ba828d08176e83",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "fEDE": 0.023933456097294196,
            "log10z_c": 3.646270415577982,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "thetai_scf": 2.7133966874881033,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 798,
          "objective": 561.295665965051,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423106,
          "source_artifact_digest": "sha256:ca54817dff0210e8fb8ca5a7a13dc8d48512f34a30118cdf75ef12e9cb20cd40",
          "source_artifact_id": 10914246548,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_SN-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "aa9fffcf42e28cb8424746c81a415a401841a7d7bc67370f54219885a7de47f3",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "fEDE": 0.01595,
            "log10z_c": 3.5682704155779823,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "thetai_scf": 2.95,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 3120,
          "message": "Success: rho has reached rhoend",
          "model": "ede_n3",
          "nf": 234,
          "objective": 529.1299116083803,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423104,
          "source_artifact_digest": "sha256:a68bf0226c3b2129488556dbc2d868377fcefa3cc9e61181ac9add78d5fa8d33",
          "source_artifact_id": 10908711994,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-ede_n3-NO_SN-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "79f8a2d1a9b24a84e8862a9fb915435071d5067fe5f40e079817eadbde8e5d7f",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "fEDE": 0.047853456097294196,
            "log10z_c": 3.7502704155779822,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "thetai_scf": 2.95,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:lcdm:FULL": {
      "all_four_present": true,
      "best_objective": 1229.6810164306594,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 170,
          "objective": 1229.6810164306594,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423000,
          "source_artifact_digest": "sha256:2b95c64e23fa013e7b9ceef20378e63cac98f3576beb1c30c0aafb0767bf7af2",
          "source_artifact_id": 10894745222,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-FULL-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "996352b28bd5edc47591c204487d097b20f4ca449e87645d9d37ba58377c7244",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 485,
          "objective": 1234.8347782599703,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423001,
          "source_artifact_digest": "sha256:67d4c3f00df255cb4f1b09792bff78b8be1d54d0fefdce52d4c52a35e5ed06b8",
          "source_artifact_id": 10894479916,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-FULL-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "5db7050b21ff7978c6213d970851e25c9d0392ea6dd70e4d5a4ef676d539ce97",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 683,
          "objective": 1237.5597081089584,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423003,
          "source_artifact_digest": "sha256:4f7c569b64ec1217afdc6b88153b467a973e39edc5a5d6ff52129c719d7ced2c",
          "source_artifact_id": 10897702504,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-FULL-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "267c16d6875a400a16b9fa3799292a244aef4511daf2f19b14b537451510e734",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "FULL",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 571,
          "objective": 1247.3533943730595,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423002,
          "source_artifact_digest": "sha256:0d47411c7bbe90dac0ec513045472acf31e6b19cfa896353643e9c1078cbab0c",
          "source_artifact_id": 10896576350,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-FULL-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "a2fae91beb07c44d81edf201880f9a4641867db08079d637d9cd9dd8a9f38324",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:lcdm:NO_ACT_LENSING": {
      "all_four_present": true,
      "best_objective": 1222.5571609895107,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 462,
          "objective": 1225.7650876264279,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423004,
          "source_artifact_digest": "sha256:43014feb4f3d95ccd9b66a981db41d0db222126ec94801b056e01ce8f00e2f10",
          "source_artifact_id": 10899187674,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_LENSING-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "89f9f592269874aa298494872f55f4139ea55e82e32fb1b39c9e27eb4834d213",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 482,
          "objective": 1226.8673066238837,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423003,
          "source_artifact_digest": "sha256:cf193da9fa8a9003ef573344adc7b2f58382f0271e3d486b391ccea7d4772dc9",
          "source_artifact_id": 10899336239,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_LENSING-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "747af2132b3f8d1dcdecdf8ca46ae3a0131aeb39287112680746268f99523a8b",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 265,
          "objective": 1222.5571609895107,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423002,
          "source_artifact_digest": "sha256:74ef5c53a6a3827a4c23198b2493160b5a4e450d6de52df2063f53d9e7a85a9d",
          "source_artifact_id": 10897482135,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_LENSING-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "1e3dfa65a4a7e8730e8c473c76ab060f156654a743cfcac1b72f439f76847d42",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_LENSING",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 621,
          "objective": 1244.3908588626662,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423005,
          "source_artifact_digest": "sha256:052280fd52d5f1ea96d9f3bc05ff1815c1b3ff8c52d30f12909175410f8a45f2",
          "source_artifact_id": 10899555216,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_LENSING-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "2400944cac4889b8a2a3d534ba7989cb7b1ac0439d1d58b186a3d09c958f2495",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:lcdm:NO_ACT_PRIMARY": {
      "all_four_present": true,
      "best_objective": 3760.271996382225,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2520,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 617,
          "objective": 3760.371923743305,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423003,
          "source_artifact_digest": "sha256:7cd1ddfca2477ff01901ea8be29eb51ed1eaeafe3c468c6cc9eb96b2a1f5ff35",
          "source_artifact_id": 10896933601,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_PRIMARY-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "7e74552ec521b64af591cd712cf26c2f4fb873385a066730c6fc1ae49908da39",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2520,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 1027,
          "objective": 3771.8883942277635,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423004,
          "source_artifact_digest": "sha256:bb744c48b8db316d0692bd6c35e32bb6474c1d74700b18dbb85c11d7ebf0410d",
          "source_artifact_id": 10898293947,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_PRIMARY-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "01785d9877706f6453d3a5d69869e980d602a94c0ecd076c2ba84fa9f38cf6ab",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2520,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 287,
          "objective": 3762.5534940306843,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423001,
          "source_artifact_digest": "sha256:bcf5521572d4b513ca45e1c32c2e1b463e5f3a81c0751265e57169008ab8a8e4",
          "source_artifact_id": 10896780989,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_PRIMARY-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "6dd4e3de3f531e37cb8e38d28d7121175bb83bd698119924a85f0d0e61369d9a",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_ACT_PRIMARY",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2520,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 519,
          "objective": 3760.271996382225,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423002,
          "source_artifact_digest": "sha256:d82a09185deb119ad6d1f0894a718b24b19b930d04fc47fb318505746622fddf",
          "source_artifact_id": 10897900547,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_ACT_PRIMARY-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "de99a4fcf09a857192e9c24c79e5b0b586e9e8c7b4cbb9c7e71dd6d329f160ea",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    },
    "hillipop:lcdm:NO_DESI_DR2": {
      "all_four_present": true,
      "best_objective": 1218.4725771519393,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 372,
          "objective": 1223.0568310570245,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423005,
          "source_artifact_digest": "sha256:8101dce3d5b7d5bcf1add9cd0ad43378472b95820a69892428ef5b85ce9ad102",
          "source_artifact_id": 10899896034,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_DESI_DR2-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "35d0fd4f217196a1d7726ba156424b929b0bf614ba6dca5476352351980a327b",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 179,
          "objective": 1218.4725771519393,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423003,
          "source_artifact_digest": "sha256:6a05d51895739cfcab1ad36eda78b6096277c2ead57b094903e725c914c3b75a",
          "source_artifact_id": 10899064150,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_DESI_DR2-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "1450a6f28d0b7c3b6dec6b8e9cf633a9192a6fba9f6f115dfafe0e328e63a06c",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": -3,
          "max_evals": 2760,
          "message": "Minimization failed! Here is the raw result object:\n****** Py-BOBYQA Results ******\nSolution xmin = [-13.49052608 -18.18647175 -15.70504985   2.96618017  -8.9133129\n  12.95589609   3.22232607  24.86729947  -4.54806424  -9.82741482\n   6.92004015  -9.69801235  -5.54203246   0.71189142  12.73847741\n   0.22482543   0.85498131  -0.65363165  -7.80232699  23.36610305\n  11.67162591  74.7248662    3.5224873 ]\nObjective value f(xmin) = 1225.17065\nNeeded 882 objective evaluations (at 882 points)\nApproximate gradient = [ 0.00784593  0.57862146 -0.36475651  0.2043215   0.0105407   1.75181089\n  0.98867399  0.59832832 -0.13451603  0.37436778  1.31685407  0.1771023\n -0.35559082 -0.19116672  0.21701416  0.08797471  0.97817872  0.38905976\n  1.10040036 -0.27670043 -3.35112117  0.12082308 -0.60976713]\nNot showing approximate Hessian because it is too long; check self.hessian\nExit flag = -3\nError (linear algebra): Singular matrix in mini-model interpolation (main loop)\n******************************\n",
          "model": "lcdm",
          "nf": 882,
          "objective": 1225.17065,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423006,
          "source_artifact_digest": "sha256:c1935159c6d463dbd2c72870fddb5fc4b760d19923af7015ca2d11f84b9cb1df",
          "source_artifact_id": 10901776074,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_DESI_DR2-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "10bdca5f3447aa5ca4470c97af9fef418a441dbb9d31f93c74bd3f359e566b74",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "xi": -0.16716259105715642
          },
          "status": "RECORDED_FAILURE",
          "technical_ok": false,
          "wrapper_exception": "LoggedError('Minimization failed! Here is the raw result object:\\n****** Py-BOBYQA Results ******\\nSolution xmin = [-13.49052608 -18.18647175 -15.70504985   2.96618017  -8.9133129\\n  12.95589609   3.22232607  24.86729947  -4.54806424  -9.82741482\\n   6.92004015  -9.69801235  -5.54203246   0.71189142  12.73847741\\n   0.22482543   0.85498131  -0.65363165  -7.80232699  23.36610305\\n  11.67162591  74.7248662    3.5224873 ]\\nObjective value f(xmin) = 1225.17065\\nNeeded 882 objective evaluations (at 882 points)\\nApproximate gradient = [ 0.00784593  0.57862146 -0.36475651  0.2043215   0.0105407   1.75181089\\n  0.98867399  0.59832832 -0.13451603  0.37436778  1.31685407  0.1771023\\n -0.35559082 -0.19116672  0.21701416  0.08797471  0.97817872  0.38905976\\n  1.10040036 -0.27670043 -3.35112117  0.12082308 -0.60976713]\\nNot showing approximate Hessian because it is too long; check self.hessian\\nExit flag = -3\\nError (linear algebra): Singular matrix in mini-model interpolation (main loop)\\n******************************\\n')"
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_DESI_DR2",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 652,
          "objective": 1223.330825203618,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423004,
          "source_artifact_digest": "sha256:9296363bf54569d59d3cb5f835de852c3b5e98ce8a1850a99ee51f25458e8198",
          "source_artifact_id": 10900426360,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_DESI_DR2-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "4e15044ee4deea2149c86e0a80df25c7d5179aa9842bb693d238c1a4800821ee",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 3
    },
    "hillipop:lcdm:NO_SN": {
      "all_four_present": true,
      "best_objective": 525.5684296092363,
      "starts": [
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 495,
          "objective": 530.009217094505,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423005,
          "source_artifact_digest": "sha256:f463c9e9d2ca3b102fd883f45e699c5b368f388d9ae5c3df749c8428038cb6e1",
          "source_artifact_id": 10900962490,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_SN-s1",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "cef1137ae7d2acce16717794b75c61a603e051edcdd2c617647e5a4943efe9f9",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 1,
          "start_values": {
            "A_act": 0.92,
            "Acib": 3.4280064789322493,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 48.63758995597009,
            "Atsz": 4.623587304485474,
            "H0": 71.11112237752118,
            "P_act": 1.016,
            "cal100A": 0.998827771218167,
            "cal100B": 0.9906061018681405,
            "cal143B": 0.9782349705740255,
            "cal217A": 1.0067015937283674,
            "cal217B": 0.9853130146269569,
            "logA": 2.989547604794533,
            "n_s": 0.9558548882321027,
            "omega_b": 0.02284304442959164,
            "omega_cdm": 0.11716742051289905,
            "tau_reio": 0.06030685267029027,
            "xi": 0.3928374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 215,
          "objective": 525.5684296092363,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423004,
          "source_artifact_digest": "sha256:de97e8e3f99da1437879c72470b271dbde2d8fcbc04eab441c627c194dfdf4e4",
          "source_artifact_id": 10899094474,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_SN-s0",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "589398ea2c54119c6d992a045552bfda984e2c7996b6bf4c7c3e210ef77353e5",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 0,
          "start_values": {
            "A_act": 1.0,
            "Acib": 1.8280064789322492,
            "Adusty": 5.980990136411378,
            "Aksz": 4.875301534658886,
            "Aradio": 60.63758995597009,
            "Atsz": 8.623587304485474,
            "H0": 68.71112237752118,
            "P_act": 1.0,
            "cal100A": 1.014827771218167,
            "cal100B": 1.0066061018681405,
            "cal143B": 0.9942349705740255,
            "cal217A": 0.9907015937283674,
            "cal217B": 1.0013130146269569,
            "logA": 3.045547604794533,
            "n_s": 0.9718548882321028,
            "omega_b": 0.022203044429591638,
            "omega_cdm": 0.12356742051289905,
            "tau_reio": 0.05150685267029027,
            "xi": 0.2328374089428436
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 531,
          "objective": 545.3112770901035,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423006,
          "source_artifact_digest": "sha256:cfb7a05bf4ff9b8cc231cc61f7872eb43093bb6fae1e47b7512bce6d27aabd69",
          "source_artifact_id": 10901505754,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_SN-s2",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "f97b3c40d0edfcb45d0a13aa2eb266e81d6427ad62f946591cdfe696a5783338",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 2,
          "start_values": {
            "A_act": 0.86,
            "Acib": 1.0,
            "Adusty": 19.98099013641138,
            "Aksz": 2.5,
            "Aradio": 39.637589955970085,
            "Atsz": 15.623587304485476,
            "H0": 64.51112237752118,
            "P_act": 1.028,
            "cal100A": 1.042827771218167,
            "cal100B": 1.0346061018681405,
            "cal143B": 1.0222349705740255,
            "cal217A": 0.9627015937283674,
            "cal217B": 0.9733130146269569,
            "logA": 3.143547604794533,
            "n_s": 0.9438548882321027,
            "omega_b": 0.02108304442959164,
            "omega_cdm": 0.11236742051289905,
            "tau_reio": 0.06690685267029027,
            "xi": -0.04716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        },
        {
          "arm": "hillipop",
          "case_id": "NOT DOCUMENTED",
          "combination": "NO_SN",
          "computed_by_program_id": "Q042-PROD-V1",
          "computed_by_result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
          "computed_by_run_id": "Q042-PRODUCTION-PORTABILITY-V1",
          "flag": 0,
          "max_evals": 2760,
          "message": "Success: rho has reached rhoend",
          "model": "lcdm",
          "nf": 796,
          "objective": 528.6824202287895,
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
          "reused_by_program_id": "Q042-PROD-V18",
          "rhoend": 0.05,
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "scientific_role": "WITHIN_ARM_BEST_FIT_ONLY",
          "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
          "seed": 423007,
          "source_artifact_digest": "sha256:50c376085f8df627d6f67e94939bb2ee33adb9a674f0effb7673309bd4565da6",
          "source_artifact_id": 10901719823,
          "source_artifact_name": "q042-prod-36133813540-bobyqa-hillipop-lcdm-NO_SN-s3",
          "source_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
          "source_record_sha256": "45ab619b4c6e7aab743a9b10e7ee800f4ab63f55ccd9e539adaaf51a43e0c979",
          "source_root_run_id": 36133813540,
          "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
          "start_index": 3,
          "start_values": {
            "A_act": 0.8,
            "Acib": 1.0,
            "Adusty": 5.0,
            "Aksz": 2.5,
            "Aradio": 90.6375899559701,
            "Atsz": 18.623587304485476,
            "H0": 74.71112237752118,
            "P_act": 0.96,
            "cal100A": 0.974827771218167,
            "cal100B": 0.9666061018681404,
            "cal143B": 1.0342349705740255,
            "cal217A": 1.0307015937283674,
            "cal217B": 0.9613130146269568,
            "logA": 2.905547604794533,
            "n_s": 1.0118548882321028,
            "omega_b": 0.02380304442959164,
            "omega_cdm": 0.13956742051289905,
            "tau_reio": 0.029506852670290264,
            "xi": -0.16716259105715642
          },
          "status": "PASS",
          "technical_ok": true
        }
      ],
      "usable_start_count": 4
    }
  },
  "bobyqa_recomputed_in_v19": 0,
  "bobyqa_unusable_cells": [],
  "case_id": "NOT DOCUMENTED",
  "controlled_polychord_cells": [
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_SN",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "4f587084ce63766bcfb52b4e730b6f0ca5a69549b38493e89bf258a4332c0ff0",
          "seed": 421104,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790941976.8059084,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790941880606343811,
        "primary_resume_sha256": "a3f39fcd0a759592822c441f51cfccb5ec20487d2c1a092ad47e177324a287fe",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_SN",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "4f587084ce63766bcfb52b4e730b6f0ca5a69549b38493e89bf258a4332c0ff0",
          "seed": 421104,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790927371.1221623,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790941880606343811,
        "primary_resume_sha256": "a3f39fcd0a759592822c441f51cfccb5ec20487d2c1a092ad47e177324a287fe",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36980360731",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_SN",
      "config_hash": "688c120fd9d59c6981de206a482e421c9ecfe704c4c733224bbc312352166968",
      "elapsed_seconds": 14408.238047361374,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421104,
      "segment": 7,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_SN",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "23035c3143bb405245d1510f69a84e08f8d2670ded8ce4eff2a8c8a6c3308814",
          "seed": 421004,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790869122.8317564,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790869022564465909,
        "primary_resume_sha256": "3263bff7061047b9fc8f329e361604376de8c813efd145d1581eb932292b6c15",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_SN",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "23035c3143bb405245d1510f69a84e08f8d2670ded8ce4eff2a8c8a6c3308814",
          "seed": 421004,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790853555.5036247,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790869022564465909,
        "primary_resume_sha256": "3263bff7061047b9fc8f329e361604376de8c813efd145d1581eb932292b6c15",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36854266455",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_SN",
      "config_hash": "ac1b90878c9cef88f0ee4cc435fb2114f94117f35b173e6fe26633601b0e0525",
      "elapsed_seconds": 14405.381870508194,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421004,
      "segment": 3,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_SN",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "28f9fc72f70f22fd3db4add0bc3c459ebb8b75def96a85d3eda2fc9beb6e6052",
          "seed": 422004,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790911878.7736328,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790911785557258272,
        "primary_resume_sha256": "8d9b9366d58eb2d10ff85373f883ac701e7fd3e1aadb8278b3ab22ddf33e1d1f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_SN",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "28f9fc72f70f22fd3db4add0bc3c459ebb8b75def96a85d3eda2fc9beb6e6052",
          "seed": 422004,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897320.232221,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790911785557258272,
        "primary_resume_sha256": "8d9b9366d58eb2d10ff85373f883ac701e7fd3e1aadb8278b3ab22ddf33e1d1f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36940804912",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_SN",
      "config_hash": "e08efd5fc3c2cd4dc0707ac3fa042d8833d8a32a2bb282226bb6ad0603c6a37e",
      "elapsed_seconds": 14408.974584579468,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422004,
      "segment": 4,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "FULL",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "b75ddddab4046459aa88fe45b3a56d3b24fa23d3838047fe8d595f3914a6b54e",
          "seed": 421000,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790853721.6915994,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853630238028698,
        "primary_resume_sha256": "00d26623c43d2807409ac1d0ce1001088b461e6d3298e33561e439d6ce5688fa",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "FULL",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "b75ddddab4046459aa88fe45b3a56d3b24fa23d3838047fe8d595f3914a6b54e",
          "seed": 421000,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790839145.5915728,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853630238028698,
        "primary_resume_sha256": "00d26623c43d2807409ac1d0ce1001088b461e6d3298e33561e439d6ce5688fa",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36829393843",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "FULL",
      "config_hash": "2548689967a5be19c7c883db132efb5560a4ac5feb5f8559985cf5685239cc0a",
      "elapsed_seconds": 11852.813889980316,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "HOSTED_RUNNER_OR_NUMERICAL_SEGMENT_FAILURE",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421000,
      "segment": 3,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": false,
      "worker": null,
      "worker_returncode": 1
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "FULL",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "55d496b1520f47a75bdc4902875e0613134b082cf541715f97539dc69fc8babe",
          "seed": 422000,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790912265.9642646,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912168817874962,
        "primary_resume_sha256": "7f39002276371ad827e827d86e246c05b6461982ecc2c6af1ee0c9b76e7653ac",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "FULL",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "55d496b1520f47a75bdc4902875e0613134b082cf541715f97539dc69fc8babe",
          "seed": 422000,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897709.955853,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912168817874962,
        "primary_resume_sha256": "7f39002276371ad827e827d86e246c05b6461982ecc2c6af1ee0c9b76e7653ac",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36941369164",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "FULL",
      "config_hash": "a052487e92fde9b92f416cda81447ee96d86ab06ad6b3ea1ecb586059fa04d86",
      "elapsed_seconds": 14410.681753873825,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422000,
      "segment": 5,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_DESI_DR2",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "cafba5a4dfd9907664476d4f178f4814ae963ae6919cb495acbf7134f169faae",
          "seed": 422003,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790912145.2418466,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912039038729754,
        "primary_resume_sha256": "08060fb73ec95cb28498dfb3cdba4bb76515230904d01e9e2d062f4f1c5a84d4",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_DESI_DR2",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "cafba5a4dfd9907664476d4f178f4814ae963ae6919cb495acbf7134f169faae",
          "seed": 422003,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897579.1975365,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912039038729754,
        "primary_resume_sha256": "08060fb73ec95cb28498dfb3cdba4bb76515230904d01e9e2d062f4f1c5a84d4",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36941163620",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_DESI_DR2",
      "config_hash": "3976644aa2c978ed0a8f42d00171b8e81a31401f43dc3e2f157a4d654de1d5be",
      "elapsed_seconds": 14412.038119792938,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422003,
      "segment": 4,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "5d1b5bfe9af4935bb724448507cafe778ffd652548a02442cb76cb2516b2bad1",
          "seed": 422102,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1791014010.020201,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791013911304615773,
        "primary_resume_sha256": "40497bfc563f9fa85a09ed3fc9d2cd00db61838d89348f317059da72c5a4e86f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "5d1b5bfe9af4935bb724448507cafe778ffd652548a02442cb76cb2516b2bad1",
          "seed": 422102,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790999413.0613644,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791013911304615773,
        "primary_resume_sha256": "40497bfc563f9fa85a09ed3fc9d2cd00db61838d89348f317059da72c5a4e86f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "37094382151",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_LENSING",
      "config_hash": "a29baf76cbc4af8e85744bd529f912dbb98252e3622d8d9f7f774012369d6c81",
      "elapsed_seconds": 14404.257545471191,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422102,
      "segment": 10,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_PRIMARY",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "412fce5d2aed4e3487ad114ccbb441041034dc101cb9724250ebeee8eda4ff6c",
          "seed": 422101,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1791049063.605754,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791048979351870688,
        "primary_resume_sha256": "2882d99f6d8b1d6b03be22fbd8e210b32da7d011f483476512b8de039f8f6b88",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_PRIMARY",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "412fce5d2aed4e3487ad114ccbb441041034dc101cb9724250ebeee8eda4ff6c",
          "seed": 422101,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897636.1131802,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791048979351870688,
        "primary_resume_sha256": "2882d99f6d8b1d6b03be22fbd8e210b32da7d011f483476512b8de039f8f6b88",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36941264149",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_PRIMARY",
      "config_hash": "ad13c78f8cb4bb427cee1409a7258065bb035e8ad76a0e91f1dc9ebacd788e14",
      "elapsed_seconds": 14406.814023733139,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422101,
      "segment": 4,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "FULL",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "5339d64c41b721982d7ab9bbb75cbb057dc0b10b8ed2fe837950ef3849a7bc6a",
          "seed": 421100,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790926575.0320973,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790926495085738072,
        "primary_resume_sha256": "c30e41c032d805d1b987fa362b77db5ad303a382c33d3a96ece13c86a57ed054",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "FULL",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "5339d64c41b721982d7ab9bbb75cbb057dc0b10b8ed2fe837950ef3849a7bc6a",
          "seed": 421100,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790911984.9910758,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790926495085738072,
        "primary_resume_sha256": "c30e41c032d805d1b987fa362b77db5ad303a382c33d3a96ece13c86a57ed054",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36960394429",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "FULL",
      "config_hash": "7a2fe29c622ea5adcb948e58c7b72cdab5b6436da20b2d360bd661c28ff66593",
      "elapsed_seconds": 14406.108242034912,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421100,
      "segment": 7,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_DESI_DR2",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "a2c29ce81deea9dc34fa8242ba55d26d55b002ee400d41c9a4a64709462bff1e",
          "seed": 422103,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1791019076.4884572,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791018973795392431,
        "primary_resume_sha256": "97218a749f63a75f73e745000781d1a331ccdcdb7dc915d53c89bd02a98cdf9a",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_DESI_DR2",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "a2c29ce81deea9dc34fa8242ba55d26d55b002ee400d41c9a4a64709462bff1e",
          "seed": 422103,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1791004495.7898197,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1791018973795392431,
        "primary_resume_sha256": "97218a749f63a75f73e745000781d1a331ccdcdb7dc915d53c89bd02a98cdf9a",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "37099070675",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_DESI_DR2",
      "config_hash": "d437ebc36807bb80079d593d4c6a998a9b1df338af1093fda2d74654454f3c26",
      "elapsed_seconds": 14415.399819612503,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422103,
      "segment": 10,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_PRIMARY",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "3886853e716ce35b61b341c185c2b375281b8e513f24c2597980842428643bab",
          "seed": 421101,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790853593.9254808,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853489828689392,
        "primary_resume_sha256": "1a4609fab9e93a720d407f0b38bd1b1b7e78a1456369fd10cc3fb66510761041",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_PRIMARY",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "3886853e716ce35b61b341c185c2b375281b8e513f24c2597980842428643bab",
          "seed": 421101,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790838970.8727922,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853489828689392,
        "primary_resume_sha256": "1a4609fab9e93a720d407f0b38bd1b1b7e78a1456369fd10cc3fb66510761041",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36829120607",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_PRIMARY",
      "config_hash": "32d7e24a222e794473f50743d9daae34b2a2f99806ea005e91b85977f17537b0",
      "elapsed_seconds": 14407.648090362549,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421101,
      "segment": 2,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "FULL",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "a21300f6315c28b275e193bfb7922c74f5eef01f6a51bb7f0d3e626f16c0443a",
          "seed": 422100,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790912538.1304553,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912437703884353,
        "primary_resume_sha256": "033f9f56d23f96397151f9a7946c7cace3f89b8cacd1882fdaa4d44e16679d5f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "FULL",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "a21300f6315c28b275e193bfb7922c74f5eef01f6a51bb7f0d3e626f16c0443a",
          "seed": 422100,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897957.622106,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912437703884353,
        "primary_resume_sha256": "033f9f56d23f96397151f9a7946c7cace3f89b8cacd1882fdaa4d44e16679d5f",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36941690978",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "FULL",
      "config_hash": "e09fa5218616769e859ae425e9343bb3372e7872f7808188cb5ca0163c846a76",
      "elapsed_seconds": 14419.315532445908,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422100,
      "segment": 9,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_PRIMARY",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "671b5ced3c591926fd7aab602b36f8c5604b2658f9b096bee032547beb86fb82",
          "seed": 422001,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790883839.792804,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790883729506588376,
        "primary_resume_sha256": "12255ef216641874b2d1ec8fe15f8f06934ff1b6739a84dd67330d473085fb88",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_PRIMARY",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "671b5ced3c591926fd7aab602b36f8c5604b2658f9b096bee032547beb86fb82",
          "seed": 422001,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790869270.131769,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790883729506588376,
        "primary_resume_sha256": "12255ef216641874b2d1ec8fe15f8f06934ff1b6739a84dd67330d473085fb88",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36883723602",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_PRIMARY",
      "config_hash": "4f42d5eba4d706d86447195ad6d06d5b250d4022211e7d93ac2b9310bac950cc",
      "elapsed_seconds": 14404.71167254448,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422001,
      "segment": 3,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_DESI_DR2",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "88f600e713c902526d1cdfd75f59d92a7e5a6dd4f25a365827096f0e3c83c712",
          "seed": 421003,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790853575.9426484,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853468542882352,
        "primary_resume_sha256": "d0fe3b5bf4bab5e459397d201db46cfe640aad7f26cc1fa9b1f178c820cae7dd",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_DESI_DR2",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "88f600e713c902526d1cdfd75f59d92a7e5a6dd4f25a365827096f0e3c83c712",
          "seed": 421003,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790838973.8713796,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790853468542882352,
        "primary_resume_sha256": "d0fe3b5bf4bab5e459397d201db46cfe640aad7f26cc1fa9b1f178c820cae7dd",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36829105261",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_DESI_DR2",
      "config_hash": "1fd26a5f9e748b60a7c9f021e97744ac4f5bab637d898b80e4508a81795ffaee",
      "elapsed_seconds": 14406.430600643158,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421003,
      "segment": 3,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "73f5c046fad45c342a3ea4ce9e1f3602dd26f6d67658f09d9671adfac8ce7bfb",
          "seed": 421102,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790927164.8191123,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790927077422364532,
        "primary_resume_sha256": "6497c243392e2fdaac24140465d0e5c6e4838aea307cee4363653e2eaf59081d",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_LENSING",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "73f5c046fad45c342a3ea4ce9e1f3602dd26f6d67658f09d9671adfac8ce7bfb",
          "seed": 421102,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790912552.4337084,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790927077422364532,
        "primary_resume_sha256": "6497c243392e2fdaac24140465d0e5c6e4838aea307cee4363653e2eaf59081d",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36961060877",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_LENSING",
      "config_hash": "617b6a5732c2ec4e39e546813f587d36489f5d76ec8d00621ed709ffd92798e8",
      "elapsed_seconds": 14410.121268033981,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421102,
      "segment": 7,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "9d8b75a803cbf120c737f012f0cf02d865fe127976c1339580a3cf3d2af62ef7",
          "seed": 422002,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790912334.2030146,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912239396288179,
        "primary_resume_sha256": "4e51e69c3b0a4fc1d972f33e1d0ffb345ed3d079e9fb1921f790cf669fe02926",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_LENSING",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "9d8b75a803cbf120c737f012f0cf02d865fe127976c1339580a3cf3d2af62ef7",
          "seed": 422002,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790897781.5090337,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790912239396288179,
        "primary_resume_sha256": "4e51e69c3b0a4fc1d972f33e1d0ffb345ed3d079e9fb1921f790cf669fe02926",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36941481815",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_LENSING",
      "config_hash": "063ffa73235cd90ad5fb82e4b0a1c4e9d90610d41c898d56c2aaadac1a4b3d0e",
      "elapsed_seconds": 14404.266168117523,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422002,
      "segment": 4,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "adb63f923d928035279204e37e8bb8b2a12ce76cf39706783b3061ffc760a3d4",
          "seed": 421002,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790868627.5342891,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790868540516472447,
        "primary_resume_sha256": "8605b9e0c5173c02c292be45a8a3aa4bb8ff67704a82628ea13fc079f68191e8",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_LENSING",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "adb63f923d928035279204e37e8bb8b2a12ce76cf39706783b3061ffc760a3d4",
          "seed": 421002,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790853529.218666,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790868540516472447,
        "primary_resume_sha256": "8605b9e0c5173c02c292be45a8a3aa4bb8ff67704a82628ea13fc079f68191e8",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36854297282",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_LENSING",
      "config_hash": "798e7bf6bd330454c552277974263def74f273442a8b826c0adce87ce239346a",
      "elapsed_seconds": 14403.509359836578,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421002,
      "segment": 4,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "hillipop",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_SN",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "82a089fca38bbe9af5a2d72defe3146df53d9940b09d2286e61061f50d2f38b2",
          "seed": 422104,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790999711.3250065,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790999613708141833,
        "primary_resume_sha256": "988774895b52acb6d9c0ba9380139c8defa5327a0fe34624ec9caeac9c80179c",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "hillipop",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_SN",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "82a089fca38bbe9af5a2d72defe3146df53d9940b09d2286e61061f50d2f38b2",
          "seed": 422104,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790985150.500494,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790999613708141833,
        "primary_resume_sha256": "988774895b52acb6d9c0ba9380139c8defa5327a0fe34624ec9caeac9c80179c",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "37079411686",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_SN",
      "config_hash": "d2849dfde903cee324dddb725aacff217c6cf07fd8cd466698c14a691b40f357",
      "elapsed_seconds": 14404.52459359169,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 422104,
      "segment": 9,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_DESI_DR2",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "c3845606ad1127978080b347ca1a823ed3e75bd2cf976e4ce872adbe3bf83b92",
          "seed": 421103,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790941190.9072046,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790941094707888744,
        "primary_resume_sha256": "50ff2986838a7eff61dcae4b308f5b0c8eef78bd4e8c76cb03e51ca99f9e6bdf",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_DESI_DR2",
          "model": "ede_n3",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "c3845606ad1127978080b347ca1a823ed3e75bd2cf976e4ce872adbe3bf83b92",
          "seed": 421103,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790926621.183172,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790941094707888744,
        "primary_resume_sha256": "50ff2986838a7eff61dcae4b308f5b0c8eef78bd4e8c76cb03e51ca99f9e6bdf",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36979281216",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_DESI_DR2",
      "config_hash": "e4ba8d6b64716170be364670e100aea6dc4dad9c9b8d3506962d98534a3e9ece",
      "elapsed_seconds": 14407.984654188156,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "ede_n3",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421103,
      "segment": 7,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    },
    {
      "action": "resume",
      "arm": "camspec",
      "case_id": "NOT DOCUMENTED",
      "checkpoint_after": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": false,
          "combination": "NO_ACT_PRIMARY",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "2589c2e693c8ac6c675a99384edf7d8370d52c66b99ed96a5b0efb2465eb306c",
          "seed": 421001,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790838963.9497707,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790838891546199609,
        "primary_resume_sha256": "bbb40d088275c7a72e5940b32ffea9ffe16b718e1396f9ecfdfd326e37143849",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_before": {
        "checkpoint_kind": "STOCK_RESUME",
        "lifecycle": {
          "action": "resume",
          "arm": "camspec",
          "cobaya_partial_resume_adapter_installed": true,
          "combination": "NO_ACT_PRIMARY",
          "model": "lcdm",
          "program_id": "Q042-PROD-V18",
          "q": "Q-042",
          "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
          "resume_input_source": "COBAYA_STORED_UPDATED_INFO",
          "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
          "sampler_contract_sha256": "2589c2e693c8ac6c675a99384edf7d8370d52c66b99ed96a5b0efb2465eb306c",
          "seed": 421001,
          "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
          "started_unix": 1790824416.9865441,
          "status": "STARTED"
        },
        "nonempty_resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "partial_init_accepted": null,
        "partial_init_files": [],
        "partial_init_meta": {},
        "partial_init_meta_files": [],
        "partial_init_nprior": null,
        "primary_resume_mtime_ns": 1790838891546199609,
        "primary_resume_sha256": "bbb40d088275c7a72e5940b32ffea9ffe16b718e1396f9ecfdfd326e37143849",
        "resumable": true,
        "resume_files": [
          "polychord/chain_polychord_raw/chain.resume"
        ],
        "updated_error": null,
        "updated_seed_ok": true,
        "updated_yaml": "polychord/chain.updated.yaml",
        "updated_yaml_nonempty": true
      },
      "checkpoint_parent_run_id": "36809278682",
      "checkpoint_progress": false,
      "checkpoint_progress_reason": "STOCK_RESUME_UNCHANGED",
      "combination": "NO_ACT_PRIMARY",
      "config_hash": "da18ccf41dde508dfb3a63e07db3056c34ac8cea8640566ad18cb45bdb9b6793",
      "elapsed_seconds": 14404.776594877243,
      "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
      "failure_class": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
      "model": "lcdm",
      "mpi_ranks": 1,
      "program_id": "Q042-PROD-V18",
      "q": "Q-042",
      "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
      "resume_lifecycle_ok": true,
      "resume_probe": false,
      "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
      "scientific_spec_origin_program_id": "Q042-PROD-V1",
      "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
      "seed": 421001,
      "segment": 2,
      "soft_minutes": 240,
      "stage": "POLYCHORD_PRODUCTION_FINAL_V18",
      "status": "CONTROLLED_TECHNICAL_FAILURE",
      "technical_parent_execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
      "timed_out": true,
      "worker": null,
      "worker_returncode": -2
    }
  ],
  "downstream_portability_classification": "NOT_AVAILABLE",
  "execution_status": "CONTROLLED_INCOMPLETE",
  "final_result_gate": "UNRESOLVED",
  "gates": {
    "CONVERGENCE": "FAIL",
    "FINAL_RESULT": "UNRESOLVED",
    "GLOBALITY": "PASS",
    "JOB_COMPLETENESS": "PASS",
    "MERGE_COMPATIBILITY": "PASS",
    "NO_NEW_BOBYQA_COMPUTE_V19": "PASS",
    "NO_NEW_POLYCHORD_COMPUTE_V19": "PASS",
    "V18_ARTIFACT_DIGEST_SELECTION_MANIFEST": "PASS",
    "V18_ARTIFACT_SET_COMPLETE": "PASS",
    "V18_BOBYQA_COMPATIBILITY_FILENAME_ADAPTER": "PASS",
    "V18_POLYCHORD_FINAL_FILENAME_ADAPTER": "PASS",
    "V1_SCIENTIFIC_MERGE_CLASSIFICATION_REUSED": "PASS"
  },
  "inherited_v1_downstream_portability_classification": "NOT_AVAILABLE",
  "inherited_v1_final_result_gate": "UNRESOLVED",
  "polychord_recomputed_in_v19": 0,
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "q042_feasibility_classification": "PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED",
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-019",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V19",
  "scientific_contract_changed": false,
  "scientific_spec_origin_program_id": "Q042-PROD-V1",
  "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
  "source_artifact_selection_manifest_sha256": "0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f",
  "source_bobyqa_record_count": 80,
  "source_bobyqa_record_filename": "q042_production_bobyqa_start_v13.json",
  "source_execution_commit": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
  "source_failed_collector_gate": "V13_POLYCHORD_FINAL_COUNT_GATE=FAIL",
  "source_failed_collector_job_id": 111286678009,
  "source_failed_collector_run_id": 37151674348,
  "source_polychord_final_count": 20,
  "source_polychord_final_filename": "q042_production_polychord_final_v18.json",
  "source_program_id": "Q042-PROD-V18",
  "source_result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
  "source_root_github_run_id": 36731879692,
  "source_run_id": "Q042-PRODUCTION-PORTABILITY-V18",
  "stage": "PRODUCTION_FINAL_V19",
  "technical_parent_source_lock_sha256": "6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde",
  "technical_recovery_class": "MERGE_ONLY_EXISTING_V18_ARTIFACTS",
  "tests_status": "COMPLETE"
}
```


## q042_production_artifact_index_v19.json

**Raw member SHA-256:** `202fa0d4e2295f0aa2f10e370f46c9bb15e9a0ee33d870b8bc841ba9bda01f96`; bytes: 488.

```json
{
  "actual_computed_scientific_result": false,
  "artifact_selection_sha256": "0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f",
  "downstream_portability_classification": "NOT_AVAILABLE",
  "final_result_gate": "UNRESOLVED",
  "final_sha256": "95f024b5ffdde740ae796e54a7dbd02340c14f340b7ea935b70082e0ea607e07",
  "merge_run_id": 37185888043,
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "source_program_id": "Q042-PROD-V18",
  "source_root_run_id": 36731879692
}
```


## q042_v18_artifact_selection_v19.json

**Raw member SHA-256:** `0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f`; bytes: 7379.

```json
{
  "artifacts": [
    {
      "candidate_count": 1,
      "digest": "sha256:bd1d255f19a44377db13f5a8bbe69a1f48e4f57e40c0bcef2c5f80afe03022d0",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11105247835,
      "name": "q042-v18-36731879692-bobyqa-import-v1-root-36133813540",
      "workflow_run_id": 36731879692
    },
    {
      "candidate_count": 1,
      "digest": "sha256:a1862aa50f99c445dcdb5ed1c4342ba8cfb52ccc7809d2ac4fda0cab8ee5350e",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11170053204,
      "name": "q042-v18-36731879692-polychord-final-camspec-lcdm-FULL",
      "workflow_run_id": 36854623733
    },
    {
      "candidate_count": 1,
      "digest": "sha256:940f212291f919b949763a80851196485686dcb69fb605964c24bcde27e82c7c",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11156642974,
      "name": "q042-v18-36731879692-polychord-final-camspec-lcdm-NO_ACT_PRIMARY",
      "workflow_run_id": 36829119227
    },
    {
      "candidate_count": 1,
      "digest": "sha256:e31f7c73e21ec572005c0614efb4d0ee27cacb8bc3870d7aece9e761964833e9",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11189001905,
      "name": "q042-v18-36731879692-polychord-final-camspec-lcdm-NO_ACT_LENSING",
      "workflow_run_id": 36883289855
    },
    {
      "candidate_count": 1,
      "digest": "sha256:d5c5cf0f91e25b7da43a69d80f6674445440e6d6bd23d84508b5220ad2f4ad5b",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11171838852,
      "name": "q042-v18-36731879692-polychord-final-camspec-lcdm-NO_DESI_DR2",
      "workflow_run_id": 36854319744
    },
    {
      "candidate_count": 1,
      "digest": "sha256:eb87f925f5d9f1dbd5802bdf2d863354f14055b7dbd5f71b6ea5f29bd24de82d",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11188923253,
      "name": "q042-v18-36731879692-polychord-final-camspec-lcdm-NO_SN",
      "workflow_run_id": 36883349799
    },
    {
      "candidate_count": 1,
      "digest": "sha256:01ac6da88043fbf84fde35713d717cf0b4ea0b53bf5b4d6d13527ada6f563bf6",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11224420078,
      "name": "q042-v18-36731879692-polychord-final-camspec-ede_n3-FULL",
      "workflow_run_id": 36979159417
    },
    {
      "candidate_count": 1,
      "digest": "sha256:2adb1a553b6e18c1bc9cf54b9bc4a2555ba0ec550e770b7aedcf70702272208c",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11171863494,
      "name": "q042-v18-36731879692-polychord-final-camspec-ede_n3-NO_ACT_PRIMARY",
      "workflow_run_id": 36854327437
    },
    {
      "candidate_count": 1,
      "digest": "sha256:0f0b0b423eeb8ad2d529c0bce07612106af83f67781b7b0b9ee0222f37a929a9",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11223599535,
      "name": "q042-v18-36731879692-polychord-final-camspec-ede_n3-NO_ACT_LENSING",
      "workflow_run_id": 36980016743
    },
    {
      "candidate_count": 1,
      "digest": "sha256:777ef6da09c3a41083fd42fdc371d633aecdf3e77a6b545c7c9db68f69413fc4",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11235903511,
      "name": "q042-v18-36731879692-polychord-final-camspec-ede_n3-NO_DESI_DR2",
      "workflow_run_id": 37002008496
    },
    {
      "candidate_count": 1,
      "digest": "sha256:da419877ed58a6e245e75d238b4aff7a0fd338a3fc525aa609cf5cb05db53fbe",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11237041318,
      "name": "q042-v18-36731879692-polychord-final-camspec-ede_n3-NO_SN",
      "workflow_run_id": 37003158762
    },
    {
      "candidate_count": 1,
      "digest": "sha256:03bff43b56ffe00cfde76f8fad49a5909366f3f26769828af37c9584713fa23e",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11214303066,
      "name": "q042-v18-36731879692-polychord-final-hillipop-lcdm-FULL",
      "workflow_run_id": 36960829147
    },
    {
      "candidate_count": 1,
      "digest": "sha256:08123d06abb6c3c9e02da23e103de45f50c419f23eaee925a0facbf0fd1b0538",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11200244000,
      "name": "q042-v18-36731879692-polychord-final-hillipop-lcdm-NO_ACT_PRIMARY",
      "workflow_run_id": 36916112928
    },
    {
      "candidate_count": 1,
      "digest": "sha256:48047a5515ab581c8935abc4a1e3dd82ff774ad78e6dcc4bdb21c0309e1a837c",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11214254864,
      "name": "q042-v18-36731879692-polychord-final-hillipop-lcdm-NO_ACT_LENSING",
      "workflow_run_id": 36960915521
    },
    {
      "candidate_count": 1,
      "digest": "sha256:99519f424b12c3d0c092c3c4dad6f0954e094bcff9de9021809b43e5b60c357c",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11214822062,
      "name": "q042-v18-36731879692-polychord-final-hillipop-lcdm-NO_DESI_DR2",
      "workflow_run_id": 36960666742
    },
    {
      "candidate_count": 1,
      "digest": "sha256:ff07e77b3bcd4d7d8458b7b6e048f1c71ec0837dd55d8a21c2ac38eda4288a7a",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11215140352,
      "name": "q042-v18-36731879692-polychord-final-hillipop-lcdm-NO_SN",
      "workflow_run_id": 36960350503
    },
    {
      "candidate_count": 1,
      "digest": "sha256:b62250bc58f4f2f030e959a668ff418f3ef007b2f6113dd8eeed2a50b5410c38",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11215420441,
      "name": "q042-v18-36731879692-polychord-final-hillipop-ede_n3-FULL",
      "workflow_run_id": 36961119462
    },
    {
      "candidate_count": 1,
      "digest": "sha256:c8e9fa34ca76247e1bdf638b8ef9ecccf8fa22468c1dfdd3d9cbe6ac2fb8090a",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11285856718,
      "name": "q042-v18-36731879692-polychord-final-hillipop-ede_n3-NO_ACT_PRIMARY",
      "workflow_run_id": 36960739114
    },
    {
      "candidate_count": 1,
      "digest": "sha256:1a9f99bd5fac8b6423f453143229928205d4e959cb1b82c20944e39066513b75",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11273293171,
      "name": "q042-v18-36731879692-polychord-final-hillipop-ede_n3-NO_ACT_LENSING",
      "workflow_run_id": 37107682674
    },
    {
      "candidate_count": 1,
      "digest": "sha256:86be15528ee0c86bd117b1d99273762d699198ecb7da3b9f1bb4fd09cf0a6e29",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11274561684,
      "name": "q042-v18-36731879692-polychord-final-hillipop-ede_n3-NO_DESI_DR2",
      "workflow_run_id": 37112407405
    },
    {
      "candidate_count": 1,
      "digest": "sha256:816f567fb5c3298da395a37fa53ae495e53e7bd16628a39150f619f794f5edd7",
      "head_sha": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
      "id": 11268701983,
      "name": "q042-v18-36731879692-polychord-final-hillipop-ede_n3-NO_SN",
      "workflow_run_id": 37094643936
    }
  ],
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "selected_artifact_count": 21,
  "selection_policy": "latest_nonexpired_artifact_id_with_exact_name_and_exact_v18_head_sha",
  "source_execution_commit": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
  "source_program_id": "Q042-PROD-V18",
  "source_root_run_id": 36731879692
}
```


## q042_prod_static_v19.json

**Raw member SHA-256:** `37312818a6bc8cf3f638d8a35f123bc9ec27394b2b858a911adf27f292ffd55b`; bytes: 752.

```json
{
  "gates": {
    "MERGE_ONLY": "PASS",
    "V18_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
    "V18_TECHNICAL_PARENT": "PASS",
    "V1_SCIENTIFIC_SPEC_BYTE_IDENTITY": "PASS",
    "V1_SOURCE_LOCK_BYTE_IDENTITY": "PASS"
  },
  "new_compute": false,
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "required_bobyqa_record_count": 80,
  "required_polychord_final_count": 20,
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-019",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V19",
  "scientific_contract_changed": false,
  "scientific_result": false,
  "source_execution_commit": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
  "source_program_id": "Q042-PROD-V18",
  "source_root_github_run_id": 36731879692,
  "stage": "MERGE_ONLY_STATIC_V19",
  "status": "PASS"
}
```


## q042_prod_static_tests_v19.json

**Raw member SHA-256:** `04a496b8db06b8a4a49f534c583a09e7d5c2da000d48e0764a67e327986d0f6b`; bytes: 1294.

```json
{
  "gate_count": 29,
  "gates": {
    "MERGE_ONLY_RECOVERY": "PASS",
    "NO_CLASSIFIER_CHANGE": "PASS",
    "NO_NEW_BOBYQA": "PASS",
    "NO_NEW_POLYCHORD": "PASS",
    "PROGRAM_CREATES_V1_SHADOWS": "PASS",
    "PROGRAM_DELETES_SHADOWS": "PASS",
    "PROGRAM_EXPOSES_ONLY_STATIC_AND_MERGE": "PASS",
    "PROGRAM_READS_INHERITED_V13_BOBYQA": "PASS",
    "PROGRAM_READS_V18_POLYCHORD_FINALS": "PASS",
    "PROGRAM_REUSES_V1_MERGE": "PASS",
    "PROGRAM_SOURCE_IDENTITY_IS_V18": "PASS",
    "Q_IDENTITY": "PASS",
    "SCIENCE_UNCHANGED": "PASS",
    "V18_FAILURE_EVIDENCE": "PASS",
    "V18_READY_21": "PASS",
    "V18_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
    "V19_LOCK_IDENTITY": "PASS",
    "V19_RECOVERY_IDENTITY": "PASS",
    "V1_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
    "V1_SPEC_BYTE_IDENTITY": "PASS",
    "WORKFLOW_DIGEST_VERIFICATION": "PASS",
    "WORKFLOW_EXPECTS_21_ARTIFACTS": "PASS",
    "WORKFLOW_FROZEN_ROOT": "PASS",
    "WORKFLOW_FROZEN_V18_COMMIT": "PASS",
    "WORKFLOW_MERGE_ONLY_NAME": "PASS",
    "WORKFLOW_NO_BOBYQA_EXECUTION": "PASS",
    "WORKFLOW_NO_POLYCHORD_EXECUTION": "PASS",
    "WORKFLOW_NO_SETUP_RUNTIME": "PASS",
    "WORKFLOW_YAML_PARSE": "PASS"
  },
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "stage": "Q042_PROD_V19_STATIC_TESTS",
  "status": "PASS"
}
```


## q042_production_spec_v1.json

**Raw member SHA-256:** `41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c`; bytes: 9024.

```json
{
  "analysis_preregister": {
    "bobyqa_chi2": "best_chi2 = 2 * minimum finite Py-BOBYQA objective because Cobaya minimize(ignore_prior=True) minimizes -log(likelihood)",
    "globality": "all four external starts must be present; negative/missing results are preserved; at least one finite non-negative result per cell is required for a usable best fit",
    "material_count_coordinates": [
      "H0",
      "fEDE",
      "omega_b",
      "omega_cdm"
    ],
    "no_cross_arm_absolute_objective": true,
    "no_pilot_science": true,
    "no_q040_endpoints": true,
    "overlap_method": "weighted 2D histogram overlap coefficient sum(min(Pij,Qij)) on common frozen-prior bounds in (H0,fEDE)",
    "overlap_primary_bins": [
      80,
      80
    ],
    "overlap_stability_bins": [
      [
        64,
        64
      ],
      [
        96,
        96
      ]
    ],
    "overlap_stability_rule": "if primary and either stability grid fall on different sides of 0.50, contour geometry is UNRESOLVED_NUMERICAL_BINNING and no final scientific class may be emitted",
    "parameter_location_coordinates": [
      "H0",
      "fEDE",
      "omega_b",
      "omega_cdm",
      "log10z_c",
      "thetai_scf"
    ],
    "posterior_summary": "weighted mean and weighted population standard deviation from final nested-sampling weighted samples",
    "primary_geometry_model": "ede_n3",
    "weak_identification_guard": "log10z_c and thetai_scf are reported but never allowed by themselves to trigger parameter-location materiality; conservative implementation of the frozen weak-identification rule."
  },
  "authoritative_contract": {
    "arms": [
      "camspec",
      "hillipop"
    ],
    "data_combinations": {
      "FULL": [
        "P",
        "A6",
        "L6",
        "D2",
        "SN"
      ],
      "NO_ACT_LENSING": [
        "P",
        "A6",
        "D2",
        "SN"
      ],
      "NO_ACT_PRIMARY": [
        "P",
        "L6",
        "D2",
        "SN"
      ],
      "NO_DESI_DR2": [
        "P",
        "A6",
        "L6",
        "SN"
      ],
      "NO_SN": [
        "P",
        "A6",
        "L6",
        "D2"
      ]
    },
    "models": [
      "lcdm",
      "ede_n3"
    ],
    "no_cross_arm_absolute_chi2_evidence": true,
    "no_hybrid_planck_likelihood": true,
    "q040_scientific_endpoints_forbidden": true,
    "reporting_coordinates": [
      "H0",
      "fEDE",
      "log10z_c",
      "thetai_scf",
      "omega_b",
      "omega_cdm"
    ],
    "required_cell_count": 20,
    "same_external_data_both_planck_arms": true
  },
  "bobyqa_production": {
    "cobaya_best_of": 1,
    "external_starts_per_cell": 4,
    "globality_gate": "within each arm/model/data cell, retain the best finite likelihood minimum only after all four external starts complete; negative Py-BOBYQA linear-algebra/input flags fail that start and must be preserved",
    "ignore_prior": true,
    "max_evals": "120d",
    "rhoend": 0.05,
    "start_rule": "start 0 = frozen Q032 parent reference; starts 1-3 = deterministic bounded signed perturbations of sampled coordinates using 0.08, 0.14 and 0.20 of each finite prior span, clipped 5 percent inside hard bounds; EDE sector remains n=3; no internal multi-start layer"
  },
  "case_id": "NOT DOCUMENTED",
  "controlled_nonresult_classes": [
    "CONTROLLED_NO_SCIENTIFIC_RESULT",
    "PRODUCTION_INCOMPLETE_OR_NUMERICALLY_UNRESOLVED"
  ],
  "created_date": "2026-09-25",
  "final_classes": [
    "MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE",
    "SCIENTIFIC_DIFFERENCE_COLLAPSES",
    "MIXED_DATASET_CONDITIONAL"
  ],
  "orchestration": {
    "artifact_campaign_namespace": "root GitHub run id",
    "bobyqa_atomicity": "one external start per job; optimizer settings are not split or altered",
    "collector_checks_per_run": 5,
    "collector_sleep_minutes": 45,
    "github_hosted_job_hard_limit_minutes": 360,
    "github_job_limit_source": "https://docs.github.com/en/actions/reference/limits",
    "github_limits_verified_date": "2026-09-25",
    "github_workflow_run_limit_days": 35,
    "job_timeout_minutes": 330,
    "max_collector_rounds": 80,
    "max_polychord_segments_per_cell": 48,
    "segment_behavior": "fresh segment 0; later segments resume exact transferred Cobaya/PolyChord state in a fresh interpreter/MPI lifecycle",
    "soft_polychord_segment_minutes": 240
  },
  "original_decision_rule": {
    "combination_materiality": "material if model-preference portability is material OR both parameter-location and contour geometry are material",
    "contour_overlap": {
      "coordinates": [
        "H0",
        "fEDE"
      ],
      "material_if": "overlap_coefficient<0.50",
      "method": "empirical weighted two-dimensional posterior/profile overlap; no Gaussian compression",
      "substantial_if": "overlap_coefficient>=0.50"
    },
    "final_classification": {
      "MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE": "FULL material AND materiality survives every required valid leave-one-out test",
      "MIXED_DATASET_CONDITIONAL": "at least one valid required combination is material and at least one valid required combination is non-material",
      "SCIENTIFIC_DIFFERENCE_COLLAPSES": "FULL and every valid leave-one-out are non-material in parameter location, have substantial contour overlap, and have portable EDE/LCDM conclusions"
    },
    "model_preference": {
      "categories": {
        "modest": "2<DeltaChi2<6",
        "negligible": "DeltaChi2<=2",
        "substantive": "DeltaChi2>=6"
      },
      "formula": "DeltaChi2_EDE_arm=Chi2_LCDM_best_arm-Chi2_EDE_best_arm",
      "portability_material_if": "arms occupy different categories AND abs(DeltaChi2_A-DeltaChi2_B)>=2",
      "within_arm_only": true
    },
    "parameter_location": {
      "formula": "D_x=abs(x_A-x_B)/sqrt(sigma_A^2+sigma_B^2)",
      "material_if": "D_H0>=1 OR D_fEDE>=1 OR at least two eligible primary cosmological coordinates have D>=1",
      "weak_identification_rule": "log10z_c and thetai_scf cannot by themselves make parameter-location material when fEDE is weakly identified/prior dominated."
    }
  },
  "polychord_production": {
    "boost_posterior": 0,
    "confidence_for_unbounded": 0.9999995,
    "do_clustering": true,
    "max_ndead": "infinity",
    "max_ndead_runtime_encoding": "Python float(\"inf\") passed to Cobaya 3.5.6; preserves frozen semantic max_ndead=infinity without changing the numerical stopping contract",
    "measure_speeds": true,
    "nfail": "nlive",
    "nlive": "25d",
    "nprior": "10nlive",
    "num_repeats": "5d",
    "oversample_power": 0.4,
    "precision_criterion": 0.001,
    "read_resume": true,
    "seed_policy": "deterministic unique seed per arm/model/combination; exact seeds generated and frozen in the production program before any production result is inspected",
    "synchronous": true,
    "write_dead": true,
    "write_live": true,
    "write_prior": true,
    "write_resume": true,
    "write_stats": true
  },
  "polychord_seed_map": {
    "camspec:ede_n3:FULL": 421100,
    "camspec:ede_n3:NO_ACT_LENSING": 421102,
    "camspec:ede_n3:NO_ACT_PRIMARY": 421101,
    "camspec:ede_n3:NO_DESI_DR2": 421103,
    "camspec:ede_n3:NO_SN": 421104,
    "camspec:lcdm:FULL": 421000,
    "camspec:lcdm:NO_ACT_LENSING": 421002,
    "camspec:lcdm:NO_ACT_PRIMARY": 421001,
    "camspec:lcdm:NO_DESI_DR2": 421003,
    "camspec:lcdm:NO_SN": 421004,
    "hillipop:ede_n3:FULL": 422100,
    "hillipop:ede_n3:NO_ACT_LENSING": 422102,
    "hillipop:ede_n3:NO_ACT_PRIMARY": 422101,
    "hillipop:ede_n3:NO_DESI_DR2": 422103,
    "hillipop:ede_n3:NO_SN": 422104,
    "hillipop:lcdm:FULL": 422000,
    "hillipop:lcdm:NO_ACT_LENSING": 422002,
    "hillipop:lcdm:NO_ACT_PRIMARY": 422001,
    "hillipop:lcdm:NO_DESI_DR2": 422003,
    "hillipop:lcdm:NO_SN": 422004
  },
  "preflight_authority": {
    "artifact": "q042-preflight-final-v11",
    "final_result_gate": "PREFLIGHT_PASS",
    "program_id": "Q042-PREFLIGHT-V11",
    "program_sha256": "3dd736334f355d9f5e2232c2900c563587e8330413185fd9f897193c66f46f32",
    "result_id": "R-Q042-POLYCHORD-BOBYQA-PREFLIGHT-011",
    "spec_sha256": "183139bf7bab9dcf1bf0e591762dbb1ddb4160244065a400709e2522d3241ebe"
  },
  "program_id": "Q042-PROD-V1",
  "q": "Q-042",
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V1",
  "scientific_question": "Kan den oprindelige Q041 downstream-portabilitetstest udf\u00f8res med en ny pr\u00e6registreret, konvergensrobust inference-strategi, der n\u00f8jagtigt bevarer den oprindelige scientific contract \u2014 begge native Planck-arme, \u039bCDM og n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, \u00e9n identisk frozen supernova-likelihood, FULL + fire leave-one-out-tests og de oprindelige materialitets-/modelpr\u00e6ferenceregler \u2014 uden at genbruge Q040's invaliderede science-endpoints, uden cross-arm absolute objective arithmetic og uden retroaktivt at \u00e6ndre kriterier efter resultaterne?",
  "status": "PREREGISTERED_PRODUCTION"
}
```


## q042_production_recovery_v19.json

**Raw member SHA-256:** `d9d82270f44b26b0e46ea0a181704ebf97629c1f213c4def2b9893ac97a84d4b`; bytes: 2389.

```json
{
  "authoritative_scientific_spec": {
    "file": "q042_production_spec_v1.json",
    "program_id": "Q042-PROD-V1",
    "sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
  },
  "case_id": "NOT DOCUMENTED",
  "created_date": "2026-10-04",
  "finalization": {
    "fail_closed": true,
    "required_source_bobyqa_records": 80,
    "required_source_polychord_finals": 20,
    "result_artifact": "q042-production-final-v19",
    "reuse_frozen_v1_scientific_merge_and_classification_logic": true
  },
  "observed_v18_failure": {
    "collector_job_id": 111286678009,
    "collector_readiness": {
      "expected": 21,
      "found": 21,
      "ready": true
    },
    "collector_run_id": 37151674348,
    "failed_gate": "V13_POLYCHORD_FINAL_COUNT_GATE=FAIL",
    "root_cause": "V18 merge_final still searches q042_production_polychord_final_v13.json even though V18 production artifacts contain q042_production_polychord_final_v18.json.",
    "root_run_id": 36731879692
  },
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "recovery_class": "MERGE_ONLY_EXISTING_V18_ARTIFACTS",
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-019",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V19",
  "scientific_contract_changed": false,
  "source_artifacts": {
    "bobyqa_import_artifact_count": 1,
    "bobyqa_record_count": 80,
    "expected_count": 21,
    "polychord_final_count": 20,
    "required_execution_commit": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
    "root_namespace": 36731879692,
    "selection_policy": "latest nonexpired exact-name artifact with exact V18 head SHA; ZIP digest verified before extraction"
  },
  "supersedes": "Q042-PROD-V18",
  "technical_change_v19": {
    "change": "Finalization-only filename adapter. Discover and digest-verify the completed V18 artifact set, create temporary V1 compatibility filenames for V18 PolyChord finals and inherited V13-named BOBYQA records, call q042_production_v1.merge_final unchanged, delete shadows, then relabel only the final technical envelope as V19.",
    "classification_rules_changed": false,
    "cross_arm_absolute_objective_added": false,
    "new_bobyqa_compute": false,
    "new_polychord_compute": false,
    "polychord_settings_changed": false,
    "q040_endpoints_reused": false,
    "scientific_contract_changed": false,
    "seed_map_changed": false,
    "thresholds_changed": false
  }
}
```


## q042_production_source_lock_v19.json

**Raw member SHA-256:** `b5367385fd96ccd07db17dcd74f6bbd5a14e1f4c4cc7783abea4554eee02fa3b`; bytes: 2662.

```json
{
  "case_id": "NOT DOCUMENTED",
  "created_date": "2026-10-04",
  "hard_rules": {
    "github_mutation_by_assistant_forbidden": true,
    "no_cross_arm_absolute_objective_evidence": true,
    "no_retroactive_threshold_changes": true,
    "pilot_outputs_forbidden_as_science": true,
    "q040_scientific_endpoints_forbidden": true
  },
  "program_id": "Q042-PROD-V19",
  "q": "Q-042",
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-019",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V19",
  "scientific_parent_source_lock_file": "q042_production_source_lock_v1.json",
  "scientific_parent_source_lock_sha256": "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56",
  "scientific_spec_file": "q042_production_spec_v1.json",
  "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
  "technical_parent": {
    "execution_commit": "d0f92c7f2ce53da32818244f8847f8e745e20c4f",
    "failed_collector_job_id": 111286678009,
    "failed_collector_run_id": 37151674348,
    "failed_gate": "V13_POLYCHORD_FINAL_COUNT_GATE=FAIL",
    "production_program_sha256": "19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962",
    "program_id": "Q042-PROD-V18",
    "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
    "root_github_run_id": 36731879692,
    "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
    "workflow_sha256": "95ecae46549732f6fc1263a5d0116590ca784104bc11894a279a8cce4a175a5c"
  },
  "technical_parent_source_lock_file": "q042_production_source_lock_v18.json",
  "technical_parent_source_lock_sha256": "6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde",
  "technical_repair": {
    "bobyqa_recomputed": false,
    "bobyqa_source_filename": "q042_production_bobyqa_start_v13.json",
    "classification_rules_changed": false,
    "compatibility_shadow_filename_bobyqa": "q042_production_bobyqa_start_v1.json",
    "compatibility_shadow_filename_polychord": "q042_production_polychord_final_v1.json",
    "polychord_recomputed": false,
    "recovery_class": "MERGE_ONLY_EXISTING_V18_ARTIFACTS",
    "scientific_contract_changed": false,
    "scientific_merge_implementation": "q042_production_v1.merge_final",
    "scientific_setting_changed": false,
    "source_artifact_count": 21,
    "source_bobyqa_record_count": 80,
    "source_collector_evidence": {
      "expected": 21,
      "found": 21,
      "job_id": 111286678009,
      "ready": "yes",
      "run_id": 37151674348
    },
    "source_polychord_filename": "q042_production_polychord_final_v18.json",
    "source_polychord_final_count": 20,
    "stale_v18_merge_expected_filename": "q042_production_polychord_final_v13.json"
  }
}
```


## APPENDIX C — COMPLETE RETRIEVED V18 TECHNICAL-HISTORY SOURCE LOCK

**Preserved UTF-8 source SHA-256:** `6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde`; bytes: 12997.

```json
{
  "case_id": "NOT DOCUMENTED",
  "created_date": "2026-09-30",
  "deployment_parent": {
    "failure_class": "COBAYA_PARTIAL_INIT_RESUME_DETECTION_CLEANUP_RESTART",
    "failure_scope": "V17 s0 checkpoint recorded accepted=900/nprior=6500. V17 relay s1 then logged Cobaya cleanup/start-new before PolyChord invocation, so the partial checkpoint was not consumed and the 240-minute segment ended RESUME_NO_CHECKPOINT_PROGRESS.",
    "program_id": "Q042-PROD-V17"
  },
  "external": {
    "act_dr6_lensing_commit": "b386ddbb5821c1216c709f051c9289292f174d30",
    "act_dr6_primary_commit": "880eacb40d66722eb1c32d7b5621e91662b4d808",
    "desi_dr2_bao_data_commit": "b7b8a36e9bccb063081f811f323cada21ab5fbdd",
    "desi_dr2_cobaya_definition_commit": "b76b6fed2a6c8c5594c6f92d5058bef10079746a",
    "supernova_component": "sn.pantheonplus",
    "supernova_runtime_file_hash_manifest_required": true
  },
  "hard_rules": {
    "github_mutation_by_assistant_forbidden": true,
    "no_cross_arm_absolute_objective_evidence": true,
    "no_retroactive_threshold_changes": true,
    "pilot_outputs_forbidden_as_science": true,
    "q040_scientific_endpoints_forbidden": true
  },
  "parent_source_lock_file": "q042_production_source_lock_v1.json",
  "parent_source_lock_sha256": "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56",
  "program_id": "Q042-PROD-V18",
  "q": "Q-042",
  "q032": {
    "execution_commit": "4dc873a5e880d40858d831a3b421456728f0c032",
    "github_run_id": 33994305721,
    "result_id": "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
  },
  "result_id": "R-Q042-PRODUCTION-PORTABILITY-018",
  "run_id": "Q042-PRODUCTION-PORTABILITY-V18",
  "scientific_spec_file": "q042_production_spec_v1.json",
  "scientific_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
  "software": {
    "class_ede_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "cobaya_version": "3.5.6",
    "hillipop_commit": "a09ddde3e7ce11df99f74685feb1f1764cafb251",
    "numpy_version": "1.26.4",
    "polychordlite_exact_commit": "3ade6445bb3719a6db6f6e81f178765545ffc833",
    "polychordlite_release_tag": "1.22.2",
    "pybobyqa_version": "1.5.0",
    "python_version": "3.11"
  },
  "technical_parent": {
    "execution_commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
    "production_program_sha256": "889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642",
    "program_id": "Q042-PROD-V1",
    "result_id": "R-Q042-PRODUCTION-PORTABILITY-001",
    "root_github_run_id": 36133813540,
    "run_id": "Q042-PRODUCTION-PORTABILITY-V1",
    "runtime_artifact_digest": "sha256:162b99026d025d1021fa8a83dbf4290b7bd0c2c53917ea56cbf04f8b169bff4a",
    "runtime_artifact_id": 10862038917,
    "runtime_artifact_name": "q042-prod-36133813540-environment"
  },
  "technical_repair": {
    "bobyqa_recomputed": false,
    "removed_from_executable_polychord_options_only": [
      "seed_policy",
      "max_ndead_runtime_encoding"
    ],
    "retained_in_authoritative_scientific_spec": [
      "seed_policy",
      "max_ndead_runtime_encoding"
    ],
    "scientific_setting_changed": false,
    "v11_runtime_adapter_test_harness_repair": {
      "change": "Add the runtime-adapter subcommand required by the workflow and validate its PASS output before production dispatch.",
      "classification_rules_changed": false,
      "execution_patch_changed": false,
      "polychord_scientific_settings_changed": false,
      "scientific_setting_changed": false,
      "seed_map_changed": false
    },
    "v12_nested_anchor_repair": {
      "anchor_match_cardinality_required": 1,
      "base_polychord_commit": "3ade6445bb3719a6db6f6e81f178765545ffc833",
      "change": "Replace two nested_sampling.F90 exact-whitespace anchors with constrained unique regex anchors.",
      "checkpoint_format_changed": false,
      "classification_rules_changed": false,
      "execution_semantics_changed": false,
      "expected_upstream_import": "use generate_module,   only: GenerateSeed,GenerateLivePoints",
      "failed_v11_gate": "NESTED_IMPORT_GATE expected_one_anchor got=0",
      "polychord_scientific_settings_changed": false,
      "scientific_setting_changed": false,
      "seed_map_changed": false
    },
    "v12_partial_initialization_checkpoint": {
      "base_polychord_commit": "3ade6445bb3719a6db6f6e81f178765545ffc833",
      "checkpoint_interval_accepted_points": 25,
      "inherited_byte_for_byte_from": "Q042-PROD-V11 execution semantics; anchor matcher repaired only",
      "paid_hpc_required": false,
      "patcher_file": "q042_patch_polychord_partial_init_v12.py",
      "patcher_sha256": "6c4bd61fb535ab05281011ec701d0444942424f3d09b34661c7659616140ae6d",
      "requires_exact_resume_byte_identity_selftest": true,
      "scientific_setting_changed": false,
      "selftest_file": "q042_polychord_partial_init_selftest_v12.py",
      "selftest_sha256": "d11a05d9571b98edbe39c679112c527d6d50b23999dbb49e370168c0a2f4a076",
      "serial_only": true
    },
    "v13_forced_relink_repair": {
      "base_polychord_commit": "3ade6445bb3719a6db6f6e81f178765545ffc833",
      "change": "Deployment-only build repair: explicitly remove stale libchord targets, clean src/polychord objects, relink the pinned PolyChordLite shared library, and require patch symbols in the linked binary before self-test.",
      "checkpoint_format_changed": false,
      "classification_rules_changed": false,
      "execution_patch_semantics_changed": false,
      "failed_v12_gate": "PARTIAL_INIT_SELFTEST_EARLY_EXIT_GATE=FAIL",
      "linked_binary_symbol_gate": true,
      "observed_v12_build_message": "make: Nothing to be done for libchord.so.",
      "patcher_file": "q042_patch_polychord_partial_init_v13.py",
      "patcher_sha256": "22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6",
      "polychord_scientific_settings_changed": false,
      "scientific_setting_changed": false,
      "seed_map_changed": false,
      "selftest_file": "q042_polychord_partial_init_selftest_v13.py",
      "selftest_sha256": "7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462",
      "serial_only": true,
      "standard_github_runner": "ubuntu-24.04"
    },
    "v16_canary_relay_repair": {
      "change": "Replace 10-minute disposable canary resume probe with real 240-minute segment 1; require semantic checkpoint progress or completion before fan-out.",
      "checkpoint_format_changed": false,
      "checkpoint_interval_accepted_points": 25,
      "classification_rules_changed": false,
      "failed_v15_status": "RESUME_PROBE_NO_PROGRESS",
      "observed_v15_interrupt_location": "CLASS compute during resumed PolyChord likelihood evaluation",
      "polychord_scientific_settings_changed": false,
      "scientific_setting_changed": false,
      "seed_map_changed": false
    },
    "v16_runtime_manifest_hash_alignment_and_relay_progress": {
      "change": "Deployment-only recovery: align executable runtime gate with the exact V13 patcher/selftest hashes already emitted by the V13 setup, and require semantic checkpoint progress across GitHub relay segments.",
      "checkpoint_format_changed": false,
      "checkpoint_interval_accepted_points": 25,
      "execution_patch_semantics_changed": false,
      "failed_v13_gate": "PARTIAL_INIT_RUNTIME_CONTENT_GATE=FAIL",
      "github_job_timeout_minutes": 330,
      "observed_v13_mismatch": {
        "program_expected_patcher_sha256": "b8dc1fe134f69068fb5a1c97044b4bb5910b93320156acae009b76135a3f9136",
        "program_expected_selftest_sha256": "7f103dd2fd7a6f5575af4de43e8102d3b99893abaf16ee2ea1973a8780de7a69",
        "runtime_manifest_patcher_sha256": "22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6",
        "runtime_manifest_selftest_sha256": "7d7a3544b8e9880527e87be6a020e950d7a20d0bdfb1b718b680863af2236462"
      },
      "partial_init_progress_rule": "accepted_after > accepted_before",
      "partial_to_stock_resume_progress": true,
      "polychord_scientific_settings_changed": false,
      "relay_soft_segment_minutes": 240,
      "scientific_setting_changed": false,
      "seed_map_changed": false,
      "serial_only": true,
      "standard_github_runner": "ubuntu-24.04",
      "stock_resume_progress_rule": "resume sha256 or mtime must change"
    },
    "v17_selftest_capture_and_matrix_isolation_repair": {
      "change": "Deployment-only test-harness repair: keep the V13 PolyChord patch/checkpoint format unchanged; slow the synthetic capture worker, require both atomically-renamed meta and binary checkpoint files, freeze with SIGSTOP before teardown, kill only after frozen-file verification, retry capture up to three times, and set the production fan-out matrix fail-fast policy to false so one setup flake cannot cancel independent cells.",
      "checkpoint_format_changed": false,
      "classification_rules_changed": false,
      "execution_patch_semantics_changed": false,
      "fanout_fail_fast": false,
      "observed_v16_failed_gate": "PARTIAL_INIT_SELFTEST_BINARY_GATE=FAIL",
      "observed_v16_failed_job_id": 109445325348,
      "observed_v16_root_run_id": 36528427653,
      "patcher_file": "q042_patch_polychord_partial_init_v13.py",
      "patcher_sha256": "22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6",
      "polychord_scientific_settings_changed": false,
      "production_relay_semantics_changed": false,
      "scientific_setting_changed": false,
      "seed_map_changed": false,
      "selftest_capture_attempts": 3,
      "selftest_capture_method": "ATOMIC_META_AND_BINARY_DETECT_SIGSTOP_THEN_SIGKILL",
      "selftest_capture_sleep_seconds": 0.25,
      "selftest_file": "q042_polychord_partial_init_selftest_v17.py",
      "selftest_sha256": "1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9",
      "standard_github_runner": "ubuntu-24.04",
      "v16_canary_relay_segment1_success": true,
      "v16_canary_segment0_success": true
    },
    "v18_cobaya_partial_resume_detection_adapter": {
      "adapter_file": "q042_cobaya_partial_resume_adapter_v18.py",
      "adapter_sha256": "b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567",
      "change": "Recognize <prefix>.partial_init as a minimal Cobaya PolyChord resume marker while leaving the stock <prefix>.resume marker and normal output deletion patterns intact.",
      "checkpoint_contents_changed": false,
      "checkpoint_format_changed": false,
      "checkpoint_interval_accepted_points": 25,
      "checkpoint_interval_changed": false,
      "classification_rules_changed": false,
      "cobaya_version": "3.5.6",
      "execution_patch_semantics_changed": false,
      "inherited_patcher_sha256": "22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6",
      "inherited_selftest_sha256": "1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9",
      "observed_v17_nprior": 6500,
      "observed_v17_partial_accepted": 900,
      "observed_v17_relay_job_id": 109827789054,
      "observed_v17_root_run_id": 36673568849,
      "polychord_scientific_settings_changed": false,
      "relay_soft_minutes": 240,
      "scientific_setting_changed": false,
      "seed_map_changed": false,
      "standard_github_runner": "ubuntu-24.04"
    },
    "v1_bobyqa_source_artifacts_reused": 80,
    "v3_dependency_repair": {
      "job": "import-bobyqa",
      "packages": [
        "PyYAML==6.0.2",
        "numpy==1.26.4"
      ],
      "scientific_setting_changed": false
    },
    "v4_version_integrity_repair": {
      "preserves_v3_import_bobyqa_dependency_fix": true,
      "scientific_setting_changed": false,
      "scope": "recovery-owned version labels/file expectations/tests/workflow artifacts only"
    },
    "v5_registry_parent_test_repair": {
      "preserves_v3_import_bobyqa_dependency_fix": true,
      "preserves_v4_version_integrity_repair": true,
      "scientific_setting_changed": false,
      "scope": "static test lineage assertion only"
    },
    "v6_reduced_environment_regeneration": {
      "direct_v1_reduced_meta_reuse": false,
      "required_equivalence_fields": [
        "support_sha256",
        "parent_q032_support_sha256",
        "restricted_precision_sha256",
        "parent_q032_precision_sha256",
        "final_semantics",
        "scientific_semantics",
        "canonical_common_keys",
        "selected_keys_native_order"
      ],
      "scientific_setting_changed": false,
      "source": "same frozen Q032 commit/artifacts used by V1"
    },
    "v8_parent_matrix_adoption_and_canary": {
      "canary_cell": "hillipop:ede_n3:FULL",
      "fanout_requires_resume_probe": true,
      "fresh_checkpoint_window_minutes": 315,
      "matrix_recomputed": false,
      "parent_program_id": "Q042-PROD-V1",
      "required_parent_restricted_precision_sha256": "ad0328d766380f89e2bd39eef607056b587de3ae828ebd86632a05a9bffb0424",
      "resume_probe_minutes": 10,
      "scientific_setting_changed": false
    }
  }
}
```


## APPENDIX D1 — RETRIEVED V19 MERGE RUN METADATA

**Preserved UTF-8 source SHA-256:** `22a6c753863fc4989789cdd517486b57de74e1b10b1ba681b823c354b3951069`; bytes: 13803.

```json
{
  "id": 37185888043,
  "name": "Bubbleverse Q042 Production V19 — merge-only recovery",
  "node_id": "WFR_kwLOUFxv0M8AAAAIqHOfKw",
  "head_branch": "main",
  "head_sha": "7af1298c5f1db17557d7671d2ea38ca6d67b7df1",
  "path": ".github/workflows/q042-production-v19.yml",
  "display_title": "Bubbleverse Q042 Production V19 — merge-only recovery",
  "run_number": 1,
  "event": "workflow_dispatch",
  "status": "completed",
  "conclusion": "success",
  "workflow_id": 374437077,
  "check_suite_id": 100724099172,
  "check_suite_node_id": "CS_kwDOUFxv0M8AAAAXc5_IZA",
  "url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043",
  "html_url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37185888043",
  "pull_requests": [],
  "created_at": "2026-10-04T07:28:30Z",
  "updated_at": "2026-10-04T07:29:04Z",
  "actor": {
    "login": "Morfindien",
    "id": 66628138,
    "node_id": "MDQ6VXNlcjY2NjI4MTM4",
    "avatar_url": "https://avatars.githubusercontent.com/u/66628138?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/Morfindien",
    "html_url": "https://github.com/Morfindien",
    "followers_url": "https://api.github.com/users/Morfindien/followers",
    "following_url": "https://api.github.com/users/Morfindien/following{/other_user}",
    "gists_url": "https://api.github.com/users/Morfindien/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Morfindien/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Morfindien/subscriptions",
    "organizations_url": "https://api.github.com/users/Morfindien/orgs",
    "repos_url": "https://api.github.com/users/Morfindien/repos",
    "events_url": "https://api.github.com/users/Morfindien/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Morfindien/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "run_attempt": 1,
  "referenced_workflows": [],
  "run_started_at": "2026-10-04T07:28:30Z",
  "triggering_actor": {
    "login": "Morfindien",
    "id": 66628138,
    "node_id": "MDQ6VXNlcjY2NjI4MTM4",
    "avatar_url": "https://avatars.githubusercontent.com/u/66628138?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/Morfindien",
    "html_url": "https://github.com/Morfindien",
    "followers_url": "https://api.github.com/users/Morfindien/followers",
    "following_url": "https://api.github.com/users/Morfindien/following{/other_user}",
    "gists_url": "https://api.github.com/users/Morfindien/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Morfindien/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Morfindien/subscriptions",
    "organizations_url": "https://api.github.com/users/Morfindien/orgs",
    "repos_url": "https://api.github.com/users/Morfindien/repos",
    "events_url": "https://api.github.com/users/Morfindien/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Morfindien/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "jobs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043/jobs",
  "logs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043/logs",
  "check_suite_url": "https://api.github.com/repos/Morfindien/Bubbleverse/check-suites/100724099172",
  "artifacts_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043/artifacts",
  "cancel_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043/cancel",
  "rerun_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/runs/37185888043/rerun",
  "previous_attempt_url": null,
  "workflow_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/workflows/374437077",
  "head_commit": {
    "id": "7af1298c5f1db17557d7671d2ea38ca6d67b7df1",
    "tree_id": "a9939494d18eeec4b114e87c7a979638609c4ecd",
    "message": "Rename q042-production-v19.yml to .github/workflows/q042-production-v19.yml",
    "timestamp": "2026-10-04T07:28:01Z",
    "author": {
      "name": "Jim Pedersen",
      "email": "66628138+Morfindien@users.noreply.github.com"
    },
    "committer": {
      "name": "GitHub",
      "email": "noreply@github.com"
    }
  },
  "repository": {
    "id": 1348235216,
    "node_id": "R_kgDOUFxv0A",
    "name": "Bubbleverse",
    "full_name": "Morfindien/Bubbleverse",
    "private": false,
    "owner": {
      "login": "Morfindien",
      "id": 66628138,
      "node_id": "MDQ6VXNlcjY2NjI4MTM4",
      "avatar_url": "https://avatars.githubusercontent.com/u/66628138?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Morfindien",
      "html_url": "https://github.com/Morfindien",
      "followers_url": "https://api.github.com/users/Morfindien/followers",
      "following_url": "https://api.github.com/users/Morfindien/following{/other_user}",
      "gists_url": "https://api.github.com/users/Morfindien/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/Morfindien/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/Morfindien/subscriptions",
      "organizations_url": "https://api.github.com/users/Morfindien/orgs",
      "repos_url": "https://api.github.com/users/Morfindien/repos",
      "events_url": "https://api.github.com/users/Morfindien/events{/privacy}",
      "received_events_url": "https://api.github.com/users/Morfindien/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "html_url": "https://github.com/Morfindien/Bubbleverse",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/Morfindien/Bubbleverse",
    "forks_url": "https://api.github.com/repos/Morfindien/Bubbleverse/forks",
    "keys_url": "https://api.github.com/repos/Morfindien/Bubbleverse/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/Morfindien/Bubbleverse/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/Morfindien/Bubbleverse/teams",
    "hooks_url": "https://api.github.com/repos/Morfindien/Bubbleverse/hooks",
    "issue_events_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues/events{/number}",
    "events_url": "https://api.github.com/repos/Morfindien/Bubbleverse/events",
    "assignees_url": "https://api.github.com/repos/Morfindien/Bubbleverse/assignees{/user}",
    "branches_url": "https://api.github.com/repos/Morfindien/Bubbleverse/branches{/branch}",
    "tags_url": "https://api.github.com/repos/Morfindien/Bubbleverse/tags",
    "blobs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/Morfindien/Bubbleverse/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/Morfindien/Bubbleverse/languages",
    "stargazers_url": "https://api.github.com/repos/Morfindien/Bubbleverse/stargazers",
    "contributors_url": "https://api.github.com/repos/Morfindien/Bubbleverse/contributors",
    "subscribers_url": "https://api.github.com/repos/Morfindien/Bubbleverse/subscribers",
    "subscription_url": "https://api.github.com/repos/Morfindien/Bubbleverse/subscription",
    "commits_url": "https://api.github.com/repos/Morfindien/Bubbleverse/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/Morfindien/Bubbleverse/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/Morfindien/Bubbleverse/contents/{+path}",
    "compare_url": "https://api.github.com/repos/Morfindien/Bubbleverse/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/Morfindien/Bubbleverse/merges",
    "archive_url": "https://api.github.com/repos/Morfindien/Bubbleverse/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/Morfindien/Bubbleverse/downloads",
    "issues_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues{/number}",
    "pulls_url": "https://api.github.com/repos/Morfindien/Bubbleverse/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/Morfindien/Bubbleverse/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/Morfindien/Bubbleverse/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/Morfindien/Bubbleverse/labels{/name}",
    "releases_url": "https://api.github.com/repos/Morfindien/Bubbleverse/releases{/id}",
    "deployments_url": "https://api.github.com/repos/Morfindien/Bubbleverse/deployments"
  },
  "head_repository": {
    "id": 1348235216,
    "node_id": "R_kgDOUFxv0A",
    "name": "Bubbleverse",
    "full_name": "Morfindien/Bubbleverse",
    "private": false,
    "owner": {
      "login": "Morfindien",
      "id": 66628138,
      "node_id": "MDQ6VXNlcjY2NjI4MTM4",
      "avatar_url": "https://avatars.githubusercontent.com/u/66628138?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Morfindien",
      "html_url": "https://github.com/Morfindien",
      "followers_url": "https://api.github.com/users/Morfindien/followers",
      "following_url": "https://api.github.com/users/Morfindien/following{/other_user}",
      "gists_url": "https://api.github.com/users/Morfindien/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/Morfindien/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/Morfindien/subscriptions",
      "organizations_url": "https://api.github.com/users/Morfindien/orgs",
      "repos_url": "https://api.github.com/users/Morfindien/repos",
      "events_url": "https://api.github.com/users/Morfindien/events{/privacy}",
      "received_events_url": "https://api.github.com/users/Morfindien/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "html_url": "https://github.com/Morfindien/Bubbleverse",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/Morfindien/Bubbleverse",
    "forks_url": "https://api.github.com/repos/Morfindien/Bubbleverse/forks",
    "keys_url": "https://api.github.com/repos/Morfindien/Bubbleverse/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/Morfindien/Bubbleverse/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/Morfindien/Bubbleverse/teams",
    "hooks_url": "https://api.github.com/repos/Morfindien/Bubbleverse/hooks",
    "issue_events_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues/events{/number}",
    "events_url": "https://api.github.com/repos/Morfindien/Bubbleverse/events",
    "assignees_url": "https://api.github.com/repos/Morfindien/Bubbleverse/assignees{/user}",
    "branches_url": "https://api.github.com/repos/Morfindien/Bubbleverse/branches{/branch}",
    "tags_url": "https://api.github.com/repos/Morfindien/Bubbleverse/tags",
    "blobs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/Morfindien/Bubbleverse/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/Morfindien/Bubbleverse/languages",
    "stargazers_url": "https://api.github.com/repos/Morfindien/Bubbleverse/stargazers",
    "contributors_url": "https://api.github.com/repos/Morfindien/Bubbleverse/contributors",
    "subscribers_url": "https://api.github.com/repos/Morfindien/Bubbleverse/subscribers",
    "subscription_url": "https://api.github.com/repos/Morfindien/Bubbleverse/subscription",
    "commits_url": "https://api.github.com/repos/Morfindien/Bubbleverse/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/Morfindien/Bubbleverse/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/Morfindien/Bubbleverse/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/Morfindien/Bubbleverse/contents/{+path}",
    "compare_url": "https://api.github.com/repos/Morfindien/Bubbleverse/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/Morfindien/Bubbleverse/merges",
    "archive_url": "https://api.github.com/repos/Morfindien/Bubbleverse/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/Morfindien/Bubbleverse/downloads",
    "issues_url": "https://api.github.com/repos/Morfindien/Bubbleverse/issues{/number}",
    "pulls_url": "https://api.github.com/repos/Morfindien/Bubbleverse/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/Morfindien/Bubbleverse/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/Morfindien/Bubbleverse/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/Morfindien/Bubbleverse/labels{/name}",
    "releases_url": "https://api.github.com/repos/Morfindien/Bubbleverse/releases{/id}",
    "deployments_url": "https://api.github.com/repos/Morfindien/Bubbleverse/deployments"
  }
}
```


## APPENDIX D2 — RETRIEVED V19 FINAL ARTIFACT METADATA

**Preserved UTF-8 source SHA-256:** `4f13f9d5a2170fb53338ad3d0a1e6615a50d0d6e5d661c403bd3efddf99f195e`; bytes: 831.

```json
{
  "artifacts": [
    {
      "id": 11296144394,
      "name": "q042-production-final-v19",
      "size_in_bytes": 30912,
      "url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11296144394",
      "archive_download_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11296144394/zip",
      "expired": false,
      "created_at": "2026-10-04T07:29:02Z",
      "expires_at": "2026-11-03T07:29:02Z",
      "updated_at": "2026-10-04T07:29:02Z",
      "digest": "sha256:394baf90b4f28b821c5071f3e59636c64ea81f968f1343a28a23ae0475a208d0",
      "workflow_run": {
        "id": 37185888043,
        "repository_id": 1348235216,
        "head_repository_id": 1348235216,
        "head_branch": "main",
        "head_sha": "7af1298c5f1db17557d7671d2ea38ca6d67b7df1"
      }
    }
  ]
}
```


## APPENDIX E1 — RAW CAMSPEC EDE FULL TERMINAL JOB LOG

**Preserved UTF-8 source SHA-256:** `4b8cd3349616f0c251147fb80a6d1b49f514291fc9e9d80470558d0056493ad5`; bytes: 132935.

```text
﻿2026-10-02T07:33:15.6259661Z Current runner version: '2.337.0'
2026-10-02T07:33:15.6281845Z ##[group]Runner Image Provisioner
2026-10-02T07:33:15.6282730Z Hosted Compute Agent
2026-10-02T07:33:15.6283091Z Version: 20260901.588
2026-10-02T07:33:15.6283586Z Commit: f88ec8081b781fac6c440065ac7ff9e710ce3d0b
2026-10-02T07:33:15.6284024Z Build Date: 2026-09-01T19:56:44Z
2026-10-02T07:33:15.6284432Z Worker ID: {a172bcff-2c27-44f3-9def-725502a4f2c3}
2026-10-02T07:33:15.6284896Z Azure Region: westus3
2026-10-02T07:33:15.6285269Z ##[endgroup]
2026-10-02T07:33:15.6286201Z ##[group]Operating System
2026-10-02T07:33:15.6286564Z Ubuntu
2026-10-02T07:33:15.6286875Z 24.04.5
2026-10-02T07:33:15.6287236Z LTS
2026-10-02T07:33:15.6287551Z ##[endgroup]
2026-10-02T07:33:15.6287936Z ##[group]Runner Image
2026-10-02T07:33:15.6288329Z Image: ubuntu-24.04
2026-10-02T07:33:15.6288674Z Version: 20260927.320.1
2026-10-02T07:33:15.6289528Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20260927.320/images/ubuntu/Ubuntu2404-Readme.md
2026-10-02T07:33:15.6290441Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20260927.320
2026-10-02T07:33:15.6291001Z ##[endgroup]
2026-10-02T07:33:15.6291761Z ##[group]GITHUB_TOKEN Permissions
2026-10-02T07:33:15.6293505Z Actions: write
2026-10-02T07:33:15.6293895Z Contents: read
2026-10-02T07:33:15.6294295Z Metadata: read
2026-10-02T07:33:15.6294632Z ##[endgroup]
2026-10-02T07:33:15.6296207Z Secret source: Actions
2026-10-02T07:33:15.6296763Z Cache mode: write
2026-10-02T07:33:15.6297279Z Prepare workflow directory
2026-10-02T07:33:15.6717298Z Prepare all required actions
2026-10-02T07:33:15.6766161Z Getting action download info
2026-10-02T07:33:15.9916599Z Download action repository 'actions/checkout@v4' (SHA:11d5960a326750d5838078e36cf38b85af677262)
2026-10-02T07:33:16.0938709Z Download action repository 'actions/setup-python@v7' (SHA:5fda3b95a4ea91299a34e894583c3862153e4b97)
2026-10-02T07:33:16.2284196Z Download action repository 'actions/cache@v4' (SHA:0057852bfaa89a56745cba8c7296529d2fc39830)
2026-10-02T07:33:16.3867957Z Download action repository 'actions/download-artifact@v4' (SHA:d3f86a106a0bac45b974a628896c90dbdf5c8093)
2026-10-02T07:33:17.1374145Z Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
2026-10-02T07:33:17.3379997Z Complete job name: polychord-continuation
2026-10-02T07:33:17.3867693Z ##[group]Run actions/checkout@v4
2026-10-02T07:33:17.3868434Z with:
2026-10-02T07:33:17.3868697Z   repository: Morfindien/Bubbleverse
2026-10-02T07:33:17.3871381Z   token: ***
2026-10-02T07:33:17.3871625Z   ssh-strict: true
2026-10-02T07:33:17.3871879Z   ssh-user: git
2026-10-02T07:33:17.3872142Z   persist-credentials: true
2026-10-02T07:33:17.3872555Z   clean: true
2026-10-02T07:33:17.3872816Z   sparse-checkout-cone-mode: true
2026-10-02T07:33:17.3873138Z   fetch-depth: 1
2026-10-02T07:33:17.3873386Z   fetch-tags: false
2026-10-02T07:33:17.3873646Z   show-progress: true
2026-10-02T07:33:17.3873931Z   lfs: false
2026-10-02T07:33:17.3874207Z   submodules: false
2026-10-02T07:33:17.3874466Z   set-safe-directory: true
2026-10-02T07:33:17.3874767Z   allow-unsafe-pr-checkout: false
2026-10-02T07:33:17.3875165Z env:
2026-10-02T07:33:17.3875393Z   CURRENT_Q: Q-042
2026-10-02T07:33:17.3875652Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:33:17.3876005Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:33:17.3876383Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:33:17.3876830Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:33:17.3877257Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:33:17.3877643Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:33:17.3878104Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:33:17.3878686Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:33:17.3879228Z ##[endgroup]
2026-10-02T07:33:17.4666827Z Syncing repository: Morfindien/Bubbleverse
2026-10-02T07:33:17.4668958Z ##[group]Getting Git version info
2026-10-02T07:33:17.4669551Z Working directory is '/home/runner/work/Bubbleverse/Bubbleverse'
2026-10-02T07:33:17.4670458Z [command]/usr/bin/git version
2026-10-02T07:33:17.4740354Z git version 2.55.0
2026-10-02T07:33:17.4756235Z ##[endgroup]
2026-10-02T07:33:17.4768796Z Temporarily overriding HOME='/home/runner/work/_temp/f8bfb25f-0fed-4593-b296-224217d09063' before making global git config changes
2026-10-02T07:33:17.4770267Z Adding repository directory to the temporary git global config as a safe directory
2026-10-02T07:33:17.4773527Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/Bubbleverse/Bubbleverse
2026-10-02T07:33:17.4827633Z Deleting the contents of '/home/runner/work/Bubbleverse/Bubbleverse'
2026-10-02T07:33:17.4832968Z ##[group]Initializing the repository
2026-10-02T07:33:17.4835885Z [command]/usr/bin/git init /home/runner/work/Bubbleverse/Bubbleverse
2026-10-02T07:33:17.5082948Z hint: Using 'master' as the name for the initial branch. This default branch name
2026-10-02T07:33:17.5085050Z hint: will change to "main" in Git 3.0. To configure the initial branch name
2026-10-02T07:33:17.5086310Z hint: to use in all of your new repositories, which will suppress this warning,
2026-10-02T07:33:17.5087323Z hint: call:
2026-10-02T07:33:17.5088036Z hint:
2026-10-02T07:33:17.5088750Z hint: 	git config --global init.defaultBranch <name>
2026-10-02T07:33:17.5089484Z hint:
2026-10-02T07:33:17.5090141Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2026-10-02T07:33:17.5091259Z hint: 'development'. The just-created branch can be renamed via this command:
2026-10-02T07:33:17.5092154Z hint:
2026-10-02T07:33:17.5092703Z hint: 	git branch -m <name>
2026-10-02T07:33:17.5093217Z hint:
2026-10-02T07:33:17.5093920Z hint: Disable this message with "git config set advice.defaultBranchName false"
2026-10-02T07:33:17.5095191Z Initialized empty Git repository in /home/runner/work/Bubbleverse/Bubbleverse/.git/
2026-10-02T07:33:17.5097393Z [command]/usr/bin/git remote add origin https://github.com/Morfindien/Bubbleverse
2026-10-02T07:33:17.5160309Z ##[endgroup]
2026-10-02T07:33:17.5160871Z ##[group]Disabling automatic garbage collection
2026-10-02T07:33:17.5163128Z [command]/usr/bin/git config --local gc.auto 0
2026-10-02T07:33:17.5196024Z ##[endgroup]
2026-10-02T07:33:17.5197019Z ##[group]Setting up auth
2026-10-02T07:33:17.5201755Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-02T07:33:17.5232808Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-02T07:33:17.5534511Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-02T07:33:17.5567368Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-02T07:33:17.5752821Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-02T07:33:17.5785394Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-02T07:33:17.5972569Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-10-02T07:33:17.6008223Z ##[endgroup]
2026-10-02T07:33:17.6008819Z ##[group]Fetching the repository
2026-10-02T07:33:17.6016744Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +d0f92c7f2ce53da32818244f8847f8e745e20c4f:refs/remotes/origin/main
2026-10-02T07:33:18.7574196Z From https://github.com/Morfindien/Bubbleverse
2026-10-02T07:33:18.7575966Z  * [new ref]         d0f92c7f2ce53da32818244f8847f8e745e20c4f -> origin/main
2026-10-02T07:33:18.7579240Z ##[endgroup]
2026-10-02T07:33:18.7580385Z ##[group]Determining the checkout info
2026-10-02T07:33:18.7582043Z ##[endgroup]
2026-10-02T07:33:18.7584293Z [command]/usr/bin/git sparse-checkout disable
2026-10-02T07:33:18.7804081Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2026-10-02T07:33:18.7834557Z ##[group]Checking out the ref
2026-10-02T07:33:18.7871896Z [command]/usr/bin/git checkout --progress --force -B main refs/remotes/origin/main
2026-10-02T07:33:18.8513308Z Switched to a new branch 'main'
2026-10-02T07:33:18.8523724Z branch 'main' set up to track 'origin/main'.
2026-10-02T07:33:18.8528223Z ##[endgroup]
2026-10-02T07:33:18.8569476Z [command]/usr/bin/git log -1 --format=%H
2026-10-02T07:33:18.8596825Z d0f92c7f2ce53da32818244f8847f8e745e20c4f
2026-10-02T07:33:18.8870553Z ##[group]Run actions/setup-python@v7
2026-10-02T07:33:18.8871269Z with:
2026-10-02T07:33:18.8871750Z   python-version: 3.11
2026-10-02T07:33:18.8872414Z   check-latest: false
2026-10-02T07:33:18.8877878Z   token: ***
2026-10-02T07:33:18.8878394Z   update-environment: true
2026-10-02T07:33:18.8879013Z   allow-prereleases: false
2026-10-02T07:33:18.8879611Z   freethreaded: false
2026-10-02T07:33:18.8880138Z env:
2026-10-02T07:33:18.8880585Z   CURRENT_Q: Q-042
2026-10-02T07:33:18.8881110Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:33:18.8881740Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:33:18.8882728Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:33:18.8883776Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:33:18.8884599Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:33:18.8885354Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:33:18.8886373Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:33:18.8887530Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:33:18.8888562Z ##[endgroup]
2026-10-02T07:33:18.9722174Z ##[group]Installed versions
2026-10-02T07:33:18.9776531Z Successfully set up CPython (3.11.16)
2026-10-02T07:33:18.9778116Z ##[endgroup]
2026-10-02T07:33:18.9926269Z ##[group]Run test 'Q042-PROD-V18' = "$PROGRAM_ID"
2026-10-02T07:33:18.9927384Z [36;1mtest 'Q042-PROD-V18' = "$PROGRAM_ID"[0m
2026-10-02T07:33:18.9928123Z [36;1mtest -n '36731879692'[0m
2026-10-02T07:33:18.9928835Z [36;1mtest -n '36960394429'[0m
2026-10-02T07:33:19.0251939Z shell: /usr/bin/bash -e {0}
2026-10-02T07:33:19.0252739Z env:
2026-10-02T07:33:19.0253213Z   CURRENT_Q: Q-042
2026-10-02T07:33:19.0253760Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:33:19.0254400Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:33:19.0255171Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:33:19.0256066Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:33:19.0256895Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:33:19.0257628Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:33:19.0258530Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:33:19.0259761Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:33:19.0260937Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0261961Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:33:19.0263049Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0263982Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0264911Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0265843Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:33:19.0266621Z ##[endgroup]
2026-10-02T07:33:19.0453098Z ##[group]Run actions/cache/restore@v4
2026-10-02T07:33:19.0453712Z with:
2026-10-02T07:33:19.0455362Z   path: ~/.cache/pip
external/cobaya_packages
external/class_ede
external/hillipop
external/act_dr6_cmbonly
external/act_dr6_lenslike
external/cobaya_desi_dr2_source
external/bao_data_v2_6
external/PolyChordLite

2026-10-02T07:33:19.0457684Z   key: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-02T07:33:19.0458693Z   fail-on-cache-miss: true
2026-10-02T07:33:19.0459270Z   enableCrossOsArchive: false
2026-10-02T07:33:19.0459837Z   lookup-only: false
2026-10-02T07:33:19.0460319Z env:
2026-10-02T07:33:19.0460745Z   CURRENT_Q: Q-042
2026-10-02T07:33:19.0461236Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:33:19.0461817Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:33:19.0462615Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:33:19.0463445Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:33:19.0464246Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:33:19.0464933Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:33:19.0465775Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:33:19.0466820Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:33:19.0467937Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0468864Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:33:19.0469809Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0470658Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0471517Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:33:19.0472472Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:33:19.0473206Z ##[endgroup]
2026-10-02T07:33:19.1221038Z (node:2095) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-02T07:33:19.1222686Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-02T07:33:19.3221290Z Cache hit for: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-02T07:33:19.3288779Z (node:2095) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-02T07:33:20.5340645Z Received 41943040 of 2242870168 (1.9%), 40.0 MBs/sec
2026-10-02T07:33:21.5343128Z Received 184549376 of 2242870168 (8.2%), 88.0 MBs/sec
2026-10-02T07:33:22.5364491Z Received 301989888 of 2242870168 (13.5%), 96.0 MBs/sec
2026-10-02T07:33:23.5383573Z Received 461373440 of 2242870168 (20.6%), 109.9 MBs/sec
2026-10-02T07:33:24.5393605Z Received 603979776 of 2242870168 (26.9%), 115.2 MBs/sec
2026-10-02T07:33:25.5367594Z Received 725614592 of 2242870168 (32.4%), 115.3 MBs/sec
2026-10-02T07:33:26.5368403Z Received 843055104 of 2242870168 (37.6%), 114.8 MBs/sec
2026-10-02T07:33:27.5369258Z Received 968884224 of 2242870168 (43.2%), 115.5 MBs/sec
2026-10-02T07:33:28.5390344Z Received 1098907648 of 2242870168 (49.0%), 116.4 MBs/sec
2026-10-02T07:33:29.5371547Z Received 1233125376 of 2242870168 (55.0%), 117.6 MBs/sec
2026-10-02T07:33:30.5370868Z Received 1350565888 of 2242870168 (60.2%), 117.1 MBs/sec
2026-10-02T07:33:31.5371640Z Received 1476395008 of 2242870168 (65.8%), 117.3 MBs/sec
2026-10-02T07:33:32.5376663Z Received 1606418432 of 2242870168 (71.6%), 117.8 MBs/sec
2026-10-02T07:33:33.5384776Z Received 1723858944 of 2242870168 (76.9%), 117.4 MBs/sec
2026-10-02T07:33:34.5393821Z Received 1832910848 of 2242870168 (81.7%), 116.5 MBs/sec
2026-10-02T07:33:35.5399510Z Received 1962934272 of 2242870168 (87.5%), 117.0 MBs/sec
2026-10-02T07:33:36.5400360Z Received 2067791872 of 2242870168 (92.2%), 116.0 MBs/sec
2026-10-02T07:33:37.5408382Z Received 2172649472 of 2242870168 (96.9%), 115.1 MBs/sec
2026-10-02T07:33:38.0686930Z Received 2242870168 of 2242870168 (100.0%), 115.4 MBs/sec
2026-10-02T07:33:38.0688050Z Cache Size: ~2139 MB (2242870168 B)
2026-10-02T07:33:38.0778915Z [command]/usr/bin/tar -xf /home/runner/work/_temp/afaabbd6-1a1b-4486-8809-9ce43bfa5d50/cache.tzst -P -C /home/runner/work/Bubbleverse/Bubbleverse --use-compress-program unzstd
2026-10-02T07:34:02.3511099Z Cache restored successfully
2026-10-02T07:34:02.4546547Z Cache restored from key: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-02T07:34:02.4931769Z ##[group]Run sudo apt-get update -y
2026-10-02T07:34:02.4932025Z [36;1msudo apt-get update -y[0m
2026-10-02T07:34:02.4932455Z [36;1msudo apt-get install -y gfortran gcc g++ make openmpi-bin libopenmpi-dev pkg-config[0m
2026-10-02T07:34:02.4932785Z [36;1mgit fetch --depth 1 origin "$Q032_EXECUTION_COMMIT"[0m
2026-10-02T07:34:02.4933020Z [36;1mgit worktree add --detach q032_parent "$Q032_EXECUTION_COMMIT"[0m
2026-10-02T07:34:02.4987485Z shell: /usr/bin/bash -e {0}
2026-10-02T07:34:02.4987640Z env:
2026-10-02T07:34:02.4987761Z   CURRENT_Q: Q-042
2026-10-02T07:34:02.4987887Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:34:02.4988035Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:34:02.4988216Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:34:02.4988437Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:34:02.4988626Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:34:02.4988847Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:34:02.4989060Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:34:02.4989320Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:34:02.4989599Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:02.4989832Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:34:02.4990059Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:02.4990268Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:02.4990480Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:02.4990691Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:34:02.4990879Z ##[endgroup]
2026-10-02T07:34:02.7510572Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-10-02T07:34:02.8110579Z Hit:2 http://azure.archive.ubuntu.com/ubuntu noble InRelease
2026-10-02T07:34:02.8111460Z Get:6 https://packages.microsoft.com/ubuntu/24.04/prod noble InRelease [3600 B]
2026-10-02T07:34:02.8126652Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
2026-10-02T07:34:02.9614853Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
2026-10-02T07:34:02.9629484Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble-security InRelease [126 kB]
2026-10-02T07:34:03.0036207Z Get:7 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1364 kB]
2026-10-02T07:34:03.0873675Z Get:16 https://packages.microsoft.com/ubuntu/24.04/prod noble/main arm64 Packages [458 kB]
2026-10-02T07:34:03.1284282Z Get:8 http://azure.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [304 kB]
2026-10-02T07:34:03.1321953Z Get:19 https://packages.microsoft.com/ubuntu/24.04/prod noble/main amd64 Packages [510 kB]
2026-10-02T07:34:03.2676293Z Get:9 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [181 kB]
2026-10-02T07:34:03.2693411Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1699 kB]
2026-10-02T07:34:03.2714666Z Get:28 https://packages.microsoft.com/ubuntu/24.04/prod noble/main armhf Packages [12.6 kB]
2026-10-02T07:34:03.5065513Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [341 kB]
2026-10-02T07:34:03.5082115Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [388 kB]
2026-10-02T07:34:03.5865340Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [1720 kB]
2026-10-02T07:34:03.6466806Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [394 kB]
2026-10-02T07:34:03.7055597Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
2026-10-02T07:34:03.7066258Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [5760 B]
2026-10-02T07:34:03.7564032Z Get:18 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [12.6 kB]
2026-10-02T07:34:03.7650707Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Packages [1069 kB]
2026-10-02T07:34:03.8266044Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble-security/main Translation-en [221 kB]
2026-10-02T07:34:03.8270366Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Components [46.4 kB]
2026-10-02T07:34:03.8280366Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1216 kB]
2026-10-02T07:34:03.9556618Z Get:24 http://azure.archive.ubuntu.com/ubuntu noble-security/universe Translation-en [244 kB]
2026-10-02T07:34:03.9557284Z Get:25 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Components [76.3 kB]
2026-10-02T07:34:03.9563124Z Get:26 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [1566 kB]
2026-10-02T07:34:04.0741398Z Get:27 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted Translation-en [361 kB]
2026-10-02T07:34:09.8344925Z Fetched 12.6 MB in 1s (8527 kB/s)
2026-10-02T07:34:10.4353944Z Reading package lists...
2026-10-02T07:34:10.4603801Z Reading package lists...
2026-10-02T07:34:10.6595869Z Building dependency tree...
2026-10-02T07:34:10.6601756Z Reading state information...
2026-10-02T07:34:10.8104237Z gfortran is already the newest version (4:13.2.0-7ubuntu1).
2026-10-02T07:34:10.8104793Z gcc is already the newest version (4:13.2.0-7ubuntu1).
2026-10-02T07:34:10.8105231Z g++ is already the newest version (4:13.2.0-7ubuntu1).
2026-10-02T07:34:10.8105666Z make is already the newest version (4.3-4.1build2).
2026-10-02T07:34:10.8106108Z pkg-config is already the newest version (1.8.1-2build1).
2026-10-02T07:34:10.8106574Z The following additional packages will be installed:
2026-10-02T07:34:10.8107144Z   libamd-comgr2 libamdhip64-5 libcaf-openmpi-3t64 libcoarrays-dev
2026-10-02T07:34:10.8107734Z   libcoarrays-openmpi-dev libevent-2.1-7t64 libevent-core-2.1-7t64
2026-10-02T07:34:10.8108346Z   libevent-dev libevent-extra-2.1-7t64 libevent-openssl-2.1-7t64
2026-10-02T07:34:10.8108950Z   libevent-pthreads-2.1-7t64 libfabric1 libhsa-runtime64-1 libhsakmt1
2026-10-02T07:34:10.8109598Z   libhwloc-dev libhwloc-plugins libhwloc15 libibverbs-dev libjs-jquery-ui
2026-10-02T07:34:10.8110227Z   libltdl-dev libmunge2 libnl-3-dev libnl-route-3-dev libnuma-dev
2026-10-02T07:34:10.8110856Z   libopenmpi3t64 libpmix-dev libpmix2t64 libpsm-infinipath1 libpsm2-2
2026-10-02T07:34:10.8111414Z   librdmacm1t64 libucx0 libxnvctrl0 ocl-icd-libopencl1 openmpi-common
2026-10-02T07:34:10.8120095Z Suggested packages:
2026-10-02T07:34:10.8120387Z   libhwloc-contrib-plugins libjs-jquery-ui-docs libtool-doc openmpi-doc
2026-10-02T07:34:10.8120679Z   opencl-icd
2026-10-02T07:34:10.8524790Z The following NEW packages will be installed:
2026-10-02T07:34:10.8525449Z   libamd-comgr2 libamdhip64-5 libcaf-openmpi-3t64 libcoarrays-dev
2026-10-02T07:34:10.8525984Z   libcoarrays-openmpi-dev libevent-2.1-7t64 libevent-dev
2026-10-02T07:34:10.8526483Z   libevent-extra-2.1-7t64 libevent-openssl-2.1-7t64 libfabric1
2026-10-02T07:34:10.8527010Z   libhsa-runtime64-1 libhsakmt1 libhwloc-dev libhwloc-plugins libhwloc15
2026-10-02T07:34:10.8527590Z   libibverbs-dev libjs-jquery-ui libltdl-dev libmunge2 libnl-3-dev
2026-10-02T07:34:10.8528150Z   libnl-route-3-dev libnuma-dev libopenmpi-dev libopenmpi3t64 libpmix-dev
2026-10-02T07:34:10.8530882Z   libpmix2t64 libpsm-infinipath1 libpsm2-2 librdmacm1t64 libucx0 libxnvctrl0
2026-10-02T07:34:10.8533134Z   ocl-icd-libopencl1 openmpi-bin openmpi-common
2026-10-02T07:34:10.8539255Z The following packages will be upgraded:
2026-10-02T07:34:10.8544756Z   libevent-core-2.1-7t64 libevent-pthreads-2.1-7t64
2026-10-02T07:34:10.8691918Z 2 upgraded, 34 newly installed, 0 to remove and 23 not upgraded.
2026-10-02T07:34:10.8692702Z Need to get 38.3 MB of archives.
2026-10-02T07:34:10.8693024Z After this operation, 145 MB of additional disk space will be used.
2026-10-02T07:34:10.8693582Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-10-02T07:34:10.9772921Z Get:2 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libamd-comgr2 amd64 6.0+git20231212.4510c28+dfsg-3build2 [14.4 MB]
2026-10-02T07:34:12.8447542Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhsakmt1 amd64 5.7.0-1build1 [62.9 kB]
2026-10-02T07:34:12.9644649Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhsa-runtime64-1 amd64 5.7.1-2build1 [491 kB]
2026-10-02T07:34:13.1745908Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libamdhip64-5 amd64 5.7.1-3 [9621 kB]
2026-10-02T07:34:13.9701577Z Get:6 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-pthreads-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [7988 B]
2026-10-02T07:34:14.0352479Z Get:7 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-core-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [91.9 kB]
2026-10-02T07:34:14.1160083Z Get:8 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpsm-infinipath1 amd64 3.3+20.604758e7-6.3build1 [178 kB]
2026-10-02T07:34:14.2138807Z Get:9 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpsm2-2 amd64 11.2.185-2build1 [194 kB]
2026-10-02T07:34:14.2800561Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 librdmacm1t64 amd64 50.0-2ubuntu0.2 [70.7 kB]
2026-10-02T07:34:14.3450624Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libfabric1 amd64 1.17.0-3build2 [657 kB]
2026-10-02T07:34:14.4175704Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc15 amd64 2.10.0-1build1 [172 kB]
2026-10-02T07:34:14.4831915Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 libmunge2 amd64 0.5.15-4ubuntu0.1 [14.8 kB]
2026-10-02T07:34:14.5473511Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libxnvctrl0 amd64 510.47.03-0ubuntu4.24.04.1 [12.7 kB]
2026-10-02T07:34:14.6125098Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 ocl-icd-libopencl1 amd64 2.3.2-1build1 [38.5 kB]
2026-10-02T07:34:14.6775355Z Get:16 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc-plugins amd64 2.10.0-1build1 [15.7 kB]
2026-10-02T07:34:14.7417320Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpmix2t64 amd64 5.0.1-4.1build1 [697 kB]
2026-10-02T07:34:14.8157111Z Get:18 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libucx0 amd64 1.16.0+ds-5ubuntu1 [1140 kB]
2026-10-02T07:34:14.8945954Z Get:19 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libopenmpi3t64 amd64 4.1.6-7ubuntu2 [2563 kB]
2026-10-02T07:34:14.9955939Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcaf-openmpi-3t64 amd64 2.10.2+ds-2.1build2 [39.1 kB]
2026-10-02T07:34:15.0597739Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcoarrays-dev amd64 2.10.2+ds-2.1build2 [37.5 kB]
2026-10-02T07:34:15.1240885Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 openmpi-common all 4.1.6-7ubuntu2 [170 kB]
2026-10-02T07:34:15.1907796Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 openmpi-bin amd64 4.1.6-7ubuntu2 [114 kB]
2026-10-02T07:34:15.2552047Z Get:24 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcoarrays-openmpi-dev amd64 2.10.2+ds-2.1build2 [372 kB]
2026-10-02T07:34:15.3229582Z Get:25 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [146 kB]
2026-10-02T07:34:15.3878908Z Get:26 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-extra-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [64.6 kB]
2026-10-02T07:34:15.4520892Z Get:27 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-openssl-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [15.8 kB]
2026-10-02T07:34:15.5160092Z Get:28 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-dev amd64 2.1.12-stable-9ubuntu2.2 [274 kB]
2026-10-02T07:34:15.5828292Z Get:29 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libjs-jquery-ui all 1.13.2+dfsg-1 [252 kB]
2026-10-02T07:34:15.6490715Z Get:30 http://azure.archive.ubuntu.com/ubuntu noble/main amd64 libltdl-dev amd64 2.4.7-7build1 [168 kB]
2026-10-02T07:34:15.7139156Z Get:31 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnl-3-dev amd64 3.7.0-0.3build1.1 [99.5 kB]
2026-10-02T07:34:15.7784405Z Get:32 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnl-route-3-dev amd64 3.7.0-0.3build1.1 [216 kB]
2026-10-02T07:34:15.8443325Z Get:33 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnuma-dev amd64 2.0.18-1ubuntu0.24.04.1 [37.0 kB]
2026-10-02T07:34:15.9083543Z Get:34 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc-dev amd64 2.10.0-1build1 [268 kB]
2026-10-02T07:34:15.9749926Z Get:35 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpmix-dev amd64 5.0.1-4.1build1 [4018 kB]
2026-10-02T07:34:16.1138828Z Get:36 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libibverbs-dev amd64 50.0-2ubuntu0.2 [686 kB]
2026-10-02T07:34:16.1820075Z Get:37 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libopenmpi-dev amd64 4.1.6-7ubuntu2 [864 kB]
2026-10-02T07:34:16.4028326Z Fetched 38.3 MB in 5s (7185 kB/s)
2026-10-02T07:34:16.4205959Z Selecting previously unselected package libamd-comgr2:amd64.
2026-10-02T07:34:16.4450999Z (Reading database ... 
2026-10-02T07:34:16.4451339Z (Reading database ... 5%
2026-10-02T07:34:16.4451765Z (Reading database ... 10%
2026-10-02T07:34:16.4451963Z (Reading database ... 15%
2026-10-02T07:34:16.4452102Z (Reading database ... 20%
2026-10-02T07:34:16.4452380Z (Reading database ... 25%
2026-10-02T07:34:16.4452520Z (Reading database ... 30%
2026-10-02T07:34:16.4452644Z (Reading database ... 35%
2026-10-02T07:34:16.4452794Z (Reading database ... 40%
2026-10-02T07:34:16.4452919Z (Reading database ... 45%
2026-10-02T07:34:16.4453043Z (Reading database ... 50%
2026-10-02T07:34:16.4496504Z (Reading database ... 55%
2026-10-02T07:34:16.5795433Z (Reading database ... 60%
2026-10-02T07:34:16.7838633Z (Reading database ... 65%
2026-10-02T07:34:16.9888857Z (Reading database ... 70%
2026-10-02T07:34:17.1921855Z (Reading database ... 75%
2026-10-02T07:34:17.3336663Z (Reading database ... 80%
2026-10-02T07:34:17.5393007Z (Reading database ... 85%
2026-10-02T07:34:17.7478046Z (Reading database ... 90%
2026-10-02T07:34:17.8972987Z (Reading database ... 95%
2026-10-02T07:34:17.8973302Z (Reading database ... 100%
2026-10-02T07:34:17.8973611Z (Reading database ... 202296 files and directories currently installed.)
2026-10-02T07:34:17.9011831Z Preparing to unpack .../00-libamd-comgr2_6.0+git20231212.4510c28+dfsg-3build2_amd64.deb ...
2026-10-02T07:34:17.9142326Z Unpacking libamd-comgr2:amd64 (6.0+git20231212.4510c28+dfsg-3build2) ...
2026-10-02T07:34:18.3760640Z Selecting previously unselected package libhsakmt1:amd64.
2026-10-02T07:34:18.3855795Z Preparing to unpack .../01-libhsakmt1_5.7.0-1build1_amd64.deb ...
2026-10-02T07:34:18.3863251Z Unpacking libhsakmt1:amd64 (5.7.0-1build1) ...
2026-10-02T07:34:18.4052805Z Selecting previously unselected package libhsa-runtime64-1.
2026-10-02T07:34:18.4147115Z Preparing to unpack .../02-libhsa-runtime64-1_5.7.1-2build1_amd64.deb ...
2026-10-02T07:34:18.4155256Z Unpacking libhsa-runtime64-1 (5.7.1-2build1) ...
2026-10-02T07:34:18.4454289Z Selecting previously unselected package libamdhip64-5.
2026-10-02T07:34:18.4549538Z Preparing to unpack .../03-libamdhip64-5_5.7.1-3_amd64.deb ...
2026-10-02T07:34:18.4655251Z Unpacking libamdhip64-5 (5.7.1-3) ...
2026-10-02T07:34:18.6530654Z Preparing to unpack .../04-libevent-pthreads-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:18.6609233Z Unpacking libevent-pthreads-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) over (2.1.12-stable-9ubuntu2.1) ...
2026-10-02T07:34:18.7103270Z Preparing to unpack .../05-libevent-core-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:18.7154066Z Unpacking libevent-core-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) over (2.1.12-stable-9ubuntu2.1) ...
2026-10-02T07:34:18.7373375Z Selecting previously unselected package libpsm-infinipath1.
2026-10-02T07:34:18.7471930Z Preparing to unpack .../06-libpsm-infinipath1_3.3+20.604758e7-6.3build1_amd64.deb ...
2026-10-02T07:34:18.7479297Z Unpacking libpsm-infinipath1 (3.3+20.604758e7-6.3build1) ...
2026-10-02T07:34:18.7674124Z Selecting previously unselected package libpsm2-2.
2026-10-02T07:34:18.7769691Z Preparing to unpack .../07-libpsm2-2_11.2.185-2build1_amd64.deb ...
2026-10-02T07:34:18.7777306Z Unpacking libpsm2-2 (11.2.185-2build1) ...
2026-10-02T07:34:18.7971178Z Selecting previously unselected package librdmacm1t64:amd64.
2026-10-02T07:34:18.8065920Z Preparing to unpack .../08-librdmacm1t64_50.0-2ubuntu0.2_amd64.deb ...
2026-10-02T07:34:18.8073097Z Unpacking librdmacm1t64:amd64 (50.0-2ubuntu0.2) ...
2026-10-02T07:34:18.8260673Z Selecting previously unselected package libfabric1:amd64.
2026-10-02T07:34:18.8357095Z Preparing to unpack .../09-libfabric1_1.17.0-3build2_amd64.deb ...
2026-10-02T07:34:18.8364236Z Unpacking libfabric1:amd64 (1.17.0-3build2) ...
2026-10-02T07:34:18.8626559Z Selecting previously unselected package libhwloc15:amd64.
2026-10-02T07:34:18.8721854Z Preparing to unpack .../10-libhwloc15_2.10.0-1build1_amd64.deb ...
2026-10-02T07:34:18.8727895Z Unpacking libhwloc15:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:18.9083795Z Selecting previously unselected package libmunge2:amd64.
2026-10-02T07:34:18.9180291Z Preparing to unpack .../11-libmunge2_0.5.15-4ubuntu0.1_amd64.deb ...
2026-10-02T07:34:18.9186801Z Unpacking libmunge2:amd64 (0.5.15-4ubuntu0.1) ...
2026-10-02T07:34:18.9354962Z Selecting previously unselected package libxnvctrl0:amd64.
2026-10-02T07:34:18.9451269Z Preparing to unpack .../12-libxnvctrl0_510.47.03-0ubuntu4.24.04.1_amd64.deb ...
2026-10-02T07:34:18.9457020Z Unpacking libxnvctrl0:amd64 (510.47.03-0ubuntu4.24.04.1) ...
2026-10-02T07:34:18.9627668Z Selecting previously unselected package ocl-icd-libopencl1:amd64.
2026-10-02T07:34:18.9724330Z Preparing to unpack .../13-ocl-icd-libopencl1_2.3.2-1build1_amd64.deb ...
2026-10-02T07:34:18.9729969Z Unpacking ocl-icd-libopencl1:amd64 (2.3.2-1build1) ...
2026-10-02T07:34:18.9968136Z Selecting previously unselected package libhwloc-plugins:amd64.
2026-10-02T07:34:19.0064611Z Preparing to unpack .../14-libhwloc-plugins_2.10.0-1build1_amd64.deb ...
2026-10-02T07:34:19.0070440Z Unpacking libhwloc-plugins:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:19.0244249Z Selecting previously unselected package libpmix2t64:amd64.
2026-10-02T07:34:19.0342908Z Preparing to unpack .../15-libpmix2t64_5.0.1-4.1build1_amd64.deb ...
2026-10-02T07:34:19.0348974Z Unpacking libpmix2t64:amd64 (5.0.1-4.1build1) ...
2026-10-02T07:34:19.0660289Z Selecting previously unselected package libucx0:amd64.
2026-10-02T07:34:19.0754846Z Preparing to unpack .../16-libucx0_1.16.0+ds-5ubuntu1_amd64.deb ...
2026-10-02T07:34:19.0760823Z Unpacking libucx0:amd64 (1.16.0+ds-5ubuntu1) ...
2026-10-02T07:34:19.1166244Z Selecting previously unselected package libopenmpi3t64:amd64.
2026-10-02T07:34:19.1261466Z Preparing to unpack .../17-libopenmpi3t64_4.1.6-7ubuntu2_amd64.deb ...
2026-10-02T07:34:19.1267196Z Unpacking libopenmpi3t64:amd64 (4.1.6-7ubuntu2) ...
2026-10-02T07:34:19.2091842Z Selecting previously unselected package libcaf-openmpi-3t64:amd64.
2026-10-02T07:34:19.2187142Z Preparing to unpack .../18-libcaf-openmpi-3t64_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-02T07:34:19.2192509Z Unpacking libcaf-openmpi-3t64:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:19.2361157Z Selecting previously unselected package libcoarrays-dev:amd64.
2026-10-02T07:34:19.2454545Z Preparing to unpack .../19-libcoarrays-dev_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-02T07:34:19.2621293Z Unpacking libcoarrays-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:19.2924246Z Selecting previously unselected package openmpi-common.
2026-10-02T07:34:19.3020296Z Preparing to unpack .../20-openmpi-common_4.1.6-7ubuntu2_all.deb ...
2026-10-02T07:34:19.3026044Z Unpacking openmpi-common (4.1.6-7ubuntu2) ...
2026-10-02T07:34:19.3501781Z Selecting previously unselected package openmpi-bin.
2026-10-02T07:34:19.3600142Z Preparing to unpack .../21-openmpi-bin_4.1.6-7ubuntu2_amd64.deb ...
2026-10-02T07:34:19.3605434Z Unpacking openmpi-bin (4.1.6-7ubuntu2) ...
2026-10-02T07:34:19.3931174Z Selecting previously unselected package libcoarrays-openmpi-dev:amd64.
2026-10-02T07:34:19.4028439Z Preparing to unpack .../22-libcoarrays-openmpi-dev_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-02T07:34:19.4033947Z Unpacking libcoarrays-openmpi-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:19.4493407Z Selecting previously unselected package libevent-2.1-7t64:amd64.
2026-10-02T07:34:19.4590095Z Preparing to unpack .../23-libevent-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:19.4596396Z Unpacking libevent-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:19.4783812Z Selecting previously unselected package libevent-extra-2.1-7t64:amd64.
2026-10-02T07:34:19.4880954Z Preparing to unpack .../24-libevent-extra-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:19.4887455Z Unpacking libevent-extra-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:19.5070486Z Selecting previously unselected package libevent-openssl-2.1-7t64:amd64.
2026-10-02T07:34:19.5167083Z Preparing to unpack .../25-libevent-openssl-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:19.5173948Z Unpacking libevent-openssl-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:19.5340407Z Selecting previously unselected package libevent-dev.
2026-10-02T07:34:19.5437289Z Preparing to unpack .../26-libevent-dev_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-02T07:34:19.5544107Z Unpacking libevent-dev (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:19.5802185Z Selecting previously unselected package libjs-jquery-ui.
2026-10-02T07:34:19.5898681Z Preparing to unpack .../27-libjs-jquery-ui_1.13.2+dfsg-1_all.deb ...
2026-10-02T07:34:19.5903725Z Unpacking libjs-jquery-ui (1.13.2+dfsg-1) ...
2026-10-02T07:34:19.6445777Z Selecting previously unselected package libltdl-dev:amd64.
2026-10-02T07:34:19.6542773Z Preparing to unpack .../28-libltdl-dev_2.4.7-7build1_amd64.deb ...
2026-10-02T07:34:19.6547967Z Unpacking libltdl-dev:amd64 (2.4.7-7build1) ...
2026-10-02T07:34:19.6778271Z Selecting previously unselected package libnl-3-dev:amd64.
2026-10-02T07:34:19.6874542Z Preparing to unpack .../29-libnl-3-dev_3.7.0-0.3build1.1_amd64.deb ...
2026-10-02T07:34:19.6880111Z Unpacking libnl-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-02T07:34:19.7165131Z Selecting previously unselected package libnl-route-3-dev:amd64.
2026-10-02T07:34:19.7261729Z Preparing to unpack .../30-libnl-route-3-dev_3.7.0-0.3build1.1_amd64.deb ...
2026-10-02T07:34:19.7267448Z Unpacking libnl-route-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-02T07:34:19.7457438Z Selecting previously unselected package libnuma-dev:amd64.
2026-10-02T07:34:19.7552008Z Preparing to unpack .../31-libnuma-dev_2.0.18-1ubuntu0.24.04.1_amd64.deb ...
2026-10-02T07:34:19.7559040Z Unpacking libnuma-dev:amd64 (2.0.18-1ubuntu0.24.04.1) ...
2026-10-02T07:34:19.7788850Z Selecting previously unselected package libhwloc-dev:amd64.
2026-10-02T07:34:19.7883228Z Preparing to unpack .../32-libhwloc-dev_2.10.0-1build1_amd64.deb ...
2026-10-02T07:34:19.7889178Z Unpacking libhwloc-dev:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:19.8097466Z Selecting previously unselected package libpmix-dev:amd64.
2026-10-02T07:34:19.8192843Z Preparing to unpack .../33-libpmix-dev_5.0.1-4.1build1_amd64.deb ...
2026-10-02T07:34:19.8199164Z Unpacking libpmix-dev:amd64 (5.0.1-4.1build1) ...
2026-10-02T07:34:19.9258986Z Selecting previously unselected package libibverbs-dev:amd64.
2026-10-02T07:34:19.9356955Z Preparing to unpack .../34-libibverbs-dev_50.0-2ubuntu0.2_amd64.deb ...
2026-10-02T07:34:19.9361983Z Unpacking libibverbs-dev:amd64 (50.0-2ubuntu0.2) ...
2026-10-02T07:34:20.0019221Z Selecting previously unselected package libopenmpi-dev:amd64.
2026-10-02T07:34:20.0116465Z Preparing to unpack .../35-libopenmpi-dev_4.1.6-7ubuntu2_amd64.deb ...
2026-10-02T07:34:20.0243453Z Unpacking libopenmpi-dev:amd64 (4.1.6-7ubuntu2) ...
2026-10-02T07:34:20.1973593Z Setting up libcoarrays-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:20.1990656Z Setting up libevent-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2004801Z Setting up libnuma-dev:amd64 (2.0.18-1ubuntu0.24.04.1) ...
2026-10-02T07:34:20.2018706Z Setting up libxnvctrl0:amd64 (510.47.03-0ubuntu4.24.04.1) ...
2026-10-02T07:34:20.2032329Z Setting up libltdl-dev:amd64 (2.4.7-7build1) ...
2026-10-02T07:34:20.2044990Z Setting up libjs-jquery-ui (1.13.2+dfsg-1) ...
2026-10-02T07:34:20.2058494Z Setting up libmunge2:amd64 (0.5.15-4ubuntu0.1) ...
2026-10-02T07:34:20.2071603Z Setting up libhwloc15:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:20.2084751Z Setting up libnl-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-02T07:34:20.2098147Z Setting up ocl-icd-libopencl1:amd64 (2.3.2-1build1) ...
2026-10-02T07:34:20.2111981Z Setting up libpsm2-2 (11.2.185-2build1) ...
2026-10-02T07:34:20.2124557Z Setting up openmpi-common (4.1.6-7ubuntu2) ...
2026-10-02T07:34:20.2137637Z Setting up librdmacm1t64:amd64 (50.0-2ubuntu0.2) ...
2026-10-02T07:34:20.2151043Z Setting up libhwloc-dev:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:20.2163919Z Setting up libevent-core-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2177065Z Setting up libamd-comgr2:amd64 (6.0+git20231212.4510c28+dfsg-3build2) ...
2026-10-02T07:34:20.2189997Z Setting up libpsm-infinipath1 (3.3+20.604758e7-6.3build1) ...
2026-10-02T07:34:20.2233410Z update-alternatives: using /usr/lib/libpsm1/libpsm_infinipath.so.1.16 to provide /usr/lib/x86_64-linux-gnu/libpsm_infinipath.so.1 (libpsm_infinipath.so.1) in auto mode
2026-10-02T07:34:20.2247275Z Setting up libhsakmt1:amd64 (5.7.0-1build1) ...
2026-10-02T07:34:20.2258957Z Setting up libfabric1:amd64 (1.17.0-3build2) ...
2026-10-02T07:34:20.2272554Z Setting up libevent-pthreads-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2286167Z Setting up libevent-openssl-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2299471Z Setting up libhwloc-plugins:amd64 (2.10.0-1build1) ...
2026-10-02T07:34:20.2313841Z Setting up libnl-route-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-02T07:34:20.2327138Z Setting up libpmix2t64:amd64 (5.0.1-4.1build1) ...
2026-10-02T07:34:20.2341702Z Setting up libevent-extra-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2354874Z Setting up libhsa-runtime64-1 (5.7.1-2build1) ...
2026-10-02T07:34:20.2367862Z Setting up libibverbs-dev:amd64 (50.0-2ubuntu0.2) ...
2026-10-02T07:34:20.2380621Z Setting up libamdhip64-5 (5.7.1-3) ...
2026-10-02T07:34:20.2394312Z Setting up libevent-dev (2.1.12-stable-9ubuntu2.2) ...
2026-10-02T07:34:20.2408458Z Setting up libpmix-dev:amd64 (5.0.1-4.1build1) ...
2026-10-02T07:34:20.2423497Z Setting up libucx0:amd64 (1.16.0+ds-5ubuntu1) ...
2026-10-02T07:34:20.2437054Z Setting up libopenmpi3t64:amd64 (4.1.6-7ubuntu2) ...
2026-10-02T07:34:20.2449778Z Setting up openmpi-bin (4.1.6-7ubuntu2) ...
2026-10-02T07:34:20.2510859Z update-alternatives: using /usr/bin/mpirun.openmpi to provide /usr/bin/mpirun (mpirun) in auto mode
2026-10-02T07:34:20.2549016Z update-alternatives: using /usr/bin/mpicc.openmpi to provide /usr/bin/mpicc (mpi) in auto mode
2026-10-02T07:34:20.2577137Z Setting up libcaf-openmpi-3t64:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:20.2591209Z Setting up libopenmpi-dev:amd64 (4.1.6-7ubuntu2) ...
2026-10-02T07:34:20.2635614Z update-alternatives: using /usr/lib/x86_64-linux-gnu/openmpi/include to provide /usr/include/x86_64-linux-gnu/mpi (mpi-x86_64-linux-gnu) in auto mode
2026-10-02T07:34:20.2654489Z Setting up libcoarrays-openmpi-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-02T07:34:20.2697506Z update-alternatives: using /usr/lib/x86_64-linux-gnu/open-coarrays/openmpi/bin/caf to provide /usr/bin/caf.openmpi (caf-openmpi) in auto mode
2026-10-02T07:34:20.2732388Z update-alternatives: using /usr/bin/caf.openmpi to provide /usr/bin/caf (caf) in auto mode
2026-10-02T07:34:20.2750271Z Processing triggers for libc-bin (2.39-0ubuntu8.9) ...
2026-10-02T07:34:20.4815729Z Processing triggers for man-db (2.12.0-4build2) ...
2026-10-02T07:34:20.4834431Z Not building database; man-db/auto-update is not 'true'.
2026-10-02T07:34:20.9488900Z 
2026-10-02T07:34:20.9489369Z Running kernel seems to be up-to-date.
2026-10-02T07:34:20.9489602Z 
2026-10-02T07:34:20.9489702Z No services need to be restarted.
2026-10-02T07:34:20.9489846Z 
2026-10-02T07:34:20.9489937Z No containers need to be restarted.
2026-10-02T07:34:20.9490085Z 
2026-10-02T07:34:20.9490187Z No user sessions are running outdated binaries.
2026-10-02T07:34:20.9490364Z 
2026-10-02T07:34:20.9490525Z No VM guests are running outdated hypervisor (qemu) binaries on this host.
2026-10-02T07:34:22.3254015Z From https://github.com/Morfindien/Bubbleverse
2026-10-02T07:34:22.3254448Z  * branch            4dc873a5e880d40858d831a3b421456728f0c032 -> FETCH_HEAD
2026-10-02T07:34:22.3274026Z Preparing worktree (detached HEAD 4dc873a)
2026-10-02T07:34:22.3596905Z HEAD is now at 4dc873a Rename q032-planck-tt3pair-bridge-v2.yml to .github/workflows/q032-planck-tt3pair-bridge-v2.yml
2026-10-02T07:34:22.3648136Z ##[group]Run actions/download-artifact@v4
2026-10-02T07:34:22.3648319Z with:
2026-10-02T07:34:22.3649667Z   github-token: ***
2026-10-02T07:34:22.3649786Z   run-id: 36731879692
2026-10-02T07:34:22.3649914Z   name: q042-v18-36731879692-environment
2026-10-02T07:34:22.3650054Z   path: env_bundle
2026-10-02T07:34:22.3650170Z   merge-multiple: false
2026-10-02T07:34:22.3650298Z   repository: Morfindien/Bubbleverse
2026-10-02T07:34:22.3650435Z env:
2026-10-02T07:34:22.3650534Z   CURRENT_Q: Q-042
2026-10-02T07:34:22.3650651Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:34:22.3650792Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:34:22.3650972Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:34:22.3651168Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:34:22.3651348Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:34:22.3651511Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:34:22.3651731Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:34:22.3651976Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:34:22.3652403Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:22.3652634Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:34:22.3652850Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:22.3653048Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:22.3653249Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:22.3653452Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:34:22.3653624Z ##[endgroup]
2026-10-02T07:34:22.4605896Z Downloading single artifact
2026-10-02T07:34:22.4650685Z (node:2936) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-02T07:34:22.4651331Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-02T07:34:22.4812850Z (node:2936) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-02T07:34:22.7649465Z Preparing to download the following artifacts:
2026-10-02T07:34:22.7650097Z - q042-v18-36731879692-environment (ID: 11104699558, Size: 278493088, Expected Digest: sha256:cc9d05fd514f50e64e4e1f56a6ecb1a9046ba43373491a9023f465a015e7d905)
2026-10-02T07:34:22.7669758Z Downloading artifact '11104699558' from 'Morfindien/Bubbleverse'
2026-10-02T07:34:22.9526413Z Redirecting to blob download url: https://productionresultssa3.blob.core.windows.net/actions-results/2c197768-5f79-49c7-b6da-cd466920b916/workflow-job-run-496d5009-1d18-5828-9622-8cb0335918ef/artifacts/05922946e67ed61a98ae0dbd7f4a02ecde010c0e90b1b08fa70fc13ec27b0e95.zip
2026-10-02T07:34:22.9527520Z Starting download of artifact to: /home/runner/work/Bubbleverse/Bubbleverse/env_bundle
2026-10-02T07:34:23.2540526Z (node:2936) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
2026-10-02T07:34:52.1892050Z SHA256 digest of downloaded artifact is cc9d05fd514f50e64e4e1f56a6ecb1a9046ba43373491a9023f465a015e7d905
2026-10-02T07:34:52.1892540Z Artifact download completed successfully.
2026-10-02T07:34:52.1892716Z Total of 1 artifact(s) downloaded
2026-10-02T07:34:52.1897853Z Download artifact has finished successfully
2026-10-02T07:34:52.2024597Z ##[group]Run set -euo pipefail
2026-10-02T07:34:52.2024786Z [36;1mset -euo pipefail[0m
2026-10-02T07:34:52.2024921Z [36;1mP=$((PREV_SEG-1))[0m
2026-10-02T07:34:52.2025099Z [36;1mgh run download "$PREV_RUN" --repo "$GITHUB_REPOSITORY" \[0m
2026-10-02T07:34:52.2025374Z [36;1m  --name "q042-v18-${ROOT}-checkpoint-${ARM}-${MODEL}-${COMBO}-s${P}" --dir previous[0m
2026-10-02T07:34:52.2025624Z [36;1mcp -a previous/cell_state ./cell_state[0m
2026-10-02T07:34:52.2025784Z [36;1mpython - <<'PY'[0m
2026-10-02T07:34:52.2025909Z [36;1mimport json,os[0m
2026-10-02T07:34:52.2026083Z [36;1mp=json.load(open('previous/q042_production_segment_v18.json'))[0m
2026-10-02T07:34:52.2026319Z [36;1massert p['q']=='Q-042' and p['program_id']=='Q042-PROD-V18'[0m
2026-10-02T07:34:52.2026618Z [36;1massert p['arm']==os.environ['ARM'] and p['model']==os.environ['MODEL'] and p['combination']==os.environ['COMBO'][0m
2026-10-02T07:34:52.2026936Z [36;1massert int(p['segment'])==int(os.environ['PREV_SEG'])-1[0m
2026-10-02T07:34:52.2027147Z [36;1massert p['status']=='SEGMENT_CHECKPOINTED'[0m
2026-10-02T07:34:52.2027341Z [36;1mprint('Q042_PROD_V18_CHECKPOINT_LINEAGE_GATE=PASS')[0m
2026-10-02T07:34:52.2027512Z [36;1mPY[0m
2026-10-02T07:34:52.2081408Z shell: /usr/bin/bash -e {0}
2026-10-02T07:34:52.2081544Z env:
2026-10-02T07:34:52.2081649Z   CURRENT_Q: Q-042
2026-10-02T07:34:52.2081772Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:34:52.2081917Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:34:52.2082085Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:34:52.2082424Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:34:52.2082800Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:34:52.2083050Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:34:52.2083325Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:34:52.2083721Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:34:52.2084102Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:52.2084417Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:34:52.2084745Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:52.2085008Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:52.2085322Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:52.2085630Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:34:52.2087199Z   GH_TOKEN: ***
2026-10-02T07:34:52.2087386Z   PREV_RUN: 36960394429
2026-10-02T07:34:52.2087625Z   PREV_SEG: 7
2026-10-02T07:34:52.2087811Z   ROOT: 36731879692
2026-10-02T07:34:52.2088023Z   ARM: camspec
2026-10-02T07:34:52.2088233Z   MODEL: ede_n3
2026-10-02T07:34:52.2099968Z   COMBO: FULL
2026-10-02T07:34:52.2100165Z ##[endgroup]
2026-10-02T07:34:55.4947953Z Q042_PROD_V18_CHECKPOINT_LINEAGE_GATE=PASS
2026-10-02T07:34:55.5072837Z ##[group]Run bash q042_setup_recovery_v18.sh
2026-10-02T07:34:55.5073216Z [36;1mbash q042_setup_recovery_v18.sh[0m
2026-10-02T07:34:55.5126078Z shell: /usr/bin/bash -e {0}
2026-10-02T07:34:55.5126228Z env:
2026-10-02T07:34:55.5126342Z   CURRENT_Q: Q-042
2026-10-02T07:34:55.5126464Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:34:55.5126616Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:34:55.5126786Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:34:55.5126987Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:34:55.5127170Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:34:55.5127341Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:34:55.5127546Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:34:55.5127798Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:34:55.5128102Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:55.5128339Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:34:55.5128575Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:55.5128793Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:55.5129004Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:34:55.5129213Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:34:55.5129395Z ##[endgroup]
2026-10-02T07:34:55.5841765Z Q042_V4_Q032_CACHE_GATE=HIT
2026-10-02T07:34:57.4112348Z Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (26.2.1)
2026-10-02T07:34:58.4016655Z Collecting cobaya==3.5.6 (from -r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:58.4017074Z   Using cached cobaya-3.5.6-py3-none-any.whl
2026-10-02T07:34:58.4365152Z Collecting PyYAML==6.0.2 (from -r q005_hpc_v14_requirements.txt (line 2))
2026-10-02T07:34:58.4376700Z   Using cached PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
2026-10-02T07:34:58.5500676Z Collecting numpy==1.26.4 (from -r q005_hpc_v14_requirements.txt (line 3))
2026-10-02T07:34:58.5513639Z   Using cached numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
2026-10-02T07:34:58.6220707Z Collecting scipy==1.15.3 (from -r q005_hpc_v14_requirements.txt (line 4))
2026-10-02T07:34:58.6234128Z   Using cached scipy-1.15.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
2026-10-02T07:34:58.7141857Z Collecting Py-BOBYQA==1.5.0 (from -r q005_hpc_v14_requirements.txt (line 5))
2026-10-02T07:34:58.7150811Z   Using cached Py_BOBYQA-1.5.0-py3-none-any.whl.metadata (9.5 kB)
2026-10-02T07:34:58.7988057Z Collecting getdist==1.6.1 (from -r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:58.7988458Z   Using cached getdist-1.6.1-py3-none-any.whl
2026-10-02T07:34:58.9265546Z Collecting Cython==0.29.37 (from -r q005_hpc_v14_requirements.txt (line 7))
2026-10-02T07:34:58.9278064Z   Using cached Cython-0.29.37-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl.metadata (3.1 kB)
2026-10-02T07:34:59.0137797Z Collecting sacc==1.0.2 (from -r q005_hpc_v14_requirements.txt (line 8))
2026-10-02T07:34:59.0147046Z   Using cached sacc-1.0.2-py3-none-any.whl.metadata (2.4 kB)
2026-10-02T07:34:59.1125974Z Collecting pandas>=1.0.1 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.1138225Z   Using cached pandas-3.0.6-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (79 kB)
2026-10-02T07:34:59.1443095Z Collecting requests>=2.18 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.1453496Z   Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
2026-10-02T07:34:59.1604354Z Collecting fuzzywuzzy>=0.17 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.1614041Z   Using cached fuzzywuzzy-0.18.0-py2.py3-none-any.whl.metadata (4.9 kB)
2026-10-02T07:34:59.1768741Z Collecting packaging (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.1778099Z   Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
2026-10-02T07:34:59.2023312Z Collecting tqdm (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.2034547Z   Using cached tqdm-4.70.1-py3-none-any.whl.metadata (57 kB)
2026-10-02T07:34:59.2211512Z Collecting portalocker>=2.3.0 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.2223072Z   Using cached portalocker-4.4.0-py3-none-any.whl.metadata (10 kB)
2026-10-02T07:34:59.2379201Z Collecting dill>=0.3.3 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.2389951Z   Using cached dill-0.4.1-py3-none-any.whl.metadata (10 kB)
2026-10-02T07:34:59.2554267Z Collecting typing_extensions (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:34:59.2564883Z   Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
2026-10-02T07:34:59.2591524Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0->-r q005_hpc_v14_requirements.txt (line 5)) (79.0.1)
2026-10-02T07:34:59.3355960Z Collecting matplotlib!=3.5.0,>=2.2.0 (from getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.3368244Z   Using cached matplotlib-3.11.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (80 kB)
2026-10-02T07:34:59.4367001Z Collecting astropy (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-02T07:34:59.4380586Z   Using cached astropy-8.0.1-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-02T07:34:59.4833884Z Collecting contourpy>=1.0.1 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.4848146Z   Using cached contourpy-1.3.3-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (5.5 kB)
2026-10-02T07:34:59.4993562Z Collecting cycler>=0.10 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.5006049Z   Using cached cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
2026-10-02T07:34:59.5949141Z Collecting fonttools>=4.28.2 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.6737490Z   Downloading fonttools-4.66.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (130 kB)
2026-10-02T07:34:59.7423335Z Collecting kiwisolver>=1.3.1 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.7434364Z   Using cached kiwisolver-1.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.2 kB)
2026-10-02T07:34:59.8669113Z Collecting pillow>=9 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.8681831Z   Using cached pillow-12.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (9.1 kB)
2026-10-02T07:34:59.8883744Z Collecting pyparsing>=3 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.8893277Z   Using cached pyparsing-3.3.3-py3-none-any.whl.metadata (5.9 kB)
2026-10-02T07:34:59.9035016Z Collecting python-dateutil>=2.7 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.9044228Z   Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
2026-10-02T07:34:59.9222302Z Collecting six>=1.5 (from python-dateutil>=2.7->matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-02T07:34:59.9232495Z   Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
2026-10-02T07:34:59.9952688Z Collecting charset_normalizer<4,>=2 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:35:00.0055105Z   Downloading charset_normalizer-3.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (46 kB)
2026-10-02T07:35:00.0262871Z Collecting idna<4,>=2.5 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:35:00.0273633Z   Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
2026-10-02T07:35:00.0462653Z Collecting urllib3<3,>=1.26 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:35:00.0473538Z   Using cached urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
2026-10-02T07:35:00.0647988Z Collecting certifi>=2023.5.7 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-02T07:35:00.0659209Z   Using cached certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
2026-10-02T07:35:00.0913323Z Collecting astropy-iers-data>=0.2026.6.22.1.23.34 (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-02T07:35:00.1015494Z   Downloading astropy_iers_data-0.2026.9.28.0.59.37-py3-none-any.whl.metadata (3.4 kB)
2026-10-02T07:35:00.1049037Z INFO: pip is looking at multiple versions of astropy to determine which version is compatible with other requirements. This could take a while.
2026-10-02T07:35:00.1054448Z Collecting astropy (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-02T07:35:00.1065604Z   Using cached astropy-8.0.0-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-02T07:35:00.1111725Z   Using cached astropy-7.2.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-02T07:35:00.1373986Z Collecting pyerfa>=2.0.1.1 (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-02T07:35:00.1385742Z   Using cached pyerfa-2.0.1.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.7 kB)
2026-10-02T07:35:00.1452163Z Using cached PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
2026-10-02T07:35:00.1464197Z Using cached numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.3 MB)
2026-10-02T07:35:00.1521931Z Using cached scipy-1.15.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (37.7 MB)
2026-10-02T07:35:00.1626462Z Using cached Py_BOBYQA-1.5.0-py3-none-any.whl (57 kB)
2026-10-02T07:35:00.1636130Z Using cached Cython-0.29.37-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl (1.9 MB)
2026-10-02T07:35:00.1649954Z Using cached sacc-1.0.2-py3-none-any.whl (33 kB)
2026-10-02T07:35:00.1659222Z Using cached dill-0.4.1-py3-none-any.whl (120 kB)
2026-10-02T07:35:00.1668428Z Using cached fuzzywuzzy-0.18.0-py2.py3-none-any.whl (18 kB)
2026-10-02T07:35:00.1677420Z Using cached matplotlib-3.11.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (9.9 MB)
2026-10-02T07:35:00.1709868Z Using cached contourpy-1.3.3-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (355 kB)
2026-10-02T07:35:00.1719172Z Using cached cycler-0.12.1-py3-none-any.whl (8.3 kB)
2026-10-02T07:35:00.1819654Z Downloading fonttools-4.66.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.4 MB)
2026-10-02T07:35:00.4613051Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 20.6 MB/s  0:00:00
2026-10-02T07:35:00.4625296Z Using cached kiwisolver-1.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.4 MB)
2026-10-02T07:35:00.4639668Z Using cached packaging-26.3-py3-none-any.whl (129 kB)
2026-10-02T07:35:00.4649953Z Using cached pandas-3.0.6-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (11.1 MB)
2026-10-02T07:35:00.4687863Z Using cached pillow-12.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.9 MB)
2026-10-02T07:35:00.4713828Z Using cached portalocker-4.4.0-py3-none-any.whl (129 kB)
2026-10-02T07:35:00.4723523Z Using cached pyparsing-3.3.3-py3-none-any.whl (126 kB)
2026-10-02T07:35:00.4733198Z Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
2026-10-02T07:35:00.4742408Z Using cached requests-2.34.2-py3-none-any.whl (73 kB)
2026-10-02T07:35:00.4854147Z Downloading charset_normalizer-3.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (269 kB)
2026-10-02T07:35:00.4915306Z Using cached idna-3.20-py3-none-any.whl (69 kB)
2026-10-02T07:35:00.4924262Z Using cached urllib3-2.8.0-py3-none-any.whl (135 kB)
2026-10-02T07:35:00.4933069Z Using cached certifi-2026.7.22-py3-none-any.whl (136 kB)
2026-10-02T07:35:00.4941558Z Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
2026-10-02T07:35:00.4950577Z Using cached astropy-7.2.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (9.9 MB)
2026-10-02T07:35:00.5078661Z Downloading astropy_iers_data-0.2026.9.28.0.59.37-py3-none-any.whl (2.0 MB)
2026-10-02T07:35:00.5609372Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 36.7 MB/s  0:00:00
2026-10-02T07:35:00.5620066Z Using cached pyerfa-2.0.1.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (738 kB)
2026-10-02T07:35:00.5630841Z Using cached tqdm-4.70.1-py3-none-any.whl (80 kB)
2026-10-02T07:35:00.5639730Z Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
2026-10-02T07:35:00.7851255Z Installing collected packages: fuzzywuzzy, urllib3, typing_extensions, tqdm, six, PyYAML, pyparsing, portalocker, pillow, packaging, numpy, kiwisolver, idna, fonttools, dill, Cython, cycler, charset_normalizer, certifi, astropy-iers-data, scipy, requests, python-dateutil, pyerfa, contourpy, pandas, matplotlib, astropy, sacc, Py-BOBYQA, getdist, cobaya
2026-10-02T07:35:10.9134984Z 
2026-10-02T07:35:10.9147921Z Successfully installed Cython-0.29.37 Py-BOBYQA-1.5.0 PyYAML-6.0.2 astropy-7.2.2 astropy-iers-data-0.2026.9.28.0.59.37 certifi-2026.7.22 charset_normalizer-3.5.2 cobaya-3.5.6 contourpy-1.3.3 cycler-0.12.1 dill-0.4.1 fonttools-4.66.1 fuzzywuzzy-0.18.0 getdist-1.6.1 idna-3.20 kiwisolver-1.5.1 matplotlib-3.11.2 numpy-1.26.4 packaging-26.3 pandas-3.0.6 pillow-12.3.0 portalocker-4.4.0 pyerfa-2.0.1.5 pyparsing-3.3.3 python-dateutil-2.9.0.post0 requests-2.34.2 sacc-1.0.2 scipy-1.15.3 six-1.17.0 tqdm-4.70.1 typing_extensions-4.16.0 urllib3-2.8.0
2026-10-02T07:35:11.0747334Z Q017_V3_FROZEN_DEPENDENCY_GATE=PASS
2026-10-02T07:35:11.4589892Z HEAD is now at 5a131c91 Update README.md
2026-10-02T07:35:11.4632585Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/class_ede'
2026-10-02T07:35:11.4667021Z make: 'libclass.a' is up to date.
2026-10-02T07:35:11.4668423Z make: 'class' is up to date.
2026-10-02T07:35:11.4668789Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/class_ede'
2026-10-02T07:35:13.1924652Z warning: classy.pyx:363:76: local variable 'errmsg' referenced before assignment
2026-10-02T07:35:13.1924978Z warning: classy.pyx:364:39: local variable 'errmsg' referenced before assignment
2026-10-02T07:35:14.5053715Z In file included from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/ndarraytypes.h:1929,
2026-10-02T07:35:14.5054857Z                  from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
2026-10-02T07:35:14.5055728Z                  from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/arrayobject.h:5,
2026-10-02T07:35:14.5056525Z                  from /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/../python/classy.c:752:
2026-10-02T07:35:14.5057678Z /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
2026-10-02T07:35:14.5058696Z    17 | #warning "Using deprecated NumPy API, disable it with " \
2026-10-02T07:35:14.5059123Z       |  ^~~~~~~
2026-10-02T07:35:29.5111425Z [INFO] cobaya-install planck_NPIPE_highl_CamSpec.TTTEEE attempt=1/4
2026-10-02T07:35:30.3447827Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages'
2026-10-02T07:35:30.3459294Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-02T07:35:30.3486940Z 
2026-10-02T07:35:30.3487757Z ================================================================================
2026-10-02T07:35:30.3488003Z planck_NPIPE_highl_CamSpec.TTTEEE
2026-10-02T07:35:30.3488222Z ================================================================================
2026-10-02T07:35:30.3488400Z 
2026-10-02T07:35:30.3488548Z [install] Checking if dependencies have already been installed...
2026-10-02T07:35:30.3493784Z [install] External dependencies for this component already installed.
2026-10-02T07:35:30.3502897Z [install] Doing nothing.
2026-10-02T07:35:30.3503040Z 
2026-10-02T07:35:30.3503188Z ================================================================================
2026-10-02T07:35:30.3503449Z * Summary * 
2026-10-02T07:35:30.3503623Z ================================================================================
2026-10-02T07:35:30.3503745Z 
2026-10-02T07:35:30.3504002Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages
2026-10-02T07:35:30.8791961Z Q017_V3_CLASS_EDE_GATE=PASS /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/build/lib.linux-x86_64-cpython-311/classy.cpython-311-x86_64-linux-gnu.so
2026-10-02T07:35:30.8792604Z Q017_V3_PLANCK_FULL_MF_INSTALL_GATE=PASS
2026-10-02T07:35:31.0371660Z Q017_V3_RUNTIME_PROVENANCE_GATE=PASS
2026-10-02T07:35:31.0450883Z Q017_V3_SETUP_GATE=PASS
2026-10-02T07:35:31.0524585Z Q032_PYTHON_311_GATE=PASS 3.11.16
2026-10-02T07:35:31.2392600Z Requirement already satisfied: cobaya==3.5.6 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 1)) (3.5.6)
2026-10-02T07:35:31.2394002Z Requirement already satisfied: PyYAML==6.0.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 2)) (6.0.2)
2026-10-02T07:35:31.2396648Z Requirement already satisfied: numpy==1.26.4 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 3)) (1.26.4)
2026-10-02T07:35:31.2399009Z Requirement already satisfied: scipy==1.15.3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 4)) (1.15.3)
2026-10-02T07:35:31.2401355Z Requirement already satisfied: Py-BOBYQA==1.5.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 5)) (1.5.0)
2026-10-02T07:35:31.2403633Z Requirement already satisfied: getdist==1.6.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 6)) (1.6.1)
2026-10-02T07:35:31.2405829Z Requirement already satisfied: Cython==0.29.37 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 7)) (0.29.37)
2026-10-02T07:35:31.2408395Z Requirement already satisfied: sacc==1.0.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 8)) (1.0.2)
2026-10-02T07:35:31.2436238Z Requirement already satisfied: pandas>=1.0.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.0.6)
2026-10-02T07:35:31.2439186Z Requirement already satisfied: requests>=2.18 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2.34.2)
2026-10-02T07:35:31.2443087Z Requirement already satisfied: fuzzywuzzy>=0.17 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (0.18.0)
2026-10-02T07:35:31.2444693Z Requirement already satisfied: packaging in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (26.3)
2026-10-02T07:35:31.2446867Z Requirement already satisfied: tqdm in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.70.1)
2026-10-02T07:35:31.2449113Z Requirement already satisfied: portalocker>=2.3.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.4.0)
2026-10-02T07:35:31.2451334Z Requirement already satisfied: dill>=0.3.3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (0.4.1)
2026-10-02T07:35:31.2453570Z Requirement already satisfied: typing_extensions in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.16.0)
2026-10-02T07:35:31.2505691Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0->-r q005_hpc_v14_requirements.txt (line 5)) (79.0.1)
2026-10-02T07:35:31.2533707Z Requirement already satisfied: matplotlib!=3.5.0,>=2.2.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (3.11.2)
2026-10-02T07:35:31.2544185Z Requirement already satisfied: astropy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (7.2.2)
2026-10-02T07:35:31.2576467Z Requirement already satisfied: contourpy>=1.0.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.3.3)
2026-10-02T07:35:31.2578910Z Requirement already satisfied: cycler>=0.10 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (0.12.1)
2026-10-02T07:35:31.2581322Z Requirement already satisfied: fonttools>=4.28.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (4.66.1)
2026-10-02T07:35:31.2583789Z Requirement already satisfied: kiwisolver>=1.3.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.5.1)
2026-10-02T07:35:31.2587217Z Requirement already satisfied: pillow>=9 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (12.3.0)
2026-10-02T07:35:31.2589488Z Requirement already satisfied: pyparsing>=3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (3.3.3)
2026-10-02T07:35:31.2592046Z Requirement already satisfied: python-dateutil>=2.7 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (2.9.0.post0)
2026-10-02T07:35:31.2704967Z Requirement already satisfied: six>=1.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from python-dateutil>=2.7->matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.17.0)
2026-10-02T07:35:31.2712031Z Requirement already satisfied: charset_normalizer<4,>=2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.5.2)
2026-10-02T07:35:31.2715242Z Requirement already satisfied: idna<4,>=2.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.20)
2026-10-02T07:35:31.2717660Z Requirement already satisfied: urllib3<3,>=1.26 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2.8.0)
2026-10-02T07:35:31.2721838Z Requirement already satisfied: certifi>=2023.5.7 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2026.7.22)
2026-10-02T07:35:31.2752544Z Requirement already satisfied: astropy-iers-data>=0.2026.6.22.1.23.34 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (0.2026.9.28.0.59.37)
2026-10-02T07:35:31.2756154Z Requirement already satisfied: pyerfa>=2.0.1.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (2.0.1.5)
2026-10-02T07:35:31.5423287Z Requirement already satisfied: astropy==7.2.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (7.2.2)
2026-10-02T07:35:31.5430816Z Requirement already satisfied: astropy-iers-data>=0.2026.6.22.1.23.34 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (0.2026.9.28.0.59.37)
2026-10-02T07:35:31.5434151Z Requirement already satisfied: numpy<2.7,>=1.24 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (1.26.4)
2026-10-02T07:35:31.5436733Z Requirement already satisfied: packaging>=22.0.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (26.3)
2026-10-02T07:35:31.5438937Z Requirement already satisfied: pyerfa>=2.0.1.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (2.0.1.5)
2026-10-02T07:35:31.5440905Z Requirement already satisfied: PyYAML>=6.0.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (6.0.2)
2026-10-02T07:35:31.6608342Z Q032_FROZEN_DEPENDENCY_GATE=PASS
2026-10-02T07:35:31.9668938Z HEAD is now at 5a131c91 Update README.md
2026-10-02T07:35:32.3032831Z HEAD is now at a09ddde Merge pull request #36 from planck-npipe/v4.3
2026-10-02T07:35:32.4837165Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/hillipop
2026-10-02T07:35:32.4849443Z   Installing build dependencies: started
2026-10-02T07:35:33.5014196Z   Installing build dependencies: finished with status 'done'
2026-10-02T07:35:33.5018882Z   Checking if build backend supports build_editable: started
2026-10-02T07:35:33.6974250Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-02T07:35:33.6979867Z   Getting requirements to build editable: started
2026-10-02T07:35:34.6973716Z   Getting requirements to build editable: finished with status 'done'
2026-10-02T07:35:34.6981646Z   Preparing editable metadata (pyproject.toml): started
2026-10-02T07:35:34.9378821Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-02T07:35:34.9423623Z Building wheels for collected packages: planck_2020_hillipop
2026-10-02T07:35:34.9429076Z   Building editable for planck_2020_hillipop (pyproject.toml): started
2026-10-02T07:35:35.2021922Z   Building editable for planck_2020_hillipop (pyproject.toml): finished with status 'done'
2026-10-02T07:35:35.2027026Z   Created wheel for planck_2020_hillipop: filename=planck_2020_hillipop-4.3-0.editable-py3-none-any.whl size=30032 sha256=f7c95207aa2dece8f381b76ef5627eb486c7abaad7d1b1797e7660df30df4821
2026-10-02T07:35:35.2027811Z   Stored in directory: /tmp/pip-ephem-wheel-cache-e580tu_y/wheels/ea/81/c6/7ed21441057e2523daefa6adbb44ef71baacfa55e2f6aacb52
2026-10-02T07:35:35.2072030Z Successfully built planck_2020_hillipop
2026-10-02T07:35:35.2138267Z Installing collected packages: planck_2020_hillipop
2026-10-02T07:35:35.2195220Z Successfully installed planck_2020_hillipop-4.3
2026-10-02T07:35:35.2751022Z [INFO] Q032 cobaya-install planck_2020_hillipop.TT attempt=1/4
2026-10-02T07:35:35.7292107Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages'
2026-10-02T07:35:35.7607008Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-02T07:35:35.8678184Z 
2026-10-02T07:35:35.8678671Z ================================================================================
2026-10-02T07:35:35.8679003Z planck_2020_hillipop.TT
2026-10-02T07:35:35.8679228Z ================================================================================
2026-10-02T07:35:35.8679355Z 
2026-10-02T07:35:35.8679460Z [install] Checking if dependencies have already been installed...
2026-10-02T07:35:35.8686771Z [install] External dependencies for this component already installed.
2026-10-02T07:35:35.8687077Z [install] Doing nothing.
2026-10-02T07:35:35.8687212Z 
2026-10-02T07:35:35.8687313Z ================================================================================
2026-10-02T07:35:35.8687558Z * Summary * 
2026-10-02T07:35:35.8687747Z ================================================================================
2026-10-02T07:35:35.8687891Z 
2026-10-02T07:35:35.8688139Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages
2026-10-02T07:35:36.9729907Z Q032_BACKEND_IDENTITY_GATE=PASS
2026-10-02T07:35:36.9730163Z Q032_HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=PASS
2026-10-02T07:35:36.9730342Z Q032_HILLIPOP_TT_DATA_GATE=PASS
2026-10-02T07:35:37.1071025Z Q032_CONTEXT_CONTINUITY_GATE=PASS
2026-10-02T07:35:37.1071264Z Q032_PYTHON_311_GATE=PASS
2026-10-02T07:35:37.1539393Z Q039_AUTHORITATIVE_Q032_CACHE_ENV_GATE=PASS
2026-10-02T07:35:37.2135519Z Q042_V4_FROZEN_Q032_CORE_GATE=PASS
2026-10-02T07:35:37.2729521Z Q041_FROZEN_CORE_DEPENDENCY_GATE=PASS
2026-10-02T07:35:37.4752171Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_cmbonly
2026-10-02T07:35:37.4761340Z   Installing build dependencies: started
2026-10-02T07:35:37.8336792Z   Installing build dependencies: finished with status 'done'
2026-10-02T07:35:37.8341840Z   Checking if build backend supports build_editable: started
2026-10-02T07:35:38.0105561Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-02T07:35:38.0111275Z   Getting requirements to build editable: started
2026-10-02T07:35:38.1350842Z   Getting requirements to build editable: finished with status 'done'
2026-10-02T07:35:38.1358285Z   Preparing editable metadata (pyproject.toml): started
2026-10-02T07:35:38.2480065Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-02T07:35:38.2502516Z Building wheels for collected packages: ACT-DR6-CMBonly
2026-10-02T07:35:38.2507733Z   Building editable for ACT-DR6-CMBonly (pyproject.toml): started
2026-10-02T07:35:38.3718220Z   Building editable for ACT-DR6-CMBonly (pyproject.toml): finished with status 'done'
2026-10-02T07:35:38.3722916Z   Created wheel for ACT-DR6-CMBonly: filename=act_dr6_cmbonly-1.0.0-0.editable-py3-none-any.whl size=2965 sha256=1e32b2637bcabf62ae8d3e239ac4c72fbdf2e7f0cb0770003654ad98623f04dd
2026-10-02T07:35:38.3723791Z   Stored in directory: /tmp/pip-ephem-wheel-cache-ccse8kkd/wheels/e9/00/d4/6bcdd39f247b8990a0d608a159e82446ce7b174bc7258a895b
2026-10-02T07:35:38.3737672Z Successfully built ACT-DR6-CMBonly
2026-10-02T07:35:38.3801062Z Installing collected packages: ACT-DR6-CMBonly
2026-10-02T07:35:38.3848447Z Successfully installed ACT-DR6-CMBonly-1.0.0
2026-10-02T07:35:38.4307919Z Q041_ACT_CMB_LAMBDA_DATA_GATE=PASS path=/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits
2026-10-02T07:35:38.6131904Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_lenslike
2026-10-02T07:35:38.6142934Z   Installing build dependencies: started
2026-10-02T07:35:39.0700460Z   Installing build dependencies: finished with status 'done'
2026-10-02T07:35:39.0705243Z   Checking if build backend supports build_editable: started
2026-10-02T07:35:39.1304887Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-02T07:35:39.1309899Z   Getting requirements to build editable: started
2026-10-02T07:35:39.1821162Z   Getting requirements to build editable: finished with status 'done'
2026-10-02T07:35:39.1827322Z   Preparing editable metadata (pyproject.toml): started
2026-10-02T07:35:39.2327703Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-02T07:35:39.2352055Z Building wheels for collected packages: act_dr6_lenslike
2026-10-02T07:35:39.2358427Z   Building editable for act_dr6_lenslike (pyproject.toml): started
2026-10-02T07:35:39.2885572Z   Building editable for act_dr6_lenslike (pyproject.toml): finished with status 'done'
2026-10-02T07:35:39.2890089Z   Created wheel for act_dr6_lenslike: filename=act_dr6_lenslike-1.2.0-py2.py3-none-any.whl size=4126 sha256=7bdf95443fdac11857a2fbd6e20617f9c206fb7ddb3cb1ea5a15a61e71e19991
2026-10-02T07:35:39.2891054Z   Stored in directory: /tmp/pip-ephem-wheel-cache-bowlpcc5/wheels/8c/db/c7/248b06e38a1f07a22faa7bcbc157b826e315394147e0942bc1
2026-10-02T07:35:39.2906830Z Successfully built act_dr6_lenslike
2026-10-02T07:35:39.2973195Z Installing collected packages: act_dr6_lenslike
2026-10-02T07:35:39.4164568Z Successfully installed act_dr6_lenslike-1.2.0
2026-10-02T07:35:39.4665476Z Q041_ACT_LENS_LAMBDA_DATA_GATE=PASS path=/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages/data/ACT_dr6_likelihood/v1.2
2026-10-02T07:35:40.0041584Z Q041_DESI_DR2_BAO_DTYPE_COMPATIBILITY_PATCH_GATE=PASS
2026-10-02T07:35:40.4805952Z Q041_DESI_DR2_BAO_STRINGDTYPE_RUNTIME_GATE=PASS pandas=3.0.6
2026-10-02T07:35:41.2181179Z Q041_DESI_DR2_COBAYA_VERSION_METADATA_GATE=PASS
2026-10-02T07:35:41.8433641Z Q041_EXTERNAL_RUNTIME_PROVENANCE_GATE=PASS
2026-10-02T07:35:41.9739655Z Q041_V14_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-02T07:35:41.9939368Z Q041_V15_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-02T07:35:42.0133098Z Q041_V16_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-02T07:35:42.0334250Z Q041_V19_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-02T07:35:42.2207129Z Requirement already satisfied: Py-BOBYQA==1.5.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (1.5.0)
2026-10-02T07:35:42.2212715Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (79.0.1)
2026-10-02T07:35:42.2215259Z Requirement already satisfied: numpy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (1.26.4)
2026-10-02T07:35:42.2217607Z Requirement already satisfied: scipy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (1.15.3)
2026-10-02T07:35:42.2219724Z Requirement already satisfied: pandas in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (3.0.6)
2026-10-02T07:35:42.2262571Z Requirement already satisfied: python-dateutil>=2.8.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from pandas->Py-BOBYQA==1.5.0) (2.9.0.post0)
2026-10-02T07:35:42.2286656Z Requirement already satisfied: six>=1.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas->Py-BOBYQA==1.5.0) (1.17.0)
2026-10-02T07:35:42.7541156Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages'
2026-10-02T07:35:42.7552080Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-02T07:35:42.7579859Z 
2026-10-02T07:35:42.7580535Z ================================================================================
2026-10-02T07:35:42.7580880Z sn.pantheonplus
2026-10-02T07:35:42.7581300Z ================================================================================
2026-10-02T07:35:42.7581495Z 
2026-10-02T07:35:42.7581661Z [install] Checking if dependencies have already been installed...
2026-10-02T07:35:42.7582524Z [install] External dependencies for this component already installed.
2026-10-02T07:35:42.7583107Z [install] Doing nothing.
2026-10-02T07:35:42.7583423Z 
2026-10-02T07:35:42.7583536Z ================================================================================
2026-10-02T07:35:42.7583796Z * Summary * 
2026-10-02T07:35:42.7584009Z ================================================================================
2026-10-02T07:35:42.7584207Z 
2026-10-02T07:35:42.7584608Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:35:42.8824907Z Q042_MPI_TOOLCHAIN_GATE=PASS mpicc=/usr/bin/mpicc mpifort=/usr/bin/mpifort
2026-10-02T07:35:43.0306591Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-02T07:35:43.0405316Z make: Nothing to be done for 'libchord.so'.
2026-10-02T07:35:43.0405707Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-02T07:35:43.2235403Z Processing ./external/PolyChordLite
2026-10-02T07:35:43.2242530Z   Preparing metadata (pyproject.toml): started
2026-10-02T07:35:43.6476921Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-10-02T07:35:43.6490851Z Building wheels for collected packages: pypolychord
2026-10-02T07:35:43.6496138Z   Building wheel for pypolychord (pyproject.toml): started
2026-10-02T07:35:43.9773959Z   Building wheel for pypolychord (pyproject.toml): finished with status 'done'
2026-10-02T07:35:43.9784159Z   Created wheel for pypolychord: filename=pypolychord-1.22.2-cp311-cp311-linux_x86_64.whl size=374446 sha256=26d531ac684697062bf6b3fec18c57efd730b5a86b49730702f72cdd71158d11
2026-10-02T07:35:43.9785160Z   Stored in directory: /tmp/pip-ephem-wheel-cache-m18t70bs/wheels/b9/80/45/d967b892eb659dbd8b31b85b9ee242adcb1da43378c684d8d5
2026-10-02T07:35:43.9800522Z Successfully built pypolychord
2026-10-02T07:35:43.9871233Z Installing collected packages: pypolychord
2026-10-02T07:35:44.0092044Z Successfully installed pypolychord-1.22.2
2026-10-02T07:35:44.5462496Z Q042_V11_RUNTIME_SOURCE_GATE=PASS polychord_commit=3ade6445bb3719a6db6f6e81f178765545ffc833 pantheon_files=6
2026-10-02T07:35:44.7339474Z Q042_PROD_V1_RUNTIME_SOURCE_GATE=PASS
2026-10-02T07:35:44.7537188Z Q042_PROD_V8_RECOVERED_RUNTIME_GATE=PASS
2026-10-02T07:35:44.7818900Z Q042_POLYCHORD_PARTIAL_INIT_SOURCE_PATCH_GATE=PASS
2026-10-02T07:35:44.7902540Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-02T07:35:44.7902922Z rm -f *.o *.mod *.MOD
2026-10-02T07:35:44.7915807Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-02T07:35:44.7925735Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-02T07:35:44.8024335Z make -C /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/lib/libchord.so
2026-10-02T07:35:44.8035669Z make[1]: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-02T07:35:44.8036264Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c utils.F90
2026-10-02T07:35:46.8773010Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c abort.F90
2026-10-02T07:35:46.9442609Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c array_utils.f90
2026-10-02T07:35:47.4449890Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c settings.f90
2026-10-02T07:35:47.5236545Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c calculate.f90
2026-10-02T07:35:47.6390933Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c mpi_utils.F90
2026-10-02T07:35:47.7033759Z mpi_utils.F90:627:12:
2026-10-02T07:35:47.7034005Z 
2026-10-02T07:35:47.7034177Z   627 |             empty_buffer,                &! not sending anything
2026-10-02T07:35:47.7034504Z       |            1
2026-10-02T07:35:47.7034707Z ......
2026-10-02T07:35:47.7034934Z   655 |             live_point,                  &! live point being sent
2026-10-02T07:35:47.7035216Z       |            2
2026-10-02T07:35:47.7035596Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-02T07:35:47.7036000Z mpi_utils.F90:581:12:
2026-10-02T07:35:47.7036117Z 
2026-10-02T07:35:47.7036253Z   581 |             logL,                        &!
2026-10-02T07:35:47.7036498Z       |            1
2026-10-02T07:35:47.7036669Z ......
2026-10-02T07:35:47.7036885Z   655 |             live_point,                  &! live point being sent
2026-10-02T07:35:47.7037144Z       |            2
2026-10-02T07:35:47.7037498Z Warning: Rank mismatch between actual argument at (1) and actual argument at (2) (rank-1 and scalar)
2026-10-02T07:35:47.7037906Z mpi_utils.F90:517:12:
2026-10-02T07:35:47.7038034Z 
2026-10-02T07:35:47.7038134Z   517 |             logL,                        &!
2026-10-02T07:35:47.7038375Z       |            1
2026-10-02T07:35:47.7038541Z ......
2026-10-02T07:35:47.7038749Z   680 |             live_point,                  &! live point recieved
2026-10-02T07:35:47.7039019Z       |            2
2026-10-02T07:35:47.7039371Z Warning: Rank mismatch between actual argument at (1) and actual argument at (2) (rank-1 and scalar)
2026-10-02T07:35:47.7039737Z mpi_utils.F90:527:12:
2026-10-02T07:35:47.7039864Z 
2026-10-02T07:35:47.7039965Z   527 |             epoch,                       &!
2026-10-02T07:35:47.7040208Z       |            1
2026-10-02T07:35:47.7040373Z ......
2026-10-02T07:35:47.7040580Z   680 |             live_point,                  &! live point recieved
2026-10-02T07:35:47.7040838Z       |            2
2026-10-02T07:35:47.7041203Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-02T07:35:47.7041600Z mpi_utils.F90:275:12:
2026-10-02T07:35:47.7041715Z 
2026-10-02T07:35:47.7041834Z   275 |             doubles,                     &!broadcast buffer
2026-10-02T07:35:47.7042097Z       |            1
2026-10-02T07:35:47.7042511Z ......
2026-10-02T07:35:47.7042729Z   291 |             integers,                    &!broadcast buffer
2026-10-02T07:35:47.7042998Z       |            2
2026-10-02T07:35:47.7043362Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (REAL(8)/INTEGER(4)).
2026-10-02T07:35:47.7043781Z mpi_utils.F90:240:12:
2026-10-02T07:35:47.7043903Z 
2026-10-02T07:35:47.7044028Z   240 |             intgr_local,                 &!send buffer
2026-10-02T07:35:47.7044298Z       |            1
2026-10-02T07:35:47.7044473Z ......
2026-10-02T07:35:47.7044670Z   258 |             db_local,                    &!send buffer
2026-10-02T07:35:47.7044930Z       |            2
2026-10-02T07:35:47.7045289Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-02T07:35:47.7045691Z mpi_utils.F90:241:12:
2026-10-02T07:35:47.7045813Z 
2026-10-02T07:35:47.7045939Z   241 |             intgr,                       &!recieve buffer
2026-10-02T07:35:47.7046214Z       |            1
2026-10-02T07:35:47.7046394Z ......
2026-10-02T07:35:47.7046604Z   259 |             db,                          &!recieve buffer
2026-10-02T07:35:47.7046867Z       |            2
2026-10-02T07:35:47.7047526Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-02T07:35:47.8828835Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c random_utils.F90
2026-10-02T07:35:48.2165122Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c chordal_sampling.f90
2026-10-02T07:35:48.4719952Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c run_time_info.f90
2026-10-02T07:35:49.4124133Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c clustering.f90
2026-10-02T07:35:49.9452001Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c params.f90
2026-10-02T07:35:50.0355987Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c priors.f90
2026-10-02T07:35:50.9422465Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c read_write.F90
2026-10-02T07:35:51.7437788Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c feedback.f90
2026-10-02T07:35:51.9165836Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c generate.F90
2026-10-02T07:35:52.2180614Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c ini.f90
2026-10-02T07:35:52.4365204Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c nelder_mead.f90
2026-10-02T07:35:52.7217410Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c maximiser.F90
2026-10-02T07:35:52.9591982Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c nested_sampling.F90
2026-10-02T07:35:53.2764918Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c interfaces.F90
2026-10-02T07:35:53.5444905Z mpicxx -std=c++11 -fPIC -Ofast -DUSE_MPI -c c_interface.cpp
2026-10-02T07:35:56.2758265Z mpifort -shared abort.o array_utils.o calculate.o chordal_sampling.o clustering.o feedback.o generate.o ini.o interfaces.o maximiser.o mpi_utils.o nelder_mead.o nested_sampling.o params.o priors.o random_utils.o read_write.o run_time_info.o settings.o utils.o c_interface.o -o /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/lib/libchord.so -lstdc++ -Wl,-z,noexecstack 
2026-10-02T07:35:56.3464792Z make[1]: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-02T07:35:56.3465694Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-02T07:36:03.9853919Z Q042_POLYCHORD_PATCHED_BINARY_SYMBOL_GATE=PASS
2026-10-02T07:36:04.1642596Z Processing ./external/PolyChordLite
2026-10-02T07:36:04.1650398Z   Preparing metadata (pyproject.toml): started
2026-10-02T07:36:04.3872493Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-10-02T07:36:04.3887033Z Building wheels for collected packages: pypolychord
2026-10-02T07:36:04.3892636Z   Building wheel for pypolychord (pyproject.toml): started
2026-10-02T07:36:04.6963854Z   Building wheel for pypolychord (pyproject.toml): finished with status 'done'
2026-10-02T07:36:04.6972103Z   Created wheel for pypolychord: filename=pypolychord-1.22.2-cp311-cp311-linux_x86_64.whl size=379301 sha256=c64e1ebfa43160924b93109167cb2320507943199d22b9c7742b657dda882196
2026-10-02T07:36:04.6973246Z   Stored in directory: /tmp/pip-ephem-wheel-cache-aviey63s/wheels/b9/80/45/d967b892eb659dbd8b31b85b9ee242adcb1da43378c684d8d5
2026-10-02T07:36:04.6987782Z Successfully built pypolychord
2026-10-02T07:36:04.7052156Z Installing collected packages: pypolychord
2026-10-02T07:36:04.7053070Z   Attempting uninstall: pypolychord
2026-10-02T07:36:04.7063396Z     Found existing installation: pypolychord 1.22.2
2026-10-02T07:36:04.7075928Z     Uninstalling pypolychord-1.22.2:
2026-10-02T07:36:04.7830380Z       Successfully uninstalled pypolychord-1.22.2
2026-10-02T07:36:04.8059441Z Successfully installed pypolychord-1.22.2
2026-10-02T07:36:05.5943894Z 
2026-10-02T07:36:05.5944512Z PolyChord: Next Generation Nested Sampling
2026-10-02T07:36:05.5944865Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-02T07:36:05.5945120Z   version: 1.22.2
2026-10-02T07:36:05.5945291Z   release: 10th Jan 2024
2026-10-02T07:36:05.5945485Z     email: wh260@mrao.cam.ac.uk
2026-10-02T07:36:05.5945642Z 
2026-10-02T07:36:05.6143502Z  ____________________________________________________ 
2026-10-02T07:36:05.6143832Z |                                                    |
2026-10-02T07:36:05.6144026Z | ndead  =          100                              |
2026-10-02T07:36:05.6144244Z | log(Z) =           -0.09361 +/-            0.01161 |
2026-10-02T07:36:05.6144413Z |____________________________________________________|
2026-10-02T07:36:06.4151951Z 
2026-10-02T07:36:06.4152645Z PolyChord: Next Generation Nested Sampling
2026-10-02T07:36:06.4153025Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-02T07:36:06.4153281Z   version: 1.22.2
2026-10-02T07:36:06.4153461Z   release: 10th Jan 2024
2026-10-02T07:36:06.4153668Z     email: wh260@mrao.cam.ac.uk
2026-10-02T07:36:06.4153771Z 
2026-10-02T07:36:13.4131628Z 
2026-10-02T07:36:13.4132157Z PolyChord: Next Generation Nested Sampling
2026-10-02T07:36:13.4132658Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-02T07:36:13.4133046Z   version: 1.22.2
2026-10-02T07:36:13.4133467Z   release: 10th Jan 2024
2026-10-02T07:36:13.4133736Z     email: wh260@mrao.cam.ac.uk
2026-10-02T07:36:13.4133917Z 
2026-10-02T07:36:13.4173454Z  ____________________________________________________ 
2026-10-02T07:36:13.4187692Z |                                                    |
2026-10-02T07:36:13.4187953Z | ndead  =          100                              |
2026-10-02T07:36:13.4188234Z | log(Z) =           -0.09361 +/-            0.01161 |
2026-10-02T07:36:13.4188476Z |____________________________________________________|
2026-10-02T07:36:13.5703785Z Q042_POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_GATE_V17=PASS
2026-10-02T07:36:13.5945407Z Q042_PROD_V17_PARTIAL_INIT_RUNTIME_GATE=PASS
2026-10-02T07:36:14.0621306Z Q042_COBAYA_PARTIAL_RESUME_ADAPTER_SELFTEST_V18=PASS
2026-10-02T07:36:14.2005364Z Q042_PROD_V18_COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_GATE=PASS
2026-10-02T07:36:14.2075203Z ##[group]Run python q042_production_v18.py polychord-segment \
2026-10-02T07:36:14.2075613Z [36;1mpython q042_production_v18.py polychord-segment \[0m
2026-10-02T07:36:14.2075912Z [36;1m  --q032-parent-root q032_parent \[0m
2026-10-02T07:36:14.2076255Z [36;1m  --preflight env_bundle/q032_preflight/q032_preflight_sealed_v2.json \[0m
2026-10-02T07:36:14.2076633Z [36;1m  --parent-dir env_bundle/q032_parent_profiles \[0m
2026-10-02T07:36:14.2077004Z [36;1m  --hlp-matrix env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.npy \[0m
2026-10-02T07:36:14.2077446Z [36;1m  --hlp-meta env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.json \[0m
2026-10-02T07:36:14.2077959Z [36;1m  --reduced-support env_bundle/q042_environment/q042_primary_nonoverlap_support_prod_v18.json \[0m
2026-10-02T07:36:14.2078541Z [36;1m  --reduced-hlp-matrix env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.npy \[0m
2026-10-02T07:36:14.2079192Z [36;1m  --reduced-hlp-meta env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.json \[0m
2026-10-02T07:36:14.2079623Z [36;1m  --spec q042_production_spec_v1.json \[0m
2026-10-02T07:36:14.2079931Z [36;1m  --source-lock q042_production_source_lock_v18.json \[0m
2026-10-02T07:36:14.2080338Z [36;1m  --external-runtime q042_runtime/q042_external_runtime_provenance_prod_v1.json \[0m
2026-10-02T07:36:14.2080760Z [36;1m  --arm 'camspec' --model 'ede_n3' --combination 'FULL' \[0m
2026-10-02T07:36:14.2081168Z [36;1m  --segment '7' --soft-minutes 240 --mpi-ranks 1 --parent-run-id '36960394429' \[0m
2026-10-02T07:36:14.2081860Z [36;1m  --output-dir cell_state --segment-json q042_production_segment_v18.json || true[0m
2026-10-02T07:36:14.2141973Z shell: /usr/bin/bash -e {0}
2026-10-02T07:36:14.2142127Z env:
2026-10-02T07:36:14.2142375Z   CURRENT_Q: Q-042
2026-10-02T07:36:14.2142508Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T07:36:14.2142660Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T07:36:14.2142843Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T07:36:14.2143141Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T07:36:14.2143396Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T07:36:14.2143564Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T07:36:14.2143769Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T07:36:14.2144021Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T07:36:14.2144291Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:36:14.2144515Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T07:36:14.2144738Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:36:14.2144944Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:36:14.2145148Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T07:36:14.2145356Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T07:36:14.2145532Z ##[endgroup]
2026-10-02T07:36:15.0364923Z [output] Output to be read-from/written-into folder '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord', with prefix 'chain'
2026-10-02T07:36:15.0365753Z [output] Found existing info files with the requested output prefix: '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain'
2026-10-02T07:36:15.0366245Z [output] Let's try to resume/load.
2026-10-02T07:36:15.2294285Z [output] Found an old sample. Resuming.
2026-10-02T07:36:15.2373459Z [prior] *WARNING* External prior 'q041_act_calibration_shape' loaded. Mind that it might not be normalized!
2026-10-02T07:36:15.2388420Z [classy] `classy` module loaded successfully from /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/build/lib.linux-x86_64-cpython-311
2026-10-02T07:36:15.2389210Z [classy] *WARNING* Detected an old CLASS version (<3.3). Please update: support for this will be deprecated soon.
2026-10-02T07:36:15.2423604Z [planck_npipe_highl_camspec.ttteee] Using range {'143x143': [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599], '217x217': [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599], '143x217': [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599]}
2026-10-02T07:36:15.2950619Z [planck_npipe_highl_camspec.ttteee] L-range for 143x143: 30 2000
2026-10-02T07:36:15.2951048Z [planck_npipe_highl_camspec.ttteee] L-range for 217x217: 500 2500
2026-10-02T07:36:15.2951396Z [planck_npipe_highl_camspec.ttteee] L-range for 143x217: 500 2500
2026-10-02T07:36:15.2953962Z [planck_npipe_highl_camspec.ttteee] Number of data points: 750
2026-10-02T07:36:15.3323604Z [q019_shape_tau_reio] Initialized external likelihood.
2026-10-02T07:36:15.3343073Z [q019_shape_a_planck] Initialized external likelihood.
2026-10-02T07:36:15.5368028Z /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/sacc/sacc.py:935: UserWarning: The FITS format without the 'sacc_ordering' column is deprecated. Assuming data rows are in the correct order as it was before version 1.0.
2026-10-02T07:36:15.5368969Z   warnings.warn(
2026-10-02T07:36:22.1102168Z /home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_lenslike/act_dr6_lenslike/act_dr6_lenslike.py:422: UserWarning: Hartlap correction to cinv: 0.9860935524652339
2026-10-02T07:36:22.1103101Z   warnings.warn(f"Hartlap correction to cinv: {hartlap_correction}")
2026-10-02T07:36:22.1155832Z Loading ACT DR6 lensing likelihood v1.2...
2026-10-02T07:36:22.1156387Z [bao.desi_dr2] Initialized.
2026-10-02T07:36:22.6736571Z [polychord] *WARNING* This run has been SEEDED with seed 421100
2026-10-02T07:36:22.6818460Z [polychord] `pypolychord` module loaded successfully from /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord
2026-10-02T07:36:22.6843380Z [polychord] Storing raw PolyChord output in '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain_polychord_raw'.
2026-10-02T07:36:22.6873039Z [polychord] Parameter blocks and their oversampling factors:
2026-10-02T07:36:22.6873436Z [polychord] *  1 : ['tau_reio']
2026-10-02T07:36:22.6873855Z [polychord] *  1 : ['omega_b', 'omega_cdm', 'H0', 'n_s', 'logA', 'fEDE', 'log10z_c', 'thetai_scf']
2026-10-02T07:36:22.6874576Z [polychord] * 32 : ['A_act', 'P_act']
2026-10-02T07:36:22.6874845Z [polychord] * 46 : ['A_planck']
2026-10-02T07:36:22.6875198Z [polychord] * 51 : ['amp_143', 'amp_217', 'amp_143x217', 'n_143', 'n_217', 'n_143x217']
2026-10-02T07:36:22.6875949Z [prior] *WARNING* There are unbounded parameters (['A_planck']). Prior bounds are given at 0.9999995 confidence level. Beware of likelihood modes at the edge of the prior
2026-10-02T07:36:22.7387016Z [polychord] Calling PolyChord...
2026-10-02T07:36:23.0064430Z PolyChord: MPI is already initilised, not initialising, and will not finalize
2026-10-02T07:36:23.0064703Z 
2026-10-02T07:36:23.0064786Z PolyChord: Next Generation Nested Sampling
2026-10-02T07:36:23.0065000Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-02T07:36:23.0065177Z   version: 1.22.2
2026-10-02T07:36:23.0065309Z   release: 10th Jan 2024
2026-10-02T07:36:23.0065457Z     email: wh260@mrao.cam.ac.uk
2026-10-02T07:36:23.0065586Z 
2026-10-02T07:36:23.0065638Z Run Settings
2026-10-02T07:36:23.0065751Z nlive    :     450
2026-10-02T07:36:23.0065871Z nDims    :      18
2026-10-02T07:36:23.0065991Z nDerived :      17
2026-10-02T07:36:23.0066103Z Doing Clustering
2026-10-02T07:36:23.0066235Z Synchronous parallelisation
2026-10-02T07:36:23.0066391Z Generating equally weighted posteriors
2026-10-02T07:36:23.0066572Z Generating weighted posteriors
2026-10-02T07:36:23.0066715Z Clustering on posteriors
2026-10-02T07:36:23.0067027Z Writing a resume file to /home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain_polychord_raw/chain.resume
2026-10-02T07:36:23.0067288Z 
2026-10-02T07:36:23.1298155Z Resuming from previous run
2026-10-02T07:36:23.1298433Z number of repeats:            5          40         320         230        1530
2026-10-02T07:36:23.1298650Z started sampling
2026-10-02T07:36:23.1298727Z 
2026-10-02T11:36:18.3123484Z [exception handler] ---------------------------------------
2026-10-02T11:36:18.3123705Z 
2026-10-02T11:36:18.3123780Z Traceback (most recent call last):
2026-10-02T11:36:18.3131395Z   File "/home/runner/work/Bubbleverse/Bubbleverse/q042_production_v18.py", line 1309, in <module>
2026-10-02T11:36:18.3131719Z     raise SystemExit(a.func(a))
2026-10-02T11:36:18.3131861Z                      ^^^^^^^^^
2026-10-02T11:36:18.3132641Z   File "/home/runner/work/Bubbleverse/Bubbleverse/q042_production_v18.py", line 555, in polychord_worker
2026-10-02T11:36:18.3132897Z     _, sm = cobaya_run(
2026-10-02T11:36:18.3133017Z             ^^^^^^^^^^^
2026-10-02T11:36:18.3133272Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/run.py", line 146, in run
2026-10-02T11:36:18.3133530Z     sampler.run()
2026-10-02T11:36:18.3133807Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/samplers/polychord/polychord.py", line 266, in run
2026-10-02T11:36:18.3134166Z     self.pc.run_polychord(logpost, self.nDims, self.nDerived, self.pc_settings,
2026-10-02T11:36:18.3134597Z   File "/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord/polychord.py", line 177, in run_polychord
2026-10-02T11:36:18.3134955Z     _pypolychord.run(wrap_loglikelihood,
2026-10-02T11:36:18.3135324Z   File "/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord/polychord.py", line 163, in wrap_loglikelihood
2026-10-02T11:36:18.3135680Z     logL = loglikelihood(theta)
2026-10-02T11:36:18.3135812Z            ^^^^^^^^^^^^^^^^^^^^
2026-10-02T11:36:18.3136143Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/samplers/polychord/polychord.py", line 253, in logpost
2026-10-02T11:36:18.3136468Z     result = self.model.logposterior(params_values)
2026-10-02T11:36:18.3136638Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-02T11:36:18.3136920Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/model.py", line 558, in logposterior
2026-10-02T11:36:18.3137336Z     like = self._loglikes_input_params(input_params,
2026-10-02T11:36:18.3137505Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-02T11:36:18.3137802Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/model.py", line 378, in _loglikes_input_params
2026-10-02T11:36:18.3138117Z     compute_success = component.check_cache_and_compute(
2026-10-02T11:36:18.3138298Z                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-02T11:36:18.3138596Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/theory.py", line 253, in check_cache_and_compute
2026-10-02T11:36:18.3138930Z     if self.calculate(state, want_derived, **params_values_dict) is False:
2026-10-02T11:36:18.3139139Z        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-02T11:36:18.3139457Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/theories/classy/classy.py", line 557, in calculate
2026-10-02T11:36:18.3139753Z     self.classy.compute()
2026-10-02T11:36:18.3139884Z KeyboardInterrupt
2026-10-02T11:36:18.3140028Z -------------------------------------------------------------
2026-10-02T11:36:18.3140162Z 
2026-10-02T11:36:18.3140227Z [exception handler] Interrupted by the user.
2026-10-02T11:36:20.5311383Z Q042_PROD_V18_SEGMENT_STATUS=RESUME_NO_CHECKPOINT_PROGRESS
2026-10-02T11:36:20.5483980Z ##[group]Run python - <<'PY'
2026-10-02T11:36:20.5484233Z [36;1mpython - <<'PY'[0m
2026-10-02T11:36:20.5484416Z [36;1mimport json[0m
2026-10-02T11:36:20.5484638Z [36;1md=json.load(open('q042_production_segment_v18.json'))[0m
2026-10-02T11:36:20.5484910Z [36;1ma=(d.get('checkpoint_after') or {})[0m
2026-10-02T11:36:20.5485174Z [36;1mb=(d.get('checkpoint_before') or {})[0m
2026-10-02T11:36:20.5485451Z [36;1mprint('Q042_RELAY_STATUS='+str(d.get('status')))[0m
2026-10-02T11:36:20.5485755Z [36;1mprint('Q042_RELAY_KIND='+str(a.get('checkpoint_kind')))[0m
2026-10-02T11:36:20.5486149Z [36;1mprint('Q042_RELAY_PARTIAL_ACCEPTED_BEFORE='+str(b.get('partial_init_accepted')))[0m
2026-10-02T11:36:20.5486579Z [36;1mprint('Q042_RELAY_PARTIAL_ACCEPTED_AFTER='+str(a.get('partial_init_accepted')))[0m
2026-10-02T11:36:20.5487009Z [36;1mprint('Q042_RELAY_PROGRESS_REASON='+str(d.get('checkpoint_progress_reason')))[0m
2026-10-02T11:36:20.5487300Z [36;1mPY[0m
2026-10-02T11:36:20.5539277Z shell: /usr/bin/bash -e {0}
2026-10-02T11:36:20.5539413Z env:
2026-10-02T11:36:20.5539518Z   CURRENT_Q: Q-042
2026-10-02T11:36:20.5539636Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T11:36:20.5539779Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T11:36:20.5539946Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T11:36:20.5540143Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T11:36:20.5540323Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T11:36:20.5540491Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T11:36:20.5540692Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T11:36:20.5540943Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T11:36:20.5541204Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5541420Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T11:36:20.5541637Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5541833Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5542033Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5542371Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T11:36:20.5542549Z ##[endgroup]
2026-10-02T11:36:20.5755604Z Q042_RELAY_STATUS=RESUME_NO_CHECKPOINT_PROGRESS
2026-10-02T11:36:20.5755903Z Q042_RELAY_KIND=STOCK_RESUME
2026-10-02T11:36:20.5756133Z Q042_RELAY_PARTIAL_ACCEPTED_BEFORE=None
2026-10-02T11:36:20.5756380Z Q042_RELAY_PARTIAL_ACCEPTED_AFTER=None
2026-10-02T11:36:20.5756844Z Q042_RELAY_PROGRESS_REASON=STOCK_RESUME_UNCHANGED
2026-10-02T11:36:20.5804356Z ##[group]Run set -euo pipefail
2026-10-02T11:36:20.5804536Z [36;1mset -euo pipefail[0m
2026-10-02T11:36:20.5804782Z [36;1mSTATUS=$(python -c "import json;print(json.load(open('q042_production_segment_v18.json'))['status'])")[0m
2026-10-02T11:36:20.5805204Z [36;1mMAXSEG=$(python -c "import json;print(json.load(open('q042_production_spec_v1.json'))['orchestration']['max_polychord_segments_per_cell'])")[0m
2026-10-02T11:36:20.5805523Z [36;1mif [ "$STATUS" = COMPLETE ]; then[0m
2026-10-02T11:36:20.5805682Z [36;1m  echo 'final=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5805857Z [36;1m  echo 'checkpoint=no' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5806015Z [36;1m  python - <<'PY'[0m
2026-10-02T11:36:20.5806138Z [36;1mimport json[0m
2026-10-02T11:36:20.5806543Z [36;1md=json.load(open('q042_production_segment_v18.json'));d['stage']='POLYCHORD_PRODUCTION_FINAL_V18';d['status']='COMPLETE';json.dump(d,open('q042_production_polychord_final_v18.json','w'),indent=2,sort_keys=True)[0m
2026-10-02T11:36:20.5806945Z [36;1mPY[0m
2026-10-02T11:36:20.5807121Z [36;1melif [ "$STATUS" = SEGMENT_CHECKPOINTED ] && [ "$SEG" -lt $((MAXSEG-1)) ]; then[0m
2026-10-02T11:36:20.5807332Z [36;1m  NEXT=$((SEG+1))[0m
2026-10-02T11:36:20.5807468Z [36;1m  echo 'final=no' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5807637Z [36;1m  echo 'checkpoint=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5807805Z [36;1m  echo "next=$NEXT" >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5807953Z [36;1melse[0m
2026-10-02T11:36:20.5808071Z [36;1m  echo 'final=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5808235Z [36;1m  echo 'checkpoint=no' >> "$GITHUB_OUTPUT"[0m
2026-10-02T11:36:20.5808387Z [36;1m  python - <<'PY'[0m
2026-10-02T11:36:20.5808509Z [36;1mimport json[0m
2026-10-02T11:36:20.5808658Z [36;1md=json.load(open('q042_production_segment_v18.json'))[0m
2026-10-02T11:36:20.5808851Z [36;1md['stage']='POLYCHORD_PRODUCTION_FINAL_V18'[0m
2026-10-02T11:36:20.5809170Z [36;1md['status']='CONTROLLED_MAX_SEGMENTS_WITHOUT_CONVERGENCE' if d['status']=='SEGMENT_CHECKPOINTED' else 'CONTROLLED_TECHNICAL_FAILURE'[0m
2026-10-02T11:36:20.5809549Z [36;1mjson.dump(d,open('q042_production_polychord_final_v18.json','w'),indent=2,sort_keys=True)[0m
2026-10-02T11:36:20.5809770Z [36;1mPY[0m
2026-10-02T11:36:20.5809868Z [36;1mfi[0m
2026-10-02T11:36:20.5856169Z shell: /usr/bin/bash -e {0}
2026-10-02T11:36:20.5856299Z env:
2026-10-02T11:36:20.5856500Z   CURRENT_Q: Q-042
2026-10-02T11:36:20.5856640Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T11:36:20.5856782Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T11:36:20.5856953Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T11:36:20.5857148Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T11:36:20.5857336Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T11:36:20.5857499Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T11:36:20.5857704Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T11:36:20.5857953Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T11:36:20.5858212Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5858432Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T11:36:20.5858647Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5858842Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5859039Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.5859239Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T11:36:20.5859412Z   SEG: 7
2026-10-02T11:36:20.5859512Z ##[endgroup]
2026-10-02T11:36:20.6509648Z ##[group]Run actions/upload-artifact@v4
2026-10-02T11:36:20.6509810Z with:
2026-10-02T11:36:20.6509971Z   name: q042-v18-36731879692-polychord-final-camspec-ede_n3-FULL
2026-10-02T11:36:20.6510334Z   path: cell_state/**
q042_production_polychord_final_v18.json

2026-10-02T11:36:20.6510517Z   if-no-files-found: error
2026-10-02T11:36:20.6510647Z   retention-days: 30
2026-10-02T11:36:20.6510764Z   compression-level: 6
2026-10-02T11:36:20.6510880Z   overwrite: false
2026-10-02T11:36:20.6510998Z   include-hidden-files: false
2026-10-02T11:36:20.6511143Z env:
2026-10-02T11:36:20.6511243Z   CURRENT_Q: Q-042
2026-10-02T11:36:20.6511357Z   PROGRAM_ID: Q042-PROD-V18
2026-10-02T11:36:20.6511498Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-02T11:36:20.6511664Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-02T11:36:20.6511859Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-02T11:36:20.6512036Z   V1_ROOT_RUN_ID: 36133813540
2026-10-02T11:36:20.6512352Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-02T11:36:20.6512559Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-02T11:36:20.6512808Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-02T11:36:20.6513076Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.6513294Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-02T11:36:20.6513508Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.6513703Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.6513902Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-02T11:36:20.6514102Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-02T11:36:20.6514270Z ##[endgroup]
2026-10-02T11:36:20.7549075Z (node:5600) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-02T11:36:20.7549568Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-02T11:36:20.7645082Z Multiple search paths detected. Calculating the least common ancestor of all paths
2026-10-02T11:36:20.7646567Z The least common ancestor is /home/runner/work/Bubbleverse/Bubbleverse. This will be the root directory of the artifact
2026-10-02T11:36:20.7647055Z With the provided path, there will be 18 files uploaded
2026-10-02T11:36:20.7650268Z Artifact name is valid!
2026-10-02T11:36:20.7650630Z Root directory input is valid!
2026-10-02T11:36:21.1470283Z Beginning upload of artifact content to blob storage
2026-10-02T11:36:21.7501333Z (node:5600) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-02T11:36:22.5396485Z Uploaded bytes 8388608
2026-10-02T11:36:22.6267080Z Uploaded bytes 10038491
2026-10-02T11:36:22.6890622Z Finished uploading artifact content to blob storage!
2026-10-02T11:36:22.6891408Z SHA256 digest of uploaded artifact zip is 01ac6da88043fbf84fde35713d717cf0b4ea0b53bf5b4d6d13527ada6f563bf6
2026-10-02T11:36:22.6892955Z Finalizing artifact upload
2026-10-02T11:36:22.9470799Z Artifact q042-v18-36731879692-polychord-final-camspec-ede_n3-FULL.zip successfully finalized. Artifact ID 11224420078
2026-10-02T11:36:22.9471435Z Artifact q042-v18-36731879692-polychord-final-camspec-ede_n3-FULL has been successfully uploaded! Final size is 10038491 bytes. Artifact ID is 11224420078
2026-10-02T11:36:22.9475905Z Artifact download URL: https://github.com/Morfindien/Bubbleverse/actions/runs/36979159417/artifacts/11224420078
2026-10-02T11:36:22.9612606Z Post job cleanup.
2026-10-02T11:36:23.0470341Z Post job cleanup.
2026-10-02T11:36:23.1017618Z [command]/usr/bin/git version
2026-10-02T11:36:23.1049520Z git version 2.55.0
2026-10-02T11:36:23.1073396Z Temporarily overriding HOME='/home/runner/work/_temp/618eb54b-5d3c-40c4-b35a-b29c084ed8be' before making global git config changes
2026-10-02T11:36:23.1073876Z Adding repository directory to the temporary git global config as a safe directory
2026-10-02T11:36:23.1076737Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/Bubbleverse/Bubbleverse
2026-10-02T11:36:23.1105737Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-02T11:36:23.1130620Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-02T11:36:23.1349109Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-02T11:36:23.1371745Z http.https://github.com/.extraheader
2026-10-02T11:36:23.1385658Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2026-10-02T11:36:23.1408320Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-02T11:36:23.1597464Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-02T11:36:23.1629322Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-02T11:36:23.1934554Z Cleaning up orphan processes
2026-10-02T11:36:23.2083100Z ##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/cache/restore@v4, actions/checkout@v4, actions/download-artifact@v4, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
```


## APPENDIX E2 — RAW CAMSPEC LCDM FULL TERMINAL JOB LOG

**Preserved UTF-8 source SHA-256:** `2d40de0b817d02372ee5ebfcc7ba044fcbba256787de0c096ec1b92560e1c0c3`; bytes: 134032.

```text
﻿2026-10-01T11:19:20.6489757Z Current runner version: '2.337.0'
2026-10-01T11:19:20.6511790Z ##[group]Runner Image Provisioner
2026-10-01T11:19:20.6512569Z Hosted Compute Agent
2026-10-01T11:19:20.6513074Z Version: 20260901.588
2026-10-01T11:19:20.6513720Z Commit: f88ec8081b781fac6c440065ac7ff9e710ce3d0b
2026-10-01T11:19:20.6514413Z Build Date: 2026-09-01T19:56:44Z
2026-10-01T11:19:20.6515053Z Worker ID: {5e58043a-092d-4e16-af0f-9892a5802fb9}
2026-10-01T11:19:20.6516141Z Azure Region: centralus
2026-10-01T11:19:20.6516650Z ##[endgroup]
2026-10-01T11:19:20.6517818Z ##[group]Operating System
2026-10-01T11:19:20.6518387Z Ubuntu
2026-10-01T11:19:20.6518857Z 24.04.5
2026-10-01T11:19:20.6519317Z LTS
2026-10-01T11:19:20.6519770Z ##[endgroup]
2026-10-01T11:19:20.6520298Z ##[group]Runner Image
2026-10-01T11:19:20.6520883Z Image: ubuntu-24.04
2026-10-01T11:19:20.6521381Z Version: 20260927.320.1
2026-10-01T11:19:20.6522549Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20260927.320/images/ubuntu/Ubuntu2404-Readme.md
2026-10-01T11:19:20.6524007Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20260927.320
2026-10-01T11:19:20.6524908Z ##[endgroup]
2026-10-01T11:19:20.6526328Z ##[group]GITHUB_TOKEN Permissions
2026-10-01T11:19:20.6528222Z Actions: write
2026-10-01T11:19:20.6528745Z Contents: read
2026-10-01T11:19:20.6529271Z Metadata: read
2026-10-01T11:19:20.6529753Z ##[endgroup]
2026-10-01T11:19:20.6531492Z Secret source: Actions
2026-10-01T11:19:20.6532311Z Cache mode: write
2026-10-01T11:19:20.6532932Z Prepare workflow directory
2026-10-01T11:19:20.6972777Z Prepare all required actions
2026-10-01T11:19:20.7017833Z Getting action download info
2026-10-01T11:19:20.9521547Z Download action repository 'actions/checkout@v4' (SHA:11d5960a326750d5838078e36cf38b85af677262)
2026-10-01T11:19:21.0488847Z Download action repository 'actions/setup-python@v7' (SHA:5fda3b95a4ea91299a34e894583c3862153e4b97)
2026-10-01T11:19:21.2275050Z Download action repository 'actions/cache@v4' (SHA:0057852bfaa89a56745cba8c7296529d2fc39830)
2026-10-01T11:19:21.3856002Z Download action repository 'actions/download-artifact@v4' (SHA:d3f86a106a0bac45b974a628896c90dbdf5c8093)
2026-10-01T11:19:21.8698681Z Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
2026-10-01T11:19:22.1374220Z Complete job name: polychord-continuation
2026-10-01T11:19:22.2030028Z ##[group]Run actions/checkout@v4
2026-10-01T11:19:22.2030894Z with:
2026-10-01T11:19:22.2031527Z   repository: Morfindien/Bubbleverse
2026-10-01T11:19:22.2038762Z   token: ***
2026-10-01T11:19:22.2039333Z   ssh-strict: true
2026-10-01T11:19:22.2039938Z   ssh-user: git
2026-10-01T11:19:22.2040468Z   persist-credentials: true
2026-10-01T11:19:22.2041106Z   clean: true
2026-10-01T11:19:22.2041647Z   sparse-checkout-cone-mode: true
2026-10-01T11:19:22.2042315Z   fetch-depth: 1
2026-10-01T11:19:22.2042879Z   fetch-tags: false
2026-10-01T11:19:22.2043413Z   show-progress: true
2026-10-01T11:19:22.2043965Z   lfs: false
2026-10-01T11:19:22.2044504Z   submodules: false
2026-10-01T11:19:22.2045049Z   set-safe-directory: true
2026-10-01T11:19:22.2045881Z   allow-unsafe-pr-checkout: false
2026-10-01T11:19:22.2046799Z env:
2026-10-01T11:19:22.2047288Z   CURRENT_Q: Q-042
2026-10-01T11:19:22.2047826Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:19:22.2048622Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:19:22.2049427Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:19:22.2050355Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:19:22.2051251Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:19:22.2052004Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:19:22.2052983Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:19:22.2054236Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:19:22.2055410Z ##[endgroup]
2026-10-01T11:19:22.2936201Z Syncing repository: Morfindien/Bubbleverse
2026-10-01T11:19:22.2939338Z ##[group]Getting Git version info
2026-10-01T11:19:22.2940567Z Working directory is '/home/runner/work/Bubbleverse/Bubbleverse'
2026-10-01T11:19:22.2942056Z [command]/usr/bin/git version
2026-10-01T11:19:22.2992643Z git version 2.55.0
2026-10-01T11:19:22.3012638Z ##[endgroup]
2026-10-01T11:19:22.3027256Z Temporarily overriding HOME='/home/runner/work/_temp/e7549b91-021d-4875-b93b-4f0a71c42ed3' before making global git config changes
2026-10-01T11:19:22.3030612Z Adding repository directory to the temporary git global config as a safe directory
2026-10-01T11:19:22.3034561Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/Bubbleverse/Bubbleverse
2026-10-01T11:19:22.3078783Z Deleting the contents of '/home/runner/work/Bubbleverse/Bubbleverse'
2026-10-01T11:19:22.3081455Z ##[group]Initializing the repository
2026-10-01T11:19:22.3085959Z [command]/usr/bin/git init /home/runner/work/Bubbleverse/Bubbleverse
2026-10-01T11:19:22.3160581Z hint: Using 'master' as the name for the initial branch. This default branch name
2026-10-01T11:19:22.3163398Z hint: will change to "main" in Git 3.0. To configure the initial branch name
2026-10-01T11:19:22.3166325Z hint: to use in all of your new repositories, which will suppress this warning,
2026-10-01T11:19:22.3167782Z hint: call:
2026-10-01T11:19:22.3168719Z hint:
2026-10-01T11:19:22.3170023Z hint: 	git config --global init.defaultBranch <name>
2026-10-01T11:19:22.3171165Z hint:
2026-10-01T11:19:22.3172521Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2026-10-01T11:19:22.3174310Z hint: 'development'. The just-created branch can be renamed via this command:
2026-10-01T11:19:22.3175823Z hint:
2026-10-01T11:19:22.3177072Z hint: 	git branch -m <name>
2026-10-01T11:19:22.3178183Z hint:
2026-10-01T11:19:22.3179729Z hint: Disable this message with "git config set advice.defaultBranchName false"
2026-10-01T11:19:22.3182288Z Initialized empty Git repository in /home/runner/work/Bubbleverse/Bubbleverse/.git/
2026-10-01T11:19:22.3186853Z [command]/usr/bin/git remote add origin https://github.com/Morfindien/Bubbleverse
2026-10-01T11:19:22.3244434Z ##[endgroup]
2026-10-01T11:19:22.3246021Z ##[group]Disabling automatic garbage collection
2026-10-01T11:19:22.3248749Z [command]/usr/bin/git config --local gc.auto 0
2026-10-01T11:19:22.3279060Z ##[endgroup]
2026-10-01T11:19:22.3280334Z ##[group]Setting up auth
2026-10-01T11:19:22.3286032Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-01T11:19:22.3313004Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-01T11:19:22.3605123Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-01T11:19:22.3632758Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-01T11:19:22.3803230Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-01T11:19:22.3829040Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-01T11:19:22.3991298Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-10-01T11:19:22.4025160Z ##[endgroup]
2026-10-01T11:19:22.4026501Z ##[group]Fetching the repository
2026-10-01T11:19:22.4032609Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +d0f92c7f2ce53da32818244f8847f8e745e20c4f:refs/remotes/origin/main
2026-10-01T11:19:23.1975502Z From https://github.com/Morfindien/Bubbleverse
2026-10-01T11:19:23.1976740Z  * [new ref]         d0f92c7f2ce53da32818244f8847f8e745e20c4f -> origin/main
2026-10-01T11:19:23.1979823Z ##[endgroup]
2026-10-01T11:19:23.1981137Z ##[group]Determining the checkout info
2026-10-01T11:19:23.1982917Z ##[endgroup]
2026-10-01T11:19:23.1987933Z [command]/usr/bin/git sparse-checkout disable
2026-10-01T11:19:23.2030053Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2026-10-01T11:19:23.2055655Z ##[group]Checking out the ref
2026-10-01T11:19:23.2058432Z [command]/usr/bin/git checkout --progress --force -B main refs/remotes/origin/main
2026-10-01T11:19:23.2606813Z Switched to a new branch 'main'
2026-10-01T11:19:23.2610037Z branch 'main' set up to track 'origin/main'.
2026-10-01T11:19:23.2616996Z ##[endgroup]
2026-10-01T11:19:23.2647919Z [command]/usr/bin/git log -1 --format=%H
2026-10-01T11:19:23.2666379Z d0f92c7f2ce53da32818244f8847f8e745e20c4f
2026-10-01T11:19:23.2932589Z ##[group]Run actions/setup-python@v7
2026-10-01T11:19:23.2933472Z with:
2026-10-01T11:19:23.2934264Z   python-version: 3.11
2026-10-01T11:19:23.2935096Z   check-latest: false
2026-10-01T11:19:23.2938456Z   token: ***
2026-10-01T11:19:23.2939250Z   update-environment: true
2026-10-01T11:19:23.2940154Z   allow-prereleases: false
2026-10-01T11:19:23.2940972Z   freethreaded: false
2026-10-01T11:19:23.2941772Z env:
2026-10-01T11:19:23.2942514Z   CURRENT_Q: Q-042
2026-10-01T11:19:23.2943275Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:19:23.2944109Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:19:23.2945014Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:19:23.2946162Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:19:23.2947083Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:19:23.2948005Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:19:23.2949059Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:19:23.2950154Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:19:23.2951169Z ##[endgroup]
2026-10-01T11:19:23.3969448Z ##[group]Installed versions
2026-10-01T11:19:23.4027936Z Successfully set up CPython (3.11.16)
2026-10-01T11:19:23.4030023Z ##[endgroup]
2026-10-01T11:19:23.4206487Z ##[group]Run test 'Q042-PROD-V18' = "$PROGRAM_ID"
2026-10-01T11:19:23.4208136Z [36;1mtest 'Q042-PROD-V18' = "$PROGRAM_ID"[0m
2026-10-01T11:19:23.4209384Z [36;1mtest -n '36731879692'[0m
2026-10-01T11:19:23.4210560Z [36;1mtest -n '36829393843'[0m
2026-10-01T11:19:23.4429459Z shell: /usr/bin/bash -e {0}
2026-10-01T11:19:23.4430418Z env:
2026-10-01T11:19:23.4431207Z   CURRENT_Q: Q-042
2026-10-01T11:19:23.4432011Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:19:23.4432886Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:19:23.4433778Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:19:23.4434783Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:19:23.4436134Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:19:23.4437039Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:19:23.4438011Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:19:23.4439240Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:19:23.4440324Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4441327Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:19:23.4442367Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4443307Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4444286Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4445272Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:19:23.4446271Z ##[endgroup]
2026-10-01T11:19:23.4629957Z ##[group]Run actions/cache/restore@v4
2026-10-01T11:19:23.4630838Z with:
2026-10-01T11:19:23.4632182Z   path: ~/.cache/pip
external/cobaya_packages
external/class_ede
external/hillipop
external/act_dr6_cmbonly
external/act_dr6_lenslike
external/cobaya_desi_dr2_source
external/bao_data_v2_6
external/PolyChordLite

2026-10-01T11:19:23.4633860Z   key: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-01T11:19:23.4634883Z   fail-on-cache-miss: true
2026-10-01T11:19:23.4635930Z   enableCrossOsArchive: false
2026-10-01T11:19:23.4636804Z   lookup-only: false
2026-10-01T11:19:23.4637661Z env:
2026-10-01T11:19:23.4638434Z   CURRENT_Q: Q-042
2026-10-01T11:19:23.4639283Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:19:23.4640157Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:19:23.4641094Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:19:23.4642062Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:19:23.4643141Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:19:23.4644081Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:19:23.4645081Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:19:23.4646376Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:19:23.4647494Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4648480Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:19:23.4649490Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4650449Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4651402Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:19:23.4652351Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:19:23.4653206Z ##[endgroup]
2026-10-01T11:19:23.5552586Z (node:2103) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-01T11:19:23.5554194Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-01T11:19:23.6997131Z Cache hit for: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-01T11:19:23.7078705Z (node:2103) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-01T11:19:24.8886410Z Received 104857600 of 2242870168 (4.7%), 99.9 MBs/sec
2026-10-01T11:19:25.8917824Z Received 310378496 of 2242870168 (13.8%), 147.7 MBs/sec
2026-10-01T11:19:26.8898501Z Received 490733568 of 2242870168 (21.9%), 155.7 MBs/sec
2026-10-01T11:19:27.9238189Z Received 671088640 of 2242870168 (29.9%), 158.5 MBs/sec
2026-10-01T11:19:28.9256564Z Received 838860800 of 2242870168 (37.4%), 158.7 MBs/sec
2026-10-01T11:19:29.9259662Z Received 1044381696 of 2242870168 (46.6%), 164.9 MBs/sec
2026-10-01T11:19:30.9267745Z Received 1207959552 of 2242870168 (53.9%), 163.6 MBs/sec
2026-10-01T11:19:31.9271359Z Received 1363148800 of 2242870168 (60.8%), 161.7 MBs/sec
2026-10-01T11:19:32.9277901Z Received 1522532352 of 2242870168 (67.9%), 160.6 MBs/sec
2026-10-01T11:19:33.9272642Z Received 1669332992 of 2242870168 (74.4%), 158.5 MBs/sec
2026-10-01T11:19:34.9277144Z Received 1837105152 of 2242870168 (81.9%), 158.7 MBs/sec
2026-10-01T11:19:35.9278417Z Received 1983905792 of 2242870168 (88.5%), 157.1 MBs/sec
2026-10-01T11:19:36.9287475Z Received 2122317824 of 2242870168 (94.6%), 155.2 MBs/sec
2026-10-01T11:19:37.7034665Z Received 2242870168 of 2242870168 (100.0%), 154.8 MBs/sec
2026-10-01T11:19:37.7045848Z Cache Size: ~2139 MB (2242870168 B)
2026-10-01T11:19:37.7234887Z [command]/usr/bin/tar -xf /home/runner/work/_temp/b4394894-e95d-4a2c-917c-1d6208ae6cd8/cache.tzst -P -C /home/runner/work/Bubbleverse/Bubbleverse --use-compress-program unzstd
2026-10-01T11:20:02.8097576Z Cache restored successfully
2026-10-01T11:20:02.8932651Z Cache restored from key: q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus
2026-10-01T11:20:02.9647684Z ##[group]Run sudo apt-get update -y
2026-10-01T11:20:02.9648148Z [36;1msudo apt-get update -y[0m
2026-10-01T11:20:02.9648672Z [36;1msudo apt-get install -y gfortran gcc g++ make openmpi-bin libopenmpi-dev pkg-config[0m
2026-10-01T11:20:02.9649344Z [36;1mgit fetch --depth 1 origin "$Q032_EXECUTION_COMMIT"[0m
2026-10-01T11:20:02.9649791Z [36;1mgit worktree add --detach q032_parent "$Q032_EXECUTION_COMMIT"[0m
2026-10-01T11:20:02.9686438Z shell: /usr/bin/bash -e {0}
2026-10-01T11:20:02.9686803Z env:
2026-10-01T11:20:02.9687116Z   CURRENT_Q: Q-042
2026-10-01T11:20:02.9687444Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:20:02.9687769Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:20:02.9688163Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:20:02.9688588Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:20:02.9689041Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:20:02.9689503Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:20:02.9690486Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:20:02.9690970Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:20:02.9691590Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:02.9692125Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:20:02.9692623Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:02.9693164Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:02.9693656Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:02.9694152Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:20:02.9694590Z ##[endgroup]
2026-10-01T11:20:03.3923849Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-10-01T11:20:03.4319992Z Hit:2 http://azure.archive.ubuntu.com/ubuntu noble InRelease
2026-10-01T11:20:03.4348137Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
2026-10-01T11:20:03.4698716Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
2026-10-01T11:20:03.4785002Z Get:6 https://packages.microsoft.com/ubuntu/24.04/prod noble InRelease [3600 B]
2026-10-01T11:20:03.5023281Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble-security InRelease [126 kB]
2026-10-01T11:20:03.5895325Z Get:7 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [1343 kB]
2026-10-01T11:20:03.7074825Z Get:8 http://azure.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [302 kB]
2026-10-01T11:20:03.7104858Z Get:9 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [181 kB]
2026-10-01T11:20:03.8511718Z Get:18 https://packages.microsoft.com/ubuntu/24.04/prod noble/main arm64 Packages [456 kB]
2026-10-01T11:20:03.9395552Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1699 kB]
2026-10-01T11:20:03.9476778Z Get:27 https://packages.microsoft.com/ubuntu/24.04/prod noble/main amd64 Packages [509 kB]
2026-10-01T11:20:03.9771774Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [341 kB]
2026-10-01T11:20:03.9847776Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [388 kB]
2026-10-01T11:20:03.9968648Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [1701 kB]
2026-10-01T11:20:04.0154941Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [389 kB]
2026-10-01T11:20:04.0240911Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
2026-10-01T11:20:04.0290873Z Get:16 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [5760 B]
2026-10-01T11:20:04.0772122Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [12.6 kB]
2026-10-01T11:20:04.0813031Z Get:19 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Packages [1066 kB]
2026-10-01T11:20:04.0980105Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble-security/main Translation-en [220 kB]
2026-10-01T11:20:04.1013532Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Components [46.4 kB]
2026-10-01T11:20:04.1163676Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1216 kB]
2026-10-01T11:20:04.1372821Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble-security/universe Translation-en [244 kB]
2026-10-01T11:20:04.1562836Z Get:24 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Components [76.3 kB]
2026-10-01T11:20:04.1796594Z Get:25 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [1566 kB]
2026-10-01T11:20:04.2186124Z Get:26 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted Translation-en [361 kB]
2026-10-01T11:20:11.5130922Z Fetched 12.5 MB in 2s (8289 kB/s)
2026-10-01T11:20:12.2867014Z Reading package lists...
2026-10-01T11:20:12.3170659Z Reading package lists...
2026-10-01T11:20:12.4779293Z Building dependency tree...
2026-10-01T11:20:12.4785540Z Reading state information...
2026-10-01T11:20:12.6349070Z gfortran is already the newest version (4:13.2.0-7ubuntu1).
2026-10-01T11:20:12.6350137Z gcc is already the newest version (4:13.2.0-7ubuntu1).
2026-10-01T11:20:12.6350709Z g++ is already the newest version (4:13.2.0-7ubuntu1).
2026-10-01T11:20:12.6351274Z make is already the newest version (4.3-4.1build2).
2026-10-01T11:20:12.6351778Z pkg-config is already the newest version (1.8.1-2build1).
2026-10-01T11:20:12.6352219Z The following additional packages will be installed:
2026-10-01T11:20:12.6352718Z   libamd-comgr2 libamdhip64-5 libcaf-openmpi-3t64 libcoarrays-dev
2026-10-01T11:20:12.6353191Z   libcoarrays-openmpi-dev libevent-2.1-7t64 libevent-core-2.1-7t64
2026-10-01T11:20:12.6353696Z   libevent-dev libevent-extra-2.1-7t64 libevent-openssl-2.1-7t64
2026-10-01T11:20:12.6354264Z   libevent-pthreads-2.1-7t64 libfabric1 libhsa-runtime64-1 libhsakmt1
2026-10-01T11:20:12.6354770Z   libhwloc-dev libhwloc-plugins libhwloc15 libibverbs-dev libjs-jquery-ui
2026-10-01T11:20:12.6355259Z   libltdl-dev libmunge2 libnl-3-dev libnl-route-3-dev libnuma-dev
2026-10-01T11:20:12.6355974Z   libopenmpi3t64 libpmix-dev libpmix2t64 libpsm-infinipath1 libpsm2-2
2026-10-01T11:20:12.6356707Z   librdmacm1t64 libucx0 libxnvctrl0 ocl-icd-libopencl1 openmpi-common
2026-10-01T11:20:12.6362656Z Suggested packages:
2026-10-01T11:20:12.6363278Z   libhwloc-contrib-plugins libjs-jquery-ui-docs libtool-doc openmpi-doc
2026-10-01T11:20:12.6363702Z   opencl-icd
2026-10-01T11:20:12.6783929Z The following NEW packages will be installed:
2026-10-01T11:20:12.6784650Z   libamd-comgr2 libamdhip64-5 libcaf-openmpi-3t64 libcoarrays-dev
2026-10-01T11:20:12.6785258Z   libcoarrays-openmpi-dev libevent-2.1-7t64 libevent-dev
2026-10-01T11:20:12.6785831Z   libevent-extra-2.1-7t64 libevent-openssl-2.1-7t64 libfabric1
2026-10-01T11:20:12.6786323Z   libhsa-runtime64-1 libhsakmt1 libhwloc-dev libhwloc-plugins libhwloc15
2026-10-01T11:20:12.6786788Z   libibverbs-dev libjs-jquery-ui libltdl-dev libmunge2 libnl-3-dev
2026-10-01T11:20:12.6787329Z   libnl-route-3-dev libnuma-dev libopenmpi-dev libopenmpi3t64 libpmix-dev
2026-10-01T11:20:12.6788738Z   libpmix2t64 libpsm-infinipath1 libpsm2-2 librdmacm1t64 libucx0 libxnvctrl0
2026-10-01T11:20:12.6789871Z   ocl-icd-libopencl1 openmpi-bin openmpi-common
2026-10-01T11:20:12.6794208Z The following packages will be upgraded:
2026-10-01T11:20:12.6799205Z   libevent-core-2.1-7t64 libevent-pthreads-2.1-7t64
2026-10-01T11:20:12.6955735Z 2 upgraded, 34 newly installed, 0 to remove and 22 not upgraded.
2026-10-01T11:20:12.6956298Z Need to get 38.3 MB of archives.
2026-10-01T11:20:12.6956802Z After this operation, 145 MB of additional disk space will be used.
2026-10-01T11:20:12.6957236Z Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
2026-10-01T11:20:12.7572825Z Get:2 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libamd-comgr2 amd64 6.0+git20231212.4510c28+dfsg-3build2 [14.4 MB]
2026-10-01T11:20:13.0841395Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhsakmt1 amd64 5.7.0-1build1 [62.9 kB]
2026-10-01T11:20:13.2080651Z Get:4 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhsa-runtime64-1 amd64 5.7.1-2build1 [491 kB]
2026-10-01T11:20:13.3275968Z Get:5 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libamdhip64-5 amd64 5.7.1-3 [9621 kB]
2026-10-01T11:20:13.4670154Z Get:6 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-pthreads-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [7988 B]
2026-10-01T11:20:13.4984087Z Get:7 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-core-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [91.9 kB]
2026-10-01T11:20:13.5339884Z Get:8 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpsm-infinipath1 amd64 3.3+20.604758e7-6.3build1 [178 kB]
2026-10-01T11:20:13.5730641Z Get:9 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpsm2-2 amd64 11.2.185-2build1 [194 kB]
2026-10-01T11:20:13.6136207Z Get:10 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 librdmacm1t64 amd64 50.0-2ubuntu0.2 [70.7 kB]
2026-10-01T11:20:13.6545717Z Get:11 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libfabric1 amd64 1.17.0-3build2 [657 kB]
2026-10-01T11:20:13.7040384Z Get:12 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc15 amd64 2.10.0-1build1 [172 kB]
2026-10-01T11:20:13.7438295Z Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 libmunge2 amd64 0.5.15-4ubuntu0.1 [14.8 kB]
2026-10-01T11:20:13.7823867Z Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libxnvctrl0 amd64 510.47.03-0ubuntu4.24.04.1 [12.7 kB]
2026-10-01T11:20:13.8206967Z Get:15 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 ocl-icd-libopencl1 amd64 2.3.2-1build1 [38.5 kB]
2026-10-01T11:20:13.8595929Z Get:16 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc-plugins amd64 2.10.0-1build1 [15.7 kB]
2026-10-01T11:20:13.8912898Z Get:17 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpmix2t64 amd64 5.0.1-4.1build1 [697 kB]
2026-10-01T11:20:14.0677312Z Get:18 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libucx0 amd64 1.16.0+ds-5ubuntu1 [1140 kB]
2026-10-01T11:20:14.1418746Z Get:19 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libopenmpi3t64 amd64 4.1.6-7ubuntu2 [2563 kB]
2026-10-01T11:20:14.2364324Z Get:20 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcaf-openmpi-3t64 amd64 2.10.2+ds-2.1build2 [39.1 kB]
2026-10-01T11:20:14.2722205Z Get:21 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcoarrays-dev amd64 2.10.2+ds-2.1build2 [37.5 kB]
2026-10-01T11:20:14.3080758Z Get:22 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 openmpi-common all 4.1.6-7ubuntu2 [170 kB]
2026-10-01T11:20:14.3367285Z Get:23 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 openmpi-bin amd64 4.1.6-7ubuntu2 [114 kB]
2026-10-01T11:20:14.3650172Z Get:24 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libcoarrays-openmpi-dev amd64 2.10.2+ds-2.1build2 [372 kB]
2026-10-01T11:20:14.3952568Z Get:25 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [146 kB]
2026-10-01T11:20:14.4236213Z Get:26 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-extra-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [64.6 kB]
2026-10-01T11:20:14.4595531Z Get:27 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-openssl-2.1-7t64 amd64 2.1.12-stable-9ubuntu2.2 [15.8 kB]
2026-10-01T11:20:14.4950345Z Get:28 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libevent-dev amd64 2.1.12-stable-9ubuntu2.2 [274 kB]
2026-10-01T11:20:14.5340659Z Get:29 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libjs-jquery-ui all 1.13.2+dfsg-1 [252 kB]
2026-10-01T11:20:14.5717772Z Get:30 http://azure.archive.ubuntu.com/ubuntu noble/main amd64 libltdl-dev amd64 2.4.7-7build1 [168 kB]
2026-10-01T11:20:14.6079686Z Get:31 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnl-3-dev amd64 3.7.0-0.3build1.1 [99.5 kB]
2026-10-01T11:20:14.6439176Z Get:32 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnl-route-3-dev amd64 3.7.0-0.3build1.1 [216 kB]
2026-10-01T11:20:14.6810946Z Get:33 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libnuma-dev amd64 2.0.18-1ubuntu0.24.04.1 [37.0 kB]
2026-10-01T11:20:14.7166592Z Get:34 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libhwloc-dev amd64 2.10.0-1build1 [268 kB]
2026-10-01T11:20:14.7558170Z Get:35 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libpmix-dev amd64 5.0.1-4.1build1 [4018 kB]
2026-10-01T11:20:14.8357367Z Get:36 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 libibverbs-dev amd64 50.0-2ubuntu0.2 [686 kB]
2026-10-01T11:20:14.8779315Z Get:37 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 libopenmpi-dev amd64 4.1.6-7ubuntu2 [864 kB]
2026-10-01T11:20:15.1378804Z Fetched 38.3 MB in 2s (17.4 MB/s)
2026-10-01T11:20:15.1628971Z Selecting previously unselected package libamd-comgr2:amd64.
2026-10-01T11:20:15.1770444Z (Reading database ... 
2026-10-01T11:20:15.1771056Z (Reading database ... 5%
2026-10-01T11:20:15.1771430Z (Reading database ... 10%
2026-10-01T11:20:15.1771842Z (Reading database ... 15%
2026-10-01T11:20:15.1772242Z (Reading database ... 20%
2026-10-01T11:20:15.1772597Z (Reading database ... 25%
2026-10-01T11:20:15.1772979Z (Reading database ... 30%
2026-10-01T11:20:15.1773302Z (Reading database ... 35%
2026-10-01T11:20:15.1774040Z (Reading database ... 40%
2026-10-01T11:20:15.1774405Z (Reading database ... 45%
2026-10-01T11:20:15.1774804Z (Reading database ... 50%
2026-10-01T11:20:15.1802949Z (Reading database ... 55%
2026-10-01T11:20:15.3388346Z (Reading database ... 60%
2026-10-01T11:20:15.5296050Z (Reading database ... 65%
2026-10-01T11:20:15.7337900Z (Reading database ... 70%
2026-10-01T11:20:15.9389560Z (Reading database ... 75%
2026-10-01T11:20:16.0816785Z (Reading database ... 80%
2026-10-01T11:20:16.2873566Z (Reading database ... 85%
2026-10-01T11:20:16.4776470Z (Reading database ... 90%
2026-10-01T11:20:16.6407540Z (Reading database ... 95%
2026-10-01T11:20:16.6408199Z (Reading database ... 100%
2026-10-01T11:20:16.6409049Z (Reading database ... 202296 files and directories currently installed.)
2026-10-01T11:20:16.6451020Z Preparing to unpack .../00-libamd-comgr2_6.0+git20231212.4510c28+dfsg-3build2_amd64.deb ...
2026-10-01T11:20:16.6568849Z Unpacking libamd-comgr2:amd64 (6.0+git20231212.4510c28+dfsg-3build2) ...
2026-10-01T11:20:17.1571393Z Selecting previously unselected package libhsakmt1:amd64.
2026-10-01T11:20:17.1680711Z Preparing to unpack .../01-libhsakmt1_5.7.0-1build1_amd64.deb ...
2026-10-01T11:20:17.1690706Z Unpacking libhsakmt1:amd64 (5.7.0-1build1) ...
2026-10-01T11:20:17.1858057Z Selecting previously unselected package libhsa-runtime64-1.
2026-10-01T11:20:17.1968553Z Preparing to unpack .../02-libhsa-runtime64-1_5.7.1-2build1_amd64.deb ...
2026-10-01T11:20:17.1977969Z Unpacking libhsa-runtime64-1 (5.7.1-2build1) ...
2026-10-01T11:20:17.2321389Z Selecting previously unselected package libamdhip64-5.
2026-10-01T11:20:17.2433512Z Preparing to unpack .../03-libamdhip64-5_5.7.1-3_amd64.deb ...
2026-10-01T11:20:17.2444014Z Unpacking libamdhip64-5 (5.7.1-3) ...
2026-10-01T11:20:17.4614527Z Preparing to unpack .../04-libevent-pthreads-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:17.4701840Z Unpacking libevent-pthreads-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) over (2.1.12-stable-9ubuntu2.1) ...
2026-10-01T11:20:17.5013368Z Preparing to unpack .../05-libevent-core-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:17.5244614Z Unpacking libevent-core-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) over (2.1.12-stable-9ubuntu2.1) ...
2026-10-01T11:20:17.5488071Z Selecting previously unselected package libpsm-infinipath1.
2026-10-01T11:20:17.5604881Z Preparing to unpack .../06-libpsm-infinipath1_3.3+20.604758e7-6.3build1_amd64.deb ...
2026-10-01T11:20:17.5614937Z Unpacking libpsm-infinipath1 (3.3+20.604758e7-6.3build1) ...
2026-10-01T11:20:17.5818964Z Selecting previously unselected package libpsm2-2.
2026-10-01T11:20:17.5930147Z Preparing to unpack .../07-libpsm2-2_11.2.185-2build1_amd64.deb ...
2026-10-01T11:20:17.5940717Z Unpacking libpsm2-2 (11.2.185-2build1) ...
2026-10-01T11:20:17.6137008Z Selecting previously unselected package librdmacm1t64:amd64.
2026-10-01T11:20:17.6246442Z Preparing to unpack .../08-librdmacm1t64_50.0-2ubuntu0.2_amd64.deb ...
2026-10-01T11:20:17.6255800Z Unpacking librdmacm1t64:amd64 (50.0-2ubuntu0.2) ...
2026-10-01T11:20:17.6430015Z Selecting previously unselected package libfabric1:amd64.
2026-10-01T11:20:17.6537979Z Preparing to unpack .../09-libfabric1_1.17.0-3build2_amd64.deb ...
2026-10-01T11:20:17.6551585Z Unpacking libfabric1:amd64 (1.17.0-3build2) ...
2026-10-01T11:20:17.6840821Z Selecting previously unselected package libhwloc15:amd64.
2026-10-01T11:20:17.6950157Z Preparing to unpack .../10-libhwloc15_2.10.0-1build1_amd64.deb ...
2026-10-01T11:20:17.6957165Z Unpacking libhwloc15:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:17.7136085Z Selecting previously unselected package libmunge2:amd64.
2026-10-01T11:20:17.7244294Z Preparing to unpack .../11-libmunge2_0.5.15-4ubuntu0.1_amd64.deb ...
2026-10-01T11:20:17.7251845Z Unpacking libmunge2:amd64 (0.5.15-4ubuntu0.1) ...
2026-10-01T11:20:17.7559698Z Selecting previously unselected package libxnvctrl0:amd64.
2026-10-01T11:20:17.7673327Z Preparing to unpack .../12-libxnvctrl0_510.47.03-0ubuntu4.24.04.1_amd64.deb ...
2026-10-01T11:20:17.7682074Z Unpacking libxnvctrl0:amd64 (510.47.03-0ubuntu4.24.04.1) ...
2026-10-01T11:20:17.7833304Z Selecting previously unselected package ocl-icd-libopencl1:amd64.
2026-10-01T11:20:17.7943512Z Preparing to unpack .../13-ocl-icd-libopencl1_2.3.2-1build1_amd64.deb ...
2026-10-01T11:20:17.7951307Z Unpacking ocl-icd-libopencl1:amd64 (2.3.2-1build1) ...
2026-10-01T11:20:17.8153202Z Selecting previously unselected package libhwloc-plugins:amd64.
2026-10-01T11:20:17.8262226Z Preparing to unpack .../14-libhwloc-plugins_2.10.0-1build1_amd64.deb ...
2026-10-01T11:20:17.8269129Z Unpacking libhwloc-plugins:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:17.8412438Z Selecting previously unselected package libpmix2t64:amd64.
2026-10-01T11:20:17.8519114Z Preparing to unpack .../15-libpmix2t64_5.0.1-4.1build1_amd64.deb ...
2026-10-01T11:20:17.8525629Z Unpacking libpmix2t64:amd64 (5.0.1-4.1build1) ...
2026-10-01T11:20:17.8942069Z Selecting previously unselected package libucx0:amd64.
2026-10-01T11:20:17.9053395Z Preparing to unpack .../16-libucx0_1.16.0+ds-5ubuntu1_amd64.deb ...
2026-10-01T11:20:17.9060116Z Unpacking libucx0:amd64 (1.16.0+ds-5ubuntu1) ...
2026-10-01T11:20:17.9430394Z Selecting previously unselected package libopenmpi3t64:amd64.
2026-10-01T11:20:17.9541538Z Preparing to unpack .../17-libopenmpi3t64_4.1.6-7ubuntu2_amd64.deb ...
2026-10-01T11:20:17.9550079Z Unpacking libopenmpi3t64:amd64 (4.1.6-7ubuntu2) ...
2026-10-01T11:20:18.0683374Z Selecting previously unselected package libcaf-openmpi-3t64:amd64.
2026-10-01T11:20:18.0795784Z Preparing to unpack .../18-libcaf-openmpi-3t64_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-01T11:20:18.0803745Z Unpacking libcaf-openmpi-3t64:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:18.0954490Z Selecting previously unselected package libcoarrays-dev:amd64.
2026-10-01T11:20:18.1066125Z Preparing to unpack .../19-libcoarrays-dev_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-01T11:20:18.1209861Z Unpacking libcoarrays-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:18.1372661Z Selecting previously unselected package openmpi-common.
2026-10-01T11:20:18.1494499Z Preparing to unpack .../20-openmpi-common_4.1.6-7ubuntu2_all.deb ...
2026-10-01T11:20:18.1500820Z Unpacking openmpi-common (4.1.6-7ubuntu2) ...
2026-10-01T11:20:18.1718440Z Selecting previously unselected package openmpi-bin.
2026-10-01T11:20:18.1830888Z Preparing to unpack .../21-openmpi-bin_4.1.6-7ubuntu2_amd64.deb ...
2026-10-01T11:20:18.1836670Z Unpacking openmpi-bin (4.1.6-7ubuntu2) ...
2026-10-01T11:20:18.2084154Z Selecting previously unselected package libcoarrays-openmpi-dev:amd64.
2026-10-01T11:20:18.2194615Z Preparing to unpack .../22-libcoarrays-openmpi-dev_2.10.2+ds-2.1build2_amd64.deb ...
2026-10-01T11:20:18.2201455Z Unpacking libcoarrays-openmpi-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:18.2764572Z Selecting previously unselected package libevent-2.1-7t64:amd64.
2026-10-01T11:20:18.2876294Z Preparing to unpack .../23-libevent-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:18.2884640Z Unpacking libevent-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:18.3057911Z Selecting previously unselected package libevent-extra-2.1-7t64:amd64.
2026-10-01T11:20:18.3169009Z Preparing to unpack .../24-libevent-extra-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:18.3176057Z Unpacking libevent-extra-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:18.3334156Z Selecting previously unselected package libevent-openssl-2.1-7t64:amd64.
2026-10-01T11:20:18.3445524Z Preparing to unpack .../25-libevent-openssl-2.1-7t64_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:18.3451428Z Unpacking libevent-openssl-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:18.3595196Z Selecting previously unselected package libevent-dev.
2026-10-01T11:20:18.3705454Z Preparing to unpack .../26-libevent-dev_2.1.12-stable-9ubuntu2.2_amd64.deb ...
2026-10-01T11:20:18.3711420Z Unpacking libevent-dev (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:18.3957321Z Selecting previously unselected package libjs-jquery-ui.
2026-10-01T11:20:18.4069083Z Preparing to unpack .../27-libjs-jquery-ui_1.13.2+dfsg-1_all.deb ...
2026-10-01T11:20:18.4077343Z Unpacking libjs-jquery-ui (1.13.2+dfsg-1) ...
2026-10-01T11:20:18.5071208Z Selecting previously unselected package libltdl-dev:amd64.
2026-10-01T11:20:18.5184317Z Preparing to unpack .../28-libltdl-dev_2.4.7-7build1_amd64.deb ...
2026-10-01T11:20:18.5191956Z Unpacking libltdl-dev:amd64 (2.4.7-7build1) ...
2026-10-01T11:20:18.5466615Z Selecting previously unselected package libnl-3-dev:amd64.
2026-10-01T11:20:18.5580000Z Preparing to unpack .../29-libnl-3-dev_3.7.0-0.3build1.1_amd64.deb ...
2026-10-01T11:20:18.5589479Z Unpacking libnl-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-01T11:20:18.5919621Z Selecting previously unselected package libnl-route-3-dev:amd64.
2026-10-01T11:20:18.6034423Z Preparing to unpack .../30-libnl-route-3-dev_3.7.0-0.3build1.1_amd64.deb ...
2026-10-01T11:20:18.6045281Z Unpacking libnl-route-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-01T11:20:18.6278723Z Selecting previously unselected package libnuma-dev:amd64.
2026-10-01T11:20:18.6392333Z Preparing to unpack .../31-libnuma-dev_2.0.18-1ubuntu0.24.04.1_amd64.deb ...
2026-10-01T11:20:18.6399378Z Unpacking libnuma-dev:amd64 (2.0.18-1ubuntu0.24.04.1) ...
2026-10-01T11:20:18.6583378Z Selecting previously unselected package libhwloc-dev:amd64.
2026-10-01T11:20:18.6694757Z Preparing to unpack .../32-libhwloc-dev_2.10.0-1build1_amd64.deb ...
2026-10-01T11:20:18.6701299Z Unpacking libhwloc-dev:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:18.6968478Z Selecting previously unselected package libpmix-dev:amd64.
2026-10-01T11:20:18.7079191Z Preparing to unpack .../33-libpmix-dev_5.0.1-4.1build1_amd64.deb ...
2026-10-01T11:20:18.7320083Z Unpacking libpmix-dev:amd64 (5.0.1-4.1build1) ...
2026-10-01T11:20:18.8682407Z Selecting previously unselected package libibverbs-dev:amd64.
2026-10-01T11:20:18.8795864Z Preparing to unpack .../34-libibverbs-dev_50.0-2ubuntu0.2_amd64.deb ...
2026-10-01T11:20:18.8804025Z Unpacking libibverbs-dev:amd64 (50.0-2ubuntu0.2) ...
2026-10-01T11:20:18.9294637Z Selecting previously unselected package libopenmpi-dev:amd64.
2026-10-01T11:20:18.9407734Z Preparing to unpack .../35-libopenmpi-dev_4.1.6-7ubuntu2_amd64.deb ...
2026-10-01T11:20:18.9718615Z Unpacking libopenmpi-dev:amd64 (4.1.6-7ubuntu2) ...
2026-10-01T11:20:19.2700311Z Setting up libcoarrays-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:19.2719610Z Setting up libevent-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.2737164Z Setting up libnuma-dev:amd64 (2.0.18-1ubuntu0.24.04.1) ...
2026-10-01T11:20:19.2754921Z Setting up libxnvctrl0:amd64 (510.47.03-0ubuntu4.24.04.1) ...
2026-10-01T11:20:19.2771150Z Setting up libltdl-dev:amd64 (2.4.7-7build1) ...
2026-10-01T11:20:19.2787382Z Setting up libjs-jquery-ui (1.13.2+dfsg-1) ...
2026-10-01T11:20:19.2803474Z Setting up libmunge2:amd64 (0.5.15-4ubuntu0.1) ...
2026-10-01T11:20:19.2819877Z Setting up libhwloc15:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:19.2835991Z Setting up libnl-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-01T11:20:19.2850848Z Setting up ocl-icd-libopencl1:amd64 (2.3.2-1build1) ...
2026-10-01T11:20:19.2867043Z Setting up libpsm2-2 (11.2.185-2build1) ...
2026-10-01T11:20:19.2882671Z Setting up openmpi-common (4.1.6-7ubuntu2) ...
2026-10-01T11:20:19.2898725Z Setting up librdmacm1t64:amd64 (50.0-2ubuntu0.2) ...
2026-10-01T11:20:19.2914890Z Setting up libhwloc-dev:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:19.2930437Z Setting up libevent-core-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.2945886Z Setting up libamd-comgr2:amd64 (6.0+git20231212.4510c28+dfsg-3build2) ...
2026-10-01T11:20:19.2961660Z Setting up libpsm-infinipath1 (3.3+20.604758e7-6.3build1) ...
2026-10-01T11:20:19.3008511Z update-alternatives: using /usr/lib/libpsm1/libpsm_infinipath.so.1.16 to provide /usr/lib/x86_64-linux-gnu/libpsm_infinipath.so.1 (libpsm_infinipath.so.1) in auto mode
2026-10-01T11:20:19.3020603Z Setting up libhsakmt1:amd64 (5.7.0-1build1) ...
2026-10-01T11:20:19.3037006Z Setting up libfabric1:amd64 (1.17.0-3build2) ...
2026-10-01T11:20:19.3053709Z Setting up libevent-pthreads-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.3070061Z Setting up libevent-openssl-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.3086322Z Setting up libhwloc-plugins:amd64 (2.10.0-1build1) ...
2026-10-01T11:20:19.3102206Z Setting up libnl-route-3-dev:amd64 (3.7.0-0.3build1.1) ...
2026-10-01T11:20:19.3117732Z Setting up libpmix2t64:amd64 (5.0.1-4.1build1) ...
2026-10-01T11:20:19.3133794Z Setting up libevent-extra-2.1-7t64:amd64 (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.3149417Z Setting up libhsa-runtime64-1 (5.7.1-2build1) ...
2026-10-01T11:20:19.3165645Z Setting up libibverbs-dev:amd64 (50.0-2ubuntu0.2) ...
2026-10-01T11:20:19.3181016Z Setting up libamdhip64-5 (5.7.1-3) ...
2026-10-01T11:20:19.3196996Z Setting up libevent-dev (2.1.12-stable-9ubuntu2.2) ...
2026-10-01T11:20:19.3213320Z Setting up libpmix-dev:amd64 (5.0.1-4.1build1) ...
2026-10-01T11:20:19.3229122Z Setting up libucx0:amd64 (1.16.0+ds-5ubuntu1) ...
2026-10-01T11:20:19.3245450Z Setting up libopenmpi3t64:amd64 (4.1.6-7ubuntu2) ...
2026-10-01T11:20:19.3262003Z Setting up openmpi-bin (4.1.6-7ubuntu2) ...
2026-10-01T11:20:19.3326183Z update-alternatives: using /usr/bin/mpirun.openmpi to provide /usr/bin/mpirun (mpirun) in auto mode
2026-10-01T11:20:19.3361607Z update-alternatives: using /usr/bin/mpicc.openmpi to provide /usr/bin/mpicc (mpi) in auto mode
2026-10-01T11:20:19.3386276Z Setting up libcaf-openmpi-3t64:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:19.3402716Z Setting up libopenmpi-dev:amd64 (4.1.6-7ubuntu2) ...
2026-10-01T11:20:19.3447139Z update-alternatives: using /usr/lib/x86_64-linux-gnu/openmpi/include to provide /usr/include/x86_64-linux-gnu/mpi (mpi-x86_64-linux-gnu) in auto mode
2026-10-01T11:20:19.3463338Z Setting up libcoarrays-openmpi-dev:amd64 (2.10.2+ds-2.1build2) ...
2026-10-01T11:20:19.3506743Z update-alternatives: using /usr/lib/x86_64-linux-gnu/open-coarrays/openmpi/bin/caf to provide /usr/bin/caf.openmpi (caf-openmpi) in auto mode
2026-10-01T11:20:19.3538361Z update-alternatives: using /usr/bin/caf.openmpi to provide /usr/bin/caf (caf) in auto mode
2026-10-01T11:20:19.3558427Z Processing triggers for libc-bin (2.39-0ubuntu8.9) ...
2026-10-01T11:20:19.5258486Z Processing triggers for man-db (2.12.0-4build2) ...
2026-10-01T11:20:19.5278457Z Not building database; man-db/auto-update is not 'true'.
2026-10-01T11:20:20.0149451Z 
2026-10-01T11:20:20.0150637Z Running kernel seems to be up-to-date.
2026-10-01T11:20:20.0151016Z 
2026-10-01T11:20:20.0151325Z No services need to be restarted.
2026-10-01T11:20:20.0151625Z 
2026-10-01T11:20:20.0151792Z No containers need to be restarted.
2026-10-01T11:20:20.0152083Z 
2026-10-01T11:20:20.0152287Z No user sessions are running outdated binaries.
2026-10-01T11:20:20.0152608Z 
2026-10-01T11:20:20.0152970Z No VM guests are running outdated hypervisor (qemu) binaries on this host.
2026-10-01T11:20:21.2162608Z From https://github.com/Morfindien/Bubbleverse
2026-10-01T11:20:21.2163368Z  * branch            4dc873a5e880d40858d831a3b421456728f0c032 -> FETCH_HEAD
2026-10-01T11:20:21.2182072Z Preparing worktree (detached HEAD 4dc873a)
2026-10-01T11:20:21.2471745Z HEAD is now at 4dc873a Rename q032-planck-tt3pair-bridge-v2.yml to .github/workflows/q032-planck-tt3pair-bridge-v2.yml
2026-10-01T11:20:21.2543027Z ##[group]Run actions/download-artifact@v4
2026-10-01T11:20:21.2543370Z with:
2026-10-01T11:20:21.2545959Z   github-token: ***
2026-10-01T11:20:21.2546282Z   run-id: 36731879692
2026-10-01T11:20:21.2546607Z   name: q042-v18-36731879692-environment
2026-10-01T11:20:21.2546959Z   path: env_bundle
2026-10-01T11:20:21.2547253Z   merge-multiple: false
2026-10-01T11:20:21.2547552Z   repository: Morfindien/Bubbleverse
2026-10-01T11:20:21.2547868Z env:
2026-10-01T11:20:21.2548182Z   CURRENT_Q: Q-042
2026-10-01T11:20:21.2548463Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:20:21.2548794Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:20:21.2549154Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:20:21.2549610Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:20:21.2550005Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:20:21.2550370Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:20:21.2550913Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:20:21.2551412Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:20:21.2551943Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:21.2552381Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:20:21.2552811Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:21.2553278Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:21.2553665Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:21.2554103Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:20:21.2554456Z ##[endgroup]
2026-10-01T11:20:21.3854656Z Downloading single artifact
2026-10-01T11:20:21.3913288Z (node:2945) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-01T11:20:21.3914421Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-01T11:20:21.4073028Z (node:2945) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-01T11:20:21.6693961Z Preparing to download the following artifacts:
2026-10-01T11:20:21.6695020Z - q042-v18-36731879692-environment (ID: 11104699558, Size: 278493088, Expected Digest: sha256:cc9d05fd514f50e64e4e1f56a6ecb1a9046ba43373491a9023f465a015e7d905)
2026-10-01T11:20:21.6724579Z Downloading artifact '11104699558' from 'Morfindien/Bubbleverse'
2026-10-01T11:20:21.8729410Z Redirecting to blob download url: https://productionresultssa3.blob.core.windows.net/actions-results/2c197768-5f79-49c7-b6da-cd466920b916/workflow-job-run-496d5009-1d18-5828-9622-8cb0335918ef/artifacts/05922946e67ed61a98ae0dbd7f4a02ecde010c0e90b1b08fa70fc13ec27b0e95.zip
2026-10-01T11:20:21.8730688Z Starting download of artifact to: /home/runner/work/Bubbleverse/Bubbleverse/env_bundle
2026-10-01T11:20:22.1318012Z (node:2945) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
2026-10-01T11:20:28.7470635Z SHA256 digest of downloaded artifact is cc9d05fd514f50e64e4e1f56a6ecb1a9046ba43373491a9023f465a015e7d905
2026-10-01T11:20:28.7471673Z Artifact download completed successfully.
2026-10-01T11:20:28.7472141Z Total of 1 artifact(s) downloaded
2026-10-01T11:20:28.7476191Z Download artifact has finished successfully
2026-10-01T11:20:28.7577687Z ##[group]Run set -euo pipefail
2026-10-01T11:20:28.7578104Z [36;1mset -euo pipefail[0m
2026-10-01T11:20:28.7578416Z [36;1mP=$((PREV_SEG-1))[0m
2026-10-01T11:20:28.7578801Z [36;1mgh run download "$PREV_RUN" --repo "$GITHUB_REPOSITORY" \[0m
2026-10-01T11:20:28.7579312Z [36;1m  --name "q042-v18-${ROOT}-checkpoint-${ARM}-${MODEL}-${COMBO}-s${P}" --dir previous[0m
2026-10-01T11:20:28.7579812Z [36;1mcp -a previous/cell_state ./cell_state[0m
2026-10-01T11:20:28.7580151Z [36;1mpython - <<'PY'[0m
2026-10-01T11:20:28.7580468Z [36;1mimport json,os[0m
2026-10-01T11:20:28.7580854Z [36;1mp=json.load(open('previous/q042_production_segment_v18.json'))[0m
2026-10-01T11:20:28.7581349Z [36;1massert p['q']=='Q-042' and p['program_id']=='Q042-PROD-V18'[0m
2026-10-01T11:20:28.7581892Z [36;1massert p['arm']==os.environ['ARM'] and p['model']==os.environ['MODEL'] and p['combination']==os.environ['COMBO'][0m
2026-10-01T11:20:28.7582556Z [36;1massert int(p['segment'])==int(os.environ['PREV_SEG'])-1[0m
2026-10-01T11:20:28.7582975Z [36;1massert p['status']=='SEGMENT_CHECKPOINTED'[0m
2026-10-01T11:20:28.7583640Z [36;1mprint('Q042_PROD_V18_CHECKPOINT_LINEAGE_GATE=PASS')[0m
2026-10-01T11:20:28.7583991Z [36;1mPY[0m
2026-10-01T11:20:28.7621954Z shell: /usr/bin/bash -e {0}
2026-10-01T11:20:28.7622304Z env:
2026-10-01T11:20:28.7622649Z   CURRENT_Q: Q-042
2026-10-01T11:20:28.7622933Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:20:28.7623265Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:20:28.7623699Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:20:28.7624105Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:20:28.7624513Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:20:28.7624871Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:20:28.7625523Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:20:28.7626028Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:20:28.7626524Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:28.7627020Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:20:28.7627451Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:28.7627885Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:28.7628283Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:28.7628719Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:20:28.7630941Z   GH_TOKEN: ***
2026-10-01T11:20:28.7631236Z   PREV_RUN: 36829393843
2026-10-01T11:20:28.7631565Z   PREV_SEG: 3
2026-10-01T11:20:28.7631825Z   ROOT: 36731879692
2026-10-01T11:20:28.7632092Z   ARM: camspec
2026-10-01T11:20:28.7632393Z   MODEL: lcdm
2026-10-01T11:20:28.7632634Z   COMBO: FULL
2026-10-01T11:20:28.7632943Z ##[endgroup]
2026-10-01T11:20:30.3509117Z Q042_PROD_V18_CHECKPOINT_LINEAGE_GATE=PASS
2026-10-01T11:20:30.3567085Z ##[group]Run bash q042_setup_recovery_v18.sh
2026-10-01T11:20:30.3567510Z [36;1mbash q042_setup_recovery_v18.sh[0m
2026-10-01T11:20:30.3605856Z shell: /usr/bin/bash -e {0}
2026-10-01T11:20:30.3606288Z env:
2026-10-01T11:20:30.3606567Z   CURRENT_Q: Q-042
2026-10-01T11:20:30.3606892Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:20:30.3607234Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:20:30.3607796Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:20:30.3608207Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:20:30.3608847Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:20:30.3609233Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:20:30.3609696Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:20:30.3610178Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:20:30.3610808Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:30.3611259Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:20:30.3611730Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:30.3612122Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:30.3612504Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:20:30.3612929Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:20:30.3613333Z ##[endgroup]
2026-10-01T11:20:30.3820351Z Q042_V4_Q032_CACHE_GATE=HIT
2026-10-01T11:20:30.8938480Z Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (26.2.1)
2026-10-01T11:20:31.3706250Z Collecting cobaya==3.5.6 (from -r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:31.3707208Z   Using cached cobaya-3.5.6-py3-none-any.whl
2026-10-01T11:20:31.4159953Z Collecting PyYAML==6.0.2 (from -r q005_hpc_v14_requirements.txt (line 2))
2026-10-01T11:20:31.4175003Z   Using cached PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
2026-10-01T11:20:31.5606916Z Collecting numpy==1.26.4 (from -r q005_hpc_v14_requirements.txt (line 3))
2026-10-01T11:20:31.5620384Z   Using cached numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
2026-10-01T11:20:31.6535187Z Collecting scipy==1.15.3 (from -r q005_hpc_v14_requirements.txt (line 4))
2026-10-01T11:20:31.6550354Z   Using cached scipy-1.15.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
2026-10-01T11:20:31.6789907Z Collecting Py-BOBYQA==1.5.0 (from -r q005_hpc_v14_requirements.txt (line 5))
2026-10-01T11:20:31.6801076Z   Using cached Py_BOBYQA-1.5.0-py3-none-any.whl.metadata (9.5 kB)
2026-10-01T11:20:31.6966607Z Collecting getdist==1.6.1 (from -r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:31.6967642Z   Using cached getdist-1.6.1-py3-none-any.whl
2026-10-01T11:20:31.8586546Z Collecting Cython==0.29.37 (from -r q005_hpc_v14_requirements.txt (line 7))
2026-10-01T11:20:31.8600927Z   Using cached Cython-0.29.37-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl.metadata (3.1 kB)
2026-10-01T11:20:31.8759947Z Collecting sacc==1.0.2 (from -r q005_hpc_v14_requirements.txt (line 8))
2026-10-01T11:20:31.8771104Z   Using cached sacc-1.0.2-py3-none-any.whl.metadata (2.4 kB)
2026-10-01T11:20:31.9982854Z Collecting pandas>=1.0.1 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:31.9995922Z   Using cached pandas-3.0.6-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (79 kB)
2026-10-01T11:20:32.0378373Z Collecting requests>=2.18 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.0390858Z   Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
2026-10-01T11:20:32.0551406Z Collecting fuzzywuzzy>=0.17 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.0563291Z   Using cached fuzzywuzzy-0.18.0-py2.py3-none-any.whl.metadata (4.9 kB)
2026-10-01T11:20:32.0741309Z Collecting packaging (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.0753478Z   Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
2026-10-01T11:20:32.1013212Z Collecting tqdm (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.1023043Z   Using cached tqdm-4.70.1-py3-none-any.whl.metadata (57 kB)
2026-10-01T11:20:32.1255775Z Collecting portalocker>=2.3.0 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.1267525Z   Using cached portalocker-4.4.0-py3-none-any.whl.metadata (10 kB)
2026-10-01T11:20:32.1423870Z Collecting dill>=0.3.3 (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.1435189Z   Using cached dill-0.4.1-py3-none-any.whl.metadata (10 kB)
2026-10-01T11:20:32.1613750Z Collecting typing_extensions (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:32.1625489Z   Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
2026-10-01T11:20:32.1655584Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0->-r q005_hpc_v14_requirements.txt (line 5)) (79.0.1)
2026-10-01T11:20:32.2590820Z Collecting matplotlib!=3.5.0,>=2.2.0 (from getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.2604272Z   Using cached matplotlib-3.11.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (80 kB)
2026-10-01T11:20:32.3678571Z Collecting astropy (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-01T11:20:32.3690752Z   Using cached astropy-8.0.1-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-01T11:20:32.4207199Z Collecting contourpy>=1.0.1 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.4218418Z   Using cached contourpy-1.3.3-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (5.5 kB)
2026-10-01T11:20:32.4366716Z Collecting cycler>=0.10 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.4378892Z   Using cached cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
2026-10-01T11:20:32.5720196Z Collecting fonttools>=4.28.2 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.6693506Z   Downloading fonttools-4.66.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (130 kB)
2026-10-01T11:20:32.7857421Z Collecting kiwisolver>=1.3.1 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.7869510Z   Using cached kiwisolver-1.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.2 kB)
2026-10-01T11:20:32.9254152Z Collecting pillow>=9 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.9268042Z   Using cached pillow-12.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (9.1 kB)
2026-10-01T11:20:32.9500249Z Collecting pyparsing>=3 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.9513080Z   Using cached pyparsing-3.3.3-py3-none-any.whl.metadata (5.9 kB)
2026-10-01T11:20:32.9673080Z Collecting python-dateutil>=2.7 (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.9685656Z   Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
2026-10-01T11:20:32.9888084Z Collecting six>=1.5 (from python-dateutil>=2.7->matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6))
2026-10-01T11:20:32.9901165Z   Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
2026-10-01T11:20:33.1004484Z Collecting charset_normalizer<4,>=2 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:33.1141141Z   Downloading charset_normalizer-3.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (46 kB)
2026-10-01T11:20:33.1463931Z Collecting idna<4,>=2.5 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:33.1476654Z   Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
2026-10-01T11:20:33.1686074Z Collecting urllib3<3,>=1.26 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:33.1698715Z   Using cached urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
2026-10-01T11:20:33.1888219Z Collecting certifi>=2023.5.7 (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1))
2026-10-01T11:20:33.1900672Z   Using cached certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
2026-10-01T11:20:33.2212570Z Collecting astropy-iers-data>=0.2026.6.22.1.23.34 (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-01T11:20:33.2349179Z   Downloading astropy_iers_data-0.2026.9.28.0.59.37-py3-none-any.whl.metadata (3.4 kB)
2026-10-01T11:20:33.2386766Z INFO: pip is looking at multiple versions of astropy to determine which version is compatible with other requirements. This could take a while.
2026-10-01T11:20:33.2391879Z Collecting astropy (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-01T11:20:33.2405880Z   Using cached astropy-8.0.0-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-01T11:20:33.2461801Z   Using cached astropy-7.2.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (11 kB)
2026-10-01T11:20:33.2754703Z Collecting pyerfa>=2.0.1.1 (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8))
2026-10-01T11:20:33.2767564Z   Using cached pyerfa-2.0.1.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.7 kB)
2026-10-01T11:20:33.2849817Z Using cached PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
2026-10-01T11:20:33.2865706Z Using cached numpy-1.26.4-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.3 MB)
2026-10-01T11:20:33.2939928Z Using cached scipy-1.15.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (37.7 MB)
2026-10-01T11:20:33.3077418Z Using cached Py_BOBYQA-1.5.0-py3-none-any.whl (57 kB)
2026-10-01T11:20:33.3088480Z Using cached Cython-0.29.37-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl (1.9 MB)
2026-10-01T11:20:33.3107024Z Using cached sacc-1.0.2-py3-none-any.whl (33 kB)
2026-10-01T11:20:33.3118549Z Using cached dill-0.4.1-py3-none-any.whl (120 kB)
2026-10-01T11:20:33.3130272Z Using cached fuzzywuzzy-0.18.0-py2.py3-none-any.whl (18 kB)
2026-10-01T11:20:33.3141905Z Using cached matplotlib-3.11.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (9.9 MB)
2026-10-01T11:20:33.3187879Z Using cached contourpy-1.3.3-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (355 kB)
2026-10-01T11:20:33.3200634Z Using cached cycler-0.12.1-py3-none-any.whl (8.3 kB)
2026-10-01T11:20:33.3331925Z Downloading fonttools-4.66.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.4 MB)
2026-10-01T11:20:33.4580446Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 48.2 MB/s  0:00:00
2026-10-01T11:20:33.4594935Z Using cached kiwisolver-1.5.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.4 MB)
2026-10-01T11:20:33.4613167Z Using cached packaging-26.3-py3-none-any.whl (129 kB)
2026-10-01T11:20:33.4625569Z Using cached pandas-3.0.6-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (11.1 MB)
2026-10-01T11:20:33.4675727Z Using cached pillow-12.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.9 MB)
2026-10-01T11:20:33.4711018Z Using cached portalocker-4.4.0-py3-none-any.whl (129 kB)
2026-10-01T11:20:33.4723026Z Using cached pyparsing-3.3.3-py3-none-any.whl (126 kB)
2026-10-01T11:20:33.4734760Z Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
2026-10-01T11:20:33.4747039Z Using cached requests-2.34.2-py3-none-any.whl (73 kB)
2026-10-01T11:20:33.4882592Z Downloading charset_normalizer-3.5.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (269 kB)
2026-10-01T11:20:33.4921076Z Using cached idna-3.20-py3-none-any.whl (69 kB)
2026-10-01T11:20:33.4932127Z Using cached urllib3-2.8.0-py3-none-any.whl (135 kB)
2026-10-01T11:20:33.4943809Z Using cached certifi-2026.7.22-py3-none-any.whl (136 kB)
2026-10-01T11:20:33.4955140Z Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
2026-10-01T11:20:33.4966783Z Using cached astropy-7.2.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (9.9 MB)
2026-10-01T11:20:33.5132761Z Downloading astropy_iers_data-0.2026.9.28.0.59.37-py3-none-any.whl (2.0 MB)
2026-10-01T11:20:33.5301574Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 118.1 MB/s  0:00:00
2026-10-01T11:20:33.5313965Z Using cached pyerfa-2.0.1.5-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (738 kB)
2026-10-01T11:20:33.5328661Z Using cached tqdm-4.70.1-py3-none-any.whl (80 kB)
2026-10-01T11:20:33.5340137Z Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
2026-10-01T11:20:33.8280707Z Installing collected packages: fuzzywuzzy, urllib3, typing_extensions, tqdm, six, PyYAML, pyparsing, portalocker, pillow, packaging, numpy, kiwisolver, idna, fonttools, dill, Cython, cycler, charset_normalizer, certifi, astropy-iers-data, scipy, requests, python-dateutil, pyerfa, contourpy, pandas, matplotlib, astropy, sacc, Py-BOBYQA, getdist, cobaya
2026-10-01T11:20:47.5186541Z 
2026-10-01T11:20:47.5203224Z Successfully installed Cython-0.29.37 Py-BOBYQA-1.5.0 PyYAML-6.0.2 astropy-7.2.2 astropy-iers-data-0.2026.9.28.0.59.37 certifi-2026.7.22 charset_normalizer-3.5.2 cobaya-3.5.6 contourpy-1.3.3 cycler-0.12.1 dill-0.4.1 fonttools-4.66.1 fuzzywuzzy-0.18.0 getdist-1.6.1 idna-3.20 kiwisolver-1.5.1 matplotlib-3.11.2 numpy-1.26.4 packaging-26.3 pandas-3.0.6 pillow-12.3.0 portalocker-4.4.0 pyerfa-2.0.1.5 pyparsing-3.3.3 python-dateutil-2.9.0.post0 requests-2.34.2 sacc-1.0.2 scipy-1.15.3 six-1.17.0 tqdm-4.70.1 typing_extensions-4.16.0 urllib3-2.8.0
2026-10-01T11:20:47.6857746Z Q017_V3_FROZEN_DEPENDENCY_GATE=PASS
2026-10-01T11:20:47.9848613Z HEAD is now at 5a131c91 Update README.md
2026-10-01T11:20:47.9884210Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/class_ede'
2026-10-01T11:20:47.9921289Z make: 'libclass.a' is up to date.
2026-10-01T11:20:47.9922961Z make: 'class' is up to date.
2026-10-01T11:20:47.9923851Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/class_ede'
2026-10-01T11:20:50.2419692Z warning: classy.pyx:363:76: local variable 'errmsg' referenced before assignment
2026-10-01T11:20:50.2420577Z warning: classy.pyx:364:39: local variable 'errmsg' referenced before assignment
2026-10-01T11:20:51.1343621Z In file included from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/ndarraytypes.h:1929,
2026-10-01T11:20:51.1344714Z                  from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
2026-10-01T11:20:51.1345787Z                  from /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/arrayobject.h:5,
2026-10-01T11:20:51.1346512Z                  from /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/../python/classy.c:752:
2026-10-01T11:20:51.1347552Z /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
2026-10-01T11:20:51.1348443Z    17 | #warning "Using deprecated NumPy API, disable it with " \
2026-10-01T11:20:51.1348885Z       |  ^~~~~~~
2026-10-01T11:21:10.5373014Z [INFO] cobaya-install planck_NPIPE_highl_CamSpec.TTTEEE attempt=1/4
2026-10-01T11:21:11.3575906Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages'
2026-10-01T11:21:11.3589636Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-01T11:21:11.3623853Z 
2026-10-01T11:21:11.3624149Z ================================================================================
2026-10-01T11:21:11.3624699Z planck_NPIPE_highl_CamSpec.TTTEEE
2026-10-01T11:21:11.3625292Z ================================================================================
2026-10-01T11:21:11.3626040Z 
2026-10-01T11:21:11.3626282Z [install] Checking if dependencies have already been installed...
2026-10-01T11:21:11.3627668Z [install] External dependencies for this component already installed.
2026-10-01T11:21:11.3628274Z [install] Doing nothing.
2026-10-01T11:21:11.3628554Z 
2026-10-01T11:21:11.3629055Z ================================================================================
2026-10-01T11:21:11.3629453Z * Summary * 
2026-10-01T11:21:11.3629853Z ================================================================================
2026-10-01T11:21:11.3630261Z 
2026-10-01T11:21:11.3630884Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages
2026-10-01T11:21:11.9535135Z Q017_V3_CLASS_EDE_GATE=PASS /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/build/lib.linux-x86_64-cpython-311/classy.cpython-311-x86_64-linux-gnu.so
2026-10-01T11:21:11.9536936Z Q017_V3_PLANCK_FULL_MF_INSTALL_GATE=PASS
2026-10-01T11:21:12.0820990Z Q017_V3_RUNTIME_PROVENANCE_GATE=PASS
2026-10-01T11:21:12.0892269Z Q017_V3_SETUP_GATE=PASS
2026-10-01T11:21:12.0966741Z Q032_PYTHON_311_GATE=PASS 3.11.16
2026-10-01T11:21:12.3229507Z Requirement already satisfied: cobaya==3.5.6 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 1)) (3.5.6)
2026-10-01T11:21:12.3232750Z Requirement already satisfied: PyYAML==6.0.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 2)) (6.0.2)
2026-10-01T11:21:12.3236556Z Requirement already satisfied: numpy==1.26.4 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 3)) (1.26.4)
2026-10-01T11:21:12.3240197Z Requirement already satisfied: scipy==1.15.3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 4)) (1.15.3)
2026-10-01T11:21:12.3243568Z Requirement already satisfied: Py-BOBYQA==1.5.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 5)) (1.5.0)
2026-10-01T11:21:12.3246895Z Requirement already satisfied: getdist==1.6.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 6)) (1.6.1)
2026-10-01T11:21:12.3250028Z Requirement already satisfied: Cython==0.29.37 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 7)) (0.29.37)
2026-10-01T11:21:12.3253700Z Requirement already satisfied: sacc==1.0.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from -r q005_hpc_v14_requirements.txt (line 8)) (1.0.2)
2026-10-01T11:21:12.3291210Z Requirement already satisfied: pandas>=1.0.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.0.6)
2026-10-01T11:21:12.3295090Z Requirement already satisfied: requests>=2.18 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2.34.2)
2026-10-01T11:21:12.3300513Z Requirement already satisfied: fuzzywuzzy>=0.17 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (0.18.0)
2026-10-01T11:21:12.3303466Z Requirement already satisfied: packaging in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (26.3)
2026-10-01T11:21:12.3306655Z Requirement already satisfied: tqdm in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.70.1)
2026-10-01T11:21:12.3310221Z Requirement already satisfied: portalocker>=2.3.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.4.0)
2026-10-01T11:21:12.3313532Z Requirement already satisfied: dill>=0.3.3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (0.4.1)
2026-10-01T11:21:12.3316653Z Requirement already satisfied: typing_extensions in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (4.16.0)
2026-10-01T11:21:12.3386875Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0->-r q005_hpc_v14_requirements.txt (line 5)) (79.0.1)
2026-10-01T11:21:12.3423969Z Requirement already satisfied: matplotlib!=3.5.0,>=2.2.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (3.11.2)
2026-10-01T11:21:12.3438958Z Requirement already satisfied: astropy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (7.2.2)
2026-10-01T11:21:12.3484777Z Requirement already satisfied: contourpy>=1.0.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.3.3)
2026-10-01T11:21:12.3488080Z Requirement already satisfied: cycler>=0.10 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (0.12.1)
2026-10-01T11:21:12.3491486Z Requirement already satisfied: fonttools>=4.28.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (4.66.1)
2026-10-01T11:21:12.3494897Z Requirement already satisfied: kiwisolver>=1.3.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.5.1)
2026-10-01T11:21:12.3500124Z Requirement already satisfied: pillow>=9 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (12.3.0)
2026-10-01T11:21:12.3503324Z Requirement already satisfied: pyparsing>=3 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (3.3.3)
2026-10-01T11:21:12.3507214Z Requirement already satisfied: python-dateutil>=2.7 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (2.9.0.post0)
2026-10-01T11:21:12.3662353Z Requirement already satisfied: six>=1.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from python-dateutil>=2.7->matplotlib!=3.5.0,>=2.2.0->getdist==1.6.1->-r q005_hpc_v14_requirements.txt (line 6)) (1.17.0)
2026-10-01T11:21:12.3672682Z Requirement already satisfied: charset_normalizer<4,>=2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.5.2)
2026-10-01T11:21:12.3676739Z Requirement already satisfied: idna<4,>=2.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (3.20)
2026-10-01T11:21:12.3680210Z Requirement already satisfied: urllib3<3,>=1.26 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2.8.0)
2026-10-01T11:21:12.3683782Z Requirement already satisfied: certifi>=2023.5.7 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from requests>=2.18->cobaya==3.5.6->-r q005_hpc_v14_requirements.txt (line 1)) (2026.7.22)
2026-10-01T11:21:12.3731211Z Requirement already satisfied: astropy-iers-data>=0.2026.6.22.1.23.34 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (0.2026.9.28.0.59.37)
2026-10-01T11:21:12.3736630Z Requirement already satisfied: pyerfa>=2.0.1.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy->sacc==1.0.2->-r q005_hpc_v14_requirements.txt (line 8)) (2.0.1.5)
2026-10-01T11:21:12.6934411Z Requirement already satisfied: astropy==7.2.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (7.2.2)
2026-10-01T11:21:12.6945065Z Requirement already satisfied: astropy-iers-data>=0.2026.6.22.1.23.34 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (0.2026.9.28.0.59.37)
2026-10-01T11:21:12.6949802Z Requirement already satisfied: numpy<2.7,>=1.24 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (1.26.4)
2026-10-01T11:21:12.6954096Z Requirement already satisfied: packaging>=22.0.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (26.3)
2026-10-01T11:21:12.6958127Z Requirement already satisfied: pyerfa>=2.0.1.1 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (2.0.1.5)
2026-10-01T11:21:12.6961722Z Requirement already satisfied: PyYAML>=6.0.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from astropy==7.2.2) (6.0.2)
2026-10-01T11:21:12.8393884Z Q032_FROZEN_DEPENDENCY_GATE=PASS
2026-10-01T11:21:13.0774752Z HEAD is now at 5a131c91 Update README.md
2026-10-01T11:21:13.4538932Z HEAD is now at a09ddde Merge pull request #36 from planck-npipe/v4.3
2026-10-01T11:21:13.6783616Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/hillipop
2026-10-01T11:21:13.6797302Z   Installing build dependencies: started
2026-10-01T11:21:14.5503553Z   Installing build dependencies: finished with status 'done'
2026-10-01T11:21:14.5508200Z   Checking if build backend supports build_editable: started
2026-10-01T11:21:14.7651849Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-01T11:21:14.7658278Z   Getting requirements to build editable: started
2026-10-01T11:21:15.2268737Z   Getting requirements to build editable: finished with status 'done'
2026-10-01T11:21:15.2276217Z   Preparing editable metadata (pyproject.toml): started
2026-10-01T11:21:15.5194128Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-01T11:21:15.5247587Z Building wheels for collected packages: planck_2020_hillipop
2026-10-01T11:21:15.5253164Z   Building editable for planck_2020_hillipop (pyproject.toml): started
2026-10-01T11:21:15.8470472Z   Building editable for planck_2020_hillipop (pyproject.toml): finished with status 'done'
2026-10-01T11:21:15.8475955Z   Created wheel for planck_2020_hillipop: filename=planck_2020_hillipop-4.3-0.editable-py3-none-any.whl size=30032 sha256=500d27053307bf8031849ce19b3eb8ed73292602feaa83b5005e560ab78d124f
2026-10-01T11:21:15.8477493Z   Stored in directory: /tmp/pip-ephem-wheel-cache-yqksz29d/wheels/ea/81/c6/7ed21441057e2523daefa6adbb44ef71baacfa55e2f6aacb52
2026-10-01T11:21:15.8533384Z Successfully built planck_2020_hillipop
2026-10-01T11:21:15.8615606Z Installing collected packages: planck_2020_hillipop
2026-10-01T11:21:15.8706545Z Successfully installed planck_2020_hillipop-4.3
2026-10-01T11:21:15.9234595Z [INFO] Q032 cobaya-install planck_2020_hillipop.TT attempt=1/4
2026-10-01T11:21:16.4858578Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages'
2026-10-01T11:21:16.4975466Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-01T11:21:16.6158715Z 
2026-10-01T11:21:16.6159992Z ================================================================================
2026-10-01T11:21:16.6160541Z planck_2020_hillipop.TT
2026-10-01T11:21:16.6160925Z ================================================================================
2026-10-01T11:21:16.6161152Z 
2026-10-01T11:21:16.6161365Z [install] Checking if dependencies have already been installed...
2026-10-01T11:21:16.6168917Z [install] External dependencies for this component already installed.
2026-10-01T11:21:16.6169490Z [install] Doing nothing.
2026-10-01T11:21:16.6169693Z 
2026-10-01T11:21:16.6169844Z ================================================================================
2026-10-01T11:21:16.6170211Z * Summary * 
2026-10-01T11:21:16.6170512Z ================================================================================
2026-10-01T11:21:16.6170779Z 
2026-10-01T11:21:16.6171187Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/q032_parent/external/cobaya_packages
2026-10-01T11:21:17.9757167Z Q032_BACKEND_IDENTITY_GATE=PASS
2026-10-01T11:21:17.9757632Z Q032_HILLIPOP_IMPLEMENTATION_IDENTITY_GATE=PASS
2026-10-01T11:21:17.9758136Z Q032_HILLIPOP_TT_DATA_GATE=PASS
2026-10-01T11:21:18.0878261Z Q032_CONTEXT_CONTINUITY_GATE=PASS
2026-10-01T11:21:18.0878733Z Q032_PYTHON_311_GATE=PASS
2026-10-01T11:21:18.1419872Z Q039_AUTHORITATIVE_Q032_CACHE_ENV_GATE=PASS
2026-10-01T11:21:18.2061125Z Q042_V4_FROZEN_Q032_CORE_GATE=PASS
2026-10-01T11:21:18.2745194Z Q041_FROZEN_CORE_DEPENDENCY_GATE=PASS
2026-10-01T11:21:18.5190873Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_cmbonly
2026-10-01T11:21:18.5200613Z   Installing build dependencies: started
2026-10-01T11:21:18.9588964Z   Installing build dependencies: finished with status 'done'
2026-10-01T11:21:18.9593432Z   Checking if build backend supports build_editable: started
2026-10-01T11:21:19.1664919Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-01T11:21:19.1670661Z   Getting requirements to build editable: started
2026-10-01T11:21:19.3142029Z   Getting requirements to build editable: finished with status 'done'
2026-10-01T11:21:19.3149935Z   Preparing editable metadata (pyproject.toml): started
2026-10-01T11:21:19.4656212Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-01T11:21:19.4685986Z Building wheels for collected packages: ACT-DR6-CMBonly
2026-10-01T11:21:19.4690859Z   Building editable for ACT-DR6-CMBonly (pyproject.toml): started
2026-10-01T11:21:19.6410443Z   Building editable for ACT-DR6-CMBonly (pyproject.toml): finished with status 'done'
2026-10-01T11:21:19.6414753Z   Created wheel for ACT-DR6-CMBonly: filename=act_dr6_cmbonly-1.0.0-0.editable-py3-none-any.whl size=2965 sha256=6dac5b6b7e9ef893258f455aa7b709a6f2417133f00e34cdcc986a3c1042a288
2026-10-01T11:21:19.6416802Z   Stored in directory: /tmp/pip-ephem-wheel-cache-s8ub8vmx/wheels/e9/00/d4/6bcdd39f247b8990a0d608a159e82446ce7b174bc7258a895b
2026-10-01T11:21:19.6433867Z Successfully built ACT-DR6-CMBonly
2026-10-01T11:21:19.6519314Z Installing collected packages: ACT-DR6-CMBonly
2026-10-01T11:21:19.7254594Z Successfully installed ACT-DR6-CMBonly-1.0.0
2026-10-01T11:21:19.7756835Z Q041_ACT_CMB_LAMBDA_DATA_GATE=PASS path=/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages/data/ACTDR6CMBonly/v1.0/dr6_data_cmbonly.fits
2026-10-01T11:21:20.0046287Z Obtaining file:///home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_lenslike
2026-10-01T11:21:20.0059352Z   Installing build dependencies: started
2026-10-01T11:21:20.4361297Z   Installing build dependencies: finished with status 'done'
2026-10-01T11:21:20.4367155Z   Checking if build backend supports build_editable: started
2026-10-01T11:21:20.5096928Z   Checking if build backend supports build_editable: finished with status 'done'
2026-10-01T11:21:20.5102811Z   Getting requirements to build editable: started
2026-10-01T11:21:20.5727413Z   Getting requirements to build editable: finished with status 'done'
2026-10-01T11:21:20.5734528Z   Preparing editable metadata (pyproject.toml): started
2026-10-01T11:21:20.6373623Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-10-01T11:21:20.6401159Z Building wheels for collected packages: act_dr6_lenslike
2026-10-01T11:21:20.6406990Z   Building editable for act_dr6_lenslike (pyproject.toml): started
2026-10-01T11:21:20.7047228Z   Building editable for act_dr6_lenslike (pyproject.toml): finished with status 'done'
2026-10-01T11:21:20.7052266Z   Created wheel for act_dr6_lenslike: filename=act_dr6_lenslike-1.2.0-py2.py3-none-any.whl size=4126 sha256=7bdf95443fdac11857a2fbd6e20617f9c206fb7ddb3cb1ea5a15a61e71e19991
2026-10-01T11:21:20.7053910Z   Stored in directory: /tmp/pip-ephem-wheel-cache-oor_g74m/wheels/8c/db/c7/248b06e38a1f07a22faa7bcbc157b826e315394147e0942bc1
2026-10-01T11:21:20.7071774Z Successfully built act_dr6_lenslike
2026-10-01T11:21:20.7154009Z Installing collected packages: act_dr6_lenslike
2026-10-01T11:21:20.7204499Z Successfully installed act_dr6_lenslike-1.2.0
2026-10-01T11:21:20.7676252Z Q041_ACT_LENS_LAMBDA_DATA_GATE=PASS path=/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages/data/ACT_dr6_likelihood/v1.2
2026-10-01T11:21:21.4008875Z Q041_DESI_DR2_BAO_DTYPE_COMPATIBILITY_PATCH_GATE=PASS
2026-10-01T11:21:21.9735042Z Q041_DESI_DR2_BAO_STRINGDTYPE_RUNTIME_GATE=PASS pandas=3.0.6
2026-10-01T11:21:22.8247257Z Q041_DESI_DR2_COBAYA_VERSION_METADATA_GATE=PASS
2026-10-01T11:21:23.5175119Z Q041_EXTERNAL_RUNTIME_PROVENANCE_GATE=PASS
2026-10-01T11:21:23.6259925Z Q041_V14_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-01T11:21:23.6491244Z Q041_V15_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-01T11:21:23.6723672Z Q041_V16_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-01T11:21:23.6951643Z Q041_V19_EXTERNAL_RUNTIME_IDENTITY_GATE=PASS
2026-10-01T11:21:23.9251296Z Requirement already satisfied: Py-BOBYQA==1.5.0 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (1.5.0)
2026-10-01T11:21:23.9260299Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (79.0.1)
2026-10-01T11:21:23.9263053Z Requirement already satisfied: numpy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (1.26.4)
2026-10-01T11:21:23.9266151Z Requirement already satisfied: scipy in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (1.15.3)
2026-10-01T11:21:23.9269179Z Requirement already satisfied: pandas in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from Py-BOBYQA==1.5.0) (3.0.6)
2026-10-01T11:21:23.9324175Z Requirement already satisfied: python-dateutil>=2.8.2 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from pandas->Py-BOBYQA==1.5.0) (2.9.0.post0)
2026-10-01T11:21:23.9357510Z Requirement already satisfied: six>=1.5 in /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas->Py-BOBYQA==1.5.0) (1.17.0)
2026-10-01T11:21:24.5929751Z [install] Installing external packages at '/home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages'
2026-10-01T11:21:24.5940078Z [install] The installation path has been written into the global config file: /home/runner/.config/cobaya/config.yaml
2026-10-01T11:21:24.5970707Z 
2026-10-01T11:21:24.5971225Z ================================================================================
2026-10-01T11:21:24.5971595Z sn.pantheonplus
2026-10-01T11:21:24.5971928Z ================================================================================
2026-10-01T11:21:24.5972186Z 
2026-10-01T11:21:24.5972424Z [install] Checking if dependencies have already been installed...
2026-10-01T11:21:24.5973100Z [install] External dependencies for this component already installed.
2026-10-01T11:21:24.5973684Z [install] Doing nothing.
2026-10-01T11:21:24.5973942Z 
2026-10-01T11:21:24.5974110Z ================================================================================
2026-10-01T11:21:24.5974593Z * Summary * 
2026-10-01T11:21:24.5974880Z ================================================================================
2026-10-01T11:21:24.5975112Z 
2026-10-01T11:21:24.5975583Z [install] All requested components' dependencies correctly installed at /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:21:24.6915556Z Q042_MPI_TOOLCHAIN_GATE=PASS mpicc=/usr/bin/mpicc mpifort=/usr/bin/mpifort
2026-10-01T11:21:24.7962892Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-01T11:21:24.8058943Z make: Nothing to be done for 'libchord.so'.
2026-10-01T11:21:24.8059804Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-01T11:21:25.0297719Z Processing ./external/PolyChordLite
2026-10-01T11:21:25.0305197Z   Preparing metadata (pyproject.toml): started
2026-10-01T11:21:25.6407892Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-10-01T11:21:25.6423471Z Building wheels for collected packages: pypolychord
2026-10-01T11:21:25.6429423Z   Building wheel for pypolychord (pyproject.toml): started
2026-10-01T11:21:26.0296281Z   Building wheel for pypolychord (pyproject.toml): finished with status 'done'
2026-10-01T11:21:26.0306345Z   Created wheel for pypolychord: filename=pypolychord-1.22.2-cp311-cp311-linux_x86_64.whl size=374446 sha256=083ededcb16b3139c55088be39fc3d3fd44567304a79629c0739f407b6adf1ff
2026-10-01T11:21:26.0308331Z   Stored in directory: /tmp/pip-ephem-wheel-cache-d1tnyyj0/wheels/b9/80/45/d967b892eb659dbd8b31b85b9ee242adcb1da43378c684d8d5
2026-10-01T11:21:26.0325972Z Successfully built pypolychord
2026-10-01T11:21:26.0408733Z Installing collected packages: pypolychord
2026-10-01T11:21:26.0595126Z Successfully installed pypolychord-1.22.2
2026-10-01T11:21:26.7165078Z Q042_V11_RUNTIME_SOURCE_GATE=PASS polychord_commit=3ade6445bb3719a6db6f6e81f178765545ffc833 pantheon_files=6
2026-10-01T11:21:26.8266372Z Q042_PROD_V1_RUNTIME_SOURCE_GATE=PASS
2026-10-01T11:21:26.8516132Z Q042_PROD_V8_RECOVERED_RUNTIME_GATE=PASS
2026-10-01T11:21:26.8866313Z Q042_POLYCHORD_PARTIAL_INIT_SOURCE_PATCH_GATE=PASS
2026-10-01T11:21:26.8956208Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-01T11:21:26.8957111Z rm -f *.o *.mod *.MOD
2026-10-01T11:21:26.8969446Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-01T11:21:26.8979462Z make: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-01T11:21:26.9080431Z make -C /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/lib/libchord.so
2026-10-01T11:21:26.9094201Z make[1]: Entering directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-01T11:21:26.9095189Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c utils.F90
2026-10-01T11:21:31.6392716Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c abort.F90
2026-10-01T11:21:31.7081936Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c array_utils.f90
2026-10-01T11:21:32.3758246Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c settings.f90
2026-10-01T11:21:32.4733709Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c calculate.f90
2026-10-01T11:21:32.6171663Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c mpi_utils.F90
2026-10-01T11:21:32.6834260Z mpi_utils.F90:627:12:
2026-10-01T11:21:32.6834628Z 
2026-10-01T11:21:32.6835053Z   627 |             empty_buffer,                &! not sending anything
2026-10-01T11:21:32.6835875Z       |            1
2026-10-01T11:21:32.6836673Z ......
2026-10-01T11:21:32.6837086Z   655 |             live_point,                  &! live point being sent
2026-10-01T11:21:32.6837540Z       |            2
2026-10-01T11:21:32.6838226Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-01T11:21:32.6838882Z mpi_utils.F90:581:12:
2026-10-01T11:21:32.6839174Z 
2026-10-01T11:21:32.6839377Z   581 |             logL,                        &!
2026-10-01T11:21:32.6839867Z       |            1
2026-10-01T11:21:32.6840181Z ......
2026-10-01T11:21:32.6840608Z   655 |             live_point,                  &! live point being sent
2026-10-01T11:21:32.6841067Z       |            2
2026-10-01T11:21:32.6841698Z Warning: Rank mismatch between actual argument at (1) and actual argument at (2) (rank-1 and scalar)
2026-10-01T11:21:32.6842325Z mpi_utils.F90:517:12:
2026-10-01T11:21:32.6842543Z 
2026-10-01T11:21:32.6842727Z   517 |             logL,                        &!
2026-10-01T11:21:32.6843208Z       |            1
2026-10-01T11:21:32.6843536Z ......
2026-10-01T11:21:32.6843974Z   680 |             live_point,                  &! live point recieved
2026-10-01T11:21:32.6844472Z       |            2
2026-10-01T11:21:32.6845156Z Warning: Rank mismatch between actual argument at (1) and actual argument at (2) (rank-1 and scalar)
2026-10-01T11:21:32.6846042Z mpi_utils.F90:527:12:
2026-10-01T11:21:32.6846330Z 
2026-10-01T11:21:32.6846503Z   527 |             epoch,                       &!
2026-10-01T11:21:32.6847000Z       |            1
2026-10-01T11:21:32.6847388Z ......
2026-10-01T11:21:32.6847826Z   680 |             live_point,                  &! live point recieved
2026-10-01T11:21:32.6848322Z       |            2
2026-10-01T11:21:32.6848952Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-01T11:21:32.6849719Z mpi_utils.F90:275:12:
2026-10-01T11:21:32.6849925Z 
2026-10-01T11:21:32.6850179Z   275 |             doubles,                     &!broadcast buffer
2026-10-01T11:21:32.6850691Z       |            1
2026-10-01T11:21:32.6851114Z ......
2026-10-01T11:21:32.6851540Z   291 |             integers,                    &!broadcast buffer
2026-10-01T11:21:32.6852047Z       |            2
2026-10-01T11:21:32.6852673Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (REAL(8)/INTEGER(4)).
2026-10-01T11:21:32.6853420Z mpi_utils.F90:240:12:
2026-10-01T11:21:32.6853623Z 
2026-10-01T11:21:32.6853890Z   240 |             intgr_local,                 &!send buffer
2026-10-01T11:21:32.6854379Z       |            1
2026-10-01T11:21:32.6854743Z ......
2026-10-01T11:21:32.6855175Z   258 |             db_local,                    &!send buffer
2026-10-01T11:21:32.6855826Z       |            2
2026-10-01T11:21:32.6856469Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-01T11:21:32.6857142Z mpi_utils.F90:241:12:
2026-10-01T11:21:32.6857405Z 
2026-10-01T11:21:32.6857662Z   241 |             intgr,                       &!recieve buffer
2026-10-01T11:21:32.6858125Z       |            1
2026-10-01T11:21:32.6858521Z ......
2026-10-01T11:21:32.6858948Z   259 |             db,                          &!recieve buffer
2026-10-01T11:21:32.6859507Z       |            2
2026-10-01T11:21:32.6860338Z Warning: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(4)/REAL(8)).
2026-10-01T11:21:32.9047517Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c random_utils.F90
2026-10-01T11:21:33.3504581Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c chordal_sampling.f90
2026-10-01T11:21:33.6881338Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c run_time_info.f90
2026-10-01T11:21:34.9352163Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c clustering.f90
2026-10-01T11:21:35.6362072Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c params.f90
2026-10-01T11:21:35.7501665Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c priors.f90
2026-10-01T11:21:36.9981636Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c read_write.F90
2026-10-01T11:21:38.0748530Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c feedback.f90
2026-10-01T11:21:38.3217185Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c generate.F90
2026-10-01T11:21:38.7363291Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c ini.f90
2026-10-01T11:21:39.0138481Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c nelder_mead.f90
2026-10-01T11:21:39.3974730Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c maximiser.F90
2026-10-01T11:21:39.6884453Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c nested_sampling.F90
2026-10-01T11:21:40.1161728Z mpifort -ffree-line-length-none -cpp -fPIC -fno-stack-arrays  -fallow-argument-mismatch -Ofast -DMPI -c interfaces.F90
2026-10-01T11:21:40.4761160Z mpicxx -std=c++11 -fPIC -Ofast -DUSE_MPI -c c_interface.cpp
2026-10-01T11:21:41.4030337Z mpifort -shared abort.o array_utils.o calculate.o chordal_sampling.o clustering.o feedback.o generate.o ini.o interfaces.o maximiser.o mpi_utils.o nelder_mead.o nested_sampling.o params.o priors.o random_utils.o read_write.o run_time_info.o settings.o utils.o c_interface.o -o /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/lib/libchord.so -lstdc++ -Wl,-z,noexecstack 
2026-10-01T11:21:41.5025013Z make[1]: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/src/polychord'
2026-10-01T11:21:41.5026388Z make: Leaving directory '/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite'
2026-10-01T11:21:49.9235574Z Q042_POLYCHORD_PATCHED_BINARY_SYMBOL_GATE=PASS
2026-10-01T11:21:50.1481208Z Processing ./external/PolyChordLite
2026-10-01T11:21:50.1490955Z   Preparing metadata (pyproject.toml): started
2026-10-01T11:21:50.4099093Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-10-01T11:21:50.4115629Z Building wheels for collected packages: pypolychord
2026-10-01T11:21:50.4121684Z   Building wheel for pypolychord (pyproject.toml): started
2026-10-01T11:21:50.7694908Z   Building wheel for pypolychord (pyproject.toml): finished with status 'done'
2026-10-01T11:21:50.7705541Z   Created wheel for pypolychord: filename=pypolychord-1.22.2-cp311-cp311-linux_x86_64.whl size=379301 sha256=51ec139189270d3c5a7fd58aa2677ad536ec8e2db839417625889594c69025f1
2026-10-01T11:21:50.7706949Z   Stored in directory: /tmp/pip-ephem-wheel-cache-05a525ah/wheels/b9/80/45/d967b892eb659dbd8b31b85b9ee242adcb1da43378c684d8d5
2026-10-01T11:21:50.7724873Z Successfully built pypolychord
2026-10-01T11:21:50.7807734Z Installing collected packages: pypolychord
2026-10-01T11:21:50.7808432Z   Attempting uninstall: pypolychord
2026-10-01T11:21:50.7821614Z     Found existing installation: pypolychord 1.22.2
2026-10-01T11:21:50.7836116Z     Uninstalling pypolychord-1.22.2:
2026-10-01T11:21:50.8528395Z       Successfully uninstalled pypolychord-1.22.2
2026-10-01T11:21:50.8826912Z Successfully installed pypolychord-1.22.2
2026-10-01T11:21:51.8523363Z 
2026-10-01T11:21:51.8524221Z PolyChord: Next Generation Nested Sampling
2026-10-01T11:21:51.8524708Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-01T11:21:51.8525236Z   version: 1.22.2
2026-10-01T11:21:51.8526109Z   release: 10th Jan 2024
2026-10-01T11:21:51.8526465Z     email: wh260@mrao.cam.ac.uk
2026-10-01T11:21:51.8526647Z 
2026-10-01T11:21:51.8631067Z  ____________________________________________________ 
2026-10-01T11:21:51.8631537Z |                                                    |
2026-10-01T11:21:51.8632046Z | ndead  =          100                              |
2026-10-01T11:21:51.8632440Z | log(Z) =           -0.09361 +/-            0.01161 |
2026-10-01T11:21:51.8632808Z |____________________________________________________|
2026-10-01T11:21:52.7460619Z 
2026-10-01T11:21:52.7461551Z PolyChord: Next Generation Nested Sampling
2026-10-01T11:21:52.7462166Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-01T11:21:52.7462539Z   version: 1.22.2
2026-10-01T11:21:52.7462863Z   release: 10th Jan 2024
2026-10-01T11:21:52.7463205Z     email: wh260@mrao.cam.ac.uk
2026-10-01T11:21:52.7463371Z 
2026-10-01T11:21:59.8296957Z 
2026-10-01T11:21:59.8297786Z PolyChord: Next Generation Nested Sampling
2026-10-01T11:21:59.8298245Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-01T11:21:59.8298745Z   version: 1.22.2
2026-10-01T11:21:59.8299073Z   release: 10th Jan 2024
2026-10-01T11:21:59.8299442Z     email: wh260@mrao.cam.ac.uk
2026-10-01T11:21:59.8299630Z 
2026-10-01T11:21:59.8344842Z  ____________________________________________________ 
2026-10-01T11:21:59.8345492Z |                                                    |
2026-10-01T11:21:59.8346151Z | ndead  =          100                              |
2026-10-01T11:21:59.8346776Z | log(Z) =           -0.09361 +/-            0.01161 |
2026-10-01T11:21:59.8349302Z |____________________________________________________|
2026-10-01T11:21:59.9678586Z Q042_POLYCHORD_PARTIAL_INIT_REPRODUCIBILITY_GATE_V17=PASS
2026-10-01T11:21:59.9957842Z Q042_PROD_V17_PARTIAL_INIT_RUNTIME_GATE=PASS
2026-10-01T11:22:00.5677795Z Q042_COBAYA_PARTIAL_RESUME_ADAPTER_SELFTEST_V18=PASS
2026-10-01T11:22:00.6701212Z Q042_PROD_V18_COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_GATE=PASS
2026-10-01T11:22:00.6772477Z ##[group]Run python q042_production_v18.py polychord-segment \
2026-10-01T11:22:00.6772896Z [36;1mpython q042_production_v18.py polychord-segment \[0m
2026-10-01T11:22:00.6773222Z [36;1m  --q032-parent-root q032_parent \[0m
2026-10-01T11:22:00.6773570Z [36;1m  --preflight env_bundle/q032_preflight/q032_preflight_sealed_v2.json \[0m
2026-10-01T11:22:00.6773955Z [36;1m  --parent-dir env_bundle/q032_parent_profiles \[0m
2026-10-01T11:22:00.6774338Z [36;1m  --hlp-matrix env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.npy \[0m
2026-10-01T11:22:00.6774783Z [36;1m  --hlp-meta env_bundle/q032_hlp_cov/q032_hillipop_tt3pair_precision_v2.json \[0m
2026-10-01T11:22:00.6775272Z [36;1m  --reduced-support env_bundle/q042_environment/q042_primary_nonoverlap_support_prod_v18.json \[0m
2026-10-01T11:22:00.6776032Z [36;1m  --reduced-hlp-matrix env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.npy \[0m
2026-10-01T11:22:00.6776656Z [36;1m  --reduced-hlp-meta env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v18.json \[0m
2026-10-01T11:22:00.6777073Z [36;1m  --spec q042_production_spec_v1.json \[0m
2026-10-01T11:22:00.6777388Z [36;1m  --source-lock q042_production_source_lock_v18.json \[0m
2026-10-01T11:22:00.6777791Z [36;1m  --external-runtime q042_runtime/q042_external_runtime_provenance_prod_v1.json \[0m
2026-10-01T11:22:00.6778196Z [36;1m  --arm 'camspec' --model 'lcdm' --combination 'FULL' \[0m
2026-10-01T11:22:00.6778589Z [36;1m  --segment '3' --soft-minutes 240 --mpi-ranks 1 --parent-run-id '36829393843' \[0m
2026-10-01T11:22:00.6779050Z [36;1m  --output-dir cell_state --segment-json q042_production_segment_v18.json || true[0m
2026-10-01T11:22:00.6816077Z shell: /usr/bin/bash -e {0}
2026-10-01T11:22:00.6816326Z env:
2026-10-01T11:22:00.6816523Z   CURRENT_Q: Q-042
2026-10-01T11:22:00.6816750Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T11:22:00.6817000Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T11:22:00.6817299Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T11:22:00.6817627Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T11:22:00.6818075Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T11:22:00.6818360Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T11:22:00.6818700Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T11:22:00.6819109Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T11:22:00.6819539Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:22:00.6819895Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T11:22:00.6820247Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:22:00.6820578Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:22:00.6820911Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T11:22:00.6821247Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T11:22:00.6821525Z ##[endgroup]
2026-10-01T11:22:01.6939070Z [output] Output to be read-from/written-into folder '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord', with prefix 'chain'
2026-10-01T11:22:01.6939901Z [output] Found existing info files with the requested output prefix: '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain'
2026-10-01T11:22:01.6940411Z [output] Let's try to resume/load.
2026-10-01T11:22:01.9206204Z [output] Found an old sample. Resuming.
2026-10-01T11:22:01.9312288Z [prior] *WARNING* External prior 'q041_act_calibration_shape' loaded. Mind that it might not be normalized!
2026-10-01T11:22:01.9328453Z [classy] `classy` module loaded successfully from /home/runner/work/Bubbleverse/Bubbleverse/external/class_ede/python/build/lib.linux-x86_64-cpython-311
2026-10-01T11:22:01.9329616Z [classy] *WARNING* Detected an old CLASS version (<3.3). Please update: support for this will be deprecated soon.
2026-10-01T11:22:01.9356336Z [planck_npipe_highl_camspec.ttteee] Using range {'143x143': [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599], '217x217': [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599], '143x217': [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599]}
2026-10-01T11:22:02.0704375Z [planck_npipe_highl_camspec.ttteee] L-range for 143x143: 30 2000
2026-10-01T11:22:02.0704948Z [planck_npipe_highl_camspec.ttteee] L-range for 217x217: 500 2500
2026-10-01T11:22:02.0705684Z [planck_npipe_highl_camspec.ttteee] L-range for 143x217: 500 2500
2026-10-01T11:22:02.0706619Z [planck_npipe_highl_camspec.ttteee] Number of data points: 750
2026-10-01T11:22:02.1193755Z [q019_shape_tau_reio] Initialized external likelihood.
2026-10-01T11:22:02.1194320Z [q019_shape_a_planck] Initialized external likelihood.
2026-10-01T11:22:02.3432978Z /opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/sacc/sacc.py:935: UserWarning: The FITS format without the 'sacc_ordering' column is deprecated. Assuming data rows are in the correct order as it was before version 1.0.
2026-10-01T11:22:02.3434466Z   warnings.warn(
2026-10-01T11:22:06.4221841Z /home/runner/work/Bubbleverse/Bubbleverse/external/act_dr6_lenslike/act_dr6_lenslike/act_dr6_lenslike.py:422: UserWarning: Hartlap correction to cinv: 0.9860935524652339
2026-10-01T11:22:06.4222972Z   warnings.warn(f"Hartlap correction to cinv: {hartlap_correction}")
2026-10-01T11:22:06.4274336Z Loading ACT DR6 lensing likelihood v1.2...
2026-10-01T11:22:06.4295838Z [bao.desi_dr2] Initialized.
2026-10-01T11:22:07.0433785Z [polychord] *WARNING* This run has been SEEDED with seed 421000
2026-10-01T11:22:07.0523855Z [polychord] `pypolychord` module loaded successfully from /home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord
2026-10-01T11:22:07.0546777Z [polychord] Storing raw PolyChord output in '/home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain_polychord_raw'.
2026-10-01T11:22:07.0576540Z [polychord] Parameter blocks and their oversampling factors:
2026-10-01T11:22:07.0606025Z [polychord] *  1 : ['tau_reio']
2026-10-01T11:22:07.0636130Z [polychord] *  1 : ['omega_b', 'omega_cdm', 'H0', 'n_s', 'logA']
2026-10-01T11:22:07.0666031Z [polychord] * 26 : ['A_act', 'P_act']
2026-10-01T11:22:07.0695973Z [polychord] * 36 : ['A_planck']
2026-10-01T11:22:07.0726134Z [polychord] * 41 : ['amp_143', 'amp_217', 'amp_143x217', 'n_143', 'n_217', 'n_143x217']
2026-10-01T11:22:07.0756516Z [prior] *WARNING* There are unbounded parameters (['A_planck']). Prior bounds are given at 0.9999995 confidence level. Beware of likelihood modes at the edge of the prior
2026-10-01T11:22:07.1246646Z [polychord] Calling PolyChord...
2026-10-01T11:22:07.3950726Z PolyChord: MPI is already initilised, not initialising, and will not finalize
2026-10-01T11:22:07.3951230Z 
2026-10-01T11:22:07.3951412Z PolyChord: Next Generation Nested Sampling
2026-10-01T11:22:07.3951893Z copyright: Will Handley, Mike Hobson & Anthony Lasenby
2026-10-01T11:22:07.3952328Z   version: 1.22.2
2026-10-01T11:22:07.3952634Z   release: 10th Jan 2024
2026-10-01T11:22:07.3952965Z     email: wh260@mrao.cam.ac.uk
2026-10-01T11:22:07.3953182Z 
2026-10-01T11:22:07.3953302Z Run Settings
2026-10-01T11:22:07.3953570Z nlive    :     375
2026-10-01T11:22:07.3953850Z nDims    :      15
2026-10-01T11:22:07.3954135Z nDerived :      17
2026-10-01T11:22:07.3954411Z Doing Clustering
2026-10-01T11:22:07.3954717Z Synchronous parallelisation
2026-10-01T11:22:07.3955079Z Generating equally weighted posteriors
2026-10-01T11:22:07.3955699Z Generating weighted posteriors
2026-10-01T11:22:07.3956053Z Clustering on posteriors
2026-10-01T11:22:07.3956755Z Writing a resume file to /home/runner/work/Bubbleverse/Bubbleverse/cell_state/polychord/chain_polychord_raw/chain.resume
2026-10-01T11:22:07.3957376Z 
2026-10-01T11:22:07.5216904Z Resuming from previous run
2026-10-01T11:22:07.5217428Z number of repeats:            5          25         260         180        1230
2026-10-01T11:22:07.5217871Z started sampling
2026-10-01T11:22:07.5218046Z 
2026-10-01T14:39:31.5297643Z [classy] *ERROR* Computation error (see traceback below)! Parameters sent to CLASS: {'omega_b': 0.020721894362238032, 'omega_cdm': 0.10267093582571502, 'H0': 73.1518764249673, 'tau_reio': 0.022146719553358576, 'n_s': 1.0712271414025623, 'A_s': 1.6612992056613594e-09} and {'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.06, 'T_ncdm': 0.71611, 'output': 'lCl tCl tCl,pCl,lCl,mPk mPk pCl', 'lensing': 'yes', 'non_linear': 'hmcode', 'l_max_scalars': 9001, 'P_k_max_1/Mpc': 2.0}.
2026-10-01T14:39:31.5316325Z To ignore this kind of error, make 'stop_at_error: False'.
2026-10-01T14:39:31.5316941Z [classy] *ERROR* Error at evaluation. See error information below.
2026-10-01T14:39:31.5317569Z [exception handler] ---------------------------------------
2026-10-01T14:39:31.5317956Z 
2026-10-01T14:39:31.5318389Z Traceback (most recent call last):
2026-10-01T14:39:31.5325978Z   File "/home/runner/work/Bubbleverse/Bubbleverse/q042_production_v18.py", line 1309, in <module>
2026-10-01T14:39:31.5326481Z     raise SystemExit(a.func(a))
2026-10-01T14:39:31.5326712Z                      ^^^^^^^^^
2026-10-01T14:39:31.5327132Z   File "/home/runner/work/Bubbleverse/Bubbleverse/q042_production_v18.py", line 555, in polychord_worker
2026-10-01T14:39:31.5327517Z     _, sm = cobaya_run(
2026-10-01T14:39:31.5327721Z             ^^^^^^^^^^^
2026-10-01T14:39:31.5328106Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/run.py", line 146, in run
2026-10-01T14:39:31.5328500Z     sampler.run()
2026-10-01T14:39:31.5328950Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/samplers/polychord/polychord.py", line 266, in run
2026-10-01T14:39:31.5329508Z     self.pc.run_polychord(logpost, self.nDims, self.nDerived, self.pc_settings,
2026-10-01T14:39:31.5330142Z   File "/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord/polychord.py", line 177, in run_polychord
2026-10-01T14:39:31.5330682Z     _pypolychord.run(wrap_loglikelihood,
2026-10-01T14:39:31.5331286Z   File "/home/runner/work/Bubbleverse/Bubbleverse/external/PolyChordLite/build/lib.linux-x86_64-cpython-311/pypolychord/polychord.py", line 163, in wrap_loglikelihood
2026-10-01T14:39:31.5331818Z     logL = loglikelihood(theta)
2026-10-01T14:39:31.5332038Z            ^^^^^^^^^^^^^^^^^^^^
2026-10-01T14:39:31.5332504Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/samplers/polychord/polychord.py", line 253, in logpost
2026-10-01T14:39:31.5333001Z     result = self.model.logposterior(params_values)
2026-10-01T14:39:31.5333275Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-01T14:39:31.5333956Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/model.py", line 558, in logposterior
2026-10-01T14:39:31.5334388Z     like = self._loglikes_input_params(input_params,
2026-10-01T14:39:31.5334651Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-01T14:39:31.5335102Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/model.py", line 378, in _loglikes_input_params
2026-10-01T14:39:31.5335733Z     compute_success = component.check_cache_and_compute(
2026-10-01T14:39:31.5336013Z                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-01T14:39:31.5336486Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/theory.py", line 253, in check_cache_and_compute
2026-10-01T14:39:31.5337001Z     if self.calculate(state, want_derived, **params_values_dict) is False:
2026-10-01T14:39:31.5337320Z        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-10-01T14:39:31.5337790Z   File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/site-packages/cobaya/theories/classy/classy.py", line 557, in calculate
2026-10-01T14:39:31.5338234Z     self.classy.compute()
2026-10-01T14:39:31.5338507Z   File "classy.pyx", line 398, in classy.Class.compute
2026-10-01T14:39:31.5338787Z classy.CosmoComputationError: 
2026-10-01T14:39:31.5338936Z 
2026-10-01T14:39:31.5339241Z Error in Class: perturbations_init(L:1007) :error in perturbations_solve(ppr, pba, pth, ppt, index_md, index_ic, index_k, pppw[thread]);
2026-10-01T14:39:31.5340162Z =>perturbations_solve(L:3245) :error in perturbations_find_approximation_switches(ppr, pba, pth, ppt, index_md, k, ppw, tau, ppt->tau_sampling[tau_actual_size-1], ppr->tol_tau_approx, interval_number, interval_number_of, interval_limit, interval_approx);
2026-10-01T14:39:31.5341172Z =>perturbations_find_approximation_switches(L:3713) :error in perturbations_approximations(ppr, pba, pth, ppt, index_md, k, mid, ppw);
2026-10-01T14:39:31.5342341Z =>perturbations_approximations(L:6217) :condition (tau_c < 0.) is true; tau_c = 1/kappa' should always be positive unless there is something wrong in the thermodynamics module. However you have here tau_c=-2.403414e+09 at z=5.663014e-02, conformal time=1.449787e+04 x_e=-1.174788e-03. (This could come from the interpolation of a too poorly sampled reionisation history?).
2026-10-01T14:39:31.5343187Z 
2026-10-01T14:39:31.5343310Z -------------------------------------------------------------
2026-10-01T14:39:31.5343500Z 
2026-10-01T14:39:33.7432173Z Q042_PROD_V18_SEGMENT_STATUS=FAILED
2026-10-01T14:39:33.7652273Z ##[group]Run python - <<'PY'
2026-10-01T14:39:33.7652684Z [36;1mpython - <<'PY'[0m
2026-10-01T14:39:33.7652980Z [36;1mimport json[0m
2026-10-01T14:39:33.7653351Z [36;1md=json.load(open('q042_production_segment_v18.json'))[0m
2026-10-01T14:39:33.7653808Z [36;1ma=(d.get('checkpoint_after') or {})[0m
2026-10-01T14:39:33.7654191Z [36;1mb=(d.get('checkpoint_before') or {})[0m
2026-10-01T14:39:33.7654617Z [36;1mprint('Q042_RELAY_STATUS='+str(d.get('status')))[0m
2026-10-01T14:39:33.7655150Z [36;1mprint('Q042_RELAY_KIND='+str(a.get('checkpoint_kind')))[0m
2026-10-01T14:39:33.7656065Z [36;1mprint('Q042_RELAY_PARTIAL_ACCEPTED_BEFORE='+str(b.get('partial_init_accepted')))[0m
2026-10-01T14:39:33.7656805Z [36;1mprint('Q042_RELAY_PARTIAL_ACCEPTED_AFTER='+str(a.get('partial_init_accepted')))[0m
2026-10-01T14:39:33.7657512Z [36;1mprint('Q042_RELAY_PROGRESS_REASON='+str(d.get('checkpoint_progress_reason')))[0m
2026-10-01T14:39:33.7658036Z [36;1mPY[0m
2026-10-01T14:39:33.7704379Z shell: /usr/bin/bash -e {0}
2026-10-01T14:39:33.7704634Z env:
2026-10-01T14:39:33.7704819Z   CURRENT_Q: Q-042
2026-10-01T14:39:33.7705023Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T14:39:33.7705265Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T14:39:33.7705831Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T14:39:33.7706149Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T14:39:33.7706441Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T14:39:33.7706881Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T14:39:33.7707205Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T14:39:33.7707596Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T14:39:33.7708013Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.7708357Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T14:39:33.7708705Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.7709017Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.7709332Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.7709644Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T14:39:33.7709911Z ##[endgroup]
2026-10-01T14:39:33.7947964Z Q042_RELAY_STATUS=FAILED
2026-10-01T14:39:33.7948400Z Q042_RELAY_KIND=STOCK_RESUME
2026-10-01T14:39:33.7948813Z Q042_RELAY_PARTIAL_ACCEPTED_BEFORE=None
2026-10-01T14:39:33.7949239Z Q042_RELAY_PARTIAL_ACCEPTED_AFTER=None
2026-10-01T14:39:33.7949704Z Q042_RELAY_PROGRESS_REASON=STOCK_RESUME_UNCHANGED
2026-10-01T14:39:33.8010151Z ##[group]Run set -euo pipefail
2026-10-01T14:39:33.8010437Z [36;1mset -euo pipefail[0m
2026-10-01T14:39:33.8010815Z [36;1mSTATUS=$(python -c "import json;print(json.load(open('q042_production_segment_v18.json'))['status'])")[0m
2026-10-01T14:39:33.8011422Z [36;1mMAXSEG=$(python -c "import json;print(json.load(open('q042_production_spec_v1.json'))['orchestration']['max_polychord_segments_per_cell'])")[0m
2026-10-01T14:39:33.8011897Z [36;1mif [ "$STATUS" = COMPLETE ]; then[0m
2026-10-01T14:39:33.8012157Z [36;1m  echo 'final=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8012428Z [36;1m  echo 'checkpoint=no' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8012682Z [36;1m  python - <<'PY'[0m
2026-10-01T14:39:33.8012895Z [36;1mimport json[0m
2026-10-01T14:39:33.8013518Z [36;1md=json.load(open('q042_production_segment_v18.json'));d['stage']='POLYCHORD_PRODUCTION_FINAL_V18';d['status']='COMPLETE';json.dump(d,open('q042_production_polychord_final_v18.json','w'),indent=2,sort_keys=True)[0m
2026-10-01T14:39:33.8014111Z [36;1mPY[0m
2026-10-01T14:39:33.8014388Z [36;1melif [ "$STATUS" = SEGMENT_CHECKPOINTED ] && [ "$SEG" -lt $((MAXSEG-1)) ]; then[0m
2026-10-01T14:39:33.8014721Z [36;1m  NEXT=$((SEG+1))[0m
2026-10-01T14:39:33.8014942Z [36;1m  echo 'final=no' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8015202Z [36;1m  echo 'checkpoint=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8015711Z [36;1m  echo "next=$NEXT" >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8015962Z [36;1melse[0m
2026-10-01T14:39:33.8016166Z [36;1m  echo 'final=yes' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8016433Z [36;1m  echo 'checkpoint=no' >> "$GITHUB_OUTPUT"[0m
2026-10-01T14:39:33.8016684Z [36;1m  python - <<'PY'[0m
2026-10-01T14:39:33.8016903Z [36;1mimport json[0m
2026-10-01T14:39:33.8017156Z [36;1md=json.load(open('q042_production_segment_v18.json'))[0m
2026-10-01T14:39:33.8017462Z [36;1md['stage']='POLYCHORD_PRODUCTION_FINAL_V18'[0m
2026-10-01T14:39:33.8017930Z [36;1md['status']='CONTROLLED_MAX_SEGMENTS_WITHOUT_CONVERGENCE' if d['status']=='SEGMENT_CHECKPOINTED' else 'CONTROLLED_TECHNICAL_FAILURE'[0m
2026-10-01T14:39:33.8018504Z [36;1mjson.dump(d,open('q042_production_polychord_final_v18.json','w'),indent=2,sort_keys=True)[0m
2026-10-01T14:39:33.8018847Z [36;1mPY[0m
2026-10-01T14:39:33.8019022Z [36;1mfi[0m
2026-10-01T14:39:33.8052793Z shell: /usr/bin/bash -e {0}
2026-10-01T14:39:33.8053167Z env:
2026-10-01T14:39:33.8053467Z   CURRENT_Q: Q-042
2026-10-01T14:39:33.8053706Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T14:39:33.8053943Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T14:39:33.8054216Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T14:39:33.8054528Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T14:39:33.8054822Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T14:39:33.8055234Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T14:39:33.8055708Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T14:39:33.8056114Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T14:39:33.8056524Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8056865Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T14:39:33.8057204Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8057520Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8057830Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8058142Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T14:39:33.8058418Z   SEG: 3
2026-10-01T14:39:33.8058599Z ##[endgroup]
2026-10-01T14:39:33.8860877Z ##[group]Run actions/upload-artifact@v4
2026-10-01T14:39:33.8861159Z with:
2026-10-01T14:39:33.8861412Z   name: q042-v18-36731879692-polychord-final-camspec-lcdm-FULL
2026-10-01T14:39:33.8861753Z   path: cell_state/**
q042_production_polychord_final_v18.json

2026-10-01T14:39:33.8862034Z   if-no-files-found: error
2026-10-01T14:39:33.8862255Z   retention-days: 30
2026-10-01T14:39:33.8862450Z   compression-level: 6
2026-10-01T14:39:33.8862643Z   overwrite: false
2026-10-01T14:39:33.8862834Z   include-hidden-files: false
2026-10-01T14:39:33.8863045Z env:
2026-10-01T14:39:33.8863211Z   CURRENT_Q: Q-042
2026-10-01T14:39:33.8863399Z   PROGRAM_ID: Q042-PROD-V18
2026-10-01T14:39:33.8863626Z   RUN_ID: Q042-PRODUCTION-PORTABILITY-V18
2026-10-01T14:39:33.8863893Z   RESULT_ID: R-Q042-PRODUCTION-PORTABILITY-018
2026-10-01T14:39:33.8864205Z   Q032_EXECUTION_COMMIT: 4dc873a5e880d40858d831a3b421456728f0c032
2026-10-01T14:39:33.8864489Z   V1_ROOT_RUN_ID: 36133813540
2026-10-01T14:39:33.8864789Z   V1_EXECUTION_COMMIT: 6c44a4117449145afd0a3ae6eb238490686a8c6d
2026-10-01T14:39:33.8865110Z   V1_RUNTIME_ARTIFACT: q042-prod-36133813540-environment
2026-10-01T14:39:33.8865629Z   COBAYA_PACKAGES_PATH: /home/runner/work/Bubbleverse/Bubbleverse/external/cobaya_packages
2026-10-01T14:39:33.8866043Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8866385Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-10-01T14:39:33.8866730Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8867043Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8867362Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-10-01T14:39:33.8867681Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-10-01T14:39:33.8867948Z ##[endgroup]
2026-10-01T14:39:34.0306966Z (node:5407) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
2026-10-01T14:39:34.0307692Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-10-01T14:39:34.0411320Z Multiple search paths detected. Calculating the least common ancestor of all paths
2026-10-01T14:39:34.0413107Z The least common ancestor is /home/runner/work/Bubbleverse/Bubbleverse. This will be the root directory of the artifact
2026-10-01T14:39:34.0413983Z With the provided path, there will be 18 files uploaded
2026-10-01T14:39:34.0418598Z Artifact name is valid!
2026-10-01T14:39:34.0419028Z Root directory input is valid!
2026-10-01T14:39:34.4274441Z Beginning upload of artifact content to blob storage
2026-10-01T14:39:35.2175139Z (node:5407) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
2026-10-01T14:39:35.6475834Z Uploaded bytes 7640339
2026-10-01T14:39:35.6963212Z Finished uploading artifact content to blob storage!
2026-10-01T14:39:35.6964139Z SHA256 digest of uploaded artifact zip is a1862aa50f99c445dcdb5ed1c4342ba8cfb52ccc7809d2ac4fda0cab8ee5350e
2026-10-01T14:39:35.6965765Z Finalizing artifact upload
2026-10-01T14:39:35.9544132Z Artifact q042-v18-36731879692-polychord-final-camspec-lcdm-FULL.zip successfully finalized. Artifact ID 11170053204
2026-10-01T14:39:35.9545576Z Artifact q042-v18-36731879692-polychord-final-camspec-lcdm-FULL has been successfully uploaded! Final size is 7640339 bytes. Artifact ID is 11170053204
2026-10-01T14:39:35.9550818Z Artifact download URL: https://github.com/Morfindien/Bubbleverse/actions/runs/36854623733/artifacts/11170053204
2026-10-01T14:39:35.9679464Z Post job cleanup.
2026-10-01T14:39:36.0729773Z Post job cleanup.
2026-10-01T14:39:36.1502990Z [command]/usr/bin/git version
2026-10-01T14:39:36.1543627Z git version 2.55.0
2026-10-01T14:39:36.1578820Z Temporarily overriding HOME='/home/runner/work/_temp/189db76b-7c3e-4314-801b-5f338ce14bea' before making global git config changes
2026-10-01T14:39:36.1579877Z Adding repository directory to the temporary git global config as a safe directory
2026-10-01T14:39:36.1584289Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/Bubbleverse/Bubbleverse
2026-10-01T14:39:36.1617667Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-10-01T14:39:36.1647485Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-10-01T14:39:36.1837403Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-10-01T14:39:36.1858680Z http.https://github.com/.extraheader
2026-10-01T14:39:36.1867901Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2026-10-01T14:39:36.1898952Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-10-01T14:39:36.2106856Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-10-01T14:39:36.2142454Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-10-01T14:39:36.2464465Z Cleaning up orphan processes
2026-10-01T14:39:36.2626274Z ##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/cache/restore@v4, actions/checkout@v4, actions/download-artifact@v4, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
```


## APPENDIX F1 — DETERMINISTIC INGESTION AUDIT SOURCE

**Preserved UTF-8 source SHA-256:** `b57071f9d9362bd5acb63709e1570ef1941e6d5772b12e0a769ed9dae8a67e30`; bytes: 7245.

```python
from pathlib import Path
import zipfile, json, hashlib, itertools, collections, math

root=Path('/workspace/scratch/d80c762a97e8')
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
def check(name,condition):
    checks[name]='PASS' if condition else 'FAIL'

with zipfile.ZipFile(root/'upload/q042-production-final-v19.zip') as z:
    raw={n:z.read(n) for n in z.namelist()}
    objs={n:json.loads(b) for n,b in raw.items()}
d=objs['q042_production_final_v19.json']
spec=objs['q042_production_spec_v1.json']
index=objs['q042_production_artifact_index_v19.json']
sel=objs['q042_v18_artifact_selection_v19.json']
lock=objs['q042_production_source_lock_v19.json']
art=json.loads((root/'evidence/merge_artifact_metadata.json').read_text())['artifacts'][0]
run=json.loads((root/'evidence/merge_run_metadata.json').read_text())
arms=['camspec','hillipop'];mods=['lcdm','ede_n3'];combos=list(spec['authoritative_contract']['data_combinations'])
expected=set(itertools.product(arms,mods,combos))
cells=d['controlled_polychord_cells']
keys=[(c['arm'],c['model'],c['combination']) for c in cells]
check('ZIP_MATCHES_LIVE_GITHUB_ARTIFACT',sha((root/'upload/q042-production-final-v19.zip').read_bytes())==art['digest'].removeprefix('sha256:'))
check('ZIP_SIZE_MATCHES_ARTIFACT', (root/'upload/q042-production-final-v19.zip').stat().st_size==art['size_in_bytes'])
check('FINAL_HASH_MATCHES_INDEX',sha(raw['q042_production_final_v19.json'])==index['final_sha256'])
check('SELECTION_HASH_MATCHES_INDEX_AND_FINAL',sha(raw['q042_v18_artifact_selection_v19.json'])==index['artifact_selection_sha256']==d['source_artifact_selection_manifest_sha256'])
check('SPEC_HASH_MATCHES_LOCK_AND_FINAL',sha(raw['q042_production_spec_v1.json'])==lock['scientific_spec_sha256']==d['scientific_spec_sha256'])
check('V1_SOURCE_LOCK_MATCH',sha((root/'evidence/repo/q042_production_source_lock_v1.json').read_bytes())==lock['scientific_parent_source_lock_sha256'])
check('V18_SOURCE_LOCK_MATCH',sha((root/'evidence/repo/q042_production_source_lock_v18.json').read_bytes())==lock['technical_parent_source_lock_sha256'])
check('V18_PROGRAM_PINNED_HASH_MATCH',sha((root/'evidence/repo/q042_production_v18_pinned.py').read_bytes())==lock['technical_parent']['production_program_sha256'])
check('Q_IDENTITY',d['q']==spec['q']==lock['q']=='Q-042')
check('CASE_ID_REMAINS_NOT_DOCUMENTED',d['case_id']==spec['case_id']==lock['case_id']=='NOT DOCUMENTED')
check('RUN_IDENTITY',run['id']==index['merge_run_id']==art['workflow_run']['id']==37185888043)
check('RUN_COMMIT_IDENTITY',run['head_sha']==art['workflow_run']['head_sha']=='7af1298c5f1db17557d7671d2ea38ca6d67b7df1')
check('LIVE_RUN_COMPLETED',run['status']=='completed' and run['conclusion']=='success')
check('TWENTY_UNIQUE_TERMINAL_CELLS',len(keys)==len(set(keys))==20 and set(keys)==expected)
check('ALL_TERMINAL_CELLS_CONTROLLED_FAILURE',all(c['status']=='CONTROLLED_TECHNICAL_FAILURE' for c in cells))
check('NINETEEN_CHECKPOINT_FAILURES',sum(c['failure_class']=='POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS' for c in cells)==19)
check('ONE_OTHER_FAILURE',sum(c['failure_class']=='HOSTED_RUNNER_OR_NUMERICAL_SEGMENT_FAILURE' for c in cells)==1)
check('ALL_RECORDED_STOCK_CHECKPOINTS_RESUMABLE',all(c['checkpoint_before']['checkpoint_kind']==c['checkpoint_after']['checkpoint_kind']=='STOCK_RESUME' and c['checkpoint_before']['resumable'] and c['checkpoint_after']['resumable'] for c in cells))
check('ALL_STOCK_CHECKPOINT_HASHES_UNCHANGED',all(c['checkpoint_before']['primary_resume_sha256']==c['checkpoint_after']['primary_resume_sha256'] for c in cells))
check('ALL_STOCK_CHECKPOINT_MTIMES_UNCHANGED',all(c['checkpoint_before']['primary_resume_mtime_ns']==c['checkpoint_after']['primary_resume_mtime_ns'] for c in cells))
check('ALL_REPORTED_RESUME_LIFECYCLES_OK',all(c['resume_lifecycle_ok'] for c in cells))
check('NO_COMPLETED_WORKER_RECORDS',all(c['worker'] is None for c in cells))
check('MAX_SEGMENT_BUDGET_NOT_EXHAUSTED',max(c['segment'] for c in cells)<spec['orchestration']['max_polychord_segments_per_cell'])
check('COMPLETE_BOBYQA_CELL_SET',set(tuple(k.split(':')) for k in d['bobyqa'])==expected)
starts=[s for c in d['bobyqa'].values() for s in c['starts']]
check('EIGHTY_UNIQUE_BOBYQA_STARTS',len(starts)==len({(s['arm'],s['model'],s['combination'],s['start_index']) for s in starts})==80)
check('FOUR_STARTS_PER_CELL',all(len(c['starts'])==4 and {s['start_index'] for s in c['starts']}=={0,1,2,3} for c in d['bobyqa'].values()))
check('BOBYQA_FLAGS_PRESERVED',dict(collections.Counter(s['flag'] for s in starts))=={0:78,-3:2})
check('BOBYQA_SOURCE_V1_IDENTITY',all(s['computed_by_program_id']=='Q042-PROD-V1' and s['source_root_run_id']==36133813540 and s['source_execution_commit']=='6c44a4117449145afd0a3ae6eb238490686a8c6d' for s in starts))
best=[]
for k,c in d['bobyqa'].items():
    eligible=[s['objective'] for s in c['starts'] if s['flag']>=0 and math.isfinite(s['objective'])]
    best.append(bool(eligible) and min(eligible)==c['best_objective'] and len(eligible)==c['usable_start_count'])
check('BEST_OBJECTIVES_MATCH_FROZEN_ELIGIBILITY',all(best))
check('NO_NEW_V19_COMPUTE',d['bobyqa_recomputed_in_v19']==d['polychord_recomputed_in_v19']==0)
check('SCIENTIFIC_CONTRACT_UNCHANGED_FLAG',d['scientific_contract_changed'] is False)
check('UNRESOLVED_FAIL_CLOSED',d['final_result_gate']=='UNRESOLVED' and d['actual_computed_scientific_result'] is False and d['downstream_portability_classification']=='NOT_AVAILABLE')
check('TWENTY_ONE_UNIQUE_SOURCE_ARTIFACTS',sel['selected_artifact_count']==len(sel['artifacts'])==len({a['name'] for a in sel['artifacts']})==21)
check('SOURCE_ARTIFACT_COMMIT_IDENTITY',all(a['head_sha']==d['source_execution_commit']=='d0f92c7f2ce53da32818244f8847f8e745e20c4f' for a in sel['artifacts']))
check('CHECKPOINT_LOG_SHOWS_RESUME_AND_INTERRUPT_IN_CLASS',all(t in (root/'evidence/camspec_ede_FULL_terminal.log').read_text() for t in ['Found an old sample. Resuming.','Resuming from previous run','KeyboardInterrupt','self.classy.compute()','RESUME_NO_CHECKPOINT_PROGRESS']))
check('OTHER_FAILURE_LOG_SHOWS_CLASS_NEGATIVE_ELECTRON_FRACTION',all(t in (root/'evidence/camspec_lcdm_FULL_terminal.log').read_text() for t in ['classy.CosmoComputationError','tau_c=-2.403414e+09','x_e=-1.174788e-03','Q042_PROD_V18_SEGMENT_STATUS=FAILED']))
diagnostics=[]
for combo in combos:
    diagnostics.append({'combination':combo,**{arm:2*(d['bobyqa'][f'{arm}:lcdm:{combo}']['best_objective']-d['bobyqa'][f'{arm}:ede_n3:{combo}']['best_objective']) for arm in arms}})
out={'status':'PASS' if all(v=='PASS' for v in checks.values()) else 'FAIL','scope':'Identity, internal consistency, inventory and observed log evidence only; no sampler or likelihood replay. Source ZIP digests for the 21 underlying V18 bundles were not independently downloaded.','gate_count':len(checks),'gates':checks,'member_sha256':{n:sha(b) for n,b in raw.items()},'posterior_terminal_count':20,'completed_posterior_count':0,'terminal_segment_range':[min(c['segment'] for c in cells),max(c['segment'] for c in cells)],'candidate_within_arm_delta_chi2':diagnostics}
(root/'evidence/v19_ingestion_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['status']=='PASS'
```


## APPENDIX F2 — INGESTION AUDIT OUTPUT

**Preserved UTF-8 source SHA-256:** `decc4551f34c2c10ad361e547e7e37d97558d297eda1482f113129256764925b`; bytes: 3535.

```json
{
  "status": "PASS",
  "scope": "Identity, internal consistency, inventory and observed log evidence only; no sampler or likelihood replay. Source ZIP digests for the 21 underlying V18 bundles were not independently downloaded.",
  "gate_count": 36,
  "gates": {
    "ZIP_MATCHES_LIVE_GITHUB_ARTIFACT": "PASS",
    "ZIP_SIZE_MATCHES_ARTIFACT": "PASS",
    "FINAL_HASH_MATCHES_INDEX": "PASS",
    "SELECTION_HASH_MATCHES_INDEX_AND_FINAL": "PASS",
    "SPEC_HASH_MATCHES_LOCK_AND_FINAL": "PASS",
    "V1_SOURCE_LOCK_MATCH": "PASS",
    "V18_SOURCE_LOCK_MATCH": "PASS",
    "V18_PROGRAM_PINNED_HASH_MATCH": "PASS",
    "Q_IDENTITY": "PASS",
    "CASE_ID_REMAINS_NOT_DOCUMENTED": "PASS",
    "RUN_IDENTITY": "PASS",
    "RUN_COMMIT_IDENTITY": "PASS",
    "LIVE_RUN_COMPLETED": "PASS",
    "TWENTY_UNIQUE_TERMINAL_CELLS": "PASS",
    "ALL_TERMINAL_CELLS_CONTROLLED_FAILURE": "PASS",
    "NINETEEN_CHECKPOINT_FAILURES": "PASS",
    "ONE_OTHER_FAILURE": "PASS",
    "ALL_RECORDED_STOCK_CHECKPOINTS_RESUMABLE": "PASS",
    "ALL_STOCK_CHECKPOINT_HASHES_UNCHANGED": "PASS",
    "ALL_STOCK_CHECKPOINT_MTIMES_UNCHANGED": "PASS",
    "ALL_REPORTED_RESUME_LIFECYCLES_OK": "PASS",
    "NO_COMPLETED_WORKER_RECORDS": "PASS",
    "MAX_SEGMENT_BUDGET_NOT_EXHAUSTED": "PASS",
    "COMPLETE_BOBYQA_CELL_SET": "PASS",
    "EIGHTY_UNIQUE_BOBYQA_STARTS": "PASS",
    "FOUR_STARTS_PER_CELL": "PASS",
    "BOBYQA_FLAGS_PRESERVED": "PASS",
    "BOBYQA_SOURCE_V1_IDENTITY": "PASS",
    "BEST_OBJECTIVES_MATCH_FROZEN_ELIGIBILITY": "PASS",
    "NO_NEW_V19_COMPUTE": "PASS",
    "SCIENTIFIC_CONTRACT_UNCHANGED_FLAG": "PASS",
    "UNRESOLVED_FAIL_CLOSED": "PASS",
    "TWENTY_ONE_UNIQUE_SOURCE_ARTIFACTS": "PASS",
    "SOURCE_ARTIFACT_COMMIT_IDENTITY": "PASS",
    "CHECKPOINT_LOG_SHOWS_RESUME_AND_INTERRUPT_IN_CLASS": "PASS",
    "OTHER_FAILURE_LOG_SHOWS_CLASS_NEGATIVE_ELECTRON_FRACTION": "PASS"
  },
  "member_sha256": {
    "q042_production_final_v19.json": "95f024b5ffdde740ae796e54a7dbd02340c14f340b7ea935b70082e0ea607e07",
    "q042_production_artifact_index_v19.json": "202fa0d4e2295f0aa2f10e370f46c9bb15e9a0ee33d870b8bc841ba9bda01f96",
    "q042_v18_artifact_selection_v19.json": "0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f",
    "q042_prod_static_v19.json": "37312818a6bc8cf3f638d8a35f123bc9ec27394b2b858a911adf27f292ffd55b",
    "q042_prod_static_tests_v19.json": "04a496b8db06b8a4a49f534c583a09e7d5c2da000d48e0764a67e327986d0f6b",
    "q042_production_spec_v1.json": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
    "q042_production_recovery_v19.json": "d9d82270f44b26b0e46ea0a181704ebf97629c1f213c4def2b9893ac97a84d4b",
    "q042_production_source_lock_v19.json": "b5367385fd96ccd07db17dcd74f6bbd5a14e1f4c4cc7783abea4554eee02fa3b"
  },
  "posterior_terminal_count": 20,
  "completed_posterior_count": 0,
  "terminal_segment_range": [
    2,
    10
  ],
  "candidate_within_arm_delta_chi2": [
    {
      "combination": "FULL",
      "camspec": -5.202886578325888,
      "hillipop": -7.807410914942011
    },
    {
      "combination": "NO_ACT_LENSING",
      "camspec": -6.102295794285965,
      "hillipop": -2.5458950026445564
    },
    {
      "combination": "NO_ACT_PRIMARY",
      "camspec": -0.16021399016972282,
      "hillipop": 5.070110608394316
    },
    {
      "combination": "NO_DESI_DR2",
      "camspec": -4.648358940409707,
      "hillipop": -4.743352580811916
    },
    {
      "combination": "NO_SN",
      "camspec": 2.7814845174088987,
      "hillipop": -7.122963998288014
    }
  ]
}
```


## APPENDIX G1 — RETRIEVED V19 MERGE-ONLY PROGRAM

**Preserved UTF-8 source SHA-256:** `8f8d5688169bb7f27b6f4d0a88ea2d1c53d927a8c008145d8eeeaea1bc89080b`; bytes: 12353.

```python
#!/usr/bin/env python3
"""Bubbleverse Q042 production recovery V19 — merge-only finalization repair.

V19 performs no new PolyChord or Py-BOBYQA computation. It consumes the exact
existing Q042-PROD-V18 artifact set from frozen root run 36731879692, adapts
only the recovery-owned filenames expected by the inherited V1 merge routine,
and then delegates all scientific merge/classification logic byte-for-byte to
q042_production_v1.merge_final.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import q042_production_v1 as v1

Q = "Q-042"
CASE_ID = "NOT DOCUMENTED"
PROGRAM_ID = "Q042-PROD-V19"
RUN_ID = "Q042-PRODUCTION-PORTABILITY-V19"
RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-019"

SOURCE_PROGRAM_ID = "Q042-PROD-V18"
SOURCE_RUN_ID = "Q042-PRODUCTION-PORTABILITY-V18"
SOURCE_RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-018"
SOURCE_ROOT_RUN_ID = 36731879692
SOURCE_EXECUTION_COMMIT = "d0f92c7f2ce53da32818244f8847f8e745e20c4f"
SOURCE_FAILED_COLLECTOR_RUN_ID = 37151674348
SOURCE_FAILED_COLLECTOR_JOB_ID = 111286678009

V1_SPEC_SHA256 = "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256 = "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V18_SOURCE_LOCK_SHA256 = "6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde"
V18_PROGRAM_SHA256 = "19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962"
V18_WORKFLOW_SHA256 = "95ecae46549732f6fc1263a5d0116590ca784104bc11894a279a8cce4a175a5c"

ARMS = ("camspec", "hillipop")
MODELS = ("lcdm", "ede_n3")
COMBINATIONS = ("FULL", "NO_ACT_PRIMARY", "NO_ACT_LENSING", "NO_DESI_DR2", "NO_SN")


def sha256_file(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def read_json(p):
    x = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return x


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False, default=str) + "\n", encoding="utf-8")
    os.replace(t, p)


def load_spec(p):
    p = Path(p)
    if sha256_file(p) != V1_SPEC_SHA256:
        raise RuntimeError("SCIENTIFIC_SPEC_BYTE_IDENTITY_GATE=FAIL")
    d = read_json(p)
    if (d.get("q"), d.get("case_id"), d.get("program_id"), d.get("run_id"), d.get("result_id")) != (
        Q, CASE_ID, "Q042-PROD-V1", "Q042-PRODUCTION-PORTABILITY-V1", "R-Q042-PRODUCTION-PORTABILITY-001"
    ):
        raise RuntimeError("SCIENTIFIC_SPEC_IDENTITY_GATE=FAIL")
    c = d.get("authoritative_contract") or {}
    if tuple(c.get("arms") or ()) != ARMS or tuple(c.get("models") or ()) != MODELS:
        raise RuntimeError("AUTHORITATIVE_CONTRACT_GATE=FAIL")
    if set((c.get("data_combinations") or {}).keys()) != set(COMBINATIONS) or int(c.get("required_cell_count", -1)) != 20:
        raise RuntimeError("AUTHORITATIVE_CELL_MATRIX_GATE=FAIL")
    return d


def load_lock(p, spec):
    d = read_json(p)
    if (d.get("q"), d.get("case_id"), d.get("program_id"), d.get("run_id"), d.get("result_id")) != (
        Q, CASE_ID, PROGRAM_ID, RUN_ID, RESULT_ID
    ):
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("scientific_spec_sha256") != sha256_file(spec):
        raise RuntimeError("SOURCE_LOCK_SCIENTIFIC_SPEC_GATE=FAIL")
    v1lock = Path(d.get("scientific_parent_source_lock_file", ""))
    if not v1lock.is_file() or sha256_file(v1lock) != d.get("scientific_parent_source_lock_sha256") or sha256_file(v1lock) != V1_SOURCE_LOCK_SHA256:
        raise RuntimeError("V1_PARENT_SOURCE_LOCK_GATE=FAIL")
    v18lock = Path(d.get("technical_parent_source_lock_file", ""))
    if not v18lock.is_file() or sha256_file(v18lock) != d.get("technical_parent_source_lock_sha256") or sha256_file(v18lock) != V18_SOURCE_LOCK_SHA256:
        raise RuntimeError("V18_PARENT_SOURCE_LOCK_GATE=FAIL")
    tp = d.get("technical_parent") or {}
    if tp.get("program_id") != SOURCE_PROGRAM_ID or int(tp.get("root_github_run_id", -1)) != SOURCE_ROOT_RUN_ID or tp.get("execution_commit") != SOURCE_EXECUTION_COMMIT:
        raise RuntimeError("V18_TECHNICAL_PARENT_GATE=FAIL")
    return d


def expected_cells():
    return {(a, m, c) for a in ARMS for m in MODELS for c in COMBINATIONS}


def validate_source_records(root: Path):
    poly_paths = list(root.rglob("q042_production_polychord_final_v18.json"))
    bob_paths = list(root.rglob("q042_production_bobyqa_start_v13.json"))
    if len(poly_paths) != 20:
        raise RuntimeError(f"V18_POLYCHORD_FINAL_COUNT_GATE=FAIL count={len(poly_paths)}")
    if len(bob_paths) != 80:
        raise RuntimeError(f"V18_BOBYQA_IMPORT_COUNT_GATE=FAIL count={len(bob_paths)}")

    seen = set()
    for p in poly_paths:
        d = read_json(p)
        if d.get("q") != Q or d.get("program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError(f"V18_POLYCHORD_IDENTITY_GATE=FAIL path={p}")
        cell = (d.get("arm"), d.get("model"), d.get("combination"))
        if cell in seen:
            raise RuntimeError(f"V18_POLYCHORD_DUPLICATE_CELL_GATE=FAIL cell={cell}")
        seen.add(cell)
    if seen != expected_cells():
        raise RuntimeError(f"V18_POLYCHORD_CELL_COMPLETENESS_GATE=FAIL missing={sorted(expected_cells()-seen)}")

    starts = {}
    for p in bob_paths:
        d = read_json(p)
        if d.get("q") != Q or d.get("program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError(f"V18_BOBYQA_IDENTITY_GATE=FAIL path={p}")
        cell = (d.get("arm"), d.get("model"), d.get("combination"))
        idx = int(d.get("start_index", -1))
        starts.setdefault(cell, set()).add(idx)
    if set(starts) != expected_cells() or any(v != {0,1,2,3} for v in starts.values()):
        raise RuntimeError("V18_BOBYQA_CELL_START_COMPLETENESS_GATE=FAIL")
    return poly_paths, bob_paths


def install_compatibility_shadows(poly_paths, bob_paths):
    shadows = []
    for p in poly_paths:
        q = p.with_name("q042_production_polychord_final_v1.json")
        if q.exists():
            raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
        shutil.copy2(p, q)
        shadows.append(q)
    for p in bob_paths:
        q = p.with_name("q042_production_bobyqa_start_v1.json")
        if q.exists():
            raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
        shutil.copy2(p, q)
        shadows.append(q)
    return shadows


def configure_v1_merge_for_v18_inputs():
    # Inputs are genuine V18 records. Keep V18 identity while the inherited V1
    # merge routine reads them; V19 relabels only the final technical envelope.
    v1.Q = Q
    v1.CASE_ID = CASE_ID
    v1.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.RUN_ID = SOURCE_RUN_ID
    v1.RESULT_ID = SOURCE_RESULT_ID
    v1.core.Q = Q
    v1.core.CASE_ID = CASE_ID
    v1.core.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.core.RUN_ID = SOURCE_RUN_ID
    v1.core.RESULT_ID = SOURCE_RESULT_ID
    v1.core.legacy.Q = Q
    v1.core.legacy.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.core.legacy.RUN_ID = SOURCE_RUN_ID
    v1.core.legacy.RESULT_ID = SOURCE_RESULT_ID
    v1.load_spec = load_spec
    v1.load_lock = load_lock


def merge_final(a):
    load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    root = Path(a.input_dir)
    poly_paths, bob_paths = validate_source_records(root)

    manifest = read_json(a.artifact_manifest) if a.artifact_manifest else None
    if manifest is not None:
        if manifest.get("q") != Q or manifest.get("source_program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError("ARTIFACT_MANIFEST_IDENTITY_GATE=FAIL")
        if int(manifest.get("source_root_run_id", -1)) != SOURCE_ROOT_RUN_ID or int(manifest.get("selected_artifact_count", -1)) != 21:
            raise RuntimeError("ARTIFACT_MANIFEST_COUNT_GATE=FAIL")

    shadows = install_compatibility_shadows(poly_paths, bob_paths)
    try:
        configure_v1_merge_for_v18_inputs()
        rc = v1.merge_final(a)
    finally:
        for p in shadows:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    out = read_json(a.output)
    inherited_gate = out.get("final_result_gate")
    inherited_class = out.get("downstream_portability_classification")
    out.update({
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "PRODUCTION_FINAL_V19",
        "technical_recovery_class": "MERGE_ONLY_EXISTING_V18_ARTIFACTS",
        "scientific_contract_changed": False,
        "scientific_spec_origin_program_id": "Q042-PROD-V1",
        "scientific_spec_sha256": sha256_file(a.spec),
        "source_program_id": SOURCE_PROGRAM_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_result_id": SOURCE_RESULT_ID,
        "source_root_github_run_id": SOURCE_ROOT_RUN_ID,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_failed_collector_run_id": SOURCE_FAILED_COLLECTOR_RUN_ID,
        "source_failed_collector_job_id": SOURCE_FAILED_COLLECTOR_JOB_ID,
        "source_failed_collector_gate": "V13_POLYCHORD_FINAL_COUNT_GATE=FAIL",
        "source_polychord_final_filename": "q042_production_polychord_final_v18.json",
        "source_bobyqa_record_filename": "q042_production_bobyqa_start_v13.json",
        "polychord_recomputed_in_v19": 0,
        "bobyqa_recomputed_in_v19": 0,
        "source_polychord_final_count": 20,
        "source_bobyqa_record_count": 80,
        "inherited_v1_final_result_gate": inherited_gate,
        "inherited_v1_downstream_portability_classification": inherited_class,
        "technical_parent_source_lock_sha256": lock["technical_parent_source_lock_sha256"],
    })
    gates = out.setdefault("gates", {})
    gates["V18_ARTIFACT_SET_COMPLETE"] = "PASS"
    gates["V18_POLYCHORD_FINAL_FILENAME_ADAPTER"] = "PASS"
    gates["V18_BOBYQA_COMPATIBILITY_FILENAME_ADAPTER"] = "PASS"
    gates["V1_SCIENTIFIC_MERGE_CLASSIFICATION_REUSED"] = "PASS"
    gates["NO_NEW_POLYCHORD_COMPUTE_V19"] = "PASS"
    gates["NO_NEW_BOBYQA_COMPUTE_V19"] = "PASS"
    if manifest is not None:
        gates["V18_ARTIFACT_DIGEST_SELECTION_MANIFEST"] = "PASS"
        out["source_artifact_selection_manifest_sha256"] = sha256_file(a.artifact_manifest)
    write_json(a.output, out)
    print("Q042_PROD_V19_FINAL_GATE=" + str(out.get("final_result_gate")))
    return rc


def static_check(a):
    load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    write_json(a.output, {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "MERGE_ONLY_STATIC_V19",
        "status": "PASS",
        "scientific_result": False,
        "scientific_contract_changed": False,
        "source_program_id": SOURCE_PROGRAM_ID,
        "source_root_github_run_id": SOURCE_ROOT_RUN_ID,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "required_polychord_final_count": 20,
        "required_bobyqa_record_count": 80,
        "new_compute": False,
        "gates": {
            "V1_SCIENTIFIC_SPEC_BYTE_IDENTITY": "PASS",
            "V1_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
            "V18_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
            "V18_TECHNICAL_PARENT": "PASS",
            "MERGE_ONLY": "PASS",
        },
    })
    print("Q042_PROD_V19_STATIC_GATE=PASS")
    return 0


def parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("static")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=static_check)
    s = sp.add_parser("merge-final")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--artifact-manifest", required=False, default="")
    s.add_argument("--output", required=True)
    s.set_defaults(func=merge_final)
    return p


if __name__ == "__main__":
    a = parser().parse_args()
    raise SystemExit(a.func(a))
```


## APPENDIX G2 — PINNED V18 PRODUCTION PROGRAM

**Preserved UTF-8 source SHA-256:** `19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962`; bytes: 49387.

```python
#!/usr/bin/env python3
"""Bubbleverse Q042 production recovery V18.

Technical recovery only. The authoritative scientific contract remains
q042_production_spec_v1.json byte-for-byte. Q042-PROD-V18 fixes the V1
PolyChord sampler-option adapter and reuses verified V1 BOBYQA records.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import q042_cobaya_partial_resume_adapter_v18 as cobaya_partial_resume_adapter

import q042_production_v1 as v1

Q = "Q-042"
CASE_ID = "NOT DOCUMENTED"
PROGRAM_ID = "Q042-PROD-V18"
RUN_ID = "Q042-PRODUCTION-PORTABILITY-V18"
RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-018"

SCIENTIFIC_SPEC_PROGRAM_ID = "Q042-PROD-V1"
SCIENTIFIC_RUN_ID = "Q042-PRODUCTION-PORTABILITY-V1"
SCIENTIFIC_RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-001"

V1_EXECUTION_COMMIT = "6c44a4117449145afd0a3ae6eb238490686a8c6d"
V1_ROOT_RUN_ID = 36133813540
V1_SPEC_SHA256 = "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256 = "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V1_PROGRAM_SHA256 = "889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642"

ARMS = ("camspec", "hillipop")
MODELS = ("lcdm", "ede_n3")
COMBINATIONS = ("FULL", "NO_ACT_PRIMARY", "NO_ACT_LENSING", "NO_DESI_DR2", "NO_SN")

# Only options that belong to Cobaya's PolyChord component may cross this adapter.
# Descriptive preregistration metadata stays in the scientific spec and provenance.
POLYCHORD_EXECUTABLE_KEYS = (
    "nlive",
    "num_repeats",
    "nprior",
    "nfail",
    "precision_criterion",
    "max_ndead",
    "do_clustering",
    "boost_posterior",
    "confidence_for_unbounded",
    "measure_speeds",
    "oversample_power",
    "synchronous",
    "read_resume",
    "write_resume",
    "write_live",
    "write_dead",
    "write_prior",
    "write_stats",
)
POLYCHORD_METADATA_ONLY_KEYS = ("seed_policy", "max_ndead_runtime_encoding")


def finite(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def read_json(p):
    x = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return x


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(
        json.dumps(obj, indent=2, sort_keys=True, allow_nan=False, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(t, p)


def sha256_file(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def canonical_hash(x):
    return hashlib.sha256(
        json.dumps(x, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def freeze_v1_globals():
    """Make inherited V1 helper functions emit the current technical execution identity."""
    v1.Q = Q
    v1.CASE_ID = CASE_ID
    v1.PROGRAM_ID = PROGRAM_ID
    v1.RUN_ID = RUN_ID
    v1.RESULT_ID = RESULT_ID

    v1.core.Q = Q
    v1.core.CASE_ID = CASE_ID
    v1.core.PROGRAM_ID = PROGRAM_ID
    v1.core.RUN_ID = RUN_ID
    v1.core.RESULT_ID = RESULT_ID
    v1.core.legacy.Q = Q
    v1.core.legacy.PROGRAM_ID = PROGRAM_ID
    v1.core.legacy.RUN_ID = RUN_ID
    v1.core.legacy.RESULT_ID = RESULT_ID


def load_spec(p):
    p = Path(p)
    if sha256_file(p) != V1_SPEC_SHA256:
        raise RuntimeError("SCIENTIFIC_SPEC_BYTE_IDENTITY_GATE=FAIL")
    d = read_json(p)
    if (
        d.get("q"),
        d.get("case_id"),
        d.get("program_id"),
        d.get("run_id"),
        d.get("result_id"),
    ) != (
        Q,
        CASE_ID,
        SCIENTIFIC_SPEC_PROGRAM_ID,
        SCIENTIFIC_RUN_ID,
        SCIENTIFIC_RESULT_ID,
    ):
        raise RuntimeError("SCIENTIFIC_SPEC_IDENTITY_GATE=FAIL")

    c = d["authoritative_contract"]
    if (
        tuple(c["arms"]) != ARMS
        or tuple(c["models"]) != MODELS
        or set(c["data_combinations"]) != set(COMBINATIONS)
        or int(c["required_cell_count"]) != 20
    ):
        raise RuntimeError("AUTHORITATIVE_CONTRACT_GATE=FAIL")

    pc = d["polychord_production"]
    frozen = {
        "nlive": "25d",
        "num_repeats": "5d",
        "nprior": "10nlive",
        "nfail": "nlive",
        "precision_criterion": 0.001,
        "max_ndead": "infinity",
        "do_clustering": True,
        "boost_posterior": 0,
        "confidence_for_unbounded": 0.9999995,
        "measure_speeds": True,
        "oversample_power": 0.4,
        "synchronous": True,
        "read_resume": True,
        "write_resume": True,
        "write_live": True,
        "write_dead": True,
        "write_prior": True,
        "write_stats": True,
    }
    for k, expected in frozen.items():
        if pc.get(k) != expected:
            raise RuntimeError(f"POLYCHORD_PRODUCTION_LOCK_GATE=FAIL key={k}")
    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k not in pc:
            raise RuntimeError(f"POLYCHORD_METADATA_PRESERVATION_GATE=FAIL key={k}")

    bq = d["bobyqa_production"]
    if (
        int(bq["external_starts_per_cell"]) != 4
        or int(bq["cobaya_best_of"]) != 1
        or bq["max_evals"] != "120d"
        or float(bq["rhoend"]) != 0.05
        or bq["ignore_prior"] is not True
    ):
        raise RuntimeError("BOBYQA_PRODUCTION_LOCK_GATE=FAIL")

    seeds = d["polychord_seed_map"]
    if len(seeds) != 20 or len(set(int(x) for x in seeds.values())) != 20:
        raise RuntimeError("SEED_MAP_GATE=FAIL")
    return d


def load_lock(p, spec):
    d = read_json(p)
    if (
        d.get("q"),
        d.get("case_id"),
        d.get("program_id"),
        d.get("run_id"),
        d.get("result_id"),
    ) != (Q, CASE_ID, PROGRAM_ID, RUN_ID, RESULT_ID):
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("scientific_spec_sha256") != sha256_file(spec):
        raise RuntimeError("SOURCE_LOCK_SCIENTIFIC_SPEC_GATE=FAIL")
    parent = Path(d.get("parent_source_lock_file", ""))
    if not parent.exists() or sha256_file(parent) != d.get("parent_source_lock_sha256"):
        raise RuntimeError("PARENT_SOURCE_LOCK_GATE=FAIL")
    if d.get("parent_source_lock_sha256") != V1_SOURCE_LOCK_SHA256:
        raise RuntimeError("PARENT_SOURCE_LOCK_FROZEN_HASH_GATE=FAIL")
    if d.get("technical_parent", {}).get("execution_commit") != V1_EXECUTION_COMMIT:
        raise RuntimeError("TECHNICAL_PARENT_COMMIT_GATE=FAIL")
    if int(d.get("technical_parent", {}).get("root_github_run_id", -1)) != V1_ROOT_RUN_ID:
        raise RuntimeError("TECHNICAL_PARENT_RUN_GATE=FAIL")
    return d


PARTIAL_INIT_RUNTIME_MANIFEST = Path("q042_runtime/q042_polychord_partial_init_v17.json")
PARTIAL_INIT_BASE_COMMIT = "3ade6445bb3719a6db6f6e81f178765545ffc833"
PARTIAL_INIT_CHECKPOINT_INTERVAL = 25
PARTIAL_INIT_PATCHER_SHA256 = "22ca8d786e2061e99454d1940a6f1fe12b9bcef0632a9524f3a0bb79c9facce6"
PARTIAL_INIT_SELFTEST_SHA256 = "1208f10b703e85511882c1f5251e8facf62179cc6e5f5194ef633ac6fd7975f9"


def partial_init_runtime_gate():
    if not PARTIAL_INIT_RUNTIME_MANIFEST.exists():
        raise RuntimeError("PARTIAL_INIT_RUNTIME_MANIFEST_GATE=FAIL")
    d=read_json(PARTIAL_INIT_RUNTIME_MANIFEST)
    if (
        d.get("status")!="PASS"
        or d.get("base_commit")!=PARTIAL_INIT_BASE_COMMIT
        or int(d.get("checkpoint_interval",-1))!=PARTIAL_INIT_CHECKPOINT_INTERVAL
        or d.get("serial_only") is not True
        or d.get("patcher_sha256")!=PARTIAL_INIT_PATCHER_SHA256
        or d.get("selftest_sha256")!=PARTIAL_INIT_SELFTEST_SHA256
        or d.get("selftest_status")!="PASS"
        or d.get("selftest_exact_resume_byte_identity") is not True
    ):
        raise RuntimeError("PARTIAL_INIT_RUNTIME_CONTENT_GATE=FAIL")
    for key in ("generate_file","nested_sampling_file","libchord_file"):
        p=Path(d.get(key,""))
        if not p.is_file():
            raise RuntimeError(f"PARTIAL_INIT_RUNTIME_FILE_GATE=FAIL key={key}")
        hk=key.replace("_file","_sha256")
        if sha256_file(p)!=d.get(hk):
            raise RuntimeError(f"PARTIAL_INIT_RUNTIME_HASH_GATE=FAIL key={key}")
    return d


COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_MANIFEST = Path("q042_runtime/q042_cobaya_partial_resume_adapter_v18.json")
COBAYA_PARTIAL_RESUME_ADAPTER_SHA256 = "b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567"


def cobaya_partial_resume_adapter_runtime_gate():
    if not COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_MANIFEST.exists():
        raise RuntimeError("COBAYA_PARTIAL_RESUME_ADAPTER_MANIFEST_GATE=FAIL")
    d=read_json(COBAYA_PARTIAL_RESUME_ADAPTER_RUNTIME_MANIFEST)
    if (
        d.get("status")!="PASS"
        or d.get("program_id")!=PROGRAM_ID
        or d.get("cobaya_version")!="3.5.6"
        or d.get("adapter_sha256")!=COBAYA_PARTIAL_RESUME_ADAPTER_SHA256
        or d.get("baseline_cleanup_observed") is not True
        or d.get("adapted_resuming") is not True
        or d.get("adapted_partial_checkpoint_preserved") is not True
    ):
        raise RuntimeError("COBAYA_PARTIAL_RESUME_ADAPTER_CONTENT_GATE=FAIL")
    return d


def runtime_gate(p):
    r = read_json(p)
    # Runtime is intentionally the recovered V1 production runtime.
    patch_runtime = partial_init_runtime_gate()
    adapter_runtime = cobaya_partial_resume_adapter_runtime_gate()
    if (
        r.get("q") != Q
        or r.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID
        or r.get("status") != "PASS"
        or r.get("cobaya_version") != "3.5.6"
        or r.get("pybobyqa_version") != "1.5.0"
        or r.get("polychord_commit") != "3ade6445bb3719a6db6f6e81f178765545ffc833"
        or not r.get("pantheonplus_runtime_files")
        or not r.get("pantheonplus_manifest_sha256")
    ):
        raise RuntimeError("RECOVERED_V1_RUNTIME_SOURCE_GATE=FAIL")
    return r


def cell_seed(spec, arm, model, combo):
    return int(spec["polychord_seed_map"][f"{arm}:{model}:{combo}"])


def production_pc(spec, runtime, arm, model, combo):
    """Recovery repair: metadata and executable sampler options are separated."""
    source = spec["polychord_production"]
    pc = {}
    for key in POLYCHORD_EXECUTABLE_KEYS:
        if key not in source:
            raise RuntimeError(f"POLYCHORD_EXECUTABLE_OPTION_MISSING_GATE=FAIL key={key}")
        pc[key] = copy.deepcopy(source[key])

    if pc["max_ndead"] != "infinity":
        raise RuntimeError("POLYCHORD_INFINITY_SEMANTICS_GATE=FAIL")
    pc["max_ndead"] = float("inf")
    pc["path"] = runtime["polychord_path"]
    pc["seed"] = cell_seed(spec, arm, model, combo)

    leaked = [k for k in POLYCHORD_METADATA_ONLY_KEYS if k in pc]
    if leaked:
        raise RuntimeError(f"POLYCHORD_METADATA_LEAK_GATE=FAIL keys={leaked}")
    return pc


def validate_polychord_options(pc):
    import cobaya
    from cobaya.input import update_info

    if getattr(cobaya, "__version__", None) != "3.5.6":
        raise RuntimeError(
            f"COBAYA_PIN_GATE=FAIL got={getattr(cobaya, '__version__', None)}"
        )
    updated = update_info({"sampler": {"polychord": copy.deepcopy(pc)}})
    block = (updated.get("sampler") or {}).get("polychord")
    if not isinstance(block, dict):
        raise RuntimeError("COBAYA_POLYCHORD_UPDATE_INFO_GATE=FAIL")
    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k in block:
            raise RuntimeError(f"COBAYA_METADATA_LEAK_AFTER_UPDATE_GATE=FAIL key={k}")
    return block


def static_check(a):
    spec = load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    write_json(
        a.output,
        {
            "q": Q,
            "case_id": CASE_ID,
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "PRODUCTION_RECOVERY_STATIC_V18",
            "status": "PASS",
            "scientific_spec_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "scientific_spec_sha256": sha256_file(a.spec),
            "parent_source_lock_sha256": lock["parent_source_lock_sha256"],
            "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
            "technical_parent_root_run_id": V1_ROOT_RUN_ID,
            "required_cell_count": 20,
            "seed_count": 20,
            "scientific_result": False,
            "gates": {
                "Q_IDENTITY": "PASS",
                "V1_SCIENTIFIC_SPEC_BYTE_IDENTITY": "PASS",
                "V1_SOURCE_LOCK_IDENTITY": "PASS",
                "PRODUCTION_SETTINGS_FROZEN": "PASS",
                "METADATA_PRESERVED_IN_SPEC": "PASS",
                "Q040_FIREWALL": "PASS",
                "NO_PILOT_SCIENCE": "PASS",
            },
        },
    )
    print("Q042_PROD_V18_STATIC_GATE=PASS")
    return 0


def sampler_adapter_regression(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    runtime = runtime_gate(a.external_runtime)

    raw = copy.deepcopy(spec["polychord_production"])
    raw["max_ndead"] = float("inf")
    raw["path"] = runtime["polychord_path"]
    raw["seed"] = cell_seed(spec, "camspec", "lcdm", "FULL")

    raw_rejected = False
    raw_error = ""
    try:
        validate_polychord_options(raw)
    except Exception as exc:
        raw_rejected = True
        raw_error = f"{type(exc).__name__}: {exc}"

    if not raw_rejected:
        raise RuntimeError("V1_DICTIONARY_REJECTION_REGRESSION_GATE=FAIL")

    corrected = production_pc(spec, runtime, "camspec", "lcdm", "FULL")
    validate_polychord_options(corrected)

    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k not in spec["polychord_production"] or k in corrected:
            raise RuntimeError(f"METADATA_SEPARATION_GATE=FAIL key={k}")

    if not math.isinf(float(corrected["max_ndead"])):
        raise RuntimeError("POLYCHORD_INFINITY_RUNTIME_ENCODING_GATE=FAIL")

    write_json(
        a.output,
        {
            "q": Q,
            "program_id": PROGRAM_ID,
            "stage": "POLYCHORD_ADAPTER_REGRESSION_V18",
            "status": "PASS",
            "cobaya_version": "3.5.6",
            "v1_dictionary_rejected": True,
            "v1_rejection_error": raw_error[:2000],
            "corrected_dictionary_accepted": True,
            "metadata_preserved_in_scientific_spec": list(POLYCHORD_METADATA_ONLY_KEYS),
            "metadata_excluded_from_executable_sampler": list(POLYCHORD_METADATA_ONLY_KEYS),
            "max_ndead_runtime_is_numeric_infinity": True,
            "seed": corrected["seed"],
            "executable_sampler_keys": sorted(corrected),
        },
    )
    print("Q042_PROD_V18_POLYCHORD_ADAPTER_REGRESSION=PASS")
    return 0


def prepare_nonoverlap(a):
    rc = v1.prepare_nonoverlap(a)
    for p in (Path(a.support_output), Path(a.meta_output)):
        d = read_json(p)
        d.update(
            {
                "q": Q,
                "case_id": CASE_ID,
                "program_id": PROGRAM_ID,
                "run_id": RUN_ID,
                "result_id": RESULT_ID,
                "technical_parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            }
        )
        write_json(p, d)
    return rc


def runtime_preflight(a):
    # Reuse V1's exact science-building checks, then validate the exact recovered sampler adapter
    # across every one of the 20 production cells.
    rc = v1.runtime_preflight(a)
    spec = load_spec(a.spec)
    runtime = runtime_gate(a.external_runtime)
    rows = []
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                pc = production_pc(spec, runtime, arm, model, combo)
                updated = validate_polychord_options(pc)
                rows.append(
                    {
                        "arm": arm,
                        "model": model,
                        "combination": combo,
                        "seed": pc["seed"],
                        "status": "PASS",
                        "runtime_sampler_sha256": canonical_hash(pc),
                        "validated_key_count": len(updated),
                    }
                )
    if len(rows) != 20:
        raise RuntimeError("POLYCHORD_ADAPTER_20_CELL_GATE=FAIL")

    d = read_json(a.output)
    d["stage"] = "PRODUCTION_RUNTIME_PREFLIGHT_V18"
    d["program_id"] = PROGRAM_ID
    d["run_id"] = RUN_ID
    d["result_id"] = RESULT_ID
    d["scientific_spec_origin_program_id"] = SCIENTIFIC_SPEC_PROGRAM_ID
    d["polychord_adapter_validation"] = rows
    d.setdefault("gates", {})["POLYCHORD_EXACT_RUNTIME_DICTIONARY_20_CELL"] = "PASS"
    d["gates"]["COBAYA_3_5_6_INPUT_VALIDATION"] = "PASS"
    d["gates"]["V1_METADATA_LEAK_REMOVED"] = "PASS"
    write_json(a.output, d)
    print("Q042_PROD_V18_RUNTIME_PREFLIGHT_GATE=PASS")
    return rc


def polychord_worker(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    runtime = runtime_gate(a.external_runtime)
    outdir = Path(a.output_dir)
    prefix = (outdir / "polychord" / "chain").resolve()
    prefix.parent.mkdir(parents=True, exist_ok=True)

    built, _ = v1.build_info(a, a.arm, a.model, a.combination, prefix)
    pc = production_pc(spec, runtime, a.arm, a.model, a.combination)
    contract_hash = canonical_hash({
        "pc": spec["polychord_production"],
        "seed": pc["seed"],
        "arm": a.arm,
        "model": a.model,
        "combination": a.combination,
    })

    cobaya_partial_resume_adapter_installed = False
    if a.action == "fresh":
        info = built
        info["sampler"] = {"polychord": pc}
        info["output"] = str(prefix)
        info["force"] = True
        info["resume"] = False
        source = "FRESH_BUILT_INFO"
    else:
        info = copy.deepcopy(v1.stored_info(prefix))
        sp = (info.get("sampler") or {}).get("polychord") or {}
        if int(sp.get("seed", pc["seed"])) != pc["seed"]:
            raise RuntimeError("POLYCHORD_STORED_SEED_GATE=FAIL")
        info["output"] = str(prefix)
        info["force"] = False
        info["resume"] = True
        source = "COBAYA_STORED_UPDATED_INFO"

        raw_dir = prefix.parent / (prefix.name + "_polychord_raw")
        partial_file = raw_dir / (prefix.name + ".partial_init")
        stock_resume_file = raw_dir / (prefix.name + ".resume")
        if partial_file.is_file() and partial_file.stat().st_size > 0 and not stock_resume_file.is_file():
            cobaya_partial_resume_adapter.install_partial_init_resume_detection()
            cobaya_partial_resume_adapter_installed = True

    lifecycle = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "POLYCHORD_WORKER_LIFECYCLE_V8",
        "status": "STARTED",
        "action": a.action,
        "resume_input_source": source,
        "arm": a.arm,
        "model": a.model,
        "combination": a.combination,
        "seed": pc["seed"],
        "sampler_contract_sha256": contract_hash,
        "started_unix": time.time(),
        "cobaya_partial_resume_adapter_installed": cobaya_partial_resume_adapter_installed,
    }
    write_json(outdir / "worker_lifecycle_v18.json", lifecycle)

    from cobaya.run import run as cobaya_run
    sm = None
    try:
        _, sm = cobaya_run(
            info,
            output=str(prefix),
            force=(a.action == "fresh"),
            resume=(a.action == "resume"),
            stop_at_error=True,
        )
        prod = sm.products() if sm is not None else {}
        sample = prod.get("sample") if isinstance(prod, dict) else None
        write_json(
            a.result_json,
            {
                "q": Q,
                "program_id": PROGRAM_ID,
                "stage": "POLYCHORD_PRODUCTION_WORKER",
                "status": "COMPLETE",
                "arm": a.arm,
                "model": a.model,
                "combination": a.combination,
                "seed": pc["seed"],
                "sampler_contract_sha256": contract_hash,
                "resume_input_source": source,
                "sample_count": len(sample) if sample is not None else 0,
                "runtime_commit": runtime["polychord_commit"],
            },
        )
        lifecycle["status"] = "COMPLETE"
        lifecycle["completed_unix"] = time.time()
        write_json(outdir / "worker_lifecycle_v18.json", lifecycle)
        print("Q042_PROD_POLYCHORD_WORKER=COMPLETE")
        return 0
    finally:
        try:
            if sm is not None and hasattr(sm, "close"):
                sm.close()
        except Exception:
            pass


def _read_partial_meta(path):
    out={}
    p=Path(path)
    if not p.is_file():
        return out
    for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
        if "=" not in line:
            continue
        k,v=line.split("=",1)
        try: out[k]=int(v)
        except Exception: out[k]=v
    return out


def checkpoint_state(outdir, expected_seed=None):
    outdir = Path(outdir)
    polydir = outdir / "polychord"
    resume = sorted([p for p in polydir.rglob("*resume*") if p.is_file()])
    nonempty = [p for p in resume if p.stat().st_size > 0]
    partial = sorted([p for p in polydir.rglob("*.partial_init") if p.is_file() and p.stat().st_size > 0])
    partial_meta_files = sorted([p for p in polydir.rglob("*.partial_init.meta") if p.is_file()])
    partial_meta = _read_partial_meta(partial_meta_files[0]) if partial_meta_files else {}

    updated = polydir / "chain.updated.yaml"
    updated_ok = updated.is_file() and updated.stat().st_size > 0
    updated_seed_ok = False
    updated_error = None
    if updated_ok:
        try:
            import yaml
            d = yaml.safe_load(updated.read_text(encoding="utf-8"))
            sp = ((d or {}).get("sampler") or {}).get("polychord") or {}
            got = sp.get("seed", expected_seed)
            updated_seed_ok = expected_seed is None or int(got) == int(expected_seed)
        except Exception as exc:
            updated_error = f"{type(exc).__name__}: {exc}"

    checkpoint_kind = "STOCK_RESUME" if nonempty else "PARTIAL_INIT" if partial else None
    primary = nonempty[0] if nonempty else partial[0] if partial else None
    lifecycle_path = outdir / "worker_lifecycle_v18.json"
    lifecycle = read_json(lifecycle_path) if lifecycle_path.exists() else None
    return {
        "checkpoint_kind": checkpoint_kind,
        "resume_files": [str(p.relative_to(outdir)) for p in resume],
        "nonempty_resume_files": [str(p.relative_to(outdir)) for p in nonempty],
        "partial_init_files": [str(p.relative_to(outdir)) for p in partial],
        "partial_init_meta_files": [str(p.relative_to(outdir)) for p in partial_meta_files],
        "partial_init_meta": partial_meta,
        "partial_init_accepted": int(partial_meta.get("accepted",-1)) if partial_meta else None,
        "partial_init_nprior": int(partial_meta.get("nprior",-1)) if partial_meta else None,
        "primary_resume_sha256": sha256_file(primary) if primary else None,
        "primary_resume_mtime_ns": primary.stat().st_mtime_ns if primary else None,
        "updated_yaml": str(updated.relative_to(outdir)) if updated.exists() else None,
        "updated_yaml_nonempty": updated_ok,
        "updated_seed_ok": updated_seed_ok,
        "updated_error": updated_error,
        "lifecycle": lifecycle,
        "resumable": bool((nonempty or partial) and updated_ok and updated_seed_ok),
    }

def common_cli(a):
    out = []
    for k in (
        "q032_parent_root",
        "preflight",
        "parent_dir",
        "hlp_matrix",
        "hlp_meta",
        "reduced_support",
        "reduced_hlp_matrix",
        "reduced_hlp_meta",
        "spec",
        "source_lock",
        "external_runtime",
    ):
        out += ["--" + k.replace("_", "-"), str(getattr(a, k))]
    return out


def polychord_segment(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    runtime_gate(a.external_runtime)
    if a.arm not in ARMS or a.model not in MODELS or a.combination not in COMBINATIONS:
        raise RuntimeError("CELL_IDENTITY_GATE=FAIL")
    if a.segment < 0:
        raise RuntimeError("SEGMENT_INDEX_GATE=FAIL")

    outdir = Path(a.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    action = "fresh" if a.segment == 0 else "resume"
    seed = cell_seed(spec, a.arm, a.model, a.combination)
    # V13 partial-init checkpoint format is deliberately serial-only so the
    # saved Fortran RNG state is a complete deterministic state.
    mpi_ranks = int(getattr(a, "mpi_ranks", 1))
    if mpi_ranks != 1:
        raise RuntimeError("V18_PARTIAL_INIT_SERIAL_ONLY_GATE=FAIL")

    before = checkpoint_state(outdir, seed) if action == "resume" else None
    if action == "resume" and not before["resumable"]:
        raise RuntimeError("PRE_RESUME_CHECKPOINT_GATE=FAIL " + json.dumps(before, sort_keys=True))

    cmd = [
        sys.executable, str(Path(__file__).resolve()), "polychord-worker",
        *common_cli(a),
        "--arm", a.arm, "--model", a.model, "--combination", a.combination,
        "--action", action, "--output-dir", str(outdir),
        "--result-json", str(outdir / "worker_result.json"),
    ]

    start = time.time()
    proc = subprocess.Popen(cmd, start_new_session=True)
    timed_out = False
    try:
        rc = proc.wait(timeout=int(a.soft_minutes) * 60)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(proc.pid, signal.SIGINT)
        try:
            rc = proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                rc = proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                rc = proc.wait()

    time.sleep(2)
    after = checkpoint_state(outdir, seed)
    worker = read_json(outdir / "worker_result.json") if (outdir / "worker_result.json").exists() else None

    resume_lifecycle_ok = True
    if action == "resume":
        lc = after.get("lifecycle") or {}
        resume_lifecycle_ok = (
            lc.get("action") == "resume"
            and lc.get("resume_input_source") == "COBAYA_STORED_UPDATED_INFO"
            and int(lc.get("seed", -1)) == seed
            and (
                (before or {}).get("checkpoint_kind") != "PARTIAL_INIT"
                or lc.get("cobaya_partial_resume_adapter_installed") is True
            )
        )

    checkpoint_progress = True
    checkpoint_progress_reason = "FRESH_OR_COMPLETE"
    if action == "resume" and before and before.get("resumable") and after.get("resumable"):
        bk = before.get("checkpoint_kind")
        ak = after.get("checkpoint_kind")
        if bk == "PARTIAL_INIT" and ak == "PARTIAL_INIT":
            bacc = before.get("partial_init_accepted")
            aacc = after.get("partial_init_accepted")
            checkpoint_progress = (
                isinstance(bacc, int) and isinstance(aacc, int) and aacc > bacc
            )
            checkpoint_progress_reason = f"PARTIAL_ACCEPTED_{bacc}_TO_{aacc}"
        elif bk == "PARTIAL_INIT" and ak == "STOCK_RESUME":
            # Crossing the GenerateLivePoints boundary into the stock PolyChord resume
            # is itself strict forward progress.
            checkpoint_progress = True
            checkpoint_progress_reason = "PARTIAL_TO_STOCK_RESUME"
        elif bk == "STOCK_RESUME" and ak == "STOCK_RESUME":
            checkpoint_progress = (
                before.get("primary_resume_sha256") != after.get("primary_resume_sha256")
                or before.get("primary_resume_mtime_ns") != after.get("primary_resume_mtime_ns")
            )
            checkpoint_progress_reason = "STOCK_RESUME_CHANGED" if checkpoint_progress else "STOCK_RESUME_UNCHANGED"
        else:
            checkpoint_progress = False
            checkpoint_progress_reason = f"INVALID_CHECKPOINT_TRANSITION_{bk}_TO_{ak}"

    if rc == 0 and worker and worker.get("status") == "COMPLETE":
        status = "COMPLETE"
    elif (
        a.resume_probe and action == "resume" and timed_out
        and after["resumable"] and resume_lifecycle_ok and checkpoint_progress
    ):
        status = "RESUME_PROBE_PASS"
    elif (
        a.resume_probe and action == "resume" and timed_out
        and after["resumable"] and resume_lifecycle_ok and not checkpoint_progress
    ):
        status = "RESUME_PROBE_NO_PROGRESS"
    elif timed_out and action == "fresh" and after["resumable"]:
        status = "SEGMENT_CHECKPOINTED"
    elif timed_out and action == "fresh" and not after["resumable"]:
        status = "SOFT_STOP_BEFORE_RESUMABLE_CHECKPOINT"
    elif timed_out and action == "resume" and after["resumable"] and resume_lifecycle_ok and checkpoint_progress:
        status = "SEGMENT_CHECKPOINTED"
    elif timed_out and action == "resume" and after["resumable"] and resume_lifecycle_ok and not checkpoint_progress:
        status = "RESUME_NO_CHECKPOINT_PROGRESS"
    elif action == "resume" and not resume_lifecycle_ok:
        status = "RESUME_PROCESS_GATE_FAILED"
    else:
        status = "FAILED"

    rec = {
        "q": Q,
        "case_id": CASE_ID,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "POLYCHORD_PRODUCTION_SEGMENT_V18",
        "status": status,
        "arm": a.arm,
        "model": a.model,
        "combination": a.combination,
        "segment": a.segment,
        "action": action,
        "seed": seed,
        "soft_minutes": a.soft_minutes,
        "mpi_ranks": mpi_ranks,
        "execution_mode": "SERIAL_PARTIAL_INIT_CHECKPOINT_V18",
        "elapsed_seconds": time.time() - start,
        "worker_returncode": rc,
        "timed_out": timed_out,
        "resume_probe": bool(a.resume_probe),
        "checkpoint_before": before,
        "checkpoint_after": after,
        "resume_lifecycle_ok": resume_lifecycle_ok,
        "checkpoint_progress": checkpoint_progress,
        "checkpoint_progress_reason": checkpoint_progress_reason,
        "worker": worker,
        "checkpoint_parent_run_id": a.parent_run_id or None,
        "scientific_spec_origin_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
        "scientific_spec_sha256": sha256_file(a.spec),
        "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
        "config_hash": canonical_hash({
            "spec": sha256_file(a.spec),
            "arm": a.arm,
            "model": a.model,
            "combination": a.combination,
            "seed": seed,
        }),
    }

    failures = {
        "SOFT_STOP_BEFORE_RESUMABLE_CHECKPOINT": "POLYCHORD_INITIAL_LIVE_POINT_CHECKPOINT_NOT_YET_AVAILABLE",
        "RESUME_NO_CHECKPOINT_PROGRESS": "POLYCHORD_RESUME_SEGMENT_NO_CHECKPOINT_PROGRESS",
        "RESUME_PROBE_NO_PROGRESS": "POLYCHORD_PARTIAL_INIT_RESUME_PROBE_NO_PROGRESS",
        "RESUME_PROCESS_GATE_FAILED": "CHECKPOINT_RESUME_VALIDATION_FAILURE",
        "FAILED": "HOSTED_RUNNER_OR_NUMERICAL_SEGMENT_FAILURE",
    }
    if status in failures:
        rec["failure_class"] = failures[status]

    write_json(a.segment_json, rec)
    print("Q042_PROD_V18_SEGMENT_STATUS=" + status)
    return 0 if status in ("COMPLETE", "SEGMENT_CHECKPOINTED", "RESUME_PROBE_PASS") else 2

def expected_bobyqa_artifact_names():
    out = []
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                for s in range(4):
                    out.append(
                        f"q042-prod-{V1_ROOT_RUN_ID}-bobyqa-{arm}-{model}-{combo}-s{s}"
                    )
    return out


def parse_artifact_identity(name):
    prefix = f"q042-prod-{V1_ROOT_RUN_ID}-bobyqa-"
    if not name.startswith(prefix):
        raise RuntimeError(f"BOBYQA_ARTIFACT_NAME_GATE=FAIL name={name}")
    tail = name[len(prefix):]
    for arm in ARMS:
        ap = arm + "-"
        if tail.startswith(ap):
            tail2 = tail[len(ap):]
            for model in MODELS:
                mp = model + "-"
                if tail2.startswith(mp):
                    rest = tail2[len(mp):]
                    for combo in COMBINATIONS:
                        cp = combo + "-s"
                        if rest.startswith(cp):
                            return arm, model, combo, int(rest[len(cp):])
    raise RuntimeError(f"BOBYQA_ARTIFACT_PARSE_GATE=FAIL name={name}")


def import_bobyqa(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    manifest = read_json(a.artifact_manifest)

    if int(manifest.get("source_root_run_id", -1)) != V1_ROOT_RUN_ID:
        raise RuntimeError("BOBYQA_IMPORT_ROOT_RUN_GATE=FAIL")
    if manifest.get("source_head_sha") != V1_EXECUTION_COMMIT:
        raise RuntimeError("BOBYQA_IMPORT_HEAD_SHA_GATE=FAIL")

    entries = manifest.get("artifacts")
    if not isinstance(entries, list):
        raise RuntimeError("BOBYQA_IMPORT_MANIFEST_GATE=FAIL")
    by_name = {x.get("name"): x for x in entries if isinstance(x, dict)}
    expected = expected_bobyqa_artifact_names()
    if set(by_name) != set(expected) or len(entries) != 80:
        raise RuntimeError("BOBYQA_IMPORT_ARTIFACT_SET_GATE=FAIL")

    source_root = Path(a.input_dir)
    output_root = Path(a.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    imported = []
    eligible = 0
    failed = 0

    for name in expected:
        arm, model, combo, s = parse_artifact_identity(name)
        entry = by_name[name]
        if entry.get("head_sha") != V1_EXECUTION_COMMIT:
            raise RuntimeError(f"BOBYQA_IMPORT_ARTIFACT_HEAD_GATE=FAIL name={name}")
        if not str(entry.get("digest", "")).startswith("sha256:"):
            raise RuntimeError(f"BOBYQA_IMPORT_DIGEST_GATE=FAIL name={name}")

        source_dir = source_root / name
        matches = list(source_dir.rglob("q042_production_bobyqa_start_v1.json"))
        if len(matches) != 1:
            raise RuntimeError(
                f"BOBYQA_IMPORT_RECORD_FILE_GATE=FAIL name={name} count={len(matches)}"
            )
        raw_path = matches[0]
        raw = read_json(raw_path)
        raw_hash = sha256_file(raw_path)

        if (
            raw.get("q") != Q
            or raw.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID
            or raw.get("run_id") != SCIENTIFIC_RUN_ID
            or raw.get("result_id") != SCIENTIFIC_RESULT_ID
        ):
            raise RuntimeError(f"BOBYQA_IMPORT_RECORD_IDENTITY_GATE=FAIL name={name}")
        if (
            raw.get("arm"),
            raw.get("model"),
            raw.get("combination"),
            int(raw.get("start_index", -1)),
        ) != (arm, model, combo, s):
            raise RuntimeError(f"BOBYQA_IMPORT_CELL_GATE=FAIL name={name}")

        expected_seed = cell_seed(spec, arm, model, combo) + 1000 + s
        if int(raw.get("seed", -1)) != expected_seed:
            raise RuntimeError(f"BOBYQA_IMPORT_SEED_GATE=FAIL name={name}")
        if float(raw.get("rhoend", -1)) != 0.05:
            raise RuntimeError(f"BOBYQA_IMPORT_RHOEND_GATE=FAIL name={name}")

        adapted = copy.deepcopy(raw)
        adapted.update(
            {
                "program_id": PROGRAM_ID,
                "run_id": RUN_ID,
                "result_id": RESULT_ID,
                "stage": "BOBYQA_IMPORTED_V1_RESULT_V13",
                "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
                "computed_by_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
                "computed_by_run_id": SCIENTIFIC_RUN_ID,
                "computed_by_result_id": SCIENTIFIC_RESULT_ID,
                "reused_by_program_id": PROGRAM_ID,
                "source_root_run_id": V1_ROOT_RUN_ID,
                "source_execution_commit": V1_EXECUTION_COMMIT,
                "source_artifact_id": int(entry["id"]),
                "source_artifact_name": name,
                "source_artifact_digest": entry["digest"],
                "source_record_sha256": raw_hash,
                "scientific_spec_sha256": sha256_file(a.spec),
            }
        )

        dest = output_root / name
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / "q042_production_bobyqa_start_v13.json"
        write_json(out, adapted)

        ok = bool(
            raw.get("technical_ok")
            and finite(raw.get("objective"))
            and int(raw.get("flag", -999)) >= 0
        )
        eligible += int(ok)
        failed += int(not ok)
        imported.append(
            {
                "artifact_id": int(entry["id"]),
                "artifact_name": name,
                "artifact_digest": entry["digest"],
                "arm": arm,
                "model": model,
                "combination": combo,
                "start_index": s,
                "seed": expected_seed,
                "technical_ok": ok,
                "source_record_sha256": raw_hash,
            }
        )

    if len(imported) != 80 or eligible != 78 or failed != 2:
        raise RuntimeError(
            f"BOBYQA_IMPORT_INGESTION_IDENTITY_GATE=FAIL total={len(imported)} "
            f"eligible={eligible} failed={failed}"
        )

    # All four starts must remain present for each cell and at least one must be eligible.
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                rows = [
                    r
                    for r in imported
                    if (r["arm"], r["model"], r["combination"])
                    == (arm, model, combo)
                ]
                if len(rows) != 4 or not any(r["technical_ok"] for r in rows):
                    raise RuntimeError(
                        f"BOBYQA_IMPORT_CELL_COMPLETENESS_GATE=FAIL {arm}:{model}:{combo}"
                    )

    write_json(
        a.summary,
        {
            "q": Q,
            "case_id": CASE_ID,
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "BOBYQA_V1_IMPORT_V13",
            "status": "PASS",
            "source_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "source_root_run_id": V1_ROOT_RUN_ID,
            "source_execution_commit": V1_EXECUTION_COMMIT,
            "imported_record_count": len(imported),
            "eligible_record_count": eligible,
            "preserved_failure_count": failed,
            "all_20_cells_have_four_starts": True,
            "all_20_cells_have_eligible_candidate": True,
            "records": imported,
        },
    )
    print("Q042_PROD_V13_BOBYQA_IMPORT_GATE=PASS")
    return 0


def merge_final(a):
    load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    root = Path(a.input_dir)

    # V1 contains the frozen scientific merge/classification implementation.
    # Create short-lived compatibility filenames next to V4 records so the
    # inherited merge code can read them without changing any science logic.
    shadows = []
    try:
        for p in root.rglob("q042_production_polychord_final_v13.json"):
            q = p.with_name("q042_production_polychord_final_v1.json")
            if q.exists():
                raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
            shutil.copy2(p, q)
            shadows.append(q)
        for p in root.rglob("q042_production_bobyqa_start_v13.json"):
            q = p.with_name("q042_production_bobyqa_start_v1.json")
            if q.exists():
                raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
            shutil.copy2(p, q)
            shadows.append(q)

        if len(list(root.rglob("q042_production_polychord_final_v13.json"))) != 20:
            raise RuntimeError("V13_POLYCHORD_FINAL_COUNT_GATE=FAIL")
        if len(list(root.rglob("q042_production_bobyqa_start_v13.json"))) != 80:
            raise RuntimeError("V13_BOBYQA_IMPORT_COUNT_GATE=FAIL")

        rc = v1.merge_final(a)
    finally:
        for p in shadows:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    out = read_json(a.output)
    out.update(
        {
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "PRODUCTION_FINAL_V13",
            "scientific_spec_origin_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "scientific_spec_sha256": sha256_file(a.spec),
            "technical_parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "technical_parent_root_run_id": V1_ROOT_RUN_ID,
            "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
            "technical_repair": "POLYCHORD_METADATA_SEPARATED_FROM_EXECUTABLE_COBAYA_OPTIONS",
            "bobyqa_reuse": {
                "source_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
                "source_root_run_id": V1_ROOT_RUN_ID,
                "reused_record_count": 80,
                "recomputed_in_recovery": 0,
                "preserved_failures": 2,
            },
        }
    )
    out.setdefault("gates", {})["V1_SCIENTIFIC_SPEC_BYTE_IDENTITY"] = "PASS"
    out["gates"]["V1_BOBYQA_PROVENANCE_REUSE"] = "PASS"
    out["gates"]["POLYCHORD_V13_METADATA_ADAPTER"] = "PASS"
    write_json(a.output, out)
    print("Q042_PROD_V13_FINAL_GATE=" + str(out.get("final_result_gate")))
    return rc



def adopt_parent_reduced_environment(a):
    """Adopt the validated V1 reduced matrix byte-for-byte with V8 execution provenance."""
    import numpy as np

    parent_support = read_json(a.parent_support)
    parent_meta = read_json(a.parent_meta)

    if parent_support.get("q") != Q or parent_support.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID:
        raise RuntimeError("PARENT_REDUCED_SUPPORT_IDENTITY_GATE=FAIL")
    if parent_meta.get("q") != Q or parent_meta.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID:
        raise RuntimeError("PARENT_REDUCED_META_IDENTITY_GATE=FAIL")
    if parent_meta.get("stage") != "Q041_HILLIPOP_PRIMARY_NONOVERLAP_PRECISION":
        raise RuntimeError("PARENT_REDUCED_META_STAGE_GATE=FAIL")
    if parent_meta.get("status") != "PASS":
        raise RuntimeError("PARENT_REDUCED_META_STATUS_GATE=FAIL")
    if parent_meta.get("support_sha256") != parent_support.get("support_sha256"):
        raise RuntimeError("PARENT_REDUCED_SUPPORT_LINK_GATE=FAIL")

    parent_matrix = Path(a.parent_matrix)
    if sha256_file(parent_matrix) != parent_meta.get("matrix_file_sha256"):
        raise RuntimeError("PARENT_REDUCED_MATRIX_FILE_HASH_GATE=FAIL")

    q32 = v1.core.legacy.load_q032(a.q032_parent_root)
    P = np.load(parent_matrix, allow_pickle=False)
    if q32.sha256_array(P) != parent_meta.get("restricted_precision_sha256"):
        raise RuntimeError("PARENT_REDUCED_MATRIX_ARRAY_HASH_GATE=FAIL")

    current_matrix = Path(a.current_matrix)
    current_matrix.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(parent_matrix, current_matrix)

    if sha256_file(current_matrix) != sha256_file(parent_matrix):
        raise RuntimeError("BYTE_IDENTICAL_REDUCED_MATRIX_COPY_GATE=FAIL")
    P2 = np.load(current_matrix, allow_pickle=False)
    if q32.sha256_array(P2) != parent_meta.get("restricted_precision_sha256"):
        raise RuntimeError("ADOPTED_REDUCED_MATRIX_ARRAY_HASH_GATE=FAIL")

    support = copy.deepcopy(parent_support)
    support.update({
        "q": Q,
        "case_id": CASE_ID,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "Q041_PRIMARY_NONOVERLAP_SUPPORT",
        "status": "PASS",
        "adoption_mode": "BYTE_IDENTICAL_V1_PARENT_REUSE",
        "parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
        "parent_support_file_sha256": sha256_file(a.parent_support),
    })

    meta = copy.deepcopy(parent_meta)
    meta.update({
        "q": Q,
        "case_id": CASE_ID,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "Q041_HILLIPOP_PRIMARY_NONOVERLAP_PRECISION",
        "status": "PASS",
        "matrix_file": current_matrix.name,
        "matrix_file_sha256": sha256_file(current_matrix),
        "adoption_mode": "BYTE_IDENTICAL_V1_PARENT_REUSE",
        "parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
        "parent_matrix_file_sha256": sha256_file(parent_matrix),
        "parent_meta_file_sha256": sha256_file(a.parent_meta),
        "scientific_numeric_recomputation": False,
    })

    write_json(a.current_support, support)
    write_json(a.current_meta, meta)
    write_json(a.output, {
        "q": Q,
        "case_id": CASE_ID,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "REDUCED_ENVIRONMENT_PARENT_ADOPTION_V13",
        "status": "PASS",
        "scientific_result": False,
        "parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
        "matrix_recomputed": False,
        "matrix_byte_identical_to_parent": True,
        "support_sha256": support["support_sha256"],
        "restricted_precision_sha256": meta["restricted_precision_sha256"],
        "matrix_file_sha256": meta["matrix_file_sha256"],
        "gates": {
            "PARENT_IDENTITY": "PASS",
            "PARENT_FILE_HASH": "PASS",
            "PARENT_ARRAY_HASH": "PASS",
            "BYTE_IDENTICAL_COPY": "PASS",
            "ACTIVE_PROVENANCE_RESTAMP": "PASS",
        },
    })
    print("Q042_PROD_V13_PARENT_REDUCED_ENVIRONMENT_ADOPTION_GATE=PASS")
    return 0

def common_args(s):
    for x in (
        "q032-parent-root",
        "preflight",
        "parent-dir",
        "hlp-matrix",
        "hlp-meta",
        "reduced-support",
        "reduced-hlp-matrix",
        "reduced-hlp-meta",
        "spec",
        "source-lock",
        "external-runtime",
    ):
        s.add_argument("--" + x, required=True)


def parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("static")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=static_check)

    s = sp.add_parser("sampler-adapter-regression")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--external-runtime", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=sampler_adapter_regression)

    s = sp.add_parser("prepare-nonoverlap")
    for x in (
        "q032-parent-root",
        "preflight",
        "hlp-matrix",
        "hlp-meta",
        "support-output",
        "matrix-output",
        "meta-output",
    ):
        s.add_argument("--" + x, required=True)
    s.set_defaults(func=prepare_nonoverlap)

    s = sp.add_parser("runtime-preflight")
    common_args(s)
    s.add_argument("--output", required=True)
    s.set_defaults(func=runtime_preflight)

    s = sp.add_parser("adopt-parent-reduced-environment")
    for x in ("parent-support","parent-matrix","parent-meta","current-support","current-matrix","current-meta","q032-parent-root","output"):
        s.add_argument("--" + x, required=True)
    s.set_defaults(func=adopt_parent_reduced_environment)

    s = sp.add_parser("polychord-worker")
    common_args(s)
    s.add_argument("--arm", choices=ARMS, required=True)
    s.add_argument("--model", choices=MODELS, required=True)
    s.add_argument("--combination", choices=COMBINATIONS, required=True)
    s.add_argument("--action", choices=("fresh", "resume"), required=True)
    s.add_argument("--output-dir", required=True)
    s.add_argument("--result-json", required=True)
    s.set_defaults(func=polychord_worker)

    s = sp.add_parser("polychord-segment")
    common_args(s)
    s.add_argument("--arm", choices=ARMS, required=True)
    s.add_argument("--model", choices=MODELS, required=True)
    s.add_argument("--combination", choices=COMBINATIONS, required=True)
    s.add_argument("--segment", type=int, required=True)
    s.add_argument("--soft-minutes", type=int, default=240)
    s.add_argument("--mpi-ranks", type=int, default=1)
    s.add_argument("--parent-run-id", default="")
    s.add_argument("--resume-probe", action="store_true")
    s.add_argument("--output-dir", required=True)
    s.add_argument("--segment-json", required=True)
    s.set_defaults(func=polychord_segment)

    s = sp.add_parser("import-bobyqa")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--artifact-manifest", required=True)
    s.add_argument("--output-dir", required=True)
    s.add_argument("--summary", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.set_defaults(func=import_bobyqa)

    s = sp.add_parser("merge-final")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=merge_final)

    return p


freeze_v1_globals()
v1.load_spec = load_spec
v1.load_lock = load_lock
v1.runtime_gate = runtime_gate
v1.cell_seed = cell_seed
v1.production_pc = production_pc

if __name__ == "__main__":
    a = parser().parse_args()
    raise SystemExit(a.func(a))
```


## APPENDIX G3 — RETRIEVED V18 PARTIAL-INIT DETECTION ADAPTER

**Preserved UTF-8 source SHA-256:** `b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567`; bytes: 5649.

```python
#!/usr/bin/env python3
"""Q042-PROD-V18 Cobaya 3.5.6 partial-init resume adapter.

Cobaya's PolyChord wrapper recognizes only <prefix>.resume as the minimal
resume marker. Q042's pre-stock GenerateLivePoints state lives in
<prefix>.partial_init, so Cobaya 3.5.6 otherwise logs "Did not find an old
sample. Cleaning up and starting anew." and deletes the raw PolyChord folder
before patched PolyChord can read the partial checkpoint.

This adapter changes only Cobaya's *resume-file detection* for PolyChord:
when minimal resume detection is requested, an existing .partial_init file is
also accepted as evidence of a resumable run. Normal output deletion patterns,
PolyChord settings, likelihoods, priors, seeds, checkpoint bytes and sampling
logic are not modified.
"""
from __future__ import annotations
import argparse, json, re, shutil, tempfile
from pathlib import Path

MARKER = "Q042_COBAYA_PARTIAL_RESUME_ADAPTER_V18"


def install_partial_init_resume_detection():
    from cobaya.samplers.polychord.polychord import polychord
    if getattr(polychord, "_q042_partial_resume_adapter_v18", False):
        return False
    original = polychord.output_files_regexps

    def patched(cls, output, info=None, minimal=False):
        entries = list(original(output, info=info, minimal=minimal))
        if minimal:
            entries.append((
                re.compile(re.escape(output.prefix + ".partial_init")),
                cls.get_base_dir(output),
            ))
        return entries

    polychord.output_files_regexps = classmethod(patched)
    polychord._q042_partial_resume_adapter_v18 = True
    polychord._q042_partial_resume_adapter_v18_marker = MARKER
    return True


def _fixture(root: Path):
    from cobaya.output import Output
    from cobaya.samplers.polychord.polychord import polychord
    root.mkdir(parents=True, exist_ok=True)
    prefix = root / "chain"
    # Output only needs the updated-info file to know resume was requested for an
    # existing run; check_force_resume performs the sampler-file detection next.
    Path(str(prefix) + ".updated.yaml").write_text("sampler: {}\n", encoding="utf-8")
    output = Output(str(prefix), resume=True, force=False)
    raw = Path(polychord.get_base_dir(output))
    raw.mkdir(parents=True, exist_ok=True)
    partial = raw / (output.prefix + ".partial_init")
    partial.write_bytes(b"Q042-V18-PARTIAL-RESUME-ADAPTER-SELFTEST")
    return output, partial


def selftest(output_path: str):
    import cobaya
    from cobaya.samplers.polychord.polychord import polychord

    if getattr(cobaya, "__version__", None) != "3.5.6":
        raise SystemExit(f"COBAYA_PARTIAL_RESUME_ADAPTER_VERSION_GATE=FAIL got={getattr(cobaya,'__version__',None)}")

    root = Path(tempfile.mkdtemp(prefix="q042_v18_cobaya_resume_"))
    try:
        # Reproduce the V17 failure with unmodified Cobaya detection.
        base_out, base_partial = _fixture(root / "baseline")
        if not base_out.is_resuming():
            raise SystemExit("COBAYA_PARTIAL_RESUME_BASELINE_PRECONDITION_GATE=FAIL")
        polychord.check_force_resume(base_out, info={})
        baseline_cleanup_observed = (not base_out.is_resuming()) and (not base_partial.exists())
        if not baseline_cleanup_observed:
            raise SystemExit("COBAYA_PARTIAL_RESUME_BASELINE_CLEANUP_GATE=FAIL")

        installed = install_partial_init_resume_detection()
        adapted_out, adapted_partial = _fixture(root / "adapted")
        polychord.check_force_resume(adapted_out, info={})
        adapted_resuming = bool(adapted_out.is_resuming())
        adapted_preserved = adapted_partial.is_file() and adapted_partial.stat().st_size > 0
        if not (adapted_resuming and adapted_preserved):
            raise SystemExit("COBAYA_PARTIAL_RESUME_ADAPTER_PRESERVATION_GATE=FAIL")

        patterns = polychord.output_files_regexps(adapted_out, info={}, minimal=True)
        partial_pattern_present = any(
            getattr(rx, "pattern", "").endswith(re.escape(adapted_out.prefix + ".partial_init"))
            for rx, _ in patterns
        )
        if not partial_pattern_present:
            raise SystemExit("COBAYA_PARTIAL_RESUME_ADAPTER_PATTERN_GATE=FAIL")

        record={
            "q":"Q-042",
            "program_id":"Q042-PROD-V18",
            "stage":"COBAYA_PARTIAL_INIT_RESUME_ADAPTER_SELFTEST_V18",
            "status":"PASS",
            "scientific_result":False,
            "scientific_contract_changed":False,
            "cobaya_version":"3.5.6",
            "marker":MARKER,
            "adapter_installed_now":bool(installed),
            "baseline_cleanup_observed":True,
            "adapted_resuming":True,
            "adapted_partial_checkpoint_preserved":True,
            "normal_output_deletion_patterns_changed":False,
            "minimal_resume_detection_addition":"<prefix>.partial_init",
        }
        p=Path(output_path); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("Q042_COBAYA_PARTIAL_RESUME_ADAPTER_SELFTEST_V18=PASS")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--output")
    a=ap.parse_args()
    if a.selftest:
        if not a.output: raise SystemExit("--output required with --selftest")
        return selftest(a.output)
    install_partial_init_resume_detection()
    print("Q042_COBAYA_PARTIAL_RESUME_ADAPTER_V18=INSTALLED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
```


# APPENDIX H — PRESERVATION MANIFEST

```json
[
  {
    "title": "Appendix A",
    "source_local_name": "Q042_PROD_V1_INGESTION_HANDOFF.md",
    "size_bytes": 167050,
    "sha256": "3f608302a625abafd28d9ada487ee4a2c17681717be62e8e84d97af574a993c4"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_production_final_v19.json",
    "size_bytes": 287166,
    "sha256": "95f024b5ffdde740ae796e54a7dbd02340c14f340b7ea935b70082e0ea607e07"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_production_artifact_index_v19.json",
    "size_bytes": 488,
    "sha256": "202fa0d4e2295f0aa2f10e370f46c9bb15e9a0ee33d870b8bc841ba9bda01f96"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_v18_artifact_selection_v19.json",
    "size_bytes": 7379,
    "sha256": "0967a7ed9203d36d8ae7e11dd77a2ca0679c1de83d7118f5d19a60e7c751cc0f"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_prod_static_v19.json",
    "size_bytes": 752,
    "sha256": "37312818a6bc8cf3f638d8a35f123bc9ec27394b2b858a911adf27f292ffd55b"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_prod_static_tests_v19.json",
    "size_bytes": 1294,
    "sha256": "04a496b8db06b8a4a49f534c583a09e7d5c2da000d48e0764a67e327986d0f6b"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_production_spec_v1.json",
    "size_bytes": 9024,
    "sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_production_recovery_v19.json",
    "size_bytes": 2389,
    "sha256": "d9d82270f44b26b0e46ea0a181704ebf97629c1f213c4def2b9893ac97a84d4b"
  },
  {
    "title": "Appendix B",
    "source_local_name": "q042_production_source_lock_v19.json",
    "size_bytes": 2662,
    "sha256": "b5367385fd96ccd07db17dcd74f6bbd5a14e1f4c4cc7783abea4554eee02fa3b"
  },
  {
    "title": "APPENDIX C \u2014 COMPLETE RETRIEVED V18 TECHNICAL-HISTORY SOURCE LOCK",
    "source_local_name": "q042_production_source_lock_v18.json",
    "size_bytes": 12997,
    "sha256": "6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde"
  },
  {
    "title": "APPENDIX D1 \u2014 RETRIEVED V19 MERGE RUN METADATA",
    "source_local_name": "merge_run_metadata.json",
    "size_bytes": 13803,
    "sha256": "22a6c753863fc4989789cdd517486b57de74e1b10b1ba681b823c354b3951069"
  },
  {
    "title": "APPENDIX D2 \u2014 RETRIEVED V19 FINAL ARTIFACT METADATA",
    "source_local_name": "merge_artifact_metadata.json",
    "size_bytes": 831,
    "sha256": "4f13f9d5a2170fb53338ad3d0a1e6615a50d0d6e5d661c403bd3efddf99f195e"
  },
  {
    "title": "APPENDIX E1 \u2014 RAW CAMSPEC EDE FULL TERMINAL JOB LOG",
    "source_local_name": "camspec_ede_FULL_terminal.log",
    "size_bytes": 132935,
    "sha256": "4b8cd3349616f0c251147fb80a6d1b49f514291fc9e9d80470558d0056493ad5"
  },
  {
    "title": "APPENDIX E2 \u2014 RAW CAMSPEC LCDM FULL TERMINAL JOB LOG",
    "source_local_name": "camspec_lcdm_FULL_terminal.log",
    "size_bytes": 134032,
    "sha256": "2d40de0b817d02372ee5ebfcc7ba044fcbba256787de0c096ec1b92560e1c0c3"
  },
  {
    "title": "APPENDIX F1 \u2014 DETERMINISTIC INGESTION AUDIT SOURCE",
    "source_local_name": "audit_v19_ingestion.py",
    "size_bytes": 7245,
    "sha256": "b57071f9d9362bd5acb63709e1570ef1941e6d5772b12e0a769ed9dae8a67e30"
  },
  {
    "title": "APPENDIX F2 \u2014 INGESTION AUDIT OUTPUT",
    "source_local_name": "v19_ingestion_audit.json",
    "size_bytes": 3535,
    "sha256": "decc4551f34c2c10ad361e547e7e37d97558d297eda1482f113129256764925b"
  },
  {
    "title": "APPENDIX G1 \u2014 RETRIEVED V19 MERGE-ONLY PROGRAM",
    "source_local_name": "q042_production_v19.py",
    "size_bytes": 12353,
    "sha256": "8f8d5688169bb7f27b6f4d0a88ea2d1c53d927a8c008145d8eeeaea1bc89080b"
  },
  {
    "title": "APPENDIX G2 \u2014 PINNED V18 PRODUCTION PROGRAM",
    "source_local_name": "q042_production_v18_pinned.py",
    "size_bytes": 49387,
    "sha256": "19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962"
  },
  {
    "title": "APPENDIX G3 \u2014 RETRIEVED V18 PARTIAL-INIT DETECTION ADAPTER",
    "source_local_name": "q042_cobaya_partial_resume_adapter_v18.py",
    "size_bytes": 5649,
    "sha256": "b547b2dfd75f29015e7b0e08dfe4214d8889fb911a32060e48d30283e419a567"
  }
]
```
