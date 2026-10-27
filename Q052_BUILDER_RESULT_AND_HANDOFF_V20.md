# Q052 V20 — første betingede fejlrør er lukket

**Resultat: betinget første-celle PASS for begge helium-arme. Q052 som helhed er fortsat ACTIVE / INCONCLUSIVE.**

Tid for denne rapport: 2026-10-27T09:29:20.319518+00:00 UTC. Lokal tid: 2026-10-27T10:29:20.319518+01:00 (Europe/Copenhagen). Numerisk kørsel: 2026-10-27T09:15:58.484807+00:00 → 2026-10-27T09:16:10.882943+00:00. CASE: LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1. CURRENT_Q=TARGET_Q=Q052. Motor: Execution/HPC/Motor-builder2.4.0, leveret prompt SHA256 `5e97deb69af1e16192c5130820a484fa7839378f9d5ada7d682ae5700c01b47d`.

## Den afgrænsede afgørelse

Den nye lokale producent har beregnet hele den todimensionale direkte defekt d, en vægtet infinity-Jacobiangrænse L og den strenge Grönwall-lukning på første celle, z=810 til den eksakte binær64-knude `0x1.94d75c28f5c29p+9` (vist som809.6825). Der er64 rationelle underceller i x=-z, to arme og højst de to på forhånd tilladte radiepar. Der er ikke kørt en ny native integration.

| Radier (rho_h,rho_v) | Arm | d-bar, vist | L-bar, vist | Beregnet normaliseret loft, vist | Afgørelse |
|---|---|---:|---:|---:|---|
| (1e-5,1e-4) | L, q=1e-6 | 3638.204490 | 1453.184267 | 1.919110 | INCONCLUSIVE_METHOD_WIDTH |
| (1e-5,1e-4) | R, q=0 | 3637.302966 | 1452.833863 | 1.918491 | INCONCLUSIVE_METHOD_WIDTH |
| (2e-5,5e-4) | L, q=1e-6 | 1819.102245 | 1445.010059 | 0.957877 | PASS |
| (2e-5,5e-4) | R, q=0 | 1818.651483 | 1444.659602 | 0.957567 | PASS |

Tabellen er opad afrundet til visning. Receiptets hex-endpoints er autoritative. Acceptkravet er et **strengt loft under1** i normen W=diag(1/rho_h,1/rho_v). Første forsøg bevares som et mislykket metodeforsøg; det er hverken fysisk falsifikation eller et bevis for, at det mindre rør faktisk forlades. Andet radiepar var fastlagt i V19, og dets branche- og domænekrav blev kontrolleret særskilt.

For det accepterede andet forsøg giver de beregnede øvre grænser på hele cellen:

| Arm | abs(h−hhat) højst | abs(v−vhat) højst |
|---|---:|---:|
| L | 0.000019157524 | 0.000478938098 |
| R | 0.000019151340 | 0.000478783486 |

Her er v=Tm/Tgamma. Det er fejlgrænser for hver rekonstruktion mod dens betingede kilde-real mål, ikke en måling af L−R-forskellen, ikke temperaturfejl i kelvin og ikke de realiserede suprema for elektronfraktion eller optisk dybde. De positive intervaller i JSON-feltet `error_components_if_pass` omslutter **det beregnede loftsudtryk**; den faktiske absolutte fejl ligger mellem0 og det øvre endpoint. Samme skel gælder `bound_expression_interval`: det er ikke en positiv nedre grænse for den faktiske fejl.

## Præmisser og uændret hovedspørgsmål

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

V20 kvantificerer over hvert eksisterende fast admitted medlem af den arvede fælles baggrundsfamilie, med samme medlem i begge arme og gennem hele cellen. Den arvede betingede Q050-binding og Q051/V18 positive-escape-præmis (`1+DK>0`) bevares. Familiens ikke-tomhed og native baggrundsmedlemskab bevises ikke her.

