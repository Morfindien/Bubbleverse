# Q048 V99 full-tube reconstruction

This package starts a **fresh V99 implementation**. It is deliberately not labelled as the missing historical `q048_full_tube_reuse_v1.py`.

The V98 composite gate has been recovered exactly at the interface level and is split into five independently reported subpredicates. The accepted V90 verifier also preserves the two thermal face identities used to validate the thermal certificate.

The original numerical bodies of `hydrogen_barrier_term()` and `thermal_certificate()` are not present in the currently exposed repository bytes. They are therefore **not guessed** here. The reconstructed primitive module fails closed if either is called. This prevents a reconstructed file from silently becoming fake historical evidence.

Authoritative Q048 state remains **actual 110 / frontier 980 / INCONCLUSIVE**. Nothing in this package advances the proof frontier.

Next scientific step: derive the two numerical primitive bodies from preserved source/theorem lineage, regression-test them against accepted historical moving-H cells, and only then execute the V99 980→970 diagnostic to expose which L-branch subpredicate fails.
