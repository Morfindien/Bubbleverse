# Q042-PROD-V11 — mobile / no-HPC installation

Purpose: run Q-042 without a self-hosted/paid HPC and without a local PC. Compute is performed by ordinary GitHub-hosted `ubuntu-24.04` Actions runners.

## What V11 changes

- Keeps `q042_production_spec_v1.json` byte-identical.
- Keeps the V10 serial partial-initialization PolyChord checkpoint algorithm byte-identical.
- Uses `--mpi-ranks 1`; no `q042-hpc` runner label is used.
- Repairs the V10 deployment defect: the workflow called a `runtime-adapter` test subcommand that the delivered V10 test parser did not implement.
- Uses new V11 identities/artifacts so V10 remains auditable rather than silently overwritten.

## Upload from a phone

Copy the files from this package into the repository, preserving the `.github/workflows/q042-production-v11.yml` path. Do not replace the frozen V1 scientific spec or V1 source lock.

Apply the registry patch and README patch through your normal repository workflow if those files are used by the canonical launcher.

## Start manually from GitHub

1. Open **Actions**.
2. Select **Bubbleverse Q042 Production V11 — bounded technical recovery**.
3. Tap **Run workflow**.
4. `program_id`: `Q042-PROD-V11`
5. `mode`: `bootstrap`
6. Leave the remaining fields at their defaults.

The phone does not need to stay open after dispatch. GitHub Actions owns the compute. The real canary and a separate resume probe must pass before the other 19 PolyChord cells fan out.

## Expected execution model

- Standard GitHub-hosted Ubuntu runner only.
- Serial PolyChord (`mpi-ranks=1`).
- 240-minute production segments with checkpoint/resume.
- Up to the frozen 48-segment per-cell limit from the V1 preregistered orchestration contract.
- Existing verified V1 BOBYQA records are imported rather than recomputed.

## Fail-closed rule

If the partial-initialization checkpoint reproducibility self-test, runtime adapter test, canary, or resume-progress gate fails, do not interpret the run as a scientific Q42 result. Fix the technical failure under a new recovery version.
