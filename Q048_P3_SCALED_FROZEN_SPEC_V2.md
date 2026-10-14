# Q048 — P3 scaled-arithmetic operator-admission frozen specification V2

TASK_ID: `LOCAL-Q048-P3-SCALED-ARITHMETIC-FULL-OPERATOR-ADMISSION-BUILDER-V1`  
RESULT_ID: `LOCAL-Q048-BUILDER-P3-SCALED-OPERATOR-ADMISSION-V2`  
CANDIDATE_ID: `LOCAL-Q048-P3-ARITHMETIC-CANDIDATE-V2`  
CURRENT_Q / TARGET_Q: Q048 operational boundary; CASE_ID NOT_ASSIGNED.  
QUESTION_SHA256: `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`.  
FROZEN_UTC: 2026-10-14T02:15:00.470408+00:00  
FROZEN_EUROPE_COPENHAGEN: 2026-10-14T04:15:00.470408+02:00

## Immutable scientific scope

V1's P3 scientific domain, source interpretation, signed cubic interpolation,
endpoint stencils, four captured initialization bindings, Alpha/Alpha_eq/R operator
definitions and SWIFT `1+DK_K` denominator conditions are reused. Historical V1
failure remains immutable. This V2 is a new arithmetic candidate, not a rewrite.

No full rate IVP, common first event, complete histories, tau shooting, native P6,
accepted-model promotion or new-Q activation is authorized.

## Material change from V1

The absolute `10^-120` lattice is forbidden for positive small-rate arithmetic.

Each table token is interpreted as the union of:
1. its exact decimal rational value; and
2. the exact rational value of its Python/IEEE-754 binary64 parse.

For each positive token, V2 computes an outward log interval at **384 binary bits**:
`ln(m)=2 sum y^(2j+1)/(2j+1)`, `y=(m-1)/(m+1)`, 140 terms,
with the same rigorous geometric tail form as MATH018. The final table-token log
union is widened by a fixed, predeclared `2^-180` on both sides.

Primary exp uses dynamic binary range reduction at 384 bits and a 100-term directed
Taylor enclosure for a reduced argument with `|r| < ln(2)/2` (or a rigorously
verified neighboring reduction). Its scale is carried as an exact binary exponent.

Independent control uses 448-bit fixed-point arithmetic, eight halvings,
40 directed Taylor terms and eight squarings. It is evaluated independently at
the selected inverse controls and all global operator-bound endpoints.

Positive exp outputs are represented by significant dyadic intervals:
`mantissa / 2^p * 2^e2`. Product and reciprocal checks preserve the separate
binary exponent. No absolute sub-`10^-120` rounding is introduced.

## Mandatory execution

1. Hash-verify frozen P3 tables/config dependencies and MATH018 artifacts.
2. Recompute exactly **16,100** table-node log transforms:
   - 16,000 `Alpha_inf.dat`;
   - 100 `R_inf.dat`.
3. Serialize all 16,100 transformed log intervals before later admission checks.
4. Prove strict inverse-exp controls for the frozen R0 discriminator and a
   predeclared deterministic node-control set spanning both tables, including
   extrema and endpoints.
5. Reuse V1's exact signed-Lagrange/Bernstein norm proof and its separate
   interval-product control.
6. Recompute all seven global atomic log/rate operator ranges with dynamic
   scaled exp; require finite strictly positive lower bounds in both primary
   and independent exp controls.
7. Recompute source grid spacings and derivative bounds.
8. Recompute all four SWIFT fit cases; both primary and independent column-wise
   `1+DK_K` denominator lowers must be strictly positive.
9. Execute source lookup controls at the same frozen endpoint/interior tuples.
10. Stop on the first material unresolved inequality or input/provenance failure.

Proofcell plan remains V1's 30 cells. The 16,100 transforms are loader work and
are separately counted.

## Acceptance

PASS requires all bounded P3 V2 checks, serialized transforms, no absolute-lattice
fallback, proofcells exactly 30, and execution within 180 s / 512 proofcells.

A PASS is only **bounded conditional source-real P3 operator admission**.
It does not answer Q048 and does not qualify native P6, E1–E3 first-event logic,
full P4/post-frec state tubes, or complete `x_e(z)` / `tau_T(z)` bounds.

FAILURE is the first exact new material obstruction. Preserve every valid prior
branch and return once to Result Ingestion.
