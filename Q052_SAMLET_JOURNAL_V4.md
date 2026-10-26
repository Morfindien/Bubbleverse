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



---

# Q052 V3 — first actual native attempt blocked before physics

RUN_ID: `LOCAL-Q052-INGESTION-40330420102-20261026-V3`  
UTC: 2026-10-26T13:37:08Z  
Europe/Copenhagen: 2026-10-26T14:37:08+01:00  
ENGINE: `BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0`  
CURRENT_Q = TARGET_Q = **Q052**  
CASE: `LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1`  
CASE LIFECYCLE: **ACTIVE**  
SCIENTIFIC STATUS: **UNSOLVED / NO_NATIVE_RESULT**

## Exact scientific question (unchanged)

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

## Canonical recovery and immutable history

The current repository tree and run commit are `f7378413f90600d07f31dd29d719d13fe983e9ff`. The supplied complete
V2 journal matches the canonical V2 journal byte-for-byte (SHA256
`d33409c41a2440740fd3b400505466ad1db466cc0d38877c6ea95fced994e3fa`). The complete V1/V2 text above
is retained unchanged; this entry is an append-only successor. Prior Q048/Q050/
Q051 state remains linked through the journal and exact V1 contract, not rewritten
or independently reproved here. No later-Q science was accessed.

## Direct output — observed

