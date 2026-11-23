# Q052 · V146 · Overlevering fra række 2 til et blokforsøg

**23. november 2026 · Resultatindtag og routing 2.3.0**

V145-certifikatet er verificeret. De to genkørsler ved 108 og 128 cifre genskabte hver sin arkiverede JSON-fil byte for byte. Den maksimale absolutte relative H-afvigelse på celle 2 ligger strengt mellem **6,3677 × 10⁻¹¹ og 6,3754 × 10⁻¹¹**. Den gemte H-spline ligger under V73-referencen gennem hele cellen.

Ved række 2 matcher de gemte splineværdier de oprindelige L- og R-tabeller. Den konforme hastighed blev delt med exp(u₂) på ny ved 140 cifre. Resultatet er indeholdt i V145's beregnede interval. Evidensfilen bevarer feltets og hastighedens fulde V73-intervaller som starttilstand til næste beregning. Ved række 2 er den akkumulerede feltforskydning cirka 1,925670 × 10⁻⁴⁷ i CLASS-feltenheder.

## Grundlaget for 32 celler i én beregning

| Kontrol | Resultat |
| --- | --- |
| Oprindelige data | Begge 40.000-rækkers filer og deres datadele matcher de arkiverede SHA-256-summer. Række 2–34 er byteidentiske i L og R. |
| Koordinater | 32 sammenhængende celler fra række 2 til 34, med samlet bredde cirka 0,0257896 i ln(a). |
| Kildegren | For hele blokken giver strålingsleddet H > 1,8985 × 10²² Mpc⁻¹. Grænsen U/(3H²) < 1,8140 × 10⁻⁴² ligger under CLASS-grænsen 0,5. Den indesluttede kraft V′ er positiv. |
| Feltets spline | De 33 knuder har samme feltværdi som det oprindelige input og nul gemte andenafledte. Feltets spline er derfor konstant gennem blokken. |
| Overgange | Splinernes værdier har fælles knudepunkter. De rationelt beregnede relative spring i de ensidige afledte er under 2,0 × 10⁻¹⁶ for H og den konforme felthastighed. De eksakte kubiske stykker behandles hver for sig. |

Springet ved række 2 er målbart i den eksakte rekonstruktion af de afrundede splinekoefficienter. Det giver grund til at beholde begge ensidige afledte i beregninger, der bruger dem. Beregningen af fejlgrænser kan fortsætte stykkevis med de fælles knudeværdier. Derfor giver en blok med flere celler mere information end en særskilt gentagelse ved række 2.

**V147 går til Matematikmotor 2.3.0.** Opgaven er at føre referenceintervallerne frem gennem de 32 celler og give signerede grænser for Δφ, ΔX og ΔH. Den skal desuden give en øvre grænse for den største absolutte relative H-afvigelse, et verificeret punktvidne og en klar endepunktstilstand. Den stopper ved række 34 eller ved den første dokumenterede celle, hvor en krævet kontrol fejler. Valget af 32 celler er et afgrænset forsøg på at teste, hvordan usikkerheden udvikler sig gennem flere overgange.

**Q052 fortsætter som INCONCLUSIVE.** V146 kontrollerer data, overgang og kildegren. V147 skal beregne de faktiske splineafvigelser i blokken. For hele Q052 mangler forbindelsen til CLASS' interne bane og certificerede maksimumafvigelser for elektronfraktion og Thomson-optisk dybde.

V146 giver **72 estimerede arbejdspoint**. Total **16.705**, med **295** til M017. De fire V146-filer er klar til manuel upload til roden af Morfindien/Bubbleverse. Den kontrollerede GitHub-revision indeholdt V144 og begge motorer. V145-filerne lå endnu ikke i roden under deres afleverede navne.

- [GitHub-revision med de verificerede motorer og V144-input](https://github.com/Morfindien/Bubbleverse/tree/d0807d9af724c3a2d4251a16fffeac2c7475f659)
- [Oprindelig V141-kørsel med L- og R-tabellerne](https://github.com/Morfindien/Bubbleverse/actions/runs/45061263002)
- [Fastlåst CLASS-kilde for baggrundsligningerne](https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c#L2697)
