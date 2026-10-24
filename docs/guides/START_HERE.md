# Bubbleverse technical entry guide

Repository: [Morfindien/Bubbleverse](https://github.com/Morfindien/Bubbleverse), inspected at `b99a5c78058b624c8d5847bed582df4ea816358a`. The scientific model repository is [Morfindien/bubbleverse-model](https://github.com/Morfindien/bubbleverse-model); it was not modified.

Read [START_CODES.md](../../START_CODES.md), [the directory map](../REPOSITORY_STRUCTURE.md), and [this cleanup report](../maintenance/cleanup/20261024-b99a5c7-v330/REPORT.md). The root [README](../../README.md) is preserved byte-for-byte because the passing V9 installed-package check requires its exact historical suffix. Its many old “current target” headings are historical context, not a reliable universal launch instruction.

## Scientific state and project memory

The authoritative scientific state belongs to journals and original result records. The existing [Motor 14 revision](../../revision.md), [handoff](../../handoff.md) and [memory update contract](../../github_memory_update.json) are retained at their actual installed paths. This cleanup does not reconcile scientific status or choose a journal by largest filename. Their intended `revisions/...` destinations are not silently installed over protected originals.

The [program registry](../../bubbleverse_program_registry.json) controls exact launch lookup, while the [permanent launcher](../../.github/workflows/00-bubbleverse-start.yml) rejects non-ACTIVE and unknown IDs. Existing registry flags can outlive scientific completion. Check the appropriate journal before any new launch; this package grants no production authorization.

## Environments and checks

There is no single installable Python package or root dependency manifest. Use each target workflow's exact Python/native environment, requirements, config, source locks and upstream artifacts; do not merge requirements or upgrade dependencies to run a historical case. This cleanup's tools require Python 3.12 standard library. YAML was inspected locally with PyYAML 6.0.3; the delivered integrity checker needs no third-party dependency.

From the repository root, run the verified local maintenance commands in START_CODES. `q048_inputcheck_tests_v1` uses isolated synthetic/control metadata; its PASS is not a scientific result. The current V9 package check passes; the old V1 package check already fails on its registry pin. No full scientific, native, checkpoint/resume or remote CI execution is claimed.

Outputs and resume paths remain in the original workflow/config contracts; all original code/config/result/checkpoint bytes and paths are preserved. Use isolated fixtures for tests. A missing original dataset, cache, external artifact or binary blocks that historical route; do not replace it with a newly generated equivalent.

## Contribution and corrections

Preserve old conclusions, source locks, failures and journals. Add separately versioned corrections or analyses with explicit provenance. Technical cleanup cannot accept a model or close a case. Website: [bubbleverse.dk](https://bubbleverse.dk). Contact and scientific philosophy remain in the original README.
