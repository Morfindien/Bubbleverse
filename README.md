# Bubbleverse HPC

**One question at a time. Reproducible execution. Evidence before model.**

Bubbleverse HPC is the public research-execution and reproducibility repository behind the Bubbleverse project.

Bubbleverse does not begin with a model that must be defended. It begins with a scientific question. When a question requires numerical work, this repository is where the computational experiment is defined, locked, executed, tested and preserved.

The scientific model that survives this process is maintained separately in [`Morfindien/bubbleverse-model`](https://github.com/Morfindien/bubbleverse-model).

Website: **https://bubbleverse.dk**

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

`Q042-REFACQ-V26` is one isolated diagnostic target. Open **🚀 BUBBLEVERSE START**, enter that PROGRAM_ID and press **Run workflow**. The canonical launcher is `.github/workflows/00-bubbleverse-start.yml`; exact target resolution uses `bubbleverse_program_registry.json`. The internal target is `.github/workflows/q042-reference-acquisition-v26.yml`.

The frozen `q042_reference_contract_v26.json` and byte-exact `q042_reference_point_v26.ini` define two fixed trials, RK4 and implicit midpoint, levels1/2/4:12 branches attempted once. The original cached CLASS source and binary must match their pinned identities; the binary is never rebuilt. A common original background/recombination prefix supplies conditional initial state. Isolated child processes implement the new stepping and preserve failures. No root search, spectra, optimizer, posterior, production restart, automatic retries or resume is authorized.

Results are **RAW_NOT_QUALIFIED**, even when all twelve branches complete. Observed differences, point-sampled defects and same-spline optical depths do not establish an independent true history or downstream likelihood accuracy. Reporting completeness, numerical branch completeness and scientific qualification are separate gates.

The worker has bounded call/time/storage budgets and a60-minute job limit. This finite target uses one worker; no long stateful chain, checkpoint or merge across different configurations is needed. Collection checks all twelve identities and artifact hashes. Raw nodes, defects, accepted entry/grid, logs and `q042_reference_worker_result_v26.json` are in `q042-v26-<run_id>-raw-acquisition`; the collected result is `q042-v26-<run_id>-diagnostic-final`. The complete received journal is retained verbatim in `q042_execution_handoff_reference_v26.md`; the contract carries source IDs and claim mappings. Return actual artifacts to Result Ingestion & Routing.

V25, its hash failure and earlier scientific/technical history remain historical. V26 validates this mutable README semantically rather than against a prior campaign's README hash.
