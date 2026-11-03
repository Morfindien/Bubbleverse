# Q052 · Fase 6 og elektronloftet

**BUBBLEVERSE — OVERLEVERING**  
Matematikmotor 2.3.0 · V79 · 3. november 2026

For den fastlagte model og det fælles baggrundsforløb B★ er den absolutte forskel mellem de to kildeløsningers elektronfraktion højst én elektron pr. million hydrogenkerner i to adskilte områder. Sæt

- $z_A=408663367683441/8796093022208\approx46,459646$,
- $z_B=787504997847845/140737488355328\approx5,595560$.

| Område | Hvad er dokumenteret? |
|---|---|
| $[z_A,810]$ | Maksimum er præcis $10^{-6}$, alene ved 810. V79 føjer 236 hele intervaller til beviset fra V75 og V77. |
| $[0,z_B]$ | Den absolutte forskel er højst $9,8840\times10^{-7}$, afrundet opad. Det følger af 373 hele intervaller fra V64 efter reionisationens omregning. |
| $(z_B,z_A)$ | Det skarpe mål på $10^{-6}$ er åbent. De arkiverede helcellebokse giver på dette mellemstykke højst $0,00128477$, afrundet opad. |

Det nye resultat angår løsningerne af kildeligningerne under de arvede Q048-, V62-, V64- og V73-forudsætninger. V78 gav en øvre grænse på 0,00092647 for den største absolutte forskel i akkumuleret Thomson-optisk dybde på hele historien. V79 har ikke genberegnet den. Den nøjagtige Thomson-maksimumværdi og den samlede sammenligning med det interpolerede CLASS-output står fortsat åbne.

## Hvilken elektronfraktion indgår hvor?

Brug $u=\ln[811/(1+z)]$, som vokser langs forløbet, og $v=T_m/T_\gamma$. For venstre arm er den interne elektronfraktion $X_L=h_L+q$, for højre arm er $X_R=h_R$, hvor $q=10^{-6}$ og $h$ er hydrogenets ionisationsfraktion. I den fastlagte konfiguration er eksotisk energiinjektion slået fra. Hydrogenligningen bruger den interne elektronfraktion. Temperatur og offentlig elektronfraktion bruger den reioniserede værdi $M(X)=\lambda(z) X+b(z)$. Begge arme har samme $\lambda$ og $b$. Den observerbare modeldifference er derfor $\lambda(h_L-h_R+q)$.

Over $753585/65536$ er kortet identiteten. Ved selve grænsen og under den bruges CAMB-grenen. Her er $\lambda=(1-\tanh A)/2$ med det fælles hydrogenargument $A$ fra koden. Heliumleddet er additivt og fælles. V64 deler ved grænsen og indhyller også den særskilte endepunktsværdi. I udglatningsområdet $46<z\le50$ bruger fase 5 og 6 samme $h+q$ ved samme tilstand. En vægtet blanding ændrer derfor ikke kildeobservablen dér.

Skriv $S$ for Saha-leddet og $n_H,H$ for de positive fælles faktorer i HyRec-enheder. På HMLA-grenen er $h'=-(n_H/H)\sum_i C_i[\alpha_i(v)hX-\alpha_i(1)S(1-h)]$. På Peebles-grenen anvendes samme udtryk med én PPB-rate og én Peebles-faktor med fudgefaktor 1. Temperaturfeltet er $v'=-v+A(M(X))(1-v)$ med $A(x)=k x/(1+f_{He}+x)$, hvor $k>0$ er fælles. Kildehenvisninger findes nederst.

## Fra 50 til det første mulige grenskift

Sæt $d=h_L-h_R$, $y=(h_R+q)(v_L-v_R)/(qv_L)$ og $B=199/200$. Vi afprøver $-2q\le d\le0$ og $|y|\le B$. Ved 50 giver V77 streng indgang og $|y|<0,99$. Den lidt bredere temperaturgrænse gør det muligt at nå hele vejen til første mulige skift.

Begge arme bruger HMLA i de første 236 celler. Hver helcelle opfylder $h>2q$ og $0,1<v<1$. Den største øvre grænse for temperaturens tvangsled, $(h_R+q)(1-v_R)/(h_R-q)$, er under 0,99054 og dermed under $B$. På hele dette område giver de to HMLA-tabeller $-1<\partial\log\alpha_i/\partial\log v<0$. Primærberegningen indhyller hver nødvendig stencil i begge koordinater. En separat omskrivning i Bernstein-basis kontrollerer 4.992 koefficientintervaller på 78 hele tabelstykker, inklusive endestenciler. Desuden gælder $S<h_R^2$, så højre hydrogenfelt er negativt.

