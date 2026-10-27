# Q052 — Execution/HPC Builder V10

RUN_ID: `LOCAL-Q052-EXECUTION-BUILDER-VALIDATEDDIAG-V3-20261026-V10`  
RUN TIME UTC: `2026-10-26T17:02:16Z`  
RUN TIME EUROPE/COPENHAGEN: `2026-10-26T18:02:16+01:00`  
ENGINE: `BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0`  
CURRENT_Q = TARGET_Q = **Q052**  
CASE: `LOCAL-Q052-NATIVE-REALIZATION-CERTIFICATION-V1`

## A. Task and state

Task type: **SCIENTIFIC_CASE_EXECUTION / EXECUTION-TARGET BUILD**, not result ingestion and not a new Q.

Exact Q052 remains unchanged: under the pinned `hillipop-ede_n3` source/configuration, fixed admitted common background and matched validated z=810 start state, determine the actual native q=1e-6 versus q=0 electron-fraction and Thomson-optical-depth differences with a validated numerical error certificate.

The complete V9 journal is preserved as the prefix of `Q052_SAMLET_JOURNAL_V10.md`. V8 already certifies only the exact saved-data interpolants; Q052 remains **INCONCLUSIVE_SOURCE_REAL_CERTIFICATION_UNRESOLVED**. No historical result is rewritten.

RUN POINTS: **300 pts**. TOTAL WORK POINTS: **1695 pts**. PUBLICATION INTERVAL: **1000 pts**. NEXT SOME MILESTONE: **2000 pts**. POINTS TO NEXT MILESTONE: **305 pts**. No new milestone was crossed; `Q052-SOME-M001` remains the delivered milestone. Canonical cadence ledger: `Q052_QUESTION_ACTIVITY_LEDGER_V10.json`.

Assessment basis: 70 source/provenance/ABI feasibility + 70 design/analysis + 100 implementation + 45 static validation + 15 state/routing/memory. This is a rounded heuristic activity index, not measured compute or confidence. No prior native work, V8 mathematics, Q051 work, formatting, copying or hashing is recounted.

## B. Runtime and capabilities

Verified in this run: local Python/file validation; current GitHub repository inspection; exact source inspection at `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`; existing Bubbleverse launcher/registry/workflow/source reuse inspection.

The current local container does **not** contain the exact executable pinned CLASS environment/original binary needed to truthfully compile and run the native wrapper. The repository already has that environment recovery path. No model switch or external paid compute was used.

Recommended execution profile: existing GitHub Actions native environment **after guarded installation**, because it already recovers the original binary, pins Python 3.11.16 and checks out the exact source commit. Fallback is a separately reconstructed exact native environment, but its setup cost and compatibility are unmeasured and offer no demonstrated benefit.

## C. Execution decision

Selected mechanism: **new technical program `Q052-VALIDATEDDIAG-V3`**, derived fail-closed from the immutable `Q052-NATIVEPAIR-V2` wrapper. It is not a new physics implementation.

Why V2 alone is insufficient: V2 produced the paired histories but did not save the internal state/guard/background evidence required for the V8 whole-cell source-real certificate. Re-running V2 unchanged would produce no material new evidence.

Why the new mechanism is minimal: it reuses the exact V2 orchestration and original shared object, adding only diagnostic exports/interposition. It permits exactly **one new nominal L/R pair**. No refined pair is allowed because refinement already exists historically and is not the missing certificate mechanism.

## D. Prior work and sources

Reused without recounting or recomputing:

