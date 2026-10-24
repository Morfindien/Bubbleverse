# Q049 V2 — resultat og filer

**Betinget global grænse: |Δtau_T,tail| ≤46.67050453** for den frosne source-real continuum-opgave. Grænsen er meget grov; lille følsomhed er ikke dokumenteret.

**Næste motor: Result Ingestion & Routing2.2.0**, til én registrering og closure-vurdering; derefter Motor14 hvis ingen konkret fejl. Ingen ny research er bestilt.

RUN COST:146 pts · USED:322/1000 pts · REMAINING:678 pts.

## Primære filer

- [Q049_V2_MATEMATISK_RESULTAT.md](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_MATEMATISK_RESULTAT.md)
- [Q049_V2_RESULT_STATE_AND_HANDOFF.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_RESULT_STATE_AND_HANDOFF.json)
- [Q047_SAMLET_JOURNAL_Q049_V2_BOUND_APPENDED.md](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q047_SAMLET_JOURNAL_Q049_V2_BOUND_APPENDED.md)
- [Q049_QUESTION_BUDGET_LEDGER_V4.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_QUESTION_BUDGET_LEDGER_V4.json)

## Kontrol, kode og provenance

- [Q049_V2_DELIVERY_VALIDATION.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_DELIVERY_VALIDATION.json)
- [Q049_V2_GLOBAL_BOUND_RESULT.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_GLOBAL_BOUND_RESULT.json)
- [Q049_V2_INDEPENDENT_VERIFICATION.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_INDEPENDENT_VERIFICATION.json)
- [Q049_V2_INPUT_PROVENANCE.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_INPUT_PROVENANCE.json)
- [Q049_V2_JOURNAL_APPEND.md](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_JOURNAL_APPEND.md)
- [Q049_V2_OUTPUT_MANIFEST.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_OUTPUT_MANIFEST.json)
- [Q049_V2_PRODUCER_FIRST_RAW.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_PRODUCER_FIRST_RAW.json)
- [Q049_V2_PROSPECTIVE_RUN.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_PROSPECTIVE_RUN.json)
- [Q049_V2_RUN_AND_MEMORY.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_RUN_AND_MEMORY.json)
- [Q049_V2_VALIDATION_CONTRACT.json](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/Q049_V2_VALIDATION_CONTRACT.json)
- [q049_v2_independent_verify.py](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/q049_v2_independent_verify.py)
- [q049_v2_invariant_bound.py](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/q049_v2_invariant_bound.py)
- [q049_v2_producer_first_draft.py](sandbox:/workspace/scratch/5696cf6119fd/q049_v2/output/q049_v2_producer_first_draft.py)

## Anvendelse og GitHub

Giv næste ingestionmotor resultatet, handoff-JSON, den fulde nye journal og ledgerV4. Originale sourceinputs, P3-parametre og z810-checkpoint er identificeret i inputprovenance. De historiske V1/V2/V3-ledgers og gamle journaler skal bevares. Ingen af dem nulstilles eller omskrives.

Upload alle nye filer i denne pakke til repoets rod under de versionsbestemte navne. Repoets synlige maskinledger er fortsat den gamleV1; upload også de manglende eksisterende maskinrecords fra tidligere filoversigter, så repoets hukommelse bliver sammenhængende. Nye current-view/pointere i run/memory-filen er forslag, indtil upload er udført. Ingen global CURRENT_STATE-sti eller launcher er opfundet.

Outputmanifestet indeholder faktiske størrelser ogSHA256 for alle filer undtagen sig selv. Hele inputjournalens14.865.746bytes bevares som eksakt prefix. Der er ingen zip, ny Actions-workflow eller PROGRAM_ID. Ingen GitHub-write, commit, PR eller dispatch er udført.

## Reproduktion

Bevar mapperne fra inputprovenance relativt til en fælles workspace-rod; de indeholder præcise source-URLer, hashes og eksisterende Library-identiteter. Læg denne pakke under q049_v2/output/. Kør python q049_v2/output/q049_v2_invariant_bound.py og derefter python q049_v2/output/q049_v2_independent_verify.py. De rekonstruerer kun det eksakte globale cap-/kontrolresultat; ingen kosmologisk bane eller native solver køres. Reproduktion er ikke nyt uafhængigt fysisk bevis.

q049_v2_producer_first_draft.py og Q049_V2_PRODUCER_FIRST_RAW.json er bevaret kladdeprovenance, ikke de aktuelle kontrolprogrammer. Den aktuelle producent er q049_v2_invariant_bound.py. Kontrakt, metode og fysiske inputs blev ikke ændret ved den dokumenterede kladdeoprydning.
