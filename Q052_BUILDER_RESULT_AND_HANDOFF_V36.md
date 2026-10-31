# Q052 V36 — nyt L/R-par kørt

**Det nye native L/R-par er gennemført. Næste motor: BUBBLEVERSE.RESULT_INGESTION_ROUTING2.3.0.**

Build, kontroller og ét nominelt par tog cirka18sekunder lokalt. Begge arme har samme start, og alle40000x32 tabelrækker matcher V30 bit for bit. Vi kan dermed fortsætte fra et nyt dokumenteret evidensgrundlag.

RUN_ID LOCAL-Q052-PROSPECTIVE-20261030-V36. CURRENT_Q=TARGET_Q=Q052. CASE LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1. UTC 2026-10-30T10:51:12.655908+00:00.

## Hvad der er leveret og kørt

`q052_native_pair_v36.py` er et selvstændigt program med capture-C, inputpunkt og alle sourcepins indlejret. Det bygger samme fastlåste CLASS-kilde som en ny numerisk realisering og kører højst ét nominelt L/R-par. Det valgfri workflow `q052-native-pair-v36.yml` er kontrolleret og henviser til dette faktiske program.

Bygningen bruger eksplicitte flags mod fast-math/reassociation og FMA-kontraktion. Koordinatkaldet i background_at_z er udskiftet med en kontrolleret MPFR-logaritme: rettede nedre/øvre endpoints skal give samme binary64 RN-værdi, før funktionen returnerer. Dette er en dokumenteret ny regneimplementation under samme fysik og konfiguration. De gamle kørsler og deres begrænsninger bevares.

## Faktiske checks og resultater

- 315 originale sourcefiler matcher pinned Git-blobs.
- 131 sammenligninger mod separat Decimal100-beregning bestod, inklusive fortegnet nul.
- L/R gennemførte59062/59043 koordinatkald;19/22 ligger i de to valgte celler. Alle blev afgjort ved128bit, og RN-/FTZ-/DAZ-kontrollerne bestod.
- Begge arme deler eksakt start og koefficientrækker. De registrerede h/D_Tmat/prehelium-startværdier matcher også de oprindelige serialiserede værdier.
- Samtlige tabelrækker og baggrundskonstanter matcher V30. Et eksplicit kompatibilitetsreceipt gør V31's eksakte referencegrænser genbrugelige under samme præmisser. Forskellige run-/armlabels giver forskellige fulde filhashes; row-stream-identiteten er kontrolleret særskilt.

