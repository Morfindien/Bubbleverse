# Q052 V80 · Kan de to baner skifte formel på forskelligt tidspunkt?

**Resultatindtag og routing 2.3.0 · Q052 fortsætter**

V79 er godkendt under de fastholdte modelpræmisser. Fra rødforskydning 810 ned til 46,459646 ligger forskellen i kildeløsningernes elektronfraktion på højst én elektron pr. million hydrogenkerner. Maksimum nås kun ved 810 i dette område. Fra 0 op til cirka 5,595560 er forskellen højst 0,98840 elektron pr. million. Det skarpe loft er fortsat uafgjort på mellemstykket. De eksakte intervalender står i certifikatet.

## Hvor meget af den første usikre celle kan vi allerede afgøre?

Den første arkiverede celle, hvor begge kildemodeller kan forekomme, går i udviklingsretningen fra 46,45964596 til 46,44464446. V79 fandt et punkt ved 46,45214521, hvor de to formler giver et udadrettet felt på kanten af det område, der skulle holde elektronforskellen nede. Punktet er tilladt af de daværende temperaturbokse. Der foreligger ingen dokumentation for, at de faktiske kildeløsninger når punktet.

V80 udelukker et blandet formelvalg i den første del af cellen, fra den øvre kant ned til mindst 46,45868. Den eksakte beregning dækker 6,4699 % af cellens bredde i rødforskydning. Det afgør ikke situationen ved V79-punktet længere inde i cellen.

## Én temperaturtest før det fælles formelskift

Lad $v=T_m/T_\gamma$ og lad $u=\ln[811/(1+z)]$ stige, mens rødforskydningen falder. Begge arme opfylder $v'=-v+A(1-v)$. De arkiverede kildeindeslutninger har $A>0$ og $0<v\le1$ i alle 2.266 celler pr. arm fra 50 til den nedre kant af det fælles strålingstemperaturskift. Dermed er $d[v/(1+z)]/du=A(1-v)/(1+z)\ge0$. En nedre grænse $b$ for temperaturforholdet ved $z_0$ giver i hele det efterfølgende interval

$$
v(z)\ \ge\ b\,\frac{1+z}{1+z_0}.
$$

Ved den øvre kant af den første usikre celle er den mindste af de to dokumenterede nedre temperaturgrænser cirka 0,1000020451. Uligheden ovenfor udelukker den kolde gren, så længe begge temperaturforhold med sikkerhed er over kildens tærskel 0,1. I regnestykket bruges den højeste af den eksakte decimal og dens binære repræsentation. Ved den eksakte beregnede ydergrænse bruger vi konservativt et åbent endepunkt.

| Mål | Tilstrækkelig nedre grænse for hver kildeløsning ved $z=50$ |
|---|---:|
| Udeluk et temperaturbetinget grenskift i hele den første usikre celle | 0,10749370 |
| Udeluk et temperaturbetinget grenskift helt til det fælles skift omkring $z=16,03101$ | 0,29946 |

Tabellens tal er rundet op. De eksakte krav og de strenge uligheder står i guard80.json. Når strålingstemperaturen alene vælger Peebles-grenen, sker det ved samme rødforskydning i begge arme, fordi de deler baggrund og kildetærskel. Den stærke test ville derfor udelukke den specifikke mekanisme, som V79 fandt. De øvrige betingelser for elektronloftet skal stadig kontrolleres på de senere intervaller.

## Hvad mangler ved rødforskydning 50?

| Temperaturforhold ved $z=50$ | Venstre beregning | Højre beregning |
|---|---:|---:|
| Arkiveret nedre grænse for kildeløsningen, omtrent | 0,10745537 | 0,10745533 |
| Gemt værdi fra CLASS, omtrent | 0,36566352 | 0,36545782 |

De gemte værdier fortæller, hvor der er mulighed for en afgørende kontrol. Hvis det kan bevises for **begge** arme, at den gemte værdi ved 50 højst overvurderer kildeløsningen med 0,065 i temperaturforhold, følger hele den stærke temperaturtest. Hverken disse fejlgrænser eller de stærke nedre kildegrænser er dokumenteret endnu.

**Næste motor er Matematikmotor 2.3.0.** Dens ene opgave er at bevise en skarpere nedre grænse for hver arms temperaturforhold ved 50 ud fra de matchede startdata og den fælles baggrund. Det kan gøres ved at afgrænse opvarmningen i de arkiverede intervaller eller ved at sætte en ensidig grænse for forskellen mellem gemt temperatur og kildeløsning. Lykkes kun den svagere test, skal den præcise opnåede rækkevidde og den første utilstrækkeligt bestemte størrelse afleveres.

Q052 er fortsat åbent. V78's øvre grænse på 0,00092647 for den største absolutte forskel i akkumuleret Thomson-optisk dybde er fortsat den anvendte grænse. Den sande maksimumværdi er uafgjort.

