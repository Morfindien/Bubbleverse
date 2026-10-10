# BUBBLEVERSE — OVERLEVERING

STATUS: V1 FAILED IN ENVIRONMENT SETUP; V2 REPAIR PREPARED, NOT INSTALLED OR DISPATCHED BY ASSISTANT.

DATE AND TIME: 2026-10-10T04:04:19.081115+00:00 (UTC).

FAILURE CLASS: ENVIRONMENT. Run #2 `38021982095` at `7b5047dd9eafbd7986c15514ec3534e2b0ed3bc3`: all four ACT lensing editable installs failed because V1 disabled build isolation without supplying flit_core. Static and input acquisition passed; all numerical evaluation steps were skipped. V2 adds `flit_core==3.12.0` and an early import/version/editable-capability gate. The failure and repaired build were reproduced locally with Python 3.12.14; this does not certify the complete Python 3.11.16 GitHub environment.

Failure/source evidence: [run](https://github.com/Morfindien/Bubbleverse/actions/runs/38021982095), [frozen backend declaration](https://github.com/ACTCollaboration/act_dr6_lenslike/blob/b386ddbb5821c1216c709f051c9289292f174d30/pyproject.toml).

## A. Current Q

CURRENT Q: Q045 / Q-045 — PROPOSED; canonical scientific registration pending.

The scientific question is retained verbatim in the contract and authoritative journal. It asks whether replacing the native optical-depth functional, at identical requested tau and otherwise frozen Q041 inputs, changes CMB spectra/native likelihood enough to threaten original H0/EDE decision margins. This package acquires prerequisites only.

## B. ChatGPT setting

RECOMMENDED: current Work/Codex with strong reasoning, code/files and authenticated repository access; High reasoning if selectable. Capability classes C/A + H. This is a contained code adaptation and validation task. ASTRA MAX availability and exact active effort are not verified; no mode switch occurred.

FALLBACK: GPT-5.6 if available with equivalent capabilities. Upgrade for difficult independent reference/error qualification or extensive inference, not for this fixed four-point acquisition.

## C–H. Capability, execution and scientific decision

RELEVANT AVAILABLE CAPABILITIES: authenticated GitHub read/search/artifact retrieval, local Python/file execution, primary-source web lookup and persistent file delivery. GitHub recovered the actual original frozen inputs; local code verified hashes and package integrity. No browser, new plugin installation or parallel agents were required.

EXECUTION MODE: existing numerical execution engine + conventional finite program. EXISTING MOTOR SUFFICIENT: YES. No additional motor prompt is created.

SCIENTIFIC REQUIREMENT: before implementing the scalar/cumulative reference treatments, acquire valid native FULL baseline products at the four frozen diagnostic starts. Success is necessary preliminary evidence; it cannot answer the main question or qualify reference accuracy.

JOURNAL: KEEP the complete incoming journal, Q and source IDs, previous results, failures and scientific boundaries. ADD V1 failure provenance, local build reproduction and the minimal V2 repair. Preserve the full earlier journal verbatim. Q044 and Q042 stay closed inconclusive. Q045 stays proposed. The complete updated authoritative journal is `Q045_SAMLET_JOURNAL.md`; it contains all incoming bytes unchanged after its differential update. It replaces the supplied journal's identity and does not start a parallel journal.

## I. GitHub inspection and reuse

Execution repository: `Morfindien/Bubbleverse`.

Inspected main: `7b5047dd9eafbd7986c15514ec3534e2b0ed3bc3`. The current registry has Q045 V1 and no V2. Current README/journal/registry match the previously delivered bytes/state. The existing launcher is unchanged.

REUSE unchanged existing repository files:

- `.github/workflows/00-bubbleverse-start.yml`
- `q042_production_v1.py`
- `q042_planck_portability_v11.py`
- `q041_planck_portability_v13.py`
- `q041_setup_v13.sh` (only its frozen DESI compatibility excerpt is incorporated in the new setup).

Q032 builders/configuration are materialized from commit `4dc873a5e880d40858d831a3b421456728f0c032`. Their `external` directory is mapped to the unchanged restored backend/data paths. No physical input is changed by this path mapping.

Recovered original environment/input source: Q042 V1 run `36133813540`, artifact `10862038917`, head `6c44a4117449145afd0a3ae6eb238490686a8c6d`, 278412344 bytes, SHA256 `162b99026d025d1021fa8a83dbf4290b7bd0c2c53917ea56cbf04f8b169bff4a`. All 29 internal file hashes are frozen in the contract, including 18 parent endpoint records, sealed preflight, full/reduced precision matrices, support, original spec/lock and runtime/SN manifests. No reconstructed JSON substitutes for those original files.

Original Q032 final was independently retrieved as artifact `9980784387`, run `33994305721`, digest `dd7b069337aeee660d1c46158f78d9a81d6a0115309f6b333e8555899308d692`. CamSpec M6-S0 and HiLLiPoP M6-S2 are the recovered native parent references. The runtime selects them through the original nine-record-per-arm algorithm.

Historical incomplete production, Q040 science endpoints and unqualified physical reference paths are not reused as scientific results.

## J. Frozen numerical specification

MODEL: original native LambdaCDM / n_scf=3 EDE, unchanged physical equations, initial conditions, fixed parameters and precision settings from the existing builders. No scalar or cumulative integral replacement is authorized here; treatment is 00.

DATA: each arm's native common-TT Planck support reduced to ell <= 599 in FULL, plus ACT DR6 primary, ACT DR6 lensing, DESI DR2 and the same frozen PantheonPlus likelihood. Original likelihood/nuisance/priors and reduced covariance semantics are retained. No cross-arm absolute objective inference is performed.

POINTS: both arms × both models, FULL, original production start index 0. The exact existing start implementation includes 5%-interior clipping of uniform-prior coordinates. The resulting full vector is retained and evaluated; it is not overwritten by raw parents, randomized, refitted or represented as a minimum.

SOLVER: restored unchanged CLASS EDE at commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`, required documented diagnostic binary SHA256 `df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf`. Loaded binary routing is checked after model initialization. Equivalence to the original campaign binary beyond the documented diagnostic pin is not assumed.

SOFTWARE: Python 3.11.16; Cobaya 3.5.6; NumPy 1.26.4; SciPy 1.15.3; PyYAML 6.0.2; Py-BOBYQA 1.5.0; GetDist 1.6.1; Cython 0.29.37; SACC 1.0.2; Astropy 7.2.2; build backend Flit Core 3.12.0 (new technical dependency). Pinned HiLLiPoP/ACT Python interfaces and the established DESI definition/pandas compatibility backport are restored. There is no CLASS compilation, PolyChord run, sampler or optimizer.

LIKELIHOOD OUTPUT: per-component log likelihood and its sum are distinct from log priors and log posterior. Native raw spectra retain C_ell units muK² without the ell factor. Full sampled vector and effective CLASS inputs are preserved.

## K–L. Program and launcher

PROGRAM_ID: `Q045-BASELINE-V2`.

LAUNCHER: 🚀 BUBBLEVERSE START.

LAUNCHER FILE: `.github/workflows/00-bubbleverse-start.yml` — unchanged.

REGISTRY: `bubbleverse_program_registry.json`.

TARGET: `.github/workflows/q045-native-baseline-v2.yml`.

PROGRAM_ID REGISTERED: YES in the delivered local registry; NO remote installation performed. The prepared registry retires Q045 V1 as SUPERSEDED and adds the V2 repair target. Q042 V29 remains COMPLETED. Unrelated entries remain unchanged. Execution registration is not canonical scientific acceptance or model promotion.

LAUNCHER_GATE: local package validation PASS; remote runtime pending.

## M–O. Runtime, jobs and finite result tests

Measured runtime: NOT AVAILABLE for these four points. Do not interpret caps as estimates.

GitHub-hosted job execution hard limit checked on 2026-10-10: 6 hours, official `https://docs.github.com/en/actions/reference/limits`. The package uses much shorter fixed bounds.

Seven jobs: one static check (5 min), one original-input acquisition (20 min), four independent native workers (80 min each; at most four in parallel), one collector (10 min). Numerical workers cap the native subprocess at 20 min, reserve 10 min for cache restore, 25 min for interface restoration, and leave time for transfer/reporting. No new cache is saved. Exact-cache miss is a controlled blocker. Upper allocated job-time sum is 355 min; it is not measured CPU consumption or predicted elapsed time.

Single-job risk: UNKNOWN runtime before measurement, bounded by the finite caps. Strategy: parallel independent fixed points, fail-fast false. Checkpoint/resume: NO; each point is atomic and state sharing would obscure failures. Merge: YES, four compatible records. Test jobs: static plus tests within each worker and collector; no long validation run.

Mandatory tests:

| ID | Test | Failure effect |
|---|---|---|
| T001 | Q, package hashes, journal, registry, safe launcher target and README | Do not acquire inputs or evaluate |
| T002 | Original artifact/files, parents, supports, source/versions, Flit backend capability and actual CLASS backend identity | Record blocker, preserve provenance |
| T003 | One finite native likelihood at each unchanged FULL start | Preserve native failure; no repair/retry |
| T004 | Finite complete background/total-x_e thermodynamics and TT/TE/EE exports with declared units | Baseline incomplete |
| T005 | Exactly four workers, compatible Q/run/config/binary/external data and output hashes | Merge fails; successful independent artifacts remain |

Offline synthetic integrity tests validate file/control logic only. Runtime/physical tests are not claimed executed locally. In particular total x_e is not a separately qualified H/He history, finite native output is not a convergence proof, and common cached hashes are not a complete independent historical data qualification.

## P–R. File decisions and exact installation

All files are individual deliverables; no archive.

| Delivered file | Repository destination | Action |
|---|---|---|
| `q045_native_baseline_v2.py` | root | CREATE |
| `q045_native_baseline_tests_v2.py` | root | CREATE |
| `q045_native_baseline_contract_v2.json` | root | CREATE |
| `q045_native_baseline_manifest_v2.json` | root | CREATE |
| `q045_native_baseline_requirements_v2.txt` | root | CREATE |
| `q045_setup_baseline_v2.sh` | root | CREATE |
| `q045-native-baseline-v2.yml` | `.github/workflows/` | CREATE |
| `bubbleverse_program_registry.json` | root | UPDATE |
| `README.md` | root | UPDATE |
| `Q045_SAMLET_JOURNAL.md` | root, canonical current journal for this package | authoritative journal update |
| `Q045_EXECUTION_HANDOFF.md` | root | UPDATE, next-task instructions only |

README update is differential: the current Q045 section names V2 and records V1's pre-evaluation environment failure; the rest of the repository introduction/history remains. README_GATE and REPOSITORY_CONSISTENCY_GATE: local PASS; remote installation pending.

Upload all files before launching, with the YAML at its stated path. Existing frozen builders must remain byte-identical. The registry/README snapshots are based on the inspected main; preserve any later unrelated changes if main changes before installation. Hash guards reject an incomplete package. No user search through internal workflow names is necessary.

## S–U. Execution, outputs and gates

OPEN: 🚀 BUBBLEVERSE START.

PASTE: `Q045-BASELINE-V2`.

PRESS: Run workflow.

Expected raw outputs per worker: `attempt.json`, `native.log`, `sampled_vector.json`, `likelihood.json`, `spectra.tsv`, `thermodynamics.tsv`, `background.tsv`, `product_manifest.json`, `runtime_input_manifest.json`, `q045_worker_result_v2.json`. Failed preconditions may produce only the attempt/log and failure evidence; they cannot masquerade as complete scientific products.

Final output: `q045_native_baseline_final_v2.json`, contract, manifest, full authoritative journal and handoff. The final JSON retains expected/completed/failed/pending jobs, provenance and gates. Retrieve all four worker artifacts with the final artifact; source/input failures are in the input acquisition artifact.

`BASELINE_GATE=PASS_NATIVE_DIAGNOSTIC_ONLY` requires T001–T005. `FINAL_RESULT_GATE` remains `UNRESOLVED` even if they pass. Raw baseline products are `RAW_NOT_QUALIFIED`. No artifact means no calculation; missing jobs mean partial execution. There is no automatic retry, production restart or next-stage dispatch.

## V. Return to Bubbleverse

Return Q045's exact scientific question + `Q045_SAMLET_JOURNAL.md` + all existing source IDs and source locks + PROGRAM_ID + actual raw products + run/commit/config/binary/data provenance + T001–T005 status + unresolved issues to the **Result Ingestion & Routing Engine**.

Next action: ingest native success or the exact failed gate. If baselines succeed, assess independent history/reference qualification and actual decision margins before specifying the later scalar-only/cumulative-only/combined treatments. The mathematics handoff's maximum-52 factorial design remains a downstream proposal, not an execution authorized by this workflow. Do not infer posterior or optimized-minimum robustness from fixed-point output.

## W. Start this

START THIS: `Q045-BASELINE-V2`
