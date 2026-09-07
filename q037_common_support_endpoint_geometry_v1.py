#!/usr/bin/env python3
"""Bubbleverse Q-037 — exact-TT-common-support endpoint geometry analysis V1.

Artifact-only deterministic analysis of the already validated Q032 CamSpec and
HiLLiPoP refinement endpoints. No CLASS, likelihood, optimizer or sampler is
executed. Cross-likelihood objective values are neither subtracted nor summed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any, Mapping, Sequence

Q = "Q-037"
PROGRAM_ID = "Q037-TTGEOM-V1"
RUN_ID = "Q037-TT-COMMON-SUPPORT-ENDPOINT-GEOMETRY-V1"
RESULT_ID = "R-Q037-EDE-TT-COMMON-SUPPORT-GEOMETRY-001"
PARENT_Q032_RESULT = "R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002"
PARENT_Q032_RUN = "Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2"
BACKEND_COMMIT = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
HILLIPOP_COMMIT = "a09ddde3e7ce11df99f74685feb1f1764cafb251"
EXPECTED_LABELS = tuple(f"M{m}-S{s}" for m in (3, 6, 7) for s in (0, 1, 2))
COORDS = ("omega_b", "omega_cdm", "fEDE", "log10z_c", "thetai_scf", "H0", "A_planck")
SCALES = {
    "omega_b": 3.644915744246274e-05,
    "omega_cdm": 2.9761589951235456e-04,
    "fEDE": 1.0851930861718734e-03,
    "log10z_c": 3.666125981785351e-02,
    "thetai_scf": 1.2826810796868315e-02,
    "H0": 2.253286448991929e-01,
    "A_planck": 3.7111561222435974e-04,
}
LOCKED_SCALES_HASH = "732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6"
THRESHOLD = 0.10


def read_json(path: str | Path) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON_OBJECT_GATE=FAIL path={path}")
    return obj


def write_json(path: str | Path, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except Exception:
        return False


def metric(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    terms = []
    for name in COORDS:
        if not (finite(a.get(name)) and finite(b.get(name)) and SCALES[name] > 0):
            raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL coordinate={name}")
        terms.append((float(a[name]) - float(b[name])) / SCALES[name])
    return float(math.sqrt(sum(x * x for x in terms) / len(terms)))


def validate_preregister(pr: Mapping[str, Any]) -> None:
    p = pr.get("project", {})
    if p != {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
    }:
        raise RuntimeError("Q_IDENTITY_GATE=FAIL preregister")
    cg = pr.get("common_geometry", {})
    if tuple(cg.get("coordinates", [])) != COORDS:
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL preregister")
    if cg.get("locked_scales") != SCALES or cg.get("locked_scales_hash") != LOCKED_SCALES_HASH:
        raise RuntimeError("Q031_LOCKED_SCALE_GATE=FAIL preregister")
    if float(cg.get("materiality_threshold", -1)) != THRESHOLD:
        raise RuntimeError("MATERIALITY_THRESHOLD_GATE=FAIL preregister")
    rules = pr.get("rules", {})
    must = (
        "q035_remains_authoritative_closed",
        "q036_remains_closed",
        "stable_label_not_sole_discriminator",
        "q022_mask_labels_are_provenance_only",
        "no_cross_likelihood_absolute_objective_subtraction",
        "no_cross_likelihood_objective_sum",
        "no_forced_native_nuisance_mapping",
        "shared_planck_sky_not_independent_observations",
        "no_q032_likelihood_rerun",
        "no_threshold_tuning",
        "no_scale_tuning",
        "preserve_unexpected_raw_output",
        "no_physical_systematic_claim_from_q037_alone",
        "stop_after_a_b_c_decision",
    )
    if not all(rules.get(k) is True for k in must):
        raise RuntimeError("PREREGISTER_RULE_GATE=FAIL")


def validate_source_lock(lock: Mapping[str, Any]) -> None:
    if lock.get("q") != Q or lock.get("program_id") != PROGRAM_ID:
        raise RuntimeError("SOURCE_LOCK_IDENTITY_GATE=FAIL")
    q32 = lock.get("q032", {})
    if q32.get("run_id") != 33994305721 or q32.get("result_id") != PARENT_Q032_RESULT:
        raise RuntimeError("PARENT_Q032_PROVENANCE_GATE=FAIL")
    if q32.get("execution_commit") != "4dc873a5e880d40858d831a3b421456728f0c032":
        raise RuntimeError("PARENT_Q032_COMMIT_GATE=FAIL")
    analysis = lock.get("analysis_lock", {})
    if tuple(analysis.get("coordinates", [])) != COORDS:
        raise RuntimeError("COMMON_COORDINATE_GATE=FAIL source_lock")
    if analysis.get("locked_scales") != SCALES or analysis.get("locked_scales_hash") != LOCKED_SCALES_HASH:
        raise RuntimeError("Q031_LOCKED_SCALE_GATE=FAIL source_lock")
    if float(analysis.get("materiality_threshold", -1)) != THRESHOLD:
        raise RuntimeError("MATERIALITY_THRESHOLD_GATE=FAIL source_lock")


def load_q032_final(path: str | Path) -> dict[str, Any]:
    d = read_json(path)
    if not (
        d.get("q") == "Q-032"
        and d.get("run_id") == PARENT_Q032_RUN
        and d.get("result_id") == PARENT_Q032_RESULT
        and d.get("status") == "PASS"
        and d.get("execution_status") == "COMPLETE"
        and d.get("actual_computed_result") is True
    ):
        raise RuntimeError("PARENT_Q032_FINAL_GATE=FAIL")
    support = d.get("support_sha256")
    if not isinstance(support, str) or len(support) != 64:
        raise RuntimeError("EXACT_COMMON_SUPPORT_IDENTITY_GATE=FAIL q032_final")
    return d


def expected_filename(implementation: str, label: str) -> str:
    mask = label[1]
    seed = label[-1]
    return f"{implementation}_m{mask}_s{seed}.json"


def load_refinements(root: str | Path, q032_final: Mapping[str, Any]) -> tuple[dict[str, dict[str, dict[str, float]]], dict[str, Any]]:
    root = Path(root)
    if not root.exists():
        raise RuntimeError("PARENT_Q032_ARTIFACT_GATE=FAIL root_missing")

    rows: dict[str, dict[str, dict[str, float]]] = {"camspec": {}, "hillipop": {}}
    provenance: dict[str, Any] = {}
    support_expected = str(q032_final["support_sha256"])

    for implementation in ("camspec", "hillipop"):
        for label in EXPECTED_LABELS:
            name = expected_filename(implementation, label)
            matches = list(root.rglob(name))
            if len(matches) != 1:
                raise RuntimeError(
                    f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL file={name} matches={len(matches)}"
                )
            path = matches[0]
            d = read_json(path)
            mask = int(label[1])
            seed = int(label[-1])

            optional_identity_ok = (
                (d.get("q") in (None, "Q-032"))
                and (d.get("run_id") in (None, PARENT_Q032_RUN))
                and (d.get("result_id") in (None, PARENT_Q032_RESULT))
            )
            if not optional_identity_ok:
                raise RuntimeError(f"PARENT_Q032_PROVENANCE_GATE=FAIL identity={name}")
            if not (
                d.get("stage") == "Q032_REFINEMENT"
                and d.get("phase") == "refinement"
                and d.get("implementation") == implementation
                and int(d.get("source_mask", -1)) == mask
                and int(d.get("source_seed", -1)) == seed
                and d.get("source_label") == label
                and d.get("source_semantics") == "Q022_START_PROVENANCE_ONLY_NOT_HILLIPOP_MASK"
                and d.get("seed_semantics") == "EXACT_MATCHED_Q032_STAGE1_MINIMUM"
                and d.get("status") == "COMPLETE"
                and d.get("actual_computed_result") is True
                and d.get("cross_likelihood_objective_comparison_performed") is False
                and d.get("backend_commit") == BACKEND_COMMIT
                and d.get("support_sha256") == support_expected
            ):
                raise RuntimeError(f"PARENT_Q032_PROVENANCE_GATE=FAIL record={name}")
            if implementation == "hillipop" and d.get("hillipop_commit") != HILLIPOP_COMMIT:
                raise RuntimeError(f"PARENT_Q032_PROVENANCE_GATE=FAIL hillipop_commit={name}")

            minimum = d.get("minimum")
            if not isinstance(minimum, Mapping):
                raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL minimum={name}")
            vector = {}
            for coord in COORDS:
                if coord not in minimum or not finite(minimum[coord]):
                    raise RuntimeError(f"COMMON_COORDINATE_GATE=FAIL {name}:{coord}")
                vector[coord] = float(minimum[coord])
            rows[implementation][label] = vector
            provenance[f"{implementation}:{label}"] = {
                "source_file": str(path),
                "sha256": sha256_file(path),
                "support_sha256": support_expected,
                "objective_present_but_not_used": "objective_chi2" in d,
            }

    for implementation in rows:
        if tuple(sorted(rows[implementation])) != tuple(sorted(EXPECTED_LABELS)):
            raise RuntimeError(f"NINE_BY_NINE_LABEL_IDENTITY_GATE=FAIL implementation={implementation}")
    return rows, provenance


def calculate(rows: Mapping[str, Mapping[str, Mapping[str, float]]]) -> dict[str, Any]:
    camspec = rows["camspec"]
    hillipop = rows["hillipop"]
    matched = {label: metric(camspec[label], hillipop[label]) for label in EXPECTED_LABELS}

    c_centroid = {c: statistics.mean(camspec[l][c] for l in EXPECTED_LABELS) for c in COORDS}
    h_centroid = {c: statistics.mean(hillipop[l][c] for l in EXPECTED_LABELS) for c in COORDS}
    centroid = metric(c_centroid, h_centroid)

    cp: dict[str, float] = {}
    hp: dict[str, float] = {}
    drift: dict[str, float] = {}
    for a, b in combinations(EXPECTED_LABELS, 2):
        key = f"{a}|{b}"
        dc = metric(camspec[a], camspec[b])
        dh = metric(hillipop[a], hillipop[b])
        cp[key] = dc
        hp[key] = dh
        drift[key] = abs(dh - dc)

    return {
        "matched_endpoint_rms": matched,
        "matched_median_displacement": float(statistics.median(matched.values())),
        "matched_max_displacement": float(max(matched.values())),
        "matched_exceedance_count_gt_0_10": int(sum(v > THRESHOLD for v in matched.values())),
        "normalized_centroid_displacement": float(centroid),
        "camspec_internal_pairwise_distances": cp,
        "hillipop_internal_pairwise_distances": hp,
        "absolute_pairwise_distance_drifts": drift,
        "pairwise_median_drift": float(statistics.median(drift.values())),
        "pairwise_max_drift": float(max(drift.values())),
        "pairwise_exceedance_count_gt_0_10": int(sum(v > THRESHOLD for v in drift.values())),
    }


def decision(metrics: Mapping[str, Any]) -> dict[str, Any]:
    location_material = (
        float(metrics["matched_median_displacement"]) > THRESHOLD
        or float(metrics["normalized_centroid_displacement"]) > THRESHOLD
    )
    shape_material = float(metrics["pairwise_median_drift"]) > THRESHOLD
    if location_material or shape_material:
        return {
            "stop_case": "A",
            "classification": "COMMON_SUPPORT_DOES_NOT_REMOVE_IMPLEMENTATION_GEOMETRY_DIFFERENCE",
            "location_material": bool(location_material),
            "shape_material": bool(shape_material),
            "journal_effect": "STRENGTHEN_C036_IMPL_AND_WEAKEN_DATA_SUPPORT_AS_PRIMARY_EXPLANATION",
        }
    return {
        "stop_case": "B",
        "classification": "INFORMATION_SUPPORT_RESTRICTION_MATERIALLY_EXPLAINS_OR_LOCALIZES_Q036_DIFFERENCE",
        "location_material": False,
        "shape_material": False,
        "journal_effect": "LOCALIZE_Q036_DIFFERENCE_TO_ELEMENTS_REMOVED_BY_Q032_COMMON_SUPPORT",
    }


def permutation_invariance(rows: Mapping[str, Mapping[str, Mapping[str, float]]], baseline: Mapping[str, Any]) -> bool:
    # Reversing label traversal must not alter the symmetric metric summaries.
    labels = tuple(reversed(EXPECTED_LABELS))
    matched = [metric(rows["camspec"][l], rows["hillipop"][l]) for l in labels]
    drifts = []
    for a, b in combinations(labels, 2):
        dc = metric(rows["camspec"][a], rows["camspec"][b])
        dh = metric(rows["hillipop"][a], rows["hillipop"][b])
        drifts.append(abs(dh - dc))
    return (
        abs(statistics.median(matched) - float(baseline["matched_median_displacement"])) <= 1e-12
        and abs(statistics.median(drifts) - float(baseline["pairwise_median_drift"])) <= 1e-12
        and abs(max(drifts) - float(baseline["pairwise_max_drift"])) <= 1e-12
    )


def technical_result(reason: str, preregister: str, source_lock: str) -> dict[str, Any]:
    return {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "execution_status": "TECHNICAL_INCONCLUSIVE",
        "actual_computed_result": False,
        "q037_stop_case": "C",
        "final_classification": "INCONCLUSIVE_TECHNICAL",
        "FINAL_RESULT_GATE": "UNRESOLVED",
        "technical_reason": reason,
        "preregister_sha256": sha256_file(preregister) if Path(preregister).exists() else None,
        "source_lock_sha256": sha256_file(source_lock) if Path(source_lock).exists() else None,
        "claim_boundaries": {
            "q035_classifier_harmonization_remains_authoritative": True,
            "q036_remains_closed": True,
            "physical_planck_systematic_established": False,
            "ede_preference_established": False,
            "ede_falsification_established": False,
            "h0_changed": False,
        },
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    prereg = read_json(args.preregister)
    lock = read_json(args.source_lock)
    validate_preregister(prereg)
    validate_source_lock(lock)

    source_gate = read_json(args.source_gate)
    if source_gate.get("status") != "PASS" or source_gate.get("q") != Q:
        raise RuntimeError("SOURCE_ARTIFACT_DIGEST_GATE=FAIL")

    q032_final = load_q032_final(args.q032_final)
    rows, provenance = load_refinements(args.q032_dir, q032_final)
    metrics = calculate(rows)
    dec = decision(metrics)

    gates = {
        "Q_IDENTITY_GATE": True,
        "PARENT_Q032_PROVENANCE_GATE": True,
        "SOURCE_ARTIFACT_DIGEST_GATE": True,
        "Q035_BASELINE_PRESERVATION_GATE": True,
        "Q036_CLOSED_PRESERVATION_GATE": True,
        "NINE_BY_NINE_LABEL_IDENTITY_GATE": True,
        "COMMON_COORDINATE_GATE": True,
        "Q031_LOCKED_SCALE_GATE": True,
        "MATERIALITY_THRESHOLD_GATE": True,
        "EXACT_COMMON_SUPPORT_IDENTITY_GATE": True,
        "NO_CROSS_LIKELIHOOD_OBJECTIVE_GATE": True,
        "FINITE_RESULT_GATE": all(
            finite(v)
            for k, v in metrics.items()
            if isinstance(v, (int, float))
        ),
        "PERMUTATION_INVARIANCE_GATE": permutation_invariance(rows, metrics),
    }
    if not all(gates.values()):
        raise RuntimeError("MANDATORY_ANALYSIS_GATE=FAIL")

    result = {
        "q": Q,
        "program_id": PROGRAM_ID,
        "run_id": RUN_ID,
        "result_id": RESULT_ID,
        "scientific_question": prereg["scientific_question"],
        "execution_mode": "ARTIFACT_ONLY_DETERMINISTIC_PROGRAM",
        "execution_status": "COMPLETE",
        "actual_computed_result": True,
        "parent_q032": {
            "run_id": 33994305721,
            "result_id": PARENT_Q032_RESULT,
            "execution_commit": lock["q032"]["execution_commit"],
            "support_sha256": q032_final["support_sha256"],
        },
        "common_geometry": {
            "coordinates": list(COORDS),
            "locked_scales": SCALES,
            "locked_scales_hash": LOCKED_SCALES_HASH,
            "metric": "sqrt(mean(((a_i-b_i)/scale_i)^2))",
            "materiality_threshold": THRESHOLD,
            "objective_values_used": False,
        },
        "raw_endpoint_vectors": rows,
        "endpoint_provenance": provenance,
        "descriptors": metrics,
        "decision": dec,
        "q037_stop_case": dec["stop_case"],
        "final_classification": dec["classification"],
        "journal_effect": dec["journal_effect"],
        "gates": gates,
        "claim_boundaries": {
            "q035_classifier_harmonization_remains_authoritative": True,
            "q036_remains_closed": True,
            "camspec_hillipop_are_independent_observations": False,
            "physical_planck_systematic_established": False,
            "instrument_failure_established": False,
            "foreground_error_established": False,
            "covariance_defect_established": False,
            "ede_preference_established": False,
            "ede_falsification_established": False,
            "new_physics_established": False,
            "h0_changed": False,
            "causal_component_attribution_performed": False,
        },
        "preregister_sha256": sha256_file(args.preregister),
        "source_lock_sha256": sha256_file(args.source_lock),
        "source_gate_sha256": sha256_file(args.source_gate),
        "FINAL_RESULT_GATE": "PASS",
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q032-dir", required=True)
    ap.add_argument("--q032-final", required=True)
    ap.add_argument("--preregister", required=True)
    ap.add_argument("--source-lock", required=True)
    ap.add_argument("--source-gate", required=True)
    ap.add_argument("--output", default="q037_final_v1.json")
    ap.add_argument("--raw-output", default="q037_raw_endpoints_v1.json")
    args = ap.parse_args()

    try:
        result = run(args)
        write_json(args.raw_output, {
            "q": Q,
            "program_id": PROGRAM_ID,
            "parent_q032_run_id": 33994305721,
            "raw_endpoint_vectors": result["raw_endpoint_vectors"],
            "endpoint_provenance": result["endpoint_provenance"],
        })
        write_json(args.output, result)
        print(f"FINAL_RESULT_GATE={result['FINAL_RESULT_GATE']}")
        print(f"Q037_STOP_CASE={result['q037_stop_case']}")
        print(f"FINAL_CLASSIFICATION={result['final_classification']}")
        return 0
    except Exception as exc:
        result = technical_result(str(exc), args.preregister, args.source_lock)
        write_json(args.output, result)
        print("FINAL_RESULT_GATE=UNRESOLVED")
        print("Q037_STOP_CASE=C")
        print(f"TECHNICAL_REASON={exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
