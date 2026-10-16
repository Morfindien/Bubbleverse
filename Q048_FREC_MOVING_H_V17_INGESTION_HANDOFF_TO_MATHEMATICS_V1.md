# Q048 V17 ingestion — handoff to Matematikmotor 2.1.0

STATUS: CONTINUES  
CASE LIFECYCLE: ACTIVE  
SCIENTIFIC STATE: INCONCLUSIVE  
TARGET_Q: Q048 only  
PARENT RECEIPT: `LOCAL-Q048-FREC-MOVING-H-V17-INGESTION-RECEIPT-V1`  
NEXT ENGINE: `BUBBLEVERSE.MATHEMATICS 2.1.0`  
NEXT TASK: `LOCAL-Q048-POST-V17-MOVING-H-DOMAIN-1370-1360-MATH-V1`  
TASK FINGERPRINT: `879eda6fff356d392dd7271edf50c559158851c335a611d1854d9802aceef053`

## Objective

Construct and independently validate **one and only one** new connected moving-h proof-domain cell for Hillipop-EDE `1370→1360`, a=[1/1371,1/1361]. This is a mathematics-only task. Actual paired-frec state must remain **71 cells / frontier1370** during this run.

## Frozen identities and accepted parent

- Question SHA256 `c8d4ca366c84d235986b4413cbd436806be839198c4c6eaf85f8141ad3dc0436`
- CLASS/source commit `5a131c91d657dd9a7c6364cc45b038710f8d0d97`
- Capture SHA256 `2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b`
- Accepted V17 actual checkpoint `20eedde76e12d8337d2856264abb2a1c9de4d5e11930a697ed06d0080889c2ce`
- V17 raw `425508af979a82b04fac0b7d671a6be6fa594ebbe7421e98de49ccc77210999f`
- V17 validation `2d353393e1fffb3f0c5d64a025f1ffb8c98bdf34d008fcde0cb8435187c20327` — 90/90 PASS; 20/20 mutation rejections
- V17 post-accept validation `71024aae6a5424f4c03cf5648bb913a461062c1df4b6282f96a8e454288264a0` — 10/10 PASS
- V14 theorem result `7035c9b1b9646873a668c6e8a7cba56d62d944262a011ff8c69cc51e447ff578`
- V14 theorem validation `70d9d40d2accb9bb93f2874c3b8bbb9491d58ab9cd0d29c5ad26fdb2cd04ecb7`
- V14 proof contract `8f9102ef83dd4e7c7f903a7ef41c0a6fe83be65794a240f5caab7e2a24f8481d`
- Previous V16 cell raw `73763bb47f0fa39b908cc446ea69143d124d8efc100086cd5e3367e0e50e1bc0` / validation `e1d74abdd7a40b9bd4e80f8006de155bf1ee55085db8daf0cebbbc1d9e66ff91` / accepted math checkpoint `2b6f763f8f608b72e9a4aaee625eaad08ca7af0ca6724f4bb9fd49d1e75c03cc`

Accepted actual endpoint at a=1/1371: E=`82527736379536298057/500000000000000000`, Y=`66007103382050520379/500000000000000000`, Vbar=`1979034161157150451/62500000000000000`. Connected moving lower projection=`10774707685364977/1000000000000000000`. It is an auxiliary certified comparison projection, not a measured h/xe state and not permission to reset.

## V12 row8 binding

V12 raw `90c8d452e0a7e60e5ffea6dc40fe41570f1b3fa6ec195dc6495044f241bf21b5`. Primary row8 SHA `dc4ac3a9307655b19e6866df2de3db3a611d5ad125ac6b017069ee237977c2c1`; control row8 SHA `448b4c843f69190fe64371a032c8f189ccd372a4e3a6fc441937eab4fe53dc89`. Both are accepted+committed on a=[1/1371,1/1361].

Primary row8 exactly glues to V17:
- E_input_left=`82527736379536298057/500000000000000000`
- Y_left=`66007103382050520379/500000000000000000`
- V_previous=`1979034161157150451/62500000000000000`
- E_safe_left=`10266176903631569913/62500000000000000`
- V_admitted=`30901097706753907939/1000000000000000000`
- G_lower=`382587872658728587/40000000000000000`
- derivative_lower=`114486537095265838733/1000000000000000000`
- candidate scalar endpoint E_right=`8050821440704072213/50000000000000000`, Y_right=`12877180512007736641/100000000000000000`

The control row is a conservative aligned guard track only and must not replace the primary actual state.

## Required proof and anti-loop rule

Reuse the qualified Riccati theorem/method lineage, but **recompute a fresh row8/new-cell K and all source/rate/thermal domains**. Do not carry V16 K or V16 h_min into the new cell by assumption. Start comparison gluing from the accepted V17 lower projection, never from 1/2.

Success requires one linked, whole-cell, source-faithful proof-domain certificate for both q branches plus producer-free independent validation. Failure returns the first exact obstruction and preserves actual71/frontier1370. A failed sufficient inequality is method insufficiency unless separate evidence shows a physical contradiction.

Hard stop: one validated proof cell OR first exact obstruction OR 300 s aggregate new science. No actual consumer, no continuation below1360, no subdivision/tuning/method campaign, no refit/recapture/likelihood/native/P6/HPC/paid run, no Q049+. Return exactly once to Result Ingestion & Routing 2.1.0.

Machine task contract: `Q048_FREC_MOVING_H_V17_NEXT_MATHEMATICS_TASK_V1.json`.
