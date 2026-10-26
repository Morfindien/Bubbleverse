# Q052 V1 — canonical adoption and native-realization execution preflight

RUN_ID: `LOCAL-Q052-ADOPTION-AND-NATIVE-PREFLIGHT-20261026-V1-RUN`  
UTC: 2026-10-26T10:52:20Z  
Europe/Copenhagen: 2026-10-26T11:52:20+01:00  
CURRENT_Q = TARGET_Q = **Q052**  
CASE: `LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1`  
STATUS: **ACTIVE / NOT_YET_COMPUTED**  
STARTING MOTOR: `BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0`  
RETURN MOTOR: `BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0`

## Adoption

Jim's instruction to start Q052 is taken as the required human authorization to activate the already-selected scientific question. This does not claim that GitHub has been updated or that a native calculation has already run. Repository canonicalization remains a manual-upload/integration step. Q051 stays CLOSED / RESOLVED_WITHIN_SCOPE and its historical artifacts remain immutable.

## Exact scientific question

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

No scientific wording is changed from the Motor-14 proposal.

## New provenance finding before execution

The missing Q051 V7 transfer bundle was recovered from the user's Library. It binds Q051 back to the frozen Q048 capture `q048_prefix_config_v1.json` and Q050 common-background record `Q050_CLEAN_BG_BINDING_V1.json`. The exact Q048 accepted z=810 checkpoint was also recovered.

The checkpoint pins `hillipop-ede_n3` at actual127/frontier810 and gives the background anchor

- `a = 1/811`
- `E = 87861503356118157/3125000000000000`
- `Y = 22285530672339861267/1000000000000000000`
- `Vbar = 5587227468217201099/1000000000000000000`

with checkpoint SHA256 `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`. The common-background dependency is `Q050-COMMON-BACKGROUND-92de319899bf911563aff4d1`.

Crucially, Q051's mathematics quantified over matched validated z=810 hydrogen/temperature starts. The Q048 checkpoint provides an admissible start domain (`h<1`, retained bound `h<=99999/100000`, thermal deviation domain `[-1e-6, 0.02]`) rather than one unique thermodynamic start vector. Therefore the native Q052 run **must not choose an arbitrary point inside that domain**. It must reproduce/observe the concrete native z=810 thermodynamic state from the frozen hillipop-ede_n3 capture/source path, freeze that exact state, clone it into both arms, and then change only `q` (`1e-6` versus `0`). This is an execution clarification, not a new scientific assumption.

## Frozen identities

- Physics source: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
- Frozen capture SHA256: `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`.
- Q050 common-background binding SHA256: `bfbe380364983b166658793514526986ae61e0c37a67a07774375ef49a4f7481`.
- Q048 z=810 accepted checkpoint SHA256: `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`.
- Q051 global transfer input bundle SHA256: `b7edfbf830163cdc31b5e3af1a11717551a2eab4076cdad0481781ea9eea128b`.
- Q051 analytic envelope: `sup|Delta x_e| <= 0.0023814`; `sup|Delta tau_T| < 0.0421` (sharper `0.04209103698658`).

The frozen Q048 capture includes the exact hillipop-ede_n3 effective-background, precision and thermal-start hashes plus fixed accepted reionization redshift. New Q052 comparison must use fixed z, not tau shooting.

## Execution routing

`COMPUTE_BACKEND = GITHUB_ACTIONS` for the first native realization. This is a capability choice, not a speed claim. The current chat/container does not expose an executable pinned native class_ede checkout, while current Bubbleverse repository memory contains the permanent launcher/registry architecture and prior native CLASS runner paths at the same source lineage. Q052 runtime is unmeasured; the first bounded target must record setup/compile/native-run/validation timings.

Reserved local program identity: `Q052-NATIVEPAIR-V1` — **DRAFT_UNREGISTERED**. No workflow/registry write or dispatch is claimed. The Execution/HPC motor must search/reuse the existing Q048/Q045/Q042 native harnesses before writing new code and register the target only after static/preflight validation.

## Mandatory first-run sequence

1. Verify the exact frozen source/config/capture/background/checkpoint bytes and hashes.
2. Reproduce/observe the native hillipop-ede_n3 thermodynamic state at z=810 from the frozen capture path.
3. Verify its background anchor against the Q048/Q050 z=810 identity.
4. Freeze one common z=810 thermodynamic state.
5. Fork two arms with every setting identical except `q=xHeII`: `1e-6` versus `0`.
6. Run native low-z evolution to z=0 with unchanged literal selector/equality semantics and fixed reionization configuration.
7. Emit full `x_e(z)` and cumulative `tau_T(0,Z)` histories in common coordinates.
8. Compute realized `sup|Delta x_e|` and `sup|Delta tau_T|`.
9. Perform convergence/refinement and independent serialized readback or a second implementation-level check.
10. Compare the realized differences to Q051's analytic envelopes.
11. Stop after one validated pair or the first exact conclusion-critical blocker and return once to Result Ingestion & Routing 2.3.0.

