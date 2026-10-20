# Q048 V109 — handoff to Builder 2.2.0

STATUS: **CONTINUE / ONE MATERIAL SOURCE-CORRECT ACTUAL-CONSUMER TASK**  
TASK_ID: `LOCAL-Q048-V109-SOURCE-CORRECT-ACTUAL-CONSUMER-970-960-V1`  
TASK_FINGERPRINT: `042bf80b3e652120e1a00fd33a00a9aef2c907c0ec05f112497540a57d43f5cd`  
CURRENT_Q / TARGET_Q: Q048 / Q048

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

## Objective

Execute exactly one new **source-correct reassessment-lineage actual consumer 970→960**.

Parent authority: `Q048_V107_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json` SHA256 `3876328fa6acfd5a79c01505526de8e2b6d384b06241685eb359fa5635747e24`.

Theorem authority: `Q048_V108_SOURCE_CORRECT_PROOF_BRIDGE_ACCEPTANCE_V1.json` SHA256 `4356c7f697c2df5897a64bfb7dc5f155af0b5dbaea7345f1f0af804d6963c5e7`; raw `df25316ce4a19f9177d99d3d256754dc640773f4ac9d0420d02c2f8e7412e928`; verifier `c201bbdf75f7529f3c3f3d03a6c75df2197542d63fcad2d86d60c740e1ab7c8b`.

Retained theorem: K=`1001919080623370229873/200000000000000000`, connected lower=`479774678212513/1000000000000000000`, correct SAHA_FACT=`3.016103031869581e21`.

## Guard / endpoint binding

Use committed primary **row48** from the already recovered V12 guard source:

- guard source SHA256 `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`
- primary row SHA256 `98b31afe3cc6371533b59edf6ef673c0da6219122d145a8ca997276c270301cf`
- cell z=`[970,960]`, a=`[1/971,1/961]`
- E_input_left=`2575086164999170119/50000000000000000`
- Y_left=`40971463401285721027/1000000000000000000`
- V_previous=`10091499069585277963/1000000000000000000`
- `source_state_reset=false`
- row is whole-cell-qualified, accepted and committed

The row must glue exactly to V107. Control row remains guard-only.

Expected endpoint is a cross-check, not authority: a=`1/961`, E=`49737668672811936943/1000000000000000000`, Y=`39560432998711765483/1000000000000000000`, Vbar=`4876592093839665491/500000000000000000`.

## Required Builder behavior

1. Freeze V107 parent, V108 theorem authority and primary row48.
2. Verify exact hashes and exact left glue before consumer execution.
3. Consume the V108 theorem exactly once; do **not** rerun/reprove V102/V108.
4. Produce at most one new actual cell: expected state **actual112/frontier960**.
5. Bind new connected lower to `479774678212513/1000000000000000000` and K_upper to `1001919080623370229873/200000000000000000` only if theorem/consumer checks pass.
6. Use separate validation and postaccept checks, including semantic mutations against wrong parent/theorem/row/reset/cell/endpoint/below960.
7. Preserve historical V101/V102 and all prior reassessment records unchanged.
8. Return exactly once to Result Ingestion 2.1.0.

## Success / failure / stop

SUCCESS: one validated/accepted source-correct actual112/frontier960, exactly one new actual cell, zero new proof cells, no reset.

FAIL: any parent hash, theorem hash, row48 glue, source/reset, endpoint, verifier or postaccept invariant fails. Preserve first material failure; do not tune or relabel history.

STOP: after one cell. **No work below z=960**.

## Forbidden

No proof rerun; no historical V101/V102 replay/relabel; no physical reset/refit/recapture/tuning; no below960; no NativeP6 claim; no Q/model change; no Q closure.

## Engine / repository

Builder 2.2.0 verified via `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0-33.md` at `Morfindien/Bubbleverse@d910cc2ea09e9251f6f241992520f57d4609c62f`; Git blob `e6f8cef22d4fc45b5c5b3d645539b05caf3c2c9a`, exact prompt SHA256 previously verified `49175d52ac1e7ae4a04551950eb4b05bddbada29d956eb6c20782e610c6f6de1`.

Preparation is not execution. This ingestion grants the bounded consumer route; Builder must still perform and validate it.
