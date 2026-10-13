# Bubbleverse — Q048 phase-energy first-turn guard V8

Current runnable target: **Q048-PHASETURN-V8**. The inspected remote registry still predates V7, so installation is deliberately two-stage and fail-closed: upload the individual V8 package files, run **🔧 INSTALL Q048 PHASE-TURN V8** once (`.github/workflows/q048-install-phase-turn-v8.yml`), then use the permanent **🚀 BUBBLEVERSE START** normally. The installer may change only `bubbleverse_program_registry.json` and `README.md`; it refuses unrelated mutable-base changes. After installation, paste `Q048-PHASETURN-V8` into **🚀 BUBBLEVERSE START** and press **Run workflow**. The permanent launcher remains `.github/workflows/00-bubbleverse-start.yml` and is not modified.

Q-048 remains **PROPOSED_UNVERIFIED**, CASE **NOT_ASSIGNED**, while Q047 remains **CLOSED INCONCLUSIVE**. V8 has the bounded scope `CONDITIONAL_SOURCE_REAL_PHASE_ENERGY_TURN_GUARD_THERMAL`. `FINAL_RESULT_GATE=UNRESOLVED` by construction: V8 does not qualify native floating-point/source-instance identity, does not locate the shared helium `q=xHeII=1e-6` cutoff, and does not compute complete latch/reset `x_e(z)` or `tau_T(z)` histories.

V8 is a materially new executable successor to V7, not a larger V7 replay. Official V7 run `38348832247` remains frozen parent evidence. V7 established a valid Camspec prefix but stopped with `TRAJECTORY_TUBE_NOT_CLOSED` after 1693 accepted Cartesian `(phi,X)` cells; it did not establish source-guard failure. Mathematics-008 diagnosed oscillatory interval wrapping and derived a phase-energy first-turn certificate.

The V8 implementation re-verifies accepted V7 Camspec cell 1509 against the frozen source and exact official V7 artifact, then uses the globally smooth source-equivalent coordinates `theta=lambda*phi` and signed `y=-X`. Before the first scalar turn `y>0`; the turn is the unique certified `y=0` crossing; after it `y<0`. Every V8 phase cell must retain a positive exact source-guard margin. The event bracket is accepted only while `dy/du<0` throughout, proving unique crossing direction. At the turn the kinetic term vanishes, so `e_turn=U(theta_turn)`.

The post-anchor gate is the Mathematics-008 inequality `e_turn_upper < 3*B_transfer_lower + V_floor_lower`, using the exact V6 transfer-base lower endpoint. If it passes, monotone scalar energy proves the source guard for every later scale factor through `z=2870`, eliminating any need to propagate further oscillatory scalar tubes. Camspec thermal evolution is then recomputed from `z=4600` through He1f and He2 using the established sign-aware positive-w method: the V6 initial energy cap is used before the completed turn bracket and the tighter turn-energy cap afterward.

The parent V7 artifact is downloaded by exact workflow run ID `38348832247` and verified by raw SHA256 before use. No new native CLASS capture, fit, likelihood, sampler, GPU or HPC campaign is authorized. A failure to certify the new sufficient bound returns a precise `UNRESOLVED_BOUNDED_OBSTRUCTION`; it is not a physical EDE falsification unless an admitted source-real guard margin itself is rigorously shown nonpositive.

Workflow target: `.github/workflows/q048-phase-turn-v8.yml`. Expected outputs are `camspec-ede_n3_phase_turn_v8.json` and collector `q048_phase_turn_final_v8.json`. Return the bounded result once to **RESULT INGESTION & ROUTING ENGINE**. Do not automatically start H/frec/shared-cutoff/full-history execution.

Prepared from Mathematics result `I-PROPOSED-Q048-MATHEMATICS-008`, official V7 run `38348832247`, frozen source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`, and inspected Bubbleverse repository HEAD `c9ca98f232a0c753ce9a8c04437fc5d7ef699dab` on 2026-10-13.

---

## Preserved historical repository context

# Bubbleverse — Q048 direct guard + He1f/He2 continuation V7

Current runnable target: **Q048-GUARDCONT-V7**. After installing the individual V7 files and applying the supplied differential repository patch, open **🚀 BUBBLEVERSE START**, paste `Q048-GUARDCONT-V7`, and press **Run workflow**. Canonical launcher remains `.github/workflows/00-bubbleverse-start.yml`; it is not modified.

Q-048 remains **PROPOSED_UNVERIFIED**, CASE **NOT_ASSIGNED**, and Q047 remains **CLOSED INCONCLUSIVE**. Scope is `CONDITIONAL_SOURCE_REAL_GUARD_THERMAL_CONTINUATION`. `FINAL_RESULT_GATE=UNRESOLVED` by construction: V7 does not qualify native floating-point/source-instance identity, does not locate the shared `q=xHeII=1e-6` cutoff, and does not compute complete latch/reset `x_e(z)` or `tau_T(z)` histories.

V7 reuses the frozen V6/V5/Q047 rational proof backend and source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`. It adds exactly one bounded scientific computation: a source-root trajectory-correlated validated `(phi,X)` tube for **Camspec EDE n=3** with the source guard checked on every certified whole-state cell, followed by sign-correct positive-`w` propagation through He1f `4600→3550` and He2 `3550→2870` for both EDE configurations. At `z=2870` it reports the conditional source-real H-entry helium state `q`. Hillipop keeps the already-valid V6 full-transfer source-root guard.

The Camspec guard proof uses the exact equivalent margin `3 B(a)+X^2/2+V_floor-V_e > 0`; a loose interval on the displayed ratio alone is diagnostic and is not allowed to override a proved positive equivalent margin. Thermal propagation uses Mathematics-007's sign rule: for positive lower `L`, the lower homogeneous factor is `L exp(-d_max)`. A separate rational Bernoulli comparison supplies an independent control without exponential evaluation.

The computation is finite. Camspec uses fixed relative `a` step `1/64`, at most 5000 accepted cells, at most 14 halvings per attempted cell, and a 5400-second scientific work budget. A failure to close a tube or separate the direct guard returns a preserved `UNRESOLVED_BOUNDED_OBSTRUCTION`; it is not a source crossing or physical falsification. Hillipop thermal continuation uses fixed relative step `1/32`. No fit, likelihood, sampler, GPU, native CLASS capture, or HPC campaign is authorized.

Workflow target: `.github/workflows/q048-guard-continuation-v7.yml`. Expected worker artifacts contain `camspec-ede_n3_guard_v7.json`, `hillipop-ede_n3_guard_v7.json`, their checkpoints/progress where applicable, and collector `q048_guard_final_v7.json`. Return the bounded result once to **RESULT INGESTION & ROUTING ENGINE**. Do not automatically start H/frec/cutoff/full-history execution from this workflow.

Prepared from Mathematics result `I-PROPOSED-Q048-MATHEMATICS-007` and repository HEAD `2bc190aeb1a2659fbc9bc0d402159c7768c6b15a` at 2026-10-12T21:58:34+02:00. V6 remains preserved as historical provenance and is marked superseded only after the differential registry patch is applied.

---

## Preserved historical repository context

# Bubbleverse — Q048 source-root energy and He1 extension V6

Install the individual files below, then open **🚀 BUBBLEVERSE START**, enter
**Q048-STRUCTURAL-V6** and press **Run workflow**. Canonical launcher:
`.github/workflows/00-bubbleverse-start.yml`; registry `bubbleverse_program_registry.json`.
The exact-lookup launcher is unchanged. Unknown IDs and shell input fail closed.

Q-048 is PROPOSED_UNVERIFIED; CASE NOT_ASSIGNED; Q047 CLOSED INCONCLUSIVE.
Scope CONDITIONAL_SOURCE_REAL_STRUCTURAL_EXTENSION. FINAL_RESULT_GATE=UNRESOLVED:
native/actual-source admission, common first cutoff and full xe/tau bounds remain NOT_COMPUTED.

## Install

At repository root:
- `q048_structural_v6.py`, `q048_structural_runner_v6.py`, `q048_structural_tests_v6.py`
- `q048_structural_config_v6.json`, `q048_structural_parent_v6.json`
- `q048_structural_package_check_v6.py`, `q048_structural_package_v6.json`
- `Q048_V5_STRUCTURAL_MATHEMATICS.json`, `Q048_V5_INDEPENDENT_REVIEW.json`, `Q048_V5_SYMBOLIC_CONTROL.json`
- `bubbleverse_program_registry.json`, `README.md`, `Q047_SAMLET_JOURNAL.md`

