# Q048 V121 — handoff to Builder2.2.0

STATUS: **CONTINUE / ONE SOURCE-CORRECT ACTUAL-CONSUMER TASK**.  
TASK_ID `LOCAL-Q048-V121-SOURCE-CORRECT-ACTUAL-CONSUMER-910-900-V1`. TASK_FINGERPRINT `781f560ae5a913bedd6d0305552cdc4f36dc79ab8f7af99299a544337c2abd44`.  
CURRENT_Q=TARGET_Q=Q048; authorized Q001–Q048. CASE ACTIVE/INCONCLUSIVE.  
Ingestion event `LOCAL-Q048-V120-SOURCE-CORRECT-PROOF-INGESTION-V1`; UTC `2026-10-20T14:52:22.356248+00:00`, Europe/Copenhagen `2026-10-20T16:52:22.356248+02:00`.

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Question SHA256 `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`.

## Objective and current state

Execute exactly one NEW source-correct reassessment-lineage actual consumer **910→900**, a=[1/911,1/901]. Current accepted actual is117/frontier910. **Expected** actual118/frontier900 is not existing authority; it may be accepted only after all source/parent/theorem/glue/endpoint/verifier/postaccept checks pass.

Parent `Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json` SHA256 `b99025ea901930476d91d31a8ff3cbdbf1caadc86d4b92a44cd0bd4e5d63e8ae`. Parent endpoint `{"a": "1/911", "E": "41553114742782417797/1000000000000000000", "Y": "33016542108247500469/1000000000000000000", "Vbar": "8180882108095962439/1000000000000000000"}`; current lower `426269669916063/1000000000000000000`, current prior-cell K `1202814173580219054419/250000000000000000`, correct SAHA_FACT3.016103031869581e21. Other3frontiers1440.

Theorem `Q048_V120_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json` SHA256 `9f3d2381f40bdd03f4bd692e72105fb4e3e02611e47772be2bab27dee7b0158f`; raw `3324b5801396dd5a7b13be99f8fe0e5e1d65b347711b535eb0f3ac9dc30804a0`; verifier `e439c998684b9d047a5d78d909cfc30568a82ea9d21a074b1db9c4b74400460e`; postaccept `dae1aac830186e328669ad1dd82605290e2b7aedce330cd21c959ffea4cb0b06`. Accepted theorem fresh K_upper=`1184837959588125278027/250000000000000000`, connected lower=`83379887432219/200000000000000000`, w=[-1/1000000,1/50], source SAHA_FACT3.016103031869581e21. Existing verifier31/31 PASS,18/18 real mutations rejected; postaccept21/21 PASS. Ingestion did not rerun the proof.

**Schema binding:** this V120 acceptance is `bubbleverse.q048.v120.source_correct_proof.acceptance.v1`, with `proof_cell_z`, `proof_cell_a`, `parent_checkpoint_sha256`, and flat `K_upper`/`connected_lower`. Do not assume older bridge acceptance fields such as `retained_theorem` or `proof_bridge_cell_z`. Use the actual accepted bytes and explicit binding, not an invented schema coercion.

## Guard and endpoint

Original `q048_guard_local_v_result_v12.json` SHA256 `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`, Library ID `libfile_f8cfc5fd42988191ba68db41eb12641f`. Primary row54 SHA256 `448ae715d15903d6bf77750ba62c673fde3d7422e6bd626a76f0062c037329ec`. The row is committed, accepted and whole-cell-qualified with source_state_reset=false; left a/E/Y/V_previous match V119 exactly. Control remains guard-only. Full primary/control rows and eight saved/hash-pinned V119 method references with Library IDs are in `Q048_V121_NEXT_BUILDER_TASK_V1.json`. Freeze actual wrong-schema controls with the base suite; every mutation must change a derivative fixture. No V119 main is to be replayed.

Expected endpoint cross-check only: a=`1/901`, E=`10009745397581786717/250000000000000000`, Y=`1987905512933907887/62500000000000000`, Vbar=`3944736412871797407/500000000000000000`. Obtain endpoints from the committed primary row, then compare. Bind new K/lower from V120 only after all admission checks pass.

## Required behavior / finite return

