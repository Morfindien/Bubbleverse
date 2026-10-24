# Installation and scoped recovery

Target: **Morfindien/Bubbleverse**. Required source commit: `b99a5c78058b624c8d5847bed582df4ea816358a`. Default branch observed: `main`. Result state: INSTALLATION_PACKAGE_READY; no remote repository was updated.

Use `Bubbleverse_cleanup_b99a5c7.patch` and its SHA-256 file from the delivery. The ZIP contains every changed/new file at its intended repository-relative path under `files/`, plus the patch and guides. **Apply the patch:** manually copying files would leave the old moved path behind. Do not apply the old `cleanup-installation/Bubbleverse_cleanup_24f380b.patch` or dispatch its old installer workflow.

## Exact safe application order

1. Keep the delivered patch outside the checkout. Verify it against the accompanying `.sha256` file. Review REPORT.md, the patch summary and the move manifest.
2. Work in a new isolated clone of `https://github.com/Morfindien/Bubbleverse.git`. Check out a new local branch starting exactly at `b99a5c78058b624c8d5847bed582df4ea816358a`. Confirm `git rev-parse HEAD` equals that SHA and `git remote get-url origin` identifies Morfindien/Bubbleverse. If the remote has advanced, use the exact source commit for review; do not reset or overwrite somebody else's newer work.
3. Require clean tracked worktree and index: `git diff --exit-code` and `git diff --cached --exit-code`. Preserve unrelated/untracked files. Git's check must reject unexpected destination collisions; never overwrite or resolve them by deleting unknown files.
4. Preview from repository root: `git apply --index --check /ABSOLUTE/PATH/Bubbleverse_cleanup_b99a5c7.patch`. This performs no mutation. Stop on any error or source/base mismatch; do not force it.
5. Apply: `git apply --index /ABSOLUTE/PATH/Bubbleverse_cleanup_b99a5c7.patch`. All intended changes are staged together. There is one rename, one original maintenance documentation update and the documented additions. Scientific originals, README, registry and active workflow bytes must remain unchanged.
6. Run the post-install checks below and review `git diff --cached --stat` and `git diff --cached --check`. Commit the reviewed local changes if desired. Publishing a branch, pushing, merging or dispatching jobs is a separate operator action; this package performs none.

## Exact post-install checks

Run from the repository root with Python 3.12 and Git available. No dependency installation is required by the cleanup checker.

```bash
python tools/maintenance/check_cleanup_integrity.py
python -m unittest discover -s tests/maintenance -v
python -m unittest -v q048_inputcheck_tests_v1
python q048_threshold_anchor_package_check_v9.py
git diff --cached --check
```

Expected: integrity/coverage/schema PASS; six maintenance fixtures PASS; nine metadata controls PASS; V9 package and installed-state verifier PASS. These are local technical checks, not scientific acceptance or a GitHub Actions run.

Known pre-existing failure: `python q048_package_check_v1.py` returns 2 and `PACKAGE_GATE=FAIL PACKAGE_FILE bubbleverse_program_registry.json`. This old frozen V1 package does not match the evolved registry; cleanup intentionally does not rewrite it. Do not treat that known failure as a newly passing gate.

Reapplication must stop clearly at Git's applicability check because the rename/source is already applied and added destinations exist. A second application must not add another tree or duplicate records. For confirmation of installed state, run the read-only integrity checker instead of forcing a second application.

## Recovery limited to this release

Before committing, with no later edits to the cleanup paths: preview `git apply --index --reverse --check /ABSOLUTE/PATH/Bubbleverse_cleanup_b99a5c7.patch`, then use the same command without `--check`. It reverses exactly this patch, restoring the root maintenance copy and placeholder install README and removing only this release's additions. It leaves unrelated files alone. If a touched file changed afterward, stop and reconcile that file; do not use a blanket reset or clean command.

After committing, prefer `git revert YOUR_CLEANUP_COMMIT` after checking its exact scoped diff. No untracked scientific data is backed up by Git or touched by this package. The final patch's clean apply, repeat refusal, unrelated-file preservation and inverse restoration are recorded in the external PACKAGE_VERIFICATION.json delivered beside it. This external verification record is not recursively included in the patch it hashes.