Workflow target: `.github/workflows/q048-structural-v6.yml`.
Place `q048-structural-v6.yml` at that exact path.
Retain every installed V5/V4/frozen backend dependency and the canonical launcher.
Prepared against commit05ec5263fc4be2cee29892839d0f818ccba64c91; reconcile later
repository changes before replacing registry/README snapshots. Local preparation
has not installed files or dispatched a GitHub run.

## Structural method and scientific boundaries

The immutable official V5 parent is run38259814813, raw hash
bf63e8698a2c0a3b6f518f691443ceec151398a21693aea523743dac5d76bfa5.
All inherited certificates are reverified. Original records/cells/intervals stay
unchanged, embedded in each new report. A separate structural extension derives
E=X^2/2+V and dE/dln(a)=-3X^2 from the exact frozen source initial state, and
proves a He1 invariant-domain/variable-coefficient enclosure from each untouched
thermal endpoint to the next fixed phase boundary z4600. It uses an independent
source-root energy background envelope beyond old cell coverage. No old background
cell is extrapolated. No later He1f transition, helium cutoff, native solver or
full history is qualified. Caps/methods/intervals are recomputed, not accepted
from saved PASS fields. Independent rational exponential bounds verify endpoints.

Hillipop's background guard is bounded through z2870. Camspec's current conservative
guard only reaches approximatelyz3562.59; its full-transfer guard is not established.
The bound threshold is not an actual event. Original source/effective inputs,
accepted z_reio, initial errors and all older certificates remain fixed.

## Jobs, checkpoints and result tests

One finite launch: preflight, four independent workers, collector; max-parallel4.
No automatic chaining or repeat-from-a-new-tiny-cell strategy. Each worker has
900s preverification and900s postverification budgets, a35-minute process limit
and40-minute job timeout. Collector has20-minute process/25-minute job limits.
These are below GitHub's official6-hour hosted-job limit checked2026-10-12:
https://docs.github.com/en/actions/reference/limits . Setup/transfer reserve is explicit.
Atomic provisional/final `*_checkpoint_v6.json` preserve parent and new proof;
they are completion evidence for this one-pass target, not an indefinite resume chain.
Retry a failed independent worker only for a concrete technical recovery reason.

Finite mandatory tests: exact pins/Q/root/run, energy positivity and source guard,
original initial-state retention, phase boundary, invariant barriers, independent
endpoint control, forged cap/method/endpoint rejection, preserved parent records,
missing/duplicate/foreign-run collection rejection, launcher/registry/README and
full unchanged journal tail. Collector recomputes inherited and extension proofs.
Execution COMPLETE and conditional test PASS never upgrade the scientific gate.

Outputs: `q048_structural_results/*_structural_v6.json` and `*_checkpoint_v6.json`;
collector `q048_structural_final_v6.json` retains all four raw records and a job manifest.
Full authoritative journal: `Q047_SAMLET_JOURNAL.md`, preserving sources/claims/failures.
Return actual outputs and full journal to RESULT INGESTION & ROUTING ENGINE.
V5 remains the frozen historical implementation; its launch preference is superseded.

---

## Preserved historical repository context

The following incoming README is unchanged historical context. Active Q048 execution
instructions are V6 above; old version launch examples are historical.

# Bubbleverse — Q048 controlled prefix continuation V5

After installing the individual files, open **🚀 BUBBLEVERSE START**, enter
**`Q048-RESUME-V5`**, and press **Run workflow**. Canonical launcher:
**`.github/workflows/00-bubbleverse-start.yml`**; exact registry:
**`bubbleverse_program_registry.json`**. The launcher is unchanged and performs
an exact approved lookup; PROGRAM_ID is never shell code.

Q **Q-048 — PROPOSED_UNVERIFIED**; CASE **NOT_ASSIGNED**; Q047 remains **CLOSED
INCONCLUSIVE**. Scope **CONDITIONAL_SOURCE_REAL_PREFIX**. Scientific
**FINAL_RESULT_GATE=UNRESOLVED**: actual-source equivalence, common first cutoff,
complete latch/reset electron-history and optical-depth bounds are NOT_COMPUTED.

## Install individual files

Put at repository root:
- `q048_resume_v5.py`, `q048_comparison_v5.py`, `q048_resume_config_v5.json`
- `q048_resume_controls_v5.py`, `q048_resume_control_fixture_v5.json`, `q048_resume_tests_v5.py`
- `q048_resume_merge_v5.py`, `q048_resume_package_check_v5.py`, `q048_resume_package_v5.json`
- `q048_resume_parent_v5.json`, `bubbleverse_program_registry.json`, `README.md`, `Q047_SAMLET_JOURNAL.md`

Put `q048-resume-v5.yml` at **`.github/workflows/q048-resume-v5.yml`**.
Retain the current canonical launcher and all pinned V4/older dependency files.
Preparation base **ab301e052743773b6734959f80fbd6540afee230**; reconcile later
repository changes before installing the registry/README snapshots. Remote
installation and dispatch are not performed by local preparation.

## Minimum numerical change and exact continuity

Pinned first parent: actual GitHub **run38249121532**, complete raw
`q048_resume_parent_v5.json`, SHA256
`7f1f805d39840592622df23f781b594548a4e355e80b656006a87c6eed013c08`.
Camspec EDE starts427 background/319 thermal cells, Hillipop342/234; each LCDM
retains35 thermal cells. No frozen source, effective input, accepted z_reio,
initial radius, physical equation, old certificate or likelihood is changed.

New background trials permit **k=0..12** instead of0..11, retaining the existing
recomputed weighted certificate and strict H/latch/tube guards. New He1 cells
in the approved outer tube use the explicit method
`he1_outer_lower_finite_time_v1`. On normalized xi in[0,1], with recomputed
lambda=-L>0 and full r0/defect delta, the independent rational radius is
`U=r0+max(0,delta/lambda-r0)*min(1,lambda)`. Require strict closure, constant
predictor, correct phase/coverage and positive temperature/beta. The ordinary
primary signed scalar proof must close as well. Old stationary V4 markers keep
old stationary admission semantics; unknown/domain-incompatible markers fail.
These controls certify prospective local cells only; later cells need fresh proofs.

Frozen dependencies include `q047_math_v1.py`, `q047_certificate_v1.py`,
`q047_precursor_check_v1.py`, `q048_prefix_v1.py`, `q048_prefix_config_v1.json`,
`q048_resume_v3.py`, `q048_resume_controls_v3.py`, `q048_resume_v4.py`,
`q048_comparison_v4.py`, `q048_resume_config_v4.json`, `q048_resume_parent_v4.json`.
All are already installed at the preparation base and checked byte for byte.
No compile, native CLASS run, re-shoot/refit, sampler or likelihood evaluation.

## Checkpoint, job and validation design

Four independent case workers, maximum parallelism4, serialized campaign runs.
Each has900s predecessor verification,180s background,180s thermal and900s
successor verification;40-minute process safeguard and50-minute job timeout.
Preflight/collector have25-minute timeouts. Collector recomputes all four cases
in separate processes and refuses missing, duplicate or incompatible reports.
These safe stages stay below GitHub's currently documented6-hour hosted job
limit (verified2026-10-12): https://docs.github.com/en/actions/reference/limits .
No automatic endless workflow chain or hypothesis-rescue retry is introduced.

Before continuation every inherited cell is recomputed; after continuation the
complete successor is recomputed, and collection repeats full admission.
Atomic checkpoints preserve exact cursor/error/root/config/run lineage after
verification, every8 new cells and at stage boundaries. Historical V3/V4 roots
survive; the immediate V4 parent hash is exact. Later V5 runs search the last20
completed runs for retained case checkpoints. Found expired/duplicate/wrong-run
artifacts fail closed. If prior V5 runs exist but no retained case artifact is found in that bounded
window, discovery fails closed. Only no previous V5 runs permits the pinned V4
asset. Use CLI `--checkpoint` for an older authenticated retained checkpoint.
The rooted parent-lineage list and its tail are bound in metadata and the proof
payload. Historical hash pointers provide consistency, not an independent
authentication of every past file; authenticated artifact retrieval supplies
the input provenance.

Mandatory finite tests: selected k12 and k7 controls with independent matrix
Taylor/algebraic comparison; historical stationary failure; normalized-domain
and method/weight/proof tamper rejection; frozen config/root/run identity;
source guards; exact inherited prefix preservation; unsupported full-product
claims rejected; incomplete/duplicate/config-incompatible merge rejected;
launcher resolver, registry history, README paths and journal-tail preservation.
Successful process execution is not physical confirmation.

## Outputs and journal

