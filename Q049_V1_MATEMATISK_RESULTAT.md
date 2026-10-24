# BUBBLEVERSE — OVERLEVERING

STATUS: FORTSÆTTER — præcis hindring dokumenteret; ingen certificeret talgrænse for hele halen.
WORKFLOW_STATE: READY_FOR_HANDOFF
SCIENTIFIC_STATE: INCONCLUSIVE
TECHNICAL_STATE: PASS — kun de afgrænsede kilde-, aritmetik- og kontroltests.
TARGET_Q: Q049
AUTHORIZED_Q_RANGE / EVIDENCE_BOUNDARY: Q049 med dokumenteret Q048-forhistorie til Motor 14-overleveringen; ingen Q050 eller senere resultater.
PROMPT_ID: BUBBLEVERSE.MATHEMATICS
PROMPT_VERSION: 2.2.0
RUN_ID: LOCAL-Q049-MATH-GLOBAL-ENVELOPE-20261024-V1
NÆSTE MOTOR: BUBBLEVERSE.RESULT_INGESTION_ROUTING2.2.0 — registrering af dette resultat, derefter kildekomplet global matematik på samme Q049.

## Dokumenteret svar

Der er ikke etableret en numerisk, rigorøs øvre grænse for den samlede resterende `|Δtau_T|` over `0 ≤ z ≤ 810`. Der er etableret en præcis hindring for at udvide det arvede bevis direkte: **Den frosne kildekode vælger nødvendigvis Peebles-operatoren på mindst `0 ≤ z ≤ 16`, mens det accepterede z=810-certifikat kun omfatter HMLA/SWIFT.** Den nødvendige ekstra kildegren er ikke dækket af dette certifikat.

Dette er en fejlende dækningspræmis for den foreslåede genbrug af beviset. Det viser ikke fysisk ustabilitet, stor faktisk optisk effekt eller umuligheden af enhver anden global grænse. En bred grænse fra andre, selvstændigt beviste invariants er fortsat mulig.

Derudover indeholder z=810-checkpointet ikke et snævert parvist hydrogen-/temperaturfejlområde. En lille initial differens ved selve heliumhændelsen må ikke uden et transportbevis genbruges som den aktuelle differens ved z=810.

Leverancen indeholder en betinget adjoint-metode, der kan begrænse integralet direkte uden at rekonstruere hele lav-z-banen celle for celle. Metodens symbolske gyldighed og en eksakt fremad/bagud-kontrol er kontrolleret; dens kosmologiske præmisser er endnu ikke certificeret.

## Spørgsmål og uændrede identiteter

Q049 undersøger den resterende lav-z-del af latch/reset-forskellen i Thomson-dybde for `hillipop-ede_n3`, med fælles frosne inputs, fast accepteret `z_reio` og anker ved z=810. Latch har `q=10^-6`, reset har `q=0` efter samme første cutoff-hændelse.

`q=xHeII=fHe*x_He` er normaliseret pr. hydrogenatom. Derfor er det residuale elektronbidrag `x_noreio=h+q`, **ikke** `h+fHe*q`.

| Identitet | Verificeret grundlag |
|---|---|
| Projektversion læst | `Morfindien/Bubbleverse@bc9a4909bedb1d8be508c7f255407827f49ada9d` |
| Frossen fysisk kilde | `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97` |
| Arvet capture/config-pin | `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b` |
| Faktisk fil bag denne pin | `q048_prefix_config_v1.json`, 105.567 bytes; indeholder captured hex-felter og kildederiverede reioniseringsindstillinger |
| Accepteret checkpoint | `Q048_V151_ACCEPTED_CHECKPOINT_V1.json`, 8.071 bytes, SHA-256 `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96` |
| Faktisk accepteret anker | actual127 / frontier810, `a=1/811` |
| Accepteret z_reio | `0x1.dfec4p+2` = 7,4987945556640625, dimensionløs |

