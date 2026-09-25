# Q042-PREFLIGHT-V11 manual installation

Upload the V11 files individually to the Bubbleverse repository. Do not replace `.github/workflows/00-bubbleverse-start.yml`. Keep `q042_prepare_frozen_core_v4.sh` unchanged.

Place the workflow at `.github/workflows/q042-planck-portability-v11.yml`.

V11 is a technical workflow-bootstrap repair only. V10 failed in `merge-preflight` before merge logic because the fresh runner had no NumPy installation. V11 explicitly installs `PyYAML==6.0.2` and `numpy==1.26.4` in that job.

No scientific contract, observational data, priors, PolyChord pilot/production settings, Py-BOBYQA settings, thresholds, or classification rules are changed.

Do not dispatch through an automated write tool. Use the permanent Bubbleverse launcher manually with:

`PROGRAM_ID = Q042-PREFLIGHT-V11`
