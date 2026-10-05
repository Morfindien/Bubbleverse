# Bubbleverse HPC

**One question at a time. Reproducible execution. Evidence before model.**

Bubbleverse HPC is the public research-execution and reproducibility repository behind the Bubbleverse project.

Bubbleverse does not begin with a model that must be defended. It begins with a scientific question. When a question requires numerical work, this repository is where the computational experiment is defined, locked, executed, tested and preserved.

The scientific model that survives this process is maintained separately in [`Morfindien/bubbleverse-model`](https://github.com/Morfindien/bubbleverse-model).

Website: **https://bubbleverse.dk**


## Current Q-042 target — V29 initialized context and interval prerequisite

Q-042 remains open. V26/V27/V28 are completed `RAW_NOT_QUALIFIED` diagnostics; do not relaunch them. The prepared active target is `Q042-CONTEXT-V29`. It captures the hash-pinned original initialization once and checks a bounded real-table interval RHS prerequisite. It does not integrate a history, search for a root, evaluate a likelihood or restart production.

Install the individual V29 files at the repository root, except `q042-context-v29.yml`, which belongs in `.github/workflows/`. Install this README and `bubbleverse_program_registry.json` together with the immutable package. The existing launcher is unchanged: **[🚀 BUBBLEVERSE START](https://github.com/Morfindien/Bubbleverse/actions/workflows/00-bubbleverse-start.yml)** → enter **`Q042-CONTEXT-V29`** → **Run workflow**. Canonical launcher: `.github/workflows/00-bubbleverse-start.yml`; registry: `bubbleverse_program_registry.json`.

Controller: `q042_context_v29.py`; native capture: `q042_context_native_v29.c`; interval evaluator: `q042_interval_v29.py`; frozen configuration: `q042_context_contract_v29.json`; immutable hashes: `q042_context_manifest_v29.json`. Finite tests: `q042_interval_tests_v29.py` and `q042_source_check_v29.py`. The unchanged original binary is restored from the existing exact-key cache; there is no rebuild fallback. The evaluator requires MPFR 4.2.1 on Linux x86_64 and uses directed rounding. A different version fails preflight.

There is one computational worker between static and collection jobs. The worker has a 50-minute timeout; original initialization is capped at 600 seconds and interval qualification at 300 seconds. No trajectory sharding, checkpoint or resume is needed. A prior V29 workflow attempt blocks another acquisition; failures go back to ingestion rather than automatic retry.

Outputs are under `context_v29/`: exact hexadecimal initialized tables/grid, provenance and hashes, original point diagnostics, continuous background positivity checks and interval boxes. GitHub output names are `q042-v29-<run_id>-context-and-checks` and `q042-v29-<run_id>-final`; final JSON is `q042_context_final_v29.json`. Full journal/source/provenance continuity is in `q042_context_full_handoff_v29.md`.

Local checks qualify only implementation tests. Actual capture and real-table checks are pending until execution. Even runtime prerequisite success leaves original-binary arithmetic bounds, upstream accuracy and the complete history/reference/scientific result **UNRESOLVED**. Successful point containment is diagnostic; it is not a history-error proof. Return either the completed prerequisite or the concrete failed gate to the Result Ingestion & Routing Engine.

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

V22 run `37221166634` completed the one-branch durability task; V23 run `37264477494` completed original-binary spline attribution; V24 run `37275520455` completed original-binary tau-path observation. V25 run `37288546095` completed one-point upstream boundary attribution at commit `3d15a3a7a627de2f29533cac7fe9e43dd022226f`. These technical targets are `COMPLETED`; scientific Q-042 remains `UNRESOLVED`.

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
