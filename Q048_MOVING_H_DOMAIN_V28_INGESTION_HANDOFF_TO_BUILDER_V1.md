# Q048 V28 — til Execution/HPC Motor Builder 2.2.0

STATUS: CONTINUES. CASE: ACTIVE. SCIENTIFIC: INCONCLUSIVE. TARGET_Q: Q048 only.  
INGESTION_RECEIPT: `LOCAL-Q048-MOVING-H-DOMAIN-V28-INGESTION-RECEIPT-V1`.  
TASK: `LOCAL-Q048-POST-V28-MOVING-H-ACTUAL-CONSUMER-ONE-CELL-V1`.  
TASK_FINGERPRINT: `b3107127230c0962d1a4293c313c6f4b088a7ab9a0901c9b29999d0ec7243c11`.

**Udfør præcis én actual paired-frec consumer for Hillipop-EDE 1320→1310, a=[1/1321,1/1311].** Start fra accepteret V27 actual76/frontier1320. Brug den accepterede V28 proofcelle og V12 committed row13. Candidate77/frontier1310 må kun accepteres efter en separat producer-free consumer-verifier PASS.

V28 proof: raw `2447b554c7c68a94988c7dc5524eaf5418e09451e3db6c79e834eb7a2b7821b9`, validation `98af01e0b9966e3f52a375a0f3691f716903793bea99d161f088d9bd5013fd9e`, candidate `707f24df3fc36c3a5200ca9ebdfd553b6055b5319358f6f11e0fd59055df57ba`, accepted math checkpoint `405462169669a6f81440b934dc61cffa26ed3f27778a4a4c991e4f05b5cb648b`, transition `1a2f37b3ebdfaf8aa36aa9b262e56c5e323df79688ab9dd208cc373c072f3e3c`, postaccept `7c0993cff66c5930030c978e5698becb198a81883446003edf034dc04c9c72ec`, spec `e413848a72aed13e14374abb3bbffadf36cdb5da8e693813dab38db27ceab6d2`, contract `4026c200425f622d682dfbfaef701c65e14078188d2e5110e4a35acdede8b3c6`. K=`3027395738921693080237/500000000000000000`; whole-cell lower=`169519772393333/62500000000000000`; epsilon=`1/1000000`. Ingen reset til1/2 eller genbrug af V26 K/h_min.

Parent V27 actual checkpoint `a7f01cc307579d42268cdad82bd3857d73796b0fcfe46e821ef699b11ef8e0f4`; raw `e128b3ab5b0ad9e7ab1d861d35b0d3e35f45e3a2da07c128fc09f34c10516d38`; validation `0dbc7a848183d0cc24a4fcad14fdcd3d2da58c8281afeab787c3657553c6ba11`; postaccept `5b547abe533a8e0893019bfa9ba1f7fcaf69a1425688386c2bfc64b24141b1e3`. Actual scalar ved a=1/1321: E=`145558115152839369247/1000000000000000000`, Y=`23272834626295280593/200000000000000000`, Vbar=`13988763885236421343/500000000000000000`. Moving lower=`1550450091764323/500000000000000000`.

V12 row13 primary `c3fe09a8da35ebddf82e904a0d5a203d794fab908701b352efaa7a43764c5eb6` og control `d143be5b31a329597c6d10cf4761be49c0514f510bc43981ec8a9fcf29b6e4d0` er accepted+committed. Primary gluer eksakt til V27 actual. Control erstatter aldrig primary. Row13 candidate endpoint: E=`70932185071436793743/500000000000000000`, Y=`113399833034449708669/1000000000000000000`, Vbar=`27278514728906217199/1000000000000000000`.

SUCCESS: separat consumer + verifier accepterer begge q-grene på den V28-certificerede source/C/upper-h/thermal-domain, skriver én accepted actual checkpoint og opdaterer kun Hillipop-EDE 76→77/frontier1320→1310.  
FAILURE: stop ved første eksakte binding/admission/validation-obstruction og bevar76/1320.  
STOP: én valideret actualcell, første obstruction eller300s executed science. Ingen below1310, Math replay, guardregen, tuning/subdivision, native/P6, refit/recapture, HPC/paidrun, Q049+ eller modelpromotion. Returnér præcis én gang til Result Ingestion & Routing2.1.0.

Fuld taskkontrakt: `Q048_MOVING_H_DOMAIN_V28_NEXT_BUILDER_TASK_V1.json`.  
Fuld journal: `Q047_SAMLET_JOURNAL_MOVING_H_DOMAIN_V28_INGESTED_V1.md`.
