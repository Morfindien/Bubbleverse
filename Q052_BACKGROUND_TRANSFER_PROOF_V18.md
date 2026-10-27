# Q052 V18 — direkte residualbevis uden native-baggrundsmedlemskab

Denne udledning gælder den definerede rekonstruktion af de gemte native tilstande. Den etablerer en tilstrækkelig bevisvej for dens afstand til det betingede Q051-kildeflow. Den færdiggør ikke den numeriske fejlgrænse og beviser ikke medlemskab for den oprindelige native baggrund.

## 1. Målobjektet og de bevarede kvantorer

Q051's operative udsagn er ikke en udpegning af én beregnet baggrundstabel. Det fulde V7-bevis, §1, siger:

> Fasthold én vilkårlig allerede admitted fælles baggrund fra den frosne hillipop-ede_n3-familie, defineret på 0≤z≤810. Fasthold ét valideret startpar (h0,v0), identisk for alle q∈[0,10⁻⁶].

Samme bevis, §3.1, beskriver den faste baggrund som et admitted glat kilde-real medlem. Q050-bindingen bruger tilsvarende kvantoren `every_fixed_admitted_background_in_retained_connected_frozen_capture_family`. Den beviser ikke, at familien er ikke-tom. Native/P6-identitet er udtrykkeligt uden for Q051's konklusion.

Lad derfor \(\mathcal A\) være netop denne arvede, betingede klasse. Fasthold **samme** \(B\in\mathcal A\) i begge helium-arme og gennem hele cellen. Alle nedenstående estimates er uniforme i dette faste valg. Brug af projektionsintervaller i en ulighed vælger ikke en ny fysisk baggrund ved hvert tidspunkt.

De tre objekter holdes adskilt:

| Objekt | Definition og status |
|---|---|
| \(B\) | Allerede admitted kilde-real baggrund. Der indføres ikke en ny kosmologisk IVP eller et nyt familiemedlem. |
| \(S\) | Real-aritmetisk spline gennem en bestemt native baggrundstabel og dens lagrede andenafledte. Tabelidentiteten er ikke etableret her. |
| \(\mathrm{fl}(S)\) | Den historiske floating-point evaluering, inklusive logaritme, opslag og afrunding. Den er ikke identisk med \(S\) ved definition. |

Det uændrede Q052 kræver fortsat en forsvarlig relation mellem faktisk native historik og de bogstavelige kilde-real ligninger under de frosne præmisser. At få en betinget fejlgrænse for en rekonstruktion er ét led i dette krav, ikke automatisk hele svaret.

## 2. Første celles aktive felter

Brug

\[
u=\log\frac{811}{1+z},\quad x=-z,\quad
y=(h,v),\quad v=1+\frac{D}{T_0(1+z)}.
\]

Cellen er fra \(z=810\) til den eksakte binær64-knude
\(7122042588453929/8796093022208\), vist som809.6825. Fase5 er `frec`, `require_H=1`, `require_He=0`. Frosne flags udelukker varierende konstanter, injection og de aktive IDM-led. Før reionisation er \(X=h+q\).

I den relevante `thermodynamics_derivs`-gren afhænger feltet af Hubblefeltet og fotontætheden. `H_prime` bruges kun i den tidligere steady-state-gren, som ikke er denne fase. Hydrogenkernen og den her aktive termiske ligning er

\[
h'=f_q(u,h,v;H_s,\theta),\qquad
v'=-v+A(u,h,q;B)(1-v),
\]

\[
A=\frac{K_\gamma\rho_\gamma}{H_s}\frac{h+q}{1+f_{He}+h+q},\quad
K_\gamma=\frac{2\sigma_T}{m_e c}\frac43 J_{\mathrm{Mpc}},\quad
H_s=\kappa H_{\mathrm{CLASS}},\quad \kappa=c/\mathrm{Mpc}.
\]

Her er \(\rho_\gamma=\Omega_\gamma H_0^2(1+z)^4\) for det frosne kilde-real mål. \(J_{\mathrm{Mpc}}\) er kildens konvertering fra CLASS-tæthed til J/m³. \(n_H=n_{H0}(1+z)^3\), med SI→cm³-konvertering i HyRec. Der sættes ingen ekstra c-faktor ind i et Mpc⁻¹-udtryk.

Det følger, at **hverken H's tidsafledte eller den native H′-kolonne er nødvendig for den direkte første-celle-residual**. Dette er ikke en påstand om alle senere faser eller alle observableberegninger.

På den definerede rekonstruktion er

\[
\widehat h'=(1+z)\widehat h_x,\qquad
\widehat v'=\widehat D_x/T_0+\widehat v-1.
\]

