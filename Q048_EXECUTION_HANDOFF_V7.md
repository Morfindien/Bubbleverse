# BUBBLEVERSE — EXECUTION / NUMERICAL HANDOFF V7

Date/time: 2026-10-12T21:58:34+02:00 Europe/Copenhagen

## A. CURRENT Q

CURRENT Q: Q-048 — PROPOSED_UNVERIFIED
CASE ID: NOT_ASSIGNED

Scientific question: For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

## B. RECOMMENDED CHATGPT SETTING

RECOMMENDED CHATGPT SETTING: GPT-5.6 / current GPT-5.6 Sol with High reasoning.
REASON: the next task is a bounded source-pinned interval-proof implementation, not a broad long-horizon research campaign. The decisive compute is external GitHub execution. Astra Max is not required and is not assumed available.
FALLBACK: strongest actually available code/reasoning Work-style setup if a material proof conflict appears.

## C. PLUGIN / CAPABILITY PLAN

USE: connected GitHub read-only inspection; attached Files/journal; exact Python/rational proof machinery already in the repository.
UPSTREAM CONTROL RETAINED: Wolfram exact He1f/He2 identity check from Mathematics-007.
NOT REQUIRED: literature search, likelihood tools, MCMC/nested sampling, native CLASS capture, GPU/HPC service.

## D. EXECUTION DECISION

EXECUTION MODE: EXISTING MOTOR + PROGRAM + RELEVANT READ-ONLY CAPABILITIES.
No new reasoning motor is created. A new runnable program is required because the remaining task is an actual validated interval IVP calculation.

## E. SCIENTIFIC REQUIREMENT

1. Preserve all frozen Q048 inputs, source commit, V5 parent, V6 endpoint and fixed accepted z_reio.
2. Camspec EDE only: certify a trajectory-correlated (phi,X) source-real tube through z=2870 and check the exact source guard on every whole-state cell, or return a bounded scoped obstruction.
3. Continue both EDE positive-w intervals through He1f 4600->3550 and He2 3550->2870 using the Mathematics-007 sign rule.
4. Recheck the source-real He1f/He2 Saha transition at z=3550.
5. Compute conditional H-entry q at z=2870.
6. Stop. Do not start H/frec/cutoff/full-xe/tau execution.

## F. JOURNAL CONTEXT

KEEP all prior scientific state and failures. ADD this V7 execution design only. The canonical delivered Q047_SAMLET_JOURNAL.md prepends the V7 design and preserves the complete Math007 journal byte-for-byte as its tail.

## G. SOURCES AND PROVENANCE

Scientific source: mwt5345/class_ede commit 5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Bubbleverse inspected base: Morfindien/Bubbleverse commit 2bc190aeb1a2659fbc9bc0d402159c7768c6b15a.
Parent execution evidence: Q048-STRUCTURAL-V6 / GitHub run 38293480870.
Mathematics input: I-PROPOSED-Q048-MATHEMATICS-007.
Question SHA256: c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436.

## H. EXISTING MOTOR ASSESSMENT

EXISTING MOTOR SUFFICIENT: YES.
SELECTED MOTOR: AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.
No separate new motor prompt is needed.

## I. BUBBLEVERSE GITHUB SEARCH

Current HEAD inspected read-only: 2bc190aeb1a2659fbc9bc0d402159c7768c6b15a.
No V7 direct-guard/He1f-He2 target exists.
REUSE: Q047/Q048 exact rational backend; Q048-STRUCTURAL-V6 source-root and phase machinery; permanent launcher.
PATCH/EXTEND: V6 architecture into one new bounded V7 proof target.
REFERENCE ONLY: superseded V2-V5 continuation targets and historical failures.
CREATE: V7 kernel, runner, tests, config, package checker/lock, workflow, registry entry, README section, installation guide, differential repository patch.
LAUNCHER: unchanged.

## J. NUMERICAL SPECIFICATION

Camspec guard state: phi, X with frozen source ODE phi_u=X/H, X_u=-3X-V_phi/H.
Direct source acceptance: equivalent positive margin 3*B(a)+X^2/2+V_floor-V_e > 0 on every certified whole-state tube.
Target a=1/2871. Mandatory milestones: 1/4601, 1/3551, 1/2871.
Camspec initial relative step 1/64; max 5000 accepted cells; max 14 halvings; 5400 s scientific budget.
Thermal whole domain w in [0,1/50]. Hillipop relative step 1/32 with inherited V6 full-transfer guard.
Positive-w primary comparison uses L exp(-d_max) for the lower homogeneous term; independent rational Bernoulli control is intersected with it.
Likelihood/priors/sampler/seeds: NOT APPLICABLE.

