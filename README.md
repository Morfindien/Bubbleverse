# CASE-Q013 — Gate-P Boundary Validation

This package adds a separate GitHub Actions diagnostic workflow for CASE-Q013. It does **not** modify HYP-004C and does **not** issue a physical Gate-P verdict.

## What it tests

1. Repeats the known-working 2ax physical boundary `f1=f2=0` at three `(a_c1,a_c2)` choices.
2. Reproduces the old 1ax direct `fraction_maxion_ac=0` crash and captures Python faulthandler plus GDB backtrace.
3. Tests 1ax with **physical** `f=0` while only the solver-facing value is regularized to `1e-12`, at three `a_c` choices.
4. Tests physical `f=1e-8` through the same mapping.
5. Reproduces the standalone `N_mscf=0` + shooting failure.
6. Runs plain LambdaCDM using the same frozen mAxiCLASS commit but without MSCF shooting, only to isolate the configuration failure.
7. Rejects NaN/inf/missing likelihoods.
8. Compares valid zero-boundary effective chi2 values with R1 = `317.4238643933`, tolerance `0.1`.

## Frozen chain

- mAxiCLASS: `b5a3af9818d04d2fe696e54972545e8c6805f4ea`
- ACT DR6 lite: `0e0cd2c703c62a0e980470b572602233b27750e1`
- SPT data: `2cec6e762a8c540484dd5acafc529f0035856350`
- `candl-like==2.0.3`
- `cobaya==3.6.2`
- ACT DR6 TT/TE/EE ell 600..8500 + SPT-3G D1 TT/TE/EE + tau information.
- No ACT/SPT lensing likelihood.

## Setup

Copy these items into the root of the existing Bubbleverse GitHub repository:

- `.github/workflows/gatep-boundary-validation.yml`
- `scripts/gatep_boundary_validation.py`
- `requirements-boundary-validation.txt`

Commit them to the default branch. Then open **Actions** -> **Bubbleverse Gate P - BOUNDARY VALIDATION** -> **Run workflow**.

No GitHub secrets are required.

The workflow clones and pins the three frozen external repositories, builds mAxiCLASS, installs the frozen Python environment and ACT likelihood data, runs the diagnostic, and uploads:

`gatep-boundary-validation-<RUN_ID>`

A green workflow means the **diagnostic completed**. It does not mean Gate P passed. Use `BOUNDARY_VALIDATION_RESULT.json` and `BOUNDARY_VALIDATION_REPORT.md` for the technical result.

## Routing afterward

If `technical_status` is `BOUNDARY_VALIDATED`, send the artifact through the Bubbleverse Result Ingestion engine. The next numerical task is to return to Gate-P globality recovery and re-minimize 1ax from the validated zero boundary.

If the status is `NEEDS_TECHNICAL_DEBUGGING`, feed the same artifact back into Technical Debugging. The artifact contains the faulthandler/GDB logs.
