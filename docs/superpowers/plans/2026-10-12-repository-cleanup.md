# Repository Cleanup Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve navigation and launch documentation without changing scientific programs or their contracts.

**Architecture:** Archive byte-identical downloaded copies and unused installation notes, preserving root executable aliases as relative links to unchanged canonical root programs. Keep the source-locked runtime layout at the root and add question indexes instead of silently invalidating locks.

**Tech Stack:** Git, Python 3.12, Bash, PyYAML for authoring only.

**Spec:** [cleanup specification](../../cleanup/CLEANUP_SPEC.md)

## Global Constraints

- TARGET_REPO = Morfindien/Bubbleverse; BASE_SHA = 24f380ba4bc0129ac3bfcd1dcb105c597191b47a.
- Preserve numerical code, inputs, journals, results, registry, workflows and campaign paths.
- Local work and installation package only; no push, dispatch, merge or production jobs.
- README.md and START_CODES.md remain at the root; documentation is English.
- Keep the original README and Q048 package lock and explicitly rebind only its README hash.

## Review Focus

- Executable aliases must resolve to the original canonical root code, preserving __file__ root discovery.
- Archive copies must match their original bytes and mode.
- All original entry points need a launch record or explicit exclusion.
- Historical failures and missing native headers must stay visible.
- A patch must apply exactly to BASE_SHA, reject collisions and reverse only cleanup changes.

### Task 1: Baseline and relocation map

- [x] Acquire isolated checkout at BASE_SHA and inspect tracked tree/instructions.
- [x] Record byte hashes, modes, references, duplicate groups and baseline checks.
- [x] Finalize explicit map; defer unresolved dependencies and source-locked paths.

### Task 2: Layout, README and complete launch registry

- [x] Archive selected files with git mv; keep executable aliases to unchanged canonical sources.
- [x] Create question indexes and START_CODES.md with concrete commands, CLI schemas and workflow inputs.
- [x] Preserve original documentation/lock; rewrite README and update README hash only.
- [x] Add tools/check_repository_layout.py with tests/test_repository_layout.py.
- [x] First run `python -m unittest discover -s tests -v` before implementation; expect missing verifier failure.
- [x] Verify positive layout plus tampering, traversal and coverage failures using isolated fixtures.

### Task 3: Verification and installation

- [x] Repeat full static checks and the 68 existing Q047/Q048 tests; expect the same three historical issues and one missing-header skip.
- [x] Replay all twenty pinned Q048 metadata members before/after; compare result content except timestamps/timing.
- [x] Check Q048 package, launcher resolution, permissions, links and preserved hashes.
- [x] Commit local result; generate binary-capable patch and complete changed/new files.
- [x] Apply, repeated-apply rejection and reverse-check on a clean BASE_SHA checkout.
- [x] Publish installation guide and full verification report with exact unresolved scope.