1. Freeze and pin V119 parent, V120 acceptance/raw/verifier and primary row54. Check exact hashes and exact no-reset left glue before execution.
2. Consume V120 once; no proof rerun/recomputation. Use the smallest sufficient direct/local execution mechanism where feasible; no speculative GitHub workflow required.
3. Produce at most1new actual cell with zero new proof cells.
4. Run separate validation and postaccept checks including actual semantic mutations against wrong parent/theorem/schema/row/reset/cell/endpoint/K/lower/below900/extra cell.
5. Preserve first material failure if any; no tuning, relabelling or historical replay.
6. STOP after this one accepted cell or first exact blocker and return exactly once to Result Ingestion2.1.0. **No below900 work.** Finite300 science-second budget, zero retries, no postfreeze edits.

SUCCESS: one validated/accepted actual118/frontier900 under the exact accepted source-correct theorem, no reset, postaccept PASS. FAIL: first authority/hash/schema/source/glue/endpoint/verifier/postaccept invariant. All historical V101 through V120 records unchanged. No NativeP6/full four-case bounds claim, model/Q change or Q closure.

The V120 Mathematics consumer_authorization=NOT_GRANTED is preserved. The new V120 ingestion separately grants this bounded V121 task; use the new ingestion state/envelope as downstream authorization without rewriting the theorem record. No further consumer is authorized.

## Full state / engine / delivery

Complete journal `Q047_SAMLET_JOURNAL_Q048_V120_INGESTED_SOURCE_CORRECT_V1.md` SHA256 `bc273f76c398293765b3ad478dbd9706fc77ecb5a92f95ac97a0f06cb7968cfe` preserves incoming proof journal `e966651e0cf64e2c1c66db3aebf5e9e723f9b39899f95d9d48477372cae3c020` byte-for-byte plus one ingestion receipt. New source/evidence map `Q048_V120_INGESTION_EVIDENCE_AUDIT_V1.json`, current snapshot `Q048_V120_INGESTION_STATE_V1.json`, machine envelope `Q048_V120_INGESTION_HANDOFF_ENVELOPE_V1.json`, exact task `Q048_V121_NEXT_BUILDER_TASK_V1.json`, inventory `Q048_V120_INGESTION_OUTPUT_MANIFEST_V1.json`. Canonical old source/claim history remains in the full journal. All19 V120 sources are present and byte-equivalent at GitHub base `8bc070b56e8178637075d3d542b22bc552c2582d`.

Builder2.2.0 verified through `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0-33.md` at that base; Git blob `e6f8cef22d4fc45b5c5b3d645539b05caf3c2c9a`, exact prompt SHA256 `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`. Parent and8 V119 method files are GitHub-byte-verified; exact hashes,commit and saved Library IDs are in the task recovery map and audit. The20 older V115 ancestry files remain upload-pending with exact saved recovery refs in the audit. Source origin INTERNAL/AI_ASSISTED with shared physical theorem premises; no independent physical support from upload. Q048 remains ACTIVE/INCONCLUSIVE, NativeP6 and complete four-case xe/tau bounds unresolved.

Setup: current exact-arithmetic-capable runtime for the small deterministic admission; model/settings catalog not verified, no switch claimed. Handoff PREPARED, not dispatched or executed. NEW ingestion files USER_UPLOAD_PENDING; existing V120 source files already on GitHub. Preserve the complete journal and immutable source artifacts through the next return.


## V120 endpoint900 source contract

The unchanged pinned hydrogen.c source uses `if (z < 900.)`; exact z=900 is outside the low-z branch. V120 separately qualified the inclusive z>=900 domain in producer and independent verifier. Its new source_boundary_certificate is bound by acceptance/raw and passed verifier and postaccept checks. All other captured model/flag/temperature/fit gates remain required. The original historical strict above900 restriction is preserved in old records.

Reuse V120's completed 31/31 verification,18/18 real mutation rejections,21/21 postaccept,35/35 delivery and5/5 preflight records. No scientific rerun is performed here. Before freeze V121 must adapt V119 methods' older30/16/20 assumptions and bind the exact new certificate in consumer, separate validator and postaccept. Freeze real negative fixtures for missing/changed certificate, below900, source/cell/a mismatch and wrong proof-record counts. A count alone is insufficient. No extension below900 is authorized; that would require separately authorized source-branch work.