Disse relationer er kinematiske identiteter for den definerede kurve, ikke brug af native H′.

## 3. En faktisk kontrolleret branchekasse

Udvid V14/V17's eksakte h- og v-rekonstruktionsgrænser med de faste diagnostiske radier \(10^{-5}\) og \(10^{-4}\). Dette er en kasse til branchekontrol; en løsningsbane er endnu ikke bevist at blive i den.

Q050's indeholdende810→800-celle giver

\[
H_{\mathrm{CLASS}}\in
\left[
\frac{1580426358065720928530117}{500000000000000000000000},
\frac{4480552533941654713}{1000000000000000000}
\right]\ \mathrm{Mpc}^{-1}.
\]

Det nye finite check evaluerer den bogstavelige Pion-formel med rettet MPFR-aritmetik på **hele** denne H-projektion, hele første celle og hver udvidet h-kasse. Skriftlige decimal-konstanter og deres binær64-literal-konverteringer omsluttes begge. Resultat:

| Arm | Pion, vist med almindelige decimaler | \(99B_{ion}-L-3R_\alpha\), s⁻¹ |
|---|---|---|
| L | [0.20525121932371077,0.23022562325433865] | [352.6256280126322,357.3262632262054] |
| R | [0.20525121932371077,0.23022562326124946] | [352.6256280126322,357.3262632266925] |

Autoritative rettede endpoints står som hex i receiptet. Pion er strengt over den originale grænse0.01. Desuden er TR over0.004eV og under0.4eV, v ligger strengt mellem0.1 og1, og Tγ ligger over SWIFT-fitfilens første temperatur1775K. Den oprindelige dispatcher vælger derfor cold/SWIFT på disse diagnostiske kasser. Ingen equality-regel ændres. De observerede endpoint-dispatches er ikke brugt som bevis for hele cellen.

Det er et nyt betinget branchecertifikat. Det er **ikke** en tube-closure, et interval for den fulde RHS eller et nyt source-real løsningscertifikat.

## 4. Direkte defektsætning

Lad \(\widehat y\) være V14's eksakt definerede AC-rekonstruktion på \([0,T]\), og sæt
\(W=\operatorname{diag}(1/\rho_h,1/\rho_v)\), med positive faste radier. Betragt røret

\[
\mathcal T(u)=\{y:\|W(y-\widehat y(u))\|_\infty\le1\}.
\]

Antag på dette rør og alle relevante eksisterende \(B\in\mathcal A\):

