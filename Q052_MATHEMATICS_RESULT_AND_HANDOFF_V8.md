BUBBLEVERSE — OVERLEVERING

STATUS: FORTSÆTTER — Q052 ER ÅBEN  
WORKFLOW_STATE: READY_FOR_HANDOFF  
SCIENTIFIC_STATE: INCONCLUSIVE for det fulde Q052; dokumenteret delresultat om de gemte interpolanter  
TECHNICAL_STATE: PASS for udført eksakt efterbehandling og separate aritmetiske checks; source-real fejlcertifikat INCOMPLETE  
TARGET_Q: Q052  
AUTHORIZED_Q_RANGE / EVIDENCE_BOUNDARY: Q052 og de eksplicit frosne Q048–Q051-afhængigheder; ingen senere Q anvendt  
PROMPT_ID / PROMPT_VERSION: BUBBLEVERSE.MATHEMATICS / 2.3.0  
RUN_ID: LOCAL-Q052-MATHEMATICS-NATIVE-CERTIFICATE-V8  
VALGT NÆSTE MOTOR: BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0  
DISPATCH: NOT_PERFORMED.

## Dokumenteret svar og hovedspørgsmål

De eksisterende data kan give et **rigorøst certifikat for præcist definerede interpolanter af de gemte tal**, men denne kontrol etablerer ikke den ønskede fejlgrænse til den underliggende source-real-løsning. To præcisionsniveauer leverer ikke den manglende fejlgrænse. Det første konkrete informationsproblem er, at en fuld tilstandsrekonstruktion og dens temperatur-/brancheresidual ikke kan evalueres fra de syv gemte kolonner. Den nødvendige nye diagnostic-kontrakt er nu specificeret.

Det uændrede spørgsmål er:

> Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

Denne runde ændrer hverken spørgsmålet, fysikken, reionisationsindstillingen eller Q051's betingede theorem. Den tidligere korrekte betegnelse »gittermaksimum« bevares. Ingen historisk kørsel omklassificeres.

## Ny beregning: hele splineceller, ikke ekstra sampling

Native run40350424272, attempt1, execution commit59631447fab9e4b67a8d599422c76f7c373199f2 genbruges. Ingen kosmologisk integration er genkørt. Hvert niveau har4861 punkter og4860 celler. Det dækkede z-interval er0 til809.6825; sidste tal er det viste decimalnavn for den verificerede binary64-koordinat.

| Størrelse | Nominal | Refined | Certificeret betydning |
| --- | --- | --- | --- |
| sup abs Δx_e for gemt kubisk spline | [0.00000110720467419025501068, 0.00000110720467425944621511] | [0.00000110291896012718997522, 0.00000110291896014694724668] | Hele det gemte z-domæne, eksakt rationale koefficienter |
| sup abs Δtau for eksakt integreret gemt opacity-spline | [0.00002420392909987223728202, 0.00002420392909987223728203] | [0.00002433629693645924548139, 0.00002433629693645924548140] | Hele det tilsvarende konformtidsinterval, integral fra z=0 |
| Maksimal afvigelse mellem eksakt opacity-integral og gemt parret kumulativ kolonne ved knuder | ≤2.8233634542e-16 | ≤3.8918574038e-16 | Kun disse nodale aritmetik-/serialiseringsafvigelser |

Alle observabler og fejl i tabellen er dimensionsløse. Intervallerne er deterministiske indhegninger af de specificerede numeriske objekter, ikke statistiske konfidensintervaller eller målinger. De ekstra cifre er teknisk reproduktionsinformation.

Det nominelle spline-maksimum har et verificeret nedre vidne nær **z=809.494388885498** i sidste komplette celle. Den separate stationærpunktskontrol bekræfter intervallet. Spline-maksimum er cirka10,7% større end det tidligere nominelle gittermaksimum1.0001128312991242e-6. Dette viser konkret, hvorfor gittermaksima ikke må kaldes kontinuerte suprema. Årsagen til oversvinget er ikke isoleret ved et nyt execution-eksperiment; en effekt af interpolationen nær interventionen er en fortolkning, ikke et bevist solverproblem.

