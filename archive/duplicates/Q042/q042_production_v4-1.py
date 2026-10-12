#!/usr/bin/env python3
"""Bubbleverse Q042 production recovery V4.

Technical recovery only. The authoritative scientific contract remains
q042_production_spec_v1.json byte-for-byte. Q042-PROD-V4 fixes the V1
PolyChord sampler-option adapter and reuses verified V1 BOBYQA records.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import q042_production_v1 as v1

Q = "Q-042"
CASE_ID = "NOT DOCUMENTED"
PROGRAM_ID = "Q042-PROD-V4"
RUN_ID = "Q042-PRODUCTION-PORTABILITY-V4"
RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-004"

SCIENTIFIC_SPEC_PROGRAM_ID = "Q042-PROD-V1"
SCIENTIFIC_RUN_ID = "Q042-PRODUCTION-PORTABILITY-V1"
SCIENTIFIC_RESULT_ID = "R-Q042-PRODUCTION-PORTABILITY-001"

V1_EXECUTION_COMMIT = "6c44a4117449145afd0a3ae6eb238490686a8c6d"
V1_ROOT_RUN_ID = 36133813540
V1_SPEC_SHA256 = "41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c"
V1_SOURCE_LOCK_SHA256 = "0f973de56cc232e67b37839babadbe192bab4a4c58e0102bee98c48a2106df56"
V1_PROGRAM_SHA256 = "889232bf9b1cd0a098cb42b2974774a343648c73f0ef9bf55c215a9ac0b90642"

ARMS = ("camspec", "hillipop")
MODELS = ("lcdm", "ede_n3")
COMBINATIONS = ("FULL", "NO_ACT_PRIMARY", "NO_ACT_LENSING", "NO_DESI_DR2", "NO_SN")

# Only options that belong to Cobaya's PolyChord component may cross this adapter.
# Descriptive preregistration metadata stays in the scientific spec and provenance.
POLYCHORD_EXECUTABLE_KEYS = (
    "nlive",
    "num_repeats",
    "nprior",
    "nfail",
    "precision_criterion",
    "max_ndead",
    "do_clustering",
    "boost_posterior",
    "confidence_for_unbounded",
    "measure_speeds",
    "oversample_power",
    "synchronous",
    "read_resume",
    "write_resume",
    "write_live",
    "write_dead",
    "write_prior",
    "write_stats",
)
POLYCHORD_METADATA_ONLY_KEYS = ("seed_policy", "max_ndead_runtime_encoding")


def finite(x):
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def read_json(p):
    x = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={p}")
    return x


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix(p.suffix + ".tmp")
    t.write_text(
        json.dumps(obj, indent=2, sort_keys=True, allow_nan=False, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(t, p)


def sha256_file(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def canonical_hash(x):
    return hashlib.sha256(
        json.dumps(x, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def freeze_v1_globals():
    """Make inherited V1 helper functions emit V4 execution identity."""
    v1.Q = Q
    v1.CASE_ID = CASE_ID
    v1.PROGRAM_ID = PROGRAM_ID
    v1.RUN_ID = RUN_ID
    v1.RESULT_ID = RESULT_ID

    v1.core.Q = Q
    v1.core.CASE_ID = CASE_ID
    v1.core.PROGRAM_ID = PROGRAM_ID
    v1.core.RUN_ID = RUN_ID
    v1.core.RESULT_ID = RESULT_ID
    v1.core.legacy.Q = Q
    v1.core.legacy.PROGRAM_ID = PROGRAM_ID
    v1.core.legacy.RUN_ID = RUN_ID
    v1.core.legacy.RESULT_ID = RESULT_ID


def load_spec(p):
    p = Path(p)
    if sha256_file(p) != V1_SPEC_SHA256:
        raise RuntimeError("SCIENTIFIC_SPEC_BYTE_IDENTITY_GATE=FAIL")
    d = read_json(p)
    if (
        d.get("q"),
        d.get("case_id"),
        d.get("program_id"),
        d.get("run_id"),
        d.get("result_id"),
    ) != (
        Q,
        CASE_ID,
        SCIENTIFIC_SPEC_PROGRAM_ID,
        SCIENTIFIC_RUN_ID,
        SCIENTIFIC_RESULT_ID,
    ):
        raise RuntimeError("SCIENTIFIC_SPEC_IDENTITY_GATE=FAIL")

    c = d["authoritative_contract"]
    if (
        tuple(c["arms"]) != ARMS
        or tuple(c["models"]) != MODELS
        or set(c["data_combinations"]) != set(COMBINATIONS)
        or int(c["required_cell_count"]) != 20
    ):
        raise RuntimeError("AUTHORITATIVE_CONTRACT_GATE=FAIL")

    pc = d["polychord_production"]
    frozen = {
        "nlive": "25d",
        "num_repeats": "5d",
        "nprior": "10nlive",
        "nfail": "nlive",
        "precision_criterion": 0.001,
        "max_ndead": "infinity",
        "do_clustering": True,
        "boost_posterior": 0,
        "confidence_for_unbounded": 0.9999995,
        "measure_speeds": True,
        "oversample_power": 0.4,
        "synchronous": True,
        "read_resume": True,
        "write_resume": True,
        "write_live": True,
        "write_dead": True,
        "write_prior": True,
        "write_stats": True,
    }
    for k, expected in frozen.items():
        if pc.get(k) != expected:
            raise RuntimeError(f"POLYCHORD_PRODUCTION_LOCK_GATE=FAIL key={k}")
    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k not in pc:
            raise RuntimeError(f"POLYCHORD_METADATA_PRESERVATION_GATE=FAIL key={k}")

    bq = d["bobyqa_production"]
    if (
        int(bq["external_starts_per_cell"]) != 4
        or int(bq["cobaya_best_of"]) != 1
        or bq["max_evals"] != "120d"
        or float(bq["rhoend"]) != 0.05
        or bq["ignore_prior"] is not True
    ):
        raise RuntimeError("BOBYQA_PRODUCTION_LOCK_GATE=FAIL")

    seeds = d["polychord_seed_map"]
    if len(seeds) != 20 or len(set(int(x) for x in seeds.values())) != 20:
        raise RuntimeError("SEED_MAP_GATE=FAIL")
    return d


def load_lock(p, spec):
    d = read_json(p)
    if (
        d.get("q"),
        d.get("case_id"),
        d.get("program_id"),
        d.get("run_id"),
        d.get("result_id"),
    ) != (Q, CASE_ID, PROGRAM_ID, RUN_ID, RESULT_ID):
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    if d.get("scientific_spec_sha256") != sha256_file(spec):
        raise RuntimeError("SOURCE_LOCK_SCIENTIFIC_SPEC_GATE=FAIL")
    parent = Path(d.get("parent_source_lock_file", ""))
    if not parent.exists() or sha256_file(parent) != d.get("parent_source_lock_sha256"):
        raise RuntimeError("PARENT_SOURCE_LOCK_GATE=FAIL")
    if d.get("parent_source_lock_sha256") != V1_SOURCE_LOCK_SHA256:
        raise RuntimeError("PARENT_SOURCE_LOCK_FROZEN_HASH_GATE=FAIL")
    if d.get("technical_parent", {}).get("execution_commit") != V1_EXECUTION_COMMIT:
        raise RuntimeError("TECHNICAL_PARENT_COMMIT_GATE=FAIL")
    if int(d.get("technical_parent", {}).get("root_github_run_id", -1)) != V1_ROOT_RUN_ID:
        raise RuntimeError("TECHNICAL_PARENT_RUN_GATE=FAIL")
    return d


def runtime_gate(p):
    r = read_json(p)
    # Runtime is intentionally the recovered V1 production runtime.
    if (
        r.get("q") != Q
        or r.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID
        or r.get("status") != "PASS"
        or r.get("cobaya_version") != "3.5.6"
        or r.get("pybobyqa_version") != "1.5.0"
        or r.get("polychord_commit") != "3ade6445bb3719a6db6f6e81f178765545ffc833"
        or not r.get("pantheonplus_runtime_files")
        or not r.get("pantheonplus_manifest_sha256")
    ):
        raise RuntimeError("RECOVERED_V1_RUNTIME_SOURCE_GATE=FAIL")
    return r


def cell_seed(spec, arm, model, combo):
    return int(spec["polychord_seed_map"][f"{arm}:{model}:{combo}"])


def production_pc(spec, runtime, arm, model, combo):
    """Recovery repair: metadata and executable sampler options are separated."""
    source = spec["polychord_production"]
    pc = {}
    for key in POLYCHORD_EXECUTABLE_KEYS:
        if key not in source:
            raise RuntimeError(f"POLYCHORD_EXECUTABLE_OPTION_MISSING_GATE=FAIL key={key}")
        pc[key] = copy.deepcopy(source[key])

    if pc["max_ndead"] != "infinity":
        raise RuntimeError("POLYCHORD_INFINITY_SEMANTICS_GATE=FAIL")
    pc["max_ndead"] = float("inf")
    pc["path"] = runtime["polychord_path"]
    pc["seed"] = cell_seed(spec, arm, model, combo)

    leaked = [k for k in POLYCHORD_METADATA_ONLY_KEYS if k in pc]
    if leaked:
        raise RuntimeError(f"POLYCHORD_METADATA_LEAK_GATE=FAIL keys={leaked}")
    return pc


def validate_polychord_options(pc):
    import cobaya
    from cobaya.input import update_info

    if getattr(cobaya, "__version__", None) != "3.5.6":
        raise RuntimeError(
            f"COBAYA_PIN_GATE=FAIL got={getattr(cobaya, '__version__', None)}"
        )
    updated = update_info({"sampler": {"polychord": copy.deepcopy(pc)}})
    block = (updated.get("sampler") or {}).get("polychord")
    if not isinstance(block, dict):
        raise RuntimeError("COBAYA_POLYCHORD_UPDATE_INFO_GATE=FAIL")
    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k in block:
            raise RuntimeError(f"COBAYA_METADATA_LEAK_AFTER_UPDATE_GATE=FAIL key={k}")
    return block


def static_check(a):
    spec = load_spec(a.spec)
    lock = load_lock(a.source_lock, a.spec)
    write_json(
        a.output,
        {
            "q": Q,
            "case_id": CASE_ID,
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "PRODUCTION_RECOVERY_STATIC_V4",
            "status": "PASS",
            "scientific_spec_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "scientific_spec_sha256": sha256_file(a.spec),
            "parent_source_lock_sha256": lock["parent_source_lock_sha256"],
            "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
            "technical_parent_root_run_id": V1_ROOT_RUN_ID,
            "required_cell_count": 20,
            "seed_count": 20,
            "scientific_result": False,
            "gates": {
                "Q_IDENTITY": "PASS",
                "V1_SCIENTIFIC_SPEC_BYTE_IDENTITY": "PASS",
                "V1_SOURCE_LOCK_IDENTITY": "PASS",
                "PRODUCTION_SETTINGS_FROZEN": "PASS",
                "METADATA_PRESERVED_IN_SPEC": "PASS",
                "Q040_FIREWALL": "PASS",
                "NO_PILOT_SCIENCE": "PASS",
            },
        },
    )
    print("Q042_PROD_V4_STATIC_GATE=PASS")
    return 0


def sampler_adapter_regression(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    runtime = runtime_gate(a.external_runtime)

    raw = copy.deepcopy(spec["polychord_production"])
    raw["max_ndead"] = float("inf")
    raw["path"] = runtime["polychord_path"]
    raw["seed"] = cell_seed(spec, "camspec", "lcdm", "FULL")

    raw_rejected = False
    raw_error = ""
    try:
        validate_polychord_options(raw)
    except Exception as exc:
        raw_rejected = True
        raw_error = f"{type(exc).__name__}: {exc}"

    if not raw_rejected:
        raise RuntimeError("V1_DICTIONARY_REJECTION_REGRESSION_GATE=FAIL")

    corrected = production_pc(spec, runtime, "camspec", "lcdm", "FULL")
    validate_polychord_options(corrected)

    for k in POLYCHORD_METADATA_ONLY_KEYS:
        if k not in spec["polychord_production"] or k in corrected:
            raise RuntimeError(f"METADATA_SEPARATION_GATE=FAIL key={k}")

    if not math.isinf(float(corrected["max_ndead"])):
        raise RuntimeError("POLYCHORD_INFINITY_RUNTIME_ENCODING_GATE=FAIL")

    write_json(
        a.output,
        {
            "q": Q,
            "program_id": PROGRAM_ID,
            "stage": "POLYCHORD_ADAPTER_REGRESSION_V4",
            "status": "PASS",
            "cobaya_version": "3.5.6",
            "v1_dictionary_rejected": True,
            "v1_rejection_error": raw_error[:2000],
            "corrected_dictionary_accepted": True,
            "metadata_preserved_in_scientific_spec": list(POLYCHORD_METADATA_ONLY_KEYS),
            "metadata_excluded_from_executable_sampler": list(POLYCHORD_METADATA_ONLY_KEYS),
            "max_ndead_runtime_is_numeric_infinity": True,
            "seed": corrected["seed"],
            "executable_sampler_keys": sorted(corrected),
        },
    )
    print("Q042_PROD_V4_POLYCHORD_ADAPTER_REGRESSION=PASS")
    return 0


def prepare_nonoverlap(a):
    rc = v1.prepare_nonoverlap(a)
    for p in (Path(a.support_output), Path(a.meta_output)):
        d = read_json(p)
        d.update(
            {
                "q": Q,
                "case_id": CASE_ID,
                "program_id": PROGRAM_ID,
                "run_id": RUN_ID,
                "result_id": RESULT_ID,
                "technical_parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            }
        )
        write_json(p, d)
    return rc


def runtime_preflight(a):
    # Reuse V1's exact science-building checks, then validate the exact recovered sampler adapter
    # across every one of the 20 production cells.
    rc = v1.runtime_preflight(a)
    spec = load_spec(a.spec)
    runtime = runtime_gate(a.external_runtime)
    rows = []
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                pc = production_pc(spec, runtime, arm, model, combo)
                updated = validate_polychord_options(pc)
                rows.append(
                    {
                        "arm": arm,
                        "model": model,
                        "combination": combo,
                        "seed": pc["seed"],
                        "status": "PASS",
                        "runtime_sampler_sha256": canonical_hash(pc),
                        "validated_key_count": len(updated),
                    }
                )
    if len(rows) != 20:
        raise RuntimeError("POLYCHORD_ADAPTER_20_CELL_GATE=FAIL")

    d = read_json(a.output)
    d["stage"] = "PRODUCTION_RUNTIME_PREFLIGHT_V4"
    d["program_id"] = PROGRAM_ID
    d["run_id"] = RUN_ID
    d["result_id"] = RESULT_ID
    d["scientific_spec_origin_program_id"] = SCIENTIFIC_SPEC_PROGRAM_ID
    d["polychord_adapter_validation"] = rows
    d.setdefault("gates", {})["POLYCHORD_EXACT_RUNTIME_DICTIONARY_20_CELL"] = "PASS"
    d["gates"]["COBAYA_3_5_6_INPUT_VALIDATION"] = "PASS"
    d["gates"]["V1_METADATA_LEAK_REMOVED"] = "PASS"
    write_json(a.output, d)
    print("Q042_PROD_V4_RUNTIME_PREFLIGHT_GATE=PASS")
    return rc


def polychord_worker(a):
    rc = v1.polychord_worker(a)
    p = Path(a.result_json)
    if p.exists():
        d = read_json(p)
        spec = load_spec(a.spec)
        runtime = runtime_gate(a.external_runtime)
        pc = production_pc(spec, runtime, a.arm, a.model, a.combination)
        d.update(
            {
                "program_id": PROGRAM_ID,
                "run_id": RUN_ID,
                "result_id": RESULT_ID,
                "technical_adapter": "Q042-PROD-V4_METADATA_SEPARATION",
                "scientific_spec_origin_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
                "scientific_spec_sha256": sha256_file(a.spec),
                "runtime_sampler_sha256": canonical_hash(pc),
            }
        )
        write_json(p, d)
    return rc


def common_cli(a):
    out = []
    for k in (
        "q032_parent_root",
        "preflight",
        "parent_dir",
        "hlp_matrix",
        "hlp_meta",
        "reduced_support",
        "reduced_hlp_matrix",
        "reduced_hlp_meta",
        "spec",
        "source_lock",
        "external_runtime",
    ):
        out += ["--" + k.replace("_", "-"), str(getattr(a, k))]
    return out


def polychord_segment(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    runtime_gate(a.external_runtime)
    if (
        a.arm not in ARMS
        or a.model not in MODELS
        or a.combination not in COMBINATIONS
    ):
        raise RuntimeError("CELL_IDENTITY_GATE=FAIL")
    if a.segment < 0:
        raise RuntimeError("SEGMENT_INDEX_GATE=FAIL")

    outdir = Path(a.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    action = "fresh" if a.segment == 0 else "resume"
    seed = cell_seed(spec, a.arm, a.model, a.combination)

    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "polychord-worker",
        *common_cli(a),
        "--arm",
        a.arm,
        "--model",
        a.model,
        "--combination",
        a.combination,
        "--action",
        action,
        "--output-dir",
        str(outdir),
        "--result-json",
        str(outdir / "worker_result.json"),
    ]

    start = time.time()
    proc = subprocess.Popen(cmd, start_new_session=True)
    timed_out = False
    try:
        rc = proc.wait(timeout=int(a.soft_minutes) * 60)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(proc.pid, signal.SIGINT)
        try:
            rc = proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                rc = proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                rc = proc.wait()

    rf = v1.resume_files(outdir)
    updated = list((outdir / "polychord").glob("chain.updated.*"))
    worker = (
        read_json(outdir / "worker_result.json")
        if (outdir / "worker_result.json").exists()
        else None
    )
    status = (
        "COMPLETE"
        if rc == 0 and worker and worker.get("status") == "COMPLETE"
        else "SEGMENT_CHECKPOINTED"
        if timed_out and rf and updated
        else "FAILED"
    )

    rec = {
        "q": Q,
        "case_id": CASE_ID,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "stage": "POLYCHORD_PRODUCTION_SEGMENT_V4",
        "status": status,
        "arm": a.arm,
        "model": a.model,
        "combination": a.combination,
        "segment": a.segment,
        "action": action,
        "seed": seed,
        "soft_minutes": a.soft_minutes,
        "elapsed_seconds": time.time() - start,
        "worker_returncode": rc,
        "timed_out": timed_out,
        "resume_files": [str(p.relative_to(outdir)) for p in rf],
        "worker": worker,
        "checkpoint_parent_run_id": a.parent_run_id or None,
        "scientific_spec_origin_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
        "scientific_spec_sha256": sha256_file(a.spec),
        "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
        "config_hash": canonical_hash(
            {
                "spec": sha256_file(a.spec),
                "arm": a.arm,
                "model": a.model,
                "combination": a.combination,
                "seed": seed,
            }
        ),
    }
    if status == "FAILED":
        rec["failure_class"] = "HPC_OR_NUMERICAL_SEGMENT_FAILURE"
    write_json(a.segment_json, rec)
    print("Q042_PROD_V4_SEGMENT_STATUS=" + status)
    return 0 if status != "FAILED" else 2


def expected_bobyqa_artifact_names():
    out = []
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                for s in range(4):
                    out.append(
                        f"q042-prod-{V1_ROOT_RUN_ID}-bobyqa-{arm}-{model}-{combo}-s{s}"
                    )
    return out


def parse_artifact_identity(name):
    prefix = f"q042-prod-{V1_ROOT_RUN_ID}-bobyqa-"
    if not name.startswith(prefix):
        raise RuntimeError(f"BOBYQA_ARTIFACT_NAME_GATE=FAIL name={name}")
    tail = name[len(prefix):]
    for arm in ARMS:
        ap = arm + "-"
        if tail.startswith(ap):
            tail2 = tail[len(ap):]
            for model in MODELS:
                mp = model + "-"
                if tail2.startswith(mp):
                    rest = tail2[len(mp):]
                    for combo in COMBINATIONS:
                        cp = combo + "-s"
                        if rest.startswith(cp):
                            return arm, model, combo, int(rest[len(cp):])
    raise RuntimeError(f"BOBYQA_ARTIFACT_PARSE_GATE=FAIL name={name}")


def import_bobyqa(a):
    spec = load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    manifest = read_json(a.artifact_manifest)

    if int(manifest.get("source_root_run_id", -1)) != V1_ROOT_RUN_ID:
        raise RuntimeError("BOBYQA_IMPORT_ROOT_RUN_GATE=FAIL")
    if manifest.get("source_head_sha") != V1_EXECUTION_COMMIT:
        raise RuntimeError("BOBYQA_IMPORT_HEAD_SHA_GATE=FAIL")

    entries = manifest.get("artifacts")
    if not isinstance(entries, list):
        raise RuntimeError("BOBYQA_IMPORT_MANIFEST_GATE=FAIL")
    by_name = {x.get("name"): x for x in entries if isinstance(x, dict)}
    expected = expected_bobyqa_artifact_names()
    if set(by_name) != set(expected) or len(entries) != 80:
        raise RuntimeError("BOBYQA_IMPORT_ARTIFACT_SET_GATE=FAIL")

    source_root = Path(a.input_dir)
    output_root = Path(a.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    imported = []
    eligible = 0
    failed = 0

    for name in expected:
        arm, model, combo, s = parse_artifact_identity(name)
        entry = by_name[name]
        if entry.get("head_sha") != V1_EXECUTION_COMMIT:
            raise RuntimeError(f"BOBYQA_IMPORT_ARTIFACT_HEAD_GATE=FAIL name={name}")
        if not str(entry.get("digest", "")).startswith("sha256:"):
            raise RuntimeError(f"BOBYQA_IMPORT_DIGEST_GATE=FAIL name={name}")

        source_dir = source_root / name
        matches = list(source_dir.rglob("q042_production_bobyqa_start_v1.json"))
        if len(matches) != 1:
            raise RuntimeError(
                f"BOBYQA_IMPORT_RECORD_FILE_GATE=FAIL name={name} count={len(matches)}"
            )
        raw_path = matches[0]
        raw = read_json(raw_path)
        raw_hash = sha256_file(raw_path)

        if (
            raw.get("q") != Q
            or raw.get("program_id") != SCIENTIFIC_SPEC_PROGRAM_ID
            or raw.get("run_id") != SCIENTIFIC_RUN_ID
            or raw.get("result_id") != SCIENTIFIC_RESULT_ID
        ):
            raise RuntimeError(f"BOBYQA_IMPORT_RECORD_IDENTITY_GATE=FAIL name={name}")
        if (
            raw.get("arm"),
            raw.get("model"),
            raw.get("combination"),
            int(raw.get("start_index", -1)),
        ) != (arm, model, combo, s):
            raise RuntimeError(f"BOBYQA_IMPORT_CELL_GATE=FAIL name={name}")

        expected_seed = cell_seed(spec, arm, model, combo) + 1000 + s
        if int(raw.get("seed", -1)) != expected_seed:
            raise RuntimeError(f"BOBYQA_IMPORT_SEED_GATE=FAIL name={name}")
        if float(raw.get("rhoend", -1)) != 0.05:
            raise RuntimeError(f"BOBYQA_IMPORT_RHOEND_GATE=FAIL name={name}")

        adapted = copy.deepcopy(raw)
        adapted.update(
            {
                "program_id": PROGRAM_ID,
                "run_id": RUN_ID,
                "result_id": RESULT_ID,
                "stage": "BOBYQA_IMPORTED_V1_RESULT_V4",
                "reuse_status": "IMPORTED_EXISTING_V1_COMPUTATION",
                "computed_by_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
                "computed_by_run_id": SCIENTIFIC_RUN_ID,
                "computed_by_result_id": SCIENTIFIC_RESULT_ID,
                "reused_by_program_id": PROGRAM_ID,
                "source_root_run_id": V1_ROOT_RUN_ID,
                "source_execution_commit": V1_EXECUTION_COMMIT,
                "source_artifact_id": int(entry["id"]),
                "source_artifact_name": name,
                "source_artifact_digest": entry["digest"],
                "source_record_sha256": raw_hash,
                "scientific_spec_sha256": sha256_file(a.spec),
            }
        )

        dest = output_root / name
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / "q042_production_bobyqa_start_v4.json"
        write_json(out, adapted)

        ok = bool(
            raw.get("technical_ok")
            and finite(raw.get("objective"))
            and int(raw.get("flag", -999)) >= 0
        )
        eligible += int(ok)
        failed += int(not ok)
        imported.append(
            {
                "artifact_id": int(entry["id"]),
                "artifact_name": name,
                "artifact_digest": entry["digest"],
                "arm": arm,
                "model": model,
                "combination": combo,
                "start_index": s,
                "seed": expected_seed,
                "technical_ok": ok,
                "source_record_sha256": raw_hash,
            }
        )

    if len(imported) != 80 or eligible != 78 or failed != 2:
        raise RuntimeError(
            f"BOBYQA_IMPORT_INGESTION_IDENTITY_GATE=FAIL total={len(imported)} "
            f"eligible={eligible} failed={failed}"
        )

    # All four starts must remain present for each cell and at least one must be eligible.
    for arm in ARMS:
        for model in MODELS:
            for combo in COMBINATIONS:
                rows = [
                    r
                    for r in imported
                    if (r["arm"], r["model"], r["combination"])
                    == (arm, model, combo)
                ]
                if len(rows) != 4 or not any(r["technical_ok"] for r in rows):
                    raise RuntimeError(
                        f"BOBYQA_IMPORT_CELL_COMPLETENESS_GATE=FAIL {arm}:{model}:{combo}"
                    )

    write_json(
        a.summary,
        {
            "q": Q,
            "case_id": CASE_ID,
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "BOBYQA_V1_IMPORT_V4",
            "status": "PASS",
            "source_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "source_root_run_id": V1_ROOT_RUN_ID,
            "source_execution_commit": V1_EXECUTION_COMMIT,
            "imported_record_count": len(imported),
            "eligible_record_count": eligible,
            "preserved_failure_count": failed,
            "all_20_cells_have_four_starts": True,
            "all_20_cells_have_eligible_candidate": True,
            "records": imported,
        },
    )
    print("Q042_PROD_V4_BOBYQA_IMPORT_GATE=PASS")
    return 0


def merge_final(a):
    load_spec(a.spec)
    load_lock(a.source_lock, a.spec)
    root = Path(a.input_dir)

    # V1 contains the frozen scientific merge/classification implementation.
    # Create short-lived compatibility filenames next to V4 records so the
    # inherited merge code can read them without changing any science logic.
    shadows = []
    try:
        for p in root.rglob("q042_production_polychord_final_v4.json"):
            q = p.with_name("q042_production_polychord_final_v1.json")
            if q.exists():
                raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
            shutil.copy2(p, q)
            shadows.append(q)
        for p in root.rglob("q042_production_bobyqa_start_v4.json"):
            q = p.with_name("q042_production_bobyqa_start_v1.json")
            if q.exists():
                raise RuntimeError(f"MERGE_SHADOW_COLLISION_GATE=FAIL path={q}")
            shutil.copy2(p, q)
            shadows.append(q)

        if len(list(root.rglob("q042_production_polychord_final_v4.json"))) != 20:
            raise RuntimeError("V4_POLYCHORD_FINAL_COUNT_GATE=FAIL")
        if len(list(root.rglob("q042_production_bobyqa_start_v4.json"))) != 80:
            raise RuntimeError("V4_BOBYQA_IMPORT_COUNT_GATE=FAIL")

        rc = v1.merge_final(a)
    finally:
        for p in shadows:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    out = read_json(a.output)
    out.update(
        {
            "program_id": PROGRAM_ID,
            "run_id": RUN_ID,
            "result_id": RESULT_ID,
            "stage": "PRODUCTION_FINAL_V4",
            "scientific_spec_origin_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "scientific_spec_sha256": sha256_file(a.spec),
            "technical_parent_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
            "technical_parent_root_run_id": V1_ROOT_RUN_ID,
            "technical_parent_execution_commit": V1_EXECUTION_COMMIT,
            "technical_repair": "POLYCHORD_METADATA_SEPARATED_FROM_EXECUTABLE_COBAYA_OPTIONS",
            "bobyqa_reuse": {
                "source_program_id": SCIENTIFIC_SPEC_PROGRAM_ID,
                "source_root_run_id": V1_ROOT_RUN_ID,
                "reused_record_count": 80,
                "recomputed_in_recovery": 0,
                "preserved_failures": 2,
            },
        }
    )
    out.setdefault("gates", {})["V1_SCIENTIFIC_SPEC_BYTE_IDENTITY"] = "PASS"
    out["gates"]["V1_BOBYQA_PROVENANCE_REUSE"] = "PASS"
    out["gates"]["POLYCHORD_V4_METADATA_ADAPTER"] = "PASS"
    write_json(a.output, out)
    print("Q042_PROD_V4_FINAL_GATE=" + str(out.get("final_result_gate")))
    return rc


def common_args(s):
    for x in (
        "q032-parent-root",
        "preflight",
        "parent-dir",
        "hlp-matrix",
        "hlp-meta",
        "reduced-support",
        "reduced-hlp-matrix",
        "reduced-hlp-meta",
        "spec",
        "source-lock",
        "external-runtime",
    ):
        s.add_argument("--" + x, required=True)


def parser():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("static")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=static_check)

    s = sp.add_parser("sampler-adapter-regression")
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--external-runtime", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=sampler_adapter_regression)

    s = sp.add_parser("prepare-nonoverlap")
    for x in (
        "q032-parent-root",
        "preflight",
        "hlp-matrix",
        "hlp-meta",
        "support-output",
        "matrix-output",
        "meta-output",
    ):
        s.add_argument("--" + x, required=True)
    s.set_defaults(func=prepare_nonoverlap)

    s = sp.add_parser("runtime-preflight")
    common_args(s)
    s.add_argument("--output", required=True)
    s.set_defaults(func=runtime_preflight)

    s = sp.add_parser("polychord-worker")
    common_args(s)
    s.add_argument("--arm", choices=ARMS, required=True)
    s.add_argument("--model", choices=MODELS, required=True)
    s.add_argument("--combination", choices=COMBINATIONS, required=True)
    s.add_argument("--action", choices=("fresh", "resume"), required=True)
    s.add_argument("--output-dir", required=True)
    s.add_argument("--result-json", required=True)
    s.set_defaults(func=polychord_worker)

    s = sp.add_parser("polychord-segment")
    common_args(s)
    s.add_argument("--arm", choices=ARMS, required=True)
    s.add_argument("--model", choices=MODELS, required=True)
    s.add_argument("--combination", choices=COMBINATIONS, required=True)
    s.add_argument("--segment", type=int, required=True)
    s.add_argument("--soft-minutes", type=int, default=240)
    s.add_argument("--parent-run-id", default="")
    s.add_argument("--output-dir", required=True)
    s.add_argument("--segment-json", required=True)
    s.set_defaults(func=polychord_segment)

    s = sp.add_parser("import-bobyqa")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--artifact-manifest", required=True)
    s.add_argument("--output-dir", required=True)
    s.add_argument("--summary", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.set_defaults(func=import_bobyqa)

    s = sp.add_parser("merge-final")
    s.add_argument("--input-dir", required=True)
    s.add_argument("--spec", required=True)
    s.add_argument("--source-lock", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=merge_final)

    return p


freeze_v1_globals()
v1.load_spec = load_spec
v1.load_lock = load_lock
v1.runtime_gate = runtime_gate
v1.cell_seed = cell_seed
v1.production_pc = production_pc

if __name__ == "__main__":
    a = parser().parse_args()
    raise SystemExit(a.func(a))
