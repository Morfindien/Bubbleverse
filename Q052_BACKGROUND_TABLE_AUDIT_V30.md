# Q052 V30 — native baggrundstabel indlæst og afgrænset

Kilde: GitHub Actions-artefakt `q052-background-dump-v30-41005961285.zip`, run `41005961285`, arm L, nominal. Den indbyggede resultatfil angiver `RAW_NATIVE_TABLE_CAPTURED_NOT_ERROR_CERTIFICATE`.

## Integritet og faktisk indhold

- `background_table_hex.jsonl`: SHA256 `2b037acdb209419707c24525d582e390596d92689f7af0d38183e83ca5f7eadd`, kontrolleret mod resultatmanifestet.
- 40.000 fortløbende rækker, 32 baggrundskolonner og 32 tilsvarende spline-andenderivater pr. række; strengt voksende `loga` og strengt faldende `z` blev kontrolleret over hele filen.
- Pinned source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`; binary SHA256 `df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf`; point SHA256 `12100006d1e164ce9b7605641e1321d4a6cf4b022bb196d04199e59ee76c237c` matcher den tidligere native L/R-inventarregistrering. Den nye kørsel har samme serialiserede z=810-start som arkivet for L, bortset fra run-id.
- Tabellen blev skrevet efter `background_init` i én ny L-kørsel. Den indeholder data, ikke en certificeret fejlgrænse for baggrundsintegrationen.

## Kontrol på de to første celler

Cellerne spænder fra z=810 til z=`0x1.9497ae147ae14p+9` (=809,185). Ifølge tabellens `z`-kolonne dækkes dette interval af splineintervallerne 31687–31688 og 31688–31689. Den pinned `background_at_z`-kilde evaluerer en kubisk spline i `loga=-log(1+z)` og læser H som kolonne 1; H_prime er en selvstændigt interpoleret kolonne 2.

Jeg omskrev den lagrede splineformel til kubiske Bernstein-koefficienter med eksakte rationelle tal fra hexværdierne. På **begge hele tabelintervaller** ligger alle H-koefficienter mellem `3.269387055325748` og `3.277837159385664` 1/Mpc (udad afrundede decimaler). Derfor ligger den eksakt fortolkede lagrede H-spline i dette interval, når forespørgslen mappes til disse intervaller. Q050's eksisterende betingede H-projektion for den omsluttende z=810→800-celle er `[3.160852716131442…, 4.480552533941655…]` 1/Mpc. Denne **projektionskompatibilitet** passerer med stor margin.

## Videnskabelig status og næste beviskrav

Projektionskompatibilitet identificerer ikke native kurven med ét fast medlem af den admitted Q050-baggrundsfamilie. Der mangler fortsat en valideret fejlindeslutning for tabellens numeriske baggrundsintegration, `-log(1+z)` og splineberegning samt en binding af de aktive baggrundsfelter til den samme frosne Q050-B på hele intervallet. Den nye kørsel er kun L; tidligere R har samme pin og første H-snapshot, men ingen komplet R-tabel er byte-sammenlignet. Derefter mangler særskilt start-, solver-, output-, xe/τ- og globalt supremumsbevis.

Q052 er fortsat **ACTIVE/INCONCLUSIVE**. `native_background_membership_certified=false`, `source_real_certificate=false`, `full_q052_gate=UNRESOLVED`; realiserede globale suprema er ukendte. V30 fjerner V29's rene *mangel på native tabeldata* og gør en tabelbaseret interval-/admissionsanalyse mulig. Den afslutter ikke det matematiske certifikat og ændrer ingen model eller Q051-grænse.