Do not refit, tau-shoot, smooth/convexify selectors, change equality semantics, substitute background/start state, open a likelihood campaign, or generalize to all four configurations in this first Q052 run.

## Current scientific state

ACTUAL_COMPUTED_RESULT: **NOT_YET_COMPUTED**.  
EXECUTION_STATUS: **PLAN_READY / PREPARED_NOT_DISPATCHED**.  
RESULT_VALIDATION_STATUS: **NOT_RUN**.  
SCIENTIFIC_OUTCOME: **NOT_ASSESSED**.  
CASE_LIFECYCLE: **OPEN / ACTIVE**.

Q052 is now active; what remains is genuine native execution, not another mathematical proof.

## Point / publication cadence

RUN POINTS: **100 pts**  
TOTAL Q052 POINTS: **100 pts**  
PUBLICATION INTERVAL: **1000 pts**  
NEXT SOME MILESTONE: **1000 pts**  
POINTS TO NEXT PUBLICATION: **900 pts**  
NEW MILESTONES: none  
SOME PACKAGE DUE: no

Breakdown: analysis 40 + search/provenance recovery 30 + validation/routing 30. Copying, formatting and hashing are 0. Q051's 1820-point ledger remains Q051 history and is not transferred into the new Q052 counter. Points do not stop research.

## Memory / repository status

MEMORY_BACKEND: GITHUB  
REPOSITORY_REFERENCE: `Morfindien/Bubbleverse@256536fef86bb6400314e7c80c8596fe1ecdaca7`  
MEMORY_READ_STATUS: VERIFIED/PARTIAL — current head, launcher/registry presence, Q048 capture lineage and no existing Q052 scientific artifact were checked; the recovered Q051 V7 transfer bundle came from Library.  
FILES_DELIVERED: see `FILES_Q052_START_V1.md`.  
MEMORY_WRITE_STATUS: **FILES_READY_FOR_MANUAL_UPLOAD**.  
MEMORY_LINKS_UPDATED: proposed only; no GitHub write performed.  
MEMORY_BLOCKER: Q052 native target/workflow is not yet built, registered or dispatched.

## Gate register

- Q_IDENTITY_GATE: PASS — Q052 selected by Motor14 and explicitly activated by Jim.
- CASE_INTEGRITY_GATE: PASS — Q049–Q051 remain immutable; Q051 is not reopened.
- TARGET_Q_FIREWALL_GATE: PASS — Q052 only.
- JOURNAL_CONTINUITY_GATE: PASS — Q051 close state and Q048/Q050 provenance are linked, not rewritten.
- SOURCE_AND_CITATION_GATE: PASS for the frozen project/source identities used here.
- NO_REPEAT_COMPLETED_WORK_GATE: PASS.
- SPECIFICATION_FREEZE_GATE: PASS for Q052 V1 task contract.
- COMPUTE_BUDGET_GATE: UNRESOLVED — Q052 native runtime not yet measured; first bounded run must record it.
- GITHUB_WORTHWHILE_GATE: PASS — selected on current capability availability, not claimed speed.
- PROGRAM_ID_REGISTRY_GATE: UNRESOLVED — `Q052-NATIVEPAIR-V1` is draft/unregistered.
- LAUNCHER_GATE: UNRESOLVED for Q052 — permanent launcher exists, but no Q052 target is registered.
- ENVIRONMENT_AND_DATA_GATE: UNRESOLVED until Q052 native preflight verifies executable source/binary and frozen inputs.
- MANDATORY_RESULT_TESTS_GATE: NOT_RUN.
- FINAL_RESULT_GATE: UNRESOLVED.
- PUBLICATION_CADENCE_GATE: PASS — 100/1000; no SoMe package due.
- FILE_DELIVERY_AND_MEMORY_GATE: PASS for manual-upload start package; repository integration itself is pending.
- TERMINATION_GATE: PASS for this adoption/preflight stage; next stage is the actual Execution/HPC build/run.

## Exact next action

Feed `Q052_EXECUTION_HPC_TASK_NATIVE_REALIZATION_V1.json` plus `Q052_FROZEN_INPUT_MANIFEST_V1.json` and this journal to **BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0**. The motor should reuse existing native CLASS/capture machinery, build/register the smallest Q052 target, execute exactly one paired native realization if preflight passes, and return the result or first exact blocker to Result Ingestion & Routing 2.3.0.

---

# Q052 V2 — Execution/HPC builder: native pair target generated, not yet dispatched

RUN_ID: `LOCAL-Q052-BUILDER-NATIVEPAIR-20261026-V2`  
UTC: 2026-10-26T11:09:04Z  
Europe/Copenhagen: 2026-10-26T12:09:04+01:00  
ENGINE: `BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0`  
CURRENT_Q = TARGET_Q = **Q052**

## Result of this builder stage

The repository already contains sufficient native machinery to avoid a new
physics implementation. Q045/Q047 provide the exact pinned CLASS binary/source
environment and reconstruction path. Q042 V26 demonstrates executable symbol
interposition around the original `thermodynamics_derivs` and
`thermodynamics_sources`.

