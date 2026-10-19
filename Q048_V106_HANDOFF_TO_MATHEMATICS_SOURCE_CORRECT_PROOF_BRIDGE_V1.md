# Q048 V106 — handoff to Mathematics 2.1.0

STATUS: **CONTINUE / NEW MATERIAL BRIDGE TASK**  
TASK_ID: `LOCAL-Q048-V106-SOURCE-CORRECT-PROOF-BRIDGE-980-970-V1`  
TASK_FINGERPRINT: `baba4158ce40821351a73bf8e94622628deffb1e2e12a439e6883012f203b8e2`  
CURRENT_Q / TARGET_Q: Q048 / Q048

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

## Objective

Create exactly one **new source-correct mathematical proof bridge for 980→970** by binding the already validated V100/V103 local theorem content to the new V105 source-qualified actual110/frontier980 parent. Do **not** rewrite or relabel historical V97/V100/V101, and do not rerun the full V100 proof unless a concrete applicability check fails and recomputation is necessary to resolve it.

## New information that makes this nonduplicate

V103 already established corrected-source admissibility for the V100 local source/H/C transfer conditional on V97, but stopped because no source-qualified upstream parent was available. V104+V105 now provide a distinct source-qualified lineage through actual110/frontier980. V105 numerically matches the V97 endpoint/K/lower required by the V100 proof, but has a different provenance identity. That changed parent evidence is the material reason for this Mathematics task.

## Required inputs / pins

- V105 accepted parent checkpoint SHA256 `cedaef00bab86ac24bb876ae475e5dff15f8b97a0a55f83d9ba12d25da07b098`; accepted state actual110/frontier980; endpoint a=1/981, E=`13327406922059142279/250000000000000000`, Y=`1696710572528996873/40000000000000000`, Vbar=`10438035734386161987/1000000000000000000`.
- V100 accepted proof SHA256 `f656241001cd54f6505e1a79705cfe51dc04bd25954f205c9f0525c18e762df6` for cell 980→970, thermal domain `[-1/1000000, 1/50]`.
- V100 raw full gate SHA256 `5efd0103b8d08b723c408a98099275a0ca1cb9dd8cce1f25fb8ce0c705986a2d`.
- V100 independent thermal verification SHA256 `9e9ca61068b7045cae4e51f9cb5d0e5cb62c1cfab0b10eeb4be8f65ef90da8e6`.
- V103 corrected-source certificate SHA256 `3f26ed2bed293b2489f36dd59f63b6ea623365fea0d24216ed7cfaadb4207edb` and validation `8ce6e107ab9f7cd71a61056953a0c520b1e11ab5ceef4c9713a965632ea05a55`.
- Correct SAHA_FACT `3.016103031869581e21`.
- Historical V97 checkpoint `be53c4e56133bfce66108a5bc81e9ba8ce49334c2cfee4cef21306c652663da8` is reference-only for exact numerical-binding comparison; it is not the new parent authority.

## Mandatory checks

1. Verify the V105 endpoint equals exactly the numerical parent values actually consumed by V100; record identity distinction explicitly.
2. Rebind V103's corrected-source transfer to V105 as the source-qualified parent and show the V100 source/H/C premises remain valid.
3. Verify retained atomic, C-factor, comparison/Riccati, thermal and guard-glue premises remain applicable on 980→970 without physical reset or changed captured inputs.
4. Preserve thermal proof domain `w=[-1e-6,1/50]`, accepted z_reio, latch/reset definition and original Q048 physics.
5. Produce a new V106 theorem/acceptance record with new hashes/provenance and **zero actual cells**.
6. Use a separate verifier for the bridge/binding logic; do not claim physical independence from shared historical source enclosures.

## Success / fail / stop

SUCCESS: one V106 source-correct accepted proof bridge for exactly 980→970; full source-qualified parent chain through V105; verifier PASS; zero actual cells.  
FAIL: any required exact binding, source transfer, domain premise, guard glue or verifier check fails.  
STOP: after this one proof bridge. **No actual consumer and no work below970.** Return exactly once to Result Ingestion 2.1.0.

Q048 remains ACTIVE / INCONCLUSIVE throughout this task.