Alle opregnede SHA-256-værdier er kontrolleret mod læste bytes. Capture/config-navnet er præciseret fremadrettet; der er ikke påstået en ny rå capture eller ny måling. Hele capture-arkivets oprindelige provenance er arvet, ikke reproduceret her. Reioniseringsbredde, eksponent og heliumindstillinger i config er mærket `SOURCE_DERIVED_NOT_DIRECTLY_CAPTURED`; denne begrænsning bevares.

Q048 forbliver terminalt uløst efter sin eksisterende budgetpolitik. V154's 810→800-bevis forbliver ACCEPTED_UNCONSUMED. Der er ikke forbrugt noget bevis, oprettet actual128 eller flyttet nogen frontier.

## Ny præcis hindring: LOCAL-Q049-OBS-001-SOURCE-MODE-COVERAGE

Den frosne wrapper bruger, uden aktive varierende konstanter,

\[
T_{\gamma,\mathrm{eV}}=k_B T_0(1+z),
\]

og vælger `PEEBLES`, når `Trad_phys <= TR_MIN` **eller** `Tmat/Trad <= T_RATIO_MIN`. De kildefaste decimalkonstanter er

\[
k_B=8.617343\,10^{-5}\;\mathrm{eV/K},\quad
TR_{\min}=0.004\;\mathrm{eV},\quad T_{\mathrm{ratio,min}}=0.1.
\]

Captured `T0=0x1.5cdd2f1a9fbe7p+1 K` er læst som en eksakt rational repræsentation af binary64-værdien. Temperaturgrænsen er derfor den eksakte rational

\[
z_T=\frac{0.004}{(8.617343\,10^{-5})T_0}-1,
\qquad 16.02<z_T<16.04,
\]

med orienterende decimal `16.0310108356`. Den fulde rational står i `Q049_V1_CERTIFICATE_RESULT.json`. Ved simpel eksakt krydsmultiplikation fås

\[
17\,k_B T_0<0.004.
\]

Dermed er Peebles-grenen tvungen for hele `0 ≤ z ≤ 16`, uanset temperaturforholdets værdi. Intervallet ligger inden for Q049's målområde. For en fortsættende admissibel kildebane er det tilstrækkeligt til at afvise global kildekomplethed af det arvede HMLA/SWIFT-certifikat.

`z_T` er grænsen for den sikre temperaturudløste fallback, **ikke** den første faktisk nåede switch. Temperaturforholdet eller de interne hydrogenvalg kan skifte tidligere. Kildens decimalfortolkning er den source-real fortolkning; en ny native floating-point- eller switch-timing-certificering påstås ikke.

Kildetræets Git-blob for `hydrogen.h` er uafhængigt kontrolleret som `088b34a699efe5d6d3aefb158229e9fb83d9a586`. Wrapper og hydrogenimplementation viser både valgbetingelsen og kaldet til `rec_TLA_dxHIIdlna`. Dette er en konkret kildegren, ikke en antaget ekstra model.

## Ankeret begrænser ikke automatisk parrets forskel til epsilon

Det accepterede checkpoint bærer scalar-/baggrundsendpointet `(a,E,Y,Vbar)` og et fælles tilladt termokemisk område. Det er ikke en eksport af `(h_L,h_R,w_L,w_R)` med deres relation.

De arvede projektioner giver ved z=810

\[
L=346752030166741/10^{18},\quad U=99999/100000,
\quad w\in[-10^{-6},1/50].
\]

En gyldig, men meget bred følge er

\[
|h_L-h_R|\le U-L\simeq0.99964324797,
\qquad |w_L-w_R|\le0.020001.
\]

Disse deterministiske projektionsdiametre kræver ingen antagelse om statistisk uafhængighed. De er ikke målte forskelle og heller ikke bevis for, at yderpunktsparret faktisk er nåeligt fra den fælles hændelse. De viser præcist, hvad checkpointets projicerede oplysninger alene kan give. Et smallere relationelt initialområde eller en global kontraktionsanalyse kan forbedre dem; dette er ikke vist umuligt.

## Direkte integralmetode: betinget adjoint-certifikat

