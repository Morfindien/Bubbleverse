# BUBBLEVERSE — AFSLUTTET MATEMATISK SAG

STATUS: AFSLUTTET inden for det arvede betingede source-real scope
WORKFLOW_STATE: CLOSED
SCIENTIFIC_STATE: RESOLVED_WITHIN_SCOPE
TECHNICAL_STATE: PASS for de beskrevne eksakte kontroller
TARGET_Q: Q049
PROMPT_ID: BUBBLEVERSE.MATHEMATICS
PROMPT_VERSION: 2.2.0
RUN_ID: LOCAL-Q049-MATH-GLOBAL-INVARIANT-20261024-V2

NÆSTE MODTAGER: BUBBLEVERSE.RESULT_INGESTION_ROUTING2.2.0, som udtrykkeligt krævet af den konkrete V2-task, til registrering og vurdering af Q-closure. Det matematiske slutresultat er integrationsklart til Motor 14 uden ny undersøgelse, hvis indtagelsen ikke finder en konkret fejl.

## Dokumenteret svar

For den frosne `hillipop-ede_n3` latch/reset-definition og enhver af de arvede admissible source-real parvise fortsættelser, der når fra z=810 til z=0, er

\[
\boxed{\left|\Delta\tau_{T,\mathrm{tail}}\right|
=\left|\int_0^{810}W(z)\Delta x_e(z)\,dz\right|
\le 46.67050453.}
\]

Dette er en dimensionløs, deterministisk og konservativ grænse. Den gælder også absolutværdien af hvert delintegral fra0 til et z≤810. Fortegnet er ikke bestemt. Der er ingen positiv nedre grænse for den faktiske forskel i dette resultat; nul er tilladt.

Grænsen er meget grov: Den tillader en hydrogenforskel af størrelsesorden1. Den dokumenterer ikke epsilon-skaleret følsomhed, en lille fysisk effekt eller robustness af Q048. Den løser alene opgaven om en rigorøs endelig global øvre grænse inden for den accepterede betingede model. Det er ikke en ny komplet rekombinationshistorie, native tabel-/splinecertificering eller et eksistens-/entydighedsbevis for den faktiske native bane.

Ingen lav-z-bane er integreret. Beviset bruger et globalt invariant område og et analytisk integrerbart baggrundsenvelope. HMLA/SWIFT-beviset er ikke ekstrapoleret hen over den manglende Peebles-gren.

## Eksakt spørgsmål og inputgrænse

Q049 spørger:

> Under the frozen Q048 source/capture and fixed accepted z_reio, what rigorous upper bound can be placed on the remaining low-redshift contribution to |Δtau_T| over 0 <= z <= 810 for the hillipop-ede_n3 configuration between the event-resolved latch q=xHeII=10^-6 and the same-event reset q=0, using a correlation-preserving global stability/envelope analysis anchored at the validated z=810 frontier rather than reconstructing the full low-z x_e(z) trajectory cell by cell?

Question SHA-256: `56be0d72bb554c456221857e5ef29eb870455e6d48eeb244bd30f1ef33f003f3`.

Case: `LOCAL-Q049-FOCUSED-LOWZ-TAUTAIL-V1`; permanent videnskabelig registry-writeback afventer. TARGET_Q er Q049 med dokumenteret Q048-forhistorie. Ingen Q050+ eller ny ekstern observationsviden anvendes.

