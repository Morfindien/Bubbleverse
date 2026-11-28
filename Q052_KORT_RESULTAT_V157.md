# Q052 V157 · Kontrol af udvidelseshastigheden frem til z = 800

**For den fastlåste model og beregningsopsætning afviger tabellens udvidelseshastighed højst 0,0065 % fra referencen gennem hele intervallet fra z = 800 til 810.** V157 dækker fra 800 til 7123223648197587/8796093022208 ≈ 809,8167709474. V155 dækker resten op til 810. Fortegnet af den faktiske fejl er åbent.

| Kontrolleret størrelse | Udadrettet interval i V157 |
|---|---|
| H fra programmet minus H fra B★ | −0,0002114617277410 til +0,0002077410574652 Mpc⁻¹ |
| Bredden af det signerede H-interval | 0,0004192027852060 til 0,0004192027852061 Mpc⁻¹ |
| Relativ forskel, med H fra B★ som nævner | −0,00645999964515 % til +0,00634633591546 % |
| Offentlig, opad afrundet absolut relativ grænse | 65 milliontedele |

Den smallere V155-grænse på 50 milliontedele gælder stadig i dens oprindelige delinterval. For den samlede strækning bruges den største af de to ydergrænser. Grænsernes bredde udtrykker vores numeriske usikkerhed om forskellen. De fastslår hverken den realiserede maksimumsfejl eller dens fortegn.

## Samme baggrund ved begge ender

Begge energiankre gælder den samme B★-løsning. Den fastlåste V105-celle 142 slutter ved præcis a = 1/801. Ved z = 810 anvendes den V153-indeslutning, der er bundet til samme kilde og de samme startdata. For e = X²/2 + V med V ≥ 0 gælder −6e ≤ de/dln(a) ≤ 0. Skriv s = 1+z. Så ligger energien for hvert z i skæringen af følgende to intervaller:

- Fra 810 ligger e mellem e810_nedre · (s/811)⁶ og e810_øvre.
- Fra 800 ligger e mellem e800_nedre og e800_øvre · (s/801)⁶.

Begge nedre og begge øvre funktioner vokser eller er konstante med z. De validerede ankres skæringer ved enderne er forenelige. Den underliggende energilov gælder for hvert indre punkt. Endepunkterne af de monotone omslutninger giver en referenceboks for hvert af de 1.024 lukkede delintervaller. Positive stof-, strålings- og neutrinobidrag indgår i den positive Friedmann-rod. To beregninger bruger forskellige intervalbiblioteker, splineformer og neutrinoudtryk. De deler energiloven og de historiske referencebeviser.

## Tabelopslag, afrunding og kontrol

Programværdien ved fysisk z defineres som det fastlåste tabelopslag ved z afrundet til nærmeste binary64 med lige sidste bit ved lighed. Derefter kommer eksakt addition af 1 på dette talgitter og den korrekt afrundede logaritme fra arkivets MPFR-konvention. Den reelle reference evalueres ved det oprindelige z.

Koden kontrollerer hældningens fortegn og størrelse på alle relevante kubikstykker. Ved hver berørt indre knude køres begge nabogrene. Begge returnerer knudens gemte H. Sammenhængen og hældningsgrænsen dækker derfor også forskellen mellem den fysiske og den afrundede logkoordinat ved et grenskel. Hver regneoperation i tabellens kubik indgår i afrundingsbudgettet. De numeriske forudsætninger følger V155, herunder samme operationsrækkefølge og afrunding. Referencen og de præcise fejlbudgetter står i certifikatet.

Alle 83 RHS-kald og 40 outputposter blev genafspillet med samme H-værdi som i arkivet. De punktvise fejlindeslutninger ligger i de tilhørende delintervallers signerede grænser. Den øvre endes egen punktkontrol ligger helt inde i V155’s første delinterval for både den absolutte og den relative signerede forskel. Ved z = 800 ligger referenceboksen inden for grænsen fra V105-endepunktet. V156’s arkivudtræk er desuden genkørt fra de fastlåste råfiler. De oprindelige V156-evidens- og opgavefiler matcher deres Git-blobs ved 1a47e7b9a34080282692211645ebe65bcb9fed7b.

## Status og næste opgave

Teknisk PASS_CONDITIONAL_SCOPED. Q052 er ACTIVE · CONTINUE · INCONCLUSIVE. Virkningen af H-fejlen på elektronfraktionen og den integrerede Thomson-dybde er åben. Der er ingen ny observation eller ny native tidsintegration i V157.

**Resultatindtag og routing 2.4.0 → V158.** Genkør V157, kontrollér sammenføjningen ved den fælles grænse og registrér dækningen 800–810 én gang. Afgør på arkiveret grundlag, hvor den første udækkede afhængighed ligger efter z = 800, og vælg én afgrænset opgave. En fortsættelse af referencecelle 142 under dens endepunkt kræver nyt grundlag.

V156-totalen var 17.586. V157 tilføjer 95 estimerede aktivitetspoint, fordelt på 23 for analyse, 30 for beregning, 8 for kildeafstemning og 34 for validering. Det giver 17.681, med 319 til næste 1.000-pointtærskel. Det nye sammenhængende H-interval udløser en videnskabelig milepæl. SoMe og læringsforklaring er journalført som klargjort.

Python med eksakte brøker, dyadiske intervaller og mpmath.iv 1.3.0 er anvendt. Kode, input, datamanifest og reproduktionsvejledning følger med. Alle V157-filer har nye navne og er klar til manuel arkivering i projektets rod. Handoff-formatet er kontrolleret lokalt med referencer og hashes. [GitHub-base](https://github.com/Morfindien/Bubbleverse/tree/1a47e7b9a34080282692211645ebe65bcb9fed7b) · [Målearkiv](https://github.com/Morfindien/Bubbleverse/actions/runs/45109440243)

Afsluttet 2026-11-28T07:48:51+01:00 (Europe/Copenhagen).