E0=0 gælder alene for samme **eksakte fangede h/v-koordinatstart** i målet og rekonstruktionen. Starten er h0=4651594516923411/1152921504606846976, v0=9947469393499555215/9954668796147009946. Ingen ukendt pre810-nativefejl er sat til0. q evalueres ved præcis1/1000000 henholdsvis0; den fangede flydende heliumparameter er ikke substitueret for det eksakte mål.

## Beregning og kildeoverensstemmelse

Den uændrede scalar-I/MPFR-backend fra V18 er genbrugt; den gamle fysiske z≤50/reio-evaluator er ikke kaldt. Nye funktioner rekonstruerer h,D med eksakt rationel Bernstein-restriktion og bruger h_u=(1+z)h_x og v_u=D_x/Tcmb+v−1. Det aktive felt er h_u=f og v_u=−v+A(1−v). Hubblefeltet omregnes med c/Mpc til s⁻¹; HyRec-nH er i cm⁻³. H_prime er ikke et input til denne fase.

Alle 16000 Alpha_inf-tal og 100 R_inf-tal log-initialiseres med rettet MPFR-aritmetik. Kildens decimaltekst og dens binær64-inputkonvertering omsluttes. Log-grid, temperatur-grid, floor/clamp-stencils, kubisk interpolation, temperaturafledte, exp/pow og fysiske konstanter er omsluttet. Partition-of-unity-omskrivning af interpolationen fjerner et fælles log-rate-offset uden at ændre polynomiet. Dette er en evaluator for source-real initialisering; der påstås ikke korrekt afrundet historisk native libm. Den historiske beregnings virkning på den definerede gemte kurve håndteres gennem den direkte defekt, uden en duplikeret native-aritmetikpost.

Over den fulde celle og begge radiepar ligger h i(0,1), v i(0.1,1), TR i(0.004,0.4)eV, og Tgamma inden for SWIFT-fitdomænet. På andet radiepar er Pion≥0.20525052293869164>0.01; v≤0.9997767812978128<1. Alle evaluerede ratebokse bruger stencilen(iTR,iTM)=(83,37), med alle relevante lukkede stencilgrænser i koden. Ingen equality-regel er ændret.

C_s,C_p er omsluttet konservativt af[0,1] under den arvede positive-escape-præmis. De positive atomrater og den positive omskrevne C-denominator D0 verificeres numerisk på rørene. DK afhænger ikke af h eller v på denne gren, så den arvede positive-escape-præmis ændres ikke ved det andet radiepar; **der er ikke udledt et nyt numerisk DK-interval**. V18§5.3 giver abs(C_h)≤1/(4(1−h)) og C_v=0. De bruges til hele hydrogenrækken; de eksakte termiske afledte bruges til den anden række. L-bar er maksimum af begge vægtede rækkesummer, ikke kun en termisk komponent.

For hver undercelle evalueres defekten langs kurven og Jacobianloftet på det udvidede rør. Maksima over alle 64 underceller giver d-bar og L-bar for hele cellen. T=log(811/(1+z_lower)) er omsluttet af [0.0003915686381971496, 0.00039156863819737165]. Derefter evalueres E0 exp(L-bar T)+d-bar(exp(L-bar T)−1)/L-bar udadrettet. Streng lukning og V18's første-exit-argument giver de betingede fejlgrænser. d og L er dimensionløse normkonstanter per u; de er ikke observerede fysiske forskelle.

## Faktisk verifikation og begrænsninger

Producenten tog 12.398142 s i det aktuelle lokale miljø, inklusive input- og tabelinitialisering; den samlede analyse-/leveringstid er ikke målt.13 nye afsluttende tests bestod på 1.327 s. Der blev først kørt11 tests med én receipt-test markeret ikke kørt, mens slutresultatet manglede; slutsuiten omfatter13 faktiske tests uden skips. Tests omfatter rationel Bernstein- og afledtkontrol, separat Lagrange-produktform, stencilgrænser,90-cifret Decimal-rate/derivativ-orakel for både tekst- og binære input, termiske fortegn/enheder, begge Jacobianrækker, streng versus ikke-streng lukning, begge faktiske radiedomæner, inputkorruption og det faktiske første mislykkede forsøg. Fire closure-udtryk er desuden kontrolleret med separat90-cifret Decimal-exp/log.