Denne del er en ny direkte formulering af den allerede kendte komponentvise sammenligningsmetode. Den tidligere journal indeholder allerede Jacobian/Metzler- og Thomson-kernelrelationerne; disse genfremsættes ikke som ny fysik.

Sæt

\[
t=\log\frac{811}{1+z},\quad 0\le t\le T=\log811,
\quad r=(|\Delta h|,|\Delta w|)^T,\quad \epsilon=10^{-6}.
\]

Alle koordinater her er dimensionløse. Fælles baggrund, frosne parametre og kvalificerede løsninger skal bruges som **samme** objekter i begge grene. Antag på hele et fremadrettet certificeret domæne, at

\[
D^+r\le A(t)r+f(t),\quad f=\epsilon b+d,\quad A_{ij}\ge0\ (i\ne j),
\]

hvor `d` omfatter enhver tilladt selector-/modelskiftsmismatch og valideret realiseringsfejl. Signed diagonalled bevares. En fuld kildekomplethedspræmis er nødvendig før denne ulighed kan bruges globalt.

Med observer-normaliseret fysisk Thomson-dybde er

\[
\kappa(t)=\frac{c\sigma_T n_{H0}(1+z(t))^3}{H_s(z(t))}>0,
\qquad \Delta\tau_{\rm tail}=\int_0^T\kappa\Delta x_e\,dt.
\]

Faktoren `(1+z)^3` følger af `|dz/dt|=1+z` anvendt på den kendte redshift-kernel med `(1+z)^2`. `c` er i m/s, `sigma_T` i m², `nH0` i m⁻³ og `Hs` i s⁻¹; kernel og dybde er dimensionløse. Ingen konstantværdi eller Hubble-enhed er numerisk indsat her.

Antag et kvalificeret output-map

\[
|\Delta x_e|\le g(t)^T r+g_q(t)\epsilon+e_o(t),\quad
g,g_q,e_o\ge0.
\]

For usmoothet `x_noreio=h+q` er `g=(1,0),g_q=1`. Fælles frosset `reio_camb` giver den eksakte multiplikative gain `1-S(z)` på forskellen; fælles senere heliumtilførsel bortfalder i differensen. Konveks makrosmoothing kan behandles via en fælles gain, når begge side-maps er kvalificeret. Native spline-output skal have sin egen operator-/restfejlsgrænse; det følger ikke automatisk af kontinuerte state-bounds.

Vælg en ikke-negativ, stykkevist absolut kontinuert adjoint-supersolution `p`, der opfylder

\[
-p'(t)\ge A(t)^Tp(t)+\kappa(t)g(t),\qquad p(T)\ge0.
\]

Da følger den direkte grænse

\[
\boxed{
|\Delta\tau_{\rm tail}|\le
p(0)^Tr(0)+\int_0^T p(t)^Tf(t)\,dt
+\epsilon\int_0^T\kappa(t)g_q(t)\,dt
+\int_0^T\kappa(t)e_o(t)\,dt.}
\]

**Bevis.** For næsten alle t giver produktreglen og `p≥0`
`(p^T r)' ≤ -kappa*g^T r+p^T f`. Integration og `p(T)^T r(T)≥0` giver uligheden; trekantsuligheden for Thomson-integralet og output-grænsen giver boksen. Adjointlighedens løsning med `p(T)=0` er en mulighed, men en verificerbar eksplicit supersolution er nok. Der kræves ikke en fuld rekonstrueret x_e-bane.

Ved fælles faste transfers `r^+≤Jr^-+eta`, `J,eta≥0`, kræves `p^-≥J^T p^+`; tilføj `p^+·eta` for hver transfer. Tilstandsafhængige, usynkroniserede switches kræver særskilt mismatch-/eventbevis. Et glat Jacobian-bevis hen over dem er ikke tilstrækkeligt.

### Korrelation og temperaturled

For fælles `A_C(t)>0`, `fHe` og reioniseringsindstillinger gælder eksakt

\[
\Delta\beta=A_C(1+f_{He})\frac{\Delta x_e}
{(1+f_{He}+x_{e,L})(1+f_{He}+x_{e,R})},
\]

