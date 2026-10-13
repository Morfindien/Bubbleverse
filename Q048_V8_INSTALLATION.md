# Q048-PHASETURN-V8 — installation and launch

## Scientific identity

- CURRENT Q: `Q-048 — PROPOSED_UNVERIFIED`
- CASE: `NOT_ASSIGNED`
- PROGRAM_ID: `Q048-PHASETURN-V8`
- Frozen source: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`
- Parent numerical evidence: official V7 run `38348832247`
- Mathematics input: `I-PROPOSED-Q048-MATHEMATICS-008`
- Full-Q `FINAL_RESULT_GATE`: `UNRESOLVED` by construction.

## Why there is a one-time installer

At the inspected repository state, the permanent `🚀 BUBBLEVERSE START` launcher is correct and unchanged, but the canonical remote registry/README still predate the V7 installation. V7 was previously reconciled only in runner-local checkouts. V8 therefore ships a one-time fail-closed installer workflow rather than weakening or hard-coding the permanent launcher.

The installer accepts only the exact inspected registry/README base (or the exact already-installed V8 state). Its allowed repository mutation is limited to:

- `bubbleverse_program_registry.json`
- `README.md`

It installs the historical chain as:

`Q048-STRUCTURAL-V6` → SUPERSEDED by `Q048-GUARDCONT-V7` → SUPERSEDED by `Q048-PHASETURN-V8` (ACTIVE).

No scientific source, program, launcher, old result, or journal history is deleted.

## Upload paths

Upload every package file at the exact relative path supplied. In particular:

- `.github/workflows/q048-phase-turn-v8.yml`
- `.github/workflows/q048-install-phase-turn-v8.yml`
- all `q048_phase_turn_*_v8.*` files at repository root
- `q048_v8_repository_patch.py`
- `q048_v8_registry_entry.json`
- `README_Q048_V8_SECTION.md`
- `Q048_MATHEMATICS_008.md`
- `Q048_MATHEMATICS_008.json`
- updated `Q047_SAMLET_JOURNAL.md`

Do not rename the files.

## One-time installation

1. Open GitHub Actions.
2. Run **🔧 INSTALL Q048 PHASE-TURN V8** once.
3. Require `INSTALL_DIFF_GATE=PASS` and `INSTALL_COMMIT_GATE=PASS` (or the corresponding `PASS_ALREADY_INSTALLED`).
4. The installer must show that only `README.md` and `bubbleverse_program_registry.json` changed.

If branch protection refuses the bot push, no science run has occurred. Apply the exact two generated registry/README changes through the repository's normal protected-branch process, then rerun the installer; it should return `PASS_ALREADY_INSTALLED`.

## Normal launch after installation

1. Open **🚀 BUBBLEVERSE START**.
2. Paste `Q048-PHASETURN-V8`.
3. Press **Run workflow**.

The launcher performs exact registry lookup. V6 and V7 are intentionally rejected as superseded Q048 execution targets after installation.

## Expected run structure

- `preflight`: downloads exact V7 parent, validates hashes/package/launcher/source and unit/adversarial tests.
- `camspec`: computes the bounded signed phase/first-turn proof and independently recomputes it once inside the worker.
- `collect`: requires exactly one valid Camspec worker report and returns `q048_phase_turn_final_v8.json`.

No MCMC, likelihood, native CLASS recapture, GPU, or HPC campaign is authorized.

## Scientific stop rule

V8 stops after either:

- conditional Camspec source guard through z=2870 + He1f/He2 continuation + H-entry q, or
- one precise bounded obstruction of the new phase/first-turn method.

It never automatically starts the shared `q=xHeII=10^-6` cutoff or complete latch/reset `x_e(z)` / `tau_T(z)` histories.