Med $x=q/(h_R+q)$ giver hældningsgrænsen $1-Bx\le\alpha_L/\alpha_R\le1+Bx$. Ved $d=0$ gælder $(h_R+q)(1-Bx)>h_R$ og C-faktorerne er ens, så $d'<0$. Ved $d=-2q$ gælder $(h_R-q)(1+Bx)<h_R$. C-faktoren i L er højst C-faktoren i R, fordi escape-raten vokser med $h$. Det giver $d'>0$ som i V77. De to temperaturflader peger indad, fordi $h_R'<0$ og tvangsleddet er mindre end $B$. Første-kontakt-argumentet fra V77 bevarer derfor de strenge uligheder til og med $z_A$. Alle tidligere kontrolbokse er genbrugt uden at nulstille startforskellen.

## Hvor metoden standser

Den næste arkiverede celle går fra 46,45964596 til 46,44464446. På dens midtpunkt, $z\approx46,45214521$, vælges følgende punkt på den øvre flade $d=0$:

| Størrelse | Venstre arm | Højre arm |
|---|---:|---:|
| $h$ | 0,001 | 0,001 |
| $v$ | 0,099999 | 0,100001 |
| Kildegren | Peebles | HMLA |

Punktet ligger i begge relevante helcellebokse og opfylder $y=-2002/99999$. Temperaturforholdene ligger på hver sin side af 0,1. Strålingstemperaturen er over den nedre tabelgrænse, og SWIFT-fittemperaturen er ikke nået. Valget af grene følger dermed af den bogstavelige kildekode. På den øvre flade kræver metoden $d'\le0$. Direkte indsættelse, med udadrettet afrunding og C-faktorer indhyllet for alle positive escape-rater, giver derimod

$$
0,33670744 < d'/|h_L'| < 0,33670746.
$$

For at kontrollere fortegnet separat genopbygger kontrolprogrammet HMLA-raten fra de rå decimaltabeller med en anden interpolationsform. Det bruger en nedre grænse for højre tab og en øvre grænse for venstre tab og får $d'/|h_L'|>0,3367$. Fortegnet er dermed bestemt. Den brede indeslutning tillader en tilstand, hvor feltet peger udad. Om de matchede starttilstande kan føre til dette punkt, er ikke bevist. At feltet peger udad dér er derfor ikke et modeksempel til den faktiske elektronkurve.

## Den lave ende og de senere skift

For hver arkiveret celle indhyller V64 begge hydrogenfraktioner og den fælles kortfaktor. Ved at kombinere endepunkterne for $q+h_L-h_R$ med endepunkterne for $\lambda$ kan produktet afgrænses direkte med eksakte brøker. Fra nul tilbage til $z_B$ består 373 sammenhængende celler. Deres største arkiverede absolutte øvre grænse er $4667583517324017/4722366482869645213696$. Den tilstødende celle har et bredere interval. Det lokaliserer grænsen for denne kontrol. Der er ikke vist en overskridelse i nabocellen.

De to tætliggende arkivgrænser omkring $z=16,03101084$ indhyller strålingstemperaturens grenskift. Selve reionisationsgrænsen ligger ved $z=11,4987945556640625$. Alle tre koordinater findes som cellegrænser. Fortsættelsen fra $z_A$ gennem disse hændelser er fortsat åben. Kontrollens lave del hviler direkte på V64-boksene og kræver ingen fortsættelse gennem det uløste område.

## Overdragelse

Resultatindtags- og routingmotor 2.3.0 modtager det delvise bevis og det lokaliserede problem. En konkret næste test er at afgrænse den faktisk opnåelige afstand $-d$ til den øvre flade, når den første arm når $v=0,1$, og det maksimale akkumulerede udadrettede bidrag, indtil den anden arm har skiftet. Udelukkes det blandede grenskift allerede af skarpere temperaturbokse, kan overdragelsen også godkendes med dette bevis. Begge udfald skal følge fra de matchede startdata. En ukorreleret bokskombination afgør ikke spørgsmålet.

**Evidens.** Se result.json og control.json for eksakte brøker, og PROOF_V77.md for første-kontakt-argumentet. De centrale kodepassager er thermodynamics_derivs og thermodynamics_reionization_function i thermo.c, hyrec_dx_H_dz i wrap_hyrec.c samt rec_TLA_dxHIIdlna, rec_HMLA_dxHIIdlna og interpolate_rates i hyrec.c. De fastlagte kildefiler og tabeller findes med deres identiteter i v19.json. Kildecommit er 5a131c91d657dd9a7c6364cc45b038710f8d0d97.
