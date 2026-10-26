# Q052 native pair V1 — README addition

Add this section to the current repository README after installing the files.

## Q052-NATIVEPAIR-V1

Q052 performs one `hillipop-ede_n3` native paired realization from an explicit
`z=810` intervention boundary. The pinned original CLASS/HyRec source and
`classy.so` are reused. The wrapper does not copy hydrogen-rate physics: it
keeps the original NDF15 evolution and source functions, freezes residual
helium after the shared z=810 state, and compares only `q=xHeII=1e-6` with
`q=0`. Reionization uses the previously accepted fixed `z_reio`; tau shooting
is forbidden.

Install `q052_native_pair_v1.py`, `q052_native_pair_v1.c`,
`q052_native_pair_tests_v1.py`, `Q052_NATIVEPAIR_CONTRACT_V1.json` and the
add-only registry entry. Put `q052-native-pair-v1.yml` at
`.github/workflows/q052-native-pair-v1.yml`. Do not replace
`.github/workflows/00-bubbleverse-start.yml`.

After installation and static validation, start only:

`Q052-NATIVEPAIR-V1`

The final artifact is `Q052_NATIVEPAIR_RESULT_V1.json`. Two-level refinement
is explicitly a numerical diagnostic, not by itself a rigorous truncation-error
theorem. If that remains the only error evidence, Q052 returns the exact
remaining certification blocker instead of claiming a final scientific PASS.
