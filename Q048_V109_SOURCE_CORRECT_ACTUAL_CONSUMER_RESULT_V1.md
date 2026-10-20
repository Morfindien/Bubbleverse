# Q048 V109 — source-correct actual consumer 970→960

STATUS: **COMPLETE / VALIDATED** for this one admission.  
SCIENTIFIC STATE: **INCONCLUSIVE**. CASE: **ACTIVE**. CURRENT_Q=TARGET_Q=**Q048**.  
UTC: 2026-10-20T05:36:31.226937+00:00; Europe/Copenhagen: 2026-10-20T07:36:31.226937+02:00.

## Result

One source-correct reassessment-lineage actual cell was admitted: **111/frontier970 → 112/frontier960**. The run consumed V108 once, added zero proof cells, performed zero full theorem recomputations, and stopped at960. It did not perform native trajectory integration.

| Quantity | Accepted value |
|---|---|
| a | `1/961` |
| E | `49737668672811936943/1000000000000000000` |
| Y | `39560432998711765483/1000000000000000000` |
| Vbar | `4876592093839665491/500000000000000000` |
| connected lower | `479774678212513/1000000000000000000` |
| K_upper | `1001919080623370229873/200000000000000000` |
| SAHA_FACT | `3.016103031869581e21` |

Only hillipop-ede_n3 advances to960. camspec-lcdm, camspec-ede_n3 and hillipop-lcdm remain1440. No physical reset/refit/recapture/tuning, model change, historical replay/relabel, NativeP6 claim or Q closure.

## Exact scientific question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

Question SHA256: `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`. The complete histories and cumulative optical-depth differences remain unresolved. This local admission cannot establish the full requested result.

## Authority and method

V107 validated parent + V108 accepted source-correct theorem + committed primary V12 row48. Exact-byte authority pins are in the frozen spec and manifest. Source guard `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5` and canonical primary-row `98b31afe3cc6371533b59edf6ef673c0da6219122d145a8ca997276c270301cf` match the handoff. Left E/Y/V/a glue is exact. Endpoint values are read from the committed primary row; handoff endpoint values are cross-checks. K/lower are read from the accepted V108 theorem. Control row remains guard-only.

V108 Mathematics' `consumer_authorization=NOT_GRANTED` is unchanged. The independent V108 ingestion state grants the bounded V109 task, with SHA256 `adb1f7efda7eeb75a6da68781e2af8db195bcc634d3d8335b3d5c69c0742aed0`. This distinction is enforced by both producer and validator.

REUSE: V107 consumer pattern, immutable V107/V108 authority and V12 guard evidence. PATCH/CREATE: separately versioned V109 consumer, independent validator, acceptor, postaccept checker and contract tests. Historical V101/V102 remain reference history and are not used as this new consumer's authority. No previous scientific program was rerun.

Evidence categories: BUBBLEVERSE_NUMERICAL_RESULT / BUBBLEVERSE_TECHNICAL_EVIDENCE. Exact equality/provenance checks are OBSERVED; one-cell theorem applicability/admission is INFERRED under the retained source/domain premises. The validator shares those premises and is not an independent physical replication. No new external paper/source IDs were allocated.

## Execution and finite tests

- Producer executed once; four serial commands returned exit0.
- Separate verifier: **50/50 PASS**, **24/24 modified raw records rejected** by actual validator execution.
- Postaccept disk readback: **30/30 PASS**, **8/8 modified checkpoints rejected**.
- Contract suite: **2/2 unittest tests PASS**, including modified authority bytes; synthetic controls are never admitted scientific cells. Expected preimplementation RED was followed by GREEN.
- All six authority inputs remain byte-identical after execution. Entire incoming journal is preserved as the exact prefix of the successor.

Accepted checkpoint SHA256: `37a1d5d738f2d64fba0e23ab7b19d53f58acef22f776735a14c98e6524e284ba`.  
Raw SHA256: `e4775af028c0d8bd0d20b28f707d00ad61eb1e81b31c520f51c438509285cb13`.  
Validation SHA256: `6089770aec4d21efcc9656c4741a2281cecca0568e7a29d19039a3a58f8f8705`.  
Postaccept SHA256: `cc466dbd57a389d17c6a93bba67358c0ac778aff4cca6f30a698abf337a76dcc`.  
Journal successor SHA256: `efd137b04f971145d78f438215d82975acd0ab9d3986583151521f279bc02388`.

