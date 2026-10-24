# Bubbleverse start codes

Technical navigation generated from exact source commit `b99a5c78058b624c8d5847bed582df4ea816358a`. No scientific workflow was dispatched. ACTIVE means the existing registry accepts the ID, not that a journal authorizes another run. Historical, deprecated and blocked routes are reference only. Required placeholders must be replaced after checking their source contract.

Start with [the current technical guide](docs/guides/START_HERE.md). The existing permanent launcher and registry are unchanged.

## Verified local maintenance commands

```bash
python --version
python tools/maintenance/check_cleanup_integrity.py
python -m unittest discover -s tests/maintenance -v
python -m unittest -v q048_inputcheck_tests_v1
python q048_threshold_anchor_package_check_v9.py
```

These checks perform no production campaign. Nine metadata controls and the V9 package gate passed. `python q048_package_check_v1.py` has the pre-existing failure `PACKAGE_FILE bubbleverse_program_registry.json`.

## Complete launch inventory

The following entries link to the unchanged sources. Full prerequisites, parameter declarations, original registry metadata, cost, outputs, resume/unknown fields and verification states are in [ENTRYPOINT_REGISTRY.json](docs/maintenance/cleanup/20261024-b99a5c7-v330/ENTRYPOINT_REGISTRY.json). Every executable workflow run block is preserved in [WORKFLOW_COMMANDS.json](docs/maintenance/cleanup/20261024-b99a5c7-v330/WORKFLOW_COMMANDS.json). Documented shell blocks and inline command spans, with their source locations is in [DOCUMENTED_COMMANDS.json](docs/maintenance/cleanup/20261024-b99a5c7-v330/DOCUMENTED_COMMANDS.json). No secret values were collected.

