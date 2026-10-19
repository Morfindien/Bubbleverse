# Q048 V90 — frozen input map and execution identity

## Scope

- Task: `LOCAL-Q048-POST-V89-MOVING-H-DOMAIN-1020-1010-MATH-V1`
- Task fingerprint: `fabe82fad1c1a3007cc97e8037d854e6c451259b00942ebb01c91bb12eee3745`
- Execution fingerprint: `4288a871e508ebdc92130434fe91c1b69f62416330e5c638987320fd3d4fb743`
- Frozen spec SHA256: `cdac544e3e44de61c43e9318d5f03cc0c7d0939f0cb95bae028a5b98219eacd7`
- Proof cell: z=1020→1010, a=[1/1021,1/1011]
- Actual must remain 106/frontier1020
- Max new proof cells: 1; max new actual cells: 0; science budget: 300s

## Consumed and hash-verified inputs

| Path | Bytes | SHA256 |
|---|---:|---|
| `inputs/Q048_FREC_MOVING_H_V89_NEXT_MATHEMATICS_TASK_V1.json` | 28303 | `6070389b7765aa892bbbf02dd821ee442c21c75c942b7046f75d121285a4beec` |
| `inputs/q048_frec_moving_h_accepted_checkpoint_v89.json` | 7115 | `96b2b93050581d5b3c82e5023acacb30e9a723008d5067bf88fc3a880a235158` |
| `inputs/q048_guard_local_v_result_v12.json` | 1198030 | `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5` |
| `inputs/q048_guard_local_v_validation_v12.json` | 206698 | `51e4dfd3ef7a429b459af73b125d251e789bb0ac9244ef7630d5a44d4d99b554` |
| `inputs/q048_prefix_config_v1.json` | 105567 | `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b` |
| `inputs/q048_p3_scaled_raw_result_v2.json` | 699697 | `fe9070d5054a4aac84cd342332dcec4b4895cc95d316ef527ad6a4a012c4c44c` |
| `inputs/q048_p3_scaled_transformed_log_tables_v2.json` | 3958952 | `ac162812185f862eb845019a6910dda94d40c8e962a9a7fc0b360e3b968075cb` |
| `inputs/q048_full_tube_reuse_v1.py` | 10171 | `e975c73f7e767442cb0084c61791686061be6cd045378c8fbc48ba412bd454dc` |
| `inputs/q048_post_event_state_tube_v1.py` | 12423 | `445b27a81502402029c69d62b63b21db757321104842e30fbdae449c56beb01b` |
| `inputs/q048_p3_scaled_kernel_v2.py` | 15855 | `168275855fe8d36da42c6e997375444dc7eb8f2dc2f47132f11d888d575f85dd` |
| `inputs/q048_p3_scaled_arithmetic_v2.py` | 5988 | `d0b6ab8022b3c66b90be1108a4a2c708b7c1112a0d4201e18335897db94586fa` |
| `inputs/q048_prefix_v1.py` | 17198 | `00414ccd02d79130f38ca00a8ba397a61f33bac1ed018b50ab71af73d3e62516` |
| `inputs/q047_math_v1.py` | 12617 | `d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d` |
| `inputs/q047_certificate_v1.py` | 15302 | `11e87a05bca511c0b421752151082a2fecb9030c7e8f5949365566b9960c1240` |
| `inputs/q047_precursor_check_v1.py` | 29808 | `634ccfb21df8b85a15b5c1917e6a06917f8a28a97d6ed7a4208c14b2688268e5` |
| `inputs/source/q047_math_v1.py` | 12617 | `d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d` |
| `inputs/Bubbleverse_Matematikmotor_2.1.0-46.md` | 56414 | `3594851ec3b827d643ba89c410a04ca454e80648011dde549f229a69f085475b` |

## Parent provenance not consumed as bytes

- V89 raw SHA256: `7bc860409d0a208008999da84b44587ba7740a6750450a367fe4b9e4f75307e7` — inherited provenance only; bytes not consumed/reconstructed.
- V89 validation SHA256: `efe4abfb468ea6e35944728fbd4369086d06f19e1de69ce3dcbdddeb89069967` — inherited provenance only; bytes not consumed/reconstructed.
- Consumed V89 accepted checkpoint SHA256: `96b2b93050581d5b3c82e5023acacb30e9a723008d5067bf88fc3a880a235158`.

## Guard binding

- V12 raw SHA256: `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`
- V12 validation SHA256: `51e4dfd3ef7a429b459af73b125d251e789bb0ac9244ef7630d5a44d4d99b554`; 6566/6566 checks, 24/24 mutations.
- Primary row43 SHA256: `b8027c12855303ffc33130edf153afddf122745d0ad1f00cb381f60d58d4f828`; exact left glue to V89 endpoint.
- Control row43 SHA256: `37ba71d2f6a8c5191859e5e090730a1e88486867784e930364217f3b4b61092c`; guard-only.

## Frozen code pins

| File | Bytes | SHA256 |
|---|---:|---|
| `q048_v90_proof_contract.py` | 6225 | `8fddc247a926905e2c37ccd3e0a1cc8e8ce516ba270def5142f83a28b80df69e` |
| `q048_moving_h_domain_v90.py` | 10077 | `8ca2d233068ba179dd57e1751925c81a7281625d76c09782185b733a4bda8327` |
| `q048_moving_h_domain_verify_v90.py` | 18058 | `e4f758dde5cbafb43e38750b57caae3893d2fdc536f0b9a6b273b6a45175463f` |
| `q048_moving_h_domain_accept_v90.py` | 7412 | `677eb53949afbc83709a7c1842a4ef21045ca461923e10f9c59ff82b10f27d96` |
| `q048_v90_import_probe.py` | 2244 | `218d8ac8499de82b2253842e749c4b833f266956dc63f56cc09b6efdf0ebf975` |
| `q048_v90_freeze_and_execute.py` | 3842 | `cd3ebb05e3fb1d3036902c34da06f69903c0b512ce0c40df34d9c9afb5108e3f` |
| `test_q048_moving_h_v90.py` | 3049 | `846864b473dc00635bffdedfe590dfdfe6d45e7e1926e2cefd4ce743fd025d4c` |
| `test_q048_v90_layout.py` | 1031 | `cbf1180ac960ff169dd26c5457d4a35dd866c90e68831d3e4b161addbaf03980` |

## Pre-freeze audit note

Before freeze, a static audit corrected the row43 list binding and stale transformed-reference strings. The frozen spec was regenerated after those edits. No science had run and no V90 science output existed at that point. After freeze: 0 edits, 0 retries.

## Import layout

- `inputs/q047_math_v1.py` and `inputs/source/q047_math_v1.py` are byte-identical and pinned to SHA256 `d8a6e8bc7dfc08f53b92a58a8d2b4dec3aee88be2dfdedff5b3800eb2e61937d`.
- Actual producer transitive import resolved the pinned producer/full_tube/kernel/root+nested math modules, invoked 0 scientific entrypoints and created 0 science outputs.
- Missing nested pin and wrong nested hash were rejected in preflight tests.
