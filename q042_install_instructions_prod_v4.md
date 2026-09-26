# Q042-PROD-V4 — version-integrity technical repair

Q042-PROD-V3 did not reach scientific execution.

Observed V3 failure:
- `q042_production_v3.py static` passed.
- `q042_production_tests_v3.py static` failed because `WORKFLOW_COLLECTOR`
  still expected the V2 artifact name `q042-production-final-v2`.
- A complete V3 audit found additional recovery-owned V2 filename/stage
  expectations that could have caused a later merge failure.

V4 is therefore a technical version-integrity repair.

It changes no Q042 science:
- V1 scientific specification remains byte-identical.
- Same 20 cells.
- Same PolyChord settings.
- Same 20 PolyChord seeds.
- Same 80 V1 BOBYQA records; zero optimizer recomputation.
- Same finite 240-minute segment / 330-minute job / 48-segment policy.
- Same scientific merge/classification rules.
- Same fail-closed `UNRESOLVED` behavior.

V4 also preserves the V3 deployment fix:
- `import-bobyqa` installs pinned `PyYAML==6.0.2` and `numpy==1.26.4`
  before importing the production module.

V4 additionally enforces static regression gates against stale recovery-owned
V2 filenames.

Manual install only. The assistant did not upload, commit, rerun, or dispatch.

After adding the files:
1. Apply `q042_apply_registry_patch_prod_v4.py`.
2. Apply `q042_apply_readme_patch_v4.py` if README still needs synchronization.
3. Open `🚀 BUBBLEVERSE START`.
4. Paste `Q042-PROD-V4`.
5. Run workflow.

START THIS:
Q042-PROD-V4
