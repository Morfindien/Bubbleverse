# BUBBLEVERSE --- OVERLEVERING

PROMPT_ID: BUBBLEVERSE.MATHEMATICS PROMPT_VERSION: 2.3.0 TARGET_Q: Q050
CASE_ID: LOCAL-Q050-LOWZ-SELECTOR-EXISTENCE-V1 RUN_ID:
LOCAL-Q050-MATH-RATIO-CLEAR-PION-REDUCTION-V2 UTC:
2026-10-25T00:33:01.745606+00:00

WORKFLOW_STATE: READY_FOR_HANDOFF SCIENTIFIC_STATE: INCONCLUSIVE
TECHNICAL_STATE: PASS PUBLICATION_STATE: NOT_DUE

## Inputgrænse

Denne runde fortsætter udelukkende fra den gyldige Q050 RAW
V1-checkpointtilstand med TOTAL POINTS=95. Repo-filer fra det tidligere
kasserede Q050-forløb er ikke anvendt som evidens, resultat eller
pointkilde.

Pinned source: -
mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97 -
external/HyRec2020/hydrogen.c - source/thermodynamics.c / HyRec wrapper
call-chain - Bubbleverse frozen q048_prefix_config_v1.json at the valid
Q049/Q048 evidence boundary.

## Resultat A --- ratio-selectorens lokale normal-obstruktion ryddes

Den source-real outer selector bruger PEEBLES ved Tmat/Trad \<= 0.1.

For den frosne konfiguration er de relevante exotic/IDM thermal flags
nul. Hydrogenbranchens valg ændrer hydrogenkomponenten, men ved samme
state ændrer det ikke øjeblikkeligt den materietemperaturkomponent, som
bestemmer normalretningen til surface

g = Tmat/Trad - 0.1 = 0.

Dermed har de to hydrogen-selectorarme samme øjeblikkelige
normal-komponent til g=0 ved en fælles state. Den specifikke
V1-obstruktion "ukendt/modsat one-sided normalretning på ratiofladen"
består derfor ikke.

Dette er IKKE et globalt continuation theorem og beviser ikke
uniqueness.

RESULT_ID: LOCAL-Q050-RATIO-SURFACE-COMPATIBILITY-V2 STATUS:
SUPPORTED_WITHIN_TESTED_DOMAIN

## Resultat B --- Pion-surface reduceret eksakt

Pinned HyRec definerer for z\<900:

Pion = B/(A+B)

med

B = 4 beta_B

A = 3 R_Lya + Lambda_2s1s

R_Lya = LYA_FACT \* H/\[nH(1-xHII)\]

og selectorgrænsen PION_MAX=0.01.

På Pion=0.01:

B/(A+B)=1/100 =\> 100B=A+B =\> 99B=A =\> 396 beta_B = 3 R_Lya +
Lambda_2s1s.

Dette giver en præcis source-real hypersurface uden numerisk sampling.

For F=Pion-0.01 er fortegnet af den normale evolution på surface
ækvivalent med fortegnet af den relative evolution af B mod A:

sign(dF/ds)\|F=0 = sign\[d ln(B/A)/ds\]\|F=0

for enhver monoton evolutionsparameter s, op til den kendte positive
faktor fra Pion=r/(1+r).

HMLA- og SWIFT-siden har samme algebraiske Pion-definition ved samme
state, men de kan have forskellig dxHII/ds. Da R_Lya indeholder
1/(1-xHII), kan branchforskellen derfor ændre normalderivativet.
Pion-fladen kan ikke ryddes alene ved den ratio-surface argumentation.

BLOCKER_ID: LOCAL-Q050-PION-SURFACE-INTERVAL-CERTIFICATE-V2

## Frozen hillipop-ede_n3 checks

