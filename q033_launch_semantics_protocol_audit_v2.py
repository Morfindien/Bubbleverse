#!/usr/bin/env python3
"""
Bubbleverse Q-033 — historical launch-semantics protocol audit V2.

CURRENT_Q: Q-033
RUN_ID: Q033-CAMSPEC-LAUNCH-SEMANTICS-PROTOCOL-AUDIT-V2
RESULT_ID: R-Q033-EDE-LAUNCH-SEMANTICS-AUDIT-002

Why V2 exists
-------------
Q033 V1 preregistered a matched A/B experiment in which the historical Q022 arm
was assumed to contain non-scalar Cobaya ref distributions. Its preflight
correctly failed NONSCALAR_HISTORICAL_REFERENCE_GATE because reconstruction of
the actual Q019/Q021/Q022 runtime lineage produced no such non-scalar refs.

V2 does not weaken that failed gate. It tests the premise itself.

Scientific question
-------------------
Under the frozen CamSpec full-multifrequency MOD-EDE-N3 likelihood, can the
difference between historical Q022 stable-multibasin classification and Q032
V4 non-stable FULL_NATIVE classification be explained by launch/reference
semantics alone?

Decision rule
-------------
If the actual historical Q022 constructor resolves all Q022-sampled parameter
refs to finite scalars, then Q022 and Q032 V4 use the same Cobaya pointlike
reference semantics for the corresponding coordinates. In that case there is
no launch/reference-semantics variable to A/B test and Q033 is answered NO
without new likelihood optimization.

V2 then identifies, but does not execute, the smallest remaining implementation
difference: Q022 freezes the primordial block (n_s, logA, tau_reio) at each Q021
vertex while Q032 V4 FULL_NATIVE leaves those coordinates sampled and merely
assigns scalar refs.

No Q032 sector add-back is rerun. HiLLiPoP is not rerun. Basin thresholds,
physics, data, likelihood and backend commit remain untouched.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent

Q = "Q-033"
RUN = "Q033-CAMSPEC-LAUNCH-SEMANTICS-PROTOCOL-AUDIT-V2"
RESULT = "R-Q033-EDE-LAUNCH-SEMANTICS-AUDIT-002"
CONFIG_FILE = "q033_launch_semantics_protocol_audit_v2_config.yml"
SOURCE_LOCK_FILE = "q033_launch_semantics_source_lock_v2.json"

BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
Q022_RUN = "Q022-FULL-MF-OPTIMIZER-BASIN-CONTINUATION-V2"
Q022_RESULT = "R-Q022-EDE-FULLMF-OPTIMIZER-BASIN-002"
Q032_RUN = "Q032-EXACT-START-CONFORMANCE-ADDBACK-V4"
Q032_RESULT = "R-Q032-EDE-CAMSPEC-ADDBACK-004"
FULL_NATIVE = "full_native"
MASKS = (3, 6, 7)
SEEDS = (0, 1, 2)
START_LABELS = tuple(f"M{m}-S{s}" for m in MASKS for s in SEEDS)
PRIMORDIAL = ("n_s", "logA", "tau_reio")


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def json_default(x: Any) -> Any:
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer, np.floating, np.bool_)):
        return x.item()
    return str(x)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=json_default).encode()
    ).hexdigest()


def read_json(path: str | Path) -> dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return d


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, p)


def sampled(spec: Any) -> bool:
    return isinstance(spec, Mapping) and isinstance(spec.get("prior"), Mapping)


def is_scalar_ref(ref: Any) -> bool:
    return isinstance(ref, (int, float, np.integer, np.floating)) and finite(ref)


def git_blob(path: str | Path) -> str:
    import subprocess
    proc = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"GIT_BLOB_GATE=FAIL path={path} stderr={proc.stderr!r}")
    return proc.stdout.strip()


def load_cfg(path: str | Path = CONFIG_FILE) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    c = yaml.safe_load(p.read_text(encoding="utf-8"))
    if c["project"]["q"] != Q:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL")
    if c["project"]["run_id"] != RUN or c["project"]["result_id"] != RESULT:
        raise RuntimeError("RUN_IDENTITY_GATE=FAIL")
    m = c["model"]
    if m["name"] != "MOD-EDE-N3" or int(m["n_scf"]) != 3:
        raise RuntimeError("MODEL_IDENTITY_GATE=FAIL")
    if m["backend_commit"] != BACKEND_COMMIT:
        raise RuntimeError("BACKEND_COMMIT_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["masks"]) != MASKS:
        raise RuntimeError("MASK_IDENTITY_GATE=FAIL")
    if tuple(int(x) for x in c["starts"]["seed_restarts"]) != SEEDS:
        raise RuntimeError("SEED_IDENTITY_GATE=FAIL")
    if tuple(c["starts"]["labels"]) != START_LABELS:
        raise RuntimeError("START_LABEL_GATE=FAIL")
    if tuple(c["q022_parameterization"]["frozen_primordial"]) != PRIMORDIAL:
        raise RuntimeError("PRIMORDIAL_IDENTITY_GATE=FAIL")
    required = (
        "v1_failed_no_scientific_result",
        "audit_actual_runtime_lineage",
        "no_new_likelihood_optimization",
        "no_q032_sector_rerun",
        "hillipop_not_rerun",
        "no_new_seed_family",
        "no_threshold_change",
        "q022_raw_result_preserved",
        "q023_q030_fixed_vector_results_preserved",
        "q032_v4_raw_computation_preserved",
        "q032_v4_non_scalar_recovery_interpretation_revisable",
        "technical_failure_no_scientific_result",
        "stop_after_premise_resolution",
        "no_open_ended_search",
    )
    if not all(c["rules"].get(k) is True for k in required):
        raise RuntimeError("SCIENTIFIC_RULE_GATE=FAIL")
    return c


def load_source_lock() -> dict[str, Any]:
    d = read_json(ROOT / SOURCE_LOCK_FILE)
    if d.get("q") != Q or d.get("run_id") != RUN or d.get("result_id") != RESULT:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    for name, expected in d["bubbleverse_files"].items():
        p = ROOT / name
        if not p.exists():
            raise RuntimeError(f"SOURCE_FILE_GATE=FAIL missing={name}")
        actual = git_blob(p)
        if actual != expected:
            raise RuntimeError(
                f"HISTORICAL_SOURCE_BLOB_GATE=FAIL file={name} expected={expected} actual={actual}"
            )
    return d


def q022_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q022"
        and d.get("run_id") == Q022_RUN
        and d.get("result_id") == Q022_RESULT
        and d.get("FINAL_RESULT_GATE") == "PASS"
        and d.get("classification") == "STABLE_MIXED_COSMOLOGY_NUISANCE_MULTIBASIN_STRUCTURE"
    ):
        raise RuntimeError("Q022_HISTORICAL_RESULT_GATE=FAIL")
    return d


def q032_preflight_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("FINAL_PREFLIGHT_GATE") == "PASS"
    ):
        raise RuntimeError("Q032_V4_PREFLIGHT_GATE=FAIL")
    starts = d.get("q022_source_starts", {})
    if tuple(sorted(starts)) != tuple(sorted(START_LABELS)):
        raise RuntimeError("START_PROVENANCE_GATE=FAIL")
    if FULL_NATIVE not in d.get("surface_lock", {}).get("surfaces", {}):
        raise RuntimeError("Q032_V4_FULL_NATIVE_SURFACE_GATE=FAIL")
    return d


def q032_final_state(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == Q032_RUN
        and d.get("result_id") == Q032_RESULT
        and d.get("FINAL_RESULT_GATE") == "PASS"
        and d.get("actual_computed_result") is True
    ):
        raise RuntimeError("Q032_V4_FINAL_GATE=FAIL")
    ctrl = d.get("control_result")
    if not isinstance(ctrl, Mapping):
        raise RuntimeError("Q032_V4_CONTROL_GATE=FAIL missing control_result")
    r = ctrl.get("surface_results", {}).get(FULL_NATIVE, {})
    if r.get("stable_multibasin") is not False or int(r.get("stable_basin_count", -1)) != 0:
        raise RuntimeError("Q032_V4_FULL_NATIVE_NONSTABLE_GATE=FAIL")
    return d


def q022_runtime_template(mask: int, prefix: Path) -> tuple[dict[str, Any], list[str]]:
    """
    Reconstruct the exact Q021 zero-phase constructor that Q022 calls before it
    replaces sampled non-primordial refs by the harvested Q021 endpoint values.
    """
    import q021_primordial_decomposition_v1 as q21

    q22cfg = yaml.safe_load(
        (ROOT / "q022_globality_continuation_v2_config.yml").read_text(encoding="utf-8")
    )
    q21cfg = q21.load_cfg(ROOT / q22cfg["parents"]["q021_config"])
    info, _fixed, _like = q21.build_info(q21cfg, "full_mf", int(mask), 1, prefix)
    names = sorted(
        name
        for name, spec in info["params"].items()
        if q21.sampled(spec) and name not in q21.PRIMORDIAL
    )
    return info, names


def q022_ref_semantics_audit(mask: int, center: Mapping[str, float], prefix: Path) -> dict[str, Any]:
    import q021_primordial_decomposition_v1 as q21

    info, names = q022_runtime_template(mask, prefix)
    missing = [n for n in names if n not in center or not finite(center[n])]
    if missing:
        raise RuntimeError("Q022_ENDPOINT_VECTOR_COVERAGE_GATE=FAIL missing=" + repr(missing))

    before = {}
    after = {}
    for name in names:
        before[name] = copy.deepcopy(info["params"][name].get("ref"))
        q21.set_ref(info["params"], name, float(center[name]))
        after[name] = copy.deepcopy(info["params"][name].get("ref"))

    nonscalar_before = sorted(n for n, r in before.items() if not is_scalar_ref(r))
    nonscalar_after = sorted(n for n, r in after.items() if not is_scalar_ref(r))
    scalar_after = {n: float(after[n]) for n in names if is_scalar_ref(after[n])}

    return {
        "mask": int(mask),
        "historically_sampled_nonprimordial_names": names,
        "ref_types_before_q022_endpoint_recenter": {
            n: ("SCALAR" if is_scalar_ref(before[n]) else type(before[n]).__name__)
            for n in names
        },
        "ref_types_after_q022_endpoint_recenter": {
            n: ("SCALAR" if is_scalar_ref(after[n]) else type(after[n]).__name__)
            for n in names
        },
        "non_scalar_before": nonscalar_before,
        "non_scalar_after": nonscalar_after,
        "all_q022_sampled_refs_scalar_after_recenter": not nonscalar_after,
        "scalar_endpoint_ref_vector": scalar_after,
        "scalar_endpoint_ref_sha256": canonical_hash(scalar_after),
    }


def q032_full_native_sampled_audit(pf: Mapping[str, Any], center: Mapping[str, float], prefix: Path) -> dict[str, Any]:
    import q032_exact_start_addback_v4 as q32v4

    c32 = q32v4.load_cfg(ROOT / "q032_exact_start_addback_v4_config.yml")
    info = q32v4.build_camspec_surface_info(
        c32,
        pf["surface_lock"],
        FULL_NATIVE,
        center,
        prefix,
        "stage1",
    )
    names = sorted(name for name, spec in info["params"].items() if sampled(spec))
    refs = {name: copy.deepcopy(info["params"][name].get("ref")) for name in names}
    non_scalar = sorted(name for name, r in refs.items() if not is_scalar_ref(r))
    return {
        "sampled_parameter_names": names,
        "non_scalar_ref_names": non_scalar,
        "all_sampled_refs_scalar": not non_scalar,
        "scalar_ref_sha256": canonical_hash(
            {n: float(refs[n]) for n in names if is_scalar_ref(refs[n])}
        ),
    }


def audit(
    c: Mapping[str, Any],
    q032_preflight_path: str | Path,
    q032_final_path: str | Path,
    q022_final_path: str | Path,
    output: str | Path,
    manifest_output: str | Path,
) -> int:
    source_lock = load_source_lock()
    pf = q032_preflight_state(q032_preflight_path)
    q32 = q032_final_state(q032_final_path)
    q22 = q022_state(q022_final_path)

    # Audit all three Q022 vertex masks. Seed-restart changes the endpoint values,
    # not the ref representation type, so for every mask use one authoritative
    # Q022 provenance vector to audit constructor semantics, and separately prove
    # all nine labels exist in the sealed Q032 provenance mapping.
    per_mask = {}
    for mask in MASKS:
        label = f"M{mask}-S0"
        center = dict(pf["q022_source_starts"][label]["params"])
        per_mask[str(mask)] = q022_ref_semantics_audit(
            mask, center, ROOT / f"q033_runtime/v2_q022_m{mask}"
        )

    q022_all_scalar = all(
        x["all_q022_sampled_refs_scalar_after_recenter"] for x in per_mask.values()
    )
    if not q022_all_scalar:
        raise RuntimeError(
            "Q022_POINTLIKE_REFERENCE_GATE=FAIL "
            "V2 expected premise correction but found genuine non-scalar refs"
        )

    probe_center = dict(pf["q022_source_starts"]["M3-S0"]["params"])
    q32audit = q032_full_native_sampled_audit(
        pf, probe_center, ROOT / "q033_runtime/v2_q032_full_native"
    )
    if not q32audit["all_sampled_refs_scalar"]:
        raise RuntimeError("Q032_V4_SCALAR_REFERENCE_GATE=FAIL")

    q022_names = set(per_mask["3"]["historically_sampled_nonprimordial_names"])
    q032_names = set(q32audit["sampled_parameter_names"])
    q032_only = sorted(q032_names - q022_names)
    q022_only = sorted(q022_names - q032_names)

    expected_q032_only = sorted(PRIMORDIAL)
    if q032_only != expected_q032_only or q022_only:
        raise RuntimeError(
            "SMALLEST_REMAINING_PARAMETERIZATION_DELTA_GATE=FAIL "
            f"q032_only={q032_only!r} q022_only={q022_only!r}"
        )

    classification = "LAUNCH_REFERENCE_SEMANTICS_ALREADY_IDENTICAL_NOT_CAUSAL"
    answer = "NO"
    final_gate = "PASS"

    result = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_LAUNCH_SEMANTICS_PROTOCOL_AUDIT_FINAL",
        "status": "PASS",
        "execution_status": "COMPLETE",
        "tests_status": "COMPLETE",
        "actual_new_likelihood_optimization": False,
        "scientific_question": c["project"]["scientific_question"],
        "q033_answer": answer,
        "classification": classification,
        "reason": (
            "The actual historical Q019/Q021/Q022 runtime lineage resolves the "
            "Q022-sampled non-primordial parameter refs to finite scalar values. "
            "Q021.set_ref therefore recenters scalar refs to scalar endpoint values; "
            "it does not preserve a hidden ref distribution in this executed lineage. "
            "Q032 V4 also uses scalar refs. Launch/reference representation is thus "
            "not a differing variable capable of explaining Q022-vs-Q032 V4."
        ),
        "q022_runtime_ref_audit": per_mask,
        "q032_v4_full_native_ref_audit": q32audit,
        "parameterization_delta": {
            "id": "D-Q033-REMAINING-001",
            "status": "IDENTIFIED_NOT_EXECUTED",
            "q022_sampled_nonprimordial": sorted(q022_names),
            "q032_full_native_sampled": sorted(q032_names),
            "q032_only_sampled_coordinates": q032_only,
            "q022_only_sampled_coordinates": q022_only,
            "interpretation": (
                "Q022 freezes n_s, logA and tau_reio at each Q021 primordial vertex. "
                "Q032 V4 FULL_NATIVE leaves those coordinates sampled and assigns "
                "them scalar refs. This is the smallest remaining implementation "
                "difference after launch/reference semantics is eliminated."
            ),
            "next_test_if_routed": (
                "A future case may match the Q022 frozen-primordial parameterization "
                "against Q032 V4 FULL_NATIVE while holding scalar refs and all other "
                "components fixed. Q033 itself stops here."
            ),
        },
        "parent_results": {
            "Q022": {
                "run_id": q22["run_id"],
                "result_id": q22["result_id"],
                "classification": q22["classification"],
                "status": "KEEP_HISTORICAL_RAW_RESULT",
            },
            "Q032_V4": {
                "run_id": q32["run_id"],
                "result_id": q32["result_id"],
                "classification": q32["classification"],
                "status": "KEEP_RAW_COMPUTATION_REVISE_START_SEMANTICS_INTERPRETATION",
            },
        },
        "v1_status": {
            "run_id": "Q033-CAMSPEC-LAUNCH-SEMANTICS-MATCHED-AB-V1",
            "result_id": "R-Q033-EDE-CAMSPEC-LAUNCH-SEMANTICS-001",
            "status": "FAILED_PREFLIGHT_NO_SCIENTIFIC_RESULT",
            "failure": "NONSCALAR_HISTORICAL_REFERENCE_GATE=FAIL",
            "meaning": "CORRECTLY_EXPOSED_FALSE_PREMISE; NOT_A_NEGATIVE_LIKELIHOOD_RESULT",
        },
        "source_lock_sha256": canonical_hash(source_lock),
        "mandatory_gates": {
            "CONTEXT_CONTINUITY_GATE": "PASS",
            "Q_IDENTITY_GATE": "PASS",
            "HISTORICAL_SOURCE_BLOB_GATE": "PASS",
            "Q022_HISTORICAL_RESULT_GATE": "PASS",
            "Q032_V4_FINAL_GATE": "PASS",
            "START_PROVENANCE_GATE": "PASS",
            "Q022_POINTLIKE_REFERENCE_GATE": "PASS",
            "Q032_V4_SCALAR_REFERENCE_GATE": "PASS",
            "LAUNCH_REFERENCE_SEMANTICS_IDENTITY_GATE": "PASS",
            "SMALLEST_REMAINING_PARAMETERIZATION_DELTA_GATE": "PASS",
            "NO_NEW_LIKELIHOOD_EXECUTION_GATE": "PASS",
            "ANTI_LOOP_STOP_GATE": "PASS",
            "SCIENTIFIC_INTERPRETATION_GATE": "PASS",
            "FINAL_RESULT_GATE": final_gate,
        },
        "journal_effect": {
            "Q022": (
                "KEEP raw historical stable-multibasin result. Restore/correct the "
                "technical provenance: its Q022 sampled refs were scalar pointlike "
                "endpoint refs in the executed lineage; do not describe them as "
                "non-scalar reference distributions."
            ),
            "Q023_Q030": (
                "KEEP fixed-vector diagnostics. Their interpretation remains conditional "
                "on the historical Q022 endpoint family."
            ),
            "Q032_V4": (
                "KEEP authoritative raw computational result and no-clean-sector-localization "
                "result. SUPERSEDE only the claim that V4 corrected historical Q022 "
                "non-scalar ref-distribution launch semantics."
            ),
            "HYP_Q033_A": "FALSIFIED_AS_STATED",
            "HYP_Q033_B": "STRENGTHENED; D-Q033-REMAINING-001 IDENTIFIED",
            "CASE031": "KEEP_CLOSED",
        },
        "next_required_action": (
            "RETURN_TO_RESULT_INGESTION_AND_ROUTING_ENGINE. STOP Q033. "
            "DO NOT RUN THE V1 18-SHARD A/B PROGRAM. If another case is opened, "
            "test D-Q033-REMAINING-001 as the smallest remaining matched difference."
        ),
        "return_route": "BUBBLEVERSE_RESULT_INGESTION_AND_ROUTING_ENGINE",
        "FINAL_RESULT_GATE": final_gate,
    }
    write_json(output, result)

    manifest = {
        "q": Q,
        "run_id": RUN,
        "result_id": RESULT,
        "stage": "Q033_V2_JOB_MANIFEST_FINAL",
        "status": "COMPLETE",
        "new_likelihood_optimizer_jobs": 0,
        "audit_jobs": 1,
        "v1_optimizer_jobs_cancelled_as_unnecessary": 18,
        "final_result_gate": final_gate,
    }
    write_json(manifest_output, manifest)
    print("Q033_V2_PROTOCOL_AUDIT_GATE=PASS")
    print("Q033_ANSWER=NO")
    print("Q033_CLASSIFICATION=" + classification)
    print("FINAL_RESULT_GATE=PASS")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=CONFIG_FILE)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit")
    a.add_argument("--q032-preflight", required=True)
    a.add_argument("--q032-final", required=True)
    a.add_argument("--q022-final", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--manifest-output", required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    c = load_cfg(args.config)
    if args.cmd == "audit":
        return audit(
            c,
            args.q032_preflight,
            args.q032_final,
            args.q022_final,
            args.output,
            args.manifest_output,
        )
    raise RuntimeError("COMMAND_GATE=FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