For succesfulde koordinatkald på binary64 z∈[0x1.9497ae147ae14p+9,810] er log-fejlen≤2^-51≈4.4408921e-16. Her er1+z eksakt, og log-størrelsen ligger mellem4 og8. Den rettede MPFR-kontrakt plus dette grid-/afrundingsargument giver grænsen;131 samples er en implementationskontrol. Algoritmen stopper ved en præcisionscap, hvis afrundingen ikke kan afgøres; universel termination på alle hypotetiske inputs er ikke påstået. Begge faktiske native arme gennemførte. Se [MPFR4.2.1's afrundingssemantik](https://www.mpfr.org/mpfr-4.2.1/mpfr.html#Rounding).

V31's loga-interval udvidet med denne fejl ligger strengt inden for de komplette relevante splinestencils; det er verificeret med eksakte rationale uligheder. De faktiske runtime-biblioteker, wrapperen, den nye native-library, CPU/OS, byggekommandoer, C-source og assembly er bevaret.

## Hvad næste motor skal gøre

Indtag V36 én gang. Brug det konkrete kompatibilitetskort til V31-referencebeviset og vælg den næste afgrænsede native fejl-/solveropgave. Det nye er en faktisk kørt numerisk realisering og en dokumenteret koordinatkontrakt. Det er derfor ikke endnu en audit af det gamle miljø.

Q052 er stadig ACTIVE/INCONCLUSIVE. Fuld instruktionsequivalence for splinearitmetikken, det samlede aktive fejlbudget, startfejl mod source-real mål, solver-/outputfejl, resten af domænet og globale realiserede suprema er fortsat uafklarede. Ingen fysisk anomali/falsifikation eller fuld native certifikation er erklæret. Hovedspørgsmålet er uændret og står i den fulde journal/receiptet.

## Program og workflow

Programmet kræver Linux x86_64, Python3.11+, GCC/make/binutils og MPFR4.2.1-runtime/headers. Det kan selv hente pinnedsource; alle315 blobs verificeres før patch/build. Et nyt outputdirectory er obligatorisk, så eksisterende evidence ikke overskrives.

```bash
python q052_native_pair_v36.py --output q052_native_pair_v36_run --run-id MY_NEW_RUN_ID
```

Den leverede lokale kørsel er allerede gennemført; en ny kørsel er kun relevant til nødvendig reproduktion eller ændrede input. GitHub Actions er ikke startet. Hvis workflowet skal bruges, lægges Pythonprogrammet i repo-roden og YAML under.github/workflows. Det kræver ingen af de tidligere manglende runner-/recoveryfiler eller classy/Python3.11-binding.

## Memory og aktivitet

Den fulde V35-journal er bevaret byteidentisk som præfiks i V36. Alle33 gamle aktivitetsevents og fire milepælsrecords er bevaret. Ny aktivitet210points; total4935;65 til næste milepæl5000. Heuristisk arbejdsindeks, ikke credits/penge eller sikkerhed. Ingen ny SoMe-pakke eller ekstern post.

To udviklingsfejl blev rettet før nogen native kørsel: escaping i C-proben og source-copyfilteret. De fejlede states/logs er bevaret; det gennemførte par er det eneste nye par.

GitHub base `95f33afd5e9dd07d5e65782e0f33b7fa33d93378`; upload af V36 afventer, ingen commit/PR. Upload filerne individuelt til manifestets stier, bevar historik og afstem nyere main før ændring af eksisterende state/index. Handoff er PREPARED_NOT_SENT. Der leveres ingen ZIP.

## Individuelle filer

- [q052_native_pair_v36.py](https://chatgpt.com/library?file_id=libfile_d0480dae24848191a38d74debb7ec89e&account_id=personal)
- [q052-native-pair-v36.yml](https://chatgpt.com/library?file_id=libfile_6f8c8f68357c819187cb844203a6ed06&account_id=personal)
- [Q052_NEW_NATIVE_PAIR_RECEIPT_V36.json](https://chatgpt.com/library?file_id=libfile_e501a17eb22c81918196f31a3fe092e4&account_id=personal)
- [Q052_REFERENCE_COMPATIBILITY_V36.json](https://chatgpt.com/library?file_id=libfile_fdaac1d12ba481918d8b918983491966&account_id=personal)
- [Q052_NATIVE_CAPTURE_AND_RUNTIME_RECORDS_V36.json](https://chatgpt.com/library?file_id=libfile_ce44f40fda9881918aa9e5092d9b2248&account_id=personal)
- [Q052_NATIVE_BACKGROUND_TABLE_V36.jsonl](https://chatgpt.com/library?file_id=libfile_a644819f676481918048b1c6b29ddaa7&account_id=personal)
- [Q052_SAMLET_JOURNAL_V36.md](https://chatgpt.com/library?file_id=libfile_fd7147e175008191835158e79edd6a44&account_id=personal)
- [Q052_QUESTION_ACTIVITY_LEDGER_V36.json](https://chatgpt.com/library?file_id=libfile_646e7759ba708191ba9bedc905b255da&account_id=personal)
- [0ccdfb6d6f5c039465f6d002cf7e4c072d48ac6a2cffc8dd6c748dec31592804_libgmp.so.10.5.0](https://chatgpt.com/library?file_id=libfile_8369a3cb382081919fba10d3f46e9af3&account_id=personal)
- [135f3c8f006d2fe5e68e51281c7974cb991a03de3bfb3593d68d174dfcf854d1_libgomp.so.1.0.0](https://chatgpt.com/library?file_id=libfile_80defa1fb99c8191928f3d6c1b5f201a&account_id=personal)
- [2156351fa3dedd04a7381c6ac7a8a26efa2d6fb08b80f8a2d644ccdd653710ae_libmpfr.so.6.2.1](https://chatgpt.com/library?file_id=libfile_016ad9032b408191b6d64a4519fb4701&account_id=personal)
- [511f825ee075610ac9c0f7f91e2c13de2000d0f7b859f6461137e809a0a009d0_libc.so.6](https://chatgpt.com/library?file_id=libfile_883848f0c1d481918d0b9a1fdff668ce&account_id=personal)
- [6222a16be7f2d458d6870efe6e715fc0c8d45766fb79cf7dcc3125538d703e28_ld-linux-x86-64.so.2](https://chatgpt.com/library?file_id=libfile_8dee1575ef448191958ac6a71afd36e2&account_id=personal)
- [87fe92a528b6fb7284d72c145c78a5f7b51c6db7e770826d60644cbb21dcbbb0_libq052_class_v36.so](https://chatgpt.com/library?file_id=libfile_478ae236083c8191a0da6d30a7e76127&account_id=personal)
- [f06f2ce1f1833df5f41cf13b6447ff07bea993ad9b27297d3428c2f70ab3f0e7_libm.so.6](https://chatgpt.com/library?file_id=libfile_7544c5c7cb748191ae049ca147e66b60&account_id=personal)
- [ff85c12f2b5841c85b31859f54046bd4b94ebafa88b3eb7e75b5d2cc1c7b3b70_q052_capture_v36](https://chatgpt.com/library?file_id=libfile_5fc4d20fff348191b857f9597e22e3d9&account_id=personal)

Returprompt: [Result Ingestion & Routing2.3.0](https://chatgpt.com/library?file_id=libfile_3a417a1ff8588191b40b6147c00b06eb&account_id=personal).
