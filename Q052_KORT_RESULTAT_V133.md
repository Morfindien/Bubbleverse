# BUBBLEVERSE — OVERLEVERING

**Q052 · V133 · 22. november 2026**  
Status er FORTSÆTTER. Workflow er READY_FOR_HANDOFF, den tekniske kontrol har bestået (PASS), og det videnskabelige hovedspørgsmål står åbent (INCONCLUSIVE). Runden bruger Matematikmotor 2.3.0 og evidensen for Q052 til og med V132. Næste motor er **Resultatindtag og routing 2.3.0**.

## Resultat

Fejlloftet for forskellen mellem det gemte CLASS/P6-pars optiske dybde og kildeligningernes parforskel falder **2,19 %**. Over hele intervallet fra z = 0 til 810 er det nye loft **2,15627 × 10⁻⁵**, afrundet opad. Det gælder på den fælles fastlagte baggrund B★ med de matchede startdata. Størrelsen er dimensionsløs. Det signerede interval er [−2,15627 × 10⁻⁵, +1,92807 × 10⁻⁵], afrundet udad.

De 106 arkiverede bidrag ved z = 700–750 giver samme sum i en fremadgående og en baglæns kontrol. Lokalt falder loftet her fra 2,20456 × 10⁻⁵ til 1,98034 × 10⁻⁵. De to ydergrænser for hele forløbet kommer nu fra z omkring 800–800,23 og 809,6825–810. Hvor den faktiske fejl er størst, står åbent.

## Hvad mangler?

Den underliggende CLASS/P6-beregnings reproducerbarhed og forbindelsen mellem dens interne tilstande og kildeløsningen skal stadig dokumenteres gennem hele forløbet. V133 genbruger certificerede data. Begge snit ved z = 810 er dækket. Så længe deres nuværende punktintervaller fastholdes, kan en finere opdeling af forløbet højst sænke V133-loftet med yderligere ca. 3,45 %.

## Næste runde

Resultatindtag og routing skal prøve de 147 arkiverede stykker ved z = 800–810 og måle, hvor meget den sidste del af loftet kan sænkes. Opgaven, inddata, acceptkriterier og stopregel ligger i Q052_RESULTATINDTAG_OPGAVE_V133.json. Python med eksakte brøker og adgang til de vedlagte originaldata er tilstrækkeligt til opgaven. Ved uoverensstemmelse mellem delsummerne skal V134 fastholde V133-loftet og dokumentere afvigelsen.

## Journal og point

Q052_MATEMATIK_OG_SAMLET_JOURNAL_V133.md er den samlede journal. Bevis, kode, maskinlæsbare resultater og GitHub-overlevering ligger i ZIP-filen. Rundens 74 point fordeler sig på 22 for analyse, 23 for beregning, 6 for kildearbejde og 23 for validering. Totalen er **15.704**. M015 er leveret. Der mangler **296 point** til næste SoMe-pakke ved 16.000.
