# BUBBLEVERSE — Q048 V104 V96-LINK REANALYSIS RESULT V1

EVENT: `LOCAL-Q048-V104-V96-LINK-REANALYSIS-990-980-V1`  
ENGINE: `BUBBLEVERSE.MATHEMATICS 2.1.0`  
VERIFIED TIME: 2026-10-19T17:53:20.422518+00:00 UTC; 2026-10-19T19:53:20.422518+02:00 Europe/Copenhagen  
CURRENT_Q / TARGET_Q: Q048 / Q048; authorized Q001–Q048  
WORKFLOW_STATE: READY_FOR_HANDOFF  
SCIENTIFIC_STATE: INCONCLUSIVE  
TECHNICAL_STATE: PASS  
ANALYSIS_KIND: NEW_VERSIONED_REANALYSIS_NOT_RECOVERED_V96

## Exact question

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

## Result

Jim explicitly authorized a new versioned mathematical reconstruction of the missing V96 link. This analysis therefore does **not** claim to recover or recreate the lost historical bytes of `q048_moving_h_domain_result_v96.json` or `q048_moving_h_domain_verifier_recomputation_v96.json`. Historical V96–V103 records remain unchanged.

The fresh 990→980 theorem was recomputed from the exact recovered historical captured inputs. All 12 conclusion-critical input files used by the analysis match the V96 manifest byte sizes and SHA256 values. Row46 primary/control hashes also match the recorded historical bindings.

The source prefactor is corrected prospectively to the pinned HyRec value `3.016103031869581e21`, rather than the historical proof-family literal `3.016101031869581e21` (relative change ≈ 6.63107760164e-07).

**PASS_FRESH_SOURCE_CORRECTED_990_980_THEOREM**

- cell: z=990→980, a=[1/991,1/981]
- parent: exact accepted V95 actual109/frontier990 checkpoint
- fixed branches: q_L=10^-6 and q_R=0
- fresh `K_upper` = `2493577725162681856783/500000000000000000` ≈ 4987.15545032536
- fresh conservative connected whole-cell lower = `50514140794199/100000000000000000` ≈ 0.00050514140794199
- both values exactly equal the historical accepted V96 theorem values
- source/background/atomic positivity: PASS
- corrected-source upper-H barriers: PASS for both branches
- C-factor positive-complement certificate: PASS
- thermal inward-face certificate: PASS for both branches
- no source-state or physical reset
- no actual consumer executed

A domain cross-check was run at both `w ∈ [-10^-6, 1/100]` and the wider `w ∈ [-10^-6, 1/50]`. Both pass, and both produce the same `K_upper` and conservative connected lower. Thus the theorem does not depend on resolving which of those two retained thermal-width conventions should be used for this fresh source-corrected link.

## Independent entrypoint verification

`Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json`: **15/15 PASS**. The verifier does not import the producer. It does share the exact historical captured inputs and interval/helper modules, so this is independent theorem recomputation at the entrypoint/code-path level, not independent physical evidence.

## Scientific effect

This fresh result removes the **mathematical source/domain uncertainty for the 990→980 theorem itself**: the corrected pinned source still proves the same K/lower theorem that historical V96 supplied.

It does **not** retroactively turn the new result into historical V96 evidence, does not rewrite V97/V100/V101/V102/V103, and does not by itself authorize an actual consumer or close Q048. The current authoritative later state (actual111/frontier970, other three frontiers1440; V102 970→960 conditional; NativeP6/full four-case x_e/tau still unresolved) is preserved exactly as received.

The next required action is one Result Ingestion disposition: determine whether this fresh substitute theorem is sufficient to discharge the historical parent-source/domain blocker prospectively and, if so, select the single next material Q048 task. Do not rerun V96 recovery and do not treat this V104 result as recovered bytes.

## Provenance

- raw: `Q048_V104_V96_LINK_REANALYSIS_RAW_V1.json` SHA256 `1e7d64d7f22981e09bf937dad54e0387344453591f4d527f133deb7a33c9c7e9`
- verifier: `Q048_V104_V96_LINK_REANALYSIS_VERIFICATION_V1.json` SHA256 `1c0b460cc1138b38b4aecb8e736460afd12cecf38739642ffaa35173e4ef6c6a`
- producer: `q048_v104_v96_link_reanalysis.py` SHA256 `f69ffa5de9f605f95df0e5dc42922b16758055cf498842b0ba52049c94997abb`
- verifier code: `q048_v104_v96_link_verify.py` SHA256 `2e0999d87655c22285d10bc9044e5fe8dd180c00d865d4133ab20bf5e6c868cd`
- recovered evidence package: `Q048_V96_FULL_RECOVERY_COMPLETE_PACKAGE_V1.zip` SHA256 `2661ad7210fc4087ec3151a346c8900bd2016bfc7f285b39b8682adb1c258b29`
- original historical V96 raw expected SHA256 remains `a2757a2804d7e43629f0361b9664deaadb8f93d0c4af1d47707ad87f189c81b0` and was **not** recovered.

- `Q048_V104_V96_LINK_REANALYSIS_ACCEPTED_CHECKPOINT_V1.json` — accepted fresh theorem checkpoint; SHA256 `4cac1a8fb598001c6907163752a7a9bf6005de649546fade84658bdb0627b691`.
