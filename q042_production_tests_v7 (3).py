#!/usr/bin/env python3
"""Static and runtime regression gates for Q042-PROD-V7."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

Q = "Q-042"
PROGRAM_ID = "Q042-PROD-V7"
WORKFLOW = ".github/workflows/q042-production-v7.yml"
V1_SPEC_SHA256 = "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256 = "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V1_EXECUTION_COMMIT = "6c44a4117449145afd0a3ae6eb238490686a8c6d"
V1_ROOT_RUN_ID = 36133813540


def read(p):
    x = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL {p}")
    return x


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, x):
    Path(p).write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def static(a):
    spec = read(a.spec)
    lock = read(a.source_lock)
    recovery = read(a.recovery_spec)
    patch = read(a.registry_patch)
    pr = Path(a.program).read_text(encoding="utf-8")
    wf = Path(a.workflow).read_text(encoding="utf-8")
    setup = Path(a.setup).read_text(encoding="utf-8")
    readme_patch = Path(a.readme_patch).read_text(encoding="utf-8")

    gates = {}

    def gate(name, cond):
        if not cond:
            raise RuntimeError(f"{name}=FAIL")
        gates[name] = "PASS"

    gate("Q_IDENTITY", spec.get("q") == Q and lock.get("q") == Q)
    gate("SCIENTIFIC_SPEC_BYTE_IDENTITY", sha(a.spec) == V1_SPEC_SHA256)
    gate("PARENT_SOURCE_LOCK_BYTE_IDENTITY", sha(a.parent_source_lock) == V1_SOURCE_LOCK_SHA256)
    gate("RECOVERY_SOURCE_LOCK_IDENTITY", lock.get("program_id") == PROGRAM_ID)
    gate("RECOVERY_SPEC_IDENTITY", recovery.get("program_id") == PROGRAM_ID)
    gate("TECHNICAL_PARENT_COMMIT", lock["technical_parent"]["execution_commit"] == V1_EXECUTION_COMMIT)
    gate("TECHNICAL_PARENT_ROOT_RUN", int(lock["technical_parent"]["root_github_run_id"]) == V1_ROOT_RUN_ID)
    gate("SCIENTIFIC_CONTRACT_UNCHANGED", recovery.get("scientific_contract_changed") is False)
    gate("BOBYQA_REUSE_80", recovery["bobyqa_reuse"]["expected_record_count"] == 80)
    gate("BOBYQA_RECOMPUTE_ZERO", recovery["bobyqa_reuse"]["recompute_in_recovery"] == 0)
    gate("POLYCHORD_20_CELLS", recovery["posterior_recovery"]["fresh_cell_count"] == 20)

    gate("PROGRAM_NO_BOBYQA_STAGE", '"bobyqa-stage"' not in pr)
    gate("PROGRAM_METADATA_FILTER", "POLYCHORD_EXECUTABLE_KEYS" in pr and "POLYCHORD_METADATA_ONLY_KEYS" in pr)
    gate("PROGRAM_COBAYA_UPDATE_INFO", "update_info" in pr and "validate_polychord_options" in pr)
    gate("PROGRAM_V1_REJECTION_REGRESSION", "V1_DICTIONARY_REJECTION_REGRESSION_GATE" in pr)
    gate("PROGRAM_BOBYQA_IMPORT", "import-bobyqa" in pr and "IMPORTED_EXISTING_V1_COMPUTATION" in pr)
    gate("PROGRAM_78_2_LINEAGE", "eligible != 78 or failed != 2" in pr)

    gate("WORKFLOW_PROGRAM_ID", "PROGRAM_ID: Q042-PROD-V7" in wf)
    gate("WORKFLOW_NO_BOBYQA_MATRIX", "bobyqa-production:" not in wf)
    # Regression for V2 deployment failure: import-bobyqa must install numpy before importing q042_production_v7.py.
    import_block = wf.split("  import-bobyqa:",1)[1].split("\n  start-collector:",1)[0]
    dep_line = "python -m pip install --disable-pip-version-check PyYAML==6.0.2 numpy==1.26.4"
    gate("IMPORT_BOBYQA_NUMPY_DEPENDENCY", dep_line in import_block)
    gate("IMPORT_BOBYQA_DEPENDENCY_BEFORE_EXECUTION", import_block.find(dep_line) < import_block.find("python q042_production_v7.py import-bobyqa"))
    gate("WORKFLOW_IMPORTS_V1_BOBYQA", str(V1_ROOT_RUN_ID) in wf and "import-bobyqa" in wf)
    gate("WORKFLOW_POLYCHORD_MATRIX", "polychord-segment0:" in wf and "max-parallel: 4" in wf)
    gate("WORKFLOW_CHECKPOINT_BEFORE_DISPATCH", wf.find("checkpoint-${{ matrix.arm }}") < wf.find("Dispatch continuation after checkpoint upload"))
    gate("WORKFLOW_COLLECTOR", "collector:" in wf and "q042-production-final-v7" in wf)
    gate("WORKFLOW_FINAL_REQUIRES_20_PLUS_IMPORT", "EXPECTED=21" in wf)
    # Recovery-owned version integrity. Historical/frozen references are allowed only by exact token.
    forbidden_stale = [
        "q042-production-final-v2",
        "q042_production_polychord_final_v2.json",
        "q042_production_bobyqa_start_v2.json",
        "q042_prod_static_v2.json",
        "q042_prod_static_tests_v2.json",
        "q042_v2_env_bundle",
        "adapted_bobyqa_v2",
        "q042_bobyqa_import_summary_v2.json",
        "POLYCHORD_PRODUCTION_FINAL_V2",
        "PRODUCTION_FINAL_V2",
    ]
    gate("WORKFLOW_NO_STALE_RECOVERY_V2_REFERENCES", not any(x in wf for x in forbidden_stale))
    gate("PROGRAM_NO_STALE_RECOVERY_V2_FILENAMES",
         "q042_production_polychord_final_v2.json" not in pr and
         "q042_production_bobyqa_start_v2.json" not in pr)
    gate("WORKFLOW_NO_STALE_RECOVERY_V5_FILENAMES",
         "q042-production-final-v5" not in wf and
         "q042_production_polychord_final_v5.json" not in wf and
         "q042_v5_env_bundle" not in wf)
    gate("PROGRAM_NO_STALE_RECOVERY_V5_FILENAMES",
         "q042_production_polychord_final_v5.json" not in pr and
         "q042_production_bobyqa_start_v5.json" not in pr)
    gate("WORKFLOW_48_SEGMENT_POLICY", "max_polychord_segments_per_cell" in wf)
    gate("WORKFLOW_240_MIN_SOFT", "--soft-minutes 240" in wf)
    gate("WORKFLOW_330_MIN_JOB", "timeout-minutes: 330" in wf)
    gate("CANARY_JOB_PRESENT", "polychord-canary-segment0:" in wf)
    gate("INITIAL_355_MIN_JOB_BUDGET", wf.count("timeout-minutes: 355") >= 2)
    gate("CANARY_USES_330_MINUTES", "--segment 0 --soft-minutes 330" in wf)
    gate("CANARY_RESUME_PROBE_PRESENT", "polychord-canary-resume-probe:" in wf)
    gate("CANARY_RESUME_PROBE_5_MINUTES", "--segment 1 --soft-minutes 5 --resume-probe" in wf)
    gate("FANOUT_DEPENDS_ON_CANARY_RESUME_GATE", "needs: [environment, import-bobyqa, polychord-canary-resume-probe]" in wf)
    gate("CANARY_EXCLUDED_FROM_MATRIX", "exclude:" in wf and "arm: hillipop" in wf and "model: ede_n3" in wf and "combination: FULL" in wf)
    gate("INITIAL_MATRIX_FAIL_FAST", "fail-fast: true" in wf)
    gate("PROGRAM_EXPLICIT_PRECHECKPOINT_STATUS", "SOFT_STOP_BEFORE_RESUMABLE_CHECKPOINT" in pr)
    gate("PROGRAM_CHECKPOINT_VALIDATION", "def checkpoint_state(" in pr and "updated_seed_ok" in pr and "nonempty_resume_files" in pr and "resume_snapshot" in pr)
    gate("PROGRAM_CHECKPOINT_ADVANCEMENT_GATE", "def checkpoint_advanced(" in pr and "RESUME_CHECKPOINT_DID_NOT_ADVANCE" in pr)
    gate("PROGRAM_RESUME_LIFECYCLE_PROOF", "worker_lifecycle_v7.json" in pr and "COBAYA_STORED_UPDATED_INFO" in pr and "resumed_process_started" in pr)
    gate("PROGRAM_RESUME_PROBE_MODE", "RESUME_PROBE_PASSED" in pr and "resume_probe" in pr)
    gate("WORKFLOW_DISCARDS_PROBE_CHECKPOINT", "checkpoint-hillipop-ede_n3-FULL-s1" not in wf)
    gate("WORKFLOW_REAL_CANARY_CONTINUES_FROM_S0", '-f segment=1 -f previous_run_id="$GITHUB_RUN_ID" -f root_run_id="$GITHUB_RUN_ID"' in wf)
    gate("WORKFLOW_REGENERATES_REDUCED_ENVIRONMENT",
         "q042_production_v7.py prepare-nonoverlap" in wf)
    gate("WORKFLOW_REDUCED_ENVIRONMENT_EQUIVALENCE",
         "q042_production_v7.py verify-reduced-environment" in wf)
    gate("WORKFLOW_RUNTIME_PREFLIGHT_USES_V7_REDUCED_META",
         "--reduced-hlp-meta q042_environment/q042_hillipop_nonoverlap_precision_prod_v7.json" in wf)
    gate("WORKFLOW_DOWNSTREAM_USES_V7_REDUCED_META",
         wf.count("--reduced-hlp-meta env_bundle/q042_environment/q042_hillipop_nonoverlap_precision_prod_v7.json") >= 2)
    gate("WORKFLOW_DOES_NOT_USE_PARENT_REDUCED_META_AS_ACTIVE_INPUT",
         "--reduced-hlp-meta recovered_v1_env/q042_environment/q042_hillipop_nonoverlap_precision_prod_v1.json" not in wf)
    gate("PROGRAM_HAS_REDUCED_EQUIVALENCE_GATE",
         "REDUCED_ENVIRONMENT_SCIENCE_EQUIVALENCE_GATE" in pr and
         "Q042_PROD_V7_REDUCED_ENVIRONMENT_EQUIVALENCE_GATE=PASS" in pr)

    entry = patch.get("patch", {}).get(PROGRAM_ID)
    gate("REGISTRY_ENTRY_PRESENT", isinstance(entry, dict))
    gate("REGISTRY_ACTIVE", entry.get("status") == "ACTIVE")
    gate("REGISTRY_WORKFLOW", entry.get("workflow_id") == "q042-production-v7.yml")
    gate("REGISTRY_Q", entry.get("q") == Q)
    gate("REGISTRY_PARENT", entry.get("technical_parent_program_id") == "Q042-PROD-V6")
    gate("SCIENTIFIC_PROVENANCE_PARENT_REMAINS_V1", lock["technical_parent"]["program_id"] == "Q042-PROD-V1")
    gate("DEPLOYMENT_PARENT_IS_IMMEDIATE_PREDECESSOR", recovery["deployment_parent"]["program_id"] == "Q042-PROD-V6")

    gate("SETUP_REUSES_V1_RUNTIME", "q042_setup_prod_v1.sh" in setup)
    gate("SETUP_EXACT_COBAYA", "3.5.6" in setup)
    gate("README_PATCH_CANONICAL_LAUNCHER", "🚀 BUBBLEVERSE START" in readme_patch and "00-bubbleverse-start.yml" in readme_patch)

    try:
        import yaml
        y = yaml.safe_load(wf)
        gate("WORKFLOW_YAML_PARSE", isinstance(y, dict))
    except Exception as exc:
        raise RuntimeError(f"WORKFLOW_YAML_PARSE=FAIL {exc}")

    gate("STATIC_GATE_COUNT", len(gates) >= 30)

    write(
        a.output,
        {
            "q": Q,
            "program_id": PROGRAM_ID,
            "stage": "Q042_PROD_V7_STATIC_TESTS",
            "status": "PASS",
            "gate_count": len(gates),
            "gates": gates,
        },
    )
    print(f"Q042_PROD_V7_STATIC_TEST_GATE=PASS_{len(gates)}")
    return 0


def runtime_adapter(a):
    # Delegate the exact Cobaya 3.5.6 regression to the production program.
    import subprocess, sys
    cmd = [
        sys.executable,
        a.program,
        "sampler-adapter-regression",
        "--spec", a.spec,
        "--source-lock", a.source_lock,
        "--external-runtime", a.external_runtime,
        "--output", a.output,
    ]
    subprocess.run(cmd, check=True)
    d = read(a.output)
    if d.get("status") != "PASS" or not d.get("v1_dictionary_rejected") or not d.get("corrected_dictionary_accepted"):
        raise RuntimeError("RUNTIME_ADAPTER_GATE=FAIL")
    print("Q042_PROD_V7_RUNTIME_ADAPTER_TEST_GATE=PASS")
    return 0


def parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("static")
    for x in (
        "spec", "source-lock", "parent-source-lock", "recovery-spec", "program",
        "workflow", "setup", "registry-patch", "readme-patch", "output",
    ):
        s.add_argument("--" + x, required=True)
    s.set_defaults(func=static)

    s = sp.add_parser("runtime-adapter")
    for x in ("program", "spec", "source-lock", "external-runtime", "output"):
        s.add_argument("--" + x, required=True)
    s.set_defaults(func=runtime_adapter)
    return p


if __name__ == "__main__":
    a = parser().parse_args()
    raise SystemExit(a.func(a))
