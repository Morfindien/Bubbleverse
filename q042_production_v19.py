#!/usr/bin/env python3
"""Bubbleverse Q042 production recovery V19 — merge-only finalization repair.

V19 performs no new PolyChord or Py-BOBYQA computation. It consumes the exact
existing Q042-PROD-V18 artifact set from frozen root run 36731879692, adapts
only the recovery-owned filenames expected by the inherited V1 merge routine,
and then delegates all scientific merge/classification logic byte-for-byte to
q042_production_v1.merge_final.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

import q042_production_v1 as v1

Q = "Q-042"
CASE_ID = "NOT DOCUMENTED"
PROGRAM_ID = "Q042-PROD-V19"
RUN_ID = "Q042-PRODUCTION-PORTABILITY-V19"
RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-019"

SOURCE_PROGRAM_ID = "Q042-PROD-V18"
SOURCE_RUN_ID = "Q042-PRODUCTION-PORTABILITY-V18"
SOURCE_RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-018"
SOURCE_ROOT_RUN_ID = 36731879692
SOURCE_EXECUTION_COMMIT = "d0f92c7f2ce53da32818244f8847f8e745e20c4f"
SOURCE_FAILED_COLLECTOR_RUN_ID = 37151674348
SOURCE_FAILED_COLLECTOR_JOB_ID = 111286678009

V1_SPEC_SHA256 = "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256 = "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V18_SOURCE_LOCK_SHA256 = "6d79b78592438c082f1bd6dc472931d18b00a4a7525cf67bd1633ba1c77e4dde"
V18_PROGRAM_SHA256 = "19d27facbb92e1e030460883c4d9155cb16e97d04d2c4816723e622716e42962"
V18_WORKFLOW_SHA256 = "95ecae46549732f6fc1263a5d0116590ca784104bc11894a279a8cce4a175a5c"

ARMS = ("camspec", "hillipop")
MODELS = ("lcdm", "ede_n3")
COMBINATIONS = ("FULL", "NO_ACT_PRIMARY", "NO_ACT_LENSING", "NO_DESI_DR2", "NO_SN")


def sha256_file(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def read_json(p):
    x = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return x


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False, default=str) + "\n", encoding="utf-8")
    os.replace(t, p)


def load_spec(p):
    p = Path(p)
    if sha256_file(p) != V1_SPEC_SHA256:
        raise RuntimeError("SCIENTIFIC_SPEC_BYTE_IDENTITY_GATE=FAIL")
    d = read_json(p)
    if (d.get("q"), d.get("case_id"), d.get("program_id"), d.get("run_id"), d.get("result_id")) != (
        Q, CASE_ID, "Q042-PROD-V1", "Q042-PRODUCTION-PORTABILITY-V1", "R-Q042-PRODUCTION-PORTABILITY-001"
    ):
        raise RuntimeError("SCIENTIFIC_SPEC_IDENTITY_GATE=FAIL")
    c = d.get("authoritative_contract") or {}
    if tuple(c.get("arms") or ()) != ARMS or tuple(c.get("models") or ()) != MODELS:
        raise RuntimeError("AUTHORITATIVE_CONTRACT_GATE=FAIL")
    if set((c.get("data_combinations") or {}).keys()) != set(COMBINATIONS) or int(c.get("required_cell_count", -1)) != 20:
        raise RuntimeError("AUTHORITATIVE_CELL_MATRIX_GATE=FAIL")
    return d


def load_lock(p, spec):
    d = read_json(p)
    if (d.get("q"), d.get("case_id"), d.get("program_id"), d.get("run_id"), d.get("result_id")) != (
        Q, CASE_ID, PROGRAM_ID, RUN_ID, RESULT_ID
    ):
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("scientific_spec_sha256") != sha256_file(spec):
        raise RuntimeError("SOURCE_LOCK_SCIENTIFIC_SPEC_GATE=FAIL")
    v1lock = Path(d.get("scientific_parent_source_lock_file", ""))
    if not v1lock.is_file() or sha256_file(v1lock) != d.get("scientific_parent_source_lock_sha256") or sha256_file(v1lock) != V1_SOURCE_LOCK_SHA256:
        raise RuntimeError("V1_PARENT_SOURCE_LOCK_GATE=FAIL")
    v18lock = Path(d.get("technical_parent_source_lock_file", ""))
    if not v18lock.is_file() or sha256_file(v18lock) != d.get("technical_parent_source_lock_sha256") or sha256_file(v18lock) != V18_SOURCE_LOCK_SHA256:
        raise RuntimeError("V18_PARENT_SOURCE_LOCK_GATE=FAIL")
    tp = d.get("technical_parent") or {}
    if tp.get("program_id") != SOURCE_PROGRAM_ID or int(tp.get("root_github_run_id", -1)) != SOURCE_ROOT_RUN_ID or tp.get("execution_commit") != SOURCE_EXECUTION_COMMIT:
        raise RuntimeError("V18_TECHNICAL_PARENT_GATE=FAIL")
    return d


def expected_cells():
    return {(a, m, c) for a in ARMS for m in MODELS for c in COMBINATIONS}


def validate_source_records(root: Path):
    poly_paths = list(root.rglob("q042_production_polychord_final_v18.json"))
    bob_paths = list(root.rglob("q042_production_bobyqa_start_v13.json"))
    if len(poly_paths) != 20:
        raise RuntimeError(f"V18_POLYCHORD_FINAL_COUNT_GATE=FAIL count={len(poly_paths)}")
    if len(bob_paths) != 80:
        raise RuntimeError(f"V18_BOBYQA_IMPORT_COUNT_GATE=FAIL count={len(bob_paths)}")

    seen = set()
    for p in poly_paths:
        d = read_json(p)
        if d.get("q") != Q or d.get("program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError(f"V18_POLYCHORD_IDENTITY_GATE=FAIL path={p}")
        cell = (d.get("arm"), d.get("model"), d.get("combination"))
        if cell in seen:
            raise RuntimeError(f"V18_POLYCHORD_DUPLICATE_CELL_GATE=FAIL cell={cell}")
        seen.add(cell)
    if seen != expected_cells():
        raise RuntimeError(f"V18_POLYCHORD_CELL_COMPLETENESS_GATE=FAIL missing={sorted(expected_cells()-seen)}")

    starts = {}
    for p in bob_paths:
        d = read_json(p)
        if d.get("q") != Q or d.get("program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError(f"V18_BOBYQA_IDENTITY_GATE=FAIL path={p}")
        cell = (d.get("arm"), d.get("model"), d.get("combination"))
        idx = int(d.get("start_index", -1))
        starts.setdefault(cell, set()).add(idx)
    if set(starts) != expected_cells() or any(v != {0,1,2,3} for v in starts.values()):
        raise RuntimeError("V18_BOBYQA_CELL_START_COMPLETENESS_GATE=FAIL")
    return poly_paths, bob_paths


def install_compatibility_shadows(poly_paths, bob_paths):
    shadows = []
    for p in poly_paths:
        q = p.with_name("q042_production_polychord_final_v1.json")
        if q.exists():
            raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
        shutil.copy2(p, q)
        shadows.append(q)
    for p in bob_paths:
        q = p.with_name("q042_production_bobyqa_start_v1.json")
        if q.exists():
            raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
        shutil.copy2(p, q)
        shadows.append(q)
    return shadows


def configure_v1_merge_for_v18_inputs():
    # Inputs are genuine V18 records. Keep V18 identity while the inherited V1
    # merge routine reads them; V19 relabels only the final technical envelope.
    v1.Q = Q
    v1.CASE_ID = CASE_ID
    v1.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.RUN_ID = SOURCE_RUN_ID
    v1.RESULT_ID = SOURCE_RESULT_ID
    v1.core.Q = Q
    v1.core.CASE_ID = CASE_ID
    v1.core.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.core.RUN_ID = SOURCE_RUN_ID
    v1.core.RESULT_ID = SOURCE_RESULT_ID
    v1.core.legacy.Q = Q
    v1.core.legacy.PROGRAM_ID = SOURCE_PROGRAM_ID
    v1.core.legacy.RUN_ID = SOURCE_RUN_ID
    v1.core.legacy.RESULT_ID = SOURCE_RESULT_ID
    v1.load_spec = load_spec
    v1.load_lock = load_lock


def merge_final(a):
    load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    root = Path(a.input_dir)
    poly_paths, bob_paths = validate_source_records(root)

    manifest = read_json(a.artifact_manifest) if a.artifact_manifest else None
    if manifest is not None:
        if manifest.get("q") != Q or manifest.get("source_program_id") != SOURCE_PROGRAM_ID:
            raise RuntimeError("ARTIFACT_MANIFEST_IDENTITY_GATE=FAIL")
        if int(manifest.get("source_root_run_id", -1)) != SOURCE_ROOT_RUN_ID or int(manifest.get("selected_artifact_count", -1)) != 21:
            raise RuntimeError("ARTIFACT_MANIFEST_COUNT_GATE=FAIL")

    shadows = install_compatibility_shadows(poly_paths, bob_paths)
    try:
        configure_v1_merge_for_v18_inputs()
        rc = v1.merge_final(a)
    finally:
        for p in shadows:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    out = read_json(a.output)
    inherited_gate = out.get("final_result_gate")
    inherited_class = out.get("downstream_portability_classification")
    out.update({
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "PRODUCTION_FINAL_V19",
        "technical_recovery_class": "MERGE_ONLY_EXISTING_V18_ARTIFACTS",
        "scientific_contract_changed": False,
        "scientific_spec_origin_program_id": "Q042-PROD-V1",
        "scientific_spec_sha256": sha256_file(a.spec),
        "source_program_id": SOURCE_PROGRAM_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_result_id": SOURCE_RESULT_ID,
        "source_root_github_run_id": SOURCE_ROOT_RUN_ID,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "source_failed_collector_run_id": SOURCE_FAILED_COLLECTOR_RUN_ID,
        "source_failed_collector_job_id": SOURCE_FAILED_COLLECTOR_JOB_ID,
        "source_failed_collector_gate": "V13_POLYCHORD_FINAL_COUNT_GATE=FAIL",
        "source_polychord_final_filename": "q042_production_polychord_final_v18.json",
        "source_bobyqa_record_filename": "q042_production_bobyqa_start_v13.json",
        "polychord_recomputed_in_v19": 0,
        "bobyqa_recomputed_in_v19": 0,
        "source_polychord_final_count": 20,
        "source_bobyqa_record_count": 80,
        "inherited_v1_final_result_gate": inherited_gate,
        "inherited_v1_downstream_portability_classification": inherited_class,
        "technical_parent_source_lock_sha256": lock["technical_parent_source_lock_sha256"],
    })
    gates = out.setdefault("gates", {})
    gates["V18_ARTIFACT_SET_COMPLETE"] = "PASS"
    gates["V18_POLYCHORD_FINAL_FILENAME_ADAPTER"] = "PASS"
    gates["V18_BOBYQA_COMPATIBILITY_FILENAME_ADAPTER"] = "PASS"
    gates["V1_SCIENTIFIC_MERGE_CLASSIFICATION_REUSED"] = "PASS"
    gates["NO_NEW_POLYCHORD_COMPUTE_V19"] = "PASS"
    gates["NO_NEW_BOBYQA_COMPUTE_V19"] = "PASS"
    if manifest is not None:
        gates["V18_ARTIFACT_DIGEST_SELECTION_MANIFEST"] = "PASS"
        out["source_artifact_selection_manifest_sha256"] = sha256_file(a.artifact_manifest)
    write_json(a.output, out)
    print("Q042_PROD_V19_FINAL_GATE=" + str(out.get("final_result_gate")))
    return rc


def static_check(a):
    load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    write_json(a.output, {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "MERGE_ONLY_STATIC_V19",
        "status": "PASS",
        "scientific_result": False,
        "scientific_contract_changed": False,
        "source_program_id": SOURCE_PROGRAM_ID,
        "source_root_github_run_id": SOURCE_ROOT_RUN_ID,
        "source_execution_commit": SOURCE_EXECUTION_COMMIT,
        "required_polychord_final_count": 20,
        "required_bobyqa_record_count": 80,
        "new_compute": False,
        "gates": {
            "V1_SCIENTIFIC_SPEC_BYTE_IDENTITY": "PASS",
            "V1_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
            "V18_SOURCE_LOCK_BYTE_IDENTITY": "PASS",
            "V18_TECHNICAL_PARENT": "PASS",
            "MERGE_ONLY": "PASS",
        },
    })
    print("Q042_PROD_V19_STATIC_GATE=PASS")
    return 0


def parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("static")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=static_check)
    s = sp.add_parser("merge-final")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--artifact-manifest", required=False, default="")
    s.add_argument("--output", required=True)
    s.set_defaults(func=merge_final)
    return p


if __name__ == "__main__":
    a = parser().parse_args()
    raise SystemExit(a.func(a))
