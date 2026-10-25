# BUBBLEVERSE — Q050 PEEBLES T_RATIO TANGENCY CERTIFICATE

STATUS: OVERLEVERING
WORKFLOW_STATE: READY_FOR_RESULT_INGESTION
SCIENTIFIC_STATE: ACTIVE / INCONCLUSIVE at whole-Q level
TECHNICAL_STATE: PASS
TANGENCY_GATE: CLEARED
TASK_TYPE: SCIENTIFIC_CASE_EXECUTION
ENGINE: BUBBLEVERSE.EXECUTION_HPC_MOTOR_BUILDER 2.4.0
RUN_ID: LOCAL-Q050-PEEBLES-T_RATIO-TANGENCY-HPC-20261025-V1
TASK_ID: LOCAL-Q050-PEEBLES-T_RATIO-TANGENCY-CERTIFICATE-V1
PROGRAM_ID: Q050-PEEBLES-TANGENCY-CERT-V1-LOCAL-UNREGISTERED
UTC: 2026-10-25T05:04:46+00:00
EUROPE/COPENHAGEN: 2026-10-25T06:04:46+01:00
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1
CURRENT_Q=TARGET_Q=Q050
QUESTION_SHA256: 11af5cf58d6c94e34a050e9672a76e47d277c0fcaec14e9acbcf58e96eb22b01

EXACT QUESTION:
For the frozen hillipop-ede_n3 configuration and each fixed admitted common background on 0 <= z <= 810, do the exact source-real low-redshift hydrogen/temperature branch-selection rules admit an absolutely continuous continuation to z=0 from every state in the validated z=810 domain, separately for q=xHeII=10^-6 and q=0, without changing or convexifying the selector?

## EXECUTION PROFILE

Backend: **LOCAL_RUNTIME**.
GitHub Actions/HPC worthwhile: **NO**. The exact remaining gate reduced to a short analytic certificate plus deterministic scalar checks; remote execution would add orchestration without scientific information gain.
Paid compute: none.
GitHub workflow dispatch: none.
Producer runtime: 4.241618 s.
Independent validator runtime: 3.527862 s.

## DIRECT RESULT

**PASS — the PEEBLES `Tmat/Trad=0.1` exact-tangency gate is cleared for both q=10^-6 and q=0.**

At the literal switching surface let

`v = Tmat/Trad`, `A = rate_gamma_b/H`, `u = ln(a)`.

The frozen source gives

`v_u = A(1-v)-v`.

At `v=1/10`, tangency is exactly `A=1/9`. The source wrapper assigns equality `v<=1/10` to **PEEBLES**.

The decisive result is stronger than the requested disjunction: at **every admissible tangent state in the material strip**, the equality-assigned PEEBLES branch itself satisfies

`v_uu < -1/10`.

Therefore its classical branch solution departs quadratically into `v<1/10`, i.e. strictly into PEEBLES's own literal side. No convexification, selector modification or HMLA rescue is needed at the tangent.

## SOURCE-REAL PROOF

The photon-baryon coupling can be written

`A = R(z) * x/(1+fHe+x)`,

where `x=x_e` and `R(z)` contains only the photon density, Hubble background and pinned constants.

On the frozen positive flat background,

`H_CLASS >= H0*sqrt(Omega_g)*(1+z)^2`.

Using the pinned capture/constants on the full material tangent strip gives a direct upper bound `R<11524.501`; the proof intentionally rounds this outward to

`R < 11700`.

Tangency `A=1/9` then forces

`x/(1+fHe+x) > 1/(9*11700)`

and hence, even after dropping the positive `fHe` from the lower-bound algebra,

`x > 1/105299 ≈ 9.496766351e-6`.

For `q=10^-6`, `x=h+q`, so

`h > 894701/105299000000 ≈ 8.496766351e-6`

and

`x*h > 894701/11087879401000000 ≈ 8.06918e-11`.

For `q=0`, the product is larger.

The PEEBLES source term simplifies exactly to the sign bracket

`B = alphaB(Tm)*x*h - alphaB(Tr)*s*(1-h)`,

with `s` the ground-state Saha factor. At `v=0.1`, the pinned `alphaB_PPB(T)` is strictly decreasing, so `alphaB(Tm)>alphaB(Tr)>0`.