De alternative formler og Decimal-kontroller deler kilder og præmisser med producenten. Ingen ekstern fagfælle, separat agent, formel teoremprover eller uafhængig kosmologisk reproduktion er brugt. En indledende scratch-smoketest havde en Python-parentesfejl og blev rettet før nogen numerisk kørsel; den ændrede ingen videnskabelig kode eller resultater. Gamle V16-tests, V18-algebra-tests, Q048–Q051-producenter og native kampagner er ikke genkørt.

Det fulde Q052 kræver fortsat native/common-background-anvendelighed, resten af domænet og events, relationen til faktisk native historik samt output-smoothing, xe/tau-transfer, integral og suprema. `source_real_certificate=false`, `native_background_membership_certified=false`, `full_q052_gate=UNRESOLVED`; globale ukendte fejlposter er null. Første-celle-claimet har sit eget betingede PASS. Accepteret model ændres ikke.

## Genbrug, provenance og GitHub-hukommelse

Repository: Morfindien/Bubbleverse, main@b68455c3cbcabeefa37e5f7fca39a21793650cab, commitets tree331439bf90bcb87c514035975abf2de304fa1fea. Alle fem vedhæftede V19-casefiler matcher aktuelle Git-blobs. Repository-søgningen fandt ikke en nyere Q052/V20-kerne, AGENTS.md eller en universel CURRENT_STATE/core. V18's præcise kilder, backend og bevis ligger allerede i den verificerede V19-bundle. CORE_VERSION=NOT_AVAILABLE; den leverede motor er minimumskontrakten.

README og programregistry blev læst. README fører fortsat med gammel V3/V2-starttekst; det er historisk navigation og må ikke udløse en ny native kørsel. Registryens Q052-NATIVEPAIR-V2 og Q052-VALIDATEDDIAG-V3 er ikke denne opgave. `Q052-DIRECTDEFECT-V1` er en lokal programidentitet, **ikke et registreret launcher-target**. Ingen workflow, registry eller README er ændret. De nye V20-filer skal placeres i repository-roden og linkes fra den aktuelle Q052-status; tidligere filer bevares. En foreslået statusændring og præcise pointere følger i handoff.

MEMORY_BACKEND:GITHUB. MEMORY_READ_STATUS:VERIFIED_AT_BASE. MEMORY_WRITE_STATUS:FILES_READY_FOR_MANUAL_UPLOAD. MEMORY_LINKS_UPDATED:NONE; foreslåede links er leveret. Ingen commit, PR, dispatch, modelskift eller offentlig post er udført. Filernes indhold er den nye memory-delta, ikke en påstand om integration.

## Beregningsvalg, gates og næste motor

COMPUTE_BACKEND:LOCAL_RUNTIME. GITHUB_WORTHWHILE:NO. GITHUB_WORTHWHILE_GATE:PASS. Den begrænsede256 arm/undercelle-evaluering og tests kan og blev kørt lokalt; ingen native software skulle bygges. Indledende kernel-/setuptid var UNMEASURED; faktisk kerne12.398s og slutsuite1.327s er nu målt. GitHub køtid, samlet integrationstid, ekstern pris og samlet operator-/rapporttid er fortsat UNMEASURED. Ingen betalt compute er bestilt.

EXECUTION_STATUS:COMPLETE for den afgrænsede opgave. RESULT_VALIDATION_STATUS:VALIDATED_WITHIN_STATED_CONDITIONAL_SCOPE. CONDITIONAL_FIRST_CELL_GATE:PASS. FULL_Q052_GATE:UNRESOLVED. CASE_LIFECYCLE:ACTIVE. TERMINATION_GATE:PASS for denne motor. Input-, source-/domain-, norm-, strengt closure-, no-repeat- og journalgates er dækket af receipt, spec, testlog og validationfil; launcher/merge/checkpoint er NOT_APPLICABLE. Ingen hel-domænefortsættelse er autoriseret af dette PASS.

