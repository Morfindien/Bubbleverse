# Q048 V100 — refined thermal candidate for 980→970

Status: **CANDIDATE PASS / NOT ACCEPTED**

Q048's original physical question and captured physics are unchanged. This is new proof machinery, not a repair or replay of V98.

The accepted parent remains V97: actual=110, frontier=980.

The historical thermal box `w ∈ [-1e-6, 0.01]` fails the upper thermal face at 980→970. The refined candidate uses `w ∈ [-1e-6, 0.01031]`.

This glues to the parent because the old parent domain is a subset of the refined domain; no new physical start state is assumed.

Exact minimum upper-face thresholds from the computed beta lower bounds:
- L: `100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000/9726438777464786593105358934318307845748374556514179382433883832873223866184227320969161471807888094498778109940026202733` ≈ 0.010281255276257
- R: `1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000/97069214251182180705966196352771278911313524164968788828982875514046693821285724061161981562959745426024447017942899372687` ≈ 0.010301927420699

At `w_hi = 0.01031`, all five composite gate conditions pass for both L and R in the new candidate calculation: both upper-H faces, positive thermal denominator, positive beta, and admitted thermal faces.

This does **not** create actual111 or frontier970. Independent verification/acceptance is required before state advancement.

Authoritative state remains: **actual110 / frontier980 / Q048 ACTIVE-INCONCLUSIVE**.
