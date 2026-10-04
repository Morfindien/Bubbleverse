# Q042-STOCKDIAG-V21 — manual installation

All files belong in the repository root except the YAML workflow:

| File | Repository destination |
| --- | --- |
| q042_stock_diagnostic_v21.py | root |
| q042_stock_diagnostic_tests_v21.py | root |
| q042_stock_diagnostic_contract_v21.json | root |
| q042_install_stock_diagnostic_v21.py | root |
| q042_stock_diagnostic_install_v21.md | root |
| q042_execution_handoff_v21.md | root |
| q042_stock_diagnostic_manifest_v21.json | root |
| q042-stock-diagnostic-v21.yml | .github/workflows/q042-stock-diagnostic-v21.yml |
| bubbleverse_program_registry.json | replace the existing root file |
| README.md | replace the existing root file |

Use the exact filenames above, without download-added timestamps or numeric suffixes. Keep V20 historical files and the permanent launcher unchanged.

The supplied registry and README are prepared from commit `85518349123e012cce3f21f11800bd988ea5da42`. The registry adds V21 and changes only V20's status to BROKEN; other entries are preserved. README is updated differentially to describe the current diagnostic. If either live canonical file changed after that commit, apply the installer on the newer checkout instead of overwriting newer edits:

```bash
python q042_install_stock_diagnostic_v21.py
python q042_install_stock_diagnostic_v21.py --check
```

The helper never commits or starts workflows. If using the prepared canonical files, no local helper invocation is needed; the workflow performs `--check` before compute.

Commit all installation files, then start a new run on updated main:

**🚀 BUBBLEVERSE START → Q042-STOCKDIAG-V21 → Run workflow**

Do not re-run old V20 jobs: they use old code. V21 imports the completed CLASS artifact from V20 run 37195728280 after checking artifact ID, name, run, commit, SHA-256 and raw record hash. The original CLASS JSON and its V20 provenance remain unchanged. It is not recomputed.

Only one stock-resume probe runs, with the original 240-minute soft limit and 330-minute job timeout. No automatic continuation, production matrix, new BOBYQA starts or modified scientific settings are introduced. Archive files are used internally by GitHub's artifact transport; none are delivered for manual installation.

Return the final JSON and both diagnostic artifacts with the full handoff. A complete diagnostic still has scientific status UNRESOLVED. Missing mandatory products remain DIAGNOSTIC_INCOMPLETE.

START THIS: Q042-STOCKDIAG-V21