Begge interpolanter er inden for0.0023814 og0.0421 **på det dækkede domæne**. Dette er hverken en validering af alle Q051-præmisser eller et helt0≤z≤810-certifikat. Optisk dybde over den sidste manglende del er ikke sat til nul.

### Definition og bevis for interpolantcertifikatet

17-signifikante-cifres CSV-tokens føres tilbage til deres endelige binary64-tal. Disse tal repræsenteres derefter som eksakte rationale tal. Der påstås ingen fejlgrænse mellem disse tal og den eksakte IVP.

For én celle med koordinatlængde h og t∈[0,1] bruges den låste kildes splineform:

\[
S(t)=(1-t)y_0+t y_1+\frac{h^2}{6}\{[(1-t)^3-(1-t)]m_0+(t^3-t)m_1\}.
\]

For x_e er koordinaten z og m=d²x_e/dz². L/R har identiske koordinater; deres forskel er derfor én kubik med differerede koefficienter. Formen følger arrays.c:1796–1875 og thermodynamics.c:225–282 ved det frosne physics-commit. Den generelt valgte kubiske interpolant er det certificerede objekt. Kildens særlige lineære reionisationsgrene, hvis aktive, er ikke stiltiende kaldt kubiske; ingen påstand om alle mulige API-grene er nødvendig for dette objekt.

For opacity er koordinaten eta i Mpc, h=eta[i+1]−eta[i]<0, y=dkappa i Mpc⁻¹ og m=d²dkappa/deta² i Mpc⁻³. Det kontinuerte kumulative objekt defineres ved

\[
T_i(t)=T_i(0)-h\int_0^t S_i(s)\,ds,\qquad T_0(0)=0.
\]

Den negative h giver den korrekte fortegnkonvention fra z=0 mod større z. Integralpolynomiet er af grad4. Integralerne summeres eksakt fra celle til celle, før L/R subtraheres. De er derfor ikke identiske med en definition, der genstarter fra en afrundet kumulativ CSV-værdi i hver celle. Netop den afvigelse ved alle knuder er beregnet særskilt. En kontinuerlig monoton parametrisering gennem de fælles eta-knuder ændrer ikke supremummet over det dækkede interval.

Et polynomium P(t)=Σc_k t^k omskrives eksakt i Bernstein-basis af grad n:

\[
b_i=\sum_{k=0}^i c_k\frac{\binom{i}{k}}{\binom{n}{k}},\qquad
\min_i b_i\le P(t)\le\max_i b_i.
\]

Basisfunktionerne er ikke-negative og summerer til1; dermed er max|b_i| en gyldig øvre grænse for |P| på hele cellen. Evaluerede endepunkter/midtpunkter giver nedre grænser. Eksakt rational de Casteljau-halvering opdeler cellen og indhegner alle mellemliggende værdier. Det globale stopkrav var øvre−nedre≤10⁻¹⁶ for hvert polynomielt supremum. Dette er et beregningskrav for interpolanten, **ikke** en valgt fysisk negligibilitetstolerance. Der krævedes15/16 opdelinger for de to x_e-maksima; integralernes globale Bernstein-loft var allerede deres eksakte slutværdi.

Den separate checker importerer ikke producenten. Den indhegner kvadratiske stationærrødder for alle x_e-kubikker med integer-square-root og120-bit rationale grænser. Dens sup-indhegning ligger inde i producentens interval. Den kontrollerer også opacity-slutintegralet og samtlige nodale afrundingsafvigelser med den uafhængige lukkede form

\[
-h(y_0+y_1)/2+h^3(m_0+m_1)/24.
\]

Checkerens tau-slutkontrol alene beviser ikke et globalt maksimum; hele-domæne-loftet kommer fra producentens Bernstein-argument. Kontrollerne deler CSV-data og kildeform; dette er begrænset uafhængig aritmetisk kontrol, ikke en uafhængig fysisk replikation eller formel theorem-prover.

## Første præcise blocker og hvorfor data ikke afgør den

BLOCKER_ID: **LOCAL-Q052-FULLSTATE-RESIDUAL-AND-EVENT-CLOSURE-MISSING-V8**.

