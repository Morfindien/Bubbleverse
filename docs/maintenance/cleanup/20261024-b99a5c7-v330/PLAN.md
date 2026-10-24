# Bubbleverse technical cleanup implementation plan

Goal: deliver a BASE_SHA-bound, locally verified cleanup without changing scientific records or working historical gates.

Spec: operator-supplied BV-REPOSITORY-CLEANUP v3.3.0; source prompt is hashed in RUN_MANIFEST.json.

Architecture: preserve historical root paths, physically organize eligible maintenance material, add navigation and a read-only integrity checker. No scientific execution, dependency upgrade, remote write or workflow dispatch.

## Global constraints

- Repository: Morfindien/Bubbleverse, main@b99a5c78058b624c8d5847bed582df4ea816358a.
- TARGET_Q=UNSET; technical inspection only; scientific state is not inferred from filenames.
- Keep every scientific source, journal, manifest, result, input and checkpoint unchanged.
- Existing V9 package check passes and pins the whole README: preserve README bytes and explain the blocked upgrade.
- Frozen prompts remain protected; completion does not by itself establish retirement.
- No production compute or remote mutation. Verification budget: bounded local syntax, integrity, resolver, fixture and package checks; no full scientific suite.

## Review focus

1. Protected missing/changed files must fail the integrity checker.
2. Path traversal and symlink escapes must be rejected.
3. Every baseline file needs one placement decision; duplicated IDs must fail.
4. Reapplication must stop clearly; inverse patch must restore exactly the scoped paths.
5. Existing baseline failures must not be relabeled as cleanup regressions or successes.

## Tasks

- [x] Capture repository identity, baseline gates, capabilities, source hashes and authorization.
- [x] Scan every tracked file for byte identity, purpose, references and entry points; record uncertain dependencies explicitly.
- [x] Move only eligible maintenance payloads after dependency/collision checks; retain all uncertain historical paths.
- [x] Add START_CODES.md, docs/guides/START_HERE.md, docs/REPOSITORY_STRUCTURE.md and case navigation; reuse cleanup-installation/.
- [x] Add read-only integrity checker and focused adversarial fixtures, schemas and complete per-file records.
- [x] Rerun affected checks; compare unchanged syntax failures; test exact-base patch and inverse in isolated clean snapshots.
- [x] Freeze delivery hashes, complete report/limitations, link the maintenance index and provide installation artifacts.

Ruling: README upgrade is deferred because q048_threshold_anchor_package_check_v9.py verifies its full historical suffix. Changing a passing check or its frozen package lock is outside this cleanup. A new guide is the safe independent batch.

Ruling: no global unittest discovery because historical tests may launch scientific/native work. The operator requires bounded affected checks and forbids rerunning retired/completed campaigns.

Final rulings: README contract migration and retirement qualification remain deferred. Every substantive independent review finding was addressed by focused fixture/static checks. Final patch application/recovery evidence is external to avoid a self-hashing patch.
