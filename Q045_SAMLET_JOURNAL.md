# BUBBLEVERSE — Q045 BOUNDED NATIVE HISTORY REFINEMENT V1

DATE AND TIME: 2026-10-10T10:36:39.832774+02:00 (Europe/Copenhagen).
CURRENT Q: Q-045 / Q045 — PROPOSED_CANONICAL_REGISTRATION_PENDING.
CASE ID: NOT DOCUMENTED.
EXACT QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
STATUS: CONTINUES. EXECUTION MODE: reuse native program/observer + bounded numerical diagnostic.
RECOMMENDED CHATGPT SETTING: current Work/Codex; strong reasoning, High if selectable. No account-specific ASTRA MAX availability or current effort level is asserted. A focused capable code/reasoning setup such as GPT-5.6, if available, is a fallback; no model switch or multi-agent work was used.

KEEP: complete incoming 615773-byte journal follows verbatim, SHA256 `cda8486d30a4236de7fd17785ecbc99639f62fbcc3b8968b91b10e7873601919`. All inherited state, Q042/Q044 epistemic closures, Q041 frozen inputs, source IDs/maps, actual successes, failures and model v0.5/R000005 through Q043 remain intact. This differential header governs the new stage; it does not reopen closed cases or replace physical conclusions.

ADD — J-Q045-REFHIST-01 [SOURCE-DOCUMENTED LIMITATION]: pinned CLASS thermodynamics/background use local adaptive tolerances and finite grid spacing. NDF15 accepts/rejects steps using its order-dependent local error estimate; this supplies no exported global continuum history or Thomson-integral enclosure. The V3 stored total-electron histories and spline derivatives support representation diagnostics. Its H/He workspace snapshots can lag source smoothing and are not independently certified species solutions. Missing historical binary compiler information remains NOT DOCUMENTED; reuse of the exact original binary hash avoids inventing build equivalence. Source/history/event/calibration qualifications are not waived.

ADD — J-Q045-REFHIST-02 [PREREGISTERED NUMERICAL DIAGNOSTIC]: PROGRAM_ID Q045-REFHIST-V1 uses the four completed optical V3 histories as L0, and runs exactly eight native background/thermodynamics observations: each original CamSpec/HiLLiPoP LCDM/EDE point at L1 and L2. Physical dictionaries and requested tau_reio remain identical. The nine settings below change only numerical controls; all other effective precision entries are checked against each parent. Original cached CLASS binary/source remain unchanged; only the read-only observer is compiled. This is a bounded reduction of history-accuracy uncertainty, not a declaration that global qualification follows from convergence.

| Numerical control | Existing L0 | L1 | L2 |
|---|---:|---:|---:|
| tol_thermo_integration | 1e-06 | 5e-07 | 2.5e-07 |
| thermo_integration_stepsize | 0.1 | 0.05 | 0.025 |
| thermo_Nz_lin | 20000 | 40000 | 80000 |
| thermo_Nz_log | 5000 | 10000 | 20000 |
| reionization_sampling | 0.015 | 0.0075 | 0.00375 |
| reionization_optical_depth_tol | 0.0001 | 5e-05 | 2.5e-05 |
| tol_background_integration | 1e-10 | 5e-11 | 2.5e-11 |
| background_integration_stepsize | 0.5 | 0.25 | 0.125 |
| background_Nloga | 40000 | 80000 | 160000 |

ADD — J-Q045-REFHIST-03 [METHOD/SCOPE]: eta-space exact cubic-minus is checked by independent two-point Gauss evaluation. In redshift space, 16/32-point Gauss-Legendre integrate cubic interpolated total xe and linearly interpolated native H in each interval, with integrand nH0·sigma_T·Mpc·xe(z)(1+z)^2/H(z). Native H is 1/Mpc, so no extra c enters. Same-history quadrature differences do not bound unobserved histories or H interpolation. Refined cubic xe/q are projected onto the original L0 redshift grid; accepted scalar depths, z_reio and selected support endpoints are compared. Recalibration and selector drift remain mixed with refinement; they are not isolated history error. Any empirical three-level order/remaining estimate is explicitly EMPIRICAL_NOT_A_BOUND. Even perfect agreement leaves REFERENCE_TRUTH_GATE=UNQUALIFIED and reference_error_bound=null. No source-physics, helium, integrator formula, global arrays, CMB, likelihood, optimizer, sampler or production change is made.

ADD — J-Q045-REFHIST-04 [BUDGET / FINITE STOP]: 8/52 theory slots already consumed (4 FULL baseline starts + 4 component observations). This stage adds at most 8 component observations, giving at most16/52 consumed and at least36 remaining. It does not satisfy eight independent FULL response/reproducibility tests, replace the original treatment matrix or authorize a larger budget. Eight independent 45-minute jobs, maximum4 in parallel, each native process capped900s and output512MiB. No checkpoint is required for these short stateless independent calls. Successful jobs survive failures; missing/duplicate/incompatible jobs cannot merge as complete. No automatic reruns/extra levels/response dispatch. Partial outcomes return to ingestion before recovery consumes any new slot.



[FINITE BUDGET / SPECIFICATION CONFLICT]: the inherited original treatment matrix requires48 FULL evaluations (four points × four treatments × three levels). Only4 FULL L0 native controls already exist; the4 prior telemetry observations and8 new history observations are components, not FULL replacements. Completing that unchanged matrix after this stage would require44 further FULL calls with only36 slots left: a minimum total60 exceeds52 by8. Including the original4 independent FULL repeats yields64, exceeding52 by12. FULL_MATRIX_BUDGET_GATE=FAIL_FOR_UNMODIFIED_48_FULL_PLAN_AFTER_THIS_STAGE. The eight-observation target itself stays within52 and stops as a diagnostic. No response campaign, test waiver, raised cap or narrowed scientific claim is authorized. Ingestion must report this exact terminal specification conflict alongside missing reference/error qualification; no automatic continuation is permitted.

ADD — J-Q045-REFHIST-05 [EXISTING RAW DATA REANALYSIS]: the new analyzer reads all four actual L0 parents (28333 nodes each) without a theory call and verifies their complete member hashes. Below z=30, redshift Gauss32 versus eta exact cubic differs by approximately6.38e-8–6.41e-8 dimensionless depth. Gauss16 versus32 is at most1.39e-17 there. This comparison uses total-xe cubic and linear sampled H, so it is a representation discrepancy, not a global physical-reference error. Unexpected native outputs and interpolation signs are preserved, never clipped. Refined L1/L2 histories and all CMB/likelihood responses remain NOT YET COMPUTED.

UPDATE — J-Q045-REFHIST-06 [REPOSITORY STATE]: current main inspected at2b08781ce57e3b71d7a6de19076db71d9e7702fe, full nontruncated1569-entry tree, no applicable AGENTS.md. No existing refinement target found. Reused executed optical V3 controller helpers and observational C bodies; patched observer metadata/node cap for declared refinement. Canonical launcher remains byte-identical. Registry corrects the V3 nested duplicated Q045- prefix and records its actual completed run38035928310; unrelated entries remain unchanged. New target Q045-REFHIST-V1 is locally registered ACTIVE for manual installation only. README documents current real architecture and V3 completion. No GitHub mutation or dispatch occurred. The package is locally prepared; runtime cache availability and native refined histories remain unverified until execution.

UNRESOLVED: uniform continuum/source/species/event/endpoint/calibration error evidence, admissibility of isolated two-call-site treatments, frozen decision margins, all consumed-observable response and native-likelihood contrasts. Original hypothesis and accepted model status are unchanged. The finite diagnostic cannot by itself close Q045 as a physical YES/NO. Its collector stops and returns the exact qualification blocker plus all eight outcomes to Result Ingestion & Routing. Ingestion determines whether further obtainable material evidence exists or an honest inconclusive closure should go to Motor14; no endless refinement loop is authorized.

## Source-register additions and claim map

```json
[
  {
    "source_id": "K-Q045-REFHIST-SOURCE-001",
    "type": "OFFICIAL PINNED REPOSITORY SOURCE",
    "title": "CLASS EDE native precision, thermodynamics grid and calibration stopping controls",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c",
    "file": "source/thermodynamics.c",
    "sha256": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
    "relevant_sections": [
      "thermodynamics_workspace_init",
      "thermodynamics_reionization_evolve_with_tau",
      "thermodynamics_reionization_get_tau",
      "thermodynamics_calculate_opticals"
    ],
    "supports": [
      "J-Q045-REFHIST-01",
      "J-Q045-REFHIST-02"
    ],
    "retrieval_method": "Authenticated pinned repository retrieval, local source read"
  },
  {
    "source_id": "K-Q045-REFHIST-SOURCE-002",
    "type": "OFFICIAL PINNED REPOSITORY SOURCE",
    "title": "Native adaptive NDF15 local error control and background integration",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/evolver_ndf15.c",
    "files": {
      "tools/evolver_ndf15.c": "49d26ddf369c08baea9cb297825f52a734df52e568687ed1f0be12ac68417856",
      "source/background.c": "84871d25c0a29391edf8d08b4826bd3ca3b33c638dae306375c0a681bb87d451"
    },
    "supports": [
      "J-Q045-REFHIST-01"
    ],
    "retrieval_method": "Authenticated pinned repository retrieval, local source read"
  },
  {
    "source_id": "I-Q045-REFHIST-PREP-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Preregistered bounded native history-refinement package",
    "program_id": "Q045-REFHIST-V1",
    "inspection_commit": "2b08781ce57e3b71d7a6de19076db71d9e7702fe",
    "contract": "q045_reference_history_contract_v1.json",
    "validation": "Q045_REFERENCE_HISTORY_LOCAL_VALIDATION.json",
    "scientific_results": "NOT YET COMPUTED",
    "supports": [
      "J-Q045-REFHIST-02",
      "J-Q045-REFHIST-03",
      "J-Q045-REFHIST-04"
    ]
  },
  {
    "source_id": "K-Q045-REFHIST-LIMITS-001",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "title": "GitHub Actions limits",
    "institution": "GitHub",
    "url": "https://docs.github.com/en/actions/reference/limits",
    "retrieved_date": "2026-10-10T10:36:39.832774+02:00",
    "claim": "GitHub-hosted job maximum 6 hours; this target caps each refinement job at 45 minutes",
    "supports": [
      "J-Q045-REFHIST-04"
    ]
  }
]
```

J-Q045-REFHIST-01 → K-Q045-REFHIST-SOURCE-001, K-Q045-REFHIST-SOURCE-002.
J-Q045-REFHIST-02/03 → I-Q045-REFHIST-PREP-001, K-Q045-REFHIST-SOURCE-001; input context I-Q045-OPTICAL-AUDIT-RAW-V3-001.
J-Q045-REFHIST-04 → I-Q045-REFHIST-PREP-001, K-Q045-REFHIST-LIMITS-001, I-Q045-OPTICAL-AUDIT-INGEST-V3-001.
J-Q045-REFHIST-05 → I-Q045-OPTICAL-AUDIT-RAW-V3-001, I-Q045-REFHIST-PREP-001 (local stored-history arithmetic only).
J-Q045-REFHIST-06 → I-Q045-OPTICAL-AUDIT-RUN-V3-001, I-Q045-REFHIST-PREP-001.
All preceding source IDs and claim mappings are preserved below.

## Verbatim incoming authoritative journal

# BUBBLEVERSE — Q045 OPTICAL AUDIT V3 RESULT INGESTION

DATE AND TIME: 2026-10-10T10:07:51.443051+02:00 (Europe/Copenhagen).
CURRENT Q: Q-045 / Q045 — PROPOSED_CANONICAL_REGISTRATION_PENDING.
CASE ID: NOT DOCUMENTED.
EXACT QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
STATUS: CONTINUES. Selected next engine: existing Execution-Mechanism / Numerical / HPC / Motor-Builder Engine.

KEEP: the complete incoming 601700-byte journal follows verbatim, SHA256 `2ad3e5771cfe79007fe1717048ba7bfd660c789a4dfb39696933b8a595b61a23`. Every inherited source ID, claim mapping, failure, scientific boundary and Q042/Q044 closure survives. This is a differential update to the same authoritative journal; this header governs the current stage. The unchanged original incoming journal/handoff in the executed final artifact match the supplied attachments byte-for-byte.

ADD — J-Q045-INGEST-V3-01 [TECHNICALLY VALIDATED COMPONENT RESULT]: run 38035928310, attempt1, repository Morfindien/Bubbleverse at `2b08781ce57e3b71d7a6de19076db71d9e7702fe` completed all seven jobs successfully. Final artifact and all four worker archives were downloaded and their official size/SHA256 verified. All expected worker identities, raw-product hashes, original parent hashes, exact physical dictionaries and executed package-manifest files passed ingestion. Collector records no failed/pending worker or error. Completed acquisition now supersedes prospective “V3 telemetry not yet computed” wording, solely at its actual scope.

ADD — J-Q045-INGEST-V3-02 [NATIVE OBSERVATION]: each point has 28333 final nodes, 19 scalar trials (17 bisections), a finite accepted native bracket, and source-produced support/spline data. Each final z/eta/total xe/opacity/exp(-κ)/g column is exactly equal to its original V2 baseline column. q = nH0·sigma_T·Mpc·xe·(1+z)^2 has max relative reconstruction residual 4.39e-16–5.30e-16. This validates decoded normalization at these outputs; it is not continuum/history accuracy. Native tau_reported equals the requested input; actual trial residuals below remain separate. Original source/binary pins are unchanged.

ADD — J-Q045-INGEST-V3-03 [BEREGNET, SAME CUBIC ONLY]: all worker analyses and derived files rederive exactly. Exact-cubic minus and independent two-point Gauss agree within 3.64e-12–2.33e-10 dimensionless depth over the full range. Native original cumulative versus decoded plus differs by at most 3.03e-9. Independently summing the interval curvature discrepancy reproduces the full plus-minus prefix within 2.03e-9. These are observed floating-point comparisons, not a certified continuum or floating-point error bound. The accepted trial scalar discrepancy is about 4.10e-7–4.13e-7. All depth entries in the table are dimensionless.

| Native diagnostic point | Actual last-trial tau | Scalar plus − exact cubic | Last trial − requested tau | Support rows | max absolute κ discrepancy, z≤1500 |
|---|---:|---:|---:|---:|---:|
| camspec-ede_n3 | 0.051415226206 | 4.127e-07 | -3.29731e-06 | 729 | 2.38435e-05 |
| camspec-lcdm | 0.051415282233 | 4.127e-07 | -3.24129e-06 | 729 | 2.39095e-05 |
| hillipop-ede_n3 | 0.0515073394426 | 4.09647e-07 | 4.86772e-07 | 730 | 2.3793e-05 |
| hillipop-lcdm | 0.0515074192794 | 4.09647e-07 | 5.66609e-07 | 730 | 2.38493e-05 |

The exact-real component identity remains Fplus−Fcubic = −sum[(m_i+m_i+1)h_i^3/12], h_i=eta_i+1−eta_i<0, q in Mpc^-1 and m=d²q/deta² in Mpc^-3. The unresolved physical-model error is b=(Fplus−Fcubic)+(Fcubic−R), not the first term alone. No statistical sigma is assigned to deterministic formula differences.

ADD — J-Q045-INGEST-V3-04 [PRESERVED DISCREPANCY, INTERPRETATION LIMITED]: full-table maxima 1.60134–1.60750 occur at z=5000000, native κ≈1.038e6–1.042e6, where recorded exp(-κ)=0. Underflow counts are 11547–11712. Those raw values are preserved; they are not an observable CMB effect or physical anomaly. For z≤1500 the same-history maximum is 2.37930e-5–2.39095e-5; for z≤30 it is 5.74182e-7–5.77744e-7. These are descriptive windows, not prospectively defined scientific pass/fail tolerances. Scalar supports vary across calibration trials, including the N=max(3,argmin) lower branch. Do not use a global smooth derivative through selectors. Workspace species snapshots and the node trapezoid remain non-certified diagnostics. No calibrated reference, changed spectrum or likelihood was evaluated.

UPDATE — J-Q045-INGEST-V3-05 [EXECUTION STATE]: baseline4 + telemetry4 = 8/52 consumed; ingestion starts0, at most44 slots remain. V3 acquisition is complete and must not be relaunched unchanged. The prior V1/V2 environmental/path failures remain HISTORICAL, not physical falsifications. Repository README/registry were read-only evidence; no remote change/dispatch was made during ingestion. Prepared registry ACTIVE wording is historical execution preparation, not scientific permission to repeat. [CORRECTED] the inherited handoff typo Q045-Q045-OPTICAL-AUDIT-V3 is not an identifier; canonical executed PROGRAM_ID is Q045-OPTICAL-AUDIT-V3.

UNRESOLVED — J-Q045-INGEST-V3-06 [PHYSICAL ANSWER]: REFERENCE_TRUTH_GATE=UNQUALIFIED; FINAL_RESULT_GATE=UNRESOLVED. Component tests are complete but physical history/event/endpoint/calibration remainder, reference recalibration, TT/TE/EE/all consumed observables, native likelihood response, original qualified inference margins and whole-domain coverage remain absent. Therefore Q045 cannot close as YES, NO or model falsification. It remains materially unresolved because a finite reference qualification and response acquisition may change its answer. No accepted model, H0 estimate, posterior or portability result is promoted. H0 entries remain frozen inputs.

## Exact next task and stopping rules

Recover the named numerical controls and event/support semantics from the acquired effective_precision.tsv, exact source and traces. Make the existing J-045-09 reference-qualification stage concrete: freeze baseline/half/quarter accuracy settings and an independent eta/redshift Thomson integration, then justify a physical history/interpolation/event/endpoint/calibration error enclosure. Reuse the four completed native inputs and raw histories. Do not repeat V3 or repair unrelated physics.

Before new computation, resolve exact original-binary/compiler reproducibility and species/history validity prerequisites; qualify each rather than assuming a workspace snapshot is an independent species solution. Missing historical compiler information remains a documented limitation; a new build must not be declared identical by assumption. Establish whether the isolated two-call-site intervention is valid without solver/source-physics repairs.

Allocate any necessary new histories prospectively within the 44 remaining theory slots. The original 48-treatment/three-level plan plus independent FULL repeats cannot simply be launched in addition to telemetry: these four telemetry runs are background/thermodynamics observations, not independent FULL CMB/likelihood repeats. Document reuse and mandatory tests, or report a finite budget/specification conflict; do not raise 52 or waive a test silently. Unqualified continuum remainder is a terminal prerequisite for that bounded stage, not permission to dispatch counterfactuals.

Only after reference qualification may a separately documented finite 00/10/01/11 response target be proposed with exact consumed-observable/native-likelihood coverage and unchanged inputs. No new target, PROGRAM_ID, remote dispatch, spectrum/likelihood execution, optimizer, sampler or production is authorized or created by this ingestion. Return qualification evidence or the exact blocker to Result Ingestion & Routing Engine. Actual original decision margins remain missing; no substitute spectral-percent tolerance or fixed-start likelihood gap may replace them.

SUCCESS: demonstrate a defensible physical reference/error enclosure on the exact domain with frozen numerical controls, valid histories/supports, preserved native control, reproducible identities and explicit budget; or document an exact terminal blocker with evidence. Neither outcome automatically answers decision-margin materiality.
FAILURE: missing/invalid identity/history/source support, nonfinite bracket, inadmissible reference, unqualified history/event/calibration remainder or irreconcilable mandatory-test/budget conflict stops that stage with the original raw evidence. This is technical/reference failure, not physical falsification.
STOP: stop this ingestion now; no further repetition of acquired V3 is needed. Next bounded stage returns once qualification passes or a specific prerequisite fails. Close Q045 and route to MOTOR14 only when the exact question has a defensible scoped answer and no obtainable material uncertainty can reasonably reverse it; an honest inconclusive closure is allowed if the terminal blocker exhausts the credible finite path. Current closure is not asserted.

## Source-register additions — stable IDs and provenance

```json
[
  {
    "source_id": "I-Q045-OPTICAL-AUDIT-RUN-V3-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Q045 original-binary optical audit V3, completed run and all seven jobs",
    "repository": "Morfindien/Bubbleverse",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/38035928310",
    "run_id": "38035928310",
    "commit": "2b08781ce57e3b71d7a6de19076db71d9e7702fe",
    "retrieved_at": "2026-10-10T10:07:51.443051+02:00",
    "supports": [
      "J-Q045-INGEST-V3-01",
      "J-Q045-INGEST-V3-05"
    ],
    "retrieval_method": "Authenticated GitHub run/jobs/artifact retrieval; actual artifact bytes SHA256 verified"
  },
  {
    "source_id": "I-Q045-OPTICAL-AUDIT-RAW-V3-001",
    "type": "BUBBLEVERSE NUMERICAL RESULT",
    "title": "Four native optical calibration and cumulative-opacity raw observations",
    "repository": "Morfindien/Bubbleverse",
    "run_id": "38035928310",
    "commit": "2b08781ce57e3b71d7a6de19076db71d9e7702fe",
    "artifact_ids": [
      11664510984,
      11664106256,
      11664032213,
      11663672292,
      11663577235
    ],
    "artifacts": [
      {
        "artifact_id": 11664510984,
        "artifact_name": "q045-audit-38035928310-worker-camspec-ede_n3",
        "archive_size": 8872393,
        "archive_sha256": "89cab696b213ee096b8e4404794a6b80302f9c43c0f9260f4c52fc92f7880817"
      },
      {
        "artifact_id": 11664106256,
        "artifact_name": "q045-audit-38035928310-worker-camspec-lcdm",
        "archive_size": 8875268,
        "archive_sha256": "1b33c6eac26aa007152afc91f8d1cab57a6114deea95395776e54041e943e536"
      },
      {
        "artifact_id": 11664032213,
        "artifact_name": "q045-audit-38035928310-final",
        "archive_size": 210202,
        "archive_sha256": "7f75dee1a9db28f7f5407ed950535123dcf73a84a0162bba9780fb2461e15d96"
      },
      {
        "artifact_id": 11663672292,
        "artifact_name": "q045-audit-38035928310-worker-hillipop-lcdm",
        "archive_size": 8863901,
        "archive_sha256": "5ce5f7baca5a37c8aaf7f3f40bf86ab106f6b41ad2f443e64d424c67cfcc392d"
      },
      {
        "artifact_id": 11663577235,
        "artifact_name": "q045-audit-38035928310-worker-hillipop-ede_n3",
        "archive_size": 8881624,
        "archive_sha256": "8368e832fee6e69fe308120c4c9145de60cdf827399dc794d8d9337c20be0fd6"
      }
    ],
    "supports": [
      "J-Q045-INGEST-V3-02",
      "J-Q045-INGEST-V3-03",
      "J-Q045-INGEST-V3-04"
    ],
    "retrieval_method": "Official artifact download; archive/member digests; unchanged original raw files saved individually"
  },
  {
    "source_id": "I-Q045-OPTICAL-AUDIT-INGEST-V3-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Independent raw-product ingestion and same-cubic arithmetic validation",
    "date": "2026-10-10T10:07:51.443051+02:00",
    "method": "Reverify original parent worker identities and exact manifests; replay pinned executed analyze(); compare derived file bytes; independently sum -((m_i+m_i+1)*h_i^3)/12 as cumulative component discrepancy",
    "validation_file": "Q045_OPTICAL_AUDIT_INGESTION_VALIDATION.json",
    "scope": "Existing stored histories only; zero new theory runs; no continuum error certificate",
    "supports": [
      "J-Q045-INGEST-V3-02",
      "J-Q045-INGEST-V3-03",
      "J-Q045-INGEST-V3-04"
    ]
  }
]
```

## Claim-to-source-map additions

```json
{
  "J-Q045-INGEST-V3-01": [
    "I-Q045-OPTICAL-AUDIT-RUN-V3-001",
    "I-Q045-OPTICAL-AUDIT-RAW-V3-001"
  ],
  "J-Q045-INGEST-V3-02": [
    "I-Q045-OPTICAL-AUDIT-RAW-V3-001",
    "I-Q045-OPTICAL-AUDIT-INGEST-V3-001",
    "I-Q045-WORKERS-V2-001"
  ],
  "J-Q045-INGEST-V3-03": [
    "I-Q045-OPTICAL-AUDIT-RAW-V3-001",
    "I-Q045-OPTICAL-AUDIT-INGEST-V3-001",
    "K-Q042-INGESTDESIGN-001"
  ],
  "J-Q045-INGEST-V3-04": [
    "I-Q045-OPTICAL-AUDIT-RAW-V3-001",
    "I-Q045-OPTICAL-AUDIT-INGEST-V3-001"
  ],
  "J-Q045-INGEST-V3-05": [
    "I-Q045-OPTICAL-AUDIT-RUN-V3-001",
    "I-Q045-OPTICAL-AUDIT-DESIGN-001"
  ],
  "J-Q045-INGEST-V3-06": [
    "I-Q045-MATH-OPTICAL-TRANSPORT-001",
    "I-Q045-OPTICAL-AUDIT-RAW-V3-001"
  ]
}
```

Complete prior scientific/external source records, source-to-claim maps and historical provenance follow within the unchanged original journal. New source objects are internal computational/technical evidence, not new publications. Raw artifact/member hashes and individual file links are in Q045_OPTICAL_AUDIT_RAW_FILE_INDEX.md; records/commands/software/inputs remain in Q045_OPTICAL_AUDIT_INGESTION_RESULT.json and original worker files.

---

# COMPLETE INCOMING AUTHORITATIVE JOURNAL — VERBATIM BYTES FOLLOW

# BUBBLEVERSE — Q045 OPTICAL AUDIT V3 INSTALLATION-PATH REPAIR

DATE AND TIME: 2026-10-10T08:36:36.753322+02:00 (Europe/Copenhagen).
CURRENT Q: Q-045 / Q045 — PROPOSED_CANONICAL_REGISTRATION_PENDING.
CASE ID: NOT DOCUMENTED.
EXACT QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
PROGRAM_ID: Q045-OPTICAL-AUDIT-V3. STATUS: CONTINUES.

KEEP: complete previous journal follows verbatim (597695 bytes, SHA256 `8ac73814394f9df228817288cf14b4a694c8f01851ae08a862536f3133bab4f8`). All previous source IDs, claim maps, baseline values, failures and Q042/Q044 closures survive. This header differentially updates the same authoritative journal.

ADD — J-Q045-PATH-01 [TECHNICAL FAILURE]: optical audit V2 run38030968453, attempt1, commit `0124316bfb88629bcccd9b18a5cef448ade309ed` passed static/input recovery and restored the exact original cache in all four workers. Its finite-test step then failed because the cache regression test read the workflow from repository root, while the installed workflow exists at `.github/workflows/q045-optical-audit-v2.yml`. All four native observation steps were skipped. Zero theory evaluations started in optical V1 or V2; the inherited budget remains4/52 consumed. The inspected CamSpec-EDE worker's native-array synthetic fixture passed, but this is not an original cosmological binary observation.

ADD — J-Q045-PATH-02 [CORRECTION]: V3 changes the test's workflow path to its canonical `.github/workflows/` location. Local validation stages the exact installed file map with no root YAML duplicate. Reproducing that layout exposed the old failure before correction. The production controller changes only optical target/file version names; the C observer is byte-identical to V2. The successful original nine-path cache identity, CLASS source/binary pins, physical dictionaries, precision, methods, data/likelihood/prior, four-worker limit and numerical gates remain unchanged. No substitute binary, rebuild or scientific tolerance is introduced.

UPDATE: V2 is FAILED/inactive in the prepared registry, carrying actual run/commit and zero started evaluations; V3 is the new ACTIVE target. Other registry entries and the permanent launcher are unchanged. README describes the current target and retains V1/V2 failures. Earlier local preparation PASS did not establish installed-layout validity and is corrected for that limitation, without erasing its historical test evidence.

ADD — I-Q045-OPTICAL-AUDIT-RUN-V2-001 [INTERNAL TECHNICAL EVIDENCE]: https://github.com/Morfindien/Bubbleverse/actions/runs/38030968453; official jobs/artifact metadata and CamSpec-EDE worker log, retrieved 2026-10-10T08:36:36.753322+02:00; preserved in `Q045_OPTICAL_AUDIT_V2_FAILURE.json`. Artifact inner files are not claimed as retrieved. I-Q045-PATH-REPAIR-001: this V3 code/contract/manifest and red/green installed-layout validation. Claim map: J-Q045-PATH-01→I-Q045-OPTICAL-AUDIT-RUN-V2-001; -02→I-Q045-PATH-REPAIR-001 plus frozen source/method IDs already in this journal.

UNRESOLVED: new original-binary telemetry, qualified physical continuum reference, response in CMB/likelihood and actual original inference margins. FINAL_RESULT_GATE=UNRESOLVED; REFERENCE_TRUTH_GATE=UNQUALIFIED. No model is physically falsified or promoted. Scientific results are NOT YET COMPUTED.

NEXT: one V3 launch, four bounded independent outcomes, then existing Result Ingestion & Routing Engine with complete Q/journal/source/provenance state. No automatic reruns, treatments, samplers or production continuation. Actual V3 GitHub installation/execution is not performed by assistant.

---

# COMPLETE PREVIOUS AUTHORITATIVE JOURNAL — VERBATIM BYTES FOLLOW

# BUBBLEVERSE — Q045 OPTICAL AUDIT V2 CACHE REPAIR

DATE AND TIME: 2026-10-10T07:16:28.480315+02:00 (Europe/Copenhagen).
CURRENT Q: Q-045 / Q045 — PROPOSED_CANONICAL_REGISTRATION_PENDING.
CASE ID: NOT DOCUMENTED.
EXACT QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
PROGRAM_ID: Q045-OPTICAL-AUDIT-V2.
STATUS: CONTINUES; locally checked repair prepared, remote installation and execution not performed by assistant.

KEEP: the complete prior authoritative journal follows verbatim (592961 bytes; SHA256 `1e9fefdaa4c528501cd24994f2ff8f9596af927d0de7d5f3673cb7a98934fb36`). Every inherited source ID, claim map, failed hypothesis, Q042/Q044 closure, frozen scientific input and baseline result survives. This differential header updates the same journal.

ADD — J-Q045-CACHE-01 [TECHNICAL FAILURE]: optical audit V1 run38026287784, attempt1, commit `e4a4c1061ae84d5bb638afaa2d0902004d779dcb` passed static and baseline-input recovery. All four audit jobs failed at cache acquisition; their original-binary observation steps were skipped. The collector failed its completeness requirement and preserved the final artifact. Zero new theory evaluations started, supported by official job-step records. Four original V2 native baseline evaluations remain consumed out of52; the four telemetry slots remain available. No physical answer, parameter preference or anomaly was produced.

ADD — J-Q045-CACHE-02 [DOCUMENTED DIAGNOSIS]: V1 used the correct original key but replaced its nine-path cache list with only `external/class_ede`. GitHub matches the cache version as well as key; the path metadata contributes to that version. This explains why V1 cannot select the previously used nine-path version. Current cache retention/availability is not independently established. The Node punycode warning is preserved; it is not the failing prerequisite.

UPDATE — J-Q045-CACHE-03 [MINIMAL REPAIR]: V2 restores the exact original nine paths, order, key and cache action from the successful baseline workflow. `fail-on-cache-miss:true`, no restore keys, no cache save, no rebuild and exact CLASS source/binary hashes remain enforced. The native observer C is byte-identical to V1; controller changes only target/file version names. Numerical methods, input dictionaries, precision, likelihoods, data, priors, limits and physical gates are unchanged. Ten Python tests now include a regression for the original complete cache identity.

SUPERSEDE: V1 is retained as FAILED in the prepared registry, with actual run/commit and zero started evaluations. V2 is the new active target; all other registry entries survive exactly. The permanent launcher is unchanged. README current-target references move to V2 and preserve the failed V1 record.

ADD — I-Q045-OPTICAL-AUDIT-RUN-V1-001 [INTERNAL TECHNICAL EVIDENCE]: https://github.com/Morfindien/Bubbleverse/actions/runs/38026287784; official jobs/artifact metadata and worker/collector logs, retrieved 2026-10-10T07:16:28.480315+02:00; summarized with original excerpts in `Q045_OPTICAL_AUDIT_V1_FAILURE.json`. Raw artifact inner contents were not downloaded during this repair; no claim is invented from their filenames.

ADD — I-Q045-CACHE-VERSION-001 [OFFICIAL TECHNICAL DOCUMENTATION]: GitHub, Dependency caching reference, https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching, retrieved 2026-10-10T07:16:28.480315+02:00; cache matching includes key/version, with path/compression metadata in the version. Claim map: J-Q045-CACHE-01→I-Q045-OPTICAL-AUDIT-RUN-V1-001; -02→I-Q045-CACHE-VERSION-001,I-Q045-OPTICAL-AUDIT-RUN-V1-001; -03→the frozen V2 baseline workflow at `e4a4c1061ae84d5bb638afaa2d0902004d779dcb`, this V2 package/tests/manifest.

UNRESOLVED: original-binary remote observation, physical continuum reference qualification, CMB/likelihood response and original inference margins. FINAL_RESULT_GATE=UNRESOLVED; REFERENCE_TRUTH_GATE=UNQUALIFIED. Successful cache recovery alone resolves no physical claim. A corrected lookup that still misses must stop before computation and preserve its evidence, not build a substitute binary.

RETURN ROUTE: existing Result Ingestion & Routing Engine after the four bounded outcomes or failed prerequisites. No automatic treatment, repeated campaign, posterior, source repair or production restart.

---

# COMPLETE PREVIOUS AUTHORITATIVE JOURNAL — VERBATIM BYTES FOLLOW

# BUBBLEVERSE — Q045 OPTICAL AUDIT EXECUTION UPDATE

DATE AND TIME: 2026-10-10T06:56:50.876576+02:00 (Europe/Copenhagen).
CURRENT Q: Q-045 / Q045 — PROPOSED_CANONICAL_REGISTRATION_PENDING.
CASE ID: NOT DOCUMENTED.
QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?

STATUS: bounded observation package prepared and locally checked; GitHub installation and execution NOT PERFORMED by assistant.
PROGRAM_ID: Q045-OPTICAL-AUDIT-V1.

## Differential journal actions

KEEP: all incoming scientific state, source IDs, maps, numerical values, technical failures and warnings. The complete 586654-byte incoming journal (SHA256 `a02f72a9b9354e29eef3000db5344fce95bcd817637b945a8adf30d3ef77ac81`) follows verbatim. This header is a differential update to the same authoritative journal; it is not a new or competing journal.

UPDATE: V2 baseline run38023210800 is complete (four diagnostic points), while its remote README still said full runtime validation was pending. The prepared README/registry now record that actual completion and make V2 inactive against redundant relaunch. All other registry entries survive exactly.

ADD — J-Q045-OPTICAL-AUDIT-01 [TECHNICAL PREPARATION]: inspect exact scalar trials and raw cumulative kappa through read-only symbol observers linked to the unchanged original diagnostic classy binary. Reuse the existing Q042 V24 linking method, never the V24 scientific point or Q042 repair task. Fixed physical input dictionaries are copied from the four verified V2 manifests; sampled vectors/nuisances remain connected to those original baseline records. No new motor, physical input, source patch, accuracy override, dataset, prior, optimizer or posterior is introduced.

ADD — J-Q045-OPTICAL-AUDIT-02 [PREREGISTERED METHOD]: record every actual scalar support, source-produced spline second derivatives, trial z_reio/tau/endpoint, native accepted bracket replay, effective precision/default paths/constants, source species workspace snapshots, raw cumulative kappa before exponentiation, and final total-x_e/opacity/background tables. Require exact equality of decoded final native columns against V2. Workspace H/He are snapshots after source returns; smoothing may leave them at the previous-regime evaluation and parametric reionization modifies the total separately. They are not independent fully qualified species histories. Preserve both workspace and actually stored total x_e instead of imposing equality between different physical conventions.

ADD — J-Q045-OPTICAL-AUDIT-03 [MATHEMATICAL COMPONENT]: native-plus and exact-cubic-minus use identical emitted eta/opacity/second derivatives; independent two-node Gauss evaluation checks the same cubic integral. A redshift-space node trapezoid uses the fork's nH0, sigma, Mpc and native H in1/Mpc; no c is inserted twice. The coordinate reconstruction and shared history dependence stay explicit. Neither comparison establishes a converged physical Thomson reference, a continuum remainder, a response in CMB/likelihood, or an original decision margin.

UNRESOLVED: original binary compiler provenance, full historical campaign equivalence, physical species/history/event validity, independently qualified continuum error, prospective matched three-level reference accuracy, all required new response observables and actual inference margins. FINAL_RESULT_GATE remains UNRESOLVED. Actual new telemetry/numerical response is NOT YET COMPUTED. No physical hypothesis is falsified or promoted.

ADD — J-Q045-OPTICAL-AUDIT-04 [FINITE EXECUTION]: exactly four original-background/thermodynamics observations maximum, one per fixed input. Reserve four conservative theory-evaluation slots in the existing52 total; four native baselines are already complete. At most8 slots consumed after this target; at most44 remain for any separately justified work. No count reset, automatic retry, new point, fourth refinement, source repair or historical sampler resume. These are new telemetry evaluations, not full CMB/likelihood reproducibility runs. Runtime attempts/failures consume their started slots; unstarted jobs do not. The first failed prerequisite stops its worker, preserves raw logs, and returns the failure. Valid independent workers remain preserved.

ADD — I-Q045-OPTICAL-AUDIT-DESIGN-001 [INTERNAL TECHNICAL EVIDENCE]: this prepared contract/code/manifest/test record; inspection head `175a657490c2a04bbbd8e1b3e4a3c3fbbc499f72`. Primary method sources remain K-Q042-INGESTDESIGN-001 (pinned arrays.c), K-Q042-V24-001/K-Q042-DESIGN-001 (pinned thermodynamics.c), I-Q045-WORKERS-V2-001 and I-Q045-RUN-V2-001. New implementation reference: repository `q042_class_origin_probe_v24.c` / `q042_class_origin_v24.py` at the inspection head. These supply a previously executed observation architecture, not an independent scientific reference.

ADD — I-Q045-GITHUB-LIMITS-001 [OFFICIAL TECHNICAL DOCUMENTATION]: GitHub, Actions limits, retrieved 2026-10-10T06:56:50.876576+02:00, https://docs.github.com/en/actions/reference/limits. Hosted job limit6hours; four45-minute worker caps with900-second native process caps are below it. Actual cache/install/observer time is NOT YET MEASURED; runtime estimates are planning estimates, not measured CPU-hours.

CLAIM MAP: J-Q045-OPTICAL-AUDIT-01→I-Q045-WORKERS-V2-001,I-Q045-ARCHITECTURE-001,I-Q045-OPTICAL-AUDIT-DESIGN-001; -02/-03→K-Q042-INGESTDESIGN-001,K-Q042-V24-001,K-Q042-DESIGN-001,I-Q045-OPTICAL-AUDIT-DESIGN-001; -04→I-Q045-OPTICAL-AUDIT-DESIGN-001,I-Q045-GITHUB-LIMITS-001. No new numerical or physical claim is assigned before execution.

RETURN ROUTE: exactly Result Ingestion & Routing Engine with this complete journal, raw products and honest reference gate. Q042/Q044 remain closed. No admission/promotion/production restart occurs. A terminal blocker from this audit is evidence for ingestion's closure decision; this preparation does not close Q045.

---

# COMPLETE INCOMING AUTHORITATIVE JOURNAL — UNCHANGED BYTES FOLLOW

# BUBBLEVERSE — RESULT INGESTION & ROUTING HANDOFF

STATUS: CONTINUES.
CASE ID: NOT DOCUMENTED.
CURRENT Q: Q-045 / Q045 — PROPOSED; canonical scientific registration pending.
QUESTION: For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
DATE AND TIME: 2026-10-10T06:30:30.109873+02:00 (Europe/Copenhagen; runtime clock).
RESULT ID: R-Q045-NATIVE-BASELINE-INGESTION-001.
SELECTED NEXT ENGINE: BUBBLEVERSE — AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.
Q-COMPLETION GATE: NOT YET SATISFIED.
FINAL_RESULT_GATE: UNRESOLVED.

## RECOMMENDED CHATGPT EXECUTION PROFILE

AVAILABLE CONFIGURATIONS CONSIDERED: current Work/Codex with code/files, GitHub reads/artifact retrieval and web/primary-source access. The exposed agent catalogue includes GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol and GPT-6 Luna, but this does not establish the operator's model menu or comparative scientific reliability. No model switch or agent delegation occurred.
RECOMMENDED MODEL / MODE: current Work/Codex with a strong reasoning configuration.
RECOMMENDED REASONING LEVEL: High or deeper if selectable; exact active effort is not independently verified.
RECOMMENDED EXECUTION STYLE: bounded autonomous source/code/numerical work; capability classes C + E in this ingestion engine's catalogue.
WHY: full journal continuity and a narrowly defined two-call-site numerical reference need careful provenance and real code execution. A maximum-mode research campaign is unnecessary for parsing these successful raw baselines.
RECOMMENDED PLUGINS / TOOLS: read-only GitHub for pinned methods/artifacts; local Python for raw integrity and reference calculations; persistent individual-file delivery.
OPTIONAL CAPABILITIES: primary literature/source lookup only for missing reference/error definitions. No browser, broad literature search, plugin installation, images, deployment or parallel agents are needed now.
FALLBACK: another strong reasoning setup with equivalent file/repository/computation tools; GPT-5.6 if available and sufficient.
UPGRADE: only if switched-event reference/error enclosure or coupled calibration/transport implementation exceeds the current setup's reliable capacity.
CAPABILITY LIMITATIONS: account model menu, exact context/usage limits and allocated HPC are not verified. More reasoning cannot supply missing physical/inference products.

## SAMLET JOURNAL — CURRENT EFFECTIVE UPDATE

KEEP all 568275 incoming journal bytes, including the complete 91-object inherited source register, the inherited claim-map trees, all Q/source IDs and scientific/technical failures. Incoming SHA256 `aec2dd628f61197a2b06f732fe39ad8be09c374e43b1f632c3c0c6644757f4cc`. They follow this differential update verbatim. The current supplied journal identity is preserved; no parallel scientific journal is created. Historical preparation/launch instructions below are superseded for the completed V2 acquisition.

KEEP Q042 and Q044 closed inconclusive; KEEP Q045 proposed/open; KEEP the accepted-model boundary only as inherited, not freshly verified or promoted. No main question, source pin, physical model or original scientific decision rule changes.

ADD [BUBBLEVERSE NUMERICAL / TECHNICAL RESULT] Run `38023210800`, attempt 1, workflow `.github/workflows/q045-native-baseline-v2.yml`, execution commit `175a657490c2a04bbbd8e1b3e4a3c3fbbc499f72`, completed successfully. All seven jobs succeeded. The four native FULL diagnostic starts completed with process return code 0 and no worker errors. Job completeness and merge compatibility PASS; baseline gate PASS_NATIVE_DIAGNOSTIC_ONLY. The received final archive matches official artifact `11659125612` digest `d1a236bbf4d0660e7b3d38f13aff1a2aa8f3f330d45ddc3b51072edaaa428e97`. Contract SHA256 `d1855120a2746e1b3838aa422cfe41cfd980f340301ea5c0fa6612b0cd29e6b8`. Attached handoff/journal equal their archived copies.

| Native FULL diagnostic | log likelihood sum | H0 input (km/s/Mpc) | Requested tau | Worker wall time (s) |
|---|---:|---:|---:|---:|
| camspec-lcdm | -1590.008076 | 68.165994 | 0.05141852 | 35.103 |
| camspec-ede_n3 | -1283.825249 | 68.165994 | 0.05141852 | 61.641 |
| hillipop-lcdm | -1692.644369 | 68.711122 | 0.05150685 | 34.828 |
| hillipop-ede_n3 | -1248.049955 | 68.711122 | 0.05150685 | 48.079 |

These H0/tau values are fixed diagnostic INPUTS, not new fitted estimates or measurements. Likelihoods include the unchanged shape/penalty components recorded by the original builders; no cross-arm absolute subtraction, evidence comparison, model ranking or optimized DeltaChi2 is inferred. Full machine precision and component/prior/posterior separation are preserved in the raw JSONs.

STRENGTHEN [TECHNICAL USABILITY] All four downloaded worker archives match their official SHA256 digests; every original file hash matches its worker record. The final/worker Q, run, contract and execution identities agree. All workers report the pinned original diagnostic CLASS binary `df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf`, Python 3.11.16, all ten package versions, identical external source pins, the same complete 175-file cached-data snapshot and the same external signature. Native likelihood sums match component sums; posterior accounting agrees within <=2.3e-13. All three tables are finite and correctly shaped: 9,002 TT/TE/EE rows (ell 0..9001), 28,333 thermodynamics rows and 40,000 background rows. This is role-limited validation, not independent physical-history or full historical-parent qualification.

UPDATE [KNOWN GOOD TECHNICAL PATH] The flit_core 3.12.0 repair is now demonstrated in the actual Python 3.11.16 GitHub execution. V1's environment failure remains historical. No baseline repeat is needed merely to show that the installation works.

ADD [REPRESENTATION LIMITATION; RAW OUTPUT PRESERVED] Thermodynamics contains native total x_e, opacity, exp(-kappa) and visibility. Depending on the worker, 11,547–11,712 exp(-kappa) entries are exactly zero. At those rows raw g equals DBL_MIN=2.2250738585072014e-308, matching the pinned source's explicit zero-visibility guard. This explains the tiny absolute residual in g versus opacity*exp(-kappa); it is not a new scientific anomaly or a reason to delete the rows. The exported exponent does not preserve the pre-exponentiation kappa at those rows. A -log inversion would not recover that missing curve. Requested tau is present; calibrated z_reio, accepted bracket/residual, scalar-specific spline derivatives and direct raw kappa are not explicitly recorded in this package.

UNRESOLVED [SCIENTIFIC ANSWER] No 10/01/11 intervention, independently qualified Thomson reference, refinement/remainder bound, calibrated spectrum/native-likelihood contrast, actual original decision-margin transport or full-domain inference envelope was produced. Native total x_e is not an independently qualified species history. Original campaign-binary equivalence and independently missing parent-data qualification remain exactly as documented. The finite values do not repair or refute the historical failing V29 point; these are different frozen input vectors.

PRESERVE warnings: legacy SACC FITS ordering assumption and ACT lensing's Hartlap correction 0.9860935524652339. They are original raw execution details, not new data choices; they are not independently qualified by this ingestion. No undocumented warning is silently waived into a physical final PASS.

SELECT exactly one next engine: the existing Execution-Mechanism / Numerical / HPC / Motor-Builder Engine. The bottleneck is now actual reference-stage execution and missing internal quantities, not another proof of the already established integration formula. The repository's scoped motor file is historical Q042 context; its helium-repair instructions must not be imported into Q045. The operator's existing engine and J-045-09 finite optical-depth specification govern this handoff.

NEXT TASK: Finish the already specified isolated Thomson-reference acquisition, reusing the verified native 00 baselines; first recover exact scalar-calibration support/spline/bracket and pre-exponentiation cumulative depth, then qualify same-history reference error before any 10/01/11 coupled history/spectrum/native-likelihood evaluation.

## NEXT TASK — FROZEN SCOPE AND FINITE STOP

1. Reuse these exact four 00 outputs and their immutable input vectors as the native diagnostic controls. Inspect recoverability from these stored products before scheduling anything. Do not repeat V2 wholesale or refit starts.
2. Recover the scalar-calibration-specific table/eta nodes, selected first-minimum index and actual endpoint, spline boundary conditions/second derivatives, requested/reported/independently realized tau, z_reio and accepted calibration bracket/residual. Recover cumulative kappa BEFORE exponentiation, its full-table spline derivatives, and every additional observable consumed by the frozen likelihoods (including lensing). Export effective default precision/helium/constants/build identities where not already recorded. Use minimal observation-only instrumentation if exact quantities cannot be reconstructed; do not guess or merge a helium/branch repair into this experiment.
3. Freeze units and source-derived normalization; H is in 1/Mpc in the export, conformal time is a length in Mpc, opacity is in 1/Mpc, and x_e is electrons per H nucleus. Derive reference n_e and c conversions from the actual fork. Compare native plus, exact-spline minus and independently integrated Thomson depth on IDENTICAL history/support; cross-check eta and z formulations. A same-grid minus correction is a control, not by itself a converged physical-model reference.
4. Make the already specified J-045-09 reference stage executable only with a defensible interpolation/history/quadrature/calibration error account. Freeze the three accuracy levels and event/support handling before new treatment output. If qualification cannot be defended, stop this stage with the exact UNQUALIFIED/BLOCKED reason; do not choose a tolerance to make it pass.
5. If that gate passes, carry out the existing isolated treatments 10 (reference scalar only), 01 (reference cumulative only), 11 (both), with matched native controls where a new build/refinement makes them necessary. Change only the authorized optical-depth call sites, preserve all physical inputs, native likelihoods/nuisances and requested tau. Preserve the original binary/control. The unchanged initial maximum is 52 theory evaluations across the entire preregistered diagnostic acquisition; four original 00 evaluations are now completed. Count instrumented controls/refinements/repeats in that ledger rather than restarting its budget. No arbitrary fourth refinement, automatic rerun, additional point or old sampler checkpoint resume.
6. Report signed same-history scalar/cumulative biases, support/endpoint terms, calibration changes, absolute TT/TE/EE and consumed-observable changes, exact within-arm native likelihood contrasts and factorial interaction, with qualified uncertainty or explicit failed reference gate. Avoid dividing by TE near zero. Recover actual original decision margins only from qualified existing products; do not fabricate a replacement margin or launch inference to create one. Fixed-point sensitivity alone is not a changed posterior/best-fit preference.
7. Return the complete current journal, source IDs, all raw products, build/patch/config/data/binary identities, the exact qualification/response scope and finite stop result to Result Ingestion & Routing. If no remaining obtainable material evidence can change the warranted answer, ingestion closes Q045 epistemically and routes directly to Motor14.

SUCCESS: A same-definition reference with defensible uncertainty and qualified finite response, or a precise documented terminal prerequisite blocker. Acquisition success does not automatically establish inference materiality.
FAILURE: Missing source/identity/observable, invalid history, unsupported reference or nonfinite bracket -> preserve the raw evidence and stop that acquisition branch. Technical failure is not physical falsification.
STOP: Do not repeat successful baseline acquisition or old component proofs. End at the first terminal reference/identity failure, the inherited finite evaluation limit, or a defensible answer to the exact Q. If further obtainable work has no realistic material-reversal value, close Q045 with its honest warranted scope and route directly to Motor14. Report Writer is excluded.
PRODUCTION_RESTART_AUTHORIZED=false. No sampler, optimizer, remote mutation, new PROGRAM_ID or dispatch is performed by this ingestion.

## ACTIVE SOURCE REGISTER — CURRENT ADDITIONS AND RELEVANT INHERITED SOURCES

- **I-Q045-FINAL-V2-001** — V2 four-native-baseline final artifact. Native completeness/merge result, identities and explicit unresolved science gates. https://github.com/Morfindien/Bubbleverse/actions/runs/38023210800/artifacts/11659125612
- **I-Q045-WORKERS-V2-001** — Four exact raw V2 worker artifacts. Actual fixed inputs, native spectra/thermodynamics/background, likelihood components and original warnings. Exact artifacts/files and hashes are carried in Q045_INGESTION_RESULT.json and the raw-file index.
- **I-Q045-RUN-V2-001** — GitHub run 38023210800 and seven job conclusions. All seven GitHub jobs succeeded; not physical qualification. https://github.com/Morfindien/Bubbleverse/actions/runs/38023210800
- **I-Q045-CODE-V2-001** — Executed frozen V2 controller, workflow and contract. One unchanged FULL diagnostic evaluation at each original start; no optical-depth intervention or inference. https://github.com/Morfindien/Bubbleverse/blob/175a657490c2a04bbbd8e1b3e4a3c3fbbc499f72/q045_native_baseline_v2.py
- **I-Q045-PRODUCT-AUDIT-001** — Independent raw-byte and product audit. Role-limited technical usability, exact raw preservation and numerical representation limitations. Exact artifacts/files and hashes are carried in Q045_INGESTION_RESULT.json and the raw-file index.
- **I-Q045-ARCHITECTURE-001** — Established execution engine and historical scoped repository motor. Existing engine function; this historical Q042 task does not authorize a Q045 helium repair or production restart. https://github.com/Morfindien/Bubbleverse/blob/175a657490c2a04bbbd8e1b3e4a3c3fbbc499f72/q042_treatment_design_motor.md

- **K-Q044-M14-REION-001** — Planck Collaboration, R. Adam et al., *Planck intermediate results. XLVII. Planck constraints on reionization history*, 2016, A&A 596 A108; DOI 10.1051/0004-6361/201628897; arXiv:1605.03507v3; https://arxiv.org/html/1605.03507v3 . Physical Thomson-depth and CMB-screening context only; not this fork's accuracy certificate.
- **K-Q042-INGESTDESIGN-001** — `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`, `tools/arrays.c`; SHA256 c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4. Scalar/cumulative plus-curvature integration formulas. https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c
- **K-Q042-V24-001 / K-Q042-DESIGN-001** — same fork/pin, `source/thermodynamics.c`; SHA256 d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6. Scalar support/calibration, cumulative opacity, exponentiation and DBL_MIN visibility guard. These aliases are the same source, not independent evidence. https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c
- **I-Q044-CONTRACT-001 / I-Q044-SOURCELOCK-001** — original scientific specification and dependency lock in `Morfindien/Bubbleverse`; SHA256 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c and 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56. Original decision predicates and frozen identities; no inferred actual margins. https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_spec_v1.json
- **I-Q045-MATH-OPTICAL-TRANSPORT-001** — preserved internal mathematical stage in the full journal: physical units/orientation, native support, calibration identity, two-call-site factorial and finite qualification/stop rules. Methodological evidence, not an independent observation.

The complete inherited register and maps are physically preserved in the authoritative journal below. New internal source objects, exact artifact/file hashes and raw-file mappings are serialized in Q045_INGESTION_RESULT.json. Multiple references to the same pinned file are not independent evidence.

## CLAIM-TO-SOURCE MAP — NEW DIFFERENTIAL ENTRIES

- **C-Q045-I01**: All four native diagnostics completed; no failed/pending workers; native-only completeness/merge pass → I-Q045-FINAL-V2-001, I-Q045-WORKERS-V2-001, I-Q045-RUN-V2-001
- **C-Q045-I02**: Actual files/hashes/identities, all three table products and component accounting pass role-limited ingestion checks → I-Q045-WORKERS-V2-001, I-Q045-PRODUCT-AUDIT-001
- **C-Q045-I03**: H0 and requested tau are fixed start inputs; likelihoods are unoptimized values and are not a posterior/model-preference conclusion → I-Q045-WORKERS-V2-001, I-Q045-CODE-V2-001, I-Q044-CONTRACT-001
- **C-Q045-I04**: No isolated optical-depth contrast, qualified reference or actual decision-margin transport has been computed → I-Q045-FINAL-V2-001, I-Q045-CODE-V2-001, I-Q045-MATH-OPTICAL-TRANSPORT-001
- **C-Q045-I05**: exp(-kappa) has exact zero rows; pre-exponentiation native kappa cannot be recovered there by logarithm; g floor at these rows agrees with the pinned DBL_MIN guard → I-Q045-WORKERS-V2-001, I-Q045-PRODUCT-AUDIT-001, K-Q042-V24-001, K-Q042-DESIGN-001
- **C-Q045-I06**: The sole next destination is the established execution engine for the finite reference stage, preserving Q045 rather than resurrecting historical Q042 treatment instructions → I-Q045-ARCHITECTURE-001, I-Q045-MATH-OPTICAL-TRANSPORT-001, I-Q045-WORKERS-V2-001

---

## COMPLETE INCOMING AUTHORITATIVE JOURNAL — VERBATIM HISTORICAL STATE

# BUBBLEVERSE — OVERLEVERING

STATUS: CONTINUES — V1 ENVIRONMENT FAILURE DOCUMENTED; V2 REPAIR PREPARED, GITHUB VALIDATION PENDING.
CURRENT Q: Q045 / Q-045 — PROPOSED; canonical scientific registration pending.
STAGE RECORD: I-Q045-ENV-FLIT-REPAIR-002.
DATE AND TIME: 2026-10-10T04:04:19.081115+00:00 (UTC, runtime clock).
PROGRAM_ID: Q045-BASELINE-V2; supersedes Q045-BASELINE-V1.
NEXT ENGINE: Result Ingestion & Routing Engine after bounded baseline acquisition.
ACTUAL COMPUTED SCIENTIFIC RESULT: NOT COMPUTED; all four V1 evaluations were skipped.
FINAL_RESULT_GATE: UNRESOLVED.
REMOTE WRITES / DISPATCH BY ASSISTANT: false.

## CHATGPT-SETUPVURDERING

Recommended: current Work/Codex with repository reads, local code execution and strong reasoning; High if selectable. Capability classes C/A + H. This is a contained installation repair. GPT-5.6 with equivalent tools is a suitable fallback if available; ASTRA MAX menu availability is not verified. No model switch is necessary. Upgrade only if a later failure requires substantial scientific or numerical reconstruction.

## Differential journal update

KEEP the full previous authoritative journal verbatim below, including Q, scientific question, sources/source IDs, constraints, results, failures and unresolved scientific qualifications. Prior journal SHA256: `03006221b8d73a0f8d0e51a133e733d8b7a61fea6ef8a180f1c8149c510ab298`. Historical instructions below are superseded by this current action; no journal is rebuilt.

ADD [BUBBLEVERSE TECHNICAL EVIDENCE] Read-only repository inspection at `7b5047dd9eafbd7986c15514ec3534e2b0ed3bc3`. V1 was installed by the operator. Run #2, ID `38021982095`, failed: static and original-input recovery passed; all four baseline jobs failed in interface setup; their native evaluation steps were skipped. All four logs contain `Cannot import 'flit_core.buildapi'` after obtaining `external/act_dr6_lenslike`. Collector failed completeness. Reported CamSpec/EDE job: `114124874775`; other jobs: `114124874735`, `114124874759`, `114124874765`. Run #1 also reports failure, but its cause was not inspected in this repair.

FAILED: Q045 V1 editable ACT lensing installation with `--no-build-isolation` and no flit_core dependency.
CAUSE: At frozen ACT lensing commit `b386ddbb5821c1216c709f051c9289292f174d30`, `pyproject.toml` declares `flit_core >=3.2,<4` and backend `flit_core.buildapi`. Disabling build isolation makes the caller responsible for supplying it. V1's requirements omitted it. The earlier Q041 setup allowed pip build isolation; V1 introduced the omission by disabling it.
FIX: Add exactly `flit_core==3.12.0`, retaining all nine scientific package pins; import/version/PEP660 gate before editable installations. CLASS, model, likelihood definitions, physical inputs, source commits, data and precision are unchanged.
KNOWN GOOD (LOCAL BUILD MECHANISM ONLY): The same backend failure was reproduced in a clean local Python 3.12.14 environment; installing only flit_core 3.12.0 enabled editable installation of the frozen ACT lensing source subset (metadata/module files retrieved directly at its commit). Actual V2 backend preflight passed. Wheel SHA256: `e7a0304069ea895172e3c7bb703292e992c5d1555dd1233ab7b5621b5b69e62c`. This is not a full likelihood/data test; GitHub remains Python 3.11.16 and its complete restored environment must still pass all gates.

SUPERSEDE the executable V1 target with Q045-BASELINE-V2 in the prepared registry; V1 status becomes SUPERSEDED and is rejected by the unchanged launcher. Preserve V1 files, run and artifacts as technical history. Other registry entries are unchanged. README's current target and failure boundary are updated differentially.

KEEP all scientific boundaries: Q042/Q044 closed inconclusive; Q045 proposed; four native FULL start-index-0 diagnostic points only; no reference treatments, optimization, posterior inference, production restart or model promotion. All acquired outputs remain RAW_NOT_QUALIFIED and FINAL_RESULT_GATE remains UNRESOLVED. No hypothesis was tested by the failed setup.

NEXT REQUIRED ACTION: Upload the complete V2 files at their stated paths, replace the canonical registry/README/journal/handoff, and launch only Q045-BASELINE-V2 through 🚀 BUBBLEVERSE START. Return the final JSON and worker artifacts to ingestion, including any newly failed gate. The assistant has neither modified GitHub nor dispatched this target.

## Technical source continuity

Run: https://github.com/Morfindien/Bubbleverse/actions/runs/38021982095
Reported job: https://github.com/Morfindien/Bubbleverse/actions/runs/38021982095/job/114124874775
Backend declaration: https://github.com/ACTCollaboration/act_dr6_lenslike/blob/b386ddbb5821c1216c709f051c9289292f174d30/pyproject.toml
Prior working installation route: `q041_setup_v13.sh`, retained frozen file hash in the contract.
The GitHub connector supplied primary logs/source files; local Python supplied the isolated build reproduction. No new external scientific source ID or physical claim is created.

---

## COMPLETE PREVIOUS AUTHORITATIVE JOURNAL — VERBATIM

# BUBBLEVERSE — OVERLEVERING

STATUS: CONTINUES — LOCAL EXECUTION PACKAGE PREPARED; NOT EXECUTED.
CURRENT Q: Q045 / Q-045, PROPOSED; CANONICAL SCIENTIFIC REGISTRATION PENDING.
STAGE RECORD: I-Q045-EXECUTION-BASELINE-PREPARATION-001.
DATE AND TIME: 2026-10-10T05:35:47.154976+02:00 (Europe/Copenhagen; runtime clock).
SELECTED NEXT ENGINE: Result Ingestion & Routing Engine after the bounded baseline acquisition.
PROGRAM_ID: Q045-BASELINE-V1.
WORKFLOW_DISPATCH_PERFORMED: false.
REMOTE_WRITES_PERFORMED: false.
REMOTE_PROGRAM_REGISTRATION: NOT_PERFORMED; prepared local registry only.
PRODUCTION_RESTART_AUTHORIZED: false.
ACTUAL COMPUTED SCIENTIFIC RESULT: NOT YET COMPUTED.
FINAL_RESULT_GATE: UNRESOLVED.

## CHATGPT-SETUPVURDERING

Primary: current Work/Codex with strong reasoning, code/files and authenticated read-only repository access. High reasoning if operator-selectable; exact active variant/effort and Astra Max menu availability are not independently verified. Capability classes C/A + H. The immediate work is a bounded code adaptation and integrity review; a frontier long-horizon campaign is unnecessary. GPT-5.6 is a suitable fallback if available with equivalent tools. Upgrade only for difficult independent reference/error qualification or a genuinely larger inference task. No model switch or delegation occurred.

## Differential journal update

KEEP the complete incoming authoritative journal, all Q/source IDs, failures, tested boundaries and accepted-model history. Incoming bytes: 556043; SHA256 `8f76d796d24cb9ac92c1ea9d62dee18914aa3a659bd15669c78b9e44149c5002`. Those exact bytes follow this section unchanged. This is the same authoritative journal identity, not a second journal.

KEEP Q044 closed epistemically inconclusive and Q042 closed inconclusive. KEEP Q045 proposed and its exact scientific question from I-Q045-MATH-OPTICAL-TRANSPORT-001. No scientific Q is created by the technical baseline stage. KEEP the inherited accepted remote boundary v0.5/R000005 through Q043; no promotion or remote synchronization is performed.

ADD [TECHNICAL EVIDENCE] Read-only inspection of `Morfindien/Bubbleverse` main at `72cf9e92fc794c122f593a77b6a555e6e97f6a2e`, recursive tree nontruncated: existing canonical launcher and registry exist; no Q045 target existed. Q041/Q042 model builders and production start rule are reused, with their file hashes frozen in the new contract. README's stale Q042-open/current-V29 front section is corrected in the prepared snapshot. Existing launcher is unchanged; Q042 V29 becomes COMPLETED in the prepared registry. Other registry entries remain as inspected.

ADD [TECHNICAL EVIDENCE] Original Q032 final artifact 9980784387 from run 33994305721 was retrieved and checked: 13161 bytes, SHA256 `dd7b069337aeee660d1c46158f78d9a81d6a0115309f6b333e8555899308d692`. It recovers CamSpec M6-S0 and HiLLiPoP M6-S2 parent records; these are seeds, not Q045 minima. No new observational evidence is inferred from retrieving them.

ADD [TECHNICAL EVIDENCE] Frozen original Q042 V1 environment artifact 10862038917, run 36133813540, head `6c44a4117449145afd0a3ae6eb238490686a8c6d`, was retrieved locally and its 278412344-byte digest verified: `162b99026d025d1021fa8a83dbf4290b7bd0c2c53917ea56cbf04f8b169bff4a`. It preserves all 18 original Q032 refinement record files, sealed preflight, full/reduced precision matrices and supports, original specification/source lock, frozen SN manifest and runtime metadata. Individual hashes of all 29 archived files are frozen in the Q045 contract. The workflow uses this acquisition source directly. Archive transport is internal; no archive is delivered to the operator.

ADD [EXECUTION DECISION] Existing numerical/HPC execution engine plus a small conventional controller is sufficient. The full 52-evaluation scalar/cumulative factorial proposal is not yet runnable responsibly. First acquire four unmodified native FULL baseline diagnostics at start index 0, via the unchanged original builders and start algorithm. The start algorithm already clips uniform-prior coordinates 5 percent inside bounds; raw Q032 parent values must not overwrite those resulting starts. Full sampled vector, fixed/derived/likelihood definitions and effective CLASS parameters are retained at runtime.

ADD [PROGRAM PREPARED] Q045-BASELINE-V1 has static, input-acquisition, four independent worker and collection jobs (seven jobs total, at most four numerical workers concurrently). Exact-key cache restore only. Pinned Python interface installation/backport is allowed; CLASS source/binary changes and missing-data downloads are forbidden. Native process cap 1200 seconds, worker job timeout 80 minutes. Caps are not runtime predictions. No checkpoint is needed for one atomic fixed-point evaluation. Failed jobs and completed independent jobs remain visible; no automatic retry or downstream dispatch occurs.

ADD [TEST PLAN] T001 package/Q/registry/launcher/README/journal; T002 original input/source/software/backend identity; T003 one finite native likelihood per FULL point; T004 complete finite native background/thermodynamics and TT/TE/EE exports; T005 exactly four compatible workers, external input identity and output hashes. Local integrity tests use synthetic fixtures and cannot validate physical accuracy. Mandatory numerical/runtime tests remain pending until GitHub execution. Package verification evidence is delivered separately as technical evidence.

UNRESOLVED Actual complete physical histories and qualified reference integration; separate hydrogen/helium trajectory qualification; original-campaign binary equivalence beyond the frozen unchanged diagnostic binary; parent-data hashes not independently present in the preserved records; calibrated scalar/cumulative treatments and their interaction; reference convergence; actual posterior/minimum decision margins. Native x_e/background export does not remove these qualifications. A PASS_NATIVE_DIAGNOSTIC_ONLY never becomes a scientific PASS.

NEXT REQUIRED ACTION: Install the individual prepared files, preserving their paths, and run only Q045-BASELINE-V1 through the permanent launcher. Return its final JSON and worker artifacts to ingestion. If blocked, route the exact failed gate; do not patch helium, change the physical model, resurrect Q040 endpoints or restart closed production.

## Source/provenance continuity

All existing K/source IDs and registers remain in the complete inherited journal below. Additional technical references: `Morfindien/Bubbleverse` inspected commit above; Q032 execution `4dc873a5e880d40858d831a3b421456728f0c032`; CLASS EDE `5a131c91d657dd9a7c6364cc45b038710f8d0d97`; official Cobaya v3.5.6 classy wrapper inspected for direct export access and component likelihood semantics. Existing dataset/version/software freezes are retained in the contract and original artifact. GitHub official Actions limits were checked on 2026-10-10: hosted jobs up to 6 h; this bounded 80-minute layout has explicit shorter process/step caps. No external HPC allocation was verified.

---

## COMPLETE INCOMING AUTHORITATIVE JOURNAL — VERBATIM

# BUBBLEVERSE — OVERLEVERING

STATUS: CONTINUES.
SELECTED NEXT ENGINE: BUBBLEVERSE — AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.
Q: Q045 — PROPOSED; [Q-ID REQUIRES CANONICALIZATION].
CASE ID: NOT DOCUMENTED.
STAGE RECORD: I-Q045-MATH-OPTICAL-TRANSPORT-001.
DATE AND TIME: 2026-10-09T19:56:34.500082+02:00 (Europe/Copenhagen; verified runtime clock).
SCIENTIFIC ANSWER: INSUFFICIENT EVIDENCE AT THE CURRENT ACQUISITION BOUNDARY.
CASE CLOSURE: NOT CLAIMED. One finite numerical acquisition is specified below.
PRODUCTION_RESTART_AUTHORIZED: false.
WORKFLOW_DISPATCH_PERFORMED: false.
REMOTE_Q_REGISTRATION: NOT_PERFORMED.

## CHATGPT-SETUPVURDERING

Current: Work/Codex with local code execution, files, authenticated read-only GitHub and primary-source web retrieval. The assistant is Codex based on GPT-6; the exact active variant and inference effort are not independently exposed. Agent catalogue entries include GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol and GPT-6 Luna with selectable reasoning in the agent interface. This does not establish the operator's account menu, scientific benchmarks or an automatic mode switch. No model switch or delegation was performed. Context and usage limits and allocated external HPC are not verified.

Recommended primary setup: current Work/Codex with a strong reasoning model at High or deeper, retaining file, repository and numerical execution access; GPT-6.1 Sol at High if selectable. Capability classes H/X + C/A. The immediate task is a small, controlled numerical experiment and source interpretation, not a full posterior campaign. A name-based frontier ranking is unsupported.

Fallback: strongest available high-reasoning configuration with equivalent source/code access and a verified numerical execution environment.
Upgrade trigger: interval reference qualification, switched helium evolution, full-prior likelihood envelopes or competing numerical controls require more reasoning than the current setup can reliably sustain. Extra reasoning cannot supply absent data.
Tools required: YES. Relevant: pinned repository reads, physical-definition primary sources, local arithmetic, complete matched numerical products. Browser, image, deployment and parallel-agent work are unnecessary.

## SAMLET JOURNAL — CURRENT EFFECTIVE UPDATE

This is an update to the same authoritative journal identity supplied for Q044. The complete incoming 524236-byte journal is preserved below, including source registers, claim maps and recovered historical records. SHA256 of those incoming bytes: 2d22b8bb6caa8bb2cec4bc74cfe4b5f6aee59adca3de336182980a74a43b730a. This current section governs routing; inherited stage-specific instructions below describe their historical stages.

Q044 remains CLOSED EPISTEMICALLY INCONCLUSIVE. Q045 remains proposed only and CONTINUES with a finite acquisition handoff. The inherited accepted remote boundary remains v0.5/R000005 through Q043; it was not promoted or reinspected as current main in this stage. No accepted scientific benchmark, mechanism, anomaly, prediction, source pin or original decision threshold changes here. No result is manufactured for the missing 20-cell inference.

### J-045-01 — Main question and present answer

For the frozen Q041 ΛCDM and n_scf=3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested tau_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?

[INSUFFICIENT EVIDENCE] A source-level numerical distinction is confirmed. Its realized physical bias, CMB response and inference materiality remain unmeasured. Neither a YES nor a NO follows from the Q044 native-functional hull. No full physical history, calibrated reference pair or relevant actual decision margin was acquired in this stage.

[NEW SOURCE-VERIFIED REFINEMENT] There are TWO conclusion-critical uses of the plus-curvature integration in the pinned backend:
1. The scalar tau_reio calibration in thermodynamics_reionization_get_tau calls array_integrate_all_spline_table_line_to_line.
2. The cumulative optical depth used for exp(-kappa) and the visibility function in thermodynamics_calculate_opticals calls array_integrate_spline_table_line_to_line. That cumulative routine also uses the plus curvature term.

Consequently a scalar-calibration-only change and a cumulative-opacity-only change are different interventions. A claimed complete optical-depth reference must specify both. A wholesale change to shared arrays.c would additionally change unrelated integrations and cannot isolate this question.

This is a numerical-method finding, not evidence of a material H0 bias or new physics.

### J-045-02 — Physical target, variables and units

Use the homogeneous Thomson depth of the frozen cosmological model, not a newly inferred astrophysical truth:

tau_T(z_a,z_b) = integral[z_a,z_b] c * sigma_T * n_e(z) / [(1+z) H(z)] dz.

Here H is the physical expansion rate in s^-1, c in m s^-1, sigma_T in m^2 and physical n_e in m^-3. The result is dimensionless. H must be evaluated from the SAME ΛCDM or n=3 EDE background; substituting a convenient ΛCDM H(z) for EDE changes physics.

Define x_e=n_e/n_H and n_H(z)=n_H0(1+z)^3. Then

tau_T(0,z_s) = c*sigma_T*n_H0 * integral[0,z_s] x_e(z)(1+z)^2/H(z) dz.

x_e includes hydrogen electrons, helium electrons and the inherited residual ionization. In a species decomposition x_e=x_HII+f_He(x_HeII+2*x_HeIII), with f_He=n_He/n_H fixed by the frozen helium abundance and mass convention. Use the fork's actual constants, not an approximate mass ratio silently substituted for them. Do not subtract the residual recombination background, omit helium, change a helium cutoff, add energy injection or replace the reionization parameterization.

Let eta be conformal LENGTH, eta=c*integral dt/a, in Mpc, with eta increasing toward today. Define the nonnegative opacity rate

q(eta) = a*n_e*sigma_T*(metres per Mpc), in Mpc^-1,
kappa_T(eta) = integral[eta,eta_today] q(u) du,
g_T(eta) = q(eta)*exp[-kappa_T(eta)], in Mpc^-1.

Hence dkappa_T/deta=-q. The native positive dkappa column names the scattering rate; it is not the derivative of depth-to-today with that orientation. CLASS's coordinate named tau must not be confused with the dimensionless optical depth tau_reio.

Residual histories, helium, endpoints and background values remain physical inputs. Numerical integration of them does not independently establish that those inputs describe the real Universe.

### J-045-03 — Native support is not an arbitrary redshift cutoff

Pinned thermodynamics_reionization_get_tau scans rows 0 through tt_size-2 with a strict less-than comparison to find the first global x_e minimum in that scanned range. If the minimum is at index 0, the function returns zero. Otherwise N=max(3,i_min), and the spline and scalar integral use rows 0 through N-1. The row i_min is excluded when i_min>=3. The final table row is excluded from the minimum search.

The native tau_table decreases as redshift increases. With h_i=eta_(i+1)-eta_i<0, the routine negates the signed integral at the end. A reference must reproduce this orientation and first compare the identical N rows and identical endpoint eta_(N-1). It must not silently integrate to eta_(i_min).

Separately report the signed endpoint contribution
E_endpoint = integral[eta_(i_min),eta_(N-1)] q(u) du
when i_min>=3. More general common-support comparisons must explicitly label their actual endpoints. The native-zero branch is a definition outcome, not a theorem that all Thomson scattering vanishes.

The minimum selector and estimated spline endpoint derivatives can change when z_reio and the history change. Record those changes. A discontinuous support switch invalidates an unqualified smooth derivative argument. Refining only a frozen spline cannot establish convergence of the underlying electron history.

### J-045-04 — Exact component discrepancy and error decomposition

For the SAME history, SAME N, SAME eta nodes and SAME spline second derivatives m_i=d^2q/deta^2, define signed functionals

J_plus = sum_i [(q_i+q_(i+1))*h_i/2 + (m_i+m_(i+1))*h_i^3/24],
J_minus = sum_i [(q_i+q_(i+1))*h_i/2 - (m_i+m_(i+1))*h_i^3/24].

The exact-real integral of that cubic spline is J_minus. With the native orientation,
F_plus=-J_plus, F_minus=-J_minus,
F_plus-F_minus = -sum_i (m_i+m_(i+1))*h_i^3/12.

The discrepancy has no universal sign when curvature changes. For zero curvature this channel vanishes. Under smooth bounded curvature, the magnitude scales no worse than a curvature bound times sum |h_i|^3/6; that is an interpolation-level statement, not a whole-history certificate.

For the converged physical-model integral R on the identical support,

b = F_plus-R
  = (F_plus-F_minus) + (F_minus-R).

The second term contains history/grid/interpolation error. Floating-point evaluation, endpoint/support error and solver validity require separate accounting. No difference between two correlated methods alone certifies the size of their common error. A corrected minus formula on a fixed grid is therefore a useful control, not automatically a qualified physical reference.

The published Q044 upper/lower native-plus hulls refer to conditional support/rail constructions. They cannot be substituted for b, a fitted tau, the realized spectrum change or a likelihood error.

### J-045-05 — Calibration is the physical bridge

Let t be identical requested tau_reio. For fixed non-reionization inputs theta, let z_plus solve native calibration and z_R solve same-definition reference calibration. Let e_plus=F_plus(z_plus)-t and e_R=R(z_R)-t be actual calibration residuals.

Exactly,
R(z_plus)=t+e_plus-b(z_plus),
R(z_R)-R(z_plus)=b(z_plus)+e_R-e_plus.

Thus identical requested tau does not guarantee identical realized physical depth. Nor does the curvature discrepancy at a frozen trial immediately give a spectrum difference.

If the same support branch is smooth and R'(z)>=s_min>0 throughout the root bracket, then

|z_R-z_plus| <= [|b(z_plus)|+|e_plus|+|e_R|]/s_min.

To first order, z_R-z_plus approximately equals b(z_plus)/R'(z_plus). This derivative must include the actual history response and, if allowed to move smoothly, the endpoint term. For a moving redshift endpoint z_s(z_reio),

dR/dz_reio = integral[0,z_s] W(z)*partial(x_e)/partial(z_reio) dz
             + W(z_s)*x_e(z_s)*dz_s/dz_reio,

where W=c*sigma_T*n_H0*(1+z)^2/H(z), with other physical parameters fixed. At a discrete minimum switch use piecewise brackets or interval root analysis; do not assert monotonicity or invent s_min.

Native bisection stops on a native bracket-width rule proportional to requested tau and reionization_optical_depth_tol. It is not an independent physical tau accuracy certificate. Finite, ordered brackets and a complete valid history must be checked explicitly; a nonfinite comparison or zero-iteration path cannot pass.

### J-045-06 — Visibility exposes an additional channel

Let b_N(z) be the scalar support-specific bias and b_full(eta,z) the cumulative full-table opacity bias for the same physical history. In general they differ, even where their integration domains overlap, because their spline boundary conditions and supports differ.

At the scalar support endpoint, schematically and only after exact support alignment,

kappa_plus(z_plus)-t = e_plus-b_N(z_plus)+b_full(z_plus).

Calibration can partly compensate the scalar bias while leaving a cumulative-opacity bias. Common-backend cancellation is not guaranteed, and scalar agreement alone does not certify the visibility function.

For a fixed q history and a changed cumulative integral,
g_R/g_plus = exp[kappa_plus-kappa_R].
A calibration-induced change also changes q, and must be evaluated as a new physical-model history. Separate both effects experimentally.

High-ell primary screening roughly scales as exp(-2*tau), so the first-order fractional primary-power response is approximately -2*delta_tau at fixed primordial amplitude and other relevant inputs. Low-ell EE and TE also depend on the reionization history. These are sanity estimates only; lensed spectra, TE zeros, lensing observables, parameter compensation and native likelihood response prevent them from supplying a decision certificate. The Planck reionization paper supports the screening/polarization context, not a current frozen-fork tolerance.

### J-045-07 — Native likelihood and scientific-margin relationship

Evaluate ell_a,m,c directly for each arm a, model m and dataset combination c, at identical full cosmological/nuisance vectors, using each frozen native likelihood. Within each arm and model define delta_ell=ell_counterfactual-ell_native. Do not subtract cross-arm absolute likelihoods or multiply two overlapping Planck likelihoods.

If a likelihood term is exactly Gaussian with fixed covariance C, r=D-M_plus and d=M_counterfactual-M_plus, then

delta_chi2 = -2*r^T*C^-1*d + d^T*C^-1*d,
|delta_ell| <= ||r||_(C^-1)*||d||_(C^-1) + (1/2)||d||_(C^-1)^2.

This does not apply unchanged to parameter-dependent covariance or non-Gaussian likelihoods. Use exact native evaluations there. Percent spectral changes and a synthetic covariance are not substitutes for native data weighting. Preserve physical units, C_ell/D_ell conversions, frequency/nuisance conventions and every observable consumed, including lensing and external-distance terms where required.

For fixed-point within-arm model improvement D_a=q_a,LCDM-q_a,EDE, q=-2*ell, evaluation errors bounded by b_a,m give
|delta D_a|<=b_a,LCDM+b_a,EDE.
This becomes a best-fit decision bound only with a qualified same-domain likelihood envelope and separate optimizer uncertainty. Comparing start-vector objectives does not compare best fits.

Retain J-044-05–09: whole-support likelihood oscillation w gives TV<=tanh(w/4); bounded-prior mean error <=R_x*TV; width error <=R_x*sqrt(TV); three-grid overlap error bounds; and separate objective-offset/optimizer bounds. Those derivations remain conditional. Exact finite-point likelihood differences do not supply a uniform w or posterior means.

Original rules remain unchanged: standardized-location threshold 1; overlap 0.50 on 64/80/96 grids; within-arm DeltaChi2 categories <=2, (2,6), >=6; preference portability requires different categories and absolute improvement difference >=2. These are operational predicates, not Gaussian significance or Bayes factors.

No actual original decision margins are available in qualified products here. A finite-point effect can establish an observable-level counterexample or a threat requiring new qualification. It cannot alone establish a changed posterior preference. A negligible-at-diagnostic-points result cannot establish global safety. There is no universal positive tau tolerance independent of actual margins.

### J-045-08 — Controls and checks actually completed

Source recovery: complete pinned arrays.c, thermodynamics.c, original science specification, source lock and production V1 were read. Their SHA256s match the inherited arrays/thermodynamics/spec/lock identities. The cumulative integral call path and the scalar endpoint semantics were inspected directly. The complete pinned execution tree was non-truncated; no committed V31 complete-history product was located. The journal explicitly records V31 as LOCAL_NOT_COMMITTED, with no asserted remote numerical run. The archived readiness record remains historical and does not reopen Q042.

The V29 point ini was read only as prerequisite lineage. Its requested tau=0.022146719553358576 is a diagnostic input, not a current fitted value, optimum, representative EDE vector or qualified calibration result. It supplies neither a complete matched two-model reference set nor nuisances/priors for this investigation.

Independent arithmetic control used exact Python Fraction calculations, not floating-point cosmology:
- Illustrative R(z)=z/100, t=3/50, b=1/1000: native z=59/10, reference z=6 and realized depth change=1/1000 satisfy the calibration identity exactly. These invented rational constants are explicitly a mathematical example, not physical inputs.
- Exact rational checks of (r-d)^2-r^2=d^2-2*r*d passed.
- A constant log-likelihood offset 1/4 in only the EDE model leaves its normalized posterior shape unchanged but shifts an illustrative within-arm improvement from 2 to 5/2, crossing a category boundary. This verifies why posterior-shape agreement does not certify preference.
All three controls passed. A dedicated symbolic package was unavailable; no symbolic-service execution is claimed.
No Q044 fixture campaign, physical history run, CMB calculation, likelihood evaluation, optimizer, posterior or sampler was rerun.

### J-045-09 — Exact finite discriminating acquisition

ONE NEXT TASK: obtain a bounded matched calibration/cumulative-opacity factorial test, with reference uncertainty and explicit scope, before any full inference.

Prospective diagnostic domain:
- Four FULL-contract points: the original frozen start-index-0 full cosmological/nuisance vector for each of camspec/lcdm, hillipop/lcdm, camspec/ede_n3 and hillipop/ede_n3.
- Recover them through the pinned q042_production_v1.py build_info/production_start route, q042_planck_portability_v11.py, its q041 dependency and locked Q032 parent objects. Inspect and freeze every emitted sampled, derived/fixed and nuisance input, complete prior definition and reference hash BEFORE looking at counterfactual output.
- These are diagnostic STARTS, never reconstructed minima. Duplicate physical vectors may share a theory evaluation only after complete identity equality; nuisance likelihoods remain separate.
- No substituted posterior means, incomplete optimizer records, invalid Q040 points, ad hoc midpoint guesses or replacement points after failure. If an input component or locked parent cannot be recovered, the identity gate fails finitely. The failing V29 point may document a prerequisite failure separately; it is not silently added as an eligible reference.

Treatments (calibration flag, cumulative-opacity flag):
00: original native scalar plus and original native cumulative plus.
10: same-support reference scalar calibration, native cumulative plus.
01: native scalar calibration, same-history reference cumulative opacity.
11: reference scalar calibration and reference cumulative opacity.

Primary literal scalar-functional answer is the 10-minus-00 contrast. The 01 contrast isolates opacity/visibility transport. The 11 contrast measures the total Thomson-integration channel, and
Y11-Y10-Y01+Y00 reports interaction for each spectrum/likelihood quantity Y.
Do not label 11-minus-00 a scalar-only change. This definition resolves the two call paths without changing the scientific question or hiding an additional intervention.

Patch scope:
- Preserve the original pin/binary unmodified for 00.
- New documented counterfactual versions may alter only Thomson-depth evaluation at the reionization-calibration call and the cumulative Thomson-depth evaluation used in thermodynamics_calculate_opticals, according to those flags.
- Do not globally replace array routines; drag/damping/background/other integrals stay untouched. No helium treatment, lower-branch fall-through repair, cosmology, requested tau, nuisance, prior, dataset, width, support-selector or cutoff change is part of this test.
- Recover exact original binary/config/compiler identities; record exact patch and resulting binary hashes before execution. Missing identities fail the baseline-reproduction gate.
- If valid complete histories require another physics/solver repair, this isolated experiment is BLOCKED. Record the failure and stop; do not merge that repair into the optical-depth contrast.
- Never resume an old likelihood-containing sampler checkpoint under a new binary.

Reference qualification and separation:
- First evaluate plus, exact-spline minus and independently integrated Thomson depth on the IDENTICAL complete history and native support, with units/orientation and helium/residual accounting explicit.
- Independently cross-check eta-space and redshift-space reference integrals. Their common dependence on the history must be included in the uncertainty.
- Keep the native output grid fixed for the causal contrast. Additional reference nodes and tighter internal evolution are numerical-reference diagnostics and must not replace original native inputs silently.
- Regenerate complete histories at three prospectively frozen reference accuracy levels: baseline, then halved, then quartered relevant thermodynamics integration error controls and reference integration spacings. Freeze exact knobs, baseline values, handling of discrete events and output-grid projection before results. Record every change; comparison at a refined level uses a matched native/control treatment at that level.
- Three agreeing levels are only an empirical convergence diagnostic. A qualified reference needs a defensible remainder bound, supported asymptotic regime or validated residual/error enclosure, including switched-event validity. If that cannot be justified, label reference uncertainty UNQUALIFIED.
- Preserve same native support-selection semantics during calibration; evaluate every fixed-history contrast on identical support first. Report support drift as a separate endpoint term, plus common-endpoint recalculations. Do not use a smooth calibration formula through a discrete selector jump.
- Record requested tau, native reported tau, independently realized same-support depth, full cumulative kappa, z_reio, x_e species/history validity, support indices, endpoints, bisection residual/bracket and numerical uncertainty.

Finite work bound:
- Up to 4 diagnostic points x 4 treatments x 3 matched accuracy levels = 48 theory evaluations, plus one independent repeat of each original 00 baseline for reproducibility: at most 52 theory evaluations before the gate review.
- Independent quadrature evaluations on stored valid histories do not require additional theory jobs.
- At each completed theory point, evaluate each of the five existing external combinations with the unchanged native arm/parameters where their product definitions permit exact reuse. This is 20-point/combinations coverage at fixed diagnostic vectors, not 20 posterior cells. Theory reuse must follow verified likelihood requirements; no accidental omission of an observable is allowed.
- No adaptive domain expansion, new optimizer start, sampler, arbitrary rerun or fourth refinement is authorized by this finite specification. An unresolved gate records its actual reason and hands back evidence for a new decision, rather than assuming more runtime will fix it.

Minimum products:
identity manifest; all 00 raw successes/failures; exact counterfactual patch/build identities; complete species/background/thermodynamic histories; same-support scalar and cumulative quadrature differences with uncertainty; TT/TE/EE and every consumed native observable; per-component and total native likelihood values; factorial contrasts; numerical-response intervals; explicit point/support/combination coverage; missing products and preserved failures. Hash each product and its parent inputs.

Prospective decision and stop gates:
A. Missing identity, invalid history, nonfinite bracket, missing observable, inadmissible reference or unqualified uncertainty -> STOP with INSUFFICIENT EVIDENCE and the exact failed prerequisite. A failed baseline is not an EDE/LCDM falsification.
B. A resolved finite-point spectrum/likelihood perturbation -> record its signed size, interval and domain. It establishes sensitivity, not automatic decision materiality.
C. If actual qualified original decision products/margins can be recovered, propagate errors through the unchanged J-044 interval predicates. A certified threshold crossing or inability to exclude one is reported at its warranted inferential scope. Do not reinterpret pointwise DeltaChi2 as optimized model preference.
D. If no actual margin can be recovered, report CONDITIONAL numerical sensitivity or INSUFFICIENT EVIDENCE for margin materiality. No replacement tolerance is guessed.
E. A NO/global-negligibility claim requires justified full-domain/support/tail coverage and relevant optimizer/sampling qualification; these four vectors cannot pass that gate by themselves. Stop the bounded acquisition and report the limitation rather than initiating the old full production.
F. End this acquisition when the 52-evaluation bound or a terminal gate is reached. Return evidence for ingestion. If no additional obtainable evidence could change the narrower answer at the documented boundary, then close Q045 epistemically and send the complete same-identity journal to Motor14. This mathematical stage itself does not claim that closure.

No launcher, PROGRAM_ID, GitHub mutation or production dispatch is created here. The receiving execution engine must make the finite experiment concrete and resolve the outstanding execution authority before any remote dispatch. This document is an exact scientific acquisition specification, not permission to run the historical campaign.

## AKTUEL OVERLEVERING

Remaining conclusion-critical uncertainty: the realized calibrated history/visibility/spectrum/native-likelihood response to the isolated integration channel, together with defensible reference uncertainty and its relationship to actual original decision margins.

Why the execution engine: the equations, causal factors, exact source paths and finite stopping gates are now specified. Further algebra cannot supply missing complete matched physical products. Execute or concretely diagnose the single acquisition above; do not repeat Q044 component proofs, generic qualification lists or repository maintenance as a scientific result.

Missing: exact complete diagnostic-vector/parent realization; original baseline binary/config reproduction; valid matched histories; independently qualified scalar/cumulative reference; CMB/native-likelihood contrasts; actual original decision margins; any whole-domain envelope. Each is a gate, not a free input to invent.

Preserve Q044 closure, proposed-Q045 boundary, all inherited failed paths and original 20-cell decision contract. A bounded diagnostic does not reopen Q042 or resolve CamSpec–HiLLiPoP portability.

## KILDER TIL NÆSTE MOTOR / SOURCE AND TOOL PROVENANCE

K1 — Physical Thomson depth and CMB response context.
Planck Collaboration, R. Adam et al. Planck intermediate results. XLVII. Planck constraints on reionization history. 2016. A&A 596, A108. DOI 10.1051/0004-6361/201628897; arXiv:1605.03507v3.
https://arxiv.org/html/1605.03507v3
Supports physical definitions and screening/polarization context. Does not validate this fork, supply a current tolerance or constitute new independent Planck data. Inherited ID K-Q044-M14-REION-001.

K2 — Frozen scalar and cumulative integration source.
mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97, tools/arrays.c.
https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c
SHA256 c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4; verified full recovered text.
Supports the plus-curvature formulas for both integral routes. Inherited K-Q042-INGESTDESIGN-001 is retained; this stage adds the cumulative-call claim, not an independent cosmological source.

K3 — Frozen calibration, support and visibility call path.
Same repository/pin, source/thermodynamics.c.
https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c
SHA256 d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6; verified full recovered text.
Relevant functions thermodynamics_reionization_get_tau, thermodynamics_reionization_evolve_with_tau, thermodynamics_calculate_opticals. Supports actual endpoint/first-minimum semantics, bisection and cumulative visibility dependence. Inherited K-Q042-V24-001/K-Q042-DESIGN-001 refer to the same file and are not independent sources.

K4 — Corrected upstream comparison.
lesgourg/class_public@814ce59c380a5cccd0bed1747a384ff7bfc1f9cf, tools/arrays.c.
https://github.com/lesgourg/class_public/blob/814ce59c380a5cccd0bed1747a384ff7bfc1f9cf/tools/arrays.c
Scalar excerpt independently read; upstream documents correction of the historical plus sign. Inherited full-file SHA256 1c5c1cc954a5b4c288f51a055b9aae6576f8ab3a1b083464e59a5c0432126ecd was not recomputed from this excerpt. Supports comparison methodology only; not a drop-in EDE reference.

K5 — Frozen decision contract and dependency lock.
Morfindien/Bubbleverse@72cf9e92fc794c122f593a77b6a555e6e97f6a2e:
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_spec_v1.json
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_source_lock_v1.json
Verified SHA256 respectively 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c and 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56. Supports original scientific predicates and dependency identities, not valid installed runtime or convergence. Inherited I-Q044-CONTRACT-001/I-Q044-SOURCELOCK-001.

K6 — Exact diagnostic-vector reconstruction route.
Same execution pin, q042_production_v1.py and q042_planck_portability_v11.py.
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_v1.py
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_planck_portability_v11.py
Production V1 SHA256 889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642. Directly read; full transitive Q032 parent bytes and emitted complete input vectors NOT RECOVERED in this stage. Therefore this is a precise recovery route, not a claim the required numeric input manifest already exists. Do not use builder defaults as undocumented physical measurements.

K7 — Authoritative inherited knowledge and present derivations.
Incoming Q044_SAMLET_JOURNAL, byte count/hash above, contains I-Q044-MATH-QUALIFICATION-001, Q044 component result/checks, V29/V31 provenance and complete preserved source/claim maps.
This current I-Q045-MATH-OPTICAL-TRANSPORT-001 contains the source-call refinement, physical definitions, calibration identities, causal test and exact rational checks. These are internally derived methodological evidence; no independent sky observation is added.

Tools: GitHub read connector -> pinned source/contract content -> local SHA256 and call-path inspection; primary-source web retrieval -> original Planck/CLASS context; file reader -> authoritative journal -> complete historical preservation; local Python standard library -> exact rational checks -> illustrative arithmetic only. The same source retrieved through several routes is still one source.

Evidence strength: STRONG for inspected code formulas/call paths and exact conditional identities; CANNOT BE DETERMINED WITH CURRENT DATA for the actual physical/inferential materiality.
Critical reservations: incomplete matched physical products and reference validation, additional solver failures, support switching, missing margins/domain/tails and optimizer/posterior uncertainty. No current H0 shift, EDE preference or portability class is claimed.

---

# PRESERVED INCOMING AUTHORITATIVE JOURNAL

The following incoming bytes are preserved unchanged. Their historical timestamps, source registers and results remain recoverable; current routing and Q045 stage status are defined above.


# BUBBLEVERSE — MASTER JOURNAL

AUTHORITATIVE EFFECTIVE STATE AFTER MOTOR14
Date and time: 2026-10-09T17:21:13+00:00 (UTC; runtime clock).
CURRENT CLOSED Q: Q044; established identifier preserved. CASE ID: NOT DOCUMENTED.
NEXT SCIENTIFIC QUESTION: Q045 — PROPOSED; [Q-ID REQUIRES CANONICALIZATION]
No remote Q registration, accepted-model modification, workflow dispatch or production restart occurred.

## Authority and continuity

This is a new version of the same Q044_SAMLET_JOURNAL.md identity, not a competing journal. The effective current global model below governs interpretation. The entire incoming 239491-byte journal follows unchanged as recoverable history, including all 91 inherited source objects, every later addition and all claim maps. The recovered chronological Q001–Q043 record also follows in full as historical transcription. No missing Q010 journal is invented; retrospective early reconstructions remain labelled. Publication narrative and archived instructions retain their historical dates rather than governing current routing.

The three supplied PDFs match EVD-Q043 admission hashes. Their actual chronological record reaches Q043 despite the Q001–Q042 filename. Earlier statements that all global material is unrecovered are SUPERSEDED for the supplied archive, not proof that every original raw historical artifact has been recovered.

## Current global scientific model

1. [SUPPORTED, MULTI-PROBE INFERENCE] The observable Universe is structured and dynamically evolving and has a hotter, denser past. A physical initial singularity is not established. Observation, reconstruction and interpretation remain distinct. Sources: EVD-Q043-QJOURNAL-PDF/Q001, EVD-Q043-MAINBOOK-PDF/chapters1,5; corresponding inherited primary references survive in the historical record.
2. [SUPPORTED UNDER STATED GRAVITATIONAL/COSMOLOGICAL FRAMEWORKS] Non-luminous gravitating phenomena and late acceleration are supported; a dark-matter particle and a microscopic dark-energy mechanism remain unestablished. MECH-LCDM-001 is a supported compact description, not directly observed reality. MECH-DYNDE-001 remains an active model-comparison candidate, not a detected field. Sources: accepted observations/mechanisms at dd7575e7146382957d206e87274ca6246c2587b7; supplied books.
3. [MODEL-INFERRED BENCHMARKS, NOT THREE RAW MEASUREMENTS] Preserve local distance network H0=73.50±0.81, combined Planck+SPT-3G+ACT DR6 flat-ΛCDM H0=67.24±0.35, and DESI DR2+BBN flat-ΛCDM H0=68.51±0.58, all km s^-1 Mpc^-1. These are inherited accepted benchmarks; this Motor14 run did not independently remeasure or revalidate their contemporary primary-data pipelines. Do not combine them indiscriminately or interpret a marginal Gaussian tension as detection of new physics. OBS-H0-LOCAL-001, OBS-H0-CMB-001, OBS-H0-BAOBBN-001; BENCH-H0-*; sources: archived journal/books and accepted benchmark records. Ordinary single-cause explanations rejected in historical tests remain rejected only in those scopes.
4. [ACTIVE/CONSTRAINED] MOD-EDE-N3 / MECH-EDE-N3-001, n_scf=3, can reach high-H0 regions on tested surfaces but is not an established complete solution. MECH-ME-001 (varying electron mass) remains a constrained partial mechanism. Viability depends on datasets, likelihoods, priors, optimizer basin and implementation. Corrected finite-search minima supersede older points where documented; global minima remain unproved. Sources: chronological Q004–Q016, technical appendices and accepted robustness/constraints. Historical ACT attribution stays attached to its actual frozen points.
5. [METHODOLOGICAL RESULT] Q035 resolves historical basin-label disagreement as classifier dependence. Q036–Q038 retain a distributed CamSpec–HiLLiPoP endpoint-geometry difference on matched TT support, localized minimally to omega_b, omega_cdm, f_EDE and theta_i under the tested capture rule. CTR-PLANCK-IMPL-001 and C-036-IMPL remain OPEN_NARROWED. This is overlapping-data implementation evidence, not two independent observations or a physical-systematic identification.
6. [VALIDATED CONDITIONAL NEGATIVE RESULTS] Q039 interventions reject relative calibration alone, native off-diagonal precision alone, their tested combination and native foreground-profile freedom alone as sufficient explanations. Rejecting those interventions does not identify the actual causal mechanism. Sources: EVD-Q039-IMPLBLOCK, EVD-Q039-FGPROFILE; runs34161368438/34184346582 and archived locked definitions.
7. [MATHEMATICALLY SUPPORTED OBJECT; FAILED FINITE IMPLEMENTATIONS] Q040 separately marginalizes each native nuisance space around a common physical CMB object. Laplace/Schur and defensive RQMC failed mandatory qualification before endpoints; do not revive those endpoints or interpret numerical failure as physical falsification. EVD-Q040-RQMC, run34258155387.
8. [CONTROLLED NO SCIENTIFIC RESULT] Q041 V19 obtained 0/32 documented complete converged chains; 30 reached frozen sample limits, two remained partial. Its narrower EDE-only campaign omitted ΛCDM controls/common SN and differs from the original20-cell contract. Run34979609004 success validated a terminal firewall, not cosmology. Original downstream portability remains scientific debt.
9. [CLOSED INCONCLUSIVE GENERAL FEASIBILITY] Q042 did not qualify the original20-cell matrix. V29 recovered context is prerequisite-only; V30/V31 histories were partial; the cap32 incompatibility is conditional on its append-only support representation, not universal infeasibility. No completed physical tau/prediction result is resurrected.
10. [CLOSED TECHNICAL PREPARATION; SUBSEQUENT PUBLICATION VERIFIED] Q043 originally established local candidate preparation only. Subsequent installation run37927147545 and receipt now establish accepted v0.5/R000005 through Q043. This changes repository provenance, not physical models, benchmarks or production authorization. No Q044 acceptance is implied.
11. [CLOSED EPISTEMICALLY INCONCLUSIVE] Q044 establishes support-specific adjoint real-arithmetic component bounds under the inherited hydrogen rail, source witnesses and fixed knots. R-Q044-SPLINE-ADJOINT-001 is accepted with those scope limits; R-Q044-SPLINE-INGESTION-002 preserves the evidence-boundary closure. Original downstream class remains NOT_AVAILABLE. No H0 difference, qualified equivalence, dataset-conditional conclusion or EDE/ΛCDM preference has been established.
12. [OPEN PHYSICAL VALIDITY GAP] Frozen CLASS_EDE optical-depth integration uses the historical plus curvature correction; the ordinary cubic integral uses minus. The official upstream source documents that correction. Synthetic exact/native tests establish a functional difference, not a physical optical-depth bias or inference-level effect. Error-budget relevance to CMB predictions is still unmeasured. This distinction is central to the proposed next question.

## Active tensions, predictions and unresolved state

- CTR-H0-001: OPEN inference-chain TENSION; no robust same-assumption fundamental contradiction is newly established.
- C-036-IMPL / CTR-PLANCK-IMPL-001: OPEN_NARROWED methodological implementation tension; historical IDs are cross-references, not newly independent conflicts.
- CTR-HIST-BASIN-LABEL-001: RESOLVED_METHODOLOGICALLY; do not reopen without new evidence.
- PRED-H0-INDEPENDENT-001, PRED-EDE-PORTABILITY-001, PRED-Q039-COUPLED-001: all OPEN. Q044 adds insufficient-qualification history, not a failed physical prediction.
- Open: dark-matter identity, acceleration microphysics, global topology/size beyond accessible evidence, earliest-epoch interpretation, EDE globality, causal likelihood structure, complete-history/upstream/binary reference accuracy and posterior convergence. None is resolved by this local mathematical component.

## New component result retained exactly in scope

UPPER:138 supports3195..3332; conditional native-plus hull [0.70676532823050475,0.7067869701940579]; width2.1641963553142851e-05.
LOWER:3002 supports331..3332; conditional native-plus hull [0.0016297839913017342,0.0018091545475532051]; width0.00017937055625147098.
Values are dimensionless component enclosure extrema, not measured optical depths. Source boxes are correlated physically; independent-box extrema can be conservative/unattainable.64 rational fixtures and18 native-C diagnostics passed in the received result, not rerun here.17 V29 members matched in the received recovery. Uniform original-binary rounding, full history/grid accuracy and physical/inferential adequacy remain UNRESOLVED. No more fixture repetition is prescribed.

## Revision actions

ADD: scoped component knowledge and its accepted epistemic closure; prospective physical-validity question.
REFINE: distinguish exact-real native functional bounds from physical Thomson depth and from posterior qualification.
UPDATE: current repository accepted v0.5/R000005/Q043; full global archive now accessible.
SUPERSEDE: stale current-state v0.4-only/no-promotion descriptions and generic repeat-design/ingestion instructions. Preserve their historical truth.
KEEP: scientific benchmark values and uncertainties; all physical model/candidate statuses; all source IDs/claim mappings; rejected scoped mechanisms; contradictions and open predictions.
No active physical hypothesis or prediction is deleted by Q044; no independent cosmological evidence is added.

## Dependency propagation and scientific debt

The conditional hull clears only a representation/storage subproblem. It does not clear reference accuracy -> CMB prediction accuracy -> native likelihood accuracy -> posterior/model-decision qualification. Every downstream result relying on an unqualified physical reference remains unqualified; original scientific thresholds stay frozen. Earlier validated geometry is not retroactively invalidated merely by an unmeasured potential integration effect.
Originating casesQ041–Q042; carried throughQ043–Q044: materiality/portability of likelihood-dependent H0/EDE inference remains unresolved. Storage representation is PARTIALLY CLEARED; complete-history, physical functional, binary arithmetic, likelihood transport and convergence blockers remain ACTIVE. Resume one distinct science subquestion; do not reopen Q044's completed bounded audit or dispatch the old production campaign.

## Prioritized scientific backlog

SELECTED HIGH — Q045 — PROPOSED; [Q-ID REQUIRES CANONICALIZATION]: For the frozen Q041 ΛCDM and n_scf = 3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested τ_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?
Reason: tests a specific known numerical/physical distinction at the shared backend, with possible consequences for both model branches and both likelihood arms. A demonstrated material effect would require new qualification of affected scientific outputs; a controlled negligible effect would eliminate this particular threat within its tested domain. It would not resolve other accuracy channels or Q044's full posterior question. Start: BUBBLEVERSE — AUTONOMOUS MATHEMATICS ENGINE.
HIGH, existing prediction PRED-EDE-PORTABILITY-001: original20-cell H0/model portability; deferred scientific debt, not newly numbered/reworded as Q045.
HIGH, existing prediction PRED-Q039-COUPLED-001: whether valid coupled native-likelihood harmonization accounts for the residual geometry; preserve prior failed routes and native spaces. Start when warranted: documented research/consistency specialist according to exact remaining bottleneck.
HIGH, existing PRED-H0-INDEPENDENT-001: an observationally independent H0 inference able to discriminate chains; no new measurement or claim of available1% data is supplied here. Start: documented research.
MEDIUM: remaining finite-search EDE globality/robustness questions in the historical backlog; do not confuse finite minimizer success with global proof. Broad unformulated microphysical unknowns remain background uncertainties, not fabricated numbered tasks.
Priority selection is conditional on the documented backend validity gap; it is not a claim that this gap is a measured dominant systematic. No new direct robust contradiction outranks it in the supplied state.

## Scientific question firewall and ID boundary

PASS: scientific object is reionization/optical depth, CMB spectra and scientific likelihood inference; answer is constrained by mathematics, reference calculations and data-weighted response; yes/no/conditional/insufficient-evidence endpoints change qualification status; wording assumes no effect; no maintenance endpoint. Q045 tests a specific functional-to-observable consequence, whereas Q044 asked for the full cross-arm posterior/model classification.
Q044 is the preserved operator scientific identifier; remote authoritative boundary endsQ043 and does not admitQ044. Q045 is proposed only; reconcile/admit canonical numbering before registration. Never reuseQ044 or pretendQ045 is registered. This ID prerequisite must not be made into a universe question.

## Non-Q technical follow-up

Record Q044 closure and this revision in the controlled model-update route when authorized; source README/registry synchronization remains separate pending work. Do not overwrite accepted snapshots or change source pins. Complete matched histories/reference products and a quantitative inference-error bridge are execution prerequisites for the selected scientific question. No blanket production authority is granted. No new PROGRAM_ID or launcher target is created in Motor14. Repository contents are unchanged.

## Source/claim supplement

All inherited sources and mapping trees below remain intact. The accepted model state is scientific-project synthesis, not independent evidence. Publication sources remain primary where actually documented; archival references not newly verified retain their limitations, including the book's explicit K-033 verification gap. Newly checked historical reionization/CLASS literature supplies method context only, not new parameter values or a calibrated Bubbleverse accuracy target.

```json
{
  "new_source_records": [
    {
      "source_id": "I-Q044-M14-REPOSITORY-001",
      "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
      "title": "Motor14 read-only accepted-state, installation and source-pin audit",
      "date_utc": "2026-10-09T17:21:13+00:00",
      "repository": "Morfindien/bubbleverse-model",
      "commit": "dd7575e7146382957d206e87274ca6246c2587b7",
      "files": [
        "accepted/model_state.json",
        "accepted/observations.json",
        "accepted/constraints.json",
        "accepted/contradictions.json",
        "accepted/mechanisms.json",
        "accepted/predictions.json",
        "versions/accepted/v0.5/parameters.json",
        "versions/accepted/v0.5/benchmarks.json",
        "versions/accepted/v0.5/assumptions.json",
        "versions/accepted/v0.5/uncertainty.json",
        "evidence/evidence_registry.json",
        "evidence/q_updates/Q043.json",
        "provenance/Q043_REMOTE_INSTALLATION_RECEIPT.json",
        "README.md"
      ],
      "execution_repository": "Morfindien/Bubbleverse",
      "execution_head": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "installation_run_id": 37927147545,
      "independent_cosmological_evidence": false,
      "supports": "Current accepted v0.5/R000005 boundary Q001–Q043; Q043 promotion is technical only; unchanged production prohibition; repository/journal metadata divergence."
    },
    {
      "source_id": "K-Q044-M14-REION-001",
      "type": "EXTERNAL PRIMARY SCIENTIFIC PUBLICATION",
      "authors": "Planck Collaboration, R. Adam et al.",
      "title": "Planck intermediate results. XLVII. Planck constraints on reionization history",
      "year": 2016,
      "journal": "Astronomy & Astrophysics 596, A108",
      "arxiv": "1605.03507v3",
      "doi": "10.1051/0004-6361/201628897",
      "url": "https://arxiv.org/html/1605.03507v3",
      "relevant_sections": "3; 4.1; Appendix B",
      "retrieval_method": "Primary arXiv metadata and HTML, targeted source verification",
      "supports": "Optical-depth/history sensitivity and CMB polarization/parameter dependence justify an observable-level validity question. This source does not establish the bias of the frozen Bubbleverse fork.",
      "independence": "Historical Planck-based work; overlaps the Planck evidence family, not independent confirmation of Bubbleverse results.",
      "caveat": "Historical ΛCDM/reionization analysis; no imported tau tolerance, posterior or current-EDE verdict."
    },
    {
      "source_id": "K-Q044-M14-CLASS-001",
      "type": "EXTERNAL PRIMARY TECHNICAL PUBLICATION",
      "authors": "Julien Lesgourgues",
      "title": "The Cosmic Linear Anisotropy Solving System (CLASS) I: Overview",
      "year": 2011,
      "arxiv": "1104.2932v2",
      "url": "https://arxiv.org/abs/1104.2932v2",
      "retrieval_method": "Primary arXiv metadata/abstract verification",
      "supports": "CLASS output-accuracy control and modular numerical architecture; contextual method only.",
      "caveat": "General overview does not validate the pinned CLASS_EDE fork or give a Bubbleverse error budget."
    },
    {
      "source_id": "K-Q044-M14-CLASS-002",
      "type": "EXTERNAL PRIMARY TECHNICAL PUBLICATION",
      "authors": "Diego Blas, Julien Lesgourgues, Thomas Tram",
      "title": "The Cosmic Linear Anisotropy Solving System (CLASS) II: Approximation schemes",
      "year": 2011,
      "arxiv": "1104.2933",
      "doi": "10.1088/1475-7516/2011/07/034",
      "url": "https://arxiv.org/abs/1104.2933",
      "retrieval_method": "Primary arXiv metadata/abstract verification",
      "supports": "Context for precision/approximation qualification, not a certificate of this frozen implementation.",
      "caveat": "No numerical tolerance adopted from this abstract."
    }
  ],
  "recovered_archive_records": [
    {
      "source_id": "EVD-Q043-QJOURNAL-PDF",
      "filename": "Bubbleverse_Q-Journals_Q001-Q042.pdf",
      "size_bytes": 1192715,
      "sha256": "c87270ed88b5b0994cd83d94305d915c55a4783c650c321ce784f5904447eb04",
      "source_type": "BUBBLEVERSE HISTORICAL SYNTHESIS",
      "independence": "Archive of prior evidence, not an independent observation",
      "status": "Recovered attachment identity matches current Q043 GitHub admission metadata"
    },
    {
      "source_id": "EVD-Q043-APPENDICES-PDF",
      "filename": "Bubbleverse_Technical_Appendices_A-D.pdf",
      "size_bytes": 635977,
      "sha256": "e3c21469cc7a53c51a2800146396c2cfcd8872154b6701d9f88668d965c833a7",
      "source_type": "BUBBLEVERSE HISTORICAL SYNTHESIS",
      "independence": "Archive of prior evidence, not an independent observation",
      "status": "Recovered attachment identity matches current Q043 GitHub admission metadata"
    },
    {
      "source_id": "EVD-Q043-MAINBOOK-PDF",
      "filename": "Bubbleverse_Main_Book.pdf",
      "size_bytes": 1370169,
      "sha256": "507945a2549c26e56f894a4fca5e9115682c242fcccda66f7b9b6b89dae33b05",
      "source_type": "BUBBLEVERSE HISTORICAL SYNTHESIS",
      "independence": "Archive of prior evidence, not an independent observation",
      "status": "Recovered attachment identity matches current Q043 GitHub admission metadata"
    }
  ],
  "new_claim_to_source_map": {
    "C-Q044-M14-01": {
      "claim": "Conditional real-arithmetic functional bounds add component knowledge without a qualified cosmological result.",
      "sources": [
        "I-Q044-SPLINE-ADJOINT-001",
        "I-Q044-SPLINE-CHECKS-001",
        "I-Q044-SPLINE-INGESTION-002"
      ]
    },
    "C-Q044-M14-02": {
      "claim": "Q043 is currently accepted as v0.5/R000005, while Q044 is not remotely admitted.",
      "sources": [
        "I-Q044-M14-REPOSITORY-001",
        "EVD-Q043-RESULT"
      ]
    },
    "C-Q044-M14-03": {
      "claim": "The global historical record is now accessible; Q010 remains explicitly absent and early retrospective status survives.",
      "sources": [
        "EVD-Q043-QJOURNAL-PDF",
        "EVD-Q043-MAINBOOK-PDF",
        "EVD-Q043-APPENDICES-PDF"
      ]
    },
    "C-Q044-M14-04": {
      "claim": "The frozen plus functional and ordinary cubic integral differ; their cosmological importance remains unmeasured here.",
      "sources": [
        "K-Q042-INGESTDESIGN-001",
        "K-Q042-INGESTDESIGN-002",
        "I-Q042-INGESTDESIGN-001",
        "I-Q042-REFQUAL-001",
        "I-Q044-NATIVE-PIN-RECHECK-001"
      ]
    },
    "C-Q044-M14-05": {
      "claim": "A distinct prospective optical-depth-to-CMB validity question has scientific information value; no answer is claimed.",
      "sources": [
        "C-Q044-M14-01",
        "C-Q044-M14-04",
        "K-Q044-M14-REION-001",
        "I-Q044-CONTRACT-001"
      ]
    }
  },
  "current_repository_snapshot": {
    "accepted/contradictions.json": {
      "contradictions": [
        {
          "description": "High local H0 conflicts with lower CMB and BAO+BBN inferences.",
          "id": "CTR-H0-001",
          "resolution": "Unresolved through Q040; preserve chain distinctions and dependencies.",
          "results": [
            "OBS-H0-LOCAL-001",
            "OBS-H0-CMB-001",
            "OBS-H0-BAOBBN-001"
          ],
          "status": "OPEN"
        },
        {
          "description": "CamSpec and HiLLiPoP produce materially different fitted endpoint geometry on overlapping Planck PR4/NPIPE information.",
          "history": [
            {
              "note": "Feasibility closure gives no physical downstream verdict; methodological implementation tension preserved.",
              "q": "Q042",
              "status": "OPEN_NARROWED"
            }
          ],
          "id": "CTR-PLANCK-IMPL-001",
          "resolution": "Q039 excludes several simple single-block explanations. Q040 identifies a legitimate common physical CMB-space nuisance-marginalization route, but tested finite numerical representations fail validation before endpoint geometry. Q041 V19 then attempts direct downstream portability with matched external data, but the required complete converged posterior matrix is not obtained, so no physical downstream class is issued. The causal origin and downstream scientific significance remain unresolved; V19 is also narrower than the broader original Q041 contract.",
          "results": [
            "ROB-PLANCK-GEOM-001",
            "ROB-Q039-001",
            "ROB-Q040-CMB-MARGINAL-001",
            "ROB-Q040-NUMERIC-001",
            "ROB-Q041-CONTROLLED-NOSCIENCE-001",
            "ROB-Q041-FIREWALL-001",
            "ROB-Q041-CONTRACT-SCOPE-001"
          ],
          "status": "OPEN_NARROWED"
        },
        {
          "description": "Historical stable vs later non-stable basin labels appeared contradictory.",
          "id": "CTR-HIST-BASIN-LABEL-001",
          "resolution": "Crosswalk showed classifier dependence rather than demonstrated disappearance of classifier-invariant geometry.",
          "results": [
            "ROB-CLASSIFIER-001"
          ],
          "status": "RESOLVED_METHODOLOGICALLY"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "accepted/constraints.json": {
      "constraints": [
        {
          "id": "CON-H0-001",
          "statement": "The H0 conflict must be preserved as disagreement among distinct inference chains, not averaged into one raw measurement.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-H0-002",
          "statement": "The H0 Distance Network versus combined CMB benchmark differs by about 7.1 sigma under the manuscript's simple marginal Gaussian comparison; this is not a 7.1 sigma detection of new physics.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-H0-003",
          "statement": "DESI DR2 + BBN supplies a separate lower-H0 route without CMB anisotropy data, while retaining early-universe and sound-horizon model dependence.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-SYSTEMATICS-001",
          "statement": "No tested ordinary single systematic in the authorized state reconciles the complete local, CMB, and BAO+BBN evidence by itself.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-EDE-001",
          "statement": "Moving H0 upward is insufficient; n=3 EDE must satisfy the complete likelihood structure and its viability is experiment- and likelihood-dependent.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-GLOBALITY-001",
          "statement": "Corrected high-H0 EDE basins are best-observed finite-search solutions, not proven mathematical global minima.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q039-001",
          "statement": "Relative-calibration neutralization, removal of native off-diagonal precision coupling, their tested combination, and native foreground profiling freedom do not individually remove the CamSpec-HiLLiPoP geometry discrepancy under the locked Q039 conditions.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q039-002",
          "statement": "Q039 does not identify a physical Planck calibration error, foreground contamination, covariance defect, instrumental failure, likelihood superiority, EDE preference/falsification, or new physics.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-DM-IDENTITY-001",
          "statement": "The microscopic identity of dark matter remains unresolved through Q040.",
          "status": "OPEN"
        },
        {
          "id": "CON-ACCEL-ORIGIN-001",
          "statement": "The physical origin of late-time acceleration remains unresolved through Q040.",
          "status": "OPEN"
        },
        {
          "id": "CON-Q040-001",
          "statement": "The Q040 common-CMB nuisance-marginalization bridge cannot establish whether the CamSpec-HiLLiPoP discrepancy disappears or survives physically because numerical validation failed before endpoint geometry was produced.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q040-002",
          "statement": "Q040 does not establish likelihood defect or superiority, calibration, foreground, covariance or instrumental failure, n=3 EDE preference/falsification, or new physics.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q041-001",
          "q_introduced": "Q041",
          "statement": "No MATERIAL_DOWNSTREAM_DIFFERENCE, SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS, or CONSTRAINED_MIXED conclusion may be assigned from V19 because the chain-completeness, hard-Rhat, and both-arms/all-combinations science gates were not satisfied.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q041-002",
          "q_introduced": "Q041",
          "statement": "Q041 non-convergence and a green workflow terminal state are not physical evidence for CamSpec-HiLLiPoP agreement or disagreement, likelihood superiority, EDE preference or falsification, or new physics.",
          "status": "ACTIVE"
        },
        {
          "id": "CON-Q041-003",
          "q_introduced": "Q041",
          "statement": "Q041 conclusions are restricted to the preregistered V19 EDE-only campaign and must not be generalized to the broader original downstream contract.",
          "status": "ACTIVE"
        },
        {
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "CON-Q042-001",
          "q_introduced": "Q042",
          "statement": "No posterior portability class, model preference, physical falsification, pipeline superiority or new physics follows from Q042. The original 20-cell scientific comparison remains unqualified.",
          "status": "ACTIVE"
        },
        {
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "CON-Q042-002",
          "production_restart_authorized": false,
          "q_introduced": "Q042",
          "statement": "Unchanged V31 reruns, more time alone and retrospective cap increases are not a sufficient qualified repair. A materially different design requires a new-case or explicit reopening decision; none is authorized here.",
          "status": "ACTIVE"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "accepted/mechanisms.json": {
      "mechanisms": [
        {
          "id": "MECH-LCDM-001",
          "name": "flat LCDM",
          "scope": "Highly successful compact cosmological description; not identical to underlying reality and does not identify microscopic dark matter/dark energy.",
          "status": "SUPPORTED"
        },
        {
          "id": "MECH-DYNDE-001",
          "name": "dynamical dark energy",
          "scope": "Model-comparison candidate; not directly observed as a changing field.",
          "status": "ACTIVE"
        },
        {
          "active": true,
          "id": "MECH-EDE-N3-001",
          "name": "n=3 early dark energy",
          "scope": "Can access higher-H0 regions in tested profiles, but viability is strongly dataset-, likelihood-, basin-, and implementation-dependent; not established as a complete Hubble-tension solution.",
          "status": "CONSTRAINED"
        },
        {
          "active": true,
          "id": "MECH-ME-001",
          "name": "varying electron mass",
          "scope": "Can reduce the drag-epoch ruler and move H0 upward in tested profiles, but transfers positive fit cost notably into BBN/DESI at high H0; not established as a complete solution.",
          "status": "CONSTRAINED"
        },
        {
          "id": "MECH-LOCAL-SINGLE-CAUSE-001",
          "name": "tested ordinary local single-cause systematics",
          "scope": "Can shift local inference but no tested ordinary single cause accounts for the full local/CMB/BAO+BBN discrepancy.",
          "status": "REJECTED_AS_FULL_EXPLANATION"
        },
        {
          "id": "MECH-Q039-CAL-001",
          "name": "relative calibration as sole CamSpec-HiLLiPoP geometry explanation",
          "scope": "Rejected as sufficient under Q039 locked intervention.",
          "status": "REJECTED_AS_FULL_EXPLANATION"
        },
        {
          "id": "MECH-Q039-PREC-001",
          "name": "native off-diagonal precision coupling as sole explanation",
          "scope": "Rejected as sufficient under Q039 locked intervention.",
          "status": "REJECTED_AS_FULL_EXPLANATION"
        },
        {
          "id": "MECH-Q039-FG-001",
          "name": "native foreground nuisance profiling freedom as sole explanation",
          "scope": "Sealed classification NATIVE_FOREGROUND_PROFILE_FREEDOM_REJECTED_AS_SUFFICIENT.",
          "status": "REJECTED_AS_FULL_EXPLANATION"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "accepted/observations.json": {
      "observations": [
        {
          "claim": "The observable universe is dynamically evolving; redshift, distance, and time relations support an evolving large-scale geometry.",
          "epistemic_level": "inference from multiple observable relations",
          "id": "OBS-COSMIC-EVOLUTION-001",
          "status": "SUPPORTED"
        },
        {
          "claim": "CMB, expansion, and light-element evidence support a hotter and denser early phase; this does not establish a physical singularity.",
          "epistemic_level": "multi-probe physical inference",
          "id": "OBS-HOT-DENSE-PAST-001",
          "status": "SUPPORTED"
        },
        {
          "claim": "Within the standard gravitational framework, observed gravitational behavior requires a substantial non-luminous gravitating component; its microscopic identity is unknown.",
          "epistemic_level": "phenomenon supported; particle identity unresolved",
          "id": "OBS-MISSING-MASS-001",
          "status": "SUPPORTED"
        },
        {
          "claim": "Late-time acceleration is strongly supported within the relevant relativistic cosmological framework; its microscopic cause is unresolved.",
          "epistemic_level": "model-dependent physical inference",
          "id": "OBS-LATE-ACCEL-001",
          "status": "SUPPORTED"
        },
        {
          "id": "OBS-H0-LOCAL-001",
          "inference_chain": "local distance network",
          "not_raw_measurement": true,
          "route": "H0 Distance Network",
          "sigma": 0.81,
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 73.5
        },
        {
          "id": "OBS-H0-CMB-001",
          "inference_chain": "CMB cosmological inference",
          "not_raw_measurement": true,
          "route": "Planck + SPT-3G + ACT DR6, flat LCDM",
          "sigma": 0.35,
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 67.24
        },
        {
          "id": "OBS-H0-BAOBBN-001",
          "inference_chain": "BAO standard ruler + BBN",
          "not_raw_measurement": true,
          "route": "DESI DR2 + BBN, flat LCDM",
          "sigma": 0.58,
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 68.51
        },
        {
          "claim": "A common physical CMB-space likelihood can be defined for CamSpec and HiLLiPoP by separately marginalizing each implementation over its own native nuisance parameters while retaining the physical CMB TT spectrum and A_Planck as common coordinates. Native data, covariance, foreground models and priors remain inside their own likelihoods; the likelihoods are not multiplied or subtracted.",
          "epistemic_level": "methodological computational construction",
          "evidence_refs": [
            "EVD-Q040-MANUSCRIPT",
            "EVD-Q040-RQMC"
          ],
          "id": "OBS-Q040-CMB-MARGINAL-001",
          "q_introduced": "Q040",
          "status": "SUPPORTED"
        },
        {
          "claim": "The finite defensive randomized quasi-Monte Carlo campaign reached m=16, 393216 nuisance nodes per replicate and implementation, but failed the preregistered numerical-stability tolerance 0.05. Maximum transition changes were approximately 16.59 for CamSpec and 61.13 for HiLLiPoP; independent-bank differences were approximately 28.44 and 63.11. Endpoint cosmological geometry was therefore not executed.",
          "epistemic_level": "numerical validation result",
          "evidence_refs": [
            "EVD-Q040-MANUSCRIPT",
            "EVD-Q040-RQMC"
          ],
          "id": "OBS-Q040-RQMC-VALIDATION-001",
          "q_introduced": "Q040",
          "scientific_falsification": false,
          "status": "TECHNICAL_FAIL"
        },
        {
          "claim": "The preregistered Q041 V19 downstream CamSpec-HiLLiPoP portability campaign reached a valid controlled terminal state without a complete converged posterior matrix. Thirty logical chains reached the frozen 20,000-sample limit and two remained partial through the eighth compute segment; 0 of 32 logical chains were documented COMPLETE. The mandatory completeness and Rhat science gates were blocked and no downstream portability class was scientifically issued.",
          "epistemic_level": "validated computational non-result",
          "evidence_refs": [
            "EVD-Q041-PORTABILITY-V19",
            "EVD-Q041-QJOURNAL-PDF"
          ],
          "id": "OBS-Q041-PORTABILITY-V19-001",
          "q_introduced": "Q041",
          "scientific_falsification": false,
          "status": "INCONCLUSIVE_CONTROLLED_NO_SCIENTIFIC_RESULT"
        },
        {
          "claim": "The executed V19 campaign is scientifically narrower than the broader original Q041 downstream design: V19 is n=3 EDE-only, omits a separate LCDM matrix and the common supernova block, uses three leave-one-out combinations rather than four, and uses its own preregistered decision rule. This does not invalidate V19, but V19 cannot substitute for the broader design.",
          "epistemic_level": "provenance and scope audit",
          "evidence_refs": [
            "EVD-Q041-QJOURNAL-PDF",
            "EVD-Q041-MAINBOOK-PDF"
          ],
          "id": "OBS-Q041-CONTRACT-SCOPE-001",
          "q_introduced": "Q041",
          "status": "SUPPORTED_PROVENANCE_SCOPE"
        },
        {
          "claim": "The documented strategies did not qualify the original 20-cell downstream-portability contract. Q042 closes inconclusively; feasibility of a materially different contract-preserving design remains unresolved.",
          "epistemic_level": "documented investigation closure",
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "OBS-Q042-CLOSURE-001",
          "physical_model_change": false,
          "q_introduced": "Q042",
          "scientific_falsification": false,
          "status": "CLOSED_INCONCLUSIVE_GENERAL_FEASIBILITY"
        },
        {
          "actual_computed_cosmological_result": false,
          "actual_tau": null,
          "actual_tau_status": "NOT_COMPUTED",
          "claim": "Both bounded V31 attempts stopped at the parent 600-second deadline. Histories remain partial; no complete tau or cosmological result was computed. Final killed-tail counters and peak memory are not documented.",
          "epistemic_level": "numerical provenance",
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "OBS-Q042-PARTIAL-V31-001",
          "q_introduced": "Q042",
          "status": "PARTIAL_CONDITIONAL_RAW_EVIDENCE",
          "whole_history": "PARTIAL"
        },
        {
          "actual_functional_pipeline": "NOT_EXECUTED",
          "cap": 32,
          "claim": "Under the frozen source extension, global rails and append-only retention of the existing intervals, completion cannot remove the retained candidates enough to satisfy cap32. This is a policy/representation failure, not physical minima, an executed tau failure or universal numerical impossibility.",
          "epistemic_level": "conditional frozen-algorithm support-cap incompatibility",
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "OBS-Q042-CAP-POLICY-001",
          "physical_minima_count": null,
          "physical_minima_count_status": "NOT_ESTABLISHED",
          "q_introduced": "Q042",
          "retained_candidate_counts": {
            "LOWER": 3002,
            "UPPER": 138
          },
          "status": "SUPPORTED_CONDITIONAL_MATHEMATICAL_RESULT"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "versions/accepted/v0.5/parameters.json": {
      "parameters": [
        {
          "benchmark_refs": [
            "BENCH-H0-LOCAL",
            "BENCH-H0-CMB",
            "BENCH-H0-BAOBBN"
          ],
          "id": "PAR-H0",
          "name": "Hubble constant / present expansion-rate parameter",
          "rule": "Preserve inference-chain identity; do not replace the three accepted benchmarks by one raw measurement.",
          "symbol": "H0",
          "units": "km s^-1 Mpc^-1",
          "value": null,
          "value_status": "MULTIPLE_ACCEPTED_INFERENCE_CHAINS_NOT_COLLAPSED"
        },
        {
          "id": "PAR-EDE-N-SCF",
          "name": "n=3 early-dark-energy model index used by the active constrained EDE mechanism",
          "source_mechanism_id": "MECH-EDE-N3-001",
          "symbol": "n_scf",
          "units": "dimensionless",
          "value": 3,
          "value_status": "DEFINED_BY_ACCEPTED_MECHANISM"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "versions/accepted/v0.5/benchmarks.json": {
      "benchmarks": [
        {
          "id": "BENCH-H0-LOCAL",
          "inference_chain": "local distance network",
          "not_raw_measurement": true,
          "parameter_symbol": "H0",
          "route": "H0 Distance Network",
          "sigma": 0.81,
          "source_observation_id": "OBS-H0-LOCAL-001",
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 73.5
        },
        {
          "id": "BENCH-H0-CMB",
          "inference_chain": "CMB cosmological inference",
          "not_raw_measurement": true,
          "parameter_symbol": "H0",
          "route": "Planck + SPT-3G + ACT DR6, flat LCDM",
          "sigma": 0.35,
          "source_observation_id": "OBS-H0-CMB-001",
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 67.24
        },
        {
          "id": "BENCH-H0-BAOBBN",
          "inference_chain": "BAO standard ruler + BBN",
          "not_raw_measurement": true,
          "parameter_symbol": "H0",
          "route": "DESI DR2 + BBN, flat LCDM",
          "sigma": 0.58,
          "source_observation_id": "OBS-H0-BAOBBN-001",
          "status": "ACTIVE_BENCHMARK",
          "units": "km s^-1 Mpc^-1",
          "value": 68.51
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "versions/accepted/v0.5/uncertainty.json": {
      "q_access_end": "Q043",
      "schema_version": 1,
      "uncertainties": [
        {
          "benchmark_ref": "BENCH-H0-LOCAL",
          "id": "UNC-BENCH-H0-LOCAL",
          "sigma": 0.81,
          "status": "ACCEPTED_BENCHMARK_UNCERTAINTY",
          "type": "inference_uncertainty",
          "units": "km s^-1 Mpc^-1"
        },
        {
          "benchmark_ref": "BENCH-H0-CMB",
          "id": "UNC-BENCH-H0-CMB",
          "sigma": 0.35,
          "status": "ACCEPTED_BENCHMARK_UNCERTAINTY",
          "type": "inference_uncertainty",
          "units": "km s^-1 Mpc^-1"
        },
        {
          "benchmark_ref": "BENCH-H0-BAOBBN",
          "id": "UNC-BENCH-H0-BAOBBN",
          "sigma": 0.58,
          "status": "ACCEPTED_BENCHMARK_UNCERTAINTY",
          "type": "inference_uncertainty",
          "units": "km s^-1 Mpc^-1"
        },
        {
          "id": "UNC-EDE-GLOBALITY",
          "source_constraint_id": "CON-GLOBALITY-001",
          "statement": "Corrected high-H0 EDE basins are best-observed finite-search solutions, not proven global minima.",
          "status": "OPEN_METHOD_UNCERTAINTY",
          "type": "optimization_globality"
        },
        {
          "id": "UNC-EDE-LIKELIHOOD",
          "source_robustness_id": "ROB-EDE-LIKE-001",
          "statement": "High-H0 EDE viability depends materially on experiment, likelihood, basin, and implementation.",
          "status": "ACTIVE_MODEL_DEPENDENCE",
          "type": "likelihood_implementation_dependence"
        },
        {
          "id": "UNC-Q039-STRUCTURAL",
          "source_robustness_id": "ROB-Q039-001",
          "statement": "Single tested implementation blocks do not remove the Planck likelihood geometry discrepancy; deeper coupled differences remain unresolved.",
          "status": "OPEN_STRUCTURAL_UNCERTAINTY",
          "type": "likelihood_implementation_dependence"
        },
        {
          "id": "UNC-Q040-MARGINAL-NUMERIC",
          "statement": "Tested finite representations fail mandatory stability validation; marginalized endpoint geometry is not established.",
          "status": "OPEN_NUMERICAL_UNCERTAINTY",
          "type": "numerical_integration_and_compression"
        },
        {
          "id": "UNC-Q040-CAUSAL",
          "statement": "The causal origin of the CamSpec-HiLLiPoP fitted-geometry difference remains unresolved.",
          "status": "OPEN_STRUCTURAL_UNCERTAINTY",
          "type": "likelihood_implementation_dependence"
        },
        {
          "id": "UNC-Q041-POSTERIOR-CONVERGENCE",
          "q_introduced": "Q041",
          "statement": "Under the frozen Q041 V19 sampler and compute budget, the complete converged posterior matrix required for downstream portability classification was not obtained. This blocks physical classification but is not physical falsification.",
          "status": "OPEN_NUMERICAL_UNCERTAINTY",
          "type": "finite_sampling_and_convergence"
        },
        {
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "UNC-Q042-REFERENCE-QUALIFICATION",
          "q_introduced": "Q042",
          "statement": "Original binary arithmetic, upstream physical/table accuracy, original switched-RHS solution properties and downstream prediction/likelihood error budget remain unresolved or not documented. Reference truth is BLOCKED.",
          "status": "OPEN_NUMERICAL_UNCERTAINTY",
          "type": "structural_and_numerical_qualification"
        },
        {
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "UNC-Q042-KILLED-TAIL",
          "q_introduced": "Q042",
          "statement": "V31 histories are partial. Final committed endpoints, counters and peak RSS after the parent kill are NOT DOCUMENTED; no complete tau value exists.",
          "status": "OPEN_NUMERICAL_UNCERTAINTY",
          "type": "incomplete_execution_reporting"
        }
      ]
    },
    "versions/accepted/v0.5/assumptions.json": {
      "assumptions": [
        {
          "id": "ASSUMP-INDEPENDENT-GAUSSIAN",
          "scope": "gaussian-tension calculation only",
          "statement": "The simple tension calculator treats the supplied marginal uncertainties as independent Gaussian standard deviations.",
          "status": "EXPLICIT_COMPUTATIONAL_ASSUMPTION"
        },
        {
          "id": "ASSUMP-IVW-COMPATIBILITY",
          "scope": "weighted-mean calculation only",
          "statement": "Inverse-variance weighting is meaningful only when the supplied estimates are scientifically suitable to combine and the supplied sigmas represent the relevant uncertainties.",
          "status": "EXPLICIT_COMPUTATIONAL_ASSUMPTION"
        },
        {
          "id": "ASSUMP-H0-INFERENCE-CHAIN-SEPARATION",
          "source_constraint_id": "CON-H0-001",
          "statement": "The three active H0 benchmarks are distinct inference chains and must not be treated as identical raw measurements.",
          "status": "ACCEPTED_MODEL_CONSTRAINT"
        },
        {
          "benchmark_ref": "BENCH-H0-CMB",
          "id": "ASSUMP-CMB-BENCH-FLAT-LCDM",
          "statement": "The accepted combined CMB H0 benchmark is conditional on the flat LCDM inference route recorded in accepted observations.",
          "status": "BENCHMARK_CONDITION"
        },
        {
          "benchmark_ref": "BENCH-H0-BAOBBN",
          "id": "ASSUMP-BAOBBN-BENCH-FLAT-LCDM",
          "statement": "The accepted DESI DR2 + BBN H0 benchmark is conditional on the flat LCDM route recorded in accepted observations.",
          "status": "BENCHMARK_CONDITION"
        },
        {
          "id": "ASSUMP-EDE-LIKELIHOOD-DEPENDENCE",
          "source_mechanism_id": "MECH-EDE-N3-001",
          "statement": "High-H0 n=3 EDE viability is dataset-, likelihood-, basin-, and implementation-dependent in the accepted state.",
          "status": "ACCEPTED_MODEL_CONSTRAINT"
        },
        {
          "id": "ASSUMP-Q039-LOCKED-SCOPE",
          "source_constraint_ids": [
            "CON-Q039-001",
            "CON-Q039-002"
          ],
          "statement": "Q039 conclusions apply to the tested locked interventions and do not establish a unique physical cause for the CamSpec-HiLLiPoP discrepancy.",
          "status": "ACCEPTED_MODEL_SCOPE"
        },
        {
          "id": "ASSUMP-Q040-NATIVE-NUISANCE",
          "scope": "EQ-Q040-CMB-NATIVE-MARGINAL only",
          "statement": "Each likelihood retains its own native data, covariance, foreground model, nuisance coordinates and nuisance prior in a separate marginalization integral.",
          "status": "ACCEPTED_MODEL_SCOPE"
        },
        {
          "id": "ASSUMP-Q040-COMMON-CMB",
          "scope": "EQ-Q040-CMB-NATIVE-MARGINAL only",
          "statement": "The common object is the physical CMB TT spectrum plus A_Planck; the likelihoods are not multiplied or subtracted into a synthetic likelihood.",
          "status": "ACCEPTED_MODEL_SCOPE"
        },
        {
          "evidence_refs": [
            "EVD-Q042-QJOURNAL-PDF",
            "EVD-Q042-INGESTION-V31",
            "EVD-Q042-CAP-CERTIFICATE"
          ],
          "id": "ASSUMP-Q042-FROZEN-INTERVAL-POLICY",
          "q_introduced": "Q042",
          "scope": "OBS-Q042-CAP-POLICY-001 only",
          "statement": "The necessary cap failure assumes the frozen real-table source extension, no-exotic/fixed-helium/reio_camb domain, global rails and append-only unchanged retained intervals. It concerns existing absolutely continuous solutions satisfying that frozen RHS almost everywhere; it proves neither original switched-RHS existence/uniqueness nor original executable/upstream accuracy.",
          "status": "ACCEPTED_MODEL_SCOPE"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "evidence/q_updates/Q043.json": {
      "authoritative_result_id": "R-Q043-REPOSITORY-INTEGRATION-001",
      "case_id": null,
      "case_id_status": "NOT_DOCUMENTED",
      "current_verified_model_head": "14eacce7a93e4ac780d59b1e86dc0cb9060f38ad",
      "historical_model_head": "10fa83797b2f7740519d4e43b1bebf0a6e35bada",
      "historical_state_is_current_state": false,
      "input_documents": [
        {
          "archived_name": "integration_result.json",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 102151,
          "filename": "q043_integration_result(1).json",
          "origin": "ORIGINAL_BUBBLEVERSE_RESULT_FROM_RESOLVED_FILE_REFERENCE",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "ORIGINAL_STRUCTURED_RESULT",
          "sha256": "4486e5173ba8ef3ac659c743bb578284c93446ce9e5b3d0dae71728beadbb9ff",
          "source_repository_commit": null
        },
        {
          "archived_name": "cumulative_journal.md",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 105684,
          "filename": "Q043_SAMLET_JOURNAL(1).md",
          "origin": "ORIGINAL_BUBBLEVERSE_RESULT_FROM_RESOLVED_FILE_REFERENCE",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "ORIGINAL_CUMULATIVE_JOURNAL",
          "sha256": "b952c3e80e58dc6290e16b432ef20040e32bb111aea56d97e4fbf7892836b42c",
          "source_repository_commit": null
        },
        {
          "archived_name": "q_journal.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 1192715,
          "filename": "Bubbleverse_Q-Journals_Q001-Q042.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "PRIMARY_Q_JOURNAL_PDF",
          "sha256": "c87270ed88b5b0994cd83d94305d915c55a4783c650c321ce784f5904447eb04",
          "source_repository_commit": null
        },
        {
          "archived_name": "appendices.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 635977,
          "filename": "Bubbleverse_Technical_Appendices_A-D.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "SUPPORTING_APPENDICES_PDF",
          "sha256": "e3c21469cc7a53c51a2800146396c2cfcd8872154b6701d9f88668d965c833a7",
          "source_repository_commit": null
        },
        {
          "archived_name": "main_book.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 1370169,
          "filename": "Bubbleverse_Main_Book.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "SUPPORTING_MAIN_BOOK_PDF",
          "sha256": "507945a2549c26e56f894a4fca5e9115682c242fcccda66f7b9b6b89dae33b05",
          "source_repository_commit": null
        }
      ],
      "model_change_summary": {
        "added": [
          {
            "category": "ROBUSTNESS_UPDATE",
            "evidence_refs": [
              "EVD-Q043-RESULT",
              "EVD-Q043-JOURNAL"
            ],
            "id": "ROB-Q043-LOCAL-VALIDATION-001",
            "statement": "Internal local preparation validation with historical remote boundaries retained."
          }
        ],
        "evidence_refs": [
          "EVD-Q043-RESULT",
          "EVD-Q043-JOURNAL",
          "EVD-Q043-QJOURNAL-PDF",
          "EVD-Q043-APPENDICES-PDF",
          "EVD-Q043-MAINBOOK-PDF"
        ],
        "from_version": "v0.4",
        "modified": [
          "Controlled metadata boundary Q001-Q043 after promotion; historical Q043 statements remain verbatim."
        ],
        "new_assumptions": [],
        "new_benchmarks": [],
        "new_calculations": [],
        "new_domains": [],
        "new_equations": [],
        "new_parameters": [],
        "new_uncertainties": [],
        "physical_model_change": false,
        "preserved": [
          "All existing physical observations, constraints, mechanisms, predictions and contradictions",
          "All parameter, equation, benchmark, assumption, uncertainty and domain entries",
          "All prior accepted snapshots, Q042 evidence bytes, 91 source objects and inherited claim maps",
          "All 14 existing public operations and calculation schemas"
        ],
        "resolved_contradictions": [],
        "schema_version": 1,
        "superseded": [],
        "target_q": "Q043",
        "to_candidate_version": "v0.5",
        "update_class": "EVIDENCE_ONLY_UPDATE"
      },
      "physical_model_change": false,
      "production_restart_authorized": false,
      "q_id": "Q043",
      "result": "PASS_LOCAL_PREPARATION_AND_VALIDATION_ONLY",
      "schema_version": 1,
      "source_manuscript_commit": null,
      "source_repository": "Morfindien/Bubbleverse",
      "source_repository_inspection_commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "source_repository_modified": false,
      "source_repository_sync_required": true,
      "target_input_commit": "14eacce7a93e4ac780d59b1e86dc0cb9060f38ad",
      "update_class": "EVIDENCE_ONLY_UPDATE"
    },
    "accepted/model_state.json": {
      "accepted_at": "2026-10-09T11:09:50.022279+00:00",
      "accepted_model_version": "v0.5",
      "artifact_type": "BUBBLEVERSE_MODEL_STATE",
      "candidate_model_version": null,
      "created_at": "2026-10-09T10:55:49.771933+00:00",
      "current_q": "Q043",
      "input_document_type": "PDF_AUTHORIZED_SUBSTITUTE_WITH_ORIGINAL_STRUCTURED_RESULT",
      "input_documents": [
        {
          "archived_name": "integration_result.json",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 102151,
          "filename": "q043_integration_result(1).json",
          "origin": "ORIGINAL_BUBBLEVERSE_RESULT_FROM_RESOLVED_FILE_REFERENCE",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "ORIGINAL_STRUCTURED_RESULT",
          "sha256": "4486e5173ba8ef3ac659c743bb578284c93446ce9e5b3d0dae71728beadbb9ff",
          "source_repository_commit": null
        },
        {
          "archived_name": "cumulative_journal.md",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 105684,
          "filename": "Q043_SAMLET_JOURNAL(1).md",
          "origin": "ORIGINAL_BUBBLEVERSE_RESULT_FROM_RESOLVED_FILE_REFERENCE",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "ORIGINAL_CUMULATIVE_JOURNAL",
          "sha256": "b952c3e80e58dc6290e16b432ef20040e32bb111aea56d97e4fbf7892836b42c",
          "source_repository_commit": null
        },
        {
          "archived_name": "q_journal.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 1192715,
          "filename": "Bubbleverse_Q-Journals_Q001-Q042.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "PRIMARY_Q_JOURNAL_PDF",
          "sha256": "c87270ed88b5b0994cd83d94305d915c55a4783c650c321ce784f5904447eb04",
          "source_repository_commit": null
        },
        {
          "archived_name": "appendices.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 635977,
          "filename": "Bubbleverse_Technical_Appendices_A-D.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "SUPPORTING_APPENDICES_PDF",
          "sha256": "e3c21469cc7a53c51a2800146396c2cfcd8872154b6701d9f88668d965c833a7",
          "source_repository_commit": null
        },
        {
          "archived_name": "main_book.pdf",
          "authority": "AUTHORITATIVE_BUBBLEVERSE_SOURCE",
          "bytes": 1370169,
          "filename": "Bubbleverse_Main_Book.pdf",
          "origin": "OPERATOR_SUPPLIED_PDF",
          "q_boundary_status": "AUTHORIZED_THROUGH_Q043",
          "role": "SUPPORTING_MAIN_BOOK_PDF",
          "sha256": "507945a2549c26e56f894a4fca5e9115682c242fcccda66f7b9b6b89dae33b05",
          "source_repository_commit": null
        }
      ],
      "knowledge_boundary": "Q001-Q043",
      "layers": {
        "constraints": "accepted/constraints.json",
        "contradictions": "accepted/contradictions.json",
        "mechanisms": "accepted/mechanisms.json",
        "observations": "accepted/observations.json",
        "predictions": "accepted/predictions.json",
        "robustness": "accepted/robustness.json"
      },
      "mode": "INCREMENTAL_UPDATE",
      "model_repository": "Morfindien/bubbleverse-model",
      "model_revision": "R000005",
      "new_scientific_q_allocated": false,
      "physical_model_change": false,
      "processed_through_q": "Q043",
      "production_restart_authorized": false,
      "q042_investigation_status": "CLOSED_INCONCLUSIVE_GENERAL_FEASIBILITY",
      "q043_investigation_status": "CLOSED_LOCAL_PREPARATION_AND_VALIDATION",
      "q043_result": "PASS_LOCAL_PREPARATION_AND_VALIDATION_ONLY",
      "q_access_end": "Q043",
      "q_access_start": "Q001",
      "schema_version": 1,
      "scientific_rule": "Best current compression of validated Bubbleverse state inside the authorized Q range; not established truth.",
      "source_bubbleverse_commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "source_repository": "Morfindien/Bubbleverse",
      "source_repository_commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "source_repository_sync_required": true,
      "status": "ACCEPTED",
      "update_class": "EVIDENCE_ONLY_UPDATE",
      "word_input_filename": null,
      "word_input_semantics": "NO_WORD_DOCUMENT_DISCOVERED; AUTHORITATIVE_PDF_AND_STRUCTURED_RESULT_USED",
      "word_input_sha256": null
    },
    "accepted/predictions.json": {
      "predictions": [
        {
          "future_q_evidence_used": false,
          "id": "PRED-H0-INDEPENDENT-001",
          "statement": "A future roughly one-percent H0 determination nearly independent of both stellar distance-ladder calibration and early-universe sound-horizon calibration would strongly discriminate among current inference chains.",
          "status": "OPEN"
        },
        {
          "future_q_evidence_used": false,
          "history": [
            {
              "note": "V19 reached a valid controlled no-science terminal state because convergence and completeness gates were not met; no portability class was issued.",
              "q": "Q041",
              "status": "INCONCLUSIVE_COMPUTATIONAL_ATTEMPT"
            },
            {
              "note": "Q042 closed without a qualified 20-cell comparison; physical prediction remains open.",
              "q": "Q042",
              "status": "INCONCLUSIVE_FEASIBILITY_INVESTIGATION"
            }
          ],
          "id": "PRED-EDE-PORTABILITY-001",
          "statement": "A robust high-H0 n=3 EDE explanation should remain scientifically viable across genuinely matched likelihood implementations rather than only within one favorable construction.",
          "status": "OPEN"
        },
        {
          "future_q_evidence_used": false,
          "history": [
            {
              "note": "A deeper common-latent nuisance-marginalization route was defined, but numerical validation failed before endpoint geometry.",
              "q": "Q040",
              "status": "INCONCLUSIVE_PREREQUISITE_ATTEMPT"
            }
          ],
          "id": "PRED-Q039-COUPLED-001",
          "statement": "A future preregistered coupled likelihood/data-vector harmonization test can discriminate whether the residual CamSpec-HiLLiPoP geometry difference is removed only by jointly changing multiple implementation layers.",
          "status": "OPEN"
        }
      ],
      "q_access_end": "Q043",
      "schema_version": 1
    },
    "provenance/Q043_REMOTE_INSTALLATION_RECEIPT.json": {
      "accepted_version": "v0.5",
      "baseline_commit": "14eacce7a93e4ac780d59b1e86dc0cb9060f38ad",
      "bundle_sha256": "d18c0ad4e3438d86cbec4a137800abf652fe6ade70b88cc61f16bfb6d3f3c459",
      "initial_main_commit": "40d5b77077bbf4804ff32dd5b07bdff89bb295a7",
      "model_revision": "R000005",
      "package_commit": "7ce4ab007cf991922650f466936c1f5da2ffe237",
      "physical_model_change": false,
      "production_restart_authorized": false,
      "promotion_commit": "95e035013960d681bc54efccf3739d8eaa55acd8",
      "remote_promotion_verified": true,
      "run_id": "37927147545",
      "run_url": "https://github.com/Morfindien/bubbleverse-model/actions/runs/37927147545",
      "source_repository_modified": false,
      "stop_state": "PROMOTED",
      "target_q": "Q043",
      "test_results": {
        "campaign_gate": "PASS",
        "protected_state_unchanged": true,
        "public_healthcheck_passed": 20,
        "q043_gate": "PASS",
        "regression_tests_passed": 22
      },
      "timestamp_utc": "2026-10-09T11:59:40.027770+00:00"
    }
  },
  "current_closed_q": "Q044",
  "case_id": null,
  "proposed_next_q": "Q045",
  "canonicalization_required": true,
  "next_question": "For the frozen Q041 ΛCDM and n_scf = 3 EDE configurations, does replacing only the native optical-depth integration functional with a convergent Thomson-integral reference, at identical requested τ_reio and otherwise unchanged physical inputs, alter CMB TT/TE/EE predictions and native likelihood values enough to threaten the original H0/EDE decision margins?",
  "starting_motor": "BUBBLEVERSE — AUTONOMOUS MATHEMATICS ENGINE",
  "production_restart_authorized": false,
  "remote_write_performed": false
}
```

## Effective end state

Physical scientific model unchanged; numerical knowledge refined/extended; evidence limits narrowed and scientific debt explicit. No new robust connection candidate, fundamental contradiction or required reopening of a previous closed case is established. This does not mean every possible cross-domain connection has been excluded.
THE NEXT PROPOSED BUBBLEVERSE Q IS A SCIENTIFIC QUESTION, NOT A MAINTENANCE ACTION.

---
# PRESERVED INCOMING JOURNAL — HISTORICAL VERSION
The following bytes are unchanged. Current-state interpretations and routing are superseded by the effective state above wherever explicitly indicated.

# BUBBLEVERSE — COMPLETED Q → MOTOR 14 HANDOFF

RD OF THE UNIVERSE
Date and time: 2026-10-09T18:53:38.281918+02:00 (Europe/Copenhagen); 2026-10-09T16:53:38.281918+00:00 (UTC).

STATUS: QUESTION RESOLVED
CASE ID: NOT DOCUMENTED
CURRENT Q: Q044 — unchanged operator-proposed identifier; canonical remote registration NOT PERFORMED.
QUESTION: Under the original Q041 matched-data and prior contract, does the CamSpec–HiLLiPoP implementation difference produce a material difference in H0 constraints or the n_scf = 3 EDE-versus-ΛCDM conclusion once numerical prediction accuracy and posterior convergence are qualified, or is the downstream result equivalent or conditional on the external dataset combination?
SELECTED NEXT ENGINE: BUBBLEVERSE — MOTOR 14: AUTONOMOUS UNIVERSE REVISION.

## FINAL ANSWER

INCONCLUSIVE / INSUFFICIENT SCIENTIFIC QUALIFICATION.
Current documented evidence establishes none of: material H0/EDE inference difference, qualified equivalence, or external-dataset conditional behavior under the original Q041 contract. A conditional mathematical component has been computed; the qualified downstream comparison remains unavailable.

## EPISTEMIC STATUS

Q044 is CLOSED EPISTEMICALLY at the documented evidence boundary. The original scientific contract classifier remains NOT_AVAILABLE. This is not a cosmological null result, evidence of equivalence, universal numerical infeasibility or physical falsification. QUESTION RESOLVED denotes a defensible insufficient-evidence closure; the physical answer remains unknown. Preserve PRED-EDE-PORTABILITY-001, PRED-H0-INDEPENDENT-001 and PRED-Q039-COUPLED-001 as OPEN. Scientific debt survives the closure.

## RECOMMENDED CHATGPT EXECUTION PROFILE

Exposed configurations considered: GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol, GPT-6 Luna. Actual capabilities include Work/Codex files/Python/C, connected GitHub retrieval, web research, Library persistence and parallel-agent facilities. Exact current model/reasoning, full operator selector, context/usage limits and comparative reliability are NOT VERIFIED. No model switch or agents were used.
Recommended Motor14 setup: strong reasoning in Work/Codex, GPT-6.1 Sol High if selectable; classes C+E under the ingestion taxonomy. Fallback: strongest equivalent available reasoning with complete journal/source access. Escalate for genuinely difficult global contradictions or context complexity. Motor14 needs cross-case integration; another production campaign, broad cosmology search or fixture replay is not selected.

## WHY Q IS SUFFICIENTLY DOCUMENTED

The requested finite support-functional task produced actual new mathematical information. The received boundaries are usable within their explicit conditions. Targeted retrieval of original scientific criteria, treatment-readiness design/record and initialized-context contract did not recover a qualified endpoint error bridge or valid matched reference products. These records explicitly preserve missing full-history/prediction/likelihood accuracy. The current record has no qualified original20-cell downstream verdict.

Further generic derivations, repetition of the same hull, more hash audits or the already passed component tests cannot produce the missing evidence. A future independently qualified reference and inference campaign could change the physical answer; that is genuinely new evidence, not an implication of the present component. Close the bounded evidence-based investigation INCONCLUSIVE rather than repeat its design/validation loop. Closure is not merely a response to elapsed time or lack of production authorization. No claim excludes every possible future method.

## SAMLET JOURNAL

Q044_SAMLET_JOURNAL.md is the updated same-identity authoritative journal, containing this effective closure supplement and the entire218195-byte incoming journal verbatim. All six incoming JSON blocks parse. The original91 source objects have91 unique IDs; both inherited claim-map trees and all subsequent additions survive. The earlier196340-byte tail still matches its preserved hash. Separately missing global master-journal content remains NOT RECOVERED; CASE ID remains NOT DOCUMENTED.

## DECISIVE EVIDENCE

- R-Q044-SPLINE-ADJOINT-001 reports conditional fixed-knot native-plus bounds, inference adequacy UNDETERMINED, native-binary rounding NOT CERTIFIED and no complete recovered V31 history.
- The exact q042_production_spec_v1.json matches SHA25641e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c. It provides original materiality/model-preference criteria, not treatment prediction/likelihood accuracy.
- The retrieved readiness record leaves matched reference products and justified numerical tolerances missing. The V29 context contract separates original-binary arithmetic and upstream/table/entry accuracy as UNRESOLVED gates; its scope is prerequisite-only.
- No supplied qualified20-cell comparison fills this gap. Invalid Q040 endpoints, narrower Q041V19 non-result, partial Q042 records and Q043 technical preparation cannot replace it.

## SUPPORTING EVIDENCE

All ten attached files were inspected for their roles; the eight declared reproduction hashes and five validation hashes match. Fresh ingestion checks verify exact unique support coverage, correct native N/index relation, ordered intervals and aggregation of every recorded support cell into the declared hull. No mathematical-program, C-replay or artifact-extraction rerun was performed here. The64 rational fixtures,18 C replays and17 V29 member matches remain reported validation from the Mathematics result, not fresh independent reproduction.
Execution main remains72cf9e92fc794c122f593a77b6a555e6e97f6a2e. Frozen source contents were fetched read-only at that pin. This is a targeted audit of specified contracts, not an exhaustive search of every external system or artifact.

## WHAT WAS ESTABLISHED

Support-specific adjoint weights and real-arithmetic residual enclosures were implemented under documented conditions. All3140 inherited candidate supports have computed bounds. A scalar union hull represents the candidate interval union with two extrema, although every support is retained in diagnostics.

| Trial | Candidates | Conditional dimensionless native-plus bounds | Width |
|---|---:|---|---:|
| UPPER | 138 | [0.70676532823050475, 0.7067869701940579] | 2.1641963553142851e-05 |
| LOWER | 3002 | [0.0016297839913017342, 0.0018091545475532051] | 0.00017937055625147098 |

These are conservative component enclosure extrema under inherited rail/witness assumptions, not observed or fitted optical depths. The frozen V31 stored-support cap32 limitation remains conditionally valid; this distinct scalar representation does not retroactively repair or reproduce V31.

## WHAT WAS NOT ESTABLISHED

No new H0, posterior convergence, materiality class, EDE/LCDM preference, equivalence, dataset-conditional result, physical causality or physical falsification. No qualified full-history/prediction/likelihood reference or uniform original-binary error proof. A scalar bound controls one functional of a history; no supplied quantitative implication bounds every relevant prediction or the posterior decision endpoints. Its width alone cannot demonstrate inference adequacy.

## FALSIFIED / REJECTED ALTERNATIVES

Preserve Q035 classifier correction, Q039 tested clean-block negatives, Q040 invalid scientific endpoints, Q041V19's contract boundary and the unchanged V31 failure. No newly falsified physical hypothesis.
Reject unsupported upgrading of the component to a qualified reference/posterior, deriving a scientific tau tolerance from PolyChord precision_criterion0.001, optimizer settings or the1e-4 bracket stopping rule, treating finite native-C diagnostic agreement as a uniform error proof, and inferring equivalence from absent qualified posteriors. These are invalid inference substitutions, not tests falsifying cosmology.

## UNEXPLAINED ANOMALIES

C-036-IMPL remains OPEN_NARROWED. Internal fitted geometry remains documented; physical origin and downstream significance remain unknown. Native-plus versus exact-cubic-minus is a preserved known technical distinction, not newly discovered physics. Raw unexpected values remain exact; surprise is not a validity filter.

## REMAINING UNCERTAINTIES

Full native/history/grid accuracy, physical applicability of inherited rails/support assumptions, complete prediction-to-likelihood/posterior bounds, converged20-cell inference and implementation causality remain unresolved. They limit present evidence without proving nature is unknowable or future numerical methods impossible. A future new-evidence study may address them.

## BUBBLEVERSE-GENERATED RESULTS

Received R-Q044-SPLINE-ADJOINT-001: CONDITIONAL MATHEMATICAL / NUMERICAL COMPONENT RESULT, ACCEPTED WITH SCOPE LIMITS. I-Q044-SPLINE-CHECKS-001: reported component validation. I-Q044-V29-BYTE-RECOVERY-001: reported original context/grid recovery.
New R-Q044-SPLINE-INGESTION-002: SOURCE / QUALIFICATION / JOURNAL-INTEGRATION RESULT. No new numerical production, program registration or scientific computation.

## INTERNAL RESULT PROVENANCE

Q044_SPLINE_INGESTION_RESULT.json contains all ten attachment sizes/hashes, audit checks, fresh source records, source-to-claim mappings, completion boundary and journal actions. Component environment inherited: Python3.12.14, NumPy2.3.5, MPFR4.2.1 with256-bit directed source calculations; exact Fraction fixtures; local C wrapper compiled -shared -fPIC -O0 -fno-fast-math -ffp-contract=off. Full compiler details remain in the preserved journal/checks.
Native source mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97. arrays.c c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4; thermodynamics.c d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6. V29 run37362125253/artifact11366628579 and context/grid/prefix hashes survive. Complete V31 raw histories remain absent here.
New chain/sampler/likelihood products: NOT COMPUTED. Remote mutation, workflow dispatch, production restart, threshold changes and model promotion: NONE. Production remains NOT AUTHORIZED. New PROGRAM_ID: NONE. The accepted remote model state recorded historically is unchanged by this local closure.

## WEB / PLUGIN / TOOL RESEARCH

YES: targeted connected GitHub primary technical-source retrieval and local file/JSON audit. Questions: original criteria intact? Ready endpoint reference/error bridge in inspected contracts? Execution head changed? Source snapshots and hashes are preserved in Q044_ENDPOINT_SOURCE_EVIDENCE.json.
New external cosmological observations, broad survey and independent physical replication: NONE. Project contracts and computation remain internal technical evidence. No contradictory qualified cosmological outcome was recovered. The source audit confirms a finite qualification boundary; more general source summaries cannot generate the missing matched numerical products. No tool failure or fabricated fallback result contributed to this ingestion.

## COMPLETE ACTIVE SOURCE REGISTER

The full91-object inherited register, later additions and complete claim maps remain verbatim in Q044_SAMLET_JOURNAL.md. This section supplements them, not replaces them. Conclusion-critical active records:

- I-Q044-CONTRACT-001 / I-Q042-TREATMENT-003: frozen original20-cell science specification, SHA25641e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c.
- I-Q044-SOURCELOCK-001: preserved software/dataset/likelihood source lock, SHA2560f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56; not a runtime truth certificate.
- I-Q044-SPLINE-ADJOINT-001: conditional support-functional computation; result SHA25625638274b3898d97f63d1ecbb06739797396659d02270ab80e37d4bdf5b2354e.
- I-Q044-SPLINE-CHECKS-001: recorded exact/native diagnostics; checks SHA2565300cd20e40c2ff43ee48ec1a0ad1b9ef487639bd2aa2fae7d1ce9911861948f.
- I-Q044-V29-BYTE-RECOVERY-001: context artifact archive3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9, prerequisite scope.
- I-Q044-NATIVE-PIN-RECHECK-001 / K-Q042-V24-001 / K-Q042-INGESTDESIGN-001: native functional/source semantics, not observations.
- I-Q042-COMPARISON-V31-001 / I-Q042-COMPARISON-V31-VALIDATION-001 / I-Q042-V31-INGESTION-001: partial computational output and conditional cap32 limitation, no full scientific comparison.
- I-Q044-MATH-QUALIFICATION-001: preserved conditional likelihood/posterior error mathematics, still lacking a qualified likelihood envelope.
- I-Q044-SPLINE-INGESTION-002 and I-Q044-ENDPOINT-CONTRACT-AUDIT-001: this ingestion and targeted frozen-contract audit. Full metadata and actual URLs follow in the JSON supplement.

## CLAIM-TO-SOURCE MAP

All inherited mappings survive. Add C-Q044-I06–I10 as recorded below. Traceability: attached inputs/result/checks → conditional component → inspected endpoint contracts → insufficient qualification → Motor14. This does not convert project computation into external cosmological evidence.

## SUPERSEDED MATERIAL / JOURNAL EFFECT

ADD scoped acceptance, endpoint-contract audit and evidence-boundary closure. UPDATE current Q044 workflow CONTINUES to CLOSED INCONCLUSIVE; destination MOTOR14. Supersede current instructions to repeat generic qualification design or return indefinitely to ingestion. Preserve every historical continuation instruction with its original temporal scope. KEEP physical parameters, candidates, tensions, predictions, rejected paths and accepted-model boundaries.

## IMPORTANT ASSUMPTIONS

Component: fixed decoded knots/constants, inherited hydrogen rail/support set, residual helium/source-write semantics and stated outward-rounding assumptions. The real-arithmetic native-plus target differs from exact-cubic-minus and uniform original-binary qualification. Planck arms overlap in data and are not independent observations; descriptive normalized mean differences are not automatically independent-Gaussian significance.
Preserve original two native Planck arms, LCDM/n_scf3EDE, FULL and four LOO combinations, ACTDR6 primary/lensing, DESIDR2, identical frozen supernova likelihood, common priors/model definitions and native nuisances. Preserve all decision rules. No arbitrary accuracy tolerance is invented.

## IMPLICATIONS ALREADY VISIBLE

Bubbleverse has a new conditional scalar-enclosure method, not a new accepted H0 or EDE-portability verdict. Qualification debt and implementation tension remain explicit. Motor14 determines final knowledge revision and canonical registration. This local ingestion changes no repository/model publication state.

## POSSIBLE FUTURE QUESTIONS / NEW-EVIDENCE CONDITIONS

Future qualified investigation of the unresolved physical objective requires independently valid matched references, an applicable complete error envelope and a preregistered converged inference comparison. A materially changed treatment needs a new numerical lineage and validity evidence before importing cosmological claims. These are genuine new-evidence conditions, not automatic rerouting or a new Q allocation here. Motor14 chooses any next canonical scientific question; repository maintenance does not replace the scientific objective.

## NEXT TASK FOR MOTOR 14

Integrate this CLOSED INCONCLUSIVE case with accumulated knowledge. Classify the mathematical gain, preserve complete sources/claim maps and original open physical predictions, and retain numerical qualification debt. Do not promote conditional/partial evidence to a physical result, revive rejected paths or infer EDE/standard-model preference. Verify any canonical Q allocation against the current authoritative registry before registration. Select future scientific work only for a specific new-evidence opportunity; do not reopen the completed bounded audit as another validation loop. All state and provenance accompany that decision.

## MACHINE-READABLE CURRENT SUPPLEMENT

```json
{
  "new_source_records": [
    {
      "source_id": "I-Q044-SPLINE-INGESTION-002",
      "type": "BUBBLEVERSE INTERNAL RESULT INGESTION / QUALIFICATION ANALYSIS",
      "title": "Support-adjoint component ingestion and epistemic Q044 closure",
      "authors": "Bubbleverse Result Ingestion & Routing Engine",
      "year": 2026,
      "date_utc": "2026-10-09T16:53:38.281918+00:00",
      "result_id": "R-Q044-SPLINE-INGESTION-002",
      "received_result": "R-Q044-SPLINE-ADJOINT-001",
      "supports": "Input identities, support/hull aggregation, journal continuity, scoped acceptance and insufficient-evidence closure. No new cosmological computation."
    },
    {
      "source_id": "I-Q044-ENDPOINT-CONTRACT-AUDIT-001",
      "type": "BUBBLEVERSE INTERNAL SOURCE AUDIT OF PINNED TECHNICAL CONTRACTS",
      "title": "Frozen decision rules and available endpoint/reference qualification audit",
      "authors": "Bubbleverse Result Ingestion & Routing Engine; underlying project source authors NOT DOCUMENTED",
      "year": 2026,
      "date_utc": "2026-10-09T16:53:38.281918+00:00",
      "repository": "Morfindien/Bubbleverse",
      "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "file": "Q044_ENDPOINT_SOURCE_EVIDENCE.json",
      "sha256": "a20cc688457114503bd06351a9137297bf44136eaf075956fff0d4d50e40f43d",
      "underlying_sources": [
        {
          "role": "science",
          "url": "https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_spec_v1.json",
          "git_blob_sha": "9b70e5c9d62adcf43f8f48f85b7ffb628c1dd84b",
          "sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
        },
        {
          "role": "design",
          "url": "https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_treatment_design_motor.md",
          "git_blob_sha": "bdde4eee62f8e14fe8125b2ed37ef253e9a3865c",
          "sha256": "409e31572137da8210c7cd360878edea03a7afa2c9d2f50dd87d2fc61ac45bd9"
        },
        {
          "role": "readiness",
          "url": "https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_treatment_readiness.json",
          "git_blob_sha": "a10a182906efc268ceb62640eb794ad8c9e102a4",
          "sha256": "319d4d6fd058e095871bd6f9fed2f4b8abda0556b8485ff88587cc65cb67e507"
        },
        {
          "role": "context_contract",
          "url": "https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_context_contract_v29.json",
          "git_blob_sha": "3b560832a1b193dd5a68c1d97cc54c3ce157bdea",
          "sha256": "383216c96027a481c3aa649af83d5ee4f79fa79710e27b5199c1a2c8f6772b1e"
        }
      ],
      "supports": "Original thresholds present; the inspected science/readiness/context contracts do not provide a qualified end-to-end error bridge. No exhaustive absence theorem."
    }
  ],
  "new_claim_to_source_map": {
    "C-Q044-I06": {
      "claim": "Accept intact all-support component with its original conditions.",
      "sources": [
        "I-Q044-SPLINE-INGESTION-002",
        "I-Q044-SPLINE-ADJOINT-001",
        "I-Q044-SPLINE-CHECKS-001"
      ]
    },
    "C-Q044-I07": {
      "claim": "No qualified scalar-to-full-prediction/likelihood/posterior bridge was recovered in the inspected contracts.",
      "sources": [
        "I-Q044-ENDPOINT-CONTRACT-AUDIT-001",
        "I-Q044-CONTRACT-001",
        "I-Q044-SPLINE-ADJOINT-001"
      ]
    },
    "C-Q044-I08": {
      "claim": "Close Q044 epistemically INCONCLUSIVE / INSUFFICIENT_SCIENTIFIC_QUALIFICATION; original scientific class NOT_AVAILABLE.",
      "sources": [
        "I-Q044-SPLINE-INGESTION-002",
        "I-Q044-ENDPOINT-CONTRACT-AUDIT-001",
        "I-Q044-SPLINE-ADJOINT-001"
      ]
    },
    "C-Q044-I09": {
      "claim": "Physical predictions remain OPEN; no model preference, equivalence or physics failure is inferred.",
      "sources": [
        "I-Q044-SPLINE-INGESTION-002",
        "I-Q044-CONTRACT-001",
        "I-Q044-SPLINE-ADJOINT-001"
      ]
    },
    "C-Q044-I10": {
      "claim": "Repeating the completed component cannot supply missing end-to-end evidence; future qualified inference requires new evidence.",
      "sources": [
        "I-Q044-SPLINE-INGESTION-002",
        "I-Q044-ENDPOINT-CONTRACT-AUDIT-001"
      ]
    }
  },
  "closure_result_file": "Q044_SPLINE_INGESTION_RESULT.json",
  "incoming_journal_sha256": "0034b4dc90a7e99da1eb99733a74331414755c8b482f37eed9a4c4fdc91a85c3",
  "incoming_journal_bytes": 218195,
  "exact_question": "Under the original Q041 matched-data and prior contract, does the CamSpec\u2013HiLLiPoP implementation difference produce a material difference in H0 constraints or the n_scf = 3 EDE-versus-\u039bCDM conclusion once numerical prediction accuracy and posterior convergence are qualified, or is the downstream result equivalent or conditional on the external dataset combination?",
  "current_status": "CLOSED_INCONCLUSIVE",
  "scientific_contract_class": "NOT_AVAILABLE",
  "next_engine": "BUBBLEVERSE \u2014 MOTOR 14: AUTONOMOUS UNIVERSE REVISION",
  "production_restart_authorized": false
}
```

## Preserved complete incoming SAMLET JOURNAL — verbatim historical record

# BUBBLEVERSE — OVERLEVERING

RD OF THE UNIVERSE
Date and time: 2026-10-09T15:03:30.148137+00:00 (UTC).

STATUS: CONTINUES
CURRENT Q: Q044 — unchanged operator-proposed identifier; no remote canonical registration.
CASE ID: NOT DOCUMENTED
EXACT QUESTION: Under the original Q041 matched-data and prior contract, does the CamSpec–HiLLiPoP implementation difference produce a material difference in H0 constraints or the n_scf = 3 EDE-versus-ΛCDM conclusion once numerical prediction accuracy and posterior convergence are qualified, or is the downstream result equivalent or conditional on the external dataset combination?
RESULT-ID: R-Q044-SPLINE-ADJOINT-001
SELECTED NEXT ENGINE: BUBBLEVERSE — AUTONOMOUS RESULT INGESTION & ROUTING ENGINE.

## CHATGPT-SETUPVURDERING

Actual verified work style: Codex in ChatGPT Work, filesystem/Python/C, connected GitHub source/artifact access and Library persistence. Exact current model variant/reasoning allocation, context capacity and usage limits are NOT VERIFIED. Exposed execution candidates include GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol and GPT-6 Luna; availability is not a benchmark of comparative reliability or the operator's full model selector. No model switch or sub-agent was used.
Recommended primary: strong mathematical reasoning in Work/Codex; GPT-6.1 Sol High if selectable with equivalent tools. Capability classes H/X + A + C under the Mathematics Engine taxonomy. Current tool-equipped setup completed this bounded task. Fallback: strongest available equivalent high-reasoning setup. Upgrade only for a materially more complex coupled error analysis or unresolved inconsistency; do not escalate merely for formatting.
Tool need: YES. Actual uses: frozen GitHub sources and artifact byte retrieval, local bounded exact/interval computation and original-journal persistence. Browser, production/HPC, general literature survey and parallel agents were unnecessary.

## SAMLET JOURNAL — effective differential update

The entire incoming journal is preserved byte-for-byte below, including all 91 inherited source objects, both inherited claim-map trees and every later Q044 addition. This is a new version of the same authoritative journal, not a separate mathematics journal. Full global master-journal material absent from the attachment remains NOT RECOVERED. Historical next-step instructions are historical; current entries below govern this handoff.
Incoming journal: 196340 bytes; SHA256 e9363e8a236a955ab1fe258e27c09c4484771540bb19948f838d271c1b2bc26d.

### J-044-20 — Actual frozen-input recovery

[TECHNICAL EVIDENCE] Original context artifact11366628579 from run37362125253 was retrieved. Its archive SHA256 matches3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9, and all17 member hashes declared by q042_context_result_v29.json match. Actual context, native grid and shared-prefix hashes match the preserved V31 basis. The full native grid contains28333 rows. Rows0..3333 are used as fixed decoded binary64 real inputs, with increasing redshift and decreasing conformal time. The grid is not a certified uncertainty envelope for the continuum history. Below50, V29 CSV rows labelled NOT_ACQUIRED are not measurements; their placeholder zeros were not used.

V31 full UPPER/LOWER node and step histories were not recovered. A recursive search of the pinned execution tree found no committed V31 raw-history paths, consistent with LOCAL_NOT_COMMITTED. The existing cap certificate retains33 actual source-xe interval witnesses per trial and the conditional global hydrogen rail. Its candidate sets are used only under its existing admissibility/domain/prefix assumptions. No missing hydrogen values are guessed.

### J-044-21 — Support-specific native functional

[DERIVED] Let x_i=eta_i in Mpc, y_i=dkappa_i in Mpc^-1, h_i=x_{i+1}-x_i<0 and d_i=(y_{i+1}-y_i)/h_i. For argmin index j>0 use N=max(3,j) and rows0..N-1. For j=0 return tau=0 as frozen native code does. The argmin row itself is excluded when j>=3. No common final-spline weights are substituted for different N.

Estimated endpoint derivatives are

s_0=d_0-h_0(d_1-d_0)/(h_0+h_1),
s_L=d_{N-2}+h_{N-2}(d_{N-2}-d_{N-3})/(h_{N-3}+h_{N-2}).

With M_i=y''(x_i), A_N M=B_N y is symmetric tridiagonal:
- First: 2h_0 M_0+h_0 M_1=6(d_0-s_0).
- Interior: h_{i-1}M_{i-1}+2(h_{i-1}+h_i)M_i+h_iM_{i+1}=6(d_i-d_{i-1}).
- Last: h_{N-2}M_{N-2}+2h_{N-2}M_{N-1}=6(s_L-d_{N-2}).

Define t_i as half the sum of adjacent h and c_i as one twenty-fourth of the sum of adjacent h^3, using only existing adjacent segments. The frozen native-plus functional is

T_N(y)=-(t_N^T y+c_N^T A_N^-1 B_N y)=a_N^T y,
a_N=-t_N-B_N^T lambda_N, A_N^T lambda_N=c_N.

A single tridiagonal adjoint solve produces all N weights in O(N); all candidate prefixes were computed separately. The endpoint boundary depends on N. A measured difference between N3195 weights and the first3195 coordinates of N3332 weights is approximately0.1388881954 Mpc (maximum coordinate difference), directly disproving unrestricted reuse of one common spline-weight vector.

The exact cubic-segment integral has a MINUS second-derivative term. Its diagnostic functional would use a_N=-t_N+B_N^T lambda_N. The production target remains NATIVE_PLUS. For x=(2,1,0), y=(4,1,0), native-plus yields10/3 whereas the cubic integral is8/3. This is the inherited technical distinction, not new physics and not an authorized correction of the frozen model.

Dimensions: M has Mpc^-3, A has Mpc, c has Mpc^3, lambda has Mpc^2 and a has Mpc. Therefore T is dimensionless. h<0 requires the native final minus sign. Nonmonotone knots, zero denominators or nonfinite bounds fail fast.

### J-044-22 — Outward coefficient and box certificates

[DERIVED CONDITIONAL] For a finite approximate adjoint lambda_hat, compute r=c-A lambda_hat with outward interval arithmetic. All h have the same negative sign, so A is strictly diagonally dominant. The exact margin is |h_0| or |h_last| at the endpoints and |h_prev+h_next| internally. A safe lower bound delta is min lower(|h_i|)>0. At a maximum absolute-error coordinate,

|r_k| >= (|A_kk|-sum_(j!=k)|A_kj|)*||lambda-lambda_hat||_inf,

hence ||lambda-lambda_hat||_inf <= ||r||_inf/delta.

This residual bound remains valid even if the approximate solve is imperfect; it is propagated outward through B^T and t. Ordinary binary64 Thomas elimination supplies an approximation only. Coefficient/box algebra uses separate nextafter-directed enclosures for each elementary operation; sums use outward pairwise reduction, not an unbounded ordinary np.sum. It assumes the observed finite IEEE-754 binary64 arithmetic with gradual underflow and round-to-nearest primitive operations. MPFR4.2.1 at256 bits with directed binary64 export is reused for source powers/tanh. No fast-math compilation is used.

For exact a and independent ordinate intervals [l_i,u_i], the sharp box range is
L_N=sum_i min(a_i*l_i,a_i*u_i), U_N=sum_i max(a_i*l_i,a_i*u_i).

With coefficient intervals, outward term products and sums enclose those exact endpoints. Over an admissible support set S, [min_(N in S)L_N,max_(N in S)U_N] is a conservative scalar union hull. It requires only two final extrema; the delivered diagnostics preserve every candidate. Sharpness applies to the abstract independent box, not to physically attainable correlated trajectories or argmin-conditioned histories. Ignoring these correlations widens the enclosure; it does not falsely tighten it.

### J-044-23 — Concrete source boxes and computed hull

[CONDITIONAL NUMERICAL COMPONENT RESULT] Reused frozen constants include nH0 in m^-3, sigma in m^2, Mpc in m, fixed residual helium and fHe. At each z<=50, set xn=xH+fHe*xHe. The inherited rail is xH in[0,0x1.fb4196502b73fp-13], conditional on the existing certificate's global analytic-rail assumptions. Its truth for a new physical history is not proved here.

Write F=(1+tanh(arg))/2 and He=fHe*(1+tanh((he_center-z)/he_width))/2 within each trial's native reionization branch; F=He=0 outside it. The frozen smoothing q is1 for z<=46 and s^2(3-2s) with s=(50-z)/4 for46<z<=50. Then

xe_source=(1-qF)*xn+q*(F*after+He).

This affine form avoids duplicating xn with artificial interval dependency. Since0<=q,F<=1, beta=1-qF lies in[0,1]; intersecting beta with this analytically established range is justified. Each source box is intersected with its retained witness, where present; empty intersections fail. y=(1+z)^2*nH0*sigma*Mpc*xe_source. Powers, tanh and conversion are outward-rounded. No placeholder CSV hydrogen history or posterior is used.

Actual results for the NATIVE_PLUS exact-real component:

| Trial | Candidate supports | Lower bound | Upper bound | Width | Lower/upper attaining enclosure supports |
|---|---:|---:|---:|---:|---|
| UPPER | 138 | 0.70676532823050475 | 0.7067869701940579 | 2.1641963553142851e-05 | 3195 / 3332 |
| LOWER | 3002 | 0.0016297839913017342 | 0.0018091545475532051 | 0.00017937055625147098 | 331 / 3332 |

The lower/upper support indices identify enclosure extrema, not fitted or observed physical supports. All138 UPPER candidates3195..3332 and3002 LOWER candidates331..3332 were included, with N=their native index (no extra row). Total candidate coverage3140/3140. The maximum adjoint error bound over these prefixes is9.400182335212992e-11 Mpc^2; maximum weight interval width is1.4563791617128174e-8 Mpc. Elapsed component calculation 16.768s locally, not an HPC campaign estimate.

This establishes a computed bounded scalar representation under documented conditions despite the unchanged V31 stored-interval cap32 failure. It does not refute that frozen representation-specific failure, prove general feasibility, certify a physical tau or resolve Q044. No Q042 reopening, cap expansion or numerical production occurred.

### J-044-24 — Finite cross-checks and qualification boundary

[TECHNICAL VALIDATION] PASS within component scope:64 cases of exact Fraction forward-spline elimination on independent small nonuniform integer grids, all coefficient enclosures checked against exact rational basis weights, plus point functional enclosures; exact constant/linear/quadratic cubic-minus limits; preserved native-plus10/3 witness. Seed44044. Maximum fixture enclosure width5.450715434562881e-10 in the chosen arbitrary ordinate units. Early development issues in interval tuple length and NumPy-integer Fraction conversion were corrected before the recorded run; no failed-development output is a scientific result.

Eighteen independent C replays use unchanged pinned function bodies with a local wrapper, compiled -shared -fPIC -O0 -fno-fast-math -ffp-contract=off; compiler gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0. Each trial uses first/middle/last candidate supports and midpoint/min-sign/max-sign ordinate choices. Every binary64 replay value falls inside its own computed exact-real component enclosure (maximum outside distance0). The diagnostic tolerance is1e-9*max(1,abs(value)), declared solely for component comparison, not a cosmological accuracy margin. This empirical finite check does not prove a uniform error bound for the frozen original binary or its other operations.

Final math component status: CONDITIONAL_BOUNDED_RESULT / COMPONENT_CHECKS_PASS.
Native-binary global rounding-error gate: UNRESOLVED.
Hydrogen/history and fixed-grid physical truth gate: UNRESOLVED.
Prediction-to-likelihood-to-posterior qualification gate: UNRESOLVED.
Q044 final scientific gate: NOT_YET_SATISFIED.
PRODUCTION_RESTART_AUTHORIZED: false.

### J-044-25 — Journal effects and exact remaining bottleneck

KEEP all Q035–Q043 historical outcomes, sources, parameters, candidates, original20-cell contract and decision rules. C-036-IMPL remains OPEN_NARROWED; portability predictions remain OPEN. No H0 estimate, EDE/LCDM preference, equivalence, physical causality or physical falsification is added. The inherited H0 benchmark numbers retain their missing primary-source details and are not used as independent test inputs here.

ADD actual V29 byte recovery, support-specific adjoint proof, conditional all-support scalar hull, finite exact/native cross-checks and provenance. UPDATE the earlier UNIMPLEMENTED mathematical support-hull direction to IMPLEMENTED_AND_COMPUTED_CONDITIONALLY. Historical statements that no artifact bytes/no support weights were computed retain their original temporal scope; they are superseded only for the current stage.

The decisive remaining uncertainty is whether a COMPLETE physical/numerical prediction error envelope, including native arithmetic and history/grid uncertainty, yields log-likelihood and posterior/model-preference error bounds narrower than the ORIGINAL decision margins. No such bridge or required tau tolerance is present in the recovered inputs. The widths alone cannot decide adequacy. The prior conditional TV/mean/width/overlap bounds in the journal remain valid but uninstantiated. Inferring equivalence from absent qualified posteriors remains invalid.

## AKTUEL OVERLEVERING

Selected next motor: the established AUTONOMOUS RESULT INGESTION & ROUTING ENGINE. Ingest this actual component result and distinguish its scope from physical qualification. Its single material task is to determine whether any documented, accessible endpoint error contract can connect these conditional scalar bounds to Q044's frozen inference criteria. Carry the complete journal and raw component files. Do not send the same generic hull derivation back to Mathematics. Return there only with new quantitative prediction/likelihood sensitivities or a concrete counterexample requiring mathematics.

A bounded numerical qualification task may be chosen only if the missing complete-history/native-arithmetic and endpoint error requirements can actually be specified and checked without changing scientific assumptions. The stored V31 raw-node files, if later retrieved, must match their declared raw SHA256s; they may sharpen this rail-based calculation but are not required to repeat the computation already completed. No production restart is authorized by this result.

Success: an explicit adequacy/insufficiency judgment relative to documented original scientific decision margins, or a finite documented unavailability boundary. Stop repeating hash audits, generic error-budget templates, old cap32 runs, launcher tests or the same component fixtures. If no accessible material next task exists, the receiving engine may close with an honestly scoped inconclusive answer and route toMotor14; that decision has not been fabricated here. Physical Q044 remains open in this handoff.

## SOURCES, CLAIM MAP AND REPRODUCTION

Native source: https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c and https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c . Execution source: https://github.com/Morfindien/Bubbleverse/tree/72cf9e92fc794c122f593a77b6a555e6e97f6a2e . No independent external cosmological measurement was added. Original K/source IDs survive below; new source IDs supplement them without renaming.

Reproduction requires Python with NumPy and system MPFR4.2.1, the delivered inputs, adjoint module and unchanged reused q042_interval_v29.py. Run python Q044_SPLINE_ADJOINT.py Q044_SPLINE_INPUTS.json Q044_SPLINE_RESULT.json. For finite native diagnostics, compile gcc -shared -fPIC -O0 -fno-fast-math -ffp-contract=off Q044_NATIVE_REPLAY.c -o native_replay.so, then python Q044_SPLINE_VALIDATE.py ./native_replay.so. No GitHub launcher target or new PROGRAM_ID is created; these are bounded local component tools, not a registered production campaign. Remote README/registry/source files remain unchanged. Previous local control patches remain historical, not installed. No archives are delivered.

Source/artifact metadata, stable source IDs and new claim map:

```json
{
  "date_utc": "2026-10-09T15:03:30.148137+00:00",
  "new_source_records": [
    {
      "source_id": "I-Q044-V29-BYTE-RECOVERY-001",
      "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
      "title": "Original V29 context artifact byte recovery and member audit",
      "year": 2026,
      "repository": "Morfindien/Bubbleverse",
      "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
      "run_id": 37362125253,
      "artifact_id": 11366628579,
      "archive_sha256": "3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9",
      "source_file": "Q044_V29_RECOVERY.json",
      "sha256": "46f66fba8405a1d9ddf8a08911a8b404ca24586aa88d9a2b4f1e47e52275212c",
      "supports": "Actual frozen grid/context bytes; all 17 declared artifact-member hashes match. No V31 raw history recovered."
    },
    {
      "source_id": "I-Q044-SPLINE-ADJOINT-001",
      "type": "BUBBLEVERSE MATHEMATICAL / NUMERICAL COMPONENT RESULT",
      "title": "Support-dependent adjoint weights and conditional native-plus box enclosure",
      "year": 2026,
      "result_id": "R-Q044-SPLINE-ADJOINT-001",
      "input_file": "Q044_SPLINE_INPUTS.json",
      "input_sha256": "f26da12d32eb40c2ae7a8ff618180bb3e495b5f3d183a16f65c09ff97f98fa0c",
      "program": "Q044_SPLINE_ADJOINT.py",
      "program_sha256": "bbd93f22e0da56be9c74fb109e60ddd1dab1f31a76641ab47e2a735d232147fd",
      "result": "Q044_SPLINE_RESULT.json",
      "result_sha256": "25638274b3898d97f63d1ecbb06739797396659d02270ab80e37d4bdf5b2354e",
      "supports": "Conditional exact-real native-plus hull on all 138 and 3002 inherited support candidates; no cosmological inference."
    },
    {
      "source_id": "I-Q044-SPLINE-CHECKS-001",
      "type": "BUBBLEVERSE TECHNICAL VALIDATION",
      "title": "Exact rational fixtures, native component replay and full support coverage",
      "year": 2026,
      "program": "Q044_SPLINE_VALIDATE.py",
      "program_sha256": "5363a1b7ce437c0c87f195b9cbd7d58685d0f785da22236e09337503d1918d67",
      "result": "Q044_SPLINE_CHECKS.json",
      "result_sha256": "5300cd20e40c2ff43ee48ec1a0ad1b9ef487639bd2aa2fae7d1ce9911861948f",
      "supports": "64 exact-rational fixture cases, 18 native-C component diagnostics and complete candidate enumeration. Not global floating-error or posterior qualification."
    },
    {
      "source_id": "I-Q044-NATIVE-PIN-RECHECK-001",
      "type": "OFFICIAL CODE SOURCE / TECHNICAL PROVENANCE",
      "authors": "mwt5345/class_ede repository contributors",
      "title": "Pinned arrays.c and thermodynamics.c native reionization functional",
      "year": "NOT DOCUMENTED",
      "repository": "mwt5345/class_ede",
      "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c",
      "arrays_sha256": "c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4",
      "thermodynamics_sha256": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
      "supports": "Unchanged native estimated derivatives; plus correction; rows 0..N-1; sign flip; argmin0 tau0 and N<3 clamp. Not independent observations."
    }
  ],
  "new_claim_to_source_map": {
    "C-Q044-S01": {
      "claim": "Frozen V29 actual grid/context recovered with all declared member hashes matching.",
      "sources": [
        "I-Q044-V29-BYTE-RECOVERY-001"
      ]
    },
    "C-Q044-S02": {
      "claim": "Each admissible prefix has its own linear functional a_N; adjoint residual bounds enclose coefficients in real arithmetic.",
      "sources": [
        "I-Q044-SPLINE-ADJOINT-001",
        "I-Q044-NATIVE-PIN-RECHECK-001"
      ]
    },
    "C-Q044-S03": {
      "claim": "All inherited candidate supports have a computed conditional scalar hull under the inherited hydrogen rail and 33 source witnesses per trial.",
      "sources": [
        "I-Q044-SPLINE-ADJOINT-001",
        "I-Q042-V31-INGESTION-001"
      ]
    },
    "C-Q044-S04": {
      "claim": "64 rational cases and18 C replay cases pass within scoped diagnostic definitions; no uniform original-binary rounding bound.",
      "sources": [
        "I-Q044-SPLINE-CHECKS-001"
      ]
    },
    "C-Q044-S05": {
      "claim": "No H0, EDE preference, equivalence, physical falsification or reference truth is established.",
      "sources": [
        "I-Q044-SPLINE-ADJOINT-001",
        "I-Q044-SPLINE-CHECKS-001",
        "I-Q044-CONTRACT-001"
      ]
    }
  },
  "delivered_reproduction_sha256": {
    "Q044_SPLINE_ADJOINT.py": "bbd93f22e0da56be9c74fb109e60ddd1dab1f31a76641ab47e2a735d232147fd",
    "Q044_SPLINE_VALIDATE.py": "5363a1b7ce437c0c87f195b9cbd7d58685d0f785da22236e09337503d1918d67",
    "Q044_NATIVE_REPLAY.c": "56c92da28d7200c8b9b88dff8f1fe7e9a0b1dc21cc464d17e39b4fe48eef3641",
    "q042_interval_v29.py": "558592e20969dbfc063570f2224c36b4e8d7dca37db20009cb5dd2a993e0d160",
    "Q044_SPLINE_INPUTS.json": "f26da12d32eb40c2ae7a8ff618180bb3e495b5f3d183a16f65c09ff97f98fa0c",
    "Q044_SPLINE_RESULT.json": "25638274b3898d97f63d1ecbb06739797396659d02270ab80e37d4bdf5b2354e",
    "Q044_SPLINE_CHECKS.json": "5300cd20e40c2ff43ee48ec1a0ad1b9ef487639bd2aa2fae7d1ce9911861948f",
    "Q044_V29_RECOVERY.json": "46f66fba8405a1d9ddf8a08911a8b404ca24586aa88d9a2b4f1e47e52275212c"
  },
  "incoming_journal_sha256": "e9363e8a236a955ab1fe258e27c09c4484771540bb19948f838d271c1b2bc26d",
  "environment": {
    "python": "3.12.14",
    "platform": "Linux-6.18.44-x86_64-with-glibc2.39",
    "numpy": "2.3.5",
    "MPFR": "4.2.1"
  },
  "raw_V31_node_sha256": {
    "UPPER": "a42fff6504cdb50532e3dca95c8cc4d9e9251e548b0008d1b9388cc5a1793d25",
    "LOWER": "ae785faeb9658fac5516cca176c125767b8aa20b64d60aa85b1e116c536eb98b"
  },
  "inference_accuracy_requirement": "NOT AVAILABLE",
  "production_restart_authorized": false
}
```

## Preserved complete incoming SAMLET JOURNAL — verbatim historical state

# BUBBLEVERSE — RESULT INGESTION & ROUTING HANDOFF

RD OF THE UNIVERSE

## SAMLET JOURNAL — effective ingestion update

CURRENT Q: Q044. CASE ID: NOT DOCUMENTED. STATUS: CONTINUES.
RESULT-ID: R-Q044-INGESTION-001.
EXACT QUESTION: Under the original Q041 matched-data and prior contract, does the CamSpec–HiLLiPoP implementation difference produce a material difference in H0 constraints or the n_scf = 3 EDE-versus-ΛCDM conclusion once numerical prediction accuracy and posterior convergence are qualified, or is the downstream result equivalent or conditional on the external dataset combination?

This is the same authoritative attached journal updated differentially. The complete incoming 168,679-byte Q044 journal is retained verbatim below. These effective entries govern current routing; older instructions remain historical. The complete supplied 91-source register, claim-map trees, later source additions, code/output and prior case records survive. No separately missing global master journal is reconstructed.

### J-044-16 — Ingestion and qualification boundary

[TECHNICAL VALIDATION] All five attachments match recorded hashes; the decision's three declared delivery hashes agree. Four embedded JSON blocks parse. The original 91 source IDs are unique and both inherited map trees remain intact. Seven reported offline resolver outcomes are internally consistent; they were not independently rerun in this ingestion. Accept I-Q044-EXECUTION-QUALIFICATION-001 as scoped design, native-source and local-control evidence. Do not promote it to an implemented support hull, complete physical reference or cosmological result.

### J-044-17 — New structural direction and anti-loop check

[DERIVED CONDITIONAL STRUCTURE / ROUTING INFERENCE] At fixed valid conformal-time knots, native estimated-derivative endpoint formulas are linear in supplied ordinates. The real-arithmetic spline solve and declared integral therefore define a support-specific linear functional T_N(y)=a_N^T y. Its exact range over an independent ordinate box is obtained by sign-selected endpoints of each term. Prefix-dependent coefficients, uncertain knots, shared correlations and original-binary rounding must remain separately accounted for. No weights, measured width or tau enclosure were computed here.

The selected next engine is the operator-established AUTONOMOUS MATHEMATICS ENGINE, with one narrowed support-functional sensitivity/enclosure task. This supersedes the earlier immediate generic instruction to instantiate all missing qualification categories at once. No repeated TV proof, generic missing-reference report, hash audit, launcher retest or unchanged historical numerical run is selected. The new task must yield a new bound or a concrete candidate obstruction.

### J-044-18 — Current repository provenance and controls

[TECHNICAL SOURCE RECHECK] Connected GitHub branch refs are unchanged: execution72cf9e92fc794c122f593a77b6a555e6e97f6a2e; modeldd7575e7146382957d206e87274ca6246c2587b7. Original V29 artifact metadata lists two unexpired products at the original execution SHA. Metadata alone does not validate their contents; no artifact bytes were downloaded here. The local prepared README/registry and stale remote state remain separate. No remote write, workflow dispatch or numerical production occurred.

### J-044-19 — Completion, anomalies and journal delta

Q-COMPLETION_GATE=NOT_YET_SATISFIED. The exact original downstream question has no qualified materiality/equivalence/dataset-conditional verdict. A specific unassessed support-functional route can still materially affect numerical qualification. A template/blocker certificate alone does not settle the question; an inconclusive closure remains legitimate if the bounded new task demonstrates no specific accessible materially informative path remains.

KEEP all physical parameters/candidates, H0 benchmark gaps, Q035–Q043 boundaries, open portability predictions and C-036-IMPL=OPEN_NARROWED. No new anomaly, H0, model preference or physical falsification is inferred. ADD I-Q044-INGESTION-001 and I-Q044-REPOSITORY-RECHECK-001 plus C-Q044-I01–I05 source mappings. REFINE current next action only. PRODUCTION_RESTART_AUTHORIZED=false. NEXT ENGINE=AUTONOMOUS MATHEMATICS ENGINE.

## Current full ingestion handoff and source/claim delta

Assembly time: 2026-10-09T15:03:42.063378+02:00 / 2026-10-09T13:03:42.063378+00:00.

# BUBBLEVERSE — RESULT INGESTION & ROUTING HANDOFF

Date and time: 2026-10-09T15:03:42.063378+02:00 (Europe/Copenhagen); 2026-10-09T13:03:42.063378+00:00 (UTC).

STATUS: CONTINUES
CASE ID: NOT DOCUMENTED
CURRENT Q: Q044 — preserved operator-proposed scientific identifier; remote canonical registration not performed.

QUESTION:
Under the original Q041 matched-data and prior contract, does the CamSpec–HiLLiPoP implementation difference produce a material difference in H0 constraints or the n_scf = 3 EDE-versus-ΛCDM conclusion once numerical prediction accuracy and posterior convergence are qualified, or is the downstream result equivalent or conditional on the external dataset combination?

This is the exact original operator-supplied question. Shorter formulations in historical Q044 files are retained as historical summaries, not replacements.

## RECOMMENDED CHATGPT EXECUTION PROFILE

Available capabilities: Work/Codex file and Python access, connected GitHub file/branch/run/artifact retrieval, web/primary-source research, Library delivery and parallel-agent facilities. No agents were spawned. The exposed candidate catalogue includes GPT-6.1 Sol, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol and GPT-6 Luna; it does not establish the operator's complete selector, current exact model/reasoning, context limits, usage limits or comparative mathematical reliability.

Recommended model/mode: a strong mathematical reasoning configuration in Work/Codex; GPT-6.1 Sol with High reasoning if selectable. Recommended style: focused autonomous derivation plus bounded source/file analysis. Class C with relevant Class E tools under this ingestion prompt's capability taxonomy. Fallback: strongest equivalent available reasoning configuration. Escalate only if prefix-dependent linear algebra, joint uncertainty or switched-equation assumptions exceed its reliable scope. ASTRA MAX is not assumed available or automatically superior.

Recommended tools: pinned GitHub/native-source access and local symbolic/exact or outward-rounded calculation. Optional: targeted primary numerical-analysis sources if a specific theorem or rounding bound is needed. Generic cosmology searches, extra model comparisons and production compute add no current qualification evidence and are not selected.

## SELECTED NEXT BUBBLEVERSE ENGINE

BUBBLEVERSE — THE AUTONOMOUS MATHEMATICS ENGINE.

Exactly one scientific destination. The engine is established by the operator's full Mathematics Engine prompt in this session. It is not inferred from an unverified repository filename or invented as a new motor. Consistency checks are part of its task, not a second routing destination.

## SAMLET JOURNAL

The complete updated authoritative journal is delivered individually as Q044_SAMLET_JOURNAL.md. It includes this ingestion/routing decision and the entire 168,679-byte incoming journal byte-for-byte, including the original 91-source register, both complete inherited claim-map trees, later Q044 source records, proofs, synthetic check code/output and historical Q043 record. A full global master journal beyond the supplied cumulative record remains NOT RECOVERED; this gap is preserved, not repaired by invention.

## NEW RESULT

Received result ID: I-Q044-EXECUTION-QUALIFICATION-001.
Ingestion result ID: R-Q044-INGESTION-001.
Origin: Autonomous Execution-Mechanism / Numerical / HPC / Motor-Builder Engine.
Result classes: TECHNICAL DESIGN / SOURCE RESULT / CONDITIONAL MATHEMATICAL RESULT / LOCAL VALIDATION RESULT.
Result status: ACCEPTED WITH SCOPE LIMITS. Received control tests are TECHNICALLY VALIDATED locally; the new support representation is UNIMPLEMENTED and scientific inference UNQUALIFIED.

DIRECT OUTPUT: All five received file hashes match the prior documented delivery and the decision's three declared control/protocol hashes. No new cosmological result is contained in them. The recorded seven offline resolver cases have the expected accept/reject outcomes. Their script was not independently rerun during ingestion. Current GitHub branch refs still match the received execution/model pins. Two V29 artifacts are listed, unexpired, at the original execution SHA. Their bytes were not downloaded in this ingestion.

TECHNICAL INTERPRETATION: The protocol and blocker certificate are usable for defining a new qualification component. The pair of local control files retires V29 correctly within its documented scope; it has not been installed remotely. A support hull can avoid retaining every support interval in the final output, but it does not automatically improve width, runtime, complete-history coverage or prediction accuracy. Support-dependent spline coefficients prevent unproved reuse of a single common-spline prefix sum.

PHYSICAL INTERPRETATION: No material H0 shift, EDE preference, equivalence, dataset dependence or physical causality has been established. Scientific hypotheses and the observed implementation-geometry discrepancy retain their previous states. Technical failure is not physical falsification; compact output is not an accuracy certificate.

ANOMALY STATUS: C-036-IMPL remains OPEN_NARROWED; its causal origin and downstream significance are unresolved. The legacy-plus versus exact-cubic-minus functional distinction is a preserved known technical discrepancy, not newly discovered physics. No new scientific anomaly is declared.

## INTERNAL RESULT PROVENANCE

Incoming assembly: 2026-10-09T12:51:49.966136+00:00.
Current ingestion assembly time and five hashes: Q044_INGESTION_RESULT.json and updated journal.
Execution repository: Morfindien/Bubbleverse, main 72cf9e92fc794c122f593a77b6a555e6e97f6a2e.
Model repository: Morfindien/bubbleverse-model, main dd7575e7146382957d206e87274ca6246c2587b7.
Native source: mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Native arrays.c SHA256 c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4; thermodynamics.c d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6.
V29 run37362125253, attempt1, is inherited completed/success technical evidence. Native MPFR version256-bit arithmetic uses MPFR4.2.1 in V29's frozen contract; it is not a declaration of a new runtime execution here.
PROGRAM_ID: NONE NEW. Workflow dispatch, new integration, new posterior/optimizer calculation and production restart: NONE. Remote mutation: NONE. Hardware/compiler/solver for a new numerical result: NOT APPLICABLE.

## WEB / PLUGIN / TOOL RESEARCH

Research performed: YES — targeted technical provenance verification only.
Capabilities: connected GitHub branch-ref and workflow-artifact metadata; local attached-file hashing/JSON/source inspection. One artifact-tool call initially used the wrong repository argument and returned an argument-binding error; the corrected call succeeded. The failure created no result.
Questions: Do the input files match? Has a newer repository state superseded their pins? Are original V29 artifacts still listed? Does the proposed next step repeat old work?
New external cosmological evidence: NONE. New measurement/independent scientific replication: NONE. Artifact metadata establishes listing/retention/declared digest, not archive contents or scientific validity.
Contradictory evidence: NONE NEW. The prepared COMPLETED registry and stale remote ACTIVE registry are different deployment states, not conflicting cosmological observations.
Impact: retain all science; refine next action to a specific support-functional sensitivity calculation rather than repeat a general qualification template or reopen Q042.

## ACTIVE SOURCE REGISTER AND CLAIM MAP

All inherited source objects and claim maps remain inside the same journal. Necessary active records include:

- I-Q044-CONTRACT-001 and I-Q042-TREATMENT-003: original internal scientific contract, q042_production_spec_v1.json; SHA256 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c. Supports unchanged 20-cell design and decision rules.
- I-Q044-SOURCELOCK-001: q042_production_source_lock_v1.json; SHA256 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56. Supports frozen software/data dependencies, not installed-runtime correctness.
- I-Q044-CLASSIFIER-001: frozen q042_production_v1.py; SHA256 889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642. Supports descriptive D, three-grid overlap, within-arm improvements and non-exhaustive final labels.
- I-Q044-MATH-QUALIFICATION-001: conditional inference-error derivations and synthetic cross-checks in the journal. Not an observed cosmological result.
- I-Q044-EXECUTION-QUALIFICATION-001, I-Q044-NATIVE-SUPPORT-001 and I-Q044-CONTROL-001: received design, pinned native-source inspection and local control evidence.
- I-Q042-COMPARISON-V31-001 / VALIDATION-001 / I-Q042-V31-INGESTION-001: partial V31 history and conditional cap32 incompatibility, not complete tau or reference truth.
- K-Q042-INGESTDESIGN-001 and K-Q042-V24-001: pinned native spline and thermodynamics source. Fixed-grid spline coefficients are linear in supplied ordinates in real arithmetic; binary-rounding error is separate.
- I-Q044-INGESTION-001: present attached-file identity/continuity, scope, completion and routing audit.
- I-Q044-REPOSITORY-RECHECK-001: current GitHub refs and original V29 artifact metadata. Final artifact11366943024 digest6c8b5aa8bc98aa8040df4b5906e4ce5899f3997b3320c7313159f783ea8aa4c1; context artifact11366628579 digest3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9. Metadata only, not a fresh byte audit.

Current mappings:
C-Q044-I01 (received result is a scoped design/control result) → I-Q044-EXECUTION-QUALIFICATION-001, I-Q044-CONTROL-001, I-Q044-INGESTION-001.
C-Q044-I02 (no qualified scientific comparison exists in received evidence) → I-Q044-MATH-QUALIFICATION-001, I-Q044-EXECUTION-QUALIFICATION-001 and preserved Q041/Q042 failures.
C-Q044-I03 (support-functional sensitivity is a distinct material next task) → I-Q044-NATIVE-SUPPORT-001, K-Q042-INGESTDESIGN-001, I-Q044-INGESTION-001; status ROUTING INFERENCE / CONDITIONAL MATHEMATICAL STRUCTURE.
C-Q044-I04 (remote pins unchanged; V29 artifacts listed) → I-Q044-REPOSITORY-RECHECK-001.
C-Q044-I05 (complete supplied journal/source/map continuity) → input journal hash and exact suffix preservation in I-Q044-INGESTION-001.

## WHAT CHANGED / WHAT DID NOT CHANGE

ADD acceptance with explicit scope, current metadata, and a narrower next task. REFINE the earlier generic instruction to instantiate all missing qualification prerequisites at once. That instruction is SUPERSEDED for immediate routing, not deleted.
KEEP exact Q, physical model/prior/data definitions, thresholds, H0 benchmarks and bibliographic gaps, active candidates, unresolved predictions and geometry tension. Q042 stays CLOSED INCONCLUSIVE; Q043's original local-only result stays historical. Q044 remains scientifically OPEN.

## FALSIFIED / REJECTED / SUPERSEDED MATERIAL

Preserve all prior exclusions: Q040 invalid endpoints; Q041 V19 as a substitute for the full contract; classifier labels as invariant modes; unchanged V31 completion-by-time-alone; retroactive cap enlargement; partial records as complete histories; diagnostic references as qualified scientific truth; finite-start flags as global minima; cross-arm absolute chi2 arithmetic; timeout as physical falsification. No new hypothesis is falsified by this ingestion.

## OPEN UNCERTAINTIES AND Q-COMPLETION GATE

STATUS: NOT YET SATISFIED.
The exact downstream question has neither qualified 20-cell results nor demonstrated operational equivalence. Four missing categories remain: complete history/input/switch coverage; support-functional error bounds; observable/native-likelihood/domain/tail transport; sampling/optimizer qualification.

An INCONCLUSIVE closure is legitimate when the remaining evidence cannot support further material progress. It is not selected merely because an unexecuted candidate is difficult. Here a specific new mathematical route remains: exploit fixed-grid linearity without pretending different supports share their coefficients. Its ability to produce useful bounds has not been assessed. Its answer can materially change whether a qualified comparison is feasible and hence the downstream verdict. Completion of a template and launcher tests does not close the original scientific Q.

## MATERIAL-REVERSAL TEST / ANTI-LOOP DECISION

PASS for the next task only. Repeating source hashes, seven resolver tests, posterior TV proofs, generic literature surveys or unchanged V26–V31 runs is not selected. The next result must provide a new support-dependent functional sensitivity/enclosure or a specific failure of that candidate; another generic list of missing references is insufficient information gain.

## NEXT TASK — ONE BOUNDED MATHEMATICAL COMPONENT

Determine whether support-specific linear functionals can provide a rigorous and usefully tighter tau-functional hull under the frozen native semantics, without requiring storage of every support interval or using unproved common-spline coefficients.

For a fixed valid conformal-time grid and each distinct N, use the native estimated-derivative boundary conditions to derive the real-arithmetic linear operator M_N=B_N y. Then the declared native-plus or separately identified exact-cubic-minus functional has T_N(y)=a_N^T y. Prefix dependence remains in B_N and a_N. For independently bounded ordinates y_i∈[l_i,u_i] and exact weights, extrema of that linear functional over the box are sums of sign-selected endpoints. Correlations make this a conservative box bound; exploiting them requires justified joint constraints. Uncertain grid/coefficients and original-binary rounding require separate outward bounds. This is a prospective structural route, not a currently computed weight vector or tau enclosure.

Recover original V29 grid/context from existing archived products if needed, verify recorded hashes, and reuse V31 node/candidate/rail evidence where its actual bytes are available. Do not replace missing nodes with point guesses. If V31 raw products are unavailable, report exact missing paths/hashes, and distinguish an algebraic component result from an uncomputed physical-data hull. Published archive metadata alone is not enough to claim recovered numerical inputs.

Deliver: declared target functional; support-specific weight/enclosure derivation; finite independent checks appropriate to that component; actual conditional hull/width and uncertainty-source decomposition if valid inputs permit; otherwise a finite unsupported-input/candidate-failure certificate. State whether its precision is assessed against a justified tau-to-observable/likelihood requirement. If that requirement remains absent, mark INFERENCE ADEQUACY UNDETERMINED; do not invent a tolerance or equate compactness with accuracy.

## FIXED / FROZEN ELEMENTS

Q044 and exact question; full journal/source IDs; original matched 20 cells; native nuisance treatment; physical models; priors; external datasets; source commits; support candidate admissibility; excluded final row; i=0 and N=max(3,i) behavior; decreasing eta orientation; original plus-sign functional identity; all frozen scientific decision thresholds; no production authorization.

## VARIABLE ELEMENTS

New numerical representation and mathematical elimination/adjoint method only, with explicit new lineage. Error-allocation and rounding method may be proposed prospectively with justification. No physical equation, dataset, prior, endpoint or threshold is changed to obtain a desired category.

## SUCCESS / FAILURE / STOP CONDITIONS

SUCCESS: a source-matched support-dependent operator and validated bound, with explicit actual-data applicability and a defensible adequacy assessment or clearly bounded remaining transport dependency. It is a component success, not by itself a scientific Q044 result.
FAILURE: a demonstrated source mismatch, invalid coefficient/grid bound, missing indispensable raw input, or proven inadequate width under a stated justified requirement. Preserve the result and its tested scope. Candidate failure does not establish universal impossibility or model falsification.
STOP THIS COMPONENT: when the new bound/width or a concrete obstruction is documented; return to ingestion without an automatic precision ladder, new integration or production restart.
STOP Q044 AND SEND TO MOTOR14: when qualified results answer the unchanged scientific question, or a defensible scoped INCONCLUSIVE outcome is documented and no specific accessible remaining task is reasonably likely to materially alter it. Preserve open portability predictions even if Q044 closes inconclusively. A future materially new qualified reference/representation may support a future investigation; it is not evidence already obtained.


## Current machine-readable ingestion evidence

```json
{
  "result_id": "R-Q044-INGESTION-001",
  "q": "Q044",
  "case_id": "NOT_DOCUMENTED",
  "date_copenhagen": "2026-10-09T15:03:42.063378+02:00",
  "date_utc": "2026-10-09T13:03:42.063378+00:00",
  "result_status": "ACCEPTED_WITH_SCOPE_LIMITS",
  "received_result_id": "I-Q044-EXECUTION-QUALIFICATION-001",
  "input_files": {
    "Q044_SAMLET_JOURNAL.md": {
      "sha256": "36c9db2a447974feb3db371bc9250fa3ddd85d1874a7b07368e5d6a817167a9a",
      "bytes": 168679,
      "identity_match": true
    },
    "Q044_QUALIFICATION_PROTOCOL.md": {
      "sha256": "7203b9aa87673ef5a21ac87ff3afb880dd89c7d5d48c581e0587e41cd51f64ea",
      "bytes": 18458,
      "identity_match": true
    },
    "Q044_EXECUTION_DECISION.json": {
      "sha256": "573d209648796096cf537965cb42c8b4635d68e54df9dd05fbc570d287a9312d",
      "bytes": 5579,
      "identity_match": true
    },
    "README.md": {
      "sha256": "9a9653d342ad2e14dd7389394d094346c6938f8ef48e2f22f35e4c98410c57c7",
      "bytes": 22297,
      "identity_match": true
    },
    "bubbleverse_program_registry.json": {
      "sha256": "ef76c23688fd8b698526262c6b655b666e7467b4132e4cb7661ab0757ea7cee7",
      "bytes": 85915,
      "identity_match": true
    }
  },
  "journal_continuity": {
    "incoming_bytes": 168679,
    "incoming_lines": 2601,
    "original_source_object_count": 91,
    "unique_original_source_ids": 91,
    "original_source_block_sha256": "6ec529f98b021b4d7727b4b306fa612e78b489935287c43685fd27bed5678c36",
    "original_claim_map_block_sha256": "2bab59dfcf039aab36eaac9e19e16851b19d8611df3144a0a4a599508a4bc67d",
    "all_original_bytes_retained": true,
    "global_master_journal_gap": "INHERITED_NOT_RECOVERED"
  },
  "validation_scope": {
    "reported_control_cases": 7,
    "reported_control_cases_consistent": true,
    "control_cases_independently_rerun_here": 0,
    "new_numerical_execution": false,
    "new_posterior_or_optimizer_results": false,
    "new_scientific_result": false
  },
  "current_repository_refs": {
    "execution": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "model": "dd7575e7146382957d206e87274ca6246c2587b7",
    "method": "CONNECTED_GITHUB_BRANCH_REF_READ",
    "unchanged_from_received": true
  },
  "v29_artifact_metadata": {
    "artifacts": [
      {
        "id": 11366943024,
        "name": "q042-v29-37362125253-final",
        "size_in_bytes": 3826149,
        "url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11366943024",
        "archive_download_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11366943024/zip",
        "expired": false,
        "created_at": "2026-10-05T19:23:08Z",
        "expires_at": "2026-11-04T19:23:06Z",
        "updated_at": "2026-10-05T19:23:08Z",
        "digest": "sha256:6c8b5aa8bc98aa8040df4b5906e4ce5899f3997b3320c7313159f783ea8aa4c1",
        "workflow_run": {
          "id": 37362125253,
          "repository_id": 1348235216,
          "head_repository_id": 1348235216,
          "head_branch": "main",
          "head_sha": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e"
        }
      },
      {
        "id": 11366628579,
        "name": "q042-v29-37362125253-context-and-checks",
        "size_in_bytes": 3655994,
        "url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11366628579",
        "archive_download_url": "https://api.github.com/repos/Morfindien/Bubbleverse/actions/artifacts/11366628579/zip",
        "expired": false,
        "created_at": "2026-10-05T19:22:35Z",
        "expires_at": "2026-11-04T19:22:33Z",
        "updated_at": "2026-10-05T19:22:35Z",
        "digest": "sha256:3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9",
        "workflow_run": {
          "id": 37362125253,
          "repository_id": 1348235216,
          "head_repository_id": 1348235216,
          "head_branch": "main",
          "head_sha": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e"
        }
      }
    ]
  },
  "artifact_bytes_downloaded_here": false,
  "technical_source_inspection": {
    "source": "mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c",
    "scope": "Fixed-grid real-arithmetic estimated-derivative spline coefficients are linear in ordinates; binary-rounding and uncertain-grid errors are separate",
    "source_sha256": "c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4"
  },
  "q_completion_gate": "NOT_YET_SATISFIED",
  "scientific_answer": "UNRESOLVED_NO_QUALIFIED_DOWNSTREAM_COMPARISON",
  "material_reversal_test": "PASS_SPECIFIC_SUPPORT_FUNCTIONAL_SENSITIVITY_TASK",
  "selected_next_engine": "BUBBLEVERSE_AUTONOMOUS_MATHEMATICS_ENGINE",
  "exact_next_task": "Derive support-dependent linear weights/enclosures under native boundary/functional semantics and assess whether an outward support hull materially improves precision; preserve actual-data applicability and missing transport budget. No generic template repetition.",
  "new_program_id": null,
  "production_restart_authorized": false,
  "remote_write_performed": false,
  "control_files": "UNCHANGED_LOCAL_PREPARED_NOT_INSTALLED",
  "new_sources": [
    "I-Q044-INGESTION-001",
    "I-Q044-REPOSITORY-RECHECK-001"
  ],
  "new_claim_map": {
    "C-Q044-I01": [
      "I-Q044-EXECUTION-QUALIFICATION-001",
      "I-Q044-CONTROL-001",
      "I-Q044-INGESTION-001"
    ],
    "C-Q044-I02": [
      "I-Q044-MATH-QUALIFICATION-001",
      "I-Q044-EXECUTION-QUALIFICATION-001"
    ],
    "C-Q044-I03": [
      "I-Q044-NATIVE-SUPPORT-001",
      "K-Q042-INGESTDESIGN-001",
      "I-Q044-INGESTION-001"
    ],
    "C-Q044-I04": [
      "I-Q044-REPOSITORY-RECHECK-001"
    ],
    "C-Q044-I05": [
      "I-Q044-INGESTION-001"
    ]
  },
  "stop_condition": "Return after a new component bound or concrete obstruction. Close Q044 to Motor14 only on qualified unchanged scientific answer, or defensible scoped inconclusive outcome with no specific accessible materially informative path.",
  "handoff_sha256": "d0b0b7bd34c3c5e055b40897ffd378ca543f614bd3e64d65e43e5a62ee4608db"
}
```

## Complete incoming Q044 journal — preserved historical accumulated record

Input SHA256: 36c9db2a447974feb3db371bc9250fa3ddd85d1874a7b07368e5d6a817167a9a; bytes168679. The following original bytes remain exact. Earlier dates/status/routing describe their original stage.

# BUBBLEVERSE — OVERLEVERING

RD OF THE UNIVERSE

Date and time verified at assembly: 2026-10-09T12:51:49.966136+00:00 (UTC).

CURRENT Q: Q044. STATUS: CONTINUES / SCIENTIFIC ANSWER UNRESOLVED.
CURRENT STAGE: EXECUTION-MECHANISM DECISION AND PROSPECTIVE REFERENCE-ACCURACY QUALIFICATION.
RESULT-ID: I-Q044-EXECUTION-QUALIFICATION-001.
NEXT DESTINATION: RESULT INGESTION & ROUTING, retaining Q044; next scientific work belongs to the existing Mathematics/Consistency Engine.

## SAMLET JOURNAL — effective differential update

This is the same authoritative supplied journal, updated differentially. The entire incoming Q044 journal is retained byte-for-byte below as historical accumulated state; its complete 91-source register and both inherited claim-map trees remain present. The effective entries here and the embedded current protocol supersede earlier next-engine/current-head/control instructions only where stated. No missing global master journal is recreated.

### J-044-12 — Execution decision

[TECHNICAL RESULT] The smallest current mechanism is the existing Mathematics/Consistency Motor plus pinned repository retrieval. A prospective qualification protocol and finite blocker certificate have been completed. They are not an instantiated executable numerical campaign: no complete qualified history, observable/native-likelihood transport, support/tail certificate or sampling/optimizer error input has been established. No new motor, PROGRAM_ID, workflow, production run or cosmological result was created. Q044 remains OPEN, and production_restart_authorized=false.

### J-044-13 — Native support representation

[SOURCE VERIFIED / DERIVED CONDITIONAL DESIGN] Pinned native source independently confirms strict first-minimum selection excluding the final native row; i=0 gives zero; otherwise N=max(3,i) uses rows0..N−1. Estimated spline endpoint derivatives and coefficients depend on N. A fixed-spline prefix accumulator cannot silently replace the native support computations. A hull of all separately valid support-specific functional intervals preserves their coverage and can use compact final storage. This new representation is not implemented or qualified, does not reproduce V31, and establishes neither useful precision nor runtime nor physical feasibility. Its naive work is O(sum N), not automatically O(n).

[SOURCE VERIFIED] Native arrays.c uses plus-curvature integration, whereas the mathematical integral of its usual cubic spline has minus-curvature. These must be separate declared targets. No operator/sign replacement or native binary replay occurred. The previously documented V31 sign/arithmetic audit remains inherited.

### J-044-14 — Current repository/control evidence

[VERIFIED BRANCH REFS] Execution main=72cf9e92fc794c122f593a77b6a555e6e97f6a2e; model main=dd7575e7146382957d206e87274ca6246c2587b7. Accepted model remains v0.4/R000004 through Q042, production false. Earlier head observations retain their time-specific provenance.

[VERIFIED TECHNICAL COMPLETION] GitHub run37362125253 attempt1 is completed/success at the execution pin. This supports V29 COMPLETED_PREREQUISITE_ONLY, not a qualified reference. The live registry still calls V29 ACTIVE and README still directs its launch at the inspected pin. Paired local registry/README corrections are prepared; only the V29 registry entry changes. Immutable manifest and launcher stay unchanged. Seven offline executions of the actual launcher resolver pass expected outcomes: completed V29/V28, unknown identifier, unsafe identifier, invalid Q and unsafe workflow are rejected; one isolated ACTIVE fixture is accepted. No gh dispatch step is executed. Gates PASS only for this local control scope; remote remains unpatched.

### J-044-15 — Journal effect, evidence and next task

KEEP all scientific/hypothesis/parameter/prediction/contradiction states and rejected endpoints. ADD the protocol, finite unsupported-input certificate and local control evidence. UPDATE current repository observations and effective next action. Scientific evidence remains INSUFFICIENT for Q044. No H0 shift, tau, posterior, contour overlap or EDE preference is calculated here. No universal impossibility is inferred.

New source IDs: I-Q044-EXECUTION-QUALIFICATION-001 (protocol and blocker certificate); I-Q044-NATIVE-SUPPORT-001 (native thermodynamics.c and arrays.c at pinned CLASS source); I-Q044-CONTROL-001 (verified completion receipt, paired local correction and offline resolver tests). All are mathematical/technical lineage, not independent cosmological observations. Exact upstream hashes match the inherited source lock. All existing source IDs stay unchanged.

NEXT REQUIRED ACTION: ingest this bounded result, then instantiate the earliest missing qualified original-context history/input and support-specific functional prerequisite using the existing motor. Numerical/HPC implementation becomes appropriate when an exact component target, valid inputs, prospective budget and finite result tests exist. Do not repeat old acquisitions merely to fill a workflow or launch production under stale metadata.

## Current complete execution protocol

# BUBBLEVERSE — Q044 EXECUTION DECISION AND QUALIFICATION PROTOCOL

RD OF THE UNIVERSE

Status: DESIGN COMPLETE; FULL REFERENCE/INFERENCE QUALIFICATION BLOCKED.
Scientific Q044 remains OPEN. This is a prospective specification and finite blocker certificate, not production clearance or a qualified cosmological result.

## A–D. Identity, setting, capabilities and mechanism

CURRENT Q: Q044, operator-proposed scientific continuation. Historical registry identifiers Q-042 remain unchanged. No canonical Q044 allocation or repository registration has been performed.

QUESTION: Under the original matched-data/prior contract, does the CamSpec–HiLLiPoP implementation difference materially change qualified H0 constraints or n_scf=3 EDE-versus-LCDM conclusions, or is the effect non-material under the frozen criteria or dataset conditional?

RECOMMENDED CHATGPT SETTING: strong reasoning in Work/Codex with repository and mathematical tools; GPT-6.1 Sol with High reasoning if selectable. Exact active variant/reasoning and the operator's selector are not verified. GPT-6 Astra and GPT-5.6 Sol are exposed delegation candidates, not proof of account-specific ASTRA MAX availability or comparative reliability. Use the strongest available extended setting if coupled switched-history proofs and observable transport exceed the bounded current task. Fallback: equivalent deep reasoning with file, code and source access. No model switch was performed.

CAPABILITIES USED: connected GitHub for pinned files, branch refs and V29 run receipt; local file/code tools for bounded control validation; Library for delivery. Retrieval is an access mechanism, not independent physical evidence. No broad literature survey, deployment tool or production compute is needed for this decision.

EXECUTION MODE: EXISTING MATHEMATICS/CONSISTENCY MOTOR + REPOSITORY RETRIEVAL. It is sufficient to deliver this bounded qualification design and blocker certificate. No new motor, cosmological program, sampler, workflow or PROGRAM_ID is needed now. Future component qualification requires genuine numerical code after its input and reference contract are instantiated; future inference requires qualified production and separate authorization.

## E–H. Scientific requirement, continuity and sources

Preserve the original 20 cells: CamSpec and HiLLiPoP; LCDM and n_scf=3 EDE; FULL, NO_ACT_PRIMARY, NO_ACT_LENSING, NO_DESI_DR2, NO_SN. Preserve native nuisance treatment, matched priors, ACT DR6 primary/lensing, DESI DR2 and frozen Pantheon+ likelihood. Preserve every threshold and completeness gate in J-044-02 of SAMLET JOURNAL. No covariance-adjusted replacement of the frozen descriptive D index is permitted. No cross-arm absolute-objective subtraction is permitted.

Scientific-contract SHA256: 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c.
Source-lock SHA256: 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56.
Execution repository pin: Morfindien/Bubbleverse@72cf9e92fc794c122f593a77b6a555e6e97f6a2e.
Model branch-ref pin inspected this stage: Morfindien/bubbleverse-model@dd7575e7146382957d206e87274ca6246c2587b7. Its accepted model remains v0.4/R000004 through Q042, production_restart_authorized=false. This supersedes earlier current-head observations, not their historical facts.
Native CLASS source pin: mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97.

Inherited source IDs remain unchanged: EVD-Q041-QJOURNAL-PDF; I-Q042-COMPARISON-V31-001; I-Q042-COMPARISON-V31-VALIDATION-001; I-Q042-V31-INGESTION-001; I-Q044-MATH-QUALIFICATION-001 and the complete historical register/maps inside SAMLET JOURNAL. The current stage adds I-Q044-EXECUTION-QUALIFICATION-001 (this specification), I-Q044-NATIVE-SUPPORT-001 (pinned native source inspection), I-Q044-CONTROL-001 (local control patch and checks). These are technical/mathematical evidence, not new external observations.

KEEP Q035–Q043 results, excluded endpoints, unresolved portability/H0 predictions, model candidates and benchmark source gaps. ADD this design and blocker certificate. UPDATE effective repository observations. No physical parameters, hypothesis status or numerical scientific result change.

## I. Repository search and reuse decision

| Material | Decision | Scope |
|---|---|---|
| q042_context_v29.py, native capture, interval evaluator, source checks, contract and manifest | REUSE/REFERENCE ONLY | Frozen context and finite interval prerequisites; not a validated trajectory |
| V26 reference-acquisition contract and V27/V28 diagnostics | REFERENCE ONLY | Raw lineage and failures; do not relaunch |
| V31 functional-cap certificate/checks in accepted model | REFERENCE ONLY | Partial-history, representation-specific cap failure; V31 source/raw products not recovered remotely here |
| Native thermodynamics.c and tools/arrays.c | REFERENCE ONLY | Exact support selection, prefix-dependent spline and legacy functional semantics |
| q042_production_spec_v1.json and source lock | REUSE unchanged | Scientific definitions; not production-ready accuracy |
| 00-bubbleverse-start.yml | UNCHANGED | Exact registry lookup; rejects non-ACTIVE identifiers |
| bubbleverse_program_registry.json | PATCH, local prepared | Mark completed V29 inactive using verified run receipt |
| README.md | PATCH, local prepared | Replace stale active/pending V29 instructions and distinguish closed Q042 from open portability science |

V29 run 37362125253, attempt1: completed/success at the pinned execution commit. The historical manifest's ACTIVE value is retained unchanged. A mutable registry correction does not rewrite its frozen execution identity. Remote README/registry remain unmodified until this paired local patch is installed. Do not apply it over newer files without rechecking the two base Git blobs: README c17bb9ce499561d02240a7a136ede6a862ae2667; registry fae212b90ccc6509f6c4193d041cd02897334d96.

## J. Prospective numerical specification

### 1. Reference target and change firewall

Before implementing a reference, declare which object is being enclosed: original binary behavior, real-equation history under its frozen switches, the native discrete tau functional, or the continuum optical-depth integral. These are different objects. Publish both computational lineage and all changed operators. Matching two discretizations is a diagnostic; it is not reference truth.

V29's MPFR256 real-equation boxes treat binary64 constants as exact inputs. They do not enclose original binary math automatically, initial/background error, all physical parameter points, or complete histories. Its finite temperature/hydrogen boxes are not an invariant-domain proof. Original switches, frozen helium residual/cutoff, phase and flags must be retained or any change explicitly assessed as an unqualified new lineage.

Required reference product: complete time-domain/history enclosure with propagated initial/background uncertainty; inclusion/existence and uniqueness or explicit set-valued solution treatment at all active switches; accepted event and interpolation handling; validated node/observable errors; documented parameter/nuisance-domain coverage or exact/approximate posterior tail bounds. No fabricated H0 prior range or missing covariance is allowed.

### 2. Candidate compressed support representation — formal design only

For eligible native rows i=0,...,n−2, let electron-fraction enclosures be X_i=[l_i,u_i]. Define m=min_i u_i and conservative candidate set S={i:l_i<=m}. Strict native comparison picks the first equal minimum; S safely overincludes ties. The actual minimum belongs to S because its lower endpoint cannot exceed the smallest upper endpoint. Preserve the excluded final row and full native order: increasing z, decreasing conformal time eta.

Native source semantics: i=0 gives tau=0. Otherwise N=max(3,i), spline and integration use rows0,...,N−1; they do not include row N. The support map is therefore not a physical endpoint substitution. Recompute `_SPLINE_EST_DERIV_` coefficients M^(N) for each distinct N; the final derivative boundary depends on N. A single fixed-spline prefix accumulator is invalid unless a separate proof establishes equivalence.

For every N, compute a directed interval J_N enclosing the SAME declared functional using all coefficient/input errors. Return H=[min_N lower(J_N), max_N upper(J_N)], adding [0,0] if i=0 is admissible. Keep candidate count, distinct support count, endpoint witnesses, complete input/support digest and coverage certificate. Every allowed functional value is in H by union containment. Correlations may enlarge H; they cannot justify shrinking it. Missing supports, incomplete history or failed coefficient bounds make the gate fail; an empty set is an error.

This replaces the storage of many output intervals with one conservative hull. It does not reproduce frozen V31 or repair that run retrospectively. It removes an output-cardinality requirement in a NEW representation, conditional on valid J_N. It neither reduces their evaluation cost automatically nor proves useful accuracy. Straight independent coefficient solves cost O(sum_N N), at most O(n^2) over all supports; auxiliary spline memory is O(max N). The final hull is two scalar endpoints plus metadata. More efficient shared recurrences would require separate proof. No actual J_N, H or tau was computed here.

Native arrays.c uses the PLUS-curvature segment expression h(y_i+y_{i+1})/2 + h^3(M_i+M_{i+1})/24, followed by the thermodynamics minus sign for decreasing eta. The exact mathematical integral of the usual cubic spline is the corresponding MINUS-curvature expression. The latter is a distinct diagnostic/reference object; silently changing the sign would not preserve original binary behavior. Frozen V31 arithmetic/sign audit remains inherited; no new physical falsification is inferred from this source inspection.

### 3. History → observables → native likelihood

For each original cell, list every consumed observable (including spectra, lensing and background/distance products), its units, transformations, likelihood normalization and parameter/nuisance support. Bound transport of initial, background, history, event, spline, root and floating-point errors into that complete vector. Use verified remainder/sensitivity bounds or another justified enclosure. A finite derivative probe or tau-only comparison cannot certify the full vector.

Evaluate the actual native likelihood. Only for a justified fixed positive-definite Gaussian covariance use |delta logL|<=v*u+u^2/2, with u=||C^(-1/2)delta t|| and v=||C^(-1/2)(D−t)||. Variable covariance/normalization and nonlinear marginalization require their own terms. Treat shared systematic/implementation errors jointly; do not assume data-block or arm independence.

Populate the journal's log-likelihood oscillation w, absolute objective error b, support/tail and sampling-summary/bin-mass errors. Use TV<=tanh(w/4), bounded-support mean/width bounds and three-grid overlap bounds exactly as J-044-05–08 specify. Absolute likelihood offsets matter for within-arm model preference even when posterior oscillation is zero. Preserve the four-start operational statistic; a globality claim needs a separate optimizer-gap certificate.

### 4. Prospective selection and blinding

Before exposing scientific arm differences, freeze parameter/nuisance-domain coverage, seed/point selection, numerical reference method, budget allocations, confidence/coverage conventions for sampling errors, refinement schedule, and stop/failure rules. Exact numerical budget values, test-point list and justified domain/tail evidence are NOT ESTABLISHED. This is a protocol template, not a fully instantiated execution preregistration.

Use component diagnostics without arm-comparison results to construct error envelopes. Refine only under the frozen rule; never choose tolerances or omit cells because the preferred scientific category fails. Certify a frozen predicate only when its whole interval lies on the appropriate side of its unchanged threshold. Straddling/equality ambiguity or the non-exhaustive frozen classifier may remain UNRESOLVED/NOT_AVAILABLE. Failure to detect materiality does not establish equivalence.

## K–N. Registration, runtime and jobs

PROGRAM_ID: NOT APPLICABLE — no new executable campaign.
PROGRAM_ID REGISTERED: NO. No target workflow was created or dispatched. No START THIS instruction applies.
Launcher: unchanged 🚀 BUBBLEVERSE START at .github/workflows/00-bubbleverse-start.yml. V29 must be rejected after the prepared completion patch; do not restart it through stale metadata or direct dispatch.

No numerical runtime/evaluation/memory estimate is defensible without a complete validated history method and frozen reference inputs. Current GitHub hard limits are therefore not used to size a fictitious job. Single-job numerical risk: UNKNOWN. No production job/shard/checkpoint/merge exists in this design. For future independent supports, shard certified N sets and merge hull endpoints only after exact support completeness/hash checks; for stateful histories checkpoint the actual integrator enclosure/event/config state and preserve genuine continuity. Measure component runtimes and verify then-current official runner limits before registering a real campaign.

## O–Q. Finite test plan and control files

| Gate | Required evidence | Current state |
|---|---|---|
| Q/contract continuity | Full journal and original contract/source hashes | PASS for recovered relevant record; global master journal gap inherited |
| Native support semantics | Pinned row selection, prefix-dependent boundary and functional identity | SOURCE VERIFIED; implementation not built |
| Component reference identity | Exact inputs and qualified coefficient/history enclosures | BLOCKED |
| Support-hull coverage | All admissible supports, ties, i=0, clamp, final-row exclusion; directed outward arithmetic; no missing supports | NOT EXECUTED |
| Functional cross-check | Independent analytic polynomial integral; distinguish native-plus and exact-minus; both time orientations; interval containment | NOT EXECUTED |
| Complete history/events | Inclusion, switches, domain, prefix/tails and initial/background uncertainty | BLOCKED |
| Prediction/native likelihood | Complete observable transport and actual normalization/covariance coverage | BLOCKED |
| Posterior/optimizer | Weights, modes/tails, estimation error and stated optimizer scope | BLOCKED |
| Twenty-cell/five-comparison completeness | Original inputs and all required outputs | NOT EXECUTED |
| Frozen decision robustness | Interval-safe thresholds, 64/80/96 overlap and original Boolean rules | Framework available; actual inputs BLOCKED |
| Local control patch | Only V29 registry entry changes; completed target rejected; unsafe/unknown IDs rejected; README corrected; launcher unchanged | Tested separately in Q044_EXECUTION_DECISION.json |

No additional test campaign is triggered merely by this design. This finite plan is mandatory when the corresponding component/inference execution exists. Diagnostic completion must remain distinct from qualification and scientific result gates.

FILE DECISIONS: CREATE this protocol and machine-readable blocker result. UPDATE the same authoritative SAMLET JOURNAL. PATCH paired README.md and bubbleverse_program_registry.json locally. UNCHANGED launcher, all native/program/contracts and historical manifests. No archive.

README_ACTION: UPDATE, local prepared. README_GATE and REPOSITORY_CONSISTENCY_GATE can pass for the paired local control correction only; remote status remains stale until installed. They do not certify the entire historical repository or science.

## R–W. Complete existing-motor invocation and return route

Use the existing MATHEMATICS/CONSISTENCY ENGINE; this is its complete focused invocation, not a new engine:

1. Read this protocol and the entire attached updated SAMLET JOURNAL. Freeze Q044 and the exact scientific question. Preserve the complete inherited source register and claim maps; use KEEP/ADD/UPDATE actions, never regenerate history from the latest result.
2. Retrieve the exact missing reference inputs and their hashes using relevant connected capabilities. Record underlying sources and dependency scope. Do not assume raw diagnostics are true histories or replace frozen source versions.
3. Instantiate the earliest blocked gate before downstream work: complete original-context products, matching history/input uncertainty, support-specific coefficient enclosures and declared target functional. Determine whether the compressed support hull can meet a prospectively selected accuracy budget. If not, give the concrete failed gate and interval width; do not broaden physical assumptions.
4. Where genuine calculation is necessary, return an actual bounded component-program specification to this execution engine with exact inputs, accepted error budgets, finite tests, runtime estimates and new-lineage identity. Register a PROGRAM_ID only once an executable target exists and the launcher/registry/README gates pass. Do not start cosmological production without qualification and separate production authorization.
5. Stop when a finite unsupported prerequisite is demonstrated or the relevant gate is qualified. No endless repeats of V26–V31, retroactive cap changes, guessed reference values or tuning to scientific results.
6. Return to RESULT INGESTION & ROUTING with Q044, the same full journal, source IDs/commits/hashes, new technical results, exact test scope, journal delta and remaining blockers. Route any genuinely qualified computation through NUMERICAL/HPC; retain Q044 throughout.

EXPECTED OUTPUTS NOW: this design; machine-readable BLOCKED certificate; updated authoritative journal; two local control replacement files. Actual scientific computed result: NOT YET COMPUTED. FINAL SCIENTIFIC RESULT GATE: UNRESOLVED. PRODUCTION RESTART AUTHORIZED: false.

Finite blocker: no complete qualified original-context history and input-error envelope, no validated observable/native-likelihood transport/domain/tail certificate, and no justified sampling/optimizer error inputs have been established in the inspected material. These missing objects prevent a qualified Q044 verdict. This is insufficient current qualification, not a theorem that computation or the physical hypothesis is impossible.


## Current machine-readable decision and control test evidence

```json
{
  "q": "Q044",
  "date_utc": "2026-10-09T12:51:49.966136+00:00",
  "record_id": "I-Q044-EXECUTION-QUALIFICATION-001",
  "execution_mode": "EXISTING_MATHEMATICS_CONSISTENCY_MOTOR_PLUS_REPOSITORY_RETRIEVAL",
  "design_status": "COMPLETE_PROTOCOL_TEMPLATE",
  "execution_readiness": "BLOCKED_NOT_INSTANTIATED",
  "scientific_question_status": "OPEN_UNRESOLVED",
  "actual_scientific_result": "NOT_YET_COMPUTED",
  "production_restart_authorized": false,
  "program_id": null,
  "remote_write_performed": false,
  "workflow_dispatched": false,
  "source_pins": {
    "execution": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "model": "dd7575e7146382957d206e87274ca6246c2587b7",
    "native_class": "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
  },
  "original_science_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
  "original_source_lock_sha256": "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56",
  "new_support_representation": {
    "status": "FORMAL_CANDIDATE_NOT_IMPLEMENTED",
    "representation": "one hull of all valid support-specific functional intervals",
    "same_spline_prefix_reuse": "NOT_VALID_WITHOUT_EQUIVALENCE_PROOF",
    "physical_feasibility": "NOT_ESTABLISHED",
    "actual_tau": "NOT_COMPUTED"
  },
  "blockers": [
    {
      "id": "B01",
      "missing": "Complete qualified original-context history plus initial/background uncertainty and switch/domain coverage",
      "blocks": "REFERENCE_TRUTH_GATE"
    },
    {
      "id": "B02",
      "missing": "Support-specific validated coefficient/function intervals and instantiated component accuracy budget",
      "blocks": "SUPPORT_HULL_QUALIFICATION_GATE"
    },
    {
      "id": "B03",
      "missing": "Complete observable-to-native-likelihood error envelope including normalization, support/tail bounds and native nuisance domains",
      "blocks": "INFERENCE_ACCURACY_GATE"
    },
    {
      "id": "B04",
      "missing": "Qualified posterior weighted-summary/bin-mass errors and explicit optimizer scope/error inputs",
      "blocks": "POSTERIOR_DECISION_GATE"
    }
  ],
  "gates": {
    "Q_IDENTITY_GATE": "PASS_OPERATOR_SUPPLIED_NOT_CANONICALLY_REGISTERED",
    "JOURNAL_CONTINUITY_GATE": "PASS_COMPLETE_SUPPLIED_RECORD_RETAINED_GLOBAL_GAP_INHERITED",
    "CONTROL_SOURCE_HASH_GATE": "PASS",
    "LAUNCHER_GATE": "PASS_OFFLINE_RESOLVER_ONLY",
    "README_GATE": "PASS_LOCAL_PAIRED_PATCH_SCOPE",
    "REPOSITORY_CONSISTENCY_GATE": "PASS_LOCAL_CONTROL_PATCH_SCOPE_ONLY",
    "REFERENCE_TRUTH_GATE": "BLOCKED",
    "FINAL_SCIENTIFIC_RESULT_GATE": "UNRESOLVED"
  },
  "local_control_patch": {
    "status": "PREPARED_NOT_INSTALLED",
    "only_registry_entry_changed": "Q042-CONTEXT-V29",
    "completed_run_id": "37362125253",
    "completed_attempt": 1,
    "base_blobs": {
      "README.md": "c17bb9ce499561d02240a7a136ede6a862ae2667",
      "bubbleverse_program_registry.json": "fae212b90ccc6509f6c4193d041cd02897334d96"
    },
    "resolver_tests": {
      "completed_v29": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "PROGRAM_ID_GATE=FAIL status=COMPLETED",
        "fixture_only": false
      },
      "completed_v28": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "PROGRAM_ID_GATE=FAIL status=COMPLETED",
        "fixture_only": false
      },
      "unknown": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "PROGRAM_ID_GATE=FAIL exact registry match not found",
        "fixture_only": false
      },
      "shell_input": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "PROGRAM_ID_GATE=FAIL invalid identifier syntax",
        "fixture_only": false
      },
      "active_fixture": {
        "expected_accept": true,
        "actual_accept": true,
        "output": "PROGRAM_ID_GATE=PASS program_id=Q044-TEST-ONLY\nQ_IDENTITY_GATE=PASS q=Q-044\nLAUNCHER_GATE=PASS workflow_id=qualification-test.yml",
        "fixture_only": true
      },
      "invalid_q": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "Q_IDENTITY_GATE=FAIL registry q invalid",
        "fixture_only": true
      },
      "unsafe_path": {
        "expected_accept": false,
        "actual_accept": false,
        "output": "LAUNCHER_GATE=FAIL unsafe workflow id",
        "fixture_only": true
      }
    },
    "remote_control_state": "V29_STILL_ACTIVE_README_STILL_STALE_AT_INSPECTED_PIN",
    "immutable_manifest": "UNCHANGED",
    "launcher": "UNCHANGED"
  },
  "source_sha256": {
    "arrays.c": "c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4",
    "thermodynamics.c": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
    "cap_certificate.json": "8d3aa141558d6c561821ee3d4401ef8acc1aa32bc77189162b0cdbb5980d6ba0",
    "cap_checks.json": "2390be294e70b3fdb330dcf79f8e0292b9608aee75c638ca5dd270601b6224f7"
  },
  "return_route": "RESULT_INGESTION_AND_ROUTING",
  "next_scientific_engine": "EXISTING_MATHEMATICS_CONSISTENCY_ENGINE",
  "next_action": "Instantiate the earliest missing qualified history/input and support-specific functional prerequisites before any downstream production.",
  "delivered_control_hashes": {
    "README.md": "9a9653d342ad2e14dd7389394d094346c6938f8ef48e2f22f35e4c98410c57c7",
    "bubbleverse_program_registry.json": "ef76c23688fd8b698526262c6b655b666e7467b4132e4cb7661ab0757ea7cee7",
    "Q044_QUALIFICATION_PROTOCOL.md": "7203b9aa87673ef5a21ac87ff3afb880dd89c7d5d48c581e0587e41cd51f64ea"
  }
}
```

## Preserved incoming Q044 journal — historical accumulated state

Incoming SHA256: d63873f351437163cec937a4d22ca2a4112a64a70c958e11962f4c7660d539df; bytes: 139116. The following bytes are preserved exactly. Earlier status/date/routing statements apply to their original stage.

# BUBBLEVERSE — OVERLEVERING

RD OF THE UNIVERSE

Verified document assembly time: 2026-10-09T14:04:05+02:00; Europe/Copenhagen.

STATUS: CONTINUES.
Q: Q044 — proposed scientific continuation supplied by the operator; no remote canonical registration performed.
CASE-ID: NOT DOCUMENTED.
STAGE: MATHEMATICAL INFERENCE-ACCURACY QUALIFICATION DESIGN.
STAGE RECORD: I-Q044-MATH-QUALIFICATION-001; analytical framework, not a closed scientific result.
SELECTED NEXT ENGINE: BUBBLEVERSE — AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE.

## CHATGPT SETUP ASSESSMENT

Current verified capabilities: Work/Codex file access, local Python/NumPy calculation, connected read-only GitHub and Library access, primary-source web retrieval. Exact active model variant, active reasoning setting, account-specific selector, context limit and usage limits were not independently verified. No model switch was performed.

Recommended: a strong mathematical reasoning model with High or deeper reasoning in Work/Codex, retaining repository, file and computational tools; GPT-6.1 Sol with High reasoning if selectable. Capability classes H/X + A + C. The exposed candidate catalogue also names GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol and GPT-6 Luna; catalogue exposure does not verify account availability or comparative scientific accuracy. A frontier model is warranted if coupled switched-ODE stability, whole-domain enclosures or interacting solver/likelihood assumptions become intractable for the current configuration. The present bounded derivation did not require a model upgrade or parallel agents.

Fallback: strongest available deep-reasoning setup with equivalent mathematical, source and code access. A newer configuration may replace every named recommendation on capability grounds. Tools are required for pinned-contract recovery, reference qualification and reproducibility; no tool is itself evidence of physical truth.

## SAMLET JOURNAL — CURRENT EFFECTIVE STATE

This document is the single updated relevant journal for Q044. Its current entries govern the effective state. The complete supplied Q043 journal, original 91-source register and both claim-map trees are preserved below as a historical record. Its earlier accepted-v0.3 and pending-publication statements describe its original time, not current model state. The inherited record explicitly lacks a separately recovered complete global master journal; this continuation does not invent that missing material.

### J-044-01 — Scientific question and inherited boundaries

Does the CamSpec–HiLLiPoP implementation difference materially change qualified H0 constraints or the n_scf=3 EDE-versus-LCDM conclusion under the original matched-data/prior contract, or is its effect contractually non-material or dataset dependent?

[INHERITED] Q035 classifier harmonization remains valid. Q036–Q038 retain the continuous implementation-dependent fitted-geometry result without a causal or downstream cosmological interpretation. Q039 retains its negative results within frozen interventions. Q040 invalid numerical endpoints remain excluded. Q041 V19 did not qualify the original full comparison. Q042 is CLOSED with general feasibility INCONCLUSIVE, REFERENCE_TRUTH=BLOCKED and NUMERICAL_FINAL_RESULT=UNRESOLVED. Q043 established local preparation/validation only at its original closure. No investigation is restarted or renamed.

[PINNED REPOSITORY READ] At model commit 673e3d2f30eb6d1f36459d4dca3ac1fa0fb9e2ab, accepted/model_state.json records accepted v0.4/R000004 through Q042 and production_restart_authorized=false. Its blob matches the same file at the incoming 14eacce7a93e4ac780d59b1e86dc0cb9060f38ad pin. The latest commit-search result observed during this turn differs from the incoming model head. That observation is not a branch-ref verification or a complete audit of newer uploaded files. No current-head identity beyond the pinned reads is asserted.

Execution commit inspected: 72cf9e92fc794c122f593a77b6a555e6e97f6a2e. No repository write, candidate promotion, workflow dispatch, original-binary replay, cosmological prediction, optimizer start or posterior campaign occurred here. Existing model publication is separate from numerical production authorization.

Inherited physical candidates, H0 benchmarks and prediction/contradiction states remain unchanged. H0 has no single accepted value. n_scf=3 is dimensionless. The inherited benchmarks 73.50+-0.81, 67.24+-0.35 and 68.51+-0.58 km s^-1 Mpc^-1 are separate inference chains, not results calculated here. Their original primary bibliographic gaps remain. No new tension sigma was calculated from them.

### J-044-02 — Exact recovered scientific contract

[VERIFIED INPUT] q042_production_spec_v1.json is 9,024 bytes, SHA256 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c, Git blob 9b70e5c9d62adcf43f8f48f85b7ffb628c1dd84b. This is the handoff-designated preserved original scientific contract; the filename is Q042 and it must not be silently substituted with Q041 V19's narrower execution.

Two native Planck arms times two models times five dataset combinations gives 20 cells. Preserve native CamSpec/HiLLiPoP nuisance definitions, common matched priors and physical models, FULL and NO_ACT_PRIMARY, NO_ACT_LENSING, NO_DESI_DR2 and NO_SN. The external source lock selects ACT DR6 primary with ACT ell_min=600, ACT DR6 lensing, DESI DR2 and sn.pantheonplus with runtime file-hash identity required. The ACT cutoff alone does not verify the full Planck/ACT non-overlap construction. Source-lock SHA256: 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56. Preserve the complete source lock and runtime support manifests.

Frozen scientific rules:

| Quantity | Exact rule |
|---|---|
| Parameter location | D_x=abs(mu_A-mu_B)/sqrt(sigma_A^2+sigma_B^2); material if D_H0>=1, D_fEDE>=1, or at least two eligible primary coordinates have D>=1 |
| Primary count coordinates | H0, fEDE, omega_b, omega_cdm; log10z_c/thetai_scf cannot independently trigger weakly identified EDE materiality |
| Contour statistic | Weighted common-prior 2D histogram overlap in (H0,fEDE), primary 80x80, stability 64x64 and 96x96 |
| Geometry | Material for O<0.50; substantial for O>=0.50; different sides across grids are unresolved |
| Within-arm improvement | Delta_a=chi2_LCDM,a-best - chi2_EDE,a-best |
| Preference categories | negligible: Delta<=2; modest: 2<Delta<6; substantive: Delta>=6 |
| Preference portability | Different categories AND abs(Delta_A-Delta_B)>=2 |
| Combination materiality | Preference portability material OR (parameter location material AND geometry material) |
| Robust material class | FULL and all four required valid LOO combinations material |
| Dataset conditional class | At least one required valid combination material and at least one non-material |
| Collapse class | All required valid combinations have non-material location, substantial overlap and portable preference conclusions |

D_x is the frozen descriptive portability index. Because the arms reuse Planck information, it is not automatically an independent Gaussian significance or calibrated p-value. Keep its formula; do not add a covariance term to the frozen index. Any separate inferential significance assessment would need the paired covariance and separate prospective specification.

### J-044-03 — What was already known

[INHERITED, NOT NEW DISCOVERY] The recovered Q042 V26 ingestion already defines history-to-prediction accuracy as missing and an adaptive within-arm objective interval rule. It states that sampler precision 0.001 and tau bracket setting 1e-4 are not scientific accuracy certificates. This continuation preserves that result rather than claiming to discover it again.

New work here extends the propagation to posterior location/width, all three binned-overlap grids, explicit optimizer-error accounting and the full frozen Boolean classification. It supplies conditional mathematical bounds, not numerical values for the missing accuracy budgets.

### J-044-04 — History-to-prediction-to-likelihood bridge

[DERIVED, CONDITIONAL] Let t(theta,nu) be the exact prediction vector actually consumed by a cell's native likelihood, and t_tilde its numerical approximation. theta includes cosmological coordinates; nu includes every relevant native nuisance parameter. A valid budget must cover complete history, background, initial conditions, interpolation, event handling, root solve where relevant, observable transport and likelihood evaluation. A same-spline tau comparison alone cannot bound the entire vector t.

For a fixed positive-definite Gaussian covariance C and residual r=D-t, write delta_t=t_tilde-t, u=||C^(-1/2)delta_t|| and v=||C^(-1/2)r||. Then

delta_chi2=-2*r^T*C^(-1)*delta_t+delta_t^T*C^(-1)*delta_t,
abs(delta_chi2)<=2*v*u+u^2,
abs(delta_logL)<=v*u+u^2/2.

These are exact fixed-C inequalities. Units cancel after covariance whitening. They do not justify treating every Planck, ACT, SN or other likelihood as fixed-C Gaussian. If C, likelihood normalization or marginalization changes with predictions, include those terms or evaluate the actual native likelihood with a justified enclosure. For a differentiable non-Gaussian likelihood, a bound on its gradient along the complete prediction segment yields a conditional Lipschitz bound; it cannot be assumed across an unqualified discontinuity or invalid-support region.

History/tau tolerances require independently justified sensitivity or transport bounds into t. Agreement of two solvers does not certify their shared background or physics. A finite collection of reference points establishes only their tested scope unless coverage or remainder bounds justify extension.

### J-044-05 — Posterior perturbation bound

[DERIVED] In one arm/model/combination cell, preserve the same prior, nuisance domain, support and physical likelihood. Write ell=logL, delta=ell_tilde-ell and w=ess_sup(delta)-ess_inf(delta) over the complete prior support carrying likelihood. Assume this finite bound exists and both posterior normalizers are finite and nonzero. Additive constant offsets disappear from posterior normalization.

For total variation TV(P,Q)=sup_A abs(P(A)-Q(A))=one-half the L1 density difference,

TV(p,p_tilde)<=tanh(w/4).

Proof: let R=exp(w), p=P(A). A bounded likelihood tilt permits Q(A)<=R*p/(1-p+R*p). Hence Q(A)-p<=(R-1)*p*(1-p)/(1+(R-1)*p). Its maximum at p=1/(1+sqrt(R)) is (sqrt(R)-1)/(sqrt(R)+1)=tanh(w/4). Reversing the event gives the other sign. This bound does not assume Gaussian posteriors, independent arms or weak parameter degeneracy.

If abs(delta-c)<=epsilon uniformly for an arbitrary constant c, w<=2*epsilon and TV<=tanh(epsilon/2). At w=0 the posteriors agree exactly. Missing likelihood support, solver failures or truncating a mode invalidate a whole-support assertion. If only a region Omega is qualified, require separate bounds on both exact and approximate posterior tail masses; a conservative full bound is min(1,tanh(w_Omega/4)+P(Omega^c)+Q(Omega^c)). A sampler's missing tail is not evidence that its exact tail mass is zero.

The sharp inequality and proof above are derived in this journal. Sprungk's primary paper is methodological context for posterior stability under prior/log-likelihood perturbations; no claim is made that its abstract establishes this exact bound for Bubbleverse.

### J-044-06 — Location and width error

[DERIVED, CONDITIONAL] If a reporting coordinate has a verified bounded support [L,U], R_x=U-L and full posterior TV<=v_num, then

abs(mu_tilde-mu)<=R_x*v_num,
abs(sigma_tilde-sigma)<=R_x*sqrt(v_num).

Mean bound: bounded-test-function property of TV. Width bound: a maximal coupling has disagreement probability TV, so ||X-Y||_2<=R_x*sqrt(TV); centering and the reverse triangle inequality bound the difference in standard deviations. These are conservative sufficient bounds. No H0 prior range is invented here. If support is unbounded, use justified moment/tail bounds instead. Values outside frozen histogram prior bounds cannot be silently discarded and renormalized.

Add separately qualified weighted-sampling errors for means and widths. Posterior width sigma is different from uncertainty in estimating that width. Use additive worst-case bounds unless independence and distributional assumptions justify another combination; common systematic errors are not automatically independent.

For arm means muhat_A,muhat_B with absolute errors e_muA,e_muB, and widths shat_a with errors e_sigmaa, set s_a^- = max(0,shat_a-e_sigmaa), s_a^+=shat_a+e_sigmaa. Then a conservative index interval is

D^- = max(0,abs(muhat_A-muhat_B)-e_muA-e_muB)/sqrt((s_A^+)^2+(s_B^+)^2),
D^+ = (abs(muhat_A-muhat_B)+e_muA+e_muB)/sqrt((s_A^-)^2+(s_B^-)^2).

An unqualified or zero lower denominator yields no finite useful D^+; preserve UNRESOLVED. A zero upper denominator also makes the lower expression undefined; do not divide zero by zero. Certify material D only if the whole interval is >=1 and non-material D only if the whole interval is <1. Equality conventions remain frozen. A nonzero-width interval straddling the boundary is unresolved. Boolean coordinate/count rules apply to the resulting interval predicates with the original weak-identification restrictions.

### J-044-07 — Contour overlap error

[DERIVED] For normalized bin-mass distributions on each frozen grid,

O(P_A,P_B)=sum_i min(P_Ai,P_Bi)=1-TV(P_A,P_B),
abs(O_tilde-O)<=TV(P_A,P_A_tilde)+TV(P_B,P_B_tilde).

Projection to fixed bins cannot increase TV, so the likelihood-oscillation bound controls numerical bin-mass transport. Include separately qualified finite weighted-sampling bin-mass errors e_hist,A and e_hist,B. A safe overlap bound is e_O<=v_num,A+v_num,B+e_hist,A+e_hist,B, clipped to the feasible [0,1] interval. Computing TV between a continuous posterior and discrete sampled atoms is not a valid way to estimate these e_hist quantities; compare bin probabilities on the prescribed grid.

Qualify all 64x64, 80x80 and 96x96 overlap intervals. Every grid must lie entirely on the same allowed side of 0.50. Binning agreement of noisy point estimates alone does not prove contour stability. This remains the frozen histogram endpoint; no Gaussian ellipse or different contour definition replaces it.

### J-044-08 — Model-preference error and optimizer scope

[DERIVED / EXTENDS INHERITED RULE] Let q=-2*ell and b_a,m bound the actual reported best-objective error in a cell. Within-arm improvement error obeys

abs(Delta_tilde_a-Delta_a)<=b_a,LCDM+b_a,EDE,
abs((Delta_tilde_A-Delta_tilde_B)-(Delta_A-Delta_B))<=b_A,LCDM+b_A,EDE+b_B,LCDM+b_B,EDE.

If ell has a uniform absolute error epsilon, the exact minimum of q over the same search domain changes by at most 2*epsilon. A numerical optimizer's unproved residual gap is separate: if its approximate-objective suboptimality is independently bounded by g in chi2 units, a conservative b=2*epsilon+g applies. Finite-start count, successful return flags or rhoend do not establish g or global optimality. For the frozen best-of-four operational statistic evaluated at the same fixed returned points, only the evaluation error needs propagation; that is not a proof of global physical minima.

Unknown constant log-likelihood offsets can cancel in posterior shape but still affect EDE/LCDM improvement if different between models. Retain normalization and offset identity; the oscillation-only posterior bound is insufficient for preference. No cross-arm absolute chi2 or evidence is subtracted. The four-term expression above compares two separately constructed within-arm improvements, as explicitly allowed by the contract.

Apply categories <=2, (2,6), >=6 to their full intervals and evaluate the preference-portability predicate for every admissible pair. A shared category certifies a false portability predicate even if an unnecessary difference subtest is uncertain; different singleton categories and a certified absolute difference >=2 certify true. Use safe three-valued logical propagation. Any incompletely bounded optimizer result is not silently considered exact. The frozen preference categories are operational Delta-chi2 categories, not automatically sigma significances, Bayes factors or evidence for a universally complete Hubble-tension solution.

### J-044-09 — No universal positive tolerance; full classification

[DERIVED] A decision threshold has zero guaranteed margin when the true statistic may lie arbitrarily close to it. For every positive fixed error allowance one can place a statistic on opposite sides of 1, 0.50, 2 or 6 within that allowance. Consequently no single positive CLASS tolerance, tau tolerance or likelihood tolerance universally guarantees this classification.

Prospectively freeze the method, metric, confidence/coverage conventions, error sources, domain and interval decision rule. A justified diagnostic phase may calibrate numerical error envelopes without exposing the scientific arm comparison; it does not need an already qualified reference to collect raw diagnostics. Such diagnostics remain RAW_NOT_QUALIFIED until the accuracy and scope gates pass. This avoids demanding a completed qualification before acquiring the evidence needed to test it.

An inference target TV<=v_target implies w<=4*atanh(v_target) as a sufficient whole-support condition. This is a mathematical relation, not a selected numerical target. Numerical targets and reference products are NOT DOCUMENTED here. Budget allocations must be justified prospectively. Scientific thresholds remain exactly unchanged. Adaptive numerical refinement may reduce an unresolved interval only under a frozen refinement rule; equality at a true boundary or an unqualified tail may remain unresolved indefinitely.

[VERIFIED CLASSIFIER SCOPE] The frozen overall labels are not an exhaustive dichotomy. Example: every dataset combination has material location, substantial overlap and portable preference. Each combination is non-material under the combined rule, yet the stricter collapse class fails. q042_production_v1.py correctly retains NOT_AVAILABLE in that example. Likewise geometry alone with non-material location need not satisfy collapse. Do not translate 'all combined predicates false' into equivalence or change the final rule retrospectively. A contract-supported collapse class would establish only the specified operational criteria; equivalence of every distributional or physical observable does not follow.

All 20 cells and five comparisons retain original completeness/convergence and method gates. The PolyChord termination precision 0.001 is an algorithm setting, not a calibrated error bound for these quantities. Required posterior qualification must address missed modes, weights, tails and estimation error. Preserve the four-start minimum convention without relabeling it a theorem of globality. No new sampling stopping criterion or optimizer setting was substituted.

### J-044-10 — Cross-checks actually performed

[COMPUTED, SYNTHETIC ONLY] Seed 44001; 5,000 random finite-distribution cases checked TV, bounded mean, standard-deviation and overlap inequalities. An independent two-point extremal construction saturated the TV bound at w=0.001,0.1,1,5. Another 5,000 fixed positive-definite covariance cases checked the exact Gaussian likelihood perturbation inequality. Boundary categories and four representative frozen final-classification cases passed, including the deliberate NOT_AVAILABLE example. All actual check outputs and the full Python/NumPy check code are embedded below.

The analytic proofs provide the mathematical result; the finite checks support arithmetic/counterexample detection and do not prove a cosmological accuracy bound. No current scientific comparison, new H0, measured preference, posterior width or actual overlap was calculated.

### J-044-11 — Qualification status and next task

MATHEMATICAL PROPAGATION FRAMEWORK: DERIVED AND SYNTHETICALLY CROSS-CHECKED.
ACTUAL HISTORY/PREDICTION/LIKELIHOOD ERROR ENVELOPES: NOT QUALIFIED.
MATCHED INDEPENDENT VALID REFERENCE: NOT ESTABLISHED IN INSPECTED MATERIAL.
ORIGINAL SWITCHED-RHS EXISTENCE/UNIQUENESS AND PHYSICAL EQUIVALENCE OF A CHANGED REPRESENTATION: NOT ESTABLISHED HERE.
SAMPLING AND OPTIMIZER ERROR INPUTS: NOT ESTABLISHED.
Q044 SCIENTIFIC ANSWER: UNRESOLVED.
PRODUCTION_RESTART_AUTHORIZED: false.

The V31 cap32 result is still conditional on its frozen retained-support representation and admissibility/domain/rail assumptions. These posterior bounds neither repair it nor prove another representation feasible. A materially different representation may be investigated only as a new qualified numerical lineage; its physical equations, priors, data and scientific decision rules must remain matched. An event-aware integrator or compressed validated support is a possible design direction, not an accepted candidate or an equivalence proof.

## AKTUEL OVERLEVERING — ONE NEXT ENGINE

Send Q044 and this entire journal to the AUTONOMOUS EXECUTION-MECHANISM / NUMERICAL / HPC / MOTOR-BUILDER ENGINE. This is a continuing scientific investigation, not a new repository-maintenance Q or a closed-case Motor14 handoff.

Exact next task: produce a bounded, prospectively specified REFERENCE-AND-ACCURACY QUALIFICATION design that can populate w, b, support/tail, posterior-summary and bin-mass error inputs above under the unchanged 20-cell contract. Reuse the existing architecture; recover frozen model/nuisance/prior/data definitions and original valid/raw products rather than starting the historical cases over.

Required deliverable:

1. One physically justified source/solver interpretation and materially different numerical representation if needed; define switched-event semantics and accepted/rejected-step behavior explicitly. No clipping, smoothing, arbitrary cutoff change, retroactive cap change or wholesale physics replacement is justified here.
2. Exact matched full-parameter/nuisance reference identities and complete histories/background/prediction/likelihood products when accessible. Their independent validity, uncertainty and coverage must be assessed. A synthetic reference, unconverged posterior mean or successful finite startup is insufficient.
3. A reference acquisition route with diagnostic identity/method gates and prospective resource/stop policy. Raw evidence may be acquired before inference qualification; its scope and required authorization must be explicit. The receiving engine must not treat this handoff as authority to dispatch a production or spectra/likelihood campaign.
4. Actual or defensible bounded transport from history/background to every consumed observable and native likelihood, plus same-model support coverage or explicit tails. Propagate reference uncertainty, floating-point/interpolation error and changed-source error separately.
5. A predeclared simultaneous error/coverage scheme for all required posterior means, widths and histogram grids, and an honest optimizer scope. The scheme must control the family of decisions rather than stacking unspecified individual confidence intervals. Confidence level is NOT SELECTED here; no observed results may be used to choose favorable scientific rules.
6. A concrete READY_FOR_SEPARATE_QUALIFICATION_EXECUTION design or a finite BLOCKED certificate naming the exact unsupported input. A READY design is not a qualified physical reference or production clearance.

After reference/accuracy evidence is available, apply the interval predicates and original five-combination rule. Only qualified production can eventually answer material difference, contract-supported collapse, dataset conditional behavior or insufficient qualification. No unavoidable Q044 conclusion can be obtained by further symbolic manipulation without the missing bounds.

## SOURCE REGISTER FOR THIS CONTINUATION

Keep every inherited source ID; the following new source records extend their provenance. None is an independent new cosmological observation.

- I-Q044-JOURNAL-001: complete supplied Q043_SAMLET_JOURNAL(1).md; read all 1,970 lines and materialized original 105,684 bytes; SHA256 b952c3e80e58dc6290e16b432ef20040e32bb111aea56d97e4fbf7892836b42c. Supports original Q043 scope and preservation of 91 source objects/two claim-map trees. Historical statements remain historical.
- I-Q044-CONTRACT-001: Morfindien/Bubbleverse, q042_production_spec_v1.json at 72cf9e92fc794c122f593a77b6a555e6e97f6a2e; exact hashes/bytes in J-044-02. Supports frozen scientific rules and numerical settings. Internal scientific contract, not an external measurement.
- I-Q044-SOURCELOCK-001: same repository/pin, q042_production_source_lock_v1.json; SHA256 0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56, 4,974 bytes, blob 5556e79746a45b365374d723d29b73fe5b25e356. Supports dependency versions and native/source matching constraints; not proof that installed runtime files satisfy them.
- I-Q044-CLASSIFIER-001: same repository/pin, q042_production_v1.py; SHA256 889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642, 27,436 bytes, blob d0bb194a7f0fc26eb5611839c5c75ee8566a7a5f. Supports implemented weighted summaries, histogram definitions, finite-start minimum and unresolved final-classification branch. Source inspection is not an execution of scientific production.
- I-Q044-READINESS-001: same repository/pin, q042_treatment_readiness.json; SHA256 319d4d6fd058e095871bd6f9fed2f4b8abda0556b8485ff88587cc65cb67e507, 30,095 bytes, blob a10a182906efc268ceb62640eb794ad8c9e102a4. Supports inherited missing treatment/reference/tolerance gates; superseded historical operational instructions are not restarted.
- I-Q044-MODELSTATE-001: Morfindien/bubbleverse-model, accepted/model_state.json at 673e3d2f30eb6d1f36459d4dca3ac1fa0fb9e2ab; same blob as incoming pin 14eacce7a93e4ac780d59b1e86dc0cb9060f38ad; SHA256 e54306ac67384055a18f3b57cb792dc40d2696489ae69626bf76d6b824a3a41a, 2,485 bytes, blob 77d69522e687d654d9d413eadd16a1b59f70b5e3. Supports accepted state and production authorization flag at those pins.
- I-Q044-V26-INHERITED-001: q042_v26_result_ingestion_full_handoff.md, read its current 1–440 lines and located the inherited accuracy-contract content; file ID file_0000000027dc81f5b1e9948c2ca54fb1. Supports earlier raw-reference scope, unresolved transport accuracy and diagnostic acquisition versus qualification distinction. Its cumulative 111,885-line file was not reread in full or rehashed here. The full active Q043 source register contains its inherited lineage.
- K-Q044-STABILITY-001: Bjorn Sprungk, On the Local Lipschitz Stability of Bayesian Inverse Problems; arXiv:1906.07120v3, revised 22 January 2020; related publication DOI 10.1088/1361-6420/ab6f43. Primary author paper abstract/metadata retrieved at https://arxiv.org/abs/1906.07120. Supports general methodological relevance of posterior sensitivity to prior/log-likelihood perturbations, not Bubbleverse-specific accuracy or the exact sharp bound derived here.
- I-Q044-MATH-QUALIFICATION-001: explicit proofs, synthetic check code/output and effective journal entries in this document. Supports conditional mathematics only. No independent empirical evidence is added.

Pinned source URLs:

https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_spec_v1.json
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_source_lock_v1.json
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_production_v1.py
https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_treatment_readiness.json
https://github.com/Morfindien/bubbleverse-model/blob/673e3d2f30eb6d1f36459d4dca3ac1fa0fb9e2ab/accepted/model_state.json

## TOOL PROVENANCE AND EVIDENCE STRENGTH

Connected GitHub: pinned native project-source access; five reconstructed source files match their returned Git blobs and the frozen contract/source-lock hashes. Library: complete supplied Q043 journal and targeted inherited V26 qualification content. Web: primary-paper metadata/abstract for methodological context. Python/NumPy: reproducible synthetic checks, hashes and retained-source/map integrity. Tool outputs do not create absent physical reference data.

Evidence strength: STRONG for the recovered frozen contract and conditional analytic inequalities; INSUFFICIENT to answer the downstream cosmological question. Conclusion-critical limitations are the missing independent valid reference/error envelopes, domain/tail qualification, optimizer/sampling qualification and switched-source equivalence. Finite checks do not supply these. The original scientific hypotheses and unresolved tensions retain their previous status.


## REPRODUCIBLE MATHEMATICAL CHECKS — CODE AND ACTUAL OUTPUT

The code uses the preserved contract bytes for its identity check. It uses Python 3 and NumPy; no cosmology dependency or data is evaluated.

```python
import json, math, hashlib, itertools
from pathlib import Path
import numpy as np

rng=np.random.default_rng(44001)
checks={}
max_ratio=0.0
for _ in range(5000):
    n=int(rng.integers(2,35));p=rng.dirichlet(np.ones(n));d=rng.uniform(-2,2,n)
    q=p*np.exp(d);q/=q.sum();w=float(np.ptp(d));tv=float(np.abs(q-p).sum()/2)
    bound=math.tanh(w/4);assert tv<=bound+1e-13
    x=rng.uniform(-3,7,n);R=float(np.ptp(x));m1=float(p@x);m2=float(q@x)
    s1=math.sqrt(float(p@((x-m1)**2)));s2=math.sqrt(float(q@((x-m2)**2)))
    assert abs(m1-m2)<=R*tv+1e-13
    assert abs(s1-s2)<=R*math.sqrt(tv)+1e-13
    a=rng.dirichlet(np.ones(n));b=a*np.exp(rng.uniform(-1,1,n));b/=b.sum()
    O=lambda u,v:float(np.minimum(u,v).sum())
    assert abs(O(p,a)-O(q,b))<=tv+float(np.abs(a-b).sum()/2)+1e-13
    max_ratio=max(max_ratio,tv/bound if bound>0 else 0)
checks['random_posterior_mean_sigma_overlap_checks']={'cases':5000,'passed':True,'maximum_tv_bound_ratio':max_ratio}
sharp=[]
for w in (0.001,0.1,1,5):
    R=math.exp(w);p=1/(1+math.sqrt(R));q=R*p/(1+(R-1)*p)
    assert abs((q-p)-math.tanh(w/4))<1e-13
    sharp.append({'log_likelihood_oscillation':w,'exact_tv':q-p,'bound':math.tanh(w/4)})
checks['two_point_sharpness']=sharp
for _ in range(5000):
    n=8;A=rng.normal(size=(n,n));C=A@A.T+np.eye(n);Ci=np.linalg.inv(C)
    r=rng.normal(size=n);e=rng.normal(size=n)*0.01
    dq=float((r-e)@Ci@(r-e)-r@Ci@r)
    bound=2*math.sqrt(float(r@Ci@r))*math.sqrt(float(e@Ci@e))+float(e@Ci@e)
    assert abs(dq)<=bound+1e-12
checks['fixed_covariance_gaussian_checks']={'cases':5000,'passed':True}
def category(x):return 'negligible' if x<=2 else 'modest' if x<6 else 'substantive'
def final(rows):
    mats=[m or (p and g) for p,g,m in rows]
    if all(mats):return 'MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE'
    if any(mats):return 'MIXED_DATASET_CONDITIONAL'
    if all(not p and not g and not m for p,g,m in rows):return 'SCIENTIFIC_DIFFERENCE_COLLAPSES'
    return 'NOT_AVAILABLE'
assert [category(x) for x in (2,2.01,5.99,6)]==['negligible','modest','modest','substantive']
assert final([(True,False,False)]*5)=='NOT_AVAILABLE'
assert final([(False,False,False)]*5)=='SCIENTIFIC_DIFFERENCE_COLLAPSES'
assert final([(True,True,False)]*5)=='MATERIAL_SCIENTIFIC_PORTABILITY_DIFFERENCE'
assert final([(True,True,False)]+[(False,False,False)]*4)=='MIXED_DATASET_CONDITIONAL'
checks['frozen_decision_examples']={'passed':True,'classification_gap_preserved':True}
checks['scope']='Synthetic bounded mathematical cross-checks only. No cosmological predictions, likelihoods, optimizers, posterior sampling or production.'
checks['seed']=44001
checks['science_spec_sha256']=hashlib.sha256(Path(__file__).with_name('science_spec.json').read_bytes()).hexdigest()
Path(__file__).with_name('error_bound_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))

```

```json
{
  "random_posterior_mean_sigma_overlap_checks": {
    "cases": 5000,
    "passed": true,
    "maximum_tv_bound_ratio": 0.9999248130634557
  },
  "two_point_sharpness": [
    {
      "log_likelihood_oscillation": 0.001,
      "exact_tv": 0.0002499999947916387,
      "bound": 0.0002499999947916668
    },
    {
      "log_likelihood_oscillation": 0.1,
      "exact_tv": 0.02499479296842072,
      "bound": 0.024994792968420686
    },
    {
      "log_likelihood_oscillation": 1,
      "exact_tv": 0.24491866240370908,
      "bound": 0.24491866240370913
    },
    {
      "log_likelihood_oscillation": 5,
      "exact_tv": 0.8482836399575128,
      "bound": 0.8482836399575129
    }
  ],
  "fixed_covariance_gaussian_checks": {
    "cases": 5000,
    "passed": true
  },
  "frozen_decision_examples": {
    "passed": true,
    "classification_gap_preserved": true
  },
  "scope": "Synthetic bounded mathematical cross-checks only. No cosmological predictions, likelihoods, optimizers, posterior sampling or production.",
  "seed": 44001,
  "science_spec_sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
}

```

## PRESERVED Q043 HISTORICAL JOURNAL AND SOURCE/CLAIM REGISTERS

The following complete historical record is unchanged. Its date-specific state and next-task recommendations are superseded by the current Q044 entries above where explicitly updated. It remains provenance, not a second active journal.

ANBEFALET CHATGPT-SETUP

MODEL / MODE: Functional profile B/F — deep reasoning with bounded Work repository/file execution.
REASONING: High for scientific-status, source-lineage and accepted/candidate distinctions.
TOOLS: Connected GitHub reads, pinned Git checkouts, local Python/JSON/hash analysis, file retrieval and independent read-only review.
WHY: The task is evidence and execution-state integration with a large provenance chain. No new cosmological research or numerical campaign is required.
CURRENT SETUP IS SUFFICIENT. No model switch was performed; account-specific selectable modes and maximum context capacity were not independently verified.

BUBBLEVERSE — AFSLUTTET SAG

Q: Q043 — explicitly designated by the operator.
CASE-ID: NOT DOCUMENTED.
STATUS: CLOSED — LOCAL PREPARATION AND VALIDATION ONLY.
NEXT DESTINATION: MOTOR 14 — UNIVERSE REVISION / COMPARISON.
Date/time: 2026-10-09T08:14:45+02:00; timezone Europe/Copenhagen.
Task lineage: TASK-Q042-M14-SYNC-001.
Result: R-Q043-REPOSITORY-INTEGRATION-001.

## SAMLET JOURNAL

This is the active relevant journal for the bounded Q043 integration investigation. Q043 names this investigation; it does not rename Q042 sources, reopen Q042 or add new Q043 physics to the candidate. The original Q042 source register and both claim-map trees appear in full below without renumbering. The cumulative Q042 source journal remains byte-for-byte preserved inside the model preparation diff. A standalone authoritative Copy Box 1 was not supplied or independently located; a complete rewrite of Bubbleverse's global knowledge is therefore not claimed.

### J-043-01 — Question and scope

[TECHNICAL INTEGRATION] Can the Q042 inconclusive closure be incorporated into a consistent candidate model and execution-control state, preserving all source and qualification boundaries and passing the existing update gates?

Authorized work: preparation and local validation across the accepted-model and execution repositories. The question concerns state consistency and provenance, not discovery of a shared physical mechanism. Physics reruns, new optimizer starts and production restarts are outside this investigation.

### J-043-02 — Verified starting repositories

[VERIFIED REPOSITORY STATE] Both live default-branch heads match the incoming pins:

| Repository | Verified starting HEAD | Role |
|---|---|---|
| Morfindien/bubbleverse-model | 10fa83797b2f7740519d4e43b1bebf0a6e35bada | Accepted/candidate/formal model, release and provenance |
| Morfindien/Bubbleverse | 72cf9e92fc794c122f593a77b6a555e6e97f6a2e | Execution/evidence and permanent launcher |

The accepted model remains v0.3 / R000003 / Q001–Q041. Its active promoted Q041 candidate record, canonical model, canonical release and older accepted snapshots remain unchanged. Before application the live execution registry still says V29 ACTIVE. Local preparation is distinct from remote synchronization.

Technical provenance: I-Q043-REPOSITORY-INSPECTION-001, the incoming I-M14-REPOSITORY-001 pins and the verified GitHub V29 run.

### J-043-03 — Inherited scientific state

[INHERITED, UNCHANGED] Q035 harmonization removed the classifier-dependent stable/non-stable contrast. Q036–Q038 retain the internal continuous CamSpec–HiLLiPoP fitted-geometry difference, exact-common-TT survival and four-coordinate compact representation. These are not evidence of physical causality. Q039 retains the negative results for the frozen tested interventions; they do not eliminate all conceivable implementation changes.

Q040 remains a legitimate mathematical target with unqualified numerical endpoints; its science products remain excluded. Q041 V19 is a valid controlled computational non-result, with 0/32 documented complete chains and an executed scope narrower than the original contract. It establishes neither physical agreement nor physical disagreement.

C-036-IMPL / CTR-PLANCK-IMPL-001 remains an unresolved methodological geometry tension; downstream physical significance remains unknown. CTR-H0-001 / C-001 remains unresolved. CTR-HIST-BASIN-LABEL-001 remains resolved methodologically. No tension was silently resolved by this integration.

Sources: supplied handoff; relevant Q001–Q042 journal pages 120–132; inherited original source/claim maps below; accepted baseline layers.

### J-043-04 — Q042 closure and evidence limitations

[DOCUMENTED INCONCLUSIVE CLOSURE] Q042 is CLOSED. The tested documented strategies did not establish scientifically qualified execution of the exact original Q041 downstream-portability contract. General feasibility remains INCONCLUSIVE; universal impossibility is not established.

REFERENCE_TRUTH = BLOCKED. NUMERICAL_FINAL_RESULT = UNRESOLVED. PRODUCTION_RESTART_AUTHORIZED = false.

V29 is completed prerequisite-only. V30/V31 are completed bounded attempts with local partial outputs. V31 remains LOCAL_NOT_COMMITTED / Q042_COMPARISON_V31_LOCAL_001; it has no asserted GitHub numerical run or qualified remote checkpoint. No complete history or computed tau is established. Captured initialized inputs do not establish upstream physical accuracy.

All 80 optimizer records retain their original cumulative-journal/artifact provenance and validity limits. Finite-start objectives and flag 0 do not prove global minima. Q043 did not reconstruct or recalculate these records independently.

Sources: I-Q042-COMPARISON-V31-001; I-Q042-COMPARISON-V31-VALIDATION-001; I-Q042-V31-INGESTION-001; exact immutable cumulative source artifact.

### J-043-05 — Frozen contract and conditional cap result

[INHERITED CONDITIONAL MATHEMATICAL LIMITATION] The original science contract is preserved with SHA256 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c. Its paired native Planck arms, two models, common external blocks and original decision rules are not altered.

Cap32 concerns the frozen V31 support-output policy, not a physical parameter. Conservative counts UPPER 138 and LOWER 3,002 are representation-specific candidates, not physical minima. The inherited necessary-condition result retains all four assumptions: an existing admissible absolutely continuous solution; frozen source/domain identity; continuation contained in the received global rails; and unchanged retained intervals/support policy.

The preserved certificate does not prove original switched-RHS existence/uniqueness, original executable rounding accuracy, upstream accuracy, a downstream acceptance budget or feasibility failure of every alternative method. More runtime alone is rejected as a sufficient repair for this unchanged policy. Retroactive cap expansion is not reproduction. The certificate mathematics and trajectories were not rerun here.

### J-043-06 — Physical parameters and model candidates

[UNCHANGED] There is no single accepted H0 value. Inherited benchmarks remain 73.50 ± 0.81, 67.24 ± 0.35 and 68.51 ± 0.58 km s^-1 Mpc^-1 with their separate local/CMB/DESI+BBN inference chains. They are not Q042 or Q043 outputs. n_scf remains 3.

MOD-EDE-N3 / MECH-EDE-N3-001 stays ACTIVE / CONSTRAINED; MECH-ME-001 stays ACTIVE / CONSTRAINED; MECH-DYNDE-001 stays ACTIVE. No complete Hubble-tension solution, model preference, new equation, parameter reduction or physical mechanism follows from this work.

The unchanged physical files are checked against the exact accepted base; H0 benchmarks/uncertainties, parameters, equations, assumptions, result registry and mechanism/contradiction states are preserved.

### J-043-07 — Prepared model integration

[LOCAL VALIDATED PREPARATION] The recovered prospective v0.4 / R000004 candidate remains under provenance/prepared_candidates/Q042/. It is CANDIDATE_PREPARED_NOT_PROMOTED with proposed evidence boundary Q042. Canonical accepted/candidate/model/release state stays through Q041.

The proposed projection incorporates Q042 closure, completed V29 prerequisite provenance, local partial V30/V31 lineage, reference/accuracy/history constraints, conditional cap-domain restrictions and history on PRED-EDE-PORTABILITY-001. That prediction remains OPEN. Original observations, mechanisms and contradiction states are retained; all 91 source objects and inherited/new claim maps match exactly.

The existing scientific/formal validators inspect a disposable Q042 projection. They are not weakened and their success is not candidate admission or promotion.

### J-043-08 — Prepared execution reconciliation

[LOCAL CONTROL UPDATE] V29 run 37362125253 is verified completed/success, attempt 1, at execution commit 72cf9e92fc794c122f593a77b6a555e6e97f6a2e. The prepared registry changes V29 from ACTIVE to COMPLETED, preserves its completion identity and denies launch eligibility. Its historical workflow, frozen contract, manifest and existing artifacts are not deleted.

The permanent launcher is unchanged. Actual execution of its resolver rejects completed V29, unknown IDs and unsafe IDs without producing dispatch output, while an unrelated ACTIVE target still resolves. The prepared registry has zero ACTIVE Q042 targets and preserves all 43 unrelated entries.

The README and treatment override supersede stale pending execution/ingestion instructions. The current override identifies integration case Q043 and source Q042 separately. The execution closure keeps local V30/V31 outputs as evidence with no new remote numerical target.

### J-043-09 — New defect found and repaired

[TECHNICAL DEFECT RESOLVED] The recovered closure record still pointed to candidate/updates/Q042/source_register.json after the previous package moved unadmitted candidate preparation to provenance/prepared_candidates/Q042/.

A direct cross-repository resolution check failed before correction. The reference now resolves to Morfindien/bubbleverse-model:provenance/prepared_candidates/Q042/source_register.json and matches the exact original 91-object source register. This repairs provenance navigation; it changes no scientific source object, claim or original V31 execution identity.

### J-043-10 — Fresh validation and review

[LOCALLY COMPUTED TECHNICAL CHECKS]

| Check | Actual result |
|---|---|
| Staged candidate integrity/scope/lineage gates | 8/8 PASS |
| Canonical scientific / formal validators | 10/10 and 13/13 PASS |
| Candidate projection scientific / formal validators | 10/10 and 13/13 PASS |
| Historical Q041 validation | 10/10 PASS |
| Failure-injection regressions | 10/10 PASS |
| Public system healthcheck | 20/20 PASS |
| Actual permanent-launcher resolver | 4/4 PASS |
| Shared closure fields across repositories | 14 matched |
| Protected execution baseline files | 1,526 byte-identical |
| Unrelated execution registry entries | 43 unchanged |
| Original source register | Exact 91 objects unchanged |
| Both exported diffs applied to fresh pinned worktrees | PASS; post-application candidate/control checks PASS |
| Independent read-only review | No remaining Critical, Important or Minor findings |

These checks establish internal preparation/control consistency. They are not independent cosmological observations or qualified numerical science.

### J-043-11 — Actual result and remaining deployment state

[SCOPED ANSWER] Yes: a bounded, internally consistent Q042 candidate and execution-control update can be prepared and pass the existing gates at the verified pinned bases. This is demonstrated by the delivered local diffs and fresh validation.

REMOTE_SYNC = NOT_PERFORMED. ACTIVE_CANDIDATE_ADMISSION = NOT_PERFORMED. CANDIDATE_PROMOTION = NOT_PERFORMED. No official accepted v0.4 release is asserted. Local preparation does not mean the live stale ACTIVE entry has already changed.

Q043 closes only the documented preparation/validation question. Later review/application and any controlled admission/promotion are separate operations. They require current-head checks and the established update procedure; no numerical workflow dispatch is necessary.

### J-043-12 — Preserved rejections and dependencies

[REJECTED] Unchanged V31 completion-by-time-alone as a sufficient repair; retrospective cap expansion as reproduction; tau/complete-history/global-minima inference from partial records; diagnostic reference as a qualified benchmark; Q040 invalid science endpoints; green workflow as physical truth; technical failure as model falsification; classifier labels as invariant physical modes.

[DEPENDENCIES] CamSpec and HiLLiPoP share Planck information. The PDFs, accepted compression and cumulative handoff reuse evidence. Repeated implementation checks do not become independent observations. The original bibliography's missing details remain missing. Source and tool provenance do not create absent scientific error budgets.

## DOKUMENTERET SVAR

PASS_LOCAL_PREPARATION_AND_VALIDATION_ONLY. The prepared candidate and execution controls pass the existing bounded gates. Actual remote synchronization and accepted-state integration have not occurred. Q042 remains closed inconclusively; reference truth stays blocked and numerical final result unresolved.

## INTEGRATIONSSTATUS

PARTIAL INTEGRATION — internally consistent evidence/control preparation. No new shared physical mechanism is established.

## INTEGREREDE RESULTATER

Q042 inconclusive closure; prerequisite-only V29 completion; local partial V30/V31 lineage; conditional cap limitations; preserved source/claim lineage; unresolved portability history; retirement of stale current execution instructions.

## FÆLLES STRUKTUR

A consistent source-to-result-to-proposed-model-to-control provenance chain. This is administrative/epistemic structure, not physical unification.

## NULLMODEL / SEPARAT FORKLARING

Operational M0: disconnected source/model/control status with V29 stale ACTIVE. Operational M1: one qualified closure state represented consistently in the prepared layers and launch controls. M1 resolves the demonstrated operational divergence locally. No statistical or physical M0/M1 model-comparison calculation is warranted or performed.

## MODELKERNE

The accepted physical core is unchanged. The integration requires explicit accepted/candidate boundaries, immutable source identities, qualified result status and exact completed-target gating.

## HVAD INTEGRATIONEN ERSTATTER

Stale active V29 and pending execution/ingestion guidance are superseded in the prepared package. No active physical model component is replaced. Raw historical source bytes remain preserved.

## NYE KONFLIKTER

No known new conclusion-critical scientific conflict. The remaining live-versus-prepared repository divergence is explicit; it is not silently resolved by local validation.

## INTEGRATIONSGÆLD

Operational: review/apply the exported diffs using fresh repository heads, then use the existing separately controlled candidate admission/promotion procedure if pursued. Scientific: the inherited missing reference/upstream/binary/downstream qualification remains unresolved; Q043 supplies no accuracy budget.

## NYE PREDIKTIONER

No new independent physical prediction. PRED-EDE-PORTABILITY-001 remains OPEN with Q042 history in the proposal.

## UAFHÆNGIG VALIDERING

INTERNALLY CONSISTENT, with an independent read-only technical review. No new independent physical validation.

## EVIDENSSTYRKE

STRONG for the bounded local integrity, preparation and launcher-control conclusion at the pinned bases. INSUFFICIENT to claim live synchronization, accepted promotion, a numerical final result or physical inference.

## KONKLUSIONSKRITISKE FORBEHOLD

Standalone Copy Box 1 is missing. The original 80 records, cap proof and original-binary accuracy were not independently recomputed. Six structured/cumulative source hashes are verified; inherited journal/Main Book PDF hashes were not rehashed here. No remote write, admission, promotion, numerical dispatch or new optimizer start occurred. Source Q042 remains unchanged even though the operator designated the integration investigation Q043.

## KILDER OG PROVENANCE

Primary project anchors:

- [Accepted model at pinned commit](https://github.com/Morfindien/bubbleverse-model/tree/10fa83797b2f7740519d4e43b1bebf0a6e35bada).
- [Execution repository at pinned commit](https://github.com/Morfindien/Bubbleverse/tree/72cf9e92fc794c122f593a77b6a555e6e97f6a2e).
- [Verified prerequisite-only V29 run](https://github.com/Morfindien/Bubbleverse/actions/runs/37362125253).
- I-Q042-V31-INGESTION-001 and original decision/audit/certificate/checks/cumulative-handoff bytes.
- The recovered q042_model_candidate.patch and q042_execution_sync.patch; their earlier q042_sync_result(1).json is historical preparation evidence, not proof of current remote synchronization.
- Relevant Q001–Q042 updated journal pages retrieved from the supplied current file; original accepted Q041 input lineage remains retained.
- I-Q043-REPOSITORY-INSPECTION-001 and I-Q043-PREPARATION-VALIDATION-001: new technical records only, kept separately from the original 91-source register.

Verified immutable source digests and delivery diff digests are serialized in q043_integration_result.json. Repeated source objects/derived checks carry no new evidential independence.

## TIL MOTOR 14

Register Q043 as a bounded technical preparation/validation result, without converting it to a physical result or pretending the live repositories are synchronized. Preserve Q042's inconclusive closure, Q041 unresolved physical portability, Q040 endpoint exclusion and existing H0/geometry tensions. The next concrete action, if pursued, is controlled review/application of the delivered repository diffs, followed by separately gated candidate admission/promotion. Do not return to an unchanged Q042 numerical campaign.

## DELIVERY — same result, reviewable artifacts

| Artifact | Purpose |
|---|---|
| q043_model_preparation.patch | Full model preparation diff, including exact cumulative source history and original 91-source/maps |
| q043_execution_sync.patch | Execution README/registry/control preparation, including corrected cross-repository source reference |
| q042_closure_state.json | Corrected individual machine-readable execution closure record |
| q043_integration_result.json | Machine-readable serialization of this Q043 result, validation, limitations and original source/maps |

No ZIP is required. Neither diff performs numerical dispatch or promotes the accepted model.

## ORIGINAL SOURCE REGISTER — unchanged 91 objects

```json
[
  {
    "id": "I-Q042-V24-001",
    "title": "Actual V24 final diagnostic, frozen contract and received handoff",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "artifact_id": 11329942371,
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37275520455/artifacts/11329942371",
    "sha256": "737ee53134157582b2bf04a7c5a50c972aa421161a05845568d8f2d789a2fb81",
    "retrieval": "User attachment; independently matches GitHub archive digest"
  },
  {
    "id": "I-Q042-V24-002",
    "title": "Actual original-binary native worker artifact",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL / NUMERICAL EVIDENCE",
    "artifact_id": 11328889897,
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37275520455/artifacts/11328889897",
    "sha256": "b7cfd3766447225ebe35bdb8ed77cf27d212d0693b2ff0f6ee1f4c82a8b0c311",
    "retrieval": "Read-only GitHub download; archive and every reported raw member verified"
  },
  {
    "id": "I-Q042-V24-003",
    "title": "V24 run, jobs, artifacts and original-cache worker log",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37275520455",
    "execution_commit": "716a7b870f5d4470338c825ad87ae09bb8f04096",
    "retrieval": "Read-only GitHub metadata and worker log; snapshots included"
  },
  {
    "id": "I-Q042-V24-004",
    "title": "Complete received V24 execution handoff and inherited journal",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "file": "q042_execution_handoff_v24.md",
    "sha256": "c16c6880e50ac79363c69d13edcc09cbe6641e830dd985d6808aeeb60cc7028c",
    "size_bytes": 1146361,
    "retrieval": "Supplied standalone attachment equals final artifact member byte for byte"
  },
  {
    "id": "I-Q042-V24-005",
    "title": "Independent V24 ingestion audit",
    "type": "BUBBLEVERSE INTERNAL ANALYSIS",
    "file": "q042_ingestion_audit_v24.json",
    "sha256": "e5309d47b9fa883ebabc57d477f65f24a7b066a205917661641737127c7c4f02",
    "checks_passed": 48,
    "checks_failed": 0,
    "retrieval": "Analysis of archived bytes only; audit source included"
  },
  {
    "id": "K-Q042-V24-001",
    "title": "Pinned class_ede source/thermodynamics.c",
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "authors": "Repository contributors; individual authors NOT DOCUMENTED in this ingestion",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c",
    "sha256": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
    "retrieval": "Read-only GitHub full file at frozen commit; source snapshot included",
    "supported_claims": [
      "upper/lower optical-depth guards and bisection condition",
      "missing lower reio_camb break",
      "piecewise reionization formula",
      "get_tau scratch-column writes",
      "x_noreio depends on evolved hydrogen/helium state"
    ]
  },
  {
    "id": "I-Q042-V24-006",
    "title": "Executed V24 native observer and controller",
    "type": "BUBBLEVERSE INTERNAL IMPLEMENTATION EVIDENCE",
    "commit": "716a7b870f5d4470338c825ad87ae09bb8f04096",
    "observer_url": "https://github.com/Morfindien/Bubbleverse/blob/716a7b870f5d4470338c825ad87ae09bb8f04096/q042_class_origin_probe_v24.c",
    "controller_url": "https://github.com/Morfindien/Bubbleverse/blob/716a7b870f5d4470338c825ad87ae09bb8f04096/q042_class_origin_v24.py",
    "observer_sha256": "a9b43a671f1290587bf91a0780e86c9038b7e16c9de7c7e9e3df3461c37b893a",
    "controller_sha256": "b6dc50a3a2828996f437626f9b7472cf806f8eaae67ff050a3f189b736fff3db",
    "retrieval": "Read-only GitHub pinned source; snapshots included"
  },
  {
    "id": "K-Q042-V25-001",
    "title": "Frozen CLASS headers and upstream source path",
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/tree/5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "retrieval": "Read-only GitHub; original V25 source/header register retained in inherited handoff"
  },
  {
    "id": "I-Q042-V25-001",
    "title": "Pre-execution V25 repository/launcher/registry/README inspection",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "commit": "716a7b870f5d4470338c825ad87ae09bb8f04096",
    "retrieval": "Preserved original V25 execution handoff"
  },
  {
    "id": "K-Q042-V25-002",
    "title": "Actions limits",
    "authors": "GitHub",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "url": "https://docs.github.com/en/actions/reference/limits",
    "retrieval": "Official web documentation during V25 construction; historical runtime context retained"
  },
  {
    "id": "I-Q042-V25-002",
    "title": "Pre-execution local V25 implementation validation",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "file": "q042_v25_validation_report.json",
    "retrieval": "Preserved received handoff; historical local package tests, not live cosmology evidence"
  },
  {
    "id": "K-Q042-V25-003",
    "title": "Frozen HyRec wrapper, helium cutoff and initialization",
    "authors": "Nils Schoeneberg (source header)",
    "year": 2019,
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c",
    "sha256": "4747baba37424f05f168bb68d4b9bccb2c0f003bdba95ccf56fe0a4c30cc01bd",
    "retrieval": "Read-only GitHub at frozen commit; exact source bytes and Git blob identity verified",
    "doi": "NOT APPLICABLE",
    "arxiv": "NOT APPLICABLE"
  },
  {
    "id": "K-Q042-V25-004",
    "title": "Frozen helium recombination equation",
    "authors": "Yacine Ali-Haimoud and Chris Hirata; contributions Nanoom Lee (source header)",
    "year": "2010–2020 source development; publication year NOT DOCUMENTED",
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/helium.c",
    "sha256": "cc113cdc4b2d4ffa0762ab82d5485816bbbb3bbf63cd3441be5206c4c3bf6587",
    "retrieval": "Read-only GitHub at frozen commit; exact source bytes and Git blob identity verified",
    "doi": "NOT APPLICABLE",
    "arxiv": "NOT APPLICABLE"
  },
  {
    "id": "K-Q042-V25-006",
    "title": "Frozen NDF15 numerical Jacobian logic",
    "authors": "Thomas Tram (source header)",
    "year": 2010,
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/evolver_ndf15.c",
    "sha256": "49d26ddf369c08baea9cb297825f52a734df52e568687ed1f0be12ac68417856",
    "retrieval": "Read-only GitHub at frozen commit; exact source bytes and Git blob identity verified",
    "doi": "NOT APPLICABLE",
    "arxiv": "NOT APPLICABLE"
  },
  {
    "id": "K-Q042-V25-005",
    "title": "Frozen history.h helium cutoff XHEII_MIN",
    "authors": "HyRec source contributors; individual file authors NOT DOCUMENTED here",
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/history.h",
    "sha256": "b1331aed246610d2b1d598f8bedfa951974da0d2845b5c8f3d672bf33bf316f1",
    "relevant_section": "XHEII_MIN definition = 1e-6",
    "retrieval": "Pinned header recovered for prior V25 validation, Git identity preserved"
  },
  {
    "id": "I-Q042-V25-003",
    "title": "Actual V25 final diagnostic and frozen contract",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL / NUMERICAL EVIDENCE",
    "artifact_id": 11335352228,
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37288546095/artifacts/11335352228",
    "sha256": "05aa961e375a3a8ad523bb8f1b2387a1f5bb0de6f23ec61f9fc212dfd8ded02e",
    "execution_commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "retrieval": "User attachment equals GitHub final archive digest"
  },
  {
    "id": "I-Q042-V25-004",
    "title": "Actual V25 original-binary worker raw artifact",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL / NUMERICAL EVIDENCE",
    "artifact_id": 11334874529,
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37288546095/artifacts/11334874529",
    "sha256": "f7011ec77e6f41c5377b1d3a1b04f02e49bf9746706b8cfbc8060e51f431e016",
    "execution_commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "retrieval": "Read-only GitHub worker download; archive digest and all raw hashes verified"
  },
  {
    "id": "I-Q042-V25-005",
    "title": "V25 run, jobs and original-cache worker log",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37288546095",
    "execution_commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "sha256": "f5ff4b14cf8b2f247ecf453d350b6566402a24382e0fc83d11e8b6a922091666",
    "retrieval": "Read-only GitHub metadata and job log; snapshots preserved"
  },
  {
    "id": "I-Q042-V25-006",
    "title": "Archived scalar helium-boundary source replay",
    "type": "BUBBLEVERSE INTERNAL COMPUTATIONAL VERIFICATION",
    "file": "helium_boundary_replay.json",
    "sha256": "b800fc30153e73897ad781f1325b4c09a468ed683cbd55420dd4aa5c87c3b977",
    "provenance": {
      "source_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
      "source_sha256": "cc113cdc4b2d4ffa0762ab82d5485816bbbb3bbf63cd3441be5206c4c3bf6587",
      "fixture_sha256": "db0436a5e7ab9d523c5c3af2a42a031e0e631ef93232b995a0380ef8c9b77be1",
      "executable_sha256": "34c167884adf32e8cc2cc65a88ffd0219acf4c594e51b576f8b09fabca5c2f9d",
      "output_sha256": "b800fc30153e73897ad781f1325b4c09a468ed683cbd55420dd4aa5c87c3b977",
      "compiler": "gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0",
      "command": [
        "gcc",
        "-O2",
        "-Wall",
        "-Wextra",
        "-I",
        "v25_class_headers/external/HyRec2020",
        "ingest_v25/helium_boundary_replay.c",
        "ingest_v25/helium_pinned.c",
        "-lm",
        "-o",
        "ingest_v25/helium_boundary_replay"
      ],
      "density_reconstruction": "nH0 = archived nH_SI * 1e-6 / (1+z)^3; no new cosmology",
      "initialization": "T0=2.7255; fHe=0.08155605881418283; fsR=meR=1; data.error=0; pinned wrapper initialization mappings"
    },
    "retrieval": "Local unchanged pinned helium.c evaluation at two archived scalar inputs; not a cosmology rerun or a repair"
  },
  {
    "id": "I-Q042-V25-007",
    "title": "Independent V25 ingestion audit",
    "type": "BUBBLEVERSE INTERNAL ANALYSIS",
    "file": "q042_ingestion_audit_v25.json",
    "sha256": "47c60384174cbf7422590ca0f9742818281ad3ec66b69359021c549c9233d7cc",
    "checks_passed": 54,
    "checks_failed": 0,
    "retrieval": "Archived file/hash/trace/table/source audit; audit program preserved"
  },
  {
    "id": "K-Q042-TREATMENT-001",
    "title": "Frozen HyRec phase-transition implementation",
    "type": "PRIMARY TECHNICAL SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "path": "external/HyRec2020/history.c",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/history.c",
    "git_blob_sha": "9710fb166de45ab392ee7984801d8dbdf610319a",
    "sha256": "14d11b3663fcebd5a4072969237f4041549adb4449ddef875f3ca4caff948fe4",
    "size_bytes": 46089,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Reference for intended standalone helium stopping semantics; not a matched CLASS prediction benchmark"
  },
  {
    "id": "K-Q042-TREATMENT-002",
    "title": "Current official CLASS helium wrapper",
    "type": "PRIMARY TECHNICAL SOURCE",
    "repository": "lesgourg/class_public",
    "commit": "814ce59c380a5cccd0bed1747a384ff7bfc1f9cf",
    "path": "external/HyRec2020/wrap_hyrec.c",
    "url": "https://github.com/lesgourg/class_public/blob/814ce59c380a5cccd0bed1747a384ff7bfc1f9cf/external/HyRec2020/wrap_hyrec.c",
    "git_blob_sha": "2877b2da64b0254cea612e1b444bcea71d76ce82",
    "sha256": "e4785eb62b51835839e20da53944a5a170a715966b46b6f4745d9bef047c0ecb",
    "size_bytes": 7640,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Same strict helium cutoff remains; unrelated path setup differs; not an endorsed repair"
  },
  {
    "id": "K-Q042-TREATMENT-003",
    "title": "Current official CLASS thermodynamics",
    "type": "PRIMARY TECHNICAL SOURCE",
    "repository": "lesgourg/class_public",
    "commit": "814ce59c380a5cccd0bed1747a384ff7bfc1f9cf",
    "path": "source/thermodynamics.c",
    "url": "https://github.com/lesgourg/class_public/blob/814ce59c380a5cccd0bed1747a384ff7bfc1f9cf/source/thermodynamics.c",
    "git_blob_sha": "12e537259d8efd08234ff0b7984b1ce924b88226",
    "sha256": "fadf38eaa89aa46b77736a700a82b0a2842bd552533077556e8803d202a06d11",
    "size_bytes": 209535,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Lower reio_camb branch has an explicit break; source reference for a minimal branch correction only"
  },
  {
    "id": "I-Q042-TREATMENT-001",
    "title": "Frozen Q042 compiled interruption reference",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "path": "q042_compiled_reference_v22.json",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/3d15a3a7a627de2f29533cac7fe9e43dd022226f/q042_compiled_reference_v22.json",
    "git_blob_sha": "50e082a0994e10a653e3173b537e6fcc767be585",
    "sha256": "51a02ebc9b9dc78d43363f2bfeb885ff636860708a91c41ee453a97a5c400146",
    "size_bytes": 3972,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Synthetic likelihood checkpoint validation; explicitly excludes validation of the full Cobaya/CLASS runtime"
  },
  {
    "id": "I-Q042-TREATMENT-002",
    "title": "Historical unconverged-chain diagnostic reference",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "path": "q042_v19_diagnostic_reference_v1.json",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/3d15a3a7a627de2f29533cac7fe9e43dd022226f/q042_v19_diagnostic_reference_v1.json",
    "git_blob_sha": "ba1d4156728a6069f3b85f3db5faa934563dcb9b",
    "sha256": "79f1bb793550ee9a924f5db9197886837e5f2d0e60f44718a43011f0199567c1",
    "size_bytes": 2538,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Unconverged chains; forbidden cosmological endpoints; not a matched CLASS prediction benchmark"
  },
  {
    "id": "I-Q042-TREATMENT-003",
    "title": "Exact frozen production scientific specification",
    "type": "BUBBLEVERSE INTERNAL SCIENTIFIC CONTRACT",
    "repository": "Morfindien/Bubbleverse",
    "commit": "3d15a3a7a627de2f29533cac7fe9e43dd022226f",
    "path": "q042_production_spec_v1.json",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/3d15a3a7a627de2f29533cac7fe9e43dd022226f/q042_production_spec_v1.json",
    "git_blob_sha": "9b70e5c9d62adcf43f8f48f85b7ffb628c1dd84b",
    "sha256": "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c",
    "size_bytes": 9024,
    "retrieval": "Read-only GitHub fetch_file; local bytes independently verified against Git blob SHA",
    "role": "Scientific criteria recovered without numerical treatment tolerances; SHA256 matches authoritative science freeze"
  },
  {
    "id": "K-Q042-TREATMENT-004",
    "title": "HYREC-2: a highly accurate sub-millisecond recombination code",
    "authors": [
      "Nanoom Lee",
      "Yacine Ali-Haimoud"
    ],
    "year": 2020,
    "journal": "Physical Review D 102, 083517",
    "doi": "10.1103/PhysRevD.102.083517",
    "arxiv": "2007.14114",
    "url": "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.102.083517",
    "type": "PRIMARY PEER-REVIEWED SCIENTIFIC PUBLICATION",
    "retrieval": "Targeted web search: publisher abstract and arXiv metadata",
    "role": "Context only; abstract does not establish this low-redshift wrapper repair or arbitrary EDE-domain tolerance"
  },
  {
    "id": "K-Q042-DESIGN-001",
    "title": "Frozen CLASS approximation initialization, derivatives, tau search and tau definition",
    "type": "EXTERNAL TECHNICAL SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "path": "source/thermodynamics.c",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c",
    "sha256": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
    "size_bytes": 208514,
    "retrieval": "Read-only GitHub source retrieval; exact pinned text retained"
  },
  {
    "id": "I-Q042-DESIGN-001",
    "title": "Q042 production evaluator and incomplete optimizer-record schema",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "path": "q042_production_v1.py",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/ab735c80dbc707a445aade7a8123a70b1ff3801d/q042_production_v1.py",
    "sha256": "889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642",
    "size_bytes": 27436,
    "retrieval": "Read-only GitHub source retrieval; exact pinned text retained"
  },
  {
    "id": "I-Q042-DESIGN-002",
    "title": "Q032 finite-evaluation/reference-vector mechanism",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "path": "q032_planck_tt3pair_bridge_v2.py",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/ab735c80dbc707a445aade7a8123a70b1ff3801d/q032_planck_tt3pair_bridge_v2.py",
    "sha256": "f3ad6813c1b3e72a94eafffae2f1821f4cb7f45c5a5240b4bbdffb044ac427ee",
    "size_bytes": 62508,
    "retrieval": "Read-only GitHub source retrieval; exact pinned text retained"
  },
  {
    "id": "I-Q042-DESIGN-003",
    "title": "All 80 imported Q042 BOBYQA records and lineage manifest",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "run_id": 36731879692,
    "artifact_id": 11105247835,
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/36731879692/artifacts/11105247835",
    "archive_sha256": "bd1d255f19a44377db13f5a8bbe69a1f48e4f57e40c0bcef2c5f80afe03022d0",
    "record_count": 80,
    "flag_zero_count": 78,
    "flag_minus3_count": 2,
    "qualification": "Finite optimizer objectives retained; minimum-point coordinates and prediction products absent"
  },
  {
    "id": "I-Q042-DESIGN-004",
    "title": "Original CamSpec n3EDE FULL start-0 BOBYQA record",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "run_id": 36133813540,
    "artifact_id": 10874659342,
    "commit": "6c44a4117449145afd0a3ae6eb238490686a8c6d",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/36133813540/artifacts/10874659342",
    "archive_sha256": "7f25c8706c09abb91337d9422b83097b234fe85e45be4df2197121ff0a42fbba",
    "record_sha256": "44808294beec55a5bfe3487f67e4f78423cb2c9b702bc64f2b2e97a3bb73cef9",
    "qualification": "Archive contains only q042_production_bobyqa_start_v1.json. start_values are not demonstrated xmin; objective cannot be paired with that start vector as a reference."
  },
  {
    "id": "I-Q042-DESIGN-005",
    "title": "Historical V25 rerun static package failure",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "run_id": 37293733873,
    "commit": "ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37293733873",
    "qualification": "User supplied traceback PACKAGE_HASH_GATE=FAIL README.md; archived rerun inspection found class-nan skipped. This does not supersede valid run 37288546095; no cosmological result."
  },
  {
    "id": "K-Q042-INGESTDESIGN-001",
    "title": "Frozen CLASS spline fitting, interpolation and integral implementation",
    "type": "PRIMARY OFFICIAL TECHNICAL SOURCE",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "git_blob": "89837f3161cbf2d8b3485a6772bd16e0a484c93f",
    "path": "tools/arrays.c",
    "sha256": "c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4",
    "size_bytes": 92841,
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c",
    "retrieval": "Read-only GitHub fetch_file at exact commit; full source text retained",
    "evidence_strength": "Direct source evidence; does not measure cosmological effect"
  },
  {
    "id": "K-Q042-INGESTDESIGN-002",
    "title": "Official CLASS source documenting and correcting the old spline integral plus sign",
    "type": "PRIMARY OFFICIAL TECHNICAL SOURCE",
    "repository": "lesgourg/class_public",
    "commit": "814ce59c380a5cccd0bed1747a384ff7bfc1f9cf",
    "git_blob": "62b2f9092a95e0ee23ff36ab3241f88cd2c3c072",
    "path": "tools/arrays.c",
    "sha256": "1c5c1cc954a5b4c288f51a055b9aae6576f8ab3a1b083464e59a5c0432126ecd",
    "size_bytes": 94799,
    "url": "https://github.com/lesgourg/class_public/blob/814ce59c380a5cccd0bed1747a384ff7bfc1f9cf/tools/arrays.c",
    "retrieval": "Read-only GitHub fetch_file at exact commit; full source text retained",
    "evidence_strength": "Direct source evidence; does not measure cosmological effect"
  },
  {
    "id": "I-Q042-INGESTDESIGN-001",
    "title": "Exact rational spline-integral algebra check",
    "type": "BUBBLEVERSE MATHEMATICAL RESULT",
    "sha256": "f5b2e1100e65549c2198dd6ed7d04e46391428e827df33f8d36e739f7bd35457",
    "method": "Python standard-library fractions; exact polynomial basis integral and x^2 example; no cosmological evaluation",
    "runtime": "Local Python; complete environment NOT DOCUMENTED",
    "result": {
      "scope": "Exact rational polynomial identity; synthetic math demonstration, no CLASS candidate or cosmological result",
      "integral_of_a_cubed_minus_a": "-1/4",
      "curvature_integral_coefficient": "-1/24",
      "example": {
        "function": "x^2 on [0,1]",
        "endpoint_values": [
          0,
          1
        ],
        "second_derivatives": [
          2,
          2
        ],
        "exact_integral": "1/3",
        "frozen_plus_formula": "2/3",
        "official_minus_formula": "1/3"
      },
      "identity": "I_spline = h*(y0+y1)/2 - h^3*(M0+M1)/24; I_legacy-I_spline = h^3*(M0+M1)/12",
      "support": "Same nodes/coefficient/signed h; exact algebraic relation, no statement on true cosmological history"
    },
    "evidence_strength": "Exact algebra for the stated polynomial representation, not an accuracy certificate for histories"
  },
  {
    "id": "I-Q042-INGESTDESIGN-002",
    "title": "Received treatment design 35-check package audit",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "sha256": "d0ec5f36ee6376efa8ed0136a65b71be116f4cc308092eeab1eccd2df1b1514d",
    "check_count": 35,
    "status": "PASS",
    "qualification": "Checks preparation provenance/continuity/declared blockers; no numerical candidate tests"
  },
  {
    "id": "I-Q042-REFQUAL-001",
    "title": "Compiled frozen integral versus independent exact cubic reference, eight fixtures",
    "type": "BUBBLEVERSE TECHNICAL AND MATHEMATICAL EVIDENCE",
    "result_id": "R-Q042-SAME-SPLINE-C-001",
    "sha256": "49527894b20f5343b5fc660333016147dbf4b4ca39ce5549167b5ce7c95a03fa",
    "method": "Unmodified full frozen arrays.c linked with garbage collection; official integral body extracted unchanged except symbol name. Python Fraction midpoint Simpson integration independently supplies exact values.",
    "scope": "Synthetic arithmetic reference only; no physical history, candidate or production evaluation",
    "status": "PASS"
  },
  {
    "id": "I-Q042-REFQUAL-002",
    "title": "Archived V25 node-minimum and legacy support calculation",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "result_id": "R-Q042-TAU-SUPPORT-001",
    "sha256": "0c70ec568facdbedcc06ad70acb49b82ce269855f15cdd4bf7abfbfb182fdddc",
    "source_sha256": "608828a202bf8a38032bd8d8019679b0929df6f05014ff7341e942fc4b333d63",
    "method": "Read-only CSV scan excluding last row, matching frozen source scan and small-index clamp",
    "scope": "Read-only arithmetic on archived V25 lower-trial node output; not a new history",
    "limitation": "Contains z derivatives, not conformal-time spline coefficients; unsuitable as physical history truth"
  },
  {
    "id": "I-Q042-REFQUAL-003",
    "title": "Fresh read-only repository identity and content inventory",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "tree_sha": "e09537eb5c1d15bc46390e6f93f2eaf95d9ca108",
    "tree_entries": 1477,
    "truncated": false,
    "readme_git_blob": "816a640f42deefa917a3c6c6f47ef4565cbe33b2",
    "registry_git_blob": "6c11bd35b4b1e57a57ccf2b50f5c4a9f8e366c0f",
    "url": "https://github.com/Morfindien/Bubbleverse/tree/ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "method": "GitHub read-only branch/tree/spec fetch and cached-file Git blob equality verification"
  },
  {
    "id": "I-Q042-INGESTREF-001",
    "title": "Received reference qualification package and integrity verification",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "method": "Six local received files read, incoming five deliverable hashes checked against received audit, compiled result ingested without rerunning",
    "received_audit_status": "PASS",
    "received_audit_check_count": 57,
    "files": [
      {
        "file": "q042_tau_reference_qualification_full_handoff.md",
        "size_bytes": 9339440,
        "sha256": "d33d9c6630ac0c69159ffbf76ffc06eb969a5e128bd939519eb16a9e5540b2c3"
      },
      {
        "file": "q042_tau_reference_qualification_audit.json",
        "size_bytes": 6565,
        "sha256": "158dffe4ed90d333e8f46a52695e169d8a1ec7342c9b978d56b75d1a0a79c62b"
      },
      {
        "file": "q042_tau_reference_qualification_evidence.json",
        "size_bytes": 276382,
        "sha256": "b66b3c60587eeb373823443e224ea8e0dfe28d7fd7f24c006313aeabadad7f40"
      },
      {
        "file": "q042_tau_reference_qualification_decision.json",
        "size_bytes": 69252,
        "sha256": "23d9fdf1c253ddffa09257eaf64ae9781602e5ff20d5b07feeee2f68174f4eac"
      },
      {
        "file": "q042_tau_reference_qualification_protocol.md",
        "size_bytes": 17445,
        "sha256": "ac983cb454933dea97b01a1fb54907d7d78b11eeb595042fa9122438060cda03"
      },
      {
        "file": "q042_compiled_same_spline_result.json",
        "size_bytes": 9997,
        "sha256": "49527894b20f5343b5fc660333016147dbf4b4ca39ce5549167b5ce7c95a03fa"
      }
    ],
    "scope": "Receipt and provenance verification, not independent replication of the physical calculation"
  },
  {
    "id": "I-Q042-INGESTREF-002",
    "title": "Effective integration-support class arithmetic on archived V25 nodes",
    "type": "BUBBLEVERSE MATHEMATICAL AND TECHNICAL EVIDENCE",
    "result_id": "R-Q042-INGESTREF-SUPPORT-001",
    "source_sha256": "608828a202bf8a38032bd8d8019679b0929df6f05014ff7341e942fc4b333d63",
    "method": "Original complete scan; exact rational differences between represented binary64 node values",
    "supported_claim": "Small-index clamp means argmin rows1,2,3 share N3; between-class margin and conditional interval rule",
    "limitation": "Original archived invalid V25 lower trial, not a repaired history; its z-second-derivative columns are unsuitable as conformal-time spline curvature. Conditional geometric margin is not an accuracy tolerance, true xe bound or actual cosmological delta_tau."
  },
  {
    "id": "I-Q042-INGESTREF-003",
    "title": "Current ingestion read-only repository identity",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "name": "main",
    "commit": "ab735c80dbc707a445aade7a8123a70b1ff3801d",
    "tree": "e09537eb5c1d15bc46390e6f93f2eaf95d9ca108",
    "commit_date": "2026-10-05T09:59:39Z",
    "url": "https://github.com/Morfindien/Bubbleverse/tree/main",
    "retrieval_date": "2026-10-05T11:18:50.911Z",
    "method": "Read-only GitHub branch fetch in current ingestion task"
  },
  {
    "id": "K-Q042-INGESTREF-001",
    "title": "Examining Spatial (Grid) Convergence",
    "authors": "NASA Glenn / NPARC Alliance",
    "year": "NOT DOCUMENTED",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "url": "https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html",
    "retrieval_date": "2026-10-05T11:19:12.664252+00:00",
    "retrieval_method": "Direct web retrieval of primary technical guidance",
    "relevant_sections": [
      "Order of Grid Convergence",
      "Asymptotic Range of Convergence",
      "Richardson Extrapolation"
    ],
    "supported_claim": "Computed refinement levels can diagnose observed numerical convergence; Richardson estimates have assumptions. Applying this CFD guidance to the specified ODE diagnostic is a Bubbleverse inference.",
    "limitation": "Not cosmological accuracy criteria, not independent evidence for a physical hypothesis, not a rigorous global error bound"
  },
  {
    "id": "K-Q042-INGESTREF-002",
    "title": "solve_ivp — SciPy v1.15.3 Manual",
    "authors": "SciPy developers",
    "year": "NOT DOCUMENTED",
    "software_version": "1.15.3",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "url": "https://docs.scipy.org/doc/scipy-1.15.3/reference/generated/scipy.integrate.solve_ivp.html",
    "retrieval_date": "2026-10-05T11:19:12.664252+00:00",
    "retrieval_method": "Direct web retrieval",
    "relevant_section": "rtol, atol",
    "supported_claim": "The documented solver tolerances control local error estimates. An inference-level global error certificate is a separate requirement.",
    "limitation": "Documentation only; SciPy is not installed or selected as a new campaign dependency here"
  },
  {
    "id": "I-Q042-V26RUN-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "V26 raw acquisition and collected final",
    "run_id": "37323656302",
    "program_id": "Q042-REFACQ-V26",
    "commit": "92e0590f7b062b12ff86fd51a1af9258a32fe1be",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37323656302",
    "raw_artifact_id": 11351331442,
    "raw_zip_sha256": "fa1b7e2c45650d60b2a68cd78622e8636a37ed870bd7e3ac49ac4cb3a7f2abb6",
    "final_artifact_id": 11350659466,
    "final_zip_sha256": "867b7e7c5c5b3d1666f1f46fb692333fbbc3623cc72787827b097aff486290c9",
    "supported_claim": "Twelve terminal COMPLETE raw histories, conditional optical-depth values and measured refinement diagnostics; no cosmological qualification."
  },
  {
    "id": "I-Q042-V26INGEST-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Current raw-file and reporting audit",
    "retrieval_date": "2026-10-05T14:47:48.983777+00:00",
    "supported_claim": "Both archive identities, all 74 registered raw-file hashes, twelve node/support validations, twelve signed same-spline integrals and reporting diagnostics verified."
  },
  {
    "id": "K-Q042-V26HYREC-001",
    "type": "OFFICIAL REPOSITORY",
    "title": "external/HyRec2020/hydrogen.h",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "git_blob": "088b34a699efe5d6d3aefb158229e9fb83d9a586",
    "sha256": "1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.h",
    "retrieval_method": "Read-only GitHub pinned-file retrieval, Git blob identity verified",
    "supported_claim": "Frozen threshold/model-selection definitions, not proof that the transition causes the measured order loss."
  },
  {
    "id": "K-Q042-V26HYREC-002",
    "type": "OFFICIAL REPOSITORY",
    "title": "external/HyRec2020/wrap_hyrec.c",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "git_blob": "fa44c774cf1fc7dbf6185e01980764f7eb260204",
    "sha256": "4747baba37424f05f168bb68d4b9bccb2c0f003bdba95ccf56fe0a4c30cc01bd",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c",
    "retrieval_method": "Read-only GitHub pinned-file retrieval, Git blob identity verified",
    "supported_claim": "Frozen threshold/model-selection definitions, not proof that the transition causes the measured order loss."
  },
  {
    "id": "K-Q042-V26HYREC-003",
    "type": "OFFICIAL REPOSITORY",
    "title": "external/HyRec2020/history.h",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "git_blob": "a809dc3240237542361b983d244d884ea7b5f21a",
    "sha256": "b1331aed246610d2b1d598f8bedfa951974da0d2845b5c8f3d672bf33bf316f1",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/history.h",
    "retrieval_method": "Read-only GitHub pinned-file retrieval, Git blob identity verified",
    "supported_claim": "Frozen threshold/model-selection definitions, not proof that the transition causes the measured order loss."
  },
  {
    "id": "K-Q042-SWITCH27-HYDROGEN",
    "type": "OFFICIAL REPOSITORY",
    "title": "external/HyRec2020/hydrogen.c",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "sha256": "734800ccd69b41d60b519f200003ce27c3b7640f76a70353499424842ba19616",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c",
    "supported_claim": "Pion fallback routes SWIFT to the effective multilevel atom at low radiation temperature; TLA vs HMLA formulas are distinct. Actual numerical jump is not computed here."
  },
  {
    "id": "K-Q042-SWITCH27-HISTORY",
    "type": "OFFICIAL REPOSITORY",
    "title": "external/HyRec2020/history.c",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "sha256": "14d11b3663fcebd5a4072969237f4041549adb4449ddef875f3ca4caff948fe4",
    "url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/history.c",
    "supported_claim": "Pion fallback routes SWIFT to the effective multilevel atom at low radiation temperature; TLA vs HMLA formulas are distinct. Actual numerical jump is not computed here."
  },
  {
    "id": "I-Q042-SWITCH27-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Stage-weight and raw-node switch fingerprint",
    "supported_claim": "Measured signed V26 refinement errors match the order/sign/halving signature of an unresolved crossing; inferred jump magnitudes retained as inference, not actual RHS values."
  },
  {
    "id": "I-Q042-V27-RAW",
    "type": "BUBBLEVERSE NUMERICAL DIAGNOSTIC",
    "title": "Original-binary 24 fixed-state HyRec switch samples",
    "run_id": "37333030105",
    "program_id": "Q042-SWITCHPROBE-V27",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37333030105",
    "execution_commit": "f0ef57b6db30cfd6a585b18e5cbfc3b9e4e2bece",
    "raw_artifact_id": 11355435787,
    "raw_archive_sha256": "6bff8fb582453ad8644c6fca6aad1a5f50e98c5926d1cd57df83d9549702005f",
    "supported_claim": "Actual local branch mismatch, original HMLA/TLA routing, finite recorded derivatives and identical opposite-order repeats. No qualified history or physical model comparison."
  },
  {
    "id": "I-Q042-V27-AUDIT",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Independent V27 ingestion identity/completeness/hash audit",
    "run_id": "37333030105",
    "supported_claim": "All24 samples, 12 raw-file hashes, frozen inputs/binary, three successful jobs and equal received/archived handoff. Repository/docs are inspected at the actual execution commit."
  },
  {
    "id": "I-Q042-V27-ATTRIBUTION",
    "type": "BUBBLEVERSE MATHEMATICAL/NUMERICAL INTERPRETATION",
    "title": "Measured switch versus V26 stage-weight fingerprint",
    "inputs": [
      "I-Q042-V27-RAW",
      "I-Q042-SWITCH27-001"
    ],
    "supported_claim": "Measured branch mismatches quantitatively explain the leading local V26 signed RK4 refinement fingerprint under the stated fixed-state approximation. Whole-history accuracy and exclusive causality are not established."
  },
  {
    "id": "I-Q042-V27-ENDPOINT",
    "type": "BUBBLEVERSE MATHEMATICAL DERIVATION",
    "title": "Endpoint contamination of naively event-aligned RK4",
    "supported_claim": "Exact unit-step quadrature has h*J/6 error on the pre-event RK4 interval if the terminal derivative uses the post branch. An event-aware one-sided numerical endpoint convention is required; original physical <= predicate must remain intact."
  },
  {
    "id": "I-Q042-EVENT28-DESIGN",
    "type": "BUBBLEVERSE INTERNAL NUMERICAL PREREGISTRATION",
    "q": "Q-042",
    "file": "q042_event_contract_v28.json",
    "sha256": "a4d3c5c4e6399b46cf8f9f448300ce435913815750db68c33f965ce3477cf094",
    "role": "Frozen numerical convention and finite interpretation; not a computed physical result"
  },
  {
    "id": "I-Q042-EVENT28-IMPLEMENTATION",
    "type": "BUBBLEVERSE INTERNAL IMPLEMENTATION EVIDENCE",
    "q": "Q-042",
    "files": {
      "q042_event_native_v28.c": "3f8ba56e4e91b362bc1a79c1e581eff1b6fbb156b97753748301295ba5e5f083",
      "q042_event_step_v28.h": "6070e2dc68b1f3d7f54349bae9619b3018b4eb9f20e8f9b9a612d6b7fbe57d60",
      "q042_event_cell_v28.py": "301808e372c7a4a0fabbae8eab3ebb06ab51d696b4253826942e6325c0bf4404",
      "q042_event_tests_v28.py": "61aae9d801cb50115dbf4d2868e608b3f35ef849f02ab499393620a97d4be8e3",
      "q042_event_numerics_test_v28.c": "b3336064e4cdb3da88f54cb95d503260e3b3febc39a0609d336deef1e753f09f",
      "q042_event_adapter_selftest_v28.py": "a5c9e5fba233011294793207f7031ee56adb8c9316884a064eb8b3fe8f985fb1"
    },
    "role": "Reused unchanged original-binary forwarding; new one-sided numerical stage convention and finite gates"
  },
  {
    "id": "I-Q042-EVENT28-LOCALTEST",
    "type": "BUBBLEVERSE INTERNAL CONTROLLED IMPLEMENTATION VERIFICATION",
    "q": "Q-042",
    "file": "q042_event_validation_v28.json",
    "controlled_fixtures_only": true,
    "original_binary_V28_execution": "NOT YET COMPUTED",
    "role": "Exact-unit-jump red/green test; compiled native controlled fixture; original frozen derivative-body forwarding fixture;21 packet checks. No history or physical accuracy claim"
  },
  {
    "id": "I-Q042-EVENT28-FIX-001",
    "type": "BUBBLEVERSE INTERNAL TECHNICAL EXECUTION EVIDENCE",
    "run_id": "37344813050",
    "commit": "81eb5335ea5f4cbf5b61f5f2d28068ac96706676",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37344813050",
    "artifact_id": 11359857587,
    "archive_sha256": "ef9e8eeeba92e41094a303dcf51a34ddc38be0ea36084d188e8f90c9bedf1dfd",
    "raw_members_sha256": {
      "preflight_pending.json": "d63fe00f1cd9f7a531c1ee943eb49b852e132239021523f460f11acfdab56e72",
      "adapter_fixture.log": "f3dc8eb85c266d990f2e8517614cc09c6a908a505769372c867b1cca561133ab",
      "execution_failure.json": "29da0114c15ce302a96d9bb61f13d3705eed709fc73bb31b9634b8681f5d98c1",
      "native_fixture.log": "ead2d69d2ab6dfd5c4aec6bb500b22a84e8e71e46ebe3bc9434f40b2fcf4ff34"
    }
  },
  {
    "id": "I-Q042-EVENT28-FIX-002",
    "type": "BUBBLEVERSE INTERNAL IMPLEMENTATION / REGRESSION EVIDENCE",
    "file": "q042_event_tests_v28.py",
    "sha256": "c241fdd7071eda998d311cb2199f47ba62452bd3f4c2bb63723fd61342eb738f",
    "validation_file": "q042_event_fixture_fix_validation_v28.json",
    "scope": "Controlled local/CI identity regression only; actual scientific execution pending"
  },
  {
    "id": "I-Q042-V28-RAW",
    "type": "BUBBLEVERSE NUMERICAL RESULT",
    "q": "Q-042",
    "title": "Actual one-cell six-branch event-aware diagnostic",
    "program_id": "Q042-EVENTCELL-V28",
    "run_id": "37347357296",
    "repository": "Morfindien/Bubbleverse",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37347357296",
    "commit": "488a6c2ed59435137a9aad13b6c012e8aeef2e5e",
    "raw_artifact_id": 11361456203,
    "raw_archive_sha256": "3f92d011fa7b76d2276f6a24f0a6022aba19e9d51beb244ff04a64d0cf593774",
    "final_artifact_id": 11361245974,
    "final_archive_sha256": "7f8355b6c74aeaaff1b5d21496cc1c6a7d4a4dc0697a74b2d1dead45de5161e0",
    "class_repository": "https://github.com/mwt5345/class_ede",
    "class_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "class_binary_sha256": "df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf",
    "contract_sha256": "a4d3c5c4e6399b46cf8f9f448300ce435913815750db68c33f965ce3477cf094",
    "point_sha256": "eabf2d50864f5cf8d4d0d6cca3ee11faba666ad1eb72eeea8742d180ced5afeb",
    "result_status": "RAW_NOT_QUALIFIED",
    "scope": "Six conditional one-cell branches; neither whole-history nor inference reference"
  },
  {
    "id": "I-Q042-V28-AUDIT",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "q": "Q-042",
    "title": "Independent actual V28 archive, repository, stage-arithmetic and continuity audit",
    "file": "q042_v28_ingestion_audit.json",
    "sha256": "7e0f236e46375da8aa43d9a05e1216fce48467b8e23aa2729c8e5aa44cd8bb0f",
    "checks": 58,
    "supported_claim": "Actual run/jobs/archive hashes, all29 raw files, six branches/112 stages/28 nodes, original kernel routing, exact common anchors and same-state restart pass a finite independent audit. No absolute accuracy certificate."
  },
  {
    "id": "I-Q042-V28-INTERPRETATION",
    "type": "BUBBLEVERSE NUMERICAL INTERPRETATION",
    "q": "Q-042",
    "title": "One-cell common-anchor endpoint differences and limited event-treatment conclusion",
    "inputs": [
      "I-Q042-V28-RAW",
      "I-Q042-V28-AUDIT",
      "I-Q042-V27-ATTRIBUTION",
      "I-Q042-V27-ENDPOINT"
    ],
    "supported_claim": "End-H differences alternate +/-1 ULP in both trials. The event convention removes the observable leading jump-related local refinement fingerprint under the frozen RAW conditioning; order and absolute/global/history errors remain unqualified."
  },
  {
    "id": "I-Q042-POSTV28-DESIGN-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Fresh immutable repository and completed-run status inspection",
    "repository": "Morfindien/Bubbleverse",
    "commit": "488a6c2ed59435137a9aad13b6c012e8aeef2e5e",
    "url": "https://github.com/Morfindien/Bubbleverse/tree/488a6c2ed59435137a9aad13b6c012e8aeef2e5e",
    "retrieval": "GitHub read connector; content Git-blob/SHA256 verification",
    "supported_claim": "Existing V26–V28 complete; no V29 target in full tree; current registry and README have stale completion state"
  },
  {
    "id": "I-Q042-POSTV28-INPUTS-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Recovered exact V26 accepted-entry/grid/prefix and two archived node streams",
    "origin_source_id": "I-Q042-V26RUN-001",
    "run_id": "37323656302",
    "artifact_id": 11351331442,
    "archive_sha256": "fa1b7e2c45650d60b2a68cd78622e8636a37ed870bd7e3ac49ac4cb3a7f2abb6",
    "retrieval": "Read-only artifact recovery; digest plus selected member hashes verified",
    "supported_claim": "Actual accepted input geometry exists and is recoverable; archived node samples are not a continuous-path certificate"
  },
  {
    "id": "I-Q042-POSTV28-PROTOCOL-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE NUMERICAL DESIGN",
    "title": "Finite conditional whole-history reference protocol with blocked qualification",
    "file": "q042_post_v28_reference_full_handoff.md",
    "inputs": [
      "K-Q042-V24-001",
      "K-Q042-V25-003",
      "K-Q042-SWITCH27-HYDROGEN",
      "I-Q042-POSTV28-INPUTS-001",
      "I-Q042-V28-INTERPRETATION"
    ],
    "supported_claim": "Real-entry continuous trajectories, reio_start and nested predicates must be treated; no credible node/history/support intervals or downstream propagation are supplied"
  },
  {
    "id": "I-Q042-ENCLOSURE-SOURCES-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Fresh immutable source and table inspection",
    "underlying_sources": [
      {
        "encoding": "utf-8",
        "sha": "c1683f56b43e0f2ec24a8ba6120133f604cb947c",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/thermodynamics.c",
        "display_title": "thermodynamics.c",
        "sha256": "d17657c1cbd9fd4b70d62d1c6eb102a128ee1ed4cbc5dae439254af91bc45fb6",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "fa44c774cf1fc7dbf6185e01980764f7eb260204",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/wrap_hyrec.c",
        "display_title": "wrap_hyrec.c",
        "sha256": "4747baba37424f05f168bb68d4b9bccb2c0f003bdba95ccf56fe0a4c30cc01bd",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "233f174bfb1758fa910866310340ae1bfad703db",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.c",
        "display_title": "hydrogen.c",
        "sha256": "734800ccd69b41d60b519f200003ce27c3b7640f76a70353499424842ba19616",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "9710fb166de45ab392ee7984801d8dbdf610319a",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/history.c",
        "display_title": "history.c",
        "sha256": "14d11b3663fcebd5a4072969237f4041549adb4449ddef875f3ca4caff948fe4",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "89837f3161cbf2d8b3485a6772bd16e0a484c93f",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/tools/arrays.c",
        "display_title": "arrays.c",
        "sha256": "c38471b1395bc111817b2467db9af9795e1e1ab0ef2a441ecca801a82adc09c4",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "088b34a699efe5d6d3aefb158229e9fb83d9a586",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hydrogen.h",
        "display_title": "hydrogen.h",
        "sha256": "1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "fd0cfa4f380d30640c4b2da47e4e35d6894b4dcb",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/fit_swift.dat",
        "display_title": "fit_swift.dat",
        "sha256": "46a644d7d2633b8f13080f9062df9b72a2e5adfa956d70d32ad1d7f4ec0a4641",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "5e8ac170fe7839ef391de0b129113c4a7a71af1e",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/external/HyRec2020/hyrectools.c",
        "display_title": "hyrectools.c",
        "sha256": "868a4f5104e90c18b84948843cb2090b22732e54d88b5f658323a38394275ce4",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "5f6be0fc77c31bd81198d9f28a9d73690a2baabd",
        "display_url": "https://github.com/mwt5345/class_ede/blob/5a131c91d657dd9a7c6364cc45b038710f8d0d97/source/background.c",
        "display_title": "background.c",
        "sha256": "84871d25c0a29391edf8d08b4826bd3ca3b33c638dae306375c0a681bb87d451",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "a2714099c4de9af5e9fa6d3a0fb269c3c5a247f6",
        "display_url": "https://github.com/Morfindien/Bubbleverse/blob/488a6c2ed59435137a9aad13b6c012e8aeef2e5e/README.md",
        "display_title": "README.md",
        "sha256": "b600285259ea35230f33dab688dca063fca5b5e5e867487f3209e26dfc4dcf86",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "54bfe699d285f19b3521f95faf2324056c75befb",
        "display_url": "https://github.com/Morfindien/Bubbleverse/blob/488a6c2ed59435137a9aad13b6c012e8aeef2e5e/bubbleverse_program_registry.json",
        "display_title": "bubbleverse_program_registry.json",
        "sha256": "ea732a7ebf5acf55fb1e6efc672a9d9aba19a90adc99097399944dbb423911ee",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "7f22c617fb98d1508a0b22a42dd3735a74d8288e",
        "display_url": "https://github.com/Morfindien/Bubbleverse/blob/488a6c2ed59435137a9aad13b6c012e8aeef2e5e/.github/workflows/00-bubbleverse-start.yml",
        "display_title": "00-bubbleverse-start.yml",
        "sha256": "3cd5b0642353c85d472f531e7c5490b56c307e2e274d38b866d1ad0dedebe288",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      },
      {
        "encoding": "utf-8",
        "sha": "e37243fc44ff1bc74daab8f5384be3ca05c41a87",
        "display_url": "https://github.com/Morfindien/Bubbleverse/blob/488a6c2ed59435137a9aad13b6c012e8aeef2e5e/q042_reference_native_v26.c",
        "display_title": "q042_reference_native_v26.c",
        "sha256": "efa6c4bbca15660613994763a6771fa8d4ce7a7ce433c0bbfea543c4aa8d7bad",
        "git_blob_verified": true,
        "retrieval_method": "connected GitHub read, pinned ref"
      }
    ]
  },
  {
    "id": "I-Q042-ENCLOSURE-ANALYSIS-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Finite conditional temperature/routing/spline derivation",
    "status": "CONDITIONAL_ANALYTIC_RESULT_INSTANCE_ENCLOSURE_NOT_ESTABLISHED",
    "artifact": "q042_post_v28_enclosure_full_handoff.md"
  },
  {
    "id": "I-Q042-ENCLOSURE-AUDIT-001",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Exact scalar, identity, preservation and prepared retirement checks",
    "status": "PASS_LIMITED_SCOPE"
  },
  {
    "id": "I-Q042-ENCLOSURE-INGESTION-001",
    "q": "Q-042",
    "title": "Post-V28 conditional enclosure ingestion, finite audit and implementation routing",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "date": "2026-10-05T20:34:50.309718+02:00",
    "retrieval_method": "attached files plus local deterministic verification",
    "evidence_limit": "No new runtime initialization, interval integration or live repository inspection",
    "input_manifest": {
      "q042_post_v28_enclosure_full_handoff.md": {
        "sha256": "9f823bb35d7be1cc5349affdb9fec0210f3cfd824d9171cc2027bc75f701046e",
        "bytes": 11469683
      },
      "q042_post_v28_enclosure_evidence.json": {
        "sha256": "8524e91b31997e7e3acfc996a3d865763bea1b891e4b9b6a177329b5b3869dc3",
        "bytes": 2164081
      },
      "q042_post_v28_enclosure_decision.json": {
        "sha256": "51fa886bf07c4adef3a67f073dfac86a02aa2d5a0e891ba8b9bd465a24ff0c54",
        "bytes": 3631
      },
      "README.md": {
        "sha256": "c1522528e16f67404d055559255bec79b6ad6af47ea0e5539e306284137a9752",
        "bytes": 21111
      },
      "bubbleverse_program_registry.json": {
        "sha256": "9352d1609b9fc22352e42eb60ee1ce3bbc9078bac697aa5e1454c89c49cf6054",
        "bytes": 84341
      }
    }
  },
  {
    "id": "I-Q042-V29-PREP-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "V29 prepared original-context capture and interval prerequisite implementation",
    "date": "2026-10-05T21:06:17.042322+02:00",
    "file": "q042_context_validation_v29.json",
    "claim": "Locally tested executable package; actual original initialization not yet acquired; no new cosmological result",
    "retrieval_method": "read-only GitHub, pinned C source fixtures, local MPFR interval and package verification"
  },
  {
    "id": "K-Q042-V29-MPFR-001",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "title": "GNU MPFR manual: rounding, assignment and conversion functions",
    "authors": "MPFR project",
    "url": "https://www.mpfr.org/mpfr-current/mpfr.html",
    "retrieval_date": "2026-10-05T21:06:17.042322+02:00",
    "relevant_section": "4.4 Rounding; set_d/get_d; arithmetic and special functions",
    "claim": "Directed modes and correctly rounded operations; the implementation gates runtime version 4.2.1; this source is documentation, not proof of absence of library bugs"
  },
  {
    "id": "K-Q042-V29-GITHUB-001",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "title": "GitHub Actions limits",
    "authors": "GitHub",
    "url": "https://docs.github.com/en/enterprise-cloud%40latest/actions/reference/limits",
    "retrieval_date": "2026-10-05T21:06:17.042322+02:00",
    "claim": "Current GitHub-hosted job limit is six hours; V29 jobs capped at 5/50/5 minutes"
  },
  {
    "id": "K-Q042-V29-HEADERS-001",
    "type": "PRIMARY TECHNICAL REPOSITORY SOURCE",
    "title": "Frozen CLASS / HyRec header snapshot set",
    "repository": "mwt5345/class_ede",
    "commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "url": "https://github.com/mwt5345/class_ede/tree/5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "retrieval_method": "connected GitHub fetch_file at pinned commit; Git blob identities independently checked",
    "claim": "Actual struct layouts, constants and signatures for V29 native exporter and scalar fixtures",
    "files": {
      "external/HyRec2020/energy_injection.h": {
        "git_blob_sha": "e58c7a27a03cc20f39d9c5d2b5cee24f88133142",
        "sha256": "e2f0603b2bfe730814bdd57d46eff9f53d8bb1e10315524b395aa4dde97de2ea"
      },
      "external/HyRec2020/helium.h": {
        "git_blob_sha": "9ee1dc74632115183f718f5f792f563fbac209d1",
        "sha256": "ca5cbebf2ad0c256c55ad425bce2c26da7d56463f7e7a5fa9112d7cb6970619c"
      },
      "external/HyRec2020/history.h": {
        "git_blob_sha": "a809dc3240237542361b983d244d884ea7b5f21a",
        "sha256": "b1331aed246610d2b1d598f8bedfa951974da0d2845b5c8f3d672bf33bf316f1"
      },
      "external/HyRec2020/hydrogen.h": {
        "git_blob_sha": "088b34a699efe5d6d3aefb158229e9fb83d9a586",
        "sha256": "1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52"
      },
      "external/HyRec2020/hyrectools.h": {
        "git_blob_sha": "6e17d9a0ca2f431b09993050e1cecd3112f55312",
        "sha256": "00e71fdbaef4831f41822e00750a24e03c9954175b6a9680c67fb0ffc1be5715"
      },
      "external/HyRec2020/wrap_hyrec.h": {
        "git_blob_sha": "ca9b29988e591b7bae6461cf4aee61c99ac0b1f2",
        "sha256": "eac436c13e1f89516ae5fa1ffb66f7e265c63211152982629876577a2538999b"
      },
      "external/RecfastCLASS/wrap_recfast.h": {
        "git_blob_sha": "9b2e0d3a9e249bd8132f3bca4943d4c7b91e9b5f",
        "sha256": "1e5609a3e5b1ddd8f7ad99df336311a9f769867e52f203e0cb6481b617e2de73"
      },
      "external/heating/injection.h": {
        "git_blob_sha": "769c31f1e302bf504eb89bb89fbc835a2fbbeab3",
        "sha256": "5e20554b838f887971ef0f4c5e62a7eb6cdd97c7f5ce77849ca656ea0fe292f9"
      },
      "external/heating/noninjection.h": {
        "git_blob_sha": "3c7c519db6744785b81f2cbd961e3377ac813f45",
        "sha256": "4c33b9504ecba728f323bf8a1b6bd09e319848c434de55cfcfd638f69a19adee"
      },
      "include/arrays.h": {
        "git_blob_sha": "1f886e34861c1ee8c7d4a3e15ed00cb28cbcc97e",
        "sha256": "2d8f69df23bae1a8bda98c47079ded8b27a5e59985ccc2d70bd2709cd7f12a6d"
      },
      "include/background.h": {
        "git_blob_sha": "742e4f19d738b1c60467a81aadc8db4b28eb001c",
        "sha256": "b329b21bce11705eed64aa242a06272a7d9554ad1fe1de8eda870b6cfb3f2397"
      },
      "include/class.h": {
        "git_blob_sha": "004203befd4be0e971078cb38b8a4fea7f040448",
        "sha256": "d2848d216f673e28a14a5e145c0ab561962ffa38ec423e0f4d9b116843bb9edc"
      },
      "include/common.h": {
        "git_blob_sha": "6d0b6a492699c4b5ecc323ec1bb668281882b43a",
        "sha256": "410ea60e5ca1de7fc501d644711fc21023fa2cbdd56dd8daede1637a3b9e900c"
      },
      "include/dei_rkck.h": {
        "git_blob_sha": "648bf87f9f3ee49449520e022b3c987ec076a9db",
        "sha256": "77c56981a3c7e26e57531bb56d6af38bb7468e5457cd195f70b95b8a497973b3"
      },
      "include/distortions.h": {
        "git_blob_sha": "9cd66f306bbe6a518b8bb40470b465c934aca850",
        "sha256": "88ca84c63f35e0fa40f3c713e9fe46d3a288ac31ffe3708b9124d3746652557b"
      },
      "include/evolver_ndf15.h": {
        "git_blob_sha": "263187fa0080fbc567cf8947b9a02beb6c614d13",
        "sha256": "069846924e0593b8bcd98f0430edec3bcda50ad9f4b2355a393d54737d7b45d4"
      },
      "include/evolver_rkck.h": {
        "git_blob_sha": "9da76c0f3a90f276e7f76a0bd68d034c1950b460",
        "sha256": "1910f9ab2f56a1cb6c5dd1f9c61b3aa51cf35ccdd462723c40c57247ee8c6cc7"
      },
      "include/fourier.h": {
        "git_blob_sha": "5841dd98bd27e9d635928f0e38864335fc9779a6",
        "sha256": "6b241f648f3863b9bc5657eb75da2ba8df30399f139286f86a4ebae2f183c405"
      },
      "include/growTable.h": {
        "git_blob_sha": "0f73e8b798f9ebeb240328c998d4b0b17fdac2d6",
        "sha256": "7f58701538838ff651289c99ec0fa1ea2b72afc72471b65b5878c460b5da47b9"
      },
      "include/harmonic.h": {
        "git_blob_sha": "2d284a83e7f64342f5d6f860cd43fcd764b9be71",
        "sha256": "6ca68b04d962ba0047f4cce6be87d024a8f9a7b5b755fe3d95f339083e3f3f10"
      },
      "include/hermite3_interpolation_csource.h": {
        "git_blob_sha": "0cfe04375f5f3ae556a070a1e4046401bcf891c7",
        "sha256": "da5920f23387f97f6090d2d6fe2c9b073b90b7f6ff27d12e8ac6450f3e93ec43"
      },
      "include/hermite4_interpolation_csource.h": {
        "git_blob_sha": "21fc2f8f5f6a35dee5b8f2d6c49a0550bbe43176",
        "sha256": "0f7fa7d3f781749f517c048c53d55f0a70ad944bdced86d6e311bfdb6d48079a"
      },
      "include/hermite6_interpolation_csource.h": {
        "git_blob_sha": "6920a6cb665260df014c9857e855ce46cd66e674",
        "sha256": "f3462fe9c622e84c49a0e4a06c743cb2d38f5b9016023f74d4c1a1a9ee6830ff"
      },
      "include/hyperspherical.h": {
        "git_blob_sha": "140c4c4682cc429ed58f9d4402c03ac3da892357",
        "sha256": "4a4ea6ddb11cb04b4173a637cedf32ee2cd326f6e3cca10a1028cc7669d93869"
      },
      "include/input.h": {
        "git_blob_sha": "4d646f9363312f3cbf86b1ff48506a057a6a9a51",
        "sha256": "895b1460758732b0cc51b42287a4a2601b85280344fe28afaf1675aa891248fe"
      },
      "include/lensing.h": {
        "git_blob_sha": "8452a940b36259b837f4c8a0cfb709cb0fd9352f",
        "sha256": "c45b1de8675c5edeca3bc0b9dc96f8369ec98346d8822a825869a8f9418bcd71"
      },
      "include/macros_precision.h": {
        "git_blob_sha": "d54770db984a45b73bd16bf6c038112e783a8b8e",
        "sha256": "14a6887545b0f090bf15d2f70d8329e7d7f582eaa0f9c5d6952da8990890bfd6"
      },
      "include/output.h": {
        "git_blob_sha": "1b1a3ccdf63c288687235b49a2170caf393d37a2",
        "sha256": "1a1b52ffdb26aa6e6ffc2f7889d009f97fe515d2568c9d8402495d11a6b2c27b"
      },
      "include/parser.h": {
        "git_blob_sha": "1214231a0675b1f00cadb5aa044e3bb7ccc40aa2",
        "sha256": "1c20b33f0f30041490c7eda8a5bb8fa1ef1bea0ae399a7552f03dc991a8750b3"
      },
      "include/perturbations.h": {
        "git_blob_sha": "89a90fcab3ccc67c7250d638d34d6f0fbbb32cfa",
        "sha256": "79f2f536aec79c2739862782326f8d2391a1f79a775ae9f2a8bf7395e94c432c"
      },
      "include/precisions.h": {
        "git_blob_sha": "421992b5148eac4852aa5060fc887e26eca44edb",
        "sha256": "1c2416a207330e295bf3087806a0936e49e396dc22db3331bbc282bb14562cfe"
      },
      "include/primordial.h": {
        "git_blob_sha": "7c4fe94663d4b3b8069a5ef67dbc965a447a71e8",
        "sha256": "fbb72148601c309b05ad5a9e947bdde5c6e2ddb99e7088fcefc88b282a699846"
      },
      "include/quadrature.h": {
        "git_blob_sha": "19aed33f5fcadccd3c7bd3f07d6e86175a356b2f",
        "sha256": "245f9025cc6049ea9c09ccd57faa28d2d970e05fe96093be1c54eccde97fd075"
      },
      "include/sparse.h": {
        "git_blob_sha": "82179c6736ea40b60a556b306dcef717b324241c",
        "sha256": "830c38ddea0268270c5c6e8d07631c4667b69e6904d7950816701c2e371c56f7"
      },
      "include/svnversion.h": {
        "git_blob_sha": "779741fa8addf1e0eba15a709e660e01c708d075",
        "sha256": "6455940c5fe90b4786147482f2fcf8492b15e10f4b8f4139b9129145f0b728e8"
      },
      "include/thermodynamics.h": {
        "git_blob_sha": "f02f2591077ee11f3bc9481a4491b0feb83cf26d",
        "sha256": "f000e372c0db60663cc49f4bb95ab9f1d63238201ee7b3b51ca791c0f45ba0f0"
      },
      "include/transfer.h": {
        "git_blob_sha": "b92f6a89d80c92cfba2515422d7b027492e132ed",
        "sha256": "1f526b7c0b49da6e6ea9b936b76c9c6ee490dc5fe3a46e03def949ff477ef749"
      },
      "include/trigonometric_integrals.h": {
        "git_blob_sha": "da82b53a368dbe633029cb6a2061572517c3eba8",
        "sha256": "221fbff5c2140ac3e7b8fda1c3cccc40e612f48d5ce8f66e759ebe96563e09a6"
      }
    }
  },
  {
    "id": "I-Q042-V29-RUN-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL AND NUMERICAL EVIDENCE",
    "title": "V29 actual initialized context and finite real-table interval qualification",
    "program_id": "Q042-CONTEXT-V29",
    "run_id": "37362125253",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37362125253",
    "repository": "Morfindien/Bubbleverse",
    "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "date": "2026-10-05T19:23:12Z",
    "supported_claim": "Context captured; positivity/24 explicit boxes and collector pass; no history or science qualification.",
    "retrieval_method": "User supplied worker artifact, SHA256 matched to GitHub digest; collector independently retrieved",
    "artifact_digests": {
      "q042-v29-37362125253-final": "sha256:6c8b5aa8bc98aa8040df4b5906e4ce5899f3997b3320c7313159f783ea8aa4c1",
      "q042-v29-37362125253-context-and-checks": "sha256:3a543d095512e7ea46447275bee8df112704bd128f725d04a500a62c9dcd6aa9"
    }
  },
  {
    "id": "I-Q042-V29-INGESTION-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "title": "Bounded V29 provenance, scope and exact-rational positivity ingestion",
    "date": "2026-10-06T06:42:23.433171+02:00",
    "file": "q042_v29_ingestion_audit.json",
    "supported_claim": "Scoped technical result accepted; Q remains unresolved; next conditional history task; prepared retirement files",
    "retrieval_method": "Local file analysis, exact-rational cubic controls, official project provenance"
  },
  {
    "id": "K-Q042-V29-REPO-001",
    "q": "Q-042",
    "type": "OFFICIAL PROJECT REPOSITORY / TECHNICAL EVIDENCE",
    "title": "Bubbleverse V29 execution and repository records",
    "url": "https://github.com/Morfindien/Bubbleverse/actions/runs/37362125253",
    "repository": "Morfindien/Bubbleverse",
    "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "retrieval_date": "2026-10-06T06:42:23.433171+02:00",
    "retrieval_method": "Connected GitHub read-only run, jobs, artifacts, recursive tree, main commit",
    "supported_claim": "Actual execution identities and stale post-run README/registry state; not independent scientific confirmation"
  },
  {
    "id": "I-Q042-V30-001",
    "title": "V30 bounded local conditional history attempts",
    "type": "BUBBLEVERSE NUMERICAL RESULT",
    "file": "q042_history_evidence_v30.json",
    "retrieval": "Actual local execution; exact raw text and SHA256 retained",
    "config_sha256": "57f19390dcab1bffb13f0c26750a15c578060c6a24ba311642bb2204115bf00a",
    "status": "PARTIAL"
  },
  {
    "id": "I-Q042-V30-VALIDATION-001",
    "title": "V30 finite tests and post-run inclusion audit",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "file": "q042_history_evidence_v30.json",
    "retrieval": "Local test output and post-run replay of accepted certificates",
    "scope": "Conditional interval implementation checks, not independent physical validation"
  },
  {
    "id": "K-Q042-V30-MPFR-001",
    "title": "GNU MPFR 4.2.1 manual",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "url": "https://www.mpfr.org/mpfr-4.2.1/mpfr.html",
    "software_version": "4.2.1",
    "retrieval": "Web search of official versioned documentation",
    "supported_claim": "Directed rounding semantics; not validation of the complete application"
  },
  {
    "id": "K-Q042-V30-GITHUB-001",
    "title": "GitHub Actions limits",
    "type": "OFFICIAL TECHNICAL DOCUMENTATION",
    "url": "https://docs.github.com/en/enterprise-cloud%40latest/actions/reference/limits",
    "retrieval": "Official documentation web search",
    "supported_claim": "Runtime-design reference only; no GitHub execution was needed"
  },
  {
    "id": "I-Q042-V30-INGESTION-001",
    "q": "Q-042",
    "title": "V30 ingestion integrity audit, mathematical scope analysis and routing decision",
    "type": "BUBBLEVERSE TECHNICAL / MATHEMATICAL ANALYSIS",
    "date": "2026-10-06T18:17:50.134868+02:00",
    "retrieval_method": "Received individual artifacts, deterministic exact-fraction checks, frozen primary source and live read-only repository inspection",
    "file": "q042_v30_ingestion_audit.json",
    "evidence_limit": "No new trajectory, solver qualification, binary/reference validation or cosmological result"
  },
  {
    "id": "K-Q042-V30-LOHNER-001",
    "title": "A Lohner-type algorithm for control systems and ordinary differential inclusions",
    "authors": [
      "Tomasz Kapela",
      "Piotr Zgliczyński"
    ],
    "year": 2007,
    "arxiv": "0712.0910v1",
    "doi": "10.48550/arXiv.0712.0910",
    "url": "https://arxiv.org/abs/0712.0910",
    "relevant_section": "Sections 1.2, 2.2 and Theorem 9",
    "type": "PRIMARY MATHEMATICAL PREPRINT",
    "retrieval_method": "Official arXiv abstract and full paper via web retrieval",
    "supported_claim": "Rigorous reachable-set techniques exist; a constant uncertain parameter is not generally equivalent to time-varying differential-inclusion forcing. C1 premises require assessment before use on this piecewise RHS. No Bubbleverse/CAPD compatibility was established."
  },
  {
    "id": "K-Q042-V30-ARCHITECTURE-001",
    "q": "Q-042",
    "title": "Current Bubbleverse architecture and execution inventory, post-V30 ingestion",
    "type": "OFFICIAL PROJECT REPOSITORY / TECHNICAL EVIDENCE",
    "repository": "Morfindien/Bubbleverse",
    "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "url": "https://github.com/Morfindien/Bubbleverse/blob/72cf9e92fc794c122f593a77b6a555e6e97f6a2e/q042_treatment_design_motor.md",
    "retrieval_method": "Read-only recursive tree and Git-blob verified motor, README and registry snapshots",
    "supported_claim": "The scoped mathematical/reference-design task belongs to the established execution motor; a separate Mathematics engine is not verified. Live V29 registry entry is still ACTIVE and V30 is absent."
  },
  {
    "id": "I-Q042-COMPARISON-DESIGN-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE MATHEMATICAL / STATIC TECHNICAL EVIDENCE",
    "title": "One bounded hydrogen/normalized-temperature comparison design and static frozen-domain certificate after V30",
    "date": "2026-10-06T20:43:10.889063+02:00",
    "artifact": "q042_comparison_evidence_post_v30.json",
    "method_spec_id": "Q042-COMPARISON-DESIGN-001",
    "scope": "Exact source real-algebra and static initialized-table verification, conditional on existing AC solutions; not a trajectory, original binary error bound, upstream accuracy, reference or cosmological result",
    "retrieval_method": "Supplied full journal and sources; fresh read-only pinned GitHub; directed MPFR/exact rational checks",
    "limitations": [
      "Original discontinuous existence/uniqueness unproved",
      "Local enclosure widths not yet measured",
      "Reference/science gates unresolved"
    ]
  },
  {
    "id": "I-Q042-COMPARISON-INGESTION-001",
    "q": "Q-042",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE / RESULT INGESTION",
    "title": "Integrity, scope and materiality ingestion of the completed conditional comparison design",
    "date": "2026-10-07T06:46:19.997740+02:00",
    "artifact": "q042_comparison_ingestion_audit.json",
    "origin": "Result Ingestion & Routing Engine",
    "received_result_id": "R-Q042-COMPARISON-DESIGN-001",
    "method_spec_id": "Q042-COMPARISON-DESIGN-001",
    "repository": "Morfindien/Bubbleverse",
    "commit": "72cf9e92fc794c122f593a77b6a555e6e97f6a2e",
    "retrieval_method": "Received local artifact bytes and fresh read-only pinned connected GitHub",
    "scope": "Identity and preservation audit plus scientific routing judgment; no new integration, theorem reproduction or physical conclusion",
    "limitations": [
      "CASE ID NOT DOCUMENTED",
      "No implemented comparison trajectory",
      "Binary, upstream and downstream qualification unresolved"
    ]
  },
  {
    "id": "I-Q042-COMPARISON-V31-001",
    "q": "Q-042",
    "title": "Frozen V31 conditional comparison implementation and two bounded raw attempts",
    "type": "BUBBLEVERSE NUMERICAL / TECHNICAL RESULT",
    "date": "2026-10-07T05:19:56.871032+00:00",
    "program_id": "Q042-COMPARISON-V31",
    "run_id": "Q042_COMPARISON_V31_LOCAL_001",
    "file": "q042_comparison_result_v31.json",
    "config_sha256": "2f7a5d08e7566c613de93328fe4d4d6760d8ede81f6c3b789e230f64ca202dd1",
    "source_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "retrieval_method": "Local one-shot MPFR directed interval execution; independent parent deadline and raw collection",
    "evidence_limit": "Conditional real-table solution bounds only; no original-binary/upstream/downstream accuracy or cosmological result"
  },
  {
    "id": "I-Q042-COMPARISON-V31-VALIDATION-001",
    "q": "Q-042",
    "title": "Finite V31 preflight, independent review and raw lineage/completeness collection",
    "type": "BUBBLEVERSE TECHNICAL EVIDENCE",
    "date": "2026-10-07T05:19:56.871032+00:00",
    "file": "q042_comparison_audit_v31.json",
    "retrieval_method": "21 implementation fixtures, independent read-only review before attempts, frozen hashes and raw chain checks",
    "evidence_limit": "Component pass does not establish whole-history completeness, reference truth or science"
  },
  {
    "id": "I-Q042-V31-INGESTION-001",
    "q": "Q-042",
    "title": "V31 ingestion, exact identity audit and conditional support-cap incompatibility certificate",
    "type": "BUBBLEVERSE TECHNICAL / MATHEMATICAL EVIDENCE",
    "date": "2026-10-07T07:40:24.180641+02:00",
    "artifact": "q042_v31_ingestion_audit.json",
    "origin": "Result Ingestion & Routing Engine",
    "incoming_result_id": "R-Q042-COMPARISON-V31-001",
    "program_id": "Q042-COMPARISON-V31",
    "retrieval_method": "Preserved raw artifacts, exact dyadic comparisons, one directed frozen-source tail box per trial and fresh read-only repository inspection",
    "source_commit": "5a131c91d657dd9a7c6364cc45b038710f8d0d97",
    "scope": "Conditional mathematical failure of the unchanged stored-interval support_candidates policy under cap32, plus bounded epistemic closure; not an executed tau value, original-binary accuracy or cosmological conclusion",
    "limitations": [
      "Existing AC-solution/global-rail scope only",
      "No universal impossibility theorem",
      "No new trajectory or precision/correlation representation",
      "Final killed-tail counters remain NOT DOCUMENTED"
    ]
  }
]
```

## ORIGINAL CLAIM MAPS — unchanged inherited and new maps

```json
{
  "inherited_claim_maps": {
    "inherited_claim_maps": {
      "inherited_claim_maps": {
        "inherited_claim_maps": {
          "prior_new_claim_map": {
            "C-Q042-V29-001": [
              "I-Q042-V29-PREP-001",
              "K-Q042-V29-HEADERS-001"
            ],
            "C-Q042-V29-002": [
              "I-Q042-V29-PREP-001",
              "K-Q042-V29-MPFR-001"
            ],
            "C-Q042-V29-003": [
              "I-Q042-V29-PREP-001",
              "K-Q042-V29-GITHUB-001"
            ],
            "C-Q042-V29-004": [
              "I-Q042-ENCLOSURE-INGESTION-001",
              "I-Q042-V29-PREP-001"
            ]
          },
          "new_claim_to_source_map": {
            "C-Q042-V29-I001": [
              "I-Q042-V29-RUN-001",
              "K-Q042-V29-REPO-001",
              "I-Q042-V29-INGESTION-001"
            ],
            "C-Q042-V29-I002": [
              "I-Q042-V29-RUN-001",
              "I-Q042-V29-PREP-001",
              "K-Q042-V29-MPFR-001"
            ],
            "C-Q042-V29-I003": [
              "I-Q042-V29-RUN-001",
              "I-Q042-V29-INGESTION-001"
            ],
            "C-Q042-V29-I004": [
              "I-Q042-V29-RUN-001",
              "I-Q042-ENCLOSURE-INGESTION-001",
              "I-Q042-V29-INGESTION-001"
            ],
            "C-Q042-V29-I005": [
              "I-Q042-V29-INGESTION-001",
              "I-Q042-ENCLOSURE-INGESTION-001"
            ],
            "C-Q042-V29-I006": [
              "K-Q042-V29-REPO-001",
              "I-Q042-V29-RUN-001"
            ]
          }
        },
        "v30_claim_map": {
          "V30-PARTIAL-001": {
            "claim": "Both bounded attempts stop at z=49.203125 after 51 steps and 54 native nodes",
            "sources": [
              "I-Q042-V30-001"
            ]
          },
          "V30-CAUSE-001": {
            "claim": "Fixed width-based padding prevents further admissible tubes irrespective of step shrinking",
            "sources": [
              "I-Q042-V30-001",
              "I-Q042-V30-VALIDATION-001"
            ]
          },
          "V30-SCOPE-001": {
            "claim": "No full-history, binary-roundoff, upstream, tau or scientific qualification established",
            "sources": [
              "I-Q042-V30-001",
              "I-Q042-V30-VALIDATION-001"
            ]
          }
        },
        "new_claim_to_source_map": {
          "V30-INGEST-IDENTITY": {
            "claim": "All eight companions match the received decision; raw hashes and frozen source/config identities match",
            "sources": [
              "I-Q042-V30-001",
              "I-Q042-V30-INGESTION-001"
            ]
          },
          "V30-INGEST-FAILURE": {
            "claim": "The documented stop is an interval-construction obstruction, not physical negative hydrogen or global method impossibility",
            "sources": [
              "I-Q042-V30-001",
              "I-Q042-V30-VALIDATION-001",
              "I-Q042-V30-INGESTION-001"
            ]
          },
          "V30-INGEST-ALTERNATIVE": {
            "claim": "Exact real-algebra production/recombination factorization supports a conditional scalar-comparison design candidate; whole-history applicability is unproved",
            "sources": [
              "K-Q042-SWITCH27-HYDROGEN",
              "I-Q042-ENCLOSURE-SOURCES-001",
              "I-Q042-V30-INGESTION-001"
            ]
          },
          "V30-INGEST-DI-SCOPE": {
            "claim": "Generic rigorous-solver availability does not qualify this piecewise RHS or justify treating branch uncertainty as fixed parameters",
            "sources": [
              "K-Q042-V30-LOHNER-001"
            ]
          },
          "V30-INGEST-ROUTE": {
            "claim": "One bounded source-backed mathematical design task is materially useful and belongs to the existing execution engine",
            "sources": [
              "I-Q042-V30-INGESTION-001",
              "K-Q042-V30-ARCHITECTURE-001"
            ]
          }
        }
      },
      "design_claim_map": {
        "C-Q042-COMP-D001": {
          "claim": "Frozen TLA/HMLA real RHS has nonnegative production/recombination factorization and positive original transfer denominators with C factors <=1",
          "sources": [
            "K-Q042-SWITCH27-HYDROGEN",
            "K-Q042-V25-003",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        },
        "C-Q042-COMP-D002": {
          "claim": "Normalized temperature gives positive global rails; source flags, helium and SWIFT branches are covered within the frozen conditional domain",
          "sources": [
            "K-Q042-V24-001",
            "K-Q042-V25-003",
            "I-Q042-V29-RUN-001",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        },
        "C-Q042-COMP-D003": {
          "claim": "3700 exact Bernstein atomic cells plus positive background cubics give finite conditional coefficient/domain bounds without a trajectory",
          "sources": [
            "I-Q042-V29-RUN-001",
            "K-Q042-V29-MPFR-001",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        },
        "C-Q042-COMP-D004": {
          "claim": "Comparison flows on already certified rails remove additive width inflation; width has an explicit damping/forcing identity, not a promised precision result",
          "sources": [
            "I-Q042-COMPARISON-DESIGN-001",
            "I-Q042-V30-001"
          ]
        },
        "C-Q042-COMP-D005": {
          "claim": "Frozen literal tau and mathematical cubic tau must stay separately identified; original plus sign and support semantics cannot be silently changed",
          "sources": [
            "K-Q042-V24-001",
            "I-Q042-ENCLOSURE-SOURCES-001",
            "K-Q042-INGESTDESIGN-002",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        },
        "C-Q042-COMP-D006": {
          "claim": "This conditional enclosure proof does not supply existence/uniqueness for the original switched RHS or original binary/upstream/downstream accuracy",
          "sources": [
            "K-Q042-V30-LOHNER-001",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        },
        "C-Q042-COMP-D007": {
          "claim": "The bounded design task is fulfilled; ingestion must assess one specific bounded implementation rather than repeating design or V30",
          "sources": [
            "K-Q042-V30-ARCHITECTURE-001",
            "I-Q042-COMPARISON-DESIGN-001"
          ]
        }
      },
      "new_claim_to_source_map": {
        "C-Q042-COMP-I001": {
          "claim": "The received completed design and source/helper identities pass this integrity audit; its evidence remains conditional mathematical/static evidence",
          "sources": [
            "I-Q042-COMPARISON-DESIGN-001",
            "I-Q042-COMPARISON-INGESTION-001"
          ]
        },
        "C-Q042-COMP-I002": {
          "claim": "One frozen bounded implementation can materially test full-history and functional completion after removing V30 fixed-width inflation; usefulness and scientific accuracy are not promised",
          "sources": [
            "I-Q042-COMPARISON-DESIGN-001",
            "I-Q042-V30-001",
            "I-Q042-COMPARISON-INGESTION-001"
          ],
          "epistemic_status": "ROUTING_INFERENCE"
        },
        "C-Q042-COMP-I003": {
          "claim": "Q-042 remains unresolved; raw conditional completion would not qualify original-binary, upstream or downstream inference accuracy",
          "sources": [
            "I-Q042-COMPARISON-DESIGN-001",
            "I-Q042-COMPARISON-INGESTION-001"
          ]
        },
        "C-Q042-COMP-I004": {
          "claim": "The established execution engine is the sole next destination; no new engine or runnable ID is created here",
          "sources": [
            "K-Q042-V30-ARCHITECTURE-001",
            "I-Q042-COMPARISON-INGESTION-001"
          ]
        },
        "C-Q042-COMP-I005": {
          "claim": "Current repository evidence matches the received snapshots; live V29 remains ACTIVE and V30 absent. Prepared retirement/README corrections have not been applied remotely",
          "sources": [
            "I-Q042-COMPARISON-INGESTION-001",
            "K-Q042-V29-REPO-001"
          ]
        }
      }
    },
    "new_claim_to_source_map": {
      "V31-IMPLEMENTATION": {
        "claim": "Frozen conditional method implemented with directed arithmetic, original branch/electron/source semantics, and certificate-first outputs",
        "sources": [
          "I-Q042-COMPARISON-V31-001",
          "I-Q042-COMPARISON-V31-VALIDATION-001"
        ]
      },
      "V31-ACTUAL-OUTPUT": {
        "claim": "Actual per-trial completeness, stop reasons, last enclosures and artifacts are retained separately",
        "sources": [
          "I-Q042-COMPARISON-V31-001"
        ]
      },
      "V31-SCOPE": {
        "claim": "Reference truth, original-binary arithmetic, upstream accuracy and downstream acceptance remain unresolved; no scientific promotion or production restart",
        "sources": [
          "I-Q042-COMPARISON-V31-001",
          "I-Q042-COMPARISON-V31-VALIDATION-001"
        ]
      }
    },
    "raw_delivery_map": {
      "UPPER/attempt.json": {
        "delivery_file": "Q042_V31_UPPER_attempt.json",
        "sha256": "930e33c85372901a6e3ab2082934fcef2484ff28a7aa8b1a1d4cec042e667395",
        "bytes": 126
      },
      "UPPER/nodes.jsonl": {
        "delivery_file": "Q042_V31_UPPER_nodes.jsonl",
        "sha256": "a42fff6504cdb50532e3dca95c8cc4d9e9251e548b0008d1b9388cc5a1793d25",
        "bytes": 3284481
      },
      "UPPER/steps.jsonl": {
        "delivery_file": "Q042_V31_UPPER_steps.jsonl",
        "sha256": "d2521b47dd099dff263bb939e56600f319b1971d2b94b0f532775c5fa0688778",
        "bytes": 40462360
      },
      "UPPER_supervisor/process.json": {
        "delivery_file": "Q042_V31_UPPER_parent_process.json",
        "sha256": "9d09ba8667014110d39d755786604fa187efb23ec56de7ab61d79e177af2f41e",
        "bytes": 838
      },
      "UPPER_supervisor/stdout.log": {
        "delivery_file": null,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "bytes": 0,
        "delivery_action": "ZERO_BYTE_LOG_RECORDED_IN_MANIFEST; NO_CONTENT_TO_DELIVER"
      },
      "UPPER_supervisor/stderr.log": {
        "delivery_file": null,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "bytes": 0,
        "delivery_action": "ZERO_BYTE_LOG_RECORDED_IN_MANIFEST; NO_CONTENT_TO_DELIVER"
      },
      "LOWER/attempt.json": {
        "delivery_file": "Q042_V31_LOWER_attempt.json",
        "sha256": "5102b5e1b9dad218a4e5c78a53fe21163284b553c2b84003cd891df5669366a5",
        "bytes": 126
      },
      "LOWER/nodes.jsonl": {
        "delivery_file": "Q042_V31_LOWER_nodes.jsonl",
        "sha256": "ae785faeb9658fac5516cca176c125767b8aa20b64d60aa85b1e116c536eb98b",
        "bytes": 3286678
      },
      "LOWER/steps.jsonl": {
        "delivery_file": "Q042_V31_LOWER_steps.jsonl",
        "sha256": "c0ab73d7520e2b3acf6ced8857a3a2e83528fd78032beb47da0636bf920e362c",
        "bytes": 38929409
      },
      "LOWER_supervisor/process.json": {
        "delivery_file": "Q042_V31_LOWER_parent_process.json",
        "sha256": "81cc55d607eb55b4a23854a4d1c4cfe1ae1b278e23e413bb5f7a739f4bd4d318",
        "bytes": 842
      },
      "LOWER_supervisor/stdout.log": {
        "delivery_file": null,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "bytes": 0,
        "delivery_action": "ZERO_BYTE_LOG_RECORDED_IN_MANIFEST; NO_CONTENT_TO_DELIVER"
      },
      "LOWER_supervisor/stderr.log": {
        "delivery_file": null,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "bytes": 0,
        "delivery_action": "ZERO_BYTE_LOG_RECORDED_IN_MANIFEST; NO_CONTENT_TO_DELIVER"
      }
    }
  },
  "new_claim_to_source_map": {
    "V31-INGEST-IDENTITY": {
      "claim": "Attached pre-V31 files match the prior state; newer V31 delivery and the complete cumulative journal are recovered with exact hashes and all90 source objects unchanged",
      "sources": [
        "I-Q042-COMPARISON-INGESTION-001",
        "I-Q042-COMPARISON-V31-001",
        "I-Q042-V31-INGESTION-001"
      ]
    },
    "V31-INGEST-PARTIAL": {
      "claim": "Both one-shot trials ended at parent600s caps:3233/3210 of3334 nodes; no child final reports and no computed tau. Last retained certificate endpoints are not represented as last committed endpoints.",
      "sources": [
        "I-Q042-COMPARISON-V31-001",
        "I-Q042-COMPARISON-V31-VALIDATION-001"
      ]
    },
    "V31-INGEST-FUNCTIONAL": {
      "claim": "Frozen support_candidates would retain138 UPPER and3002 LOWER candidates above cap32 even after any append-only rail-admissible continuation; missing-tail source intervals cannot reduce min_hi. No actual tau test was executed.",
      "sources": [
        "I-Q042-COMPARISON-DESIGN-001",
        "I-Q042-COMPARISON-V31-001",
        "I-Q042-V31-INGESTION-001"
      ]
    },
    "V31-INGEST-CLOSURE": {
      "claim": "The full contract-preserving inference is not established by documented tested paths; general feasibility remains inconclusive. Close this investigation epistemically without a scientific result pass or universal impossibility claim.",
      "sources": [
        "I-Q042-COMPARISON-V31-001",
        "I-Q042-V31-INGESTION-001"
      ]
    },
    "V31-INGEST-NO-PHYSICS": {
      "claim": "Numerical/reference limitations imply no new EDE/LCDM preference, physical falsification, H0 value or resolution of Hubble tension.",
      "sources": [
        "I-Q042-V31-INGESTION-001"
      ]
    }
  }
}
```


---
# RECOVERED GLOBAL CHRONOLOGICAL HISTORY — Q001–Q043

Verbatim pdftotext -layout transcription of the supplied Q-journal PDF; formatting can differ from the PDF, whose original bytes and hash remain authoritative. These chronological entries are history, not competing active journals. No standalone Q010 entry was recovered.

0.42
BUBBLEVERSE
Q Journals
Building a Model of the Universe from Observation
Q001-Q043
The chronological research record

BUBBLEVERSE Q JOURNALS
0.42
Contents
Introduction to the Journal Record..........................................................................................................4
Q001..................................................................................................................................................................5
Q002..................................................................................................................................................................7
Q003................................................................................................................................................................10
Q004................................................................................................................................................................12
Q005................................................................................................................................................................15
Q006................................................................................................................................................................18
Q007................................................................................................................................................................21
Q008................................................................................................................................................................24
Q009................................................................................................................................................................27
Q010................................................................................................................................................................30
Q011................................................................................................................................................................33
Q012................................................................................................................................................................36
Q013................................................................................................................................................................39
Q014................................................................................................................................................................42
Q015................................................................................................................................................................45
Q016................................................................................................................................................................48
Q017................................................................................................................................................................51
Q018................................................................................................................................................................54
Q019................................................................................................................................................................58
Q020................................................................................................................................................................61
Q021................................................................................................................................................................64

BUBBLEVERSE Q JOURNALS
0.42
Q022................................................................................................................................................................67
Q023................................................................................................................................................................70
Q024................................................................................................................................................................73
Q025................................................................................................................................................................76
Q026................................................................................................................................................................79
Q027................................................................................................................................................................82
Q028................................................................................................................................................................85
Q029................................................................................................................................................................88
Q030................................................................................................................................................................91
Q031................................................................................................................................................................94
Q032................................................................................................................................................................97
Q033............................................................................................................................................................. 100
Q034............................................................................................................................................................. 103
Q035............................................................................................................................................................. 106
Q036............................................................................................................................................................. 109
Q037............................................................................................................................................................. 112
Q038............................................................................................................................................................. 115
Q039............................................................................................................................................................. 118
Q040............................................................................................................................................................. 121
Q041............................................................................................................................. 124
Q042............................................................................................................................. 129

BUBBLEVERSE Q JOURNALS
0.42
Appendix E — Bubbleverse Q-Journals —
Q001-Q043
Introduction to the Journal Record
The main chapters of this book organize the surviving science logically. This appendix
preserves the investigation chronologically.
Each Q-Journal records, where available, the question that was asked, the scientific state
entering the question, inherited results, hypotheses, methods, evidence, programmes,
workflows, tests, intermediate and final results, failed attempts, negative results, model
changes, provenance and the handoff to the next question.
Many early journals are retrospective reconstructions because complete journal records
were not originally maintained at the time of those questions. Their retrospective status
remains explicitly labelled. Missing historical GitHub information is not filled by invention.
Later corrections do not erase earlier journal states. Superseded numbers, failed numerical
routes and earlier interpretations remain historical records where they are required to
reconstruct the path of the investigation.
The supplied journal package contains two versions of Q009 describing the same Q, date,
question and scientific result. The more structured later copy is retained here as the
published Q009 record; the earlier editorial duplicate is not reproduced a second time.
No standalone Q010 journal was present in the supplied journal package. Its absence is
recorded explicitly at its chronological position rather than reconstructed from later
knowledge.

BUBBLEVERSE Q JOURNALS
0.42
Q001
BUBBLEVERSE — Q-JOURNAL
Q-ID: Q001 Status: CONFIRMED JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION RECONSTRUCTED ON: 2026-09-08
Question:
What observational facts about the universe are robustly established, distinct from model-
dependent interpretation?
STARTING STATE
No prior Bubbleverse model. Q001 establishes the empirical baseline.
Core rule: observation ≠ measurement ≠ reconstruction ≠ inference ≠ interpretation.
HYPOTHESES
Supported:
The observable universe is structured, evolving, expanding, and was hotter/denser in
the past.
Rejected:
ΛCDM is directly observed.
A specific dark-matter particle is established.
Dark energy is directly detected.
A hot early universe proves a (t=0) singularity.
METHOD & EVIDENCE
Primary-source review and epistemic classification.
Main evidence:
CMB: Fixsen, Planck, ACT
Expansion/BAO: DESI
Supernovae/H₀: Riess, Perlmutter, Pantheon+, SH0ES
Lensing/dark matter: Planck lensing, Bullet Cluster
Early universe: primordial deuterium
Gravitational waves: GW150914, GW170817
No numerical Bubbleverse program or workflow was required.
KEY RESULT
Robust observations establish a dynamic, expanding universe with a hotter, denser past.
Dark-matter microphysics, dark-energy nature, and several cosmological parameters
remain model-dependent or unresolved.
Contradiction retained: Hubble-tension inference chains disagree.

BUBBLEVERSE Q JOURNALS
0.42
NEGATIVE RESULTS / MIKAMI
Killed claims:
“ΛCDM is observed.”
“Dark matter particle detected.”
“Dark energy substance detected.”
“Hot Big Bang proves singularity.”
MODEL CHANGE
Before: No Bubbleverse baseline.
After: Observation-first cosmological framework established.
Change: Foundational model created.
GITHUB / PROVENANCE
Repository / commits / workflows: NOT RECORDED AT TIME OF Q
Programs: None.
Provenance reconstructed from Q001 outputs, manuscript material, handoff context, and
cited primary literature.
REPRODUCIBILITY
Recheck the listed primary sources, classify every claim by epistemic level, verify key
numerical values, preserve dataset dependencies, and apply the same acceptance criteria.
CONCLUSION
Q001 establishes Bubbleverse’s empirical foundation and permanent rule:
Never silently promote interpretation into observation.
NEXT-Q HANDOFF
Next Q: Q002
Reason:
Cosmic expansion now requires separate analysis of what is directly observed versus
model-inferred.
Next question:
What observations establish cosmic expansion, and which parts of the inferred expansion
history depend on cosmological modelling?
FINAL ANSWER: Empirical baseline established.
MIKAMI: Four overstrong claims rejected.
MODEL CHANGE: Observation-first framework created.
GITHUB: Historical provenance not recorded.
NEXT: Q002 — cosmic expansion.

BUBBLEVERSE Q JOURNALS
0.42
Q002
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q002
Date/time: 2026-08-26 20:31 CEST
Status: CONFIRMED
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
Question:
What do observations show about cosmic expansion, and which conclusions depend on
cosmological models?
2. STARTING STATE
Model entering Q: Q001 observational baseline.
Inherited:
Observation must be separated from calibration, reconstruction and interpretation.
Constraint:
Do not equate redshift, (H(z)), (H 0), scale factor or acceleration.
3. HYPOTHESES
Tested:
H1: Multiple probes support expansion.
H2: Redshift alone proves expansion.
H3: Simple tired-light/static models remain viable.
Rejected:
H2 — redshift alone is insufficient.
H3 — simple no-time-dilation models conflict with SN time dilation.
Surviving:
H1 — CONFIRMED.
4. METHOD & EVIDENCE
Methods:
Literature comparison, cross-probe consistency and observation/inference audit.
Evidence:
Hubble 1929; Riess/Perlmutter; Pantheon+; Goldhaber/Blondin SN time dilation;
BAO/eBOSS/DESI; Moresco chronometers; GW170817 standard siren; CMB (T(z)).
Programs/workflows:
None verified or required.

BUBBLEVERSE Q JOURNALS
0.42
Tests:
Redshift-distance consistency, SN time dilation, BAO, chronometers, standard sirens, simple
tired-light falsification.
5. KEY RESULTS
1+z= a(t0)
, H= ˙a
a(tem)
a
Redshift is observed; (a(t)), (H(z)), (H 0) and acceleration are inferred.
Final result:
Cosmic expansion is CONFIRMED by multiple consistent probes. Late acceleration is
strongly supported but does not prove ( Λ ) or dark energy.
Limitations:
Calibration, (rd), stellar modelling, peculiar velocities and geometric assumptions.
Contradiction:
“We directly observe space expanding” is too strong.
6. NEGATIVE RESULTS / MIKAMI
Killed:
- Redshift alone proves expansion.
- (H(z)) is directly observed.
- BAO gives absolute (H(z)) without (rd).
- Acceleration proves ( Λ ).
- Simple no-time-dilation tired light.
No computational failures recorded.
7. MODEL CHANGE
Before: Expansion evidence present.
After: Expansion = CONFIRMED; acceleration = strongly supported; mechanism = OPEN.
Change: Epistemic model strengthened.
8. GITHUB / PROVENANCE
Repository/commits/workflows/programs/artifacts:
NOT RECORDED AT TIME OF Q.
Provenance:
Reconstructed from surviving Q material, manuscript state and primary literature. No
identifiers invented.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
Re-check the cited probes, separate observations from inferred quantities, and test whether
the complete evidence set is consistent with expansion and incompatible with simple no-
time-dilation alternatives.
10. CONCLUSION
The observable Universe is very strongly consistent with an expanding large-scale
geometry. The exact expansion history and cause of acceleration remain more model-
dependent.
11. NEXT-Q HANDOFF
Next Q: Q003
Reason:
Determine exactly what (H 0) is and how different observational chains infer it.
FINAL ANSWER: Expansion CONFIRMED.
Q-JOURNAL: This journal.
MIKAMI: Redshift-only, direct-(H(z)), assumption-free BAO, acceleration=( Λ ), simple tired
light rejected.
MODEL CHANGE: Expansion promoted to CONFIRMED.
GITHUB: NOT RECORDED AT TIME OF Q.
NEXT-Q: Q003 — compare (H 0) inference chains.

BUBBLEVERSE Q JOURNALS
0.42
Q003
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q003
Date/time: 2026-08-26 23:55 CEST
Status: CONFIRMED / SUPPORTED
Question: What is (H 0), how is it inferred, and where do calibration and model dependence
enter?
2. STARTING STATE
Model entering Q: Early Bubbleverse Hubble-tension framework.
Inherited:
- Q001: observation ≠ inference.
- Q002: expansion is robust; redshift ≠ (H 0).
3. HYPOTHESES
Rejected:
- (H 0) is directly observed.
- CMB/local/BAO estimates are equivalent or fully independent.
Surviving:
Different methods provide partially independent inference routes.
4. METHOD & EVIDENCE
Method: Map each route from observable calibration/model → →(H 0).
Sources: K-002, K-014, K-019, K-024–K-030.
Programs/workflows: NOT RECORDED AT TIME OF Q.
5. KEY RESULTS
a)t0
H 0= ˙a
Key benchmarks:
- H0DN: (73.50±0.81)
- CMB-SPA, flat ΛCDM: (67.24±0.35)
- DESI DR2+BBN, flat ΛCDM: (68.51±0.58)
H0DN vs CMB-SPA: ~(7.1σ ).
H0DN vs DESI+BBN: ~(5σ ).

BUBBLEVERSE Q JOURNALS
0.42
Final result: (H 0) is an inferred parameter, not a raw observable. The tension is between
different inference chains.
Limitations: No joint likelihood/covariance reconstruction.
6. NEGATIVE RESULTS / MIKAMI
Killed:
- “(H 0) is directly measured.”
- “BAO gives model-free absolute (H 0).”
- “7.1σ tension = 7.1σ evidence for new physics.”
7. MODEL CHANGE
Before: Planck vs SH0ES shorthand.
After: Multi-chain structure using H0DN, CMB-SPA, DESI+BBN and alternative probes.
Change: MODIFIED / STRENGTHENED.
8. GITHUB / PROVENANCE
Repository/commits/workflows/results: NOT RECORDED AT TIME OF Q.
Provenance: Reconstructed from Q003 result, source register and handoff material.
9. REPRODUCIBILITY
Verify listed sources, reconstruct each inference chain, map shared dependencies, and
compare benchmarks without double counting.
10. CONCLUSION
Q003 established that the Hubble tension is a conflict among distinct inference chains for
the same parameter. Its cause remained unresolved; no new physics was established.
11. NEXT-Q HANDOFF
Next Q: Q004
Question: Is the (H 0) tension robust after known systematics, calibration dependencies,
model assumptions and independent probes are treated together?

BUBBLEVERSE Q JOURNALS
0.42
Q004
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 19:17 CEST
1. IDENTITY
Q-ID: Q004
Original date/time: NOT RECORDED
Status: SUPPORTED
Question:
Is the difference between the main H₀ inferences robust when known systematics,
calibration dependencies, model assumptions, and independent methods are considered
together?
2. STARTING STATE
Model entering Q: Bubbleverse H₀ evidence structure after CASE-003.
Inherited:
- H0DN: 73.50 ± 0.81 km s⁻¹ Mpc⁻¹.
- CMB-SPA, flat ΛCDM: 67.24 ± 0.35.
- DESI DR2 + BBN: 68.51 ± 0.58.
Constraint: H₀ is an inferred parameter, not a raw observable; overlapping evidence must
not be double-counted.
3. HYPOTHESES
Tested:
H1: Main H₀ tension survives known systematics.
H2: One dominant local systematic explains it.
H3: One CMB/Planck-specific systematic explains it.
Rejected as sufficient single causes: HST Cepheid crowding alone; Planck pipeline alone;
SN-Ia rung alone.
Surviving: residual local/systematic combinations, peculiar velocities/selection, stellar
calibration, early-/late-Universe model dependence, sound-horizon physics, multi-effect
explanations.
4. METHOD & EVIDENCE
Compared covariance/dependence structure and cross-checks across local distance, CMB,
BAO+BBN, TRGB/JAGB, megamasers, strong lenses, and standard sirens.
Primary sources: K-024–K-032; supporting K-002, K-014, K-019.
Programs/workflows: NOT RECORDED AT TIME OF Q.

BUBBLEVERSE Q JOURNALS
0.42
Numerical tests: simple Gaussian tension calculations and cross-method consistency
assessment.
5. KEY RESULTS
- H0DN vs CMB-SPA: ΔH₀ = 6.26 ± 0.88, 7.1σ. ≈
- H0DN vs DESI DR2 + BBN: 5.0σ. ≈
- CCHP JWST-only TRGB/JAGB differences from H0DN are only 2σ before shared ≈
covariance and are not independent.
- Independent megamaser/lensing/GW routes remain too imprecise to adjudicate alone.
Final result:
The H₀ discrepancy is a robust Type-C parameter tension, Level 3, but its cause is not
established.
Limitations: no ~1% fully independent third H₀ route; residual local calibration structure
remains.
Contradictions: C-001 persists; C-002 reduced to internal late-Universe methodological
tension.
6. NEGATIVE RESULTS / MIKAMI
Killed as full explanations:
- HST Cepheid crowding alone.
- Planck-specific pipeline alone.
- SN-Ia final rung alone.
Reason: independent/cross-pipeline evidence retains substantial high-versus-low H₀
disagreement.
7. MODEL CHANGE
Before: H₀ discrepancy active but robustness not yet fully established.
After: C-001 = ROBUST ANOMALY / TYPE C / LEVEL 3. C-002 = internal methodological
tension.
Change: promoted C-001; constrained C-002 and several explanations.
Reason: multi-method robustness and systematic cross-checks.
8. GITHUB / PROVENANCE
Repository: UNKNOWN / NOT RECORDED
Commits/workflows/programs/artifacts: NOT RECORDED AT TIME OF Q.
Provenance: reconstructed from surviving Q004 result, Motor-14 revision, manuscript
integration material, and cited source Ids.
9. REPRODUCIBILITY

BUBBLEVERSE Q JOURNALS
0.42
To reproduce: recover cited primary sources; reconstruct H ₀ benchmark comparisons;
preserve stated model assumptions and evidence overlaps; reproduce Gaussian tension
estimates; apply the same independence/systematics criteria.
Missing historical software/Git metadata: NOT RECORDED AT TIME OF Q.
10. CONCLUSION
The Hubble tension survives serious treatment of the major known calibration, covariance,
model, and cross-method issues. It is strong enough to require explanation, but not to
establish new physics.
11. NEXT-Q HANDOFF
Why: the anomaly is established; the remaining problem is discrimination among
explanations.
Next Q: Q005
Next question:
Which remaining systematic and cosmological explanation classes can quantitatively
reduce the robust H₀ tension while remaining consistent with H0DN, CMB-SPA, DESI DR2 +
BBN, internal late-Universe calibration structure, and physically independent H ₀ routes?
REQUIRED END-OF-Q OUTPUT
1. FINAL ANSWER: Robust H₀ parameter tension confirmed at Level 3; cause unresolved.
2. Q-JOURNAL: This retrospective reconstruction.
3. MIKAMI GRAVEYARD UPDATE: crowding-only, Planck-only, and SN-rung-only
explanations killed as sufficient full causes.
4. MODEL CHANGE SUMMARY: C-001 promoted; C-002 constrained.
5. REPRODUCIBILITY / GITHUB REFERENCES: sources preserved; GitHub metadata not
recorded.
6. NEXT-Q HANDOFF: Q005 — discriminate surviving explanation classes.

BUBBLEVERSE Q JOURNALS
0.42
Q005
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q005
Date/time: 2026-08-29 23:40 CEST
Status: SUPPORTED
Question: Hvilke af de resterende systematiske og kosmologiske forklaringsklasser kan
kvantitativt reducere den robuste H0-spænding, samtidig med at de forbliver forenelige
med H0DN, CMB-SPA, DESI DR2 + BBN, den interne late-Universe calibration structure og
de fysisk alternative H0-routes?
2. STARTING STATE
Model entering Q: Robust H0-anomali, Type C / Level 3; årsag ukendt.
Inherited: H0DN 73.50±0.81; CMB-SPA 67.24±0.35 (~7.1σ); DESI DR2+BBN 68.51±0.58.
Constraints: H0 71.5 cosmology-screen; systematik, calibration og alternative H0-ruter ≥
skal respekteres; common-backend ≠ paper-native reproduction.
3. HYPOTHESES
Tested:
H1: Late-Universe systematik kan forklare spændingen.
H2: EDE/recombination physics kan hæve H0.
H3: Andre udvidelser (N e f f ,l at e−D E , I D E , P M F ,a xiod il at on) kan give fuld løsning.
Rejected: Ordinary peculiar velocities/standard cosmic variance som fuld løsning. Generic
late-DE, N_eff-only m.fl. stærkt svækket som fulde løsninger.
Surviving: n=3 EDE = partial; varying-m_e = stærkeste common-backend partial kandidat;
IDE/systematik = partial.
4. METHOD & EVIDENCE
Methods: Litteratursyntese + fælles likelihood-backend + multi-start optimering +
deterministic basin/globality recovery.
Primary sources: K-024, K-029, K-030, K-033–K-044; især K-036 (n=3 EDE) og K-038
(n=2 E D E/v ar y in g−me).
Programs/workflows: ”q005_hpc_v14.py”; ”q005_globality_recovery_v14.py”;
”.github/workflows/q005-hpc-v14.yml”; ”.github/workflows/q005-hpc-v14-globality-
recovery.yml”.
Tests: H0 71.5 gate; Δχ²/AIC; restart/globality; deterministic basin recovery. ≥

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
- n=3 high-EDE basin: H0=70.8533, f_EDE=0.0811, χ²=548.010; kun Δχ² 0.112 fra low-fEDE ≈
basin, men under H0-gaten.
- n=2: tidligere χ² 1840–1847 var optimizer trapping; recovered low-fEDE basin ≈
H0=68.4924, χ²=548.196.
- varying-m_e: bedste recovered H0=70.1572, Δχ² 2.59, ΔAIC 0.59; globality stadig ≈− ≈−
unresolved.
Final result: Ingen testet forklaringsklasse er etableret som robust fuld H0-løsning; flere
giver kun partielle forbedringer.
Limitations: Exact global model ranking unresolved; K-036/K-038 native executable
provenance mangler.
Contradictions: H0DN vs CMB-SPA og DESI-side spænding består.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: Ordinary V14 restarts fandt ustabile minima; n=2 katastrofebasin var
numerisk forkert basin, ikke model-falsifikation.
Graveyard: Ordinary peculiar velocities/cosmic variance som fuld løsning; generic late-
DE/N_eff-only som førende fuld løsning; fysisk fortolkning af n=2 χ² 1847. ≈
7. MODEL CHANGE
Before: Flere systematiske/kosmologiske klasser åbne; n=2 numerisk patologisk.
After: Ingen fuld løsning; n=3 og varying-m_e beholdes som partial; n=2 reklassificeret low-
fEDE/ΛCDM-like.
Change: Modelrummet indsnævret og numerisk fortolkning korrigeret.
Reason: Q005 litteratur + V14 runs + deterministic recovery.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commits: ”b875ea95d9b6390b8f03dac729eb7f5fe84d3118”; recovery
”7293c7f5db4d7ab72b1aaad38fe15f2639e11d5e”
Runs: #24 ”33249784822”; #25 ”33252632548”; recovery ”33271326245”
Result: ”q005_v14_globality_recovery_result.json”
Provenance note: Frozen common backend; recovery parent metadata referenced older
run21, preserved as limitation.
9. REPRODUCIBILITY
Checkout recorded commits obtain frozen likelihood/data run listed workflows/configs → →
compare JSON/artifacts apply same H0, Δχ²/AIC og globality gates. → →
10. CONCLUSION
H0-spændingen består. Ordinary systematics er utilstrækkelige som fuld forklaring. N=3
EDE og varying-m_e kan flytte H0 opad, men ingen testet kandidat når robust fuld

BUBBLEVERSE Q JOURNALS
0.42
reconciliation. Exact common-backend ranking forbliver numerisk usikker uden at ændre
hovedkonklusionen.
11. NEXT-Q HANDOFF
Why: Den vigtigste flaskehals er nu, hvilke likelihood/data-komponenter der stopper de
overlevende high-H0 mekanismer.
Next Q: Q006
Next question: Hvilke konkrete CMB-, DESI DR2- og
BBN-likelihood-komponenter/parameterkoblinger leverer den dominerende fitstraf, når
n=3 EDE og varying-m_e forsøger at nå H0 71.5? ≥
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Ingen testet klasse giver robust fuld løsning; n=3 EDE og varying-m_e
overlever som partial.
Q-JOURNAL: Ovenstående.
MIKAMI GRAVEYARD: Ordinary PV/cosmic variance som fuld løsning; n=2 katastrofebasin
som fysisk resultat.
MODEL CHANGE: Modelrummet indsnævret; n=2 korrigeret; varying-m_e styrket som
partial.
REPRODUCIBILITY: Morfindien/Bubbleverse; commits/runs/workflows ovenfor.
NEXT-Q: Q006 — identificér den dominerende likelihood-barriere for high-H0 modeller.

BUBBLEVERSE Q JOURNALS
0.42
Q006
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q006 Date/time: 2026-08-30 CEST Status: CONFIRMED
Question:
Hvilke konkrete datasæt, likelihood-komponenter og parameterkoblinger i de aktuelle CMB
+ DESI DR2 + BBN-inferenskæder leverer den dominerende fitstraf, når n=3 EDE og varying
electron mass forsøger at flytte H0 fra cirka 68–70 til området H0 71.5? ≥
2. STARTING STATE
Model entering Q: Frozen Q005 common backend; n=3 EDE and varying-mₑ
active/constrained candidates.
Inherited results:
Q005: ΛCDM H0=68.494422, χ²=547.482504.
Q005: n=3 EDE H0=70.853292; varying-mₑ H0=70.157184, χ²=544.887898.
Constraints: Fixed backend/data/priors/bounds/nuisance; H0 profiles at baseline, 71.5, 72.5,
73.5; components Planck low-ℓ, ACT DR6, DESI DR2, BBN.
3. HYPOTHESES
Tested:
H1: Same likelihood component dominates both mechanisms.
H2: n=3 EDE is primarily CMB/ACT limited.
H3: varying-mₑ transfers penalty toward DESI/BBN.
Rejected: H1 — component attribution differs by mechanism.
Surviving: H2 supported; H3 supported.
4. METHOD & EVIDENCE
Methods: Fixed-H0 profile optimization with non-overlapping χ² decomposition and
parameter tracking.
Primary sources: K-029, K-030, K-036, K-037, K-038, K-039.
Programs/workflows:
q006_likelihood_attribution_v1.py
q006_likelihood_attribution_v1_config.yml
.github/workflows/q006-likelihood-attribution-v1.yml
Tests: 8 required profiles; completeness, component-attribution and final-result gates.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
n=3 EDE:
H0=71.5: Δχ²=+2.032, ACT +2.133.
H0=72.5: Δχ²=+19.877, ACT +9.343, DESI +9.213.
H0=73.5: Δχ²=+10.972, ACT +8.960.
ACT dominates 3/3 profiles.
varying-mₑ:
H0=71.5: Δχ²=+6.811, DESI +3.394.
H0=72.5: Δχ²=+3.421, BBN +2.906.
H0=73.5: Δχ²=+4.752, BBN +2.842.
Final result: High-H0 barriers are mechanism-specific: EDE is primarily ACT-limited;
varying-mₑ is primarily DESI/BBN-limited.
Limitations: Common-backend, not exact K-036/K-038 reproduction; global minima not
proven. EDE Δχ² profile is non-monotonic and remains a preserved numerical irregularity.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: RUN #1 and #2 failed before optimization because rendered YAML
filenames became ...pyaml; technical failures, not physics failures.
Mikami Graveyard:
Killed route: “one universal high-H0 likelihood barrier.”
Reason: EDE and varying-mₑ show different dominant penalties.
7. MODEL CHANGE
Before: Surviving high-H0 candidates treated broadly as facing a generic cosmological
barrier.
After: Model-specific constraint topology.
Change: MODIFIED / CONSTRAINED.
Reason: Q006 likelihood decomposition.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commits: RUN #1 15d60435d6199e71662448fce6a1e8506fc1eac7; RUN #2
85ff40dae59be88636d7542de00025fed1f68449; successful-run commit NOT RECORDED.
Runs: 33278320823; 33278861896; successful run ID NOT RECORDED.
Artifact: q006_likelihood_attribution_v1_result.json
Artifact SHA-256: b7ac0f72aadb01be7739560c38faff03ee082c4697fa7c6cdd101e209acf7477
9. REPRODUCIBILITY
Checkout recorded version; obtain frozen Q005 inputs; run Q006 workflow at specified H0
grid; verify component χ² outputs and PASS gates; compare against recorded result JSON.
Missing successful-run commit/run ID: NOT RECORDED.

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q006 established that reducing the sound horizon does not encounter one universal
observational barrier. n=3 EDE primarily accumulates ACT DR6 penalty, whereas varying-
mₑ shifts the dominant cost toward DESI DR2 and BBN. Neither mechanism is globally
falsified.
11. NEXT-Q HANDOFF
Why another Q is required: Q006 located the penalties but did not identify which physical
ACT observables/degeneracies create the EDE barrier.
Next Q: Q007
Next question:
Hvilke konkrete fysiske observables og parameterdegeneracies i ACT DR6 gør n=3 EDE dyr
ved H0 71.5, og hvorfor kan varying electron mass undgå den samme ACT-straf, mens ≥
dens fit cost i stedet flyttes mod DESI DR2 og BBN?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: EDE primarily ACT DR6 barrier; varying-mₑ DESI/BBN barrier. → →
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Universal common high-H0 barrier rejected.
MODEL CHANGE SUMMARY: Generic barrier mechanism-specific constraint topology. →
REPRODUCIBILITY / GITHUB REFERENCES: Morfindien/Bubbleverse; Q006
script/config/workflow; failed-run commits above; successful result JSON/hash preserved.
NEXT-Q HANDOFF: Q007 — determine the physical observables and degeneracies
producing the different barrier structures.

BUBBLEVERSE Q JOURNALS
0.42
Q007
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q007
Date/time: 2026-08-30 11:42 CEST
Status: SUPPORTED
Question: Which concrete physical observables and parameter degeneracies in ACT DR6
make n=3 EDE costly at H 0≥71.5, and why can varying electron mass avoid the same ACT
penalty while shifting fit cost toward DESI DR2 and BBN?
2. STARTING STATE
Model entering Q: Frozen Q005/Q006 common backend; n=3 EDE + varying-me; global
minima not established.
Inherited: Q006 found ACT dominant for high-H 0 EDE; varying-me cost shifted mainly to
DESI/BBN. Q006 EDE profile was non-monotonic.
Constraints: No reoptimization; preserve exact Q006 points/covariance; no independent
TT/TE/EE claim; negative signed contributions allowed.
3. HYPOTHESES
Tested:
H1: One ACT spectrum/region dominates EDE penalty.
H2: Penalty is distributed across correlated spectral structure.
H3: varying-me avoids EDE-like ACT penalty through different recombination degeneracy.
Rejected: Single isolated ACT observable as complete explanation.
Surviving: H2 + H3 — supported; TE/intermediate-ℓ concentration within distributed
covariance-coupled penalty.
4. METHOD & EVIDENCE
Methods: Exact covariance attribution ci=di (C
−1d )i; grouped TT/TE/EE and descriptive
multipole bands; EDE vs varying-me control.
Sources: K-036 Poulin et al. arXiv:2505.08051; K-037 ACT DR6 extended models
arXiv:2503.14454; K-038 Toda & Seto, JCAP 02 (2026) 019, arXiv:2508.09025; K-045 Seto &
Toda arXiv:2206.13209.
Programs/workflows: ”q007_act_observable_attribution_v2.py”; ”q007-act-observable-
attribution-v2.yml”; frozen ACT DR6-lite commit ”0e0cd2c…”.
Tests: 8/8 frozen profiles; covariance closure; completeness; interpretation/final gates.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
EDE Δχ²_ACT: 71.5: +2.135; 72.5: +9.348; 73.5: +8.966.
TE attribution: +1.667, +5.914, +6.765 respectively — largest positive spectrum contribution
at all three points.
Varying-me Δχ²_ACT: 71.5: +1.042; 72.5: 0.227; 73.5: +0.100. −
Final result: High-H 0 EDE pays a distributed ACT spectral penalty concentrated in
TE/intermediate-ℓ; varying-me largely avoids this ACT cost and transfers constraint
pressure toward DESI/BBN.
Limitations: No global-minimum proof; ACT_LOW/MID/HIGH are descriptive; Q006 non-
monotonic EDE profile remains unresolved.
Contradiction: None fundamental; numerical profile irregularity preserved.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: Early V1 runs failed because fixed H 0 was incorrectly required from
serialized ”bestfit”; later ACT-data download timeout. Both technical, not physical failures.
Mikami Graveyard additions:
- “EE alone dominates the ACT EDE penalty” — rejected.
- “Sound-horizon reduction alone is sufficient” — rejected.
- “All early-Universe solutions face the same barrier” — rejected as too crude.
7. MODEL CHANGE
Before: Generic early-Universe/CMB barrier.
After: Model-specific constraint-transfer topology.
Change: MODIFIED / PROMOTED.
Reason: EDE and varying-me reach similar high H 0/rd r a g through sharply different
likelihood-penalty structures.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commits: Successful Q007 execution commit NOT RECORDED; frozen ACT
”0e0cd2c703c62a0e980470b572602233b27750e1”; CLASS_EDE
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Workflow: ”q007-act-observable-attribution-v2.yml”
Program: ”q007_act_observable_attribution_v2.py”
Output: ”q007_act_observable_attribution_v1_result.json”
Provenance: Exact Q006 fixed-H 0 points, no reoptimization; 8/8 complete;
closure/completeness/final gates PASS.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
Checkout frozen versions obtain Q006 aggregate + ACT DR6-lite run Q007 V2 on eight → →
TC
fixed profiles verify → ∑ci=d
−1d and 8/8 completion compare result JSON and apply →
recorded gates.
10. CONCLUSION
Q007 supports a model-specific constraint-transfer picture: n=3 EDE distorts CMB spectral
structure enough to incur a strong ACT penalty, especially through TE, whereas varying-me
preserves ACT compatibility more effectively but shifts the cost toward DESI/BBN. This
does not establish either model as a complete Hubble-tension solution.
11. NEXT-Q HANDOFF
Why: The EDE fixed-H 0 profile remains strongly non-monotonic and globality is
undocumented.
Next Q: Q008
Question: Is the Q006 non-monotonic n=3 EDE profile an optimizer/basin/global-
minimization artefact, or a reproducible property of the frozen likelihood?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: EDE has a distributed ACT spectral penalty dominated positively by TE;
varying-me largely avoids it and transfers cost toward DESI/BBN.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Generic universal barrier, sound-horizon-only sufficiency,
and EE-dominance rejected.
MODEL CHANGE SUMMARY: Generic barrier model-specific constraint-transfer topology. →
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; Q007 V2 workflow/program;
frozen ACT/CLASS commits; successful run commit not recorded.
NEXT-Q HANDOFF: Q008 — determine whether the non-monotonic EDE profile is
numerical/globality artefact or real frozen-likelihood structure.

BUBBLEVERSE Q JOURNALS
0.42
Q008
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q008
Date/time: 2026-08-30 / exact completion time NOT RECORDED
Status: SUPPORTED
Question: Is the non-monotonic Q006 (n=3) EDE fixed-(H 0) profile primarily
optimizer/basin/incomplete-minimization structure, or a reproducible property of the
frozen common-backend likelihood?
2. STARTING STATE
Model entering Q: Q005 V14 frozen common backend; (n=3) EDE active/constrained, not
established new physics.
Inherited: Q006 profile ( Δ χ
2=(+2.03,+19.88,+10.97)) at (H 0=(71.5,72.5,73.5)); Q007 ACT
attribution applied to those frozen points.
Constraints: Preserve backend, priors, historical points and fixed-(H 0) targets; BEST
OBSERVED ≠ GLOBAL MINIMUM.
3. HYPOTHESES
Tested:
H1 optimizer/suboptimal basin; H2 incomplete minimization; H3 reproducible multimodal
likelihood; H4 new physical structure.
Rejected: Strong H3 and H4 as explanations of the original (+19.88) peak.
Surviving: H1 strongly supported; H2 supported; residual multi-basin/globality uncertainty
remains.
4. METHOD & EVIDENCE
Method: Four start families at (H 0=70.853292,71.5,72.5,73.5); BOBYQA Stage-1 plus
independent Stage-2 refinement; basin replication and boundary diagnostics.
Sources/evidence: Q005/Q006/Q007 internal results; K-036 Poulin et al.; ACT DR6 / DESI DR2
context.
Programs/workflows: ”q008_globality_validation_v1.py”;
”q008_globality_validation_v1_config.yml”; ”q008-globality-validation-v1.yml”.
Tests: completeness, valid-start quorum, refinement, basin replication, boundaries,
material profile change.
5. KEY RESULTS
Best observed ( χ
2):

BUBBLEVERSE Q JOURNALS
0.42
70.853292: 548.010401 (Q005 lower basin retained)
71.5: 547.154321
72.5: 548.854655
73.5: 549.105584
Relative best-known envelope: 0, 0.856, +0.844, +1.095. −
The old Q006 (H 0=72.5) value changed from +19.877 +0.844, demonstrating a material →
basin/minimization artifact.
Limitations: Global minima not established; basin replication unresolved at 70.85, 72.5 and
73.5; boundary warnings at several targets.
Contradiction: Q006’s apparent sharp non-monotonic barrier was not numerically robust.
6. NEGATIVE RESULTS / MIKAMI
Failed route: Treating the Q006 (+19.88) peak as robust likelihood structure.
Mikami Graveyard:
Killed: Strong physical interpretation of the original Q006 non-monotonic peak.
Reason: Same frozen backend produced dramatically lower valid solutions.
7. MODEL CHANGE
Before: Q006 profile active; Q007 attribution interpreted on those points.
After: Q006 points superseded as active best-observed profile; preserved historically. Q007
remains valid only for its original points.
Change: MODIFIED / CONSTRAINED.
Reason: Multi-start/refinement recovered materially lower minima.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commit(s): NOT RECORDED / NOT VERIFIED
Workflow: ”q008-globality-validation-v1.yml”
Programs: ”q008_globality_validation_v1.py”
Result: ”q008_globality_validation_v1_result.json”
Run ID: ”Q008-EDE-GLOBALITY-VALIDATION-V1”
Provenance: Frozen Q005 V14 backend; Q006 historical points retained; Q008 generated
new best-observed basin searches and refinements.
9. REPRODUCIBILITY
Checkout recorded version; obtain frozen Q005 backend/config; run Q008 workflow at
recorded fixed (H 0) targets/start families; compare result JSON; apply the same refinement,
replication and material-change gates. Missing commit/run metadata: NOT RECORDED /
NOT VERIFIED.

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q008 established that the original Q006 (n=3) EDE non-monotonic profile—especially the
(+19.88) penalty at (H 0=72.5)—was not robust. Optimizer basin structure/incomplete
minimization materially produced the apparent barrier. The corrected values are best
observed, not documented global minima.
11. NEXT-Q HANDOFF
Why: Q007’s ACT TT/TE/EE attribution was evaluated at superseded Q006 basins.
Next Q: Q009
Question: At the corrected best-observed (n=3) EDE fixed-(H 0) minima, which ACT DR6
TT/TE/EE and multipole regions dominate the residual likelihood cost, and does Q007’s
TE/intermediate-(ℓ) attribution survive?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Original Q006 non-monotonic profile was materially optimizer/basin-
driven; no global-minimum claim.
Q-JOURNAL: This reconstruction.
MIKAMI GRAVEYARD UPDATE: Strong physical interpretation of Q006 (+19.88) peak killed.
MODEL CHANGE SUMMARY: Q006 active profile superseded; Q007 retained only for
historical points.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; Q008
program/config/workflow/result listed above; missing commit metadata not invented.
NEXT-Q HANDOFF: Q009 — repeat observable attribution at corrected best-observed
minima.

BUBBLEVERSE Q JOURNALS
0.42
Q009
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q009
Date/time: 2026-08-30 CEST
Status: CONFIRMED
Question: At the corrected best-observed n=3 EDE fixed-H0 minima, which ACT DR6
TT/TE/EE observables and multipole regions dominate residual likelihood cost, and does
Q007’s TE/intermediate-ℓ attribution persist?
2. STARTING STATE
Model entering Q: n=3 EDE; Q005 V14 frozen common backend; Q008 best-observed basins;
globality unresolved.
Inherited: Q007 found TE/ACT_MID dominance at old Q006 basins. Q008 superseded those
minima with χ² = 547.154321, 548.854655, 549.105584 at H0 = 71.5, 72.5, 73.5.
Constraint: Preserve Q005 baseline H0=70.853292, χ²=548.010401; no reoptimization/new
priors/data/bounds.
3. HYPOTHESES
H1: TE/ACT_MID topology persists.
H2: Attribution changes at corrected basins.
H3: Change is target/basin dependent.
Rejected: H1 — failed at all three targets.
Surviving: H2/H3 — supported.
4. METHOD & EVIDENCE
Fixed-point ACT DR6-lite reevaluation using full covariance:
−1d )i,∑
Ci=di(C
ci= χ
2.
i
Bands: LOW 600–1499.999; MID 1500–2999.999; HIGH 3000–8500.
Evidence: INTERNAL-Q005, Q007, Q008, Q009; ACT DR6-lite commit
”0e0cd2c703c62a0e980470b572602233b27750e1”.
Final program: ”q009_act_corrected_minima_attribution_v8.py”
Workflow: Bubbleverse Q009 ACT Corrected Minima Attribution V8.
5. KEY RESULTS
H0=71.5: Δχ²_ACT = 2.5540; dominant TT / ACT_LOW. −
H0=72.5: Δχ²_ACT = +0.8768; dominant TT / ACT_LOW.

BUBBLEVERSE Q JOURNALS
0.42
H0=73.5: Δχ²_ACT = +0.1088; dominant EE / ACT_MID.
Historical Q007: TE / ACT_MID at all three.
Final result: Q007’s TE/intermediate-ℓ topology does not persist at corrected Q008 basins;
ACT attribution is basin dependent.
Limitation: Q008 GLOBALITY_GATE remains UNRESOLVED; results apply to best-observed,
not proven-global minima.
Contradictions: None fundamental; Q007 remains valid for its original basins.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1–V7 failed technically through parent-schema, stale-file, expired-artifact,
baseline-provenance and ”bestfit”/”fixed_sampled_parameters” integration errors. No
scientific failure implied.
Mikami Graveyard:
- Basin-independent TE/ACT_MID high-H0 EDE barrier — KILLED.
- Q006 high-H0 minima as active best minima — SUPERSEDED by Q008.
7. MODEL CHANGE
Before: High-H0 n=3 EDE appeared associated with TE/intermediate-ℓ ACT penalty.
After: That topology is historical/basin-conditional; corrected basins show strongly
reorganized and much smaller ACT cost.
Change: MODIFIED / CONSTRAINED.
Reason: Q009 V8 fixed-point attribution.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Inspection commit: ”a8d11cc9687e5df757f4794224d83ed34df03846”
Program: ”q009_act_corrected_minima_attribution_v8.py”
Config: ”q009_act_corrected_minima_attribution_v8_config.yml”
Workflow: ”q009-act-corrected-minima-attribution-v8.yml”
Run ID: ”Q009-ACT-CORRECTED-MINIMA-ATTRIBUTION-V8”
GitHub execution run ID: NOT RECORDED
Result: ”q009_act_corrected_minima_attribution_v8_result.json”
9. REPRODUCIBILITY
Checkout recorded versions obtain Q005/Q007/Q008 preserved inputs run V8 → →
workflow at H0=71.5/72.5/73.5 verify covariance closure and outputs compare → →
dominant spectrum/band against historical Q007.
10. CONCLUSION
The previously inferred TE/intermediate-ℓ ACT barrier was not robust to improved basin
selection. At the corrected best-observed EDE points, both the magnitude and location of

BUBBLEVERSE Q JOURNALS
0.42
ACT likelihood cost change substantially. This does not establish EDE as a solution because
globality remains unresolved.
11. NEXT-Q HANDOFF
Why: With the old ACT barrier removed, the remaining total high-H0 likelihood cost must
be localized.
Next Q: Q010
Question: At the corrected best-observed n=3 EDE fixed-H0 basins, which non-ACT
likelihood components and parameter trade-offs dominate the change in total scientific χ²
relative to the Q005 baseline?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Q007 TE/intermediate-ℓ topology does not persist; corrected ACT
attribution is basin dependent.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Basin-independent TE/ACT_MID barrier killed.
MODEL CHANGE SUMMARY: Q007 interpretation narrowed to historical basins.
REPRODUCIBILITY / GITHUB: V8 files/workflow and commits above.
NEXT-Q HANDOFF: Q010 — locate the remaining likelihood cost.

BUBBLEVERSE Q JOURNALS
0.42
Q010
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-09
1. IDENTITY
Q-ID: Q010
Date/time: 2026-08-30 CEST
Status: CONFIRMED
Question: At the corrected Q008 best-observed n=3 EDE fixed-H0 basins, which non-ACT
likelihood components and parameter trade-offs dominate the change in total scientific χ²
relative to Q005 baseline, and where does the remaining high-H0 cost move when Q007’s
ACT barrier does not persist?
2. STARTING STATE
Model entering Q: n=3 EDE; frozen Q005 V14 backend; Q008 best-observed basins; Q009
corrected ACT attribution.
Inherited:
- Q005 baseline: H0=70.853292, χ²=548.010401.
- Q008: χ²=547.154321, 548.854655, 549.105584 at H0=71.5, 72.5, 73.5.
- Q009: ACT cost strongly reorganized; no universal TE/ACT_MID barrier.
Constraint: Fixed-point attribution only; no reoptimization/new data/priors.
GLOBALITY_GATE remains UNRESOLVED.
3. HYPOTHESES
H1: One non-ACT likelihood replaces ACT as universal high-H0 barrier.
H2: Cost is distributed across likelihoods.
H3: Cost depends on basin and parameter trade-offs.
Rejected: H1 — no single replacement component persists.
Surviving: H2/H3 — confirmed within tested fixed points.
4. METHOD & EVIDENCE
Method: Re-evaluate serialized Q008 vectors on frozen Planck low-ℓ + ACT DR6 + DESI DR2
+ BBN likelihood; compare component deltas and parameter shifts.
Evidence: INTERNAL-Q005, Q007, Q008, Q009, Q010-V3.
Programs/workflows:
”q010_nonact_likelihood_attribution_v3.py”
”q010_nonact_likelihood_attribution_v3_config.yml”
”q010-nonact-likelihood-attribution-v3.yml”

BUBBLEVERSE Q JOURNALS
0.42
Tests: Q007 ACT-baseline cross-check; Q009 ACT-delta cross-check; component closure;
finite-result/final-result gates.
5. KEY RESULTS
Serialized attribution baseline: Planck 390.5709; ACT 159.1372; DESI 11.0431; BBN
11.7761; total 548.9751. Optimizer-native Q005 total remains 548.010401; +0.9647 −
roundtrip difference is diagnostic only.
H0=71.5: Planck +1.1417; ACT 2.5540; DESI 0.6380; BBN +0.3475; non-ACT +0.8512. − −
H0=72.5: Planck 0.5307; ACT +0.8768; DESI 0.4580; BBN +0.1231; non-ACT 0.8656. − − −
H0=73.5: Planck +0.1830; ACT +0.1088; DESI 0.5420; BBN +0.5011; non-ACT +0.1421. −
Major parameter reorganization with increasing H0: fEDE, n_s, omega_cdm, thetai_scf,
log10z_c, logA.
Final result: The old ACT barrier is not replaced by one universal non-ACT barrier; high-H0
constraint geometry is distributed, basin-dependent, and tied to multidimensional
parameter trade-offs.
Limitations: Q008 points are best-observed, not proven global minima; external viability
not tested.
Contradictions: None fundamental.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts:
- V1: Q008 schema/H0 ingestion error.
- V2: invalid mandatory gate requiring serialized vectors to reproduce optimizer-native χ².
- V3: PASS.
Mikami Graveyard:
- “DESI becomes the universal replacement barrier” — KILLED.
- “One invariant likelihood component controls high-H0 EDE” — KILLED for tested basins.
7. MODEL CHANGE
Before: Q007 suggested a dominant ACT TE/intermediate-ℓ bottleneck.
After: Constraint cost is distributed and changes with basin/parameter trajectory.
Change: MODIFIED / CONSTRAINED.
Reason: Q009 + Q010-V3 component attribution.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit(s): NOT RECORDED IN FINAL HANDOFF
Workflow: ”q010-nonact-likelihood-attribution-v3.yml”
Program: ”q010_nonact_likelihood_attribution_v3.py”
Config: ”q010_nonact_likelihood_attribution_v3_config.yml”

BUBBLEVERSE Q JOURNALS
0.42
Run ID: ”Q010-NONACT-LIKELIHOOD-ATTRIBUTION-V3”
Result: ”q010_nonact_likelihood_attribution_v3_result.json”
Provenance: Q005 frozen backend + Q007 serialized baseline + Q008 corrected vectors +
Q009 ACT cross-checks V3 fixed-vector full-likelihood attribution. →
9. REPRODUCIBILITY
1. Checkout recorded repository version.
2. Obtain Q005/Q007/Q008/Q009 preserved inputs.
3. Run Q010 V3 workflow.
4. Verify ACT cross-checks, closure and final JSON.
5. Compare component deltas and parameter shifts using serialized attribution basis only.
10. CONCLUSION
No single likelihood inherits the high-H0 penalty after the historical ACT barrier
disappears. Planck dominates the positive non-ACT cost at 71.5, non-ACT improves the fit at
72.5, and BBN is the largest positive non-ACT term at 73.5, while DESI improves at all three
points. The relevant structure is therefore a basin-dependent multidimensional constraint
geometry.
11. NEXT-Q HANDOFF
Why another Q is required: The scientific importance of Q008–Q010 depends on whether
the corrected basins are robust/global representatives of the frozen likelihood.
Next Q: Q011
Next question: Are the corrected Q008 best-observed n=3 EDE fixed-H0 basins at H0=71.5,
72.5 and 73.5 global or sufficiently robust minima under the frozen Q005 V14 likelihood?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No universal replacement barrier exists; high-H0 cost is distributed and
basin/parameter dependent.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Universal DESI/replacement-barrier interpretation killed.
MODEL CHANGE SUMMARY: High-H0 EDE constraint picture changed from single-barrier
to multidimensional geometry.
REPRODUCIBILITY / GITHUB REFERENCES: Morfindien/Bubbleverse; Q010 V3
program/config/workflow/result above.
NEXT-Q HANDOFF: Q011 — resolve basin robustness/globality.

BUBBLEVERSE Q JOURNALS
0.42
Q011
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q011
Date/time: 2026-09-01 04:41 CEST
Status: CONSTRAINED
Question:
Do the corrected high-H 0 n=3 early-dark-energy basins at fixed
−1 M pc
−1 represent reproducible global or sufficiently certified
H 0=71.5,72.5,73.5 k m s
near-global minima of the frozen Bubbleverse likelihood surface, or is the shallow high-H 0
profile still an optimizer-basin artifact?
2. STARTING STATE
Model entering Q: n=3 EDE / ede_n3; Q005 V14 frozen backend; active but conditional.
Inherited:
- Q008 best-observed: χ
2=547.154321,548.854655,549.105584 at H 0=71.5,72.5,73.5.
- Q008 did not prove globality; optimizer-basin sensitivity remained unresolved.
Constraints: Same datasets, likelihoods, priors, bounds and model; no new
physics/configuration changes.
3. HYPOTHESES
Tested:
H1: Q008 minima are reproducible/global or strongly near-global.
H2: Lower competing basins remain.
H3: High-H 0 profile is materially optimizer-basin sensitive.
Rejected: H1 — certification criteria not achieved.
Surviving: H2/H3 — supported; materially lower basins found.
4. METHOD & EVIDENCE
Method: Finite multi-start optimization + refinement at four fixed-H 0 targets on frozen
Q005 V14 likelihood.
Evidence: INTERNAL-Q005; INTERNAL-Q008; R-Q011-EDE-GLOBALITY-CERTIFICATION-004.
Workflow/program:
Bubbleverse Q011 EDE Globality Certification V4; ”q011_ede_globality_certification_v4.py”.
Tests: Multi-start basin search; refinement; completeness/finite-result/globality-certification
gates.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
- H 0=71.5:547.154321→546.364260, Δ χ
2=−0.790061 materially superseded. →
- H 0=72.5:548.854655→548.624632, Δ=−0.230023.
- H 0=73.5:549.105584→548.766646, Δ=−0.338938.
- H 0=70.853292: search reached χ
2=546.679939.
Final result: High-H 0 minima are BEST-OBSERVED MINIMUM ONLY; globality and strong
near-global certification were not established.
Limitations: Finite optimization cannot prove mathematical globality; same underlying
frozen likelihood means this is not independent observational evidence.
Contradictions: Q008 H 0=71.5 active minimum contradicted by materially lower Q011
basin.
6. NEGATIVE RESULTS / MIKAMI
Failed route: Promotion of Q008 high-H 0 minima to global/strongly near-global status.
Mikami Graveyard:
Q011-GLOBAL-CERTIFICATION — REJECTED.
Reason: certification gate failed; materially lower competing basin found.
7. MODEL CHANGE
Before: Q008 H 0=71.5, χ
2=547.154321 active best-observed.
After: Q011 H 0=71.5, χ
2=546.364260 active best-observed.
Change: MODIFIED / CONSTRAINED.
Reason: Δ χ
2=−0.790061, exceeding material threshold 0.50; PAT-001 strengthened.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: ”e113fb846948f424b865d1303fba8b5988ec9133”
GitHub run: ”33363067156”
Workflow: Bubbleverse Q011 EDE Globality Certification V4
Program: ”q011_ede_globality_certification_v4.py”
Program SHA256:
”53dc99d00d220671fe16d17136ef626a7db454711120f5861a6677b3879c57e6”
Config: ”q011_ede_globality_certification_v4_config.yml”
Config SHA256:
”37baaee48fd4f2bf70807dd2c6baab6e8a138725f8b70987773d4ddad5b8467b”
Parent: Q008 run ”33307023434”.
9. REPRODUCIBILITY
Checkout recorded commit restore Q005 V14 backend/data run Q011 V4 workflow at → →
recorded fixed-H 0 targets compare generated minima/gates with R-Q011-EDE- →

BUBBLEVERSE Q JOURNALS
0.42
GLOBALITY-CERTIFICATION-004 apply material-improvement threshold → 0.50 and
certification criteria.
10. CONCLUSION
Q011 did not establish global minima. It demonstrated that the high-H 0 EDE likelihood
profile remains optimizer-basin sensitive, with the H 0=71.5 Q008 minimum materially
superseded. EDE remains active but conditional; physical viability is unchanged.
11. NEXT-Q HANDOFF
Next Q: Q012
Reason: Q009/Q010 attribution at H 0=71.5 used the now-superseded Q008 point.
2=546.364260 best-observed basin, how is the
Next question: At the new H 0=71.5, χ
likelihood change distributed between ACT DR6 and Planck low-ℓ, DESI DR2 and BBN, and
do the previous attribution conclusions survive?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No; global/strong near-global certification was not achieved.
Q-JOURNAL: This journal.
MIKAMI GRAVEYARD UPDATE: Q011 global-certification claim rejected.
MODEL CHANGE SUMMARY: Q008 H 0=71.5 minimum superseded; PAT-001 strengthened.
REPRODUCIBILITY / GITHUB: Commit ”e113fb…9133”; run ”33363067156”; Q011 V4
program/config.
NEXT-Q HANDOFF: Q012 — recompute likelihood attribution at the new H 0=71.5 basin.

BUBBLEVERSE Q JOURNALS
0.42
Q012
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q012
Date/time: 2026-09-01 CEST
Status: CONFIRMED
Question: At the new Q011 best-observed (n=3) EDE minimum at fixed
−1 M pc
(H 0=71.5k m s
−1), how is the total ( χ
2) change divided between ACT DR6 and non-
ACT likelihoods, and does the previous Q009/Q010 attribution survive?
2. STARTING STATE
Model: MOD-EDE-N3 / frozen Q005 V14 / ACTIVE–CONSTRAINED.
Inherited: Q011: (H 0=71.5, χ
2=546.364260), BEST-OBSERVED ONLY. Q009/Q010 contained
attribution for the superseded Q008 vector.
Constraint: Fixed-vector evaluation only; no reoptimization, new priors, bounds, model, or
datasets.
3. HYPOTHESES
H1: Previous attribution survives qualitatively.
H2: New basin materially changes attribution.
H3: A broad likelihood sign reverses.
Rejected: H3 — no broad sign reversal.
Surviving: H1 + H2 — qualitative structure survives, quantitative attribution changes.
4. METHOD & EVIDENCE
Method: Exact Q011 vector reevaluated on common serialized attribution basis; ACT full-
covariance decomposition plus Planck low-(ℓ), DESI DR2 and BBN components.
Sources: INTERNAL-Q005; INTERNAL-Q009; INTERNAL-Q010-V4; R-Q011-EDE-GLOBALITY-
CERTIFICATION-004.
Program: ”q012_likelihood_attribution_v1.py”
Workflow: Q012 EDE Likelihood Attribution V1
GitHub run: 33465056836.
Tests: frozen-backend, exact-vector, component closure, ACT quadratic closure/cross-check,
no-reoptimization, final-result gate — PASS.
5. KEY RESULTS
Serialized attribution:

BUBBLEVERSE Q JOURNALS
0.42
- ( Δ χt ot al
2 =−2.612490)
- ACT DR6: 3.372038 −
- Planck low-(ℓ): +0.976557
- DESI DR2: 0.632194 −
- BBN: +0.415184
- non-ACT total: +0.759548
ACT: EE 1.888310; TE 1.980919; TT +0.497192. Strongest improving region: ACT_MID; − −
strongest cell: EE×ACT_MID = 2.788494. −
Final result: Q009/Q010 attribution survives qualitatively, but their active (H 0=71.5)
numbers are superseded. The new basin is even more ACT-driven.
Limitations: Q011 remains BEST-OBSERVED ONLY; external EDE viability not tested.
Optimizer-native and serialized ( χ
2) tracks must not be mixed.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: None scientifically relevant in Q012.
Graveyard: Old Q009 ACT value 2.554002 and Q010 non-ACT +0.851228 killed as active −
71.5 attribution; preserved historically for Q008 vector.
7. MODEL CHANGE
Before: Active 71.5 attribution unresolved after Q011.
After: Active Q012 attribution established.
Change: MOD-EDE-N3 remains ACTIVE / CONSTRAINED; attribution updated, no physical
promotion.
Reason: Fixed-vector Q012 decomposition.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: ”02afd47ae12daae89e9c894ae7bee7576724e85b”
Program SHA256:
”771439e47c9440818821fbdd9e1c18f276d949e69a4697d65d54818184657a2c”
Config: ”q012_likelihood_attribution_v1_config.yml”
Config SHA256:
”c1368581202d8756ca5bd6e6569449b5ba6fb8cf25d59df404274949fcdaac36”
Artifact: ”q012-likelihood-attribution-v1-final”, ID 9784591538, SHA256
”ad492704891475c5acecb240859bef13636597e54d354b513fdc33a0c8bde651”.
9. REPRODUCIBILITY
Checkout recorded commit restore Q005 V14 inputs run Q012 workflow at exact Q011 → →
vector compare component/result outputs require recorded PASS gates and closures. → →

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
The improved (H 0=71.5) EDE basin is primarily favored by ACT DR6, while Planck low-(ℓ)
and BBN oppose it and DESI DR2 mildly favors it. Q012 resolves the internal attribution
question but does not establish globality or physical EDE viability.
11. NEXT-Q HANDOFF
Next Q: Q013
Question: When model definitions, parameterizations, priors, dataset overlap and evidence
independence are treated explicitly, is the active Q011/Q012 (n=3) EDE region at fixed
(H 0=71.5) compatible with relevant external EDE constraints and independent
observational chains, or is it already excluded or substantially weakened?
Reason: Internal attribution is closed; external viability is now the main bottleneck.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Q009/Q010 qualitative attribution survives; active numerical 71.5
attribution is superseded by Q012 and is more strongly ACT-driven.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Historical Q009/Q010 values removed from active use;
preserved as provenance.
MODEL CHANGE SUMMARY: Attribution updated; MOD-EDE-N3 remains constrained, not
established.
REPRODUCIBILITY / GITHUB REFERENCES: Commit ”02afd47…”, run 33465056836, Q012 V1
program/config/artifact above.
NEXT-Q HANDOFF: Q013 — external applicability and viability.

BUBBLEVERSE Q JOURNALS
0.42
Q013
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q013
Date/time: 2026-09-01 05:42 CEST
Status: CONSTRAINED
Question: When model definition, parameterization, priors, dataset overlap and evidence
independence are treated explicitly, is the active Q011/Q012 (n=3) EDE region at fixed
(H 0=71.5) compatible with relevant external constraints, or already excluded/materially
weakened?
2. STARTING STATE
Model entering Q: MOD-EDE-N3 — ACTIVE BUT CONDITIONAL.
Inherited: Q011: (H 0=71.5,f E D E=0.096582859, χ
2=546.364260), BEST-OBSERVED ONLY.
Q012: ACT-driven improvement, ( Δ χ A C T
2 =−3.372038).
Constraint: Same-model comparisons and dataset independence must be explicit; no cross-
model exclusion.
3. HYPOTHESES
H1: External evidence permits the Q011 region.
H2: External evidence excludes it.
H3: Evidence is dataset/model dependent and materially weakens but does not universally
exclude it.
Rejected: H2 as universal claim; K-038 uses (n=2), not Q011’s (n=3).
Surviving: H3 — SUPPORTED.
4. METHOD & EVIDENCE
Method: Same-model literature comparison; model-definition, prior/statistical-method and
dataset-overlap audit.
Primary sources:
K-036 — Poulin et al., PRD 113, 063519 (2026), arXiv:2505.08051.
K-038 — Toda & Seto, JCAP 02 (2026) 019, arXiv:2508.09025.
K-039 — Efstathiou, Rosenberg & Poulin, PRL 132, 221002 (2024), arXiv:2311.00524.
K-040 — Khalife et al./SPT-3G, PRD 113, 103546 (2026), arXiv:2507.23355.
Internal: Q005, R-Q011, R-Q012.
Programs/workflows: No new numerical Q013 run; research/evidence synthesis only.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
- K-036 uses (n=3) and permits roughly (f E D E=0.09±0.03, H 0=71.0±1.1), but shares
ACT/DESI/Planck data.
- K-038’s (f E D E<0.014) is (n=2) and cannot directly exclude Q011.
- K-039 is same-model (n=3); profile limits approximately (f E D E<0.094 , H 0<70.2) at ( σ 2σ ),
materially pressuring Q011.
- K-040 SPT-only allows (f E D E<0.12) but does not independently prefer (H 0≈71.5).
Final result: Q011’s (n=3) high-(H 0) region is not universally excluded, but materially
externally weakened and not independently certified.
Limitations: No direct common-likelihood ( Δ χ
2) evaluation of the exact Q011 region; K-039
limits are separate 1D profiles.
Contradiction: Previous K-036/K-038 same-model conflict dissolved.
6. NEGATIVE RESULTS / MIKAMI
Killed: “K-038 directly excludes Q011 (n=3).” — wrong model mapping.
Killed: “K-036 independently confirms Q011.” — substantial dataset overlap.
Killed: “External evidence has already ruled out all high-(H 0) (n=3) EDE.” — too strong.
7. MODEL CHANGE
Before: MOD-EDE-N3 — ACTIVE BUT CONDITIONAL.
After: ACTIVE BUT MATERIALLY EXTERNALLY WEAKENED — NOT EXTERNALLY
CERTIFIED.
Change: CONSTRAINED.
Reason: Same-(n=3) Planck NPIPE resistance plus lack of independent SPT high-(H 0)
replication.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse.
Q013 commit/workflow/program: NOT RECORDED AT TIME OF Q.
Inherited Q011: commit ”e113fb846948f424b865d1303fba8b5988ec9133”, run
”33363067156”.
Inherited Q012: commit ”02afd47ae12daae89e9c894ae7bee7576724e85b”, run
”33465056836”.
Provenance: External primary literature compared against frozen Q005/Q011/Q012 model
state.
9. REPRODUCIBILITY
Reproduce by retrieving K-036/K-038/K-039/K-040, confirming (n), datasets and statistical
treatment; retrieve Q011/Q012 recorded states; compare model compatibility and overlap

BUBBLEVERSE Q JOURNALS
0.42
using the same acceptance rule: same-model evidence may constrain Q011, overlapping
evidence is not independent replication.
10. CONCLUSION
The active (n=3) EDE basin survives as a candidate, but its physical interpretation is
substantially weaker than its internal ACT-driven fit alone suggests. Planck NPIPE provides
genuine same-model pressure, while SPT-only does not independently reproduce the high-
(H 0) preference.
11. NEXT-Q HANDOFF
Next Q: Q014.
Why: Direct external likelihood penalty remains unmeasured.
Next question: For the same (n=3) EDE model, what likelihood penalty does the (H 0=71.5)
region receive in Planck NPIPE and SPT-3G D1 when each chain is correctly reprofiled and
overlapping data are not double counted?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Not universally excluded; materially externally weakened and not
independently certified.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: K-038 direct-exclusion and K-036 independent-confirmation
interpretations killed.
MODEL CHANGE SUMMARY: MOD-EDE-N3 materially externally weakened. →
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; Q011/Q012 provenance above; Q013
execution metadata not recorded.
NEXT-Q HANDOFF: Q014 — direct Planck NPIPE/SPT-3G same-model likelihood test.

BUBBLEVERSE Q JOURNALS
0.42
Q014
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
Q-ID: Q014 | Completed: 2026-09-02 | Status: SUPPORTED
1. IDENTITY
Question: Når den samme n=3 EDE-model anvendes, hvor stor ekstern likelihood-penalty
får high-H₀-regionen omkring det aktive Q011-punkt ved H₀=71.5 km s⁻¹ Mpc ⁻¹ i Planck
NPIPE- og SPT-3G D1-kæderne, når hver kædes egne nuisance-parametre og relevante
kosmologiske parametre profileres korrekt og datasetoverlap ikke dobbeltregnes?
2. STARTING STATE
Model entering Q: MOD-EDE-N3 — ACTIVE / externally weakened / not externally certified.
Inherited: Q011 high-H₀ best-observed basin at H₀=71.5; Q012 ACT-dominated
improvement; Q013 external mapping K-039/K-040.
Frozen constraints: n=3 only; Q011 remains BEST-OBSERVED MINIMUM ONLY; chain-
native nuisance profiling; no Planck+SPT χ² sum; no H0DN/SH0ES prior; SPT+DESI
secondary due overlap.
3. HYPOTHESES
H1: H₀=71.5 receives large external penalty across CMB chains.
H2: External viability is dataset/likelihood dependent.
H3: Exact Q011/ACT parameter vector is externally portable.
Rejected: H1 as universal claim; H3.
Surviving: H2 — supported.
4. METHOD & EVIDENCE
Profile-likelihood comparison of each chain’s free-H₀ minimum, fixed H ₀=71.5 reprofile,
and exact Q011 shared-physics vector. Multistart stability, monotonicity, finite-result,
provenance and fixed free embedding gates required. →
Sources: K-039 Planck NPIPE n=3; K-040 SPT-3G D1 n=3; K-029 DESI DR2 secondary.
Workflow: Bubbleverse Q014 n=3 EDE External Viability V12.
Program: ”q014_external_viability_v12.py”.
5. KEY RESULTS
Fixed H₀=71.5 profile penalties:
Planck NPIPE approximation Δχ²=+12.873928; SPT D1-only +0.342067; SPT D1+DESI
+0.157387.
Exact Q011-vector penalties:
Planck +101.858574; SPT-only +22.112326; SPT+DESI +21.511108.

BUBBLEVERSE Q JOURNALS
0.42
Final result: High-H₀ n=3 EDE viability is strongly dataset/likelihood dependent; the exact
ACT/Q011 vector is not externally portable.
Limits: Planck/SPT are common-backend, not exact paper-native K-039/K-040
reproductions; no proof of mathematical globality.
Contradiction: Planck materially penalizes H₀=71.5 while SPT does not.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1–V11:
extraction/setup/package/import/nuisance/objective/multistart/wrapper/nesting/embedding
failures; none accepted as Q014 physics. V12 supersedes them.
Graveyard:
- Universal large high-H₀ external penalty — REJECTED by SPT.
- Exact Q011-vector as generally externally viable — REJECTED by all tested chains.
- K-038 n=2 as direct n=3 test — INAPPLICABLE.
7. MODEL CHANGE
Before: MOD-EDE-N3 active but materially externally weakened, not certified.
After: ACTIVE BUT STRONGLY DATASET/LIKELIHOOD DEPENDENT; H₀=71.5 survives SPT
profiling but is penalized by Planck; exact Q011/ACT vector not externally portable.
Change: CONSTRAINED / REFINED.
8. GITHUB / PROVENANCE
Repo: Morfindien/Bubbleverse
Head: ”ab42b1937ca935f498a006ead2c034954ce1d81f”
GitHub run: ”33597153303”
Result: ”R-Q014-EDE-EXTERNAL-VIABILITY-009”
Artifact: ”q014-external-viability-v12-final”, ID ”9837116589”, digest
”sha256:7ac4b9a2ef6f9d64bebaa55cec50fa8cf84cfaba7bc00fe8cd055ee183e65856”
Jobs: 39/39; all mandatory gates PASS.
9. REPRODUCIBILITY
Checkout recorded head; recover frozen Q011 vector and Q014 inputs; run V12 workflow
with frozen n=3 configuration; verify 39/39 outputs and artifact; apply identical stability,
monotonicity, provenance and embedding gates.
10. CONCLUSION
Q014 closes: Planck and SPT do not impose the same penalty on reprofiled high-H ₀ n=3
EDE. Planck gives substantial resistance, SPT almost none, while all tested external chains
strongly reject the exact ACT-optimized Q011 parameter vector.
11. NEXT-Q HANDOFF
Next Q: Q015

BUBBLEVERSE Q JOURNALS
0.42
Why: Determine what physically/statistically drives the validated Planck–SPT difference.
Question: Which CMB likelihood components, observables, multipole ranges and chain-
native nuisance/calibration directions drive Planck’s Δχ² +12.87 versus SPT’s Δχ² +0.34 at ≈ ≈
H₀=71.5?
REQUIRED END-OF-Q OUTPUT:
FINAL ANSWER: Dataset-/likelihood-dependent viability; exact Q011 vector externally
rejected.
Q-JOURNAL: This entry.
MIKAMI: Universal penalty + exact-vector portability killed.
MODEL CHANGE: MOD-EDE-N3 constrained/refined.
REPRODUCIBILITY: Repo/run/artifact above.
NEXT-Q: Q015.

BUBBLEVERSE Q JOURNALS
0.42
Q015
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q015
Date/time: 2026-09-02 19:00 CEST
Status: CONFIRMED
Question: At fixed H 0=71.5 in the same n=3 EDE common backend, which CMB
components, observables, multipoles and chain-native calibration directions explain the
Planck NPIPE-approximation Δ χ
2=+12.873928 versus SPT-3G D1-only +0.342067?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; frozen class_ede backend, commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q011 best-observed H 0=71.5 basin; Q012 ACT attribution; Q014 Planck/SPT
external profiles and rejection of exact-Q011-vector portability.
Constraints: No cross-chain χ
2 summing/comparison; Q011 remains BEST-OBSERVED
MINIMUM ONLY; Planck/SPT endpoints independently reprofiled.
3. HYPOTHESES
Tested:
H1: Planck’s +12.87 is mainly CMB.
H2: Planck/SPT penalties have similar TT/TE/EE structure.
H3: SPT calibration hides a large penalty.
Rejected: H1, H2, H3.
Surviving: Dataset-/likelihood-specific spectral response; causal mechanism remains OPEN.
4. METHOD & EVIDENCE
Methods: Within-chain decomposition; covariance-aware TT/TE/EE and ℓ-bin attribution;
nuisance/calibration endpoint comparison.
Sources: K-036 ACT+DESI; K-039 Planck NPIPE; K-040 SPT-3G D1; SPT D1 spectra
arXiv:2506.20707; Q011–Q014 internal results.
Programs/workflows: Q015-CMB-ATTRIBUTION-V3; V2 endpoint jobs + V3
certification/merge.
5. KEY RESULTS
Planck: CMB +4.541019, low-z +5.319582, constraints +3.013327 total → +12.873928. High-ℓ:
TT +4.837082, TE +0.021571, EE −0.582330; strongest band ℓ=500 – 999, +3.452059. A pl anc k
moves ∼1.918σ.

BUBBLEVERSE Q JOURNALS
0.42
SPT: primary +0.743683, lensing −0.351681, τ −0.044647, Tcal −0.005287 total → +0.342067.
Primary: TE +1.138190, TT −0.557279, EE +0.168448. Tcal moves only ∼0.018σ.
Final result: Planck/SPT difference is not one universal EDE CMB penalty; it arises from
different chain components and covariance-coupled spectral responses.
Limitations: Attribution ≠ causation; branches are common-backend approximations, not
exact K-039/K-040 reproductions.
Contradictions: None fundamental.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 failed ”KeyError: use_fg_residual_model” — software transport failure.
V2 final merge failed an invalid raw-covariance/serialized-likelihood identity gate;
endpoint science remained valid and was certified unchanged by V3.
Graveyard:
- “Planck CMB = +12.87” — killed.
- Uniform Planck/SPT CMB penalty — killed.
- SPT Tcal as main driver — killed under tested conditions.
7. MODEL CHANGE
Before: C-EDE-002 = broad Planck/SPT high-H 0 discrepancy.
After: Discrepancy localized to different component/TT-TE-EE/ℓ/calibration structures.
Change: FC-002 strengthened; C-EDE-002 refined; FC-001 remains active.
Reason: Q015 covariance-aware attribution.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
V2 run: ”33629190153”
Head: ”78a65aae897fca18132a5c0758bccdbbc6a09402”
Result: ”R-Q015-EDE-CMB-ATTRIBUTION-003”
Workflow: ”Q015-CMB-ATTRIBUTION-V3”
V3 final GitHub run ID: NOT RECORDED
Final archive SHA-256:
”80b774f66c9f0650e2c36f19633a2daa6fbee69d1dbde2a9df91e286520ca8d4”
9. REPRODUCIBILITY
Checkout recorded versions obtain Q014 endpoints/likelihood data reproduce V2 → →
endpoint attribution preserve covariance allocations and bridge terms run V3 → →
certification verify final PASS and recorded outputs. →
10. CONCLUSION
Q015 resolves where the Planck/SPT difference appears, not why it exists. Planck’s large
total is partly non-CMB and its high-ℓ response is TT-dominated; SPT’s primary response is

BUBBLEVERSE Q JOURNALS
0.42
TE-dominated and substantially compensated by TT and lensing. High-H 0 n=3 EDE
viability is therefore strongly dataset/likelihood dependent.
11. NEXT-Q HANDOFF
Next Q: Q016
Why: The remaining uncertainty is mechanistic.
Question: On matched ACT/Planck/SPT observables and overlapping multipoles, does the
differing high-H 0 response reduce to experiment-/likelihood-specific structure, or does a
common physical CMB residual survive?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Q015 resolved the Planck/SPT attribution; no universal CMB penalty
exists.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Three simplified explanations killed; V1/V2 failures
retained as technical provenance.
MODEL CHANGE SUMMARY: C-EDE-002 refined; FC-002 strengthened; FC-001 remains
open.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; V2 run 33629190153; Q015-CMB-
ATTRIBUTION-V3; final archive SHA above.
NEXT-Q HANDOFF: Q016 — matched ACT/Planck/SPT spectral-response test.

BUBBLEVERSE Q JOURNALS
0.42
Q016
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q016
Date/time: 2026-09-04 06:25 CEST
Status: SUPPORTED
Question: While Planck NPIPE, SPT-3G D1 and ACT DR6 are examined on a deliberately
matched n=3 EDE surface with comparable CMB observables and overlapping multipole
ranges, can the documented difference in high-H₀ response be explained by
experiment-/likelihood-specific frequency, foreground, calibration, sky or covariance
structure, or does a common residual pattern survive across the experiments?
2. STARTING STATE
Model entering Q: MOD-EDE-N3 — ACTIVE / CONSTRAINED; ”mwt5345/class_ede”, commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q014 showed strong Planck vs weak SPT high-H₀ response; Q015 found different
covariance-aware Planck/SPT attribution patterns; exact Q011 vector already rejected as
universal endpoint.
Constraints: TT+TE+EE, ℓ=600–2000; fixed H₀=71.5 vs free profile; no cross-chain χ² sum;
chain-native nuisance reprofiling.
3. HYPOTHESES
Tested:
H1: response difference is experiment-/likelihood-specific.
H2: one common residual pattern survives across Planck/SPT/ACT.
H3: apparent Planck difference is optimizer/globality artefact.
Rejected: H2 — 0/9 matched residual cells shared the same non-zero sign. H3 — Planck low-
H₀ basin reproduced by multistart certification.
Surviving: H1 — supported; exact instrumental sub-cause remains unresolved.
4. METHOD & EVIDENCE
Methods: matched free/fixed profiling; covariance-aware residual decomposition by
TT/TE/EE and multipole band; multistart/globality checks.
Sources: K-036, K-039–K-046; Planck NPIPE/CamSpec, SPT-3G D1, ACT DR6.
Programs/workflows: Q016 V16 matched-surface certification; ”q016-cmb-mechanism-
v4.yml”.
Key run: GitHub run ”33836015653”, SHA ”91bc0736a00e2454d4e37324e5d3a1a7fe7813d6”.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Planck matched primary penalty: Δχ²=+4.67204, mainly ℓ=600–999 (+3.22423).
SPT: +0.01465; ACT: +0.01512, both with strong internal cancellations.
Common residual sign: 0/9 cells.
Final result: Q016-A — EXPERIMENT-SPECIFIC LOCALIZATION.
Limitations: No unique frequency/calibration/foreground/covariance cause identified; no
combined inter-experiment significance; SPT/ACT full-MF secondary diagnostics technically
incomplete.
Contradictions: No fundamental cosmological contradiction identified.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 dependency/bootstrap failure; V2 path/API failure; V3 Planck/ACT API
mismatches; SPT full-MF shape mismatch; ACT full-MF missing ”mflike”. Technical failures
only.
Mikami Graveyard additions:
- Common Planck/SPT/ACT residual-direction hypothesis — killed by 0/9 sign concordance.
- Planck optimizer-artifact explanation — killed by V16 multistart reproduction.
- Uniform CMB high-H₀ penalty — rejected.
7. MODEL CHANGE
Before: MOD-EDE-N3 active with unresolved optimizer/dataset-response ambiguity.
After: MOD-EDE-N3 remains active but explicitly strongly dataset-/likelihood-dependent.
Change: constrained / refined.
Reason: certified Planck–SPT–ACT response split without common residual direction.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commit: ”91bc0736a00e2454d4e37324e5d3a1a7fe7813d6”
Workflow: ”.github/workflows/q016-cmb-mechanism-v4.yml”
Results: ”R-Q016-EDE-MATCHED-CMB-SURFACE-016”; ”R-Q016-EDE-CMB-MECHANISM-004”
Artifacts: merged ”9923364927”; final gates ”9923368121”.
Provenance: V16 certified endpoints reused; V4 decomposed matched residual/covariance
response without reoptimizing parent endpoints.
9. REPRODUCIBILITY
Checkout recorded commits obtain frozen Planck/SPT/ACT likelihood inputs reproduce → →
V16 free/fixed endpoints run V4 mechanism workflow verify covariance closure and → →
0/9 sign test apply Q016 A/B/C decision rule. →

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q016 establishes that the tested high-H₀ n=3 EDE response is not one common CMB
residual expressed with different strength. Planck shows a substantial penalty, while SPT
and ACT remain nearly indifferent through different cancellation structures. The result
localizes the discrepancy to experiment-/likelihood-response structure, not to a proven
instrumental systematic or new physics.
11. NEXT-Q HANDOFF
Next Q: Q017
Why: Planck is now the principal unresolved mechanism bottleneck.
Next question: Is Planck’s H₀=71.5 penalty, especially at ℓ=600–999, localized to specific full-
multifrequency frequency/calibration/foreground/covariance directions, or broadly
distributed?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Q016-A — EXPERIMENT-SPECIFIC LOCALIZATION.
Q-JOURNAL: This journal.
MIKAMI GRAVEYARD UPDATE: Common residual, uniform penalty and optimizer-artifact
routes rejected.
MODEL CHANGE SUMMARY: MOD-EDE-N3 retained but strengthened as
dataset-/likelihood-dependent.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; run ”33836015653”; SHA
”91bc0736…”; V16 + V4 results above.
NEXT-Q HANDOFF: Q017 — isolate the Planck-specific high-H ₀ penalty mechanism.

BUBBLEVERSE Q JOURNALS
0.42
Q017
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
Q-ID: Q017 | Date: 2026-09-04 | Status: INCONCLUSIVE
QUESTION: On the certified Q016 n=3 EDE Planck NPIPE/CamSpec surface, is the high-H₀
penalty at H₀=71.5—especially the ℓ=600–999 contribution—localized to specific Planck TT
frequency, calibration, foreground or covariance directions in a full multifrequency
likelihood, or does the penalty remain broadly distributed after nuisance-aware
reprofiling?
STARTING STATE
Model: MOD-EDE-N3; n_scf=3; mwt5345/class_ede commit
5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited: Q016 certified Planck endpoints: FREE H₀=67.988328967159; FIXED H ₀=71.5.
Q016 localized most matched Planck penalty to ℓ=600–999; Q015 showed strong
covariance-coupled 143×217 structure.
Constraint: freeze cosmology/endpoints; full-MF Planck nuisance-only reprofiling; no
causal-systematic claim.
HYPOTHESES
H1: penalty localizes to one specific Planck direction.
H2: penalty remains broadly distributed.
H3: neither classification meets preregistered thresholds.
Rejected: H1, H2 under Q017 thresholds.
Surviving: H3 — INDETERMINATE / multidirectional response.
METHOD & EVIDENCE
Likelihood: planck_NPIPE_highl_CamSpec.TTTEEE. Nine calibration/foreground nuisances
reprofiled; 3 baseline starts/endpoint; 2 starts/lock group; covariance-aware
frequency/block decomposition.
Sources: K-039 (arXiv:2311.00524), K-044 (arXiv:2205.10869), K-045 (arXiv:2510.09430),
K-046 Cobaya docs; internal Q015/Q016.
Workflow: Bubbleverse Q017 Planck Direction Localization V3; GitHub run 33842355384.
Mandatory stability, closure, nesting and FINAL_RESULT_GATE: PASS.
KEY RESULTS
Full-MF fixed free objective: +17.3979348723; raw high-ℓ χ²: +17.2433166263. −
ℓ=600–999 TT abs shares: 143×217=0.54791; 143×143=0.38458; 217×217=0.06751. Effective
frequency number=2.20913.

BUBBLEVERSE Q JOURNALS
0.42
Nuisance lock shares: calibration=0.45469; fg143×217=0.18883; fg217=0.17999;
fg143=0.17648. Strongest covariance pair share=0.17533.
Final: penalty survives nuisance reprofiling, but neither specific-localized nor broadly-
distributed criteria pass. Classification: INDETERMINATE.
Limit: attribution ≠ causal systematic; Q016 and Q017 objectives are different likelihood
constructions.
NEGATIVE RESULTS / MIKAMI
V1: static-gate implementation failure; no scientific result.
V2: workflow path typo
(”q005h pcv24r e quir e me nt s.t x t ”v s”q005h pcv14r e quir e me nt s.t x t ”); scientific
execution never started.
Mikami: killed strong claims “143×217 is the cause”, “calibration is the cause”, and “penalty
is demonstrably broadly distributed”.
MODEL CHANGE
Before: FC-CMB-002 allowed possible specific Planck
frequency/calibration/foreground/covariance localization.
After: FC-CMB-002 remains active only as a multidirectional Planck-specific
likelihood/covariance candidate.
Change: CONSTRAINED / MODIFIED.
Reason: no single tested direction crossed localization thresholds.
GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Execution commit: 277bb274e5783831303b542681e8cf87a70d31c2
Backend commit: 5a131c91d657dd9a7c6364cc45b038710f8d0d97
Result: R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-003
Artifact: q017-final-v3, ID 9925585139, SHA-256
a45ba197f20595013d390136e00f8fd83f40a70fb9e9e1d83f2048f2d70320db.
REPRODUCIBILITY
Checkout recorded commit obtain frozen Q016 endpoint lock/Planck likelihood run V3 → →
workflow with frozen config compare baseline/lock/decomposition/final JSON outputs → →
apply unchanged preregistered classification thresholds.
CONCLUSION
The Planck high-H₀ penalty is robust to the tested full-MF nuisance reprofiling, but its
ℓ=600–999 structure is neither sufficiently concentrated in one
frequency/nuisance/covariance direction nor sufficiently broad to satisfy the opposite
criterion. Q017 therefore closes as INDETERMINATE, not technically unresolved.

BUBBLEVERSE Q JOURNALS
0.42
NEXT-Q HANDOFF
Next Q: Q018.
Question: Which explicit likelihood ingredients account for the difference between the
Q016 matched Planck penalty (+5.823856774789) and Q017 full-MF penalty
(+17.397934872301) at the same certified cosmological endpoints?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: INDETERMINATE; strong Planck penalty survives, no unique or broad
direction certified.
Q-JOURNAL: this entry.
MIKAMI GRAVEYARD UPDATE: single-direction causal claims rejected.
MODEL CHANGE SUMMARY: FC-CMB-002 constrained to multidirectional candidate.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; run 33842355384; commit
277bb274…; result R-Q017-EDE-PLANCK-DIRECTION-LOCALIZATION-003.
NEXT-Q HANDOFF: Q018 likelihood-bridge analysis.

BUBBLEVERSE Q JOURNALS
0.42
Q018
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q018
Date/time: 2026-09-04 09:15 CEST
Status: CONFIRMED
Question: When the same certified Q016 n=3 EDE Planck FREE and H 0=71.5 FIXED
endpoints are evaluated through a controlled bridge between Q016 CamSpec-lite and Q017
full-multifrequency CamSpec, what explains the penalty increase from +5.823856774789 to +17.397934872301, and is it one
component or several coupled components?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, ACTIVE / CONSTRAINED; nsc f=3; frozen backend
mwt5345/class_ede commit 5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited results:
- Q016: FREE H 0=67.988328967159, FIXED H 0=71.5, matched penalty +5.823856774789.
- Q017: full-MF penalty +17.397934872301, localization INDETERMINATE.
Constraints: same endpoints/model/backend; no cross-chain χ² addition; architecture gap
not physical χ²; Q017 not reopened.
3. HYPOTHESES
Tested:
- H1: objective/prior semantics causes most of the gap.
- H2: shared A pl anc k ,c alT E ,c al E E nuisance freedom causes most of the gap.
- H3: one clean additive likelihood component explains the gap.
Rejected:
- H1: native vs likelihood-only differs by only 0.235. ≈
- H2/H3: large penalty survives shared3 locking; no valid additive isolation.
Surviving:
- Coupled full-MF likelihood-architecture dependence: SUPPORTED.
4. METHOD & EVIDENCE
Methods: four controlled full-MF bridge surfaces, two endpoints, three multistarts each.
Primary evidence/sources:
- K-039 arXiv:2311.00524
- K-044 arXiv:2205.10869
- K-045 arXiv:2510.09430

BUBBLEVERSE Q JOURNALS
0.42
- K-046 Cobaya 3.5.6 documentation/source
- Q016/Q017 internal certified results.
Programs/workflows:
- Q018-PLANCK-LIKELIHOOD-BRIDGE-V3
- Bubbleverse Q018 Planck likelihood bridge V3
- 24 profile jobs.
Tests performed: identity, endpoint, completeness, multistart, finite-result, Q017-native
reproduction, non-additivity gates.
5. KEY RESULTS
Important results:
- full_native = 17.395372421241
- full_likelihood_only = 17.160171713960
- foreground6_only = 15.617680433608
- shared3_only = 11.764134763087
Final result: The extra full-MF Planck penalty is produced by coupled likelihood-
architecture effects, not one independently separable component.
Uncertainties / limitations:
- shared3_only unstable: spreads 5.28 fixed, 6.03 free. ≈ ≈
- frequency/covariance/foreground contributions remain inseparable as additive physical
terms.
Contradictions discovered: None fundamental.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts:
- V1 failed endpoint-lock schema gate; no scientific compute.
- V2 failed endpoint API/config compatibility; no scientific minimizer.
Mikami Graveyard additions:
- OBJECTIVE-SEMANTICS-ONLY.
- SINGLE CLEAN ADDITIVE COMPONENT.
- SHARED3-ONLY as sufficient explanation.
- Architecture gap 11.574078… as physical χ² component.
7. MODEL CHANGE
Before: FC-CMB-002 = possible multidirectional Planck-specific likelihood/covariance
response.
After: FC-CMB-002 = MULTIDIRECTIONAL, LIKELIHOOD-CONSTRUCTION-DEPENDENT
PLANCK RESPONSE.
Change: modified / constrained.

BUBBLEVERSE Q JOURNALS
0.42
Reason: Q018 shows the magnitude of the Planck high-H 0 penalty depends materially on
likelihood construction.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: 1883370cab6bc1bf94c48300015f8306ef1dfe47
Workflow: Bubbleverse Q018 Planck likelihood bridge V3
Program/result ID: R-Q018-EDE-PLANCK-LIKELIHOOD-BRIDGE-003
GitHub Actions run: 33846317737
Result files:
- q018_merged_v3.json
- q018_tests_v3.json
Provenance note: reused certified Q016 endpoints and Q017 full-MF architecture on frozen
MOD-EDE-N3 backend.
9. REPRODUCIBILITY
1. Checkout recorded commit.
2. Use frozen backend and Q016 endpoints.
3. Run Q018 V3 workflow with 4 surfaces × 2 endpoints × 3 restarts.
4. Compare merged/test JSON outputs.
5. Require mandatory gates PASS and preserve non-additivity rule.
10. CONCLUSION
Q018 confirms that Q016 and Q017 are valid but distinct likelihood objectives. Their
penalty difference must not be interpreted physically as an additive χ² term. Native
prior/objective semantics is subdominant; the dominant change belongs to the coupled full-
multifrequency Planck likelihood architecture.
11. NEXT-Q HANDOFF
Why another Q is required: Q018 tested fixed certified endpoints but did not determine
whether likelihood choice shifts the preferred cosmological EDE solution itself.
Next Q: Q019
Next question: Does separately reprofiling MOD-EDE-N3 under CamSpec-lite and full-MF
CamSpec materially shift the preferred H 0 and EDE parameters, or mainly alter the high-
H 0 penalty?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Coupled likelihood-architecture dependence; no single additive
component identified.
Q-JOURNAL: This journal.

BUBBLEVERSE Q JOURNALS
0.42
MIKAMI GRAVEYARD UPDATE: objective-semantics-only, shared3-only, single-component,
and physical-gap interpretations killed.
MODEL CHANGE SUMMARY: FC-CMB-002 refined to likelihood-construction-dependent
multidirectional Planck response.
REPRODUCIBILITY / GITHUB REFERENCES: Morfindien/Bubbleverse; commit 1883370…;
run 33846317737; R-Q018-EDE-PLANCK-LIKELIHOOD-BRIDGE-003; q018_merged_v3.json;
q018_tests_v3.json.
NEXT-Q HANDOFF: Q019 — test whether likelihood dependence changes the preferred
MOD-EDE-N3 cosmology itself.

BUBBLEVERSE Q JOURNALS
0.42
Q019
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q019
Date/time: 2026-09-04 14:35 CEST
Status: SUPPORTED
Question: When MOD-EDE-N3 is independently reprofiled under Q016 matched/CamSpec-
lite and Q017 full-multifrequency CamSpec, does likelihood choice materially shift the
preferred EDE/H₀ region, or mainly change the penalty at frozen high-H ₀ endpoints?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3; ACTIVE TEST MODEL. Backend
”mwt5345/class_ede”, commit ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q016 matched Planck penalty +5.8238568 at H₀=71.5; Q017 full-MF penalty
+17.3979349, INDETERMINATE; Q018 likelihood-architecture dependence.
Constraints: Same model/backend; harmonized objective semantics; no cross-chain χ²
summation; Q018 architecture gap nonphysical; threshold 1.0 operational, not significance.
3. HYPOTHESES
H1: Likelihood choice mainly changes high-H₀ penalty.
H2: Likelihood choice materially shifts the multidimensional preferred region.
H3: Difference is primarily optimizer/globality artifact.
Rejected: H1 as sufficient description; H3 as principal explanation after V3 stability.
Surviving: H2 — SUPPORTED under frozen Q019 criterion.
4. METHOD & EVIDENCE
Methods: Independent lite/full-MF reprofiling; fixed-H₀=71.5 profiles; reciprocal cross-
profile tests; targeted multistart/globality repair; Q016 endpoint reproduction.
Sources: K-039, K-044, K-045, K-046; Q016–Q018 internal validated chain.
Programs/workflows: ”q019_planck_cosmology_reprofile_v1.py”; ”q019_globality_v3.py”;
”.github/workflows/q019-planck-globality-repair-v3.yml”.
Tests: 12/12 V3 continuations; stability, reference reproduction, frozen-classification and
interpretation-safety gates.
5. KEY RESULTS
Lite free: H₀=67.9726651, fEDE=0.0462741.
Full-MF free: H₀=68.1061207, fEDE=0.0439411.
Cross-costs: full-MF optimum lite = +0.8120; lite optimum full-MF = +13.5564. → →

BUBBLEVERSE Q JOURNALS
0.42
Reprofiled H₀=71.5 penalties: lite +5.0620; full-MF +15.3993.
V3 best-two spread = 0.05387; 12/12 complete; FINAL_RESULT_GATE=PASS.
Final result: Similar H₀/fEDE coordinates do not imply equivalent multidimensional
preferred regions; likelihood choice materially shifts MOD-EDE-N3 likelihood geometry.
Limitations: No unique physical/systematic cause identified; internal Planck reanalysis, not
independent observation.
Contradiction: No fundamental contradiction; earlier “only penalty changes” interpretation
rejected.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 remained INDETERMINATE from stability/reference gates; V2 suffered
endpoint-vector and PyYAML technical failures.
Graveyard additions:
PLANCK-OPTIMIZER-ARTIFACT — rejected as principal explanation.
“ONLY HIGH-H₀ PENALTY CHANGES” — rejected as sufficient description.
7. MODEL CHANGE
Before: Planck response known to depend on likelihood architecture mainly through
penalty differences.
After: Response classified as multidirectional and likelihood-construction-dependent in full
parameter geometry.
Change: PRÆCISERET / STRENGTHENED.
Reason: Asymmetric cross-profile costs with validated globality.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Q019 V3 commit: ”71238a5dd27bba4c9f399dfaac638814bed7361e”
Run: ”33868899612”
Result: ”R-Q019-EDE-PLANCK-COSMOLOGY-REPROFILE-003”
Workflow: ”.github/workflows/q019-planck-globality-repair-v3.yml”
Programs: ”q019_globality_v3.py”, ”q019_tests_v3.py”
Provenance: Q019 V1 profiles/cross-tests + V3 targeted globality and Q016 reference
validation.
9. REPRODUCIBILITY
Checkout recorded commits; obtain frozen Planck/CamSpec inputs; run Q019 workflow
with frozen model/objective; compare generated JSON/results; apply unchanged 1.0 cross-
cost criterion and mandatory gates.

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q019 supports a material likelihood-construction dependence of the preferred
multidimensional MOD-EDE-N3 region. The projected H₀ and fEDE minima remain close,
but full-MF strongly penalizes the lite preferred vector while the reverse cost is small. No
Planck systematic or new physics is established.
11. NEXT-Q HANDOFF
Why: The parameter/nuisance direction causing the asymmetry remains unknown.
Next Q: Q020
Question: Which coupled cosmological and full-MF nuisance directions drive the
asymmetric Q019 cross-profile geometry?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Likelihood choice materially changes the multidimensional preferred
MOD-EDE-N3 region despite similar H₀/fEDE minima.
Q-JOURNAL: This journal.
MIKAMI GRAVEYARD UPDATE: Optimizer-artifact and “penalty-only” explanations rejected
as principal/sufficient explanations.
MODEL CHANGE SUMMARY: Planck response refined to multidirectional, likelihood-
construction-dependent parameter geometry.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; commit ”71238a5d…”; run
”33868899612”; Q019 V3 workflow/result.
NEXT-Q HANDOFF: Q020 — identify the coupled parameter direction producing the
asymmetry.

BUBBLEVERSE Q JOURNALS
0.42
Q020
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:13 CEST
1. IDENTITY
Q-ID: Q020
Original completion: 2026-09-04
Status: CONFIRMED
Question: Which multidimensional cosmological/nuisance direction drives the asymmetric
Q019 cross-profile response—lite cost +0.812 versus full-MF cost +13.556—and can it be ≈ ≈
localized without treating correlated likelihood contributions as independent physical χ²
components?
2. STARTING STATE
Model: MOD-EDE-N3; nsc f=3; frozen ”mwt5345/class_ede” commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q018: coupled likelihood-architecture dependence; Q019: likelihood choice shifts
preferred MOD-EDE-N3 region, with preserved asymmetric cross-profile costs.
Constraint: No cross-chain χ² summation; Shapley/interactions diagnostic only, not
causal/independent physical components.
3. HYPOTHESES
Tested: response dominated by EDE timing, primordial parameters, matter parameters, H0,
or distributed coupling.
Rejected: H0-only driver; approximately equal four-block distribution; independent- χ²
interpretation.
Surviving: Limited multidimensional direction dominated by the primordial block;
physical/systematic cause remains unresolved.
4. METHOD & EVIDENCE
Method: 16 hybrid cosmological vertices × 2 likelihood architectures × 2 nuisance restarts =
64 profiles. Blocks: EDE timing (f E D E,log10 zc ,θi), primordial (ns,log A , τ ), matter ( ωb, ωc d m),
H0. Native nuisance parameters reprofiled; Shapley and pair interactions calculated.
Sources: K-039 arXiv:2311.00524; K-044 arXiv:2205.10869; K-045 arXiv:2510.09430; K-046
Cobaya 3.5.6 documentation.
5. KEY RESULTS
Full-MF absolute Shapley fractions: primordial 71.58%, EDE timing 17.27%, matter 9.15%,
H0 2.00%. Primordial signed change: +10.5344. Largest pair interaction: matter×H0
5.7189. −

BUBBLEVERSE Q JOURNALS
0.42
Full-MF geometry span: 14.1286; lite: 0.8632. Historical Q019 costs remain +13.5564 and
+0.8120 and are not replaced.
Final result: LIMITED MULTIDIMENSIONAL DIRECTION LOCALIZED.
Limitation: Block-level only; does not establish ns alone, an instrumental systematic, or new
physics.
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q020 V1 final gate failed because it incorrectly compared a reprofiled
geometry span with Q019’s historical cross cost using different baselines.
Graveyard: H0-only explanation; additive-independent χ² interpretation; V1 final
validation semantics.
Important: V1’s 64 raw profiles remain valid.
7. MODEL CHANGE
Before: Q019 established likelihood-dependent preferred regions, but the responsible
multidimensional direction was unresolved.
After: Full-MF asymmetry is localized primarily to the primordial block; likelihood
response is explicitly architecture-dependent and non-additive.
Change: PRÆCISERET / CONSTRAINED.
8. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Q020 V1 run: ”33876066510”, commit ”7ca5fa06418eb8b6df4c1e6c4077e679fbfdc989”
Q020 V2 run: ”33878880397”, commit ”b0c0a8fd89408bac91502e15d42c69820e913ab6”
Result: ”R-Q020-EDE-PLANCK-CROSS-PROFILE-DIRECTION-002”
Programs: ”q020_direction_localization_v1.py”, ”q020_finalize_repair_v2.py”,
”q020_tests_v2.py”
Workflows: ”q020-planck-cross-profile-direction-v1.yml”, ”q020-cross-profile-gate-repair-
v2.yml”
Artifact: ”q020-final-v2”; FINAL_RESULT_GATE = PASS.
9. REPRODUCIBILITY
Checkout recorded commits; obtain frozen Q019 endpoints/source lock; run V1 64-profile
grid; apply V2 aggregation/tests; verify absolute Q019 cross-objective reproduction,
endpoint non-regression, restart stability, history preservation and no gate relaxation.
10. CONCLUSION
Q020 establishes that the large Q019 full-MF cross-profile asymmetry is not primarily an H0
effect. Under the tested four-block decomposition it is dominated by the primordial
(ns,log A ,τ ) direction, while CamSpec-lite shows a much smaller, more distributed
response. The attribution is functional likelihood geometry, not causal physics.

BUBBLEVERSE Q JOURNALS
0.42
11. NEXT-Q HANDOFF
Next Q: Q021
Why: The parameter direction is localized, but the spectra/frequency/nuisance structure
producing it is not.
Question: Which full-MF spectra/frequency combinations and nuisance couplings carry the
Q020 primordial direction, and can they be connected quantitatively to the earlier
ell/frequency response without treating correlated contributions as independent χ²?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Primordial block dominates full-MF response (~71.58%); H0 alone ~2%;
localization confirmed.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: H0-only driver and additive-independent χ² interpretation
rejected; V1 gate semantics superseded.
MODEL CHANGE SUMMARY: Q019 likelihood-choice effect refined to a primordial-
dominated, architecture-dependent multidimensional geometry.
REPRODUCIBILITY / GITHUB: Runs ”33876066510”, ”33878880397”; commits and files
above.
NEXT-Q HANDOFF: Q021 — localize the corresponding spectrum/frequency/nuisance
mechanism.

BUBBLEVERSE Q JOURNALS
0.42
Q021
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:20 CEST
1. IDENTITY
Q-ID: Q021
Original completion: 2026-09-04, time not fully recorded
Status: CONFIRMED
Question: Within the frozen n=3 early-dark-energy model, what internal structure of the
primordial block (ns,log A ,τ r eio) produces the dominant full-multifrequency Planck cross-
profile response identified in Q020, and does that structure remain materially different on
matched CamSpec-lite?
2. STARTING STATE
Model: MOD-EDE-N3; nsc f=3; mwt5345/class_ede commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q019 established asymmetric matched/full-MF likelihood geometry; Q020
localized 71.58% of absolute full-MF Shapley response to primordial block.
Constraint: Same frozen model/likelihood chain; attribution is functional, not independent
physical χ
2.
3. HYPOTHESES
Tested: ns-only; log A-only; τ-only; pair interaction; three-way/distributed coupling;
likelihood-construction dependence.
Rejected/constrained: No single parameter or pair robustly dominates. Robust matched-vs-
full-MF internal difference not established.
Surviving: PRIMORDIAL THREE-WAY / DISTRIBUTED COUPLING.
4. METHOD & EVIDENCE
Method: 2 likelihood constructions × 8 primordial vertices × 3 coherent optimizer restarts =
48 profiles; Möbius/Harsanyi and exact Shapley decomposition.
Sources: K-039 Efstathiou, Rosenberg & Poulin (2024), arXiv:2311.00524; K-044 Rosenberg,
Gratton & Efstathiou (2022), arXiv:2205.10869; K-046 Cobaya 3.5.6.
Runs: ”Q021-PRIMORDIAL-INTERNAL-STRUCTURE-V1”; repaired by ”Q021-PRIMORDIAL-
INTERNAL-STRUCTURE-REPAIR-V2”.
5. KEY RESULTS
Full-MF: DISTRIBUTED 3/3; ns largest individual term 3/3, absolute fraction 0.2885–0.4891,
never 0.50; ≥ ns Shapley 7.03–8.78.
Matched: DISTRIBUTED 3/3; leader changes between log A × τ, ns×log A, and ns.

BUBBLEVERSE Q JOURNALS
0.42
Full-vs-matched TV range: 0.24068–0.49801 around threshold 0.25 →
SENSITIVE_TO_OPTIMIZER_BASIN.
Final result: Q020 primordial dominance is internally a distributed coupled structure with
persistent ns prominence, not an ns-only effect.
Limitation: Full-MF maximum vertex objective spread 7.7236; matched 0.9149. Detailed
attribution remains basin-sensitive.
Contradiction: None fundamental.
6. NEGATIVE RESULTS / MIKAMI
Failed V1 interpretation: Process-dependent function hashes falsely broke likelihood
identity; best-per-vertex selection produced a non-coherent “Frankenstein” decomposition.
Graveyard: Single-parameter localization; robust single-pair localization; authoritative V1
aggregation.
Preserved: All 48 V1 numerical profiles remain valid.
7. MODEL CHANGE
Before: Primordial block dominant, internal driver unresolved.
After: Primordial response = distributed three-way coupling, ns most persistent individual
direction.
Change: MODIFIED / STRENGTHENED.
Reason: Stable distributed classification across all coherent restarts.
8. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Parent V1 Actions run: ”33882434170”
V1 head: ”03b20081220e9a584458c203fc798cfd39dfd692”
Program: ”scripts/q021_finalize_repair_v2.py”
Workflow: ”.github/workflows/q021_primordial_internal_structure_repair_v2.yml”
Authoritative result: ”R-Q021-EDE-PRIMORDIAL-INTERNAL-STRUCTURE-002”
V2 Actions run/commit: NOT RECORDED IN AVAILABLE JOURNAL MATERIAL.
Provenance: V2 reused all 48 V1 profiles; 0 new likelihood evaluations.
9. REPRODUCIBILITY
Checkout recorded backend/Q chain obtain Q021 V1 48 profiles run V2 coherent- → →
restart finalizer verify mandatory gates PASS reproduce distributed classifications, → →
Möbius/Shapley ranges and TV test.
10. CONCLUSION
Within the frozen MOD-EDE-N3 construction, the full-MF primordial response is robustly
distributed rather than localized to one parameter. ns is consistently the strongest

BUBBLEVERSE Q JOURNALS
0.42
individual direction but never reaches the predefined dominance threshold. Detailed
matched/full-MF decomposition remains optimizer-basin sensitive.
11. NEXT-Q HANDOFF
Next Q: Q022
Question: Within the frozen MOD-EDE-N3 full-multifrequency Planck likelihood, what
distinguishes the coherent optimizer basins observed in Q021, and are they primarily
cosmological, nuisance/foreground, or numerical?
FINAL ANSWER: Distributed primordial coupling; persistent but non-dominant ns.
MIKAMI: Single-driver interpretations killed; V1 aggregation superseded.
MODEL CHANGE: Q020 strengthened and internally refined.
REPRO/GITHUB: ”Morfindien/Bubbleverse”; V1 run ”33882434170”; V2 result ”R-Q021-EDE-
PRIMORDIAL-INTERNAL-STRUCTURE-002”.
NEXT: Q022 — identify the origin of optimizer-basin structure.

BUBBLEVERSE Q JOURNALS
0.42
Q022
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
Q-ID: Q022
Date/time: 2026-09-04 ~21:23 CEST
Status: CONFIRMED
1. IDENTITY
Question: Within the frozen MOD-EDE-N3 full-multifrequency Planck likelihood, what
distinguishes the coherent optimizer basins observed in Q021, and are they primarily
associated with different cosmological compromises, nuisance/foreground compromises, or
numerical optimizer structure?
2. STARTING STATE
Model: MOD-EDE-N3; nsc f=3; mwt5345/class_ede commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q020 — primordial-block dominance; Q021 — distributed primordial coupling
with substantial full-MF multistart spread.
Constraint: Same frozen objective/model/priors; preserve coherent restarts; no cross-
likelihood χ
2 summation.
3. HYPOTHESES
Tested:
H1 pure cosmology basin; H2 pure nuisance/foreground basin; H3 start/incomplete-
minimization artifact; H4 stable mixed multibasin structure.
Rejected: H1/H2: both parameter sectors move materially. H3 for tested masks: exact-
endpoint continuation and tighter refinement did not collapse solutions.
Surviving: H4 — STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE.
4. METHOD & EVIDENCE
Method: Read existing Q021 full-MF endpoints; quantify cosmology/nuisance/foreground
separation; select masks 3, 6, 7; reseed exact Q021 endpoints on identical objective; apply
symmetric tighter refinement.
Sources: K-039 Efstathiou, Rosenberg & Poulin (2024), arXiv:2311.00524; K-044 Rosenberg,
Gratton & Efstathiou (2022), arXiv:2205.10869; K-046 Cobaya 3.5.6; K-047 Cobaya minimizer
documentation.
Programs/workflow: ”q022_globality_continuation_v2.py”; ”.github/workflows/q022-
optimizer-basin-continuation-v2.yml”.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
V1 mean normalized RMS: cosmology 1.6065, nuisance 1.8976, foreground 1.8337;
cosmology/nuisance ratio 0.8466.
V2 refined:
- mask 3: spread 3.5728, joint RMS 2.0246
- mask 6: spread 0.4725, joint RMS 3.0266
- mask 7: spread 3.0928, joint RMS 2.3535
Final result: Stable full-MF basins involve both cosmology and nuisance/foreground
structure and do not collapse under the tested continuation/refinement procedure.
Limitations: Numerical geometry only; not proof of exact mathematical minima, physical
modes, Planck systematics, or new physics.
Contradictions: None with Q021; Q022 resolves its basin-origin uncertainty.
6. NEGATIVE RESULTS / MIKAMI
Killed: PURE-COSMOLOGY-BASIN; PURE-NUISANCE-BASIN; SIMPLE-CROSS-START-
COLLAPSE under tested conditions.
Failed attempts: No scientifically relevant technical failure recorded.
7. MODEL CHANGE
Before: Mixed basin structure observed but origin unresolved.
After: Stable mixed cosmology+nuisance multibasin structure established within frozen
machinery.
Change: CONSTRAINED / REFINED.
Reason: Exact endpoint reseeding + symmetric refinement.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Q021 parent run: ”33882434170”
Q022 V2 commit: ”16a7902c3be7d1967adaae9ee380baf0d17e903a”
Results: ”R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-001”; ”R-Q022-EDE-FULLMF-OPTIMIZER-
BASIN-002”
Program: ”q022_globality_continuation_v2.py”
Workflow: ”.github/workflows/q022-optimizer-basin-continuation-v2.yml”
Numeric Q022 Actions run ID: NOT RECORDED.
9. REPRODUCIBILITY
Checkout recorded commit; obtain Q021 raw endpoints from run ”33882434170”; run Q022
V2 workflow with masks 3/6/7 and frozen backend; compare endpoint/objective
separations; apply collapse criterion requiring both objective spread ≤0.50 and joint RMS ≤0.10.

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
The decisive full-MF optimizer families are stable numerical basins containing material
cosmological and nuisance/foreground differences. Near-equal objective values do not
imply the same solution, as mask 6 demonstrates. No physical cause is established.
11. NEXT-Q HANDOFF
Next Q: Q023
Question: Which specific cosmological and nuisance/foreground parameter combinations
distinguish the stable full-multifrequency basin families, and are those directions
reproducibly shared across masks 3, 6, and 7?
FINAL ANSWER: Stable mixed cosmology+nuisance multibasin structure confirmed within
frozen numerical machinery.
MIKAMI: Pure-cosmology, pure-nuisance and simple-collapse explanations rejected.
MODEL CHANGE: Basin origin refined; no new physical model promoted.
REPRODUCIBILITY: Repo/run/commit/workflow above.
NEXT-Q: Q023 — identify the parameter directions defining the stable basin families.

BUBBLEVERSE Q JOURNALS
0.42
Q023
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q023
Date/time: 2026-09-04 21:50 CEST
Status: CONSTRAINED
Question: Which specific cosmological and nuisance/foreground parameter combinations
distinguish the stable full-multifrequency basin families identified in Q022, and are the
distinguishing directions reproducibly shared across masks 3, 6, and 7?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; (nsc f=3); frozen class_ede commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited results:
Q021: primordial structure is distributed, not (ns)-only.
Q022: stable mixed cosmology+nuisance multibasin structure exists for masks 3, 6, 7.
Constraints: Reuse validated endpoints; no new likelihood evaluations unless necessary; no
physical causation from parameter motion; Q021/Q022 remain closed.
3. HYPOTHESES
Tested:
H1: Basin families share one reproducible normalized parameter direction across masks.
H2: Directions are mask-dependent/non-universal.
H3: Recurrent individual parameters alone define the common direction.
Rejected: H1 and H3 under fixed-lineage criterion; no seed-pair direction reproduces
across all masks.
Surviving: H2 — mask-dependent/non-universal directions. A weaker recurrence of some
individual parameters remains.
4. METHOD & EVIDENCE
Methods: Read-only normalized endpoint-vector comparison; cosine similarity across
masks; parameter ranking and group-energy decomposition.
Primary evidence/sources: Q021/Q022 validated Bubbleverse endpoints; K-039 Efstathiou,
Rosenberg & Poulin (2024); K-044 Rosenberg, Gratton & Efstathiou (2022); Cobaya technical
sources K-046/K-047.
Programs/workflows:
”q023_basin_directions_v2.py”

BUBBLEVERSE Q JOURNALS
0.42
”q023_basin_directions_v2_config.yml”
”q023_tests_v2.py”
”.github/workflows/q023-read-only-basin-directions-v2.yml”
Tests: Endpoint completeness; three-pair direction; finite outputs; zero-new-likelihood;
parent identity; no-overclaim; Q021/Q022 non-reopening. All mandatory gates PASS.
5. KEY RESULTS
Median cross-mask (|cosθ )):
0–1: 0.190; 0–2: 0.316; 1–2: 0.220.
Only mask 3 7 for pair 1–2 reached ↔ (|cosθ)≈0.719); mask 6 did not reproduce it.
Recurring large components included ”amp_143x217”, (H 0), (ωb/ ωc d m), ( A pl anc k), ”amp_217”,
”amp_143”, and (log10 zc).
Final result: ”MASK_DEPENDENT_OR_NONUNIVERSAL_BASIN_DIRECTIONS”.
Limitations: Fixed seed-lineage may not equal permutation-invariant basin identity; no
posterior-volume or physical-cause inference.
Contradictions: None with Q022; stable basins can exist without one universal separating
direction.
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q023 V1 failed ”Q022_FINAL_UNIQUENESS_GATE”, hits=3, due to an
authoritative-file selector bug; technical failure only.
Mikami Graveyard:
Strong universal basin-direction hypothesis — killed under tested lineage definition.
Reason: 0/3 seed-pair directions reproduced across all masks.
7. MODEL CHANGE
Before: Stable mixed multibasins; concrete common direction unknown.
After: Stable mixed multibasins retained; separating directions classified mask-dependent
under tested definition.
Change: CONSTRAINED / PRECISED.
Reason: Validated Q023 cross-mask endpoint geometry.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Execution commit: ”ea5af9a0b25090eb8472adb3c9574dcb4e1efe5c”
GitHub Actions run: ”33913077353”
Result: ”R-Q023-EDE-FULLMF-BASIN-DIRECTIONS-002”
Artifact: ”q023-final-v2”; supplied ZIP SHA-256
”0aae77875aeccf3b5d7245f6b03a83a50a249188d8eb5f25a3066088f4e567ad”
Outputs: ”q023_result_v2.json”, ”q023_tests_v2.json”, ”q023_final_v2.json”.

BUBBLEVERSE Q JOURNALS
0.42
Provenance note: Existing validated Q021/Q022 endpoints were analyzed read-only; 0 new
likelihood evaluations.
9. REPRODUCIBILITY
Checkout recorded commits; obtain preserved Q021/Q022 endpoints; run Q023 V2
workflow/config; compare generated JSON with recorded final artifact; apply identical
cross-mask cosine/reproducibility criterion.
10. CONCLUSION
Q023 shows that Q022’s stable full-MF basins are separated by mixed cosmological,
calibration/nuisance, and foreground directions, but no tested direction is reproducibly
shared across masks 3, 6, and 7. The result concerns internal frozen likelihood geometry,
not physical causation or independent observational evidence.
11. NEXT-Q HANDOFF
Why another Q: Fixed seed labels may not identify equivalent basin families across masks.
Next Q: Q024
Next question: After permutation- and sign-invariant matching of the stable Q022 full-MF
basin endpoints across masks 3, 6, and 7, do reproducible basin-family directions emerge,
or does Q023’s mask-dependent structure persist?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Stable basins persist, but their fixed-lineage separating directions are
mask-dependent/non-universal.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Universal shared basin-direction hypothesis rejected under
Q023 criterion.
MODEL CHANGE SUMMARY: Q022 retained; interpretation narrowed from possible
universal direction to mask-dependent multidimensional geometry.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; run ”33913077353”; commit
”ea5af9a0b25090eb8472adb3c9574dcb4e1efe5c”; Q023 V2 program/workflow/artifact
above.
NEXT-Q HANDOFF: Q024 — test permutation-/sign-invariant basin-family matching.

BUBBLEVERSE Q JOURNALS
0.42
Q024
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q024
Date/time: 2026-09-04 22:23 CEST
Status: SUPPORTED
Question: Can Q022 stable full-multifrequency basin families be matched reproducibly
across masks 3, 6, and 7 using permutation- and sign-invariant endpoint geometry, and
does this alter Q023’s non-universal-direction conclusion?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3, frozen class_ede commit
5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited:
- Q022: stable multibasin structure across masks 3/6/7.
- Q023: basin directions non-universal under fixed seed lineage.
Constraint: Read-only endpoint analysis; no new likelihood evaluations.
3. HYPOTHESES
Tested:
H1: Q023 non-alignment is only a seed-label permutation artefact.
H2: A permutation/sign-invariant common basin structure exists.
Rejected:
H1/H2 — exhaustive matching produced no shared edge.
Surviving:
Mask-dependent/non-universal basin directions under tested geometry.
4. METHOD & EVIDENCE
Methods: Enumerated all 36 joint mask-6/mask-7 family permutations relative to mask 3;
compared three basin edges using absolute cosine similarity.
Sources/evidence:
K-039; K-044; K-046; K-047; Q021–Q023 endpoint chain.
Programs/workflows:
Q024_basin_matching_v1.py
Q024_basin_matching_v1_config.yml
Q024_tests_v1.py

BUBBLEVERSE Q JOURNALS
0.42
.github/workflows/q024-read-only-basin-matching-v1.yml
Tests: permutation completeness, sign invariance, mask/seed scope, zero-new-likelihood
gate, physical-overclaim gates, FINAL_RESULT_GATE.
5. KEY RESULTS
36/36 permutations tested.
Best candidate:
- Shared edges: 0/3
- Global median |cos| = 0.374489
- Minimum edge median = 0.316164
- Maximum shared-edge count across all candidates = 0
- Best-minus-permutation-median = 0.0
- New likelihood evaluations = 0
- FINAL_RESULT_GATE = PASS
Final result: Exhaustive permutation/sign-invariant matching does not recover a
reproducibly shared cross-mask basin direction.
Limitations: Endpoint-coordinate geometry only; no proof about
nonlinear/covariance/spectrum-space representations or physical cause.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed route:
“Universal basin direction hidden only by seed-family permutation.”
Mikami Graveyard:
CONN-Q024-SEED-PERMUTATION-RESCUE — REJECTED; all 36 mappings failed.
7. MODEL CHANGE
Before: Q023 non-universality constrained by possible seed-label mismatch.
After: Non-universality strengthened under exhaustive permutation/sign-invariant
matching.
Change: CONSTRAINED / strengthened.
Reason: No permutation produced a passing shared edge.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Known related commit:
B8e16629bbc6592ee11f0d90f78c887a913ac4c1 — workflow relocation only.
Parent provenance:
Q021 raw run 33882434170

BUBBLEVERSE Q JOURNALS
0.42
Q022 commit 16a7902c3be7d1967adaae9ee380baf0d17e903a
Q023 run 33913077353 / commit ea5af9a0b25090eb8472adb3c9574dcb4e1efe5c
Q024 exact Actions run / execution commit: NOT RECORDED.
Result:
R-Q024-EDE-FULLMF-BASIN-MATCHING-001
9. REPRODUCIBILITY
Checkout recorded code/backend; obtain Q021/Q022 endpoint artifacts; run Q024 workflow
with masks 3/6/7 and seeds 0/1/2; verify 36 permutations, zero new likelihood calls,
recorded cosine metrics and PASS gates.
10. CONCLUSION
Q024 strengthens Q023: stable optimizer basins exist, but their separation directions are
not reproducibly universal across masks 3, 6, and 7 under either fixed-lineage or
exhaustive permutation/sign-invariant matching. This remains internal computational
geometry, not evidence of a physical systematic or new physics.
11. NEXT-Q HANDOFF
Next Q: Q025
Question: Which likelihood components, spectra, frequency combinations, and parameter-
group interactions generate the strengthened mask dependence of the Q022 basin
geometry?
Reason: Simple label-permutation rescue is exhausted; the next informative target is the
likelihood structure producing the mask dependence.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No robust permutation/sign-invariant common basin direction was found.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Seed-permutation rescue rejected.
MODEL CHANGE SUMMARY: Q023 conclusion strengthened; Q022 remains intact.
REPRODUCIBILITY / GITHUB REFERENCES: Morfindien/Bubbleverse; files and provenance
above.
NEXT-Q HANDOFF: Q025 — likelihood/spectrum/frequency attribution.

BUBBLEVERSE Q JOURNALS
0.42
Q025
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q025
Date/time: 2026-09-04 23:08 CEST
Status: SUPPORTED
Question: Which likelihood components, spectra, frequency combinations, and parameter-
group interactions are responsible for the strengthened mask dependence of the stable
Q022 full-multifrequency basin geometries across masks 3, 6, and 7?
2. STARTING STATE
Model: MOD-EDE-N3; n_scf=3; frozen ”mwt5345/class_ede” commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Inherited: Q022 stable full-MF multibasins; Q023 non-universal basin directions; Q024
exhaustive relabelling failed to restore common directions.
Constraints: Masks 3/6/7 fixed; Q022 endpoints preserved; no optimization; no Q024 rerun;
primordial coordinates frozen within each mask; functional attribution ≠ physical
causality.
3. HYPOTHESES
Tested: universal parameter-group driver; universal spectrum/frequency driver;
foreground-only explanation; distributed covariance/interaction structure.
Rejected: universal single-driver and pure-foreground explanations.
Surviving: distributed, mask-dependent cosmology–nuisance compensation with
covariance-coupled multifrequency structure.
4. METHOD & EVIDENCE
Method: 8 fixed-vector parameter-block vertices per basin edge × 9 edges = 72 likelihood
evaluations, 0 optimizations; covariance/spectrum/multipole and Shapley/interaction
attribution.
Sources: Planck NPIPE/CamSpec context; Efstathiou et al. 2024 (arXiv:2311.00524);
Rosenberg et al. 2022 (arXiv:2205.10869); Efstathiou & Gratton (arXiv:1910.00483).
Program/workflow: ”q025_fullmf_component_attribution_v2.py”;
”q025_fullmf_component_attribution_v2_config.yml”; ”q025_tests_v2.py”;
”.github/workflows/q025-fullmf-component-attribution-v2.yml”.
5. KEY RESULTS
- Masks 3 and 7: cosmology dominates all three edge decompositions.

BUBBLEVERSE Q JOURNALS
0.42
- Mask 6: shared nuisance dominates all three; large cosmology×shared-nuisance
interactions ( 13.79, 10.65). ≈− −
- ”143×217” largest absolute spectrum term on 7/9 edges; ”143×143” on 2/9.
- TT generally largest observable contribution; strong signed covariance cancellation, often
concentrated at ℓ<1000.
Final result: Stable full-MF basin geometry is supported by distributed mask-dependent
compensation and covariance-coupled TT multifrequency structure, not one universal
component.
Limitations: Internal dependent Planck-likelihood reanalysis; no physical/systematic
causality established.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed: Q025 V1, run ”33917809217”, SHA ”470c11eafd7249d520c401c4a91ae7fd8fa6ede9”;
endpoint loader failed (”Q022_ENDPOINT_GATE=FAIL”), 0/72 evaluations, no scientific
result.
Graveyard: universal single parameter-group driver; universal single-spectrum driver;
pure-foreground explanation; independent-additive-component interpretation.
7. MODEL CHANGE
Before: full-MF basin directions known to be mask-dependent/non-universal.
After: their internal support is localized to mask-dependent cosmology–nuisance
compensation plus covariance-coupled multifrequency structure.
Change: CONSTRAINED / PRECISED.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Successful run: ”33918779905”
Head SHA: ”b2db6827b1caf5405e6a34bff221b6ae4813c1d0”
Artifact: ”q025-final-v2”, ID ”9954333941”, SHA-256
”104b584c9212a65e7f06cae64a732dac6f58b801cb8feec34c7f49d1bfddac0f”.
Provenance: Q021/Q022 endpoints Q023/Q024 geometry Q025 fixed-vector attribution; → →
same frozen Planck/CamSpec evidence chain.
9. REPRODUCIBILITY
Checkout recorded commits; obtain preserved Q021/Q022 parent outputs; run Q025 V2
workflow with frozen masks/model; verify 72/72 evaluations, 0 optimizer calls and all gates
PASS; compare ”q025-final-v2”.
10. CONCLUSION
Q025 explains the previously established mask dependence at the likelihood level: masks
3/7 are cosmology-dominated, while mask 6 is shared-nuisance-dominated, with strong

BUBBLEVERSE Q JOURNALS
0.42
covariance cancellation and recurring 143×217/143×143 TT structure. This is a numerical-
likelihood result, not evidence of calibration failure, bad data, or distinct physical
cosmologies.
11. NEXT-Q HANDOFF
Next Q: Q026
Why: Mask 6 is qualitatively different and its shared-nuisance dominance remains
unexplained.
Question: Can mask 6’s shared-nuisance-dominated geometry be localized to specific
nuisance parameters and covariance/frequency structures, or is it irreducibly distributed?
FINAL ANSWER: Distributed mask-dependent full-MF attribution with strong covariance-
coupled TT frequency structure.
MIKAMI UPDATE: Single-driver explanations killed.
MODEL CHANGE: Precised/constrained; no fundamental model reversal.
REPRODUCIBILITY: Run ”33918779905”, SHA ”b2db6827…”, artifact ”q025-final-v2”.
NEXT-Q: Q026 — localize mask-6 compensation structure.

BUBBLEVERSE Q JOURNALS
0.42
Q026
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q026
Date/time: 2026-09-04 ~23:49 CEST
Status: CONFIRMED
Question: Why does mask 6 become shared-nuisance dominated while masks 3 and 7
remain cosmology dominated, and can this be localized to specific nuisance coordinates,
cosmology–nuisance couplings, or CamSpec covariance/data-model structure without
assuming a systematic?
2. STARTING STATE
Model: MOD-EDE-N3; (nsc f=3); frozen ”class_ede” commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”; ”planck_NPIPE_highl_CamSpec.TTTEEE”.
Inherited: Q022 stable mixed basins; Q025: masks 3/7 cosmology dominated, mask 6
shared-nuisance dominated with strong TT multifrequency/covariance structure.
Constraint: Fixed validated endpoints; no optimizer; no Q024 permutation rerun;
functional diagnostics ≠ physical causality.
3. HYPOTHESES
Tested:
H1 generic shared-nuisance response.
H2 ( A pl anc k)-centered response.
H3 specific cosmology×nuisance coupling associated with mask-sensitive covariance
structure.
Rejected: Generic/equal nuisance explanation; calTE- or calEE-dominated explanation.
Surviving: ( A pl anc k)-centered mask-6 geometry, dominated by ( ωc d m× A pl anc k).
4. METHOD & EVIDENCE
Method: 252 fixed-vector likelihood evaluations across 9 basin edges; individual nuisance
switches plus all 18 cosmology×shared-nuisance pairs.
Sources: Planck/NPIPE/CamSpec; Q022/Q025 validated parents; Rosenberg et al. 2022
(arXiv:2205.10869); Efstathiou & Gratton (arXiv:1910.00483).
Program/workflow: ”q026_mask6_nuisance_localization_v1.py”; ”.github/workflows/q026-
mask6-nuisance-localization-v1.yml”; run ”33921255497”.
Tests: All mandatory gates PASS; ”FINAL_RESULT_GATE=PASS”; 252/252 finite evaluations;
0 optimizer evaluations; 0 Q024 reruns.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Mask-6 median absolute nuisance switches:
( A pl anc k=8.6626), (calTE=0.0239), (calEE=0.0374).
Strongest mask-6 pair interactions:
(ωc d m× A pl anc k=25.1681);
(H 0× A pl anc k=7.7736);
(f E D E× A pl anc k=4.7882).
Strongest edges 0–2 and 1–2 coincide with large cancelling TT
(143×143/143×217/217×217) covariance terms around (ℓ=600!−!999).
Final result: Mask 6 is not generically shared-nuisance dominated; its distinctive likelihood
geometry is predominantly ( A pl anc k)-centered, especially through ( ωc d m× A pl anc k).
Limitations: Local functional geometry only; no calibration/systematic/physical-causality
claim.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: None scientifically relevant in Q026.
Graveyard: Uniform shared-nuisance explanation; calTE-dominated; calEE-dominated;
equal cosmology×nuisance structure. Calibration-failure claim remains NOT ESTABLISHED.
7. MODEL CHANGE
Before: Mask 6 = shared-nuisance dominated.
After: Mask 6 = predominantly ( A pl anc k)-centered, strongest pair ( ωc d m× A pl anc k).
Change: MODIFIED / CONSTRAINED interpretation.
Reason: Q026 coordinate and pair localization.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commit: ”7cb4d98c01196c22b407b6f4fd4118179afea3de”
Run: ”33921255497”
Result: ”R-Q026-EDE-FULLMF-MASK6-COUPLING-001”
Artifact: ”q026-final-v1”; ID ”9955684272”; SHA-256
”fc1970c0e531a5a9157e2054aea91d54cbca9297a0599634710f2ceaa854cc87”.
9. REPRODUCIBILITY
Checkout recorded commit obtain validated Q022/Q025 parents run Q026 workflow → →
with frozen backend/likelihood verify 252 evaluations and mandatory gates compare → →
final artifact/result ID.

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q026 resolves the parameter-side origin of mask 6’s unusual basin attribution: the effect is
overwhelmingly ( A pl anc k)-centered, with (ωc d m× A pl anc k) the dominant local functional
interaction. The same strongest edges also contain extreme cancelling TT multifrequency
covariance structure near (ℓ=600!−!999), but causal direction remains unresolved.
11. NEXT-Q HANDOFF
Why: The bridge between parameter compensation and residual/covariance structure
remains unknown.
Next Q: Q027
Question: Can the mask-6 ( A pl anc k)–(ωc d m) compensation be traced primarily to residual-
vector changes, inverse-covariance weighting, their interaction, or broader mask-sensitive
CamSpec geometry?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Mask-6 shared-nuisance dominance localizes predominantly to ( A pl anc k),
especially (ωc d m× A pl anc k); no physical systematic established.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Generic/equal shared-nuisance, calTE-dominated and calEE-
dominated terminal explanations rejected.
MODEL CHANGE SUMMARY: Q025 block-level result retained but refined to ( A pl anc k)-
centered geometry.
REPRODUCIBILITY / GITHUB: Run ”33921255497”; commit ”7cb4d98…”; result ”R-Q026-EDE-
FULLMF-MASK6-COUPLING-001”.
NEXT-Q HANDOFF: Q027 — identify residual/covariance mechanism behind the localized
mask-6 geometry.

BUBBLEVERSE Q JOURNALS
0.42
Q027
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q027
Date/time: UNKNOWN / NOT RECORDED
Status: CONFIRMED
Question: Can the mask-6 ( A pl anc k)–(ωc d m) compensation identified in Q026 be traced to the
TT (143×143), (143×217), and (217×217), (ℓ=600 – 999) blocks, or is it distributed through
broader mask-sensitive geometry?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, (nsc f=3), frozen mwt5345/class_ede commit
5a131c91d657dd9a7c6364cc45b038710f8d0d97; CamSpec TTTEEE masks 3/6/7.
Inherited results: Q025 distributed covariance-coupled full-MF structure; Q026 strong
mask-6 ( A pl anc k)-centred coupling, strongest pair (ωc d m× A pl anc k).
Constraints: reuse Q022 endpoints; no reoptimization; preserve signed covariance
accounting.
3. HYPOTHESES
Tested:
H1: TT (ℓ=600 – 999) triad is the dominant/local mask-6 explanation.
H2: Interaction is distributed through broader residual/covariance geometry.
H3: Within-mask effect arises from residual changes under fixed precision.
Rejected: H1 — localization is similar across masks and tiny after precision weighting.
Surviving: H2/H3 — supported.
4. METHOD & EVIDENCE
Methods: 36 fixed-vector likelihood evaluations; residual vector ®, precision (P), (Pr),
signed pointwise and block decomposition.
Sources: K-039, K-044, K-048, K-049; CamSpec/NPIPE computational chain.
Programs/workflows: q027_residual_covariance_bridge_v1.py;
q027_residual_covariance_bridge_v1_config.yml; q027_tests_v1.py; q027-residual-
covariance-bridge-v1.yml.
Tests: Q026 pair reproduction; precision invariance; decomposition completeness; finite
metrics; cross-mask comparison; no-causal-overclaim gate.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Mask-6 median TT-triad shares: absolute pointwise 0.4445; residual (L2^2) 0.3018; ≈ ≈
precision-weighted residual (L2^2) 0.00232. ≈
Cross-mask absolute pointwise medians: mask3 0.444585; mask6 0.444548; mask7 0.444749.
Q026 pair reproduction max difference: 0.0.
Final result: DISTRIBUTED_BEYOND_TT600_999_TRIAD.
Limitations: no valid cross-mask precision swap; residual-vs-precision cross-mask
causation remains non-identified.
Contradictions: Earlier possibility that TT600–999 alone explained mask 6 was rejected.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: None scientifically required; no optimizer/sampler reruns.
Mikami Graveyard addition: “TT 143×143/143×217/217×217 at (ℓ=600 – 999) is a sufficient
local explanation of mask-6 coupling.” Killed by cross-mask localization and precision-
weighted result.
7. MODEL CHANGE
Before: Strong mask-6 ( A pl anc k)-centred geometry with possible TT600–999 localization.
After: Broader distributed mask-sensitive full-MF residual/covariance geometry.
Change: CONSTRAINED / MODIFIED.
Reason: Q027 localization decomposition.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: Q027 execution commit UNKNOWN / NOT RECORDED
Workflow: q027-residual-covariance-bridge-v1.yml
Programs: q027_residual_covariance_bridge_v1.py; q027_tests_v1.py
Outputs: q027_merged_v1.json; q027_tests_v1.json; q027_final_v1.json
Result ID: R-Q027-EDE-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-001
Run: Q027-FULLMF-RESIDUAL-COVARIANCE-BRIDGE-V1
FINAL_RESULT_GATE: PASS
9. REPRODUCIBILITY
Checkout frozen backend and recorded Q022/Q025/Q026 state; run Q027 workflow with
masks 3/6/7 and authoritative endpoints; reproduce 36 fixed evaluations; verify Q026 pair
difference 0.0 and all gates PASS.
10. CONCLUSION
The strong mask-6 ( A pl anc k×ωc d m) interaction is not sufficiently localized to the selected TT
(ℓ=600 – 999) triad. Within each mask, the identifiable mechanism is residual change under

BUBBLEVERSE Q JOURNALS
0.42
a fixed inverse covariance. The broader cross-mask split between residual/data structure
and precision/covariance structure remains unresolved.
11. NEXT-Q HANDOFF
Why another Q is required: Cross-mask residual-vs-precision attribution is still non-
identified.
Next Q: Q028
Next question: Can cross-mask non-universality be separated into residual/data-vector
versus mask-specific precision effects using a mathematically valid common-support
counterfactual construction?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: DISTRIBUTED_BEYOND_TT600_999_TRIAD.
Q-JOURNAL: This reconstruction.
MIKAMI GRAVEYARD UPDATE: TT600–999 triad as sufficient local explanation rejected.
MODEL CHANGE SUMMARY: Interpretation narrowed to broader distributed
residual/covariance geometry.
REPRODUCIBILITY / GITHUB REFERENCES: R-Q027-EDE-FULLMF-RESIDUAL-COVARIANCE-
BRIDGE-001; listed program/workflow/result files.
NEXT-Q HANDOFF: Q028 — valid common-support residual-vs-precision decomposition.

BUBBLEVERSE Q JOURNALS
0.42
Q028
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q028
Date/time: 2026-09-05 11:34 CEST
Status: CONSTRAINED
Question: Can the established cross-mask non-universality of the frozen MOD-EDE-N3 full-
MF CamSpec likelihood be separated into residual/data-vector effects versus mask-specific
inverse-covariance/precision effects using a mathematically valid common-support
counterfactual construction, without changing the physical model or reoptimizing the
authoritative Q022 endpoints?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3; frozen backend mwt5345/class_ede @
5a131c91d657dd9a7c6364cc45b038710f8d0d97; CamSpec TTTEEE.
Inherited results: Q022 stable multibasin endpoints; Q026 strong mask-6 A_planck-centred
coupling; Q027 residual change under fixed inverse covariance, but cross-mask residual-vs-
precision attribution unresolved.
Constraints: preserve Q022 endpoints/model/likelihood; no optimization, sampling or Q024
rerun; frozen Criterion B+ tolerance 2×10^-4.
3. HYPOTHESES
Tested:
H1: A valid common-support residual/precision separation exists.
H2: Edge-dependent precision prevents unique target-functional attribution.
H3: Precision variation materially drives the omega_cdm×A_planck cross-lineage
interaction.
Rejected: H2/H3 — admissible precision choices are functionally equivalent far below
tolerance.
Surviving: H1 — supported only for the frozen Q028 target functional/construction.
4. METHOD & EVIDENCE
Methods: exact labelled common support; Schur-valid quadratic action; factorial functional
F=q11 q10 q01+q00; cross-donor Criterion B+; signed two-factor Shapley. − −
Sources: K-039, K-044, K-048, K-049, K-046; same broad Planck/NPIPE/CamSpec evidence
family.

BUBBLEVERSE Q JOURNALS
0.42
Program/workflow: q028_common_support_counterfactual_v8.py;
q028_common_support_counterfactual_v8_config.yml; q028_tests_v8.py;
.github/workflows/q028-common-support-counterfactual-v8.yml.
Tests: 36 fixed-vector evaluations; 9 family + 9 precision jobs; Criterion B+ completeness;
common-support validity; Shapley closure; FINAL_RESULT_GATE.
5. KEY RESULTS
Common support: 9915/9915 = 1.0.
Global max precision edge-choice spread: 1.3457679415×10^-10 vs 2×10^-4 threshold.
Criterion B+: PASS for masks 3, 6, 7.
Precision-side Shapley: 0.0 in all 9 comparisons; residual side carries all non-negligible
target-functional differences.
Final result: VALID_COMMON_SUPPORT_SEPARATION.
Limitations: residual r=d m is not raw-data-only; result is non-causal, −
model/likelihood/functional conditional and not independent observational evidence.
Contradictions: None with Q019–Q027; Q028 V1/V2 interpretations superseded.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 bytewise criterion too strong; V2 state-level invariance mathematically
over-restrictive; V3 symmetry gate; V4 runner shutdown; V5 ell-band schema; V6
checkpoint naming; V7 missing classifier tolerance.
Mikami Graveyard additions: “materially different precision operators drive the Q028
target” — rejected by Criterion B+; state-level q-invariance as required criterion — rejected.
7. MODEL CHANGE
Before: cross-mask residual-versus-precision attribution non-identified.
After: target-functional attribution identified as residual-side under functionally equivalent
admissible precision choices.
Change: MODIFIED / CONSTRAINED.
Reason: Q028 V8 Criterion B+ + Shapley PASS.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Execution commit: 7f5d35efeb54b4a62d6dfb8f7074014b4fabc190
Run: 33957937309
Result: R-Q028-EDE-FULLMF-COMMON-SUPPORT-COUNTERFACTUAL-008
Artifact: q028-final-v8, ID 9967068363, SHA256
7dfbd1f27251ff311dd1de6118539dd691ab03d9afdb08539b3b13586c50d5af
Validation: FINAL_RESULT_GATE PASS.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
Checkout recorded commit; obtain frozen Q021/Q022/Q025/Q026/Q027 parents; run V8
workflow with frozen model/likelihood/endpoints; compare q028_merged_v8.json,
q028_tests_v8.json and q028_final_v8.json; apply Criterion B+ 2×10^-4 and Shapley ≤
closure 10^-8. ≤
10. CONCLUSION
Within the frozen MOD-EDE-N3 full-MF CamSpec construction, the cross-lineage
omega_cdm×A_planck target-functional difference can be validly separated: admissible
precision choices are functionally indistinguishable, while the difference resides on the
residual side. This does not identify whether the residual difference originates in data or
model predictions.
11. NEXT-Q HANDOFF
Why required: r=d m remains internally unresolved. −
Next Q: Q029
Next question: Can the Q028 residual-side target-functional differences be validly
separated into observed data-vector versus model-prediction contributions, including
cosmological, nuisance, foreground and calibration components?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Valid common-support separation; residual-side dominates, precision-side
= 0.0 for all 9 final comparisons.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Precision-driven Q028 target and required state-level
invariance killed.
MODEL CHANGE SUMMARY: Cross-mask attribution changed from non-identified to
residual-side identified for the frozen target functional.
REPRODUCIBILITY / GITHUB REFERENCES: Morfindien/Bubbleverse; commit 7f5d35ef…;
run 33957937309; V8 workflow/program/tests; artifact q028-final-v8.
NEXT-Q HANDOFF: Q029 — decompose the residual itself without reopening Q028
precision identifiability.

BUBBLEVERSE Q JOURNALS
0.42
Q029
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q029
Date/time: 2026-09-05 11:59 CEST
Status: CONFIRMED
Question: Within Q028’s exact 9915-row common support, can the residual-side ωc d m× A pl anc k differences be uniquely
separated into data-vector versus model-prediction
contributions, including cosmology, nuisance, foreground and calibration?
2. STARTING STATE
Model: MOD-EDE-N3; nsc f=3; frozen ”mwt5345/class_ede” commit
”5a131c91d657dd9a7c6364cc45b038710f8d0d97”; ”planck_NPIPE_highl_CamSpec.TTTEEE”.
Inherited:
- Q026: strongest mask-6 pair interaction = ωc d m× A pl anc k.
- Q028 V8: exact 9915/9915 support; residual-side dominates target-functional variation;
precision-side 0 for the defined target. ≈
Constraints: Q022 endpoints frozen; no reoptimization/sampling; preserve r=d −m; no
causal attribution.
3. HYPOTHESES
H1: Unique data/model decomposition exists.
H2: Exact interaction-preserving decomposition exists.
H3: Model term uniquely splits into cosmology/foreground/nuisance/calibration.
Rejected: H1, H3 — irreducible cross-terms prevent unique attribution.
Surviving: H2 — CONFIRMED.
4. METHOD & EVIDENCE
Method: Exact algebraic expansion of the Q028 factorial functional plus CamSpec
likelihood-semantics check.
T P (d −ms)
F=q11−q10−q01+q00,qs=(d −ms)
Sources: K-039, K-044, K-046, K-048, K-049. K-047 unresolved.
Programs/workflows: No new Q029 computation. Q028 V8 and Q027 validated outputs
inherited.
Tests: algebraic cancellation; cross-lineage interaction/path-independence test; model-
component additivity check.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
TPΔ
T Pm)
2m+Δ
2(m
F=−2d
And exactly:
T P d )=0.
2(d
Δ
Thus no standalone data-only term exists. Data enter through the data–model factorial
TPΔ
coupling −2d
2m.
Cross-lineage interaction:
T P( Δ
I D M=−2(d A−dB)
2mA−Δ
2mB).
If I D M ≠0, data/model attribution is path-dependent. Calibration is multiplicative, so
cosmology/calibration are likewise not uniquely additive.
Final result: Exact interaction-preserving decomposition exists; unique data-vs-model or
unique multicomponent attribution does not.
Limitations: functional, likelihood-construction-dependent, non-causal; no new
observational evidence.
Contradictions: None with Q028; Q028 interpretation is narrowed.
6. NEGATIVE RESULTS / MIKAMI
Killed:
- ”RESIDUAL = RAW DATA”
- unique data/model attribution
- unique cosmology/calibration attribution
- Shapley allocation as physical identification
Failed runs: None in Q029.
7. MODEL CHANGE
Before: Q028 established residual-side rather than precision-side dominance, but lower-
level residual attribution remained unresolved.
After: residual functional contains irreducible data–model and model–model interactions.
Change: PRÆCISERET / CONSTRAINED.
Reason: exact Q029 algebra.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Q027: run ”33924573651”, commit ”df03e30712690e61ff799558598405a22c0bacbb”.
Q028 V8: run ”33957937309”, commit ”7f5d35c0725530039162adfa4d71be288e8b4462”;
artifact ”q028-final-v8”, ID ”9967068363”, SHA-256
”7dfbd1f27251ff311dd1de6118539dd691ab03d9afdb08539b3b13586c50d5af”.

Q029: no new run/program; mathematical derivation from validated inherited state.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
1. Checkout frozen model/Q028 versions.
2. Preserve Q028 9915-row support and Q022 endpoints.
T P (d −ms).
3. Reconstruct qs=(d −ms)
4. Expand the four-state factorial combination algebraically.
T P d )=0 and the stated cross-interaction identity.
5. Verify Δ
2(d
10. CONCLUSION
Q029 establishes that Q028’s residual-side result cannot be promoted to a unique data-
driven, model-driven, cosmology-driven or calibration-driven explanation. The
mathematically identifiable structure is an exact data–model coupling plus a model-
quadratic response. Any finer two-way allocation requires convention and is not causal
identification.
11. NEXT-Q HANDOFF
Why: The exact two terms are identified mathematically but not yet quantified across the
nine mask × edge diagnostics.
Next Q: Q030
Question: Quantify the signed data–model coupling and model-quadratic terms on the
frozen Q028 common support, reusing existing checkpoints where possible.
FINAL ANSWER: Unique attribution rejected; exact interaction-preserving decomposition
confirmed.
MIKAMI GRAVEYARD: raw-data-side, unique data/model split, unique
cosmology/calibration split killed.
MODEL CHANGE: interpretation narrowed; physical model unchanged.
REPRODUCIBILITY: inherited Q027/Q028 validated GitHub chain; no Q029 run.
NEXT-Q: Q030 — numerical decomposition of the two exact surviving terms.

BUBBLEVERSE Q JOURNALS
0.42
Q030
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q030
Date/time: 2026-09-05 13:25 CEST
Status: CONFIRMED
Question: Using the exact 9915-row common support and frozen Q022 endpoints, can the
Q029 identity
TPΔ
T Pm)
2m+Δ
2(m
F=−2d
Be reconstructed for all nine mask×edge diagnostics, including signed terms and
spectrum/multipole structure, without imposing a causal allocation?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, nsc f=3; frozen mwt5345/class_ede commit ”5a131c9…”;
CamSpec TTTEEE.
Inherited:
- Q028 V8: exact 9915-row common support; SHA ”60881658…”; validated fixed precision
structure.
- Q029: exact decomposition exists, but unique data/model or cosmology/calibration
attribution is mathematically non-identifiable.
Constraints: Frozen Q022 endpoints; no reoptimization, sampling, Q024 rerun, causal
allocation, or tolerance rescue.
3. HYPOTHESES
Tested:
H1: Q029 identity is numerically reconstructible for all 9 diagnostics.
H2: Original 10
−8 validation gate is attainable with stable arithmetic.
H3: Interaction remains covariance-coupled and distributed in spectrum/ℓ space.
Rejected: Numerical precision floor above 10
−8; narrow TT600–999-only explanation;
unique causal allocation.
Surviving: Exact functional decomposition + Q029 non-identifiability; CamSpec-conditional
distributed geometry.
4. METHOD & EVIDENCE
Methods: Reused frozen Q022/Q028 objects; evaluated T D M, T M M, and F; spectrum/ℓ pair
decomposition; final stable factorial-bilinear precision audit.
Sources: K-039, K-044, K-046, K-048, K-049; Morfindien/Bubbleverse.

BUBBLEVERSE Q JOURNALS
0.42
Programs/workflows:
”q030_interaction_preserving_decomposition_v2.py”;
”q030_original_gate_precision_audit_v1.py”;
”.github/workflows/q030-original-gate-audit-finalization-r1.yml”.
Tests: 13/13 final mandatory tests PASS; original 10
−8 gates retained.
5. KEY RESULTS
- All 9 mask×edge diagnostics reconstructed.
- |T M M )>|T D M ) in 9/9, functional only.
- Largest totals: mask6 E02 F=−29.5462638258; E12 F=−25.1680892024.
- Dominant absolute spectrum pair: 143×217 217×217, 9/9. ↔
- Dominant absolute ℓ pair: 1500–2000 self-pair, 9/9.
- Strong signed covariance cancellation throughout.
- Final max identity error: 2.09×10
−13.
- Max group closure error: 5.48×10
−14.
- Max |Δ
2r )=4.55×10
2m+Δ
−13.
Final result: Q029’s exact decomposition is numerically realized and passes the original
Q030 validation contract.
Limitations: Frozen MOD-EDE-N3/CamSpec construction; no unique physical cause
identified.
Contradictions: None physical; Q028 provenance SHA misrecord corrected.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts:
- Q030 V1: wrong Q028 support SHA technical failure. →
- V2: scientific values produced, but original 10
−8 closure failed from cancellation-sensitive
arithmetic.
- V3: passed only after new 10
−7 validation config; retained as historical, not final.
Graveyard additions:
- Unique data/model causal split.
- Unique cosmology/calibration split.
- TT600–999-only explanation.
- Claim that V2 failure falsified Q029 identity.
7. MODEL CHANGE
Before: Exact Q029 identity mathematical but not yet fully validated numerically.
After: Exact identity numerically confirmed on all 9 frozen diagnostics; distributed
covariance structure quantified.

BUBBLEVERSE Q JOURNALS
0.42
Change: STRENGTHENED / PRECISED.
Reason: Stable original-gate audit PASS.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Key commits: ”c0d01b8…” (V2), ”4cbe1585…” (finalization).
Runs: ”33961469874”, ”33963221940”.
Final result: ”R-Q030-ORIGINAL-GATE-PRECISION-AUDIT-001”
Artifact: ”q030-original-gate-precision-audit-final-v1”, ID ”9968592047”, SHA256
”7685d769…”.
9. REPRODUCIBILITY
Checkout recorded commits obtain frozen Q022/Q028 inputs run recorded Q030 → →
workflows compare generated JSON/artifacts apply original → → 10
−8, 10
−11, and 2×10
−4
gates unchanged.
10. CONCLUSION
Q030 confirms that the Q029 interaction-preserving decomposition is numerically valid on
the frozen CamSpec system. The large mask6 structure consists of strongly cancelling
covariance-coupled terms; it cannot be uniquely assigned to data, model, cosmology,
calibration, or a physical systematic.
NEXT-Q HANDOFF
Why: Main remaining uncertainty is whether this detailed geometry is CamSpec-specific.
Next Q: Q031
Question: Does the Q030 spectrum/multipole interaction geometry persist under an
independently validated alternative Planck high-ℓ likelihood construction?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: CONFIRMED under frozen Q030 configuration.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Unique causal allocations and TT600–999-only explanation
remain dead.
MODEL CHANGE SUMMARY: Internal likelihood geometry strengthened/precised; no new
physics claim.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; runs ”33961469874”,
”33963221940”; final artifact above.
NEXT-Q HANDOFF: Q031 — cross-likelihood robustness.

BUBBLEVERSE Q JOURNALS
0.42
Q031
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q031
Date/time: 2026-09-05, successful run completed 18:54 UTC
Status: REJECTED
Question: Does the distributed, multibasin, mask-dependent, covariance-coupled n=3 EDE
geometry found in frozen Planck NPIPE/CamSpec survive materially under an independent
Planck PR4/NPIPE likelihood implementation?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; n_scf=3; active/constrained;
class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited results: Q021–Q030 established distributed primordial response, stable mixed
cosmology–nuisance CamSpec basins, no universal basin direction, distributed attribution,
ω_cdm×A_planck coupling, common-support separation, and exact validated factorial
geometry.
Constraint: test portability without changing frozen physics, retrospectively redefining
basin criteria, summing cross-likelihood objectives, or forcing nuisance equivalence.
3. HYPOTHESES
Tested:
H1: Q022-type stable multibasin geometry survives in independent HiLLiPoP.
H2: Geometry remains separated but fails reproducible stable-basin support.
H3: Implementation fails, leaving portability unresolved.
Rejected: H1 — stable_basin_count=0. H3 — implementation and validation passed.
Surviving: H2 — implementation-specific likelihood geometry; residual separated
endpoints remain.
4. METHOD & EVIDENCE
Method: HiLLiPoP PR4/NPIPE TTTEEE v4.3, same frozen n=3 backend; 9 mapped
multistarts + mandatory tighter refinement; frozen Q022 stability criterion Δobjective 0.50 ≤
and normalized RMS 0.10 with repeated support. ≤
Sources: HiLLiPoP/Planck PR4 literature; Tristram et al. 2024; Efstathiou, Rosenberg &
Poulin 2024; McDonough et al. 2024.
Program/workflow: q031_planck_portability_v1.py; .github/workflows/q031-planck-
portability-v4.yml.

BUBBLEVERSE Q JOURNALS
0.42
Tests: independent-implementation, completeness, multibasin, final-result/claim-boundary
validation.
5. KEY RESULTS
9/9 primary starts completed; 9/9 refinements completed.
Stable_basin_count=0.
MATERIAL_STABLE_MULTIBASIN_GATE=FAIL.
Direction gate=NOT_TESTABLE; downstream primordial/compensation gates=NOT_RUN by
preregistered stop logic.
Near-degenerate separated examples:
M3-S0 M7-S2: Δobjective=0.2335; RMS=3.4915. ↔
M6-S2 M7-S1: Δobjective=0.3803; RMS=7.8245. ↔
Final result: Q021–Q030 stable CamSpec geometry does not port to HiLLiPoP under the
frozen criterion.
Limitation: one independent likelihood tested; mechanism causing non-portability remains
unidentified.
Contradiction: none fundamental; CamSpec vs HiLLiPoP creates implementation-structure
tension.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: V1 environment/setup; V2 Python/cache configuration; V3 Q022
stage/refinement artifact collision. All technical, no scientific result.
Mikami Graveyard: “Cross-implementation Planck n=3 EDE likelihood geometry” —
rejected under Q031. Universal interpretation of Q021–Q030 deleted; internal CamSpec
results preserved.
7. MODEL CHANGE
Before: Q021–Q030 geometry potentially generalizable beyond CamSpec.
After: IMPLEMENTATION-SPECIFIC INTERNAL LIKELIHOOD GEOMETRY.
Change: CONSTRAINED / GENERALIZATION REJECTED.
Reason: validated independent HiLLiPoP portability failure.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Successful commit: ff621d6e0a425a976bb7a55f9194a0de8a87f18f
Workflow: q031-planck-portability-v4.yml
Run: 33975028436
Result: R-CASE031-EDE-PLANCK-PORTABILITY-001
Artifact: q031-final-v1, ID 9975019737
Validated file: q031_final_validated_v1.json

BUBBLEVERSE Q JOURNALS
0.42
HiLLiPoP commit: a09ddde3e7ce11df99f74685feb1f1764cafb251.
9. REPRODUCIBILITY
Checkout recorded commit; obtain frozen Q021/Q022 parents and HiLLiPoP PR4 data; run
V4 workflow with recorded backend/criteria; compare q031_final_validated_v1.json;
require the same frozen portability gates.
10. CONCLUSION
Q031 rejected cross-implementation portability of the stable Q022-type CamSpec basin
geometry. The internal Q021–Q030 calculations remain valid, but their scope is narrowed
to the frozen CamSpec implementation. No Planck systematic, calibration failure, EDE
falsification, or new physics was established.
11. NEXT-Q HANDOFF
Next Q: Q032
Reason: portability failure is established; its implementation-level cause is not.
Next question: Can the CamSpec–HiLLiPoP portability failure be localized to foreground
modelling, calibration/nuisance structure, covariance, frequency/support construction, or a
distributed interaction among them?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Portability rejected under the frozen Q031 test.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Universal cross-implementation geometry killed; internal
CamSpec geometry retained.
MODEL CHANGE SUMMARY: General Planck interpretation implementation-specific →
CamSpec geometry.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse; run 33975028436; commit
ff621d6e…; V4 workflow; validated result above.
NEXT-Q HANDOFF: Q032 — identify the cause of CamSpec–HiLLiPoP non-portability.

BUBBLEVERSE Q JOURNALS
0.42
Q032
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q032
Date/time: 2026-09-06, final result; exact completion time not independently recorded here
Status: CONFIRMED
Question: Can the CASE-031 portability failure be localized to one or a small preregistered
set of differences between the frozen Planck NPIPE/CamSpec full-multifrequency likelihood
and HiLLiPoP PR4/NPIPE, or does the loss of stable multibasin structure remain distributed
across implementation changes?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; n_scf=3; mwt5345/class_ede
5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Inherited: Q022 historical stable CamSpec multibasin classification; CASE-031 HiLLiPoP
portability failure (st abl eba sinc ount=0).
Constraints: same model/priors/basin thresholds; 9 starts M3/M6/M7; no new seeds; no
Q024/Q030 reruns; no causal A_planck interpretation.
3. HYPOTHESES
Tested:
H1: removed TT SUPPORT causes loss.
H2: TE or EE causes loss.
H3: a small combination of SUPPORT/TE/EE restores stable geometry.
Rejected: H1–H3; no single, pairwise, or full three-sector restoration recovered stable
multibasin structure.
Surviving: broader likelihood/execution-semantics dependence.
4. METHOD & EVIDENCE
Method: common-support bridge followed by corrected exact-scalar-start CamSpec add-
back hierarchy: SUPPORT, TE, EE all pairs FULL_NATIVE. → →
Sources: K-044 CamSpec PR4; K-046 Cobaya 3.5.6 technical implementation; HiLLiPoP v4.3
technical source.
Programs/workflows: q032_exact_start_addback_v4.py; .github/workflows/q032-exact-start-
addback-v4.yml.
Run: GitHub Actions 34015845246.
Tests: exact scalar reference/start provenance; covariance selection; finite likelihood;
completeness; globality; interpretation; FINAL_RESULT_GATE.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Exact-start TT3 baseline: stable_basin_count=0.
SUPPORT, TE, EE: all 0.
SUPPORT+TE, SUPPORT+EE, TE+EE: all 0.
FULL_NATIVE SUPPORT+TE+EE: 0.
Final result:
NO_CLEAN_LOCALIZATION_WITHIN_TESTED_CAMSPEC_INFORMATION_SECTORS.
Limitations: methodological likelihood geometry only; does not identify
physical/systematic cause or confirm/falsify EDE.
Contradiction: historical Q022 stable classification is not reproduced under genuine scalar
exact-start semantics.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: Q032 V1 nuisance leakage technical failure; Q032 V3 optimizer failure →
plus incorrect non-scalar start semantics no scientific result. →
Graveyard: clean SUPPORT-only, TE-only, EE-only, pairwise, and three-sector restoration
explanations killed. V2 claim that removed information was materially required is
superseded.
7. MODEL CHANGE
Before: historical CamSpec geometry treated as stable multibasin, with CASE-031 showing
non-portability.
After: historical endpoint geometry retained, but stable-basin interpretation is execution-
semantics dependent; no small CamSpec sector explains portability loss.
Change: MODIFIED / CONSTRAINED.
Reason: Q032 V4 exact-start full-native result.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
V4 execution HEAD: fbde93aee01ec3bed183207518ff315c96a45c3c
Workflow: .github/workflows/q032-exact-start-addback-v4.yml
Program: q032_exact_start_addback_v4.py
Result: R-Q032-EDE-CAMSPEC-ADDBACK-004
Run: 34015845246
Provenance: Q022 endpoint vectors + frozen CamSpec/model configuration; V4 corrected
Cobaya refs to literal scalar starts.
9. REPRODUCIBILITY
Checkout recorded commit obtain frozen inputs/Q022 vectors run V4 workflow → →
unchanged compare baseline/tier/control outputs apply basin criteria Δobjective 0.50, → → ≤
RMS 0.10, support 2 and mandatory gates. ≤ ≥

BUBBLEVERSE Q JOURNALS
0.42
10. CONCLUSION
Q032 found no clean localization of the CASE-031 portability failure to SUPPORT, TE, EE, or
their combinations. Even full-native CamSpec remains non-stable under corrected exact-
start semantics. The historical geometry is therefore best treated as likelihood/execution-
dependent endpoint geometry, not an execution-invariant stable-basin property.
11. NEXT-Q HANDOFF
Why: determine whether launch/reference semantics alone explain the Q022 Q032 ↔
difference.
Next Q: Q033
Question: Under frozen full-MF CamSpec MOD-EDE-N3, can the historical Q022 stable
classification versus Q032 V4 non-stability be explained by launch-point/reference-
distribution semantics alone with all other components matched?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No clean small-sector localization; execution semantics materially matter.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: SUPPORT/TE/EE localization routes killed.
MODEL CHANGE SUMMARY: Q022 stable-basin interpretation constrained to historical
execution semantics.
REPRODUCIBILITY / GITHUB: R-Q032-EDE-CAMSPEC-ADDBACK-004, run 34015845246,
HEAD fbde93a….
NEXT-Q HANDOFF: Q033 — isolate launch/reference semantics.

BUBBLEVERSE Q JOURNALS
0.42
Q033
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q033
Date/time: 2026-09-06 21:45 CEST
Status: CONFIRMED
Journal type: RETROSPECTIVE RECONSTRUCTION
Reconstructed on: 2026-09-08
Question: Can Q022’s stable-multibasin versus Q032 V4’s non-stable FULL_NATIVE result be
explained by launch/reference-distribution semantics alone?
2. STARTING STATE
Model: MOD-EDE-N3; (nsc f=3); frozen ”mwt5345/class_ede” commit ”5a131c91…”.
Inherited: Q022 ”STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE”;
Q032 V4 ”stable_basin_count=0”, ”NO_CLEAN_LOCALIZATION…”.
Constraint: Preserve model, likelihood, numerical settings and historical execution; test
only launch/reference semantics.
3. HYPOTHESES
H1 / HYP-Q033-A: Q022 used non-scalar refs while Q032 used scalar refs.
H2 / HYP-Q033-B: Launch semantics are insufficient; another implementation difference
exists.
Rejected: H1 — historical runtime reconstruction showed Q022 refs were already scalar.
Surviving: H2 — strengthened.
4. METHOD & EVIDENCE
Method: Source/provenance audit of Q019 Q021 Q022 versus Q032 V4; no new likelihood → →
optimization.
Programs: ”q033_launch_semantics_protocol_audit_v2.py”; config/source-lock/tests;
workflow ”.github/workflows/q033-launch-semantics-protocol-audit-v2.yml”.
Evidence: Q022 run ”33902262660”; Q032 V4 run ”34015845246”; Cobaya 3.5.6 semantics;
frozen historical source blobs.
5. KEY RESULTS
- Q022 sampled non-primordial refs: scalar before/after recentering.
- Q032 V4 sampled refs: scalar.
- Remaining sampled-set difference: Q032 additionally samples ”n_s”, ”logA”, ”tau_reio”;
Q022 freezes them.
- Final result: ”LAUNCH_REFERENCE_SEMANTICS_ALREADY_IDENTICAL_NOT_CAUSAL”.

BUBBLEVERSE Q JOURNALS
0.42
Limit: Cause of Q022/Q032 discrepancy remains unresolved.
Contradiction: Stable Q022 versus non-stable Q032 remains a technical
parameterization/implementation tension, not a physical anomaly.
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q033 V1 preflight: ”NONSCALAR_HISTORICAL_REFERENCE_GATE=FAIL”; no
scientific likelihood result.
Graveyard: HYP-Q033-A and planned 18-job distribution-vs-scalar campaign — killed
because the proposed historical distribution arm never existed.
7. MODEL CHANGE
Before: Q022/Q032 difference partly attributed to launch/reference semantics.
After: That explanation removed; ”D-Q033-REMAINING-001” registered: frozen vs sampled
primordial block.
Change: Technical interpretation corrected; physical EDE/H ₀ conclusions unchanged.
8. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Q022 commit: ”16a7902c…”
Q032 commit: ”fbde93aee…”
Q033 files added: ”b03a1ac5…”; workflow placement ”614b227c…”
Result: ”R-Q033-EDE-LAUNCH-SEMANTICS-AUDIT-002”
Q033 GitHub run ID: NOT RECORDED IN SUPPLIED FINAL ARTIFACT.
9. REPRODUCIBILITY
Checkout recorded versions obtain Q022/Q032 artifacts run Q033 V2 audit with frozen → →
source lock verify scalar-ref identity and sampled-set delta require → →
”FINAL_RESULT_GATE=PASS”.
10. CONCLUSION
NO. Launch/reference representation cannot explain the Q022/Q032 classification
difference because both executed paths used scalar pointlike refs. The smallest identified
remaining difference is whether ”n_s”, ”logA”, ”tau_reio” are frozen or sampled.
11. NEXT-Q HANDOFF
Next Q: Q034
Question: Under otherwise matched FULL_NATIVE CamSpec conditions, does freezing
versus sampling ”n_s”, ”logA”, ”tau_reio” reproduce the stable-versus-non-stable
classification difference?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: NO — launch/reference semantics were already identical.
Q-JOURNAL: This entry.

BUBBLEVERSE Q JOURNALS
0.42
MIKAMI GRAVEYARD UPDATE: HYP-Q033-A + unnecessary 18-job V1 route killed.
MODEL CHANGE SUMMARY: Launch-semantics explanation removed; frozen-vs-sampled
primordial block becomes next candidate.
REPRODUCIBILITY / GITHUB: Repo, commits, workflow and result Ids above.
NEXT-Q HANDOFF: Q034 tests ”n_s/logA/tau_reio” freeze versus sampling.

BUBBLEVERSE Q JOURNALS
0.42
Q034
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q034
Date/time: 2026-09-06–07
Status: CONSTRAINED
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:40 CEST
Question: Does fixing ns,log A ,τ r eio in the later full-native CamSpec construction restore the
stable multibasin structure reported historically in Q022?
2. STARTING STATE
Model entering Q: MOD-EDE-N3 / ACTIVE, CONSTRAINED / not established new physics.
Inherited:
- Q032 V4 FULL_NATIVE: stable_basin_count = 0.
- Q033: scalar-vs-distribution launch semantics rejected; fixed-vs-sampled primordial block
remained candidate difference.
Constraint: Change only primordial fixed/sampled status; preserve backend, likelihood
construction, starts, optimizer and classifier.
3. HYPOTHESES
H1: Primordial freezing restores stable basins.
H2: It does not.
Rejected: H1.
Surviving: H2 under the later common-geometry classifier.
4. METHOD & EVIDENCE
Method: Artifact-locked matched isolation. Q032 FULL_NATIVE sampled control reused;
Q034 fixed ns,log A ,τ r eio and repeated required refinement.
Primary evidence: Morfindien/Bubbleverse; Q032 V4 artifacts; frozen mwt5345/class_ede
commit ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”.
Programs/workflows:
”q034_primordial_freeze_isolation_v1.py”
”q034_primordial_freeze_isolation_v1_config.yml”
”.github/workflows/q034-primordial-freeze-isolation-v1.yml”
Run: GitHub Actions ”34059649759”, head ”8b8035795a9e6064583379afb8663cdc28961764”.
5. KEY RESULTS
- Sampled Q032 control: stable_basin_count = 0.

BUBBLEVERSE Q JOURNALS
0.42
- Frozen Q034 arm: stable_basin_count = 0; stable_multibasin = false.
- After refinement: 9 singleton clusters, not repeated stable basins.
Final result: Freezing the primordial block is insufficient to restore stable multibasin
structure under the later classifier.
Limitation: Historical Q022 used a different basin classifier; global Q022 Q034 ↔
comparison therefore remains unresolved.
Contradiction: Historical Q022 “stable” and later “non-stable” labels are not classifier-
equivalent.
6. NEGATIVE RESULTS / MIKAMI
Failed hypothesis: Fixed-vs-sampled primordial parameters alone explain the discrepancy.
Graveyard: ”D-Q033-REMAINING-001” — rejected as sufficient under the Q031/Q032/Q034
common-geometry classifier.
7. MODEL CHANGE
Before: Primordial parameterization remained leading unresolved implementation
difference.
After: Insufficient under later classifier; classifier semantics become conclusion-critical.
Change: CONSTRAINED.
Reason: Frozen arm still produced zero stable basins.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: ”8b8035795a9e6064583379afb8663cdc28961764”
Workflow: ”q034-primordial-freeze-isolation-v1.yml”
Artifact: ”q034-final-v1”, ID ”9998302123”
SHA-256: ”0df519645906dfaaf3b270d9791a74c0f33f25e9fdcfa8ca344ad2add70f8a87”
9. REPRODUCIBILITY
Checkout recorded commits obtain Q032 decisive artifacts run Q034 workflow with → →
frozen primordial coordinates verify nine completed/refined endpoints apply identical → →
later graph-classifier thresholds and compare final artifact.
10. CONCLUSION
Q034 rejects primordial freezing as a sufficient explanation within the later classifier. It
does not invalidate Q022, Q032, or Q034 raw results. The remaining discrepancy is
methodological because Q022 and Q031–Q034 used different basin-classification
definitions.
11. NEXT-Q HANDOFF
Next Q: Q035

BUBBLEVERSE Q JOURNALS
0.42
Why: Determine whether the stable/non-stable discrepancy survives use of identical
classifiers.
Next question: When the decisive Q022, Q032 V4 FULL_NATIVE and Q034 frozen endpoint
sets are evaluated under both classifier definitions, does the reported discrepancy survive
classifier harmonization?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: Primordial freezing does not restore stable basins under the later
classifier.
Q-JOURNAL: This record.
MIKAMI GRAVEYARD UPDATE: Fixed-vs-sampled primordial block killed as sufficient
explanation under later classifier.
MODEL CHANGE SUMMARY: MOD-EDE-N3 unchanged physically; methodological
interpretation constrained.
REPRODUCIBILITY / GITHUB: Run ”34059649759”; head ”8b803579…”; artifact ”q034-final-
v1”.
NEXT-Q HANDOFF: Q035 — classifier harmonization.

BUBBLEVERSE Q JOURNALS
0.42
Q035
BUBBLEVERSE — Q-JOURNAL
Q-ID: Q035
Date/time: 2026-09-08 20:42 CEST
Status: CONFIRMED
Question: When the same decisive Q022, Q032 V4 FULL_NATIVE and Q034 frozen-
primordial endpoints are evaluated under both the historical Q022 classifier and later
Q031/Q032 classifier, does the reported stable/non-stable discrepancy survive
harmonization?
1. STARTING STATE
Model: MOD-EDE-N3; n_scf=3; class_ede ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”;
active/constrained, not established new physics.
Inherited: Q022 = historically STABLE_MULTIBASIN; Q032/Q034 = non-stable under later
common-geometry classifier. Q033 rejected launch/reference semantics as cause.
Constraint: Existing endpoints only; no new likelihood, optimization, sampling, seeds,
thresholds or physics changes.
2. HYPOTHESES
H1: Discrepancy survives same-classifier comparison. REJECTED.
H2: Classifier semantics materially explain discrepancy. CONFIRMED.
H3: Primordial freeze/sample difference is required explanation. REJECTED as
necessary/sufficient.
3. METHOD & EVIDENCE
Deterministic artifact-only cross-classification of the same Q022/Q032/Q034 endpoint sets
with both source-locked classifier definitions.
Evidence: Q022 run ”33902262660”; Q032 run ”34015845246”; Q034 run ”34059649759”.
Programs: ”q022_globality_continuation_v2.py”; ”q031_planck_portability_v1.py”;
”q032_planck_tt3pair_bridge_v2.py”; ”q035_classifier_harmonization_v1.py”.
Tests: endpoint completeness; reference replay; historical-all-stable; later-all-nonstable; all-
sets-flip; same-classifier-discrepancy-removed; physical-safety; FINAL_RESULT_GATE.
4. KEY RESULTS
Historical Q022 classifier: Q022/Q032/Q034 = STABLE.
Later common-geometry classifier: Q022/Q032/Q034 = NON-STABLE.
Thus both same-classifier cross-case discrepancies = FALSE and all endpoint sets flip
together with classifier choice.
Final result:
”CLASSIFIER_SEMANTICS_MATERIALLY_EXPLAINS_REPORTED_DISCREPANCY”.

BUBBLEVERSE Q JOURNALS
0.42
Limitations: Does not determine which classifier is physically preferable; does not establish
identical raw geometry, Planck systematics, EDE evidence/falsification or new physics.
Contradiction discovered: CASE-031 negative portability interpretation is weakened
because Q022 also fails its stable-basin gate under the same later classifier.
5. NEGATIVE RESULTS / MIKAMI
Original Q035 GitHub workflow failed with ”FileNotFoundError” from Q022 artifact path
layout; technical failure only, no scientific evidence.
Graveyard: same-classifier assumption; primordial freeze/sample as necessary/sufficient
cause; interpretation that Q022 stable Q032/Q034 non-stable demonstrated →
disappearance of physical basin structure.
6. MODEL CHANGE
Before: Q022 stable vs later non-stable treated as potentially genuine cross-case geometry
change.
After: Stable/non-stable label explicitly classifier-dependent; raw endpoints retained.
CASE-031 portability conclusion reopened.
Change: Methodological interpretation modified; physical MOD-EDE-N3/H ₀ status
unchanged.
7. GITHUB / PROVENANCE
Repo: ”Morfindien/Bubbleverse”
Commits: Q022 ”16a7902…”; Q031 ”ff621d6…”; Q032 ”fbde93a…”; Q034 ”8b80357…”; Q035
program ”b1166e8…”; Q035 V2 workflow ”e12bab3…”.
Workflow: ”.github/workflows/q035-classifier-harmonization-v2.yml”
Outputs: ”q035_classifier_crosswalk_v1.json/.csv”, ”q035_tests_v1.json”, source-lock/config
files.
Note: Successful Q035 V2 Actions run ID NOT RECORDED / NOT AVAILABLE.
8. REPRODUCIBILITY
Checkout recorded versions obtain authoritative Q022/Q032/Q034 artifacts run Q035 → →
crosswalk unchanged reproduce both classifier outputs require recorded gates and → →
final classification. No endpoint rounding or threshold tuning.
9. CONCLUSION
The former Q022-versus-Q032/Q034 stable/non-stable discrepancy disappears when
classifier choice is controlled. The endpoints remain valid; the basin label is not classifier-
invariant.
10. NEXT-Q HANDOFF
Next: Q036 — HIGH

BUBBLEVERSE Q JOURNALS
0.42
Question: Under identical Q031 common coordinates/scales and without binary stable
labels, do Q022 CamSpec and CASE-031 HiLLiPoP endpoints show a material reproducible
geometric difference supporting implementation-specific non-portability?
Start motor: NUMERICAL / HPC / MOTOR-BUILDER; preferably artifact-only.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No; classifier semantics materially explain the reported discrepancy.
Q-JOURNAL: This entry.
MIKAMI: Same-classifier assumption and freeze/sample global explanation retired.
MODEL CHANGE: Basin ontology classifier-dependent; physical model unchanged. →
REPRODUCIBILITY: ”Morfindien/Bubbleverse”, sources/runs/commits above.
NEXT-Q: Q036 — harmonized CamSpec–HiLLiPoP raw-geometry portability test.

BUBBLEVERSE Q JOURNALS
0.42
Q036
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08 20:43 CEST
1. IDENTITY
Q-ID: Q036
Date/time: 2026-09-07 09:44 CEST
Status: CONFIRMED
Question: Do Q022 CamSpec and CASE-031 HiLLiPoP endpoints show a material,
reproducible difference under the same Q031 common coordinates/scales when stable/non-
stable labels are not the sole discriminator?
2. STARTING STATE
Model entering Q: MOD-EDE-N3; ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW
PHYSICS.
Inherited:
Q035: classifier semantics explain the former stable/non-stable discrepancy.
Q022 CamSpec + CASE-031 HiLLiPoP validated endpoint sets.
Constraints: Seven Q031 common coordinates; locked scales; threshold 0.10; no cross-
likelihood χ²/objective subtraction or summation; no new likelihood/optimizer runs.
3. HYPOTHESES
Tested:
H1: Material continuous geometry difference survives.
H2: Difference disappears under common geometry.
H3: Classifier semantics explain the entire portability signal.
Rejected: H2/H3 — continuous location and shape differences remain large.
Surviving: H1 — CONFIRMED within tested geometry.
4. METHOD & EVIDENCE
Method: Deterministic artifact-only comparison of 9 matched endpoints plus 36 internal
pairwise distances.
Evidence: Q022 run 33902262660; CASE-031 run 33975028436; Q035 classifier
harmonization.
Program: q036_endpoint_geometry_portability_v1.py
Workflow: .github/workflows/q036-endpoint-geometry-portability-v5.yml
Authoritative run: 34105942065
Tests: identity/provenance; common-coordinate/scale lock; finite results; permutation
invariance; Q031 replay; decision replay; no-cross-likelihood-objective gate.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Matched median RMS = 2.3623; 9/9 > 0.10.
Pairwise median drift = 2.2590; 36/36 > 0.10.
Centroid shift = 1.5371.
Q031 replay error = 8.88×10⁻¹⁶.
FINAL_RESULT_GATE = PASS.
Final result: MATERIAL_REPRODUCIBLE_COMMON_GEOMETRY_DIFFERENCE.
Limitations: Does not identify the cause, a physical Planck systematic, preferred likelihood,
or evidence for/against EDE. CamSpec/HiLLiPoP share Planck information.
Contradictions: None with Q035; Q035 concerns classifier labels, Q036 continuous
geometry.
6. NEGATIVE RESULTS / MIKAMI
Failed attempt: Q036 V4 failed provenance gate from one incorrect artifact digest; technical
only, superseded by V5.
Graveyard additions:
“No material CamSpec–HiLLiPoP geometry difference” — rejected.
Stable/non-stable label as sole portability evidence remains dead from Q035.
7. MODEL CHANGE
Before: CASE-031 portability interpretation weakened after Q035.
After: NARROWED_IMPLEMENTATION_SPECIFIC_NON_PORTABILITY_REHABILITATED.
Change: MODIFIED / REFINED.
Reason: Continuous common-geometry difference survives classifier harmonization.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Q036 execution commit: 095f90565cf694a7c3383d1fbe736707ab187751
Parent commits: Q022 16a790…; Q031 ff621d…
Workflow: q036-endpoint-geometry-portability-v5.yml
Outputs: q036-final-v1, q036-tests-v1, q036-return-handoff-v1, q036-run-manifest-v1.
Provenance: Existing validated Q022/Q031 artifacts only; no new likelihood evaluations.
9. REPRODUCIBILITY
Checkout recorded commits obtain locked Q022/Q031 artifacts run Q036 V5 workflow → →
compare outputs with q036-final-v1 apply locked 0.10 location/shape criteria. → →
10. CONCLUSION
Q036 confirms a large reproducible CamSpec–HiLLiPoP endpoint-geometry difference
under identical normalized coordinates/scales. Q035 remains correct: the old binary
classifier argument was invalid, but continuous non-portability survives.

BUBBLEVERSE Q JOURNALS
0.42
11. NEXT-Q HANDOFF
Why: Cause of the implementation-dependent geometry remains unresolved.
Next Q: Q037
Question: Does the same material continuous geometry difference survive when Q032’s
exact TT common-support CamSpec/HiLLiPoP endpoints are compared using the Q036
metric?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: YES — material continuous common-geometry difference confirmed.
Q-JOURNAL: This entry.
MIKAMI: No-difference route rejected; classifier-only portability route remains dead.
MODEL CHANGE: CASE-031 narrowed non-portability rehabilitated.
REPRODUCIBILITY: Q036 V5, run 34105942065, listed commits/artifacts.
NEXT-Q: Q037 — common-support replay.

BUBBLEVERSE Q JOURNALS
0.42
Q037
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q037
Date/time: 2026-09-07, CEST
Status: SUPPORTED
Question: When Q032’s validated CamSpec/HiLLiPoP exact-TT common-support endpoints
are tested with Q036’s continuous seven-coordinate geometry, Q031 locked scales and 0.10
threshold, does the material location/shape difference persist?
2. STARTING STATE
Model: MOD-EDE-N3; ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW PHYSICS.
Inherited: Q032 exact-TT matched endpoints; Q035 classifier discrepancy resolved; Q036
continuous geometry difference established.
Constraint: Artifact-only deterministic replay; same 7 coordinates/scales/threshold; no new
likelihood/optimizer execution.
3. HYPOTHESES
H1: Exact matched TT support removes the geometry difference.
H2: Difference persists under matched TT support.
H3: Evidence is technically inconclusive.
Rejected: H1, H3.
Surviving: H2 — supported.
4. METHOD & EVIDENCE
Method: Compare 9 paired CamSpec/HiLLiPoP endpoints in normalized 7-D geometry; test
matched displacement, centroid and pairwise-shape drift.
Evidence: Q032 authoritative endpoints, run 33994305721, commit
”4dc873a5e880d40858d831a3b421456728f0c032”.
Program: ”q037_common_support_endpoint_geometry_v1.py” (”Q037-TTGEOM-V1”)
Workflow: ”.github/workflows/q037-common-support-endpoint-geometry-v1.yml”
Tests: finite/replay, permutation invariance, common-support identity, locked-scale identity,
threshold and preservation gates.
5. KEY RESULTS
Matched displacement: median 2.93179, max 5.22954, 9/9 >0.10.
Centroid displacement: 0.83115.
Pairwise drift: median 1.63679, max 4.75557, 36/36 >0.10.
Replay max absolute difference: 0.0; FINAL_RESULT_GATE: PASS.

BUBBLEVERSE Q JOURNALS
0.42
Final result: The material CamSpec–HiLLiPoP geometry difference persists on exact
matched TT support.
Limitation: No causal implementation component identified; shared Planck PR4/NPIPE data
are not independent observations.
Contradiction: None; Q037 narrows Q036.
6. NEGATIVE RESULTS / MIKAMI
Failed scientific attempts: None recorded. Earlier repository-registration 403 was technical
and later superseded.
Graveyard: “Unequal TT support is sufficient/primary explanation” — rejected for the
tested bridge because the difference survives exact common support.
7. MODEL CHANGE
Before: C-036-IMPL active; TT-support mismatch remained plausible.
After: C-036-IMPL strengthened; tested TT-support mismatch weakened as primary cause.
Change: CONSTRAINED.
Reason: 9/9 matched and 36/36 pairwise differences remain material.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Commits: ”9ff5f29d6ae1f5f5f702ccb98e034fb1075326ba”;
”c49d9885a5bf1e290f4b42f15c59d228c7c036cf”
Result: ”R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001”; ”q037_final_v1.json”
GitHub scientific run ID: NOT RECORDED.
Provenance: Deterministic replay of Q032 validated endpoints; no new physics execution.
9. REPRODUCIBILITY
Checkout recorded commits obtain Q032 artifacts run Q037 workflow/program → → →
compare with ”q037_final_v1.json” require same locked geometry and 0.10 criterion plus →
FINAL_RESULT_GATE PASS.
10. CONCLUSION
Exact matching of TT information support does not remove the CamSpec–HiLLiPoP
endpoint-geometry difference. This strengthens an unresolved implementation-level
discrepancy but establishes no physical Planck systematic, EDE detection/falsification, H₀
change or new physics.
11. NEXT-Q HANDOFF
Next Q: Q038
Question: Is the surviving common-support geometry difference concentrated in a
reproducible minimal subset of the seven coordinates, or distributed across several
coordinates?

BUBBLEVERSE Q JOURNALS
0.42
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: YES — the material geometry difference persists under exact matched TT
support.
Q-JOURNAL: This record.
MIKAMI: TT-support mismatch rejected as sufficient/primary explanation for the tested
discrepancy.
MODEL CHANGE: C-036-IMPL strengthened/constrained; cause unresolved.
REPRODUCIBILITY: Q032 run 33994305721 + Q037 program/workflow/commits above.
NEXT-Q: Q038 — coordinate localization.

BUBBLEVERSE Q JOURNALS
0.42
Q038
BUBBLEVERSE — Q-JOURNAL
JOURNAL TYPE: RETROSPECTIVE RECONSTRUCTION
RECONSTRUCTED ON: 2026-09-08
1. IDENTITY
Q-ID: Q038
Date/time: 2026-09-07 13:48 CEST
Status: CONFIRMED
Question: When Q037’s paired CamSpec/HiLLiPoP exact-common-support endpoints are
decomposed coordinate-by-coordinate under the seven Q031 locked scales, is the surviving
implementation-geometry difference concentrated in a reproducible minimal subset or
distributed across several coordinates?
2. STARTING STATE
Model: MOD-EDE-N3; nsc f=3; ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW PHYSICS.
Frozen ”mwt5345/class_ede” commit ”5a131c91…”.
Inherited: Q035 removed classifier semantics as a valid geometry discriminator; Q036
established a material continuous implementation difference; Q037 showed exact TT
common support does not remove it.
Constraints: Same seven Q031 coordinates/scales; no new
likelihood/CLASS/optimizer/sampler runs; no cross-likelihood objective arithmetic; causal
attribution forbidden.
3. HYPOTHESES
Tested:
H1: discrepancy concentrated in 2 coordinates. ≤
H2: discrepancy distributed across 3 coordinates. ≥
H3: apparent localization fails robustness tests.
Rejected: H1 — no 1-, 2-, or 3-coordinate subset met the preregistered joint criterion.
Surviving: H2 — distributed multivariate geometry.
4. METHOD & EVIDENCE
Deterministic artifact-only decomposition of validated Q037 endpoints. All 127 non-empty
subsets tested in matched-location, centroid and pairwise-shape channels; full capture
0.80; leave-one-label-out 0.70 with 8/9 passes. ≥ ≥ ≥
Primary evidence: Q032/Q037 endpoint artifacts; CamSpec/HiLLiPoP Planck PR4/NPIPE
methodology (K-044, K-049; comparison K-045/K-052).
Program/workflow: ”q038_coordinate_localization_v1.py”; ”.github/workflows/q038-
coordinate-localization-v1.yml”.
GitHub run: ”34121000822”; head ”02ddda7c13a53cd7ad20880bf527a86e17ac4d79”.

BUBBLEVERSE Q JOURNALS
0.42
5. KEY RESULTS
Minimal qualifying subset size: 4
Unique subset: ωb,ωc d m,f E D E,θi,sc f
Capture: 90.89% matched / 88.48% centroid / 87.20% pairwise-shape.
LOO robustness: 9/9 in all three channels.
FINAL_RESULT_GATE: PASS.
Final result: The surviving CamSpec/HiLLiPoP implementation-geometry difference is
DISTRIBUTED, not concentrated in one or two common coordinates.
Limitations: Parameter-space localization is not causal attribution; CamSpec/HiLLiPoP are
not independent observations; no H₀ benchmark or EDE viability conclusion changes.
Contradictions: None.
6. NEGATIVE RESULTS / MIKAMI
Failed routes: Single-coordinate, H₀-only, A Pl anc k-only and two-coordinate concentration
explanations are insufficient under the frozen criterion.
Mikami Graveyard:
- 2-coordinate concentration — rejected. ≤
- Simple H₀-only / A Pl anc k-only explanation — weakened.
Reason: neither appears in the unique minimal robust explanation of the complete
geometry.
7. MODEL CHANGE
Before: C-036-IMPL = material implementation-dependent geometry difference; cause
unresolved.
After: C-036-IMPL = material, exact-common-support-surviving, distributed multivariate
geometry difference; cause unresolved.
Change: PRÆCISERET / CONSTRAINED.
MOD-EDE-N3 status: unchanged.
8. GITHUB / PROVENANCE
Repository: ”Morfindien/Bubbleverse”
Parent Q037 run: ”34115280043”, head ”c49d9885…”
Q038 run: ”34121000822”, head ”02ddda7c…”
Program: ”q038_coordinate_localization_v1.py”
Workflow: ”.github/workflows/q038-coordinate-localization-v1.yml”
Result: ”R-Q038-EDE-COORDINATE-LOCALIZATION-001”
Provenance: deterministic reanalysis of validated Q037/Q032 endpoint lineage; no new
observational data or likelihood execution.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
Checkout recorded commits obtain Q037 endpoint artifact run Q038 → →
program/workflow with locked Q031 scales and preregistered thresholds verify subset →
captures/LOO tests require FINAL_RESULT_GATE PASS and classification replay. →
10. CONCLUSION
Q038 establishes that the surviving CamSpec/HiLLiPoP implementation difference is
genuinely multivariate under the tested geometry. At least four common coordinates are
required for a robust compact representation. The calculation narrows the methodological
problem but does not identify which likelihood implementation component causes it.
11. NEXT-Q HANDOFF
Why: Causal implementation source remains unresolved.
Next Q: Q039
Question: Can a controlled matched intervention isolate one implementation block as
sufficient to explain/reduce C-036-IMPL, or are coupled implementation changes required?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: DISTRIBUTED; unique minimal robust subset = ωb+ωc d m+f E D E+ θi,sc f.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: 2-coordinate concentration rejected; simple H ₀/ ≤ A Pl anc k-
only narratives weakened.
MODEL CHANGE SUMMARY: C-036-IMPL refined to distributed multivariate geometry;
MOD-EDE-N3 unchanged.
REPRODUCIBILITY / GITHUB: ”Morfindien/Bubbleverse”; runs ”34115280043”,
”34121000822”; Q038 workflow/program above.
NEXT-Q HANDOFF: Q039 — causal implementation-block attribution.

BUBBLEVERSE Q JOURNALS
0.42
Q039
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q039
Date/time: 2026-09-08 20:46 CEST
Status: INCONCLUSIVE
Question: When CamSpec and HiLLiPoP on Q032 exact TT common support are
investigated with preregistered, native-parameter-respecting matched interventions in
their implementation blocks, can one single implementation block materially
explain/reduce the Q037/Q038 distributed common-geometry difference, or are coupled
changes across multiple blocks required?
2. STARTING STATE
Model: MOD-EDE-N3, nsc f=3, ACTIVE / CONSTRAINED / NOT ESTABLISHED NEW PHYSICS.
Inherited: Q037 common-support discrepancy: matched 2.93179, centroid 0.83115, pairwise
1.63679. Q038: discrepancy DISTRIBUTED; minimal robust subset ωb,ωc d m,f E D E, θi,sc f.
Constraints: Frozen Q032 TT support/backend/scales; threshold 0.10; no cross-likelihood ≤
objective comparison; native parameter semantics only.
3. HYPOTHESES
Tested:
H1 relative calibration explains discrepancy.
H2 off-diagonal precision coupling explains discrepancy.
H3 calibration+precision explains discrepancy.
H4 native foreground profiling freedom explains discrepancy.
Rejected as sufficient: H1–H4; all remained far above threshold, 0/9 LOO sufficient.
Surviving: deeper coupled likelihood/data/foreground/covariance construction remains
possible but unproven.
4. METHOD & EVIDENCE
Methods: Matched implementation interventions; BOBYQA reoptimization; full-sample
geometry + 9 leave-one-label-out tests.
Sources: Rosenberg et al. 2022, arXiv:2205.10869; Efstathiou & Gratton 2021,
arXiv:1910.00483; Tristram et al. 2024, DOI 10.1051/0004-6361/202348015; Jense et al. 2026,
arXiv:2510.09430; HiLLiPoP commit a09ddde3; Cobaya 3.5.6.
5. KEY RESULTS
Calibration: 2.84864 / 0.87392 / 1.48583.
Precision: 2.60701 / 0.84119 / ~1.62217.
Calibration+precision: 3.07861 / 1.19445 / 1.87403.

BUBBLEVERSE Q JOURNALS
0.42
Foreground-profile: 2.98293 / 1.05547 / 1.63532, LOO sufficient 0/9.
Final result: No tested scientifically matchable single block explains C-036-IMPL. Deeper
coupled construction remains unresolved.
Limitations: Full foreground/core-likelihood harmonization cannot be isolated as a clean
native single-block intervention. No physical systematic or new physics established.
6. NEGATIVE RESULTS / MIKAMI
Failed technical attempts: Q039 V1–V4 and early FGPROFILE launcher/static failures;
workflow/infrastructure only, no scientific evidence.
Graveyard: calibration-only, precision-only, calibration+precision, native foreground-
profile freedom as sufficient explanations. Synthetic cross-likelihood nuisance/core hybrids
rejected as scientifically invalid designs.
7. MODEL CHANGE
Before: C-036-IMPL active with several possible isolated implementation causes.
After: C-036-IMPL remains active, but single-block explanation space is strongly narrowed.
Change: CONSTRAINED.
Reason: validated negative Q039 interventions.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Backend: class_ede ”5a131c91d657dd9a7c6364cc45b038710f8d0d97”
Q032: run 33994305721, commit ”4dc873a5e880d40858d831a3b421456728f0c032”
Q039 V5: run 34161368438, commit ”365217d4a4ca21e0af3b296c0e6b23df7e07ba60”,
workflow ”q039-implementation-block-intervention-v5.yml”
FGPROFILE: run 34184346582, commit ”449fe096e49a793446c0c859cf8caf0fcdaf4c8f”,
workflow ”q039-native-foreground-profile-v1.yml”
Results: R-Q039-EDE-IMPLEMENTATION-BLOCK-INTERVENTION-001; R-Q039-EDE-NATIVE-
FOREGROUND-PROFILE-001. FINAL_RESULT_GATE PASS.
9. REPRODUCIBILITY
Checkout recorded commits obtain frozen Q032 endpoints/support run recorded → →
workflows with frozen parameters reproduce geometry/LOO outputs apply 0.10 → → ≤
sufficiency criterion.
10. CONCLUSION
Q039 closes INCONCLUSIVE but strongly constraining. The CamSpec–HiLLiPoP discrepancy
survives all scientifically clean tested single-block interventions. Its remaining cause lies, if
identifiable, in deeper coupled implementation structure. This is methodological evidence
only.
11. NEXT-Q HANDOFF
Next Q: Q040

BUBBLEVERSE Q JOURNALS
0.42
Why: determine whether a finite, scientifically defensible coupled structural intervention
can explain C-036-IMPL without constructing a meaningless synthetic likelihood.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: No tested clean single implementation block is sufficient; coupled deeper
structure remains unresolved.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Calibration, precision, calibration+precision and native
foreground-profile freedom killed as sufficient explanations.
MODEL CHANGE SUMMARY: C-036-IMPL retained but substantially constrained.
REPRODUCIBILITY / GITHUB: Runs 34161368438 and 34184346582; commits and workflows
above.
NEXT-Q HANDOFF: Q040 — test whether a scientifically valid coupled structural bridge can
be defined.

BUBBLEVERSE Q JOURNALS
0.42
Q040
Q041
BUBBLEVERSE — Q-JOURNAL
1. IDENTITY
Q-ID: Q040
Date/time: 2026-09-08 22:47 CEST
Status: INCONCLUSIVE
Question: Can a finite, preregistered and scientifically defensible coupled structural
intervention involving documented CamSpec-versus-HiLLiPoP differences in foreground-
model form, data-vector construction/weighting and covariance/likelihood construction
materially reduce C-036-IMPL on the Q032 matched-support architecture without
constructing a scientifically meaningless synthetic likelihood?
2. STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3 — ACTIVE / CONSTRAINED / NOT ESTABLISHED
NEW PHYSICS.
Inherited: Q036–Q038 established reproducible, distributed CamSpec–HiLLiPoP geometry
discrepancy; Q039 rejected calibration, precision coupling and native foreground profiling
as sufficient explanations.
Constraints: Frozen Q032 TT support, 7D geometry, threshold 0.10; CamSpec/HiLLiPoP
remain native separate likelihoods; no synthetic likelihood; A_planck explicit.
3. HYPOTHESES
Tested:
H1: Valid common-CMB latent representation exists.
H2: Single-Gaussian nuisance marginalization can support the test.
H3: Defensive non-Gaussian RQMC can produce validated endpoints.
Rejected: H2 — CamSpec boundary/non-PD Hessian and HiLLiPoP multistart instability.
Surviving: H1 mathematically supported; H3 numerically unresolved. C-036-DEEP-
STRUCTURAL remains active/unresolved.
4. METHOD & EVIDENCE
Methods: Native nuisance marginalization; Laplace/Schur validation; defensive importance
sampling + Owen-scrambled Sobol RQMC, 4 replicates, m=9–16.
Sources: K-044 CamSpec; K-049 HiLLiPoP; K-053/K-054 official implementations; K-055
boundary statistics; K-056 mixed Laplace; K-057 defensive importance sampling; K-058
RQMC.
Programs/workflows: ”q040_defensive_rqmc_v4.py”; ”.github/workflows/q040-defensive-
rqmc-v4.yml”; GitHub run 34258155387.

BUBBLEVERSE Q JOURNALS
0.42
Tests: Frozen Δχ² convergence 0.05; Bank A/B 0.05; downstream science endpoints ≤ ≤
allowed only after validation.
5. KEY RESULTS
Single-Gaussian compression: COMPRESSION_VALIDATION_FAIL.
RQMC reached hard cap m=16 / 393,216 nodes per replicate/implementation.
CamSpec: transition 16.5899; Bank A/B 28.4438.
HiLLiPoP: transition 61.1260; Bank A/B 63.1116.
Required: 0.05. ≤
Final result: ”DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL”.
Science endpoints, final geometry and 9/9 LOO were correctly blocked.
Limitation: No conclusion on whether a successfully validated structural bridge would
reduce C-036-IMPL.
Contradictions: None; Q036–Q039 remain compatible.
6. NEGATIVE RESULTS / MIKAMI
Failed attempts: CMB-space V1–V3 technical failures; RQMC V1 serialization, V2 GitHub
artifact transport, V3 deployment failure. No physical evidence.
Graveyard additions: Single-Gaussian Laplace/Schur route killed for Q040 science; finite
Q040 RQMC campaign killed as numerically validated bridge at frozen hard cap.
7. MODEL CHANGE
Before: C-036-IMPL active; deeper structural origin unresolved.
After: Same physical/model status, but deeper bridge is mathematically defined and tested
numerical routes constrained.
Change: CONSTRAINED / REFINED.
Reason: Both Gaussian compression and finite defensive RQMC failed preregistered
validation.
8. GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Commit: 855a28c58246dbdd52d01cae1f40e0611103d96b
Workflow: ”.github/workflows/q040-defensive-rqmc-v4.yml”
Program: ”q040_defensive_rqmc_v4.py”
Result: R-Q040-EDE-DEFENSIVE-RQMC-CMB-MARGINAL-004
Artifacts: ”q040-rqmc-final-v4”; ”q040-rqmc-integration-final-v4”; ”q040-rqmc-state-m16-
v4”.
Provenance: Frozen Q032/Q037 architecture + native CamSpec/HiLLiPoP likelihoods;
preregistered finite campaign completed through hard cap.

BUBBLEVERSE Q JOURNALS
0.42
9. REPRODUCIBILITY
Checkout recorded commits; obtain Q032/Q037 parent artifacts and native likelihoods; run
Q040-RQMC-V4 with frozen parameters; reproduce m9–m16 states; apply unchanged 0.05
validation gates and 0.10 science criterion.
10. CONCLUSION
A scientifically defensible common native-nuisance-marginalized CMB representation
exists mathematically, but Q040 did not obtain a numerically validated implementation
capable of testing whether it materially reduces C-036-IMPL. The discrepancy therefore
remains active and unexplained; no pipeline superiority, EDE confirmation/falsification or
new physics is established.
11. NEXT-Q HANDOFF
Why: The dominant source of RQMC instability remains unidentified.
Next Q: Q041
Question: Is Q040’s finite defensive-RQMC nonconvergence dominated by a small
identifiable subset of nuisance dimensions, boundaries, proposal strata or likelihood-
specific directions, or is it broadly distributed?
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: INCONCLUSIVE — valid bridge definition exists, but finite numerical
validation failed.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Gaussian compression and Q040 finite-RQMC science route
rejected under tested conditions.
MODEL CHANGE SUMMARY: Model unchanged; methodological space narrowed.
REPRODUCIBILITY / GITHUB: Morfindien/Bubbleverse, commit 855a28c…, run
34258155387, Q040-RQMC-V4.
NEXT-Q HANDOFF: Q041 — localize the source of RQMC instability.
LATER ROUTING NOTE (2026-09-24): The Q040 handoff above is preserved as historical
research provenance. The Q041 execution that was ultimately preregistered and run
addressed downstream scientific-consequence portability rather than the proposed RQMC-
instability localization. Q040 is not reopened by this routing change.

BUBBLEVERSE Q JOURNALS
0.42
Q041
BUBBLEVERSE — Q-JOURNAL
IDENTITY
Q-ID: Q041
Date/time: 2026-09-24 CEST
Status: INCONCLUSIVE / COMPUTATIONAL CAMPAIGN COMPLETE / ORIGINAL SCIENTIFIC QUESTION UNRESOLVED
Question: Does the validated CamSpec–HiLLiPoP fitted-geometry difference in n=3 EDE
produce a materially different downstream cosmological inference when the Planck
likelihood arms are combined with matched external information?
STARTING STATE
Model entering Q: MOD-EDE-N3, n_scf=3 — ACTIVE / CONSTRAINED / NOT ESTABLISHED
NEW PHYSICS.
Inherited: Q035 showed that the historical stable/non-stable basin contrast is classifier
dependent; Q036 established a material continuous CamSpec–HiLLiPoP geometry
difference; Q037 showed that the difference survives exact-common-TT support; Q038
localized the compact multivariate structure to omega_b, omega_cdm, f_EDE, and
theta_i,scf; Q039 rejected calibration, precision coupling, calibration+precision, and native
foreground-profile freedom as sufficient explanations; Q040 defined a legitimate common-
CMB-space marginalization target but failed numerical validation before science
endpoints.
Hard constraints: the Planck arms remain separate; both arms use the same frozen n=3
EDE backend and matched external data; cross-arm absolute likelihood/chi2 subtraction is
forbidden as physical evidence; failed or unconverged chains are not scientific evidence;
Q040-CMBSPACE-* and Q040-RQMC-* scientific products are forbidden as Q041 inputs.
HYPOTHESES / DECISION CLASSES
V19 preregistered three possible scientific classes after all required gates:
MATERIAL_DOWNSTREAM_DIFFERENCE, SCIENTIFICALLY_EQUIVALENT_CONSTRAINTS,
or CONSTRAINED_MIXED.
A technical or convergence gate failure instead yields NO_SCIENTIFIC_RESULT. That state is
a control outcome and is not a fourth physical class.
METHOD & EVIDENCE
Authoritative program: Q041-PLANCKPORT-V19; result R-Q041-EDE-DOWNSTREAM-
PORTABILITY-019; workflow .github/workflows/q041-planck-portability-v19.yml.
V19 arms: camspec and hillipop. Data combinations: P, P_A6, P_L6, P_D2, P_A6_L6_D2,
P_L6_D2, P_A6_D2, P_A6_L6. Two independent chains per arm/combination produced 32
logical chains.

BUBBLEVERSE Q JOURNALS
0.42
External inputs: ACT DR6 primary through DR6-ACT-lite v1.0.1 commit
880eacb40d66722eb1c32d7b5621e91662b4d808; ACT DR6 lensing through act_dr6_lenslike
v1.2.1 commit b386ddbb5821c1216c709f051c9289292f174d30; DESI DR2 BAO through
bao_data v2.6 commit b7b8a36e9bccb063081f811f323cada21ab5fbdd and Cobaya definition
commit b76b6fed2a6c8c5594c6f92d5058bef10079746a.
Frozen parents and software: Q032 result R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002,
GitHub run 33994305721, execution commit
4dc873a5e880d40858d831a3b421456728f0c032; class_ede commit
5a131c91d657dd9a7c6364cc45b038710f8d0d97; HiLLiPoP commit
a09ddde3e7ce11df99f74685feb1f1764cafb251; Cobaya 3.5.6.
Overlap policy: without A6, use the full authoritative Q032 exact-common-TT support. With
A6, further restrict Planck primary TT to ell <= 599 while ACT primary TT/TE/EE begins at
ell = 600; cross-likelihood covariance is assumed zero only after that disjoint primary-
multipole construction.
Sampler: Cobaya MCMC; Rminus1_stop = 0.02; Rminus1_cl_stop = 0.2; hard science R-hat
gate <= 1.05; max_samples = 20,000 accepted samples per chain; maximum eight successful
compute segments per chain; 300-minute segment soft stop; 330-minute GitHub job
timeout.
Execution architecture: one fixed linear eight-stage workflow, 32 matrix jobs per segment,
max-parallel = 6. Each segment transports only the exact immediate-predecessor same-run
artifact. Cross-version chain-state reuse is forbidden. HiLLiPoP resume is locked to the
serialized planck_2020_hillipop.TT component in chain.updated.yaml; Cobaya --allow-
changes is not used.
KEY RESULTS
GitHub Actions run 34979609004 completed successfully on attempt 4 at execution commit
a962ba70077422f8b69642dea4e8272e1d00e5ff.
Final artifact: q041-final-v19, artifact ID 10754769330, SHA-256
2284518ecbaaf1ff0d0093977827d5162ec29549ba2b81880f266c250311ca2b.
The final JSON reports scientific_classification = NO_SCIENTIFIC_RESULT; outcome_type =
CONTROLLED_NO_SCIENTIFIC_RESULT; no_science_reason =
MAX_SAMPLES_WITHOUT_CONVERGENCE; actual_computed_result = false;
technical_failure = false; final_outcome_valid = true; status = PASS.
Thirty logical chains are listed as MAX_SAMPLES_WITHOUT_CONVERGENCE. The two
remaining chains — CamSpec / P_A6 / c1 and CamSpec / P_A6_L6_D2 / c1 — reached
segment 8 still PARTIAL after all eight compute segments. The combined record therefore
contains 0/32 chains with documented COMPLETE status.
Final science gates: CHAIN_COMPLETENESS = BLOCKED; ALL_RHAT_LE_1P05 = BLOCKED;
BOTH_ARMS_ALL_COMBINATIONS = BLOCKED; Q040_FIREWALL = PASS;
SEGMENTED_RESUME_COMPLETENESS = CONTROLLED_STOP.

BUBBLEVERSE Q JOURNALS
0.42
No authoritative full-matrix standardized shifts, Bhattacharyya coefficient, or leave-one-
out portability classification may be interpreted scientifically because the prerequisite
convergence/completeness gates were not satisfied.
CONTRACT AUDIT
The executed V19 preregistration is not identical to the broader Q041 scientific design that
preceded it. The broader design required matched CamSpec and HiLLiPoP arms, both
ΛCDM and n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, one common frozen
supernova likelihood, a FULL combination plus four leave-one-out combinations, within-
arm ΛCDM-versus-EDE model-preference information, and the original materiality/overlap
decision rules.
V19 instead executes MOD-EDE-N3 only, omits a separate ΛCDM matrix and the supernova
likelihood, uses three leave-one-out combinations, and applies its own six-coordinate
standardized-shift and Gaussian Bhattacharyya classification.
This is a material scope/provenance difference. It does not retroactively invalidate V19: V19
had its own preregistration before the final outcome. It does mean that V19 cannot be
described as the complete execution of the broader original downstream contract.
NEGATIVE RESULTS / MIKAMI
Killed interpretation: Q041 non-convergence => CamSpec and HiLLiPoP physically differ.
Killed interpretation: Q041 non-convergence => CamSpec and HiLLiPoP are scientifically
equivalent.
Killed interpretation: a green GitHub Actions conclusion => a green cosmological result.
Retained prohibition: failed technical runs, timeouts, runner failures, dependency failures,
and resume bugs carry no physical evidentiary weight.
Retained prohibition: Q040 invalidated science endpoints may not be resurrected as Q041
evidence.
MODEL CHANGE
Physical model change: NONE.
C-036-IMPL remains active as a methodological likelihood-geometry discrepancy. Q041
does not determine its downstream physical significance.
New computational knowledge: under the frozen V19 parameterization, sampler settings,
and compute/sample budget, a complete converged posterior matrix was not obtained.
New provenance knowledge: the executed V19 test is narrower than the broader original
Q041 scientific contract.
GITHUB / PROVENANCE
Repository: Morfindien/Bubbleverse
Branch: main
Execution commit: a962ba70077422f8b69642dea4e8272e1d00e5ff

BUBBLEVERSE Q JOURNALS
0.42
GitHub Actions run: 34979609004; attempt 4; status/conclusion: completed / success.
Workflow: .github/workflows/q041-planck-portability-v19.yml
Program: q041_planck_portability_v19.py
Preregistration: q041_planck_portability_preregister_v19.json
Source lock: q041_planck_portability_source_lock_v19.json
Validator: q041_planck_portability_tests_v19.py
Final artifact: q041-final-v19; ID 10754769330; SHA-256
2284518ecbaaf1ff0d0093977827d5162ec29549ba2b81880f266c250311ca2b.
q041_final_v19.json SHA-256:
0062874ed3529004f46cfb542a708d5b8e8dde55d1b4fd1c2ac7c394e6c8be79.
q041_final_tests_v19.json SHA-256:
95fe1e63c78033de8559f609f0d8a1f4d48ee1b4123f3bb8f845b3ac6e5797ab.
GitHub status success validates the workflow-defined terminal control state. It does not
convert blocked scientific gates into passed scientific gates.
REPRODUCIBILITY
Reconstruct V19 from the recorded execution commit; verify the preregistration and
source lock; reproduce the same external source versions and Q032 parent; preserve the
eight-stage same-run resume contract; compare the final artifact and validator output;
require the same science gates before any posterior portability interpretation.
Any successor campaign must receive a new version/result identity. Raising max_samples
or changing the sampler after observing V19 without a new preregistered configuration
would retroactively change the test rather than reproduce it.
CONCLUSION
Q041-V19 is complete as a computational campaign and valid as a controlled no-science
result. It did not produce a converged downstream cosmological portability classification.
The original downstream physical question therefore remains unresolved. V19 establishes
neither material downstream difference nor scientific equivalence nor dataset-conditional
mixed behaviour.
Because the executed V19 contract is also narrower than the broader original design, a
future test must explicitly state which scientific contract it is executing rather than silently
merging the two.
NEXT-Q HANDOFF
Next Q: Q042 — HIGH
Question: Can the original downstream-portability test be executed with a new
preregistered, convergence-robust inference strategy that preserves both native Planck
arms, ΛCDM and n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, one common
frozen supernova likelihood, FULL plus four leave-one-out tests, and the original

BUBBLEVERSE Q JOURNALS
0.42
materiality/model-preference rules, without reusing Q040 invalidated science endpoints or
moving the criteria after results are seen?
Recommended start motor: BUBBLEVERSE — AUTONOMOUS EXECUTION-MECHANISM /
NUMERICAL / HPC / MOTOR-BUILDER ENGINE.
Constraint: diagnose existing V19 chains/progress/checkpoints before authorizing another
large compute campaign. Do not simply “run longer.”
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: CONTROLLED_NO_SCIENTIFIC_RESULT — the V19 campaign did not
reach the convergence/completeness gates required for scientific classification; the broader
original downstream question remains unresolved.
Q-JOURNAL: This entry.
MIKAMI GRAVEYARD UPDATE: Non-convergence cannot be used as evidence for either
physical agreement or disagreement; green workflow status is not a scientific result.
MODEL CHANGE SUMMARY: No physical model change; computational and provenance
state refined.
REPRODUCIBILITY / GITHUB: Q041-PLANCKPORT-V19; R-Q041-EDE-DOWNSTREAM-
PORTABILITY-019; run 34979609004; execution commit
a962ba70077422f8b69642dea4e8272e1d00e5ff; final artifact digest above.
NEXT-Q HANDOFF: Q042 — design and validate the correct convergence-robust execution
mechanism for the unresolved downstream scientific contract.

Q042
BUBBLEVERSE - Q-JOURNAL
IDENTITY
Q-ID: Q042 Case-ID: NOT DOCUMENTED Date/time: 2026-10-07 08:00 CEST closure state Status: CLOSED - INCONCLUSIVE
GENERAL FEASIBILITY / NO NEW COSMOLOGICAL INFERENCE
QUESTION
Can the original Q041 downstream-portability test be executed using a newly preregistered, convergence-robust strategy that
preserves both native Planck arms, LCDM and n=3 EDE, ACT DR6 primary, ACT DR6 lensing, DESI DR2, one identical frozen
supernova likelihood, FULL plus four leave-one-out tests and the original materiality/model-preference rules, without reusing
invalidated Q040 science endpoints, cross-arm absolute-objective arithmetic or retrospective criteria changes?
STARTING STATE
Q041-V19 was complete as a controlled computational campaign but produced NO_SCIENTIFIC_RESULT: 30 chains reached the
sample limit, two remained partial, and 0/32 had documented COMPLETE status. Its executed contract was narrower than the
original downstream specification because it omitted the separate LCDM matrix and common supernova block and used three
rather than four leave-one-out combinations. The physical downstream significance of the CamSpec-HiLLiPoP fitted-geometry
difference therefore remained unresolved.
Q040 science endpoints remained forbidden inputs. Cross-arm absolute likelihood or chi-squared subtraction remained forbidden
as physical evidence. A green workflow status could not substitute for convergence, completeness or scientific qualification.
FROZEN SCIENTIFIC CONTRACT
The retained contract required two native Planck arms x two models (LCDM and n=3 EDE) x FULL plus four leave-one-out
combinations, for 20 required inference cells. External blocks remained ACT DR6 primary, ACT DR6 lensing, DESI DR2 and one
identical frozen supernova likelihood. Original priors, overlap rules, materiality rules and model-preference criteria were
unchanged.
Scientific specification SHA-256: 41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c.
PRODUCTION HISTORY
The original Q042 posterior branch failed before completed posteriors were produced. Initial sampler-option leakage was a
configuration failure, not a measured convergence failure. All 80 optimizer records survive: 78 flag-0 records and two flag-3
failures. Their existence does not certify global minima and does not provide posterior portability evidence.

Subsequent bounded diagnostics progressively isolated a numerical reference-construction problem. V22 tested bounded branch
durability/checkpoint behaviour. V23 exposed positive-node spline overshoot in the original binary. V24 recorded a nonfinite
upper optical-depth trial followed by successful return and zero bisection. V25 reproduced a source-consistent finite-input helium-
cutoff overflow followed by propagation of nonfinite state. V26-V28 were retained as RAW_NOT_QUALIFIED diagnostics. V29
initialized the context and 24 explicit interval-box prerequisites but did not qualify a complete history or a scientific result. V30
produced partial conditional histories and failed its frozen inflation construction.
V31 BOUNDED COMPARISON
V31 produced partial conditional histories plus a separate necessary support-cap incompatibility. Both local attempts stopped at
the parent 600-second deadline.
UPPER: 3,741 retained certificates; 3,233/3,334 post-entry native nodes; last retained certificate endpoint z = 1.501953125. LOWER:
3,579 retained certificates; 3,210/3,334 post-entry native nodes; last retained certificate endpoint z = 1.849609375.
Final committed endpoints, complete final counters and peak memory after the parent kill are NOT DOCUMENTED. No full tau
value was computed.
CONDITIONAL MATHEMATICAL RESULT
Frozen support-candidate cap: 32. Retained conservative candidate counts: UPPER 138; LOWER 3,002. Existing minimum upper
bounds: UPPER 0.00024287858999792338; LOWER 0.00024212042562975905. Certified missing-tail source lower bounds: UPPER
1.1628411809721158; LOWER 0.08148057013890592.
Under the frozen source extension, global rails and append-only retention of the existing intervals, the missing tail cannot lower
the relevant minimum threshold or remove the existing candidates. Completing that unchanged representation therefore cannot
satisfy cap32.
This is a conditional failure of an interval representation and output policy. It is not evidence for 138 or 3,002 physical minima, an
executed tau failure, or impossibility of every alternative method.
QUALIFICATION BOUNDARY
The construction concerns existing absolutely continuous solutions of the frozen real-table right-hand side under its stated
domain assumptions. It does not establish existence or uniqueness for the original switched right-hand side, original-binary
arithmetic accuracy, upstream physical/table accuracy, a justified downstream prediction/likelihood error budget, a valid
complete reference, or the convergence-qualified 20-cell comparison.
CURRENT GATES
Q completion: PASS - documented inconclusive closure. Whole history: PARTIAL. Actual support/spline/tau pipeline: NOT
EXECUTED. Unchanged support-cap condition: FAIL within the stated conditional scope. Original-binary arithmetic accuracy:
UNRESOLVED. Upstream accuracy: UNRESOLVED.

Downstream acceptance budget: NOT DOCUMENTED. Reference truth: BLOCKED. Numerical final result: UNRESOLVED.
Production restart: NOT AUTHORIZED.
NEGATIVE RESULTS / MIKAMI
Killed as sufficient repair: simply running the unchanged V31 retained-interval representation longer. Faster or longer execution
cannot remove the independently documented cap32 obstruction under the frozen append-only/global-rail assumptions.
Not killed: LCDM, n=3 EDE, the underlying common-latent mathematical target, or every future contract-preserving numerical
strategy. Technical failures and unqualified diagnostics remain non-physical evidence.
MODEL CHANGE
Physical model change: NONE. H0 benchmarks are unchanged. MOD-EDE-N3 remains ACTIVE / CONSTRAINED. C-036-IMPL
remains a methodological CamSpec-HiLLiPoP geometry tension with unresolved downstream cosmological significance.
Execution-state change: Q042 is no longer an active unchanged execution campaign. The documented tested strategies did not
qualify the original contract, and Q042 closes inconclusively. A materially new qualified design would require a new-case or
explicit reopening decision.
GITHUB / PROVENANCE
Relevant remote prerequisite: Q042-CONTEXT-V29, GitHub Actions run 37362125253, attempt 1, execution commit
72cf9e92fc794c122f593a77b6a555e6e97f6a2e, status success. Its scope is prerequisite-only.
V31 is local, not committed as a GitHub workflow result: RUN Q042_COMPARISON_V31_LOCAL_001; result R-Q042-COMPARISON-
V31-001; CONFIG SHA-256 2f7a5d08e7566c613de93328fe4d4d6760d8ede81f6c3b789e230f64ca202dd1; CLASS_EDE source commit
5a131c91d657dd9a7c6364cc45b038710f8d0d97.
Conclusion-critical internal source IDs: I-Q042-COMPARISON-DESIGN-001; I-Q042-COMPARISON-V31-001; I-Q042-COMPARISON-
V31-VALIDATION-001; I-Q042-V31-INGESTION-001. The complete Q042 ingestion decision/audit preserves the 91-source register
and inherited claim maps without renumbering legacy K-IDs.
REPOSITORY STATE
At the documented revision point, Morfindien/bubbleverse-model remained accepted through Q041 at model head
10fa83797b2f7740519d4e43b1bebf0a6e35bada, while Morfindien/Bubbleverse remained at execution head
72cf9e92fc794c122f593a77b6a555e6e97f6a2e. README and program-registry status lagged the supplied Q042 closure. No remote
synchronization was performed as part of this journal closure.
CONCLUSION
The available tested strategies did not establish execution and scientific qualification of the exact original Q041 downstream-
portability contract. General feasibility remains

inconclusive. Q042 therefore closes as a documented inconclusive feasibility investigation, not as an affirmative production result
and not as a universal impossibility theorem.
The downstream physical question remains unresolved. No posterior portability class, model preference, physical falsification,
pipeline superiority, or new physics follows from Q042.
NEXT HANDOFF
No new scientific Q-ID is allocated solely from this closure. The next concrete task is operational: TASK-Q042-M14-SYNC-001 -
synchronize the Q042 closure into one consistent repository, registry and candidate-model state while preserving the existing
evidential boundaries and previous accepted snapshot until the controlled update passes its gates.
REQUIRED END-OF-Q OUTPUT
FINAL ANSWER: CLOSED - INCONCLUSIVE GENERAL FEASIBILITY. The documented strategies did not qualify the original
contract; materially different contract-preserving feasibility remains unresolved. MIKAMI: Run-longer is rejected as sufficient
repair of unchanged V31. Technical failure is not physical failure. MODEL CHANGE: No physical change; execution feasibility and
qualification limits refined. NEXT: Repository/model synchronization task; no new scientific Q allocated.

Q043 — Repository integration preparation and validation
Q-ID: Q043. Status: CLOSED. Result ID: R-Q043-REPOSITORY-INTEGRATION-001. Task lineage: TASK-Q042-M14-SYNC-001. CASE-
ID: NOT DOCUMENTED.
QUESTION: Can the Q042 closure be incorporated into a consistent candidate/control package while preserving source and
qualification boundaries and passing the existing gates?
ANSWER: Yes, locally at the pinned repository bases. Result: PASS_LOCAL_PREPARATION_AND_VALIDATION_ONLY. No remote
synchronization, candidate admission, promotion, release or numerical production was performed.
STARTING STATE: Q042 CLOSED, general feasibility INCONCLUSIVE; reference-truth gate BLOCKED; final-result gate
UNRESOLVED; production NOT AUTHORIZED. Accepted remote model v0.3/R000003 through Q041. Original Q041 physical
portability question remains OPEN.
METHOD: Prepare and validate controlled diffs for Morfindien/bubbleverse-model and Morfindien/Bubbleverse. Preserve all 91
late-Q042 source objects, both claim-map trees, all prior accepted snapshots, physical model content, and historical
workflows/manifests/artifacts. Proposed v0.4/R000004 stored under provenance/prepared_candidates/Q042/; status
CANDIDATE_PREPARED_NOT_PROMOTED.
VALIDATION: Candidate 8/8 PASS; scientific 10/10 PASS; formal 13/13 PASS; Q041 historical 10/10 PASS; failure-injection 10/10
PASS; public healthcheck 20/20 PASS; launcher resolver 4/4 PASS; shared closure fields 14 matched; protected execution files 1,526
unchanged; clean-base diff PASS; read-only technical review CLEAN.
GITHUB BOUNDARY: Last inspected model HEAD 10fa83797b2f7740519d4e43b1bebf0a6e35bada; execution HEAD
72cf9e92fc794c122f593a77b6a555e6e97f6a2e. V29 run 37362125253 succeeded for prerequisites only; live registry remained ACTIVE
for V29. Prepared package had not been applied at the inspected heads.
LIMITATIONS: Internal technical consistency is not independent physical validation. Q042 optimizer trajectories and cap proof
were preserved rather than rerun. No scientific portability classification, H0 shift, EDE detection or falsification follows. Physical
model NOT MATERIALLY CHANGED.
NEXT HANDOFF: TASK-Q043-M14-APPLY-001 to REPOSITORY / MODEL UPDATE ENGINE for controlled application and
separately gated admission/promotion. This journal does not authorize dispatch. PRED-EDE-PORTABILITY-001 and PRED-Q039-
COUPLED-001 remain OPEN.
SOURCES: EVD-Q043-JOURNAL; EVD-Q043-RESULT; I-Q043-PREPARATION-VALIDATION-001; I-Q042-V31-INGESTION-001.
q043_integration_result.json SHA-256 4486e5173ba8ef3ac659c743bb578284c93446ce9e5b3d0dae71728beadbb9ff. Revision
timestamp: 2026-10-09 06:32:29 UTC (historical revision time, not a new inspection).