Den gemte history.csv har z, eta, x_e, d²x_e/dz², opacity, dens eta-andenderiverede og kumulativ tau. Den har ikke en tæt rekonstruktion af D_Tmat eller v=Tmat/Trad, den aktive interne x_H, brancheskift, fuld background-tilstand eller indhegnet afledt. En spline-andenderiveret for x_e er ikke temperaturens IVP-residual.

Den faktiske kilde læser Tmat direkte fra den evolverede D_Tmat ved thermodynamics.c:2597 og sender den til HyRec ved:2665. wrap_hyrec.c:135 vælger PEEBLES ved **Trad_phys≤TR_MIN ELLER Tmat/Trad≤T_RATIO_MIN**. hydrogen.c:1054–1080 har yderligere Pion- og SWIFT-fit-dispatch; interpolate_rates har warm/cold-reglen ved v=1. Lighedsreglerne er del af målet og kan ikke erstattes med glatte blandinger. De manglende temperatur-/tilstandsdata er derfor relevante for selve feltet F, ikke blot en sekundær observable.

Selv dér hvor h kan udledes af X=h+q uden reionisation/smoothing, følger v ikke af de syv kolonner. Under reionisation og kildebestemt output-smoothing er output-X heller ikke generelt lig den interne h+q. At vælge en temperaturkurve, der passer pænt gennem startpunktet, ville være en ny uverificeret rekonstruktion.

En elementær informationskontrol: Tilføj en glat bump med støtte strengt inde i én celle. Bumpen og alle dens afledte kan være nul ved samtlige gemte knuder, mens dens indre amplitude er vilkårlig. Endelige værdi-/andenderivattabeller alene udelukker derfor ikke mellemknudeafvigelser for en ukendt sand funktion. Bumpen påstås **ikke** at være en løsning af den kendte IVP. Pointen er, at den nødvendige IVP-/residualkontrol er det ekstra argument, som skal udelukke den; den er ikke indeholdt i knudetallene.

Tilsvarende har to approksimationer X+a+e_N og X+a+e_R forskel e_N−e_R, uanset størrelsen af den fælles bias a. Refined-niveauet ændrer desuden præ-interventionsstarten: Δh_start≈1.0109100631e-9 og ΔD_Tmat_start≈−9.5177042603e-7 K i forhold til nominal. L/R matcher inden for hvert niveau, men de to niveauer er ikke identiske IVP-starts. Refinementdiagnostikken blander derfor start- og integrationsændringer. Den er fortsat nyttig som diagnostik, uden at blive en fejlgrænse.

Dette beviser en konkret mangel i den foreliggende residual-certifikatrute. Det er ikke et umulighedsteorem om enhver tænkelig valideret analyse af den fuldt kendte kilde. En ny valideret integration eller en særskilt kildebaseret enclosure kan i princippet levere de manglende oplysninger. En uændret native genkørsel med samme syv kolonner gør det ikke.

## Finite valideringskontrakt og mindste nye opgave

Den fulde maskinlæsbare specifikation er **Q052_VALIDATED_NUMERICS_CONTRACT_V8.json**. Den er DESIGNED, ikke EXECUTED. Stop denne matematikrunde efter det dokumenterede informationsproblem; implementér ikke en ny physics-solver under dække af et certifikat.

For hver arm q∈{0,10⁻⁶} sættes u=ln(811/(1+z)), 0≤u≤ln811 og y=(h,v), med eventuelle yderligere faktisk aktive kildevariable medtaget. B er den ene faste admitted fælles baggrund. På en gren σ er y′=F_σ(u,y;q,B). Udarbejd en eksplicit, differentierbar rekonstruktion yhat per glat segment med fuld tilstand, præcis initialcondition og source-real outputmap G.

Med en valgt og angivet norm, valideret tilstandstube, brancheregularitet og stabilitetsmajorant L(u), skal følgende endelige størrelser indhegnes:

\[
r(u)=\|\widehat y'(u)-F_\sigma(u,\widehat y(u);q,\widehat B)\|,
\qquad \|F_\sigma(\cdot;\widehat B)-F_\sigma(\cdot;B)\|\le\beta(u).
\]