Per-case `*_checkpoint_v5.json`, `*_resume_v5.json` under `q048_resume_results/`;
preflight `q048_resume_controls_v5.json`; collection `q048_resume_final_v5.json`
with all raw certificates, job manifest, tests and missing scientific products.
Local preparation results and detailed status are documented in
`Q048_EXECUTION_REPORT_V5.md` and `q048_resume_local_validation_v5.json`.

Full authoritative memory remains **`Q047_SAMLET_JOURNAL.md`**, preserving stable
sources, claims, failures and complete prior journal. Return raw results plus
journal/provenance to the **RESULT INGESTION & ROUTING ENGINE**.
The registry adds V5, supersedes V4, and preserves every unrelated entry. V4 is
retained as the frozen historical source/method implementation.

---

## Preserved historical repository context

The following V4 and older snapshots are historical. Current Q048 continuation
is V5 above; old method descriptions remain to document earlier certificates.

# Bubbleverse — Q048 controlled prefix continuation V4

Use **🚀 BUBBLEVERSE START**, enter **`Q048-RESUME-V4`**, and press **Run workflow** after installing this package. The canonical launcher remains **`.github/workflows/00-bubbleverse-start.yml`**, registry **`bubbleverse_program_registry.json`**. The launcher performs an exact approved registry lookup; input is never shell code.

Q: **Q-048 — PROPOSED_UNVERIFIED**. CASE: **NOT_ASSIGNED**. Q047 remains **CLOSED INCONCLUSIVE**. Scientific scope: **`CONDITIONAL_SOURCE_REAL_PREFIX`**. **`FINAL_RESULT_GATE=UNRESOLVED`**; actual first-event, complete latch/reset electron histories and optical-depth bounds remain **NOT_COMPUTED**. Program completion establishes only this finite conditional component.

## Install the individual files

Place at repository root:

- `q048_resume_v4.py`, `q048_comparison_v4.py`, `q048_resume_config_v4.json`
- `q048_resume_controls_v4.py`, `q048_resume_control_fixture_v4.json`, `q048_resume_tests_v4.py`
- `q048_resume_merge_v4.py`, `q048_resume_package_check_v4.py`, `q048_resume_package_v4.json`
- `q048_resume_parent_v4.json`, `bubbleverse_program_registry.json`, `README.md`, `Q047_SAMLET_JOURNAL.md`

Place **`q048-resume-v4.yml`** at **`.github/workflows/q048-resume-v4.yml`**. Preserve the existing canonical launcher byte-for-byte. This package was prepared against **`fa85edc216985c02fe88bd5f0b5d03ba5cb3a7a5`**; reconcile newer repository changes before replacing registry/README. Remote installation and dispatch are not performed by the preparation workflow.

Preserve installed frozen dependencies: `q047_math_v1.py`, `q047_certificate_v1.py`, `q047_precursor_check_v1.py`, `q048_prefix_v1.py`, `q048_prefix_config_v1.json`, `q048_resume_v3.py`, `q048_resume_controls_v3.py`. Their hashes are checked. No compile, native CLASS evaluation, solver replacement, re-shoot, refit, sampler or likelihood execution is introduced.

## Numerical change and continuity

The immutable parent is the exact raw final JSON from GitHub **run38230594450**, SHA256 **`12d7cfa0b863e76d0cf3760c532b2a40adbdc789d2b08f8a364a7e488c5c58b3`**. Exact V3 checkpoints reconstruct from it. Camspec EDE starts with424 background/319 thermal cells; Hillipop with340/232. Each LCDM case retains35 thermal cells.

All carried source-real cells are recomputed before continuation, then the entire successor is recomputed after continuation and in collection. Original cells keep their exact predictor, box, certificate and original comparison method. New background cells use positive diagonal similarity with a freshly derived weight; initial radii and defects transform consistently and resulting bounds map back. Stored weights/flags do not count as evidence. The original50 comparison cap and halving schedule0..11 remain.

Only new EDE **He1** thermal cells may use the prospective outer tube `[-2e-6,1/50]`. This requires the original interval proof, a separately checked constant supersolution, negative scalar Jacobian bound, correct phase/background coverage, positive temperature/beta and strict closure. No carried error is narrowed and a negative lower tube does not assert a negative physical state. Unknown proof/tube methods fail closed.

The three frozen finite controls are checked against the incoming exact mathematical evidence. Background alltime bounds also pass an independent positive-matrix series method; the thermal bound uses `R=max(r0,delta/(-L))`. Source evaluation is shared; this is not independent physical source admission. Scope assertions for all actual physical products are enforced as NOT_COMPUTED.

First execution migrates the pinned V3 asset. Later executions search the last20 completed V4 runs for each case's retained V4 checkpoint. Found expired, duplicate, malformed or incompatible artifacts fail closed. A downloaded checkpoint must report the exact retained run selected by the workflow; its metadata run and record run must agree. If none exists in that bounded window, fallback to the pinned V3 asset is explicit in the log and may repeat previous work. An older retained checkpoint can be supplied using the script's `--checkpoint` option. V2 ancestral migration roots survive alongside exact V3 roots and immediate-parent hashes. Earlier V4 parent bytes are authenticated by the retrieved artifact/input path; hash pointers alone do not independently authenticate every historical link.

## Jobs, checkpoints and finite tests

Four independent matrix workers, maximum parallelism4; workflow runs serialized. Each worker has900s preverification,180s background,180s thermal and900s postverification cooperative budgets:36minutes total. A40-minute process safeguard and50-minute job timeout reserve time for checkout and artifact transfer. Preflight and collection use25-minute job timeouts. Collection recomputes case proofs in up to4 parallel processes with a15-minute per-case limit and18-minute process safeguard.

The current standard GitHub-hosted job limit was verified on2026-10-12 as6hours: https://docs.github.com/en/actions/reference/limits . Individual long certificate evaluations can pass a cooperative deadline; the process safeguard preserves the last atomic checkpoint. These are finite stages, not an automatic endless continuation chain. Rerun only for a concrete recovery/information reason; unchanged enclosure blockers need a mathematical change.

Mandatory tests: input/source/Q/scope pins; the three finite controls and independent comparison; exact predecessor/prefix preservation; rejected forged method/weight/certificate and unsupported physical-product claims; valid checkpoint/lineage; case completeness, duplicate/config incompatibility rejection and full merge proof recomputation; launcher/registry/README consistency. Partial reports remain provisional; missing jobs never produce a final scientific result.

## Outputs and handoff

Per-case `*_checkpoint_v4.json`, `*_resume_v4.json` under `q048_resume_results/`; preflight `q048_resume_controls_v4.json`; collector `q048_resume_final_v4.json`. The collector retains raw records and a Q-bound job manifest. A COMPLETE execution may still contain partial scientific histories and retains an UNRESOLVED scientific gate.

Local preparation evidence: `q048_resume_final_v4.json`, individual checkpoints, `q048_resume_local_validation_v4.json` and `Q048_EXECUTION_REPORT_V4.md`. Local calculations used the separately preserved `q048_resume_executed_core_v4.py`; final `q048_resume_v4.py` additionally rejects unsupported result claims and hardens immediate-parent checking. The final collector rechecks all computed cells with the final validation code. The numerical algorithms are unchanged by this admission hardening. These evidence files are not installation prerequisites.

Full authoritative memory: **`Q047_SAMLET_JOURNAL.md`**, including stable sources, claim mappings, technical failures and provenance. Return outputs plus that journal to the **RESULT INGESTION & ROUTING ENGINE**. No scientific closure or Motor14 routing is implied by this package.

The registry preserves all previous entries, marks V3 SUPERSEDED and adds V4 as its successor. Other entries are unchanged. V3 remains the known-good historical reference at the frozen base commit.

---

## Preserved historical repository context

The following sections describe earlier stages. Their installation/start examples are historical; the active Q048 continuation is V4 above.

# Historical Q048 verified prefix continuation V2

PROGRAM_ID: **`Q048-RESUME-V2`**. This finite numerical component verifies and continues the existing **CONDITIONAL_SOURCE_REAL_PREFIX**. `FINAL_RESULT_GATE=UNRESOLVED`. Q-048 remains `PROPOSED_UNVERIFIED`, CASE `NOT_ASSIGNED`; Q047 remains closed inconclusive.

The local continuation has run: Camspec EDE has356 background and251 thermal cells; Hillipop EDE has335 background and231 thermal cells. Both LCDM cases retain their35-cell thermal prefixes through the H transfer at z=2870. Camspec EDE stops at the background time budget; Hillipop EDE stops at comparison growth and thermal-tube closure. These are finite conditional component results, not physical model falsification or complete latch/reset histories.

