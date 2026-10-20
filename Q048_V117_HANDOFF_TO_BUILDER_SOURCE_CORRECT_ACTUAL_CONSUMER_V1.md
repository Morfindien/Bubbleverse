# Q048 V117 — handoff to Builder2.2.0

STATUS: **CONTINUE / ONE SOURCE-CORRECT ACTUAL-CONSUMER TASK**.  
TASK_ID `LOCAL-Q048-V117-SOURCE-CORRECT-ACTUAL-CONSUMER-930-920-V1`. TASK_FINGERPRINT `1befbb323eea6f78d76783b307b2ddb8d00f704aa190638022bfeba7ed218fed`.  
CURRENT_Q=TARGET_Q=Q048; authorized Q001–Q048. CASE ACTIVE/INCONCLUSIVE.  
Ingestion event `LOCAL-Q048-V116-SOURCE-CORRECT-PROOF-INGESTION-V1`; UTC `2026-10-20T11:28:02.834732+00:00`, Europe/Copenhagen `2026-10-20T13:28:02.834732+02:00`.

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Question SHA256 `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`.

## Objective and current state

Execute exactly one NEW source-correct reassessment-lineage actual consumer **930→920**, a=[1/931,1/921]. Current accepted actual is115/frontier930. **Expected** actual116/frontier920 is not existing authority; it may be accepted only after all source/parent/theorem/glue/endpoint/verifier/postaccept checks pass.

Parent `Q048_V115_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json` SHA256 `0b69e1f1d37f213d833a23016e5bcbc9874bb0967584625828fcb5351a7e887a`. Parent endpoint `{"a": "1/931", "E": "22351147953825389271/500000000000000000", "Y": "7106773794579442473/200000000000000000", "Vbar": "8786409145805500919/1000000000000000000"}`; current lower `89291638472793/200000000000000000`, current prior-cell K `38382440913912560363/8000000000000000`, correct SAHA_FACT3.016103031869581e21. Other3frontiers1440.

Theorem `Q048_V116_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json` SHA256 `5c5e44f868c1c75ab453c5529139d4619af61dfa5374d986c5085c2799606929`; raw `c51eef3334fe9c237afe2735eca93d0538611b98d5023707bc9e544dda2d871f`; verifier `58bd7305ee69d3552922f0dba72e680d211ca7ca41d49cbc287105b3d8edf282`; postaccept `d455ac922a3855cf935bbe1e482b8754c099c2a3991002af238d01cb01f6cc8d`. Accepted theorem fresh K_upper=`1220855076846709617829/250000000000000000`, connected lower=`54513832861587/125000000000000000`, w=[-1/1000000,1/50], source SAHA_FACT3.016103031869581e21. Existing verifier30/30 PASS,16/16 real mutations rejected; postaccept20/20 PASS. Ingestion did not rerun the proof.

**Schema binding:** this V116 acceptance is `bubbleverse.q048.v116.source_correct_proof.acceptance.v1`, with `proof_cell_z`, `proof_cell_a`, `parent_checkpoint_sha256`, and flat `K_upper`/`connected_lower`. Do not assume older bridge acceptance fields such as `retained_theorem` or `proof_bridge_cell_z`. Use the actual accepted bytes and explicit binding, not an invented schema coercion.

## Guard and endpoint

Original `q048_guard_local_v_result_v12.json` SHA256 `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`, Library ID `libfile_f8cfc5fd42988191ba68db41eb12641f`. Primary row52 SHA256 `7b1b3f0656c9b2c92e8cdcd032b0fdc130846692fadb03613b05b127734034d3`. The row is committed, accepted and whole-cell-qualified with source_state_reset=false; left a/E/Y/V_previous match V115 exactly. Control remains guard-only. Full primary/control rows and eight saved/hash-pinned V115 method references with Library IDs are in `Q048_V117_NEXT_BUILDER_TASK_V1.json`. Freeze actual wrong-schema controls with the base suite; every mutation must change a derivative fixture. No V115 main is to be replayed.

Expected endpoint cross-check only: a=`1/921`, E=`21553673409627471439/500000000000000000`, Y=`133823577632185643/3906250000000000`, Vbar=`2119955747339110627/250000000000000000`. Obtain endpoints from the committed primary row, then compare. Bind new K/lower from V116 only after all admission checks pass.

## Required behavior / finite return

1. Freeze and pin V115 parent, V116 acceptance/raw/verifier and primary row52. Check exact hashes and exact no-reset left glue before execution.
2. Consume V116 once; no proof rerun/recomputation. Use the smallest sufficient direct/local execution mechanism where feasible; no speculative GitHub workflow required.
3. Produce at most1new actual cell with zero new proof cells.
4. Run separate validation and postaccept checks including actual semantic mutations against wrong parent/theorem/schema/row/reset/cell/endpoint/K/lower/below920/extra cell.
5. Preserve first material failure if any; no tuning, relabelling or historical replay.
6. STOP after this one accepted cell or first exact blocker and return exactly once to Result Ingestion2.1.0. **No below920 work.** Finite300 science-second budget, zero retries, no postfreeze edits.

SUCCESS: one validated/accepted actual116/frontier920 under the exact accepted source-correct theorem, no reset, postaccept PASS. FAIL: first authority/hash/schema/source/glue/endpoint/verifier/postaccept invariant. All historical V101 through V116 records unchanged. No NativeP6/full four-case bounds claim, model/Q change or Q closure.

The V116 Mathematics consumer_authorization=NOT_GRANTED is preserved. The new V116 ingestion separately grants this bounded V117 task; use the new ingestion state/envelope as downstream authorization without rewriting the theorem record. No further consumer is authorized.

## Full state / engine / delivery

Complete journal `Q047_SAMLET_JOURNAL_Q048_V116_INGESTED_SOURCE_CORRECT_V1.md` SHA256 `da6b29c98789a405e3ae51e26016cd861f8afe2adc287c2c91a5764532c43f0b` preserves incoming proof journal `c7ea02f5e38a784a0a66b31f166128d52e9aacb8108f48bdade9bd9bea959fe8` byte-for-byte plus one ingestion receipt. New source/evidence map `Q048_V116_INGESTION_EVIDENCE_AUDIT_V1.json`, current snapshot `Q048_V116_INGESTION_STATE_V1.json`, machine envelope `Q048_V116_INGESTION_HANDOFF_ENVELOPE_V1.json`, exact task `Q048_V117_NEXT_BUILDER_TASK_V1.json`, inventory `Q048_V116_INGESTION_OUTPUT_MANIFEST_V1.json`. Canonical old source/claim history remains in the full journal. All19 V116 sources are present and byte-equivalent at GitHub base `58b956cc2b05068a5636501261e0ae680f46734f`.

Builder2.2.0 verified through `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0-33.md` at that base; Git blob `e6f8cef22d4fc45b5c5b3d645539b05caf3c2c9a`, exact prompt SHA256 `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`. Parent and8 V115 method files remain GitHub-upload-pending; exact Library IDs and hashes are in the task recovery map and audit. Source origin INTERNAL/AI_ASSISTED with shared physical theorem premises; no independent physical support from upload. Q048 remains ACTIVE/INCONCLUSIVE, NativeP6 and complete four-case xe/tau bounds unresolved.

Setup: current exact-arithmetic-capable runtime for the small deterministic admission; model/settings catalog not verified, no switch claimed. Handoff PREPARED, not dispatched or executed. NEW ingestion files USER_UPLOAD_PENDING; existing V116 source files already on GitHub. Preserve the complete journal and immutable source artifacts through the next return.