Indhegnet kildearitmetik og rekonstruerings-/afrundingsusikkerhed tilføjes som a(u), herunder den eksplicitte forskel mellem det præcise endpoint10⁻⁶ og dets native binary64-repræsentation, hvis det præcise endpoint er target-IVP. På et valideret glat segment [s,t] giver differentialuligheden

\[
E(t)\le e^{\int_s^t L}\,E(s)
+\int_s^t e^{\int_\xi^t L}\,[r(\xi)+\beta(\xi)+a(\xi)]\,d\xi.
\]

Det følger af at subtrahere rekonstruktionsligningen fra IVP'en og anvende normens differentialulighed samt integrerende faktor. L kan være en verificeret ensidet/logaritmisk-norm-majorant eller en almindelig Lipschitz-majorant i den valgte norm. Ingen numerisk L, residual eller eventfaktor er målt her. Hvis et groft L giver en ubrugelig grænse, er det INCONCLUSIVE og ikke tilladelse til at indsætte en mindre faktor.

Formlen må **ikke** bruges hen over et diskontinuert brancheskift uden ekstra argument. Hver guard skal enten have certificeret fortegn på tuben eller indgå i en valideret eventslab. For almindelige isolerede transversale, kontinuerte-state-events kan et lokalt flow-/saltationsbound bruges efter kontrol af normal og nævner. Coincidens, start-/endepunktsevents og ligehedsregler kræver den faktisk relevante finite-order-/tube-kontrol. En intervalindhegning af flere mulige grene er kun en beregningsindhegning; den ændrer ikke løsningen til et Filippov-system. Q051's q-parameterkoefficient2381.4 må ikke automatisk genbruges som Green's-funktion for vilkårlige residualer eller initialfejl.

Med et valideret outputmap og en tilstandsfejl E_q findes et observable-bound e_X,q. Hvis der sammenlignes med en separat gemt output-spline, skal dens afstand til G(yhat) også indgå. For pairen fås e_pair≤e_X,L+e_X,R. På et fuldt dækket domæne giver dette

\[
\max(0,\widehat M^-_X-e_{pair})\le\sup|\Delta X|
\le\widehat M^+_X+e_{pair}.
\]

Thomson-transfer kræver separat samme-baggrundskernel w_B(z)≥0 og indhegnet quadrature-/kernel-/outputfejl:

\[
|\Delta\tau-\Delta\widehat\tau|
\le\int_0^Z w_B(z)(e_{X,L}+e_{X,R})\,dz
+\int_0^Z|w_B-\widehat w|\,|\Delta\widehat X|\,dz
+e_{quad}+e_{map}.
\]

Dette er en trekantsulighed for Δtau=∫w_BΔX og den valgte approksimation; e_map omfatter enhver forskel mellem dens integrand og den gemte opacity-interpolant. Konstantenheder, z↔eta, nH og sigma_T skal føres korrekt med. Sæt ikke den manglende kernel-fejl til nul ud fra parameteridentitet.

Den mindste nye capture er fuld state/dense-step-rekonstruktion for én eksisterende nominel L/R-pair med uændret kilde, binary, start og config; guard-/phase-/outputmap-information; nødvendig fælles background-rekonstruktion; samt outputkoefficienter på hele sidste celle til810. Alle endelige accepterede trin skal kunne indhegnes. NDF15-historik/Jacobian caches behøves kun som yderligere capture, hvis en validering af det konkrete algoritmiske trin kræver dem; de er ikke en universel forudsætning for residualmetoden. En residualrekonstruktion kan være en anden piecewise-polynomiel rekonstruktion, hvis dens forbindelse til den observerede native bane bevises.

For det historiske run findes den fulde trace ikke blandt de bevarede branch-filer; den kan ikke udledes alene af det observerede output. En instrumenteret rekonstruktion er et **nyt** run med nyt ID. Match af de gamle syv kolonner gør ikke den nye interne trace til historisk evidens for40350424272. Ny validated-reference og gammel interpolant kan dog sammenlignes matematisk med tydeligt forskellige roller. Intet core-rebuild, refit, tau-shooting, selector-smoothing eller ny Q er autoriseret af dette handoff.