## Install individual files and start

Place these files at repository root: `q048_resume_v2.py`, `q048_resume_config_v2.json`, `q048_resume_tests_v2.py`, `q048_resume_merge_v2.py`, `q048_resume_package_check_v2.py`, `q048_resume_package_v2.json`, all four shipped `*_checkpoint_v2.json`, the updated `bubbleverse_program_registry.json`, `README.md` and `Q047_SAMLET_JOURNAL.md`. Place `q048-resume-v2.yml` at **`.github/workflows/q048-resume-v2.yml`**. Preserve the exact installed dependencies `q047_math_v1.py`, `q047_certificate_v1.py`, `q047_precursor_check_v1.py`, `q048_prefix_v1.py`, `q048_prefix_config_v1.json` and `q048_prefix_final_v1.json`; their hashes and Git blobs are checked.

The permanent launcher **`.github/workflows/00-bubbleverse-start.yml`**, display name **🚀 BUBBLEVERSE START**, remains unchanged. The canonical registry `bubbleverse_program_registry.json` preserves all57 existing entries and adds this candidate, giving58. The snapshots are based on commit `0208945bb167d1cb2ae3ea15038a8382a7598c15`; reconcile newer repository changes before installing. Remote installation and dispatch have not been performed.

After installation: open **🚀 BUBBLEVERSE START**, paste **`Q048-RESUME-V2`**, select **Run workflow**. The first run continues the shipped local V2 checkpoints. Later runs search the last20 completed V2 runs for each case's newest retained artifact. An expired or invalid found checkpoint fails closed. If no retained artifact exists in that bounded window, the shipped checkpoint is used explicitly. No numerical state is invented and no automatic downstream run is dispatched. Runs are serialized to preserve a clear checkpoint lineage.

## Proof, budgets and result gates

Each case recomputes its carried background and thermal certificates before continuing from the verified endpoints and carried interval errors. V1 omitted proof domains are reconstructed from its exact pinned generation rule; V2 writes them explicitly. Coordinate fractions may have up to4096 characters without rounding; all reused mathematical source files remain byte-unchanged. Inputs, helium convention, phase boundaries, accepted `z_reio`, source commit, neutrino nodes, priors and scientific criteria are preserved. No native CLASS initialization, recompilation, tau shooting, likelihood evaluation or sampling occurs.

Independent budgets are120seconds for checkpoint verification and180seconds each for background and thermal continuation, at most256 new cells per stage with at most10 halvings. Checkpoints are written atomically after verification, every8 accepted cells and at stage boundaries. Four independent case jobs have20-minute timeouts and a12-minute process safeguard; preflight and collection each have10-minute timeouts. Mandatory tests cover corrupted certificates, partitions, question/scope, exact coordinate roundtrip, endpoint consistency and incomplete/invalid collection. If future checkpoint verification exceeds its finite cap, the result stays unresolved and requires a specific verification design change; it does not authorize skipping checks.

The collector requires four final, compatible case reports, retains all raw certificates and never averages unlike cases. `execution_status=COMPLETE` means four component reports exist. Background/thermal statuses may still be partial. `actual_event_redshifts`, `actual_xe_history_bounds` and `actual_tau_T_bounds` remain `NOT_COMPUTED`; `final_result_gate` remains `UNRESOLVED`.

Outputs: per-case `*_checkpoint_v2.json` and `*_resume_v2.json`, collected `q048_resume_final_v2.json`. Current local revalidation is `q048_resume_local_validation_v2.json`. Full authoritative memory remains `Q047_SAMLET_JOURNAL.md`, including source IDs and exact raw result provenance. Return these to the **Result Ingestion & Routing Engine**. Hillipop's enclosure blockers need a mathematical/numerical change, not unchanged repeated launches; actual reference admission, the first cutoff event, post-event propagation and whole-history optical-depth comparison remain outstanding.

---

## Historical repository documentation — preserved below

The following snapshots document their own earlier installation states and entry counts; the V2 instructions above describe the current candidate.

# Historical Q048 conditional source-real prefix V1

PROGRAM_ID: **`Q048-PREFIX-V1`**. This stage computes a controlled common-background/early-thermal **CONDITIONAL_SOURCE_REAL_PREFIX** from the captured inputs. It does not calculate the complete latch/reset histories or their Thomson-depth difference. Actual scientific `FINAL_RESULT_GATE` remains **UNRESOLVED**.

The local computation has already run. Both LCDM references reach the H-mode transfer at z=2870; both EDE references retain a certified partial background prefix at the finite work cap. This is not physical model failure. An unchanged GitHub replay is optional reproducibility, not the missing scientific calculation.

## Install individual files

Place `q048_prefix_v1.py`, `q048_prefix_config_v1.json`, `q048_prefix_tests_v1.py`, `q048_prefix_merge_v1.py`, `q048_prefix_package_check_v1.py`, `q048_prefix_package_v1.json`, `Q047_SAMLET_JOURNAL.md`, the updated `bubbleverse_program_registry.json` and this `README.md` at repository root. Place `q048-prefix-v1.yml` at **`.github/workflows/q048-prefix-v1.yml`**.

Reuse the existing root files `q047_math_v1.py`, `q047_certificate_v1.py` and `q047_precursor_check_v1.py` exactly. The package gate verifies their pinned Git blob identities. No new dependencies, CLASS compilation, native initialization, tau shooting, likelihood evaluation or sampling occurs. The degree32 trigonometric primitive uses an explicit rigorous remainder; the scientific source is unchanged.

The permanent launcher is **`.github/workflows/00-bubbleverse-start.yml`**, display name **🚀 BUBBLEVERSE START**. It remains unchanged. The canonical registry is **`bubbleverse_program_registry.json`**; all 56 previous entries are preserved and one candidate is added. Remote installation and dispatch have not been performed by this engine. Check the registry base if the repository changes before installing this snapshot.

After installation, for an optional replay: open **🚀 BUBBLEVERSE START**, paste **`Q048-PREFIX-V1`**, select **Run workflow**. No launch is needed to obtain the already preserved local results.

## Computation and finite result gates

Four independent case jobs use at most 160 cells per stage and a shared 60-second compute budget per case. Each numerical job has a 120-second process safeguard and a 10-minute workflow timeout, preserving setup/output time. A preflight job checks package/input/launcher/README consistency and finite reference/negative tests. The collection job requires all four identity-compatible results, refuses missing/duplicate cases and preserves raw certificates. Component completion is distinct from prefix completion and scientific validity.

Both native tolerances and exported phase-H starts remain diagnostic evidence. No Boolean can certify actual source applicability. A closed residual/Jacobian tube yields a conditional continuous enclosure; a work/domain cap yields a preserved partial result. The output includes exact rational error endpoints, background forcing bounds, source branch checks, partial endpoints, source hashes, Q/CASE status and explicit missing scopes. Partial background computation is preserved for a future genuinely verified continuation; V1 has no resume CLI and must not be described as resumable.

Results: per-case `*_prefix_v1.json`, collected `q048_prefix_final_v1.json`. That final container includes all raw certificates and keeps `actual_xe_history_bounds=NOT_COMPUTED`, `actual_tau_T_bounds=NOT_COMPUTED` and `final_result_gate=UNRESOLVED`. The full scientific state remains in `Q047_SAMLET_JOURNAL.md`; source IDs and frozen reionization information remain in the journal/config. Return all of these to the Result Ingestion & Routing Engine. Improve the EDE background enclosure/continuation and qualify the actual reference before implementing the shared first event and post-event comparison; do not repeat unchanged input checks.

---

## Existing repository documentation — retained

# Historical Q048 reconstruction metadata qualification V1

Prepared target: **`Q048-INPUTCHECK-V1`**. This package audits the already captured four-case reconstruction from run `38140371059`; it performs no new CLASS initialization, compilation, sampling or likelihood evaluation. The local metadata audit has completed. The GitHub target is a reproducible replay after installation, not a prerequisite to repeating completed work.

Open **🚀 BUBBLEVERSE START**, enter **`Q048-INPUTCHECK-V1`**, then select **Run workflow**. Permanent launcher: `.github/workflows/00-bubbleverse-start.yml` (unchanged). Target: `.github/workflows/q048-input-check-v1.yml`. Registry: `bubbleverse_program_registry.json`. This candidate preserves all 55 existing entries and adds one. Remote installation and dispatch have not been performed.