The previous V107 mutation report used inequality controls. V109 strengthens this specific technical test by actually feeding altered records through the validation function and recording the invariants that fail. This is a new test implementation; no claim or alteration of historical validation is made.

## Runtime and backend

ACTUAL_RUNTIME: available local Linux/Python, exact Fraction arithmetic, standard library; connected GitHub read access and source-file retrieval verified. Model setting unchanged; SWITCH_STATUS=NOT_NEEDED. Shared core/versioned schema registry not available in the scoped evidence; existing V107/V108 format was extended with a distinct V109 schema.

COMPUTE_BACKEND=LOCAL_RUNTIME; GITHUB_WORTHWHILE=NO; GITHUB_WORTHWHILE_GATE=PASS. Pre-run estimate1–10s from measured V1072.326s plus finite mutations. Observed four-command wall total=0.139049s. This excludes source retrieval, code development and delivery. GitHub queue/setup overhead unmeasured; building/registering/dispatching an extra workflow offered no material benefit. No paid/external compute, shards, merge or long-run recovery required. No launch instruction applies.

## Gates and limits

| Gate | Status / scope |
|---|---|
| Q identity / TARGET_Q | PASS, Q048 only |
| case integrity / no repeat | PASS, immutable evidence; new bounded V109 task |
| journal continuity | PASS, exact incoming-byte prefix |
| source / specification freeze | PASS, raw-byte and canonical-row hashes; frozen spec |
| mandatory result / final result | PASS, this one consumer admission only |
| anti-ping-pong / termination | PASS, one new cell, then one return to ingestion |
| claim strength | PASS, INCONCLUSIVE; no complete histories/NativeP6/closure |
| README / repository integration | UNRESOLVED, HTTP403 blocked writing; proposed README section delivered |
| launcher / program registry | NOT_APPLICABLE to local run; program ID is LOCAL_NOT_REGISTERED |
| checkpoint resume / merge | NOT_APPLICABLE, one finite admission; no continuation authorized |

## GitHub memory and upload

MEMORY_BACKEND: GITHUB.  
REPOSITORY_REFERENCE: Morfindien/Bubbleverse@ab2822e44b35c507deea430e7c92d5d0c4e0e991.  
MEMORY_READ_STATUS: VERIFIED for the relevant scoped records and complete untruncated tree.  
MEMORY_WRITE_STATUS: FILES_READY_FOR_MANUAL_UPLOAD.  
MEMORY_LINKS_UPDATED: proposed only, in this report, journal append and README_Q048_V109_SECTION.md.  
MEMORY_BLOCKER: create-branch call for `codex/q048-v109-source-correct-consumer` returned GitHub HTTP403 `Resource not accessible by integration`. No branch, commit or PR was created.

Upload the individual files listed in the output manifest at repository root, following the existing Q048 naming convention. Preserve every historical artifact. Add the supplied README section to the front/current-state area, linking V109 report/checkpoint/handoff. Append the journal event once, using task fingerprint as idempotency key; the full successor is also delivered. If main advanced, reconcile against the latest state before changing derived pointers. Mark the V109 task completed and the route V108 Ingestion → V109 Builder → Result Ingestion; no next scientific cell is authorized here.

Reproduction uses Python standard library, the frozen spec and exact six pinned inputs in one directory. Five inputs are at the inspected GitHub base; V12 raw guard can be retrieved by filename `q048_guard_local_v_result_v12.json`, Library ID `libfile_f8cfc5fd42988191ba68db41eb12641f`, then verified against its SHA256. Supply `--inputs INPUT_DIRECTORY --out NEW_OUTPUT_DIRECTORY` to the four scripts in the order in EXECUTION_V1.json, copying the frozen SPEC into that new output directory. Existing raw/checkpoint/result files are intentionally not overwritten. Do not rerun merely for formatting; these commands describe reproducibility.

## Return

Return exactly once to **Result Ingestion & Routing2.1.0**, with the handoff, checkpoint, raw/validation/postaccept, execution/spec, output manifest and complete journal. Ingestion is not executed in this Builder turn. Q048 remains ACTIVE/INCONCLUSIVE. **STOP at960.**