Det udækkede interval har bredde cirka0.3175 i z. En præcis z810-start begrænser kun det ene endepunkt; den dokumenterer ikke hele intervallet eller dets tau-integral. Eksportér den straddlende celle med begge sider og en separat post-interventionsdefinition; ekstrapolér ikke den sidste gemte kubik som om den var næste kildecelle.

## Afgrænsninger, gates og næste motor

Q051 gav en betinget analytisk envelope, ikke native error. Q050-bindingens egen status er CONDITIONAL_BACKGROUND_ENCLOSURE_REQUIRES_VALIDATION_RECEIPT. En ens effektiv parameterliste etablerer ikke alene tilhørsforhold til den retained connected-familie eller den eksakte baggrundsbane. Genbrug et dækkende valideret receipt, hvis det findes; ellers returnér den præcise manglende background-closure. Udfør ikke Q049–Q051-producenter igen.

G1 PASS: entydigt spørgsmål og scope. G2 PASS for nye interpolantinputs; source-real-diagnostics mangler eksplicit. G3/G4 PASS for det begrænsede eksakt-aritmetiske objekt, UNRESOLVED for den fulde IVP. G5: separat aritmetisk kontrol, med fælles kilder og begrænsninger oplyst. G6: det første materialt nødvendige diagnostic-gap er dokumenteret og har en finite kontrakt. G7 PASS for journalprefix, provenance og append. **Q052 termination gate: NOT SATISFIED**; ingen Motor14-lukning eller accepted-model-change.

Result Ingestion & Routing modtager det faktisk nye splinecertifikat, informationsanalysen og diagnostic-kontrakten. Dets ene relevante næste forskningsbeslutning er at sende den afgrænsede capture/validated-numerics-opgave til den etablerede Execution/HPC-builder-funktion, hvis den kan levere kontrakten. En uændret fire-job genkørsel eller en generel refinementkampagne er ikke næste opgave. Hvis kontrakten ikke kan opfyldes, skal den første konkrete adgangs-/implementationsmangel returneres, og Q052 forbliver åben.

## Samlet journal, GitHub og provenance

**Q052_SAMLET_JOURNAL_V8.md** indeholder alle indgående V7-bytes uændret som prefix plus denne rundes append. ParentSHA256:727d0a01cd11bce50eb8a69f68194e6ff6ea1c49f3d03f05fb8d486a5803ebab. Dette er den samme logiske Q052-journal, ikke en parallel matematikjournal. Den arvede Q051-oplysning om en manglende original M14/Mikami-mellempost forbliver gældende; denne fil rekonstruerer den ikke.

GitHub-read ved Morfindien/Bubbleverse@093d474958e76e2a44fe306afc8c6913b0ba3991 viser, at Jim har uploadet V7-journal og V7-ledger. Begge matcher de vedhæftede bytes. Det retter den **aktuelle** integrationsstatus fremadrettet; V7's historiske »ikke uploadet af denne intake« ændres ikke. README's gamle NOT_YET_COMPUTED-beskrivelse er forældet; ingen videnskabelig konflikt med det nyere run/journal følger. Q052-programmet findes ACTIVE i registry. Ingen AGENTS.md eller CURRENT_STATE-path blev fundet i det komplette tree; der opfindes ikke en global pointer.

GITHUB_READ_STATE: VERIFIED for relevante pins og V7-tilstand.  
GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD. Tidligere write gav403; ingen ny write, commit eller dispatch påstås. Memory-update i handoffet angiver de konkrete roddestinationer og en fremadrettet README-henvisning. En ny fil afleveret her er ikke i sig selv et GitHub-commit.

Kilde- og claimregisteret indeholder SHA256 og de verificerede primære kildelinjer. Physics commit er5a131c91d657dd9a7c6364cc45b038710f8d0d97. Fuld hydrogen.c og arrays.c er hentet på dette commit og Git-blobchecket. thermodynamics.c og Q051-afhængighedstekster er hashkontrolleret fra den frosne bundle b7edfbf830163cdc31b5e3af1a11717551a2eab4076cdad0481781ea9eea128b. Ingen ekstern litteraturpåstand er nødvendig for det selvstændige Bernstein-/residualargument.

