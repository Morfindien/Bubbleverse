# Q048 V19 ingestion — handoff to Matematikmotor 2.1.0

STATUS: CONTINUES  
CASE LIFECYCLE: ACTIVE  
SCIENTIFIC STATE: INCONCLUSIVE  
TARGET_Q: Q048 only  
PARENT RECEIPT: `LOCAL-Q048-FREC-MOVING-H-V19-INGESTION-RECEIPT-V1`  
NEXT ENGINE: `BUBBLEVERSE.MATHEMATICS 2.1.0`  
NEXT TASK: `LOCAL-Q048-POST-V19-MOVING-H-DOMAIN-1360-1350-MATH-V1`  
TASK FINGERPRINT: `5394a556a629e04a29c751f796212bafb4925639501d2bea66841d9e267eec1c`

## Objective

Construct and independently validate **one and only one** connected moving-h proof-domain cell for Hillipop-EDE `1360→1350`, a=[1/1361,1/1351]. This is mathematics-only. Actual paired-frec state must remain **72 cells / frontier1360** during this run.

## Frozen identities and accepted parent

- Question SHA256 `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`
- CLASS/source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`
- Capture SHA256 `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`
- Accepted V19 actual checkpoint `747d1fe7c24b04a8ab6d1294654069ea3d38c5c4c7fcf120e091abe667ec9375`
- V19 raw `a275caaab5d3a4836c492fb05fb83fbdaf4838527123bbdcfebad5e1a9b219de`
- V19 validation `0a5acc693e9edebe4941aa0bfd1bba95f38e2435e5a8f84616dbcce24e19bff3` — 93/93 PASS; 20/20 mutation rejections
- V19 post-accept `d390880103701f6dea9c16bc64e959e53a454ad6f6e5a6b75257ffa6d01ffc60` — 10/10 PASS
- V18 previous proof raw `fcbe51cee49799c2126806a8e25776861ad1ff16cde7b6b93651a8930e522e64`; validation `e968009f0ad717f333821d1d0f08fcc1bb6744d76bb831cf040d3ed1ba12f88c`; accepted proof checkpoint `6bcf5e8d8e99f8cb1b05266dd55f2f977999a15d157e8d2212c5b72506d197cb`
- V12 guard raw `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`; validation `51e4dfd3ef7a429b459af73b125d251e789bb0ac9244ef7630d5a44d4d99b554`
- V12 row9 primary `6016663d0ae5b3ffe3b396637a2a6ff3b861ed2ee1cdca502ab98f07d6943086`; row9 control `ef8aae031066f1292f18d66239e363c09c4a34e2882ec0adf5db9415022ad69b`

Accepted parent at a=1/1361: E=`8050821440704072213/50000000000000000`, Y=`12877180512007736641/100000000000000000`, Vbar=`30901097706753907939/1000000000000000000`. Connected moving lower=`3621863154303919/500000000000000000`; this auxiliary proof projection is inherited and must **not** be reset to 1/2.

V12 primary row9 is accepted+committed and exactly glues E_input/Y/V_previous to that V19 actual scalar endpoint. The aligned control row is conservative guard evidence only; it must not replace the primary actual state.

## Required mathematics

Recompute a fresh K_upper for row9/new source-rate domain and prove a strictly positive connected whole-cell lower comparison across a=[1/1361,1/1351] for both q≤1e-6 branches. Rebind fresh source/C/upper-h/thermal obligations to this cell. Reuse the V14/V18 theorem lineage only; **do not reuse V18/V16/V14 cell-specific K or h_min**.

Acceptance requires an independently validated mathematical proof-domain cell linked to V19 and V12 row9. It does **not** advance actual coverage. Failure must return the first exact binding/domain/rate/source/C/upper-h/thermal/comparison obstruction; a failed sufficient bound is method insufficiency absent separate physical contradiction.

Hard stop: one validated proof-domain cell OR first exact obstruction OR 300 s. No actual consumer, no below1350 continuation, no refit/recapture/likelihood/native/P6/HPC/paid run, no Q049+. Return exactly once to Result Ingestion & Routing 2.1.0.

Machine task contract: `Q048_FREC_MOVING_H_V19_NEXT_MATHEMATICS_TASK_V1.json`.
