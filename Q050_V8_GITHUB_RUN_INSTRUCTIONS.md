# Q050 V8 --- GitHub Actions run files

Put these two files in the Bubbleverse repository:

-   `.github/workflows/q050-v8-pion-normal-certificate.yml`
-   `q050_v8_literal_normal_runner.py`

The workflow checks out the frozen `mwt5345/class_ede` commit and runs
the V8 fail-closed certificate gate.

IMPORTANT: the runner intentionally requires
`Q050_V8_LITERAL_NORMAL_CELLS.json` before it can issue a scientific
normal certificate. If that evaluator output is not yet present, the
GitHub run will still complete and upload a machine-readable result with
blocker `LITERAL_NORMAL_EVALUATOR_OUTPUT_MISSING`.

That is deliberate: it prevents the old Q048 convexified inclusion
machinery or point sampling from being mislabeled as a literal-selector
certificate.

Run: Actions -\> Q050 V8 --- Pion literal-selector normal certificate
-\> Run workflow

Download artifact: `Q050-V8-Pion-normal-certificate`

Return: `Q050_V8_PION_NORMAL_CERTIFICATE_EXECUTION_RESULT.json` to
Bubbleverse Mathematics 2.3.0.
