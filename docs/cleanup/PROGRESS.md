# Cleanup progress

Baseline checkout is isolated and original tracked files are clean.
Ruling: proceed autonomously under the supplied CLEAN specification; no approval/handoff pause is needed.
Ruling: source-locked scientific programs remain at their original paths; moving them requires changing their provenance contracts and validating historical production paths outside this cleanup scope.
Ruling: existing Q047 failures are baseline defects and are preserved, rather than repaired by changing scientific locks or statuses.
Baseline: 509 Python, 146 Bash, 519 JSON and 320 YAML syntax checks PASS.
Baseline: 68 tests, 64 PASS, three historical failures/errors and one missing-header SKIP.
Baseline: Q048 package/launcher PASS and twenty pinned metadata members replay PASS, final scientific gate UNRESOLVED.

Task 2: complete — 96 moves, 73 aliases, 39 question indexes, 1,015 launch records; twelve verifier tests RED then GREEN.
Task 3: runtime verification complete — same baseline issues; Q048 twenty-member replay identical except timing; six aliases identical; package and layout gates PASS. Installation/review pending.

Final review: fixed README context regression by preserving historical root text; actual reconstruction static command failed before fix and passes after. Fixed top-level executable launch exclusions; added RED-to-GREEN catalogue and documentation-lock tamper tests.

Task 3: complete — 13 installer checks PASS, including staged unrelated work preservation and complete reversal. Separate reviewer findings fixed with RED-to-GREEN controls. Result packaged locally; no integration/push/dispatch.