Frosset fysisk kilde: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`. Captured/config-objektet er `q048_prefix_config_v1.json`, SHA-256 `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`. V151-checkpointet er byteverificeret med SHA-256 `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`.

Ankeret er fortsat actual127/frontier810, a=1/811. V154 er ACCEPTED_UNCONSUMED; der er ikke oprettet actual128 eller udført en ny proof-/consumercelle. Q048 forbliver terminalt uløst. Denne analyse bruger Q049's egen fortsatte konto; ingen ny Q eller nulstilling.

Alle nye påstande nedenfor er DERIVED/INFERRED under de frosne modelpræmisser. Captured hex-værdier er interne computational inputs, ikke nye astronomiske målinger.

## Variable, domæne og arvet betingelse

Sæt h=xHII, q=xHeII=fHe*x_He og v=T_b/T_gamma=1-w. q er pr. hydrogenatom, så x_noreio=h+q. Efter den fælles hændelse er q_L=epsilon=10^-6 og q_R=0. Det residuale q-hold ændrer ikke den fælles kilde-reioniseringsfunktion.

Brug t=ln(811/(1+z)), T=ln811. Begge er dimensionløse, og t vokser mod fremtiden. Det accepterede z=810-checkpoint giver

\[
0<L\le h\le U<1,\qquad
v(0)\in[0.98,1.000001].
\]

Her er L=346752030166741/10^18 og U=99999/100000. Det er et tilladt startområde for begge grene, ikke et snævert parvist differenscertifikat.

Beviset gælder eksisterende admissible absolut kontinuert source-real løsninger under den fælles frosne baggrund og de specificerede kildefelter. Konklusionen på hele intervallet er betinget af, at sådan en admissibel fortsættelse når z=0. Der bevises ikke native/source-real-identitet, global eksistens, entydig selector eller en ny fuld baggrundsguard. Denne betingelse er arvet fra V151 og den eksplicitte V2-task; den indføres ikke for at gøre native resultater gyldige.

## 1. Positivt globalt baggrundsenvelope

Den frosne source bruger, for den captured flade konfiguration,

\[
H_{\rm CLASS}(a)^2=\rho_{\rm tot}(a),\qquad
\rho_b+\rho_c=H_{0,\rm CLASS}^2(\Omega_b+\Omega_c)a^{-3}.
\]

De øvrige aktive bidrag er ikke-negative. Photon-/ur-tætheder har positive captured koefficienter. Neutrinokvadraturen har positive q-noder, vægte, faktor, temperatur og masse, så dens energisum er positiv. Der er ingen aktiv fluid, negativ Lambda, dcdm, dr, IDM/IDR eller krumning i denne captured konfiguration.

Scalarens sourcepotentiale er

\[
V(\phi)=4152.39\,m^2 f^2[1-\cos(2.435\,10^{27}\phi/f)]^3
+B\,3.968\,10^{-8}\ge0,
\]

fordi captured eksponent er3 og B≥0. Dens kinetiske bidrag er et kvadrat. Det giver på hver eksisterende source-real baggrund

\[
H_{\rm CLASS}(z)\ge
H_{0,\rm CLASS}\sqrt{\Omega_b+\Omega_c}(1+z)^{3/2}>0.
\]

Dette er et algebraisk globalt envelope, ikke en rekonstruktion af scalaroscillationerne. Captured værdier er H0_CLASS≈0.0002291956336591 Mpc^-1 og Omega_b+Omega_c≈0.3087560339193. Positive faste koefficienter giver også en endelig øvre bound på den positive Thomson-kernel over det kompakte interval.

## 2. Hydrogenbarriere for alle relevante operatorer

Med nul injection kan både HMLA og SWIFT skrives som en sum af positive ratekanaler med fælles bracket

\[
s(1-h)(\alpha-\alpha_{eq})
+\alpha[h(h+q)-s(1-h)]
=\alpha h(h+q)-\alpha_{eq}s(1-h).
\]

Ved h=0 er bracket=-alpha_eq*s<0; den samlede h-derivativ har det modsatte fortegn og peger indad. Ved h=1 er bracket=alpha*(1+q)>0, så h-derivativet peger nedad. Peebles-feltet har præcis samme bracketstruktur med alpha_B og en positiv Peebles-C-faktor; den manglende kildegren fra V1 er derfor nu omfattet af barriereargumentet.

Positivitet af C-faktorerne antages ikke. Sæt

\[
G_s=B_0+3R+\Lambda,\quad G_p=B_1+R+A,
\]

hvor A er positiv Ly-alpha escape, eventuelt korrigeret i SWIFT. Da

\[
D=G_sG_p-3R^2
=(B_0+\Lambda)G_p+3R(B_1+A)>0,
\]

er C2s=(Lambda*G_p+3R*A)/D og C2p=(A*G_s+R*Lambda)/D positive. For Peebles er C=(3A+Lambda)/(3A+Lambda+B)>0. Alle alpha-/alpha_eq-/R-rater er positive: Source interpolerer endelige logtabeller og eksponentierer; de rå atomicnoder er kontrolleret positive. Peebles' alpha_B har en positiv numerator og denominator for T_b>0.

Escape indeholder tilsyneladende en singularitet ved h=1. De algebraiske C-ratioer har et endeligt positivt grænsetilfælde ved A→+infinity: C2p→1 og C2s→(Lambda+3R)/G_s; Peebles-C→1. Fortegnet ved h=1 forstås gennem denne kontinuerte source-real udvidelse. Da start h<1 og feltet peger strengt nedad i et nabolag af grænsen, kræver løsningen ikke en evaluering ved den native division med nul.

For SWIFT skal også 1+DK>0 være dokumenteret. Med de frosne fitdata og de genbrugte source-real initialparameterintervaller er en ny eksakt centreret cubic-envelope nedre grænse **1+DK≥0.7786672769011433…**. En separat, mere konservativ kolonneberegning giver **1+DK≥0.7321156914593853…**. Begge er positive. Cubicens L1-norm≤2 er kontrolleret med eksakte Bernstein-koefficienter på dens tre signintervaller. Der er ikke ekstrapoleret uden for fitdomænet: SWIFT vælges kun ved T_gamma≥1775K og her er T_gamma≤2210.3805K<4415K; under fitgrænsen bruger kilden HMLA eller Peebles.

P3-initialparameterintervallerne, herunder N_eff, genbruges som det eksisterende kvalificerede source-real grundlag. Der er ikke udført en ny native eksport af disse felter. Captured T0,nH0,YHe,fHe samt h,Omega_b*h² og (Omega_b+Omega_c)*h² er matchet til dette grundlag. De captured massive neutrinoer ligger under NFSM-tærsklen, så den anvendte NFSM-matterkombination stemmer med kildens regel. Gamle P3-programmer eller hele historiske testsuiter er ikke genkørt.

## 3. Samtidig temperaturbarriere og lovlige rateopslag

Den sene source-ligning er

\[
v'=-v+\beta(1-v),\qquad
\beta=A_C\frac{x_{reio}}{1+f_{He}+x_{reio}}\ge0.
\]

I området0≤h≤1, q≥0 er x_noreio≥0. Den fælles reio_camb-map er en konveks blanding af x_noreio og en positiv slutfraktion plus et ikke-negativt heliumbidrag. Derfor er x_reio≥0. Captured injection/varconst/IDM-termer er nul.

Ved den øvre flade v=1.000001 er v'<0. Ved den bevægelige nedre flade v_min(t)=0.98*exp(-t)≤1 er v'≥-v=v_min'. Sammen med hydrogenets indadrettede felter giver et simultant first-exit-argument

\[
0<h<1,\qquad
0.98e^{-t}\le v(t)\le1.000001.
\]

På hele intervallet er v≥0.98/811=49/40550>0. Der er derfor ingen forudsat fortsættelse af den gamle w≤0.02-boks til z=0.

Når den frosne wrapper vælger et atomic/HMLA/SWIFT-opslag, er v>0.1 og TR>0.004eV. Hvis v>1, er den reciprokke table-koordinat mindst1/1.000001>0.1; TR er altid under0.4eV på dette interval. Kildeopslagene ligger derfor i deres dokumenterede domæner. Når en af de lave grænser overskrides, vælges Peebles, som ovenfor har samme barriereretninger og er defineret ved alle strengt positive temperaturer.

Hvert aktivt felt og enhver af de tilladte konvekse HMLA/SWIFT-valg opfylder således de samme invariants. Et state-afhængigt valg behøver ikke være identisk i de to arme. Der anvendes intet differens-Jacobian hen over et skift, så ingen skjult selector-mismatch er droppet. Beviset forbliver betinget af de eksisterende admissible løsninger; det påstår ikke en eksistens-/entydighedssætning for den diskontinuerte native selector.

## 4. Elektronenvelope med fælles reionisering

For recombination-output er x_noreio=h+q. Det fælles frosne reio_camb-map har formen

\[
x_{reio}=(1-S)(h+q)+Sx_{after}+C_{He},\qquad 0\le S\le1.
\]

De sidste to bidrag er fælles og bortfalder præcist i differensen. Derfor

\[
|\Delta x_{reio}|
=(1-S)|h_L-h_R+\epsilon|
\le1+\epsilon=1.000001.
\]

For den sourcekontinuerte transition-smoothing på målintervallet er der ingen frec-entry-smoothing tilbage ved z≤810: Den slutter ved1500. Frec→reio-smoothing kan foregå nær z=50, men begge side-maps dér er identiske h+q, fordi den frosne reioniseringsstart er753585/65536≈11.4987946. Den samme envelope gælder derfor det kontinuerte sourcemap på hele målintervallet.

En senere native cubic-spline-repræsentation er ikke omfattet. Der er ikke antaget positive splinevægte eller en native fejlgrænse. Den anvendte continuum-tau-definition er netop den, V2-tasken fastlagde.

Denne fælles-input konstruktion antager ikke statistisk uafhængighed. Vi udvider blot den mulige parvise state-mængde konservativt til0≤h_L,h_R≤1; den faktiske korrelerede parbane er indeholdt deri. Afhængigheden i reioniseringsleddene fjernes ved eksakt fælles cancellation, ikke ved uafhængig intervaldivision.

## 5. Analytisk integreret Thomson-grænse og enheder

I SI er W=c*sigma_T*nH0*(1+z)^2/H_s og H_s=c*H_CLASS/Mpc. Dermed bortfalder c i envelopeudtrykket:

\[
W(z)\le
\frac{\sigma_T n_{H0}\,\mathrm{Mpc}}
{H_{0,\rm CLASS}\sqrt{\Omega_b+\Omega_c}}\sqrt{1+z}.
\]

Her er sigma_T i m², nH0 i m^-3, Mpc i m/Mpc og H0_CLASS i Mpc^-1, så produktet er dimensionløst. At indsætte H0_CLASS som km/s/Mpc ville være en enhedsfejl.

Integration giver den eksplicitte cap

\[
B=(1+\epsilon)
\frac{2\sigma_Tn_{H0}\,\mathrm{Mpc}}
{3H_{0,\rm CLASS}\sqrt{\Omega_b+\Omega_c}}
\left[811\sqrt{811}-1\right].
\]

Capturen giver nH0≈0.188062406329951m^-3. De frosne sourcekonstanter er sigma_T=6.6524616*10^-29m² og Mpc=3.085677581282*10^22m. Beregningen omslutter både de eksakte kildedecimaler og deres binary64-repræsentationer; det giver ikke en samlet native-programfejlgrænse.

Den eksakte udadrettede rationalberegning omslutter selve cap-formlen omkring46.67050452354706 og giver den sikkert oprundede cap46.67050453. Den lille bredde af dette **beregningsinterval for cap-formlen** siger intet om størrelsen eller præcisionen af den faktiske fysiske forskel, som kun begrænses af cap'en. De eksakte rationaler ligger i `Q049_V2_GLOBAL_BOUND_RESULT.json`.

## Validering, reproducerbarhed og stop

Kontrakten blev frosset før den nye talberegning: `Q049_V2_VALIDATION_CONTRACT.json`, SHA-256 `4e4bd31cb98cbdda100e84564c91829d79757954d92e117991c6d03bf253a11a`. Ingen smallness-/materialitetstærskel blev fastsat eller efterjusteret.

Producenten består46 checks. Radikaler omsluttes med integer square root på et10^40-gitter, med eksakt kontrol af de kvadrerede endepunkter. Den separate verifier består33 checks uden producentimport: manuel hex-rationaldekodning,150-step dyadisk bisection, en anden fitdenominatorbound og generelle eksakte polynomiumidentiteter for bracket-/C-faktor-beviserne. Begge beregningsveje beviser den samme rapporterede oprundede cap. De analytiske invariant-/first-exit-argumenter står fuldt ovenfor; ingen automatisk generel teoremprover påstås.

To korte producentkørsler gav samme rationaloutput. En ubrugt header-entry i kladden blev fjernet før den endelige verifier; faktisk headeridentitet var hele tiden kontrolleret mod det frosne Git-objekt. Første kode/råoutput er bevaret som kladdeprovenance. Der blev ikke ændret fysisk input, metode, tolerance eller resultat. Verifieren blev før endelig levering præciseret til et reelt polynomial-antiderivatcheck og eksakt intervaloverlap; tre verifierinvokationer, inklusive en ren ændring af kladde-reference til leveret fil, udgør ikke tre uafhængige støttebeviser.

Alle nye kontrolkørsler er lokale og tager under det prospektive300s-loft. Der er ingen native kørsel, IVP-integration, parameteroptimering, capture, likelihood eller HPC-kampagne. SymPy var ikke tilgængelig; ingen SymPy-resultat påstås. Kontrollerne bruger standardbibliotekets heltal og Fraction.

Uafhængighed er begrænset til separat implementation/beregningsvej under samme analytiker og frosne kildedata. R2 for den dokumenterede eksakte beregning og uafhængige algoritmekontrol; ingen uafhængig menneskelig eller empirisk reproduktion. Evidensstyrke er stærk for den anførte betingede matematiske cap og begrænset for spørgsmålet om en lille faktisk fysisk effekt.

G1–G7 er opfyldt for dette præcise betingede endpoint: identitet og input, fuldt invariant- og integralbevis, alle kildegrene, fælles output, udadrettet beregning og separat kontrol, samt fuld journal/provenance. Robusthed er analytisk over hele det tilladte tilstandsområde og alle relevante valg, ikke en samling nye seeds. Ingen native-/eksistensforudsætning er erklæret løst.

Den konkrete task kræver stop ved én valideret endelig cap; derfor startes ingen ekstra adjoint-skærpelse. Det ville besvare et yderligere spørgsmål om tightness, som denne levering ikke forudsætter. Der må ikke afvises en gyldig grov cap alene for at holde Q049 åben uden en dokumenteret materiel grund.

## Budget, journal og næste destination

RUN COST: 146 pts
USED: 322/1000 pts
REMAINING: 678 pts
BUDGET_STATE: ACTIVE — den matematiske opgave er afsluttet før budgetudtømning

Forrige saldo var176/824 fra ledgerV3. Forhåndsestimat160, maksimum220, reserveret220, faktisk vurderet146 og frigivet74. Breakdown: analyse62 + beregning/kode16 + søgning18 + validering26 + journal/provenance/levering24 =146. Point er et arbejdsregnskab, ikke målte credits, tokens eller kroner. Ingen tidligere charge er gentaget; ingen overrun. Ny ledger: `Q049_QUESTION_BUDGET_LEDGER_V4.json`.

Den fulde journal er `Q047_SAMLET_JOURNAL_Q049_V2_BOUND_APPENDED.md`, med alle14.865.746 indgående bytes som eksakt prefix og én ny matematikpost. Fuld kilde-/claim-/fejl-/budgethistorik bevares; gamle tests og alle historiske links er ikke genverificeret. Støttefilerne er ikke en parallel journal.

Ruteafgørelse: Den specifikke task kræver én retur til Result Ingestion2.2.0. Den følges før matematikkens generelle Motor14-slutskabelon: Modtagermotoren skal importere dette resultat og146point én gang, kontrollere Q049-closure inden for dette scope og sende sagen til Motor14, hvis der ikke er en konkret fejl. Der bestilles ingen ny undersøgelse. Det ændrer ikke den matematiske slutstatus, og det giver ikke næste motor et nyt budget.

MODEL_DIFF: Ingen ændring af accepted model eller Q048's uløste konklusion. Tilføj kun den betingede Q049-cap og dens begrænsede informationsværdi. Globale konsekvenser tilhører Motor14. En eventuel senere opgave om epsilon-skaleret eller stram fysisk følsomhed skal identificeres særskilt; denne levering aktiverer ingen ny Q eller budgetkonto.

Faktisk setup: Codex, lokal Python/Fraction, filer og GitHub-read; konkret model-/reasoning-indstilling ikke verificeret. Ingen subagents/modelskift. Anbefalet modtagerprofil er almindelig dokumentarisk indtagelse med fokuseret matematisk vurdering; ingen dyr computation er nødvendig uden en påvist fejl.

GitHub: inspiceret projektgrundlag `dc647a7975193b8ce3ad7a84564dd61c7317ccea`. Ny journal/task fra indtagelsen er til stede; maskinledgersV2/V3 mangler fortsat i den inspicerede trævisning, men de gemte verificerede successorer og den uploadede journal stemmer. Kontoen er derfor videreført322/678, ikke nulstillet fra repoets gamle ledgerV1. Nye filer er READY_FOR_MANUAL_UPLOAD; intet push, commit, PR eller dispatch påstås.

## Primære kilder og provenance

- Frossen [background.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c), omkring430–585 og3010–3028: matterled, positive energibidrag og scalarpotentiale.
- Frossen [hydrogen.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c),68–109,350–419,425–549 og1058–1077: Peebles/HMLA/SWIFT og rateinterpolation.
- Frossen [wrap_hyrec.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c), omkring132–141: modelvalg; V1's temperaturtrigger er genbrugt, ikke genberegnet som ny viden.
- Frossen [thermodynamics.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c),1190–1212,2625–2760,2960–3000 og4153–4180: reioniseringspositivitet, temperatur, smoothing og fælles map.
- Frosne background.h/thermodynamics.h: sourcekonstanter og enheder. Fit-/atomicdata er bytekontrolleret ved de bevarede sourcehashes.
- V151-checkpoint, capture/config og P3's kvalificerede source-real initialparameterintervaller: intern computationalevidens under den samme frosne kilde. Ingen ny native identitetsvurdering.

Komplet anvendt inputinventar, versionsreferencer og beregnede hashes står i `Q049_V2_INPUT_PROVENANCE.json`. Ingen ny ekstern observation eller bibliografisk identifikator er opfundet.
