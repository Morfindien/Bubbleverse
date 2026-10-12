# Verification

**CLEANUP_PARTIALLY_VERIFIED.** Same environment before/after: Python 3.12.14. Base commit: `24f380ba4bc0129ac3bfcd1dcb105c597191b47a`. No cleanup regression was found in the checks performed. Full historical production behavior is not qualified by this cleanup.

| Check | Baseline | After cleanup | Scope |
| --- | --- | --- | --- |
| Python syntax | PASS: 509 | PASS: 559 including archives/aliases and new code | In-memory compile |
| Bash syntax | PASS: 146 | PASS: 171 including archives/aliases | bash -n only |
| JSON syntax | PASS: 519 | PASS: 526 in final static pass | Later evidence JSON separately validated |
| YAML syntax | PASS: 320 | PASS: 320 | Includes 205 discovered workflows (plus six non-workflow files in that directory); no remote run |
| Existing Q047/Q048 tests | FAIL: 68 tests, 64 pass, 3 existing issues, 1 skip | Identical issue names and skip | No cleanup regression |
| Q048 package/launcher | PASS | PASS | Hashes and existing local resolver; no dispatch |
| Q048 actual metadata replay | PASS: 20 pinned files, four cases | PASS: complete JSON identical except seconds/checked_utc | Zero new native/likelihood calls |
| Six old alias invocations | PASS | Identical exit/stdout/stderr | Q005 plan/preflight and four help interfaces |
| Layout/aliases/links/coverage | Snapshot recorded | PASS: 1,548 unchanged files, 96 archives, 73 aliases, 1,015 records | Original modes/hashes checked |
| New layout tests | RED: 9 initial missing-verifier failures | PASS: 12 adversarial fixtures | Hashes, permissions, traversal, aliases, links and coverage |
| Full native production | NOT_RUN | NOT_RUN | Pinned CLASS/Cobaya/PolyChord/data environments and compute unavailable locally |
| Live checkpoint/resume | NOT_RUN | NOT_RUN | No live state touched; original code/workflow paths preserved |
| GitHub workflow execution | NOT_RUN | NOT_RUN | Static validation is not a GitHub run |

## Exact baseline defects

- `q047_precursor_tests_v1.PrecursorTests.test_repository_gate_rejects_launcher_byte_change`: `EXISTING_REGISTRY_CHANGED`, because the inherited registry lock predates later entries.
- `test_q047_execution_v1.Controls.test_real_prepared_package_and_launcher`: `REGISTRY_ID`; the historical collection target is no longer ACTIVE in the unchanged registry.
- `test_q047_execution_v1.Controls.test_worker_cache_miss_and_rerun_never_call_native`: expected `EXACT_CACHE`, but existing `REGISTRY_ID` fails first.
- BLOCKED/SKIPPED: `test_q047_reconstruction_v1.ReconstructionGates.test_actual_c_runtime_capture_and_observation_fp_restore`; pinned native headers absent. Mandatory in the restored original native environment.
- Registered `Q039-IMPLBLOCK-V1` points to absent `.github/workflows/q039-implementation-block-intervention-v1.yml` already in BASE_SHA. Its catalog entry is BLOCKED. Registry status was not rewritten.

## Reproduction

From repository root:

```bash
python tools/check_repository_layout.py
python -m unittest discover -s tests -v
python q048_package_check_v1.py
python -m unittest -v q048_inputcheck_tests_v1 q047_certificate_tests_v1 q047_package_tests_v1 q047_precursor_tests_v1 test_q047_execution_v1 test_q047_reconstruction_v1
```

The last command retains the known baseline failures. Baseline/final static checks, unittest logs, metadata replay logs, alias-comparison JSON and the RED regression-test log are in `evidence/`. Actual replay input files were verified against the immutable contract; they are not regenerated or added to this cleanup package.

Only `file_sha256.README.md` differs in the Q048 package lock. Its exact old lock is preserved in `../history/`. Science/program/workflow/registry/journal pins are unchanged. Remaining production entry points have static coverage and schemas; they are NOT_RUN or BLOCKED pending their original prerequisites.

## Installation and review

Independent review findings were fixed with failing-before/passing-after controls; see REVIEW.md. Thirteen installer integration checks PASS; exact records are in evidence/installation-verification.json. Q047 reconstruction static and Q048 package checks PASS after the documentation fix.
