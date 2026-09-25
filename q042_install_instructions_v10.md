# Q042-PREFLIGHT-V10 manual installation

Upload the V10 files individually to the Bubbleverse repository. Do not replace `.github/workflows/00-bubbleverse-start.yml`. Keep `q042_prepare_frozen_core_v4.sh` unchanged.

Place the workflow at `.github/workflows/q042-planck-portability-v10.yml`.

V10 is a technical gate repair only. It preserves the Q042 scientific contract, V7 PolyChord smoke budget, V9 stored-info resume path, all production settings, and Py-BOBYQA pilot settings (`max_evals=60`, `rhoend=0.1`, `best_of=1`, two external starts).

The repair accepts a bounded Py-BOBYQA raw result when the objective is finite and the raw exit flag is non-negative, including Exit flag 1 / MAXFUN, exactly as already preregistered. Negative flags, missing results and unrelated exceptions still fail.

Start manually with:

`PROGRAM_ID = Q042-PREFLIGHT-V10`
