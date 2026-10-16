# Q048 V28 ingestion — upload/apply instructions

Verified project-memory base: `Morfindien/Bubbleverse@ef75d9442a7b5f020ad25578524464fe8e96287f`. V28 origin er delvist på main. Ingen ingestion GitHub-write blev udført.

## Først: kompletér immutable V28-origin

Repository mangler under forventede paths især `q048_moving_h_domain_result_v28.json` og `q048_moving_h_domain_candidate_checkpoint_v28.json`. De verificerede originalbytes er med i denne pakke under `evidence/`; upload dem som nye immutable originfiler. De må ikke tælles som ny videnskabelig evidens. De øvrige manglende supportartefakter kan uploades fra den oprindelige V28-levering, men de to nævnte er de vigtigste for næste consumer-lineage.

## Upload derefter ingestionpakken

Upload alle rootfiler i denne ingestionpakke som nye immutable filer. Overskriv eller slet ikke V28/V27/V26/V12 historik. Hvis main er rykket fra `ef75d9442a7b5f020ad25578524464fe8e96287f`, genlæs base før en working-state/index-pointer opdateres.

Til næste Builder-run er minimumshandoff:

1. `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0.md` under `evidence/` — SHA256 `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`.
2. `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V28_INGESTED_V1.md`.
3. `Q048_MOVING_H_DOMAIN_V28_INGESTION_HANDOFF_TO_BUILDER_V1.md`.
4. `Q048_MOVING_H_DOMAIN_V28_NEXT_BUILDER_TASK_V1.json`.
5. `evidence/q048_moving_h_domain_result_v28.json`.
6. `evidence/q048_moving_h_domain_validation_v28.json`.
7. `evidence/q048_moving_h_domain_accepted_checkpoint_v28.json`.
8. `evidence/q048_moving_h_domain_postaccept_validation_v28.json`.
9. V27 actual parent + V12 guard kan genfindes i projektmemory; V27 producer/verifier/spec patterns er også pakket under `evidence/`.

Stop ved én Builder actualcelle1320→1310 eller første obstruction. Ingen automatisk continuation under1310.