Reproduktion: `python3 q052_certify_interpolants_v8.py --input-bundle Q052_MATHEMATICS_INPUT_BUNDLE_V8.json --output audit.json`. Den separate checker bruger de fire CSV-filer angivet i filindekset, `--input-dir`, `--certificate` og `--output`. Seks analytisk løste tests dækker indre maksima, ikke-dyadiske stationærpunkter, negativ absolutekstremum, integralfortegn, global celleudvælgelse og binary64-identitet. De faktiske resultater og hashes kontrolleres i leveringsvalideringen. R2 for denne efterbehandling; ikke R3 native/P6 eller fysisk replikation.

## Point- og udgivelsesstatus

RUN POINTS:220 pts. TOTAL POINTS:1310 pts. PREVIOUS TOTAL:1090 pts.  
POINTS_BREAKDOWN: ANALYSIS100 + COMPUTATION45 + SEARCH25 + VALIDATION50=220.  
POINTS_BASIS: Nyt interpolant-/integralargument, fuld-state-obstruktion og finite residual-/eventkontrakt; eksakt rational efterbehandling af9720 celler; målrettet repo-/pinned-source-readback; analytiske metodechecks og separat stationary-root/integral-kontrol. Skønnet er heuristisk, ikke målte tokens, kroner, energi eller konfidens. Gamle native integrations-/Q051-bevispoint genbruges uden dobbelttælling. Pakning, kopiering og aflevering giver0 point.  
PREVIOUS_POINTS_ENTRY: Q052-ACTIVITY-SUCCESS-INGESTION-40350424272-V7.  
POINTS_STATE: VERIFIED som videreført intern redaktionel ledger.  
CYCLE PROGRESS:310/1000. NEXT SOME MILESTONE:2000. POINTS TO NEXT PUBLICATION:690.  
NEW_MILESTONES:[]; PENDING_PACKAGES:[]; PUBLICATION_STATE:NOT_DUE.  
DELIVERED_MILESTONE_IDS:[Q052-SOME-M001]; tidligere public/internal-filer bevares, NOT_POSTED. Ingen ny pakke eller pointbaseret Q-lukning.

## ChatGPT-setupvurdering og leveringskontrakt

AKTUELT SETUP: Codex, Default mode; lokal Python3.12.14, eksakt Fraction, filadgang og faktisk GitHub-read. Eksakt modelvariant og skjult reasoningindstilling er ikke runtime-verificeret. Ingen subagent eller modelskift anvendt.  
ANBEFALET PRIMÆRT SETUP: kort Result Ingestion-kontrol af de nye claims; derefter den dokumenterede Execution/HPC-builder-funktion2.4.0 for en diagnostic-kontrakt, ikke en ny physics-core.  
KAPABILITETSKLASSE: H/C/A. REASONING-NIVEAU: højt anbefalet ved interval-/eventvalidering; ikke en påstået faktisk indstilling.  
BEGRUNDELSE: Næste gap er tilstands-/residual-/eventclosure med native3.11.16-lineage, som chatten ikke har kørt. Fil-/kildeanalyse og efterbehandling er VERIFIED_AVAILABLE; fuld validated-native execution er UNAVAILABLE her i denne runde.  
FALLBACK: præcis implementations-/background-/event-blocker med bevaret delcertifikat. UPGRADE-TRIGGER: dokumenteret behov for verified intervalsolver/tabel-/libm-indhegning eller event-bevis. DOWNGRADE-TRIGGER: alene intake-/indeksarbejde resterer. Ingen dyrere model eller HPC-tidsbevilling påstås nødvendig alene på grund af motorens navn.

ACCEPTANCE: Hele0≤z≤810 dækket; finite, efterprøvelige fejlintervaller for begge observabler; source/equality/background/start-præmisser verificeret; ingen to-level-error-genvej. REJECTION: et verificeret brud på den påståede certifikatkontrakt forkaster det certifikat, ikke automatisk fysikken. INCONCLUSIVE: ubundet residual, eventtube, background-tilknytning eller terminalcelle giver præcis blocker. GENOPTAGELSE: nye diagnostics eller et direkte valideret source-real-certificate, der opfylder kontrakten. Schema: UNVALIDATED_LOCAL_CONTRACT; faktisk felt-/type-/reference-/hashkontrol, intet opfundet globalt schema.