\[
\Delta w'=-(1+\beta_L)\Delta w-\Delta\beta\,w_R.
\]

Det bevarer fælles state-afhængighed før eventuel konservativ majorering. De to forekomster af samme h må ikke erstattes af uafhængige h-værdier i et påstået skarpt ratio-bevis.

For en konveks hydrogenroster `F_lambda=lambda F_H+(1-lambda)F_S` med potentielt forskellige selectors indeholder den eksakte differens ved fælles tidspunkt også

\[
(\lambda_L-\lambda_R)(F_H(y_R,q_R)-F_S(y_R,q_R)).
\]

En fælles kildekode betyder ikke automatisk `lambda_L=lambda_R`, da selector kan afhænge af state. Dette led skal begrænses eller bevises fraværende. En eksplicit mismatch-majorant tillader stadig et gyldigt, eventuelt bredere, certifikat. Efter fallback skal Peebles-feltet indgå. Ingen af disse mangler beviser, at en brugbar grænse er umulig.

## Udført validering og dens begrænsning

Den prospektive kontrakt er frosset i `Q049_V1_VALIDATION_CONTRACT.json`; SHA-256 `e4996e77b41bee7c11c20e227949b87496c2c1cc5677879a71305783e2460f23`. Ingen materialitetsgrænse er opfundet eller efterjusteret.

`q049_v1_certificate.py` bestod 31 eksakte/provenancekontroller. `q049_v1_independent_verify.py` bestod 40 kontroller uden at importere producenten. Den anden vej rekonstruerer hex-tal med heltal, bruger krydsmultiplikation, kontrollerer kildens Git-blob og integrerer et fremad/bagud-polynomium separat.

Den fremstillede kontrol bruger `A=[[0,1],[0,0]]`, `f=(0,epsilon)`, `g*kappa=(1,0)`, `T=1`, `r(0)=0`. Fremad fås `r=(epsilon*t²/2,epsilon*t)` og integral `epsilon/6`. Bagud fås `p=(1-t,(1-t)²/2)` og samme eksakte integral `1/6000000`. Dette er en algebraisk kontrol, ikke en kosmologisk simulation.

Uafhængighedens rækkevidde: separat beregningsvej og ingen producentimport; samme analytiker, inputbytes og matematiske præmisser. Ingen selvstændig fysisk måling, native reproduktion eller uafhængig menneskelig review påstås. Reproducerbarhed R2 for den nye eksakte hindringskontrol; R1/DESIGNED for et fysisk numerisk adjoint-certifikat. Source-real/native identitet og NativeP6 er fortsat uafklaret.

G1 PASS: entydigt spørgsmål. G2 PARTIAL: anker og kildeskift verificeret; fuld global certificering mangler. G3 PARTIAL: direkte theorem og hindring kontrolleret; koefficienter/integral ikke kvalificeret. G4 NOT_RUN for kosmologisk robusthed. G5 PASS kun for afgrænset rekonstruktion. G6 NOT_SATISFIED for talgrænse. G7 PASS efter journalens byteidentiske prefix-kontrol. **Q049 er ikke CLOSED.**

## Budget og journal

RUN COST: 148 pts
USED: 148/1000 pts
REMAINING: 852 pts
BUDGET_STATE: ACTIVE
PREVIOUS_BUDGET_ENTRY: `Q049_QUESTION_BUDGET_LEDGER_V1.json`, aktivering `LOCAL-Q049-BUDGET-ACTIVATION-M14-V1`, SHA-256 `433fab75e72f739198b5be4876e453a75c4c553baa693aaa71f734e336284da2`.

ESTIMATED_RUN_COST: 140; MAX_RUN_COST: 180. COST_BREAKDOWN: analyse 60 + beregning 12 + søgning 28 + validering 24 + levering/journal 24 = 148. Point er et vurderet arbejdsregnskab, ikke kroner, målte tokens eller credits. Afvigelsen skyldes recovery af det faktiske checkpoint og den kildepræcise lavtemperaturgren. Ingen reservation eller gammel charge er debiteret igen; ingen overrun.