Across the material strip the Saha factor is increasing with z and reaches its maximum at `z=4006/49`. Direct high-precision evaluation gives an astronomically small value (~1.09e-284); the independent proof uses only the much weaker safe bound

`s < 1e-280`.

Thus `x*h > s` by more than 269 decimal orders even for q=10^-6. Therefore `B>0`. With positive finite Peebles C-factor and positive `nH/H`, and frozen `has_exotic_injection=0`,

`h_u < 0`.

The material strip lies above the frozen reionization start, so source-real `x_reio=x_noreio=h+q`, with q fixed. Hence

`x_u = h_u < 0`.

Now differentiate the coupling ratio:

`A_u/A = -4 - ell + (1+fHe)*x_u/[x(1+fHe+x)]`,

where `ell=d ln H/d ln a`. The inherited admitted common-background proof gives `ell>=-3`. Since the electron term is strictly negative,

`A_u/A < -1`.

At tangency `A=1/9`,

`A_u < -1/9`.

Finally, because `v_u=0` at the tangent,

`v_uu = (1-v)A_u = (9/10)A_u < -1/10`.

This is strict and uniform in both q branches.

## DOMAIN / SOURCE SAFETY

Material tangent strip:
`16.0310108356 < z <= 4006/49 ≈ 81.75510204081633`.

- It is above the fixed reionization start `753585/65536`, so reionization does not alter `x`.
- It is below the 1775 K SWIFT-fit region; the non-PEEBLES arm would be HMLA, but it is not needed for the existence certificate.
- The inherited source-real hydrogen domain has `h<=99999/100000`, so `1-h>=1e-5`; the PEEBLES Lyman-alpha denominator remains finite.
- All relevant source constants, H, nH and C-factor are positive on the admitted domain.
- No exotic injection and no varying constants are active in the frozen case.

## VALIDATION

Producer: `q050_peebles_tangency_certificate_v1.py`.
Independent validator: `q050_peebles_tangency_validator_v1.py`.

Validator result: **PASS**.
Checks: **8/8 PASS**.
Semantic mutations: **5/5 rejected**.

The validator deliberately uses coarse outward inequalities (`R<11700`, `s<1e-280`) rather than trusting the producer's high-precision transcendental values.

## SCIENTIFIC INTERPRETATION

This run **closes the exact higher-order PEEBLES tangency obligation** that Mathematics isolated.

It does **not** by itself close all of Q050. The required next action is a single Result Ingestion & Routing 2.3.0 completion audit: combine this newly cleared tangent gate with the already-cleared Pion literal-selector gate and SWIFT-time-boundary result, then decide whether any global extension/Zeno/domain-boundary obligation remains.

Do not rerun Pion, background binding, runtime recovery, native/P6 or the HMLA tangent derivative merely for reassurance.

## CLAIM FIREWALL

Not established here:
- selector uniqueness;
- existence of the common background itself;
- cosmological reachability of every theorem-domain point;
- native/P6 equivalence;
- a new physical trajectory;
- model confirmation/falsification;
- final Q050 closure.

## POINT / SOME STATUS

RUN COST: 170 pts
TOTAL WORK POINTS: 1590 pts
SOME INTERVAL: 1000 pts
CYCLE PROGRESS: 590/1000 pts
NEWLY CROSSED SOME MILESTONES: []
NEXT SOME MILESTONE: 2000 pts
POINTS TO NEXT SOME MILESTONE: 410 pts
SOME PACKAGE STATUS: READY — existing Q050-SOME-M001; no duplicate/regeneration
SCIENTIFIC STATUS: ACTIVE / INCONCLUSIVE pending ingestion completion audit
NEXT SCIENTIFIC ENGINE: BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0
EXTERNAL PUBLICATION: NOT_REQUESTED_NOT_POSTED

## REPOSITORY / PROVENANCE

Bubbleverse repository freshness at execution:
`Morfindien/Bubbleverse main@2bd8c5bb27cb3576c81508f58ba636521fbe0bb5`,
tree `0bb7681912071f40ddc1bb9f38bb7dcfb3b22043`, 4562 entries, nontruncated.
The complete incoming ingestion package and tangent task are present on current main.

Pinned scientific source:
`mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.

No GitHub write, PR, merge or workflow dispatch was performed by this run. New files are USER_UPLOAD_PENDING.

## RETURN

Return this result **once** to `BUBBLEVERSE.RESULT_INGESTION_ROUTING 2.3.0`.
