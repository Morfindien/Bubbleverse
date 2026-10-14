# Q048 — H local event payload: bounded obstruction return

STATUS: PRIMARY_OBSTRUCTION / PARTIAL_THREE_CASE_CONDITIONAL_CERTIFICATE.
Q048 remains ACTIVE / UNRESOLVED. Q047 remains CLOSED INCONCLUSIVE. TARGET_Q=Q048.
Produced UTC: 2026-10-14T05:47:09.467315+00:00. Result ID: LOCAL-Q048-H-EVENT-PAYLOAD-CERTIFICATE-V1 (local provisional, unregistered).

The frozen method exports connected E1, strict interior E2, whole moving-bracket E3 and conservative linked event-state sets for camspec-lcdm, camspec-ede_n3 and hillipop-lcdm. The fourth case stops at SCALAR_CENTRAL_WELL_WALL_NOT_SEPARATED. This is a sufficient-method obstruction; it does not falsify the model or the existing all-four first-H-root theorem. A complete all-four payload is **not** obtained.

## Exact question and pins

For each of the four Q041 FULL/start0 configurations explicitly reconstructed in run 38140371059, what rigorously controlled bounds can be placed on the differences in the complete electron-fraction history x_e(z) and cumulative Thomson optical depth tau_T(z) between an event-resolved latch at q=xHeII=10^-6 and a reset to q=0 at the same first cutoff event, with identical captured effective inputs and fixed accepted z_reio?

QUESTION_SHA256: c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436. SOURCE_COMMIT: 5a131c91d657dd9a7c6364cc45b038710f8d0d97. CAPTURE_SHA256: 2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b.
The full incoming journal remains an unchanged byte tail of the updated journal. No Q049+ scientific integration, registry writeback, repository mutation, refit, P6 admission or paired-history execution occurs.

## New mathematical certificate and finite uncertainty

Let u=ln(a), s be the source helium Saha forcing, and r_s be its positive h=1 equilibrium, `(f-r_s)s=r_s(1+r_s)`. The frozen lower barrier is L=(51/50)r_s. Sixteen fixed rational-a cells certify inward lower-face slack

`rho*k_s_low*(1+r_s_lo)/(1+s_hi+2*r_s_hi) - K_upper*(rho-1)*(s_hi+1+(rho+1)*r_s_hi) > 0`,

with k_s=285325/T_gamma−3/2. This follows from D(L,h)>=−(rho−1)r_s[s+1+(rho+1)r_s] for h<=1 and the exact derivative of r_s. It uses the positive escape rewrite and the source upper K bound, not an assumption that F_q<0.

On the admitted moving tube `rho*r_s(a)<=q<=qmax` with the inherited thermal strip and common source-real background, D<=r_s(1−rho*h_min)<0. The retained uniform margin is `nu=K_lower*(rho*h_min−1)*r_s(a_plus)_lower>0`. The certificate covers the **whole calendar bracket tube**, including the portion below the old 0.99epsilon collar. It does not claim negative rate on a generic q=0 box.

`a_minus=(1/1946)*(1+1/1000000)` and `a_plus=(1/1601)*(1−1/1000000)`, strictly inside H mode. Their corresponding closed outer redshift enclosure is approximately [1600.001601001601, 1944.998054001946], with finite width about 344.996453. This is deliberately coarse; no precise point localization is claimed. E1 reuses MATH020's connected prefix through a=1/1946 plus a new tiny admitted left bridge. E2 reuses the first 15 immutable primary upper cells and recomputes only the shortened final cell. q_plus is the **ordinary unlatched auxiliary** value, never a native stopped phase sample.