Verified from frozen config: - H0 = 0x1.e0a87807cbe58p-13 - Omega0_b =
0x1.81414da191ee2p-5 - T_cmb = 0x1.5cdd2f1a9fbe7p+1 - nH0_SI =
0x1.8126dce65a872p-3 - z_reio = 0x1.dfec4p+2 - has_scf=1 -
has_varconst=0 - has_exotic_injection=0 -
has_idm_b=has_idm_g=has_idm_dr=0 - recombination=HyRec.

Because the common background includes the frozen scalar-field
background, replacing H(z) by a generic LCDM approximation would violate
the source-real test contract.

## Minimal execution contract

Evaluate the exact pinned background and both literal hydrogen arms on
the potentially reachable Pion=0.01 surface for z in \[0,810\],
separately q=1e-6 and q=0.

Required observable: D_branch = d/ds ln(B/A) evaluated on 396 beta_B = 3
R_Lya + Lambda_2s1s.

Required branches: 1. literal HMLA arm, 2. literal SWIFT arm where its
fit-grid guard permits SWIFT.

Required certificate: - interval lower/upper bound for D_HMLA and
D_SWIFT over every reachable surface cell; - source/config hashes; -
domain subdivision; - outward/forward evolution sign convention; -
explicit list of unresolved cells.

ACCEPT: No reachable cell has an incompatible one-sided
sign/no-continuation pattern, and all zero-containing intervals are
resolved by refinement or a documented higher-order/tangency
certificate.

REJECT: A reachable certified cell exhibits literal one-sided fields
that prevent continuation under the specified selector/equality rule.

INCONCLUSIVE: At least one reachable cell retains a zero-containing or
dependency-dominated interval after the predefined refinement limit,
without a valid higher-order certificate.

No convexification. No Filippov replacement. No sampling-only
certificate.

## Termination gate

G1 PASS. G2 PASS for pinned source/config used in this round. G3 PASS
for ratio compatibility and exact Pion algebra; incomplete for global
Q050. G4 PARTIAL. G5 PARTIAL --- independent numerical interval
certificate not yet executed. G6 OPEN --- Pion surface remains
conclusion-critical. G7 PASS --- forward append only.

Q050 is not CLOSED.

## Point event

PREVIOUS_POINTS_ENTRY: Q050 RAW V1 / TOTAL 95 POINTS_EVENT: RESEARCH_RUN
ANALYSIS_POINTS: 45 COMPUTATION_POINTS: 0 SEARCH_POINTS: 20
VALIDATION_POINTS: 25 RUN POINTS: 90 pts TOTAL POINTS: 185 pts CYCLE
PROGRESS: 185/1000 pts NEXT SOME MILESTONE: 1000 pts POINTS TO NEXT
PUBLICATION: 815 pts NEW MILESTONES: NONE PENDING SOME PACKAGES: NONE
POINTS_STATE: VERIFIED PUBLICATION_STATE: NOT_DUE POINTS_BASIS:
Heuristisk redaktionel tæller for ny source-level selectorudledning,
frozen-config verification, ratio-surface compatibility proof and exact
Pion-surface reduction. Ingen interval/HPC execution er krediteret.

## Routing

NEXT_ENGINE: EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER
NEXT_TASK: Kør den definerede source-faithful intervalcertificate for
D_HMLA og D_SWIFT på den reachable Pion=0.01-surface under den pinned
hillipop-ede_n3 background, separat for q=1e-6 og q=0, og returnér
resultater + diagnostics til Matematikmotoren.

WHY_NEXT_ENGINE: Den næste mangel er ikke en ny matematisk definition.
Testen, observable, surface, branches og acceptkriterier er nu
defineret; den kræver source-faithful execution over den frosne
EDE-background.

EXPECTED_OUTPUT_ARTIFACT: Q050_PION_SURFACE_INTERVAL_CERTIFICATE_V1 +
machine-readable cells/diagnostics + hashes.

RETURN_ENGINE_AFTER_EXECUTION: BUBBLEVERSE.MATHEMATICS 2.3.0

GITHUB_READ_STATE: VERIFIED GITHUB_WRITE_STATE: READY_FOR_MANUAL_UPLOAD