## K. PROGRAM_ID

PROGRAM_ID: Q048-GUARDCONT-V7

## L. BUBBLEVERSE START REGISTRATION

LAUNCHER: 🚀 BUBBLEVERSE START
LAUNCHER FILE: .github/workflows/00-bubbleverse-start.yml
PROGRAM_ID REGISTERED REMOTELY: NO — no remote mutation was performed.
PREPARED REGISTRY ENTRY: YES.
REGISTRY: bubbleverse_program_registry.json after running q048_v7_repository_patch.py on the exact inspected base.
TARGET: .github/workflows/q048-guard-continuation-v7.yml
LAUNCHER_GATE: prepared for PASS; final installed gate is enforced by q048_guard_package_check_v7.py.

## M. GITHUB RUNTIME ASSESSMENT

Prior V6 measured EDE workers were only minutes, but V7 has a larger validated direct trajectory. The Camspec scientific work budget is capped at 90 minutes; worker job timeout is 120 minutes. Collector/full replay validation is also capped below 120 minutes. This remains below the current standard GitHub-hosted six-hour maximum job execution time.
Single-job risk: MODERATE for Camspec, LOW for Hillipop.
Execution strategy: PARALLEL two-EDE matrix, then single collector/full replay validator.
Estimated GitHub jobs: 4 total (preflight + 2 matrix workers + collector).
Checkpoint: YES — provisional Camspec progress every 100 accepted cells plus final checkpoint; no automatic infinite chain.
Merge: YES — case-preserving, no averaging.
Test jobs: preflight plus full collector replay validation.

## N. JOB PLAN

preflight -> camspec-ede_n3 and hillipop-ede_n3 in parallel -> collector/full proof replay -> final artifact.
A Camspec inability to separate the guard within frozen limits is a successful bounded UNRESOLVED obstruction report, not physical falsification.

## O. RESULT TEST PLAN

T001 Q/source/config/journal/Git-blob pins.
T002 V6 positive endpoints and inherited Hillipop guard.
T003 direct Camspec guard margin on every certified cell.
T004 full stored-cell recomputation in collection.
T005 positive-w sign-aware primary comparison.
T006 independent rational comparison.
T007 exact fixed phase partition and He1f/He2 transition control.
T008 H-entry q recomputation.
T009 two-EDE job completeness and merge context.
T010 launcher/registry/README/journal/repository consistency after installation.

## P. FILE DECISIONS

REUSE: current V6/V5/Q047 dependencies and permanent launcher.
CREATE: all V7 files delivered with this handoff.
PATCH: registry and README only, through exact-base fail-closed script.
UNCHANGED: all scientific source/input/parent files and launcher.
REFERENCE ONLY: old superseded Q048 workflows/results.

## Q. README STATUS

README ACTION: UPDATE, differential only.
FILE: README.md.
Prepared section: README_Q048_V7_SECTION.md.
README_GATE: PREPARED_NOT_INSTALLED; package checker enforces PASS after exact differential patch.

## R. ACTUAL MOTOR / PROGRAM FILES

Actual individual files are delivered separately; no archive.

## S. EXECUTION

After installing the individual files and applying the differential metadata patch:
OPEN 🚀 BUBBLEVERSE START -> PASTE Q048-GUARDCONT-V7 -> Run workflow.

## T. EXPECTED OUTPUTS

Per-EDE reports/checkpoints, optional provisional Camspec progress, and q048_guard_final_v7.json. Expected scientific state after a successful technical run remains conditional; full Q048 cutoff/x_e/tau products are not part of V7.

ACTUAL COMPUTED V7 RESULT: NOT YET COMPUTED.

## U. PASS / FAIL GATES

Technical PASS requires source/config/journal identities, two EDE reports, compatible run context, full proof replay, package/launcher/registry/README consistency.
Scientific component PASS_CONDITIONAL requires Camspec direct guard to z=2870 and both EDE thermal continuations/H-entry q.
If direct guard remains unproved within frozen bounds: guard_continuation_gate=UNRESOLVED, not physical FAIL.
FINAL_RESULT_GATE remains UNRESOLVED for the exact Q.

## V. RETURN TO BUBBLEVERSE

Return CURRENT Q, PROGRAM_ID, full journal, raw/final V7 artifacts, stable source IDs, exact source/repository commits, validation status, any bounded obstruction, and unresolved native/cutoff/full-history products to RESULT INGESTION & ROUTING ENGINE.

## W. START THIS

START THIS: Q048-GUARDCONT-V7
