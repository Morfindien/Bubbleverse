# Q048-GUARDCONT-V7 — installation

Prepared: 2026-10-12T21:58:34+02:00
Base repository commit: `2bc190aeb1a2659fbc9bc0d402159c7768c6b15a`
Current Q: `Q-048 — PROPOSED_UNVERIFIED`

This package is intentionally delivered as individual files, never an archive.

Journal preparation: `Q047_SAMLET_JOURNAL.md` prepends the V7 execution-design header and preserves the complete Math007 journal unchanged as its tail.

## 1. Put these files at repository root

- `q048_guard_continuation_v7.py`
- `q048_guard_runner_v7.py`
- `q048_guard_tests_v7.py`
- `q048_guard_config_v7.json`
- `q048_guard_package_check_v7.py`
- `q048_guard_package_v7.json`
- `q048_v7_repository_patch.py`
- `q048_v7_registry_entry.json`
- `README_Q048_V7_SECTION.md`
- `Q048_MATHEMATICS_007.md`
- `Q047_SAMLET_JOURNAL.md`

## 2. Workflow path

Place `q048-guard-continuation-v7.yml` at:

`.github/workflows/q048-guard-continuation-v7.yml`

Do **not** modify `.github/workflows/00-bubbleverse-start.yml`.

## 3. Differential repository metadata patch

Before committing the installation, run at repository root:

`python q048_v7_repository_patch.py`

It refuses to run unless the existing registry and README match the exact base Git blobs from `2bc190aeb1a2659fbc9bc0d402159c7768c6b15a`. It changes only:

- `Q048-STRUCTURAL-V6`: `ACTIVE -> SUPERSEDED`, adds `superseded_by=Q048-GUARDCONT-V7`
- adds registry entry `Q048-GUARDCONT-V7`
- prepends the exact V7 README section while retaining the complete prior README as historical context

If the base files have changed, **do not force the patch**; reconcile the newer repository first.

## 4. Validate before launch

Run:

`python q048_guard_package_check_v7.py`

Then the normal user flow is:

**OPEN 🚀 BUBBLEVERSE START → PASTE `Q048-GUARDCONT-V7` → Run workflow**

V7 stops after conditional H-entry at `z=2870` and returns once to Result Ingestion & Routing. It does not launch the later cutoff/full-history stage.