| Configuration | q lower at a_minus | q upper at a_plus | nu lower per ln(a) | Product |
|---|---:|---:|---:|---|
| camspec-lcdm | 1.0841640471e-06 | 6.83554964909e-09 | 3.14177293183e-13 | E1/E2/E3 + outer state |
| camspec-ede_n3 | 1.08422022812e-06 | 2.19394345639e-07 | 2.40527422827e-13 | E1/E2/E3 + outer state |
| hillipop-lcdm | 1.08811222427e-06 | 7.32649146613e-09 | 3.15297061316e-13 | E1/E2/E3 + outer state |
| hillipop-ede_n3 | Not exported | Not exported | Not exported | Scalar wall gate fails |

All exact fractions, 48 serialized lag-cell witnesses, endpoint bounds, state widths and structural correlations are in the raw result. Each event set has q=epsilon exactly, inherited w in [-1e-6,0.01], coupled CLASS Saha h, T_b=(1-w)T0/a, T_gamma=T0/a and positive H. For the successful EDE case, scalar energy, central-well theta, phi and X bounds preserve the potential/energy/background equations. The finite component boxes are widened outer projections with the same-time/source constraints retained; they are not independent exact initial values or an ordinary numerical point restart. Initial-set linkage remains conditional source-real. Native P6 discrepancy/error is UNRESOLVED.

## First material obstruction

Case hillipop-ede_n3, stage event_state_scalar, theta wall=2.

- Source wall potential interval: [696.320960517, 696.320960517].
- Transported event-window energy upper bound: 818.962302959.
- Exact wall-minus-energy lower margin: -30660335610525242951804430893747034925587098540138914832397007259557358691164946484117786853292074898609000072334355946211/250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, approximately -122.641342442.

The frozen retained-wall criterion requires a positive margin; it fails. Periodicity means energy alone does not furnish a global phi bound. No widened wall, new root bracket, finer mesh, replacement initial point or alternative method is attempted after this gate. The fourth case's pre-state calculations are not serialized in the exception return and receive no exported E1/E2/E3 claim. Missing fields are not zero. The three successful certificates remain reusable.

## Execution and validation

Local exact-Fraction computation was chosen after early/late same-kernel pilots (~0.27 s/cell initially) and a complete-path estimate including validation, input recovery, checkpoints, delivery and review. The final bounded run took 16.189 s. No measurable Actions advantage was established; setup/queue/quotas/prices remain unmeasured, and no dummy workflow was created.

The finite checks return `PASS_BOUNDED_OBSTRUCTION_RETURN_WITH_THREE_PARTIAL_CERTIFICATES` with 632/632 passing. They bind raw hash cbe6bb0f61e3f6b7eb5dddc77ab0420a8197bbe0bc6d4f1e794a5bd56e10f563, reconstruct new arithmetic, reject 15 negative mutations, reject a false four-case completion, and supplement the rational proof with independent Decimal180 exp/equilibrium/scalar-wall diagnostics. Standard-library Decimal substitutes for unavailable mpmath; no package installation or source campaign occurs. The independent mathematical review is delivered separately.

One routine implementation failure preceded the accepted bounded run: the serializer passed an interval to a scalar-only cached background API. Its code and reproducer are preserved. The sole correction uses monotone endpoint bounds; no frozen scientific parameter or acceptance gate changes. This is an explicit implementation retry, not a rescue of a failed mathematical gate. Both the failed attempt and the corrected code are disclosed in provenance.

## Claim delta and route

New conditional claims: C01 connected strict-H E1/E2 for three serialized cases; C02 whole moving-bracket E3 for those cases; C03 finite coupled outer event states for those cases; C04 exact nonclosing fourth-case scalar-wall criterion. No empirical/model promotion, complete x_e/tau_T difference bound or all-four event-state admission follows.

Return exactly to **RESULT INGESTION & ROUTING ENGINE**. Ingestion should retain the partial certificates and obstruction, preserve the all-four MATH020 first-root theorem, and decide any next task. Do not dispatch full paired histories from this incomplete packet. Registered case ID/global ledger uniqueness/registry integration remain NOT_VERIFIED or NOT_PERFORMED.