Ny ledger er `Q049_QUESTION_BUDGET_LEDGER_V2.json`. Den autoritative journalstrøm videreføres i `Q047_SAMLET_JOURNAL_Q049_V1_APPENDED.md`: hele forgængerens 14.856.072 bytes bevares som eksakt prefix; kun én ny Q049-post tilføjes. Rapport og støttemetadata udgør ikke parallelle journaler. De historiske poster er bevaret, men deres samtlige ældre eksterne links og tests er ikke genverificeret.

## Setup og næste afgørende arbejde

Aktuelt setup: Codex-session, lokal Python/Fraction, filer og verificeret GitHub-read. Konkret modelnavn og reasoning-indstilling er ikke særskilt verificeret; ingen modelændring eller subagents. Kapabilitetsklasse H/X/A/C. Primært anbefales samme fokuserede matematiksetup; fallback er tilsvarende filer/kode/repositoryadgang. Eskalér først hvis kildekomplette globale koefficienter eller eventgrænser ikke kan kvalificeres lokalt; nedskalér ved ren metadataindtagelse. Ingen HPC-, produktions-, native-, fit-, refit- eller Actions-kørsel er startet.

Indtag dette resultat én gang og fasthold samme Q049-ledger. Den næste særskilte matematiske opgave er at etablere et kildekomplet globalt sammenligningsområde med Peebles-felt og switchmismatch samt en verificeret adjoint-supersolution. Brug enten de ærlige brede initialdiametre eller et selvstændigt begrundet skarpere parvist z=810-område. Bevis domæne, output-map og positiv kernel samlet før et tal accepteres. Et nyt native capture er ikke automatisk nødvendigt. Gentag ikke denne kildegrænsekontrol som nyt videnskabeligt fremskridt og gå ikke tilbage til Q048's 10-redshift-loop.

GITHUB_READ_STATE: VERIFIED for de opregnede filer/versioner; fuld repo-audit er ikke udført.
GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD. Ingen GitHub-write, commit, PR eller dispatch påstås. Eksisterende kilde-/historikfiler er uændrede. Permanente videnskabelige Q049-registry-writeback er fortsat afventende; programregistry er ikke stiltiende gjort til spørgsmålsregister.

MODEL_DIFF: NONE — ingen accepted-model-promovering. Nyt lokalt metode-/hindringsrecord og Q049-budgetappend alene.

## Kilder og filspor

K1 — Autoritativ journal: `Q047_SAMLET_JOURNAL_Q048_M14_EXHAUSTED_Q049_SELECTED_V1.md` ved den opregnede projektcommit. Understøtter ankerets accepterede status, Q048-terminalisering, Q049-udvælgelse og budgetstart. Intern forskningshistorik, ikke empirisk uafhængig evidens.

K2 — [Frossen wrapper](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c), navnlig linje 132–141 og 175. Understøtter kildevalget, enheder og q-normalisering. Kildeimplementering af CLASS/HyRec-bidragsydere; source-real fortolkning.

K3 — [Frosne konstanter](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.h), linje 57, 67, 70, samt [hydrogenimplementation](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c), linje 1058–1077. Understøtter temperaturgrænsen og den separate Peebles-operator.

K4 — [Frossen termodynamik](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c), hydrogen-/temperaturrelationer omkring 2625–2760, reio_camb omkring 4153–4180. Understøtter forskellen mellem x_noreio og x_reio samt det fælles reioniseringsmap.

K5 — Det genfundne byteverificerede V151-checkpoint og `q048_prefix_config_v1.json`. Understøtter operatorroster, initiale projektioner og captured constants. Hele råkørslen er ikke reproduceret her.

Ingen eksterne observationer, nye likelihoods, sigma-påstande, numeriske fysiske fejlskøn eller nye bibliografiske identifikatorer er tilføjet. Fuld lokal inputliste med hashes: `Q049_V1_INPUT_PROVENANCE.json`.