GitHub run [40330420102](https://github.com/Morfindien/Bubbleverse/actions/runs/40330420102),
attempt 1, was dispatched at 2026-10-26T13:25:20Z (14:25:20 Copenhagen) and
completed with FAILURE by 13:27:40Z (14:27:40 Copenhagen). This is approximately
140 seconds of overall workflow wall interval, not measured native integration time.

| Job | Observed outcome | Material consequence |
| --- | --- | --- |
| static | SUCCESS | Static gates ran in GitHub; no native validity follows. |
| native L/nominal | Restore FAILURE; compute SKIPPED | No native trajectory. |
| native R/nominal | Restore FAILURE; compute SKIPPED | No native trajectory. |
| native L/refined | Restore FAILURE; compute SKIPPED | No native trajectory. |
| native R/refined | Restore FAILURE; compute SKIPPED | No native trajectory. |
| collect | FAILURE | `ValueError: JOB_COUNT L-nominal 0`. |

The original L/nominal log says:
`Failed to restore cache entry. Exiting as fail-on-cache-miss is set.`
Its exact requested key was
`q042-prod-v1-Linux-py311-cobaya356-q032-4dc873a-pc1222-pybobyqa150-pantheonplus`.
All four arms failed at that same restore step according to job metadata. Full
logs were retrieved for L/nominal and collect; the other three arms were checked
through step metadata. Cache eviction, path/version mismatch, branch scope and
other service causes remain possible; no one cause beyond failed exact restore
has been established.

The supplied final ZIP has SHA256
`952df70e96568b127579dd25da56fdbb959e7606458ce525d0b61c6f0d276c61`, matching
GitHub artifact 12653133514. Its sole member is
`Q052_NATIVEPAIR_CONTRACT_V1.json`, whose SHA256 is
`604616c205d936f676ae94149c260184bc9085f4e0a218b893040a0a7ce353e3`.
`Q052_NATIVEPAIR_RESULT_V1.json`, worker receipts and histories are absent.

## Technical interpretation

The first blocker is **EXACT_NATIVE_ENVIRONMENT_CACHE_RESTORE_FAILED**.
The collector's missing-job error is downstream of this blocker. Inspection of
the pinned controller shows that its exception handler prints error JSON to
stdout but does not write the requested result file. This explains the
contract-only final artifact and is a separate failure-report delivery defect.
No modified code or workflow was installed or executed by this intake.

Current `bubbleverse_program_registry.json` contains no Q052 entry. Deployment
and direct workflow dispatch are verified, while permanent-launcher registration
is not established. Historical V2 not-dispatched status remains true for that
earlier stage and is superseded only in the current working view.

## Scientific interpretation / what did not change

Realized `sup|Delta x_e|` and `sup|Delta tau_T|`: **NOT COMPUTED**.
Native trajectory consistency, containment, reproducibility and error certificate:
**NOT ASSESSED**. Q051's inherited bounds 0.0023814 and <0.0421 are analytic
references, not new observed native differences. This technical failure neither
confirms nor falsifies the physical model or Q051 mathematics. No physical anomaly
is established. Two-level refinement alone would still be insufficient for the
rigorous error-certificate requirement after environment recovery.

EXECUTION: **FAILURE (workflow) / NOT_EXECUTED (native physics)**  
TECHNICAL VALIDITY: **UNRESOLVED for native computation**  
REPRODUCIBILITY / ROBUSTNESS: **NOT_ASSESSED**  
SCIENTIFIC EFFECT: **NO_MATERIAL_CHANGE to the unanswered physical question**  
Q-COMPLETION GATE: **NOT SATISFIED**

## Exactly one next engine / bounded recovery

**BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0**. Identity/version are documented by the prior supplied
builder journal; no new engine deployment is asserted. The full task is in
`Q052_INGESTION_HANDOFF_V3.json`.

Recover and verify the original source/binary environment; investigate cache
identity/scope/path before choosing a recovery mechanism. Do not loosen the
source, binary or input hashes or silently rebuild a substitute core. If exact
bytes cannot be recovered, return that blocker. Version a small failure-report
change so future cache/worker failure persists an actual result JSON, preserving
failure exit status and original error. Resolve add-only launcher registration
when needed. Then execute one existing four-job pair only after unchanged frozen
preflight passes, and return once with actual data or the first exact blocker.

The route adds information because the first real attempt exposed a new
environment/delivery failure. An unchanged rerun is not the next task. No Motor14
closure, new Q, mathematical reproof, refit or expanded configuration campaign is
warranted. Native wrapper/source semantics are not validated by this intake.

## Activity ledger / publication cadence

RUN COST: **120 pts**  
TOTAL WORK POINTS: **480 pts**  
SOME INTERVAL: **1000 pts**  
NEWLY CROSSED SOME MILESTONES: **[]**  
NEXT SOME MILESTONE: **1000 pts**  
POINTS TO NEXT SOME MILESTONE: **520 pts**  
SOME PACKAGE STATUS: **NOT_DUE**  
NEXT SCIENTIFIC ENGINE: **BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0**

Parent total 360; event `Q052-ACTIVITY-INGEST-40330420102-V3` adds 120 exactly once. Breakdown: intake and
archive integrity 25, repository provenance/failure diagnosis 50, claim/state
validation 30, bounded routing 15. This is a rounded heuristic activity index;
resource metrics are not calibrated. Prior build/static work is not recounted.
No separate invented charge is added for skipped native jobs. Packaging and
copying do not recursively add points. Research permission is independent of
publication milestones. No SoMe package or external post was made.

## Evidence, complete-state delivery and GitHub memory

`Q052_EVIDENCE_AND_CLAIMS_V3.json` maps all new claims to exact preserved evidence.
The archive includes all ten supplied raw inputs, original fetched logs, canonical
V2 ledger/journal, pinned controller and run/job/artifact metadata. Earlier
scientific dependency bundles remain pinned references requiring byte verification
at native preflight; they were not all fetched during this technical intake.

No competing global CURRENT_STATE was created. GitHub was read but not mutated;
no commit, PR, registry edit, dispatch or rerun was performed. New V3 files form
an upload-ready append-only memory update; integration instructions and expected
base commit are in `Q052_GITHUB_MEMORY_UPDATE_V3.json`. Full-history continuity,
exact Q, scope, parent ledger, event uniqueness, artifact hashes and ZIP contents
are checked locally before delivery. Files are prepared for the next engine;
preparation does not claim actual engine dispatch.


---

# Q052 V4 — exact original binary recovered; V2 technical repair validated locally

RUN_ID: `LOCAL-Q052-EXACT-OBJECT-RECOVERY-AND-V2-REPAIR-20261026-V4`  
UTC: 2026-10-26T14:09:41Z  
Europe/Copenhagen: 2026-10-26T15:09:41+01:00  
ENGINE: `BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0`  
TASK TYPE: **TECHNICAL_REPAIR + EXECUTION_PREPARATION**  
CURRENT_Q = TARGET_Q = **Q052**  
CASE: `LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1`

## Exact scientific question (unchanged)

Under the pinned hillipop-ede_n3 source/configuration, the same fixed admitted common background and matched validated z=810 start state used by Q051, does the actual native CLASS/P6 low-z implementation produce q=xHeII=10^-6 versus q=0 electron-fraction and Thomson-optical-depth histories that are reproducible, trajectory-consistent with the literal source-real dynamics, and contained within Q051's uniform analytic bounds; and what are the realized sup|Delta x_e| and sup|Delta tau_T| with a validated numerical error certificate?

## New observed evidence and actual recovery

Current inspected repository base is `31d810c0a8e8a550ae18b7114eb98476e29635a6`.
The supplied V3 journal matches canonical repository V3 bytes. Full prior V1/V2/V3
text is retained unchanged above. Canonical V3 ledger was still absent from GitHub;
the delivered V3 ledger and uploaded handoff jointly establish the 480-point parent.

Q045 raw hillipop artifact 11659110603 (run 38023210800) was downloaded and its
archive digest verified. Its ten members contain tables and receipts, no binary;
it is reference-only for restoration. Q047 preflight run **38113104261**, raw artifact
**11691844278**, preserves the actual original binary. Its ZIP SHA256 is
`fa3602e64ddc644eeb59fb8fb6e0dc271ed1dc6b8ee79d4e8fb3804eb1a55b49`.
Member `q047_capture/original_objects/classy.so` was recovered and checked:
**SHA256 df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf**,
exactly the frozen Q052 binary. Four frozen source/header hashes were also checked
against the preserved original sources. No CLASS core was rebuilt or executed.
The binary is delivered individually as `Q052_ORIGINAL_CLASSY_PINNED.so`; after
installation the native target no longer depends on the old cache or expiring artifact.

The required `Q048_V151_ACCEPTED_CHECKPOINT_V1.json` was absent from the current
repository. It was recovered from the identified persistent file and verified at
SHA256 `60dcd23a315a28be2ef84c4c5353c783e88eb73c4199d43b7f5640a16db2eb96`.
It must be included when installing the target; no arbitrary start state was chosen.

## Diagnosed defects and separately versioned correction

1. V1 imports nonexistent `q047_acquire_v1`. Existing verified helper is
   `q047_execution_v1.identify_binary`; V2 reuses that helper.
2. V1's error handler printed failure JSON without writing the output file.
   An empty-worker regression reproduced the failure against V1; it passes against
   V2, preserving the original error and a nonzero exit. Branch/stage/run/attempt
   metadata and original error-log text/hash survive setup failures.
3. The generated V1 registry patch used `q=Q052`, while the unchanged permanent
   launcher requires `Q-[0-9]{3,}`. V2 uses explicit mapping `q=Q-052`,
   `scientific_q=Q052`; a test executes the actual launcher resolver against it.
4. V1 assumed a cache-only environment. The new V2 restores the exact preserved
   binary, checks out source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`,
   and retains exact binary/source/lineage gates. It does not broaden a cache key,
   substitute a rebuilt binary, or alter V1 history.

New target **Q052-NATIVEPAIR-V2** is locally allocated and unregistered.
The scientific C wrapper changes only its program version label; parameter mapping,
worker validation and collector scientific logic are preserved. Python 3.11.16 is
now an explicit pre-native gate. A guarded installer adds only the V2 registry entry
and a README prefix, with expected base hashes; the launcher remains unchanged.
Both workflows and the exact file manifest are delivered for manual integration.

## Actual finite validation

**13 tests PASS, zero skipped**: inherited Q052 contract/difference/grid tests;
empty-directory failure persistence; branch/log preservation; exact binary copying;
corrupt binary/archive rejection; frozen lineage hashes; actual launcher resolver;
add-only/idempotent installer and changed-base refusal. Installer tests mutate
synthetic temporary active-state fixtures only. No tests use fabricated native histories.

C syntax/type compilation against recovered original headers exits 0. Scientific
source preservation was checked by C-label normalization and function AST equality.
Full native linking/execution remains **NOT_RUN**: this local runtime has Python
**3.12.14**, whereas the native contract requires **3.11.16**.
No claim of complete environment reproduction is made from binary/hash recovery alone.

## Backend, runtime and next action

Restoration and repair tests ran locally. Native placement remains **GITHUB_ACTIONS**
because the required Python/source checkout and existing runner architecture are
available through the prepared workflow, while the current local runtime does not
satisfy the native freeze. No selectable workflow-dispatch tool is exposed here;
no new run was dispatched. Native run duration, quota and monetary cost remain
unmeasured. Existing caps are retained: 10 min static, 10 min recovery, 25 min per
native job, 10 min collection. The nominal dependency-path cap is 55 min excluding
queue delays; summed job timeout allocations are 130 runner-minutes, not measured
usage or an expected bill. No new paid resource commitment is made in this session.

Upload the individual manifest-listed files, place the two workflows under
`.github/workflows/`, and run **Install Q052 native pair V2** once. It verifies the
package and guards registry/README bases. Only after successful installation use
**BUBBLEVERSE START → Q052-NATIVEPAIR-V2** once. Return the final result JSON,
upstream job-state JSON and raw branch artifacts to Result Ingestion & Routing 2.3.0.
An unchanged V1 rerun is not warranted.

START_STATUS: **NOT_READY until repository installation succeeds**  
EXECUTION_STATUS: **FILES_GENERATED / LOCAL_REPAIR_TESTS_COMPLETE / NATIVE_NOT_RUN**  
RESULT_VALIDATION_STATUS: **VALIDATED for repair behavior; NOT_RUN for native science**  
SCIENTIFIC_OUTCOME: **NOT_ASSESSED**  
ACTUAL_COMPUTED_RESULT: **NOT_YET_COMPUTED**  
CASE LIFECYCLE: **ACTIVE / OPEN**  
FINAL_RESULT_GATE: **UNRESOLVED**

Q051 bounds remain inherited analytic references. No realized continuous supremum,
trajectory identity, physical confirmation/falsification or rigorous numerical error
certificate is established. Two-level refinement still does not itself supply that
certificate. A successful next run remains subject to the original scientific gates.

## Activity and publication cadence

RUN POINTS: **320 pts**  
TOTAL WORK POINTS: **800 pts**  
PUBLICATION INTERVAL: **1000 pts**  
NEXT SOME MILESTONE: **1000 pts**  
POINTS TO NEXT MILESTONE: **200 pts**  
SOME PACKAGES DUE: **NONE**  
SOME PACKAGES DELIVERED: **NONE**

Event `Q052-ACTIVITY-EXACT-OBJECT-RECOVERY-V4` is appended once to the delivered V3 ledger. Breakdown: provenance/
recovery 90, implementation 140, validation 70, state/routing 20. This is a rounded
heuristic estimate, not measured compute, cost or confidence. Old runs and native
computations are not recounted; packaging does not add recursive points.

## Gates and memory

Identity/scope/history/scientific-freeze: PASS. Local repair tests and relevant
header compile: PASS. Program registration, actual launcher dispatch, exact native
runtime/source checkout, pair completeness and scientific error certificate:
UNRESOLVED until their actual checks run. FILE_DELIVERY_AND_MEMORY is a manual-upload
package, not a GitHub write. TERMINATION_GATE: PASS for this bounded recovery/repair
stage; the next necessary evidence requires installing/executing the prepared target.

MEMORY_BACKEND: GITHUB  
MEMORY_READ_STATUS: VERIFIED for relevant current state and original objects  
MEMORY_WRITE_STATUS: **FILES_READY_FOR_MANUAL_UPLOAD**  
MEMORY_LINKS_UPDATED: proposed V4 journal/ledger/handoff and V2 registry/README prefix  
REPOSITORY MUTATION / WORKFLOW DISPATCH BY THIS RUN: **NONE**

`Q052_REPAIR_PROVENANCE_V4.json`, `Q052_BUILDER_HANDOFF_V4.json`, exact test log,
original-object receipt and install manifest preserve the technical record. V1 files,
old failed run 40330420102, earlier journals and the permanent launcher are unchanged.