A new target, `Q052-NATIVEPAIR-V1`, has therefore been generated around the
original native NDF15 thermodynamics evolution. It adds exactly one scientific
intervention boundary at `z=810`. Each arm independently runs the unchanged
pinned source to that boundary, records the pre-intervention frec state, then
sets only `q=xHeII` to `1e-6` or `0` and keeps that helium residual fixed while
the original hydrogen/temperature source routines continue. The original
frec→reio transition remains at z=50. Reionization uses the accepted fixed
`z_reio=7.4987945556640625`; tau shooting is rejected by runtime gate.

This is an execution wrapper, not a copied H/He rate model.

## Native/P6 status

No existing completed NativeP6 target was found in current repository memory.
Historical Q048 records repeatedly leave NativeP6 / native trajectory identity
unresolved. `Q052-NATIVEPAIR-V1` is the first dedicated Q052 realization target
in this lineage.

## Validation design

Four logical jobs are frozen: L/R at nominal precision and L/R with a validation
refinement (`tol×0.1`, integration-step scale `×0.5`). Within each level the
two pre-intervention z=810 `D_Tmat` and `x_H` values must match bitwise and the
effective background must match. Python collection independently rereads the
CSV bytes and recomputes pair differences.

The refinement discrepancy is deliberately not called a rigorous truncation
bound. If no stronger native error certificate is established, the exact
remaining blocker is:

`RIGOROUS_NATIVE_NUMERICAL_ERROR_CERTIFICATE_NOT_ESTABLISHED_BY_TWO_LEVEL_REFINEMENT_ALONE`.

## Compute/backend

COMPUTE_BACKEND: GITHUB_ACTIONS  
GITHUB_WORTHWHILE: YES  
GITHUB_WORTHWHILE_GATE: PASS for placement.  
ESTIMATE_BASIS: existing Q047/Q045 exact-cache/source/binary lineage; Q052
runtime itself remains unmeasured. Worker timeout 25 min is a safety cap, not a
runtime estimate.

Current chat/container cannot execute the pinned cached `class_ede` binary.
No GitHub workflow dispatch capability is exposed in this session. Therefore:

EXECUTION_STATUS: **FILES_GENERATED / NOT_DISPATCHED**  
RESULT_VALIDATION_STATUS: **NOT_RUN**  
SCIENTIFIC_OUTCOME: **NOT_ASSESSED**  
ACTUAL_COMPUTED_RESULT: **NOT_YET_COMPUTED**

## Point cadence

RUN POINTS: **260 pts**  
PREVIOUS Q052 POINTS: **100 pts**  
TOTAL Q052 POINTS: **360 pts**  
NEXT SOME MILESTONE: **1000 pts**  
POINTS TO NEXT PUBLICATION: **640 pts**  
SOME PACKAGE DUE: **NO**

Breakdown: analysis 70 + repository/source search 45 + implementation 100 +
static validation 45. Formatting/hashing do not add points.

## Files generated

See `FILES_Q052_NATIVEPAIR_V1.md`. All files are individually deliverable.
No archive is used.

## Memory/write state

MEMORY_BACKEND: GITHUB  
REPOSITORY_REFERENCE: `Morfindien/Bubbleverse@256536fef86bb6400314e7c80c8596fe1ecdaca7`  
MEMORY_READ_STATUS: VERIFIED for relevant native lineage.  
MEMORY_WRITE_STATUS: **FILES_READY_FOR_MANUAL_UPLOAD**.  
MEMORY_LINKS_UPDATED: proposed only.  
MEMORY_BLOCKER: target must be installed and registered before launcher use.

## Gates

- Q_IDENTITY_GATE: PASS.
- CASE_INTEGRITY_GATE: PASS.
- TARGET_Q_FIREWALL_GATE: PASS.
- NO_REPEAT_COMPLETED_WORK_GATE: PASS.
- SPECIFICATION_FREEZE_GATE: PASS.
- GITHUB_WORTHWHILE_GATE: PASS.
- PROGRAM_ID_REGISTRY_GATE: UNRESOLVED — add-only patch generated, not installed.
- LAUNCHER_GATE: UNRESOLVED for Q052 until registry/workflow installation.
- ENVIRONMENT_AND_DATA_GATE: UNRESOLVED until the first GitHub cache/source preflight.
- MANDATORY_RESULT_TESTS_GATE: NOT_RUN.
- FINAL_RESULT_GATE: UNRESOLVED.
- PUBLICATION_CADENCE_GATE: PASS — 360/1000.
- FILE_DELIVERY_AND_MEMORY_GATE: PASS for manual-upload builder package.
- TERMINATION_GATE: PASS for this builder stage.

## Exact next action

Install the generated target files, merge the add-only registry entry, keep the
permanent launcher unchanged, and run `Q052-NATIVEPAIR-V1` once. Return the
final artifact and raw branch artifacts to Result Ingestion & Routing 2.3.0.