- completed `Q052-NATIVEPAIR-V2` result and its nominal/refined histories;
- V8 serialized-interpolant certificate and validated-numerics contract;
- Q048/Q050/Q051 frozen lineage and z=810 start semantics through the existing V2 gates;
- original binary SHA256 `df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf`;
- source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`;
- historical Q042/Q047 diagnostic patterns for thermodynamic workspace and HyRec dispatch inspection.

The V8 saved-interpolant result is not strengthened here. Its nominal exact interpolant bounds remain approximately `1.1072046742e-6` for sup |Delta x_e| and `2.42039290999e-5` for sup |Delta tau| on the saved domain ending near z=809.6825. Those are representation results, not a new source-real certificate.

## E. Repository findings

Repository inspected: `Morfindien/Bubbleverse@1f420951ecad7109fa59476d824bbcb2b8240680`.

That commit is one commit ahead of the V9 report's earlier read base and contains the six supplied V9 root files. Relevant inspected material includes:

- `q052_native_pair_v2.c` — current git blob `0539a22cb503af2030c4ca6cdbc7f0c41ba6e1f7`;
- `q052_native_pair_v2.py`;
- `.github/workflows/q052-native-pair-v2.yml`;
- `bubbleverse_program_registry.json` with active historical `Q052-NATIVEPAIR-V2`;
- `.github/workflows/00-bubbleverse-start.yml` permanent launcher;
- `q047_collect_state_v2.c`, `q042_context_native_v29.c`, `q042_event_native_v28.c` as reuse evidence.

Pinned source inspection confirms that the native ABI exposes the complete active thermodynamic vector, workspace phase/flags, `x_H/x_He/x_noreio/x_reio/Tmat`, background workspace pointer/vector and dynamic component indices. Pinned HyRec source exposes the relevant model/threshold semantics; the new diagnostic records actual dispatch inputs rather than inferring historical callbacks.

README currently contains stale historical Q052 V2 navigation saying the native result is not yet computed. This builder does not rewrite it in chat or silently in GitHub. The guarded installer prepends a new current V3 section only if the expected README/registry/launcher base blobs still match.

MEMORY_BACKEND: **GITHUB**. MEMORY_READ_STATUS: **VERIFIED**. MEMORY_WRITE_STATUS: **FILES_READY_FOR_MANUAL_UPLOAD**. No repository write is claimed.

## F. Numerical and compute plan

Frozen science remains: `hillipop-ede_n3`; z=810 intervention; L q=1e-6, R q=0; fixed `z_reio=0x1.dfec4p+2`; no tau shooting; no core rebuild; literal selector/equality semantics unchanged.

New capture records:

- full active `y` and supplied `dy` at original output callbacks;
- post-intervention RHS callback state/derivative records, explicitly **not** labelled accepted NDF15 steps;
- vector indices, phase and require flags;
- `x_H`, `x_He`, `x_noreio`, `x_reio`, `Tmat`, `Tmat/Trad`;
- normal background workspace snapshots and index mapping;
- exact z=810 pre/post intervention state and phase boundaries;
- observed HyRec `rec_dxHIIdlna` model/input tuple and observed HMLA/TLA/SWIFT child calls.

The diagnostic does **not** invent Pion or a guard margin. Those values must later be reconstructed and interval-enclosed from the pinned source. It also does not pretend sampled background values are an admitted-family interval tube.

COMPUTE_BACKEND: **GITHUB_ACTIONS_AFTER_INSTALL_ONLY**. GITHUB_WORTHWHILE: **YES**. GITHUB_WORTHWHILE_GATE: **PASS**, because the exact original binary recovery/native environment already exists there; this decision is about reproducibility and compatibility, not speed.

Job structure: static -> recover -> two parallel native jobs `[L,R]` in nominal mode -> collect. Native branch cap = **2**. No automatic retry. Prior native processes were about 0.816 s each, but diagnostic I/O overhead is unmeasured, so that number is not used as a runtime prediction. Workflow safety caps are static 10 min, recovery 10 min, each native job 25 min and collection 10 min; with the two native branches parallel, the configured dependency-path cap is 55 min. This is a hard safety envelope, not an expected duration.

The first remaining certificate capability after successful capture is:

`LOCAL-Q052-VALIDATED-WHOLE-CELL-RESIDUAL-BACKGROUND-ARITHMETIC-ENGINE-MISSING-V10`

It covers the still-unimplemented validated whole-cell reconstruction/residual, admitted-background tube, literal guard interval signs/slabs, source/table/libm/rounding enclosures, tube/event propagation and observable/tau transfer. Therefore capture success remains **PARTIAL**.

## G. Actual deliverables

Execution package:

- `q052_build_validated_diag_v3.py` — exact-parent-gated source-to-source diagnostic generator;
- `q052_validated_diag_v3.py` — worker, trace validator, collector and failure serializer;
- `test_q052_validated_diag_v3.py` — finite fail-closed tests;
- `Q052_VALIDATED_DIAGNOSTICS_CONTRACT_V10.json` — frozen new target contract;
- `Q052_ABI_CAPTURE_FEASIBILITY_V10.json` — ABI/capture feasibility map;
- `.github/workflows/q052-validated-diagnostics-v3.yml` — two-branch execution workflow;
- `q052_program_registry_patch_validateddiag_v3.json` — new registry entry only;
- `README_Q052_VALIDATEDDIAG_V3_SECTION.md` — current README prefix;
- `q052_install_validated_diag_v3.py` and `.github/workflows/q052-install-validated-diag-v3.yml` — guarded registration/install path;
- `Q052_INSTALL_MANIFEST_VALIDATEDDIAG_V3.json` — package/base identity locks.

Memory/report package:

- `Q052_STATIC_VALIDATION_V10.json` and `Q052_LOCAL_STATIC_TEST_LOG_V10.txt`;
- `Q052_QUESTION_ACTIVITY_LEDGER_V10.json`;
- `Q052_SAMLET_JOURNAL_V10.md`;
- `Q052_EXECUTION_HANDOFF_V10.json`;
- `Q052_BUILDER_REPORT_V10.md`;
- `Q052_OUTPUT_MANIFEST_V10.json`, `FILES_Q052_BUILDER_V10.md`, `SHA256SUMS_Q052_BUILDER_V10.txt`.

Generated files are not integrated merely because they exist here. The historical V2 source is never replaced; V3 C is generated only inside the exact installed environment after the parent identity and patch anchors pass.

## H. Actual execution and validation

Performed now:

- current repository and source/ABI inspection: **PASS**;
- Python syntax checks for builder/controller/installer/tests: **PASS**;
- JSON parsing: **PASS**;
- workflow YAML parsing: **PASS**;
- local unit tests: **6/6 PASS**;
- synthetic full six-anchor patch application: **PASS**;
- one-pair/no-refinement lock: **PASS**;
- forced-PARTIAL/no-accidental-final-PASS gate: **PASS**.

Not performed now:

- patch application against the uploaded repository copy: deferred to the workflow static gate;
- generated C compile against the original binary: **NOT_RUN**;
- native L/R execution: **NOT_RUN**;
- whole-cell validated source-real certificate: **NOT_RUN**.

ACTUAL_NEW_SCIENTIFIC_RESULT: **NONE**. This run builds and statically validates the next evidence-producing mechanism. It does not change the existing numerical values or Q052 scientific status.

## I. Journal and return

`Q052_SAMLET_JOURNAL_V10.md` is an append-only successor. `Q052_QUESTION_ACTIVITY_LEDGER_V10.json` adds the 300-point event exactly once and carries Q052 to 1695 points. No SoMe package is due at this total.

Termination decision for this builder run: **STOP WITH RUNNABLE PACKAGE PREPARED, NOT DISPATCHED**. The V9 request for actual ABI/capture feasibility has been answered positively, and the versioned diagnostic mechanism has been built. The next action is installation followed by exactly one target run. After that run, return once to `BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0` whether capture succeeds or fails.

Q052 remains open. No Motor-14 closure and no new Q.

## J. Start this — readiness state

**START_STATUS: NOT_READY**

Exact blocker: `Q052-VALIDATEDDIAG-V3` is **not yet integrated into the canonical GitHub registry/README**, so the permanent launcher cannot truthfully be used yet. Upload the individual V10 execution-package files to their declared repository paths and run **Install Q052 validated diagnostics V3** once. The installer fails closed if the expected registry, README, launcher or package identities changed.

Only after that guarded installation succeeds does the intended start become:

`OPEN: 🚀 BUBBLEVERSE START`  
`PASTE: Q052-VALIDATEDDIAG-V3`  
`PRESS: Run workflow`  
`START THIS: Q052-VALIDATEDDIAG-V3`

Do not launch it from the current unintegrated package state.
