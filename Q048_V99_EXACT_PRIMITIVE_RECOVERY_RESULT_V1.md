# Q048 V99 exact primitive recovery result

Status: **PASS_EXACT_RECOVERY_AND_HYDROGEN_REGRESSION**.

The historical `q048_full_tube_reuse_v1.py` was recovered exactly: 10171 bytes, SHA256 `e975c73f7e767442cb0084c61791686061be6cd045378c8fbc48ba412bd454dc`. This is the V98-pinned historical dependency, not a reconstruction.

Recovered exact primitive bodies include `hydrogen_barrier_term()` and `thermal_certificate()`. The hydrogen formula was regression-checked against accepted V90 and V92 branch certificates: 8/8 interval-containment checks passed (L/R × two levels × two accepted cells).

For the frozen thermal face domain `w in [-1e-6, 1e-2]`, the exact historical face rule implies upper-face admission iff `(1+beta_lo)*0.01 - 1 > 0`, i.e. **beta_lo > 99**.

No Q048 scientific state is advanced by this recovery. Authoritative state remains actual110/frontier980. Next diagnostic target is exact evaluation of the V98 980→970 L branch and its five split predicates.