The stage checks five pinned metadata files per case, their declared source/rate-table links, the seven thermal phase starts, exact hexadecimal ingestion and fixed accepted `z_reio`. The quantity in the CLASS vector is `x_He`; the cutoff quantity is **`q = fHe_CLASS * x_He`**. Four native late-phase samples are slightly below the cutoff. Neither sampled crossing nor repeated equal samples establish a continuous first-event certificate. `FINAL_RESULT_GATE` remains **UNRESOLVED**.

Scientific memory: `Q047_SAMLET_JOURNAL.md`, carrying proposed Q-048 and the complete inherited journal. Contract: `Q048_INPUTCHECK_CONTRACT_V1.json`. Package pins: `Q048_INPUTCHECK_PACKAGE_V1.json`. Code/tests: `q048_inputcheck_v1.py`, `q048_inputcheck_tests_v1.py`, `q048_package_check_v1.py`. Outputs: `q048_inputcheck_results/Q048_INPUTCHECK_RESULT_V1.json` plus the exact contract/package/journal in the result artifact.

Replay uses one finite job with a 20-minute total cap, a 12-minute frozen-artifact retrieval cap, and 90-second test and audit caps. No splitting, checkpoint or mathematical merge is needed for this metadata workload. Missing/expired artifacts fail admission; they do not authorize reconstruction or a version change. No automatic retries or downstream launches are included.

Offline replay: `python -m unittest -v q048_inputcheck_tests_v1`, then `python q048_inputcheck_v1.py --input-root PATH_TO_q047_reconstructed --output NEW_RECEIPT.json`. A pre-existing receipt is never overwritten. Run `python q048_package_check_v1.py` after installing all files at their canonical paths. Keep the permanent launcher unchanged. Apply the registry addition and README/journal updates against the current repository; the supplied complete files are based on commit `76d6b4a4b02ddd929899008f476e99da29c1f931`.

The next scientific requirement is validated qualification of the common upper flow and its first cutoff event or certified no reach. Coupled hydrogen/temperature propagation, smoothing/interpolation and cumulative Thomson-depth bounds follow only if required. This package does not implement those solvers.

---

# Historical Q047 finite-growth precursor backend V1

Current prepared target: **`Q047-PRECURSORCHECK-V1`**. After this candidate package is installed, open **🚀 BUBBLEVERSE START**, paste that exact PROGRAM_ID and select **Run workflow**. Target: `.github/workflows/q047-precursor-check-v1.yml`; registry: `bubbleverse_program_registry.json`. The permanent launcher `.github/workflows/00-bubbleverse-start.yml` is byte-unchanged. All52 existing registry entries are preserved; the candidate has53. No remote installation or launch is claimed by these files.

The backend recomputes rational interval source fields, signed scalar/two-state comparison errors, between-node polynomial defects and strict prospective-tube closure. Positive finite error growth is allowed. It implements algebraic radiation/matter/Lambda/curvature plus declared neutrino references, n_scf=3 EDE background cells, the distinct brec and later thermal equations, four ordered source modes, carried temperature and the helium onset map. Cell coordinate is exact rational **a**; source equations in u=ln(a) are transformed by dy/da=F_u/a. This avoids uncertain log endpoint conversion without changing the model.

**CONDITIONAL** source-real proof inputs are assumptions. The full four-mode radiation fixture is deliberately artificial, and can pass finite source-control gates without qualifying any actual frozen case. All four actual cases remain **INSUFFICIENT_EVIDENCE** and **FINAL_RESULT_GATE=UNRESOLVED**. Effective initialized-instance linkage, actual initialization errors, uncertain source/binary arithmetic and the downstream M06 first-event proof remain outstanding. No native build/init/re-shoot, CLASS call, sampler, optical-depth or likelihood run is included; budget stays16/52 consumed,36 remaining.

Files: `q047_precursor_check_v1.py`, `q047_precursor_tests_v1.py`, `q047_precursor_packet_control_v1.json`, `q047_precursor_package_v1.json`, `Q047_EFFECTIVE_STATE_SCHEMA_V1.json`, unchanged `Q047_PRECURSOR_CONTRACT_V1.json`, and `Q047_PRECURSOR_EXECUTION_SPEC_V1.md`. The backend reuses unchanged installed `q047_math_v1.py` and `q047_certificate_v1.py`. Complete scientific memory remains `Q047_SAMLET_JOURNAL.md`. Source locks identify the exact ten files from class_ede5a131c91...; fetched files are read, never compiled or executed.

One finite job has a10-minute cap, with bounded source retrieval and a90-second backend limit. Work caps return unresolved; there is no retry/sharding/merge/checkpoint or downstream dispatch. Outputs are in `q047_precursor_results/`; technical success does not close Q047.

Replay: `python -m unittest discover -p 'q047_*tests_v1.py' -v`, then `python q047_precursor_check_v1.py --source-dir PATH_TO_PINNED_SOURCE`. Optional conditional primitive input: `--packet FILE`; optional read-only export representation audit: `--audit-effective FILE`. A representation PASS is never actual admission. Do not relaunch old CERTCHECK merely to repeat the previous missing-object list.

---

# Completed prior Q047 certificate qualification — historical

The prior **`Q047-CERTCHECK-V1`** package completed its technical qualification as run38091858306. Its files and target `.github/workflows/q047-certificate-check-v1.yml` remain preserved. Do not relaunch it solely to repeat the unchanged missing-input inventory. The following text documents that preceding package; the current prepared precursor target is described above. At its original preparation, all51 prior registry entries were preserved in the52-entry candidate.

Q-047 remains **PROPOSED; canonical scientific admission unverified**. It asks whether each of four frozen Q041 FULL/start0 helium trajectories reaches the strict numerical cutoff at a first event with negative upper rate and no competing switch/reset. Actual applicability is **INSUFFICIENT EVIDENCE in all four cases**.

V1 implements the Mathematics Engine's source-consistent rational interval/AD field, signed comparison-matrix propagation, prospective error rectangles, continuous predictor bounds and a conditional local event checker. A **manufactured local proof-input control** exercises the checker; it is not an actual cosmological initial state or a complete helium history. The actual-input gate lists the missing effective-model/background/onset/full-path/switch qualifications. An asserted qualification boolean, raw native output or successful process exit cannot pass that gate.

The program performs **zero new CLASS/native/theory evaluations** and cannot launch a cosmology, spectrum, likelihood or sampler. The inherited ledger remains16/52 consumed and36 remaining. It uses Python3.12.14 standard library and pinned source/action identities, with no pip installation, CLASS cache or remote HPC service. One short atomic job has a10-minute cap. There is no shard/merge/checkpoint dependency, automatic retry or downstream dispatch.

Outputs are in `q047_results/`: the technical final JSON, exact required-input reports, manufactured conditional-control certificate, four regional arithmetic controls and package/source/result tests. **FINAL_RESULT_GATE=UNRESOLVED** remains the scientific result even when all technical checks pass. Return the result artifact to Result Ingestion & Routing with the same Q047 and journal; no optical-depth/CMB/likelihood/H0 bias is inferred.

The authoritative accumulated journal snapshot travels as `Q047_SAMLET_JOURNAL.md`. Frozen requested/native identities are in `q047_targets_v1.json`; the executable/source lock is `q047_package_v1.json`; the numerical specification and finite test plan are in `Q047_EXECUTION_SPEC_V1.md`. The source-continuum input remains unqualified. Conditional packet mode is `python q047_certificate_v1.py --packet PATH --out DIRECTORY`; its output remains conditional and cannot close the factual question.

Local replay: `python -m unittest discover -p 'q047_*tests_v1.py' -v`, `python q047_certificate_v1.py`, `python q047_math_v1.py > q047_results/q047_regional_controls_v1.json`, then `python q047_package_check_v1.py results`. No supplied file is an archive.

---

# Completed preceding stage — Q045 offline recovery

The previous Q045 recovery used `Q045-REFHIST-V2` through the same permanent launcher and registry. Its target was `.github/workflows/q045-reference-history-v2.yml`. The Q047 checker is now the current bounded preparation target described above.

