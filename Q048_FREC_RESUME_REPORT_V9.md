# Q048 — Builder V9: ny frec-celle accepteret

**Resultat:** Hillipop-EDE z1490→1480 er nu accepteret for både L(q=10⁻⁶) og R(q=0). Den bevarede kæde er vokset fra **59 til 60 celler**. Næste celle z1480→1470 stopper på en ny, præcist beregnet utilstrækkelig guard-grænse. **Q048 er fortsat uafklaret.**

## Opgave og bevaret tilstand

TASK_TYPE SCIENTIFIC_CASE_EXECUTION. CURRENT_Q/TARGET_Q Q048/Q048. Revision GUARD_V8_INGESTED_V1_BUILDER_V9. Builder-prompt 2.2.0, SHA256 `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`.

Den præcise videnskabelige opgave er:

> For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Spørgsmålshash `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`. Source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`; capture SHA256 `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`. Alle fire konfigurationer, accepteret z_reio, fælles første event og begge jump-map-familier er bevaret. Q047 forbliver CLOSED INCONCLUSIVE. Q048's registrerede PROPOSED_UNVERIFIED og CASE NOT_ASSIGNED ændres ikke.

Hele den indsendte journal er hashkontrolleret og bevaret som eksakt byteprefix i den leverede efterfølger. De relevante slutafsnit og lineage er læst; hele historikken på 138.935 linjer er ikke semantisk genlæst. Builder-prompten og alle fire korte ledsagefiler er læst. Appendmarkøren for V9 forekommer præcis én gang.

## Udførelse og genbrug

Mekanisme: MODIFIED_MOTOR / CONVENTIONAL_PROGRAM — en afgrænset V9-tilpasning af eksisterende V7-kode, med uændrede atomare/source- og invariantprimitiver. Ingen ny motorarkitektur. PROGRAM_ID Q048-FREC-RESUME-V9 er kontrolleret ubrugt i det læste register, men er **LOCAL_UNREGISTERED**.

GitHub-hukommelse er læst i `Morfindien/Bubbleverse`, main `7aff72a6c09a2a8891b11b255ba198a8e0d832be`. Gren, komplet træ, relevante V7/V8-filer, register og README er inspiceret. Ingen AGENTS.md blev fundet i træet. V7 raw/checkpoint/validering og V8 raw/validering matcher de dokumenterede SHA256. 31 ældre afhængigheder er genfundet i deres præcist identificerede filversioner og hashkontrolleret; manglende filer blev ikke konstrueret ud fra prosa.

REUSE: 59 accepterede frec-celler, fire H→frec-tubes, V8-certifikat og eksisterende sourceprimitiver. PATCH: V7-producer/validator til versioneret V9-guardbinding og 59-cellers resume. CREATE: nye resultater, checks, journalappend og overlevering. UNCHANGED: historiske journaler, kilder, parametre, fejl og resultater. README/register er REFERENCE_ONLY, ikke ændret.

ACTUAL_RUNTIME: observeret lokal Python 3.12.14 på Linux-6.18.44-x86_64-with-glibc2.39; præcis Fraction- og udadrettet intervalaritmetik samt GitHub-læseadgang. Numerisk modelidentitet er ikke eksponeret; intet modelskift påstås. Anbefalet profil er grundig reasoning med kodeeksekvering og kilde-/hashkontrol. SWITCH_STATUS NOT_NEEDED. Fælles core og globalt valideringsschema er NOT_AVAILABLE; den eksplicitte lokale kontrakt bruges.

COMPUTE_BACKEND LOCAL_RUNTIME. GITHUB_WORTHWHILE NO; beslutningsgate PASS. 581 resterende faste celler ville kræve mindst to kørsler ved grænsen 512. Tidligere V7 målte 0,260 s plus 0,055 s validering. Et betinget 20–120 s skøn for resterende numerik/validering er usikkert og forudsætter ingen nye metode-/sourceblokeringer; forberedelse, hentning og aflevering er særskilt overhead. GitHub-kø/setup/operatørtid er ikke målt, intet V9-workflow er installeret, og ingen parallel fordel er dokumenteret. Ingen fuldhistorie-tid eller cloudpris opfindes. Den aktuelle lokale kørsel tog 0.220462168 s og valideringen 0.082467574 s. 300 s/512-cellers budget er overholdt; ingen betalt/native/HPC-kørsel.

## Faktiske værdier og deres betydning

| Størrelse | z1490→1480 | z1480→1470 |
|---|---:|---:|
| a-interval | [1/1491,1/1481] | [1/1481,1/1471] |
| E_upper, Mpc⁻² | 225,043660050541934326 | 221,188505238016493787 |
| Nyberegnet G_lower, Mpc⁻² (afrundet) | 0,2341710534968224 | −0,8875594112214912 |
| Anvendt target-margin, Mpc⁻² | 0,196966211731054556 | Ingen target-margin genbrugt |
| Paired celle | PASS | Ikke accepteret |

Første celle består de frosne domæne-, source-, positivitet-, hydrogen- og termiske facechecks for begge grene. V8-marginen bindes kun til den aftalte celle; den erstatter ikke en frisk celleberegning. Den præcise accepterede margin er minimum af V8-certifikatet og den nyberegnede margin.

På næste celle føres kun endpointenergien videre under den kvalificerede relation e_u=−3X²≤0. Frisk G=3B0_lower−E_forward_upper+floor_lower er negativ. Dette er **METHOD_INSUFFICIENT** for denne tilstrækkelige grænse. Det er ikke et bevis for en fysisk crossing eller falsifikation. Alle eksakte brøker, operands og bounds står i raw JSON; source-/termiske checks for den blokerede celle er ikke udført.

Frontiers efter kørslen: camspec-lcdm 1440; camspec-ede_n3 1440; hillipop-lcdm 1440; hillipop-ede_n3 1480. De fire oprindelige H→frec-tubes er uændrede. Ingen uafhængig initialtilstand er indført.

## Validering, begrænsninger og status

**82/82 kontroller PASS; 10/10 mutationer afvist; 3/3 fokuserede kontrakttests PASS.** Kontrakttesten viste først de manglende V8-bindinger, derefter PASS efter tilpasningen. Den særskilte validator importerer ikke produceren: den kontrollerer exact-hashlineage, kontinuitet, finite-node-backgroundgrænse, G-algebra, source-domæner, begge q-værdier, hydrogen-/termiske uligheder og overfortolkningsværn. Atomare kildeprimitiver og fysiske præmisser er fælles med den arvede validerede konstruktion; dette er ikke uafhængig fysisk evidens, en ny gennemgang af alle historiske beviser eller global formel schemavalidering.

EXECUTION_STATUS PARTIAL; RESULT_VALIDATION_STATUS VALIDATED inden for det nye finite komponentresultat; SCIENTIFIC_OUTCOME INCONCLUSIVE; CASE_LIFECYCLE OPEN. Bounded Builder TERMINATION_GATE PASS; hele Q048 FINAL_RESULT_GATE UNRESOLVED. Gate-register og begrundelser findes i machine-handoffet.

Der foreligger fortsat ingen komplette fire-case-historier til a=1/reio, endelige Δx_e(z)-grænser, observer-normaliserede kumulative Δτ_T(z)-grænser eller native P6-kvalifikation. Ingen modelpromovering, ny Q, fysisk bekræftelse eller sletning/omskrivning af tidligere resultater.

## Præcis overlevering

**Næste motor: Result Ingestion & Routing 2.1.0.** Den modtager V9 én gang og vælger den videre faglige rute. Det konkrete nye behov er et sammenhængende source-korreleret energy/phase/Y/background-certifikat på a=[1/1481,1/1471], videreført fra den eksakte V8-endpointfamilie. Det skal bevare de 60 accepterede celler og dokumentere streng G>0 eller en præcis ny hindring. Et uændret Builder-replay er ikke en løsning. Ingen direkte Motor14-dispatch er foretaget.

Alle no-repeat-forbud, arvede kilder/claimregistre og historiske negative resultater følger den komplette journal. Nye lokale claims V9-C01–C03 er knyttet til raw/validering i handoffet; de udgiver sig ikke for globalt registrerede IDs.

MEMORY_BACKEND GITHUB. MEMORY_READ_STATUS VERIFIED for de anførte repoobjekter; hele projektets aktuelle tilstand er ikke auditeret. MEMORY_WRITE_STATUS FILES_READY_FOR_MANUAL_UPLOAD. MEMORY_LINKS_UPDATED: foreslået ny journal-/V9-resultatpointer, ikke skrevet. Filerne skal indlæses efter den eksisterende workflowkonvention; filindekset og memory-update beskriver de eksakte foreslåede paths. Ingen remote commit/PR, registrering eller README-ændring påstås. START_STATUS NOT_READY for GitHub; lokal kørsel er allerede udført.

## Direkte projektkilder

- [V7-konstruktion](https://github.com/Morfindien/Bubbleverse/blob/7aff72a6c09a2a8891b11b255ba198a8e0d832be/q048_frec_resume_v7.py) — den genbrugte konstruktion.
- [V7-checkpoint](https://github.com/Morfindien/Bubbleverse/blob/7aff72a6c09a2a8891b11b255ba198a8e0d832be/q048_frec_resume_checkpoint_v7.json) — de 59 bevarede celler/frontiers.
- [V8-certifikat](https://github.com/Morfindien/Bubbleverse/blob/7aff72a6c09a2a8891b11b255ba198a8e0d832be/q048_guard_resume_result_v8.json) og [V8-validering](https://github.com/Morfindien/Bubbleverse/blob/7aff72a6c09a2a8891b11b255ba198a8e0d832be/q048_guard_resume_validation_v8.json) — target- og endpointbinding.
