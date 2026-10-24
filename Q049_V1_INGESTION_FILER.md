# Q049 — indtagelse V1: filer og upload

**Næste motor: Matematik 2.2.0.** Brug den nye task, den nye samlede journal og ledgerV3.

RUN COST:28 pts · USED:176/1000 pts · REMAINING:824 pts. MatematikV1s148point er allerede indregnet; ingen dobbeltdebitering.

## Nye primære filer

- [Q049_V1_INGESTION_RESULTAT_OG_OVERLEVERING.md](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_RESULTAT_OG_OVERLEVERING.md)
- [Q049_V2_NEXT_MATHEMATICS_TASK.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V2_NEXT_MATHEMATICS_TASK.json)
- [Q049_V1_INGESTION_STATE_AND_HANDOFF.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_STATE_AND_HANDOFF.json)
- [Q047_SAMLET_JOURNAL_Q049_V1_INGESTED_V1.md](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q047_SAMLET_JOURNAL_Q049_V1_INGESTED_V1.md)
- [Q049_QUESTION_BUDGET_LEDGER_V3.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_QUESTION_BUDGET_LEDGER_V3.json)

## Nye kontrol- og memoryfiler

- [Q049_V1_INGESTION_AUDIT_AND_MEMORY.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_AUDIT_AND_MEMORY.json)
- [Q049_V1_INGESTION_JOURNAL_APPEND.md](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_JOURNAL_APPEND.md)
- [Q049_V1_INGESTION_PROSPECTIVE.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_PROSPECTIVE.json)
- [Q049_V1_INGESTION_VALIDATION.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_VALIDATION.json)
- [Q049_V1_INGESTION_OUTPUT_MANIFEST.json](sandbox:/workspace/scratch/5696cf6119fd/q049_ingestion/output/Q049_V1_INGESTION_OUTPUT_MANIFEST.json)

## Eksisterende V1-filer, der fortsat skal følge sagen

Disse er de allerede gemte originaler. De er ikke nye kørsler eller nye debiteringer. GitHub-træet ved den inspicerede commit indeholdt V1s fire Markdown-filer, men ikke disse maskin-/kodefiler.

- [Q049_QUESTION_BUDGET_LEDGER_V2.json](https://chatgpt.com/library?file_id=libfile_00c4f69d98388191b1b6f53832b7771d&account_id=personal)
- [Q049_V1_HANDOFF.json](https://chatgpt.com/library?file_id=libfile_79ba322524748191aa47e4a48b346c26&account_id=personal)
- [Q049_V1_CERTIFICATE_RESULT.json](https://chatgpt.com/library?file_id=libfile_fc2d51c36ec48191851228c2d24efc64&account_id=personal)
- [Q049_V1_INDEPENDENT_VERIFICATION.json](https://chatgpt.com/library?file_id=libfile_125618fc91008191959f5ac2a1330ff4&account_id=personal)
- [Q049_V1_INPUT_PROVENANCE.json](https://chatgpt.com/library?file_id=libfile_dc1b94dce18c81918f5ab3b9804220b6&account_id=personal)
- [Q049_V1_VALIDATION_CONTRACT.json](https://chatgpt.com/library?file_id=libfile_516f7ec420c48191b2de305ec5f758d2&account_id=personal)
- [Q049_V1_RUN_MANIFEST.json](https://chatgpt.com/library?file_id=libfile_744d639b6620819183cc0c2d2c055925&account_id=personal)
- [Q049_V1_PROSPECTIVE_RUN.json](https://chatgpt.com/library?file_id=libfile_a9e299a2c2f88191ae40964cf50aeb72&account_id=personal)
- [Q049_V1_DELIVERY_VALIDATION.json](https://chatgpt.com/library?file_id=libfile_06e54c2dda148191b19090457df8ccd2&account_id=personal)
- [Q049_V1_JOURNAL_APPEND.md](https://chatgpt.com/library?file_id=libfile_41bed88dd6e88191a7fa4dd31425d6fb&account_id=personal)
- [Q049_V1_GITHUB_MEMORY_UPDATE.json](https://chatgpt.com/library?file_id=libfile_ddcd8979ccb48191a56ed0c959cb7b24&account_id=personal)
- [Q049_V1_SHA256SUMS.txt](https://chatgpt.com/library?file_id=libfile_142b62afc9588191adb8a3d8cb51a24c&account_id=personal)
- [q049_v1_certificate.py](https://chatgpt.com/library?file_id=libfile_a8e60378e9888191b6c832c92913d4c0&account_id=personal)
- [q049_v1_independent_verify.py](https://chatgpt.com/library?file_id=libfile_1cd2053a3948819185a87ee4bf2fd034&account_id=personal)

## Sådan anvendes pakken

1. Upload de manglende originale V1-filer ovenfor til repoets rod med præcis de eksisterende filnavne. Bevar ledgerV1 og alle øvrige historiske filer.
2. Upload alle nye filer i denne pakke til repoets rod med de versionsbestemte filnavne. Ingen gamle journaler eller ledgers skal erstattes. Manifestets egen SHA er udeladt for at undgå rekursion.
3. Lad den aktuelle arbejdsvisning pege på den nye samlede journal, ledgerV3 og næste task. En central videnskabelig CURRENT_STATE-sti er ikke identificeret; ændr ingen eksisterende global struktur ud fra et gæt.
4. Kør den eksisterende Matematikmotor2.2.0 med den nye task, journal, handoff-state og ledgerV3. Den har824point tilbage; næste runde er anslået160, højst220, endnu ikke reserveret eller afregnet. Ingen Actions-workflow/PROGRAM_ID er oprettet.

Kontrollér nyeste repo-/budgetversion før en senere upload. Denne motor har ikke foretaget et push, commit, PR eller dispatch. Repoets aktuelle kildegrundlag er inspiceret ved6832445dc571a279cc5446c271dce93cdac54c15; nye pointere er forslag, indtil filerne faktisk er uploadet.

Alle filer leveres enkeltvis. Der er ingen zip.
