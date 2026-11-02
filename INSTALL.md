# Install the scoped Bubbleverse cleanup

Repository: `Morfindien/Bubbleverse`. Exact source commit: `f689c9ca4a4917909104ea34b0428f46059e4c07`.

This is a local installation package; no remote changes have been made. The patch archives seven retired workflow definitions, retains scientific payloads and adds launch/navigation/maintenance records. It does not run a scientific campaign. Do not use any pre-existing cleanup apply workflow as a substitute for applying this exact patch.

1. Use a clean checkout with `git rev-parse HEAD` exactly `f689c9ca4a4917909104ea34b0428f46059e4c07`. Preserve user changes elsewhere. Stop on any different commit or conflicting file; do not force application.
2. From that repository root, run `git apply --check /absolute/path/to/cleanup.patch`, then `git apply /absolute/path/to/cleanup.patch`.
3. Run `git diff --check`; inspect `git diff --stat` and this run’s REPORT/VALIDATION_RESULTS. Verify payload SHA256 values in DELIVERY_MANIFEST.json. GitHub workflow execution is NOT_RUN.
4. New files and existing-file replacements are all supplied under `files/` at their exact repository-relative destinations. Prefer the patch, since manual copies alone do not remove the seven old workflow paths. Do not overwrite another version or mix application methods.

If installation fails preflight, nothing should be applied. After applying, scoped rollback requires `git apply --reverse --check /absolute/path/to/cleanup.patch` and then `git apply --reverse /absolute/path/to/cleanup.patch`; stop if later user edits conflict. Never use blanket reset/clean. Reapplication must fail preflight rather than make duplicate archives.

The pre-existing ACTIVE registry entry Q039-IMPLBLOCK-V1 points to an absent workflow. That blocker remains. Historical journal/notebook command extraction and whole retired-source bundle migration remain incomplete. This is CLEANUP_PARTIALLY_VERIFIED, not a scientific outcome. Remote publication/merge is a separate step.

Patch SHA256: `773f6cbc42922948dcfdbe3b445640775dcfc805a5ae5d729af33067551d3108`.