1. Samme bogstavelige gren gælder, og alle kilde-denominatorer/tabeldomæner er kvalificeret.
2. \(F_q\) er lokalt Lipschitz i y, uniformt med
\(\|W\partial_y F_q W^{-1}\|_\infty\le L\).
3. Hele rekonstruktionskurvens defekt omsluttes med
\(\|W(\widehat y'-F_q(u,\widehat y;B))\|_\infty\le d\).
4. Den oprindelige målstart har
\(\|W(y_0-\widehat y(0))\|_\infty\le E_0\).

Da opfylder fejlen før en mulig første tube-exit

\[
E(u)\le E_0e^{Lu}+d\phi_L(u),\quad
\phi_L(u)=\begin{cases}(e^{Lu}-1)/L,&L>0,\\u,&L=0.\end{cases}
\]

Hvis det rettede loft ved \(T\) er strengt under1, kan en første exit ikke forekomme. Dermed gælder boundet på hele cellen. Beviset er integraluligheden for \(e=y-\widehat y\), efterfulgt af Grönwall og første-exit-kontinuitet. Fortsættelse inde i et kompakt kildefineret rør følger af de samme lokale feltforudsætninger; det beviser ikke baggrundseksistens.

Vigtigt: antagelserne indeholder **ikke** \(S\in\mathcal A\). F er evalueret mod hvert fast admitted mål direkte. Native solver-, tabel- og afrundingsafvigelser fra dette mål fremtræder i den registrerede kurves defekt. De må ikke bagefter tælles én gang til som en identisk ekstra fejlpost. Fejl i selve den validerede proof-evaluator skal derimod omsluttes i d; den må aldrig antages nul.

En fuldt gyldig implementation kan derfor evaluere intervallet

\[
\mathcal D_j=\widehat y'(U_j)-
F_q(U_j,\widehat y(U_j);H(U_j),\rho_\gamma(U_j),\Theta)
\]

på en endelig rationel underdeling af første celle og sætte
\(d=\max_j\sup\|W\mathcal D_j\|_\infty\). Afhængighedstab gør dette grovere, ikke ugyldigt. Det er ikke tilladt at bruge feltværdier kun ved gemte knuder som whole-cell d.

**Denne sætning og de leverede data er en tilstrækkelig konstruktion. d, L og den strenge closure-ulighed er endnu ikke evalueret.**

## 5. Alternativt residualbudget og en eksplicit beta

Vælg en vilkårlig positiv hjælpefunktion \(\widehat H\), eksempelvis V16's definerede H-Hermitekurve. Den behøver ikke være den native log(a)-spline. Brug samme fotontæthed og faste kildeparametre i hjælpefeltet. Sæt

\[
r=\|W(\widehat y'-F_q(u,\widehat y;\widehat H))\|_\infty,
\quad
\beta=\sup_{B\in\mathcal A}\|W(F_q(u,\widehat y;B)-F_q(u,\widehat y;\widehat H))\|_\infty.
\]

Et sound intervalregnskab giver \(d\le r+\beta+a_{eval}\), hvis r og beta er beregnede matematiske størrelser, og a_eval indeholder den resterende evaluatorusikkerhed. Hvis deres intervalevaluering allerede omfatter denne usikkerhed, bruges den ikke endnu en gang. Det direkte d-budget i §4 er normalt enklere.

### 5.1 Reciprocal H

Fra hele cellens admitted H-projektion og hjælpekurvens Bernstein-kontrolgrænser \(\widehat H\in[\hat l,\hat u]\) fås præcist

\[
H_{\mathrm{CLASS}}^{-1}-\widehat H^{-1}
\in[H_U^{-1}-\hat l^{-1},H_L^{-1}-\hat u^{-1}].
\]

For begge arme er det kontrollerede absolutte loft

\[
\delta w_{\mathrm{CLASS}}\le
\frac{2719749397929188898422419677773824}
{33019691606079689570869247429145235}\ \mathrm{Mpc}
\approx0.08237\ \mathrm{Mpc}.
\]

Dette er et konservativt **betinget mismatch til hjælpekurven**, ikke en målt native baggrundsfejl. For \(w=H_s^{-1}\) er \(\delta w=\delta w_{\mathrm{CLASS}}/\kappa\), med enhed sekunder.

Den termiske beta opfylder direkte

\[
|\Delta g|\le
K_\gamma\rho_\gamma
\left|\frac{h+q}{1+f_{He}+h+q}(1-v)\right|\delta w.
\]

Dette komponentloft er faktisk evalueret på rekonstruktionskurven: højst0.26852429992544813 for L og0.2684851439208496 for R pr. enhed u. De autoritative rettede hex-endpoints står i receiptet. Dette er en grov betinget v-komponent af feltmismatch til hjælpekurven, ikke den fulde beta og ikke en propagateret temperaturfejl. Et fysisk temperaturudsving på denne størrelse er ikke målt eller udledt.

### 5.2 SWIFT-kernens præcise H-afhængighed

På et fast u,h,v,q sættes \(j=R_{2p2s}>0\), \(\lambda=L_{2s1s}>0\), \(b_s=\Beta_s>0\), \(b_p=\Beta_p>0\), og \(e\) er fitted escape rate. Sæt

\[
A=b_s+3j+\lambda,\quad B=b_p+j,\quad
D_0=AB-3j^2>0,\quad D_1=A,
\]

\[
e=k/w,\quad k=\frac{\mathrm{LYA\_FACT}}{n_H(1-h)(1+DK)},\quad
U_i=\alpha_i h(h+q)-\alpha_{i,eq}s(1-h).
\]

Den arvede source-real denominator-kvalifikation kræver \(1+DK>0\). For denne klasse er

\[
C_s=\frac{\lambda B+(\lambda+3j)e}{D_0+D_1e},\quad
C_p=\frac{\lambda j+Ae}{D_0+D_1e},\quad 0<C_s,C_p<1.
\]

Dermed, med \(V_0=U_s\lambda B+U_p\lambda j\) og \(V_1=U_s(\lambda+3j)+U_pA\),

\[
f=-n_Hw\frac{V_0w+V_1k}{D_0w+D_1k},
\]

\[
\partial_wf=-n_H\left[
\frac{V_0w+V_1k}{D_0w+D_1k}
+\frac{wk(V_0D_1-V_1D_0)}{(D_0w+D_1k)^2}
\right].
\]

Et interval for dette udtryk giver \(|\Delta f|\le\sup|\partial_w f|\delta w\). Samme faste params og atomtabeller skal bruges i begge feltled. En samplet DK eller et positivt endpoint er ikke en denominator-kvalifikation over en boks.

Der findes også et grovere, men nyttigt parameterfrit loft. En af C-fraktionerne er en Möbius-funktion af e med endpointværdier i[0,1], så

\[
|e\partial_eC_i|\le1/4,\qquad
|\partial_w f|\le\frac54n_H(|U_s|+|U_p|).
\]

Dette følger ved \(t=D_1e/D_0\) og \(t/(1+t)^2\le1/4\). Det kræver den arvede positive-escape/domænepræmis; det tillader ikke vilkårlig negativ DK. Det giver en eksplicit beta uden at kende en specifik native H-tabel eller vælge en bestemt DK-værdi.

### 5.3 Tilstrækkelige state-Jacobianlofter

Da C_i på denne cold/SWIFT-gren er uafhængig af v, og e_h=e/(1-h), er

\[
|\partial_hC_i|\le\frac1{4(1-h)}.
\]

Derfor kan en konservativ intervalimplementation bruge

\[
|f_h|\le\frac{n_H}{H_s}\sum_i
\left[\alpha_i(2h+q)+\alpha_{i,eq}s+\frac{|U_i|}{4(1-h)}\right],
\quad
|f_v|\le\frac{n_H}{H_s}h(h+q)\sum_i|\partial_v\alpha_i|.
\]

For g er \(g_v=-(1+A)\) og

\[
g_h=\frac{K_\gamma\rho_\gamma}{H_s}
\frac{1+f_{He}}{(1+f_{He}+h+q)^2}(1-v).
\]

Disse bounds giver den krævede vægtede infinity-Jacobiannorm ved
\(L=\max_i\sum_j|J_{ij}|\rho_j/\rho_i\). Alle værdier skal evalueres over hele røret. Der påstås ikke et tal for L her.

## 6. Initialkonvertering og hvad nul betyder

Den leverede opgave fastholder de fangede nominale h,D-starts. Definér derfor det betingede målstartpar i samme koordinater som rekonstruktionen:

\[
h_0=\frac{4651594516923411}{1152921504606846976},\quad
v_0=1+\frac{D_0^{capt}}{811T_0}
=\frac{9947469393499555215}{9954668796147009946}.
\]

L/R er præcist matchede. De ligger i Q051 V2's angivne initialklasse: \(0\le h_0\le99999/100000\), \(.98\le v_0\le1.000001\). For et mål med disse **samme eksakte koordinatstarts** er E0=0 i §4 ved definition og eksakt endpoint-interpolation. Der er ikke sat en ukendt numerisk native-fejl til nul. Det er ikke et bevis for native integration før810 eller for en anden, uoplyst initialkonvention.

Den gemte native ratio er ikke helt den samme rationelle konvertering: forskellen vises eksakt i receiptet. Tilsvarende er det reale produkt af gemt fHe og xHe i L-armen ikke nøjagtigt10⁻⁶. Når det direkte felt i §4 evalueres ved det **eksakte fysiske mål-q**, omsluttes parameter-/konverteringsvirkningen i den samlede defekt. Bruges et hjælpefelt ved en anden q, skal dens forcing-budget tilføjes eksplicit. Ingen q-ændring eller refit udføres.

## 7. Hvorfor native-tabellen er et særskilt evidenskrav

Hvis man specifikt vil rekonstruere eller validere S, kræves første celles relevante log(a)-knuder, H- og fotontæthedskolonner, deres d²/dlog(a)²-værdier og indeks-/strideidentitet, eller et verificeret alternativ, der bestemmer dem. For netop denne aktive RHS behøves ikke H′-kolonnen. En validator må også håndtere logaritme og floating-point evaluator, hvis claimet omfatter den historiske fl(S).

Den faktiske real-aritmetiske splineformel er, for \(\ell\in[\ell_j,\ell_{j+1}]\),

\[
S(\ell)=aY_j+bY_{j+1}
+\frac{\Delta^2}{6}\big[(a^3-a)M_j+(b^3-b)M_{j+1}\big],
\quad b=\frac{\ell-\ell_j}{\Delta},\ a=1-b.
\]

Da \(\ell=\log a=u-\log811\), er \(d\ell/du=1\), og

\[
S_u=\frac{Y_{j+1}-Y_j}{\Delta}
+\frac\Delta6\big[-(3a^2-1)M_j+(3b^2-1)M_{j+1}\big].
\]

Dette er splinekolonnens afledte. Den separat interpolerede H′-kolonne er ikke sat lig dette udtryk. Segmenter og deres boundaries skal medtages, hvis S faktisk bruges i et senere proof.

To endpointværdier og separat lagrede H′-værdier bestemmer ikke en kubisk H-spline: til en positiv lineær kurve kan føjes \(a\,s(1-s)\) uden at ændre endpoints. Det er et informations-eksempel, ikke et alternativt admitted kosmologisk medlem. De fulde eksisterende traces indeholder flere punkter; de kan i særlige, verificerede knotkonfigurationer indsnævre eller bestemme et polynomium. Dette dokument beviser derfor **ikke**, at samtlige historiske traceoplysninger er utilstrækkelige under enhver ekstra kildeforudsætning.

Kilden genererer en uniform log(a)-grid fra den faktisk beregnede loga_ini til0. Precision-parameteren alene fastslår ikke alle historiske floating-point knotbytes og kolonnekoefficienter. Selv en bestemt S er endnu ikke bevis for \(S\in\mathcal A\). En sådan native admission/IVP-fejlkvittering er stadig uløst, men den er ikke en nødvendig forudsætning for sætningen i §4.

## 8. Endelig, ikke-gentagen implementation

Den næste nye beregningskerne skal evaluere d og L for den direkte sætning, med de allerede leverede source-/tablebytes. Den skal forsøge streng closure på denne ene celle og én eksplicit norm. Begynd med0<C_i<1 og de positive denominatorpræmisser som arvet fra det tilladte domæne; hvis dette er for groft, må de faktisk kvalificerede SWIFT-fitparametre og C-intervaller indsnævres. En bred boks, der ikke lukker, er et metode-INCONCLUSIVE, ikke fysisk FAIL.

Atomtabellerne Alpha_inf.dat og R_inf.dat samt fit_swift.dat er genfundet ved det frosne physics-commit og følger med som præcise bytes. Rateinitialisering, log/exp/pow, stencilgrænser og afledte skal omsluttes; native libm antages ikke korrekt afrundet. C-faktorgrænser kræver fortsat den arvede admitted domænekvalifikation. Det gamle z≤50-fysikmodul må ikke kaldes som z810-evaluator.

Stop med et faktisk første-celle d/L/E-receipt eller den første konkrete manglende felt-/domæneforpligtelse. Gentag ikke V16's hardkodede manglende-native-receipt-gate. Hele domænet, eventhåndtering, output-smoothing, xe-/tau-observable transfer og native-baggrundsidentitet er fortsat nødvendige separate led før fuld Q052-afgørelse.

## 9. Validering og kilder

Den nye reproducerbare kode bruger det uændrede scalar-I-lag med MPFR4.2.1,256bit,RNDD/RNDU. Den beregner branche-/koordinat-/reciprocal-grænser,24 eksakt-rationelle cases af den oprindelige C-formel mod den omordnede formel og dual-differentierede w-afledte samt2 separate100-cifrede Decimal-readbacks. De finite cases kontrollerer implementationen af algebraen; det generelle argument er den symbolske omskrivning ovenfor. De er ikke24 fysiske kørsler eller en uafhængig kosmologisk reproduktion.

Den uafhængige del er alternativ exact-rational dual-differentiering af den oprindelige C-form og separat Decimal-aritmetik for reciprocal-endpointet. Alle kontroller deler frosne kilder og præmisser. Ingen ekstern proof-review eller formel teoremprover er brugt. V16's17 tests og alle gamle Q048–Q051-producenter er ikke genkørt.

- Q051 V7 fuldt globalbevis: Library-ID `libfile_b4c24cfa6e6c8191b8f9e7a9130f83e7`, læst§§1–9. Genbrug af betingede kvantorer og startklasse, ikke genbevis af global stabilitet.
- Q051 V7 afhængighedsbundle: `libfile_242bad27c6d88191891e9ae1f23e1e5c`; V2-startklasse og den arvede positive-escape/source-domænepræmis læst. Ingen fremtidig Q importeret.
- Q050 binding/receipts og Q048 capture/checkpoint ligger byteidentisk i V18-inputfilens V17-forælder.
- [background.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c),132–210,425,1940–1965: splineobjekt, fotontæthed og gridkonstruktion.
- [thermodynamics.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c),2576–2809: aktive feltgrene og fortegn.
- [hydrogen.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c),429–488,1048–1077; [wrap_hyrec.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c),103–139: felt og bogstavelig dispatch.
- Native splinekolonnernes interpolation: [arrays.c](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c),2504–2567. H′ er ikke automatisk spline-H's afledte.

MODEL_DIFF:NONE for accepted model. Ny betinget fejlbeviskonstruktion og branchekontrol; den fulde numeriske kilde-real certificering er stadig uafklaret.