| ID / kind | Lifecycle | Source | Command / exclusion |
| --- | --- | --- | --- |
| Q036-GEOMETRY-V1 / registered-program | ACTIVE | [source](.github/workflows/q036-endpoint-geometry-portability-v3.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q036-GEOMETRY-V1 |
| Q036-GEOMETRY-V2 / registered-program | ACTIVE | [source](.github/workflows/q036-endpoint-geometry-portability-v3.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q036-GEOMETRY-V2 |
| Q036-GEOMETRY-V3 / registered-program | ACTIVE | [source](.github/workflows/q036-endpoint-geometry-portability-v3.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q036-GEOMETRY-V3 |
| Q038-COORDLOC-V1 / registered-program | ACTIVE | [source](.github/workflows/q038-coordinate-localization-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q038-COORDLOC-V1 |
| Q039-FGPROFILE-V1 / registered-program | ACTIVE | [source](.github/workflows/q039-native-foreground-profile-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-FGPROFILE-V1 |
| Q039-IMPLBLOCK-V1 / registered-program | ACTIVE | [source](bubbleverse_program_registry.json) | Pre-existing missing registered workflow: .github/workflows/q039-implementation-block-intervention-v1.yml |
| Q040-CMBSPACE-V1 / registered-program | BLOCKED | [source](.github/workflows/q040-cmbspace-coupled-bridge-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-CMBSPACE-V2 / registered-program | BLOCKED | [source](.github/workflows/q040-cmbspace-coupled-bridge-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-CMBSPACE-V3 / registered-program | BLOCKED | [source](.github/workflows/q040-cmbspace-coupled-bridge-v3.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-CMBSPACE-V4 / registered-program | DEPRECATED | [source](.github/workflows/q040-cmbspace-coupled-bridge-v4.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-CMBSPACE-V5 / registered-program | DEPRECATED | [source](.github/workflows/q040-cmbspace-compression-seal-v5.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-RQMC-V1 / registered-program | BLOCKED | [source](.github/workflows/q040-defensive-rqmc-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-RQMC-V2 / registered-program | BLOCKED | [source](.github/workflows/q040-defensive-rqmc-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-RQMC-V3 / registered-program | BLOCKED | [source](.github/workflows/q040-defensive-rqmc-v3.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q040-RQMC-V4 / registered-program | ACTIVE | [source](.github/workflows/q040-defensive-rqmc-v4.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-RQMC-V4 |
| Q041-PLANCKPORT-V1 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V10 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v10.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V11 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v11.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V12 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v12.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V13 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v13.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V14 / registered-program | DEPRECATED | [source](.github/workflows/q041-planck-portability-v14.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V15 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v15.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V16 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v16.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V17 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v17.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V18 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v18.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V19 / registered-program | ACTIVE | [source](.github/workflows/q041-planck-portability-v19.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q041-PLANCKPORT-V19 |
| Q041-PLANCKPORT-V2 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V3 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v3.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V4 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v4.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V5 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v5.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V6 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v6.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V7 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v7.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V8 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v8.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q041-PLANCKPORT-V9 / registered-program | BLOCKED | [source](.github/workflows/q041-planck-portability-v9.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-STOCKDIAG-V20 / registered-program | BLOCKED | [source](.github/workflows/q042-stock-diagnostic-v20.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-STOCKDIAG-V21 / registered-program | DEPRECATED | [source](.github/workflows/q042-stock-diagnostic-v21.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-DURABLE-V22 / registered-program | HISTORICAL | [source](.github/workflows/q042-durable-v22.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-CLASSCAUSE-V23 / registered-program | HISTORICAL | [source](.github/workflows/q042-class-cause-v23.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-CLASSORIGIN-V24 / registered-program | HISTORICAL | [source](.github/workflows/q042-class-origin-v24.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-CLASSNAN-V25 / registered-program | HISTORICAL | [source](.github/workflows/q042-class-nan-v25.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-REFACQ-V26 / registered-program | HISTORICAL | [source](.github/workflows/q042-reference-acquisition-v26.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-SWITCHPROBE-V27 / registered-program | HISTORICAL | [source](.github/workflows/q042-switch-probe-v27.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-EVENTCELL-V28 / registered-program | HISTORICAL | [source](.github/workflows/q042-event-cell-v28.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q042-CONTEXT-V29 / registered-program | HISTORICAL | [source](.github/workflows/q042-context-v29.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-BASELINE-V1 / registered-program | DEPRECATED | [source](.github/workflows/q045-native-baseline-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-BASELINE-V2 / registered-program | HISTORICAL | [source](.github/workflows/q045-native-baseline-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-OPTICAL-AUDIT-V1 / registered-program | BLOCKED | [source](.github/workflows/q045-optical-audit-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-OPTICAL-AUDIT-V2 / registered-program | BLOCKED | [source](.github/workflows/q045-optical-audit-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-OPTICAL-AUDIT-V3 / registered-program | HISTORICAL | [source](.github/workflows/q045-optical-audit-v3.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-REFHIST-V1 / registered-program | HISTORICAL | [source](.github/workflows/q045-reference-history-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q045-REFHIST-V2 / registered-program | ACTIVE | [source](.github/workflows/q045-reference-history-v2.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q045-REFHIST-V2 |
| Q047-CERTCHECK-V1 / registered-program | ACTIVE | [source](.github/workflows/q047-certificate-check-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q047-CERTCHECK-V1 |
| Q047-PRECURSORCHECK-V1 / registered-program | ACTIVE | [source](.github/workflows/q047-precursor-check-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q047-PRECURSORCHECK-V1 |
| Q047-COLLECTION-PREFLIGHT-V1 / registered-program | HISTORICAL | [source](.github/workflows/q047-collection-preflight-v1.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q047-RECONSTRUCTION-V1 / registered-program | ACTIVE | [source](.github/workflows/q047-reconstruction-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q047-RECONSTRUCTION-V1 |
| Q048-INPUTCHECK-V1 / registered-program | ACTIVE | [source](.github/workflows/q048-input-check-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-INPUTCHECK-V1 |
| Q048-PREFIX-V1 / registered-program | ACTIVE | [source](.github/workflows/q048-prefix-v1.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-PREFIX-V1 |
| Q048-RESUME-V2 / registered-program | DEPRECATED | [source](.github/workflows/q048-resume-v2.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-RESUME-V3 / registered-program | DEPRECATED | [source](.github/workflows/q048-resume-v3.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-RESUME-V4 / registered-program | DEPRECATED | [source](.github/workflows/q048-resume-v4.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-RESUME-V5 / registered-program | DEPRECATED | [source](.github/workflows/q048-resume-v5.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-STRUCTURAL-V6 / registered-program | DEPRECATED | [source](.github/workflows/q048-structural-v6.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-GUARDCONT-V7 / registered-program | DEPRECATED | [source](.github/workflows/q048-guard-continuation-v7.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-PHASETURN-V8 / registered-program | DEPRECATED | [source](.github/workflows/q048-phase-turn-v8.yml) | Permanent launcher rejects non-ACTIVE status; preserved as reference only |
| Q048-THRESHOLD-V9 / registered-program | ACTIVE | [source](.github/workflows/q048-threshold-anchor-v9.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-THRESHOLD-V9 |
| ENTRY-64deb6afe35f0667 / workflow | HISTORICAL | [source](.github/workflows/00-bubbleverse-start-add-only-v2.yml) | gh workflow run 00-bubbleverse-start-add-only-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-056a812a90a5d15f / workflow | HISTORICAL | [source](.github/workflows/00-bubbleverse-start-segmented-v5.yml) | gh workflow run 00-bubbleverse-start-segmented-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-c921d80deb2fa895 / workflow | HISTORICAL | [source](.github/workflows/00-bubbleverse-start-verified-v4.yml) | gh workflow run 00-bubbleverse-start-verified-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-909f1d12abab3f93 / workflow | HISTORICAL | [source](.github/workflows/00-bubbleverse-start.yml) | gh workflow run 00-bubbleverse-start.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-78fd1efaddb46cd3 / workflow | HISTORICAL | [source](.github/workflows/apply-bubbleverse-cleanup.yml) | gh workflow run apply-bubbleverse-cleanup.yml --repo Morfindien/Bubbleverse --ref main -f mode=preview |
| ENTRY-afc32716927251c0 / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v11.yml) | gh workflow run q005-hpc-v11.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2fa734aafb61cfbb / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v12.yml) | gh workflow run q005-hpc-v12.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-65da185876499295 / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v13.yml) | gh workflow run q005-hpc-v13.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e8e993f33417358f / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v14-globality-recovery.yml) | gh workflow run q005-hpc-v14-globality-recovery.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e92757a28b417adf / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v14.yml) | gh workflow run q005-hpc-v14.yml --repo Morfindien/Bubbleverse --ref main -f restarts=2 -f include_h0dn_reoptimization=false |
| ENTRY-c277e3f96f8c367b / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v5.yml) | gh workflow run q005-hpc-v5.yml --repo Morfindien/Bubbleverse --ref main -f mode=preflight |
| ENTRY-e734e86396a9b3dc / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v6.yml) | gh workflow run q005-hpc-v6.yml --repo Morfindien/Bubbleverse --ref main -f mode=preflight |
| ENTRY-9294e273653a1771 / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v7.yml) | gh workflow run q005-hpc-v7.yml --repo Morfindien/Bubbleverse --ref main -f mode=preflight |
| ENTRY-3680cac390d21600 / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v8.yml) | gh workflow run q005-hpc-v8.yml --repo Morfindien/Bubbleverse --ref main -f mode=preflight |
| ENTRY-2b002658606b2034 / workflow | HISTORICAL | [source](.github/workflows/q005-hpc-v9.yml) | gh workflow run q005-hpc-v9.yml --repo Morfindien/Bubbleverse --ref main -f mode=preflight |
| ENTRY-583bc963f0c5627b / python | HISTORICAL | [source](.github/workflows/q005_hpc_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-482412626d2dcc30 / workflow | HISTORICAL | [source](.github/workflows/q006-likelihood-attribution-v1.yml) | gh workflow run q006-likelihood-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-7a7df2baa3e13193 / workflow | HISTORICAL | [source](.github/workflows/q007-act-observable-attribution-v1.yml) | gh workflow run q007-act-observable-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-504e90e51c97d06a / workflow | HISTORICAL | [source](.github/workflows/q007-act-observable-attribution-v2.yml) | gh workflow run q007-act-observable-attribution-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-c0d94f4e7081ec8c / workflow | HISTORICAL | [source](.github/workflows/q008-globality-validation-v1.yml) | gh workflow run q008-globality-validation-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-54cdd954ca40a625 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v1.yml) | gh workflow run q009-act-corrected-minima-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-6df88cb8f09fa23b / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v2.yml) | gh workflow run q009-act-corrected-minima-attribution-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-54a4de3118333ce5 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v3.yml) | gh workflow run q009-act-corrected-minima-attribution-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e8fcff4d48a1afa7 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v4.yml) | gh workflow run q009-act-corrected-minima-attribution-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-3dab376075bb0acb / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v5.yml) | gh workflow run q009-act-corrected-minima-attribution-v5.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-f1dd563a943e5ed5 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v6.yml) | gh workflow run q009-act-corrected-minima-attribution-v6.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-888a8fcd717976b7 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v7.yml) | gh workflow run q009-act-corrected-minima-attribution-v7.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-8a9aedfadaeb38b9 / workflow | HISTORICAL | [source](.github/workflows/q009-act-corrected-minima-attribution-v8.yml) | gh workflow run q009-act-corrected-minima-attribution-v8.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-12464fa1d2665d6a / workflow | HISTORICAL | [source](.github/workflows/q010-nonact-likelihood-attribution-v1.yml) | gh workflow run q010-nonact-likelihood-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-f1bd77fc1a66ccb2 / workflow | HISTORICAL | [source](.github/workflows/q010-nonact-likelihood-attribution-v2.yml) | gh workflow run q010-nonact-likelihood-attribution-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-a79a96a3d80f12da / workflow | HISTORICAL | [source](.github/workflows/q010-nonact-likelihood-attribution-v3.yml) | gh workflow run q010-nonact-likelihood-attribution-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-f99b07ea119c1d57 / workflow | HISTORICAL | [source](.github/workflows/q011-ede-globality-certification-v1.yml) | gh workflow run q011-ede-globality-certification-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-da733cebc1fd9416 / workflow | HISTORICAL | [source](.github/workflows/q011-ede-globality-certification-v2.yml) | gh workflow run q011-ede-globality-certification-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-172bdd899ee0f9d9 / workflow | HISTORICAL | [source](.github/workflows/q011-ede-globality-certification-v3.yml) | gh workflow run q011-ede-globality-certification-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-220a69d81b9803b3 / workflow | HISTORICAL | [source](.github/workflows/q011-ede-globality-certification-v4.yml) | gh workflow run q011-ede-globality-certification-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e333b5f961bef8be / workflow | HISTORICAL | [source](.github/workflows/q012-likelihood-attribution-v1.yml) | gh workflow run q012-likelihood-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-3563d7adc47a802d / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v1.yml) | gh workflow run q014-external-viability-v1.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-6178f91109a9937f / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v10.yml) | gh workflow run q014-external-viability-v10.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-206002f38068070f / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v11.yml) | gh workflow run q014-external-viability-v11.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-6b4331976fc5fa15 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v12.yml) | gh workflow run q014-external-viability-v12.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-fa106e71dbdd0245 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v2.yml) | gh workflow run q014-external-viability-v2.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-c2b5cd067a553d54 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v3.yml) | gh workflow run q014-external-viability-v3.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-55ae798319151df0 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v4.yml) | gh workflow run q014-external-viability-v4.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-0d3eef14cf965fe4 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v5.yml) | gh workflow run q014-external-viability-v5.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-77fb227b8fff02f8 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v6.yml) | gh workflow run q014-external-viability-v6.yml --repo Morfindien/Bubbleverse --ref main -f depth=expanded |
| ENTRY-b6734cdf17922903 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v7.yml) | gh workflow run q014-external-viability-v7.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-7be72a8aec24e0b6 / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v8.yml) | gh workflow run q014-external-viability-v8.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-c89b041af306f97a / workflow | HISTORICAL | [source](.github/workflows/q014-external-viability-v9.yml) | gh workflow run q014-external-viability-v9.yml --repo Morfindien/Bubbleverse --ref main -f depth=standard |
| ENTRY-85a25f7ea6bacfd6 / workflow | HISTORICAL | [source](.github/workflows/q015-cmb-attribution-v1.yml) | gh workflow run q015-cmb-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-f3ce77ef5dd1e87b / workflow | HISTORICAL | [source](.github/workflows/q015-cmb-attribution-v2.yml) | gh workflow run q015-cmb-attribution-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-9130ff1cab9c5ac3 / workflow | HISTORICAL | [source](.github/workflows/q015-cmb-attribution-v3.yml) | gh workflow run q015-cmb-attribution-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-0ca2d89f9290c9eb / workflow | HISTORICAL | [source](.github/workflows/q016-cmb-mechanism-v1.yml) | gh workflow run q016-cmb-mechanism-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-7528898675b2ee2d / workflow | HISTORICAL | [source](.github/workflows/q016-cmb-mechanism-v2.yml) | gh workflow run q016-cmb-mechanism-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-b751d249e46d741b / workflow | HISTORICAL | [source](.github/workflows/q016-cmb-mechanism-v3.yml) | gh workflow run q016-cmb-mechanism-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-d8d16f44e746f1e4 / workflow | HISTORICAL | [source](.github/workflows/q016-cmb-mechanism-v4.yml) | gh workflow run q016-cmb-mechanism-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-a38db57ca5b82e6d / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v1.yml) | gh workflow run q016-matched-cmb-surface-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-b9f181ce02454da2 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v10.yml) | gh workflow run q016-matched-cmb-surface-v10.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-51abba63bddca8af / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v11.yml) | gh workflow run q016-matched-cmb-surface-v11.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-6022b65e3dbb1829 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v12.yml) | gh workflow run q016-matched-cmb-surface-v12.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-61ca0f39a9367c9f / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v14.yml) | gh workflow run q016-matched-cmb-surface-v14.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e5555fb0b7fde46e / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v15.yml) | gh workflow run q016-matched-cmb-surface-v15.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-53ca2f151a2441eb / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v16.yml) | gh workflow run q016-matched-cmb-surface-v16.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-d5e0e6a1d586a5ed / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v2.yml) | gh workflow run q016-matched-cmb-surface-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-06aeac548285a961 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v3.yml) | gh workflow run q016-matched-cmb-surface-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2ab02341437067ad / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v4.yml) | gh workflow run q016-matched-cmb-surface-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e1f98b250be28db2 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v5.yml) | gh workflow run q016-matched-cmb-surface-v5.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-da41f3788ccf0a27 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v6.yml) | gh workflow run q016-matched-cmb-surface-v6.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-1b04ae7ad9690f54 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v7.yml) | gh workflow run q016-matched-cmb-surface-v7.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-d2e4bb68d2ac9144 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v8.yml) | gh workflow run q016-matched-cmb-surface-v8.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-12af672fcc794e83 / workflow | HISTORICAL | [source](.github/workflows/q016-matched-cmb-surface-v9.yml) | gh workflow run q016-matched-cmb-surface-v9.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-d748ac0b811fc7c9 / workflow | HISTORICAL | [source](.github/workflows/q017-planck-direction-localization-v1.yml) | gh workflow run q017-planck-direction-localization-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e80082e76fcfabe8 / workflow | HISTORICAL | [source](.github/workflows/q017-planck-direction-localization-v2.yml) | gh workflow run q017-planck-direction-localization-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-6db819807134eb45 / workflow | HISTORICAL | [source](.github/workflows/q017-planck-direction-localization-v3.yml) | gh workflow run q017-planck-direction-localization-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-75fdffabfe98b07b / workflow | HISTORICAL | [source](.github/workflows/q018-planck-likelihood-bridge-v1.yml) | gh workflow run q018-planck-likelihood-bridge-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-7c738e9559f18f5b / workflow | HISTORICAL | [source](.github/workflows/q018-planck-likelihood-bridge-v2.yml) | gh workflow run q018-planck-likelihood-bridge-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-a046569c7309c14e / workflow | HISTORICAL | [source](.github/workflows/q018-planck-likelihood-bridge-v3.yml) | gh workflow run q018-planck-likelihood-bridge-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-46463f517f50ff31 / workflow | HISTORICAL | [source](.github/workflows/q019-planck-cosmology-reprofile-v1.yml) | gh workflow run q019-planck-cosmology-reprofile-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-5c50c57e38045aa4 / workflow | HISTORICAL | [source](.github/workflows/q019-planck-globality-repair-v2.yml) | gh workflow run q019-planck-globality-repair-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-af9273579a6dd575 / workflow | HISTORICAL | [source](.github/workflows/q019-planck-globality-repair-v3.yml) | gh workflow run q019-planck-globality-repair-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-33a36f0cb4b44703 / workflow | HISTORICAL | [source](.github/workflows/q020-cross-profile-gate-repair-v2.yml) | gh workflow run q020-cross-profile-gate-repair-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-179dac115807ef7d / workflow | HISTORICAL | [source](.github/workflows/q020-planck-cross-profile-direction-v1.yml) | gh workflow run q020-planck-cross-profile-direction-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2f34b980f8b4e288 / workflow | HISTORICAL | [source](.github/workflows/q021-coherent-restart-gate-repair-v2.yml) | gh workflow run q021-coherent-restart-gate-repair-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-52d3c3806b159faf / workflow | HISTORICAL | [source](.github/workflows/q021-primordial-internal-structure-v1.yml) | gh workflow run q021-primordial-internal-structure-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-cb1bad3a5d157a3f / workflow | HISTORICAL | [source](.github/workflows/q022-optimizer-basin-continuation-v2.yml) | gh workflow run q022-optimizer-basin-continuation-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-fca69f6e2eb50a96 / workflow | HISTORICAL | [source](.github/workflows/q022-optimizer-basin-diagnostic-v1.yml) | gh workflow run q022-optimizer-basin-diagnostic-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-78510a321d25abb3 / workflow | HISTORICAL | [source](.github/workflows/q023-read-only-basin-directions-v1.yml) | gh workflow run q023-read-only-basin-directions-v1.yml --repo Morfindien/Bubbleverse --ref main -f q022_run_id= |
| ENTRY-f5db8a0ac65e3c86 / workflow | HISTORICAL | [source](.github/workflows/q023-read-only-basin-directions-v2.yml) | gh workflow run q023-read-only-basin-directions-v2.yml --repo Morfindien/Bubbleverse --ref main -f q022_run_id= |
| ENTRY-e63ac75f9847005a / workflow | HISTORICAL | [source](.github/workflows/q024-read-only-basin-matching-v1.yml) | gh workflow run q024-read-only-basin-matching-v1.yml --repo Morfindien/Bubbleverse --ref main -f q022_run_id= |
| ENTRY-c6eb73b816da6f2d / workflow | HISTORICAL | [source](.github/workflows/q025-fullmf-component-attribution-v1.yml) | gh workflow run q025-fullmf-component-attribution-v1.yml --repo Morfindien/Bubbleverse --ref main -f q022_run_id= |
| ENTRY-73f0201ceaab9258 / workflow | HISTORICAL | [source](.github/workflows/q025-fullmf-component-attribution-v2.yml) | gh workflow run q025-fullmf-component-attribution-v2.yml --repo Morfindien/Bubbleverse --ref main -f q022_run_id= |
| ENTRY-7516ec6b477203ad / workflow | HISTORICAL | [source](.github/workflows/q026-mask6-nuisance-localization-v1.yml) | gh workflow run q026-mask6-nuisance-localization-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-1bac0d17845dde7b / workflow | HISTORICAL | [source](.github/workflows/q027-residual-covariance-bridge-v1.yml) | gh workflow run q027-residual-covariance-bridge-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-9d749f59ce8dd9b6 / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v1.yml) | gh workflow run q028-common-support-counterfactual-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-d0b78dee4d7772dc / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v2.yml) | gh workflow run q028-common-support-counterfactual-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-fbc07bdad3e283cd / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v3.yml) | gh workflow run q028-common-support-counterfactual-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-5627678773b25de3 / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v4.yml) | gh workflow run q028-common-support-counterfactual-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-1087f19df381e5a9 / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v5.yml) | gh workflow run q028-common-support-counterfactual-v5.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-b767464943c4feb1 / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v6.yml) | gh workflow run q028-common-support-counterfactual-v6.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-5fb92a938537f7de / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v7.yml) | gh workflow run q028-common-support-counterfactual-v7.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-af888e4ebe0db4b6 / workflow | HISTORICAL | [source](.github/workflows/q028-common-support-counterfactual-v8.yml) | gh workflow run q028-common-support-counterfactual-v8.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-56d7c92688bccc20 / workflow | HISTORICAL | [source](.github/workflows/q030-interaction-preserving-decomposition-v1.yml) | gh workflow run q030-interaction-preserving-decomposition-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-376c91831d40bd95 / workflow | HISTORICAL | [source](.github/workflows/q030-interaction-preserving-decomposition-v2.yml) | gh workflow run q030-interaction-preserving-decomposition-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-78b8e107ba1b1d9e / workflow | HISTORICAL | [source](.github/workflows/q030-original-gate-audit-finalization-r1.yml) | gh workflow run q030-original-gate-audit-finalization-r1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2d22676634ef7e46 / workflow | HISTORICAL | [source](.github/workflows/q030-original-gate-precision-audit-v1.yml) | gh workflow run q030-original-gate-precision-audit-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-350742dc082fe7ac / workflow | HISTORICAL | [source](.github/workflows/q030-validation-repair-v3.yml) | gh workflow run q030-validation-repair-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-f5fb52a8f465ca80 / workflow | HISTORICAL | [source](.github/workflows/q031-planck-portability-v1.yml) | gh workflow run q031-planck-portability-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-74d037d6f6384933 / workflow | HISTORICAL | [source](.github/workflows/q031-planck-portability-v2.yml) | gh workflow run q031-planck-portability-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-ad93e2da093b2fe4 / workflow | HISTORICAL | [source](.github/workflows/q031-planck-portability-v3.yml) | gh workflow run q031-planck-portability-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-af092f8800a97602 / workflow | HISTORICAL | [source](.github/workflows/q031-planck-portability-v4.yml) | gh workflow run q031-planck-portability-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-ae532a327d0d79b1 / workflow | HISTORICAL | [source](.github/workflows/q032-camspec-addback-v3.yml) | gh workflow run q032-camspec-addback-v3.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2d1ff8037988914e / workflow | HISTORICAL | [source](.github/workflows/q032-exact-start-addback-v4.yml) | gh workflow run q032-exact-start-addback-v4.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-ca78458b872f596c / workflow | HISTORICAL | [source](.github/workflows/q032-planck-tt3pair-bridge-v1.yml) | gh workflow run q032-planck-tt3pair-bridge-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-e6053bb3b47d5076 / workflow | HISTORICAL | [source](.github/workflows/q032-planck-tt3pair-bridge-v2.yml) | gh workflow run q032-planck-tt3pair-bridge-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-ea8ecec54cb392e3 / workflow | HISTORICAL | [source](.github/workflows/q033-launch-semantics-matched-ab-v1.yml) | gh workflow run q033-launch-semantics-matched-ab-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-0a322916cd923677 / workflow | HISTORICAL | [source](.github/workflows/q033-launch-semantics-protocol-audit-v2.yml) | gh workflow run q033-launch-semantics-protocol-audit-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-b6f44b403e658490 / workflow | HISTORICAL | [source](.github/workflows/q034-primordial-freeze-isolation-v1.yml) | gh workflow run q034-primordial-freeze-isolation-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-c3fb7c5a0db472bb / workflow | HISTORICAL | [source](.github/workflows/q035-classifier-harmonization-v1.yml) | gh workflow run q035-classifier-harmonization-v1.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-2d89097af4c1aa67 / workflow | HISTORICAL | [source](.github/workflows/q035-classifier-harmonization-v2.yml) | gh workflow run q035-classifier-harmonization-v2.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-02100a3dc19acf43 / workflow | HISTORICAL | [source](.github/workflows/q036-endpoint-geometry-portability-v1_REPLACE.yml) | gh workflow run q036-endpoint-geometry-portability-v1_REPLACE.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-b2ceb13e97ace975 / workflow | HISTORICAL | [source](.github/workflows/q036-endpoint-geometry-portability-v2.yml) | gh workflow run q036-endpoint-geometry-portability-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-cc7c503fd7f1cf15 / workflow | HISTORICAL | [source](.github/workflows/q036-endpoint-geometry-portability-v3.yml) | gh workflow run q036-endpoint-geometry-portability-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-6b693f4522c18251 / workflow | HISTORICAL | [source](.github/workflows/q036-endpoint-geometry-portability-v4.yml) | gh workflow run q036-endpoint-geometry-portability-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-df5e3d5c196b4eff / workflow | HISTORICAL | [source](.github/workflows/q036-endpoint-geometry-portability-v5.yml) | gh workflow run q036-endpoint-geometry-portability-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-9c8df13e89c2f739 / workflow | HISTORICAL | [source](.github/workflows/q037-common-support-endpoint-geometry-v1.yml) | gh workflow run q037-common-support-endpoint-geometry-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-1f94765a99ee4a1e / workflow | HISTORICAL | [source](.github/workflows/q038-coordinate-localization-v1.yml) | gh workflow run q038-coordinate-localization-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-3dbc68ac542d6c24 / workflow | HISTORICAL | [source](.github/workflows/q039-implementation-block-intervention-v1-fixed.yml) | gh workflow run q039-implementation-block-intervention-v1-fixed.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-IMPLBLOCK-V1 |
| ENTRY-69ccf56343a6a27c / workflow | HISTORICAL | [source](.github/workflows/q039-implementation-block-intervention-v2.yml) | gh workflow run q039-implementation-block-intervention-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-IMPLBLOCK-V2 |
| ENTRY-041a0cf543fe75b8 / workflow | HISTORICAL | [source](.github/workflows/q039-implementation-block-intervention-v3.yml) | gh workflow run q039-implementation-block-intervention-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-IMPLBLOCK-V3 |
| ENTRY-bbc6bfbc270364c6 / workflow | HISTORICAL | [source](.github/workflows/q039-implementation-block-intervention-v5.yml) | gh workflow run q039-implementation-block-intervention-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-IMPLBLOCK-V5 |
| ENTRY-cee8d5a3165527e5 / workflow | HISTORICAL | [source](.github/workflows/q039-native-foreground-profile-v1.yml) | gh workflow run q039-native-foreground-profile-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q039-FGPROFILE-V1 |
| ENTRY-05f899f0e0387d8b / python | HISTORICAL | [source](.github/workflows/q039_implementation_block_intervention_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4def70f43eedc61a / workflow | HISTORICAL | [source](.github/workflows/q040-cmbspace-compression-seal-v5.yml) | gh workflow run q040-cmbspace-compression-seal-v5.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-4eefa5891d99b855 / workflow | HISTORICAL | [source](.github/workflows/q040-cmbspace-coupled-bridge-v1.yml) | gh workflow run q040-cmbspace-coupled-bridge-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-CMBSPACE-V1 |
| ENTRY-b4175d4954b2e105 / workflow | HISTORICAL | [source](.github/workflows/q040-cmbspace-coupled-bridge-v2.yml) | gh workflow run q040-cmbspace-coupled-bridge-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-CMBSPACE-V2 |
| ENTRY-c745bfc7f523cccd / workflow | HISTORICAL | [source](.github/workflows/q040-cmbspace-coupled-bridge-v3.yml) | gh workflow run q040-cmbspace-coupled-bridge-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-CMBSPACE-V3 |
| ENTRY-1ca708d610a969fd / workflow | HISTORICAL | [source](.github/workflows/q040-cmbspace-coupled-bridge-v4.yml) | gh workflow run q040-cmbspace-coupled-bridge-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-CMBSPACE-V4 |
| ENTRY-c140cd006f131c80 / workflow | HISTORICAL | [source](.github/workflows/q040-defensive-rqmc-v1.yml) | gh workflow run q040-defensive-rqmc-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-RQMC-V1 |
| ENTRY-46649d7988298ebc / workflow | HISTORICAL | [source](.github/workflows/q040-defensive-rqmc-v2.yml) | gh workflow run q040-defensive-rqmc-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-RQMC-V2 |
| ENTRY-56792a3d996b975d / workflow | HISTORICAL | [source](.github/workflows/q040-defensive-rqmc-v3.yml) | gh workflow run q040-defensive-rqmc-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-RQMC-V3 |
| ENTRY-4569cadc7cf5e412 / workflow | HISTORICAL | [source](.github/workflows/q040-defensive-rqmc-v4.yml) | gh workflow run q040-defensive-rqmc-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q040-RQMC-V4 |
| ENTRY-12c61434be11cd91 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v1.yml) | gh workflow run q041-planck-portability-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-83f22d4555358120 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v10.yml) | gh workflow run q041-planck-portability-v10.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-da61f34d9e155b60 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v11.yml) | gh workflow run q041-planck-portability-v11.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-1bc21f7187689751 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v12.yml) | gh workflow run q041-planck-portability-v12.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-2037f591dbee6638 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v13.yml) | gh workflow run q041-planck-portability-v13.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-e1a1535e2157332c / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v14.yml) | gh workflow run q041-planck-portability-v14.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f segment=1 |
| ENTRY-2d2aaa18861eadbe / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v15.yml) | gh workflow run q041-planck-portability-v15.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f segment=1 |
| ENTRY-e82412779f42fe82 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v16.yml) | gh workflow run q041-planck-portability-v16.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f segment=1 -f series_id= |
| ENTRY-72ae87831275c5a0 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v17.yml) | gh workflow run q041-planck-portability-v17.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f segment=1 -f series_id= |
| ENTRY-f092018e2dc39735 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v18.yml) | gh workflow run q041-planck-portability-v18.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-78f647f1f4609ab4 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v19.yml) | gh workflow run q041-planck-portability-v19.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-9b92764b2d78fe62 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v2.yml) | gh workflow run q041-planck-portability-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-937918e1a378ef59 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v3.yml) | gh workflow run q041-planck-portability-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-e6bb6aea8d6eb46a / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v4.yml) | gh workflow run q041-planck-portability-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-0effeaf54e87b93d / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v5.yml) | gh workflow run q041-planck-portability-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-d83bb1ccbc65c3cb / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v6.yml) | gh workflow run q041-planck-portability-v6.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-88b3fd8b1bc5bbbe / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v7.yml) | gh workflow run q041-planck-portability-v7.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-a1886982901507c7 / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v8.yml) | gh workflow run q041-planck-portability-v8.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-8c08376f088baafc / workflow | HISTORICAL | [source](.github/workflows/q041-planck-portability-v9.yml) | gh workflow run q041-planck-portability-v9.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-542c180e0dc4e835 / workflow | HISTORICAL | [source](.github/workflows/q042-class-cause-v23.yml) | gh workflow run q042-class-cause-v23.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-8737a0b58fbc4b11 / workflow | HISTORICAL | [source](.github/workflows/q042-class-nan-v25.yml) | gh workflow run q042-class-nan-v25.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-5e5b3c5bff79489e / workflow | HISTORICAL | [source](.github/workflows/q042-class-origin-v24.yml) | gh workflow run q042-class-origin-v24.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-c3c6c5666bde4087 / workflow | HISTORICAL | [source](.github/workflows/q042-context-v29.yml) | gh workflow run q042-context-v29.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-04ee567dc6bf27f5 / workflow | HISTORICAL | [source](.github/workflows/q042-durable-v22.yml) | gh workflow run q042-durable-v22.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-c08941f47c34e407 / workflow | HISTORICAL | [source](.github/workflows/q042-event-cell-v28.yml) | gh workflow run q042-event-cell-v28.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-dc14c6ff0ecc41a3 / workflow | HISTORICAL | [source](.github/workflows/q042-execution-mechanism-v1.yml) | gh workflow run q042-execution-mechanism-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-eb5644b6295e7645 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v10.yml) | gh workflow run q042-planck-portability-v10.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-679e4e3c922641bb / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v11.yml) | gh workflow run q042-planck-portability-v11.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-cfa06d3ab9a33fc3 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v2.yml) | gh workflow run q042-planck-portability-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-00a53455dc86d932 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v3.yml) | gh workflow run q042-planck-portability-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-0455a976dad5ca09 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v4.yml) | gh workflow run q042-planck-portability-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-3e4b8b943a6eab1b / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v5.yml) | gh workflow run q042-planck-portability-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-11f981428f0b7f13 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v6.yml) | gh workflow run q042-planck-portability-v6.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-6140500685378af3 / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v7.yml) | gh workflow run q042-planck-portability-v7.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-e1fcf174e392126d / workflow | HISTORICAL | [source](.github/workflows/q042-planck-portability-v9.yml) | gh workflow run q042-planck-portability-v9.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-5bed601c57cc9c4d / workflow | HISTORICAL | [source](.github/workflows/q042-production-v1.yml) | gh workflow run q042-production-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-04a167a940ab3cf0 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v11.yml) | gh workflow run q042-production-v11.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-4f434cffcb11f06e / workflow | HISTORICAL | [source](.github/workflows/q042-production-v12.yml) | gh workflow run q042-production-v12.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-be0bc0d82e85a7ec / workflow | HISTORICAL | [source](.github/workflows/q042-production-v13.yml) | gh workflow run q042-production-v13.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-aa0cfea7c6b2ec83 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v15.yml) | gh workflow run q042-production-v15.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-49f46e3e82b32196 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v16.yml) | gh workflow run q042-production-v16.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-f7cb288e8983777e / workflow | HISTORICAL | [source](.github/workflows/q042-production-v17.yml) | gh workflow run q042-production-v17.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-be053d00431d66fc / workflow | HISTORICAL | [source](.github/workflows/q042-production-v18.yml) | gh workflow run q042-production-v18.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-9d67d36790565cef / workflow | HISTORICAL | [source](.github/workflows/q042-production-v19.yml) | gh workflow run q042-production-v19.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q042-PROD-V19 -f v18_root_run_id=36731879692 |
| ENTRY-77ca7c11f1101cca / workflow | HISTORICAL | [source](.github/workflows/q042-production-v2.yml) | gh workflow run q042-production-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-836d9c62f9915b0a / workflow | HISTORICAL | [source](.github/workflows/q042-production-v3.yml) | gh workflow run q042-production-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-eb572635296ae53a / workflow | HISTORICAL | [source](.github/workflows/q042-production-v4.yml) | gh workflow run q042-production-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-798eebc18d287a83 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v5.yml) | gh workflow run q042-production-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-f25af43ea841d5ea / workflow | HISTORICAL | [source](.github/workflows/q042-production-v6.yml) | gh workflow run q042-production-v6.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-ae5f84e09dd46cb9 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v7.yml) | gh workflow run q042-production-v7.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-54825a4371163e14 / workflow | HISTORICAL | [source](.github/workflows/q042-production-v8.yml) | gh workflow run q042-production-v8.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-9b30d9f2a8726edf / workflow | HISTORICAL | [source](.github/workflows/q042-production-v9.yml) | gh workflow run q042-production-v9.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID -f mode=bootstrap -f arm= -f model= -f combination= -f segment=0 -f previous_run_id= -f root_run_id= -f collector_round=0 |
| ENTRY-383c1906724144d0 / workflow | HISTORICAL | [source](.github/workflows/q042-reference-acquisition-v26.yml) | gh workflow run q042-reference-acquisition-v26.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-55fa6fd655779253 / workflow | HISTORICAL | [source](.github/workflows/q042-stock-diagnostic-v20.yml) | gh workflow run q042-stock-diagnostic-v20.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-5f445166f3ce05b0 / workflow | HISTORICAL | [source](.github/workflows/q042-stock-diagnostic-v21.yml) | gh workflow run q042-stock-diagnostic-v21.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-8d0105706eb4dd58 / workflow | HISTORICAL | [source](.github/workflows/q042-switch-probe-v27.yml) | gh workflow run q042-switch-probe-v27.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-7fa652b728fc1b79 / python | HISTORICAL | [source](.github/workflows/q042_apply_readme_patch_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4699ebd163776e72 / python | HISTORICAL | [source](.github/workflows/q042_apply_registry_patch_prod_v11.py) | python .github/workflows/q042_apply_registry_patch_prod_v11.py |
| ENTRY-9b1b5ed241610706 / workflow | HISTORICAL | [source](.github/workflows/q045-native-baseline-v1.yml) | gh workflow run q045-native-baseline-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-096b0b817f793bcb / workflow | HISTORICAL | [source](.github/workflows/q045-native-baseline-v2.yml) | gh workflow run q045-native-baseline-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-6e2e70592c8d2a1e / workflow | HISTORICAL | [source](.github/workflows/q045-optical-audit-v1.yml) | gh workflow run q045-optical-audit-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-56f539dacb8ab606 / workflow | HISTORICAL | [source](.github/workflows/q045-optical-audit-v2.yml) | gh workflow run q045-optical-audit-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-ee3b344dd7c78d9b / workflow | HISTORICAL | [source](.github/workflows/q045-optical-audit-v3.yml) | gh workflow run q045-optical-audit-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-a54ebfab8e669236 / workflow | HISTORICAL | [source](.github/workflows/q045-reference-history-v1.yml) | gh workflow run q045-reference-history-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-37cfc8dea8f2ef51 / workflow | HISTORICAL | [source](.github/workflows/q045-reference-history-v2.yml) | gh workflow run q045-reference-history-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-f3b2b305188df7bc / workflow | HISTORICAL | [source](.github/workflows/q047-certificate-check-v1.yml) | gh workflow run q047-certificate-check-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-904beb9f42d4fd84 / workflow | HISTORICAL | [source](.github/workflows/q047-collection-preflight-v1.yml) | gh workflow run q047-collection-preflight-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-012e662168ef7bda / workflow | HISTORICAL | [source](.github/workflows/q047-precursor-check-v1.yml) | gh workflow run q047-precursor-check-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-b4e360898ab9d44a / workflow | HISTORICAL | [source](.github/workflows/q047-reconstruction-v1.yml) | gh workflow run q047-reconstruction-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=REPLACE_PROGRAM_ID |
| ENTRY-79ceabc6dcd22367 / workflow | HISTORICAL | [source](.github/workflows/q048-guard-continuation-v7.yml) | gh workflow run q048-guard-continuation-v7.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-GUARDCONT-V7 |
| ENTRY-6a4f31f8aa22b7db / workflow | HISTORICAL | [source](.github/workflows/q048-input-check-v1.yml) | gh workflow run q048-input-check-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-INPUTCHECK-V1 |
| ENTRY-21a30a1730d54fb6 / workflow | HISTORICAL | [source](.github/workflows/q048-install-threshold-v9.yml) | gh workflow run q048-install-threshold-v9.yml --repo Morfindien/Bubbleverse --ref main |
| ENTRY-a11a0d878011487c / workflow | HISTORICAL | [source](.github/workflows/q048-phase-turn-v8.yml) | gh workflow run q048-phase-turn-v8.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-PHASETURN-V8 |
| ENTRY-407cc228c15068ef / workflow | HISTORICAL | [source](.github/workflows/q048-prefix-v1.yml) | gh workflow run q048-prefix-v1.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-PREFIX-V1 |
| ENTRY-e8549a12f33ad686 / workflow | HISTORICAL | [source](.github/workflows/q048-resume-v2.yml) | gh workflow run q048-resume-v2.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-RESUME-V2 |
| ENTRY-e8683b2269f7bcd4 / workflow | HISTORICAL | [source](.github/workflows/q048-resume-v3.yml) | gh workflow run q048-resume-v3.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-RESUME-V3 |
| ENTRY-66f7e7de8b060321 / workflow | HISTORICAL | [source](.github/workflows/q048-resume-v4.yml) | gh workflow run q048-resume-v4.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-RESUME-V4 |
| ENTRY-cb18d9e2e97ee793 / workflow | HISTORICAL | [source](.github/workflows/q048-resume-v5.yml) | gh workflow run q048-resume-v5.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-RESUME-V5 |
| ENTRY-717c838333f5cf58 / workflow | HISTORICAL | [source](.github/workflows/q048-structural-v6.yml) | gh workflow run q048-structural-v6.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-STRUCTURAL-V6 |
| ENTRY-b88cf12d6fa52d96 / workflow | HISTORICAL | [source](.github/workflows/q048-threshold-anchor-v9.yml) | gh workflow run q048-threshold-anchor-v9.yml --repo Morfindien/Bubbleverse --ref main -f program_id=Q048-THRESHOLD-V9 |
| ENTRY-50d9a1d884a96def / workflow | HISTORICAL | [source](q005-hpc-v11.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-290d5b2e65b1d44b / python | HISTORICAL | [source](q005_globality_recovery_v14-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cab14ce1b1f68d23 / python | HISTORICAL | [source](q005_globality_recovery_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e38a7bf1e3caebe2 / python | HISTORICAL | [source](q005_hpc_v11-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9ba4d7757a4fd029 / python | HISTORICAL | [source](q005_hpc_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3aebb26a31aa5f2f / python | HISTORICAL | [source](q005_hpc_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-83d71db73eaaca20 / python | HISTORICAL | [source](q005_hpc_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6d03644467b5aa78 / python | HISTORICAL | [source](q005_hpc_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6292bf5c7f2f4c66 / python | HISTORICAL | [source](q005_hpc_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dfc3c7aea49627f6 / python | HISTORICAL | [source](q005_hpc_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a21378139ad69011 / python | HISTORICAL | [source](q005_hpc_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9977fbc80c16b51b / python | HISTORICAL | [source](q005_hpc_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-53ee4aebcee573a7 / python | HISTORICAL | [source](q005_hpc_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ee031b099ff4d34a / shell | HISTORICAL | [source](q005_setup_v14.sh) | bash q005_setup_v14.sh |
| ENTRY-1225b4aa53a4f5d2 / python | HISTORICAL | [source](q005_validate_v11-1.py) | python q005_validate_v11-1.py |
| ENTRY-db2faba44a4a3575 / python | HISTORICAL | [source](q005_validate_v11.py) | python q005_validate_v11.py |
| ENTRY-f95d4482c2a8f785 / python | HISTORICAL | [source](q005_validate_v12.py) | python q005_validate_v12.py |
| ENTRY-b3406737af72e0d6 / python | HISTORICAL | [source](q005_validate_v13.py) | python q005_validate_v13.py |
| ENTRY-73f731b6ec0a1e56 / python | HISTORICAL | [source](q005_validate_v14.py) | python q005_validate_v14.py |
| ENTRY-2817c0b1d972170e / python | HISTORICAL | [source](q005_validate_v5.py) | python q005_validate_v5.py |
| ENTRY-59454fdee5ee5cd3 / python | HISTORICAL | [source](q005_validate_v6.py) | python q005_validate_v6.py |
| ENTRY-d9914f66d4e143fd / python | HISTORICAL | [source](q005_validate_v7.py) | python q005_validate_v7.py |
| ENTRY-85fd353254be3ab7 / python | HISTORICAL | [source](q005_validate_v8.py) | python q005_validate_v8.py |
| ENTRY-00b5eb2d27e96c47 / python | HISTORICAL | [source](q005_validate_v9.py) | python q005_validate_v9.py |
| ENTRY-e272fccb09d3a90f / python | HISTORICAL | [source](q006_likelihood_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1cfc4f8270d3b560 / python | HISTORICAL | [source](q007_act_observable_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-624fa1e50221c7f3 / python | HISTORICAL | [source](q007_act_observable_attribution_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b81b7974549388e5 / python | HISTORICAL | [source](q008_globality_validation_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-182c097a02d27e2c / workflow | HISTORICAL | [source](q009-act-corrected-minima-attribution-v1.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-f17a93f00f8c4731 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v1-2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b2ac447477320cef / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c93ac1064816b812 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v2-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-53b9a654c99d315a / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-89cd7331b1a57537 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6fa1afcd26b86982 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dfda0d306a94f077 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fe921f23022ecf6b / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e372ee6a05aac616 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ae4b63514c3dff86 / python | HISTORICAL | [source](q009_act_corrected_minima_attribution_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-90b3b1239cdbe39e / python | HISTORICAL | [source](q010_nonact_likelihood_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-56b2aee835adfaef / python | HISTORICAL | [source](q010_nonact_likelihood_attribution_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2bb08c11e1a46ded / python | HISTORICAL | [source](q010_nonact_likelihood_attribution_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2e4dbcc52dd7c5b1 / python | HISTORICAL | [source](q011_ede_globality_certification_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c3928e1b96029913 / python | HISTORICAL | [source](q011_ede_globality_certification_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-42ce7c5566dc3da9 / python | HISTORICAL | [source](q011_ede_globality_certification_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-beebdfdf2567d824 / python | HISTORICAL | [source](q011_ede_globality_certification_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3c4fcd59e443ad9c / python | HISTORICAL | [source](q012_likelihood_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-613b251b78f2a820 / workflow | HISTORICAL | [source](q014-external-viability-v10.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-d753299f81e1915c / python | HISTORICAL | [source](q014_aggregate_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2bd0e14b14a70dd3 / python | HISTORICAL | [source](q014_aggregate_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-35ca58a7f25ac1a9 / python | HISTORICAL | [source](q014_aggregate_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a101af6686231335 / python | HISTORICAL | [source](q014_aggregate_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f16bdedc73eed53c / python | HISTORICAL | [source](q014_aggregate_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-765c8fd4606d5381 / python | HISTORICAL | [source](q014_aggregate_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-08a6c6f3f6b958ba / python | HISTORICAL | [source](q014_aggregate_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bfedcd366396b944 / python | HISTORICAL | [source](q014_aggregate_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-277c79e18f0920be / python | HISTORICAL | [source](q014_aggregate_v6.py) | python q014_aggregate_v6.py |
| ENTRY-af65d083fb9d7bae / python | HISTORICAL | [source](q014_aggregate_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ebeb77583f8754f2 / python | HISTORICAL | [source](q014_aggregate_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c98a19b336eaea49 / python | HISTORICAL | [source](q014_aggregate_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c277f389f78da08d / python | HISTORICAL | [source](q014_external_viability_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f91dc37a6121e4f3 / python | HISTORICAL | [source](q014_external_viability_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-608c32c73dfa22d5 / python | HISTORICAL | [source](q014_external_viability_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b4968ec729ba65e7 / python | HISTORICAL | [source](q014_external_viability_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-eb3443edf6c36f59 / python | HISTORICAL | [source](q014_external_viability_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5fdbe73a508559ed / python | HISTORICAL | [source](q014_external_viability_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-af4fbe8a0d8e44b1 / python | HISTORICAL | [source](q014_external_viability_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e41152220f74d133 / python | HISTORICAL | [source](q014_external_viability_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-39f001ec5dbf3c97 / python | HISTORICAL | [source](q014_external_viability_v6.py) | python q014_external_viability_v6.py |
| ENTRY-000d07b30cd1a69a / python | HISTORICAL | [source](q014_external_viability_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0b595493880b8ab4 / python | HISTORICAL | [source](q014_external_viability_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1d64bb8f2aae557a / python | HISTORICAL | [source](q014_external_viability_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e57030d5a2fc49a0 / shell | HISTORICAL | [source](q014_setup_v1.sh) | bash q014_setup_v1.sh |
| ENTRY-3a9ac3bbc420a954 / shell | HISTORICAL | [source](q014_setup_v10.sh) | bash q014_setup_v10.sh |
| ENTRY-d460339006dff1b0 / shell | HISTORICAL | [source](q014_setup_v11.sh) | bash q014_setup_v11.sh |
| ENTRY-e1120339b3628035 / shell | HISTORICAL | [source](q014_setup_v12.sh) | bash q014_setup_v12.sh |
| ENTRY-01f1b6f814d74b2b / shell | HISTORICAL | [source](q014_setup_v2.sh) | bash q014_setup_v2.sh |
| ENTRY-c9fcc5b026e515ae / shell | HISTORICAL | [source](q014_setup_v3.sh) | bash q014_setup_v3.sh |
| ENTRY-6fd58a560888b150 / shell | HISTORICAL | [source](q014_setup_v4.sh) | bash q014_setup_v4.sh |
| ENTRY-cdcb2bed9cb8fe0f / shell | HISTORICAL | [source](q014_setup_v5.sh) | bash q014_setup_v5.sh |
| ENTRY-11d1eecd0b923f04 / shell | HISTORICAL | [source](q014_setup_v6.sh) | bash q014_setup_v6.sh |
| ENTRY-46f0d781ba0eac69 / shell | HISTORICAL | [source](q014_setup_v8.sh) | bash q014_setup_v8.sh |
| ENTRY-9fd5fe1047c78b79 / shell | HISTORICAL | [source](q014_setup_v9.sh) | bash q014_setup_v9.sh |
| ENTRY-ccbca7226ba19f86 / python | HISTORICAL | [source](q014_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fe19100035463ff7 / python | HISTORICAL | [source](q014_tests_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d11eb05932202e32 / python | HISTORICAL | [source](q014_tests_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-87f78febb6dc49cc / python | HISTORICAL | [source](q014_tests_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a568fc2ec773cbcb / python | HISTORICAL | [source](q014_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7957baf1f4d0e2ff / python | HISTORICAL | [source](q014_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0bcc46e259ab4260 / python | HISTORICAL | [source](q014_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-385854c788cea84b / python | HISTORICAL | [source](q014_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dfaf10ef1789bcef / python | HISTORICAL | [source](q014_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-db487c247211489b / python | HISTORICAL | [source](q014_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-87c35822b7511512 / python | HISTORICAL | [source](q014_tests_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e24e7e4271d4a39d / python | HISTORICAL | [source](q014_tests_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bad8959f79957a78 / python | HISTORICAL | [source](q015_cmb_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0a033dc2f50312cc / python | HISTORICAL | [source](q015_cmb_attribution_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ab6857ee55b30f98 / python | HISTORICAL | [source](q015_cmb_attribution_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9b67dcfd3f908a5b / shell | HISTORICAL | [source](q015_setup_v1.sh) | bash q015_setup_v1.sh |
| ENTRY-dc5076054ffefde4 / shell | HISTORICAL | [source](q015_setup_v2.sh) | bash q015_setup_v2.sh |
| ENTRY-2a7d2c901c895e35 / shell | HISTORICAL | [source](q015_setup_v3.sh) | bash q015_setup_v3.sh |
| ENTRY-7f16b8a19ccf3ff1 / workflow | HISTORICAL | [source](q016-matched-cmb-surface-v14.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-94933064a56711e7 / workflow | HISTORICAL | [source](q016-matched-cmb-surface-v16.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-c0ace84691f6a855 / workflow | HISTORICAL | [source](q016-matched-cmb-surface-v8.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-da41d7a4d4b00a2b / shell | HISTORICAL | [source](q016_act_asset_v10.sh) | bash q016_act_asset_v10.sh |
| ENTRY-c09d1116fdd483e1 / shell | HISTORICAL | [source](q016_act_asset_v5.sh) | bash q016_act_asset_v5.sh |
| ENTRY-18d98989998b09ba / shell | HISTORICAL | [source](q016_act_asset_v6.sh) | bash q016_act_asset_v6.sh |
| ENTRY-0f8a438211290fcc / shell | HISTORICAL | [source](q016_act_asset_v7.sh) | bash q016_act_asset_v7.sh |
| ENTRY-11cbd705e95c0b87 / shell | HISTORICAL | [source](q016_act_asset_v8-1.sh) | bash q016_act_asset_v8-1.sh |
| ENTRY-05fe898bbfa39cd3 / shell | HISTORICAL | [source](q016_act_asset_v8.sh) | bash q016_act_asset_v8.sh |
| ENTRY-e78cf05f813b2a04 / shell | HISTORICAL | [source](q016_act_asset_v9.sh) | bash q016_act_asset_v9.sh |
| ENTRY-140097a075abfb10 / python | HISTORICAL | [source](q016_aggregate_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3b9593d840a36092 / python | HISTORICAL | [source](q016_aggregate_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-68fdea905260e9b6 / python | HISTORICAL | [source](q016_aggregate_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-59f3463e8548f0a7 / python | HISTORICAL | [source](q016_aggregate_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e7cd8960ec3573ff / python | HISTORICAL | [source](q016_aggregate_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f2c6982637a4e690 / python | HISTORICAL | [source](q016_aggregate_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c1afe20ffb97ddce / python | HISTORICAL | [source](q016_aggregate_v16-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7e8eb0e9b64b658d / python | HISTORICAL | [source](q016_aggregate_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-581555532d59e73a / python | HISTORICAL | [source](q016_aggregate_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-58dbe7b0035dbf48 / python | HISTORICAL | [source](q016_aggregate_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-734fc4836f5bdafc / python | HISTORICAL | [source](q016_aggregate_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-79e71fb06f77b579 / python | HISTORICAL | [source](q016_aggregate_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7681e306290532b4 / python | HISTORICAL | [source](q016_aggregate_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-46e335600bb7453d / python | HISTORICAL | [source](q016_aggregate_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2bcbf3be90c2d908 / python | HISTORICAL | [source](q016_aggregate_v8-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5ac4b549f14eae3a / python | HISTORICAL | [source](q016_aggregate_v8-2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-242a9a2762cdf126 / python | HISTORICAL | [source](q016_aggregate_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1e3c4f796824ebc5 / python | HISTORICAL | [source](q016_branch_runner_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6adeb12ffe88e9cb / python | HISTORICAL | [source](q016_branch_runner_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5a39b0b90ea7b3d8 / python | HISTORICAL | [source](q016_branch_runner_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-707fcff172448f60 / python | HISTORICAL | [source](q016_branch_runner_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9592b420fe61863f / python | HISTORICAL | [source](q016_branch_runner_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4ac863ae4bcd590f / python | HISTORICAL | [source](q016_branch_runner_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0d5e6b332679759b / python | HISTORICAL | [source](q016_mechanism_aggregate_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fcfaa32702180f2b / python | HISTORICAL | [source](q016_mechanism_aggregate_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3f6da9155aadf3b7 / python | HISTORICAL | [source](q016_mechanism_aggregate_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ba2f50e9a7c46b28 / python | HISTORICAL | [source](q016_mechanism_aggregate_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4de7e65886d36035 / shell | HISTORICAL | [source](q016_mechanism_setup_v1.sh) | bash q016_mechanism_setup_v1.sh |
| ENTRY-2e7c03998547d976 / shell | HISTORICAL | [source](q016_mechanism_setup_v2.sh) | bash q016_mechanism_setup_v2.sh |
| ENTRY-e87e05677cc10f8b / shell | HISTORICAL | [source](q016_mechanism_setup_v3.sh) | bash q016_mechanism_setup_v3.sh |
| ENTRY-1c2c6218e2b26c02 / shell | HISTORICAL | [source](q016_mechanism_setup_v4.sh) | bash q016_mechanism_setup_v4.sh |
| ENTRY-138271f6add86759 / python | HISTORICAL | [source](q016_mechanism_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3d0eff7adb590c69 / python | HISTORICAL | [source](q016_mechanism_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8e2990978d33a0e9 / python | HISTORICAL | [source](q016_mechanism_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f8fd2ec18153cab3 / python | HISTORICAL | [source](q016_mechanism_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8a7479770fb2572c / python | HISTORICAL | [source](q016_mechanism_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4bb1721d05e2cf13 / python | HISTORICAL | [source](q016_mechanism_v2-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8fd4aeacb297b0ab / python | HISTORICAL | [source](q016_mechanism_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e47c08c59cfa749c / python | HISTORICAL | [source](q016_mechanism_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1ed11faff6881fb4 / python | HISTORICAL | [source](q016_mechanism_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c85f20e10659e409 / python | HISTORICAL | [source](q016_objective_reprofile_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8d23bd8fd6dbb5e2 / python | HISTORICAL | [source](q016_objective_reprofile_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0430f54215325cc7 / python | HISTORICAL | [source](q016_objective_reprofile_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-71970a787ddf29ad / python | HISTORICAL | [source](q016_objective_reprofile_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ee41cba03c42141a / python | HISTORICAL | [source](q016_objective_reprofile_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a1dd18b90800f4df / python | HISTORICAL | [source](q016_objective_reprofile_v16-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9954ca729a96e298 / python | HISTORICAL | [source](q016_objective_reprofile_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-65978cf41963ce9d / python | HISTORICAL | [source](q016_objective_reprofile_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-98adcebe1fde0e77 / python | HISTORICAL | [source](q016_objective_reprofile_v8-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bf16d9c90afd3e97 / python | HISTORICAL | [source](q016_objective_reprofile_v8-2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bb585c753642eb99 / python | HISTORICAL | [source](q016_objective_reprofile_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-afbce96b0f14851a / python | HISTORICAL | [source](q016_primary_result_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b9efa5d8036afb22 / python | HISTORICAL | [source](q016_result_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-db702320fd514cde / python | HISTORICAL | [source](q016_result_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-26dc61ee58239a1a / python | HISTORICAL | [source](q016_result_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8d492c3d96b0603a / python | HISTORICAL | [source](q016_result_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1c038a73a7866586 / python | HISTORICAL | [source](q016_result_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0690754f141d3fec / python | HISTORICAL | [source](q016_result_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cc3211c792e0dbc2 / shell | HISTORICAL | [source](q016_setup_v10.sh) | bash q016_setup_v10.sh |
| ENTRY-8f03843b50eb1c01 / shell | HISTORICAL | [source](q016_setup_v11.sh) | bash q016_setup_v11.sh |
| ENTRY-d5011a35f5a89aa2 / shell | HISTORICAL | [source](q016_setup_v12.sh) | bash q016_setup_v12.sh |
| ENTRY-7379f6b76af43e8f / shell | HISTORICAL | [source](q016_setup_v14.sh) | bash q016_setup_v14.sh |
| ENTRY-c6299838fed119fe / shell | HISTORICAL | [source](q016_setup_v15.sh) | bash q016_setup_v15.sh |
| ENTRY-7272c9f791e1ce55 / shell | HISTORICAL | [source](q016_setup_v16-1.sh) | bash q016_setup_v16-1.sh |
| ENTRY-b943c4f83fd2933d / shell | HISTORICAL | [source](q016_setup_v16.sh) | bash q016_setup_v16.sh |
| ENTRY-c3e2fef185414043 / shell | HISTORICAL | [source](q016_setup_v3.sh) | bash q016_setup_v3.sh |
| ENTRY-ba970d4f3dc7b3bc / shell | HISTORICAL | [source](q016_setup_v4.sh) | bash q016_setup_v4.sh |
| ENTRY-8d95c4a49adbc9f0 / shell | HISTORICAL | [source](q016_setup_v5.sh) | bash q016_setup_v5.sh |
| ENTRY-5c8ce003e0d2351e / shell | HISTORICAL | [source](q016_setup_v6.sh) | bash q016_setup_v6.sh |
| ENTRY-1798940c77e6ef86 / shell | HISTORICAL | [source](q016_setup_v7.sh) | bash q016_setup_v7.sh |
| ENTRY-ff4644e8f1c009c8 / shell | HISTORICAL | [source](q016_setup_v8-1.sh) | bash q016_setup_v8-1.sh |
| ENTRY-f809eacca4028350 / shell | HISTORICAL | [source](q016_setup_v8-2.sh) | bash q016_setup_v8-2.sh |
| ENTRY-167dbd953c3c392d / shell | HISTORICAL | [source](q016_setup_v8.sh) | bash q016_setup_v8.sh |
| ENTRY-9053a4bc654a2eb9 / shell | HISTORICAL | [source](q016_setup_v9.sh) | bash q016_setup_v9.sh |
| ENTRY-b4fa0bb1bbe7082e / python | HISTORICAL | [source](q016_tests_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dd182237facd502c / python | HISTORICAL | [source](q016_tests_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b92bbc9450bde494 / python | HISTORICAL | [source](q016_tests_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-45bd383c7a4d9ca5 / python | HISTORICAL | [source](q016_tests_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cfeaf64cb10b1f7b / python | HISTORICAL | [source](q016_tests_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-515c274599a7edf5 / python | HISTORICAL | [source](q016_tests_v16-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a14269090c0583c8 / python | HISTORICAL | [source](q016_tests_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e4729b4194943a03 / python | HISTORICAL | [source](q016_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a3d8e625c784fa12 / python | HISTORICAL | [source](q016_tests_v8-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7731cd53934c4e34 / python | HISTORICAL | [source](q016_tests_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-914c5e7bf96e85a1 / python | HISTORICAL | [source](q017_planck_direction_localization_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e43bc4e8cf5b7b4b / python | HISTORICAL | [source](q017_planck_direction_localization_v2.py) | python q017_planck_direction_localization_v2.py |
| ENTRY-4ed20fb1534497de / python | HISTORICAL | [source](q017_planck_direction_localization_v3.py) | python q017_planck_direction_localization_v3.py |
| ENTRY-66e41f01e2e9726c / shell | HISTORICAL | [source](q017_setup_v1.sh) | bash q017_setup_v1.sh |
| ENTRY-4bdc24892f480f13 / shell | HISTORICAL | [source](q017_setup_v2.sh) | bash q017_setup_v2.sh |
| ENTRY-f4bf64ce6ff7379b / shell | HISTORICAL | [source](q017_setup_v3.sh) | bash q017_setup_v3.sh |
| ENTRY-32eb32f771741b61 / python | HISTORICAL | [source](q017_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-40c3edf313d80383 / python | HISTORICAL | [source](q017_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6cba7e87a6bfa3f8 / python | HISTORICAL | [source](q017_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ea66225b3a7aca3b / python | HISTORICAL | [source](q018_planck_likelihood_bridge_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4dfde697c901b75f / python | HISTORICAL | [source](q018_planck_likelihood_bridge_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2b8537efc5f91026 / python | HISTORICAL | [source](q018_planck_likelihood_bridge_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d57f53f28e490831 / shell | HISTORICAL | [source](q018_setup_v1.sh) | bash q018_setup_v1.sh |
| ENTRY-fe4d45ee98c83976 / shell | HISTORICAL | [source](q018_setup_v2.sh) | bash q018_setup_v2.sh |
| ENTRY-e18037be203f493b / shell | HISTORICAL | [source](q018_setup_v3.sh) | bash q018_setup_v3.sh |
| ENTRY-3164d84f04126f1c / python | HISTORICAL | [source](q018_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f2c0cf336a8360b3 / python | HISTORICAL | [source](q018_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-065e7c6f0c9b5bde / python | HISTORICAL | [source](q018_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c025bfd09d8af9e2 / python | HISTORICAL | [source](q019_globality_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5c51a4593f19d69a / python | HISTORICAL | [source](q019_globality_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9f011f01a6620e12 / python | HISTORICAL | [source](q019_planck_cosmology_reprofile_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9f42e76bbf1658d0 / shell | HISTORICAL | [source](q019_setup_v1.sh) | bash q019_setup_v1.sh |
| ENTRY-7753ea25e880e5e3 / shell | HISTORICAL | [source](q019_setup_v2.sh) | bash q019_setup_v2.sh |
| ENTRY-70769d600823c850 / shell | HISTORICAL | [source](q019_setup_v3.sh) | bash q019_setup_v3.sh |
| ENTRY-370b0c1390cba8fa / python | HISTORICAL | [source](q019_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8e1cbfb7fcf437b6 / python | HISTORICAL | [source](q019_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1bfe3ccaf6e233ab / python | HISTORICAL | [source](q019_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-46ae71f9bf78056c / python | HISTORICAL | [source](q020_direction_localization_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2ce29ab66b40fc18 / python | HISTORICAL | [source](q020_finalize_repair_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-25ba9e8e9d6dce14 / python | HISTORICAL | [source](q020_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6b44f59f28639a18 / python | HISTORICAL | [source](q020_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-099ca15833647ded / python | HISTORICAL | [source](q021_finalize_repair_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-40d7b838833f6f06 / python | HISTORICAL | [source](q021_primordial_decomposition_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-348c7ed0a8db94e1 / python | HISTORICAL | [source](q021_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-215dc661045a190b / python | HISTORICAL | [source](q021_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bbb2b2ae21ecd68a / python | HISTORICAL | [source](q022_basin_diagnostic_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-755de611164cc435 / python | HISTORICAL | [source](q022_globality_continuation_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4e0738614451a651 / python | HISTORICAL | [source](q022_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b9457f0dfac500b5 / python | HISTORICAL | [source](q022_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-36f5f815e3e27904 / python | HISTORICAL | [source](q023_basin_directions_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a1278aa41c027fd2 / python | HISTORICAL | [source](q023_basin_directions_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7675d0a4ed29e6ea / python | HISTORICAL | [source](q023_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ccf5a23e1a3c78f3 / python | HISTORICAL | [source](q023_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1bbabc3844a26f16 / python | HISTORICAL | [source](q024_basin_matching_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-10726ccbd6c8c922 / python | HISTORICAL | [source](q024_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-46fd05dd46aefb81 / python | HISTORICAL | [source](q025_fullmf_component_attribution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f4ae5a4c29e67de5 / python | HISTORICAL | [source](q025_fullmf_component_attribution_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-878654b2d74e0775 / python | HISTORICAL | [source](q025_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-33e37bfac1002d72 / python | HISTORICAL | [source](q025_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-90328be957615b0a / python | HISTORICAL | [source](q026_mask6_nuisance_localization_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-eb94d601ef597908 / python | HISTORICAL | [source](q026_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6e229f7482d2a7c5 / python | HISTORICAL | [source](q027_residual_covariance_bridge_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-96065bd94c1009c2 / python | HISTORICAL | [source](q027_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1f71276c5ee8db55 / workflow | HISTORICAL | [source](q028-common-support-counterfactual-v6.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-f25e1374edcaf229 / python | HISTORICAL | [source](q028_common_support_counterfactual_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ec69a7f2ce434dd4 / python | HISTORICAL | [source](q028_common_support_counterfactual_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-35c47fed52ba5b99 / python | HISTORICAL | [source](q028_common_support_counterfactual_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-24d85e9dfe4f99e5 / python | HISTORICAL | [source](q028_common_support_counterfactual_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fd20055b0a1f401d / python | HISTORICAL | [source](q028_common_support_counterfactual_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e52647080bfad0df / python | HISTORICAL | [source](q028_common_support_counterfactual_v6-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-915c3dabf575e09a / python | HISTORICAL | [source](q028_common_support_counterfactual_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-41b4b7f944d35a4c / python | HISTORICAL | [source](q028_common_support_counterfactual_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5288b075b61b86e5 / python | HISTORICAL | [source](q028_common_support_counterfactual_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-139e6e440a63be8b / python | HISTORICAL | [source](q028_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e7cca3741781ae67 / python | HISTORICAL | [source](q028_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-26fc4593b123c1e2 / python | HISTORICAL | [source](q028_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-10094c8159f2d1c4 / python | HISTORICAL | [source](q028_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0c4f42d079b9a312 / python | HISTORICAL | [source](q028_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e8dea588905b902c / python | HISTORICAL | [source](q028_tests_v6-2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f1e396e224bc237a / python | HISTORICAL | [source](q028_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3e105e06449b2c5b / python | HISTORICAL | [source](q028_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cfb4f8bc1418085c / python | HISTORICAL | [source](q028_tests_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-be5651e28e36fc90 / python | HISTORICAL | [source](q030_interaction_preserving_decomposition_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6116cb5be3b2fd7c / python | HISTORICAL | [source](q030_interaction_preserving_decomposition_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-34e3cc686b2cdb7d / python | HISTORICAL | [source](q030_original_gate_precision_audit_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-00bd81c4862ede2d / python | HISTORICAL | [source](q030_original_gate_precision_audit_tests_v1r1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2f9417cd65a9be95 / python | HISTORICAL | [source](q030_original_gate_precision_audit_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cebe4ea91eb5a572 / python | HISTORICAL | [source](q030_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-45e2a6b7b934271c / python | HISTORICAL | [source](q030_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-156812f9b26fff25 / python | HISTORICAL | [source](q030_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f42699985c6319c1 / python | HISTORICAL | [source](q030_validation_repair_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2713044032417c7c / python | HISTORICAL | [source](q031_planck_portability_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f99cc12323afa573 / shell | HISTORICAL | [source](q031_setup_v1.sh) | bash q031_setup_v1.sh |
| ENTRY-4bbb0b8428210787 / shell | HISTORICAL | [source](q031_setup_v2.sh) | bash q031_setup_v2.sh |
| ENTRY-5bb8d3ffbcd52d2d / shell | HISTORICAL | [source](q031_setup_v3.sh) | bash q031_setup_v3.sh |
| ENTRY-35462d7185354d41 / shell | HISTORICAL | [source](q031_setup_v4.sh) | bash q031_setup_v4.sh |
| ENTRY-debd8991d7924f8b / python | HISTORICAL | [source](q031_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-29d44a4e5d0e3723 / python | HISTORICAL | [source](q032_addback_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d34461228d08a609 / python | HISTORICAL | [source](q032_camspec_addback_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bba33848a1eda3eb / python | HISTORICAL | [source](q032_exact_start_addback_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e922d3bfa603371a / python | HISTORICAL | [source](q032_exact_start_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ee158d1ac9523865 / python | HISTORICAL | [source](q032_planck_tt3pair_bridge_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-207969c3582dadd0 / python | HISTORICAL | [source](q032_planck_tt3pair_bridge_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-72166de98060b1cd / shell | HISTORICAL | [source](q032_setup_v1.sh) | bash q032_setup_v1.sh |
| ENTRY-9b98375c194c4179 / shell | HISTORICAL | [source](q032_setup_v2.sh) | bash q032_setup_v2.sh |
| ENTRY-d15d29767620f563 / shell | HISTORICAL | [source](q032_setup_v3.sh) | bash q032_setup_v3.sh |
| ENTRY-874a847c899edc18 / shell | HISTORICAL | [source](q032_setup_v4.sh) | bash q032_setup_v4.sh |
| ENTRY-39a4809f8bcb2f8d / python | HISTORICAL | [source](q032_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-23c10f800aa86cd9 / python | HISTORICAL | [source](q032_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c8fca8440d2b1a52 / python | HISTORICAL | [source](q033_launch_semantics_ab_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8291265bc5318180 / python | HISTORICAL | [source](q033_launch_semantics_protocol_audit_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b67c19ecc5b99948 / python | HISTORICAL | [source](q033_launch_semantics_tests_v1.py) | python q033_launch_semantics_tests_v1.py |
| ENTRY-9956d182513d173b / python | HISTORICAL | [source](q033_launch_semantics_tests_v2.py) | python q033_launch_semantics_tests_v2.py |
| ENTRY-226593f87c3b7b74 / python | HISTORICAL | [source](q034_primordial_freeze_isolation_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-520e0ad99179c2dc / python | HISTORICAL | [source](q034_primordial_freeze_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2ba35d32775f8705 / python | HISTORICAL | [source](q035_classifier_harmonization_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-87a4c9b923d07ea8 / python | HISTORICAL | [source](q035_classifier_harmonization_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dfd1e52996155dd9 / workflow | HISTORICAL | [source](q036-endpoint-geometry-portability-v3.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-ebf1b686178e9ea9 / python | HISTORICAL | [source](q036_endpoint_geometry_portability_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5e9bf63bd118f3e7 / python | HISTORICAL | [source](q036_endpoint_geometry_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4fa8d1905c016688 / python | HISTORICAL | [source](q037_common_support_endpoint_geometry_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8fbcb379ad326fe3 / python | HISTORICAL | [source](q037_common_support_endpoint_geometry_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5c754cd92c8bee5c / python | HISTORICAL | [source](q038_coordinate_localization_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5a468dc7f56d20fc / python | HISTORICAL | [source](q038_coordinate_localization_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4b5e424ced0bda61 / workflow | HISTORICAL | [source](q039-implementation-block-intervention-v4.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-f7b1a6eb9298f31d / python | HISTORICAL | [source](q039_implementation_block_intervention_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ba0630481c557e56 / python | HISTORICAL | [source](q039_implementation_block_intervention_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f8a47d8058045cec / python | HISTORICAL | [source](q039_implementation_block_intervention_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d9441f1bf112e6bf / python | HISTORICAL | [source](q039_implementation_block_intervention_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-29707f22b043d25a / python | HISTORICAL | [source](q039_implementation_block_intervention_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8796cf74af1a2888 / python | HISTORICAL | [source](q039_native_foreground_profile_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ac18b438dcbb55e0 / python | HISTORICAL | [source](q039_native_foreground_profile_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-390116944c135c5d / shell | HISTORICAL | [source](q039_prepare_frozen_env_v3.sh) | bash q039_prepare_frozen_env_v3.sh |
| ENTRY-be19e1e4d45e3ba2 / shell | HISTORICAL | [source](q039_prepare_frozen_env_v4.sh) | bash q039_prepare_frozen_env_v4.sh |
| ENTRY-5cba8e2975261313 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-93a1ce67c37564c7 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8103c67db9a0c0e8 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4de9376826d8fd55 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6b7fea6ea8f31373 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d7470b19a1139eaf / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a9c289dbe4f34163 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7e3cbae93cc5b560 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_v3.py) | python q040_cmbspace_coupled_bridge_v3.py |
| ENTRY-f681882903c51786 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_v4.py) | python q040_cmbspace_coupled_bridge_v4.py |
| ENTRY-f77e2aed1b1089d5 / python | HISTORICAL | [source](q040_cmbspace_coupled_bridge_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ad8c06609c85968c / python | HISTORICAL | [source](q040_defensive_rqmc_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7c0e6c23d615c72a / python | HISTORICAL | [source](q040_defensive_rqmc_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0aa7fe0bf4addef1 / python | HISTORICAL | [source](q040_defensive_rqmc_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-338702bf73b6b55e / python | HISTORICAL | [source](q040_defensive_rqmc_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8125533dcdd8059d / python | HISTORICAL | [source](q040_defensive_rqmc_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-17f68281faa89651 / python | HISTORICAL | [source](q040_defensive_rqmc_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a7ec85712cd1cc11 / python | HISTORICAL | [source](q040_defensive_rqmc_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-877358129cba6c4b / python | HISTORICAL | [source](q040_defensive_rqmc_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-07df6a2b9b5ecfac / python | HISTORICAL | [source](q041_planck_portability_tests_v1-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-15236c34ba021b88 / python | HISTORICAL | [source](q041_planck_portability_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b72b7e47a4cb0d3f / python | HISTORICAL | [source](q041_planck_portability_tests_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e19302cf9083e8e7 / python | HISTORICAL | [source](q041_planck_portability_tests_v11-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cf4853da8dba563e / python | HISTORICAL | [source](q041_planck_portability_tests_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ada4cb07b0e39ca2 / python | HISTORICAL | [source](q041_planck_portability_tests_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ccadeef3ee1d060e / python | HISTORICAL | [source](q041_planck_portability_tests_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b89da964564f7b9c / python | HISTORICAL | [source](q041_planck_portability_tests_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7960dba76033867e / python | HISTORICAL | [source](q041_planck_portability_tests_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ea4277cd026f5a2e / python | HISTORICAL | [source](q041_planck_portability_tests_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c78ce72add3d4883 / python | HISTORICAL | [source](q041_planck_portability_tests_v17.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cdd7f6881049a1ea / python | HISTORICAL | [source](q041_planck_portability_tests_v18.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1c02bf9adee6268a / python | HISTORICAL | [source](q041_planck_portability_tests_v19.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0ca91310699d4de3 / python | HISTORICAL | [source](q041_planck_portability_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-71fa461970ed9f4e / python | HISTORICAL | [source](q041_planck_portability_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4deb7c4e8c1903da / python | HISTORICAL | [source](q041_planck_portability_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c4bc9b7dceab933a / python | HISTORICAL | [source](q041_planck_portability_tests_v5-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5d5b21e3993c0dbd / python | HISTORICAL | [source](q041_planck_portability_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-96b97eb11df63812 / python | HISTORICAL | [source](q041_planck_portability_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a74524c1eb23e197 / python | HISTORICAL | [source](q041_planck_portability_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-92e910818027173d / python | HISTORICAL | [source](q041_planck_portability_tests_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-131c0a64aa673352 / python | HISTORICAL | [source](q041_planck_portability_tests_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b6a0f3e9c899f96f / python | HISTORICAL | [source](q041_planck_portability_v1-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cd86f223f06dde4a / python | HISTORICAL | [source](q041_planck_portability_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2e655acb93fe2a72 / python | HISTORICAL | [source](q041_planck_portability_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-442a18c416294cc4 / python | HISTORICAL | [source](q041_planck_portability_v11-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ac10e670ce76b576 / python | HISTORICAL | [source](q041_planck_portability_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2d73a6a4d87c11a2 / python | HISTORICAL | [source](q041_planck_portability_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b4e4cc7393a30396 / python | HISTORICAL | [source](q041_planck_portability_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1527205bddba9aed / python | HISTORICAL | [source](q041_planck_portability_v14.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-02a9e25b95e41fbd / python | HISTORICAL | [source](q041_planck_portability_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-16e1b060f7441d96 / python | HISTORICAL | [source](q041_planck_portability_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5efabd8662961b9b / python | HISTORICAL | [source](q041_planck_portability_v17.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fedecbddf6baf0c0 / python | HISTORICAL | [source](q041_planck_portability_v18.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f2af060e1f09002d / python | HISTORICAL | [source](q041_planck_portability_v19.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e86429ab10a25527 / python | HISTORICAL | [source](q041_planck_portability_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b1caff88bd3a8ab4 / python | HISTORICAL | [source](q041_planck_portability_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-72c41e61dfd9d913 / python | HISTORICAL | [source](q041_planck_portability_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-296296b05877e92b / python | HISTORICAL | [source](q041_planck_portability_v5-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ed0570e4ca46959a / python | HISTORICAL | [source](q041_planck_portability_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0a36caf0367ae523 / python | HISTORICAL | [source](q041_planck_portability_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c27ff56dd71d733f / python | HISTORICAL | [source](q041_planck_portability_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e5833f68f3becb74 / python | HISTORICAL | [source](q041_planck_portability_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-63853c16f40a6647 / python | HISTORICAL | [source](q041_planck_portability_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-feff18d70617f7a5 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v10.sh) | bash q041_prepare_frozen_core_v10.sh |
| ENTRY-fe5a2be3c7f0ed35 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v11-1.sh) | bash q041_prepare_frozen_core_v11-1.sh |
| ENTRY-870f2b04c1f2e647 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v11.sh) | bash q041_prepare_frozen_core_v11.sh |
| ENTRY-7cf6613a39725ea8 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v12.sh) | bash q041_prepare_frozen_core_v12.sh |
| ENTRY-1835def86fb41b54 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v13.sh) | bash q041_prepare_frozen_core_v13.sh |
| ENTRY-a2b9e428098ce58b / shell | HISTORICAL | [source](q041_prepare_frozen_core_v14.sh) | bash q041_prepare_frozen_core_v14.sh |
| ENTRY-8a608c27918e3e67 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v15-1.sh) | bash q041_prepare_frozen_core_v15-1.sh |
| ENTRY-5df1fc467206bc0b / shell | HISTORICAL | [source](q041_prepare_frozen_core_v15.sh) | bash q041_prepare_frozen_core_v15.sh |
| ENTRY-9a6718560db98c4b / shell | HISTORICAL | [source](q041_prepare_frozen_core_v16.sh) | bash q041_prepare_frozen_core_v16.sh |
| ENTRY-e078e90cbf2e4eba / shell | HISTORICAL | [source](q041_prepare_frozen_core_v17.sh) | bash q041_prepare_frozen_core_v17.sh |
| ENTRY-6acbdf8f34de1c58 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v18.sh) | bash q041_prepare_frozen_core_v18.sh |
| ENTRY-2f587856c19be354 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v19.sh) | bash q041_prepare_frozen_core_v19.sh |
| ENTRY-ff2063297366a041 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v3.sh) | bash q041_prepare_frozen_core_v3.sh |
| ENTRY-6251580087f42be4 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v4.sh) | bash q041_prepare_frozen_core_v4.sh |
| ENTRY-1cbe70bc15faba58 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v5-1.sh) | bash q041_prepare_frozen_core_v5-1.sh |
| ENTRY-2d5f8710de53eafb / shell | HISTORICAL | [source](q041_prepare_frozen_core_v5.sh) | bash q041_prepare_frozen_core_v5.sh |
| ENTRY-e744f7d90926def5 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v6.sh) | bash q041_prepare_frozen_core_v6.sh |
| ENTRY-13a631b90f84645c / shell | HISTORICAL | [source](q041_prepare_frozen_core_v7-1.sh) | bash q041_prepare_frozen_core_v7-1.sh |
| ENTRY-7e361074c89659e5 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v7.sh) | bash q041_prepare_frozen_core_v7.sh |
| ENTRY-e529b21c542165ed / shell | HISTORICAL | [source](q041_prepare_frozen_core_v8.sh) | bash q041_prepare_frozen_core_v8.sh |
| ENTRY-7051558ea7f89e03 / shell | HISTORICAL | [source](q041_prepare_frozen_core_v9.sh) | bash q041_prepare_frozen_core_v9.sh |
| ENTRY-ea902e8cbf773d9c / shell | HISTORICAL | [source](q041_setup_v1-1.sh) | bash q041_setup_v1-1.sh |
| ENTRY-a0e948229e872299 / shell | HISTORICAL | [source](q041_setup_v1.sh) | bash q041_setup_v1.sh |
| ENTRY-e01cc25fc870bd77 / shell | HISTORICAL | [source](q041_setup_v10.sh) | bash q041_setup_v10.sh |
| ENTRY-4350f86a9d88a052 / shell | HISTORICAL | [source](q041_setup_v11-1.sh) | bash q041_setup_v11-1.sh |
| ENTRY-aed50fe4ac7a7d8c / shell | HISTORICAL | [source](q041_setup_v11.sh) | bash q041_setup_v11.sh |
| ENTRY-f19230657a787476 / shell | HISTORICAL | [source](q041_setup_v12.sh) | bash q041_setup_v12.sh |
| ENTRY-25157223e305007f / shell | HISTORICAL | [source](q041_setup_v13.sh) | bash q041_setup_v13.sh |
| ENTRY-f5e2e5dc694feeeb / shell | HISTORICAL | [source](q041_setup_v14.sh) | bash q041_setup_v14.sh |
| ENTRY-279d402269fe3f52 / shell | HISTORICAL | [source](q041_setup_v15.sh) | bash q041_setup_v15.sh |
| ENTRY-7fbfb6d317b7ddb8 / shell | HISTORICAL | [source](q041_setup_v16.sh) | bash q041_setup_v16.sh |
| ENTRY-165bed67e7654b63 / shell | HISTORICAL | [source](q041_setup_v17.sh) | bash q041_setup_v17.sh |
| ENTRY-7549ff815aa85680 / shell | HISTORICAL | [source](q041_setup_v18.sh) | bash q041_setup_v18.sh |
| ENTRY-5e727032c14adbdc / shell | HISTORICAL | [source](q041_setup_v19.sh) | bash q041_setup_v19.sh |
| ENTRY-6ebcc8d6f7e92774 / shell | HISTORICAL | [source](q041_setup_v2.sh) | bash q041_setup_v2.sh |
| ENTRY-989c6ee7e892cee7 / shell | HISTORICAL | [source](q041_setup_v3.sh) | bash q041_setup_v3.sh |
| ENTRY-9ac94f78c6d7c334 / shell | HISTORICAL | [source](q041_setup_v4.sh) | bash q041_setup_v4.sh |
| ENTRY-88c0e97702ac1599 / shell | HISTORICAL | [source](q041_setup_v5-1.sh) | bash q041_setup_v5-1.sh |
| ENTRY-d93ef1f2f5cf469c / shell | HISTORICAL | [source](q041_setup_v5.sh) | bash q041_setup_v5.sh |
| ENTRY-7a12435d6f2c44e5 / shell | HISTORICAL | [source](q041_setup_v6.sh) | bash q041_setup_v6.sh |
| ENTRY-5a85f6310660ec91 / shell | HISTORICAL | [source](q041_setup_v7-1.sh) | bash q041_setup_v7-1.sh |
| ENTRY-066f4c5a7867395b / shell | HISTORICAL | [source](q041_setup_v7.sh) | bash q041_setup_v7.sh |
| ENTRY-54b31d7e9313400e / shell | HISTORICAL | [source](q041_setup_v8.sh) | bash q041_setup_v8.sh |
| ENTRY-a49b44d3d7b4796c / shell | HISTORICAL | [source](q041_setup_v9.sh) | bash q041_setup_v9.sh |
| ENTRY-7030db9b04d4e049 / workflow | HISTORICAL | [source](q042-planck-portability-v11.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-5d00c8e2d469aa55 / workflow | HISTORICAL | [source](<q042-production-v9 (1).yml>) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-04e3e4089fc814c9 / workflow | HISTORICAL | [source](q042-production-v9.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-bc0016aacccdb14b / python | HISTORICAL | [source](q042_apply_readme_patch_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6058a746ba4fd680 / python | HISTORICAL | [source](q042_apply_readme_patch_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0c44ecafbb807629 / python | HISTORICAL | [source](q042_apply_readme_patch_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-50cdbc8a7b84e20c / python | HISTORICAL | [source](q042_apply_readme_patch_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-14da92e89cd0e72c / python | HISTORICAL | [source](q042_apply_readme_patch_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6224a045758465eb / python | HISTORICAL | [source](q042_apply_readme_patch_v17.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a8d8825054f9b895 / python | HISTORICAL | [source](q042_apply_readme_patch_v18.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1fa8faee511d855f / python | HISTORICAL | [source](q042_apply_readme_patch_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-05a3ed0fdb1bac28 / python | HISTORICAL | [source](q042_apply_readme_patch_v4-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fc49bdf5a0390cc5 / python | HISTORICAL | [source](q042_apply_readme_patch_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e54c4d1471e0cd79 / python | HISTORICAL | [source](q042_apply_readme_patch_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6ef303b8107e9a87 / python | HISTORICAL | [source](q042_apply_readme_patch_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a095ad1215fc8a88 / python | HISTORICAL | [source](<q042_apply_readme_patch_v7 (1).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c0d44c2fe4fb89ed / python | HISTORICAL | [source](<q042_apply_readme_patch_v7 (2).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4c00c359404ca1bd / python | HISTORICAL | [source](q042_apply_readme_patch_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-93413fc96f08ceef / python | HISTORICAL | [source](q042_apply_readme_patch_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-bc2054a8ab670b72 / python | HISTORICAL | [source](q042_apply_readme_patch_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7e20ae0461197fd3 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v1.py) | python q042_apply_registry_patch_prod_v1.py |
| ENTRY-e3ff193008f1f900 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v11.py) | python q042_apply_registry_patch_prod_v11.py |
| ENTRY-b18dd4bd757c8385 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v12.py) | python q042_apply_registry_patch_prod_v12.py |
| ENTRY-39f16cc57b8835ef / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v13.py) | python q042_apply_registry_patch_prod_v13.py |
| ENTRY-afbfe3b178ca003b / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v15.py) | python q042_apply_registry_patch_prod_v15.py |
| ENTRY-d469dda9e8286df0 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v16.py) | python q042_apply_registry_patch_prod_v16.py |
| ENTRY-17cb544933dea31d / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v17.py) | python q042_apply_registry_patch_prod_v17.py |
| ENTRY-33b7c01905688ce3 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v18.py) | python q042_apply_registry_patch_prod_v18.py |
| ENTRY-d093ec73de94af67 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v19.py) | python q042_apply_registry_patch_prod_v19.py |
| ENTRY-6c92518c9e3caaf2 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v2.py) | python q042_apply_registry_patch_prod_v2.py |
| ENTRY-89a99442d9fa46ed / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v3.py) | python q042_apply_registry_patch_prod_v3.py |
| ENTRY-943e67f4554049fb / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v4-1.py) | python q042_apply_registry_patch_prod_v4-1.py |
| ENTRY-44827572f2f056a5 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v4.py) | python q042_apply_registry_patch_prod_v4.py |
| ENTRY-fd1e0330cc19f299 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v5.py) | python q042_apply_registry_patch_prod_v5.py |
| ENTRY-125a10d8a15a104f / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v6.py) | python q042_apply_registry_patch_prod_v6.py |
| ENTRY-e075ab9e5b136a10 / python | HISTORICAL | [source](<q042_apply_registry_patch_prod_v7 (1).py>) | python 'q042_apply_registry_patch_prod_v7 (1).py' |
| ENTRY-78f45531924fba02 / python | HISTORICAL | [source](<q042_apply_registry_patch_prod_v7 (2).py>) | python 'q042_apply_registry_patch_prod_v7 (2).py' |
| ENTRY-f5473f1e8f472c23 / python | HISTORICAL | [source](<q042_apply_registry_patch_prod_v7 (3).py>) | python 'q042_apply_registry_patch_prod_v7 (3).py' |
| ENTRY-1fbaa68076be1bd0 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v7.py) | python q042_apply_registry_patch_prod_v7.py |
| ENTRY-0bad4ca0fb976af0 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v8.py) | python q042_apply_registry_patch_prod_v8.py |
| ENTRY-326d0d3bea961648 / python | HISTORICAL | [source](q042_apply_registry_patch_prod_v9.py) | python q042_apply_registry_patch_prod_v9.py |
| ENTRY-4d3a47ddbf875423 / python | HISTORICAL | [source](q042_apply_registry_patch_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7ef6c6c676d0b3c3 / python | HISTORICAL | [source](q042_apply_registry_patch_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cb40a33faf09fa5d / python | HISTORICAL | [source](q042_apply_registry_patch_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cbb94a4dd716d0e5 / python | HISTORICAL | [source](q042_apply_registry_patch_v2-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2a0aa30a3d896d45 / python | HISTORICAL | [source](q042_apply_registry_patch_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c6a1cdf2867d8bc2 / python | HISTORICAL | [source](q042_apply_registry_patch_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5d0b7854be9311bc / python | HISTORICAL | [source](q042_apply_registry_patch_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-449376bf761764ef / python | HISTORICAL | [source](q042_apply_registry_patch_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1bd82b2fcc38955d / python | HISTORICAL | [source](q042_apply_registry_patch_v6-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f7256280552105d3 / python | HISTORICAL | [source](q042_apply_registry_patch_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a77a699aa8b39c14 / python | HISTORICAL | [source](q042_apply_registry_patch_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-14df3110a1e0db4c / python | HISTORICAL | [source](q042_apply_registry_patch_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4844dee3fa286710 / python | HISTORICAL | [source](q042_class_diagnostic_v23.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-074b3cec2935b74f / python | HISTORICAL | [source](q042_class_nan_native_selftest_v25.py) | python q042_class_nan_native_selftest_v25.py |
| ENTRY-5799559f218aafb2 / python | HISTORICAL | [source](q042_class_nan_tests_v25.py) | python q042_class_nan_tests_v25.py |
| ENTRY-8172c358ab61ee67 / python | HISTORICAL | [source](q042_class_nan_v25.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fa30c1bf92fd9c99 / python | HISTORICAL | [source](q042_class_origin_tests_v24.py) | python q042_class_origin_tests_v24.py |
| ENTRY-a9e7cb7df08a3023 / python | HISTORICAL | [source](q042_class_origin_v24.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3569bbc78a756114 / python | HISTORICAL | [source](q042_class_tests_v23.py) | python q042_class_tests_v23.py |
| ENTRY-cf9c23ba8d5ff840 / python | HISTORICAL | [source](q042_cobaya_partial_resume_adapter_v18.py) | python q042_cobaya_partial_resume_adapter_v18.py |
| ENTRY-d007a4e0267b46e5 / python | HISTORICAL | [source](q042_context_v29.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-671b818109decc6a / python | HISTORICAL | [source](q042_durable_diagnostic_v22.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7fb147682a2a0d7c / python | HISTORICAL | [source](q042_durable_selftest_v22.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e0259d9ded04cf82 / python | HISTORICAL | [source](q042_durable_tests_v22.py) | python q042_durable_tests_v22.py |
| ENTRY-95e749f0abee5d52 / python | HISTORICAL | [source](q042_event_adapter_selftest_v28.py) | python q042_event_adapter_selftest_v28.py |
| ENTRY-7c5d62b823ed3a2c / python | HISTORICAL | [source](q042_event_cell_v28.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3914313d7c9f6613 / python | HISTORICAL | [source](q042_event_tests_v28.py) | python q042_event_tests_v28.py |
| ENTRY-9f7109c46e20a0cc / python | HISTORICAL | [source](q042_execution_mechanism_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e46faa6170a8c52f / python | HISTORICAL | [source](q042_execution_mechanism_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a5d5854706b3d01d / python | HISTORICAL | [source](q042_install_durable_v22.py) | python q042_install_durable_v22.py |
| ENTRY-0aa1c9152d58841f / python | HISTORICAL | [source](q042_install_stock_diagnostic_v20.py) | python q042_install_stock_diagnostic_v20.py |
| ENTRY-98f388c54fbd1bd5 / python | HISTORICAL | [source](q042_install_stock_diagnostic_v21.py) | python q042_install_stock_diagnostic_v21.py |
| ENTRY-d7a332a9e8cfb1b3 / python | HISTORICAL | [source](q042_interval_tests_v29.py) | python q042_interval_tests_v29.py |
| ENTRY-303227e74cc4fa71 / python | HISTORICAL | [source](q042_interval_v29.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b0eabbc652bc16ec / python | HISTORICAL | [source](q042_patch_durable_v22.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ef5f33868b7ca8a7 / python | HISTORICAL | [source](q042_patch_polychord_partial_init_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5f19be70980242b8 / python | HISTORICAL | [source](q042_patch_polychord_partial_init_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4d4cf372d8b94682 / python | HISTORICAL | [source](q042_patch_polychord_partial_init_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4d31fd422d35a449 / python | HISTORICAL | [source](q042_planck_portability_tests_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-90319fffd19ea567 / python | HISTORICAL | [source](q042_planck_portability_tests_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c37bee1cafb5d4f5 / python | HISTORICAL | [source](q042_planck_portability_tests_v2-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-87616cc0b63f0f41 / python | HISTORICAL | [source](q042_planck_portability_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d217b414bfebee42 / python | HISTORICAL | [source](q042_planck_portability_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f21b140fbe0a4ef3 / python | HISTORICAL | [source](q042_planck_portability_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0a54ed44169a2844 / python | HISTORICAL | [source](q042_planck_portability_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6358e815c35cb992 / python | HISTORICAL | [source](q042_planck_portability_tests_v6-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-06cf3dbf19bd678b / python | HISTORICAL | [source](q042_planck_portability_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dd8d158fd4586634 / python | HISTORICAL | [source](q042_planck_portability_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-254b6551b08bbf1c / python | HISTORICAL | [source](q042_planck_portability_tests_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9979061ef0e5a71c / python | HISTORICAL | [source](q042_planck_portability_v10.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2c694193f2cb1253 / python | HISTORICAL | [source](q042_planck_portability_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0ce6cd20b8a06bb8 / python | HISTORICAL | [source](q042_planck_portability_v2-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b82d9234d9643114 / python | HISTORICAL | [source](q042_planck_portability_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-27479381a98dfd4c / python | HISTORICAL | [source](q042_planck_portability_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0838ecb910a82740 / python | HISTORICAL | [source](q042_planck_portability_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3a7bf5559f33d4b7 / python | HISTORICAL | [source](q042_planck_portability_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3a6f6bf95ddf071a / python | HISTORICAL | [source](q042_planck_portability_v6-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d484a96d28d1fc0d / python | HISTORICAL | [source](q042_planck_portability_v6-2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6a1ac70c257f5110 / python | HISTORICAL | [source](q042_planck_portability_v6-3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7e261881b4db3068 / python | HISTORICAL | [source](q042_planck_portability_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6c8933b8e5b11168 / python | HISTORICAL | [source](q042_planck_portability_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6cad0b8c65b5fdf4 / python | HISTORICAL | [source](q042_planck_portability_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d8eaf57e410063e4 / python | HISTORICAL | [source](q042_polychord_partial_init_selftest_v11.py) | python q042_polychord_partial_init_selftest_v11.py |
| ENTRY-32e79628cd1ce8e9 / python | HISTORICAL | [source](q042_polychord_partial_init_selftest_v12.py) | python q042_polychord_partial_init_selftest_v12.py |
| ENTRY-1a2dfbb91b614769 / python | HISTORICAL | [source](q042_polychord_partial_init_selftest_v13.py) | python q042_polychord_partial_init_selftest_v13.py |
| ENTRY-3d2bbbde9645151e / python | HISTORICAL | [source](q042_polychord_partial_init_selftest_v17.py) | python q042_polychord_partial_init_selftest_v17.py |
| ENTRY-868b27ba1775e288 / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-1.sh) | bash q042_prepare_frozen_core_v4-1.sh |
| ENTRY-c02c7e5fb2fe1f5c / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-2.sh) | bash q042_prepare_frozen_core_v4-2.sh |
| ENTRY-1cc8b7100a4dd5a4 / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-3.sh) | bash q042_prepare_frozen_core_v4-3.sh |
| ENTRY-e6f5e08496edd74e / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-4.sh) | bash q042_prepare_frozen_core_v4-4.sh |
| ENTRY-02649cda93e14fac / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-5.sh) | bash q042_prepare_frozen_core_v4-5.sh |
| ENTRY-8a0f00f497493f94 / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-6.sh) | bash q042_prepare_frozen_core_v4-6.sh |
| ENTRY-f018700454309e1a / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4-8.sh) | bash q042_prepare_frozen_core_v4-8.sh |
| ENTRY-892f9e56c2138cf7 / shell | HISTORICAL | [source](q042_prepare_frozen_core_v4.sh) | bash q042_prepare_frozen_core_v4.sh |
| ENTRY-24fd3d591a0f59f0 / python | HISTORICAL | [source](q042_production_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e65fe2f5bd5ea1c3 / python | HISTORICAL | [source](q042_production_tests_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ed69757287c360a5 / python | HISTORICAL | [source](q042_production_tests_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f78a57f9de83e7f5 / python | HISTORICAL | [source](q042_production_tests_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c3a88d7e58400f1b / python | HISTORICAL | [source](q042_production_tests_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-008f4dc9b76b3d17 / python | HISTORICAL | [source](q042_production_tests_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ce4dce6e62ca5633 / python | HISTORICAL | [source](q042_production_tests_v17.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-881cf06f1e98f8b8 / python | HISTORICAL | [source](q042_production_tests_v18.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-38c7f5175285a126 / python | HISTORICAL | [source](q042_production_tests_v19.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-36a1240b8dbd6df4 / python | HISTORICAL | [source](q042_production_tests_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8f23d8bd65c759af / python | HISTORICAL | [source](q042_production_tests_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d37ba99027ea282d / python | HISTORICAL | [source](q042_production_tests_v4-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2c2de452348941ce / python | HISTORICAL | [source](q042_production_tests_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5457aa6e41ee5cc7 / python | HISTORICAL | [source](q042_production_tests_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ed70e2527ee4c075 / python | HISTORICAL | [source](q042_production_tests_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-754dba83f187a362 / python | HISTORICAL | [source](<q042_production_tests_v7 (1).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7a131c6bfc782047 / python | HISTORICAL | [source](<q042_production_tests_v7 (2).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e87d65f2a66b7faf / python | HISTORICAL | [source](<q042_production_tests_v7 (3).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d74921f640b011fc / python | HISTORICAL | [source](<q042_production_tests_v7 (4).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a45aaeaffa777ba3 / python | HISTORICAL | [source](q042_production_tests_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-af49a5a74cdf2807 / python | HISTORICAL | [source](<q042_production_tests_v8 (1).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8d88c3d6e2f7bedc / python | HISTORICAL | [source](<q042_production_tests_v8 (2).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-085ec7eddcc299c2 / python | HISTORICAL | [source](<q042_production_tests_v8 (3).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-552f84d5f02dd269 / python | HISTORICAL | [source](<q042_production_tests_v8 (4).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4205e845bfa84310 / python | HISTORICAL | [source](<q042_production_tests_v8 (5).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0b5c6208007b63bc / python | HISTORICAL | [source](<q042_production_tests_v8 (6).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1d31fc90e9fb46a3 / python | HISTORICAL | [source](<q042_production_tests_v8 (7).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0cce6af594106d7c / python | HISTORICAL | [source](q042_production_tests_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cc7fd8252ca56264 / python | HISTORICAL | [source](<q042_production_tests_v9 (1).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7cbcc643d6bece1e / python | HISTORICAL | [source](q042_production_tests_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7af154a7f99a17b5 / python | HISTORICAL | [source](q042_production_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d2fb94482f780681 / python | HISTORICAL | [source](q042_production_v11.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6e5f67706c8f3ef3 / python | HISTORICAL | [source](q042_production_v12.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c04c099d5ec33b15 / python | HISTORICAL | [source](q042_production_v13.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f0c4887714897606 / python | HISTORICAL | [source](q042_production_v15.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-172cef9c91449589 / python | HISTORICAL | [source](q042_production_v16.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8665a1b728e40273 / python | HISTORICAL | [source](q042_production_v17.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b85f62be92a56015 / python | HISTORICAL | [source](q042_production_v18.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dcae9b0c077b9f2d / python | HISTORICAL | [source](q042_production_v19.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-30f70b028612fa68 / python | HISTORICAL | [source](q042_production_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c7b57a1155371d46 / python | HISTORICAL | [source](q042_production_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-036425d2a4e0dbf7 / python | HISTORICAL | [source](q042_production_v4-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e6fce3f7dfccf7c1 / python | HISTORICAL | [source](q042_production_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-122f18ffb84f2302 / python | HISTORICAL | [source](q042_production_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-143a7bb0073c3d3c / python | HISTORICAL | [source](q042_production_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9a44e1d0c4445d8e / python | HISTORICAL | [source](<q042_production_v7 (1).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4a225c0c5b79d984 / python | HISTORICAL | [source](<q042_production_v7 (2).py>) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-36e28a1bd45e6ccf / python | HISTORICAL | [source](q042_production_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a16d64f390b4d3de / python | HISTORICAL | [source](q042_production_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e9c6b29aaf74f6ba / python | HISTORICAL | [source](q042_production_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-852b267ee8bc8904 / python | HISTORICAL | [source](q042_reference_acquisition_v26.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-84190ced3651d33f / python | HISTORICAL | [source](q042_reference_adapter_selftest_v26.py) | python q042_reference_adapter_selftest_v26.py |
| ENTRY-086d224bfdf359ff / python | HISTORICAL | [source](q042_reference_tests_v26.py) | python q042_reference_tests_v26.py |
| ENTRY-a9d640be9a78e298 / shell | HISTORICAL | [source](q042_setup_prod_v1.sh) | bash q042_setup_prod_v1.sh |
| ENTRY-f96550c9e1b10faa / shell | HISTORICAL | [source](q042_setup_recovery_v11.sh) | bash q042_setup_recovery_v11.sh |
| ENTRY-741ba6ac614c9ae1 / shell | HISTORICAL | [source](q042_setup_recovery_v12.sh) | bash q042_setup_recovery_v12.sh |
| ENTRY-ee4663115404ad4f / shell | HISTORICAL | [source](q042_setup_recovery_v13.sh) | bash q042_setup_recovery_v13.sh |
| ENTRY-c896118378cd146b / shell | HISTORICAL | [source](q042_setup_recovery_v15.sh) | bash q042_setup_recovery_v15.sh |
| ENTRY-7c4708c000718722 / shell | HISTORICAL | [source](q042_setup_recovery_v16.sh) | bash q042_setup_recovery_v16.sh |
| ENTRY-125669a74bd3e70c / shell | HISTORICAL | [source](q042_setup_recovery_v17.sh) | bash q042_setup_recovery_v17.sh |
| ENTRY-7c409e679451dfa2 / shell | HISTORICAL | [source](q042_setup_recovery_v18.sh) | bash q042_setup_recovery_v18.sh |
| ENTRY-d69f16f29527f2f4 / shell | HISTORICAL | [source](q042_setup_recovery_v2.sh) | bash q042_setup_recovery_v2.sh |
| ENTRY-eb5a63573e85ce07 / shell | HISTORICAL | [source](q042_setup_recovery_v3.sh) | bash q042_setup_recovery_v3.sh |
| ENTRY-0bb407e471014623 / shell | HISTORICAL | [source](q042_setup_recovery_v4-1.sh) | bash q042_setup_recovery_v4-1.sh |
| ENTRY-3cde006607eab31b / shell | HISTORICAL | [source](q042_setup_recovery_v4.sh) | bash q042_setup_recovery_v4.sh |
| ENTRY-20bebf2e6efd6da7 / shell | HISTORICAL | [source](q042_setup_recovery_v5.sh) | bash q042_setup_recovery_v5.sh |
| ENTRY-a08766e41d244e9b / shell | HISTORICAL | [source](q042_setup_recovery_v6.sh) | bash q042_setup_recovery_v6.sh |
| ENTRY-a6ccb905ca51fcb2 / shell | HISTORICAL | [source](<q042_setup_recovery_v7 (1).sh>) | bash 'q042_setup_recovery_v7 (1).sh' |
| ENTRY-ca4cc11f904b4193 / shell | HISTORICAL | [source](<q042_setup_recovery_v7 (2).sh>) | bash 'q042_setup_recovery_v7 (2).sh' |
| ENTRY-45de4ceabf8f1e27 / shell | HISTORICAL | [source](<q042_setup_recovery_v7 (3).sh>) | bash 'q042_setup_recovery_v7 (3).sh' |
| ENTRY-aa2cece5e8e58a81 / shell | HISTORICAL | [source](q042_setup_recovery_v7.sh) | bash q042_setup_recovery_v7.sh |
| ENTRY-73a9c3a3ca5ea0e8 / shell | HISTORICAL | [source](q042_setup_recovery_v8.sh) | bash q042_setup_recovery_v8.sh |
| ENTRY-c579a6101204c3fa / shell | HISTORICAL | [source](q042_setup_recovery_v9.sh) | bash q042_setup_recovery_v9.sh |
| ENTRY-0b41341781191168 / shell | HISTORICAL | [source](q042_setup_v10.sh) | bash q042_setup_v10.sh |
| ENTRY-7c8df856a161407c / shell | HISTORICAL | [source](q042_setup_v11.sh) | bash q042_setup_v11.sh |
| ENTRY-93d086a443df6223 / shell | HISTORICAL | [source](q042_setup_v2-1.sh) | bash q042_setup_v2-1.sh |
| ENTRY-571d5f2a248acb03 / shell | HISTORICAL | [source](q042_setup_v2.sh) | bash q042_setup_v2.sh |
| ENTRY-8bce6f0efc4d549a / shell | HISTORICAL | [source](q042_setup_v3.sh) | bash q042_setup_v3.sh |
| ENTRY-9657b8222c1cead0 / shell | HISTORICAL | [source](q042_setup_v4.sh) | bash q042_setup_v4.sh |
| ENTRY-42e4f05e8f23fe3d / shell | HISTORICAL | [source](q042_setup_v5.sh) | bash q042_setup_v5.sh |
| ENTRY-469ba184e9509dc8 / shell | HISTORICAL | [source](q042_setup_v6-1.sh) | bash q042_setup_v6-1.sh |
| ENTRY-f1d801366f59fc0f / shell | HISTORICAL | [source](q042_setup_v6.sh) | bash q042_setup_v6.sh |
| ENTRY-bc0177b76947f473 / shell | HISTORICAL | [source](q042_setup_v7.sh) | bash q042_setup_v7.sh |
| ENTRY-fda6e5b0c649640f / shell | HISTORICAL | [source](q042_setup_v9.sh) | bash q042_setup_v9.sh |
| ENTRY-7dcc3b531c48b5a8 / python | HISTORICAL | [source](q042_source_check_v29.py) | python q042_source_check_v29.py |
| ENTRY-ab6517d4a5222340 / python | HISTORICAL | [source](q042_stock_diagnostic_tests_v20.py) | python q042_stock_diagnostic_tests_v20.py |
| ENTRY-db7dd2b69568d32d / python | HISTORICAL | [source](q042_stock_diagnostic_tests_v21.py) | python q042_stock_diagnostic_tests_v21.py |
| ENTRY-4da84dd1fceb2bf4 / python | HISTORICAL | [source](q042_stock_diagnostic_v20.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-851ecbfd9b19c5ec / python | HISTORICAL | [source](q042_stock_diagnostic_v21.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a2b5ead6483c9c5e / python | HISTORICAL | [source](q042_switch_adapter_selftest_v27.py) | python q042_switch_adapter_selftest_v27.py |
| ENTRY-88587dca079e2f57 / python | HISTORICAL | [source](q042_switch_probe_v27.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4f33bfe98b79258b / python | HISTORICAL | [source](q042_switch_tests_v27.py) | python q042_switch_tests_v27.py |
| ENTRY-aabc49a42ecbed7a / python | HISTORICAL | [source](q045_native_baseline_tests_v1.py) | python q045_native_baseline_tests_v1.py |
| ENTRY-9c3cbd9ce9a137cf / python | HISTORICAL | [source](q045_native_baseline_tests_v2.py) | python q045_native_baseline_tests_v2.py |
| ENTRY-fcef10ef5c0cd449 / python | HISTORICAL | [source](q045_native_baseline_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ecb7adf0b4c96722 / python | HISTORICAL | [source](q045_native_baseline_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-46e0bf3f33db6070 / python | HISTORICAL | [source](q045_optical_audit_tests_v1.py) | python q045_optical_audit_tests_v1.py |
| ENTRY-18b1b1d2e697071c / python | HISTORICAL | [source](q045_optical_audit_tests_v2.py) | python q045_optical_audit_tests_v2.py |
| ENTRY-cb942bd57464279f / python | HISTORICAL | [source](q045_optical_audit_tests_v3.py) | python q045_optical_audit_tests_v3.py |
| ENTRY-4813d8f69096da48 / python | HISTORICAL | [source](q045_optical_audit_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c0f7334cd45b57db / python | HISTORICAL | [source](q045_optical_audit_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-eb762a0e17e86f56 / python | HISTORICAL | [source](q045_optical_audit_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-54215955bbc64889 / python | HISTORICAL | [source](q045_reference_history_tests_v1.py) | python q045_reference_history_tests_v1.py |
| ENTRY-cd31235261f39c95 / python | HISTORICAL | [source](q045_reference_history_tests_v2.py) | python q045_reference_history_tests_v2.py |
| ENTRY-dfff4a508ea804b8 / python | HISTORICAL | [source](q045_reference_history_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-eb4cd05c0fe369a6 / python | HISTORICAL | [source](q045_reference_history_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-58358fed1880b985 / shell | HISTORICAL | [source](q045_setup_baseline_v1.sh) | bash q045_setup_baseline_v1.sh |
| ENTRY-60daf0f4bd54a6dc / shell | HISTORICAL | [source](q045_setup_baseline_v2.sh) | bash q045_setup_baseline_v2.sh |
| ENTRY-09ebfc9a8bff7d26 / python | HISTORICAL | [source](q047_certificate_tests_v1.py) | python q047_certificate_tests_v1.py |
| ENTRY-1a430b1a08da7184 / python | HISTORICAL | [source](q047_certificate_v1.py) | python q047_certificate_v1.py |
| ENTRY-c100b872d8e922fe / python | HISTORICAL | [source](q047_collection_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7ff14d58632ccf98 / python | HISTORICAL | [source](q047_execution_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-18a3a2daa81d03d2 / python | HISTORICAL | [source](q047_math_v1.py) | python q047_math_v1.py |
| ENTRY-fc9ada57f69470ea / python | HISTORICAL | [source](q047_package_check_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d92daccd0d6ab44e / python | HISTORICAL | [source](q047_package_tests_v1.py) | python q047_package_tests_v1.py |
| ENTRY-0e60d2f24c470407 / python | HISTORICAL | [source](q047_precursor_check_v1.py) | python q047_precursor_check_v1.py |
| ENTRY-c98a3c5e1af614a5 / python | HISTORICAL | [source](q047_precursor_tests_v1.py) | python q047_precursor_tests_v1.py |
| ENTRY-fd2a5bc5f5d12538 / python | HISTORICAL | [source](q047_reconstruction_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0d69e94d666a58fc / workflow | HISTORICAL | [source](q048-resume-v4.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-e2abf40ae9bd109a / workflow | HISTORICAL | [source](q048-structural-v6-1.yml) | Not dispatchable at this path; root workflow copy or non-dispatch event only |
| ENTRY-bafa84d2dffd4f47 / python | HISTORICAL | [source](q048_comparison_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-101a1b729c638cb9 / python | HISTORICAL | [source](q048_comparison_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fa046d8f15996fb0 / python | HISTORICAL | [source](q048_firsthit_builder_tests_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7f9abec6a3d9abcd / python | HISTORICAL | [source](q048_firsthit_builder_v1.py) | python q048_firsthit_builder_v1.py |
| ENTRY-1f94ebedfc0c98eb / python | HISTORICAL | [source](q048_frec_moving_h_accept_v87.py) | python q048_frec_moving_h_accept_v87.py |
| ENTRY-380bb2e8cbc03b0e / python | HISTORICAL | [source](q048_frec_moving_h_v31.py) | python q048_frec_moving_h_v31.py |
| ENTRY-5a28655b927be22f / python | HISTORICAL | [source](q048_frec_moving_h_v87.py) | python q048_frec_moving_h_v87.py |
| ENTRY-33962a255a9b47c8 / python | HISTORICAL | [source](q048_frec_moving_h_verify_v31.py) | python q048_frec_moving_h_verify_v31.py |
| ENTRY-1211aadff8ed2af3 / python | HISTORICAL | [source](q048_frec_moving_h_verify_v87.py) | python q048_frec_moving_h_verify_v87.py |
| ENTRY-c6ad19831c08e0c9 / python | HISTORICAL | [source](q048_frec_resume_v7.py) | python q048_frec_resume_v7.py |
| ENTRY-d199f6da2ad19465 / python | HISTORICAL | [source](q048_frec_resume_validate_v7.py) | python q048_frec_resume_validate_v7.py |
| ENTRY-04e72e27973244f0 / python | HISTORICAL | [source](q048_full_tube_reuse_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f363dc1d1a2d3e11 / python | HISTORICAL | [source](q048_full_tube_v99_reconstructed.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fe09a38b5de3dae7 / python | HISTORICAL | [source](q048_guard_continuation_v7.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-84736acbe715dab1 / python | HISTORICAL | [source](q048_guard_package_check_v7.py) | python q048_guard_package_check_v7.py |
| ENTRY-a7315da8c7e9e615 / python | HISTORICAL | [source](q048_guard_resume_v8.py) | python q048_guard_resume_v8.py |
| ENTRY-69c8ff8712b3827f / python | HISTORICAL | [source](q048_guard_resume_verify_v8.py) | python q048_guard_resume_verify_v8.py |
| ENTRY-df010dcb46475dbc / python | HISTORICAL | [source](q048_guard_runner_v7.py) | python q048_guard_runner_v7.py |
| ENTRY-94070472b3e98b45 / python | HISTORICAL | [source](q048_guard_tests_v7.py) | python q048_guard_tests_v7.py |
| ENTRY-dec0c29507ac1a8e / python | HISTORICAL | [source](q048_inputcheck_tests_v1.py) | python q048_inputcheck_tests_v1.py |
| ENTRY-5036a03a9c3c287a / python | HISTORICAL | [source](q048_inputcheck_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fcf4f5c0f90e3303 / python | HISTORICAL | [source](q048_math018_scaled_exp_certificate_v1.py) | python q048_math018_scaled_exp_certificate_v1.py |
| ENTRY-ee9c4ce5ed372668 / python | HISTORICAL | [source](q048_math021_decimal_control_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c017e19cbe92837b / python | HISTORICAL | [source](q048_math021_scalar_enclosure_audit_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-65aff1e0f8fefb15 / python | HISTORICAL | [source](q048_moving_h_domain_accept_v90.py) | python q048_moving_h_domain_accept_v90.py |
| ENTRY-2fa476fc369d349b / python | HISTORICAL | [source](q048_moving_h_domain_v16.py) | python q048_moving_h_domain_v16.py |
| ENTRY-ccf1e5acc2f9380e / python | HISTORICAL | [source](q048_moving_h_domain_v18.py) | python q048_moving_h_domain_v18.py |
| ENTRY-afcad4a05f4e794d / python | HISTORICAL | [source](q048_moving_h_domain_v28-1.py) | python q048_moving_h_domain_v28-1.py |
| ENTRY-cf3023c8e80bfe89 / python | HISTORICAL | [source](q048_moving_h_domain_v30.py) | python q048_moving_h_domain_v30.py |
| ENTRY-e776b50fdb222112 / python | HISTORICAL | [source](q048_moving_h_domain_v54_executed.py) | python q048_moving_h_domain_v54_executed.py |
| ENTRY-156695946a94f3e0 / python | HISTORICAL | [source](q048_moving_h_domain_v90.py) | python q048_moving_h_domain_v90.py |
| ENTRY-6dc26fb9f2877a97 / python | HISTORICAL | [source](q048_moving_h_domain_v98_RECONSTRUCTED_DIAGNOSTIC_ONLY.py) | python q048_moving_h_domain_v98_RECONSTRUCTED_DIAGNOSTIC_ONLY.py |
| ENTRY-0ab2e5ca64279961 / python | HISTORICAL | [source](q048_moving_h_domain_verify_v16.py) | python q048_moving_h_domain_verify_v16.py |
| ENTRY-6090cfed4c421efd / python | HISTORICAL | [source](q048_moving_h_domain_verify_v18.py) | python q048_moving_h_domain_verify_v18.py |
| ENTRY-f46b67ed165abff9 / python | HISTORICAL | [source](q048_moving_h_domain_verify_v28-1.py) | python q048_moving_h_domain_verify_v28-1.py |
| ENTRY-a210b47287caae37 / python | HISTORICAL | [source](q048_moving_h_domain_verify_v30.py) | python q048_moving_h_domain_verify_v30.py |
| ENTRY-fda977ee4a185958 / python | HISTORICAL | [source](q048_moving_h_domain_verify_v90.py) | python q048_moving_h_domain_verify_v90.py |
| ENTRY-2b850ed4ef049fa9 / python | HISTORICAL | [source](q048_p3_scaled_arithmetic_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-62c5190479e180b5 / python | HISTORICAL | [source](q048_p3_scaled_kernel_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3bc93b8b8789fc56 / python | HISTORICAL | [source](q048_package_check_v1.py) | python q048_package_check_v1.py |
| ENTRY-9967fe9d81e3f438 / python | HISTORICAL | [source](q048_phase_turn_package_check_v8.py) | python q048_phase_turn_package_check_v8.py |
| ENTRY-52cb2bcaa2f33d1c / python | HISTORICAL | [source](q048_phase_turn_runner_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-046cd435f4657065 / python | HISTORICAL | [source](q048_phase_turn_tests_v8.py) | python q048_phase_turn_tests_v8.py |
| ENTRY-c9980680e80b113f / python | HISTORICAL | [source](q048_phase_turn_v8.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7774837ddb269d24 / python | HISTORICAL | [source](q048_prefix_merge_v1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6983871696362a64 / python | HISTORICAL | [source](q048_prefix_tests_v1.py) | python q048_prefix_tests_v1.py |
| ENTRY-57dcc73cd97f64b0 / python | HISTORICAL | [source](q048_prefix_v1.py) | python q048_prefix_v1.py |
| ENTRY-d2acb1389d914649 / python | HISTORICAL | [source](q048_resume_controls_v3.py) | python q048_resume_controls_v3.py |
| ENTRY-808ca65518a1fcca / python | HISTORICAL | [source](q048_resume_controls_v4.py) | python q048_resume_controls_v4.py |
| ENTRY-5052b59ed06509eb / python | HISTORICAL | [source](q048_resume_controls_v5.py) | python q048_resume_controls_v5.py |
| ENTRY-e3b97111463c1c60 / python | HISTORICAL | [source](q048_resume_executed_core_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b9bdd3bf90337cf8 / python | HISTORICAL | [source](q048_resume_executed_core_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c118ad6b481d660c / python | HISTORICAL | [source](q048_resume_executed_core_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-da11c7be64e024d4 / python | HISTORICAL | [source](q048_resume_executed_core_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f1876f9ab0f54cb2 / python | HISTORICAL | [source](q048_resume_merge_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0d5b508ea6707256 / python | HISTORICAL | [source](q048_resume_merge_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b4a51a674cf907c7 / python | HISTORICAL | [source](q048_resume_merge_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-41247ab23df213d1 / python | HISTORICAL | [source](q048_resume_merge_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cbbfa8e39c385699 / python | HISTORICAL | [source](q048_resume_package_check_v2.py) | python q048_resume_package_check_v2.py |
| ENTRY-5ad249d58b4692ca / python | HISTORICAL | [source](q048_resume_package_check_v3.py) | python q048_resume_package_check_v3.py |
| ENTRY-a879010fbce73dbf / python | HISTORICAL | [source](q048_resume_package_check_v4.py) | python q048_resume_package_check_v4.py |
| ENTRY-f81ab1cb0ffa301b / python | HISTORICAL | [source](q048_resume_package_check_v5.py) | python q048_resume_package_check_v5.py |
| ENTRY-ab56fb3e0f12fb9f / python | HISTORICAL | [source](q048_resume_tests_v2.py) | python q048_resume_tests_v2.py |
| ENTRY-ae06a143cec96b7d / python | HISTORICAL | [source](q048_resume_tests_v3.py) | python q048_resume_tests_v3.py |
| ENTRY-68f201d2cbc4b8a6 / python | HISTORICAL | [source](q048_resume_tests_v4.py) | python q048_resume_tests_v4.py |
| ENTRY-8c9889cf5b5c1dda / python | HISTORICAL | [source](q048_resume_tests_v5.py) | python q048_resume_tests_v5.py |
| ENTRY-309681509d6caa5a / python | HISTORICAL | [source](q048_resume_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f5f13482ce8c4bfb / python | HISTORICAL | [source](q048_resume_v3.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-17a65178e5f959e6 / python | HISTORICAL | [source](q048_resume_v4.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1c9c0fbdd676d3ef / python | HISTORICAL | [source](q048_resume_v5.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-be2f2ac9299d627a / python | HISTORICAL | [source](q048_structural_package_check_v6.py) | python q048_structural_package_check_v6.py |
| ENTRY-36f42263506bec3b / python | HISTORICAL | [source](q048_structural_runner_v6.py) | python q048_structural_runner_v6.py |
| ENTRY-6c31b5633bb93a9f / python | HISTORICAL | [source](q048_structural_tests_v6.py) | python q048_structural_tests_v6.py |
| ENTRY-e98067543378e8e7 / python | HISTORICAL | [source](q048_structural_v6.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cc6404ec00b57e34 / python | HISTORICAL | [source](q048_threshold_anchor_package_check_v9.py) | python q048_threshold_anchor_package_check_v9.py |
| ENTRY-90cf539e4612b0de / python | HISTORICAL | [source](q048_threshold_anchor_runner_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2bf1810714c73c55 / python | HISTORICAL | [source](q048_threshold_anchor_tests_v9.py) | python q048_threshold_anchor_tests_v9.py |
| ENTRY-5fc65c31d8154f6e / python | HISTORICAL | [source](q048_threshold_anchor_v9.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-dcdef7bf04fc7757 / python | HISTORICAL | [source](q048_v100_refined_thermal_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3da6dbcd8a51edef / python | HISTORICAL | [source](q048_v101_accept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-18b93f3a0445165b / python | HISTORICAL | [source](q048_v101_actual_consumer.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7dabb955f2e69702 / python | HISTORICAL | [source](q048_v101_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-19b911d010d4535c / python | HISTORICAL | [source](q048_v105_accept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b69e8b46e62ec04d / python | HISTORICAL | [source](q048_v105_actual_consumer.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-1cf38c516486acc4 / python | HISTORICAL | [source](q048_v105_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-970056694bdb092a / python | HISTORICAL | [source](q048_v106_accept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-5c60f5de2ecd33ef / python | HISTORICAL | [source](q048_v106_bridge.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2e6b823c25f53030 / python | HISTORICAL | [source](q048_v106_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cb1a03a6dca2c68d / python | HISTORICAL | [source](q048_v107_accept-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0b75be4334fe593b / python | HISTORICAL | [source](q048_v107_actual_consumer.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a3b3605c10389ab7 / python | HISTORICAL | [source](q048_v107_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8fa03f6a1b282762 / python | HISTORICAL | [source](q048_v108_accept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-830fe4a217f59269 / python | HISTORICAL | [source](q048_v108_bridge.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-56ebd00423b0698e / python | HISTORICAL | [source](q048_v108_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-ba96c83fa865d45e / python | HISTORICAL | [source](q048_v109_accept.py) | python q048_v109_accept.py |
| ENTRY-eb5404d4c949598f / python | HISTORICAL | [source](q048_v109_actual_consumer.py) | python q048_v109_actual_consumer.py |
| ENTRY-2572e7ec2459448e / python | HISTORICAL | [source](q048_v109_postaccept.py) | python q048_v109_postaccept.py |
| ENTRY-7e43e6d93a62c70d / python | HISTORICAL | [source](q048_v109_verify.py) | python q048_v109_verify.py |
| ENTRY-2e5e4cb9c365120e / python | HISTORICAL | [source](q048_v110_accept.py) | python q048_v110_accept.py |
| ENTRY-a63243917b42b543 / python | HISTORICAL | [source](q048_v110_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d83d501c6cac735f / python | HISTORICAL | [source](q048_v110_run.py) | python q048_v110_run.py |
| ENTRY-90d139a8a25aab7e / python | HISTORICAL | [source](q048_v110_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-3513d7b6ccc412f6 / python | HISTORICAL | [source](q048_v111_accept.py) | python q048_v111_accept.py |
| ENTRY-c374abfd4b4641b7 / python | HISTORICAL | [source](q048_v111_actual_consumer.py) | python q048_v111_actual_consumer.py |
| ENTRY-7e5c27c7cd296636 / python | HISTORICAL | [source](q048_v111_postaccept.py) | python q048_v111_postaccept.py |
| ENTRY-d16617d4058907a0 / python | HISTORICAL | [source](q048_v111_run.py) | python q048_v111_run.py |
| ENTRY-f44d793930708515 / python | HISTORICAL | [source](q048_v111_verify.py) | python q048_v111_verify.py |
| ENTRY-70ed92ce576a02d8 / python | HISTORICAL | [source](q048_v112_accept.py) | python q048_v112_accept.py |
| ENTRY-6d4f94d8e35db715 / python | HISTORICAL | [source](q048_v112_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-861a243f83c11d12 / python | HISTORICAL | [source](q048_v112_run-1.py) | python q048_v112_run-1.py |
| ENTRY-7d598c19e4016818 / python | HISTORICAL | [source](q048_v112_run.py) | python q048_v112_run.py |
| ENTRY-e1dbf26b057225e9 / python | HISTORICAL | [source](q048_v112_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-4242f369b8ac6102 / python | HISTORICAL | [source](q048_v113_accept.py) | python q048_v113_accept.py |
| ENTRY-9bd89b86760529f1 / python | HISTORICAL | [source](q048_v113_actual_consumer.py) | python q048_v113_actual_consumer.py |
| ENTRY-bd99dafd1c23c1ec / python | HISTORICAL | [source](q048_v113_postaccept.py) | python q048_v113_postaccept.py |
| ENTRY-b7c60c9ff94b9028 / python | HISTORICAL | [source](q048_v113_run.py) | python q048_v113_run.py |
| ENTRY-233e7f734a76c113 / python | HISTORICAL | [source](q048_v113_verify.py) | python q048_v113_verify.py |
| ENTRY-dd0e587cbfb7ed46 / python | HISTORICAL | [source](q048_v114_accept-1.py) | python q048_v114_accept-1.py |
| ENTRY-5beff2d85d793c6d / python | HISTORICAL | [source](q048_v114_accept.py) | python q048_v114_accept.py |
| ENTRY-d9410029d3b4c3bb / python | HISTORICAL | [source](q048_v114_proof-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e3ba80b02ec4dec8 / python | HISTORICAL | [source](q048_v114_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-d941f88a4d9ddb4c / python | HISTORICAL | [source](q048_v114_run-1.py) | python q048_v114_run-1.py |
| ENTRY-44251442ac3329d8 / python | HISTORICAL | [source](q048_v114_run.py) | python q048_v114_run.py |
| ENTRY-ae8013c83a7329c0 / python | HISTORICAL | [source](q048_v114_verify-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-fcfa34881ad8eee5 / python | HISTORICAL | [source](q048_v114_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6e53598270c83e20 / python | HISTORICAL | [source](q048_v116_accept.py) | python q048_v116_accept.py |
| ENTRY-5cb4340aefbc3ff2 / python | HISTORICAL | [source](q048_v116_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-617a3b22d69a95de / python | HISTORICAL | [source](q048_v116_run.py) | python q048_v116_run.py |
| ENTRY-cabb7ef155062e98 / python | HISTORICAL | [source](q048_v116_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a1bbcbcd3f1e9f53 / python | HISTORICAL | [source](q048_v117_accept.py) | python q048_v117_accept.py |
| ENTRY-167e8c87a62b4bb2 / python | HISTORICAL | [source](q048_v117_actual_consumer.py) | python q048_v117_actual_consumer.py |
| ENTRY-5ac51d2a28c0f6f2 / python | HISTORICAL | [source](q048_v117_postaccept.py) | python q048_v117_postaccept.py |
| ENTRY-25c934a4516b8695 / python | HISTORICAL | [source](q048_v117_run.py) | python q048_v117_run.py |
| ENTRY-eca5202495e50dcb / python | HISTORICAL | [source](q048_v117_verify.py) | python q048_v117_verify.py |
| ENTRY-16aef7bae694b3a5 / python | HISTORICAL | [source](q048_v118_accept.py) | python q048_v118_accept.py |
| ENTRY-a3b12e19731c27c5 / python | HISTORICAL | [source](q048_v118_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-6df55c1835093202 / python | HISTORICAL | [source](q048_v118_run-1.py) | python q048_v118_run-1.py |
| ENTRY-3281c844b639ba63 / python | HISTORICAL | [source](q048_v118_run.py) | python q048_v118_run.py |
| ENTRY-113ee7b12a05d47b / python | HISTORICAL | [source](q048_v118_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-b3980610378e29f9 / python | HISTORICAL | [source](q048_v119_accept.py) | python q048_v119_accept.py |
| ENTRY-d48a69b7e6f844f4 / python | HISTORICAL | [source](q048_v119_actual_consumer.py) | python q048_v119_actual_consumer.py |
| ENTRY-82359870a5d2aafc / python | HISTORICAL | [source](q048_v119_postaccept.py) | python q048_v119_postaccept.py |
| ENTRY-f55b32e9b99d9ed1 / python | HISTORICAL | [source](q048_v119_run.py) | python q048_v119_run.py |
| ENTRY-73cccf14f06ac8cc / python | HISTORICAL | [source](q048_v119_verify.py) | python q048_v119_verify.py |
| ENTRY-2d29959fa36e4101 / python | HISTORICAL | [source](q048_v120_accept.py) | python q048_v120_accept.py |
| ENTRY-aaf1fb56878d3960 / python | HISTORICAL | [source](q048_v120_proof.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-f7c82fdbf02b9ec5 / python | HISTORICAL | [source](q048_v120_run.py) | python q048_v120_run.py |
| ENTRY-59884d33b2c3c830 / python | HISTORICAL | [source](q048_v120_verify.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-2590badc721dd910 / python | HISTORICAL | [source](q048_v121_accept.py) | python q048_v121_accept.py |
| ENTRY-8072d622228a6e77 / python | HISTORICAL | [source](q048_v121_actual_consumer.py) | python q048_v121_actual_consumer.py |
| ENTRY-880f5a837af4e9e1 / python | HISTORICAL | [source](q048_v121_postaccept.py) | python q048_v121_postaccept.py |
| ENTRY-6acc9ae24f600d83 / python | HISTORICAL | [source](q048_v121_run.py) | python q048_v121_run.py |
| ENTRY-3691479612395987 / python | HISTORICAL | [source](q048_v121_verify.py) | python q048_v121_verify.py |
| ENTRY-05a279bc669cd9fb / python | HISTORICAL | [source](q048_v122_accept.py) | python q048_v122_accept.py |
| ENTRY-1f4cc842f64e63ba / python | HISTORICAL | [source](q048_v122_diagnostic.py) | python q048_v122_diagnostic.py |
| ENTRY-4c6a0c1646b2d3d7 / python | HISTORICAL | [source](q048_v122_run.py) | python q048_v122_run.py |
| ENTRY-fce687b33ff03bd8 / python | HISTORICAL | [source](q048_v122_verify.py) | python q048_v122_verify.py |
| ENTRY-bf50211abfe242fc / python | HISTORICAL | [source](q048_v141_proof.py) | python q048_v141_proof.py |
| ENTRY-a2e62b4d0942cf6a / python | HISTORICAL | [source](q048_v141_run.py) | python q048_v141_run.py |
| ENTRY-8e3c8ae9910182a0 / python | HISTORICAL | [source](q048_v141_verify.py) | python q048_v141_verify.py |
| ENTRY-eac413d08eadfc5c / python | HISTORICAL | [source](q048_v142_proof.py) | python q048_v142_proof.py |
| ENTRY-ae828e887b086613 / python | HISTORICAL | [source](q048_v142_run.py) | python q048_v142_run.py |
| ENTRY-b027451e7d0e2e10 / python | HISTORICAL | [source](q048_v142_verify.py) | python q048_v142_verify.py |
| ENTRY-fb97d8fdd393183e / python | HISTORICAL | [source](q048_v144_accept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-8e289a3e904cd4df / python | HISTORICAL | [source](q048_v144_consumer.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-9d6efc74f56b92cc / python | HISTORICAL | [source](q048_v144_contract.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0d70df94543da9a6 / python | HISTORICAL | [source](q048_v144_postaccept.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7e8510eb49f61c55 / python | HISTORICAL | [source](q048_v144_publish-1.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-7d823b307235d027 / python | HISTORICAL | [source](q048_v144_publish.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-0b0d8f7c44dfd3ee / python | HISTORICAL | [source](q048_v144_run.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-e9ae8ed4c98e16a0 / python | HISTORICAL | [source](q048_v144_validate.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-a18e25f520c02331 / python | HISTORICAL | [source](q048_v7_repository_patch.py) | python q048_v7_repository_patch.py |
| ENTRY-bbbdffef6f9229e8 / python | HISTORICAL | [source](q048_v87_consumer_contract.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-93e60a5f25327edb / python | HISTORICAL | [source](q048_v87_freeze_and_execute.py) | python q048_v87_freeze_and_execute.py |
| ENTRY-e1afc2cc325585f1 / python | HISTORICAL | [source](q048_v87_import_probe.py) | python q048_v87_import_probe.py |
| ENTRY-d4880bc24ed2c234 / python | HISTORICAL | [source](q048_v8_repository_patch.py) | python q048_v8_repository_patch.py |
| ENTRY-8959d23017193e11 / python | HISTORICAL | [source](q048_v90_freeze_and_execute-1.py) | python q048_v90_freeze_and_execute-1.py |
| ENTRY-57796695b36551ee / python | HISTORICAL | [source](q048_v90_freeze_and_execute.py) | python q048_v90_freeze_and_execute.py |
| ENTRY-818748249a95bdf9 / python | HISTORICAL | [source](q048_v90_import_probe-1.py) | python q048_v90_import_probe-1.py |
| ENTRY-84ae433274cec19d / python | HISTORICAL | [source](q048_v90_import_probe.py) | python q048_v90_import_probe.py |
| ENTRY-a90563b7f059519f / python | HISTORICAL | [source](q048_v90_proof_contract.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c71dbdfb9eafb33d / python | HISTORICAL | [source](q048_v98_proof_contract_RECONSTRUCTED_DIAGNOSTIC_ONLY.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-cf5dd2bddc129293 / python | HISTORICAL | [source](q048_v99_gate_diagnostic.py) | python q048_v99_gate_diagnostic.py |
| ENTRY-6ffc9e2bd423d44e / python | HISTORICAL | [source](q048_v9_repository_patch.py) | python q048_v9_repository_patch.py |
| ENTRY-3da16d14221b0070 / python | HISTORICAL | [source](run_q048_p3_scaled_v2.py) | python run_q048_p3_scaled_v2.py |
| ENTRY-df45934b1a9ab9d3 / python | HISTORICAL | [source](test_q047_execution_v1.py) | python test_q047_execution_v1.py |
| ENTRY-a410b850df61ee7a / python | HISTORICAL | [source](test_q047_reconstruction_v1.py) | python test_q047_reconstruction_v1.py |
| ENTRY-75e7be961cfdcf84 / python | HISTORICAL | [source](test_q048_moving_h_v90-1.py) | python test_q048_moving_h_v90-1.py |
| ENTRY-98eda1b0477aaede / python | HISTORICAL | [source](test_q048_moving_h_v90.py) | python test_q048_moving_h_v90.py |
| ENTRY-27f748e689f28b0b / python | HISTORICAL | [source](test_q048_p3_scaled_v2.py) | python test_q048_p3_scaled_v2.py |
| ENTRY-98aa6b082ae2841c / python | HISTORICAL | [source](test_q048_v109_contract.py) | python test_q048_v109_contract.py |
| ENTRY-76542ec533ac61b1 / python | HISTORICAL | [source](test_q048_v110_binding.py) | python test_q048_v110_binding.py |
| ENTRY-6df7130b304a04d5 / python | HISTORICAL | [source](test_q048_v111_contract.py) | python test_q048_v111_contract.py |
| ENTRY-c22b30cdda98e90e / python | HISTORICAL | [source](test_q048_v112_binding.py) | python test_q048_v112_binding.py |
| ENTRY-67afbf50878ad56c / python | HISTORICAL | [source](test_q048_v113_contract.py) | python test_q048_v113_contract.py |
| ENTRY-8de733fd76ec043b / python | HISTORICAL | [source](test_q048_v114_binding-1.py) | python test_q048_v114_binding-1.py |
| ENTRY-e9e456f64f2c537f / python | HISTORICAL | [source](test_q048_v114_binding.py) | python test_q048_v114_binding.py |
| ENTRY-47e163cb9a892cf3 / python | HISTORICAL | [source](test_q048_v116_binding.py) | python test_q048_v116_binding.py |
| ENTRY-d26bc55acc0a8214 / python | HISTORICAL | [source](test_q048_v117_contract.py) | python test_q048_v117_contract.py |
| ENTRY-8c83c8dae61bd9b3 / python | HISTORICAL | [source](test_q048_v118_binding.py) | python test_q048_v118_binding.py |
| ENTRY-e67be9c5f6b79e99 / python | HISTORICAL | [source](test_q048_v119_contract.py) | python test_q048_v119_contract.py |
| ENTRY-693f82e7d9c60887 / python | HISTORICAL | [source](test_q048_v120_binding.py) | python test_q048_v120_binding.py |
| ENTRY-725b109940aaa61a / python | HISTORICAL | [source](test_q048_v121_contract.py) | python test_q048_v121_contract.py |
| ENTRY-4c8ffc46ff3b24ef / python | HISTORICAL | [source](test_q048_v122_dispatch.py) | python test_q048_v122_dispatch.py |
| ENTRY-a6f9f1978d4db1b0 / python | HISTORICAL | [source](test_q048_v87_contract.py) | python test_q048_v87_contract.py |
| ENTRY-92c9384a0fda17fd / python | HISTORICAL | [source](test_q048_v87_import_layout.py) | python test_q048_v87_import_layout.py |
| ENTRY-4a59220c9342a7ac / python | HISTORICAL | [source](test_q048_v90_layout-1.py) | python test_q048_v90_layout-1.py |
| ENTRY-f8c2937c94b3adba / python | HISTORICAL | [source](test_q048_v90_layout.py) | python test_q048_v90_layout.py |
| ENTRY-66e0317ad8b3a371 / python | HISTORICAL | [source](verify_q048_p3_scaled_v2.py) | No standalone main, syntax error, or required argument/subcommand context; use exact owning workflow steps, not a fabricated command |
| ENTRY-c14474ca60d52f00 / python | ACTIVE | [source](tools/maintenance/check_cleanup_integrity.py) | python tools/maintenance/check_cleanup_integrity.py |
| ENTRY-0f4c7160266e16a7 / python | ACTIVE | [source](tests/maintenance/test_cleanup_integrity.py) | python -m unittest discover -s tests/maintenance -v |
| ENTRY-0faa444a82ad3f3f / setup | ACTIVE | [source](tools/maintenance/check_cleanup_integrity.py) | python --version |

## Historical registry snapshots — reference only

These entries preserve every discovered program in frozen registry snapshots. They do not add current launch IDs. Original workflow/parameter metadata is in the machine-readable registry; use the original checkout if a separately authorized historical reconstruction is needed.

| Program | Snapshot | Current command |
| --- | --- | --- |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-FGPROFILE-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V2 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V3 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V4 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V5 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V2 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V3 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V4 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V1 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V10 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V11 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V12 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V13 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V14 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V15 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V16 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V17 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V2 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V3 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V4 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V5 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V6 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V7 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V8 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V9 | [source](<bubbleverse_program_registry(20260912-101957).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-FGPROFILE-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V2 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V3 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V4 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V5 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V2 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V3 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V4 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V1 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V10 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V11 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V12 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V13 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V14 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V15 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V16 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V17 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V2 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V3 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V4 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V5 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V6 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V7 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V8 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V9 | [source](<bubbleverse_program_registry(20260912-103059).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-FGPROFILE-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V3 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V4 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-CMBSPACE-V5 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V3 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q040-RQMC-V4 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V10 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V11 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V12 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V13 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V14 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V15 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V16 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V17 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V18 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V19 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V3 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V4 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V5 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V6 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V7 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V8 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q041-PLANCKPORT-V9 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-STOCKDIAG-V20 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-STOCKDIAG-V21 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-DURABLE-V22 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-CLASSCAUSE-V23 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-CLASSORIGIN-V24 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-CLASSNAN-V25 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-REFACQ-V26 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-SWITCHPROBE-V27 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-EVENTCELL-V28 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q042-CONTEXT-V29 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-BASELINE-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-BASELINE-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-OPTICAL-AUDIT-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-OPTICAL-AUDIT-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-OPTICAL-AUDIT-V3 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-REFHIST-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q045-REFHIST-V2 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q047-CERTCHECK-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q047-PRECURSORCHECK-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q047-COLLECTION-PREFLIGHT-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q047-RECONSTRUCTION-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q048-INPUTCHECK-V1 | [source](<bubbleverse_program_registry(20261011-163107).json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry_V2.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry_V3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry_V3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry_V3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V4 | [source](<bubbleverse_program_registry_q036_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V5 | [source](<bubbleverse_program_registry_q036_v5.json>) | Unavailable as a supported current route; original metadata retained |
| Q037-TTGEOM-V1 | [source](<bubbleverse_program_registry_q037_v1.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V2 | [source](<bubbleverse_program_registry_q039_v2.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V2 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V3 | [source](<bubbleverse_program_registry_q039_v3.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V3 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V2 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q036-GEOMETRY-V1 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q038-COORDLOC-V1 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V1 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V2 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V3 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V4 | [source](<bubbleverse_program_registry_q039_v4.json>) | Unavailable as a supported current route; original metadata retained |
| Q039-IMPLBLOCK-V5 | [source](<bubbleverse_program_registry_q039_v5.json>) | Unavailable as a supported current route; original metadata retained |

## Cleanup installer V3.3.0

Source: [.github/workflows/apply-bubbleverse-cleanup-v330.yml](.github/workflows/apply-bubbleverse-cleanup-v330.yml). Upload the self-contained program to `cleanup-installation/v330/bubbleverse_cleanup_v330.py`. Preview validates without publishing. Apply publishes a separate branch; merge is manual.

```bash
gh workflow run apply-bubbleverse-cleanup-v330.yml --repo Morfindien/Bubbleverse --ref main -f mode=preview
gh workflow run apply-bubbleverse-cleanup-v330.yml --repo Morfindien/Bubbleverse --ref main -f mode=apply
```
