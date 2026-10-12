# Installation and recovery

Keep `install_cleanup.sh`, `Bubbleverse_cleanup_24f380b.patch` and `Bubbleverse_cleanup_24f380b.patch.sha256` together outside a Linux Git checkout of Morfindien/Bubbleverse.

```bash
bash install_cleanup.sh --root /absolute/path/to/Bubbleverse --dry-run
bash install_cleanup.sh --root /absolute/path/to/Bubbleverse --apply
```

Preview is the default. The installer checks origin, exact BASE_SHA `24f380ba4bc0129ac3bfcd1dcb105c597191b47a`, patch checksum and affected paths with git apply --index --check. It rejects unexpected collisions/affected edits and preserves unrelated work. If the repository has advanced, rebase/review this change against the new snapshot; do not reset newer scientific work to install it. Linux symlink support is required.

After installing, from repository root:

```bash
python tools/check_repository_layout.py
python -m unittest discover -s tests -v
python -m unittest -v q048_inputcheck_tests_v1
python q048_package_check_v1.py
```

Review staged changes before committing. No push, merge or workflow dispatch is part of installation. The broader historical tests retain the exact three existing issues in VERIFICATION.md.

Before committing, recovery is:

```bash
bash install_cleanup.sh --root /absolute/path/to/Bubbleverse --reverse --dry-run
bash install_cleanup.sh --root /absolute/path/to/Bubbleverse --reverse --apply
```

Reverse checks identity and applicability first and changes only cleanup paths. After a cleanup commit, use a reviewed git revert of that cleanup commit, resolving later overlapping edits deliberately. Never use whole-tree reset or git clean for this recovery.

The complete changed/new file tree is supplied for inspection. The patch is authoritative for moves, deletions, symlinks and modes. Installer testing includes a clean BASE_SHA application, repeated-application detection, reverse application, mismatch/collision rejection and preservation of unrelated staged work.