**Næste motor: Result Ingestion & Routing2.3.0**, én gang med V20-resultatet. Overdragelse:PREPARED_NOT_SENT. Den skal registrere den nye betingede første-celle-lukning, bevare det første metodeforsøg og full-Q-begrænsningerne, indtage point/milepæl én gang og afgrænse næste forpligtelse. Ved et eventuelt nyt celletrin må E0 ikke nulstilles: slutfejlen fra V20 skal videreføres i samme fælles baggrund og koordinater. En ny beregningskontrakt skal vælge radier, håndtere grene/events og kræve streng closure med det ikke-nul initiale fejlbudget. V20 selv udfører ingen celle2 eller ny routingrunde.

## Point og SoMe

RUN POINTS:360. TOTAL WORK POINTS:3030=2670+360. PUBLICATION INTERVAL:1000. NEXT SOME MILESTONE:4000. POINTS TO NEXT MILESTONE:970. M003 leveres nu som to særskilte public/internal-filer; M001/M002 bevares. Ingen ekstern publicering. Point fordeles60 kilde/genbrug,150 ny intervalkerne,100 verifikation,50 faglig fortolkning. Det er en grov heuristisk vurdering, ikke ressource- eller evidensmåling. Det indledende360-estimat er bevaret; filarbejde og SoMe giver ingen ekstra point.

Bundlefilens `parent_activity_ledger` indeholder V18's2590. V19's80 eksisterende point er derfor genfundet fra dens leverede journal/rapport/task og videreført én gang; V19-ledgerens ukendte filhash er ikke opfundet. Den fulde V18-posthistorik er bevaret i V20-ledgeren. Milepælen lukker ikke Q052.

## Reproduktion og kilder

Læg de nye filer ved siden af den allerede leverede `Q052_DIRECT_DEFECT_EXECUTION_BUNDLE_V19.json` og kør ved behov:

```bash
python q052_direct_defect_v20.py --bundle Q052_DIRECT_DEFECT_EXECUTION_BUNDLE_V19.json --output replay_receipt.json
Q052_RESULT=replay_receipt.json python -m unittest test_q052_direct_defect_v20 -v
```

Programmet kræver Python3 og MPFR4.2.1 på Linuxx86_64LP64. Det skriver kun en ny outputfil og afviser overskrivning; replay er en ny reproduktionshandling, ikke nyt videnskabeligt arbejde. Den hash-pinnede scalar-backend udlæses midlertidigt fra V19-bundlen. Der findes ingen START-knap til denne lokale opgave.

- [V19-bundle, præcis verificeret version](https://github.com/Morfindien/Bubbleverse/blob/b68455c3cbcabeefa37e5f7fca39a21793650cab/Q052_DIRECT_DEFECT_EXECUTION_BUNDLE_V19.json): hele inputtransporten, originale sourcebytes, bevis og receipts; SHA256`3f3838394c1a85b2fa592dc2fb4c66d7c67e3d6c74a07873b9a060c22aebe89c`.
- [V18 direkte defektbevis, §§2,4,5.3,6](https://github.com/Morfindien/Bubbleverse/blob/b68455c3cbcabeefa37e5f7fca39a21793650cab/Q052_BACKGROUND_TRANSFER_PROOF_V18.md): det betingede theorem, normen, startkonventionen og Jacobianlofter.
- [hydrogen.c, frosset kilde](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c): atominitialisering, rateinterpolation, SWIFT-RHS og dispatcher; i bundlen kaldt hyrec.c.
- [wrap_hyrec.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c): SI→cm⁻³, eV-konvertering, gren og derivativfortegn.
- [thermodynamics.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c): aktiv termisk ligning og x=-z-fortegn; headers og alle anvendte tabeller følger med i inputbundlen.

Evidensklasser: selve de udførte intervalværdier er BUBBLEVERSE_NUMERICAL_RESULT; sourcebytes er teknisk primære kilder; dette nye argument og fortolkningen er AI_GENERATED_ANALYSIS. De arvede admitted/positive-escape-præmisser er betingelser, ikke observationer.
