# Q048 V15 ingestion — individuelle filer

**70actualceller; frontier1380. Q048 ACTIVE/INCONCLUSIVE. Næste motor: Matematikmotor2.1.0.**

Send motorprompt, handoff, fuldjournal og detteindeks. Ingenvidenskabeliggenkørsel eller dobbelttælling.

| Fil | Rolle / foreslået repositorypath |
|---|---|
| [Bubbleverse_Matematikmotor_2.1.0.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Bubbleverse_Matematikmotor_2.1.0.md) | `Bubbleverse_Matematikmotor_2.1.0-4.md` |
| [Q047_SAMLET_JOURNAL_FREC_MOVING_H_V15_INGESTED_V1.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q047_SAMLET_JOURNAL_FREC_MOVING_H_V15_INGESTED_V1.md) | `Q047_SAMLET_JOURNAL_FREC_MOVING_H_V15_INGESTED_V1.md` |
| [Q048_FREC_MOVING_H_V15_INGESTION_FILES_V1.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q048_FREC_MOVING_H_V15_INGESTION_FILES_V1.md) | `Q048_FREC_MOVING_H_V15_INGESTION_FILES_V1.md` |
| [Q048_FREC_MOVING_H_V15_INGESTION_GITHUB_MEMORY_UPDATE_V1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q048_FREC_MOVING_H_V15_INGESTION_GITHUB_MEMORY_UPDATE_V1.json) | `Q048/ingestion/frec-moving-h-v15/Q048_FREC_MOVING_H_V15_INGESTION_GITHUB_MEMORY_UPDATE_V1.json` |
| [Q048_FREC_MOVING_H_V15_INGESTION_HANDOFF_V1.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q048_FREC_MOVING_H_V15_INGESTION_HANDOFF_V1.md) | `Q048_FREC_MOVING_H_V15_INGESTION_HANDOFF_V1.md` |
| [Q048_FREC_MOVING_H_V15_INGESTION_JOURNAL_APPEND_V1.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q048_FREC_MOVING_H_V15_INGESTION_JOURNAL_APPEND_V1.md) | `Q048_FREC_MOVING_H_V15_INGESTION_JOURNAL_APPEND_V1.md` |
| [Q048_FREC_MOVING_H_V15_UPLOAD_INSTRUCTIONS_V1.md](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/Q048_FREC_MOVING_H_V15_UPLOAD_INSTRUCTIONS_V1.md) | `Q048_FREC_MOVING_H_V15_UPLOAD_INSTRUCTIONS_V1.md` |
| [q048_frec_moving_h_v15_ingestion_checks_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_checks_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_checks_v1.json` |
| [q048_frec_moving_h_v15_ingestion_envelope_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_envelope_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_envelope_v1.json` |
| [q048_frec_moving_h_v15_ingestion_evidence_manifest_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_evidence_manifest_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_evidence_manifest_v1.json` |
| [q048_frec_moving_h_v15_ingestion_execution_profile_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_execution_profile_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_execution_profile_v1.json` |
| [q048_frec_moving_h_v15_ingestion_next_task_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_next_task_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_next_task_v1.json` |
| [q048_frec_moving_h_v15_ingestion_output_manifest_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_output_manifest_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_output_manifest_v1.json` |
| [q048_frec_moving_h_v15_ingestion_state_delta_v1.json](sandbox:/workspace/scratch/915459e705c6/ingestion-v15/q048_frec_moving_h_v15_ingestion_state_delta_v1.json) | `Q048/ingestion/frec-moving-h-v15/q048_frec_moving_h_v15_ingestion_state_delta_v1.json` |

## Recovery og fuldvidenskabelig state

Det komplette evidensmanifest `q048_frec_moving_h_v15_ingestion_evidence_manifest_v1.json` indeholder de31byteverificerede originoutputs med durableLibraryID og de75frosne inputs med exactsha/bytes/layout. Det erstatter ikke de fulde historiske registre; de er bevaret i helejournalen. Til næste Matematik skal task/envelope/evidensfilerne kunne åbnes.

Vigtigste genbrugte artefakter:

- `q048_frec_moving_h_result_v15.json` — `libfile_ba269bea98f88191b2b579ff73923bfe`; SHA256 `d2fa7eed39fe88b4992fe08d23c27931e89597c951d7658437c49716d056e8ca`.
- `q048_frec_moving_h_validation_v15.json` — `libfile_c1f9bc4cba60819190a4647310143efa`; SHA256 `c7710973013a2cf9442d861eb2c6688dff6d3a2587a27c98ddfd22e45b9894eb`.
- `q048_frec_moving_h_checkpoint_v15.json` — `libfile_00364640a644819197ce8eb7cb67512c`; SHA256 `be854ef0d1b6fe5435c1066c3b659c519804c7f95331d1b46667c5306cc7c57c`.
- `q048_frec_moving_h_recovery_v15.json` — `libfile_5b6a7209ed04819189220ae0a2115ddd`; SHA256 `3c2b919357a40abc39dcca9f3feb6d137c50abedaea3b5ec0c4daddad08a996d`.
- `q048_frec_moving_h_spec_v15.json` — `libfile_839b0c9750188191a0418785aa5807ef`; SHA256 `00f83f38a16d01abb2f94333388c221babec88d65a172ea32d9ff02a8039cf12`.

GitHub USER_UPLOAD_PENDING. Ingen commit/PR, synkronisering eller automatiskdispatch påstås. Alle nye outputs er individuelle filer; ingenarchive.
