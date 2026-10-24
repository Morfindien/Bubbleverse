# Q050 V8 GitHub Action package

Place exactly these three files in the Bubbleverse repository:

1.  `.github/workflows/q050-v8-execute.yml`
2.  `q050_v8_execute.py`
3.  `q050_v8_verify.py`

Then run **Actions → Q050 V8 --- execute and return result → Run
workflow**.

The run always uploads `Q050-V8-RESULT` and prints
`Q050_V8_PION_NORMAL_CERTIFICATE_EXECUTION_RESULT.json` directly in the
Actions log.

This package does not alter historical Q048 files or the pinned
`class_ede` checkout.

Important scientific gate: a VALIDATED normal certificate is accepted
only when the repository contains the actual versioned
`q050_v8_literal_normal_evaluator.py` and that evaluator supplies
complete coverage and both q branches. The wrapper will not relabel
Q048's convexified continuation or a sampling-only calculation as the
Q050 theorem.
