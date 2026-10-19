# Q048 V107 — handoff to Execution/HPC/Motor-Builder 2.2.0

STATUS: **CONTINUE / SOURCE-CORRECT ACTUAL CONSUMER REQUIRED**  
TASK_ID: `LOCAL-Q048-V107-SOURCE-CORRECT-ACTUAL-CONSUMER-980-970-V1`  
TASK_FINGERPRINT: `4314813e9da301880e9c8fd9e3246921710be110cd2d19f457e814c21150cd3d`  
CURRENT_Q / TARGET_Q: Q048 / Q048

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

## Objective

Execute exactly one new **source-correct reanalysis-lineage actual consumer 980→970**. Authority parent is V105 actual110/frontier980; theorem authority is V106 accepted source-correct proof bridge. Historical V101 is implementation/reference evidence only and MUST NOT be replayed, relabelled or overwritten.

## Authority inputs / pins

- V105 parent checkpoint SHA256 `cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098`; state actual110/frontier980; endpoint a=`1/981`, E=`13327406922059142279/250000000000000000`, Y=`1696710572528996873/40000000000000000`, Vbar=`10438035734386161987/1000000000000000000`.
- V106 accepted proof bridge SHA256 `5294bed5e3d32d71e396d933a5387c8c8f7538e1bc55c432b0b151fc0e9f9fe3`; raw `e7b526416746e83005d353e4d6107c405cbb05646520f9fb0fea8b8756baef11`; verification `e0793a3c8b543c5e8d6646c4df43d7f226759cced2aa471f1baeec1d708e2375`.
- V106 theorem: cell 980→970, K_upper `5080670052472740707779/1000000000000000000`, connected lower `492108035315773/1000000000000000000`, thermal domain `[-1/1000000,1/50]`, SAHA_FACT `3.016103031869581e21`.
- Guard row47 primary hash `01e9f92295d60287f74a2760c1d38da42d2d37098a4d0dd32d1782dbf757b5ea`; exact left E/Y/V matches V105; `source_state_reset=false`; whole-cell qualified/accepted/committed.
- Historical V101 consumer implementation reference: `q048_v101_actual_consumer.py` Git blob `c7524b8996fd1ed16522b3b1fdfca378b7866786` and historical accepted checkpoint `270e615ae9ee8455ce5ddb1c0d28ff24efa478db1db0e09c55ce8015bf434686`. Use only as implementation/expected-endpoint cross-check, not authority.
- Expected committed row47 endpoint for validation only: a=`1/971`, E=`2575086164999170119/50000000000000000`, Y=`40971463401285721027/1000000000000000000`, Vbar=`10091499069585277963/1000000000000000000`. Output match alone is not identity.

## Required execution

1. Pin V105 and V106 authority bytes/hashes before execution.
2. Bind row47 left exactly to V105 endpoint; no reset/refit/recapture.
3. Consume V106 K/lower; do not substitute historical V100/V101 authority.
4. Produce one candidate actual cell only: actual110/frontier980 → actual111/frontier970.
5. Use a separate verifier with semantic mutations sufficient to reject wrong parent, wrong theorem, wrong cell, wrong row47, altered SAHA, reset=true, historical-V101-as-authority, and below970 advancement.
6. Accept only after validation and postaccept checks.

## Success / rejection / stop

SUCCESS: exactly one new source-correct reanalysis-lineage actual111/frontier970, endpoint equal to committed row47 primary, consumed V106 theorem pins exact, no reset, validation PASS, postaccept PASS, zero new proof cells.

REJECTION: any authority hash, glue, cell identity, theorem, source-correct pin, verifier, or postaccept invariant fails.

INCONCLUSIVE: required execution/provenance cannot be established without changing frozen physics or authority.

STOP after this one cell. **No below970 work.** Return exactly once to Result Ingestion 2.1.0.

## Frozen

Exact Q048 physics/question; captured effective inputs; fixed accepted z_reio; latch/reset definition; V105 parent; V106 theorem; row47 semantics; historical V97/V100/V101 records.

Builder prompt verified in repository as `Bubbleverse_Execution_HPC_Motor_Builder_v2.2.0-33.md`, prompt version 2.2.0, Git blob `e6f8cef22d4fc45b5c5b3d645539b05caf3c2c9a` at repository head `8fc2c0bd636f94867e9b12c655369c9d45687e6b`.