**Do not rerun Q045-REFHIST-V1 or either failed native worker.** All eight original computations completed in run [38039690879](https://github.com/Morfindien/Bubbleverse/actions/runs/38039690879). Six passed analysis; both HiLLiPoP L1 jobs failed after computation because V1 required exact equality for BBN-derived `YHe`. Both outputs differ from L0 by one binary64 ULP, while requested physical dictionaries and recorded normalization constants are unchanged. Original failed records remain historical failures.

V2 retrieves the ten frozen original artifacts, verifies archive digests and every member, and reanalyzes the stored histories with `numpy==1.26.4`. It permits at most one ULP only in BBN-derived helium output, records the difference, rejects changed explicit helium/physical inputs or normalization constants, and requires the six originally successful summaries to reproduce exactly. It performs **zero new native/theory evaluations**, needs no CLASS cache or compilation, and cannot launch a native worker. Missing/expired artifacts or incompatible data cause failure. Original GitHub artifacts have 30-day retention; the pinned IDs/digests and raw-member index remain in the contract.

Outputs: `q045_recovery/q045_reference_history_final_v2.json`, eight recovered worker reports and four `*_common_grid.tsv` comparisons. Each report preserves the original status/error and its worker hash. The locally recovered final result and common grids are also delivered individually.

Recovery has passed for all eight stored histories. This is a component diagnostic: `REFERENCE_TRUTH_GATE=UNQUALIFIED`, `FINAL_RESULT_GATE=UNRESOLVED`. No CMB/likelihood response or continuum-error enclosure has been computed. The accepted tau sequence is non-monotonic at all four points, so no positive Richardson order is established for it. Budget remains16/52 consumed and36 remaining; the unmodified FULL matrix remains incompatible with the cap. No automatic next stage is authorized.

The authoritative journal is `Q045_SAMLET_JOURNAL.md`; complete handoff/source history is `Q045_EXECUTION_HANDOFF.md`. Existing V1 source, contract, manifest, observer and workflow remain unchanged for provenance. Registry status blocks repeating V1 through the launcher.

---

# Bubbleverse HPC

**One question at a time. Reproducible execution. Evidence before model.**

Bubbleverse HPC is the public research-execution and reproducibility repository behind the Bubbleverse project.

Bubbleverse does not begin with a model that must be defended. It begins with a scientific question. When a question requires numerical work, this repository is where the computational experiment is defined, locked, executed, tested and preserved.

The scientific model that survives this process is maintained separately in [`Morfindien/bubbleverse-model`](https://github.com/Morfindien/bubbleverse-model).

Website: **https://bubbleverse.dk**


## Completed prior stage — Q045 optical audit V3

Q042 and Q044 remain closed with inconclusive scientific boundaries. Q045 remains **PROPOSED; canonical scientific registration pending**.

V2 baseline run [38023210800](https://github.com/Morfindien/Bubbleverse/actions/runs/38023210800) completed all four native FULL diagnostic starts. Installation, completeness and raw-product gates passed. Those starts are fixed inputs, not fitted minima; their likelihood values establish no model preference. The registry records `Q045-BASELINE-V2` as **COMPLETED** so it is not relaunched unchanged. Its V1 failed installation and V2 Flit repair remain preserved.

Completed PROGRAM_ID: **`Q045-OPTICAL-AUDIT-V3`** (the prior duplicated `Q045-` prefix is corrected). The registry records this target **COMPLETED**, run [38035928310](https://github.com/Morfindien/Bubbleverse/actions/runs/38035928310). Its original files and workflow are retained for provenance, not another unchanged launch. The historical recovery launcher target was `Q045-REFHIST-V2`; V1 native computation completed and must not be repeated.

The completed target retrieved the exact four completed V2 worker artifacts, then uses read-only original-function observation to export each scalar calibration trial/support, raw cumulative optical depth before exponentiation, effective precision/constants and species workspace snapshots. The unchanged original diagnostic CLASS binary and source are required; there is no cache-miss rebuild, scientific source patch, new spectrum/likelihood run, optimizer, sampler or automatic retry. Final native table columns must exactly match V2. Separate worker jobs have45-minute caps and15-minute native-process caps. The original52-evaluation budget is retained: four V2 evaluations already complete, at most four telemetry observations now, at most44 slots remaining after all four start. Background/thermodynamics observations do not constitute full CMB/likelihood reproducibility runs.

Controller `q045_optical_audit_v3.py`; native observer `q045_optical_audit_probe_v3.c`; immutable contract `q045_optical_audit_contract_v3.json`; integrity manifest `q045_optical_audit_manifest_v3.json`; finite tests `q045_optical_audit_tests_v3.py`. Complete current memory: `Q045_SAMLET_JOURNAL.md`; baseline ingestion record: `Q045_INGESTION_RESULT.json`.

Native-plus, exact-cubic-minus and independent same-cubic Gauss integration are **component diagnostics**. Redshift-space node quadrature is a shared-history diagnostic. Both remain **UNQUALIFIED** as continuum Thomson references. Workspace species after source returns may reflect a previous regime during smoothing and are not separately certified physical histories. No treatments10/01/11, three new accuracy levels or inference continuation dispatch automatically. Preserve raw anomalies/failures and return to Result Ingestion & Routing.

Outputs: `q045-audit-<run_id>-baselines`, four `q045-audit-<run_id>-worker-<job>` artifacts and `q045-audit-<run_id>-final`. Final JSON: `q045_optical_audit_final_v3.json`. Missing, duplicate or incompatible workers yield PARTIAL and failing technical merge gates. Even complete acquisition retains `FINAL_RESULT_GATE=UNRESOLVED` and `REFERENCE_TRUTH_GATE=UNQUALIFIED`. Exact histories, raw κ and full provenance survive in worker artifacts. A prior launch of this target blocks a new unchanged dispatch; recovery requires reviewing preserved records before assigning another executable version.


Optical audit V1 [run38026287784](https://github.com/Morfindien/Bubbleverse/actions/runs/38026287784) failed before all four observations. Its key was correct but its shortened cache path list selected a different cache version. The V2 repair restored the original nine-path list exactly, while retaining no rebuild/fallback/save and the frozen source/binary checks. V1 consumed zero theory-evaluation slots. Failure evidence: `Q045_OPTICAL_AUDIT_V1_FAILURE.json`. Ten controller tests include the cache-identity regression; the native observer is unchanged. The V2 run subsequently verified cache restoration; V3 subsequently completed all four observations and collection in run38035928310.


Optical audit V2 [run38030968453](https://github.com/Morfindien/Bubbleverse/actions/runs/38030968453) restored the original cache successfully in every worker, then failed its test because the workflow was read from the wrong directory. No original cosmological observation started. V3 reads `.github/workflows/q045-optical-audit-v3.yml`; local validation uses the actual installed layout without a root YAML duplicate. The source/binary/physical contract is unchanged. Failure evidence: `Q045_OPTICAL_AUDIT_V2_FAILURE.json`. Prior V1 evidence remains retained.

---

## What this repository is

This repository is the execution side of Bubbleverse.

It contains the machinery used to turn a scientific question into a traceable computational result, including:

- GitHub Actions workflows
- scientific Python programs
- setup and environment scripts
- preregistrations
- source locks
- program registries
- validation tests
- execution notes and install manifests
- result-artifact contracts
- historical and superseded implementations

The repository intentionally preserves technical history. A newer workflow may supersede an older one without erasing the path that led to it.

This is therefore both an active research system and a reproducibility record.

---

## The basic workflow

A Bubbleverse computational question normally moves through a chain like this:

```text
Scientific question
        ↓
Preregistered test
        ↓
Locked sources / data / environment
        ↓
Registered PROGRAM_ID
        ↓
GitHub Actions execution
        ↓
Numerical result artifacts
        ↓
Validation and scientific gates
        ↓
Result / handoff
        ↓
Bubbleverse Model
```

The exact route depends on the question.

Not every question needs HPC, and not every numerical run produces a scientific result.

---

## Start system

The repository includes a central launcher for registered programs.

From GitHub:

1. Open **Actions**
2. Select **🚀 BUBBLEVERSE START**
3. Press **Run workflow**
4. Enter the exact `PROGRAM_ID`
5. Start the run

The launcher checks the registry before dispatching the scientific workflow.

It verifies the exact `PROGRAM_ID`, active status, Q identity and allowed workflow/ref syntax against `bubbleverse_program_registry.json`.

The permanent launcher is `.github/workflows/00-bubbleverse-start.yml`. It dispatches the registered target; that target validates its inputs and publishes its own results. Open the child run to inspect its outcome.

### Q-042 completed CLASS diagnostics; treatment not yet runnable

V22 run `37221166634` completed the one-branch durability task; V23 run `37264477494` completed original-binary spline attribution; V24 run `37275520455` completed original-binary tau-path observation. V25 run `37288546095` completed one-point upstream boundary attribution at commit `3d15a3a7a627de2f29533cac7fe9e43dd022226f`. These technical targets are `COMPLETED`; scientific Q-042 is now closed with an inconclusive feasibility result; its numerical final result remains `UNRESOLVED`.

V25 observed finite inputs and an infinite helium derivative at the low-temperature cutoff boundary. The original upper optical-depth trial is nonfinite, the routine returns success after two trial calls and zero bisection iterations, and the table remains byte-identical to V23/V24. The first observed function boundary is not asserted to locate the globally first invalid arithmetic operation. Preserve both V25 artifacts and all 80 inherited optimizer records.

Do not launch `Q042-CLASSNAN-V25` again unchanged. The registry now records its completed run, so the permanent launcher rejects that inactive target. Existing V23–V25 controllers, contracts, observers, tests, workflow files and historical manifests remain preserved. Keep `.github/workflows/00-bubbleverse-start.yml` unchanged.

A coupled numerical treatment requires valid matched references, an explicit justified helium phase/cutoff rule, frozen prediction/likelihood and optical-depth accuracy criteria, and a separate executable/config/checkpoint lineage before execution. No treatment target or new `PROGRAM_ID` has been registered. No repaired CLASS binary, new sampler/optimizer run, scientific result or production restart is authorized by these diagnostic completions. Return the documented state to the Result Ingestion & Routing Engine.

The registry is the authoritative mapping between a program identifier and the workflow that is allowed to execute it.

---

## Program registry

The central registry is:

```text
bubbleverse_program_registry.json
```

A registered scientific program can define information such as:

```text
PROGRAM_ID
Q
workflow
scientific program
tests
preregistration
source lock
result ID
expected artifacts
status
version
supersession history
```

This makes the execution path explicit instead of relying on filenames or memory.

Programs may be marked, for example, as active, broken or superseded as the implementation evolves.

---

## Scientific locking

Bubbleverse HPC tries to separate scientific changes from technical repairs.

For demanding runs, the repository can preserve or lock:

- source versions
- external repository commits
- data definitions
- package versions
- execution commits
- priors and parameter definitions
- scientific acceptance criteria
- expected result artifacts

Where practical, later technical versions reuse an already validated scientific setup rather than silently changing the experiment.

A technical repair should not become a scientific change by accident.

---

## Preregistration

Many workflows include a preregistration file before the numerical result exists.

Typical files follow patterns such as:

```text
q###_*_preregister_*.json
```

A preregistration can define the test surface, comparison rules, acceptance thresholds, allowed branches of the analysis and other scientific decisions that should not be rewritten after seeing the outcome.

This is used to reduce result-driven rule changes.

---

## Source locks and provenance

Scientific programs can also carry source-lock files such as:

```text
q###_*_source_lock_*.json
```

These record the external scientific state required by the run.

Depending on the experiment, this may include exact commits, datasets, numerical packages or previously validated Bubbleverse results.

Runtime setup can additionally record hashes and provenance for installed or downloaded scientific inputs before the main calculation begins.

The goal is simple:

> A result should remain connected to the exact scientific inputs that produced it.

---

## Tests and gates

The repository contains question-specific validation code as well as workflow-level gates.

These can test things such as:

- registry consistency
- preregistration consistency
- source-lock identity
- valid numerical inputs
- finite likelihoods
- expected parameter support
- convergence
- artifact completeness
- scientific classification rules
- reproducibility contracts

A workflow reaching the end of GitHub Actions is not, by itself, proof that a scientific result exists.

Technical success and scientific success are deliberately treated as different things.

---

## Long-running computation

Some Bubbleverse questions are small.

Others are not.

Long numerical campaigns can use:

- matrix execution
- parallel independent chains
- cached scientific environments
- checkpointed or resumable state
- segmented runs
- bounded runtime per segment
- continuation decisions
- final convergence gates

For example, current portability workflows can split independent posterior chains into bounded compute segments, preserve resumable state and continue until the preregistered completion criteria are reached or the allowed execution boundary is exhausted.

This is designed to make long calculations survive the practical limits of hosted CI infrastructure without pretending an incomplete chain is a finished result.

---

## Artifacts are part of the record

Bubbleverse workflows use named GitHub Actions artifacts as part of the scientific handoff.

Artifacts may contain:

- static validation results
- environment provenance
- numerical chains
- endpoint results
- test outputs
- run manifests
- preregistration copies
- source-lock copies
- final classifications
- handoff material

The expected artifact set can be registered before execution.

Missing required artifacts can therefore be treated as a failed execution contract rather than silently ignored.

---

## Failure is preserved

Bubbleverse does not require every program version to succeed.

The repository contains technical failures, superseded attempts and repaired implementations because they are part of the development and scientific audit trail.

A failed version may reveal:

- non-convergence
- an invalid environment
- an artifact-contract failure
- a numerical instability
- an implementation error
- a scientific incompatibility

Where a later version repairs a technical problem, the earlier failure can remain documented instead of being rewritten out of history.

Negative and failed results are information.

---

## Current cosmology work

The repository currently contains a substantial cosmology execution chain, including work on:

- Hubble-constant inference
- Early Dark Energy
- likelihood attribution
- optimizer/globality tests
- Planck likelihood implementations
- CamSpec / HiLLiPoP comparisons
- ACT information
- BAO information
- robustness and portability tests

One example is the Q041 downstream portability campaign, which tests whether a validated CamSpec–HiLLiPoP geometry difference in an n=3 EDE analysis remains scientifically consequential after adding matched external CMB, lensing and BAO information.

The individual scientific conclusions should be taken from their completed result artifacts and the accepted Bubbleverse model — not inferred from the existence of a workflow alone.

---

## Repository map

The repository is intentionally execution-oriented rather than arranged like a conventional software library.

Important areas and filename families include:

```text
.github/workflows/
    GitHub Actions launchers and question-specific execution workflows

bubbleverse_program_registry.json
    Central program-to-workflow registry

q###_*.py
    Scientific programs, analysis code and validation tests

q###_*.sh
    Environment preparation and execution setup

q###_*_preregister_*.json
    Preregistered scientific rules

q###_*_source_lock_*.json
    Locked scientific sources and external dependencies

*_INSTALL.txt
*_manifest.txt
*_NOTE.txt
    Installation, repair, execution and provenance notes
```

Because Bubbleverse preserves the research path, multiple versions of a program can coexist.

The registry and status fields determine which version is authoritative for execution.

---

## Relationship to Bubbleverse Model

Bubbleverse uses two public repositories with different jobs.

### Bubbleverse HPC

Repository:

[`Morfindien/Bubbleverse`](https://github.com/Morfindien/Bubbleverse)

Purpose:

**Execute, test and preserve scientific computations.**

This is where numerical experiments, workflows, source locks, preregistrations, artifacts and execution history live.

### Bubbleverse Model

Repository:

[`Morfindien/bubbleverse-model`](https://github.com/Morfindien/bubbleverse-model)

Purpose:

**Maintain the version-controlled scientific model state produced from validated Bubbleverse evidence.**

It contains accepted and candidate model states, formalization, tests, provenance, releases and version history.

In short:

```text
Bubbleverse HPC  →  asks and computes
Bubbleverse Model →  retains what survives
```

---

## Scientific philosophy

Bubbleverse is not designed to prove Bubbleverse.

It is not designed to defend standard cosmology.

It is not designed to reject standard cosmology.

The working rule is:

> **Reality has priority over the model.**

If a Bubbleverse idea fails, it should fail.

If an established result survives testing, it should survive.

If the evidence is insufficient, **unknown** is a valid scientific outcome.

The purpose of computation is not to manufacture certainty.

It is to make uncertainty, assumptions, failures and surviving results more explicit.

---

## Reproducibility notice

This repository is an active research environment, not a stable general-purpose software package.

Historical workflows may depend on:

- specific GitHub Actions behavior
- exact external commits
- cached environments
- external scientific datasets
- artifacts from earlier Bubbleverse runs
- version-specific numerical software

The existence of source code does not guarantee that every historical workflow can be rerun indefinitely without reconstructing its original environment.

Where the project has locked enough provenance to reconstruct that environment, those locks should be preferred over replacing dependencies with newer versions.

---

## Public use

The repository is public so the computational side of Bubbleverse can be inspected.

You are welcome to:

- read the code
- inspect workflows
- examine preregistrations and source locks
- follow the execution history
- fork the repository
- reproduce or independently challenge results

A fork or third-party modification is not an official Bubbleverse result unless it is incorporated into the authoritative Bubbleverse process.

---

## Contact

**jnperdersen@bubbleverse.dk**

---

## Links

- Website: https://bubbleverse.dk
- Bubbleverse HPC: https://github.com/Morfindien/Bubbleverse
- Bubbleverse Model: https://github.com/Morfindien/bubbleverse-model

---

## Final rule

**One question at a time.**

**Lock the test.**

**Run the evidence.**

**Preserve the failures.**

**Change the model when reality demands it.**


## Q-042 V26 bounded raw reference acquisition

`Q042-REFACQ-V26` is a completed historical diagnostic (run `37323656302`), with result status `RAW_NOT_QUALIFIED`. Do not relaunch it unchanged. The historical target is `.github/workflows/q042-reference-acquisition-v26.yml`.

The frozen `q042_reference_contract_v26.json` and byte-exact `q042_reference_point_v26.ini` define two fixed trials, RK4 and implicit midpoint, levels1/2/4:12 branches attempted once. The original cached CLASS source and binary must match their pinned identities; the binary is never rebuilt. A common original background/recombination prefix supplies conditional initial state. Isolated child processes implement the new stepping and preserve failures. No root search, spectra, optimizer, posterior, production restart, automatic retries or resume is authorized.

Results are **RAW_NOT_QUALIFIED**, even when all twelve branches complete. Observed differences, point-sampled defects and same-spline optical depths do not establish an independent true history or downstream likelihood accuracy. Reporting completeness, numerical branch completeness and scientific qualification are separate gates.

The worker has bounded call/time/storage budgets and a60-minute job limit. This finite target uses one worker; no long stateful chain, checkpoint or merge across different configurations is needed. Collection checks all twelve identities and artifact hashes. Raw nodes, defects, accepted entry/grid, logs and `q042_reference_worker_result_v26.json` are in `q042-v26-<run_id>-raw-acquisition`; the collected result is `q042-v26-<run_id>-diagnostic-final`. The complete received journal is retained verbatim in `q042_execution_handoff_reference_v26.md`; the contract carries source IDs and claim mappings. Return actual artifacts to Result Ingestion & Routing.

V25, its hash failure and earlier scientific/technical history remain historical. V26 validates this mutable README semantically rather than against a prior campaign's README hash.


## Q-042: bounded original HyRec switch attribution (V27)

`Q042-SWITCHPROBE-V27` is a completed historical diagnostic (run `37333030105`), with result status `RAW_NOT_QUALIFIED`. Do not relaunch it unchanged.

This diagnostic restores the original hash-pinned CLASS cache and evaluates only 24 fixed-state RHS samples on either side of the original HyRec temperature threshold. It reuses two RAW V26 states; it does not integrate a new history, solve a root, run likelihoods or restart production. Results remain `RAW_NOT_QUALIFIED`. The target is `.github/workflows/q042-switch-probe-v27.yml`; artifacts are `q042-v27-<run_id>-raw-switch-probes` and `q042-v27-<run_id>-diagnostic-final`.

Three bounded jobs check package identity, acquire two isolated probe sets and collect their completeness/model-route evidence. Finite derivative offsets and solver stage fingerprints do not qualify a reference history. The inherited journal and original scientific contract remain in `q042_execution_handoff_switch_v27.md`.


## Historical Q-042 event-aware cell diagnostic (V28)

`Q042-EVENTCELL-V28` completed as run `37347357296`, with result status `RAW_NOT_QUALIFIED`. It is not the next runnable target. The historical workflow is `.github/workflows/q042-event-cell-v28.yml`; do not repeat it unchanged.

This target preserves the original cached CLASS binary, physical switch and frozen scientific contract. It compares only one native crossing cell at the two archived RAW V26 conditioning states, using RK4 L1/L2/L4 (six independent branches;112 original-kernel stages). The terminal pre-event stage samples the immediately adjacent representable pre-event coordinate; the post-event segment restarts at the exact threshold with the same propagated state. Actual routing and the additional temperature-ratio predicate are checked at every stage. A new active crossing fails explicitly.

Three jobs perform static/numerical tests, one bounded worker, and failure-aware collection. The existing cache is restored read-only; a missing or mismatched original binary fails rather than rebuilding or changing dependencies. Successful branch outputs are preserved; no automatic retry or continuation campaign is configured. This finite diagnostic needs neither a checkpoint nor a numerical merge of independent trajectories.

Raw stages, accepted nodes and endpoints are in `q042-v28-<run_id>-raw-event-cell`; the final diagnostic is in `q042-v28-<run_id>-diagnostic-final`. `q042_event_final_v28.json` reports finite refinement and heuristic roundoff diagnostics. RAW_NOT_QUALIFIED, REFERENCE_TRUTH_GATE=BLOCKED and FINAL_RESULT_GATE=UNRESOLVED remain explicit. A local technical PASS does not qualify a history, prefix, tau root, predictions, likelihood or cosmological inference.

`q042_event_contract_v28.json` preregisters the scope/tests/interpretation. `q042_execution_handoff_event_v28.md` preserves the complete received journal verbatim, and `q042_event_source_evidence_v28.json` carries the source register, claim map and V27 raw/provenance evidence. Return the raw and final diagnostic to Result Ingestion & Routing after this one pass, including unresolved or failed outcomes. Do not repeat V27, add L8/L16, or restart production.


### V28 fixture identity correction (fixture-runid-r1)

Run37344813050 stopped in the controlled test before any actual original-binary cell computation: the fixture used `LOCAL` while the strict collector expected GitHub's run-id. The fixture now inherits `GITHUB_RUN_ID`, falling back to `LOCAL` only outside Actions; unrelated identities remain rejected. Numerical physics,contract,program,workflow,registry and launcher are unchanged. The complete failure/provenance and journal update are in the current V28 handoff/source evidence.

The fixture correction was followed by completed run `37347357296`. The failed run and fix remain historical evidence; no further V28 launch or retry is required. Local implementation tests and successful cell execution do not qualify whole-history accuracy.



## Q-047: approved four-case reconstruction V1

The current target is **Q047-RECONSTRUCTION-V1**. Once the individual files are
installed, open **🚀 BUBBLEVERSE START** (`.github/workflows/00-bubbleverse-start.yml`),
enter that PROGRAM_ID and press **Run workflow**. The launcher is unchanged;
`bubbleverse_program_registry.json` resolves the exact ID to
`.github/workflows/q047-reconstruction-v1.yml`.

The original environment preflight V1 completed as run38113104261. It is a
historical acquisition/build result and is not to be launched again unchanged.
The new acquisition is explicitly approved by the user; its contract is
`Q047_RECONSTRUCTION_CONTRACT_V1.json`. It preserves the exact Q047 question,
source/core/input pins and the original precursor contract V1.

Four independent case jobs restore the exact original nine-path cache, verify
source and binary, acquire their hash-pinned original reference tables, and
compile only observer v2. Each performs one new input/shooting/background/thermal
initialization, with a600-second native process cap. There is no core rebuild,
production fit, CMB/likelihood evaluation, retry or checkpoint campaign.

Captured binary64 state is marked **NEW_RECONSTRUCTION**, never historical export.
It includes accepted initial vectors, effective scalar fields, neutrino nodes
and weights, thermal starts and precision. Six new-run FP checkpoints, CPUID/XCR0,
math-symbol reference addresses and loaded-object hashes are saved. Actual libm,
libc/loader/OpenMP objects and pinned source/data inputs are preserved separately.
Observer formatting restores the surrounding FP environment; full observer
neutrality and all-call error bounds remain unproved.

The new ledger counts up to four top-level capture processes and records every
internal initialization entry. It does not assume that four cases cost four
shooting calls or silently redefine the inherited16/52 native/theory ledger.
The explicit approved capture scope is separate; no full theory evaluation is
performed.60-minute case jobs run with max-parallel4; the collector has15 minutes.
These caps are below the checked6-hour hosted-runner hard job limit. Runtime and
cache transfer variability are not measured for this new target.

Raw artifacts: `q047-reconstruction-v1-<run_id>-<case>-raw`. Final artifact:
`q047-reconstruction-v1-<run_id>-final`, containing
`q047_reconstruction_final_v1.json`, the frozen new contract and full
`Q047_SAMLET_JOURNAL.md`. Four-case collection checks IDs, config/contract and every
raw member hash; missing cases produce PARTIAL_OR_FAILED. It never averages
incompatible trajectories. Failed gates and nonmatching tables remain evidence.

Even a COMPLETE acquisition retains **INSUFFICIENT_EVIDENCE** and
**FINAL_RESULT_GATE=UNRESOLVED** for the historical first-hit question. Exact output
equality is not a proof of unique historical state or source-real trajectory
accuracy. Return the actual new raw states to Result Ingestion & Routing for the
specific state/linkage/error qualification, then the unchanged first-event test
where admissible. Do not repeat a successful capture merely to obtain more
agreement.

Before launch, read `Q047_RECONSTRUCTION_INSTALLATION_V1.md`. The prepared files
have not been remotely installed or executed by the authoring agent.
