# Q042-DURABLE-V22 — installation and one bounded diagnostic

CURRENT Q: Q-042. Scientific status: UNRESOLVED. This is a technical repair diagnosis.

## Place the files

Keep all supplied files at the repository root, including the workflow file initially. The installer places that file at `.github/workflows/q042-durable-v22.yml`. Alternatively put the workflow there directly; its filename and bytes must remain unchanged.

The repository must already contain the unchanged V21 helper `q042_stock_diagnostic_v21.py` (SHA256 `c7a253a8a8d9965e7f9857b9124674d5dfb23b56ea604916e2943f4d5d88dd10`), the current registry and README, and the permanent launcher `.github/workflows/00-bubbleverse-start.yml`. V18 and Q032 are checked out by the workflow at their frozen commits. No renamed `diagnostic_delivery` installation is required; that directory is created by checkout during execution.

From the repository root:

```bash
python q042_install_durable_v22.py
python q042_install_durable_v22.py --check
python -m unittest discover -s . -p 'q042_durable_tests_v22.py'
```

The helper makes a differential registry/README update and checks all package hashes. It performs no commit, push or dispatch. Apply it before starting the workflow. Upload/commit the resulting files yourself through your normal repository process. The prepared package has not been written to GitHub.

## Start once

**🚀 BUBBLEVERSE START → Q042-DURABLE-V22 → Run workflow**

The permanent launcher remains unchanged. V21 becomes SUPERSEDED as an executable target, retaining its successful diagnostic evidence. V20 remains historical broken execution evidence.

## Execution order

1. Static package, identity, registry, README and finite offline tests.
2. Restore the frozen V18 environment and verify hashed input artifact bytes and metadata.
3. Preserve a baseline library, apply the complete-state patch, rebuild and require compiled reference/interrupt tests. No scientific update cadence changes.
4. Only after all those pass: one isolated CamSpec/EDE/FULL diagnostic branch. First process explicitly imports lossy legacy state and waits at most 120 minutes for one new completed replacement. Stop it; validate and preserve its complete binary state. A second process restores that state and must publish further progress. Both processes share one 240-minute compute clock; they do not each receive four hours. Job timeout remains 330 minutes, with a remaining-budget gate before starting. V21's prior compute is retained in the accounting; original 48-segment limits are not reset.
5. Collect and stop. There is no automatic retry, next segment, 20-cell fan-out, BOBYQA start or CLASS replay.

## What the checkpoint does

An atomic `.durable_v22` file stores all 44 pinned RTI fields, including pending posterior stacks, exact covariance/cholesky and statistical state, plus Fortran RNG, local likelihood counters, failure counter and context hash. Publication occurs after the original complete serial loop iteration. Existing compression/covariance/clustering/posterior updates stay at their original boundaries. A `.tmp` file is never selected for continuation.

The scope is one serial rank on the same frozen binary/compiler ABI, with deterministic likelihood callbacks. It does not capture arbitrary Python/CLASS process memory. It does not promise power-loss/fsync durability. Stock `.resume` files remain present for Cobaya's resume discovery, but the full binary takes precedence in the sampler. Partial diagnostic text outputs are not validated posterior products.

The historical RNG and pending posterior stack absent from V18's stock checkpoint cannot be reconstructed. Its import is labelled a new diagnostic branch, never an exact reconstruction or authorized production result.

## Return these results

Return `q042-v22-<RUN_ID>-diagnostic-final` and `q042-v22-<RUN_ID>-durability-diagnostic`, along with `q042_execution_handoff_v22.md`, to Result Ingestion & Routing. Important individual outputs include:

- `q042_durable_final_v22.json`
- `q042_durable_pilot_v22.json`, first/second worker logs
- `checkpoint_context.json`, `first_checkpoint_lineage.json`
- `first_complete.durable_v22`, `second_complete.durable_v22`
- baseline/durable runtime records, patch manifest and compiled reference report

A failed gate produces an incomplete diagnostic; no automatic retry is allowed. A passing durability gate remains technical evidence. The preserved CLASS exception is still an independent production blocker, and Q-042's frozen posterior/convergence/overlap/LOO/classifier gates remain mandatory.
