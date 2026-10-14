# Q048 MATH018 — frozen scaled-exp / interval contract V1

RESULT_ID: `LOCAL-Q048-MATH018-SCALED-EXP-INTERVAL-V1`
TASK_ID: `LOCAL-Q048-P3-SCALED-EXP-INTERVAL-ADMISSION-MATH-V1`

The method and acceptance criteria were frozen before scientific execution.

## Representation

Represent every positive small quantity as a pair `(M, e2)` meaning
`M / 2^p * 2^e2`, with outward integer rounding at fixed precision `p`.
The binary exponent is carried separately, so values far below `10^-120`
never round to zero merely because of absolute scale.

For the frozen first discriminator, use `e2 = -897`; the corresponding
mantissa is order unity. The input set is the union of the exact decimal token
`1.7280364e-270` and the exact rational value of its binary64 parse.

## Log enclosure

Normalize a positive rational `q = m 2^e`, `1 <= m < 2`, and use

`ln(m) = 2 sum_{j>=0} y^(2j+1)/(2j+1)`,  `y=(m-1)/(m+1)`.

All operations use outward fixed-point integer intervals. The omitted tail is
bounded by

`2 y^(2N+1) / ((2N+1)(1-y^2)) <= (9/4) y^(2N+1)/(2N+1)`

because `0 <= y <= 1/3`. `ln 2` is certified by the same identity at `y=1/3`.
The final union-log interval is deliberately widened by `2^-180` on each side,
providing a predeclared strict inverse-control margin.

## Primary exp enclosure

Use the exact decomposition

`exp(x) = 2^-897 exp(r)`,  `r = x + 897 ln 2`,

and certify `0 < r < ln 2`. Evaluate positive `exp(r)` with a directed Taylor
sum. For truncation after term `N`, with `r<1`, bound the tail by

`next_term * (N+2)/(N+1)`.

## Independent control

Use the same exact binary decomposition but independently evaluate
`exp(r/2^8)` with directed Taylor bounds and square the interval eight times.
This is a separate numerical proof path from the direct primary Taylor enclosure.

## Downstream contract

Products retain separate binary exponents and outward-round only order-unity
mantissas. Reciprocals use integer floor/ceiling division on the positive
mantissa and negate the exponent. Therefore no absolute sub-`10^-120` lattice
is introduced downstream.

## Frozen acceptance

1. Primary and independent-control exp lower bounds are strictly positive.
2. `exp_upper(log_lower) < R_lower` for the exact decimal/binary64 union.
3. `exp_lower(log_upper) > R_upper` for that union.
4. The independent path proves the same two strict inequalities.
5. Multiplication by positive unit preserves strict positivity.
6. Reciprocal arithmetic is finite/positive and reciprocal-roundtrip encloses the original interval.

Stop on subcomponent success or the first material failed inequality. Success is
only an arithmetic admission component; it is not full P3 PASS and does not answer Q048.
